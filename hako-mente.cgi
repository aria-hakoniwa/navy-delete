#!/usr/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������

# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ���ƥʥ󥹥ġ���(ver1.01)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------

#������������������������������������������������������������������������
#							  Ȣ����� 2nd
#								  v1.5
#
#					  by ���� webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#������������������������������������������������������������������������

#������������������������������������������������������������������������
#							 Ȣ����� ����
#								  v1.3
#
#					  by ���� webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#������������������������������������������������������������������������
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

# ��������ѥե�������ɤ߹���
require './hako-init.cgi';
require './hako-io.cgi';

# hako-mente.cgi ����ƥ֥饦���ǳ����ȡ��ޥ����ѥ���ɤ��ü�ѥ���ɤ�
# ���Ϥ��׵ᤵ��ޤ������������Ϥ��줿�ѥ���ɤϰŹ沽���졢�ѥ���ɥե�����
# �˵�������ޤ���

# �ѥ���ɤ��ѹ�������ϡ�FTP ����³���ƥѥ���ɥե�����������Ƥ���������
# ���θ塢hako-mente.cgi ��֥饦���ǳ����ƥѥ���ɤ������Ԥ��ޤ���
# �������ǥ�����ǡ���������뤳�ȤϤ���ޤ��󡣥�������Ǥ��ѹ��Ǥ��ޤ���

# index���ʤ���зٹ𤹤롩(1:���롢0:���ʤ�)
$alertNoIndex = 0;
$indexName = 'index.html';
# ������������������������������������������������������������
# �Ƽ�������
# ������������������������������������������������������������
# use Time::Local���Ȥ��ʤ��Ķ��Ǥϡ�'use Time::Local'�ιԤ�ä��Ʋ�������
# �����ˤ��Υե�����ΰ��ֺǸ�ǥ����ȥ����Ȥ��Ƥ���Time::Local �θߴ��ؿ�
# sub timelocal��ȤäƲ�������

#use Time::Local;
# ������������������������������������������������������������
# ������ܤϰʾ�
# ������������������������������������������������������������
my $title   = 'Ȣ����� ���� ���ƥʥ󥹥ġ���';

# �礭��ʸ��
my $HtagBig_ = '<span class="big">';
my $H_tagBig = '</span>';
# ������������������������������������������������������������
# �ᥤ��
# ������������������������������������������������������������

# �Ƽ��ѿ�
my($mainMode);
my($mpass1, $mpass2, $spass1, $spass2);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	close(PIN);
}

cookieInput();
cgiInput();
cookieOutput();

if($HskinName ne '' ){
	$baseSKIN = $HskinName;
} else {
	$baseSKIN = "${HcssDir}/$HcssDefault";
}

print <<END;
Content-type: text/html; charset=EUC-JP

<HTML>
<HEAD>
<TITLE>$title</TITLE>
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body
$Hheader
<HR>
END

if($alertNoIndex) {
	my $flag = 0;
	if(!(-e $indexName)) {
		print "${HbaseDir}��${indexName}������ޤ���";
		$flag = 1;
	}
#	if(!(-e "$HdirName/$indexName")) {
#		print "<BR>\n" if($flag);
#		print "${HbaseDir}/${HdirName}��${indexName}������ޤ���";
#		$flag = 1;
#	}
	print "<HR>\n" if($flag);
}

if($mainMode eq 'delete') {
	deleteMode() if(passCheck());
} elsif($mainMode eq 'current') {
	currentMode() if(passCheck());
} elsif($mainMode eq 'backup') {
	backupMode() if(passCheck());
} elsif($mainMode eq 'time') {
	timeMode() if(passCheck());
} elsif($mainMode eq 'stime') {
	stimeMode() if(passCheck());
} elsif($mainMode eq 'new') {
	newMode() if(passCheck());
} elsif($mainMode eq 'setup' || $mainMode eq 'changepw') {
	setupMode($modeValue) if(!$modeValue || passCheck());
} elsif($mainMode eq 'allylog') {
	allyLogMain() if(passCheck());
} elsif($mainMode eq 'dellog') {
	dellogMode() if(passCheck());
} elsif($mainMode eq 'log2html') {
	log2htmlMain() if(passCheck());
} elsif($mainMode eq 'mente') {
	menteMode() if(passCheck());
} elsif($mainMode eq 'unmente') {
	unmenteMode() if(passCheck());
}
if(($mainMode eq 'admin' || $dellcheck) && (passCheck())) {
	adminMode();
} elsif(($mainMode ne 'allylog') && ($mainMode ne 'dellog') && ($mainMode ne 'log2html')) {
	mainMode();
}

print<<"END";
</FORM></BODY></HTML>
END
exit(0);

sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	} 
	closedir(DIN);
	rmdir($dn);
}

sub currentMode {
	myrmtree "${HdirName}";
	mkdir("${HdirName}", $HdirMode);
	opendir(DIN, "${HdirName}.bak$currentID/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
	} 
	closedir(DIN);
}

sub backupMode {
	myrmtree "${HdirName}.bak$backupNo";
	mkdir("${HdirName}.bak$backupNo", $HdirMode);
	opendir(DIN, "${HdirName}/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}/$fileName", "${HdirName}.bak$backupNo/$fileName");
	} 
	closedir(DIN);
}

sub deleteMode {
	if($deleteID eq '') {
		myrmtree "${HdirName}";
	} else {
		myrmtree "${HdirName}.bak$deleteID";
	}
	unlink "hakojimalockflock";
}

sub newMode {
	mkdir($HdirName, $HdirMode);
	mkdir($HlogdirName, $HdirMode);
	mkdir($HbbsdirName, $HdirMode);

	# ���ߤλ��֤����
	my($now) = time();
	$now -= $now % $HunitTime if($HunitTime);

	open(OUT, ">$HdirName/$HmainData"); # �ե�����򳫤�
	print OUT "0,1\n";  # ������� 0,������ե饰 1
	print OUT "$now\n"; # ���ϻ���
	print OUT "0\n";    # ��ο�
	print OUT "1\n";    # ���˳�����Ƥ�ID
	print OUT "\n";     # �������¤������ID
	# �ȡ��ʥ�����
	print OUT "0\n";          # ���ߤ���Ʈ�⡼��
	print OUT "$HyosenTurn\n";# �ڤ��ؤ�������
	print OUT "0\n";          # �������ܤ�
	print OUT "0\n";          # �����󹹿���

	print OUT "\n"; # ͽ��
	print OUT "\n"; # ͽ��
	print OUT "\n"; # ͽ��
	print OUT "\n"; # ͽ��
	print OUT "\n"; # ͽ��
	print OUT "\n"; # ͽ��

	# �ե�������Ĥ���
	close(OUT);

	open(AOUT, ">${HdirName}/${HallyData}"); # �ե�����򳫤�
	print AOUT "0\n";   # Ʊ���� 0
	close(AOUT);

	if($HoceanMode) {
		open(MOUT, ">${HdirName}/world.${HsubData}"); # �ե�����򳫤�
		for($y = 0; $y < $HoceanSizeY*$HislandSizeY; $y++) {
			for($x = 0; $x < $HoceanSizeX*$HislandSizeX; $x++) {
				printf MOUT ("%02x%08x", 0, 0);
			}
			print MOUT "\n";
		}
		close(MOUT);
	}

}

