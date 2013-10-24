# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 新規作成モジュール(ver1.00)
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
# 島の新規作成モード
#----------------------------------------------------------------------
# メイン
sub newIslandMain {
	my($mode) = @_;
	# 不正アクセスをチェック
	if($HadminJoinOnly) {
		unless($ENV{HTTP_REFERER}  =~ /^$HthisFile/) {
			unlock();
			tempHeader();
			tempNoReferer();
			return 0;
		}
	}
	# 島がいっぱいでないかチェック
	if(
		($HislandNumber - $HbfieldNumber >= $HmaxIsland) ||
		($HsurvivalTurn && ($HislandTurn >= $HsurvivalTurn)) # サバイバルモード
		) {
		unlock();
		tempHeader();
		tempNewIslandFull();
		return 0;
	}

	# 島名があるかチェック
	if($HcurrentName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoName();
		return 0;
	}

	# オーナー名があるかチェック
	if($HcurrentOwnerName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoOwnerName();
		return 0;
	}

	# 島名が正当かチェック
	if($HcurrentName =~ /[,\?\(\)\<\>\$]|^無人|^沈没$/) {
		# 使えない名前
		unlock();
		tempHeader();
		tempNewIslandBadName();
		return 0;
	}

	# オーナー名が正当かチェック
	if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
		# 使えない名前
		unlock();
		tempHeader();
		tempNewIslandBadOwnerName();
		return 0;
	}

	# 陣営を決定
	my($campNum);
	if($HarmisticeTurn && ($HallyNumber > 1)) {
		if($HcampSelectRule != 2 || $HcampNumber == -1) {
			$campNum = selectCamp();
		} else {
			$campNum = $HcampNumber;
			if ($Hally[$campNum]->{'number'} >= ($HmaxIsland / $HallyNumber)) {
				# その陣営は満杯
				unlock();
				tempHeader();
				tempNewIslandFull();
				return 0;
			}
		}
	}
	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
		# すでに発見ずみ
		unlock();
		tempHeader();
		tempNewIslandAlready();
		return 0;
	}

	# passwordの存在判定
	if($HinputPassword eq '') {
		# password無し
		unlock();
		tempHeader();
		tempNewIslandNoPassword();
		return 0;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempHeader();
		tempWrongPassword();
		return 0;
	}

	# IDの使い回し
	my $safety = 100;
	while(defined $HidToNumber{$HislandNextID}) {
		$HislandNextID ++;
		$HislandNextID = 1 if($HislandNextID > 100);
		last if(!$safety--);
	}

	# ログファイル調整
	logFileAdjust(-1, $HislandNextID);

#	readIslandsFile(-3);
	# 地形データ、掲示板調整
	islandFileAdjust(-1, $HislandNextID);

	# 新しい島の番号を決める
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$islandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland($mode);
	my($island) = $Hislands[$HcurrentNumber];

	# 各種の値を設定
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
	# 人口その他算出
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

	# データ書き出し
	$HidToNumber{$island->{'id'}} = $HcurrentNumber;
	islandSort($HrankKind, 1);
	if($HarmisticeTurn) {
		allyOccupy();
		allySort();
	}
	writeIslandsFile($island->{'id'});
	$HcurrentNumber = $HidToNumber{$island->{'id'}};
	$HcurrentName = islandName($island);
	logDiscover($HcurrentName, $HcurrentOwnerName); # ログ

	$HcurrentID = $HislandNextID - 1;
	$HmainMode = 'owner';
	$HjavaMode = 'java';

	return 1 if($mode);
	# COOKIE出力
	cookieOutput();

	# 開放
	unlock();

	# 発見画面
	tempHeader();
	tempNewIslandHead($HcurrentName); # 発見しました!!
	islandInfo(); # 島の情報
	islandMap(1); # 島の地図、ownerモード
}

# 島数が最も少なく、順位が最下位の陣営
sub selectMinCamp {
	my($i, $num) = (0, 0);
	for ($i = 1; $i < $HallyNumber; $i++) {
		if ($Hally[$i]->{'number'} <= $Hally[$num]->{'number'}) {
			$num = $i;
		}
	}
	return $num;
}

# ランダム("合計の島数/陣営の数+1"まで)
sub selectRandomCamp {
	return 0 if(!$HallyNumber);
	my($i, $j, $ave, $iave, @array, $len);
	# 空き陣営配列の作成
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

# 陣営の選択ルーチン(設定により変化)
sub selectCamp {
	if ($HcampSelectRule == 0) {
		return selectMinCamp();
	} elsif ($HcampSelectRule == 1) {
		return selectRandomCamp();
	} else {
		# どこでも良いを選択
		return selectRandomCamp();
	}
}
#---------------------------------------------------------------------
#	ファイル調整
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
					# 海軍なら
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
		# データ書き出し
		writeIsland($tIsland, $tId, 0) if($writeflag);
	}
}

