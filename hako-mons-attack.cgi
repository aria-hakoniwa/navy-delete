#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# ターン進行補助モジュール(ver1.00)
# 　怪獣の能力 ミサイル攻撃
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------

# 怪獣のミサイル攻撃目標を探す
sub searchMonsterTarget {
	my($island, $x, $y, $huge) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($lv)        = $landValue->[$x][$y];
	my($lv2)        = $landValue2->[$x][$y];

	# 各要素の取り出し
	my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$x][$y]);
	my $mName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = ($huge) ? $HhugeMonsterSpecial[$mKind] : $HmonsterSpecial[$mKind];

	return unless($special & 0x100);

	# 難民の数
	my($boat) = 0;

	my $rtemp = ($huge) ? $HhugeMonsterFireRange[$mKind] : $HmonsterFireRange[$mKind];
	my $range = $an[$rtemp];

	# 範囲内の目標地形を探す
	my($i, $sx, $sy, $kind, $tId, $tLv, $tFlag);
	# 順番決め
	my $rang = $range - 2;
	my(@order) = randomArray($rang);
	foreach $i (0..$rang) {
		my $j = $order[$i] + 1;
		$sx = $x + $ax[$j];
		$sy = $y + $ay[$j];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		# 範囲内の場合
		$tKind = $land->[$sx][$sy];
		$tLv   = $landValue->[$sx][$sy];

		my $target = { x => $sx, y => $sy };

		if ($mFlag & 1) {
			# 硬化中なら、なにもしない
		} elsif ($mFlag & 2) {
			# 硬化中でなく、海にいた
			# 対潜、対艦攻撃
			if ($tKind == $HlandNavy) {
				# 海軍
				($tId, $tFlag) = (navyUnpack($tLv))[0, 5];
				if (($mId != $tId) && !($tFlag & 1)) {
					# 味方の艦艇ではない残骸以外
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			} elsif (($tKind == $HlandSbase) || # 海底基地
				($tKind == $HlandOil)) {   # 海底油田
				if ($id != $mId) {
					# 味方の施設ではない
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			} elsif($tKind == $HlandComplex) { # 複合地形
				if ($id != $mId) {
					# 味方の施設ではない
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					next if(!($HcomplexAttr[$cKind] & 0x100)); # 対潜
					if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind] || $HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]) {
						# 攻撃目標設定
						$HmonsterAttackTarget{"$id,$x,$y"} = $target;
						last;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# 怪獣
				($tId, $tFlag) = (monsterUnpack($tLv))[0, 4];
				if (($mId != $tId) && !($tFlag & 1) && ($tFlag & 2)) {
					# 硬化中でなく、海にいる
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			}
		} elsif (!($mFlag & 2)) {
			# 陸にいた
			# 対艦攻撃
			if ($tKind == $HlandNavy) {
				# 海軍
				($tId, $tFlag) = (navyUnpack($tLv))[0, 5];
				if (($mId != $tId) && !($tFlag & 2) && !($tFlag & 1)) {
					# 味方の艦艇ではない浮上中の残骸以外
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}

			# 対地攻撃
			} elsif (($tKind == $HlandTown) || # 町系
				($tKind == $HlandForest) || # 森
				($tKind == $HlandFarm) || # 農場
				($tKind == $HlandFactory) || # 工場
				($tKind == $HlandBase) || # ミサイル基地
				($tKind == $HlandDefence) || # 防衛施設
				($tKind == $HlandMonument) || # 記念碑
				($tKind == $HlandHaribote)) { # ハリボテ
				if ($id != $mId) {
					# 味方の施設ではない
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}

			} elsif($tKind == $HlandComplex) {  # 複合地形
				if ($id != $mId) {
					# 味方の施設ではない
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					next if(!($HcomplexAttr[$cKind] & 0x600)); # 対艦・対地
					if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind] || $HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]) {
						# 攻撃目標設定
						$HmonsterAttackTarget{"$id,$x,$y"} = $target;
						last;
					}
				}

			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# 怪獣
				($tId, $tFlag) = (monsterUnpack($tLv))[0, 4];
				if (($mId != $tId) && !($tFlag & 1) && !($tFlag & 2)) {
					# 硬化中でなく、陸にいる
					# 攻撃目標設定
					$HmonsterAttackTarget{"$id,$x,$y"} = $target;
					last;
				}
			}
		}
	}
}