sub setupMode {
	if (!($mpass1 && $mpass2) || ($mpass1 ne $mpass2)) {
		print "${HtagBig_}�ޥ����ѥ���ɤ����Ϥ���Ƥ��ʤ����ְ�äƤ��ޤ�${H_tagBig}";
		return;
	}
	if (!($spass1 && $spass2) || ($spass1 ne $spass2)) {
		print "${HtagBig_}�ü�ѥ���ɤ����Ϥ���Ƥ��ʤ����ְ�äƤ��ޤ�${H_tagBig}";
		return;
	}

	if (-e $HpasswordFile) {
		if(!$modeValue) {
			# �������ƥ����ۡ���Υ����å�
			print "${HtagBig_}���Ǥ˥ѥ���ɤ����ꤵ��Ƥ��ޤ�${H_tagBig}";
			return;
		} else {
			unlink("$HpasswordFile");
		}
	}

	$HinputPassword = $mpass1;
	$mpass1 = crypt($mpass1, 'ma');
	$spass1 = crypt($spass1, 'sp');

	open(OUT, ">$HpasswordFile") || die $!;
	print OUT <<END;
$mpass1
$spass1
END
	close(OUT);
	$modeValue = (!$modeValue) ? '����' : '�ѹ�';
	print "${HtagBig_}�ѥ���ɤ�${modeValue}���ޤ���${H_tagBig}";
}

sub timeMode {
	$ctMon--;
	$ctYear -= 1900;
	$ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
	stimeMode();
}

sub stimeMode {
	my($t) = $ctSec;
	open(IN, "${HdirName}/$HmainData");
	my(@lines);
	@lines = <IN>;
	close(IN);

	$lines[1] = "$t\n";

	open(OUT, ">${HdirName}/$HmainData");
	print OUT @lines;
	close(OUT);
}

sub mainMode {
	print <<END;
<STYLE type="text/css">
<!--
A { text-decoration:none; }
A:HOVER { text-decoration:underline; }
H1, H3, H5 { display:inline; }
H5 { color: green; }
-->
</STYLE>
<FORM action="$HmenteFile" method="POST">
<H1>$title</H1>�� [<a href="$HthisFile">$HtitleTag</a>]
<HR>
END

	unless (-e $HpasswordFile) {
		# �ѥ���ɥե����뤬�ʤ�
		print <<END;
<H2>�ޥ����ѥ���ɤ��ü�ѥ���ɤ���Ƥ���������</H2>
<P>�����ϥߥ����ɤ�����ˡ����줾�죲�󤺤����Ϥ��Ƥ���������</P>
<B>�ޥ����ѥ���ɡ�</B><BR>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><BR>
<BR>
<B>�ü�ѥ���ɡ�</B><BR>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><BR>
<BR>
<INPUT type="submit" value="�ѥ���ɤ����ꤹ��" name="SETUP">
END
		return;
	}
	$HinputPassword = $HdefaultPassword if($HinputPassword eq '');
	print <<END;
<B>�ޥ����ѥ���ɡ�</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HinputPassword">
<INPUT type="submit" value="�����ͼ�������" name="ADMIN">
END

	opendir(DIN, "./");

	# ����ǡ���
	if(-d "${HdirName}") {
		if(-e "./mente_lock") {
			print qq#<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼�ɲ��" NAME="UNMENTE">\n#;
		} else {
			print qq#<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼��" NAME="MENTE">\n#;
		}
		dataPrint("");
	} else {
		print <<END;
	<HR>
	<INPUT TYPE="submit" VALUE="�������ǡ�������" NAME="NEW">
END
	}

	# �Хå����åץǡ���
	my($dn);
#	while($dn = readdir(DIN)) {
#		if($dn =~ /^${HdirName}.bak(.*)/) {
#			dataPrint($1);
#		}
#	} 
	my(@suf);
	while($dn = readdir(DIN)) {
		if($dn =~ /^${HdirName}.bak(.*)/) {
			push(@suf, $1);
		}
	}
	foreach (sort { $a <=> $b } @suf) {
		dataPrint($_);
	}
	closedir(DIN);
}

