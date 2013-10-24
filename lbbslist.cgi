#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for 海戦JS
# 　lbbslist.cgi?pass=[マスタパス]でアクセスすると、投稿欄もつきます。
# 　投稿する時の投稿名は管理者名で、島名は「管理人」になります。
# 　注！クッキーにマスタパスを喰ってる場合は、普通にアクセスするだけでOK!
#---------------------------------------------------------------------
#	
#	究想の箱庭　ローカル掲示板を一覧表示
#
#	作成日 : 2001/10/06 (ver0.10)
#	作成者 : ラスティア <nayupon@mail.goo.ne.jp>
#
#	管理者が島民の発言を逃さないよう一覧で確認するためのものです。
#	lbbslist.cgi?pass=マスタパス　でアクセスすると極秘通信も見れます。
#
#	修正履歴
#	2001/10/20 V0.20 最近の発言を色を変えて表示できるようにした。
#	2001/12/31 V0.30 共通設定部をconfig.cgiから取り込むようにした。
#	2002/01/13 V0.31 version4対応
#	2002/02/03 V0.40 CSSを別ファイルから読み込むようにした。
#	2002/04/17 V0.41 負荷表示をつけた。スクリプトを全体的に見直し。
#	2002/07/27 V0.50 極秘通信に対応。見た目の改善等。
#	2002/10/28 V0.60 スタイルシート辺りを改良
#
#---------------------------------------------------------------------
#	当スクリプトは以下を元に作成しました
#
#	怪獣撃退ポイント＋獲得賞金　ランキング表示
#	作成者 : Watson <watson@catnip.freemail.ne.jp>
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

# 色を変えて表示するターン
$kyoutyouturn = 10;

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '観光者通信一覧';

# 冒頭のメッセージ(HTML書式)
$headKill = <<"EOF";
<h1>$Htitle 観光者通信一覧表（管理用）</h1>
EOF

# 画面の「戻る」リンク先(URL)
$bye = $HthisFile;

# 管理者以外に投稿欄を表示するか？
$HpermitPost = 1;

#ここまで-------------------------------------------------------------

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
	close(PIN);
}
&cookieInput;
&cgiInput;
my($mode) = 0;
my $bye2 = '';
my $post = 'SS';
my $del = 'DS';

