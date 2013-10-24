# The Return of Neptune: http://no-one.s53.xrea.com/
# ����JS���Ѥ˲���
#----------------------------------------------------------------------
# Ȣ��ȡ��ʥ��ȣ�
# ����ü���⥸�塼��
# $Id: hako-mobile.cgi 60 2005-01-23 07:22:47Z takayama $
#----------------------------------------------------------------------

McgiInput();

tempHeader();

if($HmainMode eq 'turn') {
	# �����󹹿��Ԥ�
	MturnPageMain();
} elsif($HmainMode eq 0) {
	# �Ѹ�����
	MprintMain(0);
} elsif($HmainMode eq 1) {
	# �����
	MlogMain();
} elsif($HmainMode eq 2) {
	# ��ȯ���� �����ʡ�
	MprintMain(1);
} elsif($HmainMode eq 3) {
	# �ײ����
	McmdMain(0);
} elsif($HmainMode eq 4) {
	# �ײ�����
	McmdMain(1);
} elsif($HmainMode eq 5) {
	# �Ǽ���
	MlbbsMain();
} elsif($HmainMode eq 'command') {
	# �ײ�����
	McmdInputMain();
} elsif($HmainMode eq 'TimeTable') {
	# ���ֹ����
	MlistPageMain();
} elsif($HmainMode eq 'setupv') {
	# �Ϸ�����
	MhelpPageMain();
} elsif($HmainMode eq 'FightView') {
	# ���
	MlinkPageMain();
} else {
	MtopPageMain();
}

tempFooter();

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------

# CGI �ɤ߹���
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

# ���¸�߳�ǧ
sub MexistCheck {
	my $mode = shift;
	unlock() if(!$mode);

	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		tempProblem();
		return 1;
	}

	return 0;
}

# �ѥ���ɥ����å�
sub MpassCheck {
	my $island = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		return 1;
	}

	return 0;
}

# �Ͽޥ⡼��
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

	MislandInfo($mode); # ��ξ���
	MislandMap($mode); # ����Ͽ�
}

# �����
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

# �Ǽ���
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

# ������Ǽ�������
sub MlbbsContents {
	my($mode) = @_;
	my($lbbs, $line, $no);
	$lbbs = readLbbs($HcurrentID);
	$no = @lbbs;
	out(<<END) if($lbbs->[0] ne '0<<0>>' && $lbbs->[0] ne '');
No:[�����]��Ƽ�>����($AfterName̾)<BR>
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
			my($turn, $name) = split(/��/, $tan);
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
				# �Ѹ���
				if ($m == 0) {
					# ����
					if($sID ne '0') {
						out("$tan > ${com} $speaker<BR>");
					} else {
						out("$tan > ${com} $speaker<BR>");
					}
				} else {
					# ����
					if (!$mode) {
						# �Ѹ���
						out("- ���� -<BR>");
					} else {
						# �����ʡ�
						out("$tan >(��) ${com} $speaker<BR>");
					}
				}
			} else {
				# ���
				out("$tan > ${com} $speaker<BR>");
			}
		}
	}
}

# ��ȯ�ײ�
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

# ��ȯ�ײ����Ͻ���
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

