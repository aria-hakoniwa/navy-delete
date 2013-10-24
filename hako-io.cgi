# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �������ѥ�����ץ�(ver1.00)
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
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
	my($num) = @_; # 0�����Ϸ������ޥ�ɡ��Ǽ��ĥ����ɤߤ��ޤ�
				   # -1�������Ϸ��������ޥ�ɤ��ɤ�
				   # -2�������Ϸ����ɤ�
				   # -3���������ޥ�ɤ��ɤ�
				   # -4�������Ǽ��ĥ����ɤ�
				   # �ֹ���Ȥ�������Ϸ������ޥ�ɡ��Ǽ��ĥ��������ɤߤ���

	# �ǡ����ե�����򳫤�
	if(!open(IN, "${HdirName}/$HmainData")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/$HmainData");
		if(!open(IN, "${HdirName}/$HmainData")) {
			return 0;
		}
	}

	# �ƥѥ�᡼�����ɤߤ���
	my $tmp = <IN>;
	chomp($tmp);
	($HislandTurn, $HplayNow) = split(/,/, $tmp); # �������, ��������ե饰
#	if($HislandTurn == 0) {
#		return 0;
#	}
	$HislandLastTime = int(<IN>); # �ǽ���������
	if($HislandLastTime == 0) {
		return 0;
	}
	# unitTime��repeatTurn�ξ��
	my $armTurn = ($HarmisticeTurn < $HsurvivalTurn) ?  $HsurvivalTurn : $HarmisticeTurn;
	$HarmTime = $HunitTime;
	$HarmRepeatTurn = $HrepeatTurn;
	if($armTurn && ($HislandTurn < $armTurn)){
		$HunitTime = $HarmisticeTime;
		$HrepeatTurn = $HarmisticeRepeatTurn;
	}
	$HislandNumber = int(<IN>); # ������
	$islandNumber = $HislandNumber - 1; # ������ - 1
	$HislandNextID = int(<IN>); # ���˳�����Ƥ�ID
	# �������¤������ID
	$tmp = <IN>;
	chomp($tmp);
	my(%preFlag);
	foreach (split(/,/, $tmp)) {
		my($pID, $pTurn) = split(/<>/, $_);
		$preFlag{$pID} = $pTurn;
		push(@HpreDeleteID, $pID);
	}

	# �ȡ��ʥ�����
	$HislandFightMode  = int(<IN>);  # ���ߤ���Ʈ�⡼��
	$HislandChangeTurn = int(<IN>);  # �ڤ��ؤ�������
	$HislandFightCount = int(<IN>);  # �������ܤ�

	chomp($tmp = <IN>); # ��������
	@HwarIsland = split(/,/, $tmp);
	<IN>;# ��ĥ��
	<IN>;# ��ĥ��
	<IN>;# ��ĥ��
	<IN>;# ��ĥ��
	<IN>;# ��ĥ��
	<IN>;# ��ĥ��
	if($Htournament){
		# �ȡ��ʥ��ȥ⡼��
		if(($HislandChangeTurn != $HyosenTurn) && ($HislandTurn < $HyosenTurn)) {
			# ����������ѹ��������ν���
			$HislandChangeTurn = $HyosenTurn;
			$HislandFightMode  = 0;
			$HislandFightCount = 0;
		}
		$HcounterSetting = 0;
		$HallyUse = 0;
		$HuseAmity = 0;
		$HuseDeWar = 0;
		$HarmisticeTurn = 0;
		$HsurvivalTurn = 0;
		if($HislandFightMode == 1) {
			# ��ȯ
			@HflexTime = @HtmTime2;
			$HunitTime = $HdevelopeTime;
			$HunitTime = (($HislandTurn > $HyosenTurn) && ($HislandTurn == $HislandChangeTurn - $HdevelopeTurn)) ? $HinterTime : $HdevelopeTime;
			$HrepeatTurn = $HdeveRepCount;
		} elsif($HislandFightMode == 2) {
			# ��Ʈ
			@HflexTime = @HtmTime3;
			$HunitTime = $HfightTime;
			$HrepeatTurn = $HfightRepCount;
		} else {
			# ͽ��
			@HflexTime = @HtmTime1;
			$HunitTime = $HyosenTime;
			$HrepeatTurn = $HyosenRepCount;
		}
	} else {
		$HislandFightMode  = 0;  # ���ߤ���Ʈ�⡼��
		$HislandChangeTurn = 0;  # �ڤ��ؤ�������
		$HislandFightCount = 0;  # �������ܤ�
	}
	# flexTime����
	$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	# ���������Ƚ��
	my($now) = time;
	my $flag = 0; # �����󹹿�����0����������1
	my $tempMode = $HmainMode;
	my $predelNumber = @HpreDeleteID; # �����ͤ����������
	if (
		( ($Hdebug && ($HmainMode eq 'Hdebugturn')) || (($now - $HislandLastTime) >= $HunitTime) )
		&&
		( !$HgameLimitTurn || ($HislandTurn < $HgameLimitTurn) )
		&&
		( !$HsurvivalTurn || ($islandNumber != $predelNumber) || ($HislandTurn <= $HsurvivalTurn) )
		&&
		( !$Htournament || ($islandNumber != $predelNumber) || ($HislandTurn <= $HyosenTurn) )
	   ) {
		$HmainMode = 'turn';
		$num = -1; # �����ɤߤ���
		$flag = 1; # �����ե饰��1��
	}

	$HnextTime = $HislandLastTime + $HunitTime;
	if($flag) {
		if($HflexTimeSet) {
			$HnextTime += 3600 * $HflexTime[(($HislandTurn + 1) % ($#HflexTime + 1))];
		} else {
			$HnextTime += $HunitTime;
		}
	}

	if (
		!($HgameLimitTurn && !($HislandTurn < $HgameLimitTurn)) && 
		!($HsurvivalTurn && !($islandNumber > $predelNumber) && ($HislandTurn > $HsurvivalTurn)) && 
		!($Htournament && !($islandNumber > $predelNumber) && ($HislandTurn > $HyosenTurn))
	   ) {
		$HleftTime = $HnextTime - $now;
		$HplayNow  = 1 if(!$HarmisticeTurn && !$Htournament);
		$HnextTime = sprintf('%d�� %d�� %d��', (gmtime($HnextTime + $Hjst))[4] + 1, (gmtime($HnextTime + $Hjst))[3,2]);
	} else {
		$HplayNow  = 0;
		$HnextTime = ' ';
		$HmainMode = ($tempMode ne '') ? $tempMode : 'top';
	}

	# ����ɤߤ���
	if($HoceanMode && !(-e "${HdirName}/world.${HsubData}") && !(-e "${HdirName}/worldtmp.${HsubData}")) {
		$HoceanMapNone = 1;
	}
	my($i);
	# �����ͤ�������Υե饰���å�
	$HbfieldNumber = 0;
	foreach $i (0..$islandNumber) {
		$Hislands[$i] = readIsland($num);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
		if($Hislands[$i]->{'field'}) {
			$HbfieldNumber++;
		}
		if($preFlag{$Hislands[$i]->{'id'}}) {
			# �����ͤ�������Υե饰����
			$Hislands[$i]->{'predelete'} = $preFlag{$Hislands[$i]->{'id'}};
		}
	}
	# �ե�������Ĥ���
	close(IN);

	# ����
	my($island);
	if($HoceanMapNone && ($num >= -2)) {
		my($x, $y, $i, $j, @land, @landValue);
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$i];
			foreach $y (@{$island->{'map'}->{'y'}}) {
				foreach $x (@{$island->{'map'}->{'x'}}) {
					$Hworld->{'land'}->[$x][$y] = $island->{'land'}->[$x][$y];
					$Hworld->{'landValue'}->[$x][$y] = $island->{'landValue'}->[$x][$y];
				}
			}
		}
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$i];
			($island->{'land'}, $island->{'landValue'}) = ($Hworld->{'land'}, $Hworld->{'landValue'});
		}
	} elsif(($HoceanMode && ($num >= -2)) || $HislandMapNone) {
		if(!open(WIN, "${HdirName}/world.${HsubData}")) {
			if(-e "${HdirName}/worldtmp.${HsubData}") {
				rename("${HdirName}/worldtmp.${HsubData}", "${HdirName}/world.${HsubData}");
			}
			if(!open(WIN, "${HdirName}/world.${HsubData}")) {
				exit(0);
			}
		}
		chomp(my @line = <WIN>);
		close(WIN);
		my $map  = { 'x' => \@defaultX, 'y' => \@defaultY };
		($Hworld->{'land'}, $Hworld->{'landValue'}, $Hworld->{'landValue2'}) = readLand($map, @line);
		if(!$HislandMapNone) {
			foreach $i (0..$islandNumber) {
				$island = $Hislands[$i];
				($island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}) = ($Hworld->{'land'}, $Hworld->{'landValue'}, $Hworld->{'landValue2'});
			}
		} else {
			foreach $i (0..$islandNumber) {
				$island = $Hislands[$i];
				my(@mx) = @{$island->{'map'}->{'x'}};
				my(@my) = @{$island->{'map'}->{'y'}};
				my($x, $y, $i, $j, @land, @landValue);
				foreach $j (@defaultY) {
					$y = $my[$j];
					foreach $i (@defaultX) {
						$x = $mx[$i];
						$land[$i][$j] = $Hworld->{'land'}->[$x][$y];
						$landValue[$i][$j] = $Hworld->{'landValue'}->[$x][$y];
						$landValue2[$i][$j] = $Hworld->{'landValue2'}->[$x][$y];
					}
				}
				$island->{'land'} = \@land;
				$island->{'landValue'} = \@landValue;
				$island->{'landValue2'} = \@landValue2;
				$island->{'map'} = $map;
			}
		}
	}
	# Ʊ���ǡ������ɤ߹���
	readAllyFile() if($HallyUse || $HarmisticeTurn || ($HmainMode eq 'asetup'));

	# �����ƥ�ν���
	if($HuseItem) {
		my $iKind;
		foreach $iKind (1..$#HitemName) {
			foreach (0..5) {
				push(@{$Hitems[$_]}, $iKind) if($HitemSpecial[$iKind][$_] != 0);
			}
			foreach (6..23) {
				push(@{$Hitems[$_]}, $iKind) if($HitemSpecial[$iKind][$_] != 1);
			}
		}
		my %keyItem;
		foreach (@{$Hitems[0]}) {
			$keyItem{$_} = 1;
		}
		$HitemComplete  = 0;
		$HitemCompleteA = 0;
		my(%checkItemA);
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$i];
			foreach (1..23) {
				$island->{'itemAbility'}[$_] = $HitemSpecial[0][$_];
			}
			my(%checkItem);
			foreach $iKind (@{$island->{'item'}}) {
				next if($checkItem{$iKind});
				$checkItem{$iKind} = 1;
				next if($iKind eq '');
				$island->{'itemNumber'}++;
				foreach (1..6, 24) {
					$island->{'itemAbility'}[$_] = $HitemSpecial[$iKind][$_] if($island->{'itemAbility'}[$_] < $HitemSpecial[$iKind][$_]);
				}
				foreach (7..23) {
					$island->{'itemAbility'}[$_] *= $HitemSpecial[$iKind][$_];
				}
				$HitemGetId[$iKind]{$island->{'id'}} = 1;
				next if(!$keyItem{$iKind});
				$island->{'keyItemNumber'}++;
				next if(!$HallyItemComplete);
				foreach (@{$island->{'allyId'}}) {
					my $aNum = $HidToAllyNumber{$_};
					next if($checkItemA{$aNum}{$iKind});
					$checkItemA{$aNum}{$iKind} = 1;
					my $ally = $Hally[$aNum];
					$ally->{'keyItemNumber'}++;
					$HitemCompleteA = $ally->{'id'} if(@{$Hitems[0]} && ($ally->{'keyItemNumber'} == @{$Hitems[0]}));
				}
			}
			@{$island->{'item'}} = sort { $a <=> $b } keys %checkItem;
			$HitemComplete = $island->{'id'} if(@{$Hitems[0]} && ($island->{'keyItemNumber'} == @{$Hitems[0]}));
		}
		foreach (1..$#HitemName){
			push(@Hitem, $_) if!(keys %{$HitemGetId[$_]});
		}
		$HitemRest = @Hitem;
	} else {
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$i];
			foreach (1..23) {
				$island->{'itemAbility'}[$_] = $HitemSpecial[0][$_];
			}
		}
	}
	foreach $i (0..$islandNumber) {
		$island = $Hislands[$i];
		if($HoceanMode) {
			# ��ɸ���Ϸ���ID�򥻥å�
			my($x, $y);
			foreach $x (@{$island->{'map'}->{'x'}}) {
				foreach $y (@{$island->{'map'}->{'y'}}) {
					$HlandID[$x][$y] = $island->{'id'};
				}
			}
		}
		# ���ޥ�ɼ¹ԥե饰����
		next if($HmainMode ne 'turn');
		foreach (keys %{$island->{'epoint'}}) {
			delete $island->{'epoint'}{$_} if!($Hislands[$HidToNumber{$_}]->{'event'}[0]);
		}
		if(!$HcomflagUse) {
			$island->{'comflag'} = 0;
		} elsif($HcomflagUse == 1) {
			$island->{'comflag'} = 1;
		}
	}
	makeRen() if($HoceanMode && $HnotuseNavyMove);
	if (
		!$HplayNow ||
		$HitemComplete || $HitemCompleteA ||
		($HsurvivalTurn && ($islandNumber - $predelNumber == $HbfieldNumber) && ($HislandTurn > $HsurvivalTurn)) ||
		($Htournament && ($islandNumber - $predelNumber == $HbfieldNumber) && ($HislandTurn > $HyosenTurn))
	   ) {
		# �ȥåץ⡼�ɤ��ѹ�
		$HmainMode = ($tempMode ne '') ? $tempMode : 'top';
		$HplayNow  = 0;
		$HnextTime = ' ';
	}
	return 1;
}

