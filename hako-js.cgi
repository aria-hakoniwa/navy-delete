# The Return of Neptune: http://no-one.s53.xrea.com/
# ����JS���Ѥ˲���
#----------------------------------------------------------------------
# �ʣ��֣�������ץ��� -ver1.11-
# ���Ѿ�������ˡ���ϡ����۸��Ǥ���ǧ��������
# ��°��js-readme.txt�⤪�ɤ߲�������
# ���äݡ���http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �����ͣ��Хǡ�������
#----------------------------------------------------------------------
sub landStringFlash {
	my($mode) = @_;
	my($island);
	$island = $Hislands[$HcurrentNumber];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($map) = $island->{'map'};
	my($l, $lv);
	my($code) = "";
	my($befor) = "a";
	my($Count) = 0;
	my($Comp) = "";
	my($ret) = "";

	# ���Ϸ������
	my($x, $y);
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$code = landFlashData($l, $lv, $mode);

			if ($code eq $befor) {
				$Count++;
			} else {
				$Comp .= $befor;
				if( $Count != 0){
					$Comp .= ($Count - 1);
				}
				$Count = 0;
				$befor = $code;
			}
		}
 	}
	if($befor ne "a"){
		$Comp .= $befor;
		if( $Count != 0){
			$Comp .= ($Count - 1);
		}
	}
	$Comp .= "\@";
	$Comp = substr($Comp,1);

	# ���Ϸ������
	my($Compjs) = "";
	foreach $y (@{$map->{'y'}}) {
		foreach $x (@{$map->{'x'}}) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			$code = landFlashData($l, $lv, $mode);
			$Compjs .= $code;
		}
 	}

	out(<<END);
<FORM>
�����ͣ��к����ġ����ѥǡ���(FLASH��)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="3">$Comp</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/flash/hako-map.html" target="_blank">
�����ͣ��к����ġ���(FLASH��)�򥪥�饤��ǵ�ư</a><P>
�����ͣ��к����ġ����ѥǡ���(Java������ץ���)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="4">$Compjs</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/javascript/map.html" target="_blank">
�����ͣ��к����ġ���(Java������ץ���)�򥪥�饤��ǵ�ư</a><BR><BR><BR>
<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">
�����ͣ��к����ġ���(JAVA��FLASH��)���������ɤ���</a><p>
</FORM>
END

}

