#----------------------------------------------------------------------
# Ȣ����� ���� JS ver7.xx
# �����⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �����ͤˤ�������۹���ƥʥ�
#----------------------------------------------------------------------
sub dewarSetupMain() {
	if ($HwsetupMode) {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HdefaultPassword)) {
			# �ü�ѥ����
			undef @HwarIsland;
			for($i=0;$i < $#HdeWarChange;$i+=4){
				my($turn) = $HdeWarChange[$i];
				my($id1)  = $HdeWarChange[$i+1];
				my($id2)  = $HdeWarChange[$i+2];
				my($flag) = $HdeWarChange[$i+3];
				if(!$turn || $HdeWarDel{$i} || ($id1 == $id2)) {
				} else {
					push(@HwarIsland, ($turn, $id1, $id2, $flag));
				}
			}
			writeIslandsFile();
			# �ѹ�����
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# �ƥ�ץ졼�Ƚ���
	tempDeWarSetupPage();
}

# �����۹���ƥʥ󥹥ڡ���
sub tempDeWarSetupPage() {
	# ����
	unlock();
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='campInfo'>
<H1>�����۹� ����</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="WSetup">
<TABLE BORDER><TR>
<TH $HbgTitleCell colspan=5>${HtagTH_}�����۹�����${H_tagTH}��<INPUT TYPE="submit" VALUE="�ѹ�" NAME="WarChangeButton"></TH>
</TR><TR>
<TD align="center">${HtagTH_}���${H_tagTH}</TD>
<TD align="center">${HtagTH_}���ϥ�����${H_tagTH}</TD>
<TD align="center">${HtagTH_}�����۹𤷤�${AfterName}${H_tagTH}</TD>
<TD align="center">${HtagTH_}�����۹𤵤줿${AfterName}${H_tagTH}</TD>
<TD align="center">${HtagTH_}����${H_tagTH}</TD></TR>
END

	my($i, $j, %warFlag);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($turn)  = $HwarIsland[$i];
		my($id1)   = $HwarIsland[$i+1];
		my($id2)   = $HwarIsland[$i+2];
		my($flag)  = $HwarIsland[$i+3] % 10;
		my($fturn) = int($HwarIsland[$i+3] / 10);

		my $islandList1 = getIslandList($id1, 1, 'yellow');
		my $islandList2 = getIslandList($id2, 1, 'yellow');
		my $turnList = "<OPTION VALUE=\"$turn\" style=\"background:yellow;\" selected>$turn";
		for($j=$turn+1;$j<$turn+100;$j++) {
			$turnList .= "<OPTION VALUE=\"$j\">$j";
		}
		my @s = ('', '', '');
		$s[$flag] = " style=\"background:yellow;\" selected";
		my($t1, $t2);
		$t1 = ($fturn) ? $fturn : $HislandTurn;
		$t1 *= 10;
		$t1++;
		$t2 = $t1 + 1;

		out(<<END);
<TR>
<TD align="center"><input type=checkbox name=del value="$i"></TD>
<TD align="center"><select name=war>$turnList</select></TD>
<TD align="center"><select name=war>$islandList1</select></TD>
<TD align="center"><select name=war>$islandList2</select></TD>
<TD align="center"><select name=war>
<OPTION VALUE="0"$s[0]>������
<OPTION VALUE="$t1"$s[1]>��������(�۹�¦)
<OPTION VALUE="$t2"$s[2]>��������(���۹�¦)
</select></TD></TR>
END
	}
	my $turnList = "<OPTION VALUE=\"0\" style=\"background:red;\" selected>�ɲä��ʤ�";
	for($j=$HislandTurn+1;$j<$HislandTurn+100;$j++) {
		$turnList .= "<OPTION VALUE=\"$j\">$j";
	}
	my $islandList = getIslandList(0, 1);
	$t1 = $HislandTurn * 10 + 1;
	$t2 = $t1 + 1;
	out(<<END);
<TR>
<TH>����</TH>
<TH><select name=war>$turnList</select></TH>
<TD align="center"><select name=war>$islandList</select></TD>
<TD align="center"><select name=war>$islandList</select></TD>
<TD align="center"><select name=war>
<OPTION VALUE="0">������
<OPTION VALUE="$t1">��������(�۹�¦)
<OPTION VALUE="$t2">��������(���۹�¦)
</select></TD></TR>
</TABLE><INPUT TYPE="hidden" VALUE="dummy" NAME="WarChange"></FORM></DIV>
END
}

#----------------------------------------------------------------------
# �����ͤˤ��ͧ����Ʊ��(�ر�)����
#----------------------------------------------------------------------
sub amitySetupMain() {
	if ($HasetupMode) {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HdefaultPassword)) {
			# �ü�ѥ����
			my($id, $aId);
			foreach (0..$islandNumber) {
				undef $Hislands[$_]->{'amity'};
				undef $Hislands[$_]->{'allyId'};
			}
			my $allyNumber = $HallyNumber - 1;
			foreach (0..$allyNumber) {
				undef $Hally[$_]->{'memberId'};
				undef $Hally[$_]->{'number'};
				undef $Hally[$_]->{'score'};
				my $aId = $Hally[$_]->{'id'};
				if(defined $HidToNumber{$aId}) {
					push(@{$Hally[$_]->{'memberId'}}, $Hally[$_]->{'id'});
					$Hally[$_]->{'score'} += $Hislands[$HidToNumber{$aId}]->{$HrankKind} if(!$Hislands[$HidToNumber{$aId}]->{'predelete'});
					push(@{$Hislands[$HidToNumber{$aId}]->{'allyId'}}, $aId);
				}
			}
			foreach (@HamityChange) {
				($id, $aId) = split(/-/, $_);
				push(@{$Hislands[$HidToNumber{$id}]->{'amity'}}, $aId);
			}
			foreach (@HallyChange) {
				($id, $aId) = split(/-/, $_);
				$Hally[$HidToAllyNumber{$aId}]->{'score'} += $Hislands[$HidToNumber{$id}]->{$HrankKind} if(!$Hislands[$HidToNumber{$id}]->{'predelete'});
				next if($id == $aId);
				push(@{$Hally[$HidToAllyNumber{$aId}]->{'memberId'}}, $id);
				push(@{$Hislands[$HidToNumber{$id}]->{'allyId'}}, $aId);
			}
			foreach (0..$allyNumber) {
				$Hally[$_]->{'number'} = @{$Hally[$_]->{'memberId'}};
			}
			allyOccupy();
			allySort();
			writeIslandsFile();
			# �ѹ�����
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# �ƥ�ץ졼�Ƚ���
	tempAmitySetupPage();
}

