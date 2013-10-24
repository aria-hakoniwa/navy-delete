# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
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
# トップページモード
#----------------------------------------------------------------------
# メイン
sub topPageMain {

	# アクセス・ログ
	axeslog(0) if($HtopAxes > 2);
	# 開放
	unlock();

	# テンプレート出力
	tempTopPage();
}

# トップページ
sub tempTopPage {
	if($Htournament){
		# トーナメント
		if($HislandFightMode == 0){
			# 予選
#			@HflexTime = @HtmTime1;
		}elsif($HislandFightMode == 1){
			# 開発
#			@HflexTime = @HtmTime2;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 2){
			# 戦闘
#			@HflexTime = @HtmTime3;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 9){
			# 終了
			$HlastTurn = $HislandTurn;
		}
	}

	$HtopTemplateFile = "tempTop.html" if($HtopTemplateFile eq '');
	if($HlayoutTop && (-e "./$HtopTemplateFile")) {
		open(TEMPLATE, "./$HtopTemplateFile") || &tempProblem;
		while ( <TEMPLATE> ) {
			if($_ =~ /<!--title-->/) {
				# タイトル
				out("${HtagTitle_}$Htitle${H_tagTitle}");
				# デバッグモードでクッキーにマスパス(or特殊パス)喰ってたら「ターンを進める」ボタン
				if($Hdebug == 1 && checkSpecialPassword($HdefaultPassword)) {
					out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
				}
				if(-e "./mente_lock") {
					out("${HtagBig_}<span class='attention'>メンテナンス・モード</span>${H_tagBig}");
				}
			} elsif($_ =~ /<!--turn-->/) {
				# ターン・更新時間の情報表示
				tempTopTurnInfo();
			} elsif($_ =~ /<!--link-->/) {
				# リンク表示
				tempTopLink();
			} elsif($_ =~ /<!--login-->/) {
				# ログイン
				tempTopLogin();
			} elsif($_ =~ /<!--island-->/) {
				# 諸島の状況表示 通常
				tempTopIslandView(0);
			} elsif($_ =~ /<!--playerisland-->/) {
				# 諸島の状況表示 プレイヤー島のみ
				tempTopIslandView(1);
			} elsif($_ =~ /<!--battlefield-->/) {
				# 諸島の状況表示 バトルフィールドのみ
				tempTopIslandView(2);
			} elsif($_ =~ /<!--alliance-->/) {
				# 陣営の状況表示
				if($HallyNumber){
					allyInfo(-1);
					my $aStr = ($HarmisticeTurn) ? '陣営' : '同盟';
					out("　<B>※</B>${aStr}の名前をクリックすると「${aStr}の情報」欄へ");
					out("、${HallyTopName}島の名前だと「コメント変更」欄へ") if(!$HarmisticeTurn);
					out("移動します。");
				}
			} elsif($_ =~ /<!--history-->/) {
				# 発見の記録
				out(<<END);
<DIV ID='HistoryLog'>
<H1>発見の記録</H1>
<DIV style="overflow:auto; height:${HdivHeight}px;">
END
				historyPrint();
	out(<<END);
</DIV></DIV>
END
			} elsif($_ =~ /<!--recent-->/) {
				# 近況
				my $hFile;
				if(!$HhtmlLogMode || !(-e "${HhtmlDir}/hakolog.html") || $Hgzip) {
					$hFile = "${HbaseDir}/history.cgi?Event=0&Topmode=1";
				} else {
					$hFile = "${htmlDir}/hakolog.html";
				}
				out(<<END);
<iframe width="100%" height="400" src="$hFile" frameborder="0" scrolling="AUTO" name="log"> 
</iframe>
END
			} elsif($_ =~ /<!--admin-->/) {
				# 管理人だけ島登録できる場合のログイン
				out(<<END) if ($HadminJoinOnly);
<DIV align="right">
<FORM action="$HthisFile" method="POST" style="margin : 2px 0px;">
<INPUT type="hidden" name="Join" value=0>
<INPUT type="password" name="PASSWORD" size=16 maxlength=16 class=f>
<INPUT type="submit" name="submit" value="管理用">
</FORM></DIV>
END
			} elsif($_ =~ /<!--news-->/) {
				# ニュース
				out("$Hnews");
			} else {
				out("$_");
			}
		}
	} else {
		tempTopPageDefault();
	}
}

#「トップページ」デフォルト
sub tempTopPageDefault {
	# リンク表示
#	tempTopLink();
#	out("<HR>");

	# タイトル
	out("${HtagTitle_}$Htitle${H_tagTitle}");

out("Ａ海域は満員になったので、<A HREF=\"http://muhochitai.com/navy2/hako-main.cgi\"><strong>Ｂ海域</strong></A>へ登録お願いします。<BR>");
out("<strong>※他の海域と同時に参加することは出来ません</strong>");
out("<BR>バグ発見の際は、wikiに記載をお願いします。");
out("<A HREF=\"http://www24.atwiki.jp/kyoyuhakoniwa/pages/210.html\">共有箱庭wiki</A><BR>");
out("バグ修正等が遅れる場合がありますが、ご了承ください<br>");

	# デバッグモードなら「ターンを進める」ボタン
	if($Hdebug == 1) {
		out(<<END);
<BR>
<FORM style="display:inline" action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
<FORM style="display:inline" action="$HmenteFile" method="GET">
<INPUT TYPE="hidden" NAME="ADMIN" VALUE="$HdefaultPassword">
<INPUT TYPE="submit" VALUE="管理人室へ" NAME="TurnButton">
</FORM>
END
	}

	if(-e "./mente_lock") {
		out("${HtagBig_}<span class='attention'>メンテナンス・モード</span>${H_tagBig}");
	}

	# ターン・更新時間の情報表示
	tempTopTurnInfo();

	# リンク表示
#	out("<HR>");
#	tempTopLink();

	out(<<END);
<HR>
<TABLE BORDER=0 width="100%">
<TR valign="top">
<TD class="M">
END

	# ログイン
	tempTopLogin();

	# リンク表示
#	out("</TD><TD width=\"35%\" class=\"M\">");
#	tempTopLink();

	out(<<END);
</TD>
<TD class="M">
<DIV ID='HistoryLog'>
<H1>発見の記録</H1>
<DIV style="overflow:auto; height:${HdivHeight}px;">
END

	historyPrint();

	out(<<END);
</DIV></DIV>
</TD></TABLE>
END

	# リンク表示
	out("<HR>");
	tempTopLink();

	# 陣営の状況表示
	if($HallyNumber){
		out("<HR>");
		allyInfo(-1);
		my $aStr = ($HarmisticeTurn) ? '陣営' : '同盟';
		out("　<B>※</B>${aStr}の名前をクリックすると「${aStr}の情報」欄へ");
		out("、${HallyTopName}島の名前だと「コメント変更」欄へ") if(!$HarmisticeTurn);
		out("移動します。");
	}

	out("<HR>");
	# 諸島の状況表示
	tempTopIslandView(0);

	out(<<END) if ($HadminJoinOnly);
<HR>
<DIV align="right">
<FORM action="$HthisFile" method="POST" style="margin : 2px 0px;">
<INPUT type="hidden" name="Join" value=0>
<INPUT type="password" name="PASSWORD" size=16 maxlength=16 class=f>
<INPUT type="submit" name="submit" value="管理用">
</FORM></DIV>
END

}

