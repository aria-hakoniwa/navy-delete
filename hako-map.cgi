# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
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
# ����JS���Ѥ˲���
#----------------------------------------------------------------------
# �ʣ��֣�������ץ��� -ver1.11-
# ���Ѿ�������ˡ���ϡ����۸��Ǥ���ǧ��������
# ��°��js-readme.txt�⤪�ɤ߲�������
# ���äݡ���http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ݥåץ��åץʥ�JS��ʬ
#----------------------------------------------------------------------
$HpopupNaviJS =<<"END" if($HpopupNavi);
$HnaviExp

function Navi(x, y, img, title, text, exp) { // 1
	if(!document.mark_form.mark.checked) {
		StyElm = document.getElementById("NaviView");
		StyElm.style.visibility = "visible";
		if(x - mapX + 1 > $HislandSizeX / 2) {
//			StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // ��¦
			StyElm.style.marginLeft = -10; // ��¦
		} else {
//			StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // ��¦
			StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 120; // ��¦
		}
//		if(y - mapY + 1 == $HislandSizeY) {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1.5) * $HchipSize*2; // ��¦
//		} else if(y - mapY + 1 > $HislandSizeY / 2) {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // ��¦
//		} else {
//			StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // ��¦
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
# �ʣ���᥹����ץȳ�ȯ����
#----------------------------------------------------------------------
# �إå�
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

	# ���Υ�����ޤǤλ���ɽ��
	if (!($HmainMode eq 'turn') && (defined $HleftTime)) {
		my $nextturn = '';
		if(!$HgameLimitTurn || ($HislandTurn < $HgameLimitTurn)) {
			my $hour2 = int($HleftTime / 3600);
			my $min2 = int(($HleftTime - $hour2 * 3600) / 60);
			my $sec2 = ($HleftTime - $hour2 * 3600 - $min2 * 60);
			foreach (1..$HrepeatTurn) {
				$nextturn .= '��' if($_ != 1);
				$nextturn .= $HislandTurn + $_;
				last if($HislandTurn + $_ == $HarmisticeTurn || $HislandTurn + $_ == $HsurvivalTurn ||  $HislandTurn + $_ == $HislandChangeTurn);
			}
			$rtStr = "���ι�������<span class='number'>(������$nextturn)</span>�ޤǤ��� $hour2���� $min2ʬ $sec2��";
		} else {
			$rtStr = "��";
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

		document.all.REALTIME.innerHTML = '���󹹿�(<span class="number">������$nextturn</span>)�ޤǻĤ� ' + hour + '���� ' + min + 'ʬ ' + sec + '�� ($HnextTime)';
	} else {
		document.all.REALTIME.innerHTML = '�����󹹿�����ˤʤ�ޤ����� ($HnextTime)';
	}
}

if ($HplayNow) {
	showTimeLeft();
} else {
	document.all.REALTIME.innerHTML = '������Ͻ�λ���ޤ�����';
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

# ����������
sub sortOption {
	$a =~ /^\<.+\>(.+) \(.+ (.+)\/.+\/.+ (.+)\)$/;
	my($aa) = sprintf("%s%03d%02d", $1, $3, $2);
	$b =~ /^\<.+\>(.+) \(.+ (.+)\/.+\/.+ (.+)\)$/;
	my($bb) = sprintf("%s%03d%02d", $1, $3, $2);
#	my($aa) = ($a =~ /^\<.+\>(.+)$/);
#	my($bb) = ($b =~ /^\<.+\>(.+)$/);
	return ($bb cmp $aa);
};

# �����糫ȯ�ײ�
sub tempOwnerJava {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# ���⹽����Ĵ�٤롦�ޥåץǡ��������������ǡ�������
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
				# �γ��Ǥʤ�
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
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);# ��Υ��֤ΤȤ�
                        my($goal);
                        if(($goalx == 31) ||
                           ($goaly == 31)) {
                            $goal = "������";
                        }else{
                            $goal = "��ɸ($goalx, $goaly)";
                        }

                        $wait--;

                        # �Ҷ�����ȯ���Ԥ�ɽ��
                        if($wait <= 0){
                            $ririku = "��ȯ�Ͻ���OK";
                        }else{
                            $ririku = "��ΥΦ�Ԥ�${wait}������"
                        }

                        # ȯ�ʵ�ǽ�ʤ��ä���ä�
                        if(($nKind != 0) && ($nKind != 0x0c)){
                            $ririku = "";
                        }

                        # �Ҷ������ä���ɽ���ѹ�
                        if($HnavyCruiseTurn[$nKind] !=0){
                            $ririku = "��${wait}�������˵���";
                        }

			# �ĳ��Ͻ���
			if($nFlag == 1) {
				$setmap .= "$nKind,";
				next;
			}

			# ¾����δ���Ͻ���
			if ($nId != $id) {
				$invade{"$nId,$nNo"} += 1;
				$setmap .= "$nKind,";
				next;
			}

                        # �����ѵ���
                        my $maxHp = int($HnavyHP[$nKind] * (120 + $nExp) / 120);

			my $nSpecial = $HnavySpecial[$nKind];
			my $navyLevel = expToLevel($HlandNavy, $nExp);
			# ��������å�
			if($nSpecial & 0x8) {
				$setmap .= (100 + $navyLevel) . ',';
				$navyPort++;
                        }elsif($HnavyNoMove[$nKind]){
				$setmap .= "$HlandNavy,";
			} else {
				$setmap .= "$HlandNavy,";
				$name = $HnavyName[$nKind];
				push(@{$fleet[$nNo]}, <<END);
<OPTION value="$x,$y">$name (�ѵ���${nHp}/${maxHp}���и���${nExp}${ririku})
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
			$ifname .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]����($invade{$_}��)<BR>"
		} else {
			$ifname .= "��°����($invade{$_}��)<BR>";
		}
	}
	$ifname .= '��';

	# ���ޥ�ɥ��å�
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# �����Ǥμ��Ф�
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg, $s_target2) = (
			$command->{'kind'},
			$command->{'target'},
			$command->{'x'},
			$command->{'y'},
			$command->{'arg'},
			$command->{'target2'}
		);
		# ���ޥ����Ͽ
		$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_target2\]\,\n";
		$com_max .= "[0,0],";
	}
	substr($set_com, -2) = '';
	substr($com_max, -1) = '';

	#���ޥ�ɥꥹ�ȥ��å�
	my($l_kind);
	$set_listcom = "";
	@click_com = ();
	$All_listCom = 0;
	$com_count = @HcommandDivido;
	#��¤(�и���)��٥��ǧ
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
				$l_cost = '̵��';
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
				if(($m == 0) || ($m == 1) || ($m == 2) || ($m == 3) || ($m == 4) || ($m == 5) || ($m == 7)){ #���ޥ�ɥݥåץ��åפα�¦�ΤȤ��Ф����ɤ���
					next if(($l_kind == $HcomNavySend) || ($l_kind == $HcomNavyReturn)); # ������Ф��Ƥϼ¹Ԥ��ʤ�
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

	# ������ư�ݥåץ��åץ�˥塼���å�
	$click_com[3] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR><TD colspan=2></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,17)' class='M'>11��</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,18)' class='M'>12��</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,7)' class='M'>����</a></TH><TD colspan=2></TD></TR>
<TR><TD></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,16)' class='M'>10��</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,6)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,1)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,8)' class='M'>����</a></TH><TD></TD></TR>
<TR><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,15)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,5)' class='M'> �� </a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,0)' class='M'>�Ե�</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,2)' class='M'> �� </a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,9)' class='M'>����</a></TH></TR>
<TR><TD></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,14)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,4)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,3)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,10)' class='M'>����</a></TH><TD></TD></TR>
<TR><TD colspan=2></TD><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,13)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,12)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='cominput(myForm,7,11)' class='M'>����</a></TH><TD colspan=2></TD></TR>
</TABLE>
END
	$click_com[6] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,0)' class='M'>�̾�</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,1)' class='M'>�༣</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,2)' class='M'>���</a></TH>
<TH><a href='javascript:void(0);' onClick='cominput(myForm,9,3)' class='M'>����</a></TH>
</TR>
</TABLE>
END

	# �����ư�ݥåץ��åץ�˥塼���å�
	$click_com[9] = '';

	#��ꥹ�ȥ��å�
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
		# �ȡ��ʥ���
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		if($island->{'fight_id'} < 1){
			# ̵��
			$HtargetList = "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
			$click_com[9] ="<a href='javascript:void(0);' onClick='cominput(myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}else{
			# ͭ��
			my $fight_id = $island->{'fight_id'};
			$click_com[9] ="<a href='javascript:void(0);' onClick='cominput(myForm,8,$fight_id)' STYlE='text-decoration:none;'>${tName}</a><BR>\n";
			$click_com[9] .="<a href='javascript:void(0);' onClick='cominput(myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}
	}
	# ����̾�����å�
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
	$styleUseComplex = ', #category2' if(!$HuseComplex2);#�ѹ�
	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
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
// �ʣ��֣�������ץȳ�ȯ�������۸�
// ���äݡ���Ȣ������ http://appoh.execweb.cx/hakoniwa/ ��
// Programmed by Jynichi Sakai(���äݡ�)
// �� ������ʤ��ǲ�������
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

		// �Ԥˤ�����Ĵ��
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
<!-- �����ѹ��ե����� -->
<DIV ID="mc_div" style="background-color:white;position:absolute;top:-50;left:-50;height:22px;">&nbsp;</DIV>
<DIV ID="ch_num" style="position:absolute;visibility:hidden;display:none">
<form name="ch_numForm">
<TABLE BORDER=1 BGCOLOR="#e0ffff" CELLSPACING=1>
<TR><TD VALIGN=TOP NOWRAP>
<A HREF="JavaScript:void(0)" onClick="hideElement('ch_num');" STYlE="text-decoration:none"><B>��</B></A><BR>
<select name="AMOUNT" size=13 onchange="chNumDo()">
</select>
</TD>
</TR>
</TABLE>
</form>
</DIV>
<!-- �����ư�ե����� -->
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
<span class='attention'>�������ֹ���ǧ���Ʋ�������</span><br>
�ֿ��̡פǴ����ֹ����ꤷ�Ƥ���<br>
��ư��������$AfterName̾�򥯥�å�
</small>
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
</TD></TR>
</TABLE>
</DIV>
<!-- ��ư��ĥե����� -->
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
<span class='attention'>��������ǽ�Ϥ��ǧ���Ʋ�������</span><br>
�������=>�ְ�ư���(����)��<br>
2Hex��ư=>�ְ�ư��(�ȤƤ�)®����
</small>
</TD></TR>
<TR><TD align='center'>
${HtagTH_}�����ѹ�${H_tagTH}$click_com[6]
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
</TD></TR>
</TABLE>
</DIV>
<!-- ���ޥ�ɥե����� -->
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
<a href="javascript:void(0);" onClick="display(1);" STYlE='text-decoration:none; font-weight:bold;' id='category1'>����(¤��)</a><BR>
<a href="javascript:void(0);" onClick="display(2);" STYlE='text-decoration:none;' id='category2'>����(����)</a>
<a href="javascript:void(0);" onClick="display(3);" STYlE='text-decoration:none;' id='category3'>����(����)</a>
END

	out("<BR>") if($HuseComplex);

	out(<<END);
