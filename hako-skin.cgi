#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 箱庭スキン・モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 箱庭スキンの設定
#----------------------------------------------------------------------
# メイン
sub hakoSkinMain {

	my($Hskinflag);
	if($HskinName eq '' || $HskinName eq "${HcssDir}/$HcssDefault"){
		$Hskinflag = '<span class=attention>未設定</span>';
	} elsif($HskinName =~ /${HcssDir}\/([^\)]*)/ ) {
		$Hskinflag = $HcssFile{$1};
	} else {
		$Hskinflag = '<span class=attention>未設定</span>';
	}

	my $select_list;
	foreach (keys %HcssFile) {
		my $s = ($_ eq $HcssDefault) ? ' selected' : '';
		$select_list .= "<OPTION value='$_'$s>$HcssFile{$_}\n";
	}


	# 開放
	unlock();

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='hakoSkin'>
<H1>箱庭スキンの設定</H1>
<table border width=50%><tr><td class='N'>
　箱庭スキンを変更して、お好きなインターフェイスに！<br>
　気分転換にご利用くださいm(_ _)m
</td></tr></table>
<table border=0 width=50%><tr><td class="M">
現在の設定<B>[</b> ${Hskinflag} <B>]</B>
<form action=$HthisFile method=POST>
<SELECT NAME="SKIN">$select_list</SELECT>
<INPUT TYPE="submit" VALUE="設定" name=SKINSET>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="SKIN" value="del">
<INPUT TYPE="submit" VALUE="設定を解除する" name=SKINSET>
</form>
</td></tr></table>
</DIV>
END
}

1;

###----------###
### 導入方法 ###
###----------###
### 注！本体のHTML出力部分にスタイルシートのclassやidを設定しなければ
###     導入しても意味がありません(^^;;

### 行頭の#をとってコピペ、###は導入についてのコメントなのでコピペ不要


### 設定部分に追加
## CSSを置くディレクトリ
#$HcssDir = "$HbaseDir";
## デフォルトCSSファイルの名前
#$HcssDefault = 'style.css';
#
## 箱庭スキンの設定
#%HcssFile = (
#	"$HcssDefault" => 'Default', # 'CSSファイル名' => 'スキン名'で追加。「,」の付け忘れに注意
#);

### メインモード分岐部分に追加
#} elsif($HmainMode eq 'hakoskin') {
#	# 箱庭スキンの設定
#	require('./hako-skin.cgi');
#	hakoSkinMain();

### CGIの読みこみ部分に追加 sub cgiInput内のmain modeの取得部分
#	} elsif($getLine =~ /Skin=([0-9]*)/) {
#		$HmainMode = 'hakoskin';

### CGIの読みこみ部分に追加 sub cgiInput内
#	if($line =~ /SKIN=([^\&]*)\&/) {
#		my($flag) = $1;
#		if(($flag eq 'del') || ($flag eq '')){
#			$flag = "${HcssDir}/$HcssDefault";
#		} else {
#			$flag = "${HcssDir}/" . $flag;
#		}
#		$HskinName = $flag;
#	}

### cookie入力に追加
#	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
#		$HskinName = $1;
#	}

### cookie出力に追加
#	if($HskinName) {
#		$cookie .= "Set-Cookie: ${HthisFile}SKIN=($HskinName) $info";
#	}

### ヘッダに追加 sub tempHeader内のprint(out)処理以前(※あればsub tempHeaderJavaにも追加)
#	if($HskinName ne '' ){
#		$baseSKIN = $HskinName;
#	} else {
#		$baseSKIN = "${HcssDir}/$HcssDefault";
#	}

### ヘッダに追加  sub tempHeader内のBASE HREFの下あたりに追加(※あればsub tempHeaderJavaにも追加)
#<link rel="stylesheet" type="text/css" href="${baseSKIN}">

### ヘッダかトップページのリンク部分に追加
#	out(qq|[<A href="$HthisFile?Skin=0">箱庭スキンの設定</A>] |);
### outを使わなくても、[<A href="$HthisFile?Skin=0">箱庭スキンの設定</A>]がHTML内に記述されるようにすればよい