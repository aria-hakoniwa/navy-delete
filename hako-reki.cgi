#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �����󥭥󥰥⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------

# �ǡ����ե�����̾
my $HrekidaiData = 'rekidai.cgi';

# ��Ͽ����ǡ����μ���(����Ū�ˤ�$island->{KIND}��KIND������ƥǡ��������ȤǤ����Τ˸��ꤵ��ޤ�)
my @HrekidaiKind      = (
	'pop',
	'area',
	'farm',
	'factory',
	'mountain',
	'defeatcount',
	'monsterkill',
	'monslive',
	'unknownlive',
	'gain',
	'totalNavyExp',
	'navyExp',
	'portExp',
	'totalSink',
);
# �ǡ�������̾
my @HrekidaiName      = (
	'�͸�',
	'����',
	'����',
	'����',
	'�η���',
	"${AfterName}���˿�",
	'�����༣��',
	'���ýи���',
	'��°�����Ͻи���',
	'������и���',
	'�����и��͹��',
	'�����и���',
	'�����и���',
	'����������',
);
# �ǡ������᡼������
my @HrekidaiImage     = (
	"$HlandTownImage[$#HlandTownImage]",
	"$HlandImage[$HlandPlains]",
	"$HlandImage[$HlandFarm]",
	"$HlandImage[$HlandFactory]",
	"$HlandImage[$HlandMountain][1]",
	"$HlandImage[$HlandWaste][1]",
	'monster7.gif',
	'monster0.gif',
	'navy1.gif',
	"$HlandImage[$HlandBase]",
	'navy2.gif',
	'navy3.gif',
	'navy0.gif',
	"$HnavyImageZ",
);
# �ǡ����θ��ˤĤ�����
my @HrekidaiAfterName = (
	"$HunitPop",
	"$HunitArea",
	"0$HunitPop����",
	"0$HunitPop����",
	"0$HunitPop����",
	"$AfterName",
	"$HunitMonster",
	"$HunitMonster",
	'��',
	'',
	'',
	'',
	'',
	'��',
);

# ��󥭥󥰵�Ͽ��(��Ư����ѹ����ǽ�Ǥ�)
my $HrecordNo = 10;
# ��󥭥�ɽ����(��Ͽ������礭�����Ƥ����Ǥ�)
my $Hranking = 10;
# ��Ԥ�ɽ���������ܿ�
my $Hcolum = 2;
#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------
# �ǡ����ɤ߹���
sub readReki {
	# �ǡ����ե�����򳫤�
	if(!open(RIN, "<${HlogdirName}/${HrekidaiData}")) {
		rename("${HlogdirName}/tmp${HrekidaiData}", "${HlogdirName}/${HrekidaiData}");
		if(!open(RIN, "${HlogdirName}/${HrekidaiData}")) {
			return 0;
		}
	}
	my $kind;
	my $j = 0;
	while($line = <RIN>) {
		if($line =~ /^([0-9]*),([0-9]*),([0-9]*),(.*)$/) {
			($id, $value, $turn, $name) = ($1, $2, $3, $4);
			$rekidai{$kind}[$j]->{'id'}    = $id;
			$rekidai{$kind}[$j]->{'value'} = $value;
			$rekidai{$kind}[$j]->{'turn'}  = $turn;
			$rekidai{$kind}[$j]->{'name'}  = $name;
			$HidToNumberR{$kind}{$id} = $j;
			$j++;
		} elsif($line =~ /^<(.*)>$/) {
			$kind = $1;
			$j = 0;
		}
	}
	# �ե�������Ĥ���
	close(RIN);

	return 1;
}

# �ǡ����񤭹���
sub writeReki {
	my $i;
	open(ROUT, ">${HlogdirName}/tmp${HrekidaiData}");
	foreach (@HrekidaiKind) {
		print ROUT '<' . $_ . '>' . "\n";
		my @rdata = @{$rekidai{$_}};
		for($i = 0; $i < $HrecordNo; $i++) {
			my($id, $value, $turn, $name) = ($rdata[$i]->{'id'}, $rdata[$i]->{'value'}, $rdata[$i]->{'turn'}, $rdata[$i]->{'name'});
			print ROUT "$id,$value,$turn,$name\n";
		}
	}
	close(ROUT);
	unlink("${HlogdirName}/${HrekidaiData}");
	rename("${HlogdirName}/tmp${HrekidaiData}", "${HlogdirName}/${HrekidaiData}");
}