#---------------------------------------------------------------------
# 新しい島を作成する
#---------------------------------------------------------------------
sub makeNewIsland {
	my($mode) = @_;
	# 海域座標
	my($wmap, $map);
	if($HoceanMode) {
		if(($HoceanSelect || $HmainMode eq 'bfield' || $HmainMode eq 'isetup') &&
			!$HmapRandom && $HoceanMapX ne '' && $HoceanMapY ne '' && !$HoceanMap[$HoceanMapX][$HoceanMapY]) {
			$wmap = { 'x' => $HoceanMapX, 'y' => $HoceanMapY };
		} else {
			$wmap = randomIslandMap(); # 島の座標を決める
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
	# マップ配列
	my @x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
	my @y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
	$map = { 'x' => \@x, 'y' => \@y };
	# 地形を作る
	my($land, $landValue) = makeNewLand($wmap, $map, $mode);

	# 初期コマンドを生成
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

	# 初期掲示板を作成
	my @lbbs = ();

	# 撃沈数カウンターセット
	my $n = @HnavyName;
	my(@navy) = ((0)x$n);

	# 拡張データセット
	my(@ext) = ((0)x11); # 0〜10
	# 拡張サブデータセット
	# extの勝利フラグ[0]をターンに変えて、最後に退治数[11],報奨金[12]を追加。
	my(@subExt) = ($HislandTurn, (0)x12); # 0〜12

	# 天候初期値
	my(@weather) = (20,1000,60,0,0,0,0);
	for($i = 0; $i < 4; $i++) {
		 push(@weather,'2');
	}

	# 島にして返す
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

# (0,0)から(7, 7)までの数字が一回づつ出てくるように
# (@rpx, @rpy)を設定
sub makeRandomEightArray {
	undef @rpx;
	undef @rpy;
	# 初期値
	@rpx = (0..7) x 8;
	foreach (0..7) {
		push(@rpy, ($_) x 8);
	}
	# シャッフル
	for ($i = 64; --$i; ) {
		my($j) = int(rand($i+1)); 
		next if($i == $j);
		@rpx[$i,$j] = @rpx[$j,$i];
		@rpy[$i,$j] = @rpy[$j,$i];
	}
}

# 新しい島の地形を作成する
sub makeNewLand {
	my($wmap, $map, $mode) = @_;
	# 基本形を作成
	my(@land, @landValue, $x, $y, $i);
	if($HoceanMode) {
		@land = @{$Hworld->{'land'}};
		@landValue = @{$Hworld->{'landValue'}};
	}
	# 海に初期化
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$land[$x][$y] = $HlandSea;
			$landValue[$x][$y] = 0;
		}
	}
	return (\@land, \@landValue) if($mode);
	# 中央の4*4に荒地(平地)を配置
	my($centerX) = $wmap->{'x'}*$HislandSizeX + int($HislandSizeX / 2) - 1;
	my($centerY) = $wmap->{'y'}*$HislandSizeY + int($HislandSizeY / 2) - 1;
	for($y = $centerY - 1; $y < $centerY + 3; $y++) {
		for($x = $centerX - 1; $x < $centerX + 3; $x++) {
			$land[$x][$y] = (!$HnewIslandSetting) ? $HlandWaste : $HlandPlains;
		}
	}
	my($count);
	if(!$HnewIslandSetting) {
		# 8*8範囲内に陸地を増殖
		foreach $i (1..120) {
			# ランダム座標
			$x = random(8) + $centerX - 3;
			$y = random(8) + $centerY - 3;

			if(countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7){
				# 周りに陸地がある場合、浅瀬にする
				# 浅瀬は荒地にする
				# 荒地は平地にする
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
		# 平地を作る
		makeRandomEightArray();
		$count = 0;
		$HcountLandArea -= 16;
		foreach $i (0..63) {
			last if($count >= $HcountLandArea);
			# ランダム座標
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# そこが海でかつ周囲に陸があれば、平地を作る
			if(($land[$x][$y] == $HlandSea) && (countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7)) {
				$land[$x][$y] = $HlandPlains;
				$landValue[$x][$y] = 0;
				$count++;
			}
		}

		# 浅瀬を作る
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandSea);
			# ランダム座標
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# そこが海でかつ周囲に陸があれば、浅瀬を作る
			if(($land[$x][$y] == $HlandSea) && !$landValue[$x][$y] && (countAroundforMake(\@land, $x, $y, 7, $HlandSea) != 7)) {
				$landValue[$x][$y] = 1;
				$count++;
			}
		}

		# 荒地を作る
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandWaste);
			# ランダム座標
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# そこがすでに平地なら、荒地を作る
			if($land[$x][$y] == $HlandPlains) {
				$land[$x][$y] = $HlandWaste;
				$count++;
			}
		}
	}

	# 町を作る
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandTown);
		# ランダム座標
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# そこが平地なら、町を作る
		if($land[$x][$y] == $HlandPlains) {
			$land[$x][$y] = $HlandTown;
			$landValue[$x][$y] = $HvalueLandTown; # 最初は500人
			$count++;
		}
	}

	# 森を作る
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandForest);
		# ランダム座標
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# そこが平地なら、森を作る
		if($land[$x][$y] == $HlandPlains) {
#			$land[$x][$y] = $HlandForest;
#			$landValue[$x][$y] = $HvalueLandForest; # 最初は500本
			# 複合地形(森)
			$land[$x][$y] = $HlandComplex;
			$landValue[$x][$y] = landPack(0, 2, 1, 0, 0); # 最初は100本
			$count++;
		}
	}

	# 山を作る
#	makeRandomEightArray();
#	$count = 0;
#	foreach $i (0..63) {
#		last if($count >= $HcountLandMountain);
#		# ランダム座標
#		$x = $rpx[$i] + $centerX - 3;
#		$y = $rpy[$i] + $centerY - 3;
#
#		# そこが平地なら、山を作る
#		if($land[$x][$y] == $HlandPlains) {
#			$land[$x][$y] = $HlandMountain;
#			$landValue[$x][$y] = $HvalueLandMountain; # 最初は採掘場なし
#			$count++;
#		}
#	}

	# 軍港を作る
	makeRandomEightArray();
	$count = 0;
	foreach $i (0..63) {
		last if($count >= $HcountLandPort);
		# ランダム座標
		$x = $rpx[$i] + $centerX - 3;
		$y = $rpy[$i] + $centerY - 3;

		# そこが浅瀬なら、軍港を作る
		if(($land[$x][$y] == $HlandSea) && $landValue[$x][$y]) {
			$land[$x][$y] = $HlandNavy;
			$landValue[$x][$y] = navyPack($HislandNextID, 0, 0, 0, 0, 0, 0, 0, $HnavyHP[0]);
			$count++;
		}
	}

	if ($HuseBase) {
		# 基地を作る
		makeRandomEightArray();
		$count = 0;
		foreach $i (0..63) {
			last if($count >= $HcountLandBase);
			# ランダム座標
			$x = $rpx[$i] + $centerX - 3;
			$y = $rpy[$i] + $centerY - 3;

			# そこが平地なら、基地
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
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
	# idから島を取得
	readIsland
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# パスワードチェック
	if(checkSpecialPassword($HoldPassword)) {
		# 特殊パスワード
		if($HcurrentName =~ /^ログ$/) {
			# 最近の出来事強制出力
			logPrintHtml();
			unlock();
			tempChange();
			return;
		} elsif($HcurrentName =~ /^無人$/) {
			# 島削除モード
			deleteIsland(1);
			return;
		} elsif($HcurrentName =~ /^沈没$/) {
			# 島削除モード
			deleteIsland(0);
			return;
		} elsif(!checkMasterPassword($HoldPassword)) {
			# 食糧/資金maxモード
			$island->{'money'} = $HmaximumMoney;
			$island->{'food'}  = $HmaximumFood;
			$flag = 1;
		}
	} elsif(!checkPassword($island,$HoldPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# 島名変更の場合	
		# 島名が正当かチェック
		if($HcurrentName =~ /[,\?\(\)\<\>\$]|^無人|^沈没$/) {
			# 使えない名前
			unlock();
			tempNewIslandBadName();
			return;
		}

		# 名前の重複チェック
		if(nameToNumber($HcurrentName) != -1) {
			# すでに発見ずみ
			unlock();
			tempNewIslandAlready();
			return;
		}

		# 代金
		unless(checkSpecialPassword($HoldPassword)) {
			if($island->{'money'} < $HcostChangeName) {
				# 金が足りない
				unlock();
				tempChangeNoMoney();
				return;
			}
			$island->{'money'} -= $HcostChangeName;
		}

		# 名前を変更
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
		my $n = $HidToAllyNumber{$HcurrentID};
		if(defined $n) {
			$Hally[$n]->{'oName'} = $HcurrentName;
		}
	}

	if ($HcurrentOwnerName ne '') {
		# オーナー名変更の場合
		# オーナー名が正当かチェック
		if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
			# 使えない名前
			unlock();
			tempNewIslandBadOwnerName();
			return;
		}

		# 代金
		unless(checkSpecialPassword($HoldPassword)) {
			if($island->{'money'} < $HcostChangeName) {
				# 金が足りない
				unlock();
				tempChangeNoMoney();
				return;
			}
			$island->{'money'} -= $HcostChangeName;
		}

		# 名前を変更
		logChangeOwnerName($island->{'name'}, $HcurrentOwnerName);
		$island->{'owner'} = $HcurrentOwnerName;
		$flag = 1;
	}

	# password変更の場合
	if($HinputPassword ne '') {
		# パスワードを変更
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
		my $n = $HidToAllyNumber{$HcurrentID};
		if(defined $n) {
			$Hally[$n]->{'password'} = encode($HinputPassword);
		}
	}

	if($flag == 0) {
		# どちらも変更されていない
		unlock();
		tempChangeNothing();
		return;
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);
	unlock();

	# 変更成功
	tempChange();
}

#----------------------------------------------------------------------
# 新しい島を探す
#----------------------------------------------------------------------
# メイン
sub newIslandTop {
	# 開放
	unlock();

	# 管理人だけが新しい島を探せる？
	if ($HadminJoinOnly) {
		# マスタパスワードチェック
		unless (checkMasterPassword($HinputPassword)) {
			# password間違い
			tempWrongPassword();
			return;
		}
	}
	
	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='newIsland'>
$HPoliciesDisclaimers
<H1>新しい${AfterName}を探す</H1>
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
海域座標を指定して下さい<BR>座標（
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
</SELECT>）　<INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>ランダム<BR><BR>
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
陣営名を選択して下さい<BR>
<SELECT NAME="CAMPNUMBER">
$allyList
<OPTION VALUE=\"-1\">どこでも良い
</SELECT><BR>
END
		}
		
		$HjoinNewIslandButton = '探しに行く' if(!$HjoinNewIslandButton);
		out(<<END);
どんな名前をつける予定？<small>(全角${HlengthIslandName}字まで)</small><BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>${AfterName}<BR>
あなたの名前は？<small>(全角${HlengthOwnerName}字まで)</small><BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32 class=f><BR>
<BR>
<INPUT TYPE="submit" VALUE="$HjoinNewIslandButton" NAME="NewIslandButton">
</FORM>
</DIV>
END
	} else {
	out(<<END);
		${AfterName}の数が最大数です・・・現在登録できません。
</DIV>
END
	}
}

