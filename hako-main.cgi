#!/usr/bin/perl
# ↑はサーバーに合わせて変更して下さい。
# perl5用です。

# 海戦 JS.(based on ver1.3) patchworked by neo_otacky
# The Return of Neptune: http://no-one.s53.xrea.com/
# 改造時に非表示にしてもかまいませんが、できれば変更はしないでください。
my $versionInfo = "version7.15"; # JS版オリジナルのバージョン。
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メインスクリプト(ver1.02)
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

# 初期設定用ファイルを読み込む(requireの順序を変えてはいけません！)
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#----------------------------------------------------------------------
# 以下、好みによって設定する部分
#----------------------------------------------------------------------
# 異常終了基準時間
# (ロック後何秒で、強制解除するか)
my($unlockTime) = 120;

#----------------------------------------------------------------------
# 好みによって設定する部分は以上
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 変数
#----------------------------------------------------------------------
# COOKIE
# $defaultID;     # 島の名前
# $defaultTarget; # ターゲットの名前

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------
# アクセス制限
my $host = $ENV{'REMOTE_HOST'};
my $addr = $ENV{'REMOTE_ADDR'};
if ($gethostbyaddr && (($host eq '') || ($host eq $addr))) {
	$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
}
if($host eq '') {
	$host = $addr;
}
my $flag = 0;
foreach (@Hdeny) {
	if (!$_) { next; }
	s/\*/\.\*/g;
	if ($host =~ /$_/i || $addr =~ /$_/i) { $flag=1; last; }
}
if ($flag) {
	if($HdenyLocation ne '') {
		print "Location: $HdenyLocation\n\n";
		exit;
	} else {
		tempHeader();
		tempWrong("アクセスを許可されていません");
		tempFooter();
		exit(0);
	}
}

# 「戻る」リンク
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}トップへ戻る${H_tagBig}</A>";

my $agent=$ENV{'HTTP_USER_AGENT'};
if($agent =~ /(DoCoMo|J-PHONE|UP\.Browser|DDIPOCKET|ASTEL|PDXGW)/i) {
   # 携帯端末
   $Hmobile = 1;
}

# ロックをかける
if(!hakolock()) {
	# ロック失敗
	# ヘッダ出力
	tempHeader();

	# ロック失敗メッセージ
	tempLockFail();

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}

# 乱数の初期化
srand(time() ^ ($$ + ($$ << 15)));

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # マスタパスワードを読み込む
	chomp($HspecialPassword = <PIN>); # 特殊パスワードを読み込む
	close(PIN);
} else {
	unlock();
	tempHeader();
	tempNoHpasswordFile();
	tempFooter();
	exit(0);
}

# COOKIE読みこみ
cookieInput();
$HchipSize = 16 if(!$HchipSize);

# CGI読みこみ
cgiInput();

# メンテモード
if(-e "./mente_lock") {
	if(!checkSpecialPassword($HdefaultPassword) && !checkSpecialPassword($HcampPassword)) {
		unlock();
		mente_mode()
	}
}

# 島データの読みこみ
if(!readIslandsFile($HcurrentID)) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

if($Hmobile) {
	require('hako-mobile.cgi');
	exit(0);
}

# サバイバルモード ターン消費判定
if($HsurvivalTurn && ($HislandTurn >= $HsurvivalTurn)){
	foreach (
			$HcomReclaim,$HcomDestroy,$HcomPlant,$HcomFarm,$HcomFactory,$HcomMountain,
			$HcomMonument,$HcomDbase,$HcomBase,$HcomSbase,$HcomBouha,$HcomSeaMine,
			$HcomNavyWreckRepair,$HcomNavyWreckSell,@HcomNavy #,$HcomHaribote # ターン消費用にハリボテ(^^;
		) {
		$HcomTurn[$_] = 0;
	}
}

# COOKIEによるIDチェック
if($HmainMode eq 'owner') {
	unless($ENV{'HTTP_COOKIE'}) {
		cookieOutput(); # COOKIEが削除されたかどうか書き込みチェック
		next if($ENV{'HTTP_COOKIE'}); # 書き込みOK
		# クッキーを有効にしていない
		axeslog(1, 'cookie invalid') if($HtopAxes && $HtopAxes != 3);
		unlock();
		tempHeader();
		tempWrong("cookieを有効にしていますか？<BR>もう一度やり直してみて下さい。");
		tempFooter();
		exit(0);
	}
	my($pcheck) = checkPassword($Hislands[$HidToNumber{$HcurrentID}],$HinputPassword);
	if(!$pcheck) {
		unlock();
		tempHeader();
		tempWrongPassword(); # パスワード違い
		tempFooter();
		exit(0);
	}
	if($checkID || $checkImg) {
		# idから島を取得
		my $free = 0;
		foreach (@freepass){
			$free += 1 if(($_ == $defaultID) || ($_ == $HcurrentID));
		}
		my($icheck) = !($checkID && ($HcurrentID != $defaultID) && $defaultID);
		my($lcheck) = !($checkImg && ($HimgLine eq '' || $HimgLine eq $HimageDir));
		# パスワード
		if(($pcheck != 2) && ($free != 2) && ((!$icheck && !$Hcodevelope) || !$lcheck)) {
			# １つの島を初心者用に解放する時などは ($free != 2) の部分を !$free に変更して下さい。
			unlock();
			tempHeader();
			if(!$icheck) {
				axeslog(1, 'ID error!') if($HtopAxes && $HtopAxes != 3);
				tempWrong("自分の島以外には入れません！"); # ID違い
			} else {
				axeslog(1, 'image invalid') if($HtopAxes && $HtopAxes != 3);
				tempWrong("「画像のローカル設定」をして下さい。"); # ローカル設定していない
			}
			tempFooter();
			exit(0);
		}
	}
	# アクセス・ログ
	if($HtopAxes && ($HcurrentID != $defaultID)) {
		axeslog(1, 'ID differ!');
	} elsif(($HtopAxes == 2) || ($HtopAxes > 3)) {
		axeslog(1);
	}

# テンプレートを初期化
	tempInitialize(1);
} elsif(!checkMasterPassword($HinputPassword) && (($HmainMode eq '') || ($HmainMode eq 'top'))) {
	tempInitialize(0);
} else {
	tempInitialize(1);
}

# COOKIE出力
cookieOutput() if($HmainMode ne 'setupv');