# ��������
sub mainReki {
	# �ǡ����ɤ߹���
	readReki();

	# ����ǡ�������($island->{KIND}�ʳ�)
	my($i, $island, $monster, $monslive, $fkind, $sink, $selfsink);
	foreach $i (0..$islandNumber) {
		$island = $Hislands[$i];

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
				$island->{'portExp'} = $nExp if($nExp > $island->{'portExp'});
			} else {
				$island->{'navyExp'} = $nExp if($nExp > $island->{'navyExp'});
			}
		}
	}
	# ����ǡ������������ޤ�

	# ��󥭥󥰹���
	my($kind, , $id, $value, $turn, $name, $n, $reki);
	foreach $kind (@HrekidaiKind){
		$j = $HrecordNo;
		foreach $i ($HbfieldNumber..$islandNumber) {
			$island = $Hislands[$i];
			$id = $island->{'id'};
			$name = islandName($island);
			$value = $island->{$kind};
			$n = $HidToNumberR{$kind}{$id};
			if(defined $n) {
				if($value > $rekidai{$kind}[$n]->{'value'}) {
					$rekidai{$kind}[$n]->{'id'}    = $id;
					$rekidai{$kind}[$n]->{'value'} = $value;
					$rekidai{$kind}[$n]->{'turn'}  = $HislandTurn;
					$rekidai{$kind}[$n]->{'name'}  = $name;
				} elsif($rekidai[$n]->{'name'} ne $name){
					$rekidai[$n]->{'name'} = $name;
				}
			} else {
				$rekidai{$kind}[$j]->{'id'}    = $id;
				$rekidai{$kind}[$j]->{'value'} = $value;
				$rekidai{$kind}[$j]->{'turn'}  = $HislandTurn;
				$rekidai{$kind}[$j]->{'name'}  = $name;
				$j++;
			}
		}

		# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
		my $max = @{$rekidai{$kind}} - 1;
		my @idx = (0..$max);
		@idx = sort { $rekidai{$kind}[$b]->{'value'} <=> $rekidai{$kind}[$a]->{'value'} || $a <=> $b } @idx;
		@{$rekidai{$kind}} = @{$rekidai{$kind}}[@idx];
		splice(@{$rekidai{$kind}}, $HrecordNo);
	}

	# �ǡ����ɤ߹���
	writeReki();

}