<a href="javascript:void(0);" onClick="display(4);" STYlE='text-decoration:none;' id='category4'>����</a><BR>
<a href="javascript:void(0);" onClick="display(5);" STYlE='text-decoration:none;' id='category5'>�������</a><BR>
<a href="javascript:void(0);" onClick="display(6);" STYlE='text-decoration:none;' id='category6'>��������</a>
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
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
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
<INPUT TYPE=submit VALUE="�ײ�����" NAME="CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}">
<span id="progresssub"></span>
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
	# �ײ��ֹ�
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><br>
<INPUT TYPE="checkbox" NAME="MENUOPEN" onClick="check_menu()" $HmenuOpen>��ɽ\��
<INPUT TYPE="checkbox" NAME="MENUOPEN2" onClick="check_menu2()" $HmenuOpen2 class='useFlag'><span class='useFlag'>��ư���</span>
<INPUT TYPE="checkbox" NAME="MENUOPEN3" onClick="check_menu3()" $HmenuOpen3 class='useNavy'><span class='useNavy'>�����ư</span>
<br>
<SELECT NAME=menuList onchange="SelectList(myForm)">
<OPTION VALUE=>������
END
	for($i = 0; $i < $com_count; $i++) {
#		next if($i == 4 && !$HuseBase && !$HuseSbase && !$HuseSendMonster && !$HuseSendMonsterST);
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
	out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
</SELECT>
<HR>
<P>
<B>���ޥ������</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">����</A>
��<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">���</A>
��<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">���</A>
</B><HR>
<B>��ɸ(</B>
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
<B>����</B><SELECT NAME=AMOUNT>
END

	# ����
	foreach $i (0..99) {
		out("<OPTION VALUE=$i>$i\n");
	}
	my($myislandID) = $defaultTarget;
	$myislandID = $island->{'id'} if($myislandID eq '');

	my($strUseNavy);
	$strUseNavy = "(�����ư��)" if($HnavyName[0] ne '');
	out(<<END);
</SELECT>
<HR>
<B>��ɸ��${AfterName}</B>${strUseNavy}��
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> ɽ\�� </A></B>
��
<B><A HREF=JavaScript:void(0); onClick="myisland(myForm,'$myislandID')"> ����\�� </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT><BR>
END
	if($HmlogMap) {
		out(<<END);
<BR><B> ������ɽ\�� </B><BR>
END
		my($i, $turn);
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=JavaScript:void(0); onClick=\"jump(myForm, '$HjavaMode', $i)\">");
			if($i == 1) {
				out("������${turn}(����)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
			out("<BR>\n") if($i%3==1);
		}
	}
	my($flagDtr, $amityDtr);
	$flagDtr = 'F=����������' if($HnavyName[0] ne '');
	$amityDtr = 'A=ͧ��������' if($HuseAmity && !$HarmisticeTurn);
	out(<<END);
<span class='useNavy'>
<div align='left'>�����ư��(�ɸ���ǤϤ���ޤ���)</div>
<SELECT NAME=TARGETID2>
$HtargetList<BR>
</SELECT>
</span>
<HR>
<B>���ޥ�ɰ�ư</B><BR>
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> �� </A>����
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> �� </A>
</BIG>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE=submit VALUE="�ײ�����" NAME="CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}">
<span id="progress"></span>
<br><font size=2>�Ǹ��<span class='attention'>�ײ������ܥ���</span>��<br>�����Τ�˺��ʤ��褦�ˡ�</font>
</FORM>
�������ϴʰ�����(NN4�Բ�)<BR>
����=���̡�BS=��������<BR>
DEL=�����INS=��ⷫ��<BR>
$flagDtr$amityDtr<BR>
</TD>
<TD $HbgMapCell>
END

	$ofname = $island->{'fleet'};
	out(<<END) if($HnavyName[0] ne '');
<FORM NAME="FLEET">
<TABLE border=0 align="center">
<TR><TH>$ofname->[0]����</TH><TD><SELECT onfocus="selectFleetXY(0);" onchange="selectFleetXY(0);">@{$fleet[0]}</SELECT></TD><TD>($nFleet[0]��)</TD></TR>
<TR><TH>$ofname->[1]����</TH><TD><SELECT onfocus="selectFleetXY(1);" onchange="selectFleetXY(1);">@{$fleet[1]}</SELECT></TD><TD>($nFleet[1]��)</TD></TR>
<TR><TH>$ofname->[2]����</TH><TD><SELECT onfocus="selectFleetXY(2);" onchange="selectFleetXY(2);">@{$fleet[2]}</SELECT></TD><TD>($nFleet[2]��)</TD></TR>
<TR><TH>$ofname->[3]����</TH><TD><SELECT onfocus="selectFleetXY(3);" onchange="selectFleetXY(3);">@{$fleet[3]}</SELECT></TD><TD>($nFleet[3]��)</TD></TR>
<TR><TH>$HtagTH_¾��δ���$H_tagTH</TH><TD class='N' colspan=2>$ifname</TD></TR>
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
	islandMap(1, 1, 0);	# ����Ͽޡ���ͭ�ԥ⡼��
	my $comment = $Hislands[$HcurrentNumber]->{'comment'};
	out(<<END);
<FORM NAME="LANDINFO">
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA>
</FORM>
END

	#��ư�ϥ��ޥ��
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
				$cost = '̵��';
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
<B>Ȳ�ο���</B><SELECT NAME=AMOUNT>
END

	# ����
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
				$priList[$i] .= "��" if($pFlag);
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
			$priSelectList .= "<BR>��" if($i && $i % 4 == 0);
			$priSelectList .= "��" if($i);
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
	my @status = ('', '�༣', '���', '����');
	my($fkind) = $island->{'fkind'};
	my @flist = @$fkind;
	my @fleetlist = ();
#	my @idx = (0..$#flist);
#	@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
#	@flist = @flist[@idx];
	foreach (@flist) {
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack(hex($_));#���ξ�������������ΤȤ��˽ФƤ����ĺǰ��ä�������
		next if ($HnavySpecial[$nKind] & 0x8); # �����Ͻ���
		next if ($HnavyNoMove[$nKind]); # �����ɱҤȤ��Ͻ���
		my($s, $l) = ();
		my $navyLevel = expToLevel($HlandNavy, $nExp);
#		$s = "\n�ѵ��� $nHp/�и��� $nExp";
		$s = " [${status[$nStat]}]" . $s if($nStat);
		if(($eId != $id) && (defined $HidToNumber{$eId})) {
			my $name = islandName($Hislands[$HidToNumber{$eId}]);
			$name =~ s/<[^<]*>//g;
			$s .= "\n${name}���ɸ���";
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
		push(@fleetMove, " <small><B>��ɸ����</B>${HtagName_}${str}${H_tagName}</small>");
	}

	out(<<END);
</SELECT>��200�ܰʾ�<br>
<INPUT TYPE="hidden" NAME="CommandButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="��ư�Ϸײ�����">
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

	islandInfoWeather() if($HuseWeather); # ���ݾ���
	islandData(); # ��ĥ�ǡ���
	islandInfoSub(1) if($HnavyName[0] ne ''); # ����DATA

	out(<<END);
</TD></TR></TABLE>
</DIV></TD></TR>
</TABLE>
</TD></TR><TR><TD class='M'>
<HR>
<DIV ID='CommentBox'>
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<TABLE BORDER=0>
<TR>
<TH>������<BR><small>(����${HlengthMessage}���ޤ�)</small></TH>
<TD colspan=2><INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"></TD>
</TR>
<TR>
<TH>�ѥ����</TH><TD colspan=2><INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</TD>
</TR>
END
	
	my $sakustr = ($HusePriority ? ' ��()��Ϻ�Ũ��' : '');

	out(<<END) if($HnavyName[0] ne '');
<TR>
</FORM>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH colspan=3>����̾�ѹ�<small>(����${HlengthFleetName}���ޤ�)</small>$sakustr</TH></TR>
<TR><TH>�裱����</TH><TD class='C' colspan=2>$fleetlist[0]<br><INPUT TYPE=text NAME=FLEET1 SIZE=20 VALUE="$ofname->[0]">����$fleetMove[0] $priList[0]</TD></TR>
<TR><TH>�裲����</TH><TD class='C' colspan=2>$fleetlist[1]<br><INPUT TYPE=text NAME=FLEET2 SIZE=20 VALUE="$ofname->[1]">����$fleetMove[1] $priList[1]</TD></TR>
<TR><TH>�裳����</TH><TD class='C' colspan=2>$fleetlist[2]<br><INPUT TYPE=text NAME=FLEET3 SIZE=20 VALUE="$ofname->[2]">����$fleetMove[2] $priList[2]</TD></TR>
<TR><TH>�裴����</TH><TD class='C' colspan=2>$fleetlist[3]<br><INPUT TYPE=text NAME=FLEET4 SIZE=20 VALUE="$ofname->[3]">����$fleetMove[3] $priList[3]</TD></TR>
<TR><TD colspan=3 align=center><INPUT TYPE=submit VALUE="����̾�ѹ�" NAME=FleetnameButton$Hislands[$HcurrentNumber]->{'id'}></TD></TR>
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
<TH>��Ũ���ѹ�</TH><TD><SELECT NAME=PSF onChange=priorityChange() onClick=priorityChange()>
END
		foreach (0..3) {
			out("<OPTION VALUE=$_>$ofname->[$_]\n");
		}
	out(<<END);
</SELECT>���⡡</TD><TD>
$priSelectList
<INPUT TYPE=submit VALUE="�ѹ�" NAME=PriorityButton$Hislands[$HcurrentNumber]->{'id'}>
<small>[<a href="javascript:void(0);" onClick="resetPriority();">�����</a>]</small>
</TD>
END
	}

	my($earth);
	if($HroundView == 2) {
		my $earthstr = ($island->{'earth'} ? '����ɽ��<B><FONT COLOR="#FF0000">����</FONT></B>' : '����ɽ��<B><FONT COLOR="#0000FF">���ʤ�</FONT></B>');
		$earth = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>����ɽ������</TH><TD colspan=2>$earthstr<INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=EarthButton$island->{'id'}></TD></TR>";
	}

	my($comflag);
	if($HcomflagUse >= 2) {
		my $comflagstr = ($island->{'comflag'} ? '�ʤ��Ƥ�' : '�ʤ����');
		my $comflagtmp = ($island->{'comflag'} ? '<FONT COLOR="#FF0000">���ʤ�</FONT>' : '<FONT COLOR="#0000FF">����</FONT>');
		$comflag = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>���ޥ�ɼ¹�����</TH><TD colspan=2>���ޥ�ɤ��¹ԤǤ�${comflagstr}��ͽ�꥿����򷫤�夲�Ƽ¹�<B>$comflagtmp</B><INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=ComflagButton$island->{'id'}></TD></TR>";
	}

	my($preab);
	if($HarmisticeTurn && $HuseCoDevelop) {
		my $preabstr = ($island->{'preab'} ? '�ʤ��Ƥ�' : '�ʤ����');
		my $preabtmp = ($island->{'preab'} ? '<FONT COLOR="#FF0000">���Ĥ���</FONT>' : '<FONT COLOR="#0000FF">���Ĥ��ʤ�</FONT>');
		$preab = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>�رĶ�Ʊ��ȯ</TH><TD colspan=2>�ر��¤����${preabstr}���رĥѥ���ɤǳ�ȯ���̤����뤳�Ȥ�<B>$preabtmp</B><INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=PreabButton$Hislands[$HcurrentNumber]->{'id'}></TD></TR>";
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
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
sub commandJavaMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# �⡼�ɤ�ʬ��
	my($command) = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
		# ���ޥ����Ͽ
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

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	if($Hasync) {
		unlock();
		out("OKsenddatacomplete");
	} else {
		tempCommandAdd();
		# owner mode��
		ownerMain();
	}
}

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
sub printIslandJava {
	# ����
	unlock();

	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	$island = $Hislands[$HcurrentNumber];

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# ̾���μ���
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# ���⹽����Ĵ�٤롦�ޥåץǡ��������������ǡ�������
	my($x, $y, $nKind, $value);
	my $setmap = '';
	my @x = (!$HoceanMode) ? @{$island->{'map'}->{'x'}} : @defaultX;
	my @y = (!$HoceanMode) ? @{$island->{'map'}->{'y'}} : @defaultY;
	foreach $y (@y) {
		$setmap .= '[';
		foreach $x (@x) {
			if($HoceanMode && ($HlandID[$x][$y] != $island->{'id'})) {
				# �γ��Ǥʤ�
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

	#���ޥ�ɥꥹ�ȥ��å�
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
					$l_cost = '̵��';
				} elsif($l_cost =~ /^\@(.*)$/) {
					$l_cost = $1;
				} else {
					$l_cost .= $HunitMoney;
				}
				if($l_kind >= $dd && $l_kind <= $ff) {
					if(($m == 5) || ($m == 8)){
						# ¾����Ф��Ƥϼ¹ԤǤ��ʤ����ޥ��
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
		# ������ư
		$click_com[3] = <<"END";
<TABLE BORDER=0 class="PopupCell">
<TR><TH colspan=2></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,17)' class='M'>11��</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,18)' class='M'>12��</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,7)' class='M'>����</a></TH><TH colspan=2></TH></TR>
<TR><TH></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,16)' class='M'>10��</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,6)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,1)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,8)' class='M'>����</a></TH><TH></TH></TR>
<TR><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,15)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,5)' class='M'> �� </a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,0)' class='M'>�Ե�</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,2)' class='M'> �� </a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,9)' class='M'>����</a></TH></TR>
<TR><TH></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,14)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,4)' class='M'>����</a></TH><TH colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,3)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,10)' class='M'>����</a></TH><TH></TH></TR>
<TR><TH colspan=2></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,13)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,12)' class='M'>����</a></TH><TH class='T' colspan=2><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,7,11)' class='M'>����</a></TH><TH colspan=2></TH></TR>
</TABLE>
END
		$click_com[4] = <<"END";
<TABLE BORDER=0 BGCOLOR="#FFFFFF" class="PopupCell">
<TR>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,0)' class='M'>�̾�</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,1)' class='M'>�༣</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,2)' class='M'>���</a></TH>
<TH><a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,9,3)' class='M'>����</a></TH>
</TR>
</TABLE>
END

	# �����ư�ݥåץ��åץ�˥塼���å�
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
		# �ȡ��ʥ���
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		my $id = $island->{'id'};
		if($island->{'fight_id'} < 1){
			# ̵��
			$click_com[9] ="<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,8,$id)' STYlE='text-decoration:none;'>${HcurrentName}</a>\n";
		}else{
			# ͭ��
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

if((document.layers) || (document.all)){  // IE4��IE5��NN4
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
���⤹�������򥯥�å����Ʋ�������<br>����å�������������ȯ���̤κ�ɸ�����ꤵ��ޤ���
<FORM name="myForm">
<INPUT TYPE="hidden" NAME="MENUOPEN">
<INPUT TYPE="checkbox" NAME="MENUOPEN2" onClick="check_menu2()" class='useFlag'><span class='useFlag'>��ư���</span>
<INPUT TYPE="checkbox" NAME="MENUOPEN3" onClick="check_menu3()" class='UseNavy'><span class='useNavy'>�����ư</span>
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
<span class='attention'>�������ֹ���ǧ���Ʋ�������</span><br>
�ֿ��̡פǴ����ֹ����ꤷ�Ƥ���<br>
��ư��������$AfterName̾�򥯥�å�
</small>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
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
<span class='attention'>��������ǽ�Ϥ��ǧ���Ʋ�������</span><br>
�������=>�ְ�ư���(����)��<br>
2Hex��ư=>�ְ�ư��(�ȤƤ�)®����
</small>
</TD></TR>
<TR><TD align='center'>
${HtagTH_}�����ѹ�${H_tagTH}$click_com[4]
</TD></TR>
<TR><TD>
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
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
<a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">��˥塼���Ĥ���</A>
</TD></TR>
</TABLE>
</DIV>
END
	if(checkPassword($island, $HdefaultPassword) && $island->{'id'} eq $defaultID) {
		islandMap(1, 1, $HmissileMode);  # ����Ͽޡ��Ѹ��⡼��
#		templandStringFlash(1); # �����ͣ��Хǡ���ɽ��
	}else{
		if($island->{'field'}) {
			islandMap(1, 1, $HmissileMode); # ����Ͽޡ��Ѹ��⡼��
		} else {
			islandMap(0, 1, $HmissileMode); # ����Ͽޡ��Ѹ��⡼��
		}
#		templandStringFlash(0); # �����ͣ��Хǡ���ɽ��
	}
	if($HmlogMap && $HmissileMode) {
		out(<<END);
<DIV align='center'>
<TABLE class="DamageCell" BORDER><TR>
<TH>${HtagDisaster_}������${H_tagDisaster}</TH><TH>̵��</TH><TH>�ɱ�</TH><TH>�Ų�or����</TH><TH>̿��</TH>
</TR><TR>
<TH>${HcurrentName}�ι���</TH><TH><span class='nodamage'>��</span></TH><TH><span class='defence'>��</span></TH><TH><span class='harden'>��</span></TH><TH><span class='hitpoint'>��</span></TH>
</TR><TR>
<TH>¾${AfterName}�ι���</TH><TH><span class='nodamage'>��</span></TH><TH><span class='defence'>��</span></TH><TH><span class='harden'>��</span></TH><TH><span class='hitpoint'>��</span></TH>
</TR></TABLE>
<HR>
END
		my $i;
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=\"$HthisFile?IslandMap=$island->{'id'}&JAVAMODE=$HjavaMode&MISSILEMODE=$i\">");
			if($i == 1) {
				out("������${turn}(����)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
		}
		out("</DIV>\n");

		# ���ƥޥåפ�Ʊ��������Υ���ɽ�������פʤ饳���ȥ����ȡ�
		#logFilePrint($HmissileMode-1, $island->{'id'}, $mode);
	}

	# �����������Ǽ���
#	if($HuseLbbs) {
		#require('./hako-lbbs.cgi');
		#tempLbbsContents(); # �Ǽ�������
		#�Ť��ʤ�Τ�ɽ�������ʤ���ɽ��������ϡ�#tempLbbs������#���롣
#	}
	# �����Ǽ���
#	if($HuseExlbbs) {
#		if($island->{'password'} eq encode($HdefaultPassword) && ($island->{'id'} eq $defaultID)) {
#			exLbbs($island->{'id'}, 1);
#		}else{
#			exLbbs($island->{'id'}, 0);
#		}
#	}

	# �ᶷ
	out("</DIV>");
	tempRecent(0, $HuseHistory2);
}

sub templandStringFlash {
	my($mode) = @_;
	require './hako-js.cgi';
	landStringFlash($mode); # �����ͣ��Хǡ���ɽ��
}
#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMain {
	# ����
	unlock();
	if($HadminMode && !checkSpecialPassword($HdefaultPassword)) {
			tempWrongPassword();
			return;
	}
	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# ̾���μ���
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# �Ѹ�����
	if($HadminMode) {
		tempPrintIslandHead($island, 1); # �褦����!!
	} else {
		tempPrintIslandHead($island, 0); # �褦����!!
	}
	islandInfo(0); # ��ξ���
	if(!$HadminMode && $Hislands[$HcurrentNumber]->{'field'}) {
		islandMap(2, 0, 0); # ����Ͽޡ��Ѹ��⡼��
	} else {
		islandMap($HadminMode, 0, 0); # ����Ͽޡ��Ѹ��⡼��
	}
	islandJamp();   # ��ΰ�ư

	islandInfoWeather() if($HuseWeather); # ���ݾ���
	islandData(); # ��ĥ�ǡ���
	islandInfoSub((!$Hislands[$HcurrentNumber]->{'field'}) ? 1 : 0) if($HnavyName[0] ne ''); # �����ǡ���

	# �����������Ǽ���
	if($HuseLbbs) {
		require('./hako-lbbs.cgi');
		tempLbbsMain(0);
	}
	if($HuseExlbbs) { # �����Ǽ���
		exLbbs($HcurrentID, 0) ;
	}

	# �ᶷ
	tempRecent(0, $HuseHistory2);
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub ownerMain {
	# ����
	unlock();

	# �⡼�ɤ�����
	$HmainMode = 'owner';

	if($HcurrentID eq '') {
		tempProblem();
		return;
	}

	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# �ѥ����(�¤����ס�ǰ�Τ���Ĥ��Ƥ���)
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		return;
	}

	if($Htournament){
		# �ȡ��ʥ���
		$tName = islandName($Hislands[$HidToNumber{$island->{'fight_id'}}]);
		if($island->{'fight_id'} < 1){
			# ̵��
			$HtargetList = "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
		}else{
			# ͭ��
			$HtargetList = "<OPTION VALUE=\"$island->{'fight_id'}\">${tName}\n";
			$HtargetList .= "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}\n";
			#$defaultTarget = $island->{'fight_id'} if($defaultTarget != $HcurrentID && $defaultTarget != $island->{'fight_id'});
		}
	}

	# ��ȯ����
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # ��Java������ץȳ�ȯ�ײ��
	}else{
		tempOwner();     # ���̾�⡼�ɳ�ȯ�ײ��
	}

	# �����������Ǽ���
	if($HuseLbbs) {
		require('./hako-lbbs.cgi');
		tempLbbsMain(1); # ������Ǽ���
	}
	if($HuseExlbbs) { # �����Ǽ���
		exLbbs($HcurrentID, 1) ;
	}

	# �ᶷ
	tempRecent(1, $HuseHistory1);
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commandMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# �ѥ����
	if(($HcommandKind == $HcomGiveup) && ($HcommandMode ne 'delete')) {
		if(!checkSpecialPassword($HinputPassword) && (encode($HinputPassword) ne $island->{'password'})) {
			# owner mode��
			ownerMain();
			return;
		}
	} elsif(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	commandAdd($island);

	# owner mode��
	ownerMain();
}

