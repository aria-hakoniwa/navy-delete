# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
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
# 海戦JS版用に改変
#----------------------------------------------------------------------
# ＪＡＶＡスクリプト版 -ver1.11-
# 使用条件、使用方法等は、配布元でご確認下さい。
# 付属のjs-readme.txtもお読み下さい。
# あっぽー：http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ポップアップナビJS部分
#----------------------------------------------------------------------
$HpopupNaviJS =<<"END" if($HpopupNavi);
$HnaviExp

function Navi(x, y, img, title, text, exp) { // 1
	if(!document.mark_form.mark.checked) {
		StyElm = document.getElementById("NaviView");
		StyElm.style.visibility = "visible";
		if(x - mapX + 1 > $HislandSizeX / 2) {
//			StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // 左側
			StyElm.style.marginLeft = -10; // 左側
		} else {
//			StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // 右側
			StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 120; // 右側
		}
//		if(y - mapY + 1 == $HislandSizeY) {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1.5) * $HchipSize*2; // 下側
//		} else if(y - mapY + 1 > $HislandSizeY / 2) {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // 下側
//		} else {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // 上側
//		}
		StyElm.innerHTML = "<div class='NaviTitle'>" + title + " (" + x + "," + y + ")<\\/div><table><tr><td class='M'><img class='NaviImg' src=" + img + "><\\/td><td class='M'><div class='NaviText'>" + text + "<\\/div>";
		if(exp) {
			StyElm.innerHTML += "<div class='NaviText'>" + eval(exp) + "<\\/div>";
		}
		StyElm.innerHTML += "<\\/td><\\/tr><\\/table>";
	}
}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
END
#----------------------------------------------------------------------
# Ｊａｖａスクリプト開発画面
#----------------------------------------------------------------------
# ヘッダ
sub tempHeaderJava {
	if($HimgLine ne '' ){
		$baseIMG = $HimgLine;
	} else {
		$baseIMG = $HimageDir;
	}
	if($HskinName ne '' ){
		$baseSKIN = $HskinName;
	} else {
		$baseSKIN = "${HcssDir}/$HcssDefault";
	}
	my($styleUseNavy, $styleUseFlag, $styleUseMark);
	$styleUseNavy = ".useNavy, " if(($HnavyName[0] eq '') || ($HjavaMode eq 'cgi'));
	$styleUseMark = ".mark_form{ visibility:hidden; } " if($HjavaMode eq 'cgi');
	$styleUseFlag = <<"END" if(!$HuseFlag || ($HjavaMode eq 'cgi'));
<style type="text/css">
<!--
${styleUseNavy}.useFlag { visibility:hidden; }
${styleUseMark}
-->
</style>
END

	# 次のターンまでの時間表示
	if (!($HmainMode eq 'turn') && (defined $HleftTime)) {
		my $nextturn = '';
		if(!$HgameLimitTurn || ($HislandTurn < $HgameLimitTurn)) {
			my $hour2 = int($HleftTime / 3600);
			my $min2 = int(($HleftTime - $hour2 * 3600) / 60);
			my $sec2 = ($HleftTime - $hour2 * 3600 - $min2 * 60);
			foreach (1..$HrepeatTurn) {
				$nextturn .= '・' if($_ != 1);
				$nextturn .= $HislandTurn + $_;
				last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
			}
			$rtStr = "次の更新時間<span class='number'>(ターン$nextturn)</span>まであと $hour2時間 $min2分 $sec2秒";
		} else {
			$rtStr = "　";
		}
		$realtimejs =<<END if($Hrealtimer);
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

	}

	if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ && $Hgzip == 1){
		print qq{Content-type: text/html; charset=EUC-JP\n};
		return if($Hasync);
		print qq{Content-encoding: gzip\n\n};
		open(STDOUT,"| $HpathGzip/gzip -1 -c");
		print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}else{
		print qq{Content-type: text/html; charset=EUC-JP\n\n};
		return if($Hasync);
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};
	}

	out(<<END);
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html;charset=EUC-JP">
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$baseIMG/">
<link rel="stylesheet" type="text/css" href="${baseSKIN}">
$styleUseFlag
</HEAD>
$Body<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
$Hheader
<DIV ID="REALTIME" class=timer>$rtStr</DIV>
$realtimejs
<HR></DIV>
END
}

# 艦艇ソート
sub sortOption {
	$a =~ /^\<.+\>(.+) \(.+ (.+)\/.+\/.+ (.+)\)$/;
	my($aa) = sprintf("%s%03d%02d", $1, $3, $2);
	$b =~ /^\<.+\>(.+) \(.+ (.+)\/.+\/.+ (.+)\)$/;
	my($bb) = sprintf("%s%03d%02d", $1, $3, $2);
#	my($aa) = ($a =~ /^\<.+\>(.+)$/);
#	my($bb) = ($b =~ /^\<.+\>(.+)$/);
	return ($bb cmp $aa);
};

# ○○島開発計画
sub tempOwnerJava {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# 艦隊構成を調べる・マップデータ取得・軍港データ取得
	my($id, $land, $landValue, $landValue2, $map) = ($island->{'id'}, $island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}, $island->{'map'});
	my(@fleet);
	my(@nFleet) = (0, 0, 0, 0);
	my($x, $y, $nKind, $value, $value2, $name, %invade);
	my $setmap = '';
	my $navyPort = 0;
	my @x = (!$HoceanMode) ? @{$map->{'x'}} : @defaultX;
	my @y = (!$HoceanMode) ? @{$map->{'y'}} : @defaultY;
	foreach $y (@y) {
		$setmap .= '[';
		foreach $x (@x) {
			if($HoceanMode && ($HlandID[$x][$y] != $id)) {
				# 領海でない
				$setmap .= '-2,';
				next;
			}
			$nKind = int($land->[$x][$y]);
			$value = $landValue->[$x][$y];
			$value2 = $landValue2->[$x][$y];
			if ($nKind != $HlandNavy) {
				$setmap .= (($nKind == $HlandSea) && $value) ? '-1,' : "$nKind,";
				next;
			}
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);# 上のタブのとこ
                        my($goal);
                        if(($goalx == 31) ||
                           ($goaly == 31)) {
                            $goal = "停船中";
                        }else{
                            $goal = "目標($goalx, $goaly)";
                        }

                        $wait--;

                        # 航空機の発進待ち表示
                        if($wait <= 0){
                            $ririku = "、発艦準備OK";
                        }else{
                            $ririku = "、離陸待ち${wait}ターン"
                        }

                        # 発進機能なかったら消す
                        if(($nKind != 0) && ($nKind != 0x0c)){
                            $ririku = "";
                        }

                        # 航空機だったら表記変更
                        if($HnavyCruiseTurn[$nKind] !=0){
                            $ririku = "、${wait}ターン後に帰投";
                        }

			# 残骸は除く
			if($nFlag == 1) {
				$setmap .= "$nKind,";
				next;
			}

			# 他の島の艦隊は除く
			if ($nId != $id) {
				$invade{"$nId,$nNo"} += 1;
				$setmap .= "$nKind,";
				next;
			}

                        # 最大耐久力
                        my $maxHp = int($HnavyHP[$nKind] * (120 + $nExp) / 120);

			my $nSpecial = $HnavySpecial[$nKind];
			my $navyLevel = expToLevel($HlandNavy, $nExp);
			# 港をチェック
			if($nSpecial & 0x8) {
				$setmap .= (100 + $navyLevel) . ',';
				$navyPort++;
                        }elsif($HnavyNoMove[$nKind]){
				$setmap .= "$HlandNavy,";
			} else {
				$setmap .= "$HlandNavy,";
				$name = $HnavyName[$nKind];
				push(@{$fleet[$nNo]}, <<END);
<OPTION value="$x,$y">$name (耐久力${nHp}/${maxHp}、経験値${nExp}${ririku})
END
				$nFleet[$nNo]++;
			}
		}
		substr($setmap, -1) = '';
		$setmap .= "],\n";
	}
	substr($setmap, -2) = '';
	@{$fleet[0]} = sort sortOption @{$fleet[0]};
	@{$fleet[1]} = sort sortOption @{$fleet[1]};
	@{$fleet[2]} = sort sortOption @{$fleet[2]};
	@{$fleet[3]} = sort sortOption @{$fleet[3]};

	my $navyBuild = '';
	foreach (@HcomNavyNumber) {
		$navyBuild .= $_ . ',';
	}
	substr($navyBuild, -1) = '';

	my $ifname = '';
	foreach (sort { $a cmp $b } keys %invade) {
		my($iId,$iNo) = split(/\,/, $_);
		my $in = $HidToNumber{$iId};
		if(defined $in) {
			my $iName = islandName($Hislands[$in]);
			$ifname .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]艦隊($invade{$_}艦)<BR>"
		} else {
			$ifname .= "所属不明($invade{$_}艦)<BR>";
		}
	}
	$ifname .= '　';

	# コマンドセット
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# 各要素の取り出し
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg, $s_target2) = (
			$command->{'kind'},
			$command->{'target'},
			$command->{'x'},
			$command->{'y'},
			$command->{'arg'},
			$command->{'target2'}
		);
		# コマンド登録
		$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_target2\]\,\n";
		$com_max .= "[0,0],";
	}
	substr($set_com, -2) = '';
	substr($com_max, -1) = '';

	#コマンドリストセット
	my($l_kind);
	$set_listcom = "";
	@click_com = ();
	$All_listCom = 0;
	$com_count = @HcommandDivido;
	#建造(経験値)レベル確認
	my $navyComLevel = gainToLevel($island->{'gain'});
	for($m = 0; $m < $com_count; $m++) {
		($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
		$set_listcom .= "\[ ";
		for($i = 0; $i < $HcommandTotal; $i++) {
			$l_kind = $HcomList[$i];
			next if($HmaxComNavyLevel &&
				 ($HcomNavy[0] + $HcomNavyNumber[$navyComLevel-1] < $l_kind) && ($l_kind <= $HcomNavy[$#HnavyName]));
			next if($HuseCoreLimit && ($l_kind == $HcomCore) &&
				 ($HislandTurn - $island->{'birthday'} > $HdevelopTurn));
			$l_cost = $HcomCost[$l_kind];
			if($l_cost eq '0') {
				$l_cost = '無料';
			} elsif($l_cost =~ /^\@(.*)$/) {
				$l_cost = $1;
			} elsif($l_cost < 0) {
				$l_cost = - $l_cost;
				$l_cost .= $HunitFood;
			} else {
				$l_cost .= $HunitMoney;
			}
			if($l_kind >= $dd && $l_kind <= $ff) {
				my($l_name) = $HcomName[$l_kind];
				next if($l_name eq '');
				$set_listcom .= "\[$l_kind\,\'$l_name\',\'$l_cost\',$HcomTurn[$l_kind]\]\,\n";
				$All_listCom++;
				if(($m == 0) || ($m == 1) || ($m == 2) || ($m == 3) || ($m == 4) || ($m == 5) || ($m == 7)){ #コマンドポップアップの右側のとこ出すかどうか
					next if(($l_kind == $HcomNavySend) || ($l_kind == $HcomNavyReturn)); # 自島に対しては実行しない
					$l_name = ($HcomTurn[$l_kind] > 0) ? "$HtagComName1_${l_name}$H_tagComName" : "$HtagComName2_${l_name}$H_tagComName";
					$click_com[$m] .= "<a title='$l_cost' onMouseOver='StatusMsg($l_kind);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none;cursor:pointer;'>$l_name</a><br>\n";
				}
			}
		}
		substr($set_listcom, -2) = '' if(substr($set_listcom, -2) ne "\[ ");
		$set_listcom .= " \],\n";
	}
	substr($set_listcom, -2) = '';
	if($HdefaultKind eq ''){
		$default_Kind = 1;
	} else {
		$default_Kind = $HdefaultKind;
	}
	my @ofnamejs = @{$island->{'fleet'}};
	my @monumentjs = @HmonumentName;
	foreach (@ofnamejs, @monumentjs) {
		$_ =~ s/'/\\'/g;
		$_ = "'$_'";
	}
	my $ofname = join(',', @ofnamejs);
	my $monument = join(',', @monumentjs);

	# 艦艇移動ポップアップメニューセット
	$click_com[3] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD colspan=2></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,17)' class='M'>11時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,18)' class='M'>12時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,7)' class='M'>１時</a></TH><TD colspan=2></TD></TR>
<TR><TD></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,16)' class='M'>10時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,6)' class='M'>左上</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,1)' class='M'>右上</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,8)' class='M'>２時</a></TH><TD></TD></TR>
<TR><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,15)' class='M'>９時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,5)' class='M'> 左 </a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,0)' class='M'>待機</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,2)' class='M'> 右 </a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,9)' class='M'>３時</a></TH></TR>
<TR><TD></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,14)' class='M'>８時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,4)' class='M'>左下</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,3)' class='M'>右下</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,10)' class='M'>４時</a></TH><TD></TD></TR>
<TR><TD colspan=2></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,13)' class='M'>７時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,12)' class='M'>６時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,11)' class='M'>５時</a></TH><TD colspan=2></TD></TR>
</TABLE>
END
	$click_com[6] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,0)' class='M'>通常</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,1)' class='M'>退治</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,2)' class='M'>巡航</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,3)' class='M'>停船</a></TH>
