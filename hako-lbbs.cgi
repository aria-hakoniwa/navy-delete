# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ローカル掲示板モジュール(ver1.00)
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
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン

sub localBbsMain {
	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($speaker);

	# ヘッダ出力
	tempHeader() if($HjavaMode ne 'java' && $HlbbsMode < 7);

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		unlock();
		tempProblem();
		return;
	}

	# 記帳モードで名前かメッセージがない場合
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

	# idから島番号を取得
	my($number) = $HidToNumber{$HspeakerID};
	my($sIsland) = $Hislands[$number];
	# パスワードチェック
	if(!checkPassword($sIsland,$HinputPassword)) {
		$HspeakerID = undef;
		$number = undef;
		$sIsland = undef;
	}

	# 観光者モードじゃない時はパスワードチェック
	if($HlbbsMode % 2 == 1) {
		if(!checkPassword($island,$HinputPassword)) {
			# password間違い
			tempHeader() if($HlbbsMode == 5 || $HlbbsMode == 7);
			unlock();
			tempWrongPassword();
			return;
		}

		# オーナー名を設定
		# $HlbbsName = $island->{'owner'};
	} elsif ($HlbbsMode == 0) {
		# 観光者モード

		if ($HlbbsType ne 'ANON') {
			# 公開と極秘


			# なぜかその島がない場合
			if($number eq '') {
				unlock();
				tempProblem();
				return;
			}

			# パスワードチェック
			if(!checkPassword($sIsland,$HinputPassword)) {
				# password間違い
				unlock();
				tempWrongPassword();
				return;
			}

			# オーナー名を設定
			# $HlbbsName = $sIsland->{'owner'};

			# 通信費用を払う
			my($cost) = ($HlbbsType eq 'PUBLIC') ? $HlbbsMoneyPublic : $HlbbsMoneySecret;
			if ($sIsland->{'money'} < $cost) {
				# 費用不足
				unlock();
				tempLbbsNoMoney();
				return;
			}
			$sIsland->{'money'} -= $cost;
		}

		# 発言者を記憶する
		if ($HlbbsType ne 'ANON') {
			# 公開と極秘
			my $name = islandName($sIsland);
			$speaker = $name . ',' . $HspeakerID;
		} else {
			# 匿名
			$speaker = $ENV{'REMOTE_HOST'};
			$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
		}
	} elsif ($HlbbsMode == 2) {
		# 観光者削除モード

		# なぜかその島がない場合
		if($number eq '') {
			unlock();
			tempProblem();
			return;
		}

		# IDチェック
		$lbbs->[$HcommandPlanNumber] =~ /[0-9]*\<.*,([0-9]+)\<.*\>.*\>.*$/;
		my $wId = $1;
		if($wId != $HspeakerID) {
			# ID間違い
			unlock();
			tempWrong("あなたの発言ではありません！");
			return;
		}

		# パスワードチェック
		if(!checkPassword($sIsland,$HinputPassword)) {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	} elsif ($HlbbsMode == 4) {
		# 観光者極秘通信確認モード

		# なぜかその島がない場合
		if($number eq '') {
			unlock();
			tempProblem();
			return;
		}

		# パスワードチェック
		if(!checkPassword($sIsland,$HinputPassword)) {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}

	# モードで分岐
	$HlbbsView = $HlbbsViewMax if(!$HlbbsView);
	if($HlbbsMode == 2 || $HlbbsMode == 3 || $HlbbsMode == 9) {
		# 削除モード
		if(($HlbbsMode == 3 || $HlbbsMode == 9) && ($HcommandPlanNumber == -1)) {
			splice(@$lbbs, 0, $HlbbsView);
		} else {
			splice(@$lbbs, $HcommandPlanNumber, 1);
		}
		tempLbbsDelete() if($HlbbsMode != 9);
	} elsif($HlbbsMode == 7 || $HlbbsMode == 1 || $HlbbsMode == 0) {
		# 記帳モード
		$speaker = "管理人,0" if($HlbbsMode == 7);
		if ($HlbbsType ne 'SECRET') {
			# 公開と匿名
			$speaker = "0<$speaker";
		} else {
			# 極秘
			$speaker = "1<$speaker";
		}
		# メッセージを後ろにずらす
		slideLbbsMessage($lbbs);

		# メッセージ書き込み
		my($message);
		if($HlbbsMode == 1) {
			$message = '1';
		} else {
			$message = '0';
		}
		# IPと日時を取得
		my $addr    = $ENV{'REMOTE_ADDR'};
		my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + $Hjst);
		my $day = ('日','月','火','水','木','金','土')[$wday];
		$year = $year + 1900;
		$mon = $mon + 1;
		my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);
		$message .= ",$date,$addr";

		$HlbbsName = "$HislandTurn：" . htmlEscape($HlbbsName);
		$HlbbsMessage = htmlEscape($HlbbsMessage);
		$lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";

		tempLbbsAdd() if($HlbbsMode != 7);
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);

	# もとのモードへ
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

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
#	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsView - 1] = '';
}

#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
sub tempLbbsMain {
	my($mode) = @_;

	out("<DIV ID='localBBS'>");
	tempLbbsHead();     # ローカル掲示板
	# 書き込みフォーム
	out("<TABLE><TR><TD class='M'>");
	if($mode) {
		tempLbbsInputOW();
	} else {
		tempLbbsInput();
	}
	out("</TD></TR><TR><TD class='M'>");
	tempLbbsContents(); # 掲示板内容
	out("</TD></TR></TABLE></DIV>");
}