# ���ޥ����Ͽ
sub commandAdd {
	my $island = shift;
	# �⡼�ɤ�ʬ��
	my($command) = $island->{'command'};

	my($i, $j) = (0, 0);
	my($x, $y);
	# ��ɸ�������
	makeRandomIslandPointArray($island);
	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# �ե����ϡ��ե��Ϥʤ餷
		my($land) = $island->{'land'};

		# ���ޥ�ɤμ������
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
		# �������Ω�ơ���������
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		# ���ޥ�ɤμ������
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
		# Ȳ�Ρ�Ȳ�Τȿ���
		# �ʿ��̡ߣ������ܤ��¿�����������оݡ�
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		# ���ޥ�ɤμ������
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
		# ���ä�
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
		# ���ޥ�ɤ���Ͽ
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

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);
}

#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commentMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = islandName($island);

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��å������򹹿�
	$island->{'comment'} = htmlEscape($Hmessage);

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# �����ȹ�����å�����
	tempComment();

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# ����̾�ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub fleetnameMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ����̾�򹹿�
	my @fleetname;
	$fleetname[0] = htmlEscape($HfleetName[0]);
	$fleetname[1] = htmlEscape($HfleetName[1]);
	$fleetname[2] = htmlEscape($HfleetName[2]);
	$fleetname[3] = htmlEscape($HfleetName[3]);
	$island->{'fleet'} = \@fleetname;

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# �����ȹ�����å�����
	tempFleetName();

	# owner mode��
	ownerMain();
}

sub priorityMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��Ũ��򹹿�
	my $mypri = $island->{'priority'};
	foreach (0..3) {
		if($_ == $HfleetNumber) {
			$mypri->[$_] = $HfleetPriority;
		}
	}
	$island->{'priority'} = $mypri;

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# ������å�����
	tempPriority();

	# owner mode��
	ownerMain();
}

sub earthMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ����ɽ������ե饰���ѹ�
	$island->{'earth'} ^= 1;

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();
}

sub comflagMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ���ޥ�ɼ¹�����ե饰���ѹ�
	$island->{'comflag'} ^= 1;

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();
}

sub preabMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �ѥ����
	if(!checkPassword($island,$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# �رĶ�Ʊ��ȯ�ե饰���ѹ�
	$island->{'preab'} ^= 1;

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
	my($mode) = @_;

	my($island) = $Hislands[$HcurrentNumber];
	# ����ɽ��
	my($rank) = $HcurrentNumber + 1 - $HbfieldNumber;
	my($pop) = ($island->{'pop'} == 0) ? "̵��" : "$island->{'pop'}$HunitPop";
	1 while $pop =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($food) = ($island->{'food'} == 0) ? "���ߥ���" : "$island->{'food'}$HunitFood";
	1 while $food =~ s/(.*\d)(\d\d\d)/$1,$2/;
                # �ɲ�
                $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood) * 10);
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
                $foodrate .= '����/10000�ȥ�';
	my($farm) = ($island->{'farm'} == 0) ? "��ͭ����" : "$island->{'farm'}0$HunitPop";
	1 while $farm =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($factory) = ($island->{'factory'} == 0) ? "��ͭ����" : "$island->{'factory'}0$HunitPop";
	1 while $factory =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($mountain) = ($island->{'mountain'} == 0) ? "��ͭ����" : "$island->{'mountain'}0$HunitPop";
	1 while $mountain =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($area) = $island->{'area'};
	if($area > $HdisFallBorder) {
		$area = "${HtagDisaster_}$area$HunitArea${H_tagDisaster}";
	} elsif($area == $HdisFallBorder) {
		$area = "<span class='attention'>$area$HunitArea</span>";
	} elsif(!$area) {
		$area = "�ʤ�";
	} else {
		$area .= $HunitArea;
	}
	1 while $area =~ s/(.*\d)(\d\d\d)/$1,$2/;
	my($sea) = calcSea($island);
	if($HnoDisFlag) {
		if($sea) {
			$sea .= $HunitArea;
		} else {
			$sea = "�ʤ�";
		}
	} elsif(!$sea) {
		$sea = "<span class='attention'>�ʤ�</span>";
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
		# ̵���ޤ���owner�⡼�ɤޤ���BattleField
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>";
		my($money) = ($island->{'money'} == 0) ? "��⥼��" : "$island->{'money'}$HunitMoney";
		1 while $money =~ s/(.*\d)(\d\d\d)/$1,$2/;
		$mStr2 = "<TD $HbgInfoCell align=right>$money</TD><TD $HbgInfoCell align=right>$food</TD>";
		$col++;
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		1 while $mTmp =~ s/(.*\d)(\d\d\d)/$1,$2/;

		# 1000��ñ�̥⡼��
		$mStr1 = "<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>";
		$mStr2 = "<TD $HbgInfoCell align=right>$mTmp</TD>";
		$col++;
	}
	my($bStr) = '';
	my($rStr1) = '';
	my($rStr2) = '';
	if(!$island->{'field'}) {
		# ���
		$rStr1 = "<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>";
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
<TH $HbgTitleCell>${HtagTH_}�͸�${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}�����졼��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�η��쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������и���${H_tagTH}</TH>
</TR>
<TR>
$rStr2
<TD $HbgInfoCell align=right>$pop</TD>
$mStr2
<TD $HbgInfoCell align=right>$foodrate</TD>
<TD $HbgInfoCell align=right> $area <B>Φ��</B><BR> $sea <B>����</B></TD>
<TD $HbgInfoCell align=right>${farm}</TD>
<TD $HbgInfoCell align=right>${factory}</TD>
<TD $HbgInfoCell align=right>${mountain}</TD>
<TD $HbgInfoCell align=right>${totalExp}</TD></TR>
END

	if($HuseAmity && !$HarmisticeTurn&& !$Htournament) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}ͧ����${H_tagTH}</TH>
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
		out("��") unless(defined $ami);
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
			$allyName =~ s/�ھ��ԡ���//g;
			$aNo += $i;
			my $campInfo = '';
			$campInfo .=<<_CAMP_ if($mode && $HarmisticeTurn);
��[<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm${aNo}.action='${HthisFile}';document.allyForm${aNo}.submit();return false;">��������</A>]&nbsp;&nbsp;
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
# Ʊ���Ǽ��ĤؤΥ�󥯤�Ʊ��̾�Ǥʤ��ֺ����ļ��פˤ�������硢����'$HarmisticeTurn'��'1'�˽񤭴�����Ф褤��
				if($HarmisticeTurn) {
					$AllyBBS .=<<_BBS_;
<TD class='M'>
<FONT COLOR="$ally->{'color'}"><B>$ally->{'mark'}</B></FONT>$ally->{'name'}
��[<A STYlE="text-decoration:none" HREF="JavaScript:void(0)" onClick="document.allyForm${aNo}.action='${HbaseDir}/${HallyBbsScript}';document.allyForm${aNo}.submit();return false;">�����ļ�</A>]
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

	my $allytitle = $HarmisticeTurn ? '�ر�' : 'Ʊ��';
	out(<<END) if($HallyNumber);
<TR>
<TH $HbgTitleCell>${HtagTH_}${allytitle}${H_tagTH}</TH>
<TD colspan="$col" class='C'>${AllyBBS}</TD></TR>
END

	if($HuseDeWar && !$HarmisticeTurn && !$HsurvivalTurn && !$Htournament) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}�����${H_tagTH}</TH>
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
			$turn .= '��' if($turn < $HislandTurn);
			$turn = '������' . $turn;
			my($f, $fturn) = ($flag % 10, int($flag / 10) + $HdeclareTurn);
			my($flag1, $flag2) = ('', '');
			if($f == 1) {
				($flag1, $flag2) = ("[�����ǿ���:$fturn]", "[�����ǿǤ���:$fturn");
				$flag2 .= (!$mode) ? ']' : " <a href='javascript:void(0);' onClick='cominput(myForm,10,$id1)'>���</a> <a href='javascript:void(0);' onClick='cominput(myForm,11,$id1)'>�˴�</a>]";
			} elsif($f == 2) {
				($flag1, $flag2) = ("[�����ǿǤ���:$fturn", "[�����ǿ���:$fturn]");
				$flag1 .= (!$mode) ? ']' : " <a href='javascript:void(0);' onClick='cominput(myForm,10,$id2)'>���</a> <a href='javascript:void(0);' onClick='cominput(myForm,11,$id2)'>�˴�</a>]";
			}
			if($island->{'id'} == $id1){
				$warName .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${id2}\" target=\"_blank\">${name2}</A>($turn$flag1) ";
			}elsif($island->{'id'} == $id2){
				$warName .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${id1}\" target=\"_blank\">${name1}</A>($turn$flag2) ";
			}
		}
		$warName = "��" unless(defined $warName);
		out("$warName</TD></TR>");
	}

	$col++;
	if($island->{'predelete'}) {
		my $rest = ($island->{'predelete'} != 99999999) ? "<small>(����$island->{'predelete'}������)</small>" : '';
		out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"\>${HtagDisaster_}�����ͤ�������${H_tagDisaster}�ˤ�꥿���󹹿������$rest</TH></TR>");
	} elsif($Htournament) {
		if($island->{'fight_id'} > 0) {
			my $cn = $HidToNumber{$island->{'fight_id'}};
			if($cn ne '') {
				my $tIsland = $Hislands[$cn];
				my $name = islandName($tIsland);
				$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$tIsland->{'id'}\" target=\"_blank\">$name</A>";
				out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"><B>��������$name�Ǥ�</B></TH></TR>");
			}
		} elsif($island->{'rest'} && ($HislandNumber > 1)) {
			out("<TR><TH $HbgCommentCell COLSPAN=\"$col\"\>���ﾡ�ˤ�곫ȯ����桡�Ĥ�${HtagDisaster_}$island->{'rest'}${H_tagDisaster}������</TH></TR>");
		}
	} elsif($island->{'event'}[0]) {
		my $flag = 0;
		my $type  = $HeventName[$island->{'event'}[6]];
		if(($island->{'event'}[1] - $HnoticeTurn <= $HislandTurn) && ($HislandTurn < $island->{'event'}[1])) {
			out("</TABLE><TABLE BORDER><TR></TR><TR><TH class=CommentCellT COLSPAN=\"8\"\><big>${HtagTH_}$type${H_tagTH}���š�</big>��$island->{'event'}[1]�����󤫤��</TH></TR>");
			$flag = 1;
		} elsif($island->{'event'}[1] <= $HislandTurn) {
			out("</TABLE><TABLE BORDER><TR></TR><TR><TH class=CommentCellT COLSPAN=\"8\"\><big>${HtagTH_}$type${H_tagTH}�����桪</big></TH></TR>");
			$flag = 1;
		}
		my $turm = $island->{'event'}[2];
		if(!$turm) {
			$turm = '<big><B>̵����</B></big>';
		} else {
			$turm += $island->{'event'}[1];
			$turm = "<B>������<big>${HtagNumber_}${turm}${H_tagNumber}</big></B>";
		}
		$turm .= "<BR>${HtagDisaster_}$HlandName[$HlandCore][0]���ǻ�������λ${H_tagDisaster}"if($island->{'event'}[23]);
		my $max  = $island->{'event'}[3];
		$max = ($max) ? "$max��" : '̵����';
		my $addition  = $island->{'event'}[11];
		$addition = ($addition) ? "���Ĥ���" : '���Ĥ��ʤ�';
		my $autoreturn  = $island->{'event'}[18];
		$autoreturn = ($autoreturn) ? "����" : '���ʤ�';
		my $kind  = $island->{'event'}[4];
		my $ship = '';
		foreach (1..$#HnavyName) {
			$ship .= " $HnavyName[$_]" if($kind & (2 ** $_));
		}
		my $sstr = '';
		if($ship eq '') {
			$ship = "${HtagDisaster_}�ʤ�${H_tagDisaster}";
		} elsif($kind & 1) {
			$ship = "${HtagDisaster_}$ship${H_tagDisaster}";
			$sstr = '<BR><small>(��¤�ϤΤ�)</small>';
		}
		my $restriction = $island->{'event'}[5];
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
			$limit = '';
			foreach (1..$HmaxComNavyLevel) {
				if($restriction & (2 ** $_)) {
					$limit .= "<nobr>${HtagDisaster_}��${H_tagDisaster}Lv.$_</nobr> ��";
				} else {
					$limit .= "<nobr><B>��</B>Lv.$_</nobr> ��";
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
			$prize .= "�����ͥץ쥼���";
		}
		1 while $prize =~ s/(.*\d)(\d\d\d)/$1,$2/;
		if($island->{'event'}[10]) {
			$prize .= " + " if($money || $food || $present);
			foreach (1..$#HitemName) {
				$prize .= "<span class='check'><img src=\"$HitemImage[$_]\" title=\"$HitemName[$_]\"></span>\n" if($item[$_]);
			}
		}
		$prize = '�ʤ�' if($prize eq '');
		my $mons = ($island->{'event'}[13]) ? "${HtagNumber_}$island->{'event'}[12]${H_tagNumber}<small>������ˤĤ�</small><BR>��<B>$island->{'event'}[13]</B><small>ɤ�и�</small>" : '�и����ʤ�';
		my $huemons = ($island->{'event'}[15]) ? "${HtagNumber_}$island->{'event'}[14]${H_tagNumber}<small>������ˤĤ�</small><BR>��<B>$island->{'event'}[15]</B><small>ɤ�и�</small>" : '�и����ʤ�';
		my $unknown = ($island->{'event'}[17]) ? "${HtagNumber_}$island->{'event'}[16]${H_tagNumber}<small>������ˤĤ�</small><BR>��<B>$island->{'event'}[17]</B><small>�Ͻи�</small>" : '�и����ʤ�';
		my $core = ($island->{'event'}[20]) ? "${HtagNumber_}$island->{'event'}[19]${H_tagNumber}<small>������ˤĤ�</small><BR>��<B>$island->{'event'}[20]</B><small>��и�</small>" : '�и����ʤ�';
		if($flag) {
			out(<<END);
<TR><TH $HbgTitleCell>��λ������</TH><TD align='right' class='N'>$turm</TD>
<TH $HbgTitleCell>��λ�����Խ���</TH><TD align='right' class='N'>$autoreturn</TD>
<TH $HbgTitleCell>�ɸ���ǽ������</TH><TD align='right' class='N'>$max</TD>
<TH $HbgTitleCell>�ɲ��ɸ�</TH><TD align='right' class='N'>$addition</TD></TR>
<TR><TH $HbgTitleCell>�ɸ���ǽ�ϼ�$sstr</TH><TD colspan='7' align='left'>$ship</TD></TR>
END
			out("<TR><TH $HbgTitleCell>�ɸ���ǽ��٥�<BR><small>(��Υ�٥�)</small></TH><TD colspan='7' align='left'>$limit</TD></TR>") if($HmaxComNavyLevel);
			out(<<END);
<TR><TH $HbgTitleCell>����</TH><TD align='right'>$mons</TD>
<TH $HbgTitleCell>�������</TH><TD align='right'>$huemons</TD>
<TH $HbgTitleCell>��°������</TH><TD align='right'>$unknown</TD>
<TH $HbgTitleCell>$HlandName[$HlandCore][0]</TH><TD align='right'>$core</TD></TR>
<TR><TH $HbgTitleCell>���</TH><TD colspan='7' align='left' class='N'>$prize</TD></TR>
END
		}
	}
	out("</TABLE></DIV>");
}

