#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# 各種一覧モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 友好国設定一覧
#----------------------------------------------------------------------
sub amityInfo() {
	# 開放
	unlock();
	my($title) = '';
	$title = '友好国' if($HuseAmity);
	if($HuseDeWar) {
		$title .= '・' if($HuseAmity);
		$title .= '交戦国';
	}

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='campInfo'>
<H1>$title 一覧</H1>
<span class='number'>◎</span>：友好(相互)　
<span class='number'>○</span>：友好　
${HtagDisaster_}Ｘ${H_tagDisaster}：交戦(宣戦布告)　
${HtagDisaster_}x${H_tagDisaster}：交戦(被宣戦布告)　
−：中立
<TABLE BORDER><TR>
<TH $HbgTitleCell>${HtagTH_}$title${H_tagTH}</TH>
END

	my($number, $island, $name, $i, %warFlag);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($id1) = $HwarIsland[$i+1];
		my($id2) = $HwarIsland[$i+2];
		my($tn1) = $HidToNumber{$id1};
		my($tn2) = $HidToNumber{$id2};
		next if(($tn1 eq '') || ($tn2 eq ''));
		$warFlag{"$id1,$id2"} = 1;
	}
	foreach ($HbfieldNumber..$islandNumber) {
		$number = $_;
		$island = $Hislands[$number];
		$name = islandName($island);
		out(<<END);
<TD class='T'>$name</TD>
END
	}
	my $aStr = ($HarmisticeTurn) ? '陣営' : '同盟';
	out("<TH $HbgTitleCell>${HtagTH_}${aStr}${H_tagTH}</TH>\n") if($HallyNumber);
	out("</TR>\n");
	foreach ($HbfieldNumber..$islandNumber) {
		$island = $Hislands[$_];
		$name = islandName($island);
		my($id, $amity, %amityFlag, $aId);
		$id = $island->{'id'};
		$amity = $island->{'amity'};
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
		out("<TR>\n<TH $HbgTitleCell>$name</TH>\n");
		foreach $number ($HbfieldNumber..$islandNumber) {
			$aId = $Hislands[$number]->{'id'};
			my($tAmity, %tAmityFlag);
			$tAmity = $Hislands[$number]->{'amity'};
			foreach (@$tAmity) {
				$tAmityFlag{$_} = 1;
			}
			if($id == $aId) {
				out("<TD align='center'>＝</TD>\n");
			} elsif($amityFlag{$aId}) {
				if($tAmityFlag{$id}) {
					out("<TD align='center'><span class='number'>◎</span></TD>\n");
				} else {
					out("<TD align='center'><span class='number'>○</span></TD>\n");
				}
			} elsif($warFlag{"$id,$aId"}) {
				out("<TD align='center'>${HtagDisaster_}Ｘ${H_tagDisaster}</TD>\n");
			} elsif($warFlag{"$aId,$id"}) {
				out("<TD align='center'>${HtagDisaster_}x${H_tagDisaster}</TD>\n");
			} else {
				out("<TD align='center'>−</TD>\n");
			}
		}
		my $AllyInfo;
		if($HallyNumber){
			my $aNo = random(100);
			$aNo *= 10;
			for ($i = 0; $i < $HallyNumber; $i++) {
				my $ally  = $Hally[$i];
				my $member = $Hally[$i]->{'memberId'};
				my $flag = 1;
				foreach (@$member) {
					if($island->{'id'} == $_) {
						$flag = 0;
						last;
					}
				}
				next if($flag);
				my $allyId  = $ally->{'id'};
				my $allyName = $ally->{'name'};
				$allyName =~ s/【勝者！】//g;
				$AllyInfo .= "<A style=\"text-decoration:none\" href=\"$HthisFile?AmiOfAlly=${allyId}\"><FONT COLOR=\"$ally->{'color'}\"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}</A>&nbsp;&nbsp;";
			}
			out("<TD align='left'>$AllyInfo</TD>\n");
		}
		out("\n</TR>\n");
	}
	out(<<END);
</TABLE>
</DIV>
END
}

#----------------------------------------------------------------------
# アイテム獲得状況
#----------------------------------------------------------------------
sub ItemInfo() {
	# 開放
	unlock();

	out(<<"END");
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='islandInfo'>
<H1>${HitemName[0]}獲得状況</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell colspan='2'>${HtagTH_}${HitemName[0]}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}保有$AfterName名${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}能力${H_tagTH}　★はキーアイテム</TH>
</TR>
END

	my($island, $name, $navyComLevel, $totalExp);
	my @sptext  = ('<span class=check>[★]</span>', '<span class=check>[全島補給可]</span>', '<span class=check>[地形遮蔽無効]</span>', '<span class=check>[保有艦艇', '<span class=check>[射程UP ', '<span class=check>[命中率UP ', '<span class=check>[コマンド回数 x',
					'<span class=check>[食料Max x', '<span class=check>[資金Max x', '<span class=check>[収穫 x', '<span class=check>[収入 x', '<span class=check>[攻撃回数 x', '<span class=check>[破壊力 x', '<span class=check>[維持食料 x', '<span class=check>[維持資金 x', '<span class=check>[食料消費 x', '<span class=check>[コマンドコスト x',
					'<span class=check>[地震 x', '<span class=check>[台風 x', '<span class=check>[隕石 x', '<span class=check>[巨大隕石 x', '<span class=check>[噴火 x', '<span class=check>[火災 x', '<span class=check>[津波 x',
					'<span class=check>[破壊力 '
					);
	my @sptextafter  = ('',  '',  '',  ']</span>',  'Hex]</span>',  '%]</span>',  ']</span>',
						']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',
						']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',  ']</span>',
						']</span>'
					);
	my @pm = (' ', ' +');
	foreach (1..$#HitemName){
		my($i, $special);
		foreach $i (0..2) {
			$special .= $sptext[$i] if($HitemSpecial[$_][$i] != 0);
		}
		$special .= $sptext[3] . $pm[($HitemSpecial[$_][3] > 0)] . $HitemSpecial[$_][3] . $sptextafter[3] if($HitemSpecial[$_][3] != 0);
		foreach $i (4..5) {
			$special .= $sptext[$i] . $HitemSpecial[$_][$i] . $sptextafter[$i] if($HitemSpecial[$_][$i] != 0);
		}
		foreach $i (6..23) {
			$special .= $sptext[$i] . $HitemSpecial[$_][$i] . $sptextafter[$i] if($HitemSpecial[$_][$i] != 1);
		}
		$special .= $sptext[24] . (($HitemSpecial[$_][24] > 0) ? '+' : '') . $HitemSpecial[$_][24] . $sptextafter[24] if($HitemSpecial[$_][24] != 0);
		my @getId = keys %{$HitemGetId[$_]};
		my $ng = @getId;
		my($rspan);
		$rspan = " rowspan='$ng'" if($ng > 1);
		out(<<"END");
<TR $HbgInfoCell>
<TD align='right'${rspan}><img src='$HitemImage[$_]'></TD>
<TH${rspan}>$HitemName[$_]</TH>
END
		if(!$ng) {
			out(<<"END");
<TD $HbgNameCell align=left><DIV align='center'>−</DIV></TD>
<TD $HbgInfoCell align=right>−</TD>
<TD $HbgInfoCell align=left>$special</TD>
</TR>
END
		} else {
			my $c = 0;
			my $gId;
			foreach $gId (@getId) {
				my $n = $HidToNumber{$gId};
				if(defined $n) {
					$island = $Hislands[$n];
					$name = islandName($island);
					if($island->{'field'}) {
						$name = "${HtagNumber_}${name}${H_tagNumber}";
					} elsif($island->{'absent'}  == 0) {
						$name = "${HtagName_}${name}${H_tagName}";
					} else {
						$name = "${HtagName2_}${name}($island->{'absent'})${H_tagName2}";
					}
					$name .= "${HtagDisaster_}★${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
					if($island->{'predelete'}) {
						my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
						$name = "${HtagDisaster_}【管理人あずかり】$rest${H_tagDisaster}<BR>" . $name;
					}
					$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\">${name}</A>";
					$navyComLevel = gainToLevel($island->{'gain'});
					$totalExp = $island->{'gain'};
					$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
				} else {
					$name = "<DIV align='center'>−</DIV>";
					$totalExp = '−';
				}
				out("<TR $HbgInfoCell>") if($c);
				out(<<"END");
<TD $HbgNameCell align=left>$name</TD>
<TD $HbgInfoCell align=right>$totalExp</TD>
END
				out("<TD class='N' align=left${rspan}>$special</TD>") if(!$c);
				out("</TR>");
				$c++;
			}
		}
	}
	out(<<"END");
</TABLE>
</DIV>
END
}

