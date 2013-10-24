#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for 海戦JS
#---------------------------------------------------------------------
#	
#	究想の箱庭　最近の出来事と最近の天気の履歴を表示
#
#	作成日 : 2001/11/25 (ver0.10)
#	作成者 : ラスティア <nayupon@mail.goo.ne.jp>
#
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
$title = '最近の出来事';

# 画面の「戻る」リンク先(URL)
$bye = $HthisFile;

#メインルーチン-------------------------------------------------------
unless($ENV{HTTP_REFERER}  =~ /${HbaseDir}/) {
	print qq{Content-type: text/html; charset=EUC-JP\n\n};
	out(<<END);
<HTML>
<HEAD>
<TITLE>
$title
</TITLE>
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body
<H1>不正なアクセスです</H1>
</BODY></HTML>
END
	exit(0);
}
cookieInput();
cgiInput();
if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # マスタパスワードを読み込む
	chomp($HspecialPassword = <PIN>); # 特殊パスワードを読み込む
	close(PIN);
}

if($HhtmlLogMake && ($HcurrentID == 0)) {
	unless(-e "${HhtmlDir}/hakolog.html") {
		# 最近の出来事ＨＴＭＬ出力
		logPrintHtml();
		tempRefresh(3, 'ログ作成中です。そのまましばらくお待ち下さい') if($HhtmlLogMode);
	} else {
		tempRefresh(0, 'しばらくお待ち下さい') if($HhtmlLogMode);
	}
}

if(!readIslandsFile()){
	tempHeader();
	htmlError();
} else {
	# 無限ループ回避
	$HrepeatTurn = 1 if(!$HrepeatTurn);

	$HislandList = getIslandList($HcurrentID);
	tempHeader();
	out("<DIV ID='RecentlyLog'>\n");

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);
	if($HMode == 100 && $HuseWeather) {
		# 天気
		&logTenki();
	} else {
		# 最近の出来事
		if($HMode == 99) {
			if($HcurrentID == 0) {
				logFilePrintAll();
			} else {
				tempIslandHeader($HcurrentID, $HcurrentName);
				# パスワード
				if(checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					logPrintLocal(1);
				} else {
					# password違う
					logPrintLocal(0);
				}
			}
		} else {
			if($HcurrentID == 0) {
				foreach (1..$HrepeatTurn) {
					last if($HMode + $_ - 1 >= $HlogMax);
					logFilePrint($HMode + $_ - 1, $HcurrentID, 0);
				}
			} else {
				tempIslandHeader($HcurrentID, $HcurrentName);
				# パスワード
				if(checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					foreach (1..$HrepeatTurn) {
						last if($HMode + $_ - 1 >= $HlogMax);
						logFilePrint($HMode + $_ - 1, $HcurrentID, 1);
					}
				} else {
					# password間違い
					foreach (1..$HrepeatTurn) {
						last if($HMode + $_ - 1 >= $HlogMax);
						logFilePrint($HMode + $_ - 1, $HcurrentID, 0);
					}
				}
			}
		}
	}
	out("</DIV>\n");
}

tempFooter();
#終了
exit(0);

#サブルーチン---------------------------------------------------------
#---------------------------------------------------------------------
#	関数名 : htmlError
#	機　能 : HTMLのエラーメッセージの出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlError{
	out("<h2>エラーが発生しました</h2>\n");
}
#--------------------------------------------------------------------
#	POST or GETで入力されたデータ取得
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);

	# 入力を受け取って日本語コードをEUCに
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	jcode::convert(\$line, 'euc'); # jcode使用時
	$line =~ s/[\x00-\x1f\,]//g;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	if($line =~ /ID=([0-9]*)/){
		$HcurrentID = $1;
	} elsif($getLine =~ /ID=([0-9]*)/){
		$HcurrentID = $1;
	}
	if($line =~ /PASSWORD=([^\&]*)/) {
		$HinputPassword = $1;
	} elsif($getLine =~ /PASSWORD=([^\&]*)/) {
		$HinputPassword = $1;
	}
	if($line =~ /Event=([0-9]*)/){
		$HMode = $1;
	} elsif($getLine =~ /Event=([0-9]*)/){
		$HMode = $1;
	} else {
		$HMode = 0;
	}
	if($line =~ /Topmode=([0-9]*)/){
		$HtopMode = $1;
	} elsif($getLine =~ /Topmode=([0-9]*)/) {
		$HtopMode = $1;
	}
}

#---------------------------------------------------------------------
#	HTMLのヘッダとフッタ部分を出力
#---------------------------------------------------------------------
# ヘッダ
sub tempHeader {
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

	my($img);
	$img = "<BASE HREF=\"$baseIMG/\">" if($HMode == 100);
	out(<<END);
<HTML>
<HEAD>
<TITLE>
$title
</TITLE>
$img
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
END


	out(<<END) if(!$HtopMode);
$Hheader
<HR></DIV>
[<A HREF="$bye">戻る</A>] 
<br><br>
END
	logDekigoto();

	out(<<END);
<HR>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST" style="margin  : 2px 0px;">
END
	if($HuseWeather) {
		if($HMode == 100) {
			out("[<B><span class=number>最近の天気</span></B>]　");
		} else {
			out("[<A HREF=\"${HbaseDir}/history.cgi?Event=100\">最近の天気</A>]　");
		}
	}

	out("<B>[最近の出来事]</B>");
	if($HMode == 99 && $HcurrentID == 0) {
		out("[<B><span class=number>ALL</span></B>] ");
	} else {
		out("[<A HREF='${HbaseDir}/history.cgi?Event=99");
		out("&Topmode=1") if($HtopMode);
		out("'>ALL</A>] ");
	}
	my($i, $turn);
	for($i = 0;$i < $HtopLogTurn;$i+=$HrepeatTurn) {
		$turn = $HislandTurn - $i;
		last unless($turn > 0);
		$turn = "<a href='#${turn}' style='text-decoration:none;'>${turn}</a>" if($HMode == $i && $HcurrentID == 0);
		$turn = "ターン${turn}(現在)" if(!$i);
		if($HrepeatTurn > 1) {
			foreach(2..$HrepeatTurn) {
				my $n = $HislandTurn - $i - ($_ - 1);
				last unless($n > 0 && $HislandTurn - $n < $HtopLogTurn);
				$n = "<a href='#${n}' style='text-decoration:none;'>${n}</a>" if($HMode == $i && $HcurrentID == 0);
				$turn .= "・$n";
			}
		}
		if($HMode == $i && $HcurrentID == 0) {
			out("[<B><span class=number>${turn}</span></B>]\n");
			next;
		}
		out("[<A HREF='${HbaseDir}/history.cgi?Event=${i}");
		out("&Topmode=1") if($HtopMode);
		out("'>${turn}</A>]\n");
	}

	out(<<END);
　<B>[リンク]</B>　
<SELECT NAME="ID">$HislandList</SELECT>
<INPUT type=hidden name=PASSWORD value="$HinputPassword">
<INPUT type=hidden name=Topmode value="$HtopMode">
<INPUT type="submit" value="を見る">
</FORM>
END
}
# フッタ
sub tempFooter {
	if(!$HtopMode) {
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
		out("</DIV>");
	}
	out("</BODY></HTML>");
}

# html化リフレッシュ
sub tempRefresh {
	my($delay, $str) = @_;


	unless($Hgzip == 1) {
		print qq{Content-type: text/html; charset=EUC-JP\n\n};
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
		out(<<END);
<HTML><HEAD>
<TITLE>HTML化</TITLE>
<meta HTTP-EQUIV='refresh' CONTENT='$delay; URL="${htmlDir}/hakolog.html"'>
</HEAD>$Body<DIV ID='BodySpecial'>
<H2>$str</H2>
END
	} else {
		open(IN, "<${HhtmlDir}/hakolog.html") || die $!;
		@buffer = <IN>;
		close(IN);
		if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/) {
			print qq{Content-type: text/html;\n};
			print qq{Content-encoding: gzip\n\n};
			open(STDOUT,"| $HpathGzip/gzip -1 -c");
			print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
		} else {
			print qq{Content-type: text/html;\n\n};
		}
		print @buffer;
	}
	exit(0);
}