# �����ɽ��(����)
sub islandInfoSub {
	my($mode) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	# ����ɽ��
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
			$navykind[$_] = 0; # ��ͭ���ν����
			next if($HnavySpecial[$_] & 0x8); # �����Ϲ�פ�����ʤ�
			$totalSink += $kindSink[$_];
			$selfSink += $island->{'sinkself'}[$_];
			$subTotalSink += $subKindSink[$_];
			$subSelfSink += $island->{'subSinkself'}[$_];
		}
		$subTotalSink = $totalSink - $subTotalSink;
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp) = navyUnpack(hex($_));#��������ͭ������������ʤ������
			$navykind[$nKind]++; # ��ͭ��
			next if($HnavySpecial[$nKind] & 0x8); # �����Ϲ�פ�����ʤ�
			$totalNavy++;
		}
	}
	# ���⹽����Ĵ�٤�
	my($id, $land, $landValue, $landValue2, $map) = ($island->{'id'}, $island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}, $island->{'map'});
	my($x, $y, $kind, $value, $value2, $name, @own, %invade, %invadeTotal);
	my $owntotal = 0;
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$value2 = $landValue2->[$x][$y];
			next if ($kind != $HlandNavy);
			# ��α������Ĵ�٤�
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
			my $nSpecial = $HnavySpecial[$nKind];
			# �����ĳ��Ͻ���
			next if(($nSpecial & 0x8) || ($nFlag == 1));
			if($nId == $id && !$island->{'event'}[0]) {
				$own[$nKind]++;
				$owntotal++;
			} else {
				$invade{$nId}[91] = $nHp if($invade{$nId}[91] < $nHp);   # �ѵ���
				$invade{$nId}[92] = $nExp if($invade{$nId}[92] < $nExp); # �����и���
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
<TR><TH$row>${HtagTH_}����DATA${H_tagTH}$pstr</TH>
<TH $HbgTitleCell$row>${HtagTH_}���${H_tagTH}</TH>
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
#				$level = '��';
#			}
#			if($level == 1) {
#				$exp = 0;
#			} elsif($level ne '��') {
#				$exp = $HcomNavyBorder[$level-2];
#			} else {
#				$exp = '����';
#			}
#			$head .= "<TD class='T'>Lv.${level}</TD>";
#		}
#		$head .="</TR>";
#	}

	out("<DIV ID='islandInfo'><TABLE BORDER>$head") if(keys %invade != () || $mode);
	if($mode) {
		out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}��ͭ��${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${totalNavy}��${H_tagNumber}</TD>
END
		foreach (0..$#HnavyName) {
			my $kindNavy = $navykind[$_]; # ��ͭ��
			$kindNavy .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
			out("<TD $HbgInfoCell align=right>$kindNavy</TD>");
		}

		out(<<END);
</TR><TR>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${totalSink}��${H_tagNumber}</TD>
END
		foreach (0..$#HnavyName) {
			my $kindsink = $kindSink[$_];
			$kindsink .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
			out("<TD $HbgInfoCell align=right>$kindsink</TD>");
		}
		out("</TR>");

		if(!$HnavySafetyZone || $HnavySafetyInvalidp) {
			out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${selfSink}��${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $sinkself = $island->{'sinkself'}[$_];
				$sinkself .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
				out("<TD $HbgInfoCell align=right>$sinkself</TD>");
			}
			out("</TR>");
		}
	}


	# ��α����
	my $flag = 0;
	my @infleet = sort { $a <=> $b } keys %invade;
	if($island->{'event'}[0]) {
		if($island->{'event'}[6] == 1) { # ���Х��Х�
			# ������=>�ѵ��Ϥǥ�����
			@infleet = sort { $invadeTotal{$b} <=> $invadeTotal{$a} ||
								 $invade{$b}[91] <=> $invade{$a}[91] } keys %invade;
		} else { # epoint
			# epoint=>������=>�ѵ���=>�и��ͤǥ�����
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
				if($island->{'event'}[6] == 1) { # ���Х��Х�
					# ������
					#$epoint = ' (' . int($invadeTotal{$_}) . ')';
				} else { # epoint
					# epoint
					$epoint = ' (' . int($invade{$_}[90]) . ')';
				}
			}
			out(<<END);
<TR>
<TD align=right>${HtagTH_}<A STYlE="text-decoration:none" href="${HthisFile}?Sight=$_" target="_blank">${iName}</A>${H_tagTH}$epoint</TH>
<TD align=right>${HtagNumber_}$invadeTotal{$_}��${H_tagNumber}</TD>
END
			foreach $in (0..$#HnavyName) {
				my $invadeship = ($HnavySpecial[$in] & 0x8) ? '��' : sprintf("%d��", $invade{$_}[$in]);
				out("<TD align=right>$invadeship</TD>");
			}
			out("</TR>");
			$flag = 1 if(!$island->{'event'}[0]);
		}
		if($mode && $flag) {
			out(<<END);
<TR>
<TH>${HtagTH_}��α����${H_tagTH}</TH>
<TD align=right>${HtagNumber_}${owntotal}��${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $ownship = ($HnavySpecial[$_] & 0x8) ? '��' : sprintf("%d��", $own[$_]);
				out("<TD align=right>$ownship</TD>");
			}
			out("</TR>");
		}
	}
	if($mode) {
		# ���֥ǡ���
		my(@sData) = @{$Hislands[$HcurrentNumber]->{'subExt'}};
		my $sTurn = $sData[0];
		$sTurn++;
		my $birthday = $Hislands[$HcurrentNumber]->{'birthday'};
		$birthday++;
		if($sTurn > $birthday) {
			my $row = (!$HnavySafetyZone || $HnavySafetyInvalidp) ? 2 : 1;
			out(<<END);
</TR>
<TR><TH $HbgTitleCell colspan='$col'>${HtagTH_}${HnormalColor_}������${H_normalColor}${sTurn}${HnormalColor_}��${H_normalColor}����${H_tagTH}</TH></TR>
$head
<TR><TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${subTotalSink}��${H_tagNumber}</TD>
END
			foreach (0..$#HnavyName) {
				my $subKindSink = $kindSink[$_] - $subKindSink[$_];
				$subKindSink .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
				out("<TD $HbgInfoCell align=right>$subKindSink</TD>");
			}
			out("</TR>");

			if(!$HnavySafetyZone || $HnavySafetyInvalidp) {
				out(<<END);
<TR>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TD $HbgNumberCell align=right>${HtagNumber_}${subSelfSink}��${H_tagNumber}</TD>
END
				foreach (0..$#HnavyName) {
					my $subSinkself = $island->{'sinkself'}[$_] - $island->{'subSinkself'}[$_];
					$subSinkself .= ($HnavySpecial[$_] & 0x8) ? '��' : '��';
					out("<TD $HbgInfoCell align=right>$subSinkself</TD>");
				}
				out("</TR>");
			}
		}
	}
	out("</TABLE></DIV>");
}

# �����ɽ��(����)
sub islandInfoWeather {
	my($mode) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	my($kion, $kiatu, $situdo, $kaze, $jiban, $nami, $ijoh, @weather) = @{$island->{'weather'}};
	my @turn = ($HislandTurn, $HislandTurn + 1, $HislandTurn + 2, $HislandTurn + 3);
	out(<<END);
<DIV ID='weatherInfo'><TABLE BORDER>
<TR><TH colspan></TH></TR>
<TR>
<TH $headNameCellcolor colspan=6>���ݥǡ���</TH>
<TH $headNameCellcolor><span $todayColor>����</TH>
<TH $headNameCellcolor colspan=6><span $tomorrowColor>ͽ��</TH>
</TR>
<TR><TD $pointCellcolor>${HtagTH_}����${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}����${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}����${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}��®${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}����${H_tagTH}</TD><TD $pointCellcolor>${HtagTH_}����${H_tagTH}</TD>
<TD $pointCellcolor rowspan=2><img src ='${HimageDir}/$HweatherImage[$weather[3]]'><br><span $todayColor>$HweatherName[$weather[3]]</span></TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>����(${turn[1]})</TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>${turn[2]}</TD>
<TD $headNameCellcolor colspan=2><span $tomorrowColor>${turn[3]}</TD>
</TR>
<TR><TD $pointCellcolor2>${kion}��</TD><TD $pointCellcolor2>${kiatu}hPa</TD><TD $pointCellcolor2>${situdo}%</TD><TD $pointCellcolor2>${kaze}m/s</TD><TD $pointCellcolor2>${jiban}</TD><TD $pointCellcolor2>${nami}</TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[2]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[2]]</span></TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[1]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[1]]</span></TD>
<TD $pointCellcolor><img src ='${HimageDir}/$HweatherImage[$weather[0]]' width='16' height='16'></TD><TD $pointCellcolor><span $tomorrowColor>$HweatherName[$weather[0]]</span></TD>
</TR>
</TABLE></DIV>
END
}

# �Ƽ��ĥ�ǡ���ɽ��(���ζ�˴)
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
	my(@after) = ('', '', '��', '��', "$HunitPop", 'ȯ', 'ȯ', 'ȯ', '��', '��', '��');
	# ������
	$data[1] = int($data[1] / 10);
	$sData[1] = int($sData[1] / 10);
	foreach (2..$loop){
		$data[$_] = $data[$_] ? "${data[$_]}${after[$_]}" : '�ʤ�';
		$sData[$_] = $sData[$_] ? "${sData[$_]}${after[$_]}" : '�ʤ�';
	}
	$sMkill = $Hislands[$HcurrentNumber]->{'monsterkill'} - $sMkill;
	my $monsterkill = $Hislands[$HcurrentNumber]->{'monsterkill'} ? "$Hislands[$HcurrentNumber]->{'monsterkill'}$HunitMonster" : '�ʤ�';
	my $sMonsterkill = $sMkill ? "$sMkill$HunitMonster" : '�ʤ�';
	my(@aStr, @mStr, @nStr);
	my $col = 6;
	if($HallyNumber && ($Hislands[$HcurrentNumber]->{'allyId'}[0] ne '')) {
		$aStr[0] = "<TH $HbgTitleCell>${HtagTH_}�׸���${H_tagTH}</TH>";
		$aStr[1] = "<TD $HbgInfoCell align=center>$data[1]</TD>";
		$aStr[2] = "<TD $HbgInfoCell align=center>$sData[1]</TD>";
		$col++;
	}
	if($HuseBase || $HuseSbase) {
		$mStr[0] =  "<TH $HbgTitleCell>${HtagTH_}�߷���${H_tagTH}</TH>";
		$mStr[1] =  "<TD $HbgInfoCell align=center>$data[3]</TD>";
		$mStr[2] =  "<TD $HbgInfoCell align=center>$sData[3]</TD>";
		$col++;
	}
	if($HnavyName[0] ne '') {
		$nStr[0] =  "<TH $HbgTitleCell>${HtagTH_}���ɸ�${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}���轱${H_tagTH}</TH><TH $HbgTitleCell>${HtagTH_}���˲�${H_tagTH}</TH>";
		$nStr[1] =  "<TD $HbgInfoCell align=center>$data[8]</TD><TD $HbgInfoCell align=center>$data[9]</TD><TD $HbgInfoCell align=center>$data[10]</TD>";
		$nStr[2] =  "<TD $HbgInfoCell align=center>$sData[8]</TD><TD $HbgInfoCell align=center>$sData[9]</TD><TD $HbgInfoCell align=center>$sData[10]</TD>";
		$col += 3;
	}
	out(<<END);
