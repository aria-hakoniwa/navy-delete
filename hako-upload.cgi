#!/usr/bin/perl

# The Return of Neptune: http://no-one.s53.xrea.com/
# patchworked by neo_otacky. for 海戦JS
#----------------------------------------------------------------------
# アップロードモジュール
#	島データをサーバーへアップするためのものです。
#----------------------------------------------------------------------
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
#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
# 初期設定用ファイルを読み込む
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#ここまで-------------------------------------------------------------

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
	close(PIN);
}
&cookieInput();
if(!(&formdecode())){
	&error("送信エラー");
}
if(!checkSpecialPassword($HdefaultPassword)) {
	$HtempBack2 = "<small><A HREF=\"$HthisFile\">トップへ戻る</A></small>";
	&error("パスワードエラー");
} else {
	$HtempBack2 = "<A HREF=\"$HmenteFile?ADMIN=$HdefaultPassword\">メンテナンスへ</A> <small><A HREF=\"$HthisFile\">トップへ戻る</A></small>";
}
if(!(&readIslandsFile())){
	&error("メインデータ読み込みエラー");
} else {
	&dataUpload();
}

#終了
exit(0);

#サブルーチン---------------------------------------------------------
#----------------------------------------------------------------------
# デコード
#----------------------------------------------------------------------
sub formdecode {
	my($line, $boundary, @params, $param);

	if($HuseUpload && uc($ENV{'REQUEST_METHOD'}) eq 'POST') {
		binmode STDIN;
		read(STDIN, $line, $ENV{'CONTENT_LENGTH'});
	} else {
		return 0;
	}
	if ( $line =~ /^(-+\w+)/ ) {
		$boundary = $1;
		@params = split($boundary, $line);
	}

	foreach $param (@params) {
		if ( $param =~ /^--/ ) { last; }
		$param =~ s/^(\r\n|\r|\n)//;
		$param =~ s/(\r\n|\r|\n)$//;
		if ( $param =~ /^Content-Disposition: form-data; name="([^"]*?)"; filename="([^"]*?)"(\r\n|\r|\n)/ ) {
			$Hfilename = $2; # これはアップしたファイル名
			if ($Hfilename =~ /\\/) {
				$Hfilename = (split(/\\/, $Hfilename))[-1];
			}
			$param =~ s/^Content-Disposition:(.+?)(\r\n|\r|\n)Content-Type:(.+?)(\r\n\r\n|\r\r|\n\n)//i;
			$param =~ s/(\r\n|\r)/\n/g;
			@Hcontents = split(/\n/, $param); # これがファイル本体のデータ
		} elsif ( $param =~ /^Content-Disposition: form-data; name="([^"]*?)"(\r\n|\r|\n)/ ) { #"
			$name = $1;
			$param =~ s/^Content-Disposition:(.+?)(\r\n\r\n|\r\r|\n\n)//i;
			if($name eq 'Upload') {
				$HmainMode = 'upload';
				$HinputPassword = htmlEscape($param);
				$HdefaultPassword = $HinputPassword;
			}
		}
	}
	return ($HmainMode eq 'upload') ? 1 : 0;
}

#----------------------------------------------------------------------
# アップロード
#----------------------------------------------------------------------
sub dataUpload {

	my $kind = '';
	if(checkSpecialPassword($HdefaultPassword)) {
		if($Hfilename =~ /^([0-9]+)_save.${HsubData}/) {
			$HcurrentID = $1;
			$kind  = 'save';
			$mode = 1;
		} elsif($Hfilename =~ /^([0-9]+)_lose.${HsubData}/) {
			$HcurrentID = $1;
			$kind  = 'lose';
			$mode = 2;
		}
	}
	if($kind eq '') {
		&error("ファイルに問題があります。");
	}
	# 内部IDとの整合性(違う場合外部IDに変更)
	$Hcontents[3] = $HcurrentID if($Hcontents[3] != $HcurrentID);

	my $dir = ($kind eq 'lose') ? $HfightdirName : $HsavedirName;
	my $flag = 0;
	if(open(LIN, "${dir}/${Hfilename}")) {
		# 同名ファイルを読み込み 0島名,1オーナー名,7パスワードをチェック
		chomp(my @line = <LIN>);
		close(LIN);
		if(($line[0] ne $Hcontents[0]) || ($line[1] ne $Hcontents[1]) || ($line[7] ne $Hcontents[7])) {
			# 新しいIDの割り当て
			my($dn, %dnset);
			opendir(DIN, "${dir}/");
			# バックアップデータ
			while($dn = readdir(DIN)) {
				if($dn =~ /^([0-9]+)_${kind}.${HsubData}/) {
					$dnset{$1} = 1;
				}
			}
			closedir(DIN);
			foreach (1..100) {
				if(!$dnset{$_}) {
					$HcurrentID = $_ ;
					last;
				}
			}
			# 内部IDの変更
			if($Hcontents[3] != $HcurrentID) {
				$Hcontents[3] = $HcurrentID
			} else {
				# 割り当てに失敗
				&error("IDの割り当てに失敗しました。");
			}
		} else {
			$flag = 1;
		}
	} elsif(!opendir(DIN, "${dir}/")) {
		# 保存ディリクトリのチェック
		mkdir("${dir}", $HdirMode);
	} else {
		closedir(DIN);
	}

	my $file = "${HcurrentID}_${kind}.${HsubData}";
	my $tmpfile = "tmp_${HcurrentID}_${kind}.${HsubData}";

	open(FILE, ">${dir}/${tmpfile}");
	binmode FILE;
	foreach (@Hcontents) {
		print FILE $_ . "\n";
	}
	close(FILE);

	# 本来の名前にする
	unlink("${dir}/${file}") if($flag);
	rename("${dir}/${tmpfile}", "${dir}/${file}");

	print "Location: ${HthisFile}?ViewLose=${HdefaultPassword}\n\n";
	exit(0); # 終了
}

#---------------------------------------------------------------------
# エラー出力
#---------------------------------------------------------------------
sub error {
	print qq{Content-type: text/html; charset=EUC-JP\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n\n};

	out(<<END);
<HTML><HEAD><TITLE>ERROR!</TITLE></HEAD>
$Body<DIV ID='BodySpecial'>
$HtempBack2
<HR>
$_[0]
<HR>
</DIV>
</BODY></HTML>
END
	exit(0);

}

1;