# ��ҤȤ��ɤߤ���
sub readIsland {
	my($num) = @_;
	my($name, $owner, $birthday, $id, $prize, $absent, $preab, $comflag, $earth, $comment, $password, $money, $food,
		$pop, $area, $farm, $factory, $mountain, $tmp, @amity, @fleet, @priority, @fkind, $gain, $monskill, $monslive,
		@sinktmp, @sink, @sinkself, @subSink, @subSinkself, @exttmp, @ext, @subExt, $field, @item, @weather,
		$fight_id, $rest, @event, $point, @defeat ,%epoint, @epointtmp, @xytmp, @x, @y, $map, $wmap, @move);
	chomp($name = <IN>);     # ���̾��
	chomp($owner = <IN>);    # �����ʡ���̾��
	$birthday = int(<IN>);   # ���ϥ�����
	$id = int(<IN>);         # ID�ֹ�
	chomp($prize = <IN>);    # ����
	chomp(($absent, $preab, $comflag, $earth) = split(/\,/, <IN>)); # Ϣ³��ⷫ���, ��ȯ����(�رĤ�������), ���ޥ�ɼ¹�����, �ϵ�⡼�ɼ���ɽ��
	chomp($comment = <IN>);  # ������
	chomp($password = <IN>); # �Ź沽�ѥ����
	$money    = int(<IN>);   # ���
	$food     = int(<IN>);   # ����
	$pop      = int(<IN>);   # �͸�
	$area     = int(<IN>);   # ����
	$farm     = int(<IN>);   # ����
	$factory  = int(<IN>);   # ����
	$mountain = int(<IN>);   # �η���
	chomp($tmp = <IN>);      # ͧ����
		@amity = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ����̾
		@fleet = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ��Ũ��
		@priority = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ��ͭ��������
		@fkind = split(/\,/, $tmp);
	$gain     = int(<IN>);   # ������и���
	$monskill = int(<IN>);   # �����༣��
	chomp($monslive = <IN>); # ���ýи���, ����, ����(����), ��°���������и���, ����
	chomp($tmp = <IN>);      # ������
		@sinktmp = split(/\-/, $tmp);
			@sink = split(/\,/,$sinktmp[0]);        # ����ʳ��δ���
			@sinkself = split(/\,/,$sinktmp[1]);    # ����
			@subSink = split(/\,/,$sinktmp[2]);     # ���ּ���ʳ��δ���
			@subSinkself = split(/\,/,$sinktmp[3]); # ���ּ���
	chomp($tmp = <IN>);      # ��ĥ�ΰ�
		@exttmp = split(/<>/, $tmp);
			@ext = split(/\,/,$exttmp[0]);    # ��ĥ�ΰ�
			# �����ե饰, �׸���x10, �ɷ���, �߷���, ̱�߽�, ������, ��ȯ��, ���ɸ�, ���ɸ�, ���轱, ���˲�
			@subExt = split(/\,/,$exttmp[1]); # ���ֳ�ĥ�ΰ�
			# ��Ͽ������, �׸���x10, �ɷ���, �߷���, ̱�߽�, ������, ��ȯ��, ���ɸ�, ���ɸ�, ���轱, ���˲�, �༣��, �󾩶�
	chomp($field = <IN>);    # �ե������°��
	chomp($tmp = <IN>);      # �����ƥ�
		@item = split(/\,/, $tmp);
	chomp($tmp = <IN>); # ����,����,����,��®,����,����,�۾�,ŷ��(��ɽ����)
		$tmp = "20,1013,40,0,0,0,0,2,2,2,2" if($tmp == '');
		@weather = split(/\,/, $tmp);
	chomp(($fight_id, $rest) = split(/\,/, <IN>)); # �ȡ��ʥ��� �������ID, ��ȯ��߻Ĥ꥿�����
	chomp($tmp = <IN>); # ���٥�ȥե饰 ���ϥ����� ���� ������ �ϼ� ���� ������ ����� ������� �����ͥץ쥼��Ȥ�̵ͭ ��������ƥ� �ɲ��ɸ� ���ýи�1 ���ýи�2 ������ýи�1 ������ýи�2 �����и�1 �����и�2 ��ư����
#               0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
		$tmp = "0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0" if($tmp == '');
		@event = split(/\,/, $tmp);
	$point = int(<IN>); # �ݥ����
	chomp($tmp = <IN>); # ���פ�������̾,�������,������
		@defeat = split(/\,/, $tmp);
	chomp($tmp = <IN>); # ���٥�ȥݥ����
		@epointtmp = split(/\,/, $tmp);
		for($i=0;$i<$#epointtmp;$i+=2) {
			$epoint{$epointtmp[$i]} = $epointtmp[$i+1];
		}
	chomp($tmp = <IN>);      # �ޥå������Ǽ x0,x1,...,xn<>y0,y1,...,yn<>x<>y
		if(!$HoceanMode && !(-e "${HdirName}/${id}.${HsubData}") && !(-e "${HdirName}/${id}tmp.${HsubData}")) {
			$HislandMapNone = 1;
		}
		@xytmp = split(/<>/, $tmp);
			@x = (($HoceanMode || $HislandMapNone) && (defined $xytmp[0])) ? split(/\,/, $xytmp[0]) : (0..($HislandSizeX-1));
			@y = (($HoceanMode || $HislandMapNone) && (defined $xytmp[1])) ? split(/\,/, $xytmp[1]) : (0..($HislandSizeY-1));
		$map  = { 'x' => \@x, 'y' => \@y };
		$wmap = { 'x' => $xytmp[2], 'y' => $xytmp[3] };
		if($HoceanMapNone) {
			$wmap = randomIslandMap(); # ��κ�ɸ�����
			# �ޥå�����
			my @x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
			my @y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
			$map = { 'x' => \@x, 'y' => \@y };
		}
		$HoceanMap[$wmap->{'x'}][$wmap->{'y'}] = $id;
	chomp($tmp = <IN>);      # ��ư���� x,y<>x,y<>x,y<>x,y
		@move = split(/<>/, $tmp);
	<IN>; # ͽ��
	<IN>; # ͽ��

	# HidToName�ơ��֥����¸
	$HidToName{$id} = $name;

	my(@line, @land, $command, $lbbs);

	# �Ϸ�
	if((!$HoceanMode && (($num == -1) || ($num == -2) || ($num == $id))) || $HoceanMapNone) {
		if(!open(IIN, "${HdirName}/${id}.${HsubData}")) {
			if(-e "${HdirName}/${id}tmp.${HsubData}") {
				rename("${HdirName}/${id}tmp.${HsubData}", "${HdirName}/${id}.${HsubData}");
			}
			if(!open(IIN, "${HdirName}/${id}.${HsubData}")) {
				#exit(0);
				$HislandMapNone = 1;
			}
		}
		if(!$HislandMapNone) {
			chomp(@line = <IIN>);
			close(IIN);
			@land = readLand($map, @line);
		}
	}

	# ���ޥ��
	if(($num == -1) || ($num == -3) || ($num == $id)) {
		if( $HmainMode eq 'owner'       || # ��ȯ�⡼��
			$HmainMode eq 'commandJava' || # ���ޥ�����ϥ⡼��
			$HmainMode eq 'command'     || # ���ޥ�����ϥ⡼��
			$HmainMode eq 'command2'    || # ���ޥ�����ϥ⡼�ɡ�ver1.1����ɲá���ư���ѡ�
			$HmainMode eq 'comment'     || # ���������ϥ⡼��
			$HmainMode eq 'fleetname'   || # ����̾�ѹ��⡼��
			$HmainMode eq 'priority'    || # ��Ũ���ѹ��⡼��
			$HmainMode eq 'earth'       || # ����ɽ������⡼��
			$HmainMode eq 'comflag'     || # ���ޥ�ɼ¹�����⡼��
			$HmainMode eq 'preab'       || # �رĶ�Ʊ��ȯ�⡼��
			$HmainMode eq 'lbbs'        || # ������Ǽ��ĥ⡼��
			$HmainMode eq 'new'         || # ��ο�������
			$HmainMode eq 'print'       || # �Ѹ��⡼��
			$HmainMode eq 'reload'      || # ��¸�ǡ��������⡼��
			$HmainMode eq 'turn'        || # ������ʹ�
			$HmainMode eq 'camp'        || # �رĥ⡼��
			$HmainMode eq 3             || # ��Х���⡼��
			$HmainMode eq 4                # ��Х���⡼��
		) {
			$command = readCommand($id, $HcommandMax);
		}
	}

	# ������Ǽ���
	if(($num == -4) || ($num == $id)) {
		if( $HmainMode eq 'owner'       || # ��ȯ�⡼��
			$HmainMode eq 'commandJava' || # ���ޥ�����ϥ⡼��
			$HmainMode eq 'command'     || # ���ޥ�����ϥ⡼��
			$HmainMode eq 'command2'    || # ���ޥ�����ϥ⡼�ɡ�ver1.1����ɲá���ư���ѡ�
			$HmainMode eq 'comment'     || # ���������ϥ⡼��
			$HmainMode eq 'fleetname'   || # ����̾�ѹ��⡼��
			$HmainMode eq 'priority'    || # ��Ũ���ѹ��⡼��
			$HmainMode eq 'earth'       || # ����ɽ������⡼��
			$HmainMode eq 'comflag'     || # ���ޥ�ɼ¹�����⡼��
			$HmainMode eq 'preab'       || # �رĶ�Ʊ��ȯ�⡼��
			$HmainMode eq 'lbbs'        || # ������Ǽ��ĥ⡼��
			$HmainMode eq 'landmap'     || # �Ѹ��⡼��
			$HmainMode eq 'new'         || # ��ο�������
			$HmainMode eq 'print'       || # �Ѹ��⡼��
			$HmainMode eq 'reload'      || # ��¸�ǡ��������⡼��
			$HmainMode eq 5                # ��Х���⡼��
		) {
			$lbbs = readLbbs($id);
		}
	}

	# �緿�ˤ����֤�
	return {
		'name' => $name,
		'owner' => $owner,
		'birthday' => $birthday,
		'id' => $id,
		'prize' => $prize,
		'absent' => $absent,
		'preab' => $preab,
		'comflag' => $comflag,
		'earth' => $earth,
		'comment' => $comment,
		'password' => $password,
		'money' => $money,
		'food' => $food,
		'pop' => $pop,
		'area' => $area,
		'farm' => $farm,
		'factory' => $factory,
		'mountain' => $mountain,
		'amity' => \@amity,
		'fleet' => \@fleet,
		'priority' => \@priority,
		'fkind' => \@fkind,
		'gain' => $gain,
		'monsterkill' => $monskill,
		'monsterlive' => $monslive,
		'sink' => \@sink,
		'sinkself' => \@sinkself,
		'subSink' => \@subSink,
		'subSinkself' => \@subSinkself,
		'ext' => \@ext,
		'subExt' => \@subExt,
		'field' => $field,
		'item' => \@item,
		'weather' => \@weather,
		'fight_id' => $fight_id,
		'rest' => $rest,
		'event' => \@event,
		'point' => $point,
		'defeat' => \@defeat,
		'epoint' => \%epoint,
		'map' => $map,
		'wmap' => $wmap,
		'move' => \@move,
		'land' => $land[0],
		'landValue' => $land[1],
		'landValue2' => $land[2],
		'command' => $command,
		'lbbs' => $lbbs,
	};
}

# �Ϸ��ɤ߹���
sub readLand {
	my($map, @line) = @_;

	my(@land, @landValue, @landValue2, @mx, @my);
	@mx = sort { $a <=> $b } @{$map->{'x'}};
	@my = sort { $a <=> $b } @{$map->{'y'}};
	my($x, $y, $dx, $dy, $startx, $sflagx, $endx, $starty, $sflagy, $endy);
	if(!$HoceanMode && !$HislandMapNone) {
		$dx = @{$map->{'x'}} - (length($line[0]) / 18);
		$dy = @{$map->{'y'}} - @line;
		$sflagx = int($dx/2);
		$startx = ($sflagx < 0) ? 0 : abs($sflagx);
		$sflagx = 0 if($sflagx > 0);
		$endx   = $startx + $#{$map->{'x'}};
		$sflagy = int($dy/2);
		$starty = ($sflagy < 0) ? 0 : abs($sflagy);
		$endy   = $starty + $#{$map->{'y'}};
	} else {
		$sflagx = 0;
		$startx = 0;
		$endx   = (length($line[0]) / 18) - 1;
		$sflagy = 0;
		$starty = 0;
		$endy   = $#line;
		if($HislandMapNone) {
			@mx = ($startx..$endx);
			@my = ($starty..$endy);
		}
	}
	foreach $y ($starty..$endy) {
		foreach $x ($startx..$endx) {
			$line[$y - $sflagy] =~ s/^(..)(........)(........)//;
			next if($x + $sflagx < 0);
                        my $temp;
			$land[$mx[$x + $sflagx]][$my[$y]] = hex($1);
                        $landValue[$mx[$x + $sflagx]][$my[$y]] = hex($2);
                        $landValue2[$mx[$x + $sflagx]][$my[$y]] = hex($3);
			last if(!length($line[$y - $sflagy]));
		}
	}
	return (\@land, \@landValue, \@landValue2);
}

# ���ޥ���ɤ߹���
sub readCommand {
	my($id, $cnum) = @_;
	my(@line, @command);
	if(!open(CIN, "${HdirName}/${id}.${HcommandData}")) {
		if(-e "${HdirName}/${id}tmp.${HcommandData}") {
			rename("${HdirName}/${id}tmp.${HcommandData}", "${HdirName}/${id}.${HcommandData}");
		}
		if(!open(CIN, "${HdirName}/${id}.${HcommandData}")) {
			open(COUT, ">${HdirName}/${id}.${HcommandData}");
			close(COUT);
			open(CIN, "${HdirName}/${id}.${HcommandData}");
		}
	}
	chomp(@line = <CIN>);
	close(CIN);

	my($i);
	for($i = 0; $i < $cnum; $i++) {
		$line = shift(@line);
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
		my($kind, $target, $x, $y, $arg, $target2) = (int($1), int($2), int($3), int($4), int($5), int($6));
		($kind, $target, $x, $y, $arg, $target2) = (41, 0, 0, 0, 0, 0) if(!$kind);
		$command[$i] = {
			'kind'    => $kind,
			'target'  => $target,
			'x'       => $x,
			'y'       => $y,
			'arg'     => $arg,
			'target2' => $target2
		}
	}

	return \@command;
}

# ������Ǽ����ɤ߹���
sub readLbbs {
	my($id) = @_;
	my(@lbbs);
	if(!open(LIN, "${HlogdirName}/${id}.${HlbbsData}")) {
		if(-e "${HlogdirName}/${id}tmp.${HlbbsData}") {
			rename("${HlogdirName}/${id}tmp.${HlbbsData}", "${HlogdirName}/${id}.${HlbbsData}");
		}
		if(!open(LIN, "${HlogdirName}/${id}.${HlbbsData}")) {
			open(LOUT, ">${HlogdirName}/${id}.${HlbbsData}");
			close(LOUT);
			open(LIN, "${HlogdirName}/${id}.${HlbbsData}");
		}
	}
	chomp(@lbbs = <LIN>);
	close(LIN);

	return \@lbbs;
}

# ����ǡ����񤭹���
sub writeIslandsFile {
	my($num) = @_; # 0�����Ϸ������ޥ�ɡ��Ǽ��ĥ����Ϸ��񤭤��ޤ�
				   # -1�������Ϸ��������ޥ�ɤ�񤭤���
				   # -2�������Ϸ���񤭤���
				   # -3���������ޥ�ɤ�񤭤���
				   # -4�������Ǽ��ĥ���񤭤���
				   # �ֹ���Ȥ�������Ϸ������ޥ�ɡ��Ǽ��ĥ������Ͻ񤭤���

	# �ե�����򳫤�
	open(OUT, ">${HdirName}/hakojima.tmp");

	# �ƥѥ�᡼���񤭹���
	print OUT "$HislandTurn,$HplayNow\n";
	print OUT "$HislandLastTime\n";
	print OUT "$HislandNumber\n";
	print OUT "$HislandNextID" . "\n";
	my(@preTemp, %preCheck);
	foreach (@HpreDeleteID) {
		next if($preCheck{$_});
		my $turn = $Hislands[$HidToNumber{$_}]->{'predelete'};
		if($turn) {
			push(@preTemp, "$_<>$turn");
			$preCheck{$_} = 1;
		}
	}
	print OUT join(',', @preTemp) . "\n";
	print OUT "$HislandFightMode\n";
	print OUT "$HislandChangeTurn\n";
	print OUT "$HislandFightCount\n";
	print OUT join(',', @HwarIsland) . "\n";
	print OUT "\n";
	print OUT "\n";
	print OUT "\n";
	print OUT "\n";
	print OUT "\n";
	print OUT "\n";

	# ��ν񤭤���
	my($i);
	foreach $i (0..$islandNumber) {
		writeIsland($Hislands[$i], $num, 1);
	}
	# �ե�������Ĥ���
	close(OUT);

	# ����
	if($HoceanMode && ($num >= -2)) {
		open(IOUT, ">${HdirName}/worldtmp.${HsubData}");
		writeLand(*IOUT, $Hworld->{'land'}, $Hworld->{'landValue'}, $Hworld->{'landValue2'}, { 'x' => \@defaultX, 'y' => \@defaultY });
		close(IOUT);
		unlink("${HdirName}/world.${HsubData}");
		rename("${HdirName}/worldtmp.${HsubData}", "${HdirName}/world.${HsubData}");
	}

	# Ʊ���ǡ����ν񤭹���
	writeAllyFile() if($HallyUse || $HarmisticeTurn || ($HmainMode eq 'asetup'));

	# �����̾���ˤ���
	unlink("${HdirName}/$HmainData");
	rename("${HdirName}/hakojima.tmp", "${HdirName}/$HmainData");
}

