#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for ����JS
# ��lbbslist.cgi?pass=[�ޥ����ѥ�]�ǥ�����������ȡ�������Ĥ��ޤ���
# ����Ƥ���������̾�ϴ�����̾�ǡ���̾�ϡִ����͡פˤʤ�ޤ���
# �������å����˥ޥ����ѥ�����äƤ���ϡ����̤˥����������������OK!
#---------------------------------------------------------------------
#	
#	���ۤ�Ȣ��������Ǽ��Ĥ����ɽ��
#
#	������ : 2001/10/06 (ver0.10)
#	������ : �饹�ƥ��� <nayupon@mail.goo.ne.jp>
#
#	�����Ԥ���̱��ȯ����ƨ���ʤ��褦�����ǳ�ǧ���뤿��Τ�ΤǤ���
#	lbbslist.cgi?pass=�ޥ����ѥ����ǥ�����������ȶ����̿��⸫��ޤ���
#
#	��������
#	2001/10/20 V0.20 �Ƕ��ȯ���򿧤��Ѥ���ɽ���Ǥ���褦�ˤ�����
#	2001/12/31 V0.30 ������������config.cgi���������褦�ˤ�����
#	2002/01/13 V0.31 version4�б�
#	2002/02/03 V0.40 CSS���̥ե����뤫���ɤ߹���褦�ˤ�����
#	2002/04/17 V0.41 ���ɽ����Ĥ�����������ץȤ�����Ū�˸�ľ����
#	2002/07/27 V0.50 �����̿����б��������ܤβ�������
#	2002/10/28 V0.60 �������륷�����դ�����
#
#---------------------------------------------------------------------
#	��������ץȤϰʲ��򸵤˺������ޤ���
#
#	���÷���ݥ���ȡܳ����޶⡡��󥭥�ɽ��
#	������ : Watson <watson@catnip.freemail.ne.jp>
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

# �����Ѥ���ɽ�����륿����
$kyoutyouturn = 10;

#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = '�Ѹ����̿�����';

# ��Ƭ�Υ�å�����(HTML��)
$headKill = <<"EOF";
<h1>$Htitle �Ѹ����̿�����ɽ�ʴ����ѡ�</h1>
EOF

# ���̤Ρ����ץ����(URL)
$bye = $HthisFile;

# �����԰ʳ���������ɽ�����뤫��
$HpermitPost = 1;

#�����ޤ�-------------------------------------------------------------

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
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
			tempWrongPassword(); # �ѥ���ɰ㤤
			&htmlFooter;
			exit(0);
		}
	}
	$bye2 = ($mode < 2) ? '' : "[<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A>] ";

	&htmlHeader;
	out("<DIV align='center'>");
	out($headKill);
#	out("��������ץȤϡ������Ф���٤�������Ȼפ��뤿��Ȣ�����Τ����󥯤�ĥ�äƤ��ޤ���<br>");
#	out("���ˤ˥������������ꡢ����ɤʤɤι԰٤ϤǤ������������褦�ˡ�<br>");
	out("<B>��������ץȤϡ������Ф��礭����٤�������Ȼפ���Τǡ����ˤ˥������������ꡢ����ɤʤɤι԰٤ϤǤ�����������Ʋ�������</B><br><br>");
	out("<B>����Ƥ���ȡ���Ƥ�����δѸ����̤��ڤ��ؤ��ޤ�</B><br>") if($mode == 1);
	out("<TABLE BORDER><TR><TD>");
	foreach $i (0..$islandNumber) {
		&tempLbbsContents($i);
	}
	out("<TR><TD colspan=2 class='M'><P align='center'>${AfterName}��̾���򥯥�å�����ȡ��Ѹ����뤳�Ȥ��Ǥ��ޤ���</P></TD></TR>");
	out("</TABLE>");
	out("</DIV>");
}
&htmlFooter;
#��λ
exit(0);

#���֥롼����---------------------------------------------------------
#--------------------------------------------------------------------
#	POST or GET�����Ϥ��줿�ǡ�������
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;

	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};

	if($getLine =~ /id=([0-9]+)/) {
		# �ǽ�ε�ư
		$defaultID = $1;
	}
	if($getLine =~ /pass=([^\&]*)/) {
		# �ǽ�ε�ư
		$HdefaultPassword = $1;
	}
	if($line =~ /LBBSVIEW=([0-9]+)\&/) {
		$HlbbsView = $1;
	}
}