# ͧ��������ڡ���
sub tempAmitySetupPage() {
	# ����
	unlock();
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='campInfo'>
<H1>ͧ����Ʊ��(�ر�)����</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="ASetup">
<TABLE BORDER><TR>
<TH $HbgTitleCell rowspan=2>${HtagTH_}ͧ��������${H_tagTH}<BR><INPUT TYPE="submit" VALUE="�ѹ�" NAME="AmityChangeButton"></TH>
END

	my($i, %warFlag);
	for($i=0;$i < $#HwarIsland;$i+=4){
		my($id1) = $HwarIsland[$i+1];
		my($id2) = $HwarIsland[$i+2];
		my($tn1) = $HidToNumber{$id1};
		my($tn2) = $HidToNumber{$id2};
		next if(($tn1 eq '') || ($tn2 eq ''));
		$warFlag{"$id1,$id2"} = 1;
	}
	foreach (0..$islandNumber) {
		$Hislands[$_]->{'ally'} = $Hislands[$_]->{'allyId'}[0];
	}
	my @idx = (0..$#Hislands);
	@idx = sort {
			$Hislands[$b]->{'field'} <=> $Hislands[$a]->{'field'} || # �Хȥ�ե������ͥ��
			$Hislands[$b]->{'ally'} <=> $Hislands[$a]->{'ally'} || # Ʊ���ǥ�����
			$a <=> $b # $kind��Ʊ���ʤ�����Τޤ�
		   } @idx;

	my $aStr = ($HarmisticeTurn) ? '�ر�' : 'Ʊ��';
	out("<TH $HbgTitleCell colspan=$HislandNumber>${HtagTH_}${AfterName}̾${H_tagTH}</TH>\n");
	out("<TH $HbgTitleCell colspan=$HallyNumber>${HtagTH_}${aStr}${H_tagTH}</TH>") if($HallyNumber);
	out("</TR><TR>\n");
	my($number, $island, $name, $ally);
	foreach (0..$islandNumber) {
		$island = $Hislands[$idx[$_]];
		$name = islandName($island);
		out(<<END);
<TD class='T'>$name</TD>
END
	}
	my $allyNumber = $HallyNumber - 1;
	foreach (0..$allyNumber) {
		$ally = $Hally[$_];
		$name = "<FONT COLOR=\"$ally->{'color'}\"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}";
		out(<<END);
<TD class='T'>$name</TD>
END
	}
	out("</TR>\n");
	foreach (0..$islandNumber) {
		$island = $Hislands[$idx[$_]];
		$name = islandName($island);
		my($id, $amity, %amityFlag, $aId);
		$id = $island->{'id'};
		$amity = $island->{'amity'};
		foreach (@$amity) {
			$amityFlag{$_} = 1;
		}
		out("<TR><TH $HbgTitleCell>$name</TH>");
		foreach $number (0..$islandNumber) {
			$aId = $Hislands[$idx[$number]]->{'id'};
			if($id == $aId) {
				out("<TD align=\"center\">��</TD>");
			} elsif($warFlag{"$id,$aId"}) {
				out("<TD align='center'>${HtagDisaster_}��${H_tagDisaster}</TD>\n");
			} elsif($warFlag{"$aId,$id"}) {
				out("<TD align='center'>${HtagDisaster_}x${H_tagDisaster}</TD>\n");
			} elsif($amityFlag{$aId}) {
				out("<TD align=\"center\"><input type=checkbox name=amity value=\"$id-$aId\" CHECKED></TD>");
			} else {
				out("<TD align=\"center\"><input type=checkbox name=amity value=\"$id-$aId\"></TD>");
			}
		}
		for ($i = 0; $i < $HallyNumber; $i++) {
			$ally  = $Hally[$i];
			$aId = $ally->{'id'};
			my $member = $Hally[$i]->{'memberId'};
			my $flag = 1;
			foreach (@$member) {
				if($id == $_) {
					$flag = 0;
					last;
				}
			}
			if($flag) {
				out("<TD align=\"center\"><input type=checkbox name=ally value=\"$id-$aId\"></TD>");
			} else {
				out("<TD align=\"center\"><input type=checkbox name=ally value=\"$id-$aId\" CHECKED></TD>");
			}
		}
		out("</TR>\n");
	}
	out(<<END);
</TABLE><INPUT TYPE="hidden" VALUE="dummy" NAME="AmityChange"></FORM></DIV>
END
}

#----------------------------------------------------------------------
# �����ͤˤ��ץ쥼��ȥ⡼��
#----------------------------------------------------------------------
sub presentMain {
	if (!$HpresentMode) {
		# ����
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();

		# �ƥ�ץ졼�Ƚ���
		tempPresentPage();
	} else {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HoldPassword)) {
			# �ü�ѥ����

			if (!$HpresentMoney && !$HpresentFood) {
				# ��⿩����ʤ�
				tempPresentEmpty();
				unlock();
				return;
			}

			# id����������
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($name)   = $island->{'name'};

			$island->{'money'} += $HpresentMoney;
			$island->{'money'} = 0 if ($island->{'money'} < 0);
			$island->{'food'}  += $HpresentFood;
			$island->{'food'} = 0 if ($island->{'food'} < 0);

			logPresent($HcurrentID, $name, $HpresentLog);

			# �ǡ����񤭽Ф�
			writeIslandsFile($HcurrentID);
			unlock();

			# �ѹ�����
			tempPresentOK($name);
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# �ץ쥼��ȥ⡼�ɤΥȥåץڡ���
sub tempPresentPage {
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>����${AfterName}�˥ץ쥼��Ȥ�£��</H1>

<FORM action="$HthisFile" method="POST">
<B>�ץ쥼��Ȥ�������${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
<BR>
<B>�ץ쥼��Ȥ����Ƥϡ�(�ޥ��ʥ��ͤ��ǽ)</B><BR>
<INPUT TYPE="text" NAME="PRESENTMONEY" VALUE="0" SIZE=16 MAXLENGTH=16>$HunitMoney<BR>
<INPUT TYPE="text" NAME="PRESENTFOOD"  VALUE="0" SIZE=16 MAXLENGTH=16>$HunitFood<BR>
<BR>
<B>����å������ϡ�(��ά��ǽ����Ƭ��${AfterName}̾����������ޤ�)<small>(����${HlengthPresentLog}���ޤ�)</small></B><BR>
����${AfterName}<INPUT TYPE="text" NAME="PRESENTLOG"  VALUE="" SIZE=128 MAXLENGTH=256><BR>
<BR>
<B>�ޥ������ѥ���ɤϡ�</B><BR>
<INPUT TYPE="password" NAME="OLDPASS" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f><BR>
<INPUT TYPE="submit" VALUE="�ץ쥼��Ȥ�£��" NAME="PresentButton"><BR>
</FORM>
END
}

# �ץ쥼��ȴ�λ
sub tempPresentOK {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}�˥ץ쥼��Ȥ�£��ޤ���${H_tagBig}$HtempBack
END
}

# �ץ쥼������Ƥ���������
sub tempPresentEmpty {
	out(<<END);
${HtagBig_}�ץ쥼��Ȥ����Ƥ����������褦�Ǥ�${H_tagBig}$HtempBack
END
}

# �ץ쥼���
sub logPresent {
	my($id, $name, $log) = @_;
	logHistory("${HtagName_}${name}��${H_tagName}$log") if ($log ne '');
}

#----------------------------------------------------------------------
# �����ͤˤ�����ۥ⡼��
#----------------------------------------------------------------------
sub punishMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# �ü�ѥ����
		if ($HpunishMode) {
			my(%punish);
			if (open(Fpunish, "<${HdirName}/punish.cgi")) {
				local(@_);
				while (<Fpunish>) {
					chomp;
					@_ = split(',');
					my($obj);
					$obj->{id} = shift;
					$obj->{punish} = shift;
					$obj->{x} = shift;
					$obj->{y} = shift;
					$punish{$obj->{id}} = $obj;
				}
				close(Fpunish);
			}

			if (open(Fpunish, ">${HdirName}/punish.cgi")) {
				{
					my($obj);
					$obj->{id} = $HcurrentID;
					$obj->{punish} = $HpunishID;
					$obj->{x} = $HcommandX;
					$obj->{y} = $HcommandY;
					$punish{$obj->{id}} = $obj;
				}

				my($key, $obj);
				while (($key, $obj) = each %punish) {
					next if ($obj->{punish} == 0);
					print Fpunish
						$obj->{id} . ','.
						$obj->{punish} . ','.
						$obj->{x} . ','.
						$obj->{y} . "\n";
				}
				close(Fpunish);
			}
		}
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempPunishPage();

	} else {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
#		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
#		require('./hako-top.cgi');
#		unlock();
#		# �ƥ�ץ졼�Ƚ���
#		tempTopPage();
	}
}

# ���ۥ⡼�ɤΥȥåץڡ���
sub tempPunishPage {
	my(@punishName) =
		(
		 '�ʤ�', # 0
		 '�Ͽ�', # 1
		 '����', # 2
		 '���áʿ͸���說�ꥢ���Τߡ�', # 3
		 '������áʿ͸���說�ꥢ���Τߡ�', # 4
		 '��°���������ʿ͸���說�ꥢ���Τߡ�', # 5
		 '�������������Ѿ�說�ꥢ���Τߡ�', # 6
		 '����', # 7
		 '������Сʺ�ɸ�����', # 8
		 '���', # 9
		 'ʮ�Сʺ�ɸ�����', # 10
		 );

	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>����${AfterName}�����ۤ�ä���</H1>

<DL>
<DT>���֥롼��˰�ȿ�����פȻפ����ˡ��֤��Υ롼���ï�⤬�ɤ����˽񤤤Ƥ��뤫���פ��ǧ���ޤ��礦��</DT>
<DT>�����ۤ�ä���ΤϤ��䤹�����ȤǤ����������˴����ͤȤ��Ƥ�Ω��ǹԤäƤ��뤫�ͤ��ޤ��礦��</DT>
<DT>�����ۤ�ä��ʤ���Фʤ�ʤ��ۤ��ﳲ���礭�����ͤ��ޤ��礦���ڤ��������ǹ��⤹��ͤϤ��ĤǤ⤤���ΤǤ���</DT>
<DT>��<span class=attention>���ۤ�¸�ߤ϶���ˤ��ޤ��礦��</span>���ۤ����餫�ˤʤ��¾�Υץ쥤�䡼�Ȥο���ط�������ޤ���</DT>
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Punish">
<B>���ۤ�ä���${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="�ޥåפ򳫤�" onclick="printIsland();">
<BR><BR>
<B>��ɸ�ϡ��ʺ�ɸ����Ǥ������ۤǤΤ�ͭ����</B><BR>
<B>(</B><SELECT NAME=POINTX>
END

	my($i);
	foreach $i (@defaultX) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>, </B><SELECT NAME=POINTY>
END

	foreach $i (@defaultY) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>)</B><BR>
<BR>
<B>���ۤ����Ƥϡ�</B><BR>
<SELECT NAME="PUNISHID">
END

	for($i = 0; $i < $#punishName + 1; $i++) {
		out("<OPTION VALUE=\"$i\">$punishName[$i]\n");
	}

	out(<<END);
</SELECT><BR>
<BR>
<INPUT TYPE="submit" VALUE="���ۤ�ä���" NAME="PunishButton"><BR>
</FORM>
<SCRIPT Language="JavaScript">
<!--

function printIsland() {
	var iid;
	with (document.lcForm.ISLANDID) {
		iid = options[selectedIndex].value;
	}
	window.open("$HthisFile?Sight=" + iid + "&ADMINMODE=$HdefaultPassword", "punish", "toolbar=0,location=0,directories=0,menubar=0,status=1,scrollbars=1,resizable=1,width=450,height=630");
}
//-->
</SCRIPT>
END

	if (open(Fpunish, "<${HdirName}/punish.cgi")) {
		out('<HR>');
		out("<TABLE BORDER><TR><TH>${AfterName}̾</TH><TH>��������</TH><TH>��ɸ</TH></TR>");
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

			$HcurrentNumber = $HidToNumber{$obj->{id}};
			$island = $Hislands[$HcurrentNumber];

			out("<TR><TD>$island->{'name'}${AfterName}</TD><TD>$punishName[$obj->{punish}]</TD><TD>($obj->{x}, $obj->{y})</TD></TR>");
		}
		out('</TABLE>');
		close(Fpunish);
	}
}

#----------------------------------------------------------------------
# �����ͤˤ���Ϸ��ѹ��⡼��
#----------------------------------------------------------------------
sub lchangeMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# �ü�ѥ����
		if ($HlchangeMode) {
			# id����������
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($land) = $island->{'land'};
			my($landValue) = $island->{'landValue'};

			# �Ϸ����ͤ�������������å�(�����å��������ʤ����ϥ����ȥ����Ȥ��Ʋ�����)
			if(!landCheck($HlchangeKIND, $HlchangeVALUE)) {
				tempBadValue();
				unlock();
				return;
			}

			$land->[$HcommandX][$HcommandY] = $HlchangeKIND;
			$landValue->[$HcommandX][$HcommandY] = $HlchangeVALUE;

			# �ǡ����񤭽Ф�
			writeIslandsFile($HcurrentID);
			unlock();

			# �ѹ�����
			tempLchangeOK($island->{'name'});
		}
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempLchangePage();
	} else {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
#		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
#		require('./hako-top.cgi');
#		unlock();
#		# �ƥ�ץ졼�Ƚ���
#		tempTopPage();
	}
}