# ��󥭥�ɽ��
sub rankingReki {
	# �ǡ����ɤ߹���
	readReki();
	# ����
	unlock();

	out(<<END);
<DIV ID='Ranking'>
<H1>�����󥭥�</H1>
<P>
${AfterName}�Ͼä��Ƥ�̾�ϻĤ롪���ܻؤ�<B>ALL NO.1</B>����¸�ߤ���${AfterName}��<B>�Ѹ�</B>�Ǥ��ޤ���
</P>
[<A HREF="${HthisFile}?Rank=0">������No.1(������${HislandTurn})��</A>]
END
	splice(@HrekidaiKind, -5) if($HnavyName[0] eq '');
	$Hcolum = 1 if(!$Hcolum);
	foreach (0..$#HrekidaiKind) {
		out("<TABLE ALIGN=\"center\" width=\"100%\"><TR>\n") if(!($_ % $Hcolum));
		out(<<END);
<td width="9%">
<TABLE BORDER=1 width="100%">
<TR><TD ALIGN="left"><img src="$HrekidaiImage[$_]"></TD>
<TD class="RankingCell" colspan=3 ALIGN="center" width="100%"><span class="bumon"><B>${HrekidaiName[$_]}</B></span></TD></TR>
<TR><TH>${HtagTH_}���${H_tagTH}</TH><TH>${HtagTH_}${AfterName}̾${H_tagTH}</TH><TH>${HtagTH_}��Ͽ${H_tagTH}</TH><TH>${HtagTH_}������${H_tagTH}</TH></TR>
END
		my $max = $Hranking - 1;
		foreach my $i (0..$max) {
			my $id    = $rekidai{$HrekidaiKind[$_]}[$i]->{'id'};
			my $name  = $rekidai{$HrekidaiKind[$_]}[$i]->{'name'};
			my $value = $rekidai{$HrekidaiKind[$_]}[$i]->{'value'};
			my $turn  = $rekidai{$HrekidaiKind[$_]}[$i]->{'turn'};

			if(($value ne '') && ($value != 0)) {
				my $j = $i + 1;
				my $value = "${value}${HrekidaiAfterName[$_]}";
				1 while $value =~ s/(.*\d)(\d\d\d)/$1,$2/;

				my ($Str1, $Str2);
				my $n = $HidToNumber{$id};
				if(defined $n) {
					$Str1 = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=${id}\" alt=\"ID=${id}\" title=\"ID=${id}\">${HtagName_}";
					$Str2 = "${H_tagName}</A>";
				} else {
					$Str1 = $HtagName2_;
					$Str2 = $H_tagName2;
				}
				if($j == 1) {
				out(<<END);
<TR>
<TH ALIGN="right"><H3 style='display:inline'>$j</H3></TH>
<TH><H3 style='display:inline'>${Str1}${name}${Str2}</H3></TH>
<TH><H3 style='display:inline'>$value</H3></TH>
<TH><H3 style='display:inline'>$turn</H3></TH>
</TR>
END
				} else {
				out(<<END);
<TR>
<TD ALIGN="right">$j</TD>
<TD ALIGN="center">${Str1}${name}${Str2}</TD>
<TD ALIGN="center">$value</TD>
<TD ALIGN="center">$turn</TD>
</TR>
END
				}
			} else {
			out(<<END);
<TR>
<TD ALIGN="right"> - </TD>
<TD ALIGN="center">${HtagName_} - ${H_tagName}</TD>
<TD ALIGN="center"> - </TD>
<TD ALIGN="center"> - </TD>
</TR>
END
			}
		}
		out("</TABLE></TD>\n");
		out("</TR></TABLE>\n") if(!(($_ + 1) % $Hcolum));
	}
	out("</TR></TABLE>\n") if((($#HrekidaiKind + 1) % $Hcolum));
	out("</DIV>\n");
# ���ɽ�� - ¾��Ȣ��ذܿ�������˲��Υ����ȥ����Ȥ�ȤäƤ���������
	out("<DIV align='right'>patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/' target='_top'>neo_otacky</a></DIV>\n");
}

1;

###----------###
### Ƴ����ˡ ###
###----------###

### ��Ƭ��#��Ȥäƥ��ԥڡ�###��Ƴ���ˤĤ��ƤΥ����ȤʤΤǥ��ԥ�����

### �ᥤ��⡼��ʬ����ʬ���ɲ�
#} elsif($HmainMode eq 'rekidai') {
#	# ���嵭Ͽ
#	require('./hako-reki.cgi');
#	rankingReki();

### CGI���ɤߤ�����ʬ���ɲ� sub cgiInput���main mode�μ�����ʬ
#	} elsif($getLine =~ /Rekidai=([0-9]*)/) {
#		$HmainMode = 'rekidai';

### �إå����ȥåץڡ����Υ����ʬ���ɲ�
#	out(qq|[<A href="$HthisFile?Rekidai=0" target="_blank">���嵭Ͽ</A>] |);
### out��Ȥ�ʤ��Ƥ⡢[<A href="$HthisFile?Rekidai=0" target="_blank">���嵭Ͽ</A>]��HTML��˵��Ҥ����褦�ˤ���Ф褤

### �����󹹿��������ɲ� sub turnMain���writeIslandsFile�ξ夢����
#		# ���嵭Ͽ����
#		require './hako-reki.cgi';
#		mainReki();

### ����ǡ�������(line83-107)��ʬ�����ޤ��ϥ����ȥ����Ȥ��ơ���Ͽ����ǡ����μ���������񤭴����Ƥ���������
