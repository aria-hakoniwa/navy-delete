#----------------------------------------------------------------------
# Ȣ����� ���� JS ver7.xx
# ������ʹ�����⥸�塼��(ver1.00)
# �����ä�ǽ�� �ߥ����빶��
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------

# ���äΥߥ����빶����ɸ��õ��
sub searchMonsterTarget {
	my($island, $x, $y, $huge) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($lv)        = $landValue->[$x][$y];
	my($lv2)        = $landValue2->[$x][$y];

	# �����Ǥμ��Ф�
	my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$x][$y]);
	my $mName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = ($huge) ? $HhugeMonsterSpecial[$mKind] : $HmonsterSpecial[$mKind];

	return unless($special & 0x100);

	# ��̱�ο�
	my($boat) = 0;

	my $rtemp = ($huge) ? $HhugeMonsterFireRange[$mKind] : $HmonsterFireRange[$mKind];
	my $range = $an[$rtemp];

	# �ϰ������ɸ�Ϸ���õ��
	my($i, $sx, $sy, $kind, $tId, $tLv, $tFlag);
	# ���ַ��
	my $rang = $range - 2;
	my(@order) = randomArray($rang);
	foreach $i (0..$rang) {
		my $j = $order[$i] + 1;
		$sx = $x + $ax[$j];
		$sy = $y + $ay[$j];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		# �ϰ���ξ��
		$tKind = $land->[$sx][$sy];
		$tLv   = $landValue->[$sx][$sy];

		my $target = { x => $sx, y => $sy };

		if ($mFlag & 1) {
			# �Ų���ʤ顢�ʤˤ⤷�ʤ�
		} elsif ($mFlag & 2) {
			# �Ų���Ǥʤ������ˤ���
			# �������дϹ���
			if ($tKind == $HlandNavy) {
				# ����
				($tId, $tFlag) = (navyUnpack($tLv))[0, 5];
				if (($mId != $tId) && !($tFlag & 1)) {
					# ̣���δ����ǤϤʤ��ĳ��ʳ�
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			} elsif (($tKind == $HlandSbase) || # �������
				($tKind == $HlandOil)) {   # ��������
				if ($id != $mId) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			} elsif($tKind == $HlandComplex) { # ʣ���Ϸ�
				if ($id != $mId) {
					# ̣���λ��ߤǤϤʤ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					next if(!($HcomplexAttr[$cKind] & 0x100)); # ����
					if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind] || $HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]) {
						# ������ɸ����
						$HmonsterAttackTarget{"$id,$x,$y"} = $target;
						last;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# ����
				($tId, $tFlag) = (monsterUnpack($tLv))[0, 4];
				if (($mId != $tId) && !($tFlag & 1) && ($tFlag & 2)) {
					# �Ų���Ǥʤ������ˤ���
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			}
		} elsif (!($mFlag & 2)) {
			# Φ�ˤ���
			# �дϹ���
			if ($tKind == $HlandNavy) {
				# ����
				($tId, $tFlag) = (navyUnpack($tLv))[0, 5];
				if (($mId != $tId) && !($tFlag & 2) && !($tFlag & 1)) {
					# ̣���δ����ǤϤʤ������λĳ��ʳ�
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}

			# ���Ϲ���
			} elsif (($tKind == $HlandTown) || # Į��
				($tKind == $HlandForest) || # ��
				($tKind == $HlandFarm) || # ����
				($tKind == $HlandFactory) || # ����
				($tKind == $HlandBase) || # �ߥ��������
				($tKind == $HlandDefence) || # �ɱһ���
				($tKind == $HlandMonument) || # ��ǰ��
				($tKind == $HlandHaribote)) { # �ϥ�ܥ�
				if ($id != $mId) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}

			} elsif($tKind == $HlandComplex) {  # ʣ���Ϸ�
				if ($id != $mId) {
					# ̣���λ��ߤǤϤʤ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					next if(!($HcomplexAttr[$cKind] & 0x600)); # �дϡ�����
					if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind] || $HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]) {
						# ������ɸ����
						$HmonsterAttackTarget{"$id,$x,$y"} = $target;
						last;
					}
				}

			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# ����
				($tId, $tFlag) = (monsterUnpack($tLv))[0, 4];
				if (($mId != $tId) && !($tFlag & 1) && !($tFlag & 2)) {
					# �Ų���Ǥʤ���Φ�ˤ���
					# ������ɸ����
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			}
		}
	}
}