# ��ҤȤĽ񤭹���
sub writeIsland {
	my($island, $num, $mode) = @_;
	if($mode) {

		my $priority = $island->{'priority'};
		my $fleet = $island->{'fleet'};
		my @fnum = ('�裱', '�裲', '�裳', '�裴');
		foreach (0..3) {
			$fleet->[$_] = $fnum[$_] if($fleet->[$_] eq '');
			$priority->[$_] = "0-1-2-3-4-5-6-7" if($priority->[$_] eq '' || !$HusePriority);
		}

		my $fkind = $island->{'fkind'};
		my @flist = @$fkind;
		my @idx = (0..$#flist);
		@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
		@flist = @flist[@idx];

		$island->{'ext'}[1] = 0 if($island->{'allyId'}[0] eq '');

		print OUT $island->{'name'} . "\n";
		print OUT $island->{'owner'} . "\n";
		print OUT $island->{'birthday'} . "\n";
		print OUT $island->{'id'} . "\n";
		print OUT $island->{'prize'} . "\n";
		print OUT $island->{'absent'} . "," . $island->{'preab'} . "," . $island->{'comflag'} . "," . $island->{'earth'} . "\n";
		print OUT $island->{'comment'} . "\n";
		print OUT $island->{'password'} . "\n";
		print OUT $island->{'money'} . "\n";
		print OUT $island->{'food'} . "\n";
		print OUT $island->{'pop'} . "\n";
		print OUT $island->{'area'} . "\n";
		print OUT $island->{'farm'} . "\n";
		print OUT $island->{'factory'} . "\n";
		print OUT $island->{'mountain'} . "\n";
		print OUT join(',', @{$island->{'amity'}}) . "\n";
		print OUT join(',', @$fleet) . "\n";
		print OUT join(',', @$priority) . "\n";
		print OUT join(',', @flist) . "\n";
		print OUT $island->{'gain'} . "\n";
		print OUT $island->{'monsterkill'} . "\n";
		print OUT $island->{'monsterlive'} . "\n";
		print OUT join(',', @{$island->{'sink'}}) . "-" . join(',', @{$island->{'sinkself'}}) . "-" . join(',', @{$island->{'subSink'}}) . "-" . join(',', @{$island->{'subSinkself'}}) . "\n";
		print OUT join(',', @{$island->{'ext'}}) . "<>" . join(',', @{$island->{'subExt'}}) . "\n";
		print OUT $island->{'field'} . "\n";
		print OUT join(',', @{$island->{'item'}}) . "\n";
		print OUT join(',', @{$island->{'weather'}}) . "\n";
		print OUT $island->{'fight_id'} . "," . $island->{'rest'} . "\n";
		print OUT join(',', @{$island->{'event'}}) . "\n";
		print OUT $island->{'point'} . "\n";
		print OUT join(',', @{$island->{'defeat'}}) . "\n";
		my(@epoint);
		foreach (keys %{$island->{'epoint'}}){
			push(@epoint, "$_,$island->{'epoint'}{$_}");
		}
		print OUT join(',', @epoint) . "\n";
		print OUT join(',', @{$island->{'map'}->{'x'}}) . "<>" . join(',', @{$island->{'map'}->{'y'}}) . "<>" . $island->{'wmap'}->{'x'} . "<>" . $island->{'wmap'}->{'y'} . "\n";
		print OUT join('<>', @{$island->{'move'}}) . "\n";
		print OUT "\n";
		print OUT "\n";
	}

	my $id = $island->{'id'};
	# �Ϸ�
	if(!$HoceanMode && (($num == -1) || ($num == -2) || ($num == $id))) {
		my($land, $landValue, $landValue2, $map);
		$land = $island->{'land'};
		$landValue = $island->{'landValue'};
		$landValue2 = $island->{'landValue2'};
		$map = $island->{'map'};

		open(IOUT, ">${HdirName}/${id}tmp.${HsubData}");
		writeLand(*IOUT, $land, $landValue, $landValue2, $map);
		close(IOUT);
		unlink("${HdirName}/${id}.${HsubData}");
		rename("${HdirName}/${id}tmp.${HsubData}", "${HdirName}/${id}.${HsubData}");
	}
	# ���ޥ��
	if(($num == -1) || ($num == -3) || ($num == $id)) {
		if($HmainMode eq 'commandJava' || $HmainMode eq 'command2' || $HmainMode eq 'turn' || $HmainMode eq 'command' || $HmainMode eq 'new' || $HmainMode eq 'reload' || $HmainMode eq 'bfield') {
			writeCommand($id, $island->{'command'});
		}
	}
	# ������Ǽ���
	if(($num == -4) || ($num == $id)) {
		if($HmainMode eq 'lbbs' || $HmainMode eq 'new' || $HmainMode eq 'reload' || $HmainMode eq 'bfield') {
			writeLbbs($id, $island->{'lbbs'});
		}
	}
}

# �Ϸ��񤭹���
sub writeLand {
	local(*FH, $land, $landValue, $landValue2, $map) = @_;
	my($x, $y);
	foreach $y (sort { $a <=> $b } @{$map->{'y'}}) {
		foreach $x (sort { $a <=> $b } @{$map->{'x'}}) {
			printf FH ("%02x%08x%08x", $land->[$x][$y], $landValue->[$x][$y], $landValue2->[$x][$y]);
		}
		print FH "\n";
	}
}

# ���ޥ�ɽ񤭹���
sub writeCommand {
	my($id, $command) = @_;
	my($i);
	open(COUT, ">${HdirName}/${id}tmp.${HcommandData}");
	for($i = 0; $i < $HcommandMax; $i++) {
		printf COUT ("%d,%d,%d,%d,%d,%d\n", 
			$command->[$i]->{'kind'},
			$command->[$i]->{'target'},
			$command->[$i]->{'x'},
			$command->[$i]->{'y'},
			$command->[$i]->{'arg'},
			$command->[$i]->{'target2'}
		);
	}
	close(COUT);
	unlink("${HdirName}/${id}.${HcommandData}");
	rename("${HdirName}/${id}tmp.${HcommandData}", "${HdirName}/${id}.${HcommandData}");
}

# ������Ǽ��Ľ񤭹���
sub writeLbbs {
	my($id, $lbbs) = @_;
	while ($HlbbsMax < @$lbbs) { pop @$lbbs; }
#	open(LOUT, ">${HlogdirName}/${id}tmp.${HlbbsData}");
	open(LOUT, ">${HlogdirName}/${id}.${HlbbsData}");
	foreach (@$lbbs) {
		next if($_ eq '0<<0>>' || $_ eq '');
		print LOUT $_ . "\n";
	}
	close(LOUT);
#	unlink("${HlogdirName}/${id}.${HlbbsData}");
#	rename("${HlogdirName}/${id}tmp.${HlbbsData}", "${HlogdirName}/${id}.${HlbbsData}");
}

# ���ǻ��ǡ����ե�����������
sub deleteIslandData {
	my($island) = @_;
	my($id) = $island->{'id'};
	if(!$HoceanMode) {
		unlink("${HdirName}/${id}.${HsubData}");
		unlink("${HdirName}/${id}.${HcommandData}");
		unlink("${HlogdirName}/${id}.${HlbbsData}");
	} else {
		# ���˽����
		foreach $y (@{$island->{'map'}->{'y'}}) {
			foreach $x (@{$island->{'map'}->{'x'}}) {
				$island->{'land'}[$x][$y] = $HlandSea;
				$island->{'landValue'}[$x][$y] = 0;
			}
		}
	}
#HdebugOut("$island->{'id'} : $island->{'wmap'}->{'x'} ,  $island->{'wmap'}->{'y'}\n");
#HdebugOut("@{$island->{'map'}->{'x'}}\n");
#HdebugOut("@{$island->{'map'}->{'y'}}\n");
#		foreach $y (@defaultY) {
#			foreach $x (@defaultX) {
#				$d = sprintf("%02x%08x", $island->{'land'}[$x][$y], $island->{'landValue'}[$x][$y]);
#HdebugOut("$d");
#			}
#HdebugOut("\n");
#		}
}

# ��Ʈ���ֳ��ϻ�����ξ��֤���¸(�ȡ��ʥ���)
# mode 0:����������¸ 1:�����ʳ�����¸
# ***�ԼԤλ��ǻ���¸ island_save($island, $HfightdirName, 'lose', 0);
# ***mode 0��������¸ island_save($island, $HsavedirName, 'save', 0);
# ***mode 1��������¸ island_save($island, $HsavedirName, 'save', 1, \@land, \@landValue);(���ɥǡ������Ϥ�)
sub island_save {
	my($island, $dir, $suf, $mode, $oldland, $oldlandValue) = @_;
	my($id) = $island->{'id'};

	my $land = $island->{'land'}; # ���ߤ��Ϸ�
	my $landValue = $island->{'landValue'};
	my $map = $island->{'map'};
	my($x, $y);
	my(@saveland, @savelandValue, @stack); # ��¸�����Ϸ��ǡ�������
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			if($mode && ($land->[$x][$y] == $HlandNavy)) {
				# ��¸�ǡ����Τޤ�
				if($oldland->[$x][$y] == $HlandNavy) {
					$saveland[$x][$y] = $oldland->[$x][$y];
					$savelandValue[$x][$y] = $oldlandValue->[$x][$y];
				} else {
					my $nSea = (navyUnpack($island->{'landValue'}[$x][$y]))[3];
					$saveland[$x][$y] = $HlandSea;
					$savelandValue[$x][$y] = $oldlandValue->[$x][$y];
				}
			} elsif($mode && ($oldland->[$x][$y] == $HlandNavy)) {
				if(($land[$x][$y] == $HlandSea) || ($land[$x][$y] == $HlandNavy)) {
					# ��¸�ǡ����Τޤ�
					$saveland[$x][$y] = $oldland->[$x][$y];
					$savelandValue[$x][$y] = $oldlandValue->[$x][$y];
				} else {
					# �Ȥꤢ�����������Ϸ�
					$saveland[$x][$y] = $land->[$x][$y];
					$savelandValue[$x][$y] = $landValue->[$x][$y];
					push(@stack, { 'x' => $x, 'y' => $y });
				}
			} elsif((@stack > 0) && (($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy))) {
				my $point = shift(@stack);
				$saveland[$x][$y] = $oldland->[$point->{'x'}][$point->{'y'}];
				$savelandValue[$x][$y] = $oldlandValue->[$point->{'x'}][$point->{'y'}];
			} else {
				$saveland[$x][$y] = $land->[$x][$y];
				$savelandValue[$x][$y] = $landValue->[$x][$y];
			}
		}
	}
	# �����å��Ϸ�������Ф���٥롼��
	if(@stack > 0) {
		foreach $y (@{$map->{'y'}}) {
			last if(!@stack);
			foreach $x (@{$map->{'x'}}) {
				last if(!@stack);
				if(($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy)) {
					my $point = shift(@stack);
					$saveland[$x][$y] = $oldland->[$point->{'x'}][$point->{'y'}];
					$savelandValue[$x][$y] = $oldlandValue->[$point->{'x'}][$point->{'y'}];
				}
			}
		}
	}

	# ��¸�ǥ��ꥯ�ȥ�Υ����å�
	if(!opendir(DIN, "${dir}/")) {
		mkdir("${dir}", $HdirMode);
	} else {
		closedir(DIN);
	}

	open(OUT, ">${dir}/${id}tmp_${suf}.${HsubData}");
	writeIsland($island, 0, 1);
	writeLand(*OUT, \@saveland, \@savelandValue, \@savelandValue2, $map);
	close(OUT);
	unlink("${dir}/${id}_${suf}.${HsubData}");
	rename("${dir}/${id}tmp_${suf}.${HsubData}", "${dir}/${id}_${suf}.${HsubData}");
}