#----------------------------------------------------------------------
# 艦艇保有数一覧
#----------------------------------------------------------------------
sub fleetInfo {
	# 開放
	unlock();
	my($col, $row);
	if(!$HinfoMode) {
		$col = 2; $row = (!$HnavySafetyZone || $HnavySafetyInvalidp) ? 3 : 2;
	} else {
		$col = 1; $row = 1;
	}
	my $title = ('全データ', '保有数', '撃沈数', '自爆数')[$HinfoMode];
	my $rowstr = ($HinfoMode < 2) ? ' rowspan=2' : '';
	out(<<"END");
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='islandInfo'>
<H1>艦艇保有数一覧</H1>
END
	out(qq|[<A href="$HthisFile?Fleet=0">全データ</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=1">保有数</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=2">撃沈数</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=3">自爆数</A>] |) if(!$HnavySafetyZone || $HnavySafetyInvalidp);
	out(<<"END");
<TABLE BORDER>
<TR>
<TH colspan=$col>$title</TH>
END
	foreach (0..$#HnavyName) {
		out("<TD class='T'>${HtagTH_}$HnavyName[$_]${H_tagTH}<BR><img src=\"$HnavyImage[$_]\"></TD>");
	}
	out("<TD class='T'$rowstr>${HtagTH_}合計${H_tagTH}</TD>");
	out("<TD class='T'$rowstr>${HtagTH_}保有艦艇<BR>維持費${H_tagTH}</TD>");
	out("<TD class='T'$rowstr>${HtagTH_}保有艦艇<BR>維持食料${H_tagTH}</TD>");
	out("</TR>");
	if($HinfoMode < 2) {
		out("<TR><TH colspan=$col>保有可能数</TH>");
		foreach (0..$#HnavyName) {
			if($HnavyKindMax[$_]) {
				out("<TH>$HnavyKindMax[$_]</TH>");
			} else {
				out("<TH>無制限</TH>");
			}
		}
		out("</TR>");
	}
	my($island, $id, $name, $fkind, $kind, @ids, $islands, $kindNavy, $money, $food);
	foreach ($HbfieldNumber..$islandNumber) {
		$island = $Hislands[$_];
		$island->{'totalnavy'} = 0;
		$island->{'upkeepMoney'} = 0;
		$island->{'upkeepFood'} = 0;
		$island->{'totalsink'} = 0;
		$island->{'totalsinkself'} = 0;
		foreach (0..$#HnavyName) {
			$kind = "navykind$_";
			$island->{$kind} = 0; # 保有数の初期化
			$kind = "sinkkind$_";
			$island->{$kind} = 0; # 撃沈数の初期化
			$island->{$kind} += $island->{'sink'}[$_] + $island->{'sinkself'}[$_]; # 撃沈数
			$island->{'totalsink'} += $island->{$kind};
			$kind = "sinkself$_";
			$island->{$kind} = 0; # 自爆数の初期化
			$island->{$kind} += $island->{'sinkself'}[$_]; # 自爆数
			$island->{'totalsinkself'} += $island->{$kind};
		}
		$fkind = $island->{'fkind'};
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack(hex($_));
			$kind = "navykind${nKind}";
			$island->{$kind}++; # 保有数
			$island->{'upkeepMoney'} += $HnavyMoney[$nKind]; # 維持費
			$island->{'upkeepFood'} += $HnavyFood[$nKind]; # 維持食料
			next if ($HnavySpecial[$nKind] & 0x8); # 軍港は合計に入れない
			$island->{'totalnavy'}++;
		}
	}
	$islands = islandSort('totalnavy');
	$ids{'totalnavy'} = $islands->{'id'};
	$islands = islandSort('upkeepMoney');
	$ids{'upkeepMoney'} = $islands->{'id'};
	$islands = islandSort('upkeepFood');
	$ids{'upkeepFood'} = $islands->{'id'};
	$islands = islandSort('totalsink');
	$ids{'totalsink'} = $islands->{'id'};
	$islands = islandSort('totalsinkself');
	$ids{'totalsinkself'} = $islands->{'id'};
	foreach (0..$#HnavyName) {
		$kind = "navykind$_";
		$islands = islandSort($kind);
		$ids{$kind} = $islands->{'id'};
		$kind = "sinkkind$_";
		$islands = islandSort($kind);
		$ids{$kind} = $islands->{'id'};
		$kind = "sinkself$_";
		$islands = islandSort($kind);
		$ids{$kind} = $islands->{'id'};
	}
	foreach ($HbfieldNumber..$islandNumber) {
		$island = $Hislands[$_];
		$name = islandName($island);
		$id = $island->{'id'};

		out("<TR>\n<TH $HbgTitleCell rowspan=$row>$name</TH>\n");

		my $upkeepInfo = '';
		if($island->{'upkeepMoney'} < 0) {
			$money = "<span class='Money'>収入" . - $island->{'upkeepMoney'} . "${HunitMoney}";
		} elsif($island->{'upkeepMoney'} == 0) {
			$money = '−';
		} else {
			$money = $island->{'upkeepMoney'} . "${HunitMoney}";
		}
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		if($id == $ids{'upkeepMoney'}) {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>${HtagTH_}$money${H_tagTH}</TD>";
		} else {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>$money</TD>";
		}
		if($island->{'upkeepFood'} < 0) {
			$food = "<span class='Food'>収穫" . - $island->{'upkeepFood'} . "${HunitFood}";
		} elsif($island->{'upkeepFood'} == 0) {
			$food = '−';
		} else {
			$food = $island->{'upkeepFood'} . "${HunitFood}";
		}
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		if($id == $ids{'upkeepFood'}) {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>${HtagTH_}$food${H_tagTH}</TD>";
		} else {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>$food</TD>";
		}

		out("<TH $HbgTitleCell>${HtagTH_}保有数${H_tagTH}</TH>\n") if(!$HinfoMode);
		if(!$HinfoMode || $HinfoMode == 1) {
			foreach (0..$#HnavyName) {
				$kind = "navykind$_";
				$kindNavy = $island->{$kind}; # 保有数
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalnavy'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalnavy'}艦${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalnavy'}艦</TD>");
			}
			out("$upkeepInfo");
			out("\n</TR><TR>\n") if(!$HinfoMode);
		}

		out("<TH $HbgTitleCell>${HtagTH_}撃沈数${H_tagTH}</TH>\n") if(!$HinfoMode);;
		if(!$HinfoMode || $HinfoMode == 2) {
			foreach (0..$#HnavyName) {
				$kind = "sinkkind$_";
				$kindNavy = $island->{$kind}; # 撃沈数
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalsink'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalsink'}艦${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalsink'}艦</TD>");
			}
			out("$upkeepInfo") if($HinfoMode == 2);
			out("\n</TR><TR>\n") if(!$HinfoMode);
		}

		if((!$HnavySafetyZone || $HnavySafetyInvalidp) && (!$HinfoMode || $HinfoMode == 3)) {
			out("<TH $HbgTitleCell>${HtagTH_}自爆数${H_tagTH}</TH>\n") if(!$HinfoMode);
			foreach (0..$#HnavyName) {
				$kind = "sinkself$_";
				$kindNavy = $island->{$kind}; # 自爆数
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalsinkself'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalsinkself'}艦${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalsinkself'}艦</TD>");
			}
			out("$upkeepInfo") if($HinfoMode == 3);
		}
	}
	out(<<END);
</TR></TABLE></DIV>
END

}

#------------------------------------------------
# トーナメントモード
#------------------------------------------------
# 対戦更新時間
sub TimeTableMain {
	my $tournament = "";
	my $sec = ($HyosenTime % 60);
	$sec = ($sec ? "$sec秒" : '');
	my $min = ($HyosenTime % 3600);
	$min = ($min ? "$min分" : '');
	my $hour = int($HyosenTime / 3600);
	$hour = ($hour ? "$hour時間" : '');
	my $yosenTime = "$hour$min$sec";
	$sec = ($HdevelopeTime % 60);
	$sec = ($sec ? "$sec秒" : '');
	$min = ($HdevelopeTime % 3600);
	$min = ($min ? "$min分" : '');
	$hour = int($HdevelopeTime / 3600);
	$hour = ($hour ? "$hour時間" : '');
	my $developeTime = "$hour$min$sec";
	$sec = ($HinterTime % 60);
	$sec = ($sec ? "$sec秒" : '');
	$min = ($HinterTime % 3600);
	$min = ($min ? "$min分" : '');
	$hour = int($HinterTime / 3600);
	$hour = ($hour ? "$hour時間" : '');
	my $interTime = "$hour$min$sec";
	$sec = ($HfightTime % 60);
	$sec = ($sec ? "$sec秒" : '');
	$min = ($HfightTime % 3600);
	$min = ($min ? "$min分" : '');
	$hour = int($HfightTime / 3600);
	$hour = ($hour ? "$hour時間" : '');
	my $fightTime = "$hour$min$sec";


	# トーナメント　ターン更新時間早見表
	out(<<"END");
<STYLE type="text/css">
<!--
#list { display:none; }
-->
</STYLE>
<SCRIPT LANGUAGE="JavaScript">
<!--
function textcopy(mapdata){
	window.clipboardData.setData("text",mapdata);
}
function searchID(url){
	if(document.getElementById){
		return document.getElementById(url);
	} else if(document.all){
		return document.all(url);
	} else if(document.layers){
		return document.layers[url];
	}
}
//-->
</SCRIPT>
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='FightLog'>
<H1>対戦タイムテーブル</H1>
END
	my $round = $HislandFightCount;
	my $flag  = 0;
	my $pNumber = @HpreDeleteID;
	my $iNumber = $HislandNumber - $pNumber - $HbfieldNumber;
	if($round && $iNumber > $Htournament) {
		$iNumber = $Htournament;
	}
	my $fturn = 0;
	my $nofight = 0;
	if($HislandFightMode == 1) {
		$fturn = $HislandChangeTurn - $HyosenTurn - $HdevelopeTurn;
	} elsif($HislandFightMode == 2) {
		$HfightTurn = $HfinalTurn if($iNumber <= 2);
		$fturn = $HislandChangeTurn - $HyosenTurn - $HdevelopeTurn - $HfightTurn;
		foreach ($HbfieldNumber..$islandNumber) {
			$nofight++ if($Hislands[$_]->{'fight_id'} < 0);
		}
	}
	$tournament .= "ターン\t$AfterName数\t進行状態\t更新時間\n";
	my $end = 0;
	if($iNumber > 1) {
		out("<TABLE BORDER=0><TR $HbgTitleCell><TH colspan=2>${HtagTH_}種別${H_tagTH}</TH><TH>${HtagTH_}残島${H_tagTH}</TH><TH colspan=2>${HtagTH_}ターン${H_tagTH}</TH><TH>${HtagTH_}期間${H_tagTH}</TH><TH>${HtagTH_}不戦勝の<BR>開発停止<BR>ターン数${H_tagTH}</TH></TR>");
	} else {
		$end =1;
	}
	while($iNumber > 1){
		if($HislandTurn < $HyosenTurn) {
			# 予選
			$HislandFightMode = 0;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime1[($HislandTurn % ($#HtmTime1 + 1))] : $HyosenTime;
			$timeString = timeToString($HislandLastTime);
			foreach(1..$HyosenRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\t予選\t$timeString\n";
				if(!$flag) {
					$flag = 1;
					out("<TR class='InfoCellT'><TH colspan=2><span class='lbbsOW'>予選</span></TH><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$yosenTime</B>毎に1回<B>$HyosenRepCountターン更新</B>で<B>全$HyosenTurnターン</B></TD><TD align='right'>〜$HyosenTurn</TD>");
					out("<TD>${timeString}〜");
				}
				last if($HislandTurn == $HyosenTurn);
			}
			if($HislandTurn == $HyosenTurn) {
				out("${HtagTH_}${timeString}${H_tagTH}</TD><TD align='center'>−</TD></TR>");
				$flag = 0;
			}
		} elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $fturn) {
			# 開発
			$iNumber = $Htournament if(($HislandFightMode == 0) && ($iNumber > $Htournament));
			$HislandFightMode = 1;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime2[($HislandTurn % ($#HtmTime2 + 1))] : $HdevelopeTime;
			$timeString = timeToString($HislandLastTime);
			$HfightTurn = $HfinalTurn if($iNumber <= 2);
			foreach(1..$HdeveRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\t開発\t$timeString\n";
				if(!$flag) {
					$round++;
					$flag = 1;
					my $endturn = $HyosenTurn + $HdevelopeTurn + $fturn;
					if($iNumber + $nofight <= 2) {
						out("<TR $HbgInfoCell><TH>決　勝</TH>");
					} elsif($iNumber + $nofight <= 4) {
						out("<TR $HbgInfoCell><TH>準決勝</TH>");
					} else {
						out("<TR $HbgInfoCell><TH>第${round}回戦</TH>");
					}
					out("<TD><span class='lbbsSS'>開発期間</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$developeTime</B>毎に1回<B>$HdeveRepCountターン更新</B>で<B>全$HdevelopeTurnターン</B></TD><TD align='right'>$HislandTurn〜$endturn</TD>");
					out("<TD>${timeString}〜");
				}
				last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn);
			}
			if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn) {
				out("<B>${timeString}</B></TD><TD align='center'>−</TD></TR>");
				$flag = 0;
			}
		}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
			# 戦闘
			$HislandFightMode = 2;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime3[($HislandTurn % ($#HtmTime3 + 1))] : $HfightTime;
			$timeString = timeToString($HislandLastTime);
			#$tournament .= "$HislandTurn\t$iNumber\t戦闘♪\t$timeString\t$HfightRepCount\n";
			foreach(1..$HfightRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\t戦闘♪\t$timeString\n";
				if(!$flag) {
					$flag = 1;
					my $endturn = $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn;
					if($iNumber + $nofight <= 2) {
						out("<TR class='InfoCellT'><TH>決　勝</TH>");
					} elsif($iNumber + $nofight <= 4) {
						out("<TR class='InfoCellT'><TH>準決勝</TH>");
					} else {
						out("<TR class='InfoCellT'><TH>第${round}回戦</TH>");
					}
					out("<TD><span class='lbbsOW'>戦闘期間</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$fightTime</B>毎に1回<B>$HfightRepCountターン更新</B>で<B>全$HfightTurnターン</B></TD><TD align='right'>$HislandTurn〜$endturn</TD>");
					out("<TD>${timeString}〜");
				}
				last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn);
			}
			if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn) {
				my $nofight = $round * $HnofightUp + $HnofightTurn . "ターン";
				$nofight = '−' if($iNumber <= 2);
				out("${HtagTH_}${timeString}${H_tagTH}</TD><TD align='center'>$nofight</TD></TR>");
				$flag = 0;
			}
		} else {
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime2[($HislandTurn % ($#HtmTime2 + 1))] : ($HislandTurn == $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn) ? $HinterTime : $HdevelopeTime;
			if($HislandFightMode == 2) {
				$iNumber = int(($iNumber + $nofight) / 2 + 0.5);
				$iNumber++ if(($iNumber > 2) && (($iNumber % 2) != 0) && ($HconsolationMatch));
				$nofight = 0;
			}
			$HislandFightMode = 1;
			$timeString = timeToString($HislandLastTime);
			$fturn += $HdevelopeTurn + $HfightTurn;
			last if(!$fturn); # 無限ループ回避
			$HfightTurn = $HfinalTurn if($iNumber <= 2);
			if($iNumber > 1) {
				foreach(1..$HdeveRepCount){
					$HislandTurn++;
					$tournament .= "$HislandTurn\t$iNumber\t開発\t$timeString\n";
					if(!$flag) {
						$round++;
						$flag = 1;
						my $endturn = $HyosenTurn + $HdevelopeTurn + $fturn;
						if($iNumber + $nofight <= 2) {
							out("<TR $HbgInfoCell><TH>決　勝</TH>");
						} elsif($iNumber + $nofight <= 4) {
							out("<TR $HbgInfoCell><TH>準決勝</TH>");
						} else {
							out("<TR $HbgInfoCell><TH>第${round}回戦</TH>");
						}
						out("<TD><span class='lbbsSS'>開発期間</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$developeTime</B>毎に1回<B>$HdeveRepCountターン更新</B>で<B>全$HdevelopeTurnターン</B></TD><TD align='right'>$HislandTurn〜$endturn</TD>");
						out("<TD>${timeString}〜");
					}
					last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn);
				}
				if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn) {
					out("<B>${timeString}</B></TD><TD align='center'>−</TD></TR>");
					$flag = 0;
				}
			}
		}
	}
	unlock();

	if(!$end) {
		out("</TABLE><BR>");
		my $con = ('', '※戦闘終了後奇数(不戦勝が発生する見込み)になる場合に敗退する島で最上位の島を<B>敗者復活</B>します。<BR>')[$HconsolationMatch];
		my $halffight = int($HfightTurn/2);
		my $halffinal = int($HfinalTurn/2);

		out(<<END);
<blockquote>
※資金繰り回数が<B>$HstopAddPop回</B>になると人口増加がストップします。<BR>
　 また予選では、失業者数が<B>$Hno_work$HunitPop</B>を超えても、人口増加がストップします<BR>
※対戦相手がいない場合、または開発期間中に「相手がいなくなった場合」は<B>不戦勝扱い</B>となります。<BR>
　 不戦勝の場合、<B>（回戦数×${HnofightUp}+${HnofightTurn}）ターン</B>の開発停止になります。 <BR>
※戦闘期間の半分（$halffightターン・決勝は$halffinalターン）が経過するまでに、「相手がいなくなった場合」及び<BR>
　 「相手の<B>戦闘行為回数が$do_fight回に満たなかった</B>（または、<B>相手が１度も艦隊派遣を行わなかった</B>）場合」は<B>不戦勝扱い</B>となります。<BR>
　 この場合は、戦闘開始時の島の状態に戻され、開発停止になります。停止期間は、<B>（回戦数×${HnofightUp}+${HnofightTurn}）− 経過ターン数</B>です。 <BR>
$con
</blockquote></DIV>
END
	} else {
		out("ゲームは終了しました。");
	}
#	out(<<END);
#<DIV id='hyo'><INPUT TYPE="button" VALUE="トーナメント更新時間早見表をクリップボードにコピー" onClick="textcopy(searchID('ALIST').value);"></DIV>
#<DIV id='list'><textarea NAME="ALIST" cols="100" rows="0">$tournament</textarea></DIV>
#END
}

# 対戦の記録
sub FightViewMain {

	my %rankKind = (
		'pop' => '人口',
		'gain' => '総獲得経験値',
		'money' => '資金',
		'food' => '食料',
		'area' => '面積',
		'farm' => '農場規模',
		'factory' => '工場規模',
		'mountain' => '採掘場規模',
		'monsterkill' => '怪獣退治数',
		'itemNumber' => "$HitemName[0]獲得数",
		'point' => "$HpointName",
	);
	my %rankAfter = (
		'pop' => "$HunitPop",
		'gain' => '',
		'money' => "$HunitMoney",
		'food' => "$HunitFood",
		'area' => "$HunitArea",
		'farm' => "0$HunitPop",
		'factory' => "0$HunitPop",
		'mountain' => "0$HunitPop",
		'monsterkill' => "$HunitMonster",
		'itemNumber' => '',
		'point' => "$HpointAfter",
	);

	TimeTableMain() if($HplayNow && $Htournament);
	if(!open(IN, "${HfightdirName}/${Hfightlog}")){
		unlock();
#		out ("${HtagBig_}データがありません！${H_tagBig}$HtempBack\n");
		return;
	}
	my @lines = <IN>;
	close(IN);
	unlock();

#	out ("${HtagTitle_}対戦の記録${H_tagTitle}<BR><DIV ALIGN=right>*敗者の島名をクリックすると敗戦時の状況が見れます</DIV>\n");
#	out ("<DIV align='center'>$HtempBack</DIV><BR>\n");
	out("<HR>") if($HplayNow && $Htournament);
	out(<<END);
<DIV ID='FightLog'>
<H1>対戦の記録</H1>
*敗者の${AfterName}名をクリックすると敗戦時の状況を見ることができます。
END

	my $lineflag = 0;
	chomp(@lines);
	foreach $line (@lines) {
		if($line =~ /<[0-9]*>/) {
			$line =~ s/<|>//g;
			$lineflag = $line;
			my $msg = (!$line) ? "予選落ち" : ($line == 99) ? "決勝戦" : $line."回戦";
			out("</TABLE>\n") if($line < 99);
			out("<HR><DIV ID='fightlogS'><H1>${HtagHeader_}$msg${H_tagHeader}</H1></DIV>");
			# テーブルヘッダ
			if($lineflag == 0) {
				out(<<END);
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}${AfterName}${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</NOBR></TH></TR>
END

			} else {

				my $mStr1;
				if($HuseBase || $HuseSbase) {
					$mStr1 =  "<TH $HbgTitleCell>${HtagTH_}ミ撃${H_tagTH}</TH>";
				}
				my $col = ($HuseBase || $HuseSbase) ? 10 : 9;
				out(<<END);
<TABLE BORDER>
<TR><TH colspan=3></TH><TH $HbgTitleCell colspan=$col>${HtagTH_}勝者${H_tagTH}</TH><TH colspan=1></TH>
<TH $HbgTitleCell colspan=$col>${HtagTH_}敗者${H_tagTH}</TH></TR>
<TR>
<TH $HbgTitleCell>${HtagTH_}勝者${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}敗者${H_tagTH}</TH>
<TH $HbgTitleCell width=15>　</TH>
<TH $HbgTitleCell>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}防撃${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}民救${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾飛${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾発${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾防${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦派${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦来${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦破${H_tagTH}</TH>
<TH $HbgTitleCell width=15>　</TH>
<TH $HbgTitleCell>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}防撃${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}民救${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾飛${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾発${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾防${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦派${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦来${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦破${H_tagTH}</TH>
</tr>
END

			}

		} elsif($lineflag == 0) {
			# 予選結果
			my($count, $id, $name, $score, $data, $tId, $tName, $tScore, $tData, $reward) = split(/\,/,$line);
			if(-e "${HfightdirName}/${id}_lose.${HsubData}") {
				$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?LoseMap=${id}\">${HtagName2_}$name${H_tagName2}</A>";
			} else {
				$name = "${HtagName2_}$name${H_tagName2}";
			}
			out(<<END);
<TR><TD $HbgInfoCell align=right>${HtagName_}${name}${H_tagName}</TD>
<TD $HbgInfoCell align=center><B>${score}$rankAfter{$HrankKind}</B></TD></TR>
END

		} else {
			# トーナメント結果
			my($count, $id, $name, $score, $data, $tId, $tName, $tScore, $tData, $reward) = split(/\,/,$line);
			my(@subExt) = split(/-/,$data);
			my(@tSubExt) = split(/-/,$tData);
#			$tName = "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
#						$HtagName2_.$tName.$H_tagName2."</A>";
			$tPop .= ${HunitPop};
			$score .= $rankAfter{$HrankKind};
			if($tId == -1) {
				$tName = "${HtagName2_}- 不戦勝 -${H_tagName2}";
				$tScore = "−";
			} elsif($tId == -2) {
				$tName = "${HtagName2_}- 圧勝！ -${H_tagName2}";
				$tScore = "−";
			} else {
				if(-e "${HfightdirName}/${tId}_lose.${HsubData}") {
					$tName = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?LoseMap=${tId}\">${HtagName2_}$tName${H_tagName2}</A>";
				} else {
					$tName = "${HtagName2_}$tName${H_tagName2}";
				}
				$tScore .= $rankAfter{$HrankKind};
			}
			if($tId != -9) {
				my(@after) = ('', '', '基', '基', "$HunitPop", '発', '発', '発', '艦', '艦', '艦');
				foreach (2..$#subExt){
					$subExt[$_] = $subExt[$_] ? "${subExt[$_]}${after[$_]}" : 'なし';
					$tSubExt[$_] = ($tScore == '−') ? '−' : ($tSubExt[$_] ? "${tSubExt[$_]}${after[$_]}" : 'なし');
				}
				my($mStr1, $mStr2) = ('', '');
				if($HuseBase || $HuseSbase) {
					$mStr1 =  "<TD $HbgInfoCell align=center>$subExt[3]</TD>";
					$mStr2 =  "<TD $HbgInfoCell align=center>$tSubExt[3]</TD>";
				}
				out(<<END);
<TR><TD $HbgInfoCell align=right>${HtagName_}${name}${H_tagName}</TD>
<TD $HbgInfoCell align=center>${tName}</TD>
<TD $HbgInfoCell>　</TD>
<TH $HbgInfoCell>${score}</TH>
<TD $HbgInfoCell align=center>$subExt[2]</TD>
$mStr1
<TD $HbgInfoCell align=center>$subExt[4]</TD>
<TD $HbgInfoCell align=center>$subExt[5]</TD>
<TD $HbgInfoCell align=center>$subExt[6]</TD>
<TD $HbgInfoCell align=center>$subExt[7]</TD>
<TD $HbgInfoCell align=center>$subExt[8]</TD>
<TD $HbgInfoCell align=center>$subExt[9]</TD>
<TD $HbgInfoCell align=center>$subExt[10]</TD>
<TD $HbgInfoCell>　</TD>
<TH $HbgInfoCell>${tScore}</TH>
<TD $HbgInfoCell align=center>$tSubExt[2]</TD>
$mStr2
<TD $HbgInfoCell align=center>$tSubExt[4]</TD>
<TD $HbgInfoCell align=center>$tSubExt[5]</TD>
<TD $HbgInfoCell align=center>$tSubExt[6]</TD>
<TD $HbgInfoCell align=center>$tSubExt[7]</TD>
<TD $HbgInfoCell align=center>$tSubExt[8]</TD>
<TD $HbgInfoCell align=center>$tSubExt[9]</TD>
<TD $HbgInfoCell align=center>$tSubExt[10]</TD>
</TR>
END
			} else {
				out("<TR><TD class='M' colspan=6 align=right>${HtagName_}${name}${H_tagName}、<B>敗者復活！</B></TD></TR>\n");
			}
		}

	}
	out("</TABLE>\n") if(@lines != ());
	out("</DIV>\n");

}

#----------------------------------------------------------------------
# 初期設定確認
#----------------------------------------------------------------------
sub setupValue{
	my $mode = 1;
	my $admin;

	if(checkSpecialPassword($HdefaultPassword)) {
		$admin = 1 ;
		$mode = 0;
	}
	if($mode) {
		if(-e "${HefileDir}/setup.html") {
			out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=${efileDir}/setup.html\">");
		}
	}

	my($src);

	unlock();

	my $unitTime = ($HarmisticeTurn || $HsurvivalTurn) ? $HarmTime : $HunitTime;
	my $sec = ($unitTime % 60);
	$sec = ($sec ? "$sec秒" : '');
	my $min = ($unitTime % 3600);
	$min = ($min ? "$min分" : '');
	my $hour = int($unitTime / 3600);
	$hour = ($hour ? "$hour時間" : '');

	my $repeatTurn = ($HarmisticeTurn || $HsurvivalTurn) ? $HarmRepeatTurn : $HrepeatTurn;

	my @switchStr = ('OFF', 'ON');
	my $jsLocalImg1 = '';
	my $jsLocalImg2 = '';

	$jsLocalImg1 =<<"END";
<script language="JavaScript">
<!--
ckary = new Array();
gifhref = '';
skinhref = '';

function getck(){
	ckary = document.cookie;
	ckstr = "";

	i = 0;
	while (ckary[i]){
		num = ckary[i].indexOf("KAISEN_JS=");
		if (num != -1){
			cookp = ckary[i].split("=");
			cook   = cookp[1].split("<>");
			gifhref = cook[8];
			skinhref = cook[9];
			break;
		}
		i++;
	}
}
getck();
if (skinhref == '') {
	skinhref = '${HcssDir}/${HcssDefault}';
}
//if (gifhref == '') {
//	gifhref = '$HimageDir';
//}
//document.write('<BASE HREF="' + gifhref + '/">\\n');
document.write('<link rel="stylesheet" type="text/css" href="' + skinhref + '">\\n');
// -->
</script>
END

	$src = <<"END" if($mode);
<HTML>
<HEAD>
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
$HtitleTag
</TITLE>
$jsLocalImg1
</HEAD>
$Body
<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
$Hheader
</DIV>
<HR>
END

	$src .= <<"END";
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='setupValue'>
<a name='top'><H1>設定一覧</H1></a>
END

$src .= "<a href='#admin' style='text-decoration=none'>管理設定</a> / ";
$src .= "<a href='#basic' style='text-decoration=none'>基本設定</a> / ";
$src .= "<a href='#ocean' style='text-decoration=none'>海域モード</a> / ";
$src .= "<a href='#autokeep' style='text-decoration=none'>無人(死滅)回避</a> / ";
$src .= "<a href='#survival' style='text-decoration=none'>サバイバル</a> / ";
$src .= "<a href='#imperial' style='text-decoration=none'>陣営戦(帝國海戦)</a> / ";
$src .= "<a href='#tournament' style='text-decoration=none'>トーナメント</a> / ";
$src .= "<a href='#amity' style='text-decoration=none'>友好国設定</a> / ";
$src .= "<a href='#ally' style='text-decoration=none'>同盟システム</a> / ";
$src .= "<a href='#dewar' style='text-decoration=none'>宣戦布告システム</a> / ";
$src .= "<a href='#event' style='text-decoration=none'>イベントシステム</a>";
$src .= "<BR>";
$src .= "<a href='#usecom' style='text-decoration=none'>地形・コマンド設定</a> / ";
$src .= "<a href='#town' style='text-decoration=none'>都市系設定</a> / ";
$src .= "<a href='#complex' style='text-decoration=none'>複合地形</a> / ";
$src .= "<a href='#core' style='text-decoration=none'>コア</a> / ";
$src .= "<a href='#navy' style='text-decoration=none'>海軍</a> / ";
$src .= "<a href='#def' style='text-decoration=none'>防衛施設</a> / ";
$src .= "<a href='#base' style='text-decoration=none'>基地・ミサイル</a> / ";
$src .= "<a href='#weather' style='text-decoration=none'>天候</a> / ";
$src .= "<a href='#disaster' style='text-decoration=none'>災害</a> / ";
$src .= "<a href='#monster' style='text-decoration=none'>怪獣</a> / ";
$src .= "<a href='#hmonster' style='text-decoration=none'>巨大怪獣</a> / ";
$src .= "<a href='#item' style='text-decoration=none'>アイテム</a> / ";
$src .= "<a href='#monument' style='text-decoration=none'>記念碑</a> / ";
$src .= "<a href='#prize' style='text-decoration=none'>ターン杯・各賞</a> / ";
$src .= "<a href='#command' style='text-decoration=none'>コマンド一覧</a>";

	my @adminStr = ('管理人以外も探せる', '管理人だけ探せる(メールor掲示板等で登録を依頼してください)');
	my @doStr  = ('しない', 'する');
	my %rankKind = (
		'pop' => '人口',
		'gain' => '総獲得経験値',
		'money' => '資金',
		'food' => '食料',
		'area' => '面積',
		'farm' => '農場',
		'factory' => '工場',
		'mountain' => '採掘場',
		'monsterkill' => '怪獣退治数',
		'itemNumber' => "$HitemName[0]獲得数",
		'point' => "$HpointName",
	);
	my @useStr = ('使わない', '使う');
	my @useableStr = ('使えない', '使える');
	my @seeStr = ('見えない', '見える', '100の位で四捨五入');
	my @pointStr = ('しない', '座標あり', '座標なし');
	my @axesStr = ('とらない', '開発画面に入る時でエラー発生時', '開発画面に入る時', 'トップページにアクセスした時', '開発画面に入る時 + トップページにアクセスした時');
	my $topAxes = ($HtopAxes > 4) ? 4 : $HtopAxes;
	my @selectStr = (
		"$AfterName数が最も少なく、順位が最下位の陣営",
		"ランダム(\"合計の$AfterName数/陣営の数\"を超えない)",
		"選択可能(\"合計の$AfterName数/陣営の数\"を超えない)"
	);
	my @anStr = ('ない', 'ある');
	my @selfStr = ('受ける', '受けない', '友好国も受けない');
	my $useDeWar = ('', '<BR>　※攻撃制限は一切ありません。「宣戦布告」なしで攻撃可能です。', "<BR>　※「宣戦布告」していない$AfterNameへの攻撃は許可されません。「宣戦布告」直後から攻撃可能です。", "<BR>　※「宣戦布告」していない$AfterNameへの攻撃は許可されません。猶予ターン終了後の戦争中のみ攻撃可能です。")[$HuseDeWar];
	my @hide = ('見える', '隠す');
	my @ox = ('○', '−');
	my @turnStr = ($HtagComName2_, $HtagComName1_);
	my @saftyStr = ('しない', 'する', '友好国も無害にする');
	my @nodefStr = ('しない', "自$AfterNameの攻撃のみ着弾", "友好国に設定してくれている$AfterNameの攻撃も着弾する", "友好国に設定している$AfterNameの攻撃も着弾する", "友好国に設定している$AfterNameの攻撃も，友好国に設定してくれている$AfterNameの攻撃も着弾する");
	my @nearfar = ('最も<B>近い</B>地形から順番に目標を探す', '最も<B>遠い</B>地形から順番に目標を探す', '射程内を<B>ランダム</B>に目標を探す');

# 管理用データ
#------------------

	$src .= <<"END";
<HR>
<a name='admin'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 管理設定</H3></a>
END

	if($admin) {
		$src .= <<"END";
管理者名　<B>$HadminName</B><BR>
管理者のメールアドレス　<B><a href=\"mailto:$Hemail\">$Hemail</a></B><BR>
掲示板アドレス　<B><a href=\"$Hbbs\">$Hbbs</a></B><BR>
ホームページのアドレス　<B><a href=\"$Htoppage\">$Htoppage</a></B><BR>
画像のローカル設定の説明ページ　<B><a href=\"$imageExp\">$imageExp</a></B><BR>
ローカル設定用画像圧縮ファイル　<B><a href=\"$localImg\">$localImg</a></B><BR>
END

		$src .= <<"END";
<BR>
デバッグモード　<B>$switchStr[$Hdebug]</B><BR>
設置フォルダ　<B>$HbaseDir</B><BR>
画像フォルダ　<B>$HimageDir</B><BR>
CSS,JSフォルダ　<B>$efileDir</B><BR>
GMT に対する JST の時差　<B>${Hjst}秒</B><BR>
gzipを使用して圧縮伝送するか　<B>$doStr[$Hgzip]</B><BR>
gzipのインストール先　<B>$HpathGzip</B><BR>
<BR>
リアルタイマーの使用　<B>$useStr[$Hrealtimer]</B><BR>
トップページのレイアウトをtempTop.htmlで指定するか　<B>$doStr[$HlayoutTop]</B><BR>
トップページに表示する${AfterName}の数　<B>$HviewIslandCount</B><BR>
ログファイル保持ターン数　<B>$HlogMaxターン</B><BR>
「最近の出来事」に表示するログのターン数　<B>$HtopLogTurnターン</B><BR>
「最近の出来事」をHTML化するか　<B>$doStr[$HhtmlLogMake]</B><BR>
END

		$src .= <<"END" if($HhtmlLogMake);
「最近の出来事」に表示するログのターン数(HTML)　<B>$HhtmlLogTurnターン</B><BR>
トップページの「最近の出来事」をHTMLにリンクするか　<B>$doStr[$HhtmlLogMode]</B><BR>
END

		$src .= <<"END";
<BR>
開発画面でポップアップナビを表示するか　<B>$doStr[$HpopupNavi]</B><BR>
自$AfterName(開発画面)の「近況」をhistory.cgiで表示するか　<B>$doStr[$HuseHistory1]</B><BR>
他$AfterName(観光画面など)の「近況」をhistory.cgiで表示するか　<B>$doStr[$HuseHistory2]</B><BR>
バックアップを何ターンおきに取るか　<B>$HbackupTurnターン</B><BR>
バックアップを何回分残すか　<B>$HbackupTimes回分</B><BR>
発見ログ保持行数　<B>$HhistoryMax行</B><BR>
ローカル掲示板の使用　<B>$useStr[$HuseLbbs]</B><BR>
外部簡易掲示板を使用するか　<B>$useStr[$HuseExlbbs]</B><BR>
END

		if($HuseExlbbs) {
			$src .= "外部簡易掲示板のアドレス　<B><A href='$HlbbsDir/view.cgi?admin=$HviewPass'>$HlbbsDir</A></B><BR>";
		}

		$src .= <<"END";
<BR>
着弾点をマップ表示可能にするか？　<B>$doStr[$HmlogMap]</B><BR>
他人から資金を見えなくするか？　<B>$seeStr[$HhideMoneyMode]</B><BR>
整地系ログのまとめに座標も出力するか？　<B>$pointStr[$HoutPoint]</B><BR>
各$AfterNameの収支ログ(機密)を出力するか？　<B>$doStr[$HbalanceLog]</B><BR>
JavaScriptの一部を外部ファイル化するか？　<B>$doStr[$HextraJs]</B><BR>
プレイヤーのパスワードを暗号化するか？　<B>$doStr[$cryptOn]</B><BR>
<BR>
パスワード・エラーの画面に警告文を表示するか？　<B>$doStr[$HpassError]</B><BR>
アクセスログをとるか？　<B>$axesStr[$topAxes]</B><BR>
最大記録件数　<B>$HaxesMax件</B><BR>
負荷計測するか？　<B>$doStr[$Hperformance]</B><BR>
<BR>
END
	}

	$src .= <<"END";
新しい${AfterName}は　<B>$adminStr[$HadminJoinOnly]</B><BR>
END
	if($HuseLbbs) {
	}

	$src .= <<"END";
<BR>
COOKIEによるIDチェックをするか？　<B>$doStr[$checkID]</B><BR>
COOKIEによる「画像のローカル設定」もチェックする？　<B>$doStr[$checkImg]</B><BR>
END
	my @freepassName;
	my $i;
	if($freepass[0] eq '') {
		@freepassName = ('なし') ;
	} else {
		foreach $i (@freepass) {
			next unless(defined $HidToNumber{$i});
			push(@freepassName, "$HidToName{$i}${AfterName}");
		}
	}
	$src .= "COOKIEチェック（上の２つの設定）を免除する$AfterNameのID　<B>@freepassName</B><BR>" if($checkId || $checkImg);

	if($HjoinCommentPenaltyStr ne '') {
		$src .= <<"END";
<BR>
コメント欄が発見時のままの場合、管理人あずかりにするか？　<B>$doStr[($HjoinCommentPenalty > 0)]</B><BR>
END
		$src .= "※島発見後、<B>$HjoinCommentPenaltyターン</B>内にコメントがなければ、管理人あずかりになります。解除依頼は$HjoinCommentPenaltyStr<BR>" if($HjoinCommentPenalty);
	}
	$src .= "<BR>「管理人あずかり」でも最初のコマンドが「島の放棄」なら死滅処理をするか？　<B>$doStr[$HforgivenGiveUp]</B><BR>";
	$src .= "<BR>「管理人あずかり」の島への攻撃(艦隊派遣・怪獣派遣・ミサイル攻撃)を許可するか？　<B>$doStr[$HforgivenAttack]</B><BR>";

# 基本設定
#------------------

	my $doNothingMoney = "$HdoNothingMoney$HunitMoney";
	1 while $doNothingMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;

	$src .= <<"END";
<HR>
<a name='basic'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 基本設定</H3></a>
${AfterName}の最大数　<B>$HmaxIsland</B><BR>
${AfterName}の大きさ　<B>${HislandSizeX}x${HislandSizeY}</B><BR>
コマンド入力限界数　<B>$HcommandMax</B><BR>
1ターンが何秒か　<B>${unitTime}秒 ( $hour$min$sec )</B><BR>
１回の更新で何ターン進めるか　<B>$repeatTurnターン</B><BR>
ゲーム終了ターン数　<B>$HgameLimitTurnターン</B><BR>
順位のもとになる要素　<B>$rankKind{$HrankKind}</B><BR>
<BR>
「資金繰り」での収入　<B>$doNothingMoney</B><BR>
<BR>
新規登録された${AfterName}の開発期間　<B>$HdevelopTurnターン</B><BR>
放棄コマンド自動入力ターン数（開発期間）　<B>$HdevelopGiveupTurnターン</B><BR>
放棄コマンド自動入力ターン数　<B>$HgiveupTurnターン</B><BR>
新しい$AfterNameを見つけた直後の放置ターン数　<B>$HjoinGiveupTurnターン</B><BR>
END

	if($HuseLbbs) {
		my $lbbsMoneyPublic = "$HlbbsMoneyPublic$HunitMoney";
		1 while $lbbsMoneyPublic =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $lbbsMoneySecret = "$HlbbsMoneySecret$HunitMoney";
		1 while $lbbsMoneySecret =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= <<"END";
<BR>
ローカル掲示板の表示行数　<B>$HlbbsViewMax</B><BR>
ローカル掲示板の保存行数　<B>$HlbbsMax</B><BR>
ローカル掲示板への匿名発言を許可するか？　<B>$doStr[$HlbbsAnon]</B><BR>
ローカル掲示板に発言者の名前を表示するか？　<B>$doStr[$HlbbsSpeaker]</B><BR>
ローカル掲示板でオートリンクを使用するか？　<B>$doStr[($HlbbsAutolinkSymbol ne '')]</B>(マーク　<B>$HlbbsAutolinkSymbol</B>)<BR>
他$AfterNameのローカル掲示板に発言するための費用　　公開　<B>$lbbsMoneyPublic</B>　極秘　<B>$lbbsMoneySecret</B><BR>
END
	}

# 資金、食料などの設定値
#-------------------------

	my $initialMoney = "$HinitialMoney$HunitMoney";
	1 while $initialMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $maximumMoney = "$HmaximumMoney$HunitMoney";
	1 while $maximumMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $costChangeName = "$HcostChangeName$HunitMoney";
	1 while $costChangeName =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $treeValue = "$HtreeValue$HunitMoney";
	1 while $treeValue =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $initialFood = "$HinitialFood$HunitFood";
	1 while $initialFood =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $maximumFood = "$HmaximumFood$HunitFood";
	1 while $maximumFood =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $oilMoney = "$HoilMoney$HunitMoney";
	1 while $oilMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
	if($HoilMoneyMin) {
		my $oilMoney2 = "$HoilMoneyMin$HunitMoney";
		1 while $oilMoney2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$oilMoney = "ランダム収入　($oilMoney2〜$oilMoney)";
	}
	$oilRatio = $HoilRatio/10;
	$src .= <<"END";
<BR><TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}初期資金 / 最大資金${H_tagTH}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}初期食料 / 最大食料${H_tagTH}</TH><TH colspan=5>${HtagTH_}最小単位${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}お金${H_tagTH}</TH><TH>${HtagTH_}食料${H_tagTH}</TH><TH>${HtagTH_}人口${H_tagTH}</TH><TH>${HtagTH_}広さ${H_tagTH}</TH><TH>${HtagTH_}木の数${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$initialMoney / $maximumMoney</TD><TD align='center'>$initialFood / $maximumFood</TD><TD align='right'>1$HunitMoney</TD><TD align='right'>1$HunitFood</TD><TD align='right'>1$HunitPop</TD><TD align='right'>1$HunitArea</TD><TD align='right'>1$HunitTree</TD></TR>
</TABLE></B><BR>
名前変更のコスト　<B>$costChangeName</B><BR>
木の1$HunitTree当たりの売値　<B>$treeValue</B><BR>
1ターンで増える木の本数(森1Hexあたり)　<B>${HtreeGrow}$HunitTree</B><BR>
人口1$HunitPopあたりの食料消費量　<B>${HeatenFood}x1$HunitFood</B><BR>
怪獣の数の単位　<B>$HunitMonster</B><BR>
<BR>
油田発見確率　<B>(掘削数量 - 発見済み油田数 x 25)%</B><BR>
油田枯渇確率　<B>$oilRatio%</B><BR>
油田収入　<B>$oilMoney</B><BR>
<BR>
難易度調整（食料・資金の収入倍率：通常レートに対する倍率）　<B>${HincomeRate}倍</B><BR>
END

# 海域モード
#------------------

	$src .= <<"END";
<HR>
<a name='ocean'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 海域モード</H3></a>
海域モード　<B>$switchStr[($HoceanMode > 0)]</B>
END
	$src .= "　($AfterNameと$AfterNameがひとつながりの大きなマップになります)<BR>" if($HoceanMode);

	my(@yesno) = ('いいえ', 'はい');
	if($HoceanMode > 0) {
		$src .= <<"END";
<blockquote>
${AfterName}の配置数　<B>${HoceanSizeX}x${HoceanSizeY}</B><BR><BR>
海域マップを表示するか？　<B>$doStr[$HuseOceanMap]</B><BR>
END
		if($HuseOceanMap) {
			$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH colspan='2'>海域マップ地形</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[0]'></TD><TH>未知の海域</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[1]'></TD><TH>自分の$AfterName</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[2]'></TD><TH>ふつうの$AfterName</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[3]'></TD><TH>バトルフィールド</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[4]'></TD><TH>管理人あずかり</TH></TR>
</TABLE>
　地球モードの時，対象の島がマップの中央にくるようにするか？　<B>$doStr[$HadjustMap]</B><BR>
　海域マップの下に詳細マップを表示するか？　<B>$doStr[($HshowWorld > 0)]</B><BR><BR>
END
		}
		$src .= <<"END";
海域が接続している島どうしでは，艦隊移動，派遣，帰還，怪獣派遣コマンドを使えなくするか？<BR>
　艦隊移動，派遣，帰還(自島に対する移動，派遣，帰還を含む)：<B>$useableStr[!$HnotuseNavyMove]</B><BR>
　怪獣派遣(自島に対する派遣は除く)：<B>$useableStr[!$HnotuseMonsterSend]</B><BR><BR>
バトルフィールドは海域を接続しない。　<B>$yesno[$HfieldUnconnect]</B><BR>
END
		$src .= <<"END" if($HfieldUnconnect);
バトルフィールド内の艦艇・怪獣は移動操縦でなければ外の海域へは出られないようにするか？　艦艇：<B>$yesno[$HfieldNavy]</B>　怪獣：<B>$yesno[$HfieldNavy]</B><BR>
END
		$src .= <<"END";
</blockquote>
END
	}
	$src .= <<"END";
<BR>
地球モード　<B>$switchStr[($Hroundmode > 0)]</B>
END
	$src .= "　(マップの上下と左右が繋がります)<BR>" if($Hroundmode);
# 死滅回避・無人化回避
#----------------------

	my $autokeep = '';
	if($HautoKeeper > 1) {
		my $autoKeeperPop = "$HautoKeeper$HunitPop";
		1 while $autoKeeperPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$autokeep =<<"END";
<B>$autoKeeperPopで無人化自動回避機能発動</B><BR>
　※「島の放棄」以外では死滅処理をしない。ただし、人口が０になった場合、荒地か平地がなければ沈没してしまう。<BR>
　※他島に派遣中の艦艇や自島(処理対象の島)に出現中の怪獣・巨大怪獣は海になり消滅。<BR>
　※他島から自島へ派遣されている艦隊は、帰還処理される。（人口が０の場合、初期設定の人口になる）<BR>
　※初期設定の人口で開発期間に入る。
END
	} elsif($HautoKeeper) {
		$autokeep =<<"END";
<B>死滅判定回避機能発動</B><BR>
　※「島の放棄」以外では死滅処理をしない。<BR>
　※他島に派遣中の艦艇や自島(処理対象の島)に出現中の怪獣・巨大怪獣は海になり消滅。<BR>
　※他島から自島へ派遣されている艦隊は、帰還処理される。<BR>
　※管理人あずかりにする。（人口が０の場合、あずかり解除の時に初期設定の人口になる）<BR>
　　　注！
END
		$autokeep .= (!$HautoKeeperSetTurn) ? '管理人あずかりは管理人自身の手によって解除されます。' : "管理人あずかりは<B>$HautoKeeperSetTurnターン後に自動解除</B>されます。";
	} else {
		$autokeep = '<B>使用しない</B>';
	}
	$src .= <<"END";
<HR>
<a name='autokeep'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 無人(死滅)回避</H3></a>
無人化自動回避・死滅判定回避機能の使用　$autokeep<BR><BR>
END

# サバイバルモード
#------------------

	$src .= <<"END";
<HR>
<a name='survival'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> サバイバル</H3></a>
サバイバルモード　<B>$switchStr[($HsurvivalTurn > 0)]</B><BR>
END

	my $sec2 = ($HarmisticeTime % 60);
	$sec2 = ($sec2 ? "$sec2秒" : '');
	my $min2 = ($HarmisticeTime % 3600);
	$min2 = ($min2 ? "$min2分" : '');
	my $hour2 = int($HarmisticeTime / 3600);
	$hour2 = ($hour2 ? "$hour2時間" : '');

	$src .= <<"END" if($HsurvivalTurn > 0);
<blockquote>
停戦期間　<B>$HsurvivalTurnターンまで</B><BR>
停戦期間中のターン更新間隔　<B>${HarmisticeTime}秒 ( $hour2$min2$sec2 )</B><BR>
停戦期間中１回の更新で何ターン進めるか　<B>$HarmisticeRepeatTurnターン</B><BR>
何ターンごとに最下位の${AfterName}が滅ぶか　<B>$HturnDeadターン($HsurvivalTurnターン以降)</B><BR>
</blockquote>
END

# 陣営戦モード
#------------------

	$src .= <<"END";
<HR>
<a name='imperial'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 陣営戦(帝國海戦)</H3></a>
陣営戦モード　<B>$switchStr[($HarmisticeTurn > 0)]</B><BR>
END

	my $cdr = (!$HcampDeleteRule) ? "" : ($HcampDeleteRule == 1) ? "　※占有率<B>(50÷陣営数)%未満</B>で消滅" : "　※占有率<B>${HcampDeleteRule}%未満</B>で消滅";
	my $initialMoney2 = "$HinitialMoney2$HunitMoney";
	1 while $initialMoney2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $initialFood2 = "$HinitialFood2$HunitFood";
	1 while $initialFood2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END" if($HarmisticeTurn);
<blockquote>
停戦期間　<B>$HarmisticeTurnターンまで</B><BR>
停戦期間中のターン更新間隔　<B>${HarmisticeTime}秒 ( $hour2$min2$sec2 )</B><BR>
停戦期間中１回の更新で何ターン進めるか　<B>$HarmisticeRepeatTurnターン</B><BR>
勝利条件　<B>占有率${HfinishOccupation}%</B><BR>
陣営預かりに移行するターン数　<B>$HpreGiveupTurnターン</B><BR>
「陣営共同開発」ができるようにするか？　<B>$doStr[$HuseCoDevelop]</B><BR>
陣営パスワードでパスワード変更ができるようにするか？　<B>$doStr[$HpassChangeOK]</B><BR>
陣営外への援助を許可するか？　<B>$doStr[!$HcampAidOnly]</B><BR>
陣営の選択の方法　<B>$selectStr[$HcampSelectRule]</B><BR>
陣営の消滅があるか？　<B>$anStr[($HcampDeleteRule > 0)]</B>$cdr<BR>
陣営作戦本部コマンド表示数　<B>${HcampCommandTurnNumber}</B>(× $HrepeatTurnターン)<BR>
ゲーム開始後の初期資金と初期食料　初期資金 <B>${initialMoney2}</B> / 初期食料 <B>${initialFood2}</B><BR>
</blockquote>
END

# トーナメントモード
#---------------------

	$src .= <<"END";
<HR>
<a name='tournament'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> トーナメント</H3></a>
トーナメントモード　<B>$switchStr[($Htournament > 0)]</B><BR>
END

	my $tournament = "";
	if($Htournament){
		# トーナメント　ターン更新時間早見表
		$tournament = <<"END";
<STYLE type="text/css">
<!--
#list { display:none; }
-->
</STYLE>
<SCRIPT LANGUAGE="JavaScript">
<!--
function textcopy(mapdata){
	window.clipboardData.setData("text",mapdata);
}
function searchID(url){
	if(document.getElementById){
		return document.getElementById(url);
	} else if(document.all){
		return document.all(url);
	} else if(document.layers){
		return document.layers[url];
	}
}
function display() {
  if(document.getElementById){
    var obj1 = document.getElementById('list');
    var obj2 = document.getElementById('hyo');
    if (obj1.style.display == 'block'){
      obj1.style.display='none';
      obj2.style.display='block';
    } else {
      obj1.style.display='block';
      obj2.style.display='none';
    }
  }
}
//-->
</SCRIPT>
<DIV id='hyo'><INPUT TYPE="button" VALUE="トーナメント更新時間早見表" onClick="display();"></DIV>
<DIV id='list'><INPUT TYPE="button" VALUE="クリップボードにコピー" onClick="textcopy(searchID('ALIST').value);display();"><BR>
<textarea NAME="ALIST" cols="100" rows="5">
END
		my $round = $HislandFightCount;
		my $pno = @HpreDeleteID;
		my $ino = $HislandNumber - $pno - $HbfieldNumber;
		my $itn = $HislandTurn;
		my $ftn = $HfightTurn;
		my $ilt = $HislandLastTime;
		if($round && $ino > $Htournament) {
			$ino = $Htournament;
		}
		my $fturn = 0;
		my $nofight = 0;
		if($HislandFightMode == 1) {
			$fturn = $HislandChangeTurn - $HyosenTurn - $HdevelopeTurn;
		} elsif($HislandFightMode == 2) {
			$ftn = $HfinalTurn if($ino <= 2);
			$fturn = $HislandChangeTurn - $HyosenTurn - $HdevelopeTurn - $ftn;
			foreach ($HbfieldNumber..$islandNumber) {
				$nofight++ if($Hislands[$_]->{'fight_id'} < 0);
			}
		}
		$tournament .= "ターン\t$AfterName数\t進行状態\t更新時間\n";
		while($ino > 1){
			if($itn < $HyosenTurn){
				# 予選
				$HislandFightMode = 0;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime1[($itn % ($#HtmTime1 + 1))] : $HyosenTime;
				$timeString = timeToString($ilt);
				foreach(1..$HyosenRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\t予選\t$timeString\n";
					last if($itn == $HyosenTurn);
				}
			} elsif($itn < $HyosenTurn + $HdevelopeTurn + $fturn) {
				# 開発
				$ino = $Htournament if(($HislandFightMode == 0) && ($ino > $Htournament));
				$HislandFightMode = 1;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime2[($itn % ($#HtmTime2 + 1))] : $HdevelopeTime;
				$timeString = timeToString($ilt);
				$ftn = $HfinalTurn if($ino <= 2);
				foreach(1..$HdeveRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\t開発\t$timeString\n";
					last if($itn == $HyosenTurn + $HdevelopeTurn + $fturn);
				}
			} elsif($itn < $HyosenTurn + $HdevelopeTurn + $ftn + $fturn) {
				# 戦闘
				$HislandFightMode = 2;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime3[($itn % ($#HtmTime3 + 1))] : $HfightTime;
				$timeString = timeToString($ilt);
				#$tournament .= "$itn\t$ino\t戦闘♪\t$timeString\t$HfightRepCount\n";
				foreach(1..$HfightRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\t戦闘♪\t$timeString\n";
					last if($itn == $HyosenTurn + $HdevelopeTurn + $ftn + $fturn);
				}
			} else {
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime2[($itn % ($#HtmTime2 + 1))] : ($itn == $HyosenTurn + $HdevelopeTurn + $ftn + $fturn) ? $HinterTime : $HdevelopeTime;
				if($HislandFightMode == 2) {
					$ino = int(($ino + $nofight) / 2 + 0.5);
					$ino++ if(($ino > 2) && (($ino % 2) != 0) && ($HconsolationMatch));
					$nofight = 0;
				}
				$HislandFightMode = 1;
				$timeString = timeToString($ilt);
				$fturn += $HdevelopeTurn + $ftn;
				$ftn = $HfinalTurn if($ino <= 2);
				if($ino > 1) {
					foreach(1..$HdeveRepCount){
						$itn++;
						$tournament .= "$itn\t$ino\t開発\t$timeString\n";
						last if($itn == $HyosenTurn + $HdevelopeTurn + $fturn);
					}
				}
			}
		}
		$tournament .= "</textarea></DIV>";
		$sec2 = ($HyosenTime % 60);
		$sec2 = ($sec2 ? "$sec2秒" : '');
		$min2 = ($HyosenTime % 3600);
		$min2 = ($min2 ? "$min2分" : '');
		$hour2 = int($HyosenTime / 3600);
		$hour2 = ($hour2 ? "$hour2時間" : '');

		$src .= <<"END";
<blockquote>
予選後通過島数　<B>$Htournament$AfterName</B><BR>
予選期間ターン数　<B>$HyosenTurnターン</B><BR>
予選期間中のターン更新間隔　<B>${HyosenTime}秒 ( $hour2$min2$sec2 )</B><BR>
予選期間中１回の更新で何ターン進めるか　<B>$HyosenRepCountターン</B><BR><BR>
END

		$sec2 = ($HdevelopeTime % 60);
		$sec2 = ($sec2 ? "$sec2秒" : '');
		$min2 = ($HdevelopeTime % 3600);
		$min2 = ($min2 ? "$min2分" : '');
		$hour2 = int($HdevelopeTime / 3600);
		$hour2 = ($hour2 ? "$hour2時間" : '');

		$src .= <<"END";
開発期間ターン数　<B>$HdevelopeTurnターン</B><BR>
開発期間中のターン更新間隔　<B>${HdevelopeTime}秒 ( $hour2$min2$sec2 )</B><BR>
開発期間中１回の更新で何ターン進めるか　<B>$HdeveRepCountターン</B><BR><BR>
END

		$sec2 = ($HinterTime % 60);
		$sec2 = ($sec2 ? "$sec2秒" : '');
		$min2 = ($HinterTime % 3600);
		$min2 = ($min2 ? "$min2分" : '');
		$hour2 = int($HinterTime / 3600);
		$hour2 = ($hour2 ? "$hour2時間" : '');

	$src .= <<"END";
開発期間終了後の戦闘期間への移行までの時間　<B>${HinterTime}秒 ( $hour2$min2$sec2 )</B><BR><BR>
END

		$sec2 = ($HfightTime % 60);
		$sec2 = ($sec2 ? "$sec2秒" : '');
		$min2 = ($HfightTime % 3600);
		$min2 = ($min2 ? "$min2分" : '');
		$hour2 = int($HfightTime / 3600);
		$hour2 = ($hour2 ? "$hour2時間" : '');
		my $halffight = int($HfightTurn/2);
		my $halffinal = int($HfinalTurn/2);
		my $no_workPop = "$Hno_work$HunitPop";
		1 while $no_workPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= <<"END";
戦闘期間ターン数　<B>$HfightTurnターン</B><BR>
戦闘期間中のターン更新間隔　<B>${HfightTime}秒 ( $hour2$min2$sec2 )</B><BR>
戦闘期間中１回の更新で何ターン進めるか　<B>$HfightRepCountターン</B><BR><BR>
決勝戦の戦闘期間ターン数　<B>$HfinalTurnターン</B><BR>
不戦勝の開発停止ターン数　<B>(回戦数)x${HnofightUp}+${HnofightTurn}ターン</B><BR>
不戦勝にならないための、必要戦闘行為回数　<B>$do_fight回</B><BR>
※戦闘期間の半分（$halffightターン・決勝は$halffinalターン）が経過するまでに、「相手がいなくなった場合」及び「相手の戦闘行為回数が$do_fight回に満たなかった（相手が１度も艦隊派遣を行わなかった）場合」は不戦勝扱いとなります。<BR>
　この場合は、戦闘開始時の島の状態に戻され、開発停止になります。<BR>
　停止期間は、（回戦数×${HnofightUp}+${HnofightTurn}）− 経過ターン数です。 <BR>
人口増加ストップする資金繰り回数　<B>$HstopAddPop回</B><BR>
失業者数のボーダーライン　<B>$no_workPop</B>　※この数値を超えると、人口増加がストップします（予選のみ）<BR>
「敗者復活」ができるようにするか？　<B>$doStr[$HconsolationMatch]</B>　※戦闘終了後奇数(不戦勝が発生する見込み)になる場合に敗退する$AfterNameで最上位の$AfterNameを復活します。<BR>
<BR>$tournament</blockquote>
END
	}

# 友好国設定
#----------------------

	$src .= <<"END";
<HR>
<a name='amity'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 友好国設定</H3></a>
友好国設定を使うか？　<B>$useStr[$HuseAmity]</B><BR>
END

	if($HuseAmity && !$HarmisticeTurn) {
		if($HamityMax) {
			$src .= "友好国設定可能最大数　<B>$HamityMax${AfterName}</B><BR>";
		} else {
			$src .= "友好国設定可能最大数　<B>制限なし</B><BR>";
		}
		if($HamityMoney) {
			my $amityMoney = "$HamityMoney$HunitMoney";
			1 while $amityMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= "友好国１$AfterNameあたりの維持費用　<B>$amityMoney</B><BR>　※(友好国に設定している$AfterName数)×${amityMoney}が毎ターン必要になります。<BR>";
		}
		if($HamityDisarm) {
			$src .= "　※艦隊派遣中の${AfterName}に対しては、<B>友好国の破棄ができません</B>。(認定はできます)<BR>";
		}
		if($HamityInvalid) {
			$src .= "　※バトルフィールドでは「艦艇の補給」「索敵しない」「攻撃しない」設定が無効になります。<BR>";
		}
	}

# 宣戦布告システム
#----------------------
	$src .= <<"END";
<HR>
<a name='dewar'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 宣戦布告システム</H3></a>
「宣戦布告」「停戦交渉」コマンドを使うか？　<B>$useStr[(($HuseDeWar > 0) && !$HarmisticeTurn && !$HsurvivalTurn && !$Htournament)]</B>$useDeWar<BR>
END

	if(!$HarmisticeTurn && !$HsurvivalTurn && !$Htournament) {
		if($HuseDeWar) {
			my $matchplay = ('<B>しない</B>', '<B>する</B>(制限だけ)', '<B>する</B>(戦争勃発ログ出力と同時に、自動で２島の拡張データのカウンターリセットと地形保存を行う)')[$HmatchPlay];
			$src .= <<"END";
宣戦布告するのもされるのも１島だけにする？　$matchplay<BR>
宣戦布告猶予ターン　<B>$HdeclareTurnターン</B><BR>
停戦打診コマンドで停戦合意した場合、自動で艦隊を帰還するか？　<B>$doStr[$HceasefireAutoNavyReturn]</B><BR>
拡張データのカウンター設定をプレイヤーに公開するか？　<B>$doStr[$HcounterSetting]</B><BR>
END
		}
	}

# イベントシステム
#----------------------

	$src .= <<"END";
<HR>
<a name='event'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> イベントシステム</H3></a>
イベント開始前の告知ターン数　<B>$HnoticeTurnターン</B><BR>
<TABLE BORDER>
<TR><TH>${HtagTH_}イベントの種類${H_tagTH}</TH><TH>${HtagTH_}勝利条件など${H_tagTH}</TH></TR>
<TR><TH>サバイバル</TH>
<TD class='N'>
<u>開催$AfterNameに派遣されている他$AfterName所属の艦艇をすべて撃破し，最後まで生き残った$AfterNameが優勝！</u>
<BR>　・所属不明艦艇は撃破しなくてもよい。
<BR>　・終了ターンは勝負がつくまでで，追加派遣はできない。
</TD></TR>
<TR><TH>艦艇経験値獲得バトル</TH>
<TD class='N'>
<u>派遣された艦艇が終了ターンまでに獲得した経験値の合計が最も高い$AfterNameが優勝！</u>
<BR>　・派遣艦艇すべてが開催期間中に獲得した経験値の合計で判定する。
<BR>　・獲得経験値の合計が同じ$AfterNameが複数ある場合は，サドンデスにはいる。
<BR>　・高い経験値をもつ艦艇の派遣や開催期間中の派遣が可能かどうかは設定による。
</TD></TR>
<TR><TH>艦艇撃沈バトル</TH>
<TD class='N'>
<u>派遣された艦艇が終了ターンまでに沈没させた艦艇数総計が最も高い$AfterNameが優勝！</u>
<BR>　・派遣艦艇すべてが開催期間中に沈没させた艦艇数で判定する。
<BR>　・沈没させた艦艇数が同じ$AfterNameが複数ある場合は，サドンデスにはいる。
<BR>　・開催期間中の派遣が可能かどうかは設定による。
</TD></TR>
<TR><TH>怪獣退治バトル</TH>
<TD class='N'>
<u>派遣された艦艇が終了ターンまでに倒した怪獣・巨大怪獣の総計が最も高い$AfterNameが優勝！</u>
<BR>　・派遣艦艇すべてが開催期間中に倒した怪獣数(+ 巨大怪獣数)で判定する。
<BR>　・倒した怪獣数(+ 巨大怪獣数)が同じ$AfterNameが複数ある場合は，サドンデスにはいる。
<BR>　・開催期間中の派遣が可能かどうかは設定による。
</TD></TR>
<TR><TH>賞金稼ぎバトル</TH>
<TD class='N'>
<u>派遣された艦艇が終了ターンまでに獲得した賞金総額が最も高い$AfterNameが優勝！</u>
<BR>　・派遣艦艇すべてが開催期間中に獲得した怪獣退治・巨大怪獣退治の賞金総額で判定する。
<BR>　・賞金総額が同じ$AfterNameが複数ある場合は，サドンデスにはいる。
<BR>　・開催期間中の派遣が可能かどうかは設定による。
</TD></TR>
</TABLE>
※派遣艦艇すべてが撃沈するなどの理由で，終了判定時に開催$AfterNameに艦艇がいない参戦$AfterNameは，順位がつきません！
END

# 同盟
#----------------------

	my $allyDisDown = '同じ';
	if($HallyDisDown) {
		$allyDisDown = $HallyDisDown . '倍';
	}
	my $allyMax = (!$HallyMax) ? '無制限' : "$HallyMax$AfterName";
	my $allyAutoBreakup = ('しない', 'する', 'する[掲示板を消滅ログへ移行]')[$HallyAutoBreakup];
	my $costMakeAlly = "$HcostMakeAlly$HunitMoney";
	1 while $costMakeAlly =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $costKeepAlly = "$HcostKeepAlly$HunitMoney";
	1 while $costKeepAlly =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END";
<HR>
<a name='ally'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 同盟システム</H3></a>
同盟の作成を許可するか？　<B>$doStr[$HallyUse]</B><BR>
END

	$src .= <<"END" if($HallyUse);
ひとつの同盟にしか加盟できないようにするか？　<B>$doStr[$HallyJoinOne]</B><BR>
　※この設定にかかわらず盟主はひとつの同盟にしか加盟できません！<BR>
盟主島消滅時に同盟を自動的に解散するか？　<B>$allyAutoBreakup</B><BR>
１つの同盟への加盟可能最大$AfterName数　<B>$allyMax</B><BR>
同盟に加盟している場合の災害発生確率（通常時に対する割合）　<B>$allyDisDown</B><BR>
　※対象となる災害：地震、津波、台風、隕石、巨大隕石、噴火<BR><BR>
同盟にかかる費用　結成・変更 <B>${costMakeAlly}</B> / 維持費 <B>${costKeepAlly}</B><BR>
END

# 地形・コマンド設定
#----------------------
	$src .= <<"END";
<HR>
<a name='usecom'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 地形・コマンド設定</H3></a>
<TABLE><TR>
END

	# 海，荒地，平地，山，森，農場，工場, 海底油田，ハリボテ，防衛施設，ミサイル基地，海底基地，防波堤，機雷，コア
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'>一般地形</TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
	foreach ("$HlandSea", "$HlandWaste", "$HlandPlains", "$HlandMountain", "$HlandForest", "$HlandFarm", "$HlandFactory", "$HlandOil", "$HlandHaribote", "$HlandDefence", "$HlandBase", "$HlandSbase", "$HlandBouha", "$HlandSeaMine", "$HlandCore") {
		next if (($_ == $HlandForest) && !$HusePlantSellTree);
		next if (($_ == $HlandFarm) && !$HuseFarm);
		next if (($_ == $HlandFactory) && !$HuseFactory);
		next if (($_ == $HlandMountain) && !$HuseMountain);
		next if (($_ == $HlandBase) && !$HuseBase);
		next if (($_ == $HlandSbase) && (!$HuseSbase || $Htournament));
		next if (($_ == $HlandBouha) && !$HuseBouha);
		next if (($_ == $HlandSeaMine) && !$HuseSeaMine);
		next if (($_ == $HlandCore) && !$HuseCore);
		my @set = @{$HlandName[$_]};
		if(defined $set[0]) {
			pop(@set) if(($_ == $HlandDefence) && (!$HdurableDef || ($HdurableDef < $HdefLevelUp)));
			foreach $i (0..$#set) {
				$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$_][$i]'></TD><TH>$HlandName[$_][$i]</TH></TR>";
			}
		} else {
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$_]'></TD><TH>$HlandName[$_]</TH></TR>";
		}
	}
	$src .= "</TABLE></TD>";
	# 都市系
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#town' style='text-decoration=none'>都市系</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
	foreach (0..$#HlandTownName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandTownImage[$_]'></TD><TH>$HlandTownName[$_]</TH></TR>";
	}
	$src .= "</TABLE></TD>";
	# 記念碑
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#monument' style='text-decoration=none'>記念碑</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
	foreach (0..$#HmonumentName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonumentImage[$_]'></TD><TH>$HmonumentName[$_]</TH></TR>";
	}
	$src .= "</TABLE></TD>";
	# 複合地形
	if($HuseComplex) {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#complex' style='text-decoration=none'>複合地形</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
		foreach (0..$#HcomplexName) {
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$_]'></TD><TH>$HcomplexName[$_]</TH></TR>";
		}
		$src .= "</TABLE></TD>";
	}
	# 海軍
	if($HnavyName[0] ne '') {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#navy' style='text-decoration=none'>海軍</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
		foreach (0..$#HnavyName) {
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HnavyImage[$_]'></TD><TH>$HnavyName[$_]</TH></TR>";
			next if(!($HnavySpecial[$_] & 0x4));
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HnavyImage2[$_]'></TD><TH>$HnavyName[$_]<small>(潜水)</small></TH></TR>";
		}
		$src .= "</TABLE></TD>";
	}
	# 怪獣
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#monster' style='text-decoration=none'>怪獣</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
	foreach (0..$#HmonsterName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImage[$_]'></TD><TH>$HmonsterName[$_]</TH></TR>";
		next if(!($HmonsterSpecial[$_] & 0x4));
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImage2[$_]'></TD><TH>$HmonsterName[$_]<small>(硬化)</small></TH></TR>";
	}
	$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImageUnderSea'></TD><TH>共通設定<small>(潜水)</small></TH></TR>";
	$src .= "</TABLE></TD>";
	# 巨大怪獣
	if($HhugeMonsterAppear) {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#hmonster' style='text-decoration=none'>巨大怪獣</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH></TR>";
		foreach (0..$#HhugeMonsterName) {
			my(@monImage);
			my $space = "<img src='${HimageDir}/$HlandImage[$HlandWaste][0]' width=16 height=32>";
			foreach $i (0..6) {
				$monImage[$i] = ($HhugeMonsterImage[$_][$i] eq '') ? "${HimageDir}/$HlandImage[$HlandWaste][0]" : "${HimageDir}/$HhugeMonsterImage[$_][$i]";
			}
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'>
$space<img src='$monImage[6]'><img src='$monImage[1]'>$space<br>
<img src='$monImage[5]'><img src='$monImage[0]'><img src='$monImage[2]'><br>
$space<img src='$monImage[4]'><img src='$monImage[3]'>$space
</TD><TH>$HhugeMonsterName[$_]</TH></TR>
END
		}
		$src .= "</TABLE></TD>";
	}

	$src .= "</TR></TABLE><BR>";

	$src .= "防波堤を使うか？　<B>$useStr[($HuseBouha > 0)]</B><BR>";
	if($HuseBouha) {
		$src .= "　防波堤保有可能数　<B>$HuseBouha</B><BR>";
	}

	$src .= "機雷を使うか？　<B>$useStr[($HuseSeaMine > 0)]</B><BR>";
	if($HuseSeaMine) {
		$src .= "　機雷設置可能数　<B>$HuseSeaMine</B><BR>";
		$src .= "　自$AfterNameの機雷でダメージを受けるか？　<B>$selfStr[$HmineSelfDamage]</B><BR>";
	}
	my $edgeDef = "";
	if($HedgeReclaim > 1) {
		my $edgeSize1 = $HedgeReclaim - 1;
		my $edgeSizeX = $HislandSizeX - $HedgeReclaim;
		my $edgeSizeY = $HislandSizeY - $HedgeReclaim;
		$edgeDef = "<B>${HedgeReclaim}Hex</B>";
		$edgeDef .= "(x座標の一方が'$edgeSize1'以下か'$edgeSizeX'以上の地点)か(y座標の一方が'$edgeSize1'以下か'$edgeSizeY'以上の地点)" if(!$HoceanMode);
	} elsif($HedgeReclaim) {
		my $edgeSizeX = $HislandSizeX - 1;
		my $edgeSizeY = $HislandSizeY - 1;
		$edgeDef = '<B>1Hex</B>';
		$edgeDef .= "(x座標の一方が'0'か'$edgeSizeX'の地点)か(y座標の一方が'0'か'$edgeSizeY'の地点)" if(!$HoceanMode);
	}

	$src .= <<"END";
<BR>
伐採をターン消費なしにするか？　<B>$doStr[$HnoturnSellTree]</B><BR>
艦艇の周囲が埋め立てできる裏ワザ(バグ?)を修正するか？　<B>$doStr[$HnavyReclaim]</B><BR>
怪獣(海にいる)の周囲が埋め立てできる裏ワザ(バグ?)を修正するか？　<B>$doStr[$HmonsterReclaim]</B><BR>
港に隣接した深い海でしか艦艇を建造できないようにするか？　<B>$doStr[$HnavyBuildFlag]</B><BR>
浅瀬にも移動可＆派遣可にするか？　<B>$doStr[$HnavyMoveAsase]</B><BR>
$AfterNameの最外周${edgeDef}を埋め立て不可にするか？　<B>$doStr[($HedgeReclaim > 0)]</B><BR>
END

	$src .= <<"END";
<BR>$AfterNameの面積を統一するか？　<B>$doStr[$HnewIslandSetting]</B><BR>
END
	$HcountLandArea = 16 if($HcountLandArea < 16);
	$HcountLandPlains = $HcountLandArea - $HcountLandWaste - $HcountLandForest - $HcountLandTown - $HcountLandMountain - $HcountLandPort;
	my $bcol = 6;
	my($bstr1, $bstr2);
	if($HuseBase) {
		$bcol++;
		$bstr1 = "<TH>${HtagTH_}基地の数${H_tagTH}</TH>";
		$bstr2 = "<TD align='center'>$HcountLandBase</TD>";
		$HcountLandPlains -= $HcountLandBase;
	}

	my $valueLandTownPop = "$HvalueLandTown$HunitPop";
	1 while $valueLandTownPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $valueLandMountainPop = "$HvalueLandMountain$HunitPop";
	1 while $valueLandMountainPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END" if($HnewIslandSetting);
<BR>
<TABLE>
<TR $HbgInfoCell><TH colspan=$bcol>${HtagTH_}陸地総数　${HnormalColor_}${HcountLandArea}${H_normalColor}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}浅瀬の数${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}平地の数${H_tagTH}</TH><TH>${HtagTH_}荒地の数${H_tagTH}</TH><TH>${HtagTH_}森の数 (木の数)${H_tagTH}</TH><TH>${HtagTH_}町の数 (人口)${H_tagTH}</TH><TH>${HtagTH_}山の数 (規模)${H_tagTH}</TH>$bstr1<TH>${HtagTH_}軍港の数${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$HcountLandPlains</TD><TD align='center'>$HcountLandWaste</TD><TD align='right'>${HcountLandForest} ($HvalueLandForest$HunitTree)</TD><TD align='right'>${HcountLandTown} ($valueLandTownPop)</TD><TD align='right'>${HcountLandMountain} ($valueLandMountainPop)</TD>$bstr2<TD align='center'>$HcountLandPort</TD><TD align='center'>$HcountLandSea</TD></TR>
</TABLE></B><BR>
END

# 都市系
#-------------------------
	my $tcol1 = (!$HsurvivalTurn) ? 2 : 4;
	my $tcol2 = (!$HsurvivalTurn) ? 1 : 2;
	my $trow1 = (!$HsurvivalTurn) ? 1 : 2;
	my $trow2 = (!$HsurvivalTurn) ? 2 : 3;

	$src .= <<"END";
<HR>
<a name='town'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 都市系設定</H3></a>
<TABLE>
<TR $HbgInfoCell>
<TH colspan=3>${HtagTH_}都市系${H_tagTH}</TH>
<TH colspan=$tcol1>${HtagTH_}人口の増加幅${H_tagTH}</TH>
<TH rowspan=$trow2>${HtagTH_}難民<BR>受け<BR>入れ<BR>上限${H_tagTH}</TH>
<TH rowspan=$trow2>${HtagTH_}食料<BR>不足の<BR>人口<BR>減少値${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=$trow1>${HtagTH_}名称${H_tagTH}</TH>
<TH rowspan=$trow1>${HtagTH_}規模${H_tagTH}</TH>
<TH colspan=$tcol2>${HtagTH_}通常${H_tagTH}</TH><TH colspan=$tcol2>${HtagTH_}誘致${H_tagTH}</TH>
</TR>
END
	if($HsurvivalTurn) {
		$src .= "<TR $HbgInfoCell><TH>${HtagTH_}開発${H_tagTH}</TH><TH>${HtagTH_}戦闘${H_tagTH}</TH><TH>${HtagTH_}開発${H_tagTH}</TH><TH>${HtagTH_}戦闘${H_tagTH}</TH></TR>";
	}
	foreach $i (0..$#HlandTownName) {
		$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandTownImage[$i]'></TD><TH>$HlandTownName[$i]</TH>
END
		my $value = (!$HlandTownValue[$i]) ? '−' : "$HlandTownValue[$i]${HunitPop}以上";
		1 while $value =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= "<TD align='right'>$value</TD>";
		if(!$HsurvivalTurn) {
			my $add1 = (!$Haddpop[$i]) ? '−' : "$Haddpop[$i]${HunitPop}";
			1 while $add1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add2 = (!$HaddpopPropa[$i]) ? '−' : "$HaddpopPropa[$i]${HunitPop}";
			1 while $add2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='right'>$add1</TD><TD align='right'>$add2</TD>
END
		} else {
			my $add1 = (!$HaddpopSD[$i]) ? '−' : "$HaddpopSD[$i]${HunitPop}";
			1 while $add1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add2 = (!$HaddpopSDpropa[$i]) ? '−' : "$HaddpopSDpropa[$i]${HunitPop}";
			1 while $add2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add3 = (!$HaddpopSA[$i]) ? '−' : "$HaddpopSA[$i]${HunitPop}";
			1 while $add3 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add4 = (!$HaddpopSApropa[$i]) ? '−' : "$HaddpopSApropa[$i]${HunitPop}";
			1 while $add4 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='right'>$add1</TD><TD align='right'>$add2</TD>
<TD align='right'>$add3</TD><TD align='right'>$add4</TD>
END
		}
		my $achieve = (!$HachiveValueMax[$i]) ? '−' : "$HachiveValueMax[$i]${HunitPop}";
		1 while $achieve =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $reduction = (!$HreductionPop[$i]) ? '−' : "$HreductionPop[$i]${HunitPop}";
		1 while $reduction =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= <<"END";
<TD align='right'>$achieve</TD><TD align='right'>$reduction</TD>
END
	}
	my $valueLandTownMaxPop = "$HvalueLandTownMax$HunitPop";
	1 while $valueLandTownMaxPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $achivePlainsMaxPop = "$HachivePlainsMax$HunitPop";
	1 while $achivePlainsMaxPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $achivePlainsLossPop = "$HachivePlainsLoss$HunitPop";
	1 while $achivePlainsLossPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END";
</TR></TABLE>
<BR>
人口の最大値　<B>$valueLandTownMaxPop</B><BR>
難民の平地への受け入れ上限　<B>$achivePlainsMaxPop</B>（受け入れ時のロス　<B>$achivePlainsLossPop</B>）<BR>
村の発生率　<B>${HtownGlow}%</B><BR>
艦艇攻撃・ミサイル攻撃命中時、一撃で荒れ地にならず都市ランクが下がるようにするか？　<B>$doStr[$HtownStepDown]</B><BR>
　※ランク２まで（$HlandTownName[0]・$HlandTownName[1]）は一撃で破壊されます。また、破壊力に応じてランクが下がります。
END

# 複合地形
#-------------------------

		$src .= <<"END";
<HR>
<a name='complex'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 複合地形</H3></a>
複合地形を使うか？　<B>$useStr[$HuseComplex]</B><BR>
END
	if($HuseComplex) {
		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}複合<BR>地形${H_tagTH}</TH><TH rowspan=2>${HtagTH_}名称${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}保有<BR>可能<BR>上限${H_tagTH}</TH><TH rowspan=2>${HtagTH_}設置可能地形${H_tagTH}</TH><TH rowspan=2>${HtagTH_}被害規模<BR>/破壊力1${H_tagTH}</TH>
<TH colspan=15>${HtagTH_}破壊された時の地形${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}整地${H_tagTH}</TH><TH>${HtagTH_}埋立${H_tagTH}</TH><TH>${HtagTH_}掘削${H_tagTH}</TH>
<TH>${HtagTH_}地震${H_tagTH}</TH><TH>${HtagTH_}台風${H_tagTH}</TH><TH>${HtagTH_}火災${H_tagTH}</TH><TH>${HtagTH_}津波${H_tagTH}</TH><TH>${HtagTH_}暴動${H_tagTH}</TH>
<TH>${HtagTH_}沈下${H_tagTH}</TH><TH>${HtagTH_}噴火${H_tagTH}</TH><TH>${HtagTH_}隕石${H_tagTH}</TH><TH>${HtagTH_}広域<BR>１${H_tagTH}</TH><TH>${HtagTH_}広域<BR>２${H_tagTH}</TH>
<TH>${HtagTH_}攻撃${H_tagTH}</TH><TH>${HtagTH_}移動${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HcomplexName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH>
END
			if($HcomplexMax[$i]) {
				$src .= "<TD align='right'>$HcomplexMax[$i]</TD>";
			} else {
				$src .= "<TD align='right'>−</TD>";
			}

			$src .= "<TD class='N'>";
			foreach (@{$HcomplexBefore[$i]}) {
				my $lkind = $_->[0];
				my $lvmin = $_->[1];
				my $lvmax = $_->[2];
				my $lname1 = landName($lkind, $lvmin);
				my $lname2 = landName($lkind, $lvmax);
				if($lname1 eq $lname2) {
					$src .= "<span class='check'>$lname1　</span>";
				} else {
					my @set = @{$HlandName[$lkind]};
					my $lname = ($set[0] ne '') ? $set[0] : $HlandName[$lkind];
					$src .= "<span class='check'>$lname($lname1〜$lname2)　</span>";
				}
			}
			foreach (@{$HcomplexBefore2[$i]}) {
				my $lname = $HcomplexName[$_];
				$src .= "<span class='check'>$lname　</span>";
			}
			$src .= "</TD><TD align='center'>";
			my $down = $HcomplexAfter[$i]->{'stepdown'};
			if($down) {
				$src .= $down . 'ランク';
			} elsif(defined $HcomplexAfter[$i]->{'attack'}[0]) {
				$src .= "一撃で壊滅";
			} else {
				$src .= "−";
			}
			$src .= "</TD>";
			my($l, $lv, $lname);
			foreach ('prepare', 'reclaim', 'destroy', 'earthquake', 'typhoon', 'fire', 'tsunami', 'starve', 'falldown', 'eruption', 'meteo', 'wide1', 'wide2', 'attack') {
				$l = $HcomplexAfter[$i]->{$_}[0];
				if(defined $l) {
					$lv =$HcomplexAfter[$i]->{$_}[1];
					$lname = landName($l, $lv);
					my(@limg) = @{$HlandImage[$l]};
					if($limg[0] eq '') {
						$src .= "<TD align='center'><img src='${HimageDir}/$HlandImage[$l]' alt='$lname'></TD>";
					} else {
						$src .= "<TD align='center'><img src='${HimageDir}/$limg[$lv]' alt='$lname'></TD>";
					}
				} else {
					$src .= "<TD align='center'>−</TD>";
				}
			}
			$l = $HcomplexAfter[$i]->{'move'}[0];
			$lv =$HcomplexAfter[$i]->{'move'}[1];
			if(defined $l) {
				if(!$l) {
					$src .= "<TD align='center'><img src='${HimageDir}/$HlandImage[$HlandWaste][0]' alt='$HlandName[$HlandWaste][0]'></TD>";
				} elsif(!$lv) {
					$src .= "<TD align='center'><img src='${HimageDir}/$HlandImage[$HlandSea][1]' alt='$HlandName[$HlandSea][1]'></TD>";
				} else {
					$src .= "<TD align='center'><img src='${HimageDir}/$HlandImage[$HlandSea][0]' alt='$HlandName[$HlandSea][0]'></TD>";
				}
			} else {
				$src .= "<TD align='center'>−</TD>";
			}
			$src .= "</TR>";
		}

		$src .= <<"END";
</TABLE>
　※「被害規模/破壊力1」は、初期値の規模、追加値の規模をそれぞれ１ランクとカウントして、食料・資金ともに被害を受ける数値です。
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}複合<BR>地形${H_tagTH}</TH><TH rowspan=2>${HtagTH_}名称${H_tagTH}</TH>
<TH colspan=11>${HtagTH_}属性${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}周囲<BR>に村<BR>発生${H_tagTH}</TH><TH>${HtagTH_}火災<BR>被害<BR>防止${H_tagTH}</TH><TH>${HtagTH_}台風<BR>被害<BR>防止${H_tagTH}</TH>
<TH>${HtagTH_}力場<BR>発生${H_tagTH}</TH><TH>${HtagTH_}ミサ<br>イル<br>防衛${H_tagTH}</TH><TH>${HtagTH_}艦隊<br>攻撃<br>防衛${H_tagTH}</TH>
<TH>${HtagTH_}対潜<BR>攻撃<BR>対象${H_tagTH}</TH><TH>${HtagTH_}対艦<BR>攻撃<BR>対象${H_tagTH}</TH><TH>${HtagTH_}対地<BR>攻撃<BR>対象${H_tagTH}</TH>
<TH>${HtagTH_}ラン<BR>ダム<BR>収入${H_tagTH}</TH><TH>${HtagTH_}ラン<BR>ダム<BR>収穫${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HcomplexName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH>
END
			foreach (0x1, 0x2, 0x4, 0x10, 0x20, 0x40, 0x100, 0x200, 0x400, 0x1000, 0x2000) {
				$src .= "<TD align='center'>$ox[!($HcomplexAttr[$i] & $_)]</TD>";
			}
			$src .= "</TR>";
		}

		$src .= <<"END";
</TABLE>
<TABLE>
<TR $HbgInfoCell>
<TH rowspan=2>${HtagTH_}複合<BR>地形${H_tagTH}</TH><TH rowspan=2>${HtagTH_}名称${H_tagTH}</TH>
<TH colspan=5>${HtagTH_}ターンフラグ${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}食料フラグ${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}資金フラグ${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}加算<BR>対象${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH><TH>${HtagTH_}増加値${H_tagTH}</TH><TH>${HtagTH_}最大値${H_tagTH}</TH><TH>${HtagTH_}観光${H_tagTH}</TH>
<TH>${HtagTH_}加算<BR>対象${H_tagTH}</TH><TH>${HtagTH_}初期値${H_tagTH}</TH><TH>${HtagTH_}追加値${H_tagTH}</TH><TH>${HtagTH_}最大値${H_tagTH}</TH>
<TH>${HtagTH_}加算<BR>対象${H_tagTH}</TH><TH>${HtagTH_}初期値${H_tagTH}</TH><TH>${HtagTH_}追加値${H_tagTH}</TH><TH>${HtagTH_}最大値${H_tagTH}</TH>
</TR>
END
		my(@turnmax, @foodmax, @moneymax);
		foreach $i (0..$#HcomplexName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH>
END
			my($tname, $tkind, $trate, $tmax, $thide);
			if($HcomplexTPCmax[$i]) {
				$tname = $HcomplexTPname[$i];
				$tkind = ($HcomplexTPkind[$i] eq '') ? '−' : $rankKind{$HcomplexTPkind[$i]};
				$trate = $HcomplexTPrate[$i] . $HcomplexTPunit[$i];
				$turnmax[$i]  = $HcomplexTPCmax[$i] * $HcomplexTPrate[$i];
				$tmax  = $turnmax[$i] . $HcomplexTPunit[$i];
				$thide = $hide[$HcomplexTPhide[$i]];
			} else {
				$tname = '−';
				$tkind = '−';
				$trate = '−';
				$tmax  = '−';
				$thide = '−';
			}
			my($fkind, $fbase, $fplus, $fmax, $mkind, $mbase, $mplus, $mmax);
			$foodmax[$i]  = $HcomplexFPCmax[$i]*$HcomplexFPplus[$i]+$HcomplexFPbase[$i];
			$moneymax[$i]  = $HcomplexMPCmax[$i]*$HcomplexMPplus[$i]+$HcomplexMPbase[$i];
			if($foodmax[$i]) {
				$fkind = $rankKind{$HcomplexFPkind[$i]};
				$fmax  = $foodmax[$i] . "0${HunitPop}規模";
				1 while $fmax =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$fbase = $HcomplexFPbase[$i] . "0${HunitPop}規模";
				1 while $fbase =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$fplus = $HcomplexFPplus[$i] . "0${HunitPop}規模";
				1 while $fplus =~ s/(.*\d)(\d\d\d)/$1,$2/;
			} else {
				$fkind = '−';
				$fmax  = '−';
				$fbase = '−';
				$fplus = '−';
			}
			if($moneymax[$i]) {
				$mkind = $rankKind{$HcomplexMPkind[$i]};
				$mmax  = $moneymax[$i] . "0${HunitPop}規模";
				1 while $mmax =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mbase = $HcomplexMPbase[$i] . "0${HunitPop}規模";
				1 while $mbase =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mplus = $HcomplexMPplus[$i] . "0${HunitPop}規模";
				1 while $mplus =~ s/(.*\d)(\d\d\d)/$1,$2/;
			} else {
				$mkind = '−';
				$mmax  = '−';
				$mbase = '−';
				$mplus = '−';
			}

			$src .= <<"END";
<TD align='right'>$tkind</TD><TD align='center'>$tname</TD><TD align='right'>$trate</TD><TD align='right'>$tmax</TD><TD align='center'>$thide</TD>
<TD align='right'>$fkind</TD><TD align='right'>$fbase</TD><TD align='right'>$fplus</TD><TD align='right'>$fmax</TD>
<TD align='right'>$mkind</TD><TD align='right'>$mbase</TD><TD align='right'>$mplus</TD><TD align='right'>$mmax</TD>
</TR>
END
		}
		$src .= <<"END";
</TABLE>
END
		my @rankup;
		foreach $i (0..$#HcomplexName) {
			push(@rankup, $i) if(defined $HcomplexLevelValue[$i][0]);
		}
		my $col = $#rankup + 1;
		if(@rankup) {
			$src .= <<"END";
<TABLE><TR $HbgInfoCell><TH colspan=$col>${HtagTH_}フラグ値により発展する複合地形${H_tagTH}</TH></TR><TR>
END
			my $rankflag  = { 'turn'=>'ターンフラグ', 'food'=>'食料フラグ', 'money'=>'資金フラグ' };
			foreach $i (@rankup) {
				$src .= <<"END";
<TD class='M'><TABLE>
<TR $HbgInfoCell><TH>${HtagTH_}地形${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH><TH>${HtagTH_}対象フラグ${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH><TH>$rankflag->{"$HcomplexLevelKind[$i]"}</TH>
END
				my $maxflag = ($HcomplexLevelKind[$i] eq 'turn') ? $turnmax[$i] : ($HcomplexLevelKind[$i] eq 'food') ? $foodmax[$i] : $moneymax[$i];
				my($cflag);
				foreach (0..$#{$HcomplexLevelValue[$i]}) {
					$cflag = $HcomplexLevelValue[$i][$_];
					if($cflag) {
						$cflag .= "0${HunitPop}規模" if($HcomplexLevelKind[$i] ne 'turn');
						$cflag .= "以上" if($HcomplexLevelValue[$i][$_] < $maxflag);
						1 while $cflag =~ s/(.*\d)(\d\d\d)/$1,$2/;
					} else {
						$cflag = '−';
					}
					$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexSubImage[$i][$_]'></TD><TD align='center'>$HcomplexSubName[$i][$_]</TD><TD align='center'>$cflag</TD>
END
				}
				$src .= <<"END";
</TABLE></TD>
END
			}
			$src .= <<"END";
</TR></TABLE>
※注・発展しても外観と名称が変化するだけで，実際の機能に特に変化はありません。
<BR>
END
		}
		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell>
<TH colspan=4>${HtagTH_}複合地形開発コマンド　　　${turnStr[1]}■${H_tagComName}<small>ターンを消費する</small>　${turnStr[0]}■${H_tagComName}<small>ターンを消費しない</small>${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}対象フラグ${H_tagTH}</TH><TH colspan=3>${HtagTH_}ターンフラグリセット時${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}名称${H_tagTH}</TH><TH>${HtagTH_}対象地形${H_tagTH}</TH><TH>${HtagTH_}コスト${H_tagTH}</TH><TH>${HtagTH_}説明${H_tagTH}</TH>
<TH>${HtagTH_}設置のみ${H_tagTH}</TH><TH>${HtagTH_}ターン${H_tagTH}</TH><TH>${HtagTH_}食料${H_tagTH}</TH><TH>${HtagTH_}資金${H_tagTH}</TH>
<TH>${HtagTH_}増加対象${H_tagTH}</TH><TH>${HtagTH_}フラグ<BR>の倍率${H_tagTH}</TH><TH>${HtagTH_}処理後<BR>の地形${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HcomplexComName) {
			my $cost = (!$HcomplexComCost[$i]) ? '無料' : "$HcomplexComCost[$i]$HunitMoney";
			1 while $cost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TR $HbgInfoCell><TH>${turnStr[$HcomplexComTurn[$i]]}$HcomplexComName[$i]${H_tagComName}</TH>
<TD align='center'>$HcomplexName[$HcomplexComKind[$i]]</TD><TD align='right'>$cost</TD><TD align='left'>$HcomplexComMsgs[$i]</TD>
END
			my $turn  = $HcomplexComFlag[$i] & 0x1;
			my $food  = $HcomplexComFlag[$i] & 0x2;
			my $money = $HcomplexComFlag[$i] & 0x4;
			my($bonly);
			$bonly = 1 if(!$turn && !$food && !$money);
			my($lname, $kind, $ratio);
			if($turn) {
				if($HcomplexComTFRL[$i][0] ne '') {
					$lname = landName($HcomplexComTFRL[$i][0], $HcomplexComTFRL[$i][1]);
				} else {
					$lname = $HcomplexName[$HcomplexComKind[$i]];
				}
				my $income = $HcomplexComTFInCome[$i];
				$kind  = $rankKind{$income->{'type'}};
				$ratio = $income->{'ratio'};
			} else {
				$lname  = '−';
				$kind   = '−';
				$ratio  = '−';
			}

			$src .= <<"END";
<TD align='center'>$ox[!$bonly]</TD><TD align='center'>$ox[!$turn]</TD><TD align='center'>$ox[!$food]</TD><TD align='center'>$ox[!$money]</TD>
<TD align='center'>$kind</TD><TD align='right'>$ratio</TD><TD align='center'>$lname</TD>
</TR>
END

		}
		$src .= "</TABLE>";
	}

# コア
#-------------------------

	$src .= <<"END";
<HR>
<a name='core'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> コア</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan='2'>${HtagTH_}コア${H_tagTH}</TH><TH>${HtagTH_}設置地形など${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][0]'></TD><TH>$HlandName[$HlandCore][0]</TH>
<TD align='left'>
<!--- コア --->
・平地に設置。整地，掘削が可能。<BR>
・隕石，噴火，地盤沈下，広域被害(2Hex)で破壊される。
</TD></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][1]'></TD><TH>$HlandName[$HlandCore][1]</TH>
<TD align='left'>
<!--- 海上コア --->
・浅瀬に設置。埋立，掘削が可能。<BR>
・隕石，噴火，広域被害(2Hex)で破壊される。
</TD></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][2]'></TD><TH>$HlandName[$HlandCore][2]</TH>
<TD align='left'>
<!--- 海底コア --->
・海に設置。埋立が可能。<BR>
・隕石，噴火，広域被害(1Hex)で破壊される。
</TD></TR>
</TABLE></TD>
建設コマンドを使うか？　<B>$useStr[$HuseCore]</B>
END

	if($HuseCore && $HuseCoreLimit) {
		$src .= "　(注！建設できるのは新規登録された$AfterNameの<B>開発期間だけ</B>です)";
	}
	my $coremax = (!$HcoreMax) ? '無制限' : $HcoreMax;
	my $durablec;
	if($HdurableCore){
		$durablec = "<B>最大$HdurableCoreまでアップ</B>";
	} else {
		$durablec = "<B>なし</B>(通常)";
	}
	my $hidec = '';
	$hidec = "($HlandName[$HlandCore][0] => <B>森</B>，$HlandName[$HlandCore][1]・$HlandName[$HlandCore][2] => <B>海</B>)" if($HcoreHide);
	my @coreless = ('沈没しない', '沈没する', '死滅判定回避機能発動');
	$src .= <<"END";
<BR><BR>
保有可能最大数　<B>$coremax</B><BR>
コアの耐久力設定？　$durablec<BR>
コアを偽装するか？　<B>$doStr[$HcoreHide]</B>　$hidec<BR><BR>
コアを保有しない島は沈没する？　<B>$coreless[$HcorelessDead]</B>　(注！設定にかかわらず，新規登録された$AfterNameの<B>開発期間は沈没しません</B>。)<BR>
END

# 海軍
#-------------------------

		$src .= <<"END";
<HR>
<a name='navy'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 海軍</H3></a>
END
	if($HnavyName[0] eq '') {
		$src .= "海軍は<B>ありません！</B><BR>";
	} else {
#		$src .= "海軍(軍港および艦艇)の経験値の最大値　<B>$HmaxExpNavy</B><BR>";
#		$src .= "<TABLE><TR $HbgInfoCell><TH>海軍のレベル</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>レベルUPに必要な経験値</TH><TD align='center'>0</TD>";
#		foreach (@navyLevelUp) {
#			$src .= "<TD align='center'>$_</TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>攻撃回数</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'>+$HnavyFirePlus[int($_/2)]</TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>耐久力</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'>+$HnavyMaxHpPlus[int(($_ - 1)/2)]</TD>";
#		}
		$src .= "</TR></TABLE>";

		$src .= <<"END";
残骸売却時に金塊が発見される確率　<B>${HnavyProbWreckGold}%</B><BR>
他$AfterNameに派遣中の艦隊も補給するか？　<B>$doStr[$HnavySupplyFlag]</B>　※この設定が「しない」の場合「補給能力」の有無が意味を持ちます。<BR><BR>
END

		my $priList;
		my $pFlag = 0;
		foreach (@HpriStr) {
			$priList .= "⇒" if($pFlag);
			$pFlag++;
			$priList .= $_;
		}
		my $navyMaximum = (!$HnavyMaximum ? '無制限' : "$HnavyMaximum");
		my $fleetMaximum = (!$HfleetMaximum ? '無制限' : "$HfleetMaximum");
		my $portRetention1 = (!$HportRetention ? '　軍港数による<B>制限なし</B>' : "　軍港１港につき<B>$HportRetention</B>まで");
		my $portRetention2 = (!$HportRetention ? '無制限' : "$HportRetention");
		my $nCol = 3;
		$nCol++ if($HmaxComNavyLevel);
		$src .= <<"END";
「一斉攻撃」コマンドを使うか？　<B>$useStr[$HuseTarget]</B><BR><BR>
自$AfterName以外にいる艦隊の耐久力を表示するか？　<B>$doStr[$HnavyShowInfo]</B><BR>
攻撃した艦艇自身が射程範囲にある場合、自爆(被弾)することもあるようにするか？　<B>$anStr[$HnavySelfAttack]</B><BR>
<BR>艦艇攻撃で被弾した艦艇や地形が自$AfterNameの場合、無害にするか？　<B>$saftyStr[$HnavySafetyZone]</B><BR>
　無害化が無効になる確率　<B>${HnavySafetyInvalidp}%</B>(無害化機能が発動する場面で判定)<BR>
<BR>射程内の地形による攻撃の優先順位(デフォルト)　<B>$priList</B>(${nearfar[$Hnearfar]})</B><BR>
<BR>保有可能艦艇数　<B>$navyMaximum</B>　(１艦隊あたり <B>$fleetMaximum</B>$portRetention1)
貿易能力のある艦艇が派遣されていない$AfterNameへは援助コマンドが使えなくする？　<B>$doStr[$HtradeAbility]</B><BR>
<BR>
所属不明の艦艇が出現するか？　<B>$doStr[$HnavyUnknown]</B><BR>
END

		if($HnavyUnknown) {
			$HdisNavy *= 0.01;# 所属不明艦艇
			$HdisNavyBF *= 0.01;# 所属不明艦艇(Battle Field)
			$HdisNavyBF    = $HdisNavy*2 if(!$HdisNavyBF);
			$src .= "単位面積あたりの艦艇出現率　<B>${HdisNavy}%</B>　（バトルフィールド：<B>${HdisNavyBF}%</B>）<BR>";
		}

		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH colspan='$nCol'>${HtagTH_}海軍${H_tagTH}</TH>
END

		$src .= "<TH rowspan=2>${HtagTH_}所属<br>不明艦<br>出現人口<br>(比率)${H_tagTH}</TH>" if($HnavyUnknown);

		$src .= <<"END";
<TH>${HtagTH_}保有可能上限${H_tagTH}</TH><TH colspan=2>${HtagTH_}耐久力${H_tagTH}</TH><TH rowspan=2>${HtagTH_}破壊<br>力${H_tagTH}</TH><TH rowspan=2>${HtagTH_}攻撃<br>数${H_tagTH}</TH><TH rowspan=2>${HtagTH_}攻撃<br>範囲${H_tagTH}</TH><TH rowspan=2>${HtagTH_}射程<br>範囲${H_tagTH}</TH><TH colspan=2>${HtagTH_}経験値${H_tagTH}</TH><TH rowspan=2>${HtagTH_}建造<br>費用${H_tagTH}</TH><TH rowspan=2>${HtagTH_}工期${H_tagTH}</TH><TH rowspan=2>${HtagTH_}弾薬<br>１発<br>の<br>費用${H_tagTH}</TH><TH rowspan=2>${HtagTH_}維持<br>費用${H_tagTH}</TH><TH rowspan=2>${HtagTH_}維持<br>食料${H_tagTH}</TH><TH rowspan=2>${HtagTH_}航続<br>ターン${H_tagTH}</TH><TH rowspan=2>${HtagTH_}残骸<br>確率${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}自$AfterName${H_tagTH}</TH><TH>${HtagTH_}他$AfterName${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH>
END

		$src .= "<TH>${HtagTH_}建造<br>レベル${H_tagTH}</TH>" if($HmaxComNavyLevel);

		$src .= <<"END";
<TD align='center'>１艦隊:$fleetMaximum<BR>$portRetention2/1港<BR>合計:$navyMaximum</TD>
<TH>${HtagTH_}初期${H_tagTH}</TH><TH>${HtagTH_}最終${H_tagTH}</TH>
<TH>${HtagTH_}撃沈<br>時${H_tagTH}</TH><TH>${HtagTH_}建造<br>時${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HnavyName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><span class='myFleetCell'><img src='${HimageDir}/$HnavyImage[$i]' class='myFleet'></span></TD><TD align='right'><img src='${HimageDir}/$HnavyImage[$i]'></TD><TH>$HnavyName[$i]</TH>
END

			my($level, $exp);
			my $maxComNavyLevel = $HmaxComNavyLevel-1;
			my $bExp = $HnavyBuildExp[$i];
			foreach (0..$maxComNavyLevel) {
				if($i <= $HcomNavyNumber[$_]) {
					$level = $_ + 1;
					last;
				}
				$level = '★';
			}
			if($level == 1) {
				$exp = 0;
			} elsif($level ne '★') {
				$exp = $HcomNavyBorder[$level-2];
			} else {
				$exp = '不明';
				$bExp = '−';
			}
			$src .= "<TD align='center'><B>${level}</B><BR>(${exp})</TD>" if($HmaxComNavyLevel);
			if($HnavyUnknown) {
				my $unknownpop = ($HdisNavyBorder[$i]) ? $HdisNavyBorder[$i] . $HunitPop : '−';
				1 while $unknownpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
				my $unknownratio = $HdisNavyRatio[$i];
				$src .= "<TD align='right'>$unknownpop<BR>(${unknownratio})</TD>";
			}
			my $kindMax = (!$HnavyKindMax[$i]) ? '無制限' : $HnavyKindMax[$i];
			my $damage = $HnavyDamage[$i];
			$damage = 1 if(!$damage);
			my $nCost = (!$HnavyCost[$i]) ? "−" : ($HnavyCost[$i] > 0 ? "$HnavyCost[$i]$HunitMoney" : "<DIV class='Money' align=left>収入</DIV>" . - $HnavyCost[$i] . "$HunitMoney");
			1 while $nCost =~ s/(.*\d)(\d\d\d)/$1,$2/;
#この下
			my $nBuild = (!$HnavyBuildTurn[$i]) ? "−" : ($HnavyBuildTurn[$i] > 0 ? "$HnavyBuildTurn[$i]ターン" : "<DIV class='Money' align=left></DIV>" . - $HnavyBuildTurn[$i] . "ターン");
			1 while $nBuild =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $sCost = (!$HnavyShellCost[$i]) ? "−" : ($HnavyShellCost[$i] > 0 ? "$HnavyShellCost[$i]$HunitMoney" : "<DIV class='Money' align=left>収入</DIV>" . - $HnavyShellCost[$i] . "$HunitMoney");
			1 while $sCost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $nMoney = (!$HnavyMoney[$i]) ? "−" : ($HnavyMoney[$i] > 0 ? "$HnavyMoney[$i]$HunitMoney" : "<DIV class='Money' align=left>収入</DIV>" . - $HnavyMoney[$i] . "$HunitMoney");
			1 while $nMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $nFood = (!$HnavyFood[$i]) ? "−" : ($HnavyFood[$i] > 0 ? "$HnavyFood[$i]$HunitFood" : "<DIV class='Food' align=left>収穫</DIV>" . - $HnavyFood[$i] . "$HunitFood");
			1 while $nFood =~ s/(.*\d)(\d\d\d)/$1,$2/;
#この下
			my $nCruise = (!$HnavyCruiseTurn[$i]) ? "−" : ($HnavyCruiseTurn[$i] > 0 ? "$HnavyCruiseTurn[$i]ターン" : "<DIV class='Food' align=left>収穫</DIV>" . - $HnavyCruiseTurn[$i] . "ターン");
			1 while $nCruise =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='center'>$kindMax</TD><TD align='right'>$HnavyHP[$i]</TD><TD align='right'>$HnavyMaxHP[$i]</TD><TD align='right'>$damage</TD><TD align='right'>$HnavyFire[$i]</TD><TD align='right'>$HnavyFireHex[$i]</TD><TD align='right'>$HnavyFireRange[$i]</TD><TD align='right'>$HnavyExp[$i]</TD><TD align='right'>$bExp</TD>
<TD align='right'>$nCost</TD><TD align='right'>$nBuild</TD><TD align='right'>$sCost</TD><TD align='right'>$nMoney</TD><TD align='right'>$nFood</TD><TD align='right'>$nCruise</TD><TD align='right'>$HnavyProbWreck[$i]%</TD>
</TR>
END
		}

		$src .= "</TABLE>";
		if($HmaxComNavyLevel) {
			$src .= "　※「レベル」のカッコ内は建造に必要な『総獲得経験値』";
			$src .= "(建造には、<B>軍港のレベルも建造レベルと同じ数値が必要</B>になります)" if($HmaxComPortLevel);
		}

		$src .= <<"END";
<BR><TABLE>
<TR $HbgInfoCell><TH colspan=3>${HtagTH_}海軍${H_tagTH}</TH>
<TH colspan=26>${HtagTH_}能力${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}自$AfterName${H_tagTH}</TH><TH>${HtagTH_}他$AfterName${H_tagTH}</TH><TH>${HtagTH_}名称${H_tagTH}</TH>
<TH>${HtagTH_}移動<br>が<br>速い${H_tagTH}</TH><TH>${HtagTH_}移動が<br>とても<br>速い${H_tagTH}</TH><TH>${HtagTH_}潜水する<br>(浮上率)${H_tagTH}</TH><TH>${HtagTH_}飛行<BR>する${H_tagTH}</TH>
<TH>${HtagTH_}先行<br>移動${H_tagTH}</TH><TH>${HtagTH_}ミサ<br>イル<br>防衛${H_tagTH}</TH><TH>${HtagTH_}艦隊<br>攻撃<br>防衛${H_tagTH}</TH><TH>${HtagTH_}移動<BR>操縦<BR>(旗艦)${H_tagTH}</TH>
<TH>${HtagTH_}対潜<br>攻撃${H_tagTH}</TH><TH>${HtagTH_}対艦<br>攻撃${H_tagTH}</TH><TH>${HtagTH_}対地<br>攻撃${H_tagTH}</TH><TH>${HtagTH_}対空<br>攻撃${H_tagTH}</TH>
<TH>${HtagTH_}水雷系<BR>対潜系${H_tagTH}</TH><TH>${HtagTH_}艦砲系${H_tagTH}</TH><TH>${HtagTH_}対艦系${H_tagTH}</TH><TH>${HtagTH_}対空系${H_tagTH}</TH>
<TH>${HtagTH_}補給<br>能力${H_tagTH}</TH><TH>${HtagTH_}貿易<br>能力${H_tagTH}</TH><TH>${HtagTH_}海賊<br>能力${H_tagTH}</TH><TH>${HtagTH_}陸地<br>掘削<br>能力${H_tagTH}</TH>
<TH>${HtagTH_}目標<br>補正${H_tagTH}</TH><TH>${HtagTH_}体当<br>たり${H_tagTH}</TH><TH>${HtagTH_}命中<br>率UP${H_tagTH}</TH><TH>${HtagTH_}防波<br>能力${H_tagTH}</TH>
<TH>${HtagTH_}破壊力<br>ランダム<br>max(率)${H_tagTH}</TH><TH>${HtagTH_}絨毯<br>爆撃${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HnavyName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><span class='myFleetCell'><img src='${HimageDir}/$HnavyImage[$i]' class='myFleet'></span></TD><TD align='right'><img src='${HimageDir}/$HnavyImage[$i]'></TD><TH>$HnavyName[$i]</TH>
END

			my $submarineSurface = ($HnavySpecial[$i] & 0x4) ? $HsubmarineSurface[$i] . '%' : '';
			my @fireName = ([($HnavyFireName[$i][0] ne '' ? $HnavyFireName[$i][0] : '魚雷発射'),'−'], [($HnavyFireName[$i][1] ne '' ? $HnavyFireName[$i][1] : '艦砲射撃'),'−'], [($HnavyFireName[$i][2] ne '' ? $HnavyFireName[$i][2] : '対艦攻撃'),'−'], [($HnavyFireName[$i][3] ne '' ? $HnavyFireName[$i][3] : '対空射撃'),'−']);
			my($towardhex, $oilp, $supplyhex, $pirateshex, $firehexp, $bouhahex, $damagemaxp, $terrorhexnv);
			$towardhex = "<br>($HnavyTowardRange[$i]Hex)" if($HnavySpecial[$i] & 0x800);
			if($HnavySpecial[$i] & 0x8000) {
				$oilp = '<br>' . $Hoilp[$i] * 0.1 . '%';
				my $probecost = int($Hoilp[$i] * $HcomCost[$HcomDestroy]) . $HunitMoney;
				1 while $probecost =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$oilp .= "<br><span style='text-decoration: overline;'>" . $probecost . '</span>';
			}
			$supplyhex = "<br>($HnavySupplyRange[$i]Hex)" if($HnavySpecial[$i] & 0x10000);
			$pirateshex = "<br>($HpiratesHex[$i]Hex)" if($HnavySpecial[$i] & 0x40000);
			$firehexp = "<br>($Hfirehexp[$i]%)" if($HnavySpecial[$i] & 0x4000000);
			$bouhahex = "<br>($HbouhaHex[$i]Hex)" if($HnavySpecial[$i] & 0x8000000);
			$damagemaxp = "<br>$HdamageMax[$i]($Hdamagep[$i]%)" if($HnavySpecial[$i] & 0x10000000);
			$terrorhexnv = "<br>($HnavyTerrorHex[$i]Hex)" if($HnavySpecial[$i] & 0x20000000);
			$src .= <<"END";
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x1)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x2)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x4)]<BR>$submarineSurface</TD><TD align='center'>$ox[!(!($HnavySpecial[$i] & 0x8) && !($HnavySpecial[$i] & 0x80) && !($HnavyNoMove[$i]))]</TD>
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x10)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x20)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x40)]</TD><TD align='center'>$ox[!(!$HnavyCruiseTurn[$i] && !$HnavyNoMove[$i])]</TD>
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x100)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x200)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x400)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x800)]</TD>
<TD align='center'>$fireName[0][!($HnavySpecial[$i] & 0x1000)]</TD><TD align='center'>$fireName[1][!($HnavySpecial[$i] & 0x2000)]</TD><TD align='center'>$fireName[2][!($HnavySpecial[$i] & 0x4000)]</TD><TD align='center'>$fireName[3][!($HnavySpecial[$i] & 0x8000)]</TD>
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x10000)]$supplyhex</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x20000)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x40000)]$pirateshex</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x80000)]</TD>
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x1000000)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x2000000)]</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x4000000)]$firehexp</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x8000000)]$bouhahex</TD>
<TD align='center'>$ox[!($HnavySpecial[$i] & 0x10000000)]$damagemaxp</TD><TD align='center'>$ox[!($HnavySpecial[$i] & 0x20000000)]$terrorhexnv</TD>
</TR>
END
		}

		$src .= "</TABLE>";
		$src .= "　※「海底探査能力」は、移動のたびに調査費用がかかります。(維持費に計上されます)<BR>";
		$src .= "　※「体当たり」は、耐久力に関係なく相手もろとも沈没する能力です。";
		if($HnavySafetyZone == 2) {
			$src .= "ただし、自島や友好国の艦艇には無効です。<BR>";
		} elsif($HnavySafetyZone == 1) {
			$src .= "ただし、自島の艦艇だけは無効です。<BR>";
		} else {
			$src .= "たとえ、自島の艦艇であっても体当たりは有効です。<BR>";
		}
		if($HsuicideAbility) {
			$src .= "　　　旗艦・移動操縦をしなくても移動時に進行方向に艦艇があれば勝手に体当たりします。<BR>";
		} else {
			$src .= "　　　旗艦・移動操縦をしなければ体当たりしません。<BR>";
		}
		$src .= "　※「破壊力ランダム」は、率の割合で乱数が発生し、maxで設定された数値を最大値として破壊力が変化します。乱数が発生しなければ通常の破壊力です。<BR>";
		$src .= "　※「絨毯爆撃」は、初弾の着弾点の周囲(設定Hex)にまんべんなく着弾します。ただし，攻撃数がHexに足りない場合は虫喰い絨毯になります。<BR>";
	}