</TR>
</TABLE>
END

	# 艦隊移動ポップアップメニューセット
	$click_com[9] = '';

	#島リストセット
	my($set_island, $l_name, $l_id);
	$set_island = "";
	foreach $i (0..$islandNumber) {
		$l_name = islandName($Hislands[$i]);
		$l_name =~ s/<[^<]*>//g;
		$l_name =~ s/'/\\'/g;
		$l_id = $Hislands[$i]->{'id'};
		$set_island .= "\'$l_id\'\:\'$l_name\'\,\n";
		$click_com[9] .="<a href='javascript:void(0);' onClick='cominput(myForm,8,$l_id)' STYlE='text-decoration:none;'>$l_name</a><br>\n";
	}
	substr($set_island, -2) = '';
	substr($click_com[9], -5) = "\n";
	if($Htournament){
		# トーナメント
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		if($island->{'fight_id'} < 1){
			# 無し
			$HtargetList = "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
			$click_com[9] ="<a href='javascript:void(0);' onClick='cominput(myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}else{
			# 有り
			my $fight_id = $island->{'fight_id'};
			$click_com[9] ="<a href='javascript:void(0);' onClick='cominput(myForm,8,$fight_id)' STYlE='text-decoration:none;'>${tName}</a><BR>\n";
			$click_com[9] .="<a href='javascript:void(0);' onClick='cominput(myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}
	}
	# 怪獣名前セット
	my($monsterName, $hugeMonsterName);
	if($HuseSendMonster || $HuseSendMonsterST) {
		$monsterName = "monsterName = \[\n";
		foreach (@HmonsterName) {
			$monsterName .= "\'$_\'\,\n";
		}
		substr($monsterName, -2) = "\n";
		$monsterName .= "\]";
		if($HhugeMonsterAppear && ($HsendHugeMonsterNumber >= 0)) {
			$hugeMonsterName = "hugeMonsterName = \[\n";
			foreach (@HhugeMonsterName) {
				$hugeMonsterName .= "\'$_\'\,\n";
			}
			substr($hugeMonsterName, -2) = "\n";
			$hugeMonsterName .= "\]";
		}
	}

	my $portflag = '';
	foreach (0..$#HnavyName) {
		$portflag .= ($HnavySpecial[$_] & 0x8) ? '1,' : '0,';
	}
	substr($portflag, -1) = "";

	my $stcheck = '';
	foreach (0..$#HmissileName) {
		$stcheck .= ($HmissileSpecial[$_] & 0x1) ? '1,' : '0,';
	}
	substr($stcheck, -1) = "";

	if($HextraJs) {
		unless(-e "${HefileDir}/hakojima.js") {
			require('./hako-js.cgi');
			makeJS(1);
		}
	}
	my($styleUseComplex) = '';
	$styleUseComplex = ', #category2' if(!$HuseComplex2);#変更
	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>
<BR>
</DIV>
<STYLE type="text/css">
<!--
#submenu2, #submenu3, #submenu4, #submenu5, #submenu6${styleUseComplex} { display:none; }
-->
</STYLE>
<SCRIPT Language="JavaScript">
<!--
// ＪＡＶＡスクリプト開発画面配布元
// あっぽー庵箱庭諸島（ http://appoh.execweb.cx/hakoniwa/ ）
// Programmed by Jynichi Sakai(あっぽー)
// ↑ 削除しないで下さい。
var xmlhttp;
var str;
var d_Kind = $default_Kind;
var d_ID = $HcurrentID;
var All_list = $All_listCom;
var navyPort = $navyPort;
var mapX = $island->{'map'}->{'x'}[0];
var mapY = $island->{'map'}->{'y'}[0];
ofName = [$ofname];
portflag = [$portflag];
stcheck = [$stcheck];
monument = [$monument];
mapdata = [
$setmap
];
navybuild = [$navyBuild];
g = [$com_max];
tmpcom1 = [ [0,0,0,0,0,0] ];
command = [
$set_com
];
comlist = [
$set_listcom
];
islname = {
$set_island
};
$monsterName;
$hugeMonsterName;

function display(num) {
  var cid = 'category' + num;
  var id = 'submenu' + num;
  if(document.getElementById){
    var obj = document.getElementById(id);
    obj.style.display='block';
    var con = document.getElementById(cid);
    con.style.fontWeight='bold';
    for(ii=1; ii < 7; ii++) {
      if(ii != num) {
        var cid2 = 'category' + ii;
        var id2 = 'submenu' + ii;
        var obj2 = document.getElementById(id2);
        obj2.style.display='none';
        var con2 = document.getElementById(cid2);
        con2.style.fontWeight='normal';
      }
    }
  }
}

function searchNavyPort(x, y, range){
	var xArray = new Array(${\join(',', @ax)});
	var yArray = new Array(${\join(',', @ay)});
	var cxArray = new Array(${\join(',', @correctX)});
	var cyArray = new Array(${\join(',', @correctY)});
	if(range == 0) {
		range = $an[$#an] - 1;
	}
	for (j = 0; j < range; j++) {
		var targetX = x * 1 + xArray[j];
		var targetY = y * 1 + yArray[j];

		// 行による位置調整
		if(((targetY % 2) == 0) && ((y % 2) == 1)) {
			targetX--;
		}
		targetX = cxArray[targetX + $#an];
		targetY = cyArray[targetY + $#an];
		if(!(targetX < 0 || targetY < 0)) {
			if(mapdata[targetY][targetX] > 100) {
				return (mapdata[targetY][targetX] - 100);
			}
		}
	}
	if(range == $an[$#an] - 1) {
		for (k = ${\min(@{$island->{'map'}->{'y'}})}; k <= ${\max(@{$island->{'map'}->{'y'}})}; k++) {
			for (j = ${\min(@{$island->{'map'}->{'x'}})}; j <= ${\max(@{$island->{'map'}->{'x'}})}; j++) {
				if(mapdata[k][j] > 100) {
					return (mapdata[k][j] - 100);
				}
			}
		}
	}
	return 0;
}

//-->
</SCRIPT>
END

	if($HextraJs) {
		out(<<END);
<SCRIPT Language="JavaScript" SRC="${efileDir}/hakojima.js"></SCRIPT>
END
	} else {
		require('./hako-js.cgi');
		makeJS(0);
	}

	out(<<END);
<!-- 数量変更フォーム -->
<DIV ID="mc_div" style="background-color:white;position:absolute;top:-50;left:-50;height:22px;">&nbsp;</DIV>
<DIV ID="ch_num" style="position:absolute;visibility:hidden;display:none">
<form name="ch_numForm">
<TABLE BORDER=1 BGCOLOR="#e0ffff" CELLSPACING=1>
<TR><TD VALIGN=TOP NOWRAP>
<A HREF="JavaScript:void(0)" onClick="hideElement('ch_num');" STYlE="text-decoration:none"><B>×</B></A><BR>
<select name="AMOUNT" size=13 onchange="chNumDo()">
</select>
</TD>
</TR>
</TABLE>
</form>
</DIV>
<!-- 艦隊移動フォーム -->
<DIV ID="menu3" style="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD class='T'>
<FORM name='POPUP3'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR><TD><DIV style="overflow-y:auto; height:100px;">
$click_com[9]
</DIV></TD></TR>
<TR><TD class='T'>
<small>
<span class='attention'>！艦隊番号を確認して下さい！</span><br>
「数量」で艦隊番号を指定してから<br>
移動させたい$AfterName名をクリック
</small>
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
<!-- 移動操縦フォーム -->
<DIV ID="menu2" style="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD class='T'>
<FORM name='POPUP2'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR><TD><DIV align='center'>
$click_com[3]</DIV>
</TD></TR>
<TR><TD class='T'>
<small>
<span class='attention'>！艦艇の能力を確認して下さい！</span><br>
艦艇操作=>「移動操縦(旗艦)」<br>
2Hex移動=>「移動が(とても)速い」
</small>
</TD></TR>
<TR><TD align='center'>
${HtagTH_}指令変更${H_tagTH}$click_com[6]
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
<!-- コマンドフォーム -->
<DIV ID="menu" style="position:absolute; visibility:hidden; top:-500;left:-500;"> 
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD colspan=2 class='T'>
<FORM name='POPUP1'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR>
<TD valign='top'>
<a href="javascript:void(0);" onClick="display(1);" STYlE='text-decoration:none; font-weight:bold;' id='category1'>内政(造成)</a><BR>
<a href="javascript:void(0);" onClick="display(2);" STYlE='text-decoration:none;' id='category2'>内政(建築)</a>
<a href="javascript:void(0);" onClick="display(3);" STYlE='text-decoration:none;' id='category3'>内政(建設)</a>
END

	out("<BR>") if($HuseComplex);

	out(<<END);
<a href="javascript:void(0);" onClick="display(4);" STYlE='text-decoration:none;' id='category4'>海軍</a><BR>
<a href="javascript:void(0);" onClick="display(5);" STYlE='text-decoration:none;' id='category5'>作戦指令</a><BR>
<a href="javascript:void(0);" onClick="display(6);" STYlE='text-decoration:none;' id='category6'>軍事施設</a>
</TD>
<TD valign='top'>
<DIV id='submenu1'>$click_com[0]</DIV>
<DIV id='submenu2'>$click_com[1]</DIV>
<DIV id='submenu3'>$click_com[2]</DIV>
<DIV id='submenu4'>$click_com[4]</DIV>
<DIV id='submenu5'>$click_com[5]</DIV>
<DIV id='submenu6'>$click_com[7]</DIV>
</TD></TR>
<TR><TD COLSPAN=2>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
END

	islandInfo(1);

	out(<<END);
<DIV align='center'><TABLE BORDER=0><TR><TD class='M'>
<TABLE BORDER>
<TR valign=top>
<TD $HbgInputCell width=25%>
<FORM name="myForm" action="$HthisFile" method=POST onsubmit="return send_command(this);">
<INPUT TYPE=submit VALUE="計画送信" NAME="CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}">
<span id="progresssub"></span>
<HR>
<B>計画番号</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
	# 計画番号
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><br>
<INPUT TYPE="checkbox" NAME="MENUOPEN" onClick="check_menu()" $HmenuOpen>非表\示
<INPUT TYPE="checkbox" NAME="MENUOPEN2" onClick="check_menu2()" $HmenuOpen2 class='useFlag'><span class='useFlag'>移動操縦</span>
<INPUT TYPE="checkbox" NAME="MENUOPEN3" onClick="check_menu3()" $HmenuOpen3 class='useNavy'><span class='useNavy'>艦隊移動</span>
<br>
<SELECT NAME=menuList onchange="SelectList(myForm)">
<OPTION VALUE=>全種類
END
	for($i = 0; $i < $com_count; $i++) {
#		next if($i == 4 && !$HuseBase && !$HuseSbase && !$HuseSendMonster && !$HuseSendMonsterST);
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
	out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
</SELECT>
<HR>
<P>
<B>コマンド入力</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">挿入</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">上書き</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">削除</A>
</B><HR>
<B>座標(</B>
<SELECT NAME=POINTX>

END
	foreach $x (@defaultX) {
		if($x == $HdefaultX) {
			out("<OPTION VALUE=$x SELECTED>$x\n");
		} else {
			out("<OPTION VALUE=$x>$x\n");
		}
	}

	out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

	foreach $y (@defaultY) {
		if($y == $HdefaultY) {
			out("<OPTION VALUE=$y SELECTED>$y\n");
		} else {
			out("<OPTION VALUE=$y>$y\n");
		}
	}
	out(<<END);
</SELECT><B>)</B>
<HR>
<B>数量</B><SELECT NAME=AMOUNT>
END

	# 数量
	foreach $i (0..99) {
		out("<OPTION VALUE=$i>$i\n");
	}
	my($myislandID) = $defaultTarget;
	$myislandID = $island->{'id'} if($myislandID eq '');

	my($strUseNavy);
	$strUseNavy = "(艦隊移動元)" if($HnavyName[0] ne '');
	out(<<END);
</SELECT>
<HR>
<B>目標の${AfterName}</B>${strUseNavy}：
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> 表\示 </A></B>
・
<B><A HREF=JavaScript:void(0); onClick="myisland(myForm,'$myislandID')"> 前選\択 </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT><BR>
END
	if($HmlogMap) {
		out(<<END);
<BR><B> 着弾点表\示 </B><BR>
END
		my($i, $turn);
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=JavaScript:void(0); onClick=\"jump(myForm, '$HjavaMode', $i)\">");
			if($i == 1) {
				out("ターン${turn}(現在)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
			out("<BR>\n") if($i%3==1);
		}
	}
	my($flagDtr, $amityDtr);
	$flagDtr = 'F=艦隊編成　' if($HnavyName[0] ne '');
	$amityDtr = 'A=友好国設定' if($HuseAmity && !$HarmisticeTurn);
	out(<<END);
<span class='useNavy'>
<div align='left'>艦隊移動先(派遣先ではありません)</div>
<SELECT NAME=TARGETID2>
$HtargetList<BR>
</SELECT>
</span>
<HR>
<B>コマンド移動</B><BR>
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> ▲ </A>・・
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> ▼ </A>
</BIG>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE=submit VALUE="計画送信" NAME="CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}">
<span id="progress"></span>
<br><font size=2>最後に<span class='attention'>計画送信ボタン</span>を<br>押すのを忘れないように。</font>
</FORM>
キー入力簡易説明(NN4不可)<BR>
数字=数量　BS=一つ前削除<BR>
DEL=削除　INS=資金繰り<BR>
$flagDtr$amityDtr<BR>
</TD>
<TD $HbgMapCell>
END

	$ofname = $island->{'fleet'};
	out(<<END) if($HnavyName[0] ne '');
<FORM NAME="FLEET">
<TABLE border=0 align="center">
<TR><TH>$ofname->[0]艦隊</TH><TD><SELECT onfocus="selectFleetXY(0);" onchange="selectFleetXY(0);">@{$fleet[0]}</SELECT></TD><TD>($nFleet[0]艦)</TD></TR>
<TR><TH>$ofname->[1]艦隊</TH><TD><SELECT onfocus="selectFleetXY(1);" onchange="selectFleetXY(1);">@{$fleet[1]}</SELECT></TD><TD>($nFleet[1]艦)</TD></TR>
<TR><TH>$ofname->[2]艦隊</TH><TD><SELECT onfocus="selectFleetXY(2);" onchange="selectFleetXY(2);">@{$fleet[2]}</SELECT></TD><TD>($nFleet[2]艦)</TD></TR>
<TR><TH>$ofname->[3]艦隊</TH><TD><SELECT onfocus="selectFleetXY(3);" onchange="selectFleetXY(3);">@{$fleet[3]}</SELECT></TD><TD>($nFleet[3]艦)</TD></TR>
<TR><TH>$HtagTH_他島の艦隊$H_tagTH</TH><TD class='N' colspan=2>$ifname</TD></TR>
</TABLE>
<SCRIPT Language="JavaScript">
<!--
function selectFleetXY(n) {
	var iid;
	with (document.FLEET.elements[n]) {
		if (length < 1) { return; }
		iid = options[selectedIndex].value;
	}
	var x, y;
	n = iid.indexOf(',');
	x = iid.substring(0, n);
	y = iid.substring(n + 1, iid.length);
	with (document.myForm) {
		POINTX.options[x].selected = true;
		POINTY.options[y].selected = true;
		with (TARGETID) {
			var i;
			for (i = 0; i < length; i++) {
				if (options[i].value == $HcurrentID) {
					options[i].selected = true;
					break;
				}
			}
		}
	}
}
//-->
</SCRIPT>
</FORM>
END

	islandMarking($Hislands[$HcurrentNumber], 0);
	islandMap(1, 1, 0);	# 島の地図、所有者モード
	my $comment = $Hislands[$HcurrentNumber]->{'comment'};
	out(<<END);
<FORM NAME="LANDINFO">
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA>
</FORM>
END

	#自動系コマンド
	my($kind, $cost, $s);
	my($aa,$dd,$ff) = split(/,/,$HcommandAuto);
	out(<<END);
</TD>
<TD $HbgCommandCell id="plan" onmouseout="mc_out();return false;">
<FORM name="allForm" action="$HthisFile" method=POST>
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=MENUOPEN VALUE="allmenu">
<INPUT TYPE="hidden" NAME=MENUOPEN2 VALUE="allmenu">
<INPUT TYPE="hidden" NAME=MENUOPEN3 VALUE="allmenu">
<INPUT TYPE="hidden" NAME=TARGETID VALUE="$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="hidden" NAME=TARGETID2 VALUE="$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="hidden" NAME=NUMBER VALUE="allno">
<INPUT TYPE="hidden" NAME=POINTY VALUE="0">
<INPUT TYPE="hidden" NAME=POINTX VALUE="0"><br>
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<DIV ID='AutoCommand'><B>$aa</B><br>
<SELECT NAME=COMMAND>
END
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($dd <= $kind && $kind <= $ff){
			if($cost eq '0') {
				$cost = '無料';
			} elsif($cost =~ /^\@(.*)$/) {
				$cost = $1;
			}
			if($kind == $HdefaultKind) {
				$s = 'SELECTED';
			} else {
				$s = '';
			}
			out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
		}
	}
	out(<<END);
</SELECT><br>
<B>伐採数量</B><SELECT NAME=AMOUNT>
END

	# 数量
	foreach $i (0..99) {
		out("<OPTION VALUE=$i>$i\n");
	}

	my(@priList, $priListJS, $priSelectList);
	if($HusePriority) {
		my $mypri = $island->{'priority'};
		my($i, $j, $s);
		foreach $i (0..3) {
			$priList[$i] = '(';
			my $pFlag = 0;
			$priListJS .= '[';
			foreach (split(/\-/, $mypri->[$i])) {
				$priList[$i] .= "⇒" if($pFlag);
				$pFlag++;
				$priList[$i] .= "$HpriStr[$_]";
				$priListJS .= "$_";
				$priListJS .= ',' if($pFlag <= $#HpriStr);
			}
			$priList[$i] .= ')';
			$priListJS .= ']';
			$priListJS .= ',' if($i < 3);
		}
		$priSelectList = "";
		$i = 0;
		foreach (split(/\-/, $mypri->[$i])) {
			$priSelectList .= "<BR>　" if($i && $i % 4 == 0);
			$priSelectList .= "⇒" if($i);
			$priSelectList .= "<SELECT NAME=PS${i}>";
			foreach $j (0..$#HpriStr) {
				if($_ == $j) {
					$s = " SELECTED";
				} else {
					$s = "";
				}
				$priSelectList .= "<OPTION VALUE=${j}${s}>$HpriStr[$j]";
			}
			$priSelectList .= "</SELECT>";
			$i++;
		}
	}
	my @status = ('', '退治', '巡航', '停船');
	my($fkind) = $island->{'fkind'};
	my @flist = @$fkind;
	my @fleetlist = ();
#	my @idx = (0..$#flist);
#	@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
#	@flist = @flist[@idx];
	foreach (@flist) {
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack(hex($_));#下の小さいアイコンのとこに出てくるやつ最悪消す方向で
		next if ($HnavySpecial[$nKind] & 0x8); # 軍港は除外
		next if ($HnavyNoMove[$nKind]); # 海上防衛とかは除外
		my($s, $l) = ();
		my $navyLevel = expToLevel($HlandNavy, $nExp);
#		$s = "\n耐久力 $nHp/経験値 $nExp";
		$s = " [${status[$nStat]}]" . $s if($nStat);
		if(($eId != $id) && (defined $HidToNumber{$eId})) {
			my $name = islandName($Hislands[$HidToNumber{$eId}]);
			$name =~ s/<[^<]*>//g;
			$s .= "\n${name}へ派遣中";
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
		push(@fleetMove, " <small><B>目標地点</B>${HtagName_}${str}${H_tagName}</small>");
	}

	out(<<END);
</SELECT>×200本以上<br>
<INPUT TYPE="hidden" NAME="CommandButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="自動系計画送信">
<HR>
</DIV>
<ilayer name="PARENT_LINKMSG" width="100%" height="100%">
   <layer name="LINKMSG1" width="200"></layer>
   <span id="LINKMSG1"></span>
</ilayer>
<BR>
</FORM>
</TD></TR>
<TR><TD colspan=3 class='M'><DIV align='center'>
<TABLE BORDER><TR><TD class='M'>
END

	islandInfoWeather() if($HuseWeather); # 気象情報
	islandData(); # 拡張データ
	islandInfoSub(1) if($HnavyName[0] ne ''); # 艦艇DATA

	out(<<END);
</TD></TR></TABLE>
</DIV></TD></TR>
</TABLE>
</TD></TR><TR><TD class='M'>
<HR>
<DIV ID='CommentBox'>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<TABLE BORDER=0>
<TR>
<TH>コメント<BR><small>(全角${HlengthMessage}字まで)</small></TH>
<TD colspan=2><INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"></TD>
</TR>
<TR>
<TH>パスワード</TH><TD colspan=2><INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</TD>
</TR>
END
	
	my $sakustr = ($HusePriority ? ' 　()内は索敵順' : '');

	out(<<END) if($HnavyName[0] ne '');
<TR>
</FORM>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH colspan=3>艦隊名変更<small>(全角${HlengthFleetName}字まで)</small>$sakustr</TH></TR>
<TR><TH>第１艦隊</TH><TD class='C' colspan=2>$fleetlist[0]<br><INPUT TYPE=text NAME=FLEET1 SIZE=20 VALUE="$ofname->[0]">艦隊$fleetMove[0] $priList[0]</TD></TR>
<TR><TH>第２艦隊</TH><TD class='C' colspan=2>$fleetlist[1]<br><INPUT TYPE=text NAME=FLEET2 SIZE=20 VALUE="$ofname->[1]">艦隊$fleetMove[1] $priList[1]</TD></TR>
<TR><TH>第３艦隊</TH><TD class='C' colspan=2>$fleetlist[2]<br><INPUT TYPE=text NAME=FLEET3 SIZE=20 VALUE="$ofname->[2]">艦隊$fleetMove[2] $priList[2]</TD></TR>
<TR><TH>第４艦隊</TH><TD class='C' colspan=2>$fleetlist[3]<br><INPUT TYPE=text NAME=FLEET4 SIZE=20 VALUE="$ofname->[3]">艦隊$fleetMove[3] $priList[3]</TD></TR>
<TR><TD colspan=3 align=center><INPUT TYPE=submit VALUE="艦隊名変更" NAME=FleetnameButton$Hislands[$HcurrentNumber]->{'id'}></TD></TR>
END

	if($HusePriority) {
		out(<<END);
<TR>
</FORM>
<SCRIPT Language="JavaScript">
<!--
function priorityChange() {
	data=[$priListJS];
	document.priorityForm.PS0.value = data[document.priorityForm.PSF.value][0];
	document.priorityForm.PS1.value = data[document.priorityForm.PSF.value][1];
	document.priorityForm.PS2.value = data[document.priorityForm.PSF.value][2];
	document.priorityForm.PS3.value = data[document.priorityForm.PSF.value][3];
	document.priorityForm.PS4.value = data[document.priorityForm.PSF.value][4];
	document.priorityForm.PS5.value = data[document.priorityForm.PSF.value][5];
	document.priorityForm.PS6.value = data[document.priorityForm.PSF.value][6];
	document.priorityForm.PS7.value = data[document.priorityForm.PSF.value][7];
	return true;
}
function resetPriority() {
	document.priorityForm.PS0.value = 0;
	document.priorityForm.PS1.value = 1;
	document.priorityForm.PS2.value = 2;
	document.priorityForm.PS3.value = 3;
	document.priorityForm.PS4.value = 4;
	document.priorityForm.PS5.value = 5;
	document.priorityForm.PS6.value = 6;
	document.priorityForm.PS7.value = 7;
	return true;
}
//-->
</SCRIPT>
<FORM name="priorityForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH>索敵順変更</TH><TD><SELECT NAME=PSF onChange=priorityChange() onClick=priorityChange()>
END
		foreach (0..3) {
			out("<OPTION VALUE=$_>$ofname->[$_]\n");
		}
	out(<<END);
</SELECT>艦隊　</TD><TD>
$priSelectList
<INPUT TYPE=submit VALUE="変更" NAME=PriorityButton$Hislands[$HcurrentNumber]->{'id'}>
<small>[<a href="javascript:void(0);" onClick="resetPriority();">初期化</a>]</small>
</TD>
END
	}

	my($earth);
	if($HroundView == 2) {
		my $earthstr = ($island->{'earth'} ? '周辺表示<B><FONT COLOR="#FF0000">する</FONT></B>' : '周辺表示<B><FONT COLOR="#0000FF">しない</FONT></B>');
		$earth = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>周辺表示設定</TH><TD colspan=2>$earthstr<INPUT TYPE=submit VALUE=\"変更\" NAME=EarthButton$island->{'id'}></TD></TR>";
	}

	my($comflag);
	if($HcomflagUse >= 2) {
		my $comflagstr = ($island->{'comflag'} ? 'なくても' : 'なければ');
		my $comflagtmp = ($island->{'comflag'} ? '<FONT COLOR="#FF0000">しない</FONT>' : '<FONT COLOR="#0000FF">する</FONT>');
		$comflag = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>コマンド実行設定</TH><TD colspan=2>コマンドが実行でき${comflagstr}、予定ターンを繰り上げて実行<B>$comflagtmp</B><INPUT TYPE=submit VALUE=\"変更\" NAME=ComflagButton$island->{'id'}></TD></TR>";
	}

	my($preab);
	if($HarmisticeTurn && $HuseCoDevelop) {
		my $preabstr = ($island->{'preab'} ? 'なくても' : 'なければ');
		my $preabtmp = ($island->{'preab'} ? '<FONT COLOR="#FF0000">許可する</FONT>' : '<FONT COLOR="#0000FF">許可しない</FONT>');
		$preab = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>陣営共同開発</TH><TD colspan=2>陣営預かりで${preabstr}、陣営パスワードで開発画面に入ることを<B>$preabtmp</B><INPUT TYPE=submit VALUE=\"変更\" NAME=PreabButton$Hislands[$HcurrentNumber]->{'id'}></TD></TR>";
	}
	out(<<END);
$earth
$comflag
$preab
</TABLE>
</FORM>
</DIV>
</TD></TR></TABLE></DIV>
END

}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
sub commandJavaMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# モードで分岐
	my($command) = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
		# コマンド登録
		$HcommandComary =~ s/([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) //;
		my $kind = $1;
		if($kind == 0) {
			$kind = $HcomDoNothing ;
		} elsif($kind == $HcomGiveup) {
			if(!checkSpecialPassword($HinputPassword) && (encode($HinputPassword) ne $island->{'password'})) {
				$i--;
				next;
			}
		}
		my $arg = $4;
		$arg = 99 if($arg > 99);
		$command->[$i] = {
			'kind' => $kind,
			'x' => $2,
			'y' => $3,
			'arg' => $arg,
			'target' => $5,
			'target2' => $6
		};
	}

	# データの書き出し
	writeIslandsFile($HcurrentID);

	if($Hasync) {
		unlock();
		out("OKsenddatacomplete");
	} else {
		tempCommandAdd();
		# owner modeへ
		ownerMain();
	}
}

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
sub printIslandJava {
	# 開放
	unlock();

	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	$island = $Hislands[$HcurrentNumber];

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# 名前の取得
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# 艦隊構成を調べる・マップデータ取得・軍港データ取得
	my($x, $y, $nKind, $value);
	my $setmap = '';
	my @x = (!$HoceanMode) ? @{$island->{'map'}->{'x'}} : @defaultX;
	my @y = (!$HoceanMode) ? @{$island->{'map'}->{'y'}} : @defaultY;
	foreach $y (@y) {
		$setmap .= '[';
		foreach $x (@x) {
			if($HoceanMode && ($HlandID[$x][$y] != $island->{'id'})) {
				# 領海でない
				$setmap .= '-2,';
				next;
			} else {
				$setmap .= '1,';
			}
		}
		substr($setmap, -1) = '';
		$setmap .= "],\n";
	}
	substr($setmap, -1) = '';

	#コマンドリストセット
	my($l_kind);
	@click_com = ();
	if($HjavaMode eq 'java'){
		$com_count = @HcommandDivido;
		for($m = 0; $m < $com_count; $m++) {
			($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
			for($i = 0; $i < $HcommandTotal; $i++) {
				$l_kind = $HcomList[$i];
				$l_cost = $HcomCost[$l_kind];
				if($l_cost eq '0') {
					$l_cost = '無料';
				} elsif($l_cost =~ /^\@(.*)$/) {
					$l_cost = $1;
				} else {
					$l_cost .= $HunitMoney;
				}
				if($l_kind >= $dd && $l_kind <= $ff) {
					if(($m == 5) || ($m == 8)){
						# 他島に対しては実行できないコマンド
						next if(($l_kind == $HcomNavyForm) ||
								($l_kind == $HcomNavyExpell) ||
#								($l_kind == $HcomNavyDestroy) ||
								($l_kind == $HcomNavyWreckRepair) ||
								($l_kind == $HcomNavyWreckSell) ||
                                                                ($l_kind == $Hcomremodel) ||
								($l_kind == $Hcomshikin));
						my($l_name) = ($HcomTurn[$l_kind] > 0) ? "$HtagComName1_${HcomName[$l_kind]}$H_tagComName" : "$HtagComName2_${HcomName[$l_kind]}$H_tagComName";
						$click_com[$m] .= "<a title='$l_cost' onMouseOver='StatusMsg($l_kind);' onClick='window.opener.cominput(window.opener.document.myForm,6,$l_kind)' STYlE='text-decoration:none;cursor:pointer;'>$l_name</a><br>\n";
					}
				}
			}
		}
	}
	$click_com[5] .= "<hr>" if($click_com[8] ne '');
		# 艦艇移動
		$click_com[3] = <<"END";
<TABLE BORDER=0 class="PopupCell">
<TR><TH colspan=2></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,17)' class='M'>11時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,18)' class='M'>12時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,7)' class='M'>１時</a></TH><TH colspan=2></TH></TR>
<TR><TH></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,16)' class='M'>10時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,6)' class='M'>左上</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,1)' class='M'>右上</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,8)' class='M'>２時</a></TH><TH></TH></TR>
<TR><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,15)' class='M'>９時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,5)' class='M'> 左 </a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,0)' class='M'>待機</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,2)' class='M'> 右 </a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,9)' class='M'>３時</a></TH></TR>
<TR><TH></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,14)' class='M'>８時</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,4)' class='M'>左下</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,3)' class='M'>右下</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,10)' class='M'>４時</a></TH><TH></TH></TR>
<TR><TH colspan=2></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,13)' class='M'>７時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,12)' class='M'>６時</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,11)' class='M'>５時</a></TH><TH colspan=2></TH></TR>
</TABLE>
END
		$click_com[4] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,0)' class='M'>通常</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,1)' class='M'>退治</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,2)' class='M'>巡航</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,3)' class='M'>停船</a></TH>
</TR>
</TABLE>
END

	# 艦隊移動ポップアップメニューセット
	$click_com[9] = '';
	my($l_name, $l_id);
	$set_island = "";
	foreach $i (0..$islandNumber) {
		$l_name = islandName($Hislands[$i]);
		$l_name =~ s/<[^<]*>//g;
		$l_name =~ s/'/\\'/g;
		$l_id = $Hislands[$i]->{'id'};
		$click_com[9] .="<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,8,$l_id)' STYlE='text-decoration:none;'>$l_name</a><br>\n";
	}
	substr($click_com[9], -5) = "\n";
	if($Htournament){
		# トーナメント
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		my $id = $island->{'id'};
		if($island->{'fight_id'} < 1){
			# 無し
			$click_com[9] ="<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}else{
			# 有り
			my $fight_id = $island->{'fight_id'};
			$click_com[9] ="<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,8,$fight_id)' STYlE='text-decoration:none;'>${tName}</a><BR>\n";
			$click_com[9] .="<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}
	}

	out(<<END);
<SCRIPT Language="JavaScript">
<!--
var mapX = $island->{'map'}->{'x'}[0];
var mapY = $island->{'map'}->{'y'}[0];
mapdata = [
$setmap
];

$HpopupNaviJS

if(document.getElementById){
	document.onmousemove = Mmove;
} else if(document.layers){
	window.captureEvents(Event.MOUSEMOVE);
	window.onMouseMove = Mmove;
} else if(document.all){
	document.onmousemove = Mmove;
}

if((document.layers) || (document.all)){  // IE4、IE5、NN4
	window.document.onmouseup = menuclose;
}
function sv(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	if($HpopupNavi) {
		NaviClose();
	}
	status = '';
	return false;
}
function ps(x, y) {
	if($HpopupNavi) {
		NaviClose();
	}
	var java = '$HjavaMode';
		window.opener.document.myForm.POINTX.options[x].selected = true;
		window.opener.document.myForm.POINTY.options[y].selected = true;
		with (window.opener.document.myForm.TARGETID) {
			var i;
			for (i = 0; i < length; i++) {
				if (options[i].value == $HcurrentID) {
					options[i].selected = true;
					break;
				}
			}
		}
	if(document.mark_form.mark.checked) {
		set_mark(x, y);
	} else if(document.myForm.MENUOPEN3.checked) {
		if(java == 'java')moveLAYER("menu3",mx,my);
	} else if(document.myForm.MENUOPEN2.checked) {
		if(java == 'java')moveLAYER("menu2",mx,my);
	} else {
		if(java == 'java')moveLAYER("menu",mx,my);
	}
	return true;
}

function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		if(document.all){				//IE5
			el = document.getElementById(layName);
			el.style.left= event.clientX + document.body.scrollLeft + 10;
			el.style.top= event.clientY + document.body.scrollTop - 30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}else{
			el = document.getElementById(layName);
			el.style.left=x+10;
			el.style.top=y-30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}
	} else if(document.layers){				//NN4
		msgLay = document.layers[layName];
		msgLay.moveTo(x+10,y-30);
		msgLay.visibility = "show";
	} else if(document.all){				//IE4
		msgLay = document.all(layName);
		msgLay.style.pixelLeft = x+10;
		msgLay.style.pixelTop = y-30;
		msgLay.style.display = "block";
		msgLay.style.visibility = "visible";
	}

}

function menuclose(){
	if (document.getElementById){
		document.getElementById("menu").style.display = "none";
		document.getElementById("menu2").style.display = "none";
		document.getElementById("menu3").style.display = "none";
	} else if (document.layers){
		document.menu.visibility = "hide";
		document.menu2.visibility = "hide";
		document.menu3.visibility = "hide";
	} else if (document.all){
		window["menu"].style.display = "none";
		window["menu2"].style.display = "none";
		window["menu3"].style.display = "none";
	}
}

function Mmove(e){
	if(document.all){
		mx = event.x;
		my = event.y;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}
}

function check_menu2(){
	if(document.myForm.MENUOPEN2.checked){
		if(document.myForm.MENUOPEN3.checked) { document.myForm.MENUOPEN3.checked = false; }
		if(document.mark_form.mark.checked)   { document.mark_form.mark.checked = false; }
	}
}

function check_menu3(){
	if(document.myForm.MENUOPEN3.checked){
		if(document.myForm.MENUOPEN2.checked) { document.myForm.MENUOPEN2.checked = false; }
		if(document.mark_form.mark.checked)   { document.mark_form.mark.checked = false; }
	}
}

function set_land(x, y, land, img) {
	com_str = land + "\\n";
	if($oroti) { img = '${baseIMG}/' + img; }
	document.POPUP1.COMSTATUS.value= com_str;
	document.POPUP1.NAVIIMG.src= img;
	document.POPUP2.COMSTATUS.value= com_str;
	document.POPUP2.NAVIIMG.src= img;
	document.POPUP3.COMSTATUS.value= com_str;
	document.POPUP3.NAVIIMG.src= img;
}

function StatusMsg(x) {
msg = new Array(64);
END
	my($i ,$k);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$k = $HcomList[$i];
		my($Msg) = $HcomMsgs[$k];
		out("msg[$k] = \"$Msg\";\n");
	}
	out(<<END);
	window.status = msg[x];
}
//-->
</SCRIPT>
<DIV ID='targetMap'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}${H_tagBig}<br>
攻撃する地点をクリックして下さい。<br>クリックした地点が開発画面の座標に設定されます。
<FORM name="myForm">
<INPUT TYPE="hidden" NAME="MENUOPEN">
<INPUT TYPE="checkbox" NAME="MENUOPEN2" onClick="check_menu2()" class='useFlag'><span class='useFlag'>移動操縦</span>
<INPUT TYPE="checkbox" NAME="MENUOPEN3" onClick="check_menu3()" class='UseNavy'><span class='useNavy'>艦隊移動</span>
</FORM>
END

	islandMarking($island, $HmissileMode);
	out(<<END);
<DIV ID="menu3" style="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD class='T'>
<FORM name='POPUP3'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR><TD><DIV style="overflow:auto; height:150px;">
$click_com[9]
</DIV></TD></TR>
<TR><TD class='T'>
<small>
<span class='attention'>！艦隊番号を確認して下さい！</span><br>
「数量」で艦隊番号を指定してから<br>
移動させたい$AfterName名をクリック
</small>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
<DIV ID="menu2" style="position:absolute; visibility:hidden;">
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD class='T'>
<FORM name='POPUP2'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR><TD><DIV align='center'>
$click_com[3]</DIV>
</TD></TR>
<TR><TD class='T'>
<small>
<span class='attention'>！艦艇の能力を確認して下さい！</span><br>
艦艇操作=>「移動操縦(旗艦)」<br>
2Hex移動=>「移動が(とても)速い」
</small>
</TD></TR>
<TR><TD align='center'>
${HtagTH_}指令変更${H_tagTH}$click_com[4]
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
END

	out(<<END);
<DIV ID="menu" style="position:absolute; visibility:hidden;"> 
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD class='T'>
<FORM name='POPUP1'>
<IMG NAME="NAVIIMG" SRC="" width=${\($HchipSize*2)} height=${\($HchipSize*2)} align="left">
<TEXTAREA NAME="COMSTATUS" cols="10" rows="2" class="popupnavi"></TEXTAREA>
</TD></TR>
</FORM>
<TR><TD>
$click_com[5]
$click_com[8]
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</TD></TR>
</TABLE>
</DIV>
END
	if(checkPassword($island, $HdefaultPassword) && $island->{'id'} eq $defaultID) {
		islandMap(1, 1, $HmissileMode);  # 島の地図、観光モード
#		templandStringFlash(1); # 擬似ＭＡＰデータ表示
	}else{
		if($island->{'field'}) {
			islandMap(1, 1, $HmissileMode); # 島の地図、観光モード
		} else {
			islandMap(0, 1, $HmissileMode); # 島の地図、観光モード
		}
#		templandStringFlash(0); # 擬似ＭＡＰデータ表示
	}
	if($HmlogMap && $HmissileMode) {
		out(<<END);
<DIV align='center'>
<TABLE class="DamageCell" BORDER><TR>
<TH>${HtagDisaster_}着弾点${H_tagDisaster}</TH><TH>無効</TH><TH>防衛</TH><TH>硬化or潜水</TH><TH>命中</TH>
</TR><TR>
<TH>${HcurrentName}の攻撃</TH><TH><span class='nodamage'>★</span></TH><TH><span class='defence'>★</span></TH><TH><span class='harden'>★</span></TH><TH><span class='hitpoint'>★</span></TH>
</TR><TR>
<TH>他${AfterName}の攻撃</TH><TH><span class='nodamage'>●</span></TH><TH><span class='defence'>●</span></TH><TH><span class='harden'>●</span></TH><TH><span class='hitpoint'>●</span></TH>
</TR></TABLE>
<HR>
END
		my $i;
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=\"$HthisFile?IslandMap=$island->{'id'}&JAVAMODE=$HjavaMode&MISSILEMODE=$i\">");
			if($i == 1) {
				out("ターン${turn}(現在)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
		}
		out("</DIV>\n");

		# 着弾マップと同じターンのログを表示（不要ならコメントアウト）
		#logFilePrint($HmissileMode-1, $island->{'id'}, $mode);
	}

	# ○○島ローカル掲示板
#	if($HuseLbbs) {
		#require('./hako-lbbs.cgi');
		#tempLbbsContents(); # 掲示板内容
		#重くなるので表示させない。表示する場合は、#tempLbbs・・の#を取る。
#	}
	# 外部掲示板
#	if($HuseExlbbs) {
#		if($island->{'password'} eq encode($HdefaultPassword) && ($island->{'id'} eq $defaultID)) {
#			exLbbs($island->{'id'}, 1);
#		}else{
#			exLbbs($island->{'id'}, 0);
#		}
#	}

	# 近況
	out("</DIV>");
	tempRecent(0, $HuseHistory2);
}