#----------------------------------------------------------------------
# 島の名前とパスワードの変更
#----------------------------------------------------------------------
# メイン
sub renameIslandMain {
	# 開放
	unlock();

	my($str);
	$str = '<BR>　また、「陣営パスワード」では、パスワードの変更はできません。' if($HarmisticeTurn);
	$str = '<BR>　陣営預かりになった島へは各ターンで設定された陣営パスワードで入れます。<BR>　パスワード変更が必要な時は、管理者へご連絡下さい。' if($HarmisticeTurn && !$HpassChangeOK);
	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='changeInfo'>
<H1>${AfterName}の名前とパスワードの変更</H1>
<table border=0 width=50%><tr><td class="M"><P>
<span class='attention'>(注意)</span><BR>
　名前の変更には${HtagMoney_}$HcostChangeName${HunitMoney}${H_tagMoney}かかります。$str
</P>
<FORM action="$HthisFile" method="POST">
どの${AfterName}ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
どんな名前に変えますか？(変更する場合のみ)<small>(全角${HlengthIslandName}字まで)</small><BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>${AfterName}<BR>
あなたの名前を変えますか？(変更する場合のみ)<small>(全角${HlengthOwnerName}字まで)</small><BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32 class=f><BR>

<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
</FORM>
</td></tr></table></DIV>
END
}

# 島の名前から番号を得る(IDじゃなくて番号)
sub nameToNumber {
	my($name) = @_;

	# 全島から探す
	my($i);
	foreach $i (0..$islandNumber) {
		if($Hislands[$i]->{'name'} eq $name) {
			return $i;
		}
	}

	# 見つからなかった場合
	return -1;
}

# 同盟の名前からIDを得る
sub aNameToId {
	my($name) = @_;

	# 全島から探す
	my($i);
	for($i = 0; $i < $HallyNumber; $i++) {
		if($Hally[$i]->{'name'} eq $name) {
			return $Hally[$i]->{'id'};
		}
	}

	# 見つからなかった場合
	return -1;
}

# 同盟のマークからIDを得る
sub aMarkToId {
	my($mark) = @_;

	# 全島から探す
	my($i);
	for($i = 0; $i < $HallyNumber; $i++) {
		if($Hally[$i]->{'mark'} eq $mark) {
			return $Hally[$i]->{'id'};
		}
	}

	# 見つからなかった場合
	return -1;
}

#----------------------------------------------------------------------
# 同盟の新規作成モード
#----------------------------------------------------------------------
# 結成・変更メイン
sub makeAllyMain {

	my $adminMode = 0;
	# パスワードチェック
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
				# 同盟データの書き込み
				writeAllyFile() if($HallyUse || $HarmisticeTurn);
				$HislandList = getIslandList($HcurrentID, 0);

				# 開放
				unlock();
				# トップへ
				topPageMain();
				return;
			}
		} else {
			unlock();
			out("${HtagBig_}結成or変更できません。${H_tagBig}$HtempBack");
			return;
		}
	}

	# 同盟名があるかチェック
	if($HallyName eq '') {
		unlock();
		$AfterName = '同盟';
		tempNewIslandNoName();
		return;
	}

	# 同盟名が正当かチェック
	if($HallyName =~ /[,\?\(\)\<\>\$]|^無人|^沈没$/) {
		# 使えない名前
		unlock();
		tempNewIslandBadOwnerName();
		return;
	}
	# 名前の重複チェック
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	if(!($adminMode && ($HallyID ne '') && ($HallyID < 200)) &&
		((nameToNumber($HallyName) != -1) ||
		((aNameToId($HallyName) != -1) && (aNameToId($HallyName) != $HcurrentID)))) {
		# すでに結成ずみ
		unlock();
		tempNewAllyAlready();
		return;
	}

	# マークの重複チェック
	if(!($adminMode && ($HallyID ne '') && ($HallyID < 200)) &&
		((aMarkToId($HallyMark) != -1) && (aMarkToId($HallyMark) != $HcurrentID))) {
		# すでに使用ずみ
		unlock();
		tempMarkAllyAlready();
		return;
	}

	# passwordの判定
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
				out("${HtagBig_}変更できません。${H_tagBig}$HtempBack");
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
			# すでに結成ずみなら変更
			logChangeAlly($Hally[$n]->{'name'}, $HallyName) if(!$adminMode && ($Hally[$n]->{'name'} ne $HallyName));
		}
	} else {
		# 他の島の同盟に入っている場合は、結成できない
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

		# 新規
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
		logMakeAlly($HallyName, islandName($island)) if(!$adminMode); # ログ
	}

	# 同盟の各種の値を設定
	$Hally[$n]->{'name'}     = $HallyName;
	$Hally[$n]->{'mark'}     = $HallyMark;
	$Hally[$n]->{'color'}    = "#${HallyColor}";
	
	# 費用をいただく
	$island->{'money'} -= $HcostMakeAlly if(!$adminMode);
	# データ書き出し
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# 開放
	unlock();
	# トップへ
	topPageMain();
}