# �����ͼ�
sub adminMode {
	print <<END;
<STYLE type="text/css">
<!--
A { text-decoration:none; }
A:HOVER { text-decoration:underline; }
H1, H3, H5 { display:inline; }
H5 { color: green; }
#changpw, #setupvalue, #news, #lbbslist, #exbbs, #axeslog, #centercamp, #bbsally, #bbsdead, #bbsdel, #event,
#log2html, #allymake, #allysetup, #dewarsetup, #predelete, #counter, #datachange, #mapchange, #mapsave, #viewlose, #movefleet,
#delisland, #present, #punish, #bfmake, #bfin { display:none; }
-->
</STYLE>
<script type="text/javascript">
<!--
function display(id) {
  if(document.getElementById){
    var obj = document.getElementById(id);
    if (obj.style.display == 'block'){
      obj.style.display='none';
    } else {
      obj.style.display='block';
    }
  }
}
-->
</script>
<FORM action="$HmenteFile" method="POST">
[<A href="$HmenteFile">���</A>]
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ADMIN value=1>
��<H1>Ȣ����� ���� �����ͼ�</H1>
�� [<a href="$HthisFile">$HtitleTag</a>]
END
	print <<END;
<HR>
END
	if($Hbbs eq "${HbaseDir}/hako-yy-bbs.cgi") {
		print "[<A HREF=\"$Hbbs\" target=\"_blank\">�Ǽ���</A>(<A HREF=\"$Hbbs?id=0&cpass=${HinputPassword}\" target=\"_blank\">�����⡼��</A>)] ";
	} else {
		print "[<A HREF=\"$Hbbs\" target=\"_blank\">�Ǽ���</A>] ";
	}
	print <<END;
[<A href="$HthisFile?Amity=0" target="_blank">ͧ�������</A>] 
[<A href="$HthisFile?Fleet=1" target="_blank">������ͭ������</A>] 
[<A href="$HthisFile?Item=0" target="_blank">�����ƥ��������</A>] 
[<A href="$HthisFile?Rekidai=0" target="_blank">���嵭Ͽ</A>] 
[<A href="$HthisFile?Rank=0" target="_blank">��󥭥�</A>] 
END
	if((-e "${HefileDir}/setup.html") && $sfFlag) {
		print "[<A href=\"${efileDir}/setup.html\">�������</A>] ";
	} else {
		print "[<A href=\"$HthisFile?SetupV=0\">�������</A>] ";
	}
	print "[<A href=\"$HthisFile?FightLog=0\" class=\"M\" TARGET=_blank>����ε�Ͽ</A>] " if($Htournament);
	if(!$HhtmlLogMode || !(-e "${HhtmlDir}/hakolog.html") || $Hgzip) {
		print "[<A href=\"${HbaseDir}/history.cgi?Event=0\" target=\"_blank\">�Ƕ�ν����</A>] ";
	} else {
		print "[<A href=\"${htmlDir}/hakolog.html\" target=\"_blank\">�Ƕ�ν����</A>] ";
	}
	print <<END;
<HR>
<H3><span class='disaster'>���ʲ��κ�Ȥϡ������ֺݤ˹Ԥ������˴��Ǥ���</span></H3>
END
	if(-e "./mente_lock") {
		print qq#��<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼�ɲ��" NAME="UNMENTE">\n#;
	} else {
		print qq#��<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼��" NAME="MENTE">\n#;
	}
	my $exMark = '��';
	print "<blockquote><h5>$exMark</h5>�򥯥�å�����ȴ�ñ��������ɽ������ޤ���";
	print <<END;
</FORM>
<FORM name="CHANGEPW" action="${HmenteFile}" method=POST>
<a href="javascript: display('changpw');"><h5>$exMark</h5></a>��
<H3><a href="javascript: display('changpw');">�ޥ����ѥ���ɡ��ü�ѥ���ɤ��ѹ�</a></H3>
<DIV id='changpw'>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<P>���������ѥ���ɤϡ����ϥߥ����ɤ�����ˡ����줾�죲�󤺤����Ϥ��Ƥ���������</P>
<B>�������ޥ����ѥ���ɡ�</B><BR>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><BR>
<BR>
<B>�������ü�ѥ���ɡ�</B><BR>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><BR>
<BR>
������<INPUT type="submit" value="�ѥ���ɤ����ꤹ��" name="CHANGEPW">
</FORM>
</DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('setupvalue');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?SetupV=${HinputPassword}" target="_blank">�������(��������)ɽ��</A>(<A HREF="${HthisFile}?SetupV=0" target="_blank">���������񤭴�����</A>)</H3>
<DIV id='setupvalue'>
<UL>
<LI>�������Ѥȥȥåץڡ����Υ�󥯤Ȥΰ㤤�ϡ��ץ쥤�䡼�˸������ʤ����������Ǥ��뤳�Ȥ��餤�Ǥ���
<LI>������ѹ��������ʤɤϡ�html��񤭴����Ƥ����Ȥ褤�Ǥ��礦��
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('news');"><h5>$exMark</h5></a>��
<H3><A HREF="hako-news.cgi?pass=${HinputPassword}" target="_blank">�˥塼����񤭴�����</A></H3>
<DIV id='news'>
<UL>
<LI>�ȥåץڡ����Τ��Τ餻��񤭴����뵡ǽ�Ǥ���<br>
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('lbbslist');"><h5>$exMark</h5></a>��
<H3><A HREF="${HlbbsFile}" target="_blank">�Ѹ����̿�����ɽ</A></H3>
<DIV id='lbbslist'>
<UL>
<LI>lbbslist.cgi�����֤��Ƥ����硢�����üԤδѸ����̿������������Ǥ��ޤ���<br>
<LI>���Υ�����ץȤϡ������Ф���٤�������Ȼפ���١����ˤ˥������������ꡢ����ɤʤɤι԰٤ϤǤ������������褦�ˤ��ޤ��礦��
<LI>�����ͥ⡼�ɤ�����ȡ������̿��򸫤뤳�Ȥ��Ǥ��ޤ��������͸��¤�����ȸ��äƤ���ޤ������������衣<br>��COOKIE�˥ޥ������ѥ���ɶ��äƤ�ȡִ����ͥ⡼�ɡפˤʤ�ޤ���
</UL></DIV><BR><BR>
END

	print <<END if($HuseExlbbs);
<a href="javascript: display('exbbs');"><h5>$exMark</h5></a>��
<H3><A HREF="${HlbbsDir}/view.cgi" target="_blank">�����ʰ׷Ǽ��Ĥ��������</A>(<A HREF="${HlbbsDir}/view.cgi?admin=${HviewPass}" target="_blank">�����ͥ⡼��</A>)</H3>
<DIV id='exbbs'>
<UL>
<LI>�������(hako-init.cgi)�ǡֳ����ʰ׷Ǽ��Ĥ���Ѥ���פ褦�ˤ��Ƥ��ʤ���С����Ƥ����������ޤ���
<LI>view.cgi������ǥ����ʡ������å��򥪥�ˤ��Ƥ����硢�ֱ����פǤ���ƤǤ��ʤ��褦�ˤʤ�ޤ����ޤ�����index�����פΥܥ���򲡤��ʤ���С������Ϻǿ��Υǡ����ˤϤʤ�ޤ���
<LI>�����ͥ⡼�ɤǥ�����������ȡ��ƷǼ��Ĥδ����ͤε�ǽ���Ȥ���褦�ˤʤ�ޤ����ʴ����ͤȤ��ƤΥ��å����򿩤٤Ƥ��ޤ��ޤ��Τǡ��������ƤˤϽ�ʬ������Ĥ���������
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('axeslog');"><h5>$exMark</h5></a>��
<H3><A HREF="JavaScript:void(0)" onClick="document.AXESLOG.target='newWindow';document.AXESLOG.submit();return false;">�����������򸫤�</a></H3>
<DIV id='axeslog'>
<FORM name="AXESLOG" action="${HaxesFile}" method=POST>
<INPUT type=hidden name=password value="${HinputPassword}">
<INPUT type=hidden name=mode value="analyze">
<INPUT type=hidden name=category value="a">
</FORM>
<UL>
<LI>�ᥤ�󥹥���ץ�(hako-main.cgi)������ǡ֥�����������Ȥ�פ褦�ˤ��Ƥ��ʤ���С����뤳�Ȥ��Ǥ��ޤ���
<LI>����Ĥ�ư��ˤ��������ϥХ��ˤʤ�ޤ���Τǡ�Ȣ�����Τ�ư��ˤ�ƶ������뤳�Ȥ�и礷�Ʋ�������
</UL></DIV><BR><BR>
END

	my $viewCommand = $HrepeatTurn * $HcampCommandTurnNumber;
	print <<END;
<FORM name="MAINCAMP" action="${HthisFile}" method="POST" target="_blank">
<a href="javascript: display('centercamp');"><h5>$exMark</h5></a>��
<H3>
<A HREF="JavaScript:void(0)" onClick="document.MAINCAMP.target='newWindow';document.MAINCAMP.submit();return false;">���ﱿ��������</a></H3>
<INPUT type=hidden name=camp value="0">
<INPUT type=hidden name=cpass value="${HinputPassword}">
<INPUT type=hidden name=id value="0">
<DIV id='centercamp'>
</FORM>
<UL>
<LI>����Υ��ޥ��(����$viewCommand��ʬ)�ȴ���ξ���������Ǥ��ޤ���
<LI>���ε�ǽ�ϡ������Ф���٤�������Ȼפ���١����ˤ˥������������ꡢ����ɤʤɤι԰٤ϤǤ������������褦�ˤ��ޤ��礦��
</UL></DIV><BR><BR>
END

	my $allyList = '';
	my $deadallyList = '';
	if($HallyUse || $HarmisticeTurn) {
		if($HallyBbs) {
			readAllyFile();
			if($HallyNumber) {
				foreach (0..$#Hally) {
					my $s = '';
					$s = ' SELECTED' if(!$_);
					$allyList .= "<OPTION VALUE=\"$Hally[$_]->{'id'}\"$s>$Hally[$_]->{'name'}\n"
				}
				print <<END;
<FORM name="ALLYBBS" action="${HbaseDir}/$HallyBbsScript" method=POST>
<a href="javascript: display('bbsally');"><h5>$exMark</h5></a>��
<H3><select name=ally>${allyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.ALLYBBS.target='newWindow';document.ALLYBBS.submit();return false;">Ʊ���Ǽ��Ĥ�</a></H3>
<INPUT type=hidden name=id value="0">
<INPUT type=hidden name=cpass value="${HinputPassword}">
<DIV id='bbsally'>
</FORM>
<UL>
<LI>��Ʊ���Ǽ��ġפ�����Ǥ��ޤ���
<LI>��Ƥ���ȡ�̾�����ֳ��ﱿ�������פˤʤ�ޤ���
</UL></DIV>

<FORM name="DEADBBS" action="${HmenteFile}" method=POST>
<a href="javascript: display('bbsdead');"><h5>$exMark</h5></a>��
<H3><select name=ALLYID>${allyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.DEADBBS.submit();return false;">Ʊ���Ǽ��ĥ�����ǥ��ذܹ�</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ALLYLOG>
<DIV id='bbsdead'>
</FORM>
<UL>
<LI>Ʊ���κ���Ͼ�Ρֿر�(Ʊ��)�κ����������ѹ��פǲ�ǽ�Ǥ���<BR>
�ֿر�(Ʊ��)�κ����������ѹ��פξ��ϡ���ȯ���ε�Ͽ�פ˲򻶥���ɽ������ơ�Ʊ���Ǽ��ĤΥ��Ϥ��Τޤ���¸����ޤ���<BR>
������ϡ�Ʊ���Ϥ��Τޤޤǡ�Ʊ���Ǽ��ĤΥ�����ǥ��ذܹԤ����ޤ���
<LI>���ǥ���hako-yy-bbs.cgi�ξ����˥�󥯤���ޤ���<BR>
</UL></DIV><BR><BR>
END
			}
			if(-f "${HbbsdirName}/dead${HallyData}") {
				open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
				my @dead = <DIN>;
				close(DIN);
				foreach (@dead) {
					my($dally, $daName, $diName) = split(/\,/, $_);
					my($did, $dturn) = split(/-/, $dally);
					$daName =~ s/<[^<]*>//g;
					$deadallyList .= "<OPTION VALUE=\"$dally\">$daName($HallyTopName��$diName ������$dturn�˾���)\n"
				}
				print <<END if(@dead > 0);
<FORM name="DELBBS" action="${HmenteFile}" method=POST>
<a href="javascript: display('bbsdel');"><h5>$exMark</h5></a>��
<H3><select name=DEADALLY>${deadallyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.DELBBS.submit();return false;">���ǥ��κ��</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden value='���ǥ��κ��' name="DELLOG">
<DIV id='bbsdel'>
</FORM>
<UL>
<LI>Ʊ���Ǽ��Ĥξ��ǥ��������ޤ���
</UL></DIV><BR><BR>
END
			}
		}
		if($Hbbs == "${HbaseDir}/hako-yy-bbs.cgi" || $allyList ne '' || $deadallyList ne '') {
				print <<END;
<FORM name="HTMLLOG" action="${HmenteFile}" method=POST>
<a href="javascript: display('log2html');"><h5>$exMark</h5></a>��
<H3><a href="javascript: display('log2html');">�Ǽ��ĥ���HTML��</a></H3>
<DIV id='log2html'>
<BR>����<select name=ALLYID><OPTION VALUE="0">����Ǽ���
${allyList}${deadallyList}</select>
���ե�����̾<INPUT type=text name=HTMLNAME value="bbslog" size=8> 
�Ƶ���(1�ڡ���������)<INPUT type=text name=MAXLINE value="100" size=3> 
amity�����ν���<INPUT type=checkbox name=AMITY value="1" checked>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<BR><BR>����<INPUT type=submit value='�Ǽ��ĥ���HTML��' name="HTMLLOG">
<UL>
<LI>��Ʊ���Ǽ��ġפΥ��򡢲�����ޤ��HTML�����ޤ���
<LI>HTML�ե�����ϡ��ֺǶ�ν�����פ�HTML����������(hako-init.cgi)��Ʊ���ǥ��ꥯ�ȥ����������ޤ���
<UL>
<LI>�إե�����̾�٤ΤȤ�����bbslog�פˤ����bbslog0000.html����ɬ�פʤ����ե������ʬ�䤷�����֤Ǻ������ޤ���
<LI>�ؿƵ���(1�ڡ���������)�٤ϡ�$HallyBbsScript�����ꤷ�Ƥ���ֺ��絭�����פ�ۤ��뤳�ȤϤǤ��ޤ���
<LI>��amity�����ν��ϡ٤Υ����å���Ϥ����Ƚ��Ϥ��ޤ���
</UL></UL></FORM>
</DIV>
<BR><BR>
END
		}

		print <<END;
<a href="javascript: display('allymake');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?JoinA=${HinputPassword}">�ر�(Ʊ��)�κ����������ѹ�</A></H3>
<DIV id='allymake'>
<UL>
<LI>�ֿر���⡼�ɡפ�ͭ���ˤ��Ƥ�����ϡ���������ر�(Ʊ��)�򿷵��������Ƥ���������
<LI>�ر�(Ʊ��)��������򤷤��ѹ��ܥ���򲡤��ȡ��ر�(Ʊ��)�λ���(����)��Ǥ̿���뤳�Ȥ��Ǥ��ޤ���
</UL></DIV><BR><BR>
END
	}

	print <<END if($HuseAmity || $HallyUse || $HarmisticeTurn);
<a href="javascript: display('allysetup');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?ASetup=${HinputPassword}">ͧ����Ʊ��(�ر�)�ν�°�ѹ�</A></H3>
<DIV id='allysetup'>
<UL>
<LI>ͧ���������Ʊ����°���ѹ���Ԥ��ޤ���
</UL></DIV><BR><BR>
END

	print <<END if($HuseDeWar);
<a href="javascript: display('dewarsetup');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?WSetup=${HinputPassword}">�����۹���ƥʥ�</A></H3>
<DIV id='dewarsetup'>
<UL>
<LI>�����۹�Υ��ƥʥ󥹤�Ԥ��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('event');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Esetup=${HinputPassword}">���٥�Ȥ����ꤹ��</A></H3>
<DIV id='event'>
<UL>
<LI>���٥�Ȥ����ꤷ�ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('predelete');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Pdelete=${HinputPassword}">����${AfterName}������ͤ�������ˤ���</A></H3>
<DIV id='predelete'>
<UL>
<LI>��������ˤʤä�${AfterName}�ϡ����������(�������������ޥ�ɽ�������Ĺ���ҳ������ȼ԰�̱)����ʤ��ʤ�ޤ���
<LI>¾��${AfterName}����ι��������դ��ޤ���
<LI>���ޥ�ɤκǽ�ˡ���������פ����Ϥ����Ȥ����������������褦�ˤʤäƤ��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('counter');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?ICounter=${HinputPassword}">����${AfterName}�γ�ĥ�ǡ����Υ����󥿡������ꤹ��</A></H3>
<DIV id='counter'>
<UL>
<LI>�ޥåײ��̲��Ρ֥�������������ߡפΥǡ�����(�����󥿡�)���ɲá���������õ��Ԥ��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('datachange');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?ISetup=${HinputPassword}">����${AfterName}��${AfterName}�ǡ�����������</A></H3>
<DIV id='datachange'>
<UL>
<LI>�Ӥ餷���ﳲ�䡢�����С��ȥ�֥롢������ץȤΥХ��ʤɤǡ�${AfterName}�ǡ��������ܰդʾ��֤ˤʤäƤ��ޤä�${AfterName}��ߺѤ��ޤ���
<LI>���ˤ�����Ϸ��ǡ����פǤϤʤ����ᥤ��ǡ����˴ؤ�뽤����Ԥ��ޤ���
<LI>�ᥤ��ǡ�����ľ�ܽ���������ϰ������⤷��ޤ��󤬡��μ����ʤ���л��Ѥ��񤷤����⤷��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('mapchange');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Lchange=${HinputPassword}">����${AfterName}���Ϸ��ǡ������ѹ�����</A></H3>
<DIV id='mapchange'>
<UL>
<LI>�Ӥ餷���ﳲ�䡢�����С��ȥ�֥롢������ץȤΥХ��ʤɤǡ��Ϸ��ǡ��������ܰդʾ��֤ˤʤäƤ��ޤä�${AfterName}��ߺѤ��ޤ���
<LI>��ɸ���Ĥ��Ĥν����ʤΤǡ���ʬŪ�ʵߺ����֤����Ǥ��ޤ�������Ū���ѹ���ľ�ܥǡ�������Ѥ��������ᤤ�Ǥ��礦��
<LI>�ޤ����͸������쵬�Ϥʤɤο��ͥǡ����ؤ�ȿ�Ǥϥ����󹹿��������Ԥ��Ƥ���ˤʤ�Τǡ���դ��Ƥ���������
<LI>���Ϸ��פȡ��Ϸ����͡פˤĤ��Ƥ��μ����ʤ���л��Ѥ��񤷤����⤷��ޤ��󡣤��Ȥ��Сֳ��פ��ͤ򣱤ˤ���ȡ������פˤʤä��ꡢ�ԻԤο͸���ɽ����ο��ͤȥǡ�����ο��ͤΰ㤤(10000�ͤ�100�ȵ�Ͽ����Ƥ����ꤹ��Τ�)�䡢����乩���ȯŸ���ϤǤȤꤦ����ͤ���ޤäƤ��뤳�Ȥʤ�(hako-make.cgi��sub landCheck�Ǵʰץ����å��򤹤�褦�ˤ��Ƥ��ޤ�)��
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('mapsave');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?ISave=${HinputPassword}">����${AfterName}���Ϸ��ǡ�������¸����������</A></H3>
<DIV id='mapsave'>
<UL>
<LI>�ȡ��ʥ��ȥ⡼�ɤ����ﾡ������ή�ѤǤ���
<LI>�����Τ��Ϸ��ǡ����Ȼ�⡦��������¸���������뤳�Ȥ��Ǥ��ޤ���
<LI>�ȡ��ʥ��ȥ⡼�ɤǤ���Ʈ���֤�������ˡ������֥ǡ�������񤭤���ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('viewlose');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?ViewLose=${HinputPassword}">��¸�ǡ�������(���������)</A></H3>
<DIV id='viewlose'>
<UL>
<LI>���ԼԤ�${AfterName}�����פǤϥȡ��ʥ��ȥ⡼�ɤ��ԼԤȤʤä�${AfterName}�����׻�����¸���줿�ǡ����򸫤뤳�Ȥ��Ǥ��ޤ���
<LI>���ԼԤ�${AfterName}�פϡ��ȡ��ʥ��Ȱʳ��Ǥ���ǽ����κݤ˥ǡ�������¸����褦������Ǥ��ޤ�(init-game.cgi��\$HdeadToSaveAsLose)��
<LI>����¸�ǡ��������פǤϡֻ���${AfterName}���Ϸ��ǡ�������¸����������פ���¸���줿�ǡ����򸫤뤳�Ȥ��Ǥ��ޤ���
<LI>�ǡ������Ϸ������Ǥʤ���δ��ܥǡ������٤Ƥ���¸����Ƥ��ޤ���
<LI>�������ǡ������פ���ȡ���¸���Ƥ�����ˤĤ��Ƥϥǡ����ν񤭴��������Ǥ��Ƥ�����ˤĤ��Ƥ����������Ȥʤ�ޤ���
<LI>��¸���Ƥ������Ƚ��ϡ�ID����̾�������ʡ�̾���ѥ���ɤΣ��ĤΥǡ������٤Ƥ����פ��뤫�ɤ����Ǥ����ҤȤĤǤ�㤦��硤������ID�������Ƥ������������ޤ���
</UL>
</DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('movefleet');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Mfleet=${HinputPassword}">�������Ū�˰�ư������</A></H3>
<DIV id='movefleet'>
<UL>
<LI>�������ˤ��������̤���ذ�ư�����ޤ���
<LI>��ɸ����ϤǤ��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('delisland');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Rename=0" target="_blank">����${AfterName}�����������</A></H3>
<DIV id='delisland'>
<UL>
<LI>��${AfterName}��̾���ȥѥ���ɤ��ѹ��ײ��̤ǡ�������${AfterName}��̾�����̵�͡�${AfterName}�ޤ��ϡ����ס�${AfterName}�ˤ��Ƥ���������
<LI>���κݡ��ѥ������ˤϡ��ü�ѥ���ɡפ����Ϥ��ʤ���Фʤ�ޤ���
<LI>��̵�͡�${AfterName}�ˤ���ȡ�ȯ���ε�Ͽ�פˡ��ֳ�����<B>�ܤ�˿���</B>Φ�ϤϤ��٤�<span class='disaster'>���פ��ޤ�����</span>�פȤ��������Ĥ�ޤ���
<LI>�����ס�${AfterName}�ξ��ϥ���Ф��ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('present');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Present=">����${AfterName}�˥ץ쥼��Ȥ�£��</A></H3>
<DIV id='present'>
<UL>
<LI>��ȯ���ε�Ͽ�פ˥����Ĥ륤�٥�ȤȤ��Ʊ����Ԥ����Ȥ��Ǥ��ޤ���
<LI>ɽ�����줿�ե������ɬ�פ��ͤ��å����������Ϥ��ơ��ѥ���ɤˡ��ü�ѥ���ɡפ����졢�֥ץ쥼��Ȥ�£��ץܥ���򲡤��Хץ쥼��ȴ�λ�Ǥ���
<LI>���ˤ�HTML������Ȥ��ޤ������ְ�ä����κ�����Ǥ��ޤ���Τǡ����Ť����Ϥ��Ƥ������������餫����֥饦����ɽ���ƥ��Ȥ�ԤäƤ������ۤ��������Ǥ��礦����ȯ���ε�Ͽ�פ��Ѥʥ����Ĥ�ȡ�����ä��Ѥ��������Ǥ���
<LI>�ץ쥼��Ȥη�̤Ȥ��ƶ�俩������ͭ�̤������ͤ�Ķ���뤳�Ȥ�����ޤ�������Υ�����ʹԤ������ͤ��ڤ�ΤƤ��ޤ��������Υ���������ϻ��äƤ�������Ȥ��ޤ���
�㤨����ͭ�̤�20000�ˤʤäƤ����硢���Τޤޥ�����ʹԤ����9999���ڤ�ΤƤ��ޤ��������������Υ�����Ƿ����99��Ԥä����ˤϡ�����19800���������200�������Ĥ�ޤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('punish');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Punish=${HinputPassword}">����${AfterName}�����ۤ�ä���</A></H3>
<DIV id='punish'>
<UL>
<LI>���ۤϻ��ꤷ�������ҳ���ɬ��ȯ�������ޤ����㤨�С֣�${AfterName}�����������פȤ����ؼ���Ф��ȼ��Υ�����������������ޤ���
<LI>������Ф�ʮ�ФϺ�ɸ���꤬��ǽ�ǡ�ɬ�����κ�ɸ��ȯ�����ޤ����ɤ����褦��ʤ��ץ쥤�䡼���ӽ�����Ȥ��˸���Ū�˻Ȥ��ޤ���
<LI>���β�¤�ϡ��ֹӤ餷�Ȥ����ۤɤǤϤʤ���Ȣ���ʷ�ϵ��򰭲�������褦�ʹ԰٤򤹤�ץ쥤�䡼�פ䡢�ִ����ͤη�᤿������롼��˰�ȿ���Ƥ��Ʋ����θ����ߤ��ʤ��ץ쥤�䡼�פʤɡ�Ȣ��α��ľ幥�ޤ����ʤ���Ƚ�Ǥ��줿�ץ쥤�䡼�˼����ҳ������Ū��ȯ���������ΤǤ���
<LI>�����ͤ����ޤ����ʤ���Ƚ�Ǥ����ץ쥤�䡼�ȤϷǼ��Ĥʤɤ��ä��礦�٤��Ǥ��������ˤϡ����������ä��礤�Ǥ�����Կ�������ʤ����Ȥ⤢��ޤ�������������硢����${AfterName}�δ֤ǡ֤���${AfterName}���٤����פȤ�������������夬�ä��ꤷ�ޤ�������̣�Ϥ��ʤ갭���Ǥ���
<LI>�����ͤˤ�äƤϡ֤���${AfterName}�ϹӤ餷��ǧ�ꤷ�ޤ��Τǹ��⤷�Ƥ��������פ���${AfterName}�����ǧ��뤳�Ȥ⤢��褦�Ǥ������ʤ��ʤ������ޤǤ��б����񤷤���ΤǤ�������Ū��${AfterName}��������������֤Ϥޤ����ؤǤ������������줿${AfterName}�Υץ쥤�䡼�����Ȥ��Ȥޤǹ��Ĥ��Ƥ��뤳�Ȥ⤢��ޤ���
<LI>���������Ȥ��ˡ��ּ¤ˤ������֤˵�����СפȤ��ֱ��������������פȤ�������С����ޤ���᤺������${AfterName}�ϼ��β����ޤ�����ꤹ�����Ȣ���ʷ�ϵ��������ʤ�ޤ��Τ���դ�ɬ�פǤ���
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('bfmake');"><h5>$exMark</h5></a>��
<H3><A HREF="${HthisFile}?Bfield=${HinputPassword}">Battle Field���������</A></H3>
<DIV id='bfmake'>
<UL>
<LI>�͸����ˤʤäƤ����פ��ʤ�${AfterName}��������ޤ�������Сֱ齬${AfterName}�פǤ������и��ͤ���̱�Ԥ��ˤϤʤ�ޤ�(ʿ�·ϸ���)��
<LI>���餫����ֿ�����${AfterName}��õ���פˤ�ä�${AfterName}��������Ƥ����ʤ���Фʤ�ޤ���Τǡ�������Ͽ����ۤ������֤ξ��ϰ��Ū�ˤ�����ѹ��������䤷�Ƥ����ʤ���Фʤ�ʤ��Ǥ��礦�����ݤǤ��������ΤȤ�����ͤǤ���
<LI>�Ӥ餷��${AfterName}���ʣ��Ͽ��${AfterName}��Battle Field���ѹ����뤳�Ȥ�Ǥ��ޤ��͡�
<LI>�ޤ���Battle Field�ˤ��Ƥ���${AfterName}�򸵤��᤹���Ȥ�Ǥ��ޤ�����${AfterName}����Ͽ��������ξ��ϤǤ��ޤ���
<LI><B>Battle Field�λ���</B>
<UL>
<LI>���줬�ʤ��Ƥ⿩����­�ˤϤʤ�ʤ���
<LI>�Ӥ��ϤϤ��ʤ���Ψ��ʿ�Ϥˤʤꡢʿ�ϤϿ����ԻԤ��ܤ��Ƥ��ʤ��Ƥ�¼��ȯ�����롣
<LI>���ýи���Ψ���̾�Σ��ܤǡ��͸��ˤ�����餺��˥�٥룲��
<LI>���ä��ݤ��������󾩶�ϡ��ݤ�����Τ�Τˤʤ롣
</UL>
</UL></DIV><BR><BR>
END

	print <<END;
<FORM name="BFDEVELOP" action="${HthisFile}" method=POST>
<a href="javascript: display('bfin');"><h5>$exMark</h5></a>��
<H3><a href="JavaScript:void(0)" onClick="document.BFDEVELOP.target='newWindow';document.BFDEVELOP.submit();return false;">Battle Field�γ�ȯ���̤�����</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=dummy value="dummy">
<DIV id='bfin'>
</FORM>
<UL>
<LI>�ȥåץڡ�������ꥹ�Ȥ�Battle Field�����٤�褦�ˤʤ�ޤ���
<LI>Battle Field��������Ƥ��ʤ���С��������̤Υȥåץڡ�����ɽ�����������Ǥ���
</UL></DIV><BR><BR>
END

	print "</blockquote>";
}

# Ʊ���Ǽ��ĥ�����ǥ��ذܹ�
sub allyLogMain {
	# ��ǡ������ɤߤ���
	if(!readIslandsFile()) {
		print "�ǡ����ɤ߹��ߥ��顼ȯ����<HR>";
		return;
	}
	my $an = $HidToAllyNumber{$HallyID};
	if(defined $an) {
		my $n = $HidToNumber{$HallyID};
		my $name = $Hislands[$n]->{'name'} . $AfterName;
		$name = "${HallyTopName}�Ժ�" if !(defined $n);
		if($dellcheck) {
			if(make_pastlog($HallyID, $name)) {
				print "�ܹ���������<a href='${HbaseDir}/hako-yy-bbs.cgi'>�Ǽ��Ĥ�</a><HR>";
			} else {
				print "�Ǽ��ĥ����ߤĤ���ʤ����ޤ��ϡ��ܹԼ��ԡ�<HR>";
			}
		} else {
			my $allyName = $Hally[$an]->{'name'};
			print <<END;
<H2>$allyName��Ʊ���Ǽ��ĥ�����ǥ��ذܹԤ��ޤ�����</H2>
<H2><FORM name="DEADBBS" action="${HmenteFile}" method=POST>
<INPUT type=hidden name=DELLOK value="1">
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ALLYID value="${HallyID}">
<INPUT type=hidden name=ALLYLOG>
<a href="JavaScript:void(0)" onClick="document.DEADBBS.submit();return false;">�Ϥ�</a>��<a href="${HmenteFile}?ADMIN=${HinputPassword}">������</a></H2>
END
		}
		return;
	} else {
		print "Ʊ�����ߤĤ���ޤ���<HR>";
		$dellcheck = 1;
	}
	return;
}

# Ʊ���Ǽ��ĥ���HTML��
sub log2htmlMain {
	# ��ǡ������ɤߤ���
	if(!readIslandsFile()) {
		print "�ǡ����ɤ߹��ߥ��顼ȯ����<HR>";
		return;
	}
	my $an = $HidToAllyNumber{$HallyID};
	my $allyName = $Hally[$an]->{'name'};
	if(!(defined $an)) {
		if($HallyID eq '0') {
			$allyName = '����Ǽ���';
			$HallyID = '';
		} else {
			open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
			my @dead = <DIN>;
			close(DIN);
			foreach (@dead) {
				my($dally, $daName, $diName) = split(/\,/, $_);
				next if($dally ne $HallyID);
				my($did, $dturn) = split(/-/, $dally);
				$allyName = "$daName($HallyTopName��$diName ������$dturn�˾���)";
				last;
			}
		}
	}
	my $amitycheck = ('���ʤ�', '����')[$Hamity];
	print <<END;
<H3>��$allyName�פ�Ʊ���Ǽ��ĥ���HTML�����ޤ�����</H3>
�ե�����̾:${HhtmlName}0000.html��
<BR>�Ƶ����ο�(1�ڡ���������):$HmaxLine
<BR>amity�����ν���:$amitycheck
<FORM name="HTMLLOG" action="${HbaseDir}/$HallyBbsScript" method=POST>
<INPUT type=hidden name=ally value="$HallyID">
<INPUT type=hidden name=htmlname value="$HhtmlName"> 
<INPUT type=hidden name=maxline value="$HmaxLine"> 
<INPUT type=hidden name=amity value="$Hamity">
<INPUT type=hidden name=id value="0">
<INPUT type=hidden name=mode value="html">
<INPUT type=hidden name=cpass value="${HinputPassword}">
</FORM>
<H2><a href="JavaScript:void(0)" onClick="document.HTMLLOG.submit();return false;">�Ϥ�</a>��<a href="${HmenteFile}?ADMIN=${HinputPassword}">������</a></H2>
END
	return;
}

# ���ǥ����
sub dellogMode {
	if($dellcheck) {
		my $logfile = "${HbbsdirName}/${deadally}$Hlogfile_name";
		unlink($logfile) if (-f $logfile);
		# ������ե�����
		my $logfile2 = "${HbbsdirName}/${deadally}$Hlogfile2_name";
		unlink($logfile2) if (-f $logfile2);
		# �����󥿥ե�����
		if($Hcounter) {
			my $cntfile = "${HbbsdirName}/${deadally}$Hcntfile_name";
			unlink($cntfile) if (-f $cntfile);
		}
		# ������NO�ե�����
		if($Hpastkey) {
			my $nofile  = "${HbbsdirName}/${deadally}$Hnofile_name";
			my $count;
			if (-f $nofile) {
				# ���NO�򳫤�
				open(NO,"$nofile") || die $!;
				$count = <NO>;
				close(NO);
			}
			unlink($nofile);
			foreach (1..$count) {
				my $pastfile = sprintf("%s/%04d\.%s\.cgi", $HpastdirName,$_,$deadally);
				unlink($pastfile) if (-f $pastfile);
			}
		}
		open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
		my @dead = <DIN>;
		close(DIN);
		open(DOUT, ">${HbbsdirName}/dead${HallyData}") || die $!;
		foreach (@dead) {
			my($dally, $daName, $diName) = split(/\,/, $_);
			next if($dally eq $deadally);
			print DOUT $_;
		}
		close(DOUT);
	} else {
		open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
		my @dead = <DIN>;
		close(DIN);
		my $deadallyList;
		foreach (@dead) {
			my($dally, $daName, $diName) = split(/\,/, $_);
			my($did, $dturn) = split(/-/, $dally);
			$deadallyList = "$daName($HallyTopName��$diName ������$dturn�˾���)\n";
			last if($dally eq $deadally);
			$deadallyList = '';
		}
		if($deadallyList eq '') {
			$dellcheck = 1;
			return;
		}
		
		print <<END if(@dead > 0);
<H2>$deadallyList�ξ��ǥ��������ޤ�����</H2>
<H2><FORM name="DELBBS" action="${HmenteFile}" method=POST>
<INPUT type=hidden name=DELLOK value="1">
<INPUT type=hidden name=DEADALLY value="${deadally}">
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden value='���ǥ��κ��' name="DELLOG">
<a href="JavaScript:void(0)" onClick="document.DELBBS.submit();return false;">�Ϥ�</a>��<a href="${HmenteFile}?ADMIN=${HinputPassword}">������</a></H2>
END
	}
	return;
}

# ɽ���⡼��
sub dataPrint {
	my($suf) = @_;

	print "<HR>";
	if($suf eq "") {
		open(IN, "${HdirName}/$HmainData");
		print "<H1>����ǡ���</H1>";
	} else {
		open(IN, "${HdirName}.bak$suf/$HmainData");
		print "<H1>�Хå����å�$suf</H1>";
	}

	my($lastTurn, $playNow);
	my $tmp = <IN>;
	chomp($tmp);
	($lastTurn, $playNow) = split(/,/, $tmp); # �������, ��������ե饰
	if($playNow) {
		$playNow = '';
	} else {
		$playNow = '(�����ཪλ)';
	}
	my($lastTime);
	$lastTime = <IN>;

	my($timeString) = timeToString($lastTime);

	print <<END;
	��<H3>[������ $lastTurn]</H5>$playNow<BR>
	<B>�ǽ���������</B>��$timeString<BR>
	<B>�ǽ���������(�ÿ�ɽ��)</B>��1970ǯ1��1������$lastTime ��<BR>
	<INPUT TYPE="submit" VALUE="���Υǡ�������" NAME="DELETE$suf">
END

	if($suf eq "") {
		my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($lastTime + $Hjst);
		$mon++;
		$year += 1900;

		print <<END;
	<INPUT TYPE="submit" VALUE="���Υǡ�����Хå����å�" NAME="BACKUP">
	�Хå����å� No.<SELECT NAME="BUNO"><OPTION VALUE="0" SELECTED>0
END
	foreach (1..99) {
		print "<OPTION VALUE=\"$_\">$_\n";
	}

		print <<END;
	</SELECT>
	<H2>�ǽ��������֤��ѹ�</H2>
	<INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">ǯ
	<INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">��
	<INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">��
	<INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">��
	<INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">ʬ
	<INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">��
	<INPUT TYPE="submit" VALUE="�ѹ�" NAME="NTIME"><BR>
	1970ǯ1��1������<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">��
	<INPUT TYPE="submit" VALUE="�û�����ѹ�" NAME="STIME">
END
	} else {
		print <<END;
	<INPUT TYPE="submit" VALUE="���Υǡ��������" NAME="CURRENT$suf">
END
	}
}

# CGI���ɤߤ���
sub cgiInput {
	my($line);

	# ���Ϥ�������
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};

	if($line =~ /DELETE([0-9]*)/) {
		$mainMode = 'delete';
		$deleteID = $1;
	} elsif($line =~ /CURRENT([0-9]*)/) {
		$mainMode = 'current';
		$currentID = $1;
	} elsif($line =~ /BACKUP/) {
		$mainMode = 'backup';
		if($line =~ /BUNO=([0-9]*)/) {
			$backupNo = $1;
		} else {
			$backupNo = 0;
		}
	} elsif($line =~ /NEW/) {
		$mainMode = 'new';
	} elsif($line =~ /UNMENTE/) {
		$mainMode = 'unmente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /MENTE/) {
		$mainMode = 'mente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /ALLYLOG/) {
		$mainMode = 'allylog';
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		if($line =~ /DELLOK=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /DELLOG/) {
		$mainMode = 'dellog';
		$line =~ /DEADALLY=([0-9]*\-[0-9]*)\&/;
		$deadally = $1;
		if($line =~ /DELLOK=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /HTMLLOG/) {
		$mainMode = 'log2html';
		if($line =~ /ALLYID=([0-9\-]*)\&/) {
			$HallyID = $1;
		}
		if($line =~ /HTMLNAME=([^\&]*)\&/) {
			$HhtmlName = $1;
		}
		if($line =~ /MAXLINE=([0-9]*)\&/) {
			$HmaxLine = $1;
		}
		if($line =~ /AMITY=([0-9])/) {
			$Hamity = $1;
		}
	} elsif($line =~ /ADMIN/) {
		$mainMode = 'admin';
	} elsif($getLine =~ /ADMIN=([^\&]*)/) {
		$mainMode = 'admin';
		$HinputPassword = htmlEscape($1);
	} elsif($line =~ /SETUP/ || $line =~ /CHANGEPW/) {
		$mainMode = 'setup';
		$modeValue = ($line =~ /CHANGEPW/) ? 1 : 0;
		if($line =~ /MPASS1=([^\&]*)\&/) {
			$mpass1 = htmlEscape($1);
		}
		if($line =~ /MPASS2=([^\&]*)\&/) {
			$mpass2 = htmlEscape($1);
		}
		if($line =~ /SPASS1=([^\&]*)\&/) {
			$spass1 = htmlEscape($1);
		}
		if($line =~ /SPASS2=([^\&]*)\&/) {
			$spass2 = htmlEscape($1);
		}
	} elsif($line =~ /NTIME/) {
		$mainMode = 'time';
		if($line =~ /YEAR=([0-9]*)/) {
			$ctYear = $1; 
		}
		if($line =~ /MON=([0-9]*)/) {
			$ctMon = $1; 
		}
		if($line =~ /DATE=([0-9]*)/) {
			$ctDate = $1; 
		}
		if($line =~ /HOUR=([0-9]*)/) {
			$ctHour = $1; 
		}
		if($line =~ /MIN=([0-9]*)/) {
			$ctMin = $1; 
		}
		if($line =~ /NSEC=([0-9]*)/) {
			$ctSec = $1; 
		}
	} elsif($line =~ /STIME/) {
		$mainMode = 'stime';
		$ctSec = $1 if($line =~ /SSEC=([0-9]*)/);
	} elsif($line =~ /TOURNAMENTTIME/) {
		$mainMode = 'tournamenttime';
	}

	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = htmlEscape($1);
	}
	if(checkMasterPassword($HinputPassword)) {
		$HcurrentID = 0;
		$defaultID = 0;
	}
}

# �ե�����Υ��ԡ�
sub fileCopy {
	my($src, $dist) = @_;
	open(IN, $src);
	open(OUT, ">$dist");
	while(<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);
}

# �ѥ������å�
sub passCheck {
	if(checkMasterPassword($HinputPassword)) {
		return 1;
	} else {
		tempWrongPassword(); # �ѥ���ɰ㤤
		print<<"END";
</BODY></HTML>
END
		exit(0);
	}
}

# ���ƥʥ󥹥⡼��
sub menteMode {
    mkdir("./mente_lock", $HdirMode);
}

# ���ƥ⡼�ɲ��
sub unmenteMode {
	rmdir("./mente_lock");
}

# Time::Local �θߴ��ؿ�
sub timelocal {
	my($sec, $min, $hour, $day, $mon, $year) = @_;

	$year += 1900;
	$mon++;
	if ($mon <= 2) { $mon += 12; $year--; }

	my $days = $year * 365 + int($year / 4) - int($year / 100) + int($year / 400)
	+ $mon * 30 + int(($mon + 1) * 3 / 5) + $day - 33 - 719528; # 719528 = 1970/1/1

	return (($days * 24 + $hour) * 60 + $min) * 60 + $sec - $Hjst;
}

1;
