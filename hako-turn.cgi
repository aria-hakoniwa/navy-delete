# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------

#――――――――――――――――――――――――――――――――――――
#							  箱庭諸島 2nd
#								  v1.5
#
#					  by 親方 webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#――――――――――――――――――――――――――――――――――――

#――――――――――――――――――――――――――――――――――――
#							 箱庭諸島 海戦
#								  v1.3
#
#					  by 親方 webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#――――――――――――――――――――――――――――――――――――

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {

	# 最終更新時間を更新
	$HislandLastTime += $HunitTime if($HrepeatTurn);

	if($HallyNumber && $HrepeatTurn) { # 同盟の情勢を示すデータのクリア
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

		# 順番決め
		my(@order) = randomArray($HislandNumber);

		my($island);
		# 座標配列を作る
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			makeRandomIslandPointArray($island);
		}

		# ターン番号
		$HislandTurn++;
		# 停戦(開発、戦闘)期間最後のターンではリピートを停止
		$repeatTurn = 0 if($HislandTurn == $HarmisticeTurn || $HislandTurn == $HsurvivalTurn ||  $HislandTurn == $HislandChangeTurn);

		if($HarmisticeTurn || $HsurvivalTurn ||$Htournament) {
			# 災害あり？
			if(!$repeatTurn && !$Htournament) {
				# 最後のターンは災害あり
				if ($HislandTurn < $HarmisticeTurn) {
					# 停戦期間は無災害
					$HnoDisFlag = 1;
				} else {
					# 災害あり
					$HnoDisFlag = 0;
				}
			} else {
				# 最後のターン以外は災害なし
				$HnoDisFlag = 1;
			}
		} elsif($HuseDeWar) {
			# 戦争開始ログ
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
							logOut("${name}が${tName}に打診していた停戦は破棄されました。", $HwarIsland[$i+1], $HwarIsland[$i+2]);
						} elsif($f == 2) {
							$HwarIsland[$i+3] = 0;
							logOut("${tName}が${name}に打診していた停戦は破棄されました。", $HwarIsland[$i+2], $HwarIsland[$i+1]);
						}
					}
				}
				push(@newWarIsland, @HwarIsland[$i..$i+3]);
				next if($HwarIsland[$i] != $HislandTurn);
				if($HmatchPlay > 1) {
					foreach ($isl, $tIsl){
						# カウンタリセット
						$_->{'subSink'} = $_->{'sink'};
						$_->{'subSinkself'} = $_->{'sinkself'};
						my @wext = @{$_->{'ext'}};
						shift(@ext);
						unshift(@ext, $HislandTurn);
						push(@ext, $_->{'monsterkill'});
						push(@ext, 0);
						$_->{'subExt'} = \@ext;
						# 島の状態を保存
						island_save($_, $HsavedirName, 'save', 0);
					}
				}
				my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
				logOut("${wname}戦争勃発！！", $HwarIsland[$i+1], $HwarIsland[$i+2]);
				logHistory("${wname}戦争勃発！！");
			}
			@HwarIsland = @newWarIsland;
		}
		if($HsurvivalTurn && ($HislandTurn == $HsurvivalTurn) && (-e "${HefileDir}/setup.html")){
			unlink("${HefileDir}/setup.html");
		}

		# 収入、消費フェイズ
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];

			# コメント欄変更チェック
			if($HjoinCommentPenalty && !$island->{'predelete'}) {
				if(($HislandTurn - $island->{'birthday'} >= $HjoinCommentPenalty) && ($island->{'comment'} eq $HjoinComment)){
					push(@HpreDeleteID, $island->{'id'});
					$island->{'predelete'} = (!$HautoKeeperSetTurn) ? 99999999 : ($HautoKeeperSetTurn + 1);
					my $name = islandName($island);
					logHistory("${HtagName_}${name}${H_tagName}、コメントがないため<B>管理人あずかり</B>。");
				}
			}
			# 変数の初期化
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
			# ターン開始前の人口、資金、食料をメモる
			$island->{'oldPop'} = $island->{'pop'};
			$island->{'oldMoney'} = $island->{'money'};
			$island->{'oldFood'} = $island->{'food'};
			# 被友好国のフラグ設定
			my $amityNum = 0;
			foreach (@{$island->{'amity'}}) {
				my $amn = $HidToNumber{$_};
				if(defined $amn) {
					# 友好国に設定してくれている島IDを'amityBy'に格納
					push(@{$Hislands[$amn]->{'amityBy'}}, $island->{'id'});
					$amityNum++;
				}
			}
			next if($island->{'predelete'} || $island->{'rest'});

			# 友好国維持費
			$island->{'upkeepAmity'} = ($HarmisticeTurn) ?  0 : $amityNum * $HamityMoney;
			$island->{'money'} -= $island->{'upkeepAmity'};
			$island->{'money'} = 0 if($island->{'money'} < 0);

