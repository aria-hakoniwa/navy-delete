#----------------------------------------------------------------------
# Ȣ����� ���� JS ver7.xx
# ����������⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �Ƽ�������
# (����ʹߤ���ʬ�γ������ͤ�Ŭ�ڤ��ͤ��ѹ����Ƥ�������)
#----------------------------------------------------------------------

# ����������̾(�ر�̾)�����ˤĤ���ι�(��λ����������رĥ⡼�ɡ����Х��Х�⡼�ɡ��ȡ��ʥ��ȥ⡼�ɶ�������)
# �ι�
@HwinnerTitle = (
	'COMPLETE��', # �����ƥॳ�����
	'�����Ƽ�',
	);
# �ޡ���
@HwinnerMark = ( # �����ξ��
	'trophy2[gold].gif', # �����ƥॳ�����
	'king[yellow].gif',
	); # ��å������Ǻླྀ http://homepage2.nifty.com/yoshi-m/sozai/
#@HwinnerMark = ( # �ƥ����Ȥξ��
#	'��COMPLETE����', # �����ƥॳ�����
#	'�ھ��ԡ���'
#	);
# �ޡ���ɽ���򣱤Ĥ����ˤ��뤫��(0:���ʤ���1:����)
$HviewMarkOne = 0;

# ���������õ����Τϴ����ͤ�����(0:��������1:�Ϥ�)
# �ʴ����ͤ����ξ��� $HjoinGiveupTurn �򾮤������Ƥ���������
$HadminJoinOnly = 0;

# ������Ͽ���줿��γ�ȯ����
# �ʳ�ȯ���֤ϡ�¾����ؤα����¾����ؤι��⡢���ػߤ�����
$HdevelopTurn = 50;

# �������ޥ�ɼ�ư���ϥ�������ʳ�ȯ���֡�
$HdevelopGiveupTurn = 4;

# �������ޥ�ɼ�ư���ϥ������
$HgiveupTurn = 24;

# ��������򸫤Ĥ���ľ������֥�������ʲ����������֤���Ƥ������Ȥˤ��뤫��
$HjoinGiveupTurn = $HgiveupTurn - 3;

# ��������򸫤Ĥ������Υ�������
$HjoinComment = '(̤��Ͽ)';
# ��������ȯ�����Τޤޤξ�硢�����ͤ�������ˤ��롩(0:���ʤ�)
$HjoinCommentPenalty = 0; # 1�ʤ�ȯ��������μ��Υ����󹹿�����Ƚ�ꡣ2�ʾ��ͱͽ��⤿���뤳�Ȥ���ǽ��
# ���ε�ǽ�����������ɽ�����뤫��
#    ���ʤ����ϡ�""
#    ������ϡ�"��§�Ȥ��Ƽ����դ��ʤ�", "<a href='��'>�Ǽ���</a>�Ǽ����դ���", "<a href="mailto:��>�᡼��</a>�Ǽ����դ���"�ʤ�
#$HjoinCommentPenaltyStr = "�����դ��ޤ���ȯ�����衢<B>�����</B>���ޤ���"; # �ش����ͤ�������������ϡ�(�������������)�ס�
$HjoinCommentPenaltyStr = "";

# ̵�Ͳ���ư���򡦻���Ƚ�����ǽ�λ���(0:���Ѥ��ʤ���1:����Ƚ�����2��:̵�Ͳ���ư����)
#����������װʳ��Ǥϻ��ǽ����򤷤ʤ���
# ¾����ɸ���δ����伫��(�����оݤ���)�˽и���β��á�������äϳ��ˤʤ���ǡ�
# ¾�礫�鼫����ɸ�����Ƥ������ϡ����Խ�������롣
# 1:����Ƚ�����ξ��
#    �����ͤ�������ˤ��롣
# 2��:̵�Ͳ���ư����ξ��
#    �������ο͸��ǳ�ȯ���֤ˤʤ�(�ֿرĥ⡼�ɡס֥��Х��Х�⡼�ɡס֥ȡ��ʥ��ȥ⡼�ɡפǤϻ����Բ�)
#    ���������͸������ˤʤä���硢���Ϥ�ʿ�Ϥ��ʤ�������פ��Ƥ��ޤ���
$HautoKeeper = 0; # �͸������������ͤ򲼲���ȯư

# ����Ƚ�����ˤ��ִ����ͤ�������פμ�ư������������(0:̵���¡�1��99999998:�������)
$HautoKeeperSetTurn = 24;

# �ִ����ͤ�������פǤ�ǽ�Υ��ޥ�ɤ�����������פʤ���ǽ����򤹤뤫��(0:��������1:�Ϥ�)
$HforgivenGiveUp = 1;

# �ִ����ͤ�������פ���ؤι���(�����ɸ��������ɸ����ߥ����빶��)����Ĥ��뤫��(0:��������1:�Ϥ�)
$HforgivenAttack = 0;

# ���ǽ����Ǻ���������ǡ�����ȡ��ʥ��Ȥ��ԼԤ���Ȥ��ư�����¸���뤫��(0:��������1:�Ϥ���2:�����������¸����)
$HdeadToSaveAsLose = 2;

#----------------------------------------
# ����
#----------------------------------------
# ���ߥ��ޥ�ɤ�Ȥ�����(0:�ػ�)
$HuseCore = 0;

# ���ߤǤ���ΤϿ�����Ͽ���줿��γ�ȯ���֤�����(0:���¤ʤ���1:������Ͽ���줿��γ�ȯ���֤���)
$HuseCoreLimit = 0;

# ��ͭ��ǽ�������
$HcoreMax = 0; # 0:̵����

# �ѵ�������
$HdurableCore = 3; # ������(0�����̾�����99�ޤ�)

# �����������뤫��(1:���롢0:���ʤ�)
$HcoreHide = 0;

# ��������ͭ���ʤ�������פ��롩(��������Ͽ���줿��γ�ȯ���֤����פ��ޤ���)
$HcorelessDead = 0; # 0:���פ��ʤ���1:���פ��롢2:����Ƚ�����ǽȯư(��ư������������$HautoKeeperSetTurn������)

# �����ե������hako-init.cgi������

#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
# �ȥåץڡ�����ɽ��������ο�
# �ʤ������������ʣ���ڡ�����ʬ�����ޤ���
$HviewIslandCount = 10;

# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTurn = 12;

# �Хå����åפ򲿲�ʬ�Ĥ���
$HbackupTimes = 4;

# ȯ�����ݻ��Կ�(10����礭�������ɽ��������ޤ������ο��ͤ�Ĵ�����Ʋ�����)
$HhistoryMax = 100;
# ����ɽ�����κ���ι⤵��
# height�λ����ͤ�Ķ����ȥ�������С���ɽ������ޤ���
$HdivHeight = 120; # <DIV style="overflow:auto; height:${HdivHeight}px;">

# �ꥢ�륿���ޡ��λ���(0:���Ѥ��ʤ���1:���Ѥ���)
$Hrealtimer = 1;

# ��ȯ���̤ǥݥåץ��åץʥӤ�ɽ�����뤫��(0:���Ѥ��ʤ���1:���Ѥ���)
$HpopupNavi = 1;

# �����󥭥󥰤�Ͽ���뤫��(�ܺ������hako-reki.cgi�ǹԤ����Ȥ��Ǥ��ޤ�)
$HuseRekidai = 1;

# �����μ��Ϥ����Ω�ƤǤ���΢�略(�Х�?)�������뤫��(0:���ʤ���1:����)
$HnavyReclaim = 1;

# ����(���ˤ���)�μ��Ϥ����Ω�ƤǤ���΢�略(�Х�?)�������뤫��(0:���ʤ���1:����)
$HmonsterReclaim = 1;

# ST�����ɸ���ST�ߥ�����ȯ�ͤ�΢�略(�Х�?)�������뤫��(0:���ʤ���1:����)
$HattackST = 1;

# ��κǳ��������Ω���ԲĤˤ��뤫��(0:���ʤ���1:����)
# ��ɸ�ΰ�������($HedgeReclaim - 1)�ʲ� �� ($HislandSizeX(orY) - $HedgeReclaim)�ʾ�����������Ω�ƤǤ��ʤ�����Ȥ������ȤǤ���
# ��ʮ�Ф�Φ�Ϥˤʤ뤳�ȤϤ���ޤ���
$HedgeReclaim = 1; # $HislandSizeX(orY)/2���⾮��������������

# ��������ޥå�ɽ����ǽ�ˤ��뤫��(0:���ʤ���1:����)
$HmlogMap = 1;

# ¾�ͤ�����򸫤��ʤ����뤫
# 0 �����ʤ�
# 1 ������
# 2 100�ΰ̤ǻͼθ���
$HhideMoneyMode = 0;

# ���Ϸϥ��ΤޤȤ�˺�ɸ����Ϥ��롩(0:���ʤ� 1:����)
# ���ϡ��Ϥʤ餷�����Ω�ơ����Ȳ��
$HoutPoint = 1;

# ����μ��٥�(��̩)����Ϥ��롩(0:���ʤ� 1:����)
$HbalanceLog = 1;

# JavaScript�ΰ��������ե����벽���뤫��(0:���ʤ� 1:����)
$HextraJs = 0;

#----------------------------------------------------------------------
# ���ޥ�ɴ�Ϣ����
#----------------------------------------------------------------------
# ʣ���Ϸ���(ʣ���Ϸ��Ƚ�ʣ���뵡ǽ���Ϸ���������ζػ�����)
#-------------------------------------------------------------
# �ֹ�����ߡפ�Ȥ�����(0:�ػ�)
$HuseFactory = 0;

# �����������פ�Ȥ�����(0:�ػ�)
$HuseFarm = 0;

# �ֺη��������פ�Ȥ�����(0:�ػ�)
$HuseMountain = 0;

# �ֿ��ӡ�Ȳ�Ρפ�Ȥ�����(0:�ػ�)
$HusePlantSellTree = 1;

# ��®��(���������ʤ�)
#-----------------------
# Ȳ�Τ򥿡������ʤ��ˤ��뤫��(0:���ʤ���1:����)
$HnoturnSellTree = 1;

# �ֹ�®���Ω�ơפ�Ȥ�����(0:�ػ�)
$HuseFastReclaim = 1;

# �ֹ�®����פ�Ȥ�����(0:�ػ�)
$HuseFastDestroy = 1;

# �ֹ�®������ߡפ�Ȥ�����(0:�ػ�)
$HuseFastFactory = 1;

# �ֹ�®���������פ�Ȥ�����(0:�ػ�) ���ȡ��ʥ��ȥ⡼�ɤǻ��ѡ�
$HuseFastFarm = 1;

# �ְ���Ϥʤ餷�פ�Ȥ�����(0:�ػ�) �����Х��Х�⡼�ɤǻ��ѡ�
$HusePrepare3 = 1;
# ��缫ư�Ϥʤ餷��
$precheap  = 10; # �����ܤι��Ϥ�����������ʤ��ο��μ��ι��Ϥ����
$precheap2 =  8; # ���κݤγ��Ψ��8�ˤ����顢2����Ȥ������Ȥˤʤ�ޤ���
#----------------------------------------
# ��ο�����Ͽ��������
#----------------------------------------
# ������Ѥ����줹�뤫��
$HnewIslandSetting = 0;

# �����������
$HcountLandArea     = 32; # Φ�Ϥο�(�̾�:32) ��16��꾮�����ͤˤ��Ƥ����16�ϤǤ��ޤ���
$HcountLandSea      = 16; # ��(����)�ο�(�̾�:16)

$HcountLandWaste    = 8;  # ���Ϥο�(�̾�:8)
$HcountLandForest   = 4;  # ���ο�(�̾�:4)
$HcountLandTown     = 2;  # Į�ο�:̵�Ͳ�����ǽ�Ǥ�ͭ��(�̾�:2 ���Х��Х�:10)
$HcountLandMountain = 1;  # ���ο�(�̾�:1 ���Х��Х�:0)
$HcountLandPort     = 0;  # �����ο�(�̾�:0 ���Х��Х�:0)
$HcountLandBase     = 0;  # ���Ϥο�(�̾�:1 ���Х��Х�:0  �����ѻ��Τ�)

# ���Ϥ�����(���줷�Ƥ⤷�ʤ��Ƥ�ͭ��)
$HvalueLandForest   = 5;  # ���ε���(�̾�:5 ���Х��Х�:10)
$HvalueLandTown     = 5;  # Į�ε���(�̾�:5 ���Х��Х�:100)
$HvalueLandMountain = 0;  # ��(�η���)�ε���(�̾�:0)
#������η����ʣ���Ϸ��ǤϤ���ޤ���
#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
# �ֻ�ⷫ��פǤμ���(�̾�ϡ��Ρ��ޥ�:10, ���Х��Х�:100)
$HdoNothingMoney = 10;

# ������
$HmaximumMoney = 100000;

# ���翩��
$HmaximumFood = 500000;

# �����ñ��
$HunitMoney = '����';

# ������ñ��
$HunitFood = '00�ȥ�';

# �͸���ñ��
$HunitPop = '00��';

# ������ñ��
$HunitArea = '00����';

# �ڤο���ñ��
$HunitTree = '00��';

# �ڤ�ñ�������������
$HtreeValue = 5;

# 1��������������ڤ��ܿ�(ñ��������)�̾��1
$HtreeGrow = 3;

# ̾���ѹ��Υ�����
$HcostChangeName = 500;

# �͸�1ñ�̤�����ο���������
$HeatenFood = 0.2;

# ���äο���ñ��
$HunitMonster = 'ɤ';

# �����Ĵ���ʿ��������μ�����Ψ���̾�졼�Ȥ��Ф�����Ψ��
$HincomeRate = 1;

#----------------------------------------
# �ߥ������Ϣ
#----------------------------------------
# �ߥ�������Ϥ�Ȥ�����(0:�ػ�)
# �ʳ���ΥХ�󥹤�ͤ���ȻȤ�ʤ����Ȥ�侩���ޤ���
$HuseBase = 0;

# ������Ϥ�Ȥ�����(0:�ػ�)
# �ʳ���ΥХ�󥹤�ͤ���ȻȤ�ʤ����Ȥ�侩���ޤ���
$HuseSbase = 0;

# ���Ϥηи���
#----------------------------------------
# �и��ͤκ�����
$HmaxExpPoint = 200; # ������������Ǥ�255�ޤ�

# ��٥�κ�����
$maxBaseLevel  = 5;  # �ߥ��������
$maxSBaseLevel = 3; # �������

# �и��ͤ������Ĥǥ�٥륢�åפ�
@baseLevelUp  = (20, 60, 120, 200); # �ߥ��������
@sBaseLevelUp = (50, 200); # �������

my($num, $cno);
#----------------------------------------
# �ߥ�����
#----------------------------------------
# ST�ߥ������Ȥ�����(0:�ػ�)
$HuseMissileST = 0;

# ������˲��á�������ä����ʤ���С��ߥ������ȯ����ߤˤ��뤫��(0:���ʤ���1:����)
$HtargetMonster = 0;

# �ߥ���������Ƥ����������Ϸ�������ξ�硢̵���ˤ��뤫����0:���ʤ���1:���롢2:ͧ�����̵���ˤ����
$HmissileSafetyZone = 2;
# ̵������̵���ˤʤ��Ψ(%) ��̵������ǽ��ȯư������̤�Ƚ��
$HmissileSafetyInvalidp = 0;

# �ߥ�����μ���(����10����)
### �ߥ�����
$num = 0; # �����ֹ�
$HmissileName[$num] = '�ߥ�����';         # ̾��
$HmissileMsgs[$num] = '��2';            # �ߥ����������
$HmissileCost[$num]    = 20;              # ȯ������
$HmissileTurn[$num]    = 1;               # ���������(ST��Ϣ³���Բ�)
$HmissileDamage[$num]  = 0;               # �˲���(̿����Υ��᡼��) ���ѵ��ϤΤ����Ϸ����оݡ�����ʤ���1�ʤΤǡ�2�ʾ�ο��ͤ����ꤹ����˻��ѡ�
$HmissileErr[$num]     = 2;               # ��(Hex)
$HmissileSpecial[$num] = 0x0;             # °��
# 0x0 �ʤ�
# 0x1 ST(���ƥ륹�ߥ�����)ȯ�ͤ�����̾������ɽ������ޤ���
# 0x2 Φ���˲�(��������(Φ���Ϸ�)������(�����Ϸ�)����)
# 0x4 �������(���Ƥ��������μ��Ͽ��إå����򹶷�)
# 0x10 �Ų�̵��(�в��á��������)
# 0x20 ����̵��(�в��á�������á�����ǽ����ͭ�ϡ����롦�������)

#���������׼��ϲ�Hex�оݤ�����1��2�����ꡣ
$HmissileTerrorHex[$num] = 0;# ������������⤹��ˤ�1Hex:7ȯ��2Hex:19ȯ��ɬ�פǤ������Ū�˹�����������뤳�Ȥˤʤ�ޤ���

### PP�ߥ�����
$num = 1; # �����ֹ�
$HmissileName[$num]      = 'PP�ߥ�����';   # ̾��
$HmissileMsgs[$num]      = '��1';        # ����
$HmissileCost[$num]      = 50;             # ȯ������
$HmissileTurn[$num]      = 1;              # ���������
$HmissileDamage[$num]    = 0;              # �˲��� ������ʤ���1
$HmissileErr[$num]       = 1;              # ��(Hex)
$HmissileSpecial[$num]   = 0x0;            # °��
$HmissileTerrorHex[$num] = 0;              #����������Hex

### ST�ߥ�����
$num = 2; # �����ֹ�
$HmissileName[$num]      = 'ST�ߥ�����';   # ̾��
$HmissileMsgs[$num]      = '��2�����ߤ˷�ĤΤϤ��ޤ��礦'; # ����
$HmissileCost[$num]      = 50;             # ȯ������
$HmissileTurn[$num]      = 0;              # ���������
$HmissileDamage[$num]    = 0;              # �˲��� ������ʤ���1
$HmissileErr[$num]       = 2;              # ��(Hex)
$HmissileSpecial[$num]   = 0x1;            # °��
$HmissileTerrorHex[$num] = 0;              #����������Hex

### Φ���˲���
$num = 3; # �����ֹ�
$HmissileName[$num]      = 'Φ���˲���';   # ̾��
$HmissileMsgs[$num]      = '��2��Φ�˲�(�������Ϣ���������)'; # ����
$HmissileCost[$num]      = 100;            # ȯ������
$HmissileDamage[$num]    = 0;              # �˲��� ������ʤ���1
$HmissileTurn[$num]      = 1;              # ���������
$HmissileErr[$num]       = 2;              # ��(Hex)
$HmissileSpecial[$num]   = 0x2;            # °��
$HmissileTerrorHex[$num] = 0;              #����������Hex

### �Ȼ��ߥ�����
#$num = 4; # �����ֹ�
#$HmissileName[$num]      = '�Ȼ��ߥ�����'; # ̾��
#$HmissileMsgs[$num]      = '��2���������μ���1Hex���˲������Ѥ�1ȯ�������7ȯ�ʾ��ȯ��ǽ�Ϥ����꤬ɬ��'; # ����
#$HmissileCost[$num]      = 100;            # ȯ������
#$HmissileTurn[$num]      = 1;              # ���������
#$HmissileDamage[$num]    = 0;              # �˲��� ������ʤ���1
#$HmissileErr[$num]       = 2;              # ��(Hex)
#$HmissileSpecial[$num]   = 0x4;            # °��
#$HmissileTerrorHex[$num] = 1;              #����������Hex

#----------------------------------------
# �ɱһ���
#----------------------------------------
# ��ͭ��ǽ�������
$HdBaseMax = 10; # 0:̵����

# ���ä�Ƨ�ޤ줿���������뤫��(1:���롢0:���ʤ�)
$HdBaseAuto = 0;

# �ɱһ��ߤ򿹤˵������뤫��(1:���롢0:���ʤ�)
$HdBaseHide = 0;

# ����ι���ϼ�����ɱҷ�(¾����ɱҷ��Ǥʤ�����)�����ƤǤ���褦�ˤ��뤫�����Ĥޤ��ɱҤ��ʤ��Ȥ������ȡ�(�ɱҤ�̵����)
# (0:���Ƥ��ʤ�(�ɱҤ���Ȥ�������)��1:����ι���Τ����ơ�2:ͧ��������ꤷ�Ƥ���Ƥ�����ι�������ơ�3:ͧ��������ꤷ�Ƥ�����ι�������ơ�4:ͧ��������ꤷ�Ƥ�����ι����ͧ��������ꤷ�Ƥ���Ƥ�����ι��������)
$HdBaseSelfNoDefenceNV = 1; # ���⹶��
$HdBaseSelfNoDefenceMS = 1; # �ߥ����빶��
$HdBaseSelfNoDefenceMA = 1; # ���äΥߥ����빶��

# �ѵ�������
$HdurableDef = 5; # ������(0�����̾����98)
$HdefLevelUp = 3; # �ѵ��Ϥ�����������Ͱʾ�ˤʤ���ɱ��ϰϤ����إå����ˤʤ�ޤ���
# ����������ꤷ�Ƥ�����ˡ����������������Ͽ��̡�99�פ���ꤷ�ʤ���Фʤ�ޤ���
#     0��1���ѵ��Ϥκ����ͤ�1�Ǥ�����0�����ɲ÷��ߤǼ�����1���ȡ�99�פǼ����Ǥ���
$HdefExplosion = 100; # �����ο��̤��99�װʳ��ˤ����������ѹ���100�ʾ�ˤ���м����Ǥ��ʤ��ʤ�ޤ���
#----------------------------------------
# �ҳ�
#----------------------------------------
# �̾�ҳ�ȯ��Ψ(��Ψ��0.1%ñ��)
$HdisEarthquake = 0;  # �Ͽ�
$HdisTyphoon    = 20; # ����
$HdisMeteo      = 15; # ���
$HdisHugeMeteo  = 0;  # �������
$HdisEruption   = 0; # ʮ��
$HdisFire       = 100; # �к�
$HdisMaizo      = 10; # ��¢��

# ����
$HdisTsunami     = 0; # ȯ��Ψ
$HdisTsunamiDmax = 0;  # ���Ȥ�������Ϳ������᡼���κ�����
$HdisTsunamiFsea = 20; # �������ѥե饰������򲼲�������ȯ����Ψ���⤯�ʤ롣

# ��������
$HdisFallBorder = 90; # �����³��ι���(Hex��)
$HdisFalldown   = 30; # ���ι�����Ķ�������γ�Ψ

#----------------------------------------
# �����顦����
#----------------------------------------
# �������Ȥ�����(0:�ػ�) ���Ȥ���硢bouha.gif��ɬ�פǤ���
$HuseBouha = 0; # ��ͭ��ǽ�������

# �����Ȥ�����(0:�ػ�) ���Ȥ���硢seamine.gif��ɬ�פǤ���
$HuseSeaMine = 10; # ���ֲ�ǽ�������
# �˲��Ϥκ�����
$HmineDamageMax = 9;
# ����ε���ǥ��᡼��������뤫��(0:�����롢1:�����ʤ���2:ͧ���������ʤ�)
$HmineSelfDamage = 2;

#----------------------------------------
# ����
#----------------------------------------
# ���Ĥμ���
$HoilMoney = 1000;

# ���ļ����������ˤ���(0:���ʤ���1��:�Ǿ��ͤ����ꤹ�롣$HoilMoney�������ͤˤʤ�)
$HoilMoneyMin = 0;

# ���Ĥθϳ��Ψ
$HoilRatio = 40;

#----------------------------------------
# �ԻԷ�����
#----------------------------------------
# ̾��
#@HlandTownName  = ('¼', 'Į', '�Ի�', '���Ի�', '�����Ի�', 'Ķ�����Ի�');
@HlandTownName  = ('����Ի�', '1���Ի�','2���Ի�','3���Ի�','4���Ի�','5���Ի�','6���Ի�','7���Ի�','8���Ի�','9���Ի�','10���Ի�');

# ����
#@HlandTownImage = ('land3.gif', 'land4.gif', 'land5.gif', 'land41.gif', 'land42.gif', 'land43.gif');
@HlandTownImage = ('landtown0.gif','landtown1.gif','landtown2.gif','landtown3.gif','landtown4.gif',
                   'landtown5.gif','landtown6.gif','landtown7.gif','landtown8.gif','landtown9.gif','landtown10.gif');

# ��󥯥��åפ�ɬ�פ��Ϸ����ͤκǾ���(�Ϸ����ͤ�����ʾ�ˤʤ�ȥ�󥯥��å�)
#@HlandTownValue  = (   0, 30, 100, 200, 300, 400);
@HlandTownValue  = (   0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000);

# ��̱��������ξ��(��̱�����������ԻԤε��ϤǤϤʤ��ơ����������Ϳ��θ��ˤʤ����)
#@HachiveValueMax   = (  50, 50,  50,  50,  50,  50); # ���Ǥ��ԻԷϤξ��
@HachiveValueMax   = (900,800,700,600,500,400,300,200,100,50,0); # ���Ǥ��ԻԷϤξ��
$HachivePlainsMax  = 10; # ʿ�Ϥؤμ���������(�̾�:10)
$HachivePlainsLoss = 5;  # ʿ�ϼ���������Υ�(�̾�:5)
# ��Max10,Loss5�Ǽ¼�ʿ�Ϥؤμ�������Ϻ���5�Ǥ�����̱���������ʿ�Ϥ��ԻԷϤˤʤ뤿��5����̱���ä��ޤ���

# ��Ĺ�κ�����(�Ϸ����� Max:1000000000)
#$HvalueLandTownMax = 500; # �̾� 200(20000�͡�
$HvalueLandTownMax = 1000;

# �͸�����������10���Ⱥ���1000�͡�
#@Haddpop        = (  10, 10, 10, 10, 10,  0); # �̾�(¼, Į, �Ի�)=(10, 10, 0)
#@HaddpopPropa   = (  30, 30, 20, 20, 20, 10); # Ͷ�׳�ư�� �̾�(¼, Į, �Ի�)=(30, 30, 10)
#@HaddpopSD      = (  40, 40, 20, 20, 20,  0); # ���Х��Х볫ȯ���� �̾�(40, 40, 0)
#@HaddpopSDpropa = (  60, 60, 30, 30, 30, 10); # ���Х��Х볫ȯ���� Ͷ�׳�ư��(60, 60, 10)
#@HaddpopSA      = (   5,  5,  5,  5,  5,  0); # ���Х��Х���Ʈ���� �̾�(5, 5, 0)
#@HaddpopSApropa = (  10, 10, 10, 10, 10,  3); # ���Х��Х���Ʈ���� Ͷ�׳�ư��(10, 10, 3)
@Haddpop        = (  10, 50, 30,0,0,0,0,0,0,0,0);
@HaddpopPropa   = (  50, 30, 10,5,3,0,0,0,0,0,0);
@HaddpopSD      = (  40, 40,  0);
@HaddpopSDpropa = (  60, 60, 10);
@HaddpopSA      = (   5,  5,  0);
@HaddpopSApropa = (  10, 10,  3);

# ������­�ξ��ο͸�������(�ޥ��ʥ�����)
@HreductionPop  = ( -10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10); # �̾� -30

#  �ݥåץ��åץʥӲ�����ʬ(����ˤ�äƽ񤭴�����ɬ�פ���)
$HnaviExp.=<<"END";
TOWN0  = "����Ի�";
TOWN1  = "1���Ի�";
TOWN2  = "2���Ի�";
TOWN3  = "3���Ի�";
TOWN4  = "4���Ի�";
TOWN5  = "5���Ի�";
TOWN6  = "6���Ի�";
TOWN7  = "7���Ի�";
TOWN8  = "8���Ի�";
TOWN9  = "9���Ի�";
TOWN10 = "10���Ի�";


END

# ¼��ȯ��Ψ�ʡ��
$HtownGlow = 50; # �̾� 20 �ȡ��ʥ��� 25

# �������⡦�ߥ����빶��̿��������ǹӤ��Ϥˤʤ餺�Իԥ�󥯤�������褦�ˤ��뤫��(1:���롢0:���ʤ�)
$HtownStepDown = 1;
# ��󥯣��ޤǡ�¼��Į�ˤϰ����˲�����ޤ���
#----------------------------------------
# ʣ���Ϸ�
#----------------------------------------
# ʣ���Ϸ���Ȥ�����(0:�ػ�)
$HuseComplex = 1;

#  �����󹹿���°��
# �֥���������׺Ǿ��ͤȺ�����
@HcomplexRinMoney = (10, 100);
# �֥�������ϡ׺Ǿ��ͤȺ�����
@HcomplexRinFood = (10, 100);
# ���Ͼ�ǽ�ϡ׼��ϲ�Hex�β��á�������ä�ֻ����뤫��
$HcomplexFieldHex = 1;

# ʣ���Ϸ����Ϸ�����(����32����)
#-------------------------------
### ����
#$num = 0; # �����ֹ�

# ̾��
#$HcomplexName[$num] = '����';

# ʣ���Ϸ��β����ե�����
#$HcomplexImage[$num] = 'land7.gif';

# ��ͭ(����)��ǽ�����(0:̵����)
#$HcomplexMax[$num] = 0;

# ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # 3�ΤȤ���̾��
#$HcomplexPretendImage[$num] = ''; # 3�ΤȤ��β���
#$HcomplexPretendNavi[$num]  = ''; # �ݥåץ��åץʥӲ��� 'SEA0'�Ȥ�'FOREST'�Ȥ�

# ��󥯥��å�����
#$HcomplexLevelKind[$num] = 'food'; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
#$HcomplexLevelValue[$num] = [0, 20, 40]; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
#$HcomplexSubName[$num] = ['����(Lv1)', '����(Lv2)', '����(Lv3)'];# ̾��
#$HcomplexSubImage[$num] = ['land7.gif', 'land7.gif', 'land7.gif'];# ����

# ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore2[$num] = []; # ʣ���Ϸ�����߲�ǽ�ʡ��̼��ʣ���Ϸ�($HlandComplex)�פμ���(ʣ���ξ��ϡ�[1, 3]�Τ褦�˥���ޤǶ��ڤ�)  ���̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������

# ������ե饰����:���߻���1�Ȥ��ƥ����󹹿����Ȥ�+1�������
#$HcomplexTPCmax[$num] = 0;  # ������(Max500) 
#$HcomplexTPname[$num] = ''; # ̾�� ..���Ȥ��С�'�ڤο�','���Ի�'
#$HcomplexTPrate[$num] = 0;  # ɽ����Ψ �ե饰�ˤ�����Ψ�򤫤������ͤ�ɽ����
#$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾�� ..���Ȥ��С�'00��',"$HunitPop"
#$HcomplexTPkind[$num] = ''; # �û���($island->{KIND}��KIND��ʬ) ..���Ȥ��С�'','pop' ��ñ�̤򤽤��뤳�ȡ�
#$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 

#  �����ե饰����
#$HcomplexFPbase[$num]  = 10;     # ����� ($HunitPop x 10 ����)
#$HcomplexFPplus[$num]  = 2;      # �ɲ��� ($HunitPop x 10 ����)
#$HcomplexFPCmax[$num]  = 20;     # �ɲò�ǽ��� Max50(�ǽ��ͤϡ�����͡��ɲ��ͣ��ɲò�ǽ����ˤʤ�ޤ�)
#$HcomplexFPkind[$num]  = 'farm'; # �û���($island->{KIND}��KIND��ʬ) ..���Ȥ��С�'','pop' ��ñ�̤򤽤��뤳�ȡ�

#  ���ե饰����
#$HcomplexMPbase[$num]  = 0;  # ����� ($HunitPop x 10 ����)
#$HcomplexMPplus[$num]  = 0;  # �ɲ��� ($HunitPop x 10 ����)
#$HcomplexMPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50(�ǽ��ͤϡ�����͡��ɲ��ͣ��ɲò�ǽ����ˤʤ�ޤ�)
#$HcomplexMPkind[$num]  = ''; # �û���($island->{KIND}��KIND��ʬ) ..���Ȥ��С�'','pop' ��ñ�̤򤽤��뤳�ȡ�

#  �����󹹿���°��
#$HcomplexAttr[$num] = 0x401;
# 0x1 ���Ϥ�ʿ�Ϥ�¼��ȯ������(countGrowȽ��:����(Į)�Ȥ��ƥ�����Ȥ����)
# 0x2 �кҤ��ﳲ���ɤ�����(���䵭ǰ���Ʊ��)
# 0x4 �������ﳲ���ɤ�����(���䵭ǰ���Ʊ��)
# 0x10 �Ͼ�ȯ��:���á�������ä򲡤��Ĥ֤��ֻ�����
# 0x20 ����2Hex�Υߥ������ɱҡ��ɱҴ��Ϥ�Ʊ���ε�ǽ��
# 0x40 ����2Hex�δ��⹶���ɱҡ��ɱҴ��Ϥ�Ʊ���ε�ǽ��
# 0x100 ��������ι����оݤˤʤ�
# 0x200 �дϹ���ι����оݤˤʤ�
# 0x400 ���Ϲ���ι����оݤˤʤ�
# 0x1000 ���������
# 0x2000 ���������

### �ʲ�3���ܤϸ��������Բ�
# �֥���������׺Ǿ��ͤȺ�����
# �֥�������ϡ׺Ǿ��ͤȺ�����
# ���Ͼ�ǽ�ϡ׼��ϲ�Hex�β��á�������ä�ֻ����뤫��


#  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
#   prepare:���ϡ��Ϥʤ餷��, reclaim:���Ω�Ƹ�, destroy:�����,
#   attack:����(����)�����,
#   stepdown:���Ƥ�������1����˲����줺�˥�󥯥����󤹤롣(���᡼��)x(stepdown)���ɲõ��Ϥ��鸺���������
#   move:���ð�ư��ե饰 ��[�Ϸ�(0:Φ,1:��), �Ϸ�����(0:����, 1:����)],
#   earthquake:�Ͽ̸�, typhoon:������, fire:�кҸ�, tsunami:���ȸ�, starve:˽ư��
#   falldown:����������, eruption:ʮ�и�(�濴��ɬ�����ʤΤǼ�����������), meteo:��и�,
#   wide1:����ҳ�(�ɱһ��߼���������ߥ����롦�������)��1Hex����
#   wide2:����ҳ�(�ɱһ��߼���������ߥ����롦�������)��2Hex����
#  �������˵��Ҥ��ʤ����ϡ��˲��Ǥ��ʤ�(����ʤ�)��
#$HcomplexAfter[$num]  = { # ����
#	'prepare'    => [$HlandPlains, 0],
#	'reclaim'    => '',
#	'destroy'    => [$HlandSea,    1],
#	'attack'     => [$HlandWaste,  1],
#	'stepdown'   => 0,
#	'move'       => [0, 0],
#	'earthquake' => '',
#	'typhoon'    => [$HlandPlains, 0],
#	'fire'       => '',
#	'tsunami'    => [$HlandWaste,  0],
#	'starve'     => [$HlandWaste,  0],
#	'falldown'   => [$HlandSea,    1],
#	'eruption'   => [$HlandWaste,  0],
#	'meteo'      => [$HlandSea,    0],
#	'wide1'      => [$HlandSea,    1],
#	'wide2'      => [$HlandWaste,  0],
#};

#  �ݥåץ��åץʥӲ�����ʬ(''�δ֤˵��ҡ�����ˤ�äƽ񤭴�����ɬ�פ���)
#$HnaviExp.= "COMPLEX$num = '';\n";

### ����
#$num = 0; # �����ֹ�
#$HcomplexName[$num] = '����'; # ̾��
#$HcomplexImage[$num] = 'land8.gif';# ʣ���Ϸ��β����ե�����
#$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
## ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # ̾��
#$HcomplexPretendImage[$num] = ''; # ����
#$HcomplexPretendNavi[$num]  = ''; # �ʥ�
## ��󥯥��å�����
#$HcomplexLevelKind[$num] = 'money'; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
#$HcomplexLevelValue[$num] = [0, 50, 80]; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
#$HcomplexSubName[$num] = ['����(Lv1)', '����(Lv2)', '����(Lv3)'];# ̾��
#$HcomplexSubImage[$num] = ['land8.gif', 'land8.gif', 'land8.gif'];# ����
## ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 200]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore2[$num] = []; # ʣ���Ϸ����̼�Τ������ֹ�ǻ���(ʣ���ξ��ϡ�[1, 3]�Τ褦�˥���ޤǶ��ڤ�)��Ʊ���ʣ���Ϸ��ϵ�������
## ������ե饰����
#$HcomplexTPCmax[$num] = 0;  # ������
#$HcomplexTPname[$num] = ''; # ̾��
#$HcomplexTPrate[$num] = 0;  # ɽ����Ψ
#$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾��
#$HcomplexTPkind[$num] = ''; # �û���
#$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
##  �����ե饰����
#$HcomplexFPbase[$num]  = 0;  # �����
#$HcomplexFPplus[$num]  = 0;  # �ɲ���
#$HcomplexFPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
#$HcomplexFPkind[$num]  = ''; # �û���
##  ���ե饰����
#$HcomplexMPbase[$num]  = 30;  # �����
#$HcomplexMPplus[$num]  = 10;  # �ɲ���
#$HcomplexMPCmax[$num]  =  7;  # �ɲò�ǽ��� Max50
#$HcomplexMPkind[$num]  = 'factory'; # �û���
##  �����󹹿���°��
#$HcomplexAttr[$num] = 0x400;
##  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
#$HcomplexAfter[$num]  = {
#	'prepare'    => [$HlandPlains, 0],
#	'reclaim'    => '',
#	'destroy'    => [$HlandSea,    1],
#	'attack'     => [$HlandWaste,  1],
#	'stepdown'   => 0,
#	'move'       => [0, 0],
#	'earthquake' => [$HlandWaste,  0],
#	'typhoon'    => '',
#	'fire'       => [$HlandWaste,  0],
#	'tsunami'    => [$HlandWaste,  0],
#	'starve'     => [$HlandWaste,  0],
#	'falldown'   => [$HlandSea,    1],
#	'eruption'   => [$HlandWaste,  0],
#	'meteo'      => [$HlandSea,    0],
#	'wide1'      => [$HlandSea,    1],
#	'wide2'      => [$HlandWaste,  0],
#};
#$HnaviExp.= "COMPLEX$num = '';\n"; # �ݥåץ��åץʥӲ�����ʬ

### �η���
#$num = 2; # �����ֹ�
#$HcomplexName[$num] = '�η���'; # ̾��
#$HcomplexImage[$num] = 'land15.gif';# ʣ���Ϸ��β����ե�����
#$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
## ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # ̾��
#$HcomplexPretendImage[$num] = ''; # ����
#$HcomplexPretendNavi[$num]  = ''; # �ʥ�
## ��󥯥��å�����
#$HcomplexLevelKind[$num] = ''; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
#$HcomplexLevelValue[$num] = ''; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
#$HcomplexSubName[$num] = '';# ̾��
#$HcomplexSubImage[$num] = '';# ����
## ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
#$HcomplexBefore[$num]  = [[$HlandMountain, 0, 200]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore2[$num] = [4]; # ʣ���Ϸ����̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������
## ������ե饰����
#$HcomplexTPCmax[$num] = 0;  # ������
#$HcomplexTPname[$num] = ''; # ̾��
#$HcomplexTPrate[$num] = 0;  # ɽ����Ψ
#$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾��
#$HcomplexTPkind[$num] = ''; # �û���
#$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
##  �����ե饰����
#$HcomplexFPbase[$num]  = 0;  # �����
#$HcomplexFPplus[$num]  = 0;  # �ɲ���
#$HcomplexFPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
#$HcomplexFPkind[$num]  = ''; # �û���
##  ���ե饰����
#$HcomplexMPbase[$num]  =  5;  # �����
#$HcomplexMPplus[$num]  =  5;  # �ɲ���
#$HcomplexMPCmax[$num]  = 39;  # �ɲò�ǽ��� Max50
#$HcomplexMPkind[$num]  = 'mountain'; # �û���
##  �����󹹿���°��
#$HcomplexAttr[$num] = 0x0;
##  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
#$HcomplexAfter[$num]  = {
#	'prepare'    => '',
#	'reclaim'    => '',
#	'destroy'    => [$HlandWaste,  0],
#	'attack'     => '',
#	'stepdown'   => 0,
#	'move'       => '',
#	'earthquake' => '',
#	'typhoon'    => '',
#	'fire'       => '',
#	'tsunami'    => '',
#	'starve'     => '',
#	'falldown'   => '',
#	'eruption'   => '',
#	'meteo'      => [$HlandWaste,  1],
#	'wide1'      => [$HlandSea,    1],
#	'wide2'      => '',
#};
#$HnaviExp.= "COMPLEX$num = '';\n"; # �ݥåץ��åץʥӲ�����ʬ

