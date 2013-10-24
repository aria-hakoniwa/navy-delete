# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
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
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {

	# �ǽ��������֤򹹿�
	$HislandLastTime += $HunitTime if($HrepeatTurn);

	if($HallyNumber && $HrepeatTurn) { # Ʊ���ξ����򼨤��ǡ����Υ��ꥢ
		for($i = 0; $i < $HallyNumber; $i++) {
			$Hally[$i]->{'ext'}[0] = 0;
			$Hally[$i]->{'ext'}[1] = 0;
			$Hally[$i]->{'ext'}[2] = 0;
			$Hally[$i]->{'ext'}[3] = 0;
			$Hally[$i]->{'ext'}[4] = 0;
		}
	}

	my $repeatTurn = $HrepeatTurn;
	while ($repeatTurn--) {
		my($i, $j, $s, $d, $island);

		# ���ַ��
		my(@order) = randomArray($HislandNumber);

		my($island);
		# ��ɸ�������
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			makeRandomIslandPointArray($island);
		}

		# �������ֹ�
		$HislandTurn++;
		# ����(��ȯ����Ʈ)���ֺǸ�Υ�����Ǥϥ�ԡ��Ȥ����
		$repeatTurn = 0 if($HislandTurn == $HarmisticeTurn || $HislandTurn == $HsurvivalTurn ||  $HislandTurn == $HislandChangeTurn);

		if($HarmisticeTurn || $HsurvivalTurn ||$Htournament) {
			# �ҳ����ꡩ
			if(!$repeatTurn && !$Htournament) {
				# �Ǹ�Υ�����Ϻҳ�����
				if ($HislandTurn < $HarmisticeTurn) {
					# ������֤�̵�ҳ�
					$HnoDisFlag = 1;
				} else {
					# �ҳ�����
					$HnoDisFlag = 0;
				}
			} else {
				# �Ǹ�Υ�����ʳ��Ϻҳ��ʤ�
				$HnoDisFlag = 1;
			}
		} elsif($HuseDeWar) {
			# ���賫�ϥ�
			my @newWarIsland;
			for($i=0;$i < $#HwarIsland;$i+=4){
				my($tn1) = $HidToNumber{$HwarIsland[$i+1]};
				my($tn2) = $HidToNumber{$HwarIsland[$i+2]};
				next if(($tn1 eq '') || ($tn2 eq ''));
				#my($name) = islandName($Hislands[$tn1]);
				#my($tName) = islandName($Hislands[$tn2]);
				#$name = "${HtagName_}${name}${H_tagName}";
				#$tName = "${HtagName_}${tName}${H_tagName}";
				my($isl) = $Hislands[$tn1];
				my($tIsl) = $Hislands[$tn2];
				my($name) = "${HtagName_}${\islandName($isl)}${H_tagName}";
				my($tName) = "${HtagName_}${\islandName($tIsl)}${H_tagName}";
				if($HwarIsland[$i+3]) {
					my($f, $fturn) = ($HwarIsland[$i+3] % 10, int($HwarIsland[$i+3] / 10) + $HdeclareTurn);
					if($fturn < $HislandTurn) {
						if($f == 1) {
							$HwarIsland[$i+3] = 0;
							logOut("${name}��${tName}���ǿǤ��Ƥ���������˴�����ޤ�����", $HwarIsland[$i+1], $HwarIsland[$i+2]);
						} elsif($f == 2) {
							$HwarIsland[$i+3] = 0;
							logOut("${tName}��${name}���ǿǤ��Ƥ���������˴�����ޤ�����", $HwarIsland[$i+2], $HwarIsland[$i+1]);
						}
					}
				}
				push(@newWarIsland, @HwarIsland[$i..$i+3]);
				next if($HwarIsland[$i] != $HislandTurn);
				if($HmatchPlay > 1) {
					foreach ($isl, $tIsl){
						# �����󥿥ꥻ�å�
						$_->{'subSink'} = $_->{'sink'};
						$_->{'subSinkself'} = $_->{'sinkself'};
						my @wext = @{$_->{'ext'}};
						shift(@ext);
						unshift(@ext, $HislandTurn);
						push(@ext, $_->{'monsterkill'});
						push(@ext, 0);
						$_->{'subExt'} = \@ext;
						# ��ξ��֤���¸
						island_save($_, $HsavedirName, 'save', 0);
					}
				}
				my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
				logOut("${wname}������ȯ����", $HwarIsland[$i+1], $HwarIsland[$i+2]);
				logHistory("${wname}������ȯ����");
			}
			@HwarIsland = @newWarIsland;
		}
		if($HsurvivalTurn && ($HislandTurn == $HsurvivalTurn) && (-e "${HefileDir}/setup.html")){
			unlink("${HefileDir}/setup.html");
		}

		# ����������ե�����
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];

			# ���������ѹ������å�
			if($HjoinCommentPenalty && !$island->{'predelete'}) {
				if(($HislandTurn - $island->{'birthday'} >= $HjoinCommentPenalty) && ($island->{'comment'} eq $HjoinComment)){
					push(@HpreDeleteID, $island->{'id'});
					$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
					my $name = islandName($island);
					logHistory("${HtagName_}${name}${H_tagName}�������Ȥ��ʤ�����<B>�����ͤ�������</B>��");
				}
			}
			# �ѿ��ν����
			undef $island->{'ships'};
			undef $island->{'shipk'};
			undef $island->{'cIncome'};
			undef $island->{'rinmoney'};
			undef $island->{'rinfood'};
			undef $island->{'slaughterer'};
			$island->{'oilincome'} = 0;
			$island->{'inMoney'} = 0;
			$island->{'inFood'} = 0;
			$island->{'payFood'} = 0;
			$island->{'upkeepMoney'} = 0;
			$island->{'upkeepMoneyPlus'} = 0;
			$island->{'upkeepMoneyProbe'} = 0;
			$island->{'upkeepAlly'} = 0;
			$island->{'upkeepFood'} = 0;
			$island->{'upkeepFoodPlus'} = 0;
			$island->{'shellMoney'} = 0;
			# �����󳫻����ο͸�����⡢���������
			$island->{'oldPop'} = $island->{'pop'};
			$island->{'oldMoney'} = $island->{'money'};
			$island->{'oldFood'} = $island->{'food'};
			# ��ͧ����Υե饰����
			my $amityNum = 0;
			foreach (@{$island->{'amity'}}) {
				my $amn = $HidToNumber{$_};
				if(defined $amn) {
					# ͧ��������ꤷ�Ƥ���Ƥ�����ID��'amityBy'�˳�Ǽ
					push(@{$Hislands[$amn]->{'amityBy'}}, $island->{'id'});
					$amityNum++;
				}
			}
			next if($island->{'predelete'} || $island->{'rest'});

			# ͧ����ݻ���
			$island->{'upkeepAmity'} = ($HarmisticeTurn) ?  0 : $amityNum * $HamityMoney;
			$island->{'money'} -= $island->{'upkeepAmity'};
			$island->{'money'} = 0 if($island->{'money'} < 0);

#-------------------------������Ƚ���-------------------------
                        $island->{'setreadyx'} = 31;
                        $island->{'setreadyy'} = 31;

			# ���ޥ�ɥ����å�(�����ư���ɸ������Խ����򤹤뤫)
			my($comArray, $c, $tflag, $ctflag);
			$comArray = $island->{'command'};
			$tflag = 0;
			$ctflag = int($island->{'itemAbility'}[6]);
			for($c = 0; $c < $HcommandMax; $c++) {
				my($ckind) = $comArray->[$c]->{'kind'};
				my($carg) = $comArray->[$c]->{'arg'};
				$carg--;
				if ($carg < 0) {
					$carg = 0;
				} elsif ($carg > 3) {
					$carg = 3;
				}
				$island->{'NavyMove_flag'}[$carg] = 1 if(($ckind == $HcomNavyMove) || ($ckind == $HcomNavySend) || ($ckind == $HcomNavyReturn));
				$tflag += $HcomTurn[$ckind];
				last if($tflag >= $ctflag);
			}

			# ���ݥե�����
			if($HuseWeather) {
				my(@tempWeather) = ();
				foreach (1..$#HweatherName) {
					@tempWeather = (@tempWeather, ($_)x$HweatherRatio[$_] );
				}
				my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$island->{'weather'}};
				# ����
				my $dkion = ($HweatherSpecial[$weather[0]] & 0xF) - 8;
				$dkion = ($dkion == -8) ? 0 : $dkion * $HweatherSpecialRatio[0] + random($HrKion * 2 + 1) - $HrKion;
				$kion += $dkion;
				$kion = ($kion > 41) ? 25 : ($kion < -12) ? 0 : $kion;
				$kion = ($kion > 40) ? 40 : ($kion < -10) ? -10 : $kion;
				# ����
				my $dkiatu = (($HweatherSpecial[$weather[0]] & 0xF0)>>(4*1)) - 8;
				$dkiatu = ($dkiatu == -8) ? 0 : $dkiatu * $HweatherSpecialRatio[1] + random($HrKiatu * 2 + 1) - $HrKiatu;
				$kiatu += $dkiatu;
				$kiatu = ($kiatu > 1105) ? 1000 : ($kiatu < 895) ? 1000 : $kiatu;
				$kiatu = ($kiatu > 1100) ? 1100 : ($kiatu < 900) ? 900 : $kiatu;
				# ����
				my $dsitudo = (($HweatherSpecial[$weather[0]] & 0xF00)>>(4*2)) - 8;
				$dsitudo = ($dsitudo == -8) ? 0 : $dsitudo * $HweatherSpecialRatio[2] + random($HrSitudo * 2 + 1) - $HrSitudo;
				$situdo += $dsitudo;
				$situdo = ($situdo > 103) ? 90 : ($situdo < -1) ? 60 : $situdo;
				$situdo = ($situdo > 100) ? 100 : ($situdo < 0) ? 0 : $situdo;
				# ��®
				$kaze += (abs($dkiatu) > $HrKiatu / 2) ? abs($dkiatu / 30) : -abs($dkiatu / 5);
				$kaze = ($kaze > 50) ? 50 : ($kaze < 0) ? 0 : int($kaze);
				# ���׻ؿ�
				$jiban += int(($situdo - 50) / 4) if($situdo > 60);
				$jiban -= int($kion / 2) if($kion > 20);
				$jiban = ($jiban > 100) ? 100 : ($jiban < 0) ? 0 : $jiban;
				# ���ϻؿ�
				$nami += ($kaze < 5) ? -int($kaze / 3) : int($kaze / 3);
				$nami = ($nami > 100) ? 100 : ($nami < 0) ? 0 : $nami;
				# �۾�ؿ�(���Ѥ���)
				$ijoh = 0;
				# ŷ������
				my(@newWeather);
				$newWeather[0] = $tempWeather[random($#tempWeather)];
				$newWeather[1] = (random(10) < 7) ? $weather[0] : $tempWeather[random($#tempWeather)];
				$newWeather[2] = (random(10) < 9) ? $weather[1] : $tempWeather[random($#tempWeather)];
				foreach (1..$HtopLogTurn) {
					$newWeather[($_ + 2)] = ($weather[($_ + 1)] == '') ? 0 : $weather[($_ + 1)];
				}
				@newWeather = ($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @newWeather);
				$island->{'weather'} = \@newWeather;
			}
		}

		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			estimate($order[$i]);
			next if($island->{'predelete'} || $island->{'rest'});

			# ��������
			income($island);
			# ������������
			supplyNavy($island);
		}

		# ��Խ���
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doPreEachHex($island);
		}

		# ���ޥ�ɽ���
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if(!($HforgivenGiveUp && $island->{'command'}[0]->{'kind'} == $HcomGiveup) && ($island->{'predelete'} || $island->{'rest'}));
			# �����1�ˤʤ�ޤǷ����֤�
			$HflagST = 0;
			$HflagCommand = 0;
			my $cflag = int($island->{'itemAbility'}[6]);
			$HflagDoNothing = ($island->{'command'}[0]->{'kind'} != $HcomDoNothing);
			my($safety) = $HcommandMax * 2;
			while ($HflagCommand < $cflag) {
				my($flagcom) = $HcomTurn[$island->{'command'}->[0]->{'kind'}];
				last if($HflagCommand + $flagcom > $cflag);
				if($island->{'comflag'}) {
					$HflagCommand += $flagcom;
					doCommand($island);
				} else {
					$HflagCommand += doCommand($island);
				}
				last if(!$safety--);
			}
			# ���ϥ�(�ޤȤ�ƥ�����)
			logMatome($island);
		}

		# ��Ĺ�����ñ�إå����ҳ�
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doEachHex($island);
		}

                # ñ�إå������� 2����
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doEachHex2($island);
		}

		my($remainCampNumber, $campDelete);
		if($HarmisticeTurn && $HallyNumber) {
			# �رľ���Ƚ��
			$remainCampNumber = $HallyNumber;
			if ($HcampDeleteRule) {
				my($threshold);
				if($HcampDeleteRule == 1) {
					my($anumber) = 0;
					for ($i = 0; $i < $HallyNumber; $i++) {
						$anumber++ if($Hally[$i]->{'number'});
					}
					$anumber = 1 if(!$anumber);
				 	$threshold = 50 / $anumber;
				} else {
				 	$threshold = $HcampDeleteRule;
				}
				for ($i = 0; $i < $HallyNumber; $i++) {
					if ($Hally[$i]->{'number'} && ($Hally[$i]->{'occupation'} < $threshold)) {
						push(@{$campDelete->{'id'}}, $Hally[$i]->{'id'});
						push(@{$campDelete->{'name'}}, $Hally[$i]->{'name'});
						$campDelete->{'count'}++;
						foreach (@{$Hally[$i]->{'memberId'}}){
							if($HautoKeeper != 1) {
								$Hislands[$HidToNumber{$_}]->{'dead'} = 1;
							} else {
								$Hislands[$HidToNumber{$_}]->{'delete'} = 1;
							}
						}
						if($HautoKeeper == 1) {
							logCampPreDelete($Hally[$i]->{'name'});
						} else {
							$remainCampNumber--;
							logCampDelete($Hally[$i]->{'name'});
						}
					}
				}
			}
		}

		# ������ؤ��������Ƥ��ɤ߹���
		readPunishData();

		# �����ν���
		# ���ýи��͸��ե饰����
		foreach (@HdisMonsBorder) {
			$HdisMonsBorderMax = $_ if($HdisMonsBorderMax <= $_);
		}
		$HdisMonsBorderMin = $HdisMonsBorderMax;
		foreach (@HdisMonsBorder) {
			next if(!$_);
			$HdisMonsBorderMin = $_ if($HdisMonsBorderMin >= $_);
		}
		# ������ýи��͸��ե饰����
		foreach (@HdisHugeBorder) {
			$HdisHugeBorderMax = $_ if($HdisHugeBorderMax <= $_);
		}
		$HdisHugeBorderMin = $HdisHugeBorderMax;
		foreach (@HdisHugeBorder) {
			next if(!$_);
			$HdisHugeBorderMin = $_ if($HdisHugeBorderMin >= $_);
		}
		# �����и��͸��ե饰����
		foreach (@HdisNavyBorder) {
			$HdisNavyBorderMax = $_ if($HdisNavyBorderMax <= $_);
		}
		$HdisNavyBorderMin = $HdisNavyBorderMax;
		foreach (@HdisNavyBorder) {
			next if(!$_);
			$HdisNavyBorderMin = $_ if($HdisNavyBorderMin >= $_);
		}
		# �����ν���
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doIslandProcess($island);
			undef $island->{'ships'};
			undef $island->{'shipk'};
		}

		# ������(estimate)����
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doIslandProcessEstimate($order[$i], $island);
			# �ȡ��ʥ��� ��������Ʈ�԰٤����ä���
			my $name = islandName($island);
			if(0 && $Htournament && ($HislandFightMode == 2) && ($island->{'fight_id'} > 0)) { # �ȡ��ʥ��� ������Ʈ��������å�
				if((int($HfightTurn / 2) == ($HislandChangeTurn - $HislandTurn)) &&
					($island->{'ext'}[6] - $island->{'subExt'}[6] < $do_fight) &&
					($island->{'ext'}[8] - $island->{'subExt'}[8] < min(1,$do_fight))) {
					my $fn = $HidToNumber{$island->{'fight_id'}};
					my $tIsland = $Hislands[$fn];
					next if($HnofleetNotAvail && $island->{'ships'}[4] && !$tIsland->{'ships'}[4]);
					logGiveup_no_do_fight($island->{'id'}, islandName($island));
					if($HautoKeeper != 1) {
						$island->{'dead'} = 1;
						logTDead($island->{'id'}, $name);
					} else {
						$island->{'delete'} = 1;
					}
				}
			}
			# ������ͭ��ǧ
			if($HcorelessDead && !$island->{'field'} && !$island->{'event'}[0] && !$island->{'core'} &&
				!($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) &&
				!($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn)) &&
				!($Htournament && ($HislandFightMode < 2)) &&
				!($HislandTurn - $island->{'birthday'} <= $HdevelopTurn)
				) {
				logHistory("${HtagName_}${name}${H_tagName}��$HlandName[$HlandCore][0]��${HtagDisaster_}����${H_tagDisaster}���ޤ�����");
				if($HcorelessDead == 1) {
					$island->{'dead'} = 1;
					logTDead($island->{'id'}, $name);
				} else {
					$island->{'delete'} = 1;
				}
			}
		}

		# ����Ƚ�ꡦ���٥��Ƚ��
		my $predelNumber = @HpreDeleteID; # �����ͤ����������ϻ��ǽ�������ƨ���
		my $remainNumber = $HislandNumber - $predelNumber;
		my $deadline = ($HarmisticeTurn || $HsurvivalTurn || $Htournament) ? 0 : $HautoKeeper;
		my $tournamentflg = 0;
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			if($island->{'event'}[0]) {
				# ���٥��Ƚ��
				my $winner;
				if($island->{'event'}[1] - $HnoticeTurn == $HislandTurn) {
					# ���٥�ȳ�����(ͱͽ����)
					my $type  = $HeventName[$island->{'event'}[6]];
					my $name = islandName($island);
					islandDeadNavy($island);# ��������
					$island->{'comment'} = "<B>$type���š�</B>";
					if(!$island->{'event'}[11]) {
						$island->{'comment'} .= "(<span class=attention>��</span>�ɸ��Ǥ���Τ�<B>������$island->{'event'}[1]����</B>�Ǥ�)";
					} else {
						$island->{'comment'} .= "(<span class=attention>��</span><B>������$island->{'event'}[1]����</B>����ɸ���ǽ�Ǥ�)";
					}
					logHistory("${HtagName_}${name}${H_tagName}��${HtagDisaster_}$type${H_tagDisaster}���š�(${HtagDisaster_}$island->{'event'}[1]������${H_tagDisaster}����)");
				} elsif($island->{'event'}[1] <= $HislandTurn) {
					# ���٥�ȳ�����
					$winner = islandEventNavy($island, $island->{'event'}[6]);
				}
				if($winner != 0) {
					my $type  = $HeventName[$island->{'event'}[6]];
					my $name = islandName($island);
					$island->{'comment'} = "<B>$type�Ͻ�λ���ޤ�����</B>($HislandTurn������)";
					if($winner > 0) {
						$island->{'comment'} .= "�����ԡ�<span class=islName>$Hislands[$HidToNumber{$winner}]->{'name'}$AfterName</span>";
						$winner = islandName($Hislands[$HidToNumber{$winner}]);
						logHistory("${HtagName_}${name}${H_tagName}�ǳ��Ť���${HtagDisaster_}$type${H_tagDisaster}��${HtagName_}${winner}${H_tagName}��<B>����</B>���ޤ�����");
					} else {
						logHistory("${HtagName_}${name}${H_tagName}�ǳ��Ť���${HtagDisaster_}$type${H_tagDisaster}��<B>���Ԥʤ��ǽ�λ</B>���ޤ�����");
						$island->{'comment'} .= "�����ԡ�<span class=islName>�ʤ�</span>";
					}
					undef $island->{'event'}; # �ե饰���ꥢ
				}
			} elsif($island->{'dead'} == 1) {
				# ����Ƚ��(�ե饰����)
				island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
				$island->{$HrankKind} = 0;
				$island->{'pop'} = 0;
				my($tmpid) = $island->{'id'};
				islandDeadNavy($island); # ��������
				# �ȡ��ʥ��Ȥ���Ʈ������
				$tournamentflg = fightNoFight($island, $remainNumber) if($Htournament && ($island->{'fight_id'} > 0));
				preDelIdCut($tmpid);
				$HidToNumber{$tmpid} = undef;
				deleteIslandData($island);
				$remainNumber--;
			} elsif( (!$island->{'field'} && !$island->{'predelete'} && ($island->{'pop'} <= $deadline)
						&& (!$island->{'pop'} || ($HislandTurn - $island->{'birthday'} > $HdevelopTurn)))
				|| $island->{'delete'}
				) {
				# ����Ƚ��
				my($tmpid) = $island->{'id'};
				islandDeadNavy($island);
				# �ȡ��ʥ��Ȥ���Ʈ������
				$tournamentflg = fightNoFight($island, $remainNumber) if($Htournament && ($island->{'fight_id'} > 0));
				# �����˲�
				my $dNo2 = $HidToNumber{$island->{'slaughterer2'}};
				if(defined $dNo2) {
					push(@{$Hislands[$dNo2]->{'defeat'}},(islandName($island),$HislandTurn));
				}
				my $count = 0;
				if(!$island->{'pop'}) {
					my $dNo = $HidToNumber{$island->{'slaughterer'}};
					if(defined $dNo) {
						push(@{$Hislands[$dNo]->{'defeat'}},(islandName($island),$HislandTurn));
					}
					if($HautoKeeper && !$HarmisticeTurn && !$HsurvivalTurn && !$Htournament){
						# ����͸���Į����
						my($land) = $island->{'land'};
						my($landValue) = $island->{'landValue'};
						foreach (0..$island->{'pnum'}) {
							last if($count >= $HcountLandTown);
							$x = $island->{'rpx'}[$i];
							$y = $island->{'rpy'}[$i];
							# ������ʿ�Ϥ����Ϥʤ顢Į
							if(($land->[$x][$y] == $HlandPlains) || ($land->[$x][$y] == $HlandWaste)) {
								$land->[$x][$y] = $HlandTown;
								$landValue->[$x][$y] = $HvalueLandTown;
								$island->{'pop'} += $HvalueLandTown;
								$count++;
							}
						}
					}
				}
				if(($HautoKeeper == 1) || $island->{'delete'}) {
					push(@HpreDeleteID, $tmpid);
					$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
					undef $island->{'item'};
					$remainNumber--;
					$predelNumber++;
					logTDead2PD($tmpid, islandName($island));
				} elsif($HautoKeeper && ($island->{'pop'} > 0)) {
#					$island->{'money'} = $HinitialMoney;
#					$island->{'food'} =  $HinitialFood;
					$island->{'birthday'} = $HislandTurn;
					$island->{'monsterlive'} = "0,0,0,0,0";
					undef $island->{'item'};
					#undef $island->{'allyId'};
					#undef $island->{'amity'};
					logAutoKeep($tmpid, islandName($island));
				} elsif($island->{'pop'} <= 0) {
					island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
					$island->{'dead'} = 1;
					$island->{$HrankKind} = 0;
					$remainNumber--;
					# ���ǥ�å�����
					logDead($tmpid, islandName($island));
					$HidToNumber{$tmpid} = undef;
					deleteIslandData($island);
				}
			} else {
				$island->{'ext'}[1] += int($island->{$HrankKind}/10);
			}
			undef $island->{'fkind'};
		}
			# �رľ���Ƚ��
		if($campDelete->{'count'}) {
			foreach (0..($campDelete->{'count'} - 1)) {
				islandDeadAlly('', $campDelete->{'id'}[$_], $campDelete->{'name'}[$_]);
			}
		}
		# ��ξ��ǽ���(���Х��Х�⡼��)
		if($HsurvivalTurn && ($HislandTurn > $HsurvivalTurn) && ($remainNumber > $HbfieldNumber + 1)){
			# $HrankKind��(�����$HrankKind�ι�ס�100)��(100�����)��2��꾯�ʤ�����������Ͼ���

			my $rNumber = $remainNumber;
			my($allscore, $i);
			my $rn = $rNumber - 1;
			foreach $i ($HbfieldNumber..$rn) {
				$allscore += $Hislands[$i]->{$HrankKind} if(!$Hislands[$i]->{'predelete'});
			}
			my $rNumber2 = $rNumber - 1;
			foreach $i ($HbfieldNumber..$rNumber2) {
				my($island) = $Hislands[$i];
				next if($island->{'dead'} || $island->{'predelete'});
				my $iocc = ($allscore > 0) ? sprintf("%.1f", $island->{$HrankKind} * 100 / $allscore) : 0;
				my $border = sprintf("%.1f", 50/$rNumber);
				if($iocc && ($iocc < $border)){
					if($remainNumber > $HbfieldNumber + 1){
						$remainNumber--;
						islandDeadNavy($island);
						# ���ǥ�å�����
						my($tmpid) = $island->{'id'};
						if($HautoKeeper != 1){
							island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
							$island->{'dead'} = 1;
							$island->{$HrankKind} = 0;
							logTDead($tmpid, islandName($island));
							$HidToNumber{$tmpid} = undef;
							deleteIslandData($island);
						} elsif(!$island->{'predelete'}) {
							push(@HpreDeleteID, $tmpid);
							$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
							$predelNumber++;
							logTDead2PD($tmpid, islandName($island));
						}
					}
			   }
			}
		}

		if($Htournament) {
			# �ȡ��ʥ���
			foreach $i ($HbfieldNumber..$islandNumber) {
				# �󽷶�׻�
				$island = $Hislands[$i];
				next if($island->{'predelete'});
				foreach (keys %Hreward) {
					$island->{'subExt'}[12] += int($island->{$_} * $Hreward{$_});
				}
			}

			if($HislandFightMode == 0) {
				# ͽ��
				if($HislandTurn == $HislandChangeTurn) {
					# ��ȯ������˰ܹ�
					$tournamentflg = 1;
					$HislandFightMode = 1;
					$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
				}
			} elsif($HislandFightMode == 1) {
				# ��ȯ
				if($HislandTurn == $HislandChangeTurn) {
					# ��Ʈ������˰ܹ�
					$tournamentflg = 2;# ��������������Ͽ͸������ȸ��
					$HislandFightMode = 2;
					$HislandFightCount++;
					if($remainNumber > 2) {
						# �辡��ʳ��ϡ����֤������
						$HislandChangeTurn = $HislandTurn + $HfightTurn;
					} else {
						# �辡��
						$HislandChangeTurn = $HislandTurn + $HfinalTurn;
					}
					my $rno = $remainNumber - 1;
					foreach $i ($HbfieldNumber..$rno){
						$island = $Hislands[$i];
						# �����󥿥ꥻ�å�
						$island->{'subSink'} = $island->{'sink'};
						$island->{'subSinkself'} = $island->{'sinkself'};
						my @ext = @{$island->{'ext'}};
						shift(@ext);
						unshift(@ext, $HislandTurn);
						push(@ext, $island->{'monsterkill'});
						push(@ext, 0);
						#undef $island->{'subExt'};
						$island->{'subExt'} = \@ext;
						# ��ξ��֤���¸
						island_save($island, $HsavedirName, 'save');
					}
				}
			} elsif($HislandFightMode == 2) {
				# ��Ʈ
				if($HislandTurn == $HislandChangeTurn){
					# ���Է��塡��ȯ������˰ܹ�
					$tournamentflg = 3;
					if(($remainNumber < $HbfieldNumber + 2) ||
						( ($remainNumber <= $HbfieldNumber + 2) &&
						($Hislands[$HbfieldNumber]->{'fight_id'} > -1) &&
						($Hislands[$HbfieldNumber+1]->{'fight_id'} > -1) )
					) {
						# ��λ
						$HislandFightMode = 9;
						$repeatTurn = 0;
						$HplayNow = 0;
						$Hislands[$HbfieldNumber]->{'ext'}[0] |= (2 ** $#HwinnerMark);
					} else {
						$HislandFightMode = 1;
					}
					$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
					my $HwinIsland = 0;       # ����������ο�
					my $consolationScore = 0; # �Լ������о���͸�
					my $consolationID = 0;    # �Լ������о���ɣ�
					my $rno = $remainNumber - 1;
					my $fightIslandNumber = 0;
					my $winIslandNumber = 0;
					foreach $i ($HbfieldNumber..$rno){
						$island = $Hislands[$i];
						if($island->{'fight_id'} < 0) {
							$winIslandNumber++;
						} elsif($island->{'fight_id'} > 0) {
							$fightIslandNumber++;
						}
					}
					$winIslandNumber += int(($fightIslandNumber + 1)/2);
					foreach $i ($HbfieldNumber..$rno){
						$island = $Hislands[$i];
						my $tn = $HidToNumber{$island->{'fight_id'}};
						my $tIsland = $Hislands[$tn];
						# ��Ʈ��ξ���
						my $reward = $island->{'subExt'}[12];
						if(($tn ne '' && $island->{$HrankKind} >= $tIsland->{$HrankKind}) || ($island->{'fight_id'} == -1) || ($island->{'fight_id'} == -2)) {
							# ����
							my $name = islandName($island);
							my $tName = islandName($tIsland);
							my $tScore = 0;
							$HwinIsland++;
							if($island->{'fight_id'} > 0){
								$island->{'money'} += $reward;
								$island->{'prizemoney'} += $reward;
								logWin($island->{'id'}, $name, "����", $reward, $winIslandNumber);
								$tScore = $tIsland->{$HrankKind};
								$tIsland->{'fight_id'} = 0;
								if($consolationScore <= $tScore){
									$consolationScore = $tScore;
									$consolationID = $tIsland->{'id'};
								}
								$tIsland->{'lose'} = 1;
								logOut("${HtagName_}${tName}${H_tagName}��<B>����</B>��",$tIsland->{'id'});
							} elsif($island->{'fight_id'} == -2) {
								# ������ɾ���
								#$island->{'money'} += $reward;
								#$island->{'prizemoney'} += $reward;
								logWin($island->{'id'}, $name, "������", '', $winIslandNumber);
							} else {
								# ���ﾡ
								logWin($island->{'id'}, $name, "���ﾡ", '', $winIslandNumber);
							}
							my(@text);
							my(@iext) = @{$island->{'subExt'}};
							foreach (0..$#iext) {
								$iext[$_] = $island->{'ext'}[$_] - $island->{'subExt'}[$_];
								$iext[$_] = -$iext[$_] if($iext[$_] < 0);
								$text[$_] = $tIsland->{'ext'}[$_] - $tIsland->{'subExt'}[$_];
								$text[$_] = -$text[$_] if($text[$_] < 0);
							}
							if($island->{'fight_id'} > 0) {
								push(@HfightLogPool, "$HislandFightCount,$island->{'id'},$name,$island->{$HrankKind}," . join('-', @iext) . ",$island->{'fight_id'},$tName,$tScore," . join('-', @text) . ",$reward");
							} else {
								push(@HfightLogPool, "$HislandFightCount,$island->{'id'},$name,$island->{$HrankKind}," . join('-', @iext) . ",$island->{'fight_id'},,,,$reward");
							}
						} elsif(($tn eq '') && ($island->{'fight_id'} > 0)){
							$HwinIsland++;
							my $name = islandName($island);
							$island->{'money'} += $reward;
							$island->{'prizemoney'} += $reward;
							logWin($island->{'id'}, $name, "������", $reward, $winIslandNumber);
							my(@iext) = @{$island->{'subExt'}};
							foreach (0..$#iext) {
								$iext[$_] = $island->{'ext'}[$_] - $island->{'subExt'}[$_];
								$iext[$_] = -$iext[$_] if($iext[$_] < 0);
							}
							push(@HfightLogPool, "$HislandFightCount,$island->{'id'},$name,$island->{$HrankKind}," . join('-', @iext) . ",-2,,,,$reward");
						}
						$island->{'fight_id'} = 0;
						$island->{'subExt'}[12] = 0;
					}
					$consolationID = 0 if($HislandFightMode == 9);
					# ���ष����ν���
					foreach $i (0..$islandNumber){
						$island = $Hislands[$i];
						islandDeadNavy($island);
						my $name = islandName($island);
						if($island->{'lose'}){
							if(($consolationID == $island->{'id'}) && (($HwinIsland % 2) != 0) && ($HconsolationMatch)){
								# �Լ������о���Ǽ������ξ����Լ�����⡼��
								my(@iext) = @{$island->{'subExt'}};
								foreach (0..$#iext) {
									$iext[$_] = $island->{'ext'}[$_] - $island->{'subExt'}[$_];
									$iext[$_] = -$iext[$_] if($iext[$_] < 0);
								}
								my $reward = int($island->{'subExt'}[12] / 2);
								$island->{'money'} += $reward;
								$island->{'prizemoney'} += $reward;
								push(@HfightLogPool, "$HislandFightCount,$island->{'id'},$name,$island->{$HrankKind}," . join('-', @iext) . ",-9,,,,");
								logOut("${HtagName_}${name}${H_tagName}��<B>�Լ����衪</B>��$reward$HunitMoney</B>�λٱ�⤬��ʧ���ޤ�����",$island->{'id'});
							} else {
								island_save($island, $HfightdirName, 'lose', 0);
								if(!$island->{'predelete'}) {
									logHistory("${HtagName_}${name}${H_tagName}��<B>����</B>��");
									$remainNumber--;
									my($tmpid) = $island->{'id'};
									if($HautoKeeper != 1){
										$island->{'dead'} = 1;
										$island->{$HrankKind} = 0;
										#OceanMente($island->{'id'});
										logTDead($tmpid, $name);
										$HidToNumber{$tmpid} = undef;
										deleteIslandData($island);
									} else {
										push(@HpreDeleteID, $tmpid);
										$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
										$predelNumber++;
										logTDead2PD($tmpid, $name);
									}
								}
							}
						}
					}
				}
			}
		}

		# ��̤򹹿�
		if($HrankKind eq 'point') {
			# �ݥ���Ƚ���
			foreach $i (0..$islandNumber) {
				calcPoint($i);
			}
		}
		islandSort($HrankKind, 1);
		# ���������оݥ�������ä��顢���ν���
		if($HturnPrizeUnit && !($HislandTurn % $HturnPrizeUnit) && $remainNumber) {
			foreach (0..($Hprize[0]->{'kind'} - 1)) {
				my($island) = $Hislands[($HbfieldNumber + $_)];
				if($Hprize[0]->{'money'}) {
					$island->{'prizemoney'} += $Hprize[0]->{'money'};
					$island->{'money'} += $Hprize[0]->{'money'};
				}
				logPrize($island->{'id'}, islandName($island), "$HislandTurn${Hprize[0]->{'name'}}", $Hprize[0]->{'money'});
				$island->{'prize'} .= "${HislandTurn},";
			}
 			if($HitemGivePerTurn && $HuseItem) { #���ꥹ������å����
				my $i = 0;
				@Hitem = @Hitem[randomArray($#Hitem + 1)];
				foreach (@Hitem) {
					last if(($_ eq '') || ($HbfieldNumber + $i >= $remainNumber));
					my $num;
					my $flag = 0;
					while($HbfieldNumber + $i < $remainNumber) {
						$num = ($HitemGivePerTurn == 1) ? $HbfieldNumber + $i : $remainNumber - ($i + 1);
						if(($Hislands[$num]->{'keyItemNumber'} == @{$Hitems[0]} - 1) ||
							(($HnavyName[0] ne '') && !($Hislands[$num]->{'ships'}[4] + $Hislands[$num]->{'navyPort'}))) {
							$i++;
						} else {
							$flag = 1;
							last;
						}
					}
					if($flag) {
						push(@{$Hislands[$num]->{'item'}}, $_);
						my @str = ('</span><span>������', '</span><span>���Ի׵�', '</span><span>������', '</span><span>���۱�');
						my @where = ('����', '����', '����', '���Ϥ�');
						$Hislands[$num]->{'itemNumber'}++;
						logItemGetLucky($Hislands[$num]->{'id'}, islandName($Hislands[$num]), $str[random(4)], $HitemName[$_], $where[random(4)]);
					}
					$i++;
				}
			}
		}

		if($Htournament){
			# �ȡ��ʥ���
			if($tournamentflg == 1){
				# ͽ����������פ�����
				while($remainNumber - $HbfieldNumber > $Htournament){
					$remainNumber--;
					$island = $Hislands[$remainNumber];
					my $name = islandName($island);
					unshift(@HfightLogPool, "0,$island->{'id'},$name,$island->{$HrankKind}");
					islandDeadNavy($island);
					my($tmpid) = $island->{'id'};
					if($HautoKeeper != 1){
						island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
						$island->{'dead'} = 1;
						$island->{$HrankKind} = 0;
						logTDead($tmpid, islandName($island));
						$HidToNumber{$tmpid} = undef;
						deleteIslandData($island);
					} elsif(!$island->{'predelete'}) {
						push(@HpreDeleteID, $tmpid);
						$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
						$predelNumber++;
						logTDead2PD($tmpid, islandName($island));
					}
					logLoseOut($island->{'id'}, islandName($island));
				}
			}
			if(($tournamentflg == 1) || ($tournamentflg == 3)){
				# �������������
				my($l,$r);
				$r = $remainNumber - 1;
				for($l = $HbfieldNumber; $l <= $r; $l++, $r--){
					if($Hislands[$r]->{'id'} == $Hislands[$l]->{'id'}){
						# ���ﾡ
						$Hislands[$r]->{'fight_id'} = -1;
						$Hislands[$r]->{'rest'} += $HnofightTurn + $HislandFightCount * $HnofightUp;
					} else {
						$Hislands[$l]->{'fight_id'} = $Hislands[$r]->{'id'};
						$Hislands[$r]->{'fight_id'} = $Hislands[$l]->{'id'};
					}
				}
			}
		}

		# �ǲ�����Ȥ��Υ�������ä��餽�ν���(���Х��Х�⡼��)
		if( $HsurvivalTurn && $HturnDead && !(($HislandTurn - $HsurvivalTurn) % $HturnDead) && ($HislandTurn > $HsurvivalTurn) ) {
			if($remainNumber > 1 + $HbfieldNumber){
				my $i = 1;
				$remainNumber--;
				$island = $Hislands[$remainNumber];
				islandDeadNavy($island);
				my($tmpid) = $island->{'id'};
				if($HautoKeeper != 1){
					island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
					$island->{'dead'} = 1;
					$island->{$HrankKind} = 0;
					logTDead($tmpid, islandName($island));
					$HidToNumber{$tmpid} = undef;
					deleteIslandData($island);
				} elsif(!$island->{'predelete'}) {
					push(@HpreDeleteID, $tmpid);
					$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
					$predelNumber++;
					logTDead2PD($tmpid, islandName($island));
				}
			}
		}

		# ������å�
		if($remainNumber + $predelNumber < $HislandNumber) {
			islandSort($HrankKind, 1);
			$HislandNumber = $remainNumber + $predelNumber;
			foreach $i ($HislandNumber..$islandNumber) {
				$HidToNumber{$Hislands[$i]->{'id'}} = undef;
				$Hislands[$i] = undef;
			}
			splice(@Hislands, $HislandNumber);
			$islandNumber = $HislandNumber - 1;
		}

		if($HallyNumber) { # Ʊ����Ϣ����
			# �رĥ��å�(���ǥ롼��)
			$HallyNumber = $remainCampNumber if($HarmisticeTurn && ($HautoKeeper != 1));
			for($i = 0; $i < $HallyNumber; $i++) {
				$Hally[$i]->{'score'} = 0;
				# �ݻ���(���ʤ��ʤä��礬���äƤ⤤������Ƭ���ǽ���)
				my($keepCost);
				$keepCost = int($HcostKeepAlly / $Hally[$i]->{'number'}) if($Hally[$i]->{'number'});
				$Hally[$i]->{'number'} = 0;
				my $allyMember = $Hally[$i]->{'memberId'};
				foreach (@$allyMember) {
					my $no = $HidToNumber{$_};
					if(defined $no) {
						$Hally[$i]->{'score'} += $Hislands[$no]->{$HrankKind} if(!$Hislands[$no]->{'predelete'});
						$Hally[$i]->{'number'}++;
						# �ݻ���ħ��
						if(!$HarmisticeTurn) {
							$Hislands[$no]->{'upkeepAlly'} += $keepCost;
							$Hislands[$no]->{'money'} -= $keepCost;
							$Hislands[$no]->{'money'} = 0 if($Hislands[$no]->{'money'} < 0);
						}
						# �׸���(�͸��ʤ�1���ͤˤĤ�1�ݥ����)
						$Hislands[$no]->{'ext'}[1] += int($island->{$HrankKind}/10);
					}
				}
				$Hally[$i]->{'Takayan'} = makeRandomString();
			}
			allyOccupy();
			allySort();
		}

		if($HbalanceLog) { # ���٥�(��̩)
			foreach $i ($HbfieldNumber..$islandNumber) {
				$island = $Hislands[$i];
				next if($island->{'predelete'});
				my $id = $island->{'id'};
				if($HcorelessDead && !$island->{'field'} && !$island->{'core'}) {
					my $dturn = $HdevelopTurn - ($HislandTurn - $island->{'birthday'}) + 1;
					my($alertstr);
					if($dturn <= 1) {
						$alertstr = '���Υ������';
					} else {
						$alertstr = $dturn . '����������';
					}
					logSecret("��--- <span class='attention'>�ٹ�</span> ����������ޤ���${HtagDisaster_}$alertstr${H_tagDisaster}���ߤ��ʤ����${HtagDisaster_}����${H_tagDisaster}���ޤ���",$id) if($dturn <= 10);
				}
				my($money) = $island->{'money'} - $island->{'oldMoney'};
				if($island->{'money'} && ($money < 0)) {
					my $turn = $island->{'money'} / (- $money);
					my $str;
					if($turn <= 1) {
						$str = "���Υ�����ˤ�";
					} else {
						$turn = int($turn);
						$str = "${turn}��������";
					}
					logSecret("��--- <span class='attention'>�ٹ�</span> $str��ȯ��⤬�ʤ��ʤ�ȿ�¬����ޤ���",$id) if($turn <= 50);
				}
				$money = ($money >= 0) ? "${HtagMoney_}$money" : "<span class='attention'>$money";
				my($food) = $island->{'food'} - $island->{'oldFood'};
				if($island->{'food'} && ($food < 0)) {
					my $turn = $island->{'food'} / (- $food);
					my $str;
					if($turn <= 1) {
						$str = "���Υ�����ˤ�";
					} else {
						$turn = int($turn);
						$str = "${turn}��������";
					}
					logSecret("��--- <span class='attention'>�ٹ�</span> $str���߿������ʤ��ʤ�ȿ�¬����ޤ���",$id) if($turn <= 50);
				}
				$food = ($food >= 0) ? "${HtagFood_}$food" : "<span class='attention'>$food";
				$food .= ($island->{'randomfood'}) ? "$HunitFood${H_tagFood} ��������ϡ�${HtagFood_}$island->{'randomfood'}" : '';
				my $uMoney = - $island->{'upkeepMoney'};
				$uMoney .= ($island->{'upkeepMoneyPlus'}) ? "$HunitMoney${H_tagMoney} ������${HtagMoney_}$island->{'upkeepMoneyPlus'}" : '';
				$uMoney .= ($island->{'upkeepMoneyProbe'}) ? "$HunitMoney${H_tagMoney} Ĵ����${HtagMoney_}-$island->{'upkeepMoneyProbe'}" : '';
				my $uFood = - $island->{'upkeepFood'};
				$uFood .= ($island->{'upkeepFoodPlus'}) ? "$HunitFood${H_tagFood} ���ϡ�${HtagFood_}$island->{'upkeepFoodPlus'}" : '';
				my $sMoney = - $island->{'shellMoney'};
				my $inMoney = $island->{'inMoney'};
				$inMoney .= ($island->{'prizemoney'}) ? "$HunitMoney${H_tagMoney} �����޶⡧${HtagMoney_}" . $island->{'prizemoney'} : '';
				$inMoney .= ($island->{'randommoney'}) ? "$HunitMoney${H_tagMoney} �����������${HtagMoney_}" . $island->{'randommoney'} : '';
				$inMoney .= ($island->{'upkeepAlly'}) ? "$HunitMoney${H_tagMoney} Ʊ���ݻ���${HtagMoney_}" . - $island->{'upkeepAlly'} : '';
				$inMoney .= ($island->{'upkeepAmity'}) ? "$HunitMoney${H_tagMoney} ͧ����ݻ���${HtagMoney_}" . - $island->{'upkeepAmity'} : '';
				my $pFood = - $island->{'payFood'};
				my $name = islandName($island);

				$logS[0] = "��--- ������ ��⡧$money$HunitMoney${H_tagMoney} ������$food$HunitFood${H_tagFood}";
				$logS[1] = "��--- ���� �ݻ���${HtagMoney_}$uMoney$HunitMoney${H_tagMoney} �ݻ�������${HtagFood_}$uFood$HunitFood${H_tagFood} ������${HtagMoney_}$sMoney$HunitMoney${H_tagMoney}";
				$logS[2] = "��--- ���ܼ��� ��⡧${HtagMoney_}$inMoney$HunitMoney${H_tagMoney} ���������̡�${HtagFood_}$island->{'inFood'}$HunitFood${H_tagFood} �����̡�${HtagFood_}$pFood$HunitFood${H_tagFood}";
				$logS[3] = "${HtagName_}${name}${H_tagName}<B>�Լ�������</B>";
				foreach (0..3) {
					1 while $logS[$_] =~ s/(.*\d)(\d\d\d)/$1,$2/;
					logSecret("$logS[$_]",$id);
				}
			}
		}

		# �������н���
		foreach $i (0..$islandNumber) {
			estimateNavy($i);
			$Hislands[$i]->{'rest'}-- if($Hislands[$i]->{'rest'} > 0);
			my $preflag = $Hislands[$i]->{'predelete'};
			$Hislands[$i]->{'predelete'}-- if(($Hislands[$i]->{'predelete'} > 0) && ($Hislands[$i]->{'predelete'} != 99999999));
			if($preflag && !$Hislands[$i]->{'predelete'}) {
				my($island) = $Hislands[$i];
				if(!$island->{'pop'}) {
					my($land) = $island->{'land'};
					my($landValue) = $island->{'landValue'};
					makeRandomIslandPointArray($island);
					foreach (0..$island->{'pnum'}) {
						last if($count >= $HcountLandTown);
						$x = $island->{'rpx'}[$_];
						$y = $island->{'rpy'}[$_];
						# ������ʿ�Ϥ����Ϥʤ顢Į
						if(($land->[$x][$y] == $HlandPlains) || ($land->[$x][$y] == $HlandWaste)) {
							$land->[$x][$y] = $HlandTown;
							$landValue->[$x][$y] = $HvalueLandTown;
							$island->{'pop'} += $HvalueLandTown;
							$count++;
						}
					}
				}
				if($HcorelessDead) {
					randomBuildCore($island, 1, 0, 0, 0) if(!$island->{'core'});
				}
			}
			if($Hislands[$i]->{'itemNumber'} && ($HnavyName[0] ne '') && !($Hislands[$i]->{'ships'}[4] + $Hislands[$i]->{'navyPort'})) {
				foreach(shift @{$Hislands[$i]->{'item'}}) {
					$HitemGetId[$_]{$Hislands[$i]->{'id'}} = undef;
				}
				$Hislands[$i]->{'item'} = undef;
				$Hislands[$i]->{'itemNumber'} = 0;
				$Hislands[$i]->{'gain'} = 0;# �Ĥ��Ǥ˷и��ͤ�ꥻ�åȤ����ꤷ��(^^;
				logItemLost($Hislands[$i]->{'id'}, islandName($Hislands[$i]), "��ͭ���Ƥ������٤Ƥ�$HitemName[0]", "�������ǤȤȤ��");
			}
		}
		# ����Ƚ��(���Х��Х�⡼�ɡ��ȡ��ʥ��ȥ⡼��)
		if(
			( $HsurvivalTurn && ($remainNumber == $HbfieldNumber + 1) && ($HislandTurn > $HsurvivalTurn) ) ||
			( $Htournament && ($remainNumber == $HbfieldNumber + 1) && ($HislandTurn > $HyosenTurn) )
		) {
			my $name = islandName($Hislands[$HbfieldNumber]);
			logHistory("${HtagName_}${name}${H_tagName}��<B>����</B>���ޤ�����");
			$Hislands[$HbfieldNumber]->{'ext'}[0] |= (2 ** $#HwinnerMark);
			$repeatTurn = 0;
			$HplayNow = 0;
		}

		# ��λ����Ƚ��
		my $n = gameOver();
		if ($n != -1) {
			my($v) = 2 ** $#HwinnerMark;
			if($HarmisticeTurn) {
				logHistory("${HtagName_}${Hally[$n]->{'name'}}${H_tagName}��<B>����</B>���ޤ�����");
				$Hally[$n]->{'ext'}[5] |= $v;
				my $allyMember = $Hally[$n]->{'memberId'};
				foreach (@$allyMember) {
					my $no = $HidToNumber{$_};
					if(defined $no) {
						$Hislands[$no]->{'ext'}[0] |= $v;
					}
				}
			} else {
				my $name = islandName($Hislands[$HbfieldNumber]);
				logHistory("${HtagName_}${name}${H_tagName}��<B>�ȥå�</B>�ǽ�λ���ޤ�����");
				$Hislands[$HbfieldNumber]->{'ext'}[0] |= $v;
			}
			$repeatTurn = 0;
			$HplayNow = 0;
		}

		# ���嵭Ͽ����
		if($HuseRekidai) {
			require './hako-reki.cgi';
			mainReki();
		}
		# �ݥ���Ƚ���
#		if($HrankKind eq 'point') {
#			foreach $i (0..$islandNumber) {
#				calcPoint($i);
#			}
#			# ��̤򹹿�
#			islandSort($HrankKind, 1);
#		}
		# �ȡ��ʥ��ȥ�
		fightlog() if($Htournament && ($tournamentflg == 3 || $tournamentflg == 1));

		# �Хå����åץ�����Ǥ���С�������rename
		if($HbackupTurn && !($HislandTurn % $HbackupTurn)) {
			my($i);
			my($tmp) = $HbackupTimes - 1;
			myrmtree("${HdirName}.bak$tmp");
			for($i = $tmp; $i > 0; $i--) {
				my($j) = $i - 1;
				rename("${HdirName}.bak$j", "${HdirName}.bak$i");
			}
			rename("${HdirName}", "${HdirName}.bak0");
			mkdir("${HdirName}", $HdirMode);

			# ���ե���������᤹
			foreach $i (0..$HlogMax) {
				copy("${HdirName}.bak0/$i$HlogData", "${HdirName}/$i$HlogData") if (-e "${HdirName}.bak0/$i$HlogData");
			}
			copy("${HdirName}.bak0/hakojima.his", "${HdirName}/hakojima.his") if (-e "${HdirName}.bak0/hakojima.his");
		}

		# �ե�����˽񤭽Ф�
		writeIslandsFile(-1);

		# ���ե��������ˤ��餹
		for($i = ($HlogMax - 1); $i >= 0; $i--) {
			$j = $i + 1;
			my($s) = "${HdirName}/$i$HlogData";
			my($d) = "${HdirName}/$j$HlogData";
			unlink($d);
			rename($s, $d);
		}

		# ��ٷ׻�(�ɲ� ����20020307 by �饹�ƥ���)
		if($Hperformance) {
			my($uti, $sti, $cuti, $csti) = times();
			$uti += $cuti;
			$sti += $csti;
			my($cpu) = $uti + $sti;

			# ���ե�����񤭽Ф�(�ƥ��ȷ�¬�ѡ����ʤϥ����Ȥˤ��Ƥ����Ƥ�������)
			#open(POUT,">>cpu-t.log");
			#print POUT "CPU($cpu) : user($uti) system($sti)\n";
			#close(POUT);

			logLate("<SMALL>��ٷ�¬ CPU($cpu) : user($uti) system($sti)</SMALL>",0);
		}

		# ���񤭽Ф�
		logFlush();

		# �ޤ�������ʹԤ��롩
		if ($repeatTurn) {
			# ��λ������ʤ�롼�פ�ȴ����
			last if ($HgameLimitTurn && ($HislandTurn >= $HgameLimitTurn));

			# ɬ�פ��ѿ�����������
			undef %HidToNumber;
			undef %HidToName;
			undef %HidToAllyNumber;
			undef @HmonsterMove;
			undef @HnavyMove;
			undef @HlandMove;
			undef %HnavyAttackTarget;

			my($island, $id, $ally);
			foreach $i (0..$islandNumber) {
				$island = $Hislands[$i];
				$island->{'dead'} = 0;
				$island->{'delete'} = 0;
				$id = $island->{'id'};
				$HidToNumber{$id} = $i;
				$HidToName{$id} = $island->{'name'};
			}
			for ($i = 0; $i < $HallyNumber; $i++) {
				$ally = $Hally[$i];
				$id = $ally->{'id'};
				$HidToAllyNumber{$id} = $i;
			}
		}
	}

	if($HhtmlLogMake && $HrepeatTurn && (-e "${HhtmlDir}/hakolog.html")) {
		unlink("${HhtmlDir}/hakolog.html");
	}

	tempInitialize(0);
	# �ȥåפ�
	topPageMain();
}

# ��λ���ɤ���
sub gameOver {
	# �����ڤ�
	if($HgameLimitTurn) {
		if ($HislandTurn >= $HgameLimitTurn) {
			# �ȥåפοرĤ򤫤���
			return 0;
		}
	}
	# �������
	if($HarmisticeTurn) {
		my($i);
		for ($i = 0; $i < $HallyNumber; $i++) {
			if ($Hally[$i]->{'occupation'} >= $HfinishOccupation) {
				return $i;
			}
		}
	}
	return -1;
}

# �ե������ݤ��ȥ��ԡ�
#sub copy {
#	my($src, $dest) = @_;
#
#	open(FS, "<$src") || die $!;
#	open(FD, ">$dest") || die $!;
#	binmode(FS); # Windows������Ǥ�ɬ��
#	binmode(FD); # Windows������Ǥ�ɬ��
#
#	my $buf;
#	while (read(FS, $buf, 1024 * 8) > 0) {
#		print FD $buf;
#	}
#
#	close(FD);
#	close(FS);
#}
sub copy {
	my($src, $dest) = @_;

	open(FS, "<$src") || die $!;
	my @buf = <FS>;
	close(FS);
	open(FD, ">$dest") || die $!;
	print FD @buf;
	close(FD);
}

# �ǥ��쥯�ȥ�ä�
sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	} 
	closedir(DIN);
	rmdir($dn);
}

# ������ؤ��������Ƥ��ɤ߹���
sub readPunishData {
	if (open(Fpunish, "<${HdirName}/punish.cgi")) {
		local(@_);
		my($island);
		while (<Fpunish>) {
			chomp;
			@_ = split(',');
			my($obj);
			$obj->{id} = shift;
			$obj->{punish} = shift;
			$obj->{x} = shift;
			$obj->{y} = shift;

			$HpunishInfo{$obj->{id}} = $obj;
		}
		close(Fpunish);
	}

	# ���ۥǡ�����������
	unlink("${HdirName}/punish.cgi");
}


# �����ͤ���������ǽ���
sub preDelIdCut {
	my($id) = @_;
	my @newID = ();
	foreach (@HpreDeleteID) {
		if(!(defined $HidToNumber{$_})) {
		} elsif($_ != $id) {
			push(@newID, $_);
		}
	}
	@HpreDeleteID = @newID;
}

# ����������ե�����
sub income {
	my($island) = @_;
	my($pop, $farm, $factory, $mountain) = 
	(	  
		$island->{'pop'},
		$island->{'farm'} * 10,
		$island->{'factory'},
		$island->{'mountain'}
	);

	my $fflag = $island->{'itemAbility'}[9];
	$fflag /= 2 if($HuseWeather && $island->{'weather'}[0] < 0);
	my $mflag = $island->{'itemAbility'}[10];
	# ����
	if($pop > $farm) {
		# ���Ȥ�������꤬;����
		$island->{'inFood'} = int($farm * $HincomeRate * $fflag); # ����ե��Ư
		$island->{'inMoney'} =
		min(
			int(($pop - $farm) * $HincomeRate * $mflag / 10),
			int(($factory + $mountain) * $HincomeRate * $mflag)
		);
	} else {
		# ���Ȥ����Ǽ���դξ��
		$island->{'inFood'} = int($pop * $HincomeRate * $fflag); # �������ɻŻ�
	}
	$island->{'down'} = 1 if($pop - ($farm + $factory * 10 + $mountain * 10) >= $Hno_work);

	# ��������
	my $eflag = $island->{'itemAbility'}[15];
	$island->{'payFood'} = int($pop * $HeatenFood * $eflag);

	$island->{'money'} += $island->{'inMoney'};
	$island->{'food'} += ($island->{'inFood'} - $island->{'payFood'});
	$island->{'food'} = 0 if($island->{'field'} && ($island->{'food'} < 0));
	if($HallyNumber) {
		my $gnp = int($island->{'inMoney'} + ($island->{'inFood'} - $island->{'payFood'})/10);
		foreach (@{$island->{'allyId'}}) {
			${Hally[$HidToAllyNumber{$_}]->{'ext'}[2]} += $gnp;
		}
	}
}

# ����ޤȤ��
sub logMatome {
	my($island) = @_;

	my($sno, $i, $sArray, $spnt, $x, $y, $point);
	my %mkind = (
		'prepare'  => "$HcomName[$HcomPrepare]",
		'selltree' => "$HcomName[$HcomSellTree]",
		'reclaim'  => "$HcomName[$HcomReclaim]",
		'destroy'  => "$HcomName[$HcomDestroy]",
	);
	foreach (keys %mkind) {
		$sno = @{$island->{$_}};
		$point = "";
		if($sno > 0) {
			if($HoutPoint) {
				$sArray = $island->{$_};
				for($i = 0; $i < $sno; $i++) {
					$point .= "($sArray->[$i]->{x}, $sArray->[$i]->{y})";
				}
			}
			$point .= "��<B>$sno����</B>" if($i > 1 || !$HoutPoint);
		}
		unless($point eq "") {
			if($HoutPoint && ($sno > 1)) {
				logLandSucMatome($island->{'id'}, islandName($island), $mkind{$_}, "$point");
			} else {
				logLandSuc($island->{'id'}, islandName($island), $mkind{$_}, "$point");
			}
		}
		$island->{$_} = undef;
	}
}

# ���ޥ�ɥե�����
sub doCommand {
	my($island) = @_;

	# ���ޥ�ɼ��Ф�
	my($comArray, $command, $c);
	$comArray = $island->{'command'};
	$command = $comArray->[0]; # �ǽ�Τ���Ф�
	slideFront($comArray, 0); # �ʹߤ�ͤ��

	# �����Ǥμ��Ф�
	my($kind, $target, $x, $y, $arg, $target2) = 
	(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'target2'}
	);

	# Ƴ����
	my($name) = islandName($island);
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];
	my($lv2) = $landValue2->[$x][$y];
	my($comName) = $HcomName[$kind];
	my($point) = "($x, $y)";
	my($landName) = landName($landKind, $lv);

	my $cflag = $island->{'itemAbility'}[16];
	my($cost) = $HcomCost[$kind];
	$cost = int($HcomCost[$kind] * $cflag) if($cost > 0);

#$cost = 0;

	if(($kind == $HcomDoNothing) ||
	 (($kind == $HcomGiveup) && $island->{'event'}[0])) {
		if(!$island->{'field'}) {
			# ��ⷫ��
			$island->{'money'} += $HdoNothingMoney;
			$island->{'inMoney'} += $HdoNothingMoney;
			if(!$HflagDoNothing) {
				$island->{'absent'} ++;

				# �ر��¤���Ƚ��
				if ($HarmisticeTurn && ($island->{'absent'} > $HpreGiveupTurn)) {
					# passward��رĥѥ���ɤ��ѹ����西�����
#					$island->{'password'} = encode($ally->{'Takayan'});
					$island->{'preab'} = 1;
					$island->{'comment'} = "����${AfterName}�Ͽر��¤���ˤʤ�ޤ�����";
				}
			}

			# ��ư����
			if($island->{'absent'} >= (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ? $HdevelopGiveupTurn : $HgiveupTurn)) {
				$comArray->[0] = {
					'kind' => $HcomGiveup,
					'target' => 0,
					'x' => 0,
					'y' => 0,
					'arg' => 0,
					'target2' => 0
				};
			}
		}
		return 1;
	}

	$island->{'absent'} = 0;

#-------������¤�ξ��ϡ������ǥ����Ȥ�500�˾�񤭤���---------
	if (($HcomNavy[0] <= $kind) && ($kind <= $HcomNavy[$#HnavyName])) { #������¤��
            if($HnavyBuildTurn[$kind - $HcomNavy[0]] != 0){ #��¤������¸�ߤ���
                $cost = 0;
            }
        }

	# �����ȥ����å�
	my($returnflag) = 0;
	if(($cost > 0) && ($island->{'money'} < $cost)) {
		# ��ξ��
		logNoMoney($id, $name, $comName);
		$returnflag = 1;
	} elsif(($cost < 0) && ($island->{'food'} < (-$cost))) {
		# �����ξ��
		logNoFood($id, $name, $comName);
		$returnflag = 1;
	}
	if(($kind == $HcomAutoPrepare3 || $kind == $HcomFastFarm || $kind == $HcomFastFactory) && ($HislandFightMode == 2)){
		logLandNG($id, $name, $comName, '������Ʈ������Τ���');
		$returnflag = 1;
	}
	if($HoceanMode) {
		if($HlandID[$x][$y] != $id) {
			# �о��Ϸ���ID������Ǥʤ����
			if(($kind < 90) || ((100 < $kind) && ($kind < 200)) || ((330 < $kind) && ($kind < 350)) || ($kind == $HcomNavyWreckRepair) || ($kind == $HcomNavyWreckSell)) {
				# ����(��ȯ)������(����)��ʣ����ߡ�����(��¤) <200 , 330< ����(����) <350 , �ĳ��������ĳ���ѤϤǤ��ʤ�
				logNotAvail($id, $name, $comName);
				$returnflag = 1;
			}
		}
		if(((215 < $kind) && ($kind < 220)) || ((350 < $kind) && ($kind < 361))) {
			# ��ư��ġ���ư���ᡤ���������ѹ������ƹ���ȷ���(����)
			# ��������¤�ʳ��ǡ���ɸ���ꤹ���Τϡ�ǰ�Τ���$target����
			$target = $HlandID[$x][$y];
		}
	}

	if($returnflag) {
		if($island->{'comflag'}) {
			# ����դ��ʤ顢���ޥ�ɤ��᤹
			if($arg > 1) {
				$arg--;
				slideBack($comArray, 0);
				$comArray->[0] = {
					'kind' => $kind,
					'target' => $target,
					'x' => $x,
					'y' => $y,
					'arg' => $arg,
					'target2' => $target2
				};
			}
		}
		return 0;
	}
	# ���ޥ�ɤ�ʬ��
	if($kind == $Hcomshikin){

	    $island->{'money'} += 2000;
	    logPropaganda($id, $name, $comName);

	    # ����դ��ʤ顢���ޥ�ɤ��᤹
	    if($arg > 1) {
	    	    $arg--;
		    slideBack($comArray, 0);
		    $comArray->[0] = {
			    'kind' => $kind,
			    'target' => $target,
			    'x' => $x,
			    'y' => $y,
			    'arg' => $arg,
			    'target2' => $target2
		    };
	    }
	    return $HcomTurn[$kind];
	}elsif(($kind == $HcomPrepare) || ($kind == $HcomPrepare2)) {
		# ���ϡ��Ϥʤ餷
		if(($landKind == $HlandSea) ||
			($landKind == $HlandSbase) ||
			($landKind == $HlandOil) ||
			($landKind == $HlandBouha) ||
			($landKind == $HlandSeaMine) ||
			($landKind == $HlandMountain) ||
			($landKind == $HlandMonster) ||
			($landKind == $HlandHugeMonster) ||
			($landKind == $HlandResource) ||
			(($landKind == $HlandCore) && int($lv / 10000)) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'prepare'}[0] eq '')) ||
			($landKind == $HlandNavy)) {
			# ����������ϡ����ġ������顢���롢�������á�������á�����(��)��ʣ���Ϸ�(����ʤ�)�����������ϤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		if($landKind == $HlandComplex) {
			# ʣ���Ϸ��ʤ������Ϸ�
#			my $cKind = (landUnpack($lv))[1];
			$land->[$x][$y] = $HcomplexAfter[$cKind]->{'prepare'}[0];
			$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'prepare'}[1];
			$island->{'complex'}[$cKind]--;
		} elsif($landKind == $HlandDefence) {
			$island->{'dbase'}--;
		} elsif($landKind == $HlandCore) {
			$island->{'core'}--;
		}
		my $sno = @{$island->{'prepare'}};
		$island->{'prepare'}->[$sno]->{x} = $x;
		$island->{'prepare'}->[$sno]->{y} = $y;

		# ��򺹤�����
		$island->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# �Ϥʤ餷
			$island->{'prepare2'}++;
		} else {
			# ���Ϥʤ顢��¢��β�ǽ������
			if(!$HnoDisFlag && random(1000) < $HdisMaizo) {
				my($v) = 100 + random(901);
				$island->{'money'} += $v;
				logMaizo($id, $name, $comName, $v);
			}
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomPrepare3) {
		# ����Ϥʤ餷
		my($i, $sx, $sy);
		my($prepareM, $prepareFlag) = ($HcomCost[$HcomPrepare2], 0);
		foreach $i (0..$island->{'pnum'}) {
			$sx = $island->{'rpx'}[$i];
			$sy = $island->{'rpy'}[$i];
			last if($island->{'money'} < $HcomCost[$HcomPrepare2]);
			if($land->[$sx][$sy] == $HlandWaste) {
				# ��Ū�ξ���ʿ�Ϥˤ���
				$land->[$sx][$sy] = $HlandPlains;
				$landValue->[$sx][$sy] = 0;
				if(($prepareM > 0) && ($island->{'money'} < $prepareM)) {
					logNoMoney($id, $name, $comName);
					return 0;
				}
				# ��򺹤�����
				$island->{'money'} -= $prepareM;
				my $sno = @{$island->{'prepare'}};
				$island->{'prepare'}->[$sno]->{x} = $sx;
				$island->{'prepare'}->[$sno]->{y} = $sy;
				# �Ϥʤ餷
#				$island->{'prepare2'}++;
				$prepareFlag++;
				if($prepareFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
#		logAllPrepare($id, $name, $comName);
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomReclaim) || ($kind == $HcomReclaim2)) {
		# ���Ω�ơ���®���Ω��
		if(($landKind != $HlandSea) &&
			($landKind != $HlandOil) &&
			($landKind != $HlandBouha) &&
			($landKind != $HlandSeaMine) &&
			($landKind != $HlandSbase) &&
			!(($landKind == $HlandCore) && int($lv / 10000)) &&
			!(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'reclaim'}[0] ne '')) &&
			($landKind != $HlandNavy)) {
			# ����������ϡ����ġ������顢���롢����(��)��ʣ���Ϸ�(���ꤢ��)�������������Ω�ƤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# �����Φ�����뤫�����å�
		my($seaCount) =
			countAround($island, $x, $y, $an[1], $HlandSea, $HlandOil, $HlandSeaMine, $HlandSbase, $HlandResource);
		$seaCount += countAroundNavy($island, $x, $y, $an[1]) if($HnavyReclaim);
		$seaCount += countAroundMonster($island, $x, $y, $an[1]) if($HmonsterReclaim);

		if($seaCount == 7) {
			# ���������������Ω����ǽ
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "��κǳ���", $point);
				return 0;
			}
		}

		if ($landKind == $HlandNavy) {
			# �����ξ�硢�����Τ�
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			my $nSpecial = $HnavySpecial[$nKind];
			unless ($nSpecial & 0x8) {
				# ���ʳ������Ω�ƤǤ��ʤ�
				logLandFail($id, $name, $comName, $landName, $point);
				return 0;
			}

                        if($id != $nId){
                                # ;��η��������Ω�ƤǤ��ʤ�
				logLandFail($id, $name, $comName, $landName, $point);
				return 0;
                        }

			$island->{'navyPort'}--;
			$island->{'shipk'}[$nKind]--;
		} elsif($landKind == $HlandCore) {
			$island->{'core'}--;
		}

		if($landKind == $HlandComplex) {
			# ʣ���Ϸ��ʤ������Ϸ�
#			my $cKind = (landUnpack($lv))[1];
			$land->[$x][$y] = $HcomplexAfter[$cKind]->{'reclaim'}[0];
			$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'reclaim'}[1];
			$island->{'complex'}[$cKind]--;
			#$island->{'area'}++; ���ν����ϸ�����
		} elsif((($landKind == $HlandSea) && ($lv == 1)) || (($landKind == $HlandCore) && (int($lv / 10000) == 1))) {
			# �����ξ��
			# ��Ū�ξ�����Ϥˤ���
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			$island->{'area'}++;

			if($seaCount <= 4) {
				# ����γ���3�إå�������ʤΤǡ������ˤ���
				my($i, $sx, $sy);
				foreach $i (1..6) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					# �Ԥˤ�����Ĵ��
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];

					if (($sx < 0) || ($sy < 0)) {
						# �ϰϳ��ξ�粿�⤷�ʤ�
					} else {
						# �ϰ���ξ��
						$landValue->[$sx][$sy] = 1 if ($land->[$sx][$sy] == $HlandSea);
					}
				}
			}
		} else {
			# ���ʤ顢��Ū�ξ��������ˤ���
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'bouha'}-- if($landKind == $HlandBouha); # ������ΤȤ�
		}
#		logLandSuc($id, $name, $comName, $point);
		my $sno = @{$island->{'reclaim'}};
		$island->{'reclaim'}->[$sno]->{x} = $x;
		$island->{'reclaim'}->[$sno]->{y} = $y;
		# ��򺹤�����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomDestroy) || ($kind == $HcomDestroy2)) {
		# �����®����
		if(($landKind == $HlandSbase) ||
			($landKind == $HlandOil) ||
			($landKind == $HlandSeaMine) ||
			($landKind == $HlandBouha) ||
			($landKind == $HlandMonster) ||
			($landKind == $HlandHugeMonster) ||
			(($landKind == $HlandCore) && (int($lv / 10000) != 2)) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'destroy'}[0] eq '')) ||
			($landKind == $HlandNavy)) {
			# ������ϡ����ġ����롢�����顢���á�������á�����(��)��ʣ���Ϸ�(����ʤ�)�������Ϸ���Ǥ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		if(($landKind == $HlandSea) && (!$lv)) {
			# ���ʤ顢����õ��
			if ($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) {
				# ��ȯ����������Ķػ�
				logNotAvail($id, $name, $comName);
				return 0;
			}
			# ���۷���
			$arg = 1 if(!$arg);
			my($value, $str, $p);
			$value = min($arg * ($cost), $island->{'money'});
			$str = "$value$HunitMoney";
			$p = int($value / $cost) if($cost);
			$island->{'money'} -= $value;

			# ���Ĥ��뤫Ƚ��
			if($p > random(100) + $island->{'oil'} * 25) {
				# ���ĸ��Ĥ���
				logOilFound($id, $name, $point, $comName, $str);
				$land->[$x][$y] = $HlandOil;
				$landValue->[$x][$y] = 0;
				$island->{'oil'}++;
			} else {
				# ̵�̷���˽����
				logOilFail($id, $name, $point, $comName, $str);
			}
			return $HcomTurn[$kind];
		}

		# ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
		if($landKind == $HlandMountain) {
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
		} elsif($landKind == $HlandSea) {
			$landValue->[$x][$y] = 0;
		} elsif($landKind == $HlandCore) {
			$land->[$x][$y] = $HlandSea;
			if(int($lv / 10000) == 1) {
				$landValue->[$x][$y] = 0;
			} else {
				$landValue->[$x][$y] = 1;
			}
			$island->{'core'}--;
		} elsif($landKind == $HlandComplex) {
			# ʣ���Ϸ��ʤ������Ϸ�
#			my $cKind = (landUnpack($lv))[1];
			$land->[$x][$y] = $HcomplexAfter[$cKind]->{'destroy'}[0];
			$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'destroy'}[1];
			$island->{'complex'}[$cKind]--;
		} else {
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'area'}--;
			$island->{'dbase'}-- if($landKind == $HlandDefence);
		}
#		logLandSuc($id, $name, $comName, $point);
		my $sno = @{$island->{'destroy'}};
		$island->{'destroy'}->[$sno]->{x} = $x;
		$island->{'destroy'}->[$sno]->{y} = $y;

		# ��򺹤�����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSellTree) {
		# Ȳ��
		if($landKind != $HlandForest) {
			# ���ʳ���Ȳ�ΤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
#		logLandSuc($id, $name, $comName, $point);
		my $sno = @{$island->{'selltree'}};
		$island->{'selltree'}->[$sno]->{x} = $x;
		$island->{'selltree'}->[$sno]->{y} = $y;

		# ��Ѷ������
		$island->{'money'} += $HtreeValue * $lv;
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomPlant) ||
                ($kind == $HcomPlant2) ||
		($kind == $HcomFarm) ||
		($kind == $HcomFastFarm) ||
		($kind == $HcomFactory) ||
		($kind == $HcomFastFactory) ||
		($kind == $HcomBase) ||
		($kind == $HcomMonument) ||
		($kind == $HcomHaribote) ||
		($kind == $HcomBouha) ||
		($kind == $HcomDbase) ||
		($kind == $HcomDbase2)) {

		# �Ͼ���߷�
		if(!
			(($landKind == $HlandPlains) ||
			($landKind == $HlandTown) ||
			(($landKind == $HlandMonument) && ($kind == $HcomMonument)) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFarm || $kind == $HcomFastFarm)) ||
			(($landKind == $HlandFactory) && ($kind == $HcomFactory || $kind == $HcomFastFactory)) ||
			(($landKind == $HlandSea) && ($lv == 1) && ($kind == $HcomBouha)) ||
			(($landKind == $HlandBouha) && ($kind == $HcomBouha)) ||
			(($landKind == $HlandDefence) && ($kind == $HcomDbase)) ||
			(($landKind == $HlandDefence) && ($kind == $HcomDbase2)))) {

			# ��Ŭ�����Ϸ�
			logLandFail($id, $name, $comName, $landName, $point);
			if($island->{'comflag'}) {
				# ����դ��ʤ顢���ޥ�ɤ��᤹
				if(($kind == $HcomFarm) ||
					($kind == $HcomFactory) ||
					(($kind == $HcomDbase) && $HdurableDef)) {
					if($arg > 1) {
						$arg--;
						slideBack($comArray, 0);
						$comArray->[0] = {
							'kind' => $kind,
							'target' => $target,
							'x' => $x,
							'y' => $y,
							'arg' => $arg,
							'target2' => $target2
						};
					}
				}
			}
			return 0;
		}

		# �����ʬ��
		if(($kind == $HcomPlant) ||
                   ($kind == $HcomPlant)) {
			# ��Ū�ξ��򿹤ˤ��롣
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # �ڤϺ���ñ��
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			return if(!$HuseBase);
			# ��Ū�ξ���ߥ�������Ϥˤ��롣
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # �и���0
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomHaribote) {
			# ��Ū�ξ���ϥ�ܥƤˤ���
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
		    if ($HdBaseHide) { # �ɱһ��ߤ򿹤˵�������?
				logPBSuc($id, $name, $comName, $point);
		    } else {
				logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
			}
		} elsif($kind == $HcomBouha) {
			return if(!$HuseBouha);
			# ��Ū�ξ���������ˤ��롣
			if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
				my($map) = $island->{'map'};
				my(@x) = @{$map->{'x'}};
				my(@y) = @{$map->{'y'}};
				if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
					logLandFail($id, $name, $comName, "��κǳ���", $point);
					return 0;
				}
			}
			if($island->{'bouha'} >= $HuseBouha) {
				# ��ͭ��ǽ����������С�
				logOverFail($id, $name, $comName, $point);
				return 0;
			}
			$land->[$x][$y] = $HlandBouha;
			$landValue->[$x][$y] = 0;
			$island->{'bouha'}++;
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomFarm || $kind == $HcomFastFarm) {
			# ����
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			if($rep > 1) {
				my $value = min($rep * $cost, $island->{'money'});
				$rep = int($value / $cost) if($cost);
				$comName .= "($rep��)";
				$cost *= $rep;
				$arg = 1;
			}
			if($landKind == $HlandFarm) {
				# ���Ǥ�����ξ��
				$landValue->[$x][$y] += 2*$rep; # ���� + 2000��
			} else {
				# ��Ū�ξ��������
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10 + 2*($rep - 1); # ���� = 10000��
			}
			if($landValue->[$x][$y] > 50) {
				$landValue->[$x][$y] = 50; # ���� 50000��
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomFactory || $kind == $HcomFastFactory) {
			# ����
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			if($rep > 1) {
				my $value = min($rep * $cost, $island->{'money'});
				$rep = int($value / $cost) if($cost);
				$comName .= "($rep��)";
				$cost *= $rep;
				$arg = 1;
			}
			if($landKind == $HlandFactory) {
				# ���Ǥ˹���ξ��
				$landValue->[$x][$y] += 10*$rep; # ���� + 10000��
			} else {
				# ��Ū�ξ��򹩾��
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30 + 10*($rep - 1); # ���� = 10000��
			}
			if($landValue->[$x][$y] > 100) {
				$landValue->[$x][$y] = 100; # ���� 100000��
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif(($kind == $HcomDbase) ||
		        ($kind == $HcomDbase2)) {
			# �ɱһ���
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			# ���٤˿���ʬ���ѵ��Ϥ��ɲä��������
			# ���1�Ԥ򥳥��ȥ����Ȥ��Ʋ��Υ����Ȥ�Ϥ���
			#my $rep = $arg;
			if($landKind == $HlandDefence) {
				# ���Ǥ��ɱһ��ߤξ��
				if(!$HdurableDef) {
					$landValue->[$x][$y] += 10000; # �������֥��å�
					logBombSet($id, $name, $landName, $point);
					$island->{'money'} -= $cost;
					return $HcomTurn[$kind];
				} elsif($arg == $HdefExplosion) {
					$landValue->[$x][$y] += 10000; # �������֥��å�
					logBombSet($id, $name, $landName, $point);
					$island->{'money'} -= $cost;
					return $HcomTurn[$kind];
				} else {
					if($rep > 1) {
						my $value = min($rep * $cost, $island->{'money'});
						$rep = int($value / $cost) if($cost);
						$cost *= $rep;
						$arg = 1;
					}
					if($landValue->[$x][$y] == $HdurableDef - 1) {
						logBombDurableMax($id, $name, $landName, $point, $HdBaseHide);
					} else {
						$landValue->[$x][$y] += $rep;
						$landValue->[$x][$y] = $HdurableDef - 1 if($landValue->[$x][$y] > $HdurableDef - 1);
						logBombDurableUp($id, $name, $landName, $point, $rep, $HdBaseHide);
					}
				}
			} else {
				if($HdBaseMax && ($island->{'dbase'} >= $HdBaseMax)) {
					logOverFail($id, $name, $comName, $point);
					return 0;
				}
				if($rep > 1) {
					my $value = min($rep * $cost, $island->{'money'});
					$rep = int($value / $cost) if($cost);
					$rep = min($rep, $HdurableDef) if($HdurableDef);
					$comName .= "(�ѵ���$rep)";
					$cost *= $rep;
					$arg = 1;
				}
				# ��Ū�ξ����ɱһ��ߤ�
				$land->[$x][$y] = $HlandDefence;
				$rep = 1 if(!$HdurableDef);
				$landValue->[$x][$y] = $rep - 1;
				$island->{'dbase'}++;
				if ($HdBaseHide) { # �ɱһ��ߤ򿹤˵�������?
				    logPBSuc($id, $name, $comName, $point);
				} else {
				    logLandSuc($id, $name, $comName, $point);
				}
			}
		} elsif($kind == $HcomMonument) {
			# ��ǰ��
			if($HuseBigMissile && ($landKind == $HlandMonument)) {
				# ���Ǥ˵�ǰ��ξ��

				# �������åȼ���
				my($tn) = $HidToNumber{$target};
				my($tIsland) = $Hislands[$tn];
				my(%amityFlag);
				my($amity) = $island->{'amity'};
				foreach (@$amity) {
					$amityFlag{$_} = 1;
				}
				# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��
				if (
					($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn || $amityFlag{$target})) ||
					($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
					) {
					# ���⤬���Ĥ���Ƥ��ʤ�
					logNotAvail($id, $name, $comName);
					return 0;
				} elsif(($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($id, $name, $comName);
					return 0;

				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($id, $name, $comName, '���߳�ȯ������Τ���');
						return 0;
					} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
						# ������ꤸ��ʤ��������
						logLandNG($id, $name, $comName, '��ɸ���������Ǥʤ�����');
						return 0;
					}
				} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
					my $warflag = chkWarIsland($id, $target);
					if(!$warflag) {
						logLandNG($id, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
						return 0;
					} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
						logLandNG($id, $name, $comName, 'ͱͽ������Τ���');
						return 0;
					}
				} elsif($tIsland->{'event'}[0]) {
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($id, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
						return 0;
					} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# ���٥�ȥ����פ����Х��Х�
						logLandNG($id, $name, $comName, '���Х��Х볫����Τ���');
						return 0;
					}
				}

				if($tn eq '') {
					# �������åȤ����Ǥˤʤ�
					# ������鷺�����
					return 0;
				}

				$tIsland->{'bigmissile'}++;
				$island->{'ext'}[1] += $cost; #�׸���
				$tIsland->{'ext'}[1] += $cost; #�׸���

				# ���ξ��Ϲ��Ϥ�
				$land->[$x][$y] = $HlandWaste;
				$landValue->[$x][$y] = 0;
				logMonFly($id, $name, $landName, $point);
			} else {
				# ��Ū�ξ���ǰ���
				$land->[$x][$y] = $HlandMonument;
				$arg = 0 if($arg >= $HmonumentNumber);
				$landValue->[$x][$y] = $arg;
				logLandSuc($id, $name, $comName, $point);
			}
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if(($kind == $HcomFarm) ||
			($kind == $HcomFactory) ||
			(($kind == $HcomDbase) && $HdurableDef)) {
			if($arg > 1) {
				$arg--;
				slideBack($comArray, 0);
				$comArray->[0] = {
					'kind' => $kind,
					'target' => $target,
					'x' => $x,
					'y' => $y,
					'arg' => $arg,
					'target2' => $target2
				};
			}
		}
		return $HcomTurn[$kind];

	} elsif (($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) {
		# ʣ���Ϸ�����

                # ʿ�Ϥ�Ȳ�Τϥ���
		if(($landKind == $HlandPlains) && ($kind == $HcomComplex[4])){
			# ���ʳ���Ȳ�ΤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

                # �ԻԤ�Ȳ�Τ����
		if(($landKind == $HlandTown) && ($kind == $HcomComplex[4])){
			# ���ʳ���Ȳ�ΤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		$arg = 1 if(!$arg);
		my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
		if($rep > 1) {
			my $value = min($rep * $cost, $island->{'money'});
			$rep = int($value / $cost) if($cost);
			$comName .= "($rep��)";
			$cost *= $rep;
			$arg = 1;
		}
		unless (buildComplex($island, $comName, $kind - $HcomComplex[0], $rep, $x, $y)) {
			if($island->{'comflag'}) {
				if($arg > 1) {
					$arg--;
					slideBack($comArray, 0);
					$comArray->[0] = {
						'kind' => $kind,
						'target' => $target,
						'x' => $x,
						'y' => $y,
						'arg' => $arg,
						'target2' => $target2
					};
				}
			}
			return 0;
		}

		$island->{'money'} -= $cost;
		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if($arg > 1) {
			$arg--;
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg,
				'target2' => $target2
			};
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomMountain) {
		# �η���
		if($landKind != $HlandMountain) {
			# ���ʳ��ˤϺ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			if($island->{'comflag'}) {
				if($arg > 1) {
					$arg--;
					slideBack($comArray, 0);
					$comArray->[0] = {
						'kind' => $kind,
						'target' => $target,
						'x' => $x,
						'y' => $y,
						'arg' => $arg,
						'target2' => $target2
					};
				}
			}
			return 0;
		}
		$arg = 1 if(!$arg);
		my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
		if($rep > 1) {
			my $value = min($rep * $cost, $island->{'money'});
			$rep = int($value / $cost) if($cost);
			$comName .= "($rep��)";
			$cost *= $rep;
			$arg = 1;
		}

		$landValue->[$x][$y] += 5*$rep; # ���� + 5000��
		if($landValue->[$x][$y] > 200) {
			$landValue->[$x][$y] = 200; # ���� 200000��
		}
		logLandSuc($id, $name, $comName, $point);

		# ��򺹤�����
		$island->{'money'} -= $cost;
		if($arg > 1) {
			$arg--;
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg,
				'target2' => $target2
			};
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSeaMine) {
		# ����
		return if(!$HuseSeaMine);
		if($landKind == $HlandSeaMine){
			# ���Ǥ˵���ʤ����
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, '�������', '(?, ?)');
			$arg = min($lv, int($island->{'money'} / ($cost * 0.2))) if($cost);
			$island->{'money'} -= $arg * ($cost * 0.2);
			$island->{'mine'}--;
			return $HcomTurn[$kind];
		} elsif(($landKind != $HlandSea) || $lv){
			# ���ʳ��ˤϺ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "��κǳ���", $point);
				return 0;
			}
		}
		if($island->{'mine'} >= $HuseSeaMine) {
			logOverFail($id, $name, $comName, $point);
			return 0;
		}

		# �˲��Ͼ�� $HmineDamageMax
		if(!$arg){
			$arg = 1;
		} elsif($arg > $HmineDamageMax){
			$arg = $HmineDamageMax;
		}
		my $value = min($arg * $cost, $island->{'money'});
		$arg = int($value / $cost) if($cost);
		$land->[$x][$y] = $HlandSeaMine;
		$landValue->[$x][$y] = $arg; # �˲���
		logLandSuc($id, $name, $comName, '(?, ?)');

		# ��򺹤�����
		$island->{'money'} -= $value;
		$island->{'mine'}++;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSbase) {
		# �������
		return if(!$HuseSbase || $Htournament);
		if(($landKind != $HlandSea) || $lv){
			# ���ʳ��ˤϺ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "��κǳ���", $point);
				return 0;
			}
		}

		$land->[$x][$y] = $HlandSbase;
		$landValue->[$x][$y] = 0; # �и���0
		logLandSuc($id, $name, $comName, '(?, ?)');

		# ��򺹤�����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomCore) {
		return if(!$HuseCore);
		if ($HuseCoreLimit && ($HislandTurn - $island->{'birthday'} > $HdevelopTurn)) {
			logDevelopTurnFail2($id, $name, $comName);
			return 0;
		}
		# ����
		$arg = 1 if(!$arg);
		my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
		# ���٤˿���ʬ���ѵ��Ϥ��ɲä��������
		# ���1�Ԥ򥳥��ȥ����Ȥ��Ʋ��Υ����Ȥ�Ϥ���
		#my $rep = $arg;
		if($landKind == $HlandCore) {
			# ���Ǥ˥����ξ��
			if(!$HdurableCore) {
				# ��Ŭ�����Ϸ�
				logLandFail($id, $name, $comName, $landName, $point);
				if($island->{'comflag'}) {
					if($arg > 1) {
						$arg--;
						slideBack($comArray, 0);
						$comArray->[0] = {
							'kind' => $kind,
							'target' => $target,
							'x' => $x,
							'y' => $y,
							'arg' => $arg,
							'target2' => $target2
						};
					}
				}
				return 0;
			} else {
				if($rep > 1) {
					my $value = min($rep * $cost, $island->{'money'});
					$rep = int($value / $cost) if($cost);
					$cost *= $rep;
					$arg = 1;
				}
				if($lv % 10000 == $HdurableCore - 1) {
					logBombDurableMax($id, $name, $landName, $point, $HcoreHide);
				} else {
					$rep = ($HdurableCore - 1) - ($lv % 10000) if($rep > ($HdurableCore - 1) - ($lv % 10000));
					$landValue->[$x][$y] += $rep;
					logBombDurableUp($id, $name, $landName, $point, $rep, $HcoreHide);
				}
			}
		} else {
			if(($landKind != $HlandPlains) && ($landKind != $HlandSea)) {
				# ʿ�Ϥ����Ǥʤ���к��ʤ�
				logLandFail($id, $name, $comName, $landName, $point);
				if($island->{'comflag'}) {
					if($arg > 1) {
						$arg--;
						slideBack($comArray, 0);
						$comArray->[0] = {
							'kind' => $kind,
							'target' => $target,
							'x' => $x,
							'y' => $y,
							'arg' => $arg,
							'target2' => $target2
						};
					}
				}
				return 0;
			} elsif($HcoreMax && ($island->{'core'} >= $HcoreMax)) {
				logOverFail($id, $name, $comName, $point);
				if($island->{'comflag'}) {
					if($arg > 1) {
						$arg--;
						slideBack($comArray, 0);
						$comArray->[0] = {
							'kind' => $kind,
							'target' => $target,
							'x' => $x,
							'y' => $y,
							'arg' => $arg,
							'target2' => $target2
						};
					}
				}
				return 0;
			}
			if($rep > 1) {
				my $value = min($rep * $cost, $island->{'money'});
				$rep = int($value / $cost) if($cost);
				$rep = min($rep, $HdurableCore) if($HdurableCore);
				$comName .= "(�ѵ���$rep)";
				$cost *= $rep;
				$arg = 1;
			}
			# ��Ū�ξ��򥳥���
			$land->[$x][$y] = $HlandCore;
			$rep = 1 if(!$HdurableCore);
			$landValue->[$x][$y] = $rep - 1;
			$island->{'core'}++;
			if($landKind == $HlandSea) {
				$landValue->[$x][$y] += (!$lv) ? 20000 : 10000; # ��������
			}
			if ($HcoreHide) { # ������������?
				if($landKind == $HlandPlains) {
				    logPBSuc($id, $name, $comName, $point);     # ��
				} else {
					logLandSuc($id, $name, $comName, '(?, ?)'); # ��
				}
			} else {
			    logLandSuc($id, $name, $comName, $point);
			}
		}
		# ��򺹤�����
		$island->{'money'} -= $cost;
		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if($arg > 1) {
			$arg--;
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg,
				'target2' => $target2
			};
		}
		return $HcomTurn[$kind];

	} elsif (($HcomMissile[0] <= $kind) && ($kind <= $HcomMissile[$#HmissileName])) {
#		return if(!$HuseBase || !HuseSbase);
		# �ߥ������
		if((($HflagCommand += $HflagST) >= int($island->{'itemAbility'}[6])) && $STcheck{$kind}) {
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg
			};
			return 1;
		}


		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];

		if ($id != $target) {
			# ¾����ؤι���

			# ȯ�Ͳ��ݳ�ǧ
			# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��
			if (
				($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# ���⤬���Ĥ���Ƥ��ʤ�
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '���߳�ȯ������Τ���');
					return 0;
				} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
					# ������ꤸ��ʤ��������
					logLandNG($id, $name, $comName, '��ɸ���������Ǥʤ�����');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
				my $warflag = chkWarIsland($id, $target);
				if(!$warflag) {
					logLandNG($id, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
					return 0;
				} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
					logLandNG($id, $name, $comName, 'ͱͽ������Τ���');
					return 0;
				}
			} elsif($tIsland->{'event'}[0]) {
				if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
					return 0;
				} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
					# ���٥�ȥ����פ����Х��Х�
					logLandNG($id, $name, $comName, '���Х��Х볫����Τ���');
					return 0;
				}
			}
		}

		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		# 0�ξ��Ϸ�Ƥ����
		$arg = 10000 if($arg == 0);

		# �ߥ�����ȯ��
		require('./hako-missile.cgi');
		return 0 unless(missileFire($target, $island, $tIsland, $x, $y, $kind, $arg, $cost));
		if (!$HcomTurn[$kind] && ($HmissileSpecial[$kind - $HcomMissile[0]] & 0x1)) {
			# ���Υ��ޥ�ɤ� ST�ߥ����뤫 ST�����ɸ��Ǥʤ���Х��������ʤ�
			$HflagST = 1 if($HattackST);
			return 0 if (!($STcheck{$comArray->[0]->{'kind'}}) &&
				 ($comArray->[0]->{'kind'} != $HcomSendMonsterST));
		}
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomSendMonster) ||
		($kind == $HcomSendMonsterST)) {
		# �����ɸ�
		return if((!$HuseSendMonster && ($kind == $HcomSendMonster)) || (!$HuseSendMonsterST && ($kind == $HcomSendMonsterST)) || $Htournament);
		if((($HflagCommand += $HflagST) >= int($island->{'itemAbility'}[6])) && ($kind == $HcomSendMonsterST)) {
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg
			};
			return 1;
		}
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);


		if ($id != $target) {
			# ¾����ؤι���
			if($HoceanMode && $HnotuseMonsterSend) {
				my($fw) = $island->{'wmap'};
				my($tw) = $tIsland->{'wmap'};
				if($HislandConnect[$fw->{'x'}][$fw->{'y'}] == $HislandConnect[$tw->{'x'}][$tw->{'y'}]) {
					logLandNG($id, $name, $comName, '���褬��³���Ƥ��뤿��');
					return 0;
				}
			}

			my(%amityFlag);
			my($amity) = $island->{'amity'};
			foreach (@$amity) {
				$amityFlag{$_} = 1;
			}
			# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��
			if (
				($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn || $amityFlag{$target})) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# ���⤬���Ĥ���Ƥ��ʤ�
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '���߳�ȯ������Τ���');
					return 0;
				} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
					# ������ꤸ��ʤ��������
					logLandNG($id, $name, $comName, '��ɸ���������Ǥʤ�����');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
				my $warflag = chkWarIsland($id, $target);
				if(!$warflag) {
					logLandNG($id, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
					return 0;
				} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
					logLandNG($id, $name, $comName, 'ͱͽ������Τ���');
					return 0;
				}
			} elsif($tIsland->{'event'}[0]) {
				if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
					return 0;
				} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
					# ���٥�ȥ����פ����Х��Х�
					logLandNG($id, $name, $comName, '���Х��Х볫����Τ���');
					return 0;
				}
			}
		}

		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		# ��å�����
		if ($kind == $HcomSendMonsterST) {
			logMonsSendST($id, $target, $name, $tName);
		} else {
			logMonsSend($id, $target, $name, $tName);
		}


		my $huge = 0;
		if($arg >= 50 && ($HsendHugeMonsterNumber >= 0) && $HhugeMonsterAppear) {
			$huge = 1;
			$arg -= 50;
			$arg = $HsendHugeMonsterNumber if($arg > $HsendHugeMonsterNumber);
			$cost = ($kind == $HcomSendMonsterST) ? $HhugeMonsterCostST[$arg] : $HhugeMonsterCost[$arg];
		} else {
			$arg = $HsendMonsterNumber if($arg > $HsendMonsterNumber);
			$cost = ($kind == $HcomSendMonsterST) ? $HmonsterCostST[$arg] : $HmonsterCost[$arg];
		}
		# �ᥫ���Τ������
		bringMonster($tIsland, ($kind == $HcomSendMonsterST) ? 0 : $id, $arg, $huge);

		$island->{'money'} -= $cost;
		$island->{'ext'}[1] += $cost; # �׸���
		$tIsland->{'ext'}[1] += $cost; # �׸���

		if (!$HcomTurn[$kind] && ($kind == $HcomSendMonsterST)) {
			# ���Υ��ޥ�ɤ� ST�ߥ����뤫 ST�����ɸ��Ǥʤ���Х��������ʤ�
			$HflagST = 1 if($HattackST);
			return 0 if (!($STcheck{$comArray->[0]->{'kind'}}) &&
				 ($comArray->[0]->{'kind'} != $HcomSendMonsterST));
		}
		return $HcomTurn[$kind];

	} elsif (($HcomNavy[0] <= $kind) && ($kind <= $HcomNavy[$#HnavyName])) {
		# ������¤
		return 0 unless (buildNavy($island, $comName, $kind - $HcomNavy[0], $arg, $x, $y));

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif (($HcomNavy2[0] <= $kind) && ($kind <= $HcomNavy2[3])) {
		# �Ҷ�������ȯ��
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];

		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

                my $nKind;
                if($kind == $HcomNavy2[0]){
                    $nKind = 3;
                }elsif($kind == $HcomNavy2[1]){
                    $nKind = 4;
                }elsif($kind == $HcomNavy2[2]){
                    $nKind = 6;
                }elsif($kind == $HcomNavy2[3]){
                    $nKind = 15;
                }

		return 0 unless (buildNavy2($tIsland, $comName, $nKind, $arg, $x, $y, $id));

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];
	} elsif (($kind == $HcomNavyMove) || ($kind == $HcomNavySend) || ($kind == $HcomNavyReturn)) {
		# �����ư(�ɸ�������)

		my($ftarget, $ttarget);
		if($kind == $HcomNavyMove) {
			# �����ư
			($ftarget, $ttarget) = ($target, $target2);
		} elsif($kind == $HcomNavySend) {
			# �����ɸ�
			($ftarget, $ttarget) = ($id, $target);
		} else {
			# ���ⵢ��
			($ftarget, $ttarget) = ($target, $id);
		}
		$comName = ($id == $ttarget) ? '���ⵢ��' : '�����ɸ�';
		# �����ư���������åȼ���
		my($fn) = $HidToNumber{$ftarget};
		if($fn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($fromIsland) = $Hislands[$fn];

		# �����ư�西�����åȼ���
		my($tn) = $HidToNumber{$ttarget};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($toIsland) = $Hislands[$tn];
		if($HoceanMode && $HnotuseNavyMove) {
			my($fw) = $fromIsland->{'wmap'};
			my($tw) = $toIsland->{'wmap'};
			if($HislandConnect[$fw->{'x'}][$fw->{'y'}] == $HislandConnect[$tw->{'x'}][$tw->{'y'}]) {
				logLandNG($id, $name, $comName, '���褬��³���Ƥ��뤿��');
				return 0;
			}
		}

                # �ɸ����ݥե饰�����
                $moveErrorFlag = 0;

		if ($id != $ttarget) {
			# ¾����ؤι���
			# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��

			if (($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# ���⤬���Ĥ���Ƥ��ʤ�
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $toIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $toIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
				return 0;
			} elsif($HnofleetNotAvail && !$toIsland->{'field'} && !$toIsland->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "�������ͭ���ʤ�$AfterName�Ǥ��ä�����");
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '���߳�ȯ������Τ���');
					return 0;
				} elsif($island->{'fight_id'} != $toIsland->{'id'}) {
					# ������ꤸ��ʤ��������
					logLandNG($id, $name, $comName, '��ɸ���������Ǥʤ�����');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$toIsland->{'field'} && !$HarmisticeTurn && !$HsurvivalTurn) {
                                # ̱�����ɸ��β�ǽ��������Τǡ������Ǥ�return��̵���ˤ���
                                # ����˥ե饰Ω�Ƥơ�movefleet�Υ롼������ǥ��顼�֤�

				my(%amityFlag);
				my($amity) = $island->{'amity'};
				foreach (@$amity) {
					$amityFlag{$_} = 1;
				}
				if(!$amityFlag{$ttarget}) { 
					my $warflag = chkWarIsland($id, $ttarget);
#					if(!$warflag) {
#						logLandNG($id, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
#						return 0;
#					} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
#						logLandNG($id, $name, $comName, 'ͱͽ������Τ���');
#						return 0;
#					}

					if($warflag != 2) {
                                            $moveErrorFlag = 1;
                                        }
				}

			} elsif($toIsland->{'event'}[0]) {
				my $level = 2 ** gainToLevel($island->{'gain'});
				if(($toIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $toIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
					return 0;
				} elsif($toIsland->{'event'}[3] && ($toIsland->{'event'}[3] <= $island->{"invade$ttarget"})) {
					logLandNG($id, $name, $comName, '�ɸ���ǽ��������Ķ���뤿��');
					return 0;
				} elsif($HmaxComNavyLevel && !($toIsland->{'event'}[5] & (2 ** gainToLevel($island->{'gain'})))) {
					logLandNG($id, $name, $comName, '�ɸ���ǽ��٥�Ǥʤ�����');
					return 0;
				} elsif((!$toIsland->{'event'}[11]) && ($HislandTurn > $toIsland->{'event'}[1])) {
					# �ɲ��ɸ�����Ĥ��ʤ�
					logLandNG($id, $name, $comName, '���٥�ȳ�����Τ���');
					return 0;
				}

			} elsif($island->{'NavyAttack_flag'}[$arg - 1]) {
				# ���ޥ�ɤ���Ĥ��ʤ�
				logLandNG($id, $name, $comName, '��Ʈ���֤ˤ��뤿��');
				return 0;
			}
		}


		# ������Τ�
		$arg--;
		if ($arg < 0) {
			$arg = 0;
		} elsif ($arg > 3) {
			$arg = 3;
		}

		# ������ư����
		return 0 unless (moveFleet($island, $fromIsland, $toIsland, $arg));
		$island->{'money'} -= $cost;
		if($id != $ttarget) {
			$island->{'ext'}[1] += $cost; # �׸���
			$toIsland->{'ext'}[1] += $cost; # �׸���
			$island->{'NavyMove_flag'}[$arg] = 1; # ��ư�ե饰��Ω�Ƥ�
		}
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyForm) {
		# ��������
		if ($landKind != $HlandNavy) {
			# �����������������Ǥ��ʤ�
			logNavyFormFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# �����ĳ���¾����δ��⡢�ϴ��������Ǥ��ʤ�
			logNavyFormFail($id, $name, $point, $landName);
			return 0;
		}

		# ������Τ�
		$arg--;
		if ($arg < 0) {
			$arg = 0;
		} elsif ($arg > 3) {
			$arg = 3;
		}
		my $ofname1 = $island->{'fleet'}->[$nNo];
		my $ofname2 = $island->{'fleet'}->[$arg];

		my $nflag = $island->{'itemAbility'}[3];
		if($HfleetMaximum && ($island->{'ships'}[$arg] >= $HfleetMaximum + int($nflag/4))){
			logNavyFormMaxOver($id, $name, $point, $landName, $ofname1, $ofname2);
			return 0;
		}

		$island->{'ships'}[$nNo]--;
		$island->{'ships'}[$arg]++;
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $arg, $nKind, $wait, $nHp, $goalx, $goaly);

		logNavyForm($id, $name, $point, $landName, $ofname1, $ofname2);

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyExpell) {
		# ��������(��ɸ�ϻ���)
		if ($landKind != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
			logNavyTargetFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# ����¾����δ���Ͻ��ҤˤǤ��ʤ�
			logNavyTargetFail($id, $name, $point, $landName);
			return 0;
		}

		#$landValue->[$x][$y] = navyPack(0, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp); # ��°��ʤ��ˤ���
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack(0, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # ��°��ʤ�(�̾�)�ˤ���

		logNavyTarget($id, $name, $point, $landName);

		$island->{'money'} -= $cost;
		$island->{'shipk'}[$nKind]--;
		$island->{'ships'}[$nNo]--;
		$island->{'ships'}[4]--;
		# ���Х��Х�
		$island->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyDestroy) {
		# �����˴�

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];

		if ($tL != $HlandNavy) {
			# ���������˴��Ǥ��ʤ�
			logNavyDestroyFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];

		if (($nSpecial & 0x8) || ($nId != $id)) {
			# ����¾����δ�����˴��Ǥ��ʤ�
			logNavyDestroyFail($id, $name, $point, $tLandName);
			return 0;
		}

		$tLand->[$x][$y] = $HlandSea; # ���ˤ���
		$tLandValue->[$x][$y] = 0;

		logNavyDestroy($id, $name, $point, $tLandName, $tId);

		$island->{'money'} -= $cost;
		$island->{'shipk'}[$nKind]--;
		$island->{'ships'}[$nNo]--;
		$island->{'ships'}[4]--;
		# ���Х��Х�
		$island->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyWreckRepair) {
		# �ĳ�����
		if ($landKind != $HlandNavy) {
			# �������������Ǥ��ʤ�
			logNavyWreckRepairFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless ($nFlag == 1) {
			# �ĳ��ʳ��Ͻ����Ǥ��ʤ�
			logNavyWreckRepairFail($id, $name, $point, $landName);
			return 0;
		}
		$cost = int($HnavyCost[$nKind] * ($nExp / 100.0) * $cflag);
		if ($island->{'money'} < $cost) {
			# ��⤬­��ʤ�
			logNoMoney($id, $name, $comName);
			return 0;
		}

		# ������Τ�
		$arg--;
		if ($arg < 0) {
			$arg = 0;
		} elsif ($arg > 3) {
			$arg = 3;
		}

		my $ofname = $island->{'fleet'}->[$arg];

		# ��ͭ��ǽ�����������å�
		my $nflag = int($island->{'itemAbility'}[3]);
		my $nflagk = (!$#HnavyName) ? 1 : int($nflag/$#HnavyName);
		$nflagk = 1 if($nflag && ($nflagk < 1));
		if($HnavyMaximum && ($island->{'ships'}[4] >= $HnavyMaximum + $nflag)) {
			logNavyMaxOver($id, $name, $comName);
			return 0;
		} elsif($HportRetention && ($island->{'ships'}[4] >= $island->{'navyPort'} * $HportRetention + $nflag)) {
			logFleetMaxOver($id, $name, $comName, "������������");
			return 0;
		} elsif($HfleetMaximum && ($island->{'ships'}[$arg] >= $HfleetMaximum + int($nflag/4))) {
			logNavyWreckRepairMaxOver($id, $name, $point, $landName, "${ofname}����");
			return 0;
		} elsif($HnavyKindMax[$nKind] && ($island->{'shipk'}[$nKind] >= $HnavyKindMax[$nKind] + $nflagk)) {
			logNavyKindMaxOver($id, $name, $comName);
			return 0;
		}
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($id, $nTmp, $nStat, $nSea, 0, 0, $arg, $nKind, $wait, $HnavyHP[$nKind], $goalx, $goaly);
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$arg]++;
		$island->{'ships'}[4]++;

		# ��ư�Ѥߤˤ���
		$HnavyMove[$id][$x][$y] = 2;

		logNavyWreckRepair($id, $name, $point, $landName, $cost, "${ofname}����");

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyWreckSell) {
		# �ĳ����
		if ($landKind != $HlandNavy) {
			# ����������ѤǤ��ʤ�
			logNavyWreckSellFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless ($nFlag& 1) {
			# �ĳ��ʳ�����ѤǤ��ʤ�
			logNavyWreckSellFail($id, $name, $point, $landName);
			return 0;
		}

		# ��Ѳ��ʤϡֻĳ��β��� �� ���(50%��100%)��
		$cost = int($HnavyCost[$nKind] * (1.0 - $nHp / 100.0) * ((rand(6) + 5) / 10.0));

		$land->[$x][$y] = $HlandSea; # ���ˤʤ�
		$landValue->[$x][$y] = 0;

		if (rand(100) < $HnavyProbWreckGold) {
			my $cost = int(rand(10) + 1) * 100; # 100����1000����
			logNavyWreckSellLucky($id, $name, $point, $landName, $cost);
			$island->{'money'} += $cost;
		} elsif($HitemRest && $HitemGetDenominator3 && (random($HitemGetDenominator3) < $island->{'gain'})) {
			# �����ƥ����Ƚ��
			my $num = @Hitem;
			$num = random($num);
			push(@{$island->{'item'}}, $Hitem[$num]);
			$HitemGetId[$Hitem[$num]]{$id} = 1;
			$HitemRest--;
			logItemGetLucky2($id, $name, $point, $HitemName[$Hitem[$num]], "$landName������夲���Ȥ���");
			splice(@Hitem, $num, 1);
		}

		logNavyWreckSell($id, $name, $point, $landName, $cost);

		$island->{'money'} += $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomMoveTarget) {
		# ����(�ɸ�����)���ư
		return if(!$HuseFlag);

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];

		my $sFlag = 0;
		if(($tL != $HlandNavy) && ($tL != $HlandMonster)) {
			if($tL == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$x][$y]);
				$sFlag = ($HhugeMonsterSpecial[$mKind] & 0x80);
				if(!$sFlag) {
					logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "�����Ǥʤ����ᡢ", $tId);
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);#��ư�Ǥ���ե饰
                        $sFlag2 =(navyUnpack($tLandValue->[$x][$y]), 3)[5];#��ư�Ǥ��ʤ��ե饰
			if((!$sFlag) || ($sFlag2)) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ");
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]), $lv2)[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ");
				return 0;
			}
		}

		my($sx, $sy, $via, $via1, $via2, $viaflag1, $viaflag2, $moveflag);
		if($arg > 6) { # ���ޥ���ư�Σ��ޥ���
		# ��ͳ����Ĵ�٤�
			$sFlag = 0;
			$via1 = int(($arg - 5) / 2);
			$via2 = $via1 + (($arg - 5) % 2);
			$via2 = 1 if($via2 > 6);
			$viaflag1 = random(1); # ���̤�ιԤ���������Х�����ǻ
			$viaflag2 = ($viaflag1 + 1) % 2;
			$via = ($via1, $via2)[$viaflag1];
			$sx = $x + $ax[$via];
			$sy = $y + $ay[$via];
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			$via += 2; # $pre(��԰�ư�ե饰)�ȷ��ѤΤ���+2
			if($tL == $HlandNavy) {
				$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x3);
				if(moveNavy($id, $tIsland, $x, $y, $via)) {# ��ư����
					if($tLand->[$sx][$sy] == $HlandNavy) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# ��ư���˥ȥ�֥롩
					# ���Ѥ����
						logMoveFail($id, $tName, "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# �̥롼�Ȥ�
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# �Ԥˤ�����Ĵ��
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(��԰�ư�ե饰)�ȷ��ѤΤ���
					if(moveNavy($id, $tIsland, $x, $y, $via)) {# ��ư����
						if($tLand->[$sx][$sy] == $HlandNavy) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# ��ư���˥ȥ�֥롩
							logMoveFail($id, $tName, "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#�ɤΥ롼�Ȥ��ư�Ǥ��ʤ�
						logMoveFail($id, $tName,  $point, "��ư���Ǥ��ʤ����ᡢ");
						$HnavyMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			} elsif($tL == $HlandMonster) {
				$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x3);
				if(moveMonster($id, $tIsland, $x, $y, $via, 0)) {# ��ư����
					if($tLand->[$sx][$sy] == $HlandMonster) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# ��ư���˥ȥ�֥롩
						logMoveFail($id, $tName,  "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# �̥롼�Ȥ�
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# �Ԥˤ�����Ĵ��
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(��԰�ư�ե饰)�ȷ��ѤΤ���
					if(moveMonster($id, $tIsland, $x, $y, $via, 0)) {# ��ư����
						if($tLand->[$sx][$sy] == $HlandMonster) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# ��ư���˥ȥ�֥롩
							logMoveFail($id, $tName, "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#�ɤΥ롼�Ȥ��ư�Ǥ��ʤ�
						logMoveFail($id, $tName,  $point, "��ư���Ǥ��ʤ����ᡢ");
						$HmonsterMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			} elsif($tL == $HlandHugeMonster) {
				$sFlag = ($HhugeMonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x3);
				if(moveMonster($id, $tIsland, $x, $y, $via, 1)) {# ��ư����
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$sx][$sy]);
					if(($tLand->[$sx][$sy] == $HlandHugeMonster) && ($mHflag == 0)) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# ��ư���˥ȥ�֥롩
						logMoveFail($id, $tName,  "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# �̥롼�Ȥ�
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# �Ԥˤ�����Ĵ��
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(��԰�ư�ե饰)�ȷ��ѤΤ���
					if(moveMonster($id, $tIsland, $x, $y, $via, 1)) {# ��ư����
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$sx][$sy]);
						if(($tLand->[$sx][$sy] == $HlandHugeMonster) && ($mHflag == 0)) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# ��ư���˥ȥ�֥롩
							logMoveFail($id, $tName, "($sx, $sy)", "�ȥ�֥�ȯ���Τ��ᡢ");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#�ɤΥ롼�Ȥ��ư�Ǥ��ʤ�
						logMoveFail($id, $tName, $point, "��ư���Ǥ��ʤ����ᡢ");
						$HmonsterMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			}
		}

		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		$arg += 2; # $pre(��԰�ư�ե饰)�ȷ��ѤΤ���
		if($tL == $HlandNavy) {
			if($sFlag && moveNavy($id, $tIsland, $x, $y, $arg)) {
				$HnavyMove[$tId][$sx][$sy] = 2;
			} else {
				$HnavyMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "��ư�Ǥ��ʤ����ᡢ");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		} elsif($tL == $HlandMonster) {
			if($sFlag && moveMonster($id, $tIsland, $x, $y, $arg, 0)) {
				$HmonsterMove[$tId][$sx][$sy] = 2;
			} else {
				$HmonsterMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "��ư�Ǥ��ʤ����ᡢ");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		} elsif($tL == $HlandHugeMonster) {
			if($sFlag && moveMonster($id, $tIsland, $x, $y, $arg, 1)) {
				$HmonsterMove[$tId][$sx][$sy] = 2;
			} else {
				$HmonsterMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "��ư�Ǥ��ʤ����ᡢ");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		}
		# ���Ѥ����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $Hcomgoalsetpre) {
                # ��Ū�ϻ���(�о�)

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];

		if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
			logMoveFail($id, $tName, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# ����¾����δ�����оݤˤǤ��ʤ�
			logMoveFail($id, $ntNme, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return 0;
		}

		my $sFlag = 0;
		if(($tL != $HlandNavy) && ($tL != $HlandMonster)) {
			if($tL == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$x][$y]);
				$sFlag = ($HhugeMonsterSpecial[$mKind] & 0x80);
				if(!$sFlag) {
					logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ");
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "�����Ǥʤ����ᡢ");
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		}
                $island->{'setreadyid'} = $tId;
                $island->{'setreadyx'} = $x;
                $island->{'setreadyy'} = $y;
#               $setready = navyUnpack($lv, $lv2); # ��˥ǡ������äƤ���
                logLandSuc($id, $tName, $comName, $point, $tId);
                return $HcomTurn[$kind];

	} elsif($kind == $Hcomgoalset) {
                # ��Ū�ϻ���(��ɸ)
                if(($island->{'setreadyx'} == 31) ||
                   ($island->{'setreadyy'} == 31)){
		        logMoveFail($id, $tName, $point, "�����ν������ʤ��ä����ᡢ", $tId);
                        return 0;
               }

                # ���긵�Υǡ������äƤ���
                my $fId = $island->{'setreadyid'};
                my $fx = $island->{'setreadyx'};
                my $fy = $island->{'setreadyy'};

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

                if($target != $fId){
		        logMoveFail($id, $tName, $point, "�ۤʤ���ؤΰ�ư�ؼ����ä����ᡢ", $tId);
                        return 0;
                }

      		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);
		my($tId) = $tIsland->{'id'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};

                my($fId, $fTmp, $fStat, $fSea, $fExp, $fFlag, $fNo, $fKind, $fWait, $fHp, $goalx, $goaly) = navyUnpack($tLandValue->[$fx][$fy], $tLandValue2->[$fx][$fy]);

                # ��Ū�Ϥ����Ѥ���pack
                ($tLandValue->[$fx][$fy], $tLandValue2->[$fx][$fy]) = navyPack($fId, $fTmp, $fStat, $fSea, $fExp, $fFlag, $fNo, $fKind, $fWait, $fHp, $x, $y);

                logLandSuc($id, $tName, $comName, $point, $tId);
                $island->{'setreadyx'} = 31;
                $island->{'setreadyy'} = 31;
                return 0;
	} elsif($kind == $Hcomremodel) {
                # ��������

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);

		if ($landKind != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $kind, $point);
			return 0;
		}

		if (($nKind != 8) && ($nKind != 9) && ($nKind != 10) && ($nKind != 11)){
                        # �⤷����ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $landName, $point);
			return 0;
                }
		if ($nId != $id) {
			# ¾����δ�����оݤˤǤ��ʤ�
	                logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		if ($nFlag != 0) {
			# �ĳ����ä������夷�Ƥ����¤��Ǥ����
                        logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

                # ����˹������뤫�ɤ���
		if(!(searchNavyPort($tIsland, $x, $y, $an[1], 0, $id))){
                    logNavyNoPort($id, $name, $comName, $point);
                    return 0;
                }

                if($arg > 3){
                    $arg = 3;
                }
                $nkind = $arg + 8;

                ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, 3, $nNo, $nkind, $wait, 13, 31, 31);
                logLandSuc($id, $name, $comName, $point, $tId);

                # ��ư�Ѥߥե饰
                $HnavyMove[$id][$x][$y] == 2;
		return $HcomTurn[$kind];

	} elsif($kind == $Hcomwork) {
                # ���ѥ�����Ÿ��

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];
	        my($tLandName) = landName($tLand->[$x][$y], $tLandValue->[$x][$y]);

                my $area = $tIsland->{'area'};

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);

		if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nKind != 2){
                         # ���ѥ�����������ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
                }
		if ($nId != $id) {
			# ¾����δ�����оݤˤǤ��ʤ�
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nFlag != 0) {
			# �ĳ����ä������夷�Ƥ����¤��Ǥ����
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($area >= $HdisFallBorder) {
			# ���ѥ�����ȥ���
                        logLandFail2($id, $name, $comName, "���Ѥθ³���Ķ����", $point);
			return 0;
		}

                my $shortcut = 0;
                if($arg == 0){
                    $landcount = searchLand($tIsland, $x, $y);
                    if($landcount > 3){
                        $landcount = 3;
                    }
                    $shortcut = $landcount * 3;
                    $nKind = 0;
                }elsif($arg == 1){
                    $landcount = searchLand($tIsland, $x, $y);
                    if($landcount > 3){
                        $landcount = 3;
                    }
                    $shortcut = $landcount * 3;
                    $nKind = 18;
                }elsif($arg == 2){
                    $nKind = 19;
                }else{
                    $nKind = 20;
                }

                ($tLandValue->[$x][$y], $tLandValue2->[$x][$y]) = navyPack($nId, $nTmp, 0, $nSea, 0, 3, $nNo, $nKind, $wait, $shortcut, 31, 31);
                logLandSuc($id, $name, $comName, $point, $tId);

                # ��ư�Ѥߥե饰
                $HnavyMove[$id][$x][$y] == 2;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSellPort) {
                # ����ʧ����

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];
	        my($tLandName) = landName($tLand->[$x][$y], $tLandValue->[$x][$y]);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];

		if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if (!$nSpecial & 0x8) {
			# ���ʳ����оݳ�
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nFlag) {
			# �����Ȥ����Ƥ������
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nId != $id) {
			# ¾�����°�δ�����оݤˤǤ��ʤ�
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		($tLandValue->[$x][$y], $tLandValue2->[$x][$y]) = navyPack(0, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # ��°��ʤ��ˤ���
		logSellPort($id, $tName, $point, $landName);

		$island->{'money'} += 10000;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomBuyPort) {
                # �������

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];
	        my($tLandName) = landName($tLand->[$x][$y], $tLandValue->[$x][$y]);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];

                if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if (!$nSpecial & 0x8) {
			# ���ʳ����оݳ�
                       logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nId != 0) {
			# ��°�����ʳ����оݳ�
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		($tLandValue->[$x][$y], $tLandValue2->[$x][$y]) = navyPack($id, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # ��°��ʤ��ˤ���
		logBuyPort($id, $name, $point, $landName, $tId, $tName);

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomWarpA) {
                # ���������ư(��ư��)

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];

		if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
			logMoveFail($id, $tName, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id) || $HnavyNoMove[$nKind]) {
			# ����¾����δ�����оݤˤǤ��ʤ� ư���ʤ��Ϥδ����
			logMoveFail($id, $ntNme, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return 0;
		}

		if ($nFlag == 3) {
			# �������Ƥ������
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		my $sFlag = 0;
		if(($tL != $HlandNavy) && ($tL != $HlandMonster)) {
			if($tL == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$x][$y]);
				$sFlag = ($HhugeMonsterSpecial[$mKind] & 0x80);
				if(!$sFlag) {
					logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "�����Ǥʤ����ᡢ", $tId);
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "��ĤǤ��ʤ��Ϸ��Τ��ᡢ", $tId);
				return 0;
			}
		}

                my($pcount, $px, $py) = searchNavyPort($tIsland, $x, $y, $an[1], 0, $id);
                if($pcount){
		    # �����򵭲�
		    push(@fleet, {id => $id, tId, => $tId, x => $x, y => $y });
                }else{
			logNavyNoPort($id, $name, $comName, "($x, $y)", $tId);
			return 0;
		}

                $island->{'setreadyid'} = $tId;
                $island->{'setreadyx'} = $x;
                $island->{'setreadyy'} = $y;
                logLandSuc($id, $tName, $comName, $point, $tId);
                return $HcomTurn[$kind];
	} elsif($kind == $HcomWarpB) {
                # ���������ư(��ư��)

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tId) = $tIsland->{'id'};
		my($tName) = islandName($tIsland);
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($tL) = $tLand->[$x][$y];

		if ($tL != $HlandNavy) {
			# ����������ɸ�ˤǤ��ʤ�
			logMoveFail($id, $tName, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return
                }

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if ((!$nSpecial & 0x8) || ($nId != $id)) {
			# ��ʬ�η��������оݤˤǤ��ʤ�
			logMoveFail($id, $ntNme, $point, '��ĤǤ��ʤ��Ϸ��Τ���', $tId);
			return 0;
		}

                my $i;
                for($i = 1; $i <= 6; $i++){
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];

                        # �ϰϳ��ʤ鼡
			if (($sx < 0) || ($sy < 0)) {
				next;
			}

			# ������ʤ��ʤ鼡
			if($tLand->[$sx][$sy] != $HlandSea){
                            next;
                        }

                        while(@fleet){

		            # �����ξ�������
		            ($nId, $tId, $nx, $ny) = ($fleet[0]->{id}, $fleet[0]->{tId}, $fleet[0]->{x}, $fleet[0]->{y});

		            # �������å�(��ư��)����
		            my($nn) = $HidToNumber{$nId};
		            if($nn eq '') {
			        # �������åȤ����Ǥˤʤ�
			        logMsNoTarget($id, $name, $comName);
			        return 0;
		            }
		            my($nIsland) = $Hislands[$nn];
		            my($nId) = $nIsland->{'id'};
		            my($nName) = islandName($tIsland);
		            my($nLand) = $nIsland->{'land'};
		            my($nLandValue) = $nIsland->{'landValue'};
		            my($nLandValue2) = $nIsland->{'landValue2'};
	   	            my($nL) = $nLand->[$nx][$ny];
		            my($nLv) = $nLandValue->[$nx][$ny];
		            my($nLv2) = $nLandValue2->[$nx][$ny];

                            if($nId != id){
                                # ¾�Υץ쥤�䡼�Υǡ������ĤäƤ��ǵͤ��
                                shift @fleet;
                                next;
                            }

		            my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($nLv, $nLv2);
		            # �������ư

			    $tLand->[$sx][$sy] = $nLand->[$nx][$ny];
			    ($tLandValue->[$sx][$sy], $tLandValue2->[$sx][$sy]) = navyPack($nId, $nTmp, $nStat, ($tLand->[$x][$y] == $HlandSea ? $tLv : 0), $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);

			    $nLand->[$nx][$ny] = $HlandSea;
			    $nLandValue->[$nx][$ny] = $nSea; 
                            # ������(���


		            shift @fleet;
                            last;
                        }

                }
                logLandSuc($id, $tName, $comName, $point, $tId);
		return $HcomTurn[$kind];
	} elsif($kind == $HcomMoveMission) {
		# ������Ф�����ɸ�����ؤΰ�ư����
		return if(!$HoceanMode);
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland)    = $Hislands[$tn];
		my($flg, $fNo)  = (int($arg / 10), $arg % 10);
		if($fNo < 1) {
			$fNo = 1;
		} elsif($fNo > 4) {
			$fNo = 4;
		}
		$fNo--;
		my $ofname = $island->{'fleet'}->[$fNo];
		if($flg) {
			undef $island->{'move'}[$fNo];
			logMoveMissionFleetLift($id, $target, $name, islandName($tIsland), $point, $ofname);
		} else {
			if($Hroundmode) {
				my($wx, $wy) = ($island->{'wmap'}->{'x'}, $island->{'wmap'}->{'y'});
				my($tWx, $tWy) = ($tIsland->{'wmap'}->{'x'}, $tIsland->{'wmap'}->{'y'});
				if(abs($tWx - $wx) > $HoceanSizeX/2) {
					$x = ($tWx > $wx) ? $x - ($HoceanSizeX * $HislandSizeX) : $x + ($HoceanSizeX * $HislandSizeX);
				}
				if(abs($tWy - $wy) > $HoceanSizeY/2) {
					$y = ($tWy > $wy) ? $y - ($HoceanSizeY * $HislandSizeY) : $y + ($HoceanSizeY * $HislandSizeY);
				}
			}
			$island->{'move'}[$fNo] = "$x,$y";
			logMoveMissionFleet($id, $target, $name, islandName($tIsland), $point, $ofname);
		}
		# ���Ѥ����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomNavyTarget) {
		# ���ƹ���̿��
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland)    = $Hislands[$tn];
		my($tLand)      = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};
		my($mission) = $island->{"mission,$target,$x,$y"};
		if(defined $mission) {
			logNavyMission($id, $target, $name, islandName($tIsland), $point, landName($tLand->[$x][$y], $tLandValue->[$x][$y]), $mission);
		} else {
			logNavyMissionFail($id, $target, $name, islandName($tIsland), $point, landName($tLand->[$x][$y], $tLandValue->[$x][$y]));
		}
		# ���Ѥ����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomAmity) {
		# ͧ���� ���ꡦ���
		# �������åȼ���
		return if(!$HuseAmity || $HarmisticeTurn || $Htournament);
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		# ��α����Ĵ��
		my(%invade);
		if($HamityDisarm) {
			foreach (@{$island->{'fkind'}}) {
				my($eId, $nFlag, $nKind) = (navyUnpack(hex($_), 0))[0,5,7];
				next if(($HnavySpecial[$nKind] & 0x8) || ($nFlag == 1)); # �������ĳ��Ͻ���
                                next if($HnavyNoMove[$nKind]); # ư���ʤ��Ϥ����  
				if(($eId != $id) && (defined $HidToNumber{$eId})) {
					$invade{$eId}++;
				}
			}
		}
		my $amity = $island->{'amity'};
		my @newamity = ();
		my $ami;
		if($target == $id) {
			if($$amity[0] eq '') {
				if(!$HamityMax || $islandNumber < $HamityMax) {
					my $i;
					foreach $i (0..$islandNumber) {
						next if($Hislands[$i]->{'id'} == $id);
						push(@newamity, $Hislands[$i]->{'id'});
					}
					logAmity($id, $name, $target, "���٤Ƥ�${AfterName}");
				} else {
					logAmityMaxOver($id, $name, "���٤Ƥ�${AfterName}");
				}
			} else {
				@newamity = keys %invade;
				my($str);
				$str = '�����ɸ���Ǥʤ�' if($HamityDisarm);
				logAmityEnd($id, $name, $target, "ͧ����Ǥ��ä����٤Ƥ�${str}${AfterName}");
			}
			$island->{'amity'} = \@newamity;
			# ���Ѥ����
			$island->{'money'} -= $cost;
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);
		my $flag = 0;
		foreach $ami (@$amity) {
			if(!(defined $HidToNumber{$ami})) {
			} elsif($ami == $target) {
				$flag = 1;
			} else {
				push(@newamity, $ami);
			}
		}
		my $amiNum = @newamity;
		if($flag) {
			if($HamityDisarm && $invade{$target}) {
				push(@newamity, $target);
				logAmityEndFail($id, $name, $target, $tName);
			} else {
				logAmityEnd($id, $name, $target, $tName);
			}
		} else {
			if(!$HamityMax || $amiNum < $HamityMax) {
				push(@newamity, $target);
				logAmity($id, $name, $target, $tName);
			} else {
				logAmityMaxOver($id, $name, $tName);
			}
		}
		$island->{'amity'} = \@newamity;

		# ���Ѥ����
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomAlly) {
		# Ʊ�� ������æ��
		# �������åȼ���
		return if(!$HallyUse || !$HallyJoinComUse || $HarmisticeTurn || $Htournament);
		my($tn) = $HidToNumber{$target};
		my($tan) = $HidToAllyNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		} elsif($tan eq '') {
			$tan = $HidToAllyNumber{$Hislands[$tn]->{'allyId'}[0]};
		}
		if($tan eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		my $tName = islandName($Hislands[$tn]);
		if(defined $HidToAllyNumber{$id}) {
			logLeaderAlready($id, $name, $tName, $comName);
			return;
		}
		my $ally = $Hally[$tan];
		if($HallyJoinOne && ($island->{'allyId'}[0] ne '') && ($island->{'allyId'}[0] != $ally->{'id'})) {
			logOtherAlready($id, $target, islandName($island), $ally->{'name'});
			return;
		}
		my(%vetoID);
		foreach(@{$ally->{'vetoId'}}) {
			$vetoID{$_} = 1;
		}
		if((!$ally->{'vkind'} && $vetoID{$id}) || ($ally->{'vkind'} && !$vetoID{$id})) {
			logAllyVeto($id, $target, islandName($island), $ally->{'name'});
			return;
		}
		my $allyMember = $ally->{'memberId'};
		my @newAllyMember = ();
		my $flag = 0;
		foreach (@$allyMember) {
			if(!(defined $HidToNumber{$_})) {
			} elsif($_ == $id) {
				$flag = 1;
			} else {
				push(@newAllyMember, $_);
			}
		}
		my $allyNum = @newAllyMember;
		if($flag) {
			logAllyEnd($id, $target, islandName($island), $ally->{'name'});
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
				logAlly($id, $target, islandName($island), $ally->{'name'});
				push(@newAllyMember, $id);
				push(@{$island->{'allyId'}}, $ally->{'id'});
				$ally->{'score'} += $island->{$HrankKind} if(!$island->{'predelete'});
				$ally->{'number'}++;
			} else {
				# ����
				logAllyMaxOver($id, $target, islandName($island), $ally->{'name'});
				return;
			}
		}
		$ally->{'memberId'} = \@newAllyMember;
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomDeWar) || ($kind == $HcomCeasefire)) {
		# �����۹�����
		# �������åȼ���
		return if(!$HuseDeWar || $HarmisticeTurn || $HsurvivalTurn || $Htournament);
		return 0 if($target == $id);
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);
		# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��
		if (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
			($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
			logDevelopTurnFail($id, $name, $comName);
			return 0;
		} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
			logLandNG($id, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
			return 0;
		} elsif($HnofleetNotAvail) {
			if(!$tIsland->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "�������ͭ���ʤ�$AfterName�Ǥ��ä�����");
				return 0;
			} elsif(!$island->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "�������ͭ���Ƥ��ʤ�����");
				return 0;
			}
		}
		$name = "${HtagName_}${name}${H_tagName}";
		$tName = "${HtagName_}${tName}${H_tagName}";
		my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
		# ͧ����
		my(%amityFlag);
		my($amity) = $island->{'amity'};
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
		if(chkWarIsland($id, $target)){
			# ������
			for($i=0;$i < $#HwarIsland;$i+=4){
				my($id1, $id2) = ($HwarIsland[$i+1], $HwarIsland[$i+2]);
				my($tn1) = $HidToNumber{$id1};
				next if($tn1 eq '');
				my($tn2) = $HidToNumber{$id2};
				next if($tn2 eq '');
				my $turn = $HwarIsland[$i];
				if(($id1 == $id) && ($id2 == $target)){
					# �����ģ�(�����۹𤷤�¦)
					if($kind == $HcomDeWar){
						if($HwarIsland[$i+3] % 10 == 1){
							$HwarIsland[$i+3] = 0;
							logOut("${name}��${tName}���ǿǤ��Ƥ��������ű�������³���̹𤷤ޤ�����",$id, $target);
						} elsif($HwarIsland[$i+3] % 10 == 2){
							$HwarIsland[$i+3] = 0;
							logOut("${name}��${tName}����������Ĥ��˴��������³���̹𤷤ޤ�����",$id, $target);
						}
					} elsif($HwarIsland[$i+3] % 10 == 2){
						# �������
						if($HwarIsland[$i] > $HislandTurn){
							# �����������
							logOut("${name}��${tName}������ϲ��򤵤�ޤ�����",$id, $target);
						} else {
							# ��������
							if($HceasefireAutoNavyReturn) {
								islandCeasefire($Hislands[$tn1], $id2);
								islandCeasefire($Hislands[$tn2], $id1);
							}
							logOut("${name}��${tName}�������դˤ��<B>������${turn}</B>����³��������Ͻ��뤷�ޤ�����",$id, $target);
							logHistory("${HtagName_}${wname}${H_tagName}����(������${turn}��${HislandTurn})�Ͻ��뤷�ޤ�����");
						}
						splice(@HwarIsland,$i,4);
					} else {
						# ����Ԥ�
						$HwarIsland[$i+3] = $HislandTurn * 10 + 1;
						logOut("${name}��${tName}��<b>����ΰջ�</b>���ǿǤ��ޤ�����",$id, $target);
					}
					last;
				} elsif(($id1 == $target) && ($id2 == $id)) {
					# �����ģ�
					if($kind == $HcomDeWar) {
						if($HwarIsland[$i+3] % 10 == 2){
							$HwarIsland[$i+3] = 0;
							logOut("${name}��${tName}���ǿǤ��Ƥ��������ű�������³���̹𤷤ޤ�����",$id, $target);
						} elsif($HwarIsland[$i+3] % 10 == 1){
							$HwarIsland[$i+3] = 0;
							logOut("${name}��${tName}����������Ĥ��˴��������³���̹𤷤ޤ�����",$id, $target);
						}
					} elsif($HwarIsland[$i+3] % 10 == 1) {
						# �������
						if($HwarIsland[$i] > $HislandTurn){
							# �����������
							logOut("${name}��${tName}������ϲ��򤵤�ޤ�����",$id, $target);
						}else{
							# ��������
							if($HceasefireAutoNavyReturn) {
								islandCeasefire($Hislands[$tn1], $id2);
								islandCeasefire($Hislands[$tn2], $id1);
							}
							logOut("${name}��${tName}�������դˤ��<B>������${turn}</B>����³��������Ͻ��뤷�ޤ�����",$id, $target);
							logHistory("${HtagName_}${wname}${H_tagName}����(������${turn}��${HislandTurn})�Ͻ��뤷�ޤ�����");
						}
						splice(@HwarIsland,$i,4);
					} else {
						# ����Ԥ�
						$HwarIsland[$i+3] = $HislandTurn * 10 + 2;
						logOut("${name}��${tName}��<B>����ΰջ�</B>���ǿǤ��ޤ�����",$id, $target);
					}
					last;
				}
			}
		} elsif($kind == $HcomCeasefire) {
			# �����̵��
			return 0;
		} else {
			# �����۹�
			if($amityFlag{$target}){
				logOut("${name}����$tName�ؤ�${HtagComName_}$comName${H_tagComName}�ϡ�$tName��<B>ͧ����Τ���</B>����ߤ��ޤ�����",$id);
				return 0;
			}
			if($HmatchPlay) { # �����ޥ�⡼��
				my $oId = chkWarIslandOR($id, $target);
				if($oId) {
					my $oName = islandName($Hislands[$HidToNumber{$oId}]);
					$oName = "${HtagName_}${oName}${H_tagName}";
					$otName = (chkWarIslandOR($id, $id)) ? $name : $tName;
					logOut("${name}����$tName�ؤ�${HtagComName_}$comName${H_tagComName}�ϡ�$otName��$oName��<B>������Τ���</B>����ߤ��ޤ�����",$id);
					return 0;
				}
			}
		#	$arg = ($arg < $HdeclareTurn) ? $HislandTurn + $HdeclareTurn : $HislandTurn + $arg;
			$arg = $HislandTurn + $HdeclareTurn;
			push(@HwarIsland, ($arg, $id, $target, 0));
			if($HdeclareTurn > 0) {
				logOut("${name}��${tName}��${HtagDisaster_}�����۹𡪡�${H_tagDisaster}(<B>${arg}������˳���</B>)",$id, $target);
			} else {
				my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
				logOut("${name}��${tName}��${HtagDisaster_}�����۹𡪡�${H_tagDisaster}${wname}������ȯ����",$id, $target);
				logHistory("${wname}������ȯ����");
			}
		}

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];


	} elsif($kind == $HcomSell) {
		# ͢���̷���
		$arg = 1 if(!$arg);
		my($value) = min($arg * (-$HcomCost[$kind]), $island->{'food'});
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / ($island->{'food'}/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }

		# ͢�Х�
		logSell($id, $name, $comName, $value);
		$island->{'food'}  -=  int($value);
		$island->{'money'} += int($value * $foodrate / 400);
		return $HcomTurn[$kind];

	} elsif($kind == $HcomBuy) {
		# ͢���̷���
		$arg = 1 if(!$arg);
		my($value) = min($arg * $HcomCost[$kind], $island->{'money'});
		$value *= 10;
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / ($island->{'food'}/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }

		# ͢����
		logBuy($id, $name, $comName, $value);
		$island->{'food'}  +=  int($value / $foodrate * 10 / 4);
		$island->{'money'} -= int($value/ 10);
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomFood) || ($kind == $HcomMoney)) {
		# �����

		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);

		my(%amityFlag);
		my($amity) = $island->{'amity'};
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
		# ¾�οرĤˤϱ���Ǥ��ʤ�
		if ($HarmisticeTurn && $HcampAidOnly && !$amityFlag{$target}) {
			logAidFail($id, $target, $name, $tName, $comName);
			return 0;
		}
		# ��ȯ���֤ʤ饳�ޥ�ɤ�̵��
		if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) {
			logDevelopTurnFail($id, $name, $comName);
			return 0;
		}

		# �ǰ�ǽ�ϤΤ���������ɸ�����Ƥ��ʤ���ؤϱ�����ޥ�ɤ��Ĥ����ʤ�
		if ($HtradeAbility) {
			my $tradeFlag = 1;
			my($fkind) = $island->{'fkind'};
			my @flist = @$fkind;
			foreach (@flist) {
				my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack(hex($_), 0);
				my $special = $HnavySpecial[$nKind];
				next if ($special & 0x8); # �����Ͻ���
				if(($eId == $target) && ($special & 0x20000)) {
					$tradeFlag = 0;
					last;
				}
			}
			if($tradeFlag) {
				logTradeFail($id, $name, $comName);
				return 0;
			}
		}

		# ����̷���
		$arg = 1 if(!$arg);

		my($value, $str);
		if($HcomCost[$kind] < 0) {
			$value = min($arg * (-$HcomCost[$kind]), $island->{'food'});
			$str = "${HtagFood_}$value$HunitFood${H_tagFood}";
		} else {
			$value = min($arg * $HcomCost[$kind], $island->{'money'});
			$str = "${HtagMoney_}$value$HunitMoney${H_tagMoney}";
		}

		# �����
		logAid($id, $target, $name, $tName, $comName, $str);

		if($HcomCost[$kind] < 0) {
			$island->{'food'} -= $value;
			$tIsland->{'food'} += $value * 0.8;
			$island->{'ext'}[1] += int($value/10); # �׸���
			$tIsland->{'ext'}[1] -= int($value/10); # �׸���
			#$tIsland->{'ext'}[1] = 0 if($tIsland->{'ext'}[1] < 0);
		} else {
			$island->{'money'} -= $value;
			$tIsland->{'money'} += $value * 0.8;
			$island->{'ext'}[1] += $value; # �׸���
			$tIsland->{'ext'}[1] -= $value; # �׸���
			#$tIsland->{'ext'}[1] = 0 if($tIsland->{'ext'}[1] < 0);
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomPropaganda) {
		# Ͷ�׳�ư
		logPropaganda($id, $name, $comName);
		$island->{'propaganda'} = 1;
		$island->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if($arg > 1) {
			$arg--;
			slideBack($comArray, 0);
			$comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg,
				'target2' => $target2
			};
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomGiveup) {
		# ����
		logGiveup($id, $name);
		$island->{'dead'} = 1;
		if($island->{'field'}) {
			$island->{'field'} = 0;
			$HbfieldNumber--;
		}
		return $HcomTurn[$kind];
	}
	return 1;
}

sub moveFleet {
	my($island, $fIsland, $tIsland, $no) = @_;

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($name)      = islandName($island);

	my($fId)        = $fIsland->{'id'};
	my($fLand)      = $fIsland->{'land'};
	my($fLandValue) = $fIsland->{'landValue'};
	my($fLandValue2) = $fIsland->{'landValue2'};
	my($fName)      = islandName($fIsland);

	my($tId)        = $tIsland->{'id'};
	my($tLand)      = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tLandValue2) = $tIsland->{'landValue2'};
	my($tName)      = islandName($tIsland);
	my(%amityFlag);
	if($HmineSelfDamage) {
		$amityFlag{$tId} = 1;
		if($HmineSelfDamage == 2) {
			foreach (@{$tIsland->{'amity'}}) {
				$amityFlag{$_} = 1;
			}
		}
	}
	# ���٥��ȯ����ؤ��ɸ�
	my($kNew, %kindFlag, $eMax);
	if(($id != $tId) && $tIsland->{'event'}[0] && ($tIsland->{'event'}[1] <= $HislandTurn)) {
		$kNew = ($tIsland->{'event'}[4] & (2 ** 0));
		foreach (1..$#HnavyName) {
			$kindFlag{$_} = 1 unless($tIsland->{'event'}[4] & (2 ** $_));
		}
		if($tIsland->{'event'}[3]) {
			$eMax = $tIsland->{'event'}[3] - $island->{"invade$tId"};
		}
	}
	# ����򸡺�
	my(@fleet);
	my($i, $x, $y, $fLv, $fLv2);
	my $fSend = ($fId == $tId) ? '�ǰ�ư' : ($id == $tId) ? '���鵢��' : '���ɸ�';
	my $fSname = ($fId == $tId) ? $tName : ($id == $tId) ? $fName : $tName;
	foreach $i (0..$fIsland->{'pnum'}) {
		$x = $fIsland->{'rpx'}[$i];
		$y = $fIsland->{'rpy'}[$i];
		$fLv = $fLandValue->[$x][$y];
		$fLv2 = $fLandValue2->[$x][$y];

		# ������õ��
		next unless ($fLand->[$x][$y] == $HlandNavy);

		# ��ư��������
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($fLv, $fLv2);
		next if (($nId != $id) || ($nNo != $no) || ($nFlag == 3));

		# ���ʤ�̵��
		my $nSpecial = $HnavySpecial[$nKind];
		next if ($nSpecial & 0x8);

                # ư���ʤ��Ϥδ����̵��
                next if($HnavyNoMove[$nKind]);

		# ���٥��ȯ������ɸ���ǽ����Ƚ��
		next if ($kindFlag{$nKind} || ($kNew && $nExp));

                
                # ̱�����ʳ��δ���������Ȥ��Ƥ��ơ������ɸ����ݥե饰������ʾ��
                if($Hprivate[$nKind] != 1){
                    if($moveErrorFlag == 1){
		        logLandNG($id, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
		        return 0;
                    }
                }

		# �����򵭲�
		push(@fleet, { x => $x, y => $y });

		# ���٥��ȯ������ɸ���ǽ������Ƚ��
		last if(--$eMax == 0);
	}

	$i = $#fleet + 1;
	my $ofname = $Hislands[$HidToNumber{$id}]->{'fleet'}->[$no];
	if(($id != $fId) && ($id != $tId)) {
		$no = "${HtagName_}${fName}${H_tagName}���ɸ����$ofname����";
	} else {
		$no = "$ofname����";
	}
	if ($i < 1) {
		# ����ʤ�
		logNavySendNone($id, $name, $tName, $no, $fSend);
		return 0;
	}

	# �����ư
	my $sendshipStr = '';
	my($tx, $ty, $tLv);
	foreach $i (0..$tIsland->{'pnum'}) {
		$tx = $tIsland->{'rpx'}[$i];
		$ty = $tIsland->{'rpy'}[$i];
		$tLv = $tLandValue->[$tx][$ty];
		$tLv2 = $tLandValue2->[$tx][$ty];

		# �������������õ��
		next unless ( (($tLand->[$tx][$ty] == $HlandSea) && (!$tLv || $HnavyMoveAsase)) ||
						(!$amityFlag{$id} && ($tLand->[$tx][$ty] == $HlandSeaMine)) );

		# �����ξ�������
		($x, $y) = ($fleet[0]->{x}, $fleet[0]->{y});
		$fLv = $fLandValue->[$x][$y];
		$fLv2 = $fLandValue2->[$x][$y];
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($fLv, $fLv2);

                # ��ɸ�����Υꥻ�åȤȹ�³�������Ⱦ��������Ԥ�
                $goalx = 31;
                $goaly = 31;
                if($HnavyCruiseTurn[$nKind] != 0){
                    $wait = int($wait/2);
                }

		# �������ư
		if($tLand->[$tx][$ty] == $HlandSeaMine) {
			# ����ε���ǥ��᡼��������뤫�ɤ���(ǰ�Τ���)
			next if($amityFlag{$nId});
			# ����ʤ��ѵ��ϸ���
			$nHp -= $tLandValue->[$tx][$ty];
			# ������
			my $nName = landName($fLand->[$x][$y], $fLv);
			if($nHp > 0) {
				logSeaMineDamage($tId, $tName, $nId, "($tx, $ty)", $nName);
			} else {
				logSeaMineDestroy($tId, $tName, $nId, "($tx, $ty)", $nName);
			}
		}

		if($nHp > 0) {
			$tLand->[$tx][$ty] = $fLand->[$x][$y];
			($tLandValue->[$tx][$ty], $tLandValue2->[$tx][$ty]) = navyPack($nId, $nTmp, $nStat, ($tLand->[$tx][$ty] == $HlandSea ? $tLv : 0), $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
		} elsif($nHp == 0) {
			# �ĳ��ˤʤ�
			$tLand->[$tx][$ty] = $fLand->[$x][$y];
			($tLandValue->[$tx][$ty], $tLandValue2->[$tx][$ty]) = navyPack(0, $nTmp, $nStat, ($tLand->[$tx][$ty] == $HlandSea ? $tLv : 0), int(rand(90)) + 10, 1, 0, $nKind, 0, 0, 31, 31);
			$island->{'shipk'}[$nKind]--;
			$island->{'ships'}[$nNo]--;
			$island->{'ships'}[4]--;
			# ���Х��Х�
			$island->{'epoint'}{$tId} = $HislandTurn if($tIsland->{'event'}[6] == 1);
		} else {
			# ����
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
			$island->{'shipk'}[$nKind]--;
			$island->{'ships'}[$nNo]--;
			$island->{'ships'}[4]--;
			# ���Х��Х�
			$island->{'epoint'}{$tId} = $HislandTurn if($tIsland->{'event'}[6] == 1);

		}
		$fLand->[$x][$y] = $HlandSea;
		$fLandValue->[$x][$y] = $nSea;
		$HlandMove[$fId][$x][$y] = 1;
		$HnavyAttackTarget{"$id,$x,$y"} = undef;

		# ��ư�Ѥߤˤ���
		$HnavyMove[$tId][$tx][$ty] = 2;
		$island->{'ext'}[8]++;
		$tIsland->{'ext'}[9]++;
		if($HallyNumber) {
			foreach (@{$island->{'allyId'}}) {
				$Hally[$HidToAllyNumber{$_}]->{'ext'}[3]++;
			}
			foreach (@{$tIsland->{'allyId'}}) {
				$Hally[$HidToAllyNumber{$_}]->{'ext'}[4]++;
			}
		}
		# ����Ф�
		$sendshipStr .= " <B>$HnavyName[$nKind]</B>${HtagName_}($tx, $ty)${H_tagName}";
		shift @fleet;
		last if(!@fleet);
	}
	my $restshipStr = '<BR>��--- ��α���� �� ';
	if(@fleet > 0) {
		my(%restShip);
		foreach (@fleet) {
			# �����ξ�������
			($x, $y) = ($_->{x}, $_->{y});
			$fLv = $fLandValue->[$x][$y];
			$fLv2 = $fLandValue2->[$x][$y];
			my($nKind) = (navyUnpack($fLv, $fLv2))[7];
			$restShip{$nKind}++;
		}
		foreach (keys %restShip) {
			$restshipStr .= " <B>$HnavyName[$_]</B>${HtagName_}($restShip{$_}��)${H_tagName}"
		}
	}
	if($sendshipStr eq '') {
		# Ÿ�����ꥢ�ʤ�
		logNavySendNoArea($id, $name, $tName, $no, $fSend, $restshipStr);
	} elsif(@fleet > 0) {
		# Ÿ�����ꥢ��­
		$sendshipStr .= $restshipStr;
		$island->{'epoint'}{$tId} = 0 if($tIsland->{'event'}[0]);
		logNavySendShip($id, $tId, $sendshipStr, substr($fSend, -4));
		logNavySend($id, $fId, $tId, $name, $fSname, $no, $fSend);
	} else {
		# Ÿ������
		$island->{'epoint'}{$tId} = 0 if($tIsland->{'event'}[0] && !(defined $island->{'epoint'}{$tId}));
		logNavySendShip($id, $tId, $sendshipStr, substr($fSend, -4));
		logNavySend($id, $fId, $tId, $name, $fSname, $no, $fSend);
	}
	return 1;
}

# ���������줿���δ������
sub islandDeadNavy {
	my($island) = @_;

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($name)      = islandName($island);

	# �ɸ�����Ƥ�����⤬���뤫Ĵ�٤�
	my(%fleet, $i, $n, $x, $y, $lv);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];

		if($HautoKeeper) {
			# ���äȵ�����ä򳤤ˤ���
			if(($land->[$x][$y] == $HlandMonster) || ($land->[$x][$y] == $HlandHugeMonster)) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if ($mFlag & 2) {
					$land->[$x][$y] = $HlandSea;
					$landValue->[$x][$y] = $mSea;
				} else {
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
				next;
			}
		}

		# ������õ��
		next unless ($land->[$x][$y] == $HlandNavy);

		# ����δ�����̵��°�δ�����̵��
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$n = $HidToNumber{$nId};
		if ($nId == $id) {
			# ����δ�����̵��
			$island->{'stayNavyExp'} += $nExp if($HmatchPlay > 3);
			next;
		} elsif(!(defined $n) || !$nId) {
			# ���Ǥ���������Ƥ�����δ�����̵��°�δ���
			if($HautoKeeper) {
				# ���ˤ���
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = $nSea;
				$HnavyAttackTarget{"$id,$x,$y"} = undef;
			} else {
				# ̵��
				next;
			}
			next;
		}

		# �������򵭲�
		$fleet{$n}[$nNo]++;
		$Hislands[$n]->{'sendNavyExp'} += $nExp if($HmatchPlay > 3);
	}

	# �ɸ�����Ƥ������򵢴Ԥ�����
	foreach $n (keys %fleet) {
		foreach $i (0..3) {
			next unless ($fleet{$n}[$i]);
			moveFleet($Hislands[$n], $island, $Hislands[$n], $i);
		}
	}

	# ͧ������
	if($HuseAmity && !$HautoKeeper) {
		foreach $i (0..$islandNumber) {
			my @newamity = ();
			foreach (@{$Hislands[$i]->{'amity'}}) {
				next if(($_ eq $id) || !(defined $HidToNumber{$_}));
				push(@newamity, $_);
			}
			$Hislands[$i]->{'amity'} = \@newamity;
		}
	}
	# ������ֲ��
	if(chkWarIslandOR($id, $id)) {
		for($i=0;$i < $#HwarIsland;$i+=4){
			my($wid1) = $HwarIsland[$i+1];
			my($wid2) = $HwarIsland[$i+2];
			my($tn1) = $HidToNumber{$wid1};
			my($tn2) = $HidToNumber{$wid2};
			if(($wid1 == $id) || ($wid2 == $id) || ($tn1 eq '') || ($tn2 eq '')){
				splice(@HwarIsland,$i,4);
				$i -= 4;
			}
		}
	}
	# �ɸ��������ɸ����äν����ե饰
	$HautoKeepID{$id} = 1 if($HautoKeeper || $island->{'delete'});
	# Ʊ��score����
	islandDeadAlly($island) if($HallyNumber);
}

# �����դξ��δ������($island���ɸ����줿$tId�δ����򵢴Ԥ�����)
sub islandCeasefire {
	my($island, $tId) = @_;

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# �ɸ�����Ƥ�����⤬���뤫Ĵ�٤�
	my(%fleet, $i, $x, $y, $lv);
	my $t = $HidToNumber{$tId};
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];
		# ������õ��
		next unless ($land->[$x][$y] == $HlandNavy);
		# ����δ�����̵��°�δ�����̵��
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		if ($nId == $id) {
			# ����δ�����̵��
			$island->{'stayNavyExp'} += $nExp if($HmatchPlay > 3);
		} elsif($nId == $tId) {
			# �������򵭲�
			$fleet{$nNo}++;
			$Hislands[$t]->{'sendNavyExp'} += $nExp if($HmatchPlay > 3);
		}
	}
	# �ɸ�����Ƥ������򵢴Ԥ�����
	foreach $i (keys %fleet) {
		moveFleet($Hislands[$t], $island, $Hislands[$t], $i);
	}
}

# ���٥�Ȼ��δ�������å�
sub islandEventNavy {
	my($island, $type) = @_;

	# ������ǡ��������Ǥˤ�붯����λ���꤬�ʤ������ޤ��ϡ�����������
	my($continueflag) = (($island->{'event'}[2] && ($island->{'event'}[1] + $island->{'event'}[2] > $HislandTurn)) && (!$island->{'event'}[23] || $island->{'core'})) ? 1 : 0;
	# �ɲ��ɸ��������硤�������Ƚ�ꤷ�ʤ�(�������Ǥˤ�붯����λ���꤬�ʤ������ޤ��ϡ������������)
	return 0 if(!$HeventLog && $island->{'event'}[11] && $continueflag);

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# �ɸ�����Ƥ�����⤬���뤫Ĵ�٤�
	my(%epoint, $x, $y, $n, %fleet, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my $lv = $landValue->[$x][$y];
		my $lv2 = $landValue2->[$x][$y];
		# ������õ��
		next if ($land->[$x][$y] != $HlandNavy);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$n = $HidToNumber{$nId};
		my $special = $HnavySpecial[$nKind];
		# �����ĳ������Ǥ���������Ƥ�����δ�����̵��°�δ���
		next if (!(defined $n) || !$nId || ($special & 0x8) || ($nFlag == 1));
		# �������򵭲�
		$fleet{$n}[$nNo]++;
	}
	foreach (keys %fleet) {
		# epoint
		$epoint{$Hislands[$_]->{'id'}} = $Hislands[$_]->{'epoint'}{$id};
	}
	# ����Ƚ��
	my(@winnertmp, @winner, $wno);
	@winnertmp = sort { $epoint{$b} <=> $epoint{$a} } keys %epoint;
	foreach (@winnertmp) {
		next if($Hislands[$HidToNumber{$_}]->{'dead'} || $Hislands[$HidToNumber{$_}]->{'delete'} || $Hislands[$HidToNumber{$_}]->{'predelete'});
		push(@winner, $_);
	}
	$wno = @winner;
	if(!$wno) {
		return -1;
	} elsif(($type == 1) && ($wno != 1)) {
		# ���Х��Х�
		return 0;
	} elsif(!$HeventLog && ($type != 1) && ($wno != 1) && ($epoint{$winner[0]} == $epoint{$winner[1]})) {
		# �����и��ͳ���, ��������, �����༣, �޶�Ԥ�
		return 0 if((!$island->{'event'}[23] || $island->{'core'}));
	}
	# ����������Τǡ��������Ƚ�ꤷ�ʤ�(�������Ǥˤ�붯����λ���꤬�ʤ������ޤ��ϡ������������)
	my $eventLog = 0;
	if($continueflag |= (($type != 1) && ($wno != 1) && ($epoint{$winner[0]} == $epoint{$winner[1]}))) {
		if(!$HeventLog) {
			return 0;
		} elsif($type != 1) {
			$eventLog = 1;
		}
	}
	if($type == 1) {
		my(%lpoint);
		foreach (0..$islandNumber) {
			next if($Hislands[$_]->{'dead'} || $Hislands[$_]->{'delete'} || $Hislands[$_]->{'predelete'});
			$lpoint{$Hislands[$_]->{'id'}} = $Hislands[$_]->{'epoint'}{$id} if($Hislands[$_]->{'epoint'}{$id});
		}
		$lpoint{$winner[0]} = $HislandTurn + 1;
		my @loser = sort { $lpoint{$b} <=> $lpoint{$a} } keys %lpoint;
		%epoint = %lpoint;
		@winner = @loser;
	}
	my $detail = '';
	my $dcount = ($epoint{$winner[0]} == $epoint{$winner[1]}) ? 1 : 0;
	foreach (0..$#winner) {
		my $lIsland =$Hislands[$HidToNumber{$winner[$_]}];
		my $lName =islandName($lIsland);
		$dcount = $_ + 1 if(($_ < 1) || (!$eventLog && ($_ < 3)) || ($epoint{$winner[$_]} != $epoint{$winner[($_-1)]}));
		if(!$eventLog) {
			if($dcount == 1) {
				$detail .= "<BR>��--- <B>ͥ����</B>";
			} elsif($dcount == 2) {
				$detail .= "<BR>��--- <B>��ͥ����</B>";
			} else {
				$detail .= "<BR>��--- <B>��$dcount�̡�</B>";
			}
		} else {
			$detail .= "<BR>��--- <B>��$dcount�̡�</B>";
		}
		$detail .= "${HtagName_}${lName}${H_tagName}";
		if($type == 1) {
			$detail .= "(������${HtagNumber_}" . int($epoint{$winner[$_]}) ."${H_tagNumber})" if($_);
		} elsif($type == 5) {
			$detail .= '(' . int($epoint{$winner[$_]}) . $HunitMoney . ')';
		} else {
			$detail .= '(' . int($epoint{$winner[$_]}) .'��)';
		}
	}
	my $typeName  = $HeventName[$island->{'event'}[6]];
	my $name = islandName($island);
	# ������Υ�����
	if($eventLog) {
		logOut("${HtagDisaster_}$typeName${H_tagDisaster}(������${HtagNumber_}$island->{'event'}[1]${H_tagNumber}��������${HtagName_}${name}${H_tagName})<B>�в����</B>$detail", $id);
		return 0 if($continueflag);
	}
	my $tIsland = $Hislands[$HidToNumber{$winner[0]}];
	my $tName = islandName($tIsland);
	# ���
	my $money  = $island->{'event'}[7];
	my $food  = $island->{'event'}[8];
	my $present  = $island->{'event'}[9];
	my @item  = split(' *', $island->{'event'}[10]);
	my($prize);
	if($money) {
		$prize = "$money$HunitMoney";
		$tIsland->{'money'} += $money;
		$tIsland->{'prizemoney'} += $money;
	}
	if($food) {
		$prize .= " + " if($money);
		$prize .= "$food$HunitFood";
		$tIsland->{'food'} += $food;
	}
	if($present) {
		$prize .= " + " if($money || $food);
		$prize .= "�����ͥץ쥼���";
	}
	if($island->{'event'}[10]) {
		$prize .= " + " if($money || $food || $present);
		my(%newItem);
		foreach (@{$tIsland->{'item'}}) {
			$newItem{$_} = 1;
		}
		foreach (1..$#HitemName) {
			if($item[$_]) {
				$prize .= "<span class=\"check\"><img src=\"${HimageDir}/$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>";
				$newItem{$_} = 1;
			}
		}
		my @newi = keys %newItem;
		$tIsland->{'item'} = \@newi;
	}
	$prize = '�ʤ�' if($prize eq '');
	my($coreless);
	$coreless = "(${HtagDisaster_}$HlandName[$HlandCore][0]���Ǥˤ�붯����λ${H_tagDisaster})" if(($island->{'event'}[2] && ($island->{'event'}[1] + $island->{'event'}[2] > $HislandTurn)) && $island->{'event'}[23] && !$island->{'core'});
	logOut("${HtagName_}${name}${H_tagName}�ǥ�����${HtagNumber_}$island->{'event'}[1]${H_tagNumber}���鳫�Ť���Ƥ���${HtagDisaster_}$typeName${H_tagDisaster}��${HtagName_}${tName}${H_tagName}��<B>����</B>���ޤ�����$coreless(���:<B>$prize</B>)$detail", $id, $winner[0]);

	# ��ư���Խ���
	if($island->{'event'}[18]) {
		foreach $n (keys %fleet) {
			foreach $i (0..3) {
				next unless ($fleet{$n}[$i]);
				moveFleet($Hislands[$n], $island, $Hislands[$n], $i);
			}
		}
	}

	return $winner[0];

}

# ��Խ���
sub doPreEachHex {
	my($island) = @_;

	# Ƴ����
	my($name) = islandName($island);
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# �롼��
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv)       = $landValue->[$x][$y];
		my($lv2)      = $landValue2->[$x][$y];

		if($landKind == $HlandMonster) {
			# ����
			moveMonster(0, $island, $x, $y, 1, 0);
		} elsif($landKind == $HlandHugeMonster) {
			# �������
			my($mHflag) = (monsterUnpack($lv))[1];
			moveMonster(0, $island, $x, $y, 1, 1) if(!$mHflag);
		} elsif ($landKind == $HlandNavy) {
			# ����
			my($nStat) = (navyUnpack($lv, $lv2))[2];
			moveNavy(0, $island, $x, $y, 1) if($nStat < 3);
		}
	}
}

# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
	my($island) = @_;
	# Ƴ����
	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# ������͸��Υ�����
	my(@addpop)  = @Haddpop;

	if($Htournament && ($HislandTurn <= $HyosenTurn)) { # �ȡ��ʥ���
		# Ϣ³��ⷫ�꤫����������­��ʤ���祹�ȥå�
		@addpop = (0) x @Haddpop if(($island->{'absent'} >= $HstopAddPop) || $island->{'down'});
	} elsif($HsurvivalTurn) { # ���Х��Х�
		if($HislandTurn <= $HsurvivalTurn){
			@addpop = @HaddpopSD;# ��ȯ����
		} else {
			@addpop = @HaddpopSA; # ��Ʈ����
		}
	}
	if($island->{'food'} < 0) {
		# ������­
		@addpop = @HreductionPop;
	} elsif($island->{'propaganda'} == 1) {
		# Ͷ�׳�ư��
		@addpop = (!$HsurvivalTurn) ? @HaddpopPropa : ($HislandTurn <= $HsurvivalTurn) ? @HaddpopSDpropa : @HaddpopSApropa;
	}

	# �롼��
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];
		my($lv2) = $landValue2->[$x][$y];

		if($landKind == $HlandTown) {
			# Į��
			my $rank = 0;
			foreach (reverse(0..$#HlandTownValue)) {
				if($HlandTownValue[$_] <= $lv) {
					$rank = $_;
					last;
				}
			}
			if($addpop[$rank] < 0) {
				# ��­
				$lv -= (random(-$addpop[$rank]) + 1);
				if($lv <= 0) {
					# ʿ�Ϥ��᤹
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} else {
				# ��Ĺ
				next if($HsurvivalTurn && $island->{'absent'});
				if($addpop[$rank]) {
					$lv += random($addpop[$rank]) + 1;
				}
			}
			$lv = $HvalueLandTownMax if($lv > $HvalueLandTownMax);
			$landValue->[$x][$y] = $lv;
		} elsif($landKind == $HlandPlains) {
			# ʿ��
			next if($HsurvivalTurn && $island->{'absent'});
			my $tflag = ($island->{'field'}) ? 1 : countGrow($island, $x, $y);
			my $rflag = (!$HsurvivalTurn) ? !($HtownGlow >= random(100)) : (($HislandTurn <= $HsurvivalTurn) ? random(3) : random(11));
			if(!$rflag && $tflag) {
				# ��������졢Į������С�������Į�ˤʤ�
				$land->[$x][$y] = $HlandTown;
				$landValue->[$x][$y] = 1;
			}
		} elsif($landKind == $HlandForest) {
			# ��
			if($lv < 200) {
			# �ڤ����䤹
				$landValue->[$x][$y] += $HtreeGrow;
			}
		} elsif($landKind == $HlandDefence) {
			if(int($lv / 100) > 0) {
				# �ɱһ��߼���
				my($lName) = &landName($landKind, $lv);

				# �����ﳲ�롼����
				wideDamage($id, $name, $island, $x, $y);
				logBombFire($id, $name, $lName, "($x, $y)");
				$island->{'dbase'}--;
			}
		} elsif($landKind == $HlandOil) {
			# ��������
			my($value, $str, $lName);
			$lName = landName($landKind, $lv);
			$value = $HoilMoney;
			if($HoilMoneyMin) {
				$value -= random($HoilMoney - $HoilMoneyMin + 1);
			}
			$island->{'money'} += $value;
			$island->{'oilincome'} += $value;
			$str = "$value$HunitMoney";

			# ������
			#logOilMoney($id, $name, $lName, "($x, $y)", $str, "����");

			# �ϳ�Ƚ��
			if(!$HnoDisFlag && random(1000) < $HoilRatio) {
				# �ϳ�
				logOilEnd($id, $name, $lName, "($x, $y)");
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 0;
			}
		} elsif($landKind == $HlandWaste) {
			# �Ӥ���(BattleField)
			if(!random(3) && $island->{'field'}) {
				if(!$landValue->[$x][$y]) {
					$land->[$x][$y] = $HlandPlains;
				} else {
					$landValue->[$x][$y]--;
				}
			}
		} elsif($landKind == $HlandComplex) {
			# ʣ���Ϸ�
			my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
			if($HcomplexTPCmax[$cKind]) {
				# ������ե饰����
				if($cTurn < $HcomplexTPCmax[$cKind]) {
					$cTurn++;
					$landValue->[$x][$y] = landPack($cTmp, $cKind, $cTurn, $cFood, $cMoney);
				}
			}
			my $attr = $HcomplexAttr[$cKind];
			if($attr & 0x1000) {
				# ���������
				my $value = $HcomplexRinMoney[1] - $HcomplexRinMoney[0] + 1;
				$value = $HcomplexRinMoney[0] + random($value);
				$island->{'rinmoney'}[$cKind] += $value;
				$island->{'money'} += $value;
			}
			if($attr & 0x2000) {
				# ���������
				my $value = $HcomplexRinFood[1] - $HcomplexRinFood[0] + 1;
				$value = $HcomplexRinFood[0] + random($value);
				$island->{'rinfood'}[$cKind] += $value;
				$island->{'food'} += $value;
			}
			if($attr & 0x10) {
				# �Ͼ�
				my($i, $sx, $sy);
				for($i = 1; $i < $an[$HcomplexFieldHex]; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					# �Ԥˤ�����Ĵ��
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					# �ϰϳ�
					next if(($sx < 0) || ($sy < 0));
					if($land->[$sx][$sy] == $HlandMonster || $land->[$sx][$sy] == $HlandHugeMonster){
						# ����1Hex���̤β��ä������硢���β��ä򹶷⤹��

						# �оݤȤʤ���äγ����Ǽ��Ф�
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$sx][$sy]);
						my $mName = ($land->[$sx][$sy] == $HlandMonster) ? $HmonsterName[$mKind] : $HhugeMonsterName[$mKind];

						if(!$mHflag) {
							if($land->[$sx][$sy] == $HlandHugeMonster) {
								my($j, $ssx, $ssy);
								foreach $j (1..6) {
									next if($HhugeMonsterImage[$mKind][$j] eq '');
									$ssx = $sx + $ax[$j];
									$ssy = $sy + $ay[$j];
									# �Ԥˤ�����Ĵ��
									$ssx-- if(!($ssy % 2) && ($sy % 2));
									$ssx = $correctX[$ssx + $#an];
									$ssy = $correctY[$ssy + $#an];
									# �ϰϳ�
									next if(($ssx < 0) || ($ssy < 0));

									next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
									# �����Ǥμ��Ф�
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
									if ($mFlag2 & 2) {
										# ���ˤ���
										$land->[$ssx][$ssy] = $HlandSea;
										$landValue->[$ssx][$ssy] = $mSea2;
									} else {
										# Φ�Ϥˤ���
										$land->[$ssx][$ssy] = $HlandWaste;
										$landValue->[$ssx][$ssy] = 0;
									}
									$HlandMove[$id][$ssx][$ssy] = 1;
								}
							}
							logIslpnt($id, $name, "($sx, $sy)", $mId, "��<B>$mName</B>�����Ϥ��Ͼ�˲����٤���ޤ�����");
						} else {
							logIslpnt($id, $name, "($sx, $sy)", $mId, "��<B>$mName</B>�����Ϥ��Ͼ���Τΰ����򼺤��ޤ�����");
						}
						# �оݤβ��ä��ݤ��
						if ($mFlag & 2) {
							# ���ˤ���
							$land->[$sx][$sy] = $HlandSea;
							$landValue->[$sx][$sy] = $mSea;
						} else {
							# Φ�Ϥˤ���
							$land->[$sx][$sy] = $HlandWaste;
							$landValue->[$sx][$sy] = 0;
						}
						$HlandMove[$id][$sx][$sy] = 1;
					}
				}
			}
		} elsif($landKind == $HlandMonster) {
			# ����
			moveMonster(0, $island, $x, $y, 0, 0);
		} elsif($landKind == $HlandHugeMonster) {
			# �������
			my($mHflag) = (monsterUnpack($lv))[1];
			moveMonster(0, $island, $x, $y, 0, 1) if(!$mHflag);
		} elsif ($landKind == $HlandNavy) {
			# ����
			#my($nStat, $nFlag) = (navyUnpack($lv, $lv2))[2,5];
		        my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			moveNavy(0, $island, $x, $y, 0) if(($nStat < 3) && ($nFlag < 3));
                        # ������ʤ��
                        if($nFlag == 3){
		            my($nn) = $HidToNumber{$nId};
      		            my($nIsland) = $Hislands[$nn];
			    if ($nIsland->{'money'} >= 500) {
                                $nHp++;
		                $nIsland->{'money'} -= 500;
			    }
                            if($nHp == $HnavyBuildTurn[$nKind]){
                                $nHp = $HnavyHP[$nKind];
                                $nFlag = 0;
                                logshunkou($id, $name, $HnavyName[$nKind], "($x, $y)");
                            }
		        ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
                        }
		} elsif ($landKind == $HlandSea) {
                    if($landValue->[$x][$y]){ # ������
                        if(!searchLand ($island, $x, $y)){ # ���Ϥ�Φ�Ϥ�̵���ä���
                            $landValue->[$x][$y] = 0; # �������ˤʤ�
                        }
                    }
		}

                # ������ư��ΤȤ����ݽ�
		if ($landKind != $HlandNavy) {
		    $landValue2->[$x][$y] = 0;
                }

		# �к�Ƚ��
		if((($landKind == $HlandTown) && ($lv > 30)) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'fire'}[0] ne '')) ||
			($landKind == $HlandHaribote) ||
			($landKind == $HlandFactory)) {
			if(!$HnoDisFlag && (random(1000) < $HdisFire * $island->{'itemAbility'}[22])) {
				# ���Ϥο��ȵ�ǰ��������
				if(!(countAround($island, $x, $y, $an[1], $HlandForest, $HlandMonument)) &&
					!(countAroundComplex($island, $x, $y, $an[1], 0x2))) {
					# ̵���ä���硢�кҤǲ���
					logFire($id, $name, landName($land->[$x][$y], $landValue->[$x][$y]), "($x, $y)");
	                                if($landKind == $HlandTown){
				            if($lv <= 100) {
					        $land->[$x][$y] = $HlandWaste;
					        $landValue->[$x][$y] = 0;
                                            }else{
					        $landValue->[$x][$y] -= 100;
				            }
                                        }else{
					    $land->[$x][$y] = $HlandWaste;
					    $landValue->[$x][$y] = 0;
					    if($landKind == $HlandComplex) {
						# ʣ���Ϸ��ʤ������Ϸ�
#						my $cKind = (landUnpack($lv))[1];
						$land->[$x][$y] = $HcomplexAfter[$cKind]->{'fire'}[0];
						$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'fire'}[1];
						$island->{'complex'}[$cKind]--;
                                            }
					}
				}
			}
		}
	}
}

# ñ�إå�������2
sub doEachHex2 {
	my($island) = @_;
	# Ƴ����
	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# �롼��
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];
		my($lv2) = $landValue2->[$x][$y];

               if ($landKind == $HlandNavy) {
			# ����
			#my($nStat, $nFlag) = (navyUnpack($lv, $lv2))[2,5];
		        my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			moveNavy(0, $island, $x, $y, 0) if(($nStat < 3) && ($nFlag < 3));
		}

                # ������ư��ΤȤ����ݽ�
		if ($landKind != $HlandNavy) {
		    $landValue2->[$x][$y] = 0;
                }
	}
}


# ���äΰ�ư(
# $tId�ɲâ����äΰ�ư�ˤϻȤ�ʤ�(0�Ǥ褤)
# $pre��2�ʾ�ǡְ�ư��ġ�(��ư����$arg = $pre - 2)
# $huge��1�ʤ�������
sub moveMonster {
	my($tId, $island, $x, $y, $pre, $huge) = @_;
	my($name) = islandName($island);
	my($id)   = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	my $flagmove = 0;
	my $arg = $pre - 2;
	if($arg < 0) {
		# ���äΰ�ư�ʤ�$flagmove��1�ˤ���
		$flagmove = 1;
	} elsif(!$arg) {
		# ���������Ե��ξ��
		$HmonsterMove[$id][$x][$y] = 2;
		return 1;
	}

	# ���Ǥ�ư������
	return if ($HmonsterMove[$id][$x][$y] == 2);

	# �����Ǥμ��Ф�
	my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$x][$y]);
	my $mName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = $HmonsterSpecial[$mKind];
	$special = $HhugeMonsterSpecial[$mKind] if($huge);

	if($flagmove) {
		# ���äΰ�ư�ξ��
		if($pre) {
			# ��԰�ư
			my $mm  = $HidToNumber{$mId};
			if(!($special & 0x10)) {
				# ǽ�Ϥ��ʤ�
				return;
			} elsif(defined $mm) {
				# ǽ�Ϥ������°�礬����
				# ���ޥ�ɥ����å�(��ư��Ĥ򤹤뤫)
				my($mIsland) = $Hislands[$mm];
				my($comArray, $c, $tflag, $ctflag);
				$comArray = $mIsland->{'command'};
				$tflag = 0;
				$ctflag = int($mIsland->{'itemAbility'}[6]);
				for($c = 0; $c < $HcommandMax; $c++) {
					my($ck) = $comArray->[$c]->{'kind'};
					my($ct) = $comArray->[$c]->{'target'};
					my($cx) = $comArray->[$c]->{'x'};
					my($cy) = $comArray->[$c]->{'y'};
					return if(($ck == $HcomMoveTarget) && ($ct == $id) && ($cx == $x) && ($cy == $y));
					$tflag += $HcomTurn[$ck];
					last if($tflag >= $ctflag);
				}
			}
		} elsif($special & 0x10) {
			# ��԰�ư�Ǥʤ��Τ�ǽ�Ϥ�����
			return;
		}
	} else {
		# ��ư��Ĥξ��
		return if($mId != $tId); # ������ɸ����á�
		return if (!($special & 0x80)); # ǽ�Ϥ��ʤ�
	}

	# �Ų����֤��ѹ�
	if (($special & 0x4) && (rand(1) < .50)) { # 50%
		$mFlag ^= 1;
		$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
	}

	# Φ��ǹŲ��桩
	return if (($mFlag & 1) && !($mFlag & 2));

	# ������ɸ����ª���ߥ����빶�⤹���ü�ǽ��
	if($special & 0x100) {
		require('./hako-mons-attack.cgi');
		# �Ų���Ǥʤ���й����оݤ�õ��
		searchMonsterTarget($island, $x, $y, $huge) unless($mFlag & 1);
		# ����ͽ�꤬���롩
		my $target = $HmonsterAttackTarget{"$id,$x,$y"};
		if (defined $target) {
			# ���⡪
			($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterAttack($island, $x, $y, $target->{x}, $target->{y}, $huge);
			$HmonsterAttackTarget{"$id,$x,$y"} = undef;
		}

		return if (($land->[$x][$y] == $HlandWaste) || ($land->[$x][$y] == $HlandSea));
	}

	my($sx, $sy, $d, $ssx, $ssy, $d2, $dmove, $rebody, @bodyHp);
	# ������äΥ����ʳ����̾��Ϸ����᤹
	if($huge) {
		foreach $i (1..6) {
			next if($HhugeMonsterImage[$mKind][$i] eq '');
			$ssx = $x + $ax[$i];
			$ssy = $y + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$ssx-- if(!($ssy % 2) && ($y % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# �ϰϳ��ξ��
			next if(($ssx < 0) || ($ssy < 0));

			if($land->[$ssx][$ssy] != $HlandHugeMonster) {
				$rebody .= "$i";
				next;
			}
			# �����Ǥμ��Ф�
			my($mHflag2, $mSea2, $mFlag2, $mHp2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4, 6];
			next if($mHflag2 != $i);
			$bodyHp[$i] = $mHp2;
			if ($mFlag2 & 2) {
				# ���ˤ���
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = $mSea2;
			} else {
				# Φ�Ϥˤ���
				$land->[$ssx][$ssy] = $HlandWaste;
				$landValue->[$ssx][$ssy] = 0;
			}
			$HlandMove[$id][$ssx][$ssy] = 1;
		}
	}
	if(($mHp < 1) && ($special & 0x100)) {
		if ($mFlag & 2) {
			# ���ˤ���
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = $mSea2;
		} else {
			# Φ�Ϥˤ���
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
		}
		$HlandMove[$id][$x][$y] = 1;
		return 0;
	}

	# ư�����������
	my $dnavy = 0;
	if($flagmove) { # ���äΰ�ư
		my(@dir);
		if ($special & 0x20) {
			# ����ư
			my $kind;
			# ���Ϥ򸫲�
			# �ʤ��ޤ깭���ϰϤ�õ���ʤ��褦�ˤ��Ƥ���������;�פʥ�������٤ˤʤ�ޤ���
			if ($d = searchTarget(0, $island, $x, $y, $an[3], $HlandHaribote, $HlandDefence, $HlandOil, $HlandSbase, $HlandBase, $HlandFarm, $HlandFactory, $HlandComplex, $HlandTown, $HlandNavy)) { # ���إå���
				# ��ɸ�����Ĥ��ä�
				push(@dir, $d);
			}
		}

		for ($i = $#dir + 1; $i < 3; $i++) {
			push(@dir, random(6) + 1);
		}

		while ($d = shift @dir) {
			$sx = $x + $ax[$d];
			$sy = $y + $ay[$d];
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# �ϰϳ�
			next if(($sx < 0) || ($sy < 0));
			if($HoceanMode) {
				# ̤�Τγ���ؤϰ�ư�Ǥ��ʤ�
				next if(!$HlandID[$sx][$sy]);
				if($HlandID[$sx][$sy] != $id) {
					# ����Τ�������Хȥ�ե�����ɤʤ龡���ư����Τ�Ʊ�������
					next if($HfieldMonster && $island->{'field'});
					# ����Τ�������Хȥ�ե�����ɤؤ�����ʤ�
					next if($HfieldUnconnect && ($Hislands[$HisToNumber{$HlandID[$sx][$sy]}]->{'field'} || $island->{'field'}));
				}
			}
			$dmove = 0;
			if($huge) {
				foreach $i (0..6) {
					next if(($HhugeMonsterImage[$mKind][$i] eq ''));
					$d2 = ($d + 3) % 6;
					$d2 = 6 if($d2 == 0);
					next if($i == $d2);
					$ssx = $sx + $ax[$i];
					$ssy = $sy + $ay[$i];
					# �Ԥˤ�����Ĵ��
					$ssx-- if(!($ssy % 2) && ($sy % 2));
					$ssx = $correctX[$ssx + $#an];
					$ssy = $correctY[$ssy + $#an];

					# �ϰϳ�Ƚ��
					if(($ssx < 0) || ($ssy < 0)) {
						$dmove = 1;
						next;
					}
					if($HoceanMode) {
						# ̤�Τγ���ؤϰ�ư�Ǥ��ʤ�
						if(!$HlandID[$ssx][$ssy]) {
							$dmove = 1;
							next;
						}
						if($HlandID[$ssx][$ssy] != $id) {
							# ����Τ�������Хȥ�ե�����ɤʤ龡���ư����Τ�Ʊ�������
							if($HfieldMonster && $island->{'field'}) {
								$dmove = 1;
								next;
							}
							# ����Τ�������Хȥ�ե�����ɤؤ�����ʤ�
							if($HfieldUnconnect && ($Hislands[$HisToNumber{$HlandID[$ssx][$ssy]}]->{'field'} || $island->{'field'})) {
								$dmove = 1;
								next;
							}
						}
					}
					if($land->[$ssx][$ssy] == $HlandNavy) {
						next if((navyUnpack($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]))[9] < 2);
						$dnavy = 1;
						next;
					}
					# ���á�������á�������ǰ�ꡤ�����ʤ��ư�Ǥ��ʤ�
					if(($land->[$ssx][$ssy] == $HlandMountain) ||
						($land->[$ssx][$ssy] == $HlandMonument) ||
						($land->[$ssx][$ssy] == $HlandCore) ||
						($land->[$ssx][$ssy] == $HlandResource) ||
						(($land->[$ssx][$ssy] == $HlandComplex) && ($HcomplexAfter[(landUnpack($landValue->[$ssx][$ssy]))[1]]->{'move'}[0] eq '')) ||
						($land->[$ssx][$ssy] == $HlandHugeMonster) ||
						($land->[$ssx][$ssy] == $HlandMonster)) {
						$dmove = 1;
						next;
					}
				}
				next if($dmove);
			} else {
				# ���á�������á�������ǰ�ꡤ�����ʤ��ư�Ǥ��ʤ�
				if(($land->[$sx][$sy] == $HlandMountain) ||
					($land->[$sx][$sy] == $HlandMonument) ||
					($land->[$sx][$sy] == $HlandCore) ||
					($land->[$ssx][$ssy] == $HlandResource) ||
					(($land->[$sx][$sy] == $HlandComplex) && ($HcomplexAfter[(landUnpack($landValue->[$sx][$sy]))[1]]->{'move'}[0] eq '')) ||
					($land->[$sx][$sy] == $HlandHugeMonster) ||
					($land->[$sx][$sy] == $HlandMonster)) {
					next;
				}
			}

			# ��ư�Ǥ����Ϸ�
			last;
		}

		# ��ư�Ǥ��ʤ��ä���
		unless(defined $d) {
			$HmonsterMove[$id][$x][$y] = 2;
			if($huge) {
				$dmove = 1;
			} else {
				return;
			}
		}

	} else { # �������
		$dmove = 0;
		$arg %= 7;
		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# �ϰϳ�Ƚ��
		if(($sx < 0) || ($sy < 0)) {
			$HmonsterMove[$id][$x][$y] = 2;
			return;
		}
		if($HoceanMode && ($HlandID[$sx][$sy] != $id)) {
			# ����Ǥʤ����
			my $mn = $HidToNumber{$HlandID[$sx][$sy]};
			my $comName = $HcomName[$HcomMoveTarget];
			my $mflag = 0;
			if(defined $mn) {
				my $tIsland = $Hislands[$mn];
				my(%amityFlag);
				my($amity) = $mIsland->{'amity'};
				foreach (@$amity) {
					$amityFlag{$_} = 1;
				}
				if (
					($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn || $amityFlag{$tIsland->{'id'}})) ||
					($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
					) {
					# ���⤬���Ĥ���Ƥ��ʤ�
					logNotAvail($mId, $name, $comName);
					$mflag = 1;
				} elsif (($HislandTurn - $nIsland->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($mId, $name, $comName);
					$mflag = 1;
				} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
					logLandNG($mId, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
					$mflag = 1;
				} elsif($HfieldUnconnect && $tIsland->{'field'}) {
					logLandNG($mId, $name, $comName, '���褬��³���Ƥ��ʤ�');
					$mflag = 1;

				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($mId, $name, $comName, '���߳�ȯ������Τ���');
						$mflag = 1;
					} elsif($mIsland->{'fight_id'} != $tIsland->{'id'}) {
						# ������ꤸ��ʤ��������
						logLandNG($mId, $name, $comName, '��ɸ���������Ǥʤ�����');
						$mflag = 1;
					}
				} elsif(($HuseDeWar > 1) && !$tIsland->{'field'} && !$HarmisticeTurn && !$HsurvivalTurn) {
					if(!$amityFlag{$tIsland->{'id'}}) {
						my $warflag = chkWarIsland($mId, $tIsland->{'id'});
						if(!$warflag) {
							logLandNG($mId, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
							$mflag = 1;
						} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
							logLandNG($mId, $name, $comName, 'ͱͽ������Τ���');
							$mflag = 1;
						}
					}
				} elsif($tIsland->{'event'}[0]) {
					my $level = 2 ** gainToLevel($island->{'gain'});
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($mId, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
						$mflag = 1;
					} elsif((!$tIsland->{'event'}[11]) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# �ɲ��ɸ�����Ĥ��ʤ�
						logLandNG($mId, $name, $comName, '���٥�ȳ�����Τ���');
						$mflag = 1;
					}
				}
			} else {
				# ��Τʤ�����ؤ�ư���ʤ�
				logLandNG($mId, $name, $comName, '̤�Τγ���Ǥ��뤿��');
				$mflag = 1;
			}
			if($mflag == 1) {
				$HmonsterMove[$id][$x][$y] = 2;
				return 0;
			}
		}

		if($huge) {
			foreach $i (0..6) {
				next if(($HhugeMonsterImage[$mKind][$i] eq ''));
				$d2 = ($arg + 3) % 6;
				$d2 = 6 if($d2 == 0);
				next if($i == $d2);
				$ssx = $sx + $ax[$i];
				$ssy = $sy + $ay[$i];
				# �Ԥˤ�����Ĵ��
				$ssx-- if(!($ssy % 2) && ($sy % 2));
				$ssx = $correctX[$ssx + $#an];
				$ssy = $correctY[$ssy + $#an];

				# �ϰϳ�Ƚ��
				if(($ssx < 0) || ($ssy < 0)) {
					$dmove = 1;
					last;
				}
				if($HoceanMode) {
					# ̤�Τγ���ؤϰ�ư�Ǥ��ʤ�
					if(!$HlandID[$ssx][$ssy]) {
						$dmove = 1;
						last;
					}
					if($HlandID[$ssx][$ssy] != $id) {
						# ����Τ�������Хȥ�ե�����ɤʤ龡���ư����Τ�Ʊ�������
						if($HfieldMonster && $island->{'field'}) {
							$dmove = 1;
							last;
						}
						# ����Τ�������Хȥ�ե�����ɤؤ�����ʤ�
						if($HfieldUnconnect && ($Hislands[$HisToNumber{$HlandID[$ssx][$ssy]}]->{'field'} || $island->{'field'})) {
							$dmove = 1;
							last;
						}
					}
				}
				if($land->[$ssx][$ssy] == $HlandNavy) {
					next if((navyUnpack($landValue->[$ssx][$ssy],$landValue2->[$ssx][$ssy]))[9] < 2);
					$dnavy = 1;
					next;
				}
				# ���á�������á�������ǰ�ꡤ�����ʤ��ư�Ǥ��ʤ�
				if(($land->[$ssx][$ssy] == $HlandMountain) ||
					($land->[$ssx][$ssy] == $HlandMonument) ||
					($land->[$ssx][$ssy] == $HlandCore) ||
					(($land->[$ssx][$ssy] == $HlandComplex) && ($HcomplexAfter[(landUnpack($landValue->[$ssx][$ssy]))[1]]->{'move'}[0] eq '')) ||
					($land->[$ssx][$ssy] == $HlandHugeMonster) ||
					($land->[$ssx][$ssy] == $HlandMonster)) {
					$dmove = 1;
					last;
				}
			}
		} else {
			# ���á�������á�������ǰ�ꡤ�����ʤ��ư�Ǥ��ʤ�
			if(($land->[$sx][$sy] == $HlandMountain) ||
				($land->[$sx][$sy] == $HlandMonument) ||
				($land->[$sx][$sy] == $HlandCore) ||
				(($land->[$sx][$sy] == $HlandComplex) && ($HcomplexAfter[(landUnpack($landValue->[$sx][$sy]))[1]]->{'move'}[0] eq '')) ||
				($land->[$sx][$sy] == $HlandHugeMonster) ||
				($land->[$sx][$sy] == $HlandMonster)) {
				$HmonsterMove[$id][$x][$y] = 2;
				return;
			}
		}
	}

	# ��ư����Ϸ��ˤ���å�����
	my($l)     = $land->[$sx][$sy];
	my($lv)    = $landValue->[$sx][$sy];
	my($lv2)   = $landValue2->[$sx][$sy];
	my($lName) = landName($l, $lv);
	my($point) = "($sx, $sy)";

	if ($l == $HlandNavy) {
		# ����
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless (($nSpecial & 0x8) || ($nFlag == 1)) {
			# ���Ǥ�ĳ��Ǥ�ʤ�
			if ($nHp > 1) {
				# �ѵ��Ϥ򸺤餹
				($landValue->[$sx][$sy], $landValue2->[$sx][$sy]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp - 1, $goalx, $goaly);

				logMonsAttackNavy($id, $name, $lName, $point, $mName, $mId);
				$HmonsterMove[$id][$x][$y] = 2;
				if($huge) {
					$dmove = 1;
				} else {
					return 1;
				}
			}
		}
	}

	# ������ä���ư�Ǥ��ʤ��ä���硢�����ʳ�������
	if($huge && ($dmove || $dnavy)) {
		foreach $i (1..6) {
			next if(($HhugeMonsterImage[$mKind][$i] eq ''));
			$ssx = $x + $ax[$i];
			$ssy = $y + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$ssx-- if(!($ssy % 2) && ($y % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# �ϰϳ�
			next if(($ssx < 0) || ($ssy < 0));
			# ��ư�Ǥ��ʤ��Ϸ��ʤ��������ʤ�
			next if(((($land->[$ssx][$ssy] == $HlandDefence) && $HdBaseAuto)) ||
				($land->[$ssx][$ssy] == $HlandMountain) ||
				($land->[$ssx][$ssy] == $HlandMonument) ||
				($land->[$ssx][$ssy] == $HlandCore) ||
				(($land->[$ssx][$ssy] == $HlandComplex) && ($HcomplexAfter[(landUnpack($landValue->[$ssx][$ssy]))[1]]->{'move'}[0] eq '')) ||
				($land->[$ssx][$ssy] == $HlandHugeMonster) ||
				($land->[$ssx][$ssy] == $HlandMonster));

			my($mSea2, $mFlag2);
			my $mHp2 = $bodyHp[$i];
			$mHp2 = $mHp if(!$mHp2);

			if ($land->[$ssx][$ssy] == $HlandSea) {
				# ��
				$mFlag2 |= 2;
				$mSea2 = $landValue->[$ssx][$ssy];
			} elsif (($land->[$ssx][$ssy] == $HlandSbase) || ($land->[$ssx][$ssy] == $HlandOil) || ($land->[$ssx][$ssy] == $HlandBouha) || ($land->[$ssx][$ssy] == $HlandSeaMine)) {
				# ���λ��ߤ��˲�
				$mFlag2 |= 2;
				$mSea2 = 0;
				if($l == $HlandBouha) {
					$mSea2 = 1;
					$island->{'bouha'}--;
				}
			} elsif ($land->[$ssx][$ssy] == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				$mFlag2 |= 2;
				if($nSpecial & 0x8) {
					$mSea2 = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} else {
					$mSea2 = 0;
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
						# ���Х��Х�
						$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					$HnavyAttackTarget{"$id,$ssx,$ssy"} = undef;
				}
			} elsif ($land->[$ssx][$ssy] == $HlandComplex) {
				my $cKind = (landUnpack($landValue->[$ssx][$ssy]))[1];
				my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
				if($cFlag) { # ����
					$mFlag2 |= 2;
					$mSea2 = $HcomplexAfter[$cKind]->{'move'}[1];
				} else { # Φ��
					$mFlag2 &= ~2;
					$mSea2 = 0;
				}
				$island->{'complex'}[$cKind]--;
			} elsif ($land->[$ssx][$ssy] == $HlandWaste) {
				# �Ӥ���
				$mFlag2 &= ~2;
				$mSea2 = 0;
			}
			if($rebody =~ /$i/) {
				next if(($special & 0x20000) && (random(100) >= $HpRebody));
				logMonsRebody($id, $name, "($ssx, $ssy)", $mName, $mId);
			}
			$land->[$ssx][$ssy] = $HlandHugeMonster;
			$landValue->[$ssx][$ssy] = monsterPack($mId, $i, $mSea2, $mExp, $mFlag2, $mKind, $mHp2);
#			undef $HlandMove[$id][$ssx][$ssy];
		}
		return if(!$dnavy);
		foreach $i (1..6) {
			next if($HhugeMonsterImage[$mKind][$i] eq '');
			$ssx = $sx + $ax[$i];
			$ssy = $sy + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$ssx-- if(!($ssy % 2) && ($sy % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# �ϰϳ�
			next if(($ssx < 0) || ($ssy < 0));
			next if ($land->[$ssx][$ssy] != $HlandNavy);

			# ��ư����Ϸ��ˤ���å�����
			$lName2 = landName($land->[$ssx][$ssy], $landValue->[$ssx][$ssy]);
			$point2 = "($ssx, $ssy)";

			my($mSea2);
			# ����
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]);
			my $nSpecial = $HnavySpecial[$nKind];
			if ($nHp > 1) {
				# �ѵ��Ϥ򸺤餹
				($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp - 1, $goalx, $goaly);
				logMonsAttackNavy($id, $name, $lName2, $point2, $mName, $mId);
			} else {
				my $n = $HidToNumber{$nId};
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if($nSpecial & 0x8) {
					$mSea2 = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} else {
					$mSea2 = 0;
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
						# ���Х��Х�
						$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					$HnavyAttackTarget{"$id,$ssx,$ssy"} = undef;
				}
				logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = $mSea2;
			}
		}
		return;
	}

	if ($mFlag & 2) {
		# ���ˤ���
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = $mSea;
	} else {
		# Φ�Ϥˤ���
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
	}
	$HlandMove[$id][$x][$y] = 1;

	# ��ư
	my $dm = ($flagmove ? $d : $arg);
	if ($l == $HlandSea) {
		# �����ư
		$mFlag |= 2;
		$mSea = $lv;
		logMonsMoveSea($id, $name, $lName, $point, $mName, $mId) if($huge == 0);
	} elsif (($l == $HlandSbase) || ($l == $HlandOil) || ($l == $HlandBouha)) {
		# ���λ��ߤ��˲�
		$mFlag |= 2;
		$mSea = 0;
		if($l == $HlandBouha) {
			$mSea = 1;
			$island->{'bouha'}--;
		}
		logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
	} elsif ($l == $HlandNavy) {
		# �������˲�
		$mFlag |= 2;
		my($nId, $nNo, $nKind) = (navyUnpack($lv, $lv2))[0, 6, 7];
		my $nSpecial = $HnavySpecial[$nKind];
		my $n = $HidToNumber{$nId};
		$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
		if($nSpecial & 0x8) {
			$mSea = 1;
			$Hislands[$n]->{'navyPort'}-- if(defined $n);
		} else {
			$mSea = 0;
			if(defined $n) {
				$Hislands[$n]->{'ships'}[$nNo]--;
				$Hislands[$n]->{'ships'}[4]--;
				# ���Х��Х�
				$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
			}
			$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
		}
		logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
	} elsif ($l == $HlandSeaMine) {
		# ����ʤ���̿�ϸ���
		$mHp -= $landValue->[$sx][$sy];
		$mFlag |= 2;
		$mSea = 0;
		# ������
		if($mHp < 1) {
			logMonsSeaMineDestroy($id, $name, $lName, $point, $mName, $mId);
		} else {
			logMonsSeaMineDamage($id, $name, $lName, $point, $mName, $mId);
		}
	} elsif($l == $HlandComplex) {
		# ʣ���Ϸ��ʤ������Ϸ�
		my $cKind = (landUnpack($lv))[1];
		my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
		if($cFlag) { # ����
			$mFlag |= 2;
			$mSea = $HcomplexAfter[$cKind]->{'move'}[1];
			logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
		} else { # Φ��
			$mFlag &= ~2;
			$mSea = 0;
			logMonsMove($id, $name, $lName, $point, $mName, $mId);
		}
		$island->{'complex'}[$cKind]--;
	} elsif($l == $HlandHugeMonster) {
		($mSea, $mFlag) = (monsterUnpack($lv))[2, 4];
	} else {
		# Φ�Ϥ��ư
		$mFlag &= ~2;
		$mSea = 0;
		logMonsMove($id, $name, $lName, $point, $mName, $mId) if(!$huge || ($HhugeMonsterImage[$mKind][$dm] eq ''));
	}

	if($mHp < 1) {
		# ��ư���˵���ǻ���
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = 0;
		$huge = 0;
		$HlandMove[$id][$sx][$sy] = 1;
	} elsif(!$HdBaseAuto || ($l != $HlandDefence)) {
		$land->[$sx][$sy] = ($huge) ? $HlandHugeMonster : $HlandMonster;
		$landValue->[$sx][$sy] = monsterPack($mId, 0, $mSea, $mExp, $mFlag, $mKind, $mHp);
	}

	my $dflag = 0;
	my($l2, $lv2, $lName2, $point2);
	if($huge && ($mHp > 0)) {
		foreach $i (1..6) {
			next if($HhugeMonsterImage[$mKind][$i] eq '');
			$ssx = $sx + $ax[$i];
			$ssy = $sy + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$ssx-- if(!($ssy % 2) && ($sy % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# �ϰϳ�
			next if(($ssx < 0) || ($ssy < 0));

			# ��ư����Ϸ��ˤ���å�����
			$l2     = $land->[$ssx][$ssy];
			$lv2    = $landValue->[$ssx][$ssy];
			$lName2 = landName($land->[$ssx][$ssy], $landValue->[$ssx][$ssy]);
			$point2 = "($ssx, $ssy)";

			my($mSea2, $mFlag2);
			my $mHp2 = $bodyHp[$i];
			$mHp2 = $mHp if(!$mHp2);
			my $navyFlag = 0;

			if($rebody =~ /$i/) {
				next if(($special & 0x20000) && (random(100) >= $HpRebody));
				logMonsRebody($id, $name, "($ssx, $ssy)", $mName, $mId);
			}
			if ($l2 == $HlandSea) {
				# �����ư
				$mFlag2 |= 2;
				$mSea2 = $lv2;
				logMonsMoveSea($id, $name, $lName2, $point2, $mName, $mId) if($i == $dm);
			} elsif (($l2 == $HlandSbase) || ($l2 == $HlandOil) || ($l2 == $HlandBouha)) {
				# ���λ��ߤ��˲�
				$mFlag2 |= 2;
				$mSea2 = 0;
				if($l2 == $HlandBouha) {
					$mSea2 = 1;
					$island->{'bouha'}--;
				}
				logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
			} elsif ($l2 == $HlandNavy) {
				# ����
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				if ($nHp > 1) {
					# �ѵ��Ϥ򸺤餹
					$navyFlag = 1;
					($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp - 1, $goalx, $goaly);
					logMonsAttackNavy($id, $name, $lName2, $point2, $mName, $mId);
				} else {
					$mFlag2 |= 2;
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
					if($nSpecial & 0x8) {
						$mSea2 = 1;
						$Hislands[$n]->{'navyPort'}-- if(defined $n);
					} else {
						$mSea2 = 0;
						if(defined $n) {
							$Hislands[$n]->{'ships'}[$nNo]--;
							$Hislands[$n]->{'ships'}[4]--;
							# ���Х��Х�
							$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
						}
						$HnavyAttackTarget{"$id,$ssx,$ssy"} = undef;
					}
					logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
					# ���Х��Х�
				}
			} elsif ($l2 == $HlandSeaMine) {
				# ����ʤ���̿�ϸ���
				$mHp2 -= $lv2;
				$mFlag2 |= 2;
				$mSea2 = 0;
				# ������
				if($mHp2 < 1) {
					logMonsSeaMineDestroy($id, $name, $lName2, $point2, $mName, $mId);
				} else {
					logMonsSeaMineDamage($id, $name, $lName2, $point2, $mName, $mId);
				}
			} elsif($l2 == $HlandComplex) {
				# ʣ���Ϸ��ʤ������Ϸ�
				my $cKind = (landUnpack($lv2))[1];
				my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
				if($cFlag) { # ����
					$mFlag2 |= 2;
					$mSea2 = $HcomplexAfter[$cKind]->{'move'}[1];
					logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
				} else { # Φ��
					$mFlag2 &= ~2;
					$mSea2 = 0;
					logMonsMove($id, $name, $lName2, $point2, $mName, $mId);
				}
				$island->{'complex'}[$cKind]--;
#			} elsif($land->[$ssx][$ssy] == $HlandHugeMonster) {
#				($mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[2, 4];
			} elsif (($l2 == $HlandDefence) && $HdBaseAuto) {
				# �ɱһ��ߤ�Ƨ���
				$dflag = 1;
				last;
			} else {
				# Φ�Ϥ��ư
				$mFlag2 &= ~2;
				$mSea2 = 0;
				logMonsMove($id, $name, $lName2, $point2, $mName, $mId) if(($l2 != $HlandWaste) || ($i == $dm));
			}
			next if($navyFlag);
			if($mHp2 < 1) {
				# ������Τΰ������ä���
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = $mSea2;
			} else {
				$land->[$ssx][$ssy] = $HlandHugeMonster;
				$landValue->[$ssx][$ssy] = monsterPack($mId, $i, $mSea2, $mExp, $mFlag2, $mKind, $mHp2);
#				undef $HlandMove[$id][$ssx][$ssy];
			}
		}
	}

	# ��ư�Ѥߥե饰
	if ($special & 0x2) {
		# �ȤƤ�®������
		# ��ư�Ѥߥե饰��Ω�Ƥʤ�
	} elsif ($special & 0x1) {
		# ®������
		$HmonsterMove[$id][$sx][$sy] = $HmonsterMove[$id][$x][$y] + 1;
	} else {
		# ���̤β���
		$HmonsterMove[$id][$sx][$sy] = 2;
	}
#	undef $HlandMove[$id][$sx][$sy];

	if ((($l == $HlandDefence) || ($dflag)) && $HdBaseAuto) {
		($lName, $point, $sx, $sy) = ($lName2, $point2, $ssx, $ssy) if($dflag);
		# �ɱһ��ߤ�Ƨ���
		# �����ﳲ�롼����
		wideDamage($id, $name, $island, $sx, $sy);
		logMonsMoveDefence($id, $name, $lName, $point, $mName, $mId);
		$island->{'dbase'}--;
	}
	return 1;
}

# ������������
sub supplyNavy {
	my($island) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	my $flag;
	my($i, $x, $y, $lv, $hp);
	my(%amityFlag, %repairShip, %failShip);
	my($amity) = $island->{'amity'};
	$amityFlag{$id} = 1;
	if(!$HamityInvalid || !$island->{'field'}) {
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
	}
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];

		# ������õ��
		next unless ($land->[$x][$y] == $HlandNavy);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $special = $HnavySpecial[$nKind];
		my $tn = $HidToNumber{$nId};

                # ��¤����ä�����뤷�ʤ�
                if($nFlag == 3){
                    next;
                }

                # ΥΦ�����ʤ��
                if($wait > 0){
                    $wait--;
                }

		if (defined $tn) {
			# ¸�ߤ�����δ����ʤ�
			my $tIsland = $Hislands[$tn];
			$flag = 0;
			# ������񤹤�
			my $mflag = $tIsland->{'itemAbility'}[14];
			my $nMoney = int($HnavyMoney[$nKind] * $mflag); # �ݻ���
			if ($tIsland->{'money'} >= $nMoney) {
				$tIsland->{'money'} -= $nMoney;
				if($nMoney >= 0) {
					$tIsland->{'upkeepMoney'} += $nMoney;
				} else {
					$tIsland->{'upkeepMoneyPlus'} -= $nMoney;
				}
				$flag |= 1;
			} else {
				$nExp -= 10;
				$nExp = 0 if ($nExp < 0);
			}
			# ��������񤹤�
			my $fflag = $tIsland->{'itemAbility'}[13];
			my $nFood = int($HnavyFood[$nKind] * $fflag); # �ݻ�����
			if ($tIsland->{'food'} >= $nFood) {
				$tIsland->{'food'} -= $nFood;
				if($nFood >= 0) {
					$tIsland->{'upkeepFood'} += $nFood;
				} else {
					$tIsland->{'upkeepFoodPlus'} -= $nFood;
				}
				$flag |= 2;
			} else {
				$nExp -= 10;
				$nExp = 0 if ($nExp < 0);
			}
			my @tAmity = (!$HamityInvalid || !$island->{'field'}) ? @{$tIsland->{'amityBy'}} : ();
#			my $sflag = ($tIsland->{'itemAbility'}[1] && (!$HitemInvalid || !$island->{'field'})) ? 1 : 0;

				# $HnavySupplyFlag��0�ΤȤ��ϡ�����orͧ����δ���ʤ� or
				# ����($HnavySupplyRange������)�˼���orͧ��������ꤷ�Ƥ���Ƥ����������(�ü�ǽ��)�������顢�����̤˥ץ饹����
                        my $repair = 0;
                        $repair += countAroundNavySpecial($island, $x, $y, 0x10000, 19, $nId);
                        $repair += countAroundNavySpecial($island, $x, $y, 0x10000, 19, @tAmity);
                        if($nId == $id){
                            $repair ++;
                        }


#			if ($HnavySupplyFlag || ($amityFlag{$nId} == 1) || $sflag ||
#				countAroundNavySpecial($island, $x, $y, 0x10000, $an[$HnavySupplyRange[$nKind]], $nId, @tAmity)) {

				my $point = "($x, $y)";

				if ($flag == 3) {
                                    if($repair){
					# ��ʬ�����Ǥ���

					# �������Ϥ��ᡢ�ѵ��Ϥ��������
					$hp = int($HnavyHP[$nKind] * (120 + $nExp)/120);
					if ($nHp < $hp) {
						# �ѵ��� +1
						$nHp += $repair;
						$repairShip{$nId} .= " <B>$HnavyName[$nKind]</B>${HtagName_}${point}${H_tagName}";
					}
                                        if($nHp >= $hp){
                                            $nHp = $hp;
                                        }
                                    }
				} else {
					# ���Ǥ��ʤ��ä�
					$failShip{$nId} .= " <B>$HnavyName[$nKind]</B>${HtagName_}${point}${H_tagName}";
				}
#			}
			($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
		} else {
			if ($nFlag == 1) {
				# �ĳ��ʤ��˲�Ψ���å�
				$nExp += int(rand(10) + 1); # 1%��10% 
				if ($nExp >= 100) {
					# �˲�Ψ 100% �ˤʤ�Ⱦ���
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				} else {
					($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
				}
			}
		}

		# ������ɸ��õ��
		if(!($special & 0x1000000) && !($nFlag == 1) && ($nStat < 2)) {
			# �ĳ��ʳ��ʤ�
			searchNavyTarget($island, $x, $y);
		}
	}
	# ������
	my @ids;
	foreach (keys %repairShip) {
		push(@ids, $_);
		logNavyShipRepairM($id, $_, $repairShip{$_});
	}
	foreach (keys %failShip) {
		push(@ids, $_);
		logNavyShipSupplyFailM($id, $_, $failShip{$_});
	}
	my $idstr = join('-', @ids);
	logNavyShipRepair($id, $name, $idstr) if($idstr ne '');
}

# �����ΰ�ư����ư���
# $tId�ɲâ������ΰ�ư�ˤϻȤ�ʤ�(0�Ǥ褤)
# $pre��2�ʾ�ǡְ�ư��ġ�(��ư����$arg = $pre - 2)
sub moveNavy {
	my($tId, $island, $x, $y, $pre) = @_;
	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
        my($point)     = "($x, $y)";

	my $flagmove = 0;
	my $arg = $pre - 2;
	if($arg < 0) {
		# �����ΰ�ư�ʤ�$flagmove��1�ˤ���
		$flagmove = 1;
	} elsif(!$arg) {
		# ��ư��Ĥ��Ե��ξ��
		$HnavyMove[$id][$x][$y] = 2;
		return 1;
	}

	# ���Ǥ�ư������
	return if ($HnavyMove[$id][$x][$y] == 2);

	# �����Ǥμ��Ф�
	my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$x][$y], $landValue2->[$x][$y]);
	my $nn  = $HidToNumber{$nId};
	my($nIsland);
	$nIsland  = $Hislands[$nn] if(defined $nn);
	my $nName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = $HnavySpecial[$nKind];

	# �����ư(�ɸ�������)�ե饰�����äƤ�����ϡ���ư���ʤ�
#	return if($nIsland->{'NavyMove_flag'}[$nNo]);

	if($flagmove) {
		# �����ΰ�ư�ξ��
		if($pre) {
			# ��԰�ư
			if(!($special & 0x10)) {
				# ǽ�Ϥ��ʤ�
				return;
			} elsif(defined $nn) {
				# ǽ�Ϥ������°�礬����
				# ���ޥ�ɥ����å�(��ư��Ĥ򤹤뤫)
				my($comArray, $c, $tflag, $ctflag);
				$comArray = $nIsland->{'command'};
				$tflag = 0;
				$ctflag = int($nIsland->{'itemAbility'}[6]);
				for($c = 0; $c < $HcommandMax; $c++) {
					my($ck) = $comArray->[$c]->{'kind'};
					my($ct) = $comArray->[$c]->{'target'};
					my($cx) = $comArray->[$c]->{'x'};
					my($cy) = $comArray->[$c]->{'y'};
					return if(($ck == $HcomMoveTarget) && ($ct == $id) && ($cx == $x) && ($cy == $y));
					$tflag += $HcomTurn[$ck];
					last if($tflag >= $ctflag);
				}
			}
		} elsif($special & 0x10) {
			# ��԰�ư�Ǥʤ��Τ�ǽ�Ϥ�����
			return;
		}
	} else {
		# ��ư��Ĥξ��
		return if($nId != $tId); # ����δ�����
		return if (!($special & 0x80) && !$HnavyNoMove[$nKind]); # ǽ�Ϥ��ʤ�
	}

	# �ĳ���
	return if ($nFlag == 1);

	# ������֤��ѹ�
	if ($special & 0x4) {
		if (random(100) < $HsubmarineSurface[$nKind]) { # ����Ψ:20%
			# ���
			$nFlag = 0;
		} else {
			# ����
			$nFlag = 2;
		}
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
	}

	# ����η�����
	if ($special & 0x200000) {
            my $i;
            for($i = 1; $i <= 6; $i++){
                my $sx = $x + $ax[$i];
                my $sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
                if(($land->[$sx][$sy] == $HlandResource) &&
		   ($Resource[$id][$sx][$sy] != 1)){
                    my ($rTmp, $rKind, $rTurn, $rFood, $rMoney) = landUnpack($landValue->[$sx][$sy]);
                    if($rKind == 0){
                        # ����η�����+�۾����Ȥ߹�碌
                        my $arg = int(($rMoney * 20 + 1200) * (random(120) + $nExp) / 240);
                        my $point2 = "($sx, $sy)";
                        $Hislands[$HidToNumber{$nId}]->{'money'} += $arg;
                        $nExp++;
                        if($nExp >= 120){
                            $nExp = 120;
                        }
		        $Resource[$id][$sx][$sy] = 1; # �μ�Ѥߥե饰
                        logResourceS($id, $nId, $name, '����η�����', '����۾�', $point, $point2, $arg);
                        ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
                        if(!random(300)){
                            $land->[$sx][$sy] = $HlandSea;
                            $landValue->[$sx][$sy] = 0;
                        }
                    }
                }
            }
	}

	# ������
	if ($special & 0x400000) {
            my $i;
            for($i = 1; $i <= 6; $i++){
                my $sx = $x + $ax[$i];
                my $sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
                if(($land->[$sx][$sy] == $HlandResource) &&
		   ($Resource[$id][$sx][$sy] != 1)){
                    my ($rTmp, $rKind, $rTurn, $rFood, $rMoney) = landUnpack($landValue->[$sx][$sy]);
                    if($rKind == 1){
                        # ������+���̤��Ȥ߹�碌
                        my $arg = int(($rFood * 20 + 1200) * (random(120) + $nExp) / 240 * 10);
                        my $point2 = "($sx, $sy)";
                        $Hislands[$HidToNumber{$nId}]->{'food'} += $arg;
                        $nExp++;
                        if($nExp >= 120){
                            $nExp = 120;
                        }
		        $Resource[$id][$sx][$sy] = 1; # �μ�Ѥߥե饰
                        logResourceF($id, $nId, $name, '������', '����', $point, $point2, $arg);
                        ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
                        if(!random(300)){
                            $land->[$sx][$sy] = $HlandSea;
                            $landValue->[$sx][$sy] = 0;
                        }
                    }
                }
            }
	}

        # �������˥å�
	if ($special & 0x20000) {

	    return if($HnavyMove[$id][$x][$y] == 2);

	    # �����ʡ��������
	    my($nn) = $HidToNumber{$nId};
	    my($nIsland) = $Hislands[$nn];
	    my($nName) = islandName($nIsland);
            my $nNavyComLevel = gainToLevel($nIsland->{'gain'});
	    if($nNavyComLevel< 6) {
                # �и���­��ʤ��ä��鲿����鷺���
	        return 0;
	    }

            # ������
           my $navyComLevel = gainToLevel($island->{'gain'});
	    if($navyComLevel< 6) {
                # �и���­��ʤ��ä��鲿����鷺���
	        return 0;
	    }

            # �ǰפǤ����ǡ����Υ졼�ȳ�ǧ
            my $nFoodrate = int(($nIsland->{'money'}/$HmaximumMoney) / ($nIsland->{'food'}/$HmaximumFood) * 10);
            if($nFoodrate < 5){
                $nFoodrate = 5;
            }elsif($nFoodrate > 20){
                $nFoodrate = 20;
            }

            my $foodrate = int(($island->{'money'}/$HmaximumMoney) / ($island->{'food'}/$HmaximumFood) * 10);
            if($foodrate < 5){
                $foodrate = 5;
            }elsif($foodrate > 20){
                $foodrate = 20;
            }

            # �ǰ��̻���
            my $value = int(3000 + 3000 * ($nExp /120));

            if($nFoodrate < $foodrate){
                # (���礫�鸫��)���Υ졼�Ȥ��⤤����͢��
		$nIsland->{'food'} -= $value;
		$island->{'food'} += $value;
		$nIsland->{'money'} += int($value * $foodrate / 100);
		$island->{'money'} -= int($value * $foodrate / 100);
                $nExp++;
                logTrade($id, $nId, $name, $nName, $value, int($value * $foodrate / 100), '͢��', $point);
            }elsif($nFoodrate > $foodrate){
                # ͢��
		$nIsland->{'food'} += $value;
		$island->{'food'} -= $value;
		$nIsland->{'money'} -= int($value * $foodrate / 100);
		$island->{'money'} += int($value * $foodrate / 100);
                $nExp++;
                logTrade($id, $nId, $name, $nName, $value, int($value * $foodrate / 100), '͢��', $point);
            }else{
                # Ʊ�����ä�����ǰ�̵��
            }
	    $HnavyMove[$id][$x][$y] = 2;
            if($nExp > 120){
                $nExp = 120;
            }

            ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
	}

	# ������ɸ��õ������ɸ����ǽ�ϡ�
	if(($special & 0x1000000) && !$HnavyMoveCount[$id][$x][$y] && !($nFlag == 1) && ($nStat < 2)) {
		# �ĳ��ʳ��ʤ�
		searchNavyTarget($island, $x, $y);
	}
	# ����ͽ�꤬���롩
	my $target = $HnavyAttackTarget{"$id,$x,$y"};
	if (defined $target) {
		# ���⡪
		($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyAttack($island, $x, $y, $target->{x}, $target->{y}, $target->{special});
		$HnavyAttackTarget{"$id,$x,$y"} = undef;
	}

	# �ĳ����ޤ��ϳ�(����)��
	return if (($nFlag == 1) || ($land->[$x][$y] == $HlandSea));

	# ����
	return if ($special & 0x8);

	# ư���ʤ��ϡ�
        if ($HnavyNoMove[$nKind]){
            # ��ư�Ѥߥե饰
	    $HnavyMove[$id][$sx][$sy] = 2;
            return ;
        }
 
        # ���꥿���󤹤��Ƥ��鵢��
        if(($HnavyCruiseTurn[$nKind] != 0) && ($wait <= 0) && ($nId)) {
	        my $n = $HidToNumber{$nId};
                $Hislands[$n]->{'money'} += $HnavyCost[$nKind];
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = $nSea;
                return;
        }

        # ��ư��λؼ������ξ����ä����Ե���
        if(($goalx == $x) &&
           ($goaly == $y)) {
            $goalx = 31;
            $goaly = 31;
            # ��ư�Ѥߥե饰
	    $HnavyMove[$id][$sx][$sy] = 2;
        }

        # ��Ĳ�ǽ�ˤ�ؤ�餺��ư�ؼ���̵������ư��ĤǤ�ʤ�
        if(($special & 0x80) && ($goalx == 31) && ($goaly == 31) && ($flagmove)) {
            ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
#logdebug ($id, "code2($x, $y)");
            return;
        }

	# ����ε���ǥ��᡼��������뤫�ɤ���
	my(%amityFlag);
	if($HmineSelfDamage) {
		$amityFlag{$id} = 1;
		if($HmineSelfDamage == 2) {
			foreach (@{$island->{'amity'}}) {
				$amityFlag{$_} = 1;
			}
		}
	}

	# ������ͧ����������ǧ
	my(%nAmityFlag);
	if($HnavySafetyZone) {
		$nAmityFlag{$nId} = 1;
		if(defined $nn && $HnavySafetyZone == 2) {
			foreach (@{$nIsland->{'amity'}}) {
				$nAmityFlag{$_} = 1;
			}
		}
	}

	my($i, $sx, $sy);
	# ư�����������
	if($flagmove) { # �����ΰ�ư
		my $mvotherisl = 0;
		my(@dir, $d);
		#if($HoceanMode && (defined $nn) && (defined $nIsland->{'move'}[$nNo])) {
		if($special & 0x80) {
			#my($tx, $ty) = split(/,/, $nIsland->{'move'}[$nNo]);
                        my $tx = $goalx;
                        my $ty = $goaly;

			# ��ư������׻�����
			my $dy = ($ty > $y) ? 2 : ($ty < $y) ? 0 : 1;
			if ($tx < $x) {
				$d = (6, 5, 4)[$dy];
				push(@dir, $d);
				if($dy != 1) {
					$d = (6, 5, 4)[1];
					push(@dir, $d);
				}
			} elsif ($tx > $x) {
				$d = (1, 2, 3)[$dy];
				push(@dir, $d);
				if($dy != 1) {
					$d = (1, 2, 3)[1];
					push(@dir, $d);
				}
			} else {
				my $r = rand(1);
				$d = (($r < .5 ? 1 : 6), 0, ($r < .5 ? 3 : 4))[$dy];
				push(@dir, $d);
				if($dy != 1) {
					$d = (($r >= .5 ? 1 : 6), 0, ($r >= .5 ? 3 : 4))[$dy];
					push(@dir, $d);
				}
			}
			$mvotherisl = 1 if(@dir);
		} elsif ($special & 0x800) {
			# ����ư�ʼ�ʬ��°�������δ��Ϥ��ܻؤ��ư�ư��
			# ���Ϥ򸫲�
			if ($d = searchTarget($id, $island, $x, $y, $an[$HnavyTowardRange[$nKind]], $HlandNavy)) {
				# ���Ϥ����Ĥ��ä�
				push(@dir, $d);
			}
		}
		for ($i = $#dir; $i < 3; $i++) {
			push(@dir, random(6) + 1);
		}

		$mvotherisl = (!(defined $nn)); # ��°�����ϼ�ͳ��ư����
		while ($d = shift @dir) {
			$sx = $x + $ax[$d];
			$sy = $y + $ay[$d];
                        $point = "($sx, $sy)";
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# �ϰϳ�
			next if(($sx < 0) || ($sy < 0));
			if($HoceanMode) {
				# ̤�Τγ���ؤϰ�ư�Ǥ��ʤ�
				next if(!$HlandID[$sx][$sy]);
				if($HlandID[$sx][$sy] != $id) {
					# ��ư���᤬�ʤ�������°�����Ǥʤ���С������ư����Τ�Ʊ�������
					next if(!$mvotherisl);
					# ����Τ�������Хȥ�ե�����ɤʤ龡���ư����Τ�Ʊ�������
					next if($HfieldNavy && $island->{'field'});
					# ����Τ�������Хȥ�ե�����ɤؤ�����ʤ�
					next if($HfieldUnconnect && ($Hislands[$HisToNumber{$HlandID[$sx][$sy]}]->{'field'} || $island->{'field'}));
				}
			}
			my($l)  = $land->[$sx][$sy];
			my($lv) = $landValue->[$sx][$sy];
			my($lv2) = $landValue2->[$sx][$sy];
			# ������������ʳ��ʤ��ư�Ǥ��ʤ�
			my($tId, $tTmp, $tStat, $tSea, $tExp, $tFlag, $tNo, $tKind, $tWait, $tHp, $tgoalx, $tgoaly) = navyUnpack($lv, $lv2) if($l == $HlandNavy);
			# unless����˰�ư�Ǥ����Ϸ��򵭽�
			next unless (
				(($l == $HlandSea) && (!$lv || $HnavyMoveAsase)) || # ��
				(($l == $HlandSeaMine) && !$amityFlag{$nId}) ||     # ����
				(($l == $HlandNavy) && # ������
					(($HsuicideAbility || !$nId) && ($special & 0x2000000) && !$nAmityFlag{$tId}) # ��������
				) ||
				(($l == $HlandWaste) && ($special & 0x80000)) # ����
			);

			# ��ư�Ǥ�����ǡ����Ϥκ¾�Ƚ��
                        if(($l == $HlandSea) && ($lv == 1) && ($HnavyBuildTurn[$nKind] != 0)){
                            if(random(10) == 0){ # �¾̤γ�Ψ
                                # �¾̤�������HP��3��Υ��᡼���������
                                $nHp -= int($HnavyHP[$nKind] * 0.3);
                            }
                        }
			last;
		}

		# ��ư�Ǥ��ʤ��ä���
		return unless (defined $d);

	} else { # ��ư���
		$arg %= 7;
		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# �ϰϳ�Ƚ��
		if(($sx < 0) || ($sy < 0)) {
			$HnavyMove[$id][$x][$y] = 2;
			return;
		}
		if($HoceanMode && ($HlandID[$sx][$sy] != $id)) {
			# ����Ǥʤ����
			my $mn = $HidToNumber{$HlandID[$sx][$sy]};
			my $comName = $HcomName[$HcomMoveTarget];
			my $mflag = 0;
			if(defined $mn) {
				my $tIsland = $Hislands[$mn];
				if (
					($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
					($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
					) {
					# ���⤬���Ĥ���Ƥ��ʤ�
					logNotAvail($nId, $name, $comName);
					$mflag = 1;
				} elsif (($HislandTurn - $nIsland->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($nId, $name, $comName);
					$mflag = 1;
				} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
					logLandNG($nId, $name, $comName, '���ߡڴ����ͤ�������ۤΤ���');
					$mflag = 1;
				} elsif($HfieldUnconnect && $tIsland->{'field'}) {
					logLandNG($nId, $name, $comName, '���褬��³���Ƥ��ʤ�');
					$mflag = 1;
				} elsif($HnofleetNotAvail && !$tIsland->{'field'} && !$tIsland->{'ships'}[4]) {
					logLandNG($nId, $name, $comName, "�������ͭ���ʤ�$AfterName�Ǥ��ä�����");
					$mflag = 1;
				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($nId, $name, $comName, '���߳�ȯ������Τ���');
						$mflag = 1;
					} elsif($nIsland->{'fight_id'} != $tIsland->{'id'}) {
						# ������ꤸ��ʤ��������
						logLandNG($nId, $name, $comName, '��ɸ���������Ǥʤ�����');
						$mflag = 1;
					}
				} elsif(($HuseDeWar > 1) && !$tIsland->{'field'} && !$HarmisticeTurn && !$HsurvivalTurn) {
					my(%amityFlag);
					my($amity) = $nIsland->{'amity'};
					foreach (@$amity) {
						$amityFlag{$_} = 1;
					}
					if(!$amityFlag{$tIsland->{'id'}}) {
						my $warflag = chkWarIsland($nId, $tIsland->{'id'});
						if(!$warflag) {
							logLandNG($nId, $name, $comName, '�����۹�򤷤Ƥ��ʤ�����');
							$mflag = 1;
						} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
							logLandNG($nId, $name, $comName, 'ͱͽ������Τ���');
							$mflag = 1;
						}
					}
				} elsif($tIsland->{'event'}[0]) {
					my $level = 2 ** gainToLevel($island->{'gain'});
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($nId, $name, $comName, '���ߥ��٥�Ƚ���������Τ���');
						$mflag = 1;
					} elsif($tIsland->{'event'}[3] && ($tIsland->{'event'}[3] <= $nIsland->{"invade$tIsland->{'id'}"})) {
						logLandNG($nId, $name, $comName, '�ɸ���ǽ��������Ķ���뤿��');
						$mflag = 1;
					} elsif($HmaxComNavyLevel && !($tIsland->{'event'}[5] & (2 ** gainToLevel($nIsland->{'gain'})))) {
						logLandNG($nId, $name, $comName, '�ɸ���ǽ��٥�Ǥʤ�����');
						$mflag = 1;
					} elsif((!$tIsland->{'event'}[11]) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# �ɲ��ɸ�����Ĥ��ʤ�
						logLandNG($nId, $name, $comName, '���٥�ȳ�����Τ���');
						$mflag = 1;
					}
				} elsif($nIsland->{'NavyAttack_flag'}[$nNo]) {
					# ���ޥ�ɤ���Ĥ��ʤ�
					logLandNG($nId, $name, $comName, '��Ʈ���֤ˤ��뤿��');
					$mflag = 1;
				}
			} else {
				# ��Τʤ�����ؤ�ư���ʤ�
				logLandNG($nId, $name, $comName, '̤�Τγ���Ǥ��뤿��');
				$mflag = 1;
			}
			if($mflag == 1) {
				$HnavyMove[$id][$x][$y] = 2;
				return 0;
			}
		}

		my($l)  = $land->[$sx][$sy];
		my($lv) = $landValue->[$sx][$sy];
		my($lv2) = $landValue2->[$sx][$sy];
		my($tId, $tTmp, $tStat, $tSea, $tExp, $tFlag, $tNo, $tKind, $tWait, $tHp, $tgoalx, $tgoaly) = navyUnpack($lv, $lv2) if($l == $HlandNavy);
		# unless����˰�ư�Ǥ����Ϸ��򵭽�
		unless (
			($l == $HlandSea) || # ��
			(($l == $HlandSeaMine) && !$amityFlag{$nId}) ||     # ����
			(($l == $HlandNavy) &&  # ������
				(($special & 0x2000000) && !$nAmityFlag{$tId}) # ��������
			) ||
			(($l == $HlandWaste) && ($special & 0x80000)) # ����
		) {
			$HnavyMove[$id][$x][$y] = 2;
			return;
		}

		# ��ư����Ϸ��ˤ���å�����(��ư��Ļ�)
		my($lName) = landName($l, $lv);
		my($point) = "($sx, $sy)";
#		logNavyMoveSea($id, $name, $lName, $point, $nName, $nId) if($land->[$sx][$sy] != $HlandWaste && $land->[$sx][$sy] != $HlandNavy);
	}

	if($land->[$sx][$sy] == $HlandWaste) {
		logNavyMoveDestroy($id, $name, landName($land->[$sx][$sy], $landValue->[$sx][$sy]), "($sx, $sy)", $nName, $nId, $landValue->[$sx][$sy]);
		if(!$landValue->[$sx][$sy]) {
			# ��ư���ʤ�
			$landValue->[$sx][$sy] = 1;
			$HnavyMove[$id][$x][$y] = 2;
			return 1;
		}
		$HnavyMove[$id][$sx][$sy] = 2;
	} elsif($land->[$sx][$sy] == $HlandNavy) {
		my($tId, $tTmp, $tStat, $tSea, $tExp, $tFlag, $tNo, $tKind, $tWait, $tHp, $tgoalx, $tgoaly) = navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]);
		logNavyMoveAttack($id, $name, $nId, "($x, $y)",  $nName, $tId, "($sx, $sy)",  landName($land->[$sx][$sy], $landValue->[$sx][$sy]));
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = $nSea;
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = $tSea;
		$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
		$HnavyMove[$id][$x][$y] = 2;
		$HnavyMove[$id][$sx][$sy] = 2;
		return 1;
	}
	# ��ư����Ϸ��ˤ���å�����
#	my($l)	 = $land->[$sx][$sy];
#	my($lv)	= $landValue->[$sx][$sy];
#	my($lName) = landName($l, $lv);
#	my($point) = "($sx, $sy)";

	$land->[$x][$y] = $HlandSea;
	$landValue->[$x][$y] = $nSea;
	$landValue2->[$x][$y] = 0;
	$HlandMove[$id][$x][$y] = 1;
	# ��ư
# ��ư����ݵƫ�����Τǥ����Ȥˤ��ޤ���
#	logNavyMoveSea($id, $name, $lName, $point, $nName, $nId);
#logdebug ($id, "code3($x, $y)");
	# ����õ��ǽ��
	if ($special & 0x100000) {
		my(@x, @y);
		if($HedgeReclaim) {
			my($map) = $island->{'map'};
			@x = @{$map->{'x'}};
			@y = @{$map->{'y'}};
		}
		if (random(1000) < $Hoilp[$nKind]) { # ��Ψ0.2%
			# ����ȯ����
			$land->[$x][$y] = $HlandOil;
			$landValue->[$x][$y] = 0;
			my $str = $Hoilp[$nKind] * $HcomCost[$HcomDestroy];
			logOilFound($id, $name, "($x, $y)", "����õ��", "$str$HunitMoney");
		} elsif(random(2000) < $Hoilp[$nKind]) { # ��Ψ0.1%(����ȯ����Ψ��0.5��)
			# ����ȯ����
			my $value = ($Hoilp[$nKind] * $HcomCost[$HcomDestroy]); # �����ݾ�(^^��
			$value += random(10 * $Hoilp[$nKind] * $HcomCost[$HcomDestroy]); # ��̿�Υ롼��å�(^��^)
			if(defined $nn) {
				$nIsland->{'money'} += $value ;
				logTansaku($id, $name, $nId, $nName, "($x, $y)", "$value$HunitMoney");
			}
		} elsif((random(4000) < $Hoilp[$nKind]) && (!$HedgeReclaim ||
			($HedgeReclaim && !(($x < $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim))) # ��κǳ��������Ω���ԲĤˤ�����
			)) { # ��Ψ0.05%(����ȯ����Ψ��0.25��)
			# ����л�ʮ��
			my($landKind, $lv, $point);
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$point = "($x, $y)";
			$land->[$x][$y] = $HlandMountain;
			$landValue->[$x][$y] = 0;
			if(defined $nn) {
				$nIsland->{'shipk'}[$nKind]--;
				$nIsland->{'ships'}[$nNo]--;
				$nIsland->{'ships'}[4]--;
				# ���Х��Х�
				$nIsland->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
			}

			foreach $i (1..6) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				# �Ԥˤ�����Ĵ��
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];
				# �ϰϳ�
				next if(($sx < 0) || ($sy < 0));

				# �ϰ���ξ��
				$landKind = $land->[$sx][$sy];
				$lv = $landValue->[$sx][$sy];
				$lv2 = $landValue2->[$sx][$sy];
				$point = "($sx, $sy)";
				if(($landKind == $HlandSea) || ($landKind == $HlandOil)) {
					# �������Ĥξ��
					if(!$lv || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
						logEruptionSea($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandSea;
						$landValue->[$sx][$sy] = 1;
						next;
					} else {
						# ����
						logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					}
				} elsif(($landKind == $HlandSeaMine) || ($landKind == $HlandSbase) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
					# ���롢���𡤳��쥳���ξ��
					logEruptionSea($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandSea;
					$landValue->[$sx][$sy] = 1;
					next;
				} elsif(($landKind == $HlandMountain) || ($landKind == $HlandWaste)) {
					next;
				} elsif($landKind == $HlandComplex) {
					# ʣ���Ϸ��ʤ������Ϸ�
					my $cKind = (landUnpack($lv))[1];
					next if($HcomplexAfter[$cKind]->{'eruption'}[0] eq '');
					$land->[$sx][$sy] = $HcomplexAfter[$cKind]->{'eruption'}[0];
					$landValue->[$sx][$sy] = $HcomplexAfter[$cKind]->{'eruption'}[1];
					$island->{'complex'}[$cKind]--;
					logEruptionNormal($id, $name, landName($landKind, $lv), $point);
					next;
				} elsif(($landKind == $HlandMonster) || ($landKind == $HlandHugeMonster)) {
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
					if((($mFlag & 2) && !$mSea) || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
						logEruptionSea3($id, $name, landName($landKind, $lv), $point);
						$mSea = 1;
					} else {
						logEruptionSea2($id, $name, landName($landKind, $lv), $point);
						$mFlag &= ~2;
						$mSea = 0;
					}
					$landValue->[$sx][$sy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
					next;
				} elsif($landKind == $HlandNavy) {
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
					my $nSpecial = $HnavySpecial[$nKind];
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
					if ($nSpecial & 0x8) {
						# ����Φ��
						logEruptionSea1($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandWaste;
						$landValue->[$sx][$sy] = 0;
						$Hislands[$n]->{'navyPort'}-- if(defined $n);
					} else {
						if(!$nSea || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
							# ����¾������
							logEruptionSea($id, $name, landName($landKind, $lv), $point);
							$land->[$sx][$sy] = $HlandSea;
							$landValue->[$sx][$sy] = 1;
						} else {
							# ������Φ��
							logEruptionSea1($id, $name, landName($landKind, $lv), $point);
							$land->[$sx][$sy] = $HlandWaste;
							$landValue->[$sx][$sy] = 0;
						}
						if(defined $n) {
							$Hislands[$n]->{'ships'}[$nNo]--;
							$Hislands[$n]->{'ships'}[4]--;
						}
						$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
					}
					next;
				} else {
					# ����ʳ��ξ��
					logEruptionNormal($id, $name, landName($landKind, $lv), $point);
				}
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
			}
			logEruption($id, $name, landName($land->[$x][$y], $landValue->[$x][$y]), "($x, $y)");
			$HnavyMove[$id][$x][$y] = 2;
			return;
		}
	}

	if($land->[$sx][$sy] == $HlandSeaMine) {
	# ����ʤ��ѵ��ϸ���
		$nHp -= $landValue->[$sx][$sy];
		# ������
		if($nHp > 0) {
			logSeaMineDamage($id, $name, $nId, "($sx, $sy)", $nName);
#		} elsif($nHp == 0) {
#			logSeaMineDestroy($id, $name, $nId, "($sx, $sy)", $nName);
		} else {
			logSeaMineDestroy($id, $name, $nId, "($sx, $sy)", $nName);
		}
	} elsif($land->[$sx][$sy] == $HlandSea) {
		$nSea = $landValue->[$sx][$sy];
	} elsif($land->[$sx][$sy] == $HlandWaste) {
		$nSea = 1;
	}

	if($nHp > 0) {
		# ��±ǽ��
		if ((defined $nn) && ($special & 0x40000) && ($id != $nId)) {
			my($i, $j, $ssx, $ssy);
			my $nPoint = "($sx, $sy)";
			for($j = 0; $j < $HpiratesHex[$nKind]; $j++) {
				for($i = $an[$j]; $i < $an[$j+1]; $i++) {
					$ssx = $sx + $ax[$i];
					$ssy = $sy + $ay[$i];
					# �Ԥˤ�����Ĵ��
					$ssx-- if(!($ssy % 2) && ($sy % 2));
					$ssx = $correctX[$ssx + $#an];
					$ssy = $correctY[$ssy + $#an];
					# �ϰϳ�
					next if(($ssx < 0) || ($ssy < 0));

					my($landKind, $lv, $point, $value);
					$landKind = $land->[$ssx][$ssy];
					$lv = $landValue->[$ssx][$ssy];
					$lv2 = $landValue2->[$ssx][$ssy];
					$point = "($ssx, $ssy)";

					# �ϰ���ξ��
					if($landKind == $HlandFarm) {
						$value = int($lv * 10 / 2); # ���Ϥ�Ⱦʬ�ο���
						next if(random(100) >= 50 - ($j * 20)); # 1Hex��50%,2Hex30%,3Hex10%
						$nIsland->{'food'} += $value;
						$island->{'food'} -= $value;
						logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagFood_}$value$HunitFood${H_tagFood}");
					} elsif($landKind == $HlandFactory) {
						$value = int($lv / 2); # ���Ϥ�Ⱦʬ�λ��
						next if(random(100) >= 50 - ($j * 20)); # 1Hex��50%,2Hex30%,3Hex10%
						$nIsland->{'money'} += $value;
						$island->{'money'} -= $value;
						logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagMoney_}$value$HunitMoney${H_tagMoney}");
					} elsif($landKind == $HlandComplex) {
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
						if($cFood && (random(100) >= 50 - ($j * 20))) { # 1Hex��50%,2Hex30%,3Hex10%
							my $food = $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
							$food  = int($food / 2); # ���Ϥ�Ⱦʬ�ο���
							$nIsland->{'food'} += $food;
							$island->{'food'} -= $food;
							logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagFood_}$food$HunitFood${H_tagFood}");
						} elsif($cMoney && (random(100) >= 50 - ($j * 20))) { # 1Hex��50%,2Hex30%,3Hex10%
							my $money = $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
							$money = int($money / 2); # ���Ϥ�Ⱦʬ�λ��
							$nIsland->{'money'} += $money;
							$island->{'money'} -= $money;
							logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagMoney_}$money$HunitMoney${H_tagMoney}");
						}
					}
				}
			}
		}
		$land->[$sx][$sy] = $HlandNavy;
		($landValue->[$sx][$sy], $landValue2->[$sx][$sy]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
	} elsif($nHp == 0) {
	# �ĳ��ˤʤ�
		$land->[$sx][$sy] = $HlandNavy;
		($landValue->[$sx][$sy], $landValue2->[$sx][$sy]) = navyPack(0, $nTmp, $nStat, $nSea, int(rand(90)) + 10, 1, 0, $nKind, 0, 0, 31, 31);
		if(defined $nn) {
			$nIsland->{'shipk'}[$nKind]--;
			$nIsland->{'ships'}[$nNo]--;
			$nIsland->{'ships'}[4]--;
		}
	} else {
	# ����
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = $nSea;
		$HlandMove[$id][$sx][$sy] = 1;
		$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
		if(defined $nn) {
			$nIsland->{'shipk'}[$nKind]--;
			$nIsland->{'ships'}[$nNo]--;
			$nIsland->{'ships'}[4]--;
			# ���Х��Х�
			$nIsland->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		}
	}

	# ��ư�Ѥߥե饰
	if ($special & 0x2) {
		# �ȤƤ�®����ư
		# ��ư�Ѥߥե饰��Ω�Ƥʤ�
	} elsif ($special & 0x1) {
		# ®����ư
		$HnavyMove[$id][$sx][$sy] = $HnavyMove[$id][$x][$y] + 1;
	} else {
		# ���̤ΰ�ư
		$HnavyMove[$id][$sx][$sy] = 2;
	}
	$HnavyMoveCount[$id][$sx][$sy] = 1;
#	undef $HlandMove[$id][$sx][$sy];
	return 1;
}

# ��û��Υ�ˤ�����ɸ�Ϸ���������׻�����
sub searchTarget {
	my($id, $island, $x, $y, $range, @kind) = @_;

	# �ϰ������ɸ�Ϸ���õ��
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($tx, $ty) = ($x, $y);
	my($i, $sx, $sy, %kflag);
	foreach (@kind) {
		$kflag{$_} = 1;
	}
	my $rn = $range - 1;
	foreach $i (0..$rn) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ�
		next if(($sx < 0) || ($sy < 0));

		# �ϰ���ξ��
		if ($kflag{$land->[$sx][$sy]}) {
			if($id != 0){
				# �����Ǥμ��Ф�
				my($nId, $nNo, $nKind) = (navyUnpack($landValue->[$x][$y], 0))[0, 6, 7];
				my $special = $HnavySpecial[$nKind];

				# ����δ�����
				next if($nId != $id);

				# ���Ϥ���ʤ���
				next if(!($special & 0x80));
			}
			$tx = $sx;
			$ty = $sy;
			last;
		}
	}

	# ��ư������׻�����
	my $dy = ($ty > $y) ? 2 : ($ty < $y) ? 0 : 1;

	if ($tx < $x) {
		return (6, 5, 4)[$dy];
	} elsif ($tx > $x) {
		return (1, 2, 3)[$dy];
	} else {
		return ((rand(1) < .5 ? 1 : 6), 0, (rand(1) < .5 ? 3 : 4))[$dy];
	}
}

# �����ι�����ɸ��õ��
sub searchNavyTarget {
	my($island, $x, $y) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($lv)        = $landValue->[$x][$y];
	my($lv2)        = $landValue2->[$x][$y];

	my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
	my $nNum = $HidToNumber{$nId};
	my($nIsland, $n, $targetMission, %mission);
	if(defined $nNum) {
		$nIsland = $Hislands[$nNum];
		# ���ƹ������
		my($comArray) = $nIsland->{'command'};
		my($cflag) = 0;
		my($p) = 1;
		for($n = 0; $n < $HcommandMax; $n++) {
			my($command) = $comArray->[$n];
#HdebugOut("[for] ($command->{'kind'} == $HcomNavyTarget) && ($command->{'target'} == $id)\n");
			if(($command->{'kind'} == $HcomNavyTarget) && ($command->{'target'} == $id)) {
				$mission{"$command->{'x'},$command->{'y'}"} = $p;
#HdebugOut("[if] mission,$id,$command->{'x'},$command->{'y'}\n");
			}
			last if($HcomTurn[$command->{'kind'}]);
			$p++;
		}
	}
	my(%amityFlag);
	$amityFlag{$nId} = 1;
	my $nSpecial = $HnavySpecial[$nKind];
	my $rflag = ((defined $nNum) && (!$HitemInvalid || !$island->{'field'})) ? $nIsland->{'itemAbility'}[4] : 0;
	$rflag += $HnavyFireBF[2] if($island->{'field'});
	my $tmp = $HnavyFireRange[$nKind] + $rflag;
	$tmp = ($tmp > 8) ? 8 : ($tmp <= 0) ? 1 : int($tmp);
	my $range = $an[$tmp];
	my @HmyPriority = @Hpriority;
	my($amity, $mypri);
	if(defined $nNum) {
		if(!$HamityInvalid || !$island->{'field'}) {
			$amity = $Hislands[$nNum]->{'amity'};
			foreach (@$amity) {
				$amityFlag{$_} = 1;
			}
		}
		$mypri = $Hislands[$nNum]->{'priority'};
		@HmyPriority = @Hpriority[split(/\-/, $mypri->[$nNo])];
	}
	my(%targetTmp);

	# �ϰ������ɸ�Ϸ���õ��
	my($i, $j, $sx, $sy, $kind, $tId, $tLv);
	my $rn = $range - 2;
	my(@order) = randomArray($rn);
	my($missionflag) = 0;
	foreach $j (0..$rn) {
		if($Hnearfar == 1) {
			$i = $range - 1 - $j;
		} elsif($Hnearfar == 2) {
			$i = $order[$j] + 1;
		} else {
			$i = $j + 1;
		}
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ�
		next if(($sx < 0) || ($sy < 0));

		# �ϰ���ξ��
		$tKind = $land->[$sx][$sy];
		$tLv   = $landValue->[$sx][$sy];
		$tLv2  = $landValue2->[$sx][$sy];

		my $target = { 'x' => $sx, 'y' => $sy };

		next if(($tKind != $HlandMonster) && ($tKind != $HlandHugeMonster) && ($nStat > 1));

                # ��������֤ϲ��ä����������åȤˤǤ��ʤ�
                if(($HvsMonster[$nKind] == 1) && ($tKind != $HlandMonster)){
                    next;
                }

                # �����۹𤷤Ƥʤ��ä��顢̱�������оݳ�
#		foreach (@$amity) {
#			$amityFlag{$_} = 1;
#		}
#		if(!$amityFlag{$ttarget}) { 
#                    if ($tKind == $HlandNavy) {
#			my ($tId, $nKind) = (navyUnpack($tLv,0))[0, 7];
#                        if($Hprivate[$nKind] == 1){
#logdebug ($id, "code1");
#                            next;
#                        }
#                    }
#                }

		if ($nSpecial & 0x100) {
			# ��������
			$target->{special} = 0x100;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# ���ƹ����ǽ
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# ����
				($tId, $nFlag) = (navyUnpack($tLv,0))[0, 5];
				# ͧ����
				if(!$amityFlag{$tId}) {
					# ̣���δ����ǤϤʤ�
					if ($nFlag == 2) {
						# ���夷�Ƥ�
						# ������ɸ����
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					if(int($tLv / 10000) >= 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif (($tKind == $HlandSbase) || # �������
					($tKind == $HlandOil)) {   # ��������
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					$targetTmp{($tKind == $HlandSbase ? 'Arm' : 'Money')} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) { # ʣ���Ϸ�
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x100) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# ����
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# ͧ����
				if(!$amityFlag{$tId}) {
					# ̣�����ɸ����äǤϤʤ�
					if ($nFlag & 2) {
						# ���ˤ��뤫
						# ������ɸ����
						$targetTmp{($tKind == $HlandMonster ? 'Monster' : 'HugeMonster')} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x200) {
			# �дϹ���
			$target->{special} = 0x200;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# ���ƹ����ǽ
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# ����
				($tId, $nFlag, $nKind) = (navyUnpack($tLv,0))[0, 5, 7];
				# ͧ����
				if(!$amityFlag{$tId}) {
					# ̣���δ����ǤϤʤ�
					if (($nFlag != 2) && !$HnavyCruiseTurn[$nKind]) {
						# ����ǤϤʤ����Ҷ����Ǥ�ʤ�
						# ������ɸ����
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					if(int($tLv / 10000) == 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandOil) { # ��������
				# ͧ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					$targetTmp{'Money'} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) {
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x200) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif ($tKind == $HlandHugeMonster) {
				# �������
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# ͧ����
				if(!$amityFlag{$tId}) {
					if ($nFlag & 2) {
						# ���ˤ��뤫
						# ������ɸ����
						$targetTmp{'HugeMonster'} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x400) {
			# ���Ϲ���
			$target->{special} = 0x400;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# ���ƹ����ǽ
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if (($tKind == $HlandTown)     || # Į��
				($tKind == $HlandForest)   || # ��
				($tKind == $HlandFarm)     || # ����
				($tKind == $HlandFactory)  || # ����
				($tKind == $HlandComplex)  || # ʣ���Ϸ�
				($tKind == $HlandBase)     || # �ߥ��������
				($tKind == $HlandDefence)  || # �ɱһ���
				($tKind == $HlandMonument) || # ��ǰ��
				($tKind == $HlandHaribote)) { # �ϥ�ܥ�
				# ͧ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					if($tKind == $HlandTown) {
						$targetTmp{'Pop'} = $target;
						next;
					} elsif($tKind == $HlandFarm) {
						$targetTmp{'Food'} = $target;
						next;
					} elsif($tKind == $HlandFactory) {
						$targetTmp{'Money'} = $target;
						next;
					} elsif($tKind == $HlandComplex) {
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
						if($HcomplexAttr[$cKind] & 0x400) {
							$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
							$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
							next;
						}
					} elsif(($tKind == $HlandBase) || ($tKind == $HlandHaribote) || (!$HdBaseHide && ($tKind == $HlandDefence))) {
						$targetTmp{'Arm'} = $target;
						next;
					} else {
						$targetTmp{'Other'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					if(!(int($tLv / 10000))) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# ����
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# ͧ����
				if(!$amityFlag{$tId}) {
					# Φ�ˤ��뤫��
					unless ($nFlag & 2) {
						# ������ɸ����
						$targetTmp{($tKind == $HlandMonster ? 'Monster' : 'HugeMonster')} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x800) {
			# �ж�����
			$target->{special} = 0x800;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# ���ƹ����ǽ
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# ����
				($tId, $nFlag, $nKind) = (navyUnpack($tLv,0))[0, 5, 7];
				# ͧ����
				if(!$amityFlag{$tId}) {
					# ̣���δ����ǤϤʤ�
					if ($HnavyCruiseTurn[$nKind]) {
						# �Ҷ����Τ�
						# ������ɸ����
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					if(int($tLv / 10000) == 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandOil) { # ��������
				# ͧ����
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					# ������ɸ����
					$targetTmp{'Money'} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) {
				if(!$amityFlag{$id}) {
					# ̣���λ��ߤǤϤʤ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x200) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif ($tKind == $HlandHugeMonster) {
				# �������
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# ͧ����
				if(!$amityFlag{$tId}) {
					if ($nFlag & 2) {
						# ���ˤ��뤫
						# ������ɸ����
						$targetTmp{'HugeMonster'} = $target;
						next;
					}
				}
			}
		}


	} # for
	return if((keys %targetTmp) eq ());
	foreach ('Mission', @HmyPriority) {
		if(defined $targetTmp{$_}) {
			$HnavyAttackTarget{"$id,$x,$y"} = $targetTmp{$_};
			$nIsland->{"mission,$id,$targetTmp{$_}->{'x'},$targetTmp{$_}->{'y'}"} .= " <B>$HnavyName[$nKind]</B>${HtagName_}($x, $y)${H_tagName}" if((defined $nNum) && ($_ eq 'Mission'));
#			$nIsland->{"missionset,$id,$x,$y"} = 1 if((defined $nNum) && ($_ eq 'Mission'));
#			HdebugOut("====> missionset,$id,$x,$y\n") if((defined $nNum) && ($_ eq 'Mission'));
			return;
		}
	}
	$HnavyAttackTarget{"$id,$x,$y"} = undef;
	return;
}

# �����ι���
sub navyAttack {
	my($island, $x, $y, $tx, $ty, $tSpecial) = @_;

	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($tLandName) = landName($land->[$tx][$ty], $landValue->[$tx][$ty]);
	$tLandName = ($HlandMove[$id][$tx][$ty]) ? "${HtagName2_}${tLandName}${H_tagName2}" : "${HtagName_}${tLandName}${H_tagName}";
	my($landKind)  = $land->[$x][$y];
	my($lv)        = $landValue->[$x][$y];
	my($lv2)       = $landValue2->[$x][$y];

	my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
	my $nn  = $HidToNumber{$nId};
	my $nSpecial = $HnavySpecial[$nKind];
	my $nName    = landName($landKind, $lv);
	my $nPoint   = "($x, $y)";
	my $tPoint   = "($tx, $ty)";
	my($nIsland, %amityFlag, @noDefenceIds);
	if(defined $nn) {
		$nIsland = $Hislands[$nn];
		if($HnavySafetyZone) {
			$amityFlag{$nId} = 1;
			if(($HnavySafetyZone == 2) && (!$HamityInvalid || !$island->{'field'})) {
				foreach (@{$nIsland->{'amity'}}) {
					$amityFlag{$_} = 1;
				}
			}
		}
		if($HdBaseSelfNoDefenceNV == 1) {
			@noDefenceIds = ($nId);
		} elsif($HdBaseSelfNoDefenceNV == 2) {
			@noDefenceIds = ($nId, @{$nIsland->{'amityBy'}});
		} elsif($HdBaseSelfNoDefenceNV == 3) {
			@noDefenceIds = ($nId, @{$nIsland->{'amity'}});
		} elsif($HdBaseSelfNoDefenceNV == 4) {
			@noDefenceIds = ($nId, @{$nIsland->{'amity'}}, @{$nIsland->{'amityBy'}});
		} else {
			@noDefenceIds = (0);
		}
	}
	# ��̱�ο�
	my($boat) = 0;

	# ʼ������
	my @arms;
	my $n;
	if ($tSpecial & 0x100) {
		# ��������
		$n = 0x1000;
	} elsif ($tSpecial & 0x200) {
		# �дϹ���
		push(@arms, 0x1000) if ($nSpecial & 0x1000);
		push(@arms, 0x2000) if ($nSpecial & 0x2000);
		push(@arms, 0x4000) if ($nSpecial & 0x4000);
		$n = $arms[int(rand($#arms + 1))];
	} elsif ($tSpecial & 0x400) {
		# ���Ϲ���
		push(@arms, 0x2000) if ($nSpecial & 0x2000);
		push(@arms, 0x4000) if ($nSpecial & 0x4000);
		$n = $arms[int(rand($#arms + 1))];
	}

	# �����
	my $rflag = $HnavyFireHex[$nKind] + $HnavyFireBF[1];
	$rflag = ($rflag > $#an) ? $#an : ($rflag < 0) ? 0 : int($rflag);
	my $rpflag = 0;
	my $err1 = $an[$rflag];
	my $err2;
	if($rflag) {
	 	$err2 = $an[$rflag - 1];
		if($nSpecial & 0x4000000) {
			$rpflag = $Hfirehexp[$nKind];
		} elsif(!$HitemInvalid || !$island->{'field'}) {
			$rpflag = $nIsland->{'itemAbility'}[5];
		}
	}
	# ������
	my $nFire = $HnavyFire[$nKind];
	my $fflag = ((defined $nn) && (!$HitemInvalid || !$island->{'field'})) ? $nIsland->{'itemAbility'}[11] : 1;
	$nFire *= $fflag;
	$nFire += $HnavyFireBF[0] if($island->{'field'});
	$nFire = int($nFire);
	$nFire = 1 if($nFire < 1);
	# �˲���
	my $damage = int(random($HnavyDamage[$nKind] * (120 + $nExp)/120));
#	if(($nSpecial & 0x10000000) && (rand(100) < $Hdamagep[$nKind])) {
#		$damage = int(rand($HdamageMax[$nKind]) + 1);
#	}
	$damage += $HnavyFireBF[3] if($island->{'field'});
	if((defined $nn) && (!$HitemInvalid || !$island->{'field'})) {
		$damage *= $nIsland->{'itemAbility'}[12];
		$damage += $nIsland->{'itemAbility'}[24];
	}
	$damage = int($damage + 0.5);
	$damage = 1 if($damage < 1);
	# ����������γȻ��ϰ�
	my $range = 0;

	# ���ƹ���
#	if($nIsland->{"missionset,$id,$x,$y"}) {
#HdebugOut("[fire] missionset,$id,$x,$y => mission,$id,$tx,$ty\n");
#		$nIsland->{"mission,$id,$tx,$ty"} .= " <B>$HnavyName[$nKind]</B>${HtagName_}($x, $y)${H_tagName}";
#	}

	# ���⤹��
	my($r, $err, $xx, $yy, $fx, $fy, $fPoint, $fName, $fKind, $fLv, @pointErr, @terrorPnt);
	my(%damageId);
	my $loopflag = 0;
	my $fire = 0;
	while ($fire < $nFire) {
		last if($loopflag); # ������­���ĳ��ǹ��⽪λ

		# ����������
		if($rpflag && (rand(100) < $rpflag)) {
			$err = $err2;
		} else {
			$err = $err1;
		}
		$r = int(rand($err));
		$xx = $tx + $ax[$r];
		$yy = $ty + $ay[$r];
		# �Ԥˤ�����Ĵ��
		$xx-- if(!($yy % 2) && ($ty % 2));
		$xx = $correctX[$xx + $#an];
		$yy = $correctY[$yy + $#an];
		if(!$HnavySelfAttack && ($xx == $x) && ($yy == $y)) {
			$r += int(1 + rand($err-1));
			$r -= $err if($r >= $err);
			# �Ԥˤ�����Ĵ��
			$xx = $tx + $ax[$r];
			$yy = $ty + $ay[$r];
			$xx-- if(!($yy % 2) && ($ty % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];
		}

		if($nSpecial & 0x20000000) {
			if (($xx < 0) || ($yy < 0)) {
				# �ϰϳ��ξ�硢������⤷�ʤ�
				$range = 0;
			} else {
				push(@terrorPnt, "($xx, $yy)");
				$range = $an[$HnavyTerrorHex[$nKind]] - 1;
			}
		}
		my(@order) = randomArray($range + 1);
		foreach my $loop (0..$range) {

			($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$x][$y], $landValue2->[$x][$y]);
			# �ĳ������ˤʤäƤ��顢���⽪λ(�����������硢ɬ��)
			#return ($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) if($nHp == 0);
			if($nHp == 0) {
				$loopflag = 1;
				last;
			}

			# ���깶������λ
			last if($fire >= $nFire);

			# �������Ѥ����
			if(defined $nn) {
				$nIsland->{'money'} -= $HnavyShellCost[$nKind];
				if ( ($nIsland->{'money'} < 0) &&
					(($HnavyUnknown && ($nId != 0)) || !$HnavyUnknown) ) {
					# �������Ѥ�­��ʤ�
					$nIsland->{'money'} = 0;
					$nIsland->{'shellMoney'} -= $nIsland->{'money'};
					logNavyNoShell($id, $nId, $name, $nPoint, $nName);
					$loopflag = 1;
					last;
				} else {
					$nIsland->{'shellMoney'} += $HnavyShellCost[$nKind];
				}
				$nIsland->{'ext'}[1] += $HnavyShellCost[$nKind]; # �׸���
				$nIsland->{'ext'}[6]++;
				if($HallyNumber) {
					foreach (@{$nIsland->{'allyId'}}) {
						$Hally[$HidToAllyNumber{$_}]->{'ext'}[0]++;
					}
					foreach (@{$island->{'allyId'}}) {
						$Hally[$HidToAllyNumber{$_}]->{'ext'}[1]++;
					}
				}
			}

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
				$island->{'ext'}[5]++; # �������ߥ�����ο�
				next;
			}
			$fKind  = $land->[$fx][$fy];
			$fLv    = $landValue->[$fx][$fy];
			$fLv2   = $landValue2->[$fx][$fy];
			$fName  = landName($fKind, $fLv);

			# �ɱһ���Ƚ��
			my($defence) = 0;
			my($defflag) = 1;
			# ̤Ƚ���ΰ�
#			if (($fKind == $HlandDefence) || countAroundComplex($island, $fx, $fy, $an[0], 0x40) ||
#				countAroundNavySpecial($island, $fx, $fy, 0x40, $an[0], 0)) {
#				# �ɱһ��ߤ�̿��
#				if ($fKind == $HlandDefence) { # �ɱһ��ߤ�
#					if($amityFlag{$id}) { # ̵����
#						if(random(100) < $HnavySafetyInvalidp) {
#							# �����Ψ�Ǹ���
#							push(@pointErr, { 'SS' => $fPoint });
#						} else {
#							push(@pointErr, { 'SZ' => $fPoint });
#							next;
#						}
#					}
#					# �ɱһ��ߤ��ѵ��Ϥ򲼤���
#					$defflag = ($fLv % 100) - $damage;
#					$fLv -= $damage;
#					if($defflag < 0) {
#						$island->{'dbase'}--;
#						$nIsland->{'ext'}[2]++ if(defined $nn); # �˲������ɱһ��ߤο�
#					}
#				}
#			} elsif (countAroundDef($id, $island, $fx, $fy, 0x40, @noDefenceIds)) {
#				# �ɱ��ϰ�
#				$defence = 1;
#			}

                        # �ɱ�Ƚ��
                        if (countAroundDef($id, $island, $fx, $fy, 0x40, @noDefenceIds)) {
				# 
				$defence = 1;
			}


			if ($defence) {
				# �ɱҤ��줿
				if ($n == 0x1000) {
					# ���롡���������дϡ�
					# ������ɱҤ��ʤ�
# �ɱҤ������Ȥ��ϥ����Ȥ򳰤�����
#					push(@pointErr, { 'DF' => $fPoint });
#					$island->{'ext'}[7]++;
#					next;
				} elsif ($n == 0x2000) {
					# ��ˤ�����дϡ����ϡ�
					push(@pointErr, { 'DF' => $fPoint });
					$island->{'ext'}[7]++;
					next;
				} elsif ($n == 0x4000) {
					# �Ϻܵ����дϡ����ϡ�
					push(@pointErr, { 'DF' => $fPoint });
					$island->{'ext'}[7]++;
					next;
				}
			}

			# ���̤Τʤ��Ϸ�
			if ($n == 0x1000) {
				# ���롡���������дϡ�
				if (($fKind == $HlandSea)      || # ��
					($fKind == $HlandWaste)    || # ����
					($fKind == $HlandPlains)   || # ʿ��
					($fKind == $HlandTown)     || # Į��
					($fKind == $HlandForest)   || # ��
					($fKind == $HlandFarm)     || # ����
					($fKind == $HlandFactory)  || # ����
					($fKind == $HlandBase)     || # �ߥ��������
					($fKind == $HlandDefence)  || # �ɱһ���
					($fKind == $HlandMountain) || # ��
					($fKind == $HlandMonument) || # ��ǰ��
					($fKind == $HlandHaribote)) { # �ϥ�ܥ�
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
			} elsif ($n == 0x2000) {
				# ��ˤ�����дϡ����ϡ�
				if (($fKind == $HlandSea)      || # ��
					($fKind == $HlandMountain) || # ��
					($fKind == $HlandWaste)    || # ����
					($fKind == $HlandSbase)) {    # �������
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}

				if ($fKind == $HlandNavy){ # ����
 				    my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
                                    if($HnavyCruiseTurn[$nkind2]){ # �Ҷ����ξ��
                                    	push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
                                    }
                                }


			} elsif ($n == 0x4000) {
				# �Ϻܵ����дϡ����ϡ�
				if (($fKind == $HlandSea)      || # ��
					($fKind == $HlandMountain) || # ��
					($fKind == $HlandWaste)    || # ����
					($fKind == $HlandSbase)) {    # �������
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}

				if ($fKind == $HlandNavy){ # ����
 				    my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
                                    if($HnavyCruiseTurn[$nkind2]){ # �Ҷ����ξ��
                                    	push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
                                    }
                                }
			}

			# ���������á�������ðʳ���̵����
			if($amityFlag{$id} && $fKind != $HlandNavy && $fKind != $HlandMonster && $fKind != $HlandHugeMonster) {
				if(random(100) < $HnavySafetyInvalidp) {
					# �����Ψ�Ǹ���
					push(@pointErr, { 'SS' => $fPoint });
				} else {
					push(@pointErr, { 'SZ' => $fPoint });
					next;
				}
			}

			# ���̤��Ϸ�
			if ($fKind == $HlandComplex) {  # ʣ���Ϸ�
				$island->{'ext'}[5]++;
				my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($fLv);
				# ���̤Τ����Ϸ�
				if( (defined  $HcomplexAfter[$cKind]->{'attack'}[0]) &&
					( (($n == 0x1000) && ($HcomplexAttr[$cKind] & 0x300)) || # ���롡���������дϡ�
					(($n == 0x2000) && ($HcomplexAttr[$cKind] & 0x600)) ||   # ��ˤ�����дϡ����ϡ�
					(($n == 0x4000) && ($HcomplexAttr[$cKind] & 0x600)) )    # �Ϻܵ����дϡ����ϡ�
				  ) {
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
					$island->{'complex'}[$cKind]--;
					$HlandMove[$id][$fx][$fy] = 1;

					if ($n == 0x1000) {
						# ���롡���������дϡ�
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} elsif (($n == 0x2000) || ($n == 0x4000)) {
						# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
						logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					}
					next;
				}
				# ���̤Τʤ��Ϸ�
				push(@pointErr, { 'ND' => $fPoint });
				next;
			} elsif ($fKind == $HlandMonster) {  # ����
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($fLv);
				my $mName = landName($fKind, $fLv);
				my $mn = $HidToNumber{$mId};
				if(defined $mn) {
					my $mIsland = $Hislands[$mIsland];
					$mIsland->{'ext'}[5]++ if(defined $mIsland);
				}
				# �����桩
				if ($mFlag & 2) {
					# ������
					if (($n == 0x2000) || ($n == 0x4000)) {
						# ��ˤ�����дϡ����ϡ� �Ϻܵ����дϡ����ϡ�
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				} else {
					# ������Ǥʤ�
					if ($n == 0x1000) {
						# ���롡���������дϡ�
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				}

				# �Ų��桩
				if ($mFlag & 1) {
					# �Ų���
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# �Ų��椸��ʤ�
					if($amityFlag{$mId}) { # ̵����
						if(random(100) < $HnavySafetyInvalidp) {
							# �����Ψ�Ǹ���
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $nId));
                                        if($nKind == 5){
                                            $Hislands[$HidToNumber{$nId}]->{'food'} += $damage * 10000;
                                        }
					if ($mHp <= $damage) {
						# ���ä��Ȥ᤿
						# �и���
						$nExp += $HmonsterExp[$mKind];
						$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
						($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
						if(defined $nn) {
							$nIsland->{'gain'} += $HmonsterExp[$mKind];
							if($island->{'event'}[1] <= $HislandTurn) {
								if($island->{'event'}[6] == 2) {
									# �����и��ͳ���
									$nIsland->{'epoint'}{$id} += $HmonsterExp[$mKind];
								} elsif($island->{'event'}[6] == 4) {
									# �����༣
									$nIsland->{'epoint'}{$id}++;
								} elsif($island->{'event'}[6] == 5) {
									# �޶�Ԥ�
									$nIsland->{'epoint'}{$id} += $HmonsterValue[$mKind];
								}
							}
						}

						if ($n == 0x1000) {
							# ���롡���������дϡ�
							if ($mFlag & 2) {
								# ������
								logNavyTorpedoMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
							}
						} elsif (($n == 0x2000) || ($n == 0x4000)) {
							# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
							logNavyMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						}
						$HlandMove[$id][$fx][$fy] = 1;


						if (defined $nn) {
							# ����
							my($value) = $HmonsterValue[$mKind];
							if ($value > 0) {
								$nIsland->{'money'} += $value;
								logMonMoney($nId, $mName, $value);
							}
							# �޴ط�
							my($prize) = $nIsland->{'prize'};
							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
							$monsters |= (2 ** $mKind);
							$nIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# �����༣��
							$nIsland->{'monsterkill'}++;
							# �����ƥ����Ƚ��
							if($HitemRest && $HitemGetDenominator2 && (random($HitemGetDenominator2) < $nIsland->{'gain'})) {
								my $num = @Hitem;
								$num = random($num);
								push(@{$nIsland->{'item'}}, $Hitem[$num]);
								$HitemGetId[$Hitem[$num]]{$nId} = 1;
								$HitemRest--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$Hitem[$num]], "$mName�����⤫��");
								splice(@Hitem, $num, 1);
							}
						}

					} else {
						# ���������Ƥ�
						logNavyMonster($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);

						# HP��1����
						#$landValue->[$fx][$fy] -= $damage;
						$mHp -= $damage;
						if($mHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
							next;
						}
						next;
					}
				}
			} elsif ($fKind == $HlandHugeMonster) {  # �������
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($fLv);
				my $mName = landName($fKind, $fLv);
				my $mn = $HidToNumber{$mId};
				if(defined $mn) {
					my $mIsland = $Hislands[$mIsland];
					$mIsland->{'ext'}[5]++ if(defined $mIsland);
				}
				# �����桩
				if ($mFlag & 2) {
					# ������
# ������äϳ��ˤ��Ƥ��ˤ���Ϻܵ��ǹ����ǽ���ԲĤˤ�����ϥ����Ȥ�Ϥ�����
#					if (($n == 0x2000) || ($n == 0x4000)) {
#						# ��ˤ�����дϡ����ϡ� �Ϻܵ����дϡ����ϡ�
#						push(@pointErr, { 'MS' => $fPoint });
#						next;
#					}
				} else {
					# ������Ǥʤ�
					if ($n == 0x1000) {
						# ���롡���������дϡ�
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				}

				# �Ų��桩
				if ($mFlag & 1) {
					# �Ų���
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# �Ų��椸��ʤ�
					if($amityFlag{$mId}) { # ̵����
						if(random(100) < $HnavySafetyInvalidp) {
							# �����Ψ�Ǹ���
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $nId));
					if (($mHp <= $damage) && ($mHflag == 0)) {
						# ���ä��Ȥ᤿
						# ������ý���
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$mKind][$j] eq '');
							$ssx = $fx + $ax[$j];
							$ssy = $fy + $ay[$j];
							# �Ԥˤ�����Ĵ��
							$ssx-- if(!($ssy % 2) && ($fy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# �ϰϳ�
							next if(($ssx < 0) || ($ssy < 0));

							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# �����Ǥμ��Ф�
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# �����μ��Ϥ��ĤäƤ����繶��̵��
							if($HhugeMonsterSpecial[$mKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							} elsif ($mFlag2 & 2) {
								# ���ˤ���
								$land->[$ssx][$ssy] = $HlandSea;
								$landValue->[$ssx][$ssy] = $mSea2;
							} else {
								# Φ�Ϥˤ���
								$land->[$ssx][$ssy] = $HlandWaste;
								$landValue->[$ssx][$ssy] = 0;
							}
							$HlandMove[$id][$ssx][$ssy] = 1;
						}
						next if($deflag);

						# �и���
						$nExp += $HhugeMonsterExp[$mKind];
						$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
						($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
						if(defined $nn) {
							$nIsland->{'gain'} += $HhugeMonsterExp[$mKind];
							if($island->{'event'}[1] <= $HislandTurn) {
								if($island->{'event'}[6] == 2) {
									# �����и��ͳ���
									$nIsland->{'epoint'}{$id} += $HhugeMonsterExp[$mKind];
								} elsif($island->{'event'}[6] == 4) {
									# �����༣
									$nIsland->{'epoint'}{$id}++;
								} elsif($island->{'event'}[6] == 5) {
									# �޶�Ԥ�
									$nIsland->{'epoint'}{$id} += $HhugeMonsterValue[$mKind];
								}
							}
						}

						if ($n == 0x1000) {
							# ���롡���������дϡ�
							if ($mFlag & 2) {
								# ������
								logNavyTorpedoMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
							}
						} elsif (($n == 0x2000) || ($n == 0x4000)) {
							# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
							logNavyMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						}
						$HlandMove[$id][$fx][$fy] = 1;


						if (defined $nn) {
							# ����
							my($value) = $HhugeMonsterValue[$mKind];
							if ($value > 0) {
								$nIsland->{'money'} += $value;
								logMonMoney($nId, $mName, $value);
							}
							# �޴ط�
							my($prize) = $nIsland->{'prize'};
							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
							$hmonsters |= (2 ** $mKind);
							$nIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# �����༣��
							$nIsland->{'monsterkill'}++;
							# �����ƥ����Ƚ��
							if($HitemRest && $HitemGetDenominator && (random($HitemGetDenominator) < $nIsland->{'gain'})) {
								my $num = @Hitem;
								$num = random($num);
								push(@{$nIsland->{'item'}}, $Hitem[$num]);
								$HitemGetId[$Hitem[$num]]{$nId} = 1;
								$HitemRest--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$Hitem[$num]], "$mName�����⤫��");
								splice(@Hitem, $num, 1);
							}
						}

					} else {
						# ���������Ƥ�
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$mKind][$j] eq '');
							$ssx = $fx + $ax[$j];
							$ssy = $fy + $ay[$j];
							# �Ԥˤ�����Ĵ��
							$ssx-- if(!($ssy % 2) && ($fy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# �ϰϳ�
							next if(($ssx < 0) || ($ssy < 0));

							next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
							# �����Ǥμ��Ф�
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# �����μ��Ϥ��ĤäƤ����繶��̵��
							if($HhugeMonsterSpecial[$mKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							}
						}
						next if($deflag);
						# HP������
						$mHp -= $damage;
						logNavyMonster($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						if($mHp > 0) {
							# ���������Ƥ�
							$landValue->[$fx][$fy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
							next;
						}
					}
					# �Τΰ������ä���
					if ($mFlag & 2) {
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
			} elsif ($fKind == $HlandNavy) { # ����
				my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
				my $nSpecial2 = $HnavySpecial[$nKind2];
				my $nName2 = landName($fKind, $fLv);
				my $nn2 = $HidToNumber{$nId2};
				my($nIsland2);
				$nIsland2 = $Hislands[$nn2] if (defined $nn2);

				if ($nFlag2 == 2) {
					# ������
					if (($n == 0x2000) || ($n == 0x4000)) {
						# ��ˤ�����дϡ����ϡ� �Ϻܵ����дϡ����ϡ�
						push(@pointErr, { 'FS' => $fPoint });
						next;
					}
				}

				# �ĳ���
				if ($nFlag2 == 1) {
					logNavyWreckDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nName2, $fPoint);

					# ���ˤʤ�
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = $nSea2;
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}

				if($amityFlag{$nId2}) { # ̵����
					if(random(100) < $HnavySafetyInvalidp) {
						# �����Ψ�Ǹ���
						push(@pointErr, { 'SS' => $fPoint });
					} else {
						push(@pointErr, { 'SZ' => $fPoint });
						next;
					}
				}

				if(defined $nn2) {
					if ($nId == $nId2) {
						# ̣���˷⤿�줿���׸��٥ޥ��ʥ�(�������ߥ�����ο��ϥ�����Ȥ��ʤ�)
						$nIsland2->{'ext'}[1] -= $HnavyShellCost[$nKind]; # �׸���
						#$nIsland2->{'ext'}[1] = 0 if($nIsland2->{'ext'}[1] < 0);
					} else {
						# Ũ�˷⤿�줿���׸��٥ץ饹
						$nIsland2->{'ext'}[1] += $HnavyShellCost[$nKind]; # �׸���
						$nIsland2->{'ext'}[5]++;
					}
				}

				$damageId{$nId2} = 1 if($nId2 && ($nId2 != $id) && ($nId2 != $nId));
				if ($nHp2 <= $damage) {
					# ����

					# �и���
					$nExp += $HnavyExp[$nKind2];
                                        $nExp += int($nExp2 / 2);
					$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
					($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
					if(defined $nn) {

                                                # ������и�����ư
                                                my $buildLevel  = gainToLevel($nIsland->{'gain'});
                                                my $buildLevel2 = gainToLevel($nIsland2->{'gain'});
                                                if($buildLevel < $buildLevel2){
                                                    # ��������¦�ηи��ͤ��㤤
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2] * ($buildLevel2 - $buildLevel + 1));
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2] * ($buildLevel2 - $buildLevel + 1)/2);
                                                }elsif($buildLevel > $buildLevel2){
                                                    # ��������¦�Τ��⤤
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2] / ($buildLevel - $buildLevel2 + 1));
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2] / ($buildLevel - $buildLevel2 + 1)/2);
                                                }else{
                                                    # Ʊ��
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2]);
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2]/2);
                                                }

						if($island->{'event'}[1] <= $HislandTurn) {
							if($island->{'event'}[6] == 2) {
								# �����и��ͳ���
								$nIsland->{'epoint'}{$id} += $HnavyExp[$nKind2];
							} elsif($island->{'event'}[6] == 3) {
								# ��������
								$nIsland->{'epoint'}{$id}++;
							}
						}
						# �����ƥ�å��Ƚ��
						if($HitemSeizeDenominator && $nIsland2->{'itemNumber'}) {
							if(($nIsland2->{'ships'}[4] + $nIsland2->{'navyPort'}) == 1) {
								foreach(shift @{$nIsland2->{'item'}}) {
									push(@{$nIsland->{'item'}}, $_);
									$HitemGetId[$_]{$nId2} = undef;
									$HitemGetId[$_]{$nId} = 1;
								}
								$nIsland->{'itemNumber'} += $nIsland2->{'itemNumber'};
								$nIsland2->{'itemNumber'} = 0;
								my $name2 = islandName($nIsland2);
								logItemGetLucky2($nId, $name, $fPoint, "${HtagName_}${name2}${H_tagName}����ͭ���Ƥ������٤Ƥ�$HitemName[0]", "���״ֺݤ�$nName2����");
							} elsif(random($HitemSeizeDenominator) < $nExp) {
								my $num = random($nIsland2->{'itemNumber'});
								push(@{$nIsland->{'item'}}, $nIsland2->{'item'}[$num]);
								$HitemGetId[$num]{$nId2} = undef;
								$HitemGetId[$num]{$nId} = 1;
								$nIsland->{'itemNumber'}++;
								$nIsland2->{'itemNumber'}--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$nIsland2->{'item'}[$num]], "���״ֺݤ�$nName2����");
								splice(@{$nIsland2->{'item'}}, $num, 1);
							}
						}
						$nIsland->{'ext'}[10]++;
						if($nId2 != $nId) {
							$nIsland->{'sink'}[$nKind2]++;
						} else {
							$nIsland->{'sinkself'}[$nKind2]++;
						}
					}

					if(defined $nn2) {
						$nIsland2->{'shipk'}[$nKind2]--;
						# ���Х��Х�
						$nIsland2->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					if ($nSpecial2 & 0x8) {
						# ��������
						logNavyPortDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

						# �����ˤʤ�
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = 1;
						$nIsland2->{'navyPort'}--;
					} else {
						# ��������
						logNavyShipDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

						if (rand(100) < $HnavyProbWreck[$nKind2]) {
							# �ĳ��ˤʤ�
							($landValue->[$fx][$fy], $landValue2->[$fx][$fy]) = navyPack(0, $nTmp2, $nStat2, $nSea2, int(rand(90)) + 10, 1, 0, $nKind2, 0, 0, 31, 31);
						} else {
							# ���ˤʤ�
							$land->[$fx][$fy] = $HlandSea;
							$landValue->[$fx][$fy] = $nSea2;
							$HnavyAttackTarget{"$id,$fx,$fy"} = undef;
						}
						if(defined $nn2) {
							$nIsland2->{'ships'}[$nNo2]--;
							$nIsland2->{'ships'}[4]--;
						}
					}
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				} else {
					# ����
					logNavyDamage($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

					# HP������
					#$landValue->[$fx][$fy] -= $damage;
					$nHp2 -= $damage;
					if($nHp2 > 0) {
						($landValue->[$fx][$fy], $landValue2->[$fx][$fy]) = navyPack($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx, $goaly);

					} else {
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = $nSea2;
					}
					next;
				}
			} elsif($fKind == $HlandSeaMine) {
				# ����
				logNavySeaMine($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);

				$land->[$fx][$fy]      = $HlandSea; # ������
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
				$island->{'ext'}[5]++;
				next;
			} elsif (($fKind == $HlandDefence) && ($defflag >= 0)) {
				# �ɱһ���

				if($amityFlag{$id}) { # ̵����
					if(random(100) < $HnavySafetyInvalidp) {
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
					$nIsland->{'ext'}[2]++ if(defined $nn); # �˲������ɱһ��ߤο�
				}

				logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
			} elsif ($fKind == $HlandCore) {
				# ����
				my($lFlag, $lLv) = (int($fLv / 10000), ($fLv % 10000));
				if( !(($n == 0x1000) && ($lFlag >= 1)) && !((($n == 0x2000) || ($n == 0x4000)) && ($lFlag <= 1)) )  {
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
				# �ѵ��Ϥ򲼤���
				my $coreflag = $lLv - $damage;
				$fLv -= $damage;
				# ����������������˲���
				$nIsland->{'epoint'}{$id}++ if((defined $nn) && ($island->{'event'}[6] == 6) || (($coreflag < 0) && ($island->{'event'}[6] == 7)) && ($island->{'event'}[1] <= $HislandTurn));
				if($coreflag >= 0) {
					$land->[$fx][$fy] = $HlandCore;
					$landValue->[$fx][$fy] = $fLv;
					logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} else {
					$island->{'core'}--;
					$island->{'slaughterer2'} = $nId if($HcorelessDead && (defined $nn) && !$island->{'core'}); # �˲�������ID��Ͽ
					if ($n == 0x1000) {
						# ���롡���������дϡ�
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} elsif (($n == 0x2000) || ($n == 0x4000)) {
						# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
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
			} elsif ($fKind == $HlandTown) {
				# �ԻԷ�
				$island->{'ext'}[5]++;
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
				$nExp += int(($fLv - $sLv) / 20);
				$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
				($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
				if(defined $nn) {
					$nIsland->{'gain'} += int(($fLv - $sLv) / 20) if($HsurvivalTurn);
					if(($island->{'event'}[6] == 2) && ($island->{'event'}[1] <= $HislandTurn)) {
						# �����и��ͳ���
						$nIsland->{'epoint'}{$id} += int(($fLv - $sLv) / 20);
					}
				}
				$boat += ($fLv - $sLv); # ��̱�˥ץ饹
				if($rank) {
					$landValue->[$fx][$fy] = $sLv;
					logNavyNormalTown($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint, $HlandTownName[$rank]);
				} else {
					$island->{'slaughterer'} = $nId if(defined $nn); # �ԻԷϤ��˲�������ID��Ͽ
					logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					$land->[$fx][$fy] = $HlandWaste; # ���ϡ���������
					$landValue->[$fx][$fy] = 1;
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} else {
				# ����¾���Ϸ�
				if ($n == 0x1000) {
					# ���롡���������дϡ�
					logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} elsif (($n == 0x2000) || ($n == 0x4000)) {
					# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
					logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				}
				$island->{'ext'}[5]++;

				if ($fKind == $HlandBase && (defined $nn)) {
					$nIsland->{'ext'}[3]++; # ���ˤ����ߥ�������Ϥο�
				}
			}

			# �������Ϸ��ˤ���
			if ($n == 0x1000) {
				# ���롡���������дϡ�
				$land->[$fx][$fy] = $HlandSea; # ������
				$landValue->[$fx][$fy] = 0;
				$landValue->[$fx][$fy] = 1 if($fKind == $HlandBouha);
			} elsif (($n == 0x2000) || ($n == 0x4000)) {
				# ��ˤ�����дϡ����ϡ˴Ϻܵ����дϡ����ϡ�
				if ($fKind == $HlandOil) { # ��������
					$land->[$fx][$fy] = $HlandSea; # ������
					$landValue->[$fx][$fy] = 0;
				} elsif(($fKind == $HlandDefence) && ($defflag >= 0)) {
					# �Ǥ��ѵ��ϤλĤäƤ����ɱһ��ߤʤ��Ѥ���
					$land->[$fx][$fy] = $HlandDefence;
					$landValue->[$fx][$fy] = $fLv;
					next;
				} elsif($fKind == $HlandBouha) {
					# �Ǥ�������ʤ�����
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = 1;
					$island->{'bouha'}--;
				} else {
					$land->[$fx][$fy] = $HlandWaste; # ���ϡ���������
					$landValue->[$fx][$fy] = 1;
				}
			}
			$HlandMove[$id][$fx][$fy] = 1;
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
		my $kind;
		if ($n == 0x1000) {
			# ���롡���������дϡ�
			$kind = ($HnavyFireName[$nKind][0] ne '') ? $HnavyFireName[$nKind][0] : '����ȯ��';
		} elsif ($n == 0x2000) {
			# ��ˤ�����дϡ����ϡ�
			$kind = ($HnavyFireName[$nKind][1] ne '') ? $HnavyFireName[$nKind][1] : '��ˤ�ͷ�';
		} elsif ($n == 0x4000) {
			# �Ϻܵ����дϡ����ϡ�
			$kind = ($HnavyFireName[$nKind][2] ne '') ? $HnavyFireName[$nKind][2] : '�Ϻܵ�������';
		}
		logNavyMatome($id, $name, $nId, $nPoint, $nName, $tPoint, $tLandName, $kind, $str, $pntStr, join('-', (keys %damageId)));
	}
	# ��̱Ƚ��
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && (defined $nn)) {
		# ��̱ɺ��
		my($achive) = boatAchive($nIsland, $boat); # ��ã��̱

		if ($achive > 0) {
			# �����Ǥ����夷����硢�����Ǥ�
			my $name = islandName($nIsland);
			logMsBoatPeople($nId, $name, $achive);
			$nIsland->{'ext'}[4] += int($achive); # �߽Ф�����̱�ι�׿͸�

			# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
			if ($achive >= 200) {
				$nIsland->{'achive'} += $achive;
			}
		}
	}
	# ����ե饰��Ω�Ƥ�(���⤷������ϴ����ư���ɸ������Խ����򤷤ʤ�)
	$nIsland->{'NavyAttack_flag'}[$nNo] = 1 if(defined $nn);
	if($land->[$x][$y] == $HlandNavy) {
		return navyUnpack($landValue->[$x][$y],$landValue2->[$x][$y]);
#logdebug ($id, "code4($x, $y)");
	} else {
		return ($nId, $nTmp, $nStat, $nSea, $nExp, 1, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
#logdebug ($id, "code5($x, $y)");
	}
}

# ��̱��ã����
sub boatAchive {
	my($island, $boat) = @_;
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};

	my($i, $x, $y, $kind, $lv, $achive);
	for ($i = 0; ($i <= $island->{'pnum'} && $boat > 0); $i++) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$kind = $land->[$x][$y];
		$lv   = $landValue->[$x][$y];

		if($kind == $HlandTown) {
			# Į�ξ��
			foreach (reverse(0..$#HlandTownValue)) {
				if($HlandTownValue[$_] <= $lv) {
					if ($boat > $HachiveValueMax[$_]) {
						$lv     += $HachiveValueMax[$_];
						$achive += $HachiveValueMax[$_];
						$boat   -= $HachiveValueMax[$_];
					} else {
						$lv     += $boat;
						$achive += $boat;
						$boat    = 0;
					}
					if ($lv > $HvalueLandTownMax) {
						$lv      = $HvalueLandTownMax;
						$achive -= ($lv - $HvalueLandTownMax);
						$boat   += ($lv - $HvalueLandTownMax);
					}
					last;
				}
			}
			$landValue->[$x][$y] = $lv;

		} elsif ($bKind == $HlandPlains) {
			# ʿ�Ϥξ��
			$land->[$x][$y] = $HlandTown;;
			if ($boat > $HachivePlainsMax) {
				$landValue->[$x][$y] = $HachivePlainsMax - $HachivePlainsLoss;
				$achive += $HachivePlainsMax - $HachivePlainsLoss;
				$boat   -= $HachivePlainsMax;
			} elsif ($boat > 5) {
				$landValue->[$x][$y] = $boat - $HachivePlainsLoss;
				$achive += $boat - $HachivePlainsLoss;
				$boat   = 0;
			}
		}

		last if($boat <= 0);
	}

	return $achive;
}
# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
	my($island, $x, $y) = @_;
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($i, $sx, $sy);
	foreach $i (1..6) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ�
		next if(($sx < 0) || ($sy < 0) || ($HoceanMode && ($HlandID[$sx][$sy] != $id)));

		# �ϰ���ξ��
		if(($land->[$sx][$sy] == $HlandTown) || ($land->[$sx][$sy] == $HlandFarm)) {
			if($landValue->[$sx][$sy]) {
				return 1;
			}
		} elsif($land->[$sx][$sy] == $HlandComplex) {
			my $cKind = (landUnpack($landValue->[$sx][$sy]))[1];
			if($HcomplexAttr[$cKind] & 0x1) {
				return 1;
			}
		}
	}
	return 0;
}

# ������
sub doIslandProcess {
	my($island) = @_;

	# Ƴ����
	my($name)      = islandName($island);;
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my $disdown    = 1;
	if($HallyDisDown && ($island->{'allyId'}[0] ne '')) {
		$disdown   = $HallyDisDown;
	}
	# ������(�ޤȤ�ƥ�����)
	logOilMoney($id, $name, "����", "", "���$island->{'oilincome'}${HunitMoney}", "����") if($island->{'oilincome'} > 0);
	foreach (0..$#HcomplexComName) {
		my $income = $HcomplexComTFInCome[$_];
		next if($income->{'log'} ne 'matome');
		my $incomeValue = $island->{'cIncome'}[$_];
		logOilMoney($id, $name, $HcomplexName[$HcomplexComKind[$_]], "", "���$incomeValue${HunitMoney}", $income->{'logstr'}) if($incomeValue > 0);
	}
	foreach (0..$#HcomplexName) {
		# ������
		$island->{'randommoney'} += $island->{'rinmoney'}[$_];
		$island->{'randomfood'} += $island->{'rinfood'}[$_];
		logOilMoney($id, $name, $HcomplexName[$_], "", "���$island->{'rinmoney'}[$_]${HunitMoney}", "����") if($island->{'rinmoney'}[$_] > 0);
		logOilMoney($id, $name, $HcomplexName[$_], "", "����$island->{'rinfood'}[$_]${HunitFood}", "����") if($island->{'rinfood'}[$_] > 0);
	}
	# �Ͽ�Ƚ��
	if(($HpunishInfo{$id}->{punish} == 1) || (!$HnoDisFlag && (random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake * $disdown * $island->{'itemAbility'}[17])))) {
		# �Ͽ�ȯ��

		my($x, $y, $landKind, $lv, $i);
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if((($landKind == $HlandTown) && ($lv >= 100)) ||
				(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'earthquake'}[0] ne '')) ||
				($landKind == $HlandHaribote) ||
				($landKind == $HlandBouha) ||
				($landKind == $HlandFactory)) {
				# 1/4�ǲ���
				if(random(4) == 0) {
					logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;

					if($landKind == $HlandBouha) {
						# �Ǥ�������ʤ�����
						$land->[$x][$y] = $HlandSea;
						$landValue->[$x][$y] = 1;
						$island->{'bouha'}--;
					} elsif($landKind == $HlandComplex) {
						# ʣ���Ϸ��ʤ������Ϸ�
#						my $cKind = (landUnpack($lv))[1];
						$land->[$x][$y] = $HcomplexAfter[$cKind]->{'earthquake'}[0];
						$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'earthquake'}[1];
						$island->{'complex'}[$cKind]--;

                                        } elsif($landKind == $HlandTown) {
				            if($lv <= 100) {
					        $land->[$x][$y] = $HlandWaste;
					        $landValue->[$x][$y] = 0;
                                            }else{
					        $landValue->[$x][$y] -= 100;
				            }
					}
				}
			}
		}
		logEarthquake($id, $name);
	}

	# ������­
	if(($island->{'food'} <= 0) && !$island->{'field'}) {
		# ��­��å�����
		logStarve($id, $name);
		$island->{'food'} = 0;

		my($x, $y, $landKind, $lv, $i);
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind == $HlandFarm) ||
				($landKind == $HlandFactory) ||
				(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'starve'}[0] ne '')) ||
				($landKind == $HlandBase) ||
				($landKind == $HlandDefence)) {
				# 1/4�ǲ���
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
					if($landKind == $HlandComplex) {
						# ʣ���Ϸ��ʤ������Ϸ�
#						my $cKind = (landUnpack($lv))[1];
						$land->[$x][$y] = $HcomplexAfter[$cKind]->{'starve'}[0];
						$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'starve'}[1];
						$island->{'complex'}[$cKind]--;
					} elsif($landKind == $HlandDefence) {
						$island->{'dbase'}--;
					}
				}
			}
		}
	}

	# ����Ƚ��
	my $tsunamiFlag = $HdisTsunami * $disdown * $island->{'itemAbility'}[23];
	if($HnoDisFlag) {
		$tsunamiFlag = 0;
	} elsif($HdisTsunamiFsea) {
		if($island->{'sea'} < $HdisTsunamiFsea) {
			$tsunamiFlag *= 10;
		} elsif($island->{'pnum'} + 1  - 8*8 - $HdisTsunamiFsea > 0) {
 			my $flag = ($island->{'pnum'} + 1 - 8*8 - $island->{'sea'})/($island->{'pnum'} + 1 - 8*8 - $HdisTsunamiFsea);
			if($flag > 0) {
				$tsunamiFlag *= (1 + int($flag * 4));
			}
		}
	}
	my($wflag);
	$wflag = ($island->{'weather'}[5] >= 90) ? 10 * $island->{'weather'}[5] : ($island->{'weather'}[3] >= 45) ? 5 * $island->{'weather'}[3] : 0 if($HuseWeather);
	if(($HpunishInfo{$id}->{punish} == 2) || (random(1000 - $wflag) < $tsunamiFlag)) {
		# ����ȯ��
		$island->{'weather'}[5] = 0;
		$island->{'weather'}[3] = 0;
		my($x, $y, $landKind, $lv, $i);
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$lv2 = $landValue2->[$x][$y];

			if(($landKind == $HlandTown) ||
			($landKind == $HlandFarm) ||
			($landKind == $HlandFactory) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'tsunami'}[0] ne '')) ||
			($landKind == $HlandBase) ||
			($landKind == $HlandNavy) || # ��������
			($landKind == $HlandSeaMine) ||
			($landKind == $HlandDefence) ||
			($landKind == $HlandHaribote)) {
				next if(countAround($island, $x, $y, $an[2], $HlandBouha));
				next if(countAroundNavyBouha($island, $x, $y));
				# 1d12 <= (���Ϥγ� - 1) ������
				if(random(12) < (countAround($island, $x, $y, $an[1], $HlandNavy, $HlandSeaMine, $HlandOil, $HlandSbase, $HlandSea) - 1)) {
					if($landKind == $HlandNavy){
						my $fDamage = random($HdisTsunamiDmax) + 1; # ���᡼��1����10
						my ($nId, $nSea, $nNo, $nKind, $nHp) = (navyUnpack($lv, $lv2))[0, 3, 6, 7, 9];
						my $nSpecial = $HnavySpecial[$nKind];
						my $n = $HidToNumber{$nId};
						$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
						if($nSpecial & 0x8) { # ��
							logTsunamiDamage($id, $name, landName($landKind, $lv), "($x, $y)");
						 	$land->[$x][$y] = $HlandSea;
							$landValue->[$x][$y] = 1;
							$Hislands[$n]->{'navyPort'}-- if(defined $n);
						} elsif(!($nHp > $fDamage)) { # �������᡼�����ѵ��Ϥ�å����
							logTsunamiDamageNavyDestroy($id, $name, landName($landKind, $lv), "($x, $y)");
						 	$land->[$x][$y] = $HlandSea;
							$landValue->[$x][$y] = $nSea;
							if(defined $n) {
								$Hislands[$n]->{'ships'}[$nNo]--;
								$Hislands[$n]->{'ships'}[4]--;
								# ���Х��Х�
								$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
							}
						} else {
							logTsunamiDamageNavy($id, $name, landName($landKind, $lv), "($x, $y)");
							$landValue->[$x][$y] -= $fDamage;
						}

					} else {
						logTsunamiDamage($id, $name, landName($landKind, $lv), "($x, $y)");
						$land->[$x][$y] = $HlandWaste;
						$landValue->[$x][$y] = 0;
						if($landKind == $HlandSeaMine) {
							# �Ǥⵡ��ʤ鳤
							$land->[$x][$y] = $HlandSea;
						} elsif($landKind == $HlandComplex) {
							# ʣ���Ϸ��ʤ������Ϸ�
#							my $cKind = (landUnpack($lv))[1];
							$land->[$x][$y] = $HcomplexAfter[$cKind]->{'tsunami'}[0];
							$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'tsunami'}[1];
							$island->{'complex'}[$cKind]--;
						} elsif($landKind == $HlandDefence) {
							$island->{'dbase'}--;
						}
					}
				}
			}
		}
		logTsunami($id, $name);

	}

	# ����Ƚ��
	my($r, $pop);
	if(!$island->{'field'}) {
		$r = (random(10000) < ($HdisMonster * $island->{'area'})) ? 1 : 0;
		$pop = $island->{'pop'};
	} else {
		#$r = ($HdisMonsterBF && random(10000) < $HdisMonsterBF) ? 1 : (random(5000) < ($HdisMonster * $island->{'area'})) ? 1 : 0;
                $r = !random(20);
		$pop = $HdisMonsBorderMax;
	}
	$r = 0 if ($HnoDisFlag);
	$r = 1 if ($HpunishInfo{$id}->{punish} == 3);
	if($r && ($pop >= $HdisMonsBorderMin)) {
		# ���ýи�
		# ��������
		my($kind, @r);
		foreach (0..$#HdisMonsBorder) {
			push(@r, ($_)x$HdisMonsRatio[$_]) if($pop >= $HdisMonsBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		# ���ýи�
		bringMonster($island, 0, $kind, 0);
	}

	# �������Ƚ��
	if(!$island->{'field'}) {
		$r = (random(10000) < ($HdisHuge * $island->{'area'})) ? 1 : 0;
		$pop = $island->{'pop'};
	} else {
		$r = ($HdisHugeBF && random(10000) < $HdisHugeBF) ? 1 : (random(5000) < ($HdisHuge * $island->{'area'})) ? 1 : 0;
		$pop = $HdisHugeBorderMax;
	}
	$r = 0 if ($HnoDisFlag);
	$r = 1 if ($HpunishInfo{$id}->{punish} == 4);
	if($r && ($pop >= $HdisHugeBorderMin) && $HhugeMonsterAppear) {
		# ������ýи�
		# ��������
		my($kind, @r);
		foreach (0..$#HdisHugeBorder) {
			push(@r, ($_)x$HdisHugeRatio[$_]) if($pop >= $HdisHugeBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		bringMonster($island, 0, $kind, 1);
	}

	# ����(��°����)Ƚ��
	if(!$island->{'field'}) {
		$r = (random(10000) < ($HdisNavy * $island->{'area'})) ? 1 : 0;
		$pop = $island->{'pop'};
	} else {
		#$r = ($HdisNavyBF && random(10000) < $HdisNavyBF) ? 1 : (random(5000) < ($HdisNavy * $island->{'area'})) ? 1 : 0;
                $r = !random(20);

		$pop = $HdisNavyBorderMax;
	}
	$r = 0 if ($HnoDisFlag);
	$r = 1 if ($HpunishInfo{$id}->{punish} == 5);
	if($r && ($pop >= $HdisNavyBorderMin) && $HnavyUnknown) {
		# �����и�
		# ��������
		my($kind, @r);
		foreach (0..$#HdisNavyRatio) {
			push(@r, ($_)x$HdisNavyRatio[$_]) if($pop >= $HdisNavyBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		bringNavy($island, $kind);
	}
	# ���٥����νи�Ƚ��
	if($island->{'event'}[0] && ($island->{'event'}[1] <= $HislandTurn)) {
		# ����
		if($island->{'event'}[13] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[12])) {
			bringMonster($island, 0, random($#HmonsterName+1), 0, $island->{'event'}[13]);
		}
		# �������
		if($island->{'event'}[15] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[14])) {
			bringMonster($island, 0, random($#HhugeMonsterName+1), 1, $island->{'event'}[15]);
		}
		# ��°������
		if($island->{'event'}[17] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[16])) {
			bringNavy($island, random($#HnavyName)+1, $island->{'event'}[17]);
		}
		# ����
		if($island->{'event'}[20] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[19])) {
			randomBuildCore($island, $island->{'event'}[20], $island->{'event'}[21], $island->{'event'}[22], 1);
		}
	}


	# ��������Ƚ��
	$wflag = ($island->{'weather'}[4] >= 90) ? 10 * $island->{'weather'}[4] : 0 if($HuseWeather);
	if(($island->{'area'} > $HdisFallBorder) &&
	   (($HpunishInfo{$id}->{punish} == 6) || (random(1000 - $wflag) < $HdisFalldown))) {
		# ��������ȯ��
		$island->{'weather'}[4] = 0;
		my($x, $y, $landKind, $lv, $i);
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$lv2= $landValue2->[$x][$y];

			if(($landKind != $HlandSea) &&
				($landKind != $HlandSbase) &&
				!(($landKind == $HlandCore) && (int($lv / 10000))) &&
				($landKind != $HlandOil) &&
				($landKind != $HlandSeaMine) &&
				($landKind != $HlandResource) &&
				($landKind != $HlandMountain)) {

				if($landKind == $HlandNavy) { # ��������
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
					my $nSpecial = $HnavySpecial[$nKind];
					unless ($nSpecial & 0x8) {
						# ���ʳ��������������ʤ�
						next;
					}
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} elsif($landKind == $HlandComplex) {
					# ʣ���Ϸ��ʤ������Ϸ�
					my $cKind = (landUnpack($lv))[1];
					next if($HcomplexAfter[$cKind]->{'falldown'}[0] eq '');
					next if(!countAround($island, $x, $y, $an[1], $HlandSea, $HlandSbase, $HlandNavy));
					$land->[$x][$y] = $HcomplexAfter[$cKind]->{'falldown'}[0];
					$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'falldown'}[1];
					$island->{'complex'}[$cKind]--;
					logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
					next;
				} elsif($landKind == $HlandMonster) { # ����
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);

					# ���ˤ���
					next if ($mFlag2 & 2);
				} elsif($landKind == $HlandHugeMonster) { # ������ä������������ʤ�
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);

					# ���ˤ���
					next if ($mFlag2 & 2);
					# ���Ϥ˳�������С�Φ�ϥե饰���������ѹ�
					if(countAround($island, $x, $y, $an[1], $HlandSea, $HlandSbase)) {
						logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
						$mFlag |= 2;
						$mSea = 1;
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
						next;
					}
				}

				# ���Ϥ˳�������С��ͤ�-1��
#				if(countAround($island, $x, $y, $an[1], $HlandSea, $HlandSbase, $HlandNavy)) {
#					logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
#					$land->[$x][$y] = -1;
#					$landValue->[$x][$y] = 0;
#				}

				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 1;
				logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
                                $island->{'area'}--;

                                if($island->{'area'} <= $HdisFallBorder){
                                    last;
                                }

			}
		}

#		foreach $i (0..$island->{'pnum'}) {
#			$x = $island->{'rpx'}[$i];
#			$y = $island->{'rpy'}[$i];
#			$landKind = $land->[$x][$y];
#
#			if($landKind == -1) {
#				# -1�ˤʤäƤ�����������
#				$land->[$x][$y] = $HlandSea;
#				$landValue->[$x][$y] = 1;
#			} elsif ($landKind == $HlandSea) {
#				# �����ϳ���
#				$landValue->[$x][$y] = 0;
#			}
#
#		}

		logFalldown($id, $name);
	}

	# ����Ƚ��
	$wflag = ($island->{'weather'}[3] >= 20) ? 10 * $island->{'weather'}[3] : 0 if($HuseWeather);
	if(($HpunishInfo{$id}->{punish} == 7) || (!$HnoDisFlag && (random(1000 - $wflag) < $HdisTyphoon * $disdown * $island->{'itemAbility'}[18]))) {
		# ����ȯ��
		$island->{'weather'}[3] = 0;
		my($x, $y, $landKind, $lv, $i);
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind == $HlandFarm) ||
				(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'typhoon'}[0] ne '')) ||
				($landKind == $HlandHaribote)) {

				# 1d12 <= (6 - ���Ϥο�) ������
				if(random(12) < (6 - countAround($island, $x, $y, $an[1], $HlandForest, $HlandMonument)
									- countAroundComplex($island, $x, $y, $an[1], 0x4))
					) {
					logTyphoonDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					if($landKind == $HlandComplex) {
						# ʣ���Ϸ��ʤ������Ϸ�
#						my $cKind = (landUnpack($lv))[1];
						$land->[$x][$y] = $HcomplexAfter[$cKind]->{'typhoon'}[0];
						$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'typhoon'}[1];
						$island->{'complex'}[$cKind]--;
					}
				}
			}
		}
		logTyphoon($id, $name);
	}

	my($map) = $island->{'map'};
	my(@x) = @{$map->{'x'}};
	my(@y) = @{$map->{'y'}};

	# �������Ƚ��
	if(($HpunishInfo{$id}->{punish} == 8) || (!$HnoDisFlag && (random(1000) < $HdisHugeMeteo * $disdown * $island->{'itemAbility'}[20]))) {
		my($x, $y, $landKind, $lv, $point);

		# �
		$x = $x[0] + random($HislandSizeX);
		$y = $y[0] + random($HislandSizeY);
		if ($HpunishInfo{$id}->{punish} == 8) {
			$x = $HpunishInfo{$id}->{x};
			$y = $HpunishInfo{$id}->{y};
		}
		$landKind = $land->[$x][$y];
		$lv = $landValue->[$x][$y];
		$point = "($x, $y)";

		# �����ﳲ�롼����
		wideDamage($id, $name, $island, $x, $y);
		# ��å�����
		logHugeMeteo($id, $name, $point);
	}

	# ����ߥ�����Ƚ��
	while($island->{'bigmissile'} > 0) {
		$island->{'bigmissile'} --;

		my($x, $y, $landKind, $lv, $point);

		# �
		$x = $x[0] + random($HislandSizeX);
		$y = $y[0] + random($HislandSizeY);
		$landKind = $land->[$x][$y];
		$lv = $landValue->[$x][$y];
		$point = "($x, $y)";

		# �����ﳲ�롼����
		wideDamage($id, $name, $island, $x, $y);
		# ��å�����
		logMonDamage($id, $name, $point);
	}

	# ���Ƚ��
	if(($HpunishInfo{$id}->{punish} == 9) || (!$HnoDisFlag && (random(1000) < $HdisMeteo * $disdown * $island->{'itemAbility'}[19]))) {
		my($x, $y, $landKind, $lv, $point, $first, $pflag);
		$first = 1;
		$pflag = 1;
		while((random(2) == 0) || ($first == 1)) {
			$first = 0;

			# �
			$x = $x[0] + random($HislandSizeX);
			$y = $y[0] + random($HislandSizeY);
			if ($pflag && ($HpunishInfo{$id}->{punish} == 9)) {
				$x = $HpunishInfo{$id}->{x};
				$y = $HpunishInfo{$id}->{y};
				$pflag = 0;
			}
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$point = "($x, $y)";

			if(($landKind == $HlandSea) && ($lv == 0)){
				# ���ݥ���
				logMeteoSea($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandSeaMine) {
				# ����
				logMeteoMountain($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandMountain) {
				# ���˲�
				logMeteoMountain($id, $name, landName($landKind, $lv), $point);
				$land->[$x][$y] = $HlandWaste;
				$landValue->[$x][$y] = 1;
				next;
			} elsif(($landKind == $HlandSbase) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				logMeteoSbase($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandComplex) {
				# ʣ���Ϸ��ʤ������Ϸ�
				my $cKind = (landUnpack($lv))[1];
				next if($HcomplexAfter[$cKind]->{'meteo'}[0] eq '');
				$land->[$x][$y] = $HcomplexAfter[$cKind]->{'meteo'}[0];
				$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'meteo'}[1];
				$island->{'complex'}[$cKind]--;
				logMeteoMountain($id, $name, landName($landKind, $lv), $point);
				next;
			} elsif($landKind == $HlandMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if ($mFlag & 2) {
					logMeteoMonsterSea($id, $name, landName($landKind, $lv), $point);
				} else {
					logMeteoMonster($id, $name, landName($landKind, $lv), $point);
				}
			} elsif($landKind == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if ($mFlag & 2) {
					logMeteoMonsterSea($id, $name, landName($landKind, $lv), $point);
				} else {
					logMeteoMonster($id, $name, landName($landKind, $lv), $point);
				}
				if($mHflag == 0) {
					my($j, $ssx, $ssy);
					foreach $j (1..6) {
						next if($HhugeMonsterImage[$mKind][$j] eq '');
						$ssx = $x + $ax[$j];
						$ssy = $y + $ay[$j];
						# �Ԥˤ�����Ĵ��
						$ssx-- if(!($ssy % 2) && ($y % 2));
						$ssx = $correctX[$ssx + $#an];
						$ssy = $correctY[$ssy + $#an];
						# �ϰϳ�
						next if(($ssx < 0) || ($ssy < 0));

						next if($land->[$ssx][$ssy] != $HlandHugeMonster);
						# �����Ǥμ��Ф�
						my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
						next if($mHflag2 != $j);
						if ($mFlag2 & 2) {
							# ���ˤ���
							$land->[$ssx][$ssy] = $HlandSea;
							$landValue->[$ssx][$ssy] = $mSea2;
						} else {
							# Φ�Ϥˤ���
							$land->[$ssx][$ssy] = $HlandWaste;
							$landValue->[$ssx][$ssy] = 0;
						}
					}
				}
			} elsif(($landKind == $HlandSea) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 1))) {
				# ����
				logMeteoSea1($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if ($nSpecial & 0x8) {
					# ��
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logMeteoNormal($id, $name, landName($landKind, $lv), $point);
				} else {
					# ����¾
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
					}
					logMeteoMountain($id, $name, landName($landKind, $lv), $point);
				}
			} else {
				logMeteoNormal($id, $name, landName($landKind, $lv), $point);
			}
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 0;
		}
	}

	# ʮ��Ƚ��
	if(($HpunishInfo{$id}->{punish} == 10) || (!$HnoDisFlag && (random(1000) < $HdisEruption * $disdown * $island->{'itemAbility'}[21]))) {
		my($x, $y, $sx, $sy, $i, $landKind, $lv, $point);
		if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
			$x = $x[0] + random($HislandSizeX - $HedgeReclaim * 2) + $HedgeReclaim;
			$y = $y[0] + random($HislandSizeY - $HedgeReclaim * 2) + $HedgeReclaim;
		} else {
			$x = $x[0] + random($HislandSizeX);
			$y = $y[0] + random($HislandSizeY);
		}
		if ($HpunishInfo{$id}->{punish} == 10) {
			$x = $HpunishInfo{$id}->{x};
			$y = $HpunishInfo{$id}->{y};
		}
		$landKind = $land->[$x][$y];
		$lv = $landValue->[$x][$y];
		$point = "($x, $y)";
		$land->[$x][$y] = $HlandMountain;
		$landValue->[$x][$y] = 0;
		if($landKind == $HlandNavy) {
			my($nId, $nNo) = (navyUnpack($lv, $lv2))[0, 6];
			my $n = $HidToNumber{$nId};
			if(defined $n) {
				$Hislands[$n]->{'shipk'}[$nKind]--;
				if($special & 0x8) {
					$Hislands[$n]->{'navyPort'}--;
				} else {
					$Hislands[$n]->{'ships'}[$nNo]--;
					$Hislands[$n]->{'ships'}[4]--;
				}
			}
		}

		my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
		# ������ý���(��������줿���Τ�)
		if(($landKind == $HlandHugeMonster) && ($mHflag == 0)) {
			my($j, $ssx, $ssy);
			foreach $j (1..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$ssx = $x + $ax[$j];
				$ssy = $y + $ay[$j];
				# �Ԥˤ�����Ĵ��
				$ssx-- if(!($ssy % 2) && ($y % 2));
				$ssx = $correctX[$ssx + $#an];
				$ssy = $correctY[$ssy + $#an];
				# �ϰϳ�
				next if(($ssx < 0) || ($ssy < 0));

				next if($land->[$ssx][$ssy] != $HlandHugeMonster);
				# �����Ǥμ��Ф�
				my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
				next if($mHflag2 != $j);
				if ($mFlag2 & 2) {
					# ���ˤ���
					$land->[$ssx][$ssy] = $HlandSea;
					$landValue->[$ssx][$ssy] = $mSea2;
				} else {
					# Φ�Ϥˤ���
					$land->[$ssx][$ssy] = $HlandWaste;
					$landValue->[$ssx][$ssy] = 0;
				}
			}
		}

		foreach $i (1..6) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# �ϰϳ�
			next if(($sx < 0) || ($sy < 0));

			$landKind = $land->[$sx][$sy];
			$lv = $landValue->[$sx][$sy];
			$point = "($sx, $sy)";

			# �ϰ���ξ��
			$landKind = $land->[$sx][$sy];
			$lv = $landValue->[$sx][$sy];
			$point = "($sx, $sy)";
			my(@x, @y);
			if($HedgeReclaim) {
				my($map) = $island->{'map'};
				@x = @{$map->{'x'}};
				@y = @{$map->{'y'}};
			}
			if(($landKind == $HlandSea) ||
				($landKind == $HlandOil)) {
				# �������Ĥξ��
				if(!$lv || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
					logEruptionSea($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandSea;
					$landValue->[$sx][$sy] = 1;
					next;
				} else {
					# ����
					logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					next if($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim))); # ��κǳ��������Ω���ԲĤˤ�����;
				}
			} elsif(($landKind == $HlandSeaMine) ||
				($landKind == $HlandSbase) ||
				(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				# ���롢���𡤳��쥳���ξ��
				logEruptionSea($id, $name, landName($landKind, $lv), $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 1;
				next;
			} elsif(($landKind == $HlandMountain) ||
				($landKind == $HlandWaste)) {
				next;
			} elsif($landKind == $HlandComplex) {
				# ʣ���Ϸ��ʤ������Ϸ�
				my $cKind = (landUnpack($lv))[1];
				next if($HcomplexAfter[$cKind]->{'eruption'}[0] eq '');
				$land->[$sx][$sy] = $HcomplexAfter[$cKind]->{'eruption'}[0];
				$landValue->[$sx][$sy] = $HcomplexAfter[$cKind]->{'eruption'}[1];
				$island->{'complex'}[$cKind]--;
				logEruptionNormal($id, $name, landName($landKind, $lv), $point);
				next;
			} elsif(($landKind == $HlandMonster) || ($landKind == $HlandHugeMonster)) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if((($mFlag & 2) && !$mSea) || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
					logEruptionSea3($id, $name, landName($landKind, $lv), $point);
					$mSea = 1;
				} else {
					logEruptionSea2($id, $name, landName($landKind, $lv), $point);
					$mFlag &= ~2;
					$mSea = 0;
				}
				$landValue->[$sx][$sy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
				next;
			} elsif($landKind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if ($nSpecial & 0x8) {
					# ����Φ��
					logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandWaste;
					$landValue->[$sx][$sy] = 0;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} else {
					if(!$nSea || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
						# ����¾������
						logEruptionSea($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandSea;
						$landValue->[$sx][$sy] = 1;
					} else {
						# ������Φ��
						logEruptionSea1($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandWaste;
						$landValue->[$sx][$sy] = 0;
					}
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
					}
				}
				next;
			} else {
				# ����ʳ��ξ��
				logEruptionNormal($id, $name, landName($landKind, $lv), $point);
			}
			$land->[$sx][$sy] = $HlandWaste;
			$landValue->[$sx][$sy] = 0;
		}
		logEruption($id, $name, landName($land->[$x][$y], $landValue->[$x][$y]), "($x, $y)");
	}

        # �۾������̤�̵���ä���Ф�褦��
        if($island->{'stone'} < 2){
            # �۾�
	    my $x = random($HislandSizeX);
	    my $y = random($HislandSizeY);
            my $kind, $money;
            if($land->[$x][$y] == $HlandSea){
                $land->[$x][$y] = $HlandResource;
                $kind = 0;
                $money = random(61);
                $landValue->[$x][$y] = landPack(0, $kind, 0, 0, $money);
            }
        }else{
            if($island->{'fish'} < 2){
                # ����
	        my $x = random($HislandSizeX);
	        my $y = random($HislandSizeY);
                my $kind, $food;
                if($land->[$x][$y] == $HlandSea){
                    $land->[$x][$y] = $HlandResource;
                    $kind = 1;
                    $food = random(61);
                    $landValue->[$x][$y] = landPack(0, $kind, 0, $food, 0);
                }
            }
        }
}

# ������(estimate����)
sub doIslandProcessEstimate {
	my($number, $island) = @_;

	# Ƴ����
	my($name)      = islandName($island);;
	my($id)        = $island->{'id'};

	# ���������դ�Ƥ��鴹��
	my $fflag = $island->{'itemAbility'}[7];
	if($island->{'food'} > int($HmaximumFood * $fflag)) {
		$island->{'money'} += int(($island->{'food'} - ($HmaximumFood * $fflag)) / 10);
		$island->{'food'} = int($HmaximumFood * $fflag);
	}

	# �⤬���դ�Ƥ����ڤ�Τ�
	my $mflag = $island->{'itemAbility'}[8];
	if($island->{'money'} > int($HmaximumMoney * $mflag)) {
		$island->{'money'} = int($HmaximumMoney * $mflag) ;
	}

	# �Ƽ���ͤ�׻�
	estimate($number);

	# �Ƽ﷮�ϼ���
	$island->{'damage'} = $island->{'oldPop'} - $island->{'pop'};
	my($prize) = $island->{'prize'};
	$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
	my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);

	my($value, $thres, $p);
	my($f) = 1;
	foreach $p (1..$#Hprize) {
		if (!($flags & $f)) {
			$value = (!$Hprize[$p]->{'ptr'} ? $island->{$Hprize[$p]->{'kind'}} : $island->{$Hprize[$p]->{'kind'}}[$Hprize[$p]->{'ptr'}]);
			$thres = $Hprize[$p]->{'threshold'};
			if ($value >= $thres) {
				$flags |= $f; # ����
				$island->{'ext'}[1] += $Hprize[$p]->{'contribution'}; # �׸���up
				if($Hprize[$p]->{'money'}) {
					$island->{'prizemoney'} += $Hprize[$p]->{'money'};
					$island->{'money'} += $Hprize[$p]->{'money'};
				}
				logPrize($id, $name, $Hprize[$p]->{'name'}, $Hprize[$p]->{'money'});
			}
		}
		$f *= 2;
	}

	$island->{'prize'} = "$flags,$monsters,$hmonsters,$turns";

}

# ���ýи�
sub bringMonster {
	my($island, $tId, $mKind, $huge, $num) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};

	# flag : bit0=�Ų�, bit1=����
	my $mHp = (!$huge) ? ($HmonsterBHP[$mKind] + random($HmonsterDHP[$mKind])) : ($HhugeMonsterBHP[$mKind] + random($HhugeMonsterDHP[$mKind]));
	my $mLv = monsterPack($tId, 0, 0, 0, 2, $mKind, $mHp);

	makeRandomIslandPointArray($island);
	my($i, $x, $y, $lv);
	my $count = 0;
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];

		# ��������õ���ʲ��äϿ������������
		next unless (($land->[$x][$y] == $HlandSea) && !$lv);

		# ������äξ��
		if($huge) {
			my($j, $sx, $sy);
			my $dmove = 0;
			foreach $j (1..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				# �Ԥˤ�����Ĵ��
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];

				# �ϰϳ�Ƚ��
				if(($sx < 0) || ($sy < 0)) {
					$dmove = 1;
				}
				if($HoceanMode && $HfieldUnconnect && ($HlandID[$sx][$sy] != $id)) {
					my $mn = $HidToNumber{$HlandID[$sx][$sy]};
					$dmove = 1 if(((defined $mn) && $Hislands{$mn}->{'field'}) || $island->{'field'});
				}
				# ���ʳ��ʤ�и��Ǥ��ʤ�
				if($land->[$sx][$sy] != $HlandSea) {
					$dmove = 1;
				}
			}
			next if($dmove);
		}

		# �Ϸ�̾
		my $lName = landName($HlandSea, $lv);

		# ���ä�����
		if($huge) {
			# ������äξ��
			my($j, $sx, $sy, $mSea, $mFlag);
			foreach $j (0..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				# �Ԥˤ�����Ĵ��
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];
				# �ϰϳ�
				next if(($sx < 0) || ($sy < 0));
				if($HoceanMode && $HfieldUnconnect && ($HlandID[$sx][$sy] != $id)) {
					my $mn = $HidToNumber{$HlandID[$sx][$sy]};
					next if(((defined $mn) && $Hislands{$mn}->{'field'}) || $island->{'field'});
				}

				$mSea = $landValue->[$sx][$sy];
				$mFlag |= 2;

				$land->[$sx][$sy] = $HlandHugeMonster;
				$landValue->[$sx][$sy] = monsterPack($tId, $j, $mSea, 0, $mFlag, $mKind, $mHp);
			}
		} else {
			$land->[$x][$y] = $HlandMonster;
			$landValue->[$x][$y] = $mLv;
		}

		# ��ư�Ѥߤˤ���
		$HmonsterMove[$id][$x][$y] = 2;

		# ����̾
		my $mName = (!$huge) ? $HmonsterName[$mKind] : $HhugeMonsterName[$mKind];

		# ��å�����
		logMonsCome($id, $name, $mName, "($x, $y)", $lName);
		last if(++$count >= $num);
	}
}

# �����и�
sub bringNavy {
	my($island, $nKind, $num) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};

	my ($nLv, $nLv2) = navyPack(0, 0, 0, 0, 0, 0, 0, $nKind, 0, $HnavyHP[$nKind], 31, 31);

	makeRandomIslandPointArray($island);
	my($i, $x, $y, $lv);
	my $count = 0;
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];

		# ��������õ��
		next unless (($land->[$x][$y] == $HlandSea) && !$lv);

		# �Ϸ�̾
		my $lName = landName($HlandSea, $lv);

		# ����������
		$land->[$x][$y] = $HlandNavy;
		$landValue->[$x][$y] = $nLv;
		$landValue2->[$x][$y] = $nLv2;

		# ��ư�Ѥߤˤ���
		$HnavyMove[$id][$x][$y] = 2;

		# ����̾
		my $nName = $HnavyName[$nKind];

		# ��å�����
		logNavyCome($id, $name, $nName, "($x, $y)", $lName);
		last if(++$count >= $num);
	}
}

# �����и�
sub randomBuildCore {
	my($island, $num, $lvmin, $lvmax, $log) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};

	makeRandomIslandPointArray($island);
	my($i, $x, $y, $l, $lv);
	my $count = 0;
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$l  = $land->[$x][$y];
		$lv = $landValue->[$x][$y];

		# ����������ʿ�ϡ����Ϥ򤵤���
		next if(($l != $HlandSea) && ($l != $HlandPlains) && ($l != $HlandWaste));

		# �Ϸ�̾
		my $lName = landName($l, $lv);

		# ����������
		$land->[$x][$y] = $HlandCore;
		$lvmin = $HdurableCore if($lvmin > $HdurableCore);
		$lvmax = $HdurableCore if($lvmax > $HdurableCore);
		$lvmin = $lvmax if($lvmin > $lvmax);
		$landValue->[$x][$y] = $lvmin + random($lvmax - $lvmin + 1);
		if($l == $HlandSea) {
			$landValue->[$x][$y] += (!$lv) ? 20000 : 10000; # ��������
		}

		# ����̾
		my $nName = landName($land->[$x][$y], $landValue->[$x][$y]);
		my $point = ($HcoreHide) ? "(?, ?)" : "($x, $y)";

		# ��å�����
		logCoreRandomBuild($id, $name, $nName, $point, $lName) if($log);
		$island->{'core'}++;
		last if(++$count >= $num);
	}
}

# ʣ���Ϸ�����
sub buildComplex {
	my($island, $comName, $kind, $rep, $x, $y) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $point     = "($x, $y)";

	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];
	my($landName) = landName($landKind, $lv);

	my($cTmp, $cKind, $cTurn, $cFood, $cMoney);
	my $clflag = 1;
	if($landKind != $HlandComplex) {
		$clflag = 0;
		foreach (@{$HcomplexBefore[$HcomplexComKind[$kind]]}) {
			if(($landKind == $_->[0]) && ($_->[1] <= $lv) && ($lv <= $_->[2])) {
				$clflag = 1;
				last;
			}
		}
	}
	if(!$clflag) {
		# ��Ŭ�����Ϸ�
		logLandFail($id, $name, $comName, $landName, $point);
		return 0;
	} elsif($landKind == $HlandComplex) {
		# ���Ǥ�ʣ���Ϸ��ξ��
		($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $landCheck = ($HcomplexComKind[$kind] != $cKind) ? 1 : 0;
		foreach (@{$HcomplexBefore2[$HcomplexComKind[$kind]]}) {
			if($cKind == $_) {
				$landCheck = 0;
				last;
			}
		}
		if($landCheck || (!$HcomplexTPCmax[$cKind] && !$HcomplexFPCmax[$cKind] && !$HcomplexMPCmax[$cKind])) {
			# ��Ŭ�����Ϸ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if(($HcomplexComKind[$kind] != $cKind) || !($HcomplexComFlag[$kind] & 0x7)) {
			# ��Ū�ξ���ʣ���Ϸ���
			if($HcomplexMax[$HcomplexComKind[$kind]] && $island->{'complex'}[$HcomplexComKind[$kind]] >= $HcomplexMax[$HcomplexComKind[$kind]]) {
				# ��ͭ��ǽ����������С�
				logOverFail($id, $name, $comName, $point);
				return 0;
			}
			$island->{'complex'}[$cKind]--;
			$land->[$x][$y] = $HlandComplex;
			$cKind = $HcomplexComKind[$kind];
			$island->{'complex'}[$cKind]++;
			($cTurn, $cFood, $cMoney) = (1, 0, 0);
		} else {
			# �����ե饰����
			$cFood  += $rep if($HcomplexComFlag[$kind] & 0x2);
			# ���ե饰����
			$cMoney += $rep if($HcomplexComFlag[$kind] & 0x4);
			if($HcomplexComFlag[$kind] & 0x1) {
				# ������ե饰�ִ�����
				my $income = $HcomplexComTFInCome[$kind];
				my $incomeValue = $cTurn * $income->{'ratio'};
				if($income->{'log'} eq 'normal') {
					$island->{$income->{'type'}} += $incomeValue;
					logOilMoney($id, $name, $HcomplexName[$cKind], $point, "$incomeValue${HunitMoney}", $income->{'logstr'});
				} else {
					$island->{'cIncome'}[$kind] += $incomeValue;
				}
				# ������ե饰�ꥻ�å�
				if($HcomplexComTFRL[$kind][0] ne '') {
					$land->[$x][$y] = $HcomplexComTFRL[$kind][0];
					$landValue->[$x][$y] = $HcomplexComTFRL[$kind][1];
					return 0;
				} else {
					$cTurn = 0;
				}
			}
		}
	} else {
		if($HcomplexMax[$HcomplexComKind[$kind]] && $island->{'complex'}[$HcomplexComKind[$kind]] >= $HcomplexMax[$HcomplexComKind[$kind]]) {
			# ��ͭ��ǽ����������С�
			logOverFail($id, $name, $comName, $point);
			return 0;
		}
		# ��Ū�ξ���ʣ���Ϸ���
		$land->[$x][$y] = $HlandComplex;
		$cKind = $HcomplexComKind[$kind];
		$island->{'complex'}[$cKind]++;
		($cTurn, $cFood, $cMoney) = (1, 0, 0);
		if($rep > 1) {
			$cFood += ($rep-1) if($HcomplexComFlag[$kind] & 0x2);
			$cMoney += ($rep-1) if($HcomplexComFlag[$kind] & 0x4);
		}
	}
	$cTurn = $HcomplexTPCmax[$cKind] if($cTurn  > $HcomplexTPCmax[$cKind]);
	$cFood = $HcomplexFPCmax[$cKind] if($cFood  > $HcomplexFPCmax[$cKind]);
	$cMoney = $HcomplexMPCmax[$cKind] if($cMoney > $HcomplexMPCmax[$cKind]);
	$landValue->[$x][$y] = landPack($cTmp, $cKind, $cTurn, $cFood, $cMoney);
	logLandSuc($id, $name, $comName, $point);
	return 1;
}

# ������¤�ʹ���ޤ��
sub buildNavy {
	my($island, $comName, $nKind, $nNo, $nx, $ny) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};
	my $point     = "($nx, $ny)";
        my $landcount;
	# ������Τ�
	$nNo--;
	if ($nNo < 0) {
		$nNo = 0;
	} elsif ($nNo > 3) {
		$nNo = 3;
	}

        # ����ͽ���Ϥ��������ɤ�����˥����å�
        my ($asase) = 0;
	if (($land->[$nx][$ny] == $HlandSea) && ($landValue->[$nx][$ny] == 1)) {
            $asase = 1;
        }

	# flag : bit0=�̾�, bit1=�ĳ�, bit2=����, bit3=������
	my ($nLv, $nLv2);
        if($HnavyBuildTurn[$nKind] == 0){
	    ($nLv, $nLv2) = navyPack($id, 0, 0, $asase, 0, 0, $nNo, $nKind, $HnavyCruiseTurn[$nKind] + 1, $HnavyHP[$nKind], 31, 31);#�������Ҷ����ξ��
        }else{
	    ($nLv, $nLv2) = navyPack($id, 0, 0, 0, 0, 3, $nNo, $nKind, 0, 0, 31, 31);#���Ϥξ�� �����ե饰��Ω�Ƥơ�Hp(����)��0������
        }

        # ���ξ��ϼ����Φ�Ϥ�����ơ�$nLv��$nLv2�������
        if($nKind == 0){
            $landcount = searchLand($island, $nx, $ny);
            if($landcount > 3){
                $landcount = 3;
            }
            my $shortcut = $landcount * 3;
	    ($nLv, $nLv2) = navyPack($id, 0, 0, 0, 0, 3, $nNo, $nKind, 0, $shortcut, 31, 31);#������
        }

	my $nSpecial = $HnavySpecial[$nKind];
	my $ofname = $island->{'fleet'}->[$nNo];

	# ��¤��٥��ǧ
	if($HmaxComNavyLevel) {
		my $navyComLevel = gainToLevel($island->{'gain'});
		if($HcomNavyNumber[$navyComLevel-1] < $nKind) {
			logNavyNoExp($id, $name, $comName);
			return 0;
		}
	}
	# ��ͭ��ǽ�����������å�
	my $nflag = int($island->{'itemAbility'}[3]);
	my $nflagk = (!$#HnavyName) ? 1 : int($nflag/$#HnavyName);
	$nflagk = 1 if($nflag && ($nflagk < 1));
	if($HnavyKindMax[$nKind] && ($island->{'shipk'}[$nKind] >= $HnavyKindMax[$nKind] + $nflagk)) {
		logNavyKindMaxOver($id, $name, $comName);
		return 0;
	}

	my($i, $x, $y, $lv, $lv2);

	if ($nSpecial & 0x8) {
		# ��������
		if($HedgeReclaim) { # ��κǳ��������Ω���ԲĤˤ�����
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($nx < $x[0] + $HedgeReclaim) || ($nx > $x[$#x] - $HedgeReclaim) || ($ny < $y[0] + $HedgeReclaim) || ($ny > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "��κǳ���", $point);
				return 0;
			}
		}
		# ���ʤ���ֻ���
		$lv = $landValue->[$nx][$ny];
		if (($land->[$nx][$ny] == $HlandSea) && ($lv == 1)) {
			# �����ʤ����
			$land->[$nx][$ny] = $HlandNavy;
			$landValue->[$nx][$ny] = $nLv;
                        $landValue2->[$nx][$ny] = $nLv2;
			$island->{'navyPort'}++;
			# ��å�����
			logLandSuc($id, $name, $comName, $point);
			return 1;
		} else {
			# ����¾�ϼ���
			my $landKind = $land->[$nx][$ny];
			my $lv       = $landValue->[$nx][$ny];
			my $landName = landName($landKind, $lv);
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
	}

	if($HnavyMaximum && ($island->{'ships'}[4] >= $HnavyMaximum + $nflag)) {
		logNavyMaxOver($id, $name, $comName);
		return 0;
	} elsif($island->{'navyPort'} && $HportRetention && ($island->{'ships'}[4] >= $island->{'navyPort'} * $HportRetention + $nflag)) {
		logFleetMaxOver($id, $island->{'ships'}[4], $comName, "������������");
		return 0;
	} elsif($HfleetMaximum && ($island->{'ships'}[$nNo] >= $HfleetMaximum + int($nflag/4))) {
		logFleetMaxOver($id, $name, $comName, "${ofname}����");
		return 0;
	}

	my($p, $px, $py);
	if($HnavyBuildFlag) {
                my $plane;
                if($HnavyCruiseTurn[$nKind] != 0){
                    $plane = 1;
                }
		($p, $px, $py) = searchNavyPort($island, $nx, $ny, $an[1], $plane, $id);
		if(!$p) {
#		unless(countAroundNavySpecial($island, $nx, $ny, 0x8, $an[1], 0)) {
			# �������¤����ˤϷ�����ɬ��

			logNavyNoPort($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		$lv = $landValue->[$nx][$ny];
		# �������Ǥʤ���з�¤�Ǥ��ʤ�
		unless ($land->[$nx][$ny] == $HlandSea && (!$lv || !$HnavyBuildTurn[$nKind])){
			logNavyNoSea($id, $name, $comName, "($nx, $ny)");
			return 0;
		}
		my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, $goalx, $goaly) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);
		# �����η�¤��٥��ǧ
		if($HmaxComPortLevel && ($HcomNavyNumber[(expToLevel($HlandNavy, $pExp) - 1)] < $nKind)) {
			logNavyNoExp($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		# ����������
		$land->[$nx][$ny] = $HlandNavy;
		$landValue->[$nx][$ny] = $nLv;
	        $landValue2->[$nx][$ny] = $nLv2;
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$nNo]++;
		$island->{'ships'}[4]++;

		# ��ư�Ѥߤˤ���
		$HnavyMove[$id][$nx][$ny] = 2;

		# ����̾
		my $nName = $HnavyName[$nKind];

		# ��å�����
                if($plane == 0){
		    logNavyBuild($id, $name, $ofname, $nName, "($nx, $ny)");
                }else{
		    logNavyBuild2($id, $name, $ofname, $nName, "($nx, $ny)");
                }

		# ����or����˷и��ͤ��Ե�����
                if($pKind == 0){
		    $pExp += $HnavyBuildExp[$nKind];
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # �Ҷ���ȯ�ʤʤ顢$wait������
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = $HnavyCruiseTurn[$nKind];
                    }
                }else{
		    $pExp += int($HnavyBuildExp[$nKind] / 3);
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # �Ҷ���ȯ�ʤʤ顢$wait������
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = int($HnavyCruiseTurn[$nKind] / 3);
                    }
                }

		($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait + 1, $pHp, 31, 31);




		return 1;
	} else {
                # ����else�Ͼ�����������ȤϤʤ���ǡ�����
		if($island->{'navyPort'} < 1) {
			# �������¤����ˤϷ�����ɬ��
			logNavyNoPort($id, $name, $comName);
			return 0;
		}

		# ��äȤ�ᤤ�����η�¤��٥��ǧ
		($p, $px, $py) = searchNavyPort($island, $nx, $ny, 0, $id);
		my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, $goalx, $goaly) = navyUnpack($landValue->[$px][$py],$landValue->[$px][$py]);
		if($HmaxComPortLevel && ($HcomNavyNumber[(expToLevel($HlandNavy, $pExp) - 1)] < $nKind)) {
			logNavyNoExp($id, $name, $comName, "($nx, $ny)");
			return 0;
		}
		foreach $i (0..$island->{'pnum'}) {
			$x = $island->{'rpx'}[$i];
			$y = $island->{'rpy'}[$i];
			$lv = $landValue->[$x][$y];
			$lv2 = $landValue2->[$x][$y];

			# ��������õ��
			next unless (($land->[$x][$y] == $HlandSea) && !$lv);

			# ����������
			$land->[$x][$y] = $HlandNavy;
			$landValue->[$x][$y] = $nLv;
			$island->{'shipk'}[$nKind]++;
			$island->{'ships'}[$nNo]++;
			$island->{'ships'}[4]++;

			# ��ư�Ѥߤˤ���
			$HnavyMove[$id][$x][$y] = 2;

			# ����̾
			my $nName = $HnavyName[$nKind];

			# �����˷и���
			$pExp += $HnavyBuildExp[$nKind];
			$pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
			($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, 31, 31);

			return 1;
		}
	}

	# �������������볤���ʤ�
	logNavyNoSea($id, $name, $comName);
	return 0;
}


# �Ҷ�������ȯ��
sub buildNavy2 {
        # ��� ���Υ롼����Ǥϡ��������åȤ����$island�Ȥ��ư���$tIsland�ǤϤʤ�
	my($island, $comName, $nKind, $nNo, $nx, $ny, $nId) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};
	my $point     = "($nx, $ny)";
        my $landcount;

        # ���ޥ�������Ԥ���ǡ�������
	my $nn = $HidToNumber{$nId};
	my $nIsland = $Hislands[$nn];
	my $nName      = islandName($nIsland);

	# ������Τ�
	$nNo--;
	if ($nNo < 0) {
		$nNo = 0;
	} elsif ($nNo > 3) {
		$nNo = 3;
	}

        # ����ͽ���Ϥ��������ɤ�����˥����å�
        my ($asase) = 0;
	if (($land->[$nx][$ny] == $HlandSea) && ($landValue->[$nx][$ny] == 1)) {
            $asase = 1;
        }

	my ($nLv, $nLv2);
	    ($nLv, $nLv2) = navyPack($nId, 0, 0, $asase, 0, 0, $nNo, $nKind, $HnavyCruiseTurn[$nKind] + 1, $HnavyHP[$nKind], 31, 31);#�Ҷ�������

	my $nSpecial = $HnavySpecial[$nKind];
	my $ofname = $island->{'fleet'}->[$nNo];

	# ��¤��٥��ǧ
	if($HmaxComNavyLevel) {
		my $navyComLevel = gainToLevel($nIsland->{'gain'});
		if($HcomNavyNumber[$navyComLevel-1] < $nKind) {
			logNavyNoExp($id, $name, $comName);
			return 0;
		}
	}

	# ��ͭ��ǽ�����������å�
	my $nflag = int($island->{'itemAbility'}[3]);
	my $nflagk = (!$#HnavyName) ? 1 : int($nflag/$#HnavyName);
	$nflagk = 1 if($nflag && ($nflagk < 1));
	if($HnavyKindMax[$nKind] && ($island->{'shipk'}[$nKind] >= $HnavyKindMax[$nKind] + $nflagk)) {
		logNavyKindMaxOver($id, $name, $comName);
		return 0;
	}

	my($i, $x, $y, $lv, $lv2);

	if($HnavyMaximum && ($island->{'ships'}[4] >= $HnavyMaximum + $nflag)) {
		logNavyMaxOver($id, $name, $comName);
		return 0;
	} elsif($island->{'navyPort'} && $HportRetention && ($island->{'ships'}[4] >= $island->{'navyPort'} * $HportRetention + $nflag)) {
		logFleetMaxOver($id, $name, $comName, "������������");
		return 0;
	} elsif($HfleetMaximum && ($island->{'ships'}[$nNo] >= $HfleetMaximum + int($nflag/4))) {
		logFleetMaxOver($id, $name, $comName, "${ofname}����");
		return 0;
	}

	my($p, $px, $py);
	if($HnavyBuildFlag) {
                my $plane;
                if($HnavyCruiseTurn[$nKind] != 0){
                    $plane = 1;
                }
		($p, $px, $py) = searchNavyPort($island, $nx, $ny, $an[1], $plane, $nId);
		if(!$p) {
#		unless(countAroundNavySpecial($island, $nx, $ny, 0x8, $an[1], 0)) {
			# �������¤����ˤϷ�����ɬ��

			logNavyNoPort($nId, $name, $comName, "($nx, $ny)");
			return 0;
		}

		my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, $goalx, $goaly) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);

		# ���Ǥʤ���з�¤�Ǥ��ʤ�
		unless ($land->[$nx][$ny] == $HlandSea){
			logNavyNoSea($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		# ����������
		$land->[$nx][$ny] = $HlandNavy;
		$landValue->[$nx][$ny] = $nLv;
	        $landValue2->[$nx][$ny] = $nLv2;
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$nNo]++;
		$island->{'ships'}[4]++;

		# ��ư�Ѥߤˤ���
		$HnavyMove[$id][$nx][$ny] = 2;

		# ����̾
		my $nName = $HnavyName[$nKind];

		# ��å�����
                if($plane == 0){
		    logNavyBuild($id, $nName, $ofname, $nName, "($nx, $ny)");
                }else{
		    logNavyBuild2($id, $nName, $ofname, $nName, "($nx, $ny)", $nId);
                }

		# ����or����˷и��ͤ��Ե�����
                if($pKind == 0){
		    $pExp += $HnavyBuildExp[$nKind];
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # �Ҷ���ȯ�ʤʤ顢$wait������
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = $HnavyCruiseTurn[$nKind];
                    }
                }else{
		    $pExp += int($HnavyBuildExp[$nKind] / 3);
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # �Ҷ���ȯ�ʤʤ顢$wait������
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = int($HnavyCruiseTurn[$nKind] / 3);
                    }
                }

		($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait + 1, $pHp, 31, 31);

		return 1;
	}

	# �������������볤���ʤ�
	logNavyNoSea($id, $name, $comName);
	return 0;
}



# �����ﳲ�롼����
sub wideDamage {
	my($id, $name, $island, $x, $y) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($sx, $sy, $i, $landKind, $landName, $lv, $point);

	foreach $i (0..18) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ�
		next if(($sx < 0) || ($sy < 0));

		$landKind = $land->[$sx][$sy];
		$lv = $landValue->[$sx][$sy];
		$landName = landName($landKind, $lv);
		$point = "($sx, $sy)";

		# �ϰϤˤ��ʬ��
		if($i < 7) {
			# �濴�������1�إå���
			if($landKind == $HlandSea) {
				$landValue->[$sx][$sy] = 0;
				next;
			} elsif(($landKind == $HlandSbase) ||
					($landKind == $HlandOil) ||
					(($landKind == $HlandCore) && int($lv / 10000))) {
				logWideDamageSea2($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			} elsif($landKind == $HlandSeaMine) {
				logWideDamageMonster($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			} elsif($landKind == $HlandComplex) {
				# ʣ���Ϸ��ʤ������Ϸ�
				my $cKind = (landUnpack($lv))[1];
				if($HcomplexAfter[$cKind]->{'wide1'}[0] ne '') {
					$land->[$sx][$sy] = $HcomplexAfter[$cKind]->{'wide1'}[0];
					$landValue->[$sx][$sy] = $HcomplexAfter[$cKind]->{'wide1'}[1];
					$island->{'complex'}[$cKind]--;
					logWideDamageMonster($id, $name, $landName, $point);
				}
			} elsif(($landKind == $HlandMonster) || ($landKind == $HlandHugeMonster)){
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				$land->[$sx][$sy] = $HlandSea;
				if (($i == 0) || ($mFlag & 2)) {
					# ��
					$landValue->[$sx][$sy] = 0;
					logWideDamageMonsterSea2($id, $name, $landName, $point);
				} else {
					# ����
					$landValue->[$sx][$sy] = 1;
					logWideDamageMonsterSea($id, $name, $landName, $point);
				}
			} elsif($landKind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$land->[$sx][$sy] = $HlandSea;
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if(($i != 0) && ($nSpecial & 0x8)) {
					# ��������
					$landValue->[$sx][$sy] = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logWideDamageSea($id, $name, $landName, $point);
				} else {
					# ����¾�ϳ�
					$landValue->[$sx][$sy] = 0;
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
					}
					logWideDamageMonster($id, $name, $landName, $point);
				}
			} else {
				logWideDamageSea($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandSea;
				if($i == 0) {
					# ��
					$landValue->[$sx][$sy] = 0;
				} else {
					# ����
					$landValue->[$sx][$sy] = 1;
				}
			}
		} else {
			# 2�إå���
			if(($landKind == $HlandSea) ||
				($landKind == $HlandOil) ||
				($landKind == $HlandSeaMine) ||
				($landKind == $HlandWaste) ||
				($landKind == $HlandMountain) ||
				($landKind == $HlandSbase) ||
				(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				next;
			} elsif($landKind == $HlandComplex) {
				# ʣ���Ϸ��ʤ������Ϸ�
				my $cKind = (landUnpack($lv))[1];
				if($HcomplexAfter[$cKind]->{'wide2'}[0] ne '') {
					$land->[$sx][$sy] = $HcomplexAfter[$cKind]->{'wide2'}[0];
					$landValue->[$sx][$sy] = $HcomplexAfter[$cKind]->{'wide2'}[1];
					$island->{'complex'}[$cKind]--;
					logWideDamageMonster($id, $name, $landName, $point);
				}
			} elsif($landKind == $HlandMonster) {
				logWideDamageMonster($id, $name, $landName, $point);
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if ($mFlag & 2) {
					$land->[$sx][$sy] = $HlandSea;
				} else {
					$land->[$sx][$sy] = $HlandWaste;
				}
				$landValue->[$sx][$sy] = 0;
			} elsif($landKind == $HlandHugeMonster) {
				logWideDamageMonster($id, $name, $landName, $point);
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
				if ($mFlag & 2) {
					$land->[$sx][$sy] = $HlandSea;
				} else {
					$land->[$sx][$sy] = $HlandWaste;
				}
				$landValue->[$sx][$sy] = 0;
				if($mHflag == 0) {
					my($j, $ssx, $ssy);
					foreach $j (1..6) {
						next if($HhugeMonsterImage[$mKind][$j] eq '');
						$ssx = $sx + $ax[$j];
						$ssy = $sy + $ay[$j];
						# �Ԥˤ�����Ĵ��
						$ssx-- if(!($ssy % 2) && ($sy % 2));
						$ssx = $correctX[$ssx + $#an];
						$ssy = $correctY[$ssy + $#an];
						# �ϰϳ�
						next if(($ssx < 0) || ($ssy < 0));

						next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
						# �����Ǥμ��Ф�
						my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
						next if($mHflag2 != $j);
						if ($mFlag2 & 2) {
							# ���ˤ���
							$land->[$ssx][$ssy] = $HlandSea;
							$landValue->[$ssx][$ssy] = $mSea2;
						} else {
							# Φ�Ϥˤ���
							$land->[$ssx][$ssy] = $HlandWaste;
							$landValue->[$ssx][$ssy] = 0;
						}
					}
				}
			} elsif($landKind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$land->[$sx][$sy] = $HlandSea;
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if ($nSpecial & 0x8) {
					# ��������
					$landValue->[$sx][$sy] = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logWideDamageSea($id, $name, $landName, $point);
				} else {
					# ����¾�ϳ�
					$landValue->[$sx][$sy] = 0;
					if(defined $n) {
						$Hislands[$n]->{'ships'}[$nNo]--;
						$Hislands[$n]->{'ships'}[4]--;
					}
					logWideDamageMonster($id, $name, $landName, $point);
				}
			} elsif(($landKind == $HlandBouha) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 1))) {
				logWideDamageSea($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 1;
				$island->{'bouha'}--;
			} else {
				logWideDamageWaste($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
			}
		}
	}
}

# ���褷�Ƥ뤫Ƚ�ꤹ��(����֤��������)
sub chkWarIsland {
	my($id, $tId) = @_;
	return 2 if(($id == 0) || ($tId == 0));
	my($i);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($wid1) = $HwarIsland[$i+1];
		my($wid2) = $HwarIsland[$i+2];
		my($tn1) = $HidToNumber{$wid1};
		my($tn2) = $HidToNumber{$wid2};
		if(($tn1 eq '') || ($tn2 eq '')){
			splice(@HwarIsland,$i,4);
			$i -= 4;
			next;
		}
		if((($wid1 == $id) && ($wid2 == $tId)) || (($wid1 == $tId) && ($wid2 == $id))){
			if($HwarIsland[$i] > $HislandTurn) {
				# ���������(ͱͽ����)
				return 1;
			} else {
				# ������
				return 2;
			}
		}
	}
	return 0;
}

# ���褷�Ƥ뤫Ƚ�ꤹ��(������������)
sub chkWarIslandOR {
	my($id, $tId) = @_;
	return 2 if(($id == 0) || ($tId == 0));
	my($i, %chkFlag);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($wid1) = $HwarIsland[$i+1];
		my($wid2) = $HwarIsland[$i+2];
# chkWarIsland�Τ��Ȥ˻Ȥ��֤����פʽ���
#		my($tn1) = $HidToNumber{$HwarIsland[$i+1]};
#		my($tn2) = $HidToNumber{$HwarIsland[$i+2]};
#		if(($tn1 eq '') || ($tn2 eq '')){
#			splice(@HwarIsland,$i,4);
#			$i -= 4;
#			next;
#		}
		$chkFlag{$wid1} = $wid2;
		$chkFlag{$wid2} = $wid1;
	}
	if($chkFlag{$id}) {
		return $chkFlag{$id};
	} elsif($chkFlag{$tId}) {
		return $chkFlag{$tId};
	}
	return 0;
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���
# ��4����:���2
# �̾��
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# �ٱ��
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# ��̩��
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# ��Ͽ��
sub logHistory {
	push(@HhistoryLogPool,"$HislandTurn,$_[0]\n");
}

# ���񤭽Ф�
sub logFlush {
	open(LOUT, ">${HdirName}/0$HlogData");
	# �����ս�ˤ��ƽ񤭽Ф�
	foreach (reverse(@HlogPool, @HlateLogPool, @HsecretLogPool)) {
		next if($_ eq ',,,,,');
		print LOUT $_ . "\n";
	}
	close(LOUT);

	# ��Ͽ���񤭽Ф���Ĵ��
	open(HIN, "${HdirName}/hakojima.his");
	my @lines = <HIN>;
	close(HIN);
	@lines = (@lines, @HhistoryLogPool);
	while ($HhistoryMax < @lines) { shift @lines; }
	open(HOUT, ">${HdirName}/hakojima.his");
	print HOUT @lines;
	close(HOUT);

	undef @HsecretLogPool;
	undef @HlateLogPool;
	undef @HlogPool;
	undef @HhistoryLogPool;
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ��ݥ���Ȼ�����ƥ�ץ�
sub logIslpnt {
	my($id, $name, $point, $tId, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}$str",$id, $tId);
}

# �����ƥ�ȯ��
sub logItemGetLucky {
	my($id, $name, $point, $itemName, $str) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��${str}��<B>$itemName</B>��ȯ�����ޤ�����",$id);
}

# �����ƥ�ȯ��2
sub logItemGetLucky2 {
	my($id, $name, $point, $itemName, $str) = @_;
	logOut("��--- ${HtagName_}${point}${H_tagName}��${str}��${HtagMoney_}${itemName}${H_tagMoney}��ȯ�����ޤ�����",$id);
}

# �����ƥ�ü�
sub logItemLost {
	my($id, $name, $itemName, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${str}��<B>$itemName</B>���ü����ޤ�����",$id);
}

# ����������õ��������
sub logProbeDestroy {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}��${HtagName_}${nName}${H_tagName}������õ�����<B>�̿������䤨�ޤ���</B>��<B>$nName</B>��${HtagDisaster_}����${H_tagDisaster}�����褦�Ǥ���",$id, $nId);
}

# ����õ������μ���
sub logTansaku {
	my($id, $name, $nId, $lName, $point, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��������ȯ����${HtagMoney_}${str}${H_tagMoney}�β��ͤ����뤳�Ȥ��狼��ޤ�����",$id, $nId);
	logHistory("${HtagName_}${name}${H_tagName}��<B>$lName</B>��������ȯ����");
}

# ��±�԰�
sub logPirates {
	my($id, $name, $point, $nId, $nName, $nPoint, $str) = @_;
	logOut("${HtagName_}${name}$nPoint${H_tagName}��<B>$nName</B>��${HtagName_}$point${H_tagName}��������$str��<B>άå</B>���ޤ�����",$id, $nId);
}

# ���������������
sub logSeaMineDestroy {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}��${HtagName_}${nName}${H_tagName}��<B>������ܿ�������</B>��<B>$nName</B>��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id, $nId);
}

# ����������ǥ��᡼��
sub logSeaMineDamage {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}��${HtagName_}${nName}${H_tagName}��<B>������ܿ�</B>��<B>$nName</B>�Ϲ����ʮ���Ф��ޤ�����",$id, $nId);
}

# ���á�����ǻ���
sub logMonsSeaMineDestroy {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>���ܿ���<B>$mName</B>���ϿԤ��������${HtagDisaster_}�ݤ�ޤ���${H_tagDisaster}��",$id, $mId);
}

# ���á�����ǻ���
sub logMonsSeaMineDamage {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>���ܿ���<B>$mName</B>�϶줷���������㤷�ޤ�����",$id, $mId);
}

# �������⡢���ä��ߥ����빶�⡢�����̿��
sub logNavySeaMine {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>�Ͼä����Ӥޤ�����",$id, $nId);
}

# ���­��ʤ�
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������­�Τ�����ߤ���ޤ�����",$id);
}

# ����­��ʤ�
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ����߿�����­�Τ�����ߤ���ޤ�����",$id);
}

# ��ȯ���֤ˤ�뼺��
sub logDevelopTurnFail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�${AfterName}��ȯ������ľ���<B>��ȯ����</B>���ä�������ߤ���ޤ�����",$id);
}

# ��ȯ����Ķ��ˤ�뼺��
sub logDevelopTurnFail2 {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�${AfterName}��ȯ������ľ���<B>��ȯ���֤�᤮�Ƥ���</B>������ߤ���ޤ�����",$id);
}

# �ǰ�ǽ�ϴ������ɸ����Ƥ��ʤ�����������
sub logTradeFail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>�����ǽ�ʴ������ɸ�����Ƥ��ʤ�</B>������ߤ���ޤ�����",$id);
}

# ������ư������
sub logMoveFail {
	my($id, $name, $point,$str, $tId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}�������Ф����ư�����$str�¹Ԥ���ޤ���Ǥ�����",$id, $tId);
}

# ����Ϥʤ餷
sub logAllPrepare {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}$comName${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ��ͭ��ǽ�������С�(���롦�����顦ʣ���Ϸ�)
sub logOverFail {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ���ͭ��ǽ����Ķ���뤿����ߤ���ޤ�����",$id);
}

# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$kind</B>���ä�������ߤ���ޤ�����",$id);
}

# �Ϸ��ʳ�������Ǽ���
sub logLandFail2 {
	my($id, $name, $comName, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>$kind</B>������ߤ���ޤ�����",$id);
}

# �����Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ�Φ�Ϥ��ʤ��ä�������ߤ���ޤ�����",$id);
}

# �������ʤ���������η�¤����
sub logNavyNoPort {
	my($id, $name, $comName, $point, $tId) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ��������������<B>�������ʤ�</B>������ߤ���ޤ�����",$id, $tId);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ��᤯��<B>�������ʤ�</B>������ߤ���ޤ�����",$id, $tId);
	}
}

# �����ʤ���������η�¤����
sub logNavyNoSea {
	my($id, $name, $comName, $point) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ���������������<B>�����ʤ�</B>������ߤ���ޤ�����",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ���������������<B>�������Ǥʤ�</B>������ߤ���ޤ�����",$id);
	}
}

# �и��ͤ��ʤ���������η�¤����
sub logNavyNoExp {
	my($id, $name, $comName, $point) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>��¤���Ѥ�­��ʤ�</B>������ߤ���ޤ�����",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>��¤���Ѥ�­��ʤ�</B>������ߤ���ޤ�����",$id);
	}
}

# ��������������С��ˤ���¤����
sub logNavyMaxOver {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>��ͭ��ǽ��������ۤ���</B>������ߤ���ޤ�����",$id);
}

# ���������������С��ˤ���¤����
sub logNavyKindMaxOver {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>�������̤���ͭ��ǽ����ۤ���</B>������ߤ���ޤ�����",$id);
}

# ������(����)��ͭ��ǽ�����������С��ˤ���¤����
sub logFleetMaxOver {
	my($id, $name, $comName, $nName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>$nName����ͭ��ǽ��������ۤ���</B>������ߤ���ޤ�����",$id);
}

# �������Ѥ�­�ꤺ�˹������
sub logNavyNoShell {
	my($id, $tId, $name, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}��${HtagName_}${nName}${H_tagName}�ι����<B>�������ʤ�</B>������ߤ���ޤ�����",$id,$tId);
}

# ���Ϸ�����
sub logLandSuc {
	my($id, $name, $comName, $point, $tId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id, $tId);
}

# ���Ϸϥ��ޤȤ�
sub logLandSucMatome {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����<br>����<B>��</B> $point",$id);
}

# ����ȯ��
sub logOilFound {
	my($id, $name, $point, $comName, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ�졢<B>���Ĥ��������Ƥ��ޤ���</B>��",$id);
}

# ����ȯ���ʤ餺
sub logOilFail {
	my($id, $name, $point, $comName, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ����������Ĥϸ��Ĥ���ޤ���Ǥ�����",$id);
}

# ���Ĥ���μ���
sub logOilMoney {
	my($id, $name, $lName, $point, $value, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>���顢${HtagMoney_}$value${H_tagMoney}��$str���夬��ޤ�����",$id);
}

# ���ĸϳ�
sub logOilEnd {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>�ϸϳ餷���褦�Ǥ���",$id);
}

# �ɱһ��ߡ��ѵ��ϥ��å�
sub logBombDurableUp {
	my($id, $name, $lName, $point, $num, $hide) = @_;
	if ($hide) {
		logSecret("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>���ѵ��Ϥ�$num���åפ��ޤ�����",$id);
		logOut("������ʤ�����${HtagName_}${name}${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
#		logOut("${HtagName_}${name}$point${H_tagName}��${HtagComName_}Ȳ��${H_tagComName}���Ԥ��ޤ�����",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>���ѵ��Ϥ�$num���åפ��ޤ�����",$id);
	}
}

# �ɱһ��ߡ��ѵ��ϥ��åפ���
sub logBombDurableMax {
	my($id, $name, $lName, $point, $hide) = @_;
	if ($hide) {
		logSecret("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>���ѵ��ϤϤ��Ǥ˺���Ǥ���",$id);
		logOut("������ʤ�����${HtagName_}${name}${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
#		logOut("${HtagName_}${name}$point${H_tagName}��${HtagComName_}Ȳ��${H_tagComName}���Ԥ��ޤ�����",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>���ѵ��ϤϤ��Ǥ˺���Ǥ���",$id);
	}
}

# �ɱһ��ߡ��������å�
sub logBombSet {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>�������֤����å�</B>����ޤ�����",$id);
}

# �ɱһ��ߡ�������ư
sub logBombFire {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�������ֺ�ư����${H_tagDisaster}",$id);
}

# ��ǰ�ꡢȯ��
sub logMonFly {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>�첻�ȤȤ������Ω���ޤ���</B>��",$id);

}

# ��ǰ�ꡢ�
sub logMonDamage {
	my($id, $name, $point) = @_;
	logOut("<B>�����ȤƤĤ�ʤ����</B>��${HtagName_}${name}$point${H_tagName}����������ޤ�������",$id);
}

# ����or�ߥ��������
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logOut("������ʤ�����${HtagName_}${name}${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
}

# �ϥ�ܥ�
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logLandSuc($id, $name, $comName2, $point);

}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)���������åȤ����ʤ�
sub logMsNoTarget {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ��${AfterName}�˿ͤ���������ʤ�������ߤ���ޤ�����",$id);
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ����������ʤ�������ߤ���ޤ�����",$id);
}

# ����ؤΰ�ư����
sub logMoveMissionFleet {
	my($id, $tId, $name, $tName, $point, $no) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${no}����${H_tagName}���Ф�${HtagName_}${tName}${point}${H_tagName}�ؤ�${HtagComName_}��ư����${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
}

# ����ؤΰ�ư�������
sub logMoveMissionFleetLift {
	my($id, $tId, $name, $tName, $point, $no) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${no}����${H_tagName}���Ф�${HtagName_}${tName}${point}${H_tagName}�ؤ�${HtagComName_}��ư����${H_tagComName}��${HtagDisaster_}���${H_tagDisaster}���ޤ�����",$id, $tId);
}

# �����ؤλ�����ѹ�
sub logChangeMission {
	my($id, $tId, $name, $tName, $point, $old, $new) = @_;
	my @status = ('�̾�', '�༣', '���', '����');
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}$point${H_tagName}��${HtagComName_}�����ؤλ����ѹ�${H_tagComName}��Ԥ��ޤ�����${HtagComName_}��$status[$old]��$status[$new]��${H_tagComName}",$id, $tId);
}

# ����ؤλ�����ѹ�
sub logChangeMissionFleet {
	my($id, $tId, $name, $tName, $no, $new) = @_;
	my @status = ('�̾�', '�༣', '���', '����');
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}${H_tagName}��${HtagComName_}${no}����ؤλ����ѹ�${H_tagComName}��Ԥ��ޤ�����${HtagComName_}��������$status[$new]�⡼�ɡ�${H_tagComName}",$id, $tId);
}

# �����ؤλ�����ѹ����褦�Ȥ���������
sub logChangeMissionFail {
	my($id, $tId, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}${H_tagName}�ǹԤä�${HtagComName_}�����ؤλ����ѹ�${H_tagComName}�ϡ��Ź�Υߥ��⤷���������оݤ������Ǥʤ����Ἲ�Ԥ��ޤ�����",$id, $tId);
}

# ���ƹ������
sub logNavyMission {
	my($id, $tId, $name, $tName, $point, $nName, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}$point${H_tagName}��<B>$nName</B>���Ф���${HtagComName_}���ƹ���${H_tagComName}��̿�ᤷ�ޤ�����<BR>��--- ����˵�� �� $str",$id, $tId);
}

# ���ƹ�����ᡧ����
sub logNavyMissionFail {
	my($id, $tId, $name, $tName, $point, $nName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ȯ�ᤷ��${HtagName_}${tName}$point${H_tagName}��<B>$nName</B>���Ф���${HtagComName_}���ƹ���${H_tagComName}�ϡ����Ԥ˽����ޤ�����",$id, $tId);
}

# �������⡢���ä��ߥ����빶��(�ޤȤ�)
sub logNavyMatome {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $tLname, $kind, $str, $pntStr, $nId2) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}��${HtagName_}${nName}${H_tagName}��${HtagName_}${tPoint}${H_tagName}������${tLname}�˸�����${HtagComName_}$kind${H_tagComName}��Ԥ��ޤ�����${str}${pntStr}",$id, $nId, $nId2);
}

# ����ȯ�͡�����¾���Ϸ�
sub logNavyTorpedoNormal {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>�ϳ��������Ȥʤ�ޤ�����",$id, $nId);
}

# ��ˤ�ͷ⡢�Ϻܵ������⡢���ä��ߥ����빶�⡢�ɱһ���(�ѵ��Ϥ���)������(�ѵ��Ϥ���)��ʣ�����(���ϥ�����)
sub logNavyNormalDefence {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>���ﳲ������ޤ�����",$id, $nId);
}

# ��ˤ�ͷ⡢�Ϻܵ������⡢�ԻԷ�
sub logNavyNormalTown {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint, $sName) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$sName</B>�ˤʤ�ޤ�����",$id, $nId);
}

# ��ˤ�ͷ⡢�Ϻܵ������⡢����¾���Ϸ�
sub logNavyNormal {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档���Ӥ����Ǥ��ޤ�����",$id, $nId);
}

# ����ȯ�͡����ä�̿�桢����
sub logNavyTorpedoMonKill {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>���ϿԤ��������${HtagDisaster_}�ݤ�ޤ���${H_tagDisaster}��",$id, $nId, $mId);
}

# ��ˤ�ͷ⡢�Ϻܵ������⡢���ä��ߥ����빶�⡢���ä�̿�桢����
sub logNavyMonKill {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>���ϿԤ���${HtagDisaster_}�ݤ�ޤ���${H_tagDisaster}��",$id, $nId, $mId);
}

# �������⡢�ĳ���̿�桢��������
sub logNavyWreckDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>�ϳ��������Ȥʤ�ޤ�����",$id, $nId);
}

# �������⡢���ä��ߥ����빶�⡢������̿�桢����
sub logNavyPortDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id, $nId, $nId2);
}

# �������⡢���ä��ߥ����빶�⡢������̿�桢����
sub logNavyShipDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id, $nId, $nId2);
}

# �������⡢���ä��ߥ����빶�⡢���ä�̿�桢���᡼��
sub logNavyMonster {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>�϶줷��������Ӭ���ޤ�����",$id, $nId, $mId);
}

# �������⡢���ä��ߥ����빶�⡢������̿�桢���᡼��
sub logNavyDamage {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("��--- ${HtagName_}${fPoint}${H_tagName}��<B>$fName</B>��̿�档<B>$fName</B>�Ϲ����ʮ���Ф��ޤ�����",$id, $nId, $nId2);
}

# ���äλ���
sub logMonMoney {
	my($tId, $mName, $value) = @_;
	logOut("��--- <B>$mName</B>�λĳ��ˤϡ�<B>$value$HunitMoney</B>���ͤ��դ��ޤ�����", $tId);
}

# �ߥ�������̱����
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}${H_tagName}�ϲ����������줿�褦�Ǥ���",$id);
}

# �����ɸ�
sub logMonsSend {
	my($id, $tId, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>��¤����</B>���¤��${HtagName_}${tName}${H_tagName}�����ꤳ�ߤޤ�����",$id, $tId);
}

# ST�����ɸ�
sub logMonsSendST {
	my($id, $tId, $name, $tName) = @_;
	logSecret("${HtagName_}${name}${H_tagName}��<B>��¤����</B>���¤��${HtagName_}${tName}${H_tagName}�����ꤳ�ߤޤ�����",$id);
	logLate("<B>���Ԥ�</B>��<B>��¤����</B>���¤��${HtagName_}${tName}${H_tagName}�����ꤳ�ߤޤ�����",$tId);
}

# ��ⷫ��
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ͧ��������
sub logAmity {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>$tName</B>��${HtagComName_}ͧ�����ǧ��${H_tagComName}���ޤ�����",$id, $tId);
}

# ͧ������
sub logAmityEnd {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>$tName</B>�ؤ�${HtagComName_}ͧ����ǧ����˴�${H_tagComName}���ޤ�����",$id, $tId);
}

# ͧ����������
sub logAmityEndFail {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}���¹Ԥ��褦�Ȥ���<B>$tName</B>�ؤ�${HtagComName_}ͧ����ǧ���˴�${H_tagComName}��<B>�����ɸ���Τ�����Ĥ���ޤ���</B>�Ǥ�����",$id, $tId);
}

# ͧ�������������С�
sub logAmityMaxOver {
	my($id, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>$tName</B>�ؤ�<B>ͧ����ǧ��˼���</B>���ޤ���${HtagComName_}��ǧ���ǽ����ȿ��${H_tagComName}��",$id);
}

# �̤�Ʊ����������Ƥ���
sub logLeaderAlready {
	my($id, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagName_}${tName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϡ����Ǥ˼�ʬ��Ʊ����������Ƥ��뤿����ߤ���ޤ�����",$id);
}

# �̤�Ʊ���˲������Ƥ���
sub logOtherAlready {
	my($id, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagName_}${tName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϡ����Ǥ��̤�Ʊ���˲������Ƥ��뤿����ߤ���ޤ�����",$id);
}

# ����
sub logAlly {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}����${HtagName_}${allyName}${H_tagName}�٤�${HtagNumber_}����${H_tagNumber}���ޤ�����", $id, $tId);
}

# æ��
sub logAllyEnd {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}����${HtagName_}${allyName}${H_tagName}�٤���${HtagDisaster_}æ��${H_tagDisaster}���ޤ�����", $id, $tId);
}

# ������ǽ����������С�
sub logAllyMaxOver {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}�Ρ�${HtagName_}${allyName}${H_tagName}�٤ؤ�<B>�����������˴�</B>����ޤ���${HtagComName_}�ʲ�����ǽ����ȿ��${H_tagComName}��", $id, $tId);
}

# ������ǽ����
sub logAllyVeto {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}�Ρ�${HtagName_}${allyName}${H_tagName}�٤ؤ�<B>�����������˴�</B>����ޤ���${HtagComName_}�ʵ��ݸ�ȯư��${H_tagComName}��", $id, $tId);
}

# ͢��
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagFood_}$value$HunitFood${H_tagFood}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}

# ͢��
sub logBuy {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagFood_}$value$HunitFood${H_tagFood}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}

# ���
sub logAid {
	my($id, $tId, $name, $tName, $comName, $str, $str2) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagName_}${tName}${H_tagName}��$str��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����(�����:2��)",$id, $tId);
}

# �رĳ��ؤα�����Ե��ġ�
sub logAidFail {
	my($id, $tId, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagName_}${tName}${H_tagName}�ؤ�${HtagComName_}${comName}${H_tagComName}�ϵ��Ĥ���Ƥ��ʤ�������ߤ��ޤ�����",$id, $tId);
}

# ����ػ�
sub logNotAvail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϵ��Ĥ���Ƥ��ʤ�������ߤ��ޤ�����",$id);
}

# ��ȯ���֤Τ��Ἲ��
sub logLandNG {
	my($id, $name, $comName, $cancel) = @_;
	logOut("${HtagName_}${name}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>$cancel</B>���¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# Ͷ�׳�ư
sub logPropaganda {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ����
sub logGiveup {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}���������졢<B>̵��${AfterName}</B>�ˤʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}����������<B>̵��${AfterName}</B>�Ȥʤ롣");
}

# ̵�Ͳ��ݸ�
sub logAutoKeep {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ο͸�������<B>��ȯ����</B>������ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}��<B>��ȯ���֤�����</B>��");
}

# ����
sub logGiveup_no_do_fight {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ϵ�������Ʈ�԰٤�Ԥ�ʤ��ä����ᡢ<B>����</B>���ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}����������Ʈ�԰٤�Ԥ�ʤ��ä����ᡢ<B>����</B>��");
}

# ����
sub logDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}����ͤ����ʤ��ʤꡢ<B>̵��${AfterName}</B>�ˤʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}���ͤ����ʤ��ʤ�<B>̵��${AfterName}</B>�Ȥʤ롣");
}

# ����(���Х��Х�⡼�ɡ��ȡ��ʥ��ȥ⡼��)
sub logTDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ϡ�<B>����</B>���׷���ʤ��ʤ�ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}��<B>����</B>���롣");
}

# ���ǲ���(�رĥ⡼�ɡ����Х��Х�⡼�ɡ��ȡ��ʥ��ȥ⡼��)
sub logTDead2PD {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ϡ�����������<B>������Υæ</B>���ޤ����������ˤϻ��֤������ꤽ���Ǥ����ڴ����ͤ��������",$id);
	logHistory("${HtagName_}${name}${H_tagName}��<B>������Υæ</B>���롣");
}

# ����
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}

# ����(��°����)����
sub logNavyCome {
	my($id, $name, $nName, $point, $lName) = @_;
	logOut("${HtagName_}${name}${H_tagName}�˽�°������<B>$nName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>���ư���Ƥ��ޤ���",$id);
}

# ��������(������)
sub logCoreRandomBuild {
	my($id, $name, $nName, $point, $lName) = @_;
	if($HcoreHide) {
		logSecret("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$nName</B>�и�����",$id);
		logOut("${HtagName_}${name}$point${H_tagName}��<B>$nName</B>�и�����",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$nName</B>�и�����",$id);
	}
}

# ���ø���
sub logMonsCome {
	my($id, $name, $mName, $point, $lName) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>���ư���Ƥ��ޤ���",$id);
}

# ����ư��
sub logMonsMove {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>��Ƨ�߹Ӥ餵��ޤ�����",$id, $mId);
}

# ������ð�������
sub logMonsRebody {
	my($id, $name, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$mName</B>���Τΰ������������ޤ�����",$id, $mId);
}

# ����ư���ʳ���
sub logMonsMoveSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>����ư���Ƥ��ޤ���",$id, $mId);
}

# ���á������򽱤�
sub logMonsAttackNavy {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>�˽����Ƥ��ޤ���",$id, $mId);
}

# ���á����λ��ߤ��˲�
sub logMonsBreakSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>�˽������˲�����ޤ�����",$id, $mId);
}

# ���á��ɱһ��ߤ�Ƨ��
sub logMonsMoveDefence {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("<B>$mName</B>��${HtagName_}${name}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}�μ������֤���ư����</B>",$id, $mId);
}

# ����ư��
sub logNavyMoveSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>���ҹԤ��Ƥ��ޤ���",$id, $mId);
}

# ������������
sub logNavyMoveAttack {
	my($id, $name, $nId, $nPoint, $nName, $nId2, $fPoint, $fName) = @_;
	logOut("${HtagName_}${name}$nPoint${H_tagName}��${HtagName_}${nName}${H_tagName}��${HtagName_}${fPoint}${H_tagName}������${HtagName_}${fName}${H_tagName}��${HtagComName_}�������ꡪ${H_tagComName}<B>$fName</B>���Ȥ�${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id, $nId, $nId2);
}

# Φ�Ϸ���
sub logNavyMoveDestroy {
	my($id, $name, $lName, $point, $mName, $mId, $mode) = @_;
	my $str = '���褦��';
	$str = '' if($mode);
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>$mName</B>������ҹ�${str}���Ƥ��ޤ���",$id, $mId);
}

# ������¤
sub logNavyBuild {
	my($id, $name, $nNo, $nName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${nNo}�����${nName}</B>���¤��${HtagName_}$point${H_tagName}���������ޤ�����",$id);
}

# �����ɸ������ԡ���ư
sub logNavySend {
	my($id, $fId, $tId, $name, $tName, $fleet, $fSend) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${fleet}</B>��${HtagName_}${tName}${H_tagName}${fSend}���ޤ�����",$id, $fId, $tId);
}

# �����ɸ������ԡ���ư�δ�����
sub logNavySendShip {
	my($id, $tId, $str, $fSend) = @_;
	logOut("��--- ${fSend}���� �� $str",$id, $tId);
}

# �����ɸ������ԡ���ư���褦�Ȥ����������ʤ�
sub logNavySendNone {
	my($id, $name, $tName, $fleet, $fSend) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${fleet}</B>��${HtagName_}${tName}${H_tagName}${fSend}���褦�Ȥ��ޤ��������¹Բ�ǽ�ʴ��⤬����ޤ���Ǥ�����",$id);
}

# �����ɸ������ԡ���ư���褦�Ȥ���������
sub logNavySendNoArea {
	my($id, $name, $tName, $fleet, $fSend, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${fleet}</B>��${HtagName_}${tName}${H_tagName}${fSend}���褦�Ȥ��ޤ����������Ԥ��ޤ�����$str",$id);
}

# ��������
sub logNavyForm {
	my($id, $name, $point, $fleet, $old, $new) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>��${old}���⤫��${new}����˽�°���ѹ����ޤ�����",$id);
}

# �����������褦�Ȥ���������
sub logNavyFormFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>������������뤳�ȤϤǤ��ޤ���",$id);
}

# �������� �����⤢�������ͭ�����������С��ˤ�뼺��
sub logNavyFormMaxOver {
	my($id, $name, $point, $fleet, $old, $new) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��${old}�����°<B>${fleet}</B>�ϴ��������Ǥ��ޤ���Ǥ�����(${new}����δ�����ͭ�������С�)",$id);
}

# ��ɸ�ϻ���
sub logNavyTarget {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>�ϡ�̱�֤�ʧ���������ޤ�����",$id);
}

# ��ɸ�ϻ��ꤷ�褦�Ȥ���������
sub logNavyTargetFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>����Ҥ��뤳�ȤϤǤ��ޤ���",$id);
}

# �����˴�
sub logNavyDestroy {
	my($id, $name, $point, $fleet, $tId) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>���˴����ޤ�����",$id, $tId);
}

# �����˴����褦�Ȥ���������
sub logNavyDestroyFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>���˴����뤳�ȤϤǤ��ޤ���",$id);
}

# �ĳ�����
sub logNavyWreckRepair {
	my($id, $name, $point, $fleet, $cost, $nName) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>��${cost}${HunitMoney}�ǽ�����<B>$nName</B>���������ޤ�����",$id);
}

# �ĳ��������褦�Ȥ���������
sub logNavyWreckRepairFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>�������뤳�ȤϤǤ��ޤ���",$id);
}

# �ĳ����� �����⤢����δ�����ͭ�������С��ˤ�뼺��
sub logNavyWreckRepairMaxOver {
	my($id, $name, $point, $fleet, $nName) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>�������뤳�ȤϤǤ��ޤ���(${nName}�δ�����ͭ�������С�)",$id);
}

# �ĳ����
sub logNavyWreckSell {
	my($id, $name, $point, $fleet, $cost) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>��${cost}${HunitMoney}����Ѥ��ޤ�����",$id);
}

# �ĳ���Ѥ��褦�Ȥ�������ȯ��
sub logNavyWreckSellLucky {
	my($id, $name, $point, $fleet, $cost) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>������夲���Ȥ���${cost}${HunitMoney}��<B>���</B>��ȯ������ޤ�����",$id);
}

# �ĳ���Ѥ��褦�Ȥ���������
sub logNavyWreckSellFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${fleet}</B>����Ѥ��뤳�ȤϤǤ��ޤ���",$id);
}

# ��������
sub logNavyShipRepair {
	my($id, $name, $tId) = @_;
	logOut("<B>��������</B>(����${HtagName_}${name}${point}${H_tagName})",$id,$id,$tId);
}

# ��������
sub logNavyShipRepairM {
	my($id, $tId, $str) = @_;
	my($name) = islandName($Hislands[$HidToNumber{$tId}]) if (defined $HidToNumber{$tId});
	logOut("�� ${HtagName_}${name}${point}${H_tagName}��°���� �� $str��������Ԥ��ޤ�����",$id,$tId);
}

# �����������­
sub logNavyShipSupplyFailM {
	my($id, $tId, $str) = @_;
	my($name) = islandName($Hislands[$HidToNumber{$tId}]) if (defined $HidToNumber{$tId});
	logOut("�� ${HtagName_}${name}${point}${H_tagName}��°���� �� $str�����ʪ����­���Ƥ��ޤ���",$id,$tId);
}

# �к�
sub logFire {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�к�${H_tagDisaster}�ˤ��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id);
}

# ��¢��
sub logMaizo {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}�Ǥ�${HtagComName_}$comName${H_tagComName}��ˡ�<B>$value$HunitMoney�����¢��</B>��ȯ������ޤ�����",$id);
}

# �Ͽ�ȯ��
sub logEarthquake {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}���絬�Ϥ�${HtagDisaster_}�Ͽ�${H_tagDisaster}��ȯ������",$id);
}

# �Ͽ��ﳲ
sub logEQDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id);
}

# ������­�ﳲ
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id);
}

# ����ȯ��
sub logTsunami {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�ն��${HtagDisaster_}����${H_tagDisaster}ȯ������",$id);
}

# �����ﳲ
sub logTsunamiDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ���������ޤ�����",$id);
}

# �����ﳲ(�����˥��᡼��)
sub logTsunamiDamageNavy {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ����᡼���򤦤��ޤ�����",$id);
}

# �����ﳲ(��������)
sub logTsunamiDamageNavyDestroy {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ��${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id);
}

# ����ȯ��
sub logTyphoon {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagDisaster_}����${H_tagDisaster}��Φ����",$id);
}

# �����ﳲ
sub logTyphoonDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�����Ф���ޤ�����",$id);
}

# ��С���
sub logMeteoSea {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}������ޤ�����",$id);
}

# ��С���
sub logMeteoMountain {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# ��С��������
sub logMeteoSbase {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>���������ޤ�����",$id);
}

# ��С�����
sub logMeteoMonster {
	my($id, $name, $lName, $point) = @_;
	logOut("<B>$lName</B>������${HtagName_}${name}$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}�����Φ�Ϥ�<B>$lName</B>���Ȥ���פ��ޤ�����",$id);
}

# ��С����á��������
sub logMeteoMonsterSea {
	my($id, $name, $lName, $point) = @_;
	logOut("<B>$lName</B>������${HtagName_}${name}$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}���������ˤ���<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# ��С�����
sub logMeteoSea1 {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}��������줬�������ޤ�����",$id);
}

# ��С�����¾
sub logMeteoNormal {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}������<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}��������Ӥ����פ��ޤ�����",$id);
}

# ��С�����¾
sub logHugeMeteo {
	my($id, $name, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}������${HtagDisaster_}�������${H_tagDisaster}�������",$id);
}

# ʮ��
sub logEruption {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}������${HtagDisaster_}�л���ʮ��${H_tagDisaster}��<B>��</B>������ޤ�����",$id);
}

# ʮ�С�����(������)
sub logEruptionSea3 {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}������<B>$lName</B>������<B>��</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ���������ˤʤ�ޤ�����",$id);
}

# ʮ�С�����(����)
sub logEruptionSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ��������˽и����ޤ�����",$id);
}

# ʮ�С�����
sub logEruptionSea1 {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ���Φ�Ϥˤʤ�ޤ�����",$id);
}

# ʮ�С���or����
sub logEruptionSea {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ���������ˤʤ�ޤ�����",$id);
}

# ʮ�С�����¾
sub logEruptionNormal {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ���${HtagDisaster_}����${H_tagDisaster}���ޤ�����",$id);
}

# ��������ȯ��
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",$id);
}

# ���������ﳲ
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageSea {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>��<B>����</B>���ޤ�����",$id);
}

# �����ﳲ�����η���
sub logWideDamageSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>���׷���ʤ��ʤ�ޤ�����",$id);
}

# �����ﳲ�����ÿ���
sub logWideDamageMonsterSea {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��Φ�Ϥ�<B>$lName</B>���Ȥ���פ��ޤ�����",$id);
}

# �����ﳲ�����ÿ��ס��������
sub logWideDamageMonsterSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}�ο���ˤ���<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageMonster {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageWaste {
	my($id, $name, $lName, $point) = @_;
	logOut("�������� ${HtagName_}$point${H_tagName}��<B>$lName</B>�ϰ�֤ˤ���<B>����</B>�Ȳ����ޤ�����",$id);
}

# ����
sub logPrize {
	my($id, $name, $pName, $money) = @_;
	my $str = ($money) ? "(�޶⡧${money}${HunitMoney})" : "";
	logOut("${HtagName_}${name}${H_tagName}��<B>$pName$str</B>����ޤ��ޤ�����",$id);
	logHistory("${HtagName_}${name}${H_tagName}��<B>$pName$str</B>�����");
}

# �رľ���
sub logCampDelete {
	my($name) = @_;
	logHistory("${HtagName_}${name}${H_tagName}�ϡ���˴���ޤ�����");
}

# �رľ���(���ǲ���)
sub logCampPreDelete {
	my($name) = @_;
	logHistory("${HtagName_}${name}${H_tagName}�ϡ����������ۤ��ޤ�����");
}

# �׹�
sub logshunkou {
	my($id, $name, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${kind}</B>�ι�������λ��${HtagName_}${point}${H_tagName}�ǽ׹����ޤ�����",$id);
}

# ������ޤȤ�
sub logkitouMatome {
	my($id, $name, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}��${HtagComName_}${kind}${H_tagComName}�����ꤷ�ޤ�����<br>����<B>��</B> $point",$id);
}

# �񸻺η�(����η�����)
sub logResourceS {
	my($id, $nId, $name, $kind, $kind2, $point, $point2, $arg) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${kind}(${name})</B>��${HtagName_}${point2}${H_tagName}������<B>${kind2}</B>�ǻ񸻤�ν���${HtagMoney_}${arg}$HunitMoney${H_tagMoney}�����μ��פ�����ޤ�����",$id, $nId);
}

# �񸻺η�(������)
sub logResourceF {
	my($id, $nId, $name, $kind, $kind2, $point, $point2, $arg) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}��<B>${kind}(${name})</B>��${HtagName_}${point2}${H_tagName}������<B>${kind2}</B>�ǻ񸻤�ν���${HtagFood_}${arg}$HunitFood${H_tagFood}�����μ��פ�����ޤ�����",$id, $nId);
}

# �Ҷ���ȯ��
sub logNavyBuild2 {
	my($id, $name, $nNo, $nName, $point, $tId) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>${nNo}�����${nName}</B>��ȯ�ʡ�${HtagName_}$point${H_tagName}������������ޤ�����",$id, $tId);
}

# ����ʧ����
sub logSellPort {
	my($id, $tName, $point, $fleet, $tId) = @_;
	logOut("${HtagName_}${tName}${point}${H_tagName}��<B>${fleet}</B>�ϡ�̱�֤�ʧ���������ޤ�����",$id, $tId);
}

# �������
sub logBuyPort {
	my($id, $name, $point, $fleet, $tId, $tName) = @_;
	logOut("${HtagName_}${tName}${point}${H_tagName}��<B>${fleet}</B>��${HtagName_}${name}${H_tagName}����������ޤ�����",$id, $tId);
}

# �ǰ�
sub logTrade {
	my($id, $tId, $name, $nName, $value, $value2, $tmp, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}��<B>��ڵ����������˥å�(${nName})</B>���ǰפ򳫻ϡ�����${HtagFood_}$value$HunitFood${H_tagFood}��${HtagMoney_}$value2$HunitMoney${H_tagMoney}��$tmp���ޤ�����",$id, $tId);
}

# �ǥХå�
sub logdebug {
        my($id, $tmp) = @_;
	logOut("$tmp", $id);
}

# �͸�����¾���ͤ򻻽�
sub estimate {
	my($number) = $_[0];
	my($island, $fkind);

	# �Ϸ������
	$island = $Hislands[$number];
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island2->{'landValue'};
	my($map) = $island->{'map'};

	# �����
	$island->{'pop'}       = 0;
	$island->{'area'}      = 0;
	$island->{'farm'}      = 0;
	$island->{'factory'}   = 0;
	$island->{'mountain'}  = 0;
	$island->{'navyPort'}  = 0;
	$island->{'oil'}       = 0;
	$island->{'sea'}       = 0;
	$island->{'mine'}      = 0;
	$island->{'stone'}     = 0;
	$island->{'fish'}      = 0;

	foreach (0..$#HcomplexName) {
		$island->{'complex'}[$_] = 0;
	}

	# ������
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$value2 = $landValue2->[$x][$y];

			if(($kind != $HlandSea) &&
				($kind != $HlandBouha) &&
				($kind != $HlandSeaMine) &&
				($kind != $HlandSbase) &&
				($kind != $HlandOil)){
				$island->{'area'}++;
				if($kind == $HlandTown) {
					# Į
					$island->{'pop'} += $value;
				} elsif($kind == $HlandFarm) {
					# ����
					$island->{'farm'} += $value;
				} elsif($kind == $HlandFactory) {
					# ����
					$island->{'factory'} += $value;
				} elsif($kind == $HlandMountain) {
					# ��
					$island->{'mountain'} += $value;
				} elsif($kind == $HlandComplex) {
					# ʣ���Ϸ�
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($value);
					$island->{$HcomplexTPkind[$cKind]} += $cTurn * $HcomplexTPrate[$cKind] if(defined $HcomplexTPkind[$cKind]);
					$island->{$HcomplexFPkind[$cKind]} += $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
					$island->{$HcomplexMPkind[$cKind]} += $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
					$island->{'complex'}[$cKind]++;
					$island->{'area'}-- if($HcomplexAttr[$cKind] & 0x300);
				} elsif(($kind == $HlandMonster) || ($kind == $HlandHugeMonster)) {
					# ���ˤ�����ä�Φ�Ϥ˥�����Ȥ��ʤ�
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($value);
					$island->{'area'}-- if ($mFlag & 2);
				} elsif ($kind == $HlandNavy) {
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
					my $nSpecial = $HnavySpecial[$nKind];
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'shipk'}[$nKind]++ if(defined $n);
					if ($nSpecial & 0x8) {
						# ��
						$island->{'navyPort'}++;
					} else {
						if(!($nFlag == 1)) {
							if(defined $n) {
								$Hislands[$n]->{'ships'}[$nNo]++;
								$Hislands[$n]->{'ships'}[4]++;
								$Hislands[$n]->{"invade$id"}++;
							}
						}
					        if ($HnavyNoMove[$nKind] == 0){
						    # �����ʤ�Φ�Ϥ˥�����Ȥ��ʤ�
						    $island->{'area'}--;
                                                }
					}
				} elsif($kind == $HlandDefence) {
					$island->{'dbase'}++;
				} elsif($kind == $HlandCore) {
					$island->{'core'}++;
					$island->{'area'}-- if(int($value / 10000) >= 1);
			        } elsif($kind == $HlandResource) {
                                    # �񸻷�
                                    my($temp, $kind, $turn, $food, $money) = landUnpack($value);
                                    if($kind == 0){
				        $island->{'stone'}++;
                                    }else{
                                        $island->{'fish'}++;
                                    }
				    $island->{'area'}--;
				}
			} elsif($kind == $HlandBouha) {
				$island->{'bouha'}++; # ������򥫥����
			} elsif($kind == $HlandSeaMine) {
				$island->{'mine'}++; # ����򥫥����
			} elsif($kind == $HlandOil) {
				$island->{'oil'}++; # ���Ĥ򥫥����(ȯ����Ψ�򲼤���)
			} elsif($kind == $HlandSea && !$value) {
				$island->{'sea'}++; # �������򥫥����
			}
		}
	}

}

# �ݥ���Ȼ���
sub calcPoint {
	my($number) = @_;

	$island = $Hislands[$number];
	my $point = 0;
	my $value;
	foreach (keys %HpointRatio) {
		$value = ($island->{$_} * $HpointRatio{$_});
		$point += $value;
	}
	foreach (0..$#HpointRatioNavy) {
		$value = ($island->{'navy'}[$_] * $HpointRatioNavy[$_]);
		$point += $value;
	}
	$point /= $HpointRatioDenominator if($HpointRatioDenominator);

	$island->{'point'} = int($point);
}

# �ϰ�����Ϸ��������
sub countAround {
	my($island, $x, $y, $range, @kind) = @_;
	my($land) = $island->{'land'};
	my($sea, $count, $sx, $sy, @list);
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

# �ϰ����ʣ���Ϸ�(°��)�������
sub countAroundComplex {
	my($island, $x, $y, $range, $attr) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ�
		next if(($sx < 0) || ($sy < 0));

		# �ϰ���ξ��
		if($land->[$sx][$sy] == $HlandComplex) {
			my $cKind = (landUnpack($landValue->[$sx][$sy]))[1];
			if($HcomplexAttr[$cKind] & $attr) {
				$count++;
			}
		}
	}
	return $count;
}

# �ϰ�����ɱһ��ߡ�������ߤĤ���
sub countAroundDef {
	my($id, $island, $x, $y, $special, @oId, $cflag) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($range, $sx, $sy, %idFlag);
	# @oId�����äƤ���ID(����¦ID)��̵��
	foreach (@oId) {
		$idFlag{$_} = 1;
	}

	my($count) = 0;
	$range = ($HdefLevelUp) ? $an[3] : $an[2];
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		if($_ < $an[2]) { # ���إå����ɱ�
			if($land->[$sx][$sy] == $HlandNavy) {
				my($dId, $dExp, $dKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[0, 4, 7];
				my $nSpecial = $HnavySpecial[$dKind];
                                my $defLimit = 3 + int($dExp /40);
				next if($idFlag{$dId} || !($nSpecial & $special));
				if(!$cflag) {
                                        if($DefCount->[$id][$sx][$sy] < $defLimit){
                                            $DefCount->[$id][$sx][$sy]++;
					    return 1;
                                        }
				} else {
					$count++;
				}
			} elsif(!$idFlag{$id}) {
				if($land->[$sx][$sy] == $HlandComplex) {
					my $cKind = (landUnpack($landValue->[$sx][$sy]))[1];
					next if(!($HcomplexAttr[$cKind] & $special));
					if(!$cflag) {
                                            if($DefCount->[$id][$sx][$sy] < 3){
                                                $DefCount->[$id][$sx][$sy]++;
					        return 1;
                                            }
					} else {
						$count++;
					}
				} elsif($land->[$sx][$sy] == $HlandDefence) {
					if(!$cflag) {
                                            if($DefCount->[$id][$sx][$sy] < 3){
                                                $DefCount->[$id][$sx][$sy]++;
					        return 1;
                                            }
					} else {
						$count++;
					}
				}
			}
		} elsif((!$idFlag{$id}) && ($land->[$sx][$sy] == $HlandDefence)) { # ���إå����ɱҤ��ɱһ���
			next if($landValue->[$sx][$sy] < $HdefLevelUp - 1);
			if(!$cflag) {
                            if($DefCount->[$id][$sx][$sy] < 3){
                                $DefCount->[$id][$sx][$sy]++;
			        return 1;
                            }
			} else {
				$count++;
			}
		}
	}
	return $count;
}

# �ϰ���γ���ˤ�����ä������
sub countAroundMonster {
	my($island, $x, $y, $range) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		if(($land->[$sx][$sy] == $HlandMonster) || ($land->[$sx][$sy] == $HlandHugeMonster)) {
			my $nFlag = (monsterUnpack($landValue->[$sx][$sy]))[4];
			$count++ if($nFlag & 2);
		}
	}
	return $count;
}

# �ϰ���δ����������
sub countAroundNavy {
	my($island, $x, $y, $range) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[7];
			my $nSpecial = $HnavySpecial[$nKind];
			$count++ unless ($nSpecial & 0x8);
		}
	}
	return $count;
}

# �ϰ�����ü�����������
sub countAroundNavySpecial {
	my($island, $x, $y, $special, $range, @id) = @_;
	# @id�Τߥ������($id��'0'��������Ϥ��٤Ƥ򥫥����)
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy, %idFlag);
	foreach (@id) {
		$idFlag{$_} = 1;
	}
	$count = 0;

	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nFlag, $nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[0, 5, 7];
			my $nSpecial = $HnavySpecial[$nKind];


			$count++ if(($nSpecial & $special) && ($idFlag{'0'} || $idFlag{$nId}) && ($nFlag != 3));
		}
	}
	return ($count);
}

# �ϰ��������ǽ�ϴ����������
sub countAroundNavyBouha {
	my($island, $x, $y) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;

	my $range = $an[3];
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# �ϰϳ��ξ��
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[0, 7];
			my $special = $HnavySpecial[$nKind];
			return 1 if(($special & 0x8000000) && ($_ < $an[$HbouhaHex[$nKind]]));
		}
	}
	return 0;
}


# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# �����
	$n = 1 if($n <= 0);
	@list = (0..$n-1);

	# ����åե�
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		next if($i == $j);
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

#------------------------------------------------
# �ȡ��ʥ��ȥ⡼��
#------------------------------------------------
# ����ε�Ͽ��
sub fightlog {
	# ��¸�ǥ��ꥯ�ȥ�Υ����å�
	if(!opendir(DIN, "${HfightdirName}/")) {
		mkdir("${HfightdirName}", $HdirMode);
	} else {
		closedir(DIN);
	}

	# ����������� �辡��ξ��99�ˤ���
	my $fTurn = ($HislandFightMode == 9) ? 99 : (!$HislandFightMode) ? 0 : $HislandFightCount;

	my($f,@offset);
	if($fTurn) {
		if(!open(FIN, "<${HfightdirName}/${Hfightlog}")) {
			rename("${HfightdirName}/fight.tmp", "${HfightdirName}/${Hfightlog}");
			if(!open(FIN, "<${HfightdirName}/${Hfightlog}")) {
				return;
			}
		}
		while($f = <FIN>){
			chomp($f);
			push(@offset,"$f\n");
		}
		close(FIN);
	}
	open(FOUT, ">${HfightdirName}/fight.tmp");
	print FOUT "<${fTurn}>\n";

	foreach (@HfightLogPool) {
		print FOUT $_ . "\n";
	}
	print FOUT @offset if($fTurn);
	close(FOUT);

	unlink("${HfightdirName}/${Hfightlog}") if(-e "${HfightdirName}/${Hfightlog}");
	rename("${HfightdirName}/fight.tmp","${HfightdirName}/${Hfightlog}");
}

# ������
sub logWin {
	my($id, $name, $str, $money, $ino) = @_;
	my $fTurn = $HislandFightCount + 1;
	if($ino <= 2) {
		$fTurn = '�辡��';
	} elsif($ino <= 4) { 
		$fTurn = '��辡';
	} else {
		$fTurn .= '����';
	}
	if($ino < 2) {
		logOut("${HtagName_}${name}${H_tagName}${str}����<B>ͥ������</B>",$id);
		logHistory("${HtagName_}${name}${H_tagName}��<B>ͥ������</B>");
	} elsif($money == 0) {
		logOut("${HtagName_}${name}${H_tagName}${str}����<B>$fTurn�ʽС�</B>",$id);
	} else {
		logOut("${HtagName_}${name}${H_tagName}${str}����<B>$fTurn�ʽС���$money$HunitMoney</B>���󽷶⤬��ʧ���ޤ�����",$id);
	}
}

# ����
sub logLose {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>����</B>��",$id);
}

# ͽ�����
sub logLoseOut {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}��<B>ͽ�����</B>��",$id);
	logHistory("${HtagName_}${name}${H_tagName}��<B>ͽ�����</B>��");
}

# ���׻����������ǡ�������
sub fightNoFight {
	my($island, $rno) = @_;
	my $delflag = 0;
	my($tIsland, $tId);
	my $tn = $HidToNumber{$island->{'fight_id'}};
	if($tn ne '') {
		$tIsland = $Hislands[$tn];
		$tId = $tIsland->{'id'};
		$delflag = $tIsland->{'delete'};
		$delflag = 1 if(!$tIsland->{'pop'});
	} else {
		$delflag = 1;
	}

	if(!$delflag) {
		my $rest_turn;
		if($HislandFightMode == 2) {
			my $reward = $tIsland->{'subExt'}[12];
			if(int($HfightTurn / 2) <= ($HislandChangeTurn - $HislandTurn)) {
				$rest_turn = ($HnofightTurn + $HislandFightCount * $HnofightUp) - ($HfightTurn - ($HislandChangeTurn - $HislandTurn));
				island_load($tIsland, -1);
				$tIsland->{'fight_id'} = -1;
			} else {
				$tIsland->{'money'} += $reward;
				$tIsland->{'prizemoney'} += $reward;
				my $fightIslandNumber = 0;
				my $winIslandNumber = 0;
				foreach $i ($HbfieldNumber..$rno){
					$island = $Hislands[$i];
					if($island->{'fight_id'} < 0) {
						$winIslandNumber++;
					} elsif($island->{'fight_id'} > 0) {
						$fightIslandNumber++;
					}
				}
				$winIslandNumber += int(($fightIslandNumber + 1)/2);
				logWin($tIsland->{'id'}, islandName($tIsland), "������", $reward, $winIslandNumber);
				$tIsland->{'fight_id'} = -2;
			}
			# �Ƽ���ͤ�׻�
			estimate($tn);
		} else {
			# �辡�ʤ�ɤ������ξ����ʤΤǡ�����γ�ȯ��߽���
			$rest_turn = $HnofightTurn + $HislandFightCount * $HnofightUp;
			$tIsland->{'fight_id'} = -1;
		}
		$tIsland->{'rest'} += $rest_turn if($rest_turn > 0);
	}
	$island->{'fight_id'} = 0;
	$island->{'delete'} = 1;
	my $flag = 0;
	if($rno <= $HbfieldNumber + 2) {
		$HislandFightMode = 9;
		$tIsland->{'rest'} = 0;
		my(@text);
		my(@iext) = @{$island->{'subExt'}};
		foreach (0..$#iext) {
			$iext[$_] = $island->{'ext'}[$_] - $island->{'subExt'}[$_];
			$iext[$_] = -$iext[$_] if($iext[$_] < 0);
			$text[$_] = $tIsland->{'ext'}[$_] - $tIsland->{'subExt'}[$_];
			$text[$_] = -$text[$_] if($text[$_] < 0);
		}
		push(@HfightLogPool, "$HislandFightCount,$tIsland->{'id'}," . islandName($tIsland) . ",$tIsland->{$HrankKind}," . join('-', @text) . ",-2," . islandName($island) . ",''," . join('-', @iext) . ",") if(!$delflag);
		$flag = 3;
	}
	#push(@delete_log, $tIsland->{'id'});


	return $flag;
}





1;