sub templandStringFlash {
	my($mode) = @_;
	require './hako-js.cgi';
	landStringFlash($mode); # 擬似ＭＡＰデータ表示
}
#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン
sub printIslandMain {
	# 開放
	unlock();
	if($HadminMode && !checkSpecialPassword($HdefaultPassword)) {
			tempWrongPassword();
			return;
	}
	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# 名前の取得
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# 観光画面
	if($HadminMode) {
		tempPrintIslandHead($island, 1); # ようこそ!!
	} else {
		tempPrintIslandHead($island, 0); # ようこそ!!
	}
	islandInfo(0); # 島の情報
	if(!$HadminMode && $Hislands[$HcurrentNumber]->{'field'}) {
		islandMap(2, 0, 0); # 島の地図、観光モード
	} else {
		islandMap($HadminMode, 0, 0); # 島の地図、観光モード
	}
	islandJamp();   # 島の移動

	islandInfoWeather() if($HuseWeather); # 気象情報
	islandData(); # 拡張データ
	islandInfoSub((!$Hislands[$HcurrentNumber]->{'field'}) ? 1 : 0) if($HnavyName[0] ne ''); # 艦艇データ

	# ○○島ローカル掲示板
	if($HuseLbbs) {
		require('./hako-lbbs.cgi');
		tempLbbsMain(0);
	}
	if($HuseExlbbs) { # 外部掲示板
		exLbbs($HcurrentID, 0) ;
	}

	# 近況
	tempRecent(0, $HuseHistory2);
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン
sub ownerMain {
	# 開放
	unlock();

	# モードを明示
	$HmainMode = 'owner';

	if($HcurrentID eq '') {
		tempProblem();
		return;
	}

	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# パスワード(実は不要。念のため残している)
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		return;
	}

	if($Htournament){
		# トーナメント
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		if($island->{'fight_id'} < 1){
			# 無し
			$HtargetList = "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
		}else{
			# 有り
			$HtargetList = "<OPTION VALUE=\"$island->{'fight_id'}\">${tName}\n";
			$HtargetList .= "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
			#$defaultTarget = $island->{'fight_id'} if($defaultTarget != $HcurrentID && $defaultTarget != $island->{'fight_id'});
		}
	}

	# 開発画面
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # 「Javaスクリプト開発計画」
	}else{
		tempOwner();     # 「通常モード開発計画」
	}

	# ○○島ローカル掲示板
	if($HuseLbbs) {
		require('./hako-lbbs.cgi');
		tempLbbsMain(1); # ローカル掲示板
	}
	if($HuseExlbbs) { # 外部掲示板
		exLbbs($HcurrentID, 1) ;
	}

	# 近況
	tempRecent(1, $HuseHistory1);
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン
sub commandMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# パスワード
	if(($HcommandKind == $HcomGiveup) && ($HcommandMode ne 'delete')) {
		if(!checkSpecialPassword($HinputPassword) && (encode($HinputPassword) ne $island->{'password'})) {
			# owner modeへ
			ownerMain();
			return;
		}
	} elsif(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	commandAdd($island);

	# owner modeへ
	ownerMain();
}

# コマンド登録
sub commandAdd {
	my $island = shift;
	# モードで分岐
	my($command) = $island->{'command'};

	my($i, $j) = (0, 0);
	my($x, $y);
	# 座標配列を作る
	makeRandomIslandPointArray($island);
	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# フル整地、フル地ならし
		my($land) = $island->{'land'};

		# コマンドの種類決定
		my($kind) = $HcomPrepare;
		if($HcommandKind == $HcomAutoPrepare2) {
			$kind = $HcomPrepare2;
		}

		while(($j <= $island->{'pnum'}) && ($i < $HcommandMax)) {
			$x = $island->{'rpx'}[$j];
			$y = $island->{'rpy'}[$j];
			if($land->[$x][$y] == $HlandWaste) {
				slideBack($command, $HcommandPlanNumber);
				$command->[$HcommandPlanNumber] = {
					'kind' => $kind,
					'target' => 0,
					'x' => $x,
					'y' => $y,
					'arg' => 0,
					'target2' => 0
				};
				$i++;
			}
			$j++;
		}
		tempCommandAdd();
	} elsif(($HcommandKind == $HcomAutoReclaim) ||
			($HcommandKind == $HcomAutoDestroy)) {
		# 浅瀬埋め立て、浅瀬掘削
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		# コマンドの種類決定
		my($kind) = $HcomReclaim;
		if($HcommandKind == $HcomAutoDestroy) {
			$kind = $HcomDestroy;
		}
		while(($j <= $island->{'pnum'}) && ($i < $HcommandMax)) {
			$x = $island->{'rpx'}[$j];
			$y = $island->{'rpy'}[$j];
			if (($land->[$x][$y] == $HlandSea) && ($landValue->[$x][$y] == 1)) {
				slideBack($command, $HcommandPlanNumber);
				$command->[$HcommandPlanNumber] = {
					'kind' => $kind,
					'target' => 0,
					'x' => $x,
					'y' => $y,
					'arg' => 0,
					'target2' => 0
				};
				$i++;
			}
			$j++;
		}
		tempCommandAdd();
	} elsif(($HcommandKind == $HcomAutoSellTree) ||
			($HcommandKind == $HcomAutoForestry)) {
		# 伐採、伐採と植林
		# （数量×２００本より多い森だけが対象）
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		# コマンドの種類決定
		my($kind) = ($HcommandKind == $HcomAutoForestry) ? 1 : 0;
		while(($j <= $island->{'pnum'}) && ($i < $HcommandMax)) {
			$x = $island->{'rpx'}[$j];
			$y = $island->{'rpy'}[$j];
			if (($land->[$x][$y] == $HlandForest) && ($landValue->[$x][$y] > $HcommandArg * 2)) {
				if($kind) {
					slideBack($command, $HcommandPlanNumber);
					$command->[$HcommandPlanNumber] = {
						'kind' => $HcomPlant,
						'target' => 0,
						'x' => $x,
						'y' => $y,
						'arg' => 0,
						'target2' => 0
					};
					$i++;
				}
				slideBack($command, $HcommandPlanNumber);
				$command->[$HcommandPlanNumber] = {
					'kind' => $HcomSellTree,
					'target' => 0,
					'x' => $x,
					'y' => $y,
					'arg' => 0,
					'target2' => 0
				};
				$i++;
			}
			$j++;
		}
		tempCommandAdd();
	} elsif($HcommandKind == $HcomAutoDelete) {
		# 全消し
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		tempCommandDelete();
	} else {
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		tempCommandAdd();
		# コマンドを登録
		my $kind = $HcommandKind;
		$kind = $HcomDoNothing if($kind == 0);
		my $arg = $HcommandArg;
		$arg = 99 if($arg > 99);
		$command->[$HcommandPlanNumber] = {
			'kind' => $kind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $arg,
			'target2' => $HcommandTarget2
		};
	}

	$HcommandPlanNumber++ if ($HcommandPlanNumber + 1 < $HcommandMax);

	# データの書き出し
	writeIslandsFile($HcurrentID);
}

#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン
sub commentMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# メッセージを更新
	$island->{'comment'} = htmlEscape($Hmessage);

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# コメント更新メッセージ
	tempComment();

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# 艦隊名変更モード
#----------------------------------------------------------------------
# メイン
sub fleetnameMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 艦隊名を更新
	my @fleetname;
	$fleetname[0] = htmlEscape($HfleetName[0]);
	$fleetname[1] = htmlEscape($HfleetName[1]);
	$fleetname[2] = htmlEscape($HfleetName[2]);
	$fleetname[3] = htmlEscape($HfleetName[3]);
	$island->{'fleet'} = \@fleetname;

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# コメント更新メッセージ
	tempFleetName();

	# owner modeへ
	ownerMain();
}

sub priorityMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 索敵順を更新
	my $mypri = $island->{'priority'};
	foreach (0..3) {
		if($_ == $HfleetNumber) {
			$mypri->[$_] = $HfleetPriority;
		}
	}
	$island->{'priority'} = $mypri;

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# 更新メッセージ
	tempPriority();

	# owner modeへ
	ownerMain();
}

sub earthMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 周辺表示設定フラグを変更
	$island->{'earth'} ^= 1;

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();
}

sub comflagMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# コマンド実行設定フラグを変更
	$island->{'comflag'} ^= 1;

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();
}

sub preabMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# パスワード
	if(!checkPassword($island,$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 陣営共同開発フラグを変更
	$island->{'preab'} ^= 1;

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
	my($mode) = @_;

	my($island) = $Hislands[$HcurrentNumber];
	# 情報表示
	my($rank) = $HcurrentNumber + 1 - $HbfieldNumber;
	my($pop) = ($island->{'pop'} == 0) ? "無人" : "$island->{'pop'}$HunitPop";
	1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($food) = ($island->{'food'} == 0) ? "備蓄ゼロ" : "$island->{'food'}$HunitFood";
	1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
                # 追加
                $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
                $foodrate .= '億円/10000トン';
	my($farm) = ($island->{'farm'} == 0) ? "保有せず" : "$island->{'farm'}0$HunitPop";
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($factory) = ($island->{'factory'} == 0) ? "保有せず" : "$island->{'factory'}0$HunitPop";
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($mountain) = ($island->{'mountain'} == 0) ? "保有せず" : "$island->{'mountain'}0$HunitPop";
	1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($area) = $island->{'area'};
	if($area > $HdisFallBorder) {
		$area = "${HtagDisaster_}$area$HunitArea${H_tagDisaster}";
	} elsif($area == $HdisFallBorder) {
		$area = "<span class='attention'>$area$HunitArea</span>";
	} elsif(!$area) {
		$area = "なし";
	} else {
		$area .= $HunitArea;
	}
	1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($sea) = calcSea($island);
	if($HnoDisFlag) {
		if($sea) {
			$sea .= $HunitArea;
		} else {
			$sea = "なし";
		}
	} elsif(!$sea) {
		$sea = "<span class='attention'>なし</span>";
	} elsif(($island->{'pnum'} + 1 - 8*8 - $HdisTsunamiFsea) && $sea <= int(($island->{'pnum'} + 1 - 8*8 - $HdisTsunamiFsea)/2)) {
		$sea = "<span class='attention'>$sea$HunitArea</span>";
	} elsif($sea <= $HdisTsunamiFsea) {
		$sea = "${HtagDisaster_}$sea$HunitArea${H_tagDisaster}";
	} else {
		$sea .= $HunitArea;
	}
	1 while $sea =~ s/(.*\d)(\d\d\d)/$1,$2/;

	my($mStr1) = '';
	my($mStr2) = '';
	my $col = 8;
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner') || $island->{'field'}) {
		# 無条件またはownerモードまたはBattleField
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>";
		my($money) = ($island->{'money'} == 0) ? "資金ゼロ" : "$island->{'money'}$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mStr2 = "<TD $HbgInfoCell align=right>$money</TD><TD $HbgInfoCell align=right>$food</TD>";
		$col++;
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		1 while $mTmp =~ s/(.*\d)(\d\d\d)/$1,$2/;

		# 1000億単位モード
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>";
		$mStr2 = "<TD $HbgInfoCell align=right>$mTmp</TD>";
		$col++;
	}
	my($bStr) = '';
	my($rStr1) = '';
	my($rStr2) = '';
	if(!$island->{'field'}) {
		# 順位
		$rStr1 = "<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>";
		$rStr2 = "<TD $HbgNumberCell align=middle>${HtagNumber_}$rank${H_tagNumber}</TD>";
	} else {
		$bStr = "<TR><TH COLSPAN=11><FONT size='5'>${HtagTH_}Battle Field${H_tagTH}</FONT></TH></TR>";
	}
	my $navyComLevel = gainToLevel($island->{'gain'});
	my $totalExp = $island->{'gain'};
	1 while $totalExp =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$totalExp .= "(Lv.${navyComLevel})" if($HmaxComNavyLevel);
	out(<<END);
<DIV ID='islandInfo'>
<TABLE BORDER>
$bStr
<TR>
$rStr1
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}食料レート${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}農場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総獲得経験値${H_tagTH}</TH>
</TR>
<TR>
$rStr2
<TD $HbgInfoCell align=right>$pop</TD>
$mStr2
<TD $HbgInfoCell align=right>$foodrate</TD>
<TD $HbgInfoCell align=right> $area <B>陸地</B><BR> $sea <B>深海</B></TD>
<TD $HbgInfoCell align=right>${farm}</TD>
<TD $HbgInfoCell align=right>${factory}</TD>
<TD $HbgInfoCell align=right>${mountain}</TD>
<TD $HbgInfoCell align=right>${totalExp}</TD></TR>
END

	if($HuseAmity && !$HarmisticeTurn&& !$Htournament) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}友好国${H_tagTH}</TH>
<TD colspan="$col" class='C'>
END

		my $amity = $island->{'amity'};
		my $ami;
		foreach $ami (@$amity) {
			next unless(defined $HidToNumber{$ami});
			my($name);
			$name = islandName($Hislands[$HidToNumber{$ami}]) if(defined $HidToNumber{$ami});
			out("<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${ami}\" target=\"_blank\">${name}</A> ");
		}
		out("　") unless(defined $ami);
		out("</TD></TR>");
	}

	my $AllyBBS = '<TABLE BORDER cellpadding=0 cellspacing=0><TR>';
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
			my $allyId  = $Hally[$i]->{'id'};
			my $cpass = $ally->{'password'};
			my $jpass = $ally->{'Takayan'};
			my $set_name = $HcurrentName;
			$set_name =~ s/<FONT COLOR=\"[\w\#]+\"><B>(.*)<\/B><\/FONT>/$1/g;
			$set_name =~ s/<[^<]*>//g;
			$set_name =~ s/\r//g;
			my $allyName = $ally->{'name'};
			$allyName =~ s/【勝者！】//g;
			$aNo += $i;
			my $campInfo = '';
			$campInfo .=<<_CAMP_ if($mode && $HarmisticeTurn);
　[<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm${aNo}.action='${HthisFile}';document.allyForm${aNo}.submit();return false;">作戦本部</A>]&nbsp;&nbsp;
_CAMP_
			$campInfo .=<<_CAMP_ if($mode);
<FORM name="allyForm$aNo" action="" method="POST" target="_blank">
<INPUT type=hidden name="camp" value="$allyId">
<INPUT type=hidden name="ally" value="$allyId">
<INPUT type=hidden name="cpass" value="$cpass">
<INPUT type=hidden name="jpass" value="$jpass">
<INPUT type=hidden name="id" value="$island->{'id'}">
</TD>
</FORM>
_CAMP_

			if($mode && $HallyBbs) {
# 同盟掲示板へのリンクを同盟名でなく「作戦会議室」にしたい場合、下の'$HarmisticeTurn'を'1'に書き換えればよい。
				if($HarmisticeTurn) {
					$AllyBBS .=<<_BBS_;
<TD class='M'>
<FONT COLOR="$ally->{'color'}"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}
　[<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm${aNo}.action='${HbaseDir}/${HallyBbsScript}';document.allyForm${aNo}.submit();return false;">作戦会議室</A>]
${campInfo}
_BBS_
				} else {
					$AllyBBS .=<<_BBS_;
<TD class='M'>
<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm${aNo}.action='${HbaseDir}/${HallyBbsScript}';document.allyForm${aNo}.submit();return false;">
<FONT COLOR="$ally->{'color'}"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}</A>${campInfo}
_BBS_
				}
			} else {
				$AllyBBS .=<<_BBS_;
<TD class='M'>
<FONT COLOR="$ally->{'color'}"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}${campInfo}
_BBS_
			}
		}
		$AllyBBS .= '</TR></TABLE>';
	}

	my $allytitle = $HarmisticeTurn ? '陣営' : '同盟';
	out(<<END) if($HallyNumber);
<TR>
<TH $HbgTitleCell>${HtagTH_}${allytitle}${H_tagTH}</TH>
<TD colspan="$col" class='C'>${AllyBBS}</TD></TR>
END

	if($HuseDeWar && !$HarmisticeTurn && !$HsurvivalTurn && !$Htournament) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}交戦国${H_tagTH}</TH>
<TD colspan="$col" class='C'>
END
		my $warName;
		for($i=0;$i < $#HwarIsland;$i+=4){
			my($id1, $id2, $flag) = ($HwarIsland[$i+1], $HwarIsland[$i+2], $HwarIsland[$i+3]);
			my($tn1) = $HidToNumber{$id1};
			next if($tn1 eq '');
			my($tn2) = $HidToNumber{$id2};
			next if($tn2 eq '');
			my($name1,$name2) = (islandName($Hislands[$tn1]), islandName($Hislands[$tn2]));
			my $turn = $HwarIsland[$i];
			$turn .= '〜' if($turn < $HislandTurn);
			$turn = 'ターン' . $turn;
			my($f, $fturn) = ($flag % 10, int($flag / 10) + $HdeclareTurn);
			my($flag1, $flag2) = ('', '');
			if($f == 1) {
				($flag1, $flag2) = ("[停戦打診中:$fturn]", "[停戦打診あり:$fturn");
				$flag2 .= (!$mode) ? ']' : " <a href='javascript:void(0);' onClick='cominput(myForm,10,$id1)'>合意</a> <a href='javascript:void(0);' onClick='cominput(myForm,11,$id1)'>破棄</a>]";
			} elsif($f == 2) {
				($flag1, $flag2) = ("[停戦打診あり:$fturn", "[停戦打診中:$fturn]");
				$flag1 .= (!$mode) ? ']' : " <a href='javascript:void(0);' onClick='cominput(myForm,10,$id2)'>合意</a> <a href='javascript:void(0);' onClick='cominput(myForm,11,$id2)'>破棄</a>]";
			}
			if($island->{'id'} == $id1){
				$warName .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${id2}\" target=\"_blank\">${name2}</A>($turn$flag1) ";
			}elsif($island->{'id'} == $id2){
				$warName .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${id1}\" target=\"_blank\">${name1}</A>($turn$flag2) ";
			}
		}
		$warName = "　" unless(defined $warName);
		out("$warName</TD></TR>");
	}

	$col++;
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(あと$island->{'predelete'}ターン)</small>" : '';
		out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"\>${HtagDisaster_}管理人あずかり${H_tagDisaster}によりターン更新停止中$rest</TH></TR>");
	} elsif($Htournament) {
		if($island->{'fight_id'} > 0) {
			my $cn = $HidToNumber{$island->{'fight_id'}};
			if($cn ne '') {
				my $tIsland = $Hislands[$cn];
				my $name = islandName($tIsland);
				$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$tIsland->{'id'}\" target=\"_blank\">$name</A>";
				out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"><B>対戦相手は$nameです</B></TH></TR>");
			}
		} elsif($island->{'rest'} && ($HislandNumber > 1)) {
			out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"\>不戦勝により開発停止中　残り${HtagDisaster_}$island->{'rest'}${H_tagDisaster}ターン</TH></TR>");
		}
	} elsif($island->{'event'}[0]) {
		my $flag = 0;
		my $type  = $HeventName[$island->{'event'}[6]];
		if(($island->{'event'}[1] - $HnoticeTurn <= $HislandTurn) && ($HislandTurn < $island->{'event'}[1])) {
			out("</TABLE><TABLE BORDER><TR></TR><TR><TH class=CommentCellT COLSPAN=\"8\"\><big>${HtagTH_}$type${H_tagTH}開催！</big>（$island->{'event'}[1]ターンから）</TH></TR>");
			$flag = 1;
		} elsif($island->{'event'}[1] <= $HislandTurn) {
			out("</TABLE><TABLE BORDER><TR></TR><TR><TH class=CommentCellT COLSPAN=\"8\"\><big>${HtagTH_}$type${H_tagTH}開催中！</big></TH></TR>");
			$flag = 1;
		}
		my $turm = $island->{'event'}[2];
		if(!$turm) {
			$turm = '<big><B>無期限</B></big>';
		} else {
			$turm += $island->{'event'}[1];
			$turm = "<B>ターン<big>${HtagNumber_}${turm}${H_tagNumber}</big></B>";
		}
		$turm .= "<BR>${HtagDisaster_}$HlandName[$HlandCore][0]壊滅時強制終了${H_tagDisaster}"if($island->{'event'}[23]);
		my $max  = $island->{'event'}[3];
		$max = ($max) ? "$max艦" : '無制限';
		my $addition  = $island->{'event'}[11];
		$addition = ($addition) ? "許可する" : '許可しない';
		my $autoreturn  = $island->{'event'}[18];
		$autoreturn = ($autoreturn) ? "する" : 'しない';
		my $kind  = $island->{'event'}[4];
		my $ship = '';
		foreach (1..$#HnavyName) {
			$ship .= " $HnavyName[$_]" if($kind & (2 ** $_));
		}
		my $sstr = '';
		if($ship eq '') {
			$ship = "${HtagDisaster_}なし${H_tagDisaster}";
		} elsif($kind & 1) {
			$ship = "${HtagDisaster_}$ship${H_tagDisaster}";
			$sstr = '<BR><small>(新造艦のみ)</small>';
		}
		my $restriction = $island->{'event'}[5];
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
			$limit = '';
			foreach (1..$HmaxComNavyLevel) {
				if($restriction & (2 ** $_)) {
					$limit .= "<nobr>${HtagDisaster_}○${H_tagDisaster}Lv.$_</nobr> 　";
				} else {
					$limit .= "<nobr><B>×</B>Lv.$_</nobr> 　";
				}
			}
		}
		my $money  = $island->{'event'}[7];
		my $food  = $island->{'event'}[8];
		my $present  = $island->{'event'}[9];
		my @item  = split(' *', $island->{'event'}[10]);
		my($prize);
		$prize = "$money$HunitMoney" if($money);
		if($food) {
			$prize .= " + " if($money);
			$prize .= "$food$HunitFood";
		}
		if($present) {
			$prize .= " + " if($money || $food);
			$prize .= "管理人プレゼント";
		}
		1 while $prize =~ s/(.*\d)(\d\d\d)/$1,$2/;
		if($island->{'event'}[10]) {
			$prize .= " + " if($money || $food || $present);
			foreach (1..$#HitemName) {
				$prize .= "<span class='check'><img src=\"$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>\n" if($item[$_]);
			}
		}
		$prize = 'なし' if($prize eq '');
		my $mons = ($island->{'event'}[13]) ? "${HtagNumber_}$island->{'event'}[12]${H_tagNumber}<small>ターンにつき</small><BR>　<B>$island->{'event'}[13]</B><small>匹出現</small>" : '出現しない';
		my $huemons = ($island->{'event'}[15]) ? "${HtagNumber_}$island->{'event'}[14]${H_tagNumber}<small>ターンにつき</small><BR>　<B>$island->{'event'}[15]</B><small>匹出現</small>" : '出現しない';
		my $unknown = ($island->{'event'}[17]) ? "${HtagNumber_}$island->{'event'}[16]${H_tagNumber}<small>ターンにつき</small><BR>　<B>$island->{'event'}[17]</B><small>艦出現</small>" : '出現しない';
		my $core = ($island->{'event'}[20]) ? "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>ターンにつき</small><BR>　<B>$island->{'event'}[20]</B><small>基出現</small>" : '出現しない';
		if($flag) {
			out(<<END);
<TR><TH $HbgTitleCell>終了ターン</TH><TD align='right' class='N'>$turm</TD>
<TH $HbgTitleCell>終了時帰還処理</TH><TD align='right' class='N'>$autoreturn</TD>
<TH $HbgTitleCell>派遣可能艦艇数</TH><TD align='right' class='N'>$max</TD>
<TH $HbgTitleCell>追加派遣</TH><TD align='right' class='N'>$addition</TD></TR>
<TR><TH $HbgTitleCell>派遣可能艦種$sstr</TH><TD colspan='7' align='left'>$ship</TD></TR>
END
			out("<TR><TH $HbgTitleCell>派遣可能レベル<BR><small>(島のレベル)</small></TH><TD colspan='7' align='left'>$limit</TD></TR>") if($HmaxComNavyLevel);
			out(<<END);
<TR><TH $HbgTitleCell>怪獣</TH><TD align='right'>$mons</TD>
<TH $HbgTitleCell>巨大怪獣</TH><TD align='right'>$huemons</TD>
<TH $HbgTitleCell>所属不明艦</TH><TD align='right'>$unknown</TD>
<TH $HbgTitleCell>$HlandName[$HlandCore][0]</TH><TD align='right'>$core</TD></TR>
<TR><TH $HbgTitleCell>報償</TH><TD colspan='7' align='left' class='N'>$prize</TD></TR>
END
		}
	}
	out("</TABLE></DIV>");
}

# 情報の表示(サブ)
sub islandInfoSub {
	my($mode) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	# 情報表示
	my $sink = $island->{'sink'};
	my $sinkself = $island->{'sinkself'};
	my $subSink = $island->{'subSink'};
	my $subSinkself = $island->{'subSinkself'};
	my (@kindSink, @subKindSink, @navykind);
	my $totalSink = 0;
	my $selfSink = 0;
	my $subTotalSink = 0;
	my $subSelfSink = 0;
	my $totalNavy = 0;
	my $fkind = $island->{'fkind'};
	if($mode) {
		foreach (0..$#HnavyName) {
			$kindSink[$_] = $island->{'sink'}[$_] + $island->{'sinkself'}[$_];
			$subKindSink[$_] = $island->{'subSink'}[$_] + $island->{'subSinkself'}[$_];
			$navykind[$_] = 0; # 保有数の初期化
			next if($HnavySpecial[$_] & 0x8); # 軍港は合計に入れない
			$totalSink += $kindSink[$_];
			$selfSink += $island->{'sinkself'}[$_];
			$subTotalSink += $subKindSink[$_];
			$subSelfSink += $island->{'subSinkself'}[$_];
		}
		$subTotalSink = $totalSink - $subTotalSink;
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp) = navyUnpack(hex($_));#ここは保有数数えるだけなんで放置
			$navykind[$nKind]++; # 保有数
			next if($HnavySpecial[$nKind] & 0x8); # 軍港は合計に入れない
			$totalNavy++;
		}
	}
	# 艦隊構成を調べる
	my($id, $land, $landValue, $landValue2, $map) = ($island->{'id'}, $island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}, $island->{'map'});
	my($x, $y, $kind, $value, $value2, $name, @own, %invade, %invadeTotal);
	my $owntotal = 0;
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$value2 = $landValue2->[$x][$y];
			next if ($kind != $HlandNavy);
			# 駐留艦艇を調べる
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
			my $nSpecial = $HnavySpecial[$nKind];
			# 港・残骸は除く
			next if(($nSpecial & 0x8) || ($nFlag == 1));
			if($nId == $id && !$island->{'event'}[0]) {
				$own[$nKind]++;
				$owntotal++;
			} else {
				$invade{$nId}[91] = $nHp if($invade{$nId}[91] < $nHp);   # 耐久力
				$invade{$nId}[92] = $nExp if($invade{$nId}[92] < $nExp); # 艦艇経験値
				$invade{$nId}[$nKind]++;
				$invadeTotal{$nId}++;
			}
		}
	}
	foreach (keys %invade) {
		next if(!(defined $HidToNumber{$_}));
		# epoint
		$invade{$_}[90] = $Hislands[$HidToNumber{$_}]->{'epoint'}{$id};
	}
	my $col = @HnavyName + 2;
#	my $row = (!$HmaxComNavyLevel) ? " rowspan='1'" : " rowspan='2'";
	my($pstr);
	$pstr = '(point)' if($island->{'event'}[0] && ($island->{'event'}[6] >= 2));
	my $head =<<END;
<TR><TH$row>${HtagTH_}艦艇DATA${H_tagTH}$pstr</TH>
<TH $HbgTitleCell$row>${HtagTH_}合計${H_tagTH}</TH>
END
	foreach (@HnavyName) {
		$head .="<TD class='T'>${HtagTH_}$_${H_tagTH}</TD>";
	}
	$head .="</TR>";