# 防衛施設・基地
#-------------------------

	my $dbMax = (!$HdBaseMax) ? '無制限' : $HdBaseMax . '基';
	my $durable;
	if($HdurableDef){
		$durable = "<B>最大$HdurableDefまでアップ</B>(自爆は数量「$HdefExplosion」を指定して追加建設)";
	} else {
		$durable = "<B>なし</B>(通常)";
	}
	my $defLevelUp = '';
	$defLevelUp = "※耐久力が<B>$HdefLevelUp以上</B>で強化防衛施設(防衛範囲周囲3Hex)になる"if($HdefLevelUp);
	$src .= <<"END";
<HR>
<a name='def'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 防衛施設</H3></a>
防衛施設の保有可能最大数　<B>$dbMax</B><BR>
防衛施設の耐久力設定？　$durable　$defLevelUp<BR>
防衛施設は、怪獣に踏まれた時自爆するか？　<B>$doStr[$HdBaseAuto]</B><BR>
防衛施設を、森に偽装するか？　<B>$doStr[$HdBaseHide]</B><BR>
自$AfterNameの攻撃は自$AfterNameの防衛圏(他$AfterNameの防衛圏でない地点)に着弾できるようにするか？
<BR>　艦艇攻撃：<B>$nodefStr[$HdBaseSelfNoDefenceNV]</B>　ミサイル攻撃：<B>$nodefStr[$HdBaseSelfNoDefenceMS]</B>　怪獣のミサイル攻撃：<B>$nodefStr[$HdBaseSelfNoDefenceMA]</B><BR>
END

