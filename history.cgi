#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for ����JS
#---------------------------------------------------------------------
#	
#	���ۤ�Ȣ���Ƕ�ν�����ȺǶ��ŷ���������ɽ��
#
#	������ : 2001/11/25 (ver0.10)
#	������ : �饹�ƥ��� <nayupon@mail.goo.ne.jp>
#
#---------------------------------------------------------------------
BEGIN {
	# Perl 5.004 �ʾ夬ɬ��
	require 5.004;

########################################
	# ���顼ɽ��
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
#	�������
#---------------------------------------------------------------------
# ��������ѥե�������ɤ߹���
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';
#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = '�Ƕ�ν����';

# ���̤Ρ����ץ����(URL)
$bye = $HthisFile;

#�ᥤ��롼����-------------------------------------------------------
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
<H1>�����ʥ��������Ǥ�</H1>
</BODY></HTML>
END
	exit(0);
}
cookieInput();
cgiInput();
if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	chomp($HspecialPassword = <PIN>); # �ü�ѥ���ɤ��ɤ߹���
	close(PIN);
}

if($HhtmlLogMake && ($HcurrentID == 0)) {
	unless(-e "${HhtmlDir}/hakolog.html") {
		# �Ƕ�ν�����ȣԣͣ̽���
		logPrintHtml();
		tempRefresh(3, '��������Ǥ������Τޤޤ��Ф餯���Ԥ�������') if($HhtmlLogMode);
	} else {
		tempRefresh(0, '���Ф餯���Ԥ�������') if($HhtmlLogMode);
	}
}

if(!readIslandsFile()){
	tempHeader();
	htmlError();
} else {
	# ̵�¥롼�ײ���
	$HrepeatTurn = 1 if(!$HrepeatTurn);

	$HislandList = getIslandList($HcurrentID);
	tempHeader();
	out("<DIV ID='RecentlyLog'>\n");

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);
	if($HMode == 100 && $HuseWeather) {
		# ŷ��
		&logTenki();
	} else {
		# �Ƕ�ν����
		if($HMode == 99) {
			if($HcurrentID == 0) {
				logFilePrintAll();
			} else {
				tempIslandHeader($HcurrentID, $HcurrentName);
				# �ѥ����
				if(checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					logPrintLocal(1);
				} else {
					# password�㤦
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
				# �ѥ����
				if(checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					foreach (1..$HrepeatTurn) {
						last if($HMode + $_ - 1 >= $HlogMax);
						logFilePrint($HMode + $_ - 1, $HcurrentID, 1);
					}
				} else {
					# password�ְ㤤
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
#��λ
exit(0);

#���֥롼����---------------------------------------------------------
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlError
#	����ǽ : HTML�Υ��顼��å������ν���
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlError{
	out("<h2>���顼��ȯ�����ޤ���</h2>\n");
}
#--------------------------------------------------------------------
#	POST or GET�����Ϥ��줿�ǡ�������
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);

	# ���Ϥ������ä����ܸ쥳���ɤ�EUC��
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	jcode::convert(\$line, 'euc'); # jcode���ѻ�
	$line =~ s/[\x00-\x1f\,]//g;

	# GET�Τ�Ĥ�������
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
#	HTML�Υإå��ȥեå���ʬ�����
#---------------------------------------------------------------------
# �إå�
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
[<A HREF="$bye">���</A>] 
<br><br>
END
	logDekigoto();

	out(<<END);
<HR>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST" style="margin  : 2px 0px;">
END
	if($HuseWeather) {
		if($HMode == 100) {
			out("[<B><span class=number>�Ƕ��ŷ��</span></B>]��");
		} else {
			out("[<A HREF=\"${HbaseDir}/history.cgi?Event=100\">�Ƕ��ŷ��</A>]��");
		}
	}

	out("<B>[�Ƕ�ν����]</B>");
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
		$turn = "������${turn}(����)" if(!$i);
		if($HrepeatTurn > 1) {
			foreach(2..$HrepeatTurn) {
				my $n = $HislandTurn - $i - ($_ - 1);
				last unless($n > 0 && $HislandTurn - $n < $HtopLogTurn);
				$n = "<a href='#${n}' style='text-decoration:none;'>${n}</a>" if($HMode == $i && $HcurrentID == 0);
				$turn .= "��$n";
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
��<B>[���]</B>��
<SELECT NAME="ID">$HislandList</SELECT>
<INPUT type=hidden name=PASSWORD value="$HinputPassword">
<INPUT type=hidden name=Topmode value="$HtopMode">
<INPUT type="submit" value="�򸫤�">
</FORM>
END
}
# �եå�
sub tempFooter {
	if(!$HtopMode) {
		out(<<END);
<HR>
<DIV ID='LinkFoot'>
$Hfooter
<BR></DIV>
END
##### �ɲ� ����20020307
		if($Hperformance) {
			my($uti, $sti, $cuti, $csti) = times();
			$uti += $cuti;
			$sti += $csti;
			my($cpu) = $uti + $sti;

	#	   ���ե�����񤭽Ф�(�ƥ��ȷ�¬�ѡ����ʤϥ����Ȥˤ��Ƥ����Ƥ�������)
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

# html����ե�å���
sub tempRefresh {
	my($delay, $str) = @_;


	unless($Hgzip == 1) {
		print qq{Content-type: text/html; charset=EUC-JP\n\n};
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
		out(<<END);
<HTML><HEAD>
<TITLE>HTML��</TITLE>
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

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
	my($select) = @_;
	my($list, $name, $id, $s, $i);

	#��ꥹ�ȤΥ�˥塼
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
#	��ζᶷ�Υ��
#---------------------------------------------------------------------
# �إå�
sub tempIslandHeader {
my($id, $name) = @_;

	if(checkPassword($Hislands[$HidToNumber{$id}], $HinputPassword) && ($HcurrentID eq $defaultID)) {
		out(<<END);
<HR>
<FONT COLOR=\"#FF0000\"><B>[${name}�ζᶷ]</B></FONT>
END
	} else {
		out(<<END);
<HR>
<B>[${name}�ζᶷ]</B>��
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
		$turn = "������${turn}(����)" if(!$i);
		if($HrepeatTurn > 1) {
			foreach(2..$HrepeatTurn) {
				my $n = $HislandTurn - $i - ($_ - 1);
				last unless($n > 0 && $HislandTurn - $n < $HtopLogTurn);
				$n = "<a href='#${n}' style='text-decoration:none;'>${n}</a>" if($HMode == $i);
				$turn .= "��$n";
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
#	���ե����륿���ȥ�
#---------------------------------------------------------------------
sub logDekigoto {
	out(<<END);
<H1>�Ƕ�ν����</H1>
END
}
#---------------------------------------------------------------------
#	���ե���������ɽ��
#---------------------------------------------------------------------
sub logFilePrintAll {
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		logFilePrint($i, 0, 0);
	}
}
#---------------------------------------------------------------------
# ���̥�ɽ��
#---------------------------------------------------------------------
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
}
#---------------------------------------------------------------------
#	�ե������ֹ����ǥ�ɽ�� # �����
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
			out("<HR><span class=number><FONT SIZE=4><a name='$turn'>������ $turn</a></FONT></span>\n<BLOCKQUOTE>\n");
			$nowTurn = $turn;
		}

		# ��̩�ط�
		if($m == 1) {
			if(!$mode || ($id1 != $id)) {
				# ��̩ɽ�������ʤ�
				next;
			}
			$m = "<span class='lbbsST'>(��̩)</span>";
		} else {
			$m = '';
		}

		# ɽ��Ū�Τ�
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

		# ɽ��
		out("${m}$message<BR>\n");
	}
	close(LIN);

	out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
}
#----------------------------------------------------------------------
# �ȣԣͣ�����
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime(time + $Hjst);
	$mon++;
	my($sss) = "${mon}��${date}�� ${hour}��${min}ʬ${sec}��";

	$html1=<<_HEADER_;
<HTML><HEAD>
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
�Ƕ�ν����
</TITLE>
<link rel="stylesheet" type="text/css" href="${HcssDir}/$HcssDefault">
<BASE HREF="$htmlDir/">
</HEAD>
$Body
$Hheader
<DIV ID='BodySpecial'>
<DIV ID='RecentlyLog'>
<H1>�Ƕ�ν����</H1>
<FORM>
�ǿ���������$sss����
<INPUT TYPE="button" VALUE=" ���ɹ���" onClick="location.reload()">
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

			# ��̩�ط�
			next if($m == 1);

			# ɽ��
			if($set_turn == 0){
				$html2 .= "<B>=====[<span class=number><FONT SIZE=4>������$turn </FONT></span>]================================================</B><BR>\n";
				$set_turn++;
			}
			$html2 .= "<span class='number'>��</span>:$message<BR>\n";
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
#	ŷ���ե�����ɽ��
#---------------------------------------------------------------------
sub logTenki {
	my($i, $j, $island, $name, $turn);
	out(<<END);
<HR>
<span class=number><FONT SIZE=4>[�Ƕ��ŷ��]</FONT></span>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
END
	my $line =<<END;
<TR>
<TD $headNameCellcolor rowspan=2 NOWRAP>${AfterName}</TD>
<TD $headNameCellcolor rowspan=2 colspan=4 NOWRAP>���ݥǡ���</TD>
<TD $headNameCellcolor colspan=3 NOWRAP><span $tomorrowColor>ͽ��</span></TD>
END
	for($i = 0; $i < $HtopLogTurn; $i++) {
		$turn = $HislandTurn - $i;
		last if($turn < 0);
		if($i == 0) {
			$line .= "<TD $headNameCellcolor rowspan=2 NOWRAP><nobr><span $todayColor>������${turn}<br><B>(����)</B></nobr>";
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
			$line .= "<nobr><span $tomorrowColor>${turn}<br><B>(����)</B></nobr>";
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
		$name .= "${HtagDisaster_}��${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
		if($island->{'predelete'}) {
			my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
			$name = "${HtagDisaster_}�ڴ����ͤ��������$rest${H_tagDisaster}<BR>" . $name;
		}
		my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$Hislands[$i]->{'weather'}};
		foreach (0..6) {
			$all[$_] += $Hislands[$i]->{'weather'}[$_];
		}
		$line .= "<TR><TD $nameCellcolor rowspan=3><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\">${name}</A></TD>";
		$line .= "<TD $pointCellcolor>����</TD><TD $pointCellcolor2>${kion}��</TD><TD $pointCellcolor>��®</TD><TD $pointCellcolor2>${kaze}m/s</TD>";
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
				$line .= "��</span></TD>";
			}
		}
		$line .=<<END;
</TR><TR>
<TD $pointCellcolor>����</TD><TD $pointCellcolor2>${kiatu}hPa</TD>
<TD $pointCellcolor>����</TD><TD $pointCellcolor2>${jiban}</TD>
</TR><TR>
<TD $pointCellcolor>����</TD><TD $pointCellcolor2>${situdo}%</TD>
<TD $pointCellcolor>����</TD><TD $pointCellcolor2>${nami}</TD>
</TR>
END
	}
	if($HislandNumber) {
		foreach (0..6) {
			$all[$_] = sprintf("%.1f", $all[$_]/$HislandNumber);
		}
		my $col = 8 + $HtopLogTurn;
		out("<TR><TD class='M' colspan='$col'><FONT COLOR='#FFFFFF'><B>���ݥǡ�������ʿ�ѡ���������$all[0]�������$all[1]hPa�����١�$all[2]%����®��$all[3]m/s�����ס�$all[4]�����ϡ�$all[5]</B></FONT></TD></TR>\n");
	}
	out("$line</TABLE></TD></TR></TABLE><br>\n");
}
