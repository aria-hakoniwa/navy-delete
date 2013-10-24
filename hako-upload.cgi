#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for ����JS
#----------------------------------------------------------------------
# ���åץ��ɥ⥸�塼��
#	��ǡ����򥵡��С��إ��åפ��뤿��Τ�ΤǤ���
#----------------------------------------------------------------------
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

#�����ޤ�-------------------------------------------------------------

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	close(PIN);
}
&cookieInput();
if(!(&formdecode())){
	&error("�������顼");
}
if(!checkSpecialPassword($HdefaultPassword)) {
	$HtempBack2 = "<small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>";
	&error("�ѥ���ɥ��顼");
} else {
	$HtempBack2 = "<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>";
}
if(!(&readIslandsFile())){
	&error("�ᥤ��ǡ����ɤ߹��ߥ��顼");
} else {
	&dataUpload();
}

#��λ
exit(0);

#���֥롼����---------------------------------------------------------
#----------------------------------------------------------------------
# �ǥ�����
#----------------------------------------------------------------------
sub formdecode {
	my($line, $boundary, @params, $param);

	if($HuseUpload && uc($ENV{'REQUEST_METHOD'}) eq 'POST') {
		binmode STDIN;
		read(STDIN, $line, $ENV{'CONTENT_LENGTH'});
	} else {
		return 0;
	}
	if ( $line =~ /^(-+\w+)/ ) {
		$boundary = $1;
		@params = split($boundary, $line);
	}

	foreach $param (@params) {
		if ( $param =~ /^--/ ) { last; }
		$param =~ s/^(\r\n|\r|\n)//;
		$param =~ s/(\r\n|\r|\n)$//;
		if ( $param =~ /^Content-Disposition: form-data; name="([^"]*?)"; filename="([^"]*?)"(\r\n|\r|\n)/ ) {
			$Hfilename = $2; # ����ϥ��åפ����ե�����̾
			if ($Hfilename =~ /\\/) {
				$Hfilename = (split(/\\/, $Hfilename))[-1];
			}
			$param =~ s/^Content-Disposition:(.+?)(\r\n|\r|\n)Content-Type:(.+?)(\r\n\r\n|\r\r|\n\n)//i;
			$param =~ s/(\r\n|\r)/\n/g;
			@Hcontents = split(/\n/, $param); # ���줬�ե��������ΤΥǡ���
		} elsif ( $param =~ /^Content-Disposition: form-data; name="([^"]*?)"(\r\n|\r|\n)/ ) { #"
			$name = $1;
			$param =~ s/^Content-Disposition:(.+?)(\r\n\r\n|\r\r|\n\n)//i;
			if($name eq 'Upload') {
				$HmainMode = 'upload';
				$HinputPassword = htmlEscape($param);
				$HdefaultPassword = $HinputPassword;
			}
		}
	}
	return ($HmainMode eq 'upload') ? 1 : 0;
}

#----------------------------------------------------------------------
# ���åץ���
#----------------------------------------------------------------------
sub dataUpload {

	my $kind = '';
	if(checkSpecialPassword($HdefaultPassword)) {
		if($Hfilename =~ /^([0-9]+)_save.${HsubData}/) {
			$HcurrentID = $1;
			$kind  = 'save';
			$mode = 1;
		} elsif($Hfilename =~ /^([0-9]+)_lose.${HsubData}/) {
			$HcurrentID = $1;
			$kind  = 'lose';
			$mode = 2;
		}
	}
	if($kind eq '') {
		&error("�ե���������꤬����ޤ���");
	}
	# ����ID�Ȥ�������(�㤦��糰��ID���ѹ�)
	$Hcontents[3] = $HcurrentID if($Hcontents[3] != $HcurrentID);

	my $dir = ($kind eq 'lose') ? $HfightdirName : $HsavedirName;
	my $flag = 0;
	if(open(LIN, "${dir}/${Hfilename}")) {
		# Ʊ̾�ե�������ɤ߹��� 0��̾,1�����ʡ�̾,7�ѥ���ɤ�����å�
		chomp(my @line = <LIN>);
		close(LIN);
		if(($line[0] ne $Hcontents[0]) || ($line[1] ne $Hcontents[1]) || ($line[7] ne $Hcontents[7])) {
			# ������ID�γ������
			my($dn, %dnset);
			opendir(DIN, "${dir}/");
			# �Хå����åץǡ���
			while($dn = readdir(DIN)) {
				if($dn =~ /^([0-9]+)_${kind}.${HsubData}/) {
					$dnset{$1} = 1;
				}
			}
			closedir(DIN);
			foreach (1..100) {
				if(!$dnset{$_}) {
					$HcurrentID = $_ ;
					last;
				}
			}
			# ����ID���ѹ�
			if($Hcontents[3] != $HcurrentID) {
				$Hcontents[3] = $HcurrentID
			} else {
				# ������Ƥ˼���
				&error("ID�γ�����Ƥ˼��Ԥ��ޤ�����");
			}
		} else {
			$flag = 1;
		}
	} elsif(!opendir(DIN, "${dir}/")) {
		# ��¸�ǥ��ꥯ�ȥ�Υ����å�
		mkdir("${dir}", $HdirMode);
	} else {
		closedir(DIN);
	}

	my $file = "${HcurrentID}_${kind}.${HsubData}";
	my $tmpfile = "tmp_${HcurrentID}_${kind}.${HsubData}";

	open(FILE, ">${dir}/${tmpfile}");
	binmode FILE;
	foreach (@Hcontents) {
		print FILE $_ . "\n";
	}
	close(FILE);

	# �����̾���ˤ���
	unlink("${dir}/${file}") if($flag);
	rename("${dir}/${tmpfile}", "${dir}/${file}");

	print "Location: ${HthisFile}?ViewLose=${HdefaultPassword}\n\n";
	exit(0); # ��λ
}

#---------------------------------------------------------------------
# ���顼����
#---------------------------------------------------------------------
sub error {
	print qq{Content-type: text/html; charset=EUC-JP\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};

	out(<<END);
<HTML><HEAD><TITLE>ERROR!</TITLE></HEAD>
$Body<DIV ID='BodySpecial'>
$HtempBack2
<HR>
$_[0]
<HR>
</DIV>
</BODY></HTML>
END
	exit(0);

}

1;