# The Return of Neptune: http://no-one.s53.xrea.com/
# 海戦JS版用に改変
#----------------------------------------------------------------------
# 箱庭トーナメント２
# 携帯端末モジュール
# $Id: hako-mobile.cgi 60 2005-01-23 07:22:47Z takayama $
#----------------------------------------------------------------------

McgiInput();

tempHeader();

if($HmainMode eq 'turn') {
	# ターン更新待ち
	MturnPageMain();
} elsif($HmainMode eq 0) {
	# 観光画面
	MprintMain(0);
} elsif($HmainMode eq 1) {
	# 出来事
	MlogMain();
} elsif($HmainMode eq 2) {
	# 開発画面 オーナー
	MprintMain(1);
} elsif($HmainMode eq 3) {
	# 計画一覧
	McmdMain(0);
} elsif($HmainMode eq 4) {
	# 計画入力
	McmdMain(1);
} elsif($HmainMode eq 5) {
	# 掲示板
	MlbbsMain();
} elsif($HmainMode eq 'command') {
	# 計画入力
	McmdInputMain();
} elsif($HmainMode eq 'TimeTable') {
	# 島番号一覧
	MlistPageMain();
} elsif($HmainMode eq 'setupv') {
	# 地形一覧
	MhelpPageMain();
} elsif($HmainMode eq 'FightView') {
	# リンク
	MlinkPageMain();
} else {
	MtopPageMain();
}

tempFooter();

#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------

# CGI 読み込み
sub McgiInput {
	my $getLine = $ENV{'QUERY_STRING'};

	if($getLine =~ /ID=([0-9]+)/){
		$HcurrentID = $1;
	}
	if($getLine =~ /PS=([^\&]*)/){
		$HinputPassword = $1;
	}
	if($getLine =~ /MP=([0-9]+)/){
		$HinputPassword2 = $1;
	}

	if($HmainMode eq 'print') {
		$HmainMode = 0;
	}

	$HinputPassword2 =~ tr/0-9//cd;
}

# 島の存在確認
sub MexistCheck {
	my $mode = shift;
	unlock() if(!$mode);

	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		tempProblem();
		return 1;
	}

	return 0;
}

# パスワードチェック
sub MpassCheck {
	my $island = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		return 1;
	}

	return 0;
}

# 地図モード
sub MprintMain {
	my $mode = shift;

	if(MexistCheck()) {
		return;
	}
	if($mode) {
		if(MpassCheck()) {
			return;
		}
	}

	MislandInfo($mode); # 島の情報
	MislandMap($mode); # 島の地図
}

# 出来事
sub MlogMain {
	my $mode = 0;

	if(MexistCheck()) {
		return;
	}

	if($HinputPassword) {
		if(MpassCheck()) {
			return;
		}

		$mode = 1;
	}

	MtoMapLink($mode);

	logFilePrint(0, $HcurrentID, $mode, 2);
}

# 掲示板
sub MlbbsMain {
	my $mode = 0;

	if(MexistCheck()) {
		return;
	}

	if($HinputPassword) {
		if(MpassCheck()) {
			return;
		}

		$mode = 1;
	}

	MtoMapLink($mode);

	MlbbsContents($mode);
	unlock();

}

# ローカル掲示板内容
sub MlbbsContents {
	my($mode) = @_;
	my($lbbs, $line, $no);
	$lbbs = readLbbs($HcurrentID);
	$no = @lbbs;
	out(<<END) if($lbbs->[0] ne '0<<0>>' && $lbbs->[0] ne '');
No:[投稿日]投稿者>内容($AfterName名)<BR>
=========================<BR>
END

	my($i);
	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	for($i = 0; $i < $HlbbsView; $i++) {
		$line = $lbbs->[$i];
		next if($line eq '0<<0>>' || $line eq '');
		if($line =~ /([0-9]*)\<(.*)\<(.*)\>(.*)\>(.*)$/) {
			my($m, $iName, $oda, $tan, $com) = ($1, $2, $3, $4, $5);
			$com =~ s/(http|ftp):\/\/([^\x81-\xFF\s\"\'\(\)\<\>\\\`\[\{\]\}\|]+)/<A href=\"$1:\/\/$2\" onclick=\"location.href=\'${HaxesFile}?$1:\/\/$2\'\; return false\;\" target=\"_blank\">$HlbbsAutolinkSymbol<\/A>/g if($HlbbsAutolinkSymbol ne '');
			my($j) = $i + 1;
			out("<B>$j</B>:");
			my($speaker);
			my($sName, $sID) = split(/,/, $iName);
			my($os, $date, $addr) = split(/,/, $oda);
			my($turn, $name) = split(/：/, $tan);
			$tan = "[${date}]$name";
			my $sNo = $HidToNumber{$sID};
			if($sName ne '') {
				if(defined $sNo){
					$speaker = "(<A HREF=\"$HthisFile?Sight=$sID&MP=$HinputPassword2\">$sName</A>)";
				} else {
					$speaker = "($sName)";
				}
			}
			if($os == 0) {
				# 観光者
				if ($m == 0) {
					# 公開
					if($sID ne '0') {
						out("$tan > ${com} $speaker<BR>");
					} else {
						out("$tan > ${com} $speaker<BR>");
					}
				} else {
					# 極秘
					if (!$mode) {
						# 観光客
						out("- 極秘 -<BR>");
					} else {
						# オーナー
						out("$tan >(秘) ${com} $speaker<BR>");
					}
				}
			} else {
				# 島主
				out("$tan > ${com} $speaker<BR>");
			}
		}
	}
}

# 開発計画
sub McmdMain {
	my $mode = shift;

	if(MexistCheck() or MpassCheck()) {
		return;
	}

	MtoMapLink(1);
	out("<HR>");
	if($mode == 0) {
		McmdListPageMain($HcommandMax);
	} else {
		McmdInputPageMain();
	}
}

# 開発計画入力処理
sub McmdInputMain {
	if(MexistCheck(1) or MpassCheck()) {
		unlock();
		return;
	}

	require('hako-map.cgi');

	my $island  = $Hislands[$HcurrentNumber];

	$HcommandPlanNumber--;

	commandAdd($island);

	unlock();

#	$HcommandPlanNumber++;
	MtoMapLink(1);
	out("<HR>");
	McmdInputPageMain();
}

# 島の情報
sub MislandInfo {
	my $mode = shift;
	my $island = $Hislands[$HcurrentNumber];

	# 情報表示
	my $rank = $HcurrentNumber + 1 - $HbfieldNumber;
	my $pop = $island->{'pop'};
	my $area = $island->{'area'};
	my $food = $island->{'food'};
	my $farm = $island->{'farm'};
	my $factory  = $island->{'factory'};
	my $mountain = $island->{'mountain'};
	my $name;

	# 人口の表示
#	$pop = (!$Hhide_town || $mode == 1) ? $island->{'pop'}.$HunitPop : aboutPop($island->{'pop'});

	$pop =  ($pop == 0) ? "-" : "${pop}$HunitPop";
	1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$area     = ($area == 0) ? "-" : "${area}$HunitArea";
	1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$food     = ($food == 0) ? "-" : "${food}$HunitFood";
	1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$farm     = ($farm == 0) ? "-" : "${farm}0$HunitPop";
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$factory  = ($factory == 0) ? "-" : "${factory}0$HunitPop";
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$mountain = ($mountain == 0) ? "-" : "${mountain}0$HunitPop";
	1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$farm     = "機密" if($Hhide_farm == 2);
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$factory  = "機密" if($Hhide_factory == 2);
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;

	# 予選期間、失業者が上限を上回っていたら警告
	my $mStr1 = '';
	if($Htournament && ($HislandTurn < $HyosenTurn)) {
		my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
		$tmp = 0 if($tmp < 0);
		$mStr1 = "<FONT COLOR=RED>失業者が".$Hno_work.$HunitPop.
		"以上出ているので、人口増加がストップします。生産施設を建てて下さい。</FONT><br>" if($tmp >= $Hno_work);
		1 while $mStr1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	}

	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($mode == 1)) {
		# 無条件またはownerモード
		$mStr2 = "$island->{'money'}$HunitMoney";
	} elsif($HhideMoneyMode == 2) {
		$mStr2 = aboutMoney($island->{'money'});
	}
	1 while $mStr2 =~ s/(.*\d)(\d\d\d)/$1,$2/;

	# 対戦相手の表示
	my $fight_name = '';
	if($island->{'fight_id'} > 0 && $island->{'pop'} > 0) {
		my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
		if($HcurrentNumber ne '') {
			my $tIsland = $Hislands[$HcurrentNumber];
			my $name = '<A HREF="'.$HthisFile."?Sight=$tIsland->{'id'}&MP=$HinputPassword2\">$tIsland->{'name'}$AfterName</A>";
			$fight_name = "相手: $name<br>";
		}
	}

	# 開発停止の表示
	my $rest_msg = '';
	if($island->{'rest'} > 0 && $HislandNumber > 1 && $island->{'pop'} > 0) {
		$rest_msg = "不戦勝により開発停止中　";
		$rest_msg .= "残り<FONT COLOR=RED>".$island->{'rest'}."</FONT>ターン<br>";
	}

	my $cmd;
	if($mode) {
		$name = "$island->{'name'}$AfterName開発画面";
		$cmd  = '<br><input type="submit" name="Mobile3" value="計画一覧">';
		$cmd  .= '<input type="submit" name="Mobile4" value="計画入力">';
	} else {
		$name = "$island->{'name'}$AfterName観光画面";
	}

	out(<<END);
$name<br>
<hr>
順位: $rank<br>
人口: $pop<br>
資金: $mStr2<br>
食料: $food<br>
面積: $area<br>
農場: $farm<br>
工場: $factory<br>
採掘: $mountain<br>
$rest_msg
$fight_name
$mStr1
<hr>
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$island->{'id'}">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" name="Mobile1" value="出来事">
<input type="submit" name="Mobile5" value="掲示板">
$cmd
</form>
<hr>
END
}

# 島の地図
sub MislandMap {
	my $mode = shift;
	my $island = $Hislands[$HcurrentNumber];

	# 地形、地形値を取得
	my($x, $y);
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my(@mx) = @{$island->{'map'}->{'x'}};
	my(@my) = @{$island->{'map'}->{'y'}};
	my @co = ('０','１','２','３','４','５','６','７','８','９');
	# 座標(上)を出力
	foreach $x (@mx) {
		out("$co[($x%10)]");
	}
	out("<br>\n<FONT COLOR=\"#0000FF\">");

	# 各地形および改行を出力
	foreach $y (@my) {
		# 偶数番号なら番号を出力
		if(!($y % 2)) {
			my $line = ($y >= 10) ? $y-10 : $y;
			out($line);
		}

		# 各地形を出力
		foreach $x (@mx) {
			my $l = $land->[$x][$y];
			my $lv = $landValue->[$x][$y];
			MlandString($l, $lv, $x, $y, $mode);
		}

		# 奇数番号なら番号を出力
		if($y % 2) {
			my $line = ($y >= 10) ? $y-10 : $y;
			out($line);
		}

		# 改行を出力
		out("<br>\n");
	}

	out("</FONT>\n");
	out("&nbsp;");
	foreach $x (@mx) {
		out("$co[($x%10)]");
	}
	out("<br>\n");
}

# 1ヘックス
sub MlandString {
	my($l, $lv, $x, $y, $mode) = @_;
	my($point) = "($x,$y)";
	my($alt, $color, $img);

	if(!$mode && $HjammingView) {
		if(($l == $HlandSea) ||
			($l == $HlandSbase) ||
			($l == $HlandSeaMine) ||
			($l == $HlandOil)) {
			$l  = $HlandSea;
			$lv = 2;
		} elsif(($l == $HlandWaste) ||
			($l == $HlandPlains) ||
			($l == $HlandForest) ||
			($l == $HlandTown) ||
			($l == $HlandFarm) ||
			($l == $HlandFactory) ||
			($l == $HlandBase) ||
			($l == $HlandDefence) ||
			($l == $HlandBouha) ||
			($l == $HlandHaribote) ||
			($l == $HlandMountain) ||
			($l == $HlandComplex) ||
			($l == $HlandMonument)) {
			$l  = $HlandWaste;
			$lv = 2;
		} elsif(($l == $HlandMonster) ||
			($l == $HlandHugeMonster)) {
			my($id, $flag) = (monsterUnpack($lv))[0,4];
			if($flag & 2) {
				$l  = $HlandSea;
				$lv = 2;
			} else {
				$l  = $HlandWaste;
				$lv = 2;
			}
		} elsif($l == $HlandCore) {
			if(int($lv/10000)) {
				$l  = $HlandSea;
				$lv = 2;
			} else {
				$l  = $HlandWaste;
				$lv = 2;
			}
		} elsif($l == $HlandNavy) {
			$l  = $HlandSea;
			$lv = 2;
		}
	}

	if($l == $HlandSea) {
		if($lv == 1) {
			# 浅瀬
			$alt = '−';
#			$color = '#0000FF';
		} else {
			# 海
			$alt = '〜';
#			$color = '#0000FF';
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		$alt = '■';
		$color = '#800000';
	} elsif($l == $HlandPlains) {
		# 平地
		$alt = '□';
		$color = '#00F000';
	} elsif($l == $HlandForest) {
		# 森
		$alt = "森";
		$color = '#008800';
	} elsif($l == $HlandTown) {
		my $tName;
		foreach (reverse(0..$#HlandTownValue)) {
			if($HlandTownValue[$_] <= $lv) {
				$tName = $HlandTownName[$_];
				last;
			}
		}
		$alt = substr($tName, 0, 2);
		$color = '#996600';
	} elsif($l == $HlandFarm) {
		# 農場
		$alt = "農";
		$color = '#00FF00';
	} elsif($l == $HlandFactory) {
		# 工場
		$alt = "工";
		$color = '#606060';
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# 観光者の場合
			$alt = '森';
		} else {
			# ミサイル基地
			$alt = "ミ";
		}
		$color = '#008800';
	} elsif($l == $HlandSbase) {
		if($mode == 0) {
			# 観光者の場合
			$alt = '〜';
		} else {
			# ミサイル基地
			$alt = "み";
		}
#		$color = '#0000FF';
	} elsif($l == $HlandDefence) {
		# 防衛施設
		if($HdBaseHide && $mode == 0) {
			$alt = '森';
			$color = '#008800';
		} else {
			$alt = '防';
			$color = '#FF0000';
		}
	} elsif($l == $HlandBouha) {
		# 防波堤
		$alt = "堤";
		$color = '#008800';
	} elsif($l == $HlandSeaMine) {
		# 機雷
		if($mode == 0) {
			$alt = '〜';
		} else {
			$alt = '機';
		}
#		$color = '#0000FF';
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		if($mode == 0) {
			# 観光者の場合は森のふり
			$alt = '森';
		} else {
			$alt = 'ハ';
		}
		$color = '#FF0000';
	} elsif($l == $HlandOil) {
		# 海底油田
		$alt = "油";
		$color = '#00FF00';
	} elsif($l == $HlandMountain) {
		# 山
		if($lv > 0) {
			$alt = "採";
		} else {
			$alt = '山';
		}
		$color = '#C03030';
	} elsif($l == $HlandCore) {
		# コア
		if($HcoreHide && $mode == 0) {
			if(int($lv/10000)) {
				# 海
				$alt = '〜';
#				$color = '#0000FF';
			} else {
				$alt = '森';
				$color = '#008800';
			}
		} else {
			$alt = 'コ';
			$color = '#00FF00';
		}
	} elsif($l == $HlandComplex) {
		# 複合地形
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $cName = $HcomplexName[$cKind];
#		&jcode::tr(\$cName, '0-9A-Za-z', '０-９Ａ-Ｚａ-ｚ');
		$alt = substr($cName, 0, 2);
		$color = '#00FF00';
	} elsif($l == $HlandMonster) {
		# 怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$kind];
#		jcode::tr(\$mName, '0-9A-Za-z', '０-９Ａ-Ｚａ-ｚ');
		$alt = substr($mName, 0, 2);
		$color = '#FF00FF';
	} elsif($l == $HlandHugeMonster) {
		# 巨大怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$kind];
#		jcode::tr(\$mName, '0-9A-Za-z', '０-９Ａ-Ｚａ-ｚ');
		$alt = substr($mName, 0, 2);
		$color = '#FF00FF';
	} elsif($l == $HlandNavy) {
		# 海軍
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $hp) = navyUnpack($lv);
		my $nName = $HnavyName[$kind];
#		jcode::tr(\$nName, '0-9A-Za-z', '０-９Ａ-Ｚａ-ｚ');
		$alt = substr($nName, 0, 2);
#		$color = '#0000FF';
	}

	if($color ne '' && $HinputPassword2 == 1) {
		$alt = "<font color='$color'>$alt</font>";
	} elsif($color eq '#008800' || $color eq '#FF0000') {
		$alt = "<font color='$color'>$alt</font>";
	}

	out $alt;
}

#----------------------------------------------------------------------
# HTML 出力
#----------------------------------------------------------------------
# ターン更新待ち
sub MturnPageMain {
	unlock();

	out("ターン更新待ちです。暫く待ってからアクセスして下さい。");
}

# 島番号一覧
sub MlistPageMain {
	unlock();

	out("[順位] $AfterName番号: $AfterName名<hr>");
	for($i = 0; $i < $HislandNumber; $i++) {
		my $j = $i + 1 - $HbfieldNumber;
		$j = 'BF' if($j <= 0);
		my $island = $Hislands[$i];
		out("[$j] $island->{'id'}: $island->{'name'}$AfterName<br>\n");
	}
}

# 計画入力
sub McmdInputPageMain {
	my $island = $Hislands[$HcurrentNumber];

	$HcommandPlanNumber++;
	$HcommandKind = 0 if($HcommandKind eq '');
	$HcommandArg  = 0 if($HcommandArg eq '');
	$HcommandX    = 0 if($HcommandX eq '');
	$HcommandY    = 0 if($HcommandY eq '');
	$HcommandMode = 'insert' if($HcommandMode eq '');

	out(<<END);
<form action="./hako-main.cgi" method="POST">
計画番号(1〜$HcommandMax)<br>
[1]<input type="text" name="NUMBER" value="$HcommandPlanNumber" size="2" accesskey="1" istyle="4"><br>
<br>

計画<br>
<select name="COMMAND" accesskey="2">
END

	#コマンド
	my($kind, $cost);
	for($i = 0; $i < $HcommandTotal; $i++) {
		my $s;
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($cost eq '0') {
			$cost = '無料';
		} elsif($cost =~ /^\@(.*)$/) {
			$cost = $1;
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		$s = ' selected' if($kind == $HcommandKind);

		out("<option value='$kind'$s>$HcomName[$kind]($cost)\n");
	}

	out(<<END);
</select><br>
<br>
座標(横,縦)<br>
[2]<input type="text" name="POINTX" value="$HcommandX" size="2" accesskey="2" istyle="4"> , 
[3]<input type="text" NAME="POINTY" value="$HcommandY" size="2" accesskey="3" istyle="4"><br>
<br>

数量(0〜49)<br>
[4]<input type="text" name="AMOUNT" value="$HcommandArg" size="2" accesskey="4" istyle="4"><br>
<br>

目標<br>
<select name="TARGETID" accesskey="6">
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<br>
</select><br>
<br>
動作<br>
<input type="radio" name="COMMANDMODE" value="insert" accesskey="5" checked>[5]挿入<br>
<input type="radio" name="COMMANDMODE" value="write" accesskey="6">[6] 上書き<br>
<input type="radio" name="COMMANDMODE" value="delete" accesskey="7">[7] 削除<br>
<br>
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" value="計画送信" name="CommandButton$island->{'id'}">
</form>
<hr>
END
	McmdListPageMain(int($HcommandMax/2));
}

# 計画一覧
sub McmdListPageMain {
	my $max = shift;

	for($i = 0; $i < $max; $i++) {
		MtempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
	}
}

# 計画表示
sub MtempCommand {
	my($number, $command) = @_;
	my($kind, $target, $x, $y, $arg, $target2) =
	(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'target2'}
	);
	my $name  = "${HcomName[$kind]}";
	my $point = "($x,$y)";

	my($j) = sprintf("[%02d] ", $number + 1);

	out("$j");

	if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) || ($kind == $HcomGiveup)) {
		# コマンド名のみ(座標なし)
		out($name);
	} elsif ((($HcomMissile[0] < $kind) && ($kind <= $HcomMissile[$#HmissileName])) || ($kind == $HcomNavyTarget)) { # ミサイル発射
		# 対象島あり(座標付き)
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "無人$AfterName" : "${target}$AfterName";

		$name =~ s/発射//;
		if($arg == 0 || ($kind == $HcomNavyTarget)) {
			out("${name}=>${target}${point}");
		} else {
			out("${name}x$arg=>${target}${point}");
		}
	} elsif(($kind == $HcomAmity) ||
		($kind == $HcomAlly) ||
		($kind == $HcomDeWar) ||
		($kind == $HcomCeasefire) ||
		($kind == $HcomSendMonster) ||
		($kind == $HcomSendMonsterST) ||
		($kind == $HcomNavySend) ||
		($kind == $HcomNavyReturn) ||
		($kind == $HcomMoveTarget) ||
		($kind == $HcomNavyMission)) {
		# 対象島あり(座標なし)
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "無人$AfterName" : "${target}$AfterName";

		$name =~ s/発射//;
		if($arg == 0) {
			out("${name}=>${target}");
		} else {
			out("${name}x${arg}=>${target}");
		}
	} elsif($kind == $HcomNavyMove) {
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "無人$AfterName" : "${target}$AfterName";
		$target2 = $HidToName{$target2};
		$target2 =  ($target2 eq '') ? "無人$AfterName" : "${target2}$AfterName";
		out("${name}=>${target}->${target2}");
	} elsif(($kind == $HcomSell) ||
		($kind == $HcomBuy) ||
		($kind == $HcomPropaganda)) {
		# 回数付き
		if($arg == 0) {
			out("$name");
		} else {
			out("${name}x$arg");
		}
	} elsif(($kind == $HcomFarm) ||
		 ($kind == $HcomFastFarm) ||
		 ($kind == $HcomFactory) ||
		 ($kind == $HcomFastFactory) ||
		 ($kind == $HcomDestroy) ||
		 ($kind == $HcomMoveMission) ||
		 (($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) || # 複合地形建設
		 ($kind == $HcomMountain)) {
		# 座標・回数付き
		if($arg == 0) {
			out("${name}=>${point}");
		} else {
			out("${name}x${arg}=>${point}");
		}
	} else {
		# 座標付き
		out("${name}=>${point}");
	}

	out("<br>\n");
}

# 各種リンク
sub MlinkPageMain {
#	my $bbTime = get_time((stat($bbsLog))[9], 1, 1);
	unlock();

	out(<<END);
- <A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">箱庭諸島スクリプト配布元</A><br>
- <A HREF="http://no-one.s53.xrea.com/">海戦JS改造配布元</A><br>
END
#	out(<<END);
#<BR>
#- <A HREF="$toppage">ホーム</A><br>
#- <A HREF="$bbs">$bbsname</A>$bbTime<br>
#END
}

# マップヘルプ
sub MhelpPageMain {
	unlock();

	out(<<END);
<font color="#0000FF">−</font> → 浅瀬<br>
<font color="#0000FF">〜</font> → 海<br>
<font color="#800000">■</font> → 荒地<br>
<font color="#00F000">□</font> → 平地<br>
<font color="#008800">森</font> → 森<br>
<br>
<font color="#00FF00">農</font> → 農場<br>
<font color="#606060">工</font> → 工場<br>
<font color="#C03030">採</font> → 採掘場<br>
<font color="#C03030">山</font> → 山<br>
<font color="#00FF00">油</font> → 海底油田<br>
<br>
<font color="#008800">ミ</font> → ミサイル基地<br>
<font color="#0000FF">み</font> → 海底基地<br>
<font color="#FF0000">防</font> → 防衛施設<br>
<font color="#FF0000">ハ</font> → ハリボテ<br>
<font color="#008800">堤</font> → 防波堤<br>
<font color="#0000FF">機</font> → 機雷<br>
<font color="#FF00FF">コ</font> → コア<br>
<br>
END

	out("【都市系】<br>");
	foreach(@HlandTownName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#996600\">$alt</font> → $_<br>");
	}
	out("【複合地形】<br>");
	foreach(@HcomplexName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#00FF00\">$alt</font> → $_<br>");
	}
	out("<br>【海軍】<br>");
	foreach(@HnavyName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#0000FF\">$alt</font> → $_<br>");
	}
	out("<br>【怪獣】<br>");
	foreach(@HmonsterName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#FF00FF\">$alt</font> → $_<br>");
	}
	out("<br>【巨大怪獣】<br>");
	foreach(@HhugeMonsterName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#FF00FF\">$alt</font> → $_<br>");
	}
}

# トップページ
sub MtopPageMain {
	unlock();

	if($HinputPassword2 ne '') {
		$sL[$HinputPassword2] = ' selected';
	} else {
		$sL[1] = ' selected';
	}

	if($HislandNumber > 1 || $HislandTurn == 0) {
		#　時間表示
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		if ($sec < 0 or $HislandTurnCount > 1){
			out("(ターン更新待ちです。暫く待ってからアクセスして下さい。)");
		} else {
			if(!$Htime_mode) {
				my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
				out("次回更新日時 $mon2月$mday2日$hour2時$min2分<br>残り $hour時間 $min分 $sec秒");
			} else {
				out("（次のターンまで、あと $hour時間 $min分 $sec秒）");
			}
		}
	}

	out(<<END);
<hr>
<form action="./hako-main.cgi" method="POST">
ID:<input type="text" name="ISLANDID" size="3" value="$HcurrentID" istyle="4"><br>
PS:<input type="text" name="PASSWORD" size="6" value="$HinputPassword" istyle="3"><br>
カラーモード:<br>
<select name="PASSWORD2">
<option$sL[0] value="0">標準
<option$sL[1] value="1">フルカラー
</select><br>
<input type="submit" name="Mobile2" value="開発">
<input type="submit" name="Mobile0" value="観光">
<input type="submit" name="Mobile1" value="出来事">
<input type="submit" name="Mobile5" value="掲示板">
</form>

<br>
<a href="./hako-main.cgi?TimeTable=1">$AfterName番号一覧</a> 
END
}

# 地図画面へのフォームリンク
sub MtoMapLink {
	my $mode = shift;

	my $name = ($mode) ? '開発' : '観光';
	my $num  = ($mode) ? 2 : 0;

	out(<<END);
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$HcurrentID">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" name="Mobile${num}" value="${name}画面">
<input type="submit" name="Mobile5" value="掲示板">
</form>
END
}

sub get_time {
	my $time = $_[0];
	my($sec,$min,$hour,$mday,$mon) = localtime($time);
	$mon  = "0".$mon  if($mon++ < 9);
	$mday = "0".$mday if($mday  < 10);
	$hour = "0".$hour if($hour  < 10);
	$min  = "0".$min  if($min	< 10);
	if($_[1] == 1) {
		return '' if($time == 1);
		if($time + 60000 < time()) {
			$date = sprintf("</b>%02d/%02d<b>", $mon,$mday);
		} else {
			$date = sprintf("<b>%02d:%02d</b>", $hour,$min);
		}
		return "(${date})";
	}
	return ($sec,$min,$hour,$mday,$mon);
}

1;

