#----------------------------------------------------------------------
# Ȣ����� ver2.30
# Ȣ�����󡦥⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Ȣ�����������
#----------------------------------------------------------------------
# �ᥤ��
sub hakoSkinMain {

	my($Hskinflag);
	if($HskinName eq '' || $HskinName eq "${HcssDir}/$HcssDefault"){
		$Hskinflag = '<span class=attention>̤����</span>';
	} elsif($HskinName =~ /${HcssDir}\/([^\)]*)/ ) {
		$Hskinflag = $HcssFile{$1};
	} else {
		$Hskinflag = '<span class=attention>̤����</span>';
	}

	my $select_list;
	foreach (keys %HcssFile) {
		my $s = ($_ eq $HcssDefault) ? ' selected' : '';
		$select_list .= "<OPTION value='$_'$s>$HcssFile{$_}\n";
	}


	# ����
	unlock();

	out(<<END);
<DIV align='center'>$HtempBack</DIV><BR>
<DIV ID='hakoSkin'>
<H1>Ȣ�����������</H1>
<table border width=50%><tr><td class='N'>
��Ȣ��������ѹ����ơ��������ʥ��󥿡��ե������ˡ�<br>
����ʬž���ˤ����Ѥ�������m(_ _)m
</td></tr></table>
<table border=0 width=50%><tr><td class="M">
���ߤ�����<B>[</b> ${Hskinflag} <B>]</B>
<form action=$HthisFile method=POST>
<SELECT NAME="SKIN">$select_list</SELECT>
<INPUT TYPE="submit" VALUE="����" name=SKINSET>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="SKIN" value="del">
<INPUT TYPE="submit" VALUE="�����������" name=SKINSET>
</form>
</td></tr></table>
</DIV>
END
}

1;

###----------###
### Ƴ����ˡ ###
###----------###
### �����Τ�HTML������ʬ�˥������륷���Ȥ�class��id�����ꤷ�ʤ����
###     Ƴ�����Ƥ��̣������ޤ���(^^;;

### ��Ƭ��#��Ȥäƥ��ԥڡ�###��Ƴ���ˤĤ��ƤΥ����ȤʤΤǥ��ԥ�����


### ������ʬ���ɲ�
## CSS���֤��ǥ��쥯�ȥ�
#$HcssDir = "$HbaseDir";
## �ǥե����CSS�ե������̾��
#$HcssDefault = 'style.css';
#
## Ȣ�����������
#%HcssFile = (
#	"$HcssDefault" => 'Default', # 'CSS�ե�����̾' => '������̾'���ɲá���,�פ��դ�˺������
#);

### �ᥤ��⡼��ʬ����ʬ���ɲ�
#} elsif($HmainMode eq 'hakoskin') {
#	# Ȣ�����������
#	require('./hako-skin.cgi');
#	hakoSkinMain();

### CGI���ɤߤ�����ʬ���ɲ� sub cgiInput���main mode�μ�����ʬ
#	} elsif($getLine =~ /Skin=([0-9]*)/) {
#		$HmainMode = 'hakoskin';

### CGI���ɤߤ�����ʬ���ɲ� sub cgiInput��
#	if($line =~ /SKIN=([^\&]*)\&/) {
#		my($flag) = $1;
#		if(($flag eq 'del') || ($flag eq '')){
#			$flag = "${HcssDir}/$HcssDefault";
#		} else {
#			$flag = "${HcssDir}/" . $flag;
#		}
#		$HskinName = $flag;
#	}

### cookie���Ϥ��ɲ�
#	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
#		$HskinName = $1;
#	}

### cookie���Ϥ��ɲ�
#	if($HskinName) {
#		$cookie .= "Set-Cookie: ${HthisFile}SKIN=($HskinName) $info";
#	}

### �إå����ɲ� sub tempHeader���print(out)��������(�������sub tempHeaderJava�ˤ��ɲ�)
#	if($HskinName ne '' ){
#		$baseSKIN = $HskinName;
#	} else {
#		$baseSKIN = "${HcssDir}/$HcssDefault";
#	}

### �إå����ɲ�  sub tempHeader���BASE HREF�β���������ɲ�(�������sub tempHeaderJava�ˤ��ɲ�)
#<link rel="stylesheet" type="text/css" href="${baseSKIN}">

### �إå����ȥåץڡ����Υ����ʬ���ɲ�
#	out(qq|[<A href="$HthisFile?Skin=0">Ȣ�����������</A>] |);
### out��Ȥ�ʤ��Ƥ⡢[<A href="$HthisFile?Skin=0">Ȣ�����������</A>]��HTML��˵��Ҥ����褦�ˤ���Ф褤