# 基地・ミサイル
#-------------------------
	$src .= <<"END";
<HR>
<a name='base'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 基地・ミサイル</H3></a>
ミサイル基地を使うか？　<B>$useStr[$HuseBase]</B><BR>
海底基地を使うか？　<B>$useStr[$HuseSbase]</B><BR>
END

	if($HuseBase || $HuseSbase) {
		$src .= <<"END";
<BR>
基地の経験値の最大値　<B>$HmaxExpPoint</B><BR>
END

		$src .= "<TABLE><TR><TD class='M'>";
		$src .= "<TABLE><TR $HbgInfoCell><TH>ミサイル基地のレベル</TH>";
		foreach (1..$maxBaseLevel) {
			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
		}
		$src .= "</TR><TR $HbgInfoCell><TH>レベルUPに必要な経験値</TH><TD align='center'>0</TD>";
		foreach (@baseLevelUp) {
			$src .= "<TD align='center'>$_</TD>";
		}
		$src .= "</TR></TABLE>";
		$src .= "</TD><TD class='M'>";
		$src .= "<TABLE><TR $HbgInfoCell><TH>海底基地のレベル</TH>";
		foreach (1..$maxSBaseLevel) {
			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
		}
		$src .= "</TR><TR $HbgInfoCell><TH>レベルUPに必要な経験値</TH><TD align='center'>0</TD>";
		foreach (@sBaseLevelUp) {
			$src .= "<TD align='center'>$_</TD>";
		}
		$src .= "</TR></TABLE>";
		$src .= "</TD></TR></TABLE>";
		$src .= <<"END";
<BR>
STミサイルを使うか？　<B>$useStr[$HuseMissileST]</B><BR>
<BR>
射程内に怪獣・巨大怪獣がいなければ、ミサイルの発射を中止するか？　<B>$doStr[$HtargetMonster]</B><BR>
ミサイルで被弾した艦艇や地形が自$AfterNameの場合、無害にするか？　<B>$saftyStr[$HmissileSafetyZone]</B><BR>
　無害化が無効になる確率　<B>${HmissileSafetyInvalidp}%</B>(無害化機能が発動する場面で判定)<BR>
END

		$src .= <<"END";
<TABLE><TR $HbgInfoCell>
<TH rowspan='2'>${HtagTH_}ミサイル名称${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}費用${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}ターン<BR>消費${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}破壊力${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}誤差${H_tagTH}</TH>
<TH colspan='5'>${HtagTH_}属性${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}ＳＴ${H_tagTH}</TH><TH>${HtagTH_}陸破${H_tagTH}</TH><TH>${HtagTH_}絨毯<br>爆撃${H_tagTH}</TH>
<TH>${HtagTH_}硬化<br>無効${H_tagTH}</TH><TH>${HtagTH_}潜水<br>無効${H_tagTH}</TH>
</TR>
END
		foreach $i (0..$#HmissileName) {
			next if ($STcheck{$HcomMissile[$i]} && (!$HuseMissileST || $Htournament));
			$src .= <<"END";
<TR $HbgInfoCell><TH>$HmissileName[$i]</TH>
END
			my $mCost = (!$HmissileCost[$i]) ? "−" : "$HmissileCost[$i]$HunitMoney";
			1 while $mCost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my($terrorhexms);
			$terrorhexms = "<br>($HmissileTerrorHex[$i]Hex)" if($HmissileSpecial[$i] & 0x4);
			my $mdamage = $HmissileDamage[$i];
			$mdamage = 1 if($mdamage <= 0);
			$src .= <<"END";
<TD align='right'>$mCost</TD><TD align='right'>$anStr[$HmissileTurn[$i]]</TD><TD align='right'>$mdamage</TD><TD align='right'>$HmissileErr[$i]Hex</TD>
<TD align='center'>$ox[!($HmissileSpecial[$i] & 0x1)]</TD><TD align='center'>$ox[!($HmissileSpecial[$i] & 0x2)]</TD><TD align='center'>$ox[!($HmissileSpecial[$i] & 0x4)]$terrorhexms</TD>
<TD align='center'>$ox[!($HmissileSpecial[$i] & 0x10)]</TD><TD align='center'>$ox[!($HmissileSpecial[$i] & 0x20)]</TD>
</TR>
END
		}
		$src .= "</TABLE>";
		$src .= "　※「絨毯爆撃」は、初弾の着弾点の周囲(設定Hex)にまんべんなく着弾します。ただし，基地ごとの攻撃であるため，1つの基地での攻撃数がHexに足りない場合は虫喰い絨毯になります。<BR>";
	}