#-------------------------いろいろと準備-------------------------
                        $island->{'setreadyx'} = 31;
                        $island->{'setreadyy'} = 31;

			# コマンドチェック(艦隊移動，派遣，帰還処理をするか)
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

			# 気象フェイズ
			if($HuseWeather) {
				my(@tempWeather) = ();
				foreach (1..$#HweatherName) {
					@tempWeather = (@tempWeather, ($_)x$HweatherRatio[$_] );
				}
				my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$island->{'weather'}};
				# 気温
				my $dkion = ($HweatherSpecial[$weather[0]] & 0xF) - 8;
				$dkion = ($dkion == -8) ? 0 : $dkion * $HweatherSpecialRatio[0] + random($HrKion * 2 + 1) - $HrKion;
				$kion += $dkion;
				$kion = ($kion > 41) ? 25 : ($kion < -12) ? 0 : $kion;
				$kion = ($kion > 40) ? 40 : ($kion < -10) ? -10 : $kion;
				# 気圧
				my $dkiatu = (($HweatherSpecial[$weather[0]] & 0xF0)>>(4*1)) - 8;
				$dkiatu = ($dkiatu == -8) ? 0 : $dkiatu * $HweatherSpecialRatio[1] + random($HrKiatu * 2 + 1) - $HrKiatu;
				$kiatu += $dkiatu;
				$kiatu = ($kiatu > 1105) ? 1000 : ($kiatu < 895) ? 1000 : $kiatu;
				$kiatu = ($kiatu > 1100) ? 1100 : ($kiatu < 900) ? 900 : $kiatu;
				# 湿度
				my $dsitudo = (($HweatherSpecial[$weather[0]] & 0xF00)>>(4*2)) - 8;
				$dsitudo = ($dsitudo == -8) ? 0 : $dsitudo * $HweatherSpecialRatio[2] + random($HrSitudo * 2 + 1) - $HrSitudo;
				$situdo += $dsitudo;
				$situdo = ($situdo > 103) ? 90 : ($situdo < -1) ? 60 : $situdo;
				$situdo = ($situdo > 100) ? 100 : ($situdo < 0) ? 0 : $situdo;
				# 風速
				$kaze += (abs($dkiatu) > $HrKiatu / 2) ? abs($dkiatu / 30) : -abs($dkiatu / 5);
				$kaze = ($kaze > 50) ? 50 : ($kaze < 0) ? 0 : int($kaze);
				# 地盤指数
				$jiban += int(($situdo - 50) / 4) if($situdo > 60);
				$jiban -= int($kion / 2) if($kion > 20);
				$jiban = ($jiban > 100) ? 100 : ($jiban < 0) ? 0 : $jiban;
				# 波力指数
				$nami += ($kaze < 5) ? -int($kaze / 3) : int($kaze / 3);
				$nami = ($nami > 100) ? 100 : ($nami < 0) ? 0 : $nami;
				# 異常指数(使用せず)
				$ijoh = 0;
				# 天候決定
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

			# 収入処理
			income($island);
			# 海軍の補給処理
			supplyNavy($island);
		}

		# 先行処理
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doPreEachHex($island);
		}

		# コマンド処理
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if(!($HforgivenGiveUp && $island->{'command'}[0]->{'kind'} == $HcomGiveup) && ($island->{'predelete'} || $island->{'rest'}));
			# 戻り値1になるまで繰り返し
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
			# 整地ログ(まとめてログ出力)
			logMatome($island);
		}

		# 成長および単ヘックス災害
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doEachHex($island);
		}

                # 単ヘックス処理 2回目
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doEachHex2($island);
		}

		my($remainCampNumber, $campDelete);
		if($HarmisticeTurn && $HallyNumber) {
			# 陣営消滅判定
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

		# 参加島への制裁内容を読み込む
		readPunishData();

		# 島全体処理
		# 怪獣出現人口フラグ処理
		foreach (@HdisMonsBorder) {
			$HdisMonsBorderMax = $_ if($HdisMonsBorderMax <= $_);
		}
		$HdisMonsBorderMin = $HdisMonsBorderMax;
		foreach (@HdisMonsBorder) {
			next if(!$_);
			$HdisMonsBorderMin = $_ if($HdisMonsBorderMin >= $_);
		}
		# 巨大怪獣出現人口フラグ処理
		foreach (@HdisHugeBorder) {
			$HdisHugeBorderMax = $_ if($HdisHugeBorderMax <= $_);
		}
		$HdisHugeBorderMin = $HdisHugeBorderMax;
		foreach (@HdisHugeBorder) {
			next if(!$_);
			$HdisHugeBorderMin = $_ if($HdisHugeBorderMin >= $_);
		}
		# 艦艇出現人口フラグ処理
		foreach (@HdisNavyBorder) {
			$HdisNavyBorderMax = $_ if($HdisNavyBorderMax <= $_);
		}
		$HdisNavyBorderMin = $HdisNavyBorderMax;
		foreach (@HdisNavyBorder) {
			next if(!$_);
			$HdisNavyBorderMin = $_ if($HdisNavyBorderMin >= $_);
		}
		# 島全体処理
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doIslandProcess($island);
			undef $island->{'ships'};
			undef $island->{'shipk'};
		}

		# 島全体(estimate)処理
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			next if($island->{'predelete'} || $island->{'rest'});
			doIslandProcessEstimate($order[$i], $island);
			# トーナメント 規程数戦闘行為があったか
			my $name = islandName($island);
			if(0 && $Htournament && ($HislandFightMode == 2) && ($island->{'fight_id'} > 0)) { # トーナメント 規定戦闘回数チェック
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
			# コア保有確認
			if($HcorelessDead && !$island->{'field'} && !$island->{'event'}[0] && !$island->{'core'} &&
				!($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) &&
				!($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn)) &&
				!($Htournament && ($HislandFightMode < 2)) &&
				!($HislandTurn - $island->{'birthday'} <= $HdevelopTurn)
				) {
				logHistory("${HtagName_}${name}${H_tagName}の$HlandName[$HlandCore][0]が${HtagDisaster_}壊滅${H_tagDisaster}しました！");
				if($HcorelessDead == 1) {
					$island->{'dead'} = 1;
					logTDead($island->{'id'}, $name);
				} else {
					$island->{'delete'} = 1;
				}
			}
		}

		# 死滅判定・イベント判定
		my $predelNumber = @HpreDeleteID; # 管理人あずかりの島は死滅処理から逃れる
		my $remainNumber = $HislandNumber - $predelNumber;
		my $deadline = ($HarmisticeTurn || $HsurvivalTurn || $Htournament) ? 0 : $HautoKeeper;
		my $tournamentflg = 0;
		foreach $i (0..$islandNumber) {
			$island = $Hislands[$order[$i]];
			if($island->{'event'}[0]) {
				# イベント判定
				my $winner;
				if($island->{'event'}[1] - $HnoticeTurn == $HislandTurn) {
					# イベント開始前(猶予期間)
					my $type  = $HeventName[$island->{'event'}[6]];
					my $name = islandName($island);
					islandDeadNavy($island);# 艦艇処理
					$island->{'comment'} = "<B>$type開催！</B>";
					if(!$island->{'event'}[11]) {
						$island->{'comment'} .= "(<span class=attention>注！</span>派遣できるのは<B>ターン$island->{'event'}[1]だけ</B>です)";
					} else {
						$island->{'comment'} .= "(<span class=attention>注！</span><B>ターン$island->{'event'}[1]から</B>随時派遣可能です)";
					}
					logHistory("${HtagName_}${name}${H_tagName}で${HtagDisaster_}$type${H_tagDisaster}開催！(${HtagDisaster_}$island->{'event'}[1]ターン${H_tagDisaster}開始)");
				} elsif($island->{'event'}[1] <= $HislandTurn) {
					# イベント開催中
					$winner = islandEventNavy($island, $island->{'event'}[6]);
				}
				if($winner != 0) {
					my $type  = $HeventName[$island->{'event'}[6]];
					my $name = islandName($island);
					$island->{'comment'} = "<B>$typeは終了しました！</B>($HislandTurnターン)";
					if($winner > 0) {
						$island->{'comment'} .= "　勝者：<span class=islName>$Hislands[$HidToNumber{$winner}]->{'name'}$AfterName</span>";
						$winner = islandName($Hislands[$HidToNumber{$winner}]);
						logHistory("${HtagName_}${name}${H_tagName}で開催した${HtagDisaster_}$type${H_tagDisaster}で${HtagName_}${winner}${H_tagName}が<B>勝利</B>しました！");
					} else {
						logHistory("${HtagName_}${name}${H_tagName}で開催した${HtagDisaster_}$type${H_tagDisaster}は<B>勝者なしで終了</B>しました！");
						$island->{'comment'} .= "　勝者：<span class=islName>なし</span>";
					}
					undef $island->{'event'}; # フラグクリア
				}
			} elsif($island->{'dead'} == 1) {
				# 死滅判定(フラグあり)
				island_save($island, $HfightdirName, 'lose', 0) if($HdeadToSaveAsLose);
				$island->{$HrankKind} = 0;
				$island->{'pop'} = 0;
				my($tmpid) = $island->{'id'};
				islandDeadNavy($island); # 艦艇処理
				# トーナメントで戦闘期間中
				$tournamentflg = fightNoFight($island, $remainNumber) if($Htournament && ($island->{'fight_id'} > 0));
				preDelIdCut($tmpid);
				$HidToNumber{$tmpid} = undef;
				deleteIslandData($island);
				$remainNumber--;
			} elsif( (!$island->{'field'} && !$island->{'predelete'} && ($island->{'pop'} <= $deadline)
						&& (!$island->{'pop'} || ($HislandTurn - $island->{'birthday'} > $HdevelopTurn)))
				|| $island->{'delete'}
				) {
				# 死滅判定
				my($tmpid) = $island->{'id'};
				islandDeadNavy($island);
				# トーナメントで戦闘期間中
				$tournamentflg = fightNoFight($island, $remainNumber) if($Htournament && ($island->{'fight_id'} > 0));
				# コア破壊
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
						# 初期人口で町を作る
						my($land) = $island->{'land'};
						my($landValue) = $island->{'landValue'};
						foreach (0..$island->{'pnum'}) {
							last if($count >= $HcountLandTown);
							$x = $island->{'rpx'}[$i];
							$y = $island->{'rpy'}[$i];
							# そこが平地か荒地なら、町
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
					# 死滅メッセージ
					logDead($tmpid, islandName($island));
					$HidToNumber{$tmpid} = undef;
					deleteIslandData($island);
				}
			} else {
				$island->{'ext'}[1] += int($island->{$HrankKind}/10);
			}
			undef $island->{'fkind'};
		}
			# 陣営消滅判定
		if($campDelete->{'count'}) {
			foreach (0..($campDelete->{'count'} - 1)) {
				islandDeadAlly('', $campDelete->{'id'}[$_], $campDelete->{'name'}[$_]);
			}
		}
		# 島の消滅処理(サバイバルモード)
		if($HsurvivalTurn && ($HislandTurn > $HsurvivalTurn) && ($remainNumber > $HbfieldNumber + 1)){
			# $HrankKind÷(全島の$HrankKindの合計÷100)が(100÷島数)÷2より少ない時、その島は消滅

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
						# 死滅メッセージ
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
			# トーナメント
			foreach $i ($HbfieldNumber..$islandNumber) {
				# 報酬金計算
				$island = $Hislands[$i];
				next if($island->{'predelete'});
				foreach (keys %Hreward) {
					$island->{'subExt'}[12] += int($island->{$_} * $Hreward{$_});
				}
			}

			if($HislandFightMode == 0) {
				# 予選
				if($HislandTurn == $HislandChangeTurn) {
					# 開発ターンに移行
					$tournamentflg = 1;
					$HislandFightMode = 1;
					$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
				}
			} elsif($HislandFightMode == 1) {
				# 開発
				if($HislandTurn == $HislandChangeTurn) {
					# 戦闘ターンに移行
					$tournamentflg = 2;# 対戦相手決定処理は人口ソート後で
					$HislandFightMode = 2;
					$HislandFightCount++;
					if($remainNumber > 2) {
						# 決勝戦以外は、時間を空ける
						$HislandChangeTurn = $HislandTurn + $HfightTurn;
					} else {
						# 決勝戦
						$HislandChangeTurn = $HislandTurn + $HfinalTurn;
					}
					my $rno = $remainNumber - 1;
					foreach $i ($HbfieldNumber..$rno){
						$island = $Hislands[$i];
						# カウンタリセット
						$island->{'subSink'} = $island->{'sink'};
						$island->{'subSinkself'} = $island->{'sinkself'};
						my @ext = @{$island->{'ext'}};
						shift(@ext);
						unshift(@ext, $HislandTurn);
						push(@ext, $island->{'monsterkill'});
						push(@ext, 0);
						#undef $island->{'subExt'};
						$island->{'subExt'} = \@ext;
						# 島の状態を保存
						island_save($island, $HsavedirName, 'save');
					}
				}
			} elsif($HislandFightMode == 2) {
				# 戦闘
				if($HislandTurn == $HislandChangeTurn){
					# 勝敗決着　開発ターンに移行
					$tournamentflg = 3;
					if(($remainNumber < $HbfieldNumber + 2) ||
						( ($remainNumber <= $HbfieldNumber + 2) &&
						($Hislands[$HbfieldNumber]->{'fight_id'} > -1) &&
						($Hislands[$HbfieldNumber+1]->{'fight_id'} > -1) )
					) {
						# 終了
						$HislandFightMode = 9;
						$repeatTurn = 0;
						$HplayNow = 0;
						$Hislands[$HbfieldNumber]->{'ext'}[0] |= (2 ** $#HwinnerMark);
					} else {
						$HislandFightMode = 1;
					}
					$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
					my $HwinIsland = 0;       # 勝利した島の数
					my $consolationScore = 0; # 敗者復活対象島人口
					my $consolationID = 0;    # 敗者復活対象島ＩＤ
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
						# 戦闘後の勝敗
						my $reward = $island->{'subExt'}[12];
						if(($tn ne '' && $island->{$HrankKind} >= $tIsland->{$HrankKind}) || ($island->{'fight_id'} == -1) || ($island->{'fight_id'} == -2)) {
							# 勝ち
							my $name = islandName($island);
							my $tName = islandName($tIsland);
							my $tScore = 0;
							$HwinIsland++;
							if($island->{'fight_id'} > 0){
								$island->{'money'} += $reward;
								$island->{'prizemoney'} += $reward;
								logWin($island->{'id'}, $name, "勝利", $reward, $winIslandNumber);
								$tScore = $tIsland->{$HrankKind};
								$tIsland->{'fight_id'} = 0;
								if($consolationScore <= $tScore){
									$consolationScore = $tScore;
									$consolationID = $tIsland->{'id'};
								}
								$tIsland->{'lose'} = 1;
								logOut("${HtagName_}${tName}${H_tagName}、<B>敗退</B>。",$tIsland->{'id'});
							} elsif($island->{'fight_id'} == -2) {
								# コールド勝ち
								#$island->{'money'} += $reward;
								#$island->{'prizemoney'} += $reward;
								logWin($island->{'id'}, $name, "圧勝！", '', $winIslandNumber);
							} else {
								# 不戦勝
								logWin($island->{'id'}, $name, "不戦勝", '', $winIslandNumber);
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
							logWin($island->{'id'}, $name, "圧勝！", $reward, $winIslandNumber);
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
					# 敗退した島の除去
					foreach $i (0..$islandNumber){
						$island = $Hislands[$i];
						islandDeadNavy($island);
						my $name = islandName($island);
						if($island->{'lose'}){
							if(($consolationID == $island->{'id'}) && (($HwinIsland % 2) != 0) && ($HconsolationMatch)){
								# 敗者復活対象島で次回奇数の場合で敗者復活モード
								my(@iext) = @{$island->{'subExt'}};
								foreach (0..$#iext) {
									$iext[$_] = $island->{'ext'}[$_] - $island->{'subExt'}[$_];
									$iext[$_] = -$iext[$_] if($iext[$_] < 0);
								}
								my $reward = int($island->{'subExt'}[12] / 2);
								$island->{'money'} += $reward;
								$island->{'prizemoney'} += $reward;
								push(@HfightLogPool, "$HislandFightCount,$island->{'id'},$name,$island->{$HrankKind}," . join('-', @iext) . ",-9,,,,");
								logOut("${HtagName_}${name}${H_tagName}、<B>敗者復活！</B>　$reward$HunitMoney</B>の支援金が支払われました。",$island->{'id'});
							} else {
								island_save($island, $HfightdirName, 'lose', 0);
								if(!$island->{'predelete'}) {
									logHistory("${HtagName_}${name}${H_tagName}、<B>敗退</B>。");
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

		# 順位を更新
		if($HrankKind eq 'point') {
			# ポイント処理
			foreach $i (0..$islandNumber) {
				calcPoint($i);
			}
		}
		islandSort($HrankKind, 1);
		# ターン杯対象ターンだったら、その処理
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
 			if($HitemGivePerTurn && $HuseItem) { #クリスタル争奪戦用
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
						my @str = ('</span><span>が古代', '</span><span>が不思議', '</span><span>が幻魔', '</span><span>が陽炎');
						my @where = ('森で', '山で', '海で', '大地で');
						$Hislands[$num]->{'itemNumber'}++;
						logItemGetLucky($Hislands[$num]->{'id'}, islandName($Hislands[$num]), $str[random(4)], $HitemName[$_], $where[random(4)]);
					}
					$i++;
				}
			}
		}

		if($Htournament){
			# トーナメント
			if($tournamentflg == 1){
				# 予選落ちを沈没させる
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
				# 対戦相手決定処理
				my($l,$r);
				$r = $remainNumber - 1;
				for($l = $HbfieldNumber; $l <= $r; $l++, $r--){
					if($Hislands[$r]->{'id'} == $Hislands[$l]->{'id'}){
						# 不戦勝
						$Hislands[$r]->{'fight_id'} = -1;
						$Hislands[$r]->{'rest'} += $HnofightTurn + $HislandFightCount * $HnofightUp;
					} else {
						$Hislands[$l]->{'fight_id'} = $Hislands[$r]->{'id'};
						$Hislands[$r]->{'fight_id'} = $Hislands[$l]->{'id'};
					}
				}
			}
		}

		# 最下位落としのターンだったらその処理(サバイバルモード)
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

		# 島数カット
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

		if($HallyNumber) { # 同盟関連処理
			# 陣営カット(消滅ルール)
			$HallyNumber = $remainCampNumber if($HarmisticeTurn && ($HautoKeeper != 1));
			for($i = 0; $i < $HallyNumber; $i++) {
				$Hally[$i]->{'score'} = 0;
				# 維持費(いなくなった島があってもいた時の頭割りで処理)
				my($keepCost);
				$keepCost = int($HcostKeepAlly / $Hally[$i]->{'number'}) if($Hally[$i]->{'number'});
				$Hally[$i]->{'number'} = 0;
				my $allyMember = $Hally[$i]->{'memberId'};
				foreach (@$allyMember) {
					my $no = $HidToNumber{$_};
					if(defined $no) {
						$Hally[$i]->{'score'} += $Hislands[$no]->{$HrankKind} if(!$Hislands[$no]->{'predelete'});
						$Hally[$i]->{'number'}++;
						# 維持費徴収
						if(!$HarmisticeTurn) {
							$Hislands[$no]->{'upkeepAlly'} += $keepCost;
							$Hislands[$no]->{'money'} -= $keepCost;
							$Hislands[$no]->{'money'} = 0 if($Hislands[$no]->{'money'} < 0);
						}
						# 貢献度(人口なら1万人につき1ポイント)
						$Hislands[$no]->{'ext'}[1] += int($island->{$HrankKind}/10);
					}
				}
				$Hally[$i]->{'Takayan'} = makeRandomString();
			}
			allyOccupy();
			allySort();
		}

		if($HbalanceLog) { # 収支ログ(機密)
			foreach $i ($HbfieldNumber..$islandNumber) {
				$island = $Hislands[$i];
				next if($island->{'predelete'});
				my $id = $island->{'id'};
				if($HcorelessDead && !$island->{'field'} && !$island->{'core'}) {
					my $dturn = $HdevelopTurn - ($HislandTurn - $island->{'birthday'}) + 1;
					my($alertstr);
					if($dturn <= 1) {
						$alertstr = '次のターンに';
					} else {
						$alertstr = $dturn . 'ターン以内に';
					}
					logSecret("　--- <span class='attention'>警告！</span> コアがありません！${HtagDisaster_}$alertstr${H_tagDisaster}建設しなければ${HtagDisaster_}沈没${H_tagDisaster}します。",$id) if($dturn <= 10);
				}
				my($money) = $island->{'money'} - $island->{'oldMoney'};
				if($island->{'money'} && ($money < 0)) {
					my $turn = $island->{'money'} / (- $money);
					my $str;
					if($turn <= 1) {
						$str = "次のターンには";
					} else {
						$turn = int($turn);
						$str = "${turn}ターン後に";
					}
					logSecret("　--- <span class='attention'>警告！</span> $str開発資金がなくなると推測されます。",$id) if($turn <= 50);
				}
				$money = ($money >= 0) ? "${HtagMoney_}$money" : "<span class='attention'>$money";
				my($food) = $island->{'food'} - $island->{'oldFood'};
				if($island->{'food'} && ($food < 0)) {
					my $turn = $island->{'food'} / (- $food);
					my $str;
					if($turn <= 1) {
						$str = "次のターンには";
					} else {
						$turn = int($turn);
						$str = "${turn}ターン後に";
					}
					logSecret("　--- <span class='attention'>警告！</span> $str備蓄食料がなくなると推測されます。",$id) if($turn <= 50);
				}
				$food = ($food >= 0) ? "${HtagFood_}$food" : "<span class='attention'>$food";
				$food .= ($island->{'randomfood'}) ? "$HunitFood${H_tagFood} ランダム収穫：${HtagFood_}$island->{'randomfood'}" : '';
				my $uMoney = - $island->{'upkeepMoney'};
				$uMoney .= ($island->{'upkeepMoneyPlus'}) ? "$HunitMoney${H_tagMoney} 収入：${HtagMoney_}$island->{'upkeepMoneyPlus'}" : '';
				$uMoney .= ($island->{'upkeepMoneyProbe'}) ? "$HunitMoney${H_tagMoney} 調査費：${HtagMoney_}-$island->{'upkeepMoneyProbe'}" : '';
				my $uFood = - $island->{'upkeepFood'};
				$uFood .= ($island->{'upkeepFoodPlus'}) ? "$HunitFood${H_tagFood} 収穫：${HtagFood_}$island->{'upkeepFoodPlus'}" : '';
				my $sMoney = - $island->{'shellMoney'};
				my $inMoney = $island->{'inMoney'};
				$inMoney .= ($island->{'prizemoney'}) ? "$HunitMoney${H_tagMoney} 獲得賞金：${HtagMoney_}" . $island->{'prizemoney'} : '';
				$inMoney .= ($island->{'randommoney'}) ? "$HunitMoney${H_tagMoney} ランダム収入：${HtagMoney_}" . $island->{'randommoney'} : '';
				$inMoney .= ($island->{'upkeepAlly'}) ? "$HunitMoney${H_tagMoney} 同盟維持費：${HtagMoney_}" . - $island->{'upkeepAlly'} : '';
				$inMoney .= ($island->{'upkeepAmity'}) ? "$HunitMoney${H_tagMoney} 友好国維持費：${HtagMoney_}" . - $island->{'upkeepAmity'} : '';
				my $pFood = - $island->{'payFood'};
				my $name = islandName($island);

				$logS[0] = "　--- 総合収支 資金：$money$HunitMoney${H_tagMoney} 食料：$food$HunitFood${H_tagFood}";
				$logS[1] = "　--- 艦隊 維持費：${HtagMoney_}$uMoney$HunitMoney${H_tagMoney} 維持食料：${HtagFood_}$uFood$HunitFood${H_tagFood} 弾薬費：${HtagMoney_}$sMoney$HunitMoney${H_tagMoney}";
				$logS[2] = "　--- 基本収支 資金：${HtagMoney_}$inMoney$HunitMoney${H_tagMoney} 食料生産量：${HtagFood_}$island->{'inFood'}$HunitFood${H_tagFood} 消費量：${HtagFood_}$pFood$HunitFood${H_tagFood}";
				$logS[3] = "${HtagName_}${name}${H_tagName}<B>《収支報告》</B>";
				foreach (0..3) {
					1 while $logS[$_] =~ s/(.*\d)(\d\d\d)/$1,$2/;
					logSecret("$logS[$_]",$id);
				}
			}
		}

		# 艦艇算出処理
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
						# そこが平地か荒地なら、町
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
				$Hislands[$i]->{'gain'} = 0;# ついでに経験値もリセットしたりして(^^;
				logItemLost($Hislands[$i]->{'id'}, islandName($Hislands[$i]), "保有していたすべての$HitemName[0]", "海軍消滅とともに");
			}
		}
		# 勝者判定(サバイバルモード・トーナメントモード)
		if(
			( $HsurvivalTurn && ($remainNumber == $HbfieldNumber + 1) && ($HislandTurn > $HsurvivalTurn) ) ||
			( $Htournament && ($remainNumber == $HbfieldNumber + 1) && ($HislandTurn > $HyosenTurn) )
		) {
			my $name = islandName($Hislands[$HbfieldNumber]);
			logHistory("${HtagName_}${name}${H_tagName}が<B>勝利</B>しました！");
			$Hislands[$HbfieldNumber]->{'ext'}[0] |= (2 ** $#HwinnerMark);
			$repeatTurn = 0;
			$HplayNow = 0;
		}

		# 終了条件の判定
		my $n = gameOver();
		if ($n != -1) {
			my($v) = 2 ** $#HwinnerMark;
			if($HarmisticeTurn) {
				logHistory("${HtagName_}${Hally[$n]->{'name'}}${H_tagName}が<B>勝利</B>しました！");
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
				logHistory("${HtagName_}${name}${H_tagName}が<B>トップ</B>で終了しました！");
				$Hislands[$HbfieldNumber]->{'ext'}[0] |= $v;
			}
			$repeatTurn = 0;
			$HplayNow = 0;
		}

		# 歴代記録処理
		if($HuseRekidai) {
			require './hako-reki.cgi';
			mainReki();
		}
		# ポイント処理
#		if($HrankKind eq 'point') {
#			foreach $i (0..$islandNumber) {
#				calcPoint($i);
#			}
#			# 順位を更新
#			islandSort($HrankKind, 1);
#		}
		# トーナメントログ
		fightlog() if($Htournament && ($tournamentflg == 3 || $tournamentflg == 1));

		# バックアップターンであれば、書く前にrename
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

			# ログファイルだけ戻す
			foreach $i (0..$HlogMax) {
				copy("${HdirName}.bak0/$i$HlogData", "${HdirName}/$i$HlogData") if (-e "${HdirName}.bak0/$i$HlogData");
			}
			copy("${HdirName}.bak0/hakojima.his", "${HdirName}/hakojima.his") if (-e "${HdirName}.bak0/hakojima.his");
		}

		# ファイルに書き出し
		writeIslandsFile(-1);

		# ログファイルを後ろにずらす
		for($i = ($HlogMax - 1); $i >= 0; $i--) {
			$j = $i + 1;
			my($s) = "${HdirName}/$i$HlogData";
			my($d) = "${HdirName}/$j$HlogData";
			unlink($d);
			rename($s, $d);
		}

		# 負荷計算(追加 親方20020307 by ラスティア)
		if($Hperformance) {
			my($uti, $sti, $cuti, $csti) = times();
			$uti += $cuti;
			$sti += $csti;
			my($cpu) = $uti + $sti;

			# ログファイル書き出し(テスト計測用　普段はコメントにしておいてください)
			#open(POUT,">>cpu-t.log");
			#print POUT "CPU($cpu) : user($uti) system($sti)\n";
			#close(POUT);

			logLate("<SMALL>負荷計測 CPU($cpu) : user($uti) system($sti)</SMALL>",0);
		}

		# ログ書き出し
		logFlush();

		# まだターン進行する？
		if ($repeatTurn) {
			# 終了ターンならループを抜ける
			last if ($HgameLimitTurn && ($HislandTurn >= $HgameLimitTurn));

			# 必要な変数を初期化する
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
	# トップへ
	topPageMain();
}

# 終了かどうか
sub gameOver {
	# 時間切れ
	if($HgameLimitTurn) {
		if ($HislandTurn >= $HgameLimitTurn) {
			# トップの陣営をかえす
			return 0;
		}
	}
	# コールド
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

# ファイルを丸ごとコピー
#sub copy {
#	my($src, $dest) = @_;
#
#	open(FS, "<$src") || die $!;
#	open(FD, ">$dest") || die $!;
#	binmode(FS); # Windowsローカルでは必要
#	binmode(FD); # Windowsローカルでは必要
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

# ディレクトリ消し
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

# 参加島への制裁内容を読み込む
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

	# 制裁データを削除する
	unlink("${HdirName}/punish.cgi");
}


# 管理人あずかり死滅処理
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

# 収入、消費フェイズ
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
	# 収入
	if($pop > $farm) {
		# 農業だけじゃ手が余る場合
		$island->{'inFood'} = int($farm * $HincomeRate * $fflag); # 農場フル稼働
		$island->{'inMoney'} =
		min(
			int(($pop - $farm) * $HincomeRate * $mflag / 10),
			int(($factory + $mountain) * $HincomeRate * $mflag)
		);
	} else {
		# 農業だけで手一杯の場合
		$island->{'inFood'} = int($pop * $HincomeRate * $fflag); # 全員野良仕事
	}
	$island->{'down'} = 1 if($pop - ($farm + $factory * 10 + $mountain * 10) >= $Hno_work);

	# 食料消費
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

# ログをまとめる
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
			$point .= "の<B>$snoケ所</B>" if($i > 1 || !$HoutPoint);
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

# コマンドフェイズ
sub doCommand {
	my($island) = @_;

	# コマンド取り出し
	my($comArray, $command, $c);
	$comArray = $island->{'command'};
	$command = $comArray->[0]; # 最初のを取り出し
	slideFront($comArray, 0); # 以降を詰める

	# 各要素の取り出し
	my($kind, $target, $x, $y, $arg, $target2) = 
	(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'target2'}
	);

	# 導出値
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
			# 資金繰り
			$island->{'money'} += $HdoNothingMoney;
			$island->{'inMoney'} += $HdoNothingMoney;
			if(!$HflagDoNothing) {
				$island->{'absent'} ++;

				# 陣営預かり判定
				if ($HarmisticeTurn && ($island->{'absent'} > $HpreGiveupTurn)) {
					# passwardを陣営パスワードに変更（毎ターン）
#					$island->{'password'} = encode($ally->{'Takayan'});
					$island->{'preab'} = 1;
					$island->{'comment'} = "この${AfterName}は陣営預かりになりました。";
				}
			}

			# 自動放棄
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

#-------海軍建造の場合は、ここでコストを500に上書きする---------
	if (($HcomNavy[0] <= $kind) && ($kind <= $HcomNavy[$#HnavyName])) { #海軍建造で
            if($HnavyBuildTurn[$kind - $HcomNavy[0]] != 0){ #建造ターンが存在する
                $cost = 0;
            }
        }

	# コストチェック
	my($returnflag) = 0;
	if(($cost > 0) && ($island->{'money'} < $cost)) {
		# 金の場合
		logNoMoney($id, $name, $comName);
		$returnflag = 1;
	} elsif(($cost < 0) && ($island->{'food'} < (-$cost))) {
		# 食料の場合
		logNoFood($id, $name, $comName);
		$returnflag = 1;
	}
	if(($kind == $HcomAutoPrepare3 || $kind == $HcomFastFarm || $kind == $HcomFastFactory) && ($HislandFightMode == 2)){
		logLandNG($id, $name, $comName, '現在戦闘期間中のため');
		$returnflag = 1;
	}
	if($HoceanMode) {
		if($HlandID[$x][$y] != $id) {
			# 対象地形のIDが自島でない場合
			if(($kind < 90) || ((100 < $kind) && ($kind < 200)) || ((330 < $kind) && ($kind < 350)) || ($kind == $HcomNavyWreckRepair) || ($kind == $HcomNavyWreckSell)) {
				# 内政(開発)，内政(建設)，複合施設，海軍(建造) <200 , 330< 軍事(建設) <350 , 残骸修理，残骸売却はできない
				logNotAvail($id, $name, $comName);
				$returnflag = 1;
			}
		}
		if(((215 < $kind) && ($kind < 220)) || ((350 < $kind) && ($kind < 361))) {
			# 移動操縦，移動指令，艦艇指令変更，一斉攻撃と軍事(攻撃)
			# 内政，建造以外で，座標指定するものは，念のため$targetを修正
			$target = $HlandID[$x][$y];
		}
	}

	if($returnflag) {
		if($island->{'comflag'}) {
			# 回数付きなら、コマンドを戻す
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
	# コマンドで分岐
	if($kind == $Hcomshikin){

	    $island->{'money'} += 2000;
	    logPropaganda($id, $name, $comName);

	    # 回数付きなら、コマンドを戻す
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
		# 整地、地ならし
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
			# 海、海底基地、油田、防波堤、機雷、山、怪獣、巨大怪獣、コア(海)、複合地形(設定なし)、海軍は整地できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		if($landKind == $HlandComplex) {
			# 複合地形なら設定地形
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

		# 金を差し引く
		$island->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# 地ならし
			$island->{'prepare2'}++;
		} else {
			# 整地なら、埋蔵金の可能性あり
			if(!$HnoDisFlag && random(1000) < $HdisMaizo) {
				my($v) = 100 + random(901);
				$island->{'money'} += $v;
				logMaizo($id, $name, $comName, $v);
			}
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomPrepare3) {
		# 一括地ならし
		my($i, $sx, $sy);
		my($prepareM, $prepareFlag) = ($HcomCost[$HcomPrepare2], 0);
		foreach $i (0..$island->{'pnum'}) {
			$sx = $island->{'rpx'}[$i];
			$sy = $island->{'rpy'}[$i];
			last if($island->{'money'} < $HcomCost[$HcomPrepare2]);
			if($land->[$sx][$sy] == $HlandWaste) {
				# 目的の場所を平地にする
				$land->[$sx][$sy] = $HlandPlains;
				$landValue->[$sx][$sy] = 0;
				if(($prepareM > 0) && ($island->{'money'} < $prepareM)) {
					logNoMoney($id, $name, $comName);
					return 0;
				}
				# 金を差し引く
				$island->{'money'} -= $prepareM;
				my $sno = @{$island->{'prepare'}};
				$island->{'prepare'}->[$sno]->{x} = $sx;
				$island->{'prepare'}->[$sno]->{y} = $sy;
				# 地ならし
#				$island->{'prepare2'}++;
				$prepareFlag++;
				if($prepareFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
#		logAllPrepare($id, $name, $comName);
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomReclaim) || ($kind == $HcomReclaim2)) {
		# 埋め立て、高速埋め立て
		if(($landKind != $HlandSea) &&
			($landKind != $HlandOil) &&
			($landKind != $HlandBouha) &&
			($landKind != $HlandSeaMine) &&
			($landKind != $HlandSbase) &&
			!(($landKind == $HlandCore) && int($lv / 10000)) &&
			!(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'reclaim'}[0] ne '')) &&
			($landKind != $HlandNavy)) {
			# 海、海底基地、油田、防波堤、機雷、コア(海)、複合地形(設定あり)、海軍しか埋め立てできない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 周りに陸があるかチェック
		my($seaCount) =
			countAround($island, $x, $y, $an[1], $HlandSea, $HlandOil, $HlandSeaMine, $HlandSbase, $HlandResource);
		$seaCount += countAroundNavy($island, $x, $y, $an[1]) if($HnavyReclaim);
		$seaCount += countAroundMonster($island, $x, $y, $an[1]) if($HmonsterReclaim);

		if($seaCount == 7) {
			# 全部海だから埋め立て不能
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "島の最外周", $point);
				return 0;
			}
		}

		if ($landKind == $HlandNavy) {
			# 海軍の場合、軍港のみ
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			my $nSpecial = $HnavySpecial[$nKind];
			unless ($nSpecial & 0x8) {
				# 港以外は埋め立てできない
				logLandFail($id, $name, $comName, $landName, $point);
				return 0;
			}

                        if($id != $nId){
                                # 余所の軍港も埋め立てできない
				logLandFail($id, $name, $comName, $landName, $point);
				return 0;
                        }

			$island->{'navyPort'}--;
			$island->{'shipk'}[$nKind]--;
		} elsif($landKind == $HlandCore) {
			$island->{'core'}--;
		}

		if($landKind == $HlandComplex) {
			# 複合地形なら設定地形
#			my $cKind = (landUnpack($lv))[1];
			$land->[$x][$y] = $HcomplexAfter[$cKind]->{'reclaim'}[0];
			$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'reclaim'}[1];
			$island->{'complex'}[$cKind]--;
			#$island->{'area'}++; この処理は見送り
		} elsif((($landKind == $HlandSea) && ($lv == 1)) || (($landKind == $HlandCore) && (int($lv / 10000) == 1))) {
			# 浅瀬の場合
			# 目的の場所を荒地にする
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			$island->{'area'}++;

			if($seaCount <= 4) {
				# 周りの海が3ヘックス以内なので、浅瀬にする
				my($i, $sx, $sy);
				foreach $i (1..6) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					# 行による位置調整
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];

					if (($sx < 0) || ($sy < 0)) {
						# 範囲外の場合何もしない
					} else {
						# 範囲内の場合
						$landValue->[$sx][$sy] = 1 if ($land->[$sx][$sy] == $HlandSea);
					}
				}
			}
		} else {
			# 海なら、目的の場所を浅瀬にする
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'bouha'}-- if($landKind == $HlandBouha); # 防波堤のとき
		}
#		logLandSuc($id, $name, $comName, $point);
		my $sno = @{$island->{'reclaim'}};
		$island->{'reclaim'}->[$sno]->{x} = $x;
		$island->{'reclaim'}->[$sno]->{y} = $y;
		# 金を差し引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomDestroy) || ($kind == $HcomDestroy2)) {
		# 掘削、高速掘削
		if(($landKind == $HlandSbase) ||
			($landKind == $HlandOil) ||
			($landKind == $HlandSeaMine) ||
			($landKind == $HlandBouha) ||
			($landKind == $HlandMonster) ||
			($landKind == $HlandHugeMonster) ||
			(($landKind == $HlandCore) && (int($lv / 10000) != 2)) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'destroy'}[0] eq '')) ||
			($landKind == $HlandNavy)) {
			# 海底基地、油田、機雷、防波堤、怪獣、巨大怪獣、コア(海)、複合地形(設定なし)、海軍は掘削できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		if(($landKind == $HlandSea) && (!$lv)) {
			# 海なら、油田探し
			if ($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) {
				# 開発期間中は油田禁止
				logNotAvail($id, $name, $comName);
				return 0;
			}
			# 投資額決定
			$arg = 1 if(!$arg);
			my($value, $str, $p);
			$value = min($arg * ($cost), $island->{'money'});
			$str = "$value$HunitMoney";
			$p = int($value / $cost) if($cost);
			$island->{'money'} -= $value;

			# 見つかるか判定
			if($p > random(100) + $island->{'oil'} * 25) {
				# 油田見つかる
				logOilFound($id, $name, $point, $comName, $str);
				$land->[$x][$y] = $HlandOil;
				$landValue->[$x][$y] = 0;
				$island->{'oil'}++;
			} else {
				# 無駄撃ちに終わる
				logOilFail($id, $name, $point, $comName, $str);
			}
			return $HcomTurn[$kind];
		}

		# 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
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
			# 複合地形なら設定地形
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

		# 金を差し引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSellTree) {
		# 伐採
		if($landKind != $HlandForest) {
			# 森以外は伐採できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
#		logLandSuc($id, $name, $comName, $point);
		my $sno = @{$island->{'selltree'}};
		$island->{'selltree'}->[$sno]->{x} = $x;
		$island->{'selltree'}->[$sno]->{y} = $y;

		# 売却金を得る
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

		# 地上建設系
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

			# 不適当な地形
			logLandFail($id, $name, $comName, $landName, $point);
			if($island->{'comflag'}) {
				# 回数付きなら、コマンドを戻す
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

		# 種類で分岐
		if(($kind == $HcomPlant) ||
                   ($kind == $HcomPlant)) {
			# 目的の場所を森にする。
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # 木は最低単位
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			return if(!$HuseBase);
			# 目的の場所をミサイル基地にする。
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # 経験値0
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomHaribote) {
			# 目的の場所をハリボテにする
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
		    if ($HdBaseHide) { # 防衛施設を森に偽装する?
				logPBSuc($id, $name, $comName, $point);
		    } else {
				logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
			}
		} elsif($kind == $HcomBouha) {
			return if(!$HuseBouha);
			# 目的の場所を防波堤にする。
			if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
				my($map) = $island->{'map'};
				my(@x) = @{$map->{'x'}};
				my(@y) = @{$map->{'y'}};
				if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
					logLandFail($id, $name, $comName, "島の最外周", $point);
					return 0;
				}
			}
			if($island->{'bouha'} >= $HuseBouha) {
				# 保有可能最大数オーバー
				logOverFail($id, $name, $comName, $point);
				return 0;
			}
			$land->[$x][$y] = $HlandBouha;
			$landValue->[$x][$y] = 0;
			$island->{'bouha'}++;
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomFarm || $kind == $HcomFastFarm) {
			# 農場
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			if($rep > 1) {
				my $value = min($rep * $cost, $island->{'money'});
				$rep = int($value / $cost) if($cost);
				$comName .= "($rep回)";
				$cost *= $rep;
				$arg = 1;
			}
			if($landKind == $HlandFarm) {
				# すでに農場の場合
				$landValue->[$x][$y] += 2*$rep; # 規模 + 2000人
			} else {
				# 目的の場所を農場に
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10 + 2*($rep - 1); # 規模 = 10000人
			}
			if($landValue->[$x][$y] > 50) {
				$landValue->[$x][$y] = 50; # 最大 50000人
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomFactory || $kind == $HcomFastFactory) {
			# 工場
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			if($rep > 1) {
				my $value = min($rep * $cost, $island->{'money'});
				$rep = int($value / $cost) if($cost);
				$comName .= "($rep回)";
				$cost *= $rep;
				$arg = 1;
			}
			if($landKind == $HlandFactory) {
				# すでに工場の場合
				$landValue->[$x][$y] += 10*$rep; # 規模 + 10000人
			} else {
				# 目的の場所を工場に
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30 + 10*($rep - 1); # 規模 = 10000人
			}
			if($landValue->[$x][$y] > 100) {
				$landValue->[$x][$y] = 100; # 最大 100000人
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif(($kind == $HcomDbase) ||
		        ($kind == $HcomDbase2)) {
			# 防衛施設
			$arg = 1 if(!$arg);
			my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
			# 一度に数量分の耐久力を追加したい場合
			# 上の1行をコメントアウトして下のコメントをはずす
			#my $rep = $arg;
			if($landKind == $HlandDefence) {
				# すでに防衛施設の場合
				if(!$HdurableDef) {
					$landValue->[$x][$y] += 10000; # 自爆装置セット
					logBombSet($id, $name, $landName, $point);
					$island->{'money'} -= $cost;
					return $HcomTurn[$kind];
				} elsif($arg == $HdefExplosion) {
					$landValue->[$x][$y] += 10000; # 自爆装置セット
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
					$comName .= "(耐久力$rep)";
					$cost *= $rep;
					$arg = 1;
				}
				# 目的の場所を防衛施設に
				$land->[$x][$y] = $HlandDefence;
				$rep = 1 if(!$HdurableDef);
				$landValue->[$x][$y] = $rep - 1;
				$island->{'dbase'}++;
				if ($HdBaseHide) { # 防衛施設を森に偽装する?
				    logPBSuc($id, $name, $comName, $point);
				} else {
				    logLandSuc($id, $name, $comName, $point);
				}
			}
		} elsif($kind == $HcomMonument) {
			# 記念碑
			if($HuseBigMissile && ($landKind == $HlandMonument)) {
				# すでに記念碑の場合

				# ターゲット取得
				my($tn) = $HidToNumber{$target};
				my($tIsland) = $Hislands[$tn];
				my(%amityFlag);
				my($amity) = $island->{'amity'};
				foreach (@$amity) {
					$amityFlag{$_} = 1;
				}
				# 開発期間ならコマンドを無視
				if (
					($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn || $amityFlag{$target})) ||
					($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
					) {
					# 攻撃が許可されていない
					logNotAvail($id, $name, $comName);
					return 0;
				} elsif(($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($id, $name, $comName);
					return 0;

				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($id, $name, $comName, '現在開発期間中のため');
						return 0;
					} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
						# 対戦相手じゃない場合は中止
						logLandNG($id, $name, $comName, '目標が対戦相手でないため');
						return 0;
					}
				} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
					my $warflag = chkWarIsland($id, $target);
					if(!$warflag) {
						logLandNG($id, $name, $comName, '宣戦布告をしていないため');
						return 0;
					} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
						logLandNG($id, $name, $comName, '猶予期間中のため');
						return 0;
					}
				} elsif($tIsland->{'event'}[0]) {
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($id, $name, $comName, '現在イベント準備期間中のため');
						return 0;
					} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# イベントタイプがサバイバル
						logLandNG($id, $name, $comName, 'サバイバル開催中のため');
						return 0;
					}
				}

				if($tn eq '') {
					# ターゲットがすでにない
					# 何も言わずに中止
					return 0;
				}

				$tIsland->{'bigmissile'}++;
				$island->{'ext'}[1] += $cost; #貢献度
				$tIsland->{'ext'}[1] += $cost; #貢献度

				# その場所は荒地に
				$land->[$x][$y] = $HlandWaste;
				$landValue->[$x][$y] = 0;
				logMonFly($id, $name, $landName, $point);
			} else {
				# 目的の場所を記念碑に
				$land->[$x][$y] = $HlandMonument;
				$arg = 0 if($arg >= $HmonumentNumber);
				$landValue->[$x][$y] = $arg;
				logLandSuc($id, $name, $comName, $point);
			}
		}

		# 金を差し引く
		$island->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
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
		# 複合地形建設

                # 平地の伐採はダメ
		if(($landKind == $HlandPlains) && ($kind == $HcomComplex[4])){
			# 森以外は伐採できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

                # 都市の伐採もダメ
		if(($landKind == $HlandTown) && ($kind == $HcomComplex[4])){
			# 森以外は伐採できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		$arg = 1 if(!$arg);
		my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
		if($rep > 1) {
			my $value = min($rep * $cost, $island->{'money'});
			$rep = int($value / $cost) if($cost);
			$comName .= "($rep回)";
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
		# 回数付きなら、コマンドを戻す
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
		# 採掘場
		if($landKind != $HlandMountain) {
			# 山以外には作れない
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
			$comName .= "($rep回)";
			$cost *= $rep;
			$arg = 1;
		}

		$landValue->[$x][$y] += 5*$rep; # 規模 + 5000人
		if($landValue->[$x][$y] > 200) {
			$landValue->[$x][$y] = 200; # 最大 200000人
		}
		logLandSuc($id, $name, $comName, $point);

		# 金を差し引く
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
		# 機雷
		return if(!$HuseSeaMine);
		if($landKind == $HlandSeaMine){
			# すでに機雷なら除去
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, '機雷除去', '(?, ?)');
			$arg = min($lv, int($island->{'money'} / ($cost * 0.2))) if($cost);
			$island->{'money'} -= $arg * ($cost * 0.2);
			$island->{'mine'}--;
			return $HcomTurn[$kind];
		} elsif(($landKind != $HlandSea) || $lv){
			# 海以外には作れない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "島の最外周", $point);
				return 0;
			}
		}
		if($island->{'mine'} >= $HuseSeaMine) {
			logOverFail($id, $name, $comName, $point);
			return 0;
		}

		# 破壊力上限 $HmineDamageMax
		if(!$arg){
			$arg = 1;
		} elsif($arg > $HmineDamageMax){
			$arg = $HmineDamageMax;
		}
		my $value = min($arg * $cost, $island->{'money'});
		$arg = int($value / $cost) if($cost);
		$land->[$x][$y] = $HlandSeaMine;
		$landValue->[$x][$y] = $arg; # 破壊力
		logLandSuc($id, $name, $comName, '(?, ?)');

		# 金を差し引く
		$island->{'money'} -= $value;
		$island->{'mine'}++;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSbase) {
		# 海底基地
		return if(!$HuseSbase || $Htournament);
		if(($landKind != $HlandSea) || $lv){
			# 海以外には作れない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($x < $x[0] + $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $y[0] + $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "島の最外周", $point);
				return 0;
			}
		}

		$land->[$x][$y] = $HlandSbase;
		$landValue->[$x][$y] = 0; # 経験値0
		logLandSuc($id, $name, $comName, '(?, ?)');

		# 金を差し引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomCore) {
		return if(!$HuseCore);
		if ($HuseCoreLimit && ($HislandTurn - $island->{'birthday'} > $HdevelopTurn)) {
			logDevelopTurnFail2($id, $name, $comName);
			return 0;
		}
		# コア
		$arg = 1 if(!$arg);
		my $rep = (!$HcomTurn[$kind]) ? $arg : 1;
		# 一度に数量分の耐久力を追加したい場合
		# 上の1行をコメントアウトして下のコメントをはずす
		#my $rep = $arg;
		if($landKind == $HlandCore) {
			# すでにコアの場合
			if(!$HdurableCore) {
				# 不適当な地形
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
				# 平地か海でなければ作れない
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
				$comName .= "(耐久力$rep)";
				$cost *= $rep;
				$arg = 1;
			}
			# 目的の場所をコアに
			$land->[$x][$y] = $HlandCore;
			$rep = 1 if(!$HdurableCore);
			$landValue->[$x][$y] = $rep - 1;
			$island->{'core'}++;
			if($landKind == $HlandSea) {
				$landValue->[$x][$y] += (!$lv) ? 20000 : 10000; # 海，浅瀬
			}
			if ($HcoreHide) { # コアを偽装する?
				if($landKind == $HlandPlains) {
				    logPBSuc($id, $name, $comName, $point);     # 森
				} else {
					logLandSuc($id, $name, $comName, '(?, ?)'); # 海
				}
			} else {
			    logLandSuc($id, $name, $comName, $point);
			}
		}
		# 金を差し引く
		$island->{'money'} -= $cost;
		# 回数付きなら、コマンドを戻す
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
		# ミサイル系
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


		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];

		if ($id != $target) {
			# 他の島への攻撃

			# 発射可否確認
			# 開発期間ならコマンドを無視
			if (
				($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# 攻撃が許可されていない
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '現在【管理人あずかり】のため');
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '現在開発期間中のため');
					return 0;
				} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
					# 対戦相手じゃない場合は中止
					logLandNG($id, $name, $comName, '目標が対戦相手でないため');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
				my $warflag = chkWarIsland($id, $target);
				if(!$warflag) {
					logLandNG($id, $name, $comName, '宣戦布告をしていないため');
					return 0;
				} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
					logLandNG($id, $name, $comName, '猶予期間中のため');
					return 0;
				}
			} elsif($tIsland->{'event'}[0]) {
				if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '現在イベント準備期間中のため');
					return 0;
				} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
					# イベントタイプがサバイバル
					logLandNG($id, $name, $comName, 'サバイバル開催中のため');
					return 0;
				}
			}
		}

		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		# 0の場合は撃てるだけ
		$arg = 10000 if($arg == 0);

		# ミサイル発射
		require('./hako-missile.cgi');
		return 0 unless(missileFire($target, $island, $tIsland, $x, $y, $kind, $arg, $cost));
		if (!$HcomTurn[$kind] && ($HmissileSpecial[$kind - $HcomMissile[0]] & 0x1)) {
			# 次のコマンドが STミサイルか ST怪獣派遣でなければターン消費なし
			$HflagST = 1 if($HattackST);
			return 0 if (!($STcheck{$comArray->[0]->{'kind'}}) &&
				 ($comArray->[0]->{'kind'} != $HcomSendMonsterST));
		}
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomSendMonster) ||
		($kind == $HcomSendMonsterST)) {
		# 怪獣派遣
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
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);


		if ($id != $target) {
			# 他の島への攻撃
			if($HoceanMode && $HnotuseMonsterSend) {
				my($fw) = $island->{'wmap'};
				my($tw) = $tIsland->{'wmap'};
				if($HislandConnect[$fw->{'x'}][$fw->{'y'}] == $HislandConnect[$tw->{'x'}][$tw->{'y'}]) {
					logLandNG($id, $name, $comName, '海域が接続しているため');
					return 0;
				}
			}

			my(%amityFlag);
			my($amity) = $island->{'amity'};
			foreach (@$amity) {
				$amityFlag{$_} = 1;
			}
			# 開発期間ならコマンドを無視
			if (
				($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn || $amityFlag{$target})) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# 攻撃が許可されていない
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '現在【管理人あずかり】のため');
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '現在開発期間中のため');
					return 0;
				} elsif($island->{'fight_id'} != $tIsland->{'id'}) {
					# 対戦相手じゃない場合は中止
					logLandNG($id, $name, $comName, '目標が対戦相手でないため');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$HarmisticeTurn && !$HsurvivalTurn) {
				my $warflag = chkWarIsland($id, $target);
				if(!$warflag) {
					logLandNG($id, $name, $comName, '宣戦布告をしていないため');
					return 0;
				} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
					logLandNG($id, $name, $comName, '猶予期間中のため');
					return 0;
				}
			} elsif($tIsland->{'event'}[0]) {
				if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '現在イベント準備期間中のため');
					return 0;
				} elsif(($tIsland->{'event'}[6] == 1) && ($HislandTurn > $tIsland->{'event'}[1])) {
					# イベントタイプがサバイバル
					logLandNG($id, $name, $comName, 'サバイバル開催中のため');
					return 0;
				}
			}
		}

		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		# メッセージ
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
		# メカいのらを送る
		bringMonster($tIsland, ($kind == $HcomSendMonsterST) ? 0 : $id, $arg, $huge);

		$island->{'money'} -= $cost;
		$island->{'ext'}[1] += $cost; # 貢献度
		$tIsland->{'ext'}[1] += $cost; # 貢献度

		if (!$HcomTurn[$kind] && ($kind == $HcomSendMonsterST)) {
			# 次のコマンドが STミサイルか ST怪獣派遣でなければターン消費なし
			$HflagST = 1 if($HattackST);
			return 0 if (!($STcheck{$comArray->[0]->{'kind'}}) &&
				 ($comArray->[0]->{'kind'} != $HcomSendMonsterST));
		}
		return $HcomTurn[$kind];

	} elsif (($HcomNavy[0] <= $kind) && ($kind <= $HcomNavy[$#HnavyName])) {
		# 海軍建造
		return 0 unless (buildNavy($island, $comName, $kind - $HcomNavy[0], $arg, $x, $y));

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif (($HcomNavy2[0] <= $kind) && ($kind <= $HcomNavy2[3])) {
		# 航空機海外発進
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];

		if($tn eq '') {
			# ターゲットがすでにない
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
		# 艦隊移動(派遣・帰還)

		my($ftarget, $ttarget);
		if($kind == $HcomNavyMove) {
			# 艦隊移動
			($ftarget, $ttarget) = ($target, $target2);
		} elsif($kind == $HcomNavySend) {
			# 艦隊派遣
			($ftarget, $ttarget) = ($id, $target);
		} else {
			# 艦隊帰還
			($ftarget, $ttarget) = ($target, $id);
		}
		$comName = ($id == $ttarget) ? '艦隊帰還' : '艦隊派遣';
		# 艦隊移動元ターゲット取得
		my($fn) = $HidToNumber{$ftarget};
		if($fn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($fromIsland) = $Hislands[$fn];

		# 艦隊移動先ターゲット取得
		my($tn) = $HidToNumber{$ttarget};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($toIsland) = $Hislands[$tn];
		if($HoceanMode && $HnotuseNavyMove) {
			my($fw) = $fromIsland->{'wmap'};
			my($tw) = $toIsland->{'wmap'};
			if($HislandConnect[$fw->{'x'}][$fw->{'y'}] == $HislandConnect[$tw->{'x'}][$tw->{'y'}]) {
				logLandNG($id, $name, $comName, '海域が接続しているため');
				return 0;
			}
		}

                # 派遣可否フラグ初期化
                $moveErrorFlag = 0;

		if ($id != $ttarget) {
			# 他の島への攻撃
			# 開発期間ならコマンドを無視

			if (($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
				($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
				) {
				# 攻撃が許可されていない
				logNotAvail($id, $name, $comName);
				return 0;
			} elsif (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
				($HislandTurn - $toIsland->{'birthday'} <= $HdevelopTurn)) {
				logDevelopTurnFail($id, $name, $comName);
				return 0;
			} elsif(!$HforgivenAttack && $toIsland->{'predelete'}) {
				logLandNG($id, $name, $comName, '現在【管理人あずかり】のため');
				return 0;
			} elsif($HnofleetNotAvail && !$toIsland->{'field'} && !$toIsland->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "艦隊を保有しない$AfterNameであったため");
				return 0;

			} elsif($Htournament) {
				if($HislandFightMode < 2) {
					logLandNG($id, $name, $comName, '現在開発期間中のため');
					return 0;
				} elsif($island->{'fight_id'} != $toIsland->{'id'}) {
					# 対戦相手じゃない場合は中止
					logLandNG($id, $name, $comName, '目標が対戦相手でないため');
					return 0;
				}
			} elsif(($HuseDeWar > 1) && !$toIsland->{'field'} && !$HarmisticeTurn && !$HsurvivalTurn) {
                                # 民間船派遣の可能性があるので、ここでのreturnは無しにする
                                # 代わりにフラグ立てて、movefleetのルーチン内でエラー返す

				my(%amityFlag);
				my($amity) = $island->{'amity'};
				foreach (@$amity) {
					$amityFlag{$_} = 1;
				}
				if(!$amityFlag{$ttarget}) { 
					my $warflag = chkWarIsland($id, $ttarget);
#					if(!$warflag) {
#						logLandNG($id, $name, $comName, '宣戦布告をしていないため');
#						return 0;
#					} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
#						logLandNG($id, $name, $comName, '猶予期間中のため');
#						return 0;
#					}

					if($warflag != 2) {
                                            $moveErrorFlag = 1;
                                        }
				}

			} elsif($toIsland->{'event'}[0]) {
				my $level = 2 ** gainToLevel($island->{'gain'});
				if(($toIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $toIsland->{'event'}[1])) {
					logLandNG($id, $name, $comName, '現在イベント準備期間中のため');
					return 0;
				} elsif($toIsland->{'event'}[3] && ($toIsland->{'event'}[3] <= $island->{"invade$ttarget"})) {
					logLandNG($id, $name, $comName, '派遣可能艦艇数を超えるため');
					return 0;
				} elsif($HmaxComNavyLevel && !($toIsland->{'event'}[5] & (2 ** gainToLevel($island->{'gain'})))) {
					logLandNG($id, $name, $comName, '派遣可能レベルでないため');
					return 0;
				} elsif((!$toIsland->{'event'}[11]) && ($HislandTurn > $toIsland->{'event'}[1])) {
					# 追加派遣を許可しない
					logLandNG($id, $name, $comName, 'イベント開催中のため');
					return 0;
				}

			} elsif($island->{'NavyAttack_flag'}[$arg - 1]) {
				# コマンドを許可しない
				logLandNG($id, $name, $comName, '戦闘状態にあるため');
				return 0;
			}
		}


		# ４艦隊のみ
		$arg--;
		if ($arg < 0) {
			$arg = 0;
		} elsif ($arg > 3) {
			$arg = 3;
		}

		# 艦隊を移動する
		return 0 unless (moveFleet($island, $fromIsland, $toIsland, $arg));
		$island->{'money'} -= $cost;
		if($id != $ttarget) {
			$island->{'ext'}[1] += $cost; # 貢献度
			$toIsland->{'ext'}[1] += $cost; # 貢献度
			$island->{'NavyMove_flag'}[$arg] = 1; # 移動フラグを立てる
		}
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyForm) {
		# 艦隊編成
		if ($landKind != $HlandNavy) {
			# 海軍しか艦隊編成できない
			logNavyFormFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# 港、残骸、他の島の艦隊、は艦隊編成できない
			logNavyFormFail($id, $name, $point, $landName);
			return 0;
		}

		# ４艦隊のみ
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
		# 艦艇除籍(目標艦指定)
		if ($landKind != $HlandNavy) {
			# 海軍しか目標にできない
			logNavyTargetFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# 港と他の島の艦隊は除籍にできない
			logNavyTargetFail($id, $name, $point, $landName);
			return 0;
		}

		#$landValue->[$x][$y] = navyPack(0, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp); # 所属島なしにする
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack(0, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # 所属島なし(通常)にする

		logNavyTarget($id, $name, $point, $landName);

		$island->{'money'} -= $cost;
		$island->{'shipk'}[$nKind]--;
		$island->{'ships'}[$nNo]--;
		$island->{'ships'}[4]--;
		# サバイバル
		$island->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyDestroy) {
		# 艦艇破棄

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか破棄できない
			logNavyDestroyFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];

		if (($nSpecial & 0x8) || ($nId != $id)) {
			# 港と他の島の艦隊は破棄できない
			logNavyDestroyFail($id, $name, $point, $tLandName);
			return 0;
		}

		$tLand->[$x][$y] = $HlandSea; # 海にする
		$tLandValue->[$x][$y] = 0;

		logNavyDestroy($id, $name, $point, $tLandName, $tId);

		$island->{'money'} -= $cost;
		$island->{'shipk'}[$nKind]--;
		$island->{'ships'}[$nNo]--;
		$island->{'ships'}[4]--;
		# サバイバル
		$island->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyWreckRepair) {
		# 残骸修理
		if ($landKind != $HlandNavy) {
			# 海軍しか修理できない
			logNavyWreckRepairFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless ($nFlag == 1) {
			# 残骸以外は修理できない
			logNavyWreckRepairFail($id, $name, $point, $landName);
			return 0;
		}
		$cost = int($HnavyCost[$nKind] * ($nExp / 100.0) * $cflag);
		if ($island->{'money'} < $cost) {
			# 資金が足りない
			logNoMoney($id, $name, $comName);
			return 0;
		}

		# ４艦隊のみ
		$arg--;
		if ($arg < 0) {
			$arg = 0;
		} elsif ($arg > 3) {
			$arg = 3;
		}

		my $ofname = $island->{'fleet'}->[$arg];

		# 保有可能艦艇数チェック
		my $nflag = int($island->{'itemAbility'}[3]);
		my $nflagk = (!$#HnavyName) ? 1 : int($nflag/$#HnavyName);
		$nflagk = 1 if($nflag && ($nflagk < 1));
		if($HnavyMaximum && ($island->{'ships'}[4] >= $HnavyMaximum + $nflag)) {
			logNavyMaxOver($id, $name, $comName);
			return 0;
		} elsif($HportRetention && ($island->{'ships'}[4] >= $island->{'navyPort'} * $HportRetention + $nflag)) {
			logFleetMaxOver($id, $name, $comName, "１軍港あたり");
			return 0;
		} elsif($HfleetMaximum && ($island->{'ships'}[$arg] >= $HfleetMaximum + int($nflag/4))) {
			logNavyWreckRepairMaxOver($id, $name, $point, $landName, "${ofname}艦隊");
			return 0;
		} elsif($HnavyKindMax[$nKind] && ($island->{'shipk'}[$nKind] >= $HnavyKindMax[$nKind] + $nflagk)) {
			logNavyKindMaxOver($id, $name, $comName);
			return 0;
		}
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($id, $nTmp, $nStat, $nSea, 0, 0, $arg, $nKind, $wait, $HnavyHP[$nKind], $goalx, $goaly);
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$arg]++;
		$island->{'ships'}[4]++;

		# 移動済みにする
		$HnavyMove[$id][$x][$y] = 2;

		logNavyWreckRepair($id, $name, $point, $landName, $cost, "${ofname}艦隊");

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif ($kind == $HcomNavyWreckSell) {
		# 残骸売却
		if ($landKind != $HlandNavy) {
			# 海軍しか売却できない
			logNavyWreckSellFail($id, $name, $point, $landName);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless ($nFlag& 1) {
			# 残骸以外は売却できない
			logNavyWreckSellFail($id, $name, $point, $landName);
			return 0;
		}

		# 売却価格は「残骸の価値 × 相場(50%〜100%)」
		$cost = int($HnavyCost[$nKind] * (1.0 - $nHp / 100.0) * ((rand(6) + 5) / 10.0));

		$land->[$x][$y] = $HlandSea; # 海になる
		$landValue->[$x][$y] = 0;

		if (rand(100) < $HnavyProbWreckGold) {
			my $cost = int(rand(10) + 1) * 100; # 100億〜1000億円
			logNavyWreckSellLucky($id, $name, $point, $landName, $cost);
			$island->{'money'} += $cost;
		} elsif($HitemRest && $HitemGetDenominator3 && (random($HitemGetDenominator3) < $island->{'gain'})) {
			# アイテム獲得判定
			my $num = @Hitem;
			$num = random($num);
			push(@{$island->{'item'}}, $Hitem[$num]);
			$HitemGetId[$Hitem[$num]]{$id} = 1;
			$HitemRest--;
			logItemGetLucky2($id, $name, $point, $HitemName[$Hitem[$num]], "$landNameを引き上げたところ");
			splice(@Hitem, $num, 1);
		}

		logNavyWreckSell($id, $name, $point, $landName, $cost);

		$island->{'money'} += $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomMoveTarget) {
		# 旗艦(派遣怪獣)を移動
		return if(!$HuseFlag);

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
					logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "コアでないため、", $tId);
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);#移動できるフラグ
                        $sFlag2 =(navyUnpack($tLandValue->[$x][$y]), 3)[5];#移動できないフラグ
			if((!$sFlag) || ($sFlag2)) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、");
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]), $lv2)[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、");
				return 0;
			}
		}

		my($sx, $sy, $via, $via1, $via2, $viaflag1, $viaflag2, $moveflag);
		if($arg > 6) { # ２マス移動の１マスめ
		# 経由点を調べる
			$sFlag = 0;
			$via1 = int(($arg - 5) / 2);
			$via2 = $via1 + (($arg - 5) % 2);
			$via2 = 1 if($via2 > 6);
			$viaflag1 = random(1); # ２通りの行き方があればランダムで試す
			$viaflag2 = ($viaflag1 + 1) % 2;
			$via = ($via1, $via2)[$viaflag1];
			$sx = $x + $ax[$via];
			$sy = $y + $ay[$via];
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			$via += 2; # $pre(先行移動フラグ)と兼用のため+2
			if($tL == $HlandNavy) {
				$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x3);
				if(moveNavy($id, $tIsland, $x, $y, $via)) {# 移動成功
					if($tLand->[$sx][$sy] == $HlandNavy) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# 移動時にトラブル？
					# 費用を引く
						logMoveFail($id, $tName, "($sx, $sy)", "トラブル発生のため、");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# 別ルートを試す
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# 行による位置調整
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(先行移動フラグ)と兼用のため
					if(moveNavy($id, $tIsland, $x, $y, $via)) {# 移動成功
						if($tLand->[$sx][$sy] == $HlandNavy) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# 移動時にトラブル？
							logMoveFail($id, $tName, "($sx, $sy)", "トラブル発生のため、");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#どのルートも移動できない
						logMoveFail($id, $tName,  $point, "移動ができないため、");
						$HnavyMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			} elsif($tL == $HlandMonster) {
				$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x3);
				if(moveMonster($id, $tIsland, $x, $y, $via, 0)) {# 移動成功
					if($tLand->[$sx][$sy] == $HlandMonster) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# 移動時にトラブル？
						logMoveFail($id, $tName,  "($sx, $sy)", "トラブル発生のため、");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# 別ルートを試す
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# 行による位置調整
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(先行移動フラグ)と兼用のため
					if(moveMonster($id, $tIsland, $x, $y, $via, 0)) {# 移動成功
						if($tLand->[$sx][$sy] == $HlandMonster) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# 移動時にトラブル？
							logMoveFail($id, $tName, "($sx, $sy)", "トラブル発生のため、");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#どのルートも移動できない
						logMoveFail($id, $tName,  $point, "移動ができないため、");
						$HmonsterMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			} elsif($tL == $HlandHugeMonster) {
				$sFlag = ($HhugeMonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x3);
				if(moveMonster($id, $tIsland, $x, $y, $via, 1)) {# 移動成功
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$sx][$sy]);
					if(($tLand->[$sx][$sy] == $HlandHugeMonster) && ($mHflag == 0)) {
						$x = $sx;
						$y = $sy;
						$arg = ($via1, $via2)[$viaflag2];
						$moveflag = 1;
					} else {# 移動時にトラブル？
						logMoveFail($id, $tName,  "($sx, $sy)", "トラブル発生のため、");
						$island->{'money'} -= $cost;
						return $HcomTurn[$kind];
					}
				} else {# 別ルートを試す
					$via = ($via1, $via2)[$viaflag2];
					$sx = $x + $ax[$via];
					$sy = $y + $ay[$via];
					# 行による位置調整
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					$via += 2; # $pre(先行移動フラグ)と兼用のため
					if(moveMonster($id, $tIsland, $x, $y, $via, 1)) {# 移動成功
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$sx][$sy]);
						if(($tLand->[$sx][$sy] == $HlandHugeMonster) && ($mHflag == 0)) {
							$x = $sx;
							$y = $sy;
							$arg = ($via1, $via2)[$viaflag1];
							$moveflag = 1;
						} else {# 移動時にトラブル？
							logMoveFail($id, $tName, "($sx, $sy)", "トラブル発生のため、");
							$island->{'money'} -= $cost;
							return $HcomTurn[$kind];
						}
					} else {#どのルートも移動できない
						logMoveFail($id, $tName, $point, "移動ができないため、");
						$HmonsterMove[$tId][$x][$y] = 2;
						return 0;
					}
				}
			}
		}

		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		$arg += 2; # $pre(先行移動フラグ)と兼用のため
		if($tL == $HlandNavy) {
			if($sFlag && moveNavy($id, $tIsland, $x, $y, $arg)) {
				$HnavyMove[$tId][$sx][$sy] = 2;
			} else {
				$HnavyMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "移動できないため、");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		} elsif($tL == $HlandMonster) {
			if($sFlag && moveMonster($id, $tIsland, $x, $y, $arg, 0)) {
				$HmonsterMove[$tId][$sx][$sy] = 2;
			} else {
				$HmonsterMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "移動できないため、");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		} elsif($tL == $HlandHugeMonster) {
			if($sFlag && moveMonster($id, $tIsland, $x, $y, $arg, 1)) {
				$HmonsterMove[$tId][$sx][$sy] = 2;
			} else {
				$HmonsterMove[$tId][$x][$y] = 2;
				logMoveFail($id, $tName, "($x, $y)", "移動できないため、");
				return ($moveflag ? $HcomTurn[$kind] : 0);
			}
		}
		# 費用を引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $Hcomgoalsetpre) {
                # 目的地指定(対象)

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
			logMoveFail($id, $tName, $point, '操縦できない地形のため', $tId);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id)) {
			# 港と他の島の艦隊は対象にできない
			logMoveFail($id, $ntNme, $point, '操縦できない地形のため', $tId);
			return 0;
		}

		my $sFlag = 0;
		if(($tL != $HlandNavy) && ($tL != $HlandMonster)) {
			if($tL == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$x][$y]);
				$sFlag = ($HhugeMonsterSpecial[$mKind] & 0x80);
				if(!$sFlag) {
					logMoveFail($id, $tName, $point, "操縦できない地形のため、");
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "コアでないため、");
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		}
                $island->{'setreadyid'} = $tId;
                $island->{'setreadyx'} = $x;
                $island->{'setreadyy'} = $y;