#	if($HmaxComNavyLevel) {
#		$head .="<TR>";
#		foreach my $i (0..$#HnavyName) {
#			my($level, $exp);
#			my $maxComNavyLevel = $HmaxComNavyLevel-1;
#			foreach (0..$maxComNavyLevel) {
#				if($i <= $HcomNavyNumber[$_]) {
#					$level = $_ + 1;
#					last;
#				}
#				$level = '★';
#			}
#			if($level == 1) {
#				$exp = 0;
#			} elsif($level ne '★') {
#				$exp = $HcomNavyBorder[$level-2];
#			} else {
#				$exp = '不明';
#			}
#			$head .= "<TD class='T'>Lv.${level}</TD>";
#		}
#		$head .="</TR>";
#	}

	out("<DIV ID='islandInfo'><TABLE BORDER>$head") if(keys %invade != () || $mode);
	if($mode) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}保有数${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${totalNavy}艦${H_tagNumber}</TD>
END
		foreach (0..$#HnavyName) {
			my $kindNavy = $navykind[$_]; # 保有数
			$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
			out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
		}

		out(<<END);
</TR><TR>
<TH $HbgTitleCell>${HtagTH_}撃沈数${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${totalSink}艦${H_tagNumber}</TD>
END
		foreach (0..$#HnavyName) {
			my $kindsink = $kindSink[$_];
			$kindsink .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
			out("<TD $HbgInfoCell align=right>$kindsink</TD>");
		}
		out("</TR>");

		if(!$HnavySafetyZone || $HnavySafetyInvalidp) {
			out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}自爆数${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${selfSink}艦${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $sinkself = $island->{'sinkself'}[$_];
				$sinkself .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
				out("<TD $HbgInfoCell align=right>$sinkself</TD>");
			}
			out("</TR>");
		}
	}


	# 駐留状況
	my $flag = 0;
	my @infleet = sort { $a <=> $b } keys %invade;
	if($island->{'event'}[0]) {
		if($island->{'event'}[6] == 1) { # サバイバル
			# 艦艇数=>耐久力でソート
			@infleet = sort { $invadeTotal{$b} <=> $invadeTotal{$a} ||
								 $invade{$b}[91] <=> $invade{$a}[91] } keys %invade;
		} else { # epoint
			# epoint=>艦艇数=>耐久力=>経験値でソート
			@infleet = sort { $invade{$b}[90] <=> $invade{$a}[90] ||
								 $invadeTotal{$b} <=> $invadeTotal{$a} ||
								 $invade{$b}[91] <=> $invade{$a}[91] ||
								 $invade{$b}[92] <=> $invade{$a}[92] } keys %invade;
		}
	}
	if(!$HicounterMode) {
		foreach (@infleet) {
			my $in = $HidToNumber{$_};
			next if(!(defined $in));
			my $iName = islandName($Hislands[$in]);
			my $epoint = '';
			if($island->{'event'}[0]) {
				if($island->{'event'}[6] == 1) { # サバイバル
					# 艦艇数
					#$epoint = ' (' . int($invadeTotal{$_}) . ')';
				} else { # epoint
					# epoint
					$epoint = ' (' . int($invade{$_}[90]) . ')';
				}
			}
			out(<<END);
<TR>
<TD align=right>${HtagTH_}<A STYlE="text-decoration:none" href="${HthisFile}?Sight=$_" target="_blank">${iName}</A>${H_tagTH}$epoint</TH>
<TD align=right>${HtagNumber_}$invadeTotal{$_}艦${H_tagNumber}</TD>
END
			foreach $in (0..$#HnavyName) {
				my $invadeship = ($HnavySpecial[$in] & 0x8) ? '−' : sprintf("%d艦", $invade{$_}[$in]);
				out("<TD align=right>$invadeship</TD>");
			}
			out("</TR>");
			$flag = 1 if(!$island->{'event'}[0]);
		}
		if($mode && $flag) {
			out(<<END);
<TR>
<TH>${HtagTH_}駐留艦隊${H_tagTH}</TH>
<TD align=right>${HtagNumber_}${owntotal}艦${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $ownship = ($HnavySpecial[$_] & 0x8) ? '−' : sprintf("%d艦", $own[$_]);
				out("<TD align=right>$ownship</TD>");
			}
			out("</TR>");
		}
	}
	if($mode) {
		# サブデータ
		my(@sData) = @{$Hislands[$HcurrentNumber]->{'subExt'}};
		my $sTurn = $sData[0];
		$sTurn++;
		my $birthday = $Hislands[$HcurrentNumber]->{'birthday'};
		$birthday++;
		if($sTurn > $birthday) {
			my $row = (!$HnavySafetyZone || $HnavySafetyInvalidp) ? 2 : 1;
			out(<<END);
</TR>
<TR><TH $HbgTitleCell colspan='$col'>${HtagTH_}${HnormalColor_}ターン${H_normalColor}${sTurn}${HnormalColor_}〜${H_normalColor}現在${H_tagTH}</TH></TR>
$head
<TR><TH $HbgTitleCell>${HtagTH_}撃沈数${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${subTotalSink}艦${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $subKindSink = $kindSink[$_] - $subKindSink[$_];
				$subKindSink .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
				out("<TD $HbgInfoCell align=right>$subKindSink</TD>");
			}
			out("</TR>");

			if(!$HnavySafetyZone || $HnavySafetyInvalidp) {
				out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}自爆数${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${subSelfSink}艦${H_tagNumber}</TD>
END
				foreach (0..$#HnavyName) {
					my $subSinkself = $island->{'sinkself'}[$_] - $island->{'subSinkself'}[$_];
					$subSinkself .= ($HnavySpecial[$_] & 0x8) ? '港' : '艦';
					out("<TD $HbgInfoCell align=right>$subSinkself</TD>");
				}
				out("</TR>");
			}
		}
	}
	out("</TABLE></DIV>");
}

# 情報の表示(気象)
sub islandInfoWeather {
	my($mode) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$island->{'weather'}};
	my @turn = ($HislandTurn, $HislandTurn + 1, $HislandTurn + 2, $HislandTurn + 3);
	out(<<END);
<DIV ID='weatherInfo'><TABLE BORDER>
<TR><TH colspan></TH></TR>
<TR>
<TH $headNameCellcolor colspan=6>気象データ</TH>
<TH $headNameCellcolor><span $todayColor>現在</TH>
<TH $headNameCellcolor colspan=6><span $tomorrowColor>予報</TH>
</TR>
<TR><TD $pointCellcolor>${HtagTH_}気温${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}気圧${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}湿度${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}風速${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}地盤${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}波力${H_tagTH}</TD>
<TD $pointCellcolor rowspan=2><img src ='${HimageDir}/$HweatherImage[$weather[3]]'><br><span $todayColor>$HweatherName[$weather[3]]</span></TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>次回(${turn[1]})</TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>${turn[2]}</TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>${turn[3]}</TD>
</TR>
<TR><TD $pointCellcolor2>${kion}℃</TD><TD $pointCellcolor2>${kiatu}hPa</TD><TD $pointCellcolor2>${situdo}%</TD><TD $pointCellcolor2>${kaze}m/s</TD><TD $pointCellcolor2>${jiban}</TD><TD $pointCellcolor2>${nami}</TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[2]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[2]]</span></TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[1]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[1]]</span></TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[0]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[0]]</span></TD>
</TR>
</TABLE></DIV>
END
}