# 島データのプルダウンメニュー用
sub getIslandList {
	my($select) = @_;
	my($list, $name, $id, $s, $i);

	#島リストのメニュー
	$list = '';
	foreach $i (0..$islandNumber) {
		$name = islandName($Hislands[$i]);
		$id = $Hislands[$i]->{'id'};
		if($id eq $select) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		$list .= "<OPTION VALUE=\"$id\" $s>${name}\n";
	}
	return $list;
}
#---------------------------------------------------------------------
#	島の近況のリンク
#---------------------------------------------------------------------
# ヘッダ
sub tempIslandHeader {
my($id, $name) = @_;

	if(checkPassword($Hislands[$HidToNumber{$id}], $HinputPassword) && ($HcurrentID eq $defaultID)) {
		out(<<END);
<HR>
<FONT COLOR=\"#FF0000\"><B>[${name}の近況]</B></FONT>
END
	} else {
		out(<<END);
<HR>
<B>[${name}の近況]</B>　
END
	}

	if($HMode == 99) {
		out("[<B><span class=number>ALL</span></B>] ");
	} elsif($HinputPassword eq '') {
		out("[<A HREF='${HbaseDir}/history.cgi?ID=${id}&Event=99");
		out("&Topmode=1") if($HtopMode);
		out("'>ALL</A>] ");
	} else {
		out("[<A HREF='${HbaseDir}/history.cgi?ID=${id}&PASSWORD=${HinputPassword}&Event=99'>ALL</A>] ");
	}
	my($i, $turn);
	for($i = 0;$i < $HtopLogTurn;$i+=$HrepeatTurn) {
		$turn = $HislandTurn - $i;
		return unless($turn > 0);
		$turn = "<a href='#${turn}' style='text-decoration:none;'>${turn}</a>" if($HMode == $i);
		$turn = "ターン${turn}(現在)" if(!$i);
		if($HrepeatTurn > 1) {
			foreach(2..$HrepeatTurn) {
				my $n = $HislandTurn - $i - ($_ - 1);
				last unless($n > 0 && $HislandTurn - $n < $HtopLogTurn);
				$n = "<a href='#${n}' style='text-decoration:none;'>${n}</a>" if($HMode == $i);
				$turn .= "・$n";
			}
		}
		if($HMode == $i) {
			out("[<B><span class=number>${turn}</span></B>]\n");
			next;
		}
		if($HinputPassword eq '') {
			out("[<A HREF='${HbaseDir}/history.cgi?ID=${id}&Event=${i}");
			out("&Topmode=1") if($HtopMode);
			out("'>${turn}</A>]\n");
		} else {
			out("[<A HREF='${HbaseDir}/history.cgi?ID=${id}&PASSWORD=${HinputPassword}&Event=${i}'>${turn}</A>]\n");
		}
	}
}
#---------------------------------------------------------------------
#	ログファイルタイトル
#---------------------------------------------------------------------
sub logDekigoto {
	out(<<END);
<H1>最近の出来事</H1>
END
}
#---------------------------------------------------------------------
#	ログファイル全て表示
#---------------------------------------------------------------------
sub logFilePrintAll {
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		logFilePrint($i, 0, 0);
	}
}
#---------------------------------------------------------------------
# 個別ログ表示
#---------------------------------------------------------------------
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
}
#---------------------------------------------------------------------
#	ファイル番号指定でログ表示 # 海戦系
#---------------------------------------------------------------------
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	my $nowTurn = -1;

	open(LIN, "${HdirName}/$fileNumber$HlogData");
	my($line, $m, $turn, $id1, $id2, $id3, $message, @ids);
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-\s]*),(.*)$/;
		($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
		next if($m eq '');
		@ids = ($id1, $id2, split('-', $id3));
		if ($nowTurn != $turn) {
			out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
			out("<HR><span class=number><FONT SIZE=4><a name='$turn'>ターン $turn</a></FONT></span>\n<BLOCKQUOTE>\n");
			$nowTurn = $turn;
		}

		# 機密関係
		if($m == 1) {
			if(!$mode || ($id1 != $id)) {
				# 機密表示権利なし
				next;
			}
			$m = "<span class='lbbsST'>(機密)</span>";
		} else {
			$m = '';
		}

		# 表示的確か
		if($id != 0) {
			my $flag = 1;
			foreach (@ids) {
				if($id == $_) {
					$flag = 0;
					last;
				}
			}
			next if($flag);
		}

		# 表示
		out("${m}$message<BR>\n");
	}
	close(LIN);

	out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
}
#----------------------------------------------------------------------
# ＨＴＭＬ生成
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime(time + $Hjst);
	$mon++;
	my($sss) = "${mon}月${date}日 ${hour}時${min}分${sec}秒";

	$html1=<<_HEADER_;
