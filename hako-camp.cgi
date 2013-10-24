# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.20
# �رĲ��̺����⥸�塼��(���ζ�˴���ꥸ�ʥ�)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://t.pos.to/hako/
#----------------------------------------------------------------------
# �����ζ�˴�� ver1.0.0 by ������ http://t.pos.to/ozzy/
# ���Ѿ���Ȣ�����˽ऺ�롥�ܤ�������°��readme.txt�ե�����򻲾�
#----------------------------------------------------------------------

#������������������������������������������������������������������������
#							 ���ζ�˴ 2nd
#								  v1.0
#
#					  by ���� webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#������������������������������������������������������������������������

#������������������������������������������������������������������������
#							���ζ�˴ ����
#								  v1.2
#
#					  by ���� webgame@oyoyo.ne.jp
#					http://www.oyoyo.ne.jp/webgame/
#������������������������������������������������������������������������

#----------------------------------------------------------------------
# �رĲ���
#----------------------------------------------------------------------
# �ᥤ��
sub campMain {

	my $aNum = $HidToAllyNumber{$HcurrentCampID};
	$HcurrentCamp = $Hally[$aNum] if(defined $aNum);
	my $pflag = checkMasterPassword($HcampPassword);
	# ����
	unlock ();

	# �ѥ����
	if($HtakayanPassword ne $HcurrentCamp->{'Takayan'} && !$pflag) {
		# password�ְ㤤
		tempWrongPassword();
		return;
	}

	if(defined $aNum) {
		tempPrintCampHead(); # ��������
		campAllIslandsInfo(); # �رĤ�°�������ξ���
	} else {
		if($pflag) {
			tempPrintAllHead();
			tempAllIslandsInfo(); # ����ξ���
		} else {
			# password�ְ㤤
			tempWrongPassword();
			return;
		}
	}
}

#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------

# �����ر� ��������
sub tempPrintCampHead {
	out(<<END);
<DIV align='center'>
$HtempBack<BR><BR>
${HtagBig_}${HtagName_}��<FONT COLOR="$HcurrentCamp->{'color'}"><B>$HcurrentCamp->{'mark'}</B></FONT>$HcurrentCamp->{'name'}��${H_tagName} ��������${H_tagBig}<BR>
�رĥѥ���ɡ���<B>$HcurrentCamp->{'Takayan'}</B>��<BR><BR>
END

	out(<<END) if($HallyBbs);
<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm.action='${HbaseDir}/${HallyBbsScript}';document.allyForm.submit();return false;">
${HtagBig_}<small>${HtagName_}<FONT COLOR="$HcurrentCamp->{'color'}"><B>$HcurrentCamp->{'mark'}</B></FONT>$HcurrentCamp->{'name'}${H_tagName}�����ļ���</A></small>${H_tagBig}
<FORM name="allyForm" action="" method="POST" target="_blank">
<INPUT type=hidden name="ally" value="$HcurrentCampID">
<INPUT type=hidden name="cpass" value="$HcampPassword">
<INPUT type=hidden name="jpass" value="$HtakayanPassword">
<INPUT type=hidden name="id" value="$HcurrentID">
</FORM>
END

	out("</DIV>");
}

# ����ɽ���إå�
sub tempPrintAllHead {
	out(<<END);
<DIV align='center'>
$HtempBack<BR><BR>
${HtagBig_}${HtagName_}���ﱿ������${H_tagName}${H_tagBig}<BR>
</DIV><BR><BR>
END
}

