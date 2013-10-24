#!/usr/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���

# ���� JS.(based on ver1.3) patchworked by neo_otacky
# The Return of Neptune: http://no-one.s53.xrea.com/
# ��¤������ɽ���ˤ��Ƥ⤫�ޤ��ޤ��󤬡��Ǥ�����ѹ��Ϥ��ʤ��Ǥ���������
my $versionInfo = "version7.15"; # JS�ǥ��ꥸ�ʥ�ΥС������
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.02)
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

# ��������ѥե�������ɤ߹���(require�ν�����Ѥ��ƤϤ����ޤ���)
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#----------------------------------------------------------------------
# �ʲ������ߤˤ�ä����ꤹ����ʬ
#----------------------------------------------------------------------
# �۾ｪλ������
# (��å��岿�äǡ�����������뤫)
my($unlockTime) = 120;

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------
# COOKIE
# $defaultID;     # ���̾��
# $defaultTarget; # �������åȤ�̾��

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------
# ������������
my $host = $ENV{'REMOTE_HOST'};
my $addr = $ENV{'REMOTE_ADDR'};
if ($gethostbyaddr && (($host eq '') || ($host eq $addr))) {
	$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
}
if($host eq '') {
	$host = $addr;
}
my $flag = 0;
foreach (@Hdeny) {
	if (!$_) { next; }
	s/\*/\.\*/g;
	if ($host =~ /$_/i || $addr =~ /$_/i) { $flag=1; last; }
}
if ($flag) {
	if($HdenyLocation ne '') {
		print "Location: $HdenyLocation\n\n";
		exit;
	} else {
		tempHeader();
		tempWrong("������������Ĥ���Ƥ��ޤ���");
		tempFooter();
		exit(0);
	}
}

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";

my $agent=$ENV{'HTTP_USER_AGENT'};
if($agent =~ /(DoCoMo|J-PHONE|UP\.Browser|DDIPOCKET|ASTEL|PDXGW)/i) {
   # ����ü��
   $Hmobile = 1;
}

# ��å��򤫤���
if(!hakolock()) {
	# ��å�����
	# �إå�����
	tempHeader();

	# ��å����ԥ�å�����
	tempLockFail();

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}

# ����ν����
srand(time() ^ ($$ + ($$ << 15)));

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	chomp($HspecialPassword = <PIN>); # �ü�ѥ���ɤ��ɤ߹���
	close(PIN);
} else {
	unlock();
	tempHeader();
	tempNoHpasswordFile();
	tempFooter();
	exit(0);
}

# COOKIE�ɤߤ���
cookieInput();
$HchipSize = 16 if(!$HchipSize);

# CGI�ɤߤ���
cgiInput();

# ���ƥ⡼��
if(-e "./mente_lock") {
	if(!checkSpecialPassword($HdefaultPassword) && !checkSpecialPassword($HcampPassword)) {
		unlock();
		mente_mode()
	}
}

# ��ǡ������ɤߤ���
if(!readIslandsFile($HcurrentID)) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

if($Hmobile) {
	require('hako-mobile.cgi');
	exit(0);
}

# ���Х��Х�⡼�� ���������Ƚ��
if($HsurvivalTurn && ($HislandTurn >= $HsurvivalTurn)){
	foreach (
			$HcomReclaim,$HcomDestroy,$HcomPlant,$HcomFarm,$HcomFactory,$HcomMountain,
			$HcomMonument,$HcomDbase,$HcomBase,$HcomSbase,$HcomBouha,$HcomSeaMine,
			$HcomNavyWreckRepair,$HcomNavyWreckSell,@HcomNavy #,$HcomHaribote # ����������Ѥ˥ϥ�ܥ�(^^;
		) {
		$HcomTurn[$_] = 0;
	}
}

# COOKIE�ˤ��ID�����å�
if($HmainMode eq 'owner') {
	unless($ENV{'HTTP_COOKIE'}) {
		cookieOutput(); # COOKIE��������줿���ɤ����񤭹��ߥ����å�
		next if($ENV{'HTTP_COOKIE'}); # �񤭹���OK
		# ���å�����ͭ���ˤ��Ƥ��ʤ�
		axeslog(1, 'cookie invalid') if($HtopAxes && $HtopAxes != 3);
		unlock();
		tempHeader();
		tempWrong("cookie��ͭ���ˤ��Ƥ��ޤ�����<BR>�⤦���٤��ľ���ƤߤƲ�������");
		tempFooter();
		exit(0);
	}
	my($pcheck) = checkPassword($Hislands[$HidToNumber{$HcurrentID}],$HinputPassword);
	if(!$pcheck) {
		unlock();
		tempHeader();
		tempWrongPassword(); # �ѥ���ɰ㤤
		tempFooter();
		exit(0);
	}
	if($checkID || $checkImg) {
		# id����������
		my $free = 0;
		foreach (@freepass){
			$free += 1 if(($_ == $defaultID) || ($_ == $HcurrentID));
		}
		my($icheck) = !($checkID && ($HcurrentID != $defaultID) && $defaultID);
		my($lcheck) = !($checkImg && ($HimgLine eq '' || $HimgLine eq $HimageDir));
		# �ѥ����
		if(($pcheck != 2) && ($free != 2) && ((!$icheck && !$Hcodevelope) || !$lcheck)) {
			# ���Ĥ����鿴���Ѥ˲���������ʤɤ� ($free != 2) ����ʬ�� !$free ���ѹ����Ʋ�������
			unlock();
			tempHeader();
			if(!$icheck) {
				axeslog(1, 'ID error!') if($HtopAxes && $HtopAxes != 3);
				tempWrong("��ʬ����ʳ��ˤ�����ޤ���"); # ID�㤤
			} else {
				axeslog(1, 'image invalid') if($HtopAxes && $HtopAxes != 3);
				tempWrong("�ֲ����Υ���������פ򤷤Ʋ�������"); # ���������ꤷ�Ƥ��ʤ�
			}
			tempFooter();
			exit(0);
		}
	}
	# ������������
	if($HtopAxes && ($HcurrentID != $defaultID)) {
		axeslog(1, 'ID differ!');
	} elsif(($HtopAxes == 2) || ($HtopAxes > 3)) {
		axeslog(1);
	}

# �ƥ�ץ졼�Ȥ�����
	tempInitialize(1);
} elsif(!checkMasterPassword($HinputPassword) && (($HmainMode eq '') || ($HmainMode eq 'top'))) {
	tempInitialize(0);
} else {
	tempInitialize(1);
}

# COOKIE����
cookieOutput() if($HmainMode ne 'setupv');