# ��¸������ξ��֤�����(�ȡ��ʥ���)
# mode 0:������������ 1:���ǡ�������¸�塤������������
# mode 2:�����ʳ����� 3:���ǡ���(�����ʳ�)��¸�塤�����ʳ�����
# mode -1:�ȡ��ʥ������ﾡ�����Ϸ�����������
sub island_load {
	my($island, $mode) = @_;
	my($id) = $island->{'id'};

	open(IIN, "${HsavedirName}/${id}_save.${HsubData}");
	chomp(my @line = <IIN>);
	close(IIN);

	my(@tmp) = splice(@line, 0, 36);
	my(@mandf) = splice(@tmp, 8, 25);
	my($money) = shift(@mandf); # ���
	my($food) = shift(@mandf);  # ����
#	my($tmp) = pop(@mandf);     # �ޥå�
#	my(@xytmp) = split(/<>/, $tmp);
#	my(@x) = split(/\,/, $xytmp[0]);
#	my(@y) = split(/\,/, $xytmp[1]);
#	my $map = { 'x' => \@x, 'y' => \@y };
#	# 7.12�����Υǡ����Τ���ν���
#	$map = $island->{'map'} if(!@x || !@y);
#	$island->{'map'} = $map;
	$map = $island->{'map'};

	# ���ɤ������ǡ���
 	my($land, $landValue, $landValue2) = readLand($map, @line);

	if($mode == 1) {
		island_save($island, $HsavedirName, 'save', 0);
	} elsif($mode == 3) {
		island_save($island, $HsavedirName, 'save', 1, $land, $landValue);
	}

	my(@loadland, @loadlandValue, @stack); # ���ɤ����Ϸ��ǡ�������
	if($HoceanMode) {
		@loadland = @{$island->{'land'}};
		@loadlandValue = @{$island->{'landValue'}};
		@loadlandValue2 = @{$island->{'landValue2'}};
	}
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			if(($mode > 1) && ($island->{'land'}[$x][$y] == $HlandNavy)) { # $island->{'land'} �����Ϸ�(�����֤���)
				if(($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy)) {
					# ���Τޤ�
					$loadland[$x][$y] = $island->{'land'}[$x][$y];
					$loadlandValue[$x][$y] = $island->{'landValue'}[$x][$y];
					$loadlandValue2[$x][$y] = $island->{'landValue2'}[$x][$y];
				} else {
					# �Ȥꤢ���������Ϸ�
					$loadland[$x][$y] = $land->[$x][$y];
					$loadlandValue[$x][$y] = $landValue->[$x][$y];
					push(@stack, { 'x' => $x, 'y' => $y });
				}
			} elsif(($mode > 1) && ($land->[$x][$y] == $HlandNavy)) {
				if($island->{'land'}[$x][$y] == $HlandNavy) {
					# ���Τޤ�
					$loadland[$x][$y] = $island->{'land'}[$x][$y];
					$loadlandValue[$x][$y] = $island->{'landValue'}[$x][$y];
					$loadlandValue2[$x][$y] = $island->{'landValue2'}[$x][$y];
				} else {
					my $nSea = (navyUnpack($landValue->[$x][$y]))[3];
					$loadland[$x][$y] = $HlandSea;
					$loadlandValue[$x][$y] = $nSea;
				}
			} elsif((@stack > 0) && (($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy))) {
				my $point = shift(@stack);
				$loadland[$x][$y] = $island->{'land'}[$point->{'x'}][$point->{'y'}];
				$loadlandValue[$x][$y] = $island->{'landValue'}[$point->{'x'}][$point->{'y'}];
				$loadlandValue2[$x][$y] = $island->{'landValue2'}[$point->{'x'}][$point->{'y'}];
			} else {
				$loadland[$x][$y] = $land->[$x][$y];
				$loadlandValue[$x][$y] = $landValue->[$x][$y];
				$loadlandValue2[$x][$y] = $landValue2->[$x][$y];
			}
		}
	}
	# �����å��Ϸ�������Ф���٥롼��
	if(@stack > 0) {
		foreach $y (@{$map->{'y'}}) {
			last if(!@stack);
			foreach $x (@{$map->{'x'}}) {
				last if(!@stack);
				if(($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy)) {
					my $point = shift(@stack);
					$loadland[$x][$y] = $island->{'land'}[$point->{'x'}][$point->{'y'}];
					$loadlandValue[$x][$y] = $island->{'landValue'}[$point->{'x'}][$point->{'y'}];
					$loadlandValue2[$x][$y] = $island->{'landValue2'}[$point->{'x'}][$point->{'y'}];
				}
			}
		}
	}

	$island->{'money'} = $money; # ���
	$island->{'food'} = $food;   # ����
	$island->{'map'} = $map;     # �ޥå�
	$island->{'land'} = \@loadland;
	$island->{'landValue'} = \@loadlandValue;
	$island->{'landValue2'} = \@loadlandValue2;

	if($mode >= 0) {
		foreach $i (0..$islandNumber) {
			undef $Hislands[$i]->{'fkind'};
		}
		foreach $i (0..$islandNumber) {
			estimateNavy($i);
		}
		writeIslandsFile(-2);
	}
}

#----------------------------------------------------------------------
# Ʊ���ǡ���������
#----------------------------------------------------------------------
# Ʊ���ǡ����ɤߤ���
sub readAllyFile {
	# �ǡ����ե�����򳫤�
	if(!open(IN, "${HdirName}/${HallyData}")) {
		rename("${HdirName}/ally.tmp", "${HdirName}/${HallyData}");
		if(!open(IN, "${HdirName}/${HallyData}")) {
			return 0;
		}
	}

	# Ʊ�����ɤߤ���
	my($i);
	$HallyNumber   = int(<IN>); # Ʊ�������
	for ($i = 0; $i < $HallyNumber; $i++) {
		$Hally[$i] = readAlly();
		$HidToAllyNumber{$Hally[$i]->{'id'}} = $i;
	}
	# �������Ƥ���Ʊ����ID���Ǽ
	for ($i = 0; $i < $HallyNumber; $i++) {
		my $member  = $Hally[$i]->{'memberId'};
		foreach (@$member) {
			my $n = $HidToNumber{$_};
			next unless(defined $n);
			push(@{$Hislands[$n]->{'allyId'}}, $Hally[$i]->{'id'});
		}
	}

	# �ե�������Ĥ���
	close(IN);

	return 1;
}

# Ʊ���ҤȤ��ɤߤ���
sub readAlly {
	my($name, $mark, $color, $id, $ownerName, $password, $jpass, $score, $number,
		$occupation, $tmp, @allymember, @ext, $comment, $title, $message, @veto, $vkind);
	chomp($name = <IN>);  # Ʊ����̾��
	chomp($mark = <IN>);  # Ʊ���μ��̥ޡ���
	chomp($color = <IN>); # ���̥ޡ����ο�
	$id = int<IN>;        # Ʊ��ID�ʼ�żԤΤ�ΤȰ���
	chomp($ownerName = <IN>); # ��żԤ����̾��
	chomp($password = <IN>);  # �ѥ���ɡʼ�żԤΤ�ΤȰ���
	chomp($jpass = <IN>);     # �ѥ���ɡ�Takayan��jpass:�����󹹿����˽񤭴�����
	$score = int(<IN>);       # Ʊ���Υ�����
	$number = int(<IN>);      # Ʊ����°������ο�
	$occupation = int(<IN>);  # ��ͭΨ
	chomp($tmp = <IN>);       # Ʊ����°��ID
	@allymember = split(/\,/,$tmp);
	chomp($tmp = <IN>);       # ��ĥ�ΰ�
	@ext = split(/\,/,$tmp);
	#$name = $HwinnerMark . $name if($ext[5]);
	chomp($comment = <IN>);   # ������
	chomp(($title, $message) = split('<>', <IN>)); # �����ȥ�,��å�����
	chomp($tmp = <IN>);       # ����ID
	@veto = split(/\,/,$tmp);
	$vkind = shift @veto;
	<IN>; # ͽ��
	<IN>; # ͽ��

	# �رķ��ˤ����֤�
	return {
		'name' => $name,
		'mark' => $mark,
		'color' => $color,
		'id' => $id,
		'oName' => $ownerName,
		'password' => $password,
		'Takayan' => $jpass,
		'score' => $score,
		'number' => $number,
		'occupation' => $occupation,
		'memberId' => \@allymember,
		'ext' => \@ext,
		'comment' => $comment,
		'title' => $title,
		'message' => $message,
		'vetoId' => \@veto,
		'vkind' => $vkind,
	};
}

# Ʊ���ǡ����񤭹���
sub writeAllyFile {
	# �ե�����򳫤�
	open(OUT, ">${HdirName}/ally.tmp");

	# �رĥǡ����ν񤭤���
	print OUT "$HallyNumber\n";
	for($i = 0; $i < $HallyNumber; $i++) {
		writeAlly($Hally[$i]);
	}
	# �ե�������Ĥ���
	close(OUT);

	# �����̾���ˤ���
	unlink("${HdirName}/${HallyData}");
	rename("${HdirName}/ally.tmp", "${HdirName}/${HallyData}");
}

# Ʊ���ҤȤĽ񤭹���
sub writeAlly {
	my($ally) = @_;
	print OUT $ally->{'name'} . "\n";
	print OUT $ally->{'mark'} . "\n";
	print OUT $ally->{'color'} . "\n";
	print OUT $ally->{'id'} . "\n";
	print OUT $ally->{'oName'} . "\n";
	print OUT $ally->{'password'} . "\n";
	print OUT $ally->{'Takayan'} . "\n";
	print OUT $ally->{'score'} . "\n";
	print OUT $ally->{'number'} . "\n";
	print OUT $ally->{'occupation'} . "\n";
	my $memId = $ally->{'memberId'};
	print OUT join(',', @$memId) . "\n";
	#��ĥ�ΰ�
	my $ext = $ally->{'ext'};
	print OUT join(',', @$ext) . "\n";
	print OUT $ally->{'comment'} . "\n";
	print OUT $ally->{'title'} . '<>' . $ally->{'message'} . "\n";
	my @vetoId = @{$ally->{'vetoId'}};
	unshift(@vetoId, $ally->{'vkind'});
	print OUT join(',', @vetoId) . "\n";
	print OUT "\n";
	print OUT "\n";
}

# [a-zA-Z]�ǹ��������8ʸ���Υѥ���ɤ���
sub makeRandomString {
	my($baseString) = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	my($baseLen) = length($baseString);
	my($i, $passward);

	foreach $i (1..8) {
		$passward .= substr($baseString, rand($baseLen), 1);
	}

	return $passward;
}

