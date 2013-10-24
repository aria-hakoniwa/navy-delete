# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ���������⥸�塼��(ver1.00)
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

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandMain {
	my($mode) = @_;
	# ������������������å�
	if($HadminJoinOnly) {
		unless($ENV{HTTP_REFERER}  =~ /^$HthisFile/) {
			unlock();
			tempHeader();
			tempNoReferer();
			return 0;
		}
	}
	# �礬���äѤ��Ǥʤ��������å�
	if(
		($HislandNumber - $HbfieldNumber >= $HmaxIsland) ||
		($HsurvivalTurn && ($HislandTurn >= $HsurvivalTurn)) # ���Х��Х�⡼��
		) {
		unlock();
		tempHeader();
		tempNewIslandFull();
		return 0;
	}

	# ��̾�����뤫�����å�
	if($HcurrentName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoName();
		return 0;
	}

	# �����ʡ�̾�����뤫�����å�
	if($HcurrentOwnerName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoOwnerName();
		return 0;
	}

	# ��̾�������������å�
	if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��|^����$/) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempHeader();
		tempNewIslandBadName();
		return 0;
	}

	# �����ʡ�̾�������������å�
	if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempHeader();
		tempNewIslandBadOwnerName();
		return 0;
	}

	# �رĤ����
	my($campNum);
	if($HarmisticeTurn && ($HallyNumber > 1)) {
		if($HcampSelectRule != 2 || $HcampNumber == -1) {
			$campNum = selectCamp();
		} else {
			$campNum = $HcampNumber;
			if ($Hally[$campNum]->{'number'} >= ($HmaxIsland / $HallyNumber)) {
				# ���οرĤ�����
				unlock();
				tempHeader();
				tempNewIslandFull();
				return 0;
			}
		}
	}
	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
		# ���Ǥ�ȯ������
		unlock();
		tempHeader();
		tempNewIslandAlready();
		return 0;
	}

	# password��¸��Ƚ��
	if($HinputPassword eq '') {
		# password̵��
		unlock();
		tempHeader();
		tempNewIslandNoPassword();
		return 0;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempHeader();
		tempWrongPassword();
		return 0;
	}

	# ID�λȤ���
	my $safety = 100;
	while(defined $HidToNumber{$HislandNextID}) {
		$HislandNextID ++;
		$HislandNextID = 1 if($HislandNextID > 100);
		last if(!$safety--);
	}

	# ���ե�����Ĵ��
	logFileAdjust(-1, $HislandNextID);

#	readIslandsFile(-3);
	# �Ϸ��ǡ������Ǽ���Ĵ��
	islandFileAdjust(-1, $HislandNextID);

	# ����������ֹ�����
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$islandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland($mode);
	my($island) = $Hislands[$HcurrentNumber];

	# �Ƽ���ͤ�����
	$island->{'name'}     = $HcurrentName;
	$island->{'owner'}    = $HcurrentOwnerName;
	$island->{'birthday'} = $HislandTurn;
	$island->{'id'}       = $HislandNextID;
	$HislandNextID ++;
	$HislandNextID = 1 if($HislandNextID > 100);
	$island->{'absent'}   = $HjoinGiveupTurn;
	$island->{'comment'}  = $HjoinComment;
	$island->{'password'} = encode($HinputPassword);
	$island->{'comflag'}  = $HcomflagUse % 2;
	# �͸�����¾����
	estimate($HcurrentNumber);

	if($HarmisticeTurn) {
		my $ally = $Hally[$campNum];
		$ally->{'score'} += $island->{$HrankKind} if(!$island->{'predelete'});
		foreach (@{$ally->{'memberId'}}) {
			push(@{$Hislands[$HidToNumber{$_}]->{'amity'}}, $island->{'id'});
			push(@{$island->{'amity'}}, $_);
		}
		push(@{$ally->{'memberId'}}, $island->{'id'});
		$ally->{'number'}++;
		push(@{$island->{'allyId'}}, $ally->{'id'});
	}

	# �ǡ����񤭽Ф�
	$HidToNumber{$island->{'id'}} = $HcurrentNumber;
	islandSort($HrankKind, 1);
	if($HarmisticeTurn) {
		allyOccupy();
		allySort();
	}
	writeIslandsFile($island->{'id'});
	$HcurrentNumber = $HidToNumber{$island->{'id'}};
	$HcurrentName = islandName($island);
	logDiscover($HcurrentName, $HcurrentOwnerName); # ��

	$HcurrentID = $HislandNextID - 1;
	$HmainMode = 'owner';
	$HjavaMode = 'java';

	return 1 if($mode);
	# COOKIE����
	cookieOutput();

	# ����
	unlock();

	# ȯ������
	tempHeader();
	tempNewIslandHead($HcurrentName); # ȯ�����ޤ���!!
	islandInfo(); # ��ξ���
	islandMap(1); # ����Ͽޡ�owner�⡼��
}

# ������Ǥ⾯�ʤ�����̤��ǲ��̤οر�
sub selectMinCamp {
	my($i, $num) = (0, 0);
	for ($i = 1; $i < $HallyNumber; $i++) {
		if ($Hally[$i]->{'number'} <= $Hally[$num]->{'number'}) {
			$num = $i;
		}
	}
	return $num;
}

# ������("��פ����/�رĤο�+1"�ޤ�)
sub selectRandomCamp {
	return 0 if(!$HallyNumber);
	my($i, $j, $ave, $iave, @array, $len);
	# �����ر�����κ���
	$ave = $HmaxIsland / $HallyNumber;
	$iave = int($ave);
	if ($iave != $ave) { $iave++; };
	for ($i = 0; $i < $HallyNumber; $i++) {
		for ($j = $Hally[$i]->{'number'}; $j < $iave; $j++) {
			push(@array, $i);
			$len++;
		}
	}
	return  $array[int(rand($len))];
}

# �رĤ�����롼����(����ˤ���Ѳ�)
sub selectCamp {
	if ($HcampSelectRule == 0) {
		return selectMinCamp();
	} elsif ($HcampSelectRule == 1) {
		return selectRandomCamp();
	} else {
		# �ɤ��Ǥ��ɤ�������
		return selectRandomCamp();
	}
}
#---------------------------------------------------------------------
#	�ե�����Ĵ��
#---------------------------------------------------------------------
sub logFileAdjust {
	my($oldId, $newId) = @_;

	for($i = 0; $i < $HlogMax;  $i++) {
		open(LIN, "${HdirName}/$i$HlogData");
		open(LOUT, ">${HdirName}/${i}tmp$HlogData");
		my($line, $m, $turn, $id1, $id2, $id3, $message);
		while($line = <LIN>) {
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-]*),(.*)$/;
			($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
			next if($m eq '');
			$id1 = 0 if($id1 == $newId);
			$id2 = 0 if($id2 == $newId);
			$id3 = 0 if($id3 == $newId);
			$id1 = $newId if($id1 == $oldId);
			$id2 = $newId if($id2 == $oldId);
			$id3 = $newId if($id3 == $oldId);
			print LOUT "$m,$turn,$id1,$id2,$id3,$message\n";
		}
		close(LIN);
		close(LOUT);
		unlink("${HdirName}/$i$HlogData");
		rename("${HdirName}/${i}tmp$HlogData", "${HdirName}/$i$HlogData");
	}
}

sub islandFileAdjust {
	my($oldId, $newId) = @_;

	foreach $i (0..$islandNumber) {
		my($tIsland) = $Hislands[$i];
		my($tId) = $tIsland->{'id'};
		my($tLand)	  = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tMap) = $tIsland->{'map'};
		my($x, $y);
		my $writeflag = 0;
		foreach $y (@{$tMap->{'y'}}) {
			foreach $x (@{$tMap->{'x'}}) {
				if ($tLand->[$x][$y] == $HlandNavy) {
					# �����ʤ�
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($tLandValue->[$x][$y]);
					if($nId == $newId){
						$Hislands[$i]->{'landValue'}->[$x][$y] = navyPack(0, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp);
						$writeflag = 1;
					}
					if($nId == $oldId){
						$Hislands[$i]->{'landValue'}->[$x][$y] = navyPack($newId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp);
						$writeflag = 1;
					}
				}
			}
		}

		my($lbbs, $line, $j);
		$lbbs = $tIsland->{'lbbs'};
		for($j = 0; $j < $HlbbsMax; $j++) {
			$line = $lbbs->[$j];
			if($line =~ /([0-9]*)\<(.*)\<(.*)\>(.*)\>(.*)$/) {
				my($kind, $message, $HlbbsName, $HlbbsMessage) = ($1, $3, $4, $5);
				my($sName, $sID) = split(/,/, $2);
				if($sID == $newId) {
					$Hislands[$i]->{'lbbs'}->[$j] = "$kind<$sName<$message>$HlbbsName>$HlbbsMessage";
					$writeflag = 1;
				}
				if($sID == $oldId) {
					$Hislands[$i]->{'lbbs'}->[$j] = "$kind<$sName,$newId<$message>$HlbbsName>$HlbbsMessage";
					$writeflag = 1;
				}
			}
		}
		# �ǡ����񤭽Ф�
		writeIsland($tIsland, $tId, 0) if($writeflag);
	}
}

#---------------------------------------------------------------------
# ����������������
#---------------------------------------------------------------------
sub makeNewIsland {
	my($mode) = @_;
	# �����ɸ
	my($wmap, $map);
	if($HoceanMode) {
		if(($HoceanSelect || $HmainMode eq 'bfield' || $HmainMode eq 'isetup') &&
			!$HmapRandom && $HoceanMapX ne '' && $HoceanMapY ne '' && !$HoceanMap[$HoceanMapX][$HoceanMapY]) {
			$wmap = { 'x' => $HoceanMapX, 'y' => $HoceanMapY };
		} else {
			$wmap = randomIslandMap(); # ��κ�ɸ�����
		}
		unless(defined $wmap) {
			unlock();
			tempHeader();
			tempNewIslandFull();
			return 0;
		}
	} else {
		$wmap = { 'x' => 0, 'y' => 0 };
	}
	# �ޥå�����
	my @x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
	my @y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
	$map = { 'x' => \@x, 'y' => \@y };
	# �Ϸ�����
	my($land, $landValue) = makeNewLand($wmap, $map, $mode);

	# ������ޥ�ɤ�����
	my(@command, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$command[$i] = {
			'kind' => $HcomDoNothing,
			'target' => 0,
			'x' => 0,
			'y' => 0,
			'arg' => 0,
			'target2' => 0
		};
	}

	# ����Ǽ��Ĥ����
	my @lbbs = ();

	# �����������󥿡����å�
	my $n = @HnavyName;
	my(@navy) = ((0)x$n);

	# ��ĥ�ǡ������å�
	my(@ext) = ((0)x11); # 0��10
	# ��ĥ���֥ǡ������å�
	# ext�ξ����ե饰[0]�򥿡�����Ѥ��ơ��Ǹ���༣��[11],�󾩶�[12]���ɲá�
	my(@subExt) = ($HislandTurn, (0)x12); # 0��12

	# ŷ�������
	my(@weather) = (20,1000,60,0,0,0,0);
	for($i = 0; $i < 4; $i++) {
		 push(@weather,'2');
	}

	# ��ˤ����֤�
	return {
		'map'         => $map,
		'wmap'        => $wmap,
		'land'        => $land,
		'landValue'   => $landValue,
		'command'     => \@command,
		'lbbs'        => \@lbbs,
		'money'       => (!$HarmisticeTurn || !$HislandTurn ? $HinitialMoney : $HinitialMoney2),
		'food'        => (!$HarmisticeTurn || !$HislandTurn ? $HinitialFood : $HinitialFood2),
		'prize'       => '0,0,0,',
		'monsterkill' => 0,
		'monsterlive' => '0,0,0,0,0',
		'gain'        => 0,
		'sink'        => \@navy,
		'sinkself'    => \@navy,
		'subSink'     => \@navy,
		'subSinkself' => \@navy,
		'ext'         => \@ext,
		'subExt'      => \@subExt,
		'fight_id'    => 0,
		'rest'        => 0,
		'weather'     => \@weather,
	};
}

