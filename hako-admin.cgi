#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# 管理モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 管理人による宣戦布告メンテナンス
#----------------------------------------------------------------------
sub dewarSetupMain() {
	if ($HwsetupMode) {
		# パスワードチェック
		if(checkSpecialPassword($HdefaultPassword)) {
			# 特殊パスワード
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
			# 変更成功
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# テンプレート出力
	tempDeWarSetupPage();
}

# 宣戦布告メンテナンスページ
sub tempDeWarSetupPage() {
	# 開放
	unlock();
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='campInfo'>
<H1>宣戦布告 設定</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="WSetup">
<TABLE BORDER><TR>
<TH $HbgTitleCell colspan=5>${HtagTH_}宣戦布告設定${H_tagTH}　<INPUT TYPE="submit" VALUE="変更" NAME="WarChangeButton"></TH>
</TR><TR>
<TD align="center">${HtagTH_}削除${H_tagTH}</TD>
<TD align="center">${HtagTH_}開始ターン${H_tagTH}</TD>
<TD align="center">${HtagTH_}宣戦布告した${AfterName}${H_tagTH}</TD>
<TD align="center">${HtagTH_}宣戦布告された${AfterName}${H_tagTH}</TD>
<TD align="center">${HtagTH_}状態${H_tagTH}</TD></TR>
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
<OPTION VALUE="0"$s[0]>交戦中
<OPTION VALUE="$t1"$s[1]>停戦交渉中(布告側)
<OPTION VALUE="$t2"$s[2]>停戦交渉中(被布告側)
</select></TD></TR>
END
	}
	my $turnList = "<OPTION VALUE=\"0\" style=\"background:red;\" selected>追加しない";
	for($j=$HislandTurn+1;$j<$HislandTurn+100;$j++) {
		$turnList .= "<OPTION VALUE=\"$j\">$j";
	}
	my $islandList = getIslandList(0, 1);
	$t1 = $HislandTurn * 10 + 1;
	$t2 = $t1 + 1;
	out(<<END);
<TR>
<TH>新規</TH>
<TH><select name=war>$turnList</select></TH>
<TD align="center"><select name=war>$islandList</select></TD>
<TD align="center"><select name=war>$islandList</select></TD>
<TD align="center"><select name=war>
<OPTION VALUE="0">交戦中
<OPTION VALUE="$t1">停戦交渉中(布告側)
<OPTION VALUE="$t2">停戦交渉中(被布告側)
</select></TD></TR>
</TABLE><INPUT TYPE="hidden" VALUE="dummy" NAME="WarChange"></FORM></DIV>
END
}

#----------------------------------------------------------------------
# 管理人による友好国・同盟(陣営)設定
#----------------------------------------------------------------------
sub amitySetupMain() {
	if ($HasetupMode) {
		# パスワードチェック
		if(checkSpecialPassword($HdefaultPassword)) {
			# 特殊パスワード
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
			# 変更成功
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# テンプレート出力
	tempAmitySetupPage();
}

# 友好国設定ページ
sub tempAmitySetupPage() {
	# 開放
	unlock();
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='campInfo'>
<H1>友好国・同盟(陣営)設定</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="ASetup">
<TABLE BORDER><TR>
<TH $HbgTitleCell rowspan=2>${HtagTH_}友好国設定${H_tagTH}<BR><INPUT TYPE="submit" VALUE="変更" NAME="AmityChangeButton"></TH>
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
			$Hislands[$b]->{'field'} <=> $Hislands[$a]->{'field'} || # バトルフィールド優先
			$Hislands[$b]->{'ally'} <=> $Hislands[$a]->{'ally'} || # 同盟でソート
			$a <=> $b # $kindが同じなら以前のまま
		   } @idx;

	my $aStr = ($HarmisticeTurn) ? '陣営' : '同盟';
	out("<TH $HbgTitleCell colspan=$HislandNumber>${HtagTH_}${AfterName}名${H_tagTH}</TH>\n");
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
				out("<TD align=\"center\">＝</TD>");
			} elsif($warFlag{"$id,$aId"}) {
				out("<TD align='center'>${HtagDisaster_}Ｘ${H_tagDisaster}</TD>\n");
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
# 管理人によるプレゼントモード
#----------------------------------------------------------------------
sub presentMain {
	if (!$HpresentMode) {
		# 開放
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();

		# テンプレート出力
		tempPresentPage();
	} else {
		# パスワードチェック
		if(checkSpecialPassword($HoldPassword)) {
			# 特殊パスワード

			if (!$HpresentMoney && !$HpresentFood) {
				# 金も食料もない
				tempPresentEmpty();
				unlock();
				return;
			}

			# idから島を取得
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($name)   = $island->{'name'};

			$island->{'money'} += $HpresentMoney;
			$island->{'money'} = 0 if ($island->{'money'} < 0);
			$island->{'food'}  += $HpresentFood;
			$island->{'food'} = 0 if ($island->{'food'} < 0);

			logPresent($HcurrentID, $name, $HpresentLog);

			# データ書き出し
			writeIslandsFile($HcurrentID);
			unlock();

			# 変更成功
			tempPresentOK($name);
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# プレゼントモードのトップページ
sub tempPresentPage {
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>参加${AfterName}にプレゼントを贈る</H1>

<FORM action="$HthisFile" method="POST">
<B>プレゼントを受け取る${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
<BR>
<B>プレゼントの内容は？(マイナス値も可能)</B><BR>
<INPUT TYPE="text" NAME="PRESENTMONEY" VALUE="0" SIZE=16 MAXLENGTH=16>$HunitMoney<BR>
<INPUT TYPE="text" NAME="PRESENTFOOD"  VALUE="0" SIZE=16 MAXLENGTH=16>$HunitFood<BR>
<BR>
<B>ログメッセージは？(省略可能。先頭に${AfterName}名が挿入されます)<small>(全角${HlengthPresentLog}字まで)</small></B><BR>
○○${AfterName}<INPUT TYPE="text" NAME="PRESENTLOG"  VALUE="" SIZE=128 MAXLENGTH=256><BR>
<BR>
<B>マスターパスワードは？</B><BR>
<INPUT TYPE="password" NAME="OLDPASS" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f><BR>
<INPUT TYPE="submit" VALUE="プレゼントを贈る" NAME="PresentButton"><BR>
</FORM>
END
}

# プレゼント完了
sub tempPresentOK {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}にプレゼントを贈りました${H_tagBig}$HtempBack
END
}

# プレゼント内容がおかしい
sub tempPresentEmpty {
	out(<<END);
${HtagBig_}プレゼントの内容がおかしいようです${H_tagBig}$HtempBack
END
}

# プレゼント
sub logPresent {
	my($id, $name, $log) = @_;
	logHistory("${HtagName_}${name}島${H_tagName}$log") if ($log ne '');
}

#----------------------------------------------------------------------
# 管理人による制裁モード
#----------------------------------------------------------------------
sub punishMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# 特殊パスワード
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
		# テンプレート出力
		tempPunishPage();

	} else {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
#		# パスワードが一致しなければトップページへ
#		require('./hako-top.cgi');
#		unlock();
#		# テンプレート出力
#		tempTopPage();
	}
}

# 制裁モードのトップページ
sub tempPunishPage {
	my(@punishName) =
		(
		 'なし', # 0
		 '地震', # 1
		 '津波', # 2
		 '怪獣（人口条件クリア時のみ）', # 3
		 '巨大怪獣（人口条件クリア時のみ）', # 4
		 '所属不明艦艇（人口条件クリア時のみ）', # 5
		 '地盤沈下（面積条件クリア時のみ）', # 6
		 '台風', # 7
		 '巨大隕石（座標指定）', # 8
		 '隕石', # 9
		 '噴火（座標指定）', # 10
		 );

	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>参加${AfterName}に制裁を加える</H1>

<DL>
<DT>・「ルールに違反した」と思う前に、「そのルールは誰もが読める場所に書いてあるか？」を確認しましょう。</DT>
<DT>・制裁を加えるのはたやすいことですが、本当に管理人としての立場で行っているか考えましょう。</DT>
<DT>・制裁を加えなければならないほど被害が大きいか考えましょう。軽い気持ちで攻撃する人はいつでもいるものです。</DT>
<DT>・<span class=attention>制裁の存在は極秘にしましょう。</span>制裁が明らかになると他のプレイヤーとの信頼関係も崩れます。</DT>
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Punish">
<B>制裁を加える${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="マップを開く" onclick="printIsland();">
<BR><BR>
<B>座標は？（座標指定できる制裁でのみ有効）</B><BR>
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
<B>制裁の内容は？</B><BR>
<SELECT NAME="PUNISHID">
END

	for($i = 0; $i < $#punishName + 1; $i++) {
		out("<OPTION VALUE=\"$i\">$punishName[$i]\n");
	}

	out(<<END);
</SELECT><BR>
<BR>
<INPUT TYPE="submit" VALUE="制裁を加える" NAME="PunishButton"><BR>
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
		out("<TABLE BORDER><TR><TH>${AfterName}名</TH><TH>制裁内容</TH><TH>座標</TH></TR>");
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
# 管理人による地形変更モード
#----------------------------------------------------------------------
sub lchangeMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# 特殊パスワード
		if ($HlchangeMode) {
			# idから島を取得
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($land) = $island->{'land'};
			my($landValue) = $island->{'landValue'};

			# 地形の値の整合性をチェック(チェックしたくない場合はコメントアウトして下さい)
			if(!landCheck($HlchangeKIND, $HlchangeVALUE)) {
				tempBadValue();
				unlock();
				return;
			}

			$land->[$HcommandX][$HcommandY] = $HlchangeKIND;
			$landValue->[$HcommandX][$HcommandY] = $HlchangeVALUE;

			# データ書き出し
			writeIslandsFile($HcurrentID);
			unlock();

			# 変更成功
			tempLchangeOK($island->{'name'});
		}
		$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
		unlock();
		# テンプレート出力
		tempLchangePage();
	} else {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
#		# パスワードが一致しなければトップページへ
#		require('./hako-top.cgi');
#		unlock();
#		# テンプレート出力
#		tempTopPage();
	}
}

# 地形変更モードのトップページ
sub tempLchangePage {

	my($expOption, $hpOption) = ('', '');
	my($i);

	foreach $i (0..250) {
		$expOption .= "<OPTION VALUE=$i>$i\n";
	}
	foreach $i (0..31) {
		$hpOption .= "<OPTION VALUE=$i>$i\n";
	}

	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>参加${AfterName}の地形データを変更する</H1>

<DL>
<DT>・「地形の値」についての知識がなければ、使用は難しいかもしれません。</DT>
<DT>・特に「怪獣」「海軍」「複合地形」については、知識があっても難しいと思います。</DT>
<DT>・「地形」に対して<B>「地形の値」が適切であるかどうか簡易判定をしています</B>ので、注意してください。</DT>
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Lchange">
<B>地形を変更する${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="マップを開く" onclick="printIsland();">
<BR><BR>
<B>座標は？</B><BR>
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
<B>地形は？</B><BR>
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
<B>地形の値は？</B><BR>
<INPUT TYPE="text" SIZE=15 NAME="LCHANGEVALUE" VALUE="0"><BR>
<BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="LchangeButton"><BR>
<BR>
<BR>
<B>サポートツール</B>
<table>
<tr>
<td rowspan=2>複合<BR>地形</td>
<td>種類</td>
<td>ターンフラグ</td>
<td>食料フラグ</td>
<td>資金フラグ</td>
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
<td rowspan=2>怪獣</td>
<td>島ID</td>
<td>浅瀬フラグ</td>
<td>経験値</td>
<td>フラグ</td>
<td>種類</td>
<td>耐久力</td>
</tr>
<tr>
<td><SELECT name=landID onChange=monsterPack() onClick=monsterPack()>$HislandList<OPTION VALUE=0>所属島なし</SELECT></td>
<td><SELECT name=seaFLAG onChange=monsterPack() onClick=monsterPack()><OPTION value=0>海<OPTION value=1>浅瀬</SELECT></td>
<td><SELECT name=landEXP onChange=monsterPack() onClick=monsterPack()>$expOption</SELECT></td>
<td><SELECT name=landFLAG1 onChange=monsterPack() onClick=monsterPack()><OPTION value=0>陸上<OPTION value=1>潜水(海上)</SELECT>
<SELECT name=landFLAG2 onChange=monsterPack() onClick=monsterPack()><OPTION value=0>硬化せず<OPTION value=1>硬化中</SELECT></td>
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
<td rowspan=2>海軍</td>
<td>島ID</td>
<td>状態</td>
<td>浅瀬フラグ</td>
<td>経験値</td>
<td>フラグ</td>
<td>艦隊番号</td>
<td>種類</td>
<td>耐久力</td>
</tr>
<tr>
<td><SELECT name=navyID onChange=navypack() onClick=navypack()>$HislandList<OPTION VALUE=0>所属島なし</SELECT></td>
<td><SELECT name=status onChange=navypack() onClick=navypack()><OPTION value=0>通常<OPTION value=1>退治<OPTION value=2>巡航<OPTION value=3>停船</SELECT></td>
<td><SELECT name=seaFLAG2 onChange=navypack() onClick=navypack()><OPTION value=0>海<OPTION value=1>浅瀬</SELECT></td>
<td><SELECT name=navyEXP onChange=navypack() onClick=navypack()>
END

	foreach $i (0..$HmaxExpNavy) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT></td>
<td><SELECT name=navyFLAG1 onChange=navypack() onClick=navypack()><OPTION value=0>海上<OPTION value=1>潜水</SELECT>
<SELECT name=navyFLAG2 onChange=navypack() onClick=navypack()><OPTION value=0>生存<OPTION value=1>残骸</SELECT></td>
<td><SELECT name=navyNO>
END

	foreach $i (0..3) {
		my $j = $i + 1;
		out("<OPTION VALUE=$i>第$j艦隊\n");
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
<td rowspan=2>巨大<br>怪獣</td>
<td>島ID</td>
<td>巨大怪獣フラグ</td>
<td>浅瀬フラグ</td>
<td>経験値</td>
<td>フラグ</td>
<td>種類</td>
<td>耐久力</td>
</tr>
<tr>
<td><SELECT name=hlandID onChange=hmonsterPack() onClick=hmonsterPack()>$HislandList<OPTION VALUE=0>所属島なし</SELECT></td>
<td><SELECT name=hugeFLAG onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>コア<OPTION value=1>右上<OPTION value=2>右<OPTION value=3>右下<OPTION value=4>左下<OPTION value=5>左<OPTION value=6>左上</SELECT></td>
<td><SELECT name=hseaFLAG onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>海<OPTION value=1>浅瀬</SELECT></td>
<td><SELECT name=hlandEXP onChange=hmonsterPack() onClick=hmonsterPack()>$expOption</SELECT></td>
<td><SELECT name=hlandFLAG1 onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>陸上<OPTION value=1>潜水(海上)</SELECT>
<SELECT name=hlandFLAG2 onChange=hmonsterPack() onClick=hmonsterPack()><OPTION value=0>硬化せず<OPTION value=1>硬化中</SELECT></td>
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
<B>参考(地形の値)</B>
<ul type="disc">
<li>$HlandName[$HlandSea][0] ======> 0:$HlandName[$HlandSea][0]，1:$HlandName[$HlandSea][1]
<li>$HlandName[$HlandWaste][0] ====> 0:$HlandName[$HlandWaste][0]，1:$HlandName[$HlandWaste][1]
<li>$HlandName[$HlandMountain][0] ======> 0:$HlandName[$HlandMountain][0]，1:$HlandName[$HlandMountain][1]
<li>$HlandName[$HlandDefence][0] ==> 数値+1が耐久力
<li>$HlandName[$HlandCore][0] ==> 数値の下2ケタ+1が耐久力，数値の10000の位が設置地形(00000:平地($HlandName[$HlandCore][0])，10000:浅瀬($HlandName[$HlandCore][1])，20000:海($HlandName[$HlandCore][2]))
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

# 地形変更完了
sub tempLchangeOK {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}の地形を変更しました${H_tagBig}
<HR>
END
}

# 地形の値がおかしい
sub tempBadValue {
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;
	out(<<END);
${HtagBig_}地形の値がおかしいようです${H_tagBig}$HtempBack2
END
}

# 地形の値をチェック
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
# 管理人によるあずかりモード
#----------------------------------------------------------------------
sub preDeleteMain {
	if(checkSpecialPassword($HdefaultPassword)) {
		# 特殊パスワード
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
							estimate($currentNumber);
							randomBuildCore($island, 1, 0, 0, 0) if(!$island->{'core'});
						}
					}
				}
				@HpreDeleteID = ();
			}
			islandSort($HrankKind, 1);
			# データ書き出し
			if(!$HcurrentID) {
				writeIslandsFile(-1);
				tempPreDeleteEnd("全");
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
		# テンプレート出力
		tempPdeleteMain();
	} else {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
#		# パスワードが一致しなければトップページへ
#		require('./hako-top.cgi');
#		unlock();
#		# テンプレート出力
#		tempTopPage();
	}
}

# あずかりモードのトップページ
sub tempPdeleteMain {
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>参加${AfterName}を管理人あずかりにする</H1>

<DL>
<DT>・あずかりになった${AfterName}は、ターン処理(収入処理・コマンド処理・成長・災害・失業者移民)されなくなります。</DT>
<DT>・他の${AfterName}からの攻撃はすべて受けつけてしまいます。</DT>
<DT>・あずかり中の島が「放棄」もしくは「強制削除」された場合、あずかりのＩＤデータは、次のあずかり処理を行うまでそのまま残ります。</DT>
</DL>

<FORM name="pdForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Pdelete">
<B>管理人あずかりにする${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">全ての島を解除
$HislandList
</SELECT>
<BR>
<B>あずかる期間は？</B><BR>
<SELECT NAME="SETTURN" onChange=RestTurnToTime()>
<OPTION VALUE='99999999'>無期限
END
	my($limit);
	$limit = $HgameLimitTurn - $HislandTurn if($HgameLimitTurn);
	$limit = 100 if(($limit < 1) || ($limit > 100));
	foreach (1..$limit) {
		out("<OPTION VALUE='$_'>$_");
	}
	out(<<END);
</SELECT>ターン
<ilayer name="PARENT_TURN" width="100%" height="100%">
   <layer name="TURN" width="200"></layer>
   <span id="TURN"></span>
</ilayer>
<BR>
<INPUT TYPE="submit" VALUE="設定・解除" NAME="PdeleteButton"><BR>
<SCRIPT language="JavaScript">
<!--
function RestTurnToTime() {
	var now = new Date();
	var turn = document.pdForm.SETTURN.value;
	var stop  = $HislandTurn + Math.floor(turn);
	if(turn == 99999999) {
		stop = ''
	} else {
		stop = '　=>　<span class="number">ターン' + stop +'</span>';
	}
	now.setTime((turn*$HunitTime + $HislandLastTime)*1000);
	var str = '';
	if(stop != '') {
		str = stop + '(';
		str += now.getYear() + '年' + (now.getMonth()+1) + '月' + now.getDate() + '日' + now.getHours() + '時';
		if(now.getMinutes() > 0) {
			str += now.getMinutes() + '分';
			if(now.getSeconds() > 0) {
				str += now.getSeconds() + '秒';
			}
		} else if(now.getSeconds() > 0) {
			str += now.getMinutes() + '分' + now.getSeconds() + '秒';
		}
		str += ')まで';
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
<TABLE BORDER><TR><TH colspan='2'>あずかり中の${AfterName}</TH></TR>
END

	if($HpreDeleteID[0] eq '') {
		out("<TR><TH colspan='2'>管理人あずかりの${AfterName}はありません！</TH></TR>");
	} else {
		my($name);
		foreach (@HpreDeleteID) {
			next if(!(defined $HidToNumber{$_}));
			$name = $Hislands[$HidToNumber{$_}]->{'name'};
			out("<TR><TH>${HtagName_}${name}${AfterName}${H_tagName}</TH>");
			if($Hislands[$HidToNumber{$_}]->{'predelete'} == 99999999) {
				out("<TD>${HtagTH_}無期限${H_tagTH}</TD>");
			} else {
				my $turn = $HislandTurn + $Hislands[$HidToNumber{$_}]->{'predelete'};
				my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($Hislands[$HidToNumber{$_}]->{'predelete'}*$HunitTime + $HislandLastTime + $Hjst);
				$mon++;
				$year += 1900;
				my $str = "$year年$month月$date日$hour時";
				if($min) {
					$str .= "$min分";
					if($sec) {
						$str .= "$sec秒";
					}
				} elsif($sec) {
					$str .= "$min分$sec秒";
				}
				out("<TD>あと$Hislands[$HidToNumber{$_}]->{'predelete'}ターン　=>　<span class='number'>ターン$turn</span>($str)まで</TD>");
			}
			out("</TR>");
		}
	}
	out("</TABLE>");
}

# 管理人あずかり設定
sub tempPreDelete {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}を管理人あずかりにしました${H_tagBig}
<HR>
END
}

# 管理人あずかり解除
sub tempPreDeleteEnd {
	my($name) = @_;
	out(<<END);
${HtagBig_}$name${AfterName}の管理人あずかりを解除しました${H_tagBig}
<HR>
END
}

#----------------------------------------------------------------------
# 艦艇強制帰還
#----------------------------------------------------------------------
sub moveFleetAdmin {
	if (!$HmfleetMode) {
		# 開放
		unlock();
		# テンプレート出力
		moveFleetAdminTop();
	} else {
		# パスワードチェック
		if(checkSpecialPassword($HdefaultPassword)) {
			# 特殊パスワード
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
						$fName = 'であった';
						$fName .= (!$HcurrentID) ? '所属不明' : islandName($fIsland);
					}
					if($HtoID) {
						tempMfleet("<small>全島に展開中$fNameの全艦隊を所属島へ帰還させました。</small>");
					} else {
						tempMfleet("<small>全島に展開中$fNameの全艦隊を消滅させました。</small>");
					}
				} else {
					tempMfleet("<small>条件に該当する艦艇はありません。</small>");
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
						tempMfleet("<small>$nameに展開中の全艦隊を所属島へ帰還させました。</small>");
					} else {
						tempMfleet("<small>$nameに展開中の全艦隊を消滅させました。</small>");
					}
				} else {
					tempMfleet("<small>条件に該当する艦艇はありません。</small>");
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
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

sub moveFleetAdminTop {
	# 「戻る」リンク2
	$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 1);
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>艦隊を強制移動する</H1>
<FORM action="$HthisFile" method="POST">
<B>どの${AfterName}にいる艦隊？</B>(移動元)<BR>
<SELECT NAME="FROMID">$HislandList
<OPTION style="background: red;" VALUE=100>全ての${AfterName}
</SELECT><BR>
※「すべての島」を選ぶと、所属が「所属不明」以外なら全島に派遣された全艦隊が対象で、移動先が「全艦艇消滅」以外なら自島へ帰還します。<BR><BR>
<B>どの${AfterName}の艦隊？</B>(所属)<BR>
<SELECT NAME="ISLANDID">
$HislandList
<OPTION style="background: yellow;" VALUE=0>所属不明
<OPTION style="background: red;" VALUE=100>全ての${AfterName}
</SELECT>　
<B>第<SELECT NAME="FLEETNUMBER">
<OPTION VALUE=0>1
<OPTION VALUE=1>2
<OPTION VALUE=2>3
<OPTION VALUE=3>4
<OPTION style="background: red;" VALUE=4>全艦隊
</SELECT>艦隊</B><BR>
※「すべての島」を選ぶと、移動先が「全艦艇消滅」以外なら全艦隊が自島へ帰還します。<BR><BR>
<B>どの${AfterName}へ移動させる？</B>(移動先)<BR>
<SELECT NAME="TOID">$HislandList
<OPTION style="background: red;" VALUE=0>全艦艇消滅
</SELECT><BR><BR>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Mfleet">
<INPUT TYPE="submit" VALUE="移動" NAME="MoveFleetButton"><BR><BR>
</FORM>
END
}

# 艦隊強制移動ログ
sub tempMfleet {
	my($str) = @_;
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$str${H_tagBig}
END
}

# 艦隊強制移動
sub moveFleetForced {
	my($fromId, $toId, $fId, $no, $logcut) = @_;
	# 移動元ID:$fromId、移動先ID:$toId、移動させる艦隊の島ID:$fId、艦隊No:$no
	my($island)    = $Hislands[$HidToNumber{$fromId}];
	my($land)      = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($name)      = islandName($island);

	my($tIsland)    = $Hislands[$HidToNumber{$toId}];
	my($tLand)      = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tName)      = islandName($tIsland);

	my($fIsland)    = $Hislands[$HidToNumber{$fId}];
	my($fName)      = (!$fId) ? '所属不明' : islandName($fIsland);

	$no = 0 if(!$fId);

	# 艦隊を検索
	my(@fleet);
	my($i, $x, $y, $lv);
	# 座標配列を作る
	makeRandomIslandPointArray($island);
	foreach $i (0..$island->{'pnum'}) {
		$x = $island->{'rpx'}[$i];
		$y = $island->{'rpy'}[$i];

		# 海軍を探す
		next if ($land->[$x][$y] != $HlandNavy);

		# 移動艦艇か？
		my($nId, $nFlag, $nNo, $nKind) = (navyUnpack($landValue->[$x][$y]))[0,5,6,7];
		next if (($nId != $fId) || ($no != 4 && $nNo != $no));

		# 残骸なら無視
		next if ($nFlag & 1);

		# 港なら無視
		my $nSpecial = $HnavySpecial[$nKind];
		next if ($nSpecial & 0x8);

		# 艦艇を記憶
		push(@fleet, { x => $x, y => $y });
	}

	if (@fleet < 1) {
		# 艦隊なし
		$no++;
		tempMfleet("<small>$nameに、$fName 第$no艦隊はありません！</small>") if(!$logcut);
		return 0;
	}
	if($no != 4) {
		my $ofname = $fIsland->{'fleet'}->[$no];
		$no = "$ofname艦隊";
	} else {
		$no = "全艦隊";
	}
	# 艦隊消滅
	my($tx, $ty, $tLv, $sendshipStr);
	if($toId eq '0') {
		foreach (@fleet) {
			# 艦艇の情報を取得
			($x, $y) = ($_->{x}, $_->{y});

			my($nSea, $nKind) = (navyUnpack($landValue->[$x][$y]))[3,7];
			$land->[$x][$y]         = $HlandSea;
			$landValue->[$x][$y]    = $nSea;
			# ログを出す
			$sendshipStr .= "<BR>　<B>$HnavyName[$nKind]</B>${HtagName_}($x, $y)${H_tagName}";
		}
		tempMfleet("<small>$nameに展開中の$fName $noを消滅させました。<small>$sendshipStr</small></small>") if(!$logcut);
		logHistory("${HtagName_}${name}${H_tagName}の${HtagName_}${fName}${H_tagName} <B>$no</B>が、突然${HtagDisaster_}消滅${H_tagDisaster}しました。");
		return 1;
	}

	# 艦隊移動
	makeRandomIslandPointArray($tIsland);
	foreach $i (0..$island->{'pnum'}) {
		$tx = $tIsland->{'rpx'}[$i];
		$ty = $tIsland->{'rpy'}[$i];
		$tLv = $tLandValue->[$tx][$ty];

		# 深い海を探す
		next if(($tLand->[$tx][$ty] != $HlandSea) || ($tLv && !$HnavyMoveAsase));

		# 艦艇の情報を取得
		($x, $y) = ($fleet[0]->{x}, $fleet[0]->{y});
		shift @fleet;

		# 艦艇を移動
		my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($landValue->[$x][$y]);
		$land->[$x][$y]         = $HlandSea;
		$landValue->[$x][$y]    = $nSea;

		$tLand->[$tx][$ty]      = $HlandNavy;
		$tLandValue->[$tx][$ty] = navyPack($nId, $nTmp, $nStat, $tLv, $nExp, $nFlag, $nNo, $nKind, $nHp);
		# ログを出す
		$sendshipStr .= "<BR>　<B>$HnavyName[$nKind]</B>${HtagName_}($tx, $ty)${H_tagName}";

		last if (@fleet < 1);
	}
	
	tempMfleet("<small>$nameに展開中の$fName $noを$tNameへ移動しました。<small>$sendshipStr</small></small>") if(!$logcut);
	return 1;
}

# 記録ログ
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

#----------------------------------------------------------------------
# イベント
#----------------------------------------------------------------------
sub setupEvent {
	if($HsetEventMode) {
		# パスワードチェック
		if(checkSpecialPassword($HdefaultPassword)) {
			# 特殊パスワード
			if($HcurrentID || (keys %HeventDel != ())) {
				readIslandsFile();
				if($HsetEventMode == 1) {
					my $island = $Hislands[$HidToNumber{$HcurrentID}];
					if($island->{'event'}[0]) {
						# password間違い
						unlock();
						tempEvent("すでに設定されています。<BR>設定しなおす場合は、削除しておく必要があります。");
						return;
					} elsif($Htype == 1) {# サバイバル
						$Haddition = 0; # 追加派遣を許可しない
						$Hturm = 0;     # 無期限にする
						$HcoreFlag = 0; # コア壊滅時強制終了しない
					} elsif(!$Hturm) {# 艦艇経験値獲得バトル,艦艇撃沈バトル,怪獣退治バトル,賞金稼ぎバトル
						# 期間が無期限はダメ
						unlock();
						tempEvent("期間が設定されていません。");
						return;
					}
					
					#
					# 0イベントフラグ 1開始ターン 2期間 3艦艇数 4艦種 5制限 6タイプ 7報償金 8報償食料 9管理人プレゼントの有無 10報償アイテム
					my @event = (1, $Hstart, $Hturm, $Hmaxship, $HpermitKind, $Hrestriction, $Htype, $HprizeMoney, $HprizeFood, $HprizePresent, join('', @HprizeItem),
					# 11追加派遣 12怪獣分母(ターン) 13怪獣分子(匹) 14巨大怪獣分母(ターン) 15巨大怪獣分子(匹) 16所属不明艦艇分母(ターン) 17所属不明艦艇分子(艦) 18自動帰還処理 19コア分母(ターン) 20コア分子(艦) 21コア耐久力(min) 22コア耐久力(max) 23コアフラグ
								$Haddition, $HmonsterTurn, $HmonsterNumber, $HhugeMonsterTurn, $HhugeMonsterNumber, $HunkownTurn, $HunkownNumber, $HautoReturn, $HcoreTurn, $HcoreNumber, $HcoreMinHP, $HcoreMaxHP, $HcoreFlag);
					$island->{'event'} = \@event;
					if($Hstart - $HnoticeTurn <= $HislandTurn) {
						my $type  = $HeventName[$Htype];
						$island->{'comment'} = "<B>$type開催！</B>";
						if(!$Haddition) {
							$island->{'comment'} .= "(<span class=attention>注！</span>派遣できるのは<B>ターン$Hstartだけ</B>です)";
						} else {
							$island->{'comment'} .= "(<span class=attention>注！</span><B>ターン$Hstartから</B>随時派遣可能です)";
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
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
	# テンプレート出力
	setupEventTop();
}

# イベントログ
sub tempEvent {
	my($str) = @_;
	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$str${H_tagBig}
END
}

sub setupEventTop {
#	$HislandList = getIslandList($Hislands[$HbfieldNumber]->{'id'}, 2);
	$HislandList = getIslandList(0, 1);
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	# 開放
	unlock();
	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>イベントを設定する</H1>
<TABLE BORDER><TR><TD class='M' WIDTH=40%>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Esetup">
<TABLE BORDER><TR>
<TH>どの${AfterName}で？</TH>
<TD><SELECT NAME="ISLANDID">$HislandList</SELECT>
</TR><TR>
<TH>タイプは？</TH>
<TD><SELECT NAME='TYPE'>
END
	foreach (1..$#HeventName) {
		out("<OPTION VALUE=$_>$HeventName[$_]\n");
	}
	out(<<END);
</SELECT></TD>
</TR><TR>
<TH>いつから？</TH>
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
</SELECT>ターン開始</TD>
</TR><TR>
<TH>期間は？</TH>
<TD><SELECT NAME="TURM">
<OPTION VALUE=0>無期限
END
	foreach (1..100) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ターン</TD><BR>
</TR><TR>
<TH>派遣可能艦艇数は？</TH>
<TD><SELECT NAME='MAXSHIP'>
END
	my $max = (!$HnavyMaximum) ?  int($HislandSizeX*$HislandSizeY/4) : $HnavyMaximum;
	$max = $HfleetMaximum if($HfleetMaximum);
	out("<OPTION VALUE=0>無制限");
	foreach (1..$max) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>艦</TD>
</TR><TR>
<TH>派遣可能艦種は？</TH>
<TD class='N'><span class='check'><input type=checkbox name=KIND value="0" CHECKED>${HtagDisaster_}新造艦(経験値０)のみ${H_tagDisaster}</span><BR>
END
	foreach (1..$#HnavyName) {
		next if($HnavySpecial[$_] & 0x8);
		out("<span class='check'><input type=checkbox name=KIND value=\"$_\" CHECKED>$HnavyName[$_]</span> ");
	}
	out(<<END);
</TD>
</TR><TR>
<TH>追加派遣は？<BR></TH>
<TD class='N'>
<input type=radio name=ADDITION value="0" checked>許可しない　
<input type=radio name=ADDITION value="1">許可する
</TD>
</TR><TR>
<TH>レベル制限<BR><small>(島のレベル)</small></TH>
<TD class='N'><input type=hidden name=RESTRICTION value="0">
END
	foreach (1..$HmaxComNavyLevel) {
		out("<span class='check'><input type=checkbox name=RESTRICTION value=\"$_\" CHECKED>Lv.$_</span> ");
	}
	out("なし") if(!$HmaxComNavyLevel);
	out(<<END);
</TD>
</TR><TR>
<TH>艦隊帰還処理<BR><small>(イベント終了時)</small></TH>
<TD class='N'>
<input type=radio name=AUTORETURN value="1" checked>帰還する　
<input type=radio name=AUTORETURN value="0">帰還しない
</TD>
</TR><TR>
<TH>怪獣出現頻度</TH>
<TD class='N'><SELECT NAME='MONSTERTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ターンにつき<SELECT NAME='MONSTERNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>匹<BR>
</TD>
</TR><TR>
<TH>巨大怪獣出現頻度</TH>
<TD class='N'><SELECT NAME='HUGEMONSTERTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ターンにつき<SELECT NAME='HUGEMONSTERNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>匹<BR>
</TD>
</TR><TR>
<TH>所属不明艦艇出現頻度</TH>
<TD class='N'><SELECT NAME='UNKNOWNTURN'>
END
	foreach (1..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ターンにつき<SELECT NAME='UNKNOWNNUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>艦<BR>
</TD>
</TR><TR>
<TH>$HlandName[$HlandCore][0]出現頻度</TH>
<TD class='N'><SELECT NAME='CORETURN'>
END
	foreach (1..100) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>ターンにつき<SELECT NAME='CORENUMBER'>
END
	foreach (0..10) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>基<BR>
耐久力：min<SELECT NAME='COREMINHP'>
END
	my $num = min($HdurableCore, 99);
	foreach (0..$num) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT>　max<SELECT NAME='COREMAXHP'>
END
	foreach (0..$num) {
		out("<OPTION VALUE=$_>$_");
	}
	out(<<END);
</SELECT><BR>
<span class='check'><input type=checkbox name=COREFLAG value='1'></span>壊滅時にイベント${HtagDisaster_}強制終了${H_tagDisaster}<BR>
　　　<small>(サバイバルを除く)</small>
</TD>
</TR><TR>
<TH>報償は？</TH>
<TD class='N'><B>資金</B><input type=text style='text-align=right' name=MONEY size=12 value=0>$HunitMoney<BR>
<B>食料</B><input type=text style='text-align=right' name=FOOD size=12 value=0>$HunitFood
<HR><input type=checkbox name=PRESENT value="1"><B>管理人プレゼント</B><BR>
　　(掲示板等で別途告知してください)
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
<INPUT TYPE="submit" VALUE="設定する" NAME="SetEventButton"><BR>
</TH></TR></TABLE>
</FORM></TD>
<TD class='M' valign='top' WIDTH=60%>
<H3>■イベントについて■</H3>
この設定は、バトルフィールドでの対戦を管理するための設定です。<BR><BR>
・開始ターンは、（設定時のターン＋猶予ターン）以降で設定可能です。<BR>
　（開始ターン−猶予ターン）になるとトップページのコメント欄にイベント発生を告知し、
他島から派遣されている艦艇すべてを帰還させます。<BR><BR>
・派遣できる艦艇数や艦艇の種類を設定できます。<BR>
　経験値によるハンデをなくすために「新造艦（経験値０の艦艇）」だけを派遣可能にすることもできます。<BR><BR>
<TABLE BORDER WIDTH=100%>
<TR><TH>サバイバル</TH><TD class='N'>派遣した島が１島になるまで艦艇どうしのつぶしあいです。<BR>期間は無期限になり，開始ターンのみ派遣を受け付けます。</TD></TR>
<TR><TH>艦艇経験値獲得バトル</TH><TD class='N'>派遣艦艇が期間中に獲得した経験値で順位を決めます。<BR>期間を設定しなければ順位はつきません。</TD></TR>
<TR><TH>艦艇撃沈バトル</TH><TD class='N'>派遣艦艇が期間中に撃沈した艦艇数で順位を決めます。<BR>期間を設定しなければ順位はつきません。</TD></TR>
<TR><TH>怪獣退治バトル</TH><TD class='N'>派遣艦艇が期間中に退治した怪獣・巨大怪獣の数で順位を決めます。<BR>期間を設定しなければ順位はつきません。</TD></TR>
<TR><TH>賞金稼ぎバトル</TH><TD class='N'>派遣艦艇が期間中に獲得した賞金の総額で順位を決めます。<BR>期間を設定しなければ順位はつきません。</TD></TR>
</TABLE>
</TD></TR></TABLE>
<HR>
<H1>イベント設定一覧</H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Esetup">
<TABLE BORDER><TR>
<TD><INPUT TYPE="submit" VALUE="削除" NAME="DelEventButton"></TD>
<TH>${AfterName}名</TH>
<TH>タイプ</TH>
<TH>開始<BR>ターン</TH>
<TH>期間</TH>
<TH>艦艇数</TH>
<TH>艦種</TH>
<TH>追加<BR>派遣</TH>
<TH>制限</TH>
<TH>怪獣</TH>
<TH>巨大<BR>怪獣</TH>
<TH>所属<BR>不明艦</TH>
<TH>$HlandName[$HlandCore][0]</TH>
<TH>報償</TH>
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
		$turm = '無期限' if(!$turm);
		$turm .= "<BR><BR><small>${HtagDisaster_}強制終了有${H_tagDisaster}</small>"if($island->{'event'}[23]);
		my $max  = $island->{'event'}[3];
		$max = ($max) ? "$max艦" : '無制限';
		my $kind  = $island->{'event'}[4];
		my $ship = '';
		foreach (1..$#HnavyName) {
			$ship .= " $HnavyName[$_]" if($kind & (2 ** $_));
		}
		if($ship eq '') {
			$ship = "${HtagDisaster_}なし${H_tagDisaster}";
		} elsif($kind & 1) {
			$ship = "${HtagDisaster_}$ship${H_tagDisaster}";
		}
		my $restriction = $island->{'event'}[5];
		my $addition = ('×', '○')[$island->{'event'}[11]];
		my $limit = '';
		if(!$HmaxComNavyLevel) {
			$limit = '制限なし';
		} else {
			$limit = '<TABLE border=1 cellpadding=1 cellspacing=0><TR>';
			foreach (1..$HmaxComNavyLevel) {
				$limit .= "<TD>Lv.$_</TD>";
			}
			$limit .= '</TR><TR>';
			foreach (1..$HmaxComNavyLevel) {
				if($restriction & (2 ** $_)) {
					$limit .= "<TD align='center'>○</TD>";
				} else {
					$limit .= "<TD align='center'>×</TD>";
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
			$prize .= "管理人プレゼント";
		}
		if($island->{'event'}[10]) {
			$prize .= " + " if($money || $food || $present);
			foreach (1..$#HitemName) {
				$prize .= "<span class='check'><img src=\"$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>\n" if($item[$_]);
			}
		}
		$prize = 'なし' if($prize eq '');
		my $mons = ($island->{'event'}[13]) ? "${HtagNumber_}$island->{'event'}[12]${H_tagNumber}<small>ターン<BR>につき</small><BR>　<B>$island->{'event'}[13]</B><small>匹出現</small>" : '出現しない';
		my $huemons = ($island->{'event'}[15]) ? "${HtagNumber_}$island->{'event'}[14]${H_tagNumber}<small>ターン<BR>につき</small><BR>　<B>$island->{'event'}[15]</B><small>匹出現</small>" : '出現しない';
		my $unknown = ($island->{'event'}[17]) ? "${HtagNumber_}$island->{'event'}[16]${H_tagNumber}<small>ターン<BR>につき</small><BR>　<B>$island->{'event'}[17]</B><small>艦出現</small>" : '出現しない';
		my $core = () ? "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>ターン<BR>につき</small><BR>　<B>$island->{'event'}[20]</B><small>基出現</small>" : '出現しない';
		if($island->{'event'}[20]) {
			$core = "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>ターン<BR>につき</small><BR>　<B>$island->{'event'}[20]</B><small>基出現<BR><B>HP</B>:min<B>$island->{'event'}[21]</B>,max<B>$island->{'event'}[22]</B></small>";
		} else {
			$core = '出現しない';
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
	out("<TR><TH colspan=14>データがありません！</TH></TR>") if(!$flag);
	out("</TABLE><INPUT TYPE=\"hidden\" VALUE=\"dummy\" NAME=\"EventDelete\"></FORM>");
}

#----------------------------------------------------------------------
# 保存データ一覧
#----------------------------------------------------------------------
sub loseIslandAdminTop {
	my($str) = @_;

	$str = "${HtagBig_}$str${H_tagBig}<HR>" if(defined $str);

	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;

	out(<<END);
$str
<DIV align='center'>$HtempBack2</DIV><BR>
<H1>敗者の島一覧<small>(${HfightdirName}フォルダ)</small></H1>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Reload">
<BR><BR>
＊敗者の${AfterName}名をクリックすると敗戦時の状況を見ることができます。<BR>
＊$AfterName名の左のボタンをチェックして「復元」をクリックすると，戦線に復帰することができます。<BR>
・沈没していない$AfterNameの場合，ID，$AfterName，オーナー名，パスワードがすべて一致していれば，データが入り替わります。<BR>
・それ以外の場合，新しい$AfterNameとしてIDが割り振られます。<BR>
【注】不用意に実行すると，同じ名前の$AfterNameが複数になり混乱の元になります)<BR>
　　　トーナメントでの使用は動作保証できません。陣営戦，サバイバルでの使用も避けた方がよいでしょう。<BR>
<TABLE><TR>
<TH><INPUT TYPE=\"submit\" VALUE=\"復元\" NAME=\"ReloadButton\"></TH>
<TH><INPUT TYPE=\"submit\" VALUE=\"削除\" NAME=\"DeleteButton\"></TH>
<TH $HbgTitleCell>DL</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}オーナー${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}農場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>
</TR>
END

	opendir(DIN, "${HfightdirName}/");
	# バックアップデータ
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
		$name     = shift @line; # *島の名前*
		$owner    = shift @line; # *オーナーの名前*
		shift @line;             # 開始ターン
		$id       = shift @line; # *ID番号*
		shift @line;             # 受賞
		shift @line;             # 連続資金繰り数, 開発委託(陣営あずかり), コマンド実行設定
		shift @line;             # コメント
		shift @line;             # 暗号化パスワード
		$money    = shift @line; # *資金*
		$food     = shift @line; # *食料*
		$pop      = shift @line; # *人口*
		$area     = shift @line; # *広さ*
		$farm     = shift @line; # *農場*
		$factory  = shift @line; # *工場*
		$mountain = shift @line; # *採掘場*
		shift @line;             # 友好国
		shift @line;             # 艦隊名
		shift @line;             # 索敵順
		shift @line;             # 保有艦艇種類
		$gain     = shift @line; # *総獲得経験値*
		$islandName = $name . $AfterName;
		if(defined $HidToNumber{$_}) {
			$islandName = $HtagName1_ . $islandName . $H_tagName1;
		} else {
			$islandName = $HtagName2_ . $islandName . $H_tagName2;
		}
		$pop = ($pop == 0) ? "無人" : "$pop$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($area == 0) ? "海域" : "$area$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$money = ($money == 0) ? "資金ゼロ" : "$money$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($food == 0) ? "備蓄ゼロ" : "$food$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
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
<H1>保存データ一覧<small>(${HsavedirName}フォルダ)</small></H1>
<BR><BR>
＊${AfterName}名をクリックすると保存の状況を見ることができます。<BR>
＊$AfterName名の左のボタンをチェックして「復元」をクリックすると，地形データを復元することができます。<BR>
・ID，$AfterName，オーナー名，パスワードがすべて一致していなければ，新しい$AfterNameとしてIDが割り振られます。<BR>
・したがって，すでに沈没している島でも保存データがあれば，戦線に復帰させることができます。<BR>
<TABLE><TR>
<TH><INPUT TYPE=\"submit\" VALUE=\"復元\" NAME=\"ReloadButton\"></TH>
<TH><INPUT TYPE=\"submit\" VALUE=\"削除\" NAME=\"DeleteButton\"></TH>
<TH $HbgTitleCell>DL</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}オーナー${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}農場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>
</TR>
END
	opendir(DIN, "${HsavedirName}/");
	# バックアップデータ
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
		$name     = shift(@line); # *島の名前*
		$owner    = shift(@line); # *オーナーの名前*
		shift(@line);             # 開始ターン
		$id       = shift(@line); # *ID番号*
		shift(@line);             # 受賞
		shift(@line);             # 連続資金繰り数, 開発委託(陣営あずかり), コマンド実行設定
		shift(@line);             # コメント
		shift(@line);             # 暗号化パスワード
		$money    = shift(@line); # *資金*
		$food     = shift(@line); # *食料*
		$pop      = shift(@line); # *人口*
		$area     = shift(@line); # *広さ*
		$farm     = shift(@line); # *農場*
		$factory  = shift(@line); # *工場*
		$mountain = shift(@line); # *採掘場*
		shift(@line);             # 友好国
		shift(@line);             # 艦隊名
		shift(@line);             # 索敵順
		shift(@line);             # 保有艦艇種類
		$gain     = shift(@line); # *総獲得経験値*
		$islandName = $name . $AfterName;
		if(defined $HidToNumber{$_}) {
			$islandName = $HtagName1_ . $islandName . $H_tagName1;
		} else {
			$islandName = $HtagName2_ . $islandName . $H_tagName2;
		}
		$pop = ($pop == 0) ? "無人" : "$pop$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($area == 0) ? "海域" : "$area$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$money = ($money == 0) ? "資金ゼロ" : "$money$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($food == 0) ? "備蓄ゼロ" : "$food$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
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
<H1>データアップロード</H1>
<INPUT TYPE="hidden" VALUE="$HdefaultPassword" NAME="Upload">
＊ローカルに保存してあるデータをアップロードすることができます。<BR>
・ファイル名が，[ID]_lose.${HsubData}なら${HfightdirName}フォルダへ，[ID]_save.${HsubData}なら${HsavedirName}フォルダへアップされます。<BR>
　　([ID]のところは1から100までのいずれかの数字)<BR>
・データの整合性のチェックはほとんどありませんから，変なファイルをアップしないようにしてください。<BR>
<INPUT TYPE="file" NAME="FILE">
<INPUT TYPE="submit" VALUE="追加" NAME=\"UPLOADBUTTON\">
</FORM>
END

	# 開放
	unlock();
}

# 保存データ削除
sub dataDelete {
	my($mode) = @_;
	if(!checkSpecialPassword($HdefaultPassword)) {
		# password間違い
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
	# 開放
	unlock();
	loseIslandAdminTop('削除しました');
	return;
}

# 保存データダウンロード
sub dataDownload {
	my($mode) = @_;
	unlock();
	if(!checkSpecialPassword($HdefaultPassword)) {
		# password間違い
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