# Ʊ������ͭΨ�η׻�
sub allyOccupy {
	my($i);
	my($totalScore) = 0;
	return if(!$HallyNumber);

	for ($i = 0; $i < $HallyNumber; $i++) {
		$totalScore += $Hally[$i]->{'score'};
	}
	for ($i = 0; $i < $HallyNumber; $i++) {
		if ($totalScore != 0) {
			$Hally[$i]->{'occupation'} = int($Hally[$i]->{'score'} / $totalScore * 100);
		} else {
			$Hally[$i]->{'occupation'} = int(100 / $HallyNumber);
		}
	}
	return;
}

# �������λ���Ʊ����Ϣ����
sub islandDeadAlly {
	my($island, $id, $name) = @_;

	$id   = $island->{'id'}   if($id eq '');
	$name = $island->{'name'} . $AfterName if($name eq '');
	my $n = $HidToAllyNumber{$id};
	if(($HarmisticeTurn && $HcampDeleteRule && ($HautoKeeper != 1)) || (defined $n)) {
		if(($HarmisticeTurn && $HcampDeleteRule && ($HautoKeeper != 1)) ||
			(!$HarmisticeTurn && $HallyAutoBreakup) ||
			($Hally[$n]->{'number'} == 1)) {
			make_pastlog($id, $name) if($HallyAutoBreakup == 2);
			$Hally[$n]->{'dead'} = 1;
			undef $island->{'allyId'};
			$HidToAllyNumber{$id} = undef;
			$HallyNumber--;
			allySort();
		}
	} else {
		make_pastlog($id, $name) if($HallyAutoBreakup == 2);
		foreach (@{$island->{'allyId'}}) {
			my $i = $HidToAllyNumber{$_};
			my $allyMember = $Hally[$i]->{'memberId'};
			my @newAllyMember = ();
			foreach (@$allyMember) {
				if(!(defined $HidToNumber{$_})) {
				} elsif($_ == $id) {
					$Hally[$i]->{'score'} -= $island->{$HrankKind} if(!$island->{'predelete'});
					$Hally[$i]->{'number'} -= 1;
				} else {
					push(@newAllyMember, $_);
				}
			}
			$Hally[$i]->{'memberId'} = \@newAllyMember;
		}
		undef $island->{'allyId'};
	}
}

#----------------------------------------
# ��������(YY-BBS)
#----------------------------------------
sub make_pastlog {
	my($id, $name) = @_;
	# ���ե�����
	my $logfile = "${HbbsdirName}/${id}$Hlogfile_name";
	return if !(-f $logfile);
	open(IN,"$logfile")  || die $!;
	my $top = <IN>;
	close(IN);
	my $allyName = (split(/<>/, $top))[3];
	$allyName =~ s/�����ļ�//;
	my $logfileNew = "${HbbsdirName}/${id}-${HislandTurn}$Hlogfile_name";
#	return if !(-f $logfile);
	rename($logfile, $logfileNew);
	# ������ե�����
	my $logfile2 = "${HbbsdirName}/${id}$Hlogfile2_name";
	my $logfile2New = "${HbbsdirName}/${id}-${HislandTurn}$Hlogfile2_name";
	return if !(-f $logfile2);
	rename($logfile2, $logfile2New);
	# �����󥿥ե�����
	if($Hcounter) {
		my $cntfile = "${HbbsdirName}/${id}$Hcntfile_name";
		my $cntfileNew = "${HbbsdirName}/${id}-${HislandTurn}$Hcntfile_name";
		return if !(-f $cntfile);
		rename($cntfile, $cntfileNew);
	}
	# ������NO�ե�����
	if($Hpastkey) {
		my $nofile  = "${HbbsdirName}/${id}$Hnofile_name";
		return if !(-f $nofile);
		# ���NO�򳫤�
		open(NO,"$nofile") || die $!;
		my $count = <NO>;
		close(NO);
		my $nofileNew  = "${HbbsdirName}/${id}-${HislandTurn}$Hnofile_name";
		rename($nofile, $nofileNew);
		foreach (1..$count) {
			my $pastfile = sprintf("%s/%04d\.%d\.cgi", $HpastdirName,$_,$id);
			my $pastfileNew = sprintf("%s/%04d\.%d-%d\.cgi", $HpastdirName,$_,$id,$HislandTurn);
			rename($pastfile, $pastfileNew);
		}
	}
	# ���Ǥ���Ʊ���Υǡ�������¸
	my(@lines);
	if(!open(IN, "${HbbsdirName}/dead${HallyData}")) {
		@lines = ();
	} else {
		@lines = <IN>;
		close(IN);
	}
	unshift(@lines, "${id}-${HislandTurn},$allyName,${name}\n");
	open(OUT, ">${HbbsdirName}/dead${HallyData}");
	print OUT @lines;
	close(OUT);
	
	return 1;
}

# ��̾���֤�
sub islandName {
	my($island) = @_;

	my($name);
#	$name = $HwinnerMark if($island->{'ext'}[0] || ($HitemComplete == $island->{'id'}));
#	if($HitemComplete == $island->{'id'}) {
#		$name = $HwinnerMark[0];
#	}
#	if($island->{'ext'}[0]) {
#		my $f = 2;
#		foreach (1..$#HwinnerMark) {
#			$name .= $HwinnerMark[$_] if($island->{'ext'}[0] & $f);
#			$f *= 2;
#		}
#	}
	foreach (@{$island->{'allyId'}}) {
		my $i = $HidToAllyNumber{$_};
		my $mark  = $Hally[$i]->{'mark'};
		my $color = $Hally[$i]->{'color'};
		$name .= '<FONT COLOR="' . $color . '"><B>' . $mark . '</B></FONT>';
	}
	$name .= $island->{'name'} . $AfterName;

	return ($name);
}

# �Ϸ��θƤ���
sub landName {
	my($land, $lv) = @_;
	if(($land == $HlandSea) || ($land == $HlandWaste)) {
		return $HlandName[$land][$lv];
	} elsif($land == $HlandTown) {
		foreach (reverse(0..$#HlandTownValue)) {
			if($HlandTownValue[$_] <= $lv) {
				return $HlandTownName[$_];
			}
		}
	} elsif($land == $HlandDefence) {
		if($HdurableDef){
			$lv++;
			if($lv >= $HdefLevelUp) {
				return $HlandName[$land][1];
			}
		}
		return $HlandName[$land][0];
	} elsif($land == $HlandComplex) {
		# ʣ���Ϸ�
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		return $HcomplexName[$cKind];
	} elsif($land == $HlandMonster) {
		# ����
		my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$mKind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$mId}]) if (defined $HidToNumber{$mId});
		$mName .= "(${name})" if (defined $name);
		return $mName;
	} elsif($land == $HlandHugeMonster) {
		# �������
		my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$mKind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$mId}]) if (defined $HidToNumber{$mId});
		$mName .= "(${name})" if (defined $name);
		return $mName;
	} elsif($land == $HlandNavy) {
		# ����
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($lv);
		my $nName = $HnavyName[$nKind];
		$nName .= '�λĳ�' if($nFlag == 1);
		my($name);
		$name = islandName($Hislands[$HidToNumber{$nId}]) if (defined $HidToNumber{$nId});
		my $nSpecial = $HnavySpecial[$nKind];
		if(!($nSpecial & 0x8) && !($nFlag & 1)) {
			if(defined $HidToName{$nId}) {
				$nName .= "(${name})";
			} else {
				$nName .= "(��°����)";
			}
		}
		return $nName;
	} elsif($land == $HlandMountain) {
		my $mlv = ($lv > 0) ? 1 : 0;
		return $HlandName[$land][$mlv];
	} elsif($land == $HlandMonument) {
		return $HmonumentName[$lv];
	} elsif($land == $HlandCore) {
		my $lFlag = int($lv / 10000);
		return $HlandName[$land][$lFlag];
	} elsif($land == $HlandResource) {
		return $HlandName[$land][$lv];
	} else {
		return $HlandName[$land];
	}
}

# �ϰ���η�����ᤤ���õ���ƺ�ɸ���֤���$range��0�ξ�硢����12(20)�إå�����Ĵ���塢����Ĵ����
sub searchNavyPort {
	my($island, $x, $y, $range, $plane, $id) = @_; #$plane�ե饰�ȥ����ʡ��ե饰���ɲ�
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my($count, $sx, $sy, $i);
	$count = 0;
	if($range) {
		$range--;
	} else {
		$range = $an[$#an] - 1;
	}
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0) || ($HoceanMode && ($HlandID[$sx][$sy] != $island->{'id'})));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nFlag, $nKind, $nWait) = (navyUnpack($landValue->[$sx][$sy]))[0, 5, 7, 8];
			my $nSpecial = $HnavySpecial[$nKind];

                        # �Ҷ����ե饰Ω�äƤʤ����Ϲ����� Ω�äƤ������⸫�ơ�ȯ�ϥե饰���ǧ
                        if($plane == 0){
    			    if(($nSpecial & 0x8) && ($nFlag != 3) && ($nId == $id)){
			  	    $count = 1;
				    last;
                            }
			} else {
    			    if((($nSpecial & 0x8) || ($nKind == 12)) && ($nFlag == 0) && ($nWait == 0) && ($nId == $id)) {
			  	    $count = 1;
				    last;
                            }
                        }
		}
	}
	if(!$count && ($range == $an[$#an] - 1)) {
		foreach $i (0..$island->{'pnum'}) {
			$sx = $island->{'rpx'}[$i];
			$sy = $island->{'rpy'}[$i];
			next if($HoceanMode && ($HlandID[$sx][$sy] != $island->{'id'})); # ǰ�Τ���
			if($land->[$sx][$sy] == $HlandNavy) {
				my($nId, $nKind) = (navyUnpack($landValue->[$sx][$sy]))[0, 7];
				my $nSpecial = $HnavySpecial[$nKind];
				if($nSpecial & 0x8) {
					$count = 1;
					last;
				}
			}
		}
	}
	return ($count, $sx, $sy);
}


# ���Ϥ���Φ�Ϥ������
sub searchLand {
	my($island, $x, $y) = @_;
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my ($sx, $sy, $i);
        my $count = 0;
	for($i == 1; $i <= 6; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0) || ($HoceanMode && ($HlandID[$sx][$sy] != $island->{'id'})));

		if(($land->[$sx][$sy] == $HlandWaste) ||
                   ($land->[$sx][$sy] == $HlandPlains) ||
                   ($land->[$sx][$sy] == $HlandTown) ||
                   ($land->[$sx][$sy] == $HlandForest) ||
                   ($land->[$sx][$sy] == $HlandFarm)  ||
                   ($land->[$sx][$sy] == $HlandFactory) ||
                   ($land->[$sx][$sy] == $HlandBase) ||
                   ($land->[$sx][$sy] == $HlandDefence) ||
                   ($land->[$sx][$sy] == $HlandMountain) ||
                   ($land->[$sx][$sy] == $HlandMonument) ||
                   ($land->[$sx][$sy] == $HlandHaribote) ||
                   ($land->[$sx][$sy] == $HlandComplex)) {
                    $count ++;
		}
	}
	return ($count);
}