# 「トップページ」リンク
sub tempTopLink {
	out("<DIV ID='LinkTop'>");
	if( $HsurvivalTurn && ($HislandTurn > $HsurvivalTurn) ) {
		out(qq|<B>※</B>サバイバルモードのため、新しい${AfterName}は探せません。<BR>|);
	} elsif($HislandNumber - $HbfieldNumber >= $HmaxIsland) {
		out(qq|[<span class='attention'>満員御礼</span>] |);
	} elsif(!$HadminJoinOnly) {
		out(qq|[<A href="$HthisFile?Join=0">新しい${AfterName}を探す</A>] |);
	} else {
		out(qq|<B>※</B>新しい${AfterName}を探したい方は「<B>${AfterName}名、あなたの名前、パスワード</B>」を管理人までメールしてください。<BR>|);
	}
	out(qq|[<A href="$HthisFile?Rename=0">${AfterName}の名前とパスワードの変更</A>] |);
	out(qq|[<A href="$HthisFile?Limg=0">画像のローカル設定</A>] |);
	out(qq|[<A href="$HthisFile?Skin=0">箱庭スキンの設定</A>] |) if($HcssSetting);
	out(qq|[<A href="$HthisFile?ICounter=0" target="_blank">カウンター設定</A>] |) if($HcounterSetting && !$Htournament);
	out(qq|[<A href="$HthisFile?JoinA=0">同盟の設定</A>] |) if($HallyUse && !$HarmisticeTurn && !$Htournament);
	out(qq|[<A href="http://muhochitai.com/navy/localrule.htm">ローカルルール</A>] |) if($HallyUse && !$HarmisticeTurn && !$Htournament);
	out(qq|[<A href="http://www24.atwiki.jp/kyoyuhakoniwa/pages/214.html">海戦マニュアルwiki</A>] |) if($HallyUse && !$HarmisticeTurn && !$Htournament);

	my $sftime = (-M "${HefileDir}/setup.html");
	my @Files = ('hako-main.cgi', 'hako-init.cgi', 'init-game.cgi', 'init-server.cgi', 'hako-table.cgi');
	my $sfFlag = 1;
	foreach (@Files) {
		if($sftime >= (-M "./$_")){
			$sfFlag = 0;
			last;
		}
	}
	if((-e "${HefileDir}/setup.html") && $sfFlag) {
		out("[<A href=\"${efileDir}/setup.html\">設定一覧</A>] ");
	} else {
		out("[<A href=\"$HthisFile?SetupV=0\">設定一覧</A>] ");
	}
	out("<BR>");
	my($title) = '';
	$title = '友好国' if($HuseAmity);
	if($HuseDeWar) {
		$title .= '・' if($HuseAmity);
		$title .= '交戦国';
	}
	out(qq|[<A href="$HthisFile?Amity=0" target="_blank">$title一覧</A>] |) if(($HuseAmity || $HuseDeWar) && !$HarmisticeTurn && !$Htournament);
	out(qq|[<A href="$HthisFile?Fleet=1" target="_blank">艦艇保有数一覧</A>] |)if($HnavyName[0] ne '');
	out(qq|[<A href="$HthisFile?Item=0" target="_blank">${HitemName[0]}獲得状況</A>] |) if($HuseItem);
	out(qq|[<A href="$HthisFile?Rank=0" target="_blank">ランキング</A>] |);
	out(qq|[<A href="$HlbbsFile">観光者通信一覧表</A>] |) if($Hlbbslist);
	if(!$HhtmlLogMode || !(-e "${HhtmlDir}/hakolog.html") || $Hgzip) {
		out(qq|[<A href="${HbaseDir}/history.cgi?Event=0" target="_blank">最近の出来事</A>] |);
	} else {
		out(qq|[<A href="${htmlDir}/hakolog.html" target="_blank">最近の出来事</A>] |);
	}
	out(qq|</DIV>|);

}

