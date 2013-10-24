# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ���� JS ver7.xx
# ������ʹ�����⥸�塼��(ver1.00)
# ���ߥ����빶��
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------

# �ߥ�����ȯ��
sub missileFire {
	my($target, $island, $tIsland, $x, $y, $kind, $arg, $cost) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($comName)   = $HcomName[$kind];
	my($point)     = "($x, $y)";

	my($tName)      = islandName($tIsland);
	my($tLand)      = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tLandName)  = landName($tLand->[$x][$y], $tLandValue->[$x][$y]);
	$tLandName = ($HlandMove[$target][$x][$y]) ? "${HtagName2_}${tLandName}${H_tagName2}" : "${HtagName_}${tLandName}${H_tagName}";

	my($boat) = 0; # ��̱�ο�
	my($flagbase)   = 0;
	my($xx, $yy, $tx, $ty, @pointErr);
	my(%damageId);
	my($mkind) = $kind - $HcomMissile[0];
	my($special) = $HmissileSpecial[$mkind];
	my($err) = $an[$HmissileErr[$mkind]]; # ��
	my($damage)= int($HmissileDamage[$mkind]);# �˲���
	$damage = 1 if($damage < 1);

	# ����������γȻ��ϰ�
	my $range = 0;

	# ������˲��á�������ä����ʤ���С�ȯ�����
	if($HtargetMonster &&
		!countAround($tIsland, $x, $y, $err, $HlandMonster, $HlandHugeMonster)) {
		logNoTarget($id, $name, $comName);
		return;
	}

	# ͧ����������ǧ
	my(%amityFlag, @noDefenceIds);
	if($HmissileSafetyZone) {
		$amityFlag{$id} = 1;
		if(($HmissileSafetyZone == 2) && (!$HamityInvalid || !$island->{'field'})) {
			foreach (@{$island->{'amity'}}) {
				$amityFlag{$_} = 1;
			}
		}
	}
	if($HdBaseSelfNoDefenceMS == 1) {
		@noDefenceIds = ($id);
	} elsif($HdBaseSelfNoDefenceMS == 2) {
		@noDefenceIds = ($id, @{$island->{'amityBy'}});
	} elsif($HdBaseSelfNoDefenceMS == 3) {
		@noDefenceIds = ($id, @{$island->{'amity'}});
	} elsif($HdBaseSelfNoDefenceMS == 4) {
		@noDefenceIds = ($id, @{$island->{'amity'}}, @{$island->{'amityBy'}});
	} else {
		@noDefenceIds = (0);
	}

	# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼��
	my($bx, $by, $count, $fire) = (0, 0, 0, 0);
	my($bKind, $bLv, @terrorPnt);
	while (($arg > 0) && ($island->{'money'} >= $cost)) {
		# ���Ϥ򸫤Ĥ���ޤǥ롼��
		while ($count <= $island->{'pnum'}) {
			$bx = $island->{'rpx'}[$count];
			$by = $island->{'rpy'}[$count];
			$bKind = $land->[$bx][$by];
			$bLv   = $landValue->[$bx][$by];

			last if (($bKind == $HlandBase) || ($bKind == $HlandSbase));

			$count++;
		}

		# ���Ĥ���ʤ��ä��餽���ޤ�
		last if ($count > $island->{'pnum'});

		# �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
		$flagbase = 1;

		# ���ϤΥ�٥�򻻽�
		my($level) = expToLevel($bKind, $bLv);


#$level = 14;
#$arg = 14;

		# ������ǥ롼��
		while (($level > 0) && ($arg > 0) && ($island->{'money'} > $cost)) {
			# ���Ϥκǿ�������Ĵ�٤�
			$bKind = $land->[$bx][$by];
			$bLv   = $landValue->[$bx][$by];

			# ����������
			my($r) = random($err);
			$xx = $x + $ax[$r];
			$yy = $y + $ay[$r];
			# �Ԥˤ�����Ĵ��
			$xx-- if(!($yy % 2) && ($y % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];

			if($special & 0x4) {
				if (($xx < 0) || ($yy < 0)) {
					# �ϰϳ��ξ�硢������⤷�ʤ�
					$range = 0;
				} else {
					push(@terrorPnt, "($xx, $yy)");
					$range = $an[$HmissileTerrorHex[$mkind]] - 1;
				}
			}
			my(@order) = randomArray($range + 1);
			foreach my $loop (0..$range) {
				# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
				$level--;
				$arg--;
				last if($level < 0 || $arg < 0 || $island->{'money'} < $cost);
				$fire++;
				$island->{'money'} -= $cost;
				$island->{'shellMoney'} += $cost;

				if(!$STcheck{$kind}) {
					$island->{'ext'}[1] += $cost; # �׸���
					$island->{'ext'}[6]++; # ȯ�ͤ����ߥ�����ο�
					if($HallyNumber) {
						foreach (@{$island->{'allyId'}}) {
							$Hally[$HidToAllyNumber{$_}]->{'ext'}[0]++;
						}
					}
				}
				if($HallyNumber) {
					my $allyflag = 0;
					my $ai;
					foreach $ai (@{$island->{'allyId'}}) {
						foreach (@{$tIsland->{'allyId'}}) {
							if($_ == $ai) {
								$allyflag = 1;
								last;
							}
						}
					}
					if($allyflag) {
						# ̣���˷⤿�줿���׸��٥ޥ��ʥ�(�������ߥ�����ο��ϥ�����Ȥ��ʤ�)
						$tIsland->{'ext'}[1] -= $cost; # �׸���
					} else {
						# Ũ�˷⤿�줿���׸��٥ץ饹
						$tIsland->{'ext'}[1] += $cost; # �׸���
						$tIsland->{'ext'}[5]++; # �������ߥ�����ο�
					}
					foreach (@{$tIsland->{'allyId'}}) {
						$Hally[$HidToAllyNumber{$_}]->{'ext'}[1]++;
					}
				}

				# ����������
				$tx = $xx + $ax[$order[$loop]];
				$ty = $yy + $ay[$order[$loop]];
				# �Ԥˤ�����Ĵ��
				$tx-- if(!($ty % 2) && ($yy % 2));
				$tx = $correctX[$tx + $#an];
				$ty = $correctY[$ty + $#an];

				# �������ϰ��⳰�����å�
				if (($tx < 0) || ($ty < 0)) {
					# �ϰϳ�
					push(@pointErr, { 'OB' => $tPoint });
					next;
				}

				# ���������Ϸ�������
				my($tL)     = $tLand->[$tx][$ty];
				my($tLv)    = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# �ɱһ���Ƚ��
				my($defence) = 0;
				my($defflag) = 1;
				# ̤Ƚ���ΰ�
				if (($tL == $HlandDefence) || countAroundComplex($tIsland, $tx, $ty, $an[0], 0x20) ||
					countAroundNavySpecial($tIsland, $tx, $ty, 0x20, $an[0], 0)){
					# �ɱһ��ߤ�̿��
					if (($tL == $HlandDefence) && # �ɱһ��ߤ�
						!($special & 0x2)) { # Φ���˲��ʳ�
						if($amityFlag{$target}) { # ̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						# �ɱһ��ߤ��ѵ��Ϥ򲼤���
						$defflag = ($tLv % 100) - $damage;
						$tLv -= $damage;
						if($defflag < 0) {
							$tIsland->{'dbase'}--;
							$island->{'ext'}[2]++ if(!$STcheck{$kind}); # �˲������ɱһ��ߤο�
						}
					}
				} elsif (countAroundDef($target, $tIsland, $tx, $ty, 0x20, @noDefenceIds)) {
					# �ɱ��ϰ�
					$defence = 1;
				}

				if ($defence) {
					# ��������
					push(@pointErr, { 'DF' => $tPoint });
					$tIsland->{'ext'}[7]++; # �ɱһ��ߤ��Ƥ����ߥ�����ο�
					next;
				}

				# �ָ��̤ʤ���hex��ǽ��Ƚ��
				if ((($tL == $HlandSea) && (!$tLv)) || # ������
					((($tL == $HlandSea) || # ��
					((($tL == $HlandSbase) || ($tL == $HlandSbase)) && !($special & 0x20)) || # ������Ϥޤ��ϵ��������̵���ʤ�
					($tL == $HlandMountain))) && # ��
					!($special & 0x2)) { # Φ���˲��ʳ�

					# ̵����
					push(@pointErr, { 'ND' => $tPoint });
					next;
				}

				# ���������á�������ðʳ���̵����
				if($amityFlag{$target} && $tL != $HlandNavy && $tL != $HlandMonster && $tL != $HlandHugeMonster) {
					if(random(100) < $HmissileSafetyInvalidp) {
						# �����Ψ�Ǹ���
						push(@pointErr, { 'SS' => $tPoint });
					} else {
						push(@pointErr, { 'SZ' => $tPoint });
						next;
					}
				}

				# �Ƥμ����ʬ��
				if ($special & 0x2) {
					# Φ���˲���
					my $seaflagLD = 1;
					if ($tL == $HlandMountain) {
						# ��(���Ϥˤʤ�)
						logMsLDMountain($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

						# ���Ϥˤʤ�
						$tLand->[$tx][$ty] = $HlandWaste;
						$tLandValue->[$tx][$ty] = 0;
						$HlandMove[$target][$tx][$ty] = 1;
						next;

					} elsif ($tL == $HlandComplex) {
						# ʣ���Ϸ�
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
						if(!(defined $HcomplexAfter[$cKind]->{'attack'}[0])) {
							# �������Ϸ������ꤵ��Ƥ��ʤ���硤���Ϥˤʤ�
							logMsLDMountain($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

							# ���Ϥˤʤ�
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 0;
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}
						# ����¾
						logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandSbase) {
						# �������
						$seaflagLD = 0; # ���ˤʤ�
						logMsLDSbase($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandSeaMine) {
						# ����
						$seaflagLD = 0; # ���ˤʤ�
						logMsSeaMine($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandMonster) {
						# ����
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						if ($mFlag & 2) {
							# ���ˤ���
							$seaflagLD = 0; # ���ˤʤ�
							logMsLDMonsterSea($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							# Φ�ˤ���
							logMsLDMonster($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}
					} elsif ($tL == $HlandHugeMonster) {
						# �������
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $deflag = 0;
						if($mHflag == 0) {
							my($i, $sx, $sy, $flag);

							foreach $i (1..6) {
								next if($HhugeMonsterImage[$mKind][$i] eq '');
								$sx = $tx + $ax[$i];
								$sy = $ty + $ay[$i];
								# �Ԥˤ�����Ĵ��
								$sx-- if(!($sy % 2) && ($ty % 2));
								$sx = $correctX[$sx + $#an];
								$sy = $correctY[$sy + $#an];
								# �ϰϳ�
								next if(($sx < 0) || ($sy < 0));

								next if($tLand->[$sx][$sy] != $HlandHugeMonster);
								my($mId2, $mHflag2, $mSea2, $mExp2, $mFlag2, $mKind2, $mHp2) = monsterUnpack($tLandValue->[$sx][$sy]);
								next if($mHflag2 != $i);
								# �����μ��Ϥ��ĤäƤ����繶��̵��
								if($HhugeMonsterSpecial[$mKind] & 0x10000) {
									$deflag = 1;
									push(@pointErr, { 'DF' => $tPoint });
									last;
								} elsif ($mFlag2 & 2) {
									$tLand->[$sx][$sy] = $HlandSea;
									$tLandValue->[$sx][$sy] = $mSea2;
									$HlandMove[$target][$tx][$ty] = 1;
								} else {
									$tLand->[$sx][$sy] = $HlandWaste;
									$tLandValue->[$sx][$sy] = 1;
									$HlandMove[$target][$tx][$ty] = 1;
								}
							}
						}
						next if($deflag);
						if ($mFlag & 2) {
							# ���ˤ���
							logMsLDMonsterSea($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$seaflagLD = 0; # ���ˤʤ�
						} else {
							# Φ�ˤ���
							logMsLDMonster($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}
					} elsif ($tL == $HlandNavy) {
						# ����
						my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($tLv);
						if($amityFlag{$nId} && !($nFlag & 1)) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $n = $HidToNumber{$nId};
						my $nSpecial = $HnavySpecial[$nKind];
						$island->{'ext'}[10]++;
						$tLname = landName($tL, $tLv);
						if(defined $n) {
							$Hislands[$n]->{'shipk'}[$nKind]--;
							# ���Х��Х�
							$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
						}
						if ($nSpecial & 0x8) {
							# ��
							logMsLDNavy($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$tIsland->{'navyPort'}--;
						} else {
							# ����
							if ($nFlag & 2) {
								# ����
								logMsLDNavySea2($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							} else {
								# ���
								logMsLDNavySea($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							}
							if(defined $n) {
								$Hislands[$n]->{'ships'}[$nNo]--;
								$Hislands[$n]->{'ships'}[4]--;
								$HnavyAttackTarget{"$id,$tx,$ty"} = undef;
							}
							$seaflagLD = 0; # ���ˤʤ�
						}
					} elsif ($tL == $HlandSea) {
						# ����
						$seaflagLD = 0; # ���ˤʤ�
						logMsLDSea1($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandCore) {
						# ����
						my($lFlag, $lLv) = (int($tLv / 10000), ($tLv % 10000));
						$tIsland->{'core'}--;
						$tIsland->{'slaughterer2'} = $id if($HcorelessDead && !$tIsland->{'core'}); # �˲�������ID��Ͽ
						if(!$lFlag) {
							logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							$seaflagLD = 0; # ���ˤʤ�
							logMsLDSea1($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}

					} else {
						# ����¾
						logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

						# �и���
						if ($tL == $HlandTown) {
							if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
								# �ޤ����Ϥξ��Τ�
								$bLv += int($tLv / 20);
								$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
								$landValue->[$bx][$by] = $bLv;
								$tIsland->{'slaughterer'} = $id;
							}
						} elsif ($tL == $HlandOil) {
							$seaflagLD = 0; # ���ˤʤ�
						}
					}

					# �����ˤʤ�
					$tLand->[$tx][$ty] = $HlandSea;
					$tIsland->{'area'}--;
					$tLandValue->[$tx][$ty] = $seaflagLD;
					# �Ǥ����ġ�������������ϡ�������ä��鳤
					$HlandMove[$target][$tx][$ty] = 1;
				} else {
					# ����¾�ߥ�����
					if ($tL == $HlandWaste) {
						# ����(�ﳲ�ʤ�)
						push(@pointErr, { 'ND' => $tPoint });
					} elsif ($tL == $HlandSeaMine) {
						# ����
						logMsSeaMine($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
					} elsif ($tL == $HlandMonster) {
						# ����
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $mName = landName($tL, $tLv);

						# �����桩
						if(($mFlag & 2) && !($special & 0x20)) {
							# ������
							push(@pointErr, { 'MS' => $tPoint });
							next;
						}

						# �Ų��桩
						if(($mFlag & 1) && !($special & 0x10)) {
							# �Ų���
							push(@pointErr, { 'MH' => $tPoint });
							next;
						} else {
							# �Ų��椸��ʤ�
							$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $target));
							if ($mHp <= $damage) {
								# ���ä��Ȥ᤿
								if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
									# �и���
									$bLv += $HmonsterExp[$mKind];
									$island->{'gain'} += $HmonsterExp[$mKind];
									$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
									$landValue->[$bx][$by] = $bLv;
								}

								logMsMonKill($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});
								$HlandMove[$target][$tx][$ty] = 1;

								# ����
								my($value) = $HmonsterValue[$mKind];
								if ($value > 0) {
									$tIsland->{'money'} += $value;
									logMsMonMoney($id, $target, $mName, $value, $STcheck{$kind});
								}

								# �޴ط�
								my($prize) = $island->{'prize'};
								$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
								my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
								my($v) = 2 ** $mKind;
								$monsters |= $v;
								$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
								# �����༣��
								$island->{'monsterkill'}++;

							} else {
								# ���������Ƥ�
								logMsMonster($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});

								# HP��1����
								$tLandValue->[$tx][$ty] -= $damage;
								next;
							}
						}
						# �Τΰ������ä���
						if ($mFlag & 2) {
							# ���ˤ���
							$tLand->[$tx][$ty] = $HlandSea;
							$tLandValue->[$tx][$ty] = $mSea;
						} else {
							# Φ�Ϥˤ���
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1;
						}
						$HlandMove[$target][$tx][$ty] = 1;
						next;
					} elsif ($tL == $HlandHugeMonster) {
						# �������
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $mName = landName($tL, $tLv);

# �����ʳ��ؤΥߥ����빶���ͭ����̵���ˤ�����ϥ����Ȥ�Ϥ�����(�����ɱҤ�ǽ�Ϥ�⤿���Ƥ����硢�Ỵ�Ǥ�(^^;;;)
#						if($mHflag != 0) { 
#							push(@pointErr, { 'ND' => $tPoint });
#							next;
#						}

# ���ˤ������ߥ�����ͭ����̵���ˤ�����ϡ������Ȥ�Ϥ�����
						# �����桩
						if(($mFlag & 2) && !($special & 0x20)) {
							# ������
							push(@pointErr, { 'MS' => $tPoint });
							next;
						}

						# �Ų��桩
						if(($mFlag & 1) && !($special & 0x10)) {
							# �Ų���
							push(@pointErr, { 'MH' => $tPoint });
							next;
						} else {
							# �Ų��椸��ʤ�
							$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $target));
							if(($mHp <= $damage) && ($mHflag == 0)) {
								# ���ä��Ȥ᤿
								my($i, $sx, $sy, $flag);
								my $deflag = 0;

								foreach $i (0..6) {
									next if($HhugeMonsterImage[$mKind][$i] eq '');
									$sx = $tx + $ax[$i];
									$sy = $ty + $ay[$i];
									# �Ԥˤ�����Ĵ��
									$sx-- if(!($sy % 2) && ($ty % 2));
									$sx = $correctX[$sx + $#an];
									$sy = $correctY[$sy + $#an];
									# �ϰϳ�
									next if(($sx < 0) || ($sy < 0));

									next if($tLand->[$sx][$sy] != $HlandHugeMonster);
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($tLandValue->[$sx][$sy]))[1, 2, 4];
									next if($mHflag2 != $i);
									# �����μ��Ϥ��ĤäƤ����繶��̵��
									if($HhugeMonsterSpecial[$mKind] & 0x10000) {
										$deflag = 1;
										push(@pointErr, { 'DF' => $tPoint });
										last;
									} elsif ($mFlag2 & 2) {
										$tLand->[$sx][$sy] = $HlandSea;
										$tLandValue->[$sx][$sy] = $mSea2;
									} else {
										$tLand->[$sx][$sy] = $HlandWaste;
										$tLandValue->[$sx][$sy] = 1;
									}
									$HlandMove[$target][$sx][$sy] = 1;
								}
								next if($deflag);
								if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
									# �и���
									$bLv += $HhugeMonsterExp[$mKind];
									$island->{'gain'} += $HhugeMonsterExp[$mKind];
									$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
									$landValue->[$bx][$by] = $bLv;
								}

								logMsMonKill($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});
								$HlandMove[$target][$tx][$ty] = 1;

								my($value) = $HhugeMonsterValue[$mKind];
								if ($value > 0) {
									$tIsland->{'money'} += $value;
									logMsMonMoney($id, $target, $mName, $value, $STcheck{$kind});
								}

								# �޴ط�
								my($prize) = $island->{'prize'};
								$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
								my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
								my($v) = 2 ** $mKind;
								$hmonsters |= $v;
								$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
								# �����༣��
								$island->{'monsterkill'}++;
								next;

							} else {
								# ���������Ƥ�
								my($i, $sx, $sy, $flag);
								my $deflag = 0;
								foreach $i (0..6) {
									next if($HhugeMonsterImage[$mKind][$i] eq '');
									$sx = $tx + $ax[$i];
									$sy = $ty + $ay[$i];
									# �Ԥˤ�����Ĵ��
									$sx-- if(!($sy % 2) && ($ty % 2));
									$sx = $correctX[$sx + $#an];
									$sy = $correctY[$sy + $#an];
									# �ϰϳ�
									next if(($sx < 0) || ($sy < 0));

									next if($tLand->[$sx][$sy] != $HlandHugeMonster);
									my($mId2, $mHflag2, $mSea2, $mExp2, $mFlag2, $mKind2, $mHp2) = monsterUnpack($tLandValue->[$sx][$sy]);
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($tLandValue->[$sx][$sy]))[1, 2, 4];
									next if($mHflag2 != $i);
									# �����μ��Ϥ��ĤäƤ����繶��̵��
									if($HhugeMonsterSpecial[$mKind] & 0x10000) {
										$deflag = 1;
										push(@pointErr, { 'DF' => $tPoint });
										last;
									}
								}
								next if($deflag);
								# HP��1����
								$mHp -= $damage;
								logMsMonster($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});
								if($mHp > 0) {
									# ���������Ƥ�
									$tLandValue->[$tx][$ty] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
									next;
								}
							}
							# �Τΰ������ä���
							if ($mFlag & 2) {
								# ���ˤ���
								$tLand->[$tx][$ty] = $HlandSea;
								$tLandValue->[$tx][$ty] = $mSea;
							} else {
								# Φ�Ϥˤ���
								$tLand->[$tx][$ty] = $HlandWaste;
								$tLandValue->[$tx][$ty] = 1;
							}
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}
					} elsif ($tL == $HlandNavy) {
						# ����
						my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($tLv);
						my $n = $HidToNumber{$nId};
						my $nSpecial = $HnavySpecial[$nKind];
						my $nName = landName($tL, $tLv);

						# �����桩
						if(($nFlag & 2) && !($special & 0x20)) {
							# ������
							push(@pointErr, { 'FS' => $tPoint });
							next;
						}

						# �ĳ���
						if ($nFlag & 1) {
							# �ĳ�
							logMsNavyWreckDestroy($id, $target, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

							# ���ˤʤ�
							$tLand->[$tx][$ty] = $HlandSea;
							$tLandValue->[$tx][$ty] = 0;
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}

						if($amityFlag{$nId}) { #̵����
							if(random(100) < $HmissileSafetyInvalidp) {
								# �����Ψ�Ǹ���
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}

						$damageId{$nId} = 1 if($nId && ($nId != $id) && ($nId != $target));
						if ($nHp <= $damage) {
							# ����
							if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
								# �и���
								$bLv += $HnavyExp[$nKind];
								$island->{'gain'} += $HnavyExp[$nKind];
								$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
								$landValue->[$bx][$by] = $bLv;
							}
							$island->{'ext'}[10]++;
							if($nId != $id) {
								$island->{'sink'}[$nKind]++;
							} else {
								$island->{'sinkself'}[$nKind]++;
							}
							if(defined $n) {
								$Hislands[$n]->{'shipk'}[$nKind]--;
								# ���Х��Х�
								$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
							}
							if ($nSpecial & 0x8) {
								# ��������
								logMsNavyPortDestroy($id, $target, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

								# �����ˤʤ�
								$tLand->[$tx][$ty] = $HlandSea;
								$tLandValue->[$tx][$ty] = 1;
								$HlandMove[$target][$tx][$ty] = 1;
								$Hislands[$n]->{'navyPort'}-- if(defined $n);
							} else {
								# ��������
								logMsNavyShipDestroy($id, $target, $nId, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

								if (rand(100) < $HnavyProbWreck[$nKind]) {
									# �ĳ��ˤʤ�
									$tLandValue->[$tx][$ty] = navyPack(0, $nTmp, $nStat, $nSea, int(rand(90)) + 10, 1, 0, $nKind, 0);
								} else {
									# ���ˤʤ�
									$tLand->[$tx][$ty] = $HlandSea;
									$tLandValue->[$tx][$ty] = 0;
									$HlandMove[$target][$tx][$ty] = 1;
									$HnavyAttackTarget{"$id,$tx,$ty"} = undef;
								}
								if(defined $n) {
									$Hislands[$n]->{'ships'}[$nNo]--;
									$Hislands[$n]->{'ships'}[4]--;
								}
							}
							next;
						} else {
							# ����
							logMsNavyDamage($id, $target, $nId, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

							# HP��1����
							$tLandValue->[$tx][$ty] -= $damage;
							next;
						}
					} elsif (($tL == $HlandDefence) && ($tLv >= 0)) {
						# �ɱһ��ߡ��ѵ��Ϥ��ĤäƤ����
						logMsDefence($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
					} elsif ($tL == $HlandCore) {
						# ����
						my($lFlag, $lLv) = (int($tLv / 10000), ($tLv % 10000));
						if(($lFlag == 2) && !($special & 0x20)) {
							# ������ߤϳ��Τդ�
							push(@pointErr, { 'ND' => $tPoint });
							next;
						}
						# �ѵ��Ϥ򲼤���
						my $coreflag = $lLv - $damage;
						$tLv -= $damage;
						if($coreflag >= 0) {
							$tLand->[$tx][$ty] = $HlandCore;
							$tLandValue->[$tx][$ty] = $tLv;
							logMsDefence($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							$tIsland->{'core'}--;
							$tIsland->{'slaughterer2'} = $id if($HcorelessDead && !$tIsland->{'core'}); # �˲�������ID��Ͽ
							if(!$lFlag) {
								$tLand->[$tx][$ty] = $HlandWaste;
								$tLandValue->[$tx][$ty] = 1; # ������
								logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							} else {
								$tLand->[$tx][$ty] = $HlandSea;
								$tLandValue->[$tx][$ty] = 2 - $lFlag;
								logMsNavyWreckDestroy($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							}
							$HlandMove[$target][$tx][$ty] = 1;
						}
						next;
					} elsif ($tL == $HlandComplex) {
						# ʣ���Ϸ�
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
						if(!(defined $HcomplexAfter[$cKind]->{'attack'}[0])) {
							push(@pointErr, { 'ND' => $tPoint });
							next;
						}
						if($HcomplexAfter[$cKind]->{'stepdown'}) {
							$cFood  -= $damage * $HcomplexAfter[$cKind]->{'stepdown'};
							$cMoney -= $damage * $HcomplexAfter[$cKind]->{'stepdown'};
							if($cFood >= 0 || $cMoney >= 0) {
								$cFood = 0 if($cFood < 0);
								$cMoney = 0 if($cMoney < 0);
								$tLandValue->[$tx][$ty] = landPack($cTmp, $cKind, $cTurn, $cFood, $cMoney);
								logMsDefence($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
								next;
							}
						}
						# �������Ϸ��ˤ���
						# ʣ���Ϸ��ʤ������Ϸ�
						$tLand->[$tx][$ty] = $HcomplexAfter[$cKind]->{'attack'}[0];
						$tLandValue->[$tx][$ty] = $HcomplexAfter[$cKind]->{'attack'}[1];
						$island->{'complex'}[$cKind]--;
						$HlandMove[$target][$tx][$ty] = 1;
						logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						next;
					} elsif ($tL == $HlandTown) {
						# �ԻԷ�
						my $sLv = 0;
						my $rank = 0;
						if($HtownStepDown) {
							foreach (reverse(0..$#HlandTownValue)) {
								if($HlandTownValue[$_] <= $tLv) {
									$rank = $_;
									last;
								}
							}
							$rank -= $damage;
							$rank = 0 if($rank < 0);
							$sLv = $HlandTownValue[$rank];
						}
						if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
							# �и���
							$bLv += int(($tLv - $sLv) / 20);
							$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
							$landValue->[$bx][$by] = $bLv;
						}
						$boat += ($tLv - $sLv); # ��̱�˥ץ饹
						if($rank) {
							$tLandValue->[$tx][$ty] = $sLv;
							logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $HlandTownName[$rank], $STcheck{$kind});
						} else {
							$tIsland->{'slaughterer'} = $id; # �ԻԷϤ��˲�������ID��Ͽ
							logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1; # ������
							$HlandMove[$target][$tx][$ty] = 1;
						}
						next;
					} else {
						# �̾��Ϸ�
						logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						$island->{'ext'}[3]++ if (!$STcheck{$kind} && $tL == $HlandBase); # ���ˤ����ߥ�������Ϥο�
					}

					if (($tL == $HlandOil) ||
						($tL == $HlandSbase) ||
						($tL == $HlandSeaMine)) {
						# �Ǥ����ġ�������ϡ�������ä��鳤
						$tLand->[$tx][$ty] = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
						$HlandMove[$target][$tx][$ty] = 1;
					} elsif($tL == $HlandBouha) {
						# �Ǥ�������ʤ�����
						$tLand->[$tx][$ty] = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
						$HlandMove[$target][$tx][$ty] = 1;
					} elsif(($tL == $HlandDefence) && ($tLv >= 0)) {
						# �Ǥ��ѵ��ϤλĤäƤ����ɱһ��ߤʤ��Ѥ���
						$tLand->[$tx][$ty] = $HlandDefence;
						$tLandValue->[$tx][$ty] = $tLv;
					} else {
						# ���Ϥˤʤ�
						$tLand->[$tx][$ty] = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1; # ������
						$HlandMove[$target][$tx][$ty] = 1;
					}
				} 
			} # foreach
		} # while������ǥ롼��

		# ����������䤷�Ȥ�
		$count++;
	}

	unless ($flagbase) {
		# ���Ϥ���Ĥ�̵���ä����
		logMsNoBase($id, $name, $comName);
		return 0;
	}

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
		logMsMatome($id, $target, $name, $tName, $comName, $point, $tLandName, $str, $pntStr, join('-', (keys %damageId)), $STcheck{$kind});
	}
	# ��̱Ƚ��
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && ($id != $target) && !($STcheck{$kind})) {
		# ��̱ɺ��
		my($achive) = boatAchive($island, $boat); # ��ã��̱

		if ($achive > 0) {
			# �����Ǥ����夷����硢�����Ǥ�
			logMsBoatPeople($id, $name, $achive);
			$island->{'ext'}[4] += int($achive); # �߽Ф�����̱�ι�׿͸�

			# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
			if ($achive >= 200) {
				$island->{'achive'} += $achive;
			}
		}
	}

	return 1;
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ������˲��ä����ʤ�
sub logNoTarget {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�������˲��ä����ʤ�������ߤ���ޤ�����",$id);
}

# Φ���˲��ơ�����̿��
sub logMsLDMountain {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�Ͼä����ӡ����ϤȲ����ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# Φ���˲��ơ�������Ϥ�̿��
sub logMsLDSbase {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ�����ˤ��ä�<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# Φ���˲��ơ����ä�̿��
sub logMsLDMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}�����Ƥ���ȯ��Φ�Ϥ�<B>$tLname</B>���Ȥ���פ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# Φ���˲��ơ����ä�̿��ʳ���
sub logMsLDMonsterSea {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ�����ˤ���<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# Φ���˲��ơ�������ä�̿��
sub logMsLDHugeMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}�����Ƥ���ȯ��Φ�Ϥ�<B>$tLname</B>���Τΰ������Ȥ���פ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# Φ���˲��ơ�������ä�̿��ʳ���
sub logMsLDHugeMonsterSea {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ�����ˤ���<B>$tLname</B>���Τΰ������׷���ʤ��᤭���Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# Φ���˲��ơ�������̿��
sub logMsLDNavy {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}�����Ƥ���ȯ��Φ�Ϥ�<B>$tLname</B>���Ȥ���פ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# Φ���˲��ơ�������̿��ʳ����
sub logMsLDNavySea {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}�����ơ�Ʊ������ҹԤ��Ƥ���<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# Φ���˲��ơ�������̿��ʳ����
sub logMsLDNavySea2 {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ���������Ҥ��Ƥ���<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# Φ���˲��ơ�������̿��
sub logMsLDSea1 {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ����줬�������ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# Φ���˲��ơ�����¾���Ϸ���̿��
sub logMsLDLand {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�Φ�ϤϿ��פ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �ߥ����롢�����̿��
sub logMsSeaMine {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�Ͼä����Ӥޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �̾�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�϶줷��������Ӭ���ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# �̾�ߥ����롢���ä�̿�桢����
sub logMsMonKill {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>���ϿԤ����ݤ�ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# �̾�ߥ����롢������̿�桢����
sub logMsNavyPortDestroy {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�ϲ��Ǥ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �̾�ߥ����롢������̿�桢���᡼��
sub logMsNavyDamage {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�Ϲ����ʮ���Ф��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# �̾�ߥ����롢������̿�桢����
sub logMsNavyShipDestroy {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>��<span class='attention'>����</span>���ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# �̾�ߥ����롢�ĳ���̿�桢��������
sub logMsNavyWreckDestroy {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�ϳ��������Ȥʤ�ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �̾�ߥ������ɱһ��ߤ�̿��
sub logMsDefence {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>���ﳲ������ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# �̾�ߥ������ԻԷϤ�̿��
sub logMsNormalTown {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $sName, $st) = @_;
	my($logstr) = "��--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢<B>$sName</B>�ˤʤ�ޤ�����";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# ���äλ���
sub logMsMonMoney {
	my($id, $tId, $mName, $value, $st) = @_;
	my($logstr) = "��--- <B>$mName</B>�λĳ��ˤϡ�<B>$value$HunitMoney</B>���ͤ��դ��ޤ�����";
	if($st) {
		logSecret($logstr, $id) if($id == $tId);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId);
	}
}

# �ߥ������Ȥ��Ȥ��������Ϥ��ʤ�
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>�ߥ�������������ͭ���Ƥ��ʤ�</B>����˼¹ԤǤ��ޤ���Ǥ�����",$id);

}

# �ߥ�����(�ޤȤ�)
sub logMsMatome {
	my($id, $tId, $name, $tName, $comName, $point, $tLname, $str, $pntStr, $nId, $st) = @_;
	if($st) {
		logSecret("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����${str}${pntStr}",$id);
		logLate("<B>���Ԥ�</B>��${HtagName_}${tName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����${str}${pntStr}",$tId, $nId);
	} else {
		logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����${str}${pntStr}", $tId, $id, $nId);
	}
}

1;
