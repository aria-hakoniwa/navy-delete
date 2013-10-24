#!/usr/bin/perl
# ↑はサーバーに合わせて変更して下さい。

# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メンテナンスツール(ver1.01)
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
BEGIN {
	# Perl 5.004 以上が必要
	require 5.004;

########################################
	# エラー表示
	$SIG{__WARN__} = $SIG{__DIE__} =
	sub {
		my($msg) = @_;

		$msg =~ s/\n/<br>/g;
		print STDOUT <<END;
Content-type: text/html; charset=EUC-JP

<p><big><tt><b>ERROR:</b><br>$msg</tt></big></p>
END
		exit(-1);
	};
########################################
}

# 初期設定用ファイルを読み込む
require './hako-init.cgi';
require './hako-io.cgi';

# hako-mente.cgi を初めてブラウザで開くと、マスタパスワードと特殊パスワードの
# 入力を要求されます。ここで入力されたパスワードは暗号化され、パスワードファイル
# に記憶されます。

# パスワードを変更する場合は、FTP で接続してパスワードファイルを削除してください。
# その後、hako-mente.cgi をブラウザで開いてパスワードの設定を行います。
# この操作でゲームデータが壊れることはありません。ゲーム中でも変更できます。

# indexがなければ警告する？(1:する、0:しない)
$alertNoIndex = 0;
$indexName = 'index.html';
# ――――――――――――――――――――――――――――――
# 各種設定値
# ――――――――――――――――――――――――――――――
# use Time::Localが使えない環境では、'use Time::Local'の行を消して下さい。
# かわりにこのファイルの一番最後でコメントアウトしてあるTime::Local の互換関数
# sub timelocalを使って下さい。

#use Time::Local;
# ――――――――――――――――――――――――――――――
# 設定項目は以上
# ――――――――――――――――――――――――――――――
my $title   = '箱庭諸島 海戦 メンテナンスツール';

# 大きい文字
my $HtagBig_ = '<span class="big">';
my $H_tagBig = '</span>';
# ――――――――――――――――――――――――――――――
# メイン
# ――――――――――――――――――――――――――――――

# 各種変数
my($mainMode);
my($mpass1, $mpass2, $spass1, $spass2);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # マスタパスワードを読み込む
	close(PIN);
}

cookieInput();
cgiInput();
cookieOutput();

if($HskinName ne '' ){
	$baseSKIN = $HskinName;
} else {
	$baseSKIN = "${HcssDir}/$HcssDefault";
}

print <<END;
Content-type: text/html; charset=EUC-JP

<HTML>
<HEAD>
<TITLE>$title</TITLE>
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body
$Hheader
<HR>
END

if($alertNoIndex) {
	my $flag = 0;
	if(!(-e $indexName)) {
		print "${HbaseDir}に${indexName}がありません！";
		$flag = 1;
	}
#	if(!(-e "$HdirName/$indexName")) {
#		print "<BR>\n" if($flag);
#		print "${HbaseDir}/${HdirName}に${indexName}がありません！";
#		$flag = 1;
#	}
	print "<HR>\n" if($flag);
}

if($mainMode eq 'delete') {
	deleteMode() if(passCheck());
} elsif($mainMode eq 'current') {
	currentMode() if(passCheck());
} elsif($mainMode eq 'backup') {
	backupMode() if(passCheck());
} elsif($mainMode eq 'time') {
	timeMode() if(passCheck());
} elsif($mainMode eq 'stime') {
	stimeMode() if(passCheck());
} elsif($mainMode eq 'new') {
	newMode() if(passCheck());
} elsif($mainMode eq 'setup' || $mainMode eq 'changepw') {
	setupMode($modeValue) if(!$modeValue || passCheck());
} elsif($mainMode eq 'allylog') {
	allyLogMain() if(passCheck());
} elsif($mainMode eq 'dellog') {
	dellogMode() if(passCheck());
} elsif($mainMode eq 'log2html') {
	log2htmlMain() if(passCheck());
} elsif($mainMode eq 'mente') {
	menteMode() if(passCheck());
} elsif($mainMode eq 'unmente') {
	unmenteMode() if(passCheck());
}
if(($mainMode eq 'admin' || $dellcheck) && (passCheck())) {
	adminMode();
} elsif(($mainMode ne 'allylog') && ($mainMode ne 'dellog') && ($mainMode ne 'log2html')) {
	mainMode();
}

print<<"END";
</FORM></BODY></HTML>
END
exit(0);

sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	} 
	closedir(DIN);
	rmdir($dn);
}

sub currentMode {
	myrmtree "${HdirName}";
	mkdir("${HdirName}", $HdirMode);
	opendir(DIN, "${HdirName}.bak$currentID/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
	} 
	closedir(DIN);
}

sub backupMode {
	myrmtree "${HdirName}.bak$backupNo";
	mkdir("${HdirName}.bak$backupNo", $HdirMode);
	opendir(DIN, "${HdirName}/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}/$fileName", "${HdirName}.bak$backupNo/$fileName");
	} 
	closedir(DIN);
}

sub deleteMode {
	if($deleteID eq '') {
		myrmtree "${HdirName}";
	} else {
		myrmtree "${HdirName}.bak$deleteID";
	}
	unlink "hakojimalockflock";
}