# 各種拡張データ表示(帝国の興亡)
sub islandData {
	my(@data) = @{$Hislands[$HcurrentNumber]->{'ext'}};
	my(@sData) = @{$Hislands[$HcurrentNumber]->{'subExt'}};
	my $sTurn = $sData[0];
	$sTurn++;
	my $birthday = $Hislands[$HcurrentNumber]->{'birthday'};
	$birthday++;
	my $sMkill = $sData[$#sData - 1];
	my $loop = (10 < $#data) ? $#data : 10;
	foreach (0..$loop){
		$sData[$_] = $data[$_] - $sData[$_];
	}
	my(@after) = ('', '', '基', '基', "$HunitPop", '発', '発', '発', '艦', '艦', '艦');
	# 前処理
	$data[1] = int($data[1] / 10);
	$sData[1] = int($sData[1] / 10);
	foreach (2..$loop){
		$data[$_] = $data[$_] ? "${data[$_]}${after[$_]}" : 'なし';
		$sData[$_] = $sData[$_] ? "${sData[$_]}${after[$_]}" : 'なし';
	}
	$sMkill = $Hislands[$HcurrentNumber]->{'monsterkill'} - $sMkill;
	my $monsterkill = $Hislands[$HcurrentNumber]->{'monsterkill'} ? "$Hislands[$HcurrentNumber]->{'monsterkill'}$HunitMonster" : 'なし';
	my $sMonsterkill = $sMkill ? "$sMkill$HunitMonster" : 'なし';
	my(@aStr, @mStr, @nStr);
	my $col = 6;
	if($HallyNumber && ($Hislands[$HcurrentNumber]->{'allyId'}[0] ne '')) {
		$aStr[0] = "<TH $HbgTitleCell>${HtagTH_}貢献度${H_tagTH}</TH>";
		$aStr[1] = "<TD $HbgInfoCell align=center>$data[1]</TD>";
		$aStr[2] = "<TD $HbgInfoCell align=center>$sData[1]</TD>";
		$col++;
	}
	if($HuseBase || $HuseSbase) {
		$mStr[0] =  "<TH $HbgTitleCell>${HtagTH_}ミ撃破${H_tagTH}</TH>";
		$mStr[1] =  "<TD $HbgInfoCell align=center>$data[3]</TD>";
		$mStr[2] =  "<TD $HbgInfoCell align=center>$sData[3]</TD>";
		$col++;
	}
	if($HnavyName[0] ne '') {
		$nStr[0] =  "<TH $HbgTitleCell>${HtagTH_}艦派遣${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}艦来襲${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}艦破壊${H_tagTH}</TH>";
		$nStr[1] =  "<TD $HbgInfoCell align=center>$data[8]</TD><TD $HbgInfoCell align=center>$data[9]</TD><TD $HbgInfoCell align=center>$data[10]</TD>";
		$nStr[2] =  "<TD $HbgInfoCell align=center>$sData[8]</TD><TD $HbgInfoCell align=center>$sData[9]</TD><TD $HbgInfoCell align=center>$sData[10]</TD>";
		$col += 3;
	}
	out(<<END);
<DIV ID='extInfo'><TABLE BORDER>
<TR>
$aStr[0]
<TH $HbgTitleCell>${HtagTH_}防撃破${H_tagTH}</TH>
$mStr[0]
<TH $HbgTitleCell>${HtagTH_}民救出${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾飛来${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾発射${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}弾防御${H_tagTH}</TH>
$nStr[0]
<TH $HbgTitleCell>${HtagTH_}退治数${H_tagTH}</TH>
</TR>
<TR>
$aStr[1]
<TD $HbgInfoCell align=center>$data[2]</TD>
$mStr[1]
<TD $HbgInfoCell align=center>$data[4]</TD>
<TD $HbgInfoCell align=center>$data[5]</TD>
<TD $HbgInfoCell align=center>$data[6]</TD>
<TD $HbgInfoCell align=center>$data[7]</TD>
$nStr[1]
<TD $HbgInfoCell align=center>$monsterkill</TD>
</TR>
END

	out(<<END) if($sTurn > $birthday);
<TR>
<TH $HbgTitleCell colspan='$col'>${HtagTH_}${HnormalColor_}ターン${H_normalColor}${sTurn}${HnormalColor_}〜${H_normalColor}現在${H_tagTH}</TH>
</TR>
<TR>
$aStr[2]
<TD $HbgInfoCell align=center>$sData[2]</TD>
$mStr[2]
<TD $HbgInfoCell align=center>$sData[4]</TD>
<TD $HbgInfoCell align=center>$sData[5]</TD>
<TD $HbgInfoCell align=center>$sData[6]</TD>
<TD $HbgInfoCell align=center>$sData[7]</TD>
$nStr[2]
<TD $HbgInfoCell align=center>$sMonsterkill</TD>
</TR>
END
	out("</TABLE></DIV>");
}
#----------------------------------------------------------------------
# 地図の表示
#----------------------------------------------------------------------
# $modeが1なら、ミサイル基地等をそのまま表示
# $jsmodeが1なら、JSモード
# $noが0でないなら、着弾点表示モード
sub islandMap {
	my($mode, $jsmode, $no, $world) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	my($id) = $island->{'id'};

	# 着弾点表示の準備
	my($mPoint, $mS, $mO, $fS, $fO);
	if($no) {
		$mPoint = missileMapSet($id, $no);
		$mS = $mPoint->{'self'};
		$mO = $mPoint->{'other'};
		$no = 0 if($mPoint == 0);
	}

	# 地形、地形値を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($map) = $island->{'map'};
	my($l, $lv, $lv2);

	# コマンド取得
	my($command) = $island->{'command'};
	my($com, @comStr, $i, $j);
	if($HmainMode eq 'owner') {
		my %comNavyFlag;
		foreach (0..$#HnavyName) {
			$comNavyFlag{$HcomNavy[$_]} = 1 if($HnavySpecial[$_] & 0x8);
		}
		for($i = 0; $i < $HcommandMax; $i++) {
			$j = $i + 1;
			$com = $command->[$i];
			if(($com->{'kind'} < 30) || $comNavyFlag{$com->{'kind'}}) { # 整地系と作る系、軍港建設
				$comStr[$com->{'x'}][$com->{'y'}] .= " [${j}]$HcomName[$com->{'kind'}]";
			}
		}
	}
	my(%amityFlag, $vIsland);
	if($HjammingView || ($HroundView == 2)) {
		my $n = $HidToNumber{$defaultID};
		$vIsland = (defined $n) ? $Hislands[$n] : '';
		$HvId = (checkPassword($vIsland, $HdefaultPassword)) ? $defaultID : -1;
		my($ii);
		if(!$HvId) {
			foreach $ii (0..$islandNumber) {
				$amityFlag{$Hislands[$ii]->{'id'}} = 1;
			}
		} else {
			$amityFlag{$HvId} = 1;
			if((defined $n) && ($HjammingView == 2)) {
				foreach $ii (0..$islandNumber) {
					foreach (@{$Hislands[$ii]->{'amity'}}) {
						if($_ == $HvId) {
							$amityFlag{$Hislands[$ii]->{'id'}} = 1;
							last;
						}
					}
				}
			}
		}
	}
	my($alpha) = ($HjammingView && ($HjammingLand != 1) && !$mode && !$vIsland->{'itemAbility'}[2]) ? " STYLE=\"filter: Alpha(opacity=50);\"" : '';
	my($wide) = (($Hroundmode || $HoceanMode) && (($HroundView == 1) || (($HroundView == 2) && $vIsland->{'earth'})));
	my(@x, @y, @tmpX, @tmpY);
	@x = (@tmpX = (!$world) ? @{$map->{'x'}} : @defaultX);
	@y = (@tmpY = (!$world) ? @{$map->{'y'}} : @defaultY);
	if($Hroundmode && $HadjustMap && $world) {
		my $mx = $island->{'wmap'}->{'x'};
		my $my = $island->{'wmap'}->{'y'};
		@bx = (@x)x3;
		@by = (@y)x3;
		@x = (@tmpX = @bx[(($mx+1+int($HoceanSizeX/2))*$HislandSizeX)..(($mx+1+$HoceanSizeX+int($HoceanSizeX/2))*$HislandSizeX-1)]);
		@y = (@tmpY = @by[(($my+1+int($HoceanSizeY/2))*$HislandSizeY)..(($my+1+$HoceanSizeY+int($HoceanSizeY/2))*$HislandSizeY-1)]);
	}
	if($wide){
		unshift(@x, $correctX[$tmpX[0]-1 + $#an]) if($correctX[$tmpX[0]-1 + $#an] >= 0);
		unshift(@y, $correctY[$tmpY[0]-1 + $#an]) if($correctY[$tmpY[0]-1 + $#an] >= 0);
		push(@x, $correctX[$tmpX[$#tmpX]+1 + $#an]) if($correctX[$tmpX[$#tmpX]+1 + $#an] >= 0);
		push(@y, $correctY[$tmpY[$#tmpY]+1 + $#an]) if($correctY[$tmpY[$#tmpY]+1 + $#an] >= 0);
	}

	out("<DIV ID='islandMap'><TABLE BORDER class='mark'><TR><TD>");
	# 座標(上)を出力
	out("<nobr>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");

	my($x, $y, $v2, $v1, $v0, $csize2, $csize1, $csize0, $i, $j);
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		unless ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
	out("</nobr><BR>");

	my $range = 0;
	if($HjammingView) {
		foreach $y (@y) {
			foreach $x (@x) {
				if($amityFlag{$HlandID[$x][$y]}) {
					$HviewJam[$x][$y] = 1;
				}
				$range = -1;
				if($land->[$x][$y] == $HlandNavy) {
					my($nId, $nKind) = (navyUnpack($landValue->[$x][$y]))[0, 7];
					$range = $HnavyFireRange[$nKind] if($nId == $HvId);
				} elsif($land->[$x][$y] == $HlandMonster) {
					my($mId, $mKind) = (monsterUnpack($landValue->[$x][$y]))[0, 5];
					$range = $HmonsterFireRange[$mKind] if($mId == $HvId);
				} elsif($land->[$x][$y] == $HhugeMonsterFireRange) {
					my($mId, $mKind) = (monsterUnpack($landValue->[$x][$y]))[0, 5];
					$range = $HnavyFireRange[$mKind] if($mId == $HvId);
				}
				if($range >= 0) {
					foreach (0..($an[$range] - 1)) {
						$sx = $x + $ax[$_];
						$sy = $y + $ay[$_];
						# 行による位置調整
						$sx-- if(!($sy % 2) && ($y % 2));
						$sx = $correctX[$sx + $#an];
						$sy = $correctY[$sy + $#an];
						# 範囲外の場合
						next if(($sx < 0) || ($sy < 0));
						$HviewJam[$sx][$sy] = 1;
					}
				}
			}
		}
	}
	# 各地形および改行を出力
	foreach $j (0..$#y) {
		$y = $y[$j];
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);
		out("<TABLE BORDER=0 cellpadding='0' cellspacing='0'><TR><TD class='M'>") if($no);

		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
		} else {
			# 偶数番号なら番号を出力
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		}
		out("</TD>") if($no);



		# 各地形を出力
		foreach $i (0..$#x) {
			$x = $x[$i];
			my($wideFlag, $islName);
			$wideFlag = ($wide && (
				(($x == $correctX[$tmpX[0]-1 + $#an]) && !$i) ||
				(($x == $correctX[$tmpX[$#tmpX]+1 + $#an]) && ($i == $#x)) ||
				(($y == $correctY[$tmpY[0]-1 + $#an]) && !$j) ||
				(($y == $correctY[$tmpY[$#tmpY]+1 + $#an]) && ($j == $#y))
				)) ? 1 : 0;
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$lv2 = $landValue2->[$x][$y];

			$jamming = 0;
			if($HjammingView && (!$mode || ($HoceanMode && $wideFlag)) && !$vIsland->{'itemAbility'}[2]) {
				$jamming = 1 if(!$HviewJam[$x][$y] && !((!$world && $amityFlag{($HoceanMode ? $HlandID[$x][$y] : $id)}) || ($world && $amityFlag{$HlandID[$x][$y]})));
			}
			if($HoceanMode && ($world || $wideFlag)) {
				my $n = $HidToNumber{$HlandID[$x][$y]};
				if(defined $n) {
					$islName = '【' . islandName($Hislands[$n]) . '】';
					$islName =~ s/<FONT COLOR=\"[\w\#]+\"><B>(.*)<\/B><\/FONT>/$1/g;
					$islName =~ s/<[^<]*>//g;
				} else {
					$islName = '【未知の海域】';
				}
			}
			landString($l, $lv, $lv2, $x, $y, $mode, $comStr[$x][$y], $jsmode, $no, $jamming, $wideFlag, $islName);
			if($no) {
				$fS = $mS->[$x][$y];
				$fO = $mO->[$x][$y];
#				out("<CENTER>") if($fS || $fO);
				if($fS ==1) {
					out("<span class='nodamage'>★</span>");
				} elsif($fS ==2) {
					out("<span class='defence'>★</span>");
				} elsif($fS ==3) {
					out("<span class='harden'>★</span>");
				} elsif($fS ==4) {
					out("<span class='hitpoint'>★</span>");
				}
				if($fO ==1) {
					out("<span class='nodamage'>●</span>");
				} elsif($fO ==2) {
					out("<span class='defence'>●</span>");
				} elsif($fO ==3) {
					out("<span class='harden'>●</span>");
				} elsif($fO ==4) {
					out("<span class='hitpoint'>●</span>");
				}
#				out("</CENTER>") if($fS || $fO);
				out("</TD>");
			}
			out("</A>");
		}

		out("<TD class='M'>") if($no);
		if($y % 2) {
			# 奇数行目なら番号を出力
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
		}

		# 改行を出力
		out("</TD></TR></TABLE>\n") if($no);
		out("</BR>\n") unless($no);
	}

	# 座標(下)を出力
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		if ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
	out("<BR>");
	out("<div id='NaviView'></div>");
	out("</TD></TR></TABLE></DIV>\n");
}

sub landString {
	my($l, $lv, $lv2, $x, $y, $mode, $comStr, $jsmode, $no, $jamming, $wideFlag, $islName) = @_;
	my($point) = "($x,$y)";
	my($image, $alt, $myFleet, $my_Fleet, $myFleet_);
	my($naviTitle);
	my($naviText);
	my($naviExp) = "''";

	if((!$mode || ($HoceanMode && $wideFlag)) && $jamming) {
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
			($l == $HlandMonument)) {
			$l  = $HlandWaste;
			$lv = 2;
		} elsif(($l == $HlandMonster) ||
			($l == $HlandHugeMonster)) {
			my($id, $flag) = (monsterUnpack($lv))[0,4];
			if($id != $HvId) {
				$l  = ($flag & 2) ? $HlandSea : $HlandWaste;
				$lv = 2;
			}
		} elsif($l == $HlandComplex) {
			my($cKind) = (landUnpack($lv))[1];
			if($HcomplexPretend[$cKind]) {
				$l  = ($HcomplexPretend[$cKind]%2) ? $HlandWaste : $HlandSea;
			} else {
				$l  = ($HcomplexAttr[$cKind] & 0x300) ? $HlandSea : $HlandWaste;
			}
			$lv = 2;
		} elsif($l == $HlandCore) {
			my($lFlag) = int($lv / 10000);
			$l  = (!$lFlag) ? $HlandWaste : $HlandSea;
			$lv = 2;
		} elsif($l == $HlandNavy) {
			my($nId) = (navyUnpack($lv, $lv2))[0];
			if($nId != $HvId) {
				$l  = $HlandSea;
				$lv = 2;
			}
		}
	}

#	my $alpha = (!$wideFlag) ? '' : " STYLE=\"filter: gray();\"";
	my $alpha = (!$wideFlag) ? '' : " STYLE=\"width=${\($HchipSize*2-2)}; height=${\($HchipSize*2-2)}; border-width=1; border-color=#FFFFFF\"";
	if($l == $HlandSea) {
		$image = $HlandImage[$l][$lv];
		$alt = $HlandName[$l][$lv];
		$naviTitle  = $alt;
		$naviExp = "SEA${\int($lv)}";
		if($lv == 2) {
			$alt = '海系地形';
			$naviTitle  = $alt;
			$naviExp = "";
			$image = $HjammingSeaImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		$image = $HlandImage[$l][$lv];
		$alt = $HlandName[$l][$lv];
		$naviTitle  = $alt;
		$naviExp = "WASTE$lv";
		if($lv == 2) {
			$alt = '陸系地形';
			$naviTitle  = $alt;
			$naviExp = "";
			$image = $HjammingWasteImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "PLAINS";
	} elsif($l == $HlandForest) {
		# 森
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		# 観光者の場合は木の本数隠す
		if($mode && !($HoceanMode && $wideFlag)) {
			$naviText = "${lv}$HunitTree";
			$alt .= '(' . $naviText .')';
		}
		$naviExp = "FOREST";
	} elsif($l == $HlandTown) {
		# 都市系
		my($n);
		foreach (reverse(0..$#HlandTownValue)) {
			if($HlandTownValue[$_] <= $lv) {
				$image = $HlandTownImage[$_];
				$n = $HlandTownName[$_];
				$naviExp = "TOWN$_";
				last;
			}
		}
		$alt = $n;
		$naviTitle  = $alt;
		$naviText  = "${lv}${HunitPop}";
		$alt .= '(' . $naviText .')';
	} elsif($l == $HlandFarm) {
		# 農場
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviText  = "${lv}0${HunitPop}規模";
		$alt .= '(' . $naviText .')';
		$naviExp = "FARM";
	} elsif($l == $HlandFactory) {
		# 工場
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviText  = "${lv}0${HunitPop}規模";
		$alt .= '(' . $naviText .')';
		$naviExp = "FACTORY";
	} elsif($l == $HlandBase) {
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# 観光者の場合は森のふり
			$image = $HlandImage[$HlandForest];
			$alt = $HlandName[$HlandForest];
			$naviTitle  = $alt;
			$naviExp = "FOREST";
		} else {
			# ミサイル基地
			my($level) = expToLevel($l, $lv);
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "レベル ${level}/経験値 $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "BASE";
		}
	} elsif($l == $HlandSbase) {
		# 海底基地
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# 観光者の場合は海のふり
			$image = $HlandImage[$HlandSea][0];
			$alt = $HlandName[$HlandSea][0];
			$naviTitle  = $alt;
			$naviExp = "SEA0";
		} else {
			my($level) = expToLevel($l, $lv);
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "レベル ${level}/経験値 $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "SEABASE";
		}
	} elsif($l == $HlandDefence) {
		# 防衛施設
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HdBaseHide) {
				# 観光者の場合は森のふり
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} else {
				# 観光者の場合は耐久力不明
				$image = $HlandImage[$l][0];
				$alt = $HlandName[$l][0];
				$naviTitle  = $alt;
				$naviExp = "DEFENCE0";
			}
		} else {
			$image = $HlandImage[$l][0];
			$alt = $HlandName[$l][0];
			$naviTitle  = $alt;
			$naviExp = "DEFENCE0";
			if($HdurableDef){
				$lv++;
				if($lv >= $HdefLevelUp) {
					$image = $HlandImage[$l][1];
					$alt = $HlandName[$l][1];
					$naviTitle  = $alt;
					$naviExp = "DEFENCE1";
				}
				$naviText  = "耐久力 $lv";
				$alt .= '(' . $naviText .')';
			}
		}
	} elsif($l == $HlandBouha) {
		# 防波堤
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "BOUHA";
	} elsif($l == $HlandSeaMine) {
		# 機雷
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# 観光者の場合は海のふり
			$image = $HlandImage[$HlandSea][0];
			$alt = $HlandName[$HlandSea][0];
			$naviTitle  = $alt;
			$naviExp = "SEA0";
		} else {
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "破壊力 $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "SEAMINE";
		}
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HdBaseHide) {
				# 観光者の場合は森のふり
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} else {
				# 観光者の場合は防衛施設のふり
				$image = $HlandImage[$HlandDefence][0];
				$alt = $HlandName[$HlandDefence][0];
				$naviTitle  = $alt;
				$naviExp = "DEFENCE";
			}
		} else {
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviExp = "HARIBOTE";
		}
	} elsif($l == $HlandOil) {
		# 海底油田
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "OIL";
	} elsif($l == $HlandMountain) {
		# 山
		my $mlv = ($lv > 0) ? 1 : 0;
		$image = $HlandImage[$l][$mlv];
		$alt = $HlandName[$l][$mlv];
		$naviTitle  = $alt;
		if($mlv) {
			$naviText  = "${lv}0${HunitPop}規模";
			$alt .= '(' . $naviText .')';
		}
		$naviExp = "MOUNTAIN$mlv";
	} elsif($l == $HlandCore) {
		# コア
		my($lFlag, $lLv) = (int($lv / 10000), ($lv % 10000));
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HcoreHide) {
				# 観光者の場合
				if(!$lFlag) { # 森のふり
					$image = $HlandImage[$HlandForest];
					$alt = $HlandName[$HlandForest];
					$naviTitle  = $alt;
					$naviExp = "FOREST";
				} else { # 海のふり
					$image = $HlandImage[$HlandSea][0];
					$alt = $HlandName[$HlandSea][0];
					$naviTitle  = $alt;
					$naviExp = "SEA0";
				}
			} else {
				# 観光者の場合は耐久力不明
				$image = $HlandImage[$l][$lFlag];
				$alt = $HlandName[$l][$lFlag];
				$naviTitle  = $alt;
				$naviExp = "CORE$lFlag";
			}
		} else {
			$image = $HlandImage[$l][$lFlag];
			$alt = $HlandName[$l][$lFlag];
			$naviTitle  = $alt;
			$naviExp = "CORE$lFlag";
			if($HdurableCore){
				$lLv++;
				$naviText  = "耐久力 $lLv";
				$alt .= '(' . $naviText .')';
			}
		}
	} elsif($l == $HlandResource) {
		# 海底資源
                my($tmp, $kind, $turn, $food, $money) = landUnpack($lv);
                if($kind == 0){
		    $image = $HlandImage[$l][$kind];
                    $money = 1200 + $money *20;
		    $alt = $HlandName[$l][$kind];
	            $naviText  = "${money}${HunitMoney}相当";
	            $alt .= '(' . $naviText .')';
		    $naviExp = "OIL";
                }else{
		    $image = $HlandImage[$l][$kind];
                    $food = 1200 + $food * 20;
		    $alt = $HlandName[$l][$kind];
	            $naviText  = "${food}0${HunitFood}相当";
	            $alt .= '(' . $naviText .')';
		    $naviExp = "OIL";
                }
	} elsif($l == $HlandMonument) {
		# 記念碑
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
		$naviTitle  = $alt;
		$naviExp = "MONIMENT$lv";
	} elsif($l == $HlandComplex) {
		# 複合地形
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $turn = $cTurn * $HcomplexTPrate[$cKind];
		my $tflag = $turn && (!$HcomplexTPhide[$cKind] || ($mode && !($HoceanMode && $wideFlag)));
		my $food = $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
		my $money = $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
		if($HcomplexPretend[$cKind] && (!$mode || ($HoceanMode && $wideFlag))) {
			if($HcomplexPretend[$cKind] == 1) { # 森のふり
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} elsif($HcomplexPretend[$cKind] == 2) { # 海のふり
				$image = $HlandImage[$HlandSea][0];
				$alt = $HlandName[$HlandSea][0];
				$naviTitle  = $alt;
				$naviExp = "SEA0";
			} else {
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = $HcomplexPretendNavi[$cKind];
			}
		} else {
			if((defined $HcomplexLevelKind[$cKind]) && (defined $HcomplexLevelValue[$cKind][0])) {
				my $levelflag = { 'turn' => $turn, 'food' => $food, 'money' => $money };
				foreach (reverse(0..$#{$HcomplexLevelValue[$cKind]})) {
					if($HcomplexLevelValue[$cKind][$_] <= $levelflag->{"$HcomplexLevelKind[$cKind]"}) {
						$image = $HcomplexSubImage[$cKind][$_];
						$alt = $HcomplexSubName[$cKind][$_];
						last;
					}
				}
			} else {
				$image = $HcomplexImage[$cKind];
				$alt = $HcomplexName[$cKind];
			}
			$naviTitle = $alt;
			$alt .= "(" if($tflag || $food || $money);
			$alt .= "T:${turn}$HcomplexTPunit[$cKind]/" if($tflag);
			$alt .= "F:${food}0${HunitPop}規模/" if($food);
			if($money) {
				$alt .= "M:${money}0${HunitPop}規模";
			} elsif($tflag || $food) {
				substr($alt, -1) = '';
			}
			$alt .= ")" if($tflag || $food || $money);
			$naviText .= "$HcomplexTPname[$cKind]\:${turn}$HcomplexTPunit[$cKind]<BR>" if($tflag);
			$naviText .= "食料生産:${food}0${HunitPop}規模<BR>" if($food);
			if($money) {
				$naviText .= "資金収入:${money}0${HunitPop}規模";
			} else {
				substr($naviText, -4) = '';
			}
			$naviExp = "COMPLEX$cKind";
		}
	} elsif($l == $HlandMonster) {
		# 怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$kind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$id}]) if (defined $HidToNumber{$id});
		$name =~ s/<[^<]*>//g;

		$image = $HmonsterImage[$kind];

		# 硬化中？
		$image = $HmonsterImage2[$kind] if ($flag & 1);

		# 潜水中？
		$image = $HmonsterImageUnderSea if ($flag & 2);

		$alt = "$mName(体力${hp}/経験値 ${exp})$name";
		$naviTitle  = $mName;
		$naviText  = "　体力${hp}<BR>　経験値 ${exp}";
		$naviText .= "<br>　$name" if (defined $name);
		$naviExp = "MONSTER$kind";
	} elsif($l == $HlandHugeMonster) {
		# 巨大怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$kind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$id}]) if (defined $HidToNumber{$id});
		$name =~ s/<[^<]*>//g;
		if(($flag & 1) && ($flag & 2)) {
			# 海で硬化
			$image = $HhugeMonsterImage4[$kind][$hflag];
		} elsif($flag & 1) {
			# 陸で硬化
			$image = $HhugeMonsterImage2[$kind][$hflag];
		} elsif($flag & 2) {
			# 海
			$image = $HhugeMonsterImage3[$kind][$hflag];
		} else {
			# 陸
			$image = $HhugeMonsterImage[$kind][$hflag];
		}
		$alt = "$mName(体力${hp}/経験値 ${exp})$name";
		$naviTitle  = $mName;
		$naviText  = "　体力${hp}<BR>　経験値 ${exp}";
		$naviText .= "<br>　$name" if (defined $name);
		$naviExp = "HUGEMONSTER$kind";
	} elsif($l == $HlandNavy) {
		# 海軍
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my($level) = expToLevel($l, $exp);
		my @status = ('', '退治', '巡航', '停船');
		my $nName = $HnavyName[$kind];
                my($goal);
                if(($goalx == 31) ||
                   ($goaly == 31)) {
                    $goal = "停船中";
                }else{
                    $goal = "目標($goalx, $goaly)";
                }

                $wait--;
                if($wait <= 0){
                    $ririku = "、発艦準備OK";
                }else{
                    $ririku = "、離陸待ち${wait}ターン"
                }

                if(($kind != 0) && ($kind != 0x0c)){
                    $ririku = "";
                }

                # 航空機だったら表記変更
                if($HnavyCruiseTurn[$kind] !=0){
                    $ririku = "、${wait}ターン後に帰投";
                }

                # 最大耐久力
                my $maxHp = int($HnavyHP[$kind] * (120 + $exp) / 120);

		$image = $HnavyImage[$kind];
		$naviTitle  = $nName;
		$naviExp = "NAVY$kind";
		$alt = '';
		if ($flag == 1) {
			# 残骸？
			$image = $HnavyImageZ;
			$alt  = "$nNameの残骸";
			$alt .= "(破壊率${exp}%)" if($mode && !($HoceanMode && $wideFlag));
			$naviText = "$nNameの残骸";
			$naviText .= "<BR>　(破壊率${exp}%)" if($mode && !($HoceanMode && $wideFlag));
		} else {
			if ($flag & 2) {
				# 潜水中？
				$image = $HnavyImage2[$kind];
			}

			my $name;
			my $special = $HnavySpecial[$kind];
			my $num = $HidToNumber{$id};
			if(defined $num) {
				my $island = $Hislands[$num];
				my %amityFlag;
				my $amity = $island->{'amity'};
				foreach (@$amity) {
					next unless(defined $HidToNumber{$_});
					$amityFlag{$_} = 1;
				}
				if($id == $defaultID) {
					$myFleet = " class='myFleet'";
					$my_Fleet = "<span class='myFleetCell'>";
					$myFleet_ = "</span>";
				} elsif($amityFlag{$defaultID}) {
					$myFleet = " class='campFleet'";
					$my_Fleet = "<span class='campFleetCell'>";
					$myFleet_ = "</span>";
				}
				my $ofname = $island->{'fleet'}->[$no];
				my($fname);
				$fname = "${ofname}艦隊 " if !($special & 0x8);
				$name = islandName($island);
				$name =~ s/<[^<]*>//g;
				$alt = "$name $fname";
				$naviText = "$name<BR>　$fname";
			} else {
				$alt = "所属不明 ";
				$naviText = "所属不明 ";
			}

			$alt .= $nName;
#			if(($mode && !($HoceanMode && $wideFlag)) || !(defined $num) || $HnavyShowInfo) {
				$status[$stat] .= '/' if($status[$stat] ne '');
                                if ($flag != 3) {
                                    if(($special & 0x8) || ($HnavyNoMove[$kind])){
				        $alt .= " (${status[$stat]}耐久力${hp}/${maxHp}、経験値${exp} ${ririku})";
				        $naviText .= "<BR>　${status[$stat]}耐久力${hp}/${maxHp}<BR> 経験値${exp}${ririku}";
                                    }else{
				        $alt .= " (${status[$stat]}耐久力${hp}/${maxHp}、経験値${exp}、${goal} ${ririku})";
				        $naviText .= "<BR>　${status[$stat]}耐久力${hp}/${maxHp}<BR> 経験値${exp}<BR> ${goal} ${ririku}";
                                    }
                                }else{
				    $alt .= " (${status[$stat]}建造中 ${hp}/${HnavyBuildTurn[$kind]})";
				    $naviText .= "<BR>　${status[$stat]}建造中 ${hp}/${HnavyBuildTurn[$kind]}";
				    $image = $HnavyImage3;
                                }
#			} elsif($stat) {
#				$alt .= " (${status[$stat]})";
#				$naviText .= "<BR>　(${status[$stat]}モード)";
#			}
		}
	}

	$alt =~ s/'/\\'/g;
	$naviText =~ s/'/\\'/g;
	$alt =~ s/&#x27;/\\'/g;
	$naviText =~ s/&#x27;/\\'/g;
	1 while $alt =~ s/(.*\d)(\d\d\d)/$1,$2/;
	1 while $naviText =~ s/(.*\d)(\d\d\d)/$1,$2/;
	if($islName ne '') {
		$alt = $islName . $alt;
		$naviTitle = $islName . $naviTitle;
	}
	# 開発画面の場合は、座標設定
	if($jsmode) {
		out("<A onclick=\"");
		out("ps($x,$y);set_land($x, $y, '$alt', '$image');\" onMouseOver=\"");
		out("Navi($x, $y,'$image', '$naviTitle', '$naviText', '$naviExp'); ") if($HpopupNavi); # 1
		if($mode == 1 && $HmainMode ne 'landmap') {
			out("set_com($x, $y, '$alt');\"");
		}elsif($HmainMode eq 'landmap') {
			out("sv($x, $y, '$alt');\"");
		}
		out(" onMouseOut=\"scls();\">");
	} else {
		out("<A onClick=\"ps($x,$y);\" onMouseOver=\"");
		# 開発画面の場合は、座標設定
		out("Navi($x, $y,'$image', '$naviTitle', '$naviText', '$naviExp'); ") if(($mode != 1) || $HpopupNavi); # 1
		out("sv($x, $y, '$alt');\" onMouseOut=\"scls();\">");
	}
	$alt =~ s/\\'/'/g;
	my($suf) = (!$wideFlag) ? '' : 'w';
	if($no) {
		out("<TD BACKGROUND=\"$image\" TITLE=\"$point $alt $comStr\" width=${\($HchipSize*2)} height=${\($HchipSize*2)} BORDER=0$alpha class='M' ID='${x}${suf}x${y}${suf}'>");
	} elsif(!$jsmode && ($mode != 1)) {
		out("${my_Fleet}<IMG SRC=\"$image\"$myFleet width=${\($HchipSize*2)} height=${\($HchipSize*2)} BORDER=0$alpha ID='${x}${suf}x${y}${suf}'>${myFleet_}");
	} else {
		out("${my_Fleet}<IMG SRC=\"$image\"$myFleet TITLE=\"$point $alt $comStr\" width=${\($HchipSize*2)} height=${\($HchipSize*2)} BORDER=0$alpha ID='${x}${suf}x${y}${suf}'>${myFleet_}");
	}
	#	out("</A>");
}

# 艦艇(怪獣)の射程範囲かどうか確認
sub countAroundRange {
	my($island, $x, $y, $id, $range) = @_;
	return 0 if($id eq '');

	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($sx, $sy);
	my $count = 0;

	my $tmp = 0;
	foreach $r (0..$range) {
		my $r2 = $an[$r] - 1;
		foreach ($tmp..$r2) {
			$sx = $x + $ax[$_];
			$sy = $y + $ay[$_];
			# 行による位置調整
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];

			# 範囲外の場合
			next if(($sx < 0) || ($sy < 0));

			if($land->[$sx][$sy] == $HlandNavy) {
				my($nId, $nKind) = (navyUnpack($landValue->[$sx][$sy]))[0, 7];
				my $nRange = $HnavyFireRange[$nKind];
				return 1 if(($nRange >= $r) && ($nId == $id));
			} elsif($land->[$sx][$sy] == $HlandMonster) {
				my($mId, $mKind) = (monsterUnpack($landValue->[$sx][$sy]))[0, 5];
				my $nRange = $HmonsterFireRange[$nKind];
				return 1 if(($nRange >= $r) && ($mId == $id));
			} elsif($land->[$sx][$sy] == $HhugeMonsterFireRange) {
				my($mId, $mKind) = (monsterUnpack($landValue->[$sx][$sy]))[0, 5];
				my $nRange = $HnavyFireRange[$nKind];
				return 1 if(($nRange >= $r) && ($mId == $id));
			}
		}
		$tmp = $an[$r];
	}
	return 0;
}

# 着弾点表示
sub missileMapSet {
	my($id, $no) = @_;
	my($line, $m, $turn, $id1, $id2, $id3, $message, @ids, $x, $y, @mS, @mO);
	$no--;
	if(!open(LIN, "${HdirName}/${no}$HlogData")) {
		return 0;
	}
	my %kindName = ('防衛'=>2, '無効'=>1, '怪潜'=>3, '硬化'=>3, '艦潜'=>3, '無害'=>1);
	while($line = <LIN>) {
		chomp($line);
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-]*),(.*)$/;
		($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
		next if($m eq '');
#		next if!($id1 == $id || ($id2 == $id && $id3 == ''));
		next if($id1 != $id);

		my $spliter = "<BR>　--- ";
		my @mes = split(/$spliter/, $message);
		if($mes[1] eq '') {
			$mes[0] =~ /^([^\w]*)(\-)(\-)(\-)(\s)<span(\s)class="islName">\(([0-9]*), ([0-9]*)\)<\/span>/;
			($x, $y) = ($7, $8);
			next if(($x eq '') || ($y eq ''));
			if(($id2 == $id) && !$m) {
				$mS[$x][$y] = 4;
			} else {
				$mO[$x][$y] = 4;
			}
		} else {
			$spliter = "　";
			my @kinds = split(/$spliter/, $mes[1]);
			foreach my $k (@kinds) {
				$spliter = " ⇒ ";
				my($name, $points) = split(/$spliter/, $k);
				my $flag = $kindName{$name};
				while($points =~ /\(([0-9]*), ([0-9]*)\)/g) {
					($x, $y) = ($1, $2);
					next if(($x eq '') || ($y eq ''));
					if(($id2 == $id) && !$m) {
						$mS[$x][$y] = $flag if($mS[$x][$y] < $flag);
					} else {
						$mO[$x][$y] = $flag if($mO[$x][$y] < $flag);
					}
				}
			}
		}
	}

	close(LIN);
	return {
		'self' => \@mS,
		'other' => \@mO,
	};
}

# マーキングモジュール(ドンガバチョさん作成)
sub islandMarking {
	my($island, $mode) = @_;

	out(<<END);
<style type="text/css">
<!--
TD.M {
/*  cursor:url('http://127.0.0.1/navy/img/scope16.ani'); */
  cursor:default;
  white-space : normal;
  border-style:outset;
  border-width:0px;
  border-color:#CCCCFF;
}
-->
</style>
<script type="text/javascript">
<!--
var mArray = new Array();
var lastX = ${\min(@{$island->{'map'}->{'x'}})};
var lastY = ${\min(@{$island->{'map'}->{'y'}})};
var lastN = 217;
var lastF = 0;

// ミサイル範囲のマーキングをセット
function set_mark(x, y) {
	if(!document.mark_form.mark.checked) return false;
	if(!document.getElementById) {
		alert("大変申し訳ありませんが、お使いのブラウザはこの機能をサポートしていません。");
		return false;
	}

	var num  = document.mark_form.number_mark.value;
	var kind = document.mark_form.kind_mark.value;

	if(kind == '') {
		do_mark(lastX, lastY, lastN, '-');

		if(lastF == 1 && lastX == x && lastY == y) {
			lastX = ${\min(@{$island->{'map'}->{'x'}})};
			lastY = ${\min(@{$island->{'map'}->{'y'}})};
			lastF = 0;
			return;
		}
		lastX = x;
		lastY = y;
		lastF = 1;
		kind = 'FFFF00';
	}

	do_mark(x, y, num, kind);
}

function do_mark(x, y, num, kind) {
	var xArray = new Array(${\join(',', @ax)});
	var yArray = new Array(${\join(',', @ay)});
	var cxArray = new Array(${\join(',', @correctX)});
	var cyArray = new Array(${\join(',', @correctY)});

	for (i = 0; i < num; i++) {
		var targetX = x + xArray[i];
		var targetY = y + yArray[i];

		// 行による位置調整
		if(((targetY % 2) == 0) && ((y % 2) == 1)) {
			targetX--;
		}
		targetX = cxArray[targetX + $#an];
		targetY = cyArray[targetY + $#an];
		if(!(targetX < 0 || targetY < 0) && (mapdata[targetY][targetX] != -2)) {
			if(kind == '-') {
				unset_highlight(targetX, targetY);
				mArray[targetX+"x"+targetY] = 0;
			} else {
				set_highlight(targetX, targetY, kind);
				mArray[targetX+"x"+targetY] = 1;
			}
		}
	}
}

END

	if(!$mode) {
		out(<<END);
// 画像をマーキング化
function set_highlight(x, y, color) {
	if(document.getElementById) {
		document.getElementById(x+"x"+y).width  = "${\($HchipSize*2-2)}";
		document.getElementById(x+"x"+y).height = "${\($HchipSize*2-2)}";
		document.getElementById(x+"x"+y).border = "1";
		document.getElementById(x+"x"+y).style.borderColor = "#"+color;
//		if($Hroundmode) {
//			if(!(x%$HislandSizeX) || !(y%$HislandSizeY)) {
//				document.getElementById(x+"wx"+y+"w").width  = "${\($HchipSize*2-4)}";
//				document.getElementById(x+"wx"+y+"w").height = "${\($HchipSize*2-4)}";
//				document.getElementById(x+"wx"+y+"w").border = "2";
//				document.getElementById(x+"wx"+y+"w").style.borderColor = "#"+color;
//			}
//		}
	}
}

// マーキング解除
function unset_highlight(x, y) {
	if(document.getElementById) {
		document.getElementById(x+"x"+y).width  = "${\($HchipSize*2)}";
		document.getElementById(x+"x"+y).height = "${\($HchipSize*2)}";
		document.getElementById(x+"x"+y).border = "0";
//		if($Hroundmode) {
//			if(!(x%$HislandSizeX) || !(y%$HislandSizeY)) {
//				document.getElementById(x+"wx"+y+"w").width  = "${\($HchipSize*2)}";
//				document.getElementById(x+"wx"+y+"w").height = "${\($HchipSize*2)}";
//				document.getElementById(x+"wx"+y+"w").border = "0";
//			}
//		}
	}
}
END
	} else {
		out(<<END);
// 画像をマーキング化
function set_highlight(x, y, color) {
	if(document.getElementById) {
		document.getElementById(x+"x"+y).width  = "${\($HchipSize*2-2)}";
		document.getElementById(x+"x"+y).height = "${\($HchipSize*2-2)}";
		document.getElementById(x+"x"+y).style.filter = "filter: Glow(color=" + color+ ")";
		document.getElementById(x+"x"+y).style.backgroundColor = "#FFFFFF";
		document.getElementById(x+"x"+y).style.borderColor = "#FFFFFF";
		document.getElementById(x+"x"+y).style.Color = "#FFFFFF";
		document.getElementById(x+"x"+y).style.borderWidth = "1";
//		if($Hroundmode) {
//			if(!(x%$HislandSizeX) || !(y%$HislandSizeY)) {
//				document.getElementById(x+"wx"+y+"w").width  = "${\($HchipSize*2-4)}";
//				document.getElementById(x+"wx"+y+"w").height = "${\($HchipSize*2-4)}";
//				document.getElementById(x+"wx"+y+"w").style.filter = "filter: Glow(color=" + color+ ")";
//				document.getElementById(x+"wx"+y+"w").style.backgroundColor = "#FFFFFF";
//				document.getElementById(x+"wx"+y+"w").style.borderColor = "#FFFFFF";
//				document.getElementById(x+"wx"+y+"w").style.Color = "#FFFFFF";
//				document.getElementById(x+"wx"+y+"w").style.borderWidth = "2";
//			}
//		}
	}
}

// マーキング解除
function unset_highlight(x, y) {
	if(document.getElementById) {
		document.getElementById(x+"x"+y).width  = "${\($HchipSize*2)}";
		document.getElementById(x+"x"+y).height = "${\($HchipSize*2)}";
		document.getElementById(x+"x"+y).style.borderWidth = "0";
//		if($Hroundmode) {
//			if(!(x%$HislandSizeX) || !(y%$HislandSizeY)) {
//				document.getElementById(x+"wx"+y+"w").width  = "${\($HchipSize*2)}";
//				document.getElementById(x+"wx"+y+"w").height = "${\($HchipSize*2)}";
//				document.getElementById(x+"wx"+y+"w").style.borderWidth = "0";
//			}
//		}
	}
}
END
	}

	out(<<END);

// 全てのマーキングを解除
function unset_all_highlight() {
	for (f = ${\min(@{$island->{'map'}->{'y'}})}; f <= ${\max(@{$island->{'map'}->{'y'}})}; f++) {
		for (i = ${\min(@{$island->{'map'}->{'x'}})}; i <= ${\max(@{$island->{'map'}->{'x'}})}; i++) {
			if(mArray[i+"x"+f] == 1) {
				unset_highlight(i, f);
			}
		}
	}
}
                                                                                                                            //-->
function mark_menu(){
	if(!document.mark_form.mark.checked){
		unset_all_highlight();
	}else{
		if(document.myForm.MENUOPEN.checked)  { document.myForm.MENUOPEN.checked = false; }
		if(document.myForm.MENUOPEN2.checked) { document.myForm.MENUOPEN2.checked = false; }
		if(document.myForm.MENUOPEN3.checked) { document.myForm.MENUOPEN3.checked = false; }
	}
}
//-->
</script>

<FORM NAME="mark_form" class='mark_form'>
マーキング<INPUT TYPE=CHECKBOX NAME="mark" onClick="mark_menu()">
種類
<SELECT NAME="kind_mark">
<OPTION VALUE="">標準
<OPTION VALUE="FFFF00">Yellow
<OPTION VALUE="FF0000">Red
<OPTION VALUE="0000FF">Blue
<OPTION VALUE="00FF00">Green
<OPTION VALUE="FF00FF">Purple
<OPTION VALUE="CCCCBB">Gray
<OPTION VALUE="-">None
</SELECT>
範囲
<SELECT NAME="number_mark">
END
	my $max = max(2, @HnavyFireHex, @HnavyFireRange);
	foreach (0..$max) {
		my $s = ($_ == 2) ? ' SELECTED' : '';
		out("<OPTION VALUE=\"$an[$_]\"$s>${_}HEX");
	}
	out(<<END);
</SELECT>
　<INPUT TYPE="BUTTON" VALUE="解除" onClick="unset_all_highlight();">
</FORM>
END
}

#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# 個別ログ表示
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HrepeatTurn; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
}

# ○○島へようこそ！！
sub tempPrintIslandHead {
	my($island, $mode) = @_;

	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}「${HcurrentName}」${H_tagName}へようこそ！！${H_tagBig}<BR>
$HtempBack<BR>
</DIV>
<SCRIPT Language="JavaScript">
<!--
var mapX = $island->{'map'}->{'x'}[0];
var mapY = $island->{'map'}->{'y'}[0];

$HnaviExp

function Navi(x, y, img, title, text, exp) { // 2
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";
	if(x - mapX + 1 > $HislandSizeX / 2) {
//		StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // 左側
		StyElm.style.marginLeft = -10; // 左側
	} else {
//		StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // 右側
		StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 90; // 右側
	}
//	if(y - mapY + 1 == $HislandSizeY) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1.5) * $HchipSize*2; // 下側
//	} else if(y - mapY + 1 > $HislandSizeY / 2) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // 下側
//	} else {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // 上側
//	}
	StyElm.innerHTML = "<div class='NaviTitle'>" + title + " (" + x + "," + y + ")<\\/div><table><tr><td class='M'><img class='NaviImg' src=" + img + "><\\/td><td class='M'><div class='NaviText'>" + text + "<\\/div>";
	if(exp) {
		StyElm.innerHTML += "<div class='NaviText'>" + eval(exp) + "<\\/div>";
	}
	StyElm.innerHTML += "<\\/td><\\/tr><\\/table>";
}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
function sv(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	NaviClose();
	status = '';
	return false;
}
END

	if($mode) {
		out(<<END);
function ps(x, y) {
	NaviClose();
	if(opener) {
		window.opener.document.lcForm.POINTX.options[x].selected = true;
		window.opener.document.lcForm.POINTY.options[y].selected = true;
		with (window.opener.document.lcForm.ISLANDID) {
			var i;
			for (i = 0; i < length; i++) {
				if (options[i].value == $HcurrentID) {
					options[i].selected = true;
					break;
				}
			}
		}
		return true;
	}
}
END
	} else {
		out(<<END);
function ps(x, y) {
	NaviClose();
	if (opener) {
		with (opener.document.myForm) {
			POINTX.options[x].selected = true;
			POINTY.options[y].selected = true;
			with (TARGETID) {
				var i;
				for (i = 0; i < length; i++) {
					if (options[i].value == $HcurrentID) {
						options[i].selected = true;
						break;
					}
				}
			}
			window.close();
		}
		return true;
	}
}
END
	}
	out(<<END);
//-->
</SCRIPT>
END
}

# ○○島開発計画
sub tempOwner {
	my($island) = $Hislands[$HcurrentNumber];
	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>
</DIV>
<SCRIPT Language="JavaScript">
<!--
var mapX = $island->{'map'}->{'x'}[0];
var mapY = $island->{'map'}->{'y'}[0];

$HpopupNaviJS
function sv(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	if($HpopupNavi) {
		NaviClose();
	}
	status = '';
	return false;
}
function ps(x, y) {
	if($HpopupNavi) {
		NaviClose();
	}
	with (document.myForm) {
		POINTX.options[x].selected = true;
		POINTY.options[y].selected = true;
		with (TARGETID) {
			var i;
			for (i = 0; i < length; i++) {
				if (options[i].value == $HcurrentID) {
					options[i].selected = true;
					break;
				}
			}
		}
	}
	if(document.mark_form.mark.checked) {
		set_mark(x, y);
	}
	return true;
}

function ns(x) {
	document.myForm.NUMBER.options[x].selected = true;
	return true;
}
function jump(theForm, j_mode, m_mode) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = theForm.TARGETID.options[sIndex].value;
	if (url != "" ) {
		if(m_mode != "") {
			window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode+"&MISSILEMODE="+m_mode, "m", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=450,height=630");
		} else {
			window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=450,height=630");
		}
	}
}
function StatusMsg(x) {
msg = new Array(64);
END
	my($i ,$k);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$k = $HcomList[$i];
		my($Msg) = $HcomMsgs[$k];
		out("msg[$k] = \"$Msg\";\n");
	}
	out(<<END);
	window.status = msg[x];
}
//-->
</SCRIPT>
END

	islandInfo(1);

	out(<<END);
<DIV align='center'>
<TABLE BORDER>
<TR valign=top>
<TD $HbgInputCell >
<FORM name="myForm" action="$HthisFile" method=POST>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$island->{'id'}>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=16 MAXLENGTH=16 class=f>
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
	# 計画番号
	my($j, $s);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		$s = ($i == $HcommandPlanNumber) ? 'SELECTED' : '';
		out("<OPTION VALUE=$i $s>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
END

	#コマンド
	my($kind, $cost);
	my $navyComLevel = gainToLevel($island->{'gain'});
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		next if($HcomName[$kind] eq '');
		next if($HmaxComNavyLevel &&
				($HcomNavy[0] + $HcomNavyNumber[$navyComLevel-1] < $kind) && ($kind <= $HcomNavy[$#HnavyName]));
		next if($HuseCoreLimit && ($kind == $HcomCore) &&
			 ($HislandTurn - $island->{'birthday'} > $HdevelopTurn));
		$cost = $HcomCost[$kind];
		if($cost eq '0') {
			$cost = '無料';
		} elsif($cost =~ /^\@(.*)$/) {
			$cost = $1;
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		if($kind == $HdefaultKind) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		my($style) = ($HcomTurn[$kind] > 0) ? "STYLE='color=${HcomNameColor1};' " : "STYLE='color=${HcomNameColor2};' ";
		out("<OPTION VALUE=$kind ${style}$s>$HcomName[$kind]($cost)\n");
	}

	my $map = $island->{'map'};
	my($x, $y);
	out(<<END);
</SELECT>
<HR>
<B>座標(</B><SELECT NAME=POINTX>

END
	foreach $x (@defaultX) {
		if($x == $HdefaultX) {
			out("<OPTION VALUE=$x SELECTED>$x\n");
		} else {
			out("<OPTION VALUE=$x>$x\n");
		}
	}

	out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

	foreach $y (@defaultY) {
		if($y == $HdefaultY) {
			out("<OPTION VALUE=$y SELECTED>$y\n");
		} else {
			out("<OPTION VALUE=$y>$y\n");
		}
	}
	out(<<END);
</SELECT><B>)</B>
<HR>
<B>数量</B><SELECT NAME=AMOUNT>
END

	# 数量
	foreach $i (0..99) {
		out("<OPTION VALUE=$i>$i\n");
	}

	my($strUseNavy);
	$strUseNavy = "(艦隊移動元)" if($HnavyName[0] ne '');
	out(<<END);
</SELECT>
<HR>
<B>目標の${AfterName}</B>${strUseNavy}：
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> 表\示 </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT><BR>
END
	if($HmlogMap) {
		out(<<END);
<BR><B> 着弾点表\示 </B><BR>
END
		my($i, $turn);
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=JavaScript:void(0); onClick=\"jump(myForm, '$HjavaMode', $i)\">");
			if($i == 1) {
				out("ターン${turn}(現在)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
			out("<BR>\n") if($i%3==1);
		}
	}
	out(<<END);
<div align='left'>艦隊移動先</div>
<SELECT NAME=TARGETID2>
$HtargetList<BR>
</SELECT>
<HR>
<B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$island->{'id'}>
</FORM>
</TD>
<TD $HbgMapCell>
END
	# 艦隊構成を調べる
	my($id, $land, $landValue, $landValue2, $map) = ($island->{'id'}, $island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}, $island->{'map'});
	my(@fleet);
	my(@nFleet) = (0, 0, 0, 0);
	my($x, $y, $nKind, $value, $value2, $name, %invade);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$nKind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			next if ($nKind != $HlandNavy);

			# 他の島の艦隊は除く
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
                        my($goal);
                        if(($goalx == 31) ||
                           ($goaly == 31)) {
                            $goal = "停船中";
                        }else{
                            $goal = "目標($goalx, $goaly)";
                        }

                        $wait--;
                        if($wait <= 0){
                            $ririku = "、発艦準備OK";
                        }else{
                            $ririku = "、離陸待ち${wait}ターン"
                        }

                # 航空機だったら表記変更
                if($HnavyCruiseTurn[$nKind] !=0){
                    $ririku = "、${wait}ターン後に帰投";
                }

                        if(($nKind != 0) && ($nKind != 0x0c)){
                            $ririku = "";
                        }

			if ($nId != $id) {
				$invade{"$nId,$nNo"} += 1;
				next;
			}

                        # 最大耐久力
                        my $maxHp = int($HnavyHP[$nKind] * (120 + $nExp) / 120);

			# 残骸は除く
			next if ($nFlag == 1);

			my $nSpecial = $HnavySpecial[$nKind];
			# 港は除く
			next if ($nSpecial & 0x8);

			$name = $HnavyName[$nKind];
			my $navyLevel = expToLevel($HlandNavy, $nExp);
			push(@{$fleet[$nNo]}, <<END);
<OPTION value="$x,$y">$name (耐久力${nHp}/${maxHp}、レベル${navyLevel}、経験値${nExp}、${goal}${ririku})
END
			$nFleet[$nNo]++;
		}
	}
	@{$fleet[0]} = sort sortOption @{$fleet[0]};
	@{$fleet[1]} = sort sortOption @{$fleet[1]};
	@{$fleet[2]} = sort sortOption @{$fleet[2]};
	@{$fleet[3]} = sort sortOption @{$fleet[3]};

	my $ifname = '';
	foreach (sort { $a cmp $b } keys %invade) {
		my($iId,$iNo) = split(/\,/, $_);
		my $in = $HidToNumber{$iId};
		if(defined $in) {
			my $iName = islandName($Hislands[$in]);
			$ifname .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]艦隊($invade{$_}艦)<BR>"
		} else {
			$ifname .= "所属不明($invade{$_}艦)<BR>";
		}
	}
	$ifname .= '　';
	my $ofname = $island->{'fleet'};
	out(<<END) if($HnavyName[0] ne '');
<FORM NAME="FLEET">
<TABLE border=0 align="center">
<TR><TH>$ofname->[0]艦隊</TH><TD><SELECT onfocus="selectFleetXY(0);" onchange="selectFleetXY(0);">@{$fleet[0]}</SELECT></TD><TD>($nFleet[0]艦)</TD></TR>
<TR><TH>$ofname->[1]艦隊</TH><TD><SELECT onfocus="selectFleetXY(1);" onchange="selectFleetXY(1);">@{$fleet[1]}</SELECT></TD><TD>($nFleet[1]艦)</TD></TR>
<TR><TH>$ofname->[2]艦隊</TH><TD><SELECT onfocus="selectFleetXY(2);" onchange="selectFleetXY(2);">@{$fleet[2]}</SELECT></TD><TD>($nFleet[2]艦)</TD></TR>
<TR><TH>$ofname->[3]艦隊</TH><TD><SELECT onfocus="selectFleetXY(3);" onchange="selectFleetXY(3);">@{$fleet[3]}</SELECT></TD><TD>($nFleet[3]艦)</TD></TR>
<TR><TH>$HtagTH_他島の艦隊$H_tagTH</TH><TD class='N' colspan=2>$ifname</TD></TR>
</TABLE>
</FORM>
<SCRIPT Language="JavaScript">
<!--
function selectFleetXY(n) {
	var iid;
	with (document.FLEET.elements[n]) {
		if (length < 1) { return; }
		iid = options[selectedIndex].value;
	}
	var x, y;
	n = iid.indexOf(',');
	x = iid.substring(0, n);
	y = iid.substring(n + 1, iid.length);
	with (document.myForm) {
		POINTX.options[x].selected = true;
		POINTY.options[y].selected = true;
		with (TARGETID) {
			var i;
			for (i = 0; i < length; i++) {
				if (options[i].value == $HcurrentID) {
					options[i].selected = true;
					break;
				}
			}
		}
	}
}
//-->
</SCRIPT>
END
	islandMap(1, 0, 0); # 島の地図、所有者モード
	islandMarking($island, 0);
	out(<<END);
<FORM NAME=SIGHTS>
<B>目標の${AfterName}</B><BR><SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<INPUT TYPE="button" VALUE="マップを開く" onclick="printIsland();">
</FORM>
<SCRIPT Language="JavaScript">
<!--
function printIsland() {
	var iid;
	with (document.SIGHTS.TARGETID) {
		iid = options[selectedIndex].value;
	}
	window.open("$HthisFile?Sight=" + iid, "_blank", "toolbar=0,location=0,directories=0,menubar=0,status=1,scrollbars=1,resizable=1");
}
//-->
</SCRIPT>
</TD>
<TD $HbgCommandCell>
END

	my $turn  = $HislandTurn + 1;
	my $cflag = $island->{'itemAbility'}[6];
	$cflag = 1 if(!$cflag);
	my $flagST = 0;
	my $count = 0;
	for($i = 0; $i < $HcommandMax; $i++) {
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

	my(@priList, $priListJS, $priSelectList);
	if($HusePriority) {
		my $mypri = $island->{'priority'};
		my($i, $j, $s);
		foreach $i (0..3) {
			$priList[$i] = '(';
			my $pFlag = 0;
			$priListJS .= '[';
			foreach (split(/\-/, $mypri->[$i])) {
				$priList[$i] .= "⇒" if($pFlag);
				$pFlag++;
				$priList[$i] .= "$HpriStr[$_]";
				$priListJS .= "$_";
				$priListJS .= ',' if($pFlag <= $#HpriStr);
			}
			$priList[$i] .= ')';
			$priListJS .= ']';
			$priListJS .= ',' if($i < 3);
		}
		$priSelectList = "";
		$i = 0;
		foreach (split(/\-/, $mypri->[$i])) {
			$priSelectList .= "<BR>　" if($i && $i % 4 == 0);
			$priSelectList .= "⇒" if($i);
			$priSelectList .= "<SELECT NAME=PS${i}>";
			foreach $j (0..$#HpriStr) {
				if($_ == $j) {
					$s = " SELECTED";
				} else {
					$s = "";
				}
				$priSelectList .= "<OPTION VALUE=${j}${s}>$HpriStr[$j]";
			}
			$priSelectList .= "</SELECT>";
			$i++;
		}
	}
	my $comment = $island->{'comment'};
	my @status = ('', '退治', '巡航', '停船');
	my($fkind) = $island->{'fkind'};
	my @flist = @$fkind;
	my @fleetlist = ();
#	my @idx = (0..$#flist);
#	@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
#	@flist = @flist[@idx];
	foreach (@flist) {
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp) = navyUnpack(hex($_));#放置　最悪消す
		next if ($HnavySpecial[$nKind] & 0x8); # 軍港は除外
		my($s, $l) = ();
		my $navyLevel = expToLevel($HlandNavy, $nExp);
		$s = "\n耐久力$nHp/レベル$navyLevel/経験値$nExp";
		$s = " [${status[$nStat]}]" . $s if($nStat);
		if(($eId != $id) && (defined $HidToNumber{$eId})) {
			my $name = islandName($Hislands[$HidToNumber{$eId}]);
			$name =~ s/<[^<]*>//g;
			$s .= "\n${name}へ派遣中";
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
		push(@fleetMove, " <small>移動指令<B>$str</B></small>");
	}

	out(<<END);
</TD></TR>
<TR><TD colspan=3 class='M'><DIV align='center'>
<TABLE BORDER><TR><TD class='M'>
END

	islandInfoWeather() if($HuseWeather); # 気象情報
	islandData(); # 拡張データ
	islandInfoSub(1) if($HnavyName[0] ne ''); # 艦艇DATA

	out(<<END);
</TD></TR></TABLE>
</DIV></TD></TR>
</TABLE>
</DIV>
<HR>
<DIV ID='CommentBox'>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<TABLE BORDER=0>
<TR>
<TH>コメント<BR><small>(全角${HlengthMessage}字まで)</small></TH>
<TD colspan=2><INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"></TD>
</TR>
<TR>
<TH>パスワード</TH><TD colspan=2><INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$island->{'id'}>
</TD>
</TR>
END

	out(<<END) if($HnavyName[0] ne '');
<TR>
</FORM>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH colspan=3>艦隊名変更<small>(全角${HlengthFleetName}字まで)</small> 　()内は索敵順</TH></TR>
<TR><TH>第１艦隊</TH><TD colspan=2>$fleetlist[0]<br><INPUT TYPE=text NAME=FLEET1 SIZE=20 VALUE="$ofname->[0]">艦隊$fleetMove[0] $priList[0]</TD></TR>
<TR><TH>第２艦隊</TH><TD colspan=2>$fleetlist[1]<br><INPUT TYPE=text NAME=FLEET2 SIZE=20 VALUE="$ofname->[1]">艦隊$fleetMove[1] $priList[1]</TD></TR>
<TR><TH>第３艦隊</TH><TD colspan=2>$fleetlist[2]<br><INPUT TYPE=text NAME=FLEET3 SIZE=20 VALUE="$ofname->[2]">艦隊$fleetMove[2] $priList[2]</TD></TR>
<TR><TH>第４艦隊</TH><TD colspan=2>$fleetlist[3]<br><INPUT TYPE=text NAME=FLEET4 SIZE=20 VALUE="$ofname->[3]">艦隊$fleetMove[3] $priList[3]</TD></TR>
<TR><TD colspan=3 align=center><INPUT TYPE=submit VALUE="艦隊名変更" NAME=FleetnameButton$island->{'id'}></TD></TR>
END

	if($HusePriority) {
		out(<<END);
<TR>
</FORM>
<SCRIPT Language="JavaScript">
<!--
function priorityChange() {
	data=[$priListJS];
	document.priorityForm.PS0.value = data[document.priorityForm.PSF.value][0];
	document.priorityForm.PS1.value = data[document.priorityForm.PSF.value][1];
	document.priorityForm.PS2.value = data[document.priorityForm.PSF.value][2];
	document.priorityForm.PS3.value = data[document.priorityForm.PSF.value][3];
	document.priorityForm.PS4.value = data[document.priorityForm.PSF.value][4];
	document.priorityForm.PS5.value = data[document.priorityForm.PSF.value][5];
	document.priorityForm.PS6.value = data[document.priorityForm.PSF.value][6];
	document.priorityForm.PS7.value = data[document.priorityForm.PSF.value][7];
	return true;
}
//-->
</SCRIPT>
<FORM name="priorityForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH>索敵順変更</TH><TD><SELECT NAME=PSF onChange=priorityChange() onClick=priorityChange()>
END
		foreach (0..3) {
			out("<OPTION VALUE=$_>$ofname->[$_]\n");
		}
	out(<<END);
</SELECT>艦隊　</TD><TD>
$priSelectList
<INPUT TYPE=submit VALUE="変更" NAME=PriorityButton$island->{'id'}></TD>
END
	}

	my($earth);
	if($HroundView == 2) {
		my $earthstr = ($island->{'earth'} ? '周辺表示<B><FONT COLOR="#FF0000">する</FONT></B>' : '周辺表示<B><FONT COLOR="#0000FF">しない</FONT></B>');
		$earth = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>周辺表示設定</TH><TD colspan=2>$earthstr<INPUT TYPE=submit VALUE=\"変更\" NAME=EarthButton$island->{'id'}></TD></TR>";
	}

	my($comflag);
	if($HcomflagUse >= 2) {
		my $comflagstr = ($island->{'comflag'} ? 'なくても' : 'なければ');
		my $comflagtmp = ($island->{'comflag'} ? '<FONT COLOR="#FF0000">しない</FONT>' : '<FONT COLOR="#0000FF">する</FONT>');
		$comflag = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>コマンド実行設定</TH><TD colspan=2>コマンドが実行でき${comflagstr}、予定ターンを繰り上げて実行<B>$comflagtmp</B><INPUT TYPE=submit VALUE=\"変更\" NAME=ComflagButton$island->{'id'}></TD></TR>";
	}

	my($preab);
	if($HarmisticeTurn && $HuseCoDevelop) {
		my $preabstr = ($island->{'preab'} ? 'なくても' : 'なければ');
		my $preabtmp = ($island->{'preab'} ? '<FONT COLOR="#FF0000">許可する</FONT>' : '<FONT COLOR="#0000FF">許可しない</FONT>');
		$preab = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>陣営共同開発</TH><TD colspan=2>陣営預かりで${preabstr}、陣営パスワードで開発画面に入ることを<B>$preabtmp</B><INPUT TYPE=submit VALUE=\"変更\" NAME=PreabButton$island->{'id'}></TD></TR>";
	}

	out(<<END);
$earth
$comflag
$preab
</TABLE>
</FORM>
</DIV>
END

}

# 入力済みコマンド表示
sub tempCommand {
	my($island, $number, $turn, $command, $level, $mode) = @_;
	my($kind, $target, $x, $y, $arg, $target2) = (
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'target2'}
	);
	$HcomName[$kind] = "" if(($HmaxComNavyLevel && ($HcomNavy[0] + $HcomNavyNumber[$level] < $kind) && ($kind <= $HcomNavy[$#HnavyName])) ||
							($HuseCoreLimit && ($kind == $HcomCore) && ($HislandTurn - $island->{'birthday'} > $HdevelopTurn)));
	my($name) = ($HcomTurn[$kind] > 0) ? "$HtagComName1_${HcomName[$kind]}$H_tagComName" : "$HtagComName2_${HcomName[$kind]}$H_tagComName";
	my($point) = "$HtagName_($x,$y)$H_tagName";
	my $tn = $HidToNumber{$target};
	my $tName;
	if($tn eq '') {
		$tName = "無人${AfterName}";
	} else {
		$tName = islandName($Hislands[$tn]);
	}
	$tName = "$HtagName_${tName}$H_tagName";
	my($value) = ($arg < 1) ? $HcomCost[$kind] : $arg * $HcomCost[$kind];
	if($value == 0) {
		$value = $HcomCost[$kind];
	} elsif($value < 0) {
		$value = -$value;
		$value = "$value$HunitFood";
	} else {
		$value = "$value$HunitMoney";
	}
	$value = "$HtagName_$value$H_tagName";

	my($j) = sprintf("%02d", $number + 1);

	out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\">") if($mode);
	out("$HtagNumber_$j$H_tagNumber$HnormalColor_($turn)：");
	if(!$HcomUse{$kind}) {
		out("$HtagComName2_このコマンドは使えなくなりました$H_tagComName");
		out("$H_normalColor");
		out("</A>") if($mode);
		out("<BR>\n");
		return;
	}

	my $ofname = $island->{'fleet'};
	my $land = $island->{'land'};
	my $landValue = $island->{'landValue'};

	if(($kind == $HcomDoNothing) ||
	   ($kind == $HcomGiveup) ||
	   ($kind == $HcomPrepare3)) {
		out("$name");
	} elsif (($HcomMissile[0] < $kind) && ($kind <= $HcomMissile[$#HmissileName])) { # ミサイル発射
		# ミサイル系
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		out("$tName$pointへ$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomAmity) {
		# 友好国 設定・解除
		if($target != $island->{'id'}) {
			out("$tNameを$name");
		} else {
			out("<B>全ての${AfterName}</B>を$name");
		}
	} elsif($kind == $HcomAlly) {
		# 同盟 加盟・脱退
		out("$tNameの$name");
	} elsif(($kind == $HcomDeWar) || ($kind == $HcomCeasefire)) {
		# 宣戦布告・停戦
		out("$tNameに$name");
	} elsif(($kind == $HcomSendMonster) ||
		($kind == $HcomSendMonsterST)) {
		# 怪獣派遣
		my $huge = 0;
		if($arg >= 50 && ($HsendHugeMonsterNumber >= 0)) {
			if($arg > 50 + $HsendHugeMonsterNumber) {
				$arg = $HsendHugeMonsterNumber;
				$huge = 1;
			} else {
				$arg -= 50;
				$huge = 1;
			}
		} elsif($arg > $HsendMonsterNumber) {
			$arg = $HsendMonsterNumber;
		}
		my $mName = ($huge) ? $HhugeMonsterName[$arg] : $HmonsterName[$arg];
		out("$tNameへ$name($HtagName_$mName$H_tagName)");
	} elsif (($HcomNavy[0] < $kind) && ($kind <= $HcomNavy[$#HnavyName])) { # 艦艇建造
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name .= "($ofname->[$arg]艦隊)";
		$name = "$pointで$name" if($HnavyBuildFlag);
		if($land->[$x][$y] != $HlandSea || ($HnavyBuildFlag && $landValue->[$x][$y])) {
			out("${HtagDisaster_}！${H_tagDisaster}");
		} elsif($HmaxComPortLevel) {
			my $flag = 0;
			my($p, $px, $py);
			if($HnavyBuildFlag) {
				($p, $px, $py) = searchNavyPort($island, $x, $y, 7);
			} else {
				($p, $px, $py) = searchNavyPort($island, $x, $y, 0);
			}
			my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);#ここは必要なかったかも
			$flag = expToLevel($HlandNavy, $pExp);
			if($flag) {
				if($HcomNavyNumber[($flag - 1)] >= $kind - $HcomNavy[0]) {
					$flag = 1;
				} else {
					$flag = 0;
				}
			}
			out("${HtagDisaster_}！${H_tagDisaster}") if(!$flag);
		}
		out("$name");
	} elsif ($kind == $HcomNavySend) {
		# 艦隊派遣
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("$tNameへ$name");
	} elsif ($kind == $HcomNavyReturn) {
		# 艦隊帰還
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("$tNameから$name");
	} elsif ($kind == $HcomNavyMove) {
		# 艦隊移動
		my $tn2 = $HidToNumber{$target2};
		my $tName2;
		if($tn2 eq '') {
			$tName2 = "無人${AfterName}";
		} else {
			$tName2 = islandName($Hislands[$tn2]);
		}
		$tName2 = "$HtagName_${tName2}$H_tagName";
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		my $comName = ($island->{'id'} == $target2) ? '艦隊帰還' : '艦隊派遣';
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${comName}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${comName}$H_tagComName";
		if($island->{'id'} == $target2) {
			out("$tNameから$name");
		} elsif($island->{'id'} == $target) {
			out("$tName2へ$name");
		} else {
			out("$tNameから$tName2へ$name");
		}
	} elsif ($kind == $HcomNavyForm) {
		# 艦隊編成
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("${HtagDisaster_}！${H_tagDisaster}") if($land->[$x][$y] != $HlandNavy);
		out("$pointで$name");
	} elsif(($kind == $HcomSell) ||
		($kind == $HcomBuy)) {
		# 食料輸出、食料輸入
		my($value2) = ($arg < 1) ? $HcomCost[$kind] : $arg * $HcomCost[$kind];
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood));
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
		if($value2 < 0) {
			$value2 = int(-$value2  * $foodrate / 40);
			$value2 = "$value2$HunitMoney相当";
		} else {
			$value2 = int($value2 / $foodrate * 10 / 4);
			$value2 = "$value2$HunitFood相当";
		}
		$value2 = "$HtagName_$value2$H_tagName";
		out("$name$value ($value2)");
	} elsif(($kind == $HcomPropaganda) ||
                ($kind == $Hcomshikin)) {
		# 誘致活動、資金繰り
		if($arg == 0) {
			out("$name");
		} else {
			out("$name($arg回)");
		}
	} elsif(($kind == $HcomMoney) ||
		($kind == $HcomFood)) {
		# 援助
		out("$tNameへ$name$value");
	} elsif($kind == $HcomDestroy) {
		# 掘削
		if($arg != 0) {
			out("$pointで$name(予算${value})");
		} else {
			out("$pointで$name");
		}
	} elsif($kind == $HcomDbase) {
		# 回数付き
		if(!$arg || !$HdurableDef) {
			if(!$HdurableDef && $land->[$x][$y] == $HlandDefence) {
				out("$pointで$name(自爆)");
			} else {
				out("$pointで$name");
			}
		} elsif($arg == $HdefExplosion && $land->[$x][$y] == $HlandDefence) {
			out("$pointで$name(自爆)");
		} else {
			out("$pointで$name($arg回)");
		}
	} elsif(($kind == $HcomFarm) ||
		 ($kind == $HcomFastFarm) ||
		 ($kind == $HcomFactory) ||
		 ($kind == $HcomFastFactory) ||
		 ($kind == $HcomMountain)) {
		# 回数付き
		if($arg == 0) {
			out("$pointで$name");
		} else {
			out("$pointで$name($arg回)");
		}
	} elsif (($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) { # 複合地形建設
		# 回数付き
		if($arg == 0) {
			out("$pointで$name");
		} else {
			out("$pointで$name($arg回)");
		}
	} elsif($kind == $HcomSeaMine) {	
		# 破壊力付き
		$arg = 1 if($arg == 0);
		$arg = $HmineDamageMax if($arg > $HmineDamageMax);
		if($land->[$x][$y] == $HlandSeaMine) {
			$name = ($HcomTurn[$kind] > 0) ? "${HtagComName1_}機雷除去${H_tagComName}" : "${HtagComName2_}機雷除去${H_tagComName}";
		} else {
			$name .= "(破壊力:$arg)";
		}
		out("$pointで$name");
	} elsif(($kind == $Hcomgoalsetpre) ||
	        ($kind == $Hcomgoalset)) {
                # 目的地設定
		out("$tName$pointで$name");
	} elsif($kind == $HcomMoveTarget) {
		# 方向付き
		my $s;
		$arg %= 19;
		if($arg == 1) {
			$s = '右上';
		} elsif($arg == 2) {
			$s = '右';
		} elsif($arg == 3) {
			$s = '右下';
		} elsif($arg == 4) {
			$s = '左下';
		} elsif($arg == 5) {
			$s = '左';
		} elsif($arg == 6) {
			$s = '左上';
		} elsif(($arg > 6) && ($arg < 19)) {
			$arg -= 6;
			$s = "$arg時";
		} else {
			$arg = 0;
			$s = '待機';
		}
		out("${HtagDisaster_}！${H_tagDisaster}") if(($target == $id) && ($land->[$x][$y] != $HlandNavy));
		out("$tName$pointで移動操縦($s)");
	} elsif($kind == $HcomMoveMission) {
		my $s;
		my $fNo = $arg % 10;
		my $flg = int($arg / 10);
		if ($fNo < 1) {
			$fNo = 1;
		} elsif ($fNo > 4) {
			$fNo = 4;
		}
		if($flg) {
			out("$name$ofname->[$fNo - 1]艦隊に対する${name}を${HtagName_}解除${H_tagName}");
		} else {
			out("$name$ofname->[$fNo - 1]艦隊に対し$tName$pointへの${name}");
		}
	} elsif($kind == $HcomNavyTarget) {
		out("$tName$pointへ$name");
	} elsif($kind == $HcomMonument) {
		if($HuseBigMissile && ($land->[$x][$y] == $HlandMonument)) {
			out("$pointで$name($tNameへ発射)");
		} else {
			$arg = $HmonumentNumber - 1 if($arg >= $HmonumentNumber);
			out("$pointで$name($HmonumentName[$arg])");
		}
	} elsif($kind == $Hcomremodel){
                # 換装
                my $tmp;
                if($arg == 0){
                    $tmp = '対潜';
                }elsif($arg == 1){
                    $tmp = '水雷';
                }elsif($arg == 2){
                    $tmp = '防空';
                }else{
                    $tmp = '対地';
                }
		out("$pointで$name($tmp)");
	} elsif($kind == $Hcomwork){
                # 展開
                my $tmp;
                if($arg == 0){
                    $tmp = '軍港';
                }elsif($arg == 1){
                    $tmp = '海防';
                }elsif($arg == 2){
                    $tmp = '採掘';
                }else{
                    $tmp = '定置';
                }
		out("$tName$pointで$name($tmp)");
	} elsif($kind == $HcomNavyDestroy){
                # 艦隊破棄
		out("$tName$pointで$name");
	} elsif($kind == $HcomSellPort){
                # 軍港払下げ
		out("$tName$pointで$name");
	} elsif($kind == $HcomBuyPort){
                # 軍港買収
		out("$tName$pointで$name");
	} else {
		# 座標付き
		out("$pointで$name");
	}
	out("$H_normalColor");
	out("</A>") if($mode);
	out("<BR>\n");
}

# コマンド削除
sub tempCommandDelete {
	out(<<END);
${HtagBig_}コマンドを削除しました。${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
	out(<<END);
${HtagBig_}コマンドを登録しました。${H_tagBig}<HR>
END
}

# コメント変更成功
sub tempComment {
	out(<<END);
${HtagBig_}コメントを更新しました。${H_tagBig}<HR>
END
}

# 艦隊名変更成功
sub tempFleetName {
	out(<<END);
${HtagBig_}艦隊名を変更しました。${H_tagBig}<HR>
END
}

# 索敵順変更成功
sub tempPriority {
	out(<<END);
${HtagBig_}索敵順を変更しました。${H_tagBig}<HR>
END
}

# 近況
sub tempRecent {
	my($mode, $mode2) = @_;

	my($enPass) = $HdefaultPassword;
	my($pass) = $mode ? "<INPUT type=hidden name=PASSWORD value=$enPass size=16 maxlength=16>" : '';
	if($mode2) {
		out(<<END);
<SCRIPT Language="JavaScript">
<!--
function Recent(){
	newRecent = window.open("", "newRecent", "menubar=yes,toolbar=no,location=no,directories=no,status=no,scrollbars=yes,resizable=yes,width=800,height=300");
	document.recentForm.target = "newRecent";
//	document.recentForm.submit();
}
//-->
</SCRIPT>
<DIV ID='RecentlyLog'><DIV align='center'>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST">
<HR>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}の近況${H_tagBig}
<INPUT type=hidden name="ID" value="$HcurrentID">
$pass
<INPUT type="submit" value="近況を見る" onClick="Recent()">
</FORM>
</DIV></DIV>
END
	} else {
		out(<<END);
<DIV ID='RecentlyLog'>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST">
<HR>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}の近況${H_tagBig}
　<a HREF="${HbaseDir}/history.cgi?ID=$HcurrentID&Event=99" onClick="document.recentForm.target='newWindow';document.recentForm.submit();return false;" style="text-decoration:none;" target='_blank'>[過去${HtopLogTurn}ターン分のログを表示]</a>
<INPUT type=hidden name="ID" value="$HcurrentID">
<INPUT type=hidden name="Event" value="99">
$pass
END
		logPrintLocal($mode);
		out("</FORM></DIV>");
	}
}

# 島の移動
sub islandJamp {
	$HtargetList = getIslandList($HcurrentID, 1);
	out(<<END);
<DIV align='center'>
<SCRIPT LANGUAGE="JavaScript">
function jump(theForm) {
  var sIndex = theForm.urlsel.selectedIndex;
  var url = theForm.urlsel.options[sIndex].value;
  if (url != "" ) location.href = "$HthisFile?Sight=" +url;
}
</SCRIPT>
<TABLE align=center border=0>
<TR><TD>
<FORM name="urlForm">
<SELECT NAME="urlsel">
$HtargetList<BR>
</SELECT>
</TD>
<TD><input type="button" value=" GO " onClick="jump(this.form)"></TD>
</TR></TABLE>
</form>
</DIV>
END
}

sub exLbbs {
	my($bbsID, $mode) = @_;
	my($admin, $id) = ('', '');
	if($mode == 1) {
		$mode = 'yes';
		$id = $bbsID;
		my $island = $Hislands[$HidToNumber{$bbsID}];
		my $onm = $island->{'onm'};
		my $name = islandName($island);
		$onm = "${name}" if($onm eq '');
		$admin =<<"END";
<INPUT type=hidden name=name value='$onm'>
<INPUT type=hidden name=title value='${name}観光掲示板'>
<INPUT type=hidden name=message value='ようこそ！${name}観光案内所へ'>
END
	} elsif($defaultID ne '') {
		$mode = 'no';
		$id = $defaultID;
	} else {
		$mode = '';
	}

	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function Exlbbs(){
	newExlbbs = window.open("", "newExlbbs", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=600,height=300");
	document.exLbbs.target = "newExlbbs";
//	document.exLbbs.submit();
}
//-->
</SCRIPT>
<HR>
<DIV align='center'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}観光者通信${H_tagBig}<BR>
<FORM name="exLbbs" action="${HlbbsDir}/lbbs.cgi" method=POST encType=multipart/form-data>
<INPUT type=hidden name=mode value='view'>
$admin
<INPUT type=hidden name=owner value="$mode">
<INPUT type=hidden name=logfile value="${bbsID}.cgi">
<INPUT type=hidden name=id value="$id">
<INPUT type=hidden name=pass value="$HdefaultPassword">
<INPUT type=submit value='観光掲示板の閲覧・投稿' onClick="Exlbbs()">
</FORM>
</DIV>
END
}

# 深い海の面積を計算
sub calcSea {
	my($island) = @_;

	my($sea) = 0;

	# 地形を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# 数える
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$sea++ if(($land->[$x][$y] == $HlandSea) && !$landValue->[$x][$y]);
	    }
	}

	return $sea;
}
#----------------------------------------------------------------------
# 管理人による地形データ保存・復元
#----------------------------------------------------------------------
sub islandSaveMain() {

	if (!$HisaveMode || !$HcurrentID) {
		# 開放
		unlock();
		# テンプレート出力
		tempIslandSavePage(0);
		return;
	} else {
		# パスワード
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if(!checkPassword($island, $HdefaultPassword) && !checkSpecialPassword($HdefaultPassword)) {
			# パスワードチェック
			# 特殊パスワード
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
	if(checkSpecialPassword($HdefaultPassword) && $HisaveMode > 1) {
		readIslandsFile(-2);
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if($HisaveMode == 2) {
			# 保存
			island_save($island, $HsavedirName, 'save', 0);
		} elsif($HisaveMode == 3) {
			# 復元
			island_load($island, 0);
		} elsif($HisaveMode == 4) {
			# 保存・復元(データの入れ替え)
			island_load($island, 1);
		} elsif($HisaveMode == 5) {
			# 保存(海軍を除く)
			island_save($island, $HsavedirName, 'save', 1);
		} elsif($HisaveMode == 6) {
			# 復元(海軍を除く)
			island_load($island, 2);
		} elsif($HisaveMode == 7) {
			# 保存・復元(海軍を除く)
			island_load($island, 3);
		}
	}
	# 開放
	unlock();
	# テンプレート出力
	tempIslandSavePage(1);
}

# 地形データ保存・復元ページ
sub tempIslandSavePage() {
	my($mode) = @_;

	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>地形データ保存・復元</H1>
<FORM action="$HthisFile" method="POST">
<B>地形データを保存・復元する${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}を選択して下さい-
$HislandList
</SELECT><BR><BR>
パスワード:<INPUT TYPE="password" NAME="ISave" VALUE="$HdefaultPassword" MAXLENGTH=32 class=f>
<INPUT TYPE="submit" VALUE="データ確認" NAME="IslandChoice"><BR>
</FORM>
END

	return if(!$mode);

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	out(<<END);
<HR>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME="ISave" VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME="ISLANDID" VALUE="$HcurrentID">
<TABLE BORDER>
<TR><TD class='T'>
<H1 style='display:inline'>ターン${HislandTurn}現在</H1>
<BR>${HtagTH_}資金：<span class='money'>$island->{'money'}$HunitMoney</span>
　食料：<span class='food'>$island->{'food'}$HunitFood</span>${H_tagTH}
END
	printMap($land, $landValue, $map, 1);
	if(checkSpecialPassword($HdefaultPassword)) {
		out("<INPUT TYPE=\"submit\" VALUE=\"保存\" NAME=\"SaveButton\">");
		out("<INPUT TYPE=\"submit\" VALUE=\"保存(海軍を除く)\" NAME=\"SaveLandButton\">");
	}
	out("</TD>");

	my $savedata = 0;
	if(-e "${HsavedirName}/${HcurrentID}_save.${HsubData}") {
		$savedata = 1;
		open(LIN, "${HsavedirName}/${HcurrentID}_save.${HsubData}");
		chomp(my @line = <LIN>);
	    close(LIN);
	    
		my(@tmp)= splice(@line, 0, 36);
		my(@mandf) = splice(@tmp, 8, 25);
		my $money = shift(@mandf);   # 資金
		my $food = shift(@mandf);    # 食料
		my $tmp = pop(@mandf);       # マップ
		my(@xytmp) = split(/<>/, $tmp);
		my(@x) = split(/\,/, $xytmp[0]);
		my(@y) = split(/\,/, $xytmp[1]);
		my $map = { 'x' => \@x, 'y' => \@y };
		$map = $island->{'map'} if(!@x || !@y || !$HoceanMode);

		($land, $landValue) = readLand($map, @line);

		out(<<END);
<TD class='T'>
<H1 style='display:inline'>セーブデータ</H1>
<BR>${HtagTH_}資金：<span class='money'>${money}${HunitMoney}</span>
　食料：<span class='food'>${food}${HunitFood}</span>${H_tagTH}
END
		printMap($land, $landValue, $map, 1);
		if(checkSpecialPassword($HdefaultPassword)) {
			out("<INPUT TYPE=\"submit\" VALUE=\"復元\" NAME=\"LoadButton\">");
			out("<INPUT TYPE=\"submit\" VALUE=\"復元(海軍を除く)\" NAME=\"LoadLandButton\">");
		}
	}
	out("</TD></TR>");
	if($savedata && checkSpecialPassword($HdefaultPassword)) {
		out("<TR><TD class='T' colspan=2>");
		out("<INPUT TYPE=\"submit\" VALUE=\"保存・復元(データの入れ替え)\" NAME=\"ChangeButton\">");
		out("<INPUT TYPE=\"submit\" VALUE=\"保存・復元(海軍を除く)\" NAME=\"ChangeLandButton\">");
		out("</TD></TR>");
	}
	out("</TABLE>");
	out("</FORM>");
	out("</DIV>");
}

#------------------------------------------------
# トーナメントモード
#------------------------------------------------
# 敗戦時マップ表示
sub fightMap {
	my($mode) = @_;

	my $filename = (!($mode % 2)) ? "${HfightdirName}/${HcurrentID}_lose.${HsubData}" : "${HsavedirName}/${HcurrentID}_save.${HsubData}";
	if(!open(IN, "$filename")) {
		unlock();
		tempProblem();
		return;
	}

	my($name, $owner, $birthday, $id, $prize, $absent, $preab, $comflag, $comment, $password, $money, $food,
		$pop, $area, $farm, $factory, $mountain, $tmp, @amity, @fleet, @priority, @fkind, $gain, $monskill, $monslive,
		@sinktmp, @sink, @sinkself, @subSink, @subSinkself, @exttmp, @ext, @subExt, $field, @item, @weather,
		$fight_id, $rest, @event, $point, @defeat ,%epoint, @epointtmp, @x, @y, $map, $wmap);
	chomp($name = <IN>);     # 島の名前
	chomp($owner = <IN>);    # オーナーの名前
	$birthday = int(<IN>);   # 開始ターン
	$id = int(<IN>);         # ID番号
	chomp($prize = <IN>);    # 受賞
	chomp(($absent, $preab, $comflag) = split(/\,/, <IN>)); # 連続資金繰り数, 開発委託(陣営あずかり), コマンド実行設定
	chomp($comment = <IN>);  # コメント
	chomp($password = <IN>); # 暗号化パスワード
	$money    = int(<IN>);   # 資金
	$food     = int(<IN>);   # 食料
	$pop      = int(<IN>);   # 人口
	$area     = int(<IN>);   # 広さ
	$farm     = int(<IN>);   # 農場
	$factory  = int(<IN>);   # 工場
	$mountain = int(<IN>);   # 採掘場
	chomp($tmp = <IN>);      # 友好国
		@amity = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 艦隊名
		@fleet = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 索敵順
		@priority = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # 保有艦艇種類
		@fkind = split(/\,/, $tmp);
	$gain     = int(<IN>);   # 総獲得経験値
	$monskill = int(<IN>);   # 怪獣退治数
	chomp($monslive = <IN>); # 怪獣出現数, 種類, 種類(巨大), 所属不明艦艇出現数, 種類
	chomp($tmp = <IN>);      # 撃沈数
		@sinktmp = split(/\-/, $tmp);
			@sink = split(/\,/,$sinktmp[0]);        # 自島以外の艦艇
			@sinkself = split(/\,/,$sinktmp[1]);    # 自島
			@subSink = split(/\,/,$sinktmp[2]);     # サブ自島以外の艦艇
			@subSinkself = split(/\,/,$sinktmp[3]); # サブ自島
	chomp($tmp = <IN>);      # 拡張領域
		@exttmp = split(/<>/, $tmp);
			@ext = split(/\,/,$exttmp[0]);    # 拡張領域
			# 勝利フラグ, 貢献度x10, 防撃破, ミ撃破, 民救出, 弾飛来, 弾発射, 弾防御, 艦派遣, 艦来襲, 艦破壊
			@subExt = split(/\,/,$exttmp[1]); # サブ拡張領域
			# 記録ターン, 貢献度x10, 防撃破, ミ撃破, 民救出, 弾飛来, 弾発射, 弾防御, 艦派遣, 艦来襲, 艦破壊, 退治数, 報奨金
	chomp($field = <IN>);    # フィールド属性
	chomp($tmp = <IN>);      # アイテム
		@item = split(/\,/, $tmp);
	chomp($tmp = <IN>); # 気温,気圧,湿度,風速,地盤,波力,異常,天候(ログ表示数)
		$tmp = "20,1013,40,0,0,0,0,2,2,2,2" if($tmp == '');
		@weather = split(/\,/, $tmp);
	chomp(($fight_id, $rest) = split(/\,/, <IN>)); # トーナメント 対戦相手ID, 開発停止残りターン数
	chomp($tmp = <IN>); # イベントフラグ 開始ターン 期間 艦艇数 艦種 制限 タイプ 報償金 報償食料 管理人プレゼントの有無 報償アイテム 追加派遣 怪獣出現1 怪獣出現2 巨大怪獣出現1 巨大怪獣出現2 艦艇出現1 艦艇出現2 自動帰還
		$tmp = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" if($tmp == '');
		@event = split(/\,/, $tmp);
	$point = int(<IN>); # ポイント
	chomp($tmp = <IN>); # 沈没させた島名,ターン数,・・・
		@defeat = split(/\,/, $tmp);
	chomp($tmp = <IN>); # イベントポイント
		@epointtmp = split(/\,/, $tmp);
		for($i=0;$i<$#epointtmp;$i+=2) {
			$epoint{$epointtmp[$i]} = $epointtmp[$i+1];
		}
	chomp($tmp = <IN>);      # マップ配列格納 x0,x1,...,xn<>y0,y1,...,yn
		@xytmp = split(/<>/, $tmp);
		@x = split(/\,/, $xytmp[0]);
		@y = split(/\,/, $xytmp[1]);
		if(!@x || !@y || !$HoceanMode) {
			@x = @defaultX;
			@y = @defaultY;
		}
		$map = { 'x' => \@x, 'y' => \@y };
		$wmap = { 'x' => $xytmp[2], 'y' => $xytmp[3] };
	<IN>; # 予備
	<IN>; # 予備
	<IN>; # 予備
	chomp(my @line = <IN>);
    close(IN);
    
	my(@land) = readLand($map, @line);

	if($HcurrentID != $id) {
		unlock();
		tempProblem();
		return;
	}

	my(@command, @lbbs);
	# 初期コマンドを生成
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$command[$i] = {
			'kind' => $HcomDoNothing,
			'target' => 0,
			'x' => 0,
			'y' => 0,
			'arg' => 0,
			'target2' => 0
		};
	}
	# 初期掲示板を作成
	@lbbs = ();

	my($newID);
	my $num = $HidToNumber{$HcurrentID};
	my $island = $Hislands[$num];
	if(defined $num) {
		if(($island->{'id'} == $id) && ($island->{'name'} eq $name) && ($island->{'owner'} eq $owner) && ($island->{'password'} eq $password)) {
			$newID = $HcurrentID;
			if(($HoceanMode) && (($island->{'wmap'}->{'x'} != $wmap->{'x'}) || ($island->{'wmap'}->{'y'} != $wmap->{'y'}))) {
				$wmap = $island->{'wmap'};
				$map  = $island->{'map'};
			}
		} elsif(($mode >= 3) && ($HislandNumber - $HbfieldNumber >= $HmaxIsland)) {
			# 開放
			unlock();

			out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}${AfterName}が一杯で復元できません！！${H_tagBig}
END
			return;
		} else {
			# IDの使い回し
			my $safety = 100;
			while(defined $HidToNumber{$HislandNextID}) {
				$HislandNextID ++;
				$HislandNextID = 1 if($HislandNextID > 100);
				last if(!$safety--);
			}
			$newID = $HislandNextID;
			$num   = $HislandNumber;
			$HidToNumber{$newID} = $num;
			if($mode >= 3) {
				# 復元モード
				$HislandNumber++;
				$islandNumber++;
				$HislandNextID ++;
				$HislandNextID = 1 if($HislandNextID > 100);
				require('./hako-make.cgi');
				# ログファイル調整
				logFileAdjust(-1, $newID);
				# 地形データ、掲示板調整
				islandFileAdjust(-1, $newID);
				if($HoceanMode) {
					$wmap = randomIslandMap() if(defined $HidToNumber{$HoceanMap[$wmap->{'x'}][$wmap->{'y'}]}); # 島の座標を決める
					@x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
					@y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
					$map = { 'x' => \@x, 'y' => \@y };
				}
			}
		}
	} elsif(($mode >= 3) && ($HislandNumber - $HbfieldNumber >= $HmaxIsland)) {
		# 開放
		unlock();

		out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}${AfterName}が一杯で復元できません！！${H_tagBig}
END
		return;
	} else {
		$newID = $HcurrentID;
		$num   = $HislandNumber;
		$HidToNumber{$newID} = $num;
		if($mode >= 3) {
			# 復元モード
			$HislandNumber++;
			$islandNumber++;
			if($HoceanMode) {
				$wmap = randomIslandMap() if(defined $HidToNumber{$HoceanMap[$wmap->{'x'}][$wmap->{'y'}]}); # 島の座標を決める
				@x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
				@y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
				$map = { 'x' => \@x, 'y' => \@y };
			}
		}
	}
	# land,landValue調整
	if($HoceanMode) {
		my(@l)  = @{$Hworld->{'land'}};
		my(@lv) = @{$Hworld->{'landValue'}};
		my $ofs = min(@{$map->{'y'}});
		my $len = @{$map->{'y'}};
		foreach $x (@{$map->{'x'}}) {
			@{$land[0]->[$x]} = splice(@{$land[0]->[$x]}, $ofs, $len);
			@{$land[1]->[$x]} = splice(@{$land[1]->[$x]}, $ofs, $len);
			splice(@{$l[$x]},  $ofs, $len, @{$land[0]->[$x]});
			splice(@{$lv[$x]}, $ofs, $len, @{$land[1]->[$x]});
		}
		@land = (\@l, \@lv);
	}
	$Hislands[$num] = {
		'name' => $name,
		'owner' => $owner,
		'birthday' => $birthday,
		'id' => $newID,
		'prize' => $prize,
		'absent' => $absent,
		'preab' => $preab,
		'comflag' => $comflag,
		'earth' => $earth,
		'comment' => $comment,
		'password' => $password,
		'money' => $money,
		'food' => $food,
		'pop' => $pop,
		'area' => $area,
		'farm' => $farm,
		'factory' => $factory,
		'mountain' => $mountain,
		'amity' => \@amity,
		'fleet' => \@fleet,
		'priority' => \@priority,
		'fkind' => \@fkind,
		'gain' => $gain,
		'monsterkill' => $monskill,
		'monsterlive' => $monslive,
		'sink' => \@sink,
		'sinkself' => \@sinkself,
		'subSink' => \@subSink,
		'subSinkself' => \@subSinkself,
		'ext' => \@ext,
		'subExt' => \@subExt,
		'field' => $field,
		'item' => \@item,
		'weather' => \@weather,
		'fight_id' => $fight_id,
		'rest' => $rest,
		'event' => \@event,
		'point' => $point,
		'defeat' => \@defeat,
		'epoint' => \%epoint,
		'wmap' => $wmap,
		'map' => $map,
		'land' => $land[0],
		'landValue' => $land[1],
		'command' => \@command,
		'lbbs' => \@lbbs,
	};
	$islandName = islandName($Hislands[$num]);

	unlock();
	if($mode <= 2) {
		my $titleStr = (!$mode) ? '敗戦時の様子' : '保存地形の状況';
	    out ("<DIV align='center'>");
		if($mode) {
			my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;
			out("$HtempBack2<BR>");
		} else {
			out("<a href=${HthisFile}?FightLog=0>${HtagBig_}戻る${H_tagBig}</a><BR>");
		}
	    out ("<BR>${HtagBig_}${HtagName_}「${islandName}」<BR>${H_tagName}$titleStr${H_tagBig}<BR>");
		printMap($land[0], $land[1], $map, 0);

	} elsif(($mode >= 3) && checkSpecialPassword($HdefaultPassword)) {
		# 復元モード
		my $HtempBack2 = "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}";

		require('./hako-turn.cgi');
		# 人口その他算出
		estimate($num);
		islandSort($HrankKind, 1);

		# データ書き出し
		writeIslandsFile($newID);

		# 開放
		unlock();

		out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$islandNameを復元しました。${H_tagBig}
END
		return;

	} else {
		unlock();
		tempProblem();
		return;
	}
}

# 敗戦時の様子表示(敗戦の島データ，保存データ)
sub printMap {
	my($land, $landValue, $map, $mode) = @_;
	my($l, $lv);

	out (<<END);
<SCRIPT Language="JavaScript">
<!--
END

	out (<<END) if(!$mode);
var mapX = $map->{'x'}[0];
var mapY = $map->{'y'}[0];

$HnaviExp

function Navi(x, y, img, title, text, exp) { // 3
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";
	if(x - mapY + 1 > $HislandSizeX / 2) {
//		StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // 左側
		StyElm.style.marginLeft = -10; // 左側
	} else {
//		StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // 右側
		StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 120; // 右側
	}
//	if(y - mapY + 1 == $HislandSizeY) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY + 0.5) * $HchipSize*2; // 下側
//	} else if(y - mapY + 1 > $HislandSizeY / 2) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // 下側
//	} else {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // 上側
//	}
	StyElm.innerHTML = "<div class='NaviTitle'>" + title + " (" + x + "," + y + ")<\\/div><table><tr><td class='M'><img class='NaviImg' src=" + img + "><\\/td><td class='M'><div class='NaviText'>" + text + "<\\/div>";
	if(exp) {
		StyElm.innerHTML += "<div class='NaviText'>" + eval(exp) + "<\\/div>";
	}
	StyElm.innerHTML += "<\\/td><\\/tr><\\/table>";
}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
function ns(x) {
    return true;
}
END

	out (<<END);
function sv(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	if($HpopupNavi) {
		NaviClose();
	}
	status = '';
	return false;
}
function ps(x, y) {
    return true;
}
//-->
</SCRIPT>
END
	out("<DIV ID='islandMap'><TABLE BORDER class='mark'><TR><TD>");
	# 座標(上)を出力
	out("<nobr>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	my($x, $y, $v2, $v1, $v0, $csize2, $csize1, $csize0, $i, $j);
	my(@mx) = @{$map->{'x'}};
	my(@my) = @{$map->{'y'}};
	foreach $x (@mx) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		unless ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("</nobr><BR>");

	# 各地形および改行を出力
	foreach $y (@my) {
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);
		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			# 偶数行目なら番号を出力
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		}

		# 各地形を出力
		$HpopupNavi = 0 if($mode);
		foreach $x (@mx) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $lv2, $x, $y, $mode, '', 0, 0, 0);#ここは使わないんで放置
			out("</A>");
		}

		if($y % 2) {
			# 奇数行目なら番号を出力
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}

		# 改行を出力
		out("</BR>\n");
	}

	# 座標(下)を出力
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	foreach $x (@mx) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		if ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HchipSize*2/3);
				$csize1 = int(($HchipSize*2-$csize2)/2);
				$csize0 = $HchipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HchipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<BR>");
	out("<div id='NaviView'></div>");
	out("</TD></TR></TABLE></DIV>\n");
}

#----------------------------------------------------------------------
# 拡張データカウンター設定
#----------------------------------------------------------------------
sub islandCounterMain() {

	if(!$HcounterSetting && !checkSpecialPassword($HdefaultPassword)) {
			unlock();
			tempProblem();
			return;
	}
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	if (!$HicounterMode || !$HcurrentID) {
		# 開放
		unlock();
		# テンプレート出力
		tempIslandCounterPage(0);
		return;
	} else {
		# パスワード
		if(!checkPassword($island, $HdefaultPassword) && !checkSpecialPassword($HdefaultPassword)) {
			# パスワードチェック
			# 特殊パスワード
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
	if(checkPassword($island, $HdefaultPassword) && $HicounterMode > 1) {
		readIslandsFile();
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if($HicounterMode == 2) {
			# カウンター設定(リセット)
			$island->{'subSink'} = $island->{'sink'};
			$island->{'subSinkself'} = $island->{'sinkself'};
			my @ext = @{$island->{'ext'}};
			shift(@ext);
			unshift(@ext, $HislandTurn);
			push(@ext, $island->{'monsterkill'});
			push(@ext, 0);
			#undef $island->{'subExt'};
			$island->{'subExt'} = \@ext;
		} elsif($HicounterMode == 3) {
			# カウンター消去
			my $n = @HnavyName;
			my(@navy) = ((0)x$n);
			my(@subExt) = ($island->{'birthday'}, (0)x12); # 0〜12
			$island->{'subSink'} = \@navy;
			$island->{'subSinkself'} = \@navy;
			$island->{'subExt'} = \@subExt;
		} elsif($HicounterMode == 4) {
			# 全島カウンター設定(リセット)
			foreach ($HbfieldNumber..$islandNumber) {
				my($island) = $Hislands[$_];
				$island->{'subSink'} = $island->{'sink'};
				$island->{'subSinkself'} = $island->{'sinkself'};
				my @ext = @{$island->{'ext'}};
				shift(@ext);
				unshift(@ext, $HislandTurn);
				push(@ext, $island->{'monsterkill'});
				push(@ext, 0);
				#undef $island->{'subExt'};
				$island->{'subExt'} = \@ext;
			}
		} elsif($HicounterMode == 5) {
			# 全島カウンター消去
			my $n = @HnavyName;
			my(@navy) = ((0)x$n);
			my(@subExt) = ($island->{'birthday'}, (0)x12); # 0〜12
			foreach ($HbfieldNumber..$islandNumber) {
				my($island) = $Hislands[$_];
				$island->{'subSink'} = \@navy;
				$island->{'subSinkself'} = \@navy;
				$island->{'subExt'} = \@subExt;
			}
		}
		writeIslandsFile();
	}
	# 開放
	unlock();
	# テンプレート出力
	tempIslandCounterPage(1);
}

# 拡張データ カウンター設定ページ
sub tempIslandCounterPage() {
	my($mode) = @_;

	# 「戻る」リンク2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>拡張データ カウンター設定</H1>
<FORM action="$HthisFile" method="POST">
<B>カウンターを設定する${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}を選択して下さい-
$HislandList
</SELECT><BR><BR>
パスワード:<INPUT TYPE="password" NAME="ICounter" VALUE="$HdefaultPassword" MAXLENGTH=32 class=f>
<INPUT TYPE="submit" VALUE="ログイン" NAME="IslandChoice"><BR>
</FORM>
END

	if(!$mode) {
		out("</DIV>");
		return;
	}

	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($name) = islandName($island);
	my($next) = $HislandTurn + 1;
	out(<<END);
<HR>
<FORM action="$HthisFile" method="POST"><TABLE BORDER><TR><TD class='M' colspan=2>
<INPUT TYPE="hidden" NAME="ICounter" VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME="ISLANDID" VALUE="$HcurrentID">
<H1 style='display:inline'>ターン${HislandTurn}現在 $HtagName_$name$H_tagName</H1>
END
	islandData(); # 拡張データ
	islandInfoSub(1) if($HnavyName[0] ne ''); # 艦艇DATA

	out(<<END) if(checkPassword($island, $HdefaultPassword));
</TD></TR><TR>
<TD><INPUT TYPE="submit" VALUE="セット\norリセット" NAME="SetButton"></TD>
<TD>まだセットしていない場合は、「ターン$next〜現在」のデータ欄(カウンター)が追加されます。<BR>
すでにセットしている場合、カウンターが初期化されます。
</TD>
</TR><TR>
<TD align='center'><INPUT TYPE="submit" VALUE="消去" NAME="DelButton"></TD>
<TD>「ターン○○〜現在」のデータ欄(カウンター)が消去されます。<BR>カウンターは初期化されます。</TD>
</TR>
<TR><TD class='M' colspan=2>
※一度ボタンを押すとカウンターを元に戻すことはできませんので注意してください。<BR>
※島発見時からカウントされているデータは、プレイヤーには変更できません！<BR>
　 (注！発見されたばかりの$AfterNameは、カウンターをセットできません。)
</TD></TR>
END
	out(<<END) if(checkSpecialPassword($HdefaultPassword));
<TR><TD colspan=2>
<INPUT TYPE="submit" VALUE="全${AfterName}セットorリセット" NAME="AllSetButton">
<INPUT TYPE="submit" VALUE="全${AfterName}消去" NAME="AllDelButton">
<BR>※全$AfterName一括設定のボタンは、上で選択している$AfterNameに関係なく動作します。<BR>
　 (注！バトルフィールドを除くすべての$AfterNameを一括設定します。)
</TD></TR>
END
	out("</TABLE></FORM></DIV>");
}

#----------------------------------------------------------------------
# 海域マップ
#----------------------------------------------------------------------
# メイン
sub printIslandMapMain {
	my($mode) = @_;
	# 開放
	unlock();

	if($mode <= 1) {
		# idから島番号を取得
		$HcurrentNumber = $HidToNumber{$HcurrentID};

		# なぜかその島がない場合
		if($HcurrentNumber eq '') {
			tempProblem();
			return;
		}
	} else {
		$HcurrentID = 0;
	}

	# マップ表示
	my($connection, $l_id, $c_id);
	$connection = '';
	foreach (0..$islandNumber) {
		$l_id = $Hislands[$_]->{'id'};
		$c_id = $HislandConnect[$Hislands[$_]->{'wmap'}->{'x'}][$Hislands[$_]->{'wmap'}->{'y'}];
		$connection .= "\'$l_id\'\:\'$c_id\'\,\n";
	}
	substr($connection, -2) = '';

	out(<<END) if(!$mode);
<DIV align='center'>
$HtempBack<BR>
${HtagBig_}${HtagName_}Ocean Map${H_tagName}${H_tagBig}<BR>
</DIV>
END
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
connectionID = {
$connection
};
END

	if($HshowWorld && !($HshowWorld % 2)) {
		my @dx = @defaultX;
		my @dy = @defaultY;
		if($Hroundmode && $HadjustMap) {
			my $isl = $Hislands[$HidToNumber{$HcurrentID}];
			my $mx = $isl->{'wmap'}->{'x'};
			my $my = $isl->{'wmap'}->{'y'};
			my @bx = (@dx)x3;
			my @by = (@dy)x3;
			@dx = @bx[(($mx+1+int($HoceanSizeX/2))*$HislandSizeX)..(($mx+1+$HoceanSizeX+int($HoceanSizeX/2))*$HislandSizeX-1)];
			@dy = @by[(($my+1+int($HoceanSizeY/2))*$HislandSizeY)..(($my+1+$HoceanSizeY+int($HoceanSizeY/2))*$HislandSizeY-1)];
		}
		my(@mapx, @mapy);
		foreach (0..$#dx) {
			$mapx[$dx[$_]] = $_;
		}
		foreach (0..$#dy) {
			$mapy[$dy[$_]] = $_;
		}
		out (<<END);
var mapxArray = new Array(${\join(',', @mapx)});
var mapyArray = new Array(${\join(',', @mapy)});
$HnaviExp
function Navi(x, y, img, title, text, exp) { // 3
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";
	if(mapxArray[x] + 1 > $HislandSizeX*$HoceanSizeX / 2) {
		StyElm.style.marginLeft = (mapxArray[x] - 5) * $HwChipSize*2 - 120; // 左側
//		StyElm.style.marginLeft = -10; // 左側
	} else {
		StyElm.style.marginLeft = (mapxArray[x] + 3) * $HwChipSize*2; // 右側
//		StyElm.style.marginLeft = $HislandSizeX*$HoceanSizeX * $HwChipSize*2 - 120; // 右側
	}
	if(mapyArray[y] + 1 == $HislandSizeY*$HoceanSizeY) {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY + 0.5) * $HwChipSize*2 + 10; // 下側
	} else if(mapyArray[y] + 1 > $HislandSizeY*$HoceanSizeY / 2) {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY - 2) * $HwChipSize*2 + 30; // 下側
	} else {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY - 1) * $HwChipSize*2 + 30; // 上側
	}
	StyElm.innerHTML = "<div class='NaviTitle'>" + title + " (" + x + "," + y + ")<\\/div><table><tr><td class='M'><img class='NaviImg' src=" + img + "><\\/td><td class='M'><div class='NaviText'>" + text + "<\\/div>";
	if(exp) {
		StyElm.innerHTML += "<div class='NaviText'>" + eval(exp) + "<\\/div>";
	}
	StyElm.innerHTML += "<\\/td><\\/tr><\\/table>";
}
function ps(x, y) {
    return true;
}
END
	}
	out (<<END) if($HshowWorld && ($HshowWorld < 3));
function displayWorld() {
  if(document.getElementById){
    var obj = document.getElementById('detail');
    if (obj.style.display == 'block'){
      document.getElementById('toggleBtn').firstChild.nodeValue='詳細表示';
      obj.style.display='none';
    } else {
      document.getElementById('toggleBtn').firstChild.nodeValue='詳細非表示';
      obj.style.display='block';
    }
  }
}
END
	if($mode == 1) {
		out (<<END);
function check(id, x, y) {
	if(id == 0) {
		document.IsetupForm.OCEANX.value = x;
		document.IsetupForm.OCEANY.value = y;
		for (var lid in connectionID) {
			unset_highlight(lid);
		}
	} else if(document.OceanForm.REN.checked) {
		for (var lid in connectionID) {
			if(connectionID[lid] == connectionID[id]) {
				set_highlight(lid, 'FFFF00');
			} else {
				unset_highlight(lid);
			}
		}
	}
    return true;
}
END
	} elsif($mode == 2) {
		out (<<END);
function check(id, x, y) {
	document.BfieldForm.ISLANDID.value = id;
	document.BfieldForm.OCEANX.value = x;
	document.BfieldForm.OCEANY.value = y;
	if(document.OceanForm.REN.checked) {
		for (var lid in connectionID) {
			if(connectionID[lid] == connectionID[id]) {
				set_highlight(lid, 'FFFF00');
			} else {
				unset_highlight(lid);
			}
		}
	}
    return true;
}
END
	} elsif($mode == 3) {
		out (<<END);
function check(id, x, y) {
	if(id == 0) {
		document.JoinForm.OCEANX.value = x;
		document.JoinForm.OCEANY.value = y;
		for (var lid in connectionID) {
			unset_highlight(lid);
		}
	} else if(document.OceanForm.REN.checked) {
		for (var lid in connectionID) {
			if(connectionID[lid] == connectionID[id]) {
				set_highlight(lid, 'FFFF00');
			} else {
				unset_highlight(lid);
			}
		}
	}
    return true;
}
END
	} else {
		out (<<END);
function check(id) {
	if(document.OceanForm.REN.checked) {
		for (var lid in connectionID) {
			if(connectionID[lid] == connectionID[id]) {
				set_highlight(lid, 'FFFF00');
			} else {
				unset_highlight(lid);
			}
		}
	} else if(id != 0) {
		window.open("$HthisFile?Sight=" +id);
	}
    return true;
}
END
	}
	out (<<END);
// 画像をマーキング化
function set_highlight(id, color) {
	if(document.getElementById) {
		document.getElementById(id).width  = "${\($HchipSize*2-2)}";
		document.getElementById(id).height = "${\($HchipSize*2-2)}";
		document.getElementById(id).border = "1";
		document.getElementById(id).style.borderColor = "#"+color;
//		document.getElementById(id).width  = "${\($HchipSize*2-2)}";
//		document.getElementById(id).height = "${\($HchipSize*2-2)}";
//		document.getElementById(id).style.filter = "filter: Glow(color=" + color+ ")";
//		document.getElementById(id).style.backgroundColor = "#FFFFFF";
//		document.getElementById(id).style.borderColor = "#FFFFFF";
//		document.getElementById(id).style.Color = "#FFFFFF";
//		document.getElementById(id).style.borderWidth = "1";
	}
}

// マーキング解除
function unset_highlight(id) {
	if(document.getElementById) {
		document.getElementById(id).width  = "${\($HchipSize*2)}";
		document.getElementById(id).height = "${\($HchipSize*2)}";
		document.getElementById(id).border = "0";
	}
}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
function ns(x) {
    return true;
}
function sv(x, y, land, id) {
//	if(connectionID[id] < 0) {
//		land += '【管理人あずかり】';
//	}
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	status = com_str;
	return true;
}
function scls() {
	if($HpopupNavi) {
		NaviClose();
	}
	status = '';
	return false;
}
//-->
</SCRIPT>
END
	out (<<END) if($HshowWorld && ($HshowWorld < 3));
<style type="text/css">
<!--
#detail { display:none; }
-->
</style>
END
	out (<<END);
<DIV ID='islandMap'>
<FORM name="OceanForm">
<INPUT TYPE="checkbox" NAME="REN">海域接続状態
<TABLE BORDER><TR><TD>
</FORM>
END

	# 座標(上)を出力
	out("<nobr>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");

	my($x, $y, $v1, $v0, @x, @y);
	@x = (0..($HoceanSizeX - 1));
	@y = (0..($HoceanSizeY - 1));
	$HadjustMap = 0 if($mode);
	if($Hroundmode && $HadjustMap) {
		my $isl = $Hislands[$HidToNumber{$HcurrentID}];
		my $mx = $isl->{'wmap'}->{'x'};
		my $my = $isl->{'wmap'}->{'y'};
		@bx = (@x)x3;
		@by = (@y)x3;
		@x = @bx[($mx+1+int($HoceanSizeX/2))..($mx+$HoceanSizeX+int($HoceanSizeX/2))];
		@y = @by[($my+1+int($HoceanSizeY/2))..($my+$HoceanSizeY+int($HoceanSizeY/2))];
	}
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		unless ($x % 2) {
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("</nobr><BR>");


	my($id, $point, $image, $alt);
	foreach $y (@y) {
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);

		out("<NOBR>");
		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			# 偶数番号なら番号を出力
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}

		foreach $x (@x) {
			$point = "($x, $y)";

			my($id, $s);
			if ($id = $HoceanMap[$x][$y]) {
				# 島
				$image = ($id == $HcurrentID) ? $HoceanImage[1] : $HoceanImage[2]; # 自分の島 or ふつうの島
				$alt = islandName($Hislands[$HidToNumber{$id}]);
				$alt =~ s/<[^<]*>//g;
				if($Hislands[$HidToNumber{$id}]->{'field'}) {
					$image = $HoceanImage[3] if($id != $HcurrentID);
					$alt .= '【BattleField】';
				} elsif($Hislands[$HidToNumber{$id}]->{'predelete'}) {
					$image = $HoceanImage[4] if($id != $HcurrentID);
					$alt .= '【管理人あずかり】';
				}
				out(qq#<A onClick="check('$id', $x, $y)" #);
				$s = " id='$id'";
			} else {
				# 未知の海域
				$image = $HoceanImage[0];
				$alt = '';

				out(qq#<A onClick="check('0', $x, $y)" #);
				$s = "";
			}

			# JavaScriptを利用した表示
			out(qq#onMouseOver="sv($x,$y,'$alt','$id');" onMouseOut="scls();">#);
			out("<IMG SRC=\"$image\" TITLE=\"$point $alt\" TITLE=\"$point $alt\" width=${\($HchipSize*2)} height=${\($HchipSize*2)} BORDER=0${s}>");
			out("</A>");
		}

		if($y % 2) {
			# 奇数行目なら番号を出力
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
		# 改行を出力
		out("</NOBR><BR>\n");
	}
	# 座標(下)を出力
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		if ($x % 2) {
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
	out("<BR>");
	out("</TD></TR></TABLE></DIV>\n");
	if(!$mode && $HshowWorld) {
		if($HshowWorld) {
			out("<DIV align='center'>${HtagName_}");
			if($HshowWorld < 3) {
				out("<a href='javascript: displayWorld();' id='toggleBtn'>詳細表示</a>");
			} else {
				out("詳細表示");
			}
			out("${H_tagName}");
		}
		if($HshowWorld && !($HshowWorld % 2)) {
			$HchipSize = $HwChipSize;
			out("<TABLE BORDER=0 id='detail'><TR><TD class='M'>");
			islandMap(0, 0, 0, 1);
			out("</TD></TR></TABLE></DIV>\n");
		} else {
			thumbnailIslandMap($Hworld, 0, 1);
		}
	}
}

sub thumbnailIslandMap {
	my($island, $mode, $world) = @_;
	my $isl = $Hislands[$HidToNumber{$HcurrentID}];
	my($id) = 0;
	# 地形、地形値を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);

	if($HjammingView || ($HroundView == 2)) {
		my $n = $HidToNumber{$defaultID};
		$vIsland = (defined $n) ? $Hislands[$n] : '';
		$HvId = (checkPassword($vIsland, $HdefaultPassword)) ? $defaultID : -1;
		my($ii);
		if(!$HvId) {
			foreach $ii (0..$islandNumber) {
				$amityFlag{$Hislands[$ii]->{'id'}} = 1;
			}
		} else {
			$amityFlag{$HvId} = 1;
			if((defined $n) && ($HjammingView == 2)) {
				foreach $ii (0..$islandNumber) {
					foreach (@{$Hislands[$ii]->{'amity'}}) {
						if($_ == $HvId) {
							$amityFlag{$Hislands[$ii]->{'id'}} = 1;
							last;
						}
					}
				}
			}
		}
	}
	my($alpha) = ($HjammingView && ($HjammingLand != 1) && !$mode && !$vIsland->{'itemAbility'}[2]) ? " STYLE=\"filter: Alpha(opacity=50);\"" : '';
	my($wide) = (($Hroundmode || $HoceanMode) && (($HroundView == 1) || (($HroundView == 2) && $vIsland->{'earth'})));
	my(@x, @y);
	@x = @defaultX;
	@y = @defaultY;
	if($Hroundmode && $world && $HadjustMap) {
		my $mx = $isl->{'wmap'}->{'x'};
		my $my = $isl->{'wmap'}->{'y'};
		@bx = (@x)x3;
		@by = (@y)x3;
		@x = @bx[(($mx+1+int($HoceanSizeX/2))*$HislandSizeX)..(($mx+1+$HoceanSizeX+int($HoceanSizeX/2))*$HislandSizeX-1)];
		@y = @by[(($my+1+int($HoceanSizeY/2))*$HislandSizeY)..(($my+1+$HoceanSizeY+int($HoceanSizeY/2))*$HislandSizeY-1)];
	}

	out("<DIV ID='islandMap'>");
	out("<TABLE BORDER id='detail'><TR><TD>");
	# 座標(上)を出力
	out("<nobr>");
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	my($x, $y, $v2, $v1, $v0, $csize2, $csize1, $csize0, $i, $j);
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		unless ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HwChipSize*2/3);
				$csize1 = int(($HwChipSize*2-$csize2)/2);
				$csize0 = $HwChipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HwChipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	out("</nobr><BR>");

	my $range = 0;
	if($HjammingView) {
		foreach $y (@y) {
			foreach $x (@x) {
				if($amityFlag{$HlandID[$x][$y]}) {
					$HviewJam[$x][$y] = 1;
				}
				$range = -1;
				if($land->[$x][$y] == $HlandNavy) {
					my($nId, $nKind) = (navyUnpack($landValue->[$x][$y]))[0, 7];
					$range = $HnavyFireRange[$nKind] if($nId == $HvId);
				} elsif($land->[$x][$y] == $HlandMonster) {
					my($mId, $mKind) = (monsterUnpack($landValue->[$x][$y]))[0, 5];
					$range = $HmonsterFireRange[$mKind] if($mId == $HvId);
				} elsif($land->[$x][$y] == $HhugeMonsterFireRange) {
					my($mId, $mKind) = (monsterUnpack($landValue->[$x][$y]))[0, 5];
					$range = $HnavyFireRange[$mKind] if($mId == $HvId);
				}
				if($range >= 0) {
					foreach (0..($an[$range] - 1)) {
						$sx = $x + $ax[$_];
						$sy = $y + $ay[$_];
						# 行による位置調整
						$sx-- if(!($sy % 2) && ($y % 2));
						$sx = $correctX[$sx + $#an];
						$sy = $correctY[$sy + $#an];
						# 範囲外の場合
						next if(($sx < 0) || ($sy < 0));
						$HviewJam[$sx][$sy] = 1;
					}
				}
			}
		}
	}
	# 各地形および改行を出力
	foreach $j (0..$#y) {
		$y = $y[$j];
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);

		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
		} else {
			# 偶数番号なら番号を出力
			if(defined $v2) {
				$csize2 = int($HwChipSize*2/3);
				$csize1 = int(($HwChipSize*2-$csize2)/2);
				$csize0 = $HwChipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HwChipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			}
		}

		# 各地形を出力
		foreach $i (0..$#x) {
			$x = $x[$i];
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			$jamming = 0;
			if($HjammingView && !$mode && !$vIsland->{'itemAbility'}[2]) {
				$jamming = 1 if(!$HviewJam[$x][$y] && !((!$world && $amityFlag{$id}) || ($world && $amityFlag{$HlandID[$x][$y]})));
			}
			thumbnailLandString($l, $lv, $x, $y, $mode, $jamming);
		}

		if($y % 2) {
			# 奇数行目なら番号を出力
			if(defined $v2) {
				$csize2 = int($HwChipSize*2/3);
				$csize1 = int(($HwChipSize*2-$csize2)/2);
				$csize0 = $HwChipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HwChipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
		}

		out("</BR>\n");
	}
	# 座標(下)を出力
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	foreach $x (@x) {
		$v0 = substr($x, -1);
		$v1 = substr($x, -2, 1);
		$v2 = substr($x, -3, 1);
		if ($x % 2) {
			if(defined $v2) {
				$csize2 = int($HwChipSize*2/3);
				$csize1 = int(($HwChipSize*2-$csize2)/2);
				$csize0 = $HwChipSize*2-$csize2-$csize1;
				out("<IMG SRC=\"space${v2}.gif\" width=$csize2 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v1}.gif\" width=$csize1 height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$csize0 height=${\($HwChipSize*2)}$alpha>");
			} else {
				out("<IMG SRC=\"space${v1}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
				out("<IMG SRC=\"space${v0}.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			}
		} else {
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
		}
	}
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
	out("</TD></TR></TABLE></DIV>\n");
}

sub thumbnailLandString {
	my($l, $lv, $x, $y, $mode, $jamming) = @_;
	my($image);

	if(!$mode && $jamming) {
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
			($l == $HlandMonument)) {
			$l  = $HlandWaste;
			$lv = 2;
		} elsif(($l == $HlandMonster) ||
			($l == $HlandHugeMonster)) {
			my($id, $flag) = (monsterUnpack($lv))[0,4];
			if($id != $HvId) {
				$l  = ($flag & 2) ? $HlandSea : $HlandWaste;
				$lv = 2;
			}
		} elsif($l == $HlandComplex) {
			my($cKind) = (landUnpack($lv))[1];
			$l  = ($HcomplexAttr[$cKind] & 0x300) ? $HlandSea : $HlandWaste;
			$lv = 2;
		} elsif($l == $HlandCore) {
			my($lFlag) = int($lv / 10000);
			$l  = (!$lFlag) ? $HlandWaste : $HlandSea;
			$lv = 2;
		} elsif($l == $HlandNavy) {
			my($nId) = (navyUnpack($lv))[0];
			if($nId != $HvId) {
				$l  = $HlandSea;
				$lv = 2;
			}
		}
	}

	my $alpha = '';
	if($l == $HlandSea) {
		$image = $HlandImage[$l][$lv];
		if($lv == 2) {
			$image = $HjammingSeaImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		$image = $HlandImage[$l][$lv];
		if($lv == 2) {
			$image = $HjammingWasteImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$image = $HlandImage[$l];
	} elsif($l == $HlandForest) {
		# 森
		$image = $HlandImage[$l];
	} elsif($l == $HlandTown) {
		# 都市系
		my($n);
		foreach (reverse(0..$#HlandTownValue)) {
			if($HlandTownValue[$_] <= $lv) {
				$image = $HlandTownImage[$_];
				last;
			}
		}
	} elsif($l == $HlandFarm) {
		# 農場
		$image = $HlandImage[$l];
	} elsif($l == $HlandFactory) {
		# 工場
		$image = $HlandImage[$l];
	} elsif($l == $HlandBase) {
		if(!$mode) {
			# 観光者の場合は森のふり
			$image = $HlandImage[$HlandForest];
		} else {
			# ミサイル基地
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandSbase) {
		# 海底基地
		if(!$mode) {
			# 観光者の場合は海のふり
			$image = $HlandImage[$HlandSea][0];
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandDefence) {
		# 防衛施設
		if(!$mode) {
			if($HdBaseHide) {
				# 観光者の場合は森のふり
				$image = $HlandImage[$HlandForest];
			} else {
				# 観光者の場合は耐久力不明
				$image = $HlandImage[$l][0];
			}
		} else {
			$image = $HlandImage[$l][0];
			if($HdurableDef){
				$lv++;
				if($lv >= $HdefLevelUp) {
					$image = $HlandImage[$l][1];
				}
			}
		}
	} elsif($l == $HlandBouha) {
		# 防波堤
		$image = $HlandImage[$l];
	} elsif($l == $HlandSeaMine) {
		# 機雷
		if(!$mode) {
			# 観光者の場合は海のふり
			$image = $HlandImage[$HlandSea][0];
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		if(!$mode) {
			if($HdBaseHide) {
				# 観光者の場合は森のふり
				$image = $HlandImage[$HlandForest];
			} else {
				# 観光者の場合は防衛施設のふり
				$image = $HlandImage[$HlandDefence][0];
			}
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandOil) {
		# 海底油田
		$image = $HlandImage[$l];
	} elsif($l == $HlandMountain) {
		# 山
		my $mlv = ($lv > 0) ? 1 : 0;
		$image = $HlandImage[$l][$mlv];
	} elsif($l == $HlandCore) {
		# コア
		my($lFlag, $lLv) = (int($lv / 10000), ($lv % 10000));
		if(!$mode) {
			if($HcoreHide) {
				# 観光者の場合
				if(!$lFlag) { # 森のふり
					$image = $HlandImage[$HlandForest];
				} else { # 海のふり
					$image = $HlandImage[$HlandSea][0];
				}
			} else {
				# 観光者の場合は耐久力不明
				$image = $HlandImage[$l][$lFlag];
			}
		} else {
			$image = $HlandImage[$l][$lFlag];
		}
	} elsif($l == $HlandMonument) {
		# 記念碑
		$image = $HmonumentImage[$lv];
	} elsif($l == $HlandComplex) {
		# 複合地形
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		$image = $HcomplexImage[$cKind];
	} elsif($l == $HlandMonster) {
		# 怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		$image = $HmonsterImage[$kind];
		# 硬化中？
		$image = $HmonsterImage2[$kind] if ($flag & 1);
		# 潜水中？
		$image = $HmonsterImageUnderSea if ($flag & 2);
	} elsif($l == $HlandHugeMonster) {
		# 巨大怪獣
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		if(($flag & 1) && ($flag & 2)) {
			# 海で硬化
			$image = $HhugeMonsterImage4[$kind][$hflag];
		} elsif($flag & 1) {
			# 陸で硬化
			$image = $HhugeMonsterImage2[$kind][$hflag];
		} elsif($flag & 2) {
			# 海
			$image = $HhugeMonsterImage3[$kind][$hflag];
		} else {
			# 陸
			$image = $HhugeMonsterImage[$kind][$hflag];
		}
	} elsif($l == $HlandNavy) {
		# 海軍
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$image = $HnavyImage[$kind];
		if ($flag == 1) {
			# 残骸？
			$image = $HnavyImageZ;
		} else {
			if ($flag & 2) {
				# 潜水中？
				$image = $HnavyImage2[$kind];
			}
		}
	}

	out("<IMG SRC=\"$image\" width=${\($HwChipSize*2)} height=${\($HwChipSize*2)} BORDER=0$alpha>");

}

1;