sub landFlashData {
	my($l, $lv, $mode) = @_;
	my($flash_data);

	if($l == $HlandSea) {
		# ����
		if($lv == 1) {
			$flash_data = "o";
		} else {
			# ��
			$flash_data = "a";
		}
	} elsif($l == $HlandWaste) {
		# ����
		if($lv == 1) {
			# ������
			$flash_data = "n";
		} else {
			$flash_data = "b";
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$flash_data = "c";
	} elsif($l == $HlandForest) {
		# ��
		$flash_data = "g";
	} elsif($l == $HlandTown) {
		if($lv < 30) {
			# ¼
			$flash_data = "d";
		} elsif($lv < 100) {
			# Į
			$flash_data = "e";
		} else {
			# �Ի�
			$flash_data = "f";
		}
	} elsif($l == $HlandFarm) {
		# ����
		$flash_data = "h";
	} elsif($l == $HlandFactory) {
		# ����
		$flash_data = "i";
	} elsif($l == $HlandBase) {
		if($mode == 0) {
		# �ߥ�������� �Ͽ��ˤʤ�
			$flash_data = "g";
		}else{
			$flash_data = "j";
		}
	} elsif($l == $HlandDefence) {
		if($mode == 0 && $HdBaseHide) {
			# �ɱһ��ߤϿ��ˤʤ�
			$flash_data = "g";
		}else{
			# �ɱһ���
			$flash_data = "k";
		}
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		$flash_data = "k";
	} elsif($l == $HlandOil) {
		# ��������
		$flash_data = "q";
	} elsif($l == $HlandMountain) {
		# ��
		if($lv > 0) {
			$flash_data = "p"; # �η���
		} else {
			$flash_data = "l";
		}
	} elsif($l == $HlandMonument) {
		# ��ǰ��
		$flash_data = "r";
	} elsif($l == $HlandMonster) {
		# ����
		$flash_data = "s";
	} else {
		# ����¾
		$flash_data = "b";
	}
	return $flash_data;
}
#----------------------------------------------------------------------
# ����js�ե��������
#----------------------------------------------------------------------
sub makeJS {
	my($mode) = @_;

	my($i, $k, $Msg);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$k = $HcomList[$i];
		$Msg .= "msg[$k] = \"$HcomMsgs[$k]\";\n"
	}

	my($src);
	$src = <<"END";
function init(){
	for(i = 0; i < command.length ;i++) {
		for(s = 0; s < $com_count ;s++) {
			var comlist2 = comlist[s];
			for(j = 0; j < comlist2.length ; j++) {
				if(command[i][0] == comlist2[j][0]) {
					g[i] = [comlist2[j][1], comlist2[j][3]];
				}
			}
		}
	}
	outp();
	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs1'><nobr><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B></nobr><br><br>"+str+"<br><nobr><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B></nobr></TD></TR></TABLE>";
	disp(str, "#ccffcc");

	xmlhttp = new_http();
	if(document.layers) {
		document.captureEvents(Event.MOUSEMOVE | Event.MOUSEUP);
	}
	document.onmouseup   = Mup;
	document.onmousemove = Mmove;
	document.onkeydown = Kdown;
	document.ch_numForm.AMOUNT.options.length = 100;
	for(i=0;i<document.ch_numForm.AMOUNT.options.length;i++){
		document.ch_numForm.AMOUNT.options[i].value = i;
		document.ch_numForm.AMOUNT.options[i].text  = i;
	}
	document.myForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;
	document.myForm.CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}.disabled = true;
	ns(0);

	check_menu();
}
function cominput(theForm, x, k, z) {
	a = theForm.NUMBER.options[theForm.NUMBER.selectedIndex].value;
	b = theForm.COMMAND.options[theForm.COMMAND.selectedIndex].value;
	c = theForm.POINTX.options[theForm.POINTX.selectedIndex].value;
	d = theForm.POINTY.options[theForm.POINTY.selectedIndex].value;
	e = theForm.AMOUNT.options[theForm.AMOUNT.selectedIndex].value;
	f = theForm.TARGETID.options[theForm.TARGETID.selectedIndex].value;
	h = theForm.TARGETID2.options[theForm.TARGETID2.selectedIndex].value;
	var newNs = a;
	k1 = g.clone();
	k2 = g.clone();
	tmpcom2 = tmpcom1.clone();
	if (x == 1 || x == 2 || (6 <= x && x <= 11)){
		if(x == 6) {
			b = k;
		} else if(x == 7) {  // ������ư
			b = $HcomMoveTarget;
			e = k;
		} else if(x == 8) {  // �����ư
			b = $HcomNavyMove;
			h = k;
		} else if(x == 10) {  // �����ǿ�(������)
			b = $HcomCeasefire;
			f = k;
		} else if(x == 11) {  // �����۹�(�����˴�)
			b = $HcomDeWar;
			f = k;
		}
		if(x != 2) {
			for(i = $HcommandMax - 1; i > a; i--) {
				command[i] = command[i-1];
				g[i] = g[i-1];
			}
		}
		for(s = 0; s < $com_count ;s++) {
			var comlist2 = comlist[s];
			for(i = 0; i < comlist2.length; i++){
				if(comlist2[i][0] == b){
					g[a] = [comlist2[i][1], comlist2[i][3]];
					break;
				}
			}
		}
		command[a] = [b,c,d,e,f,h];
		newNs++;
		menuclose();
	}else if(x == 3){
		var num = (k) ? k-1 : a;
		for(i = Math.floor(num); i < ($HcommandMax - 1); i++) {
			command[i] = command[i + 1];
			g[i] = g[i+1];
		}
		command[$HcommandMax-1] = [$HcomDoNothing,0,0,0,0];
		g[$HcommandMax-1] = ['��ⷫ��', '1'];
	}else if(x == 4){
		i = Math.floor(a)
		if (i == 0){ return true; }
		tmpcom1[i] = command[i];tmpcom2[i] = command[i - 1];
		command[i] = tmpcom2[i];command[i-1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i - 1];
		g[i] = k2[i];g[i-1] = k1[i];
		newNs = i-1;
	}else if(x == 5){
		i = Math.floor(a)
		if (i == $HcommandMax-1){ return true; }
		tmpcom1[i] = command[i];tmpcom2[i] = command[i + 1];
		command[i] = tmpcom2[i];command[i+1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i + 1];
		g[i] = k2[i];g[i+1] = k1[i];
		newNs = i+1;
	}else if(x == 12){
		// ��ư
		var ctmp = command[k];
		var gtmp = g[k];
		if(z > k) {
			// �夫�鲼��
			for(i = k; i < z-1; i++) {
				command[i] = command[i+1];
				g[i] = g[i+1];
			}
		} else {
			// ��������
			for(i = k; i > z; i--) {
				command[i] = command[i-1];
				g[i] = g[i-1];
			}
		}
		command[i] = ctmp;
		g[i] = gtmp;
	}else if(x == 13){
		command[a][3] = k;
	}
	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs2'><nobr><B>�ݡݡݡݡ�̤�����ݡݡݡݡ�</B></nobr><br><br>"+str+"<br><nobr><B>�ݡݡݡݡ�̤�����ݡݡݡݡ�</B></nobr></TD></TR></TABLE>";
	disp(str, "white");
	outp();
	theForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
	theForm.CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
	ns(newNs);
	return true;
}
function plchg(){
	strn1 = "";
	strturn = "";
	turn = $HislandTurn + 1;
	cflag = $Hislands[$HcurrentNumber]->{'itemAbility'}[6];
	if(cflag == 0) { cflag = 1; }
	flagST = 0;
	count = 0;
	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		if(g[i][1] == 0) {
			kind = '$HtagComName2_' + g[i][0] + '$H_tagComName';
		} else {
			kind = '$HtagComName1_' + g[i][0] + '$H_tagComName';
		}
		carg = c[3];
		if(carg == 0) { carg = 1; }
		if( (c[0] == $HcomFarm) ||
			(c[0] == $HcomFactory) ||
			((c[0] == $HcomDbase) && $HdurableDef) ||
			(($HcomComplex[0] <= c[0]) && (c[0] <= $HcomComplex[$#HcomplexComName])) ||
			(c[0] == $HcomMountain) ||
			(c[0] == $HcomCore) ||
			(c[0] == $HcomPropaganda)
			) {
			count += g[i][1] * carg;
		} else if((c[0] == $HcomSendMonsterST) || (($HcomMissile[0] <= c[0]) && (c[0] <= $HcomMissile[$#HmissileName]) && stcheck[c[0]-$HcomMissile[0]])) {
			if(flagST > 0) {
				count++;
				flagST = 0;
			} else {
				flagST = 1;
				if(i + 1 < $HcommandMax) {
					cc = command[i+1];
					if((cc[0] == $HcomSendMonsterST) || (($HcomMissile[0] <= cc[0]) && (cc[0] <= $HcomMissile[$#HmissileName]) && stcheck[cc[0]-$HcomMissile[0]])) {
						count++;
						flagST = 0;
					} else {
						count += g[i][1];
					}
				} else {
					count += g[i][1];
				}
			}
		} else if(flagST > 0) {
			if(i + 1 < $HcommandMax) {
				cc = command[i+1];
				if((cc[0] == $HcomSendMonsterST) || (($HcomMissile[0] <= cc[0]) && (cc[0] <= $HcomMissile[$#HmissileName]) && stcheck[cc[0]-$HcomMissile[0]])) {
					count++;
					flagST = 0;
				} else {
					count += g[i][1];
				}
			} else {
				count += g[i][1];
			}
		} else {
			count += g[i][1];
		}
		if(cflag <= count) {
			strturn = '$HtagComName1_' + turn + '$H_tagComName';
			turn += Math.floor(count/cflag);
			count %= cflag;
		} else {
			strturn = '$HtagComName2_' + turn + '$H_tagComName';
		}
		if(g[i][0] == 0) {
			tmpnum = '';
			if(i < 9){ tmpnum = '0'; }
			strn1 +=
				'<div id="com_' + i + '" ' + 'onmouseover="mc_over(' + i + ');return false;">'
				 + '<A STYLE="text-decoration:none;color:000000" HREF="JavaScript:void(0);" onClick="ns(' + i + ')" '
				 + 'onmousedown="return comListMove(' + i + ');" ' + 'ondblclick="chNum(' + c[3] + ');return false;" '
				 + '><NOBR>$HtagNumber_' + tmpnum + (i + 1) + '$H_tagNumber<FONT SIZE=-1>$HnormalColor_(' + strturn + ')��'
				 + '$HtagComName2_���Υ��ޥ�ɤϻȤ��ʤ��ʤ�ޤ���$H_tagComName$H_normalColor</FONT></NOBR></A></div>\\n';
			continue;
		}
		x = c[1];
		y = c[2];
		point = '$HtagName_(' + x + "," + y + ')$H_tagName';
		if(islname[c[4]] =='') {
			tgt = '$HtagName2_̵��${AfterName}$H_tagName2';
		} else {
			tgt = '$HtagName_' + islname[c[4]] + '$H_tagName';
		}

		if(c[0] == $HcomDoNothing || c[0] == $HcomGiveup || c[0] == $HcomPrepare3){ // ��ⷫ�ꡢ�������������Ϥʤ餷
			strn2 = kind;


//		}else if($HcomMissile[0] <= c[0] && c[0] <= $HcomMissile[$#HmissileName]) { // �ߥ�����ȯ�� ����ȯ�ʤ��ѹ�
		}else if($HcomNavy2[0] <= c[0] && c[0] <= $HcomNavy2[3]) { // ����ȯ��
//			if(c[3] == 0){
//				arg = '($HtagName_̵����$H_tagName)';
//			} else {
//				arg = '($HtagName_' + c[3] + 'ȯ$H_tagName)';
//			}
//			strn2 = tgt + point + '��' + kind + arg;
			if(c[3] <= 1){
				arg = '�裱';
			} else if(c[3] == 2){
				arg = '�裲';
			} else if(c[3] == 3){
				arg = '�裳';
			} else{
				arg = '�裴';
                      }
			arg = '($HtagName_' + arg +'����$H_tagName)';
			strn2 = tgt + point + '��' + kind + arg;
		}else if(c[0] == $HcomAmity) { // ͧ���� ���ꡦ���
			if(c[4] != d_ID) {
				strn2 = tgt + '��' + kind;
			} else {
				strn2 = '<B>���٤Ƥ�${AfterName}</B>��' + kind;
			}
		}else if(c[0] == $HcomAlly) { // Ʊ�� ������æ��
			strn2 = tgt + '��' + kind;
		}else if(c[0] == $HcomDeWar || c[0] == $HcomCeasefire) { // �����۹�����
			strn2 = tgt + '��' + kind;
		}else if(c[0] == $HcomSendMonster || // �����ɸ�
			c[0] == $HcomSendMonsterST){
			arg = c[3];
			arg2 = 0;
			if(arg >= 50 && ($HsendHugeMonsterNumber >= 0) && $HhugeMonsterAppear) {
				arg2 = 1;
				arg -= 50;
				if(arg > $HsendHugeMonsterNumber) {
					arg = $HsendHugeMonsterNumber;
				}
			} else if(arg > $HsendMonsterNumber) {
				arg = $HsendMonsterNumber;
			}
			if(arg2 == 1) {
				arg = '($HtagName_' + hugeMonsterName[arg] +'$H_tagName)';
			} else {
				arg = '($HtagName_' + monsterName[arg] +'$H_tagName)';
			}
			strn2 = tgt + '��' + kind + arg;
		}else if($HcomNavy[0] <= c[0] && c[0] <= $HcomNavy[$#HnavyName]) { // ������¤
			if(c[3] < 1){
				c[3] = 1;
			} else if (c[3] > 4){
				c[3] = 4;
			}
			arg = '';
			if(portflag[c[0]-$HcomNavy[0]] != 1) {
				arg = '($HtagName_' + ofName[c[3]-1] +'����$H_tagName)';
			}
			if($HnavyBuildFlag){
				strn2 = point + '��' + kind + arg;
			} else {
				strn2 = kind + arg;
			}
			if(portflag[c[0]-$HcomNavy[0]] != 1) {
				var flag = 0;
				if(navyPort == 0) {
					flag = 0;
				} else if($HnavyBuildFlag) {
					if(mapdata[y][x] != 0){
						flag = 0;
					} else {
						flag = searchNavyPort(x, y, 7);
						if($HmaxComPortLevel) {
							if(navybuild[flag - 1] >= c[0] - $HcomNavy[0]) {
								flag = 1;
							} else {
								flag = 0;
							}
						}
					}
				} else if($HmaxComPortLevel) {
					flag = searchNavyPort(x, y, 0);
					if(navybuild[flag - 1] >= c[0] - $HcomNavy[0]) {
						flag = 1;
					} else {
						flag = 0;
					}
				} else {
					flag = navyPort;
				}
				if(flag == 0){ strn2 = '${HtagDisaster_}��${H_tagDisaster}' + strn2; }
			} else if(mapdata[y][x] != -1) {
				strn2 = '${HtagDisaster_}��${H_tagDisaster}' + strn2;
			}
		}else if(c[0] == $HcomNavyMove) { // �����ư
			if(c[3] < 1){
				c[3] = 1;
			} else if (c[3] > 4){
				c[3] = 4;
			}
			if(islname[c[5]] =='') {
				tgt2 = '$HtagName2_̵��${AfterName}$H_tagName2';
			} else {
				tgt2 = '$HtagName_' + islname[c[5]] + '$H_tagName';
			}

			if(g[i][1] == 0) {
				arg = '$HtagComName2_' + ofName[c[3]-1];
			} else {
				arg = '$HtagComName1_' + ofName[c[3]-1];
			}
			if(c[5] == d_ID) {
				strn2 = tgt + '����' + arg + '���ⵢ��$H_tagComName';
			} else if(c[4] == d_ID) {
				strn2 = tgt2 + '��' + arg + '�����ɸ�$H_tagComName';
			} else {
				strn2 = tgt + '����' + tgt2 + '��' + arg + '�����ɸ�$H_tagComName';
			}
		}else if(c[0] == $HcomNavyForm) { // ��������
			if(mapdata[y][x] != $HlandNavy) { point = '${HtagDisaster_}��${H_tagDisaster}' + point; }
			if(c[3] < 1){
				c[3] = 1;
			} else if (c[3] > 4){
				c[3] = 4;
			}
			if(g[i][1] == 0) {
				arg = '$HtagComName2_' + ofName[c[3]-1] +'$H_tagComName';
			} else {
				arg = '$HtagComName1_' + ofName[c[3]-1] +'$H_tagComName';
			}
			strn2 = point + '��'  + arg + kind;
		}else if(c[0] == $HcomSell || //����͢�С�����͢��
			c[0] == $HcomBuy){
			if(c[3] == 0){ c[3] = 1; }
			if(c[0] == $HcomBuy) {
//				arg = '$HtagName_' + c[3] * $HcomCost[$HcomBuy] + '$HunitMoney$H_tagName ($HtagName_' + c[3] * $HcomCost[$HcomBuy] * 10 + '${HunitFood}����$H_tagName)';
				arg = '$HtagName_' + c[3] * $HcomCost[$HcomBuy] + '$HunitMoney$H_tagName';
			} else {
//				arg = '$HtagName_' + c[3] * (- ($HcomCost[$HcomSell])) + '$HunitFood$H_tagName ($HtagName_' + c[3] * (- ($HcomCost[$HcomSell])) / 10 + '${HunitMoney}����$H_tagName)';
				arg = '$HtagName_' + c[3] * (- ($HcomCost[$HcomSell])) + '$HunitFood$H_tagName';
			}
			strn2 = kind + arg;
		}else if((c[0] == $HcomPropaganda) || 
                         (c[0] == $Hcomshikin)) { // Ͷ�׳�ư����ⷫ��
			if(c[3] == 0){
				strn2 = kind;
			} else {
				arg = '($HtagName_' + c[3] + '��$H_tagName)';
				strn2 = kind + arg;
			}
		}else if(c[0] == $HcomMoney){ // �����
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * $HcomCost[$HcomMoney];
			arg = '($HtagName_' + arg + '$HunitMoney$H_tagName)';
			strn2 = tgt + '��' + kind + arg;
		}else if(c[0] == $HcomFood){ // �������
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * (- ($HcomCost[$HcomFood]));
			arg = '($HtagName_' + arg + '$HunitFood$H_tagName)';
			strn2 = tgt + '��' + kind + arg;
		}else if(c[0] == $HcomDestroy || c[0] == $HcomDestroy2) { // �����®����
			if(c[3] == 0){
				strn2 = point + '��' + kind;
			} else {
				arg = c[3] * $HcomCost[$HcomDestroy];
				arg = '(ͽ\��$HtagName_' + arg + '$HunitMoney$H_tagName)';
				strn2 = point + '��' + kind + arg;
			}
		}else if(c[0] == $HcomDbase) { // �ɱһ���
			if(c[3] == 0 || $HdurableDef == 0){
				if($HdurableDef == 0 && mapdata[y][x] == $HlandDefence) {
					strn2 = point + '��' + kind + '(${HtagName_}����${H_tagName})';
				} else {
					strn2 = point + '��' + kind;
				}
			}else if(c[3] == $HdefExplosion && mapdata[y][x] == $HlandDefence){
				strn2 = point + '��' + kind + '(${HtagName_}����${H_tagName})';
			}else{
				arg = '($HtagName_' + c[3] + '��$H_tagName)';
				strn2 = point + '��' + kind + arg;
			}
		}else if(c[0] == $HcomFarm || // ���졢���졢�η�������
			c[0] == $HcomFastFarm ||
			c[0] == $HcomFactory ||
			c[0] == $HcomFastFactory ||
			c[0] == $HcomMountain ||
			c[0] == $HcomCore) {
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '��$H_tagName)';
				strn2 = point + '��' + kind + arg;
			}else{
				strn2 = point + '��' + kind;
			}
		}else if($HcomComplex[0] <= c[0] && c[0] <= $HcomComplex[$#HcomplexComName]) { // ʣ���Ϸ�����
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '��$H_tagName)';
				strn2 = point + '��' + kind + arg;
			}else{
				strn2 = point + '��' + kind;
			}
		}else if(c[0] == $HcomSeaMine) { // ����
			if(mapdata[y][x] == $HlandSeaMine){
				if(g[i][1] == 0) {
					kind = '$HtagComName2_' + '�������' + '$H_tagComName';
				} else {
					kind = '$HtagComName1_' + '�������' + '$H_tagComName';
				}
			} else {
				if(c[3] == 0){ c[3] = 1; }
				if(c[3] > $HmineDamageMax){ c[3] = $HmineDamageMax; }
				arg = '(�˲���:$HtagName_' + c[3] + '$H_tagName)';
				kind = kind + arg;
			}
			strn2 = point + '��' + kind;
		}else if((c[0] == $Hcomgoalsetpre) || //��Ū�ϻ���
                         (c[0] == $Hcomgoalset)){
			strn2 = tgt + point + '��' + kind;

		}else if(c[0] == $HcomMoveTarget) { // ��ư���
			if(c[4] == d_ID && (mapdata[y][x] != $HlandNavy) && (mapdata[y][x] <= 100)) { tgt = '${HtagDisaster_}��${H_tagDisaster}' + tgt; }
			while(c[3] > 19) { c[3] = c[3] - 19; }
			if(c[3] == 1) {
				direction = '����';
			} else if(c[3] == 2) {
				direction = '��';
			} else if(c[3] == 3) {
				direction = '����';
			} else if(c[3] == 4) {
				direction = '����';
			} else if(c[3] == 5) {
				direction = '��';
			} else if(c[3] == 6) {
				direction = '����';
			} else if((c[3] > 6) && (c[3] < 19)) {
				arg = c[3] - 6;
				direction = arg + '��';
			} else {
				c[3] = 0;
				direction= '�Ե�';
			}
			strn2 = tgt + point + '��' + kind + '($HtagName_' + direction + '$H_tagName)';
		}else if(c[0] == $HcomMoveMission) { // ��ư����
			arg = c[3] % 10;
			arg2 = (c[3] - arg) / 10;
			if(arg < 1){
				arg = 1;
			} else if (arg > 4){
				arg = 4;
			}
			if(arg2 > 0) {
				strn2 = ofName[arg - 1] + '������Ф���' + kind + '��$HtagName_���$H_tagName';
			} else {
				strn2 = ofName[arg - 1] + '������Ф�' + tgt + point + '�ؤ�' + kind;
			}
		}else if(c[0] == $HcomNavyTarget) { // ���ƹ���
			strn2 = tgt + point + '��' + kind;
		}else if(c[0] == $HcomMonument) { // ��ǰ���¤
			if($HuseBigMissile == 1 && mapdata[y][x] == $HlandMonument) {
				arg = '(' + tgt + '��$HtagName_ȯ��$H_tagName)';
			} else {
				if(c[3] >= $HmonumentNumber){ c[3] = $HmonumentNumber - 1; }
				arg = '($HtagName_' + monument[c[3]] + '$H_tagName)';
			}
			strn2 = point + '��' + kind + arg;

		}else if(c[0] == $Hcomremodel) { // �����
			if(c[3] == 0){
                               tmp = '����';
                        }else if(c[3] == 1){
                               tmp = '����';
                        }else if(c[3] == 2){
                               tmp = '�ɶ�';
                        }else{
                               tmp = '����';
                        }
			arg = '($HtagName_' + tmp + '$H_tagName)';
			strn2 = point + '��' + kind + arg;
		}else if(c[0] == $Hcomwork) { // ���ѥ�����Ÿ��
			if(c[3] == 0){
                               tmp = '����';
                        }else if(c[3] == 1){
                               tmp = '����';
                        }else if(c[3] == 2){
                               tmp = '�η�';
                        }else{
                               tmp = '����';
                        }
			arg = '($HtagName_' + tmp + '$H_tagName)';
			strn2 = tgt + point + '��' + kind + arg;
		}else if(c[0] == $HcomNavyDestroy) { // �����˴�
			strn2 = tgt + point + '��' + kind;
		}else if(c[0] == $HcomSellPort) { // ����ʧ����
			strn2 = tgt + point + '��' + kind;
		}else if(c[0] == $HcomBuyPort) { // �������
			strn2 = tgt + point + '��' + kind;
		}else {
			strn2 = point + '��' + kind;
		}
		tmpnum = '';
		if(i < 9){ tmpnum = '0'; }
		strn1 +=
			'<div id="com_' + i + '" ' + 'onmouseover="mc_over(' + i + ');return false;">'
			 + '<A STYLE="text-decoration:none;color:000000" HREF="JavaScript:void(0);" onClick="ns(' + i + ')" '
			 + 'onmousedown="return comListMove(' + i + ');" ' + 'ondblclick="chNum(' + c[3] + ');return false;" '
			 + '><NOBR>$HtagNumber_' + tmpnum + (i + 1) + '$H_tagNumber<FONT SIZE=-1>$HnormalColor_(' + strturn + ')��'
			 + strn2 + '$H_normalColor</FONT></NOBR></A></div>\\n';
	}
	return strn1;
}
function disp(str,bgclr){
	if(str==null)  str = "";

	if(document.getElementById || document.all){
		LayWrite('LINKMSG1', str);
		SetBG('plan', bgclr);
	} else if(document.layers) {
		lay = document.layers["PARENT_LINKMSG"].document.layers["LINKMSG1"];
		lay.document.open();
		lay.document.write("<font style='font-size:11pt'>"+str+"</font>");
		lay.document.close(); 
		SetBG("PARENT_LINKMSG", bgclr);
	}
}
function outp(){
	comary = "";

	for(k = 0; k < command.length; k++){
	comary = comary + command[k][0]
	+" "+command[k][1]
	+" "+command[k][2]
	+" "+command[k][3]
	+" "+command[k][4]
	+" "+command[k][5]
	+" ";
	}
	document.myForm.COMARY.value = comary;
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
	if(document.mark_form.mark.checked) {
		set_mark(x, y);
	} else {
		with (document.myForm) {
			myForm.POINTX.options[x].selected = true;
			myForm.POINTY.options[y].selected = true;
			with (myForm.TARGETID) {
				var i;
				for (i = 0; i < length; i++) {
					if (options[i].value == d_ID) {
						options[i].selected = true;
						break;
					}
				}
			}
		}
		document.allForm.POINTX.value = x;
		document.allForm.POINTY.value = y;
		menuclose();
		if(!(document.myForm.MENUOPEN.checked)) {
			if(document.myForm.MENUOPEN3.checked) {
				moveLAYER2("menu3",mx,my);
			} else if(document.myForm.MENUOPEN2.checked) {
				moveLAYER2("menu2",mx,my);
			} else {
				moveLAYER2("menu",mx,my);
			}
		}
	}
	return true;
}
function ns(x) {
	if (x == $HcommandMax){ return true; }
	document.myForm.NUMBER.options[x].selected = true;
	document.allForm.NUMBER.value = x;
	selCommand(x);
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
function SelectList(theForm){
	var u, selected_ok;
	c = ['${HcomNameColor2}', '${HcomNameColor1}'];
	if(!theForm){s = ''}
	else { s = theForm.menuList.options[theForm.menuList.selectedIndex].value; }
	if(s == ''){
		u = 0; selected_ok = 0;
		document.myForm.COMMAND.options.length = All_list;
		for (i=0; i<comlist.length; i++) {
			var command = comlist[i];
			for (a=0; a<command.length; a++) {
				comName = command[a][1] + "(" + command[a][2] + ")";
				document.myForm.COMMAND.options[u].value = command[a][0];
				document.myForm.COMMAND.options[u].text = comName;
				with(document.myForm.COMMAND.options[u].style) {color = c[command[a][3]];};
				if(command[a][0] == d_Kind){
					document.myForm.COMMAND.options[u].selected = true;
					selected_ok = 1;
				}
				u++;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	} else {
		var command = comlist[s];
		document.myForm.COMMAND.options.length = command.length;
		for (i=0; i<command.length; i++) {
			comName = command[i][1] + "(" + command[i][2] + ")";
			document.myForm.COMMAND.options[i].value = command[i][0];
			document.myForm.COMMAND.options[i].text = comName;
			with(document.myForm.COMMAND.options[i].style) {color = c[command[i][3]];};
			if(command[i][0] == d_Kind){
				document.myForm.COMMAND.options[i].selected = true;
				selected_ok = 1;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	}
}
function chkwindowsize(){ // ���δؿ��ǡ�������ɥ����礭����Ĵ�٤롣 320x365,372x464
// body.clientWidth�ϡ��ڡ������۸�ˤ��������Ǥ��ʤ��Τǡ��ؿ��ˤ���onload��˸ƤӽФ��Ƥޤ���
	if (document.all){
		wX = document.body.clientWidth; // ����
		wY = document.body.clientHeight; // �ļ�
	} else {
		wX = window.innerWidth;
		wY = window.innerHeight;
	}
// NN�ѡ�4.7��6��Ȥ��롣
}
function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		el = document.getElementById(layName);
		el.style.left = x;
		el.style.top  = y;
	} else if(document.layers){				//NN4
		msgLay.moveTo(x,y);
	} else if(document.all){				//IE4
		msgLay = document.all(layName).style;
		msgLay.pixelLeft = x;
		msgLay.pixelTop = y;
	}
}
function moveLAYER2(layName,x,y) {
	if(!(document.myForm.MENUOPEN2.checked)){
		winX = 170; winY = 270; //�ݥåץ��åץ�˥塼�β��ĤΥ�����
	} else {
		winX = 175; winY = 135; //�ݥåץ��åץ�˥塼�β��ĤΥ�����
	}
	chkwindowsize();
	if(x + winX*3/4 > wX) { cX = -20 - winX; } else { cX = 10; }
	if(y + winY/2 > wY) { cY = 30 - winY; } else if(y + winY > wY){ cY = 30 - winY/2; } else { cY = -30; }
	if(document.getElementById){		//NN6,IE5
		if(document.all){				//IE5
			if(event.clientX + winX*3/4 > wX) { cX = -20 - winX; } else { cX = 10; }
			if(event.clientY + winY/2 > wY) { cY = 30 - winY; } else if(event.clientY + winY > wY){ cY = 30 - winY/2; } else { cY = -30; }
			el = document.getElementById(layName);
			el.style.left= event.clientX + document.body.scrollLeft + cX;
			el.style.top= event.clientY + document.body.scrollTop + cY;
			el.style.display = "block";
			el.style.visibility ='visible';
		}else{
			el = document.getElementById(layName);
			el.style.left=x + cX;
			el.style.top=y + cY;
			el.style.display = "block";
			el.style.visibility ='visible';
		}
	} else if(document.layers){				//NN4
		msgLay = document.layers[layName];
		msgLay.moveTo(x + cX,y + cY);
		msgLay.visibility = "show";
	} else if(document.all){				//IE4
		msgLay = document.all(layName);
		msgLay.style.pixelLeft = x + cX;
		msgLay.style.pixelTop = y + cY;
		msgLay.style.display = "block";
		msgLay.style.visibility = "visible";
	}

}
function menuclose(){
//	moveLAYER("menu",-500,-500);
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
		mx = event.x + document.body.scrollLeft;
		my = event.y + document.body.scrollTop;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}
}
function LayWrite(layName, str) {
	if(document.getElementById){
		document.getElementById(layName).innerHTML = str;
	} else if(document.all){
		document.all(layName).innerHTML = str;
	} else if(document.layers){
		lay = document.layers[layName];
		lay.document.open();
		lay.document.write(str);
		lay.document.close();
	}
}
function SetBG(layName, bgclr) {
	if(document.getElementById) {
		document.getElementById(layName).style.backgroundColor = bgclr;
	} else if(document.all){
		document.all.layName.bgColor = bgclr;
	}
}
var oldNum=0;
function selCommand(num) {
	document.getElementById('com_' + oldNum).style.backgroundColor = '';
	document.getElementById('com_' + num).style.backgroundColor = '#FFFFAA';
	oldNum = num;
}
//* ���ޥ�� �ɥ�å����ɥ�å����ɲå�����ץ� */
var moveLay = new MoveFalse();
var newLnum = -2;
var Mcommand = false;
function Mup() {
	moveLay.up();
	moveLay = new MoveFalse();
}
function setBorder(num, color) {
	if(document.getElementById) {
		if(color.length == 4) {
			document.getElementById('com_'+ num).style.borderTop = ' 1px solid ' + color;
		} else {
			document.getElementById('com_'+ num).style.border = '0px';
		}
	}
}
function mc_out() {
	if(Mcommand && newLnum >= 0) {
		setBorder(newLnum, '');
		newLnum = -1;
	}
}
function mc_over(num) {
	if(Mcommand) {
		if(newLnum >= 0) {
			setBorder(newLnum, '');
		}
		newLnum = num;
		setBorder(newLnum, '#116');    // blue
	}
}
function comListMove(num) {
	moveLay = new MoveComList(num);
	return (document.layers) ? true : false;
}
function MoveFalse() {
	this.move = function() { }
	this.up   = function() { }
}
function MoveComList(num) {
	var setLnum  = num;
	Mcommand = true;

	LayWrite('mc_div', '<NOBR><strong>'+(num+1)+': '+g[num]+'</strong></NOBR>');

	this.move = function() {
		moveLAYER('mc_div',mx+10,my-30);
		return false;
	}

	this.up = function() {
		if(newLnum >= 0) {
			var com = command[setLnum];
			cominput(document.myForm,12,setLnum,newLnum);
		} else if(newLnum == -1){
			cominput(document.myForm,3,setLnum+1);
		}

		mc_out();
		newLnum = -2;

		Mcommand = false;
		moveLAYER("mc_div",-50,-50);
	}
}
//* ��������̵���ǤΥ��ޥ���������ɲå�����ץ� */
function new_http() {
	if(document.getElementById) {
		try{
			return new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e){
			try {
				return new ActiveXObject("Microsoft.XMLHTTP");
			} catch (E){
				if(typeof XMLHttpRequest != 'undefined') return new XMLHttpRequest;
			}
		}
	}
}
function send_command(form) {
	if (!xmlhttp) return true;

	form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;
	form.CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}.disabled = true;

	var progress  = document.getElementById('progress');
	var progresssub  = document.getElementById('progresssub');
	progress.innerHTML = '<blink>������...</blink>';
	progresssub.innerHTML = '<blink>������...</blink>';

	if (xmlhttp.readyState == 1 || xmlhttp.readyState == 2 || xmlhttp.readyState == 3) return; 

	xmlhttp.open("POST", "$HthisFile", true);
	if(!window.opera) xmlhttp.setRequestHeader("referer", "$HthisFile");

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var result = xmlhttp.responseText;
			if(result.indexOf('OK') == 0 || result.indexOf('OK') == 2048 || result.match(/OKsenddatacomplete/)) {
				str = plchg($HcommandMax);
				str = "<TABLE border=0><TR><TD class='commandjs1'><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B><br><br>"+str+"<br><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B></TD></TR></TABLE>";
				disp(str, "#ccffcc");
				selCommand(document.myForm.NUMBER.selectedIndex);
			} else {
				alert("�����˼��Ԥ��ޤ�����");
				form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
				form.CommandJavaButtonSub$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
			}
			progress.innerHTML = '';
			progresssub.innerHTML = '';
		}
	}

	var post = 'async=true&'
		+ 'CommandJavaButton' + d_ID + '=true&'
		+ 'COMMAND='+form.COMMAND.value+'&'
		+ 'TARGETID='+form.TARGETID.value+'&'
		+ 'POINTX='+form.POINTX.value+'&'
		+ 'POINTY='+form.POINTY.value+'&'
		+ 'JAVAMODE=java&'
		+ 'COMARY='+form.COMARY.value+'&'
		+ 'PASSWORD='+form.PASSWORD.value+'&';

	xmlhttp.send(post);
	return false;
}
function Kdown(e){
	var c, el;
	var m = document.myForm.AMOUNT.selectedIndex;
	if(m > 9) { m = 0; }
	if(document.all){
		if (event.altKey || event.ctrlKey || event.shiftKey) return;
		c = event.keyCode;
		el = new String(event.srcElement.tagName);
		el = el.toUpperCase();
		if (el == "INPUT") return;
//	}else if(document.layers){// NN4 KEYDOWN���٥�Ȥ�Win98�Ϥ�ʸ����������Τǥ����Ȳ�
//		if (e.modifiers != 0) return;
//		c = e.which;
//		if ((c >= 97) && (c <= 122)) c -= 32; // �Ѿ�ʸ�������ʸ���ˤ���
//		el = new String(e.target);
//		el = el.toUpperCase();
//		if (el.indexOf("<INPUT") >= 0) return;
	}else if(document.getElementById){
		if (e.altKey || e.ctrlKey || e.shiftKey) return;
		c = e.which;
		el = new String(e.target.tagName);
		el = el.toUpperCase();
		if (el == "INPUT") return;
	}
	c = String.fromCharCode(c);

	// �����줿�����˱����Ʒײ��ֹ�����ꤹ��
	switch (c) {
		case 'A': if($HuseAmity) c = $HcomAmity; else return; break; // ͧ��������
		case 'M': if($HuseSeaMine) c = $HcomSeaMine; else return; break; // ��������
		case 'F': c = $HcomNavyForm; break; // ��������
		case 'J': c = $HcomPrepare; break; // �Ϥʤ餷
		case 'U': c = $HcomReclaim; break; // ���Ω��
		case 'K': c = $HcomDestroy; break; // ����
		case 'B': c = $HcomSellTree; break; // Ȳ��
		case 'P': c = $HcomPlant; break; // ����
		case 'N': c = $HcomFarm; break; // ��������
		case 'I': c = $HcomFactory; break; // �������
		case 'S': c = $HcomMountain; break; // �η�������
		case 'D': c = $HcomDbase; break; // �ɱһ��߷���
		case '-': c = $HcomDoNothing; break; //INS ��ⷫ��
		case '.': cominput(myForm,3); return; //DEL ���
		case'\b': //BS ��������
			var no = document.myForm.COMMAND.selectedIndex;
			if(no > 0) document.myForm.COMMAND.selectedIndex = no - 1;
			cominput(myForm,3);
			return;
		case '0':case'`': document.myForm.AMOUNT.selectedIndex = m*10+0; return;
		case '1':case'a': document.myForm.AMOUNT.selectedIndex = m*10+1; return;
		case '2':case'b': document.myForm.AMOUNT.selectedIndex = m*10+2; return;
		case '3':case'c': document.myForm.AMOUNT.selectedIndex = m*10+3; return;
		case '4':case'd': document.myForm.AMOUNT.selectedIndex = m*10+4; return;
		case '5':case'e': document.myForm.AMOUNT.selectedIndex = m*10+5; return;
		case '6':case'f': document.myForm.AMOUNT.selectedIndex = m*10+6; return;
		case '7':case'g': document.myForm.AMOUNT.selectedIndex = m*10+7; return;
		case '8':case'h': document.myForm.AMOUNT.selectedIndex = m*10+8; return;
		case '9':case'i': document.myForm.AMOUNT.selectedIndex = m*10+9; return;
		case 'Z':case'j': document.myForm.AMOUNT.selectedIndex = 0; return;
		default:
		// IE �Ǥϥ���ɤΤ���� F5 �ޤǽ����Τǡ������˽����򤤤�ƤϤ����ʤ�
		return;
	}
	StatusMsg(c);
	cominput(document.myForm, 6, c);
}
function check_menu(){
	if(!document.myForm.MENUOPEN.checked){
		if(document.getElementById){ //NN6,IE5
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		} else if(document.layers){ // NN4 KEYDOWN���٥�Ȥ�Win98�Ϥ�ʸ����������Τǥ����Ȳ�
			window.captureEvents(Event.MOUSEMOVE);
//			window.captureEvents(Event.MOUSEMOVE | Event.KEYDOWN);
			window.onMouseMove = Mmove;
//			window.onKeyDown = Kdown;
		} else if(document.all){ // IE4
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		}
		document.allForm.MENUOPEN.value="";
    }else{
		document.allForm.MENUOPEN.value="on";
		if(document.myForm.MENUOPEN2.checked) { document.myForm.MENUOPEN2.checked = false; }
		if(document.myForm.MENUOPEN3.checked) { document.myForm.MENUOPEN3.checked = false; }
		if(document.mark_form.mark.checked)   { document.mark_form.mark.checked = false; }
    }
}
function check_menu2(){
	if(!document.myForm.MENUOPEN2.checked){
		if(document.getElementById){ //NN6,IE5
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		} else if(document.layers){ // NN4 KEYDOWN���٥�Ȥ�Win98�Ϥ�ʸ����������Τǥ����Ȳ�
			window.captureEvents(Event.MOUSEMOVE);
//		      window.captureEvents(Event.MOUSEMOVE | Event.KEYDOWN);
			window.onMouseMove = Mmove;
//		      window.onKeyDown = Kdown;
		} else if(document.all){ // IE4
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		}
		document.allForm.MENUOPEN2.value="";
	}else{
		document.allForm.MENUOPEN2.value="on";
		if(document.myForm.MENUOPEN.checked)  { document.myForm.MENUOPEN.checked = false; }
		if(document.myForm.MENUOPEN3.checked) { document.myForm.MENUOPEN3.checked = false; }
		if(document.mark_form.mark.checked)   { document.mark_form.mark.checked = false; }
	}
}
function check_menu3(){
	if(!document.myForm.MENUOPEN3.checked){
		if(document.getElementById){ //NN6,IE5
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		} else if(document.layers){ // NN4 KEYDOWN���٥�Ȥ�Win98�Ϥ�ʸ����������Τǥ����Ȳ�
			window.captureEvents(Event.MOUSEMOVE);
//		      window.captureEvents(Event.MOUSEMOVE | Event.KEYDOWN);
			window.onMouseMove = Mmove;
//		      window.onKeyDown = Kdown;
		} else if(document.all){ // IE4
			document.onmousemove = Mmove;
			document.onkeydown = Kdown;
		}
		document.allForm.MENUOPEN3.value="";
	}else{
		document.allForm.MENUOPEN3.value="on";
		if(document.myForm.MENUOPEN.checked)  { document.myForm.MENUOPEN.checked = false; }
		if(document.myForm.MENUOPEN2.checked) { document.myForm.MENUOPEN2.checked = false; }
		if(document.mark_form.mark.checked)   { document.mark_form.mark.checked = false; }
	}
}
function set_land(x, y, land, img) {
	com_str = '(' + x + ', ' + y + ")\\n " + land + ' ';
	if($oroti) { img = '${baseIMG}/' + img; }

	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		x2 = c[1];
		y2 = c[2];
		if(x == x2 && y == y2 && (c[0] <= $HcomComplex[$#HcomplexComName] ||(c[0] >= 210 && c[0] <= 220)||(c[0] >= 331 && c[0] <= 350))){
			com_str += '[' + (i + 1) +']' ;
			kind = g[i][0];
			if(c[0] == $HcomDestroy){
				if(c[3] == 0){
					com_str += kind;
				} else {
					arg = c[3] * 200;
					arg = "��ͽ\��" + arg + "$HunitMoney��";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "��" + c[3] + "���";
					com_str += kind + arg;
				}else{
					com_str += kind;
				}
			}else if(c[0] == $HcomNavyForm) { // ��������
				if(c[3] < 1){
					c[3] = 1;
				} else if (c[3] > 4){
					c[3] = 4;
				}
				arg = ofName[c[3]-1];
				com_str = arg + kind;
			}else{
				com_str += kind;
			}
			com_str += ' ';
		}
	}
	document.POPUP1.COMSTATUS.value= com_str;
	document.POPUP1.NAVIIMG.src= img;
	document.POPUP2.COMSTATUS.value= com_str;
	document.POPUP2.NAVIIMG.src= img;
	document.POPUP3.COMSTATUS.value= com_str;
	document.POPUP3.NAVIIMG.src= img;
}
function showElement(layName) {
	var element = document.getElementById(layName).style;
	element.display = "block";
	element.visibility ='visible';
}
function hideElement(layName) {
	var element = document.getElementById(layName).style;
	element.display = "none";
}
function chNum(num) {
	document.ch_numForm.AMOUNT.options.length = 100;
	for(i=0;i<document.ch_numForm.AMOUNT.options.length;i++){
		if(document.ch_numForm.AMOUNT.options[i].value == num){
			document.ch_numForm.AMOUNT.selectedIndex = i;
			document.ch_numForm.AMOUNT.options[i].selected = true;
			moveLAYER('ch_num', mx-10, my-60);
			showElement('ch_num');
			break;
		}
	}
}
function chNumDo() {
	var num = document.ch_numForm.AMOUNT.options[document.ch_numForm.AMOUNT.selectedIndex].value;
	cominput(document.myForm,13,num);
	hideElement('ch_num');
}
function set_com(x, y, land) {
	com_str = '(' + x + ', ' + y + ') ' + land + "\\n";
	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		x2 = c[1];
		y2 = c[2];
		if(x == x2 && y == y2 && (c[0] <= $HcomComplex[$#HcomplexComName] ||(c[0] >= 210 && c[0] <= 220)||(c[0] >= 331 && c[0] <= 350))){
			com_str += '[' + (i + 1) +']' ;
			kind = g[i][0];
			if(c[0] == $HcomDestroy){
				if(c[3] == 0){
					com_str += kind;
				} else {
					arg = c[3] * 200;
					arg = "��ͽ\��" + arg + "$HunitMoney��";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "��" + c[3] + "���";
					com_str += kind + arg;
				}else{
					com_str += kind;
				}
			}else if(c[0] == $HcomNavyForm) { // ��������
				if(c[3] < 1){
					c[3] = 1;
				} else if (c[3] > 4){
					c[3] = 4;
				}
				arg = ofName[c[3]-1];
				com_str = arg + kind;
			}else{
				com_str += kind;
			}
			com_str += ' ';
		}
	}
	document.LANDINFO.COMSTATUS.value= com_str;
	status = com_str;
	return true;
}
function not_com() {
//	document.LANDINFO.COMSTATUS.value="";
}
function myisland(theForm,myid) {
	for(i = 0; i < theForm.TARGETID.length ;i++) {
		if(theForm.TARGETID.options[i].value == myid) {
			theForm.TARGETID.selectedIndex = i;
			return;
		}
	}
}
function StatusMsg(x) {
msg = new Array(64);
$Msg
	window.status = msg[x];
}
Array.prototype.clone = function(){
    return Array.apply(null,this)
}
END

	$src .= $HpopupNaviJS if($HpopupNavi);

	if($mode) {
		open(OUT,">${HefileDir}/hakojima.js");
#		print OUT jcode::sjis($src); # jcode���ѻ�
		print OUT $src;
		close(OUT);
		chmod(0666, "${HefileDir}/hakojima.js");
	} else {
		out(<<END);
<SCRIPT Language="JavaScript">
<!--
$src
//-->
</SCRIPT>
END
	}
}

1;