sub newMode {
	mkdir($HdirName, $HdirMode);
	mkdir($HlogdirName, $HdirMode);
	mkdir($HbbsdirName, $HdirMode);

	# 現在の時間を取得
	my($now) = time();
	$now -= $now % $HunitTime if($HunitTime);

	open(OUT, ">$HdirName/$HmainData"); # ファイルを開く
	print OUT "0,1\n";  # ターン数 0,ゲームフラグ 1
	print OUT "$now\n"; # 開始時間
	print OUT "0\n";    # 島の数
	print OUT "1\n";    # 次に割り当てるID
	print OUT "\n";     # 管理人預かりの島ID
	# トーナメント用
	print OUT "0\n";          # 現在の戦闘モード
	print OUT "$HyosenTurn\n";# 切り替えターン
	print OUT "0\n";          # 何回戦目か
	print OUT "0\n";          # ターン更新数

	print OUT "\n"; # 予備
	print OUT "\n"; # 予備
	print OUT "\n"; # 予備
	print OUT "\n"; # 予備
	print OUT "\n"; # 予備
	print OUT "\n"; # 予備

	# ファイルを閉じる
	close(OUT);

	open(AOUT, ">${HdirName}/${HallyData}"); # ファイルを開く
	print AOUT "0\n";   # 同盟数 0
	close(AOUT);

	if($HoceanMode) {
		open(MOUT, ">${HdirName}/world.${HsubData}"); # ファイルを開く
		for($y = 0; $y < $HoceanSizeY*$HislandSizeY; $y++) {
			for($x = 0; $x < $HoceanSizeX*$HislandSizeX; $x++) {
				printf MOUT ("%02x%08x", 0, 0);
			}
			print MOUT "\n";
		}
		close(MOUT);
	}

}

sub setupMode {
	if (!($mpass1 && $mpass2) || ($mpass1 ne $mpass2)) {
		print "${HtagBig_}マスタパスワードが入力されていないか間違っています${H_tagBig}";
		return;
	}
	if (!($spass1 && $spass2) || ($spass1 ne $spass2)) {
		print "${HtagBig_}特殊パスワードが入力されていないか間違っています${H_tagBig}";
		return;
	}

	if (-e $HpasswordFile) {
		if(!$modeValue) {
			# セキュリティーホールのチェック
			print "${HtagBig_}すでにパスワードが設定されています${H_tagBig}";
			return;
		} else {
			unlink("$HpasswordFile");
		}
	}

	$HinputPassword = $mpass1;
	$mpass1 = crypt($mpass1, 'ma');
	$spass1 = crypt($spass1, 'sp');

	open(OUT, ">$HpasswordFile") || die $!;
	print OUT <<END;
$mpass1
$spass1
END
	close(OUT);
	$modeValue = (!$modeValue) ? '設定' : '変更';
	print "${HtagBig_}パスワードを${modeValue}しました${H_tagBig}";
}

sub timeMode {
	$ctMon--;
	$ctYear -= 1900;
	$ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
	stimeMode();
}

sub stimeMode {
	my($t) = $ctSec;
	open(IN, "${HdirName}/$HmainData");
	my(@lines);
	@lines = <IN>;
	close(IN);

	$lines[1] = "$t\n";

	open(OUT, ">${HdirName}/$HmainData");
	print OUT @lines;
	close(OUT);
}

sub mainMode {
	print <<END;
<STYLE type="text/css">
<!--
A { text-decoration:none; }
A:HOVER { text-decoration:underline; }
H1, H3, H5 { display:inline; }
H5 { color: green; }
-->
</STYLE>
<FORM action="$HmenteFile" method="POST">
<H1>$title</H1>　 [<a href="$HthisFile">$HtitleTag</a>]
<HR>
END

	unless (-e $HpasswordFile) {
		# パスワードファイルがない
		print <<END;
<H2>マスタパスワードと特殊パスワードを決めてください。</H2>
<P>※入力ミスを防ぐために、それぞれ２回ずつ入力してください。</P>
<B>マスタパスワード：</B><BR>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><BR>
<BR>
<B>特殊パスワード：</B><BR>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><BR>
<BR>
<INPUT type="submit" value="パスワードを設定する" name="SETUP">
END
		return;
	}
	$HinputPassword = $HdefaultPassword if($HinputPassword eq '');
	print <<END;
<B>マスタパスワード：</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HinputPassword">
<INPUT type="submit" value="管理人室に入る" name="ADMIN">
END

	opendir(DIN, "./");

	# 現役データ
	if(-d "${HdirName}") {
		if(-e "./mente_lock") {
			print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード解除" NAME="UNMENTE">\n#;
		} else {
			print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード" NAME="MENTE">\n#;
		}
		dataPrint("");
	} else {
		print <<END;
	<HR>
	<INPUT TYPE="submit" VALUE="新しいデータを作る" NAME="NEW">
END
	}

	# バックアップデータ
	my($dn);
#	while($dn = readdir(DIN)) {
#		if($dn =~ /^${HdirName}.bak(.*)/) {
#			dataPrint($1);
#		}
#	} 
	my(@suf);
	while($dn = readdir(DIN)) {
		if($dn =~ /^${HdirName}.bak(.*)/) {
			push(@suf, $1);
		}
	}
	foreach (sort { $a <=> $b } @suf) {
		dataPrint($_);
	}
	closedir(DIN);
}