# (0,0)����(7, 7)�ޤǤο��������ŤĽФƤ���褦��
# (@rpx, @rpy)������
sub makeRandomEightArray {
	undef @rpx;
	undef @rpy;
	# �����
	@rpx = (0..7) x 8;
	foreach (0..7) {
		push(@rpy, ($_) x 8);
	}
	# ����åե�
	for ($i = 64; --$i; ) {
		my($j) = int(rand($i+1)); 
		next if($i == $j);
		@rpx[$i,$j] = @rpx[$j,$i];
		@rpy[$i,$j] = @rpy[$j,$i];
	}
}

# ����������Ϸ����������
sub makeNewLand {
	my($wmap, $map, $mode) = @_;
	# ���ܷ������
	my(@land, @landValue, $x, $y, $i);
	if($HoceanMode) {
		@land = @{$Hworld->{'land'}};
		@landValue = @{$Hworld->{'landValue'}};
	}
	# ���˽����
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$land[$x][$y] = $HlandSea;
			$landValue[$x][$y] = 0;
		}
	}
	return (\@land, \@landValue) if($mode);
	# �����4*4�˹���(ʿ��)������
	my($centerX) = $wmap->{'x'}*$HislandSizeX + int($HislandSizeX / 2) - 1;
	my($centerY) = $wmap->{'y'}*$HislandSizeY + int($HislandSizeY / 2) - 1;
	for($y = $centerY - 1; $y < $centerY + 3; $y++) {
		for($x = $centerX - 1; $x < $centerX + 3; $x++) {
			$land[$x][$y] = (!$HnewIslandSetting) ? $HlandWaste : $HlandPlains;
		}
	}
	my($count);
	if(!$HnewIslandSetting) {
		# 8*8�ϰ����Φ�Ϥ�����
		foreach $i (1..120) {
			# �������ɸ
			$x = random(8) + $centerX - 3;
			$y = random(8) + $centerY - 3;

			if(countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7){
				# �����Φ�Ϥ������硢�����ˤ���
				# �����Ϲ��Ϥˤ���
				# ���Ϥ�ʿ�Ϥˤ���
				if($land[$x][$y] == $HlandWaste) {
					$land[$x][$y] = $HlandPlains;
					$landValue[$x][$y] = 0;
				} else {
					if($landValue[$x][$y] == 1) {
						$land[$x][$y] = $HlandWaste;
						$landValue[$x][$y] = 0;
					} elsif($land[$x][$y] == $HlandSea) {
						$landValue[$x][$y] = 1;
					}
				}
			}
		}
	} else {
		# ʿ�Ϥ���
		makeRandomEightArray();
		$count = 0;
		$HcountLandArea -= 16;
		foreach $i (0..63) {
			last if($count >= $HcountLandArea);
			# �������ɸ
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# ���������Ǥ��ļ��Ϥ�Φ������С�ʿ�Ϥ���
			if(($land[$x][$y] == $HlandSea) && (countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7)) {
				$land[$x][$y] = $HlandPlains;
				$landValue[$x][$y] = 0;
				$count++;
			}
		}

		# ��������
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandSea);
			# �������ɸ
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# ���������Ǥ��ļ��Ϥ�Φ������С���������
			if(($land[$x][$y] == $HlandSea) && !$landValue[$x][$y] && (countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7)) {
				$landValue[$x][$y] = 1;
				$count++;
			}
		}

		# ���Ϥ���
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandWaste);
			# �������ɸ
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# ���������Ǥ�ʿ�Ϥʤ顢���Ϥ���
			if($land[$x][$y] == $HlandPlains) {
				$land[$x][$y] = $HlandWaste;
				$count++;
			}
		}
	}

	# Į����
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandTown);
		# �������ɸ
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# ������ʿ�Ϥʤ顢Į����
		if($land[$x][$y] == $HlandPlains) {
			$land[$x][$y] = $HlandTown;
			$landValue[$x][$y] = $HvalueLandTown; # �ǽ��500��
			$count++;
		}
	}

	# ������
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandForest);
		# �������ɸ
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# ������ʿ�Ϥʤ顢������
		if($land[$x][$y] == $HlandPlains) {
#			$land[$x][$y] = $HlandForest;
#			$landValue[$x][$y] = $HvalueLandForest; # �ǽ��500��
			# ʣ���Ϸ�(��)
			$land[$x][$y] = $HlandComplex;
			$landValue[$x][$y] = landPack(0, 2, 1, 0, 0); # �ǽ��100��
			$count++;
		}
	}

	# ������
#	makeRandomEightArray();
#	$count = 0;
#	foreach $i (0..63) {
#		last if($count >= $HcountLandMountain);
#		# �������ɸ
#		$x = $rpx[$i] + $centerX - 3;
#		$y = $rpy[$i] + $centerY - 3;
#
#		# ������ʿ�Ϥʤ顢������
#		if($land[$x][$y] == $HlandPlains) {
#			$land[$x][$y] = $HlandMountain;
#			$landValue[$x][$y] = $HvalueLandMountain; # �ǽ�Ϻη���ʤ�
#			$count++;
#		}
#	}

	# ��������
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandPort);
		# �������ɸ
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# �����������ʤ顢��������
		if(($land[$x][$y] == $HlandSea) && $landValue[$x][$y]) {
			$land[$x][$y] = $HlandNavy;
			$landValue[$x][$y] = navyPack($HislandNextID, 0, 0, 0, 0, 0, 0, 0, $HnavyHP[0]);
			$count++;
		}
	}

	if ($HuseBase) {
		# ���Ϥ���
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandBase);
			# �������ɸ
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# ������ʿ�Ϥʤ顢����
			if($land[$x][$y] == $HlandPlains) {
				$land[$x][$y] = $HlandBase;
				$landValue[$x][$y] = 0;
				$count++;
			}
		}
	}

	if($HoceanMode) {
		$Hworld->{'land'} = \@land;
		$Hworld->{'landValue'} = \@landValue;
	}
	return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
	# id����������
	readIsland
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# �ѥ���ɥ����å�
	if(checkSpecialPassword($HoldPassword)) {
		# �ü�ѥ����
		if($HcurrentName =~ /^��$/) {
			# �Ƕ�ν������������
			logPrintHtml();
			unlock();
			tempChange();
			return;
		} elsif($HcurrentName =~ /^̵��$/) {
			# �����⡼��
			deleteIsland(1);
			return;
		} elsif($HcurrentName =~ /^����$/) {
			# �����⡼��
			deleteIsland(0);
			return;
		} elsif(!checkMasterPassword($HoldPassword)) {
			# ����/���max�⡼��
			$island->{'money'} = $HmaximumMoney;
			$island->{'food'}  = $HmaximumFood;
			$flag = 1;
		}
	} elsif(!checkPassword($island,$HoldPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# ��̾�ѹ��ξ��	
		# ��̾�������������å�
		if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��|^����$/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadName();
			return;
		}

		# ̾���ν�ʣ�����å�
		if(nameToNumber($HcurrentName) != -1) {
			# ���Ǥ�ȯ������
			unlock();
			tempNewIslandAlready();
			return;
		}

		# ���
		unless(checkSpecialPassword($HoldPassword)) {
			if($island->{'money'} < $HcostChangeName) {
				# �⤬­��ʤ�
				unlock();
				tempChangeNoMoney();
				return;
			}
			$island->{'money'} -= $HcostChangeName;
		}

		# ̾�����ѹ�
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
		my $n = $HidToAllyNumber{$HcurrentID};
		if(defined $n) {
			$Hally[$n]->{'oName'} = $HcurrentName;
		}
	}

	if ($HcurrentOwnerName ne '') {
		# �����ʡ�̾�ѹ��ξ��
		# �����ʡ�̾�������������å�
		if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadOwnerName();
			return;
		}

		# ���
		unless(checkSpecialPassword($HoldPassword)) {
			if($island->{'money'} < $HcostChangeName) {
				# �⤬­��ʤ�
				unlock();
				tempChangeNoMoney();
				return;
			}
			$island->{'money'} -= $HcostChangeName;
		}

		# ̾�����ѹ�
		logChangeOwnerName($island->{'name'}, $HcurrentOwnerName);
		$island->{'owner'} = $HcurrentOwnerName;
		$flag = 1;
	}

	# password�ѹ��ξ��
	if($HinputPassword ne '') {
		# �ѥ���ɤ��ѹ�
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
		my $n = $HidToAllyNumber{$HcurrentID};
		if(defined $n) {
			$Hally[$n]->{'password'} = encode($HinputPassword);
		}
	}

	if($flag == 0) {
		# �ɤ�����ѹ�����Ƥ��ʤ�
		unlock();
		tempChangeNothing();
		return;
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);
	unlock();

	# �ѹ�����
	tempChange();
}

#----------------------------------------------------------------------
# ���������õ��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandTop {
	# ����
	unlock();

	# �����ͤ��������������õ���롩
	if ($HadminJoinOnly) {
		# �ޥ����ѥ���ɥ����å�
		unless (checkMasterPassword($HinputPassword)) {
			# password�ְ㤤
			tempWrongPassword();
			return;
		}
	}
	
	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='newIsland'>