<DIV ID='extInfo'><TABLE BORDER>
<TR>
$aStr[0]
<TH $HbgTitleCell>${HtagTH_}�ɷ���${H_tagTH}</TH>
$mStr[0]
<TH $HbgTitleCell>${HtagTH_}̱�߽�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ȯ��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���ɸ�${H_tagTH}</TH>
$nStr[0]
<TH $HbgTitleCell>${HtagTH_}�༣��${H_tagTH}</TH>
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
<TH $HbgTitleCell colspan='$col'>${HtagTH_}${HnormalColor_}������${H_normalColor}${sTurn}${HnormalColor_}��${H_normalColor}����${H_tagTH}</TH>
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
# �Ͽޤ�ɽ��
#----------------------------------------------------------------------
# $mode��1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
# $jsmode��1�ʤ顢JS�⡼��
# $no��0�Ǥʤ��ʤ顢������ɽ���⡼��
sub islandMap {
	my($mode, $jsmode, $no, $world) = @_;
	my($island) = $Hislands[$HcurrentNumber];
	my($id) = $island->{'id'};

	# ������ɽ���ν���
	my($mPoint, $mS, $mO, $fS, $fO);
	if($no) {
		$mPoint = missileMapSet($id, $no);
		$mS = $mPoint->{'self'};
		$mO = $mPoint->{'other'};
		$no = 0 if($mPoint == 0);
	}

	# �Ϸ����Ϸ��ͤ����
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landValue2) = $island->{'landValue2'};
	my($map) = $island->{'map'};
	my($l, $lv, $lv2);

	# ���ޥ�ɼ���
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
			if(($com->{'kind'} < 30) || $comNavyFlag{$com->{'kind'}}) { # ���ϷϤȺ��ϡ���������
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
	# ��ɸ(��)�����
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
						# �Ԥˤ�����Ĵ��
						$sx-- if(!($sy % 2) && ($y % 2));
						$sx = $correctX[$sx + $#an];
						$sy = $correctY[$sy + $#an];
						# �ϰϳ��ξ��
						next if(($sx < 0) || ($sy < 0));
						$HviewJam[$sx][$sy] = 1;
					}
				}
			}
		}
	}
	# ���Ϸ�����Ӳ��Ԥ����
	foreach $j (0..$#y) {
		$y = $y[$j];
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);
		out("<TABLE BORDER=0 cellpadding='0' cellspacing='0'><TR><TD class='M'>") if($no);

		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}$alpha>");
		} else {
			# �����ֹ�ʤ��ֹ�����
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



		# ���Ϸ������
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
					$islName = '��' . islandName($Hislands[$n]) . '��';
					$islName =~ s/<FONT COLOR=\"[\w\#]+\"><B>(.*)<\/B><\/FONT>/$1/g;
					$islName =~ s/<[^<]*>//g;
				} else {
					$islName = '��̤�Τγ����';
				}
			}
			landString($l, $lv, $lv2, $x, $y, $mode, $comStr[$x][$y], $jsmode, $no, $jamming, $wideFlag, $islName);
			if($no) {
				$fS = $mS->[$x][$y];
				$fO = $mO->[$x][$y];
#				out("<CENTER>") if($fS || $fO);
				if($fS ==1) {
					out("<span class='nodamage'>��</span>");
				} elsif($fS ==2) {
					out("<span class='defence'>��</span>");
				} elsif($fS ==3) {
					out("<span class='harden'>��</span>");
				} elsif($fS ==4) {
					out("<span class='hitpoint'>��</span>");
				}
				if($fO ==1) {
					out("<span class='nodamage'>��</span>");
				} elsif($fO ==2) {
					out("<span class='defence'>��</span>");
				} elsif($fO ==3) {
					out("<span class='harden'>��</span>");
				} elsif($fO ==4) {
					out("<span class='hitpoint'>��</span>");
				}
#				out("</CENTER>") if($fS || $fO);
				out("</TD>");
			}
			out("</A>");
		}

		out("<TD class='M'>") if($no);
		if($y % 2) {
			# ������ܤʤ��ֹ�����
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

		# ���Ԥ����
		out("</TD></TR></TABLE>\n") if($no);
		out("</BR>\n") unless($no);
	}

	# ��ɸ(��)�����
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
			$alt = '�����Ϸ�';
			$naviTitle  = $alt;
			$naviExp = "";
			$image = $HjammingSeaImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandWaste) {
		# ����
		$image = $HlandImage[$l][$lv];
		$alt = $HlandName[$l][$lv];
		$naviTitle  = $alt;
		$naviExp = "WASTE$lv";
		if($lv == 2) {
			$alt = 'Φ���Ϸ�';
			$naviTitle  = $alt;
			$naviExp = "";
			$image = $HjammingWasteImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "PLAINS";
	} elsif($l == $HlandForest) {
		# ��
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		# �Ѹ��Ԥξ����ڤ��ܿ�����
		if($mode && !($HoceanMode && $wideFlag)) {
			$naviText = "${lv}$HunitTree";
			$alt .= '(' . $naviText .')';
		}
		$naviExp = "FOREST";
	} elsif($l == $HlandTown) {
		# �ԻԷ�
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
		# ����
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviText  = "${lv}0${HunitPop}����";
		$alt .= '(' . $naviText .')';
		$naviExp = "FARM";
	} elsif($l == $HlandFactory) {
		# ����
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviText  = "${lv}0${HunitPop}����";
		$alt .= '(' . $naviText .')';
		$naviExp = "FACTORY";
	} elsif($l == $HlandBase) {
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$image = $HlandImage[$HlandForest];
			$alt = $HlandName[$HlandForest];
			$naviTitle  = $alt;
			$naviExp = "FOREST";
		} else {
			# �ߥ��������
			my($level) = expToLevel($l, $lv);
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "��٥� ${level}/�и��� $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "BASE";
		}
	} elsif($l == $HlandSbase) {
		# �������
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# �Ѹ��Ԥξ��ϳ��Τդ�
			$image = $HlandImage[$HlandSea][0];
			$alt = $HlandName[$HlandSea][0];
			$naviTitle  = $alt;
			$naviExp = "SEA0";
		} else {
			my($level) = expToLevel($l, $lv);
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "��٥� ${level}/�и��� $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "SEABASE";
		}
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HdBaseHide) {
				# �Ѹ��Ԥξ��Ͽ��Τդ�
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} else {
				# �Ѹ��Ԥξ����ѵ�������
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
				$naviText  = "�ѵ��� $lv";
				$alt .= '(' . $naviText .')';
			}
		}
	} elsif($l == $HlandBouha) {
		# ������
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "BOUHA";
	} elsif($l == $HlandSeaMine) {
		# ����
		if(!$mode || ($HoceanMode && $wideFlag)) {
			# �Ѹ��Ԥξ��ϳ��Τդ�
			$image = $HlandImage[$HlandSea][0];
			$alt = $HlandName[$HlandSea][0];
			$naviTitle  = $alt;
			$naviExp = "SEA0";
		} else {
			$image = $HlandImage[$l];
			$alt = $HlandName[$l];
			$naviTitle  = $alt;
			$naviText  = "�˲��� $lv";
			$alt .= '(' . $naviText .')';
			$naviExp = "SEAMINE";
		}
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HdBaseHide) {
				# �Ѹ��Ԥξ��Ͽ��Τդ�
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} else {
				# �Ѹ��Ԥξ����ɱһ��ߤΤդ�
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
		# ��������
		$image = $HlandImage[$l];
		$alt = $HlandName[$l];
		$naviTitle  = $alt;
		$naviExp = "OIL";
	} elsif($l == $HlandMountain) {
		# ��
		my $mlv = ($lv > 0) ? 1 : 0;
		$image = $HlandImage[$l][$mlv];
		$alt = $HlandName[$l][$mlv];
		$naviTitle  = $alt;
		if($mlv) {
			$naviText  = "${lv}0${HunitPop}����";
			$alt .= '(' . $naviText .')';
		}
		$naviExp = "MOUNTAIN$mlv";
	} elsif($l == $HlandCore) {
		# ����
		my($lFlag, $lLv) = (int($lv / 10000), ($lv % 10000));
		if(!$mode || ($HoceanMode && $wideFlag)) {
			if($HcoreHide) {
				# �Ѹ��Ԥξ��
				if(!$lFlag) { # ���Τդ�
					$image = $HlandImage[$HlandForest];
					$alt = $HlandName[$HlandForest];
					$naviTitle  = $alt;
					$naviExp = "FOREST";
				} else { # ���Τդ�
					$image = $HlandImage[$HlandSea][0];
					$alt = $HlandName[$HlandSea][0];
					$naviTitle  = $alt;
					$naviExp = "SEA0";
				}
			} else {
				# �Ѹ��Ԥξ����ѵ�������
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
				$naviText  = "�ѵ��� $lLv";
				$alt .= '(' . $naviText .')';
			}
		}
	} elsif($l == $HlandResource) {
		# �����
                my($tmp, $kind, $turn, $food, $money) = landUnpack($lv);
                if($kind == 0){
		    $image = $HlandImage[$l][$kind];
                    $money = 1200 + $money *20;
		    $alt = $HlandName[$l][$kind];
	            $naviText  = "${money}${HunitMoney}����";
	            $alt .= '(' . $naviText .')';
		    $naviExp = "OIL";
                }else{
		    $image = $HlandImage[$l][$kind];
                    $food = 1200 + $food * 20;
		    $alt = $HlandName[$l][$kind];
	            $naviText  = "${food}0${HunitFood}����";
	            $alt .= '(' . $naviText .')';
		    $naviExp = "OIL";
                }
	} elsif($l == $HlandMonument) {
		# ��ǰ��
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
		$naviTitle  = $alt;
		$naviExp = "MONIMENT$lv";
	} elsif($l == $HlandComplex) {
		# ʣ���Ϸ�
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		my $turn = $cTurn * $HcomplexTPrate[$cKind];
		my $tflag = $turn && (!$HcomplexTPhide[$cKind] || ($mode && !($HoceanMode && $wideFlag)));
		my $food = $HcomplexFPplus[$cKind] * $cFood + $HcomplexFPbase[$cKind];
		my $money = $HcomplexMPplus[$cKind] * $cMoney + $HcomplexMPbase[$cKind];
		if($HcomplexPretend[$cKind] && (!$mode || ($HoceanMode && $wideFlag))) {
			if($HcomplexPretend[$cKind] == 1) { # ���Τդ�
				$image = $HlandImage[$HlandForest];
				$alt = $HlandName[$HlandForest];
				$naviTitle  = $alt;
				$naviExp = "FOREST";
			} elsif($HcomplexPretend[$cKind] == 2) { # ���Τդ�
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
			$alt .= "F:${food}0${HunitPop}����/" if($food);
			if($money) {
				$alt .= "M:${money}0${HunitPop}����";
			} elsif($tflag || $food) {
				substr($alt, -1) = '';
			}
			$alt .= ")" if($tflag || $food || $money);
			$naviText .= "$HcomplexTPname[$cKind]\:${turn}$HcomplexTPunit[$cKind]<BR>" if($tflag);
			$naviText .= "��������:${food}0${HunitPop}����<BR>" if($food);
			if($money) {
				$naviText .= "������:${money}0${HunitPop}����";
			} else {
				substr($naviText, -4) = '';
			}
			$naviExp = "COMPLEX$cKind";
		}
	} elsif($l == $HlandMonster) {
		# ����
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HmonsterName[$kind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$id}]) if (defined $HidToNumber{$id});
		$name =~ s/<[^<]*>//g;

		$image = $HmonsterImage[$kind];

		# �Ų��桩
		$image = $HmonsterImage2[$kind] if ($flag & 1);

		# �����桩
		$image = $HmonsterImageUnderSea if ($flag & 2);

		$alt = "$mName(����${hp}/�и��� ${exp})$name";
		$naviTitle  = $mName;
		$naviText  = "������${hp}<BR>���и��� ${exp}";
		$naviText .= "<br>��$name" if (defined $name);
		$naviExp = "MONSTER$kind";
	} elsif($l == $HlandHugeMonster) {
		# �������
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		my $mName = $HhugeMonsterName[$kind];
		my($name);
		$name = islandName($Hislands[$HidToNumber{$id}]) if (defined $HidToNumber{$id});
		$name =~ s/<[^<]*>//g;
		if(($flag & 1) && ($flag & 2)) {
			# ���ǹŲ�
			$image = $HhugeMonsterImage4[$kind][$hflag];
		} elsif($flag & 1) {
			# Φ�ǹŲ�
			$image = $HhugeMonsterImage2[$kind][$hflag];
		} elsif($flag & 2) {
			# ��
			$image = $HhugeMonsterImage3[$kind][$hflag];
		} else {
			# Φ
			$image = $HhugeMonsterImage[$kind][$hflag];
		}
		$alt = "$mName(����${hp}/�и��� ${exp})$name";
		$naviTitle  = $mName;
		$naviText  = "������${hp}<BR>���и��� ${exp}";
		$naviText .= "<br>��$name" if (defined $name);
		$naviExp = "HUGEMONSTER$kind";
	} elsif($l == $HlandNavy) {
		# ����
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		my($level) = expToLevel($l, $exp);
		my @status = ('', '�༣', '���', '����');
		my $nName = $HnavyName[$kind];
                my($goal);
                if(($goalx == 31) ||
                   ($goaly == 31)) {
                    $goal = "������";
                }else{
                    $goal = "��ɸ($goalx, $goaly)";
                }

                $wait--;
                if($wait <= 0){
                    $ririku = "��ȯ�Ͻ���OK";
                }else{
                    $ririku = "��ΥΦ�Ԥ�${wait}������"
                }

                if(($kind != 0) && ($kind != 0x0c)){
                    $ririku = "";
                }

                # �Ҷ������ä���ɽ���ѹ�
                if($HnavyCruiseTurn[$kind] !=0){
                    $ririku = "��${wait}�������˵���";
                }

                # �����ѵ���
                my $maxHp = int($HnavyHP[$kind] * (120 + $exp) / 120);

		$image = $HnavyImage[$kind];
		$naviTitle  = $nName;
		$naviExp = "NAVY$kind";
		$alt = '';
		if ($flag == 1) {
			# �ĳ���
			$image = $HnavyImageZ;
			$alt  = "$nName�λĳ�";
			$alt .= "(�˲�Ψ${exp}%)" if($mode && !($HoceanMode && $wideFlag));
			$naviText = "$nName�λĳ�";
			$naviText .= "<BR>��(�˲�Ψ${exp}%)" if($mode && !($HoceanMode && $wideFlag));
		} else {
			if ($flag & 2) {
				# �����桩
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
				$fname = "${ofname}���� " if !($special & 0x8);
				$name = islandName($island);
				$name =~ s/<[^<]*>//g;
				$alt = "$name $fname";
				$naviText = "$name<BR>��$fname";
			} else {
				$alt = "��°���� ";
				$naviText = "��°���� ";
			}

			$alt .= $nName;
#			if(($mode && !($HoceanMode && $wideFlag)) || !(defined $num) || $HnavyShowInfo) {
				$status[$stat] .= '/' if($status[$stat] ne '');
                                if ($flag != 3) {
                                    if(($special & 0x8) || ($HnavyNoMove[$kind])){
				        $alt .= " (${status[$stat]}�ѵ���${hp}/${maxHp}���и���${exp} ${ririku})";
				        $naviText .= "<BR>��${status[$stat]}�ѵ���${hp}/${maxHp}<BR> �и���${exp}${ririku}";
                                    }else{
				        $alt .= " (${status[$stat]}�ѵ���${hp}/${maxHp}���и���${exp}��${goal} ${ririku})";
				        $naviText .= "<BR>��${status[$stat]}�ѵ���${hp}/${maxHp}<BR> �и���${exp}<BR> ${goal} ${ririku}";
                                    }
                                }else{
				    $alt .= " (${status[$stat]}��¤�� ${hp}/${HnavyBuildTurn[$kind]})";
				    $naviText .= "<BR>��${status[$stat]}��¤�� ${hp}/${HnavyBuildTurn[$kind]}";
				    $image = $HnavyImage3;
                                }
#			} elsif($stat) {
#				$alt .= " (${status[$stat]})";
#				$naviText .= "<BR>��(${status[$stat]}�⡼��)";
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
	# ��ȯ���̤ξ��ϡ���ɸ����
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
		# ��ȯ���̤ξ��ϡ���ɸ����
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

# ����(����)�μ����ϰϤ��ɤ�����ǧ
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
			# �Ԥˤ�����Ĵ��
			$sx-- if(!($sy % 2) && ($y % 2));
			$sx = $correctX[$sx + $#an];
			$sy = $correctY[$sy + $#an];

			# �ϰϳ��ξ��
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

# ������ɽ��
sub missileMapSet {
	my($id, $no) = @_;
	my($line, $m, $turn, $id1, $id2, $id3, $message, @ids, $x, $y, @mS, @mO);
	$no--;
	if(!open(LIN, "${HdirName}/${no}$HlogData")) {
		return 0;
	}
	my %kindName = ('�ɱ�'=>2, '̵��'=>1, '����'=>3, '�Ų�'=>3, '����'=>3, '̵��'=>1);
	while($line = <LIN>) {
		chomp($line);
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9\-]*),(.*)$/;
		($m, $turn, $id1, $id2, $id3, $message) = ($1, $2, $3, $4, $5, $6);
		next if($m eq '');
#		next if!($id1 == $id || ($id2 == $id && $id3 == ''));
		next if($id1 != $id);

		my $spliter = "<BR>��--- ";
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
			$spliter = "��";
			my @kinds = split(/$spliter/, $mes[1]);
			foreach my $k (@kinds) {
				$spliter = " �� ";
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

# �ޡ����󥰥⥸�塼��(�ɥ󥬥Х��礵�����)
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

// �ߥ������ϰϤΥޡ����󥰤򥻥å�
function set_mark(x, y) {
	if(!document.mark_form.mark.checked) return false;
	if(!document.getElementById) {
		alert("���ѿ���������ޤ��󤬡����Ȥ��Υ֥饦���Ϥ��ε�ǽ�򥵥ݡ��Ȥ��Ƥ��ޤ���");
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

		// �Ԥˤ�����Ĵ��
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
// ������ޡ����󥰲�
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

// �ޡ����󥰲��
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
// ������ޡ����󥰲�
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

// �ޡ����󥰲��
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

// ���ƤΥޡ����󥰤���
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
�ޡ�����<INPUT TYPE=CHECKBOX NAME="mark" onClick="mark_menu()">
����
<SELECT NAME="kind_mark">
<OPTION VALUE="">ɸ��
<OPTION VALUE="FFFF00">Yellow
<OPTION VALUE="FF0000">Red
<OPTION VALUE="0000FF">Blue
<OPTION VALUE="00FF00">Green
<OPTION VALUE="FF00FF">Purple
<OPTION VALUE="CCCCBB">Gray
<OPTION VALUE="-">None
</SELECT>
�ϰ�
<SELECT NAME="number_mark">
END
	my $max = max(2, @HnavyFireHex, @HnavyFireRange);
	foreach (0..$max) {
		my $s = ($_ == 2) ? ' SELECTED' : '';
		out("<OPTION VALUE=\"$an[$_]\"$s>${_}HEX");
	}
	out(<<END);
</SELECT>
��<INPUT TYPE="BUTTON" VALUE="���" onClick="unset_all_highlight();">
</FORM>
END
}

#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ���̥�ɽ��
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HrepeatTurn; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
}

# ������ؤ褦��������
sub tempPrintIslandHead {
	my($island, $mode) = @_;

	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}��${HcurrentName}��${H_tagName}�ؤ褦��������${H_tagBig}<BR>
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
//		StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // ��¦
		StyElm.style.marginLeft = -10; // ��¦
	} else {
//		StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // ��¦
		StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 90; // ��¦
	}
//	if(y - mapY + 1 == $HislandSizeY) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1.5) * $HchipSize*2; // ��¦
//	} else if(y - mapY + 1 > $HislandSizeY / 2) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // ��¦
//	} else {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // ��¦
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

# �����糫ȯ�ײ�
sub tempOwner {
	my($island) = $Hislands[$HcurrentNumber];
	out(<<END);
<DIV align='center'>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
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
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$island->{'id'}>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=16 MAXLENGTH=16 class=f>
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
	# �ײ��ֹ�
	my($j, $s);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		$s = ($i == $HcommandPlanNumber) ? 'SELECTED' : '';
		out("<OPTION VALUE=$i $s>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
END

	#���ޥ��
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
			$cost = '̵��';
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
<B>��ɸ(</B><SELECT NAME=POINTX>

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
<B>����</B><SELECT NAME=AMOUNT>
END

	# ����
	foreach $i (0..99) {
		out("<OPTION VALUE=$i>$i\n");
	}

	my($strUseNavy);
	$strUseNavy = "(�����ư��)" if($HnavyName[0] ne '');
	out(<<END);
</SELECT>
<HR>
<B>��ɸ��${AfterName}</B>${strUseNavy}��
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> ɽ\�� </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT><BR>
END
	if($HmlogMap) {
		out(<<END);
<BR><B> ������ɽ\�� </B><BR>
END
		my($i, $turn);
		for($i = 1;$i < $HtopLogTurn + 1;$i++) {
			$turn = $HislandTurn + 1 - $i;
			last if($turn < 0);
			out("[<A HREF=JavaScript:void(0); onClick=\"jump(myForm, '$HjavaMode', $i)\">");
			if($i == 1) {
				out("������${turn}(����)");
			} else {
				out("${turn}");
			}
			out("</A>]\n");
			out("<BR>\n") if($i%3==1);
		}
	}
	out(<<END);
<div align='left'>�����ư��</div>
<SELECT NAME=TARGETID2>
$HtargetList<BR>
</SELECT>
<HR>
<B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$island->{'id'}>
</FORM>
</TD>
<TD $HbgMapCell>
END
	# ���⹽����Ĵ�٤�
	my($id, $land, $landValue, $landValue2, $map) = ($island->{'id'}, $island->{'land'}, $island->{'landValue'}, $island->{'landValue2'}, $island->{'map'});
	my(@fleet);
	my(@nFleet) = (0, 0, 0, 0);
	my($x, $y, $nKind, $value, $value2, $name, %invade);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$nKind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			next if ($nKind != $HlandNavy);

			# ¾����δ���Ͻ���
			my($nId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp, $goalx, $goaly) = navyUnpack($value, $value2);
                        my($goal);
                        if(($goalx == 31) ||
                           ($goaly == 31)) {
                            $goal = "������";
                        }else{
                            $goal = "��ɸ($goalx, $goaly)";
                        }

                        $wait--;
                        if($wait <= 0){
                            $ririku = "��ȯ�Ͻ���OK";
                        }else{
                            $ririku = "��ΥΦ�Ԥ�${wait}������"
                        }

                # �Ҷ������ä���ɽ���ѹ�
                if($HnavyCruiseTurn[$nKind] !=0){
                    $ririku = "��${wait}�������˵���";
                }

                        if(($nKind != 0) && ($nKind != 0x0c)){
                            $ririku = "";
                        }

			if ($nId != $id) {
				$invade{"$nId,$nNo"} += 1;
				next;
			}

                        # �����ѵ���
                        my $maxHp = int($HnavyHP[$nKind] * (120 + $nExp) / 120);

			# �ĳ��Ͻ���
			next if ($nFlag == 1);

			my $nSpecial = $HnavySpecial[$nKind];
			# ���Ͻ���
			next if ($nSpecial & 0x8);

			$name = $HnavyName[$nKind];
			my $navyLevel = expToLevel($HlandNavy, $nExp);
			push(@{$fleet[$nNo]}, <<END);
<OPTION value="$x,$y">$name (�ѵ���${nHp}/${maxHp}����٥�${navyLevel}���и���${nExp}��${goal}${ririku})
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
			$ifname .= "<A STYlE=\"text-decoration:none\" href=\"${HthisFile}?Sight=${iId}\" target=\"_blank\">${iName}</A> $Hislands[$in]->{'fleet'}->[$iNo]����($invade{$_}��)<BR>"
		} else {
			$ifname .= "��°����($invade{$_}��)<BR>";
		}
	}
	$ifname .= '��';
	my $ofname = $island->{'fleet'};
	out(<<END) if($HnavyName[0] ne '');
<FORM NAME="FLEET">
<TABLE border=0 align="center">
<TR><TH>$ofname->[0]����</TH><TD><SELECT onfocus="selectFleetXY(0);" onchange="selectFleetXY(0);">@{$fleet[0]}</SELECT></TD><TD>($nFleet[0]��)</TD></TR>
<TR><TH>$ofname->[1]����</TH><TD><SELECT onfocus="selectFleetXY(1);" onchange="selectFleetXY(1);">@{$fleet[1]}</SELECT></TD><TD>($nFleet[1]��)</TD></TR>
<TR><TH>$ofname->[2]����</TH><TD><SELECT onfocus="selectFleetXY(2);" onchange="selectFleetXY(2);">@{$fleet[2]}</SELECT></TD><TD>($nFleet[2]��)</TD></TR>
<TR><TH>$ofname->[3]����</TH><TD><SELECT onfocus="selectFleetXY(3);" onchange="selectFleetXY(3);">@{$fleet[3]}</SELECT></TD><TD>($nFleet[3]��)</TD></TR>
<TR><TH>$HtagTH_¾��δ���$H_tagTH</TH><TD class='N' colspan=2>$ifname</TD></TR>
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
	islandMap(1, 0, 0); # ����Ͽޡ���ͭ�ԥ⡼��
	islandMarking($island, 0);
	out(<<END);
<FORM NAME=SIGHTS>
<B>��ɸ��${AfterName}</B><BR><SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<INPUT TYPE="button" VALUE="�ޥåפ򳫤�" onclick="printIsland();">
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
				$priList[$i] .= "��" if($pFlag);
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
			$priSelectList .= "<BR>��" if($i && $i % 4 == 0);
			$priSelectList .= "��" if($i);
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
	my @status = ('', '�༣', '���', '����');
	my($fkind) = $island->{'fkind'};
	my @flist = @$fkind;
	my @fleetlist = ();
#	my @idx = (0..$#flist);
#	@idx = sort { (navyUnpack(hex($flist[$a])))[0] <=> (navyUnpack(hex($flist[$b])))[0] || (navyUnpack(hex($flist[$a])))[7] <=> (navyUnpack(hex($flist[$b])))[7] } @idx;
#	@flist = @flist[@idx];
	foreach (@flist) {
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $wait, $nHp) = navyUnpack(hex($_));#���֡��ǰ��ä�
		next if ($HnavySpecial[$nKind] & 0x8); # �����Ͻ���
		my($s, $l) = ();
		my $navyLevel = expToLevel($HlandNavy, $nExp);
		$s = "\n�ѵ���$nHp/��٥�$navyLevel/�и���$nExp";
		$s = " [${status[$nStat]}]" . $s if($nStat);
		if(($eId != $id) && (defined $HidToNumber{$eId})) {
			my $name = islandName($Hislands[$HidToNumber{$eId}]);
			$name =~ s/<[^<]*>//g;
			$s .= "\n${name}���ɸ���";
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
		push(@fleetMove, " <small>��ư����<B>$str</B></small>");
	}

	out(<<END);
</TD></TR>
<TR><TD colspan=3 class='M'><DIV align='center'>
<TABLE BORDER><TR><TD class='M'>
END

	islandInfoWeather() if($HuseWeather); # ���ݾ���
	islandData(); # ��ĥ�ǡ���
	islandInfoSub(1) if($HnavyName[0] ne ''); # ����DATA

	out(<<END);
</TD></TR></TABLE>
</DIV></TD></TR>
</TABLE>
</DIV>
<HR>
<DIV ID='CommentBox'>
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<TABLE BORDER=0>
<TR>
<TH>������<BR><small>(����${HlengthMessage}���ޤ�)</small></TH>
<TD colspan=2><INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"></TD>
</TR>
<TR>
<TH>�ѥ����</TH><TD colspan=2><INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" class=f>
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$island->{'id'}>
</TD>
</TR>
END

	out(<<END) if($HnavyName[0] ne '');
<TR>
</FORM>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<TH colspan=3>����̾�ѹ�<small>(����${HlengthFleetName}���ޤ�)</small> ��()��Ϻ�Ũ��</TH></TR>
<TR><TH>�裱����</TH><TD colspan=2>$fleetlist[0]<br><INPUT TYPE=text NAME=FLEET1 SIZE=20 VALUE="$ofname->[0]">����$fleetMove[0] $priList[0]</TD></TR>
<TR><TH>�裲����</TH><TD colspan=2>$fleetlist[1]<br><INPUT TYPE=text NAME=FLEET2 SIZE=20 VALUE="$ofname->[1]">����$fleetMove[1] $priList[1]</TD></TR>
<TR><TH>�裳����</TH><TD colspan=2>$fleetlist[2]<br><INPUT TYPE=text NAME=FLEET3 SIZE=20 VALUE="$ofname->[2]">����$fleetMove[2] $priList[2]</TD></TR>
<TR><TH>�裴����</TH><TD colspan=2>$fleetlist[3]<br><INPUT TYPE=text NAME=FLEET4 SIZE=20 VALUE="$ofname->[3]">����$fleetMove[3] $priList[3]</TD></TR>
<TR><TD colspan=3 align=center><INPUT TYPE=submit VALUE="����̾�ѹ�" NAME=FleetnameButton$island->{'id'}></TD></TR>
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
<TH>��Ũ���ѹ�</TH><TD><SELECT NAME=PSF onChange=priorityChange() onClick=priorityChange()>
END
		foreach (0..3) {
			out("<OPTION VALUE=$_>$ofname->[$_]\n");
		}
	out(<<END);
</SELECT>���⡡</TD><TD>
$priSelectList
<INPUT TYPE=submit VALUE="�ѹ�" NAME=PriorityButton$island->{'id'}></TD>
END
	}

	my($earth);
	if($HroundView == 2) {
		my $earthstr = ($island->{'earth'} ? '����ɽ��<B><FONT COLOR="#FF0000">����</FONT></B>' : '����ɽ��<B><FONT COLOR="#0000FF">���ʤ�</FONT></B>');
		$earth = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>����ɽ������</TH><TD colspan=2>$earthstr<INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=EarthButton$island->{'id'}></TD></TR>";
	}

	my($comflag);
	if($HcomflagUse >= 2) {
		my $comflagstr = ($island->{'comflag'} ? '�ʤ��Ƥ�' : '�ʤ����');
		my $comflagtmp = ($island->{'comflag'} ? '<FONT COLOR="#FF0000">���ʤ�</FONT>' : '<FONT COLOR="#0000FF">����</FONT>');
		$comflag = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>���ޥ�ɼ¹�����</TH><TD colspan=2>���ޥ�ɤ��¹ԤǤ�${comflagstr}��ͽ�꥿����򷫤�夲�Ƽ¹�<B>$comflagtmp</B><INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=ComflagButton$island->{'id'}></TD></TR>";
	}

	my($preab);
	if($HarmisticeTurn && $HuseCoDevelop) {
		my $preabstr = ($island->{'preab'} ? '�ʤ��Ƥ�' : '�ʤ����');
		my $preabtmp = ($island->{'preab'} ? '<FONT COLOR="#FF0000">���Ĥ���</FONT>' : '<FONT COLOR="#0000FF">���Ĥ��ʤ�</FONT>');
		$preab = "</FORM><FORM action=\"$HthisFile\" method=\"POST\"><INPUT TYPE=\"hidden\" NAME=JAVAMODE value=\"$HjavaMode\"><INPUT TYPE=hidden NAME=PASSWORD VALUE=\"$HdefaultPassword\"><TR><TH>�رĶ�Ʊ��ȯ</TH><TD colspan=2>�ر��¤����${preabstr}���رĥѥ���ɤǳ�ȯ���̤����뤳�Ȥ�<B>$preabtmp</B><INPUT TYPE=submit VALUE=\"�ѹ�\" NAME=PreabButton$island->{'id'}></TD></TR>";
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

# ���ϺѤߥ��ޥ��ɽ��
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
		$tName = "̵��${AfterName}";
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
	out("$HtagNumber_$j$H_tagNumber$HnormalColor_($turn)��");
	if(!$HcomUse{$kind}) {
		out("$HtagComName2_���Υ��ޥ�ɤϻȤ��ʤ��ʤ�ޤ���$H_tagComName");
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
	} elsif (($HcomMissile[0] < $kind) && ($kind <= $HcomMissile[$#HmissileName])) { # �ߥ�����ȯ��
		# �ߥ������
		my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
		out("$tName$point��$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomAmity) {
		# ͧ���� ���ꡦ���
		if($target != $island->{'id'}) {
			out("$tName��$name");
		} else {
			out("<B>���Ƥ�${AfterName}</B>��$name");
		}
	} elsif($kind == $HcomAlly) {
		# Ʊ�� ������æ��
		out("$tName��$name");
	} elsif(($kind == $HcomDeWar) || ($kind == $HcomCeasefire)) {
		# �����۹�����
		out("$tName��$name");
	} elsif(($kind == $HcomSendMonster) ||
		($kind == $HcomSendMonsterST)) {
		# �����ɸ�
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
		out("$tName��$name($HtagName_$mName$H_tagName)");
	} elsif (($HcomNavy[0] < $kind) && ($kind <= $HcomNavy[$#HnavyName])) { # ������¤
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name .= "($ofname->[$arg]����)";
		$name = "$point��$name" if($HnavyBuildFlag);
		if($land->[$x][$y] != $HlandSea || ($HnavyBuildFlag && $landValue->[$x][$y])) {
			out("${HtagDisaster_}��${H_tagDisaster}");
		} elsif($HmaxComPortLevel) {
			my $flag = 0;
			my($p, $px, $py);
			if($HnavyBuildFlag) {
				($p, $px, $py) = searchNavyPort($island, $x, $y, 7);
			} else {
				($p, $px, $py) = searchNavyPort($island, $x, $y, 0);
			}
			my($pId, $pTmp, $pStat, $pSea, $pExp, $pFlag, $pNo, $pKind, $pWait, $pHp) = navyUnpack($landValue->[$px][$py], $landValue2->[$px][$py]);#������ɬ�פʤ��ä�����
			$flag = expToLevel($HlandNavy, $pExp);
			if($flag) {
				if($HcomNavyNumber[($flag - 1)] >= $kind - $HcomNavy[0]) {
					$flag = 1;
				} else {
					$flag = 0;
				}
			}
			out("${HtagDisaster_}��${H_tagDisaster}") if(!$flag);
		}
		out("$name");
	} elsif ($kind == $HcomNavySend) {
		# �����ɸ�
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("$tName��$name");
	} elsif ($kind == $HcomNavyReturn) {
		# ���ⵢ��
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("$tName����$name");
	} elsif ($kind == $HcomNavyMove) {
		# �����ư
		my $tn2 = $HidToNumber{$target2};
		my $tName2;
		if($tn2 eq '') {
			$tName2 = "̵��${AfterName}";
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
		my $comName = ($island->{'id'} == $target2) ? '���ⵢ��' : '�����ɸ�';
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${comName}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${comName}$H_tagComName";
		if($island->{'id'} == $target2) {
			out("$tName����$name");
		} elsif($island->{'id'} == $target) {
			out("$tName2��$name");
		} else {
			out("$tName����$tName2��$name");
		}
	} elsif ($kind == $HcomNavyForm) {
		# ��������
		if ($arg < 1) {
			$arg = 1;
		} elsif ($arg > 4) {
			$arg = 4;
		}
		$arg--;
		$name = ($HcomTurn[$kind] > 0) ? "$HtagComName1_$ofname->[$arg]${HcomName[$kind]}$H_tagComName" : "$HtagComName2_$ofname->[$arg]${HcomName[$kind]}$H_tagComName";
		out("${HtagDisaster_}��${H_tagDisaster}") if($land->[$x][$y] != $HlandNavy);
		out("$point��$name");
	} elsif(($kind == $HcomSell) ||
		($kind == $HcomBuy)) {
		# ����͢�С�����͢��
		my($value2) = ($arg < 1) ? $HcomCost[$kind] : $arg * $HcomCost[$kind];
                my $foodrate = int(($island->{'money'}/$HmaximumMoney) / (($island->{'food'} + 0.01)/$HmaximumFood));
                if($foodrate < 5){
                    $foodrate = 5;
                }elsif($foodrate > 20){
                    $foodrate = 20;
                }
		if($value2 < 0) {
			$value2 = int(-$value2  * $foodrate / 40);
			$value2 = "$value2$HunitMoney����";
		} else {
			$value2 = int($value2 / $foodrate * 10 / 4);
			$value2 = "$value2$HunitFood����";
		}
		$value2 = "$HtagName_$value2$H_tagName";
		out("$name$value ($value2)");
	} elsif(($kind == $HcomPropaganda) ||
                ($kind == $Hcomshikin)) {
		# Ͷ�׳�ư����ⷫ��
		if($arg == 0) {
			out("$name");
		} else {
			out("$name($arg��)");
		}
	} elsif(($kind == $HcomMoney) ||
		($kind == $HcomFood)) {
		# ���
		out("$tName��$name$value");
	} elsif($kind == $HcomDestroy) {
		# ����
		if($arg != 0) {
			out("$point��$name(ͽ��${value})");
		} else {
			out("$point��$name");
		}
	} elsif($kind == $HcomDbase) {
		# ����դ�
		if(!$arg || !$HdurableDef) {
			if(!$HdurableDef && $land->[$x][$y] == $HlandDefence) {
				out("$point��$name(����)");
			} else {
				out("$point��$name");
			}
		} elsif($arg == $HdefExplosion && $land->[$x][$y] == $HlandDefence) {
			out("$point��$name(����)");
		} else {
			out("$point��$name($arg��)");
		}
	} elsif(($kind == $HcomFarm) ||
		 ($kind == $HcomFastFarm) ||
		 ($kind == $HcomFactory) ||
		 ($kind == $HcomFastFactory) ||
		 ($kind == $HcomMountain)) {
		# ����դ�
		if($arg == 0) {
			out("$point��$name");
		} else {
			out("$point��$name($arg��)");
		}
	} elsif (($HcomComplex[0] <= $kind) && ($kind <= $HcomComplex[$#HcomplexComName])) { # ʣ���Ϸ�����
		# ����դ�
		if($arg == 0) {
			out("$point��$name");
		} else {
			out("$point��$name($arg��)");
		}
	} elsif($kind == $HcomSeaMine) {	
		# �˲����դ�
		$arg = 1 if($arg == 0);
		$arg = $HmineDamageMax if($arg > $HmineDamageMax);
		if($land->[$x][$y] == $HlandSeaMine) {
			$name = ($HcomTurn[$kind] > 0) ? "${HtagComName1_}�������${H_tagComName}" : "${HtagComName2_}�������${H_tagComName}";
		} else {
			$name .= "(�˲���:$arg)";
		}
		out("$point��$name");
	} elsif(($kind == $Hcomgoalsetpre) ||
	        ($kind == $Hcomgoalset)) {
                # ��Ū������
		out("$tName$point��$name");
	} elsif($kind == $HcomMoveTarget) {
		# �����դ�
		my $s;
		$arg %= 19;
		if($arg == 1) {
			$s = '����';
		} elsif($arg == 2) {
			$s = '��';
		} elsif($arg == 3) {
			$s = '����';
		} elsif($arg == 4) {
			$s = '����';
		} elsif($arg == 5) {
			$s = '��';
		} elsif($arg == 6) {
			$s = '����';
		} elsif(($arg > 6) && ($arg < 19)) {
			$arg -= 6;
			$s = "$arg��";
		} else {
			$arg = 0;
			$s = '�Ե�';
		}
		out("${HtagDisaster_}��${H_tagDisaster}") if(($target == $id) && ($land->[$x][$y] != $HlandNavy));
		out("$tName$point�ǰ�ư���($s)");
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
			out("$name$ofname->[$fNo - 1]������Ф���${name}��${HtagName_}���${H_tagName}");
		} else {
			out("$name$ofname->[$fNo - 1]������Ф�$tName$point�ؤ�${name}");
		}
	} elsif($kind == $HcomNavyTarget) {
		out("$tName$point��$name");
	} elsif($kind == $HcomMonument) {
		if($HuseBigMissile && ($land->[$x][$y] == $HlandMonument)) {
			out("$point��$name($tName��ȯ��)");
		} else {
			$arg = $HmonumentNumber - 1 if($arg >= $HmonumentNumber);
			out("$point��$name($HmonumentName[$arg])");
		}
	} elsif($kind == $Hcomremodel){
                # ����
                my $tmp;
                if($arg == 0){
                    $tmp = '����';
                }elsif($arg == 1){
                    $tmp = '����';
                }elsif($arg == 2){
                    $tmp = '�ɶ�';
                }else{
                    $tmp = '����';
                }
		out("$point��$name($tmp)");
	} elsif($kind == $Hcomwork){
                # Ÿ��
                my $tmp;
                if($arg == 0){
                    $tmp = '����';
                }elsif($arg == 1){
                    $tmp = '����';
                }elsif($arg == 2){
                    $tmp = '�η�';
                }else{
                    $tmp = '����';
                }
		out("$tName$point��$name($tmp)");
	} elsif($kind == $HcomNavyDestroy){
                # �����˴�
		out("$tName$point��$name");
	} elsif($kind == $HcomSellPort){
                # ����ʧ����
		out("$tName$point��$name");
	} elsif($kind == $HcomBuyPort){
                # �������
		out("$tName$point��$name");
	} else {
		# ��ɸ�դ�
		out("$point��$name");
	}
	out("$H_normalColor");
	out("</A>") if($mode);
	out("<BR>\n");
}

# ���ޥ�ɺ��
sub tempCommandDelete {
	out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ�����${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
	out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ�����${H_tagBig}<HR>
END
}

# �������ѹ�����
sub tempComment {
	out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ�����${H_tagBig}<HR>
END
}

# ����̾�ѹ�����
sub tempFleetName {
	out(<<END);
${HtagBig_}����̾���ѹ����ޤ�����${H_tagBig}<HR>
END
}

# ��Ũ���ѹ�����
sub tempPriority {
	out(<<END);
${HtagBig_}��Ũ����ѹ����ޤ�����${H_tagBig}<HR>
END
}

# �ᶷ
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
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}�ζᶷ${H_tagBig}
<INPUT type=hidden name="ID" value="$HcurrentID">
$pass
<INPUT type="submit" value="�ᶷ�򸫤�" onClick="Recent()">
</FORM>
</DIV></DIV>
END
	} else {
		out(<<END);
<DIV ID='RecentlyLog'>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST">
<HR>
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}�ζᶷ${H_tagBig}
��<a HREF="${HbaseDir}/history.cgi?ID=$HcurrentID&Event=99" onClick="document.recentForm.target='newWindow';document.recentForm.submit();return false;" style="text-decoration:none;" target='_blank'>[���${HtopLogTurn}������ʬ�Υ���ɽ��]</a>
<INPUT type=hidden name="ID" value="$HcurrentID">
<INPUT type=hidden name="Event" value="99">
$pass
END
		logPrintLocal($mode);
		out("</FORM></DIV>");
	}
}

# ��ΰ�ư
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
<INPUT type=hidden name=title value='${name}�Ѹ��Ǽ���'>
<INPUT type=hidden name=message value='�褦������${name}�Ѹ�������'>
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
${HtagBig_}${HtagName_}${HcurrentName}${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
<FORM name="exLbbs" action="${HlbbsDir}/lbbs.cgi" method=POST encType=multipart/form-data>
<INPUT type=hidden name=mode value='view'>
$admin
<INPUT type=hidden name=owner value="$mode">
<INPUT type=hidden name=logfile value="${bbsID}.cgi">
<INPUT type=hidden name=id value="$id">
<INPUT type=hidden name=pass value="$HdefaultPassword">
<INPUT type=submit value='�Ѹ��Ǽ��Ĥα��������' onClick="Exlbbs()">
</FORM>
</DIV>
END
}

# �����������Ѥ�׻�
sub calcSea {
	my($island) = @_;

	my($sea) = 0;

	# �Ϸ������
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};

	# ������
	my($x, $y, $kind, $value);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$sea++ if(($land->[$x][$y] == $HlandSea) && !$landValue->[$x][$y]);
	    }
	}

	return $sea;
}
#----------------------------------------------------------------------
# �����ͤˤ���Ϸ��ǡ�����¸������
#----------------------------------------------------------------------
sub islandSaveMain() {

	if (!$HisaveMode || !$HcurrentID) {
		# ����
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempIslandSavePage(0);
		return;
	} else {
		# �ѥ����
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if(!checkPassword($island, $HdefaultPassword) && !checkSpecialPassword($HdefaultPassword)) {
			# �ѥ���ɥ����å�
			# �ü�ѥ����
			# password�ְ㤤
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
			# ��¸
			island_save($island, $HsavedirName, 'save', 0);
		} elsif($HisaveMode == 3) {
			# ����
			island_load($island, 0);
		} elsif($HisaveMode == 4) {
			# ��¸������(�ǡ����������ؤ�)
			island_load($island, 1);
		} elsif($HisaveMode == 5) {
			# ��¸(���������)
			island_save($island, $HsavedirName, 'save', 1);
		} elsif($HisaveMode == 6) {
			# ����(���������)
			island_load($island, 2);
		} elsif($HisaveMode == 7) {
			# ��¸������(���������)
			island_load($island, 3);
		}
	}
	# ����
	unlock();
	# �ƥ�ץ졼�Ƚ���
	tempIslandSavePage(1);
}

# �Ϸ��ǡ�����¸�������ڡ���
sub tempIslandSavePage() {
	my($mode) = @_;

	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>�Ϸ��ǡ�����¸������</H1>
<FORM action="$HthisFile" method="POST">
<B>�Ϸ��ǡ�������¸����������${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}�����򤷤Ʋ�����-
$HislandList
</SELECT><BR><BR>
�ѥ����:<INPUT TYPE="password" NAME="ISave" VALUE="$HdefaultPassword" MAXLENGTH=32 class=f>
<INPUT TYPE="submit" VALUE="�ǡ�����ǧ" NAME="IslandChoice"><BR>
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
<H1 style='display:inline'>������${HislandTurn}����</H1>
<BR>${HtagTH_}��⡧<span class='money'>$island->{'money'}$HunitMoney</span>
��������<span class='food'>$island->{'food'}$HunitFood</span>${H_tagTH}
END
	printMap($land, $landValue, $map, 1);
	if(checkSpecialPassword($HdefaultPassword)) {
		out("<INPUT TYPE=\"submit\" VALUE=\"��¸\" NAME=\"SaveButton\">");
		out("<INPUT TYPE=\"submit\" VALUE=\"��¸(���������)\" NAME=\"SaveLandButton\">");
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
		my $money = shift(@mandf);   # ���
		my $food = shift(@mandf);    # ����
		my $tmp = pop(@mandf);       # �ޥå�
		my(@xytmp) = split(/<>/, $tmp);
		my(@x) = split(/\,/, $xytmp[0]);
		my(@y) = split(/\,/, $xytmp[1]);
		my $map = { 'x' => \@x, 'y' => \@y };
		$map = $island->{'map'} if(!@x || !@y || !$HoceanMode);

		($land, $landValue) = readLand($map, @line);

		out(<<END);
<TD class='T'>
<H1 style='display:inline'>�����֥ǡ���</H1>
<BR>${HtagTH_}��⡧<span class='money'>${money}${HunitMoney}</span>
��������<span class='food'>${food}${HunitFood}</span>${H_tagTH}
END
		printMap($land, $landValue, $map, 1);
		if(checkSpecialPassword($HdefaultPassword)) {
			out("<INPUT TYPE=\"submit\" VALUE=\"����\" NAME=\"LoadButton\">");
			out("<INPUT TYPE=\"submit\" VALUE=\"����(���������)\" NAME=\"LoadLandButton\">");
		}
	}
	out("</TD></TR>");
	if($savedata && checkSpecialPassword($HdefaultPassword)) {
		out("<TR><TD class='T' colspan=2>");
		out("<INPUT TYPE=\"submit\" VALUE=\"��¸������(�ǡ����������ؤ�)\" NAME=\"ChangeButton\">");
		out("<INPUT TYPE=\"submit\" VALUE=\"��¸������(���������)\" NAME=\"ChangeLandButton\">");
		out("</TD></TR>");
	}
	out("</TABLE>");
	out("</FORM>");
	out("</DIV>");
}

#------------------------------------------------
# �ȡ��ʥ��ȥ⡼��
#------------------------------------------------
# ������ޥå�ɽ��
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
	chomp($name = <IN>);     # ���̾��
	chomp($owner = <IN>);    # �����ʡ���̾��
	$birthday = int(<IN>);   # ���ϥ�����
	$id = int(<IN>);         # ID�ֹ�
	chomp($prize = <IN>);    # ����
	chomp(($absent, $preab, $comflag) = split(/\,/, <IN>)); # Ϣ³��ⷫ���, ��ȯ����(�رĤ�������), ���ޥ�ɼ¹�����
	chomp($comment = <IN>);  # ������
	chomp($password = <IN>); # �Ź沽�ѥ����
	$money    = int(<IN>);   # ���
	$food     = int(<IN>);   # ����
	$pop      = int(<IN>);   # �͸�
	$area     = int(<IN>);   # ����
	$farm     = int(<IN>);   # ����
	$factory  = int(<IN>);   # ����
	$mountain = int(<IN>);   # �η���
	chomp($tmp = <IN>);      # ͧ����
		@amity = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ����̾
		@fleet = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ��Ũ��
		@priority = split(/\,/, $tmp);
	chomp($tmp = <IN>);      # ��ͭ��������
		@fkind = split(/\,/, $tmp);
	$gain     = int(<IN>);   # ������и���
	$monskill = int(<IN>);   # �����༣��
	chomp($monslive = <IN>); # ���ýи���, ����, ����(����), ��°���������и���, ����
	chomp($tmp = <IN>);      # ������
		@sinktmp = split(/\-/, $tmp);
			@sink = split(/\,/,$sinktmp[0]);        # ����ʳ��δ���
			@sinkself = split(/\,/,$sinktmp[1]);    # ����
			@subSink = split(/\,/,$sinktmp[2]);     # ���ּ���ʳ��δ���
			@subSinkself = split(/\,/,$sinktmp[3]); # ���ּ���
	chomp($tmp = <IN>);      # ��ĥ�ΰ�
		@exttmp = split(/<>/, $tmp);
			@ext = split(/\,/,$exttmp[0]);    # ��ĥ�ΰ�
			# �����ե饰, �׸���x10, �ɷ���, �߷���, ̱�߽�, ������, ��ȯ��, ���ɸ�, ���ɸ�, ���轱, ���˲�
			@subExt = split(/\,/,$exttmp[1]); # ���ֳ�ĥ�ΰ�
			# ��Ͽ������, �׸���x10, �ɷ���, �߷���, ̱�߽�, ������, ��ȯ��, ���ɸ�, ���ɸ�, ���轱, ���˲�, �༣��, �󾩶�
	chomp($field = <IN>);    # �ե������°��
	chomp($tmp = <IN>);      # �����ƥ�
		@item = split(/\,/, $tmp);
	chomp($tmp = <IN>); # ����,����,����,��®,����,����,�۾�,ŷ��(��ɽ����)
		$tmp = "20,1013,40,0,0,0,0,2,2,2,2" if($tmp == '');
		@weather = split(/\,/, $tmp);
	chomp(($fight_id, $rest) = split(/\,/, <IN>)); # �ȡ��ʥ��� �������ID, ��ȯ��߻Ĥ꥿�����
	chomp($tmp = <IN>); # ���٥�ȥե饰 ���ϥ����� ���� ������ �ϼ� ���� ������ ����� ������� �����ͥץ쥼��Ȥ�̵ͭ ��������ƥ� �ɲ��ɸ� ���ýи�1 ���ýи�2 ������ýи�1 ������ýи�2 �����и�1 �����и�2 ��ư����
		$tmp = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" if($tmp == '');
		@event = split(/\,/, $tmp);
	$point = int(<IN>); # �ݥ����
	chomp($tmp = <IN>); # ���פ�������̾,�������,������
		@defeat = split(/\,/, $tmp);
	chomp($tmp = <IN>); # ���٥�ȥݥ����
		@epointtmp = split(/\,/, $tmp);
		for($i=0;$i<$#epointtmp;$i+=2) {
			$epoint{$epointtmp[$i]} = $epointtmp[$i+1];
		}
	chomp($tmp = <IN>);      # �ޥå������Ǽ x0,x1,...,xn<>y0,y1,...,yn
		@xytmp = split(/<>/, $tmp);
		@x = split(/\,/, $xytmp[0]);
		@y = split(/\,/, $xytmp[1]);
		if(!@x || !@y || !$HoceanMode) {
			@x = @defaultX;
			@y = @defaultY;
		}
		$map = { 'x' => \@x, 'y' => \@y };
		$wmap = { 'x' => $xytmp[2], 'y' => $xytmp[3] };
	<IN>; # ͽ��
	<IN>; # ͽ��
	<IN>; # ͽ��
	chomp(my @line = <IN>);
    close(IN);
    
	my(@land) = readLand($map, @line);

	if($HcurrentID != $id) {
		unlock();
		tempProblem();
		return;
	}

	my(@command, @lbbs);
	# ������ޥ�ɤ�����
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
	# ����Ǽ��Ĥ����
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
			# ����
			unlock();

			out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}${AfterName}�����դ������Ǥ��ޤ��󡪡�${H_tagBig}
END
			return;
		} else {
			# ID�λȤ���
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
				# �����⡼��
				$HislandNumber++;
				$islandNumber++;
				$HislandNextID ++;
				$HislandNextID = 1 if($HislandNextID > 100);
				require('./hako-make.cgi');
				# ���ե�����Ĵ��
				logFileAdjust(-1, $newID);
				# �Ϸ��ǡ������Ǽ���Ĵ��
				islandFileAdjust(-1, $newID);
				if($HoceanMode) {
					$wmap = randomIslandMap() if(defined $HidToNumber{$HoceanMap[$wmap->{'x'}][$wmap->{'y'}]}); # ��κ�ɸ�����
					@x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
					@y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
					$map = { 'x' => \@x, 'y' => \@y };
				}
			}
		}
	} elsif(($mode >= 3) && ($HislandNumber - $HbfieldNumber >= $HmaxIsland)) {
		# ����
		unlock();

		out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}${AfterName}�����դ������Ǥ��ޤ��󡪡�${H_tagBig}
END
		return;
	} else {
		$newID = $HcurrentID;
		$num   = $HislandNumber;
		$HidToNumber{$newID} = $num;
		if($mode >= 3) {
			# �����⡼��
			$HislandNumber++;
			$islandNumber++;
			if($HoceanMode) {
				$wmap = randomIslandMap() if(defined $HidToNumber{$HoceanMap[$wmap->{'x'}][$wmap->{'y'}]}); # ��κ�ɸ�����
				@x = (($wmap->{'x'} * $HislandSizeX)..($wmap->{'x'} * $HislandSizeX + $HislandSizeX - 1));
				@y = (($wmap->{'y'} * $HislandSizeY)..($wmap->{'y'} * $HislandSizeY + $HislandSizeY - 1));
				$map = { 'x' => \@x, 'y' => \@y };
			}
		}
	}
	# land,landValueĴ��
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
		my $titleStr = (!$mode) ? '��������ͻ�' : '��¸�Ϸ��ξ���';
	    out ("<DIV align='center'>");
		if($mode) {
			my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;
			out("$HtempBack2<BR>");
		} else {
			out("<a href=${HthisFile}?FightLog=0>${HtagBig_}���${H_tagBig}</a><BR>");
		}
	    out ("<BR>${HtagBig_}${HtagName_}��${islandName}��<BR>${H_tagName}$titleStr${H_tagBig}<BR>");
		printMap($land[0], $land[1], $map, 0);

	} elsif(($mode >= 3) && checkSpecialPassword($HdefaultPassword)) {
		# �����⡼��
		my $HtempBack2 = "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}";

		require('./hako-turn.cgi');
		# �͸�����¾����
		estimate($num);
		islandSort($HrankKind, 1);

		# �ǡ����񤭽Ф�
		writeIslandsFile($newID);

		# ����
		unlock();

		out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR><BR>
${HtagBig_}$islandName���������ޤ�����${H_tagBig}
END
		return;

	} else {
		unlock();
		tempProblem();
		return;
	}
}