## ��
$num = 2; # �����ֹ�
$HcomplexName[$num] = '��'; # ̾��
$HcomplexImage[$num] = 'land6.gif';# ʣ���Ϸ��β����ե�����
$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
# ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # ̾��
$HcomplexPretendImage[$num] = ''; # ����
$HcomplexPretendNavi[$num]  = ''; # �ʥ�
# ��󥯥��å�����
$HcomplexLevelKind[$num] = ''; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
$HcomplexLevelValue[$num] = ''; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
$HcomplexSubName[$num] = '';# ̾��
$HcomplexSubImage[$num] = '';# ����
# ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
$HcomplexBefore[$num]  = [[$HlandPlains,0, 0], [$HlandTown, 0, 1000]];# ʣ���Ϸ�($HlandComplex)�ʳ�
$HcomplexBefore2[$num] = []; # ʣ���Ϸ����̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������
# ������ե饰����
$HcomplexTPCmax[$num] = 500;  # ������
$HcomplexTPname[$num] = '�ڤο�'; # ̾��
$HcomplexTPrate[$num] = 1;  # ɽ����Ψ
$HcomplexTPunit[$num] = '00��'; # ���ȤˤĤ�̾��
$HcomplexTPkind[$num] = ''; # �û���
$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
#  �����ե饰����
$HcomplexFPbase[$num]  = 0;  # �����
$HcomplexFPplus[$num]  = 0;  # �ɲ���
$HcomplexFPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
$HcomplexFPkind[$num]  = ''; # �û���
#  ���ե饰����
$HcomplexMPbase[$num]  = 0;  # �����
$HcomplexMPplus[$num]  = 0;  # �ɲ���
$HcomplexMPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
$HcomplexMPkind[$num]  = ''; # �û���
#  �����󹹿���°��
$HcomplexAttr[$num] = 0x406;
#  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
$HcomplexAfter[$num]  = {
	'prepare'    => [$HlandPlains, 0],
	'reclaim'    => '',
	'destroy'    => [$HlandSea,    1],
	'attack'     => [$HlandWaste,  1],
	'stepdown'   => 0,
	'move'       => [0, 0],
	'earthquake' => '',
	'typhoon'    => '',
	'fire'       => '',
	'tsunami'    => '',
	'starve'     => '',
	'falldown'   => [$HlandSea,    1],
	'eruption'   => [$HlandWaste,  0],
	'meteo'      => [$HlandSea,    0],
	'wide1'      => [$HlandSea,    1],
	'wide2'      => [$HlandWaste,  0],
};
$HnaviExp.= "COMPLEX$num = '1${HunitTree}������${HtreeValue}${HunitMoney}';\n"; # �ݥåץ��åץʥӲ�����ʬ

### ¤��
#$num = 0; # �����ֹ�
#$HcomplexName[$num] = '¤��'; # ̾��
#$HcomplexImage[$num] = 'land11.gif';# ʣ���Ϸ��β����ե�����
#$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
## ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # ̾��
#$HcomplexPretendImage[$num] = ''; # ����
#$HcomplexPretendNavi[$num]  = ''; # �ʥ�
## ��󥯥��å�����
#$HcomplexLevelKind[$num] = ''; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
#$HcomplexLevelValue[$num] = ''; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
#$HcomplexSubName[$num] = '';# ̾��
#$HcomplexSubImage[$num] = '';# ����
## ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore2[$num] = [2]; # ʣ���Ϸ����̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������
## ������ե饰����
#$HcomplexTPCmax[$num] = 0;  # ������
#$HcomplexTPname[$num] = ''; # ̾��
#$HcomplexTPrate[$num] = 0;  # ɽ����Ψ
#$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾��
#$HcomplexTPkind[$num] = ''; # �û���
#$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
##  �����ե饰����
#$HcomplexFPbase[$num]  = 0;  # �����
#$HcomplexFPplus[$num]  = 0;  # �ɲ���
#$HcomplexFPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
#$HcomplexFPkind[$num]  = ''; # �û���
##  ���ե饰����
#$HcomplexMPbase[$num]  = 0;  # �����
#$HcomplexMPplus[$num]  = 0;  # �ɲ���
#$HcomplexMPCmax[$num]  = 1;  # �ɲò�ǽ��� Max50
#$HcomplexMPkind[$num]  = ''; # �û���
##  �����󹹿���°��
#$HcomplexAttr[$num] = 0x6;
##  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
#$HcomplexAfter[$num]  = {
#	'prepare'    => '',
#	'reclaim'    => '',
#	'destroy'    => [$HlandWaste,  0],
#	'attack'     => '',
#	'stepdown'   => 0,
#	'move'       => '',
#	'earthquake' => '',
#	'typhoon'    => '',
#	'fire'       => '',
#	'tsunami'    => '',
#	'starve'     => '',
#	'falldown'   => '',
#	'eruption'   => '',
#	'meteo'      => [$HlandWaste,  1],
#	'wide1'      => [$HlandSea,    1],
#	'wide2'      => '',
#};
#$HnaviExp.= "COMPLEX$num = '';\n"; # �ݥåץ��åץʥӲ�����ʬ

### ������
$num = 0; # �����ֹ�
$HcomplexName[$num] = '������'; # ̾��
$HcomplexImage[$num] = 'land21.gif';# ʣ���Ϸ��β����ե�����
$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
# ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # ̾��
$HcomplexPretendImage[$num] = ''; # ����
$HcomplexPretendNavi[$num]  = ''; # �ʥ�
# ��󥯥��å�����
$HcomplexLevelKind[$num] = 'food'; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
$HcomplexLevelValue[$num] = [0, 300, 600, 900, 1200]; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
$HcomplexSubName[$num] = ['������(Lv1)', '������(Lv2)', '������(Lv3)', '������(Lv4)', '������(Lv5)'];# ̾��
$HcomplexSubImage[$num] = ['land21.gif', 'land21.gif', 'land21.gif', 'land21.gif', 'land21.gif'];# ����
# ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 1000], [$HlandFarm, 0, 50]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# ʣ���Ϸ�($HlandComplex)�ʳ�
$HcomplexBefore2[$num] = [0, 1]; # ʣ���Ϸ����̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������
# ������ե饰����
$HcomplexTPCmax[$num] = 0;  # ������
$HcomplexTPname[$num] = ''; # ̾��
$HcomplexTPrate[$num] = 0;  # ɽ����Ψ
$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾��
$HcomplexTPkind[$num] = ''; # �û���
$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
#  �����ե饰����
$HcomplexFPbase[$num]  = 100;  # �����
$HcomplexFPplus[$num]  = 50;  # �ɲ���
$HcomplexFPCmax[$num]  = 28;  # �ɲò�ǽ��� Max50
$HcomplexFPkind[$num]  = 'farm'; # �û���
#  ���ե饰����
$HcomplexMPbase[$num]  = 0;  # �����
$HcomplexMPplus[$num]  = 0;  # �ɲ���
$HcomplexMPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
$HcomplexMPkind[$num]  = ''; # �û���
#  �����󹹿���°��
$HcomplexAttr[$num] = 0x2405;
#  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
$HcomplexAfter[$num]  = {
	'prepare'    => [$HlandPlains, 0],
	'reclaim'    => '',
	'destroy'    => [$HlandSea,    1],
	'attack'     => [$HlandWaste,  1],
	'stepdown'   => 1,
	'move'       => [0, 0],
	'earthquake' => '',
	'typhoon'    => [$HlandPlains, 0],
	'fire'       => '',
	'tsunami'    => [$HlandWaste,  0],
	'starve'     => [$HlandWaste,  0],
	'falldown'   => [$HlandSea,    1],
	'eruption'   => [$HlandWaste,  0],
	'meteo'      => [$HlandSea,    0],
	'wide1'      => [$HlandSea,    1],
	'wide2'      => [$HlandWaste,  0],
};
$HnaviExp.= "COMPLEX$num = '';\n"; # �ݥåץ��åץʥӲ�����ʬ

### �繩��
$num = 1; # �����ֹ�
$HcomplexName[$num] = '�繩��'; # ̾��
$HcomplexImage[$num] = 'land22.gif';# ʣ���Ϸ��β����ե�����
$HcomplexMax[$num] = 0; # ��ͭ(����)��ǽ�����(0:̵����)
# ��������(0:�����ʤ���1:���Τդꡤ2:���Τդꡤ3:�ʤˤ��̤Τ��)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # ̾��
$HcomplexPretendImage[$num] = ''; # ����
$HcomplexPretendNavi[$num]  = ''; # �ʥ�
# ��󥯥��å�����
$HcomplexLevelKind[$num] = 'money'; # ��󥯥��åפΤ�Ȥˤʤ�ե饰�μ���('turn'��'food'��'money')
$HcomplexLevelValue[$num] = [0, 500, 1000, 1500, 20000]; # ��󥯥��åפ�ɬ�פʥե饰�ͤκǾ���
$HcomplexSubName[$num] = ['�繩��(Lv1)', '�繩��(Lv2)', '�繩��(Lv3)', '�繩��(Lv4)', '�繩��(Lv5)'];# ̾��
$HcomplexSubImage[$num] = ['land22.gif', 'land22.gif', 'land22.gif', 'land22.gif', 'land22.gif'];# ����
# ʣ���Ϸ�����߲�ǽ���Ϸ����ѿ��ǵ���([�Ϸ�,�Ϸ���min,�Ϸ���max], [�Ϸ�,�Ϸ���min,�Ϸ���max],������) ��$HlandComplex�ϵ�������)
$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 1000], [$HlandFactory, 0, 100]];# ʣ���Ϸ�($HlandComplex)�ʳ�
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# ʣ���Ϸ�($HlandComplex)�ʳ�
$HcomplexBefore2[$num] = [0, 1]; # ʣ���Ϸ����̼�Τ������ֹ�ǻ��ꡣƱ���ʣ���Ϸ��ϵ�������
# ������ե饰����
$HcomplexTPCmax[$num] = 0;  # ������
$HcomplexTPname[$num] = ''; # ̾��
$HcomplexTPrate[$num] = 0;  # ɽ����Ψ
$HcomplexTPunit[$num] = ''; # ���ȤˤĤ�̾��
$HcomplexTPkind[$num] = ''; # �û���
$HcomplexTPhide[$num] = 0;  # �Ѹ��Ԥ���ߤ��ʤ����뤫(0:���ʤ���1:����) 
#  �����ե饰����
$HcomplexFPbase[$num]  = 0;  # �����
$HcomplexFPplus[$num]  = 0;  # �ɲ���
$HcomplexFPCmax[$num]  = 0;  # �ɲò�ǽ��� Max50
$HcomplexFPkind[$num]  = ''; # �û���
#  ���ե饰����
$HcomplexMPbase[$num]  = 300;  # �����
$HcomplexMPplus[$num]  = 100;  # �ɲ���
$HcomplexMPCmax[$num]  = 17;  # �ɲò�ǽ��� Max50
$HcomplexMPkind[$num]  = 'factory'; # �û���
#  �����󹹿���°��
$HcomplexAttr[$num] = 0x1400;
#  �˲����줿�����Ϸ����ѿ��ǵ���('�˲��μ���' => [�Ϸ�, �Ϸ�����])
$HcomplexAfter[$num]  = {
	'prepare'    => [$HlandPlains, 0],
	'reclaim'    => '',
	'destroy'    => [$HlandSea,    1],
	'attack'     => [$HlandWaste,  1],
	'stepdown'   => 1,
	'move'       => [0, 0],
	'earthquake' => [$HlandWaste,  0],
	'typhoon'    => '',
	'fire'       => [$HlandWaste,  0],
	'tsunami'    => [$HlandWaste,  0],
	'starve'     => [$HlandWaste,  0],
	'falldown'   => [$HlandSea,    1],
	'eruption'   => [$HlandWaste,  0],
	'meteo'      => [$HlandSea,    0],
	'wide1'      => [$HlandSea,    1],
	'wide2'      => [$HlandWaste,  0],
};
$HnaviExp.= "COMPLEX$num = '';\n"; # �ݥåץ��åץʥӲ�����ʬ


# ʣ���Ϸ����ޥ������(����50����)
#---------------------------------
#  0x0:����(����)�Τ�
#  0x1:������ꥻ�å�
#  0x2:�����ɲ�
#  0x4:����ɲ�

#  ������ꥻ�åȻ�(�ե饰��0�ˤʤä����)�ν���
#   �Ϸ��Ѳ�
#    �Ѳ�����Ϸ����Ϸ�����
#    �ޤ���������ե饰�����ͤ�0�ξ���̵���ʤΤ�''�Ǥ褤
#$HcomplexComTFRL[$cno] = ["", ""]; # �Ѳ����ʤ�����''�Ǥ褤(0�ϥ��ᡣ)
#   ���������Ͻ���(�ե饰���ͤ��Ф�����Ψ)
#    type:����food,���money�Τ����줫
#    ratio:��Ψ����(food�ξ���$HunitFood���Ф�����Ψ��money�ξ���$HunitMoney���Ф�����Ψ)
#    log:���������� �̾����normal,�ޤȤ����matome,
#    logstr:������������� '����','����'�ʤ�
#$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' };

### ����������
$cno = 0; # �����ֹ�
$HcomplexComName[$cno] = '����������'; # ̾��
$HcomplexComMsgs[$cno] = '���ȸ��Ȥʤ���ߡ�����50����(ʣ����)'; # ����
$HcomplexComKind[$cno] = 0;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 200;  # ���ޥ������
$HcomplexComTurn[$cno] = 1;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x2; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # �Ѳ����ʤ�����''�Ǥ褤(0�ϥ��ᡣ)
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' };

### ��®����������
$cno = 1; # �����ֹ�
$HcomplexComName[$cno] = '��®����������'; # ̾��
$HcomplexComMsgs[$cno] = '���������ʤ���������������(ʣ����)'; # ����
$HcomplexComKind[$cno] = 0;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 3000; # ���ޥ������
$HcomplexComTurn[$cno] = 0;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x2; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # ���������Ͻ���

### �繩�����
$cno = 2; # �����ֹ�
$HcomplexComName[$cno] = '�繩�����'; # ̾��
$HcomplexComMsgs[$cno] = '��⸻�Ȥʤ���ߡ�����100��(ʣ����)'; # ����
$HcomplexComKind[$cno] = 1;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 1000; # ���ޥ������
$HcomplexComTurn[$cno] = 1;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x4; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # ���������Ͻ���

### ��®�繩�����
$cno = 3; # �����ֹ�
$HcomplexComName[$cno] = '��®�繩�����'; # ̾��
$HcomplexComMsgs[$cno] = '���������ʤ����繩����ߡ�(ʣ����)'; # ����
$HcomplexComKind[$cno] = 1;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 3000; # ���ޥ������
$HcomplexComTurn[$cno] = 0;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x4; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # ���������Ͻ���

### ����
$cno = 5; # �����ֹ�
$HcomplexComName[$cno] = '����'; # ̾��
$HcomplexComMsgs[$cno] = 'ʿ�ϡ�Į�ϤǼ¹Բ�ǽ��'; # ����
$HcomplexComKind[$cno] = 2;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 50; # ���ޥ������
$HcomplexComTurn[$cno] = 1;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x0; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # ���������Ͻ���

### ��®����
$cno = 6; # �����ֹ�
$HcomplexComName[$cno] = '��®����'; # ̾��
$HcomplexComMsgs[$cno] = 'ʿ�ϡ�Į�ϤǼ¹Բ�ǽ��'; # ����
$HcomplexComKind[$cno] = 2;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 3000; # ���ޥ������
$HcomplexComTurn[$cno] = 0;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x0; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = ["", ""]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # ���������Ͻ���

### Ȳ��
$cno = 4; # �����ֹ�
$HcomplexComName[$cno] = 'Ȳ��'; # ̾��
$HcomplexComMsgs[$cno] = '���Ǽ¹Ԥ����ʿ�Ϥ��Ѳ�����ⲽ��'; # ����
$HcomplexComKind[$cno] = 2;   # �оݤȤʤ�ʣ���Ϸ��μ���
$HcomplexComCost[$cno] = 0; # ���ޥ������
$HcomplexComTurn[$cno] = 0;   # ���������(0:�ʤ���1:����)
$HcomplexComFlag[$cno] = 0x1; # �оݤȤʤ�ե饰
$HcomplexComTFRL[$cno] = [$HlandPlains, 0]; # ������ꥻ�åȻ��ν���
$HcomplexComTFInCome[$cno] = { 'type' => 'money', 'ratio' => 5, 'log' => 'normal', 'logstr' => '����' }; # ���������Ͻ���


#----------------------------------------
# ����
#----------------------------------------
# �и��ͤκ�����
$HmaxExpNavy = 120; # ������������Ǥ�255�ޤ�

# ��٥�κ�����
$maxNavyLevel = 0;  # ����
# �и��ͤ������Ĥǥ�٥륢�åפ�
#              Lv2   3   4   5   6    7    8    9   10
@navyLevelUp = (0);
#                    Lv2  4  6  8  10
@HnavyFirePlus  = (0); # ���ù�����(������٥�ǥ��å�)
#                 Lv1  3  5  7   9
@HnavyMaxHpPlus = (0); # �����ѵ���(�����٥�ǥ��å�)

# �ĳ���ѻ��˶����ȯ��������Ψ
$HnavyProbWreckGold = 20; # 20%

# �������ͭ���ʤ���ؤϴ�����ɸ��Ǥ��ʤ����롩��0:���ʤ���1:�����
# �������۹��Ȥ�����ξ�硢�����۹��Ǥ��ʤ��ʤ�ޤ�
$HnofleetNotAvail = 0;

# ¾����ɸ���δ������뤹�뤫����0:���ʤ���1:�����
# ��0�ʤ鼫ʬ����ˤ������Τ���뤹��or�ɸ�����礬�����ͧ��������ꤷ�Ƥ�������뤹���
$HnavySupplyFlag = 0;

# ���⤷���������Ȥ������ϰϤˤ����硢����(����)�⤢�ꡩ��0:�ʤ���1:�����
$HnavySelfAttack = 0;

# ������������Ƥ����������Ϸ�������ξ�硢̵���ˤ��뤫����0:���ʤ���1:���롢2:ͧ�����̵���ˤ����
$HnavySafetyZone = 2;
# ̵������̵���ˤʤ��Ψ(%) ��̵������ǽ��ȯư������̤�Ƚ��
$HnavySafetyInvalidp = 0;

# ��������Ϸ��ˤ�빶���ͥ����(�ǥե����)
@Hpriority = ('Navy', 'Monster', 'HugeMonster', 'Arm',    'Pop',  'Food',   'Money',  'Other');
@HpriStr   = ('����', '����',    '�������',    '������', '�Ի�', '������', '��⸻', '����¾');
# Navy:���� Monster:���� HugeMonster:�������
# Arm:�������,�ߥ��������,�ϥ�ܥ�,�ɱһ���(�������ʤ����)
# Pop:Į�� Food:���� Money:��������,���� Other:��,��ǰ��
# ����������򥫥�åݤˤ���ȹ���Ǥ��ʤ��ʤäƤ��ޤ��ޤ���
$Hnearfar = 2; # 0:�Ǥ�ᤤ�Ϸ�������ɸ��õ�� 1:�Ǥ���Ϸ�������ɸ��õ�� 2:���������������ɸ��õ��

# ��Ũ��(�����ͥ����)���ѹ�����Ĥ��뤫����0:���ʤ���1:�����
$HusePriority = 1;

# �ְ��ƹ���ץ��ޥ�ɤ�Ȥ�����(0:�ػ�)
# �����������������ˤ�Ĵ����ι����оݤ����ꤹ�륳�ޥ�ɤǤ���
$HuseTarget = 0;

# ����ʳ��ˤ��������ѵ��Ϥ�ɽ������뤫����0:�ʤ���1:�����
$HnavyShowInfo = 1;

# ��ͭ��ǽ������(���ꤷ�ʤ�����0)
$HnavyMaximum = 0;
# �����⤢�������ͭ��ǽ������(���ꤷ�ʤ�����0)
$HfleetMaximum = 0; # ���ꤹ���硢�������Թ�塢4�ܤ������ͤ�$HnavyMaximum��Ķ���������褤�Ȼפ�
# �����������������ͭ��ǽ������(���ꤷ�ʤ�����0)
$HportRetention = 4; # �����鷳�������䤷�Ƥ���ͭ��ǽ��������Ķ���뤳�ȤϤʤ�
#----------------------------------------
# ����
#----------------------------------------
# ��¤(�и���)��٥�����
$HmaxComNavyLevel = 7;  # ��٥�κ�����(���Ѥ��ʤ�����0�ˤ���)
# ��������򤽤Τޤ޻Ȥ����ϡ���Ρ֥�٥�κ����͡פ�10�ˤ��ޤ���
#                   2   3   4   5    6    7    8     9    10
@HcomNavyBorder = (5, 10, 20, 40, 80, 150); # ɬ�פ�������и���(�ƥ�٥�κǾ��͡���٥룱�ϡ�0��)
#           ��٥� 1   2   3   4   5   6   7   8   9  10
@HcomNavyNumber = (4, 6, 11, 13, 15, 16, 17); # ��¤��ǽ�ʴ����ֹ�κ�����
# ��¤����ˤϷ����ηи��ͥ�٥��ɬ�פˤ��롩(0:���ʤ���1:����)
# �ַ��������ܤ����������Ƿ�¤��ǽ�פ�����򤷤ʤ����ϡ���äȤ�ᤤ�����Υ�٥���ǧ���ޤ���
$HmaxComPortLevel = 0;

# �������ܤ����������Ǥ����������¤�Ǥ��ʤ�(0:���ʤ���1:����)
$HnavyBuildFlag = 1;

# �����ˤ��ư�ġ��ɸ��ġ�(0:���ʤ���1:����)
$HnavyMoveAsase = 1;