# ヘッダ出力
if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
	$HmainMode eq 'commandJava' ||                       # コマンド入力モード
	$HmainMode eq 'command2' ||                          # コマンド入力モード（ver1.1より追加・自動系用）
	$HmainMode eq 'comment' && $HjavaMode eq 'java' ||   # コメント入力モード
	$HmainMode eq 'fleetname' && $HjavaMode eq 'java' || # 艦隊名変更モード
	$HmainMode eq 'priority' && $HjavaMode eq 'java' ||  # 索敵順変更モード
	$HmainMode eq 'earth' && $HjavaMode eq 'java' ||     # 周辺表示設定モード
	$HmainMode eq 'comflag' && $HjavaMode eq 'java' ||   # コマンド実行設定モード
	$HmainMode eq 'preab' && $HjavaMode eq 'java' ||     # 陣営共同開発モード
	$HmainMode eq 'lbbs' && $HjavaMode eq 'java') {      # コメント入力モード

	$Body = $BodyJs;
	require('./hako-map.cgi');
	# ヘッダ出力
	tempHeaderJava();
	if($HmainMode eq 'commandJava') {
		# 開発モード
		commandJavaMain();
	} elsif($HmainMode eq 'command2') {
		# 開発モード２（自動系コマンド用（ver1.1より追加・自動系用））
		commandMain();
	} elsif($HmainMode eq 'comment') {
		# コメント入力モード
		commentMain();
	} elsif($HmainMode eq 'fleetname') {
		# 艦艇名変更モード
		fleetnameMain();
	} elsif($HmainMode eq 'priority') {
		# 索敵順変更モード
		priorityMain();
	} elsif($HmainMode eq 'earth') {
		# 周辺表示設定モード
		earthMain();
	} elsif($HmainMode eq 'comflag') {
		# コマンド実行設定モード
		comflagMain();
	} elsif($HmainMode eq 'preab') {
		# 陣営共同開発モード
		preabMain();
	} elsif($HmainMode eq 'lbbs') {
		# ローカル掲示板モード
		require('./hako-lbbs.cgi');
		localBbsMain();
	}else{
		ownerMain();
	}
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
}elsif($HmainMode eq 'landmap'){
	require('./hako-map.cgi');
	# ヘッダ出力
	tempHeaderJava();
	# 観光モード
	printIslandJava();
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
} elsif($HmainMode ne 'lbbs' && $HmainMode ne 'new' && $HmainMode ne 'download'){
	# ヘッダ出力
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ターン進行
	require('./hako-turn.cgi');
	require('./hako-top.cgi');
	turnMain();

} elsif($HmainMode eq 'new') {
	# 島の新規作成
	require('./hako-make.cgi');
	require('./hako-map.cgi');
	newIslandMain(0);

} elsif($HmainMode eq 'newally') {
	# 同盟の新規作成
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	makeAllyMain();

} elsif($HmainMode eq 'delally') {
	# 同盟の削除
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	deleteAllyMain();

} elsif($HmainMode eq 'inoutally') {
	# 同盟の加盟・脱退
	require('./hako-make.cgi');
	require('./hako-top.cgi');
	joinAllyMain();

} elsif($HmainMode eq 'allypact') {
	# 盟主コメントモード
	require('./hako-make.cgi');
	allyPactMain();

} elsif($HmainMode eq 'print') {
	# 観光モード
	require('./hako-map.cgi');
	printIslandMain();

} elsif($HmainMode eq 'oceanmap') {
	# 海域マップモード
	require('hako-map.cgi');
	printIslandMapMain();

} elsif($HmainMode eq 'owner') {
	# 開発モード
	require('./hako-map.cgi');
	ownerMain();

} elsif($HmainMode eq 'command') {
	# コマンド入力モード
	require('./hako-map.cgi');
	commandMain();

} elsif($HmainMode eq 'comment') {
	# コメント入力モード
	require('./hako-map.cgi');
	commentMain();

} elsif($HmainMode eq 'fleetname') {
	# 艦艇名変更モード
	require('./hako-map.cgi');
	fleetnameMain();

} elsif($HmainMode eq 'priority') {
	# 索敵順変更モード
	require('./hako-map.cgi');
	priorityMain();

} elsif($HmainMode eq 'earth') {
	# 周辺表示設定モード
	require('./hako-map.cgi');
	earthMain();

} elsif($HmainMode eq 'comflag') {
	# コマンド実行設定モード
	require('./hako-map.cgi');
	comflagMain();

} elsif($HmainMode eq 'preab') {
	# 陣営共同開発モード
	require('./hako-map.cgi');
	preabMain();

} elsif($HmainMode eq 'lbbs') {
	# ローカル掲示板モード
	require('./hako-map.cgi');
	require('./hako-lbbs.cgi');
	localBbsMain();

} elsif($HmainMode eq 'change') {
	# 情報変更モード
	require('./hako-make.cgi');
	changeMain();

} elsif($HmainMode eq 'FightIsland') {
	# トーナメント 敗者の島表示
	require('hako-map.cgi');
	fightMap($HadminMode);

} elsif($HmainMode eq 'FightView') {
	# トーナメント LOGモード
	require('hako-table.cgi');
	FightViewMain();

} elsif($HmainMode eq 'TimeTable') {
	# トーナメント タイムテーブル
	require('hako-table.cgi');
	TimeTableMain();

} elsif($HmainMode eq 'camp') {
	# 陣営モード
	require('./hako-map.cgi');
	require('./hako-camp.cgi');
	campMain();

} elsif($HmainMode eq 'join') {
	# 新しい島を探す
	require('./hako-make.cgi');
	require('./hako-map.cgi');
	newIslandTop();

} elsif($HmainMode eq 'rename') {
	# 島の名前とパスワードの変更
	require('./hako-make.cgi');
	renameIslandMain();

} elsif($HmainMode eq 'joinally') {
	# 同盟設定
	require('./hako-make.cgi');
	newAllyTop();

} elsif($HmainMode eq 'localimg') {
	# 画像のローカル設定
	require('./hako-limg.cgi');
	localImgMain();

} elsif($HmainMode eq 'hakoskin') {
	# 箱庭スキンの設定
	require('./hako-skin.cgi');
	hakoSkinMain();

} elsif($HmainMode eq 'rank') {
	# ランキング
	require('./hako-rank.cgi');
	rankIslandMain();

} elsif($HmainMode eq 'rekidai') {
	# 歴代記録
	require('./hako-reki.cgi');
	rankingReki();

} elsif($HmainMode eq 'aoa') {
	# 同盟内の友好国設定
	require('./hako-top.cgi');
	amityOfAlly();

} elsif($HmainMode eq 'amity') {
	# 友好国設定一覧
	require('./hako-table.cgi');
	amityInfo();

} elsif($HmainMode eq 'item') {
	# アイテム獲得状況
	require('./hako-table.cgi');
	ItemInfo();

} elsif($HmainMode eq 'fleet') {
	# 艦艇保有状況
	require('./hako-table.cgi');
	fleetInfo();

} elsif($HmainMode eq 'mfleet') {
	# 艦隊強制移動モード
	require('./hako-admin.cgi');
	moveFleetAdmin();

} elsif($HmainMode eq 'bfield') {
	# BattleField作成モード
	require('./hako-make.cgi');
	bfieldMain();

} elsif($HmainMode eq 'esetup') {
	# イベント設定モード
	require('./hako-admin.cgi');
	setupEvent();

} elsif($HmainMode eq 'download') {
	# 保存データダウンロードモード
	require('./hako-admin.cgi');
	dataDownload($HadminMode);

} elsif($HmainMode eq 'vlose') {
	# 保存データ一覧モード
	require('./hako-admin.cgi');
	loseIslandAdminTop();

} elsif($HmainMode eq 'reload') {
	# 保存データ復元モード
	require('./hako-map.cgi');
	fightMap($HadminMode);

} elsif($HmainMode eq 'delete') {
	# 保存データ削除モード
	require('./hako-admin.cgi');
	dataDelete($HadminMode);

} elsif($HmainMode eq 'present') {
	# 管理人によるプレゼントモード
	require('./hako-admin.cgi');
	presentMain();

} elsif($HmainMode eq 'punish') {
	# 管理人による制裁モード
	require('./hako-admin.cgi');
	punishMain();

} elsif($HmainMode eq 'lchange') {
	# 管理人による地形変更モード
	require('./hako-admin.cgi');
	lchangeMain();

} elsif($HmainMode eq 'predelete') {
	# 管理人によるあずかりモード
	require('./hako-admin.cgi');
	preDeleteMain();

} elsif($HmainMode eq 'asetup') {
	# 友好国設定確認モード
	require('./hako-admin.cgi');
	amitySetupMain();

} elsif($HmainMode eq 'wsetup') {
	# 宣戦布告確認モード
	require('./hako-admin.cgi');
	dewarSetupMain();

} elsif($HmainMode eq 'isetup') {
	# 島データ修正モード
	require('./hako-make.cgi');
	islandSetupMain();

} elsif($HmainMode eq 'isave') {
	# 地形データ保存・復元モード
	require('./hako-map.cgi');
	islandSaveMain();

} elsif($HmainMode eq 'icounter') {
	# 拡張データ カウンター設定モード
	require('./hako-map.cgi');
	islandCounterMain();

} elsif($HmainMode eq 'setupv') {
	# 初期設定確認モード
	require('./hako-table.cgi');
	setupValue();

} else {
	# その他の場合はトップページモード
	require('./hako-top.cgi');
	topPageMain();
}

# フッタ出力
tempFooter();

# 終了
exit(0);

# コマンドを前にずらす
sub slideFront {
	my($command, $number) = @_;
	my($i);

	# それぞれずらす
	splice(@$command, $number, 1);

	# 最後に資金繰り
	$command->[$HcommandMax - 1] = {
		'kind' => $HcomDoNothing,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
	};
}