# 天候
#-------------------------

	$src .= <<"END";
<HR>
<a name='weather'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 天候</H3></a>
天候を使うか？　<B>$useStr[$HuseWeather]</B><BR>
END


	$src .= <<"END" if($HuseWeather);
<TABLE>
<TR $HbgInfoCell><TH colspan=4>${HtagTH_}気象要素${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>気温</TH><TD align='center'>-10℃ 〜 40℃</TD><TD>0℃以下になると収穫量が半減。</TD></TR>
<TR $HbgInfoCell><TH>気圧</TH><TD align='center'>900hPa 〜 1,100hPa</TD><TD>950hPa以下で台風発生確率が10倍。変化が激しい時に風速に影響。</TD></TR>
<TR $HbgInfoCell><TH>湿度</TH><TD align='center'>0% 〜 100%</TD><TD>地盤に影響を及ぼす。</TD></TR>
<TR $HbgInfoCell><TH>風速</TH><TD align='center'>0m/s 〜 50m/s</TD><TD>20m/s以上で台風の確率上昇。40m/s以上で津波の確率上昇。波力に影響。</TD></TR>
<TR $HbgInfoCell><TH>地盤</TH><TD align='center'>0 〜 100</TD><TD>90以上で地盤沈下の確率上昇。100で地盤沈下発生。(陸地面積が限界を超えていなければ発生しません！)</TD></TR>
<TR $HbgInfoCell><TH>波力</TH><TD align='center'>0 〜 100</TD><TD>90以上で津波の確率上昇。100で津波発生。</TD></TR>
</TABLE>
<TABLE>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=3>${HtagTH_}$HweatherName[0]${H_tagTH}</TH>
<TH rowspan=3>${HtagTH_}比率${H_tagTH}</TH>
<TH colspan=3>${HtagTH_}イベント${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}気温変化${H_tagTH}</TH>
<TH>${HtagTH_}気圧変化${H_tagTH}</TH>
<TH>${HtagTH_}湿度変化${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TD align='center'>±$HrKion</TD>
<TD align='center'>±$HrKiatu</TD>
<TD align='center'>±$HrSitudo</TD>
</TR>
END

	if($HuseWeather) {
		foreach $i (1..$#HweatherName) {
			my(@wt, $j, $k);
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HweatherImage[$i]'></TD>
<TH>$HweatherName[$i]</TH>
<TD align='center'>$HweatherRatio[$i]</TD>
END
			foreach $j (0..2) {
				$wt[$j] = ($HweatherSpecial[$i] & 0xF) - 8;
				$wt[$j] = ($wt[$j] == -8 || !$wt[$j]) ? '−' : $wt[$j]*$HweatherSpecialRatio[$j];
				$wt[$j] = ($wt[$j] > 0) ? "<FONT color=blue>+$wt[$j]</FONT>" : "<FONT color=red>$wt[$j]</FONT>";
				$src .= "<TD align='right'>$wt[$j]</TD>";
				$HweatherSpecial[$i] >>= 4;
			}
			$src .= "</TR>";
		}
		$src .= "</TABLE><BR>";
	}

# 災害
#-------------------------

	$HdisEarthquake *= 0.1; # 地震
	$HdisTsunami    *= 0.1; # 津波
	$HdisTyphoon    *= 0.1; # 台風
	$HdisMeteo      *= 0.1; # 隕石
	$HdisHugeMeteo  *= 0.1; # 巨大隕石
	$HdisEruption   *= 0.1; # 噴火
	$HdisFire       *= 0.1; # 火災
	$HdisMaizo      *= 0.1; # 埋蔵金
	$HdisFalldown   *= 0.1; # 地盤沈下
	$HdisMonster    *= 0.01;# 怪獣
	$HdisMonsterBF  *= 0.01;# 怪獣(Battle Field)
	$HdisHuge       *= 0.01;# 巨大怪獣
	$HdisHugeBF     *= 0.01;# 巨大怪獣(Battle Field)
	$HdisMonsterBF = $HdisMonster*2 if(!$HdisMonsterBF);
	$HdisHugeBF    = $HdisHuge*2 if(!$HdisHugeBF);

	$src .= <<"END";
<HR>
<a name='disaster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 災害</H3></a>
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}地震${H_tagTH}</TH><TH rowspan=2>${HtagTH_}津波${H_tagTH}</TH><TH rowspan=2>${HtagTH_}台風${H_tagTH}</TH><TH rowspan=2>${HtagTH_}隕石${H_tagTH}</TH><TH rowspan=2>${HtagTH_}巨大隕石${H_tagTH}</TH><TH rowspan=2>${HtagTH_}噴火${H_tagTH}</TH><TH rowspan=2>${HtagTH_}火災${H_tagTH}</TH><TH rowspan=2>${HtagTH_}埋蔵金${H_tagTH}</TH><TH colspan=2>${HtagTH_}地盤沈下${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}安全限界の広さ${H_tagTH}</TH><TH>${HtagTH_}超えた場合の確率${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'>${HdisEarthquake}%</TD><TD align='right'>${HdisTsunami}%</TD><TD align='right'>${HdisTyphoon}%</TD><TD align='right'>${HdisMeteo}%</TD><TD align='right'>${HdisHugeMeteo}%</TD><TD align='right'>${HdisEruption}%</TD><TD align='right'>${HdisFire}%</TD><TD align='right'>${HdisMaizo}%</TD><TD align='right'>$HdisFallBorder$HunitArea(${HdisFallBorder}Hex)</TD><TD align='right'>${HdisFalldown}%</TD></TR>
</TABLE>
津波が海軍に与えるダメージの最大値　<B>$HdisTsunamiDmax</B><BR>
END

	# 島の座標数
	$HpointNumber = $HislandSizeX * $HislandSizeY;

	$src .= <<"END";
海の面積フラグ　<B>$HdisTsunamiFsea</B><BR>
　※海の面積が、これを下回ると津波発生確率が10倍になる。
END
	if($HpointNumber - 8*8 - $HdisTsunamiFsea > 0) {
		my %bai;
		my $pn = $HpointNumber - 8*8;
		foreach ($HdisTsunamiFsea..$pn) {
				my $flag = ($HpointNumber - 8*8 - $_)/($HpointNumber - 8*8 - $HdisTsunamiFsea);
			$flag = 1 + int($flag * 4);
			$bai{$flag} = $_;
		}
		$src .= "　(　注！標準的には，";
		foreach (sort { $b <=> $a } keys %bai) {
			next if($_ == 1);
			$src .= "$bai{$_}";
			$src .= "以下" if($bai{$_} != $HdisTsunamiFsea);
			$src .= "で$_倍　";
		}
		$src .= ')';
	}
	$src .= '<BR><BR>';

# 怪獣
#-------------------------
	$src .= "<HR><a name='monster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 怪獣</H3></a>";

	$src .= <<"END";
<BR>
単位面積あたりの怪獣出現率　<B>${HdisMonster}%</B>　（バトルフィールド：<B>${HdisMonsterBF}%</B>）<BR>
怪獣派遣を使うか？　<B>$useStr[$HuseSendMonster]</B><BR>
ST怪獣派遣を使うか？　<B>$useStr[$HuseSendMonsterST]</B><BR>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}怪獣${H_tagTH}</TH><TH rowspan=2>${HtagTH_}怪獣<br>出現人口<br>(比率)${H_tagTH}</TH><TH rowspan=2>${HtagTH_}派遣費用<BR>ST費用${H_tagTH}</TH><TH rowspan=2>${HtagTH_}派遣<BR>番号${H_tagTH}</TH><TH colspan=2>${HtagTH_}体力${H_tagTH}</TH><TH rowspan=2>${HtagTH_}経験値${H_tagTH}</TH><TH rowspan=2>${HtagTH_}残骸の値段${H_tagTH}</TH><TH colspan=8>${HtagTH_}能力${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH>
<TH>${HtagTH_}足が<br>速い${H_tagTH}</TH><TH>${HtagTH_}足が<br>とても<br>速い${H_tagTH}</TH><TH>${HtagTH_}ラン<br>ダム<br>硬化${H_tagTH}</TH>
<TH>${HtagTH_}先行<br>移動${H_tagTH}</TH><TH>${HtagTH_}蹂躙<br>移動${H_tagTH}</TH><TH>${HtagTH_}移動<br>操縦${H_tagTH}</TH>
<TH>${HtagTH_}攻撃能力${H_tagTH}</TH><TH>${HtagTH_}絨毯<br>爆撃${H_tagTH}</TH>
</TR>
END

	foreach $i (0..$#HmonsterName) {
		my $maxHP = $HmonsterBHP[$i] + $HmonsterDHP[$i] - 1;
		$maxHP++ if(!$HmonsterDHP[$i]);
		my $levelpop = ($HdisMonsBorder[$i]) ? $HdisMonsBorder[$i] . $HunitPop : '−';
		1 while $levelpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $levelratio = $HdisMonsRatio[$i];
		my $monsterValue = $HmonsterValue[$i] . $HunitMoney;
		1 while $monsterValue =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($mcost, $mcostst, $mno) = ('−', '−', '−');
		if($i <= $HsendMonsterNumber) {
			$mcost = $HmonsterCost[$i] . $HunitMoney if($HuseSendMonster);
			1 while $mcost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mcostst = $HmonsterCostST[$i] . $HunitMoney if($HuseSendMonsterST);
			1 while $mcostst =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mno = $i;
		}
		my @attackName = (($HmonsterFireName[$i] ne '' ? $HmonsterFireName[$i] : 'ミサイル攻撃'),'−');
		my($terrorhexma);
		$terrorhexma = "<br>($HmonsterTerrorHex[$i]Hex)" if($HmonsterSpecial[$i] & 0x200);
		$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImage[$i]'></TD><TH>$HmonsterName[$i]</TH><TD align='right'>$levelpop<BR>(${levelratio})</TD><TD align='right'>$mcost<BR>$mcostst</TD><TD align='center'>$i</TD><TD align='right'>$HmonsterBHP[$i]</TD><TD align='right'>$maxHP</TD><TD align='right'>$HmonsterExp[$i]</TD><TD align='right'>$monsterValue</TD>
<TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x1)]</TD><TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x2)]</TD><TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x4)]</TD>
<TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x10)]</TD><TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x20)]</TD><TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x80)]</TD>
<TD align='center'>$attackName[!($HmonsterSpecial[$i] & 0x100)]</TD><TD align='center'>$ox[!($HmonsterSpecial[$i] & 0x200)]$terrorhexma</TD>
</TR>
END
	}
	$src .= "</TABLE>";
	$src .= "　※「絨毯爆撃」は、初弾の着弾点の周囲(設定Hex)にまんべんなく着弾します。ただし，攻撃数がHexに足りない場合は虫喰い絨毯になります。<BR>";
	$src .= <<"END";
