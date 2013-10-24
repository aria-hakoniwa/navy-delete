#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for ����JS
#---------------------------------------------------------------------
# �˥塼���⥸�塼��
#	�ȥåץڡ����ˤ��Τ餻��ɽ�����뤿��Τ�ΤǤ���
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
$title = 'Ȣ��˥塼��';

# ��Ƭ�Υ�å�����(HTML��)
$headKill = <<"EOF";
<h1>$Htitle �˥塼���ʴ����ѡ�</h1>
EOF

#�����ޤ�-------------------------------------------------------------

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	close(PIN);
}
&cookieInput;
&cgiInput;

$HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : "${HtagBig_}<small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}";

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
		tempWrongPassword(); # �ѥ���ɰ㤤
		&htmlFooter;
		exit(0);
	}

	if($HmainMode eq 'news') {
		&newsMain;
	}
	&htmlHeader;
	out("<DIV align='center'>");
	out($headKill);
	# �إå��Υ����Ȥ�񤭴�������(hako-init.cgi��Ϣư)
	if($HlayoutTop) {
		&tempNews(0);
	} else {
		&tempNews(1);
	}
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

	if($getLine =~ /pass=([^\&]*)/) {
		# �ǽ�ε�ư
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
$HtempBack2
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
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="0"$check[0]>�إå������ľ����
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="1"$check[1]>������ɽ��ľ����
<INPUT TYPE="radio" NAME="LAYOUT" VALUE="2"$check[2]>�եå������ľ��
END
	my $str = (!$type) ? 'NEWS : �쥤�����ȵ�ǽ����' : $po;
	out(<<END);
<TABLE>
<TR></TR>
<FORM name="f$type" action="${HbaseDir}/hako-news.cgi" method="POST">
<TR><TD colspan=4><big><B>�������ѹ�($str)</B></big>
��<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="NewsComment">
��<INPUT TYPE="hidden" VALUE="$type" NAME="TYPE">
��<INPUT TYPE="submit" VALUE="�ѹ�">
</TD></TR>
<TR><TD colspan=4>
<P ALIGN="center">
<TABLE BORDER=2><TR><TD style="border-style:inset;">
<textarea name="NEWS$type" cols=100 rows=20 WRAP="soft">$newsline</textarea><BR>
</TD></TR></TABLE>
��������Preview��������
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
		tempWrongPassword(); # �ѥ���ɰ㤤
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