# �ĳ������ե�����
$HnavyImageZ = 'land18.gif';

# �ü�ǽ�ϴ�Ϣ����
#���ǰ�ǽ�ϡ��ǰ�ǽ�ϤΤ���������ɸ�����Ƥ��ʤ���ؤϱ�����ޥ�ɤ��Ĥ����ʤ����롩(0:���ʤ���1:����)
$HtradeAbility = 0;
#����������״��ϡ���ư��ĤǤʤ��Ƥ��������ꤹ�롩(0:���ʤ���1:����)
$HsuicideAbility = 1;

# ��������(����32����)
#---------------------------------
$HnavyImage3 = 'navy99_0.gif'; #��¤��β����϶��� 

### ����
$num = 0; # �����ֹ�
# ̾��
$HnavyName[$num] = '����';
# ǽ��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��(���ꤷ�ʤ�����0)
$HnavyHP[$num]        = 10;     # ����ѵ���
$HnavyMaxHP[$num]     = 20;     # �ǽ��ѵ���(Max15) ��٥륢�åפˤ�������ѵ��Ϥκ����ͤ��θ����������ꤷ�Ƥ���������
$HnavyDamage[$num]    = 0;      # �˲���(̿����Υ��᡼��) ���ѵ��ϤΤ����Ϸ����оݡ�����ʤ���1�ʤΤǡ�2�ʾ�����������ꤹ����˻��ѡ�
$HnavyFire[$num]      = 0;      # ����� ��٥륢�åפˤ�����ù������κ����ͤ��θ����������ꤷ�Ƥ���������
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 0;     # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 6000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 0;      # �������˻ĳ����Ĥ��Ψ(%) �����������̵���ˤʤ�ޤ�
$HnavySpecial[$num]   = 0x10008;    # �ü�ǽ��
$HnavyBuildTurn[$num] = 12;     # �������� ����ɬ�פʤ�����1�Ǥʤ�0��������ư�ե饰�������ϤȽ����ζ��̤ˤ�Ȥ�
$HnavyCruiseTurn[$num] = 0;     # ��³������ ���ꤷ�ʤ��ʤ�0 ���ꤷ�����Ϥ��Υ�����ФĤȵ��� �Ҷ����ե饰�ˤ�Ȥ�
$HnavyNoMove[$num]    =  1;     # ư���ʤ�����ե饰 �����������ɱҡ��η����ϡ�������

# �ü�ǽ�Ϥ����Ƥϡ�
# 0x0 �äˤʤ�
# 0x1 ��ư��®��(����2�ޥ���ư)
# 0x2 ��ư���ȤƤ�®��(���粿�ޥ���ư���뤫����)
# 0x4 ���夹��
# 0x8 ��
# 0x10 ��԰�ư���祳�ޥ�ɼ¹����˰�ư��
# 0x20 ����2Hex�Υߥ������ɱҡ��ɱҴ��Ϥ�Ʊ���ε�ǽ��
# 0x40 ����2Hex�δ��⹶���ɱҡ��ɱҴ��Ϥ�Ʊ���ε�ǽ��
# 0x80 ���ϡ���ư���(��礬��ư��ؼ�)
# 0x100 ��������
# 0x200 �дϹ���
# 0x400 ���Ϲ���
# 0x800 ����ư�ʼ�ʬ��°�������δ��Ϥ��ܻؤ��ư�ư��
# 0x800 �ж�������ѹ�
# 0x1000 ����ϡ����������дϡ��ɸ���ǽ��ñ�إå���
# 0x2000 ��ˤ�ϡ����дϡ����ϡ��ɸ��ǽ�ʥᥬ�إå���
# 0x4000 �дϹ�����дϡ����ϡ��ɸ��ǽ��ñ�إå���
# 0x8000 ����õ��(����������ȯ�����ݻ���Ȥ��̤�Ĵ�����ۡ����פ��ꡢ����л�ʮ�Ф���)
#        ���Ĥ����Ĥ���ʤ���礽��Ⱦʬ�γ�Ψ�Ǻ���ȯ��������ˤ���Ⱦʬ�γ�Ψ�ǳ���л�ʮ�С�
#        Ĵ������西����ַ������ѡ�ȯ����Ψ�ס����׳�Ψ��ȯ����Ψ��10ʬ��1��
# 0x8000 �ж�������ѹ�
# 0x10000 ���ǽ�ϡ�¾����ɸ��桢���ϣ��إå����μ���(orͧ����)�����ȼ�ʬ������Ԥ��ˢ�����(orͧ����)�����ʳ����Ǥ��ʤ�����ǻȤ�
# 0x20000 �ǰ�ǽ�ϡʱ�����ޥ�ɤ�Ȥ�����ɸ��ˢ�����������1:���������ξ��˻Ȥ��������ѹ��������ǰפ�Ԥ���
# 0x40000 ��±ǽ�� ���ɸ�������Ρ����줫�鿩�������줫�����å����1Hex��50%,2Hex30%,3Hex10%
# 0x80000 Φ�Ϸ���ǽ�ϡʹ���(������)�ذ�ư��ǽ����ư��������ˡ����̤ι��Ϥذ�ư���褦�Ȥ��������������ˤ����
# 0x100000 ����õ��ǽ�� 0x8000���餳������ѹ�
# 0x200000 �۾�����μ���
# 0x400000 ���̤���μ���
# 0x800000
# 0x1000000 ��ɸ����ǽ�ϡʹ������˺�Ũ����ľ����
# 0x2000000 �������������ꤹ��ǽ��($HsafetyZone������Ǽ��ϡ�ͧ����Ϥˤ��������ꤷ�Ƥ��ޤ��ޤ�)
# 0x4000000 ̿��ΨUP:�����������Ψ��1Hex�̤��
# 0x8000000 ����ǽ��:���Ϥ����Ȥ��ﳲ������
# 0x10000000 �˲���:������(̿����Υ��᡼��) �����ȯ����Ψ�Ⱥ����˲��Ϥ��������ꡣ�����ȯ�����ʤ����ϡ��˲��Ϥ�ǽ������⤷����1��
# 0x20000000 ������� (���Ƥ��������μ��Ͽ��إå����򹶷�)
# 0x40000000
# 0x80000000

# �ü�ǽ�ϴ�Ϣ����
# �ֵ���ϡסִ�ˤ�ϡסִϺܵ��ϡ׳����ι���̾
#    ['0x1000��̾��', '0x2000��̾��', '0x4000��̾��'] (ǽ�ϤΤʤ����϶���Ǥ褤)
#   �֡���Ԥ��ޤ����פȤ������ˤʤ�ޤ���
$HnavyFireName[$num] = ['', '', '',''];
#�����夹��װ�ư������夹���Ψ(1%ñ��)
$HsubmarineSurface[$num] = 0;
#������ư�״��Ϥ�õ���ϰ� Ⱦ�£��ޥ��ʤ��ޤ깭���ϰϤ�õ���ʤ��褦�ˤ��Ƥ���������;�פʥ�������٤ˤʤ�ޤ���
$HnavyTowardRange[$num] = 3;
#�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$Hoilp[$num] = 2;
#�����ǽ�ϡ����Ϥ�ͭ���ϰ� Ⱦ�£��ޥ��ʤ��ޤ깭���ϰϤ�õ���ʤ��褦�ˤ��Ƥ���������;�פʥ�������٤ˤʤ�ޤ���
$HnavySupplyRange[$num] = 0;
#�ֳ�±ǽ�ϡ׼��ϲ�Hex������졢������Ф��Ƴ�±�԰٤�Ԥ�������1��3�����ꡣ4�ʾ�ˤϤǤ��ޤ���
$HpiratesHex[$num] = 2;
#��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$Hfirehexp[$num] = 50;
#������ǽ�ϡ׼��ϲ�Hex�����Ȥ����뤫����1��3�����ꡣ4�ʾ�ˤϤǤ��ޤ���
$HbouhaHex[$num] = 2;
#���˲���:����������ȯ����Ψ�Ⱥ����˲���
$HdamageMax[$num] = 1; # �����˲���
$Hdamagep[$num]   = 0; # ���ȯ����Ψ(1%ñ��)
#���������׼��ϲ�Hex�оݤ�����1��2�����ꡣ
$HnavyTerrorHex[$num] = 0; # ������������⤹��ˤ�1Hex:7ȯ��2Hex:19ȯ��ɬ�פǤ������Ū�˹�����������뤳�Ȥˤʤ�ޤ���

# �ݥåץ��åץʥӲ�����ʬ(''�δ֤˵��ҡ�����ˤ�äƽ񤭴�����ɬ�פ���)
$HnaviExp.= "NAVY$num = '�����ܤ��뿼������<BR>��������¤��ǽ'\n";

# �����β����ե�����
$HnavyImage[$num]  = 'navy0.gif';
$HnavyImage2[$num] = ''; # ������

### ����쥪��
$num = 1; # �����ֹ�
$HnavyName[$num] = '����쥪���н���';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 5;      # ����ѵ���
$HnavyMaxHP[$num]     = 10;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 4;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 4;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 1;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 400;    # ��¤����
$HnavyShellCost[$num] = 100;      # ������ȯ������
$HnavyMoney[$num]     = 15;      # �ݻ�����
$HnavyFood[$num]      = 150;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x20003581; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['�н������겼','¿��Ƭ���뻶��','',''];
$HsubmarineSurface[$num] = 0;   #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ��ϰ�(Hex)
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   ���ϡ���������<BR>'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy1_0.gif';# �����β����ե�����
$HnavyImage2[$num] = '';         # ������
$HvsMonster[$num] = 1; # ���ä�������Ǥ��ʤ��ե饰

### ���ѥ�����
$num = 2; # �����ֹ�
$HnavyName[$num] = '���ѥ�����������';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 5;      # ����ѵ���
$HnavyMaxHP[$num]     = 10;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 1;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 1;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;     # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 2000;    # ��¤����
$HnavyShellCost[$num] = 200;      # ������ȯ������
$HnavyMoney[$num]     = 15;      # �ݻ�����
$HnavyFood[$num]      = 150;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x20002481; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '¿��Ƭ���뻶��', '¿��Ƭ���뻶��',''];
$HsubmarineSurface[$num] = 0;   #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   ���Ϲ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy6_0.gif';# �����β����ե�����
$HnavyImage2[$num] = '';         # ������

### ����ߥå�
$num = 3; # �����ֹ�
$HnavyName[$num] = '����ߥå���Ʈ��';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 1;      # ����ѵ���
$HnavyMaxHP[$num]     = 2;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 1;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 5;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;     # �и���
$HnavyBuildExp[$num]  = 3;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 800;    # ��¤����
$HnavyShellCost[$num] = 10;      # ������ȯ������
$HnavyMoney[$num]     = 40;      # �ݻ�����
$HnavyFood[$num]      = 50;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1008812; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 6;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '','�����ߥ�����ȯ��'];
$HsubmarineSurface[$num] = 0;   #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư���ȤƤ�®��<BR>   �ж�����'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy3_0.gif';# �����β����ե�����
$HnavyImage2[$num] = '';         # ������

### �ۡ���
$num = 4; # �����ֹ�
$HnavyName[$num] = '�ۡ������ⵡ';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 2;      # ����ѵ���
$HnavyMaxHP[$num]     = 4;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 4;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 5;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;     # �и���
$HnavyBuildExp[$num]  = 3;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 1200;    # ��¤����
$HnavyShellCost[$num] = 20;      # ������ȯ������
$HnavyMoney[$num]     = 60;      # �ݻ�����
$HnavyFood[$num]      = 100;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1004202; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 6;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '�дϥߥ�����ȯ��',''];
$HsubmarineSurface[$num] = 0;   #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư���ȤƤ�®��<BR>   �дϹ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy11_0.gif';# �����β����ե�����
$HnavyImage2[$num] = '';         # ������

