#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for 海戦JS
#---------------------------------------------------------------------
# ニュースモジュール
#	トップページにお知らせを表示するためのものです。
#---------------------------------------------------------------------
BEGIN {
	# Perl 5.004 以上が必要
	require 5.004;

########################################
	# エラー表示
	$SIG{__WARN__} = $SIG{__DIE__} =
	sub {
		my($msg) = @_;

		$msg =~ s/\n/<br>/g;
		print STDOUT <<END;
Content-type: text/html; charset=EUC-JP

<p><big><tt><b>ERROR:</b><br>$msg</tt></big></p>
END
		exit(-1);
	};
########################################
}
#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
# 初期設定用ファイルを読み込む
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '箱庭ニュース';

# 冒頭のメッセージ(HTML書式)
$headKill = <<"EOF";
<h1>$Htitle ニュース（管理用）</h1>
EOF

#ここまで-------------------------------------------------------------

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
	close(PIN);
}
&cookieInput;
&cgiInput;

$HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : "${HtagBig_}<small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}";

if($HskinName ne '' ){
	$baseSKIN = $HskinName;
} else {
	$baseSKIN = "${HcssDir}/$HcssDefault";
}

if(!(&readIslandsFile())){
	&htmlHeader;
	&htmlError;
} else {
	if(!checkSpecialPassword($HdefaultPassword)) {
		&htmlHeader;
		tempWrongPassword(); # パスワード違い
		&htmlFooter;
		exit(0);
	}

	if($HmainMode eq 'news') {
		&newsMain;
	}
	&htmlHeader;
	out("<DIV align='center'>");
	out($headKill);
	# ヘッダのコメントを書き換える場合(hako-init.cgiと連動)
	if($HlayoutTop) {
		&tempNews(0);
	} else {
		&tempNews(1);
	}
	out("</DIV>");
}
&htmlFooter;
#終了
exit(0);

#サブルーチン---------------------------------------------------------
#--------------------------------------------------------------------
#	POST or GETで入力されたデータ取得
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	if($getLine =~ /pass=([^\&]*)/) {
		# 最初の起動
		$HdefaultPassword = htmlEscape($1);
	}
	if($line =~ /NewsComment=([^\&]*)\&/) {
		$HdefaultPassword = htmlEscape($1);
		$line =~ /LAYOUT=([0-9])\&/;
		$Hlayout = $1;
		$line =~ /TYPE=([0-9])\&/;
		$Htype = $1;
		$line =~ s/(.*)NEWS([0-9])=//g;
		$HnewsComment = $line;
		$HmainMode = 'news';
	}
}

#---------------------------------------------------------------------
#	関数名 : htmlHeader
#	機　能 : HTMLのヘッダ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlHeader {
	if($HimgLine ne '' ){
		$baseIMG = $HimgLine;
	} else {
		$baseIMG = $HimageDir;
	}
	if($HskinName ne '' ){
		$baseSKIN = $HskinName;
	} else {
		$baseSKIN = "${HcssDir}/$HcssDefault";
	}
	if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ && $Hgzip == 1){
		print qq{Content-type: text/html; charset=EUC-JP\n};
		print qq{Content-encoding: gzip\n\n};
		open(STDOUT,"| $HpathGzip/gzip -1 -c");
		print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}else{
		print qq{Content-type: text/html; charset=EUC-JP\n\n};
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}
	my $term = '';
	$term = ($HislandTurn < $HarmisticeTurn) ? "(〜$HarmisticeTurn <small>停戦期間</small>)" : ($HislandTurn == $HarmisticeTurn) ? '(<small>次ターンより戦闘期間</small>)' : '(<small>戦闘期間</small>)' if($HarmisticeTurn);

	out(<<END);
<HTML>
<HEAD>
<TITLE>
$title
</TITLE>
<BASE HREF="$baseIMG/">
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
$Hheader
END

	my $nextturn = '';
	foreach (1..$HrepeatTurn) {
		$nextturn .= '・' if($_ != 1);
		$nextturn .= $HislandTurn + $_;
		last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
	}
	out(<<END) if(defined $HleftTime);
<HR>
<H1 style="display:inline;"><SMALL><B>ターン</B> </SMALL>$HislandTurn<SMALL>${term}</SMALL>　</H1>
<span ID="REALTIME" class="timer"></span>
<SCRIPT language="JavaScript">
<!--
var leftTime = $HleftTime;
var hour, min, sec;