# ��Υ��ޥ���ɤ߹���(�رĲ��̺�����)
sub readCommands {
	my($id) = @_;
	my(@line, @land, $command);
	# �Ϸ�
	my($map) = $Hislands[$HidToNumber{$id}]->{'map'};
	if(!$HoceanMode) {
		if(!open(IIN, "${HdirName}/${id}.${HsubData}")) {
			if(-e "${HdirName}/${id}tmp.${HsubData}") {
				rename("${HdirName}/${id}tmp.${HsubData}", "${HdirName}/${id}.${HsubData}");
			}
			if(!open(IIN, "${HdirName}/${id}.${HsubData}")) {
				exit(0);
			}
		}
		chomp(@line = <IIN>);
		close(IIN);
		@land = readLand($map, @line);
	} else {
		@land = ($Hworld->{'land'}, $Hworld->{'landValue'});
	}
	# ���ޥ��($HrepeatTurn��$HcampCommandTurnNumberʬ�Τ�ɽ��)
	my($cnum) = min($HrepeatTurn * $HcampCommandTurnNumber, $HcommandMax);
	$command = readCommand($id, $cnum);

	return (@land, $command);
}

# �����ɽ��
sub campAllIslandsInfo {

	# �ơ��֥�إå��ν񤭽Ф�
	campTableHeader();

	# �رĤ�°������Υ��ޥ�ɤΤ��ɤ߽Ф�
	my($id);
	foreach $id (@{ $HcurrentCamp->{'memberId'} }) {
		my @temp = readCommands($id);
		$Hislands[$HidToNumber{$id}]->{'land'} = $temp[0];
		$Hislands[$HidToNumber{$id}]->{'landValue'} = $temp[1];
		$Hislands[$HidToNumber{$id}]->{'command'} = $temp[2];
	}
	if($HoceanMode) {
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
		($Hworld->{'land'}, $Hworld->{'landValue'}) = readLand($map, @line);
		foreach $id (@{ $HcurrentCamp->{'memberId'} }) {
			($Hislands[$HidToNumber{$id}]->{'land'}, $Hislands[$HidToNumber{$id}]->{'landValue'}) = ($Hworld->{'land'}, $Hworld->{'landValue'});
		}
	}

	# ����ξ���񤭽Ф�
	my($i);
	foreach $i (0..$islandNumber) {
		next if($Hislands[$i]->{'allyId'}[0] eq '');
		if ($HcurrentCampID == $Hislands[$i]->{'allyId'}[0]) {
			campIslandInfo($Hislands[$i], $i+1-$HbfieldNumber); # �رĤ�°������Τ�
		}
	}
	# �ơ��֥�եå��ν񤭽Ф�
	campTableFooter();

}

# �����ɽ��(����)
sub tempAllIslandsInfo {

	$sStr1= '';
	if($HsurvivalTurn) {
		my $predelNumber = @HpreDeleteID;
		my $remainNumber = $islandNumber - $predelNumber;
		foreach $i ($HbfieldNumber..$remainNumber) {
			$allscore += $Hislands[$i]->{$HrankKind};
		}
		$sStr1 = "<TH $HbgTitleCell>${HtagTH_}��ͭΨ${H_tagTH}</TH>"
	}
	# �ơ��֥�إå��ν񤭽Ф�
	campTableHeader();
	my($i);
	foreach $i ($HbfieldNumber..$islandNumber) {
		# �رĤ�°������Υ��ޥ�ɤΤ��ɤ߽Ф�
		my @temp = readCommands($Hislands[$i]->{'id'});
		$Hislands[$i]->{'land'} = $temp[0];
		$Hislands[$i]->{'landValue'} = $temp[1];
		$Hislands[$i]->{'command'} = $temp[2];
		# ����ξ���񤭽Ф�
		campIslandInfo($Hislands[$i], $i+1-$HbfieldNumber);
	}
	# �ơ��֥�եå��ν񤭽Ф�
	campTableFooter();

}