### ���ֵ���
$num = 5; # �����ֹ�
$HnavyName[$num] = '���ֵ���';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 5;      # ����ѵ���
$HnavyMaxHP[$num]     = 10;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 4;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 3;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 1000;    # ��¤����
$HnavyShellCost[$num] = 100;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1181; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['������겼', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   ��������'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy5_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������
$Hprivate[$num] = 1;#̱�����ե饰
$HvsMonster[$num] = 1; # ���ä�������Ǥ��ʤ��ե饰

### ��񹶷ⵡ
$num = 6; # �����ֹ�
$HnavyName[$num] = '��񹶷ⵡ';# ̾��
$HnavyKindMax[$num]   = 3;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 1;      # ����ѵ���
$HnavyMaxHP[$num]     = 2;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 1;      # �и���
$HnavyBuildExp[$num]  = 1;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 1500;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 120;      # �ݻ�����
$HnavyFood[$num]      = 50;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x2000002; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 3;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư���ȤƤ�®��<BR>   �������깶��'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy2_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### ��ƥ�������
$num = 7; # �����ֹ�
$HnavyName[$num] = '��ƥ�������';# ̾��
$HnavyKindMax[$num]   = 3;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 5;      # ����ѵ���
$HnavyMaxHP[$num]     = 10;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 0;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 1000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 10;      # �ݻ�����
$HnavyFood[$num]      = 50;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x2000084; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 10;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ���夹��<BR>   �������깶��'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy4_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = 'land19.gif';# ������

### �������(������)
$num = 8; # �����ֹ�
$HnavyName[$num] = '�������(������)';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 15;      # ����ѵ���
$HnavyMaxHP[$num]     = 30;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 3;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 4;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 6;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 8000;    # ��¤����
$HnavyShellCost[$num] = 5;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 600;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1001181; # �ü�ǽ��
$HnavyBuildTurn[$num] = 16;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['�����겼', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   ��������'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy36_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �������(���뷿)
$num = 9; # �����ֹ�
$HnavyName[$num] = '�������(���뷿)';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 15;      # ����ѵ���
$HnavyMaxHP[$num]     = 30;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 3;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 3;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 6;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 8000;    # ��¤����
$HnavyShellCost[$num] = 5;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 600;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1001281; # �ü�ǽ��
$HnavyBuildTurn[$num] = 16;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['����ȯ��', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   �дϹ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy35_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �������(�ɶ���)
$num = 10; # �����ֹ�
$HnavyName[$num] = '�������(�ɶ���)';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 15;      # ����ѵ���
$HnavyMaxHP[$num]     = 30;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 1;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 3;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 6;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 8800;    # ��¤����
$HnavyShellCost[$num] = 5;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 600;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1008881; # �ü�ǽ��
$HnavyBuildTurn[$num] = 16;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '','�ж��ͷ�'];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   �ж�����'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy7_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �������(���Ϸ�)
$num = 11; # �����ֹ�
$HnavyName[$num] = '�������(���Ϸ�)';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 15;      # ����ѵ���
$HnavyMaxHP[$num]     = 30;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 1;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 3;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 8000;    # ��¤����
$HnavyShellCost[$num] = 5;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 600;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x21002481; # �ü�ǽ��
$HnavyBuildTurn[$num] = 16;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '��ˤ�ͷ�', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư��®��<BR>   ���Ϲ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy37_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �Ҥ夦��
$num = 12; # �����ֹ�
$HnavyName[$num] = '�Ҥ夦�����Ҷ���';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 15;      # ����ѵ���
$HnavyMaxHP[$num]     = 30;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 9;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 24000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 60;      # �ݻ�����
$HnavyFood[$num]      = 1200;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x80; # �ü�ǽ��
$HnavyBuildTurn[$num] = 48;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ���ܤ��볤����Ҷ���ȯ�ʲ�ǽ'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy39_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �������
$num = 13; # �����ֹ�
$HnavyName[$num] = '�������';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 8;      # ����ѵ���
$HnavyMaxHP[$num]     = 16;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 5;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 1;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 2;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 8;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 12000;    # ��¤����
$HnavyShellCost[$num] = 5;      # ������ȯ������
$HnavyMoney[$num]     = 45;      # �ݻ�����
$HnavyFood[$num]      = 900;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x1001284; # �ü�ǽ��
$HnavyBuildTurn[$num] = 24;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['����ȯ��', '', '',''];
$HsubmarineSurface[$num] = 5;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ���夹��<BR>   �дϹ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy10_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = 'land19.gif';# ������

### ��䷿���
$num = 14; # �����ֹ�
$HnavyName[$num] = '��䷿���';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 30;      # ����ѵ���
$HnavyMaxHP[$num]     = 60;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 4;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 4;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 15;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 24000;    # ��¤����
$HnavyShellCost[$num] = 10;      # ������ȯ������
$HnavyMoney[$num]     = 120;      # �ݻ�����
$HnavyFood[$num]      = 2400;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x21002280; # �ü�ǽ��
$HnavyBuildTurn[$num] = 48;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '��ˤ�ͷ�', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   �дϡ����Ϲ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy9_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �ե����ȥ쥹���ⵡ
$num = 15; # �����ֹ�
$HnavyName[$num] = '�ե����ȥ쥹���ⵡ';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 2;      # ����ѵ���
$HnavyMaxHP[$num]     = 4;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 1;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 4;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 4;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 2000;    # ��¤����
$HnavyShellCost[$num] = 40;      # ������ȯ������
$HnavyMoney[$num]     = 80;      # �ݻ�����
$HnavyFood[$num]      = 100;      # �ݻ�����
$HnavyProbWreck[$num] = 80;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x20002402; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 12;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '���饹�������겼', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   ��ư���ȤƤ�®��<BR>���Ϲ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy12_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### ��ڵ����������˥å�
$num = 16; # �����ֹ�
$HnavyName[$num] = '��ڵ����������˥å�';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 5;      # ����ѵ���
$HnavyMaxHP[$num]     = 10;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 0;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 2000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x20080; # �ü�ǽ��
$HnavyBuildTurn[$num] = 0;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;  #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   �ǰ�ǽ��'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy13_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������
$Hprivate[$num] = 1;#̱�����ե饰

### ���µ�������
$num = 17; # �����ֹ�
$HnavyName[$num] = '���µ�������';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 50;      # ����ѵ���
$HnavyMaxHP[$num]     = 100;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 6;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 7;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 5;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 25;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 60000;    # ��¤����
$HnavyShellCost[$num] = 20;      # ������ȯ������
$HnavyMoney[$num]     = 240;      # �ݻ�����
$HnavyFood[$num]      = 4800;      # �ݻ�����
$HnavyProbWreck[$num] = 20;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x21002680; # �ü�ǽ��
$HnavyBuildTurn[$num] = 120;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  0;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '��ˤ�ͷ�', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 1;   #����������Hex
$HnaviExp.= "NAVY$num = '   �дϡ����Ϲ���'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy16_0.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### �����ɱһ���
$num = 18; # �����ֹ�
$HnavyName[$num] = '�����ɱһ���';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 10;      # ����ѵ���
$HnavyMaxHP[$num]     = 20;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 6000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 0;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x40; # �ü�ǽ��
$HnavyBuildTurn[$num] = 12;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  1;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   ���⹶���ɱ�'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy33.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### ����η�����
$num = 19; # �����ֹ�
$HnavyName[$num] = '����η�����';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 10;      # ����ѵ���
$HnavyMaxHP[$num]     = 20;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 6000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 0;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x200000; # �ü�ǽ��
$HnavyBuildTurn[$num] = 12;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  1;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '��ˤ�ͷ�', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   �μ�ǽ��'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy32.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

### ������
$num = 20; # �����ֹ�
$HnavyName[$num] = '������';# ̾��
$HnavyKindMax[$num]   = 0;      # ��ͭ��ǽ��
$HnavyHP[$num]        = 10;      # ����ѵ���
$HnavyMaxHP[$num]     = 20;      # �ǽ��ѵ���(Max15)
$HnavyDamage[$num]    = 0;      # �˲��� ������ʤ���1
$HnavyFire[$num]      = 0;      # �����
$HnavyFireHex[$num]   = 0;      # �����ϰ�(��)
$HnavyFireRange[$num] = 0;      # ������Υ(����ߥ󥰾õ��ϰ�)
$HnavyExp[$num]       = 3;      # �и���
$HnavyBuildExp[$num]  = 0;      # ������¤�Ƿ�������������и���
$HnavyCost[$num]      = 6000;    # ��¤����
$HnavyShellCost[$num] = 0;      # ������ȯ������
$HnavyMoney[$num]     = 30;      # �ݻ�����
$HnavyFood[$num]      = 300;      # �ݻ�����
$HnavyProbWreck[$num] = 0;     # �������˻ĳ����Ĥ��Ψ(%)
$HnavySpecial[$num]   = 0x400000; # �ü�ǽ��
$HnavyBuildTurn[$num] = 12;     # ��������
$HnavyCruiseTurn[$num] = 0;     # ��³������
$HnavyNoMove[$num]    =  1;     # ư���ʤ�����ե饰
$HnavyFireName[$num] = ['', '��ˤ�ͷ�', '',''];
$HsubmarineSurface[$num] = 0;  #�����夹��װ�ư������夹���Ψ(1%ñ��)
$HnavyTowardRange[$num]  = 0;   #������ư�״��Ϥ�õ���ϰ�(Hex)
$Hoilp[$num]             = 0;   #�ֳ���õ��������ȯ����Ψ(0.1%ñ��)
$HnavySupplyRange[$num]  = 0;   #�����ǽ�ϡ����Ϥ�ͭ���ϰ�(Hex)
$HpiratesHex[$num]       = 0;   #�ֳ�±ǽ�ϡ׳�±�԰٤�Ԥ�Hex
$Hfirehexp[$num]         = 0;   #��̿��ΨUP��1Hex�̤���Ψ(%ñ��)
$HbouhaHex[$num]         = 0;   #������ǽ�ϡ����Ȥ������ϰ�(Hex)
$HdamageMax[$num]        = 0;   #���˲���:������׺����˲���
$Hdamagep[$num]          = 0;   #���˲���:����������ȯ����Ψ(1%ñ��)
$HnavyTerrorHex[$num]    = 0;   #����������Hex
$HnaviExp.= "NAVY$num = '   �μ�ǽ��'\n";# �ݥåץ��åץʥӲ�����ʬ
$HnavyImage[$num]  = 'navy24.gif'; # �����β����ե�����
$HnavyImage2[$num] = '';# ������

# ��°������
#------------
# ����(��°����)���и����롩��0:���ʤ���1:�����
$HnavyUnknown   = 1;

# ñ�����Ѥ�����νи�Ψ(0.01%ñ��)
$HdisNavy = 3;

# ��°�����Ͻи��δ��
@HdisNavyBorder = ( 0, 5000, 5000, 5000, 5000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 20000, 20000, 25000, 24000, 30000, 35000);

# ��°�����Ͻи���Ψ
@HdisNavyRatio = ( 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1); # ��������(0�ˤ���Ƚи����ʤ��ʤ롣�����Ϥ�0�ˤ��ޤ��礦d(*�ޢ���*)b)
# �и�ΨȽ��($HdisNavy)�ǽи����뤳�Ȥ����ꤷ���Τ����͸����($HdisNavyBorder)�򥯥ꥢ���Ƥ���
# �������椫������Ψ($HdisNavyRatio)�Ǵ���������

#----------------------------------------
# ����
#----------------------------------------
# ����(����32����)
$HmonsterNumber  = 8; 

# ñ�����Ѥ�����νи�Ψ(0.01%ñ��)
$HdisMonster   = 3;

# �����ɸ���Ȥ�����(0:�ػ�)
$HuseSendMonster = 0;

# ST�����ɸ���Ȥ�����(0:�ػ�)
$HuseSendMonsterST = 0;

# �ɸ���ǽ�ʲ��ä��ֹ�κ�����
$HsendMonsterNumber = 7;

# ���⤷�����ü��Ȥ������ϰϤˤ����硢����(����)�⤢�ꡩ��0:�ʤ���1:�����
$HmonsterSelfAttack = 0;

# �ֹ���ǽ�ϡפ����Ƥ����������Ϸ�������ξ�硢̵���ˤ��뤫����0:���ʤ���1:���롢2:ͧ�����̵���ˤ����
$HmonsterSafetyZone = 2;
# ̵������̵���ˤʤ��Ψ(%) ��̵������ǽ��ȯư������̤�Ƚ��
$HmonsterSafetyInvalidp = 0;

# �ֹ���ǽ�ϡפι��������(�λ�ˤʤ����ȯŪ�˹����������ä���Τ�)(0:����ʤ�)
$HmonsterFireMax = 0;

# ���ýи��δ��
@HdisMonsBorder = ( 0, 1000, 1000, 2500, 2500, 2500, 4000, 4000);

# ���ýи���Ψ
@HdisMonsRatio = ( 0, 1, 1, 1, 1, 1, 1, 1); # ��������(0�ˤ���Ƚи����ʤ��ʤ�)
# �и�ΨȽ��($HdisMonster)�ǽи����뤳�Ȥ����ꤷ���Τ����͸����($HdisMonsBorder)�򥯥ꥢ���Ƥ���
# ���ä��椫������Ψ($HdisMonsRatio)�ǲ��ä�����

# ����������ե�����(��������)
$HmonsterImageUnderSea = 'land17.gif';

# ��������(����32����)
#----------------------
### �ᥫ���Τ�
$num = 0; # �����ֹ�
# ̾��
$HmonsterName[$num] = '�ᥫ���Τ�';
# ǽ��
$HmonsterBHP[$num]       = 2;    # ��������
$HmonsterDHP[$num]       = 0;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 5;    # �и���
$HmonsterValue[$num]     = 0;    # ���Τ�����
$HmonsterCost[$num]      = 3000; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 6000; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x20; # �ü�ǽ��
# �ü�ǽ�Ϥ����Ƥϡ�
# 0x0 �äˤʤ�
# 0x1 ­��®��(����2�⤢�뤯)
# 0x2 ­���ȤƤ�®��(���粿�⤢�뤯������)
# 0x4 ������Ų�
# 0x10 ��԰�ư���祳�ޥ�ɼ¹����˰�ư��
# 0x20 ����ư��Į�ʤɤ��ܻؤ��ư�ư��
# 0x80 ��ư��ġ���礬��ư�򥳥�ȥ����
# 0x100 ����ǽ�ϡʹ�����ɸ����ª�����⤹���
# 0x200 ������� (���Ƥ��������μ��Ͽ��إå����򹶷�) ���ߥ����빶��ǽ�Ϥ�ɬ��

#���������׼��ϲ�Hex�оݤ�����1��2�����ꡣ
$HmonsterTerrorHex[$num] = 0; # ������������⤹��ˤ�1Hex:7ȯ��2Hex:19ȯ��ɬ�פǤ������Ū�˹�����������뤳�Ȥˤʤ�ޤ���

# �ݥåץ��åץʥӲ�����ʬ(''�δ֤˵��ҡ�����ˤ�äƽ񤭴�����ɬ�פ���)
$HnaviExp.="MONSTER$num = '����¤����<br>��Į�ʤɤ��ܻؤ��ư�ư����'\n";

# �����ե�����
$HmonsterImage[$num] = 'monster7.gif';
$HmonsterImage2[$num] = ''; # �Ų���

### ���Τ�
$num = 1; # �����ֹ�
$HmonsterName[$num] = '���Τ�';     # ̾��
$HmonsterBHP[$num]       = 1;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 5;    # �и���
$HmonsterValue[$num]     = 400;  # ���Τ�����
$HmonsterCost[$num]      = 3400; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 6400; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '���Τ鹶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x2;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = '�����粿���ư���뤫����'\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster0.gif'; # �����ե�����
$HmonsterImage2[$num] = ''; # �Ų���

### ���󥸥�
$num = 2; # �����ֹ�
$HmonsterName[$num] = '���󥸥�';     # ̾��
$HmonsterBHP[$num]       = 1;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 7;    # �и���
$HmonsterValue[$num]     = 500;  # ���Τ�����
$HmonsterCost[$num]      = 3500; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 6500; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x4;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = '��������Ų�'\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster5.gif'; # �����ե�����
$HmonsterImage2[$num] = 'monster4.gif'; # �Ų���

### ��åɤ��Τ�
$num = 3; # �����ֹ�
$HmonsterName[$num] = '��åɤ��Τ�';     # ̾��
$HmonsterBHP[$num]       = 3;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 12;   # �и���
$HmonsterValue[$num]     = 1000; # ���Τ�����
$HmonsterCost[$num]      = 4000; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 7000; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '��åɹ���'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x0;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 1;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = ''\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster1.gif'; # �����ե�����
$HmonsterImage2[$num] = ''; # �Ų���

### ���������Τ�
$num = 4; # �����ֹ�
$HmonsterName[$num] = '���������Τ�';     # ̾��
$HmonsterBHP[$num]       = 2;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 12;   # �и���
$HmonsterValue[$num]     = 800;  # ���Τ�����
$HmonsterCost[$num]      = 3800; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 6800; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x1;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = '������2���ư����'\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster2.gif'; # �����ե�����
$HmonsterImage2[$num] = ''; # �Ų���

### ���Τ饴������
$num = 5; # �����ֹ�
$HmonsterName[$num] = '���Τ饴������';     # ̾��
$HmonsterBHP[$num]       = 1;    # ��������
$HmonsterDHP[$num]       = 0;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 10;   # �и���
$HmonsterValue[$num]     = 300;  # ���Τ�����
$HmonsterCost[$num]      = 3300; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 6300; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x12; # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = '���祳�ޥ�ɼ¹����˰�ư<br>�����粿���ư���뤫����'\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster8.gif'; # �����ե�����
$HmonsterImage2[$num] = ''; # �Ų���

### ������
$num = 6; # �����ֹ�
$HmonsterName[$num] = '������';     # ̾��
$HmonsterBHP[$num]       = 4;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 20;   # �и���
$HmonsterValue[$num]     = 1500; # ���Τ�����
$HmonsterCost[$num]      = 4500; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 7500; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x4;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = '��������Ų�'\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster6.gif'; # �����ե�����
$HmonsterImage2[$num] = 'monster4.gif'; # �Ų���

### ���󥰤��Τ�
$num = 7; # �����ֹ�
$HmonsterName[$num] = '���󥰤��Τ�';     # ̾��
$HmonsterBHP[$num]       = 5;    # ��������
$HmonsterDHP[$num]       = 2;    # ���Ϥ��� �����Ϥκ����ͤ�31
$HmonsterExp[$num]       = 30;   # �и���
$HmonsterValue[$num]     = 2000; # ���Τ�����
$HmonsterCost[$num]      = 5000; # �ɸ����ޥ������
$HmonsterCostST[$num]    = 8000; # ST�ɸ����ޥ������
$HmonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HmonsterFire[$num]      = 0;    # �ֹ���ǽ�ϡ׹����
$HmonsterFireHex[$num]   = 0;    # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HmonsterFireRange[$num] = 0;    # ������Υ(����ߥ󥰾õ��ϰ�)
$HmonsterDamage[$num]    = 0;    # �˲��� ������ʤ���1
$HmonsterSpecial[$num]   = 0x0;  # �ü�ǽ��
$HmonsterTerrorHex[$num] = 0;    # ���������׼��ϲ�Hex
$HnaviExp.="MONSTER$num = ''\n";# �ݥåץ��åץʥ�
$HmonsterImage[$num]  = 'monster3.gif'; # �����ե�����
$HmonsterImage2[$num] = ''; # �Ų���

#----------------------------------------
# �������
#----------------------------------------
# ����(����32����)
$HhugeMonsterNumber = 3;

# ������ä��и����롩��0:���ʤ���1:�����
$HhugeMonsterAppear   = 0;

# ñ�����Ѥ�����νи�Ψ(0.01%ñ��)
$HdisHuge   = 1;

# �ɸ���ǽ�ʵ�����ä��ֹ�κ�����
$HsendHugeMonsterNumber = 0; # -1���ɸ��Բ�

# �ü�ǽ��
# ���Τκ����������˹Ԥ���ǽ�ϤǤκ�����Ψ(%)
$HpRebody = 100;

# ������ýи��δ��
@HdisHugeBorder = ( 10000, 10000, 20000);

# ������ýи���Ψ
@HdisHugeRatio = ( 1, 1, 1); # ��������(0�ˤ���Ƚи����ʤ��ʤ�)
# �и�ΨȽ��($HdisHuge)�ǽи����뤳�Ȥ����ꤷ���Τ����͸����($HdisHugeBorder)�򥯥ꥢ���Ƥ���
# ������ä��椫������Ψ($HdisHugeRatio)�ǵ�����ä�����

# �����������(����32����)
#----------------------------------------
### �ɥ���
$num = 0; # �����ֹ�
# ̾��
$HhugeMonsterName[$num] = '�ɥ���';
# ǽ��
$HhugeMonsterBHP[$num]       = 6;     # ��������
$HhugeMonsterDHP[$num]       = 3;     # ���Ϥ��� �����Ϥκ����ͤ�31
$HhugeMonsterExp[$num]       = 20;    # �и���
$HhugeMonsterValue[$num]     = 2000;  # ���Τ�����
$HhugeMonsterCost[$num]      = 32000; # �ɸ����ޥ������
$HhugeMonsterCostST[$num]    = 62000; # ST�ɸ����ޥ������
$HhugeMonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HhugeMonsterFire[$num]      = 0;     # �ֹ���ǽ�ϡ׹����
$HhugeMonsterFireHex[$num]   = 0;     # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HhugeMonsterFireRange[$num] = 0;     # ������Υ(����ߥ󥰾õ��ϰ�)
$HhugeMonsterDamage[$num]    = 0;     # �˲��� ������ʤ���1
$HhugeMonsterSpecial[$num]   = 0x20;  # �ü�ǽ��
# �ü�ǽ�Ϥ����Ƥϡ�
# 0x0 �äˤʤ�
# 0x1 ­��®��(����2�⤢�뤯)
# 0x2 ­���ȤƤ�®��(���粿�⤢�뤯������)
# 0x4 ������Ų�
# 0x10 ��԰�ư���祳�ޥ�ɼ¹����˰�ư��
# 0x20 ����ư��Į�ʤɤ��ܻؤ��ư�ư��
# 0x80 ��ư��ġ���礬��ư�򥳥�ȥ����
# 0x100 ����ǽ�ϡʹ�����ɸ����ª�����⤹���
# 0x200 ������� (���Ƥ��������μ��Ͽ��إå����򹶷�) ���ߥ����빶��ǽ�Ϥ�ɬ��
# 0x10000 �����ɱҡʼ��Ϥ��٤Ƥ�ä��ʤ��¤ꥳ���ؤι��⤬̵����
# 0x20000 �Τκ����������˹Ԥ�

#���������׼��ϲ�Hex�оݤ�����1��2�����ꡣ
$HhugeMonsterTerrorHex[$num] = 0; # ������������⤹��ˤ�1Hex:7ȯ��2Hex:19ȯ��ɬ�פǤ������Ū�˹�����������뤳�Ȥˤʤ�ޤ���

# �ݥåץ��åץʥӲ�����ʬ(����ˤ�äƽ񤭴�����ɬ�פ���)
$HnaviExp.="HUGEMONSTER$num = '��Į�ʤɤ��ܻؤ��ư�ư����'\n";

# �����ե�����(Φ��)
$HhugeMonsterImage[$num] = ['gojira.gif', 'gojira6.gif', 'gojira7.gif', 'gojira8.gif', 'gojira9.gif', 'gojira10.gif', 'gojira11.gif'];
# �����ե����뤽��2(Φ�ǹŲ���)
$HhugeMonsterImage2[$num] = ['gojira.gif', 'gojira6.gif', 'gojira7.gif', 'gojira8.gif', 'gojira9.gif', 'gojira10.gif', 'gojira11.gif'];
# �����ե����뤽��3(���ˤ���)
$HhugeMonsterImage3[$num] = ['gojira.gif', 'gojira0.gif', 'gojira1.gif', 'gojira2.gif', 'gojira3.gif', 'gojira4.gif', 'gojira5.gif'];
# �����ե����뤽��4(���ǹŲ�)
$HhugeMonsterImage4[$num] = ['gojira.gif', 'gojira0.gif', 'gojira1.gif', 'gojira2.gif', 'gojira3.gif', 'gojira4.gif', 'gojira5.gif'];
# �����ե�����(�ȥåץڡ���ɽ����)
$HhugeMonsterImageS[$num] = 'gojira.gif'; 

### �ϥ󥸥�
$num = 1; # �����ֹ�
$HhugeMonsterName[$num] = '�ϥ󥸥�'; # ̾��
$HhugeMonsterBHP[$num]       = 3;     # ��������
$HhugeMonsterDHP[$num]       = 6;     # ���Ϥ��� �����Ϥκ����ͤ�31
$HhugeMonsterExp[$num]       = 10;    # �и���
$HhugeMonsterValue[$num]     = 1000;  # ���Τ�����
$HhugeMonsterCost[$num]      = 31000; # �ɸ����ޥ������
$HhugeMonsterCostST[$num]    = 61000; # ST�ɸ����ޥ������
$HhugeMonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HhugeMonsterFire[$num]      = 0;     # �ֹ���ǽ�ϡ׹����
$HhugeMonsterFireHex[$num]   = 0;     # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HhugeMonsterFireRange[$num] = 0;     # ������Υ(����ߥ󥰾õ��ϰ�)
$HhugeMonsterDamage[$num]    = 0;     # �˲��� ������ʤ���1
$HhugeMonsterSpecial[$num]   = 0x20;  # �ü�ǽ��
$HhugeMonsterTerrorHex[$num] = 0;     #����������Hex
$HnaviExp.="HUGEMONSTER$num = '��Į�ʤɤ��ܻؤ��ư�ư����'\n"; # �ݥåץ��åץʥ�
# �����ե�����(Φ��)
$HhugeMonsterImage[$num] = ['gojira.gif', '', 'gojira7.gif', '', 'gojira9.gif', '', 'gojira11.gif'];
# �����ե����뤽��2(Φ�ǹŲ���)
$HhugeMonsterImage2[$num] = ['gojira.gif', '', 'gojira7.gif', '', 'gojira9.gif', '', 'gojira11.gif'];
# �����ե����뤽��3(���ˤ���)
$HhugeMonsterImage3[$num] = ['gojira.gif', '', 'gojira1.gif', '', 'gojira3.gif', '', 'gojira5.gif'];
# �����ե����뤽��4(���ǹŲ�)
$HhugeMonsterImage4[$num] = ['gojira.gif', '', 'gojira1.gif', '', 'gojira3.gif', '', 'gojira5.gif'];
# �����ե�����(�ȥåץڡ���ɽ����)
$HhugeMonsterImageS[$num] = 'gojira.gif'; 

### �ɱҤ��Τ�
$num = 2; # �����ֹ�
$HhugeMonsterName[$num] = '�ɱҤ��Τ�'; # ̾��
$HhugeMonsterBHP[$num]       = 2;     # ��������
$HhugeMonsterDHP[$num]       = 1;     # ���Ϥ��� �����Ϥκ����ͤ�31
$HhugeMonsterExp[$num]       = 40;    # �и���
$HhugeMonsterValue[$num]     = 4000;  # ���Τ�����
$HhugeMonsterCost[$num]      = 34000; # �ɸ����ޥ������
$HhugeMonsterCostST[$num]    = 64000; # ST�ɸ����ޥ������
$HhugeMonsterFireName[$num] = '�ߥ����빶��'; # �ֹ���ǽ�ϡ׹���̾��
$HhugeMonsterFire[$num]      = 0;     # �ֹ���ǽ�ϡ׹����
$HhugeMonsterFireHex[$num]   = 0;     # �ֹ���ǽ�ϡ׹����ϰ�(��)
$HhugeMonsterFireRange[$num] = 0;     # ������Υ(����ߥ󥰾õ��ϰ�)
$HhugeMonsterDamage[$num]    = 0;     # �˲��� ������ʤ���1
$HhugeMonsterSpecial[$num]   = 0x30000; # �ü�ǽ��
$HhugeMonsterTerrorHex[$num] = 0;     #����������Hex
$HnaviExp.="HUGEMONSTER$num = '�������ɱҡ����������ǽ�Ϥ���'\n"; # �ݥåץ��åץʥ�
# �����ե�����(Φ��)
$HhugeMonsterImage[$num] = ['monster0.gif', 'monster0.gif', '', 'monster0.gif', '', 'monster0.gif', ''];
# �����ե����뤽��2(Φ�ǹŲ���)
$HhugeMonsterImage2[$num] = ['monster0.gif', 'monster0.gif', '', 'monster0.gif', '', 'monster0.gif', ''];
# �����ե����뤽��3(���ˤ���)
$HhugeMonsterImage3[$num] = ['monster00.gif', 'monster00.gif', '', 'monster00.gif', '', 'monster00.gif', ''];
# �����ե����뤽��4(���ǹŲ�)
$HhugeMonsterImage4[$num] = ['monster00.gif', 'monster00.gif', '', 'monster00.gif', '', 'monster00.gif', ''];
# �����ե�����(�ȥåץڡ���ɽ����)
$HhugeMonsterImageS[$num] = 'monster00.gif'; 

#----------------------------------------
# ��ǰ��
#----------------------------------------
# �����ढ�뤫
$HmonumentNumber = 3;

# ̾��
@HmonumentName = (
	'��Υꥹ', 
	'ʿ�µ�ǰ��', 
	'�襤����',
);

# �ݥåץ��åץʥӲ�����ʬ(����ˤ�äƽ񤭴�����ɬ�פ���)
$HnaviExp.=<<"END";
MONIMENT0 = "";
MONIMENT1 = "";
MONIMENT2 = "";
END

# �����ե�����
@HmonumentImage = (
	'monument0.gif',
	'monument1.gif',
	'monument2.gif',
);

# ��ǰ��ȯ�ͤ�Ȥ�����(0:�ػ�)
$HuseBigMissile = 0;

#----------------------------------------
# �����ƥ�
#----------------------------------------
# �����ƥ��Ȥ�����(0:�ػ�)
$HuseItem = 1;

# Ʊ���Ǥ��٤ƤΡ֥��������ƥ�פ��������ȥ������λ���롩(0:���ʤ� 1:����)
$HallyItemComplete = 1;

# ̾��
@HitemName = (
	'���ꥹ����', # ���
	'���꡼�󡦥��ꥹ����',
	'��åɡ����ꥹ����',
	'�����������ꥹ����',
	'�֥롼�����ꥹ����',
	'����С������ꥹ����',
	'�ۥ磻�ȡ����ꥹ����',
	'�����������ꥹ����',

	'���',
	'����ޥ����',
	'����ǥ�����',
	'�ɥꥢ����',
	'����',
	'�Ρ���',
	'��������',
);
#@HitemName = (
#	'�ե����꡼���ȡ���', # ���
#	'���',
#	'����ޥ����',
#	'����ǥ�����',
#	'�ɥꥢ����',
#	'����',
#	'�Ρ���',
#	'��������',
#	'��������'
#);

# �ü�ǽ������
# ['key item',
#	 '�ɤ���Ǥ�����ǽ', '����ߥ󥰾õ�', '��ͭ��ǽ������+��', '�����򹭤���Hex��', '�������1Hex�̤���Ψ',
#	 '���ޥ�ɼ¹Բ��', '������������Ψ', '����������Ψ', '������Ψ', '������Ψ', '������������Ψ', '�˲�����Ψ'
#	 '�����ݻ�������Ψ', '�����ݻ�����Ψ', '����������Ψ', '���ޥ������Ψ', '�˲�������'
# ]
@HitemSpecial = (
#    ��, ���, ����, ��ͭ, ����, ��Ψ, ����, ��max, ��max, ����, ����, ����, ����, �ݿ�, ����, ����, ����, �Ͽ�, ����, ���, ���, ʮ��, �к�, ����, �ˡ�
	[ 0,    0,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0], # ���ߡ�(�ѹ��Բġ������ƥ������ʤ��������˻���)
	[ 1,    0,    0,    0,    0,    0,    1,    10,     1,    2,    1,    1,    1,  0.5,    1,  0.5,    1,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    1,     1,    10,    1,    2,    1,    1,    1,  0.5,    1,  0.5,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    2,     1,     1,    1,    1,    1,    1,    1,    1,    1,  0.5,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    0,   10,    1,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    1,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    2,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    1,    0,    0,   90,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    1,    0,    0,    0,    1,     1,     1,    1,    1,    2,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0],

	[ 1,    0,    0,    0,    0,    0,    1,   0.5,     1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0,    1,    1,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    1,     1,   0.5,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    2,    1,    1,    1,    1,    1,    1,    0,    0],
	[ 1,    0,    0,   -5,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    1,    0,    1,    1,    1,    1,    1,    1,    0],
	[ 1,    1,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    2,    1,    1,    1,    1,    0,    1,    1,    1,    1,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    2,    1,    1,    1,    1,    1,    1,    0,    1,    1,    0],
	[ 1,    0,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    2,    1,    1,    1,    0,    1,    1,    1,    1,    0],
);
#  0:key item(����°������ĥ����ƥ�򤹤٤ƽ����ȥ����ཪλ)[0:°���ʤ�,1:°������]
#  1:�ɤ���Ǥ�����ǽ[0:°���ʤ�,1:°������]
#  2:����ߥ󥰤��ä���(����ߥ󥰡��⡼��ͭ�����Τ߸��̤���)[0:°���ʤ�,1:°������]
#  3:��ͭ��ǽ�����������䤹[0:�̾�,��ͭ��ǽ�������������ͤ���դ��������������ꤹ�뤳��]
#  4:������Υ�򹭤���Hex��[0:�̾�,������ǽ�������ͤ���դ��������������ꤹ�뤳��]
#  5:������̿��ΨUP:�����ι����������Ψ��1Hex�̤��[0:�̾�,1��100:%ñ�̤ǻ���]
#  6:1������˼¹Ԥ��륳�ޥ�ɿ�[1:�̾�,����������������դ������ꤹ�뤳��]
#  7:�����κ����ͤ���Ψ[1:�̾�,(���������:1����礭����Хץ饹�����ƥࡢ��������Хޥ��ʥ������ƥ�)]
#  8:���κ����ͤ���Ψ[1:�̾�,(���������:1����礭����Хץ饹�����ƥࡢ��������Хޥ��ʥ������ƥ�)]
#  9:����(����)����Ψ[1:�̾�,(���������:1����礭����Хץ饹�����ƥࡢ��������Хޥ��ʥ������ƥ�)]
# 10:����(���)����Ψ[1:�̾�,(���������:1����礭����Хץ饹�����ƥࡢ��������Хޥ��ʥ������ƥ�)]
# 11:�����ι���������Ψ[1:�̾�,(�����������:1����礭����Хץ饹�����ƥ�)]
# 12:�������˲��Ϥ���Ψ[1:�̾�,(�����������:1����礭����Хץ饹�����ƥ�)]
# 13:�����ΰݻ���������Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 14:�����ΰݻ�������Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 15:�����ξ������Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 16:���ޥ�ɤΥ����Ȥ���Ψ[1:�̾�,(�����������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 17:�Ͽ�ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 18:����ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 19:���ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 20:�������ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 21:ʮ��ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 22:�к�ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 23:����ȯ����Ψ[1:�̾�,(���������:1����礭����Хޥ��ʥ������ƥࡢ��������Хץ饹�����ƥ�)]
# 24:�������˲��ϥץ饹[0:�̾�,(���������:0����礭����Хץ饹�����ƥ�)]
# �����ƥ��ʣ����ͭ�����硢1��6,24�Ϻ���Τ�Τ�ͭ����7��23�Ϥ��٤Ƥ���Ψ��褸����Τˤʤ롣

# �����ե�����
@HitemImage = (
	'item0.gif', # ���ߡ�
	'item1.gif',
	'item2.gif',
	'item3.gif',
	'item4.gif',
	'item5.gif',
	'item6.gif',
	'item7.gif',
	'runa3.gif',
	'saramanda2.gif',
	'undhine3.gif',
	'doriado2.gif',
	'zin2.gif',
	'nomu2.gif',
	'wiruowisupu2.gif',
);
#@HitemImage = (
#	'yousei2.gif',
#	'runa3.gif',
#	'saramanda2.gif',
#	'undhine3.gif',
#	'doriado2.gif',
#	'zin2.gif',
#	'nomu2.gif',
#	'wiruowisupu2.gif',
#	'sheido2.gif'
#);

# �����ƥ������å���Ψ(������и��಼͡�����ꤷ������)
# ��������������༣�λ�(0:Ƚ�ꤷ�ʤ�)
$HitemGetDenominator = 1000;

# �����������༣�λ�(0:Ƚ�ꤷ�ʤ�)
$HitemGetDenominator2 = 10000;

# �������ĳ���Ѥλ�(0:Ƚ�ꤷ�ʤ�)
$HitemGetDenominator3 = 1000;

# å�衧�����ƥ��ݻ���δ��������λ�(0:Ƚ�ꤷ�ʤ� 1:�Ǹ��1��(1��)���˲��������ˤ��٤�å��)
$HitemSeizeDenominator = 100;

# �������դ��Ȥ˾�̤��礫���ˤҤȤĤ���key item��Ϳ���뤫��(���ꥹ������å����)
$HitemGivePerTurn = 0; # 0:Ϳ���ʤ���1:Ϳ����(��̤��礫��)��2:Ϳ����(���̤��礫��)

#----------------------------------------
# Battle Field �ȼ�����
#----------------------------------------
# ��°�����Ϥνи�Ψ(0.01%ñ�̤����Ѥ�̵�ط���0�ˤ����ñ�����Ѥ�����ץ쥤�䡼���2��)
$HdisNavyBF = 0;

# ���äνи�Ψ(0.01%ñ�̤����Ѥ�̵�ط���0�ˤ����ñ�����Ѥ�����ץ쥤�䡼���2��)
$HdisMonsterBF = 0;

# ������äνи�Ψ(0.01%ñ�̤����Ѥ�̵�ط���0�ˤ����ñ�����Ѥ�����ץ쥤�䡼���2��)
$HdisHugeBF = 0;

# ͧ���������̵���ˤ��롩(0:���ʤ� 1:����) ����������롦��Ũ������Τ�ͧ���������̵���ˤ��ޤ�
$HamityInvalid = 1;

# �����ƥ��ǽ�Ϥ�̵���ˤ��롩(0:���ʤ� 1:����) ��������2�ܡ������򹭤��롦��������ǽ��̿��ΨUP���˲��ϣ��ܤΤ�̵���ˤ��ޤ�
$HitemInvalid = 1;

# ������ǽ�Ϥ򥢥åפ��롩(0:���ʤ� n:�ץ饹or�ޥ��ʥ����ͻ���)
@HnavyFireBF = ( 0, 0, 0, 0); # �����Fire �����ϰ�(��)FireHex �����ϰ�FireRange �˲���damage

#----------------------------------------
# ŷ��
#----------------------------------------
# ŷ����Ȥ�����(0:�ػ�)
$HuseWeather = 1;

@HweatherName = (
	'ŷ��', # ���
	'����',
	'����',
	'�ޤ�',
	'ǻ̸',
	'��',
	'�뱫',
);

# ŷ����Ψ(%����ʬ���ʤ��Ƥ�褤��������������κǽ�����Ǥϡ�ɬ��0�ˤ��Ƥ������ȡ�)
@HweatherRatio = ( 0, 3, 6, 3, 2, 5, 1);

# �ü�ǽ��
@HweatherSpecial = ( 0, 0x3dc, 0x4cb, 0xa07, 0x970, 0xd24, 0xe11);
# �ü�ǽ�Ϥ����Ƥϡ�����(0:0, 1:-7, 2:-6, 3:-5, 4:-4, 5:-3, 6:-2, 7:-1, 8:0, 9:+1, a:+2, b:+3, c:+4, d:+5, e:+6, f:+7)
# 0x1��0xF �����Ѳ�
$HweatherSpecialRatio[0] = 1; # �����Ѳ����ͤ���Ψ
$HrKion = 2; # ����������(+-)
# 0x10��0xF0 �����Ѳ�
$HweatherSpecialRatio[1] = 5; # �����Ѳ����ͤ���Ψ
$HrKiatu = 50; # ����������(+-)
# 0x100��0xF00 �����Ѳ�
$HweatherSpecialRatio[2] = 2; # �����Ѳ����ͤ���Ψ
$HrSitudo = 15; # ����������(+-)

# �����ե�����
@HweatherImage = (
	'weather0.gif', # ���ߡ�
	'weather1.gif',
	'weather2.gif',
	'weather3.gif',
	'weather4.gif',
	'weather5.gif',
	'weather6.gif',
);

#----------------------------------------
# �޴ط�(����32����)
#----------------------------------------
# �������դ򲿥�������˽Ф���
$HturnPrizeUnit = 100;

# �ޤ�̾��
# kind: �ɤ����ǤǷ�ޤ뤫(�������դϾ�̲���ޤǤμ��ޤ����ͻ���)
# ptr: ext�ΰ�ξ�硢�����ܤ����ǤǷ�ޤ뤫
# threshold: ptr�μ����ͤ����Ĥˤʤä�����ޤ�
# money: �޶�
# name: �ޤ�̾��
$Hprize[0]  = { 'name' => '��������',     'kind' => '1',      'ptr' => 0,  'threshold' => 0,     'contribution' => 0,    'money' => 300 };
$Hprize[1]  = { 'name' => '�˱ɾ�',       'kind' => 'pop',    'ptr' => 0,  'threshold' => 3000,  'contribution' => 0,    'money' => 3000 };
$Hprize[2]  = { 'name' => 'Ķ�˱ɾ�',     'kind' => 'pop',    'ptr' => 0,  'threshold' => 5000,  'contribution' => 0,    'money' => 5000 };
$Hprize[3]  = { 'name' => '����˱ɾ�',   'kind' => 'pop',    'ptr' => 0,  'threshold' => 10000, 'contribution' => 0,    'money' => 10000 };
$Hprize[4]  = { 'name' => 'ʿ�¾�',       'kind' => 'achive', 'ptr' => 0,  'threshold' => 200,   'contribution' => 0,    'money' => 200 };
$Hprize[5]  = { 'name' => 'Ķʿ�¾�',     'kind' => 'achive', 'ptr' => 0,  'threshold' => 500,   'contribution' => 0,    'money' => 500 };
$Hprize[6]  = { 'name' => '���ʿ�¾�',   'kind' => 'achive', 'ptr' => 0,  'threshold' => 800,   'contribution' => 0,    'money' => 800 };
$Hprize[7]  = { 'name' => '�����',       'kind' => 'damage', 'ptr' => 0,  'threshold' => 500,   'contribution' => 0,    'money' => 500 };
$Hprize[8]  = { 'name' => 'Ķ�����',     'kind' => 'damage', 'ptr' => 0,  'threshold' => 1000,  'contribution' => 0,    'money' => 1000 };
$Hprize[9]  = { 'name' => '��˺����',   'kind' => 'damage', 'ptr' => 0,  'threshold' => 2000,  'contribution' => 0,    'money' => 2000 };
$Hprize[10] = { 'name' => '�߹񷮾�',     'kind' => 'ext',    'ptr' => 1,  'threshold' => 20000, 'contribution' => 0,    'money' => 0 };
$Hprize[11] = { 'name' => 'ͥ���߹񷮾�', 'kind' => 'ext',    'ptr' => 1,  'threshold' => 50000, 'contribution' => 0,    'money' => 0 };
$Hprize[12] = { 'name' => '�ͷⷮ��',     'kind' => 'ext',    'ptr' => 2,  'threshold' => 5,     'contribution' => 500,  'money' => 0 };
$Hprize[13] = { 'name' => 'ͥ���ͷⷮ��', 'kind' => 'ext',    'ptr' => 2,  'threshold' => 10,    'contribution' => 1000, 'money' => 0 };
$Hprize[14] = { 'name' => '���η���',     'kind' => 'ext',    'ptr' => 3,  'threshold' => 10,    'contribution' => 500,  'money' => 0 };
$Hprize[15] = { 'name' => 'ͥ�����η���', 'kind' => 'ext',    'ptr' => 3,  'threshold' => 20,    'contribution' => 1000, 'money' => 0 };
$Hprize[16] = { 'name' => 'ͷ�ⷮ��',     'kind' => 'ext',    'ptr' => 10, 'threshold' => 50,    'contribution' => 1000, 'money' => 0 };
$Hprize[17] = { 'name' => 'ͥ��ͷ�ⷮ��', 'kind' => 'ext',    'ptr' => 10, 'threshold' => 100,   'contribution' => 5000, 'money' => 0 };
$Hprize[18] = { 'name' => '��������',     'kind' => 'ext',    'ptr' => 4,  'threshold' => 1000,  'contribution' => 500,  'money' => 0 };
$Hprize[19] = { 'name' => 'ͥ����������', 'kind' => 'ext',    'ptr' => 4,  'threshold' => 2000,  'contribution' => 1000, 'money' => 0 };
$Hprize[20] = { 'name' => '��ⷮ��',     'kind' => 'ext',    'ptr' => 5,  'threshold' => 50,    'contribution' => 200,  'money' => 0 };
$Hprize[21] = { 'name' => '��Ʈ����',     'kind' => 'ext',    'ptr' => 6,  'threshold' => 50,    'contribution' => 200,  'money' => 0 };
$Hprize[22] = { 'name' => 'Ŵ�ɷ���',     'kind' => 'ext',    'ptr' => 7,  'threshold' => 30,    'contribution' => 1000, 'money' => 0 };

#----------------------------------------------------------------------
# ����¾��ĥ�Ѥ�����(����Ū�ˤϡ��ѹ��Բ�)
#----------------------------------------------------------------------
# ext[0] �����ե饰
# ext[1] ����point(=�׸���x10)
# ext[2] �˲������ɱһ��ߤο�
# ext[3] �˲������ߥ�������Ϥο�
# ext[4] �߽Ф�����̱�ι�׿͸�
# ext[5] �������ߥ������
# ext[6] ȯ�ͤ����ߥ������
# ext[7] �ɱһ��ߤ��Ƥ����ߥ������
# ext[8] �ɸ����������ο�
# ext[9] �ɸ����줿�����ο�
# ext[10] �˲����������ο�
#----------------------------------------
# ����ʸ����������(����ʸ�����ǻ���)
#----------------------------------------
# ʸ�����¤򥪡��С������������������Ǥ��뤫��(0:���ʤ� 1:����)
$HlengthAlert = 1;

$HlengthIslandName  = 15;   # ���̾��
$HlengthOwnerName   = 15;   # ��ν�ͭ�Ԥ�̾��
$HlengthMessage     = 40;   # �ȥåץڡ�����ɽ����������Υ�����
$HlengthLbbsName    = 15;   # �ִѸ��Ǽ��ġפ���Ƽ�̾
$HlengthLbbsMessage = 60;   # �ִѸ��Ǽ��ġפ����
$HlengthFleetName   = 10;   # �����̾��
$HlengthAllyName    = 15;   # Ʊ����̾��
$HlengthAllyComment = 40;   # �ֳ�Ʊ���ξ��������ɽ�����������Υ�����
$HlengthAllyTitle   = 30;   # ��Ʊ���ξ������ξ��ɽ������������å������Υ����ȥ�
$HlengthAllyMessage = 1500; # ��Ʊ���ξ������ξ��ɽ������������å�����
$HlengthPresentLog  = 100;  # �����ͤˤ��ץ쥼��ȥ⡼�ɤΥ�å�����
#----------------------------------------
# �����ط�
#----------------------------------------
# <BODY>�����Υ��ץ����,�����ȥ��hako-init.cgi�ذ�ư���ޤ���

# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<div class="title">';
$H_tagTitle = '</div>';

# �礭��ʸ��
$HtagBig_ = '<span class="big">';
$H_tagBig = '</span>';

# ���̾���ʤ�
$HtagName_ = '<span class="islName">';
$H_tagName = '</span>';

# �����ʤä����̾��
$HtagName2_ = '<span class="islName2">';
$H_tagName2 = '</span>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<span class="head">';
$H_tagTH = '</span>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<span class="command">';
$H_tagComName = '</span>';

# ��ȯ�ײ��̾�� ��������񤢤� (���Ϥ��ߥ��ޥ����)
$HtagComName1_ = '<span class="command1">';
$HcomNameColor1 = '#A08000'; # CSS�ο��Ȥ�����������������
# ��ȯ�ײ��̾�� ���������ʤ� (���Ϥ��ߥ��ޥ����)
$HtagComName2_ = '<span class="command2">';
$HcomNameColor2 = '#0080A0'; # CSS�ο��Ȥ�����������������

# �ҳ�
$HtagDisaster_ = '<span class="disaster">';
$H_tagDisaster = '</span>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# ����
$HtagMoney_ = '<span class="money">';
$H_tagMoney = '</span>';

# ����
$HtagFood_ = '<span class="food">';
$H_tagFood = '</span>';

# �̾��ʸ����
$HnormalColor_ = '<span class="normal">';
$H_normalColor = '</span>';

# ���ɽ�������°��
$HbgTitleCell   = 'class=TitleCell';   # ���ɽ���Ф�
$HbgNumberCell  = 'class=NumberCell';  # ���ɽ���
$HbgNameCell    = 'class=NameCell';    # ���ɽ���̾��
$HbgInfoCell    = 'class=InfoCell';    # ���ɽ��ξ���
$HbgCommentCell = 'class=CommentCell'; # ���ɽ��������
$HbgInputCell   = 'class=InputCell';   # ��ȯ�ײ�ե�����
$HbgMapCell     = 'class=MapCell';     # ��ȯ�ײ��Ͽ�
$HbgCommandCell = 'class=CommandCell'; # ��ȯ�ײ����ϺѤ߷ײ�

# �Ƕ��ŷ���ο�°��
$headNameCellcolor = 'class=headNameCellcolor'; # �Ƕ��ŷ���Υإå���ʬ�Υ��뿧
$pointCellcolor    = 'class=pointCellcolor';    # �Ƕ��ŷ����ŷ����ʬ�Υ��뿧
$pointCellcolor2   = 'class=pointCellcolor2';   # �Ƕ��ŷ���ε��ݿ��ͤΥ��뿧
$nameCellcolor     = 'class=nameCellcolor';     # �Ƕ��ŷ������̾��ɽ����ʬ�Υ��뿧

$tomorrowColor     = 'class=TomorrowColor';     # �Ƕ��ŷ���������ʹߤ�ʸ����
$todayColor        = 'class=TodayColor';        # �Ƕ��ŷ���κ�����ʸ����
$yesterdayColor    = 'class=YesterdayColor';    # �Ƕ��ŷ���κ���������ʸ����

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------
# ���ޥ��

# �ײ��ֹ������
# 0 ����(��ȯ)
$HcomPrepare  = 1; # ����
$HcomPrepare2 = 2; # �Ϥʤ餷
$HcomPrepare3 = 3; # ����Ϥʤ餷
$HcomReclaim  = 4; # ���Ω��
$HcomReclaim2 = 5; # ��®���Ω��
$HcomDestroy  = 6; # ����
$HcomDestroy2 = 7; # ��®����


# 1 ����(����)
$HcomFarm        = 21; # ��������
$HcomFastFarm    = 22; # ��®��������
$HcomFactory     = 23; # �������
$HcomFastFactory = 24; # ��®�������
$HcomMountain    = 25; # �η�������
$HcomMonument    = 31; # ��ǰ���¤
$HcomBouha       = 32; # ����������
$HcomSellTree    = 26; # Ȳ��
$HcomPlant       = 27; # ����
$HcomPlant2      = 28; # ��®����


@HcomComplex = (); # ʣ�����
if(!$HuseComplex) { # �Ȥ�ʤ����ν���
	@HcomplexName = ();
	@HcomplexComName = ();
}
foreach (0..$#HcomplexComName) {
	$HcomComplex[$_] = 41 + $_; # 41��
}
$HcomComplex[0] = 40 if($HcomComplex[0] eq '');

# 2 ����(����)
$HcomDoNothing  = 91; # *�Ŵ�
$HcomSell       = 92; # *����͢��
$HcomBuy        = 93; # *����͢��
$HcomPropaganda = 94; # *Ͷ�׳�ư
$HcomGiveup     = 95; # *�������

# 3 ����(��¤)
@HcomNavy = ();
#foreach (0..$#HnavyName) {
#	$HcomNavy[$_] = 101 + $_; # 101��132
#}
#$HcomNavy[0] = 100 if($HcomNavy[0] eq '');




# ��ư���Ϥ��ѹ�����
$HcomNavy[0]  = 101; # ����
$HcomNavy[1]  = 102; # ����쥪��
$HcomNavy[2]  = 103; # ���ѥ�����
$HcomNavy[3]  = 104; # ����ߥå�
$HcomNavy[4]  = 105; # �ۡ���
$HcomNavy[5]  = 106; # �ꤲ��
$HcomNavy[6]  = 107; # ���
$HcomNavy[7]  = 108; # ��ƥ�
$HcomNavy[8]  = 109; # ����
$HcomNavy[9]  = 110; # ����
$HcomNavy[10] = 111; # �ɶ�
$HcomNavy[11] = 112; # ����
$HcomNavy[12] = 113; # �Ҥ夦��
$HcomNavy[13] = 114; # ��
$HcomNavy[14] = 115; # ���
$HcomNavy[15] = 116; # �ե����ȥ쥹
$HcomNavy[16] = 117; # �������˥å�
$HcomNavy[17] = 118; # ����

$HcomNavy[18] = 119; # �����ɱ�
$HcomNavy[19] = 120; # �η�
$HcomNavy[20] = 121; # ��

# ����ȯ��
$HcomNavy2[0] = 351; # ����ߥåȳ���
$HcomNavy2[1] = 352; # �ۡ�������
$HcomNavy2[2] = 353; # ��񳤳�
$HcomNavy2[3] = 354; # �ե����ȥ쥹����

# 4 ����(����)
$HcomNavyMove        = 201; # ���ư(�ɸ������Ԥ�����)
#$HcomNavySend        = 202; # �����ɸ�
#$HcomNavyReturn      = 203; # ���ⵢ��
$HcomNavyForm        = 211; # ������
#$HcomNavyExpell      = 212; # �������ҡʴ����ȴ����Ũ�ˤʤ�˵����ɸ�ϻ����
$HcomNavyDestroy     = 213; # �����˴�
$HcomNavyWreckRepair = 214; # �ĳ�����
$HcomNavyWreckSell   = 215; # �ĳ����
$HcomMoveTarget      = 216; # ��ư��ġ���ִ��ϡ���������
$HcomMoveMission     = 217; # ��ư����
#$HcomNavyMission     = 218; # ���������ѹ�
$HcomNavyTarget      = 219; # ���ƹ���
$Hcomshikin           = 220; # ��ⷫ��
$Hcomgoalsetpre      = 221; # ��Ū�ϻ���(�о�)
$Hcomgoalset         = 222; # ��Ū�ϻ���(��ɸ)
$Hcomremodel         = 223; # ��������(����/����/�ɶ�/����)
$Hcomwork            = 224; # ���ѥ�����Ÿ��
$HcomSellPort        = 225; # ����ʧ����
$HcomBuyPort         = 226; # �������
$HcomWarpA           = 227; # ���������ư(��ư��)
$HcomWarpB           = 228; # ���������ư(��ư��)


# 5 ����
$HcomMoney      = 301; # *�����
$HcomFood       = 302; # *�������
$HcomAmity      = 311; # *ͧ����°���ѹ�
$HcomAlly       = 312; # *Ʊ��������æ��
$HcomDeWar      = 321; # *�����۹�
$HcomCeasefire  = 322; # *�����ǿ�

# 6 ����(����)
$HcomDbase    = 331; # �ɱһ��߷���
$HcomHaribote = 332; # �ϥ�ܥ�����
$HcomSeaMine  = 333; # ��������
$HcomCore     = 340; # ��������
$HcomBase     = 341; # �ߥ�������Ϸ���
$HcomSbase    = 342; # ������Ϸ���
$HcomDbase2   = 334; # ��®�ɱһ��߷���

# 7 ����(����)
@HcomMissile = ();
foreach (0..$#HmissileName) {
	$HcomMissile[$_] = 361 + $_; # 351��360
}

#if($HcomMissile[0] eq '') {
#	$HcomMissile[0] = 350;
#} else {
#	foreach (0..$#HmissileName) { # ST°�������å�
#		$STcheck{$HcomMissile[$_]} = 1 if($HmissileSpecial[$_] & 0x1);
#	}
#}

$HcomSendMonster   = 361; # �����ɸ�
$HcomSendMonsterST = 362; # ST�����ɸ�

# 8 ��ư��
$HcomAutoPrepare  = 401; # �ե�����
$HcomAutoPrepare2 = 402; # �ե��Ϥʤ餷
$HcomAutoDelete   = 403; # �����ޥ�ɾõ�
$HcomAutoReclaim  = 404; # �������Ω��
$HcomAutoDestroy  = 405; # ��������
$HcomAutoSellTree = 406; # Ȳ��
$HcomAutoForestry = 407; # Ȳ�Τȿ���

# ����
my @comList = (
	# 0 ����(��ȯ)
	 $HcomPrepare, $HcomPrepare2, $HcomPrepare3,
	 $HcomReclaim, $HcomReclaim2, $HcomDestroy, $HcomDestroy2,
	# 1 ����(����)
#	 $HcomFarm, $HcomFastFarm, $HcomFactory, $HcomFastFactory, $HcomSellTree, $HcomPlant, $HcomPlant2,
	 $HcomBouha, @HcomComplex,
	# 2 ����(����)
	 $HcomSell, $HcomBuy,  
	 $HcomDoNothing, $HcomPropaganda, $HcomGiveup,
	# 3 ����(��¤)
	 @HcomNavy,
	# 4 ����(����)
	 $HcomNavyMove,# $HcomNavySend, $HcomNavyReturn,
	 $HcomNavyForm, $HcomNavyDestroy, $HcomMoveTarget,
	 $HcomNavyWreckRepair, $HcomNavyWreckSell, $Hcomshikin,
	 $Hcomgoalsetpre, $Hcomgoalset, #$HcomWarpA, $HcomWarpB, #$HcomMoveMission, $HcomNavyTarget,
         $Hcomremodel, $Hcomwork, #$HcomBuyPort, $HcomSellPort,
	# 5 ����
	 $HcomMoney, $HcomFood, $HcomAmity, $HcomAlly, $HcomDeWar, $HcomCeasefire,
	# 6 ����(����)
	 $HcomCore, 
	 $HcomBase, $HcomDbase, $HcomDbase2, $HcomSbase, $HcomHaribote, $HcomSeaMine,
	# 7 ����(����)
#	 @HcomMissile,
	 $HcomSendMonster, $HcomSendMonsterST,
         $HcomNavy2[0], $HcomNavy2[1], $HcomNavy2[2], $HcomNavy2[3],

	# 8 ��ư��
	 $HcomAutoReclaim, $HcomAutoDestroy, $HcomAutoSellTree, $HcomAutoForestry,
	 $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoDelete
	);

#-------------------------------------------------------------------------
# �ե饰�����å�(�ѹ�����)
	my $flagcheck = 0;
	$HuseFlag = 0;
	foreach(@HnavySpecial) {
		if($_ & 0x80) {
			$flagcheck = 1;
		} elsif(!$HsuicideAbility && ($_ & 0x2000000)) {
			$_ |= 0x80; # ���ϡ���ư��ĤǤʤ�����������ꤷ�ʤ���硤ǽ�ϤΤĤ�˺���ե���
		}
	}
	foreach(@HmonsterSpecial, @HhugeMonsterSpecial) {
		if($_ & 0x80) {
			$flagcheck = 1;
			last;
		}
	}
	$HuseFlag = $flagcheck; # ǽ�Ϥ����äƤ���ϡ���ư��Ĥ��������ʤ����ϡ�$flagcheck��0�ˤ��롣
	if($HcomNavy[0] == 100) {
		$HcountLandPort = 0;
		$HuseFlag       = 0;
		$HusePriority   = 0;
		$HnavyUnknown   = 0;
		$HdisNavyBF     = 0;
	}
# �ե饰�����å������ޤ�
#-------------------------------------------------------------------------
# ���ޥ�ɥꥹ������(�ѹ�����)
@HcomList = ();
foreach (@comList) {
	next if (($_ == $HcomAlly) && (!$HallyUse || !$HallyJoinComUse || $HarmisticeTurn || $Htournament));
	next if (($_ == $HcomAmity) && (!$HuseAmity || $HarmisticeTurn || $Htournament));
	next if ((($_ == $HcomDeWar) ||
			($_ == $HcomCeasefire)
			) && (!$HuseDeWar || $HarmisticeTurn || $HsurvivalTurn || $Htournament));
	next if (($_ == $HcomBase) && !$HuseBase);
	next if (($_ == $HcomSbase) && (!$HuseSbase || $Htournament));
	next if (($_ == $HcomBouha) && !$HuseBouha);
	next if (($_ == $HcomSeaMine) && !$HuseSeaMine);
#	next if ((($HcomMissile[0] <= $_) && ($_ <= $HcomMissile[$#HmissileName])
#			) && !$HuseBase && !$HuseSbase);
	next if ($STcheck{$_} && (!$HuseMissileST || $Htournament));
	next if (($_ == $HcomSendMonster) && (!$HuseSendMonster || $Htournament));
	next if (($_ == $HcomSendMonsterST) && (!$HuseSendMonsterST || $Htournament));
	next if (($_ == $HcomMoveTarget) && !$HuseFlag);
	next if (($_ == $HcomNavyTarget) && !$HuseTarget);
	next if (($_ == $HcomPrepare3) && !$HusePrepare3);
	next if (($_ == $HcomFastFarm) && !$HuseFastFarm);
	next if (($_ == $HcomFastFactory) && !$HuseFastFactory);
	next if (($_ == $HcomReclaim2) && !$HuseFastReclaim);
	next if (($_ == $HcomDestroy2) && !$HuseFastDestroy);
	next if ((($_ == $HcomMonument) ||
			($_ == $HcomFood) ||
			($_ == $HcomMoney) ||
			($_ == $HcomPropaganda)
			) && $Htournament);
	next if (($HcomNavy[0] == 100) && (201 <= $_) && ($_ <= 220));
	next if (($_ == $HcomFarm) && !$HuseFarm);
	next if (($_ == $HcomFactory) && !$HuseFactory);
	next if (($_ == $HcomMountain) && !$HuseMountain);
	next if ((($_ == $HcomPlant) || ($_ == $HcomSellTree)) && !$HusePlantSellTree);
	next if (($_ == $HcomCore) && !$HuseCore);
#	next if ((($_ == $HcomNavyMove) ||
#			($_ == $HcomNavySend) ||
#			($_ == $HcomNavyReturn)
#			) && $HoceanMode && $HnotuseNavyMove);
	next if (($_ == $HcomMoveMission) && !$HoceanMode);
	push(@HcomList, $_);
}
$HcommandTotal = $#HcomList + 1; # ���ޥ�ɤμ���
foreach (@HcomList) {
	$HcomUse{$_} = 1;
}

# ���ޥ��ʬ��
# ���Υ��ޥ��ʬ������ϡ���ư���ϷϤΥ��ޥ�ɤ����ꤷ�ʤ��ǲ�������
@HcommandDivido = (
	'����(¤��),0,20',    # ��ȯ�ޥå�
	'����(����),21,40',   # ��ȯ�ޥå�
	"����(����),$HcomComplex[0],$HcomComplex[$#HcomplexComName]",   # ��ȯ�ޥå�
	'����(����),91,100',
	"����,$HcomNavy[0],$HcomNavy[$#HcomNavy]", # ��ȯ�ޥå�
	'�������,201,230',  # ��ȯ�ޥå� ��ɸ�ޥå�
	'����,301,330',
	'��������,331,350', # ��ȯ�ޥå�
	'����,351,370', # ��ɸ�ޥå�
);



$HcommandAuto = '��ư��,401,410';

# ��ա����ڡ���������ʤ��褦��
# ����	'��ȯ,0,10',  # �ײ��ֹ�00��10
# �ߢ�	'��ȯ, 0  ,10  ',  # �ײ��ֹ�00��10

# �ײ��̾���ȴʰ������������ȡ����������
$HcomName[$HcomPrepare]         = '����';
$HcomMsgs[$HcomPrepare]         = '���ϡ���ʪ�Ϥ�ʿ�Ϥˤ��ޤ���';
$HcomCost[$HcomPrepare]         = 5;
$HcomTurn[$HcomPrepare]         = 1;
$HcomName[$HcomPrepare2]        = '�Ϥʤ餷';
$HcomMsgs[$HcomPrepare2]        = '���������ʤ������ϡ�����������ۤ��Ͽ̤γ�Ψ���徺';
$HcomCost[$HcomPrepare2]        = 100;
$HcomTurn[$HcomPrepare2]        = 0;
$HcomName[$HcomPrepare3]        = '����Ϥʤ餷';
$HcomMsgs[$HcomPrepare3]        = '���Υ��ޥ�ɤҤȤĤǡ����٤ƤιӤ��Ϥ��Ϥʤ餷���ޤ���';
$HcomCost[$HcomPrepare3]        = "���Ͽ�x${HcomCost[$HcomPrepare2]}";
$HcomTurn[$HcomPrepare3]        = 0;
$HcomName[$HcomReclaim]         = '���Ω��';
$HcomMsgs[$HcomReclaim]         = '�������������ϡ�Φ�μ��ϤΤ߲�ǽ�Ǥ���';
$HcomCost[$HcomReclaim]         = 150;
$HcomTurn[$HcomReclaim]         = 1;
$HcomName[$HcomReclaim2]        = '��®���Ω��';
$HcomMsgs[$HcomReclaim2]        = '���������ʤ������Ω�ơ�';
$HcomCost[$HcomReclaim2]        = 3000;
$HcomTurn[$HcomReclaim2]        = 0;
$HcomName[$HcomDestroy]         = '����';
$HcomMsgs[$HcomDestroy]         = '���Ϣ��������������ǿ��̻��ꤹ�������õ����';
$HcomCost[$HcomDestroy]         = 200;
$HcomTurn[$HcomDestroy]         = 1;
$HcomName[$HcomDestroy2]        = '��®����';
$HcomMsgs[$HcomDestroy2]        = '���������ʤ��η���';
$HcomCost[$HcomDestroy2]        = 4000;
$HcomTurn[$HcomDestroy2]        = 0;
#$HcomName[$HcomSellTree]        = 'Ȳ��';
#$HcomMsgs[$HcomSellTree]        = '���Ǽ¹Ԥ����ʿ�Ϥ��Ѳ�����ⲽ��';
#$HcomCost[$HcomSellTree]        = 0;
#$HcomTurn[$HcomSellTree]        = 1 - $HnoturnSellTree;
#$HcomName[$HcomPlant]           = '����';
#$HcomMsgs[$HcomPlant]           = 'ʿ�ϡ�Į�ϤǼ¹Բ�ǽ��';
#$HcomCost[$HcomPlant]           = 50;
#$HcomTurn[$HcomPlant]           = 1;
#$HcomName[$HcomPlant2]           = '��®����';
#$HcomMsgs[$HcomPlant2]           = 'ʿ�ϡ�Į�ϤǼ¹Բ�ǽ��';
#$HcomCost[$HcomPlant2]           = 1000;
#$HcomTurn[$HcomPlant2]           = 0;

#$HcomName[$HcomFarm]            = '��������';
#$HcomMsgs[$HcomFarm]            = '���ȸ��Ȥʤ���ߡ�����5����(ʣ����)';
#$HcomCost[$HcomFarm]            = 20;
#$HcomTurn[$HcomFarm]            = 1;
#$HcomName[$HcomFastFarm]        = '��®��������';
#$HcomMsgs[$HcomFastFarm]        = '���������ʤ�������������(ʣ����)';
#$HcomCost[$HcomFastFarm]        = 500;
#$HcomTurn[$HcomFastFarm]        = 0;
#$HcomName[$HcomFactory]         = '�������';
#$HcomMsgs[$HcomFactory]         = '��⸻�Ȥʤ���ߡ�����10��(ʣ����)';
#$HcomCost[$HcomFactory]         = 100;
#$HcomTurn[$HcomFactory]         = 1;
#$HcomName[$HcomFastFactory]     = '��®�������';
#$HcomMsgs[$HcomFastFactory]     = '���������ʤ��ι�����ߡ�(ʣ����)';
#$HcomCost[$HcomFastFactory]     = 2500;
#$HcomTurn[$HcomFastFactory]     = 0;

foreach (0..$#HcomplexComName) {
	$HcomName[$HcomComplex[$_]] = $HcomplexComName[$_];
	$HcomMsgs[$HcomComplex[$_]] = $HcomplexComMsgs[$_];
	$HcomCost[$HcomComplex[$_]] = $HcomplexComCost[$_];
	$HcomTurn[$HcomComplex[$_]] = $HcomplexComTurn[$_];
}
$HcomName[$HcomBase]            = '�ߥ�������Ϸ���';
$HcomMsgs[$HcomBase]            = '�ߥ�������ĤΤ�ɬ�ס�';
$HcomCost[$HcomBase]            = 300;
$HcomTurn[$HcomBase]            = 1;
$HcomName[$HcomMonument]        = '��ǰ���¤';
$HcomMsgs[$HcomMonument]        = "$AfterName�Υ���ܥ롣�ɲ÷��ߤ���ȡ�����";
$HcomCost[$HcomMonument]        = 9999;
$HcomTurn[$HcomMonument]        = 1;
$HcomName[$HcomCore]            = '��������';
$HcomMsgs[$HcomCore]            = "$AfterName�Υ�����";
$HcomCost[$HcomCore]            = 9999;
$HcomTurn[$HcomCore]            = 1;
$HcomName[$HcomHaribote]        = '�ϥ�ܥ�����';
$HcomMsgs[$HcomHaribote]        = '�����ܤ��ɱһ��ߡ���и��̰ʳ���̵̣����';
$HcomCost[$HcomHaribote]        = 0;
$HcomTurn[$HcomHaribote]        = 0;
$HcomName[$HcomBouha]           = '����������';
$HcomMsgs[$HcomBouha]           = '���ϣ��ޥ������Ȥ��ﳲ������ޤ�';
$HcomCost[$HcomBouha]           = 500;
$HcomTurn[$HcomBouha]           = 1;
$HcomName[$HcomDbase]           = '�ɱһ��߷���';
$HcomMsgs[$HcomDbase]           = '���ϤΥߥ�������ɤ���';
$HcomCost[$HcomDbase]           = 1000;
$HcomTurn[$HcomDbase]           = 1;
$HcomName[$HcomDbase2]          = '��®�ɱһ��߷���';
$HcomMsgs[$HcomDbase2]          = '���ϤΥߥ�������ɤ���';
$HcomCost[$HcomDbase2]          = 3000;
$HcomTurn[$HcomDbase2]          = 0;
$HcomName[$HcomMountain]        = '�η�������';
$HcomMsgs[$HcomMountain]        = '��⸻�Ȥʤ���ߡ��ҳ��˶���������20��(ʣ����)��';
$HcomCost[$HcomMountain]        = 300;
$HcomTurn[$HcomMountain]        = 1;
$HcomName[$HcomSeaMine]         = '��������';
$HcomMsgs[$HcomSeaMine]         = '�������֡����Ǥˤ���н�����̤��˲��ϻ��ꡣ';
$HcomCost[$HcomSeaMine]         = 300;
$HcomTurn[$HcomSeaMine]         = 1;
$HcomName[$HcomSbase]           = '������Ϸ���';
$HcomMsgs[$HcomSbase]           = '���˥ߥ�������Ϥ���';
$HcomCost[$HcomSbase]           = 8000;
$HcomTurn[$HcomSbase]           = 1;

foreach (0..$#HmissileName) {
	$HcomName[$HcomMissile[$_]] = $HmissileName[$_] . 'ȯ��';
	$HcomMsgs[$HcomMissile[$_]] = $HmissileMsgs[$_];
	$HcomCost[$HcomMissile[$_]] = $HmissileCost[$_];
	$HcomTurn[$HcomMissile[$_]] = $HmissileTurn[$_];
}

$HcomName[$HcomSendMonster]     = '�����ɸ�';
$HcomMsgs[$HcomSendMonster]     = '���ä�и������롣';
$HcomCost[$HcomSendMonster]     = '@������';
$HcomTurn[$HcomSendMonster]     = 1;
$HcomName[$HcomSendMonsterST]   = 'ST�����ɸ�';
$HcomMsgs[$HcomSendMonsterST]   = '���ä�и������롢���ߤ˽и�������ΤϤ��ޤ��礦';
$HcomCost[$HcomSendMonsterST]   = '@������';
$HcomTurn[$HcomSendMonsterST]   = 0; # ST��Ϣ³���Բ�

#foreach (0..$#HnavyName) {
#	$HcomName[$HcomNavy[$_]] = $HnavyName[$_] . (($HnavySpecial[$_] & 0x8) ? '����' : '��¤');
#	$HcomMsgs[$HcomNavy[$_]] = $HnavyName[$_] . '��' . (($HnavySpecial[$_] & 0x8) ? '����' : '��¤');
#	$HcomCost[$HcomNavy[$_]] = $HnavyCost[$_];
#	$HcomTurn[$HcomNavy[$_]] = 1;
#}

# ��ư���Ϥ��ѹ�
$HcomName[$HcomNavy[0]]     = '��������';
$HcomMsgs[$HcomNavy[0]]     = '��������ߤ��ޤ�';
$HcomCost[$HcomNavy[0]]     = $HnavyCost[0];
$HcomTurn[$HcomNavy[0]]     = 1;
$HcomName[$HcomNavy[1]]     = '����쥪���н�����¤';
$HcomMsgs[$HcomNavy[1]]     = '����쥪���н������¤���ޤ�';
$HcomCost[$HcomNavy[1]]     = $HnavyCost[1];
$HcomTurn[$HcomNavy[1]]     = 1;
$HcomName[$HcomNavy[2]]     = '���ѥ�������������¤';
$HcomMsgs[$HcomNavy[2]]     = '���ѥ��������������¤���ޤ�';
$HcomCost[$HcomNavy[2]]     = $HnavyCost[2];
$HcomTurn[$HcomNavy[2]]     = 1;
$HcomName[$HcomNavy[3]]     = '����ߥå���Ʈ��ȯ��';
$HcomMsgs[$HcomNavy[3]]     = '����ߥå���Ʈ����ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy[3]]     = $HnavyCost[3];
$HcomTurn[$HcomNavy[3]]     = 0;
$HcomName[$HcomNavy[4]]     = '�ۡ������ⵡȯ��';
$HcomMsgs[$HcomNavy[4]]     = '�ۡ������ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy[4]]     = $HnavyCost[4];
$HcomTurn[$HcomNavy[4]]     = 0;
$HcomName[$HcomNavy[5]]     = '���ֵ�����¤';
$HcomMsgs[$HcomNavy[5]]     = '���ֵ������¤���ޤ�';
$HcomCost[$HcomNavy[5]]     = $HnavyCost[5];
$HcomTurn[$HcomNavy[5]]     = 1;
$HcomName[$HcomNavy[6]]     = '��񹶷ⵡȯ��';
$HcomMsgs[$HcomNavy[6]]     = '��񹶷ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy[6]]     = $HnavyCost[6];
$HcomTurn[$HcomNavy[6]]     = 0;
$HcomName[$HcomNavy[7]]     = '��ƥ���������¤';
$HcomMsgs[$HcomNavy[7]]     = '��ƥ���¤�����¤���ޤ�';
$HcomCost[$HcomNavy[7]]     = $HnavyCost[7];
$HcomTurn[$HcomNavy[7]]     = 1;
$HcomName[$HcomNavy[8]]     = '�������(������)��¤';
$HcomMsgs[$HcomNavy[8]]     = '�������(������)���¤���ޤ�';
$HcomCost[$HcomNavy[8]]     = $HnavyCost[8];
$HcomTurn[$HcomNavy[8]]     = 1;
$HcomName[$HcomNavy[9]]     = '�������(���뷿)��¤';
$HcomMsgs[$HcomNavy[9]]     = '�������(���뷿)���¤���ޤ�';
$HcomCost[$HcomNavy[9]]     = $HnavyCost[9];
$HcomTurn[$HcomNavy[9]]     = 1;
$HcomName[$HcomNavy[10]]    = '�������(�ɶ���)��¤';
$HcomMsgs[$HcomNavy[10]]    = '�������(�ɶ���)���¤���ޤ�';
$HcomCost[$HcomNavy[10]]    = $HnavyCost[10];
$HcomTurn[$HcomNavy[10]]    = 1;
$HcomName[$HcomNavy[11]]    = '�������(���Ϸ�)��¤';
$HcomMsgs[$HcomNavy[11]]    = '�������(���Ϸ�)���¤���ޤ�';
$HcomCost[$HcomNavy[11]]    = $HnavyCost[11];
$HcomTurn[$HcomNavy[11]]    = 1;
$HcomName[$HcomNavy[12]]    = '�Ҥ夦�����Ҷ����¤';
$HcomMsgs[$HcomNavy[12]]    = '�Ҥ夦�����Ҷ�����¤���ޤ�';
$HcomCost[$HcomNavy[12]]    = $HnavyCost[12];
$HcomTurn[$HcomNavy[12]]    = 1;
$HcomName[$HcomNavy[13]]    = '������Ϸ�¤';
$HcomMsgs[$HcomNavy[13]]    = '������Ϥ��¤���ޤ�';
$HcomCost[$HcomNavy[13]]    = $HnavyCost[13];
$HcomTurn[$HcomNavy[13]]    = 1;
$HcomName[$HcomNavy[14]]    = '������Ϸ�¤';
$HcomMsgs[$HcomNavy[14]]    = '������Ϥ��¤���ޤ�';
$HcomCost[$HcomNavy[14]]    = $HnavyCost[14];
$HcomTurn[$HcomNavy[14]]    = 1;
$HcomName[$HcomNavy[15]]    = '�ե����ȥ쥹���ⵡȯ��';
$HcomMsgs[$HcomNavy[15]]    = '�ե����ȥ쥹���ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy[15]]    = $HnavyCost[15];
$HcomTurn[$HcomNavy[15]]    = 0;
$HcomName[$HcomNavy[16]]    = '��ڵ����������˥å���¤';
$HcomMsgs[$HcomNavy[16]]    = '��ڵ����������˥å�����¤���ޤ�';
$HcomCost[$HcomNavy[16]]    = $HnavyCost[16];
$HcomTurn[$HcomNavy[16]]    = 1;
$HcomName[$HcomNavy[17]]    = '���µ������Ϸ�¤';
$HcomMsgs[$HcomNavy[17]]    = '���µ������Ϥ��¤���ޤ�';
$HcomCost[$HcomNavy[17]]    = $HnavyCost[17];
$HcomTurn[$HcomNavy[17]]    = 1;


$HcomName[$HcomNavy2[0]]     = '����ߥå���Ʈ������ȯ��';
$HcomMsgs[$HcomNavy2[0]]     = '����ߥå���Ʈ����ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy2[0]]     = $HnavyCost[3];
$HcomTurn[$HcomNavy2[0]]     = 0;
$HcomName[$HcomNavy2[1]]     = '�ۡ������ⵡ����ȯ��';
$HcomMsgs[$HcomNavy2[1]]     = '�ۡ������ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy2[1]]     = $HnavyCost[4];
$HcomTurn[$HcomNavy2[1]]     = 0;
$HcomName[$HcomNavy2[2]]     = '��񹶷ⵡ����ȯ��';
$HcomMsgs[$HcomNavy2[2]]     = '��񹶷ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy2[2]]     = $HnavyCost[6];
$HcomTurn[$HcomNavy2[2]]     = 0;
$HcomName[$HcomNavy2[3]]    = '�ե����ȥ쥹���ⵡ����ȯ��';
$HcomMsgs[$HcomNavy2[3]]    = '�ե����ȥ쥹���ⵡ��ȯ�ʤ��ޤ�';
$HcomCost[$HcomNavy2[3]]    = $HnavyCost[15];
$HcomTurn[$HcomNavy2[3]]    = 0;


$HcomName[$HcomNavyMove]        = '���ư';
$HcomMsgs[$HcomNavyMove]        = "�ɸ������Ԥζ��̤ʤ�$AfterName����$AfterName�ش�����ư���ޤ�";
$HcomCost[$HcomNavyMove]        = 0;
$HcomTurn[$HcomNavyMove]        = 1;
$HcomName[$HcomNavySend]        = '�����ɸ�';
$HcomMsgs[$HcomNavySend]        = '������ɸ����ޤ�';
$HcomCost[$HcomNavySend]        = 0;
$HcomTurn[$HcomNavySend]        = 1;
$HcomName[$HcomNavyReturn]      = '���ⵢ��';
$HcomMsgs[$HcomNavyReturn]      = '�ɸ�����򵢴Ԥ��ޤ�';
$HcomCost[$HcomNavyReturn]      = 0;
$HcomTurn[$HcomNavyReturn]      = 1;
$HcomName[$HcomNavyForm]        = '������';
$HcomMsgs[$HcomNavyForm]        = '�����ν�°�������̻�����ѹ����ޤ�';
$HcomCost[$HcomNavyForm]        = 0;
$HcomTurn[$HcomNavyForm]        = 0;
$HcomName[$HcomNavyExpell]      = '��������';
$HcomMsgs[$HcomNavyExpell]      = '�������°�����ˤ����ޤ�';
$HcomCost[$HcomNavyExpell]      = 0;
$HcomTurn[$HcomNavyExpell]      = 0;
$HcomName[$HcomNavyDestroy]     = '�����˴�';
$HcomMsgs[$HcomNavyDestroy]     = '�����򳤤ˤ����ޤ�';
$HcomCost[$HcomNavyDestroy]     = 0;
$HcomTurn[$HcomNavyDestroy]     = 0;
$HcomName[$HcomNavyWreckRepair] = '�ĳ�����';
$HcomMsgs[$HcomNavyWreckRepair] = '�������������ϴ���˲ä��ޤ�';
$HcomCost[$HcomNavyWreckRepair] = '@����';
$HcomTurn[$HcomNavyWreckRepair] = 1;
$HcomName[$HcomNavyWreckSell]   = '�ĳ����';
$HcomMsgs[$HcomNavyWreckSell]   = '��ѻ��˶����ȯ�����뤳�Ȥ⤢��ޤ�';
$HcomCost[$HcomNavyWreckSell]   = '@����';
$HcomTurn[$HcomNavyWreckSell]   = 1;
$HcomName[$HcomMoveTarget]      = '��ư���';
$HcomMsgs[$HcomMoveTarget]      = '���Ϥ��Ф��ư�ư������ؼ��Ǥ��ޤ�';
$HcomCost[$HcomMoveTarget]      = 0;
$HcomTurn[$HcomMoveTarget]      = 0;
$HcomName[$Hcomgoalsetpre]      = '��Ū�ϻ���(�о�)';
$HcomMsgs[$Hcomgoalsetpre]      = '��ư�����ؼ��ν�����Ԥ��ޤ�';
$HcomCost[$Hcomgoalsetpre]      = 0;
$HcomTurn[$Hcomgoalsetpre]      = 0;
$HcomName[$Hcomgoalset]         = '��Ū�ϻ���(��ɸ)';
$HcomMsgs[$Hcomgoalset]         = '��ư������ؼ����ޤ�';
$HcomCost[$Hcomgoalset]         = 0;
$HcomTurn[$Hcomgoalset]         = 0;
$HcomName[$HcomWarpA]           = '���������ư(��ư��)';
$HcomMsgs[$HcomWarpA]           = '�����򷳹������̤η����ذ�ư�����ޤ�';
$HcomCost[$HcomWarpA]           = 0;
$HcomTurn[$HcomWarpA]           = 0;
$HcomName[$HcomWarpB]           = '���������ư(��ư��)';
$HcomMsgs[$HcomWarpB]           = '�����򷳹������̤η����ذ�ư�����ޤ�';
$HcomCost[$HcomWarpB]           = 0;
$HcomTurn[$HcomWarpB]           = 1;
$HcomName[$Hcomremodel]         = '��������(����/����/�ɶ�/����)';
$HcomMsgs[$Hcomremodel]         = '������Ϥ�������ޤ�';
$HcomCost[$Hcomremodel]         = 0;
$HcomTurn[$Hcomremodel]         = 0;
$HcomName[$Hcomwork]            = '����Ÿ��(����/����/�η�/����)';
$HcomMsgs[$Hcomwork]            = '���ѥ�������������Ÿ�����ޤ�';
$HcomCost[$Hcomwork]            = 0;
$HcomTurn[$Hcomwork]            = 1;
$HcomName[$HcomSellPort]        = '����ʧ����';
$HcomMsgs[$HcomSellPort]        = '������̱�֤�ʧ�������ޤ�';
$HcomCost[$HcomSellPort]        = 0;
$HcomTurn[$HcomSellPort]        = 1;
$HcomName[$HcomBuyPort]         = '�������';
$HcomMsgs[$HcomBuyPort]         = '̱�֤η�����������ޤ�';
$HcomCost[$HcomBuyPort]         = 6000;
$HcomTurn[$HcomBuyPort]         = 1;

$HcomName[$HcomMoveMission]     = '��ư����';
$HcomMsgs[$HcomMoveMission]     = '������Ф��ư�ư��ɸ��ؼ��Ǥ��ޤ����������ޤ�ͭ���Ǥ�����ΰ̤������ֹ桦���ΰ̤�9��Ĥ���Ȳ��';
$HcomCost[$HcomMoveMission]     = 0;
$HcomTurn[$HcomMoveMission]     = 0;
$HcomName[$HcomNavyMission]     = '���������ѹ�';
$HcomMsgs[$HcomNavyMission]     = '�̾�(0)�����(1)���༣(2)������(3)���ڤ��ؤ������ΰ̤Ǵ������Ǥ��ޤ�';
$HcomCost[$HcomNavyMission]     = 0;
$HcomTurn[$HcomNavyMission]     = 0;
$HcomName[$HcomNavyTarget]      = '���ƹ���';
$HcomMsgs[$HcomNavyTarget]      = '���ꤷ�������������ˤ�Ĵ����ι����оݤˤ������Ǥ�';
$HcomCost[$HcomNavyTarget]      = 1000;
$HcomTurn[$HcomNavyTarget]      = 1;
$HcomName[$Hcomshikin]           = '�׻�����';
$HcomMsgs[$Hcomshikin]           = "2000$HunitMoney���⤢�ꡣ";
$HcomCost[$Hcomshikin]           = 0;
$HcomTurn[$Hcomshikin]           = 1;

$HcomName[$HcomAmity]           = 'ͧ��������ꡦ���';
$HcomMsgs[$HcomAmity]           = "���ꤷ��$AfterName�ؤϴ������⤷�ʤ��ʤ�ޤ�";
$HcomCost[$HcomAmity]           = 0;
$HcomTurn[$HcomAmity]           = 0;
$HcomName[$HcomAlly]            = 'Ʊ���ز�����æ��';
$HcomMsgs[$HcomAlly]            = "����⤷����Ʊ����°��$AfterName����ꤷ�ޤ�";
$HcomCost[$HcomAlly]            = 0;
$HcomTurn[$HcomAlly]            = 1;
$HcomName[$HcomDeWar]           = '�����۹�';
$HcomMsgs[$HcomDeWar]           = '�����˻��ꤹ�륳�ޥ�ɤǤ�';
$HcomCost[$HcomDeWar]           = 0;
$HcomTurn[$HcomDeWar]           = 0;
$HcomName[$HcomCeasefire]       = '�����ǿ�';
$HcomMsgs[$HcomCeasefire]       = '������֤������뤿��ˤϹ�դ�ɬ�פǤ�';
$HcomCost[$HcomCeasefire]       = 0;
$HcomTurn[$HcomCeasefire]       = 0;

$HcomName[$HcomSell]            = '����͢��';
$HcomMsgs[$HcomSell]            = '��������ˤ����ޤ�';
$HcomCost[$HcomSell]            = -1000;
$HcomTurn[$HcomSell]            = 0;
$HcomName[$HcomBuy]             = '����͢��';
$HcomMsgs[$HcomBuy]             = '�������ˤ����ޤ�';
$HcomCost[$HcomBuy]             = 100;
$HcomTurn[$HcomBuy]             = 0;
$HcomName[$HcomMoney]           = '�����';
$HcomMsgs[$HcomMoney]           = '����̤���̻��ꤷ�ޤ�';
$HcomCost[$HcomMoney]           = 100;
$HcomTurn[$HcomMoney]           = 0;
$HcomName[$HcomFood]            = '�������';
$HcomMsgs[$HcomFood]            = '����̤���̻��ꤷ�ޤ�';
$HcomCost[$HcomFood]            = -100;
$HcomTurn[$HcomFood]            = 0;
$HcomName[$HcomPropaganda]      = 'Ͷ�׳�ư';
$HcomMsgs[$HcomPropaganda]      = '�͸��������ޤ�';
$HcomCost[$HcomPropaganda]      = 1000;
$HcomTurn[$HcomPropaganda]      = 1;
$HcomName[$HcomGiveup]          = "${AfterName}������";
$HcomMsgs[$HcomGiveup]          = '�礬�ʤ��ʤ�ޤ�';
$HcomCost[$HcomGiveup]          = 0;
$HcomTurn[$HcomGiveup]          = 1;
$HcomName[$HcomDoNothing]       = '�Ŵ�';
$HcomMsgs[$HcomDoNothing]       = "$HdoNothingMoney$HunitMoney���⤢�ꡣ��ư��������ա�";
$HcomCost[$HcomDoNothing]       = 0;
$HcomTurn[$HcomDoNothing]       = 1; # 0�ˤ��Ƥ�1������Ǥ�(^^)V

$HcomName[$HcomAutoPrepare]     = '���ϼ�ư����';
$HcomMsgs[$HcomAutoPrepare]     = '��������Ϥˤ��٤����Ϥ򥻥å�';
$HcomCost[$HcomAutoPrepare]     = 0;
$HcomTurn[$HcomAutoPrepare]     = 0;
$HcomName[$HcomAutoPrepare2]    = '�Ϥʤ餷��ư����';
$HcomMsgs[$HcomAutoPrepare2]    = '��������Ϥˤ��٤��Ϥʤ餷�򥻥å�';
$HcomCost[$HcomAutoPrepare2]    = 0;
$HcomTurn[$HcomAutoPrepare2]    = 0;
$HcomName[$HcomAutoDelete]      = '���ײ�����ű��';
$HcomMsgs[$HcomAutoDelete]      = '�ײ����������ʤ�����������';
$HcomCost[$HcomAutoDelete]      = 0;
$HcomTurn[$HcomAutoDelete]      = 0;
$HcomName[$HcomAutoReclaim]     = '�������Ω�Ƽ�ư����';
$HcomMsgs[$HcomAutoReclaim]     = '�����������ˤ��٤����Ω�Ƥ򥻥å�';
$HcomCost[$HcomAutoReclaim]     = 0;
$HcomTurn[$HcomAutoReclaim]     = 0;
$HcomName[$HcomAutoDestroy]     = '�������Ｋư����';
$HcomMsgs[$HcomAutoDestroy]     = '�����������ˤ��٤Ʒ���򥻥å�';
$HcomCost[$HcomAutoDestroy]     = 0;
$HcomTurn[$HcomAutoDestroy]     = 0;
$HcomName[$HcomAutoSellTree]    = 'Ȳ�μ�ư����';
$HcomMsgs[$HcomAutoSellTree]    = '���̤ο�(ñ��ɴ)��꾯�ʤ������о�';
$HcomCost[$HcomAutoSellTree]    = 0;
$HcomTurn[$HcomAutoSellTree]    = 0;
$HcomName[$HcomAutoForestry]    = 'Ȳ�Ρ����Ӽ�ư����';
$HcomMsgs[$HcomAutoForestry]    = '���̤ο�(ñ��ɴ)��꾯�ʤ�����Ȳ�Τ��������˿��Ӥ��ʤ�����';
$HcomCost[$HcomAutoForestry]    = 0;
$HcomTurn[$HcomAutoForestry]    = 0;

1;