# ��������ͻ�ɽ��(�������ǡ�������¸�ǡ���)
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
//		StyElm.style.marginLeft = (x - mapX - 5) * $HchipSize*2; // ��¦
		StyElm.style.marginLeft = -10; // ��¦
	} else {
//		StyElm.style.marginLeft = (x - mapX + 2) * $HchipSize*2; // ��¦
		StyElm.style.marginLeft = $HislandSizeX * $HchipSize*2 - 120; // ��¦
	}
//	if(y - mapY + 1 == $HislandSizeY) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY + 0.5) * $HchipSize*2; // ��¦
//	} else if(y - mapY + 1 > $HislandSizeY / 2) {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 2) * $HchipSize*2; // ��¦
//	} else {
//		StyElm.style.marginTop = (y - mapY - $HislandSizeY - 1) * $HchipSize*2; // ��¦
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
	# ��ɸ(��)�����
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

	# ���Ϸ�����Ӳ��Ԥ����
	foreach $y (@my) {
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);
		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			# �������ܤʤ��ֹ�����
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

		# ���Ϸ������
		$HpopupNavi = 0 if($mode);
		foreach $x (@mx) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $lv2, $x, $y, $mode, '', 0, 0, 0);#�����ϻȤ�ʤ��������
			out("</A>");
		}

		if($y % 2) {
			# ������ܤʤ��ֹ�����
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

		# ���Ԥ����
		out("</BR>\n");
	}

	# ��ɸ(��)�����
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
# ��ĥ�ǡ��������󥿡�����
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
		# ����
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempIslandCounterPage(0);
		return;
	} else {
		# �ѥ����
		if(!checkPassword($island, $HdefaultPassword) && !checkSpecialPassword($HdefaultPassword)) {
			# �ѥ���ɥ����å�
			# �ü�ѥ����
			# password�ְ㤤
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
			# �����󥿡�����(�ꥻ�å�)
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
			# �����󥿡��õ�
			my $n = @HnavyName;
			my(@navy) = ((0)x$n);
			my(@subExt) = ($island->{'birthday'}, (0)x12); # 0��12
			$island->{'subSink'} = \@navy;
			$island->{'subSinkself'} = \@navy;
			$island->{'subExt'} = \@subExt;
		} elsif($HicounterMode == 4) {
			# ���祫���󥿡�����(�ꥻ�å�)
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
			# ���祫���󥿡��õ�
			my $n = @HnavyName;
			my(@navy) = ((0)x$n);
			my(@subExt) = ($island->{'birthday'}, (0)x12); # 0��12
			foreach ($HbfieldNumber..$islandNumber) {
				my($island) = $Hislands[$_];
				$island->{'subSink'} = \@navy;
				$island->{'subSinkself'} = \@navy;
				$island->{'subExt'} = \@subExt;
			}
		}
		writeIslandsFile();
	}
	# ����
	unlock();
	# �ƥ�ץ졼�Ƚ���
	tempIslandCounterPage(1);
}