sub campIslandInfo {
	my($island, $rank) = @_;

	# ����ɽ��
	my($id) = $island->{'id'};
	my($land)= $island->{'land'};
	my($landValue)= $island->{'landValue'};
	my($contribution) = int($island->{'ext'}[1] / 10); # �׸���

	my $pop = ($island->{'pop'} == 0) ? "̵��" : "$island->{'pop'}$HunitPop";
	1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $area = ($island->{'area'} == 0) ? "����" : "$island->{'area'}$HunitArea";
	1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $money = ($island->{'money'} == 0) ? "��⥼��" : "$island->{'money'}$HunitMoney";
	1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $food = ($island->{'food'} == 0) ? "���ߥ���" : "$island->{'food'}$HunitFood";
	1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $farm = ($island->{'farm'} == 0) ? "��ͭ����" : "$island->{'farm'}0$HunitPop";
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $factory = ($island->{'factory'} == 0) ? "��ͭ����" : "$island->{'factory'}0$HunitPop";
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $mountain = ($island->{'mountain'} == 0) ? "��ͭ����" : "$island->{'mountain'}0$HunitPop";
	1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my $name = islandName($island);
	if($island->{'absent'} == 0) {
		$name = "${HtagName_}${name}${H_tagName}";
	} else {
		$name = "${HtagName2_}${name}($island->{'absent'})${H_tagName2}";
	}
	$name .= "${HtagDisaster_}��${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
		$name = "${HtagDisaster_}�ڴ����ͤ��������$rest${H_tagDisaster}<BR>��" . $name;
	}
	my $preab = ($island->{'preab'} ? '<br><small><span class=attention>(�رĳ�ȯ��)</span></small>' : '');

	my($ofname) = $island->{'fleet'};
	my($fkind) = $island->{'fkind'};
	my @flist = @$fkind;
	my @fleetlist = ();