# すでにその名前の同盟がある場合
sub tempNewAllyAlready {
	out(<<END);
${HtagBig_}その同盟ならすでに結成されています。${H_tagBig}$HtempBack
END
}

# すでにそのマークの同盟がある場合
sub tempMarkAllyAlready {
	out(<<END);
${HtagBig_}そのマークはすでに使用されています。${H_tagBig}$HtempBack
END
}

# 別の同盟を結成している
sub tempLeaderAlready {
	out(<<END);
${HtagBig_}盟主は、自分の同盟以外には加盟できません。${H_tagBig}$HtempBack
END
}

# 別の同盟に加盟している
sub tempOtherAlready {
	out(<<END);
${HtagBig_}ひとつの同盟にしか加盟できません。${H_tagBig}$HtempBack
END
}

# 資金足りず
sub tempNoMoney {
	out(<<END);
${HtagBig_}資金不足です(/_<。)${H_tagBig}$HtempBack
END
}
# 解散
sub deleteAllyMain {

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my $n = $HidToAllyNumber{$HcurrentID};
	my $adminMode = 0;
	# パスワードチェック
	if(checkSpecialPassword($HoldPassword)) {
		$n = $HcurrentAnumber;
		$HcurrentID = $Hally[$n]->{'id'};
		$adminMode = 1;
	} else {
		# passwordの判定
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
		# 念のためIDもチェック
		if($Hally[$n]->{'id'} != $HcurrentID) {
			unlock();
			tempWrongAlly();
			return;
		}
	}
	my $allyMember = $Hally[$n]->{'memberId'};
	if($adminMode && $HarmisticeTurn && ((@{$allyMember}[0] ne '') || !(defined $n))){
		unlock();
		out("${HtagBig_}削除できません。${H_tagBig}$HtempBack");
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
	# データ書き出し
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# 開放
	unlock();
	# トップへ
	topPageMain();
}

# IDチェックにひっかかる
sub tempWrongAlly {
	out(<<END);
${HtagBig_}あなたは盟主ではないと思う。${H_tagBig}$HtempBack
END
}

# 加盟・脱退
sub joinAllyMain {

	# passwordの判定
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
			# 開放
			unlock();
			logAllyMaxOver();
			exit(0);
		}
	}
	$island->{'money'} -= $HcomCost[$HcomAlly];
	$ally->{'memberId'} = \@newAllyMember;
	# データ書き出し
	allyOccupy();
	allySort();
	writeIslandsFile();
	$HislandList = getIslandList($HcurrentID, 0);

	# 開放
	unlock();
	# トップへ
	topPageMain();
}

# 結成
sub logMakeAlly {
	my($name, $owner) = @_;
	logHistory("同盟『${HtagName_}${name}${H_tagName}』が${HtagName_}${owner}${H_tagName}によって${HtagNumber_}結成${H_tagNumber}される。");
}

# 変更
sub logChangeAlly {
	my($oldname, $newname) = @_;
	logHistory("同盟「${HtagName_}${oldname}${H_tagName}」が『${HtagName_}${newname}${H_tagName}』に名称変更。");
}

# 解散
sub logDeleteAlly {
	my($name) = @_;
	logHistory("同盟『${HtagName_}${name}${H_tagName}』が${HtagDisaster_}解散！${H_tagDisaster}");
}

# 加盟
sub logAlly {
	my($name, $allyName) = @_;
	logHistory("${HtagName_}${name}${H_tagName}が『${HtagName_}${allyName}${H_tagName}』に${HtagNumber_}加盟${H_tagNumber}。");
}

# 脱退
sub logAllyEnd {
	my($name, $allyName) = @_;
	logHistory("${HtagName_}${name}${H_tagName}が『${HtagName_}${allyName}${H_tagName}』から${HtagDisaster_}脱退！${H_tagDisaster}");
}

# 同盟加盟可能島数オーバー
sub logAllyMaxOver {
	out(<<END);
${HtagBig_}加盟申請は破棄されました。(同盟加盟可能${AfterName}数オーバー)${H_tagBig}$HtempBack
END
}