<HTML><HEAD>
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
最近の出来事
</TITLE>
<link rel="stylesheet" type="text/css" href="${HcssDir}/$HcssDefault">
<BASE HREF="$htmlDir/">
</HEAD>
$Body
$Hheader
<DIV ID='BodySpecial'>
<DIV ID='RecentlyLog'>
<H1>最近の出来事</H1>
<FORM>
最新更新日：$sss・・
<INPUT TYPE="button" VALUE=" 再読込み" onClick="location.reload()">
</FORM>
<hr>
_HEADER_

$html3=<<_HEADER_;
</DIV><HR>
</DIV></BODY>
</HTML>
_HEADER_
	my($i);
	for($i = 0; $i < $HhtmlLogTurn; $i++) {
		$id =0;
		$mode = 0;
		my($set_turn) = 0;
		open(LIN, "${HdirName}/$i$HlogData");
		my($line, $m, $turn, $id1, $id2, $message);
		while($line = <LIN>) {
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-]*),(.*)$/;
			($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
			next if($m eq '');

			# 機密関係
			next if($m == 1);

			# 表示
			if($set_turn == 0){
				$html2 .= "<B>=====[<span class=number><FONT SIZE=4>ターン$turn </FONT></span>]================================================</B><BR>\n";
				$set_turn++;
			}
			$html2 .= "<span class='number'>★</span>:$message<BR>\n";
		}
		close(LIN);
	}
	open(HTML, ">${HhtmlDir}/hakolog.html");