# ��ξ���
sub MislandInfo {
	my $mode = shift;
	my $island = $Hislands[$HcurrentNumber];

	# ����ɽ��
	my $rank = $HcurrentNumber + 1 - $HbfieldNumber;
	my $pop = $island->{'pop'};
	my $area = $island->{'area'};
	my $food = $island->{'food'};
	my $farm = $island->{'farm'};
	my $factory  = $island->{'factory'};
	my $mountain = $island->{'mountain'};
	my $name;

	# �͸���ɽ��
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
	$farm     = "��̩" if($Hhide_farm == 2);
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$factory  = "��̩" if($Hhide_factory == 2);
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;

	# ͽ�����֡����ȼԤ���¤���äƤ�����ٹ�
	my $mStr1 = '';
	if($Htournament && ($HislandTurn < $HyosenTurn)) {
		my $tmp = int($island->{'pop'} - ($farm + $factory + $mountain) * 10);
		$tmp = 0 if($tmp < 0);
		$mStr1 = "<FONT COLOR=RED>���ȼԤ�".$Hno_work.$HunitPop.
		"�ʾ�ФƤ���Τǡ��͸����ä����ȥåפ��ޤ����������ߤ���ƤƲ�������</FONT><br>" if($tmp >= $Hno_work);
		1 while $mStr1 =~ s/(.*\d)(\d\d\d)/$1,$2/;
	}

	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($mode == 1)) {
		# ̵���ޤ���owner�⡼��
		$mStr2 = "$island->{'money'}$HunitMoney";
	} elsif($HhideMoneyMode == 2) {
		$mStr2 = aboutMoney($island->{'money'});
	}
	1 while $mStr2 =~ s/(.*\d)(\d\d\d)/$1,$2/;

	# ��������ɽ��
	my $fight_name = '';
	if($island->{'fight_id'} > 0 && $island->{'pop'} > 0) {
		my $HcurrentNumber = $HidToNumber{$island->{'fight_id'}};
		if($HcurrentNumber ne '') {
			my $tIsland = $Hislands[$HcurrentNumber];
			my $name = '<A HREF="'.$HthisFile."?Sight=$tIsland->{'id'}&MP=$HinputPassword2\">$tIsland->{'name'}$AfterName</A>";
			$fight_name = "���: $name<br>";
		}
	}

	# ��ȯ��ߤ�ɽ��
	my $rest_msg = '';
	if($island->{'rest'} > 0 && $HislandNumber > 1 && $island->{'pop'} > 0) {
		$rest_msg = "���ﾡ�ˤ�곫ȯ����桡";
		$rest_msg .= "�Ĥ�<FONT COLOR=RED>".$island->{'rest'}."</FONT>������<br>";
	}

	my $cmd;
	if($mode) {
		$name = "$island->{'name'}$AfterName��ȯ����";
		$cmd  = '<br><input type="submit" name="Mobile3" value="�ײ����">';
		$cmd  .= '<input type="submit" name="Mobile4" value="�ײ�����">';
	} else {
		$name = "$island->{'name'}$AfterName�Ѹ�����";
	}

	out(<<END);
$name<br>
<hr>
���: $rank<br>
�͸�: $pop<br>
���: $mStr2<br>
����: $food<br>
����: $area<br>
����: $farm<br>
����: $factory<br>
�η�: $mountain<br>
$rest_msg
$fight_name
$mStr1
<hr>
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$island->{'id'}">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" name="Mobile1" value="�����">
<input type="submit" name="Mobile5" value="�Ǽ���">
$cmd
</form>
<hr>
END
}

# ����Ͽ�
sub MislandMap {
	my $mode = shift;
	my $island = $Hislands[$HcurrentNumber];

	# �Ϸ����Ϸ��ͤ����
	my($x, $y);
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};
	my(@mx) = @{$island->{'map'}->{'x'}};
	my(@my) = @{$island->{'map'}->{'y'}};
	my @co = ('��','��','��','��','��','��','��','��','��','��');
	# ��ɸ(��)�����
	foreach $x (@mx) {
		out("$co[($x%10)]");
	}
	out("<br>\n<FONT COLOR=\"#0000FF\">");

	# ���Ϸ�����Ӳ��Ԥ����
	foreach $y (@my) {
		# �����ֹ�ʤ��ֹ�����
		if(!($y % 2)) {
			my $line = ($y >= 10) ? $y-10 : $y;
			out($line);
		}

		# ���Ϸ������
		foreach $x (@mx) {
			my $l = $land->[$x][$y];
			my $lv = $landValue->[$x][$y];
			MlandString($l, $lv, $x, $y, $mode);
		}

		# ����ֹ�ʤ��ֹ�����
		if($y % 2) {
			my $line = ($y >= 10) ? $y-10 : $y;
			out($line);
		}

		# ���Ԥ����
		out("<br>\n");
	}

	out("</FONT>\n");
	out("&nbsp;");
	foreach $x (@mx) {
		out("$co[($x%10)]");
	}
	out("<br>\n");
}

# 1�إå���
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
			# ����
			$alt = '��';