<BR>
攻撃した怪獣自身が射程範囲にある場合、自爆(被弾)することもあるようにするか？　<B>$anStr[$HmonsterSelfAttack]</B><BR>
「攻撃能力」で被弾した艦艇や地形が自$AfterNameの場合、無害にするか？　<B>$saftyStr[$HmissileSafetyZone]</B><BR>
　無害化が無効になる確率　<B>${HmissileSafetyInvalidp}%</B>(無害化機能が発動する場面で判定)<BR>
END

# 巨大怪獣
#-------------------------

	$src .= <<"END";
<HR>
<a name='hmonster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 巨大怪獣</H3></a>
巨大怪獣が出現するか？　<B>$doStr[$HhugeMonsterAppear]</B><BR>
END

	if($HhugeMonsterAppear) {

		$src .= <<"END";
単位面積あたりの巨大怪獣出現率　<B>${HdisHuge}%</B>　（バトルフィールド：<B>${HdisHugeBF}%</B>）<BR>
体の再生をランダムに行う能力での再生確率　<B>${HpRebody}%</B><BR>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}巨大怪獣${H_tagTH}</TH><TH rowspan=2>${HtagTH_}巨大怪獣<br>出現人口<br>(比率)${H_tagTH}</TH><TH rowspan=2>${HtagTH_}派遣費用<BR>ST費用${H_tagTH}</TH><TH rowspan=2>${HtagTH_}派遣<BR>番号${H_tagTH}</TH><TH colspan=2>${HtagTH_}体力${H_tagTH}</TH><TH rowspan=2>${HtagTH_}経験値${H_tagTH}</TH><TH rowspan=2>${HtagTH_}残骸の値段${H_tagTH}</TH><TH colspan=10>${HtagTH_}能力${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH>
<TH>${HtagTH_}足が<br>速い${H_tagTH}</TH><TH>${HtagTH_}足が<br>とても<br>速い${H_tagTH}</TH><TH>${HtagTH_}ラン<br>ダム<br>硬化${H_tagTH}</TH>
<TH>${HtagTH_}先行<br>移動${H_tagTH}</TH><TH>${HtagTH_}蹂躙<br>移動${H_tagTH}</TH><TH>${HtagTH_}移動<br>操縦${H_tagTH}</TH>
<TH>${HtagTH_}攻撃能力${H_tagTH}</TH><TH>${HtagTH_}絨毯<br>爆撃${H_tagTH}</TH>
<TH>${HtagTH_}コア<br>防衛${H_tagTH}</TH><TH>${HtagTH_}ラン<br>ダム<br>再生${H_tagTH}</TH></TR>
END

		foreach $i (0..$#HhugeMonsterName) {
			my $maxHP = $HhugeMonsterBHP[$i] + $HhugeMonsterDHP[$i] - 1;
			$maxHP++ if(!$HhugeMonsterDHP[$i]);
			my $levelpop = ($HdisHugeBorder[$i]) ? $HdisHugeBorder[$i] . $HunitPop : '−';
			1 while $levelpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $levelratio = $HdisHugeRatio[$i];
			my $hugeMonsterValue = $HhugeMonsterValue[$i] . $HunitMoney;
			1 while $hugeMonsterValue =~ s/(.*\d)(\d\d\d)/$1,$2/;

			$src .= "<TR $HbgInfoCell><TD align='right'>";
			my($j, @monImage);
			foreach $j (0..6) {
				$monImage[$j] = ($HhugeMonsterImage3[$i][$j] eq '') ? "${HimageDir}/$HlandImage[$HlandSea][0]" : "${HimageDir}/$HhugeMonsterImage3[$i][$j]";
			}
			my($mcost, $mcostst, $mno) = ('−', '−', '−');
			if($i <= $HsendHugeMonsterNumber) {
				$mcost = $HhugeMonsterCost[$i] . $HunitMoney if($HuseSendMonster);
				1 while $mcost =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mcostst = $HhugeMonsterCostST[$i] . $HunitMoney if($HuseSendMonsterST);
				1 while $mcostst =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mno = $i + 50;
			}
			my @attackName = (($HhugeMonsterFireName[$i] ne '' ? $HhugeMonsterFireName[$i] : 'ミサイル攻撃'),'−');
			my($terrorhexma);
			$terrorhexma = "<br>($HhugeMonsterTerrorHex[$i]Hex)" if($HhugeMonsterSpecial[$i] & 0x200);
			my($space);
			$space = "<img src='${HimageDir}/space.gif'>";
			$src .= <<"END";
$space<img src='$monImage[6]'><img src='$monImage[1]'>$space<br>
<img src='$monImage[5]'><img src='$monImage[0]'><img src='$monImage[2]'><br>
$space<img src='$monImage[4]'><img src='$monImage[3]'>$space
</TD><TH>$HhugeMonsterName[$i]</TH><TD align='right'>$levelpop<BR>(${levelratio})</TD><TD align='right'>$mcost<BR>$mcostst</TD><TD align='center'>$mno</TD><TD align='right'>$HhugeMonsterBHP[$i]</TD><TD align='right'>$maxHP</TD><TD align='right'>$HhugeMonsterExp[$i]</TD><TD align='right'>$hugeMonsterValue</TD>
<TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x1)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x2)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x4)]</TD>
<TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x10)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x20)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x80)]</TD>
<TD align='center'>$attackName[!($HhugeMonsterSpecial[$i] & 0x100)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x200)]$terrorhexma</TD>
<TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x10000)]</TD><TD align='center'>$ox[!($HhugeMonsterSpecial[$i] & 0x20000)]</TD>
</TR>
END
		}
		$src .= <<"END";
