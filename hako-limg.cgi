#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 画像のローカル設定・モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 画像のローカル設定
#----------------------------------------------------------------------
# メイン
sub localImgMain {

	my($Himfflag);
	if($HimgLine eq '' || $HimgLine eq $HimageDir){
		$Himfflag = "<span class='attention'>未設定</span>";
	} else {
		$Himfflag = $HimgLine;
	}
	# 開放
	unlock();

   out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='localImage'>
<H1>画像のローカル設定</H1>
<table border width=50%><tr><td class='N'>
　画像転送によるサーバーへの負荷を軽減するだけでなく、あなたのパソコンにある画像を呼び出すので、表示スピードが飛躍的にアップします。<br>
　画像は<B><a href="$localImg">ここ</a></B>からダウンロードして、１つのフォルダに解凍し、下の設定で「land0.gif」を指定して下さい。<br>
　それだけで表示されない場合，インターネットオプションの信頼済みサイトへ"${HbaseDir}"を追加してください。<br>
　詳しくは<B><a href="$imageExp">説明のページ</a></B>をご覧下さい。
</td></tr></table>
<table border=0 width=50%><tr><td class="M">
現在の設定<B>[</b> ${Himfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Macユーザー用<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET><BR>
<FONT SIZE=-1>Macの方は、こちらを使用して下さい。</FONT>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="設定を解除する" name=IMGSET>
</form>
</td></tr></table>
</DIV>
END
}

1;

###----------###
### 導入方法 ###
###----------###

### 行頭の#をとってコピペ、###は導入についてのコメントなのでコピペ不要

### メインモード分岐部分に追加
#} elsif($HmainMode eq 'localimg') {
#	# 画像のローカル設定
#	require('./hako-limg.cgi');
#	localImgMain();

### CGIの読みこみ部分に追加 sub cgiInput内のmain modeの取得部分
#	} elsif($getLine =~ /Limg=([0-9]*)/) {
#		$HmainMode = 'localimg';

### CGIの読みこみ部分に追加 sub cgiInput内
#	if($line =~ /IMGLINEMAC=([^&]*)\&/){
#		my($flag) = $1;
#		if($flag eq ''){
#			$flag = $HimageDir;
#		} else {
#			$flag =~ s/ /%20/g;
#			$flag = 'file:///' . $flag;
#		}
#		$HimgLine = $flag;
#	} elsif($line =~ /IMGLINE=([^&]*)\&/){
#		my($flag) = $1;
#		$flag =~ tr/\\/\//;
#		if(($flag eq 'deletemodenow') || ($flag eq '')){
#			$flag = $HimageDir;
#		} else {
#			$flag =~ s/\/[\w\.]+\.gif$//g;
#			$flag = 'file:///' . $flag;
#		}
#		$HimgLine = $flag;
#	}

### cookie入力に追加
#	if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
#		$HimgLine = $1;
#	}

### cookie出力に追加
#	if($HimgLine) {
#		$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
#	}

### ヘッダに追加 sub tempHeader内のprint(out)処理以前(※あればsub tempHeaderJavaにも追加)
#	if($HimgLine ne '' ){
#		$baseIMG = $HimgLine;
#	} else {
#		$baseIMG = $HimageDir;
#	}

### ヘッダに追加  sub tempHeader内のBASE HREFを変更(※あればsub tempHeaderJavaも変更)
#<BASE HREF="$baseIMG/">

### ヘッダかトップページのリンク部分に追加
#	out(qq|[<A href="$HthisFile?Limg=0">画像のローカル設定</A>] |);
### outを使わなくても、[<A href="$HthisFile?Limg=0">画像のローカル設定</A>]がHTML内に記述されるようにすればよい