#               $setready = navyUnpack($lv, $lv2); # 先にデータ拾っておく
                logLandSuc($id, $tName, $comName, $point, $tId);
                return $HcomTurn[$kind];

	} elsif($kind == $Hcomgoalset) {
                # 目的地指令(目標)
                if(($island->{'setreadyx'} == 31) ||
                   ($island->{'setreadyy'} == 31)){
		        logMoveFail($id, $tName, $point, "事前の準備がなかったため、", $tId);
                        return 0;
               }

                # 指定元のデータ拾ってくる
                my $fId = $island->{'setreadyid'};
                my $fx = $island->{'setreadyx'};
                my $fy = $island->{'setreadyy'};

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

                if($target != $fId){
		        logMoveFail($id, $tName, $point, "異なる島への移動指示だったため、", $tId);
                        return 0;
                }

      		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);
		my($tId) = $tIsland->{'id'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tLandValue2) = $tIsland->{'landValue2'};

                my($fId, $fTmp, $fStat, $fSea, $fExp, $fFlag, $fNo, $fKind, $fWait, $fHp, $goalx, $goaly) = navyUnpack($tLandValue->[$fx][$fy], $tLandValue2->[$fx][$fy]);

                # 目的地だけ変えてpack
                ($tLandValue->[$fx][$fy], $tLandValue2->[$fx][$fy]) = navyPack($fId, $fTmp, $fStat, $fSea, $fExp, $fFlag, $fNo, $fKind, $fWait, $fHp, $x, $y);

                logLandSuc($id, $tName, $comName, $point, $tId);
                $island->{'setreadyx'} = 31;
                $island->{'setreadyy'} = 31;
                return 0;
	} elsif($kind == $Hcomremodel) {
                # 艦艇改修

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);

		if ($landKind != $HlandNavy) {
			# 海軍しか目標にできない
                        logLandFail($id, $name, $comName, $kind, $point);
			return 0;
		}

		if (($nKind != 8) && ($nKind != 9) && ($nKind != 10) && ($nKind != 11)){
                        # 霞しか目標にできない
                        logLandFail($id, $name, $comName, $landName, $point);
			return 0;
                }
		if ($nId != $id) {
			# 他の島の艦隊は対象にできない
	                logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		if ($nFlag != 0) {
			# 残骸だったり潜水してたり建造中でもダメ
                        logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

                # 周りに港があるかどうか
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

                # 移動済みフラグ
                $HnavyMove[$id][$x][$y] == 2;
		return $HcomTurn[$kind];

	} elsif($kind == $Hcomwork) {
                # スパイダー展開

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nKind != 2){
                         # スパイダーしか目標にできない
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
                }
		if ($nId != $id) {
			# 他の島の艦隊は対象にできない
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nFlag != 0) {
			# 残骸だったり潜水してたり建造中でもダメ
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($area >= $HdisFallBorder) {
			# 面積ギリだとダメ
                        logLandFail2($id, $name, $comName, "面積の限界を超える", $point);
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

                # 移動済みフラグ
                $HnavyMove[$id][$x][$y] == 2;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomSellPort) {
                # 軍港払下げ

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if (!$nSpecial & 0x8) {
			# 港以外は対象外
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nFlag) {
			# 工事とかしてたらダメ
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nId != $id) {
			# 他の島所属の艦隊は対象にできない
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		($tLandValue->[$x][$y], $tLandValue2->[$x][$y]) = navyPack(0, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # 所属島なしにする
		logSellPort($id, $tName, $point, $landName);

		$island->{'money'} += 10000;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomBuyPort) {
                # 軍港買収

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if (!$nSpecial & 0x8) {
			# 港以外は対象外
                       logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		if ($nId != 0) {
			# 所属不明以外は対象外
	                logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		($tLandValue->[$x][$y], $tLandValue2->[$x][$y]) = navyPack($id, $nTmp, 0, $nSea, $nExp, $nFlag, 0, $nKind, $wait, $nHp, $goalx, $goaly); # 所属島なしにする
		logBuyPort($id, $name, $point, $landName, $tId, $tName);

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomWarpA) {
                # 艦艇指定移動(移動元)

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
			logMoveFail($id, $tName, $point, '操縦できない地形のため', $tId);
			return 0;
		}

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if (($nSpecial & 0x8) || ($nId != $id) || $HnavyNoMove[$nKind]) {
			# 港と他の島の艦隊は対象にできない 動かない系の艦隊も
			logMoveFail($id, $ntNme, $point, '操縦できない地形のため', $tId);
			return 0;
		}

		if ($nFlag == 3) {
			# 工事してたらダメ
                        logLandFail($id, $name, $comName, $tLandName, $point);
			return 0;
		}

		my $sFlag = 0;
		if(($tL != $HlandNavy) && ($tL != $HlandMonster)) {
			if($tL == $HlandHugeMonster) {
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($tLandValue->[$x][$y]);
				$sFlag = ($HhugeMonsterSpecial[$mKind] & 0x80);
				if(!$sFlag) {
					logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
					return 0;
				} elsif($mHflag != 0) {
					logMoveFail($id, $tName, $point, "コアでないため、", $tId);
					return 0;
				}
			} else {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		} elsif($tL == $HlandNavy) {
			$sFlag = ($HnavySpecial[(navyUnpack($tLandValue->[$x][$y]), 0)[7]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		} elsif($tL == $HlandMonster) {
			$sFlag = ($HmonsterSpecial[(monsterUnpack($tLandValue->[$x][$y]))[5]] & 0x80);
			if(!$sFlag) {
				logMoveFail($id, $tName, $point, "操縦できない地形のため、", $tId);
				return 0;
			}
		}

                my($pcount, $px, $py) = searchNavyPort($tIsland, $x, $y, $an[1], 0, $id);
                if($pcount){
		    # 艦艇を記憶
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
                # 艦艇指定移動(移動先)

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
			# 海軍しか目標にできない
			logMoveFail($id, $tName, $point, '操縦できない地形のため', $tId);
			return
                }

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($tLandValue->[$x][$y], $tLandValue2->[$x][$y]);
		my $nSpecial = $HnavySpecial[$nKind];
		if ((!$nSpecial & 0x8) || ($nId != $id)) {
			# 自分の軍港しか対象にできない
			logMoveFail($id, $ntNme, $point, '操縦できない地形のため', $tId);
			return 0;
		}

                my $i;
                for($i = 1; $i <= 6; $i++){
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];

                        # 範囲外なら次
			if (($sx < 0) || ($sy < 0)) {
				next;
			}

			# 海じゃないなら次
			if($tLand->[$sx][$sy] != $HlandSea){
                            next;
                        }

                        while(@fleet){

		            # 艦艇の情報を取得
		            ($nId, $tId, $nx, $ny) = ($fleet[0]->{id}, $fleet[0]->{tId}, $fleet[0]->{x}, $fleet[0]->{y});

		            # ターゲット(移動元)取得
		            my($nn) = $HidToNumber{$nId};
		            if($nn eq '') {
			        # ターゲットがすでにない
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
                                # 他のプレイヤーのデータが残ってるんで詰める
                                shift @fleet;
                                next;
                            }

		            my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($nLv, $nLv2);
		            # 艦艇を移動

			    $tLand->[$sx][$sy] = $nLand->[$nx][$ny];
			    ($tLandValue->[$sx][$sy], $tLandValue2->[$sx][$sy]) = navyPack($nId, $nTmp, $nStat, ($tLand->[$x][$y] == $HlandSea ? $tLv : 0), $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);

			    $nLand->[$nx][$ny] = $HlandSea;
			    $nLandValue->[$nx][$ny] = $nSea; 
                            # ログだし(後で


		            shift @fleet;
                            last;
                        }

                }
                logLandSuc($id, $tName, $comName, $point, $tId);
		return $HcomTurn[$kind];
	} elsif($kind == $HcomMoveMission) {
		# 艦隊に対する目標地点への移動指令
		return if(!$HoceanMode);
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
		# 費用を引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomNavyTarget) {
		# 一斉攻撃命令
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
		# 費用を引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomAmity) {
		# 友好国 設定・解除
		# ターゲット取得
		return if(!$HuseAmity || $HarmisticeTurn || $Htournament);
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		# 駐留状況調査
		my(%invade);
		if($HamityDisarm) {
			foreach (@{$island->{'fkind'}}) {
				my($eId, $nFlag, $nKind) = (navyUnpack(hex($_), 0))[0,5,7];
				next if(($HnavySpecial[$nKind] & 0x8) || ($nFlag == 1)); # 軍港・残骸は除外
                                next if($HnavyNoMove[$nKind]); # 動かない系も除外  
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
					logAmity($id, $name, $target, "すべての${AfterName}");
				} else {
					logAmityMaxOver($id, $name, "すべての${AfterName}");
				}
			} else {
				@newamity = keys %invade;
				my($str);
				$str = '艦隊派遣中でない' if($HamityDisarm);
				logAmityEnd($id, $name, $target, "友好国であったすべての${str}${AfterName}");
			}
			$island->{'amity'} = \@newamity;
			# 費用を引く
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

		# 費用を引く
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif($kind == $HcomAlly) {
		# 同盟 加盟・脱退
		# ターゲット取得
		return if(!$HallyUse || !$HallyJoinComUse || $HarmisticeTurn || $Htournament);
		my($tn) = $HidToNumber{$target};
		my($tan) = $HidToAllyNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		} elsif($tan eq '') {
			$tan = $HidToAllyNumber{$Hislands[$tn]->{'allyId'}[0]};
		}
		if($tan eq '') {
			# ターゲットがすでにない
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
				# 開放
				logAllyMaxOver($id, $target, islandName($island), $ally->{'name'});
				return;
			}
		}
		$ally->{'memberId'} = \@newAllyMember;
		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomDeWar) || ($kind == $HcomCeasefire)) {
		# 宣戦布告・停戦
		# ターゲット取得
		return if(!$HuseDeWar || $HarmisticeTurn || $HsurvivalTurn || $Htournament);
		return 0 if($target == $id);
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}
		my($tIsland) = $Hislands[$tn];
		my($tName) = islandName($tIsland);
		# 開発期間ならコマンドを無視
		if (($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) ||
			($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
			logDevelopTurnFail($id, $name, $comName);
			return 0;
		} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
			logLandNG($id, $name, $comName, '現在【管理人あずかり】のため');
			return 0;
		} elsif($HnofleetNotAvail) {
			if(!$tIsland->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "艦隊を保有しない$AfterNameであったため");
				return 0;
			} elsif(!$island->{'ships'}[4]) {
				logLandNG($id, $name, $comName, "艦隊を保有していないため");
				return 0;
			}
		}
		$name = "${HtagName_}${name}${H_tagName}";
		$tName = "${HtagName_}${tName}${H_tagName}";
		my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
		# 友好国
		my(%amityFlag);
		my($amity) = $island->{'amity'};
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
		if(chkWarIsland($id, $target)){
			# 停戦交渉
			for($i=0;$i < $#HwarIsland;$i+=4){
				my($id1, $id2) = ($HwarIsland[$i+1], $HwarIsland[$i+2]);
				my($tn1) = $HidToNumber{$id1};
				next if($tn1 eq '');
				my($tn2) = $HidToNumber{$id2};
				next if($tn2 eq '');
				my $turn = $HwarIsland[$i];
				if(($id1 == $id) && ($id2 == $target)){
					# 停戦交渉１(宣戦布告した側)
					if($kind == $HcomDeWar){
						if($HwarIsland[$i+3] % 10 == 1){
							$HwarIsland[$i+3] = 0;
							logOut("${name}が${tName}に打診していた停戦を撤回し戦争継続を通告しました。",$id, $target);
						} elsif($HwarIsland[$i+3] % 10 == 2){
							$HwarIsland[$i+3] = 0;
							logOut("${name}が${tName}からの停戦交渉を破棄し戦争継続を通告しました。",$id, $target);
						}
					} elsif($HwarIsland[$i+3] % 10 == 2){
						# 停戦確定
						if($HwarIsland[$i] > $HislandTurn){
							# 戦争事前回避
							logOut("${name}と${tName}の戦争は回避されました。",$id, $target);
						} else {
							# 戦争停戦
							if($HceasefireAutoNavyReturn) {
								islandCeasefire($Hislands[$tn1], $id2);
								islandCeasefire($Hislands[$tn2], $id1);
							}
							logOut("${name}と${tName}の停戦合意により<B>ターン${turn}</B>から続いた戦争は終結しました。",$id, $target);
							logHistory("${HtagName_}${wname}${H_tagName}戦争(ターン${turn}〜${HislandTurn})は終結しました。");
						}
						splice(@HwarIsland,$i,4);
					} else {
						# 相手待ち
						$HwarIsland[$i+3] = $HislandTurn * 10 + 1;
						logOut("${name}が${tName}に<b>停戦の意思</b>を打診しました。",$id, $target);
					}
					last;
				} elsif(($id1 == $target) && ($id2 == $id)) {
					# 停戦交渉２
					if($kind == $HcomDeWar) {
						if($HwarIsland[$i+3] % 10 == 2){
							$HwarIsland[$i+3] = 0;
							logOut("${name}が${tName}に打診していた停戦を撤回し戦争継続を通告しました。",$id, $target);
						} elsif($HwarIsland[$i+3] % 10 == 1){
							$HwarIsland[$i+3] = 0;
							logOut("${name}が${tName}からの停戦交渉を破棄し戦争継続を通告しました。",$id, $target);
						}
					} elsif($HwarIsland[$i+3] % 10 == 1) {
						# 停戦確定
						if($HwarIsland[$i] > $HislandTurn){
							# 戦争事前回避
							logOut("${name}と${tName}の戦争は回避されました。",$id, $target);
						}else{
							# 戦争停戦
							if($HceasefireAutoNavyReturn) {
								islandCeasefire($Hislands[$tn1], $id2);
								islandCeasefire($Hislands[$tn2], $id1);
							}
							logOut("${name}と${tName}の停戦合意により<B>ターン${turn}</B>から続いた戦争は終結しました。",$id, $target);
							logHistory("${HtagName_}${wname}${H_tagName}戦争(ターン${turn}〜${HislandTurn})は終結しました。");
						}
						splice(@HwarIsland,$i,4);
					} else {
						# 相手待ち
						$HwarIsland[$i+3] = $HislandTurn * 10 + 2;
						logOut("${name}が${tName}に<B>停戦の意思</B>を打診しました。",$id, $target);
					}
					last;
				}
			}
		} elsif($kind == $HcomCeasefire) {
			# 停戦は無効
			return 0;
		} else {
			# 宣戦布告
			if($amityFlag{$target}){
				logOut("${name}から$tNameへの${HtagComName_}$comName${H_tagComName}は、$tNameが<B>友好国のため</B>、中止しました。",$id);
				return 0;
			}
			if($HmatchPlay) { # タイマンモード
				my $oId = chkWarIslandOR($id, $target);
				if($oId) {
					my $oName = islandName($Hislands[$HidToNumber{$oId}]);
					$oName = "${HtagName_}${oName}${H_tagName}";
					$otName = (chkWarIslandOR($id, $id)) ? $name : $tName;
					logOut("${name}から$tNameへの${HtagComName_}$comName${H_tagComName}は、$otNameが$oNameと<B>交戦中のため</B>、中止しました。",$id);
					return 0;
				}
			}
		#	$arg = ($arg < $HdeclareTurn) ? $HislandTurn + $HdeclareTurn : $HislandTurn + $arg;
			$arg = $HislandTurn + $HdeclareTurn;
			push(@HwarIsland, ($arg, $id, $target, 0));
			if($HdeclareTurn > 0) {
				logOut("${name}が${tName}に${HtagDisaster_}宣戦布告！！${H_tagDisaster}(<B>${arg}ターンに開戦</B>)",$id, $target);
			} else {
				my($wname) = "$name${HtagDisaster_} VS ${H_tagDisaster}$tName";
				logOut("${name}が${tName}に${HtagDisaster_}宣戦布告！！${H_tagDisaster}${wname}戦争勃発！！",$id, $target);
				logHistory("${wname}戦争勃発！！");
			}
		}

		$island->{'money'} -= $cost;
		return $HcomTurn[$kind];


	} elsif($kind == $HcomSell) {
		# 輸出量決定
		$arg = 1 if(!$arg);
		my($value) = min($arg * (-$HcomCost[$kind]), $island->{'food'});
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / ($island->{'food'}/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }

		# 輸出ログ
		logSell($id, $name, $comName, $value);
		$island->{'food'}  -=  int($value);
		$island->{'money'} += int($value * $foodrate / 400);
		return $HcomTurn[$kind];

	} elsif($kind == $HcomBuy) {
		# 輸入量決定
		$arg = 1 if(!$arg);
		my($value) = min($arg * $HcomCost[$kind], $island->{'money'});
		$value *= 10;
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / ($island->{'food'}/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }

		# 輸入ログ
		logBuy($id, $name, $comName, $value);
		$island->{'food'}  +=  int($value / $foodrate * 10 / 4);
		$island->{'money'} -= int($value/ 10);
		return $HcomTurn[$kind];

	} elsif(($kind == $HcomFood) || ($kind == $HcomMoney)) {
		# 援助系

		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
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
		# 他の陣営には援助できない
		if ($HarmisticeTurn && $HcampAidOnly && !$amityFlag{$target}) {
			logAidFail($id, $target, $name, $tName, $comName);
			return 0;
		}
		# 開発期間ならコマンドを無視
		if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn) {
			logDevelopTurnFail($id, $name, $comName);
			return 0;
		}

		# 貿易能力のある艦艇が派遣されていない島へは援助コマンドがつかえない
		if ($HtradeAbility) {
			my $tradeFlag = 1;
			my($fkind) = $island->{'fkind'};
			my @flist = @$fkind;
			foreach (@flist) {
				my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack(hex($_), 0);
				my $special = $HnavySpecial[$nKind];
				next if ($special & 0x8); # 軍港は除外
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

		# 援助量決定
		$arg = 1 if(!$arg);

		my($value, $str);
		if($HcomCost[$kind] < 0) {
			$value = min($arg * (-$HcomCost[$kind]), $island->{'food'});
			$str = "${HtagFood_}$value$HunitFood${H_tagFood}";
		} else {
			$value = min($arg * $HcomCost[$kind], $island->{'money'});
			$str = "${HtagMoney_}$value$HunitMoney${H_tagMoney}";
		}

		# 援助ログ
		logAid($id, $target, $name, $tName, $comName, $str);

		if($HcomCost[$kind] < 0) {
			$island->{'food'} -= $value;
			$tIsland->{'food'} += $value * 0.8;
			$island->{'ext'}[1] += int($value/10); # 貢献度
			$tIsland->{'ext'}[1] -= int($value/10); # 貢献度
			#$tIsland->{'ext'}[1] = 0 if($tIsland->{'ext'}[1] < 0);
		} else {
			$island->{'money'} -= $value;
			$tIsland->{'money'} += $value * 0.8;
			$island->{'ext'}[1] += $value; # 貢献度
			$tIsland->{'ext'}[1] -= $value; # 貢献度
			#$tIsland->{'ext'}[1] = 0 if($tIsland->{'ext'}[1] < 0);
		}
		return $HcomTurn[$kind];

	} elsif($kind == $HcomPropaganda) {
		# 誘致活動
		logPropaganda($id, $name, $comName);
		$island->{'propaganda'} = 1;
		$island->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
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
		# 放棄
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
	# イベント発生島への派遣
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
	# 艦隊を検索
	my(@fleet);
	my($i, $x, $y, $fLv, $fLv2);
	my $fSend = ($fId == $tId) ? 'で移動' : ($id == $tId) ? 'から帰還' : 'へ派遣';
	my $fSname = ($fId == $tId) ? $tName : ($id == $tId) ? $fName : $tName;
	foreach $i (0..$fIsland->{'pnum'}) {
		$x = $fIsland->{'rpx'}[$i];
		$y = $fIsland->{'rpy'}[$i];
		$fLv = $fLandValue->[$x][$y];
		$fLv2 = $fLandValue2->[$x][$y];

		# 海軍を探す
		next unless ($fLand->[$x][$y] == $HlandNavy);

		# 移動艦艇か？
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($fLv, $fLv2);
		next if (($nId != $id) || ($nNo != $no) || ($nFlag == 3));

		# 港なら無視
		my $nSpecial = $HnavySpecial[$nKind];
		next if ($nSpecial & 0x8);

                # 動かない系の艦隊も無視
                next if($HnavyNoMove[$nKind]);

		# イベント発生島の派遣可能艦艇判別
		next if ($kindFlag{$nKind} || ($kNew && $nExp));

                
                # 民間船以外の艦隊を送ろうとしていて、かつ派遣可否フラグがダメな場合
                if($Hprivate[$nKind] != 1){
                    if($moveErrorFlag == 1){
		        logLandNG($id, $name, $comName, '宣戦布告をしていないため');
		        return 0;
                    }
                }

		# 艦艇を記憶
		push(@fleet, { x => $x, y => $y });

		# イベント発生島の派遣可能艦艇数判別
		last if(--$eMax == 0);
	}

	$i = $#fleet + 1;
	my $ofname = $Hislands[$HidToNumber{$id}]->{'fleet'}->[$no];
	if(($id != $fId) && ($id != $tId)) {
		$no = "${HtagName_}${fName}${H_tagName}に派遣中の$ofname艦隊";
	} else {
		$no = "$ofname艦隊";
	}
	if ($i < 1) {
		# 艦隊なし
		logNavySendNone($id, $name, $tName, $no, $fSend);
		return 0;
	}

	# 艦隊移動
	my $sendshipStr = '';
	my($tx, $ty, $tLv);
	foreach $i (0..$tIsland->{'pnum'}) {
		$tx = $tIsland->{'rpx'}[$i];
		$ty = $tIsland->{'rpy'}[$i];
		$tLv = $tLandValue->[$tx][$ty];
		$tLv2 = $tLandValue2->[$tx][$ty];

		# 深い海、機雷を探す
		next unless ( (($tLand->[$tx][$ty] == $HlandSea) && (!$tLv || $HnavyMoveAsase)) ||
						(!$amityFlag{$id} && ($tLand->[$tx][$ty] == $HlandSeaMine)) );

		# 艦艇の情報を取得
		($x, $y) = ($fleet[0]->{x}, $fleet[0]->{y});
		$fLv = $fLandValue->[$x][$y];
		$fLv2 = $fLandValue2->[$x][$y];
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($fLv, $fLv2);

                # 目標地点のリセットと航続ターンの半減処理を行う
                $goalx = 31;
                $goaly = 31;
                if($HnavyCruiseTurn[$nKind] != 0){
                    $wait = int($wait/2);
                }

		# 艦艇を移動
		if($tLand->[$tx][$ty] == $HlandSeaMine) {
			# 自島の機雷でダメージを受けるかどうか(念のため)
			next if($amityFlag{$nId});
			# 機雷なら耐久力減少
			$nHp -= $tLandValue->[$tx][$ty];
			# ログ出力
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
			# 残骸になる
			$tLand->[$tx][$ty] = $fLand->[$x][$y];
			($tLandValue->[$tx][$ty], $tLandValue2->[$tx][$ty]) = navyPack(0, $nTmp, $nStat, ($tLand->[$tx][$ty] == $HlandSea ? $tLv : 0), int(rand(90)) + 10, 1, 0, $nKind, 0, 0, 31, 31);
			$island->{'shipk'}[$nKind]--;
			$island->{'ships'}[$nNo]--;
			$island->{'ships'}[4]--;
			# サバイバル
			$island->{'epoint'}{$tId} = $HislandTurn if($tIsland->{'event'}[6] == 1);
		} else {
			# 沈没
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
			$island->{'shipk'}[$nKind]--;
			$island->{'ships'}[$nNo]--;
			$island->{'ships'}[4]--;
			# サバイバル
			$island->{'epoint'}{$tId} = $HislandTurn if($tIsland->{'event'}[6] == 1);

		}
		$fLand->[$x][$y] = $HlandSea;
		$fLandValue->[$x][$y] = $nSea;
		$HlandMove[$fId][$x][$y] = 1;
		$HnavyAttackTarget{"$id,$x,$y"} = undef;

		# 移動済みにする
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
		# ログを出す
		$sendshipStr .= " <B>$HnavyName[$nKind]</B>${HtagName_}($tx, $ty)${H_tagName}";
		shift @fleet;
		last if(!@fleet);
	}
	my $restshipStr = '<BR>　--- 残留部隊 ⇒ ';
	if(@fleet > 0) {
		my(%restShip);
		foreach (@fleet) {
			# 艦艇の情報を取得
			($x, $y) = ($_->{x}, $_->{y});
			$fLv = $fLandValue->[$x][$y];
			$fLv2 = $fLandValue2->[$x][$y];
			my($nKind) = (navyUnpack($fLv, $fLv2))[7];
			$restShip{$nKind}++;
		}
		foreach (keys %restShip) {
			$restshipStr .= " <B>$HnavyName[$_]</B>${HtagName_}($restShip{$_}艦)${H_tagName}"
		}
	}
	if($sendshipStr eq '') {
		# 展開エリアなし
		logNavySendNoArea($id, $name, $tName, $no, $fSend, $restshipStr);
	} elsif(@fleet > 0) {
		# 展開エリア不足
		$sendshipStr .= $restshipStr;
		$island->{'epoint'}{$tId} = 0 if($tIsland->{'event'}[0]);
		logNavySendShip($id, $tId, $sendshipStr, substr($fSend, -4));
		logNavySend($id, $fId, $tId, $name, $fSname, $no, $fSend);
	} else {
		# 展開成功
		$island->{'epoint'}{$tId} = 0 if($tIsland->{'event'}[0] && !(defined $island->{'epoint'}{$tId}));
		logNavySendShip($id, $tId, $sendshipStr, substr($fSend, -4));
		logNavySend($id, $fId, $tId, $name, $fSname, $no, $fSend);
	}
	return 1;
}

# 島放棄された場合の艦隊処理
sub islandDeadNavy {
	my($island) = @_;

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($name)      = islandName($island);

	# 派遣されている艦隊がいるか調べる
	my(%fleet, $i, $n, $x, $y, $lv);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];

		if($HautoKeeper) {
			# 怪獣と巨大怪獣を海にする
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

		# 海軍を探す
		next unless ($land->[$x][$y] == $HlandNavy);

		# 自島の艦艇と無所属の艦艇は無視
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$n = $HidToNumber{$nId};
		if ($nId == $id) {
			# 自島の艦艇は無視
			$island->{'stayNavyExp'} += $nExp if($HmatchPlay > 3);
			next;
		} elsif(!(defined $n) || !$nId) {
			# すでに放棄されている島の艦艇と無所属の艦艇
			if($HautoKeeper) {
				# 海にする
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = $nSea;
				$HnavyAttackTarget{"$id,$x,$y"} = undef;
			} else {
				# 無視
				next;
			}
			next;
		}

		# 艦隊情報を記憶
		$fleet{$n}[$nNo]++;
		$Hislands[$n]->{'sendNavyExp'} += $nExp if($HmatchPlay > 3);
	}

	# 派遣されている艦隊を帰還させる
	foreach $n (keys %fleet) {
		foreach $i (0..3) {
			next unless ($fleet{$n}[$i]);
			moveFleet($Hislands[$n], $island, $Hislands[$n], $i);
		}
	}

	# 友好国解除
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
	# 交戦状態解除
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
	# 派遣艦艇・派遣怪獣の処理フラグ
	$HautoKeepID{$id} = 1 if($HautoKeeper || $island->{'delete'});
	# 同盟score処理
	islandDeadAlly($island) if($HallyNumber);
}

# 停戦合意の場合の艦隊処理($islandに派遣された$tIdの艦艇を帰還させる)
sub islandCeasefire {
	my($island, $tId) = @_;

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# 派遣されている艦隊がいるか調べる
	my(%fleet, $i, $x, $y, $lv);
	my $t = $HidToNumber{$tId};
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];
		$lv2 = $landValue2->[$x][$y];
		# 海軍を探す
		next unless ($land->[$x][$y] == $HlandNavy);
		# 自島の艦艇と無所属の艦艇は無視
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		if ($nId == $id) {
			# 自島の艦艇は無視
			$island->{'stayNavyExp'} += $nExp if($HmatchPlay > 3);
		} elsif($nId == $tId) {
			# 艦隊情報を記憶
			$fleet{$nNo}++;
			$Hislands[$t]->{'sendNavyExp'} += $nExp if($HmatchPlay > 3);
		}
	}
	# 派遣されている艦隊を帰還させる
	foreach $i (keys %fleet) {
		moveFleet($Hislands[$t], $island, $Hislands[$t], $i);
	}
}

# イベント時の艦隊チェック
sub islandEventNavy {
	my($island, $type) = @_;

	# 期間中で，コア壊滅による強制終了設定がない時，または，コアがある
	my($continueflag) = (($island->{'event'}[2] && ($island->{'event'}[1] + $island->{'event'}[2] > $HislandTurn)) && (!$island->{'event'}[23] || $island->{'core'})) ? 1 : 0;
	# 追加派遣がある場合，期間中は判定しない(コア壊滅による強制終了設定がない時，または，コアがある時)
	return 0 if(!$HeventLog && $island->{'event'}[11] && $continueflag);

	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# 派遣されている艦隊がいるか調べる
	my(%epoint, $x, $y, $n, %fleet, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my $lv = $landValue->[$x][$y];
		my $lv2 = $landValue2->[$x][$y];
		# 海軍を探す
		next if ($land->[$x][$y] != $HlandNavy);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$n = $HidToNumber{$nId};
		my $special = $HnavySpecial[$nKind];
		# 港？残骸？すでに放棄されている島の艦艇と無所属の艦艇
		next if (!(defined $n) || !$nId || ($special & 0x8) || ($nFlag == 1));
		# 艦隊情報を記憶
		$fleet{$n}[$nNo]++;
	}
	foreach (keys %fleet) {
		# epoint
		$epoint{$Hislands[$_]->{'id'}} = $Hislands[$_]->{'epoint'}{$id};
	}
	# 勝者判定
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
		# サバイバル
		return 0;
	} elsif(!$HeventLog && ($type != 1) && ($wno != 1) && ($epoint{$winner[0]} == $epoint{$winner[1]})) {
		# 艦艇経験値獲得, 艦艇撃沈, 怪獣退治, 賞金稼ぎ
		return 0 if((!$island->{'event'}[23] || $island->{'core'}));
	}
	# 艦艇がいるので，期間中は判定しない(コア壊滅による強制終了設定がない時，または，コアがある時)
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
				$detail .= "<BR>　--- <B>優勝：</B>";
			} elsif($dcount == 2) {
				$detail .= "<BR>　--- <B>準優勝：</B>";
			} else {
				$detail .= "<BR>　--- <B>第$dcount位：</B>";
			}
		} else {
			$detail .= "<BR>　--- <B>第$dcount位：</B>";
		}
		$detail .= "${HtagName_}${lName}${H_tagName}";
		if($type == 1) {
			$detail .= "(ターン${HtagNumber_}" . int($epoint{$winner[$_]}) ."${H_tagNumber})" if($_);
		} elsif($type == 5) {
			$detail .= '(' . int($epoint{$winner[$_]}) . $HunitMoney . ')';
		} else {
			$detail .= '(' . int($epoint{$winner[$_]}) .'点)';
		}
	}
	my $typeName  = $HeventName[$island->{'event'}[6]];
	my $name = islandName($island);
	# 期間中のログ出力
	if($eventLog) {
		logOut("${HtagDisaster_}$typeName${H_tagDisaster}(ターン${HtagNumber_}$island->{'event'}[1]${H_tagNumber}〜：於・${HtagName_}${name}${H_tagName})<B>経過報告</B>$detail", $id);
		return 0 if($continueflag);
	}
	my $tIsland = $Hislands[$HidToNumber{$winner[0]}];
	my $tName = islandName($tIsland);
	# 報償
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
		$prize .= "管理人プレゼント";
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
	$prize = 'なし' if($prize eq '');
	my($coreless);
	$coreless = "(${HtagDisaster_}$HlandName[$HlandCore][0]壊滅による強制終了${H_tagDisaster})" if(($island->{'event'}[2] && ($island->{'event'}[1] + $island->{'event'}[2] > $HislandTurn)) && $island->{'event'}[23] && !$island->{'core'});
	logOut("${HtagName_}${name}${H_tagName}でターン${HtagNumber_}$island->{'event'}[1]${H_tagNumber}から開催されていた${HtagDisaster_}$typeName${H_tagDisaster}で${HtagName_}${tName}${H_tagName}が<B>勝利</B>しました！$coreless(報償:<B>$prize</B>)$detail", $id, $winner[0]);

	# 自動帰還処理
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