# 「トップページ」ターン・更新時間の情報
sub tempTopTurnInfo {
	# フォーム
	my $repeat = (($HrepeatTurn == 1) ? '' : "<B>※</B>１回の更新で $HrepeatTurn ターン進行します。");
	my $armTurn = ($HarmisticeTurn < $HsurvivalTurn) ?  $HsurvivalTurn : $HarmisticeTurn;
	if($armTurn && ($HislandTurn < $armTurn) && ($HarmRepeatTurn != $HarmisticeRepeatTurn)) {
		$repeat .= "(戦闘期間は、１回 $HarmRepeatTurn ターン)";
	}
	if ($HjavaModeSet eq 'cgi') {
		$radio = "CHECKED"; $radio2 = "";
	}else{
		$radio = ""; $radio2 = "CHECKED";
	}
	# 0除算回避
	$HrepeatTurn = 1 if(!$HrepeatTurn);
	$HarmRepeatTurn = 1 if(!$HarmRepeatTurn);
	$HarmisticeRepeatTurn = 1 if(!$HarmisticeRepeatTurn);
	# 終了ターン数と終了日時を表示
	my($HlastTurnS, $HlimitTime);
	if(!$HgameLimitTurn) {
		$HlastTurnS = "";
	} elsif($HislandTurn < $HgameLimitTurn) {
		my $remainTime = 0;
		if($HflexTimeSet) {
			my $all = 0;
			foreach (@HflexTime) {
				$all += $_;
			}
			my($tsb, $ts, $tsn, $teb, $te, $ten, $i);
			if($HarmisticeTurn || $HsurvivalTurn) {
				if($HislandTurn < $armTurn) {
					$tsb  = int($HislandTurn / $HrepeatTurn);
				} else {
					$tsb  = int(($HislandTurn - $armTurn) / $HarmRepeatTurn) + int($armTurn / $HarmisticeRepeatTurn);
					$tsb += 1 if(($HislandTurn - $armTurn) % $HarmRepeatTurn);
				}
				$ts  = int($tsb / @HflexTime);
				$tsn = $tsb % @HflexTime;
				$teb  = int(($HgameLimitTurn - $armTurn) / $HarmRepeatTurn) + int($armTurn / $HarmisticeRepeatTurn);
				$teb += 1 if(($HgameLimitTurn - $armTurn) % $HarmRepeatTurn);
				$teb += 1 if($armTurn % $HarmisticeRepeatTurn);
				$te  = int($teb / @HflexTime);
				$ten = $teb % @HflexTime;
			} else {
				$ts  = int(($HislandTurn / $HrepeatTurn) / @HflexTime);
				$tsn = int($HislandTurn / $HrepeatTurn) % @HflexTime;
				$te  = int(int($HgameLimitTurn / $HrepeatTurn) / @HflexTime);
				$ten = int($HgameLimitTurn / $HrepeatTurn) % @HflexTime;
			}
			$remainTime += $all * ($te - $ts - 1);
			if($tsn) {
				foreach($tsn..$#HflexTime) {
					$remainTime += $HflexTime[$_];
				}
			} else {
				$remainTime += $all;
			}
			if($ten) {
				$nine = $ten - 1;
				foreach(0..$nine) {
					$remainTime += $HflexTime[$_];
				}
			}
#			for($i=$HislandTurn; $i < $HgameLimitTurn; $i++) {
#				$remainTime += $HflexTime[($HislandTurn % ($#HflexTime + 1))];
#			}
			$remainTime *= 3600;
		} else {
			if( (($HarmisticeTurn && ($HislandTurn < $HarmisticeTurn))) ||
				(($HsurvivalTurn && ($HislandTurn < $HsurvivalTurn))) ) {
				my $armTurn = (!$HarmisticeTurn) ?  $HsurvivalTurn : $HarmisticeTurn;
				$remainTime = $HunitTime * int(($armTurn - $HislandTurn + ($HrepeatTurn - 1)) / $HrepeatTurn) + $HarmTime * int(($HgameLimitTurn - $armTurn) / $HarmRepeatTurn);
			} else {
				$remainTime = $HunitTime * int(($HgameLimitTurn - $HislandTurn + ($HrepeatTurn - 1)) / $HrepeatTurn);
			}
		}
		$HlimitTime = $HislandLastTime + $remainTime;
		$HlimitTime = sprintf('%d年 %d月 %d日 %d時', (gmtime($HlimitTime + $Hjst))[5] + 1900, (gmtime($HlimitTime + $Hjst))[4] + 1, (gmtime($HlimitTime + $Hjst))[3,2]);
		$HlastTurnS = "<small>／${HgameLimitTurn}<small>《${HlimitTime}まで》</small></small>";
	} else {
		$HlastTurnS = "　（ゲームは終了しました）";
	}

	# 次回更新時間表示
	if($HflexTimeSet) {
		$aaa = $HislandLastTime + 3600 * $HflexTime[(($HislandTurn/$HrepeatTurn) % ($#HflexTime + 1))];
	} else {
		$aaa = $HislandLastTime + $HunitTime;
		if($Htournament && ($HislandTurn >= $HyosenTurn)){
			if($HislandFightMode == 1) {
				if(($HislandTurn > $HyosenTurn) && ($HislandTurn == $HislandChangeTurn - $HdevelopeTurn)){
					$aaa += $HinterTime - $HunitTime;
				} else {
					$aaa += $HdevelopeTime - $HunitTime;
				}
			} elsif($HislandFightMode == 2) {
#				if($HislandTurn == $HislandChangeTurn - $HfightTurn){
#					$aaa += $HdevelopeTime - $HunitTime;
#				} else {
					$aaa += $HfightTime - $HunitTime;
#				}
			}
		}
	}

	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime(time + $Hjst);
	$mon++;
	my($sss) = "${mon}月 ${date}日 ${hour}時 ${min}分 ${sec}秒";
	my($sec2, $min2, $hour2, $date2, $mon2, $year2, $day2, $yday2, $dummy2) = gmtime($aaa + $Hjst);
	$mon2++;
	my($bbb) = '';
	if(!$HgameLimitTurn || ($HislandTurn < $HgameLimitTurn)) {
		$bbb = "${mon2}月 ${date2}日 ${hour2}時 ${min2}分";
	} else {
		$bbb = "更新は停止しています";
	}
	if (!$HplayNow ||
		$HsurvivalTurn && ($islandNumber == $HbfieldNumber) && ($HislandTurn > $HsurvivalTurn) 
	   ) {
		$HlastTurnS = "　（ゲームは終了しました）";
		$bbb = "更新は停止しています";
		$rtStr = "　";
		undef $HleftTime;
	}
	if($HitemComplete) {

		my $cName = islandName($Hislands[$HidToNumber{$HitemComplete}]);
		$HlastTurnS = " Game Over<BR>〜世界は<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=${HitemComplete}\">${HtagName_}${cName}${H_tagName}</A>によって「ひとつ」となった〜";
	} elsif($HitemCompleteA) {
		my $ally = $Hally[$HidToAllyNumber{$HitemCompleteA}];
		my $aName = "<FONT COLOR=\"$ally->{'color'}\"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}";
		$HlastTurnS = " Game Over<BR>〜世界は<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?AmiOfAlly=${HitemCompleteA}\">${HtagName_}${aName}${H_tagName}</A>によって「ひとつ」となった〜";
	}
	# 次のターンまでの時間表示
	if (!($HmainMode eq 'turn') && (defined $HleftTime)) {
		if(!$HgameLimitTurn || ($HislandTurn < $HgameLimitTurn)) {
			my $hour2 = int($HleftTime / 3600);
			my $min2 = int(($HleftTime - $hour2 * 3600) / 60);
			my $sec2 = ($HleftTime - $hour2 * 3600 - $min2 * 60);
			my $nextturn = '';
			foreach (1..$HrepeatTurn) {
				$nextturn .= '・' if($_ != 1);
				$nextturn .= $HislandTurn + $_;
				last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
			}
			$rtStr = "次の更新時間<span class='number'>(ターン$nextturn)</span>まであと $hour2時間 $min2分 $sec2秒";
		} else {
			$rtStr = "　";
		}
	} else {
		if ($HplayNow) {
			$rtStr = "ターンを更新しました\n";
		} else {
			$rtStr = "　";
		}
	}
	my $mode = '';
	$mode = ($HislandTurn < $HarmisticeTurn) ? "(〜$HarmisticeTurn <small>停戦期間</small>)" : ($HislandTurn == $HarmisticeTurn) ? '(<small>次ターンより戦闘期間</small>)' : '(<small>戦闘期間</small>)' if($HarmisticeTurn);
	$mode = ($HislandTurn < $HsurvivalTurn) ? "(〜$HsurvivalTurn <small>停戦期間</small>)" : ($HislandTurn == $HsurvivalTurn) ? '(<small>次ターンより戦闘期間</small>)' : '(<small>戦闘期間</small>)' if($HsurvivalTurn);

	my $eee;
	if($Htournament){
		# トーナメント
		my($tst);
		my $flog = "[<A href=\"$HthisFile?FightLog=0\" class=\"M\" TARGET=_blank>対戦の記録</A>]";
		$HlastTurnS = "";
		if($HislandFightMode == 0){
			# 予選
			if($HislandNumber > $Htournament){
				$tst = $HislandNumber - $Htournament;
				$tst = "<span class=attention>$tst$AfterName沈没</span>し";
			}
			$tst = "<span class=normal>予選終了後、${tst}開発期間に移行します。</span>";
			$mode = "(〜$HislandChangeTurn <small><span class=normal>予選期間</span>　<span class=attention>$Htournament${AfterName}選抜</span></small>)";
		}elsif($HislandFightMode == 1){
			# 開発
			$tst = $HislandChangeTurn + 1;
			$tst = "<span class=normal>${tst}ターンから攻撃開始</span>";
			$mode = ($HislandTurn == $HislandChangeTurn - $HdevelopeTurn) ? "(<small>次ターンより開発期間</small>)" : "(〜$HislandChangeTurn <small>開発期間</small>)";
		}elsif($HislandFightMode == 2){
			# 戦闘
			$mode = ($HislandTurn == $HislandChangeTurn - $HfightTurn) ? "(<small>次ターンより戦闘期間</small>)" : "(〜$HislandChangeTurn <small>戦闘期間</small>)";
		}elsif($HislandFightMode == 9){
			# 終了
			$HlastTurnS = "　（ゲームは終了しました）";
		}
		$mode .= "<small><small>　$tst　</small>$flog</small>";
	} elsif($HplayNow) {
		# 更新頻度表示
		my $safety = 0;
		my $itn = $HislandTurn;
		my $ddd = $aaa;
		my @ctime;
		while($safety++ < 100) {
			my($sec3, $min3, $hour3, $date3, $mon3, $year3, $day3, $yday3, $dummy3) = gmtime($ddd + $Hjst);
			$mon3++;
			$eee = "${hour3}時";
			$eee .= "${min3}分" if($min3);
			last if($checkTime{$eee});
			push(@ctime, $eee);
			$checkTime{$eee} = $safety;
			if($HflexTimeSet) {
				$itn += $HrepeatTurn;
				$ddd += 3600 * $HflexTime[(($itn/$HrepeatTurn) % ($#HflexTime + 1))];
			} else {
				$ddd += $HunitTime;
			}
		}
		$ddd -= $aaa;
		$ddd /= (3600 * 24);
		if($ddd == 1) {
			@ctime = sort {$a <=> $b} @ctime;
			$ddd = '';
		}
		my $ct = @ctime;
		$eee = "[更新頻度 ${ct}回/${ddd}日";
		$safety = 0;
		if($ct <= 24) {
			$eee .= "：";
			foreach (@ctime) {
				$eee .= "/" if($safety++);
				if($checkTime{$_} == $ct) {
					$eee .= "<span class='point'>" . $_ . "</span>";
				} elsif($checkTime{$_} == 1) {
					$eee .= "<span class='number'>" . $_ . "</span>";
				} else {
					$eee .= $_;
				}
			}
		}
		$eee .= "]";
	}
	out(<<END);
<DIV ID='Turn'>
<H1><SMALL><B>ターン</B> </SMALL>$HislandTurn<SMALL>${mode}$HlastTurnS</SMALL></H1>
</DIV>
<DIV class='timer'>$rtStr</DIV>
<DIV ID=nexttime>現在の時間：<b>$sss</b>　（次回の更新時間：$bbb）</DIV><br>
$repeat
$eee
$Htitler
END

	# サバイバルモード表示
	if($HsurvivalTurn) {
		my($tflag);
		$tflag = int(($HislandTurn - $HsurvivalTurn)/$HturnDead) if($HturnDead);
		$tflag = 0 if($tflag < 0);
		my $turnDead = $HsurvivalTurn + $HturnDead * ($tflag + 1);
		my $sur = ($repeat eq '') ? '<span class=attention>※</span>' : '<BR><span class=attention>※</span>';
		my $predelNumber = @HpreDeleteID;
		my($rem) = $HislandNumber - $predelNumber - $HbfieldNumber;
		my $ccc = (!$rem) ? 0 : sprintf("%.1f", 50/$rem);
		if($HislandTurn < $HsurvivalTurn) {
			my $sTurn = $HsurvivalTurn + 1;
			$sur .= "${sTurn}ターン以降、${HturnDead}ターンごとに最下位の島が沈みます。最初の沈没判定は<span class=attention>$turnDeadターン</span>です。<br>　　(占有率<span class=attention>$ccc%未満</span>でも消滅します)<br>"
		} else {
			$sur .= "${HturnDead}ターンごとに最下位の島が沈みます。次回の沈没判定は<span class=attention>$turnDeadターン</span>です。<br>　　(占有率<span class=attention>$ccc%未満</span>でも消滅します)<br>"
		}
		out("$sur");
	}

}

# 「トップページ」ログイン
sub tempTopLogin {
	my($wNo) = random(1000);
	out(<<END);
<DIV ID='myIsland'>
<H1>自分の${AfterName}へ</H1>
<FORM name="Island" action="$HthisFile" method="POST">
あなたの${AfterName}の名前は？<BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}を選択して下さい-
$HislandList
</SELECT><BR><BR>
パスワードをどうぞ！！<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32 class=f><BR>
<a STYlE="text-decoration:none; color: #000000;" href="javascript: checkOptions(0);">
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>通常モード(JS)</a>
<a STYlE="text-decoration:none; color: #000000;" href="javascript: checkOptions(1);">
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>旧モード</a><BR>
<INPUT TYPE="submit" VALUE="開発しに行く" onClick="develope()">　
<INPUT TYPE="button" VALUE="新しい画面" onClick="newdevelope()">
</FORM>
<SCRIPT language="JavaScript">
<!--
function checkOptions(i){
	if(document.Island.JAVAMODE[i].checked){
	} else {
		document.Island.JAVAMODE[i].checked = true;
	}
}
function newdevelope(){
//	newWindow$wNo = window.open("", "newWindow$wNo");
	document.Island.target = "newWindow$wNo";
	document.Island.submit();
}
function develope(){
	document.Island.target = "";
}
// -->
</SCRIPT>
</DIV>
END

}

# 「トップページ」諸島の状況
sub tempTopIslandView {
	my($bfMode) = @_;
	# 0:通常,1:プレイヤー島のみ,2:バトルフィールドのみ

	islandSort($HrankKind, 1);

	out("<DIV ID='islandView'>");

	out(<<END) if($bfMode < 2);
<A name="View"></A>
<P><H1 style="display:inline;">諸${AfterName}の状況</H1>　
${AfterName}の名前をクリックすると、<B>観光</B>することができます。
</P>
END

	my($allpop, $island, $j, $pop, $area, $food, $foodrate, $money, $farm, $factory, $mountain, $name, $id, $prize, $ii, $jj, $k);
	my $col = 6;
	my($mapStr)= '';
	if($HoceanMode && $HuseOceanMap) {
		$mapStr1 = "<TH $HbgTitleCell>${HtagTH_}座標${H_tagTH}</TH>";
		$col++;
	}
	my($sStr1)= '';
	if($HsurvivalTurn) {
		my $predelNumber = @HpreDeleteID;
		my $remainNumber = $islandNumber - $predelNumber;
		foreach $i ($HbfieldNumber..$remainNumber) {
			$allscore += $Hislands[$i]->{$HrankKind};
		}
		$sStr1 = "<TH $HbgTitleCell>${HtagTH_}占有率${H_tagTH}</TH>";
		$col++;
	}
	my($vsith)= '';
	if($Htournament){
		$vsith = "<TH $HbgTitleCell>${HtagTH_}対戦相手${H_tagTH}</TH>";
		$col++;
	}

	my($mStr1) = '';
	if($HhideMoneyMode != 0) {
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>";
		$col++;
	}

	# 駐留状況調査
	my(%invade, %shipList);
	my $iFlag = 0;
	foreach $i (0..$islandNumber) {
		my $island = $Hislands[$i];
		my $id = $island->{'id'};
		my $name = islandName($island);
		foreach (@{$island->{'fkind'}}) {
			my($eId, $nFlag, $nNo, $nKind) = (navyUnpack(hex($_)))[0,5..7];
			next if(($HnavySpecial[$nKind] & 0x8) || ($nFlag & 1)); # 軍港・残骸は除外
			next if ($HnavyNoMove[$nKind]); # 海上防衛とかは除外
			if(($eId != $id) && (defined $HidToNumber{$eId})) {
				$invade{"$eId,$id,$nNo"}++;
				$iFlag = 1;
			}
		}
	}
	if($iFlag) {
		foreach (sort { $a cmp $b } keys %invade) {
			my($id,$iId,$iNo) = split(/\,/, $_);
			my $in = $HidToNumber{$iId};
			my $iName = islandName($Hislands[$in]);
			$shipList{$id} .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]艦隊($invade{$_}艦)<BR>";
#			$sshipList{$id} .= "${iName} [$Hislands[$in]->{'epoint'}{$id}]\n";
		}
	}

	$HviewIslandCount = 1 if(!$HviewIslandCount);
	$jj = int(($islandNumber + $HviewIslandCount - $HbfieldNumber) / $HviewIslandCount);
	if(($jj > 1) && ($bfMode < 2)) {
		for($ii = 0; $ii < $jj; $ii++) {
			$j = $ii * $HviewIslandCount;
			$k = min($j + $HviewIslandCount, $HislandNumber - $HbfieldNumber);
			$j++;
			$j = "★" if(!$ii && $HbfieldNumber && !$bfMode);

#			out(qq|<A href="$HthisFile?View=$ii#View">${HtagNumber_}[$j〜$k]${H_tagNumber}</A>&nbsp;|);
		}
	}
	my($pStr1, $nStr1);
	if($HrankKind eq 'point') {
		$pStr1 = "<TH $HbgTitleCell>${HtagTH_}$HpointName${H_tagTH}</TH>";
		$col++;
	}
	if($HnavyName[0] ne '') {
		$nStr1 = "<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>";
		$col++;
	}
	out("<TABLE BORDER>");

	my($head);
	$head = <<"END";
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
$mapStr1
$sStr1
$vsith
$pStr1
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}食料レート${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}農場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
$nStr1
END

	$head .= "<TH $HbgTitleCell>${HtagTH_}他島からの派遣艦隊${H_tagTH}</TH>" if($iFlag);
	$head .= "</TR>";

#	out("$head") if($HbfieldNumber);
	$HviewIslandNumber *= $HviewIslandCount;

	my($start, $end) = ($HviewIslandNumber + $HbfieldNumber, min($HviewIslandNumber + $HviewIslandCount + $HbfieldNumber, $HislandNumber));
	$start = 0 if(!$HviewIslandNumber && $bfMode != 1);
	$end = $HbfieldNumber if($bfMode > 1);

	for($ii = 0; $ii < $HislandNumber; $ii++) {
#	for($ii = $start; $ii < $end; $ii++) {
		my($tmpHbgNumberCell, $tmpHbgNameCell, $tmpHbgInfoCell, $tmpHbgCommentCell) = ($HbgNumberCell, $HbgNameCell, $HbgInfoCell, $HbgCommentCell);

		$j = $ii + 1 - $HbfieldNumber;
		$island = $Hislands[$ii];
		out("<TR><TH></TH></TR><TR><TH></TH></TR>$head") if(($HbfieldNumber && $j == 1) || ($ii == $start));
		if($Htournament && ($j > $Htournament) || $island->{'predelete'}) {
			($tmpHbgNumberCell, $tmpHbgNameCell, $tmpHbgInfoCell, $tmpHbgCommentCell) = ($HbgNumberCell . 'T', $HbgNameCell . 'T', $HbgInfoCell . 'T', $HbgCommentCell . 'T');
		}
		$id = $island->{'id'};
		$pop = ($island->{'pop'} == 0) ? "無人" : "$island->{'pop'}$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($island->{'area'} == 0) ? "海域" : "$island->{'area'}$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($island->{'food'} == 0) ? "備蓄ゼロ" : "$island->{'food'}$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
                # 追加
                $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
                $foodrate .= '億円/10000トン';
		$farm = ($island->{'farm'} == 0) ? "保有せず" : "$island->{'farm'}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($island->{'factory'} == 0) ? "保有せず" : "$island->{'factory'}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($island->{'mountain'} == 0) ? "保有せず" : "$island->{'mountain'}0$HunitPop";
		1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$name = islandName($island);
		if($island->{'field'}) {
			$j = "★";
			$name = "${HtagNumber_}${name}${H_tagNumber}";
		} elsif($island->{'absent'} == 0) {
			$name = "${HtagName_}${name}${H_tagName}";
		} else {
			$name = "${HtagName2_}${name}($island->{'absent'})${H_tagName2}";
		}
		$name .= "${HtagDisaster_}★${H_tagDisaster}" if ($HislandTurn - $island->{'birthday'} <= $HdevelopTurn);
		if($island->{'predelete'}) {
			my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
			$name = "${HtagDisaster_}【管理人あずかり】$rest${H_tagDisaster}<BR>　" . $name;
		}
		my $event = '';
		if($island->{'event'}[0]) {
			my $type  = $HeventName[$island->{'event'}[6]];
			if(($island->{'event'}[1] - $HnoticeTurn <= $HislandTurn) && ($HislandTurn < $island->{'event'}[1])) {
				$event = "${HtagDisaster_}$type${H_tagDisaster}開催！<BR>　${HtagNumber_}$island->{'event'}[1]${H_tagNumber}ターン〜<BR>　";
			} elsif($island->{'event'}[1] <= $HislandTurn) {
				my $rest = $island->{'event'}[1] + $island->{'event'}[2] - $HislandTurn;
				if($rest > 0) {
					$rest = "あと${HtagNumber_}${rest}${H_tagNumber}ターン";
				} else {
					$rest = 1 - $rest;
					$rest = "サドンデス(${HtagNumber_}${rest}${H_tagNumber})";
				}
				$event = "${HtagDisaster_}$type${H_tagDisaster}開催中！<BR>　$rest<BR>　";
			}
		}
		$name = $event . $name;
		$prize = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
		my($flags, $monsters, $hmonsters, $turns) = ($1, $2, $3, $4);
		$prize = '';

		my($i, $s, $ss);

		# アイテムの表示
		foreach (@{$island->{'item'}}) {
			next if($_ == 0);
			$prize .= "<IMG SRC=\"$HitemImage[$_]\" TITLE=\"$HitemName[$_]\" onMouseOver='status=\"$HitemName[$_]\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16> ";
		}


		# ターン杯の表示
		$s = '';
		my @turnPrize = reverse(split(/,/, $turns));
		$i = 0;
		foreach (@turnPrize) {
			last if($i > 3);
			$s .= "\n" if($i++);
			$s .= "$_${Hprize[0]->{'name'}}";
		}
		my $tNum = @turnPrize;
		$s .= ($i < $tNum ? "\n他、${tNum}回受賞" : "\n以上${tNum}回受賞") if($tNum);
		$ss = $s;
		my $rt = "\n";
		$ss =~ s/$rt/ /g;
		$prize .= "<IMG SRC=\"prize0.gif\" TITLE=\"${s}\" onMouseOver='status=\"${ss}\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16> " if($s ne '');

		# 島名に称号を追加
		my($f) = 2;
		my($max) = -1;
		my($wintitle, $winmark);
		if($HitemComplete == $island->{'id'}) {
			$max = 0;
			$wintitle = "[${HwinnerTitle[0]}]";
			$winmark = "<IMG SRC=\"${HwinnerMark[0]}\" style=\"border-width: 0px;\" TITLE=\"${HwinnerTitle[0]}\" onMouseOver='status=\"${HwinnerTitle[0]}\"; return true;' onMouseOut=\"status = '';\">";
		}
		if($island->{'ext'}[0]) {
			foreach (1..$#HwinnerTitle) {
				if($island->{'ext'}[0] & $f) {
						$max = $_;
						$wintitle .= "\n" if($wintitle ne '');
						$wintitle .= "[${HwinnerTitle[$_]}]";
						$winmark .= "<IMG SRC=\"${HwinnerMark[$_]}\" style=\"border-width: 0px;\" TITLE=\"${HwinnerTitle[$_]}\" onMouseOver='status=\"${HwinnerTitle[$_]}\"; return true;' onMouseOut=\"status = '';\">";
				}
				$f *= 2;
			}
		}
		if($max != -1) {
			if($HviewMarkOne) {
				$winmark = "<IMG SRC=\"${HwinnerMark[$max]}\" style=\"border-width: 0px;\" TITLE=\"${wintitle}\" ";
				$wintitle =~ s/$rt//g;
				$winmark .= "onMouseOver='status=\"${wintitle}\"; return true;' onMouseOut=\"status = '';\">";
			}
			$winmark .= '<BR>';
		}
		# 名前に賞の文字を追加
		$f = 1;
		$s = '';
		foreach(1..$#Hprize) {
			if($flags & $f) {
				$s .= "<IMG SRC=\"prize${_}.gif\" TITLE=\"${Hprize[$_]->{'name'}}\" onMouseOver='status=\"${Hprize[$_]->{'name'}}\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>";
			}
			$f *= 2;
		}
		$prize .= $s;

		# 撃破した島名を追加
		$s = '';
		my @defeat = @{$island->{'defeat'}};
		for($i = 0; $i < $#defeat; $i+=2) {
			$s .= "\n" if($i);
			$s .= $defeat[$i] . '(' . $defeat[$i+1] . ')';
		}
		$s =~ s/<FONT COLOR=\"[\w\#]+\"><B>(.*)<\/B><\/FONT>/$1/g;
		$s =~ s/<[^<]*>//g;
		$ss = $s;
		$ss =~ s/$rt/ /g;
		$f = @defeat / 2;
		$prize .= "<span class='point'><IMG SRC=\"land13.gif\" TITLE=\"${s}\" onMouseOver='status=\"${ss}\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$f$AfterName撃破</span> " if($s ne '');

		# 倒した怪獣リスト
		$f = 1;
		$s = '';
		$max = -1;
		my($mNameList) = '';
		my $hflag = 0;
		for($i = 0; $i < $HmonsterNumber; $i++) {
			if($monsters & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HmonsterName[$i]]";
				$max = $i;
#				$s .= "<IMG SRC=\"${HmonsterImage[$i]}\" ALT=\"$HmonsterName[$i]\" WIDTH=16 HEIGHT=16> ";
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
#				$s .= "<IMG SRC=\"${HhugeMonsterImageS[$i]}\" ALT=\"$HhugeMonsterName[$i]\" WIDTH=16 HEIGHT=16> ";
			}
			$f *= 2;
		}
		if($max != -1) {
			my $image = ($hflag ? $HhugeMonsterImageS[$max] : $HmonsterImage[$max]);
			$s .= " <span class='monsm'><IMG SRC=\"${image}\" TITLE=\"$mNameList\" ";
			$mNameList =~ s/$rt//g;
			$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$island->{'monsterkill'}$HunitMonster退治</span> ";

			$prize .= $s;
		}


		# 出現中の怪獣リスト
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
			$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$monslive$HunitMonster出現中！</span> ";

			$prize .= $s;
		}
		# 所属不明艦
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
			$s .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\" WIDTH=16 HEIGHT=16>$unknownlive艦出現中！</span> ";

			$prize .= $s;
		}
		$prize = '　' if($prize eq '');

		$mapStr = '';
		if($HoceanMode && $HuseOceanMap) {
			$mapStr1 = "<TD $tmpHbgInfoCell align=right><a href='$HthisFile?OceanMap=$island->{'id'}' style='text-decoration: none;'><B>($island->{'wmap'}->{'x'}, $island->{'wmap'}->{'y'})</B></a></TD>";
		}
		$sStr1 = '';
		if($HsurvivalTurn) {
#			my $occupation = $allscore ? int((100 * $island->{'pop'})/$allscore) : 0;
#			$occupation = 100 if($occupation > 100);
			my $occupation = $allscore ? sprintf("%.1f", (100 * $island->{'pop'})/$allscore) : 0;
			$occupation = "100.0" if($occupation > 100);
			$sStr1 = "<TD $tmpHbgInfoCell align=right>${occupation}%</TD>";
			$sStr1 = "<TD $tmpHbgInfoCell align=right>−</TD>" if($island->{'field'} || $island->{'predelete'});
		}
		my($vsith)= '';
		if($Htournament){
			my $tName = "";
			my $ps = 'center';
			if($island->{'field'}) {
				$tName = "<B>---</B>";
			} elsif($HislandFightMode == 9) {
				$tName = "<B>- 終了 -</B>";
			} elsif($island->{'rest'}) {
				$tName = "<B>不戦勝</B><small>　開発停止：残</small>${HtagDisaster_}$island->{'rest'}${H_tagDisaster}";
				$ps = 'right';
			} elsif($island->{'fight_id'} == -2) {
				$tName = "<B>- 圧勝！ -</B>";
			} elsif($island->{'fight_id'} == -1) {
				$tName = "<B>- 不戦勝 -</B>";
			} elsif($island->{'predelete'}) {
				$tName = "<B>- 敗退 -</B>";
			} elsif($island->{'fight_id'} == 0) {
				$tName = "<B>- 未定 -</B>";
			} else {
				my $tn = $HidToNumber{$island->{'fight_id'}};
				if($tn eq '') {
					$tName = "<B>- 未定 -</B>";
				} else {
					my $tIsland = $Hislands[$tn];
					$tName = islandName($tIsland);
					$tName = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$tIsland->{'id'}\"><B>$tName</B></A>";
					$ps = 'center';
				}
			}
			$vsitd = "<TD $tmpHbgNameCell align=$ps>$tName</TD>";
		}
		 $mStr1 = '';
		if($HhideMoneyMode == 1) {
			$money = ($island->{'money'} == 0) ? "資金ゼロ" : "$island->{'money'}$HunitMoney";
			1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mStr1 = "<TD $tmpHbgInfoCell align=right>$money</TD>";
		} elsif($HhideMoneyMode == 2) {
			my($mTmp) = aboutMoney($island->{'money'});
			1 while $mTmp =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mStr1 = "<TD $tmpHbgInfoCell align=right>$mTmp</TD>";
		}
		my $preab = ($island->{'preab'} ? '<br><small><span class=attention>(陣営開発可)</span></small>' : '');

		out(<<END);
<TR>
<TD $tmpHbgNumberCell ROWSPAN=3 align=center>${HtagNumber_}$j${H_tagNumber}</TD>
<TD $tmpHbgNameCell ROWSPAN=3 align=left>
<A STYlE="text-decoration:none" HREF="${HthisFile}?Sight=${id}" TITLE="ID=${id}">
$winmark$name
</A>$preab
END

		my $ownerName = (($island->{'owner'} eq '') || $island->{'field'}) ? 'コメント' : "<A TITLE='所有者'>$island->{'owner'}</A>";
		my $navyComLevel = gainToLevel($island->{'gain'});
		my $totalExp = $island->{'gain'};
		1 while $totalExp =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
		$pStr1 = '';
		if($HrankKind eq 'point') {
			my $point = $island->{'point'};
			1 while $point =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$pStr1 = "<TD $tmpHbgInfoCell align=right>$point$HpointAfter</TD>";
		}
		$nStr1 = '';
		if($HnavyName[0] ne '') {
			$nStr1 = "<TD $tmpHbgInfoCell align=right>$totalExp</TD>";
		}

		out(<<END);
</TD>
$mapStr1
$sStr1
$vsitd
$pStr1
<TD $tmpHbgInfoCell align=right>$pop</TD>
<TD $tmpHbgInfoCell align=right>$area</TD>
$mStr1
<TD $tmpHbgInfoCell align=right>$foodrate</TD>
<TD $tmpHbgInfoCell align=right>$farm</TD>
<TD $tmpHbgInfoCell align=right>$factory</TD>
<TD $tmpHbgInfoCell align=right>$mountain</TD>
$nStr1
END

		my $slist = ($shipList{$id}) ? $shipList{$id} : '　';
		out("<TD $tmpHbgInfoCell ROWSPAN=3 align=left valign=top>$slist</TD>") if($iFlag);
#HdebugOut("------- $HislandTurn -------\n$sshipList{$id}\n") if($island->{'event'}[0]);
		out(<<END);
</TR>
<TR>
<TD $tmpHbgCommentCell COLSPAN="$col" align=left>${HtagTH_}$ownerName：${H_tagTH}$island->{'comment'}</TD>
</TR>
<TR>
<TD $tmpHbgCommentCell COLSPAN="$col" align=left>$prize</TD>
</TR>
END
		if($Htournament) {
			my $colT = $col + 2;
			$colT++ if($iFlag);
			if(($j == $Htournament) && ($HislandTurn < $HyosenTurn)) {
				out("<TR><TH colspan=$colT><FONT SIZE=+1 COLOR=#C00000><i>−　予選通過ライン　−</I></FONT></TH></TR>");
				out("$head") if($ii < $end - 1);
			}
		}
	}

	out("</TABLE>");
	out("　<B>※</B>新しく発見された${AfterName}は${AfterName}名の右端に${HtagDisaster_}★${H_tagDisaster}が付いています。${HtagDisaster_}★${H_tagDisaster}が消えるまで開発に専念しましょう。") if($HdevelopTurn && ($bfMode < 2));
	out("</DIV>");

}

