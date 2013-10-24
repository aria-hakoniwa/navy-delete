#----------------------------------------------------------------------
# Ȣ����� ���� JS ver7.xx
# �Ƽ�����⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# ͧ�����������
#----------------------------------------------------------------------
sub amityInfo() {
	# ����
	unlock();
	my($title) = '';
	$title = 'ͧ����' if($HuseAmity);
	if($HuseDeWar) {
		$title .= '��' if($HuseAmity);
		$title .= '�����';
	}

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='campInfo'>
<H1>$title ����</H1>
<span class='number'>��</span>��ͧ��(���)��
<span class='number'>��</span>��ͧ����
${HtagDisaster_}��${H_tagDisaster}������(�����۹�)��
${HtagDisaster_}x${H_tagDisaster}������(�������۹�)��
�ݡ���Ω
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
	my $aStr = ($HarmisticeTurn) ? '�ر�' : 'Ʊ��';
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
				out("<TD align='center'>��</TD>\n");
			} elsif($amityFlag{$aId}) {
				if($tAmityFlag{$id}) {
					out("<TD align='center'><span class='number'>��</span></TD>\n");
				} else {
					out("<TD align='center'><span class='number'>��</span></TD>\n");
				}
			} elsif($warFlag{"$id,$aId"}) {
				out("<TD align='center'>${HtagDisaster_}��${H_tagDisaster}</TD>\n");
			} elsif($warFlag{"$aId,$id"}) {
				out("<TD align='center'>${HtagDisaster_}x${H_tagDisaster}</TD>\n");
			} else {
				out("<TD align='center'>��</TD>\n");
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
				$allyName =~ s/�ھ��ԡ���//g;
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
# �����ƥ��������
#----------------------------------------------------------------------
sub ItemInfo() {
	# ����
	unlock();

	out(<<"END");
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='islandInfo'>
<H1>${HitemName[0]}��������</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell colspan='2'>${HtagTH_}${HitemName[0]}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ͭ$AfterName̾${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������и���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ǽ��${H_tagTH}�����ϥ��������ƥ�</TH>
</TR>
END

	my($island, $name, $navyComLevel, $totalExp);
	my @sptext  = ('<span class=check>[��]</span>', '<span class=check>[��������]</span>', '<span class=check>[�Ϸ�����̵��]</span>', '<span class=check>[��ͭ����', '<span class=check>[����UP ', '<span class=check>[̿��ΨUP ', '<span class=check>[���ޥ�ɲ�� x',
					'<span class=check>[����Max x', '<span class=check>[���Max x', '<span class=check>[���� x', '<span class=check>[���� x', '<span class=check>[������ x', '<span class=check>[�˲��� x', '<span class=check>[�ݻ����� x', '<span class=check>[�ݻ���� x', '<span class=check>[�������� x', '<span class=check>[���ޥ�ɥ����� x',
					'<span class=check>[�Ͽ� x', '<span class=check>[���� x', '<span class=check>[��� x', '<span class=check>[������� x', '<span class=check>[ʮ�� x', '<span class=check>[�к� x', '<span class=check>[���� x',
					'<span class=check>[�˲��� '
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
<TD $HbgNameCell align=left><DIV align='center'>��</DIV></TD>
<TD $HbgInfoCell align=right>��</TD>
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
					$name .= "${HtagDisaster_}��${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
					if($island->{'predelete'}) {
						my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
						$name = "${HtagDisaster_}�ڴ����ͤ��������$rest${H_tagDisaster}<BR>" . $name;
					}
					$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\">${name}</A>";
					$navyComLevel = gainToLevel($island->{'gain'});
					$totalExp = $island->{'gain'};
					$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
				} else {
					$name = "<DIV align='center'>��</DIV>";
					$totalExp = '��';
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
# ������ͭ������
#----------------------------------------------------------------------
sub fleetInfo {
	# ����
	unlock();
	my($col, $row);
	if(!$HinfoMode) {
		$col = 2; $row = (!$HnavySafetyZone || $HnavySafetyInvalidp) ? 3 : 2;
	} else {
		$col = 1; $row = 1;
	}
	my $title = ('���ǡ���', '��ͭ��', '������', '������')[$HinfoMode];
	my $rowstr = ($HinfoMode < 2) ? ' rowspan=2' : '';
	out(<<"END");
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='islandInfo'>
<H1>������ͭ������</H1>
END
	out(qq|[<A href="$HthisFile?Fleet=0">���ǡ���</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=1">��ͭ��</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=2">������</A>] |);
	out(qq|[<A href="$HthisFile?Fleet=3">������</A>] |) if(!$HnavySafetyZone || $HnavySafetyInvalidp);
	out(<<"END");
<TABLE BORDER>
<TR>
<TH colspan=$col>$title</TH>
END
	foreach (0..$#HnavyName) {
		out("<TD class='T'>${HtagTH_}$HnavyName[$_]${H_tagTH}<BR><img src=\"$HnavyImage[$_]\"></TD>");
	}
	out("<TD class='T'$rowstr>${HtagTH_}���${H_tagTH}</TD>");
	out("<TD class='T'$rowstr>${HtagTH_}��ͭ����<BR>�ݻ���${H_tagTH}</TD>");
	out("<TD class='T'$rowstr>${HtagTH_}��ͭ����<BR>�ݻ�����${H_tagTH}</TD>");
	out("</TR>");
	if($HinfoMode < 2) {
		out("<TR><TH colspan=$col>��ͭ��ǽ��</TH>");
		foreach (0..$#HnavyName) {
			if($HnavyKindMax[$_]) {
				out("<TH>$HnavyKindMax[$_]</TH>");
			} else {
				out("<TH>̵����</TH>");
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
			$island->{$kind} = 0; # ��ͭ���ν����
			$kind = "sinkkind$_";
			$island->{$kind} = 0; # �������ν����
			$island->{$kind} += $island->{'sink'}[$_] + $island->{'sinkself'}[$_]; # ������
			$island->{'totalsink'} += $island->{$kind};
			$kind = "sinkself$_";
			$island->{$kind} = 0; # �������ν����
			$island->{$kind} += $island->{'sinkself'}[$_]; # ������
			$island->{'totalsinkself'} += $island->{$kind};
		}
		$fkind = $island->{'fkind'};
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack(hex($_));
			$kind = "navykind${nKind}";
			$island->{$kind}++; # ��ͭ��
			$island->{'upkeepMoney'} += $HnavyMoney[$nKind]; # �ݻ���
			$island->{'upkeepFood'} += $HnavyFood[$nKind]; # �ݻ�����
			next if ($HnavySpecial[$nKind] & 0x8); # �����Ϲ�פ�����ʤ�
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
			$money = "<span class='Money'>����" . - $island->{'upkeepMoney'} . "${HunitMoney}";
		} elsif($island->{'upkeepMoney'} == 0) {
			$money = '��';
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
			$food = "<span class='Food'>����" . - $island->{'upkeepFood'} . "${HunitFood}";
		} elsif($island->{'upkeepFood'} == 0) {
			$food = '��';
		} else {
			$food = $island->{'upkeepFood'} . "${HunitFood}";
		}
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		if($id == $ids{'upkeepFood'}) {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>${HtagTH_}$food${H_tagTH}</TD>";
		} else {
			$upkeepInfo .= "<TD $HbgInfoCell rowspan=$row align=right>$food</TD>";
		}

		out("<TH $HbgTitleCell>${HtagTH_}��ͭ��${H_tagTH}</TH>\n") if(!$HinfoMode);
		if(!$HinfoMode || $HinfoMode == 1) {
			foreach (0..$#HnavyName) {
				$kind = "navykind$_";
				$kindNavy = $island->{$kind}; # ��ͭ��
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalnavy'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalnavy'}��${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalnavy'}��</TD>");
			}
			out("$upkeepInfo");
			out("\n</TR><TR>\n") if(!$HinfoMode);
		}

		out("<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>\n") if(!$HinfoMode);;
		if(!$HinfoMode || $HinfoMode == 2) {
			foreach (0..$#HnavyName) {
				$kind = "sinkkind$_";
				$kindNavy = $island->{$kind}; # ������
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalsink'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalsink'}��${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalsink'}��</TD>");
			}
			out("$upkeepInfo") if($HinfoMode == 2);
			out("\n</TR><TR>\n") if(!$HinfoMode);
		}

		if((!$HnavySafetyZone || $HnavySafetyInvalidp) && (!$HinfoMode || $HinfoMode == 3)) {
			out("<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>\n") if(!$HinfoMode);
			foreach (0..$#HnavyName) {
				$kind = "sinkself$_";
				$kindNavy = $island->{$kind}; # ������
				$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
				if($id == $ids{$kind}) {
					out("<TD $HbgInfoCell align=right>${HtagTH_}$kindNavy${H_tagTH}</TD>");
				} else {
					out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
				}
			}
			if($id == $ids{'totalsinkself'}) {
				out("<TD $HbgInfoCell align=right>${HtagTH_}$island->{'totalsinkself'}��${H_tagTH}</TD>");
			} else {
				out("<TD $HbgInfoCell align=right>$island->{'totalsinkself'}��</TD>");
			}
			out("$upkeepInfo") if($HinfoMode == 3);
		}
	}
	out(<<END);
</TR></TABLE></DIV>
END

}

#------------------------------------------------
# �ȡ��ʥ��ȥ⡼��
#------------------------------------------------
# ���ﹹ������
sub TimeTableMain {
	my $tournament = "";
	my $sec = ($HyosenTime % 60);
	$sec = ($sec ? "$sec��" : '');
	my $min = ($HyosenTime % 3600);
	$min = ($min ? "$minʬ" : '');
	my $hour = int($HyosenTime / 3600);
	$hour = ($hour ? "$hour����" : '');
	my $yosenTime = "$hour$min$sec";
	$sec = ($HdevelopeTime % 60);
	$sec = ($sec ? "$sec��" : '');
	$min = ($HdevelopeTime % 3600);
	$min = ($min ? "$minʬ" : '');
	$hour = int($HdevelopeTime / 3600);
	$hour = ($hour ? "$hour����" : '');
	my $developeTime = "$hour$min$sec";
	$sec = ($HinterTime % 60);
	$sec = ($sec ? "$sec��" : '');
	$min = ($HinterTime % 3600);
	$min = ($min ? "$minʬ" : '');
	$hour = int($HinterTime / 3600);
	$hour = ($hour ? "$hour����" : '');
	my $interTime = "$hour$min$sec";
	$sec = ($HfightTime % 60);
	$sec = ($sec ? "$sec��" : '');
	$min = ($HfightTime % 3600);
	$min = ($min ? "$minʬ" : '');
	$hour = int($HfightTime / 3600);
	$hour = ($hour ? "$hour����" : '');
	my $fightTime = "$hour$min$sec";


	# �ȡ��ʥ��ȡ������󹹿������ḫɽ
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
<H1>���勵����ơ��֥�</H1>
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
	$tournament .= "������\t$AfterName��\t�ʹԾ���\t��������\n";
	my $end = 0;
	if($iNumber > 1) {
		out("<TABLE BORDER=0><TR $HbgTitleCell><TH colspan=2>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH colspan=2>${HtagTH_}������${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}���ﾡ��<BR>��ȯ���<BR>�������${H_tagTH}</TH></TR>");
	} else {
		$end =1;
	}
	while($iNumber > 1){
		if($HislandTurn < $HyosenTurn) {
			# ͽ��
			$HislandFightMode = 0;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime1[($HislandTurn % ($#HtmTime1 + 1))] : $HyosenTime;
			$timeString = timeToString($HislandLastTime);
			foreach(1..$HyosenRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\tͽ��\t$timeString\n";
				if(!$flag) {
					$flag = 1;
					out("<TR class='InfoCellT'><TH colspan=2><span class='lbbsOW'>ͽ��</span></TH><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$yosenTime</B>���1��<B>$HyosenRepCount�����󹹿�</B>��<B>��$HyosenTurn������</B></TD><TD align='right'>��$HyosenTurn</TD>");
					out("<TD>${timeString}��");
				}
				last if($HislandTurn == $HyosenTurn);
			}
			if($HislandTurn == $HyosenTurn) {
				out("${HtagTH_}${timeString}${H_tagTH}</TD><TD align='center'>��</TD></TR>");
				$flag = 0;
			}
		} elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $fturn) {
			# ��ȯ
			$iNumber = $Htournament if(($HislandFightMode == 0) && ($iNumber > $Htournament));
			$HislandFightMode = 1;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime2[($HislandTurn % ($#HtmTime2 + 1))] : $HdevelopeTime;
			$timeString = timeToString($HislandLastTime);
			$HfightTurn = $HfinalTurn if($iNumber <= 2);
			foreach(1..$HdeveRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\t��ȯ\t$timeString\n";
				if(!$flag) {
					$round++;
					$flag = 1;
					my $endturn = $HyosenTurn + $HdevelopeTurn + $fturn;
					if($iNumber + $nofight <= 2) {
						out("<TR $HbgInfoCell><TH>�衡��</TH>");
					} elsif($iNumber + $nofight <= 4) {
						out("<TR $HbgInfoCell><TH>��辡</TH>");
					} else {
						out("<TR $HbgInfoCell><TH>��${round}����</TH>");
					}
					out("<TD><span class='lbbsSS'>��ȯ����</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$developeTime</B>���1��<B>$HdeveRepCount�����󹹿�</B>��<B>��$HdevelopeTurn������</B></TD><TD align='right'>$HislandTurn��$endturn</TD>");
					out("<TD>${timeString}��");
				}
				last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn);
			}
			if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn) {
				out("<B>${timeString}</B></TD><TD align='center'>��</TD></TR>");
				$flag = 0;
			}
		}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
			# ��Ʈ
			$HislandFightMode = 2;
			$HislandLastTime += ($HflexTimeSet) ? 3600 * $HtmTime3[($HislandTurn % ($#HtmTime3 + 1))] : $HfightTime;
			$timeString = timeToString($HislandLastTime);
			#$tournament .= "$HislandTurn\t$iNumber\t��Ʈ��\t$timeString\t$HfightRepCount\n";
			foreach(1..$HfightRepCount){
				$HislandTurn++;
				$tournament .= "$HislandTurn\t$iNumber\t��Ʈ��\t$timeString\n";
				if(!$flag) {
					$flag = 1;
					my $endturn = $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn;
					if($iNumber + $nofight <= 2) {
						out("<TR class='InfoCellT'><TH>�衡��</TH>");
					} elsif($iNumber + $nofight <= 4) {
						out("<TR class='InfoCellT'><TH>��辡</TH>");
					} else {
						out("<TR class='InfoCellT'><TH>��${round}����</TH>");
					}
					out("<TD><span class='lbbsOW'>��Ʈ����</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$fightTime</B>���1��<B>$HfightRepCount�����󹹿�</B>��<B>��$HfightTurn������</B></TD><TD align='right'>$HislandTurn��$endturn</TD>");
					out("<TD>${timeString}��");
				}
				last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn);
			}
			if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn) {
				my $nofight = $round * $HnofightUp + $HnofightTurn . "������";
				$nofight = '��' if($iNumber <= 2);
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
			last if(!$fturn); # ̵�¥롼�ײ���
			$HfightTurn = $HfinalTurn if($iNumber <= 2);
			if($iNumber > 1) {
				foreach(1..$HdeveRepCount){
					$HislandTurn++;
					$tournament .= "$HislandTurn\t$iNumber\t��ȯ\t$timeString\n";
					if(!$flag) {
						$round++;
						$flag = 1;
						my $endturn = $HyosenTurn + $HdevelopeTurn + $fturn;
						if($iNumber + $nofight <= 2) {
							out("<TR $HbgInfoCell><TH>�衡��</TH>");
						} elsif($iNumber + $nofight <= 4) {
							out("<TR $HbgInfoCell><TH>��辡</TH>");
						} else {
							out("<TR $HbgInfoCell><TH>��${round}����</TH>");
						}
						out("<TD><span class='lbbsSS'>��ȯ����</span></TD><TD align='right'>$iNumber$AfterName</TD><TD align='right'><B>$developeTime</B>���1��<B>$HdeveRepCount�����󹹿�</B>��<B>��$HdevelopeTurn������</B></TD><TD align='right'>$HislandTurn��$endturn</TD>");
						out("<TD>${timeString}��");
					}
					last if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn);
				}
				if($HislandTurn == $HyosenTurn + $HdevelopeTurn + $fturn) {
					out("<B>${timeString}</B></TD><TD align='center'>��</TD></TR>");
					$flag = 0;
				}
			}
		}
	}
	unlock();

	if(!$end) {
		out("</TABLE><BR>");
		my $con = ('', '����Ʈ��λ����(���ﾡ��ȯ�����븫����)�ˤʤ�������ह����ǺǾ�̤����<B>�Լ�����</B>���ޤ���<BR>')[$HconsolationMatch];
		my $halffight = int($HfightTurn/2);
		my $halffinal = int($HfinalTurn/2);

		out(<<END);
<blockquote>
����ⷫ������<B>$HstopAddPop��</B>�ˤʤ�ȿ͸����ä����ȥåפ��ޤ���<BR>
�� �ޤ�ͽ���Ǥϡ����ȼԿ���<B>$Hno_work$HunitPop</B>��Ķ���Ƥ⡢�͸����ä����ȥåפ��ޤ�<BR>
��������꤬���ʤ���硢�ޤ��ϳ�ȯ������ˡ���꤬���ʤ��ʤä����פ�<B>���ﾡ����</B>�Ȥʤ�ޤ���<BR>
�� ���ﾡ�ξ�硢<B>�ʲ������${HnofightUp}+${HnofightTurn}�˥�����</B>�γ�ȯ��ߤˤʤ�ޤ��� <BR>
����Ʈ���֤�Ⱦʬ��$halffight�����󡦷辡��$halffinal������ˤ��в᤹��ޤǤˡ�����꤬���ʤ��ʤä����׵ڤ�<BR>
�� ������<B>��Ʈ�԰ٲ����$do_fight��������ʤ��ä�</B>�ʤޤ��ϡ�<B>��꤬���٤�����ɸ���Ԥ�ʤ��ä�</B>�˾��פ�<B>���ﾡ����</B>�Ȥʤ�ޤ���<BR>
�� ���ξ��ϡ���Ʈ���ϻ�����ξ��֤��ᤵ�졢��ȯ��ߤˤʤ�ޤ�����ߴ��֤ϡ�<B>�ʲ������${HnofightUp}+${HnofightTurn}�ˡ� �в᥿�����</B>�Ǥ��� <BR>
$con
</blockquote></DIV>
END
	} else {
		out("������Ͻ�λ���ޤ�����");
	}
#	out(<<END);
#<DIV id='hyo'><INPUT TYPE="button" VALUE="�ȡ��ʥ��ȹ��������ḫɽ�򥯥�åץܡ��ɤ˥��ԡ�" onClick="textcopy(searchID('ALIST').value);"></DIV>
#<DIV id='list'><textarea NAME="ALIST" cols="100" rows="0">$tournament</textarea></DIV>
#END
}

# ����ε�Ͽ
sub FightViewMain {

	my %rankKind = (
		'pop' => '�͸�',
		'gain' => '������и���',
		'money' => '���',
		'food' => '����',
		'area' => '����',
		'farm' => '���쵬��',
		'factory' => '���쵬��',
		'mountain' => '�η��쵬��',
		'monsterkill' => '�����༣��',
		'itemNumber' => "$HitemName[0]������",
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
#		out ("${HtagBig_}�ǡ���������ޤ���${H_tagBig}$HtempBack\n");
		return;
	}
	my @lines = <IN>;
	close(IN);
	unlock();

#	out ("${HtagTitle_}����ε�Ͽ${H_tagTitle}<BR><DIV ALIGN=right>*�ԼԤ���̾�򥯥�å������������ξ���������ޤ�</DIV>\n");
#	out ("<DIV align='center'>$HtempBack</DIV><BR>\n");
	out("<HR>") if($HplayNow && $Htournament);
	out(<<END);
<DIV ID='FightLog'>
<H1>����ε�Ͽ</H1>
*�ԼԤ�${AfterName}̾�򥯥�å������������ξ����򸫤뤳�Ȥ��Ǥ��ޤ���
END

	my $lineflag = 0;
	chomp(@lines);
	foreach $line (@lines) {
		if($line =~ /<[0-9]*>/) {
			$line =~ s/<|>//g;
			$lineflag = $line;
			my $msg = (!$line) ? "ͽ�����" : ($line == 99) ? "�辡��" : $line."����";
			out("</TABLE>\n") if($line < 99);
			out("<HR><DIV ID='fightlogS'><H1>${HtagHeader_}$msg${H_tagHeader}</H1></DIV>");
			# �ơ��֥�إå�
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
					$mStr1 =  "<TH $HbgTitleCell>${HtagTH_}�߷�${H_tagTH}</TH>";
				}
				my $col = ($HuseBase || $HuseSbase) ? 10 : 9;
				out(<<END);
<TABLE BORDER>
<TR><TH colspan=3></TH><TH $HbgTitleCell colspan=$col>${HtagTH_}����${H_tagTH}</TH><TH colspan=1></TH>
<TH $HbgTitleCell colspan=$col>${HtagTH_}�Լ�${H_tagTH}</TH></TR>
<TR>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�Լ�${H_tagTH}</TH>
<TH $HbgTitleCell width=15>��</TH>
<TH $HbgTitleCell>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�ɷ�${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}̱��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ȯ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell width=15>��</TH>
<TH $HbgTitleCell>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�ɷ�${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}̱��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ȯ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
</tr>
END

			}

		} elsif($lineflag == 0) {
			# ͽ�����
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
			# �ȡ��ʥ��ȷ��
			my($count, $id, $name, $score, $data, $tId, $tName, $tScore, $tData, $reward) = split(/\,/,$line);
			my(@subExt) = split(/-/,$data);
			my(@tSubExt) = split(/-/,$tData);
#			$tName = "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
#						$HtagName2_.$tName.$H_tagName2."</A>";
			$tPop .= ${HunitPop};
			$score .= $rankAfter{$HrankKind};
			if($tId == -1) {
				$tName = "${HtagName2_}- ���ﾡ -${H_tagName2}";
				$tScore = "��";
			} elsif($tId == -2) {
				$tName = "${HtagName2_}- ������ -${H_tagName2}";
				$tScore = "��";
			} else {
				if(-e "${HfightdirName}/${tId}_lose.${HsubData}") {
					$tName = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?LoseMap=${tId}\">${HtagName2_}$tName${H_tagName2}</A>";
				} else {
					$tName = "${HtagName2_}$tName${H_tagName2}";
				}
				$tScore .= $rankAfter{$HrankKind};
			}
			if($tId != -9) {
				my(@after) = ('', '', '��', '��', "$HunitPop", 'ȯ', 'ȯ', 'ȯ', '��', '��', '��');
				foreach (2..$#subExt){
					$subExt[$_] = $subExt[$_] ? "${subExt[$_]}${after[$_]}" : '�ʤ�';
					$tSubExt[$_] = ($tScore == '��') ? '��' : ($tSubExt[$_] ? "${tSubExt[$_]}${after[$_]}" : '�ʤ�');
				}
				my($mStr1, $mStr2) = ('', '');
				if($HuseBase || $HuseSbase) {
					$mStr1 =  "<TD $HbgInfoCell align=center>$subExt[3]</TD>";
					$mStr2 =  "<TD $HbgInfoCell align=center>$tSubExt[3]</TD>";
				}
				out(<<END);
<TR><TD $HbgInfoCell align=right>${HtagName_}${name}${H_tagName}</TD>
<TD $HbgInfoCell align=center>${tName}</TD>
<TD $HbgInfoCell>��</TD>
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
<TD $HbgInfoCell>��</TD>
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
				out("<TR><TD class='M' colspan=6 align=right>${HtagName_}${name}${H_tagName}��<B>�Լ����衪</B></TD></TR>\n");
			}
		}

	}
	out("</TABLE>\n") if(@lines != ());
	out("</DIV>\n");

}

#----------------------------------------------------------------------
# ��������ǧ
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
	$sec = ($sec ? "$sec��" : '');
	my $min = ($unitTime % 3600);
	$min = ($min ? "$minʬ" : '');
	my $hour = int($unitTime / 3600);
	$hour = ($hour ? "$hour����" : '');

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
<a name='top'><H1>�������</H1></a>
END

$src .= "<a href='#admin' style='text-decoration=none'>��������</a> / ";
$src .= "<a href='#basic' style='text-decoration=none'>��������</a> / ";
$src .= "<a href='#ocean' style='text-decoration=none'>����⡼��</a> / ";
$src .= "<a href='#autokeep' style='text-decoration=none'>̵��(����)����</a> / ";
$src .= "<a href='#survival' style='text-decoration=none'>���Х��Х�</a> / ";
$src .= "<a href='#imperial' style='text-decoration=none'>�ر���(��Ԣ����)</a> / ";
$src .= "<a href='#tournament' style='text-decoration=none'>�ȡ��ʥ���</a> / ";
$src .= "<a href='#amity' style='text-decoration=none'>ͧ��������</a> / ";
$src .= "<a href='#ally' style='text-decoration=none'>Ʊ�������ƥ�</a> / ";
$src .= "<a href='#dewar' style='text-decoration=none'>�����۹𥷥��ƥ�</a> / ";
$src .= "<a href='#event' style='text-decoration=none'>���٥�ȥ����ƥ�</a>";
$src .= "<BR>";
$src .= "<a href='#usecom' style='text-decoration=none'>�Ϸ������ޥ������</a> / ";
$src .= "<a href='#town' style='text-decoration=none'>�ԻԷ�����</a> / ";
$src .= "<a href='#complex' style='text-decoration=none'>ʣ���Ϸ�</a> / ";
$src .= "<a href='#core' style='text-decoration=none'>����</a> / ";
$src .= "<a href='#navy' style='text-decoration=none'>����</a> / ";
$src .= "<a href='#def' style='text-decoration=none'>�ɱһ���</a> / ";
$src .= "<a href='#base' style='text-decoration=none'>���ϡ��ߥ�����</a> / ";
$src .= "<a href='#weather' style='text-decoration=none'>ŷ��</a> / ";
$src .= "<a href='#disaster' style='text-decoration=none'>�ҳ�</a> / ";
$src .= "<a href='#monster' style='text-decoration=none'>����</a> / ";
$src .= "<a href='#hmonster' style='text-decoration=none'>�������</a> / ";
$src .= "<a href='#item' style='text-decoration=none'>�����ƥ�</a> / ";
$src .= "<a href='#monument' style='text-decoration=none'>��ǰ��</a> / ";
$src .= "<a href='#prize' style='text-decoration=none'>�������ա��ƾ�</a> / ";
$src .= "<a href='#command' style='text-decoration=none'>���ޥ�ɰ���</a>";

	my @adminStr = ('�����Ͱʳ���õ����', '�����ͤ���õ����(�᡼��or�Ǽ���������Ͽ����ꤷ�Ƥ�������)');
	my @doStr  = ('���ʤ�', '����');
	my %rankKind = (
		'pop' => '�͸�',
		'gain' => '������и���',
		'money' => '���',
		'food' => '����',
		'area' => '����',
		'farm' => '����',
		'factory' => '����',
		'mountain' => '�η���',
		'monsterkill' => '�����༣��',
		'itemNumber' => "$HitemName[0]������",
		'point' => "$HpointName",
	);
	my @useStr = ('�Ȥ�ʤ�', '�Ȥ�');
	my @useableStr = ('�Ȥ��ʤ�', '�Ȥ���');
	my @seeStr = ('�����ʤ�', '������', '100�ΰ̤ǻͼθ���');
	my @pointStr = ('���ʤ�', '��ɸ����', '��ɸ�ʤ�');
	my @axesStr = ('�Ȥ�ʤ�', '��ȯ���̤�������ǥ��顼ȯ����', '��ȯ���̤������', '�ȥåץڡ����˥�������������', '��ȯ���̤������ + �ȥåץڡ����˥�������������');
	my $topAxes = ($HtopAxes > 4) ? 4 : $HtopAxes;
	my @selectStr = (
		"$AfterName�����Ǥ⾯�ʤ�����̤��ǲ��̤οر�",
		"������(\"��פ�$AfterName��/�رĤο�\"��Ķ���ʤ�)",
		"�����ǽ(\"��פ�$AfterName��/�رĤο�\"��Ķ���ʤ�)"
	);
	my @anStr = ('�ʤ�', '����');
	my @selfStr = ('������', '�����ʤ�', 'ͧ���������ʤ�');
	my $useDeWar = ('', '<BR>�����������¤ϰ��ڤ���ޤ��󡣡������۹�פʤ��ǹ����ǽ�Ǥ���', "<BR>�����������۹�פ��Ƥ��ʤ�$AfterName�ؤι���ϵ��Ĥ���ޤ��󡣡������۹��ľ�夫�鹶���ǽ�Ǥ���", "<BR>�����������۹�פ��Ƥ��ʤ�$AfterName�ؤι���ϵ��Ĥ���ޤ���ͱͽ������λ���������Τ߹����ǽ�Ǥ���")[$HuseDeWar];
	my @hide = ('������', '����');
	my @ox = ('��', '��');
	my @turnStr = ($HtagComName2_, $HtagComName1_);
	my @saftyStr = ('���ʤ�', '����', 'ͧ�����̵���ˤ���');
	my @nodefStr = ('���ʤ�', "��$AfterName�ι���Τ�����", "ͧ��������ꤷ�Ƥ���Ƥ���$AfterName�ι�������Ƥ���", "ͧ��������ꤷ�Ƥ���$AfterName�ι�������Ƥ���", "ͧ��������ꤷ�Ƥ���$AfterName�ι���⡤ͧ��������ꤷ�Ƥ���Ƥ���$AfterName�ι�������Ƥ���");
	my @nearfar = ('�Ǥ�<B>�ᤤ</B>�Ϸ�������֤���ɸ��õ��', '�Ǥ�<B>��</B>�Ϸ�������֤���ɸ��õ��', '�������<B>������</B>����ɸ��õ��');

# �����ѥǡ���
#------------------

	$src .= <<"END";
<HR>
<a name='admin'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ��������</H3></a>
END

	if($admin) {
		$src .= <<"END";
������̾��<B>$HadminName</B><BR>
�����ԤΥ᡼�륢�ɥ쥹��<B><a href=\"mailto:$Hemail\">$Hemail</a></B><BR>
�Ǽ��ĥ��ɥ쥹��<B><a href=\"$Hbbs\">$Hbbs</a></B><BR>
�ۡ���ڡ����Υ��ɥ쥹��<B><a href=\"$Htoppage\">$Htoppage</a></B><BR>
�����Υ���������������ڡ�����<B><a href=\"$imageExp\">$imageExp</a></B><BR>
�����������Ѳ������̥ե����롡<B><a href=\"$localImg\">$localImg</a></B><BR>
END

		$src .= <<"END";
<BR>
�ǥХå��⡼�ɡ�<B>$switchStr[$Hdebug]</B><BR>
���֥ե������<B>$HbaseDir</B><BR>
�����ե������<B>$HimageDir</B><BR>
CSS,JS�ե������<B>$efileDir</B><BR>
GMT ���Ф��� JST �λ�����<B>${Hjst}��</B><BR>
gzip����Ѥ��ư����������뤫��<B>$doStr[$Hgzip]</B><BR>
gzip�Υ��󥹥ȡ����衡<B>$HpathGzip</B><BR>
<BR>
�ꥢ�륿���ޡ��λ��ѡ�<B>$useStr[$Hrealtimer]</B><BR>
�ȥåץڡ����Υ쥤�����Ȥ�tempTop.html�ǻ��ꤹ�뤫��<B>$doStr[$HlayoutTop]</B><BR>
�ȥåץڡ�����ɽ������${AfterName}�ο���<B>$HviewIslandCount</B><BR>
���ե������ݻ����������<B>$HlogMax������</B><BR>
�ֺǶ�ν�����פ�ɽ��������Υ��������<B>$HtopLogTurn������</B><BR>
�ֺǶ�ν�����פ�HTML�����뤫��<B>$doStr[$HhtmlLogMake]</B><BR>
END

		$src .= <<"END" if($HhtmlLogMake);
�ֺǶ�ν�����פ�ɽ��������Υ������(HTML)��<B>$HhtmlLogTurn������</B><BR>
�ȥåץڡ����ΡֺǶ�ν�����פ�HTML�˥�󥯤��뤫��<B>$doStr[$HhtmlLogMode]</B><BR>
END

		$src .= <<"END";
<BR>
��ȯ���̤ǥݥåץ��åץʥӤ�ɽ�����뤫��<B>$doStr[$HpopupNavi]</B><BR>
��$AfterName(��ȯ����)�Ρֶᶷ�פ�history.cgi��ɽ�����뤫��<B>$doStr[$HuseHistory1]</B><BR>
¾$AfterName(�Ѹ����̤ʤ�)�Ρֶᶷ�פ�history.cgi��ɽ�����뤫��<B>$doStr[$HuseHistory2]</B><BR>
�Хå����åפ򲿥����󤪤��˼�뤫��<B>$HbackupTurn������</B><BR>
�Хå����åפ򲿲�ʬ�Ĥ�����<B>$HbackupTimes��ʬ</B><BR>
ȯ�����ݻ��Կ���<B>$HhistoryMax��</B><BR>
������Ǽ��Ĥλ��ѡ�<B>$useStr[$HuseLbbs]</B><BR>
�����ʰ׷Ǽ��Ĥ���Ѥ��뤫��<B>$useStr[$HuseExlbbs]</B><BR>
END

		if($HuseExlbbs) {
			$src .= "�����ʰ׷Ǽ��ĤΥ��ɥ쥹��<B><A href='$HlbbsDir/view.cgi?admin=$HviewPass'>$HlbbsDir</A></B><BR>";
		}

		$src .= <<"END";
<BR>
��������ޥå�ɽ����ǽ�ˤ��뤫����<B>$doStr[$HmlogMap]</B><BR>
¾�ͤ�����򸫤��ʤ����뤫����<B>$seeStr[$HhideMoneyMode]</B><BR>
���Ϸϥ��ΤޤȤ�˺�ɸ����Ϥ��뤫����<B>$pointStr[$HoutPoint]</B><BR>
��$AfterName�μ��٥�(��̩)����Ϥ��뤫����<B>$doStr[$HbalanceLog]</B><BR>
JavaScript�ΰ��������ե����벽���뤫����<B>$doStr[$HextraJs]</B><BR>
�ץ쥤�䡼�Υѥ���ɤ�Ź沽���뤫����<B>$doStr[$cryptOn]</B><BR>
<BR>
�ѥ���ɡ����顼�β��̤˷ٹ�ʸ��ɽ�����뤫����<B>$doStr[$HpassError]</B><BR>
������������Ȥ뤫����<B>$axesStr[$topAxes]</B><BR>
���絭Ͽ�����<B>$HaxesMax��</B><BR>
��ٷ�¬���뤫����<B>$doStr[$Hperformance]</B><BR>
<BR>
END
	}

	$src .= <<"END";
������${AfterName}�ϡ�<B>$adminStr[$HadminJoinOnly]</B><BR>
END
	if($HuseLbbs) {
	}

	$src .= <<"END";
<BR>
COOKIE�ˤ��ID�����å��򤹤뤫����<B>$doStr[$checkID]</B><BR>
COOKIE�ˤ��ֲ����Υ���������פ�����å����롩��<B>$doStr[$checkImg]</B><BR>
END
	my @freepassName;
	my $i;
	if($freepass[0] eq '') {
		@freepassName = ('�ʤ�') ;
	} else {
		foreach $i (@freepass) {
			next unless(defined $HidToNumber{$i});
			push(@freepassName, "$HidToName{$i}${AfterName}");
		}
	}
	$src .= "COOKIE�����å��ʾ�Σ��Ĥ�����ˤ��Ƚ�����$AfterName��ID��<B>@freepassName</B><BR>" if($checkId || $checkImg);

	if($HjoinCommentPenaltyStr ne '') {
		$src .= <<"END";
<BR>
��������ȯ�����Τޤޤξ�硢�����ͤ�������ˤ��뤫����<B>$doStr[($HjoinCommentPenalty > 0)]</B><BR>
END
		$src .= "����ȯ���塢<B>$HjoinCommentPenalty������</B>��˥����Ȥ��ʤ���С������ͤ�������ˤʤ�ޤ�����������$HjoinCommentPenaltyStr<BR>" if($HjoinCommentPenalty);
	}
	$src .= "<BR>�ִ����ͤ�������פǤ�ǽ�Υ��ޥ�ɤ�����������פʤ���ǽ����򤹤뤫����<B>$doStr[$HforgivenGiveUp]</B><BR>";
	$src .= "<BR>�ִ����ͤ�������פ���ؤι���(�����ɸ��������ɸ����ߥ����빶��)����Ĥ��뤫����<B>$doStr[$HforgivenAttack]</B><BR>";

# ��������
#------------------

	my $doNothingMoney = "$HdoNothingMoney$HunitMoney";
	1 while $doNothingMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;

	$src .= <<"END";
<HR>
<a name='basic'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ��������</H3></a>
${AfterName}�κ������<B>$HmaxIsland</B><BR>
${AfterName}���礭����<B>${HislandSizeX}x${HislandSizeY}</B><BR>
���ޥ�����ϸ³�����<B>$HcommandMax</B><BR>
1�����󤬲��ä���<B>${unitTime}�� ( $hour$min$sec )</B><BR>
����ι����ǲ�������ʤ�뤫��<B>$repeatTurn������</B><BR>
�����ཪλ���������<B>$HgameLimitTurn������</B><BR>
��̤Τ�Ȥˤʤ����ǡ�<B>$rankKind{$HrankKind}</B><BR>
<BR>
�ֻ�ⷫ��פǤμ�����<B>$doNothingMoney</B><BR>
<BR>
������Ͽ���줿${AfterName}�γ�ȯ���֡�<B>$HdevelopTurn������</B><BR>
�������ޥ�ɼ�ư���ϥ�������ʳ�ȯ���֡ˡ�<B>$HdevelopGiveupTurn������</B><BR>
�������ޥ�ɼ�ư���ϥ��������<B>$HgiveupTurn������</B><BR>
������$AfterName�򸫤Ĥ���ľ������֥��������<B>$HjoinGiveupTurn������</B><BR>
END

	if($HuseLbbs) {
		my $lbbsMoneyPublic = "$HlbbsMoneyPublic$HunitMoney";
		1 while $lbbsMoneyPublic =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $lbbsMoneySecret = "$HlbbsMoneySecret$HunitMoney";
		1 while $lbbsMoneySecret =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= <<"END";
<BR>
������Ǽ��Ĥ�ɽ���Կ���<B>$HlbbsViewMax</B><BR>
������Ǽ��Ĥ���¸�Կ���<B>$HlbbsMax</B><BR>
������Ǽ��Ĥؤ�ƿ̾ȯ������Ĥ��뤫����<B>$doStr[$HlbbsAnon]</B><BR>
������Ǽ��Ĥ�ȯ���Ԥ�̾����ɽ�����뤫����<B>$doStr[$HlbbsSpeaker]</B><BR>
������Ǽ��Ĥǥ����ȥ�󥯤���Ѥ��뤫����<B>$doStr[($HlbbsAutolinkSymbol ne '')]</B>(�ޡ�����<B>$HlbbsAutolinkSymbol</B>)<BR>
¾$AfterName�Υ�����Ǽ��Ĥ�ȯ�����뤿������ѡ���������<B>$lbbsMoneyPublic</B>�����롡<B>$lbbsMoneySecret</B><BR>
END
	}

# ��⡢�����ʤɤ�������
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
		$oilMoney = "�����������($oilMoney2��$oilMoney)";
	}
	$oilRatio = $HoilRatio/10;
	$src .= <<"END";
<BR><TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}������ / ������${H_tagTH}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}������� / ���翩��${H_tagTH}</TH><TH colspan=5>${HtagTH_}�Ǿ�ñ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�͸�${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�ڤο�${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$initialMoney / $maximumMoney</TD><TD align='center'>$initialFood / $maximumFood</TD><TD align='right'>1$HunitMoney</TD><TD align='right'>1$HunitFood</TD><TD align='right'>1$HunitPop</TD><TD align='right'>1$HunitArea</TD><TD align='right'>1$HunitTree</TD></TR>
</TABLE></B><BR>
̾���ѹ��Υ����ȡ�<B>$costChangeName</B><BR>
�ڤ�1$HunitTree����������͡�<B>$treeValue</B><BR>
1��������������ڤ��ܿ�(��1Hex������)��<B>${HtreeGrow}$HunitTree</B><BR>
�͸�1$HunitPop������ο��������̡�<B>${HeatenFood}x1$HunitFood</B><BR>
���äο���ñ�̡�<B>$HunitMonster</B><BR>
<BR>
����ȯ����Ψ��<B>(������� - ȯ���Ѥ����Ŀ� x 25)%</B><BR>
���ĸϳ��Ψ��<B>$oilRatio%</B><BR>
���ļ�����<B>$oilMoney</B><BR>
<BR>
�����Ĵ���ʿ��������μ�����Ψ���̾�졼�Ȥ��Ф�����Ψ�ˡ�<B>${HincomeRate}��</B><BR>
END

# ����⡼��
#------------------

	$src .= <<"END";
<HR>
<a name='ocean'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ����⡼��</H3></a>
����⡼�ɡ�<B>$switchStr[($HoceanMode > 0)]</B>
END
	$src .= "��($AfterName��$AfterName���ҤȤĤʤ�����礭�ʥޥåפˤʤ�ޤ�)<BR>" if($HoceanMode);

	my(@yesno) = ('������', '�Ϥ�');
	if($HoceanMode > 0) {
		$src .= <<"END";
<blockquote>
${AfterName}�����ֿ���<B>${HoceanSizeX}x${HoceanSizeY}</B><BR><BR>
����ޥåפ�ɽ�����뤫����<B>$doStr[$HuseOceanMap]</B><BR>
END
		if($HuseOceanMap) {
			$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH colspan='2'>����ޥå��Ϸ�</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[0]'></TD><TH>̤�Τγ���</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[1]'></TD><TH>��ʬ��$AfterName</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[2]'></TD><TH>�դĤ���$AfterName</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[3]'></TD><TH>�Хȥ�ե������</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HoceanImage[4]'></TD><TH>�����ͤ�������</TH></TR>
</TABLE>
���ϵ�⡼�ɤλ����оݤ��礬�ޥåפ�����ˤ���褦�ˤ��뤫����<B>$doStr[$HadjustMap]</B><BR>
������ޥåפβ��˾ܺ٥ޥåפ�ɽ�����뤫����<B>$doStr[($HshowWorld > 0)]</B><BR><BR>
END
		}
		$src .= <<"END";
���褬��³���Ƥ�����ɤ����Ǥϡ������ư���ɸ������ԡ������ɸ����ޥ�ɤ�Ȥ��ʤ����뤫��<BR>
�������ư���ɸ�������(������Ф����ư���ɸ������Ԥ�ޤ�)��<B>$useableStr[!$HnotuseNavyMove]</B><BR>
�������ɸ�(������Ф����ɸ��Ͻ���)��<B>$useableStr[!$HnotuseMonsterSend]</B><BR><BR>
�Хȥ�ե�����ɤϳ������³���ʤ�����<B>$yesno[$HfieldUnconnect]</B><BR>
END
		$src .= <<"END" if($HfieldUnconnect);
�Хȥ�ե��������δ��������äϰ�ư��ĤǤʤ���г��γ���ؤϽФ��ʤ��褦�ˤ��뤫����������<B>$yesno[$HfieldNavy]</B>�����á�<B>$yesno[$HfieldNavy]</B><BR>
END
		$src .= <<"END";
</blockquote>
END
	}
	$src .= <<"END";
<BR>
�ϵ�⡼�ɡ�<B>$switchStr[($Hroundmode > 0)]</B>
END
	$src .= "��(�ޥåפξ岼�Ⱥ������Ҥ���ޤ�)<BR>" if($Hroundmode);
# ���ǲ���̵�Ͳ�����
#----------------------

	my $autokeep = '';
	if($HautoKeeper > 1) {
		my $autoKeeperPop = "$HautoKeeper$HunitPop";
		1 while $autoKeeperPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$autokeep =<<"END";
<B>$autoKeeperPop��̵�Ͳ���ư����ǽȯư</B><BR>
��������������װʳ��Ǥϻ��ǽ����򤷤ʤ������������͸������ˤʤä���硢���Ϥ�ʿ�Ϥ��ʤ�������פ��Ƥ��ޤ���<BR>
����¾����ɸ���δ����伫��(�����оݤ���)�˽и���β��á�������äϳ��ˤʤ���ǡ�<BR>
����¾�礫�鼫����ɸ�����Ƥ������ϡ����Խ�������롣�ʿ͸������ξ�硢�������ο͸��ˤʤ��<BR>
�����������ο͸��ǳ�ȯ���֤����롣
END
	} elsif($HautoKeeper) {
		$autokeep =<<"END";
<B>����Ƚ�����ǽȯư</B><BR>
��������������װʳ��Ǥϻ��ǽ����򤷤ʤ���<BR>
����¾����ɸ���δ����伫��(�����оݤ���)�˽и���β��á�������äϳ��ˤʤ���ǡ�<BR>
����¾�礫�鼫����ɸ�����Ƥ������ϡ����Խ�������롣<BR>
���������ͤ�������ˤ��롣�ʿ͸������ξ�硢�����������λ��˽������ο͸��ˤʤ��<BR>
��������
END
		$autokeep .= (!$HautoKeeperSetTurn) ? '�����ͤ�������ϴ����ͼ��Ȥμ�ˤ�äƲ������ޤ���' : "�����ͤ��������<B>$HautoKeeperSetTurn�������˼�ư���</B>����ޤ���";
	} else {
		$autokeep = '<B>���Ѥ��ʤ�</B>';
	}
	$src .= <<"END";
<HR>
<a name='autokeep'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ̵��(����)����</H3></a>
̵�Ͳ���ư���򡦻���Ƚ�����ǽ�λ��ѡ�$autokeep<BR><BR>
END

# ���Х��Х�⡼��
#------------------

	$src .= <<"END";
<HR>
<a name='survival'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ���Х��Х�</H3></a>
���Х��Х�⡼�ɡ�<B>$switchStr[($HsurvivalTurn > 0)]</B><BR>
END

	my $sec2 = ($HarmisticeTime % 60);
	$sec2 = ($sec2 ? "$sec2��" : '');
	my $min2 = ($HarmisticeTime % 3600);
	$min2 = ($min2 ? "$min2ʬ" : '');
	my $hour2 = int($HarmisticeTime / 3600);
	$hour2 = ($hour2 ? "$hour2����" : '');

	$src .= <<"END" if($HsurvivalTurn > 0);
<blockquote>
������֡�<B>$HsurvivalTurn������ޤ�</B><BR>
���������Υ����󹹿��ֳ֡�<B>${HarmisticeTime}�� ( $hour2$min2$sec2 )</B><BR>
��������棱��ι����ǲ�������ʤ�뤫��<B>$HarmisticeRepeatTurn������</B><BR>
�������󤴤Ȥ˺ǲ��̤�${AfterName}���Ǥ֤���<B>$HturnDead������($HsurvivalTurn������ʹ�)</B><BR>
</blockquote>
END

# �ر���⡼��
#------------------

	$src .= <<"END";
<HR>
<a name='imperial'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �ر���(��Ԣ����)</H3></a>
�ر���⡼�ɡ�<B>$switchStr[($HarmisticeTurn > 0)]</B><BR>
END

	my $cdr = (!$HcampDeleteRule) ? "" : ($HcampDeleteRule == 1) ? "������ͭΨ<B>(50��رĿ�)%̤��</B>�Ǿ���" : "������ͭΨ<B>${HcampDeleteRule}%̤��</B>�Ǿ���";
	my $initialMoney2 = "$HinitialMoney2$HunitMoney";
	1 while $initialMoney2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $initialFood2 = "$HinitialFood2$HunitFood";
	1 while $initialFood2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END" if($HarmisticeTurn);
<blockquote>
������֡�<B>$HarmisticeTurn������ޤ�</B><BR>
���������Υ����󹹿��ֳ֡�<B>${HarmisticeTime}�� ( $hour2$min2$sec2 )</B><BR>
��������棱��ι����ǲ�������ʤ�뤫��<B>$HarmisticeRepeatTurn������</B><BR>
������<B>��ͭΨ${HfinishOccupation}%</B><BR>
�ر��¤���˰ܹԤ��륿�������<B>$HpreGiveupTurn������</B><BR>
�ֿرĶ�Ʊ��ȯ�פ��Ǥ���褦�ˤ��뤫����<B>$doStr[$HuseCoDevelop]</B><BR>
�رĥѥ���ɤǥѥ�����ѹ����Ǥ���褦�ˤ��뤫����<B>$doStr[$HpassChangeOK]</B><BR>
�رĳ��ؤα������Ĥ��뤫����<B>$doStr[!$HcampAidOnly]</B><BR>
�رĤ��������ˡ��<B>$selectStr[$HcampSelectRule]</B><BR>
�رĤξ��Ǥ����뤫����<B>$anStr[($HcampDeleteRule > 0)]</B>$cdr<BR>
�رĺ����������ޥ��ɽ������<B>${HcampCommandTurnNumber}</B>(�� $HrepeatTurn������)<BR>
�����೫�ϸ�ν�����Ƚ�������������� <B>${initialMoney2}</B> / ������� <B>${initialFood2}</B><BR>
</blockquote>
END

# �ȡ��ʥ��ȥ⡼��
#---------------------

	$src .= <<"END";
<HR>
<a name='tournament'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �ȡ��ʥ���</H3></a>
�ȡ��ʥ��ȥ⡼�ɡ�<B>$switchStr[($Htournament > 0)]</B><BR>
END

	my $tournament = "";
	if($Htournament){
		# �ȡ��ʥ��ȡ������󹹿������ḫɽ
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
<DIV id='hyo'><INPUT TYPE="button" VALUE="�ȡ��ʥ��ȹ��������ḫɽ" onClick="display();"></DIV>
<DIV id='list'><INPUT TYPE="button" VALUE="����åץܡ��ɤ˥��ԡ�" onClick="textcopy(searchID('ALIST').value);display();"><BR>
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
		$tournament .= "������\t$AfterName��\t�ʹԾ���\t��������\n";
		while($ino > 1){
			if($itn < $HyosenTurn){
				# ͽ��
				$HislandFightMode = 0;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime1[($itn % ($#HtmTime1 + 1))] : $HyosenTime;
				$timeString = timeToString($ilt);
				foreach(1..$HyosenRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\tͽ��\t$timeString\n";
					last if($itn == $HyosenTurn);
				}
			} elsif($itn < $HyosenTurn + $HdevelopeTurn + $fturn) {
				# ��ȯ
				$ino = $Htournament if(($HislandFightMode == 0) && ($ino > $Htournament));
				$HislandFightMode = 1;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime2[($itn % ($#HtmTime2 + 1))] : $HdevelopeTime;
				$timeString = timeToString($ilt);
				$ftn = $HfinalTurn if($ino <= 2);
				foreach(1..$HdeveRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\t��ȯ\t$timeString\n";
					last if($itn == $HyosenTurn + $HdevelopeTurn + $fturn);
				}
			} elsif($itn < $HyosenTurn + $HdevelopeTurn + $ftn + $fturn) {
				# ��Ʈ
				$HislandFightMode = 2;
				$ilt += ($HflexTimeSet) ? 3600 * $HtmTime3[($itn % ($#HtmTime3 + 1))] : $HfightTime;
				$timeString = timeToString($ilt);
				#$tournament .= "$itn\t$ino\t��Ʈ��\t$timeString\t$HfightRepCount\n";
				foreach(1..$HfightRepCount){
					$itn++;
					$tournament .= "$itn\t$ino\t��Ʈ��\t$timeString\n";
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
						$tournament .= "$itn\t$ino\t��ȯ\t$timeString\n";
						last if($itn == $HyosenTurn + $HdevelopeTurn + $fturn);
					}
				}
			}
		}
		$tournament .= "</textarea></DIV>";
		$sec2 = ($HyosenTime % 60);
		$sec2 = ($sec2 ? "$sec2��" : '');
		$min2 = ($HyosenTime % 3600);
		$min2 = ($min2 ? "$min2ʬ" : '');
		$hour2 = int($HyosenTime / 3600);
		$hour2 = ($hour2 ? "$hour2����" : '');

		$src .= <<"END";
<blockquote>
ͽ�����̲������<B>$Htournament$AfterName</B><BR>
ͽ�����֥��������<B>$HyosenTurn������</B><BR>
ͽ��������Υ����󹹿��ֳ֡�<B>${HyosenTime}�� ( $hour2$min2$sec2 )</B><BR>
ͽ�������棱��ι����ǲ�������ʤ�뤫��<B>$HyosenRepCount������</B><BR><BR>
END

		$sec2 = ($HdevelopeTime % 60);
		$sec2 = ($sec2 ? "$sec2��" : '');
		$min2 = ($HdevelopeTime % 3600);
		$min2 = ($min2 ? "$min2ʬ" : '');
		$hour2 = int($HdevelopeTime / 3600);
		$hour2 = ($hour2 ? "$hour2����" : '');

		$src .= <<"END";
��ȯ���֥��������<B>$HdevelopeTurn������</B><BR>
��ȯ������Υ����󹹿��ֳ֡�<B>${HdevelopeTime}�� ( $hour2$min2$sec2 )</B><BR>
��ȯ�����棱��ι����ǲ�������ʤ�뤫��<B>$HdeveRepCount������</B><BR><BR>
END

		$sec2 = ($HinterTime % 60);
		$sec2 = ($sec2 ? "$sec2��" : '');
		$min2 = ($HinterTime % 3600);
		$min2 = ($min2 ? "$min2ʬ" : '');
		$hour2 = int($HinterTime / 3600);
		$hour2 = ($hour2 ? "$hour2����" : '');

	$src .= <<"END";
��ȯ���ֽ�λ�����Ʈ���֤ؤΰܹԤޤǤλ��֡�<B>${HinterTime}�� ( $hour2$min2$sec2 )</B><BR><BR>
END

		$sec2 = ($HfightTime % 60);
		$sec2 = ($sec2 ? "$sec2��" : '');
		$min2 = ($HfightTime % 3600);
		$min2 = ($min2 ? "$min2ʬ" : '');
		$hour2 = int($HfightTime / 3600);
		$hour2 = ($hour2 ? "$hour2����" : '');
		my $halffight = int($HfightTurn/2);
		my $halffinal = int($HfinalTurn/2);
		my $no_workPop = "$Hno_work$HunitPop";
		1 while $no_workPop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= <<"END";
��Ʈ���֥��������<B>$HfightTurn������</B><BR>
��Ʈ������Υ����󹹿��ֳ֡�<B>${HfightTime}�� ( $hour2$min2$sec2 )</B><BR>
��Ʈ�����棱��ι����ǲ�������ʤ�뤫��<B>$HfightRepCount������</B><BR><BR>
�辡�����Ʈ���֥��������<B>$HfinalTurn������</B><BR>
���ﾡ�γ�ȯ��ߥ��������<B>(�����)x${HnofightUp}+${HnofightTurn}������</B><BR>
���ﾡ�ˤʤ�ʤ�����Ρ�ɬ����Ʈ�԰ٲ����<B>$do_fight��</B><BR>
����Ʈ���֤�Ⱦʬ��$halffight�����󡦷辡��$halffinal������ˤ��в᤹��ޤǤˡ�����꤬���ʤ��ʤä����׵ڤӡ�������Ʈ�԰ٲ����$do_fight��������ʤ��ä�����꤬���٤�����ɸ���Ԥ�ʤ��ä��˾��פ����ﾡ�����Ȥʤ�ޤ���<BR>
�����ξ��ϡ���Ʈ���ϻ�����ξ��֤��ᤵ�졢��ȯ��ߤˤʤ�ޤ���<BR>
����ߴ��֤ϡ��ʲ������${HnofightUp}+${HnofightTurn}�ˡ� �в᥿������Ǥ��� <BR>
�͸����å��ȥåפ����ⷫ������<B>$HstopAddPop��</B><BR>
���ȼԿ��Υܡ������饤��<B>$no_workPop</B>�������ο��ͤ�Ķ����ȡ��͸����ä����ȥåפ��ޤ���ͽ���Τߡ�<BR>
���Լ�����פ��Ǥ���褦�ˤ��뤫����<B>$doStr[$HconsolationMatch]</B>������Ʈ��λ����(���ﾡ��ȯ�����븫����)�ˤʤ�������ह��$AfterName�ǺǾ�̤�$AfterName�����褷�ޤ���<BR>
<BR>$tournament</blockquote>
END
	}

# ͧ��������
#----------------------

	$src .= <<"END";
<HR>
<a name='amity'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ͧ��������</H3></a>
ͧ���������Ȥ�������<B>$useStr[$HuseAmity]</B><BR>
END

	if($HuseAmity && !$HarmisticeTurn) {
		if($HamityMax) {
			$src .= "ͧ���������ǽ�������<B>$HamityMax${AfterName}</B><BR>";
		} else {
			$src .= "ͧ���������ǽ�������<B>���¤ʤ�</B><BR>";
		}
		if($HamityMoney) {
			my $amityMoney = "$HamityMoney$HunitMoney";
			1 while $amityMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= "ͧ����$AfterName������ΰݻ����ѡ�<B>$amityMoney</B><BR>����(ͧ��������ꤷ�Ƥ���$AfterName��)��${amityMoney}���西����ɬ�פˤʤ�ޤ���<BR>";
		}
		if($HamityDisarm) {
			$src .= "���������ɸ����${AfterName}���Ф��Ƥϡ�<B>ͧ������˴����Ǥ��ޤ���</B>��(ǧ��ϤǤ��ޤ�)<BR>";
		}
		if($HamityInvalid) {
			$src .= "�����Хȥ�ե�����ɤǤϡִ��������סֺ�Ũ���ʤ��סֹ��⤷�ʤ������̵꤬���ˤʤ�ޤ���<BR>";
		}
	}

# �����۹𥷥��ƥ�
#----------------------
	$src .= <<"END";
<HR>
<a name='dewar'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �����۹𥷥��ƥ�</H3></a>
�������۹�ס������ġץ��ޥ�ɤ�Ȥ�������<B>$useStr[(($HuseDeWar > 0) && !$HarmisticeTurn && !$HsurvivalTurn && !$Htournament)]</B>$useDeWar<BR>
END

	if(!$HarmisticeTurn && !$HsurvivalTurn && !$Htournament) {
		if($HuseDeWar) {
			my $matchplay = ('<B>���ʤ�</B>', '<B>����</B>(���¤���)', '<B>����</B>(������ȯ�����Ϥ�Ʊ���ˡ���ư�ǣ���γ�ĥ�ǡ����Υ����󥿡��ꥻ�åȤ��Ϸ���¸��Ԥ�)')[$HmatchPlay];
			$src .= <<"END";
�����۹𤹤�Τ⤵���Τ⣱������ˤ��롩��$matchplay<BR>
�����۹�ͱͽ������<B>$HdeclareTurn������</B><BR>
�����ǿǥ��ޥ�ɤ������դ�����硢��ư�Ǵ���򵢴Ԥ��뤫����<B>$doStr[$HceasefireAutoNavyReturn]</B><BR>
��ĥ�ǡ����Υ����󥿡������ץ쥤�䡼�˸������뤫����<B>$doStr[$HcounterSetting]</B><BR>
END
		}
	}

# ���٥�ȥ����ƥ�
#----------------------

	$src .= <<"END";
<HR>
<a name='event'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ���٥�ȥ����ƥ�</H3></a>
���٥�ȳ������ι��Υ��������<B>$HnoticeTurn������</B><BR>
<TABLE BORDER>
<TR><TH>${HtagTH_}���٥�Ȥμ���${H_tagTH}</TH><TH>${HtagTH_}�������ʤ�${H_tagTH}</TH></TR>
<TR><TH>���Х��Х�</TH>
<TD class='N'>
<u>����$AfterName���ɸ�����Ƥ���¾$AfterName��°�δ����򤹤٤Ʒ��ˤ����Ǹ�ޤ������Ĥä�$AfterName��ͥ����</u>
<BR>������°���������Ϸ��ˤ��ʤ��Ƥ�褤��
<BR>������λ������Ͼ��餬�Ĥ��ޤǤǡ��ɲ��ɸ��ϤǤ��ʤ���
</TD></TR>
<TR><TH>�����и��ͳ����Хȥ�</TH>
<TD class='N'>
<u>�ɸ����줿��������λ������ޤǤ˳��������и��ͤι�פ��Ǥ�⤤$AfterName��ͥ����</u>
<BR>�����ɸ��������٤Ƥ����Ŵ�����˳��������и��ͤι�פ�Ƚ�ꤹ�롣
<BR>���������и��ͤι�פ�Ʊ��$AfterName��ʣ��������ϡ����ɥ�ǥ��ˤϤ��롣
<BR>�����⤤�и��ͤ��Ĵ������ɸ��䳫�Ŵ�������ɸ�����ǽ���ɤ���������ˤ�롣
</TD></TR>
<TR><TH>���������Хȥ�</TH>
<TD class='N'>
<u>�ɸ����줿��������λ������ޤǤ����פ�������������פ��Ǥ�⤤$AfterName��ͥ����</u>
<BR>�����ɸ��������٤Ƥ����Ŵ���������פ�������������Ƚ�ꤹ�롣
<BR>�������פ�������������Ʊ��$AfterName��ʣ��������ϡ����ɥ�ǥ��ˤϤ��롣
<BR>�������Ŵ�������ɸ�����ǽ���ɤ���������ˤ�롣
</TD></TR>
<TR><TH>�����༣�Хȥ�</TH>
<TD class='N'>
<u>�ɸ����줿��������λ������ޤǤ��ݤ������á�������ä���פ��Ǥ�⤤$AfterName��ͥ����</u>
<BR>�����ɸ��������٤Ƥ����Ŵ�������ݤ������ÿ�(+ ������ÿ�)��Ƚ�ꤹ�롣
<BR>�����ݤ������ÿ�(+ ������ÿ�)��Ʊ��$AfterName��ʣ��������ϡ����ɥ�ǥ��ˤϤ��롣
<BR>�������Ŵ�������ɸ�����ǽ���ɤ���������ˤ�롣
</TD></TR>
<TR><TH>�޶�Ԥ��Хȥ�</TH>
<TD class='N'>
<u>�ɸ����줿��������λ������ޤǤ˳��������޶���ۤ��Ǥ�⤤$AfterName��ͥ����</u>
<BR>�����ɸ��������٤Ƥ����Ŵ�����˳������������༣����������༣�ξ޶���ۤ�Ƚ�ꤹ�롣
<BR>�����޶���ۤ�Ʊ��$AfterName��ʣ��������ϡ����ɥ�ǥ��ˤϤ��롣
<BR>�������Ŵ�������ɸ�����ǽ���ɤ���������ˤ�롣
</TD></TR>
</TABLE>
���ɸ��������٤Ƥ���������ʤɤ���ͳ�ǡ���λȽ����˳���$AfterName�˴��������ʤ�����$AfterName�ϡ���̤��Ĥ��ޤ���
END

# Ʊ��
#----------------------

	my $allyDisDown = 'Ʊ��';
	if($HallyDisDown) {
		$allyDisDown = $HallyDisDown . '��';
	}
	my $allyMax = (!$HallyMax) ? '̵����' : "$HallyMax$AfterName";
	my $allyAutoBreakup = ('���ʤ�', '����', '����[�Ǽ��Ĥ���ǥ��ذܹ�]')[$HallyAutoBreakup];
	my $costMakeAlly = "$HcostMakeAlly$HunitMoney";
	1 while $costMakeAlly =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $costKeepAlly = "$HcostKeepAlly$HunitMoney";
	1 while $costKeepAlly =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$src .= <<"END";
<HR>
<a name='ally'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> Ʊ�������ƥ�</H3></a>
Ʊ���κ�������Ĥ��뤫����<B>$doStr[$HallyUse]</B><BR>
END

	$src .= <<"END" if($HallyUse);
�ҤȤĤ�Ʊ���ˤ��������Ǥ��ʤ��褦�ˤ��뤫����<B>$doStr[$HallyJoinOne]</B><BR>
������������ˤ�����餺����ϤҤȤĤ�Ʊ���ˤ��������Ǥ��ޤ���<BR>
��������ǻ���Ʊ����ưŪ�˲򻶤��뤫����<B>$allyAutoBreakup</B><BR>
���Ĥ�Ʊ���ؤβ�����ǽ����$AfterName����<B>$allyMax</B><BR>
Ʊ���˲������Ƥ�����κҳ�ȯ����Ψ���̾�����Ф�����ˡ�<B>$allyDisDown</B><BR>
�����оݤȤʤ�ҳ����Ͽ̡����ȡ���������С�������С�ʮ��<BR><BR>
Ʊ���ˤ��������ѡ��������ѹ� <B>${costMakeAlly}</B> / �ݻ��� <B>${costKeepAlly}</B><BR>
END

# �Ϸ������ޥ������
#----------------------
	$src .= <<"END";
<HR>
<a name='usecom'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �Ϸ������ޥ������</H3></a>
<TABLE><TR>
END

	# �������ϡ�ʿ�ϡ������������졤����, �������ġ��ϥ�ܥơ��ɱһ��ߡ��ߥ�������ϡ�������ϡ������顤���롤����
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'>�����Ϸ�</TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
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
	# �ԻԷ�
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#town' style='text-decoration=none'>�ԻԷ�</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
	foreach (0..$#HlandTownName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandTownImage[$_]'></TD><TH>$HlandTownName[$_]</TH></TR>";
	}
	$src .= "</TABLE></TD>";
	# ��ǰ��
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#monument' style='text-decoration=none'>��ǰ��</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
	foreach (0..$#HmonumentName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonumentImage[$_]'></TD><TH>$HmonumentName[$_]</TH></TR>";
	}
	$src .= "</TABLE></TD>";
	# ʣ���Ϸ�
	if($HuseComplex) {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#complex' style='text-decoration=none'>ʣ���Ϸ�</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
		foreach (0..$#HcomplexName) {
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$_]'></TD><TH>$HcomplexName[$_]</TH></TR>";
		}
		$src .= "</TABLE></TD>";
	}
	# ����
	if($HnavyName[0] ne '') {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#navy' style='text-decoration=none'>����</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
		foreach (0..$#HnavyName) {
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HnavyImage[$_]'></TD><TH>$HnavyName[$_]</TH></TR>";
			next if(!($HnavySpecial[$_] & 0x4));
			$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HnavyImage2[$_]'></TD><TH>$HnavyName[$_]<small>(����)</small></TH></TR>";
		}
		$src .= "</TABLE></TD>";
	}
	# ����
	$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#monster' style='text-decoration=none'>����</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
	foreach (0..$#HmonsterName) {
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImage[$_]'></TD><TH>$HmonsterName[$_]</TH></TR>";
		next if(!($HmonsterSpecial[$_] & 0x4));
		$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImage2[$_]'></TD><TH>$HmonsterName[$_]<small>(�Ų�)</small></TH></TR>";
	}
	$src .= "<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonsterImageUnderSea'></TD><TH>��������<small>(����)</small></TH></TR>";
	$src .= "</TABLE></TD>";
	# �������
	if($HhugeMonsterAppear) {
		$src .= "<TD valign='top' class='M'><TABLE><TR $HbgInfoCell><TH colspan='2'><a href='#hmonster' style='text-decoration=none'>�������</a></TH></TR><TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH></TR>";
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

	$src .= "�������Ȥ�������<B>$useStr[($HuseBouha > 0)]</B><BR>";
	if($HuseBouha) {
		$src .= "����������ͭ��ǽ����<B>$HuseBouha</B><BR>";
	}

	$src .= "�����Ȥ�������<B>$useStr[($HuseSeaMine > 0)]</B><BR>";
	if($HuseSeaMine) {
		$src .= "���������ֲ�ǽ����<B>$HuseSeaMine</B><BR>";
		$src .= "����$AfterName�ε���ǥ��᡼��������뤫����<B>$selfStr[$HmineSelfDamage]</B><BR>";
	}
	my $edgeDef = "";
	if($HedgeReclaim > 1) {
		my $edgeSize1 = $HedgeReclaim - 1;
		my $edgeSizeX = $HislandSizeX - $HedgeReclaim;
		my $edgeSizeY = $HislandSizeY - $HedgeReclaim;
		$edgeDef = "<B>${HedgeReclaim}Hex</B>";
		$edgeDef .= "(x��ɸ�ΰ�����'$edgeSize1'�ʲ���'$edgeSizeX'�ʾ������)��(y��ɸ�ΰ�����'$edgeSize1'�ʲ���'$edgeSizeY'�ʾ������)" if(!$HoceanMode);
	} elsif($HedgeReclaim) {
		my $edgeSizeX = $HislandSizeX - 1;
		my $edgeSizeY = $HislandSizeY - 1;
		$edgeDef = '<B>1Hex</B>';
		$edgeDef .= "(x��ɸ�ΰ�����'0'��'$edgeSizeX'������)��(y��ɸ�ΰ�����'0'��'$edgeSizeY'������)" if(!$HoceanMode);
	}

	$src .= <<"END";
<BR>
Ȳ�Τ򥿡������ʤ��ˤ��뤫����<B>$doStr[$HnoturnSellTree]</B><BR>
�����μ��Ϥ����Ω�ƤǤ���΢�略(�Х�?)�������뤫����<B>$doStr[$HnavyReclaim]</B><BR>
����(���ˤ���)�μ��Ϥ����Ω�ƤǤ���΢�略(�Х�?)�������뤫����<B>$doStr[$HmonsterReclaim]</B><BR>
�������ܤ����������Ǥ����������¤�Ǥ��ʤ��褦�ˤ��뤫����<B>$doStr[$HnavyBuildFlag]</B><BR>
�����ˤ��ư�ġ��ɸ��Ĥˤ��뤫����<B>$doStr[$HnavyMoveAsase]</B><BR>
$AfterName�κǳ���${edgeDef}�����Ω���ԲĤˤ��뤫����<B>$doStr[($HedgeReclaim > 0)]</B><BR>
END

	$src .= <<"END";
<BR>$AfterName�����Ѥ����줹�뤫����<B>$doStr[$HnewIslandSetting]</B><BR>
END
	$HcountLandArea = 16 if($HcountLandArea < 16);
	$HcountLandPlains = $HcountLandArea - $HcountLandWaste - $HcountLandForest - $HcountLandTown - $HcountLandMountain - $HcountLandPort;
	my $bcol = 6;
	my($bstr1, $bstr2);
	if($HuseBase) {
		$bcol++;
		$bstr1 = "<TH>${HtagTH_}���Ϥο�${H_tagTH}</TH>";
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
<TR $HbgInfoCell><TH colspan=$bcol>${HtagTH_}Φ�������${HnormalColor_}${HcountLandArea}${H_normalColor}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�����ο�${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}ʿ�Ϥο�${H_tagTH}</TH><TH>${HtagTH_}���Ϥο�${H_tagTH}</TH><TH>${HtagTH_}���ο� (�ڤο�)${H_tagTH}</TH><TH>${HtagTH_}Į�ο� (�͸�)${H_tagTH}</TH><TH>${HtagTH_}���ο� (����)${H_tagTH}</TH>$bstr1<TH>${HtagTH_}�����ο�${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$HcountLandPlains</TD><TD align='center'>$HcountLandWaste</TD><TD align='right'>${HcountLandForest} ($HvalueLandForest$HunitTree)</TD><TD align='right'>${HcountLandTown} ($valueLandTownPop)</TD><TD align='right'>${HcountLandMountain} ($valueLandMountainPop)</TD>$bstr2<TD align='center'>$HcountLandPort</TD><TD align='center'>$HcountLandSea</TD></TR>
</TABLE></B><BR>
END

# �ԻԷ�
#-------------------------
	my $tcol1 = (!$HsurvivalTurn) ? 2 : 4;
	my $tcol2 = (!$HsurvivalTurn) ? 1 : 2;
	my $trow1 = (!$HsurvivalTurn) ? 1 : 2;
	my $trow2 = (!$HsurvivalTurn) ? 2 : 3;

	$src .= <<"END";
<HR>
<a name='town'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �ԻԷ�����</H3></a>
<TABLE>
<TR $HbgInfoCell>
<TH colspan=3>${HtagTH_}�ԻԷ�${H_tagTH}</TH>
<TH colspan=$tcol1>${HtagTH_}�͸���������${H_tagTH}</TH>
<TH rowspan=$trow2>${HtagTH_}��̱<BR>����<BR>����<BR>���${H_tagTH}</TH>
<TH rowspan=$trow2>${HtagTH_}����<BR>��­��<BR>�͸�<BR>������${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=$trow1>${HtagTH_}̾��${H_tagTH}</TH>
<TH rowspan=$trow1>${HtagTH_}����${H_tagTH}</TH>
<TH colspan=$tcol2>${HtagTH_}�̾�${H_tagTH}</TH><TH colspan=$tcol2>${HtagTH_}Ͷ��${H_tagTH}</TH>
</TR>
END
	if($HsurvivalTurn) {
		$src .= "<TR $HbgInfoCell><TH>${HtagTH_}��ȯ${H_tagTH}</TH><TH>${HtagTH_}��Ʈ${H_tagTH}</TH><TH>${HtagTH_}��ȯ${H_tagTH}</TH><TH>${HtagTH_}��Ʈ${H_tagTH}</TH></TR>";
	}
	foreach $i (0..$#HlandTownName) {
		$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandTownImage[$i]'></TD><TH>$HlandTownName[$i]</TH>
END
		my $value = (!$HlandTownValue[$i]) ? '��' : "$HlandTownValue[$i]${HunitPop}�ʾ�";
		1 while $value =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$src .= "<TD align='right'>$value</TD>";
		if(!$HsurvivalTurn) {
			my $add1 = (!$Haddpop[$i]) ? '��' : "$Haddpop[$i]${HunitPop}";
			1 while $add1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add2 = (!$HaddpopPropa[$i]) ? '��' : "$HaddpopPropa[$i]${HunitPop}";
			1 while $add2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='right'>$add1</TD><TD align='right'>$add2</TD>
END
		} else {
			my $add1 = (!$HaddpopSD[$i]) ? '��' : "$HaddpopSD[$i]${HunitPop}";
			1 while $add1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add2 = (!$HaddpopSDpropa[$i]) ? '��' : "$HaddpopSDpropa[$i]${HunitPop}";
			1 while $add2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add3 = (!$HaddpopSA[$i]) ? '��' : "$HaddpopSA[$i]${HunitPop}";
			1 while $add3 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $add4 = (!$HaddpopSApropa[$i]) ? '��' : "$HaddpopSApropa[$i]${HunitPop}";
			1 while $add4 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='right'>$add1</TD><TD align='right'>$add2</TD>
<TD align='right'>$add3</TD><TD align='right'>$add4</TD>
END
		}
		my $achieve = (!$HachiveValueMax[$i]) ? '��' : "$HachiveValueMax[$i]${HunitPop}";
		1 while $achieve =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $reduction = (!$HreductionPop[$i]) ? '��' : "$HreductionPop[$i]${HunitPop}";
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
�͸��κ����͡�<B>$valueLandTownMaxPop</B><BR>
��̱��ʿ�Ϥؤμ��������¡�<B>$achivePlainsMaxPop</B>�ʼ���������Υ���<B>$achivePlainsLossPop</B>��<BR>
¼��ȯ��Ψ��<B>${HtownGlow}%</B><BR>
�������⡦�ߥ����빶��̿��������ǹӤ��Ϥˤʤ餺�Իԥ�󥯤�������褦�ˤ��뤫����<B>$doStr[$HtownStepDown]</B><BR>
������󥯣��ޤǡ�$HlandTownName[0]��$HlandTownName[1]�ˤϰ����˲�����ޤ����ޤ����˲��Ϥ˱����ƥ�󥯤�������ޤ���
END

# ʣ���Ϸ�
#-------------------------

		$src .= <<"END";
<HR>
<a name='complex'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ʣ���Ϸ�</H3></a>
ʣ���Ϸ���Ȥ�������<B>$useStr[$HuseComplex]</B><BR>
END
	if($HuseComplex) {
		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}ʣ��<BR>�Ϸ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}̾��${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}��ͭ<BR>��ǽ<BR>���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}���ֲ�ǽ�Ϸ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ﳲ����<BR>/�˲���1${H_tagTH}</TH>
<TH colspan=15>${HtagTH_}�˲����줿�����Ϸ�${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}��Ω${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH>
<TH>${HtagTH_}�Ͽ�${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�к�${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}˽ư${H_tagTH}</TH>
<TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}ʮ��${H_tagTH}</TH><TH>${HtagTH_}���${H_tagTH}</TH><TH>${HtagTH_}����<BR>��${H_tagTH}</TH><TH>${HtagTH_}����<BR>��${H_tagTH}</TH>
<TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}��ư${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HcomplexName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH>
END
			if($HcomplexMax[$i]) {
				$src .= "<TD align='right'>$HcomplexMax[$i]</TD>";
			} else {
				$src .= "<TD align='right'>��</TD>";
			}

			$src .= "<TD class='N'>";
			foreach (@{$HcomplexBefore[$i]}) {
				my $lkind = $_->[0];
				my $lvmin = $_->[1];
				my $lvmax = $_->[2];
				my $lname1 = landName($lkind, $lvmin);
				my $lname2 = landName($lkind, $lvmax);
				if($lname1 eq $lname2) {
					$src .= "<span class='check'>$lname1��</span>";
				} else {
					my @set = @{$HlandName[$lkind]};
					my $lname = ($set[0] ne '') ? $set[0] : $HlandName[$lkind];
					$src .= "<span class='check'>$lname($lname1��$lname2)��</span>";
				}
			}
			foreach (@{$HcomplexBefore2[$i]}) {
				my $lname = $HcomplexName[$_];
				$src .= "<span class='check'>$lname��</span>";
			}
			$src .= "</TD><TD align='center'>";
			my $down = $HcomplexAfter[$i]->{'stepdown'};
			if($down) {
				$src .= $down . '���';
			} elsif(defined $HcomplexAfter[$i]->{'attack'}[0]) {
				$src .= "���ǲ���";
			} else {
				$src .= "��";
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
					$src .= "<TD align='center'>��</TD>";
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
				$src .= "<TD align='center'>��</TD>";
			}
			$src .= "</TR>";
		}

		$src .= <<"END";
</TABLE>
�������ﳲ����/�˲���1�פϡ�����ͤε��ϡ��ɲ��ͤε��Ϥ򤽤줾�죱��󥯤ȥ�����Ȥ��ơ����������Ȥ���ﳲ���������ͤǤ���
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}ʣ��<BR>�Ϸ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}̾��${H_tagTH}</TH>
<TH colspan=11>${HtagTH_}°��${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}����<BR>��¼<BR>ȯ��${H_tagTH}</TH><TH>${HtagTH_}�к�<BR>�ﳲ<BR>�ɻ�${H_tagTH}</TH><TH>${HtagTH_}����<BR>�ﳲ<BR>�ɻ�${H_tagTH}</TH>
<TH>${HtagTH_}�Ͼ�<BR>ȯ��${H_tagTH}</TH><TH>${HtagTH_}�ߥ�<br>����<br>�ɱ�${H_tagTH}</TH><TH>${HtagTH_}����<br>����<br>�ɱ�${H_tagTH}</TH>
<TH>${HtagTH_}����<BR>����<BR>�о�${H_tagTH}</TH><TH>${HtagTH_}�д�<BR>����<BR>�о�${H_tagTH}</TH><TH>${HtagTH_}����<BR>����<BR>�о�${H_tagTH}</TH>
<TH>${HtagTH_}���<BR>����<BR>����${H_tagTH}</TH><TH>${HtagTH_}���<BR>����<BR>����${H_tagTH}</TH>
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
<TH rowspan=2>${HtagTH_}ʣ��<BR>�Ϸ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}̾��${H_tagTH}</TH>
<TH colspan=5>${HtagTH_}������ե饰${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}�����ե饰${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}���ե饰${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}�û�<BR>�о�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH><TH>${HtagTH_}�Ѹ�${H_tagTH}</TH>
<TH>${HtagTH_}�û�<BR>�о�${H_tagTH}</TH><TH>${HtagTH_}�����${H_tagTH}</TH><TH>${HtagTH_}�ɲ���${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH>
<TH>${HtagTH_}�û�<BR>�о�${H_tagTH}</TH><TH>${HtagTH_}�����${H_tagTH}</TH><TH>${HtagTH_}�ɲ���${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH>
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
				$tkind = ($HcomplexTPkind[$i] eq '') ? '��' : $rankKind{$HcomplexTPkind[$i]};
				$trate = $HcomplexTPrate[$i] . $HcomplexTPunit[$i];
				$turnmax[$i]  = $HcomplexTPCmax[$i] * $HcomplexTPrate[$i];
				$tmax  = $turnmax[$i] . $HcomplexTPunit[$i];
				$thide = $hide[$HcomplexTPhide[$i]];
			} else {
				$tname = '��';
				$tkind = '��';
				$trate = '��';
				$tmax  = '��';
				$thide = '��';
			}
			my($fkind, $fbase, $fplus, $fmax, $mkind, $mbase, $mplus, $mmax);
			$foodmax[$i]  = $HcomplexFPCmax[$i]*$HcomplexFPplus[$i]+$HcomplexFPbase[$i];
			$moneymax[$i]  = $HcomplexMPCmax[$i]*$HcomplexMPplus[$i]+$HcomplexMPbase[$i];
			if($foodmax[$i]) {
				$fkind = $rankKind{$HcomplexFPkind[$i]};
				$fmax  = $foodmax[$i] . "0${HunitPop}����";
				1 while $fmax =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$fbase = $HcomplexFPbase[$i] . "0${HunitPop}����";
				1 while $fbase =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$fplus = $HcomplexFPplus[$i] . "0${HunitPop}����";
				1 while $fplus =~ s/(.*\d)(\d\d\d)/$1,$2/;
			} else {
				$fkind = '��';
				$fmax  = '��';
				$fbase = '��';
				$fplus = '��';
			}
			if($moneymax[$i]) {
				$mkind = $rankKind{$HcomplexMPkind[$i]};
				$mmax  = $moneymax[$i] . "0${HunitPop}����";
				1 while $mmax =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mbase = $HcomplexMPbase[$i] . "0${HunitPop}����";
				1 while $mbase =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mplus = $HcomplexMPplus[$i] . "0${HunitPop}����";
				1 while $mplus =~ s/(.*\d)(\d\d\d)/$1,$2/;
			} else {
				$mkind = '��';
				$mmax  = '��';
				$mbase = '��';
				$mplus = '��';
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
<TABLE><TR $HbgInfoCell><TH colspan=$col>${HtagTH_}�ե饰�ͤˤ��ȯŸ����ʣ���Ϸ�${H_tagTH}</TH></TR><TR>
END
			my $rankflag  = { 'turn'=>'������ե饰', 'food'=>'�����ե饰', 'money'=>'���ե饰' };
			foreach $i (@rankup) {
				$src .= <<"END";
<TD class='M'><TABLE>
<TR $HbgInfoCell><TH>${HtagTH_}�Ϸ�${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH><TH>${HtagTH_}�оݥե饰${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HcomplexImage[$i]'></TD><TH>$HcomplexName[$i]</TH><TH>$rankflag->{"$HcomplexLevelKind[$i]"}</TH>
END
				my $maxflag = ($HcomplexLevelKind[$i] eq 'turn') ? $turnmax[$i] : ($HcomplexLevelKind[$i] eq 'food') ? $foodmax[$i] : $moneymax[$i];
				my($cflag);
				foreach (0..$#{$HcomplexLevelValue[$i]}) {
					$cflag = $HcomplexLevelValue[$i][$_];
					if($cflag) {
						$cflag .= "0${HunitPop}����" if($HcomplexLevelKind[$i] ne 'turn');
						$cflag .= "�ʾ�" if($HcomplexLevelValue[$i][$_] < $maxflag);
						1 while $cflag =~ s/(.*\d)(\d\d\d)/$1,$2/;
					} else {
						$cflag = '��';
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
����ȯŸ���Ƥ⳰�Ѥ�̾�Τ��Ѳ���������ǡ��ºݤε�ǽ���ä��Ѳ��Ϥ���ޤ���
<BR>
END
		}
		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell>
<TH colspan=4>${HtagTH_}ʣ���Ϸ���ȯ���ޥ�ɡ�����${turnStr[1]}��${H_tagComName}<small>���������񤹤�</small>��${turnStr[0]}��${H_tagComName}<small>���������񤷤ʤ�</small>${H_tagTH}</TH>
<TH colspan=4>${HtagTH_}�оݥե饰${H_tagTH}</TH><TH colspan=3>${HtagTH_}������ե饰�ꥻ�åȻ�${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}̾��${H_tagTH}</TH><TH>${HtagTH_}�о��Ϸ�${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH>
<TH>${HtagTH_}���֤Τ�${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}���${H_tagTH}</TH>
<TH>${HtagTH_}�����о�${H_tagTH}</TH><TH>${HtagTH_}�ե饰<BR>����Ψ${H_tagTH}</TH><TH>${HtagTH_}������<BR>���Ϸ�${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HcomplexComName) {
			my $cost = (!$HcomplexComCost[$i]) ? '̵��' : "$HcomplexComCost[$i]$HunitMoney";
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
				$lname  = '��';
				$kind   = '��';
				$ratio  = '��';
			}

			$src .= <<"END";
<TD align='center'>$ox[!$bonly]</TD><TD align='center'>$ox[!$turn]</TD><TD align='center'>$ox[!$food]</TD><TD align='center'>$ox[!$money]</TD>
<TD align='center'>$kind</TD><TD align='right'>$ratio</TD><TD align='center'>$lname</TD>
</TR>
END

		}
		$src .= "</TABLE>";
	}

# ����
#-------------------------

	$src .= <<"END";
<HR>
<a name='core'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ����</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan='2'>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�����Ϸ��ʤ�${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][0]'></TD><TH>$HlandName[$HlandCore][0]</TH>
<TD align='left'>
<!--- ���� --->
��ʿ�Ϥ����֡����ϡ����郎��ǽ��<BR>
����С�ʮ�С����������������ﳲ(2Hex)���˲�����롣
</TD></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][1]'></TD><TH>$HlandName[$HlandCore][1]</TH>
<TD align='left'>
<!--- ���女�� --->
�����������֡���Ω�����郎��ǽ��<BR>
����С�ʮ�С������ﳲ(2Hex)���˲�����롣
</TD></TR>
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HlandImage[$HlandCore][2]'></TD><TH>$HlandName[$HlandCore][2]</TH>
<TD align='left'>
<!--- ���쥳�� --->
���������֡���Ω����ǽ��<BR>
����С�ʮ�С������ﳲ(1Hex)���˲�����롣
</TD></TR>
</TABLE></TD>
���ߥ��ޥ�ɤ�Ȥ�������<B>$useStr[$HuseCore]</B>
END

	if($HuseCore && $HuseCoreLimit) {
		$src .= "��(�����ߤǤ���ΤϿ�����Ͽ���줿$AfterName��<B>��ȯ���֤���</B>�Ǥ�)";
	}
	my $coremax = (!$HcoreMax) ? '̵����' : $HcoreMax;
	my $durablec;
	if($HdurableCore){
		$durablec = "<B>����$HdurableCore�ޤǥ��å�</B>";
	} else {
		$durablec = "<B>�ʤ�</B>(�̾�)";
	}
	my $hidec = '';
	$hidec = "($HlandName[$HlandCore][0] => <B>��</B>��$HlandName[$HlandCore][1]��$HlandName[$HlandCore][2] => <B>��</B>)" if($HcoreHide);
	my @coreless = ('���פ��ʤ�', '���פ���', '����Ƚ�����ǽȯư');
	$src .= <<"END";
<BR><BR>
��ͭ��ǽ�������<B>$coremax</B><BR>
�������ѵ������ꡩ��$durablec<BR>
�����������뤫����<B>$doStr[$HcoreHide]</B>��$hidec<BR><BR>
��������ͭ���ʤ�������פ��롩��<B>$coreless[$HcorelessDead]</B>��(������ˤ�����餺��������Ͽ���줿$AfterName��<B>��ȯ���֤����פ��ޤ���</B>��)<BR>
END

# ����
#-------------------------

		$src .= <<"END";
<HR>
<a name='navy'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ����</H3></a>
END
	if($HnavyName[0] eq '') {
		$src .= "������<B>����ޤ���</B><BR>";
	} else {
#		$src .= "����(��������Ӵ���)�ηи��ͤκ����͡�<B>$HmaxExpNavy</B><BR>";
#		$src .= "<TABLE><TR $HbgInfoCell><TH>�����Υ�٥�</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>��٥�UP��ɬ�פʷи���</TH><TD align='center'>0</TD>";
#		foreach (@navyLevelUp) {
#			$src .= "<TD align='center'>$_</TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>������</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'>+$HnavyFirePlus[int($_/2)]</TD>";
#		}
#		$src .= "</TR><TR $HbgInfoCell><TH>�ѵ���</TH>";
#		foreach (1..$maxNavyLevel) {
#			$src .= "<TD align='center'>+$HnavyMaxHpPlus[int(($_ - 1)/2)]</TD>";
#		}
		$src .= "</TR></TABLE>";

		$src .= <<"END";
�ĳ���ѻ��˶����ȯ��������Ψ��<B>${HnavyProbWreckGold}%</B><BR>
¾$AfterName���ɸ���δ������뤹�뤫����<B>$doStr[$HnavySupplyFlag]</B>�����������꤬�֤��ʤ��פξ������ǽ�ϡפ�̵ͭ����̣������ޤ���<BR><BR>
END

		my $priList;
		my $pFlag = 0;
		foreach (@HpriStr) {
			$priList .= "��" if($pFlag);
			$pFlag++;
			$priList .= $_;
		}
		my $navyMaximum = (!$HnavyMaximum ? '̵����' : "$HnavyMaximum");
		my $fleetMaximum = (!$HfleetMaximum ? '̵����' : "$HfleetMaximum");
		my $portRetention1 = (!$HportRetention ? '���������ˤ��<B>���¤ʤ�</B>' : "�����������ˤĤ�<B>$HportRetention</B>�ޤ�");
		my $portRetention2 = (!$HportRetention ? '̵����' : "$HportRetention");
		my $nCol = 3;
		$nCol++ if($HmaxComNavyLevel);
		$src .= <<"END";
�ְ��ƹ���ץ��ޥ�ɤ�Ȥ�������<B>$useStr[$HuseTarget]</B><BR><BR>
��$AfterName�ʳ��ˤ��������ѵ��Ϥ�ɽ�����뤫����<B>$doStr[$HnavyShowInfo]</B><BR>
���⤷���������Ȥ������ϰϤˤ����硢����(����)���뤳�Ȥ⤢��褦�ˤ��뤫����<B>$anStr[$HnavySelfAttack]</B><BR>
<BR>������������Ƥ����������Ϸ�����$AfterName�ξ�硢̵���ˤ��뤫����<B>$saftyStr[$HnavySafetyZone]</B><BR>
��̵������̵���ˤʤ��Ψ��<B>${HnavySafetyInvalidp}%</B>(̵������ǽ��ȯư������̤�Ƚ��)<BR>
<BR>��������Ϸ��ˤ�빶���ͥ����(�ǥե����)��<B>$priList</B>(${nearfar[$Hnearfar]})</B><BR>
<BR>��ͭ��ǽ��������<B>$navyMaximum</B>��(�����⤢���� <B>$fleetMaximum</B>$portRetention1)
�ǰ�ǽ�ϤΤ���������ɸ�����Ƥ��ʤ�$AfterName�ؤϱ�����ޥ�ɤ��Ȥ��ʤ����롩��<B>$doStr[$HtradeAbility]</B><BR>
<BR>
��°�����δ������и����뤫����<B>$doStr[$HnavyUnknown]</B><BR>
END

		if($HnavyUnknown) {
			$HdisNavy *= 0.01;# ��°��������
			$HdisNavyBF *= 0.01;# ��°��������(Battle Field)
			$HdisNavyBF    = $HdisNavy*2 if(!$HdisNavyBF);
			$src .= "ñ�����Ѥ�����δ����и�Ψ��<B>${HdisNavy}%</B>���ʥХȥ�ե�����ɡ�<B>${HdisNavyBF}%</B>��<BR>";
		}

		$src .= <<"END";
<TABLE>
<TR $HbgInfoCell><TH colspan='$nCol'>${HtagTH_}����${H_tagTH}</TH>
END

		$src .= "<TH rowspan=2>${HtagTH_}��°<br>������<br>�и��͸�<br>(��Ψ)${H_tagTH}</TH>" if($HnavyUnknown);

		$src .= <<"END";
<TH>${HtagTH_}��ͭ��ǽ���${H_tagTH}</TH><TH colspan=2>${HtagTH_}�ѵ���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�˲�<br>��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����<br>��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����<br>�ϰ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����<br>�ϰ�${H_tagTH}</TH><TH colspan=2>${HtagTH_}�и���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}��¤<br>����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����<br>��ȯ<br>��<br>����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ݻ�<br>����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ݻ�<br>����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}��³<br>������${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ĳ�<br>��Ψ${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}��$AfterName${H_tagTH}</TH><TH>${HtagTH_}¾$AfterName${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH>
END

		$src .= "<TH>${HtagTH_}��¤<br>��٥�${H_tagTH}</TH>" if($HmaxComNavyLevel);

		$src .= <<"END";
<TD align='center'>������:$fleetMaximum<BR>$portRetention2/1��<BR>���:$navyMaximum</TD>
<TH>${HtagTH_}���${H_tagTH}</TH><TH>${HtagTH_}�ǽ�${H_tagTH}</TH>
<TH>${HtagTH_}����<br>��${H_tagTH}</TH><TH>${HtagTH_}��¤<br>��${H_tagTH}</TH>
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
				$level = '��';
			}
			if($level == 1) {
				$exp = 0;
			} elsif($level ne '��') {
				$exp = $HcomNavyBorder[$level-2];
			} else {
				$exp = '����';
				$bExp = '��';
			}
			$src .= "<TD align='center'><B>${level}</B><BR>(${exp})</TD>" if($HmaxComNavyLevel);
			if($HnavyUnknown) {
				my $unknownpop = ($HdisNavyBorder[$i]) ? $HdisNavyBorder[$i] . $HunitPop : '��';
				1 while $unknownpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
				my $unknownratio = $HdisNavyRatio[$i];
				$src .= "<TD align='right'>$unknownpop<BR>(${unknownratio})</TD>";
			}
			my $kindMax = (!$HnavyKindMax[$i]) ? '̵����' : $HnavyKindMax[$i];
			my $damage = $HnavyDamage[$i];
			$damage = 1 if(!$damage);
			my $nCost = (!$HnavyCost[$i]) ? "��" : ($HnavyCost[$i] > 0 ? "$HnavyCost[$i]$HunitMoney" : "<DIV class='Money' align=left>����</DIV>" . - $HnavyCost[$i] . "$HunitMoney");
			1 while $nCost =~ s/(.*\d)(\d\d\d)/$1,$2/;
#���β�
			my $nBuild = (!$HnavyBuildTurn[$i]) ? "��" : ($HnavyBuildTurn[$i] > 0 ? "$HnavyBuildTurn[$i]������" : "<DIV class='Money' align=left></DIV>" . - $HnavyBuildTurn[$i] . "������");
			1 while $nBuild =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $sCost = (!$HnavyShellCost[$i]) ? "��" : ($HnavyShellCost[$i] > 0 ? "$HnavyShellCost[$i]$HunitMoney" : "<DIV class='Money' align=left>����</DIV>" . - $HnavyShellCost[$i] . "$HunitMoney");
			1 while $sCost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $nMoney = (!$HnavyMoney[$i]) ? "��" : ($HnavyMoney[$i] > 0 ? "$HnavyMoney[$i]$HunitMoney" : "<DIV class='Money' align=left>����</DIV>" . - $HnavyMoney[$i] . "$HunitMoney");
			1 while $nMoney =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $nFood = (!$HnavyFood[$i]) ? "��" : ($HnavyFood[$i] > 0 ? "$HnavyFood[$i]$HunitFood" : "<DIV class='Food' align=left>����</DIV>" . - $HnavyFood[$i] . "$HunitFood");
			1 while $nFood =~ s/(.*\d)(\d\d\d)/$1,$2/;
#���β�
			my $nCruise = (!$HnavyCruiseTurn[$i]) ? "��" : ($HnavyCruiseTurn[$i] > 0 ? "$HnavyCruiseTurn[$i]������" : "<DIV class='Food' align=left>����</DIV>" . - $HnavyCruiseTurn[$i] . "������");
			1 while $nCruise =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$src .= <<"END";
<TD align='center'>$kindMax</TD><TD align='right'>$HnavyHP[$i]</TD><TD align='right'>$HnavyMaxHP[$i]</TD><TD align='right'>$damage</TD><TD align='right'>$HnavyFire[$i]</TD><TD align='right'>$HnavyFireHex[$i]</TD><TD align='right'>$HnavyFireRange[$i]</TD><TD align='right'>$HnavyExp[$i]</TD><TD align='right'>$bExp</TD>
<TD align='right'>$nCost</TD><TD align='right'>$nBuild</TD><TD align='right'>$sCost</TD><TD align='right'>$nMoney</TD><TD align='right'>$nFood</TD><TD align='right'>$nCruise</TD><TD align='right'>$HnavyProbWreck[$i]%</TD>
</TR>
END
		}

		$src .= "</TABLE>";
		if($HmaxComNavyLevel) {
			$src .= "�����֥�٥�פΥ��å���Ϸ�¤��ɬ�פʡ�������и��͡�";
			$src .= "(��¤�ˤϡ�<B>�����Υ�٥���¤��٥��Ʊ�����ͤ�ɬ��</B>�ˤʤ�ޤ�)" if($HmaxComPortLevel);
		}

		$src .= <<"END";
<BR><TABLE>
<TR $HbgInfoCell><TH colspan=3>${HtagTH_}����${H_tagTH}</TH>
<TH colspan=26>${HtagTH_}ǽ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}��$AfterName${H_tagTH}</TH><TH>${HtagTH_}¾$AfterName${H_tagTH}</TH><TH>${HtagTH_}̾��${H_tagTH}</TH>
<TH>${HtagTH_}��ư<br>��<br>®��${H_tagTH}</TH><TH>${HtagTH_}��ư��<br>�ȤƤ�<br>®��${H_tagTH}</TH><TH>${HtagTH_}���夹��<br>(���Ψ)${H_tagTH}</TH><TH>${HtagTH_}����<BR>����${H_tagTH}</TH>
<TH>${HtagTH_}���<br>��ư${H_tagTH}</TH><TH>${HtagTH_}�ߥ�<br>����<br>�ɱ�${H_tagTH}</TH><TH>${HtagTH_}����<br>����<br>�ɱ�${H_tagTH}</TH><TH>${HtagTH_}��ư<BR>���<BR>(����)${H_tagTH}</TH>
<TH>${HtagTH_}����<br>����${H_tagTH}</TH><TH>${HtagTH_}�д�<br>����${H_tagTH}</TH><TH>${HtagTH_}����<br>����${H_tagTH}</TH><TH>${HtagTH_}�ж�<br>����${H_tagTH}</TH>
<TH>${HtagTH_}�����<BR>������${H_tagTH}</TH><TH>${HtagTH_}��ˤ��${H_tagTH}</TH><TH>${HtagTH_}�дϷ�${H_tagTH}</TH><TH>${HtagTH_}�ж���${H_tagTH}</TH>
<TH>${HtagTH_}���<br>ǽ��${H_tagTH}</TH><TH>${HtagTH_}�ǰ�<br>ǽ��${H_tagTH}</TH><TH>${HtagTH_}��±<br>ǽ��${H_tagTH}</TH><TH>${HtagTH_}Φ��<br>����<br>ǽ��${H_tagTH}</TH>
<TH>${HtagTH_}��ɸ<br>����${H_tagTH}</TH><TH>${HtagTH_}����<br>����${H_tagTH}</TH><TH>${HtagTH_}̿��<br>ΨUP${H_tagTH}</TH><TH>${HtagTH_}����<br>ǽ��${H_tagTH}</TH>
<TH>${HtagTH_}�˲���<br>������<br>max(Ψ)${H_tagTH}</TH><TH>${HtagTH_}���<br>����${H_tagTH}</TH>
</TR>
END

		foreach $i (0..$#HnavyName) {
			$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><span class='myFleetCell'><img src='${HimageDir}/$HnavyImage[$i]' class='myFleet'></span></TD><TD align='right'><img src='${HimageDir}/$HnavyImage[$i]'></TD><TH>$HnavyName[$i]</TH>
END

			my $submarineSurface = ($HnavySpecial[$i] & 0x4) ? $HsubmarineSurface[$i] . '%' : '';
			my @fireName = ([($HnavyFireName[$i][0] ne '' ? $HnavyFireName[$i][0] : '����ȯ��'),'��'], [($HnavyFireName[$i][1] ne '' ? $HnavyFireName[$i][1] : '��ˤ�ͷ�'),'��'], [($HnavyFireName[$i][2] ne '' ? $HnavyFireName[$i][2] : '�дϹ���'),'��'], [($HnavyFireName[$i][3] ne '' ? $HnavyFireName[$i][3] : '�ж��ͷ�'),'��']);
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
		$src .= "�����ֳ���õ��ǽ�ϡפϡ���ư�Τ��Ӥ�Ĵ�����Ѥ�������ޤ���(�ݻ���˷׾夵��ޤ�)<BR>";
		$src .= "��������������פϡ��ѵ��Ϥ˴ط��ʤ������Ȥ����פ���ǽ�ϤǤ���";
		if($HnavySafetyZone == 2) {
			$src .= "�������������ͧ����δ����ˤ�̵���Ǥ���<BR>";
		} elsif($HnavySafetyZone == 1) {
			$src .= "������������δ���������̵���Ǥ���<BR>";
		} else {
			$src .= "���Ȥ�������δ����Ǥ��äƤ����������ͭ���Ǥ���<BR>";
		}
		if($HsuicideAbility) {
			$src .= "���������ϡ���ư��Ĥ򤷤ʤ��Ƥ��ư���˿ʹ������˴���������о�����������ꤷ�ޤ���<BR>";
		} else {
			$src .= "���������ϡ���ư��Ĥ򤷤ʤ�����������ꤷ�ޤ���<BR>";
		}
		$src .= "�������˲��ϥ�����פϡ�Ψ�γ��������ȯ������max�����ꤵ�줿���ͤ�����ͤȤ����˲��Ϥ��Ѳ����ޤ��������ȯ�����ʤ�����̾���˲��ϤǤ���<BR>";
		$src .= "�������������פϡ����Ƥ��������μ���(����Hex)�ˤޤ�٤�ʤ����Ƥ��ޤ������������������Hex��­��ʤ������������ߤˤʤ�ޤ���<BR>";
	}

# �ɱһ��ߡ�����
#-------------------------

	my $dbMax = (!$HdBaseMax) ? '̵����' : $HdBaseMax . '��';
	my $durable;
	if($HdurableDef){
		$durable = "<B>����$HdurableDef�ޤǥ��å�</B>(�����Ͽ��̡�$HdefExplosion�פ���ꤷ���ɲ÷���)";
	} else {
		$durable = "<B>�ʤ�</B>(�̾�)";
	}
	my $defLevelUp = '';
	$defLevelUp = "���ѵ��Ϥ�<B>$HdefLevelUp�ʾ�</B>�Ƕ����ɱһ���(�ɱ��ϰϼ���3Hex)�ˤʤ�"if($HdefLevelUp);
	$src .= <<"END";
<HR>
<a name='def'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �ɱһ���</H3></a>
�ɱһ��ߤ���ͭ��ǽ�������<B>$dbMax</B><BR>
�ɱһ��ߤ��ѵ������ꡩ��$durable��$defLevelUp<BR>
�ɱһ��ߤϡ����ä�Ƨ�ޤ줿���������뤫����<B>$doStr[$HdBaseAuto]</B><BR>
�ɱһ��ߤ򡢿��˵������뤫����<B>$doStr[$HdBaseHide]</B><BR>
��$AfterName�ι���ϼ�$AfterName���ɱҷ�(¾$AfterName���ɱҷ��Ǥʤ�����)�����ƤǤ���褦�ˤ��뤫��
<BR>���������⡧<B>$nodefStr[$HdBaseSelfNoDefenceNV]</B>���ߥ����빶�⡧<B>$nodefStr[$HdBaseSelfNoDefenceMS]</B>�����äΥߥ����빶�⡧<B>$nodefStr[$HdBaseSelfNoDefenceMA]</B><BR>
END

# ���ϡ��ߥ�����
#-------------------------
	$src .= <<"END";
<HR>
<a name='base'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ���ϡ��ߥ�����</H3></a>
�ߥ�������Ϥ�Ȥ�������<B>$useStr[$HuseBase]</B><BR>
������Ϥ�Ȥ�������<B>$useStr[$HuseSbase]</B><BR>
END

	if($HuseBase || $HuseSbase) {
		$src .= <<"END";
<BR>
���Ϥηи��ͤκ����͡�<B>$HmaxExpPoint</B><BR>
END

		$src .= "<TABLE><TR><TD class='M'>";
		$src .= "<TABLE><TR $HbgInfoCell><TH>�ߥ�������ϤΥ�٥�</TH>";
		foreach (1..$maxBaseLevel) {
			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
		}
		$src .= "</TR><TR $HbgInfoCell><TH>��٥�UP��ɬ�פʷи���</TH><TD align='center'>0</TD>";
		foreach (@baseLevelUp) {
			$src .= "<TD align='center'>$_</TD>";
		}
		$src .= "</TR></TABLE>";
		$src .= "</TD><TD class='M'>";
		$src .= "<TABLE><TR $HbgInfoCell><TH>������ϤΥ�٥�</TH>";
		foreach (1..$maxSBaseLevel) {
			$src .= "<TD align='center'><B>&nbsp;$_&nbsp;</B></TD>";
		}
		$src .= "</TR><TR $HbgInfoCell><TH>��٥�UP��ɬ�פʷи���</TH><TD align='center'>0</TD>";
		foreach (@sBaseLevelUp) {
			$src .= "<TD align='center'>$_</TD>";
		}
		$src .= "</TR></TABLE>";
		$src .= "</TD></TR></TABLE>";
		$src .= <<"END";
<BR>
ST�ߥ������Ȥ�������<B>$useStr[$HuseMissileST]</B><BR>
<BR>
������˲��á�������ä����ʤ���С��ߥ������ȯ�ͤ���ߤ��뤫����<B>$doStr[$HtargetMonster]</B><BR>
�ߥ���������Ƥ����������Ϸ�����$AfterName�ξ�硢̵���ˤ��뤫����<B>$saftyStr[$HmissileSafetyZone]</B><BR>
��̵������̵���ˤʤ��Ψ��<B>${HmissileSafetyInvalidp}%</B>(̵������ǽ��ȯư������̤�Ƚ��)<BR>
END

		$src .= <<"END";
<TABLE><TR $HbgInfoCell>
<TH rowspan='2'>${HtagTH_}�ߥ�����̾��${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}����${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}������<BR>����${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}�˲���${H_tagTH}</TH><TH rowspan='2'>${HtagTH_}��${H_tagTH}</TH>
<TH colspan='5'>${HtagTH_}°��${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}�ӣ�${H_tagTH}</TH><TH>${HtagTH_}Φ��${H_tagTH}</TH><TH>${HtagTH_}���<br>����${H_tagTH}</TH>
<TH>${HtagTH_}�Ų�<br>̵��${H_tagTH}</TH><TH>${HtagTH_}����<br>̵��${H_tagTH}</TH>
</TR>
END
		foreach $i (0..$#HmissileName) {
			next if ($STcheck{$HcomMissile[$i]} && (!$HuseMissileST || $Htournament));
			$src .= <<"END";
<TR $HbgInfoCell><TH>$HmissileName[$i]</TH>
END
			my $mCost = (!$HmissileCost[$i]) ? "��" : "$HmissileCost[$i]$HunitMoney";
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
		$src .= "�������������פϡ����Ƥ��������μ���(����Hex)�ˤޤ�٤�ʤ����Ƥ��ޤ��������������Ϥ��Ȥι���Ǥ��뤿�ᡤ1�Ĥδ��ϤǤι������Hex��­��ʤ������������ߤˤʤ�ޤ���<BR>";
	}
# ŷ��
#-------------------------

	$src .= <<"END";
<HR>
<a name='weather'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ŷ��</H3></a>
ŷ����Ȥ�������<B>$useStr[$HuseWeather]</B><BR>
END


	$src .= <<"END" if($HuseWeather);
<TABLE>
<TR $HbgInfoCell><TH colspan=4>${HtagTH_}��������${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>����</TH><TD align='center'>-10�� �� 40��</TD><TD>0��ʲ��ˤʤ�ȼ����̤�Ⱦ����</TD></TR>
<TR $HbgInfoCell><TH>����</TH><TD align='center'>900hPa �� 1,100hPa</TD><TD>950hPa�ʲ�������ȯ����Ψ��10�ܡ��Ѳ����㤷��������®�˱ƶ���</TD></TR>
<TR $HbgInfoCell><TH>����</TH><TD align='center'>0% �� 100%</TD><TD>���פ˱ƶ���ڤܤ���</TD></TR>
<TR $HbgInfoCell><TH>��®</TH><TD align='center'>0m/s �� 50m/s</TD><TD>20m/s�ʾ�������γ�Ψ�徺��40m/s�ʾ�����Ȥγ�Ψ�徺�����Ϥ˱ƶ���</TD></TR>
<TR $HbgInfoCell><TH>����</TH><TD align='center'>0 �� 100</TD><TD>90�ʾ�����������γ�Ψ�徺��100����������ȯ����(Φ�����Ѥ��³���Ķ���Ƥ��ʤ����ȯ�����ޤ���)</TD></TR>
<TR $HbgInfoCell><TH>����</TH><TD align='center'>0 �� 100</TD><TD>90�ʾ�����Ȥγ�Ψ�徺��100������ȯ����</TD></TR>
</TABLE>
<TABLE>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=3>${HtagTH_}$HweatherName[0]${H_tagTH}</TH>
<TH rowspan=3>${HtagTH_}��Ψ${H_tagTH}</TH>
<TH colspan=3>${HtagTH_}���٥��${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}�����Ѳ�${H_tagTH}</TH>
<TH>${HtagTH_}�����Ѳ�${H_tagTH}</TH>
<TH>${HtagTH_}�����Ѳ�${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell>
<TD align='center'>��$HrKion</TD>
<TD align='center'>��$HrKiatu</TD>
<TD align='center'>��$HrSitudo</TD>
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
				$wt[$j] = ($wt[$j] == -8 || !$wt[$j]) ? '��' : $wt[$j]*$HweatherSpecialRatio[$j];
				$wt[$j] = ($wt[$j] > 0) ? "<FONT color=blue>+$wt[$j]</FONT>" : "<FONT color=red>$wt[$j]</FONT>";
				$src .= "<TD align='right'>$wt[$j]</TD>";
				$HweatherSpecial[$i] >>= 4;
			}
			$src .= "</TR>";
		}
		$src .= "</TABLE><BR>";
	}

# �ҳ�
#-------------------------

	$HdisEarthquake *= 0.1; # �Ͽ�
	$HdisTsunami    *= 0.1; # ����
	$HdisTyphoon    *= 0.1; # ����
	$HdisMeteo      *= 0.1; # ���
	$HdisHugeMeteo  *= 0.1; # �������
	$HdisEruption   *= 0.1; # ʮ��
	$HdisFire       *= 0.1; # �к�
	$HdisMaizo      *= 0.1; # ��¢��
	$HdisFalldown   *= 0.1; # ��������
	$HdisMonster    *= 0.01;# ����
	$HdisMonsterBF  *= 0.01;# ����(Battle Field)
	$HdisHuge       *= 0.01;# �������
	$HdisHugeBF     *= 0.01;# �������(Battle Field)
	$HdisMonsterBF = $HdisMonster*2 if(!$HdisMonsterBF);
	$HdisHugeBF    = $HdisHuge*2 if(!$HdisHugeBF);

	$src .= <<"END";
<HR>
<a name='disaster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �ҳ�</H3></a>
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}�Ͽ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�������${H_tagTH}</TH><TH rowspan=2>${HtagTH_}ʮ��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�к�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}��¢��${H_tagTH}</TH><TH colspan=2>${HtagTH_}��������${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}�����³��ι���${H_tagTH}</TH><TH>${HtagTH_}Ķ�������γ�Ψ${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'>${HdisEarthquake}%</TD><TD align='right'>${HdisTsunami}%</TD><TD align='right'>${HdisTyphoon}%</TD><TD align='right'>${HdisMeteo}%</TD><TD align='right'>${HdisHugeMeteo}%</TD><TD align='right'>${HdisEruption}%</TD><TD align='right'>${HdisFire}%</TD><TD align='right'>${HdisMaizo}%</TD><TD align='right'>$HdisFallBorder$HunitArea(${HdisFallBorder}Hex)</TD><TD align='right'>${HdisFalldown}%</TD></TR>
</TABLE>
���Ȥ�������Ϳ������᡼���κ����͡�<B>$HdisTsunamiDmax</B><BR>
END

	# ��κ�ɸ��
	$HpointNumber = $HislandSizeX * $HislandSizeY;

	$src .= <<"END";
�������ѥե饰��<B>$HdisTsunamiFsea</B><BR>
�����������Ѥ�������򲼲�������ȯ����Ψ��10�ܤˤʤ롣
END
	if($HpointNumber - 8*8 - $HdisTsunamiFsea > 0) {
		my %bai;
		my $pn = $HpointNumber - 8*8;
		foreach ($HdisTsunamiFsea..$pn) {
				my $flag = ($HpointNumber - 8*8 - $_)/($HpointNumber - 8*8 - $HdisTsunamiFsea);
			$flag = 1 + int($flag * 4);
			$bai{$flag} = $_;
		}
		$src .= "��(����ɸ��Ū�ˤϡ�";
		foreach (sort { $b <=> $a } keys %bai) {
			next if($_ == 1);
			$src .= "$bai{$_}";
			$src .= "�ʲ�" if($bai{$_} != $HdisTsunamiFsea);
			$src .= "��$_�ܡ�";
		}
		$src .= ')';
	}
	$src .= '<BR><BR>';

# ����
#-------------------------
	$src .= "<HR><a name='monster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ����</H3></a>";

	$src .= <<"END";
<BR>
ñ�����Ѥ�����β��ýи�Ψ��<B>${HdisMonster}%</B>���ʥХȥ�ե�����ɡ�<B>${HdisMonsterBF}%</B>��<BR>
�����ɸ���Ȥ�������<B>$useStr[$HuseSendMonster]</B><BR>
ST�����ɸ���Ȥ�������<B>$useStr[$HuseSendMonsterST]</B><BR>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����<br>�и��͸�<br>(��Ψ)${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ɸ�����<BR>ST����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ɸ�<BR>�ֹ�${H_tagTH}</TH><TH colspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�и���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ĳ�������${H_tagTH}</TH><TH colspan=8>${HtagTH_}ǽ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH>
<TH>${HtagTH_}­��<br>®��${H_tagTH}</TH><TH>${HtagTH_}­��<br>�ȤƤ�<br>®��${H_tagTH}</TH><TH>${HtagTH_}���<br>����<br>�Ų�${H_tagTH}</TH>
<TH>${HtagTH_}���<br>��ư${H_tagTH}</TH><TH>${HtagTH_}���<br>��ư${H_tagTH}</TH><TH>${HtagTH_}��ư<br>���${H_tagTH}</TH>
<TH>${HtagTH_}����ǽ��${H_tagTH}</TH><TH>${HtagTH_}���<br>����${H_tagTH}</TH>
</TR>
END

	foreach $i (0..$#HmonsterName) {
		my $maxHP = $HmonsterBHP[$i] + $HmonsterDHP[$i] - 1;
		$maxHP++ if(!$HmonsterDHP[$i]);
		my $levelpop = ($HdisMonsBorder[$i]) ? $HdisMonsBorder[$i] . $HunitPop : '��';
		1 while $levelpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $levelratio = $HdisMonsRatio[$i];
		my $monsterValue = $HmonsterValue[$i] . $HunitMoney;
		1 while $monsterValue =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($mcost, $mcostst, $mno) = ('��', '��', '��');
		if($i <= $HsendMonsterNumber) {
			$mcost = $HmonsterCost[$i] . $HunitMoney if($HuseSendMonster);
			1 while $mcost =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mcostst = $HmonsterCostST[$i] . $HunitMoney if($HuseSendMonsterST);
			1 while $mcostst =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mno = $i;
		}
		my @attackName = (($HmonsterFireName[$i] ne '' ? $HmonsterFireName[$i] : '�ߥ����빶��'),'��');
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
	$src .= "�������������פϡ����Ƥ��������μ���(����Hex)�ˤޤ�٤�ʤ����Ƥ��ޤ������������������Hex��­��ʤ������������ߤˤʤ�ޤ���<BR>";
	$src .= <<"END";
<BR>
���⤷�����ü��Ȥ������ϰϤˤ����硢����(����)���뤳�Ȥ⤢��褦�ˤ��뤫����<B>$anStr[$HmonsterSelfAttack]</B><BR>
�ֹ���ǽ�ϡפ����Ƥ����������Ϸ�����$AfterName�ξ�硢̵���ˤ��뤫����<B>$saftyStr[$HmissileSafetyZone]</B><BR>
��̵������̵���ˤʤ��Ψ��<B>${HmissileSafetyInvalidp}%</B>(̵������ǽ��ȯư������̤�Ƚ��)<BR>
END

# �������
#-------------------------

	$src .= <<"END";
<HR>
<a name='hmonster'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �������</H3></a>
������ä��и����뤫����<B>$doStr[$HhugeMonsterAppear]</B><BR>
END

	if($HhugeMonsterAppear) {

		$src .= <<"END";
ñ�����Ѥ�����ε�����ýи�Ψ��<B>${HdisHuge}%</B>���ʥХȥ�ե�����ɡ�<B>${HdisHugeBF}%</B>��<BR>
�Τκ����������˹Ԥ�ǽ�ϤǤκ�����Ψ��<B>${HpRebody}%</B><BR>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}�������${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�������<br>�и��͸�<br>(��Ψ)${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ɸ�����<BR>ST����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ɸ�<BR>�ֹ�${H_tagTH}</TH><TH colspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�и���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�ĳ�������${H_tagTH}</TH><TH colspan=10>${HtagTH_}ǽ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH>
<TH>${HtagTH_}­��<br>®��${H_tagTH}</TH><TH>${HtagTH_}­��<br>�ȤƤ�<br>®��${H_tagTH}</TH><TH>${HtagTH_}���<br>����<br>�Ų�${H_tagTH}</TH>
<TH>${HtagTH_}���<br>��ư${H_tagTH}</TH><TH>${HtagTH_}���<br>��ư${H_tagTH}</TH><TH>${HtagTH_}��ư<br>���${H_tagTH}</TH>
<TH>${HtagTH_}����ǽ��${H_tagTH}</TH><TH>${HtagTH_}���<br>����${H_tagTH}</TH>
<TH>${HtagTH_}����<br>�ɱ�${H_tagTH}</TH><TH>${HtagTH_}���<br>����<br>����${H_tagTH}</TH></TR>
END

		foreach $i (0..$#HhugeMonsterName) {
			my $maxHP = $HhugeMonsterBHP[$i] + $HhugeMonsterDHP[$i] - 1;
			$maxHP++ if(!$HhugeMonsterDHP[$i]);
			my $levelpop = ($HdisHugeBorder[$i]) ? $HdisHugeBorder[$i] . $HunitPop : '��';
			1 while $levelpop =~ s/(.*\d)(\d\d\d)/$1,$2/;
			my $levelratio = $HdisHugeRatio[$i];
			my $hugeMonsterValue = $HhugeMonsterValue[$i] . $HunitMoney;
			1 while $hugeMonsterValue =~ s/(.*\d)(\d\d\d)/$1,$2/;

			$src .= "<TR $HbgInfoCell><TD align='right'>";
			my($j, @monImage);
			foreach $j (0..6) {
				$monImage[$j] = ($HhugeMonsterImage3[$i][$j] eq '') ? "${HimageDir}/$HlandImage[$HlandSea][0]" : "${HimageDir}/$HhugeMonsterImage3[$i][$j]";
			}
			my($mcost, $mcostst, $mno) = ('��', '��', '��');
			if($i <= $HsendHugeMonsterNumber) {
				$mcost = $HhugeMonsterCost[$i] . $HunitMoney if($HuseSendMonster);
				1 while $mcost =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mcostst = $HhugeMonsterCostST[$i] . $HunitMoney if($HuseSendMonsterST);
				1 while $mcostst =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$mno = $i + 50;
			}
			my @attackName = (($HhugeMonsterFireName[$i] ne '' ? $HhugeMonsterFireName[$i] : '�ߥ����빶��'),'��');
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

# �����ƥ�
#-------------------------

	$src .= <<"END";
<HR>
<a name='item'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �����ƥ�</H3></a>
�����ƥ��Ȥ�������<B>$useStr[$HuseItem]</B><BR>
END

	if($HuseItem) {
		my $itemGet   = ($HitemGetDenominator) ? "(������и���)<B>/$HitemGetDenominator</B>" : 'Ƚ�ꤷ�ʤ�';
		my $itemGet2  = ($HitemGetDenominator2) ? "(������и���)<B>/$HitemGetDenominator2</B>" : 'Ƚ�ꤷ�ʤ�';
		my $itemGet3  = ($HitemGetDenominator3) ? "(������и���)<B>/$HitemGetDenominator3</B>" : 'Ƚ�ꤷ�ʤ�';
		my $itemSeize = ($HitemSeizeDenominator) ? "(�����и���)<B>/$HitemSeizeDenominator</B>" : 'Ƚ�ꤷ�ʤ�';
		my $itemGive  = (!$HitemGivePerTurn) ? '' : ($HitemGivePerTurn == 1) ? "�����������դ��Ȥ�<B>��̤�$AfterName������</B>�ҤȤĤ��ġ֥��������ƥ�פ�Ϳ�����ޤ���" : "�����������դ��Ȥ�<B>���̤�$AfterName������</B>�ҤȤĤ��ġ֥��������ƥ�פ�Ϳ�����ޤ���";
		$itemGive    .= "������������(����or����)����ͭ���ʤ�$AfterName�ϥ����åפ��ޤ���<BR>";
		my $itemBF    = ($HitemInvalid) ? "�����Хȥ�ե�����ɤǤϡֹ��������ܡסּ����򹭤���ס���$AfterName����ǽ�ס�̿��ΨUP�ס��˲��ϣ��ܡפ�ǽ�Ϥ�̵���ˤʤ�ޤ���" : '';
		my $compStr = (!$HallyItemComplete) ? "���Ĥ�$AfterName" : (!$HarmisticeTurn) ? "���Ĥ�Ʊ��" : "���Ĥοر�";

		$src .= <<"END";
����<B>$compStr</B>�����٤ƤΡ֥��������ƥ�פ��������ȥ����ब��λ���ޤ���<BR>
$itemGive
<BR>
�����ƥ����Ƚ���Ψ<BR>
����������༣�λ���$itemGet<BR>
�������༣�λ���$itemGet2<BR>
���ĳ���Ѥλ���$itemGet3<BR><BR>
�����ƥ�å��Ƚ���Ψ<BR>
�������ƥ���ͭ$AfterName�δ��������λ���$itemSeize<BR>
��������������Ǥ������ݤˤϡ����٤ƤΥ����ƥब�Ǹ�Σ���(����)���˲�����$AfterName�ذܤ�ޤ���<br>
�������ޤ�����ͳ��ǡ���˴ؤ�餺������ü�������ϡ����٤ƤΥ����ƥ�(�����������и���)�򼺤��ޤ���<br>
<TABLE>
<TR $HbgInfoCell><TH colspan=2 rowspan=2>${HtagTH_}$HitemName[0]${H_tagTH}</TH>
<TH colspan=25>${HtagTH_}ǽ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell>
<TH>${HtagTH_}����<br>����<br>�ƥ�${H_tagTH}</TH>
<TH>${HtagTH_}��$AfterName<br>���<br>��ǽ${H_tagTH}</TH>
<TH>${HtagTH_}�Ϸ�<br>����<br>̵��${H_tagTH}</TH>
<TH>${HtagTH_}��ͭ<br>����<br>�ܦ�${H_tagTH}</TH>
<TH>${HtagTH_}����<br>����<br>Hex${H_tagTH}</TH>
<TH>${HtagTH_}̿��<br>ΨUP<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>���<br>���<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>max<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}���<br>max<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>���<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�˲�<br>��<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�ݻ�<br>����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�ݻ�<br>��<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>���<br>������<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�Ͽ�<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}���<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>���<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}ʮ��<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�к�<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}����<br>��Ψ${H_tagTH}</TH>
<TH>${HtagTH_}�˲�<br>��<br>��${H_tagTH}</TH>
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
			$src .= ($HitemSpecial[$i][3] > 0) ? "<TD align='center'>+$HitemSpecial[$i][3]</TD>" : ($HitemSpecial[$i][3] < 0) ? "<TD align='center'>$HitemSpecial[$i][3]</TD>" : "<TD align='center'>��</TD>";
			$src .= ($HitemSpecial[$i][4] != 0) ? "<TD align='center'>$HitemSpecial[$i][4]Hex</TD>" : "<TD align='center'>��</TD>";
			$src .= ($HitemSpecial[$i][5] != 0) ? "<TD align='center'>$HitemSpecial[$i][5]%</TD>" : "<TD align='center'>��</TD>";
			foreach (6..12) {
				$src .= ($HitemSpecial[$i][$_] > 1) ? "<TD align='center'><FONT color=blue>x$HitemSpecial[$i][$_]</FONT></TD>" : ($HitemSpecial[$i][$_] < 1) ? "<TD align='center'><FONT color=red>x$HitemSpecial[$i][$_]</FONT></TD>" : "<TD align='center'>��</TD>";
			}
			foreach (13..23) {
				$src .= ($HitemSpecial[$i][$_] > 1) ? "<TD align='center'><FONT color=red>x$HitemSpecial[$i][$_]</FONT></TD>" : ($HitemSpecial[$i][$_] < 1) ? "<TD align='center'><FONT color=blue>x$HitemSpecial[$i][$_]</FONT></TD>" : "<TD align='center'>��</TD>";
			}
			$src .= ($HitemSpecial[$i][24] > 0) ? "<TD align='center'>+$HitemSpecial[$i][24]</TD>" : ($HitemSpecial[$i][24] < 0) ? "<TD align='center'>$HitemSpecial[$i][24]</TD>" : "<TD align='center'>��</TD>";
		}
		$src .= <<"END";
</TABLE>
$itemBF<BR>
END
	}

# ��ǰ��
#-------------------------

	$src .= <<"END";
<HR>
<a name='monument'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ��ǰ��</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan=2>${HtagTH_}��ǰ��${H_tagTH}</TH></TR>
END

	foreach $i (0..$#HmonumentName) {
		$src .= <<"END";
<TR $HbgInfoCell><TD align='right'><img src='${HimageDir}/$HmonumentImage[$i]'></TD><TH>$HmonumentName[$i]</TH></TR>
END
	}
	$src .= "</TABLE>";
#	$src .= "��ǰ��ȯ�ͤ�Ȥ�������<B>$useStr[$HuseBigMissile]</B><BR>";
	$src .= "��ǰ��ȯ�ͤ�Ȥ�������<B>���</B><BR>";

# �������ա��ƾ�
#-------------------------

	my $prize = 0;
	my %prizeKind = (
		'pop' => '�͸�',
		'gain' => '������и���',
		'money' => '���',
		'food' => '����',
		'area' => '����',
		'farm' => '���쵬��',
		'factory' => '���쵬��',
		'mountain' => '�η��쵬��',
		'monsterkill' => '�����༣��',
		'itemNumber' => "$HitemName[0]������",
		'point' => "$HpointName",
		'achive' => "�߽Ф�����̱(1������)",
		'damage' => "�ü������͸�(1������)",
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
	my @extKind  = ('ͥ�����', '�׸���', '�˲������ɱһ��ߤο�', '�˲������ߥ�������Ϥο�', '�߽Ф�����̱�ι�׿͸�', '�������ƿ�', 'ȯ�ͤ����ƿ�', '�ɱһ��ߤ��Ƥ����ƿ�', '�ɸ����������ο�', '�ɸ����줿�����ο�', '�˲����������ο�');
	my @extAfter = ('��', '', '��', '��', "$HunitPop", 'ȯ', 'ȯ', 'ȯ', '��', '��', '��');
	foreach $i (0..$#Hprize) {
		$prize += $Hprize[$i]->{'money'};
	}
	my $str = ($prize) ? "<TH>${HtagTH_}�޶��${H_tagTH}</TH>" : '';
	$src .= <<"END";
<HR>
<a name='prize'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> �������ա��ƾ�</H3></a>
�������դ򲿥�������˽Ф�����<B>${HturnPrizeUnit}������</B><BR>

<TABLE>
<TR $HbgInfoCell><TH colspan=2>${HtagTH_}��${H_tagTH}</TH><TH colspan=2>${HtagTH_}���޾��${H_tagTH}</TH>$str</TR>
END

	foreach $i (0..$#Hprize) {
		my($req1, $req2);
		if($Hprize[$i]->{'kind'} eq 'ext') {
			$req1 = $extKind[$Hprize[$i]->{'ptr'}];
			my $threshold = $Hprize[$i]->{'threshold'};
			$threshold /= 10 if($Hprize[$i]->{'ptr'} == 1);
			$req2 = $threshold . $extAfter[$Hprize[$i]->{'ptr'}];
			1 while $req2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$req2 .= "�ʾ�";
		} else {
			$req1 = ($i) ? $prizeKind{$Hprize[$i]->{'kind'}} : "��������Ƚ���(${HturnPrizeUnit}�����󤴤�)";
			if($i) {
				$req2 = $Hprize[$i]->{'threshold'} . $prizeAfter{$Hprize[$i]->{'kind'}};
				1 while $req2 =~ s/(.*\d)(\d\d\d)/$1,$2/;
				$req2 .= "�ʾ�";
			} else {
				if($Hprize[$i]->{'kind'} == 1) {
					$req2 = '�����裱��';
				} else {
					$req2 = "������$Hprize[$i]->{'kind'}�̰ʾ�";
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

# ���ޥ�ɰ���
#-------------------------

	$col = 1;
	$src .= <<"END";
<HR>
<a name='command'><H3 class='subtitle'><a style='text-decoration=none' href='#top'><small>��</small></a> ���ޥ�ɰ���</H3></a>
<TABLE>
<TR $HbgInfoCell><TH colspan=$col>${HtagTH_}���ޥ�ɰ���${H_tagTH}������${turnStr[1]}��${H_tagComName}���������񤹤롡${turnStr[0]}��${H_tagComName}���������񤷤ʤ�</TH></TR>
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
<TR $HbgInfoCell><TH colspan=4>${HtagTH_}${category}��${H_tagTH}</TH></TR>
END
		foreach ($start..$end) {
			next if(!$comCheck{$_});
			next if($HmaxComNavyLevel && ($HcomNavy[0] + $HcomNavyNumber[$#HcomNavyNumber] < $_) && ($_ <= $HcomNavy[$#HnavyName]));
			next if($HcomName[$_] eq '');
			my $cost = $HcomCost[$_];
			if($cost eq '0') {
				$cost = '̵��';
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
		$src .= "</TR><TR><TD  class='M' colspan=3>��${turnStr[($HcomTurn[$HcomPrepare3] > 0)]}$HcomName[$HcomPrepare3]${H_tagComName}�ϡ�<B>$precheap�Ĥ�</B>�ι��Ϥ���<B>��$discount�����</B>�ˤʤ�ޤ���</TD>";
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
<B>���� JS.$versionInfo(based on ver1.3)</B> patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/'>neo_otacky</a>
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