# 先行処理
sub doPreEachHex {
	my($island) = @_;

	# 導出値
	my($name) = islandName($island);
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# ループ
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv)       = $landValue->[$x][$y];
		my($lv2)      = $landValue2->[$x][$y];

		if($landKind == $HlandMonster) {
			# 怪獣
			moveMonster(0, $island, $x, $y, 1, 0);
		} elsif($landKind == $HlandHugeMonster) {
			# 巨大怪獣
			my($mHflag) = (monsterUnpack($lv))[1];
			moveMonster(0, $island, $x, $y, 1, 1) if(!$mHflag);
		} elsif ($landKind == $HlandNavy) {
			# 海軍
			my($nStat) = (navyUnpack($lv, $lv2))[2];
			moveNavy(0, $island, $x, $y, 1) if($nStat < 3);
		}
	}
}

# 成長および単ヘックス災害
sub doEachHex {
	my($island) = @_;
	# 導出値
	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# 増える人口のタネ値
	my(@addpop)  = @Haddpop;

	if($Htournament && ($HislandTurn <= $HyosenTurn)) { # トーナメント
		# 連続資金繰りか、生産施設足りない場合ストップ
		@addpop = (0) x @Haddpop if(($island->{'absent'} >= $HstopAddPop) || $island->{'down'});
	} elsif($HsurvivalTurn) { # サバイバル
		if($HislandTurn <= $HsurvivalTurn){
			@addpop = @HaddpopSD;# 開発期間
		} else {
			@addpop = @HaddpopSA; # 戦闘期間
		}
	}
	if($island->{'food'} < 0) {
		# 食料不足
		@addpop = @HreductionPop;
	} elsif($island->{'propaganda'} == 1) {
		# 誘致活動中
		@addpop = (!$HsurvivalTurn) ? @HaddpopPropa : ($HislandTurn <= $HsurvivalTurn) ? @HaddpopSDpropa : @HaddpopSApropa;
	}

	# ループ
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];
		my($lv2) = $landValue2->[$x][$y];

		if($landKind == $HlandTown) {
			# 町系
			my $rank = 0;
			foreach (reverse(0..$#HlandTownValue)) {
				if($HlandTownValue[$_] <= $lv) {
					$rank = $_;
					last;
				}
			}
			if($addpop[$rank] < 0) {
				# 不足
				$lv -= (random(-$addpop[$rank]) + 1);
				if($lv <= 0) {
					# 平地に戻す
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} else {
				# 成長
				next if($HsurvivalTurn && $island->{'absent'});
				if($addpop[$rank]) {
					$lv += random($addpop[$rank]) + 1;
				}
			}
			$lv = $HvalueLandTownMax if($lv > $HvalueLandTownMax);
			$landValue->[$x][$y] = $lv;
		} elsif($landKind == $HlandPlains) {
			# 平地
			next if($HsurvivalTurn && $island->{'absent'});
			my $tflag = ($island->{'field'}) ? 1 : countGrow($island, $x, $y);
			my $rflag = (!$HsurvivalTurn) ? !($HtownGlow >= random(100)) : (($HislandTurn <= $HsurvivalTurn) ? random(3) : random(11));
			if(!$rflag && $tflag) {
				# 周りに農場、町があれば、ここも町になる
				$land->[$x][$y] = $HlandTown;
				$landValue->[$x][$y] = 1;
			}
		} elsif($landKind == $HlandForest) {
			# 森
			if($lv < 200) {
			# 木を増やす
				$landValue->[$x][$y] += $HtreeGrow;
			}
		} elsif($landKind == $HlandDefence) {
			if(int($lv / 100) > 0) {
				# 防衛施設自爆
				my($lName) = &landName($landKind, $lv);

				# 広域被害ルーチン
				wideDamage($id, $name, $island, $x, $y);
				logBombFire($id, $name, $lName, "($x, $y)");
				$island->{'dbase'}--;
			}
		} elsif($landKind == $HlandOil) {
			# 海底油田
			my($value, $str, $lName);
			$lName = landName($landKind, $lv);
			$value = $HoilMoney;
			if($HoilMoneyMin) {
				$value -= random($HoilMoney - $HoilMoneyMin + 1);
			}
			$island->{'money'} += $value;
			$island->{'oilincome'} += $value;
			$str = "$value$HunitMoney";

			# 収入ログ
			#logOilMoney($id, $name, $lName, "($x, $y)", $str, "収益");

			# 枯渇判定
			if(!$HnoDisFlag && random(1000) < $HoilRatio) {
				# 枯渇
				logOilEnd($id, $name, $lName, "($x, $y)");
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 0;
			}
		} elsif($landKind == $HlandWaste) {
			# 荒れ地(BattleField)
			if(!random(3) && $island->{'field'}) {
				if(!$landValue->[$x][$y]) {
					$land->[$x][$y] = $HlandPlains;
				} else {
					$landValue->[$x][$y]--;
				}
			}
		} elsif($landKind == $HlandComplex) {
			# 複合地形
			my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
			if($HcomplexTPCmax[$cKind]) {
				# ターンフラグ更新
				if($cTurn < $HcomplexTPCmax[$cKind]) {
					$cTurn++;
					$landValue->[$x][$y] = landPack($cTmp, $cKind, $cTurn, $cFood, $cMoney);
				}
			}
			my $attr = $HcomplexAttr[$cKind];
			if($attr & 0x1000) {
				# ランダム収入
				my $value = $HcomplexRinMoney[1] - $HcomplexRinMoney[0] + 1;
				$value = $HcomplexRinMoney[0] + random($value);
				$island->{'rinmoney'}[$cKind] += $value;
				$island->{'money'} += $value;
			}
			if($attr & 0x2000) {
				# ランダム収穫
				my $value = $HcomplexRinFood[1] - $HcomplexRinFood[0] + 1;
				$value = $HcomplexRinFood[0] + random($value);
				$island->{'rinfood'}[$cKind] += $value;
				$island->{'food'} += $value;
			}
			if($attr & 0x10) {
				# 力場
				my($i, $sx, $sy);
				for($i = 1; $i < $an[$HcomplexFieldHex]; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					# 行による位置調整
					$sx-- if(!($sy % 2) && ($y % 2));
					$sx = $correctX[$sx + $#an];
					$sy = $correctY[$sy + $#an];
					# 範囲外
					next if(($sx < 0) || ($sy < 0));
					if($land->[$sx][$sy] == $HlandMonster || $land->[$sx][$sy] == $HlandHugeMonster){
						# 周囲1Hexに別の怪獣がいる場合、その怪獣を攻撃する

						# 対象となる怪獣の各要素取り出し
						my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$sx][$sy]);
						my $mName = ($land->[$sx][$sy] == $HlandMonster) ? $HmonsterName[$mKind] : $HhugeMonsterName[$mKind];

						if(!$mHflag) {
							if($land->[$sx][$sy] == $HlandHugeMonster) {
								my($j, $ssx, $ssy);
								foreach $j (1..6) {
									next if($HhugeMonsterImage[$mKind][$j] eq '');
									$ssx = $sx + $ax[$j];
									$ssy = $sy + $ay[$j];
									# 行による位置調整
									$ssx-- if(!($ssy % 2) && ($sy % 2));
									$ssx = $correctX[$ssx + $#an];
									$ssy = $correctY[$ssy + $#an];
									# 範囲外
									next if(($ssx < 0) || ($ssy < 0));

									next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
									# 各要素の取り出し
									my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
									if ($mFlag2 & 2) {
										# 海にいた
										$land->[$ssx][$ssy] = $HlandSea;
										$landValue->[$ssx][$ssy] = $mSea2;
									} else {
										# 陸地にいた
										$land->[$ssx][$ssy] = $HlandWaste;
										$landValue->[$ssx][$ssy] = 0;
									}
									$HlandMove[$id][$ssx][$ssy] = 1;
								}
							}
							logIslpnt($id, $name, "($sx, $sy)", $mId, "の<B>$mName</B>が強力な力場に押し潰されました。");
						} else {
							logIslpnt($id, $name, "($sx, $sy)", $mId, "の<B>$mName</B>が強力な力場で体の一部を失いました。");
						}
						# 対象の怪獣が倒れる
						if ($mFlag & 2) {
							# 海にいた
							$land->[$sx][$sy] = $HlandSea;
							$landValue->[$sx][$sy] = $mSea;
						} else {
							# 陸地にいた
							$land->[$sx][$sy] = $HlandWaste;
							$landValue->[$sx][$sy] = 0;
						}
						$HlandMove[$id][$sx][$sy] = 1;
					}
				}
			}
		} elsif($landKind == $HlandMonster) {
			# 怪獣
			moveMonster(0, $island, $x, $y, 0, 0);
		} elsif($landKind == $HlandHugeMonster) {
			# 巨大怪獣
			my($mHflag) = (monsterUnpack($lv))[1];
			moveMonster(0, $island, $x, $y, 0, 1) if(!$mHflag);
		} elsif ($landKind == $HlandNavy) {
			# 海軍
			#my($nStat, $nFlag) = (navyUnpack($lv, $lv2))[2,5];
		        my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			moveNavy(0, $island, $x, $y, 0) if(($nStat < 3) && ($nFlag < 3));
                        # 工事を進める
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
                    if($landValue->[$x][$y]){ # 浅瀬は
                        if(!searchLand ($island, $x, $y)){ # 周囲に陸地が無かったら
                            $landValue->[$x][$y] = 0; # 深い海になる
                        }
                    }
		}

                # 海軍移動後のとこを掃除
		if ($landKind != $HlandNavy) {
		    $landValue2->[$x][$y] = 0;
                }

		# 火災判定
		if((($landKind == $HlandTown) && ($lv > 30)) ||
			(($landKind == $HlandComplex) && ($HcomplexAfter[my $cKind = (landUnpack($lv))[1]]->{'fire'}[0] ne '')) ||
			($landKind == $HlandHaribote) ||
			($landKind == $HlandFactory)) {
			if(!$HnoDisFlag && (random(1000) < $HdisFire * $island->{'itemAbility'}[22])) {
				# 周囲の森と記念碑を数える
				if(!(countAround($island, $x, $y, $an[1], $HlandForest, $HlandMonument)) &&
					!(countAroundComplex($island, $x, $y, $an[1], 0x2))) {
					# 無かった場合、火災で壊滅
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
						# 複合地形なら設定地形
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

# 単ヘックス処理2
sub doEachHex2 {
	my($island) = @_;
	# 導出値
	my($name)      = islandName($island);
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};

	# ループ
	my($x, $y, $i);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];
		my($lv2) = $landValue2->[$x][$y];

               if ($landKind == $HlandNavy) {
			# 海軍
			#my($nStat, $nFlag) = (navyUnpack($lv, $lv2))[2,5];
		        my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
			moveNavy(0, $island, $x, $y, 0) if(($nStat < 3) && ($nFlag < 3));
		}

                # 海軍移動後のとこを掃除
		if ($landKind != $HlandNavy) {
		    $landValue2->[$x][$y] = 0;
                }
	}
}


# 怪獣の移動(
# $tId追加→怪獣の移動には使わない(0でよい)
# $preが2以上で「移動操縦」(移動方向$arg = $pre - 2)
# $hugeが1なら巨大怪獣
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
		# 怪獣の移動なら$flagmoveを1にする
		$flagmove = 1;
	} elsif(!$arg) {
		# 怪獣操作で待機の場合
		$HmonsterMove[$id][$x][$y] = 2;
		return 1;
	}

	# すでに動いた？
	return if ($HmonsterMove[$id][$x][$y] == 2);

	# 各要素の取り出し
	my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($landValue->[$x][$y]);
	my $mName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = $HmonsterSpecial[$mKind];
	$special = $HhugeMonsterSpecial[$mKind] if($huge);

	if($flagmove) {
		# 怪獣の移動の場合
		if($pre) {
			# 先行移動
			my $mm  = $HidToNumber{$mId};
			if(!($special & 0x10)) {
				# 能力がない
				return;
			} elsif(defined $mm) {
				# 能力があり所属島がある
				# コマンドチェック(移動操縦をするか)
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
			# 先行移動でないのに能力がある
			return;
		}
	} else {
		# 移動操縦の場合
		return if($mId != $tId); # 自島の派遣怪獣？
		return if (!($special & 0x80)); # 能力がない
	}

	# 硬化状態を変更
	if (($special & 0x4) && (rand(1) < .50)) { # 50%
		$mFlag ^= 1;
		$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
	}

	# 陸上で硬化中？
	return if (($mFlag & 1) && !($mFlag & 2));

	# 攻撃目標を捕捉しミサイル攻撃する特殊能力
	if($special & 0x100) {
		require('./hako-mons-attack.cgi');
		# 硬化中でなければ攻撃対象を探す
		searchMonsterTarget($island, $x, $y, $huge) unless($mFlag & 1);
		# 攻撃予定がある？
		my $target = $HmonsterAttackTarget{"$id,$x,$y"};
		if (defined $target) {
			# 攻撃！
			($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterAttack($island, $x, $y, $target->{x}, $target->{y}, $huge);
			$HmonsterAttackTarget{"$id,$x,$y"} = undef;
		}

		return if (($land->[$x][$y] == $HlandWaste) || ($land->[$x][$y] == $HlandSea));
	}

	my($sx, $sy, $d, $ssx, $ssy, $d2, $dmove, $rebody, @bodyHp);
	# 巨大怪獣のコア以外を通常地形に戻す
	if($huge) {
		foreach $i (1..6) {
			next if($HhugeMonsterImage[$mKind][$i] eq '');
			$ssx = $x + $ax[$i];
			$ssy = $y + $ay[$i];
			# 行による位置調整
			$ssx-- if(!($ssy % 2) && ($y % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# 範囲外の場合
			next if(($ssx < 0) || ($ssy < 0));

			if($land->[$ssx][$ssy] != $HlandHugeMonster) {
				$rebody .= "$i";
				next;
			}
			# 各要素の取り出し
			my($mHflag2, $mSea2, $mFlag2, $mHp2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4, 6];
			next if($mHflag2 != $i);
			$bodyHp[$i] = $mHp2;
			if ($mFlag2 & 2) {
				# 海にいた
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = $mSea2;
			} else {
				# 陸地にいた
				$land->[$ssx][$ssy] = $HlandWaste;
				$landValue->[$ssx][$ssy] = 0;
			}
			$HlandMove[$id][$ssx][$ssy] = 1;
		}
	}
	if(($mHp < 1) && ($special & 0x100)) {
		if ($mFlag & 2) {
			# 海にいた
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = $mSea2;
		} else {
			# 陸地にいた
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
		}
		$HlandMove[$id][$x][$y] = 1;
		return 0;
	}

	# 動く方向を決定
	my $dnavy = 0;
	if($flagmove) { # 怪獣の移動
		my(@dir);
		if ($special & 0x20) {
			# 蹂躙移動
			my $kind;
			# 周囲を見回す
			# （あまり広い範囲を探さないようにしてください。余計なサーバ負荷になります）
			if ($d = searchTarget(0, $island, $x, $y, $an[3], $HlandHaribote, $HlandDefence, $HlandOil, $HlandSbase, $HlandBase, $HlandFarm, $HlandFactory, $HlandComplex, $HlandTown, $HlandNavy)) { # ３ヘックス
				# 目標が見つかった
				push(@dir, $d);
			}
		}

		for ($i = $#dir + 1; $i < 3; $i++) {
			push(@dir, random(6) + 1);
		}

		while ($d = shift @dir) {
			$sx = $x + $ax[$d];
			$sy = $y + $ay[$d];
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# 範囲外
			next if(($sx < 0) || ($sy < 0));
			if($HoceanMode) {
				# 未知の海域へは移動できない
				next if(!$HlandID[$sx][$sy]);
				if($HlandID[$sx][$sy] != $id) {
					# 設定のある時，バトルフィールドなら勝手に動けるのは同じ島の中
					next if($HfieldMonster && $island->{'field'});
					# 設定のある時，バトルフィールドへは入れない
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
					# 行による位置調整
					$ssx-- if(!($ssy % 2) && ($sy % 2));
					$ssx = $correctX[$ssx + $#an];
					$ssy = $correctY[$ssy + $#an];

					# 範囲外判定
					if(($ssx < 0) || ($ssy < 0)) {
						$dmove = 1;
						next;
					}
					if($HoceanMode) {
						# 未知の海域へは移動できない
						if(!$HlandID[$ssx][$ssy]) {
							$dmove = 1;
							next;
						}
						if($HlandID[$ssx][$ssy] != $id) {
							# 設定のある時，バトルフィールドなら勝手に動けるのは同じ島の中
							if($HfieldMonster && $island->{'field'}) {
								$dmove = 1;
								next;
							}
							# 設定のある時，バトルフィールドへは入れない
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
					# 怪獣、巨大怪獣、山、記念碑，コアなら移動できない
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
				# 怪獣、巨大怪獣、山、記念碑，コアなら移動できない
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

			# 移動できる地形
			last;
		}

		# 移動できなかった？
		unless(defined $d) {
			$HmonsterMove[$id][$x][$y] = 2;
			if($huge) {
				$dmove = 1;
			} else {
				return;
			}
		}

	} else { # 怪獣操作
		$dmove = 0;
		$arg %= 7;
		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# 範囲外判定
		if(($sx < 0) || ($sy < 0)) {
			$HmonsterMove[$id][$x][$y] = 2;
			return;
		}
		if($HoceanMode && ($HlandID[$sx][$sy] != $id)) {
			# 自島でない場合
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
					# 攻撃が許可されていない
					logNotAvail($mId, $name, $comName);
					$mflag = 1;
				} elsif (($HislandTurn - $nIsland->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($mId, $name, $comName);
					$mflag = 1;
				} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
					logLandNG($mId, $name, $comName, '現在【管理人あずかり】のため');
					$mflag = 1;
				} elsif($HfieldUnconnect && $tIsland->{'field'}) {
					logLandNG($mId, $name, $comName, '海域が接続していない');
					$mflag = 1;

				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($mId, $name, $comName, '現在開発期間中のため');
						$mflag = 1;
					} elsif($mIsland->{'fight_id'} != $tIsland->{'id'}) {
						# 対戦相手じゃない場合は中止
						logLandNG($mId, $name, $comName, '目標が対戦相手でないため');
						$mflag = 1;
					}
				} elsif(($HuseDeWar > 1) && !$tIsland->{'field'} && !$HarmisticeTurn && !$HsurvivalTurn) {
					if(!$amityFlag{$tIsland->{'id'}}) {
						my $warflag = chkWarIsland($mId, $tIsland->{'id'});
						if(!$warflag) {
							logLandNG($mId, $name, $comName, '宣戦布告をしていないため');
							$mflag = 1;
						} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
							logLandNG($mId, $name, $comName, '猶予期間中のため');
							$mflag = 1;
						}
					}
				} elsif($tIsland->{'event'}[0]) {
					my $level = 2 ** gainToLevel($island->{'gain'});
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($mId, $name, $comName, '現在イベント準備期間中のため');
						$mflag = 1;
					} elsif((!$tIsland->{'event'}[11]) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# 追加派遣を許可しない
						logLandNG($mId, $name, $comName, 'イベント開催中のため');
						$mflag = 1;
					}
				}
			} else {
				# 島のない海域へは動けない
				logLandNG($mId, $name, $comName, '未知の海域であるため');
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
				# 行による位置調整
				$ssx-- if(!($ssy % 2) && ($sy % 2));
				$ssx = $correctX[$ssx + $#an];
				$ssy = $correctY[$ssy + $#an];

				# 範囲外判定
				if(($ssx < 0) || ($ssy < 0)) {
					$dmove = 1;
					last;
				}
				if($HoceanMode) {
					# 未知の海域へは移動できない
					if(!$HlandID[$ssx][$ssy]) {
						$dmove = 1;
						last;
					}
					if($HlandID[$ssx][$ssy] != $id) {
						# 設定のある時，バトルフィールドなら勝手に動けるのは同じ島の中
						if($HfieldMonster && $island->{'field'}) {
							$dmove = 1;
							last;
						}
						# 設定のある時，バトルフィールドへは入れない
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
				# 怪獣、巨大怪獣、山、記念碑，コアなら移動できない
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
			# 怪獣、巨大怪獣、山、記念碑，コアなら移動できない
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

	# 移動先の地形によりメッセージ
	my($l)     = $land->[$sx][$sy];
	my($lv)    = $landValue->[$sx][$sy];
	my($lv2)   = $landValue2->[$sx][$sy];
	my($lName) = landName($l, $lv);
	my($point) = "($sx, $sy)";

	if ($l == $HlandNavy) {
		# 海軍
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $nSpecial = $HnavySpecial[$nKind];
		unless (($nSpecial & 0x8) || ($nFlag == 1)) {
			# 港でも残骸でもない
			if ($nHp > 1) {
				# 耐久力を減らす
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

	# 巨大怪獣が移動できなかった場合、コア以外を復元
	if($huge && ($dmove || $dnavy)) {
		foreach $i (1..6) {
			next if(($HhugeMonsterImage[$mKind][$i] eq ''));
			$ssx = $x + $ax[$i];
			$ssy = $y + $ay[$i];
			# 行による位置調整
			$ssx-- if(!($ssy % 2) && ($y % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# 範囲外
			next if(($ssx < 0) || ($ssy < 0));
			# 移動できない地形なら復元しない
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
				# 海
				$mFlag2 |= 2;
				$mSea2 = $landValue->[$ssx][$ssy];
			} elsif (($land->[$ssx][$ssy] == $HlandSbase) || ($land->[$ssx][$ssy] == $HlandOil) || ($land->[$ssx][$ssy] == $HlandBouha) || ($land->[$ssx][$ssy] == $HlandSeaMine)) {
				# 海の施設を破壊
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
						# サバイバル
						$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					$HnavyAttackTarget{"$id,$ssx,$ssy"} = undef;
				}
			} elsif ($land->[$ssx][$ssy] == $HlandComplex) {
				my $cKind = (landUnpack($landValue->[$ssx][$ssy]))[1];
				my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
				if($cFlag) { # 海系
					$mFlag2 |= 2;
					$mSea2 = $HcomplexAfter[$cKind]->{'move'}[1];
				} else { # 陸系
					$mFlag2 &= ~2;
					$mSea2 = 0;
				}
				$island->{'complex'}[$cKind]--;
			} elsif ($land->[$ssx][$ssy] == $HlandWaste) {
				# 荒れ地
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
			# 行による位置調整
			$ssx-- if(!($ssy % 2) && ($sy % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# 範囲外
			next if(($ssx < 0) || ($ssy < 0));
			next if ($land->[$ssx][$ssy] != $HlandNavy);

			# 移動先の地形によりメッセージ
			$lName2 = landName($land->[$ssx][$ssy], $landValue->[$ssx][$ssy]);
			$point2 = "($ssx, $ssy)";

			my($mSea2);
			# 海軍
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$ssx][$ssy], $landValue2->[$ssx][$ssy]);
			my $nSpecial = $HnavySpecial[$nKind];
			if ($nHp > 1) {
				# 耐久力を減らす
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
						# サバイバル
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
		# 海にいた
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = $mSea;
	} else {
		# 陸地にいた
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
	}
	$HlandMove[$id][$x][$y] = 1;

	# 移動
	my $dm = ($flagmove ? $d : $arg);
	if ($l == $HlandSea) {
		# 海を移動
		$mFlag |= 2;
		$mSea = $lv;
		logMonsMoveSea($id, $name, $lName, $point, $mName, $mId) if($huge == 0);
	} elsif (($l == $HlandSbase) || ($l == $HlandOil) || ($l == $HlandBouha)) {
		# 海の施設を破壊
		$mFlag |= 2;
		$mSea = 0;
		if($l == $HlandBouha) {
			$mSea = 1;
			$island->{'bouha'}--;
		}
		logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
	} elsif ($l == $HlandNavy) {
		# 海軍を破壊
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
				# サバイバル
				$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
			}
			$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
		}
		logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
	} elsif ($l == $HlandSeaMine) {
		# 機雷なら生命力減少
		$mHp -= $landValue->[$sx][$sy];
		$mFlag |= 2;
		$mSea = 0;
		# ログ出力
		if($mHp < 1) {
			logMonsSeaMineDestroy($id, $name, $lName, $point, $mName, $mId);
		} else {
			logMonsSeaMineDamage($id, $name, $lName, $point, $mName, $mId);
		}
	} elsif($l == $HlandComplex) {
		# 複合地形なら設定地形
		my $cKind = (landUnpack($lv))[1];
		my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
		if($cFlag) { # 海系
			$mFlag |= 2;
			$mSea = $HcomplexAfter[$cKind]->{'move'}[1];
			logMonsBreakSea($id, $name, $lName, $point, $mName, $mId);
		} else { # 陸系
			$mFlag &= ~2;
			$mSea = 0;
			logMonsMove($id, $name, $lName, $point, $mName, $mId);
		}
		$island->{'complex'}[$cKind]--;
	} elsif($l == $HlandHugeMonster) {
		($mSea, $mFlag) = (monsterUnpack($lv))[2, 4];
	} else {
		# 陸地を移動
		$mFlag &= ~2;
		$mSea = 0;
		logMonsMove($id, $name, $lName, $point, $mName, $mId) if(!$huge || ($HhugeMonsterImage[$mKind][$dm] eq ''));
	}

	if($mHp < 1) {
		# 移動時に機雷で殺傷
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
			# 行による位置調整
			$ssx-- if(!($ssy % 2) && ($sy % 2));
			$ssx = $correctX[$ssx + $#an];
			$ssy = $correctY[$ssy + $#an];
			# 範囲外
			next if(($ssx < 0) || ($ssy < 0));

			# 移動先の地形によりメッセージ
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
				# 海を移動
				$mFlag2 |= 2;
				$mSea2 = $lv2;
				logMonsMoveSea($id, $name, $lName2, $point2, $mName, $mId) if($i == $dm);
			} elsif (($l2 == $HlandSbase) || ($l2 == $HlandOil) || ($l2 == $HlandBouha)) {
				# 海の施設を破壊
				$mFlag2 |= 2;
				$mSea2 = 0;
				if($l2 == $HlandBouha) {
					$mSea2 = 1;
					$island->{'bouha'}--;
				}
				logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
			} elsif ($l2 == $HlandNavy) {
				# 海軍
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				if ($nHp > 1) {
					# 耐久力を減らす
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
							# サバイバル
							$Hislands[$n]->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
						}
						$HnavyAttackTarget{"$id,$ssx,$ssy"} = undef;
					}
					logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
					# サバイバル
				}
			} elsif ($l2 == $HlandSeaMine) {
				# 機雷なら生命力減少
				$mHp2 -= $lv2;
				$mFlag2 |= 2;
				$mSea2 = 0;
				# ログ出力
				if($mHp2 < 1) {
					logMonsSeaMineDestroy($id, $name, $lName2, $point2, $mName, $mId);
				} else {
					logMonsSeaMineDamage($id, $name, $lName2, $point2, $mName, $mId);
				}
			} elsif($l2 == $HlandComplex) {
				# 複合地形なら設定地形
				my $cKind = (landUnpack($lv2))[1];
				my $cFlag = $HcomplexAfter[$cKind]->{'move'}[0];
				if($cFlag) { # 海系
					$mFlag2 |= 2;
					$mSea2 = $HcomplexAfter[$cKind]->{'move'}[1];
					logMonsBreakSea($id, $name, $lName2, $point2, $mName, $mId);
				} else { # 陸系
					$mFlag2 &= ~2;
					$mSea2 = 0;
					logMonsMove($id, $name, $lName2, $point2, $mName, $mId);
				}
				$island->{'complex'}[$cKind]--;
#			} elsif($land->[$ssx][$ssy] == $HlandHugeMonster) {
#				($mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[2, 4];
			} elsif (($l2 == $HlandDefence) && $HdBaseAuto) {
				# 防衛施設を踏んだ
				$dflag = 1;
				last;
			} else {
				# 陸地を移動
				$mFlag2 &= ~2;
				$mSea2 = 0;
				logMonsMove($id, $name, $lName2, $point2, $mName, $mId) if(($l2 != $HlandWaste) || ($i == $dm));
			}
			next if($navyFlag);
			if($mHp2 < 1) {
				# 機雷で体の一部が消える
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = $mSea2;
			} else {
				$land->[$ssx][$ssy] = $HlandHugeMonster;
				$landValue->[$ssx][$ssy] = monsterPack($mId, $i, $mSea2, $mExp, $mFlag2, $mKind, $mHp2);
#				undef $HlandMove[$id][$ssx][$ssy];
			}
		}
	}

	# 移動済みフラグ
	if ($special & 0x2) {
		# とても速い怪獣
		# 移動済みフラグは立てない
	} elsif ($special & 0x1) {
		# 速い怪獣
		$HmonsterMove[$id][$sx][$sy] = $HmonsterMove[$id][$x][$y] + 1;
	} else {
		# 普通の怪獣
		$HmonsterMove[$id][$sx][$sy] = 2;
	}
#	undef $HlandMove[$id][$sx][$sy];

	if ((($l == $HlandDefence) || ($dflag)) && $HdBaseAuto) {
		($lName, $point, $sx, $sy) = ($lName2, $point2, $ssx, $ssy) if($dflag);
		# 防衛施設を踏んだ
		# 広域被害ルーチン
		wideDamage($id, $name, $island, $sx, $sy);
		logMonsMoveDefence($id, $name, $lName, $point, $mName, $mId);
		$island->{'dbase'}--;
	}
	return 1;
}

# 海軍の補給処理
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

		# 海軍を探す
		next unless ($land->[$x][$y] == $HlandNavy);

		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my $special = $HnavySpecial[$nKind];
		my $tn = $HidToNumber{$nId};

                # 建造中だったら補給しない
                if($nFlag == 3){
                    next;
                }

                # 離陸準備進める
                if($wait > 0){
                    $wait--;
                }

		if (defined $tn) {
			# 存在する島の艦艇なら
			my $tIsland = $Hislands[$tn];
			$flag = 0;
			# 資金を消費する
			my $mflag = $tIsland->{'itemAbility'}[14];
			my $nMoney = int($HnavyMoney[$nKind] * $mflag); # 維持費
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
			# 食料を消費する
			my $fflag = $tIsland->{'itemAbility'}[13];
			my $nFood = int($HnavyFood[$nKind] * $fflag); # 維持食料
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

				# $HnavySupplyFlagが0のときは、自島or友好国の艦隊なら or
				# 周囲($HnavySupplyRangeで設定)に自島or友好国に設定してくれている島の補給艦(特殊能力)がいたら、回復量にプラスする
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
					# 十分に補給できた

					# 最大体力を求め、耐久力を回復する
					$hp = int($HnavyHP[$nKind] * (120 + $nExp)/120);
					if ($nHp < $hp) {
						# 耐久力 +1
						$nHp += $repair;
						$repairShip{$nId} .= " <B>$HnavyName[$nKind]</B>${HtagName_}${point}${H_tagName}";
					}
                                        if($nHp >= $hp){
                                            $nHp = $hp;
                                        }
                                    }
				} else {
					# 補給できなかった
					$failShip{$nId} .= " <B>$HnavyName[$nKind]</B>${HtagName_}${point}${H_tagName}";
				}
#			}
			($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
		} else {
			if ($nFlag == 1) {
				# 残骸なら破壊率アップ
				$nExp += int(rand(10) + 1); # 1%〜10% 
				if ($nExp >= 100) {
					# 破壊率 100% になると消滅
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				} else {
					($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
				}
			}
		}

		# 攻撃目標を探す
		if(!($special & 0x1000000) && !($nFlag == 1) && ($nStat < 2)) {
			# 残骸以外なら
			searchNavyTarget($island, $x, $y);
		}
	}
	# 補給状況
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

# 海軍の移動・移動操縦
# $tId追加→海軍の移動には使わない(0でよい)
# $preが2以上で「移動操縦」(移動方向$arg = $pre - 2)
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
		# 海軍の移動なら$flagmoveを1にする
		$flagmove = 1;
	} elsif(!$arg) {
		# 移動操縦で待機の場合
		$HnavyMove[$id][$x][$y] = 2;
		return 1;
	}

	# すでに動いた？
	return if ($HnavyMove[$id][$x][$y] == 2);

	# 各要素の取り出し
	my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$x][$y], $landValue2->[$x][$y]);
	my $nn  = $HidToNumber{$nId};
	my($nIsland);
	$nIsland  = $Hislands[$nn] if(defined $nn);
	my $nName = landName($land->[$x][$y], $landValue->[$x][$y]);
	my $special = $HnavySpecial[$nKind];

	# 艦隊移動(派遣・帰還)フラグがたっている場合は，移動しない
#	return if($nIsland->{'NavyMove_flag'}[$nNo]);

	if($flagmove) {
		# 海軍の移動の場合
		if($pre) {
			# 先行移動
			if(!($special & 0x10)) {
				# 能力がない
				return;
			} elsif(defined $nn) {
				# 能力があり所属島がある
				# コマンドチェック(移動操縦をするか)
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
			# 先行移動でないのに能力がある
			return;
		}
	} else {
		# 移動操縦の場合
		return if($nId != $tId); # 自島の艦艇？
		return if (!($special & 0x80) && !$HnavyNoMove[$nKind]); # 能力がない
	}

	# 残骸？
	return if ($nFlag == 1);

	# 潜水状態を変更
	if ($special & 0x4) {
		if (random(100) < $HsubmarineSurface[$nKind]) { # 浮上確率:20%
			# 浮上
			$nFlag = 0;
		} else {
			# 潜水
			$nFlag = 2;
		}
		($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
	}

	# 海上採掘基地
	if ($special & 0x200000) {
            my $i;
            for($i = 1; $i <= 6; $i++){
                my $sx = $x + $ax[$i];
                my $sy = $y + $ay[$i];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
                if(($land->[$sx][$sy] == $HlandResource) &&
		   ($Resource[$id][$sx][$sy] != 1)){
                    my ($rTmp, $rKind, $rTurn, $rFood, $rMoney) = landUnpack($landValue->[$sx][$sy]);
                    if($rKind == 0){
                        # 海上採掘基地+鉱床の組み合わせ
                        my $arg = int(($rMoney * 20 + 1200) * (random(120) + $nExp) / 240);
                        my $point2 = "($sx, $sy)";
                        $Hislands[$HidToNumber{$nId}]->{'money'} += $arg;
                        $nExp++;
                        if($nExp >= 120){
                            $nExp = 120;
                        }
		        $Resource[$id][$sx][$sy] = 1; # 採取済みフラグ
                        logResourceS($id, $nId, $name, '海上採掘基地', '海底鉱床', $point, $point2, $arg);
                        ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
                        if(!random(300)){
                            $land->[$sx][$sy] = $HlandSea;
                            $landValue->[$sx][$sy] = 0;
                        }
                    }
                }
            }
	}

	# 定置網
	if ($special & 0x400000) {
            my $i;
            for($i = 1; $i <= 6; $i++){
                my $sx = $x + $ax[$i];
                my $sy = $y + $ay[$i];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
                if(($land->[$sx][$sy] == $HlandResource) &&
		   ($Resource[$id][$sx][$sy] != 1)){
                    my ($rTmp, $rKind, $rTurn, $rFood, $rMoney) = landUnpack($landValue->[$sx][$sy]);
                    if($rKind == 1){
                        # 定置網+漁礁の組み合わせ
                        my $arg = int(($rFood * 20 + 1200) * (random(120) + $nExp) / 240 * 10);
                        my $point2 = "($sx, $sy)";
                        $Hislands[$HidToNumber{$nId}]->{'food'} += $arg;
                        $nExp++;
                        if($nExp >= 120){
                            $nExp = 120;
                        }
		        $Resource[$id][$sx][$sy] = 1; # 採取済みフラグ
                        logResourceF($id, $nId, $name, '定置網', '漁礁', $point, $point2, $arg);
                        ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
                        if(!random(300)){
                            $land->[$sx][$sy] = $HlandSea;
                            $landValue->[$sx][$sy] = 0;
                        }
                    }
                }
            }
	}

        # タイタニック
	if ($special & 0x20000) {

	    return if($HnavyMove[$id][$x][$y] == 2);

	    # オーナー情報取得
	    my($nn) = $HidToNumber{$nId};
	    my($nIsland) = $Hislands[$nn];
	    my($nName) = islandName($nIsland);
            my $nNavyComLevel = gainToLevel($nIsland->{'gain'});
	    if($nNavyComLevel< 6) {
                # 経験値足りなかったら何も言わず中止
	        return 0;
	    }

            # 島主情報
           my $navyComLevel = gainToLevel($island->{'gain'});
	    if($navyComLevel< 6) {
                # 経験値足りなかったら何も言わず中止
	        return 0;
	    }

            # 貿易できるんで、彼我のレート確認
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

            # 貿易量算出
            my $value = int(3000 + 3000 * ($nExp /120));

            if($nFoodrate < $foodrate){
                # (船主から見て)相手のレートが高い場合は輸出
		$nIsland->{'food'} -= $value;
		$island->{'food'} += $value;
		$nIsland->{'money'} += int($value * $foodrate / 100);
		$island->{'money'} -= int($value * $foodrate / 100);
                $nExp++;
                logTrade($id, $nId, $name, $nName, $value, int($value * $foodrate / 100), '輸出', $point);
            }elsif($nFoodrate > $foodrate){
                # 輸入
		$nIsland->{'food'} += $value;
		$island->{'food'} -= $value;
		$nIsland->{'money'} -= int($value * $foodrate / 100);
		$island->{'money'} += int($value * $foodrate / 100);
                $nExp++;
                logTrade($id, $nId, $name, $nName, $value, int($value * $foodrate / 100), '輸入', $point);
            }else{
                # 同じだったんで貿易無し
            }
	    $HnavyMove[$id][$x][$y] = 2;
            if($nExp > 120){
                $nExp = 120;
            }

            ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
	}

	# 攻撃目標を探す（目標補正能力）
	if(($special & 0x1000000) && !$HnavyMoveCount[$id][$x][$y] && !($nFlag == 1) && ($nStat < 2)) {
		# 残骸以外なら
		searchNavyTarget($island, $x, $y);
	}
	# 攻撃予定がある？
	my $target = $HnavyAttackTarget{"$id,$x,$y"};
	if (defined $target) {
		# 攻撃！
		($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyAttack($island, $x, $y, $target->{x}, $target->{y}, $target->{special});
		$HnavyAttackTarget{"$id,$x,$y"} = undef;
	}

	# 残骸？または海(撃沈)？
	return if (($nFlag == 1) || ($land->[$x][$y] == $HlandSea));

	# 港？
	return if ($special & 0x8);

	# 動かない系？
        if ($HnavyNoMove[$nKind]){
            # 移動済みフラグ
	    $HnavyMove[$id][$sx][$sy] = 2;
            return ;
        }
 
        # 帰投ターンすぎてたら帰る
        if(($HnavyCruiseTurn[$nKind] != 0) && ($wait <= 0) && ($nId)) {
	        my $n = $HidToNumber{$nId};
                $Hislands[$n]->{'money'} += $HnavyCost[$nKind];
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = $nSea;
                return;
        }

        # 移動先の指示が今の場所だったら待機に
        if(($goalx == $x) &&
           ($goaly == $y)) {
            $goalx = 31;
            $goaly = 31;
            # 移動済みフラグ
	    $HnavyMove[$id][$sx][$sy] = 2;
        }

        # 操縦可能にも関わらず移動指示が無く、手動操縦でもない
        if(($special & 0x80) && ($goalx == 31) && ($goaly == 31) && ($flagmove)) {
            ($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, 31, 31);
#logdebug ($id, "code2($x, $y)");
            return;
        }

	# 自島の機雷でダメージを受けるかどうか
	my(%amityFlag);
	if($HmineSelfDamage) {
		$amityFlag{$id} = 1;
		if($HmineSelfDamage == 2) {
			foreach (@{$island->{'amity'}}) {
				$amityFlag{$_} = 1;
			}
		}
	}

	# 艦艇の友好国設定を確認
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
	# 動く方向を決定
	if($flagmove) { # 海軍の移動
		my $mvotherisl = 0;
		my(@dir, $d);
		#if($HoceanMode && (defined $nn) && (defined $nIsland->{'move'}[$nNo])) {
		if($special & 0x80) {
			#my($tx, $ty) = split(/,/, $nIsland->{'move'}[$nNo]);
                        my $tx = $goalx;
                        my $ty = $goaly;

			# 移動方向を計算する
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
			# 蹂躙移動（自分の属する艦隊の旗艦を目指して移動）
			# 周囲を見回す
			if ($d = searchTarget($id, $island, $x, $y, $an[$HnavyTowardRange[$nKind]], $HlandNavy)) {
				# 旗艦が見つかった
				push(@dir, $d);
			}
		}
		for ($i = $#dir; $i < 3; $i++) {
			push(@dir, random(6) + 1);
		}

		$mvotherisl = (!(defined $nn)); # 所属不明は自由に動ける
		while ($d = shift @dir) {
			$sx = $x + $ax[$d];
			$sy = $y + $ay[$d];
                        $point = "($sx, $sy)";
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# 範囲外
			next if(($sx < 0) || ($sy < 0));
			if($HoceanMode) {
				# 未知の海域へは移動できない
				next if(!$HlandID[$sx][$sy]);
				if($HlandID[$sx][$sy] != $id) {
					# 移動指令がないか，所属不明でなければ，勝手に動けるのは同じ島の中
					next if(!$mvotherisl);
					# 設定のある時，バトルフィールドなら勝手に動けるのは同じ島の中
					next if($HfieldNavy && $island->{'field'});
					# 設定のある時，バトルフィールドへは入れない
					next if($HfieldUnconnect && ($Hislands[$HisToNumber{$HlandID[$sx][$sy]}]->{'field'} || $island->{'field'}));
				}
			}
			my($l)  = $land->[$sx][$sy];
			my($lv) = $landValue->[$sx][$sy];
			my($lv2) = $landValue2->[$sx][$sy];
			# 深い海、機雷以外なら移動できない
			my($tId, $tTmp, $tStat, $tSea, $tExp, $tFlag, $tNo, $tKind, $tWait, $tHp, $tgoalx, $tgoaly) = navyUnpack($lv, $lv2) if($l == $HlandNavy);
			# unlessの中に移動できる地形を記述
			next unless (
				(($l == $HlandSea) && (!$lv || $HnavyMoveAsase)) || # 海
				(($l == $HlandSeaMine) && !$amityFlag{$nId}) ||     # 機雷
				(($l == $HlandNavy) && # 海軍で
					(($HsuicideAbility || !$nId) && ($special & 0x2000000) && !$nAmityFlag{$tId}) # 体当たり
				) ||
				(($l == $HlandWaste) && ($special & 0x80000)) # 掘削
			);

			# 移動できたんで、軍艦の座礁判定
                        if(($l == $HlandSea) && ($lv == 1) && ($HnavyBuildTurn[$nKind] != 0)){
                            if(random(10) == 0){ # 座礁の確率
                                # 座礁したら初期HPの3割のダメージを受ける
                                $nHp -= int($HnavyHP[$nKind] * 0.3);
                            }
                        }
			last;
		}

		# 移動できなかった？
		return unless (defined $d);

	} else { # 移動操縦
		$arg %= 7;
		$sx = $x + $ax[$arg];
		$sy = $y + $ay[$arg];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		# 範囲外判定
		if(($sx < 0) || ($sy < 0)) {
			$HnavyMove[$id][$x][$y] = 2;
			return;
		}
		if($HoceanMode && ($HlandID[$sx][$sy] != $id)) {
			# 自島でない場合
			my $mn = $HidToNumber{$HlandID[$sx][$sy]};
			my $comName = $HcomName[$HcomMoveTarget];
			my $mflag = 0;
			if(defined $mn) {
				my $tIsland = $Hislands[$mn];
				if (
					($HarmisticeTurn && ($HislandTurn <= $HarmisticeTurn)) ||
					($HsurvivalTurn && ($HislandTurn <= $HsurvivalTurn))
					) {
					# 攻撃が許可されていない
					logNotAvail($nId, $name, $comName);
					$mflag = 1;
				} elsif (($HislandTurn - $nIsland->{'birthday'} <= $HdevelopTurn) ||
					($HislandTurn - $tIsland->{'birthday'} <= $HdevelopTurn)) {
					logDevelopTurnFail($nId, $name, $comName);
					$mflag = 1;
				} elsif(!$HforgivenAttack && $tIsland->{'predelete'}) {
					logLandNG($nId, $name, $comName, '現在【管理人あずかり】のため');
					$mflag = 1;
				} elsif($HfieldUnconnect && $tIsland->{'field'}) {
					logLandNG($nId, $name, $comName, '海域が接続していない');
					$mflag = 1;
				} elsif($HnofleetNotAvail && !$tIsland->{'field'} && !$tIsland->{'ships'}[4]) {
					logLandNG($nId, $name, $comName, "艦隊を保有しない$AfterNameであったため");
					$mflag = 1;
				} elsif($Htournament) {
					if($HislandFightMode < 2) {
						logLandNG($nId, $name, $comName, '現在開発期間中のため');
						$mflag = 1;
					} elsif($nIsland->{'fight_id'} != $tIsland->{'id'}) {
						# 対戦相手じゃない場合は中止
						logLandNG($nId, $name, $comName, '目標が対戦相手でないため');
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
							logLandNG($nId, $name, $comName, '宣戦布告をしていないため');
							$mflag = 1;
						} elsif(($warflag == 1) && ($HuseDeWar == 3)) {
							logLandNG($nId, $name, $comName, '猶予期間中のため');
							$mflag = 1;
						}
					}
				} elsif($tIsland->{'event'}[0]) {
					my $level = 2 ** gainToLevel($island->{'gain'});
					if(($tIsland->{'event'}[1] - $HnoticeTurn < $HislandTurn) && ($HislandTurn < $tIsland->{'event'}[1])) {
						logLandNG($nId, $name, $comName, '現在イベント準備期間中のため');
						$mflag = 1;
					} elsif($tIsland->{'event'}[3] && ($tIsland->{'event'}[3] <= $nIsland->{"invade$tIsland->{'id'}"})) {
						logLandNG($nId, $name, $comName, '派遣可能艦艇数を超えるため');
						$mflag = 1;
					} elsif($HmaxComNavyLevel && !($tIsland->{'event'}[5] & (2 ** gainToLevel($nIsland->{'gain'})))) {
						logLandNG($nId, $name, $comName, '派遣可能レベルでないため');
						$mflag = 1;
					} elsif((!$tIsland->{'event'}[11]) && ($HislandTurn > $tIsland->{'event'}[1])) {
						# 追加派遣を許可しない
						logLandNG($nId, $name, $comName, 'イベント開催中のため');
						$mflag = 1;
					}
				} elsif($nIsland->{'NavyAttack_flag'}[$nNo]) {
					# コマンドを許可しない
					logLandNG($nId, $name, $comName, '戦闘状態にあるため');
					$mflag = 1;
				}
			} else {
				# 島のない海域へは動けない
				logLandNG($nId, $name, $comName, '未知の海域であるため');
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
		# unlessの中に移動できる地形を記述
		unless (
			($l == $HlandSea) || # 海
			(($l == $HlandSeaMine) && !$amityFlag{$nId}) ||     # 機雷
			(($l == $HlandNavy) &&  # 海軍で
				(($special & 0x2000000) && !$nAmityFlag{$tId}) # 体当たり
			) ||
			(($l == $HlandWaste) && ($special & 0x80000)) # 掘削
		) {
			$HnavyMove[$id][$x][$y] = 2;
			return;
		}

		# 移動先の地形によりメッセージ(移動操縦時)
		my($lName) = landName($l, $lv);
		my($point) = "($sx, $sy)";
#		logNavyMoveSea($id, $name, $lName, $point, $nName, $nId) if($land->[$sx][$sy] != $HlandWaste && $land->[$sx][$sy] != $HlandNavy);
	}

	if($land->[$sx][$sy] == $HlandWaste) {
		logNavyMoveDestroy($id, $name, landName($land->[$sx][$sy], $landValue->[$sx][$sy]), "($sx, $sy)", $nName, $nId, $landValue->[$sx][$sy]);
		if(!$landValue->[$sx][$sy]) {
			# 移動しない
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
	# 移動先の地形によりメッセージ
#	my($l)	 = $land->[$sx][$sy];
#	my($lv)	= $landValue->[$sx][$sy];
#	my($lName) = landName($l, $lv);
#	my($point) = "($sx, $sy)";

	$land->[$x][$y] = $HlandSea;
	$landValue->[$x][$y] = $nSea;
	$landValue2->[$x][$y] = 0;
	$HlandMove[$id][$x][$y] = 1;
	# 移動
# 移動ログは鬱陶しいのでコメントにしました
#	logNavyMoveSea($id, $name, $lName, $point, $nName, $nId);
#logdebug ($id, "code3($x, $y)");
	# 海底探査能力
	if ($special & 0x100000) {
		my(@x, @y);
		if($HedgeReclaim) {
			my($map) = $island->{'map'};
			@x = @{$map->{'x'}};
			@y = @{$map->{'y'}};
		}
		if (random(1000) < $Hoilp[$nKind]) { # 確率0.2%
			# 油田発見！
			$land->[$x][$y] = $HlandOil;
			$landValue->[$x][$y] = 0;
			my $str = $Hoilp[$nKind] * $HcomCost[$HcomDestroy];
			logOilFound($id, $name, "($x, $y)", "海底探査", "$str$HunitMoney");
		} elsif(random(2000) < $Hoilp[$nKind]) { # 確率0.1%(油田発見確率の0.5倍)
			# 財宝発見！
			my $value = ($Hoilp[$nKind] * $HcomCost[$HcomDestroy]); # 元金保証(^^ゞ
			$value += random(10 * $Hoilp[$nKind] * $HcomCost[$HcomDestroy]); # 運命のルーレット(^人^)
			if(defined $nn) {
				$nIsland->{'money'} += $value ;
				logTansaku($id, $name, $nId, $nName, "($x, $y)", "$value$HunitMoney");
			}
		} elsif((random(4000) < $Hoilp[$nKind]) && (!$HedgeReclaim ||
			($HedgeReclaim && !(($x < $HedgeReclaim) || ($x > $x[$#x] - $HedgeReclaim) || ($y < $HedgeReclaim) || ($y > $y[$#y] - $HedgeReclaim))) # 島の最外周を埋め立て不可にする場合
			)) { # 確率0.05%(油田発見確率の0.25倍)
			# 海底火山噴火
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
				# サバイバル
				$nIsland->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
			}

			foreach $i (1..6) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				# 行による位置調整
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];
				# 範囲外
				next if(($sx < 0) || ($sy < 0));

				# 範囲内の場合
				$landKind = $land->[$sx][$sy];
				$lv = $landValue->[$sx][$sy];
				$lv2 = $landValue2->[$sx][$sy];
				$point = "($sx, $sy)";
				if(($landKind == $HlandSea) || ($landKind == $HlandOil)) {
					# 海、油田の場合
					if(!$lv || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
						logEruptionSea($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandSea;
						$landValue->[$sx][$sy] = 1;
						next;
					} else {
						# 浅瀬
						logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					}
				} elsif(($landKind == $HlandSeaMine) || ($landKind == $HlandSbase) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
					# 機雷、海基，海底コアの場合
					logEruptionSea($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandSea;
					$landValue->[$sx][$sy] = 1;
					next;
				} elsif(($landKind == $HlandMountain) || ($landKind == $HlandWaste)) {
					next;
				} elsif($landKind == $HlandComplex) {
					# 複合地形なら設定地形
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
						# 港は陸地
						logEruptionSea1($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandWaste;
						$landValue->[$sx][$sy] = 0;
						$Hislands[$n]->{'navyPort'}-- if(defined $n);
					} else {
						if(!$nSea || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
							# その他は浅瀬
							logEruptionSea($id, $name, landName($landKind, $lv), $point);
							$land->[$sx][$sy] = $HlandSea;
							$landValue->[$sx][$sy] = 1;
						} else {
							# 浅瀬は陸地
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
					# それ以外の場合
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
	# 機雷なら耐久力減少
		$nHp -= $landValue->[$sx][$sy];
		# ログ出力
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
		# 海賊能力
		if ((defined $nn) && ($special & 0x40000) && ($id != $nId)) {
			my($i, $j, $ssx, $ssy);
			my $nPoint = "($sx, $sy)";
			for($j = 0; $j < $HpiratesHex[$nKind]; $j++) {
				for($i = $an[$j]; $i < $an[$j+1]; $i++) {
					$ssx = $sx + $ax[$i];
					$ssy = $sy + $ay[$i];
					# 行による位置調整
					$ssx-- if(!($ssy % 2) && ($sy % 2));
					$ssx = $correctX[$ssx + $#an];
					$ssy = $correctY[$ssy + $#an];
					# 範囲外
					next if(($ssx < 0) || ($ssy < 0));

					my($landKind, $lv, $point, $value);
					$landKind = $land->[$ssx][$ssy];
					$lv = $landValue->[$ssx][$ssy];
					$lv2 = $landValue2->[$ssx][$ssy];
					$point = "($ssx, $ssy)";

					# 範囲内の場合
					if($landKind == $HlandFarm) {
						$value = int($lv * 10 / 2); # 規模の半分の食料
						next if(random(100) >= 50 - ($j * 20)); # 1Hex内50%,2Hex30%,3Hex10%
						$nIsland->{'food'} += $value;
						$island->{'food'} -= $value;
						logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagFood_}$value$HunitFood${H_tagFood}");
					} elsif($landKind == $HlandFactory) {
						$value = int($lv / 2); # 規模の半分の資金
						next if(random(100) >= 50 - ($j * 20)); # 1Hex内50%,2Hex30%,3Hex10%
						$nIsland->{'money'} += $value;
						$island->{'money'} -= $value;
						logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagMoney_}$value$HunitMoney${H_tagMoney}");
					} elsif($landKind == $HlandComplex) {
						my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
						if($cFood && (random(100) >= 50 - ($j * 20))) { # 1Hex内50%,2Hex30%,3Hex10%
							my $food = $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
							$food  = int($food / 2); # 規模の半分の食料
							$nIsland->{'food'} += $food;
							$island->{'food'} -= $food;
							logPirates($id, $name, $point, $nId, $nName, $nPoint, "${HtagFood_}$food$HunitFood${H_tagFood}");
						} elsif($cMoney && (random(100) >= 50 - ($j * 20))) { # 1Hex内50%,2Hex30%,3Hex10%
							my $money = $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
							$money = int($money / 2); # 規模の半分の資金
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
	# 残骸になる
		$land->[$sx][$sy] = $HlandNavy;
		($landValue->[$sx][$sy], $landValue2->[$sx][$sy]) = navyPack(0, $nTmp, $nStat, $nSea, int(rand(90)) + 10, 1, 0, $nKind, 0, 0, 31, 31);
		if(defined $nn) {
			$nIsland->{'shipk'}[$nKind]--;
			$nIsland->{'ships'}[$nNo]--;
			$nIsland->{'ships'}[4]--;
		}
	} else {
	# 沈没
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = $nSea;
		$HlandMove[$id][$sx][$sy] = 1;
		$HnavyAttackTarget{"$id,$sx,$sy"} = undef;
		if(defined $nn) {
			$nIsland->{'shipk'}[$nKind]--;
			$nIsland->{'ships'}[$nNo]--;
			$nIsland->{'ships'}[4]--;
			# サバイバル
			$nIsland->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
		}
	}

	# 移動済みフラグ
	if ($special & 0x2) {
		# とても速い移動
		# 移動済みフラグは立てない
	} elsif ($special & 0x1) {
		# 速い移動
		$HnavyMove[$id][$sx][$sy] = $HnavyMove[$id][$x][$y] + 1;
	} else {
		# 普通の移動
		$HnavyMove[$id][$sx][$sy] = 2;
	}
	$HnavyMoveCount[$id][$sx][$sy] = 1;
#	undef $HlandMove[$id][$sx][$sy];
	return 1;
}

# 最短距離にある目標地形の方向を計算する
sub searchTarget {
	my($id, $island, $x, $y, $range, @kind) = @_;

	# 範囲内の目標地形を探す
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外
		next if(($sx < 0) || ($sy < 0));

		# 範囲内の場合
		if ($kflag{$land->[$sx][$sy]}) {
			if($id != 0){
				# 各要素の取り出し
				my($nId, $nNo, $nKind) = (navyUnpack($landValue->[$x][$y], 0))[0, 6, 7];
				my $special = $HnavySpecial[$nKind];

				# 自島の艦艇？
				next if($nId != $id);

				# 旗艦じゃない？
				next if(!($special & 0x80));
			}
			$tx = $sx;
			$ty = $sy;
			last;
		}
	}

	# 移動方向を計算する
	my $dy = ($ty > $y) ? 2 : ($ty < $y) ? 0 : 1;

	if ($tx < $x) {
		return (6, 5, 4)[$dy];
	} elsif ($tx > $x) {
		return (1, 2, 3)[$dy];
	} else {
		return ((rand(1) < .5 ? 1 : 6), 0, (rand(1) < .5 ? 3 : 4))[$dy];
	}
}

# 海軍の攻撃目標を探す
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
		# 一斉攻撃準備
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

	# 範囲内の目標地形を探す
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外
		next if(($sx < 0) || ($sy < 0));

		# 範囲内の場合
		$tKind = $land->[$sx][$sy];
		$tLv   = $landValue->[$sx][$sy];
		$tLv2  = $landValue2->[$sx][$sy];

		my $target = { 'x' => $sx, 'y' => $sy };

		next if(($tKind != $HlandMonster) && ($tKind != $HlandHugeMonster) && ($nStat > 1));

                # カメと投網は怪獣しかターゲットにできない
                if(($HvsMonster[$nKind] == 1) && ($tKind != $HlandMonster)){
                    next;
                }

                # 宣戦布告してなかったら、民間船は対象外
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
			# 対潜攻撃
			$target->{special} = 0x100;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# 一斉攻撃可能
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# 海軍
				($tId, $nFlag) = (navyUnpack($tLv,0))[0, 5];
				# 友好国
				if(!$amityFlag{$tId}) {
					# 味方の艦艇ではない
					if ($nFlag == 2) {
						# 潜水してる
						# 攻撃目標設定
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # コア
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					if(int($tLv / 10000) >= 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif (($tKind == $HlandSbase) || # 海底基地
					($tKind == $HlandOil)) {   # 海底油田
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					$targetTmp{($tKind == $HlandSbase ? 'Arm' : 'Money')} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) { # 複合地形
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x100) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# 怪獣
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# 友好国
				if(!$amityFlag{$tId}) {
					# 味方の派遣怪獣ではない
					if ($nFlag & 2) {
						# 海にいるか
						# 攻撃目標設定
						$targetTmp{($tKind == $HlandMonster ? 'Monster' : 'HugeMonster')} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x200) {
			# 対艦攻撃
			$target->{special} = 0x200;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# 一斉攻撃可能
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# 海軍
				($tId, $nFlag, $nKind) = (navyUnpack($tLv,0))[0, 5, 7];
				# 友好国
				if(!$amityFlag{$tId}) {
					# 味方の艦艇ではない
					if (($nFlag != 2) && !$HnavyCruiseTurn[$nKind]) {
						# 潜水ではなく、航空機でもない
						# 攻撃目標設定
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # コア
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					if(int($tLv / 10000) == 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandOil) { # 海底油田
				# 友好国
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					$targetTmp{'Money'} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) {
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x200) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif ($tKind == $HlandHugeMonster) {
				# 巨大怪獣
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# 友好国
				if(!$amityFlag{$tId}) {
					if ($nFlag & 2) {
						# 海にいるか
						# 攻撃目標設定
						$targetTmp{'HugeMonster'} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x400) {
			# 対地攻撃
			$target->{special} = 0x400;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# 一斉攻撃可能
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if (($tKind == $HlandTown)     || # 町系
				($tKind == $HlandForest)   || # 森
				($tKind == $HlandFarm)     || # 農場
				($tKind == $HlandFactory)  || # 工場
				($tKind == $HlandComplex)  || # 複合地形
				($tKind == $HlandBase)     || # ミサイル基地
				($tKind == $HlandDefence)  || # 防衛施設
				($tKind == $HlandMonument) || # 記念碑
				($tKind == $HlandHaribote)) { # ハリボテ
				# 友好国
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
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
			} elsif ($tKind == $HlandCore) { # コア
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					if(!(int($tLv / 10000))) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif (($tKind == $HlandMonster) || ($tKind == $HlandHugeMonster)) {
				# 怪獣
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# 友好国
				if(!$amityFlag{$tId}) {
					# 陸にいるか？
					unless ($nFlag & 2) {
						# 攻撃目標設定
						$targetTmp{($tKind == $HlandMonster ? 'Monster' : 'HugeMonster')} = $target;
						next;
					}
				}
			}
		}

		if ($nSpecial & 0x800) {
			# 対空攻撃
			$target->{special} = 0x800;
			if($mission{"$sx,$sy"} && (!$missionflag || ($missionflag > $mission{"$sx,$sy"}))) {
				# 一斉攻撃可能
				$targetTmp{'Mission'} = $target;
				$missionflag = $mission{"$sx,$sy"};
			}
			if ($tKind == $HlandNavy) {
				# 海軍
				($tId, $nFlag, $nKind) = (navyUnpack($tLv,0))[0, 5, 7];
				# 友好国
				if(!$amityFlag{$tId}) {
					# 味方の艦艇ではない
					if ($HnavyCruiseTurn[$nKind]) {
						# 航空機のみ
						# 攻撃目標設定
						$targetTmp{'Navy'} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandCore) { # コア
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					if(int($tLv / 10000) == 1) {
						$targetTmp{($HcoreHide ? 'Other' : 'Arm')} = $target;
						next;
					}
				}
			} elsif ($tKind == $HlandOil) { # 海底油田
				# 友好国
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					# 攻撃目標設定
					$targetTmp{'Money'} = $target;
					next;
				}
			} elsif($tKind == $HlandComplex) {
				if(!$amityFlag{$id}) {
					# 味方の施設ではない
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($tLv);
					if($HcomplexAttr[$cKind] & 0x200) {
						$targetTmp{'Food'}  = $target if($HcomplexFPplus[$cKind] * $HcomplexFPCmax[$cKind] + $HcomplexFPbase[$cKind]);
						$targetTmp{'Money'} = $target if($HcomplexMPplus[$cKind] * $HcomplexMPCmax[$cKind] + $HcomplexMPbase[$cKind]);
						next;
					}
				}
			} elsif ($tKind == $HlandHugeMonster) {
				# 巨大怪獣
				($tId, $nFlag) = (monsterUnpack($tLv))[0, 4];
				# 友好国
				if(!$amityFlag{$tId}) {
					if ($nFlag & 2) {
						# 海にいるか
						# 攻撃目標設定
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

# 海軍の攻撃
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
	# 難民の数
	my($boat) = 0;

	# 兵器選択
	my @arms;
	my $n;
	if ($tSpecial & 0x100) {
		# 対潜攻撃
		$n = 0x1000;
	} elsif ($tSpecial & 0x200) {
		# 対艦攻撃
		push(@arms, 0x1000) if ($nSpecial & 0x1000);
		push(@arms, 0x2000) if ($nSpecial & 0x2000);
		push(@arms, 0x4000) if ($nSpecial & 0x4000);
		$n = $arms[int(rand($#arms + 1))];
	} elsif ($tSpecial & 0x400) {
		# 対地攻撃
		push(@arms, 0x2000) if ($nSpecial & 0x2000);
		push(@arms, 0x4000) if ($nSpecial & 0x4000);
		$n = $arms[int(rand($#arms + 1))];
	}

	# 攻撃誤差
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
	# 攻撃回数
	my $nFire = $HnavyFire[$nKind];
	my $fflag = ((defined $nn) && (!$HitemInvalid || !$island->{'field'})) ? $nIsland->{'itemAbility'}[11] : 1;
	$nFire *= $fflag;
	$nFire += $HnavyFireBF[0] if($island->{'field'});
	$nFire = int($nFire);
	$nFire = 1 if($nFire < 1);
	# 破壊力
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
	# 着弾点からの拡散範囲
	my $range = 0;

	# 一斉攻撃
#	if($nIsland->{"missionset,$id,$x,$y"}) {
#HdebugOut("[fire] missionset,$id,$x,$y => mission,$id,$tx,$ty\n");
#		$nIsland->{"mission,$id,$tx,$ty"} .= " <B>$HnavyName[$nKind]</B>${HtagName_}($x, $y)${H_tagName}";
#	}

	# 攻撃する
	my($r, $err, $xx, $yy, $fx, $fy, $fPoint, $fName, $fKind, $fLv, @pointErr, @terrorPnt);
	my(%damageId);
	my $loopflag = 0;
	my $fire = 0;
	while ($fire < $nFire) {
		last if($loopflag); # 費用不足か残骸で攻撃終了

		# 着弾点算出
		if($rpflag && (rand(100) < $rpflag)) {
			$err = $err2;
		} else {
			$err = $err1;
		}
		$r = int(rand($err));
		$xx = $tx + $ax[$r];
		$yy = $ty + $ay[$r];
		# 行による位置調整
		$xx-- if(!($yy % 2) && ($ty % 2));
		$xx = $correctX[$xx + $#an];
		$yy = $correctY[$yy + $#an];
		if(!$HnavySelfAttack && ($xx == $x) && ($yy == $y)) {
			$r += int(1 + rand($err-1));
			$r -= $err if($r >= $err);
			# 行による位置調整
			$xx = $tx + $ax[$r];
			$yy = $ty + $ay[$r];
			$xx-- if(!($yy % 2) && ($ty % 2));
			$xx = $correctX[$xx + $#an];
			$yy = $correctY[$yy + $#an];
		}

		if($nSpecial & 0x20000000) {
			if (($xx < 0) || ($yy < 0)) {
				# 範囲外の場合、絨毯爆撃しない
				$range = 0;
			} else {
				push(@terrorPnt, "($xx, $yy)");
				$range = $an[$HnavyTerrorHex[$nKind]] - 1;
			}
		}
		my(@order) = randomArray($range + 1);
		foreach my $loop (0..$range) {

			($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($landValue->[$x][$y], $landValue2->[$x][$y]);
			# 残骸か海になってたら、攻撃終了(自爆を許す場合、必要)
			#return ($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) if($nHp == 0);
			if($nHp == 0) {
				$loopflag = 1;
				last;
			}

			# 既定攻撃回数終了
			last if($fire >= $nFire);

			# 弾薬費用を引く
			if(defined $nn) {
				$nIsland->{'money'} -= $HnavyShellCost[$nKind];
				if ( ($nIsland->{'money'} < 0) &&
					(($HnavyUnknown && ($nId != 0)) || !$HnavyUnknown) ) {
					# 弾薬費用が足りない
					$nIsland->{'money'} = 0;
					$nIsland->{'shellMoney'} -= $nIsland->{'money'};
					logNavyNoShell($id, $nId, $name, $nPoint, $nName);
					$loopflag = 1;
					last;
				} else {
					$nIsland->{'shellMoney'} += $HnavyShellCost[$nKind];
				}
				$nIsland->{'ext'}[1] += $HnavyShellCost[$nKind]; # 貢献度
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
				$island->{'ext'}[5]++; # 受けたミサイルの数
				next;
			}
			$fKind  = $land->[$fx][$fy];
			$fLv    = $landValue->[$fx][$fy];
			$fLv2   = $landValue2->[$fx][$fy];
			$fName  = landName($fKind, $fLv);

			# 防衛施設判定
			my($defence) = 0;
			my($defflag) = 1;
			# 未判定領域
#			if (($fKind == $HlandDefence) || countAroundComplex($island, $fx, $fy, $an[0], 0x40) ||
#				countAroundNavySpecial($island, $fx, $fy, 0x40, $an[0], 0)) {
#				# 防衛施設に命中
#				if ($fKind == $HlandDefence) { # 防衛施設で
#					if($amityFlag{$id}) { # 無害化
#						if(random(100) < $HnavySafetyInvalidp) {
#							# 一定確率で誤爆
#							push(@pointErr, { 'SS' => $fPoint });
#						} else {
#							push(@pointErr, { 'SZ' => $fPoint });
#							next;
#						}
#					}
#					# 防衛施設の耐久力を下げる
#					$defflag = ($fLv % 100) - $damage;
#					$fLv -= $damage;
#					if($defflag < 0) {
#						$island->{'dbase'}--;
#						$nIsland->{'ext'}[2]++ if(defined $nn); # 破壊した防衛施設の数
#					}
#				}
#			} elsif (countAroundDef($id, $island, $fx, $fy, 0x40, @noDefenceIds)) {
#				# 防衛範囲
#				$defence = 1;
#			}

                        # 防衛判定
                        if (countAroundDef($id, $island, $fx, $fy, 0x40, @noDefenceIds)) {
				# 
				$defence = 1;
			}


			if ($defence) {
				# 防衛された
				if ($n == 0x1000) {
					# 魚雷　（対潜、対艦）
					# 海中は防衛しない
# 防衛したいときはコメントを外すこと
#					push(@pointErr, { 'DF' => $fPoint });
#					$island->{'ext'}[7]++;
#					next;
				} elsif ($n == 0x2000) {
					# 艦砲　（対艦、対地）
					push(@pointErr, { 'DF' => $fPoint });
					$island->{'ext'}[7]++;
					next;
				} elsif ($n == 0x4000) {
					# 艦載機（対艦、対地）
					push(@pointErr, { 'DF' => $fPoint });
					$island->{'ext'}[7]++;
					next;
				}
			}

			# 効果のない地形
			if ($n == 0x1000) {
				# 魚雷　（対潜、対艦）
				if (($fKind == $HlandSea)      || # 海
					($fKind == $HlandWaste)    || # 荒地
					($fKind == $HlandPlains)   || # 平地
					($fKind == $HlandTown)     || # 町系
					($fKind == $HlandForest)   || # 森
					($fKind == $HlandFarm)     || # 農場
					($fKind == $HlandFactory)  || # 工場
					($fKind == $HlandBase)     || # ミサイル基地
					($fKind == $HlandDefence)  || # 防衛施設
					($fKind == $HlandMountain) || # 山
					($fKind == $HlandMonument) || # 記念碑
					($fKind == $HlandHaribote)) { # ハリボテ
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
			} elsif ($n == 0x2000) {
				# 艦砲　（対艦、対地）
				if (($fKind == $HlandSea)      || # 海
					($fKind == $HlandMountain) || # 山
					($fKind == $HlandWaste)    || # 荒地
					($fKind == $HlandSbase)) {    # 海底基地
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}

				if ($fKind == $HlandNavy){ # 海軍
 				    my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
                                    if($HnavyCruiseTurn[$nkind2]){ # 航空機の場合
                                    	push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
                                    }
                                }


			} elsif ($n == 0x4000) {
				# 艦載機（対艦、対地）
				if (($fKind == $HlandSea)      || # 海
					($fKind == $HlandMountain) || # 山
					($fKind == $HlandWaste)    || # 荒地
					($fKind == $HlandSbase)) {    # 海底基地
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}

				if ($fKind == $HlandNavy){ # 海軍
 				    my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
                                    if($HnavyCruiseTurn[$nkind2]){ # 航空機の場合
                                    	push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
                                    }
                                }
			}

			# 海軍，怪獣，巨大怪獣以外の無害化
			if($amityFlag{$id} && $fKind != $HlandNavy && $fKind != $HlandMonster && $fKind != $HlandHugeMonster) {
				if(random(100) < $HnavySafetyInvalidp) {
					# 一定確率で誤爆
					push(@pointErr, { 'SS' => $fPoint });
				} else {
					push(@pointErr, { 'SZ' => $fPoint });
					next;
				}
			}

			# 特別な地形
			if ($fKind == $HlandComplex) {  # 複合地形
				$island->{'ext'}[5]++;
				my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($fLv);
				# 効果のある地形
				if( (defined  $HcomplexAfter[$cKind]->{'attack'}[0]) &&
					( (($n == 0x1000) && ($HcomplexAttr[$cKind] & 0x300)) || # 魚雷　（対潜、対艦）
					(($n == 0x2000) && ($HcomplexAttr[$cKind] & 0x600)) ||   # 艦砲　（対艦、対地）
					(($n == 0x4000) && ($HcomplexAttr[$cKind] & 0x600)) )    # 艦載機（対艦、対地）
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
					# 攻撃後の地形にする
					# 複合地形なら設定地形
					$land->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[0];
					$landValue->[$fx][$fy] = $HcomplexAfter[$cKind]->{'attack'}[1];
					$island->{'complex'}[$cKind]--;
					$HlandMove[$id][$fx][$fy] = 1;

					if ($n == 0x1000) {
						# 魚雷　（対潜、対艦）
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} elsif (($n == 0x2000) || ($n == 0x4000)) {
						# 艦砲　（対艦、対地）艦載機（対艦、対地）
						logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					}
					next;
				}
				# 効果のない地形
				push(@pointErr, { 'ND' => $fPoint });
				next;
			} elsif ($fKind == $HlandMonster) {  # 怪獣
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($fLv);
				my $mName = landName($fKind, $fLv);
				my $mn = $HidToNumber{$mId};
				if(defined $mn) {
					my $mIsland = $Hislands[$mIsland];
					$mIsland->{'ext'}[5]++ if(defined $mIsland);
				}
				# 潜水中？
				if ($mFlag & 2) {
					# 潜水中
					if (($n == 0x2000) || ($n == 0x4000)) {
						# 艦砲　（対艦、対地） 艦載機（対艦、対地）
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				} else {
					# 潜水中でない
					if ($n == 0x1000) {
						# 魚雷　（対潜、対艦）
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				}

				# 硬化中？
				if ($mFlag & 1) {
					# 硬化中
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# 硬化中じゃない
					if($amityFlag{$mId}) { # 無害化
						if(random(100) < $HnavySafetyInvalidp) {
							# 一定確率で誤爆
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
						# 怪獣しとめた
						# 経験値
						$nExp += $HmonsterExp[$mKind];
						$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
						($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
						if(defined $nn) {
							$nIsland->{'gain'} += $HmonsterExp[$mKind];
							if($island->{'event'}[1] <= $HislandTurn) {
								if($island->{'event'}[6] == 2) {
									# 艦艇経験値獲得
									$nIsland->{'epoint'}{$id} += $HmonsterExp[$mKind];
								} elsif($island->{'event'}[6] == 4) {
									# 怪獣退治
									$nIsland->{'epoint'}{$id}++;
								} elsif($island->{'event'}[6] == 5) {
									# 賞金稼ぎ
									$nIsland->{'epoint'}{$id} += $HmonsterValue[$mKind];
								}
							}
						}

						if ($n == 0x1000) {
							# 魚雷　（対潜、対艦）
							if ($mFlag & 2) {
								# 潜水中
								logNavyTorpedoMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
							}
						} elsif (($n == 0x2000) || ($n == 0x4000)) {
							# 艦砲　（対艦、対地）艦載機（対艦、対地）
							logNavyMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						}
						$HlandMove[$id][$fx][$fy] = 1;


						if (defined $nn) {
							# 収入
							my($value) = $HmonsterValue[$mKind];
							if ($value > 0) {
								$nIsland->{'money'} += $value;
								logMonMoney($nId, $mName, $value);
							}
							# 賞関係
							my($prize) = $nIsland->{'prize'};
							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
							$monsters |= (2 ** $mKind);
							$nIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# 怪獣退治数
							$nIsland->{'monsterkill'}++;
							# アイテム獲得判定
							if($HitemRest && $HitemGetDenominator2 && (random($HitemGetDenominator2) < $nIsland->{'gain'})) {
								my $num = @Hitem;
								$num = random($num);
								push(@{$nIsland->{'item'}}, $Hitem[$num]);
								$HitemGetId[$Hitem[$num]]{$nId} = 1;
								$HitemRest--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$Hitem[$num]], "$mNameの体内から");
								splice(@Hitem, $num, 1);
							}
						}

					} else {
						# 怪獣生きてる
						logNavyMonster($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);

						# HPが1減る
						#$landValue->[$fx][$fy] -= $damage;
						$mHp -= $damage;
						if($mHp > 0) {
							$landValue->[$fx][$fy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
							next;
						}
						next;
					}
				}
			} elsif ($fKind == $HlandHugeMonster) {  # 巨大怪獣
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($fLv);
				my $mName = landName($fKind, $fLv);
				my $mn = $HidToNumber{$mId};
				if(defined $mn) {
					my $mIsland = $Hislands[$mIsland];
					$mIsland->{'ext'}[5]++ if(defined $mIsland);
				}
				# 潜水中？
				if ($mFlag & 2) {
					# 潜水中
# 巨大怪獣は海にいても艦砲、艦載機で攻撃可能。不可にする場合はコメントをはずす。
#					if (($n == 0x2000) || ($n == 0x4000)) {
#						# 艦砲　（対艦、対地） 艦載機（対艦、対地）
#						push(@pointErr, { 'MS' => $fPoint });
#						next;
#					}
				} else {
					# 潜水中でない
					if ($n == 0x1000) {
						# 魚雷　（対潜、対艦）
						push(@pointErr, { 'MS' => $fPoint });
						next;
					}
				}

				# 硬化中？
				if ($mFlag & 1) {
					# 硬化中
					push(@pointErr, { 'MH' => $fPoint });
					next;
				} else {
					# 硬化中じゃない
					if($amityFlag{$mId}) { # 無害化
						if(random(100) < $HnavySafetyInvalidp) {
							# 一定確率で誤爆
							push(@pointErr, { 'SS' => $fPoint });
						} else {
							push(@pointErr, { 'SZ' => $fPoint });
							next;
						}
					}
					$damageId{$mId} = 1 if($mId && ($mId != $id) && ($mId != $nId));
					if (($mHp <= $damage) && ($mHflag == 0)) {
						# 怪獣しとめた
						# 巨大怪獣処理
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$mKind][$j] eq '');
							$ssx = $fx + $ax[$j];
							$ssy = $fy + $ay[$j];
							# 行による位置調整
							$ssx-- if(!($ssy % 2) && ($fy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# 範囲外
							next if(($ssx < 0) || ($ssy < 0));

							next if($land->[$ssx][$ssy] != $HlandHugeMonster);
							# 各要素の取り出し
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# コアの周囲が残っている場合攻撃無効
							if($HhugeMonsterSpecial[$mKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							} elsif ($mFlag2 & 2) {
								# 海にいた
								$land->[$ssx][$ssy] = $HlandSea;
								$landValue->[$ssx][$ssy] = $mSea2;
							} else {
								# 陸地にいた
								$land->[$ssx][$ssy] = $HlandWaste;
								$landValue->[$ssx][$ssy] = 0;
							}
							$HlandMove[$id][$ssx][$ssy] = 1;
						}
						next if($deflag);

						# 経験値
						$nExp += $HhugeMonsterExp[$mKind];
						$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
						($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
						if(defined $nn) {
							$nIsland->{'gain'} += $HhugeMonsterExp[$mKind];
							if($island->{'event'}[1] <= $HislandTurn) {
								if($island->{'event'}[6] == 2) {
									# 艦艇経験値獲得
									$nIsland->{'epoint'}{$id} += $HhugeMonsterExp[$mKind];
								} elsif($island->{'event'}[6] == 4) {
									# 怪獣退治
									$nIsland->{'epoint'}{$id}++;
								} elsif($island->{'event'}[6] == 5) {
									# 賞金稼ぎ
									$nIsland->{'epoint'}{$id} += $HhugeMonsterValue[$mKind];
								}
							}
						}

						if ($n == 0x1000) {
							# 魚雷　（対潜、対艦）
							if ($mFlag & 2) {
								# 潜水中
								logNavyTorpedoMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
							}
						} elsif (($n == 0x2000) || ($n == 0x4000)) {
							# 艦砲　（対艦、対地）艦載機（対艦、対地）
							logNavyMonKill($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						}
						$HlandMove[$id][$fx][$fy] = 1;


						if (defined $nn) {
							# 収入
							my($value) = $HhugeMonsterValue[$mKind];
							if ($value > 0) {
								$nIsland->{'money'} += $value;
								logMonMoney($nId, $mName, $value);
							}
							# 賞関係
							my($prize) = $nIsland->{'prize'};
							$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
							my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
							$hmonsters |= (2 ** $mKind);
							$nIsland->{'prize'} = "$flags,$monsters,$hmonsters,$turns";
							# 怪獣退治数
							$nIsland->{'monsterkill'}++;
							# アイテム獲得判定
							if($HitemRest && $HitemGetDenominator && (random($HitemGetDenominator) < $nIsland->{'gain'})) {
								my $num = @Hitem;
								$num = random($num);
								push(@{$nIsland->{'item'}}, $Hitem[$num]);
								$HitemGetId[$Hitem[$num]]{$nId} = 1;
								$HitemRest--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$Hitem[$num]], "$mNameの体内から");
								splice(@Hitem, $num, 1);
							}
						}

					} else {
						# 怪獣生きてる
						my($j, $ssx, $ssy);
						my $deflag = 0;
						foreach $j (1..6) {
							next if($HhugeMonsterImage[$mKind][$j] eq '');
							$ssx = $fx + $ax[$j];
							$ssy = $fy + $ay[$j];
							# 行による位置調整
							$ssx-- if(!($ssy % 2) && ($fy % 2));
							$ssx = $correctX[$ssx + $#an];
							$ssy = $correctY[$ssy + $#an];
							# 範囲外
							next if(($ssx < 0) || ($ssy < 0));

							next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
							# 各要素の取り出し
							my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
							next if($mHflag2 != $j);
							# コアの周囲が残っている場合攻撃無効
							if($HhugeMonsterSpecial[$mKind] & 0x10000) {
								$deflag = 1;
								push(@pointErr, { 'DF' => $fPoint });
								last;
							}
						}
						next if($deflag);
						# HPが減る
						$mHp -= $damage;
						logNavyMonster($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $mName, $fPoint);
						if($mHp > 0) {
							# 怪獣生きてる
							$landValue->[$fx][$fy] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
							next;
						}
					}
					# 体の一部が消える
					if ($mFlag & 2) {
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
			} elsif ($fKind == $HlandNavy) { # 海軍
				my($nId2, $nTmp2, $nStat2, $nSea2, $nExp2, $nFlag2, $nNo2, $nKind2, $wait2, $nHp2, $goalx2, $goaly2) = navyUnpack($fLv, $fLv2);
				my $nSpecial2 = $HnavySpecial[$nKind2];
				my $nName2 = landName($fKind, $fLv);
				my $nn2 = $HidToNumber{$nId2};
				my($nIsland2);
				$nIsland2 = $Hislands[$nn2] if (defined $nn2);

				if ($nFlag2 == 2) {
					# 潜水中
					if (($n == 0x2000) || ($n == 0x4000)) {
						# 艦砲　（対艦、対地） 艦載機（対艦、対地）
						push(@pointErr, { 'FS' => $fPoint });
						next;
					}
				}

				# 残骸？
				if ($nFlag2 == 1) {
					logNavyWreckDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nName2, $fPoint);

					# 海になる
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = $nSea2;
					$HlandMove[$id][$fx][$fy] = 1;
					next;
				}

				if($amityFlag{$nId2}) { # 無害化
					if(random(100) < $HnavySafetyInvalidp) {
						# 一定確率で誤爆
						push(@pointErr, { 'SS' => $fPoint });
					} else {
						push(@pointErr, { 'SZ' => $fPoint });
						next;
					}
				}

				if(defined $nn2) {
					if ($nId == $nId2) {
						# 味方に撃たれた場合貢献度マイナス(受けたミサイルの数はカウントしない)
						$nIsland2->{'ext'}[1] -= $HnavyShellCost[$nKind]; # 貢献度
						#$nIsland2->{'ext'}[1] = 0 if($nIsland2->{'ext'}[1] < 0);
					} else {
						# 敵に撃たれた場合貢献度プラス
						$nIsland2->{'ext'}[1] += $HnavyShellCost[$nKind]; # 貢献度
						$nIsland2->{'ext'}[5]++;
					}
				}

				$damageId{$nId2} = 1 if($nId2 && ($nId2 != $id) && ($nId2 != $nId));
				if ($nHp2 <= $damage) {
					# 撃沈

					# 経験値
					$nExp += $HnavyExp[$nKind2];
                                        $nExp += int($nExp2 / 2);
					$nExp = $HmaxExpNavy if ($nExp > $HmaxExpNavy);
					($landValue->[$x][$y], $landValue2->[$x][$y]) = navyPack($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
					if(defined $nn) {

                                                # 総獲得経験値変動
                                                my $buildLevel  = gainToLevel($nIsland->{'gain'});
                                                my $buildLevel2 = gainToLevel($nIsland2->{'gain'});
                                                if($buildLevel < $buildLevel2){
                                                    # 撃沈した側の経験値が低い
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2] * ($buildLevel2 - $buildLevel + 1));
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2] * ($buildLevel2 - $buildLevel + 1)/2);
                                                }elsif($buildLevel > $buildLevel2){
                                                    # 撃沈した側のが高い
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2] / ($buildLevel - $buildLevel2 + 1));
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2] / ($buildLevel - $buildLevel2 + 1)/2);
                                                }else{
                                                    # 同じ
						    $nIsland->{'gain'} += int($HnavyExp[$nKind2]);
						    $nIsland2->{'gain'} -= int($HnavyExp[$nKind2]/2);
                                                }

						if($island->{'event'}[1] <= $HislandTurn) {
							if($island->{'event'}[6] == 2) {
								# 艦艇経験値獲得
								$nIsland->{'epoint'}{$id} += $HnavyExp[$nKind2];
							} elsif($island->{'event'}[6] == 3) {
								# 艦艇撃沈
								$nIsland->{'epoint'}{$id}++;
							}
						}
						# アイテム奪取判定
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
								logItemGetLucky2($nId, $name, $fPoint, "${HtagName_}${name2}${H_tagName}が保有していたすべての$HitemName[0]", "沈没間際の$nName2から");
							} elsif(random($HitemSeizeDenominator) < $nExp) {
								my $num = random($nIsland2->{'itemNumber'});
								push(@{$nIsland->{'item'}}, $nIsland2->{'item'}[$num]);
								$HitemGetId[$num]{$nId2} = undef;
								$HitemGetId[$num]{$nId} = 1;
								$nIsland->{'itemNumber'}++;
								$nIsland2->{'itemNumber'}--;
								logItemGetLucky2($nId, $name, $fPoint, $HitemName[$nIsland2->{'item'}[$num]], "沈没間際の$nName2から");
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
						# サバイバル
						$nIsland2->{'epoint'}{$id} = $HislandTurn if(($island->{'event'}[6] == 1) && ($island->{'event'}[1] <= $HislandTurn));
					}
					if ($nSpecial2 & 0x8) {
						# 軍港壊滅
						logNavyPortDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

						# 浅瀬になる
						$land->[$fx][$fy] = $HlandSea;
						$landValue->[$fx][$fy] = 1;
						$nIsland2->{'navyPort'}--;
					} else {
						# 艦艇撃沈
						logNavyShipDestroy($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

						if (rand(100) < $HnavyProbWreck[$nKind2]) {
							# 残骸になる
							($landValue->[$fx][$fy], $landValue2->[$fx][$fy]) = navyPack(0, $nTmp2, $nStat2, $nSea2, int(rand(90)) + 10, 1, 0, $nKind2, 0, 0, 31, 31);
						} else {
							# 海になる
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
					# 被弾
					logNavyDamage($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $nName2, $fPoint);

					# HPが減る
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
				# 機雷
				logNavySeaMine($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);

				$land->[$fx][$fy]      = $HlandSea; # 深い海
				$landValue->[$fx][$fy] = 0;
				$HlandMove[$id][$fx][$fy] = 1;
				$island->{'ext'}[5]++;
				next;
			} elsif (($fKind == $HlandDefence) && ($defflag >= 0)) {
				# 防衛施設

				if($amityFlag{$id}) { # 無害化
					if(random(100) < $HnavySafetyInvalidp) {
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
					$nIsland->{'ext'}[2]++ if(defined $nn); # 破壊した防衛施設の数
				}

				logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
			} elsif ($fKind == $HlandCore) {
				# コア
				my($lFlag, $lLv) = (int($fLv / 10000), ($fLv % 10000));
				if( !(($n == 0x1000) && ($lFlag >= 1)) && !((($n == 0x2000) || ($n == 0x4000)) && ($lFlag <= 1)) )  {
					push(@pointErr, { 'ND' => $fPoint });
					$island->{'ext'}[5]++;
					next;
				}
				# 耐久力を下げる
				my $coreflag = $lLv - $damage;
				$fLv -= $damage;
				# コア爆撃数，コア破壊数
				$nIsland->{'epoint'}{$id}++ if((defined $nn) && ($island->{'event'}[6] == 6) || (($coreflag < 0) && ($island->{'event'}[6] == 7)) && ($island->{'event'}[1] <= $HislandTurn));
				if($coreflag >= 0) {
					$land->[$fx][$fy] = $HlandCore;
					$landValue->[$fx][$fy] = $fLv;
					logNavyNormalDefence($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} else {
					$island->{'core'}--;
					$island->{'slaughterer2'} = $nId if($HcorelessDead && (defined $nn) && !$island->{'core'}); # 破壊した島IDを記録
					if ($n == 0x1000) {
						# 魚雷　（対潜、対艦）
						logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					} elsif (($n == 0x2000) || ($n == 0x4000)) {
						# 艦砲　（対艦、対地）艦載機（対艦、対地）
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
			} elsif ($fKind == $HlandTown) {
				# 都市系
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
						# 艦艇経験値獲得
						$nIsland->{'epoint'}{$id} += int(($fLv - $sLv) / 20);
					}
				}
				$boat += ($fLv - $sLv); # 難民にプラス
				if($rank) {
					$landValue->[$fx][$fy] = $sLv;
					logNavyNormalTown($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint, $HlandTownName[$rank]);
				} else {
					$island->{'slaughterer'} = $nId if(defined $nn); # 都市系を破壊した島IDを記録
					logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
					$land->[$fx][$fy] = $HlandWaste; # 荒地（着弾点）
					$landValue->[$fx][$fy] = 1;
					$HlandMove[$id][$fx][$fy] = 1;
				}
				next;
			} else {
				# その他の地形
				if ($n == 0x1000) {
					# 魚雷　（対潜、対艦）
					logNavyTorpedoNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				} elsif (($n == 0x2000) || ($n == 0x4000)) {
					# 艦砲　（対艦、対地）艦載機（対艦、対地）
					logNavyNormal($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint);
				}
				$island->{'ext'}[5]++;

				if ($fKind == $HlandBase && (defined $nn)) {
					$nIsland->{'ext'}[3]++; # 撃破したミサイル基地の数
				}
			}

			# 攻撃後の地形にする
			if ($n == 0x1000) {
				# 魚雷　（対潜、対艦）
				$land->[$fx][$fy] = $HlandSea; # 深い海
				$landValue->[$fx][$fy] = 0;
				$landValue->[$fx][$fy] = 1 if($fKind == $HlandBouha);
			} elsif (($n == 0x2000) || ($n == 0x4000)) {
				# 艦砲　（対艦、対地）艦載機（対艦、対地）
				if ($fKind == $HlandOil) { # 海底油田
					$land->[$fx][$fy] = $HlandSea; # 深い海
					$landValue->[$fx][$fy] = 0;
				} elsif(($fKind == $HlandDefence) && ($defflag >= 0)) {
					# でも耐久力の残っている防衛施設なら耐える
					$land->[$fx][$fy] = $HlandDefence;
					$landValue->[$fx][$fy] = $fLv;
					next;
				} elsif($fKind == $HlandBouha) {
					# でも防波堤なら浅瀬
					$land->[$fx][$fy] = $HlandSea;
					$landValue->[$fx][$fy] = 1;
					$island->{'bouha'}--;
				} else {
					$land->[$fx][$fy] = $HlandWaste; # 荒地（着弾点）
					$landValue->[$fx][$fy] = 1;
				}
			}
			$HlandMove[$id][$fx][$fy] = 1;
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
		my $kind;
		if ($n == 0x1000) {
			# 魚雷　（対潜、対艦）
			$kind = ($HnavyFireName[$nKind][0] ne '') ? $HnavyFireName[$nKind][0] : '魚雷発射';
		} elsif ($n == 0x2000) {
			# 艦砲　（対艦、対地）
			$kind = ($HnavyFireName[$nKind][1] ne '') ? $HnavyFireName[$nKind][1] : '艦砲射撃';
		} elsif ($n == 0x4000) {
			# 艦載機（対艦、対地）
			$kind = ($HnavyFireName[$nKind][2] ne '') ? $HnavyFireName[$nKind][2] : '艦載機で爆撃';
		}
		logNavyMatome($id, $name, $nId, $nPoint, $nName, $tPoint, $tLandName, $kind, $str, $pntStr, join('-', (keys %damageId)));
	}
	# 難民判定
	$boat = int($boat / 2) if(!$HsurvivalTurn);
	if(($boat > 0) && (defined $nn)) {
		# 難民漂着
		my($achive) = boatAchive($nIsland, $boat); # 到達難民

		if ($achive > 0) {
			# 少しでも到着した場合、ログを吐く
			my $name = islandName($nIsland);
			logMsBoatPeople($nId, $name, $achive);
			$nIsland->{'ext'}[4] += int($achive); # 救出した難民の合計人口

			# 難民の数が一定数以上なら、平和賞の可能性あり
			if ($achive >= 200) {
				$nIsland->{'achive'} += $achive;
			}
		}
	}
	# 攻撃フラグを立てる(攻撃した艦隊は艦隊移動，派遣，帰還処理をしない)
	$nIsland->{'NavyAttack_flag'}[$nNo] = 1 if(defined $nn);
	if($land->[$x][$y] == $HlandNavy) {
		return navyUnpack($landValue->[$x][$y],$landValue2->[$x][$y]);
#logdebug ($id, "code4($x, $y)");
	} else {
		return ($nId, $nTmp, $nStat, $nSea, $nExp, 1, $nNo, $nKind, $wait, $nHp, $goalx, $goaly);
#logdebug ($id, "code5($x, $y)");
	}
}

# 難民到達処理
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
			# 町の場合
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
			# 平地の場合
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
# 周囲の町、農場があるか判定
sub countGrow {
	my($island, $x, $y) = @_;
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($i, $sx, $sy);
	foreach $i (1..6) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外
		next if(($sx < 0) || ($sy < 0) || ($HoceanMode && ($HlandID[$sx][$sy] != $id)));

		# 範囲内の場合
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

# 島全体
sub doIslandProcess {
	my($island) = @_;

	# 導出値
	my($name)      = islandName($island);;
	my($id)        = $island->{'id'};
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my $disdown    = 1;
	if($HallyDisDown && ($island->{'allyId'}[0] ne '')) {
		$disdown   = $HallyDisDown;
	}
	# 収入ログ(まとめてログ出力)
	logOilMoney($id, $name, "油田", "", "総額$island->{'oilincome'}${HunitMoney}", "収益") if($island->{'oilincome'} > 0);
	foreach (0..$#HcomplexComName) {
		my $income = $HcomplexComTFInCome[$_];
		next if($income->{'log'} ne 'matome');
		my $incomeValue = $island->{'cIncome'}[$_];
		logOilMoney($id, $name, $HcomplexName[$HcomplexComKind[$_]], "", "総額$incomeValue${HunitMoney}", $income->{'logstr'}) if($incomeValue > 0);
	}
	foreach (0..$#HcomplexName) {
		# ランダム
		$island->{'randommoney'} += $island->{'rinmoney'}[$_];
		$island->{'randomfood'} += $island->{'rinfood'}[$_];
		logOilMoney($id, $name, $HcomplexName[$_], "", "総額$island->{'rinmoney'}[$_]${HunitMoney}", "収益") if($island->{'rinmoney'}[$_] > 0);
		logOilMoney($id, $name, $HcomplexName[$_], "", "総量$island->{'rinfood'}[$_]${HunitFood}", "収穫") if($island->{'rinfood'}[$_] > 0);
	}
	# 地震判定
	if(($HpunishInfo{$id}->{punish} == 1) || (!$HnoDisFlag && (random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake * $disdown * $island->{'itemAbility'}[17])))) {
		# 地震発生

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
				# 1/4で壊滅
				if(random(4) == 0) {
					logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;

					if($landKind == $HlandBouha) {
						# でも防波堤なら浅瀬
						$land->[$x][$y] = $HlandSea;
						$landValue->[$x][$y] = 1;
						$island->{'bouha'}--;
					} elsif($landKind == $HlandComplex) {
						# 複合地形なら設定地形
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

	# 食料不足
	if(($island->{'food'} <= 0) && !$island->{'field'}) {
		# 不足メッセージ
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
				# 1/4で壊滅
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
					if($landKind == $HlandComplex) {
						# 複合地形なら設定地形
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

	# 津波判定
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
		# 津波発生
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
			($landKind == $HlandNavy) || # 軍港と船
			($landKind == $HlandSeaMine) ||
			($landKind == $HlandDefence) ||
			($landKind == $HlandHaribote)) {
				next if(countAround($island, $x, $y, $an[2], $HlandBouha));
				next if(countAroundNavyBouha($island, $x, $y));
				# 1d12 <= (周囲の海 - 1) で崩壊
				if(random(12) < (countAround($island, $x, $y, $an[1], $HlandNavy, $HlandSeaMine, $HlandOil, $HlandSbase, $HlandSea) - 1)) {
					if($landKind == $HlandNavy){
						my $fDamage = random($HdisTsunamiDmax) + 1; # ダメージ1から10
						my ($nId, $nSea, $nNo, $nKind, $nHp) = (navyUnpack($lv, $lv2))[0, 3, 6, 7, 9];
						my $nSpecial = $HnavySpecial[$nKind];
						my $n = $HidToNumber{$nId};
						$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
						if($nSpecial & 0x8) { # 港
							logTsunamiDamage($id, $name, landName($landKind, $lv), "($x, $y)");
						 	$land->[$x][$y] = $HlandSea;
							$landValue->[$x][$y] = 1;
							$Hislands[$n]->{'navyPort'}-- if(defined $n);
						} elsif(!($nHp > $fDamage)) { # か、ダメージが耐久力を奪うか
							logTsunamiDamageNavyDestroy($id, $name, landName($landKind, $lv), "($x, $y)");
						 	$land->[$x][$y] = $HlandSea;
							$landValue->[$x][$y] = $nSea;
							if(defined $n) {
								$Hislands[$n]->{'ships'}[$nNo]--;
								$Hislands[$n]->{'ships'}[4]--;
								# サバイバル
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
							# でも機雷なら海
							$land->[$x][$y] = $HlandSea;
						} elsif($landKind == $HlandComplex) {
							# 複合地形なら設定地形
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

	# 怪獣判定
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
		# 怪獣出現
		# 種類を決める
		my($kind, @r);
		foreach (0..$#HdisMonsBorder) {
			push(@r, ($_)x$HdisMonsRatio[$_]) if($pop >= $HdisMonsBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		# 怪獣出現
		bringMonster($island, 0, $kind, 0);
	}

	# 巨大怪獣判定
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
		# 巨大怪獣出現
		# 種類を決める
		my($kind, @r);
		foreach (0..$#HdisHugeBorder) {
			push(@r, ($_)x$HdisHugeRatio[$_]) if($pop >= $HdisHugeBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		bringMonster($island, 0, $kind, 1);
	}

	# 艦艇(所属不明)判定
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
		# 艦艇出現
		# 種類を決める
		my($kind, @r);
		foreach (0..$#HdisNavyRatio) {
			push(@r, ($_)x$HdisNavyRatio[$_]) if($pop >= $HdisNavyBorder[$_]);
		}
		$kind = $r[random($#r+1)];

		bringNavy($island, $kind);
	}
	# イベント島の出現判定
	if($island->{'event'}[0] && ($island->{'event'}[1] <= $HislandTurn)) {
		# 怪獣
		if($island->{'event'}[13] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[12])) {
			bringMonster($island, 0, random($#HmonsterName+1), 0, $island->{'event'}[13]);
		}
		# 巨大怪獣
		if($island->{'event'}[15] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[14])) {
			bringMonster($island, 0, random($#HhugeMonsterName+1), 1, $island->{'event'}[15]);
		}
		# 所属不明艦
		if($island->{'event'}[17] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[16])) {
			bringNavy($island, random($#HnavyName)+1, $island->{'event'}[17]);
		}
		# コア
		if($island->{'event'}[20] && !(($HislandTurn - $island->{'event'}[1])%$island->{'event'}[19])) {
			randomBuildCore($island, $island->{'event'}[20], $island->{'event'}[21], $island->{'event'}[22], 1);
		}
	}


	# 地盤沈下判定
	$wflag = ($island->{'weather'}[4] >= 90) ? 10 * $island->{'weather'}[4] : 0 if($HuseWeather);
	if(($island->{'area'} > $HdisFallBorder) &&
	   (($HpunishInfo{$id}->{punish} == 6) || (random(1000 - $wflag) < $HdisFalldown))) {
		# 地盤沈下発生
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

				if($landKind == $HlandNavy) { # 軍港と船
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
					my $nSpecial = $HnavySpecial[$nKind];
					unless ($nSpecial & 0x8) {
						# 港以外は地盤沈下しない
						next;
					}
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} elsif($landKind == $HlandComplex) {
					# 複合地形なら設定地形
					my $cKind = (landUnpack($lv))[1];
					next if($HcomplexAfter[$cKind]->{'falldown'}[0] eq '');
					next if(!countAround($island, $x, $y, $an[1], $HlandSea, $HlandSbase, $HlandNavy));
					$land->[$x][$y] = $HcomplexAfter[$cKind]->{'falldown'}[0];
					$landValue->[$x][$y] = $HcomplexAfter[$cKind]->{'falldown'}[1];
					$island->{'complex'}[$cKind]--;
					logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
					next;
				} elsif($landKind == $HlandMonster) { # 怪獣
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);

					# 海にいた
					next if ($mFlag2 & 2);
				} elsif($landKind == $HlandHugeMonster) { # 巨大怪獣は地盤沈下しない
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);

					# 海にいた
					next if ($mFlag2 & 2);
					# 周囲に海があれば、陸地フラグを浅瀬に変更
					if(countAround($island, $x, $y, $an[1], $HlandSea, $HlandSbase)) {
						logFalldownLand($id, $name, landName($landKind, $lv), "($x, $y)");
						$mFlag |= 2;
						$mSea = 1;
						$landValue->[$x][$y] = monsterPack($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp);
						next;
					}
				}

				# 周囲に海があれば、値を-1に
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
#				# -1になっている所を浅瀬に
#				$land->[$x][$y] = $HlandSea;
#				$landValue->[$x][$y] = 1;
#			} elsif ($landKind == $HlandSea) {
#				# 浅瀬は海に
#				$landValue->[$x][$y] = 0;
#			}
#
#		}

		logFalldown($id, $name);
	}

	# 台風判定
	$wflag = ($island->{'weather'}[3] >= 20) ? 10 * $island->{'weather'}[3] : 0 if($HuseWeather);
	if(($HpunishInfo{$id}->{punish} == 7) || (!$HnoDisFlag && (random(1000 - $wflag) < $HdisTyphoon * $disdown * $island->{'itemAbility'}[18]))) {
		# 台風発生
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

				# 1d12 <= (6 - 周囲の森) で崩壊
				if(random(12) < (6 - countAround($island, $x, $y, $an[1], $HlandForest, $HlandMonument)
									- countAroundComplex($island, $x, $y, $an[1], 0x4))
					) {
					logTyphoonDamage($id, $name, landName($landKind, $lv), "($x, $y)");
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					if($landKind == $HlandComplex) {
						# 複合地形なら設定地形
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

	# 巨大隕石判定
	if(($HpunishInfo{$id}->{punish} == 8) || (!$HnoDisFlag && (random(1000) < $HdisHugeMeteo * $disdown * $island->{'itemAbility'}[20]))) {
		my($x, $y, $landKind, $lv, $point);

		# 落下
		$x = $x[0] + random($HislandSizeX);
		$y = $y[0] + random($HislandSizeY);
		if ($HpunishInfo{$id}->{punish} == 8) {
			$x = $HpunishInfo{$id}->{x};
			$y = $HpunishInfo{$id}->{y};
		}
		$landKind = $land->[$x][$y];
		$lv = $landValue->[$x][$y];
		$point = "($x, $y)";

		# 広域被害ルーチン
		wideDamage($id, $name, $island, $x, $y);
		# メッセージ
		logHugeMeteo($id, $name, $point);
	}

	# 巨大ミサイル判定
	while($island->{'bigmissile'} > 0) {
		$island->{'bigmissile'} --;

		my($x, $y, $landKind, $lv, $point);

		# 落下
		$x = $x[0] + random($HislandSizeX);
		$y = $y[0] + random($HislandSizeY);
		$landKind = $land->[$x][$y];
		$lv = $landValue->[$x][$y];
		$point = "($x, $y)";

		# 広域被害ルーチン
		wideDamage($id, $name, $island, $x, $y);
		# メッセージ
		logMonDamage($id, $name, $point);
	}

	# 隕石判定
	if(($HpunishInfo{$id}->{punish} == 9) || (!$HnoDisFlag && (random(1000) < $HdisMeteo * $disdown * $island->{'itemAbility'}[19]))) {
		my($x, $y, $landKind, $lv, $point, $first, $pflag);
		$first = 1;
		$pflag = 1;
		while((random(2) == 0) || ($first == 1)) {
			$first = 0;

			# 落下
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
				# 海ポチャ
				logMeteoSea($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandSeaMine) {
				# 機雷
				logMeteoMountain($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandMountain) {
				# 山破壊
				logMeteoMountain($id, $name, landName($landKind, $lv), $point);
				$land->[$x][$y] = $HlandWaste;
				$landValue->[$x][$y] = 1;
				next;
			} elsif(($landKind == $HlandSbase) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				logMeteoSbase($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandComplex) {
				# 複合地形なら設定地形
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
						# 行による位置調整
						$ssx-- if(!($ssy % 2) && ($y % 2));
						$ssx = $correctX[$ssx + $#an];
						$ssy = $correctY[$ssy + $#an];
						# 範囲外
						next if(($ssx < 0) || ($ssy < 0));

						next if($land->[$ssx][$ssy] != $HlandHugeMonster);
						# 各要素の取り出し
						my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
						next if($mHflag2 != $j);
						if ($mFlag2 & 2) {
							# 海にいた
							$land->[$ssx][$ssy] = $HlandSea;
							$landValue->[$ssx][$ssy] = $mSea2;
						} else {
							# 陸地にいた
							$land->[$ssx][$ssy] = $HlandWaste;
							$landValue->[$ssx][$ssy] = 0;
						}
					}
				}
			} elsif(($landKind == $HlandSea) ||
					(($landKind == $HlandCore) && (int($lv / 10000) == 1))) {
				# 浅瀬
				logMeteoSea1($id, $name, landName($landKind, $lv), $point);
			} elsif($landKind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($lv, $lv2);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				$Hislands[$n]->{'shipk'}[$nKind]-- if(defined $n);
				if ($nSpecial & 0x8) {
					# 港
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logMeteoNormal($id, $name, landName($landKind, $lv), $point);
				} else {
					# その他
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

	# 噴火判定
	if(($HpunishInfo{$id}->{punish} == 10) || (!$HnoDisFlag && (random(1000) < $HdisEruption * $disdown * $island->{'itemAbility'}[21]))) {
		my($x, $y, $sx, $sy, $i, $landKind, $lv, $point);
		if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
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
		# 巨大怪獣処理(コアをやられた場合のみ)
		if(($landKind == $HlandHugeMonster) && ($mHflag == 0)) {
			my($j, $ssx, $ssy);
			foreach $j (1..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$ssx = $x + $ax[$j];
				$ssy = $y + $ay[$j];
				# 行による位置調整
				$ssx-- if(!($ssy % 2) && ($y % 2));
				$ssx = $correctX[$ssx + $#an];
				$ssy = $correctY[$ssy + $#an];
				# 範囲外
				next if(($ssx < 0) || ($ssy < 0));

				next if($land->[$ssx][$ssy] != $HlandHugeMonster);
				# 各要素の取り出し
				my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
				next if($mHflag2 != $j);
				if ($mFlag2 & 2) {
					# 海にいた
					$land->[$ssx][$ssy] = $HlandSea;
					$landValue->[$ssx][$ssy] = $mSea2;
				} else {
					# 陸地にいた
					$land->[$ssx][$ssy] = $HlandWaste;
					$landValue->[$ssx][$ssy] = 0;
				}
			}
		}

		foreach $i (1..6) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];
			# 範囲外
			next if(($sx < 0) || ($sy < 0));

			$landKind = $land->[$sx][$sy];
			$lv = $landValue->[$sx][$sy];
			$point = "($sx, $sy)";

			# 範囲内の場合
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
				# 海、油田の場合
				if(!$lv || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
					logEruptionSea($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandSea;
					$landValue->[$sx][$sy] = 1;
					next;
				} else {
					# 浅瀬
					logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					next if($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim))); # 島の最外周を埋め立て不可にする場合;
				}
			} elsif(($landKind == $HlandSeaMine) ||
				($landKind == $HlandSbase) ||
				(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				# 機雷、海基，海底コアの場合
				logEruptionSea($id, $name, landName($landKind, $lv), $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 1;
				next;
			} elsif(($landKind == $HlandMountain) ||
				($landKind == $HlandWaste)) {
				next;
			} elsif($landKind == $HlandComplex) {
				# 複合地形なら設定地形
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
					# 港は陸地
					logEruptionSea1($id, $name, landName($landKind, $lv), $point);
					$land->[$sx][$sy] = $HlandWaste;
					$landValue->[$sx][$sy] = 0;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
				} else {
					if(!$nSea || ($HedgeReclaim && (($sx < $HedgeReclaim) || ($sx > $x[$#x] - $HedgeReclaim) || ($sy < $HedgeReclaim) || ($sy > $y[$#y] - $HedgeReclaim)))) {
						# その他は浅瀬
						logEruptionSea($id, $name, landName($landKind, $lv), $point);
						$land->[$sx][$sy] = $HlandSea;
						$landValue->[$sx][$sy] = 1;
					} else {
						# 浅瀬は陸地
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
				# それ以外の場合
				logEruptionNormal($id, $name, landName($landKind, $lv), $point);
			}
			$land->[$sx][$sy] = $HlandWaste;
			$landValue->[$sx][$sy] = 0;
		}
		logEruption($id, $name, landName($land->[$x][$y], $landValue->[$x][$y]), "($x, $y)");
	}

        # 鉱床、漁礁が無かったら出るように
        if($island->{'stone'} < 2){
            # 鉱床
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
                # 漁礁
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

# 島全体(estimate処理)
sub doIslandProcessEstimate {
	my($number, $island) = @_;

	# 導出値
	my($name)      = islandName($island);;
	my($id)        = $island->{'id'};

	# 食料があふれてたら換金
	my $fflag = $island->{'itemAbility'}[7];
	if($island->{'food'} > int($HmaximumFood * $fflag)) {
		$island->{'money'} += int(($island->{'food'} - ($HmaximumFood * $fflag)) / 10);
		$island->{'food'} = int($HmaximumFood * $fflag);
	}

	# 金があふれてたら切り捨て
	my $mflag = $island->{'itemAbility'}[8];
	if($island->{'money'} > int($HmaximumMoney * $mflag)) {
		$island->{'money'} = int($HmaximumMoney * $mflag) ;
	}

	# 各種の値を計算
	estimate($number);

	# 各種勲章受賞
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
				$flags |= $f; # 受勲
				$island->{'ext'}[1] += $Hprize[$p]->{'contribution'}; # 貢献度up
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

# 怪獣出現
sub bringMonster {
	my($island, $tId, $mKind, $huge, $num) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};

	# flag : bit0=硬化, bit1=潜水
	my $mHp = (!$huge) ? ($HmonsterBHP[$mKind] + random($HmonsterDHP[$mKind])) : ($HhugeMonsterBHP[$mKind] + random($HhugeMonsterDHP[$mKind]));
	my $mLv = monsterPack($tId, 0, 0, 0, 2, $mKind, $mHp);

	makeRandomIslandPointArray($island);
	my($i, $x, $y, $lv);
	my $count = 0;
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];
		$lv = $landValue->[$x][$y];

		# 深い海を探す（怪獣は深い海に潜む）
		next unless (($land->[$x][$y] == $HlandSea) && !$lv);

		# 巨大怪獣の場合
		if($huge) {
			my($j, $sx, $sy);
			my $dmove = 0;
			foreach $j (1..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				# 行による位置調整
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];

				# 範囲外判定
				if(($sx < 0) || ($sy < 0)) {
					$dmove = 1;
				}
				if($HoceanMode && $HfieldUnconnect && ($HlandID[$sx][$sy] != $id)) {
					my $mn = $HidToNumber{$HlandID[$sx][$sy]};
					$dmove = 1 if(((defined $mn) && $Hislands{$mn}->{'field'}) || $island->{'field'});
				}
				# 海以外なら出現できない
				if($land->[$sx][$sy] != $HlandSea) {
					$dmove = 1;
				}
			}
			next if($dmove);
		}

		# 地形名
		my $lName = landName($HlandSea, $lv);

		# 怪獣を配置
		if($huge) {
			# 巨大怪獣の場合
			my($j, $sx, $sy, $mSea, $mFlag);
			foreach $j (0..6) {
				next if($HhugeMonsterImage[$mKind][$j] eq '');
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				# 行による位置調整
				$sx-- if(!($sy % 2) && ($y % 2));
				$sx = $correctX[$sx + $#an];
				$sy = $correctY[$sy + $#an];
				# 範囲外
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

		# 移動済みにする
		$HmonsterMove[$id][$x][$y] = 2;

		# 怪獣名
		my $mName = (!$huge) ? $HmonsterName[$mKind] : $HhugeMonsterName[$mKind];

		# メッセージ
		logMonsCome($id, $name, $mName, "($x, $y)", $lName);
		last if(++$count >= $num);
	}
}

# 艦艇出現
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

		# 深い海を探す
		next unless (($land->[$x][$y] == $HlandSea) && !$lv);

		# 地形名
		my $lName = landName($HlandSea, $lv);

		# 艦艇を配置
		$land->[$x][$y] = $HlandNavy;
		$landValue->[$x][$y] = $nLv;
		$landValue2->[$x][$y] = $nLv2;

		# 移動済みにする
		$HnavyMove[$id][$x][$y] = 2;

		# 艦艇名
		my $nName = $HnavyName[$nKind];

		# メッセージ
		logNavyCome($id, $name, $nName, "($x, $y)", $lName);
		last if(++$count >= $num);
	}
}

# コア出現
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

		# 海，浅瀬，平地，荒地をさがす
		next if(($l != $HlandSea) && ($l != $HlandPlains) && ($l != $HlandWaste));

		# 地形名
		my $lName = landName($l, $lv);

		# コアを配置
		$land->[$x][$y] = $HlandCore;
		$lvmin = $HdurableCore if($lvmin > $HdurableCore);
		$lvmax = $HdurableCore if($lvmax > $HdurableCore);
		$lvmin = $lvmax if($lvmin > $lvmax);
		$landValue->[$x][$y] = $lvmin + random($lvmax - $lvmin + 1);
		if($l == $HlandSea) {
			$landValue->[$x][$y] += (!$lv) ? 20000 : 10000; # 海，浅瀬
		}

		# コア名
		my $nName = landName($land->[$x][$y], $landValue->[$x][$y]);
		my $point = ($HcoreHide) ? "(?, ?)" : "($x, $y)";

		# メッセージ
		logCoreRandomBuild($id, $name, $nName, $point, $lName) if($log);
		$island->{'core'}++;
		last if(++$count >= $num);
	}
}

# 複合地形建設
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
		# 不適当な地形
		logLandFail($id, $name, $comName, $landName, $point);
		return 0;
	} elsif($landKind == $HlandComplex) {
		# すでに複合地形の場合
		($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $landCheck = ($HcomplexComKind[$kind] != $cKind) ? 1 : 0;
		foreach (@{$HcomplexBefore2[$HcomplexComKind[$kind]]}) {
			if($cKind == $_) {
				$landCheck = 0;
				last;
			}
		}
		if($landCheck || (!$HcomplexTPCmax[$cKind] && !$HcomplexFPCmax[$cKind] && !$HcomplexMPCmax[$cKind])) {
			# 不適当な地形
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		if(($HcomplexComKind[$kind] != $cKind) || !($HcomplexComFlag[$kind] & 0x7)) {
			# 目的の場所を複合地形に
			if($HcomplexMax[$HcomplexComKind[$kind]] && $island->{'complex'}[$HcomplexComKind[$kind]] >= $HcomplexMax[$HcomplexComKind[$kind]]) {
				# 保有可能最大数オーバー
				logOverFail($id, $name, $comName, $point);
				return 0;
			}
			$island->{'complex'}[$cKind]--;
			$land->[$x][$y] = $HlandComplex;
			$cKind = $HcomplexComKind[$kind];
			$island->{'complex'}[$cKind]++;
			($cTurn, $cFood, $cMoney) = (1, 0, 0);
		} else {
			# 食料フラグ処理
			$cFood  += $rep if($HcomplexComFlag[$kind] & 0x2);
			# 資金フラグ処理
			$cMoney += $rep if($HcomplexComFlag[$kind] & 0x4);
			if($HcomplexComFlag[$kind] & 0x1) {
				# ターンフラグ置換処理
				my $income = $HcomplexComTFInCome[$kind];
				my $incomeValue = $cTurn * $income->{'ratio'};
				if($income->{'log'} eq 'normal') {
					$island->{$income->{'type'}} += $incomeValue;
					logOilMoney($id, $name, $HcomplexName[$cKind], $point, "$incomeValue${HunitMoney}", $income->{'logstr'});
				} else {
					$island->{'cIncome'}[$kind] += $incomeValue;
				}
				# ターンフラグリセット
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
			# 保有可能最大数オーバー
			logOverFail($id, $name, $comName, $point);
			return 0;
		}
		# 目的の場所を複合地形に
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

# 艦艇建造（港も含む）
sub buildNavy {
	my($island, $comName, $nKind, $nNo, $nx, $ny) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};
	my $point     = "($nx, $ny)";
        my $landcount;
	# ４艦隊のみ
	$nNo--;
	if ($nNo < 0) {
		$nNo = 0;
	} elsif ($nNo > 3) {
		$nNo = 3;
	}

        # 建設予定地が浅瀬かどうか先にチェック
        my ($asase) = 0;
	if (($land->[$nx][$ny] == $HlandSea) && ($landValue->[$nx][$ny] == 1)) {
            $asase = 1;
        }

	# flag : bit0=通常, bit1=残骸, bit2=潜水, bit3=工事中
	my ($nLv, $nLv2);
        if($HnavyBuildTurn[$nKind] == 0){
	    ($nLv, $nLv2) = navyPack($id, 0, 0, $asase, 0, 0, $nNo, $nKind, $HnavyCruiseTurn[$nKind] + 1, $HnavyHP[$nKind], 31, 31);#舟艇、航空機の場合
        }else{
	    ($nLv, $nLv2) = navyPack($id, 0, 0, 0, 0, 3, $nNo, $nKind, 0, 0, 31, 31);#軍艦の場合 工期フラグを立てて、Hp(工期)を0に設定
        }

        # 港の場合は周りの陸地を数えて、$nLvと$nLv2を再設定
        if($nKind == 0){
            $landcount = searchLand($island, $nx, $ny);
            if($landcount > 3){
                $landcount = 3;
            }
            my $shortcut = $landcount * 3;
	    ($nLv, $nLv2) = navyPack($id, 0, 0, 0, 0, 3, $nNo, $nKind, 0, $shortcut, 31, 31);#再設定
        }

	my $nSpecial = $HnavySpecial[$nKind];
	my $ofname = $island->{'fleet'}->[$nNo];

	# 建造レベル確認
	if($HmaxComNavyLevel) {
		my $navyComLevel = gainToLevel($island->{'gain'});
		if($HcomNavyNumber[$navyComLevel-1] < $nKind) {
			logNavyNoExp($id, $name, $comName);
			return 0;
		}
	}
	# 保有可能艦艇数チェック
	my $nflag = int($island->{'itemAbility'}[3]);
	my $nflagk = (!$#HnavyName) ? 1 : int($nflag/$#HnavyName);
	$nflagk = 1 if($nflag && ($nflagk < 1));
	if($HnavyKindMax[$nKind] && ($island->{'shipk'}[$nKind] >= $HnavyKindMax[$nKind] + $nflagk)) {
		logNavyKindMaxOver($id, $name, $comName);
		return 0;
	}

	my($i, $x, $y, $lv, $lv2);

	if ($nSpecial & 0x8) {
		# 軍港建設
		if($HedgeReclaim) { # 島の最外周を埋め立て不可にする場合
			my($map) = $island->{'map'};
			my(@x) = @{$map->{'x'}};
			my(@y) = @{$map->{'y'}};
			if(($nx < $x[0] + $HedgeReclaim) || ($nx > $x[$#x] - $HedgeReclaim) || ($ny < $y[0] + $HedgeReclaim) || ($ny > $y[$#y] - $HedgeReclaim)) {
				logLandFail($id, $name, $comName, "島の最外周", $point);
				return 0;
			}
		}
		# 港なら位置指定
		$lv = $landValue->[$nx][$ny];
		if (($land->[$nx][$ny] == $HlandSea) && ($lv == 1)) {
			# 浅瀬なら建設
			$land->[$nx][$ny] = $HlandNavy;
			$landValue->[$nx][$ny] = $nLv;
                        $landValue2->[$nx][$ny] = $nLv2;
			$island->{'navyPort'}++;
			# メッセージ
			logLandSuc($id, $name, $comName, $point);
			return 1;
		} else {
			# その他は失敗
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
		logFleetMaxOver($id, $island->{'ships'}[4], $comName, "１軍港あたり");
		return 0;
	} elsif($HfleetMaximum && ($island->{'ships'}[$nNo] >= $HfleetMaximum + int($nflag/4))) {
		logFleetMaxOver($id, $name, $comName, "${ofname}艦隊");
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
			# 艦艇を建造するには軍港が必要

			logNavyNoPort($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		$lv = $landValue->[$nx][$ny];
		# 深い海でなければ建造できない
		unless ($land->[$nx][$ny] == $HlandSea && (!$lv || !$HnavyBuildTurn[$nKind])){
			logNavyNoSea($id, $name, $comName, "($nx, $ny)");
			return 0;
		}
		my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, $goalx, $goaly) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);
		# 軍港の建造レベル確認
		if($HmaxComPortLevel && ($HcomNavyNumber[(expToLevel($HlandNavy, $pExp) - 1)] < $nKind)) {
			logNavyNoExp($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		# 艦艇を配置
		$land->[$nx][$ny] = $HlandNavy;
		$landValue->[$nx][$ny] = $nLv;
	        $landValue2->[$nx][$ny] = $nLv2;
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$nNo]++;
		$island->{'ships'}[4]++;

		# 移動済みにする
		$HnavyMove[$id][$nx][$ny] = 2;

		# 艦艇名
		my $nName = $HnavyName[$nKind];

		# メッセージ
                if($plane == 0){
		    logNavyBuild($id, $name, $ofname, $nName, "($nx, $ny)");
                }else{
		    logNavyBuild2($id, $name, $ofname, $nName, "($nx, $ny)");
                }

		# 軍港or空母に経験値と待機時間
                if($pKind == 0){
		    $pExp += $HnavyBuildExp[$nKind];
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # 航空機発進なら、$waitを設定
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = $HnavyCruiseTurn[$nKind];
                    }
                }else{
		    $pExp += int($HnavyBuildExp[$nKind] / 3);
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # 航空機発進なら、$waitを設定
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = int($HnavyCruiseTurn[$nKind] / 3);
                    }
                }

		($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait + 1, $pHp, 31, 31);




		return 1;
	} else {
                # このelseは条件満たすことはないんで、、、
		if($island->{'navyPort'} < 1) {
			# 艦艇を建造するには軍港が必要
			logNavyNoPort($id, $name, $comName);
			return 0;
		}

		# もっとも近い軍港の建造レベル確認
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

			# 深い海を探す
			next unless (($land->[$x][$y] == $HlandSea) && !$lv);

			# 艦艇を配置
			$land->[$x][$y] = $HlandNavy;
			$landValue->[$x][$y] = $nLv;
			$island->{'shipk'}[$nKind]++;
			$island->{'ships'}[$nNo]++;
			$island->{'ships'}[4]++;

			# 移動済みにする
			$HnavyMove[$id][$x][$y] = 2;

			# 艦艇名
			my $nName = $HnavyName[$nKind];

			# 軍港に経験値
			$pExp += $HnavyBuildExp[$nKind];
			$pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
			($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, 31, 31);

			return 1;
		}
	}

	# 艦艇を配備する海がない
	logNavyNoSea($id, $name, $comName);
	return 0;
}


# 航空機海外発進
sub buildNavy2 {
        # 注意 このルーチンでは、ターゲットの島を$islandとして扱う$tIslandではない
	my($island, $comName, $nKind, $nNo, $nx, $ny, $nId) = @_;

	my $id        = $island->{'id'};
	my $name      = islandName($island);
	my $land      = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my $landValue2 = $island->{'landValue2'};
	my $point     = "($nx, $ny)";
        my $landcount;

        # コマンド送信者の島データ取得
	my $nn = $HidToNumber{$nId};
	my $nIsland = $Hislands[$nn];
	my $nName      = islandName($nIsland);

	# ４艦隊のみ
	$nNo--;
	if ($nNo < 0) {
		$nNo = 0;
	} elsif ($nNo > 3) {
		$nNo = 3;
	}

        # 建設予定地が浅瀬かどうか先にチェック
        my ($asase) = 0;
	if (($land->[$nx][$ny] == $HlandSea) && ($landValue->[$nx][$ny] == 1)) {
            $asase = 1;
        }

	my ($nLv, $nLv2);
	    ($nLv, $nLv2) = navyPack($nId, 0, 0, $asase, 0, 0, $nNo, $nKind, $HnavyCruiseTurn[$nKind] + 1, $HnavyHP[$nKind], 31, 31);#航空機専用

	my $nSpecial = $HnavySpecial[$nKind];
	my $ofname = $island->{'fleet'}->[$nNo];

	# 建造レベル確認
	if($HmaxComNavyLevel) {
		my $navyComLevel = gainToLevel($nIsland->{'gain'});
		if($HcomNavyNumber[$navyComLevel-1] < $nKind) {
			logNavyNoExp($id, $name, $comName);
			return 0;
		}
	}

	# 保有可能艦艇数チェック
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
		logFleetMaxOver($id, $name, $comName, "１軍港あたり");
		return 0;
	} elsif($HfleetMaximum && ($island->{'ships'}[$nNo] >= $HfleetMaximum + int($nflag/4))) {
		logFleetMaxOver($id, $name, $comName, "${ofname}艦隊");
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
			# 艦艇を建造するには軍港が必要

			logNavyNoPort($nId, $name, $comName, "($nx, $ny)");
			return 0;
		}

		my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp, $goalx, $goaly) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);

		# 海でなければ建造できない
		unless ($land->[$nx][$ny] == $HlandSea){
			logNavyNoSea($id, $name, $comName, "($nx, $ny)");
			return 0;
		}

		# 艦艇を配置
		$land->[$nx][$ny] = $HlandNavy;
		$landValue->[$nx][$ny] = $nLv;
	        $landValue2->[$nx][$ny] = $nLv2;
		$island->{'shipk'}[$nKind]++;
		$island->{'ships'}[$nNo]++;
		$island->{'ships'}[4]++;

		# 移動済みにする
		$HnavyMove[$id][$nx][$ny] = 2;

		# 艦艇名
		my $nName = $HnavyName[$nKind];

		# メッセージ
                if($plane == 0){
		    logNavyBuild($id, $nName, $ofname, $nName, "($nx, $ny)");
                }else{
		    logNavyBuild2($id, $nName, $ofname, $nName, "($nx, $ny)", $nId);
                }

		# 軍港or空母に経験値と待機時間
                if($pKind == 0){
		    $pExp += $HnavyBuildExp[$nKind];
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # 航空機発進なら、$waitを設定
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = $HnavyCruiseTurn[$nKind];
                    }
                }else{
		    $pExp += int($HnavyBuildExp[$nKind] / 3);
   		    $pExp = $HmaxExpNavy if ($pExp > $HmaxExpNavy);
                    # 航空機発進なら、$waitを設定
                    if($HnavyCruiseTurn[$nKind] != 0){
                        $pWait = int($HnavyCruiseTurn[$nKind] / 3);
                    }
                }

		($landValue->[$px][$py], $landValue2->[$px][$py]) = navyPack($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait + 1, $pHp, 31, 31);

		return 1;
	}

	# 艦艇を配備する海がない
	logNavyNoSea($id, $name, $comName);
	return 0;
}



# 広域被害ルーチン
sub wideDamage {
	my($id, $name, $island, $x, $y) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($sx, $sy, $i, $landKind, $landName, $lv, $point);

	foreach $i (0..18) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外
		next if(($sx < 0) || ($sy < 0));

		$landKind = $land->[$sx][$sy];
		$lv = $landValue->[$sx][$sy];
		$landName = landName($landKind, $lv);
		$point = "($sx, $sy)";

		# 範囲による分岐
		if($i < 7) {
			# 中心、および1ヘックス
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
				# 複合地形なら設定地形
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
					# 海
					$landValue->[$sx][$sy] = 0;
					logWideDamageMonsterSea2($id, $name, $landName, $point);
				} else {
					# 浅瀬
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
					# 港は浅瀬
					$landValue->[$sx][$sy] = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logWideDamageSea($id, $name, $landName, $point);
				} else {
					# その他は海
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
					# 海
					$landValue->[$sx][$sy] = 0;
				} else {
					# 浅瀬
					$landValue->[$sx][$sy] = 1;
				}
			}
		} else {
			# 2ヘックス
			if(($landKind == $HlandSea) ||
				($landKind == $HlandOil) ||
				($landKind == $HlandSeaMine) ||
				($landKind == $HlandWaste) ||
				($landKind == $HlandMountain) ||
				($landKind == $HlandSbase) ||
				(($landKind == $HlandCore) && (int($lv / 10000) == 2))) {
				next;
			} elsif($landKind == $HlandComplex) {
				# 複合地形なら設定地形
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
						# 行による位置調整
						$ssx-- if(!($ssy % 2) && ($sy % 2));
						$ssx = $correctX[$ssx + $#an];
						$ssy = $correctY[$ssy + $#an];
						# 範囲外
						next if(($ssx < 0) || ($ssy < 0));

						next unless($land->[$ssx][$ssy] == $HlandHugeMonster);
						# 各要素の取り出し
						my($mHflag2, $mSea2, $mFlag2) = (monsterUnpack($landValue->[$ssx][$ssy]))[1, 2, 4];
						next if($mHflag2 != $j);
						if ($mFlag2 & 2) {
							# 海にいた
							$land->[$ssx][$ssy] = $HlandSea;
							$landValue->[$ssx][$ssy] = $mSea2;
						} else {
							# 陸地にいた
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
					# 港は浅瀬
					$landValue->[$sx][$sy] = 1;
					$Hislands[$n]->{'navyPort'}-- if(defined $n);
					logWideDamageSea($id, $name, $landName, $point);
				} else {
					# その他は海
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

# 戦争してるか判定する(２島間の戦争状態)
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
				# 戦争準備中(猶予期間)
				return 1;
			} else {
				# 戦争中
				return 2;
			}
		}
	}
	return 0;
}

# 戦争してるか判定する(１島の戦争状態)
sub chkWarIslandOR {
	my($id, $tId) = @_;
	return 2 if(($id == 0) || ($tId == 0));
	my($i, %chkFlag);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($wid1) = $HwarIsland[$i+1];
		my($wid2) = $HwarIsland[$i+2];
# chkWarIslandのあとに使う間は不要な処理
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

# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手
# 第4引数:相手2
# 通常ログ
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# 遅延ログ
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# 機密ログ
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[3],$_[0]");
}

# 記録ログ
sub logHistory {
	push(@HhistoryLogPool,"$HislandTurn,$_[0]\n");
}

# ログ書き出し
sub logFlush {
	open(LOUT, ">${HdirName}/0$HlogData");
	# 全部逆順にして書き出す
	foreach (reverse(@HlogPool, @HlateLogPool, @HsecretLogPool)) {
		next if($_ eq ',,,,,');
		print LOUT $_ . "\n";
	}
	close(LOUT);

	# 記録ログ書き出しと調整
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
# ログテンプレート
#----------------------------------------------------------------------
# 島ポイント指定ログテンプレ
sub logIslpnt {
	my($id, $name, $point, $tId, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}$str",$id, $tId);
}

# アイテム発見
sub logItemGetLucky {
	my($id, $name, $point, $itemName, $str) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の${str}、<B>$itemName</B>を発見しました！",$id);
}

# アイテム発見2
sub logItemGetLucky2 {
	my($id, $name, $point, $itemName, $str) = @_;
	logOut("　--- ${HtagName_}${point}${H_tagName}の${str}、${HtagMoney_}${itemName}${H_tagMoney}を発見しました！",$id);
}

# アイテム消失
sub logItemLost {
	my($id, $name, $itemName, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}の${str}、<B>$itemName</B>が消失しました！",$id);
}

# 艦艇、海底探査中沈没
sub logProbeDestroy {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}の${HtagName_}${nName}${H_tagName}が海底探査中に<B>通信が途絶えました</B>。<B>$nName</B>は${HtagDisaster_}沈没${H_tagDisaster}したようです。",$id, $nId);
}

# 海底探索からの収入
sub logTansaku {
	my($id, $name, $nId, $lName, $point, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が財宝を発見！${HtagMoney_}${str}${H_tagMoney}の価値があることがわかりました。",$id, $nId);
	logHistory("${HtagName_}${name}${H_tagName}の<B>$lName</B>が財宝を発見！");
}

# 海賊行為
sub logPirates {
	my($id, $name, $point, $nId, $nName, $nPoint, $str) = @_;
	logOut("${HtagName_}${name}$nPoint${H_tagName}の<B>$nName</B>が${HtagName_}$point${H_tagName}地点から$strを<B>略奪</B>しました。",$id, $nId);
}

# 艦艇、機雷で沈没
sub logSeaMineDestroy {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}の${HtagName_}${nName}${H_tagName}が<B>機雷に接触し大破</B>。<B>$nName</B>は${HtagDisaster_}沈没${H_tagDisaster}しました。",$id, $nId);
}

# 艦艇、機雷でダメージ
sub logSeaMineDamage {
	my($id, $name, $nId, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}の${HtagName_}${nName}${H_tagName}が<B>機雷に接触</B>。<B>$nName</B>は黒煙を噴き出しました。",$id, $nId);
}

# 怪獣、機雷で殺傷
sub logMonsSeaMineDestroy {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に<B>$mName</B>が接触。<B>$mName</B>は力尽き、海底に${HtagDisaster_}倒れました${H_tagDisaster}。",$id, $mId);
}

# 怪獣、機雷で殺傷
sub logMonsSeaMineDamage {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に<B>$mName</B>が接触。<B>$mName</B>は苦しそうに咆吼しました。",$id, $mId);
}

# 艦艇攻撃、怪獣がミサイル攻撃、機雷に命中
sub logNavySeaMine {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は消し飛びました。",$id, $nId);
}

# 資金足りない
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、資金不足のため中止されました。",$id);
}

# 食料足りない
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、備蓄食料不足のため中止されました。",$id);
}

# 開発期間による失敗
sub logDevelopTurnFail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、${AfterName}を発見した直後の<B>開発期間</B>だったため中止されました。",$id);
}

# 開発期間超過による失敗
sub logDevelopTurnFail2 {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、${AfterName}を発見した直後の<B>開発期間を過ぎている</B>ため中止されました。",$id);
}

# 貿易能力艦艇を派遣していないため援助失敗
sub logTradeFail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>援助可能な艦艇が派遣されていない</B>ため中止されました。",$id);
}

# 艦艇移動、失敗
sub logMoveFail {
	my($id, $name, $point,$str, $tId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}地点に対する移動指令は$str実行されませんでした。",$id, $tId);
}

# 一括地ならし
sub logAllPrepare {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}$comName${H_tagComName}が行われました。",$id);
}

# 保有可能数オーバー(機雷・防波堤・複合地形)
sub logOverFail {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、保有可能数を超えるため中止されました。",$id);
}

# 対象地形の種類による失敗
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}が<B>$kind</B>だったため中止されました。",$id);
}

# 地形以外の問題で失敗
sub logLandFail2 {
	my($id, $name, $comName, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>$kind</B>ため中止されました。",$id);
}

# 周りに陸がなくて埋め立て失敗
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に陸地がなかったため中止されました。",$id);
}

# 軍港がないため艦艇の建造失敗
sub logNavyNoPort {
	my($id, $name, $comName, $point, $tId) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、艦艇が寄港する<B>軍港がない</B>ため中止されました。",$id, $tId);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、近くに<B>軍港がない</B>ため中止されました。",$id, $tId);
	}
}

# 海がないため艦艇の建造失敗
sub logNavyNoSea {
	my($id, $name, $comName, $point) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、艦艇を配備する<B>海がない</B>ため中止されました。",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、配備する地点が<B>深い海でない</B>ため中止されました。",$id);
	}
}

# 経験値がないため艦艇の建造失敗
sub logNavyNoExp {
	my($id, $name, $comName, $point) = @_;
	if($point eq "") {
		logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>建造技術が足りない</B>ため中止されました。",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>建造技術が足りない</B>ため中止されました。",$id);
	}
}

# 艦艇最大数オーバーによる建造失敗
sub logNavyMaxOver {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>保有可能艦艇数を越える</B>ため中止されました。",$id);
}

# 艦艇種最大数オーバーによる建造失敗
sub logNavyKindMaxOver {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>艦艇種別の保有可能数を越える</B>ため中止されました。",$id);
}

# １艦隊(軍港)保有可能艦艇数オーバーによる建造失敗
sub logFleetMaxOver {
	my($id, $name, $comName, $nName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>$nNameの保有可能艦艇数を越える</B>ため中止されました。",$id);
}

# 弾薬費用が足りずに攻撃中止
sub logNavyNoShell {
	my($id, $tId, $name, $nPoint, $nName) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}の${HtagName_}${nName}${H_tagName}の攻撃は<B>弾薬がない</B>ため中止されました。",$id,$tId);
}

# 整地系成功
sub logLandSuc {
	my($id, $name, $comName, $point, $tId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id, $tId);
}

# 整地系ログまとめ
sub logLandSucMatome {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。<br>　　<B>⇒</B> $point",$id);
}

# 油田発見
sub logOilFound {
	my($id, $name, $point, $comName, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われ、<B>油田が掘り当てられました</B>。",$id);
}

# 油田発見ならず
sub logOilFail {
	my($id, $name, $point, $comName, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われましたが、油田は見つかりませんでした。",$id);
}

# 油田からの収入
sub logOilMoney {
	my($id, $name, $lName, $point, $value, $str) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>から、${HtagMoney_}$value${H_tagMoney}の$strが上がりました。",$id);
}

# 油田枯渇
sub logOilEnd {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>は枯渇したようです。",$id);
}

# 防衛施設、耐久力アップ
sub logBombDurableUp {
	my($id, $name, $lName, $point, $num, $hide) = @_;
	if ($hide) {
		logSecret("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が耐久力を$numアップしました。",$id);
		logOut("こころなしか、${HtagName_}${name}${H_tagName}の<B>森</B>が増えたようです。",$id);
#		logOut("${HtagName_}${name}$point${H_tagName}で${HtagComName_}伐採${H_tagComName}が行われました。",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が耐久力を$numアップしました。",$id);
	}
}

# 防衛施設、耐久力アップせず
sub logBombDurableMax {
	my($id, $name, $lName, $point, $hide) = @_;
	if ($hide) {
		logSecret("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>の耐久力はすでに最大です。",$id);
		logOut("こころなしか、${HtagName_}${name}${H_tagName}の<B>森</B>が増えたようです！",$id);
#		logOut("${HtagName_}${name}$point${H_tagName}で${HtagComName_}伐採${H_tagComName}が行われました。",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>の耐久力はすでに最大です。",$id);
	}
}

# 防衛施設、自爆セット
sub logBombSet {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>の<B>自爆装置がセット</B>されました。",$id);
}

# 防衛施設、自爆作動
sub logBombFire {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>、${HtagDisaster_}自爆装置作動！！${H_tagDisaster}",$id);
}

# 記念碑、発射
sub logMonFly {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が<B>轟音とともに飛び立ちました</B>。",$id);

}

# 記念碑、落下
sub logMonDamage {
	my($id, $name, $point) = @_;
	logOut("<B>何かとてつもないもの</B>が${HtagName_}${name}$point${H_tagName}地点に落下しました！！",$id);
}

# 植林orミサイル基地
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logOut("こころなしか、${HtagName_}${name}${H_tagName}の<B>森</B>が増えたようです。",$id);
}

# ハリボテ
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logLandSuc($id, $name, $comName2, $point);

}

# ミサイル撃とうとした(or 怪獣派遣しようとした)がターゲットがいない
sub logMsNoTarget {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標の${AfterName}に人が見当たらないため中止されました。",$id);
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標が見当たらないため中止されました。",$id);
}

# 艦隊への移動指令
sub logMoveMissionFleet {
	my($id, $tId, $name, $tName, $point, $no) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${no}艦隊${H_tagName}に対し${HtagName_}${tName}${point}${H_tagName}への${HtagComName_}移動指令${H_tagComName}を行いました。",$id, $tId);
}

# 艦隊への移動指令を解除
sub logMoveMissionFleetLift {
	my($id, $tId, $name, $tName, $point, $no) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${no}艦隊${H_tagName}に対し${HtagName_}${tName}${point}${H_tagName}への${HtagComName_}移動指令${H_tagComName}を${HtagDisaster_}解除${H_tagDisaster}しました。",$id, $tId);
}

# 艦艇への指令を変更
sub logChangeMission {
	my($id, $tId, $name, $tName, $point, $old, $new) = @_;
	my @status = ('通常', '退治', '巡航', '停船');
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}$point${H_tagName}で${HtagComName_}艦艇への指令変更${H_tagComName}を行いました。${HtagComName_}（$status[$old]→$status[$new]）${H_tagComName}",$id, $tId);
}

# 艦隊への指令を変更
sub logChangeMissionFleet {
	my($id, $tId, $name, $tName, $no, $new) = @_;
	my @status = ('通常', '退治', '巡航', '停船');
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}${H_tagName}で${HtagComName_}${no}艦隊への指令変更${H_tagComName}を行いました。${HtagComName_}（全艦艇$status[$new]モード）${H_tagComName}",$id, $tId);
}

# 艦艇への指令を変更しようとしたが失敗
sub logChangeMissionFail {
	my($id, $tId, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}${H_tagName}で行った${HtagComName_}艦艇への指令変更${H_tagComName}は、暗号のミスもしくは送信対象が艦艇でないため失敗しました。",$id, $tId);
}

# 一斉攻撃指令
sub logNavyMission {
	my($id, $tId, $name, $tName, $point, $nName, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}$point${H_tagName}の<B>$nName</B>に対する${HtagComName_}一斉攻撃${H_tagComName}を命令しました。<BR>　--- 指令傍受 ⇒ $str",$id, $tId);
}

# 一斉攻撃指令：失敗
sub logNavyMissionFail {
	my($id, $tId, $name, $tName, $point, $nName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が発令した${HtagName_}${tName}$point${H_tagName}の<B>$nName</B>に対する${HtagComName_}一斉攻撃${H_tagComName}は、失敗に終わりました。",$id, $tId);
}

# 艦艇攻撃、怪獣がミサイル攻撃(まとめ)
sub logNavyMatome {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $tLname, $kind, $str, $pntStr, $nId2) = @_;
	logOut("${HtagName_}${name}${nPoint}${H_tagName}の${HtagName_}${nName}${H_tagName}が${HtagName_}${tPoint}${H_tagName}地点の${tLname}に向けて${HtagComName_}$kind${H_tagComName}を行いました。${str}${pntStr}",$id, $nId, $nId2);
}

# 魚雷発射、その他の地形
sub logNavyTorpedoNormal {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は海の藻屑となりました。",$id, $nId);
}

# 艦砲射撃、艦載機で爆撃、怪獣がミサイル攻撃、防衛施設(耐久力あり)・コア(耐久力あり)・複合施設(規模ダウン)
sub logNavyNormalDefence {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は被害を受けました。",$id, $nId);
}

# 艦砲射撃、艦載機で爆撃、都市系
sub logNavyNormalTown {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint, $sName) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$sName</B>になりました。",$id, $nId);
}

# 艦砲射撃、艦載機で爆撃、その他の地形
sub logNavyNormal {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。一帯が壊滅しました。",$id, $nId);
}

# 魚雷発射、怪獣に命中、殺傷
sub logNavyTorpedoMonKill {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は力尽き、海底に${HtagDisaster_}倒れました${H_tagDisaster}。",$id, $nId, $mId);
}

# 艦砲射撃、艦載機で爆撃、怪獣がミサイル攻撃、怪獣に命中、殺傷
sub logNavyMonKill {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は力尽き、${HtagDisaster_}倒れました${H_tagDisaster}。",$id, $nId, $mId);
}

# 艦艇攻撃、残骸に命中、海の藻屑
sub logNavyWreckDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は海の藻屑となりました。",$id, $nId);
}

# 艦艇攻撃、怪獣がミサイル攻撃、軍港に命中、壊滅
sub logNavyPortDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は${HtagDisaster_}壊滅${H_tagDisaster}しました。",$id, $nId, $nId2);
}

# 艦艇攻撃、怪獣がミサイル攻撃、艦艇に命中、撃沈
sub logNavyShipDestroy {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は${HtagDisaster_}沈没${H_tagDisaster}しました。",$id, $nId, $nId2);
}

# 艦艇攻撃、怪獣がミサイル攻撃、怪獣に命中、ダメージ
sub logNavyMonster {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $mId, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は苦しそうに咆哮しました。",$id, $nId, $mId);
}

# 艦艇攻撃、怪獣がミサイル攻撃、艦艇に命中、ダメージ
sub logNavyDamage {
	my($id, $name, $nId, $nPoint, $nName, $tPoint, $nId2, $fName, $fPoint) = @_;
	logOut("　--- ${HtagName_}${fPoint}${H_tagName}の<B>$fName</B>に命中。<B>$fName</B>は黒煙を噴き出しました。",$id, $nId, $nId2);
}

# 怪獣の死体
sub logMonMoney {
	my($tId, $mName, $value) = @_;
	logOut("　--- <B>$mName</B>の残骸には、<B>$value$HunitMoney</B>の値が付きました。", $tId);
}

# ミサイル難民到着
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}${H_tagName}は快く受け入れたようです。",$id);
}

# 怪獣派遣
sub logMonsSend {
	my($id, $tId, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>人造怪獣</B>を建造。${HtagName_}${tName}${H_tagName}へ送りこみました。",$id, $tId);
}

# ST怪獣派遣
sub logMonsSendST {
	my($id, $tId, $name, $tName) = @_;
	logSecret("${HtagName_}${name}${H_tagName}が<B>人造怪獣</B>を建造。${HtagName_}${tName}${H_tagName}へ送りこみました。",$id);
	logLate("<B>何者か</B>が<B>人造怪獣</B>を建造。${HtagName_}${tName}${H_tagName}へ送りこみました。",$tId);
}

# 資金繰り
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 友好国設定
sub logAmity {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>$tName</B>を${HtagComName_}友好国と認定${H_tagComName}しました。",$id, $tId);
}

# 友好国解除
sub logAmityEnd {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>$tName</B>への${HtagComName_}友好国認定を破棄${H_tagComName}しました。",$id, $tId);
}

# 友好国解除失敗
sub logAmityEndFail {
	my($id, $name, $tId, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が実行しようとした<B>$tName</B>への${HtagComName_}友好国認定破棄${H_tagComName}は<B>艦隊派遣中のため許可されません</B>でした。",$id, $tId);
}

# 友好国最大数オーバー
sub logAmityMaxOver {
	my($id, $name, $tName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>$tName</B>への<B>友好国認定に失敗</B>しました${HtagComName_}（認定可能数違反）${H_tagComName}。",$id);
}

# 別の同盟を結成している
sub logLeaderAlready {
	my($id, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagName_}${tName}${H_tagName}の${HtagComName_}${comName}${H_tagComName}は、すでに自分の同盟を結成しているため中止されました。",$id);
}

# 別の同盟に加盟している
sub logOtherAlready {
	my($id, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagName_}${tName}${H_tagName}の${HtagComName_}${comName}${H_tagComName}は、すでに別の同盟に加盟しているため中止されました。",$id);
}

# 加盟
sub logAlly {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が『${HtagName_}${allyName}${H_tagName}』に${HtagNumber_}加盟${H_tagNumber}しました。", $id, $tId);
}

# 脱退
sub logAllyEnd {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}が『${HtagName_}${allyName}${H_tagName}』から${HtagDisaster_}脱退${H_tagDisaster}しました。", $id, $tId);
}

# 加盟可能最大数オーバー
sub logAllyMaxOver {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}の『${HtagName_}${allyName}${H_tagName}』への<B>加盟申請は破棄</B>されました${HtagComName_}（加盟可能数違反）${H_tagComName}。", $id, $tId);
}

# 加盟可能拒否
sub logAllyVeto {
	my($id, $tId, $name, $allyName) = @_;
	logOut("${HtagName_}${name}${H_tagName}の『${HtagName_}${allyName}${H_tagName}』への<B>加盟申請は破棄</B>されました${HtagComName_}（拒否権発動）${H_tagComName}。", $id, $tId);
}

# 輸出
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagFood_}$value$HunitFood${H_tagFood}の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}

# 輸入
sub logBuy {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagFood_}$value$HunitFood${H_tagFood}の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}

# 援助
sub logAid {
	my($id, $tId, $name, $tName, $comName, $str, $str2) = @_;
	logOut("${HtagName_}${name}${H_tagName}が${HtagName_}${tName}${H_tagName}へ$strの${HtagComName_}${comName}${H_tagComName}を行いました。(手数料:2割)",$id, $tId);
}

# 陣営外への援助（不許可）
sub logAidFail {
	my($id, $tId, $name, $tName, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagName_}${tName}${H_tagName}への${HtagComName_}${comName}${H_tagComName}は許可されていないため中止しました。",$id, $tId);
}

# 攻撃禁止
sub logNotAvail {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は許可されていないため中止しました。",$id);
}

# 開発期間のため失敗
sub logLandNG {
	my($id, $name, $comName, $cancel) = @_;
	logOut("${HtagName_}${name}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>$cancel</B>、実行できませんでした。",$id);
END
}

# 誘致活動
sub logPropaganda {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 放棄
sub logGiveup {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}は放棄され、<B>無人${AfterName}</B>になりました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、放棄され<B>無人${AfterName}</B>となる。");
}

# 無人化保護
sub logAutoKeep {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}の人口が減り<B>開発期間</B>に入りました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}が<B>開発期間に入る</B>。");
}

# 追放
sub logGiveup_no_do_fight {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}は規程数戦闘行為を行わなかったため、<B>敗退</B>しました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、規程数戦闘行為を行わなかったため、<B>敗退</B>。");
}

# 死滅
sub logDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}から人がいなくなり、<B>無人${AfterName}</B>になりました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、人がいなくなり<B>無人${AfterName}</B>となる。");
}

# 死滅(サバイバルモード・トーナメントモード)
sub logTDead {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}は、<B>沈没</B>し跡形もなくなりました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、<B>沈没</B>する。");
}

# 死滅回避(陣営モード・サバイバルモード・トーナメントモード)
sub logTDead2PD {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}は、沈没寸前に<B>戦線を離脱</B>しました。復興には時間がかかりそうです。【管理人あずかり】",$id);
	logHistory("${HtagName_}${name}${H_tagName}、<B>戦線を離脱</B>する。");
}

# 飢餓
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",$id);
}

# 艦艇(所属不明)現る
sub logNavyCome {
	my($id, $name, $nName, $point, $lName) = @_;
	logOut("${HtagName_}${name}${H_tagName}に所属不明の<B>$nName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>を移動しています。",$id);
}

# コア建設(ランダム)
sub logCoreRandomBuild {
	my($id, $name, $nName, $point, $lName) = @_;
	if($HcoreHide) {
		logSecret("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に<B>$nName</B>出現！！",$id);
		logOut("${HtagName_}${name}$point${H_tagName}に<B>$nName</B>出現！！",$id);
	} else {
		logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に<B>$nName</B>出現！！",$id);
	}
}

# 怪獣現る
sub logMonsCome {
	my($id, $name, $mName, $point, $lName) = @_;
	logOut("${HtagName_}${name}${H_tagName}に<B>$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>を移動しています。",$id);
}

# 怪獣動く
sub logMonsMove {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が<B>$mName</B>に踏み荒らされました。",$id, $mId);
}

# 巨大怪獣一部再生
sub logMonsRebody {
	my($id, $name, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}で<B>$mName</B>の体の一部が再生しました。",$id, $mId);
}

# 怪獣動く（海）
sub logMonsMoveSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>を<B>$mName</B>が移動しています。",$id, $mId);
}

# 怪獣、海軍を襲う
sub logMonsAttackNavy {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が<B>$mName</B>に襲われています。",$id, $mId);
}

# 怪獣、海の施設を破壊
sub logMonsBreakSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が<B>$mName</B>に襲われて破壊されました。",$id, $mId);
}

# 怪獣、防衛施設を踏む
sub logMonsMoveDefence {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("<B>$mName</B>が${HtagName_}${name}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}の自爆装置が作動！！</B>",$id, $mId);
}

# 艦艇動く
sub logNavyMoveSea {
	my($id, $name, $lName, $point, $mName, $mId) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>を<B>$mName</B>が航行しています。",$id, $mId);
}

# 艦艇体当たり
sub logNavyMoveAttack {
	my($id, $name, $nId, $nPoint, $nName, $nId2, $fPoint, $fName) = @_;
	logOut("${HtagName_}${name}$nPoint${H_tagName}の${HtagName_}${nName}${H_tagName}が${HtagName_}${fPoint}${H_tagName}地点の${HtagName_}${fName}${H_tagName}に${HtagComName_}体当たり！${H_tagComName}<B>$fName</B>もろとも${HtagDisaster_}沈没${H_tagDisaster}しました。",$id, $nId, $nId2);
}

# 陸地掘削
sub logNavyMoveDestroy {
	my($id, $name, $lName, $point, $mName, $mId, $mode) = @_;
	my $str = 'しようと';
	$str = '' if($mode);
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>を<B>$mName</B>が掘削航行${str}しています。",$id, $mId);
}

# 艦艇建造
sub logNavyBuild {
	my($id, $name, $nNo, $nName, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>${nNo}艦隊の${nName}</B>を建造。${HtagName_}$point${H_tagName}に配備しました。",$id);
}

# 艦隊派遣・帰還・移動
sub logNavySend {
	my($id, $fId, $tId, $name, $tName, $fleet, $fSend) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>${fleet}</B>を${HtagName_}${tName}${H_tagName}${fSend}しました。",$id, $fId, $tId);
}

# 艦隊派遣・帰還・移動の艦艇ログ
sub logNavySendShip {
	my($id, $tId, $str, $fSend) = @_;
	logOut("　--- ${fSend}地点 ⇒ $str",$id, $tId);
}

# 艦隊派遣・帰還・移動しようとしたが艦艇なし
sub logNavySendNone {
	my($id, $name, $tName, $fleet, $fSend) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>${fleet}</B>を${HtagName_}${tName}${H_tagName}${fSend}しようとしましたが、実行可能な艦隊がありませんでした。",$id);
}

# 艦隊派遣・帰還・移動しようとしたが失敗
sub logNavySendNoArea {
	my($id, $name, $tName, $fleet, $fSend, $str) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>${fleet}</B>を${HtagName_}${tName}${H_tagName}${fSend}しようとしましたが、失敗しました。$str",$id);
}

# 艦隊編成
sub logNavyForm {
	my($id, $name, $point, $fleet, $old, $new) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>は${old}艦隊から${new}艦隊に所属を変更しました。",$id);
}

# 艦隊編成しようとしたが失敗
sub logNavyFormFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を艦隊編成することはできません。",$id);
}

# 艦隊編成 １艦隊あたりの保有艦艇数オーバーによる失敗
sub logNavyFormMaxOver {
	my($id, $name, $point, $fleet, $old, $new) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の${old}艦隊所属<B>${fleet}</B>は艦隊編成できませんでした。(${new}艦隊の艦艇保有数オーバー)",$id);
}

# 目標艦指定
sub logNavyTarget {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>は、民間に払い下げられました。",$id);
}

# 目標艦指定しようとしたが失敗
sub logNavyTargetFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を除籍することはできません。",$id);
}

# 艦艇破棄
sub logNavyDestroy {
	my($id, $name, $point, $fleet, $tId) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を破棄しました。",$id, $tId);
}

# 艦艇破棄しようとしたが失敗
sub logNavyDestroyFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を破棄することはできません。",$id);
}

# 残骸修理
sub logNavyWreckRepair {
	my($id, $name, $point, $fleet, $cost, $nName) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を${cost}${HunitMoney}で修理。<B>$nName</B>に配備しました。",$id);
}

# 残骸修理しようとしたが失敗
sub logNavyWreckRepairFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を修理することはできません。",$id);
}

# 残骸修理 １艦隊あたりの艦艇保有数オーバーによる失敗
sub logNavyWreckRepairMaxOver {
	my($id, $name, $point, $fleet, $nName) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を修理することはできません。(${nName}の艦艇保有数オーバー)",$id);
}

# 残骸売却
sub logNavyWreckSell {
	my($id, $name, $point, $fleet, $cost) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を${cost}${HunitMoney}で売却しました。",$id);
}

# 残骸売却しようとしたら金塊発見
sub logNavyWreckSellLucky {
	my($id, $name, $point, $fleet, $cost) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を引き上げたところ、${cost}${HunitMoney}の<B>金塊</B>が発見されました！",$id);
}

# 残骸売却しようとしたが失敗
sub logNavyWreckSellFail {
	my($id, $name, $point, $fleet) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${fleet}</B>を売却することはできません。",$id);
}

# 艦艇修理
sub logNavyShipRepair {
	my($id, $name, $tId) = @_;
	logOut("<B>修理状況</B>(於：${HtagName_}${name}${point}${H_tagName})",$id,$id,$tId);
}

# 艦艇修理
sub logNavyShipRepairM {
	my($id, $tId, $str) = @_;
	my($name) = islandName($Hislands[$HidToNumber{$tId}]) if (defined $HidToNumber{$tId});
	logOut("　 ${HtagName_}${name}${point}${H_tagName}所属艦艇 ⇒ $strが修理を行いました。",$id,$tId);
}

# 艦艇が補給不足
sub logNavyShipSupplyFailM {
	my($id, $tId, $str) = @_;
	my($name) = islandName($Hislands[$HidToNumber{$tId}]) if (defined $HidToNumber{$tId});
	logOut("　 ${HtagName_}${name}${point}${H_tagName}所属艦艇 ⇒ $strの補給物資が不足しています。",$id,$tId);
}

# 火災
sub logFire {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}火災${H_tagDisaster}により${HtagDisaster_}壊滅${H_tagDisaster}しました。",$id);
}

# 埋蔵金
sub logMaizo {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>$value$HunitMoneyもの埋蔵金</B>が発見されました。",$id);
}

# 地震発生
sub logEarthquake {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}で大規模な${HtagDisaster_}地震${H_tagDisaster}が発生！！",$id);
}

# 地震被害
sub logEQDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により${HtagDisaster_}壊滅${H_tagDisaster}しました。",$id);
}

# 食料不足被害
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は${HtagDisaster_}壊滅${H_tagDisaster}しました。",$id);
}

# 津波発生
sub logTsunami {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}付近で${HtagDisaster_}津波${H_tagDisaster}発生！！",$id);
}

# 津波被害
sub logTsunamiDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}により崩壊しました。",$id);
}

# 津波被害(艦艇にダメージ)
sub logTsunamiDamageNavy {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}によりダメージをうけました。",$id);
}

# 津波被害(艦艇沈没)
sub logTsunamiDamageNavyDestroy {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}により${HtagDisaster_}沈没${H_tagDisaster}しました。",$id);
}

# 台風発生
sub logTyphoon {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}に${HtagDisaster_}台風${H_tagDisaster}上陸！！",$id);
}

# 台風被害
sub logTyphoonDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}台風${H_tagDisaster}で飛ばされました。",$id);
}

# 隕石、海
sub logMeteoSea {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下しました。",$id);
}

# 隕石、山
sub logMeteoMountain {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は消し飛びました。",$id);
}

# 隕石、海底基地
sub logMeteoSbase {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は崩壊しました。",$id);
}

# 隕石、怪獣
sub logMeteoMonster {
	my($id, $name, $lName, $point) = @_;
	logOut("<B>$lName</B>がいた${HtagName_}${name}$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、陸地は<B>$lName</B>もろとも水没しました。",$id);
}

# 隕石、怪獣（潜水中）
sub logMeteoMonsterSea {
	my($id, $name, $lName, $point) = @_;
	logOut("<B>$lName</B>がいた${HtagName_}${name}$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、水中にいた<B>$lName</B>は消し飛びました。",$id);
}

# 隕石、浅瀬
sub logMeteoSea1 {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、海底がえぐられました。",$id);
}

# 隕石、その他
sub logMeteoNormal {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}地点の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、一帯が水没しました。",$id);
}

# 隕石、その他
sub logHugeMeteo {
	my($id, $name, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}地点に${HtagDisaster_}巨大隕石${H_tagDisaster}が落下！！",$id);
}

# 噴火
sub logEruption {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}地点で${HtagDisaster_}火山が噴火${H_tagDisaster}、<B>山</B>が出来ました。",$id);
}

# 噴火、怪獣(深い海)
sub logEruptionSea3 {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}地点の<B>$lName</B>がいる<B>海</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で海底が隆起、浅瀬になりました。",$id);
}

# 噴火、怪獣(浅瀬)
sub logEruptionSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で海底が隆起、海上に出現しました。",$id);
}

# 噴火、浅瀬
sub logEruptionSea1 {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で陸地になりました。",$id);
}

# 噴火、海or海基
sub logEruptionSea {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で海底が隆起、浅瀬になりました。",$id);
}

# 噴火、その他
sub logEruptionNormal {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で${HtagDisaster_}壊滅${H_tagDisaster}しました。",$id);
}

# 地盤沈下発生
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",$id);
}

# 地盤沈下被害
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",$id);
}

# 広域被害、水没
sub logWideDamageSea {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は<B>水没</B>しました。",$id);
}

# 広域被害、海の建設
sub logWideDamageSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は跡形もなくなりました。",$id);
}

# 広域被害、怪獣水没
sub logWideDamageMonsterSea {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の陸地は<B>$lName</B>もろとも水没しました。",$id);
}

# 広域被害、怪獣水没（潜水中）
sub logWideDamageMonsterSea2 {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の水中にいた<B>$lName</B>は消し飛びました。",$id);
}

# 広域被害、怪獣
sub logWideDamageMonster {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は消し飛びました。",$id);
}

# 広域被害、荒地
sub logWideDamageWaste {
	my($id, $name, $lName, $point) = @_;
	logOut("　･･･ ${HtagName_}$point${H_tagName}の<B>$lName</B>は一瞬にして<B>荒地</B>と化しました。",$id);
}

# 受賞
sub logPrize {
	my($id, $name, $pName, $money) = @_;
	my $str = ($money) ? "(賞金：${money}${HunitMoney})" : "";
	logOut("${HtagName_}${name}${H_tagName}が<B>$pName$str</B>を受賞しました。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、<B>$pName$str</B>を受賞");
}

# 陣営消滅
sub logCampDelete {
	my($name) = @_;
	logHistory("${HtagName_}${name}${H_tagName}は、滅亡しました。");
}

# 陣営消滅(死滅回避)
sub logCampPreDelete {
	my($name) = @_;
	logHistory("${HtagName_}${name}${H_tagName}は、完全に沈黙しました。");
}

# 竣工
sub logshunkou {
	my($id, $name, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で<B>${kind}</B>の工期が終了。${HtagName_}${point}${H_tagName}で竣工しました。",$id);
}

# 帰投ログまとめ
sub logkitouMatome {
	my($id, $name, $kind, $point) = @_;
	logOut("${HtagName_}${name}${H_tagName}で${HtagComName_}${kind}${H_tagComName}が帰投しました。<br>　　<B>⇒</B> $point",$id);
}

# 資源採掘(海上採掘基地)
sub logResourceS {
	my($id, $nId, $name, $kind, $kind2, $point, $point2, $arg) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${kind}(${name})</B>が${HtagName_}${point2}${H_tagName}地点の<B>${kind2}</B>で資源を採集。${HtagMoney_}${arg}$HunitMoney${H_tagMoney}相当の収益がありました。",$id, $nId);
}

# 資源採掘(定置網)
sub logResourceF {
	my($id, $nId, $name, $kind, $kind2, $point, $point2, $arg) = @_;
	logOut("${HtagName_}${name}${point}${H_tagName}の<B>${kind}(${name})</B>が${HtagName_}${point2}${H_tagName}地点の<B>${kind2}</B>で資源を採集。${HtagFood_}${arg}$HunitFood${H_tagFood}相当の収益がありました。",$id, $nId);
}

# 航空機発進
sub logNavyBuild2 {
	my($id, $name, $nNo, $nName, $point, $tId) = @_;
	logOut("${HtagName_}${name}${H_tagName}が<B>${nNo}艦隊の${nName}</B>を発進。${HtagName_}$point${H_tagName}上空に配備しました。",$id, $tId);
}

# 軍港払下げ
sub logSellPort {
	my($id, $tName, $point, $fleet, $tId) = @_;
	logOut("${HtagName_}${tName}${point}${H_tagName}の<B>${fleet}</B>は、民間に払い下げられました。",$id, $tId);
}

# 軍港買収
sub logBuyPort {
	my($id, $name, $point, $fleet, $tId, $tName) = @_;
	logOut("${HtagName_}${tName}${point}${H_tagName}の<B>${fleet}</B>は${HtagName_}${name}${H_tagName}に編入されました。",$id, $tId);
}

# 貿易
sub logTrade {
	my($id, $tId, $name, $nName, $value, $value2, $tmp, $point) = @_;
	logOut("${HtagName_}${name}$point${H_tagName}の<B>豪華客船タイタニック(${nName})</B>が貿易を開始。食料${HtagFood_}$value$HunitFood${H_tagFood}を${HtagMoney_}$value2$HunitMoney${H_tagMoney}で$tmpしました。",$id, $tId);
}

# デバッグ
sub logdebug {
        my($id, $tmp) = @_;
	logOut("$tmp", $id);
}

# 人口その他の値を算出
sub estimate {
	my($number) = $_[0];
	my($island, $fkind);

	# 地形を取得
	$island = $Hislands[$number];
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island2->{'landValue'};
	my($map) = $island->{'map'};

	# 初期化
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

	# 数える
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
					# 町
					$island->{'pop'} += $value;
				} elsif($kind == $HlandFarm) {
					# 農場
					$island->{'farm'} += $value;
				} elsif($kind == $HlandFactory) {
					# 工場
					$island->{'factory'} += $value;
				} elsif($kind == $HlandMountain) {
					# 山
					$island->{'mountain'} += $value;
				} elsif($kind == $HlandComplex) {
					# 複合地形
					my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($value);
					$island->{$HcomplexTPkind[$cKind]} += $cTurn * $HcomplexTPrate[$cKind] if(defined $HcomplexTPkind[$cKind]);
					$island->{$HcomplexFPkind[$cKind]} += $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
					$island->{$HcomplexMPkind[$cKind]} += $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
					$island->{'complex'}[$cKind]++;
					$island->{'area'}-- if($HcomplexAttr[$cKind] & 0x300);
				} elsif(($kind == $HlandMonster) || ($kind == $HlandHugeMonster)) {
					# 海にいる怪獣は陸地にカウントしない
					my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($value);
					$island->{'area'}-- if ($mFlag & 2);
				} elsif ($kind == $HlandNavy) {
					my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
					my $nSpecial = $HnavySpecial[$nKind];
					my $n = $HidToNumber{$nId};
					$Hislands[$n]->{'shipk'}[$nKind]++ if(defined $n);
					if ($nSpecial & 0x8) {
						# 港
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
						    # 艦艇なら陸地にカウントしない
						    $island->{'area'}--;
                                                }
					}
				} elsif($kind == $HlandDefence) {
					$island->{'dbase'}++;
				} elsif($kind == $HlandCore) {
					$island->{'core'}++;
					$island->{'area'}-- if(int($value / 10000) >= 1);
			        } elsif($kind == $HlandResource) {
                                    # 資源系
                                    my($temp, $kind, $turn, $food, $money) = landUnpack($value);
                                    if($kind == 0){
				        $island->{'stone'}++;
                                    }else{
                                        $island->{'fish'}++;
                                    }
				    $island->{'area'}--;
				}
			} elsif($kind == $HlandBouha) {
				$island->{'bouha'}++; # 防波堤をカウント
			} elsif($kind == $HlandSeaMine) {
				$island->{'mine'}++; # 機雷をカウント
			} elsif($kind == $HlandOil) {
				$island->{'oil'}++; # 油田をカウント(発見確率を下げる)
			} elsif($kind == $HlandSea && !$value) {
				$island->{'sea'}++; # 深い海をカウント
			}
		}
	}

}

# ポイント算出
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

# 範囲内の地形を数える
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];

		if(($sx < 0) || ($sy < 0)){
			# 範囲外の場合
			# 海に加算
			$sea++;
		} elsif($list[$land->[$sx][$sy]]) {
			# 範囲内の場合
			$count++;
		}
	}
	$count += $sea if($list[$HlandSea]); # 海なら加算
	return $count;
}

# 範囲内の複合地形(属性)を数える
sub countAroundComplex {
	my($island, $x, $y, $range, $attr) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外
		next if(($sx < 0) || ($sy < 0));

		# 範囲内の場合
		if($land->[$sx][$sy] == $HlandComplex) {
			my $cKind = (landUnpack($landValue->[$sx][$sy]))[1];
			if($HcomplexAttr[$cKind] & $attr) {
				$count++;
			}
		}
	}
	return $count;
}

# 範囲内の防衛施設、艦艇をみつける
sub countAroundDef {
	my($id, $island, $x, $y, $special, @oId, $cflag) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($range, $sx, $sy, %idFlag);
	# @oIdに入っているID(攻撃側ID)は無視
	foreach (@oId) {
		$idFlag{$_} = 1;
	}

	my($count) = 0;
	$range = ($HdefLevelUp) ? $an[3] : $an[2];
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		if($_ < $an[2]) { # ２ヘックス防衛
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
		} elsif((!$idFlag{$id}) && ($land->[$sx][$sy] == $HlandDefence)) { # ３ヘックス防衛の防衛施設
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

# 範囲内の海上にいる怪獣を数える
sub countAroundMonster {
	my($island, $x, $y, $range) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		if(($land->[$sx][$sy] == $HlandMonster) || ($land->[$sx][$sy] == $HlandHugeMonster)) {
			my $nFlag = (monsterUnpack($landValue->[$sx][$sy]))[4];
			$count++ if($nFlag & 2);
		}
	}
	return $count;
}

# 範囲内の艦艇を数える
sub countAroundNavy {
	my($island, $x, $y, $range) = @_;
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($count, $sx, $sy);
	$count = 0;
	$range--;
	foreach(0..$range) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[7];
			my $nSpecial = $HnavySpecial[$nKind];
			$count++ unless ($nSpecial & 0x8);
		}
	}
	return $count;
}

# 範囲内の特殊艦艇を数える
sub countAroundNavySpecial {
	my($island, $x, $y, $special, $range, @id) = @_;
	# @idのみカウント($idに'0'がある場合はすべてをカウント)
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nFlag, $nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[0, 5, 7];
			my $nSpecial = $HnavySpecial[$nKind];


			$count++ if(($nSpecial & $special) && ($idFlag{'0'} || $idFlag{$nId}) && ($nFlag != 3));
		}
	}
	return ($count);
}

# 範囲内の防波能力艦艇を数える
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nKind) = (navyUnpack($landValue->[$sx][$sy], $landValue2->[$sx][$sy]))[0, 7];
			my $special = $HnavySpecial[$nKind];
			return 1 if(($special & 0x8000000) && ($_ < $an[$HbouhaHex[$nKind]]));
		}
	}
	return 0;
}


# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# 初期値
	$n = 1 if($n <= 0);
	@list = (0..$n-1);

	# シャッフル
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		next if($i == $j);
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

#------------------------------------------------
# トーナメントモード
#------------------------------------------------
# 対戦の記録ログ
sub fightlog {
	# 保存ディリクトリのチェック
	if(!opendir(DIN, "${HfightdirName}/")) {
		mkdir("${HfightdirName}", $HdirMode);
	} else {
		closedir(DIN);
	}

	# 回戦数数代入 決勝戦の場合99にする
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

# 勝利ログ
sub logWin {
	my($id, $name, $str, $money, $ino) = @_;
	my $fTurn = $HislandFightCount + 1;
	if($ino <= 2) {
		$fTurn = '決勝戦';
	} elsif($ino <= 4) { 
		$fTurn = '準決勝';
	} else {
		$fTurn .= '回戦';
	}
	if($ino < 2) {
		logOut("${HtagName_}${name}${H_tagName}${str}し、<B>優勝！！</B>",$id);
		logHistory("${HtagName_}${name}${H_tagName}、<B>優勝！！</B>");
	} elsif($money == 0) {
		logOut("${HtagName_}${name}${H_tagName}${str}し、<B>$fTurn進出！</B>",$id);
	} else {
		logOut("${HtagName_}${name}${H_tagName}${str}し、<B>$fTurn進出！　$money$HunitMoney</B>の報酬金が支払われました。",$id);
	}
}

# 敗退
sub logLose {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}、<B>敗退</B>。",$id);
}

# 予選落ち
sub logLoseOut {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}${H_tagName}、<B>予選落ち</B>。",$id);
	logHistory("${HtagName_}${name}${H_tagName}、<B>予選落ち</B>。");
}

# 沈没時の対戦相手データ処理
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
				logWin($tIsland->{'id'}, islandName($tIsland), "圧勝！", $reward, $winIslandNumber);
				$tIsland->{'fight_id'} = -2;
			}
			# 各種の値を計算
			estimate($tn);
		} else {
			# 決勝ならどうせ相手の勝ちなので、回戦の開発停止処理
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