$HPoliciesDisclaimers
<H1>������${AfterName}��õ��</H1>
END

	if(($HislandNumber - $HbfieldNumber < $HmaxIsland) && ($HmaxIsland <= 100) && (!$HarmisticeTurn || $HallyNumber)) {
		if($HoceanMode && $HoceanSelect) {
			readIslandsFile(0);
			printIslandMapMain(3);
		}
		out(<<END);
<FORM action="$HthisFile" name="JoinForm" method="POST">
END
		if($HoceanMode && $HoceanSelect) {
			out(<<END);
�����ɸ����ꤷ�Ʋ�����<BR>��ɸ��
<SELECT NAME="OCEANX">
END
			my($i);
			foreach $i (0..($HoceanSizeX-1)) {
				out("<OPTION VALUE=$i>$i\n");
			}
			out(<<END);
</SELECT>, <SELECT NAME="OCEANY">
END
			foreach $i (0..($HoceanSizeY-1)) {
				out("<OPTION VALUE=$i>$i\n");
			}
			out(<<END);
</SELECT>�ˡ�<INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>������<BR><BR>
END
		}
		if ($HarmisticeTurn && ($HcampSelectRule == 2) && $HallyNumber) {
			my $allyList;
			foreach (0..$#Hally) {
				next if ($Hally[$_]->{'number'} >= ($HmaxIsland / $HallyNumber));
				my $s = '';
				$s = ' SELECTED' if($_ == 0);
				$allyList .= "<OPTION VALUE=\"$_\"$s>$Hally[$_]->{'name'}\n";
			}
			out(<<END);
�ر�̾�����򤷤Ʋ�����<BR>
<SELECT NAME="CAMPNUMBER">
$allyList
<OPTION VALUE=\"-1\">�ɤ��Ǥ��ɤ�
</SELECT><BR>
END
		}
		
		$HjoinNewIslandButton = 'õ���˹Ԥ�' if(!$HjoinNewIslandButton);
		out(<<END);
�ɤ��̾����Ĥ���ͽ�ꡩ<small>(����${HlengthIslandName}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>${AfterName}<BR>
���ʤ���̾���ϡ�<small>(����${HlengthOwnerName}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32 class=f><BR>
<BR>
<INPUT TYPE="submit" VALUE="$HjoinNewIslandButton" NAME="NewIslandButton">
</FORM>
</DIV>
END
	} else {
	out(<<END);
		${AfterName}�ο���������Ǥ�������������Ͽ�Ǥ��ޤ���
</DIV>
END
	}
}

#----------------------------------------------------------------------
# ���̾���ȥѥ���ɤ��ѹ�
#----------------------------------------------------------------------
# �ᥤ��
sub renameIslandMain {
	# ����
	unlock();

	my($str);
	$str = '<BR>���ޤ����ֿرĥѥ���ɡפǤϡ��ѥ���ɤ��ѹ��ϤǤ��ޤ���' if($HarmisticeTurn);
	$str = '<BR>���ر��¤���ˤʤä���ؤϳƥ���������ꤵ�줿�رĥѥ���ɤ�����ޤ���<BR>���ѥ�����ѹ���ɬ�פʻ��ϡ������Ԥؤ�Ϣ��������' if($HarmisticeTurn && !$HpassChangeOK);
	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='changeInfo'>
<H1>${AfterName}��̾���ȥѥ���ɤ��ѹ�</H1>
<table border=0 width=50%><tr><td class="M"><P>
<span class='attention'>(���)</span><BR>
��̾�����ѹ��ˤ�${HtagMoney_}$HcostChangeName${HunitMoney}${H_tagMoney}������ޤ���$str
</P>
<FORM action="$HthisFile" method="POST">
�ɤ�${AfterName}�Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<small>(����${HlengthIslandName}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>${AfterName}<BR>
���ʤ���̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<small>(����${HlengthOwnerName}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32 class=f><BR>

<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM>
</td></tr></table></DIV>
END
}

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
	my($name) = @_;

	# ���礫��õ��
	my($i);
	foreach $i (0..$islandNumber) {
		if($Hislands[$i]->{'name'} eq $name) {
			return $i;
		}
	}

	# ���Ĥ���ʤ��ä����
	return -1;
}

# Ʊ����̾������ID������
sub aNameToId {
	my($name) = @_;

	# ���礫��õ��
	my($i);
	for($i = 0; $i < $HallyNumber; $i++) {
		if($Hally[$i]->{'name'} eq $name) {
			return $Hally[$i]->{'id'};
		}
	}

	# ���Ĥ���ʤ��ä����
	return -1;
}

# Ʊ���Υޡ�������ID������
sub aMarkToId {
	my($mark) = @_;

	# ���礫��õ��
	my($i);
	for($i = 0; $i < $HallyNumber; $i++) {
		if($Hally[$i]->{'mark'} eq $mark) {
			return $Hally[$i]->{'id'};
		}
	}

	# ���Ĥ���ʤ��ä����
	return -1;
}

#----------------------------------------------------------------------
# Ʊ���ο��������⡼��
#----------------------------------------------------------------------
# �������ѹ��ᥤ��
sub makeAllyMain {

	my $adminMode = 0;
	# �ѥ���ɥ����å�
	if(checkSpecialPassword($HoldPassword)) {
		$adminMode = 1;
		if($HallyID > 200) {
			my $max = $HallyID;
			if($HallyNumber) {
				foreach (0..$#Hally) {
					$max = $Hally[$_]->{'id'} + 1 if($max <= $Hally[$_]->{'id'});
				}
			}
			$HcurrentID = $max;
		} elsif(defined $HcurrentAnumber) {
			my $ally = $Hally[$HcurrentAnumber];
			$HcurrentID = $ally->{'id'};
			my $wflag = 0;
			if($HallyID eq '0') {
				$wflag = 1;
				my $max = 200;
				if($HallyNumber) {
					foreach (0..$#Hally) {
						$max = $Hally[$_]->{'id'} + 1 if($max <= $Hally[$_]->{'id'});
					}
				}
				$HcurrentID = $max;
				$ally->{'id'} = $HcurrentID;
				$ally->{'oName'} = "";
			} elsif(($ally->{'name'} ne $HallyName) || ($ally->{'mark'} ne $HallyMark) || ($ally->{'color'} ne "#${HallyColor}")) {
				$wflag = 1;
				if((defined $HidToNumber{$HallyID}) && ($HcurrentID != $HallyID)) {
					$ally->{'id'} = $HallyID;
					$ally->{'oName'} = $Hislands[$HidToNumber{$HallyID}]->{'name'};
				}
				$ally->{'name'} = $HallyName;
				$ally->{'mark'} = $HallyMark;
				$ally->{'color'} = "#${HallyColor}";
			} elsif($HcurrentID != $HallyID) {
				$wflag = 1;
				$ally->{'id'} = $HallyID;
				$ally->{'oName'} = $Hislands[$HidToNumber{$HallyID}]->{'name'};
			}
			if($wflag) {
				# Ʊ���ǡ����ν񤭹���
				writeAllyFile() if($HallyUse || $HarmisticeTurn);
				$HislandList = getIslandList($HcurrentID, 0);

				# ����
				unlock();
				# �ȥåפ�
				topPageMain();
				return;
			}
		} else {
			unlock();
			out("${HtagBig_}����or�ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack");
			return;
		}
	}

	# Ʊ��̾�����뤫�����å�
	if($HallyName eq '') {
		unlock();
		$AfterName = 'Ʊ��';
		tempNewIslandNoName();
		return;
	}

	# Ʊ��̾�������������å�
	if($HallyName =~ /[,\?\(\)\<\>\$]|^̵��|^����$/) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempNewIslandBadOwnerName();
		return;
	}
	# ̾���ν�ʣ�����å�
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	if(!($adminMode && ($HallyID ne '') && ($HallyID < 200)) &&
		((nameToNumber($HallyName) != -1) ||
		((aNameToId($HallyName) != -1) && (aNameToId($HallyName) != $HcurrentID)))) {
		# ���Ǥ˷�������
		unlock();
		tempNewAllyAlready();
		return;
	}

	# �ޡ����ν�ʣ�����å�
	if(!($adminMode && ($HallyID ne '') && ($HallyID < 200)) &&
		((aMarkToId($HallyMark) != -1) && (aMarkToId($HallyMark) != $HcurrentID))) {
		# ���Ǥ˻��Ѥ���
		unlock();
		tempMarkAllyAlready();
		return;
	}

	# password��Ƚ��
	my($island) = $Hislands[$HcurrentNumber];
	if(!$adminMode && !checkPassword($island,$HinputPassword)) {
		unlock();
		tempWrongPassword();
		return;
	}
	if(!$adminMode && $island->{'money'} < $HcostMakeAlly) {
		unlock();
		tempNoMoney();
		return;
	}
	my $n = $HidToAllyNumber{$HcurrentID};
	if(defined $n) {
		if($adminMode && ($HallyID ne '') && ($HallyID < 200)) {
			my $allyMember = $Hally[$n]->{'memberId'};
			my $aIsland = $Hislands[$HidToNumber{$HallyID}];
			my $flag = 0;
			foreach (@$allyMember) {
				if($_ == $HallyID) {
					$flag = 1;
					last;
				}
			}
			if(!$flag) {
				$flag = 2 if(@{$aIsland->{'allyId'}}[0] eq '');
			}
			if(!$flag) {
				unlock();
				out("${HtagBig_}�ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack");
				return;
			}
			$Hally[$n]->{'id'}       = $HallyID;
			$Hally[$n]->{'oName'}    = $aIsland->{'name'};
			if($flag == 2) {
				$Hally[$n]->{'password'} = $aIsland->{'password'};
				$Hally[$n]->{'score'}    = $aIsland->{$HrankKind} if(!$aIsland->{'predelete'});
				$Hally[$n]->{'number'}++;
				push(@{$Hally[$n]->{'memberId'}}, $aIsland->{'id'});
				push(@{$aIsland->{'allyId'}}, $aIsland->{'id'});
			}
		} else {
			# ���Ǥ˷������ߤʤ��ѹ�
			logChangeAlly($Hally[$n]->{'name'}, $HallyName) if(!$adminMode && ($Hally[$n]->{'name'} ne $HallyName));
		}
	} else {
		# ¾�����Ʊ�������äƤ�����ϡ������Ǥ��ʤ�
		my $flag = 0;
		for ($i = 0; $i < $HallyNumber; $i++) {
			my $allyMember = $Hally[$i]->{'memberId'};
			foreach (@$allyMember) {
				if($_ == $HcurrentID) {
					$flag = 1;
					last;
				}
			}
			last if($flag);
		}
		if($flag) {
			unlock();
			tempOtherAlready();
			return;
		}

		# ����
		$n = $HallyNumber;
		$Hally[$n]->{'id'}       = $HcurrentID;
		my @memberId = ();
	    if($HallyID < 200) {
			$Hally[$n]->{'oName'}    = $island->{'name'};
			$Hally[$n]->{'password'} = $island->{'password'};
			$Hally[$n]->{'number'}   = 1;
			@memberId = ($HcurrentID);
			$Hally[$n]->{'score'}    = $island->{$HrankKind} if(!$island->{'predelete'});
		} else {
			$Hally[$n]->{'oName'}    = '';
			$Hally[$n]->{'password'} = encode($HinputPassword);
			$Hally[$n]->{'number'}   = 0;
			$Hally[$n]->{'score'}    = 0;
		}
		$Hally[$n]->{'Takayan'}  = makeRandomString();
		$Hally[$n]->{'occupation'} = 0;
		$Hally[$n]->{'memberId'} = \@memberId;
		$island->{'allyId'} =  \@memberId;
		my @ext = (0, 0, 0, 0, 0);
		$Hally[$n]->{'ext'}      = \@ext;
		$HidToAllyNumber{$HcurrentID} = $n;
		$HallyNumber++;
		logMakeAlly($HallyName, islandName($island)) if(!$adminMode); # ��
	}

	# Ʊ���γƼ���ͤ�����
	$Hally[$n]->{'name'}     = $HallyName;
	$Hally[$n]->{'mark'}     = $HallyMark;
	$Hally[$n]->{'color'}    = "#${HallyColor}";
	
	# ���Ѥ򤤤�����
	$island->{'money'} -= $HcostMakeAlly if(!$adminMode);
	# �ǡ����񤭽Ф�
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# ����
	unlock();
	# �ȥåפ�
	topPageMain();
}

# ���Ǥˤ���̾����Ʊ����������
sub tempNewAllyAlready {
	out(<<END);
${HtagBig_}����Ʊ���ʤ餹�Ǥ˷�������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ��Υޡ�����Ʊ����������
sub tempMarkAllyAlready {
	out(<<END);
${HtagBig_}���Υޡ����Ϥ��Ǥ˻��Ѥ���Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �̤�Ʊ����������Ƥ���
sub tempLeaderAlready {
	out(<<END);
${HtagBig_}����ϡ���ʬ��Ʊ���ʳ��ˤϲ����Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# �̤�Ʊ���˲������Ƥ���
sub tempOtherAlready {
	out(<<END);
${HtagBig_}�ҤȤĤ�Ʊ���ˤ��������Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ���­�ꤺ
sub tempNoMoney {
	out(<<END);
${HtagBig_}�����­�Ǥ�(/_<��)${H_tagBig}$HtempBack
END
}
# ��
sub deleteAllyMain {

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my $n = $HidToAllyNumber{$HcurrentID};
	my $adminMode = 0;
	# �ѥ���ɥ����å�
	if(checkSpecialPassword($HoldPassword)) {
		$n = $HcurrentAnumber;
		$HcurrentID = $Hally[$n]->{'id'};
		$adminMode = 1;
	} else {
		# password��Ƚ��
		if(!checkPassword($island,$HinputPassword)) {
			unlock();
			tempWrongPassword();
			return;
		}
		if(!checkPassword($Hally[$n],$HinputPassword)) {
			unlock();
			tempWrongPassword();
			return;
		}
		# ǰ�Τ���ID������å�
		if($Hally[$n]->{'id'} != $HcurrentID) {
			unlock();
			tempWrongAlly();
			return;
		}
	}
	my $allyMember = $Hally[$n]->{'memberId'};
	if($adminMode && $HarmisticeTurn && ((@{$allyMember}[0] ne '') || !(defined $n))){
		unlock();
		out("${HtagBig_}����Ǥ��ޤ���${H_tagBig}$HtempBack");
		return;
	}
	foreach (@$allyMember) {
		my($island, $aId, @newId);
		$island = $Hislands[$HidToNumber{$_}];
		@newId = ();
		foreach $aId (@{$island->{'allyId'}}) {
			if($aId != $HcurrentID) {
				push(@newId, $aId);
			}
		}
		$island->{'allyId'} = \@newId;
	}
	logDeleteAlly($Hally[$n]->{'name'}) if(!$adminMode);
	$Hally[$n]->{'dead'} = 1;
	$HidToAllyNumber{$HcurrentID} = undef;
	$HallyNumber--;
	# �ǡ����񤭽Ф�
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# ����
	unlock();
	# �ȥåפ�
	topPageMain();
}

# ID�����å��ˤҤä�����
sub tempWrongAlly {
	out(<<END);
${HtagBig_}���ʤ�������ǤϤʤ��Ȼפ���${H_tagBig}$HtempBack
END
}

# ������æ��
sub joinAllyMain {

	# password��Ƚ��
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	if(!checkPassword($island,$HinputPassword)) {
		unlock();
		tempWrongPassword();
		return;
	}
	if(defined $HidToAllyNumber{$HcurrentID}) {
		unlock();
		tempLeaderAlready();
		return;
	}
	my $ally = $Hally[$HcurrentAnumber];
	if($HallyJoinOne && ($island->{'allyId'}[0] ne '') && ($island->{'allyId'}[0] != $ally->{'id'})) {
		unlock();
		tempOtherAlready();
		return;
	}
	if(!$ally->{'vkind'}) {
		foreach(@{$ally->{'vetoId'}}) {
			if($island->{'id'} == $_) {
				unlock();
				logAllyVeto();
				return;
			}
		}
	} else {
		my $vflag = 1;
		foreach(@{$ally->{'vetoId'}}) {
			if($island->{'id'} == $_) {
				$vflag = 0;
				break;
			}
		}
		if($vflag) {
			unlock();
			logAllyVeto();
			return;
		}
	}
	my $allyMember = $ally->{'memberId'};
	my @newAllyMember = ();
	my $flag = 0;
	foreach (@$allyMember) {
		if(!(defined $HidToNumber{$_})) {
		} elsif($_ == $HcurrentID) {
			$flag = 1;
		} else {
			push(@newAllyMember, $_);
		}
	}
	my $allyNum = @newAllyMember;
	if($flag) {
		logAllyEnd(islandName($island), $ally->{'name'});
		my @newAlly = ();
		foreach (@{$island->{'allyId'}}) {
			if($_ != $ally->{'id'}) {
				push(@newAlly, $_);
			}
		}
		$island->{'allyId'} = \@newAlly;
		$ally->{'score'} -= $island->{$HrankKind} if(!$island->{'predelete'});
		$ally->{'number'}--;
	} else {
		if(!$HallyMax || $allyNum < $HallyMax) {
			logAlly(islandName($island), $ally->{'name'});
			push(@newAllyMember, $HcurrentID);
			push(@{$island->{'allyId'}}, $ally->{'id'});
			$ally->{'score'} += $island->{$HrankKind} if(!$island->{'predelete'});
			$ally->{'number'}++;
		} else {
			# ����
			unlock();
			logAllyMaxOver();
			exit(0);
		}
	}
	$island->{'money'} -= $HcomCost[$HcomAlly];
	$ally->{'memberId'} = \@newAllyMember;
	# �ǡ����񤭽Ф�
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# ����
	unlock();
	# �ȥåפ�
	topPageMain();
}

# ����
sub logMakeAlly {
	my($name, $owner) = @_;
	logHistory("Ʊ����${HtagName_}${name}${H_tagName}�٤�${HtagName_}${owner}${H_tagName}�ˤ�ä�${HtagNumber_}����${H_tagNumber}����롣");
}

# �ѹ�
sub logChangeAlly {
	my($oldname, $newname) = @_;
	logHistory("Ʊ����${HtagName_}${oldname}${H_tagName}�פ���${HtagName_}${newname}${H_tagName}�٤�̾���ѹ���");
}

# ��
sub logDeleteAlly {
	my($name) = @_;
	logHistory("Ʊ����${HtagName_}${name}${H_tagName}�٤�${HtagDisaster_}�򻶡�${H_tagDisaster}");
}

# ����
sub logAlly {
	my($name, $allyName) = @_;
	logHistory("${HtagName_}${name}${H_tagName}����${HtagName_}${allyName}${H_tagName}�٤�${HtagNumber_}����${H_tagNumber}��");
}

# æ��
sub logAllyEnd {
	my($name, $allyName) = @_;
	logHistory("${HtagName_}${name}${H_tagName}����${HtagName_}${allyName}${H_tagName}�٤���${HtagDisaster_}æ�ࡪ${H_tagDisaster}");
}

# Ʊ��������ǽ��������С�
sub logAllyMaxOver {
	out(<<END);
${HtagBig_}�����������˴�����ޤ�����(Ʊ��������ǽ${AfterName}�������С�)${H_tagBig}$HtempBack
END
}

# Ʊ����������
sub logAllyVeto {
	out(<<END);
${HtagBig_}�����������˴�����ޤ�����(���ݸ�ȯư)${H_tagBig}$HtempBack
END
}
#----------------------------------------------------------------------
# Ʊ���η������ѹ����򻶡�������æ��
#----------------------------------------------------------------------
# �������ѹ����򻶡�������æ��
sub newAllyTop {

	my $adminMode = 0;
	my $HtempBack2 = $HtempBack;
	# �ѥ���ɥ����å�
	if(checkSpecialPassword($HdefaultPassword)) {
		$adminMode = 1;
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		$HtempBack2 = "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}";
	} elsif(!$HallyUse) {
		require('./hako-top.cgi');
		topPageMain();
	}
	# ����
	unlock();
	my($jsIslandList, $name, $id, $i);
	foreach $i (0..$islandNumber) {
		$name = $Hislands[$i]->{'name'};
		$name =~ s/'/\\'/g;
		$id = $Hislands[$i]->{'id'};
		$jsIslandList .= "island[$id] = '$name'\;\n";
	}
	my($allyname, $markList, @colorList, @allycolor, $allyList, 
		$jsAllyList, $jsAllyIdList, $jsAllyMarkList, $jsAllyColorList);
	my($defaultMark, $defaultAllyId);
	my $n = $HidToAllyNumber{$defaultID};
	if($n eq '') {
		$allyname = '';
		$defaultMark = $Hally[0];
		$defaultAllyId= '';
	} else {
		$allyname = $Hally[$n]->{'name'};
		$allyname =~ s/'/\\'/g;
		$defaultMark = $Hally[$n]->{'mark'};
		$defaultAllyId = $Hally[$n]->{'id'};
	}
	foreach (0..$#HallyMark) {
		my $s = '';
		$s = ' SELECTED' if($HallyMark[$_] eq $defaultMark);
		$markList .= "<OPTION VALUE=\"$HallyMark[$_]\"$s>$HallyMark[$_]\n"
	}
	foreach $i (1..6) {
		if($n eq '') {
			$allycolor[$i] = 0;
		} else {
			$allycolor[$i] = substr($Hally[$n]->{'color'}, $i, 1);
		}
		foreach (0..9,A..F) {
			my $s = '';
			$s = ' SELECTED' if($_ eq $allycolor[$i]);
			$colorList[$i] .= "<OPTION VALUE=\"$_\"$s>$_\n"
		}
	}
	my $max = 201;
	if($HallyNumber) {
		$jsAllyList = "ally = [";
		$jsAllyIdList = "allyID = [";
		$jsAllyMarkList = "allyMark = [";
		$jsAllyColorList = "allyColor = [";
		foreach (0..$#Hally) {
			my $s = '';
			$s = ' SELECTED' if($Hally[$_]->{'id'} == $defaultAllyId);
			$allyList .= "<OPTION VALUE=\"$_\"$s>$Hally[$_]->{'name'}\n";
			$jsAllyList .= "'$Hally[$_]->{'name'}'";
			$jsAllyIdList .= "$Hally[$_]->{'id'}";
			$jsAllyMarkList .= "'$Hally[$_]->{'mark'}'";
			$jsAllyColorList .= "[";
			foreach $i (1..6) {
				$jsAllyColorList .= '\'' . substr($Hally[$_]->{'color'}, $i, 1) . '\'';
				$jsAllyColorList .= ',' if($i < 6);
			}
			$jsAllyColorList .= "]";
			if($_ < $#Hally) {
				$jsAllyList .= ",\n";
				$jsAllyIdList .= ",\n";
				$jsAllyMarkList .= ",\n";
				$jsAllyColorList .= ",\n";
			}
			$max = $Hally[$_]->{'id'} + 1 if($max <= $Hally[$_]->{'id'});
		}
		$jsAllyList .= "];\n";
		$jsAllyIdList .= "];\n";
		$jsAllyMarkList .= "];\n";
		$jsAllyColorList .= "];\n";
	}
	my $str1 = $adminMode ? '(���ƥʥ�)' : $HallyJoinComUse ? '' : '��������æ��';
	my $str2 = $adminMode ? '' : 'onChange=colorPack() onClick=colorPack()';
	my $makeCost = $HcostMakeAlly ? "${HcostMakeAlly}${HunitMoney}" : '̵��';
	my $keepCost = $HcostKeepAlly ? "${HcostKeepAlly}${HunitMoney}" : '̵��';
	my $joinCost = $HcomCost[$HcomAlly] ? "${$HcomCost[$HcomAlly]}${HunitMoney}" : '̵��';
	my $joinStr = $HallyJoinComUse ? '' : "������æ��κݤ����Ѥϡ�${HtagMoney_}$joinCost${H_tagMoney}�Ǥ���<BR>";
	my $str3 = $adminMode ? "�ü�ѥ���ɤϡ���ɬ�ܡ�<BR>
<INPUT TYPE=\"password\" NAME=\"OLDPASS\" VALUE=\"$HdefaultPassword\" SIZE=32 MAXLENGTH=32 class=f><BR>Ʊ��" : "<span class='attention'>(���)</span><BR>
Ʊ���η������ѹ������Ѥϡ�${HtagMoney_}${makeCost}${H_tagMoney}�Ǥ���<BR>
�ޤ����西����ɬ�פȤ����ݻ����${HtagMoney_}$keepCost${H_tagMoney}�Ǥ���<BR>
�ʰݻ����Ʊ���˽�°����${AfterName}�Ƕ�������ô���뤳�Ȥˤʤ�ޤ���<BR>
$joinStr
</P>
���ʤ�����ϡ���ɬ�ܡ�<BR>
<SELECT NAME=\"ISLANDID\" $str2>
$HislandList
</SELECT><BR>���ʤ�";

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='changeInfo'>
<H1>Ʊ���η������ѹ�����${str1}</H1>
<table border=0 width=50%><tr><td class="M"><P>
<FORM name="AcForm" action="$HthisFile" method="POST">
$str3
�Υѥ���ɤϡ���ɬ�ܡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f>
END
	
	if($HallyNumber) {
		my $str4 = $adminMode ? '���������ѹ�' : $HallyJoinComUse ? '' : '��������æ��';
		my $str5 = ($adminMode || $HallyJoinComUse) ? '' : '<INPUT TYPE="submit" VALUE="������æ��" NAME="JoinAllyButton">';
		out(<<END);
<BR>
<BR><B><FONT SIZE=4>�β�${str4}��</FONT></B>
<BR>�ɤ�Ʊ���Ǥ�����<BR>
<SELECT NAME="ALLYNUMBER" onChange=allyPack() onClick=allyPack()>
$allyList
</SELECT>
<BR>
<INPUT TYPE="submit" VALUE="��" NAME="DeleteAllyButton">
$str5
<BR>
END
	}

	my $str7 = $adminMode ? "��������ѹ�(��Υ�˥塼��Ʊ�������򤷤Ƥ�����̾����⤷����������)<BR> or Ʊ���ο�������(��Υ�˥塼��̵��)<BR><SELECT NAME=\"ALLYID\"><OPTION VALUE=\"$max\">��������<OPTION VALUE=\"0\">������\n$HislandList</SELECT><BR>" : '<BR><B><FONT SIZE=4>�η������ѹ���</FONT></B><BR>';
	out(<<END);
<BR>
$str7
Ʊ����̾�����ѹ���<small>(����${HlengthAllyName}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="ALLYNAME" VALUE="$allyname" SIZE=32 MAXLENGTH=32><BR>
�ޡ������ѹ���<BR>
<SELECT NAME="MARK" onChange=colorPack() onClick=colorPack()>
$markList
</SELECT>
<ilayer name="PARENT_CTBL" width="100%" height="100%">
   <layer name="CTBL" width="200"></layer>
   <span id="CTBL"></span>
</ilayer>
<BR>
�ޡ����ο������ɡ��ѹ���<BR><TABLE BORDER=0><TR>
<TD align='center'>RED</TD>
<TD align='center'>GREEN</TD>
<TD align='center'>BLUE</TD>
</TR><TR>
<TD><SELECT NAME="COLOR1" onChange=colorPack() onClick=colorPack()>
$colorList[1]</SELECT><SELECT NAME="COLOR2" onChange=colorPack() onClick=colorPack()>
$colorList[2]</SELECT></TD>
<TD><SELECT NAME="COLOR3" onChange=colorPack() onClick=colorPack()>
$colorList[3]</SELECT><SELECT NAME="COLOR4" onChange=colorPack() onClick=colorPack()>
$colorList[4]</SELECT></TD>
<TD><SELECT NAME="COLOR5" onChange=colorPack() onClick=colorPack()>
$colorList[5]</SELECT><SELECT NAME="COLOR6" onChange=colorPack() onClick=colorPack()>
$colorList[6]</SELECT></TD>
</TR></TABLE>
<INPUT TYPE="submit" VALUE="����(�ѹ�)" NAME="NewAllyButton">
<SCRIPT language="JavaScript">
<!--
END
	if(!$adminMode) {
		out(<<END);
function colorPack() {
	var island = new Array(128);
$jsIslandList
	a = document.AcForm.COLOR1.value;
	b = document.AcForm.COLOR2.value;
	c = document.AcForm.COLOR3.value;
	d = document.AcForm.COLOR4.value;
	e = document.AcForm.COLOR5.value;
	f = document.AcForm.COLOR6.value;
	mark = document.AcForm.MARK.value;
	number = document.AcForm.ISLANDID.value;

	str = "#" + a + b + c + d + e + f;
//	document.AcForm.AcColorValue.value = str;
	str = 'ɽ������ץ롧��<B><span class="number"><FONT color="' + str +'">' + mark + '</FONT></B>'
	  + island[number] + '${AfterName}</span>��';
	
	if(document.getElementById){
		document.getElementById("CTBL").innerHTML = str;
	} else if(document.all){
		el = document.all("CTBL");
		el.innerHTML = str;
	} else if(document.layers) {
		lay = document.layers["PARENT_CTBL"].document.layers["CTBL"];
		lay.document.open();
		lay.document.write(str);
		lay.document.close(); 
	}

	return true;
}
function allyPack() {
$jsAllyList
$jsAllyMarkList
$jsAllyColorList
	document.AcForm.ALLYNAME.value = ally[document.AcForm.ALLYNUMBER.value];
	document.AcForm.MARK.value     = allyMark[document.AcForm.ALLYNUMBER.value];
	document.AcForm.COLOR1.value   = allyColor[document.AcForm.ALLYNUMBER.value][0];
	document.AcForm.COLOR2.value   = allyColor[document.AcForm.ALLYNUMBER.value][1];
	document.AcForm.COLOR3.value   = allyColor[document.AcForm.ALLYNUMBER.value][2];
	document.AcForm.COLOR4.value   = allyColor[document.AcForm.ALLYNUMBER.value][3];
	document.AcForm.COLOR5.value   = allyColor[document.AcForm.ALLYNUMBER.value][4];
	document.AcForm.COLOR6.value   = allyColor[document.AcForm.ALLYNUMBER.value][5];
	colorPack();
	return true;
}
END
	} else {
		out(<<END);
function colorPack() {
	var island = new Array(128);
$jsIslandList
	a = document.AcForm.COLOR1.value;
	b = document.AcForm.COLOR2.value;
	c = document.AcForm.COLOR3.value;
	d = document.AcForm.COLOR4.value;
	e = document.AcForm.COLOR5.value;
	f = document.AcForm.COLOR6.value;
	mark = document.AcForm.MARK.value;
	name = document.AcForm.ALLYNAME.value;


	if(name == '') { name = '����פ�'; }
	str = "#" + a + b + c + d + e + f;
//	document.AcForm.AcColorValue.value = str;
	str = 'ɽ������ץ롧��<B><span class="number"><FONT color="' + str +'">' + mark + '</FONT></B>'
	  + name + '${AfterName}</span>��';
	
	if(document.getElementById){
		document.getElementById("CTBL").innerHTML = str;
	} else if(document.all){
		el = document.all("CTBL");
		el.innerHTML = str;
	} else if(document.layers) {
		lay = document.layers["PARENT_CTBL"].document.layers["CTBL"];
		lay.document.open();
		lay.document.write(str);
		lay.document.close(); 
	}

	return true;
}
function allyPack() {
$jsAllyList
$jsAllyIdList
$jsAllyMarkList
$jsAllyColorList
	document.AcForm.ALLYID.value   = allyID[document.AcForm.ALLYNUMBER.value];
	document.AcForm.ALLYNAME.value = ally[document.AcForm.ALLYNUMBER.value];
	document.AcForm.MARK.value     = allyMark[document.AcForm.ALLYNUMBER.value];
	document.AcForm.COLOR1.value   = allyColor[document.AcForm.ALLYNUMBER.value][0];
	document.AcForm.COLOR2.value   = allyColor[document.AcForm.ALLYNUMBER.value][1];
	document.AcForm.COLOR3.value   = allyColor[document.AcForm.ALLYNUMBER.value][2];
	document.AcForm.COLOR4.value   = allyColor[document.AcForm.ALLYNUMBER.value][3];
	document.AcForm.COLOR5.value   = allyColor[document.AcForm.ALLYNUMBER.value][4];
	document.AcForm.COLOR6.value   = allyColor[document.AcForm.ALLYNUMBER.value][5];
	colorPack();
	return true;
}
END
	}
	out(<<END);
colorPack();
//-->
</SCRIPT>
</FORM>
</td></tr></table></DIV>
END
}

# ���祳���ȥ⡼��
sub allyPactMain {
	my $ally = $Hally[$HidToAllyNumber{$HcurrentID}];
	if($HallyPactMode != 2) {
		# ����
		unlock();
		if($HallyPactMode && !checkPassword($ally, $HdefaultPassword)) {
			# password�ְ㤤
			tempWrongPassword();
			return;
		}
		# �ƥ�ץ졼�Ƚ���
		tempAllyPactPage();
	} else {
		# �ѥ���ɥ����å�
		if(checkPassword($ally, $HdefaultPassword)) {

			$HallyComment =~ s/[\x00-\x1f\,]//g;
			$ally->{'comment'} = htmlEscape($HallyComment);
			$ally->{'title'} = htmlEscape($HallyTitle);
			$ally->{'message'} = htmlEscape($HallyMessage, 1);
			$ally->{'vkind'} = $HvetoKind;
			$ally->{'vetoId'} = \@HvetoID;
			my(%vetoID);
			foreach(@HvetoID) {
				$vetoID{$_} = 1;
			}
			my @newAlly = ();
			if(!$HvetoKind) {
				foreach(@HvetoID) {
					my $vIsland = $Hislands[$HidToNumber{$_}];
					my($vId, @newVally);
					foreach $vId (@{$vIsland->{'allyId'}}) {
						push(@newVally, $vId) if($vId != $ally->{'id'});
					}
					$vIsland->{'allyId'} = \@newVally;
				}
				foreach (@{$ally->{'memberId'}}) {
					if(!$vetoID{$_}) {
						push(@newAlly, $_);
					}
				}
			} else {
				foreach(0..$islandNumber) {
					my $vIsland = $Hislands[$_];
					next if($vetoID{$vIsland->{'id'}} || ($vIsland->{'id'} == $ally->{'id'}));
					my($vId, @newVally);
					foreach $vId (@{$vIsland->{'allyId'}}) {
						push(@newVally, $vId) if($vId != $ally->{'id'});
					}
					$vIsland->{'allyId'} = \@newVally;
				}
				foreach (@{$ally->{'memberId'}}) {
					if($vetoID{$_} || ($_ == $ally->{'id'})) {
						push(@newAlly, $_);
					}
				}
			}
			$ally->{'memberId'} = \@newAlly;
			$ally->{'number'} = @newAlly;
			allyOccupy();
			# �ǡ����񤭽Ф�
			writeAllyFile();
			unlock();
			# �ѹ�����
			tempAllyPactOK($ally);
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# ���祳���ȥ⡼�ɤΥȥåץڡ���
sub tempAllyPactPage {
	my $ally = $Hally[$HidToAllyNumber{$HcurrentID}];
	my $allyMessage = $ally->{'message'};
	$allyMessage =~ s/<br>/\n/g;
	$allyMessage =~ s/&amp;/&/g;
	$allyMessage =~ s/&lt;/</g;
	$allyMessage =~ s/&gt;/>/g;
	$allyMessage =~ s/&quot;/\"/g; #"

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='changeInfo'>
<H1>�����ѹ���$ally->{'name'}��</H1>
<table border=0 width=80%><tr><td class="M">
<FORM action="$HthisFile" method="POST">
<B>����ѥ���ɤϡ�</B><BR>
<INPUT TYPE="password" NAME="Allypact" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f>
<INPUT TYPE="hidden"  NAME="ISLANDID" VALUE="$ally->{'id'}">
<INPUT TYPE="hidden"  NAME="AllypactMode" VALUE="$HallyPactMode">
<INPUT TYPE="submit" VALUE="����" NAME="AllypactButton">
END
	if($HallyPactMode) {
		out("<TABLE><TR><TD class='M'>");
		if($HallyVetoUse) {
			my(%vetoID);
			foreach (@{$ally->{'vetoId'}}) {
				$vetoID{$_} = 1;
			}
			out("<BR><BR><B>����${AfterName}������</B><TABLE cellpadding=0 cellspacing=0>");
			foreach ($HbfieldNumber..$islandNumber) {
				my($id, $name, $s);
				$id = $Hislands[$_]->{'id'};
				next if($id == $ally->{'id'});
				$name = islandName($Hislands[$_]);
				$s = ' CHECKED' if($vetoID{$id});
				out("<TR><TD><input type=checkbox name=VETOID value=\"$id\"$s></TD><TD>$name</TD></TR>");
			}
			my($s1, $s2) = (!$ally->{'vkind'}) ? ('', ' checked') : (' checked', '');
			out("<TR><TD colspan=2 class='M'>�������å������줿$AfterName�β�����</TD><TR>");
			out("<TR><TD align='center' colspan=2 class='M'>����<input type=radio name=VETOKIND value=\"1\"${s1}><FONT COLOR='#FF0000'>����</FONT> <input type=radio name=VETOKIND value=\"0\"${s2}><FONT COLOR='#0000FF'>����</FONT></TD><TR>");
			out("<TR><TD align='right' colspan=2 class='M'>���ޤ���</TD><TR>");
			out("<TR><TD align='center' colspan=2 class='M'><INPUT TYPE=\"submit\" VALUE=\"����\" NAME=\"AllypactButton\"></TD><TR>");
			out("</TABLE>");
		}
		out(<<END);
</TD><TD class='M'>
<BR><BR><B>������</B><small>(����${HlengthAllyComment}���ޤǡ��ȥåץڡ����Ρֳ�Ʊ���ξ��������ɽ������ޤ�)</small><BR>
<INPUT TYPE="text" NAME="ALLYCOMMENT"  VALUE="$ally->{'comment'}" SIZE=100 MAXLENGTH=50><BR>
<BR>
<INPUT TYPE="submit" VALUE="����" NAME="AllypactButton">
<BR><BR>
<B>��å�����������ʤ�</B>(��Ʊ���ξ������ξ��ɽ������ޤ�)<BR>
�����ȥ�<small>(����${HlengthAllyTitle}���ޤ�)</small><BR>
<INPUT TYPE="text" NAME="ALLYTITLE"  VALUE="$ally->{'title'}" SIZE=100 MAXLENGTH=50><BR>
��å�����<small>(����${HlengthAllyMessage}���ޤ�)</small><BR>
<TEXTAREA COLS=50 ROWS=16 NAME="ALLYMESSAGE" WRAP="soft">$allyMessage</TEXTAREA>
<BR>
�֥����ȥ�פ����ˤ���ȡ����礫��Υ�å������٤Ȥ��������ȥ�ˤʤ�ޤ���<BR>
�֥�å������פ����ˤ���ȡ�Ʊ���ξ������ˤϲ���ɽ������ʤ��ʤ�ޤ���
</TD></TR></TABLE>
END
	}

	out(<<END);
</FORM>
</td></tr></table>
</DIV>
END
}

# ���祳�����ѹ���λ
sub tempAllyPactOK {
	my($ally) = @_;
	out(<<END);
${HtagBig_}<FONT COLOR="$ally->{'color'}">$ally->{'mark'}</FONT>$ally->{'name'}�ξ�����ѹ����ޤ�����${H_tagBig}<HR>
END
	$HallyPactMode = 1;
	tempAllyPactPage();
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
<BASE HREF="$htmlDir/">
<link rel="stylesheet" type="text/css" href="${HcssDir}/$HcssDefault">
</HEAD>
$Body<DIV ID='BodySpecial'>
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
				$html2 .= "<B>=====[${HtagNumber_}<FONT SIZE=4>������$turn </FONT>${H_tagNumber}]================================================</B><BR>\n";
				$set_turn++;
			}
			$html2 .= "${HtagNumber_}��${H_tagNumber}:$message<BR>\n";
		}
		close(LIN);
	}
	open(HTML, ">${HhtmlDir}/hakolog.html");
#	print HTML jcode::sjis($html1); # jcode���ѻ�
#	print HTML jcode::sjis($html2);
#	print HTML jcode::sjis($html3);
	print HTML $html1;
	print HTML $html2;
	print HTML $html3;
	close (HTML);
	chmod(0666,"${HhtmlDir}/hakolog.html");
}

#----------------------------------------------------------------------
# �͸�����¾���ͤ򻻽Сʽ̾���
#----------------------------------------------------------------------
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $mountain, $navyPort, $sea) = (0, 0, 0, 0, 0);

	# �Ϸ������
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# ������
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if($kind != $HlandSea){
				$area++;
				if($kind == $HlandTown) {
					# Į
					$pop += $value;
				} elsif($kind == $HlandMountain) {
					# ��
					$mountain += $value;
				} elsif ($kind == $HlandNavy) {
					if ($HnavySpecial[(navyUnpack($value))[7]] & 0x8) {
						# ��
						$navyPort++;
					}
				}
			} elsif(!$value) {
				$sea++;
			}
		}
	}

	# ����
	$island->{'pop'}      = $pop;
	$island->{'area'}     = $area;
	$island->{'mountain'} = $mountain;
	$island->{'navyPort'} = $navyPort;
	$island->{'sea'}      = $sea;
	$island->{'farm'}     = 0;
	$island->{'factory'}  = 0;
}

# �ϰ�����Ϸ���������������ѡ�
sub countAroundforMake {
	my($land, $x, $y, $range, @kind) = @_;
	my($sea, $count, $sx, $sy, @list, @correct);
	foreach (@kind){
		$list[$_] = 1;
	}
	$sea = 0;
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		if(($sx < 0) || ($sy < 0)){
			# �ϰϳ��ξ��
			# ���˲û�
			$sea++;
		} elsif($list[$land->[$sx][$sy]]) {
			# �ϰ���ξ��
			$count++;
		}
	}
	$count += $sea if($list[$HlandSea]); # ���ʤ�û�
	return $count;
}
#----------------------------------------------------------------------
# ��ζ������(�����ѹ���)
#----------------------------------------------------------------------
sub deleteIsland {
	my($num) = @_;
	my($island) = $Hislands[$HidToNumber{$HcurrentID}];

	if($HdeadToSaveAsLose == 2) {
		require('./hako-turn.cgi');
	 	island_save($island, $HfightdirName, 'lose', 0);
	}

	my $aNum = $HidToAllyNumber{$HcurrentID};
	if(defined $aNum) {
		logDeleteAlly($Hally[$aNum]->{'name'});
		$Hally[$aNum]->{'dead'} = 1;
		$HallyNumber--;
	}
	foreach (@{$island->{'allyId'}}) {
		my $ally = $Hally[$HidToAllyNumber{$_}];
		my $allyMember = $ally->{'memberId'};
		my @newAllyMember = ();
		foreach (@$allyMember) {
			if(!(defined $HidToNumber{$_})) {
			} elsif($_ == $HcurrentID) {
				$ally->{'score'} -= $island->{$HrankKind} if(!$island->{'predelete'});
				$ally->{'number'}--;
			} else {
				push(@newAllyMember, $_);
			}
		}
		$ally->{'memberId'} = \@newAllyMember;
	}
	my @newID = ();
	foreach (@HpreDeleteID) {
		if(!(defined $HidToNumber{$_})) {
		} elsif($_ != $HcurrentID) {
			push(@newID, $_);
		}
	}
	@HpreDeleteID = @newID;
	# ��ơ��֥�����
	$island->{'dead'} = 1;
	$island->{$HrankKind} = 0;
	$island->{'pop'} = 0;
	$island->{'field'} = 0;
	$island->{'predelete'} = 0;

	allyOccupy();
	allySort();
	islandSort($HrankKind);

	logDeleteIsland($HcurrentID, $island->{'name'}) if($num);

	# �ᥤ��ǡ��������
	$HislandNumber--;
	$islandNumber--;

	deleteIslandData($island);
	writeIslandsFile($HcurrentID);

	unlock();
	tempDeleteIsland($island->{'name'});
}

#----------------------------------------------------------------------
# BattleField�����⡼��
#----------------------------------------------------------------------
sub bfieldMain {
	if (!$HbfieldMode) {
		$HislandList = getIslandList(-1, 1);
		# ����
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempBfieldPage();
	} else {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HdefaultPassword)) {
			# �ü�ѥ����
			if($HcurrentID == 0) {
				$HcurrentName = "BattleField " . ($HbfieldNumber + 1);
				$HcurrentOwnerName = $HadminName;
				$HinputPassword = $HmasterPassword;
				$HinputPassword2 = $HmasterPassword;
				if(!newIslandMain(1)) {
					unlock();
					return;
				}
			}

			# id����������
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($name) = $island->{'name'};
			my($id) = $island->{'id'};

			my($bId, $str, $tmpid);
			my $safety = 0;
			if(!$island->{'field'}) {
				# ����
				$Hislands[$HcurrentNumber]->{'field'} = 1;
				$str = "�̾���� �� Battle Field";
			} else {
				# ���
				$Hislands[$HcurrentNumber]->{'field'} = 0;
				$str = "Battle Field �� �̾����";
			}

			# �ǡ����񤭽Ф�
			islandSort($HrankKind);
			writeIslandsFile($id);

			unlock();

			# �ѹ�����
			tempBfieldOK($name, $str);
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# BattleField�����⡼�ɤΥȥåץڡ���
sub tempBfieldPage {
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2<BR>
<H1>Battle Field�����</H1>
END
	if($HoceanMode) {
		require('./hako-map.cgi');
		printIslandMapMain(2);
	}
	out(<<END);
<FORM action="$HthisFile" name="BfieldForm" method="POST">
END
	if($HoceanMode) {
		out(<<END);
�����ɸ����ꤷ�Ʋ�����<BR>��ɸ��
<SELECT NAME="OCEANX">
END
		my($i);
		foreach $i (0..($HoceanSizeX-1)) {
			out("<OPTION VALUE=$i>$i\n");
		}
		out(<<END);
</SELECT>, <SELECT NAME="OCEANY">
END
		foreach $i (0..($HoceanSizeY-1)) {
			out("<OPTION VALUE=$i>$i\n");
		}
		out(<<END);
</SELECT>�ˡ�<INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>������<BR><BR>
END
	}

	out(<<END);
<B>Battle Field������ѹ�����${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Bfield">
<INPUT TYPE="submit" VALUE="�����ѹ�" NAME="BfieldButton"><BR>
</FORM>
�ֿ�������(���٤Ƴ�)�פξ�硢��Υѥ���ɤϥޥ������ѥ���ɤˤʤ�ޤ���<BR>
�����塢ɬ�פ˱����ƥѥ���ɤ��ѹ����Ƥ���������</DIV>
END
}

# BattleField������λ
sub tempBfieldOK {
	my($name, $str) = @_;
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$name${AfterName}��Battle Field������ѹ����ޤ�����<br>$str${H_tagBig}
END
}

# BattleField��������
sub tempBfieldNG {
	my($str) = @_;
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}Battle Field�����ꥨ�顼($str)��${H_tagBig}$HtempBack2
END
}

#----------------------------------------------------------------------
# �����ͤˤ����ǡ��������⡼��
#----------------------------------------------------------------------
sub islandSetupMain() {
	if (!$HisetupMode) {
		# ����
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempIslandSetupPage(0);
		return;
	} elsif(!checkSpecialPassword($HdefaultPassword)) {
		# �ѥ���ɥ����å�
		# �ü�ѥ����
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}
	if($HisetupMode == 2) {
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		# ��̾�������������å�
		if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��|^����$/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadName();
			return;
		}
		# �����ʡ�̾�������������å�
		if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadOwnerName();
			return;
		}
		if($HoceanMode) {
			my($wmap) = $island->{'wmap'};
			my($wx, $wy) = ($wmap->{'x'}, $wmap->{'y'});
			if($HmapRandom) {
				my($wm) = randomIslandMap();
				if(defined $wm) {
					($HoceanMapX, $HoceanMapY) = ($wm->{'x'}, $wm->{'y'});
				} else {
					unlock();
					tempHeader();
					tempNewIslandFull();
					return 0;
				}
			}
			if($wx != $HoceanMapX || $wy != $HoceanMapY) {
				if(defined $HoceanMap[$HoceanMapX][$HoceanMapY]) {
					unlock();
					tempHeader();
					tempNewIslandAlready();
					return 0;
				}
				my($land, $landValue) = ($Hworld->{'land'}, $Hworld->{'landValue'});
				my $map = $island->{'map'};
				my(@mx) = @{$map->{'x'}};
				my(@my) = @{$map->{'y'}};
				my(@nx) = (($HoceanMapX * $HislandSizeX)..($HoceanMapX * $HislandSizeX + $HislandSizeX - 1));
				my(@ny) = (($HoceanMapY * $HislandSizeY)..($HoceanMapY * $HislandSizeY + $HislandSizeY - 1));
				my($i, $j, $x, $y, $xx, $yy, %convXY);
				foreach $j (0..$#my) {
					$y = $my[$j]; $yy = $ny[$j];
					foreach $i (0..$#mx) {
						$x = $mx[$i]; $xx = $nx[$i];
						$land->[$xx][$yy] = $land->[$x][$y];
						$landValue->[$xx][$yy] = $landValue->[$x][$y];
						$land->[$x][$y] = $HlandSea;
						$landValue->[$x][$y] = 0;
						$convXY{"$x,$y"} = { 'x'=>$xx, 'y'=>$yy };
					}
				}
				$island->{'wmap'} = { 'x' => $HoceanMapX, 'y' => $HoceanMapY };
				$island->{'map'}  = { 'x' => \@nx, 'y' => \@ny };
				$HoceanMap[$wmap->{'x'}][$wmap->{'y'}] = undef;
				$HoceanMap[$HoceanMapX][$HoceanMapY] = $HcurrentID;
				makeRen();
				my($n, $nId, $nCommand, $change);
				foreach $n (0..$islandNumber) {
					$nId = $Hislands[$n]->{'id'};
					$nCommand = readCommand($nId, $HcommandMax);
					$change = 0;
					foreach (@{$nCommand}) {
						my($nkind, $nx, $ny) = ($_->{'kind'}, $_->{'x'}, $_->{'y'});
						if((defined $convXY{"$nx,$ny"}) && (($kind < 90) || ((100 < $kind) && ($kind < 200)) || ((330 < $kind) && ($kind < 350)) || ($kind == $HcomNavyWreckRepair) || ($kind == $HcomNavyWreckSell) ||
								# ����(��ȯ)������(����)��ʣ����ߡ�����(��¤) <200 , 330< ����(����) <350 , �ĳ��������ĳ����
							((215 < $kind) && ($kind < 220)) || ((350 < $kind) && ($kind < 361)))) {
								# ��ư��ġ���ư���ᡤ���������ѹ������ƹ���ȷ���(����)[��������¤�ʳ��ǡ���ɸ���ꤹ����]
							$_->{'x'} = $convXY{"$nx,$ny"}->{'x'};
							$_->{'y'} = $convXY{"$nx,$ny"}->{'y'};
							$change = 1;
						}
					}
					writeCommand($nId, $nCommand) if($change);
				}
			}
		}

		$island->{'name'} = $HcurrentName;
		$island->{'owner'} = $HcurrentOwnerName;
		$island->{'birthday'} = ($Hbirthday < 0) ? 0 : ($Hbirthday > $HislandTurn) ? $HislandTurn : $Hbirthday;
		$island->{'absent'} = ($Habsent < 0) ? 0 : ($Habsent > $HgiveupTurn) ? $HgiveupTurn : $Habsent;
		$island->{'preab'} = $Hpreab;
		$island->{'money'} = ($Hmoney < 0) ? 0 : ($Hmoney > $HmaximumMoney) ? $HmaximumMoney : $Hmoney;
		$island->{'food'} = ($Hfood < 0) ? 0 : ($Hfood > $HmaximumFood) ? $HmaximumFood : $Hfood;
		$Hgain = 0 if($Hgain < 0);
		$island->{'gain'} = $Hgain;
		$island->{'field'} = $Hfield;
		$island->{'fight_id'} = $Hfight_id;
		$island->{'rest'} = $Hrest;
		$island->{'prize'} =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
		my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
		my %check;
		foreach (@Hflags) {
			$check{$_} = 1;
		}
		$flags = 0;
		foreach(reverse(1..$#Hprize)) {
			$flags |= $check{$_};
			$flags <<= 1 if($_ != 1);
		}
		undef %check;
		my $num = $HmonsterNumber - 1;
		foreach (@Hmonsters) {
			$check{$_} = 1;
		}
		$monsters = 0;
		foreach(reverse(0..$num)) {
			$monsters |= $check{$_};
			$monsters <<= 1 if($_);
		}
		undef %check;
		$num = $HhugeMonsterNumber - 1;
		foreach (@Hhmonsters) {
			$check{$_} = 1;
		}
		$hmonsters = 0;
		foreach(reverse(0..$num)) {
			$hmonsters |= $check{$_};
			$hmonsters <<= 1 if($_);
		}
		$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
		$Hmonsterkill = 0 if($Hmonsterkill < 0);
		$island->{'monsterkill'} = $Hmonsterkill;
		$island->{'sink'} = \@Hsink;
		$island->{'sinkself'} = \@Hsinkself;
		$island->{'ext'} = \@Hext;
		$island->{'subExt'} = \@HsubExt;
		$island->{'item'} = \@HtmpItem;
		$island->{'weather'} = \@HtmpWeather;
		islandSort($HrankKind, 1);
		if($HallyNumber) {
			allyOccupy();
			allySort();
		}
		writeIslandsFile();
	}
	# ����
	unlock();
	# �ƥ�ץ졼�Ƚ���
	tempIslandSetupPage(1);
}

# ��ǡ��������ڡ���
sub tempIslandSetupPage() {
	my($mode) = @_;

	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>${AfterName}�ǡ�������</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME="ISetup" VALUE="$HdefaultPassword">
<B>�ǡ�����������${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="submit" VALUE="�ǡ����������̤�" NAME="IslandChoice"><BR>
</FORM>
END

	return if(!$mode);

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	my($id) = $island->{'id'};
	my($name) = $island->{'name'};
	my($owner) = $island->{'owner'};
	my($birthday) = $island->{'birthday'};
	my($absent) = $island->{'absent'};
	my($preab) = $island->{'preab'};
	my($money) = $island->{'money'};
	my($food) = $island->{'food'};
	my($gain) = $island->{'gain'};
	my($prize) = $island->{'prize'};
	my($monsterkill) = $island->{'monsterkill'};
	my($sink) = $island->{'sink'};
	my($sinkself) = $island->{'sinkself'};
	my($subSink) = $island->{'subSink'};
	my($subSinkself) = $island->{'subSinkself'};
	my($ext) = $island->{'ext'};
	my($subExt) = $island->{'subExt'};
	my($field) = $island->{'field'};
	my($item) = $island->{'item'};
	my($weather) = $island->{'weather'};
	my($fight_id) = $island->{'fight_id'};
	my($rest) = $island->{'rest'};
	my($wmap) = $island->{'wmap'};
	my($wx, $wy) = ($wmap->{'x'}, $wmap->{'y'});

	$preab = ($preab == 1) ? ' checked' : '';
	$field = ($field == 1) ? ' checked' : '';
	my $islandList = '';
	my $fiName = '';
	if($fight_id == 0) {
		$islandList .= '<OPTION VALUE="-2">������';
		$islandList .= '<OPTION VALUE="-1">���ﾡ';
		$islandList .= '<OPTION VALUE="0" style="background:yellow;" selected>̤��';
		$islandList .= getIslandList(0, 1);
	} elsif($fight_id == -1) {
		$islandList .= '<OPTION VALUE="-2">������';
		$islandList .= '<OPTION VALUE="-1" style="background:yellow;" selected>���ﾡ';
		$islandList .= '<OPTION VALUE="0">̤��';
		$islandList .= getIslandList(0, 1);
	} elsif($fight_id == -2) {
		$islandList .= '<OPTION VALUE="-2" style="background:yellow;" selected>������';
		$islandList .= '<OPTION VALUE="-1">���ﾡ';
		$islandList .= '<OPTION VALUE="0">̤��';
		$islandList .= getIslandList(0, 1);
	} else {
		$islandList .= '<OPTION VALUE="-2">������';
		$islandList .= '<OPTION VALUE="-1">���ﾡ';
		$islandList .= '<OPTION VALUE="0">̤��';
		$islandList .= getIslandList($fight_id, 1, 'yellow');
	}
	
	my $predel = '';
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
		$predel = '�ڴ����ͤ��������$rest';
	}
	out("<HR>");
	if($HoceanMode) {
		require('./hako-map.cgi');
		printIslandMapMain(1);
	}
	out(<<END);
<FORM action="$HthisFile" name="IsetupForm" method="POST">
<INPUT TYPE="hidden" NAME="ISetup" VALUE="$HdefaultPassword">
<TABLE BORDER>
<TR><TH>${HtagTH_}$name${AfterName}${H_tagTH}$predel��${HtagTH_}�ǡ�������${H_tagTH}��<INPUT TYPE="submit" VALUE="����" NAME="ChangeButton"></TH></TR>

<TR><TD class='M'>
<TABLE BORDER width="100%">
<TR><TH colspan=12>���ܥǡ���</TH></TR><TR>
<TR>
<TH $HbgTitleCell rowspan=2>${HtagTH_}${AfterName}ID${H_tagTH}</TH>
END
	out("<TH $HbgTitleCell rowspan=2>${HtagTH_}�����ɸ${H_tagTH}</TH>") if($HoceanMode);
	out(<<END);
<TH $HbgTitleCell rowspan=2>${HtagTH_}${AfterName}̾${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}�����ʡ�̾${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}���ϥ�����${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}��ⷫ��${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}�رĳ�ȯ��${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}������и���${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}�ե������°��${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}�ȡ��ʥ�����${H_tagTH}</TH>
</TR>
<TR>
<TH $HbgTitleCell>${HtagTH_}�������${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ȯ��ߥ������${H_tagTH}</TH>
</TR>
<TR>
<TD align="center"><INPUT TYPE="hidden" NAME="ISLANDID" VALUE="$id">${id}</TD>
END
	if($HoceanMode) {
		out("<TD align=\"center\">��<SELECT NAME=\"OCEANX\">");
			my($i);
			foreach $i (0..($HoceanSizeX-1)) {
				if($i == $wx) {
					out("<OPTION VALUE=$i style=\"background:yellow;\" selected>$i\n");
				} else {
					out("<OPTION VALUE=$i>$i\n");
				}
			}
			out(<<END);
</SELECT>, <SELECT NAME="OCEANY">
END
			foreach $i (0..($HoceanSizeY-1)) {
				if($i == $wy) {
					out("<OPTION VALUE=$i style=\"background:yellow;\" selected>$i\n");
				} else {
					out("<OPTION VALUE=$i>$i\n");
				}
			}
			out(<<END);
</SELECT>��<BR><INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>������</TD>
END
	}
	out(<<END);
<TD align="center"><INPUT TYPE="text" NAME="ISLANDNAME" VALUE="$name" SIZE=20 MAXLENGTH=32>${AfterName}</TD>
<TD align="center"><INPUT TYPE="text" NAME="OWNERNAME" VALUE="$owner" SIZE=20 MAXLENGTH=32></TD>
<TD align="center"><INPUT TYPE="text" NAME="BIRTHDAY" VALUE="$birthday" SIZE=5 MAXLENGTH=32></TD>
<TD align="center"><INPUT TYPE="text" NAME="ABSENT" VALUE="$absent" SIZE=5 MAXLENGTH=32></TD>
<TD align="center"><INPUT TYPE="checkbox" NAME="PREAB" VALUE="1"$preab></TD>
<TD align="center"><INPUT TYPE="text" NAME="MONEY" VALUE="$money" SIZE=5 MAXLENGTH=32>$HunitMoney</TD>
<TD align="center"><INPUT TYPE="text" NAME="FOOD" VALUE="$food" SIZE=5 MAXLENGTH=32>$HunitFood</TD>
<TD align="center"><INPUT TYPE="text" NAME="GAIN" VALUE="$gain" SIZE=5 MAXLENGTH=32>
END
	my $navyComLevel = gainToLevel($island->{'gain'});
	out("(Lv.${navyComLevel})") if($HmaxComNavyLevel);
	out(<<END);
</TD>
<TD align="center"><INPUT TYPE="checkbox" NAME="FIELD" VALUE="1"$field></TD>
<TD align="center"><SELECT NAME="FIGHT_ID">$islandList</SELECT></TD>
<TD align="center"><INPUT TYPE="text" NAME="REST" VALUE="$rest" SIZE=5 MAXLENGTH=32>������</TD>
</TD></TR></TABLE></TD></TR>
END

	$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
	my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	my $col = $#Hprize;
	out("<TR><TH colspan=$col>��</TH></TR><TR>\n");
	foreach(1..$#Hprize) {
		out("<TD class='T'>${HtagTH_}${Hprize[$_]->{'name'}}${H_tagTH}</TD>\n");
	}
	out("</TR><TR>\n");
	my($f) = 1;
	foreach(1..$#Hprize) {
		my $s = '';
		if($flags & $f) {
			$s = ' CHECKED';
		}
		out("<TD align=\"center\"><input type=checkbox name=FLAGS value=\"$_\"$s></TH>\n");
		$f <<= 1;
	}
	out("</TR></TABLE></TD></TR>\n");
	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = $HmonsterNumber - 1;
	out("<TR><TH colspan=$HmonsterNumber>�༣��������</TH></TR><TR>\n");
	foreach(0..$col) {
		out("<TD class='T'>${HtagTH_}${HmonsterName[$_]}${H_tagTH}</TD>\n");
	}
	out("</TR><TR>\n");
	$f = 1;
	foreach(0..$col) {
		my $s = '';
		if($monsters & $f) {
			$s = ' CHECKED';
		}
		out("<TD align=\"center\"><input type=checkbox name=MONSTERS value=\"$_\"$s></TH>\n");
		$f <<= 1;
	}
	out("</TR></TABLE></TD></TR>\n");
	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = $HhugeMonsterNumber - 1;
	out("<TR><TH colspan=$HhugeMonsterNumber>�༣�����������</TH>\n");
#	out("<TH>�����༣��</TH>\n");
	out("</TR><TR>\n");
	foreach(0..$col) {
		out("<TD class='T'>${HtagTH_}${HhugeMonsterName[$_]}${H_tagTH}</TD>\n");
	}
#	out("<TD align=\"center\" rowspan=2><INPUT TYPE=\"text\" NAME=\"MONSTERKILL\" VALUE=\"$monsterkill\" SIZE=5 MAXLENGTH=32>$HunitMonster</TD>\n");
	out("</TR><TR>\n");
	$f = 1;
	foreach(0..$col) {
		my $s = '';
		if($hmonsters & $f) {
			$s = ' CHECKED';
		}
		out("<TD align=\"center\"><input type=checkbox name=HMONSTERS value=\"$_\"$s></TH>\n");
		$f <<= 1;
	}
	out("</TR></TABLE></TD></TR>\n");

	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = @HnavyName + 2;
	out("<TR><TH colspan=$col>��������������(��������¾��ܼ��硤�������Ἣ��)</TH></TR><TR><TD colspan=2>��</TD>\n");
	foreach(@HnavyName) {
		out("<TD class='T'>${HtagTH_}$_${H_tagTH}</TD>\n");
	}
	out("</TR><TR><TH colspan=2>¾��</TH>\n");
	my @kindNavy = ('��', '��');
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SINK\" VALUE=\"@$sink[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR><TR><TH colspan=2>����</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SINKSELF\" VALUE=\"@$sinkself[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	my $turn = @$subExt[0];
	$turn-- if($turn > 0);
	out("</TR><TH rowspan=2>${turn}������<BR>�ޤǤε�Ͽ</TH><TH>¾��</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBSINK\" VALUE=\"@$subSink[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR><TR><TH>����</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBSINKSELF\" VALUE=\"@$subSinkself[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR></TABLE></TD></TR>\n");

	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	out("<TR><TH colspan=11>��ĥ�ǡ���</TH>\n");
	out("<TH rowspan=2>����<BR>�༣��</TH>\n");
	out("<TD class='M' colspan='1'></TD>\n");
	out("</TR><TR>\n");
	foreach ('�����ե饰', '�׸���x10', '�ɷ���', '�߷���', '̱�߽�', '������', '��ȯ��', '���ɸ�', '���ɸ�', '���轱', '���˲�') {
		out("<TH $HbgTitleCell>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("</TR><TR>");
	my @after = ('', '', '��', '��', "$HunitPop", 'ȯ', 'ȯ', 'ȯ', '��', '��', '��');
	foreach (0..10){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"EXT\" VALUE=\"@$ext[$_]\" SIZE=5 MAXLENGTH=32>$after[$_]</TD>\n");
	}
	out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"MONSTERKILL\" VALUE=\"$monsterkill\" SIZE=5 MAXLENGTH=32>$HunitMonster</TD>\n");
	out("<TD class='M' colspan='1'></TD>\n");
	out("</TR><TR><TH colspan=13>���ֳ�ĥ�ǡ���(${turn}������ޤǤε�Ͽ)</TH></TR><TR>\n");
	foreach ('��Ͽ������', '�׸���x10', '�ɷ���', '�߷���', '̱�߽�', '������', '��ȯ��', '���ɸ�', '���ɸ�', '���轱', '���˲�', '�༣��', '�󾩶�') {
		out("<TH $HbgTitleCell>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("</TR><TR>");
	my @subAfter = ('����������', '', '��', '��', "$HunitPop", 'ȯ', 'ȯ', 'ȯ', '��', '��', '��', "$HunitMonster", "$HunitMoney");
	foreach (0..12){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBEXT\" VALUE=\"@$subExt[$_]\" SIZE=5 MAXLENGTH=32>$subAfter[$_]</TD>\n");
	}
	out("</TR></TABLE></TD></TR>\n");

	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = $#HitemName;
	out("<TR><TH colspan=$col>��ͭ�����ƥࡡ($HitemName[0])</TH></TR><TR>\n");
	foreach (1..$#HitemName) {
		out("<TD class='T'>${HtagTH_}$HitemName[$_]${H_tagTH}</TH>\n");
	}
	out("</TR><TR>\n");
	my %iflag;
	foreach (@$item) {
		$iflag{$_} = 1;
	}
	foreach (1..$#HitemName) {
		my $s = '';
		if($iflag{$_}) {
			$s = ' CHECKED';
		}
		out("<TD align=\"center\"><input type=checkbox name=ITEM value=\"$_\"$s></TD>\n");
	}
	out("</TR></TABLE></TD></TR>\n");
	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = 7 + $HtopLogTurn;
	out("<TR><TH colspan=$col>����</TH></TR><TR>\n");
	foreach ('����', '����', '����', '��®', '����', '����', '(̤����)') {
		out("<TH $HbgTitleCell rowspan=2>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("<TH $HbgTitleCell colspan=$HtopLogTurn>${HtagTH_}ŷ������${H_tagTH}</TH>\n");
	out("</TR><TR>");
	my($wTurn) = $HislandTurn + 3;
	foreach (1..$HtopLogTurn) {
		out("<TH $HbgTitleCell>${HtagTH_}������$wTurn${H_tagTH}</TH>\n");
		$wTurn--;
	}
	out("</TR><TR>");
	my @wAfter = ('��', 'hPa', '%', 'm/s', '', '', '');
	foreach (0..6){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"WEATHER\" VALUE=\"@$weather[$_]\" SIZE=5 MAXLENGTH=32>$wAfter[$_]</TD>\n");
	}
	my($i) = 7;
	foreach (1..$HtopLogTurn){
		if(@$weather[$i]) {
			out("<TD align=\"center\"><INPUT TYPE=\"hidden\" NAME=\"WEATHER\" VALUE=\"@$weather[$i]\" SIZE=5 MAXLENGTH=32><img src ='${HimageDir}/$HweatherImage[@$weather[$i]]' width='16' height='16'>$HweatherName[@$weather[$i]]</TD>\n");
		} else {
			out("<TD align=\"center\"><INPUT TYPE=\"hidden\" NAME=\"WEATHER\" VALUE=\"@$weather[$i]\" SIZE=5 MAXLENGTH=32>��</TD>\n");
		}
		$i++;
	}
	out("</TR></TABLE></TD></TR>\n");
	out(<<END);
</TR></TABLE>
<TR><TH colspan=8>${HtagTH_}${AfterName}�ǡ�������${H_tagTH}��<INPUT TYPE="submit" VALUE="����" NAME="ChangeButton"></TH></TR>
</TR></TABLE>
<INPUT TYPE="hidden" VALUE="dummy" NAME="IslandChange"></FORM></DIV>
END
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ��Ͽ��
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ȯ��
sub logDiscover {
	my($name, $owner) = @_;
	logHistory("${HtagName_}${name}${H_tagName}��${HtagName_}${owner}${H_tagName}�ˤ�ä�ȯ������롣");
}

# ��̾���ѹ�
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}��̾�Τ�${HtagName_}${name2}${AfterName}${H_tagName}���ѹ����롣");
}

# �����ʡ�̾���ѹ�
sub logChangeOwnerName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}����ͭ�Ԥ�${HtagName_}${name2}${H_tagName}���ѹ����롣");
}

# ������������
sub tempNoReferer {
	out(<<END);
${HtagBig_}���������ȤϤ���᤯������m(_ _)m${H_tagBig}$HtempBack
END
}

# �礬���äѤ��ʾ��
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}����������ޤ���${AfterName}�����դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ��������̾���ʤ����
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}${AfterName}�ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ��������̾�������ʾ��
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\$'�����äƤ����ꡢ��̵��${AfterName}�פΤ褦��̾���Ϥ��ޤ��礦��${H_tagBig}$HtempBack
END
}

