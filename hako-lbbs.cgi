# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������Ǽ��ĥ⥸�塼��(ver1.00)
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
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub localBbsMain {
	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($speaker);

	# �إå�����
	tempHeader() if($HjavaMode ne 'java' && $HlbbsMode < 7);

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		unlock();
		tempProblem();
		return;
	}

	# ��Ģ�⡼�ɤ�̾������å��������ʤ����
	if($HlbbsMode == 0 || $HlbbsMode == 1 || $HlbbsMode == 7) {
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			tempHeader() if($HlbbsMode == 5);
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	my($lbbs);
	$lbbs = $island->{'lbbs'};

	# id�������ֹ�����
	my($number) = $HidToNumber{$HspeakerID};
	my($sIsland) = $Hislands[$number];
	# �ѥ���ɥ����å�
	if(!checkPassword($sIsland,$HinputPassword)) {
		$HspeakerID = undef;
		$number = undef;
		$sIsland = undef;
	}

	# �Ѹ��ԥ⡼�ɤ���ʤ����ϥѥ���ɥ����å�
	if($HlbbsMode % 2 == 1) {
		if(!checkPassword($island,$HinputPassword)) {
			# password�ְ㤤
			tempHeader() if($HlbbsMode == 5 || $HlbbsMode == 7);
			unlock();
			tempWrongPassword();
			return;
		}

		# �����ʡ�̾������
		# $HlbbsName = $island->{'owner'};
	} elsif ($HlbbsMode == 0) {
		# �Ѹ��ԥ⡼��

		if ($HlbbsType ne 'ANON') {
			# �����ȶ���


			# �ʤ��������礬�ʤ����
			if($number eq '') {
				unlock();
				tempProblem();
				return;
			}

			# �ѥ���ɥ����å�
			if(!checkPassword($sIsland,$HinputPassword)) {
				# password�ְ㤤
				unlock();
				tempWrongPassword();
				return;
			}

			# �����ʡ�̾������
			# $HlbbsName = $sIsland->{'owner'};

			# �̿����Ѥ�ʧ��
			my($cost) = ($HlbbsType eq 'PUBLIC') ? $HlbbsMoneyPublic : $HlbbsMoneySecret;
			if ($sIsland->{'money'} < $cost) {
				# ������­
				unlock();
				tempLbbsNoMoney();
				return;
			}
			$sIsland->{'money'} -= $cost;
		}

		# ȯ���Ԥ򵭲�����
		if ($HlbbsType ne 'ANON') {
			# �����ȶ���
			my $name = islandName($sIsland);
			$speaker = $name . ',' . $HspeakerID;
		} else {
			# ƿ̾
			$speaker = $ENV{'REMOTE_HOST'};
			$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
		}
	} elsif ($HlbbsMode == 2) {
		# �Ѹ��Ժ���⡼��

		# �ʤ��������礬�ʤ����
		if($number eq '') {
			unlock();
			tempProblem();
			return;
		}

		# ID�����å�
		$lbbs->[$HcommandPlanNumber] =~ /[0-9]*\<.*,([0-9]+)\<.*\>.*\>.*$/;
		my $wId = $1;
		if($wId != $HspeakerID) {
			# ID�ְ㤤
			unlock();
			tempWrong("���ʤ���ȯ���ǤϤ���ޤ���");
			return;
		}

		# �ѥ���ɥ����å�
		if(!checkPassword($sIsland,$HinputPassword)) {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	} elsif ($HlbbsMode == 4) {
		# �Ѹ��Զ����̿���ǧ�⡼��

		# �ʤ��������礬�ʤ����
		if($number eq '') {
			unlock();
			tempProblem();
			return;
		}

		# �ѥ���ɥ����å�
		if(!checkPassword($sIsland,$HinputPassword)) {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}

	# �⡼�ɤ�ʬ��
	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	if($HlbbsMode == 2 || $HlbbsMode == 3 || $HlbbsMode == 9) {
		# ����⡼��
		if(($HlbbsMode == 3 || $HlbbsMode == 9) && ($HcommandPlanNumber == -1)) {
			splice(@$lbbs, 0, $HlbbsView);
		} else {
			splice(@$lbbs, $HcommandPlanNumber, 1);
		}
		tempLbbsDelete() if($HlbbsMode != 9);
	} elsif($HlbbsMode == 7 || $HlbbsMode == 1 || $HlbbsMode == 0) {
		# ��Ģ�⡼��
		$speaker = "������,0" if($HlbbsMode == 7);
		if ($HlbbsType ne 'SECRET') {
			# ������ƿ̾
			$speaker = "0<$speaker";
		} else {
			# ����
			$speaker = "1<$speaker";
		}
		# ��å���������ˤ��餹
		slideLbbsMessage($lbbs);

		# ��å������񤭹���
		my($message);
		if($HlbbsMode == 1) {
			$message = '1';
		} else {
			$message = '0';
		}
		# IP�����������
		my $addr    = $ENV{'REMOTE_ADDR'};
		my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + $Hjst);
		my $day = ('��','��','��','��','��','��','��')[$wday];
		$year = $year + 1900;
		$mon = $mon + 1;
		my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
		$message .= ",$date,$addr";

		$HlbbsName = "$HislandTurn��" . htmlEscape($HlbbsName);
		$HlbbsMessage = htmlEscape($HlbbsMessage);
		$lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";

		tempLbbsAdd() if($HlbbsMode != 7);
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);

	# ��ȤΥ⡼�ɤ�
	if($HlbbsMode % 2 == 0) {
		printIslandMain();
	} elsif($HlbbsMode == 7 || $HlbbsMode == 9 || $HlbbsMode == 11) {
		tempHeader() if($jumpTug !~ /location/);
		print $jumpTug;
		unlock();
		exit;
	} else {
		ownerMain();
	}
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
#	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsView - 1] = '';
}

#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
sub tempLbbsMain {
	my($mode) = @_;

	out("<DIV ID='localBBS'>");
	tempLbbsHead();     # ������Ǽ���
	# �񤭹��ߥե�����
	out("<TABLE><TR><TD class='M'>");
	if($mode) {
		tempLbbsInputOW();
	} else {
		tempLbbsInput();
	}
	out("</TD></TR><TR><TD class='M'>");
	tempLbbsContents(); # �Ǽ�������
	out("</TD></TR></TABLE></DIV>");
}

# ������Ǽ���
sub tempLbbsHead {
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
END
}

# ������Ǽ������ϥե�����
sub tempLbbsInput {
	out(<<END);
<FORM action="$HthisFile" method="POST">
END
	if ($HlbbsMoneyPublic + $HlbbsMoneySecret > 0) {
		# ȯ����ͭ��
		out("<DIV align='center'><B>��</B>");
		out("�����̿���<B>$HlbbsMoneyPublic$HunitMoney</B>�Ǥ���") if ($HlbbsMoneyPublic > 0);
		out("�����̿���<B>$HlbbsMoneySecret$HunitMoney</B>�Ǥ���") if ($HlbbsMoneySecret > 0);
		out("</DIV>");
	}
	my $col = " colspan=2";

	# out("<B>��</B>${AfterName}����äƤ�������̾�����ѹ����Ƥ��ͭ��̾���Ȥ��ޤ���");

	out(<<END);
<TABLE BORDER width=100%>
<TR>
<TH>̾��<small>(����${HlengthLbbsName}���ޤ�)</small></TH>
<TH$col>����<small>(����${HlengthLbbsMessage}���ޤ�)</small></TH>
<TH>�̿���ˡ</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD$col><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
<TD>
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>����
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>����</span>
</TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH>${AfterName}̾</TH>
<TH$col>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=16 MAXLENGTH=16 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD>
<SELECT NAME="ISLANDID2">$HislandList</SELECT>
END
	out(<<END) if ($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">�Ѹ���
END

	out(<<END);
</TD>
<TD><DIV align='center'>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonSS$HcurrentID">
<INPUT TYPE="submit" VALUE="�����ǧ" NAME="LbbsButtonCK$HcurrentID">
</DIV></TD>
<TD align=right>
END

	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	if($HlbbsViewMax < $HlbbsMax) {
		out(<<END);
View
<SELECT NAME=LBBSVIEW>
END
		for($i = $HlbbsViewMax; $i <= $HlbbsMax; $i+=10) {
			if($i != $HlbbsView) {
				out("<OPTION VALUE=$i>$i\n");
			} else {
				out("<OPTION VALUE=$i SELECTED>$i\n");
			}
		}
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="����" NAME="LbbsButtonVS$HcurrentID">
END
	}
	if(!$HlbbsAnon) {
		out(<<END);
No.
<SELECT NAME=NUMBER>
END
		# ȯ���ֹ�
		my($j, $i);
		for($i = 0; $i < $HlbbsView; $i++) {
			$j = $i + 1;
			out("<OPTION VALUE=$i>$j\n");
		}
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="���" NAME="LbbsButtonDS$HcurrentID">
END
	}
	out(<<END);
</TD>
</TR>
</FORM>
</TABLE>
END
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {

	out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
END
	# out("<B>��</B>̾�����ѹ����Ƥ��ͭ��̾���Ȥ��ޤ���");

	out(<<END);
<TABLE BORDER width=100%>
<TR>
<TH>̾��<small>(����${HlengthLbbsName}���ޤ�)</small></TH>
<TH COLSPAN=2>����<small>(����${HlengthLbbsMessage}���ޤ�)</small></TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH COLSPAN=2>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=16 MAXLENGTH=16 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="��Ģ" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
END

	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	if($HlbbsViewMax < $HlbbsMax) {
		out(<<END);
View
<SELECT NAME=LBBSVIEW>
END
		for($i = $HlbbsViewMax; $i <= $HlbbsMax; $i+=10) {
			if($i != $HlbbsView) {
				out("<OPTION VALUE=$i>$i\n");
			} else {
				out("<OPTION VALUE=$i SELECTED>$i\n");
			}
		}
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="����" NAME="LbbsButtonVO$HcurrentID">
END
	}

	out(<<END);
No.
<SELECT NAME=NUMBER>
END
	# ȯ���ֹ�
	my($j, $i);
	for($i = 0; $i < $HlbbsView; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out("<OPTION VALUE=-1>��\n");
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="���" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</FORM>
</TABLE>
END
}

# ������Ǽ�������
sub tempLbbsContents {
	my($lbbs, $line, $no);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	$no = @$lbbs;
	out(<<END) if($lbbs->[0] ne '0<<0>>' && $lbbs->[0] ne '');
<TABLE BORDER width=100%>
<TR>
<TH>�ֹ�</TH>
<TH>��Ģ���� (�ݴɵ�����:$no)</TH>
</TR>
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
			out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
			my($speaker);
#			$speaker = "<span class='lbbsST'><B><SMALL>($2)</SMALL></B></span>" if ($HlbbsSpeaker && ($2 ne ''));
			my($sName, $sID) = split(/,/, $iName);
			my($os, $date, $addr) = split(/,/, $oda);
			my($turn, $name) = split(/��/, $tan);
			$tan = "<A title='[${date}]'>������${turn}</A>��$name";
			my $sNo = $HidToNumber{$sID};
			if($sName ne '') {
				if(defined $sNo){
					$speaker = "<span class='lbbsST'><B><SMALL>(<A STYlE=\"text-decoration:none\" HREF=\"$HthisFile?Sight=$sID\" TARGET=_blank>$sName</A>)</SMALL></B></span>";
				} else {
					$speaker = "<span class='lbbsST'><B><SMALL>($sName)</SMALL></B></span>";
				}
			}
			if($os == 0) {
				# �Ѹ���
				if ($m == 0) {
					# ����
					if($sID ne '0') {
						out("<TD>$HtagLbbsSS_$tan > ${com}$H_tagLbbsSS $speaker</TD></TR>");
					} else {
						out("<TD><span class='lbbsAD'>$tan > ${com}</span> $speaker</TD></TR>");
					}
				} else {
					# ����
					if (($HmainMode ne 'owner') &&(($HlbbsMode != 4) || ($HspeakerID eq '') || ($sID != $HspeakerID))) {
						# �Ѹ���
						out("<TD><DIV align='center'><span class='lbbsST'>- ���� -</span></DIV></TD></TR>");
					} else {
						# �����ʡ�
						out("<TD><span class='lbbsST'>$tan >(��) ${com}</span> $speaker</TD></TR>");
					}
				}
			} else {
				# ���
				out("<TD>$HtagLbbsOW_$tan > ${com}$H_tagLbbsOW $speaker</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE>
END
}

# ������Ǽ��Ĥ�̾������å��������ʤ����
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ�����${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ�����${H_tagBig}<HR>
END
}

# �̿����­�ꤺ
sub tempLbbsNoMoney {
	out(<<END);
${HtagBig_}�����­�Τ��ᵭĢ�Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

1;