# コマンドを後にずらす
sub slideBack {
	my($command, $number) = @_;
	my($i);

	# それぞれずらす
	return if $number == $#$command;
	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# 入出力
#----------------------------------------------------------------------
# CGIの読みこみ
sub cgiInput {
	my($line, $getLine);

	# 入力を受け取って日本語コードをEUCに
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	jcode::convert(\$line, 'euc'); # jcode使用時
#HdebugOut("$line\n");
	if($line !~ /Allypact=([^\&]*)\&/) {
#		$line =~ s/[\x00-\x1f\,]//g;
		$line =~ s/[\x00-\x1f]//g;
		$line =~ s/\,/，/g;
	} else {
# 盟主コメントモード
# 変更ボタンが押された起動
		$HmainMode = 'allypact';
		$HdefaultPassword = htmlEscape($1);
		$line =~ /AllypactMode=([0-9]+)\&/;
		$HallyPactMode = $1 + 1;
		$line =~ /ISLANDID=([0-9]+)\&/;
		$HcurrentID = $1;
		if($HallyPactMode == 2) {
			while($line =~/VETOID=([0-9]*)\&/g) {
				push(@HvetoID, $1);
			}
			$line =~ /VETOKIND=([0-9]*)\&/;
			$HvetoKind = $1;
			$line =~ /ALLYCOMMENT=([^\&]*)\&/;
			$HallyComment = cutColumn($1, $HlengthAllyComment*2);
			$line =~ /ALLYTITLE=([^\&]*)\&/;
			$HallyTitle = cutColumn($1, $HlengthAllyTitle*2);
			$line =~ s/(.*)ALLYMESSAGE=//g;
			$HallyMessage = cutColumn($line, $HlengthAllyMessage*2);
		}
		return;
	}
	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};
#HdebugOut("$getLine\n");
	# 対象の島
	if($line =~ /ISLANDID=([0-9]+)\&/){
		$HcurrentID = $1;
	}

	# パスワード
	if($line =~ /OLDPASS=([^\&]*)\&/) {
		$HoldPassword = $HdefaultPassword = htmlEscape($1);
	}
	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = $HdefaultPassword = htmlEscape($1);
	}
	if($line =~ /PASSWORD2=([^\&]*)\&/) {
		$HinputPassword2 = htmlEscape($1);
	}

	# Ｊａｖａスクリプトモード
	if($line =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	} elsif($getLine =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}

	# 非同期通信フラグ
	if($line =~ /async=true\&/) {
		$Hasync = 1;
	}

	# main modeの取得
	if($line =~ /TurnButton/) {
		if(($Hdebug == 1)) {
			$HmainMode = 'Hdebugturn';
		}
	} elsif($getLine =~ /Top=([^\&]*)/) {
		$HtopTemplateFile = $1;
		if($HtopTemplateFile !~ /.htm/) {
			$HtopTemplateFile = '';
		}
		$HmainMode = 'top';
	} elsif($line =~ /OwnerButton/) {
		if($HcurrentID) {
			$HmainMode = 'owner';
		}
	} elsif($line =~ /CommandJavaButton([0-9]+)=/ || $line =~ /CommandJavaButtonSub([0-9]+)=/) {
		# コマンド送信ボタンの場合（Ｊａｖａスクリプト）
		$HcurrentID = $1;
		$HmainMode = 'commandJava';
		$line =~ /COMARY=([^\&]*)\&/;
		$HcommandComary = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /TARGETID2=([^\&]*)\&/;
		$HcommandTarget2 = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		# コマンドのポップアップメニューを開く？
		if($line =~ /MENUOPEN=on/) {
			$HmenuOpen = 'CHECKED';
		} elsif($line =~ /MENUOPEN2=on/) {
			$HmenuOpen2 = 'CHECKED';
		} elsif($line =~ /MENUOPEN3=on/) {
			$HmenuOpen3 = 'CHECKED';
		}
	} elsif($line =~ /CommandButton([0-9]+)=/) {
		# コマンド送信ボタンの場合
		$HcurrentID = $1;
		if($HjavaMode eq 'java'){
			$HmainMode = 'command2';
		}else{
			$HmainMode = 'command';
		}

		# コマンドモードの場合、コマンドの取得
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /TARGETID2=([^\&]*)\&/;
		$HcommandTarget2 = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		if($line =~ /COMMANDMODE=(write|insert|delete)/) {
			$HcommandMode = $1;
		}
		# コマンドのポップアップメニューを開く？
		if($line =~ /MENUOPEN=on/) {
			$HmenuOpen = 'CHECKED';
		} elsif($line =~ /MENUOPEN2=on/) {
			$HmenuOpen2 = 'CHECKED';
		} elsif($line =~ /MENUOPEN3=on/) {
			$HmenuOpen3 = 'CHECKED';
		}
	} elsif($getLine =~ /Sight=([0-9]*)/) {
		$HmainMode = 'print';
		$HcurrentID = $1;
		# 管理人モード
		if($getLine =~ /ADMINMODE=([0-9]*)/) {
			$HadminMode = 1;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		}
	} elsif($getLine =~ /OceanMap=([0-9]*)/) {
		# 海域マップの表示
		if($HuseOceanMap) {
			$HmainMode = 'oceanmap';
			$HcurrentID = $1;
		}
	} elsif($line =~ /LbbsButton(..)([0-9]*)/) {
		$HmainMode = 'lbbs';
		if($1 eq 'AD') {
			# 管理人
			$HlbbsMode = 7;
		} elsif($1 eq 'DA') {
			# 管理人削除
			$HlbbsMode = 9;
		} elsif($1 eq 'VA') {
			# 管理人閲覧数変更
			$HlbbsMode = 11;
		} elsif($1 eq 'OW') {
			# 島主
			$HlbbsMode = 1;
		} elsif($1 eq 'DL') {
			# 島主削除
			$HlbbsMode = 3;
		} elsif($1 eq 'VO') {
			# 島主閲覧数変更
			$HlbbsMode = 5;
		} elsif($1 eq 'VS') {
			# 観光者閲覧数変更
			$HlbbsMode = 6;
		} elsif($1 eq 'DS') {
			# 観光者削除
			$HlbbsMode = 2;
		} elsif($1 eq 'CK') {
			# 観光者極秘確認
			$HlbbsMode = 4;
		} else {
			# 観光者
			$HlbbsMode = 0;
			$mode = 1;
		} 
		$HcurrentID = $2;

		if($line =~ /LBBSNAME=([^\&]*)\&/) {
			$HlbbsName = cutColumn($1, $HlengthLbbsName*2);
			$HdefaultName = $HlbbsName;
		}
		if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
			my $lbbsMessage = $1;
			my $comment_length = $HlengthLbbsMessage * 2;
			if(($HlbbsAutolinkSymbol ne '') && ($lbbsMessage =~ /((http|ftp):\/\/([^\x81-\xFF\s\"\'\(\)\<\>\\\`\[\{\]\}\|]+))/ )) {
				my $matched_url = $1;
				$comment_length += length($matched_url) - 2;
			}
			$HlbbsMessage = cutColumn($lbbsMessage, $comment_length);
		}
		# 掲示板の発言島
		$line =~ /ISLANDID2=([0-9]+)\&/;
		$HspeakerID = $1;
		# 掲示板の通信形式
		$line =~ /LBBSTYPE=([^\&]*)\&/;
		$HlbbsType = $1;
		# 削除かもしれないので、番号を取得
		if($line =~ /NUMBER=([^\&]*)\&/) {
			$HcommandPlanNumber = $1;
		}
		# 閲覧数取得
		if($line =~ /LBBSVIEW=([0-9]+)\&/) {
			$HlbbsView = $1;
		}
	} elsif($line =~ /ChangeInfoButton/) {
		$HmainMode = 'change';

		# 名前指定の場合
		if($line =~ /ISLANDNAME=([^\&]*)\&/){
			$HcurrentName = htmlEscape(cutColumn($1, $HlengthIslandName*2));
		}
		# オーナー名の取得
		if($line =~ /OWNERNAME=([^\&]*)\&/){
			$HcurrentOwnerName = htmlEscape(cutColumn($1, $HlengthOwnerName*2));
		}
	} elsif($line =~ /MessageButton([0-9]*)/) {
		$HmainMode = 'comment';
		$HcurrentID = $1;
		# メッセージ
		if($line =~ /MESSAGE=([^\&]*)\&/){
			$Hmessage = cutColumn($1, $HlengthMessage*2);
		}
	} elsif($line =~ /FleetnameButton([0-9]*)/) {
		$HmainMode = 'fleetname';
		$HcurrentID = $1;
		# 艦艇名
		$line =~ /FLEET1=([^\&]*)\&FLEET2=([^\&]*)\&FLEET3=([^\&]*)\&FLEET4=([^\&]*)\&/;
		$HfleetName[0] = cutColumn($1, $HlengthFleetName*2);
		$HfleetName[1] = cutColumn($2, $HlengthFleetName*2);
		$HfleetName[2] = cutColumn($3, $HlengthFleetName*2);
		$HfleetName[3] = cutColumn($4, $HlengthFleetName*2);
	} elsif($line =~ /PriorityButton([0-9]*)/) {
		$HmainMode = 'priority';
		$HcurrentID = $1;
		# 索敵順
		$line =~ /PSF=([0-9])\&PS0=([0-9])\&PS1=([0-9])\&PS2=([0-9])\&PS3=([0-9])\&PS4=([0-9])\&PS5=([0-9])\&PS6=([0-9])\&PS7=([0-9])\&/;
		$HfleetNumber = $1;
		$HfleetPriority = "$2-$3-$4-$5-$6-$7-$8-$9";
	} elsif($line =~ /EarthButton([0-9]*)/) {
		$HmainMode = 'earth';
		$HcurrentID = $1;
	} elsif($line =~ /ComflagButton([0-9]*)/) {
		$HmainMode = 'comflag';
		$HcurrentID = $1;
	} elsif($line =~ /PreabButton([0-9]*)/) {
		$HmainMode = 'preab';
		$HcurrentID = $1;
	} elsif($getLine =~ /View=([0-9]*)/) {
		$HmainMode = 'top';
		$HviewIslandNumber = $1;
	} elsif($getLine =~ /IslandMap=([0-9]*)/) {
		$HmainMode = 'landmap';
		$HcurrentID = $1;
		if($getLine =~ /MISSILEMODE=([0-9]*)/) {
			# ミサイル着弾点
			$HmissileMode = $1;
		}
	} elsif($getLine =~ /JoinA=([^\&]*)/) {
		$HmainMode = 'joinally';
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /NewAllyButton/) {
		$HmainMode = 'newally';
		# 同盟名の取得
		if($line =~ /ALLYNUMBER=([0-9]*)\&/) {
			$HcurrentAnumber = $1;
		}
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		$line =~ /ALLYNAME=([^\&]*)\&/;
		$HallyName = htmlEscape(cutColumn($1, $HlengthAllyName*2));
		$line =~ /MARK=([^\&]*)\&/;
		$HallyMark = $1;
		$line =~ /COLOR1=([0-9A-F])\&COLOR2=([0-9A-F])\&COLOR3=([0-9A-F])\&COLOR4=([0-9A-F])\&COLOR5=([0-9A-F])\&COLOR6=([0-9A-F])\&/;
		$HallyColor = $1 . $2 . $3 . $ 4 . $5 . $6;
	} elsif($line =~ /DeleteAllyButton/) {
		$HmainMode = 'delally';
		if($line =~ /ALLYID=([0-9]*)\&/) {
			$HallyID = $1;
		}
		$line =~ /ALLYNUMBER=([0-9]*)\&/;
		$HcurrentAnumber = $1;
	} elsif($line =~ /JoinAllyButton/) {
		$HmainMode = 'inoutally';
		$line =~ /ALLYNUMBER=([0-9]*)\&/;
		$HcurrentAnumber = $1;
	} elsif($getLine =~ /AmiOfAlly=([0-9]*)/) {
		$HmainMode = 'aoa';
		$HallyID = $1;
	} elsif($getLine =~ /Allypact=([^\&]*)/) {
		# 盟主コメントモード
		# 最初の起動
		$HmainMode = 'allypact';
		$HallyPactMode = 0;
		$HcurrentID = $1;

	} elsif($getLine =~ /Amity=([0-9]*)/) {
		$HmainMode = 'amity';
	} elsif($getLine =~ /Item=([0-9]*)/) {
		$HmainMode = 'item';
		$HitemNumber = $1;
	} elsif($getLine =~ /Fleet=([0-9]*)/) {
		$HmainMode = 'fleet';
		$HinfoMode = $1;
	} elsif ($line =~ /camp=([0-9]*)/) {
		$HmainMode = 'camp';
		$HcurrentCampID = $1;
		if($line =~ /jpass=([a-zA-Z0-9]*)/) {
			$HtakayanPassword = htmlEscape($1); # 陣営パスワード
		}
		if($line =~ /cpass=([^\&]*)\&/) {
			$HcampPassword = htmlEscape($1);
		}
		if($line =~ /id=([0-9]*)/) {
			$HcurrentID = $1;
		}
	} elsif($getLine =~ /Rank=([0-9]*)/) {
		$HmainMode = 'rank';
	} elsif($getLine =~ /Rekidai=([0-9]*)/) {
		$HmainMode = 'rekidai';
	} elsif($getLine =~ /Rename=([0-9]*)/) {
		$HmainMode = 'rename';
	} elsif($getLine =~ /Limg=([0-9]*)/) {
		$HmainMode = 'localimg';
	} elsif($getLine =~ /Skin=([0-9]*)/) {
		$HmainMode = 'hakoskin';
	} elsif($getLine =~ /Join=([0-9]*)/) {
		# 誰でも新しい島を探せる
		$HmainMode = ($HadminJoinOnly ? 'top' : 'join');
	} elsif($line =~ /Join=([0-9]*)/) {
		# 管理人だけが新しい島を探せる
		$HmainMode = ($HadminJoinOnly ? 'join' : 'top');
	} elsif($line =~ /NewIslandButton/) {
		$HmainMode = 'new';
		# 名前の取得
		$line =~ /ISLANDNAME=([^\&]*)\&/;
		$HcurrentName = htmlEscape(cutColumn($1, $HlengthIslandName*2));
		# オーナー名の取得
		$line =~ /OWNERNAME=([^\&]*)\&/;
		$HcurrentOwnerName = htmlEscape(cutColumn($1, $HlengthOwnerName*2));
		if($HarmisticeTurn && $HcampSelectRule == 2) {
			# 陣営を選択可能な場合
			if($line =~ /CAMPNUMBER=([\-]?[0-9]+)\&/) {
				$HcampNumber = $1;
			}
		}
		if($HoceanMode && $HoceanSelect) {
			# 座標を選択可能な場合
			if($line =~ /OCEANX=([^\&]*)\&/) {
				$HoceanMapX = $1;
			}
			if($line =~ /OCEANY=([^\&]*)\&/) {
				$HoceanMapY = $1;
			}
			if($line =~ /RANDOM=([0-9]*)\&/) {
				$HmapRandom = $1;
			}
		}

# 初期設定確認モード
	} elsif($getLine =~ /SetupV=([^\&]*)/) {
		$HmainMode = 'setupv';
		$HdefaultPassword = htmlEscape($1);

# トーナメントモード
	} elsif($getLine =~ /LoseMap=([0-9]*)/) {
		$HmainMode = 'FightIsland';
		$HadminMode = 0;
		$HcurrentID = $1;
		if($getLine =~ /ADMINMODELOSE=([0-9]*)/) {
			$HadminMode = 2;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		} elsif($getLine =~ /ADMINMODESAVE=([0-9]*)/) {
			$HadminMode = 1;
			$HinputPassword = htmlEscape($1);
			$HdefaultPassword = $HinputPassword;
		}
	} elsif($getLine =~ /FightLog/) {
		$HmainMode = 'FightView';
	} elsif($getLine =~ /TimeTable/) {
		$HmainMode = 'TimeTable';

# 友好国設定確認モード
	} elsif($getLine =~ /ASetup=([^\&]*)/) {
		$HmainMode = 'asetup';
		$HasetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /ASetup=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'asetup';
		$HasetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		while($line =~/amity=([^\&]*)\&/g) {
			push(@HamityChange, $1);
		}
		while($line =~/ally=([^\&]*)\&/g) {
			push(@HallyChange, $1);
		}

# 宣戦布告確認モード
	} elsif($getLine =~ /WSetup=([^\&]*)/) {
		$HmainMode = 'wsetup';
		$HwsetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /WSetup=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'wsetup';
		$HwsetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		while($line =~/war=([0-9]*)\&/g) {
			push(@HdeWarChange, $1);
		}
		while($line =~/del=([0-9]*)\&/g) {
			$HdeWarDel{$1} = 1;
		}

# 島データ修正モード
	} elsif($getLine =~ /ISetup=([^\&]*)/) {
		$HmainMode = 'isetup';
		$HisetupMode = 0;
		$HdefaultPassword = htmlEscape($1);
		if($getLine =~ /id=([0-9]*)/) {
			$HcurrentID = $1;
		}
	} elsif($line =~ /ISetup=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'isetup';
		$HisetupMode = 1;
		$HdefaultPassword = htmlEscape($1);
		if($line =~ /IslandChange/) {
			$HisetupMode = 2;
			# 名前の取得
			$line =~ /ISLANDNAME=([^\&]*)\&/;
			$HcurrentName = cutColumn($1, $HlengthIslandName*2);
			# オーナー名の取得
			$line =~ /OWNERNAME=([^\&]*)\&/;
			$HcurrentOwnerName = cutColumn($1, $HlengthOwnerName*2);
			$line =~ /BIRTHDAY=([0-9]*)\&/;
			$Hbirthday = $1;
			$line =~ /ABSENT=([0-9]*)\&/;
			$Habsent = $1;
			if($line =~ /PREAB=([0-9]*)\&/) {
				$Hpreab = $1;
			}
			$line =~ /MONEY=([0-9]*)\&/;
			$Hmoney = $1;
			$line =~ /FOOD=([0-9]*)\&/;
			$Hfood = $1;
			$line =~ /GAIN=([0-9]*)\&/;
			$Hgain = $1;
			if($line =~ /FIELD=([0-9]*)\&/) {
				$Hfield = $1;
			}
			$line =~ /FIGHT_ID=([\-0-9]*)\&/;
			$Hfight_id = $1;
			$line =~ /REST=([0-9]*)\&/;
			$Hrest = $1;
			while($line =~/FLAGS=([0-9]*)\&/g) {
				push(@Hflags, $1);
			}
			while($line =~/MONSTERS=([0-9]*)\&/g) {
				push(@Hmonsters, $1);
			}
			$line =~ /MONSTERKILL=([0-9]*)\&/;
			$Hmonsterkill = $1;
			while($line =~/HMONSTERS=([0-9]*)\&/g) {
				push(@Hhmonsters, $1);
			}
			while($line =~/SINK=([0-9]*)\&/g) {
				push(@Hsink, $1);
			}
			while($line =~/SINKSELF=([0-9]*)\&/g) {
				push(@Hsinkself, $1);
			}
			while($line =~/EXT=([0-9]*)\&/g) {
				push(@Hext, $1);
			}
			while($line =~/SUBEXT=([0-9]*)\&/g) {
				push(@HsubExt, $1);
			}
			while($line =~/ITEM=([0-9]*)\&/g) {
				push(@HtmpItem, $1);
			}
			while($line =~/WEATHER=([0-9]*)\&/g) {
				push(@HtmpWeather, $1);
			}
			if($HoceanMode) {
				# 座標を選択可能な場合
				if($line =~ /OCEANX=([^\&]*)\&/) {
					$HoceanMapX = $1;
				}
				if($line =~ /OCEANY=([^\&]*)\&/) {
					$HoceanMapY = $1;
				}
				if($line =~ /RANDOM=([0-9]*)\&/) {
					$HmapRandom = $1;
				}
			}
		}

# 地形データ保存・復元モード
	} elsif($getLine =~ /ISave=([^\&]*)/) {
		$HmainMode = 'isave';
		$HisaveMode = 0;
	} elsif($line =~ /ISave=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'isave';
		$HisaveMode = 1;
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		if($line =~ /SaveButton/) {
			# 保存
			$HisaveMode = 2;
		} elsif($line =~ /LoadButton/) {
			# 復元
			$HisaveMode = 3;
		} elsif($line =~ /ChangeButton/) {
			# 保存・復元(データの入れ替え)
			$HisaveMode = 4;
		} elsif($line =~ /SaveLandButton/) {
			# 保存(海軍を除く)
			$HisaveMode = 5;
		} elsif($line =~ /LoadLandButton/) {
			# 復元(海軍を除く)
			$HisaveMode = 6;
		} elsif($line =~ /ChangeLandButton/) {
			# 保存・復元(海軍を除く)
			$HisaveMode = 7;
		}

# 保存データダウンロード
	} elsif($getLine =~ /Download=([^\&]*)\&/) {
		$HmainMode = 'download';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		$getLine =~ /mode=([0-9]*)\&/;
		$HadminMode = $1;
		$getLine =~ /id=([0-9]*)/;
		$HcurrentID = $1;

# 保存データ一覧
	} elsif($getLine =~ /ViewLose=([^\&]*)/) {
		$HmainMode = 'vlose';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
	} elsif($line =~ /Reload=([^\&]*)/) { # 復元ボタン押下
		$HmainMode = 'vlose';
		$HinputPassword = htmlEscape($1);
		$HdefaultPassword = $HinputPassword;
		if($line =~ /ReloadButton/) {
			if($line =~ /RELOADIDLOSE=([0-9]*)/) {
				$HmainMode = 'reload';
				$HadminMode = 4;
				$HcurrentID = $1;
			} elsif($line =~ /RELOADIDSAVE=([0-9]*)/) {
				$HmainMode = 'reload';
				$HadminMode = 3;
				$HcurrentID = $1;
			}
		} elsif($line =~ /DeleteButton/) {
			while($line =~/DELETEIDLOSE=([0-9]*)\&/g) {
				push(@HloseID, $1);
				$HadminMode |= 2;
			}
			while($line =~/DELETEIDSAVE=([0-9]*)\&/g) {
				push(@HsaveID, $1);
				$HadminMode |= 1;
			}
			$HmainMode = 'delete' if($HadminMode);
		}

# 拡張データ カウンター設定モード
	} elsif($getLine =~ /ICounter=([^\&]*)/) {
		my $tmp = $1; 
		$HdefaultPassword = htmlEscape($tmp) if($tmp ne '0');
		$HmainMode = 'icounter';
		$HicounterMode = 0;
	} elsif($line =~ /ICounter=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'icounter';
		$HicounterMode = 1;
		$HinputPassword = $HdefaultPassword = htmlEscape($1);
		if($line =~ /AllSetButton/) {
			$HicounterMode = 4;
		} elsif($line =~ /SetButton/) {
			$HicounterMode = 2;
		} elsif($line =~ /AllDelButton/) {
			$HicounterMode = 5;
		} elsif($line =~ /DelButton/) {
			$HicounterMode = 3;
		}

# 艦隊強制移動モード
	} elsif($getLine =~ /Mfleet=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'mfleet';
		$HmfleetMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Mfleet=([^\&]*)\&/) {
		# 艦隊強制移動ボタンが押された起動
		$HmainMode = 'mfleet';
		$HmfleetMode = 1;
		$HdefaultPassword = htmlEscape($1);
		$line =~ /FROMID=([0-9]*)\&/;
		$HfromID = $1;
		$line =~ /TOID=([0-9]*)\&/;
		$HtoID = $1;
		$line =~ /FLEETNUMBER=([0-4])\&/;
		$HfleetNo = $1;

# イベント設定モード
	} elsif($getLine =~ /Esetup=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'esetup';
		$HsetEventMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Esetup=([^\&]*)\&/) {
		# イベント設定ボタンが押された起動
		$HmainMode = 'esetup';
		$HdefaultPassword = htmlEscape($1);
		if($line =~ /SetEventButton/) {
			$HsetEventMode = 1;
			$line =~ /START=([0-9]*)\&/;
			$Hstart = $1;
			$line =~ /TURM=([0-9]*)\&/;
			$Hturm = $1;
			$line =~ /MAXSHIP=([0-9]*)\&/;
			$Hmaxship = $1;
			while($line =~/KIND=([0-9]*)\&/g) {
				$HpermitKind |= (2 ** $1);
			}
			$line =~ /ADDITION=([0-9]*)\&/;
			$Haddition = $1;
			while($line =~/RESTRICTION=([0-9]*)\&/g) {
				$Hrestriction |= (2 ** $1);
			}
			$line =~ /TYPE=([0-9]*)\&/;
			$Htype = $1;
			$line =~ /AUTORETURN=([0-9]*)\&/;
			$HautoReturn = $1;
			$line =~ /MONSTERTURN=([0-9]*)\&/;
			$HmonsterTurn = $1;
			$line =~ /MONSTERNUMBER=([0-9]*)\&/;
			$HmonsterNumber = $1;
			$line =~ /HUGEMONSTERTURN=([0-9]*)\&/;
			$HhugeMonsterTurn = $1;
			$line =~ /HUGEMONSTERNUMBER=([0-9]*)\&/;
			$HhugeMonsterNumber = $1;
			$line =~ /UNKNOWNTURN=([0-9]*)\&/;
			$HunkownTurn = $1;
			$line =~ /UNKNOWNNUMBER=([0-9]*)\&/;
			$HunkownNumber = $1;
			$line =~ /CORETURN=([0-9]*)\&/;
			$HcoreTurn = $1;
			$line =~ /CORENUMBER=([0-9]*)\&/;
			$HcoreNumber = $1;
			$line =~ /COREMINHP=([0-9]*)\&/;
			$HcoreMinHP = $1;
			$line =~ /COREMAXHP=([0-9]*)\&/;
			$HcoreMaxHP = $1;
			$line =~ /COREFLAG=([0-9]*)\&/;
			$HcoreFlag = $1;
			$line =~ /MONEY=([0-9]*)\&/;
			$HprizeMoney = int($1);
			$line =~ /FOOD=([0-9]*)\&/;
			$HprizeFood = int($1);
			if($line =~ /PRESENT=([0-9]*)\&/) {
				$HprizePresent = int($1);
			}
			my(%tmpItem);
			while($line =~/ITEM=([0-9]*)\&/g) {
				$tmpItem{$1} = 1;
			}
			foreach(0..$#HitemName) {
				push(@HprizeItem, int($tmpItem{$_}));
			}
		} else {
			$HsetEventMode = 2;
			while($line =~/DEL=([0-9]*)\&/g) {
				$HeventDel{$1} = 1;
			}
		}

# BattleField作成モード
	} elsif($getLine =~ /Bfield=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'bfield';
		$HbfieldMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Bfield=([^\&]*)\&/) {
		# BattleField作成ボタンが押された起動
		$HmainMode = 'bfield';
		$HbfieldMode = 1;
		$HdefaultPassword = htmlEscape($1);
		if($HoceanMode) {
			# 座標を選択可能な場合
			if($line =~ /OCEANX=([^\&]*)\&/) {
				$HoceanMapX = $1;
			}
			if($line =~ /OCEANY=([^\&]*)\&/) {
				$HoceanMapY = $1;
			}
			if($line =~ /RANDOM=([0-9]*)\&/) {
				$HmapRandom = $1;
			}
		}

# 管理人によるプレゼントモード
	} elsif($getLine =~ /Present/) {
		# 最初の起動
		$HmainMode = 'present';
		$HpresentMode = 0;
	} elsif($line =~ /Present/) {
		# プレゼントボタンが押された起動
		$HmainMode = 'present';
		$HpresentMode = 1;
		($HpresentMoney) = ($line =~ /PRESENTMONEY=([^\&]*)\&/);
		($HpresentFood ) = ($line =~ /PRESENTFOOD=([^\&]*)\&/);
		$line =~ /PRESENTLOG=([^\&]*)\&/;
		$HpresentLog = cutColumn($1, $HlengthPresentLog*2);

# 管理人による制裁モード
	} elsif($getLine =~ /Punish=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'punish';
		$HpunishMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Punish=([^\&]*)\&/) {
		# 制裁ボタンが押された起動
		$HmainMode = 'punish';
		$HpunishMode = 1;
		$HdefaultPassword = htmlEscape($1);

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /PUNISHID=([^\&]*)\&/;
		$HpunishID = $1;

# 管理人による地形変更モード
	} elsif($getLine =~ /Lchange=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Lchange=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'lchange';
		$HlchangeMode = 1;
		$HdefaultPassword = htmlEscape($1);

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /LCHANGEKIND=([^\&]*)\&/;
		$HlchangeKIND = $1;
		$line =~ /LCHANGEVALUE=([^\&]*)\&/;
		$HlchangeVALUE = $1;

# 管理人によるあずかりモード
	} elsif($getLine =~ /Pdelete=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'predelete';
		$HpreDeleteMode = 0;
		$HdefaultPassword = htmlEscape($1);
	} elsif($line =~ /Pdelete=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'predelete';
		$HpreDeleteMode = 1;
		$HdefaultPassword = htmlEscape($1);
		$line =~ /SETTURN=([0-9]*)\&/;
		$HsetTurn = $1;

# モバイルモード
	} elsif($line =~ /Mobile([0-9]*)/) {
		$HmainMode = $1;

# その他はトップモード
	} else {
		$HmainMode = 'top';
	}

	if($line =~ /IMGLINEMAC=([^&]*)\&/){
		my($flag) = $1;
		if($flag eq ''){
			$flag = $HimageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file://' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /IMGLINE=([^&]*)\&/){
		my($flag) = $1;
		$flag =~ tr/\\/\//;
		if(($flag eq 'deletemodenow') || ($flag eq '')){
			$flag = $HimageDir;
		} else {
			$flag =~ s/:/|/g;
			$flag =~ s/\/[\w\.]+\.gif$//g;
			$flag = 'file://' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /SKIN=([^\&]*)\&/) {
		my($flag) = $1;
		if(($flag eq 'del') || ($flag eq '')){
			$flag = "${HcssDir}/$HcssDefault";
		} else {
			$flag = "${HcssDir}/" . $flag;
		}
		$HskinName = $flag;
	}

}

#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# directory式ロック
		return hakolock1();
	} elsif($lockMode == 2) {
		# flock式ロック
		return hakolock2();
	} elsif($lockMode == 3) {
		# symlink式ロック
		return hakolock3();
	} elsif($lockMode == 4) {
		# 通常ファイル式ロック
		return hakolock4();
	} else {
		# rename式ロック
		$lfh = hakolock5() or die return 0;
		return 1;
	}
}

sub hakolock1 {
	# ロックを試す
	if(mkdir('hakojimalock', $HdirMode)) {
		# 成功
		return 1;
	} else {
		# 失敗
		my($b) = (stat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# 強制解除
			unlock();
			# ヘッダ出力
			tempHeader();
			# 強制解除メッセージ
			tempUnlock();
			# フッタ出力
			tempFooter();
			# 終了
			exit(0);
		}
		return 0;
	}
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# 成功
		return 1;
	} else {
		# 失敗
		return 0;
	}
}

sub hakolock3 {
	# ロックを試す
	if(symlink('hakojimalockdummy', 'hakojimalock')) {
		# 成功
		return 1;
	} else {
		# 失敗
		my($b) = (lstat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# 強制解除
			unlock();
			# ヘッダ出力
			tempHeader();
			# 強制解除メッセージ
			tempUnlock();
			# フッタ出力
			tempFooter();
			# 終了
			exit(0);
		}
		return 0;
	}
}

sub hakolock4 {
	# ロックを試す
	if(unlink('lockfile')) {
		# 成功
		open(OUT, '>lockfile.lock');
		print OUT time;
		close(OUT);
		return 1;
	} else {
		# ロック時間チェック
		if(!open(IN, 'lockfile.lock')) {
			return 0;
		}
		my($t);
		$t = <IN>;
		close(IN);
		if(($t != 0) && (($t + $unlockTime) < time)) {
			# 120秒以上経過してたら、強制的にロックを外す
			unlock();
			# ヘッダ出力
			tempHeader();
			# 強制解除メッセージ
			tempUnlock();
			# フッタ出力
			tempFooter();
			# 終了
			exit(0);
		}
		return 0;
	}
}

# rename式(Perlメモ http://www.din.or.jp/~ohzaki/perl.htm#File_Lock)
sub hakolock5 {
	my %lfh = (dir => "./", basename => "lockfile", timeout => $unlockTime, trytime => 3, @_);
	$lfh{path} = $lfh{dir}.$lfh{basename};

	for (my $i = 0; $i < $lfh{trytime}; $i++, sleep 1) {
		return \%lfh if (rename($lfh{path}, $lfh{current} = $lfh{path} . time));
	}

	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);

	foreach (@filelist) {
		if (/^$lfh{basename}(\d+)/) {
			return \%lfh if (time - $1 > $lfh{timeout} and
			rename($lfh{dir} . $_, $lfh{current} = $lfh{path} . time));
			last;
		}
	}
	undef;
}