function showTimeLeft() {
	if (leftTime > 0) {
		setTimeout('showTimeLeft()', 1000);

		hour = Math.floor(leftTime / 3600);
		min  = Math.floor(leftTime % 3600 / 60);
		sec  = leftTime % 60;
		leftTime--;

		document.all.REALTIME.innerHTML = '次回更新(<span class="number">ターン$nextturn</span>)まで残り ' + hour + '時間 ' + min + '分 ' + sec + '秒 ($HnextTime)';
	} else {
		document.all.REALTIME.innerHTML = 'ターン更新時刻になりました！ ($HnextTime)';
	}
}

if ($HplayNow) {
	showTimeLeft();
} else {
	document.all.REALTIME.innerHTML = 'ゲームは終了しました！';
}
//-->
</SCRIPT>
END

	out(<<END);
<HR></DIV>
$HtempBack2
END
}
#---------------------------------------------------------------------
#	関数名 : htmlFooter
#	機　能 : HTMLのフッタ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlFooter {
	out(<<END);
<HR>
<DIV ID='LinkFoot'>
$Hfooter
<BR></DIV>
END
##### 追加 親方20020307
	if($Hperformance) {
		my($uti, $sti, $cuti, $csti) = times();
		$uti += $cuti;
		$sti += $csti;
		my($cpu) = $uti + $sti;

	#	   ログファイル書き出し(テスト計測用　普段はコメントにしておいてください)
	#	   open(POUT,">>cpu-h.log");
	#	   print POUT "CPU($cpu) : user($uti) system($sti)\n";
	#	   close(POUT);

		out(<<END);
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV>
END
	}
#####
	out(<<END);
</DIV></BODY>
</HTML>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlError
#	機　能 : HTMLのエラーメッセージの出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlError{
	out("<H2>エラーが発生しました</H2>\n");
}

sub tempNews {
	my($type) = @_;
	my $newsline;
	my $layout=0;
	if(-e $Hnewsfile) {
		open(NEWS, $Hnewsfile);
		$layout = <NEWS>;
		my @news = <NEWS>;
		close(NEWS);
		$newsline = join(/\n/, @news);
		chomp($newsline);
	}
	my @check = ();
	$check[$layout] = ' CHECKED';
	my $po =<<"END";
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="0"$check[0]>ヘッダーリンク直下　
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="1"$check[1]>ターン表示直下　
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="2"$check[2]>フッターリンク直上
END
	my $str = (!$type) ? 'NEWS : レイアウト機能使用' : $po;
	out(<<END);
<TABLE>
<TR></TR>
<FORM name="f$type" action="${HbaseDir}/hako-news.cgi" method="POST">
<TR><TD colspan=4><big><B>コメント変更($str)</B></big>
　<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="NewsComment">
　<INPUT TYPE="hidden" VALUE="$type" NAME="TYPE">
　<INPUT TYPE="submit" VALUE="変更">
</TD></TR>
<TR><TD colspan=4>
<P ALIGN="center">
<TABLE BORDER=2><TR><TD style="border-style:inset;">
<textarea name="NEWS$type" cols=100 rows=20 WRAP="soft">$newsline</textarea><BR>
</TD></TR></TABLE>
↓↓↓　Preview　↓↓↓
<TABLE BORDER=2><TR><TD style="border-style:inset;">
<span ID="outputN$type"></span><br>
<SCRIPT LANGUAGE=javascript>
<!--
outputN${type}.setExpression("innerHTML","f${type}.NEWS${type}.value");
//-->
</SCRIPT>
</TD></TR></TABLE>
</TD>
</FORM>
</TR>
</TABLE>
END
}

sub newsMain {

	if(!checkSpecialPassword($HdefaultPassword)) {
		&htmlHeader;
		tempWrongPassword(); # パスワード違い
		&htmlFooter;
		exit(0);
	}
	if($HnewsComment eq '') {
		unlink($Hnewsfile) if(-e $Hnewsfile);
	} else {
		jcode::convert(\$HnewsComment, 'euc');
		my $rn = "\n";
		$HnewsComment =~ s/\r$rn/$rn/eg;
		open(NEWS, ">$Hnewsfile");
		print NEWS $Hlayout . "\n";
		print NEWS $HnewsComment;
		close(NEWS);
	}
	$Hnews = $HnewsComment;
}