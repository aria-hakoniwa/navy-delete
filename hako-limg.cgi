#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �����Υ��������ꡦ�⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �����Υ���������
#----------------------------------------------------------------------
# �ᥤ��
sub localImgMain {

	my($Himfflag);
	if($HimgLine eq '' || $HimgLine eq $HimageDir){
		$Himfflag = "<span class='attention'>̤����</span>";
	} else {
		$Himfflag = $HimgLine;
	}
	# ����
	unlock();

   out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='localImage'>
<H1>�����Υ���������</H1>
<table border width=50%><tr><td class='N'>
������ž���ˤ�륵���С��ؤ���٤�ڸ���������Ǥʤ������ʤ��Υѥ�����ˤ��������ƤӽФ��Τǡ�ɽ�����ԡ��ɤ�����Ū�˥��åפ��ޤ���<br>
��������<B><a href="$localImg">����</a></B>�����������ɤ��ơ����ĤΥե�����˲��ष����������ǡ�land0.gif�פ���ꤷ�Ʋ�������<br>
�����������ɽ������ʤ���硤���󥿡��ͥåȥ��ץ����ο���Ѥߥ����Ȥ�"${HbaseDir}"���ɲä��Ƥ���������<br>
���ܤ�����<B><a href="$imageExp">�����Υڡ���</a></B>������������
</td></tr></table>
<table border=0 width=50%><tr><td class="M">
���ߤ�����<B>[</b> ${Himfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="����" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Mac�桼������<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="����" name=IMGSET><BR>
<FONT SIZE=-1>Mac�����ϡ����������Ѥ��Ʋ�������</FONT>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="�����������" name=IMGSET>
</form>
</td></tr></table>
</DIV>
END
}

1;

###----------###
### Ƴ����ˡ ###
###----------###

### ��Ƭ��#��Ȥäƥ��ԥڡ�###��Ƴ���ˤĤ��ƤΥ����ȤʤΤǥ��ԥ�����

### �ᥤ��⡼��ʬ����ʬ���ɲ�
#} elsif($HmainMode eq 'localimg') {
#	# �����Υ���������
#	require('./hako-limg.cgi');
#	localImgMain();

### CGI���ɤߤ�����ʬ���ɲ� sub cgiInput���main mode�μ�����ʬ
#	} elsif($getLine =~ /Limg=([0-9]*)/) {
#		$HmainMode = 'localimg';

### CGI���ɤߤ�����ʬ���ɲ� sub cgiInput��
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

### cookie���Ϥ��ɲ�
#	if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
#		$HimgLine = $1;
#	}

### cookie���Ϥ��ɲ�
#	if($HimgLine) {
#		$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
#	}

### �إå����ɲ� sub tempHeader���print(out)��������(�������sub tempHeaderJava�ˤ��ɲ�)
#	if($HimgLine ne '' ){
#		$baseIMG = $HimgLine;
#	} else {
#		$baseIMG = $HimageDir;
#	}

### �إå����ɲ�  sub tempHeader���BASE HREF���ѹ�(�������sub tempHeaderJava���ѹ�)
#<BASE HREF="$baseIMG/">

### �إå����ȥåץڡ����Υ����ʬ���ɲ�
#	out(qq|[<A href="$HthisFile?Limg=0">�����Υ���������</A>] |);
### out��Ȥ�ʤ��Ƥ⡢[<A href="$HthisFile?Limg=0">�����Υ���������</A>]��HTML��˵��Ҥ����褦�ˤ���Ф褤