# 同盟加盟拒否
sub logAllyVeto {
	out(<<END);
${HtagBig_}加盟申請は破棄されました。(拒否権発動)${H_tagBig}$HtempBack
END
}
#----------------------------------------------------------------------
# 同盟の結成・変更・解散・加盟・脱退
#----------------------------------------------------------------------
# 結成・変更・解散・加盟・脱退
sub newAllyTop {

	my $adminMode = 0;
	my $HtempBack2 = $HtempBack;
	# パスワードチェック
	if(checkSpecialPassword($HdefaultPassword)) {
		$adminMode = 1;
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		$HtempBack2 = "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}";
	} elsif(!$HallyUse) {
		require('./hako-top.cgi');
		topPageMain();
	}
	# 開放
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
	my $str1 = $adminMode ? '(メンテナンス)' : $HallyJoinComUse ? '' : '・加盟・脱退';
	my $str2 = $adminMode ? '' : 'onChange=colorPack() onClick=colorPack()';
	my $makeCost = $HcostMakeAlly ? "${HcostMakeAlly}${HunitMoney}" : '無料';
	my $keepCost = $HcostKeepAlly ? "${HcostKeepAlly}${HunitMoney}" : '無料';
	my $joinCost = $HcomCost[$HcomAlly] ? "${$HcomCost[$HcomAlly]}${HunitMoney}" : '無料';
	my $joinStr = $HallyJoinComUse ? '' : "加盟・脱退の際の費用は、${HtagMoney_}$joinCost${H_tagMoney}です。<BR>";
	my $str3 = $adminMode ? "特殊パスワードは？（必須）<BR>
<INPUT TYPE=\"password\" NAME=\"OLDPASS\" VALUE=\"$HdefaultPassword\" SIZE=32 MAXLENGTH=32 class=f><BR>同盟" : "<span class='attention'>(注意)</span><BR>
同盟の結成・変更の費用は、${HtagMoney_}${makeCost}${H_tagMoney}です。<BR>
また、毎ターン必要とされる維持費は${HtagMoney_}$keepCost${H_tagMoney}です。<BR>
（維持費は同盟に所属する${AfterName}で均等に負担することになります）<BR>
$joinStr
</P>
あなたの島は？（必須）<BR>
<SELECT NAME=\"ISLANDID\" $str2>
$HislandList
</SELECT><BR>あなた";

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='changeInfo'>
<H1>同盟の結成・変更・解散${str1}</H1>
<table border=0 width=50%><tr><td class="M"><P>
<FORM name="AcForm" action="$HthisFile" method="POST">
$str3
のパスワードは？（必須）<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32 class=f>
END
	
	if($HallyNumber) {
		my $str4 = $adminMode ? '・結成・変更' : $HallyJoinComUse ? '' : '・加盟・脱退';
		my $str5 = ($adminMode || $HallyJoinComUse) ? '' : '<INPUT TYPE="submit" VALUE="加盟・脱退" NAME="JoinAllyButton">';
		out(<<END);
<BR>
<BR><B><FONT SIZE=4>［解散${str4}］</FONT></B>
<BR>どの同盟ですか？<BR>
<SELECT NAME="ALLYNUMBER" onChange=allyPack() onClick=allyPack()>
$allyList
</SELECT>
<BR>
<INPUT TYPE="submit" VALUE="解散" NAME="DeleteAllyButton">
$str5
<BR>
END
	}

	my $str7 = $adminMode ? "盟主島の変更(上のメニューで同盟を選択してから島名選択もしくは盟主解雇)<BR> or 同盟の新規作成(上のメニューは無効)<BR><SELECT NAME=\"ALLYID\"><OPTION VALUE=\"$max\">新規作成<OPTION VALUE=\"0\">盟主解雇\n$HislandList</SELECT><BR>" : '<BR><B><FONT SIZE=4>［結成・変更］</FONT></B><BR>';
	out(<<END);
<BR>
$str7
同盟の名前（変更）<small>(全角${HlengthAllyName}字まで)</small><BR>
<INPUT TYPE="text" NAME="ALLYNAME" VALUE="$allyname" SIZE=32 MAXLENGTH=32><BR>
マーク（変更）<BR>
<SELECT NAME="MARK" onChange=colorPack() onClick=colorPack()>
$markList
</SELECT>
<ilayer name="PARENT_CTBL" width="100%" height="100%">
   <layer name="CTBL" width="200"></layer>
   <span id="CTBL"></span>
</ilayer>
<BR>
マークの色コード（変更）<BR><TABLE BORDER=0><TR>
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
<INPUT TYPE="submit" VALUE="結成(変更)" NAME="NewAllyButton">
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
	str = '表示サンプル：『<B><span class="number"><FONT color="' + str +'">' + mark + '</FONT></B>'
	  + island[number] + '${AfterName}</span>』';
	
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


	if(name == '') { name = 'さんぷる'; }
	str = "#" + a + b + c + d + e + f;
//	document.AcForm.AcColorValue.value = str;
	str = '表示サンプル：『<B><span class="number"><FONT color="' + str +'">' + mark + '</FONT></B>'
	  + name + '${AfterName}</span>』';
	
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

# 盟主コメントモード
sub allyPactMain {
	my $ally = $Hally[$HidToAllyNumber{$HcurrentID}];
	if($HallyPactMode != 2) {
		# 開放
		unlock();
		if($HallyPactMode && !checkPassword($ally, $HdefaultPassword)) {
			# password間違い
			tempWrongPassword();
			return;
		}
		# テンプレート出力
		tempAllyPactPage();
	} else {
		# パスワードチェック
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
			# データ書き出し
			writeAllyFile();
			unlock();
			# 変更成功
			tempAllyPactOK($ally);
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# 盟主コメントモードのトップページ
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
<H1>情報変更（$ally->{'name'}）</H1>
<table border=0 width=80%><tr><td class="M">
<FORM action="$HthisFile" method="POST">
<B>盟主パスワードは？</B><BR>
<INPUT TYPE="password" NAME="Allypact" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f>
<INPUT TYPE="hidden"  NAME="ISLANDID" VALUE="$ally->{'id'}">
<INPUT TYPE="hidden"  NAME="AllypactMode" VALUE="$HallyPactMode">
<INPUT TYPE="submit" VALUE="送信" NAME="AllypactButton">
END
	if($HallyPactMode) {
		out("<TABLE><TR><TD class='M'>");
		if($HallyVetoUse) {
			my(%vetoID);
			foreach (@{$ally->{'vetoId'}}) {
				$vetoID{$_} = 1;
			}
			out("<BR><BR><B>加盟${AfterName}の設定</B><TABLE cellpadding=0 cellspacing=0>");
			foreach ($HbfieldNumber..$islandNumber) {
				my($id, $name, $s);
				$id = $Hislands[$_]->{'id'};
				next if($id == $ally->{'id'});
				$name = islandName($Hislands[$_]);
				$s = ' CHECKED' if($vetoID{$id});
				out("<TR><TD><input type=checkbox name=VETOID value=\"$id\"$s></TD><TD>$name</TD></TR>");
			}
			my($s1, $s2) = (!$ally->{'vkind'}) ? ('', ' checked') : (' checked', '');
			out("<TR><TD colspan=2 class='M'>※チェックを入れた$AfterNameの加盟を</TD><TR>");
			out("<TR><TD align='center' colspan=2 class='M'>　　<input type=radio name=VETOKIND value=\"1\"${s1}><FONT COLOR='#FF0000'>許可</FONT> <input type=radio name=VETOKIND value=\"0\"${s2}><FONT COLOR='#0000FF'>拒否</FONT></TD><TR>");
			out("<TR><TD align='right' colspan=2 class='M'>します。</TD><TR>");
			out("<TR><TD align='center' colspan=2 class='M'><INPUT TYPE=\"submit\" VALUE=\"送信\" NAME=\"AllypactButton\"></TD><TR>");
			out("</TABLE>");
		}
		out(<<END);
</TD><TD class='M'>
<BR><BR><B>コメント</B><small>(全角${HlengthAllyComment}字まで：トップページの「各同盟の状況」欄に表示されます)</small><BR>
<INPUT TYPE="text" NAME="ALLYCOMMENT"  VALUE="$ally->{'comment'}" SIZE=100 MAXLENGTH=50><BR>
<BR>
<INPUT TYPE="submit" VALUE="送信" NAME="AllypactButton">
<BR><BR>
<B>メッセージ・盟約など</B>(「同盟の情報」欄の上に表示されます)<BR>
タイトル<small>(全角${HlengthAllyTitle}字まで)</small><BR>
<INPUT TYPE="text" NAME="ALLYTITLE"  VALUE="$ally->{'title'}" SIZE=100 MAXLENGTH=50><BR>
メッセージ<small>(全角${HlengthAllyMessage}字まで)</small><BR>
<TEXTAREA COLS=50 ROWS=16 NAME="ALLYMESSAGE" WRAP="soft">$allyMessage</TEXTAREA>
<BR>
「タイトル」を空欄にすると『盟主からのメッセージ』というタイトルになります。<BR>
「メッセージ」を空欄にすると「同盟の情報」欄には何も表示されなくなります。
</TD></TR></TABLE>
END
	}

	out(<<END);
</FORM>
</td></tr></table>
</DIV>
END
}

# 盟主コメント変更完了
sub tempAllyPactOK {
	my($ally) = @_;
	out(<<END);
${HtagBig_}<FONT COLOR="$ally->{'color'}">$ally->{'mark'}</FONT>$ally->{'name'}の情報を変更しました。${H_tagBig}<HR>
END
	$HallyPactMode = 1;
	tempAllyPactPage();
}

#----------------------------------------------------------------------
# ＨＴＭＬ生成
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime(time + $Hjst);
	$mon++;
	my($sss) = "${mon}月${date}日 ${hour}時${min}分${sec}秒";

	$html1=<<_HEADER_;
<HTML><HEAD>
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
最近の出来事
</TITLE>
<BASE HREF="$htmlDir/">
<link rel="stylesheet" type="text/css" href="${HcssDir}/$HcssDefault">
</HEAD>
$Body<DIV ID='BodySpecial'>
<DIV ID='RecentlyLog'>
<H1>最近の出来事</H1>
<FORM>
最新更新日：$sss・・
<INPUT TYPE="button" VALUE=" 再読込み" onClick="location.reload()">
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

			# 機密関係
			next if($m == 1);

			# 表示
			if($set_turn == 0){
				$html2 .= "<B>=====[${HtagNumber_}<FONT SIZE=4>ターン$turn </FONT>${H_tagNumber}]================================================</B><BR>\n";
				$set_turn++;
			}
			$html2 .= "${HtagNumber_}★${H_tagNumber}:$message<BR>\n";
		}
		close(LIN);
	}
	open(HTML, ">${HhtmlDir}/hakolog.html");