# 記録ファイル表示
sub historyPrint {
	open(HIN, "${HdirName}/hakojima.his");
	my(@line, $l);
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
	}
	@line = reverse(@line);

#	my($this, $next);
	foreach $l (@line) {
		$l =~ /^([0-9]*),(.*)$/;
		out("${HtagNumber_}<small>ターン</small>${1}${H_tagNumber}：${2}<BR>\n");
#		$next = $1;
#		my($str) = $2;
#		if($this != $next) {
#			out("${HtagNumber_}ターン ${next}${H_tagNumber} ---<BR>\n");
#			$this = $next;
#		}
#		out("　$str<BR>\n");
	}
	close(HIN);
}

# 同盟の情報
sub amityOfAlly() {
	# 開放
	unlock();

	my $ally = $Hally[$HidToAllyNumber{$HallyID}];
	my $allyName = "<FONT COLOR=\"$ally->{'color'}\"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}";

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='campInfo'>
<H1>$allyNameの情報</H1>
END

	allyInfo($HallyID) if($ally->{'number'});

	my($mStr1) = '';
	my $col = 9;
	if($HhideMoneyMode != 0) {
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>";
		$col++;
	}
	if($ally->{'message'} ne '') {
		my $allyTitle = $ally->{'title'};
		$allyTitle = '盟主からのメッセージ' if($allyTitle eq '');
		my $allyMessage = $ally->{'message'};
		$allyMessage =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target='_top'>$2<\/a>/g;
		out(<<END);
<HR>
<TABLE BORDER width=80%>
<TR><TH $HbgTitleCell>${HtagTH_}$allyTitle${H_tagTH}</TH></TR>
<TR><TD $HbgInfoCell><blockquote>$allyMessage</blockquote></TD></TR>
</TABLE>
END
	}

	my($pStr1);
	if($HrankKind eq 'point') {
		$pStr1 = "<TH $HbgTitleCell>${HtagTH_}$HpointName${H_tagTH}</TH>";
		$col++;
	}

	out(<<END);
<HR>
<TABLE BORDER><TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
$pStr1
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}農場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>
</TR>
END
	out("<TR><TH colspan=$col>所属している$AfterNameがありません！</TH></TR>") if(!$ally->{'number'});

	my($id, $number, $island, $pop, $area, $food, $foodrate, $money, $farm, $factory, $mountain, $name, $mStr2, $navyComLevel, $totalExp);
	foreach (@{$ally->{'memberId'}}) {
		$id = $_;
		$number = $HidToNumber{$id};
		$island = $Hislands[$number];
		$number += (1 - $HbfieldNumber);
		$pop = ($island->{'pop'} == 0) ? "無人" : "$island->{'pop'}$HunitPop";
		1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$area = ($island->{'area'} == 0) ? "海域" : "$island->{'area'}$HunitArea";
		1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$food = ($island->{'food'} == 0) ? "備蓄ゼロ" : "$island->{'food'}$HunitFood";
		1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
                # 追加
                $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
                $foodrate .= '億円/10000トン';
		$farm = ($island->{'farm'} == 0) ? "保有せず" : "$island->{'farm'}0$HunitPop";
		1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$factory = ($island->{'factory'} == 0) ? "保有せず" : "$island->{'factory'}0$HunitPop";
		1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mountain = ($island->{'mountain'} == 0) ? "保有せず" : "$island->{'mountain'}0$HunitPop";
		1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
		# 島名に称号を追加(未使用・$nameの前に$winnerをつければよい)
		my($rt) = "\n";
		my($f) = 2;
		my($max) = -1;
		my($wintitle, $winmark);
		if($HitemComplete == $island->{'id'}) {
			$max = 0;
			$wintitle = "[${HwinnerTitle[0]}]";
			$winmark = "<IMG SRC=\"${HwinnerMark[0]}\" style=\"border-width: 0px;\" TITLE=\"${HwinnerTitle[0]}\" onMouseOver='status=\"${HwinnerTitle[0]}\"; return true;' onMouseOut=\"status = '';\">";
		}
		if($island->{'ext'}[0]) {
			foreach (1..$#HwinnerTitle) {
				if($island->{'ext'}[0] & $f) {
						$max = $_;
						$wintitle .= "\n" if($wintitle ne '');
						$wintitle .= "[${HwinnerTitle[$_]}]";
						$winmark .= "<IMG SRC=\"${HwinnerMark[$_]}\" style=\"border-width: 0px;\" TITLE=\"${HwinnerTitle[$_]}\" onMouseOver='status=\"${HwinnerTitle[$_]}\"; return true;' onMouseOut=\"status = '';\">";
				}
				$f *= 2;
			}
		}
		if($HviewMarkOne && ($max != -1)) {
			$winmark = "<IMG SRC=\"${HwinnerMark[$max]}\" style=\"border-width: 0px;\" TITLE=\"${wintitle}\" ";
			$wintitle =~ s/$rt//g;
			$winmark .= "onMouseOver='status=\"${wintitle}\"; return true;' onMouseOut=\"status = '';\">";
		}
		$name = islandName($island);
		if($island->{'field'}) {
			$number = "★";
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
		$mStr2 = '';
		if($HhideMoneyMode == 1) {
			$money = ($island->{'money'} == 0) ? "資金ゼロ" : "$island->{'money'}$HunitMoney";
			1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mStr2 = "<TD $HbgInfoCell align=right>$money</TD>";
		} elsif($HhideMoneyMode == 2) {
			my($mTmp) = aboutMoney($island->{'money'});
			1 while $mTmp =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$mStr2 = "<TD $HbgInfoCell align=right>$mTmp</TD>";
		}
		$navyComLevel = gainToLevel($island->{'gain'});
		$totalExp = $island->{'gain'};
		1 while $totalExp =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
		my($pStr2);
		if($HrankKind eq 'point') {
			my $point = $island->{'point'};
			1 while $point =~ s/(.*\d)(\d\d\d)/$1,$2/;
			$pStr2 = "<TD $HbgInfoCell align=right>$point$HpointAfter</TD>";
			$col++;
		}

	out(<<END);
<TR>
<TD $HbgNumberCell align=center>${HtagNumber_}$number${H_tagNumber}</TD>
<TD $HbgNameCell align=left>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}">
$name
</A></TD>
$pStr2
<TD $HbgInfoCell align=right>$pop</TD>
<TD $HbgInfoCell align=right>$area</TD>
$mStr2
<TD $HbgInfoCell align=right>$foodrate</TD>
<TD $HbgInfoCell align=right>$farm</TD>
<TD $HbgInfoCell align=right>$factory</TD>
<TD $HbgInfoCell align=right>$mountain</TD>
<TD $HbgInfoCell align=right>$totalExp</TD>
</TR>
END
	}

	my @member = @{$ally->{'memberId'}};
	if(!$HarmisticeTurn && $ally->{'number'} && $HuseAmity) {
		out(<<END);
</TABLE>
<HR>
<span class='number'>◎</span>：友好(相互)　
<span class='number'>○</span>：友好　
${HtagDisaster_}Ｘ${H_tagDisaster}：交戦(宣戦布告)　
${HtagDisaster_}x${H_tagDisaster}：交戦(被宣戦布告)　
−：中立
<TABLE BORDER><TR>
<TH $HbgTitleCell>${HtagTH_}友好国設定${H_tagTH}</TH>
END

		foreach (@member) {
			$number = $HidToNumber{$_};
			$island = $Hislands[$number];
			$name = islandName($island);
			out(<<END);
<TD class='T'>$name</TD>
END
		}
		out("</TR>");
		my($i, %warFlag, $id);
		for($i=0;$i < $#HwarIsland;$i+=4){
			my($id1) = $HwarIsland[$i+1];
			my($id2) = $HwarIsland[$i+2];
			my($tn1) = $HidToNumber{$id1};
			my($tn2) = $HidToNumber{$id2};
			next if(($tn1 eq '') || ($tn2 eq ''));
			$warFlag{"$id1,$id2"} = 1;
		}
		foreach $id (@member) {
			$number = $HidToNumber{$id};
			$island = $Hislands[$number];
			$name = islandName($island);
			my($amity, %amityFlag, $aId);
			$amity = $island->{'amity'};
			foreach (@$amity) {
				$amityFlag{$_} = 1;
			}
			out("<TR><TH $HbgTitleCell>$name</TH>\n");
			foreach $aId (@member) {
				my($tAmity, %tAmityFlag);
				$tAmity = $Hislands[$HidToNumber{$aId}]->{'amity'};
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
			out("</TR>\n");
		}
	}
	out("</TABLE>");

#	if(($HallyVetoUse == 2) && !$HarmisticeTurn) {
#		my $vetoStr = (!$ally->{'vkind'}) ? '<FONT COLOR="#0000FF">拒否</FONT>' : '<FONT COLOR="#FF0000">許可</FONT>';
#		my $vetoMark = (!$ally->{'vkind'}) ? '<FONT COLOR="#0000FF">×</FONT>' : '<FONT COLOR="#FF0000">○</FONT>';
#		out(<<END);
#<HR>
#<TABLE BORDER><TR>
#<TH $HbgTitleCell>${HtagTH_}この同盟への加盟が${vetoStr}されている$AfterName${H_tagTH}</TH>
#</TR><TR>
#<TD class='C' align=left>
#END

#		my $flag = 0;
#		foreach (@{$ally->{'vetoId'}}) {
#			my $n = $HidToNumber{$_};
#			next unless(defined $n);
#			my $name = islandName($Hislands[$n]);
#			out("<span class='check'><B>$vetoMark</B>$name</span>　");
#			out("$name<BR>");
#			$flag = 1;
#		}
#		out("該当する$AfterNameはありません！") if(!$flag);
#		out("</TD></TR></TABLE>");
#	}
}

