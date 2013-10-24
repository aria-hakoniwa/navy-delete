# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 入出力用スクリプト(ver1.00)
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
# 島データ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readIslandsFile {
	my($num) = @_; # 0だと地形・コマンド・掲示板ログを読みこまず
				   # -1だと全地形・全コマンドを読む
				   # -2だと全地形を読む
				   # -3だと全コマンドを読む
				   # -4だと全掲示板ログを読む
				   # 番号だとその島の地形・コマンド・掲示板ログだけは読みこむ

	# データファイルを開く
	if(!open(IN, "${HdirName}/$HmainData")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/$HmainData");
		if(!open(IN, "${HdirName}/$HmainData")) {
			return 0;
		}
	}

	# 各パラメータの読みこみ
	my $tmp = <IN>;
	chomp($tmp);
	($HislandTurn, $HplayNow) = split(/,/, $tmp); # ターン数, ゲーム中フラグ
#	if($HislandTurn == 0) {
#		return 0;
#	}
	$HislandLastTime = int(<IN>); # 最終更新時間
	if($HislandLastTime == 0) {
		return 0;
	}
	# unitTimeとrepeatTurnの上書き
	my $armTurn = ($HarmisticeTurn < $HsurvivalTurn) ?  $HsurvivalTurn : $HarmisticeTurn;
	$HarmTime = $HunitTime;
	$HarmRepeatTurn = $HrepeatTurn;
	if($armTurn && ($HislandTurn < $armTurn)){
		$HunitTime = $HarmisticeTime;
		$HrepeatTurn = $HarmisticeRepeatTurn;
	}
	$HislandNumber = int(<IN>); # 島の総数
	$islandNumber = $HislandNumber - 1; # 島の総数 - 1
	$HislandNextID = int(<IN>); # 次に割り当てるID
	# 管理人預かりの島ID
	$tmp = <IN>;
	chomp($tmp);
	my(%preFlag);
	foreach (split(/,/, $tmp)) {
		my($pID, $pTurn) = split(/<>/, $_);
		$preFlag{$pID} = $pTurn;
		push(@HpreDeleteID, $pID);
	}

	# トーナメント用
	$HislandFightMode  = int(<IN>);  # 現在の戦闘モード
	$HislandChangeTurn = int(<IN>);  # 切り替えターン
	$HislandFightCount = int(<IN>);  # 何回戦目か

	chomp($tmp = <IN>); # 戦争国一覧
	@HwarIsland = split(/,/, $tmp);
	<IN>;# 拡張用
	<IN>;# 拡張用
	<IN>;# 拡張用
	<IN>;# 拡張用
	<IN>;# 拡張用
	<IN>;# 拡張用
	if($Htournament){
		# トーナメントモード
		if(($HislandChangeTurn != $HyosenTurn) && ($HislandTurn < $HyosenTurn)) {
			# 途中で設定変更した場合の処理
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
			# 開発
			@HflexTime = @HtmTime2;
			$HunitTime = $HdevelopeTime;
			$HunitTime = (($HislandTurn > $HyosenTurn) && ($HislandTurn == $HislandChangeTurn - $HdevelopeTurn)) ? $HinterTime : $HdevelopeTime;
			$HrepeatTurn = $HdeveRepCount;
		} elsif($HislandFightMode == 2) {
			# 戦闘
			@HflexTime = @HtmTime3;
			$HunitTime = $HfightTime;
			$HrepeatTurn = $HfightRepCount;
		} else {
			# 予選
			@HflexTime = @HtmTime1;
			$HunitTime = $HyosenTime;
			$HrepeatTurn = $HyosenRepCount;
		}
	} else {
		$HislandFightMode  = 0;  # 現在の戦闘モード
		$HislandChangeTurn = 0;  # 切り替えターン
		$HislandFightCount = 0;  # 何回戦目か
	}
	# flexTime処理
	$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	# ターン処理判定
	my($now) = time;
	my $flag = 0; # ターン更新前は0，更新時は1
	my $tempMode = $HmainMode;
	my $predelNumber = @HpreDeleteID; # 管理人あずかりの島
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
		$num = -1; # 全島読みこむ
		$flag = 1; # 更新フラグを1に
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
		$HnextTime = sprintf('%d月 %d日 %d時', (gmtime($HnextTime + $Hjst))[4] + 1, (gmtime($HnextTime + $Hjst))[3,2]);
	} else {
		$HplayNow  = 0;
		$HnextTime = ' ';
		$HmainMode = ($tempMode ne '') ? $tempMode : 'top';
	}

	# 島の読みこみ
	if($HoceanMode && !(-e "${HdirName}/world.${HsubData}") && !(-e "${HdirName}/worldtmp.${HsubData}")) {
		$HoceanMapNone = 1;
	}
	my($i);
	# 管理人あずかりのフラグセット
	$HbfieldNumber = 0;
	foreach $i (0..$islandNumber) {
		$Hislands[$i] = readIsland($num);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
		if($Hislands[$i]->{'field'}) {
			$HbfieldNumber++;
		}
		if($preFlag{$Hislands[$i]->{'id'}}) {
			# 管理人あずかりのフラグ設定
			$Hislands[$i]->{'predelete'} = $preFlag{$Hislands[$i]->{'id'}};
		}
	}
	# ファイルを閉じる
	close(IN);

	# 海域
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
	# 同盟データの読み込み
	readAllyFile() if($HallyUse || $HarmisticeTurn || ($HmainMode eq 'asetup'));

	# アイテムの準備
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
			# 座標で地形のIDをセット
			my($x, $y);
			foreach $x (@{$island->{'map'}->{'x'}}) {
				foreach $y (@{$island->{'map'}->{'y'}}) {
					$HlandID[$x][$y] = $island->{'id'};
				}
			}
		}
		# コマンド実行フラグ処理
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
		# トップモードに変更
		$HmainMode = ($tempMode ne '') ? $tempMode : 'top';
		$HplayNow  = 0;
		$HnextTime = ' ';
	}
	return 1;
}