#---------------------------------------------------------------------
#	�ؿ�̾ : htmlHeader
#	����ǽ : HTML�Υإå���ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
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
	$term = ($HislandTurn < $HarmisticeTurn) ? "(��$HarmisticeTurn <small>�������</small>)" : ($HislandTurn == $HarmisticeTurn) ? '(<small>������������Ʈ����</small>)' : '(<small>��Ʈ����</small>)' if($HarmisticeTurn);

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
		$nextturn .= '��' if($_ != 1);
		$nextturn .= $HislandTurn + $_;
		last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
	}
	out(<<END) if(defined $HleftTime);
<HR>
<H1 style="display:inline;"><SMALL><B>������</B> </SMALL>$HislandTurn<SMALL>${term}</SMALL>��</H1>
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

		document.all.REALTIME.innerHTML = '���󹹿�(<span class="number">������$nextturn</span>)�ޤǻĤ� ' + hour + '���� ' + min + 'ʬ ' + sec + '�� ($HnextTime)';
	} else {
		document.all.REALTIME.innerHTML = '�����󹹿�����ˤʤ�ޤ����� ($HnextTime)';
	}
}

if ($HplayNow) {
	showTimeLeft();
} else {
	document.all.REALTIME.innerHTML = '������Ͻ�λ���ޤ�����';
}
//-->
</SCRIPT>
END

	out(<<END);
<HR></DIV>
${bye2}<A HREF="$bye">[���]</A><br><br>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlFooter
#	����ǽ : HTML�Υեå���ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlFooter {
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
	out(<<END);
</DIV></BODY>
</HTML>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlError
#	����ǽ : HTML�Υ��顼��å������ν���
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlError{
	out("<H2>���顼��ȯ�����ޤ���</H2>\n");
}

#---------------------------------------------------------------------
#	�ؿ�̾ : tempLbbsContents
#	����ǽ : ������Ǽ�������
#	������ : �ʤ�
#	����� : �ʤ�
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
	$name .= "${HtagDisaster_}��${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
		$name = "${HtagDisaster_}�ڴ����ͤ��������$rest${H_tagDisaster}<BR>" . $name;
	}
	out(<<END);
<TR><TH $HbgTitleCell width=5%>${HtagTH_}${AfterName}̾${H_tagTH}</TH>
<TD $HbgNameCell>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}" TARGET=_blank>
$name
</A>
</TD><TH $HbgTitleCell width=5%>${HtagTH_}���${H_tagTH}</TH>
<TD $HbgInfoCell>$owner</TD></TR>
<TR><TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH><TD $HbgCommentCell colspan=3>$comment</TD></TR>
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
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>����
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>����</span>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButton$post$id">
END

		out(<<END);
No.
<SELECT NAME=NUMBER>
END
		# ȯ���ֹ�
		my($j, $i);
		for($i = 0; $i < $HlbbsMax; $i++) {
			$j = $i + 1;
			out("<OPTION VALUE=$i>$j\n");
		}
		out("<OPTION VALUE=-1>��\n");
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="���" NAME="LbbsButton$del$id">
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
<INPUT TYPE="submit" VALUE="����" NAME="LbbsButtonView">
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
			my($turn, $name) = split(/��/, $tan);
			if($turn >= $HislandTurn - $kyoutyouturn) {
				out("<TR><TD class='RankingCell' align=center><span class='number'>$j</span></TD>");
			} else {
				out("<TR><TD $HbgNameCell align=center><span class='number'>$j</span></TD>");
			}
			$tan = "<A title='[$date]'>������${turn}</A>��$name";
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
				# �Ѹ���
				if ($m == 0) {
					# ����
					if($sID ne '0') {
						out("<span class='lbbsSS'>$tan > $com</span> $speaker</TD></TR>");
					} else {
						out("<span class='lbbsAD'>$tan > ${com}</span> $speaker</TD></TR>");
					}
				} else {
					# ����
					if ($mode < 2) {
						# �Ѹ���
						out("<DIV align='center'><span class='lbbsST'>- ���� -</span></DIV></TD></TR>");
					} else {
						# �����ʡ�
						out("<span class='lbbsST'>$tan >(��) $com</span> $speaker</TD></TR>");
					}
				}
			} else {
				# ���
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