# ���äΥߥ����빶��
sub monsterAttack {
	my($island, $x, $y, $tx, $ty, $huge) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($tLandName) = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
	$tLandName = ($HlandMove[$id][$tx][$ty]) ? "${HtagName2_}${tLandName}${H_tagName2}" : "${HtagName_}${tLandName}${H_tagName}";
	my($landKind)  = $land->[$x][$y];
	my($lv)        = $landValue->[$x][$y];
	my($lv2)        = $landValue2->[$x][$y];

	my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
	my $mn = $HidToNumber{$mId};
	my($mIsland);
	$mIsland = $Hislands[$mn] if (defined $mn);
	my $special = ($huge) ? $HhugeMonsterSpecial[$mKind] : $HmonsterSpecial[$mKind];
	my $mName = landName($landKind, $lv);
	my $mPoint = "($x, $y)";
	my $tPoint = "($tx, $ty)";

	# ͧ����������ǧ
	my(%amityFlag, @noDefenceIds);
	if(defined $mn) {
		if($HmonsterSafetyZone) {
			$amityFlag{$mId} = 1;
			if(($HmonsterSafetyZone == 2) && (!$HamityInvalid || !$island->{'field'})) {
				foreach (@{$mIsland->{'amity'}}) {
					$amityFlag{$_} = 1;
				}
			}
		}
		if($HdBaseSelfNoDefenceMA == 1) {
			@noDefenceIds = ($mId);
		} elsif($HdBaseSelfNoDefenceMA == 2) {
			@noDefenceIds = ($mId, @{$mIsland->{'amityBy'}});
		} elsif($HdBaseSelfNoDefenceMA == 3) {
			@noDefenceIds = ($mId, @{$mIsland->{'amity'}});
		} elsif($HdBaseSelfNoDefenceMA == 4) {
			@noDefenceIds = ($mId, @{$mIsland->{'amity'}}, @{$mIsland->{'amityBy'}});
		} else {
			@noDefenceIds = (0);
		}
	}

	# ������
	my $rtemp = ($huge) ? $HhugeMonsterFireHex[$mKind] : $HmonsterFireHex[$mKind];
	my $err = $an[$rtemp]; # ��
	my $mFire = ($huge) ? $HhugeMonsterFire[$mKind] : $HmonsterFire[$mKind];
	$mFire += int($mExp/$mHp) if($mHp); # ������(�и��ͤ������뤫�λ�ˤʤ��������)
	$mFire = $HmonsterFireMax if($HmonsterFireMax && ($mFire > $HmonsterFireMax));
	# �˲���
	my $damage = ($huge) ? $HhugeMonsterDamage[$mKind] : $HmonsterDamage[$mKind];
	$damage = int($damage);
	$damage = 1 if($damage < 1);
	# ����������γȻ��ϰ�
	my $terrorhex = ($huge) ? $HhugeMonsterTerrorHex[$mKind] : $HmonsterTerrorHex[$mKind];
	my $range = 0;

	# ���⤹��
	my($r, $xx, $yy, $fx, $fy, $fPoint, $fKind, $fLv, $fLv2, @pointErr, @terrorPnt);
	my(%damageId);
	my $loopflag = 0;
	my $fire = 0;
	while ($fire < $mFire) {
		last if($loopflag); # ������­���ĳ��ǹ��⽪λ

		# ����������
		$r = int(rand($err));
		$xx = $tx + $ax[$r];
		$yy = $ty + $ay[$r];
		# �Ԥˤ�����Ĵ��
		$xx-- if(!($yy % 2) && ($ty % 2));
		$xx = $correctX[$xx + $#an];
		$yy = $correctY[$yy + $#an];

		# �����򤷤ʤ����
		if(!$HmonsterSelfAttack && ($xx == $x) && ($yy == $y)) {
			$r += int(1 + rand($err-1));
			$r -= $err if($r >= $err);
			$xx = $tx + $ax[$r];
			$yy = $ty + $ay[$r];
			# �Ԥˤ�����Ĵ��
			$xx-- if(!($yy % 2) && ($ty % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];
		}

		if($special & 0x200) {
			if (($xx < 0) || ($yy < 0)) {
				# �ϰϳ��ξ�硢������⤷�ʤ�
				$range = 0;
			} else {
				push(@terrorPnt, "($xx, $yy)");
				$range = $an[$terrorhex] - 1;
			}
		}
		my(@order) = randomArray($range + 1);
		foreach my $loop (0..$range) {
			# ���ˤʤäƤ��顢���⽪λ(�����������硢ɬ��)
			#return ($mId, $mExp, $mFlag, $mKind, $mHp) if($landValue->[$x][$y] == 0);
			if(($land->[$x][$y] != $HlandMonster) && ($land->[$x][$y] != $HlandHugeMonster)) {
				$loopflag = 1;
				last;
			}

			# ���깶������λ
			last if($fire >= $mFire);

#			# �������Ѥ����
#			if (defined $mn) {
#				$mIsland->{'money'} -= 1;
#				if ($mIsland->{'money'} < 0) {
#					# �������Ѥ�­��ʤ�
#					$mIsland->{'money'} = 0;
#					logNavyNoShell($id, $mId, $name, $mPoint, $mName);
#					$loopflag = 1;
#					last;
#				}
#			}

			$fire++;
			# ����������
			$fx = $xx + $ax[$order[$loop]];
			$fy = $yy + $ay[$order[$loop]];
			# �Ԥˤ�����Ĵ��
			$fx-- if(!($fy % 2) && ($yy % 2));
			$fx = $correctX[$fx + $#an];
			$fy = $correctY[$fy + $#an];

			$fPoint = "($fx, $fy)";
			if (($fx < 0) || ($fy < 0)) {
				# �ϰϳ��ξ��
				push(@pointErr, { 'OB' => $fPoint });
				next;
			}
			$fL  = $land->[$fx][$fy];
			$fLv = $landValue->[$fx][$fy];
			$fLv2 = $landValue2->[$fx][$fy];
			$fName  = landName($fL, $fLv);
			# �ɱһ���Ƚ��
			my($defence) = 0;
			# ̤Ƚ���ΰ�
			if (($fL == $HlandDefence) || countAroundComplex($island, $fx, $fy, $an[0], 0x40) ||
				countAroundNavySpecial($island, $fx, $fy, 0x20, $an[0], 0)){
				# �ɱһ��ߤ�̿��
				if ($fL == $HlandDefence) { # �ɱһ��ߤ�
					if($amityFlag{$id}) { # ̵����
						if(random(100) < $HmonsterSafetyInvalidp) {
							# �����Ψ�Ǹ���
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					# �ɱһ��ߤ��ѵ��Ϥ򲼤���
					$defflag = ($fLv % 100) - $damage;
					$fLv -= $damage;
					if($defflag < 0) {
						$island->{'dbase'}--;
						$island->{'ext'}[2]++ if(defined $mn); # �˲������ɱһ��ߤο�
					}
				}
			} elsif (countAroundDef($id, $island, $fx, $fy, 0x20, @noDefenceIds)) {
				# �ɱ��ϰ�
				$defence = 1;
			}

			if ($defence) {
				if($mFlag & 2) {
					# ���ˤ�����ϡ��ɱҤ���ʤ�
				} else {
					# �ɱҤ��줿
					push(@pointErr, { 'DF' => $fPoint });
					next;
				}
			}

			if (!($mFlag & 2)) {
				# Φ�ˤ���������̤Τʤ��Ϸ�
				if (($fL == $HlandSea)      || # ��
					($fL == $HlandMountain) || # ��
					($fL == $HlandWaste)    || # ����
					($fL == $HlandSbase)) {    # �������
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}
			} elsif (($mFlag & 2)) {
				# ���ˤ���������̤Τʤ��Ϸ�
				if(($fL == $HlandSea) || # ��
					($fL == $HlandWaste) || # ����
					($fL == $HlandPlains) || # ʿ��
					($fL == $HlandTown) || # Į��
					($fL == $HlandForest) || # ��
					($fL == $HlandFarm) || # ����
					($fL == $HlandFactory) || # ����
					($fL == $HlandBase) || # �ߥ��������
					($fL == $HlandDefence) || # �ɱһ���
					($fL == $HlandMountain) || # ��
					($fL == $HlandMonument) || # ��ǰ��
					($fL == $HlandHaribote)) { # �ϥ�ܥ�
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}
			}

			# ���������á�������ðʳ���̵����
			if($amityFlag{$id} && $fL != $HlandNavy && $fL != $HlandMonster && $fL != $HlandHugeMonster) {
				if(random(100) < $HmonsterSafetyInvalidp) {
					# �����Ψ�Ǹ���
					push(@pointErr, { 'SS' => $fPoint });
				} else {
					push(@pointErr, { 'SZ' => $fPoint });
					next;
				}
			}

			# ���̤��Ϸ�
			if ($fL == $HlandComplex) {  # ʣ���Ϸ�
				my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($fLv);
				$island->{'ext'}[5]++;
				# ���̤Τ����Ϸ�
				if( (($mFlag & 2) && ($HcomplexAttr[$cKind] & 0x100)) ||  # ���ˤ�������������дϡ�
					(!($mFlag & 2) && ($HcomplexAttr[$cKind] & 0x600)) ) {  # Φ�ˤ�������дϡ����ϡ�

					if($HcomplexAfter[$cKind]->{'stepdown'}) {
						$cFood  -= $damage * $HcomplexAfter[$cKind]->{'stepdown'};
						$cMoney -= $damage * $HcomplexAfter[$cKind]->{'stepdown'};
						if($cFood >= 0 || $cMoney >= 0) {
							$cFood = 0 if($cFood < 0);
							$cMoney = 0 if($cMoney < 0);
							$landValue->[$fx][$fy] = landPack($cTmp, $cKind, $cTurn, $cFood, $cMoney);
							logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
							next;
						}
					}
					# �������Ϸ��ˤ���
					# ʣ���Ϸ��ʤ������Ϸ�
					$land->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[0];
					$landValue->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[1];
					$HlandMove[$id][$fx][$fy] = 1;

					logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
					next;
				}
				# ���̤Τʤ��Ϸ�
				push(@pointErr, { 'ND' => $fPoint });
				next;
			} elsif ($fL == $HlandMonster) {  # ����
				my($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp) = monsterUnpack($fLv);
				my $fName = $HmonsterName[$fKind];

				# ���ɤ�����Φ�ɤ����Ǥʤ����̵��
				if (!($mFlag & 2) && ($fFlag & 2)) {
					push(@pointErr, { 'MS' => $fPoint });
					next;
				} elsif(($mFlag & 2) && !($fFlag & 2)) {
					# ������Φ�ˤ�����ä򹶷�Ǥ��ʤ�
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}

				# �Ų��桩
				if ($fFlag & 1) {
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# �Ų��椸��ʤ�
					if($amityFlag{$fId}) { # ̵����
						if(random(100) < $HmonsterSafetyInvalidp) {
							# �����Ψ�Ǹ���
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$fId} = 1 if($fId && ($fId != $id) && ($fId != $mId));
					if ($fHp <= $damage) {
						# ���ä��Ȥ᤿
						# �и���
						$mExp += $HmonsterExp[$fKind]; # ���äηи��ͤϺǹ��255
						$mIsland->{'gain'} += $HmonsterExp[$mKind] if(defined $mn);
						$mExp = 250 if($mExp > 250);
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);

						logNavyMonKill($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);

						# ����
#						if (defined $mn) {
#							my($value) = $HmonsterValue[$mKind];
#							if ($value > 0) {
#								$mIsland->{'money'} += $value;
#								logMsMonMoney($id, $mName, $value);
#							}

							# �޴ط�
#							my($prize) = $mIsland->{'prize'};
#							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
#							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
#							my($v) = 2 ** $mKind;
#							$monsters |= $v;
#							$mIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# �����༣��
#							$mIsland->{'monsterkill'}++;
#						}

					} else {
						# ���������Ƥ�
						logNavyMonster($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);
						# HP��1����
						#$landValue->[$fx][$fy]--;
						$fHp -= $damage;
						if($fHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp);
							next;
						}
					}
					if ($fFlag & 2) {
						# ���ˤ���
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $mSea;
					} else {
						# Φ�Ϥˤ���
						$land->[$fx][$fy] = $HlandWaste;
						$landValue->[$fx][$fy] = 0;
					}
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}
			} elsif ($fL == $HlandHugeMonster) {  # �������
				my($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp) = monsterUnpack($fLv);
				my $fName = $HhugeMonsterName[$fKind];

				# ���ɤ�����Φ�ɤ����Ǥʤ����̵��
				if (!($mFlag & 2) && ($fFlag & 2)) {
					push(@pointErr, { 'MS' => $fPoint });
					next;
				} elsif(($mFlag & 2) && !($fFlag & 2)) {
					# ������Φ�ˤ�����ä򹶷�Ǥ��ʤ�
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}

				# �Ų��桩
				if ($fFlag & 1) {
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# �Ų��椸��ʤ�
					if($amityFlag{$fId}) { # ̵����
						if(random(100) < $HmonsterSafetyInvalidp) {
							# �����Ψ�Ǹ���
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$fId} = 1 if($fId && ($fId != $id) && ($fId != $mId));
					if (($fHp <= $damage) && ($fHflag == 0)) {
						# ���ä��Ȥ᤿
						# ������ý���
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$fKind][$j] eq '');
							$ssx = $sx + $ax[$j];
							$ssy = $sy + $ay[$j];
							# �Ԥˤ�����Ĵ��
							$ssx-- if(!($ssy % 2) && ($sy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# �ϰϳ�
							next if(($ssx < 0) || ($ssy < 0));

							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# �����Ǥμ��Ф�
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# �����μ��Ϥ��ĤäƤ����繶��̵��
							if($HhugeMonsterSpecial[$fKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							} elsif ($mFlag2 & 2) {
								# ���ˤ���
								$land->[$ssx][$ssy] = $HlandSea;
								$landValue->[$ssx][$ssy] = $mSea2;
								$HlandMove[$id][$ssx][$ssy] = 1;
							} else {
								# Φ�Ϥˤ���
								$land->[$ssx][$ssy] = $HlandWaste;
								$landValue->[$ssx][$ssy] = 0;
								$HlandMove[$id][$ssx][$ssy] = 1;
							}
						}
						next if($deflag);
						# �и���
						$mExp += $HhugeMonsterExp[$fKind]; # ���äηи��ͤϺǹ��255
						$mIsland->{'gain'} += $HhugeMonsterExp[$fKind] if(defined $mn);
						$mExp = 250 if($mExp > 250);
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);

						logNavyMonKill($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);

						# ����
#						if (defined $mn) {
#							my($value) = $HmonsterValue[$mKind];
#							if ($value > 0) {
#								$mIsland->{'money'} += $value;
#								logMsMonMoney($id, $mName, $value);
#							}

							# �޴ط�
#							my($prize) = $mIsland->{'prize'};
#							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
#							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
#							my($v) = 2 ** $mKind;
#							$hmonsters |= $v;
#							$mIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# �����༣��
#							$mIsland->{'monsterkill'}++;
#						}

					} else {
						# ���������Ƥ�
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$fKind][$j] eq '');
							$ssx = $sx + $ax[$j];
							$ssy = $sy + $ay[$j];
							# �Ԥˤ�����Ĵ��
							$ssx-- if(!($ssy % 2) && ($sy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# �ϰϳ�
							next if(($ssx < 0) || ($ssy < 0));
							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# �����Ǥμ��Ф�
							my($mHflag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1];
							next if($mHflag2 != $j);
							# �����μ��Ϥ��ĤäƤ����繶��̵��
							if($HhugeMonsterSpecial[$fKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							}
						}
						next if($deflag);
						logNavyMonster($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);
						# HP��1����
						$fHp -= $damage;
						if($fHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp);
							next;
						}
					}
					if ($fFlag & 2) {
						# ���ˤ���
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $mSea;
					} else {
						# Φ�Ϥˤ���
						$land->[$fx][$fy] = $HlandWaste;
						$landValue->[$fx][$fy] = 0;
					}
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}
			} elsif ($fL == $HlandNavy) { # ����
				my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $nWait2, $nHp2, $ngoalx, $ngoaly) = navyUnpack($fLv, $fLv2);
				my $nSpecial2 = $HnavySpecial[$nKind2];
				my $nName2 = landName($fL, $fLv);

				# �����桩
				if (!($mFlag & 2) && ($nFlag2 & 2)) {
					# ���ä�Φ�ˤ��ƴ�����������
					push(@pointErr, { 'FS' => $fPoint });
					next;
				}

				# �ĳ���
				if ($nFlag2 & 1) {
					logNavyWreckDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nName2, $fPoint);
					# ���ˤʤ�
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = 0;
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}

				if($amityFlag{$nId2}) { # ̵����
					if(random(100) < $HmonsterSafetyInvalidp) {
						# �����Ψ�Ǹ���
						push(@pointErr, { 'SS' => $fPoint });
					} else {
						push(@pointErr, { 'SZ' => $fPoint });
						next;
					}
				}

				$damageId{$nId2} = 1 if($nId2 && ($nId2 != $id) && ($nId2 != $mId));
				if ($nHp2 <= $damage) {
					# ����

					# �и���
					$mExp += $HnavyExp[$nKind2]; # ���äηи��ͤϺǹ��255
					$mExp = 250 if($mExp > 250);
					$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
					if(defined $mn) {
						$mIsland->{'gain'} += $HnavyExp[$nKind2];
						$mIsland->{'ext'}[10]++;
						if($nId2 != $mId) {
							$mIsland->{'sink'}[$nKind]++;
						} else {
							$mIsland->{'sinkself'}[$nKind]++;
						}
					}
					my $n = $HidToNumber{$nId2};
					if(defined $n) {
						$Hislands[$n]->{'shipk'}[$nKind]-- ;
						# ���Х��Х�
						$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					if ($nSpecial2 & 0x8) {
						# ��������
						logNavyPortDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);
						# �����ˤʤ�
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = 1;
						$HlandMove[$id][$fx][$fy] = 1;
						$Hislands[$n]->{'navyPort'}-- if(defined $n);
					} else {
						# ��������
						logNavyShipDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);

						if (rand(100) < $HnavyProbWreck[$nKind]) {
							# �ĳ��ˤʤ�
							$landValue->[$fx][$fy] = navyPack(0, $nTmp2, $nStat2, $nSea2, int(rand(90)) + 10, 1, 0, $nKind2, 0, 0, 31, 31);
						} else {
							# ���ˤʤ�
							$land->[$fx][$fy] = $HlandSea;
							$landValue->[$fx][$fy] = $nSea2;
							$HlandMove[$id][$fx][$fy] = 1;
						}
						if(defined $n) {
							$Hislands[$n]->{'ships'}[$nNo2]--;
							$Hislands[$n]->{'ships'}[4]--;
						}
					}
					next;
				} else {
					# ����
					logNavyDamage($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);

					# HP��1����
					#$landValue->[$fx][$fy]--;
					$nHp2 -= $damage;
					if($nHp2 > 0) {
						$landValue->[$fx][$fy] = navyPack($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $nWait2, $mWait2, $nHp2, $ngoalx, $ngoaly);
					} else {
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $nSea2;
					}
					next;
				}
			} elsif($fL == $HlandSeaMine) {
				# ����
				logNavySeaMine($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);

				$land->[$fx][$fy]      = $HlandSea; # ������
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
				next;
			} elsif (($fL == $HlandDefence) && ($fLv >= 0)) {
				# �ɱһ��ߡ��ѵ��Ϥ��ĤäƤ����
				logNavyNormalDefence($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
			} elsif ($fL == $HlandCore) {
				# ����
				my($lFlag, $lLv) = (int($fLv / 10000), ($fLv % 10000));
				if( !(($mFlag & 2) && ($lFlag >= 1)) && !(!($mFlag & 2) && ($lFlag <= 1)) )  {
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
				# �ѵ��Ϥ򲼤���
				my $coreflag = $lLv - $damage;
				$fLv -= $damage;
				# ����������������˲���
				#$nIsland->{'epoint'}{$id}++ if((defined $nn) && ($island->{'event'}[6] == 6) || (($coreflag < 0) && ($island->{'event'}[6] == 7)) && ($island->{'event'}[1] <= $HislandTurn));
				if($coreflag >= 0) {
					$land->[$fx][$fy] = $HlandCore;
					$landValue->[$fx][$fy] = $fLv;
					logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} else {
					$island->{'core'}--;
					$island->{'slaughterer2'} = $mId if($HcorelessDead && (defined $mn) && !$island->{'core'}); # �˲�������ID��Ͽ
					if ($mFlag & 2) {
						# ����
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} else {
						# �дϡ�����
						logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					}
					if(!$lFlag) {
						$land->[$fx][$fy] = $HlandWaste; # ���ϡ���������
						$landValue->[$fx][$fy] = 1;
					} else {
						$land->[$fx][$fy] = $HlandSea; # ��
						$landValue->[$fx][$fy] = 2 - $lFlag;
					}
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} elsif ($fL == $HlandTown) {
				# �ԻԷ�
				my $sLv = 0;
				my $rank = 0;
				if($HtownStepDown) {
					foreach (reverse(0..$#HlandTownValue)) {
						if($HlandTownValue[$_] <= $fLv) {
							$rank = $_;
							last;
						}
					}
					$rank -= $damage;
					$rank = 0 if($rank < 0);
					$sLv = $HlandTownValue[$rank];
				}
				$mExp += int($fLv / 20); # ���äηи��ͤϺǹ��255
				$mExp = 250 if($mExp > 250);
				$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
				$boat += ($fLv - $sLv); # ��̱�˥ץ饹
				if($rank) {
					$landValue->[$fx][$fy] = $sLv;
					logNavyNormalTown($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint, $HlandTownName[$rank]);
				} else {
					$island->{'slaughterer'} = $mId if(defined $mn); # �ԻԷϤ��˲�������ID��Ͽ
					logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
					$land->[$fx][$fy]      = $HlandWaste;
					$landValue->[$fx][$fy] = 1; # ������
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} else {
				# ����¾���Ϸ�
				logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
				if ($fKind == $HlandBase && (defined $mn)) {
					$mIsland->{'ext'}[3]++; # ���ˤ����ߥ�������Ϥο�
				}
			}

			# �������Ϸ��ˤ���
			if (($fL == $HlandOil) ||
				($fL == $HlandSeaMine)) {
				# �Ǥ����ġ�������ä��鳤
				$land->[$fx][$fy] = $HlandSea;
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
			} elsif($fL == $HlandBouha) {
				# �Ǥ�������ʤ�����
				$land->[$fx][$fy] = $HlandSea;
				$landValue->[$fx][$fy] = 1;
				$HlandMove[$id][$fx][$fy] = 1;
			} elsif(($fL == $HlandDefence) && ($fLv >= 0)) {
				# �Ǥ��ѵ��ϤλĤäƤ����ɱһ��ߤʤ��Ѥ���
				$land->[$fx][$fy] = $HlandDefence;
				$landValue->[$fx][$fy] = $fLv;
			} else {
				# ���Ϥˤʤ�
				$land->[$fx][$fy] = $HlandWaste;
				$landValue->[$fx][$fy] = 1; # ������
				$HlandMove[$id][$fx][$fy] = 1;
			}
		} #foreach
	} #while
	if($fire) {
		my $l;
		my @pKey  = ('OB', 'DF', 'ND', 'MS', 'MH', 'FS', 'SZ', 'SS');
		my @pName = ('����', '�ɱ�', '̵��', '����', '�Ų�', '����', '̵��', '����');
		my $str = '';
		my $pntStr = '<BR>��--- ';
		my @cntErr = (0, 0, 0, 0, 0, 0, 0, 0, 0);
		foreach $l (0..7) {
			my $pflag = 1;
			my @pointOut = ();
			my $p;
			foreach $p (@pointErr) {
				my $pnt = $p->{$pKey[$l]};
				next if($pnt eq '');
				$cntErr[$l]++;
				$cntErr[8]++;
				foreach (@pointOut) {
					$pflag = 0 if($_ eq $pnt);
				}
				push(@pointOut, $pnt) if($pflag);
			}
			if($cntErr[$l]) {
				$str .= " $pName[$l]\:" . $cntErr[$l];
				$pntStr .= "$pName[$l] �� " . join(',', @pointOut) . "��" if($l);
			}
		}
		$pntStr = '' if(!$cntErr[8] || ($cntErr[8] == $cntErr[0]));
		$pntStr .= '[����濴 �� ' . join(',', @terrorPnt) .']' if(@terrorPnt);
		$str = '(̿��:' . ($fire - $cntErr[8]) . $str .')';
		$str .= '[�˲���:' . $damage . ']' if($damage > 1);
		my $attack = ($huge) ? $HhugeMonsterFireName[$mKind] : $HmonsterFireName[$mKind];
		$attack = '�ߥ����빶��' if($attack eq '');
		logNavyMatome($id, $name, $mId, $mPoint, $mName, $tPoint, $tLandName, $attack, $str, $pntStr, join('-', (keys %damageId)));
	}
	# ��̱Ƚ��
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && (defined $mn)) {
		# ��̱ɺ��
		my($achive) = boatAchive($mIsland, $boat); # ��ã��̱

		if ($achive > 0) {
			# �����Ǥ����夷����硢�����Ǥ�
			my $name = islandName($mIsland);
			logMsBoatPeople($mId, $name, $achive);
			$mIsland->{'ext'}[4] += int($achive); # �߽Ф�����̱�ι�׿͸�

			# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
			if ($achive >= 200) {
				$mIsland->{'achive'} += $achive;
			}
		}
	}

	if(($land->[$x][$y] == $HlandMonster) || ($land->[$x][$y] == $HlandHugeMonster)) {
		return monsterUnpack($landValue->[$x][$y]);
	} else {
		return ($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, 0);
	}
}

1;