# 同盟の状況
sub allyInfo() {
	my($num) = @_;

	my %rankKind = (
		'pop' => '総人口',
		'gain' => '総獲得経験値',
		'money' => '総資金',
		'food' => '総食料',
		'area' => '総面積',
		'farm' => '総農場規模',
		'factory' => '総工場規模',
		'mountain' => '総採掘場規模',
		'monsterkill' => '総怪獣退治数',
		'itemNumber' => "総$HitemName[0]獲得数",
		'point' => "総$HpointName",
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
	my $aStr = ($HarmisticeTurn) ? '陣営' : '同盟';
	if($num == -1) {
		out(<<END);
<DIV ID='campInfo'>
<P><H1 style="display:inline;">各同盟の状況</H1>　
END
	} else {
		out("<P>");
	}

	out(<<END);
占有率は、<B>$rankKind{$HrankKind}</B>により算出されたものです。
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${aStr}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}マーク${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}の数${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}$rankKind{$HrankKind}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}占有率${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾発射${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾飛来${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦派遣${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}艦来襲${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}GNP${H_tagTH}</TH>
</TR>
END

	my $allyNumber = $HallyNumber - 1;
	foreach (0..$allyNumber) {
		next if(($num != -1) && ($_ != $HidToAllyNumber{$num}));
		my($n) = $_ + 1;
		my($ally) = $Hally[$_];
		my($score) = ($ally->{'score'} == 0) ? "なし" : "$ally->{'score'}$rankAfter{$HrankKind}";
		1 while $score =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($missileOut) = ($ally->{'ext'}[0] == 0) ? "なし" : "$ally->{'ext'}[0]発";
		1 while $missileOut =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($missileIn) = ($ally->{'ext'}[1] == 0) ? "なし" : "$ally->{'ext'}[1]発";
		1 while $missileIn =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($navyOut) = ($ally->{'ext'}[3] == 0) ? "なし" : "$ally->{'ext'}[3]艦";
		1 while $navyOut =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($navyIn) = ($ally->{'ext'}[4] == 0) ? "なし" : "$ally->{'ext'}[4]艦";
		1 while $navyIn =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my($gnp) = "$ally->{'ext'}[2]${HunitMoney}";
		1 while $gnp =~ s/(.*\d)(\d\d\d)/$1,$2/;
		my $owner = $HidToNumber{$ally->{'id'}};
		my $row = 2;
		# 称号を追加
		my($f) = 2;
		my($max) = -1;
		my($wintitle, $winmark);
		if($ally->{'ext'}[5]) {
			foreach (1..$#HwinnerTitle) {
				if($ally->{'ext'}[5] & $f) {
						$max = $_;
						$wintitle .= "\n" if($wintitle ne '');
						$wintitle .= "[${HwinnerTitle[$_]}]";
						$winmark .= "<IMG SRC=\"${HwinnerMark[$_]}\" style=\"border-width: 0px;\" TITLE=\"${HwinnerTitle[$_]}\" onMouseOver='status=\"${HwinnerTitle[$_]}\"; return true;' onMouseOut=\"status = '';\">";
				}
				$f *= 2;
			}
		}
		if($max != -1) {
			if($HviewMarkOne) {
				$winmark = "<IMG SRC=\"${HwinnerMark[$max]}\" style=\"border-width: 0px;\" TITLE=\"${wintitle}\" ";
				$wintitle =~ s/$rt//g;
				$winmark .= "onMouseOver='status=\"${wintitle}\"; return true;' onMouseOut=\"status = '';\">";
			}
			#$winmark .= '<BR>';
		}
		if(defined $owner) {
			$owner = islandName($Hislands[$owner]);
		} else {
			$row = 1;
		}
		my $name;
		if($num == -1) {
			$name = "<A style=\"text-decoration:none\" href=\"$HthisFile?AmiOfAlly=$ally->{'id'}\">$ally->{'name'}</A>";
		} else {
			$name = $ally->{'name'};
		}
		my $comment = $ally->{'comment'};
		out(<<END);
<TR>
<TD $HbgNumberCell rowspan=$row align=center>${HtagNumber_}$n${H_tagNumber}</TD>
<TD $HbgInfoCell rowspan=$row align=center>$winmark$name</TD>
<TD $HbgInfoCell align=center><B><FONT COLOR="$ally->{'color'}">$ally->{'mark'}</FONT></B></TD>
<TD $HbgInfoCell align=right>$ally->{'number'}${AfterName}</TD>
<TD $HbgInfoCell align=right>$score</TD>
<TD $HbgInfoCell align=right>$ally->{'occupation'}\%</TD>
<TD $HbgInfoCell align=right>$missileOut</TD>
<TD $HbgInfoCell align=right>$missileIn</TD>
<TD $HbgInfoCell align=right>$navyOut</TD>
<TD $HbgInfoCell align=right>$navyIn</TD>
<TD $HbgInfoCell align=right>$gnp</TD>
</TR>
END
		out(<<END) if($row == 2);
<TR>
<TD $HbgCommentCell colspan=9><A style="text-decoration:none" href="$HthisFile?Allypact=$ally->{'id'}">${owner}</A>：$comment</TD>
</TR>
END
	}

	out("</TABLE>");
	out("</DIV>") if($num == -1);
}

1;