# �إå�����
if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
	$HmainMode eq 'commandJava' ||                       # ���ޥ�����ϥ⡼��
	$HmainMode eq 'command2' ||                          # ���ޥ�����ϥ⡼�ɡ�ver1.1����ɲá���ư���ѡ�
	$HmainMode eq 'comment' && $HjavaMode eq 'java' ||   # ���������ϥ⡼��
	$HmainMode eq 'fleetname' && $HjavaMode eq 'java' || # ����̾�ѹ��⡼��
	$HmainMode eq 'priority' && $HjavaMode eq 'java' ||  # ��Ũ���ѹ��⡼��
	$HmainMode eq 'earth' && $HjavaMode eq 'java' ||     # ����ɽ������⡼��
	$HmainMode eq 'comflag' && $HjavaMode eq 'java' ||   # ���ޥ�ɼ¹�����⡼��
	$HmainMode eq 'preab' && $HjavaMode eq 'java' ||     # �رĶ�Ʊ��ȯ�⡼��
	$HmainMode eq 'lbbs' && $HjavaMode eq 'java') {      # ���������ϥ⡼��

	$Body = $BodyJs;
	require('./hako-map.cgi');
	# �إå�����
	tempHeaderJava();
	if($HmainMode eq 'commandJava') {
		# ��ȯ�⡼��
		commandJavaMain();
	} elsif($HmainMode eq 'command2') {
		# ��ȯ�⡼�ɣ��ʼ�ư�ϥ��ޥ���ѡ�ver1.1����ɲá���ư���ѡˡ�
		commandMain();
	} elsif($HmainMode eq 'comment') {
		# ���������ϥ⡼��
		commentMain();
	} elsif($HmainMode eq 'fleetname') {
		# ����̾�ѹ��⡼��
		fleetnameMain();
	} elsif($HmainMode eq 'priority') {
		# ��Ũ���ѹ��⡼��
		priorityMain();
	} elsif($HmainMode eq 'earth') {
		# ����ɽ������⡼��
		earthMain();
	} elsif($HmainMode eq 'comflag') {
		# ���ޥ�ɼ¹�����⡼��
		comflagMain();
	} elsif($HmainMode eq 'preab') {
		# �رĶ�Ʊ��ȯ�⡼��
		preabMain();
	} elsif($HmainMode eq 'lbbs') {
		# ������Ǽ��ĥ⡼��
		require('./hako-lbbs.cgi');
		localBbsMain();
	}else{
		ownerMain();
	}
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
}elsif($HmainMode eq 'landmap'){
	require('./hako-map.cgi');
	# �إå�����
	tempHeaderJava();
	# �Ѹ��⡼��
	printIslandJava();
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
} elsif($HmainMode ne 'lbbs' && $HmainMode ne 'new' && $HmainMode ne 'download'){
	# �إå�����
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ������ʹ�
	require('./hako-turn.cgi');
	require('./hako-top.cgi');
	turnMain();

} elsif($HmainMode eq 'new') {
	# ��ο�������
	require('./hako-make.cgi');
	require('./hako-map.cgi');
	newIslandMain(0);

} elsif($HmainMode eq 'newally') {
	# Ʊ���ο�������
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	makeAllyMain();

} elsif($HmainMode eq 'delally') {
	# Ʊ���κ��
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	deleteAllyMain();

} elsif($HmainMode eq 'inoutally') {
	# Ʊ���β�����æ��
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	joinAllyMain();

} elsif($HmainMode eq 'allypact') {
	# ���祳���ȥ⡼��
	require('./hako-make.cgi');
	allyPactMain();

} elsif($HmainMode eq 'print') {
	# �Ѹ��⡼��
	require('./hako-map.cgi');
	printIslandMain();

} elsif($HmainMode eq 'oceanmap') {
	# ����ޥåץ⡼��
	require('hako-map.cgi');
	printIslandMapMain();

} elsif($HmainMode eq 'owner') {
	# ��ȯ�⡼��
	require('./hako-map.cgi');
	ownerMain();

} elsif($HmainMode eq 'command') {
	# ���ޥ�����ϥ⡼��
	require('./hako-map.cgi');
	commandMain();

} elsif($HmainMode eq 'comment') {
	# ���������ϥ⡼��
	require('./hako-map.cgi');
	commentMain();

} elsif($HmainMode eq 'fleetname') {
	# ����̾�ѹ��⡼��
	require('./hako-map.cgi');
	fleetnameMain();

} elsif($HmainMode eq 'priority') {
	# ��Ũ���ѹ��⡼��
	require('./hako-map.cgi');
	priorityMain();

} elsif($HmainMode eq 'earth') {
	# ����ɽ������⡼��
	require('./hako-map.cgi');
	earthMain();

} elsif($HmainMode eq 'comflag') {
	# ���ޥ�ɼ¹�����⡼��
	require('./hako-map.cgi');
	comflagMain();

} elsif($HmainMode eq 'preab') {
	# �رĶ�Ʊ��ȯ�⡼��
	require('./hako-map.cgi');
	preabMain();

} elsif($HmainMode eq 'lbbs') {
	# ������Ǽ��ĥ⡼��
	require('./hako-map.cgi');
	require('./hako-lbbs.cgi');
	localBbsMain();

} elsif($HmainMode eq 'change') {
	# �����ѹ��⡼��
	require('./hako-make.cgi');
	changeMain();

} elsif($HmainMode eq 'FightIsland') {
	# �ȡ��ʥ��� �ԼԤ���ɽ��
	require('hako-map.cgi');
	fightMap($HadminMode);

} elsif($HmainMode eq 'FightView') {
	# �ȡ��ʥ��� LOG�⡼��
	require('hako-table.cgi');
	FightViewMain();

} elsif($HmainMode eq 'TimeTable') {
	# �ȡ��ʥ��� ������ơ��֥�
	require('hako-table.cgi');
	TimeTableMain();

} elsif($HmainMode eq 'camp') {
	# �رĥ⡼��
	require('./hako-map.cgi');
	require('./hako-camp.cgi');
	campMain();

} elsif($HmainMode eq 'join') {
	# ���������õ��
	require('./hako-make.cgi');
	require('./hako-map.cgi');
	newIslandTop();

} elsif($HmainMode eq 'rename') {
	# ���̾���ȥѥ���ɤ��ѹ�
	require('./hako-make.cgi');
	renameIslandMain();

} elsif($HmainMode eq 'joinally') {
	# Ʊ������
	require('./hako-make.cgi');
	newAllyTop();

} elsif($HmainMode eq 'localimg') {
	# �����Υ���������
	require('./hako-limg.cgi');
	localImgMain();

} elsif($HmainMode eq 'hakoskin') {
	# Ȣ�����������
	require('./hako-skin.cgi');
	hakoSkinMain();

} elsif($HmainMode eq 'rank') {
	# ��󥭥�
	require('./hako-rank.cgi');
	rankIslandMain();

} elsif($HmainMode eq 'rekidai') {
	# ���嵭Ͽ
	require('./hako-reki.cgi');
	rankingReki();

} elsif($HmainMode eq 'aoa') {
	# Ʊ�����ͧ��������
	require('./hako-top.cgi');
	amityOfAlly();

} elsif($HmainMode eq 'amity') {
	# ͧ�����������
	require('./hako-table.cgi');
	amityInfo();

} elsif($HmainMode eq 'item') {
	# �����ƥ��������
	require('./hako-table.cgi');
	ItemInfo();

} elsif($HmainMode eq 'fleet') {
	# ������ͭ����
	require('./hako-table.cgi');
	fleetInfo();

} elsif($HmainMode eq 'mfleet') {
	# ���⶯����ư�⡼��
	require('./hako-admin.cgi');
	moveFleetAdmin();

} elsif($HmainMode eq 'bfield') {
	# BattleField�����⡼��
	require('./hako-make.cgi');
	bfieldMain();

} elsif($HmainMode eq 'esetup') {
	# ���٥������⡼��
	require('./hako-admin.cgi');
	setupEvent();

} elsif($HmainMode eq 'download') {
	# ��¸�ǡ�����������ɥ⡼��
	require('./hako-admin.cgi');
	dataDownload($HadminMode);

} elsif($HmainMode eq 'vlose') {
	# ��¸�ǡ��������⡼��
	require('./hako-admin.cgi');
	loseIslandAdminTop();

} elsif($HmainMode eq 'reload') {
	# ��¸�ǡ��������⡼��
	require('./hako-map.cgi');
	fightMap($HadminMode);

} elsif($HmainMode eq 'delete') {
	# ��¸�ǡ�������⡼��
	require('./hako-admin.cgi');
	dataDelete($HadminMode);

} elsif($HmainMode eq 'present') {
	# �����ͤˤ��ץ쥼��ȥ⡼��
	require('./hako-admin.cgi');
	presentMain();

} elsif($HmainMode eq 'punish') {
	# �����ͤˤ�����ۥ⡼��
	require('./hako-admin.cgi');
	punishMain();

} elsif($HmainMode eq 'lchange') {
	# �����ͤˤ���Ϸ��ѹ��⡼��
	require('./hako-admin.cgi');
	lchangeMain();

} elsif($HmainMode eq 'predelete') {
	# �����ͤˤ�뤢������⡼��
	require('./hako-admin.cgi');
	preDeleteMain();

} elsif($HmainMode eq 'asetup') {
	# ͧ���������ǧ�⡼��
	require('./hako-admin.cgi');
	amitySetupMain();

} elsif($HmainMode eq 'wsetup') {
	# �����۹��ǧ�⡼��
	require('./hako-admin.cgi');
	dewarSetupMain();

} elsif($HmainMode eq 'isetup') {
	# ��ǡ��������⡼��
	require('./hako-make.cgi');
	islandSetupMain();

} elsif($HmainMode eq 'isave') {
	# �Ϸ��ǡ�����¸�������⡼��
	require('./hako-map.cgi');
	islandSaveMain();

} elsif($HmainMode eq 'icounter') {
	# ��ĥ�ǡ��� �����󥿡�����⡼��
	require('./hako-map.cgi');
	islandCounterMain();

} elsif($HmainMode eq 'setupv') {
	# ��������ǧ�⡼��
	require('./hako-table.cgi');
	setupValue();

} else {
	# ����¾�ξ��ϥȥåץڡ����⡼��
	require('./hako-top.cgi');
	topPageMain();
}