#	my @idx = (0..$#flist);
#	@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
#	@flist = @flist[@idx];
	my $s = '';
	foreach (@flist) {
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack(hex($_));
		next if ($HnavySpecial[$nKind] & 0x8); # �����Ͻ���
		my $l;
		my $navyLevel = expToLevel($HlandNavy, $nExp);
		$s = "\n�ѵ��� $nHp/��٥� $navyLevel/�и��� $nExp";
		$s = " [${status[$nStat]}]" . $s if($nStat);
		if(($eId != $id) && (defined $HidToNumber{$eId})) {
			my $eName = islandName($Hislands[$HidToNumber{$eId}]);
			$eName =~ s/<[^<]*>//g;
			$s .= "\n${eName}���ɸ���";
			$l = " HREF=\"${HthisFile}?Sight=${eId}\" target=\"_blank\" style=\"decoration:none;\"";
		}
		$fleetlist[$nNo] .= " <A TITLE=\"$HnavyName[$nKind]${s}\"${l}><img src=\"$HnavyImage[$nKind]\" width=24 height=24></A>";
	}
	my @fleetMove = ();
	my @McorrectX = (@defaultX)x2;
	my @McorrectY = (@defaultY)x2;
	foreach (@{$island->{'move'}}) {
		if(!(defined $_)) {
			push(@fleetMove, '');
			next;
		}
		my($tx, $ty) = split(/,/, $_);
		$tx = $McorrectX[$tx];
		$ty = $McorrectY[$ty];
		my($tId) = $HlandID[$tx][$ty];
		my($tn) = $HidToNumber{$tId};
		if(!(defined $tn)) {
			undef $_;
			push(@fleetMove, '');
			next;
		}
		my($tIsland) = $Hislands[$tn];
		my($str) = islandName($tIsland);
		$str .= "($tx, $ty)";
		push(@fleetMove, " <small><B>��ɸ����</B>${HtagName_}${str}${H_tagName}</small><br>");
	}
	my($prize) = $island->{'prize'};
	$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
	my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
	$prize = '';
	my($i, $ss);
	# �����ƥ��ɽ��
	foreach (@{$island->{'item'}}) {
		next if($_ == 0);
		$prize .= "<IMG SRC=\"$HitemImage[$_]\" TITLE=\"$HitemName[$_]\" onMouseOver='status=\"$HitemName[$_]\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16> ";
	}
	# �������դ�ɽ��
	$s = '';
	my @turnPrize = reverse(split(/,/, $turns));
	$i = 0;
	foreach (@turnPrize) {
		last if($i > 3);
		$s .= "\n" if($i++);
		$s .= "$_${Hprize[0]->{'name'}}";
	}
	my $tNum = @turnPrize;
	$s .= ($i < $tNum ? "\n¾��${tNum}�����" : "\n�ʾ�${tNum}�����") if($tNum);
	my $rt = "\n";
	$ss = $s;
	$ss =~ s/$rt/ /g;
	$prize .= "<IMG SRC=\"prize0.gif\" TITLE=\"${s}\" onMouseOver='status=\"${ss}\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16> " if($s ne '');

	# ̾���˾ޤ�ʸ�����ɲ�
	my($f) = 1;
	$s = '';
	foreach(1..$#Hprize) {
		if($flags & $f) {
			$s .= "<IMG SRC=\"prize${_}.gif\" TITLE=\"${Hprize[$_]->{'name'}}\" onMouseOver='status=\"${Hprize[$_]->{'name'}}\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>";
		}
		$f *= 2;
	}
	$prize .= $s;

	# �ݤ������åꥹ��
	$f = 1;
	$s = '';
	my($max) = -1;
	my($mNameList) = '';
	my $hflag = 0;
	for($i = 0; $i < $HmonsterNumber; $i++) {
		if($monsters & $f) {
			$mNameList .= "\n" if($mNameList ne '');
			$mNameList .= "[$HmonsterName[$i]]";
			$max = $i;
#			$s .= "<IMG SRC=\"${HmonsterImage[$i]}\" ALT=\"$HmonsterName[$i]\" WIDTH=16 HEIGHT=16> ";
		}
		$f *= 2;
	}
	$f = 1;
	for($i = 0; $i < $HhugeMonsterNumber; $i++) {
		if($hmonsters & $f) {
			$mNameList .= "\n" if($mNameList ne '');
			$mNameList .= "[$HhugeMonsterName[$i]]";
			$max = $i;
			$hflag = 1;
#			$s .= "<IMG SRC=\"${HhugeMonsterImageS[$i]}\" ALT=\"$HhugeMonsterName[$i]\" WIDTH=16 HEIGHT=16> ";
		}
		$f *= 2;
	}
	if($max != -1) {
		my $image = ($hflag ? $HhugeMonsterImageS[$max] : $HmonsterImage[$max]);
		$s .= " <span class='monsm'><IMG SRC=\"${image}\" TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$island->{'monsterkill'}$HunitMonster�༣</span> ";
		$prize .= $s;
	}

	# �и���β��åꥹ��
	my $monsterlive = $island->{'monsterlive'};
	$monsterlive =~ /([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)/;
	my($monslive, $monstertype, $hmonstertype, $unknownlive, $unknowntype) = ($1, $2, $3, $4, $5);
	$f = 1;
	$s = '';
	$max = -1;
	$mNameList = '';
	$hflag = 0;
	for($i = 0; $i < $HmonsterNumber; $i++) {
		if($monstertype & $f) {
			$mNameList .= "\n" if($mNameList ne '');
			$mNameList .= "[$HmonsterName[$i]] ";
			$max = $i;
		}
		$f *= 2;
	}
	$f = 1;
	for($i = 0; $i < $HhugeMonsterNumber; $i++) {
		if($hmonstertype & $f) {
			$mNameList .= "\n" if($mNameList ne '');
			$mNameList .= "[$HhugeMonsterName[$i]]";
			$max = $i;
			$hflag = 1;
		}
		$f *= 2;
	}
	if($max != -1) {
		my $image = ($hflag ? $HhugeMonsterImageS[$max] : $HmonsterImage[$max]);
		$s .= " <span class='unemploy2'><IMG SRC=\"${image}\" TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$monslive$HunitMonster�и��桪</span> ";
		$prize .= $s;
	}
	# ��°������
	$f = 1;
	$s = '';
	$max = -1;
	$mNameList = '';
	foreach (0..$#HnavyName) {
		if($unknowntype & $f) {
			$mNameList .= "\n" if($mNameList ne '');
			$mNameList .= "[$HnavyName[$_]] ";
			$max = $_;
		}
		$f *= 2;
	}
	if($max != -1) {
		my $image = $HnavyImage[$max];
		$s .= " <span class='unemploy2'><IMG SRC=\"${image}\" TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$unknownlive�Ͻи��桪</span> ";
		$prize .= $s;
	}
	if($prize ne '') {
		$prize = '<BR><BR>' . $prize; 
	}
	my $col = 3;
	my($sStr2)= '';
	if($HsurvivalTurn) {
#		my $occupation = $allscore ? int((100 * $island->{'pop'})/$allscore) : 0;
#		$occupation = 100 if($occupation > 100);
		my $occupation = $allscore ? sprintf("%.1f", (100 * $island->{'pop'})/$allscore) : 0;
		$occupation = "100.0" if($occupation > 100);
		$sStr2 = "<TD $HbgInfoCell align=right>${occupation}%</TD>";
		$sStr2 = "<TD $HbgInfoCell align=right>��</TD>" if($island->{'field'} || $island->{'predelete'});
		$col++;
	}
	# ��Ũ���
	my $mypri = $island->{'priority'};
	my($j, @priList);
	foreach $i (0..3) {
		$priList[$i] = "";
		my $pFlag = 0;
		foreach (split(/\-/, $mypri->[$i])) {
			$priList[$i] .= "��" if($pFlag);
			$pFlag++;
			$priList[$i] .= $HpriStr[$_];
		}
	}

	my @row;
	if($HnavyName[0] ne '') {
		@row = (6, 5);
	} else {
		@row = (2, 1);
		$col += 5;
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=$row[0] align=center>${HtagNumber_}$rank${H_tagNumber}</TD>
<TD class='C' ROWSPAN=$row[0] align=left>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}" TARGET=_blank>
$name
</A>$preab
$prize
</TD>$sStr2
<TD $HbgInfoCell align=right>$pop</TD>
<TD $HbgInfoCell align=right>$contribution</TD>
<TD $HbgInfoCell align=right>$money</TD>
<TD $HbgInfoCell align=right>$food</TD>
<TD $HbgInfoCell align=right>$area</TD>
<TD $HbgInfoCell align=right>$farm</TD>
<TD $HbgInfoCell align=right>$factory</TD>
<TD $HbgInfoCell align=right>$mountain</TD>
</TR>
END

	out("<TR><TD $HbgCommentCell ROWSPAN=$row[1] COLSPAN=$col valign=top>${HtagTH_}\n");
	my $cnum = min($HrepeatTurn * $HcampCommandTurnNumber, $HcommandMax);
	my $navyComLevel = gainToLevel($island->{'gain'});
	my $turn  = $HislandTurn + 1;
	my $cflag = $island->{'itemAbility'}[6];
	$cflag = 1 if(!$cflag);
	my $flagST = 0;
	my $count = 0;
	for($i = 0; $i < $cnum; $i++) {
		my $kind = $island->{'command'}->[$i]->{'kind'};
		my $arg  = $island->{'command'}->[$i]->{'arg'};
		$arg = 1 if(!$arg);
		if(!$HcomUse{$kind}) {
		} elsif( ($kind == $HcomFarm) ||
			($kind == $HcomFactory) ||
			(($kind == $HcomDbase) && $HdurableDef) ||
			(($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) ||
			($kind == $HcomMountain) ||
			($kind == $HcomCore) ||
			($kind == $HcomPropaganda)
			) {
			$count += $HcomTurn[$kind] * $arg;
		} elsif(($kind == $HcomSendMonsterST) || (($HcomMissile[0] <= $kind) && ($kind <= $HcomMissile[$#HmissileName]) && $STcheck{$kind})) {
			if($flagST) {
				$count++;
				$flagST = 0;
			} else {
				$flagST = 1;
				if(($i + 1 < $HcommandMax) && (($island->{'command'}->[$i+1]->{'kind'} == $HcomSendMonsterST) || (($HcomMissile[0] <= $island->{'command'}->[$i+1]->{'kind'}) && ($island->{'command'}->[$i+1]->{'kind'} <= $HcomMissile[$#HmissileName]) && $STcheck{$island->{'command'}->[$i+1]->{'kind'}}))) {
					$count++;
					$flagST = 0;
				} else {
					$count += $HcomTurn[$kind];
				}
			}
		} elsif($flagST && ($i + 1 < $HcommandMax) && (($island->{'command'}->[$i+1]->{'kind'} == $HcomSendMonsterST) || (($HcomMissile[0] <= $island->{'command'}->[$i+1]->{'kind'}) && ($island->{'command'}->[$i+1]->{'kind'} <= $HcomMissile[$#HmissileName]) && $STcheck{$island->{'command'}->[$i+1]->{'kind'}}))) {
			$count++;
			$flagST = 0;
		} else {
			$count += $HcomTurn[$kind];
		}
		my($turnstr);
		if($cflag <= $count) {
			$turnstr = "$HtagComName1_${turn}$H_tagComName";
		} else {
			$turnstr = "$HtagComName2_${turn}$H_tagComName";
		}
		tempCommand($island, $i, $turnstr, $island->{'command'}->[$i], $navyComLevel-1, 1);
		if($cflag <= $count) {
			$turn += int($count/$cflag);
			$count %= $cflag;
		}
	}
	out("${H_tagTH}</TD>\n");

	if($HnavyName[0] ne '') {
		out("<TH $HbgTitleCell>$ofname->[0]����</TH><TD COLSPAN=4 class='C'>$fleetlist[0]<BR><span style='font-size=11px'>$fleetMove[0]$priList[0]</span></TD></TR>\n");
		foreach (1..3) {
			out("<TR><TH $HbgTitleCell>$ofname->[$_]����</TH><TD COLSPAN=4 class='C'>$fleetlist[$_]<BR><span style='font-size=11px'>$fleetMove[$_]$priList[$_]</span></TD></TR>\n");
		}
		my $ifname = '';
		my($x, $y, %invade);
		my($map) = $island->{'map'};
		foreach $y (@{$map->{'y'}}) {
			foreach $x (@{$map->{'x'}}) {
				next if($land->[$x][$y] != $HlandNavy);
				# ¾����δ���Ͻ���
				my($nId, $nFlag, $nNo) = (navyUnpack($landValue->[$x][$y]))[0, 5, 6];
				# �ĳ��Ͻ���
				next if ($nFlag & 1);
				if ($nId != $id) {
					$invade{"$nId,$nNo"} += 1;
				}
			}
		}
		$i = 0;
		foreach (sort { $a cmp $b } keys %invade) {
			my($iId,$iNo) = split(/\,/, $_);
			my $in = $HidToNumber{$iId};
			$ifname .= "<BR>" if($i++);
			if(defined $in) {
				my $iName = islandName($Hislands[$in]);
				$ifname .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]����($invade{$_}��)"
			} else {
				$ifname .= "��°����($invade{$_}��)";
			}
		}
		$ifname .= '��';
		out("<TR><TH>${HtagTH_}¾��δ���${H_tagTH}</TH><TD class='N' colspan=4>$ifname</TD>\n");
	}
	out("</TR>\n");

}

sub campTableHeader {
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function ns(x) {
	return true;
}
//-->
</script>
<DIV align='center'>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
$sStr1<TH $HbgTitleCell>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�׸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�η��쵬��${H_tagTH}</TH>
</TR>
END
}

sub campTableFooter {
	out(<<END);

</TABLE>
</DIV>
END
}

1;