# ロックを外す
sub unlock {
	if($lockMode == 1) {
		# directory式ロック
		rmdir('hakojimalock');
	} elsif($lockMode == 2) {
		# flock式ロック
		close(LOCKID);
	} elsif($lockMode == 3) {
		# symlink式ロック
		unlink('hakojimalock');
	} elsif($lockMode == 4) {
		# 通常ファイル式ロック
		my($i);
		$i = rename('lockfile.lock', 'lockfile');
	} else {
		# rename式ロック
		rename($lfh->{current}, $lfh->{path});
	}
}

# 小さい方を返す
sub min {
	return (sort { $a <=> $b } @_)[0];
}

# 大きい方を返す
sub max {
	return (sort { $b <=> $a } @_)[0];
}

# 1000億単位丸めルーチン
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "推定500${HunitMoney}未満";
	} else {
		$m = int(($m + 500) / 1000);
		return "推定${m}000${HunitMoney}";
	}
}

# 80ケタに切り揃え
sub cutColumn {
	my($s, $c) = @_;
	jcode::convert(\$s, 'euc');
	if(length($s) <= $c) {
		return $s;
	} else {
		if($HlengthAlert) {
			unlock();
			tempHeader();
			tempWrong("文字数オーバーです！");
			tempFooter();
			exit(0);
		}
		# 合計80ケタになるまで切り取り
		my($ss) = '';
		my($count) = 0;
		while($count < $c) {
			$s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
			if($1) {
				$ss .= $1;
				$count ++;
			} else {
				$ss .= $2;
			}
			$count ++;
		}
		return $ss;
	}
}