# �եå�����
tempFooter();

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
	my($command, $number) = @_;
	my($i);

	# ���줾�줺�餹
	splice(@$command, $number, 1);

	# �Ǹ�˻�ⷫ��
	$command->[$HcommandMax - 1] = {
		'kind' => $HcomDoNothing,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
	};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
	my($command, $number) = @_;
	my($i);

	# ���줾�줺�餹
	return if $number == $#$command;
	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------
# CGI���ɤߤ���
sub cgiInput {
	my($line, $getLine);

	# ���Ϥ������ä����ܸ쥳���ɤ�EUC��
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	jcode::convert(\$line, 'euc'); # jcode���ѻ�
#HdebugOut("$line\n");
	if($line !~ /Allypact=([^\&]*)\&/) {
#		$line =~ s/[\x00-\x1f\,]//g;
		$line =~ s/[\x00-\x1f]//g;
		$line =~ s/\,/��/g;
	} else {
# ���祳���ȥ⡼��
# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'allypact';
		$HdefaultPassword = htmlEscape($1);
		$line =~ /AllypactMode=([0-9]+)\&/;
		$HallyPactMode = $1 + 1;
		$line =~ /ISLANDID=([0-9]+)\&/;
		$HcurrentID = $1;
		if($HallyPactMode == 2) {
			while($line =~/VETOID=([0-9]*)\&/g) {
				push(@HvetoID, $1);
			}
			$line =~ /VETOKIND=([0-9]*)\&/;
			$HvetoKind = $1;
			$line =~ /ALLYCOMMENT=([^\&]*)\&/;
			$HallyComment = cutColumn($1, $HlengthAllyComment*2);
			$line =~ /ALLYTITLE=([^\&]*)\&/;
			$HallyTitle = cutColumn($1, $HlengthAllyTitle*2);
			$line =~ s/(.*)ALLYMESSAGE=//g;
			$HallyMessage = cutColumn($line, $HlengthAllyMessage*2);
		}
		return;
	}
	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};