# ローカル掲示板
sub tempLbbsHead {
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}観光者通信${H_tagBig}<BR>
END
}

# ローカル掲示板入力フォーム
sub tempLbbsInput {
	out(<<END);
<FORM action="$HthisFile" method="POST">
END
	if ($HlbbsMoneyPublic + $HlbbsMoneySecret > 0) {
		# 発言は有料
		out("<DIV align='center'><B>※</B>");
		out("公開通信は<B>$HlbbsMoneyPublic$HunitMoney</B>です。") if ($HlbbsMoneyPublic > 0);
		out("極秘通信は<B>$HlbbsMoneySecret$HunitMoney</B>です。") if ($HlbbsMoneySecret > 0);
		out("</DIV>");
	}
	my $col = " colspan=2";

	# out("<B>※</B>${AfterName}を持っている方は名前を変更しても所有者名が使われます。");

	out(<<END);
<TABLE BORDER width=100%>
<TR>
<TH>名前<small>(全角${HlengthLbbsName}字まで)</small></TH>
<TH$col>内容<small>(全角${HlengthLbbsMessage}字まで)</small></TH>
<TH>通信方法</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD$col><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
<TD>
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>公開
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>極秘</span>
</TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH>${AfterName}名</TH>
<TH$col>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=16 MAXLENGTH=16 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD>
<SELECT NAME="ISLANDID2">$HislandList</SELECT>
END
	out(<<END) if ($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">観光客
END

	out(<<END);
</TD>
<TD><DIV align='center'>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonSS$HcurrentID">
<INPUT TYPE="submit" VALUE="極秘確認" NAME="LbbsButtonCK$HcurrentID">
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
<INPUT TYPE="submit" VALUE="閲覧" NAME="LbbsButtonVS$HcurrentID">
END
	}
	if(!$HlbbsAnon) {
		out(<<END);
No.
<SELECT NAME=NUMBER>
END
		# 発言番号
		my($j, $i);
		for($i = 0; $i < $HlbbsView; $i++) {
			$j = $i + 1;
			out("<OPTION VALUE=$i>$j\n");
		}
		out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除" NAME="LbbsButtonDS$HcurrentID">
END
	}
	out(<<END);
</TD>
</TR>
</FORM>
</TABLE>
END
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {

	out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
END
	# out("<B>※</B>名前を変更しても所有者名が使われます。");

	out(<<END);
<TABLE BORDER width=100%>
<TR>
<TH>名前<small>(全角${HlengthLbbsName}字まで)</small></TH>
<TH COLSPAN=2>内容<small>(全角${HlengthLbbsMessage}字まで)</small></TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=16 MAXLENGTH=16 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳" NAME="LbbsButtonOW$HcurrentID">
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
<INPUT TYPE="submit" VALUE="閲覧" NAME="LbbsButtonVO$HcurrentID">
END
	}

	out(<<END);
No.
<SELECT NAME=NUMBER>
END
	# 発言番号
	my($j, $i);
	for($i = 0; $i < $HlbbsView; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out("<OPTION VALUE=-1>全\n");
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</FORM>
</TABLE>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
	my($lbbs, $line, $no);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	$no = @$lbbs;
	out(<<END) if($lbbs->[0] ne '0<<0>>' && $lbbs->[0] ne '');
<TABLE BORDER width=100%>
<TR>
<TH>番号</TH>
<TH>記帳内容 (保管記事数:$no)</TH>
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
			my($turn, $name) = split(/：/, $tan);
			$tan = "<A title='[${date}]'>ターン${turn}</A>：$name";
			my $sNo = $HidToNumber{$sID};
			if($sName ne '') {
				if(defined $sNo){
					$speaker = "<span class='lbbsST'><B><SMALL>(<A STYlE=\"text-decoration:none\" HREF=\"$HthisFile?Sight=$sID\" TARGET=_blank>$sName</A>)</SMALL></B></span>";
				} else {
					$speaker = "<span class='lbbsST'><B><SMALL>($sName)</SMALL></B></span>";
				}
			}
			if($os == 0) {
				# 観光者
				if ($m == 0) {
					# 公開
					if($sID ne '0') {
						out("<TD>$HtagLbbsSS_$tan > ${com}$H_tagLbbsSS $speaker</TD></TR>");
					} else {
						out("<TD><span class='lbbsAD'>$tan > ${com}</span> $speaker</TD></TR>");
					}
				} else {
					# 極秘
					if (($HmainMode ne 'owner') &&(($HlbbsMode != 4) || ($HspeakerID eq '') || ($sID != $HspeakerID))) {
						# 観光客
						out("<TD><DIV align='center'><span class='lbbsST'>- 極秘 -</span></DIV></TD></TR>");
					} else {
						# オーナー
						out("<TD><span class='lbbsST'>$tan >(秘) ${com}</span> $speaker</TD></TR>");
					}
				}
			} else {
				# 島主
				out("<TD>$HtagLbbsOW_$tan > ${com}$H_tagLbbsOW $speaker</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE>
END
}

# ローカル掲示板で名前かメッセージがない場合
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}記帳内容を削除しました。${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}記帳を行いました。${H_tagBig}<HR>
END
}

# 通信資金足りず
sub tempLbbsNoMoney {
	out(<<END);
${HtagBig_}資金不足のため記帳できません。${H_tagBig}$HtempBack
END
}

1;