#			$color = '#0000FF';
		} else {
			# ��
			$alt = '��';
#			$color = '#0000FF';
		}
	} elsif($l == $HlandWaste) {
		# ����
		$alt = '��';
		$color = '#800000';
	} elsif($l == $HlandPlains) {
		# ʿ��
		$alt = '��';
		$color = '#00F000';
	} elsif($l == $HlandForest) {
		# ��
		$alt = "��";
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
		# ����
		$alt = "��";
		$color = '#00FF00';
	} elsif($l == $HlandFactory) {
		# ����
		$alt = "��";
		$color = '#606060';
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# �Ѹ��Ԥξ��
			$alt = '��';
		} else {
			# �ߥ��������
			$alt = "��";
		}
		$color = '#008800';
	} elsif($l == $HlandSbase) {
		if($mode == 0) {
			# �Ѹ��Ԥξ��
			$alt = '��';
		} else {
			# �ߥ��������
			$alt = "��";
		}
#		$color = '#0000FF';
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		if($HdBaseHide && $mode == 0) {
			$alt = '��';
			$color = '#008800';
		} else {
			$alt = '��';
			$color = '#FF0000';
		}
	} elsif($l == $HlandBouha) {
		# ������
		$alt = "��";
		$color = '#008800';
	} elsif($l == $HlandSeaMine) {
		# ����
		if($mode == 0) {
			$alt = '��';
		} else {
			$alt = '��';
		}
#		$color = '#0000FF';
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		if($mode == 0) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$alt = '��';
		} else {
			$alt = '��';
		}
		$color = '#FF0000';
	} elsif($l == $HlandOil) {
		# ��������
		$alt = "��";
		$color = '#00FF00';
	} elsif($l == $HlandMountain) {
		# ��
		if($lv > 0) {
			$alt = "��";
		} else {
			$alt = '��';
		}
		$color = '#C03030';
	} elsif($l == $HlandCore) {
		# ����
		if($HcoreHide && $mode == 0) {
			if(int($lv/10000)) {
				# ��
				$alt = '��';
#				$color = '#0000FF';
			} else {
				$alt = '��';
				$color = '#008800';
			}
		} else {
			$alt = '��';
			$color = '#00FF00';
		}
	} elsif($l == $HlandComplex) {
		# ʣ���Ϸ�
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $cName = $HcomplexName[$cKind];
#		&jcode::tr(\$cName, '0-9A-Za-z', '��-����-�ڣ�-��');
		$alt = substr($cName, 0, 2);
		$color = '#00FF00';
	} elsif($l == $HlandMonster) {
		# ����
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$kind];
#		jcode::tr(\$mName, '0-9A-Za-z', '��-����-�ڣ�-��');
		$alt = substr($mName, 0, 2);
		$color = '#FF00FF';
	} elsif($l == $HlandHugeMonster) {
		# �������
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$kind];
#		jcode::tr(\$mName, '0-9A-Za-z', '��-����-�ڣ�-��');
		$alt = substr($mName, 0, 2);
		$color = '#FF00FF';
	} elsif($l == $HlandNavy) {
		# ����
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $hp) = navyUnpack($lv);
		my $nName = $HnavyName[$kind];
#		jcode::tr(\$nName, '0-9A-Za-z', '��-����-�ڣ�-��');
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
# HTML ����
#----------------------------------------------------------------------
# �����󹹿��Ԥ�
sub MturnPageMain {
	unlock();

	out("�����󹹿��Ԥ��Ǥ����ä��ԤäƤ��饢���������Ʋ�������");
}

# ���ֹ����
sub MlistPageMain {
	unlock();

	out("[���] $AfterName�ֹ�: $AfterName̾<hr>");
	for($i = 0; $i < $HislandNumber; $i++) {
		my $j = $i + 1 - $HbfieldNumber;
		$j = 'BF' if($j <= 0);
		my $island = $Hislands[$i];
		out("[$j] $island->{'id'}: $island->{'name'}$AfterName<br>\n");
	}
}

# �ײ�����
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
�ײ��ֹ�(1��$HcommandMax)<br>
[1]<input type="text" name="NUMBER" value="$HcommandPlanNumber" size="2" accesskey="1" istyle="4"><br>
<br>

