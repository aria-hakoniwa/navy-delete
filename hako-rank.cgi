#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ��󥭥󥰥⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
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

# ��󥭥�ɽ����(��Ͽ������礭�����Ƥ����Ǥ�)
my $Hranking = 10;
# ��Ԥ�ɽ���������ܿ�
my $Hcolum = 2;
# ������Υ��᡼�������ե�����
my @bumonImage = (
	"$HlandTownImage[$#HlandTownImage]", # �͸�
	"$HlandImage[$HlandPlains]",    # ����
	"$HlandImage[$HlandFarm]",    # ����
	"$HlandImage[$HlandFactory]",    # ����
	"$HlandImage[$HlandMountain][1]",    # �η���
	"$HlandImage[$HlandWaste][1]",    # ����˿�
	'monster7.gif',    # �����༣��
	'monster0.gif',    # ���ýи���
	'navy1.gif',    # ��°�����Ͻи���
	"$HlandImage[$HlandBase]",    # ������и���
	'navy2.gif',    # �����и��͹��
	'navy3.gif',    # �����и���
	'navy0.gif',    # �����и���
	"$HnavyImageZ",    # ����������
);

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# ��󥭥�
#----------------------------------------------------------------------
sub rankIslandMain {
	my($i, $monster, $monslive, $monstertype, $hmonstertype, $fkind, $sink, $selfsink);
	# ����
	foreach $i (0..$islandNumber) {
		my $island = $Hislands[$i];

		$island->{'defeatcount'} = @{$island->{'defeat'}} / 2;

		$monster = $island->{'monsterlive'};
		$monster =~ /([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)/;
		$island->{'monslive'} = $1;
		$island->{'unknownlive'} = $4;

		$sink = $island->{'sink'};
		$sinkself = $island->{'sinkself'};
		foreach (0..$#HnavyName) {
			next if($HnavySpecial[$_] & 0x8); # �����Ϲ�פ�����ʤ�
			$island->{'totalSink'} += $island->{'sink'}[$_] + $island->{'sinkself'}[$_];
			$island->{'selfSink'} += $island->{'sinkself'}[$_];
		}

		$fkind = $island->{'fkind'};
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack(hex($_));
			my $kind = 'navy' . $nKind; # ��ͭ��
			$island->{$kind}++;
			$island->{'totalNavyExp'} += $nExp;
			if($HnavySpecial[$nKind] & 0x8) {
				if($nExp > $island->{'portExp'}) {
					$island->{'portExp'} = $nExp;
					$island->{'maxPortExpValue'} = hex($_);
				}
			} elsif($nExp > $island->{'navyExp'}) {
				$island->{'navyExp'} = $nExp;
				$island->{'maxExpValue'} = hex($_);
			}
		}
	}

	my @elements   = ( 'pop', 'area', 'farm', 'factory', 'mountain',         'defeatcount', 'monsterkill',   'monslive',      'unknownlive',         'gain',   'totalNavyExp',    'navyExp',    'portExp',  'totalSink');
	my @bumonName  = ('�͸�', '����', '����',    '����',   '�η���',  "${AfterName}���˿�",  '�����༣��', '���ýи���', '��°�����Ͻи���', '������и���', '�����и��͹��', '�����и���', '�����и���', '����������');
	my @bAfterName = ("$HunitPop", "$HunitArea","0$HunitPop����", "0$HunitPop����", "0$HunitPop����", "$AfterName", "$HunitMonster", "$HunitMonster", '��', '', '', '', '', '��');
	splice(@elements, -5) if($HnavyName[0] eq '');

	if(!$HnavySafetyZone || $HnavySafetyInvalidp) {
		push(@elements, 'selfSink');
		push(@bumonName, '����������');
		push(@bumonImage, 'navy5.gif');
		push(@bAfterName, '��');
	}

	foreach (0..$#HnavyName) {
		last if($HmaxComNavyLevel && ($HcomNavyNumber[$#HcomNavyNumber] < $_));
		my $kind = 'navy' . $_;
		push(@elements, $kind);
		push(@bumonName, "${HnavyName[$_]}��ͭ��");
		push(@bumonImage, $HnavyImage[$_]);
		my $after = ($_ ? '��' :'��');
		push(@bAfterName, $after);
	}


	my $rt = "\n";
	my %islands;
	my($id, $f);
	foreach (@elements) {
		@{$islands{$_}} = rankingSort($_);
	}
	# navyExp
	my(@navyLevel, @fKind, @ofname);
	foreach (@{$islands{'navyExp'}}) {
		$id = $_->{'id'};
		push(@navyLevel, expToLevel($HlandNavy, $Hislands[$HidToNumber{$id}]->{'navyExp'}));
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($Hislands[$HidToNumber{$id}]->{'maxExpValue'});
		push(@fKind, $nKind);
		push(@ofname, $Hislands[$HidToNumber{$id}]->{'fleet'}[$nNo]);
	}
	# portExp
	my(@portLevel, @pKind, @pfname);
	foreach (@{$islands{'portExp'}}) {
		$id = $_->{'id'};
		push(@portLevel, expToLevel($HlandNavy, $Hislands[$HidToNumber{$id}]->{'portExp'}));
		my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack($Hislands[$HidToNumber{$id}]->{'maxPortExpValue'});
		push(@pKind, $nKind);
		push(@pfname, $Hislands[$HidToNumber{$id}]->{'fleet'}[$nNo]);
	}

	# defeat ���ˤ�����ꥹ��
	my @dname;
	foreach (@{$islands{'defeatcount'}}) {
		$id = $_->{'id'};
		my @defeat = @{$_->{'defeat'}};
		my($dNameList)= '';
		for($i = 0; $i < $#defeat; $i+=2) {
			$dNameList .= "\n" if($i);
			$dNameList .= $defeat[$i] . '(' . $defeat[$i+1] . ')';
			$dNameList =~ s/<FONT COLOR=\"[\w\#]+\"><B>(.*)<\/B><\/FONT>/$1/g;
			$dNameList =~ s/<[^<]*>//g;
		}
		my $defeatname = "<A TITLE=\"$dNameList\" ";
		$dNameList =~ s/$rt/ /g;
		$defeatname .= "onMouseOver='status=\"$dNameList\"; return true;' onMouseOut=\"status = '';\">";
		push(@dname, $defeatname);
	}

	# monsterkill �ݤ������åꥹ��
	my @mname;
	foreach (@{$islands{'monsterkill'}}) {
		$id = $_->{'id'};
		my $monsterkill = $_->{'prize'};
		$monsterkill =~ /([0-9]*),([0-9]*),([0-9]*),(.*)/;
		my($flags, $monsters, $hmonsters) = ($1, $2, $3);
		$f = 1;
		my($mNameList) = '';
		for($i = 0; $i < $HmonsterNumber; $i++) {
			if($monsters & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HmonsterName[$i]]";
			}
			$f *= 2;
		}
		$f = 1;
		for($i = 0; $i < $HhugeMonsterNumber; $i++) {
			if($hmonsters & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HhugeMonsterName[$i]]";
			}
			$f *= 2;
		}
		$monsterkill = "<A TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$monsterkill .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\">";
		push(@mname, $monsterkill);
	}

	# monslive �и���β��åꥹ��
	my @mlive;
	foreach (@{$islands{'monslive'}}) {
		$id = $_->{'id'};
		$monsterlive = $_->{'monsterlive'};
		$monsterlive =~ /([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)/;
		($monslive, $monstertype, $hmonstertype, $unknownlive, $unknowntype) = ($1, $2, $3, $4, $5);
		$f = 1;
		$mNameList = '';
		for($i = 0; $i < $HmonsterNumber; $i++) {
			if($monstertype & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HmonsterName[$i]] ";
			}
			$f *= 2;
		}
		$f = 1;
		for($i = 0; $i < $HhugeMonsterNumber; $i++) {
			if($hmonstertype & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HhugeMonsterName[$i]]";
			}
			$f *= 2;
		}
		$monsterlive = "<A TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$monsterlive .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\">";
		push(@mlive, $monsterlive);
	}

	# unknownlive �и���ν�°���������ꥹ��
	my @ulive;
	foreach (@{$islands{'unknownlive'}}) {
		$id = $_->{'id'};
		my $unknlive = $_->{'monsterlive'};
		$unknlive =~ /([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)/;
		($monslive, $monstertype, $hmonstertype, $unknownlive, $unknowntype) = ($1, $2, $3, $4, $5);
		$f = 1;
		$mNameList = '';
		foreach(0..$#HnavyName) {
			if($unknowntype & $f) {
				$mNameList .= "\n" if($mNameList ne '');
				$mNameList .= "[$HnavyName[$_]] ";
			}
			$f *= 2;
		}
		my $unknownName = "<A TITLE=\"$mNameList\" ";
		$mNameList =~ s/$rt//g;
		$unknownName .= "onMouseOver='status=\"$mNameList\"; return true;' onMouseOut=\"status = '';\">";
		push(@ulive, $unknownName);
	}

	# ����
	unlock();

	my($reki);
	$reki = "[<A HREF=\"${HthisFile}?Rekidai=0\">�����󥭥󥰤�</A>]" if($HuseRekidai);
	out(<<END);
<DIV ID='Ranking'>
<H1>��������NO.1 (������${HislandTurn})</H1>
<P>
�ܻؤ�<B>ALL NO.1</B>����${AfterName}̾�򥯥�å�����ȡ�<B>�Ѹ�</B>�Ǥ��ޤ���
</P>
$reki
END
	$Hcolum = 1 if(!$Hcolum);
	foreach (0..$#elements) {
		out("<TABLE ALIGN=\"center\" width=\"100%\"><TR>\n") if(!($_ % $Hcolum));
		out(<<END);
<td width="9%">
<TABLE BORDER=1 width="100%">
<TR><TD ALIGN="left"><img src="$bumonImage[$_]"></TD>
<TD class="RankingCell" colspan=2 ALIGN="center" width="100%"><span class="bumon"><B>${bumonName[$_]}</B></span></TD></TR>
<TR><TH>${HtagTH_}���${H_tagTH}</TH><TH>${HtagTH_}${AfterName}̾${H_tagTH}</TH><TH>${HtagTH_}��Ͽ${H_tagTH}</TH></TR>
END
		my $max = $HbfieldNumber + ($Hranking - 1);
		foreach my $i ($HbfieldNumber..$max) {
			my $isl = $islands{$elements[$_]}[$i];
			my $id = $isl->{'id'};
			my $name = islandName($isl);
			my $element = $isl->{$elements[$_]};

			my ($Str1, $Str2);
			if(($element ne '') && ($element != 0)) {
				if($elements[$_] eq 'defeatcount') {
					$Str1 = $dname[$i];
					$Str2 = '</A>';
				} elsif($elements[$_] eq 'monsterkill') {
					$Str1 = $mname[$i];
					$Str2 = '</A>';
				} elsif($elements[$_] eq 'monslive') {
					$Str1 = $mlive[$i];
					$Str2 = '</A>';
				} elsif($elements[$_] eq 'unknownlive') {
					$Str1 = $ulive[$i];
					$Str2 = '</A>';
				} elsif($elements[$_] eq 'navyExp') {
					$Str1 = "";
					$Str2 = "<small><small>($ofname[$i]���� $HnavyName[$fKind[$i]] Lv.$navyLevel[$i])</small></small>";
				} elsif($elements[$_] eq 'portExp') {
					$Str1 = "";
					$Str2 = "<small><small>($pfname[$i]���� $HnavyName[$pKind[$i]] Lv.$portLevel[$i])</small></small>";
				} else {
					$Str1 = '';
					$Str2 = '';
				}

				my $j = $i + 1 - $HbfieldNumber;
				my $value = "${Str1}${element}${bAfterName[$_]}${Str2}";
				1 while $value =~ s/(.*\d)(\d\d\d)/$1,$2/;
				if($j == 1) {
					out(<<END);
<TR>
<TH ALIGN="right"><H3 style='display:inline'>$j</H3></TD>
<TH><H3 style='display:inline'><A STYlE="text-decoration:none" HREF="${HthisFile}?Sight=${id}" alt="ID=${id}" title="ID=${id}">${HtagName_}${name}${H_tagName}</H3></TD>
<TH><H3 style='display:inline'>$value</H3></TD>
</TR>
END
				} else {
					out(<<END);
<TR>
<TD ALIGN="right">$j</TD>
<TD ALIGN="center"><A STYlE="text-decoration:none" HREF="${HthisFile}?Sight=${id}" alt="ID=${id}" title="ID=${id}">${HtagName_}${name}${H_tagName}</TD>
<TD ALIGN="center">$value</TD>
</TR>
END
				}
			} else {
			out(<<END);
<TR>
<TD ALIGN="right"> - </TD>
<TD ALIGN="center">${HtagName_} - ${H_tagName}</TD>
<TD ALIGN="center"> - </TD>
</TR>
END
			}
		}
		out("</TABLE></TD>\n");
		out("</TR></TABLE>\n") if(!(($_ + 1) % $Hcolum));
	}
	out("</TR></TABLE>\n") if((($#elements + 1) % $Hcolum));
	out("</DIV>\n");
}

# ������
sub rankingSort {
	my($kind) = @_;

	my @idx = (0..$#Hislands);
	@idx = sort {
			$Hislands[$b]->{'field'} <=> $Hislands[$a]->{'field'} || # �Хȥ�ե������ͥ��
			$Hislands[$b]->{$kind} <=> $Hislands[$a]->{$kind} || # $kind�ǥ�����
			$a <=> $b # $kind��Ʊ���ʤ�����Τޤ�
		   } @idx;
	return @Hislands[@idx];
}

1;