# �Ϸ��ѹ��⡼�ɤΥȥåץڡ���
sub tempLchangePage {

	my($expOption, $hpOption) = ('', '');
	my($i);

	foreach $i (0..250) {
		$expOption .= "<OPTION VALUE=$i>$i\n";
	}
	foreach $i (0..31) {
		$hpOption .= "<OPTION VALUE=$i>$i\n";
	}

	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>����${AfterName}���Ϸ��ǡ������ѹ�����</H1>

<DL>
<DT>�����Ϸ����͡פˤĤ��Ƥ��μ����ʤ���С����Ѥ��񤷤����⤷��ޤ���</DT>
<DT>���äˡֲ��áסֳ����ס�ʣ���Ϸ��פˤĤ��Ƥϡ��μ������äƤ��񤷤��Ȼפ��ޤ���</DT>
<DT>�����Ϸ��פ��Ф���<B>���Ϸ����͡פ�Ŭ�ڤǤ��뤫�ɤ����ʰ�Ƚ��򤷤Ƥ��ޤ�</B>�Τǡ���դ��Ƥ���������</DT>
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Lchange">
<B>�Ϸ����ѹ�����${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="�ޥåפ򳫤�" onclick="printIsland();">
<BR><BR>
<B>��ɸ�ϡ�</B><BR>
<B>(</B><SELECT NAME=POINTX>
END

	foreach $i (@defaultX) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>, </B><SELECT NAME=POINTY>
END

	foreach $i (@defaultY) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>)</B><BR>
<BR>
<B>�Ϸ��ϡ�</B><BR>
<SELECT NAME="LCHANGEKIND">
<OPTION VALUE="$HlandSea">$HlandName[$HlandSea][0]
<OPTION VALUE="$HlandWaste">$HlandName[$HlandWaste][0]
<OPTION VALUE="$HlandPlains">$HlandName[$HlandPlains]
<OPTION VALUE="$HlandTown">$HlandName[$HlandTown]
<OPTION VALUE="$HlandForest">$HlandName[$HlandForest]
<OPTION VALUE="$HlandFarm">$HlandName[$HlandFarm]
<OPTION VALUE="$HlandFactory">$HlandName[$HlandFactory]
<OPTION VALUE="$HlandBase">$HlandName[$HlandBase]
<OPTION VALUE="$HlandDefence">$HlandName[$HlandDefence][0]
<OPTION VALUE="$HlandMountain">$HlandName[$HlandMountain][0]
<OPTION VALUE="$HlandMonster">$HlandName[$HlandMonster]
<OPTION VALUE="$HlandSbase">$HlandName[$HlandSbase]
<OPTION VALUE="$HlandOil">$HlandName[$HlandOil]
<OPTION VALUE="$HlandMonument">$HlandName[$HlandMonument]
<OPTION VALUE="$HlandHaribote">$HlandName[$HlandHaribote]
<OPTION VALUE="$HlandNavy">$HlandName[$HlandNavy]
<OPTION VALUE="$HlandBouha">$HlandName[$HlandBouha]
<OPTION VALUE="$HlandSeaMine">$HlandName[$HlandSeaMine]
<OPTION VALUE="$HlandHugeMonster">$HlandName[$HlandHugeMonster]
<OPTION VALUE="$HlandComplex">$HlandName[$HlandComplex]
<OPTION VALUE="$HlandCore">$HlandName[$HlandCore][0]
</SELECT><BR>
<BR>
<B>�Ϸ����ͤϡ�</B><BR>
<INPUT TYPE="text" SIZE=15 NAME="LCHANGEVALUE" VALUE="0"><BR>
<BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="LchangeButton"><BR>
<BR>
<BR>
<B>���ݡ��ȥġ���</B>
<table>
<tr>
<td rowspan=2>ʣ��<BR>�Ϸ�</td>
<td>����</td>
<td>������ե饰</td>
<td>�����ե饰</td>
<td>���ե饰</td>
</tr>
<tr>
END

	my($complexKindName, $complexOption1, $complexOption2);
	foreach $i (0..$#HcomplexName) {
		$complexKindName .= "<OPTION VALUE=$i>$HcomplexName[$i]\n";
	}
	foreach $i (0..500) {
		$complexOption1 .= "<OPTION VALUE=$i>$i\n";
	}
	foreach $i (0..50) {
		$complexOption2 .= "<OPTION VALUE=$i>$i\n";
	}

	out(<<END);
<td><SELECT name=complexKIND onChange=complexPack() onClick=complexPack()>$complexKindName</SELECT></td>
<td><SELECT name=complexTURN onChange=complexPack() onClick=complexPack()>$complexOption1</td>
<td><SELECT name=complexFOOD onChange=complexPack() onClick=complexPack()>$complexOption2</SELECT></td>
<td><SELECT name=complexMONEY onChange=complexPack() onClick=complexPack()>$complexOption2</SELECT></td>
</tr>
</table>
<table>
<tr>
<td rowspan=2>����</td>
<td>��ID</td>
<td>�����ե饰</td>
<td>�и���</td>
<td>�ե饰</td>
<td>����</td>
<td>�ѵ���</td>
</tr>
<tr>
<td><SELECT name=landID onChange=monsterPack() onClick=monsterPack()>$HislandList<OPTION VALUE=0>��°��ʤ�</SELECT></td>
<td><SELECT name=seaFLAG onChange=monsterPack() onClick=monsterPack()><OPTION value=0>��<OPTION value=1>����</SELECT></td>
<td><SELECT name=landEXP onChange=monsterPack() onClick=monsterPack()>$expOption</SELECT></td>
<td><SELECT name=landFLAG1 onChange=monsterPack() onClick=monsterPack()><OPTION value=0>Φ��<OPTION value=1>����(����)</SELECT>
<SELECT name=landFLAG2 onChange=monsterPack() onClick=monsterPack()><OPTION value=0>�Ų�����<OPTION value=1>�Ų���</SELECT></td>
<td><SELECT name=landKIND onChange=monsterPack() onClick=monsterPack()>
END

	for($i = 0; $i < $HmonsterNumber; $i++) {
		out("<OPTION VALUE=$i>$HmonsterName[$i]\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=landHP onChange=monsterPack() onClick=monsterPack()>$hpOption</SELECT></td>
</tr>
</table>
<table>
<tr>
<td rowspan=2>����</td>
<td>��ID</td>
<td>����</td>
<td>�����ե饰</td>
<td>�и���</td>
<td>�ե饰</td>
<td>�����ֹ�</td>
<td>����</td>
<td>�ѵ���</td>
</tr>
<tr>
<td><SELECT name=navyID onChange=navypack() onClick=navypack()>$HislandList<OPTION VALUE=0>��°��ʤ�</SELECT></td>
<td><SELECT name=status onChange=navypack() onClick=navypack()><OPTION value=0>�̾�<OPTION value=1>�༣<OPTION value=2>���<OPTION value=3>����</SELECT></td>
<td><SELECT name=seaFLAG2 onChange=navypack() onClick=navypack()><OPTION value=0>��<OPTION value=1>����</SELECT></td>
<td><SELECT name=navyEXP onChange=navypack() onClick=navypack()>
END

	foreach $i (0..$HmaxExpNavy) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=navyFLAG1 onChange=navypack() onClick=navypack()><OPTION value=0>����<OPTION value=1>����</SELECT>
<SELECT name=navyFLAG2 onChange=navypack() onClick=navypack()><OPTION value=0>��¸<OPTION value=1>�ĳ�</SELECT></td>
<td><SELECT name=navyNO>
END

	foreach $i (0..3) {
		my $j = $i + 1;
		out("<OPTION VALUE=$i>��$j����\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=navyKIND onChange=navypack() onClick=navypack()>
END

	for($i = 0; $i < $#HnavyName + 1; $i++) {
		out("<OPTION VALUE=$i>$HnavyName[$i]\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=navyHP onChange=navypack() onClick=navypack()>
END

	foreach $i (0..15) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT></td>
</tr>
</table>
<table>
<tr>
<td rowspan=2>����<br>����</td>
<td>��ID</td>
<td>������åե饰</td>
<td>�����ե饰</td>
<td>�и���</td>
<td>�ե饰</td>
<td>����</td>
<td>�ѵ���</td>
</tr>
<tr>
<td><SELECT name=hlandID onChange=hmonsterPack() onClick=hmonsterPack()>$HislandList<OPTION VALUE=0>��°��ʤ�</SELECT></td>
<td><SELECT name=hugeFLAG onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>����<OPTION value=1>����<OPTION value=2>��<OPTION value=3>����<OPTION value=4>����<OPTION value=5>��<OPTION value=6>����</SELECT></td>
<td><SELECT name=hseaFLAG onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>��<OPTION value=1>����</SELECT></td>
<td><SELECT name=hlandEXP onChange=hmonsterPack() onClick=hmonsterPack()>$expOption</SELECT></td>
<td><SELECT name=hlandFLAG1 onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>Φ��<OPTION value=1>����(����)</SELECT>
<SELECT name=hlandFLAG2 onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>�Ų�����<OPTION value=1>�Ų���</SELECT></td>
<td><SELECT name=hlandKIND onChange=hmonsterPack() onClick=hmonsterPack()>
END

	for($i = 0; $i < $HhugeMonsterNumber; $i++) {
		out("<OPTION VALUE=$i>$HhugeMonsterName[$i]\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=hlandHP onChange=hmonsterPack() onClick=hmonsterPack()>$hpOption</SELECT></td>
</tr>
</table>
<BR>
<BR>
<B>����(�Ϸ�����)</B>
<ul type="disc">
<li>$HlandName[$HlandSea][0] ======> 0:$HlandName[$HlandSea][0]��1:$HlandName[$HlandSea][1]
<li>$HlandName[$HlandWaste][0] ====> 0:$HlandName[$HlandWaste][0]��1:$HlandName[$HlandWaste][1]
<li>$HlandName[$HlandMountain][0] ======> 0:$HlandName[$HlandMountain][0]��1:$HlandName[$HlandMountain][1]
<li>$HlandName[$HlandDefence][0] ==> ����+1���ѵ���
<li>$HlandName[$HlandCore][0] ==> ���ͤβ�2����+1���ѵ��ϡ����ͤ�10000�ΰ̤������Ϸ�(00000:ʿ��($HlandName[$HlandCore][0])��10000:����($HlandName[$HlandCore][1])��20000:��($HlandName[$HlandCore][2]))
</ul>

END

	out(<<END);
</FORM>
<SCRIPT Language="JavaScript">
<!--

function printIsland() {
	var iid;
	with (document.lcForm.ISLANDID) {
		iid = options[selectedIndex].value;
	}
	window.open("$HthisFile?Sight=" + iid + "&ADMINMODE=$HdefaultPassword", "lcmap", "toolbar=0,location=0,directories=0,menubar=0,status=1,scrollbars=1,resizable=1,width=450,height=630");
}

function complexPack() {
	a = Math.floor(document.lcForm.complexKIND.value);
	b = Math.floor(document.lcForm.complexTURN.value);
	c = Math.floor(document.lcForm.complexFOOD.value);
	d = Math.floor(document.lcForm.complexMONEY.value);

	if(b > 500) b = 500;
	if(c > 50) c = 50;
	if(d > 50) d = 50;

	e = a * Math.pow(2, 21) + b * Math.pow(2, 12) + c * Math.pow(2, 6) + d;

	document.lcForm.LCHANGEVALUE.value = e;
	document.lcForm.LCHANGEKIND.options.value = $HlandComplex;
	return true;
}

function monsterPack() {
	a = Math.floor(document.lcForm.landID.value);
	c = Math.floor(document.lcForm.seaFLAG.value);
	d = Math.floor(document.lcForm.landEXP.value);
	e = Math.floor(document.lcForm.landFLAG1.value);
	f = Math.floor(document.lcForm.landFLAG2.value);
	g = Math.floor(document.lcForm.landKIND.value);
	h = Math.floor(document.lcForm.landHP.value);

	if(d > 250) d = 250;
	if(h > 15) h = 15;

	j = a * Math.pow(2, 24) + c * Math.pow(2, 20) + d * Math.pow(2, 12)
		 + e * Math.pow(2, 11) + f * Math.pow(2, 10) + g * Math.pow(2, 5) + h;

	document.lcForm.LCHANGEVALUE.value = j;
	document.lcForm.LCHANGEKIND.options.value = $HlandMonster;
	return true;
}

function navypack() {
	a = Math.floor(document.lcForm.navyID.value);
	b = Math.floor(document.lcForm.status.value);
	c = Math.floor(document.lcForm.seaFLAG2.value);
	d = Math.floor(document.lcForm.navyEXP.value);
	e = Math.floor(document.lcForm.navyFLAG1.value);
	f = Math.floor(document.lcForm.navyFLAG2.value);
	g = Math.floor(document.lcForm.navyNO.value);
	h = Math.floor(document.lcForm.navyKIND.value);
	i = Math.floor(document.lcForm.navyHP.value);

	if(d > 250) d = 250;
	if(i > 15) i = 15;

	j = a * Math.pow(2, 25) + b * Math.pow(2, 22) + c * Math.pow(2, 21) + d * Math.pow(2, 13) + e * Math.pow(2, 12)
		 + f * Math.pow(2, 11) + g * Math.pow(2, 9) + h * Math.pow(2, 4) + i;

	document.lcForm.LCHANGEVALUE.value = j;
	document.lcForm.LCHANGEKIND.options.value = $HlandNavy;
	return true;
}

function hmonsterPack() {
	a = Math.floor(document.lcForm.hlandID.value);
	b = Math.floor(document.lcForm.hugeFLAG.value);
	c = Math.floor(document.lcForm.hseaFLAG.value);
	d = Math.floor(document.lcForm.hlandEXP.value);
	e = Math.floor(document.lcForm.hlandFLAG1.value);
	f = Math.floor(document.lcForm.hlandFLAG2.value);
	g = Math.floor(document.lcForm.hlandKIND.value);
	h = Math.floor(document.lcForm.hlandHP.value);

	if(d > 250) d = 250;
	if(h > 15) h = 15;

	j = a * Math.pow(2, 24) + b * Math.pow(2, 21) + c * Math.pow(2, 20) + d * Math.pow(2, 12)
		 + e * Math.pow(2, 11) + f * Math.pow(2, 10) + g * Math.pow(2, 5) + h;

	document.lcForm.LCHANGEVALUE.value = j;
	document.lcForm.LCHANGEKIND.options.value = $HlandHugeMonster;
	return true;
}

//-->
</SCRIPT>
END
}

# �Ϸ��ѹ���λ
sub tempLchangeOK {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}���Ϸ����ѹ����ޤ���${H_tagBig}
<HR>
END
}

# �Ϸ����ͤ���������
sub tempBadValue {
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;
	out(<<END);
${HtagBig_}�Ϸ����ͤ����������褦�Ǥ�${H_tagBig}$HtempBack2
END
}

# �Ϸ����ͤ�����å�
sub landCheck {
	my($land, $lv) = @_;
	if($land == $HlandSea) {
		return 0 if(($lv < 0) || ($lv > 1));
	} elsif($land == $HlandWaste) {
		return 0 if(($lv < 0) || ($lv > 1));
	} elsif($land == $HlandPlains) {
		return 0 if($lv != 0);
	} elsif($land == $HlandTown) {
		return 0 if(($lv < 1) || ($lv > $HvalueLandTownMax));
	} elsif($land == $HlandForest) {
		return 0 if(($lv < 1) || ($lv > 200));
	} elsif($land == $HlandFarm) {
		return 0 if(($lv < 10) || ($lv > 50));
#		return if(($lv - 10) % 2 != 0);
	} elsif($land == $HlandFactory) {
		return 0 if(($lv < 30) || ($lv > 100));
#		return if(($lv - 30) % 10 != 0);
	} elsif($land == $HlandBase) {
		return 0 if(($lv < 0) || ($lv > $HmaxExpPoint));
	} elsif($land == $HlandDefence) {
		return 0 if(($lv < 0) || (($lv > $HdurableDef) && ($lv != $HdefExplosion)));
	} elsif($land == $HlandMountain) {
		return 0 if(($lv < 0) || ($lv > 200));
#		return if($lv % 5 != 0);
	} elsif($land == $HlandMonster) {
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		return 0 if(($hp < 0) || ($hp > 31) || ($kind < 0) || ($kind > $#HmonsterName));
	} elsif($land == $HlandHugeMonster) {
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		return 0 if(($hp < 0) || ($hp > 31) || ($kind < 0) || ($kind > $#HhugeMonsterName));
	} elsif($land == $HlandSbase) {
		return 0 if(($lv < 0) || ($lv > $HmaxExpPoint));
	} elsif($land == $HlandOil) {
		return 0 if($lv != 0);
	} elsif($land == $HlandMonument) {
		return 0 if(($lv < 0) || ($lv > 2));
	} elsif($land == $HlandCore) {
		return 0 if(($lv < 0) || ($lv % 10000 > $HdurableCore) || (int($lv / 10000) > 2));
	} elsif($land == $HlandHaribote) {
		return 0 if($lv != 0);
	} elsif($land == $HlandNavy) {
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $hp) = navyUnpack($lv);
		return 0 if(($hp < 0) || ($hp > 15) || ($kind < 0) || ($kind > $#HnavyName));
	} elsif($land == $HlandComplex) {
		my($tmp, $kind, $turn, $food, $money) = landUnpack($lv);
		return 0 if(($kind < 0) || ($kind > $#HcomplexName));
	} elsif($land == $HlandBouha) {
		return 0 if($lv != 0);
	} elsif($land == $HlandSeaMine) {
		return 0 if($lv != 1);
	}

	return 1;
}

#----------------------------------------------------------------------
# �����ͤˤ�뤢������⡼��
#----------------------------------------------------------------------
sub preDeleteMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# �ü�ѥ����
		if($HpreDeleteMode) {
			my @newID = ();
			my $flag = 0;
			if($HcurrentID) {
				foreach (@HpreDeleteID) {
					my $currentNumber = $HidToNumber{$_};
					if(!(defined $currentNumber)) {
					} elsif($_ == $HcurrentID) {
						$Hislands[$currentNumber]->{'predelete'} = 0;
						$flag = 1;
						my($island) = $Hislands[$currentNumber];
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
							require('./hako-turn.cgi');
							estimate($currentNumber);
							randomBuildCore($island, 1, 0, 0, 0) if(!$island->{'core'});
						}
					} else {
						push(@newID, $_);
					}
				}
				@HpreDeleteID = @newID;
				if(!$flag){
					push(@HpreDeleteID, $HcurrentID);
					$Hislands[$HidToNumber{$HcurrentID}]->{'predelete'} = $HsetTurn;
				}
			} else {
				readIslandsFile(-1);
				require('./hako-turn.cgi') if($HcorelessDead);
				foreach (@HpreDeleteID) {
					my $currentNumber = $HidToNumber{$_};
					$Hislands[$currentNumber]->{'predelete'} = 0;
					if(defined $currentNumber) {
						my($island) = $Hislands[$currentNumber];
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
							estimate($currentNumber);
							randomBuildCore($island, 1, 0, 0, 0) if(!$island->{'core'});
						}
					}
				}
				@HpreDeleteID = ();
			}
			islandSort($HrankKind, 1);
			# �ǡ����񤭽Ф�
			if(!$HcurrentID) {
				writeIslandsFile(-1);
				tempPreDeleteEnd("��");
			} else {
				writeIslandsFile($HcurrentID);
				if($flag) {
					tempPreDeleteEnd($Hislands[$HidToNumber{$HcurrentID}]->{'name'});
				} else {
					tempPreDelete($Hislands[$HidToNumber{$HcurrentID}]->{'name'});
				}
			}
		}
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempPdeleteMain();
	} else {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
#		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
#		require('./hako-top.cgi');
#		unlock();
#		# �ƥ�ץ졼�Ƚ���
#		tempTopPage();
	}
}

# ��������⡼�ɤΥȥåץڡ���
sub tempPdeleteMain {
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>����${AfterName}������ͤ�������ˤ���</H1>

<DL>
<DT>����������ˤʤä�${AfterName}�ϡ����������(�������������ޥ�ɽ�������Ĺ���ҳ������ȼ԰�̱)����ʤ��ʤ�ޤ���</DT>
<DT>��¾��${AfterName}����ι���Ϥ��٤Ƽ����Ĥ��Ƥ��ޤ��ޤ���</DT>
<DT>��������������礬�������פ⤷���ϡֶ�������פ��줿��硢��������Σɣĥǡ����ϡ����Τ������������Ԥ��ޤǤ��Τޤ޻Ĥ�ޤ���</DT>
</DL>

<FORM name="pdForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Pdelete">
<B>�����ͤ�������ˤ���${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">���Ƥ������
$HislandList
</SELECT>
<BR>
<B>����������֤ϡ�</B><BR>
<SELECT NAME="SETTURN" onChange=RestTurnToTime()>
<OPTION VALUE='99999999'>̵����
END
	my($limit);
	$limit = $HgameLimitTurn - $HislandTurn if($HgameLimitTurn);
	$limit = 100 if(($limit < 1) || ($limit > 100));
	foreach (1..$limit) {
		out("<OPTION VALUE='$_'>$_");
	}
	out(<<END);
</SELECT>������
<ilayer name="PARENT_TURN" width="100%" height="100%">
   <layer name="TURN" width="200"></layer>
   <span id="TURN"></span>
</ilayer>
<BR>
<INPUT TYPE="submit" VALUE="���ꡦ���" NAME="PdeleteButton"><BR>
<SCRIPT language="JavaScript">
<!--
function RestTurnToTime() {
	var now = new Date();
	var turn = document.pdForm.SETTURN.value;
	var stop  = $HislandTurn + Math.floor(turn);
	if(turn == 99999999) {
		stop = ''
	} else {
		stop = '��=>��<span class="number">������' + stop +'</span>';
	}
	now.setTime((turn*$HunitTime + $HislandLastTime)*1000);
	var str = '';
	if(stop != '') {
		str = stop + '(';
		str += now.getYear() + 'ǯ' + (now.getMonth()+1) + '��' + now.getDate() + '��' + now.getHours() + '��';
		if(now.getMinutes() > 0) {
			str += now.getMinutes() + 'ʬ';
			if(now.getSeconds() > 0) {
				str += now.getSeconds() + '��';
			}
		} else if(now.getSeconds() > 0) {
			str += now.getMinutes() + 'ʬ' + now.getSeconds() + '��';
		}
		str += ')�ޤ�';
	}
	if(document.getElementById){
		document.getElementById("TURN").innerHTML = str;
	} else if(document.all){
		el = document.all("TURN");
		el.innerHTML = str;
	} else if(document.layers) {
		lay = document.layers["PARENT_TURN"].document.layers["TURN"];
		lay.document.open();
		lay.document.write(str);
		lay.document.close(); 
	}

	return true;
}
RestTurnToTime();
//-->
</SCRIPT>
</FORM>
<TABLE BORDER><TR><TH colspan='2'>�����������${AfterName}</TH></TR>
END

	if($HpreDeleteID[0] eq '') {
		out("<TR><TH colspan='2'>�����ͤ��������${AfterName}�Ϥ���ޤ���</TH></TR>");
	} else {
		my($name);
		foreach (@HpreDeleteID) {
			next if(!(defined $HidToNumber{$_}));
			$name = $Hislands[$HidToNumber{$_}]->{'name'};
			out("<TR><TH>${HtagName_}${name}${AfterName}${H_tagName}</TH>");
			if($Hislands[$HidToNumber{$_}]->{'predelete'} == 99999999) {
				out("<TD>${HtagTH_}̵����${H_tagTH}</TD>");
			} else {
				my $turn = $HislandTurn + $Hislands[$HidToNumber{$_}]->{'predelete'};
				my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($Hislands[$HidToNumber{$_}]->{'predelete'}*$HunitTime + $HislandLastTime + $Hjst);
				$mon++;
				$year += 1900;
				my $str = "$yearǯ$month��$date��$hour��";
				if($min) {
					$str .= "$minʬ";
					if($sec) {
						$str .= "$sec��";
					}
				} elsif($sec) {
					$str .= "$minʬ$sec��";
				}
				out("<TD>����$Hislands[$HidToNumber{$_}]->{'predelete'}������=>��<span class='number'>������$turn</span>($str)�ޤ�</TD>");
			}
			out("</TR>");
		}
	}
	out("</TABLE>");
}

# �����ͤ�����������
sub tempPreDelete {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}������ͤ�������ˤ��ޤ���${H_tagBig}
<HR>
END
}

# �����ͤ���������
sub tempPreDeleteEnd {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}�δ����ͤ�������������ޤ���${H_tagBig}
<HR>
END
}

#----------------------------------------------------------------------
# ������������
#----------------------------------------------------------------------
sub moveFleetAdmin {
	if (!$HmfleetMode) {
		# ����
		unlock();
		# �ƥ�ץ졼�Ƚ���
		moveFleetAdminTop();
	} else {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HdefaultPassword)) {
			# �ü�ѥ����
			readIslandsFile(-2);
			my $move = 0;
			if($HfromID == 100) {
				my($i);
				if($HcurrentID == 100) {
					foreach $i (0..$islandNumber) {
						my $fromID = $Hislands[$i]->{'id'};
						foreach (0..$islandNumber) {
							my $id = $Hislands[$_]->{'id'};
							$HtoID = $id if($HtoID);
							next if($HtoID && $HfromID == $id);
							$move += moveFleetForced($fromID, $HtoID, $id, 4, 1);
						}
					}
				} else {
					foreach (0..$islandNumber) {
						my $fromID = $Hislands[$_]->{'id'};
						next if($fromID == $HtoID || $fromID == $HcurrentID);
						$move += moveFleetForced($fromID, $HtoID, $HcurrentID, 4, 1);
					}
				}
				if($move) {
					my($fName);
					if($HcurrentID != 100) {
						my($fIsland) = $Hislands[$HidToNumber{$HcurrentID}];
						$fName = '�Ǥ��ä�';
						$fName .= (!$HcurrentID) ? '��°����' : islandName($fIsland);
					}
					if($HtoID) {
						tempMfleet("<small>�����Ÿ����$fName����������°��ص��Ԥ����ޤ�����</small>");
					} else {
						tempMfleet("<small>�����Ÿ����$fName�����������Ǥ����ޤ�����</small>");
					}
				} else {
					tempMfleet("<small>���˳�����������Ϥ���ޤ���</small>");
				}
			} elsif($HcurrentID == 100) {
				my($island)  = $Hislands[$HidToNumber{$HfromID}];
				my($name)    = islandName($island);
				foreach (0..$islandNumber) {
					my $id = $Hislands[$_]->{'id'};
					$HtoID = $id if($HtoID);
					next if($HfromID == $id);
					$move += moveFleetForced($HfromID, $HtoID, $id, 4, 1);
				}
				if($move) {
					if($HtoID) {
						tempMfleet("<small>$name��Ÿ�������������°��ص��Ԥ����ޤ�����</small>");
					} else {
						tempMfleet("<small>$name��Ÿ��������������Ǥ����ޤ�����</small>");
					}
				} else {
					tempMfleet("<small>���˳�����������Ϥ���ޤ���</small>");
				}
			} else {
				$move = moveFleetForced($HfromID, $HtoID, $HcurrentID, $HfleetNo, 0);
			}
			if($move) {
				foreach (0..$islandNumber) {
					undef $Hislands[$_]->{'fkind'};
				}
				foreach (0..$islandNumber) {
					estimateNavy($_);
				}
				writeIslandsFile(-2);
			}
			unlock();
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

sub moveFleetAdminTop {
	# �����ץ��2
	$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>���������ư����</H1>
<FORM action="$HthisFile" method="POST">
<B>�ɤ�${AfterName}�ˤ�����⡩</B>(��ư��)<BR>
<SELECT NAME="FROMID">$HislandList
<OPTION style="background: red;" VALUE=100>���Ƥ�${AfterName}
</SELECT><BR>
���֤��٤Ƥ���פ����֤ȡ���°���ֽ�°�����װʳ��ʤ�������ɸ����줿�����⤬�оݤǡ���ư�褬�����������ǡװʳ��ʤ鼫��ص��Ԥ��ޤ���<BR><BR>
<B>�ɤ�${AfterName}�δ��⡩</B>(��°)<BR>
<SELECT NAME="ISLANDID">
$HislandList
<OPTION style="background: yellow;" VALUE=0>��°����
<OPTION style="background: red;" VALUE=100>���Ƥ�${AfterName}
</SELECT>��
<B>��<SELECT NAME="FLEETNUMBER">
<OPTION VALUE=0>1
<OPTION VALUE=1>2
<OPTION VALUE=2>3
<OPTION VALUE=3>4
<OPTION style="background: red;" VALUE=4>������
</SELECT>����</B><BR>
���֤��٤Ƥ���פ����֤ȡ���ư�褬�����������ǡװʳ��ʤ������⤬����ص��Ԥ��ޤ���<BR><BR>
<B>�ɤ�${AfterName}�ذ�ư�����롩</B>(��ư��)<BR>
<SELECT NAME="TOID">$HislandList
<OPTION style="background: red;" VALUE=0>����������
</SELECT><BR><BR>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Mfleet">
<INPUT TYPE="submit" VALUE="��ư" NAME="MoveFleetButton"><BR><BR>
</FORM>
END
}

# ���⶯����ư��
sub tempMfleet {
	my($str) = @_;
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$str${H_tagBig}
END
}

# ���⶯����ư
sub moveFleetForced {
	my($fromId, $toId, $fId, $no, $logcut) = @_;
	# ��ư��ID:$fromId����ư��ID:$toId����ư������������ID:$fId������No:$no
	my($island)    = $Hislands[$HidToNumber{$fromId}];
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($name)      = islandName($island);

	my($tIsland)    = $Hislands[$HidToNumber{$toId}];
	my($tLand)      = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tName)      = islandName($tIsland);

	my($fIsland)    = $Hislands[$HidToNumber{$fId}];
	my($fName)      = (!$fId) ? '��°����' : islandName($fIsland);

	$no = 0 if(!$fId);

	# ����򸡺�
	my(@fleet);
	my($i, $x, $y, $lv);
	# ��ɸ�������
	makeRandomIslandPointArray($island);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];

		# ������õ��
		next if ($land->[$x][$y] != $HlandNavy);

		# ��ư��������
		my($nId, $nFlag, $nNo, $nKind) = (navyUnpack($landValue->[$x][$y]))[0,5,6,7];
		next if (($nId != $fId) || ($no != 4 && $nNo != $no));

		# �ĳ��ʤ�̵��
		next if ($nFlag & 1);

		# ���ʤ�̵��
		my $nSpecial = $HnavySpecial[$nKind];
		next if ($nSpecial & 0x8);

		# �����򵭲�
		push(@fleet, { x => $x, y => $y });
	}

	if (@fleet < 1) {
		# ����ʤ�
		$no++;
		tempMfleet("<small>$name�ˡ�$fName ��$no����Ϥ���ޤ���</small>") if(!$logcut);
		return 0;
	}
	if($no != 4) {
		my $ofname = $fIsland->{'fleet'}->[$no];
		$no = "$ofname����";
	} else {
		$no = "������";
	}
	# �������
	my($tx, $ty, $tLv, $sendshipStr);
	if($toId eq '0') {
		foreach (@fleet) {
			# �����ξ�������
			($x, $y) = ($_->{x}, $_->{y});

			my($nSea, $nKind) = (navyUnpack($landValue->[$x][$y]))[3,7];
			$land->[$x][$y]         = $HlandSea;
			$landValue->[$x][$y]    = $nSea;
			# ����Ф�
			$sendshipStr .= "<BR>��<B>$HnavyName[$nKind]</B>${HtagName_}($x, $y)${H_tagName}";
		}
		tempMfleet("<small>$name��Ÿ�����$fName $no����Ǥ����ޤ�����<small>$sendshipStr</small></small>") if(!$logcut);
		logHistory("${HtagName_}${name}${H_tagName}��${HtagName_}${fName}${H_tagName} <B>$no</B>��������${HtagDisaster_}����${H_tagDisaster}���ޤ�����");
		return 1;
	}

	# �����ư
	makeRandomIslandPointArray($tIsland);
	foreach $i (0..$island->{'pnum'}) {
		$tx = $tIsland->{'rpx'}[$i];
		$ty = $tIsland->{'rpy'}[$i];
		$tLv = $tLandValue->[$tx][$ty];

		# ��������õ��
		next if(($tLand->[$tx][$ty] != $HlandSea) || ($tLv && !$HnavyMoveAsase));

		# �����ξ�������
		($x, $y) = ($fleet[0]->{x}, $fleet[0]->{y});
		shift @fleet;

		# �������ư
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($landValue->[$x][$y]);
		$land->[$x][$y]         = $HlandSea;
		$landValue->[$x][$y]    = $nSea;

		$tLand->[$tx][$ty]      = $HlandNavy;
		$tLandValue->[$tx][$ty] = navyPack($nId, $nTmp, $nStat, $tLv, $nExp, $nFlag, $nNo, $nKind, $nHp);
		# ����Ф�
		$sendshipStr .= "<BR>��<B>$HnavyName[$nKind]</B>${HtagName_}($tx, $ty)${H_tagName}";

		last if (@fleet < 1);
	}
	
	tempMfleet("<small>$name��Ÿ�����$fName $no��$tName�ذ�ư���ޤ�����<small>$sendshipStr</small></small>") if(!$logcut);
	return 1;
}

# ��Ͽ��
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

#----------------------------------------------------------------------
# ���٥��
#----------------------------------------------------------------------
sub setupEvent {
	if($HsetEventMode) {
		# �ѥ���ɥ����å�
		if(checkSpecialPassword($HdefaultPassword)) {
			# �ü�ѥ����
			if($HcurrentID || (keys %HeventDel != ())) {
				readIslandsFile();
				if($HsetEventMode == 1) {
					my $island = $Hislands[$HidToNumber{$HcurrentID}];
					if($island->{'event'}[0]) {
						# password�ְ㤤
						unlock();
						tempEvent("���Ǥ����ꤵ��Ƥ��ޤ���<BR>���ꤷ�ʤ������ϡ�������Ƥ���ɬ�פ�����ޤ���");
						return;
					} elsif($Htype == 1) {# ���Х��Х�
						$Haddition = 0; # �ɲ��ɸ�����Ĥ��ʤ�
						$Hturm = 0;     # ̵���¤ˤ���
						$HcoreFlag = 0; # �������ǻ�������λ���ʤ�
					} elsif(!$Hturm) {# �����и��ͳ����Хȥ�,���������Хȥ�,�����༣�Хȥ�,�޶�Ԥ��Хȥ�
						# ���֤�̵���¤ϥ���
						unlock();
						tempEvent("���֤����ꤵ��Ƥ��ޤ���");
						return;
					}
					
					#
					# 0���٥�ȥե饰 1���ϥ����� 2���� 3������ 4�ϼ� 5���� 6������ 7����� 8������� 9�����ͥץ쥼��Ȥ�̵ͭ 10��������ƥ�
					my @event = (1, $Hstart, $Hturm, $Hmaxship, $HpermitKind, $Hrestriction, $Htype, $HprizeMoney, $HprizeFood, $HprizePresent, join('', @HprizeItem),
					# 11�ɲ��ɸ� 12����ʬ��(������) 13����ʬ��(ɤ) 14�������ʬ��(������) 15�������ʬ��(ɤ) 16��°��������ʬ��(������) 17��°��������ʬ��(��) 18��ư���Խ��� 19����ʬ��(������) 20����ʬ��(��) 21�����ѵ���(min) 22�����ѵ���(max) 23�����ե饰
								$Haddition, $HmonsterTurn, $HmonsterNumber, $HhugeMonsterTurn, $HhugeMonsterNumber, $HunkownTurn, $HunkownNumber, $HautoReturn, $HcoreTurn, $HcoreNumber, $HcoreMinHP, $HcoreMaxHP, $HcoreFlag);
					$island->{'event'} = \@event;
					if($Hstart - $HnoticeTurn <= $HislandTurn) {
						my $type  = $HeventName[$Htype];
						$island->{'comment'} = "<B>$type���š�</B>";
						if(!$Haddition) {
							$island->{'comment'} .= "(<span class=attention>��</span>�ɸ��Ǥ���Τ�<B>������$Hstart����</B>�Ǥ�)";
						} else {
							$island->{'comment'} .= "(<span class=attention>��</span><B>������$Hstart����</B>����ɸ���ǽ�Ǥ�)";
						}
					}
					writeIslandsFile();
				} else {
					foreach (keys %HeventDel) {
						undef $Hislands[$HidToNumber{$_}]->{'event'};
						undef $Hislands[$HidToNumber{$_}]->{'comment'};
					}
				}
				writeIslandsFile();
			}
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# �ƥ�ץ졼�Ƚ���
	setupEventTop();
}

# ���٥�ȥ�
sub tempEvent {
	my($str) = @_;
	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$str${H_tagBig}
END
}

sub setupEventTop {
#	$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 2);
	$HislandList = getIslandList(0, 1);
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	# ����
	unlock();
	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>���٥�Ȥ����ꤹ��</H1>
<TABLE BORDER><TR><TD class='M' WIDTH=40%>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Esetup">
<TABLE BORDER><TR>
<TH>�ɤ�${AfterName}�ǡ�</TH>
<TD><SELECT NAME="ISLANDID">$HislandList</SELECT>
</TR><TR>
<TH>�����פϡ�</TH>
<TD><SELECT NAME='TYPE'>
END
	foreach (1..$#HeventName) {
		out("<OPTION VALUE=$_>$HeventName[$_]\n");
	}
	out(<<END);
</SELECT></TD>
</TR><TR>
<TH>���Ĥ��顩</TH>
<TD><SELECT NAME="START">
END
	my $nextturn = $HislandTurn + 1;
	my $minturn = $HislandTurn + $HnoticeTurn;
	my $maxturn = $minturn + 50;
	foreach ($nextturn..$maxturn) {
		if($_ > $minturn) {
			out("<OPTION VALUE=$_>$_");
		} elsif($_ < $minturn) {
			out("<OPTION style='background: red;' VALUE=$_>$_");
		} else {
			out("<OPTION VALUE=$_ SELECTED>$_");
		}
	}
	out(<<END);
</SELECT>�����󳫻�</TD>
</TR><TR>
<TH>���֤ϡ�</TH>
<TD><SELECT NAME="TURM">
<OPTION VALUE=0>̵����
END
	foreach (1..100) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>������</TD><BR>
</TR><TR>
<TH>�ɸ���ǽ�������ϡ�</TH>
<TD><SELECT NAME='MAXSHIP'>
END
	my $max = (!$HnavyMaximum) ?  int($HislandSizeX*$HislandSizeY/4) : $HnavyMaximum;
	$max = $HfleetMaximum if($HfleetMaximum);
	out("<OPTION VALUE=0>̵����");
	foreach (1..$max) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>��</TD>
</TR><TR>
<TH>�ɸ���ǽ�ϼ�ϡ�</TH>
<TD class='N'><span class='check'><input type=checkbox name=KIND value="0" CHECKED>${HtagDisaster_}��¤��(�и��ͣ�)�Τ�${H_tagDisaster}</span><BR>
END
	foreach (1..$#HnavyName) {
		next if($HnavySpecial[$_] & 0x8);
		out("<span class='check'><input type=checkbox name=KIND value=\"$_\" CHECKED>$HnavyName[$_]</span> ");
	}
	out(<<END);
</TD>
</TR><TR>
<TH>�ɲ��ɸ��ϡ�<BR></TH>
<TD class='N'>
<input type=radio name=ADDITION value="0" checked>���Ĥ��ʤ���
<input type=radio name=ADDITION value="1">���Ĥ���
</TD>
</TR><TR>
<TH>��٥�����<BR><small>(��Υ�٥�)</small></TH>
<TD class='N'><input type=hidden name=RESTRICTION value="0">
END
	foreach (1..$HmaxComNavyLevel) {
		out("<span class='check'><input type=checkbox name=RESTRICTION value=\"$_\" CHECKED>Lv.$_</span> ");
	}
	out("�ʤ�") if(!$HmaxComNavyLevel);
	out(<<END);
</TD>
</TR><TR>
<TH>���ⵢ�Խ���<BR><small>(���٥�Ƚ�λ��)</small></TH>
<TD class='N'>
<input type=radio name=AUTORETURN value="1" checked>���Ԥ��롡
<input type=radio name=AUTORETURN value="0">���Ԥ��ʤ�
</TD>
</TR><TR>
<TH>���ýи�����</TH>
<TD class='N'><SELECT NAME='MONSTERTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>������ˤĤ�<SELECT NAME='MONSTERNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ɤ<BR>
</TD>
</TR><TR>
<TH>������ýи�����</TH>
<TD class='N'><SELECT NAME='HUGEMONSTERTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>������ˤĤ�<SELECT NAME='HUGEMONSTERNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ɤ<BR>
</TD>
</TR><TR>
<TH>��°���������и�����</TH>
<TD class='N'><SELECT NAME='UNKNOWNTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>������ˤĤ�<SELECT NAME='UNKNOWNNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>��<BR>
</TD>
</TR><TR>
<TH>$HlandName[$HlandCore][0]�и�����</TH>
<TD class='N'><SELECT NAME='CORETURN'>
END
	foreach (1..100) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>������ˤĤ�<SELECT NAME='CORENUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>��<BR>
�ѵ��ϡ�min<SELECT NAME='COREMINHP'>
END
	my $num = min($HdurableCore, 99);
	foreach (0..$num) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>��max<SELECT NAME='COREMAXHP'>
END
	foreach (0..$num) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT><BR>
<span class='check'><input type=checkbox name=COREFLAG value='1'></span>���ǻ��˥��٥��${HtagDisaster_}������λ${H_tagDisaster}<BR>
������<small>(���Х��Х�����)</small>
</TD>
</TR><TR>
<TH>����ϡ�</TH>
<TD class='N'><B>���</B><input type=text style='text-align=right' name=MONEY size=12 value=0>$HunitMoney<BR>
<B>����</B><input type=text style='text-align=right' name=FOOD size=12 value=0>$HunitFood
<HR><input type=checkbox name=PRESENT value="1"><B>�����ͥץ쥼���</B><BR>
����(�Ǽ����������ӹ��Τ��Ƥ�������)
END

	if($HuseItem) {
		out("<HR>");
		foreach (1..$#HitemName) {
			out("<span class='check'><input type=checkbox name=ITEM value=\"$_\"><img src=\"$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>\n");
		}
	}

	out(<<END);
</TD>
</TR><TR><TH colspan=2>
<INPUT TYPE="submit" VALUE="���ꤹ��" NAME="SetEventButton"><BR>
</TH></TR></TABLE>
</FORM></TD>
<TD class='M' valign='top' WIDTH=60%>
<H3>�����٥�ȤˤĤ��Ƣ�</H3>
��������ϡ��Хȥ�ե�����ɤǤ������������뤿�������Ǥ���<BR><BR>
�����ϥ�����ϡ���������Υ������ͱͽ������˰ʹߤ������ǽ�Ǥ���<BR>
���ʳ��ϥ������ͱͽ������ˤˤʤ�ȥȥåץڡ����Υ�������˥��٥��ȯ������Τ���
¾�礫���ɸ�����Ƥ���������٤Ƥ򵢴Ԥ����ޤ���<BR><BR>
���ɸ��Ǥ��������������μ��������Ǥ��ޤ���<BR>
���и��ͤˤ��ϥ�Ǥ�ʤ�������ˡֿ�¤�ϡʷи��ͣ��δ����ˡפ������ɸ���ǽ�ˤ��뤳�Ȥ�Ǥ��ޤ���<BR><BR>
<TABLE BORDER WIDTH=100%>
<TR><TH>���Х��Х�</TH><TD class='N'>�ɸ������礬����ˤʤ�ޤǴ����ɤ����ΤĤ֤������Ǥ���<BR>���֤�̵���¤ˤʤꡤ���ϥ�����Τ��ɸ�������դ��ޤ���</TD></TR>
<TR><TH>�����и��ͳ����Хȥ�</TH><TD class='N'>�ɸ�������������˳��������и��ͤǽ�̤���ޤ���<BR>���֤����ꤷ�ʤ���н�̤ϤĤ��ޤ���</TD></TR>
<TR><TH>���������Хȥ�</TH><TD class='N'>�ɸ�������������˷��������������ǽ�̤���ޤ���<BR>���֤����ꤷ�ʤ���н�̤ϤĤ��ޤ���</TD></TR>
<TR><TH>�����༣�Хȥ�</TH><TD class='N'>�ɸ���������������༣�������á�������äο��ǽ�̤���ޤ���<BR>���֤����ꤷ�ʤ���н�̤ϤĤ��ޤ���</TD></TR>
<TR><TH>�޶�Ԥ��Хȥ�</TH><TD class='N'>�ɸ�������������˳��������޶����ۤǽ�̤���ޤ���<BR>���֤����ꤷ�ʤ���н�̤ϤĤ��ޤ���</TD></TR>
</TABLE>
</TD></TR></TABLE>
<HR>
<H1>���٥���������</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Esetup">
<TABLE BORDER><TR>
<TD><INPUT TYPE="submit" VALUE="���" NAME="DelEventButton"></TD>
<TH>${AfterName}̾</TH>
<TH>������</TH>
<TH>����<BR>������</TH>
<TH>����</TH>
<TH>������</TH>
<TH>�ϼ�</TH>
<TH>�ɲ�<BR>�ɸ�</TH>
<TH>����</TH>
<TH>����</TH>
<TH>����<BR>����</TH>
<TH>��°<BR>������</TH>
<TH>$HlandName[$HlandCore][0]</TH>
<TH>���</TH>
</TR>
END
	my $flag = 0;
	foreach (0..$islandNumber){
		my $island = $Hislands[$_];
		next if(!$island->{'event'}[0]);
		$flag = 1;
		my $id = $island->{'id'};
		my $name = islandName($island);
		my $turn = $island->{'event'}[1];
		my $turm = $island->{'event'}[2];
		$turm = '̵����' if(!$turm);
		$turm .= "<BR><BR><small>${HtagDisaster_}������λͭ${H_tagDisaster}</small>"if($island->{'event'}[23]);
		my $max  = $island->{'event'}[3];
		$max = ($max) ? "$max��" : '̵����';
		my $kind  = $island->{'event'}[4];
		my $ship = '';
		foreach (1..$#HnavyName) {
			$ship .= " $HnavyName[$_]" if($kind & (2 ** $_));
		}
		if($ship eq '') {
			$ship = "${HtagDisaster_}�ʤ�${H_tagDisaster}";
		} elsif($kind & 1) {
			$ship = "${HtagDisaster_}$ship${H_tagDisaster}";
		}
		my $restriction = $island->{'event'}[5];
		my $addition = ('��', '��')[$island->{'event'}[11]];
		my $limit = '';
		if(!$HmaxComNavyLevel) {
			$limit = '���¤ʤ�';
		} else {
			$limit = '<TABLE border=1 cellpadding=1 cellspacing=0><TR>';
			foreach (1..$HmaxComNavyLevel) {
				$limit .= "<TD>Lv.$_</TD>";
			}
			$limit .= '</TR><TR>';
			foreach (1..$HmaxComNavyLevel) {
				if($restriction & (2 ** $_)) {
					$limit .= "<TD align='center'>��</TD>";
				} else {
					$limit .= "<TD align='center'>��</TD>";
				}
			}
			$limit .= '</TR></TABLE>';
		}
		my $type  = $HeventName[$island->{'event'}[6]];
		my $money  = $island->{'event'}[7];
		my $food  = $island->{'event'}[8];
		my $present  = $island->{'event'}[9];
		my @item  = split(' *', $island->{'event'}[10]);
		my $prize = '';
		$prize = "$money$HunitMoney" if($money);
		if($food) {
			$prize .= " + " if($money);
			$prize .= "$food$HunitFood";
		}
		if($present) {
			$prize .= " + " if($money || $food);
			$prize .= "�����ͥץ쥼���";
		}
		if($island->{'event'}[10]) {
			$prize .= " + " if($money || $food || $present);
			foreach (1..$#HitemName) {
				$prize .= "<span class='check'><img src=\"$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>\n" if($item[$_]);
			}
		}
		$prize = '�ʤ�' if($prize eq '');
		my $mons = ($island->{'event'}[13]) ? "${HtagNumber_}$island->{'event'}[12]${H_tagNumber}<small>������<BR>�ˤĤ�</small><BR>��<B>$island->{'event'}[13]</B><small>ɤ�и�</small>" : '�и����ʤ�';
		my $huemons = ($island->{'event'}[15]) ? "${HtagNumber_}$island->{'event'}[14]${H_tagNumber}<small>������<BR>�ˤĤ�</small><BR>��<B>$island->{'event'}[15]</B><small>ɤ�и�</small>" : '�и����ʤ�';
		my $unknown = ($island->{'event'}[17]) ? "${HtagNumber_}$island->{'event'}[16]${H_tagNumber}<small>������<BR>�ˤĤ�</small><BR>��<B>$island->{'event'}[17]</B><small>�Ͻи�</small>" : '�и����ʤ�';
		my $core = () ? "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>������<BR>�ˤĤ�</small><BR>��<B>$island->{'event'}[20]</B><small>��и�</small>" : '�и����ʤ�';
		if($island->{'event'}[20]) {
			$core = "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>������<BR>�ˤĤ�</small><BR>��<B>$island->{'event'}[20]</B><small>��и�<BR><B>HP</B>:min<B>$island->{'event'}[21]</B>,max<B>$island->{'event'}[22]</B></small>";
		} else {
			$core = '�и����ʤ�';
		}
		out(<<END);
<TR>
<TD align='center'><input type=checkbox name=DEL value="$id"></TD>
<TD align='right'>$name</TD>
<TD align='right'>$type</TD>
<TD align='right'>$turn</TD>
<TD align='right'>$turm</TD>
<TD align='right'>$max</TD>
<TD class='N' align='right'>$ship</TD>
<TD align='center'>$addition</TD>
<TD align='right'>$limit</TD>
<TD align='right'>$mons</TD>
<TD align='right'>$huemons</TD>
<TD align='right'>$unknown</TD>
<TD align='right'>$core</TD>
<TD class='N' align='right'>$prize</TD>
</TR>
END
	}
	out("<TR><TH colspan=14>�ǡ���������ޤ���</TH></TR>") if(!$flag);
	out("</TABLE><INPUT TYPE=\"hidden\" VALUE=\"dummy\" NAME=\"EventDelete\"></FORM>");
}

#----------------------------------------------------------------------
# ��¸�ǡ�������
#----------------------------------------------------------------------
sub loseIslandAdminTop {
	my($str) = @_;

	$str = "${HtagBig_}$str${H_tagBig}<HR>" if(defined $str);

	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
$str
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>�ԼԤ������<small>(${HfightdirName}�ե����)</small></H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Reload">
<BR><BR>
���ԼԤ�${AfterName}̾�򥯥�å������������ξ����򸫤뤳�Ȥ��Ǥ��ޤ���<BR>
��$AfterName̾�κ��Υܥ��������å����ơ������פ򥯥�å�����ȡ��������������뤳�Ȥ��Ǥ��ޤ���<BR>
�����פ��Ƥ��ʤ�$AfterName�ξ�硤ID��$AfterName�������ʡ�̾���ѥ���ɤ����٤ư��פ��Ƥ���С��ǡ����������ؤ��ޤ���<BR>
������ʳ��ξ�硤������$AfterName�Ȥ���ID����꿶���ޤ���<BR>
��������Ѱդ˼¹Ԥ���ȡ�Ʊ��̾����$AfterName��ʣ���ˤʤ꺮��θ��ˤʤ�ޤ�)<BR>
�������ȡ��ʥ��ȤǤλ��Ѥ�ư���ݾڤǤ��ޤ��󡣿ر�����Х��Х�Ǥλ��Ѥ��򤱤������褤�Ǥ��礦��<BR>
<TABLE><TR>
<TH><INPUT TYPE=\"submit\" VALUE=\"����\" NAME=\"ReloadButton\"></TH>
<TH><INPUT TYPE=\"submit\" VALUE=\"���\" NAME=\"DeleteButton\"></TH>
<TH $HbgTitleCell>DL</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�����ʡ�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�η��쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������и���${H_tagTH}</TH>
</TR>
END

	opendir(DIN, "${HfightdirName}/");
	# �Хå����åץǡ���
	my($dn, @suf);
	while($dn = readdir(DIN)) {
		if($dn =~ /^([0-9]+)_lose.${HsubData}/) {
			push(@suf, $1);
		}
	}
	foreach (sort { $a <=> $b } @suf) {
		open(LIN, "${HfightdirName}/${_}_lose.${HsubData}");
		chomp(my @line = <LIN>);
		close(LIN);
		splice(@line, 20);

		my($name, $owner, $id, $money, $food, $pop, $area, $farm, $factory, $mountain, $gain);
		$name     = shift @line; # *���̾��*
		$owner    = shift @line; # *�����ʡ���̾��*
		shift @line;             # ���ϥ�����
		$id       = shift @line; # *ID�ֹ�*
		shift @line;             # ����
		shift @line;             # Ϣ³��ⷫ���, ��ȯ����(�رĤ�������), ���ޥ�ɼ¹�����
		shift @line;             # ������
		shift @line;             # �Ź沽�ѥ����
		$money    = shift @line; # *���*
		$food     = shift @line; # *����*
		$pop      = shift @line; # *�͸�*
		$area     = shift @line; # *����*
		$farm     = shift @line; # *����*
		$factory  = shift @line; # *����*
		$mountain = shift @line; # *�η���*
		shift @line;             # ͧ����
		shift @line;             # ����̾
		shift @line;             # ��Ũ��
		shift @line;             # ��ͭ��������
		$gain     = shift @line; # *������и���*
		$islandName = $name . $AfterName;
		if(defined $HidToNumber{$_}) {
			$islandName = $HtagName1_ . $islandName . $H_tagName1;
		} else {
			$islandName = $HtagName2_ . $islandName . $H_tagName2;
		}
		$pop = ($pop == 0) ? "̵��" : "$pop$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($area == 0) ? "����" : "$area$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$money = ($money == 0) ? "��⥼��" : "$money$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($food == 0) ? "���ߥ���" : "$food$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
		1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $navyComLevel = gainToLevel($gain);
		my $totalExp = $gain;
		1 while $totalExp =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
		out(<<END);
<TR>
<TD $HbgNumberCell align='center'><input type=radio name=RELOADIDLOSE value=\"${_}\"></TD>
<TD $HbgNumberCell align='center'><input type=checkbox name=DELETEIDLOSE value=\"${_}\"></TD>
<TD $HbgNumberCell align='center'><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Download=$HdefaultPassword&mode=2&id=${_}\">DL</A></TD>
<TH $HbgNameCell><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?LoseMap=${_}&ADMINMODELOSE=$HdefaultPassword\" target=\"_blank\">$islandName</A></TH>
<TD $HbgInfoCell align=right><B>$id</B></TD>
<TD $HbgInfoCell align=right>$owner</TD>
<TD $HbgInfoCell align=right>$pop</TD>
<TD $HbgInfoCell align=right>$area</TD>
<TD $HbgInfoCell align=right>$money</TD>
<TD $HbgInfoCell align=right>$food</TD>
<TD $HbgInfoCell align=right>$farm</TD>
<TD $HbgInfoCell align=right>$factory</TD>
<TD $HbgInfoCell align=right>$mountain</TD>
<TD $HbgInfoCell align=right>$totalExp</TD>
</TR>
END
	}
	closedir(DIN);

	out(<<END);
</TABLE>
<HR>
<H1>��¸�ǡ�������<small>(${HsavedirName}�ե����)</small></H1>
<BR><BR>
��${AfterName}̾�򥯥�å��������¸�ξ����򸫤뤳�Ȥ��Ǥ��ޤ���<BR>
��$AfterName̾�κ��Υܥ��������å����ơ������פ򥯥�å�����ȡ��Ϸ��ǡ������������뤳�Ȥ��Ǥ��ޤ���<BR>
��ID��$AfterName�������ʡ�̾���ѥ���ɤ����٤ư��פ��Ƥ��ʤ���С�������$AfterName�Ȥ���ID����꿶���ޤ���<BR>
���������äơ����Ǥ����פ��Ƥ�����Ǥ���¸�ǡ���������С����������������뤳�Ȥ��Ǥ��ޤ���<BR>
<TABLE><TR>
<TH><INPUT TYPE=\"submit\" VALUE=\"����\" NAME=\"ReloadButton\"></TH>
<TH><INPUT TYPE=\"submit\" VALUE=\"���\" NAME=\"DeleteButton\"></TH>
<TH $HbgTitleCell>DL</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�����ʡ�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�η��쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������и���${H_tagTH}</TH>
</TR>
END
	opendir(DIN, "${HsavedirName}/");
	# �Хå����åץǡ���
	my($dn, @suf);
	while($dn = readdir(DIN)) {
		if($dn =~ /^([0-9]+)_save.${HsubData}/) {
			push(@suf, $1);
		}
	}
	foreach (sort { $a <=> $b } @suf) {
		open(LIN, "${HsavedirName}/${_}_save.${HsubData}");
		chomp(my @line = <LIN>);
		close(LIN);

		my($name, $owner, $id, $money, $food, $pop, $area, $farm, $factory, $mountain, $gain);
		$name     = shift(@line); # *���̾��*
		$owner    = shift(@line); # *�����ʡ���̾��*
		shift(@line);             # ���ϥ�����
		$id       = shift(@line); # *ID�ֹ�*
		shift(@line);             # ����
		shift(@line);             # Ϣ³��ⷫ���, ��ȯ����(�رĤ�������), ���ޥ�ɼ¹�����
		shift(@line);             # ������
		shift(@line);             # �Ź沽�ѥ����
		$money    = shift(@line); # *���*
		$food     = shift(@line); # *����*
		$pop      = shift(@line); # *�͸�*
		$area     = shift(@line); # *����*
		$farm     = shift(@line); # *����*
		$factory  = shift(@line); # *����*
		$mountain = shift(@line); # *�η���*
		shift(@line);             # ͧ����
		shift(@line);             # ����̾
		shift(@line);             # ��Ũ��
		shift(@line);             # ��ͭ��������
		$gain     = shift(@line); # *������и���*
		$islandName = $name . $AfterName;
		if(defined $HidToNumber{$_}) {
			$islandName = $HtagName1_ . $islandName . $H_tagName1;
		} else {
			$islandName = $HtagName2_ . $islandName . $H_tagName2;
		}
		$pop = ($pop == 0) ? "̵��" : "$pop$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($area == 0) ? "����" : "$area$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$money = ($money == 0) ? "��⥼��" : "$money$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($food == 0) ? "���ߥ���" : "$food$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
		1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $navyComLevel = gainToLevel($gain);
		my $totalExp = $gain;
		1 while $totalExp =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
		out(<<END);
<TR>
<TD $HbgNumberCell align='center'><input type=radio name=RELOADIDSAVE value=\"${_}\"></TD>
<TD $HbgNumberCell align='center'><input type=checkbox name=DELETEIDSAVE value=\"${_}\"></TD>
<TD $HbgNumberCell align='center'><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Download=$HdefaultPassword&mode=1&id=${_}\">DL</A></TD>
<TH $HbgNameCell><A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?LoseMap=${_}&ADMINMODESAVE=$HdefaultPassword\" target=\"_blank\">$islandName</A></TH>
<TD $HbgInfoCell align=right><B>$id</B></TD>
<TD $HbgInfoCell align=right>$owner</TD>
<TD $HbgInfoCell align=right>$pop</TD>
<TD $HbgInfoCell align=right>$area</TD>
<TD $HbgInfoCell align=right>$money</TD>
<TD $HbgInfoCell align=right>$food</TD>
<TD $HbgInfoCell align=right>$farm</TD>
<TD $HbgInfoCell align=right>$factory</TD>
<TD $HbgInfoCell align=right>$mountain</TD>
<TD $HbgInfoCell align=right>$totalExp</TD>
</TR>
END
	}
	out("</TABLE><INPUT TYPE='hidden' VALUE='0' NAME='dummy'></FORM>");
	closedir(DIN);
#<FORM action="$HthisFile" method="POST" encType="multipart/form-data">
	out(<<END) if($HuseUpload);
<FORM action="$HuploadFile" method="POST" encType="multipart/form-data">
<HR>
<H1>�ǡ������åץ���</H1>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Upload">
�����������¸���Ƥ���ǡ����򥢥åץ��ɤ��뤳�Ȥ��Ǥ��ޤ���<BR>
���ե�����̾����[ID]_lose.${HsubData}�ʤ�${HfightdirName}�ե�����ء�[ID]_save.${HsubData}�ʤ�${HsavedirName}�ե�����إ��åפ���ޤ���<BR>
����([ID]�ΤȤ����1����100�ޤǤΤ����줫�ο���)<BR>
���ǡ������������Υ����å��ϤۤȤ�ɤ���ޤ��󤫤顤�Ѥʥե�����򥢥åפ��ʤ��褦�ˤ��Ƥ���������<BR>
<INPUT TYPE="file" NAME="FILE">
<INPUT TYPE="submit" VALUE="�ɲ�" NAME=\"UPLOADBUTTON\">
</FORM>
END

	# ����
	unlock();
}

# ��¸�ǡ������
sub dataDelete {
	my($mode) = @_;
	if(!checkSpecialPassword($HdefaultPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	} elsif(!$mode) {
		unlock();
		tempProblem();
		return;
	}
	if($mode & 1) { # save
		foreach (@HsaveID) {
			unlink("${HsavedirName}/${_}_save.${HsubData}") if(-e "${HsavedirName}/${_}_save.${HsubData}");
		}
	}
	if($mode & 2) { # lose
		foreach (@HloseID) {
			unlink("${HfightdirName}/${_}_lose.${HsubData}") if(-e "${HfightdirName}/${_}_lose.${HsubData}")
		}
	}
	# ����
	unlock();
	loseIslandAdminTop('������ޤ���');
	return;
}

# ��¸�ǡ������������
sub dataDownload {
	my($mode) = @_;
	unlock();
	if(!checkSpecialPassword($HdefaultPassword)) {
		# password�ְ㤤
		unlock();
		tempHeader();
		tempWrongPassword();
		return;
	}

	my $dir = (!($mode % 2)) ? $HfightdirName : $HsavedirName;
	my $file = (!($mode % 2)) ? "${HcurrentID}_lose.${HsubData}" : "${HcurrentID}_save.${HsubData}";
	open(IN, "${dir}/${file}");
	my @line = <IN>;
	close(IN);
    print "Content-Disposition: attachment; filename=$file\n";
    print "Content-type: application/octet-stream\n\n";
    print @line;
    exit;
}

1;