�ײ�<br>
<select name="COMMAND" accesskey="2">
END

	#���ޥ��
	my($kind, $cost);
	for($i = 0; $i < $HcommandTotal; $i++) {
		my $s;
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
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
		$s = ' selected' if($kind == $HcommandKind);

		out("<option value='$kind'$s>$HcomName[$kind]($cost)\n");
	}

	out(<<END);
</select><br>
<br>
��ɸ(��,��)<br>
[2]<input type="text" name="POINTX" value="$HcommandX" size="2" accesskey="2" istyle="4"> , 
[3]<input type="text" NAME="POINTY" value="$HcommandY" size="2" accesskey="3" istyle="4"><br>
<br>

����(0��49)<br>
[4]<input type="text" name="AMOUNT" value="$HcommandArg" size="2" accesskey="4" istyle="4"><br>
<br>

��ɸ<br>
<select name="TARGETID" accesskey="6">
END
	out(getIslandList($island->{'id'},1,$island->{'fight_id'}));
	out(<<END);
<br>
</select><br>
<br>
ư��<br>
<input type="radio" name="COMMANDMODE" value="insert" accesskey="5" checked>[5]����<br>
<input type="radio" name="COMMANDMODE" value="write" accesskey="6">[6] ���<br>
<input type="radio" name="COMMANDMODE" value="delete" accesskey="7">[7] ���<br>
<br>
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" value="�ײ�����" name="CommandButton$island->{'id'}">
</form>
<hr>
END
	McmdListPageMain(int($HcommandMax/2));
}

# �ײ����
sub McmdListPageMain {
	my $max = shift;

	for($i = 0; $i < $max; $i++) {
		MtempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
	}
}