</TABLE><BR>
END
	}

# アイテム
#-------------------------

	$src .= <<"END";
<HR>
<a name='item'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> アイテム</H3></a>
アイテムを使うか？　<B>$useStr[$HuseItem]</B><BR>
END

	if($HuseItem) {
		my $itemGet   = ($HitemGetDenominator) ? "(総獲得経験値)<B>/$HitemGetDenominator</B>" : '判定しない';
		my $itemGet2  = ($HitemGetDenominator2) ? "(総獲得経験値)<B>/$HitemGetDenominator2</B>" : '判定しない';
		my $itemGet3  = ($HitemGetDenominator3) ? "(総獲得経験値)<B>/$HitemGetDenominator3</B>" : '判定しない';
		my $itemSeize = ($HitemSeizeDenominator) ? "(艦艇経験値)<B>/$HitemSeizeDenominator</B>" : '判定しない';
		my $itemGive  = (!$HitemGivePerTurn) ? '' : ($HitemGivePerTurn == 1) ? "　※ターン杯ごとに<B>上位の$AfterNameから順に</B>ひとつずつ「キーアイテム」が与えられます。" : "　※ターン杯ごとに<B>下位の$AfterNameから順に</B>ひとつずつ「キーアイテム」が与えられます。";
		$itemGive    .= "ただし、海軍(艦艇or軍港)を保有しない$AfterNameはスキップします。<BR>";
		my $itemBF    = ($HitemInvalid) ? "　※バトルフィールドでは「攻撃回数２倍」「射程を広げる」「全$AfterName補給可能」「命中率UP」「破壊力２倍」の能力が無効になります。" : '';
		my $compStr = (!$HallyItemComplete) ? "１つの$AfterName" : (!$HarmisticeTurn) ? "１つの同盟" : "１つの陣営";

		$src .= <<"END";
　※<B>$compStr</B>がすべての「キーアイテム」を獲得するとゲームが終了します。<BR>
$itemGive
<BR>
アイテム獲得判定確率<BR>
　巨大怪獣退治の時、$itemGet<BR>
　怪獣退治の時、$itemGet2<BR>
　残骸売却の時、$itemGet3<BR><BR>
アイテム奪取判定確率<BR>
　アイテム保有$AfterNameの艦艇撃沈の時、$itemSeize<BR>
　　※海軍を消滅させた際には、すべてのアイテムが最後の１艦(１港)を破壊した$AfterNameへ移ります。<br>
　　※また、理由の如何に関わらず海軍を消失した島は、すべてのアイテム(および総獲得経験値)を失います。<br>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}$HitemName[0]${H_tagTH}</TH>
<TH colspan=25>${HtagTH_}能力${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}キー<br>アイ<br>テム${H_tagTH}</TH>
<TH>${HtagTH_}全$AfterName<br>補給<br>可能${H_tagTH}</TH>
<TH>${HtagTH_}地形<br>遮蔽<br>無効${H_tagTH}</TH>
<TH>${HtagTH_}保有<br>艦艇<br>＋α${H_tagTH}</TH>
<TH>${HtagTH_}射程<br>拡大<br>Hex${H_tagTH}</TH>
<TH>${HtagTH_}命中<br>率UP<br>確率${H_tagTH}</TH>
<TH>${HtagTH_}コマ<br>ンド<br>回数<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}食料<br>max<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}資金<br>max<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}収穫<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}収入<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}攻撃<br>回数<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}破壊<br>力<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}維持<br>食料<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}維持<br>金<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}食料<br>消費<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}コマ<br>ンド<br>コスト<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}地震<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}台風<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}隕石<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}巨大<br>隕石<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}噴火<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}火災<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}津波<br>倍率${H_tagTH}</TH>
<TH>${HtagTH_}破壊<br>力<br>＋${H_tagTH}</TH>
</TR>
END

		foreach $i (1..$#HitemName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HitemImage[$i]'></TD>
<TH>$HitemName[$i]</TH>
END
			foreach (0..2) {
				$src .= "<TD align='center'>$ox[!$HitemSpecial[$i][$_]]</TD>";
			}
			$src .= ($HitemSpecial[$i][3] > 0) ? "<TD align='center'>+$HitemSpecial[$i][3]</TD>" : ($HitemSpecial[$i][3] < 0) ? "<TD align='center'>$HitemSpecial[$i][3]</TD>" : "<TD align='center'>−</TD>";
			$src .= ($HitemSpecial[$i][4] != 0) ? "<TD align='center'>$HitemSpecial[$i][4]Hex</TD>" : "<TD align='center'>−</TD>";
			$src .= ($HitemSpecial[$i][5] != 0) ? "<TD align='center'>$HitemSpecial[$i][5]%</TD>" : "<TD align='center'>−</TD>";
			foreach (6..12) {
				$src .= ($HitemSpecial[$i][$_] > 1) ? "<TD align='center'><FONT color=blue>x$HitemSpecial[$i][$_]</FONT></TD>" : ($HitemSpecial[$i][$_] < 1) ? "<TD align='center'><FONT color=red>x$HitemSpecial[$i][$_]</FONT></TD>" : "<TD align='center'>−</TD>";
			}
			foreach (13..23) {
				$src .= ($HitemSpecial[$i][$_] > 1) ? "<TD align='center'><FONT color=red>x$HitemSpecial[$i][$_]</FONT></TD>" : ($HitemSpecial[$i][$_] < 1) ? "<TD align='center'><FONT color=blue>x$HitemSpecial[$i][$_]</FONT></TD>" : "<TD align='center'>−</TD>";
			}
			$src .= ($HitemSpecial[$i][24] > 0) ? "<TD align='center'>+$HitemSpecial[$i][24]</TD>" : ($HitemSpecial[$i][24] < 0) ? "<TD align='center'>$HitemSpecial[$i][24]</TD>" : "<TD align='center'>−</TD>";
		}
		$src .= <<"END";