#	print HTML jcode::sjis($html1); # jcode使用時
#	print HTML jcode::sjis($html2);
#	print HTML jcode::sjis($html3);
	print HTML $html1;
	print HTML $html2;
	print HTML $html3;
	close (HTML);
	chmod(0666,"${HhtmlDir}/hakolog.html");
}

#----------------------------------------------------------------------
# 人口その他の値を算出（縮小）
#----------------------------------------------------------------------
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $mountain, $navyPort, $sea) = (0, 0, 0, 0, 0);

	# 地形を取得
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# 数える
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if($kind != $HlandSea){
				$area++;
				if($kind == $HlandTown) {
					# 町
					$pop += $value;
				} elsif($kind == $HlandMountain) {
					# 山
					$mountain += $value;
				} elsif ($kind == $HlandNavy) {
					if ($HnavySpecial[(navyUnpack($value))[7]] & 0x8) {
						# 港
						$navyPort++;
					}
				}
			} elsif(!$value) {
				$sea++;
			}
		}
	}

	# 代入
	$island->{'pop'}      = $pop;
	$island->{'area'}     = $area;
	$island->{'mountain'} = $mountain;
	$island->{'navyPort'} = $navyPort;
	$island->{'sea'}      = $sea;
	$island->{'farm'}     = 0;
	$island->{'factory'}  = 0;
}

# 範囲内の地形を数える（島作成用）
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
#----------------------------------------------------------------------
# 島の強制削除(情報変更で)
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
	# 島テーブルの操作
	$island->{'dead'} = 1;
	$island->{$HrankKind} = 0;
	$island->{'pop'} = 0;
	$island->{'field'} = 0;
	$island->{'predelete'} = 0;

	allyOccupy();
	allySort();
	islandSort($HrankKind);

	logDeleteIsland($HcurrentID, $island->{'name'}) if($num);

	# メインデータの操作
	$HislandNumber--;
	$islandNumber--;

	deleteIslandData($island);
	writeIslandsFile($HcurrentID);

	unlock();
	tempDeleteIsland($island->{'name'});
}