# ��ĥ�ǡ��� �����󥿡�����ڡ���
sub tempIslandCounterPage() {
	my($mode) = @_;

	# �����ץ��2
	my $HtempBack2 = (checkSpecialPassword($HdefaultPassword)) ? "${HtagBig_}<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">���ƥʥ󥹤�</A> <small><A HREF=\"$HthisFile\">�ȥåפ����</A></small>${H_tagBig}" : $HtempBack;
	$HislandList = getIslandList($HcurrentID, 1);

	out(<<END);
<DIV align='center'>$HtempBack2</DIV><BR>
<DIV ID='islandInfo'>
<H1>��ĥ�ǡ��� �����󥿡�����</H1>
<FORM action="$HthisFile" method="POST">
<B>�����󥿡������ꤹ��${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}�����򤷤Ʋ�����-
$HislandList
</SELECT><BR><BR>
�ѥ����:<INPUT TYPE="password" NAME="ICounter" VALUE="$HdefaultPassword" MAXLENGTH=32 class=f>
<INPUT TYPE="submit" VALUE="������" NAME="IslandChoice"><BR>
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
<H1 style='display:inline'>������${HislandTurn}���� $HtagName_$name$H_tagName</H1>
END
	islandData(); # ��ĥ�ǡ���
	islandInfoSub(1) if($HnavyName[0] ne ''); # ����DATA

	out(<<END) if(checkPassword($island, $HdefaultPassword));
</TD></TR><TR>
<TD><INPUT TYPE="submit" VALUE="���å�\nor�ꥻ�å�" NAME="SetButton"></TD>
<TD>�ޤ����åȤ��Ƥ��ʤ����ϡ��֥�����$next�����ߡפΥǡ�����(�����󥿡�)���ɲä���ޤ���<BR>
���Ǥ˥��åȤ��Ƥ����硢�����󥿡������������ޤ���
</TD>
</TR><TR>
<TD align='center'><INPUT TYPE="submit" VALUE="�õ�" NAME="DelButton"></TD>
<TD>�֥�������������ߡפΥǡ�����(�����󥿡�)���õ��ޤ���<BR>�����󥿡��Ͻ��������ޤ���</TD>
</TR>
<TR><TD class='M' colspan=2>
�����٥ܥ���򲡤��ȥ����󥿡��򸵤��᤹���ȤϤǤ��ޤ���Τ���դ��Ƥ���������<BR>
����ȯ�������饫����Ȥ���Ƥ���ǡ����ϡ��ץ쥤�䡼�ˤ��ѹ��Ǥ��ޤ���<BR>
�� (��ȯ�����줿�Ф����$AfterName�ϡ������󥿡��򥻥åȤǤ��ޤ���)
</TD></TR>
END
	out(<<END) if(checkSpecialPassword($HdefaultPassword));
<TR><TD colspan=2>
<INPUT TYPE="submit" VALUE="��${AfterName}���å�or�ꥻ�å�" NAME="AllSetButton">
<INPUT TYPE="submit" VALUE="��${AfterName}�õ�" NAME="AllDelButton">
<BR>����$AfterName�������Υܥ���ϡ�������򤷤Ƥ���$AfterName�˴ط��ʤ�ư��ޤ���<BR>
�� (���Хȥ�ե�����ɤ�������٤Ƥ�$AfterName�������ꤷ�ޤ���)
</TD></TR>
END
	out("</TABLE></FORM></DIV>");
}