</TABLE>
$itemBF<BR>
END
	}

# 記念碑
#-------------------------

	$src .= <<"END";
<HR>
<a name='monument'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> 記念碑</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan=2>${HtagTH_}記念碑${H_tagTH}</TH></TR>
END

	foreach $i (0..$#HmonumentName) {
		$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonumentImage[$i]'></TD><TH>$HmonumentName[$i]</TH></TR>
END
	}
	$src .= "</TABLE>";
#	$src .= "記念碑発射を使うか？　<B>$useStr[$HuseBigMissile]</B><BR>";
	$src .= "記念碑発射を使うか？　<B>内緒</B><BR>";

# ターン杯・各賞
#-------------------------

	my $prize = 0;
	my %prizeKind = (
		'pop' => '人口',
		'gain' => '総獲得経験値',
		'money' => '資金',
		'food' => '食料',
		'area' => '面積',
		'farm' => '農場規模',
		'factory' => '工場規模',
		'mountain' => '採掘場規模',
		'monsterkill' => '怪獣退治数',
		'itemNumber' => "$HitemName[0]獲得数",
		'point' => "$HpointName",
		'achive' => "救出した難民(1ターン)",
		'damage' => "消失した人口(1ターン)",
	);
	my %prizeAfter = (
		'pop' => "$HunitPop",
		'gain' => '',
		'money' => "$HunitMoney",
		'food' => "$HunitFood",
		'area' => "$HunitArea",
		'farm' => "0$HunitPop",
		'factory' => "0$HunitPop",
		'mountain' => "0$HunitPop",
		'monsterkill' => "$HunitMonster",
		'itemNumber' => '',
		'point' => "$HpointAfter",
		'achive' => "$HunitPop",
		'damage' => "$HunitPop",
	);
	my @extKind  = ('優勝回数', '貢献度', '破壊した防衛施設の数', '破壊したミサイル基地の数', '救出した難民の合計人口', '受けた弾数', '発射した弾数', '防衛施設で弾いた弾数', '派遣した艦艇の数', '派遣された艦艇の数', '破壊した艦艇の数');
	my @extAfter = ('回', '', '基', '基', "$HunitPop", '発', '発', '発', '艦', '艦', '艦');
	foreach $i (0..$#Hprize) {
		$prize += $Hprize[$i]->{'money'};
	}
	my $str = ($prize) ? "<TH>${HtagTH_}賞金額${H_tagTH}</TH>" : '';
	$src .= <<"END";
<HR>
<a name='prize'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> ターン杯・各賞</H3></a>
ターン杯を何ターン毎に出すか　<B>${HturnPrizeUnit}ターン</B><BR>

<TABLE>
<TR $HbgInfoCell><TH colspan=2>${HtagTH_}賞${H_tagTH}</TH><TH colspan=2>${HtagTH_}受賞条件${H_tagTH}</TH>$str</TR>
END

	foreach $i (0..$#Hprize) {
		my($req1, $req2);
		if($Hprize[$i]->{'kind'} eq 'ext') {
			$req1 = $extKind[$Hprize[$i]->{'ptr'}];
			my $threshold = $Hprize[$i]->{'threshold'};
			$threshold /= 10 if($Hprize[$i]->{'ptr'} == 1);
			$req2 = $threshold . $extAfter[$Hprize[$i]->{'ptr'}];
			1 while $req2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$req2 .= "以上";
		} else {
			$req1 = ($i) ? $prizeKind{$Hprize[$i]->{'kind'}} : "ターン杯判定時(${HturnPrizeUnit}ターンごと)";
			if($i) {
				$req2 = $Hprize[$i]->{'threshold'} . $prizeAfter{$Hprize[$i]->{'kind'}};
				1 while $req2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$req2 .= "以上";
			} else {
				if($Hprize[$i]->{'kind'} == 1) {
					$req2 = '島ランク第１位';
				} else {
					$req2 = "島ランク第$Hprize[$i]->{'kind'}位以上";
				}
			}
		}
		my $prizemoney = "$Hprize[$i]->{'money'}$HunitMoney";
		1 while $prizemoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$str = ($prize) ? "<TD align='right'>$prizemoney</TD>" : '';
		$src .= <<"END";
<TR $HbgInfoCell><TD align='center'><img src='${HimageDir}/prize${i}.gif'></TD><TH>$Hprize[$i]->{'name'}</TH><TD>$req1</TD><TD align='right'>$req2</TD>$str</TR>
END
	}
	$src .= "</TABLE>";

# コマンド一覧
#-------------------------

	$col = 1;
	$src .= <<"END";
<HR>
<a name='command'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>▲</small></a> コマンド一覧</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan=$col>${HtagTH_}コマンド一覧${H_tagTH}　　　${turnStr[1]}■${H_tagComName}ターンを消費する　${turnStr[0]}■${H_tagComName}ターンを消費しない</TH></TR>
END

	my %comCheck;
	foreach (@HcomList) {
		$comCheck{$_} = 1;
	}
	my $count = 0;
	foreach $com (@HcommandDivido) {
		$count++;
		my($category, $start, $end) = split(/,/, $com);
		$src .= "<TR>" if($count%$col == 1);
		$src .= <<"END";
<TD valign=top class='M'>
<TABLE width=100%>
<TR $HbgInfoCell><TH colspan=4>${HtagTH_}${category}系${H_tagTH}</TH></TR>
END
		foreach ($start..$end) {
			next if(!$comCheck{$_});
			next if($HmaxComNavyLevel && ($HcomNavy[0] + $HcomNavyNumber[$#HcomNavyNumber] < $_) && ($_ <= $HcomNavy[$#HnavyName]));
			next if($HcomName[$_] eq '');
			my $cost = $HcomCost[$_];
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
			1 while $cost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $turn = $HcomTurn[$_];
			$src .= <<"END";
<TR $HbgInfoCell>
<TH>${turnStr[($turn > 0)]}$HcomName[$_]${H_tagComName}</TH><TD align='right'>$cost</TD>
<TD align='left' width=100%>$HcomMsgs[$_]</TD>
</TR>
END
		}
		$src .= "</TABLE></TD>";
		$src .= "</TR>" if($count%$col == 0);
	}
	$src .= "</TR>" if($count%$col != 0);
	if($HusePrepare3 && $precheap2 != 10) {
		my $discount = 10 - $precheap2;
		$src .= "</TR><TR><TD  class='M' colspan=3>※${turnStr[($HcomTurn[$HcomPrepare3] > 0)]}$HcomName[$HcomPrepare3]${H_tagComName}は、<B>$precheap個め</B>の荒地から<B>「$discount割引」</B>になります。</TD>";
	}
	$src .= <<"END";
</TR></TABLE>
END

	$src .= <<"END" if($mode);
<HR>
<DIV ID='LinkFoot'>
$Hfooter
<DIV align="right">
<HR>
<B>海戦 JS.$versionInfo(based on ver1.3)</B> patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/'>neo_otacky</a>
</DIV></DIV></DIV>
</BODY></HTML>
END

#	1 while $src =~ s/(.*\d)(\d\d\d)/$1,$2/;
	if($mode) {
		open(OUT,">${HefileDir}/setup.html");
#		print OUT jcode::sjis($src);
		print OUT $src;
		close(OUT);
		chmod(0666, "${HefileDir}/setup.html");

		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=${efileDir}/setup.html\">");
	} else {
		out("$src");
	}
}

1;
