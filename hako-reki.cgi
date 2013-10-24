#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 歴代ランキングモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------

# データファイル名
my $HrekidaiData = 'rekidai.cgi';

# 記録するデータの種類(基本的には$island->{KIND}のKINDに入れてデータが参照できるものに限定されます)
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
# データ項目名
my @HrekidaiName      = (
	'人口',
	'面積',
	'農場',
	'職場',
	'採掘場',
	"${AfterName}撃破数",
	'怪獣退治数',
	'怪獣出現数',
	'所属不明艦出現数',
	'総獲得経験値',
	'艦艇経験値合計',
	'艦艇経験値',
	'軍港経験値',
	'艦艇撃沈数',
);
# データイメージ画像
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
# データの後ろにつけるやつ
my @HrekidaiAfterName = (
	"$HunitPop",
	"$HunitArea",
	"0$HunitPop規模",
	"0$HunitPop規模",
	"0$HunitPop規模",
	"$AfterName",
	"$HunitMonster",
	"$HunitMonster",
	'艦',
	'',
	'',
	'',
	'',
	'艦',
);

# ランキング記録数(稼働中の変更も可能です)
my $HrecordNo = 10;
# ランキング表示数(記録数より大きくしてもムダです)
my $Hranking = 10;
# 一行に表示される項目数
my $Hcolum = 2;
#----------------------------------------------------------------------
# 好みによって設定する部分は以上
#----------------------------------------------------------------------
# データ読み込み
sub readReki {
	# データファイルを開く
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
	# ファイルを閉じる
	close(RIN);

	return 1;
}

# データ書き込み
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

# 更新処理
sub mainReki {
	# データ読み込み
	readReki();

	# 海戦データ取得($island->{KIND}以外)
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
			next if($HnavySpecial[$_] & 0x8); # 軍港は合計に入れない
			$island->{'totalSink'} += $island->{'sink'}[$_] + $island->{'sinkself'}[$_];
			$island->{'selfSink'} += $island->{'sinkself'}[$_];
		}
		$fkind = $island->{'fkind'};
		foreach (@$fkind) {
			my($eId, $nTmp, $nStat, $nSea, $nExp, $nFlag, $nNo, $nKind, $nHp) = navyUnpack(hex($_));
			my $kind = 'navy' . $nKind; # 保有数
			$island->{$kind}++;
			$island->{'totalNavyExp'} += $nExp;
			if($HnavySpecial[$nKind] & 0x8) {
				$island->{'portExp'} = $nExp if($nExp > $island->{'portExp'});
			} else {
				$island->{'navyExp'} = $nExp if($nExp > $island->{'navyExp'});
			}
		}
	}
	# 海戦データ取得ここまで

	# ランキング更新
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

		# 人口が同じときは直前のターンの順番のまま
		my $max = @{$rekidai{$kind}} - 1;
		my @idx = (0..$max);
		@idx = sort { $rekidai{$kind}[$b]->{'value'} <=> $rekidai{$kind}[$a]->{'value'} || $a <=> $b } @idx;
		@{$rekidai{$kind}} = @{$rekidai{$kind}}[@idx];
		splice(@{$rekidai{$kind}}, $HrecordNo);
	}

	# データ読み込み
	writeReki();

}

# ランキング表示
sub rankingReki {
	# データ読み込み
	readReki();
	# 開放
	unlock();

	out(<<END);
<DIV ID='Ranking'>
<H1>歴代ランキング</H1>
<P>
${AfterName}は消えても名は残る！！目指せ<B>ALL NO.1</B>！！存在する${AfterName}は<B>観光</B>できます。
</P>
[<A HREF="${HthisFile}?Rank=0">部門別No.1(ターン${HislandTurn})へ</A>]
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
<TR><TH>${HtagTH_}順位${H_tagTH}</TH><TH>${HtagTH_}${AfterName}名${H_tagTH}</TH><TH>${HtagTH_}記録${H_tagTH}</TH><TH>${HtagTH_}ターン${H_tagTH}</TH></TR>
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
# 著作権表示 - 他の箱庭へ移植する場合に下のコメントアウトをとってください。
	out("<DIV align='right'>patchworked by <a style='text-decoration:none;' href='http://no-one.s53.xrea.com/' target='_top'>neo_otacky</a></DIV>\n");
}

1;

###----------###
### 導入方法 ###
###----------###

### 行頭の#をとってコピペ、###は導入についてのコメントなのでコピペ不要

### メインモード分岐部分に追加
#} elsif($HmainMode eq 'rekidai') {
#	# 歴代記録
#	require('./hako-reki.cgi');
#	rankingReki();

### CGIの読みこみ部分に追加 sub cgiInput内のmain modeの取得部分
#	} elsif($getLine =~ /Rekidai=([0-9]*)/) {
#		$HmainMode = 'rekidai';

### ヘッダかトップページのリンク部分に追加
#	out(qq|[<A href="$HthisFile?Rekidai=0" target="_blank">歴代記録</A>] |);
### outを使わなくても、[<A href="$HthisFile?Rekidai=0" target="_blank">歴代記録</A>]がHTML内に記述されるようにすればよい

### ターン更新処理に追加 sub turnMain内のwriteIslandsFileの上あたり
#		# 歴代記録処理
#		require './hako-reki.cgi';
#		mainReki();

### 海戦データ取得(line83-107)部分を削除またはコメントアウトして、記録するデータの種類の設定を書き換えてください。