#----------------------------------------------------------------------
# BattleField作成モード
#----------------------------------------------------------------------
sub bfieldMain {
	if (!$HbfieldMode) {
		$HislandList = getIslandList(-1, 1);
		# 開放
		unlock();
		# テンプレート出力
		tempBfieldPage();
	} else {
		# パスワードチェック
		if(checkSpecialPassword($HdefaultPassword)) {
			# 特殊パスワード
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

			# idから島を取得
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($name) = $island->{'name'};
			my($id) = $island->{'id'};

			my($bId, $str, $tmpid);
			my $safety = 0;
			if(!$island->{'field'}) {
				# 設定
				$Hislands[$HcurrentNumber]->{'field'} = 1;
				$str = "通常の島 → Battle Field";
			} else {
				# 解除
				$Hislands[$HcurrentNumber]->{'field'} = 0;
				$str = "Battle Field → 通常の島";
			}

			# データ書き出し
			islandSort($HrankKind);
			writeIslandsFile($id);

			unlock();

			# 変更成功
			tempBfieldOK($name, $str);
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# BattleField作成モードのトップページ
sub tempBfieldPage {
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2<BR>
<H1>Battle Fieldを作成</H1>
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
海域座標を指定して下さい<BR>座標（
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
</SELECT>）　<INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>ランダム<BR><BR>
END
	}

	out(<<END);
<B>Battle Field設定を変更する${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Bfield">
<INPUT TYPE="submit" VALUE="設定変更" NAME="BfieldButton"><BR>
</FORM>
「新規作成(すべて海)」の場合、島のパスワードはマスターパスワードになります。<BR>
作成後、必要に応じてパスワードを変更してください。</DIV>
END
}

# BattleField作成完了
sub tempBfieldOK {
	my($name, $str) = @_;
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$name${AfterName}のBattle Field設定を変更しました。<br>$str${H_tagBig}
END
}

# BattleField作成失敗
sub tempBfieldNG {
	my($str) = @_;
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}Battle Fieldの設定エラー($str)。${H_tagBig}$HtempBack2
END
}

#----------------------------------------------------------------------
# 管理人による島データ修正モード
#----------------------------------------------------------------------
sub islandSetupMain() {
	if (!$HisetupMode) {
		# 開放
		unlock();
		# テンプレート出力
		tempIslandSetupPage(0);
		return;
	} elsif(!checkSpecialPassword($HdefaultPassword)) {
		# パスワードチェック
		# 特殊パスワード
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}
	if($HisetupMode == 2) {
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		# 島名が正当かチェック
		if($HcurrentName =~ /[,\?\(\)\<\>\$]|^無人|^沈没$/) {
			# 使えない名前
			unlock();
			tempNewIslandBadName();
			return;
		}
		# オーナー名が正当かチェック
		if($HcurrentOwnerName =~ /[,\?\(\)\<\>\$]/) {
			# 使えない名前
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
								# 内政(開発)，内政(建設)，複合施設，海軍(建造) <200 , 330< 軍事(建設) <350 , 残骸修理，残骸売却
							((215 < $kind) && ($kind < 220)) || ((350 < $kind) && ($kind < 361)))) {
								# 移動操縦，移動指令，艦艇指令変更，一斉攻撃と軍事(攻撃)[内政，建造以外で，座標指定するもの]
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
	# 開放
	unlock();
	# テンプレート出力
	tempIslandSetupPage(1);
}

# 島データ修正ページ
sub tempIslandSetupPage() {
	my($mode) = @_;

	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>${AfterName}データ修正</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME="ISetup" VALUE="$HdefaultPassword">
<B>データを修正する${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="submit" VALUE="データ修正画面へ" NAME="IslandChoice"><BR>
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
		$islandList .= '<OPTION VALUE="-2">圧勝！';
		$islandList .= '<OPTION VALUE="-1">不戦勝';
		$islandList .= '<OPTION VALUE="0" style="background:yellow;" selected>未定';
		$islandList .= getIslandList(0, 1);
	} elsif($fight_id == -1) {
		$islandList .= '<OPTION VALUE="-2">圧勝！';
		$islandList .= '<OPTION VALUE="-1" style="background:yellow;" selected>不戦勝';
		$islandList .= '<OPTION VALUE="0">未定';
		$islandList .= getIslandList(0, 1);
	} elsif($fight_id == -2) {
		$islandList .= '<OPTION VALUE="-2" style="background:yellow;" selected>圧勝！';
		$islandList .= '<OPTION VALUE="-1">不戦勝';
		$islandList .= '<OPTION VALUE="0">未定';
		$islandList .= getIslandList(0, 1);
	} else {
		$islandList .= '<OPTION VALUE="-2">圧勝！';
		$islandList .= '<OPTION VALUE="-1">不戦勝';
		$islandList .= '<OPTION VALUE="0">未定';
		$islandList .= getIslandList($fight_id, 1, 'yellow');
	}
	
	my $predel = '';
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
		$predel = '【管理人あずかり】$rest';
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
<TR><TH>${HtagTH_}$name${AfterName}${H_tagTH}$predel　${HtagTH_}データ修正${H_tagTH}　<INPUT TYPE="submit" VALUE="修正" NAME="ChangeButton"></TH></TR>

<TR><TD class='M'>
<TABLE BORDER width="100%">
<TR><TH colspan=12>基本データ</TH></TR><TR>
<TR>
<TH $HbgTitleCell rowspan=2>${HtagTH_}${AfterName}ID${H_tagTH}</TH>
END
	out("<TH $HbgTitleCell rowspan=2>${HtagTH_}海域座標${H_tagTH}</TH>") if($HoceanMode);
	out(<<END);
<TH $HbgTitleCell rowspan=2>${HtagTH_}${AfterName}名${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}オーナー名${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}開始ターン${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}資金繰り${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}陣営開発可${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}資金${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}食料${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}総獲得経験値${H_tagTH}</TH>
<TH $HbgTitleCell rowspan=2>${HtagTH_}フィールド属性${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}トーナメント用${H_tagTH}</TH>
</TR>
<TR>
<TH $HbgTitleCell>${HtagTH_}対戦相手${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}開発停止ターン数${H_tagTH}</TH>
</TR>
<TR>
<TD align="center"><INPUT TYPE="hidden" NAME="ISLANDID" VALUE="$id">${id}</TD>
END
	if($HoceanMode) {
		out("<TD align=\"center\">（<SELECT NAME=\"OCEANX\">");
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
</SELECT>）<BR><INPUT TYPE=CHECKBOX name='RANDOM' VALUE='1'>ランダム</TD>
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
<TD align="center"><INPUT TYPE="text" NAME="REST" VALUE="$rest" SIZE=5 MAXLENGTH=32>ターン</TD>
</TD></TR></TABLE></TD></TR>
END

	$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
	my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	my $col = $#Hprize;
	out("<TR><TH colspan=$col>賞</TH></TR><TR>\n");
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
	out("<TR><TH colspan=$HmonsterNumber>退治した怪獣</TH></TR><TR>\n");
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
	out("<TR><TH colspan=$HhugeMonsterNumber>退治した巨大怪獣</TH>\n");
#	out("<TH>怪獣退治数</TH>\n");
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
	out("<TR><TH colspan=$col>艦艇撃沈数　　(撃沈数＝他島＋自島，自爆数＝自島)</TH></TR><TR><TD colspan=2>　</TD>\n");
	foreach(@HnavyName) {
		out("<TD class='T'>${HtagTH_}$_${H_tagTH}</TD>\n");
	}
	out("</TR><TR><TH colspan=2>他島</TH>\n");
	my @kindNavy = ('艦', '港');
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SINK\" VALUE=\"@$sink[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR><TR><TH colspan=2>自島</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SINKSELF\" VALUE=\"@$sinkself[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	my $turn = @$subExt[0];
	$turn-- if($turn > 0);
	out("</TR><TH rowspan=2>${turn}ターン<BR>までの記録</TH><TH>他島</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBSINK\" VALUE=\"@$subSink[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR><TR><TH>自島</TH>\n");
	foreach(0..$#HnavyName) {
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBSINKSELF\" VALUE=\"@$subSinkself[$_]\" SIZE=5 MAXLENGTH=32>$kindNavy[!$_]</TD>\n");
	}
	out("</TR></TABLE></TD></TR>\n");

	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	out("<TR><TH colspan=11>拡張データ</TH>\n");
	out("<TH rowspan=2>怪獣<BR>退治数</TH>\n");
	out("<TD class='M' colspan='1'></TD>\n");
	out("</TR><TR>\n");
	foreach ('勝利フラグ', '貢献度x10', '防撃破', 'ミ撃破', '民救出', '弾飛来', '弾発射', '弾防御', '艦派遣', '艦来襲', '艦破壊') {
		out("<TH $HbgTitleCell>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("</TR><TR>");
	my @after = ('', '', '基', '基', "$HunitPop", '発', '発', '発', '艦', '艦', '艦');
	foreach (0..10){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"EXT\" VALUE=\"@$ext[$_]\" SIZE=5 MAXLENGTH=32>$after[$_]</TD>\n");
	}
	out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"MONSTERKILL\" VALUE=\"$monsterkill\" SIZE=5 MAXLENGTH=32>$HunitMonster</TD>\n");
	out("<TD class='M' colspan='1'></TD>\n");
	out("</TR><TR><TH colspan=13>サブ拡張データ(${turn}ターンまでの記録)</TH></TR><TR>\n");
	foreach ('記録ターン', '貢献度x10', '防撃破', 'ミ撃破', '民救出', '弾飛来', '弾発射', '弾防御', '艦派遣', '艦来襲', '艦破壊', '退治数', '報奨金') {
		out("<TH $HbgTitleCell>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("</TR><TR>");
	my @subAfter = ('ターンより前', '', '基', '基', "$HunitPop", '発', '発', '発', '艦', '艦', '艦', "$HunitMonster", "$HunitMoney");
	foreach (0..12){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"SUBEXT\" VALUE=\"@$subExt[$_]\" SIZE=5 MAXLENGTH=32>$subAfter[$_]</TD>\n");
	}
	out("</TR></TABLE></TD></TR>\n");

	out("<TR><TD class='M'><TABLE BORDER width=\"100%\">\n");
	$col = $#HitemName;
	out("<TR><TH colspan=$col>保有アイテム　($HitemName[0])</TH></TR><TR>\n");
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
	out("<TR><TH colspan=$col>気象</TH></TR><TR>\n");
	foreach ('気温', '気圧', '湿度', '風速', '地盤', '波力', '(未使用)') {
		out("<TH $HbgTitleCell rowspan=2>${HtagTH_}$_${H_tagTH}</TH>\n");
	}
	out("<TH $HbgTitleCell colspan=$HtopLogTurn>${HtagTH_}天気一覧${H_tagTH}</TH>\n");
	out("</TR><TR>");
	my($wTurn) = $HislandTurn + 3;
	foreach (1..$HtopLogTurn) {
		out("<TH $HbgTitleCell>${HtagTH_}ターン$wTurn${H_tagTH}</TH>\n");
		$wTurn--;
	}
	out("</TR><TR>");
	my @wAfter = ('℃', 'hPa', '%', 'm/s', '', '', '');
	foreach (0..6){
		out("<TD align=\"center\"><INPUT TYPE=\"text\" NAME=\"WEATHER\" VALUE=\"@$weather[$_]\" SIZE=5 MAXLENGTH=32>$wAfter[$_]</TD>\n");
	}
	my($i) = 7;
	foreach (1..$HtopLogTurn){
		if(@$weather[$i]) {
			out("<TD align=\"center\"><INPUT TYPE=\"hidden\" NAME=\"WEATHER\" VALUE=\"@$weather[$i]\" SIZE=5 MAXLENGTH=32><img src ='${HimageDir}/$HweatherImage[@$weather[$i]]' width='16' height='16'>$HweatherName[@$weather[$i]]</TD>\n");
		} else {
			out("<TD align=\"center\"><INPUT TYPE=\"hidden\" NAME=\"WEATHER\" VALUE=\"@$weather[$i]\" SIZE=5 MAXLENGTH=32>−</TD>\n");
		}
		$i++;
	}
	out("</TR></TABLE></TD></TR>\n");
	out(<<END);
</TR></TABLE>
<TR><TH colspan=8>${HtagTH_}${AfterName}データ修正${H_tagTH}　<INPUT TYPE="submit" VALUE="修正" NAME="ChangeButton"></TH></TR>
</TR></TABLE>
<INPUT TYPE="hidden" VALUE="dummy" NAME="IslandChange"></FORM></DIV>
END
}

#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------
# 記録ログ
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 発見
sub logDiscover {
	my($name, $owner) = @_;
	logHistory("${HtagName_}${name}${H_tagName}が${HtagName_}${owner}${H_tagName}によって発見される。");
}

# 島名の変更
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}、名称を${HtagName_}${name2}${AfterName}${H_tagName}に変更する。");
}

# オーナー名の変更
sub logChangeOwnerName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}、所有者を${HtagName_}${name2}${H_tagName}に変更する。");
}