if($HskinName ne '' ){
	$baseSKIN = $HskinName;
} else {
	$baseSKIN = "${HcssDir}/$HcssDefault";
}
$HmainMode = 'lbbs';
if(!(&readIslandsFile(-4))){
	&htmlHeader;
	&htmlError;
} else {
	if($HdefaultPassword ne '') {
		my $island = $Hislands[$HidToNumber{$defaultID}];
		if($mode = checkPassword($island, $HdefaultPassword)) {
			if($mode == 2) {
				$HdefaultName = $HadminName;
				$defaultID = 0;
				$post = 'AD';
				$del = 'DA';
			} elsif(!$HpermitPost) {
				$mode = 0;
			}
		} else {
			&htmlHeader;
			tempWrongPassword(); # パスワード違い
			&htmlFooter;
			exit(0);
		}
	}
	$bye2 = ($mode < 2) ? '' : "[<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A>] ";

	&htmlHeader;
	out("<DIV align='center'>");
	out($headKill);
#	out("当スクリプトは、サーバに負荷がかかると思われるため箱庭本体からリンクを張っていません。<br>");
#	out("頻繁にアクセスしたり、リロードなどの行為はできるだけ控えるように！<br>");
	out("<B>当スクリプトは、サーバに大きな負荷がかかると思われるので、頻繁にアクセスしたり、リロードなどの行為はできるだけ控えて下さい！</B><br><br>");
	out("<B>※投稿すると、投稿した島の観光画面に切り替わります</B><br>") if($mode == 1);
	out("<TABLE BORDER><TR><TD>");
	foreach $i (0..$islandNumber) {
		&tempLbbsContents($i);
	}
	out("<TR><TD colspan=2 class='M'><P align='center'>${AfterName}の名前をクリックすると、観光することができます。</P></TD></TR>");
	out("</TABLE>");
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

	if($getLine =~ /id=([0-9]+)/) {
		# 最初の起動
		$defaultID = $1;
	}
	if($getLine =~ /pass=([^\&]*)/) {
		# 最初の起動
		$HdefaultPassword = $1;
	}
	if($line =~ /LBBSVIEW=([0-9]+)\&/) {
		$HlbbsView = $1;
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
${bye2}<A HREF="$bye">[戻る]</A><br><br>
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

#---------------------------------------------------------------------
#	関数名 : tempLbbsContents
#	機　能 : ローカル掲示板内容
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub tempLbbsContents {
	my($number) = $_[0];
	my($island) = $Hislands[$number];
	my($name) = islandName($island);
	my($id) = $island->{'id'};
	my($owner) = $island->{'owner'};
	my($lbbs) = $island->{'lbbs'};
	my $no = @$lbbs;
	my($comment) = $island->{'comment'};
	my($line);
	if($island->{'absent'} == 0) {
		$name = "${HtagName_}$name${H_tagName}";
	} else {
		$name = "${HtagName2_}$name($island->{'absent'})${H_tagName2}";
	}
	$name .= "${HtagDisaster_}★${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
		$name = "${HtagDisaster_}【管理人あずかり】$rest${H_tagDisaster}<BR>" . $name;
	}
	out(<<END);
<TR><TH $HbgTitleCell width=5%>${HtagTH_}${AfterName}名${H_tagTH}</TH>
<TD $HbgNameCell>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}" TARGET=_blank>
$name
</A>
</TD><TH $HbgTitleCell width=5%>${HtagTH_}島主${H_tagTH}</TH>
<TD $HbgInfoCell>$owner</TD></TR>
<TR><TH $HbgTitleCell>${HtagTH_}コメント${H_tagTH}</TH><TD $HbgCommentCell colspan=3>$comment</TD></TR>
END

	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	if($mode) {
		out(<<END);
<TR>
<TD colspan=3>
<FORM action="$HthisFile" method="POST">
name:<INPUT TYPE="text" SIZE=16 NAME="LBBSNAME" VALUE="$HdefaultName">
<INPUT TYPE="hidden" NAME="ISLANDID2" VALUE="$defaultID">
com:<INPUT TYPE="text" SIZE=40 NAME="LBBSMESSAGE">
pass:<INPUT TYPE="password" SIZE=8 MAXLENGTH=16 NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>公開
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>極秘</span>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButton$post$id">
END

		out(<<END);
No.
<SELECT NAME=NUMBER>
END
		# 発言番号
		my($j, $i);
		for($i = 0; $i < $HlbbsMax; $i++) {
			$j = $i + 1;
			out("<OPTION VALUE=$i>$j\n");
		}
		out("<OPTION VALUE=-1>全\n");
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除" NAME="LbbsButton$del$id">
</TD></FORM><FORM action="$HlbbsFile" method="POST"><TD>
END

		out(<<END);
View
<SELECT NAME=LBBSVIEW>
END
		for($i = $HlbbsViewMax; $i <= $HlbbsMax; $i+=10) {
			if($i != $HlbbsView) {
				out("<OPTION VALUE=$i>$i\n");
			} else {
				out("<OPTION VALUE=$i SELECTED>$i\n");
			}
		}
		out(<<END);
</SELECT><B>/$no</B>
<INPUT TYPE="submit" VALUE="閲覧" NAME="LbbsButtonView">
</TD></TR>
</FORM>
END
	}

	my($i,$j,$str1,$turn);
	for($i = 0; $i < $HlbbsView; $i++) {
		$line = $lbbs->[$i];
		last if($line eq '0<<0>>');
		if($line =~ /([0-9]*)\<(.*)\<(.*)\>(.*)\>(.*)$/) {
			my($m, $iName, $oda, $tan, $com) = ($1, $2, $3, $4, $5);
			$com =~ s/(http|ftp):\/\/([^\x81-\xFF\s\"\'\(\)\<\>\\\`\[\{\]\}\|]+)/<A href=\"$1:\/\/$2\" onclick=\"location.href=\'${HaxesFile}?$1:\/\/$2\'\; return false\;\" target=\"_blank\">$HlbbsAutolinkSymbol<\/A>/g if($HlbbsAutolinkSymbol ne '');
			$j = $i + 1;
			my($speaker);
			my($sName, $sID) = split(/,/, $iName);
			my($os, $date, $addr) = split(/,/, $oda);
			my($turn, $name) = split(/：/, $tan);
			if($turn >= $HislandTurn - $kyoutyouturn) {
				out("<TR><TD class='RankingCell' align=center><span class='number'>$j</span></TD>");
			} else {
				out("<TR><TD $HbgNameCell align=center><span class='number'>$j</span></TD>");
			}
			$tan = "<A title='[$date]'>ターン${turn}</A>：$name";
			my $sNo = $HidToNumber{$sID};
			if($sName ne '') {
				if(defined $sNo){
					$speaker = "<span class='lbbsST'><B><SMALL>(<A STYlE=\"text-decoration:none\" HREF=\"$HthisFile?Sight=$sID\" TARGET=_blank>$sName</A>)</SMALL></B></span>";
				} else {
					$speaker = "<span class='lbbsST'><B><SMALL>($sName)</SMALL></B></span>";
				}
			}
			out("<TD $HbgInfoCell colspan=3>");
			if($os == 0) {
				# 観光者
				if ($m == 0) {
					# 公開
					if($sID ne '0') {
						out("<span class='lbbsSS'>$tan > $com</span> $speaker</TD></TR>");
					} else {
						out("<span class='lbbsAD'>$tan > ${com}</span> $speaker</TD></TR>");
					}
				} else {
					# 極秘
					if ($mode < 2) {
						# 観光客
						out("<DIV align='center'><span class='lbbsST'>- 極秘 -</span></DIV></TD></TR>");
					} else {
						# オーナー
						out("<span class='lbbsST'>$tan >(秘) $com</span> $speaker</TD></TR>");
					}
				}
			} else {
				# 島主
				out("<span class='lbbsOW'>$tan > $com</span> $speaker</TD></TR>");
			}
		}
	}
	out(<<END);
</TD></TR>
END

	out(<<END);
<TR></TR>
<TR></TR>
END
}