# 島ひとつ読みこみ
sub readIsland {
	my($num) = @_;
	my($name, $owner, $birthday, $id, $prize, $absent, $preab, $comflag, $earth, $comment, $password, $money, $food,
		$pop, $area, $farm, $factory, $mountain, $tmp, @amity, @fleet, @priority, @fkind, $gain, $monskill, $monslive,
		@sinktmp, @sink, @sinkself, @subSink, @subSinkself, @exttmp, @ext, @subExt, $field, @item, @weather,
		$fight_id, $rest, @event, $point, @defeat ,%epoint, @epointtmp, @xytmp, @x, @y, $map, $wmap, @move);
	chomp($name = <IN>);     # 島の名前
	chomp($owner = <IN>);    # オーナーの名前
	$birthday = int(<IN>);   # 開始ターン
	$id = int(<IN>);         # ID番号
	chomp($prize = <IN>);    # 受賞
	chomp(($absent, $preab, $comflag, $earth) = split(/\,/, <IN>)); # 連続資金繰り数, 開発委託(陣営あずかり), コマンド実行設定, 地球モード周辺表示
	chomp($comment = <IN>);  # コメント
	chomp($password = <IN>); # 暗号化パスワード
	$money    = int(<IN>);   # 資金
	$food     = int(<IN>);   # 食料
	$pop      = int(<IN>);   # 人口
	$area     = int(<IN>);   # 広さ
	$farm     = int(<IN>);   # 農場
	$factory  = int(<IN>);   # 工場
	$mountain = int(<IN>);   # 採掘場
	chomp($tmp = <IN>);      # 友好国
		@amity = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 艦隊名
		@fleet = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 索敵順
		@priority = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 保有艦艇種類
		@fkind = split(/\,/, $tmp);
	$gain     = int(<IN>);   # 総獲得経験値
	$monskill = int(<IN>);   # 怪獣退治数
	chomp($monslive = <IN>); # 怪獣出現数, 種類, 種類(巨大), 所属不明艦艇出現数, 種類
	chomp($tmp = <IN>);      # 撃沈数
		@sinktmp = split(/\-/, $tmp);
			@sink = split(/\,/,$sinktmp[0]);        # 自島以外の艦艇
			@sinkself = split(/\,/,$sinktmp[1]);    # 自島
			@subSink = split(/\,/,$sinktmp[2]);     # サブ自島以外の艦艇
			@subSinkself = split(/\,/,$sinktmp[3]); # サブ自島
	chomp($tmp = <IN>);      # 拡張領域
		@exttmp = split(/<>/, $tmp);
			@ext = split(/\,/,$exttmp[0]);    # 拡張領域
			# 勝利フラグ, 貢献度x10, 防撃破, ミ撃破, 民救出, 弾飛来, 弾発射, 弾防御, 艦派遣, 艦来襲, 艦破壊
			@subExt = split(/\,/,$exttmp[1]); # サブ拡張領域
			# 記録ターン, 貢献度x10, 防撃破, ミ撃破, 民救出, 弾飛来, 弾発射, 弾防御, 艦派遣, 艦来襲, 艦破壊, 退治数, 報奨金
	chomp($field = <IN>);    # フィールド属性
	chomp($tmp = <IN>);      # アイテム
		@item = split(/\,/, $tmp);
	chomp($tmp = <IN>); # 気温,気圧,湿度,風速,地盤,波力,異常,天候(ログ表示数)
		$tmp = "20,1013,40,0,0,0,0,2,2,2,2" if($tmp == '');
		@weather = split(/\,/, $tmp);
	chomp(($fight_id, $rest) = split(/\,/, <IN>)); # トーナメント 対戦相手ID, 開発停止残りターン数
	chomp($tmp = <IN>); # イベントフラグ 開始ターン 期間 艦艇数 艦種 制限 タイプ 報償金 報償食料 管理人プレゼントの有無 報償アイテム 追加派遣 怪獣出現1 怪獣出現2 巨大怪獣出現1 巨大怪獣出現2 艦艇出現1 艦艇出現2 自動帰還
#               0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
		$tmp = "0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0" if($tmp == '');
		@event = split(/\,/, $tmp);
	$point = int(<IN>); # ポイント
	chomp($tmp = <IN>); # 沈没させた島名,ターン数,・・・
		@defeat = split(/\,/, $tmp);
	chomp($tmp = <IN>); # イベントポイント
		@epointtmp = split(/\,/, $tmp);
		for($i=0;$i<$#epointtmp;$i+=2) {
			$epoint{$epointtmp[$i]} = $epointtmp[$i+1];
		}
	chomp($tmp = <IN>);      # マップ配列格納 x0,x1,...,xn<>y0,y1,...,yn<>x<>y
		if(!$HoceanMode && !(-e "${HdirName}/${id}.${HsubData}") && !(-e "${HdirName}/${id}tmp.${HsubData}")) {
			$HislandMapNone = 1;
		}
		@xytmp = split(/<>/, $tmp);
			@x = (($HoceanMode || $HislandMapNone) && (defined $xytmp[0])) ? split(/\,/, $xytmp[0]) : (0..($HislandSizeX-1));
			@y = (($HoceanMode || $HislandMapNone) && (defined $xytmp[1])) ? split(/\,/, $xytmp[1]) : (0..($HislandSizeY-1));
		$map  = { 'x' => \@x, 'y' => \@y };
		$wmap = { 'x' => $xytmp[2], 'y' => $xytmp[3] };
		if($HoceanMapNone) {
			$wmap = randomIslandMap(); # 島の座標を決める
			# マップ配列
			my @x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
			my @y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
			$map = { 'x' => \@x, 'y' => \@y };
		}
		$HoceanMap[$wmap->{'x'}][$wmap->{'y'}] = $id;
	chomp($tmp = <IN>);      # 移動指令 x,y<>x,y<>x,y<>x,y
		@move = split(/<>/, $tmp);
	<IN>; # 予備
	<IN>; # 予備

	# HidToNameテーブルへ保存
	$HidToName{$id} = $name;

	my(@line, @land, $command, $lbbs);

	# 地形
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

	# コマンド
	if(($num == -1) || ($num == -3) || ($num == $id)) {
		if( $HmainMode eq 'owner'       || # 開発モード
			$HmainMode eq 'commandJava' || # コマンド入力モード
			$HmainMode eq 'command'     || # コマンド入力モード
			$HmainMode eq 'command2'    || # コマンド入力モード（ver1.1より追加・自動系用）
			$HmainMode eq 'comment'     || # コメント入力モード
			$HmainMode eq 'fleetname'   || # 艦隊名変更モード
			$HmainMode eq 'priority'    || # 索敵順変更モード
			$HmainMode eq 'earth'       || # 周辺表示設定モード
			$HmainMode eq 'comflag'     || # コマンド実行設定モード
			$HmainMode eq 'preab'       || # 陣営共同開発モード
			$HmainMode eq 'lbbs'        || # ローカル掲示板モード
			$HmainMode eq 'new'         || # 島の新規作成
			$HmainMode eq 'print'       || # 観光モード
			$HmainMode eq 'reload'      || # 保存データ復元モード
			$HmainMode eq 'turn'        || # ターン進行
			$HmainMode eq 'camp'        || # 陣営モード
			$HmainMode eq 3             || # モバイルモード
			$HmainMode eq 4                # モバイルモード
		) {
			$command = readCommand($id, $HcommandMax);
		}
	}

	# ローカル掲示板
	if(($num == -4) || ($num == $id)) {
		if( $HmainMode eq 'owner'       || # 開発モード
			$HmainMode eq 'commandJava' || # コマンド入力モード
			$HmainMode eq 'command'     || # コマンド入力モード
			$HmainMode eq 'command2'    || # コマンド入力モード（ver1.1より追加・自動系用）
			$HmainMode eq 'comment'     || # コメント入力モード
			$HmainMode eq 'fleetname'   || # 艦隊名変更モード
			$HmainMode eq 'priority'    || # 索敵順変更モード
			$HmainMode eq 'earth'       || # 周辺表示設定モード
			$HmainMode eq 'comflag'     || # コマンド実行設定モード
			$HmainMode eq 'preab'       || # 陣営共同開発モード
			$HmainMode eq 'lbbs'        || # ローカル掲示板モード
			$HmainMode eq 'landmap'     || # 観光モード
			$HmainMode eq 'new'         || # 島の新規作成
			$HmainMode eq 'print'       || # 観光モード
			$HmainMode eq 'reload'      || # 保存データ復元モード
			$HmainMode eq 5                # モバイルモード
		) {
			$lbbs = readLbbs($id);
		}
	}

	# 島型にして返す
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

# 地形読み込み
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

# コマンド読み込み
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

# ローカル掲示板読み込み
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

# 全島データ書き込み
sub writeIslandsFile {
	my($num) = @_; # 0だと地形・コマンド・掲示板ログを地形書きこまず
				   # -1だと全地形・全コマンドを書きこむ
				   # -2だと全地形を書きこむ
				   # -3だと全コマンドを書きこむ
				   # -4だと全掲示板ログを書きこむ
				   # 番号だとその島の地形・コマンド・掲示板ログだけは書きこむ

	# ファイルを開く
	open(OUT, ">${HdirName}/hakojima.tmp");

	# 各パラメータ書き込み
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

	# 島の書きこみ
	my($i);
	foreach $i (0..$islandNumber) {
		writeIsland($Hislands[$i], $num, 1);
	}
	# ファイルを閉じる
	close(OUT);

	# 海域
	if($HoceanMode && ($num >= -2)) {
		open(IOUT, ">${HdirName}/worldtmp.${HsubData}");
		writeLand(*IOUT, $Hworld->{'land'}, $Hworld->{'landValue'}, $Hworld->{'landValue2'}, { 'x' => \@defaultX, 'y' => \@defaultY });
		close(IOUT);
		unlink("${HdirName}/world.${HsubData}");
		rename("${HdirName}/worldtmp.${HsubData}", "${HdirName}/world.${HsubData}");
	}

	# 同盟データの書き込み
	writeAllyFile() if($HallyUse || $HarmisticeTurn || ($HmainMode eq 'asetup'));

	# 本来の名前にする
	unlink("${HdirName}/$HmainData");
	rename("${HdirName}/hakojima.tmp", "${HdirName}/$HmainData");
}

# 島ひとつ書き込み
sub writeIsland {
	my($island, $num, $mode) = @_;
	if($mode) {

		my $priority = $island->{'priority'};
		my $fleet = $island->{'fleet'};
		my @fnum = ('第１', '第２', '第３', '第４');
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
	# 地形
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
	# コマンド
	if(($num == -1) || ($num == -3) || ($num == $id)) {
		if($HmainMode eq 'commandJava' || $HmainMode eq 'command2' || $HmainMode eq 'turn' || $HmainMode eq 'command' || $HmainMode eq 'new' || $HmainMode eq 'reload' || $HmainMode eq 'bfield') {
			writeCommand($id, $island->{'command'});
		}
	}
	# ローカル掲示板
	if(($num == -4) || ($num == $id)) {
		if($HmainMode eq 'lbbs' || $HmainMode eq 'new' || $HmainMode eq 'reload' || $HmainMode eq 'bfield') {
			writeLbbs($id, $island->{'lbbs'});
		}
	}
}

# 地形書き込み
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

# コマンド書き込み
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

# ローカル掲示板書き込み
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

# 死滅時データファイル削除処理
sub deleteIslandData {
	my($island) = @_;
	my($id) = $island->{'id'};
	if(!$HoceanMode) {
		unlink("${HdirName}/${id}.${HsubData}");
		unlink("${HdirName}/${id}.${HcommandData}");
		unlink("${HlogdirName}/${id}.${HlbbsData}");
	} else {
		# 海に初期化
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

# 戦闘期間開始時の島の状態を保存(トーナメント)
# mode 0:海軍ごと保存 1:海軍以外を保存
# ***敗者の死滅時保存 island_save($island, $HfightdirName, 'lose', 0);
# ***mode 0セーブ保存 island_save($island, $HsavedirName, 'save', 0);
# ***mode 1セーブ保存 island_save($island, $HsavedirName, 'save', 1, \@land, \@landValue);(ロードデータを渡す)
sub island_save {
	my($island, $dir, $suf, $mode, $oldland, $oldlandValue) = @_;
	my($id) = $island->{'id'};

	my $land = $island->{'land'}; # 現在の地形
	my $landValue = $island->{'landValue'};
	my $map = $island->{'map'};
	my($x, $y);
	my(@saveland, @savelandValue, @stack); # 保存する地形データを構成
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			if($mode && ($land->[$x][$y] == $HlandNavy)) {
				# 保存データのまま
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
					# 保存データのまま
					$saveland[$x][$y] = $oldland->[$x][$y];
					$savelandValue[$x][$y] = $oldlandValue->[$x][$y];
				} else {
					# とりあえずセーブ地形
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
	# スタック地形があればも一度ループ
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

	# 保存ディリクトリのチェック
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

# 保存した島の状態を復元(トーナメント)
# mode 0:海軍ごと復元 1:現データを保存後，海軍ごと復元
# mode 2:海軍以外復元 3:現データ(海軍以外)保存後，海軍以外復元
# mode -1:トーナメント不戦勝時，地形等回復処理
sub island_load {
	my($island, $mode) = @_;
	my($id) = $island->{'id'};

	open(IIN, "${HsavedirName}/${id}_save.${HsubData}");
	chomp(my @line = <IIN>);
	close(IIN);

	my(@tmp) = splice(@line, 0, 36);
	my(@mandf) = splice(@tmp, 8, 25);
	my($money) = shift(@mandf); # 資金
	my($food) = shift(@mandf);  # 食料
#	my($tmp) = pop(@mandf);     # マップ
#	my(@xytmp) = split(/<>/, $tmp);
#	my(@x) = split(/\,/, $xytmp[0]);
#	my(@y) = split(/\,/, $xytmp[1]);
#	my $map = { 'x' => \@x, 'y' => \@y };
#	# 7.12以前のデータのための処理
#	$map = $island->{'map'} if(!@x || !@y);
#	$island->{'map'} = $map;
	$map = $island->{'map'};

	# ロードした生データ
 	my($land, $landValue, $landValue2) = readLand($map, @line);

	if($mode == 1) {
		island_save($island, $HsavedirName, 'save', 0);
	} elsif($mode == 3) {
		island_save($island, $HsavedirName, 'save', 1, $land, $landValue);
	}

	my(@loadland, @loadlandValue, @stack); # ロードする地形データを構成
	if($HoceanMode) {
		@loadland = @{$island->{'land'}};
		@loadlandValue = @{$island->{'landValue'}};
		@loadlandValue2 = @{$island->{'landValue2'}};
	}
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			if(($mode > 1) && ($island->{'land'}[$x][$y] == $HlandNavy)) { # $island->{'land'} 今の地形(セーブする)
				if(($land->[$x][$y] == $HlandSea) || ($land->[$x][$y] == $HlandNavy)) {
					# 今のまま
					$loadland[$x][$y] = $island->{'land'}[$x][$y];
					$loadlandValue[$x][$y] = $island->{'landValue'}[$x][$y];
					$loadlandValue2[$x][$y] = $island->{'landValue2'}[$x][$y];
				} else {
					# とりあえずロード地形
					$loadland[$x][$y] = $land->[$x][$y];
					$loadlandValue[$x][$y] = $landValue->[$x][$y];
					push(@stack, { 'x' => $x, 'y' => $y });
				}
			} elsif(($mode > 1) && ($land->[$x][$y] == $HlandNavy)) {
				if($island->{'land'}[$x][$y] == $HlandNavy) {
					# 今のまま
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
	# スタック地形があればも一度ループ
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

	$island->{'money'} = $money; # 資金
	$island->{'food'} = $food;   # 食料
	$island->{'map'} = $map;     # マップ
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
# 同盟データ入出力
#----------------------------------------------------------------------
# 同盟データ読みこみ
sub readAllyFile {
	# データファイルを開く
	if(!open(IN, "${HdirName}/${HallyData}")) {
		rename("${HdirName}/ally.tmp", "${HdirName}/${HallyData}");
		if(!open(IN, "${HdirName}/${HallyData}")) {
			return 0;
		}
	}

	# 同盟の読みこみ
	my($i);
	$HallyNumber   = int(<IN>); # 同盟の総数
	for ($i = 0; $i < $HallyNumber; $i++) {
		$Hally[$i] = readAlly();
		$HidToAllyNumber{$Hally[$i]->{'id'}} = $i;
	}
	# 加盟している同盟のIDを格納
	for ($i = 0; $i < $HallyNumber; $i++) {
		my $member  = $Hally[$i]->{'memberId'};
		foreach (@$member) {
			my $n = $HidToNumber{$_};
			next unless(defined $n);
			push(@{$Hislands[$n]->{'allyId'}}, $Hally[$i]->{'id'});
		}
	}

	# ファイルを閉じる
	close(IN);

	return 1;
}

# 同盟ひとつ読みこみ
sub readAlly {
	my($name, $mark, $color, $id, $ownerName, $password, $jpass, $score, $number,
		$occupation, $tmp, @allymember, @ext, $comment, $title, $message, @veto, $vkind);
	chomp($name = <IN>);  # 同盟の名前
	chomp($mark = <IN>);  # 同盟の識別マーク
	chomp($color = <IN>); # 識別マークの色
	$id = int<IN>;        # 同盟ID（主催者のものと一緒）
	chomp($ownerName = <IN>); # 主催者の島の名前
	chomp($password = <IN>);  # パスワード（主催者のものと一緒）
	chomp($jpass = <IN>);     # パスワード（Takayanのjpass:ターン更新時に書き換え）
	$score = int(<IN>);       # 同盟のスコア
	$number = int(<IN>);      # 同盟に属する島の数
	$occupation = int(<IN>);  # 占有率
	chomp($tmp = <IN>);       # 同盟所属島ID
	@allymember = split(/\,/,$tmp);
	chomp($tmp = <IN>);       # 拡張領域
	@ext = split(/\,/,$tmp);
	#$name = $HwinnerMark . $name if($ext[5]);
	chomp($comment = <IN>);   # コメント
	chomp(($title, $message) = split('<>', <IN>)); # タイトル,メッセージ
	chomp($tmp = <IN>);       # 拒否ID
	@veto = split(/\,/,$tmp);
	$vkind = shift @veto;
	<IN>; # 予備
	<IN>; # 予備

	# 陣営型にして返す
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

# 同盟データ書き込み
sub writeAllyFile {
	# ファイルを開く
	open(OUT, ">${HdirName}/ally.tmp");

	# 陣営データの書きこみ
	print OUT "$HallyNumber\n";
	for($i = 0; $i < $HallyNumber; $i++) {
		writeAlly($Hally[$i]);
	}
	# ファイルを閉じる
	close(OUT);

	# 本来の名前にする
	unlink("${HdirName}/${HallyData}");
	rename("${HdirName}/ally.tmp", "${HdirName}/${HallyData}");
}

# 同盟ひとつ書き込み
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
	#拡張領域
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

# [a-zA-Z]で構成される8文字のパスワードを作る
sub makeRandomString {
	my($baseString) = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	my($baseLen) = length($baseString);
	my($i, $passward);

	foreach $i (1..8) {
		$passward .= substr($baseString, rand($baseLen), 1);
	}

	return $passward;
}

# 同盟の占有率の計算
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

# 島放棄の時の同盟関連処理
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
# 過去ログ処理(YY-BBS)
#----------------------------------------
sub make_pastlog {
	my($id, $name) = @_;
	# ログファイル
	my $logfile = "${HbbsdirName}/${id}$Hlogfile_name";
	return if !(-f $logfile);
	open(IN,"$logfile")  || die $!;
	my $top = <IN>;
	close(IN);
	my $allyName = (split(/<>/, $top))[3];
	$allyName =~ s/作戦会議室//;
	my $logfileNew = "${HbbsdirName}/${id}-${HislandTurn}$Hlogfile_name";
#	return if !(-f $logfile);
	rename($logfile, $logfileNew);
	# 盟主ログファイル
	my $logfile2 = "${HbbsdirName}/${id}$Hlogfile2_name";
	my $logfile2New = "${HbbsdirName}/${id}-${HislandTurn}$Hlogfile2_name";
	return if !(-f $logfile2);
	rename($logfile2, $logfile2New);
	# カウンタファイル
	if($Hcounter) {
		my $cntfile = "${HbbsdirName}/${id}$Hcntfile_name";
		my $cntfileNew = "${HbbsdirName}/${id}-${HislandTurn}$Hcntfile_name";
		return if !(-f $cntfile);
		rename($cntfile, $cntfileNew);
	}
	# 過去ログ用NOファイル
	if($Hpastkey) {
		my $nofile  = "${HbbsdirName}/${id}$Hnofile_name";
		return if !(-f $nofile);
		# 過去NOを開く
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
	# 消滅した同盟のデータを保存
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

# 島名を返す
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

# 地形の呼び方
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
		# 複合地形
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		return $HcomplexName[$cKind];
	} elsif($land == $HlandMonster) {
		# 怪獣
		my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$mKind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$mId}]) if (defined $HidToNumber{$mId});
		$mName .= "(${name})" if (defined $name);
		return $mName;
	} elsif($land == $HlandHugeMonster) {
		# 巨大怪獣
		my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$mKind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$mId}]) if (defined $HidToNumber{$mId});
		$mName .= "(${name})" if (defined $name);
		return $mName;
	} elsif($land == $HlandNavy) {
		# 海軍
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($lv);
		my $nName = $HnavyName[$nKind];
		$nName .= 'の残骸' if($nFlag == 1);
		my($name);
		$name = islandName($Hislands[$HidToNumber{$nId}]) if (defined $HidToNumber{$nId});
		my $nSpecial = $HnavySpecial[$nKind];
		if(!($nSpecial & 0x8) && !($nFlag & 1)) {
			if(defined $HidToName{$nId}) {
				$nName .= "(${name})";
			} else {
				$nName .= "(所属不明)";
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

# 範囲内の軍港を近い順に探して座標を返す。$rangeが0の場合、周囲12(20)ヘックスを調査後、全島調査。
sub searchNavyPort {
	my($island, $x, $y, $range, $plane, $id) = @_; #$planeフラグとオーナーフラグを追加
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
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
		next if(($sx < 0) || ($sy < 0) || ($HoceanMode && ($HlandID[$sx][$sy] != $island->{'id'})));

		if($land->[$sx][$sy] == $HlandNavy) {
			my($nId, $nFlag, $nKind, $nWait) = (navyUnpack($landValue->[$sx][$sy]))[0, 5, 7, 8];
			my $nSpecial = $HnavySpecial[$nKind];

                        # 航空機フラグ立ってない場合は港だけ 立ってたら空母も見て、発艦フラグも確認
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
			next if($HoceanMode && ($HlandID[$sx][$sy] != $island->{'id'})); # 念のため
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


# 周囲から陸地を数える
sub searchLand {
	my($island, $x, $y) = @_;
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my ($sx, $sy, $i);
        my $count = 0;
	for($i == 1; $i <= 6; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		# 範囲外の場合
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

# 島のない座標をランダムに返す
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

# 島同士のつながりを調べるメイン
sub makeRen {
	# @correct生成($correct[$sx + $#an])
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
			if($HoceanMap[$x][$y]) { # 島がある
				my($num) = $HidToNumber{$HoceanMap[$x][$y]};
				if((defined $num) &&
					( # 接続しない島
					$Hislands[$num]->{'predelete'} ||  # 管理人あずかり
					$Hislands[$num]->{'rest'} || # 不戦勝
					($HfieldUnconnect && $Hislands[$num]->{'field'}) # 設定時，バトルフィールド
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

# 島同士のつながりを調べるサブ
sub classRen {
	my($x, $y, $ren) = @_;
	return if(!$HoceanMap[$x][$y]); # 未知の海域
	return if($HislandConnect[$x][$y]); # 調査済み
	$HislandConnect[$x][$y] = $ren;
	my($sx, $sy);
	my(@check) = ([-1, 0], [1, 0], [0, -1], [0, 1]); # 左，右，上，下
	if(!($HislandSizeY % 2)) {
		push(@check, [-1, 1]);  # 左下
		push(@check, [1, -1]);  # 右上
	} elsif(!($HoceanSizeY % 2)) {
		if($y % 2) {
			push(@check, [-1, -1]); # 左上
			push(@check, [-1, 1]);  # 左下
		} else {
			push(@check, [1, -1]);  # 右上
			push(@check, [1, 1]);   # 右下
		}
	} else {
		if($y % 2) {
			push(@check, [-1, -1]); # 左上
			push(@check, [-1, 1]) if($y < $HoceanSizeY - 1);  # 左下
		} else {
			push(@check, [1, -1]) if($y);  # 右上
			push(@check, [1, 1]);   # 右下
		}
	}
	foreach (@check) {
		$sx = $RcorrectX[$x + $_->[0] + 1];
		$sy = $RcorrectY[$y + $_->[1] + 1];
		next if (($sx < 0) || ($sy < 0));
		# 範囲内の場合
		classRen($sx, $sy, $ren);
	}
	return 1;
}

# 海のつながりを調べるメイン
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

# 海のつながりを調べるサブ
sub classSeaRen {
	my($land, $x, $y, $rensea) = @_;
	return if($island->{'seaconnect'}->[$x][$y] || ($land->[$x][$y] != $HlandSea));
	$island->{'seaconnect'}->[$x][$y] = $rensea;
	my($sx, $sy);
	foreach (1..6) {
		$sx = $x + $ax[$_];
		$sy = $y + $ay[$_];
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		$sx = $correctX[$sx + $#an];
		$sy = $correctY[$sy + $#an];
		next if (($sx < 0) || ($sy < 0));
		# 範囲内の場合
		classSeaRen($land, $sx, $sy, $rensea);
	}
	return 1;
}
#----------------------------------------------------------------------
# 地形データ
#----------------------------------------------------------------------
# 地形の情報を Unpack
sub landUnpack {
	my $lv = shift;

	# bit 意味
	#-----------
	#  8  予備
	#  5  種類
	#  9  ターンフラグ
	#  6  食料フラグ
	#  6  資金フラグ
	my $money = $lv & 0x3f;  $lv >>= 6;
	my $food  = $lv & 0x3f;  $lv >>= 6;
	my $turn  = $lv & 0x1ff; $lv >>= 9;
	my $kind  = $lv & 0x1f; $lv >>= 5;
	my $tmp   = $lv & 0xff;

	return ($tmp, $kind, $turn, $food, $money);
}

# 地形の情報を Pack
sub landPack {
	my($tmp, $kind, $turn, $food, $money) = @_;

	# bit 意味
	#-----------
	#  8  予備
	#  5  種類
	#  9  ターンフラグ
	#  6  食料フラグ
	#  6  資金フラグ
	my $lv = 0;
	$lv |= $tmp   & 0xff;  $lv <<= 5;
	$lv |= $kind  & 0x1f;  $lv <<= 9;
	$lv |= $turn  & 0x1ff; $lv <<= 6;
	$lv |= $food  & 0x3f;  $lv <<= 6;
	$lv |= $money & 0x3f;

	return $lv;
}

# 怪獣の情報を Unpack
sub monsterUnpack {
	my $lv = shift;

	# bit 意味
	#-----------
	#  8  島ID
	#  3  巨大怪獣フラグ
	#  1  浅瀬フラグ
	#  8  経験値
	#  2  フラグ
	#  5  種類
	#  5  耐久力
	my $hp    = $lv & 0x1f; $lv >>= 5;
	my $kind  = $lv & 0x1f; $lv >>= 5;
	my $flag  = $lv & 0x03; $lv >>= 2;
	my $exp   = $lv & 0xff; $lv >>= 8;
	my $sea   = $lv & 0x01; $lv >>= 1;
	my $hflag = $lv & 0x07; $lv >>= 3;
	my $id    = $lv;

	return ($id, $hflag, $sea, $exp, $flag, $kind, $hp);
}

# 怪獣の情報を Pack
sub monsterPack {
	my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = @_;

	# bit 意味
	#-----------
	#  8  島ID
	#  3  巨大怪獣フラグ
	#  1  浅瀬フラグ
	#  8  経験値
	#  2  フラグ
	#  5  種類
	#  5  耐久力
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

# 海軍の情報を Unpack
sub navyUnpack {
        my ($lv, $lv2);
	$lv = shift;
        $lv2 = shift;

	# bit 意味
	#-----------
	#  7  島ID
	#  1  予備
	#  2  状態
	#  1  浅瀬フラグ
	#  8  経験値
	#  2  フラグ
	#  2  艦隊番号
	#  5  種類
	#  4  耐久力

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

# 海軍の情報を Pack
sub navyPack {
	my($id, $temp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = @_;

	# bit 意味
	#-----------
	#  7  島ID
	#  1  予備
	#  2  状態
	#  1  浅瀬フラグ
	#  8  経験値
	#  2  フラグ
	#  2  艦隊番号
	#  5  種類
	#  4  耐久力
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
# パスワードチェック
#----------------------------------------------------------------------
sub checkPassword {
	my($island, $p2) = @_;
	my $p1 = $island->{'password'};

	# nullチェック
	if($p2 eq '') {
		return 0;
	}

	# マスタパスワードチェック
	if(checkMasterPassword($p2)) {
		return 2;
	}

	# 本来のチェック
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

# マスタパスワードのチェック
sub checkMasterPassword {
	my $pass = shift;
	return (crypt($pass, 'ma') eq $HmasterPassword);
}

# 特殊パスワードのチェック
sub checkSpecialPassword {
	my $pass = shift;
	return (crypt($pass, 'sp') eq $HspecialPassword || crypt($pass, 'ma') eq $HmasterPassword);
}

# パスワードのエンコード
sub encode {
	my $pass = shift;
	return ($cryptOn ? crypt($pass, 'h2') : $pass);
}

# パスワード間違い
sub tempWrongPassword {
	if($HinputPassword eq '') {
		tempWrong("<span class=\"big\">パスワードを忘れていませんか？</span>"); # パスワード未入力
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
<span class="big">パスワードが違います。
<A HREF=\"$HthisFile\">トップへ戻る</span></A>
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
		my $day = ('日','月','火','水','木','金','土')[$wday];
		$year = $year + 1900;
		$mon = $mon + 1;
		my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
		out(<<END);
<HR>
<TABLE><TR><TH><span class="big">【${HtagDisaster_}！警告！${H_tagDisaster}】</span></TH></TR>
<TR><TD>あなたの情報を記録させていただきました。
　$date<BR>　<B>$host - $addr - $agent</B>
</TD></TR>
<TR><TD class='N'>
<BR>　<A HREF='http://www.ipa.go.jp/security/ciadr/law199908.html' target='_blank'><B>不正アクセス行為の禁止等に関する法律</B></A>が2001年2月13日に施行されました。
<BR><BR>　この法律は、ハイテク犯罪の防止と高度情報通信社会の健全な発展を目的としたもので、刑法で処罰できない部分を対象とする法律です。
<BR><BR>　刑法では、何らかの被害が出ないと罰することはできなかったのですが、不正アクセス禁止法では、
${HtagDisaster_}不正アクセスを行った時点で処罰の対象となります。${H_tagDisaster}
<BR><BR>　実際の法律を噛み砕いて説明すると、
『<A HREF='http://www.ipa.go.jp/security/ciadr/law199908.html#不正アクセス行為' target='_blank'><B>不正アクセス</B></A>とは、<B>パスワード等で保護された領域に、権限のないものが勝手にアクセスすること</B>』で、
これに違反した場合、『${HtagDisaster_}懲役１年以下、又は、５０万円以下の罰金${H_tagDisaster}』が科せられることになります。
<BR><BR>　単なる「パスワードの入力ミス」であればよいのですが、あまりにも頻繁であれば、<B>管理者として相応の措置をとらざるを得ません。</B>
<BR><BR>　${HtagTH_}繰り返しパスワードエラーが発生した場合、何か特別な理由があるのでしたら、この下にあるリンクの「掲示板」もしくは「メール」にてご連絡くださいますようお願いいたします。${H_tagTH}
</TD></TR></TABLE>
END
	}
}

# ID違いorローカル設定していないorクッキー設定していない
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
# アクセスログ取得
#----------------------------------------------------------------------
sub axeslog {
	my($mode, $error) = @_;

	# 「クロスサイトスクリプティング脆弱性」への対応
	# http://espion.s7.xrea.com/diary/20031027.html#p02 より
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
	my $day = ('日','月','火','水','木','金','土')[$wday];
	$year = $year + 1900;
	$mon = $mon + 1;
	my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
	my($pcheck);
	if($proxycheck) {
		my @proxy_env = (
			'HTTP_CACHE_CONTROL', # FORM送信時にno_cacheになるみたい(・_・?
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
#			print OUT jcode::sjis($line); # jcode使用時
			print OUT $line;
		}
		close(OUT);
	} else {
		tempProblem();
		return;
	}
}
#----------------------------------------------------------------------
# 入出力
#----------------------------------------------------------------------

# 標準出力への出力
sub out {
#	print STDOUT jcode::sjis($_[0], 'euc'); # jcode使用時
	print STDOUT $_[0];
}

# デバッグログ
sub HdebugOut {
	if($Hdebug) {
		open(DOUT, ">>debug.log");
		print DOUT ($_[0]);
		close(DOUT);
	}
}

# 時間の取得
sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($_[0] + $Hjst);
	$mon++;
	$year += 1900;
	my $timestring = sprintf("%04d年 %02d月 %02d日 %02d時", $year, $mon, $date, $hour);
	$timestring .= sprintf(" %02d分", $min) if($min || $sec);
	$timestring .= sprintf(" %02d秒", $sec) if($sec);

#	return "${year}年 ${mon}月 ${date}日 ${hour}時 ${min}分 ${sec}秒";
	return $timestring;
}

# エスケープ文字の処理
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
		$s =~ s/(<br>){5,}//g; # 大量改行対策
	}
	return $s;
}

#----------------------------------------------------------------------
# cookie
#----------------------------------------------------------------------
# cookie入力
sub cookieInput {
	# 海戦クッキー
	local($key, $val, *cook);

	# クッキー取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
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

# cookie出力
sub cookieOutput {
	my($cookie, $gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 14 *24*60*60); # 期限14日
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 海戦クッキー
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

	# 保存データをURLエンコード
	foreach (@data) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cookie .= "$_<>";
	}

	out("$cookie; expires=$gmt\n");
}

1;