#----------------------------------------------------------------------
# ����ޥå�
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMapMain {
	my($mode) = @_;
	# ����
	unlock();

	if($mode <= 1) {
		# id�������ֹ�����
		$HcurrentNumber = $HidToNumber{$HcurrentID};

		# �ʤ��������礬�ʤ����
		if($HcurrentNumber eq '') {
			tempProblem();
			return;
		}
	} else {
		$HcurrentID = 0;
	}

	# �ޥå�ɽ��
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
		StyElm.style.marginLeft = (mapxArray[x] - 5) * $HwChipSize*2 - 120; // ��¦
//		StyElm.style.marginLeft = -10; // ��¦
	} else {
		StyElm.style.marginLeft = (mapxArray[x] + 3) * $HwChipSize*2; // ��¦
//		StyElm.style.marginLeft = $HislandSizeX*$HoceanSizeX * $HwChipSize*2 - 120; // ��¦
	}
	if(mapyArray[y] + 1 == $HislandSizeY*$HoceanSizeY) {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY + 0.5) * $HwChipSize*2 + 10; // ��¦
	} else if(mapyArray[y] + 1 > $HislandSizeY*$HoceanSizeY / 2) {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY - 2) * $HwChipSize*2 + 30; // ��¦
	} else {
		StyElm.style.marginTop = (mapyArray[y] - $HislandSizeY*$HoceanSizeY - 1) * $HwChipSize*2 + 30; // ��¦
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
      document.getElementById('toggleBtn').firstChild.nodeValue='�ܺ�ɽ��';
      obj.style.display='none';
    } else {
      document.getElementById('toggleBtn').firstChild.nodeValue='�ܺ���ɽ��';
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
// ������ޡ����󥰲�
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

// �ޡ����󥰲��
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
//		land += '�ڴ����ͤ��������';
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
<INPUT TYPE="checkbox" NAME="REN">������³����
<TABLE BORDER><TR><TD>
</FORM>
END

	# ��ɸ(��)�����
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
			# �����ֹ�ʤ��ֹ�����
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}

		foreach $x (@x) {
			$point = "($x, $y)";

			my($id, $s);
			if ($id = $HoceanMap[$x][$y]) {
				# ��
				$image = ($id == $HcurrentID) ? $HoceanImage[1] : $HoceanImage[2]; # ��ʬ���� or �դĤ�����
				$alt = islandName($Hislands[$HidToNumber{$id}]);
				$alt =~ s/<[^<]*>//g;
				if($Hislands[$HidToNumber{$id}]->{'field'}) {
					$image = $HoceanImage[3] if($id != $HcurrentID);
					$alt .= '��BattleField��';
				} elsif($Hislands[$HidToNumber{$id}]->{'predelete'}) {
					$image = $HoceanImage[4] if($id != $HcurrentID);
					$alt .= '�ڴ����ͤ��������';
				}
				out(qq#<A onClick="check('$id', $x, $y)" #);
				$s = " id='$id'";
			} else {
				# ̤�Τγ���
				$image = $HoceanImage[0];
				$alt = '';

				out(qq#<A onClick="check('0', $x, $y)" #);
				$s = "";
			}

			# JavaScript�����Ѥ���ɽ��
			out(qq#onMouseOver="sv($x,$y,'$alt','$id');" onMouseOut="scls();">#);
			out("<IMG SRC=\"$image\" TITLE=\"$point $alt\" TITLE=\"$point $alt\" width=${\($HchipSize*2)} height=${\($HchipSize*2)} BORDER=0${s}>");
			out("</A>");
		}

		if($y % 2) {
			# ������ܤʤ��ֹ�����
			out("<IMG SRC=\"space${v1}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space${v0}.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		} else {
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
			out("<IMG SRC=\"space.gif\" width=$HchipSize height=${\($HchipSize*2)}>");
		}
		# ���Ԥ����
		out("</NOBR><BR>\n");
	}
	# ��ɸ(��)�����
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
				out("<a href='javascript: displayWorld();' id='toggleBtn'>�ܺ�ɽ��</a>");
			} else {
				out("�ܺ�ɽ��");
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
	# �Ϸ����Ϸ��ͤ����
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
	# ��ɸ(��)�����
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
						# �Ԥˤ�����Ĵ��
						$sx-- if(!($sy % 2) && ($y % 2));
						$sx = $correctX[$sx + $#an];
						$sy = $correctY[$sy + $#an];
						# �ϰϳ��ξ��
						next if(($sx < 0) || ($sy < 0));
						$HviewJam[$sx][$sy] = 1;
					}
				}
			}
		}
	}
	# ���Ϸ�����Ӳ��Ԥ����
	foreach $j (0..$#y) {
		$y = $y[$j];
		$v0 = substr($y, -1);
		$v1 = substr($y, -2, 1);
		$v2 = substr($y, -3, 1);

		if($y % 2) {
			out("<IMG SRC=\"space.gif\" width=$HwChipSize height=${\($HwChipSize*2)}$alpha>");
		} else {
			# �����ֹ�ʤ��ֹ�����
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

		# ���Ϸ������
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
			# ������ܤʤ��ֹ�����
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
	# ��ɸ(��)�����
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
		# ����
		$image = $HlandImage[$l][$lv];
		if($lv == 2) {
			$image = $HjammingWasteImage if($HjammingLand == 2);
			$alpha .= " STYLE=\"filter: Alpha(opacity=50);\"" if(!$HjammingLand);
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$image = $HlandImage[$l];
	} elsif($l == $HlandForest) {
		# ��
		$image = $HlandImage[$l];
	} elsif($l == $HlandTown) {
		# �ԻԷ�
		my($n);
		foreach (reverse(0..$#HlandTownValue)) {
			if($HlandTownValue[$_] <= $lv) {
				$image = $HlandTownImage[$_];
				last;
			}
		}
	} elsif($l == $HlandFarm) {
		# ����
		$image = $HlandImage[$l];
	} elsif($l == $HlandFactory) {
		# ����
		$image = $HlandImage[$l];
	} elsif($l == $HlandBase) {
		if(!$mode) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$image = $HlandImage[$HlandForest];
		} else {
			# �ߥ��������
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandSbase) {
		# �������
		if(!$mode) {
			# �Ѹ��Ԥξ��ϳ��Τդ�
			$image = $HlandImage[$HlandSea][0];
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		if(!$mode) {
			if($HdBaseHide) {
				# �Ѹ��Ԥξ��Ͽ��Τդ�
				$image = $HlandImage[$HlandForest];
			} else {
				# �Ѹ��Ԥξ����ѵ�������
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
		# ������
		$image = $HlandImage[$l];
	} elsif($l == $HlandSeaMine) {
		# ����
		if(!$mode) {
			# �Ѹ��Ԥξ��ϳ��Τդ�
			$image = $HlandImage[$HlandSea][0];
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		if(!$mode) {
			if($HdBaseHide) {
				# �Ѹ��Ԥξ��Ͽ��Τդ�
				$image = $HlandImage[$HlandForest];
			} else {
				# �Ѹ��Ԥξ����ɱһ��ߤΤդ�
				$image = $HlandImage[$HlandDefence][0];
			}
		} else {
			$image = $HlandImage[$l];
		}
	} elsif($l == $HlandOil) {
		# ��������
		$image = $HlandImage[$l];
	} elsif($l == $HlandMountain) {
		# ��
		my $mlv = ($lv > 0) ? 1 : 0;
		$image = $HlandImage[$l][$mlv];
	} elsif($l == $HlandCore) {
		# ����
		my($lFlag, $lLv) = (int($lv / 10000), ($lv % 10000));
		if(!$mode) {
			if($HcoreHide) {
				# �Ѹ��Ԥξ��
				if(!$lFlag) { # ���Τդ�
					$image = $HlandImage[$HlandForest];
				} else { # ���Τդ�
					$image = $HlandImage[$HlandSea][0];
				}
			} else {
				# �Ѹ��Ԥξ����ѵ�������
				$image = $HlandImage[$l][$lFlag];
			}
		} else {
			$image = $HlandImage[$l][$lFlag];
		}
	} elsif($l == $HlandMonument) {
		# ��ǰ��
		$image = $HmonumentImage[$lv];
	} elsif($l == $HlandComplex) {
		# ʣ���Ϸ�
		my($cTmp, $cKind, $cTurn, $cFood, $cMoney) = landUnpack($lv);
		$image = $HcomplexImage[$cKind];
	} elsif($l == $HlandMonster) {
		# ����
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		$image = $HmonsterImage[$kind];
		# �Ų��桩
		$image = $HmonsterImage2[$kind] if ($flag & 1);
		# �����桩
		$image = $HmonsterImageUnderSea if ($flag & 2);
	} elsif($l == $HlandHugeMonster) {
		# �������
		my($id, $hflag, $sea, $exp, $flag, $kind, $hp) = monsterUnpack($lv);
		if(($flag & 1) && ($flag & 2)) {
			# ���ǹŲ�
			$image = $HhugeMonsterImage4[$kind][$hflag];
		} elsif($flag & 1) {
			# Φ�ǹŲ�
			$image = $HhugeMonsterImage2[$kind][$hflag];
		} elsif($flag & 2) {
			# ��
			$image = $HhugeMonsterImage3[$kind][$hflag];
		} else {
			# Φ
			$image = $HhugeMonsterImage[$kind][$hflag];
		}
	} elsif($l == $HlandNavy) {
		# ����
		my($id, $tmp, $stat, $sea, $exp, $flag, $no, $kind, $wait, $hp, $goalx, $goaly) = navyUnpack($lv, $lv2);
		$image = $HnavyImage[$kind];
		if ($flag == 1) {
			# �ĳ���
			$image = $HnavyImageZ;
		} else {
			if ($flag & 2) {
				# �����桩
				$image = $HnavyImage2[$kind];
			}
		}
	}

	out("<IMG SRC=\"$image\" width=${\($HwChipSize*2)} height=${\($HwChipSize*2)} BORDER=0$alpha>");

}

1;