# 不正アクセス
sub tempNoReferer {
	out(<<END);
${HtagBig_}怪しいことはおやめくださいm(_ _)m${H_tagBig}$HtempBack
END
}

# 島がいっぱいな場合
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}申し訳ありません、${AfterName}が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で島名がない場合
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}${AfterName}につける名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規で島名が不正な場合
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\$'が入っていたり、「無人${AfterName}」のような名前はやめましょう。${H_tagBig}$HtempBack
END
}

# 新規でオーナー名がない場合
sub tempNewIslandNoOwnerName {
	out(<<END);
${HtagBig_}あなたの名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規でオーナー名が不正な場合
sub tempNewIslandBadOwnerName {
	out(<<END);
${HtagBig_}',?()<>\$'が入っている名前はやめましょう。${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}その${AfterName}ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# パスワードがない場合
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
	out(<<END);
<DIV align='center'>
${HtagBig_}${AfterName}を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}」${H_tagName}と命名します。${H_tagBig}<BR>
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

# 名前変更失敗
sub tempChangeNothing {
	out(<<END);
${HtagBig_}名前、パスワードともに空欄です。${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}資金不足のため変更できません。${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
	out(<<END);
${HtagBig_}変更完了しました。${H_tagBig}$HtempBack
END
}

# 強制削除ログ
sub logDeleteIsland {
	my($id, $name) = @_;
#	logHistory("${HtagName_}${name}${AfterName}${H_tagName}、<B>管理人権限により</B>${HtagDisaster_}退場${H_tagDisaster}となる。");
#	logHistory("${HtagName_}${name}${AfterName}${H_tagName}に、突然<B>天罰が降り</B>あっというまに${HtagDisaster_}海に沈没し${H_tagDisaster}跡形もなくなりました。");
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}は、海神の<B>怒りに触れ</B>陸地はすべて${HtagDisaster_}沈没しました。${H_tagDisaster}");
}

# 島の強制削除(スペシャルモード)
sub tempDeleteIsland {
	my($name) = @_;
	out(<<END);
${HtagBig_}${name}${AfterName}を強制削除しました。${H_tagBig}$HtempBack
END
}

1;