#HdebugOut("$getLine\n");
	# �оݤ���
	if($line =~ /ISLANDID=([0-9]+)\&/){
		$HcurrentID = $1;
	}

	# �ѥ����
	if($line =~ /OLDPASS=([^\&]*)\&/) {
		$HoldPassword = $HdefaultPassword = htmlEscape($1);
	}
	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = $HdefaultPassword = htmlEscape($1);
	}
	if($line =~ /PASSWORD2=([^\&]*)\&/) {
		$HinputPassword2 = htmlEscape($1);
	}

	# �ʣ���᥹����ץȥ⡼��
	if($line =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	} elsif($getLine =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}

	# ��Ʊ���̿��ե饰
	if($line =~ /async=true\&/) {
		$Hasync = 1;
	}

	# main mode�μ���
	if($line =~ /TurnButton/) {
		if(($Hdebug == 1)) {
			$HmainMode = 'Hdebugturn';
		}
	} elsif($getLine =~ /Top=([^\&]*)/) {
		$HtopTemplateFile = $1;
		if($HtopTemplateFile !~ /.htm/) {
			$HtopTemplateFile = '';
		}
		$HmainMode = 'top';
	} elsif($line =~ /OwnerButton/) {
		if($HcurrentID) {
			$HmainMode = 'owner';
		}
	} elsif($line =~ /CommandJavaButton([0-9]+)=/ || $line =~ /CommandJavaButtonSub([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��ʣʣ���᥹����ץȡ�
		$HcurrentID = $1;
		$HmainMode = 'commandJava';
		$line =~ /COMARY=([^\&]*)\&/;
		$HcommandComary = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /TARGETID2=([^\&]*)\&/;
		$HcommandTarget2 = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		# ���ޥ�ɤΥݥåץ��åץ�˥塼�򳫤���
		if($line =~ /MENUOPEN=on/) {
			$HmenuOpen = 'CHECKED';
		} elsif($line =~ /MENUOPEN2=on/) {
			$HmenuOpen2 = 'CHECKED';
		} elsif($line =~ /MENUOPEN3=on/) {
			$HmenuOpen3 = 'CHECKED';
		}
	} elsif($line =~ /CommandButton([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��
		$HcurrentID = $1;
		if($HjavaMode eq 'java'){
			$HmainMode = 'command2';
		}else{
			$HmainMode = 'command';
		}

		# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /TARGETID2=([^\&]*)\&/;
		$HcommandTarget2 = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		if($line =~ /COMMANDMODE=(write|insert|delete)/) {
			$HcommandMode = $1;
		}
		# ���ޥ�ɤΥݥåץ��åץ�˥塼�򳫤���
		if($line =~ /MENUOPEN=on/) {
			$HmenuOpen = 'CHECKED';
		} elsif($line =~ /MENUOPEN2=on/) {
			$HmenuOpen2 = 'CHECKED';
		} elsif($line =~ /MENUOPEN3=on/) {
			$HmenuOpen3 = 'CHECKED';
		}
	} elsif($getLine =~ /Sight=([0-9]*)/) {
		$HmainMode = 'print';
		$HcurrentID = $1;
		# �����ͥ⡼��
		if($getLine =~ /ADMINMODE=([0-9]*)/) {
			$HadminMode = 1;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		}
	} elsif($getLine =~ /OceanMap=([0-9]*)/) {
		# ����ޥåפ�ɽ��
		if($HuseOceanMap) {
			$HmainMode = 'oceanmap';
			$HcurrentID = $1;
		}
	} elsif($line =~ /LbbsButton(..)([0-9]*)/) {
		$HmainMode = 'lbbs';
		if($1 eq 'AD') {
			# ������
			$HlbbsMode = 7;
		} elsif($1 eq 'DA') {
			# �����ͺ��
			$HlbbsMode = 9;
		} elsif($1 eq 'VA') {
			# �����ͱ������ѹ�
			$HlbbsMode = 11;
		} elsif($1 eq 'OW') {
			# ���
			$HlbbsMode = 1;
		} elsif($1 eq 'DL') {
			# �����
			$HlbbsMode = 3;
		} elsif($1 eq 'VO') {
			# ���������ѹ�
			$HlbbsMode = 5;
		} elsif($1 eq 'VS') {
			# �Ѹ��Ա������ѹ�
			$HlbbsMode = 6;
		} elsif($1 eq 'DS') {
			# �Ѹ��Ժ��
			$HlbbsMode = 2;
		} elsif($1 eq 'CK') {
			# �Ѹ��Զ����ǧ
			$HlbbsMode = 4;
		} else {
			# �Ѹ���
			$HlbbsMode = 0;
			$mode = 1;
		} 
		$HcurrentID = $2;

		if($line =~ /LBBSNAME=([^\&]*)\&/) {
			$HlbbsName = cutColumn($1, $HlengthLbbsName*2);
			$HdefaultName = $HlbbsName;
		}
		if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
			my $lbbsMessage = $1;
			my $comment_length = $HlengthLbbsMessage * 2;
			if(($HlbbsAutolinkSymbol ne '') && ($lbbsMessage =~ /((http|ftp):\/\/([^\x81-\xFF\s\"\'\(\)\<\>\\\`\[\{\]\}\|]+))/ )) {
				my $matched_url = $1;
				$comment_length += length($matched_url) - 2;
			}
			$HlbbsMessage = cutColumn($lbbsMessage, $comment_length);
		}
		# �Ǽ��Ĥ�ȯ����
		$line =~ /ISLANDID2=([0-9]+)\&/;
		$HspeakerID = $1;
		# �Ǽ��Ĥ��̿�����
		$line =~ /LBBSTYPE=([^\&]*)\&/;
		$HlbbsType = $1;
		# ������⤷��ʤ��Τǡ��ֹ�����
		if($line =~ /NUMBER=([^\&]*)\&/) {
			$HcommandPlanNumber = $1;
		}
		# ����������
		if($line =~ /LBBSVIEW=([0-9]+)\&/) {
			$HlbbsView = $1;
		}
	} elsif($line =~ /ChangeInfoButton/) {
		$HmainMode = 'change';

		# ̾������ξ��
		if($line =~ /ISLANDNAME=([^\&]*)\&/){
			$HcurrentName = htmlEscape(cutColumn($1, $HlengthIslandName*2));
		}
		# �����ʡ�̾�μ���
		if($line =~ /OWNERNAME=([^\&]*)\&/){
			$HcurrentOwnerName = htmlEscape(cutColumn($1, $HlengthOwnerName*2));
		}
	} elsif($line =~ /MessageButton([0-9]*)/) {
		$HmainMode = 'comment';
		$HcurrentID = $1;
		# ��å�����
		if($line =~ /MESSAGE=([^\&]*)\&/){
			$Hmessage = cutColumn($1, $HlengthMessage*2);
		}
	} elsif($line =~ /FleetnameButton([0-9]*)/) {
		$HmainMode = 'fleetname';
		$HcurrentID = $1;
		# ����̾
		$line =~ /FLEET1=([^\&]*)\&FLEET2=([^\&]*)\&FLEET3=([^\&]*)\&FLEET4=([^\&]*)\&/;
		$HfleetName[0] = cutColumn($1, $HlengthFleetName*2);
		$HfleetName[1] = cutColumn($2, $HlengthFleetName*2);
		$HfleetName[2] = cutColumn($3, $HlengthFleetName*2);
		$HfleetName[3] = cutColumn($4, $HlengthFleetName*2);
	} elsif($line =~ /PriorityButton([0-9]*)/) {
		$HmainMode = 'priority';
		$HcurrentID = $1;
		# ��Ũ��
		$line =~ /PSF=([0-9])\&PS0=([0-9])\&PS1=([0-9])\&PS2=([0-9])\&PS3=([0-9])\&PS4=([0-9])\&PS5=([0-9])\&PS6=([0-9])\&PS7=([0-9])\&/;
		$HfleetNumber = $1;
		$HfleetPriority = "$2-$3-$4-$5-$6-$7-$8-$9";
	} elsif($line =~ /EarthButton([0-9]*)/) {
		$HmainMode = 'earth';
		$HcurrentID = $1;
	} elsif($line =~ /ComflagButton([0-9]*)/) {
		$HmainMode = 'comflag';
		$HcurrentID = $1;
	} elsif($line =~ /PreabButton([0-9]*)/) {
		$HmainMode = 'preab';
		$HcurrentID = $1;
	} elsif($getLine =~ /View=([0-9]*)/) {
		$HmainMode = 'top';
		$HviewIslandNumber = $1;
	} elsif($getLine =~ /IslandMap=([0-9]*)/) {
		$HmainMode = 'landmap';
		$HcurrentID = $1;
		if($getLine =~ /MISSILEMODE=([0-9]*)/) {
			# �ߥ�����������
			$HmissileMode = $1;
		}
	} elsif($getLine =~ /JoinA=([^\&]*)/) {
		$HmainMode = 'joinally';
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /NewAllyButton/) {
		$HmainMode = 'newally';
		# Ʊ��̾�μ���
		if($line =~ /ALLYNUMBER=([0-9]*)\&/) {
			$HcurrentAnumber = $1;
		}
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		$line =~ /ALLYNAME=([^\&]*)\&/;
		$HallyName = htmlEscape(cutColumn($1, $HlengthAllyName*2));
		$line =~ /MARK=([^\&]*)\&/;
		$HallyMark = $1;
		$line =~ /COLOR1=([0-9A-F])\&COLOR2=([0-9A-F])\&COLOR3=([0-9A-F])\&COLOR4=([0-9A-F])\&COLOR5=([0-9A-F])\&COLOR6=([0-9A-F])\&/;
		$HallyColor = $1 . $2 . $3 . $ 4 . $5 . $6;
	} elsif($line =~ /DeleteAllyButton/) {
		$HmainMode = 'delally';
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		$line =~ /ALLYNUMBER=([0-9]*)\&/;
		$HcurrentAnumber = $1;
	} elsif($line =~ /JoinAllyButton/) {
		$HmainMode = 'inoutally';
		$line =~ /ALLYNUMBER=([0-9]*)\&/;
		$HcurrentAnumber = $1;
	} elsif($getLine =~ /AmiOfAlly=([0-9]*)/) {
		$HmainMode = 'aoa';
		$HallyID = $1;
	} elsif($getLine =~ /Allypact=([^\&]*)/) {
		# ���祳���ȥ⡼��
		# �ǽ�ε�ư
		$HmainMode = 'allypact';
		$HallyPactMode = 0;
		$HcurrentID = $1;

	} elsif($getLine =~ /Amity=([0-9]*)/) {
		$HmainMode = 'amity';
	} elsif($getLine =~ /Item=([0-9]*)/) {
		$HmainMode = 'item';
		$HitemNumber = $1;
	} elsif($getLine =~ /Fleet=([0-9]*)/) {
		$HmainMode = 'fleet';
		$HinfoMode = $1;
	} elsif ($line =~ /camp=([0-9]*)/) {
		$HmainMode = 'camp';
		$HcurrentCampID = $1;
		if($line =~ /jpass=([a-zA-Z0-9]*)/) {
			$HtakayanPassword = htmlEscape($1); # �رĥѥ����
		}
		if($line =~ /cpass=([^\&]*)\&/) {
			$HcampPassword = htmlEscape($1);
		}
		if($line =~ /id=([0-9]*)/) {
			$HcurrentID = $1;
		}
	} elsif($getLine =~ /Rank=([0-9]*)/) {
		$HmainMode = 'rank';
	} elsif($getLine =~ /Rekidai=([0-9]*)/) {
		$HmainMode = 'rekidai';
	} elsif($getLine =~ /Rename=([0-9]*)/) {
		$HmainMode = 'rename';
	} elsif($getLine =~ /Limg=([0-9]*)/) {
		$HmainMode = 'localimg';
	} elsif($getLine =~ /Skin=([0-9]*)/) {
		$HmainMode = 'hakoskin';
	} elsif($getLine =~ /Join=([0-9]*)/) {
		# ï�Ǥ⿷�������õ����
		$HmainMode = ($HadminJoinOnly ? 'top' : 'join');
	} elsif($line =~ /Join=([0-9]*)/) {
		# �����ͤ��������������õ����
		$HmainMode = ($HadminJoinOnly ? 'join' : 'top');
	} elsif($line =~ /NewIslandButton/) {
		$HmainMode = 'new';
		# ̾���μ���
		$line =~ /ISLANDNAME=([^\&]*)\&/;
		$HcurrentName = htmlEscape(cutColumn($1, $HlengthIslandName*2));
		# �����ʡ�̾�μ���
		$line =~ /OWNERNAME=([^\&]*)\&/;
		$HcurrentOwnerName = htmlEscape(cutColumn($1, $HlengthOwnerName*2));
		if($HarmisticeTurn && $HcampSelectRule == 2) {
			# �رĤ������ǽ�ʾ��
			if($line =~ /CAMPNUMBER=([\-]?[0-9]+)\&/) {
				$HcampNumber = $1;
			}
		}
		if($HoceanMode && $HoceanSelect) {
			# ��ɸ�������ǽ�ʾ��
			if($line =~ /OCEANX=([^\&]*)\&/) {
				$HoceanMapX = $1;
			}
			if($line =~ /OCEANY=([^\&]*)\&/) {
				$HoceanMapY = $1;
			}
			if($line =~ /RANDOM=([0-9]*)\&/) {
				$HmapRandom = $1;
			}
		}

# ��������ǧ�⡼��
	} elsif($getLine =~ /SetupV=([^\&]*)/) {
		$HmainMode = 'setupv';
		$HdefaultPassword = htmlEscape($1);

# �ȡ��ʥ��ȥ⡼��
	} elsif($getLine =~ /LoseMap=([0-9]*)/) {
		$HmainMode = 'FightIsland';
		$HadminMode = 0;
		$HcurrentID = $1;
		if($getLine =~ /ADMINMODELOSE=([0-9]*)/) {
			$HadminMode = 2;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		} elsif($getLine =~ /ADMINMODESAVE=([0-9]*)/) {
			$HadminMode = 1;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		}
	} elsif($getLine =~ /FightLog/) {
		$HmainMode = 'FightView';
	} elsif($getLine =~ /TimeTable/) {
		$HmainMode = 'TimeTable';

# ͧ���������ǧ�⡼��
	} elsif($getLine =~ /ASetup=([^\&]*)/) {
		$HmainMode = 'asetup';
		$HasetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /ASetup=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'asetup';
		$HasetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		while($line =~/amity=([^\&]*)\&/g) {
			push(@HamityChange, $1);
		}
		while($line =~/ally=([^\&]*)\&/g) {
			push(@HallyChange, $1);
		}

# �����۹��ǧ�⡼��
	} elsif($getLine =~ /WSetup=([^\&]*)/) {
		$HmainMode = 'wsetup';
		$HwsetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /WSetup=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'wsetup';
		$HwsetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		while($line =~/war=([0-9]*)\&/g) {
			push(@HdeWarChange, $1);
		}
		while($line =~/del=([0-9]*)\&/g) {
			$HdeWarDel{$1} = 1;
		}

# ��ǡ��������⡼��
	} elsif($getLine =~ /ISetup=([^\&]*)/) {
		$HmainMode = 'isetup';
		$HisetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
		if($getLine =~ /id=([0-9]*)/) {
			$HcurrentID = $1;
		}
	} elsif($line =~ /ISetup=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'isetup';
		$HisetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		if($line =~ /IslandChange/) {
			$HisetupMode = 2;
			# ̾���μ���
			$line =~ /ISLANDNAME=([^\&]*)\&/;
			$HcurrentName = cutColumn($1, $HlengthIslandName*2);
			# �����ʡ�̾�μ���
			$line =~ /OWNERNAME=([^\&]*)\&/;
			$HcurrentOwnerName = cutColumn($1, $HlengthOwnerName*2);
			$line =~ /BIRTHDAY=([0-9]*)\&/;
			$Hbirthday = $1;
			$line =~ /ABSENT=([0-9]*)\&/;
			$Habsent = $1;
			if($line =~ /PREAB=([0-9]*)\&/) {
				$Hpreab = $1;
			}
			$line =~ /MONEY=([0-9]*)\&/;
			$Hmoney = $1;
			$line =~ /FOOD=([0-9]*)\&/;
			$Hfood = $1;
			$line =~ /GAIN=([0-9]*)\&/;
			$Hgain = $1;
			if($line =~ /FIELD=([0-9]*)\&/) {
				$Hfield = $1;
			}
			$line =~ /FIGHT_ID=([\-0-9]*)\&/;
			$Hfight_id = $1;
			$line =~ /REST=([0-9]*)\&/;
			$Hrest = $1;
			while($line =~/FLAGS=([0-9]*)\&/g) {
				push(@Hflags, $1);
			}
			while($line =~/MONSTERS=([0-9]*)\&/g) {
				push(@Hmonsters, $1);
			}
			$line =~ /MONSTERKILL=([0-9]*)\&/;
			$Hmonsterkill = $1;
			while($line =~/HMONSTERS=([0-9]*)\&/g) {
				push(@Hhmonsters, $1);
			}
			while($line =~/SINK=([0-9]*)\&/g) {
				push(@Hsink, $1);
			}
			while($line =~/SINKSELF=([0-9]*)\&/g) {
				push(@Hsinkself, $1);
			}
			while($line =~/EXT=([0-9]*)\&/g) {
				push(@Hext, $1);
			}
			while($line =~/SUBEXT=([0-9]*)\&/g) {
				push(@HsubExt, $1);
			}
			while($line =~/ITEM=([0-9]*)\&/g) {
				push(@HtmpItem, $1);
			}
			while($line =~/WEATHER=([0-9]*)\&/g) {
				push(@HtmpWeather, $1);
			}
			if($HoceanMode) {
				# ��ɸ�������ǽ�ʾ��
				if($line =~ /OCEANX=([^\&]*)\&/) {
					$HoceanMapX = $1;
				}
				if($line =~ /OCEANY=([^\&]*)\&/) {
					$HoceanMapY = $1;
				}
				if($line =~ /RANDOM=([0-9]*)\&/) {
					$HmapRandom = $1;
				}
			}
		}

# �Ϸ��ǡ�����¸�������⡼��
	} elsif($getLine =~ /ISave=([^\&]*)/) {
		$HmainMode = 'isave';
		$HisaveMode = 0;
	} elsif($line =~ /ISave=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'isave';
		$HisaveMode = 1;
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		if($line =~ /SaveButton/) {
			# ��¸
			$HisaveMode = 2;
		} elsif($line =~ /LoadButton/) {
			# ����
			$HisaveMode = 3;
		} elsif($line =~ /ChangeButton/) {
			# ��¸������(�ǡ����������ؤ�)
			$HisaveMode = 4;
		} elsif($line =~ /SaveLandButton/) {
			# ��¸(���������)
			$HisaveMode = 5;
		} elsif($line =~ /LoadLandButton/) {
			# ����(���������)
			$HisaveMode = 6;
		} elsif($line =~ /ChangeLandButton/) {
			# ��¸������(���������)
			$HisaveMode = 7;
		}

# ��¸�ǡ������������
	} elsif($getLine =~ /Download=([^\&]*)\&/) {
		$HmainMode = 'download';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		$getLine =~ /mode=([0-9]*)\&/;
		$HadminMode = $1;
		$getLine =~ /id=([0-9]*)/;
		$HcurrentID = $1;

# ��¸�ǡ�������
	} elsif($getLine =~ /ViewLose=([^\&]*)/) {
		$HmainMode = 'vlose';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
	} elsif($line =~ /Reload=([^\&]*)/) { # �����ܥ��󲡲�
		$HmainMode = 'vlose';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		if($line =~ /ReloadButton/) {
			if($line =~ /RELOADIDLOSE=([0-9]*)/) {
				$HmainMode = 'reload';
				$HadminMode = 4;
				$HcurrentID = $1;
			} elsif($line =~ /RELOADIDSAVE=([0-9]*)/) {
				$HmainMode = 'reload';
				$HadminMode = 3;
				$HcurrentID = $1;
			}
		} elsif($line =~ /DeleteButton/) {
			while($line =~/DELETEIDLOSE=([0-9]*)\&/g) {
				push(@HloseID, $1);
				$HadminMode |= 2;
			}
			while($line =~/DELETEIDSAVE=([0-9]*)\&/g) {
				push(@HsaveID, $1);
				$HadminMode |= 1;
			}
			$HmainMode = 'delete' if($HadminMode);
		}

# ��ĥ�ǡ��� �����󥿡�����⡼��
	} elsif($getLine =~ /ICounter=([^\&]*)/) {
		my $tmp = $1; 
		$HdefaultPassword = htmlEscape($tmp) if($tmp ne '0');
		$HmainMode = 'icounter';
		$HicounterMode = 0;
	} elsif($line =~ /ICounter=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'icounter';
		$HicounterMode = 1;
		$HinputPassword = $HdefaultPassword = htmlEscape($1);
		if($line =~ /AllSetButton/) {
			$HicounterMode = 4;
		} elsif($line =~ /SetButton/) {
			$HicounterMode = 2;
		} elsif($line =~ /AllDelButton/) {
			$HicounterMode = 5;
		} elsif($line =~ /DelButton/) {
			$HicounterMode = 3;
		}

# ���⶯����ư�⡼��
	} elsif($getLine =~ /Mfleet=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'mfleet';
		$HmfleetMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Mfleet=([^\&]*)\&/) {
		# ���⶯����ư�ܥ��󤬲����줿��ư
		$HmainMode = 'mfleet';
		$HmfleetMode = 1;
		$HdefaultPassword = htmlEscape($1);
		$line =~ /FROMID=([0-9]*)\&/;
		$HfromID = $1;
		$line =~ /TOID=([0-9]*)\&/;
		$HtoID = $1;
		$line =~ /FLEETNUMBER=([0-4])\&/;
		$HfleetNo = $1;

# ���٥������⡼��
	} elsif($getLine =~ /Esetup=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'esetup';
		$HsetEventMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Esetup=([^\&]*)\&/) {
		# ���٥������ܥ��󤬲����줿��ư
		$HmainMode = 'esetup';
		$HdefaultPassword = htmlEscape($1);
		if($line =~ /SetEventButton/) {
			$HsetEventMode = 1;
			$line =~ /START=([0-9]*)\&/;
			$Hstart = $1;
			$line =~ /TURM=([0-9]*)\&/;
			$Hturm = $1;
			$line =~ /MAXSHIP=([0-9]*)\&/;
			$Hmaxship = $1;
			while($line =~/KIND=([0-9]*)\&/g) {
				$HpermitKind |= (2 ** $1);
			}
			$line =~ /ADDITION=([0-9]*)\&/;
			$Haddition = $1;
			while($line =~/RESTRICTION=([0-9]*)\&/g) {
				$Hrestriction |= (2 ** $1);
			}
			$line =~ /TYPE=([0-9]*)\&/;
			$Htype = $1;
			$line =~ /AUTORETURN=([0-9]*)\&/;
			$HautoReturn = $1;
			$line =~ /MONSTERTURN=([0-9]*)\&/;
			$HmonsterTurn = $1;
			$line =~ /MONSTERNUMBER=([0-9]*)\&/;
			$HmonsterNumber = $1;
			$line =~ /HUGEMONSTERTURN=([0-9]*)\&/;
			$HhugeMonsterTurn = $1;
			$line =~ /HUGEMONSTERNUMBER=([0-9]*)\&/;
			$HhugeMonsterNumber = $1;
			$line =~ /UNKNOWNTURN=([0-9]*)\&/;
			$HunkownTurn = $1;
			$line =~ /UNKNOWNNUMBER=([0-9]*)\&/;
			$HunkownNumber = $1;
			$line =~ /CORETURN=([0-9]*)\&/;
			$HcoreTurn = $1;
			$line =~ /CORENUMBER=([0-9]*)\&/;
			$HcoreNumber = $1;
			$line =~ /COREMINHP=([0-9]*)\&/;
			$HcoreMinHP = $1;
			$line =~ /COREMAXHP=([0-9]*)\&/;
			$HcoreMaxHP = $1;
			$line =~ /COREFLAG=([0-9]*)\&/;
			$HcoreFlag = $1;
			$line =~ /MONEY=([0-9]*)\&/;
			$HprizeMoney = int($1);
			$line =~ /FOOD=([0-9]*)\&/;
			$HprizeFood = int($1);
			if($line =~ /PRESENT=([0-9]*)\&/) {
				$HprizePresent = int($1);
			}
			my(%tmpItem);
			while($line =~/ITEM=([0-9]*)\&/g) {
				$tmpItem{$1} = 1;
			}
			foreach(0..$#HitemName) {
				push(@HprizeItem, int($tmpItem{$_}));
			}
		} else {
			$HsetEventMode = 2;
			while($line =~/DEL=([0-9]*)\&/g) {
				$HeventDel{$1} = 1;
			}
		}

# BattleField�����⡼��
	} elsif($getLine =~ /Bfield=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'bfield';
		$HbfieldMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Bfield=([^\&]*)\&/) {
		# BattleField�����ܥ��󤬲����줿��ư
		$HmainMode = 'bfield';
		$HbfieldMode = 1;
		$HdefaultPassword = htmlEscape($1);
		if($HoceanMode) {
			# ��ɸ�������ǽ�ʾ��
			if($line =~ /OCEANX=([^\&]*)\&/) {
				$HoceanMapX = $1;
			}
			if($line =~ /OCEANY=([^\&]*)\&/) {
				$HoceanMapY = $1;
			}
			if($line =~ /RANDOM=([0-9]*)\&/) {
				$HmapRandom = $1;
			}
		}

# �����ͤˤ��ץ쥼��ȥ⡼��
	} elsif($getLine =~ /Present/) {
		# �ǽ�ε�ư
		$HmainMode = 'present';
		$HpresentMode = 0;
	} elsif($line =~ /Present/) {
		# �ץ쥼��ȥܥ��󤬲����줿��ư
		$HmainMode = 'present';
		$HpresentMode = 1;
		($HpresentMoney) = ($line =~ /PRESENTMONEY=([^\&]*)\&/);
		($HpresentFood ) = ($line =~ /PRESENTFOOD=([^\&]*)\&/);
		$line =~ /PRESENTLOG=([^\&]*)\&/;
		$HpresentLog = cutColumn($1, $HlengthPresentLog*2);

# �����ͤˤ�����ۥ⡼��
	} elsif($getLine =~ /Punish=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'punish';
		$HpunishMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Punish=([^\&]*)\&/) {
		# ���ۥܥ��󤬲����줿��ư
		$HmainMode = 'punish';
		$HpunishMode = 1;
		$HdefaultPassword = htmlEscape($1);

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /PUNISHID=([^\&]*)\&/;
		$HpunishID = $1;

# �����ͤˤ���Ϸ��ѹ��⡼��
	} elsif($getLine =~ /Lchange=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Lchange=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'lchange';
		$HlchangeMode = 1;
		$HdefaultPassword = htmlEscape($1);

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /LCHANGEKIND=([^\&]*)\&/;
		$HlchangeKIND = $1;
		$line =~ /LCHANGEVALUE=([^\&]*)\&/;
		$HlchangeVALUE = $1;

# �����ͤˤ�뤢������⡼��
	} elsif($getLine =~ /Pdelete=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'predelete';
		$HpreDeleteMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Pdelete=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'predelete';
		$HpreDeleteMode = 1;
		$HdefaultPassword = htmlEscape($1);
		$line =~ /SETTURN=([0-9]*)\&/;
		$HsetTurn = $1;

# ��Х���⡼��
	} elsif($line =~ /Mobile([0-9]*)/) {
		$HmainMode = $1;

# ����¾�ϥȥåץ⡼��
	} else {
		$HmainMode = 'top';
	}

	if($line =~ /IMGLINEMAC=([^&]*)\&/){
		my($flag) = $1;
		if($flag eq ''){
			$flag = $HimageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file://' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /IMGLINE=([^&]*)\&/){
		my($flag) = $1;
		$flag =~ tr/\\/\//;
		if(($flag eq 'deletemodenow') || ($flag eq '')){
			$flag = $HimageDir;
		} else {
			$flag =~ s/:/|/g;
			$flag =~ s/\/[\w\.]+\.gif$//g;
			$flag = 'file://' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /SKIN=([^\&]*)\&/) {
		my($flag) = $1;
		if(($flag eq 'del') || ($flag eq '')){
			$flag = "${HcssDir}/$HcssDefault";
		} else {
			$flag = "${HcssDir}/" . $flag;
		}
		$HskinName = $flag;
	}

}

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# directory����å�
		return hakolock1();
	} elsif($lockMode == 2) {
		# flock����å�
		return hakolock2();
	} elsif($lockMode == 3) {
		# symlink����å�
		return hakolock3();
	} elsif($lockMode == 4) {
		# �̾�ե����뼰��å�
		return hakolock4();
	} else {
		# rename����å�
		$lfh = hakolock5() or die return 0;
		return 1;
	}
}

sub hakolock1 {
	# ��å���
	if(mkdir('hakojimalock', $HdirMode)) {
		# ����
		return 1;
	} else {
		# ����
		my($b) = (stat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# �������
			unlock();
			# �إå�����
			tempHeader();
			# ���������å�����
			tempUnlock();
			# �եå�����
			tempFooter();
			# ��λ
			exit(0);
		}
		return 0;
	}
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# ����
		return 1;
	} else {
		# ����
		return 0;
	}
}

sub hakolock3 {
	# ��å���
	if(symlink('hakojimalockdummy', 'hakojimalock')) {
		# ����
		return 1;
	} else {
		# ����
		my($b) = (lstat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# �������
			unlock();
			# �إå�����
			tempHeader();
			# ���������å�����
			tempUnlock();
			# �եå�����
			tempFooter();
			# ��λ
			exit(0);
		}
		return 0;
	}
}

sub hakolock4 {
	# ��å���
	if(unlink('lockfile')) {
		# ����
		open(OUT, '>lockfile.lock');
		print OUT time;
		close(OUT);
		return 1;
	} else {
		# ��å����֥����å�
		if(!open(IN, 'lockfile.lock')) {
			return 0;
		}
		my($t);
		$t = <IN>;
		close(IN);
		if(($t != 0) && (($t + $unlockTime) < time)) {
			# 120�ðʾ�вᤷ�Ƥ��顢����Ū�˥�å��򳰤�
			unlock();
			# �إå�����
			tempHeader();
			# ���������å�����
			tempUnlock();
			# �եå�����
			tempFooter();
			# ��λ
			exit(0);
		}
		return 0;
	}
}

# rename��(Perl��� http://www.din.or.jp/~ohzaki/perl.htm#File_Lock)
sub hakolock5 {
	my %lfh = (dir => "./", basename => "lockfile", timeout => $unlockTime, trytime => 3, @_);
	$lfh{path} = $lfh{dir}.$lfh{basename};

	for (my $i = 0; $i < $lfh{trytime}; $i++, sleep 1) {
		return \%lfh if (rename($lfh{path}, $lfh{current} = $lfh{path} . time));
	}

	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);

	foreach (@filelist) {
		if (/^$lfh{basename}(\d+)/) {
			return \%lfh if (time - $1 > $lfh{timeout} and
			rename($lfh{dir} . $_, $lfh{current} = $lfh{path} . time));
			last;
		}
	}
	undef;
}

# ��å��򳰤�
sub unlock {
	if($lockMode == 1) {
		# directory����å�
		rmdir('hakojimalock');
	} elsif($lockMode == 2) {
		# flock����å�
		close(LOCKID);
	} elsif($lockMode == 3) {
		# symlink����å�
		unlink('hakojimalock');
	} elsif($lockMode == 4) {
		# �̾�ե����뼰��å�
		my($i);
		$i = rename('lockfile.lock', 'lockfile');
	} else {
		# rename����å�
		rename($lfh->{current}, $lfh->{path});
	}
}

# �����������֤�
sub min {
	return (sort { $a <=> $b } @_)[0];
}

# �礭�������֤�
sub max {
	return (sort { $b <=> $a } @_)[0];
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "����500${HunitMoney}̤��";
	} else {
		$m = int(($m + 500) / 1000);
		return "����${m}000${HunitMoney}";
	}
}

# 80�������ڤ�·��
sub cutColumn {
	my($s, $c) = @_;
	jcode::convert(\$s, 'euc');
	if(length($s) <= $c) {
		return $s;
	} else {
		if($HlengthAlert) {
			unlock();
			tempHeader();
			tempWrong("ʸ���������С��Ǥ���");
			tempFooter();
			exit(0);
		}
		# ���80�����ˤʤ�ޤ��ڤ���
		my($ss) = '';
		my($count) = 0;
		while($count < $c) {
			$s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
			if($1) {
				$ss .= $1;
				$count ++;
			} else {
				$ss .= $2;
			}
			$count ++;
		}
		return $ss;
	}
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if ($kind == $HlandNavy) {
		# ����
		for ($i = $maxNavyLevel; $i > 1; $i--) {
			if ($exp >= $navyLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	} elsif ($kind == $HlandBase) {
		# �ߥ��������
		for ($i = $maxBaseLevel; $i > 1; $i--) {
			if ($exp >= $baseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	} elsif($kind == $HlandSbase) {
		# �������
		for ($i = $maxSBaseLevel; $i > 1; $i--) {
			if ($exp >= $sBaseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	}
}

# ������и��Ϥ����٥�򻻽�
sub gainToLevel {
	my($gain) = @_;
	my($i);
	for ($i = $HmaxComNavyLevel; $i > 1; $i--) {
		if ($gain >= $HcomNavyBorder[$i - 2]) {
			return $i;
		}
	}
	return 1;
}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# $pnum($pointNumber)(@rpx, @rpy)������
sub makeRandomIslandPointArray {
	my($island) = @_;

	undef $island->{'rpx'};
	undef $island->{'rpy'};
	my(@rpx, @rpy, $map, @x, @y, $xsize, $ysize, $pnum);
	$map = $island->{'map'};
	@x = @{$map->{'x'}};
	@y = @{$map->{'y'}};
	$xsize = @x;
	$ysize = @y;
	$pnum = $xsize * $ysize;

	my($x);
	# �����
	@rpx = (@x) x $ysize;
	foreach $y (@y) {
		push(@rpy, ($y) x $xsize);
	}

	# ����åե�
	my($i, $j);
	for ($i = $pnum; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@rpx[$i,$j] = @rpx[$j,$i];
		@rpy[$i,$j] = @rpy[$j,$i];
	}

	$island->{'pnum'} = $pnum - 1;
	$island->{'rpx'} = \@rpx;
	$island->{'rpy'} = \@rpy;
}

# 0����(n - 1)�����
sub random {
	return int(rand(1) * $_[0]);
}

# ������
sub islandSort {
	my($kind, $mode) = @_;

	my @idx = (0..$#Hislands);
	@idx = sort {
			$Hislands[$b]->{'field'} <=> $Hislands[$a]->{'field'} ||         # �Хȥ�ե������ͥ��
			$Hislands[$a]->{'dead'} <=> $Hislands[$b]->{'dead'} ||           # ���ǥե饰��Ω�äƤ���и���
			$Hislands[$a]->{'predelete'} <=> $Hislands[$b]->{'predelete'} || # �����ͤ�������ե饰��Ω�äƤ���и���
			$Hislands[$b]->{$kind} <=> $Hislands[$a]->{$kind} || # $kind�ǥ�����
			$a <=> $b # $kind��Ʊ���ʤ�����Τޤ�
		   } @idx;
	if($mode) {
		my @Hidx;
		foreach (0..$#idx) {
			$Hidx[$idx[$_]] = $_;
		}
		my %temp = %HidToNumber;
		while (my($k,$v) = each %temp){
			$HidToNumber{$k} = $Hidx[$v] if(defined $v);
		}
	}
	# ��̤Τ�Ȥˤʤ����Ǥξ�硢����򹹿�
	if($kind eq $HrankKind) {
		@Hislands = @Hislands[@idx] ;
		@idx = (0..$#Hislands);
	}
	return $Hislands[$idx[$HbfieldNumber]];
}

# ������(Ʊ���С������)
sub allySort {
	# score��Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = (0..$#Hally);
	@idx = sort {
			$Hally[$a]->{'dead'} <=> $Hally[$b]->{'dead'} || # ���ǥե饰��Ω�äƤ���и���
			$Hally[$b]->{'score'} <=> $Hally[$a]->{'score'} ||
			$a <=> $b
		   } @idx;
	@Hally = @Hally[@idx];
	my @Hidx;
	foreach (0..$#idx) {
		$Hidx[$idx[$_]] = $_;
	}
	my %temp = %HidToAllyNumber;
	while (my($k,$v) = each %temp){
		$HidToAllyNumber{$k} = $Hidx[$v] if(defined $v);
	}
}

# �������ͤ򻻽�
sub estimateNavy {
	my($number) = @_;
	my($island, $fkind, $monslive, $monstertype, $hmonstertype, $unknownlive, $unknowntype);

	# �Ϸ������
	$island = $Hislands[$number];
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# ������
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if ($kind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($value);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				if($HautoKeepID{$nId} && ($nId != $id)) {
					# ���ˤ���
					$land->[$x][$y] = $HlandSea;
					$landValue->[$x][$y] = $nSea;
				} elsif(defined $n) {
#					if(!($nFlag & 1) && !($nSpecial & 0x8)) {
#						$Hislands[$n]->{'ships'}[$nNo]++;
#						$Hislands[$n]->{'ships'}[4]++;
#					}
#					$Hislands[$n]->{'shipk'}[nKind]++;
					my $fvalue = sprintf("%08x", navyPack($id, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp));
					push(@{$Hislands[$n]->{'fkind'}}, "$fvalue");
					$Hislands[$n]->{'navy'}[$nKind]++;
				} elsif(!($nSpecial & 0x8) && !($nFlag & 1)) {
					$unknownlive++;
					$unknowntype |= (2 ** $nKind);
				}
			} elsif(($kind == $HlandMonster) || ($kind == $HlandHugeMonster)){
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($value);
				if($HautoKeepID{$mId}) {
					if ($mFlag & 2) {
						$land->[$x][$y] = $HlandSea;
						$landValue->[$sx][$sy] = $mSea;
					} else {
						$land->[$x][$y] = $HlandWaste;
						$landValue->[$sx][$sy] = 0;
					}
				} elsif(($kind == $HlandHugeMonster) && ($mHflag == 0)) {
					$monslive++;
					$hmonstertype |= (2 ** $mKind);
				} elsif($kind == $HlandMonster) {
					$monslive++;
					$monstertype |= (2 ** $mKind);
				}
			}
		}
	}
	$island->{'monsterlive'}  = "$monslive,$monstertype,$hmonstertype,$unknownlive,$unknowntype";
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	my $nowTurn = -1;

	open(LIN, "${HdirName}/$_[0]$HlogData");
	my($line, $m, $turn, $id1, $id2, $id3, $message, @ids);
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-\s]*),(.*)$/;
		($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
		next if($m eq '');
		@ids = ($id1, $id2, split('-', $id3));
		if ($nowTurn != $turn) {
			out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
			out("<HR>${HtagNumber_}������ $turn${H_tagNumber}\n<BLOCKQUOTE>\n");
			$nowTurn = $turn;
		}

		# ��̩�ط�
		if($m == 1) {
			if(($mode == 0) || ($id1 != $id)) {
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
		my $str = "${m}$message<BR>";
		if($Hmobile) {
			1 while $str =~ s/(.*)(<BR>��--- (.*))/$1<BR>/i;
			1 while $str =~ s/(.*)(<(span[\s\w\=\+\-\#\"\']+)>(.*)<\/span>)/$1$4/i;
			if($str =~ /(��--- )/) {
				if($str !~ /(����|��̩)/) {
					$str = (split(/��/, $str))[0] . '<BR>';
				}
			} elsif($str =~ /(�������� )/) {
				next;
			} elsif($str =~ /(�� )/) {
				1 while $str =~ s/(.*)(<B>(.*)<\/B>)/$1$3/i;
			} else {
				$str = '��' . $str;
			}
		}
		out("$str\n");
	}
	close(LIN);

	out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
}

#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �����
sub tempInitialize {
	my($mode) = @_;

	# �祻�쥯��(�ǥե���ȼ�ʬ)
	$HislandList = getIslandList($defaultID, $mode);
	$HtargetList = getIslandList($defaultTarget, $mode);
}

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
	my($select, $mode, $color) = @_;
	my($list, $name, $id, $s, $i, $c);

	#��ꥹ�ȤΥ�˥塼
	$list = '';
	$list = "<OPTION VALUE=\"0\" SELECTED>��������(���٤Ƴ�)\n" if($select == -1);
	foreach $i (0..$islandNumber) {
		$island = $Hislands[$i];
		next if($mode == 2 && !$island->{'field'});
		$name = islandName($island);
		$name =~ s/<[^<]*>//g;
		$id = $Hislands[$i]->{'id'};
		if($id eq $select) {
			$s = ' SELECTED';
			$c = " style=\"background:$color;\"" if($color ne '');
		} else {
			$s = '';
			$c = '';
		}

		$list .= "<OPTION VALUE=\"$id\"$c$s>${name}\n" if($mode || !$island->{'field'});
	}
	return $list;
}

# ��å�����
sub tempLockFail {
	# �����ȥ�
	out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
	# �����ȥ�
	out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack
END
}

# �ѥ���ɥե����뤬�ʤ�
sub tempNoHpasswordFile {
	out(<<END);
${HtagBig_}�ѥ���ɥե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# �ᥤ��ǡ������ʤ�
sub tempNoDataFile {
	out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# ��������ȯ��
sub tempProblem {
	out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}

# ������
sub tempAnyString {
	out(<<END);
${HtagBig_}$_[0]${H_tagBig}$HtempBack
END
}

# ���ƥʥ���
sub mente_mode {
	# �إå�����
	tempHeader();

	# ��å�����
	out("${HtagBig_}�������ƥʥ���Ǥ���<BR>�ä����Ԥ���������${H_tagBig}");

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}
#----------------------------------------------------------------------
# �إå�
#----------------------------------------------------------------------
sub tempHeader {
	if($HimgLine ne '' ){
		$baseIMG = $HimgLine;
	} else {
		$baseIMG = $HimageDir;
	}
	my($bIstr) = ($HmainMode eq 'setupv') ? "" : "<BASE HREF='${baseIMG}/'>";
	if($HskinName ne '' ){
		$baseSKIN = $HskinName;
	} else {
		$baseSKIN = "${HcssDir}/$HcssDefault";
	}

	# jcode���ѻ���charset��Shift_JIS��
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

	if(!$Hmobile) {
		out(<<END);
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
$HtitleTag($versionInfo)
</TITLE>
$bIstr
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body<DIV ID='BodySpecial'>
<!-- NINJA ANALYZE -->
<script type="text/javascript">
//<![CDATA[
(function(d) {
  var sc=d.createElement("script"),
      ins=d.getElementsByTagName("script")[0];
  sc.type="text/javascript";
  sc.src=("https:"==d.location.protocol?"https://":"http://") + "code.analysis.shinobi.jp" + "/ninja_ar/NewScript?id=00231338&hash=9a215404&zone=36";
  sc.async=true;
  ins.parentNode.insertBefore(sc, ins);
})(document);
//]]>
</script>
<!-- /NINJA ANALYZE -->

<DIV ID='LinkHead'>
$Hheader
END

		my $nextturn = '';
		foreach (1..$HrepeatTurn) {
			$nextturn .= '��' if($_ != 1);
			$nextturn .= $HislandTurn + $_;
			last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
		}
		out(<<END) if($Hrealtimer && (defined $HleftTime));
<DIV ID="REALTIME" class="timer"></DIV>
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
		out("<HR></DIV>");
	} else {
       out(<<END);
<HTML><HEAD><TITLE>$Htitle</TITLE></HEAD>
<BODY bgcolor="#ffffff">


<a href="./hako-main.cgi">�ȥå�</a> <a href="./hako-main.cgi?SetupV=1">�إ��</a> <a href="./hako-main.cgi?FightLog=1">���</a>
<HR>
END
	}
}

#----------------------------------------------------------------------
# �եå�
#----------------------------------------------------------------------
sub tempFooter {
	out(<<END) if(!$Hmobile);
<HR>
<DIV ID='LinkFoot'>
$Hfooter
<DIV align="right">
END
##### �ɲ� ����20020307
	if($Hperformance && !$Hmobile) {
		my($uti, $sti, $cuti, $csti) = times();
		$uti += $cuti;
		$sti += $csti;
		my($cpu) = $uti + $sti;

	#	   ���ե�����񤭽Ф�(�ƥ��ȷ�¬�ѡ����ʤϥ����Ȥˤ��Ƥ����Ƥ�������)
	#	   open(POUT,">>cpu-h.log");
	#	   print POUT "CPU($cpu) : user($uti) system($sti)\n";
	#	   close(POUT);

		out(<<END);
��<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
END
	}
#####
	out(<<END) if(!$Hmobile);
<HR>
<B>���� JS.$versionInfo(based on ver1.3)</B> patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/'>neo_otacky</a>
</DIV></DIV></DIV>
END
	if($oroti) {
		out(<<END);
<script type="text/javascript">
<!--
var image = document.getElementsByTagName('img');
for (var i = 0; i < image.length; i++){
	image[i].src = image[i].src.replace("$HbaseDir","$baseIMG");
}
//-->
</script>

END
	}

	out("</BODY></HTML>");
}