# 管理人室
sub adminMode {
	print <<END;
<STYLE type="text/css">
<!--
A { text-decoration:none; }
A:HOVER { text-decoration:underline; }
H1, H3, H5 { display:inline; }
H5 { color: green; }
#changpw, #setupvalue, #news, #lbbslist, #exbbs, #axeslog, #centercamp, #bbsally, #bbsdead, #bbsdel, #event,
#log2html, #allymake, #allysetup, #dewarsetup, #predelete, #counter, #datachange, #mapchange, #mapsave, #viewlose, #movefleet,
#delisland, #present, #punish, #bfmake, #bfin { display:none; }
-->
</STYLE>
<script type="text/javascript">
<!--
function display(id) {
  if(document.getElementById){
    var obj = document.getElementById(id);
    if (obj.style.display == 'block'){
      obj.style.display='none';
    } else {
      obj.style.display='block';
    }
  }
}
-->
</script>
<FORM action="$HmenteFile" method="POST">
[<A href="$HmenteFile">戻る</A>]
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ADMIN value=1>
　<H1>箱庭諸島 海戦 管理人室</H1>
　 [<a href="$HthisFile">$HtitleTag</a>]
END
	print <<END;
<HR>
END
	if($Hbbs eq "${HbaseDir}/hako-yy-bbs.cgi") {
		print "[<A HREF=\"$Hbbs\" target=\"_blank\">掲示板</A>(<A HREF=\"$Hbbs?id=0&cpass=${HinputPassword}\" target=\"_blank\">管理モード</A>)] ";
	} else {
		print "[<A HREF=\"$Hbbs\" target=\"_blank\">掲示板</A>] ";
	}
	print <<END;
[<A href="$HthisFile?Amity=0" target="_blank">友好国一覧</A>] 
[<A href="$HthisFile?Fleet=1" target="_blank">艦艇保有数一覧</A>] 
[<A href="$HthisFile?Item=0" target="_blank">アイテム獲得状況</A>] 
[<A href="$HthisFile?Rekidai=0" target="_blank">歴代記録</A>] 
[<A href="$HthisFile?Rank=0" target="_blank">ランキング</A>] 
END
	if((-e "${HefileDir}/setup.html") && $sfFlag) {
		print "[<A href=\"${efileDir}/setup.html\">設定一覧</A>] ";
	} else {
		print "[<A href=\"$HthisFile?SetupV=0\">設定一覧</A>] ";
	}
	print "[<A href=\"$HthisFile?FightLog=0\" class=\"M\" TARGET=_blank>対戦の記録</A>] " if($Htournament);
	if(!$HhtmlLogMode || !(-e "${HhtmlDir}/hakolog.html") || $Hgzip) {
		print "[<A href=\"${HbaseDir}/history.cgi?Event=0\" target=\"_blank\">最近の出来事</A>] ";
	} else {
		print "[<A href=\"${htmlDir}/hakolog.html\" target=\"_blank\">最近の出来事</A>] ";
	}
	print <<END;
<HR>
<H3><span class='disaster'>※以下の作業は、更新間際に行うと非常に危険です！</span></H3>
END
	if(-e "./mente_lock") {
		print qq#　<INPUT TYPE="submit" VALUE="メンテナンスモード解除" NAME="UNMENTE">\n#;
	} else {
		print qq#　<INPUT TYPE="submit" VALUE="メンテナンスモード" NAME="MENTE">\n#;
	}
	my $exMark = '▼';
	print "<blockquote><h5>$exMark</h5>をクリックすると簡単な説明が表示されます。";
	print <<END;
</FORM>
<FORM name="CHANGEPW" action="${HmenteFile}" method=POST>
<a href="javascript: display('changpw');"><h5>$exMark</h5></a>　
<H3><a href="javascript: display('changpw');">マスタパスワード・特殊パスワードの変更</a></H3>
<DIV id='changpw'>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<P>※新しいパスワードは、入力ミスを防ぐために、それぞれ２回ずつ入力してください。</P>
<B>新しいマスタパスワード：</B><BR>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><BR>
<BR>
<B>新しい特殊パスワード：</B><BR>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><BR>
<BR>
　　　<INPUT type="submit" value="パスワードを設定する" name="CHANGEPW">
</FORM>
</DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('setupvalue');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?SetupV=${HinputPassword}" target="_blank">設定一覧(管理者用)表示</A>(<A HREF="${HthisFile}?SetupV=0" target="_blank">設定一覧を書き換える</A>)</H3>
<DIV id='setupvalue'>
<UL>
<LI>管理者用とトップページのリンクとの違いは、プレイヤーに公開しない設定も閲覧できることぐらいです。
<LI>設定を変更した時などは、htmlを書き換えておくとよいでしょう。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('news');"><h5>$exMark</h5></a>　
<H3><A HREF="hako-news.cgi?pass=${HinputPassword}" target="_blank">ニュースを書き換える</A></H3>
<DIV id='news'>
<UL>
<LI>トップページのお知らせを書き換える機能です。<br>
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('lbbslist');"><h5>$exMark</h5></a>　
<H3><A HREF="${HlbbsFile}" target="_blank">観光者通信一覧表</A></H3>
<DIV id='lbbslist'>
<UL>
<LI>lbbslist.cgiを設置している場合、全参加者の観光者通信を覗く事ができます。<br>
<LI>このスクリプトは、サーバに負荷がかかると思われる為、頻繁にアクセスしたり、リロードなどの行為はできるだけ控えるようにしましょう。
<LI>管理人モードで入ると、極秘通信を見ることができます。管理人権限だからと言ってあんまり覗いちゃダメよ。<br>注：COOKIEにマスターパスワード喰ってると「管理人モード」になります。
</UL></DIV><BR><BR>
END

	print <<END if($HuseExlbbs);
<a href="javascript: display('exbbs');"><h5>$exMark</h5></a>　
<H3><A HREF="${HlbbsDir}/view.cgi" target="_blank">外部簡易掲示板を閲覧する</A>(<A HREF="${HlbbsDir}/view.cgi?admin=${HviewPass}" target="_blank">管理人モード</A>)</H3>
<DIV id='exbbs'>
<UL>
<LI>初期設定(hako-init.cgi)で「外部簡易掲示板を使用する」ようにしていなければ、見ても仕方がありません。
<LI>view.cgiの設定でオーナーチェックをオンにしている場合、「閲覧」では投稿できないようになります。また、「index更新」のボタンを押さなければ、一覧は最新のデータにはなりません。
<LI>管理人モードでアクセスすると、各掲示板の管理人の機能が使えるようになります。（管理人としてのクッキーを食べてしまいますので、操作後の投稿には十分お気をつけ下さい）
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('axeslog');"><h5>$exMark</h5></a>　
<H3><A HREF="JavaScript:void(0)" onClick="document.AXESLOG.target='newWindow';document.AXESLOG.submit();return false;">アクセスログを見る</a></H3>
<DIV id='axeslog'>
<FORM name="AXESLOG" action="${HaxesFile}" method=POST>
<INPUT type=hidden name=password value="${HinputPassword}">
<INPUT type=hidden name=mode value="analyze">
<INPUT type=hidden name=category value="a">
</FORM>
<UL>
<LI>メインスクリプト(hako-main.cgi)の設定で「アクセスログをとる」ようにしていなければ、見ることができません。
<LI>ログを残す動作による負荷増はバカになりませんので、箱庭本体の動作にも影響があることを覚悟して下さい。
</UL></DIV><BR><BR>
END

	my $viewCommand = $HrepeatTurn * $HcampCommandTurnNumber;
	print <<END;
<FORM name="MAINCAMP" action="${HthisFile}" method="POST" target="_blank">
<a href="javascript: display('centercamp');"><h5>$exMark</h5></a>　
<H3>
<A HREF="JavaScript:void(0)" onClick="document.MAINCAMP.target='newWindow';document.MAINCAMP.submit();return false;">海戦運営本部へ</a></H3>
<INPUT type=hidden name=camp value="0">
<INPUT type=hidden name=cpass value="${HinputPassword}">
<INPUT type=hidden name=id value="0">
<DIV id='centercamp'>
</FORM>
<UL>
<LI>全島のコマンド(各島$viewCommand回分)と艦隊の状況を閲覧できます。
<LI>この機能は、サーバに負荷がかかると思われる為、頻繁にアクセスしたり、リロードなどの行為はできるだけ控えるようにしましょう。
</UL></DIV><BR><BR>
END

	my $allyList = '';
	my $deadallyList = '';
	if($HallyUse || $HarmisticeTurn) {
		if($HallyBbs) {
			readAllyFile();
			if($HallyNumber) {
				foreach (0..$#Hally) {
					my $s = '';
					$s = ' SELECTED' if(!$_);
					$allyList .= "<OPTION VALUE=\"$Hally[$_]->{'id'}\"$s>$Hally[$_]->{'name'}\n"
				}
				print <<END;
<FORM name="ALLYBBS" action="${HbaseDir}/$HallyBbsScript" method=POST>
<a href="javascript: display('bbsally');"><h5>$exMark</h5></a>　
<H3><select name=ally>${allyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.ALLYBBS.target='newWindow';document.ALLYBBS.submit();return false;">同盟掲示板へ</a></H3>
<INPUT type=hidden name=id value="0">
<INPUT type=hidden name=cpass value="${HinputPassword}">
<DIV id='bbsally'>
</FORM>
<UL>
<LI>「同盟掲示板」を閲覧できます。
<LI>投稿すると、名前が「海戦運営本部」になります。
</UL></DIV>

<FORM name="DEADBBS" action="${HmenteFile}" method=POST>
<a href="javascript: display('bbsdead');"><h5>$exMark</h5></a>　
<H3><select name=ALLYID>${allyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.DEADBBS.submit();return false;">同盟掲示板ログを消滅ログへ移行</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ALLYLOG>
<DIV id='bbsdead'>
</FORM>
<UL>
<LI>同盟の削除は上の「陣営(同盟)の作成・設定変更」で可能です。<BR>
「陣営(同盟)の作成・設定変更」の場合は、「発見の記録」に解散ログが表示されて、同盟掲示板のログはそのまま保存されます。<BR>
こちらは、同盟はそのままで、同盟掲示板のログを消滅ログへ移行させます。
<LI>消滅ログはhako-yy-bbs.cgiの上部にリンクされます。<BR>
</UL></DIV><BR><BR>
END
			}
			if(-f "${HbbsdirName}/dead${HallyData}") {
				open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
				my @dead = <DIN>;
				close(DIN);
				foreach (@dead) {
					my($dally, $daName, $diName) = split(/\,/, $_);
					my($did, $dturn) = split(/-/, $dally);
					$daName =~ s/<[^<]*>//g;
					$deadallyList .= "<OPTION VALUE=\"$dally\">$daName($HallyTopName：$diName ターン$dturnに消滅)\n"
				}
				print <<END if(@dead > 0);
<FORM name="DELBBS" action="${HmenteFile}" method=POST>
<a href="javascript: display('bbsdel');"><h5>$exMark</h5></a>　
<H3><select name=DEADALLY>${deadallyList}</select>
<A HREF="JavaScript:void(0)" onClick="document.DELBBS.submit();return false;">消滅ログの削除</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden value='消滅ログの削除' name="DELLOG">
<DIV id='bbsdel'>
</FORM>
<UL>
<LI>同盟掲示板の消滅ログを削除します。
</UL></DIV><BR><BR>
END
			}
		}
		if($Hbbs == "${HbaseDir}/hako-yy-bbs.cgi" || $allyList ne '' || $deadallyList ne '') {
				print <<END;
<FORM name="HTMLLOG" action="${HmenteFile}" method=POST>
<a href="javascript: display('log2html');"><h5>$exMark</h5></a>　
<H3><a href="javascript: display('log2html');">掲示板ログのHTML化</a></H3>
<DIV id='log2html'>
<BR>　　<select name=ALLYID><OPTION VALUE="0">海戦掲示板
${allyList}${deadallyList}</select>
　ファイル名<INPUT type=text name=HTMLNAME value="bbslog" size=8> 
親記事(1ページあたり)<INPUT type=text name=MAXLINE value="100" size=3> 
amityタグの出力<INPUT type=checkbox name=AMITY value="1" checked>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<BR><BR>　　<INPUT type=submit value='掲示板ログのHTML化' name="HTMLLOG">
<UL>
<LI>「同盟掲示板」のログを、過去ログも含めてHTML化します。
<LI>HTMLファイルは、「最近の出来事」をHTML化する設定(hako-init.cgi)と同じディリクトリに生成されます。
<UL>
<LI>『ファイル名』のところを「bbslog」にするとbbslog0000.htmlから必要なだけファイルを分割した状態で作成します。
<LI>『親記事(1ページあたり)』は、$HallyBbsScriptで設定している「最大記事数」を越えることはできません。
<LI>『amityタグの出力』のチェックをはずすと出力しません。
</UL></UL></FORM>
</DIV>
<BR><BR>
END
		}

		print <<END;
<a href="javascript: display('allymake');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?JoinA=${HinputPassword}">陣営(同盟)の作成・設定変更</A></H3>
<DIV id='allymake'>
<UL>
<LI>「陣営戦モード」を有効にしている場合は、ここから陣営(同盟)を新規作成してください。
<LI>陣営(同盟)と島を選択して変更ボタンを押すと、陣営(同盟)の参謀(盟主)を任命することができます。
</UL></DIV><BR><BR>
END
	}

	print <<END if($HuseAmity || $HallyUse || $HarmisticeTurn);
<a href="javascript: display('allysetup');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?ASetup=${HinputPassword}">友好国・同盟(陣営)の所属変更</A></H3>
<DIV id='allysetup'>
<UL>
<LI>友好国設定や同盟所属の変更を行います。
</UL></DIV><BR><BR>
END

	print <<END if($HuseDeWar);
<a href="javascript: display('dewarsetup');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?WSetup=${HinputPassword}">宣戦布告メンテナンス</A></H3>
<DIV id='dewarsetup'>
<UL>
<LI>宣戦布告のメンテナンスを行います。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('event');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Esetup=${HinputPassword}">イベントを設定する</A></H3>
<DIV id='event'>
<UL>
<LI>イベントを設定します。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('predelete');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Pdelete=${HinputPassword}">参加${AfterName}を管理人あずかりにする</A></H3>
<DIV id='predelete'>
<UL>
<LI>あずかりになった${AfterName}は、ターン処理(収入処理・コマンド処理・成長・災害・失業者移民)されなくなります。
<LI>他の${AfterName}からの攻撃も受け付けません。
<LI>コマンドの最初に「島の放棄」を入力したときだけ、処理されるようになっています。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('counter');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?ICounter=${HinputPassword}">参加${AfterName}の拡張データのカウンターを設定する</A></H3>
<DIV id='counter'>
<UL>
<LI>マップ画面下の「ターン○○〜現在」のデータ欄(カウンター)の追加・初期化・消去を行います。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('datachange');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?ISetup=${HinputPassword}">参加${AfterName}の${AfterName}データを修正する</A></H3>
<DIV id='datachange'>
<UL>
<LI>荒らしの被害や、サーバートラブル、スクリプトのバグなどで、${AfterName}データが不本意な状態になってしまった${AfterName}を救済します。
<LI>下にある「地形データ」ではなく、メインデータに関わる修正を行います。
<LI>メインデータを直接修正するよりは安全かもしれませんが、知識がなければ使用は難しいかもしれません。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('mapchange');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Lchange=${HinputPassword}">参加${AfterName}の地形データを変更する</A></H3>
<DIV id='mapchange'>
<UL>
<LI>荒らしの被害や、サーバートラブル、スクリプトのバグなどで、地形データが不本意な状態になってしまった${AfterName}を救済します。
<LI>座標１つずつの処理なので、部分的な救済措置しかできません。全体的な変更は直接データを改変した方が早いでしょう。
<LI>また、人口、農場規模などの数値データへの反映はターン更新処理が行われてからになるので、注意してください。
<LI>「地形」と「地形の値」についての知識がなければ使用は難しいかもしれません。たとえば「海」で値を１にすると「浅瀬」になったり、都市の人口の表示上の数値とデータ上の数値の違い(10000人が100と記録されていたりするので)や、農場や工場の発展規模でとりうる数値が決まっていることなど(hako-make.cgiのsub landCheckで簡易チェックをするようにしています)。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('mapsave');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?ISave=${HinputPassword}">参加${AfterName}の地形データを保存・復元する</A></H3>
<DIV id='mapsave'>
<UL>
<LI>トーナメントモードの不戦勝処理の流用です。
<LI>島全体の地形データと資金・食料を保存・復元することができます。
<LI>トーナメントモードでは戦闘期間に入る時に、セーブデータが上書きされます。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('viewlose');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?ViewLose=${HinputPassword}">保存データ一覧(復元・削除)</A></H3>
<DIV id='viewlose'>
<UL>
<LI>「敗者の${AfterName}一覧」ではトーナメントモードの敗者となった${AfterName}の沈没時に保存されたデータを見ることかできます。
<LI>「敗者の${AfterName}」は，トーナメント以外でも死滅処理の際にデータを保存するように設定できます(init-game.cgiの\$HdeadToSaveAsLose)。
<LI>「保存データ一覧」では「参加${AfterName}の地形データを保存・復元する」で保存されたデータを見ることかできます。
<LI>データは地形だけでなく島の基本データすべてが保存されています。
<LI>島を選んで「復元」すると，生存している島についてはデータの書き換え，死滅している島については戦線復帰となります。
<LI>生存している島の判定は，ID，島名，オーナー名，パスワードの４つのデータすべてが一致するかどうかです。ひとつでも違う場合，新規にIDを割り当てて戦線復帰します。
</UL>
</DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('movefleet');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Mfleet=${HinputPassword}">艦隊を強制的に移動させる</A></H3>
<DIV id='movefleet'>
<UL>
<LI>特定の島にある艦隊を別の島へ移動させます。
<LI>座標指定はできません。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('delisland');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Rename=0" target="_blank">参加${AfterName}を強制削除する</A></H3>
<DIV id='delisland'>
<UL>
<LI>「${AfterName}の名前とパスワードの変更」画面で、該当の${AfterName}の名前を「無人」${AfterName}または「沈没」${AfterName}にしてください。
<LI>その際、パスワード欄には「特殊パスワード」を入力しなければなりません。
<LI>「無人」${AfterName}にすると「発見の記録」に、「海神の<B>怒りに触れ</B>陸地はすべて<span class='disaster'>沈没しました。</span>」というログが残ります。
<LI>「沈没」${AfterName}の場合はログを出しません。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('present');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Present=">参加${AfterName}にプレゼントを贈る</A></H3>
<DIV id='present'>
<UL>
<LI>「発見の記録」にログが残るイベントとして援助を行うことができます。
<LI>表示されたフォームに必要な値やメッセージを入力して、パスワードに「特殊パスワード」を入れ、「プレゼントを贈る」ボタンを押せばプレゼント完了です。
<LI>ログにはHTMLタグも使えますが、間違ったログの削除ができませんので、慎重に入力してください。あらかじめブラウザで表示テストを行っておいたほうがいいでしょう。「発見の記録」に変なログが残ると、ちょっと恥ずかしいです。
<LI>プレゼントの結果として金や食料の保有量が制限値を超えることがあります。次回のターン進行で制限値に切り捨てられますが、そのターンだけは持っているだけ使えます。
例えば保有量が20000になっている場合、このままターン進行すると9999に切り捨てられます。しかし、このターンで掘削を99回行った場合には、費用19800が引かれて200だけが残ります。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('punish');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Punish=${HinputPassword}">参加${AfterName}に制裁を加える</A></H3>
<DIV id='punish'>
<UL>
<LI>制裁は指定した自然災害を必ず発生させます。例えば「Ａ${AfterName}に地盤沈下」という指示を出すと次のターンで地盤沈下します。
<LI>巨大隕石と噴火は座標指定が可能で、必ずその座標に発生します。どうしようもないプレイヤーを排除するときに効果的に使えます。
<LI>この改造は、「荒らしというほどではないが箱庭の雰囲気を悪化させるような行為をするプレイヤー」や、「管理人の決めたローカルルールに違反していて改善の見込みがないプレイヤー」など、箱庭の運営上好ましくないと判断されたプレイヤーに自然災害を恣意的に発生させるものです。
<LI>管理人が好ましくないと判断したプレイヤーとは掲示板などで話し合うべきですが、時には、そうした話し合いでは全く埒があかないこともあります。そういう場合、参加${AfterName}の間で「あの${AfterName}を潰そう」という機運が盛り上がったりしますが、後味はかなり悪いです。
<LI>管理人によっては「あの${AfterName}は荒らしと認定しますので攻撃してください」と全${AfterName}攻撃を認めることもあるようですが、なかなかそこまでの対応は難しいものです。強制的に${AfterName}を放棄させる処置はまだ穏便ですが、放棄された${AfterName}のプレイヤーがあとあとまで抗議してくることもあります。
<LI>そういうときに、「実にいい位置に巨大隕石」とか「運悪く地盤沈下」とかがあれば、あまり揉めずに問題${AfterName}は弱体化します。やりすぎると箱庭の雰囲気が悪くなりますので注意が必要です。
</UL></DIV><BR><BR>
END

	print <<END;
<a href="javascript: display('bfmake');"><h5>$exMark</h5></a>　
<H3><A HREF="${HthisFile}?Bfield=${HinputPassword}">Battle Fieldを作成する</A></H3>
<DIV id='bfmake'>
<UL>
<LI>人口０になっても沈没しない${AfterName}を作成します。いわば「演習${AfterName}」ですが、経験値や難民稼ぎにはなります(平和系向き)。
<LI>あらかじめ「新しい${AfterName}を探す」によって${AfterName}を作成しておかなければなりませんので、最大登録数を越えた状態の場合は一時的にそれを変更して増やしておかなければならないでしょう。面倒ですが、今のところ仕様です。
<LI>荒らしの${AfterName}や重複登録の${AfterName}をBattle Fieldに変更することもできますね。
<LI>また、Battle Fieldにしている${AfterName}を元に戻すこともできますが、${AfterName}の登録数が最大の場合はできません。
<LI><B>Battle Fieldの仕様</B>
<UL>
<LI>農場がなくても食料不足にはならない。
<LI>荒れ地はかなり高確率で平地になり、平地は森や都市に接していなくても村が発生する。
<LI>怪獣出現確率は通常の２倍で、人口にかかわらず常にレベル２。
<LI>怪獣を倒した時の報奨金は、倒した島のものになる。
</UL>
</UL></DIV><BR><BR>
END

	print <<END;
<FORM name="BFDEVELOP" action="${HthisFile}" method=POST>
<a href="javascript: display('bfin');"><h5>$exMark</h5></a>　
<H3><a href="JavaScript:void(0)" onClick="document.BFDEVELOP.target='newWindow';document.BFDEVELOP.submit();return false;">Battle Fieldの開発画面に入る</a></H3>
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=dummy value="dummy">
<DIV id='bfin'>
</FORM>
<UL>
<LI>トップページの島リストでBattle Fieldが選べるようになります。
<LI>Battle Fieldを作成していなければ、ごく普通のトップページが表示されるだけです。
</UL></DIV><BR><BR>
END

	print "</blockquote>";
}

# 同盟掲示板ログを消滅ログへ移行
sub allyLogMain {
	# 島データの読みこみ
	if(!readIslandsFile()) {
		print "データ読み込みエラー発生！<HR>";
		return;
	}
	my $an = $HidToAllyNumber{$HallyID};
	if(defined $an) {
		my $n = $HidToNumber{$HallyID};
		my $name = $Hislands[$n]->{'name'} . $AfterName;
		$name = "${HallyTopName}不在" if !(defined $n);
		if($dellcheck) {
			if(make_pastlog($HallyID, $name)) {
				print "移行成功！　<a href='${HbaseDir}/hako-yy-bbs.cgi'>掲示板へ</a><HR>";
			} else {
				print "掲示板ログがみつからない。または、移行失敗！<HR>";
			}
		} else {
			my $allyName = $Hally[$an]->{'name'};
			print <<END;
<H2>$allyNameの同盟掲示板ログを消滅ログへ移行しますか？</H2>
<H2><FORM name="DEADBBS" action="${HmenteFile}" method=POST>
<INPUT type=hidden name=DELLOK value="1">
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden name=ALLYID value="${HallyID}">
<INPUT type=hidden name=ALLYLOG>
<a href="JavaScript:void(0)" onClick="document.DEADBBS.submit();return false;">はい</a>　<a href="${HmenteFile}?ADMIN=${HinputPassword}">いいえ</a></H2>
END
		}
		return;
	} else {
		print "同盟がみつかりません！<HR>";
		$dellcheck = 1;
	}
	return;
}

# 同盟掲示板ログのHTML化
sub log2htmlMain {
	# 島データの読みこみ
	if(!readIslandsFile()) {
		print "データ読み込みエラー発生！<HR>";
		return;
	}
	my $an = $HidToAllyNumber{$HallyID};
	my $allyName = $Hally[$an]->{'name'};
	if(!(defined $an)) {
		if($HallyID eq '0') {
			$allyName = '海戦掲示板';
			$HallyID = '';
		} else {
			open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
			my @dead = <DIN>;
			close(DIN);
			foreach (@dead) {
				my($dally, $daName, $diName) = split(/\,/, $_);
				next if($dally ne $HallyID);
				my($did, $dturn) = split(/-/, $dally);
				$allyName = "$daName($HallyTopName：$diName ターン$dturnに消滅)";
				last;
			}
		}
	}
	my $amitycheck = ('しない', 'する')[$Hamity];
	print <<END;
<H3>「$allyName」の同盟掲示板ログをHTML化しますか？</H3>
ファイル名:${HhtmlName}0000.html〜
<BR>親記事の数(1ページあたり):$HmaxLine
<BR>amityタグの出力:$amitycheck
<FORM name="HTMLLOG" action="${HbaseDir}/$HallyBbsScript" method=POST>
<INPUT type=hidden name=ally value="$HallyID">
<INPUT type=hidden name=htmlname value="$HhtmlName"> 
<INPUT type=hidden name=maxline value="$HmaxLine"> 
<INPUT type=hidden name=amity value="$Hamity">
<INPUT type=hidden name=id value="0">
<INPUT type=hidden name=mode value="html">
<INPUT type=hidden name=cpass value="${HinputPassword}">
</FORM>
<H2><a href="JavaScript:void(0)" onClick="document.HTMLLOG.submit();return false;">はい</a>　<a href="${HmenteFile}?ADMIN=${HinputPassword}">いいえ</a></H2>
END
	return;
}

# 消滅ログ削除
sub dellogMode {
	if($dellcheck) {
		my $logfile = "${HbbsdirName}/${deadally}$Hlogfile_name";
		unlink($logfile) if (-f $logfile);
		# 盟主ログファイル
		my $logfile2 = "${HbbsdirName}/${deadally}$Hlogfile2_name";
		unlink($logfile2) if (-f $logfile2);
		# カウンタファイル
		if($Hcounter) {
			my $cntfile = "${HbbsdirName}/${deadally}$Hcntfile_name";
			unlink($cntfile) if (-f $cntfile);
		}
		# 過去ログ用NOファイル
		if($Hpastkey) {
			my $nofile  = "${HbbsdirName}/${deadally}$Hnofile_name";
			my $count;
			if (-f $nofile) {
				# 過去NOを開く
				open(NO,"$nofile") || die $!;
				$count = <NO>;
				close(NO);
			}
			unlink($nofile);
			foreach (1..$count) {
				my $pastfile = sprintf("%s/%04d\.%s\.cgi", $HpastdirName,$_,$deadally);
				unlink($pastfile) if (-f $pastfile);
			}
		}
		open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
		my @dead = <DIN>;
		close(DIN);
		open(DOUT, ">${HbbsdirName}/dead${HallyData}") || die $!;
		foreach (@dead) {
			my($dally, $daName, $diName) = split(/\,/, $_);
			next if($dally eq $deadally);
			print DOUT $_;
		}
		close(DOUT);
	} else {
		open(DIN, "${HbbsdirName}/dead${HallyData}") || die $!;
		my @dead = <DIN>;
		close(DIN);
		my $deadallyList;
		foreach (@dead) {
			my($dally, $daName, $diName) = split(/\,/, $_);
			my($did, $dturn) = split(/-/, $dally);
			$deadallyList = "$daName($HallyTopName：$diName ターン$dturnに消滅)\n";
			last if($dally eq $deadally);
			$deadallyList = '';
		}
		if($deadallyList eq '') {
			$dellcheck = 1;
			return;
		}
		
		print <<END if(@dead > 0);
<H2>$deadallyListの消滅ログを削除しますか？</H2>
<H2><FORM name="DELBBS" action="${HmenteFile}" method=POST>
<INPUT type=hidden name=DELLOK value="1">
<INPUT type=hidden name=DEADALLY value="${deadally}">
<INPUT type=hidden name=PASSWORD value="${HinputPassword}">
<INPUT type=hidden value='消滅ログの削除' name="DELLOG">
<a href="JavaScript:void(0)" onClick="document.DELBBS.submit();return false;">はい</a>　<a href="${HmenteFile}?ADMIN=${HinputPassword}">いいえ</a></H2>
END
	}
	return;
}

# 表示モード
sub dataPrint {
	my($suf) = @_;

	print "<HR>";
	if($suf eq "") {
		open(IN, "${HdirName}/$HmainData");
		print "<H1>現役データ</H1>";
	} else {
		open(IN, "${HdirName}.bak$suf/$HmainData");
		print "<H1>バックアップ$suf</H1>";
	}

	my($lastTurn, $playNow);
	my $tmp = <IN>;
	chomp($tmp);
	($lastTurn, $playNow) = split(/,/, $tmp); # ターン数, ゲーム中フラグ
	if($playNow) {
		$playNow = '';
	} else {
		$playNow = '(ゲーム終了)';
	}
	my($lastTime);
	$lastTime = <IN>;

	my($timeString) = timeToString($lastTime);

	print <<END;
	　<H3>[ターン $lastTurn]</H5>$playNow<BR>
	<B>最終更新時間</B>：$timeString<BR>
	<B>最終更新時間(秒数表示)</B>：1970年1月1日から$lastTime 秒<BR>
	<INPUT TYPE="submit" VALUE="このデータを削除" NAME="DELETE$suf">
END

	if($suf eq "") {
		my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = gmtime($lastTime + $Hjst);
		$mon++;
		$year += 1900;

		print <<END;
	<INPUT TYPE="submit" VALUE="このデータをバックアップ" NAME="BACKUP">
	バックアップ No.<SELECT NAME="BUNO"><OPTION VALUE="0" SELECTED>0
END
	foreach (1..99) {
		print "<OPTION VALUE=\"$_\">$_\n";
	}

		print <<END;
	</SELECT>
	<H2>最終更新時間の変更</H2>
	<INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">年
	<INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">月
	<INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">日
	<INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">時
	<INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">分
	<INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">秒
	<INPUT TYPE="submit" VALUE="変更" NAME="NTIME"><BR>
	1970年1月1日から<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">秒
	<INPUT TYPE="submit" VALUE="秒指定で変更" NAME="STIME">
END
	} else {
		print <<END;
	<INPUT TYPE="submit" VALUE="このデータを現役に" NAME="CURRENT$suf">
END
	}
}

# CGIの読みこみ
sub cgiInput {
	my($line);

	# 入力を受け取る
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	if($line =~ /DELETE([0-9]*)/) {
		$mainMode = 'delete';
		$deleteID = $1;
	} elsif($line =~ /CURRENT([0-9]*)/) {
		$mainMode = 'current';
		$currentID = $1;
	} elsif($line =~ /BACKUP/) {
		$mainMode = 'backup';
		if($line =~ /BUNO=([0-9]*)/) {
			$backupNo = $1;
		} else {
			$backupNo = 0;
		}
	} elsif($line =~ /NEW/) {
		$mainMode = 'new';
	} elsif($line =~ /UNMENTE/) {
		$mainMode = 'unmente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /MENTE/) {
		$mainMode = 'mente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /ALLYLOG/) {
		$mainMode = 'allylog';
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		if($line =~ /DELLOK=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /DELLOG/) {
		$mainMode = 'dellog';
		$line =~ /DEADALLY=([0-9]*\-[0-9]*)\&/;
		$deadally = $1;
		if($line =~ /DELLOK=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /HTMLLOG/) {
		$mainMode = 'log2html';
		if($line =~ /ALLYID=([0-9\-]*)\&/) {
			$HallyID = $1;
		}
		if($line =~ /HTMLNAME=([^\&]*)\&/) {
			$HhtmlName = $1;
		}
		if($line =~ /MAXLINE=([0-9]*)\&/) {
			$HmaxLine = $1;
		}
		if($line =~ /AMITY=([0-9])/) {
			$Hamity = $1;
		}
	} elsif($line =~ /ADMIN/) {
		$mainMode = 'admin';
	} elsif($getLine =~ /ADMIN=([^\&]*)/) {
		$mainMode = 'admin';
		$HinputPassword = htmlEscape($1);
	} elsif($line =~ /SETUP/ || $line =~ /CHANGEPW/) {
		$mainMode = 'setup';
		$modeValue = ($line =~ /CHANGEPW/) ? 1 : 0;
		if($line =~ /MPASS1=([^\&]*)\&/) {
			$mpass1 = htmlEscape($1);
		}
		if($line =~ /MPASS2=([^\&]*)\&/) {
			$mpass2 = htmlEscape($1);
		}
		if($line =~ /SPASS1=([^\&]*)\&/) {
			$spass1 = htmlEscape($1);
		}
		if($line =~ /SPASS2=([^\&]*)\&/) {
			$spass2 = htmlEscape($1);
		}
	} elsif($line =~ /NTIME/) {
		$mainMode = 'time';
		if($line =~ /YEAR=([0-9]*)/) {
			$ctYear = $1; 
		}
		if($line =~ /MON=([0-9]*)/) {
			$ctMon = $1; 
		}
		if($line =~ /DATE=([0-9]*)/) {
			$ctDate = $1; 
		}
		if($line =~ /HOUR=([0-9]*)/) {
			$ctHour = $1; 
		}
		if($line =~ /MIN=([0-9]*)/) {
			$ctMin = $1; 
		}
		if($line =~ /NSEC=([0-9]*)/) {
			$ctSec = $1; 
		}
	} elsif($line =~ /STIME/) {
		$mainMode = 'stime';
		$ctSec = $1 if($line =~ /SSEC=([0-9]*)/);
	} elsif($line =~ /TOURNAMENTTIME/) {
		$mainMode = 'tournamenttime';
	}

	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = htmlEscape($1);
	}
	if(checkMasterPassword($HinputPassword)) {
		$HcurrentID = 0;
		$defaultID = 0;
	}
}

# ファイルのコピー
sub fileCopy {
	my($src, $dist) = @_;
	open(IN, $src);
	open(OUT, ">$dist");
	while(<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);
}

# パスチェック
sub passCheck {
	if(checkMasterPassword($HinputPassword)) {
		return 1;
	} else {
		tempWrongPassword(); # パスワード違い
		print<<"END";
</BODY></HTML>
END
		exit(0);
	}
}

# メンテナンスモード
sub menteMode {
    mkdir("./mente_lock", $HdirMode);
}

# メンテモード解除
sub unmenteMode {
	rmdir("./mente_lock");
}

# Time::Local の互換関数
sub timelocal {
	my($sec, $min, $hour, $day, $mon, $year) = @_;

	$year += 1900;
	$mon++;
	if ($mon <= 2) { $mon += 12; $year--; }

	my $days = $year * 365 + int($year / 4) - int($year / 100) + int($year / 400)
	+ $mon * 30 + int(($mon + 1) * 3 / 5) + $day - 33 - 719528; # 719528 = 1970/1/1

	return (($days * 24 + $hour) * 60 + $min) * 60 + $sec - $Hjst;
}

1;