# ��Τʤ���ɸ���������֤�
sub randomIslandMap {
	my($x, $y, @pos);

	for ($x = 0; $x < $HoceanSizeX; $x++) {
		for ($y = 0; $y < $HoceanSizeY; $y++) {
			next if($HoceanMap[$x][$y]);
			push(@pos, { 'x' => $x, 'y' => $y });
		}
	}

	return $pos[int(rand($#pos + 1))];
}

# ��Ʊ�ΤΤĤʤ����Ĵ�٤�ᥤ��
sub makeRen {
	# @correct����($correct[$sx + $#an])
	my(@ax) = (0..($HoceanSizeX - 1));
	my(@ay) = (0..($HoceanSizeY - 1));
	if($Hroundmode){
		@RcorrectX = ($ax[$#ax], @ax, $ax[0]);
		@RcorrectY = ($ay[$#ay], @ay, $ay[0]);
	} else {
		@RcorrectX = (-1, @ax, -1);
		@RcorrectY = (-1, @ay, -1);
	}
	my($x, $y);
	my $ren = -1;
	foreach $y (@ay) {
		foreach $x (@ax) {
			if($HoceanMap[$x][$y]) { # �礬����
				my($num) = $HidToNumber{$HoceanMap[$x][$y]};
				if((defined $num) &&
					( # ��³���ʤ���
					$Hislands[$num]->{'predelete'} ||  # �����ͤ�������
					$Hislands[$num]->{'rest'} || # ���ﾡ
					($HfieldUnconnect && $Hislands[$num]->{'field'}) # ��������Хȥ�ե������
					)
					) { 
					$HislandConnect[$x][$y] = $ren--;
					next;
				}
			}
			$HislandConnect[$x][$y] = 0;
		}
	}
	$ren = 1;
	foreach $y (@ay) {
		foreach $x (@ax) {
			if(classRen($x, $y, $ren)) {
				$ren++;
			}
		}
	}

#foreach $y (@ay) {
#	foreach $x (@ax) {
#		HdebugOut("$HislandConnect[$x][$y](${\int($HoceanMap[$x][$y])}),");
#	}
#	HdebugOut("\n");
#}
}

# ��Ʊ�ΤΤĤʤ����Ĵ�٤륵��
sub classRen {
	my($x, $y, $ren) = @_;
	return if(!$HoceanMap[$x][$y]); # ̤�Τγ���
	return if($HislandConnect[$x][$y]); # Ĵ���Ѥ�
	$HislandConnect[$x][$y] = $ren;
	my($sx, $sy);
	my(@check) = ([-1, 0], [1, 0], [0, -1], [0, 1]); # ���������塤��
	if(!($HislandSizeY % 2)) {
		push(@check, [-1, 1]);  # ����
		push(@check, [1, -1]);  # ����
	} elsif(!($HoceanSizeY % 2)) {
		if($y % 2) {
			push(@check, [-1, -1]); # ����
			push(@check, [-1, 1]);  # ����
		} else {
			push(@check, [1, -1]);  # ����
			push(@check, [1, 1]);   # ����
		}
	} else {
		if($y % 2) {
			push(@check, [-1, -1]); # ����
			push(@check, [-1, 1]) if($y < $HoceanSizeY - 1);  # ����
		} else {
			push(@check, [1, -1]) if($y);  # ����
			push(@check, [1, 1]);   # ����
		}
	}
	foreach (@check) {
		$sx = $RcorrectX[$x + $_->[0] + 1];
		$sy = $RcorrectY[$y + $_->[1] + 1];
		next if (($sx < 0) || ($sy < 0));
		# �ϰ���ξ��
		classRen($sx, $sy, $ren);
	}
	return 1;
}

# ���ΤĤʤ����Ĵ�٤�ᥤ��
sub makeSeaRen {
	my($island, $map) = @_;
	my($land) = $island->{'land'};
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$island->{'seaconnect'}->[$x][$y] = 0;
		}
	}
	my $rensea = 1;
	my($x, $y);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			next if($island->{'seaconnect'}->[$x][$y]);
			if(classRen($land, $x, $y, $rensea)) {
				$rensea++;
			}
		}
	}
}

# ���ΤĤʤ����Ĵ�٤륵��
sub classSeaRen {
	my($land, $x, $y, $rensea) = @_;
	return if($island->{'seaconnect'}->[$x][$y] || ($land->[$x][$y] != $HlandSea));
	$island->{'seaconnect'}->[$x][$y] = $rensea;
	my($sx, $sy);
	foreach (1..6) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		next if (($sx < 0) || ($sy < 0));
		# �ϰ���ξ��
		classSeaRen($land, $sx, $sy, $rensea);
	}
	return 1;
}
#----------------------------------------------------------------------
# �Ϸ��ǡ���
#----------------------------------------------------------------------
# �Ϸ��ξ���� Unpack
sub landUnpack {
	my $lv = shift;

	# bit ��̣
	#-----------
	#  8  ͽ��
	#  5  ����
	#  9  ������ե饰
	#  6  �����ե饰
	#  6  ���ե饰
	my $money = $lv & 0x3f;  $lv >>= 6;
	my $food  = $lv & 0x3f;  $lv >>= 6;
	my $turn  = $lv & 0x1ff; $lv >>= 9;
	my $kind  = $lv & 0x1f; $lv >>= 5;
	my $tmp   = $lv & 0xff;

	return ($tmp, $kind, $turn, $food, $money);
}

# �Ϸ��ξ���� Pack
sub landPack {
	my($tmp, $kind, $turn, $food, $money) = @_;

	# bit ��̣
	#-----------
	#  8  ͽ��
	#  5  ����
	#  9  ������ե饰
	#  6  �����ե饰
	#  6  ���ե饰
	my $lv = 0;
	$lv |= $tmp   & 0xff;  $lv <<= 5;
	$lv |= $kind  & 0x1f;  $lv <<= 9;
	$lv |= $turn  & 0x1ff; $lv <<= 6;
	$lv |= $food  & 0x3f;  $lv <<= 6;
	$lv |= $money & 0x3f;

	return $lv;
}

# ���äξ���� Unpack
sub monsterUnpack {
	my $lv = shift;

	# bit ��̣
	#-----------
	#  8  ��ID
	#  3  ������åե饰
	#  1  �����ե饰
	#  8  �и���
	#  2  �ե饰
	#  5  ����
	#  5  �ѵ���
	my $hp    = $lv & 0x1f; $lv >>= 5;
	my $kind  = $lv & 0x1f; $lv >>= 5;
	my $flag  = $lv & 0x03; $lv >>= 2;
	my $exp   = $lv & 0xff; $lv >>= 8;
	my $sea   = $lv & 0x01; $lv >>= 1;
	my $hflag = $lv & 0x07; $lv >>= 3;
	my $id    = $lv;

	return ($id, $hflag, $sea, $exp, $flag, $kind, $hp);
}

# ���äξ���� Pack
sub monsterPack {
	my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = @_;

	# bit ��̣
	#-----------
	#  8  ��ID
	#  3  ������åե饰
	#  1  �����ե饰
	#  8  �и���
	#  2  �ե饰
	#  5  ����
	#  5  �ѵ���
	my $lv = 0;
	$lv |= $id    & 0xff; $lv <<= 3;
	$lv |= $hflag & 0x07; $lv <<= 1;
	$lv |= $sea   & 0x01; $lv <<= 8;
	$lv |= $exp   & 0xff;  $lv <<= 2;
	$lv |= $flag  & 0x03;  $lv <<= 5;
	$lv |= $kind  & 0x1f;  $lv <<= 5;
	$lv |= $hp    & 0x1f;

	return $lv;
}

# �����ξ���� Unpack
sub navyUnpack {
        my ($lv, $lv2);
	$lv = shift;
        $lv2 = shift;

	# bit ��̣
	#-----------
	#  7  ��ID
	#  1  ͽ��
	#  2  ����
	#  1  �����ե饰
	#  8  �и���
	#  2  �ե饰
	#  2  �����ֹ�
	#  5  ����
	#  4  �ѵ���

	my $wait = $lv & 0x0f; $lv >>= 4;
	my $kind = $lv & 0x1f; $lv >>= 5;
	my $no   = $lv & 0x03; $lv >>= 2;
	my $flag = $lv & 0x03; $lv >>= 2;
	my $exp  = $lv & 0xff; $lv >>= 8;
	my $sea  = $lv & 0x01; $lv >>= 1;
	my $stat = $lv & 0x03; $lv >>= 2;
	my $temp = $lv & 0x01; $lv >>= 1;
	my $id   = $lv;


        $lv2 >>= 15;
        my $goaly = $lv2 & 0x1f; $lv2 >>= 5;
        my $goalx = $lv2 & 0x1f; $lv2 >>= 5;
        my $hp    = $lv2 & 0x7f;

	return ($id, $temp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly);
}

# �����ξ���� Pack
sub navyPack {
	my($id, $temp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = @_;

	# bit ��̣
	#-----------
	#  7  ��ID
	#  1  ͽ��
	#  2  ����
	#  1  �����ե饰
	#  8  �и���
	#  2  �ե饰
	#  2  �����ֹ�
	#  5  ����
	#  4  �ѵ���
	my $lv = 0;
        my $lv2 = 0;
	$lv |= $id   & 0x7f; $lv <<= 1;
	$lv |= $temp & 0x01; $lv <<= 2;
	$lv |= $stat & 0x03; $lv <<= 1;
	$lv |= $sea  & 0x01; $lv <<= 8;
	$lv |= $exp  & 0xff; $lv <<= 2;
	$lv |= $flag & 0x03; $lv <<= 2;
	$lv |= $no   & 0x03; $lv <<= 5;
	$lv |= $kind & 0x1f; $lv <<= 4;
        $lv |= $wait;

        $lv2 |= $hp    & 0x7f; $lv2 <<= 5;
        $lv2 |= $goalx & 0x1f; $lv2 <<= 5;
        $lv2 |= $goaly & 0x1f; $lv2 <<= 15;

	return ($lv, $lv2);
}

#----------------------------------------------------------------------
# �ѥ���ɥ����å�
#----------------------------------------------------------------------
sub checkPassword {
	my($island, $p2) = @_;
	my $p1 = $island->{'password'};

	# null�����å�
	if($p2 eq '') {
		return 0;
	}

	# �ޥ����ѥ���ɥ����å�
	if(checkMasterPassword($p2)) {
		return 2;
	}

	# ����Υ����å�
	if($p1 eq encode($p2)) {
		return 1;
	}

	if($island->{'preab'} && ($HmainMode ne 'preab') && ($HpassChangeOK || ($HmainMode ne 'change'))) {
		my $ally = $Hally[$HidToAllyNumber{$island->{'allyId'}[0]}];
		if($ally->{'Takayan'} eq $p2) {
			$Hcodevelope = 1;
			return 1;
		}
	}
	return 0;
}

# �ޥ����ѥ���ɤΥ����å�
sub checkMasterPassword {
	my $pass = shift;
	return (crypt($pass, 'ma') eq $HmasterPassword);
}

# �ü�ѥ���ɤΥ����å�
sub checkSpecialPassword {
	my $pass = shift;
	return (crypt($pass, 'sp') eq $HspecialPassword || crypt($pass, 'ma') eq $HmasterPassword);
}

# �ѥ���ɤΥ��󥳡���
sub encode {
	my $pass = shift;
	return ($cryptOn ? crypt($pass, 'h2') : $pass);
}

# �ѥ���ɴְ㤤
sub tempWrongPassword {
	if($HinputPassword eq '') {
		tempWrong("<span class=\"big\">�ѥ���ɤ�˺��Ƥ��ޤ��󤫡�</span>"); # �ѥ����̤����
		axeslog(1, 'NoPass error!') if($HtopAxes && $HtopAxes != 3);
		return;
	}
	axeslog(1, 'PASS error!') if($HtopAxes && $HtopAxes != 3);
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function init(){
}
function SelectList(theForm){
}
//-->
</SCRIPT>
<span class="big">�ѥ���ɤ��㤤�ޤ���
<A HREF=\"$HthisFile\">�ȥåפ����</span></A>
END
	if($HpassError) {
		my $agent   = $ENV{'HTTP_USER_AGENT'};
		my $addr    = $ENV{'REMOTE_ADDR'};
		my $host    = $ENV{'REMOTE_HOST'};
		if ($gethostbyaddr && (($host eq '') || ($host eq $addr))) {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
		} elsif($host eq '') {
			$host = $addr;
		}
		my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + $Hjst);
		my $day = ('��','��','��','��','��','��','��')[$wday];
		$year = $year + 1900;
		$mon = $mon + 1;
		my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
		out(<<END);
<HR>
<TABLE><TR><TH><span class="big">��${HtagDisaster_}���ٹ�${H_tagDisaster}��</span></TH></TR>
<TR><TD>���ʤ��ξ����Ͽ�����Ƥ��������ޤ�����
��$date<BR>��<B>$host - $addr - $agent</B>
</TD></TR>
<TR><TD class='N'>
<BR>��<A HREF='http://www.ipa.go.jp/security/ciadr/law199908.html' target='_blank'><B>�������������԰٤ζػ����˴ؤ���ˡΧ</B></A>��2001ǯ2��13���˻ܹԤ���ޤ�����
<BR><BR>������ˡΧ�ϡ��ϥ��ƥ��Ⱥ���ɻߤȹ��پ����̿��Ҳ�η�����ȯŸ����Ū�Ȥ�����Τǡ���ˡ�ǽ�ȳ�Ǥ��ʤ���ʬ���оݤȤ���ˡΧ�Ǥ���
<BR><BR>����ˡ�Ǥϡ����餫���ﳲ���Фʤ���ȳ���뤳�ȤϤǤ��ʤ��ä��ΤǤ������������������ػ�ˡ�Ǥϡ�
${HtagDisaster_}��������������Ԥä������ǽ�ȳ���оݤȤʤ�ޤ���${H_tagDisaster}
<BR><BR>���ºݤ�ˡΧ����ߺդ�����������ȡ�
��<A HREF='http://www.ipa.go.jp/security/ciadr/law199908.html#�������������԰�' target='_blank'><B>������������</B></A>�Ȥϡ�<B>�ѥ���������ݸ�줿�ΰ�ˡ����¤Τʤ���Τ�����˥����������뤳��</B>�٤ǡ�
����˰�ȿ������硢��${HtagDisaster_}Ĩ��ǯ�ʲ������ϡ��������߰ʲ���ȳ��${H_tagDisaster}�٤��ʤ����뤳�Ȥˤʤ�ޤ���
<BR><BR>��ñ�ʤ�֥ѥ���ɤ����ϥߥ��פǤ���Ф褤�ΤǤ��������ޤ�ˤ����ˤǤ���С�<B>�����ԤȤ�����������֤�Ȥ餶������ޤ���</B>
<BR><BR>��${HtagTH_}�����֤��ѥ���ɥ��顼��ȯ��������硢�������̤���ͳ������ΤǤ����顢���β��ˤ����󥯤ΡַǼ��ġפ⤷���ϡ֥᡼��פˤƤ�Ϣ���������ޤ��褦���ꤤ�������ޤ���${H_tagTH}
</TD></TR></TABLE>
END
	}
}

# ID�㤤or���������ꤷ�Ƥ��ʤ�or���å������ꤷ�Ƥ��ʤ�
sub tempWrong {
	my($str) = @_;

	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function init(){
}
function SelectList(theForm){
}
//-->
</SCRIPT>
${HtagBig_}$str${H_tagBig}$HtempBack
END
}
#----------------------------------------------------------------------
# ��������������
#----------------------------------------------------------------------
sub axeslog {
	my($mode, $error) = @_;

	# �֥��������ȥ�����ץƥ����ȼ����פؤ��б�
	# http://espion.s7.xrea.com/diary/20031027.html#p02 ���
	foreach (%ENV) {
		s/&(?!(?:amp|quot|lt|gt);)/&amp;/g;
		s/"/&quot;/g; #"
		s/'/&#x27;/g; #'
		s/ /&#32;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
	}

	my($agent, $addr, $host, $referer);
	$agent   = $ENV{'HTTP_USER_AGENT'};
	$addr    = $ENV{'REMOTE_ADDR'};
	$host    = $ENV{'REMOTE_HOST'};
	$referer = $ENV{'HTTP_REFERER'} if(!$mode);
	if (($host eq $addr) || ($host eq '')) {
		$host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr;
	}
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + $Hjst);
	my $day = ('��','��','��','��','��','��','��')[$wday];
	$year = $year + 1900;
	$mon = $mon + 1;
	my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
	my($pcheck);
	if($proxycheck) {
		my @proxy_env = (
			'HTTP_CACHE_CONTROL', # FORM��������no_cache�ˤʤ�ߤ���(��_��?
			'HTTP_CACHE_INFO',
			'HTTP_CLIENT_IP',
			'HTTP_FORWARDED',
			'HTTP_FROM',
			'HTTP_PROXY_CONNECTION',
			'HTTP_SP_HOST',
			'HTTP_VIA',
			'HTTP_X_FORWARDED_FOR',
			'HTTP_XONNECTION',
			'HTTP_XROXY_CONNECTION',
		);
		$pcheck = $ENV{'HTTP_CONNECTION'};
		foreach (@proxy_env){
			$pcheck .= '<>' . $ENV{$_};
		}
	}

	open(IN, "$HaxesLogfile");
	my @lines = <IN>;
	close(IN);

	while ($HaxesMax <= @lines) { pop @lines; }
	my $id;
	if($mode) {
		$id = ($defaultID eq $HcurrentID) ? $defaultID : "$defaultID=>$HcurrentID";
	} else {
		$id = $defaultID;
	}
	my($pass);
	$pass = $HinputPassword if(($error =~ /error/) || ($HtopAxes > 4));
	unshift(@lines, "[$date] - $referer - $host - $addr - $agent - $id - $pass - $error - $pcheck\n");

	if(open(OUT, ">$HaxesLogfile")){
		foreach $line (@lines) {
#			print OUT jcode::sjis($line); # jcode���ѻ�
			print OUT $line;
		}
		close(OUT);
	} else {
		tempProblem();
		return;
	}
}
#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------

# ɸ����Ϥؤν���
sub out {
#	print STDOUT jcode::sjis($_[0], 'euc'); # jcode���ѻ�
	print STDOUT $_[0];
}

# �ǥХå���
sub HdebugOut {
	if($Hdebug) {
		open(DOUT, ">>debug.log");
		print DOUT ($_[0]);
		close(DOUT);
	}
}

# ���֤μ���
sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($_[0] + $Hjst);
	$mon++;
	$year += 1900;
	my $timestring = sprintf("%04dǯ %02d�� %02d�� %02d��", $year, $mon, $date, $hour);
	$timestring .= sprintf(" %02dʬ", $min) if($min || $sec);
	$timestring .= sprintf(" %02d��", $sec) if($sec);

#	return "${year}ǯ ${mon}�� ${date}�� ${hour}�� ${min}ʬ ${sec}��";
	return $timestring;
}