#	print HTML jcode::sjis($html1);
#	print HTML jcode::sjis($html2);
#	print HTML jcode::sjis($html3);
	print HTML $html1;
	print HTML $html2;
	print HTML $html3;
	close (HTML);
	chmod(0666,"${HhtmlDir}/hakolog.html");
}
#---------------------------------------------------------------------
#	天気ファイル表示
#---------------------------------------------------------------------
sub logTenki {
	my($i, $j, $island, $name, $turn);
	out(<<END);
<HR>
<span class=number><FONT SIZE=4>[最近の天気]</FONT></span>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
END
	my $line =<<END;
<TR>
<TD $headNameCellcolor rowspan=2 NOWRAP>${AfterName}</TD>
<TD $headNameCellcolor rowspan=2 colspan=4 NOWRAP>気象データ</TD>
<TD $headNameCellcolor colspan=3 NOWRAP><span $tomorrowColor>予報</span></TD>
END
	for($i = 0; $i < $HtopLogTurn; $i++) {
		$turn = $HislandTurn - $i;
		last if($turn < 0);
		if($i == 0) {
			$line .= "<TD $headNameCellcolor rowspan=2 NOWRAP><nobr><span $todayColor>ターン${turn}<br><B>(現在)</B></nobr>";
		} else {
			$line .= "<TD $headNameCellcolor rowspan=2 NOWRAP>${turn}";
		}
		$line .= "</TD>";
	}
	$line .= "</TR><TR>";
	for($i = 0; $i < 3; $i++) {
		$turn = $HislandTurn + 3 - $i;
		$line .= "<TD $headNameCellcolor NOWRAP>";
		if($i == 2) {
			$line .= "<nobr><span $tomorrowColor>${turn}<br><B>(次回)</B></nobr>";
		} else {
			$line .= "<nobr><span $tomorrowColor>${turn}</nobr>";
		}
		$line .= "</TD>";
	}
	my(@all);
	for($i = 0; $i < $HislandNumber; $i++) {
		$island = $Hislands[$i];
		$name = islandName($island);
		if($island->{'field'}) {
			$name = "${HtagNumber_}${name}${H_tagNumber}";
		} elsif($island->{'absent'} == 0) {
			$name = "${HtagName_}${name}${H_tagName}";
		} else {
			$name = "${HtagName2_}${name}($island->{'absent'})${H_tagName2}";
		}
		$name .= "${HtagDisaster_}★${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
		if($island->{'predelete'}) {
			my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
			$name = "${HtagDisaster_}【管理人あずかり】$rest${H_tagDisaster}<BR>" . $name;
		}
		my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$Hislands[$i]->{'weather'}};
		foreach (0..6) {
			$all[$_] += $Hislands[$i]->{'weather'}[$_];
		}
		$line .= "<TR><TD $nameCellcolor rowspan=3><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\">${name}</A></TD>";
		$line .= "<TD $pointCellcolor>気温</TD><TD $pointCellcolor2>${kion}℃</TD><TD $pointCellcolor>風速</TD><TD $pointCellcolor2>${kaze}m/s</TD>";
		for($j = 0; $j < $HtopLogTurn + 3; $j++) {
			$turn = $HislandTurn + 3 - $j;
			last if($turn < 0);
			$weather[$j] = 0 if($weather[$j] == '');
			$line .= "<TD $pointCellcolor rowspan=3 NOWRAP>";
			$line .= "<img src ='$HweatherImage[$weather[$j]]'><br>" if($weather[$j]);
			if($j > 3) {
				$line .= "<span $yesterdayColor>";
			} elsif($j == 3) {
				$line .= "<span $todayColor>";
			} else {
				$line .= "<span $tomorrowColor>";
			}
			if($weather[$j]) {
				$line .= "$HweatherName[$weather[$j]]</span></TD>";
			} else {
				$line .= "−</span></TD>";
			}
		}
		$line .=<<END;
</TR><TR>
<TD $pointCellcolor>気圧</TD><TD $pointCellcolor2>${kiatu}hPa</TD>
<TD $pointCellcolor>地盤</TD><TD $pointCellcolor2>${jiban}</TD>
</TR><TR>
<TD $pointCellcolor>湿度</TD><TD $pointCellcolor2>${situdo}%</TD>
<TD $pointCellcolor>波力</TD><TD $pointCellcolor2>${nami}</TD>
</TR>
END
	}
	if($HislandNumber) {
		foreach (0..6) {
			$all[$_] = sprintf("%.1f", $all[$_]/$HislandNumber);
		}
		my $col = 8 + $HtopLogTurn;
		out("<TR><TD class='M' colspan='$col'><FONT COLOR='#FFFFFF'><B>気象データ全島平均　　気温：$all[0]℃　気圧：$all[1]hPa　湿度：$all[2]%　風速：$all[3]m/s　地盤：$all[4]　波力：$all[5]</B></FONT></TD></TR>\n");
	}
	out("$line</TABLE></TD></TR></TABLE><br>\n");
}