# 経験地からレベルを算出
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if ($kind == $HlandNavy) {
		# 海軍
		for ($i = $maxNavyLevel; $i > 1; $i--) {
			if ($exp >= $navyLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	} elsif ($kind == $HlandBase) {
		# ミサイル基地
		for ($i = $maxBaseLevel; $i > 1; $i--) {
			if ($exp >= $baseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	} elsif($kind == $HlandSbase) {
		# 海底基地
		for ($i = $maxSBaseLevel; $i > 1; $i--) {
			if ($exp >= $sBaseLevelUp[$i - 2]) {
				return $i;
			}
		}
		return 1;
	}
}

# 総獲得経験地からレベルを算出
sub gainToLevel {
	my($gain) = @_;
	my($i);
	for ($i = $HmaxComNavyLevel; $i > 1; $i--) {
		if ($gain >= $HcomNavyBorder[$i - 2]) {
			return $i;
		}
	}
	return 1;
}

# (0,0)から(size - 1, size - 1)までの数字が一回づつ出てくるように
# $pnum($pointNumber)(@rpx, @rpy)を設定
sub makeRandomIslandPointArray {
	my($island) = @_;

	undef $island->{'rpx'};
	undef $island->{'rpy'};
	my(@rpx, @rpy, $map, @x, @y, $xsize, $ysize, $pnum);
	$map = $island->{'map'};
	@x = @{$map->{'x'}};
	@y = @{$map->{'y'}};
	$xsize = @x;
	$ysize = @y;
	$pnum = $xsize * $ysize;

	my($x);
	# 初期値
	@rpx = (@x) x $ysize;
	foreach $y (@y) {
		push(@rpy, ($y) x $xsize);
	}

	# シャッフル
	my($i, $j);
	for ($i = $pnum; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@rpx[$i,$j] = @rpx[$j,$i];
		@rpy[$i,$j] = @rpy[$j,$i];
	}

	$island->{'pnum'} = $pnum - 1;
	$island->{'rpx'} = \@rpx;
	$island->{'rpy'} = \@rpy;
}

# 0から(n - 1)の乱数
sub random {
	return int(rand(1) * $_[0]);
}

# ソート
sub islandSort {
	my($kind, $mode) = @_;

	my @idx = (0..$#Hislands);
	@idx = sort {
			$Hislands[$b]->{'field'} <=> $Hislands[$a]->{'field'} ||         # バトルフィールド優先
			$Hislands[$a]->{'dead'} <=> $Hislands[$b]->{'dead'} ||           # 死滅フラグが立っていれば後ろへ
			$Hislands[$a]->{'predelete'} <=> $Hislands[$b]->{'predelete'} || # 管理人あずかりフラグが立っていれば後ろへ
			$Hislands[$b]->{$kind} <=> $Hislands[$a]->{$kind} || # $kindでソート
			$a <=> $b # $kindが同じなら以前のまま
		   } @idx;
	if($mode) {
		my @Hidx;
		foreach (0..$#idx) {
			$Hidx[$idx[$_]] = $_;
		}
		my %temp = %HidToNumber;
		while (my($k,$v) = each %temp){
			$HidToNumber{$k} = $Hidx[$v] if(defined $v);
		}
	}
	# 順位のもとになる要素の場合、配列を更新
	if($kind eq $HrankKind) {
		@Hislands = @Hislands[@idx] ;
		@idx = (0..$#Hislands);
	}
	return $Hislands[$idx[$HbfieldNumber]];
}

# ソート(同盟バージョン)
sub allySort {
	# scoreが同じときは直前のターンの順番のまま
	my @idx = (0..$#Hally);
	@idx = sort {
			$Hally[$a]->{'dead'} <=> $Hally[$b]->{'dead'} || # 死滅フラグが立っていれば後ろへ
			$Hally[$b]->{'score'} <=> $Hally[$a]->{'score'} ||
			$a <=> $b
		   } @idx;
	@Hally = @Hally[@idx];
	my @Hidx;
	foreach (0..$#idx) {
		$Hidx[$idx[$_]] = $_;
	}
	my %temp = %HidToAllyNumber;
	while (my($k,$v) = each %temp){
		$HidToAllyNumber{$k} = $Hidx[$v] if(defined $v);
	}
}

# 海軍の値を算出
sub estimateNavy {
	my($number) = @_;
	my($island, $fkind, $monslive, $monstertype, $hmonstertype, $unknownlive, $unknowntype);

	# 地形を取得
	$island = $Hislands[$number];
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# 数える
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if ($kind == $HlandNavy) {
				my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($value);
				my $nSpecial = $HnavySpecial[$nKind];
				my $n = $HidToNumber{$nId};
				if($HautoKeepID{$nId} && ($nId != $id)) {
					# 海にする
					$land->[$x][$y] = $HlandSea;
					$landValue->[$x][$y] = $nSea;
				} elsif(defined $n) {
#					if(!($nFlag & 1) && !($nSpecial & 0x8)) {
#						$Hislands[$n]->{'ships'}[$nNo]++;
#						$Hislands[$n]->{'ships'}[4]++;
#					}
#					$Hislands[$n]->{'shipk'}[nKind]++;
					my $fvalue = sprintf("%08x", navyPack($id, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp));
					push(@{$Hislands[$n]->{'fkind'}}, "$fvalue");
					$Hislands[$n]->{'navy'}[$nKind]++;
				} elsif(!($nSpecial & 0x8) && !($nFlag & 1)) {
					$unknownlive++;
					$unknowntype |= (2 ** $nKind);
				}
			} elsif(($kind == $HlandMonster) || ($kind == $HlandHugeMonster)){
				my($mId, $mHflag, $mSea, $mExp, $mFlag, $mKind, $mHp) = monsterUnpack($value);
				if($HautoKeepID{$mId}) {
					if ($mFlag & 2) {
						$land->[$x][$y] = $HlandSea;
						$landValue->[$sx][$sy] = $mSea;
					} else {
						$land->[$x][$y] = $HlandWaste;
						$landValue->[$sx][$sy] = 0;
					}
				} elsif(($kind == $HlandHugeMonster) && ($mHflag == 0)) {
					$monslive++;
					$hmonstertype |= (2 ** $mKind);
				} elsif($kind == $HlandMonster) {
					$monslive++;
					$monstertype |= (2 ** $mKind);
				}
			}
		}
	}
	$island->{'monsterlive'}  = "$monslive,$monstertype,$hmonstertype,$unknownlive,$unknowntype";
}

#----------------------------------------------------------------------
# ログ表示
#----------------------------------------------------------------------
# ファイル番号指定でログ表示
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	my $nowTurn = -1;

	open(LIN, "${HdirName}/$_[0]$HlogData");
	my($line, $m, $turn, $id1, $id2, $id3, $message, @ids);
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-\s]*),(.*)$/;
		($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
		next if($m eq '');
		@ids = ($id1, $id2, split('-', $id3));
		if ($nowTurn != $turn) {
			out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
			out("<HR>${HtagNumber_}ターン $turn${H_tagNumber}\n<BLOCKQUOTE>\n");
			$nowTurn = $turn;
		}

		# 機密関係
		if($m == 1) {
			if(($mode == 0) || ($id1 != $id)) {
				# 機密表示権利なし
				next;
			}
			$m = "<span class='lbbsST'>(機密)</span>";
		} else {
			$m = '';
		}

		# 表示的確か
		if($id != 0) {
			my $flag = 1;
			foreach (@ids) {
				if($id == $_) {
					$flag = 0;
					last;
				}
			}
			next if($flag);
		}

		# 表示
		my $str = "${m}$message<BR>";
		if($Hmobile) {
			1 while $str =~ s/(.*)(<BR>　--- (.*))/$1<BR>/i;
			1 while $str =~ s/(.*)(<(span[\s\w\=\+\-\#\"\']+)>(.*)<\/span>)/$1$4/i;
			if($str =~ /(　--- )/) {
				if($str !~ /(沈没|機密)/) {
					$str = (split(/。/, $str))[0] . '<BR>';
				}
			} elsif($str =~ /(　･･･ )/) {
				next;
			} elsif($str =~ /(　 )/) {
				1 while $str =~ s/(.*)(<B>(.*)<\/B>)/$1$3/i;
			} else {
				$str = '◆' . $str;
			}
		}
		out("$str\n");
	}
	close(LIN);

	out("</BLOCKQUOTE>\n") if ($nowTurn != -1);
}

#----------------------------------------------------------------------
# テンプレート
#----------------------------------------------------------------------
# 初期化
sub tempInitialize {
	my($mode) = @_;

	# 島セレクト(デフォルト自分)
	$HislandList = getIslandList($defaultID, $mode);
	$HtargetList = getIslandList($defaultTarget, $mode);
}

# 島データのプルダウンメニュー用
sub getIslandList {
	my($select, $mode, $color) = @_;
	my($list, $name, $id, $s, $i, $c);

	#島リストのメニュー
	$list = '';
	$list = "<OPTION VALUE=\"0\" SELECTED>新規作成(すべて海)\n" if($select == -1);
	foreach $i (0..$islandNumber) {
		$island = $Hislands[$i];
		next if($mode == 2 && !$island->{'field'});
		$name = islandName($island);
		$name =~ s/<[^<]*>//g;
		$id = $Hislands[$i]->{'id'};
		if($id eq $select) {
			$s = ' SELECTED';
			$c = " style=\"background:$color;\"" if($color ne '');
		} else {
			$s = '';
			$c = '';
		}

		$list .= "<OPTION VALUE=\"$id\"$c$s>${name}\n" if($mode || !$island->{'field'});
	}
	return $list;
}

# ロック失敗
sub tempLockFail {
	# タイトル
	out(<<END);
${HtagBig_}同時アクセスエラーです。<BR>
ブラウザの「戻る」ボタンを押し、<BR>
しばらく待ってから再度お試し下さい。${H_tagBig}$HtempBack
END
}

# 強制解除
sub tempUnlock {
	# タイトル
	out(<<END);
${HtagBig_}前回のアクセスが異常終了だったようです。<BR>
ロックを強制解除しました。${H_tagBig}$HtempBack
END
}

# パスワードファイルがない
sub tempNoHpasswordFile {
	out(<<END);
${HtagBig_}パスワードファイルが開けません。${H_tagBig}$HtempBack
END
}

# メインデータがない
sub tempNoDataFile {
	out(<<END);
${HtagBig_}データファイルが開けません。${H_tagBig}$HtempBack
END
}

# 何か問題発生
sub tempProblem {
	out(<<END);
${HtagBig_}問題発生、とりあえず戻ってください。${H_tagBig}$HtempBack
END
}

# コメント
sub tempAnyString {
	out(<<END);
${HtagBig_}$_[0]${H_tagBig}$HtempBack
END
}

# メンテナンス中
sub mente_mode {
	# ヘッダ出力
	tempHeader();

	# メッセージ
	out("${HtagBig_}只今メンテナンス中です。<BR>暫くお待ち下さい。${H_tagBig}");

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}
#----------------------------------------------------------------------
# ヘッダ
#----------------------------------------------------------------------
sub tempHeader {
	if($HimgLine ne '' ){
		$baseIMG = $HimgLine;
	} else {
		$baseIMG = $HimageDir;
	}
	my($bIstr) = ($HmainMode eq 'setupv') ? "" : "<BASE HREF='${baseIMG}/'>";
	if($HskinName ne '' ){
		$baseSKIN = $HskinName;
	} else {
		$baseSKIN = "${HcssDir}/$HcssDefault";
	}

	# jcode使用時はcharsetをShift_JISに
 	if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ && $Hgzip == 1){
		print qq{Content-type: text/html; charset=EUC-JP\n};
		print qq{Content-encoding: gzip\n\n};
		open(STDOUT,"| $HpathGzip/gzip -1 -c");
		print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}else{
		print qq{Content-type: text/html; charset=EUC-JP\n\n};
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}

	if(!$Hmobile) {
		out(<<END);
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
$HtitleTag($versionInfo)
</TITLE>
$bIstr
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
</HEAD>
$Body<DIV ID='BodySpecial'>
<!-- NINJA ANALYZE -->
<script type="text/javascript">
//<![CDATA[
(function(d) {
  var sc=d.createElement("script"),
      ins=d.getElementsByTagName("script")[0];
  sc.type="text/javascript";
  sc.src=("https:"==d.location.protocol?"https://":"http://") + "code.analysis.shinobi.jp" + "/ninja_ar/NewScript?id=00231338&hash=9a215404&zone=36";
  sc.async=true;
  ins.parentNode.insertBefore(sc, ins);
})(document);
//]]>
</script>
<!-- /NINJA ANALYZE -->

<DIV ID='LinkHead'>
$Hheader
END

		my $nextturn = '';
		foreach (1..$HrepeatTurn) {
			$nextturn .= '・' if($_ != 1);
			$nextturn .= $HislandTurn + $_;
			last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
		}
		out(<<END) if($Hrealtimer && (defined $HleftTime));
<DIV ID="REALTIME" class="timer"></DIV>
<SCRIPT language="JavaScript">
<!--
var leftTime = $HleftTime;
var hour, min, sec;

function showTimeLeft() {
	if (leftTime > 0) {
		setTimeout('showTimeLeft()', 1000);
		hour = Math.floor(leftTime / 3600);
		min  = Math.floor(leftTime % 3600 / 60);
		sec  = leftTime % 60;
		leftTime--;
		document.all.REALTIME.innerHTML = '次回更新(<span class="number">ターン$nextturn</span>)まで残り ' + hour + '時間 ' + min + '分 ' + sec + '秒 ($HnextTime)';
	} else {
		document.all.REALTIME.innerHTML = 'ターン更新時刻になりました！ ($HnextTime)';
	}
}

if ($HplayNow) {
	showTimeLeft();
} else {
	document.all.REALTIME.innerHTML = 'ゲームは終了しました！';
}
//-->
</SCRIPT>
END
		out("<HR></DIV>");
	} else {
       out(<<END);
<HTML><HEAD><TITLE>$Htitle</TITLE></HEAD>
<BODY bgcolor="#ffffff">


<a href="./hako-main.cgi">トップ</a> <a href="./hako-main.cgi?SetupV=1">ヘルプ</a> <a href="./hako-main.cgi?FightLog=1">リンク</a>
<HR>
END
	}
}

#----------------------------------------------------------------------
# フッタ
#----------------------------------------------------------------------
sub tempFooter {
	out(<<END) if(!$Hmobile);
<HR>
<DIV ID='LinkFoot'>
$Hfooter
<DIV align="right">
END
##### 追加 親方20020307
	if($Hperformance && !$Hmobile) {
		my($uti, $sti, $cuti, $csti) = times();
		$uti += $cuti;
		$sti += $csti;
		my($cpu) = $uti + $sti;

	#	   ログファイル書き出し(テスト計測用　普段はコメントにしておいてください)
	#	   open(POUT,">>cpu-h.log");
	#	   print POUT "CPU($cpu) : user($uti) system($sti)\n";
	#	   close(POUT);

		out(<<END);
　<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
END
	}
#####
	out(<<END) if(!$Hmobile);
<HR>
<B>海戦 JS.$versionInfo(based on ver1.3)</B> patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/'>neo_otacky</a>
</DIV></DIV></DIV>
END
	if($oroti) {
		out(<<END);
<script type="text/javascript">
<!--
var image = document.getElementsByTagName('img');
for (var i = 0; i < image.length; i++){
	image[i].src = image[i].src.replace("$HbaseDir","$baseIMG");
}
//-->
</script>

END
	}

	out("</BODY></HTML>");
}