# 怪獣のミサイル攻撃
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

	# 友好国設定を確認
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

	# 攻撃回数
	my $rtemp = ($huge) ? $HhugeMonsterFireHex[$mKind] : $HmonsterFireHex[$mKind];
	my $err = $an[$rtemp]; # 誤差
	my $mFire = ($huge) ? $HhugeMonsterFire[$mKind] : $HmonsterFire[$mKind];
	$mFire += int($mExp/$mHp) if($mHp); # 攻撃回数(経験値があがるか瀕死になると増える)
	$mFire = $HmonsterFireMax if($HmonsterFireMax && ($mFire > $HmonsterFireMax));
	# 破壊力
	my $damage = ($huge) ? $HhugeMonsterDamage[$mKind] : $HmonsterDamage[$mKind];
	$damage = int($damage);
	$damage = 1 if($damage < 1);
	# 着弾点からの拡散範囲
	my $terrorhex = ($huge) ? $HhugeMonsterTerrorHex[$mKind] : $HmonsterTerrorHex[$mKind];
	my $range = 0;

	# 攻撃する
	my($r, $xx, $yy, $fx, $fy, $fPoint, $fKind, $fLv, $fLv2, @pointErr, @terrorPnt);
	my(%damageId);
	my $loopflag = 0;
	my $fire = 0;
	while ($fire < $mFire) {
		last if($loopflag); # 費用不足か残骸で攻撃終了

		# 着弾点算出
		$r = int(rand($err));
		$xx = $tx + $ax[$r];
		$yy = $ty + $ay[$r];
		# 行による位置調整
		$xx-- if(!($yy % 2) && ($ty % 2));
		$xx = $correctX[$xx + $#an];
		$yy = $correctY[$yy + $#an];

		# 自爆をしない場合
		if(!$HmonsterSelfAttack && ($xx == $x) && ($yy == $y)) {
			$r += int(1 + rand($err-1));
			$r -= $err if($r >= $err);
			$xx = $tx + $ax[$r];
			$yy = $ty + $ay[$r];
			# 行による位置調整
			$xx-- if(!($yy % 2) && ($ty % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];
		}

		if($special & 0x200) {
			if (($xx < 0) || ($yy < 0)) {
				# 範囲外の場合、絨毯爆撃しない
				$range = 0;
			} else {
				push(@terrorPnt, "($xx, $yy)");
				$range = $an[$terrorhex] - 1;
			}
		}
		my(@order) = randomArray($range + 1);
		foreach my $loop (0..$range) {
			# 海になってたら、攻撃終了(自爆を許す場合、必要)
			#return ($mId, $mExp, $mFlag, $mKind, $mHp) if($landValue->[$x][$y] == 0);
			if(($land->[$x][$y] != $HlandMonster) && ($land->[$x][$y] != $HlandHugeMonster)) {
				$loopflag = 1;
				last;
			}

			# 既定攻撃回数終了
			last if($fire >= $mFire);

#			# 弾薬費用を引く
#			if (defined $mn) {
#				$mIsland->{'money'} -= 1;
#				if ($mIsland->{'money'} < 0) {
#					# 弾薬費用が足りない
#					$mIsland->{'money'} = 0;
#					logNavyNoShell($id, $mId, $name, $mPoint, $mName);
#					$loopflag = 1;
#					last;
#				}
#			}

			$fire++;
			# 着弾点算出
			$fx = $xx + $ax[$order[$loop]];
			$fy = $yy + $ay[$order[$loop]];
			# 行による位置調整
			$fx-- if(!($fy % 2) && ($yy % 2));
			$fx = $correctX[$fx + $#an];
			$fy = $correctY[$fy + $#an];

			$fPoint = "($fx, $fy)";
			if (($fx < 0) || ($fy < 0)) {
				# 範囲外の場合
				push(@pointErr, { 'OB' => $fPoint });
				next;
			}
			$fL  = $land->[$fx][$fy];
			$fLv = $landValue->[$fx][$fy];
			$fLv2 = $landValue2->[$fx][$fy];
			$fName  = landName($fL, $fLv);
			# 防衛施設判定
			my($defence) = 0;
			# 未判定領域
			if (($fL == $HlandDefence) || countAroundComplex($island, $fx, $fy, $an[0], 0x40) ||
				countAroundNavySpecial($island, $fx, $fy, 0x20, $an[0], 0)){
				# 防衛施設に命中
				if ($fL == $HlandDefence) { # 防衛施設で
					if($amityFlag{$id}) { # 無害化
						if(random(100) < $HmonsterSafetyInvalidp) {
							# 一定確率で誤爆
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					# 防衛施設の耐久力を下げる
					$defflag = ($fLv % 100) - $damage;
					$fLv -= $damage;
					if($defflag < 0) {
						$island->{'dbase'}--;
						$island->{'ext'}[2]++ if(defined $mn); # 破壊した防衛施設の数
					}
				}
			} elsif (countAroundDef($id, $island, $fx, $fy, 0x20, @noDefenceIds)) {
				# 防衛範囲
				$defence = 1;
			}

			if ($defence) {
				if($mFlag & 2) {
					# 海にいる時は、防衛されない
				} else {
					# 防衛された
					push(@pointErr, { 'DF' => $fPoint });
					next;
				}
			}

			if (!($mFlag & 2)) {
				# 陸にいる時、効果のない地形
				if (($fL == $HlandSea)      || # 海
					($fL == $HlandMountain) || # 山
					($fL == $HlandWaste)    || # 荒地
					($fL == $HlandSbase)) {    # 海底基地
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}
			} elsif (($mFlag & 2)) {
				# 海にいる時、効果のない地形
				if(($fL == $HlandSea) || # 海
					($fL == $HlandWaste) || # 荒地
					($fL == $HlandPlains) || # 平地
					($fL == $HlandTown) || # 町系
					($fL == $HlandForest) || # 森
					($fL == $HlandFarm) || # 農場
					($fL == $HlandFactory) || # 工場
					($fL == $HlandBase) || # ミサイル基地
					($fL == $HlandDefence) || # 防衛施設
					($fL == $HlandMountain) || # 山
					($fL == $HlandMonument) || # 記念碑
					($fL == $HlandHaribote)) { # ハリボテ
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}
			}

			# 海軍，怪獣，巨大怪獣以外の無害化
			if($amityFlag{$id} && $fL != $HlandNavy && $fL != $HlandMonster && $fL != $HlandHugeMonster) {
				if(random(100) < $HmonsterSafetyInvalidp) {
					# 一定確率で誤爆
					push(@pointErr, { 'SS' => $fPoint });
				} else {
					push(@pointErr, { 'SZ' => $fPoint });
					next;
				}
			}

			# 特別な地形
			if ($fL == $HlandComplex) {  # 複合地形
				my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($fLv);
				$island->{'ext'}[5]++;
				# 効果のある地形
				if( (($mFlag & 2) && ($HcomplexAttr[$cKind] & 0x100)) ||  # 海にいる時（対潜、対艦）
					(!($mFlag & 2) && ($HcomplexAttr[$cKind] & 0x600)) ) {  # 陸にいる時（対艦、対地）

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
					# 攻撃後の地形にする
					# 複合地形なら設定地形
					$land->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[0];
					$landValue->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[1];
					$HlandMove[$id][$fx][$fy] = 1;

					logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
					next;
				}
				# 効果のない地形
				push(@pointErr, { 'ND' => $fPoint });
				next;
			} elsif ($fL == $HlandMonster) {  # 怪獣
				my($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp) = monsterUnpack($fLv);
				my $fName = $HmonsterName[$fKind];

				# 海どうしか陸どうしでなければ無効
				if (!($mFlag & 2) && ($fFlag & 2)) {
					push(@pointErr, { 'MS' => $fPoint });
					next;
				} elsif(($mFlag & 2) && !($fFlag & 2)) {
					# 海から陸にいる怪獣を攻撃できない
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}

				# 硬化中？
				if ($fFlag & 1) {
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# 硬化中じゃない
					if($amityFlag{$fId}) { # 無害化
						if(random(100) < $HmonsterSafetyInvalidp) {
							# 一定確率で誤爆
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$fId} = 1 if($fId && ($fId != $id) && ($fId != $mId));
					if ($fHp <= $damage) {
						# 怪獣しとめた
						# 経験値
						$mExp += $HmonsterExp[$fKind]; # 怪獣の経験値は最高で255
						$mIsland->{'gain'} += $HmonsterExp[$mKind] if(defined $mn);
						$mExp = 250 if($mExp > 250);
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);

						logNavyMonKill($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);

						# 収入
#						if (defined $mn) {
#							my($value) = $HmonsterValue[$mKind];
#							if ($value > 0) {
#								$mIsland->{'money'} += $value;
#								logMsMonMoney($id, $mName, $value);
#							}

							# 賞関係
#							my($prize) = $mIsland->{'prize'};
#							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
#							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
#							my($v) = 2 ** $mKind;
#							$monsters |= $v;
#							$mIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# 怪獣退治数
#							$mIsland->{'monsterkill'}++;
#						}

					} else {
						# 怪獣生きてる
						logNavyMonster($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);
						# HPが1減る
						#$landValue->[$fx][$fy]--;
						$fHp -= $damage;
						if($fHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp);
							next;
						}
					}
					if ($fFlag & 2) {
						# 海にいた
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $mSea;
					} else {
						# 陸地にいた
						$land->[$fx][$fy] = $HlandWaste;
						$landValue->[$fx][$fy] = 0;
					}
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}
			} elsif ($fL == $HlandHugeMonster) {  # 巨大怪獣
				my($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp) = monsterUnpack($fLv);
				my $fName = $HhugeMonsterName[$fKind];

				# 海どうしか陸どうしでなければ無効
				if (!($mFlag & 2) && ($fFlag & 2)) {
					push(@pointErr, { 'MS' => $fPoint });
					next;
				} elsif(($mFlag & 2) && !($fFlag & 2)) {
					# 海から陸にいる怪獣を攻撃できない
					push(@pointErr, { 'ND' => $fPoint });
					next;
				}

				# 硬化中？
				if ($fFlag & 1) {
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# 硬化中じゃない
					if($amityFlag{$fId}) { # 無害化
						if(random(100) < $HmonsterSafetyInvalidp) {
							# 一定確率で誤爆
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$fId} = 1 if($fId && ($fId != $id) && ($fId != $mId));
					if (($fHp <= $damage) && ($fHflag == 0)) {
						# 怪獣しとめた
						# 巨大怪獣処理
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$fKind][$j] eq '');
							$ssx = $sx + $ax[$j];
							$ssy = $sy + $ay[$j];
							# 行による位置調整
							$ssx-- if(!($ssy % 2) && ($sy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# 範囲外
							next if(($ssx < 0) || ($ssy < 0));

							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# 各要素の取り出し
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# コアの周囲が残っている場合攻撃無効
							if($HhugeMonsterSpecial[$fKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							} elsif ($mFlag2 & 2) {
								# 海にいた
								$land->[$ssx][$ssy] = $HlandSea;
								$landValue->[$ssx][$ssy] = $mSea2;
								$HlandMove[$id][$ssx][$ssy] = 1;
							} else {
								# 陸地にいた
								$land->[$ssx][$ssy] = $HlandWaste;
								$landValue->[$ssx][$ssy] = 0;
								$HlandMove[$id][$ssx][$ssy] = 1;
							}
						}
						next if($deflag);
						# 経験値
						$mExp += $HhugeMonsterExp[$fKind]; # 怪獣の経験値は最高で255
						$mIsland->{'gain'} += $HhugeMonsterExp[$fKind] if(defined $mn);
						$mExp = 250 if($mExp > 250);
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);

						logNavyMonKill($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);

						# 収入
#						if (defined $mn) {
#							my($value) = $HmonsterValue[$mKind];
#							if ($value > 0) {
#								$mIsland->{'money'} += $value;
#								logMsMonMoney($id, $mName, $value);
#							}

							# 賞関係
#							my($prize) = $mIsland->{'prize'};
#							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
#							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
#							my($v) = 2 ** $mKind;
#							$hmonsters |= $v;
#							$mIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# 怪獣退治数
#							$mIsland->{'monsterkill'}++;
#						}

					} else {
						# 怪獣生きてる
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$fKind][$j] eq '');
							$ssx = $sx + $ax[$j];
							$ssy = $sy + $ay[$j];
							# 行による位置調整
							$ssx-- if(!($ssy % 2) && ($sy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# 範囲外
							next if(($ssx < 0) || ($ssy < 0));
							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# 各要素の取り出し
							my($mHflag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1];
							next if($mHflag2 != $j);
							# コアの周囲が残っている場合攻撃無効
							if($HhugeMonsterSpecial[$fKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							}
						}
						next if($deflag);
						logNavyMonster($id, $name, $mId, $mPoint, $mName, $tPoint, $fId, $fName, $fPoint);
						# HPが1減る
						$fHp -= $damage;
						if($fHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($fId, $fHflag, $fSea, $fExp, $fFlag, $fKind, $fHp);
							next;
						}
					}
					if ($fFlag & 2) {
						# 海にいた
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $mSea;
					} else {
						# 陸地にいた
						$land->[$fx][$fy] = $HlandWaste;
						$landValue->[$fx][$fy] = 0;
					}
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}
			} elsif ($fL == $HlandNavy) { # 海軍
				my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $nWait2, $nHp2, $ngoalx, $ngoaly) = navyUnpack($fLv, $fLv2);
				my $nSpecial2 = $HnavySpecial[$nKind2];
				my $nName2 = landName($fL, $fLv);

				# 潜水中？
				if (!($mFlag & 2) && ($nFlag2 & 2)) {
					# 怪獣が陸にいて艦艇が潜水中
					push(@pointErr, { 'FS' => $fPoint });
					next;
				}

				# 残骸？
				if ($nFlag2 & 1) {
					logNavyWreckDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nName2, $fPoint);
					# 海になる
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = 0;
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}

				if($amityFlag{$nId2}) { # 無害化
					if(random(100) < $HmonsterSafetyInvalidp) {
						# 一定確率で誤爆
						push(@pointErr, { 'SS' => $fPoint });
					} else {
						push(@pointErr, { 'SZ' => $fPoint });
						next;
					}
				}

				$damageId{$nId2} = 1 if($nId2 && ($nId2 != $id) && ($nId2 != $mId));
				if ($nHp2 <= $damage) {
					# 撃沈

					# 経験値
					$mExp += $HnavyExp[$nKind2]; # 怪獣の経験値は最高で255
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
						# サバイバル
						$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					if ($nSpecial2 & 0x8) {
						# 軍港壊滅
						logNavyPortDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);
						# 浅瀬になる
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = 1;
						$HlandMove[$id][$fx][$fy] = 1;
						$Hislands[$n]->{'navyPort'}-- if(defined $n);
					} else {
						# 艦艇撃沈
						logNavyShipDestroy($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);

						if (rand(100) < $HnavyProbWreck[$nKind]) {
							# 残骸になる
							$landValue->[$fx][$fy] = navyPack(0, $nTmp2, $nStat2, $nSea2, int(rand(90)) + 10, 1, 0, $nKind2, 0, 0, 31, 31);
						} else {
							# 海になる
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
					# 被弾
					logNavyDamage($id, $name, $mId, $mPoint, $mName, $tPoint, $nId2, $nName2, $fPoint);

					# HPが1減る
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
				# 機雷
				logNavySeaMine($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);

				$land->[$fx][$fy]      = $HlandSea; # 深い海
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
				next;
			} elsif (($fL == $HlandDefence) && ($fLv >= 0)) {
				# 防衛施設（耐久力が残っている）
				logNavyNormalDefence($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
			} elsif ($fL == $HlandCore) {
				# コア
				my($lFlag, $lLv) = (int($fLv / 10000), ($fLv % 10000));
				if( !(($mFlag & 2) && ($lFlag >= 1)) && !(!($mFlag & 2) && ($lFlag <= 1)) )  {
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
				# 耐久力を下げる
				my $coreflag = $lLv - $damage;
				$fLv -= $damage;
				# コア爆撃数，コア破壊数
				#$nIsland->{'epoint'}{$id}++ if((defined $nn) && ($island->{'event'}[6] == 6) || (($coreflag < 0) && ($island->{'event'}[6] == 7)) && ($island->{'event'}[1] <= $HislandTurn));
				if($coreflag >= 0) {
					$land->[$fx][$fy] = $HlandCore;
					$landValue->[$fx][$fy] = $fLv;
					logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} else {
					$island->{'core'}--;
					$island->{'slaughterer2'} = $mId if($HcorelessDead && (defined $mn) && !$island->{'core'}); # 破壊した島IDを記録
					if ($mFlag & 2) {
						# 対潜
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} else {
						# 対艦、対地
						logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					}
					if(!$lFlag) {
						$land->[$fx][$fy] = $HlandWaste; # 荒地（着弾点）
						$landValue->[$fx][$fy] = 1;
					} else {
						$land->[$fx][$fy] = $HlandSea; # 海
						$landValue->[$fx][$fy] = 2 - $lFlag;
					}
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} elsif ($fL == $HlandTown) {
				# 都市系
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
				$mExp += int($fLv / 20); # 怪獣の経験値は最高で255
				$mExp = 250 if($mExp > 250);
				$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
				$boat += ($fLv - $sLv); # 難民にプラス
				if($rank) {
					$landValue->[$fx][$fy] = $sLv;
					logNavyNormalTown($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint, $HlandTownName[$rank]);
				} else {
					$island->{'slaughterer'} = $mId if(defined $mn); # 都市系を破壊した島IDを記録
					logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
					$land->[$fx][$fy]      = $HlandWaste;
					$landValue->[$fx][$fy] = 1; # 着弾点
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} else {
				# その他の地形
				logNavyNormal($id, $name, $mId, $mPoint, $mName, $tPoint, $fName, $fPoint);
				if ($fKind == $HlandBase && (defined $mn)) {
					$mIsland->{'ext'}[3]++; # 撃破したミサイル基地の数
				}
			}

			# 攻撃後の地形にする
			if (($fL == $HlandOil) ||
				($fL == $HlandSeaMine)) {
				# でも油田、機雷だったら海
				$land->[$fx][$fy] = $HlandSea;
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
			} elsif($fL == $HlandBouha) {
				# でも防波堤なら浅瀬
				$land->[$fx][$fy] = $HlandSea;
				$landValue->[$fx][$fy] = 1;
				$HlandMove[$id][$fx][$fy] = 1;
			} elsif(($fL == $HlandDefence) && ($fLv >= 0)) {
				# でも耐久力の残っている防衛施設なら耐える
				$land->[$fx][$fy] = $HlandDefence;
				$landValue->[$fx][$fy] = $fLv;
			} else {
				# 荒地になる
				$land->[$fx][$fy] = $HlandWaste;
				$landValue->[$fx][$fy] = 1; # 着弾点
				$HlandMove[$id][$fx][$fy] = 1;
			}
		} #foreach
	} #while
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
		my $attack = ($huge) ? $HhugeMonsterFireName[$mKind] : $HmonsterFireName[$mKind];
		$attack = 'ミサイル攻撃' if($attack eq '');
		logNavyMatome($id, $name, $mId, $mPoint, $mName, $tPoint, $tLandName, $attack, $str, $pntStr, join('-', (keys %damageId)));
	}
	# 難民判定
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && (defined $mn)) {
		# 難民漂着
		my($achive) = boatAchive($mIsland, $boat); # 到達難民

		if ($achive > 0) {
			# 少しでも到着した場合、ログを吐く
			my $name = islandName($mIsland);
			logMsBoatPeople($mId, $name, $achive);
			$mIsland->{'ext'}[4] += int($achive); # 救出した難民の合計人口

			# 難民の数が一定数以上なら、平和賞の可能性あり
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