# ����������ʸ���ν���
sub htmlEscape {
	my($s, $mode) = @_;
	$s =~ s/&/&amp;/g;
	$s =~ s/</&lt;/g;
	$s =~ s/>/&gt;/g;
	$s =~ s/"/&quot;/g; #"
	$s =~ s/'/&#x27;/g; #'
	$s =~ s/ /&#32;/g;
	$s =~ s/\,/&#44;/g;
	if ($mode) {
		$s =~ s/\r\n/<br>/g;
		$s =~ s/\r/<br>/g;
		$s =~ s/\n/<br>/g;
		$s =~ s/(<br>){5,}//g; # ���̲����к�
	}
	return $s;
}

#----------------------------------------------------------------------
# cookie
#----------------------------------------------------------------------
# cookie����
sub cookieInput {
	# ���說�å���
	local($key, $val, *cook);

	# ���å�������
	$cook = $ENV{'HTTP_COOKIE'};

	# ����ID����Ф�
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# �ǡ�����URL�ǥ����ɤ�������
	@cook=();
	foreach ( split(/<>/, $cook{'KAISEN_JS'}) ) {
#		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;
		push(@cook,$_);
	}
	(
		$defaultID,
		$HdefaultPassword,
		$defaultTarget,
		$HdefaultName,
		$HdefaultX,
		$HdefaultY,
		$HdefaultKind,
		$HjavaModeSet,
		$HimgLine,
		$HskinName,
		$defaultChipSize
	)
		= @cook;
}

# cookie����
sub cookieOutput {
	my($cookie, $gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 14 *24*60*60); # ����14��
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# ���ɸ��������
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# ���說�å���
	$cookie = 'Set-Cookie: KAISEN_JS=';

	my @data =
	(
		(($HmainMode eq 'owner') && !$Hcodevelope) ? $HcurrentID : $defaultID,
		($HinputPassword ne '') ? $HinputPassword : $HdefaultPassword,
		$defaultTarget,
		$HdefaultName,
		$HdefaultX,
		$HdefaultY,
		$HdefaultKind,
		($HjavaMode ne '') ? $HjavaMode : $HjavaModeSet,
		$HimgLine,
		$HskinName,
		(!$defaultChipSize) ? $HchipSize : $defaultChipSize
	);

	# ��¸�ǡ�����URL���󥳡���
	foreach (@data) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cookie .= "$_<>";
	}

	out("$cookie; expires=$gmt\n");
}

1;