# �ײ�ɽ��
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
		# ���ޥ��̾�Τ�(��ɸ�ʤ�)
		out($name);
	} elsif ((($HcomMissile[0] < $kind) && ($kind <= $HcomMissile[$#HmissileName])) || ($kind == $HcomNavyTarget)) { # �ߥ�����ȯ��
		# �о��礢��(��ɸ�դ�)
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "̵��$AfterName" : "${target}$AfterName";

		$name =~ s/ȯ��//;
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
		# �о��礢��(��ɸ�ʤ�)
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "̵��$AfterName" : "${target}$AfterName";

		$name =~ s/ȯ��//;
		if($arg == 0) {
			out("${name}=>${target}");
		} else {
			out("${name}x${arg}=>${target}");
		}
	} elsif($kind == $HcomNavyMove) {
		$target = $HidToName{$target};
		$target =  ($target eq '') ? "̵��$AfterName" : "${target}$AfterName";
		$target2 = $HidToName{$target2};
		$target2 =  ($target2 eq '') ? "̵��$AfterName" : "${target2}$AfterName";
		out("${name}=>${target}->${target2}");
	} elsif(($kind == $HcomSell) ||
		($kind == $HcomBuy) ||
		($kind == $HcomPropaganda)) {
		# ����դ�
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
		 (($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) || # ʣ���Ϸ�����
		 ($kind == $HcomMountain)) {
		# ��ɸ������դ�
		if($arg == 0) {
			out("${name}=>${point}");
		} else {
			out("${name}x${arg}=>${point}");
		}
	} else {
		# ��ɸ�դ�
		out("${name}=>${point}");
	}

	out("<br>\n");
}

# �Ƽ���
sub MlinkPageMain {
#	my $bbTime = get_time((stat($bbsLog))[9], 1, 1);
	unlock();

	out(<<END);
- <A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A><br>
- <A HREF="http://no-one.s53.xrea.com/">����JS��¤���۸�</A><br>
END
#	out(<<END);
#<BR>
#- <A HREF="$toppage">�ۡ���</A><br>
#- <A HREF="$bbs">$bbsname</A>$bbTime<br>
#END
}

# �ޥåץإ��
sub MhelpPageMain {
	unlock();

	out(<<END);
<font color="#0000FF">��</font> �� ����<br>
<font color="#0000FF">��</font> �� ��<br>
<font color="#800000">��</font> �� ����<br>
<font color="#00F000">��</font> �� ʿ��<br>
<font color="#008800">��</font> �� ��<br>
<br>
<font color="#00FF00">��</font> �� ����<br>
<font color="#606060">��</font> �� ����<br>
<font color="#C03030">��</font> �� �η���<br>
<font color="#C03030">��</font> �� ��<br>
<font color="#00FF00">��</font> �� ��������<br>
<br>
<font color="#008800">��</font> �� �ߥ��������<br>
<font color="#0000FF">��</font> �� �������<br>
<font color="#FF0000">��</font> �� �ɱһ���<br>
<font color="#FF0000">��</font> �� �ϥ�ܥ�<br>
<font color="#008800">��</font> �� ������<br>
<font color="#0000FF">��</font> �� ����<br>
<font color="#FF00FF">��</font> �� ����<br>
<br>
END

	out("���ԻԷϡ�<br>");
	foreach(@HlandTownName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#996600\">$alt</font> �� $_<br>");
	}
	out("��ʣ���Ϸ���<br>");
	foreach(@HcomplexName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#00FF00\">$alt</font> �� $_<br>");
	}
	out("<br>�ڳ�����<br>");
	foreach(@HnavyName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#0000FF\">$alt</font> �� $_<br>");
	}
	out("<br>�ڲ��á�<br>");
	foreach(@HmonsterName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#FF00FF\">$alt</font> �� $_<br>");
	}
	out("<br>�ڵ�����á�<br>");
	foreach(@HhugeMonsterName) {
		my $alt = substr($_, 0, 2);
		out("<font color=\"#FF00FF\">$alt</font> �� $_<br>");
	}
}

# �ȥåץڡ���
sub MtopPageMain {
	unlock();

	if($HinputPassword2 ne '') {
		$sL[$HinputPassword2] = ' selected';
	} else {
		$sL[1] = ' selected';
	}

	if($HislandNumber > 1 || $HislandTurn == 0) {
		#������ɽ��
		my($hour, $min, $sec);
		my($now) = time;
		my($showTIME) = ($HislandLastTime + $HunitTime - $now);
		$hour = int($showTIME / 3600);
		$min  = int(($showTIME - ($hour * 3600)) / 60);
		$sec  = $showTIME - ($hour * 3600) - ($min * 60);
		if ($sec < 0 or $HislandTurnCount > 1){
			out("(�����󹹿��Ԥ��Ǥ����ä��ԤäƤ��饢���������Ʋ�������)");
		} else {
			if(!$Htime_mode) {
				my($sec2,$min2,$hour2,$mday2,$mon2) = get_time($HislandLastTime + $HunitTime);
				out("���󹹿����� $mon2��$mday2��$hour2��$min2ʬ<br>�Ĥ� $hour���� $minʬ $sec��");
			} else {
				out("�ʼ��Υ�����ޤǡ����� $hour���� $minʬ $sec�á�");
			}
		}
	}

	out(<<END);
<hr>
<form action="./hako-main.cgi" method="POST">
ID:<input type="text" name="ISLANDID" size="3" value="$HcurrentID" istyle="4"><br>
PS:<input type="text" name="PASSWORD" size="6" value="$HinputPassword" istyle="3"><br>
���顼�⡼��:<br>
<select name="PASSWORD2">
<option$sL[0] value="0">ɸ��
<option$sL[1] value="1">�ե륫�顼
</select><br>
<input type="submit" name="Mobile2" value="��ȯ">
<input type="submit" name="Mobile0" value="�Ѹ�">
<input type="submit" name="Mobile1" value="�����">
<input type="submit" name="Mobile5" value="�Ǽ���">
</form>

<br>
<a href="./hako-main.cgi?TimeTable=1">$AfterName�ֹ����</a> 
END
}

# �Ͽ޲��̤ؤΥե�������
sub MtoMapLink {
	my $mode = shift;

	my $name = ($mode) ? '��ȯ' : '�Ѹ�';
	my $num  = ($mode) ? 2 : 0;

	out(<<END);
<form action="./hako-main.cgi" method="POST">
<input type="hidden" name="ISLANDID" value="$HcurrentID">
<input type="hidden" name="PASSWORD" value="$HinputPassword">
<input type="hidden" name="PASSWORD2" value="$HinputPassword2">
<input type="submit" name="Mobile${num}" value="${name}����">
<input type="submit" name="Mobile5" value="�Ǽ���">
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