# �����ǥ����ʡ�̾���ʤ����
sub tempNewIslandNoOwnerName {
	out(<<END);
${HtagBig_}���ʤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# �����ǥ����ʡ�̾�������ʾ��
sub tempNewIslandBadOwnerName {
	out(<<END);
${HtagBig_}',?()<>\$'�����äƤ���̾���Ϥ��ޤ��礦��${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}����${AfterName}�ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
sub tempNewIslandHead {
	out(<<END);
<DIV align='center'>
${HtagBig_}${AfterName}��ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}��${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
$HtempBack<BR>
</DIV>
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
	return true;
}
function Navi(x, y) {
	return true;
}
function NaviClose() {
	return true;
}
function sv(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	NaviClose();
	status = '';
	return false;
}
//-->
</SCRIPT>
END
}

# ̾���ѹ�����
sub tempChangeNothing {
	out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
	out(<<END);
${HtagBig_}�ѹ���λ���ޤ�����${H_tagBig}$HtempBack
END
}

# ���������
sub logDeleteIsland {
	my($id, $name) = @_;
#	logHistory("${HtagName_}${name}${AfterName}${H_tagName}��<B>�����͸��¤ˤ��</B>${HtagDisaster_}���${H_tagDisaster}�Ȥʤ롣");
#	logHistory("${HtagName_}${name}${AfterName}${H_tagName}�ˡ�����<B>ŷȳ���ߤ�</B>���äȤ����ޤ�${HtagDisaster_}�������פ�${H_tagDisaster}�׷���ʤ��ʤ�ޤ�����");
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}�ϡ�������<B>�ܤ�˿���</B>Φ�ϤϤ��٤�${HtagDisaster_}���פ��ޤ�����${H_tagDisaster}");
}

# ��ζ������(���ڥ����⡼��)
sub tempDeleteIsland {
	my($name) = @_;
	out(<<END);
${HtagBig_}${name}${AfterName}����������ޤ�����${H_tagBig}$HtempBack
END
}

1;

