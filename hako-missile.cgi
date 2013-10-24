# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# ターン進行補助モジュール(ver1.00)
# 　ミサイル攻撃
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------

# ミサイル発射
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

	my($boat) = 0; # 難民の数
	my($flagbase)   = 0;
	my($xx, $yy, $tx, $ty, @pointErr);
	my(%damageId);
	my($mkind) = $kind - $HcomMissile[0];
	my($special) = $HmissileSpecial[$mkind];
	my($err) = $an[$HmissileErr[$mkind]]; # 誤差
	my($damage)= int($HmissileDamage[$mkind]);# 破壊力
	$damage = 1 if($damage < 1);

	# 着弾点からの拡散範囲
	my $range = 0;

	# 射程内に怪獣・巨大怪獣がいなければ、発射中止
	if($HtargetMonster &&
		!countAround($tIsland, $x, $y, $err, $HlandMonster, $HlandHugeMonster)) {
		logNoTarget($id, $name, $comName);
		return;
	}

	# 友好国設定を確認
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

	# 金が尽きるか指定数に足りるか基地全部が撃つまでループ
	my($bx, $by, $count, $fire) = (0, 0, 0, 0);
	my($bKind, $bLv, @terrorPnt);
	while (($arg > 0) && ($island->{'money'} >= $cost)) {
		# 基地を見つけるまでループ
		while ($count <= $island->{'pnum'}) {
			$bx = $island->{'rpx'}[$count];
			$by = $island->{'rpy'}[$count];
			$bKind = $land->[$bx][$by];
			$bLv   = $landValue->[$bx][$by];

			last if (($bKind == $HlandBase) || ($bKind == $HlandSbase));

			$count++;
		}

		# 見つからなかったらそこまで
		last if ($count > $island->{'pnum'});

		# 最低一つ基地があったので、flagを立てる
		$flagbase = 1;

		# 基地のレベルを算出
		my($level) = expToLevel($bKind, $bLv);


#$level = 14;
#$arg = 14;

		# 基地内でループ
		while (($level > 0) && ($arg > 0) && ($island->{'money'} > $cost)) {
			# 基地の最新状況を調べる
			$bKind = $land->[$bx][$by];
			$bLv   = $landValue->[$bx][$by];

			# 着弾点算出
			my($r) = random($err);
			$xx = $x + $ax[$r];
			$yy = $y + $ay[$r];
			# 行による位置調整
			$xx-- if(!($yy % 2) && ($y % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];

			if($special & 0x4) {
				if (($xx < 0) || ($yy < 0)) {
					# 範囲外の場合、絨毯爆撃しない
					$range = 0;
				} else {
					push(@terrorPnt, "($xx, $yy)");
					$range = $an[$HmissileTerrorHex[$mkind]] - 1;
				}
			}
			my(@order) = randomArray($range + 1);
			foreach my $loop (0..$range) {
				# 撃ったのが確定なので、各値を消耗させる
				$level--;
				$arg--;
				last if($level < 0 || $arg < 0 || $island->{'money'} < $cost);
				$fire++;
				$island->{'money'} -= $cost;
				$island->{'shellMoney'} += $cost;

				if(!$STcheck{$kind}) {
					$island->{'ext'}[1] += $cost; # 貢献度
					$island->{'ext'}[6]++; # 発射したミサイルの数
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
						# 味方に撃たれた場合貢献度マイナス(受けたミサイルの数はカウントしない)
						$tIsland->{'ext'}[1] -= $cost; # 貢献度
					} else {
						# 敵に撃たれた場合貢献度プラス
						$tIsland->{'ext'}[1] += $cost; # 貢献度
						$tIsland->{'ext'}[5]++; # 受けたミサイルの数
					}
					foreach (@{$tIsland->{'allyId'}}) {
						$Hally[$HidToAllyNumber{$_}]->{'ext'}[1]++;
					}
				}

				# 着弾点算出
				$tx = $xx + $ax[$order[$loop]];
				$ty = $yy + $ay[$order[$loop]];
				# 行による位置調整
				$tx-- if(!($ty % 2) && ($yy % 2));
				$tx = $correctX[$tx + $#an];
				$ty = $correctY[$ty + $#an];

				# 着弾点範囲内外チェック
				if (($tx < 0) || ($ty < 0)) {
					# 範囲外
					push(@pointErr, { 'OB' => $tPoint });
					next;
				}

				# 着弾点の地形等算出
				my($tL)     = $tLand->[$tx][$ty];
				my($tLv)    = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# 防衛施設判定
				my($defence) = 0;
				my($defflag) = 1;
				# 未判定領域
				if (($tL == $HlandDefence) || countAroundComplex($tIsland, $tx, $ty, $an[0], 0x20) ||
					countAroundNavySpecial($tIsland, $tx, $ty, 0x20, $an[0], 0)){
					# 防衛施設に命中
					if (($tL == $HlandDefence) && # 防衛施設で
						!($special & 0x2)) { # 陸地破壊以外
						if($amityFlag{$target}) { # 無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						# 防衛施設の耐久力を下げる
						$defflag = ($tLv % 100) - $damage;
						$tLv -= $damage;
						if($defflag < 0) {
							$tIsland->{'dbase'}--;
							$island->{'ext'}[2]++ if(!$STcheck{$kind}); # 破壊した防衛施設の数
						}
					}
				} elsif (countAroundDef($target, $tIsland, $tx, $ty, 0x20, @noDefenceIds)) {
					# 防衛範囲
					$defence = 1;
				}

				if ($defence) {
					# 空中爆破
					push(@pointErr, { 'DF' => $tPoint });
					$tIsland->{'ext'}[7]++; # 防衛施設で弾いたミサイルの数
					next;
				}

				# 「効果なし」hexを最初に判定
				if ((($tL == $HlandSea) && (!$tLv)) || # 深い海
					((($tL == $HlandSea) || # 海
					((($tL == $HlandSbase) || ($tL == $HlandSbase)) && !($special & 0x20)) || # 海底基地または機雷で潜水無効なし
					($tL == $HlandMountain))) && # 山
					!($special & 0x2)) { # 陸地破壊以外

					# 無効化
					push(@pointErr, { 'ND' => $tPoint });
					next;
				}

				# 海軍，怪獣，巨大怪獣以外の無害化
				if($amityFlag{$target} && $tL != $HlandNavy && $tL != $HlandMonster && $tL != $HlandHugeMonster) {
					if(random(100) < $HmissileSafetyInvalidp) {
						# 一定確率で誤爆
						push(@pointErr, { 'SS' => $tPoint });
					} else {
						push(@pointErr, { 'SZ' => $tPoint });
						next;
					}
				}

				# 弾の種類で分岐
				if ($special & 0x2) {
					# 陸地破壊弾
					my $seaflagLD = 1;
					if ($tL == $HlandMountain) {
						# 山(荒地になる)
						logMsLDMountain($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

						# 荒地になる
						$tLand->[$tx][$ty] = $HlandWaste;
						$tLandValue->[$tx][$ty] = 0;
						$HlandMove[$target][$tx][$ty] = 1;
						next;

					} elsif ($tL == $HlandComplex) {
						# 複合地形
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
						if(!(defined $HcomplexAfter[$cKind]->{'attack'}[0])) {
							# 攻撃後の地形が設定されていない場合，荒地になる
							logMsLDMountain($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

							# 荒地になる
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 0;
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}
						# その他
						logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandSbase) {
						# 海底基地
						$seaflagLD = 0; # 海になる
						logMsLDSbase($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandSeaMine) {
						# 機雷
						$seaflagLD = 0; # 海になる
						logMsSeaMine($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandMonster) {
						# 怪獣
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						if ($mFlag & 2) {
							# 海にいる
							$seaflagLD = 0; # 海になる
							logMsLDMonsterSea($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							# 陸にいる
							logMsLDMonster($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}
					} elsif ($tL == $HlandHugeMonster) {
						# 巨大怪獣
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
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
								# 行による位置調整
								$sx-- if(!($sy % 2) && ($ty % 2));
								$sx = $correctX[$sx + $#an];
								$sy = $correctY[$sy + $#an];
								# 範囲外
								next if(($sx < 0) || ($sy < 0));

								next if($tLand->[$sx][$sy] != $HlandHugeMonster);
								my($mId2, $mHflag2, $mSea2, $mExp2, $mFlag2, $mKind2, $mHp2) = monsterUnpack($tLandValue->[$sx][$sy]);
								next if($mHflag2 != $i);
								# コアの周囲が残っている場合攻撃無効
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
							# 海にいる
							logMsLDMonsterSea($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$seaflagLD = 0; # 海になる
						} else {
							# 陸にいる
							logMsLDMonster($id, $target, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}
					} elsif ($tL == $HlandNavy) {
						# 海軍
						my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($tLv);
						if($amityFlag{$nId} && !($nFlag & 1)) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
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
							# サバイバル
							$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
						}
						if ($nSpecial & 0x8) {
							# 港
							logMsLDNavy($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$tIsland->{'navyPort'}--;
						} else {
							# 艦艇
							if ($nFlag & 2) {
								# 潜水
								logMsLDNavySea2($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							} else {
								# 水上
								logMsLDNavySea($id, $target, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							}
							if(defined $n) {
								$Hislands[$n]->{'ships'}[$nNo]--;
								$Hislands[$n]->{'ships'}[4]--;
								$HnavyAttackTarget{"$id,$tx,$ty"} = undef;
							}
							$seaflagLD = 0; # 海になる
						}
					} elsif ($tL == $HlandSea) {
						# 浅瀬
						$seaflagLD = 0; # 海になる
						logMsLDSea1($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

					} elsif ($tL == $HlandCore) {
						# コア
						my($lFlag, $lLv) = (int($tLv / 10000), ($tLv % 10000));
						$tIsland->{'core'}--;
						$tIsland->{'slaughterer2'} = $id if($HcorelessDead && !$tIsland->{'core'}); # 破壊した島IDを記録
						if(!$lFlag) {
							logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							$seaflagLD = 0; # 海になる
							logMsLDSea1($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						}

					} else {
						# その他
						logMsLDLand($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});

						# 経験値
						if ($tL == $HlandTown) {
							if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
								# まだ基地の場合のみ
								$bLv += int($tLv / 20);
								$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
								$landValue->[$bx][$by] = $bLv;
								$tIsland->{'slaughterer'} = $id;
							}
						} elsif ($tL == $HlandOil) {
							$seaflagLD = 0; # 海になる
						}
					}

					# 浅瀬になる
					$tLand->[$tx][$ty] = $HlandSea;
					$tIsland->{'area'}--;
					$tLandValue->[$tx][$ty] = $seaflagLD;
					# でも油田、浅瀬、海底基地、機雷だったら海
					$HlandMove[$target][$tx][$ty] = 1;
				} else {
					# その他ミサイル
					if ($tL == $HlandWaste) {
						# 荒地(被害なし)
						push(@pointErr, { 'ND' => $tPoint });
					} elsif ($tL == $HlandSeaMine) {
						# 機雷
						logMsSeaMine($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
					} elsif ($tL == $HlandMonster) {
						# 怪獣
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $mName = landName($tL, $tLv);

						# 潜水中？
						if(($mFlag & 2) && !($special & 0x20)) {
							# 潜水中
							push(@pointErr, { 'MS' => $tPoint });
							next;
						}

						# 硬化中？
						if(($mFlag & 1) && !($special & 0x10)) {
							# 硬化中
							push(@pointErr, { 'MH' => $tPoint });
							next;
						} else {
							# 硬化中じゃない
							$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $target));
							if ($mHp <= $damage) {
								# 怪獣しとめた
								if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
									# 経験値
									$bLv += $HmonsterExp[$mKind];
									$island->{'gain'} += $HmonsterExp[$mKind];
									$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
									$landValue->[$bx][$by] = $bLv;
								}

								logMsMonKill($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});
								$HlandMove[$target][$tx][$ty] = 1;

								# 収入
								my($value) = $HmonsterValue[$mKind];
								if ($value > 0) {
									$tIsland->{'money'} += $value;
									logMsMonMoney($id, $target, $mName, $value, $STcheck{$kind});
								}

								# 賞関係
								my($prize) = $island->{'prize'};
								$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
								my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
								my($v) = 2 ** $mKind;
								$monsters |= $v;
								$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
								# 怪獣退治数
								$island->{'monsterkill'}++;

							} else {
								# 怪獣生きてる
								logMsMonster($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});

								# HPが1減る
								$tLandValue->[$tx][$ty] -= $damage;
								next;
							}
						}
						# 体の一部が消える
						if ($mFlag & 2) {
							# 海にいた
							$tLand->[$tx][$ty] = $HlandSea;
							$tLandValue->[$tx][$ty] = $mSea;
						} else {
							# 陸地にいた
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1;
						}
						$HlandMove[$target][$tx][$ty] = 1;
						next;
					} elsif ($tL == $HlandHugeMonster) {
						# 巨大怪獣
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLv);
						if($amityFlag{$mId}) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}
						my $mName = landName($tL, $tLv);

# コア以外へのミサイル攻撃も有効。無効にする場合はコメントをはずす。(コア防衛の能力をもたせている場合、悲惨です(^^;;;)
#						if($mHflag != 0) { 
#							push(@pointErr, { 'ND' => $tPoint });
#							next;
#						}

# 海にいる場合もミサイル有効。無効にする場合は、コメントをはずす。
						# 潜水中？
						if(($mFlag & 2) && !($special & 0x20)) {
							# 潜水中
							push(@pointErr, { 'MS' => $tPoint });
							next;
						}

						# 硬化中？
						if(($mFlag & 1) && !($special & 0x10)) {
							# 硬化中
							push(@pointErr, { 'MH' => $tPoint });
							next;
						} else {
							# 硬化中じゃない
							$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $target));
							if(($mHp <= $damage) && ($mHflag == 0)) {
								# 怪獣しとめた
								my($i, $sx, $sy, $flag);
								my $deflag = 0;

								foreach $i (0..6) {
									next if($HhugeMonsterImage[$mKind][$i] eq '');
									$sx = $tx + $ax[$i];
									$sy = $ty + $ay[$i];
									# 行による位置調整
									$sx-- if(!($sy % 2) && ($ty % 2));
									$sx = $correctX[$sx + $#an];
									$sy = $correctY[$sy + $#an];
									# 範囲外
									next if(($sx < 0) || ($sy < 0));

									next if($tLand->[$sx][$sy] != $HlandHugeMonster);
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($tLandValue->[$sx][$sy]))[1, 2, 4];
									next if($mHflag2 != $i);
									# コアの周囲が残っている場合攻撃無効
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
									# 経験値
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

								# 賞関係
								my($prize) = $island->{'prize'};
								$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
								my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
								my($v) = 2 ** $mKind;
								$hmonsters |= $v;
								$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
								# 怪獣退治数
								$island->{'monsterkill'}++;
								next;

							} else {
								# 怪獣生きてる
								my($i, $sx, $sy, $flag);
								my $deflag = 0;
								foreach $i (0..6) {
									next if($HhugeMonsterImage[$mKind][$i] eq '');
									$sx = $tx + $ax[$i];
									$sy = $ty + $ay[$i];
									# 行による位置調整
									$sx-- if(!($sy % 2) && ($ty % 2));
									$sx = $correctX[$sx + $#an];
									$sy = $correctY[$sy + $#an];
									# 範囲外
									next if(($sx < 0) || ($sy < 0));

									next if($tLand->[$sx][$sy] != $HlandHugeMonster);
									my($mId2, $mHflag2, $mSea2, $mExp2, $mFlag2, $mKind2, $mHp2) = monsterUnpack($tLandValue->[$sx][$sy]);
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($tLandValue->[$sx][$sy]))[1, 2, 4];
									next if($mHflag2 != $i);
									# コアの周囲が残っている場合攻撃無効
									if($HhugeMonsterSpecial[$mKind] & 0x10000) {
										$deflag = 1;
										push(@pointErr, { 'DF' => $tPoint });
										last;
									}
								}
								next if($deflag);
								# HPが1減る
								$mHp -= $damage;
								logMsMonster($id, $target, $mId, $name, $tName, $comName, $mName, $point, $tPoint, $STcheck{$kind});
								if($mHp > 0) {
									# 怪獣生きてる
									$tLandValue->[$tx][$ty] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
									next;
								}
							}
							# 体の一部が消える
							if ($mFlag & 2) {
								# 海にいた
								$tLand->[$tx][$ty] = $HlandSea;
								$tLandValue->[$tx][$ty] = $mSea;
							} else {
								# 陸地にいた
								$tLand->[$tx][$ty] = $HlandWaste;
								$tLandValue->[$tx][$ty] = 1;
							}
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}
					} elsif ($tL == $HlandNavy) {
						# 海軍
						my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($tLv);
						my $n = $HidToNumber{$nId};
						my $nSpecial = $HnavySpecial[$nKind];
						my $nName = landName($tL, $tLv);

						# 潜水中？
						if(($nFlag & 2) && !($special & 0x20)) {
							# 潜水中
							push(@pointErr, { 'FS' => $tPoint });
							next;
						}

						# 残骸？
						if ($nFlag & 1) {
							# 残骸
							logMsNavyWreckDestroy($id, $target, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

							# 海になる
							$tLand->[$tx][$ty] = $HlandSea;
							$tLandValue->[$tx][$ty] = 0;
							$HlandMove[$target][$tx][$ty] = 1;
							next;
						}

						if($amityFlag{$nId}) { #無害化
							if(random(100) < $HmissileSafetyInvalidp) {
								# 一定確率で誤爆
								push(@pointErr, { 'SS' => $tPoint });
							} else {
								push(@pointErr, { 'SZ' => $tPoint });
								next;
							}
						}

						$damageId{$nId} = 1 if($nId && ($nId != $id) && ($nId != $target));
						if ($nHp <= $damage) {
							# 撃沈
							if (($bKind == $HlandBase) || ($bKind == $HlandSbase)) {
								# 経験値
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
								# サバイバル
								$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
							}
							if ($nSpecial & 0x8) {
								# 軍港壊滅
								logMsNavyPortDestroy($id, $target, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

								# 浅瀬になる
								$tLand->[$tx][$ty] = $HlandSea;
								$tLandValue->[$tx][$ty] = 1;
								$HlandMove[$target][$tx][$ty] = 1;
								$Hislands[$n]->{'navyPort'}-- if(defined $n);
							} else {
								# 艦艇撃沈
								logMsNavyShipDestroy($id, $target, $nId, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

								if (rand(100) < $HnavyProbWreck[$nKind]) {
									# 残骸になる
									$tLandValue->[$tx][$ty] = navyPack(0, $nTmp, $nStat, $nSea, int(rand(90)) + 10, 1, 0, $nKind, 0);
								} else {
									# 海になる
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
							# 被弾
							logMsNavyDamage($id, $target, $nId, $name, $tName, $comName, $nName, $point, $tPoint, $STcheck{$kind});

							# HPが1減る
							$tLandValue->[$tx][$ty] -= $damage;
							next;
						}
					} elsif (($tL == $HlandDefence) && ($tLv >= 0)) {
						# 防衛施設（耐久力が残っている）
						logMsDefence($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
					} elsif ($tL == $HlandCore) {
						# コア
						my($lFlag, $lLv) = (int($tLv / 10000), ($tLv % 10000));
						if(($lFlag == 2) && !($special & 0x20)) {
							# 海底施設は海のふり
							push(@pointErr, { 'ND' => $tPoint });
							next;
						}
						# 耐久力を下げる
						my $coreflag = $lLv - $damage;
						$tLv -= $damage;
						if($coreflag >= 0) {
							$tLand->[$tx][$ty] = $HlandCore;
							$tLandValue->[$tx][$ty] = $tLv;
							logMsDefence($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						} else {
							$tIsland->{'core'}--;
							$tIsland->{'slaughterer2'} = $id if($HcorelessDead && !$tIsland->{'core'}); # 破壊した島IDを記録
							if(!$lFlag) {
								$tLand->[$tx][$ty] = $HlandWaste;
								$tLandValue->[$tx][$ty] = 1; # 着弾点
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
						# 複合地形
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
						# 攻撃後の地形にする
						# 複合地形なら設定地形
						$tLand->[$tx][$ty] = $HcomplexAfter[$cKind]->{'attack'}[0];
						$tLandValue->[$tx][$ty] = $HcomplexAfter[$cKind]->{'attack'}[1];
						$island->{'complex'}[$cKind]--;
						$HlandMove[$target][$tx][$ty] = 1;
						logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						next;
					} elsif ($tL == $HlandTown) {
						# 都市系
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
							# 経験値
							$bLv += int(($tLv - $sLv) / 20);
							$bLv = $HmaxExpPoint if ($bLv > $HmaxExpPoint);
							$landValue->[$bx][$by] = $bLv;
						}
						$boat += ($tLv - $sLv); # 難民にプラス
						if($rank) {
							$tLandValue->[$tx][$ty] = $sLv;
							logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $HlandTownName[$rank], $STcheck{$kind});
						} else {
							$tIsland->{'slaughterer'} = $id; # 都市系を破壊した島IDを記録
							logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
							$tLand->[$tx][$ty] = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1; # 着弾点
							$HlandMove[$target][$tx][$ty] = 1;
						}
						next;
					} else {
						# 通常地形
						logMsNormal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $STcheck{$kind});
						$island->{'ext'}[3]++ if (!$STcheck{$kind} && $tL == $HlandBase); # 撃破したミサイル基地の数
					}

					if (($tL == $HlandOil) ||
						($tL == $HlandSbase) ||
						($tL == $HlandSeaMine)) {
						# でも油田、海底基地、機雷だったら海
						$tLand->[$tx][$ty] = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
						$HlandMove[$target][$tx][$ty] = 1;
					} elsif($tL == $HlandBouha) {
						# でも防波堤なら浅瀬
						$tLand->[$tx][$ty] = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
						$HlandMove[$target][$tx][$ty] = 1;
					} elsif(($tL == $HlandDefence) && ($tLv >= 0)) {
						# でも耐久力の残っている防衛施設なら耐える
						$tLand->[$tx][$ty] = $HlandDefence;
						$tLandValue->[$tx][$ty] = $tLv;
					} else {
						# 荒地になる
						$tLand->[$tx][$ty] = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1; # 着弾点
						$HlandMove[$target][$tx][$ty] = 1;
					}
				} 
			} # foreach
		} # while基地内でループ

		# カウント増やしとく
		$count++;
	}

	unless ($flagbase) {
		# 基地が一つも無かった場合
		logMsNoBase($id, $name, $comName);
		return 0;
	}

	if($fire) {
		my $l;
		my @pKey  = ('OB', 'DF', 'ND', 'MS', 'MH', 'FS', 'SZ', 'SS');
		my @pName = ('圏外', '防衛', '無効', '怪潜', '硬化', '艦潜', '無害', '誤爆');
		my $str = '';
		my $pntStr = '<BR>　--- ';
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
				$pntStr .= "$pName[$l] ⇒ " . join(',', @pointOut) . "　" if($l);
			}
		}
		$pntStr = '' if(!$cntErr[8] || ($cntErr[8] == $cntErr[0]));
		$pntStr .= '[絨爆中心 ⇒ ' . join(',', @terrorPnt) .']' if(@terrorPnt);
		$str = '(命中:' . ($fire - $cntErr[8]) . $str .')';
		$str .= '[破壊力:' . $damage . ']' if($damage > 1);
		logMsMatome($id, $target, $name, $tName, $comName, $point, $tLandName, $str, $pntStr, join('-', (keys %damageId)), $STcheck{$kind});
	}
	# 難民判定
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && ($id != $target) && !($STcheck{$kind})) {
		# 難民漂着
		my($achive) = boatAchive($island, $boat); # 到達難民

		if ($achive > 0) {
			# 少しでも到着した場合、ログを吐く
			logMsBoatPeople($id, $name, $achive);
			$island->{'ext'}[4] += int($achive); # 救出した難民の合計人口

			# 難民の数が一定数以上なら、平和賞の可能性あり
			if ($achive >= 200) {
				$island->{'achive'} += $achive;
			}
		}
	}

	return 1;
}

#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------
# 射程内に怪獣がいない
sub logNoTarget {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、射程内に怪獣がいないため中止されました。",$id);
}

# 陸地破壊弾、山に命中
sub logMsLDMountain {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は消し飛び、荒地と化しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 陸地破壊弾、海底基地に命中
sub logMsLDSbase {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着水後爆発、同地点にあった<B>$tLname</B>は跡形もなく吹き飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 陸地破壊弾、怪獣に命中
sub logMsLDMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>$tLname</B>もろとも水没しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 陸地破壊弾、怪獣に命中（海）
sub logMsLDMonsterSea {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着水後爆発。同地点にいた<B>$tLname</B>は跡形もなく吹き飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 陸地破壊弾、巨大怪獣に命中
sub logMsLDHugeMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>$tLname</B>の体の一部もろとも水没しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 陸地破壊弾、巨大怪獣に命中（海）
sub logMsLDHugeMonsterSea {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着水後爆発。同地点にいた<B>$tLname</B>の体の一部は跡形もなく吹き飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 陸地破壊弾、海軍に命中
sub logMsLDNavy {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>$tLname</B>もろとも水没しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# 陸地破壊弾、海軍に命中（海上）
sub logMsLDNavySea {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着弾。同地点を航行していた<B>$tLname</B>は跡形もなく吹き飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# 陸地破壊弾、海軍に命中（海中）
sub logMsLDNavySea2 {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}に着水後爆発。同地点で潜航していた<B>$tLname</B>は跡形もなく吹き飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# 陸地破壊弾、浅瀬に命中
sub logMsLDSea1 {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。海底がえぐられました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 陸地破壊弾、その他の地形に命中
sub logMsLDLand {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。陸地は水没しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# ミサイル、機雷に命中
sub logMsSeaMine {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は消し飛びました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 通常ミサイル、怪獣に命中、ダメージ
sub logMsMonster {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は苦しそうに咆哮しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 通常ミサイル、怪獣に命中、殺傷
sub logMsMonKill {
	my($id, $tId, $mId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は力尽き、倒れました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $mId);
	} else {
		logOut($logstr, $tId, $id, $mId);
	}
}

# 通常ミサイル、軍港に命中、壊滅
sub logMsNavyPortDestroy {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は壊滅しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 通常ミサイル、艦艇に命中、ダメージ
sub logMsNavyDamage {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は黒煙を噴き出しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# 通常ミサイル、艦艇に命中、撃沈
sub logMsNavyShipDestroy {
	my($id, $tId, $nId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は<span class='attention'>沈没</span>しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId, $nId);
	} else {
		logOut($logstr, $tId, $id, $nId);
	}
}

# 通常ミサイル、残骸に命中、海の藻屑
sub logMsNavyWreckDestroy {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は海の藻屑となりました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 通常ミサイル防衛施設に命中
sub logMsDefence {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は被害を受けました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 通常ミサイル都市系に命中
sub logMsNormalTown {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $sName, $st) = @_;
	my($logstr) = "　--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、<B>$sName</B>になりました。";
	if($st) {
		logSecret($logstr, $id);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId, $id);
	}
}

# 怪獣の死体
sub logMsMonMoney {
	my($id, $tId, $mName, $value, $st) = @_;
	my($logstr) = "　--- <B>$mName</B>の残骸には、<B>$value$HunitMoney</B>の値が付きました。";
	if($st) {
		logSecret($logstr, $id) if($id == $tId);
		logLate($logstr, $tId);
	} else {
		logOut($logstr, $tId);
	}
}

# ミサイル撃とうとしたが基地がない
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>ミサイル設備を保有していない</B>ために実行できませんでした。",$id);

}

# ミサイル(まとめ)
sub logMsMatome {
	my($id, $tId, $name, $tName, $comName, $point, $tLname, $str, $pntStr, $nId, $st) = @_;
	if($st) {
		logSecret("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いました。${str}${pntStr}",$id);
		logLate("<B>何者か</B>が${HtagName_}${tName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いました。${str}${pntStr}",$tId, $nId);
	} else {
		logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いました。${str}${pntStr}", $tId, $id, $nId);
	}
}

1;
