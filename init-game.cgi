#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# ゲーム設定モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 各種設定値
# (これ以降の部分の各設定値を、適切な値に変更してください)
#----------------------------------------------------------------------

# 勝利した島名(陣営名)の前につける称号(終了ターン時・陣営モード・サバイバルモード・トーナメントモード共通設定)
# 称号
@HwinnerTitle = (
	'COMPLETE！', # アイテムコンプ用
	'海戦覇者',
	);
# マーク
@HwinnerMark = ( # 画像の場合
	'trophy2[gold].gif', # アイテムコンプ用
	'king[yellow].gif',
	); # ヨッシーの素材集 http://homepage2.nifty.com/yoshi-m/sozai/
#@HwinnerMark = ( # テキストの場合
#	'【COMPLETE！】', # アイテムコンプ用
#	'【勝者！】'
#	);
# マーク表示を１つだけにするか？(0:しない、1:する)
$HviewMarkOne = 0;

# 新しい島を探せるのは管理人だけ？(0:いいえ、1:はい)
# （管理人だけの場合は $HjoinGiveupTurn を小さくしてください）
$HadminJoinOnly = 0;

# 新規登録された島の開発期間
# （開発期間は、他の島への援助、他の島への攻撃、が禁止される）
$HdevelopTurn = 50;

# 放棄コマンド自動入力ターン数（開発期間）
$HdevelopGiveupTurn = 4;

# 放棄コマンド自動入力ターン数
$HgiveupTurn = 24;

# 新しい島を見つけた直後の放置ターン数（何ターン放置されていたことにするか）
$HjoinGiveupTurn = $HgiveupTurn - 3;

# 新しい島を見つけた時のコメント欄
$HjoinComment = '(未登録)';
# コメント欄が発見時のままの場合、管理人あずかりにする？(0:しない)
$HjoinCommentPenalty = 0; # 1なら発見ターンの次のターン更新時に判定。2以上で猶予をもたせることが可能。
# この機能を設定一覧に表示するか？
#    しない場合は、""
#    する場合は、"原則として受け付けない", "<a href='〜'>掲示板</a>で受け付ける", "<a href="mailto:〜>メール</a>で受け付ける"など
#$HjoinCommentPenaltyStr = "受け付けません。発見次第、<B>島を削除</B>します。"; # 『管理人あずかり解除依頼は「(ここに入る言葉)」』
$HjoinCommentPenaltyStr = "";

# 無人化自動回避・死滅判定回避機能の使用(0:使用しない、1:死滅判定回避、2〜:無人化自動回避)
#「島の放棄」以外では死滅処理をしない。
# 他島に派遣中の艦艇や自島(処理対象の島)に出現中の怪獣・巨大怪獣は海になり消滅。
# 他島から自島へ派遣されている艦隊は、帰還処理される。
# 1:死滅判定回避の場合
#    管理人あずかりにする。
# 2〜:無人化自動回避の場合
#    初期設定の人口で開発期間になる(「陣営モード」「サバイバルモード」「トーナメントモード」では使用不可)
#    ただし、人口が０になった場合、荒地か平地がなければ沈没してしまう。
$HautoKeeper = 0; # 人口がこの設定値を下回ると発動

# 死滅判定回避による「管理人あずかり」の自動解除ターン数？(0:無期限、1〜99999998:ターン数)
$HautoKeeperSetTurn = 24;

# 「管理人あずかり」でも最初のコマンドが「島の放棄」なら死滅処理をするか？(0:いいえ、1:はい)
$HforgivenGiveUp = 1;

# 「管理人あずかり」の島への攻撃(艦隊派遣・怪獣派遣・ミサイル攻撃)を許可するか？(0:いいえ、1:はい)
$HforgivenAttack = 0;

# 死滅処理で削除される島データをトーナメントの敗者の島として扱い保存するか？(0:いいえ、1:はい、2:強制削除も保存する)
$HdeadToSaveAsLose = 2;

#----------------------------------------
# コア
#----------------------------------------
# 建設コマンドを使うか？(0:禁止)
$HuseCore = 0;

# 建設できるのは新規登録された島の開発期間だけ？(0:制限なし、1:新規登録された島の開発期間だけ)
$HuseCoreLimit = 0;

# 保有可能数を指定
$HcoreMax = 0; # 0:無制限

# 耐久力設定
$HdurableCore = 3; # 最大値(0だと通常、最大で99まで)

# コアを偽装するか？(1:する、0:しない)
$HcoreHide = 0;

# コアを保有しない島は沈没する？(注！新規登録された島の開発期間は沈没しません。)
$HcorelessDead = 0; # 0:沈没しない、1:沈没する、2:死滅判定回避機能発動(自動解除ターン数は$HautoKeeperSetTurnで設定)

# 画像ファイルはhako-init.cgiで設定

#----------------------------------------
# ゲームの進行やファイルなど
#----------------------------------------
# トップページに表示する島の数
# （これより増えると複数ページに分けられます）
$HviewIslandCount = 10;

# バックアップを何ターンおきに取るか
$HbackupTurn = 12;

# バックアップを何回分残すか
$HbackupTimes = 4;

# 発見ログ保持行数(10より大きくすると表示が崩れます。下の数値で調整して下さい)
$HhistoryMax = 100;
# 記事表示部の最大の高さ。
# heightの指定値を超えるとスクロールバーが表示されます。
$HdivHeight = 120; # <DIV style="overflow:auto; height:${HdivHeight}px;">

# リアルタイマーの使用(0:使用しない、1:使用する)
$Hrealtimer = 1;

# 開発画面でポップアップナビを表示するか？(0:使用しない、1:使用する)
$HpopupNavi = 1;

# 歴代ランキングを記録するか？(詳細設定はhako-reki.cgiで行うことができます)
$HuseRekidai = 1;

# 艦艇の周囲が埋め立てできる裏ワザ(バグ?)を修正するか？(0:しない、1:する)
$HnavyReclaim = 1;

# 怪獣(海にいる)の周囲が埋め立てできる裏ワザ(バグ?)を修正するか？(0:しない、1:する)
$HmonsterReclaim = 1;

# ST怪獣派遣、STミサイル発射の裏ワザ(バグ?)を修正するか？(0:しない、1:する)
$HattackST = 1;

# 島の最外周を埋め立て不可にするか？(0:しない、1:する)
# 座標の一方が、($HedgeReclaim - 1)以下 か ($HislandSizeX(orY) - $HedgeReclaim)以上の地点を埋め立てできなくするということです。
# 注！噴火で陸地になることはあります。
$HedgeReclaim = 1; # $HislandSizeX(orY)/2よりも小さい正数を設定

# 着弾点をマップ表示可能にするか？(0:しない、1:する)
$HmlogMap = 1;

# 他人から資金を見えなくするか
# 0 見えない
# 1 見える
# 2 100の位で四捨五入
$HhideMoneyMode = 0;

# 整地系ログのまとめに座標も出力する？(0:しない 1:する)
# 整地・地ならし・埋め立て・掘削・伐採
$HoutPoint = 1;

# 各島の収支ログ(機密)を出力する？(0:しない 1:する)
$HbalanceLog = 1;

# JavaScriptの一部を外部ファイル化するか？(0:しない 1:する)
$HextraJs = 0;

#----------------------------------------------------------------------
# コマンド関連設定
#----------------------------------------------------------------------
# 複合地形系(複合地形と重複する機能の地形がある場合の禁止設定)
#-------------------------------------------------------------
# 「工場建設」を使うか？(0:禁止)
$HuseFactory = 0;

# 「農場整備」を使うか？(0:禁止)
$HuseFarm = 0;

# 「採掘場整備」を使うか？(0:禁止)
$HuseMountain = 0;

# 「植林・伐採」を使うか？(0:禁止)
$HusePlantSellTree = 1;

# 高速系(ターン消費なし)
#-----------------------
# 伐採をターン消費なしにするか？(0:しない、1:する)
$HnoturnSellTree = 1;

# 「高速埋め立て」を使うか？(0:禁止)
$HuseFastReclaim = 1;

# 「高速掘削」を使うか？(0:禁止)
$HuseFastDestroy = 1;

# 「高速工場建設」を使うか？(0:禁止)
$HuseFastFactory = 1;

# 「高速農場整備」を使うか？(0:禁止) ※トーナメントモードで使用。
$HuseFastFarm = 1;

# 「一括地ならし」を使うか？(0:禁止) ※サバイバルモードで使用。
$HusePrepare3 = 1;
# 一括自動地ならし用
$precheap  = 10; # 何個目の荒地から割り引きか（この数の次の荒地から）
$precheap2 =  8; # その際の割引率（8にしたら、2割引ということになります）
#----------------------------------------
# 島の新規登録時の設定
#----------------------------------------
# 島の面積を統一するか？
$HnewIslandSetting = 0;

# 統一時の設定
$HcountLandArea     = 32; # 陸地の数(通常:32) 注！16より小さい値にしても最低16はできます。
$HcountLandSea      = 16; # 海(浅瀬)の数(通常:16)

$HcountLandWaste    = 8;  # 荒地の数(通常:8)
$HcountLandForest   = 4;  # 森の数(通常:4)
$HcountLandTown     = 2;  # 町の数:無人化回避機能でも有効(通常:2 サバイバル:10)
$HcountLandMountain = 1;  # 山の数(通常:1 サバイバル:0)
$HcountLandPort     = 0;  # 軍港の数(通常:0 サバイバル:0)
$HcountLandBase     = 0;  # 基地の数(通常:1 サバイバル:0  注！使用時のみ)

# 規模の設定(統一してもしなくても有効)
$HvalueLandForest   = 5;  # 森の規模(通常:5 サバイバル:10)
$HvalueLandTown     = 5;  # 町の規模(通常:5 サバイバル:100)
$HvalueLandMountain = 0;  # 山(採掘場)の規模(通常:0)
#注・森や採掘場は複合地形ではありません！
#----------------------------------------
# 資金、食料などの設定値と単位
#----------------------------------------
# 「資金繰り」での収入(通常は、ノーマル:10, サバイバル:100)
$HdoNothingMoney = 10;

# 最大資金
$HmaximumMoney = 100000;

# 最大食料
$HmaximumFood = 500000;

# お金の単位
$HunitMoney = '億円';

# 食料の単位
$HunitFood = '00トン';

# 人口の単位
$HunitPop = '00人';

# 広さの単位
$HunitArea = '00万坪';

# 木の数の単位
$HunitTree = '00本';

# 木の単位当たりの売値
$HtreeValue = 5;

# 1ターンで増える木の本数(単位当たり)通常は1
$HtreeGrow = 3;

# 名前変更のコスト
$HcostChangeName = 500;

# 人口1単位あたりの食料消費料
$HeatenFood = 0.2;

# 怪獣の数の単位
$HunitMonster = '匹';

# 難易度調整（食料・資金の収入倍率：通常レートに対する倍率）
$HincomeRate = 1;

#----------------------------------------
# ミサイル関連
#----------------------------------------
# ミサイル基地を使うか？(0:禁止)
# （海戦のバランスを考えると使わないことを推奨します）
$HuseBase = 0;

# 海底基地を使うか？(0:禁止)
# （海戦のバランスを考えると使わないことを推奨します）
$HuseSbase = 0;

# 基地の経験値
#----------------------------------------
# 経験値の最大値
$HmaxExpPoint = 200; # ただし、最大でも255まで

# レベルの最大値
$maxBaseLevel  = 5;  # ミサイル基地
$maxSBaseLevel = 3; # 海底基地

# 経験値がいくつでレベルアップか
@baseLevelUp  = (20, 60, 120, 200); # ミサイル基地
@sBaseLevelUp = (50, 200); # 海底基地

my($num, $cno);
#----------------------------------------
# ミサイル
#----------------------------------------
# STミサイルを使うか？(0:禁止)
$HuseMissileST = 0;

# 射程内に怪獣・巨大怪獣がいなければ、ミサイルを発射中止にするか？(0:しない、1:する)
$HtargetMonster = 0;

# ミサイルで被弾した艦艇や地形が自島の場合、無害にするか？（0:しない、1:する、2:友好国も無害にする）
$HmissileSafetyZone = 2;
# 無害化が無効になる確率(%) ※無害化機能が発動する場面で判定
$HmissileSafetyInvalidp = 0;

# ミサイルの種類(最大10種類)
### ミサイル
$num = 0; # 配列番号
$HmissileName[$num] = 'ミサイル';         # 名前
$HmissileMsgs[$num] = '誤差2';            # ミサイルの説明
$HmissileCost[$num]    = 20;              # 発射費用
$HmissileTurn[$num]    = 1;               # ターン消費(STの連続は不可)
$HmissileDamage[$num]  = 0;               # 破壊力(命中時のダメージ) ※耐久力のある地形が対象。設定なしで1なので、2以上の数値を設定する場合に使用。
$HmissileErr[$num]     = 2;               # 誤差(Hex)
$HmissileSpecial[$num] = 0x0;             # 属性
# 0x0 なし
# 0x1 ST(ステルスミサイル)発射した島名がログに表示されません。
# 0x2 陸地破壊(山→荒地(陸系地形)→浅瀬(海系地形)→海)
# 0x4 絨毯爆撃(初弾の着弾点の周囲数ヘックスを攻撃)
# 0x10 硬化無効(対怪獣・巨大怪獣)
# 0x20 潜水無効(対怪獣・巨大怪獣・潜水能力保有艦・機雷・海底施設)

#「絨毯爆撃」周囲何Hex対象か？※1〜2を設定。
$HmissileTerrorHex[$num] = 0;# 完全に絨毯爆撃するには1Hex:7発，2Hex:19発が必要です。結果的に攻撃誤差が広がることになります。

### PPミサイル
$num = 1; # 配列番号
$HmissileName[$num]      = 'PPミサイル';   # 名前
$HmissileMsgs[$num]      = '誤差1';        # 説明
$HmissileCost[$num]      = 50;             # 発射費用
$HmissileTurn[$num]      = 1;              # ターン消費
$HmissileDamage[$num]    = 0;              # 破壊力 ※設定なしで1
$HmissileErr[$num]       = 1;              # 誤差(Hex)
$HmissileSpecial[$num]   = 0x0;            # 属性
$HmissileTerrorHex[$num] = 0;              #「絨毯爆撃」Hex

### STミサイル
$num = 2; # 配列番号
$HmissileName[$num]      = 'STミサイル';   # 名前
$HmissileMsgs[$num]      = '誤差2、むやみに撃つのはやめましょう'; # 説明
$HmissileCost[$num]      = 50;             # 発射費用
$HmissileTurn[$num]      = 0;              # ターン消費
$HmissileDamage[$num]    = 0;              # 破壊力 ※設定なしで1
$HmissileErr[$num]       = 2;              # 誤差(Hex)
$HmissileSpecial[$num]   = 0x1;            # 属性
$HmissileTerrorHex[$num] = 0;              #「絨毯爆撃」Hex

### 陸地破壊弾
$num = 3; # 配列番号
$HmissileName[$num]      = '陸地破壊弾';   # 名前
$HmissileMsgs[$num]      = '誤差2、陸破壊(山→荒地→浅瀬→海)'; # 説明
$HmissileCost[$num]      = 100;            # 発射費用
$HmissileDamage[$num]    = 0;              # 破壊力 ※設定なしで1
$HmissileTurn[$num]      = 1;              # ターン消費
$HmissileErr[$num]       = 2;              # 誤差(Hex)
$HmissileSpecial[$num]   = 0x2;            # 属性
$HmissileTerrorHex[$num] = 0;              #「絨毯爆撃」Hex

### 拡散ミサイル
#$num = 4; # 配列番号
#$HmissileName[$num]      = '拡散ミサイル'; # 名前
#$HmissileMsgs[$num]      = '誤差2、着弾点の周囲1Hexを破壊。費用は1発あたりで7発以上の発射能力と設定が必要'; # 説明
#$HmissileCost[$num]      = 100;            # 発射費用
#$HmissileTurn[$num]      = 1;              # ターン消費
#$HmissileDamage[$num]    = 0;              # 破壊力 ※設定なしで1
#$HmissileErr[$num]       = 2;              # 誤差(Hex)
#$HmissileSpecial[$num]   = 0x4;            # 属性
#$HmissileTerrorHex[$num] = 1;              #「絨毯爆撃」Hex

#----------------------------------------
# 防衛施設
#----------------------------------------
# 保有可能数を指定
$HdBaseMax = 10; # 0:無制限

# 怪獣に踏まれた時自爆するか？(1:する、0:しない)
$HdBaseAuto = 0;

# 防衛施設を森に偽装するか？(1:する、0:しない)
$HdBaseHide = 0;

# 自島の攻撃は自島の防衛圏(他島の防衛圏でない地点)に着弾できるようにするか？※つまり防衛しないということ。(防衛の無効化)
# (0:着弾しない(防衛するということ)、1:自島の攻撃のみ着弾、2:友好国に設定してくれている島の攻撃も着弾、3:友好国に設定している島の攻撃も着弾、4:友好国に設定している島の攻撃も友好国に設定してくれている島の攻撃も着弾)
$HdBaseSelfNoDefenceNV = 1; # 艦隊攻撃
$HdBaseSelfNoDefenceMS = 1; # ミサイル攻撃
$HdBaseSelfNoDefenceMA = 1; # 怪獣のミサイル攻撃

# 耐久力設定
$HdurableDef = 5; # 最大値(0だと通常、最大98)
$HdefLevelUp = 3; # 耐久力がこの設定数値以上になると防衛範囲が３ヘックスになります。
# 注！これを設定している時に、自爆させたい場合は数量「99」を指定しなければなりません。
#     0も1も耐久力の最大値は1ですが、0だと追加建設で自爆、1だと「99」で自爆です。
$HdefExplosion = 100; # 自爆の数量を「99」以外にしたい場合に変更。100以上にすれば自爆できなくなります。
#----------------------------------------
# 災害
#----------------------------------------
# 通常災害発生率(確率は0.1%単位)
$HdisEarthquake = 0;  # 地震
$HdisTyphoon    = 20; # 台風
$HdisMeteo      = 15; # 隕石
$HdisHugeMeteo  = 0;  # 巨大隕石
$HdisEruption   = 0; # 噴火
$HdisFire       = 100; # 火災
$HdisMaizo      = 10; # 埋蔵金

# 津波
$HdisTsunami     = 0; # 発生率
$HdisTsunamiDmax = 0;  # 津波が海軍に与えるダメージの最大値
$HdisTsunamiFsea = 20; # 海の面積フラグ：これを下回ると津波発生確率が高くなる。

# 地盤沈下
$HdisFallBorder = 90; # 安全限界の広さ(Hex数)
$HdisFalldown   = 30; # その広さを超えた場合の確率

#----------------------------------------
# 防波堤・機雷
#----------------------------------------
# 防波堤を使うか？(0:禁止) ※使う場合、bouha.gifが必要です。
$HuseBouha = 0; # 保有可能数を指定

# 機雷を使うか？(0:禁止) ※使う場合、seamine.gifが必要です。
$HuseSeaMine = 10; # 設置可能数を指定
# 破壊力の最大値
$HmineDamageMax = 9;
# 自島の機雷でダメージを受けるか？(0:受ける、1:受けない、2:友好国も受けない)
$HmineSelfDamage = 2;

#----------------------------------------
# 油田
#----------------------------------------
# 油田の収入
$HoilMoney = 1000;

# 油田収入をランダムにする(0:しない、1〜:最小値を設定する。$HoilMoneyが最大値になる)
$HoilMoneyMin = 0;

# 油田の枯渇確率
$HoilRatio = 40;

#----------------------------------------
# 都市系設定
#----------------------------------------
# 名称
#@HlandTownName  = ('村', '町', '都市', '大都市', '巨大都市', '超巨大都市');
@HlandTownName  = ('初期都市', '1万都市','2万都市','3万都市','4万都市','5万都市','6万都市','7万都市','8万都市','9万都市','10万都市');

# 画像
#@HlandTownImage = ('land3.gif', 'land4.gif', 'land5.gif', 'land41.gif', 'land42.gif', 'land43.gif');
@HlandTownImage = ('landtown0.gif','landtown1.gif','landtown2.gif','landtown3.gif','landtown4.gif',
                   'landtown5.gif','landtown6.gif','landtown7.gif','landtown8.gif','landtown9.gif','landtown10.gif');

# ランクアップに必要な地形の値の最小値(地形の値がこれ以上になるとランクアップ)
#@HlandTownValue  = (   0, 30, 100, 200, 300, 400);
@HlandTownValue  = (   0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000);

# 難民受け入れの上限(難民受け入れ後の都市の規模ではなくて、受け入れる人数の元になる数値)
#@HachiveValueMax   = (  50, 50,  50,  50,  50,  50); # すでに都市系の場合
@HachiveValueMax   = (900,800,700,600,500,400,300,200,100,50,0); # すでに都市系の場合
$HachivePlainsMax  = 10; # 平地への受け入れ上限(通常:10)
$HachivePlainsLoss = 5;  # 平地受け入れ時のロス(通常:5)
# 注！Max10,Loss5で実質平地への受け入れは最大5です。難民受け入れで平地が都市系になるたび5の難民が消えます。

# 成長の最大値(地形の値 Max:1000000000)
#$HvalueLandTownMax = 500; # 通常 200(20000人）
$HvalueLandTownMax = 1000;

# 人口の増加幅（10だと最大1000人）
#@Haddpop        = (  10, 10, 10, 10, 10,  0); # 通常(村, 町, 都市)=(10, 10, 0)
#@HaddpopPropa   = (  30, 30, 20, 20, 20, 10); # 誘致活動中 通常(村, 町, 都市)=(30, 30, 10)
#@HaddpopSD      = (  40, 40, 20, 20, 20,  0); # サバイバル開発期間 通常(40, 40, 0)
#@HaddpopSDpropa = (  60, 60, 30, 30, 30, 10); # サバイバル開発期間 誘致活動中(60, 60, 10)
#@HaddpopSA      = (   5,  5,  5,  5,  5,  0); # サバイバル戦闘期間 通常(5, 5, 0)
#@HaddpopSApropa = (  10, 10, 10, 10, 10,  3); # サバイバル戦闘期間 誘致活動中(10, 10, 3)
@Haddpop        = (  10, 50, 30,0,0,0,0,0,0,0,0);
@HaddpopPropa   = (  50, 30, 10,5,3,0,0,0,0,0,0);
@HaddpopSD      = (  40, 40,  0);
@HaddpopSDpropa = (  60, 60, 10);
@HaddpopSA      = (   5,  5,  0);
@HaddpopSApropa = (  10, 10,  3);

# 食糧不足の場合の人口減少値(マイナスの値)
@HreductionPop  = ( -10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10); # 通常 -30

#  ポップアップナビ解説部分(設定によって書き換える必要あり)
$HnaviExp.=<<"END";
TOWN0  = "初期都市";
TOWN1  = "1万都市";
TOWN2  = "2万都市";
TOWN3  = "3万都市";
TOWN4  = "4万都市";
TOWN5  = "5万都市";
TOWN6  = "6万都市";
TOWN7  = "7万都市";
TOWN8  = "8万都市";
TOWN9  = "9万都市";
TOWN10 = "10万都市";


END

# 村の発生率（％）
$HtownGlow = 50; # 通常 20 トーナメント 25

# 艦艇攻撃・ミサイル攻撃命中時、一撃で荒れ地にならず都市ランクが下がるようにするか？(1:する、0:しない)
$HtownStepDown = 1;
# ランク２まで（村・町）は一撃で破壊されます。
#----------------------------------------
# 複合地形
#----------------------------------------
# 複合地形を使うか？(0:禁止)
$HuseComplex = 1;

#  ターン更新時属性
# 「ランダム収入」最小値と最大値
@HcomplexRinMoney = (10, 100);
# 「ランダム収穫」最小値と最大値
@HcomplexRinFood = (10, 100);
# 「力場能力」周囲何Hexの怪獣・巨大怪獣を瞬殺するか？
$HcomplexFieldHex = 1;

# 複合地形の地形設定(最大32種類)
#-------------------------------
### 農場
#$num = 0; # 配列番号

# 名称
#$HcomplexName[$num] = '農場';

# 複合地形の画像ファイル
#$HcomplexImage[$num] = 'land7.gif';

# 保有(建設)可能最大数(0:無制限)
#$HcomplexMax[$num] = 0;

# 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # 3のときの名前
#$HcomplexPretendImage[$num] = ''; # 3のときの画像
#$HcomplexPretendNavi[$num]  = ''; # ポップアップナビ解説 'SEA0'とか'FOREST'とか

# ランクアップ設定
#$HcomplexLevelKind[$num] = 'food'; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
#$HcomplexLevelValue[$num] = [0, 20, 40]; # ランクアップに必要なフラグ値の最小値
#$HcomplexSubName[$num] = ['農場(Lv1)', '農場(Lv2)', '農場(Lv3)'];# 名称
#$HcomplexSubImage[$num] = ['land7.gif', 'land7.gif', 'land7.gif'];# 画像

# 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# 複合地形($HlandComplex)以外
#$HcomplexBefore2[$num] = []; # 複合地形を建設可能な「別種の複合地形($HlandComplex)」の種類(複数の場合は，[1, 3]のようにコンマで区切る)  ※別種のみ配列番号で指定。同種の複合地形は記述不要

# ターンフラグ設定:建設時を1としてターン更新ごとに+1される値
#$HcomplexTPCmax[$num] = 0;  # 最大値(Max500) 
#$HcomplexTPname[$num] = ''; # 名称 ..たとえば、'木の数','大都市'
#$HcomplexTPrate[$num] = 0;  # 表示倍率 フラグにこの倍率をかけた数値が表示値
#$HcomplexTPunit[$num] = ''; # あとにつく名前 ..たとえば、'00本',"$HunitPop"
#$HcomplexTPkind[$num] = ''; # 加算種($island->{KIND}のKIND部分) ..たとえば、'','pop' 注！単位をそろえること！
#$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 

#  食料フラグ設定
#$HcomplexFPbase[$num]  = 10;     # 初期値 ($HunitPop x 10 規模)
#$HcomplexFPplus[$num]  = 2;      # 追加値 ($HunitPop x 10 規模)
#$HcomplexFPCmax[$num]  = 20;     # 追加可能回数 Max50(最終値は、初期値＋追加値ｘ追加可能回数になります)
#$HcomplexFPkind[$num]  = 'farm'; # 加算種($island->{KIND}のKIND部分) ..たとえば、'','pop' 注！単位をそろえること！

#  資金フラグ設定
#$HcomplexMPbase[$num]  = 0;  # 初期値 ($HunitPop x 10 規模)
#$HcomplexMPplus[$num]  = 0;  # 追加値 ($HunitPop x 10 規模)
#$HcomplexMPCmax[$num]  = 0;  # 追加可能回数 Max50(最終値は、初期値＋追加値ｘ追加可能回数になります)
#$HcomplexMPkind[$num]  = ''; # 加算種($island->{KIND}のKIND部分) ..たとえば、'','pop' 注！単位をそろえること！

#  ターン更新時属性
#$HcomplexAttr[$num] = 0x401;
# 0x1 周囲の平地に村が発生する(countGrow判定:農場(町)としてカウントされる)
# 0x2 火災の被害を防ぐ効果(森や記念碑と同等)
# 0x4 台風の被害を防ぐ効果(森や記念碑と同等)
# 0x10 力場発生:怪獣・巨大怪獣を押しつぶし瞬殺する
# 0x20 周囲2Hexのミサイル防衛（防衛基地と同等の機能）
# 0x40 周囲2Hexの艦隊攻撃防衛（防衛基地と同等の機能）
# 0x100 対潜攻撃の攻撃対象になる
# 0x200 対艦攻撃の攻撃対象になる
# 0x400 対地攻撃の攻撃対象になる
# 0x1000 ランダム収入
# 0x2000 ランダム収穫

### 以下3項目は個別設定不可
# 「ランダム収入」最小値と最大値
# 「ランダム収穫」最小値と最大値
# 「力場能力」周囲何Hexの怪獣・巨大怪獣を瞬殺するか？


#  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
#   prepare:整地・地ならし後, reclaim:埋め立て後, destroy:掘削後,
#   attack:海軍(怪獣)攻撃後,
#   stepdown:被弾した時に1撃で破壊されずにランクダウンする。(ダメージ)x(stepdown)を追加規模から減ずる処理。
#   move:怪獣移動後フラグ 注！[地形(0:陸,1:海), 地形の値(0:深海, 1:浅瀬)],
#   earthquake:地震後, typhoon:台風後, fire:火災後, tsunami:津波後, starve:暴動後
#   falldown:地盤沈下後, eruption:噴火後(中心は必ず山なので周辺部の設定), meteo:隕石後,
#   wide1:広域災害(防衛施設自爆・巨大ミサイル・巨大隕石)後1Hex周辺
#   wide2:広域災害(防衛施設自爆・巨大ミサイル・巨大隕石)後2Hex周辺
#  ！ここに記述がない場合は、破壊できない(されない)！
#$HcomplexAfter[$num]  = { # 農場
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

#  ポップアップナビ解説部分(''の間に記述。設定によって書き換える必要あり)
#$HnaviExp.= "COMPLEX$num = '';\n";

### 工場
#$num = 0; # 配列番号
#$HcomplexName[$num] = '工場'; # 名称
#$HcomplexImage[$num] = 'land8.gif';# 複合地形の画像ファイル
#$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
## 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # 名称
#$HcomplexPretendImage[$num] = ''; # 画像
#$HcomplexPretendNavi[$num]  = ''; # ナビ
## ランクアップ設定
#$HcomplexLevelKind[$num] = 'money'; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
#$HcomplexLevelValue[$num] = [0, 50, 80]; # ランクアップに必要なフラグ値の最小値
#$HcomplexSubName[$num] = ['工場(Lv1)', '工場(Lv2)', '工場(Lv3)'];# 名称
#$HcomplexSubImage[$num] = ['land8.gif', 'land8.gif', 'land8.gif'];# 画像
## 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 200]];# 複合地形($HlandComplex)以外
#$HcomplexBefore2[$num] = []; # 複合地形を別種のみ配列番号で指定(複数の場合は，[1, 3]のようにコンマで区切る)。同種の複合地形は記述不要
## ターンフラグ設定
#$HcomplexTPCmax[$num] = 0;  # 最大値
#$HcomplexTPname[$num] = ''; # 名称
#$HcomplexTPrate[$num] = 0;  # 表示倍率
#$HcomplexTPunit[$num] = ''; # あとにつく名前
#$HcomplexTPkind[$num] = ''; # 加算種
#$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
##  食料フラグ設定
#$HcomplexFPbase[$num]  = 0;  # 初期値
#$HcomplexFPplus[$num]  = 0;  # 追加値
#$HcomplexFPCmax[$num]  = 0;  # 追加可能回数 Max50
#$HcomplexFPkind[$num]  = ''; # 加算種
##  資金フラグ設定
#$HcomplexMPbase[$num]  = 30;  # 初期値
#$HcomplexMPplus[$num]  = 10;  # 追加値
#$HcomplexMPCmax[$num]  =  7;  # 追加可能回数 Max50
#$HcomplexMPkind[$num]  = 'factory'; # 加算種
##  ターン更新時属性
#$HcomplexAttr[$num] = 0x400;
##  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
#$HnaviExp.= "COMPLEX$num = '';\n"; # ポップアップナビ解説部分

### 採掘場
#$num = 2; # 配列番号
#$HcomplexName[$num] = '採掘場'; # 名称
#$HcomplexImage[$num] = 'land15.gif';# 複合地形の画像ファイル
#$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
## 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # 名称
#$HcomplexPretendImage[$num] = ''; # 画像
#$HcomplexPretendNavi[$num]  = ''; # ナビ
## ランクアップ設定
#$HcomplexLevelKind[$num] = ''; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
#$HcomplexLevelValue[$num] = ''; # ランクアップに必要なフラグ値の最小値
#$HcomplexSubName[$num] = '';# 名称
#$HcomplexSubImage[$num] = '';# 画像
## 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
#$HcomplexBefore[$num]  = [[$HlandMountain, 0, 200]];# 複合地形($HlandComplex)以外
#$HcomplexBefore2[$num] = [4]; # 複合地形を別種のみ配列番号で指定。同種の複合地形は記述不要
## ターンフラグ設定
#$HcomplexTPCmax[$num] = 0;  # 最大値
#$HcomplexTPname[$num] = ''; # 名称
#$HcomplexTPrate[$num] = 0;  # 表示倍率
#$HcomplexTPunit[$num] = ''; # あとにつく名前
#$HcomplexTPkind[$num] = ''; # 加算種
#$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
##  食料フラグ設定
#$HcomplexFPbase[$num]  = 0;  # 初期値
#$HcomplexFPplus[$num]  = 0;  # 追加値
#$HcomplexFPCmax[$num]  = 0;  # 追加可能回数 Max50
#$HcomplexFPkind[$num]  = ''; # 加算種
##  資金フラグ設定
#$HcomplexMPbase[$num]  =  5;  # 初期値
#$HcomplexMPplus[$num]  =  5;  # 追加値
#$HcomplexMPCmax[$num]  = 39;  # 追加可能回数 Max50
#$HcomplexMPkind[$num]  = 'mountain'; # 加算種
##  ターン更新時属性
#$HcomplexAttr[$num] = 0x0;
##  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
#$HnaviExp.= "COMPLEX$num = '';\n"; # ポップアップナビ解説部分

## 森
$num = 2; # 配列番号
$HcomplexName[$num] = '森'; # 名称
$HcomplexImage[$num] = 'land6.gif';# 複合地形の画像ファイル
$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
# 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # 名称
$HcomplexPretendImage[$num] = ''; # 画像
$HcomplexPretendNavi[$num]  = ''; # ナビ
# ランクアップ設定
$HcomplexLevelKind[$num] = ''; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
$HcomplexLevelValue[$num] = ''; # ランクアップに必要なフラグ値の最小値
$HcomplexSubName[$num] = '';# 名称
$HcomplexSubImage[$num] = '';# 画像
# 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
$HcomplexBefore[$num]  = [[$HlandPlains,0, 0], [$HlandTown, 0, 1000]];# 複合地形($HlandComplex)以外
$HcomplexBefore2[$num] = []; # 複合地形を別種のみ配列番号で指定。同種の複合地形は記述不要
# ターンフラグ設定
$HcomplexTPCmax[$num] = 500;  # 最大値
$HcomplexTPname[$num] = '木の数'; # 名称
$HcomplexTPrate[$num] = 1;  # 表示倍率
$HcomplexTPunit[$num] = '00本'; # あとにつく名前
$HcomplexTPkind[$num] = ''; # 加算種
$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
#  食料フラグ設定
$HcomplexFPbase[$num]  = 0;  # 初期値
$HcomplexFPplus[$num]  = 0;  # 追加値
$HcomplexFPCmax[$num]  = 0;  # 追加可能回数 Max50
$HcomplexFPkind[$num]  = ''; # 加算種
#  資金フラグ設定
$HcomplexMPbase[$num]  = 0;  # 初期値
$HcomplexMPplus[$num]  = 0;  # 追加値
$HcomplexMPCmax[$num]  = 0;  # 追加可能回数 Max50
$HcomplexMPkind[$num]  = ''; # 加算種
#  ターン更新時属性
$HcomplexAttr[$num] = 0x406;
#  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
$HnaviExp.= "COMPLEX$num = '1${HunitTree}あたり${HtreeValue}${HunitMoney}';\n"; # ポップアップナビ解説部分

### 造山
#$num = 0; # 配列番号
#$HcomplexName[$num] = '造山'; # 名称
#$HcomplexImage[$num] = 'land11.gif';# 複合地形の画像ファイル
#$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
## 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
#$HcomplexPretend[$num] = 0;
#$HcomplexPretendName[$num]  = ''; # 名称
#$HcomplexPretendImage[$num] = ''; # 画像
#$HcomplexPretendNavi[$num]  = ''; # ナビ
## ランクアップ設定
#$HcomplexLevelKind[$num] = ''; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
#$HcomplexLevelValue[$num] = ''; # ランクアップに必要なフラグ値の最小値
#$HcomplexSubName[$num] = '';# 名称
#$HcomplexSubImage[$num] = '';# 画像
## 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# 複合地形($HlandComplex)以外
#$HcomplexBefore2[$num] = [2]; # 複合地形を別種のみ配列番号で指定。同種の複合地形は記述不要
## ターンフラグ設定
#$HcomplexTPCmax[$num] = 0;  # 最大値
#$HcomplexTPname[$num] = ''; # 名称
#$HcomplexTPrate[$num] = 0;  # 表示倍率
#$HcomplexTPunit[$num] = ''; # あとにつく名前
#$HcomplexTPkind[$num] = ''; # 加算種
#$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
##  食料フラグ設定
#$HcomplexFPbase[$num]  = 0;  # 初期値
#$HcomplexFPplus[$num]  = 0;  # 追加値
#$HcomplexFPCmax[$num]  = 0;  # 追加可能回数 Max50
#$HcomplexFPkind[$num]  = ''; # 加算種
##  資金フラグ設定
#$HcomplexMPbase[$num]  = 0;  # 初期値
#$HcomplexMPplus[$num]  = 0;  # 追加値
#$HcomplexMPCmax[$num]  = 1;  # 追加可能回数 Max50
#$HcomplexMPkind[$num]  = ''; # 加算種
##  ターン更新時属性
#$HcomplexAttr[$num] = 0x6;
##  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
#$HnaviExp.= "COMPLEX$num = '';\n"; # ポップアップナビ解説部分

### 大農場
$num = 0; # 配列番号
$HcomplexName[$num] = '大農場'; # 名称
$HcomplexImage[$num] = 'land21.gif';# 複合地形の画像ファイル
$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
# 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # 名称
$HcomplexPretendImage[$num] = ''; # 画像
$HcomplexPretendNavi[$num]  = ''; # ナビ
# ランクアップ設定
$HcomplexLevelKind[$num] = 'food'; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
$HcomplexLevelValue[$num] = [0, 300, 600, 900, 1200]; # ランクアップに必要なフラグ値の最小値
$HcomplexSubName[$num] = ['大農場(Lv1)', '大農場(Lv2)', '大農場(Lv3)', '大農場(Lv4)', '大農場(Lv5)'];# 名称
$HcomplexSubImage[$num] = ['land21.gif', 'land21.gif', 'land21.gif', 'land21.gif', 'land21.gif'];# 画像
# 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 1000], [$HlandFarm, 0, 50]];# 複合地形($HlandComplex)以外
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# 複合地形($HlandComplex)以外
$HcomplexBefore2[$num] = [0, 1]; # 複合地形を別種のみ配列番号で指定。同種の複合地形は記述不要
# ターンフラグ設定
$HcomplexTPCmax[$num] = 0;  # 最大値
$HcomplexTPname[$num] = ''; # 名称
$HcomplexTPrate[$num] = 0;  # 表示倍率
$HcomplexTPunit[$num] = ''; # あとにつく名前
$HcomplexTPkind[$num] = ''; # 加算種
$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
#  食料フラグ設定
$HcomplexFPbase[$num]  = 100;  # 初期値
$HcomplexFPplus[$num]  = 50;  # 追加値
$HcomplexFPCmax[$num]  = 28;  # 追加可能回数 Max50
$HcomplexFPkind[$num]  = 'farm'; # 加算種
#  資金フラグ設定
$HcomplexMPbase[$num]  = 0;  # 初期値
$HcomplexMPplus[$num]  = 0;  # 追加値
$HcomplexMPCmax[$num]  = 0;  # 追加可能回数 Max50
$HcomplexMPkind[$num]  = ''; # 加算種
#  ターン更新時属性
$HcomplexAttr[$num] = 0x2405;
#  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
$HnaviExp.= "COMPLEX$num = '';\n"; # ポップアップナビ解説部分

### 大工場
$num = 1; # 配列番号
$HcomplexName[$num] = '大工場'; # 名称
$HcomplexImage[$num] = 'land22.gif';# 複合地形の画像ファイル
$HcomplexMax[$num] = 0; # 保有(建設)可能最大数(0:無制限)
# 偽装設定(0:偽装なし，1:森のふり，2:海のふり，3:なにか別のもの)
$HcomplexPretend[$num] = 0;
$HcomplexPretendName[$num]  = ''; # 名称
$HcomplexPretendImage[$num] = ''; # 画像
$HcomplexPretendNavi[$num]  = ''; # ナビ
# ランクアップ設定
$HcomplexLevelKind[$num] = 'money'; # ランクアップのもとになるフラグの種類('turn'か'food'か'money')
$HcomplexLevelValue[$num] = [0, 500, 1000, 1500, 20000]; # ランクアップに必要なフラグ値の最小値
$HcomplexSubName[$num] = ['大工場(Lv1)', '大工場(Lv2)', '大工場(Lv3)', '大工場(Lv4)', '大工場(Lv5)'];# 名称
$HcomplexSubImage[$num] = ['land22.gif', 'land22.gif', 'land22.gif', 'land22.gif', 'land22.gif'];# 画像
# 複合地形を建設可能な地形を変数で記述([地形,地形値min,地形値max], [地形,地形値min,地形値max],・・・) ※$HlandComplexは記述不要)
$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 1000], [$HlandFactory, 0, 100]];# 複合地形($HlandComplex)以外
#$HcomplexBefore[$num]  = [[$HlandPlains, 0, 0], [$HlandTown, 0, 199]];# 複合地形($HlandComplex)以外
$HcomplexBefore2[$num] = [0, 1]; # 複合地形を別種のみ配列番号で指定。同種の複合地形は記述不要
# ターンフラグ設定
$HcomplexTPCmax[$num] = 0;  # 最大値
$HcomplexTPname[$num] = ''; # 名称
$HcomplexTPrate[$num] = 0;  # 表示倍率
$HcomplexTPunit[$num] = ''; # あとにつく名前
$HcomplexTPkind[$num] = ''; # 加算種
$HcomplexTPhide[$num] = 0;  # 観光者からみえなくするか(0:しない、1:する) 
#  食料フラグ設定
$HcomplexFPbase[$num]  = 0;  # 初期値
$HcomplexFPplus[$num]  = 0;  # 追加値
$HcomplexFPCmax[$num]  = 0;  # 追加可能回数 Max50
$HcomplexFPkind[$num]  = ''; # 加算種
#  資金フラグ設定
$HcomplexMPbase[$num]  = 300;  # 初期値
$HcomplexMPplus[$num]  = 100;  # 追加値
$HcomplexMPCmax[$num]  = 17;  # 追加可能回数 Max50
$HcomplexMPkind[$num]  = 'factory'; # 加算種
#  ターン更新時属性
$HcomplexAttr[$num] = 0x1400;
#  破壊された時の地形を変数で記述('破壊の種類' => [地形, 地形の値])
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
$HnaviExp.= "COMPLEX$num = '';\n"; # ポップアップナビ解説部分


# 複合地形コマンド設定(最大50種類)
#---------------------------------
#  0x0:建設(設置)のみ
#  0x1:ターンリセット
#  0x2:食料追加
#  0x4:資金追加

#  ターンリセット時(フラグが0になった場合)の処理
#   地形変化
#    変化後の地形と地形の値
#    また、ターンフラグ最大値が0の場合は無効なので''でよい
#$HcomplexComTFRL[$cno] = ["", ""]; # 変化がない場合は''でよい(0はダメ。)
#   収入・収穫処理(フラグ数値に対する倍率)
#    type:食料food,資金moneyのいずれか
#    ratio:倍率設定(foodの場合は$HunitFoodに対する倍率、moneyの場合は$HunitMoneyに対する倍率)
#    log:ログ出力設定 通常出力normal,まとめ出力matome,
#    logstr:ログ出力補助設定 '収穫','収益'など
#$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' };

### 大農場整備
$cno = 0; # 配列番号
$HcomplexComName[$cno] = '大農場整備'; # 名称
$HcomplexComMsgs[$cno] = '食糧源となる施設。最大50万。(複数可)'; # 説明
$HcomplexComKind[$cno] = 0;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 200;  # コマンド費用
$HcomplexComTurn[$cno] = 1;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x2; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # 変化がない場合は''でよい(0はダメ。)
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' };

### 高速大農場整備
$cno = 1; # 配列番号
$HcomplexComName[$cno] = '高速大農場整備'; # 名称
$HcomplexComMsgs[$cno] = 'ターン消費なしの大農場整備。(複数可)'; # 説明
$HcomplexComKind[$cno] = 0;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 3000; # コマンド費用
$HcomplexComTurn[$cno] = 0;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x2; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # 収入・収穫処理

### 大工場建設
$cno = 2; # 配列番号
$HcomplexComName[$cno] = '大工場建設'; # 名称
$HcomplexComMsgs[$cno] = '資金源となる施設。最大100万(複数可)'; # 説明
$HcomplexComKind[$cno] = 1;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 1000; # コマンド費用
$HcomplexComTurn[$cno] = 1;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x4; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # 収入・収穫処理

### 高速大工場建設
$cno = 3; # 配列番号
$HcomplexComName[$cno] = '高速大工場建設'; # 名称
$HcomplexComMsgs[$cno] = 'ターン消費なしの大工場建設。(複数可)'; # 説明
$HcomplexComKind[$cno] = 1;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 3000; # コマンド費用
$HcomplexComTurn[$cno] = 0;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x4; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # 収入・収穫処理

### 植林
$cno = 5; # 配列番号
$HcomplexComName[$cno] = '植林'; # 名称
$HcomplexComMsgs[$cno] = '平地、町系で実行可能。'; # 説明
$HcomplexComKind[$cno] = 2;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 50; # コマンド費用
$HcomplexComTurn[$cno] = 1;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x0; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # 収入・収穫処理

### 高速植林
$cno = 6; # 配列番号
$HcomplexComName[$cno] = '高速植林'; # 名称
$HcomplexComMsgs[$cno] = '平地、町系で実行可能。'; # 説明
$HcomplexComKind[$cno] = 2;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 3000; # コマンド費用
$HcomplexComTurn[$cno] = 0;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x0; # 対象となるフラグ
$HcomplexComTFRL[$cno] = ["", ""]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => '', 'ratio' => 0, 'log' => '', 'logstr' => '' }; # 収入・収穫処理

### 伐採
$cno = 4; # 配列番号
$HcomplexComName[$cno] = '伐採'; # 名称
$HcomplexComMsgs[$cno] = '森で実行すると平地に変化し資金化。'; # 説明
$HcomplexComKind[$cno] = 2;   # 対象となる複合地形の種類
$HcomplexComCost[$cno] = 0; # コマンド費用
$HcomplexComTurn[$cno] = 0;   # ターン消費(0:なし、1:あり)
$HcomplexComFlag[$cno] = 0x1; # 対象となるフラグ
$HcomplexComTFRL[$cno] = [$HlandPlains, 0]; # ターンリセット時の処理
$HcomplexComTFInCome[$cno] = { 'type' => 'money', 'ratio' => 5, 'log' => 'normal', 'logstr' => '収益' }; # 収入・収穫処理


#----------------------------------------
# 海軍
#----------------------------------------
# 経験値の最大値
$HmaxExpNavy = 120; # ただし、最大でも255まで

# レベルの最大値
$maxNavyLevel = 0;  # 海軍
# 経験値がいくつでレベルアップか
#              Lv2   3   4   5   6    7    8    9   10
@navyLevelUp = (0);
#                    Lv2  4  6  8  10
@HnavyFirePlus  = (0); # 増加攻撃回数(偶数レベルでアップ)
#                 Lv1  3  5  7   9
@HnavyMaxHpPlus = (0); # 増加耐久力(奇数レベルでアップ)

# 残骸売却時に金塊が発見される確率
$HnavyProbWreckGold = 20; # 20%

# 艦隊を保有しない島へは艦隊を派遣できなくする？（0:しない、1:する）
# ！宣戦布告を使う設定の場合、宣戦布告もできなくなります
$HnofleetNotAvail = 0;

# 他島に派遣中の艦隊も補給するか？（0:しない、1:する）
# （0なら自分の島にいる艦隊のみ補給するor派遣先の島が自島を友好国に設定している場合補給する）
$HnavySupplyFlag = 0;

# 攻撃した艦艇自身が射程範囲にある場合、自爆(被弾)もあり？（0:なし、1:あり）
$HnavySelfAttack = 0;

# 艦艇攻撃で被弾した艦艇や地形が自島の場合、無害にするか？（0:しない、1:する、2:友好国も無害にする）
$HnavySafetyZone = 2;
# 無害化が無効になる確率(%) ※無害化機能が発動する場面で判定
$HnavySafetyInvalidp = 0;

# 射程内の地形による攻撃の優先順位(デフォルト)
@Hpriority = ('Navy', 'Monster', 'HugeMonster', 'Arm',    'Pop',  'Food',   'Money',  'Other');
@HpriStr   = ('海軍', '怪獣',    '巨大怪獣',    '軍施設', '都市', '食料源', '資金源', 'その他');
# Navy:海軍 Monster:怪獣 HugeMonster:巨大怪獣
# Arm:海底基地,ミサイル基地,ハリボテ,防衛施設(擬装しない場合)
# Pop:町系 Food:農場 Money:海底油田,工場 Other:森,記念碑
# 注！この設定をカラッポにすると攻撃できなくなってしまいます。
$Hnearfar = 2; # 0:最も近い地形から目標を探す 1:最も遠い地形から目標を探す 2:射程内をランダムに目標を探す

# 索敵順(攻撃の優先順位)の変更を許可するか？（0:しない、1:する）
$HusePriority = 1;

# 「一斉攻撃」コマンドを使うか？(0:禁止)
# ※指定地点を射程内にもつ艦艇の攻撃対象に設定するコマンドです。
$HuseTarget = 0;

# 自島以外にいる艦隊の耐久力が表示されるか？（0:なし、1:あり）
$HnavyShowInfo = 1;

# 保有可能艦艇数(設定しない場合は0)
$HnavyMaximum = 0;
# １艦隊あたりの保有可能艦艇数(設定しない場合は0)
$HfleetMaximum = 0; # 設定する場合、編成の都合上、4倍した数値が$HnavyMaximumを超える方がよいと思う
# 軍港１港あたりの保有可能艦艇数(設定しない場合は0)
$HportRetention = 4; # いくら軍港を増やしても保有可能艦艇数を超えることはない
#----------------------------------------
# 艦艇
#----------------------------------------
# 建造(経験値)レベル設定
$HmaxComNavyLevel = 7;  # レベルの最大値(使用しない場合は0にする)
# 下の設定をそのまま使う場合は、上の「レベルの最大値」は10にします。
#                   2   3   4   5    6    7    8     9    10
@HcomNavyBorder = (5, 10, 20, 40, 80, 150); # 必要な総獲得経験値(各レベルの最小値。レベル１は「0」)
#           レベル 1   2   3   4   5   6   7   8   9  10
@HcomNavyNumber = (4, 6, 11, 13, 15, 16, 17); # 建造可能な艦艇番号の最大値
# 建造するには軍港の経験値レベルも必要にする？(0:しない、1:する)
# 「軍港に隣接した深い海で建造可能」の設定をしない場合は、もっとも近い軍港のレベルを確認します。
$HmaxComPortLevel = 0;

# 港に隣接した深い海でしか艦艇を建造できない(0:しない、1:する)
$HnavyBuildFlag = 1;

# 浅瀬にも移動可＆派遣可。(0:しない、1:する)
$HnavyMoveAsase = 1;

# 残骸画像ファイル
$HnavyImageZ = 'land18.gif';

# 特殊能力関連設定
#「貿易能力」貿易能力のある艦艇が派遣されていない島へは援助コマンドがつかえなくする？(0:しない、1:する)
$HtradeAbility = 0;
#「体当たり」旗艦・移動操縦でなくても体当たりする？(0:しない、1:する)
$HsuicideAbility = 1;

# 艦艇設定(最大32種類)
#---------------------------------
$HnavyImage3 = 'navy99_0.gif'; #建造中の画像は共通 

### 軍港
$num = 0; # 配列番号
# 名前
$HnavyName[$num] = '軍港';
# 能力
$HnavyKindMax[$num]   = 0;      # 保有可能数(設定しない場合は0)
$HnavyHP[$num]        = 10;     # 初期耐久力
$HnavyMaxHP[$num]     = 20;     # 最終耐久力(Max15) レベルアップによる増加耐久力の最大値を考慮に入れて設定してください。
$HnavyDamage[$num]    = 0;      # 破壊力(命中時のダメージ) ※耐久力のある地形が対象。設定なしで1なので、2以上の整数を設定する場合に使用。
$HnavyFire[$num]      = 0;      # 攻撃数 レベルアップによる増加攻撃回数の最大値を考慮に入れて設定してください。
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 0;     # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 6000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 0;      # 撃沈時に残骸が残る確率(%) 軍港の設定は無効になります
$HnavySpecial[$num]   = 0x10008;    # 特殊能力
$HnavyBuildTurn[$num] = 12;     # 工期設定 工期必要ない場合は1でなく0、浅瀬移動フラグ等、軍艦と舟艇の区別にも使う
$HnavyCruiseTurn[$num] = 0;     # 航続ターン 設定しないなら0 設定した場合はそのターン経つと帰還 航空機フラグにも使う
$HnavyNoMove[$num]    =  1;     # 動かない艦隊フラグ 軍港、海上防衛、採掘基地、定置網

# 特殊能力の内容は、
# 0x0 特になし
# 0x1 移動が速い(最大2マス移動)
# 0x2 移動がとても速い(最大何マス移動するか不明)
# 0x4 潜水する
# 0x8 港
# 0x10 先行移動（島コマンド実行前に移動）
# 0x20 周囲2Hexのミサイル防衛（防衛基地と同等の機能）
# 0x40 周囲2Hexの艦隊攻撃防衛（防衛基地と同等の機能）
# 0x80 旗艦・移動操縦(島主が移動を指示)
# 0x100 対潜攻撃
# 0x200 対艦攻撃
# 0x400 対地攻撃
# 0x800 蹂躙移動（自分の属する艦隊の旗艦を目指して移動）
# 0x800 対空攻撃に変更
# 0x1000 魚雷系　（対潜、対艦）防御不能の単ヘックス
# 0x2000 艦砲系　（対艦、対地）防御可能なメガヘックス
# 0x4000 対艦攻撃（対艦、対地）防御可能な単ヘックス
# 0x8000 海底探査(財宝、油田発見、維持費とは別に調査費高額、沈没あり、海底火山噴火あり)
#        油田が見つからない場合その半分の確率で財宝発見、さらにその半分の確率で海底火山噴火。
#        調査費は毎ターン「掘削費用×発見確率」。沈没確率は発見確率の10分の1。
# 0x8000 対空攻撃に変更
# 0x10000 補給能力（他島へ派遣中、周囲１ヘックスの自島(or友好国)艦艇と自分に補給を行う）※自島(or友好国)艦艇以外補給できない設定で使う
# 0x20000 貿易能力（援助コマンドを使う島へ派遣）※下の設定を「1:する」設定の場合に使う。仕様変更。強制貿易を行う。
# 0x40000 海賊能力 ※派遣した島の、農場から食料、工場から資金を奪う。1Hex内50%,2Hex30%,3Hex10%
# 0x80000 陸地掘削能力（荒地(着弾点)へ移動可能。移動後は浅瀬に。普通の荒地へ移動しようとした場合は着弾点にする）
# 0x100000 海底探査能力 0x8000からこちらに変更
# 0x200000 鉱床からの収穫
# 0x400000 漁礁からの収穫
# 0x800000
# 0x1000000 目標補正能力（攻撃前に策敵をやり直す）
# 0x2000000 艦艇に体当たりする能力($HsafetyZoneの設定で自艦、友好国艦にも体当たりしてしまいます)
# 0x4000000 命中率UP:攻撃誤差を一定確率で1Hex縮める
# 0x8000000 防波能力:周囲を津波の被害から守る
# 0x10000000 破壊力:ランダム(命中時のダメージ) ※乱数発生確率と最大破壊力を別途設定。乱数が発生しない時は，破壊力の能力設定もしくは1。
# 0x20000000 絨毯爆撃 (初弾の着弾点の周囲数ヘックスを攻撃)
# 0x40000000
# 0x80000000

# 特殊能力関連設定
# 「魚雷系」「艦砲系」「艦載機系」海軍の攻撃名
#    ['0x1000の名称', '0x2000の名称', '0x4000の名称'] (能力のない場合は空欄でよい)
#   「〜を行いました」というログになります。
$HnavyFireName[$num] = ['', '', '',''];
#「潜水する」移動時に浮上する確率(1%単位)
$HsubmarineSurface[$num] = 0;
#「蹂躙移動」旗艦を探す範囲 半径３マス（あまり広い範囲を探さないようにしてください。余計なサーバ負荷になります）
$HnavyTowardRange[$num] = 3;
#「海底探査」油田発見確率(0.1%単位)
$Hoilp[$num] = 2;
#「補給能力」補給艦の有効範囲 半径３マス（あまり広い範囲を探さないようにしてください。余計なサーバ負荷になります）
$HnavySupplyRange[$num] = 0;
#「海賊能力」周囲何Hex内の農場、工場に対して海賊行為を行うか。※1〜3を設定。4以上にはできません。
$HpiratesHex[$num] = 2;
#「命中率UP」1Hex縮める確率(%単位)
$Hfirehexp[$num] = 50;
#「防波能力」周囲何Hexを津波から守るか。※1〜3を設定。4以上にはできません。
$HbouhaHex[$num] = 2;
#「破壊力:ランダム」乱数発生確率と最大破壊力
$HdamageMax[$num] = 1; # 最大破壊力
$Hdamagep[$num]   = 0; # 乱数発生確率(1%単位)
#「絨毯爆撃」周囲何Hex対象か？※1〜2を設定。
$HnavyTerrorHex[$num] = 0; # 完全に絨毯爆撃するには1Hex:7発，2Hex:19発が必要です。結果的に攻撃誤差が広がることになります。

# ポップアップナビ解説部分(''の間に記述。設定によって書き換える必要あり)
$HnaviExp.= "NAVY$num = '　隣接する深い海で<BR>　艦艇建造可能'\n";

# 海軍の画像ファイル
$HnavyImage[$num]  = 'navy0.gif';
$HnavyImage2[$num] = ''; # 潜水中

### カメレオン
$num = 1; # 配列番号
$HnavyName[$num] = 'カメレオン対獣艇';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 5;      # 初期耐久力
$HnavyMaxHP[$num]     = 10;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 4;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 4;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 1;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 400;    # 建造費用
$HnavyShellCost[$num] = 100;      # 弾薬１発の費用
$HnavyMoney[$num]     = 15;      # 維持費用
$HnavyFood[$num]      = 150;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x20003581; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['対獣爆雷投下','多弾頭地雷散布','',''];
$HsubmarineSurface[$num] = 0;   #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行う範囲(Hex)
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対地・対潜攻撃<BR>'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy1_0.gif';# 海軍の画像ファイル
$HnavyImage2[$num] = '';         # 潜水中
$HvsMonster[$num] = 1; # 怪獣しか攻撃できないフラグ

### スパイダー
$num = 2; # 配列番号
$HnavyName[$num] = 'スパイダー工作艇';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 5;      # 初期耐久力
$HnavyMaxHP[$num]     = 10;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 1;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 1;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;     # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 2000;    # 建造費用
$HnavyShellCost[$num] = 200;      # 弾薬１発の費用
$HnavyMoney[$num]     = 15;      # 維持費用
$HnavyFood[$num]      = 150;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x20002481; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '多弾頭地雷散布', '多弾頭地雷散布',''];
$HsubmarineSurface[$num] = 0;   #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対地攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy6_0.gif';# 海軍の画像ファイル
$HnavyImage2[$num] = '';         # 潜水中

### シュミット
$num = 3; # 配列番号
$HnavyName[$num] = 'シュミット戦闘機';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 1;      # 初期耐久力
$HnavyMaxHP[$num]     = 2;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 1;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 5;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;     # 経験値
$HnavyBuildExp[$num]  = 3;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 800;    # 建造費用
$HnavyShellCost[$num] = 10;      # 弾薬１発の費用
$HnavyMoney[$num]     = 40;      # 維持費用
$HnavyFood[$num]      = 50;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1008812; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 6;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '','制空ミサイル発射'];
$HsubmarineSurface[$num] = 0;   #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動がとても速い<BR>   対空攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy3_0.gif';# 海軍の画像ファイル
$HnavyImage2[$num] = '';         # 潜水中

### ホーク
$num = 4; # 配列番号
$HnavyName[$num] = 'ホーク攻撃機';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 2;      # 初期耐久力
$HnavyMaxHP[$num]     = 4;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 4;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 5;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;     # 経験値
$HnavyBuildExp[$num]  = 3;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 1200;    # 建造費用
$HnavyShellCost[$num] = 20;      # 弾薬１発の費用
$HnavyMoney[$num]     = 60;      # 維持費用
$HnavyFood[$num]      = 100;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1004202; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 6;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '対艦ミサイル発射',''];
$HsubmarineSurface[$num] = 0;   #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動がとても速い<BR>   対艦攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy11_0.gif';# 海軍の画像ファイル
$HnavyImage2[$num] = '';         # 潜水中

### 投網漁船
$num = 5; # 配列番号
$HnavyName[$num] = '投網漁船';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 5;      # 初期耐久力
$HnavyMaxHP[$num]     = 10;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 4;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 3;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 1000;    # 建造費用
$HnavyShellCost[$num] = 100;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1181; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['捕獲網投下', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対潜攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy5_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中
$Hprivate[$num] = 1;#民間船フラグ
$HvsMonster[$num] = 1; # 怪獣しか攻撃できないフラグ

### 護国攻撃機
$num = 6; # 配列番号
$HnavyName[$num] = '護国攻撃機';# 名前
$HnavyKindMax[$num]   = 3;      # 保有可能数
$HnavyHP[$num]        = 1;      # 初期耐久力
$HnavyMaxHP[$num]     = 2;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 1;      # 経験値
$HnavyBuildExp[$num]  = 1;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 1500;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 120;      # 維持費用
$HnavyFood[$num]      = 50;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x2000002; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 3;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動がとても速い<BR>   体当たり攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy2_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### メテオ潜航艇
$num = 7; # 配列番号
$HnavyName[$num] = 'メテオ潜航艇';# 名前
$HnavyKindMax[$num]   = 3;      # 保有可能数
$HnavyHP[$num]        = 5;      # 初期耐久力
$HnavyMaxHP[$num]     = 10;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 0;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 1000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 10;      # 維持費用
$HnavyFood[$num]      = 50;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x2000084; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 10;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   潜水する<BR>   体当たり攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy4_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = 'land19.gif';# 潜水中

### 霞級駆逐艦(対潜型)
$num = 8; # 配列番号
$HnavyName[$num] = '霞級駆逐艦(対潜型)';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 15;      # 初期耐久力
$HnavyMaxHP[$num]     = 30;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 3;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 4;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 6;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 8000;    # 建造費用
$HnavyShellCost[$num] = 5;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 600;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1001181; # 特殊能力
$HnavyBuildTurn[$num] = 16;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['爆雷投下', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対潜攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy36_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 霞級駆逐艦(水雷型)
$num = 9; # 配列番号
$HnavyName[$num] = '霞級駆逐艦(水雷型)';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 15;      # 初期耐久力
$HnavyMaxHP[$num]     = 30;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 3;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 3;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 6;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 8000;    # 建造費用
$HnavyShellCost[$num] = 5;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 600;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1001281; # 特殊能力
$HnavyBuildTurn[$num] = 16;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['魚雷発射', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対艦攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy35_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 霞級駆逐艦(防空型)
$num = 10; # 配列番号
$HnavyName[$num] = '霞級駆逐艦(防空型)';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 15;      # 初期耐久力
$HnavyMaxHP[$num]     = 30;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 1;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 3;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 6;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 8800;    # 建造費用
$HnavyShellCost[$num] = 5;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 600;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1008881; # 特殊能力
$HnavyBuildTurn[$num] = 16;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '','対空射撃'];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対空攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy7_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 霞級駆逐艦(対地型)
$num = 11; # 配列番号
$HnavyName[$num] = '霞級駆逐艦(対地型)';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 15;      # 初期耐久力
$HnavyMaxHP[$num]     = 30;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 1;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 3;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 8000;    # 建造費用
$HnavyShellCost[$num] = 5;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 600;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x21002481; # 特殊能力
$HnavyBuildTurn[$num] = 16;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '艦砲射撃', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動が速い<BR>   対地攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy37_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### ひゅうが
$num = 12; # 配列番号
$HnavyName[$num] = 'ひゅうが級護衛空母';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 15;      # 初期耐久力
$HnavyMaxHP[$num]     = 30;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 9;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 24000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 60;      # 維持費用
$HnavyFood[$num]      = 1200;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x80; # 特殊能力
$HnavyBuildTurn[$num] = 48;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   隣接する海から航空機発進可能'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy39_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 零式潜水艦
$num = 13; # 配列番号
$HnavyName[$num] = '零式潜水艦';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 8;      # 初期耐久力
$HnavyMaxHP[$num]     = 16;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 5;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 1;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 2;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 8;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 12000;    # 建造費用
$HnavyShellCost[$num] = 5;      # 弾薬１発の費用
$HnavyMoney[$num]     = 45;      # 維持費用
$HnavyFood[$num]      = 900;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x1001284; # 特殊能力
$HnavyBuildTurn[$num] = 24;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['魚雷発射', '', '',''];
$HsubmarineSurface[$num] = 5;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   潜水する<BR>   対艦攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy10_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = 'land19.gif';# 潜水中

### 金剛型戦艦
$num = 14; # 配列番号
$HnavyName[$num] = '金剛型戦艦';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 30;      # 初期耐久力
$HnavyMaxHP[$num]     = 60;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 4;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 4;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 15;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 24000;    # 建造費用
$HnavyShellCost[$num] = 10;      # 弾薬１発の費用
$HnavyMoney[$num]     = 120;      # 維持費用
$HnavyFood[$num]      = 2400;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x21002280; # 特殊能力
$HnavyBuildTurn[$num] = 48;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '艦砲射撃', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   対艦・対地攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy9_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### フォートレス爆撃機
$num = 15; # 配列番号
$HnavyName[$num] = 'フォートレス爆撃機';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 2;      # 初期耐久力
$HnavyMaxHP[$num]     = 4;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 1;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 4;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 4;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 2000;    # 建造費用
$HnavyShellCost[$num] = 40;      # 弾薬１発の費用
$HnavyMoney[$num]     = 80;      # 維持費用
$HnavyFood[$num]      = 100;      # 維持食料
$HnavyProbWreck[$num] = 80;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x20002402; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 12;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', 'クラスタ爆弾投下', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   移動がとても速い<BR>対地攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy12_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 豪華客船タイタニック
$num = 16; # 配列番号
$HnavyName[$num] = '豪華客船タイタニック';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 5;      # 初期耐久力
$HnavyMaxHP[$num]     = 10;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 0;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 2000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x20080; # 特殊能力
$HnavyBuildTurn[$num] = 0;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;  #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   貿易能力'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy13_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中
$Hprivate[$num] = 1;#民間船フラグ

### 大和級巨大戦艦
$num = 17; # 配列番号
$HnavyName[$num] = '大和級巨大戦艦';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 50;      # 初期耐久力
$HnavyMaxHP[$num]     = 100;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 6;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 7;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 5;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 25;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 60000;    # 建造費用
$HnavyShellCost[$num] = 20;      # 弾薬１発の費用
$HnavyMoney[$num]     = 240;      # 維持費用
$HnavyFood[$num]      = 4800;      # 維持食料
$HnavyProbWreck[$num] = 20;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x21002680; # 特殊能力
$HnavyBuildTurn[$num] = 120;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  0;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '艦砲射撃', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 1;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   対艦・対地攻撃'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy16_0.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 海上防衛施設
$num = 18; # 配列番号
$HnavyName[$num] = '海上防衛施設';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 10;      # 初期耐久力
$HnavyMaxHP[$num]     = 20;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 6000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 0;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x40; # 特殊能力
$HnavyBuildTurn[$num] = 12;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  1;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   艦隊攻撃防衛'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy33.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 海上採掘基地
$num = 19; # 配列番号
$HnavyName[$num] = '海上採掘基地';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 10;      # 初期耐久力
$HnavyMaxHP[$num]     = 20;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 6000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 0;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x200000; # 特殊能力
$HnavyBuildTurn[$num] = 12;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  1;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '艦砲射撃', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   採取能力'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy32.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

### 定置網
$num = 20; # 配列番号
$HnavyName[$num] = '定置網';# 名前
$HnavyKindMax[$num]   = 0;      # 保有可能数
$HnavyHP[$num]        = 10;      # 初期耐久力
$HnavyMaxHP[$num]     = 20;      # 最終耐久力(Max15)
$HnavyDamage[$num]    = 0;      # 破壊力 ※設定なしで1
$HnavyFire[$num]      = 0;      # 攻撃数
$HnavyFireHex[$num]   = 0;      # 攻撃範囲(誤差)
$HnavyFireRange[$num] = 0;      # 射程距離(ジャミング消去範囲)
$HnavyExp[$num]       = 3;      # 経験値
$HnavyBuildExp[$num]  = 0;      # 艦艇建造で軍港が獲得する経験値
$HnavyCost[$num]      = 6000;    # 建造費用
$HnavyShellCost[$num] = 0;      # 弾薬１発の費用
$HnavyMoney[$num]     = 30;      # 維持費用
$HnavyFood[$num]      = 300;      # 維持食料
$HnavyProbWreck[$num] = 0;     # 撃沈時に残骸が残る確率(%)
$HnavySpecial[$num]   = 0x400000; # 特殊能力
$HnavyBuildTurn[$num] = 12;     # 工期設定
$HnavyCruiseTurn[$num] = 0;     # 航続ターン
$HnavyNoMove[$num]    =  1;     # 動かない艦隊フラグ
$HnavyFireName[$num] = ['', '艦砲射撃', '',''];
$HsubmarineSurface[$num] = 0;  #「潜水する」移動時に浮上する確率(1%単位)
$HnavyTowardRange[$num]  = 0;   #「蹂躙移動」旗艦を探す範囲(Hex)
$Hoilp[$num]             = 0;   #「海底探査」油田発見確率(0.1%単位)
$HnavySupplyRange[$num]  = 0;   #「補給能力」補給艦の有効範囲(Hex)
$HpiratesHex[$num]       = 0;   #「海賊能力」海賊行為を行うHex
$Hfirehexp[$num]         = 0;   #「命中率UP」1Hex縮める確率(%単位)
$HbouhaHex[$num]         = 0;   #「防波能力」津波から守る範囲(Hex)
$HdamageMax[$num]        = 0;   #「破壊力:ランダム」最大破壊力
$Hdamagep[$num]          = 0;   #「破壊力:ランダム」乱数発生確率(1%単位)
$HnavyTerrorHex[$num]    = 0;   #「絨毯爆撃」Hex
$HnaviExp.= "NAVY$num = '   採取能力'\n";# ポップアップナビ解説部分
$HnavyImage[$num]  = 'navy24.gif'; # 海軍の画像ファイル
$HnavyImage2[$num] = '';# 潜水中

# 所属不明艦
#------------
# 艦艇(所属不明)が出現する？（0:しない、1:する）
$HnavyUnknown   = 1;

# 単位面積あたりの出現率(0.01%単位)
$HdisNavy = 3;

# 所属不明艦出現の基準
@HdisNavyBorder = ( 0, 5000, 5000, 5000, 5000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 20000, 20000, 25000, 24000, 30000, 35000);

# 所属不明艦出現比率
@HdisNavyRatio = ( 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1); # 非負整数(0にすると出現しなくなる。軍港系は0にしましょうd(*⌒▽⌒*)b)
# 出現率判定($HdisNavy)で出現することが決定したのち、人口基準($HdisNavyBorder)をクリアしている
# 艦艇の中から上の比率($HdisNavyRatio)で艦艇を選ぶ

#----------------------------------------
# 怪獣
#----------------------------------------
# 種類(最大32種類)
$HmonsterNumber  = 8; 

# 単位面積あたりの出現率(0.01%単位)
$HdisMonster   = 3;

# 怪獣派遣を使うか？(0:禁止)
$HuseSendMonster = 0;

# ST怪獣派遣を使うか？(0:禁止)
$HuseSendMonsterST = 0;

# 派遣可能な怪獣の番号の最大値
$HsendMonsterNumber = 7;

# 攻撃した怪獣自身が射程範囲にある場合、自爆(被弾)もあり？（0:なし、1:あり）
$HmonsterSelfAttack = 0;

# 「攻撃能力」で被弾した艦艇や地形が自島の場合、無害にするか？（0:しない、1:する、2:友好国も無害にする）
$HmonsterSafetyZone = 2;
# 無害化が無効になる確率(%) ※無害化機能が発動する場面で判定
$HmonsterSafetyInvalidp = 0;

# 「攻撃能力」の攻撃回数上限(瀕死になると爆発的に攻撃回数が増加するので)(0:設定なし)
$HmonsterFireMax = 0;

# 怪獣出現の基準
@HdisMonsBorder = ( 0, 1000, 1000, 2500, 2500, 2500, 4000, 4000);

# 怪獣出現比率
@HdisMonsRatio = ( 0, 1, 1, 1, 1, 1, 1, 1); # 非負整数(0にすると出現しなくなる)
# 出現率判定($HdisMonster)で出現することが決定したのち、人口基準($HdisMonsBorder)をクリアしている
# 怪獣の中から上の比率($HdisMonsRatio)で怪獣を選ぶ

# 潜水中画像ファイル(共通設定)
$HmonsterImageUnderSea = 'land17.gif';

# 怪獣設定(最大32種類)
#----------------------
### メカいのら
$num = 0; # 配列番号
# 名前
$HmonsterName[$num] = 'メカいのら';
# 能力
$HmonsterBHP[$num]       = 2;    # 最低体力
$HmonsterDHP[$num]       = 0;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 5;    # 経験値
$HmonsterValue[$num]     = 0;    # 死体の値段
$HmonsterCost[$num]      = 3000; # 派遣コマンド費用
$HmonsterCostST[$num]    = 6000; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x20; # 特殊能力
# 特殊能力の内容は、
# 0x0 特になし
# 0x1 足が速い(最大2歩あるく)
# 0x2 足がとても速い(最大何歩あるくか不明)
# 0x4 ランダム硬化
# 0x10 先行移動（島コマンド実行前に移動）
# 0x20 蹂躙移動（町などを目指して移動）
# 0x80 移動操縦（島主が移動をコントロール）
# 0x100 攻撃能力（攻撃目標を捕捉し攻撃する）
# 0x200 絨毯爆撃 (初弾の着弾点の周囲数ヘックスを攻撃) ※ミサイル攻撃能力が必要

#「絨毯爆撃」周囲何Hex対象か？※1〜2を設定。
$HmonsterTerrorHex[$num] = 0; # 完全に絨毯爆撃するには1Hex:7発，2Hex:19発が必要です。結果的に攻撃誤差が広がることになります。

# ポップアップナビ解説部分(''の間に記述。設定によって書き換える必要あり)
$HnaviExp.="MONSTER$num = '　人造怪獣<br>　町などを目指して移動する'\n";

# 画像ファイル
$HmonsterImage[$num] = 'monster7.gif';
$HmonsterImage2[$num] = ''; # 硬化中

### いのら
$num = 1; # 配列番号
$HmonsterName[$num] = 'いのら';     # 名前
$HmonsterBHP[$num]       = 1;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 5;    # 経験値
$HmonsterValue[$num]     = 400;  # 死体の値段
$HmonsterCost[$num]      = 3400; # 派遣コマンド費用
$HmonsterCostST[$num]    = 6400; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'いのら攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x2;  # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = '　最大何歩移動するか不明'\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster0.gif'; # 画像ファイル
$HmonsterImage2[$num] = ''; # 硬化中

### サンジラ
$num = 2; # 配列番号
$HmonsterName[$num] = 'サンジラ';     # 名前
$HmonsterBHP[$num]       = 1;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 7;    # 経験値
$HmonsterValue[$num]     = 500;  # 死体の値段
$HmonsterCost[$num]      = 3500; # 派遣コマンド費用
$HmonsterCostST[$num]    = 6500; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x4;  # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = '　ランダム硬化'\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster5.gif'; # 画像ファイル
$HmonsterImage2[$num] = 'monster4.gif'; # 硬化中

### レッドいのら
$num = 3; # 配列番号
$HmonsterName[$num] = 'レッドいのら';     # 名前
$HmonsterBHP[$num]       = 3;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 12;   # 経験値
$HmonsterValue[$num]     = 1000; # 死体の値段
$HmonsterCost[$num]      = 4000; # 派遣コマンド費用
$HmonsterCostST[$num]    = 7000; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'レッド攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x0;  # 特殊能力
$HmonsterTerrorHex[$num] = 1;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = ''\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster1.gif'; # 画像ファイル
$HmonsterImage2[$num] = ''; # 硬化中

### ダークいのら
$num = 4; # 配列番号
$HmonsterName[$num] = 'ダークいのら';     # 名前
$HmonsterBHP[$num]       = 2;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 12;   # 経験値
$HmonsterValue[$num]     = 800;  # 死体の値段
$HmonsterCost[$num]      = 3800; # 派遣コマンド費用
$HmonsterCostST[$num]    = 6800; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x1;  # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = '　最大2歩移動する'\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster2.gif'; # 画像ファイル
$HmonsterImage2[$num] = ''; # 硬化中

### いのらゴースト
$num = 5; # 配列番号
$HmonsterName[$num] = 'いのらゴースト';     # 名前
$HmonsterBHP[$num]       = 1;    # 最低体力
$HmonsterDHP[$num]       = 0;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 10;   # 経験値
$HmonsterValue[$num]     = 300;  # 死体の値段
$HmonsterCost[$num]      = 3300; # 派遣コマンド費用
$HmonsterCostST[$num]    = 6300; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x12; # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = '　島コマンド実行前に移動<br>　最大何歩移動するか不明'\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster8.gif'; # 画像ファイル
$HmonsterImage2[$num] = ''; # 硬化中

### クジラ
$num = 6; # 配列番号
$HmonsterName[$num] = 'クジラ';     # 名前
$HmonsterBHP[$num]       = 4;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 20;   # 経験値
$HmonsterValue[$num]     = 1500; # 死体の値段
$HmonsterCost[$num]      = 4500; # 派遣コマンド費用
$HmonsterCostST[$num]    = 7500; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x4;  # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = '　ランダム硬化'\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster6.gif'; # 画像ファイル
$HmonsterImage2[$num] = 'monster4.gif'; # 硬化中

### キングいのら
$num = 7; # 配列番号
$HmonsterName[$num] = 'キングいのら';     # 名前
$HmonsterBHP[$num]       = 5;    # 最低体力
$HmonsterDHP[$num]       = 2;    # 体力の幅 注！体力の最大値は31
$HmonsterExp[$num]       = 30;   # 経験値
$HmonsterValue[$num]     = 2000; # 死体の値段
$HmonsterCost[$num]      = 5000; # 派遣コマンド費用
$HmonsterCostST[$num]    = 8000; # ST派遣コマンド費用
$HmonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HmonsterFire[$num]      = 0;    # 「攻撃能力」攻撃数
$HmonsterFireHex[$num]   = 0;    # 「攻撃能力」攻撃範囲(誤差)
$HmonsterFireRange[$num] = 0;    # 射程距離(ジャミング消去範囲)
$HmonsterDamage[$num]    = 0;    # 破壊力 ※設定なしで1
$HmonsterSpecial[$num]   = 0x0;  # 特殊能力
$HmonsterTerrorHex[$num] = 0;    # 「絨毯爆撃」周囲何Hex
$HnaviExp.="MONSTER$num = ''\n";# ポップアップナビ
$HmonsterImage[$num]  = 'monster3.gif'; # 画像ファイル
$HmonsterImage2[$num] = ''; # 硬化中

#----------------------------------------
# 巨大怪獣
#----------------------------------------
# 種類(最大32種類)
$HhugeMonsterNumber = 3;

# 巨大怪獣が出現する？（0:しない、1:する）
$HhugeMonsterAppear   = 0;

# 単位面積あたりの出現率(0.01%単位)
$HdisHuge   = 1;

# 派遣可能な巨大怪獣の番号の最大値
$HsendHugeMonsterNumber = 0; # -1で派遣不可

# 特殊能力
# 「体の再生をランダムに行う」能力での再生確率(%)
$HpRebody = 100;

# 巨大怪獣出現の基準
@HdisHugeBorder = ( 10000, 10000, 20000);

# 巨大怪獣出現比率
@HdisHugeRatio = ( 1, 1, 1); # 非負整数(0にすると出現しなくなる)
# 出現率判定($HdisHuge)で出現することが決定したのち、人口基準($HdisHugeBorder)をクリアしている
# 巨大怪獣の中から上の比率($HdisHugeRatio)で巨大怪獣を選ぶ

# 巨大怪獣設定(最大32種類)
#----------------------------------------
### ドジラ
$num = 0; # 配列番号
# 名前
$HhugeMonsterName[$num] = 'ドジラ';
# 能力
$HhugeMonsterBHP[$num]       = 6;     # 最低体力
$HhugeMonsterDHP[$num]       = 3;     # 体力の幅 注！体力の最大値は31
$HhugeMonsterExp[$num]       = 20;    # 経験値
$HhugeMonsterValue[$num]     = 2000;  # 死体の値段
$HhugeMonsterCost[$num]      = 32000; # 派遣コマンド費用
$HhugeMonsterCostST[$num]    = 62000; # ST派遣コマンド費用
$HhugeMonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HhugeMonsterFire[$num]      = 0;     # 「攻撃能力」攻撃数
$HhugeMonsterFireHex[$num]   = 0;     # 「攻撃能力」攻撃範囲(誤差)
$HhugeMonsterFireRange[$num] = 0;     # 射程距離(ジャミング消去範囲)
$HhugeMonsterDamage[$num]    = 0;     # 破壊力 ※設定なしで1
$HhugeMonsterSpecial[$num]   = 0x20;  # 特殊能力
# 特殊能力の内容は、
# 0x0 特になし
# 0x1 足が速い(最大2歩あるく)
# 0x2 足がとても速い(最大何歩あるくか不明)
# 0x4 ランダム硬化
# 0x10 先行移動（島コマンド実行前に移動）
# 0x20 蹂躙移動（町などを目指して移動）
# 0x80 移動操縦（島主が移動をコントロール）
# 0x100 攻撃能力（攻撃目標を捕捉し攻撃する）
# 0x200 絨毯爆撃 (初弾の着弾点の周囲数ヘックスを攻撃) ※ミサイル攻撃能力が必要
# 0x10000 コア防衛（周囲すべてを消さない限りコアへの攻撃が無効）
# 0x20000 体の再生をランダムに行う

#「絨毯爆撃」周囲何Hex対象か？※1〜2を設定。
$HhugeMonsterTerrorHex[$num] = 0; # 完全に絨毯爆撃するには1Hex:7発，2Hex:19発が必要です。結果的に攻撃誤差が広がることになります。

# ポップアップナビ解説部分(設定によって書き換える必要あり)
$HnaviExp.="HUGEMONSTER$num = '　町などを目指して移動する'\n";

# 画像ファイル(陸上)
$HhugeMonsterImage[$num] = ['gojira.gif', 'gojira6.gif', 'gojira7.gif', 'gojira8.gif', 'gojira9.gif', 'gojira10.gif', 'gojira11.gif'];
# 画像ファイルその2(陸で硬化中)
$HhugeMonsterImage2[$num] = ['gojira.gif', 'gojira6.gif', 'gojira7.gif', 'gojira8.gif', 'gojira9.gif', 'gojira10.gif', 'gojira11.gif'];
# 画像ファイルその3(海にいる)
$HhugeMonsterImage3[$num] = ['gojira.gif', 'gojira0.gif', 'gojira1.gif', 'gojira2.gif', 'gojira3.gif', 'gojira4.gif', 'gojira5.gif'];
# 画像ファイルその4(海で硬化)
$HhugeMonsterImage4[$num] = ['gojira.gif', 'gojira0.gif', 'gojira1.gif', 'gojira2.gif', 'gojira3.gif', 'gojira4.gif', 'gojira5.gif'];
# 画像ファイル(トップページ表示用)
$HhugeMonsterImageS[$num] = 'gojira.gif'; 

### ハンジラ
$num = 1; # 配列番号
$HhugeMonsterName[$num] = 'ハンジラ'; # 名前
$HhugeMonsterBHP[$num]       = 3;     # 最低体力
$HhugeMonsterDHP[$num]       = 6;     # 体力の幅 注！体力の最大値は31
$HhugeMonsterExp[$num]       = 10;    # 経験値
$HhugeMonsterValue[$num]     = 1000;  # 死体の値段
$HhugeMonsterCost[$num]      = 31000; # 派遣コマンド費用
$HhugeMonsterCostST[$num]    = 61000; # ST派遣コマンド費用
$HhugeMonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HhugeMonsterFire[$num]      = 0;     # 「攻撃能力」攻撃数
$HhugeMonsterFireHex[$num]   = 0;     # 「攻撃能力」攻撃範囲(誤差)
$HhugeMonsterFireRange[$num] = 0;     # 射程距離(ジャミング消去範囲)
$HhugeMonsterDamage[$num]    = 0;     # 破壊力 ※設定なしで1
$HhugeMonsterSpecial[$num]   = 0x20;  # 特殊能力
$HhugeMonsterTerrorHex[$num] = 0;     #「絨毯爆撃」Hex
$HnaviExp.="HUGEMONSTER$num = '　町などを目指して移動する'\n"; # ポップアップナビ
# 画像ファイル(陸上)
$HhugeMonsterImage[$num] = ['gojira.gif', '', 'gojira7.gif', '', 'gojira9.gif', '', 'gojira11.gif'];
# 画像ファイルその2(陸で硬化中)
$HhugeMonsterImage2[$num] = ['gojira.gif', '', 'gojira7.gif', '', 'gojira9.gif', '', 'gojira11.gif'];
# 画像ファイルその3(海にいる)
$HhugeMonsterImage3[$num] = ['gojira.gif', '', 'gojira1.gif', '', 'gojira3.gif', '', 'gojira5.gif'];
# 画像ファイルその4(海で硬化)
$HhugeMonsterImage4[$num] = ['gojira.gif', '', 'gojira1.gif', '', 'gojira3.gif', '', 'gojira5.gif'];
# 画像ファイル(トップページ表示用)
$HhugeMonsterImageS[$num] = 'gojira.gif'; 

### 防衛いのら
$num = 2; # 配列番号
$HhugeMonsterName[$num] = '防衛いのら'; # 名前
$HhugeMonsterBHP[$num]       = 2;     # 最低体力
$HhugeMonsterDHP[$num]       = 1;     # 体力の幅 注！体力の最大値は31
$HhugeMonsterExp[$num]       = 40;    # 経験値
$HhugeMonsterValue[$num]     = 4000;  # 死体の値段
$HhugeMonsterCost[$num]      = 34000; # 派遣コマンド費用
$HhugeMonsterCostST[$num]    = 64000; # ST派遣コマンド費用
$HhugeMonsterFireName[$num] = 'ミサイル攻撃'; # 「攻撃能力」攻撃名称
$HhugeMonsterFire[$num]      = 0;     # 「攻撃能力」攻撃数
$HhugeMonsterFireHex[$num]   = 0;     # 「攻撃能力」攻撃範囲(誤差)
$HhugeMonsterFireRange[$num] = 0;     # 射程距離(ジャミング消去範囲)
$HhugeMonsterDamage[$num]    = 0;     # 破壊力 ※設定なしで1
$HhugeMonsterSpecial[$num]   = 0x30000; # 特殊能力
$HhugeMonsterTerrorHex[$num] = 0;     #「絨毯爆撃」Hex
$HnaviExp.="HUGEMONSTER$num = '　コア防衛・ランダム再生能力をもつ'\n"; # ポップアップナビ
# 画像ファイル(陸上)
$HhugeMonsterImage[$num] = ['monster0.gif', 'monster0.gif', '', 'monster0.gif', '', 'monster0.gif', ''];
# 画像ファイルその2(陸で硬化中)
$HhugeMonsterImage2[$num] = ['monster0.gif', 'monster0.gif', '', 'monster0.gif', '', 'monster0.gif', ''];
# 画像ファイルその3(海にいる)
$HhugeMonsterImage3[$num] = ['monster00.gif', 'monster00.gif', '', 'monster00.gif', '', 'monster00.gif', ''];
# 画像ファイルその4(海で硬化)
$HhugeMonsterImage4[$num] = ['monster00.gif', 'monster00.gif', '', 'monster00.gif', '', 'monster00.gif', ''];
# 画像ファイル(トップページ表示用)
$HhugeMonsterImageS[$num] = 'monster00.gif'; 

#----------------------------------------
# 記念碑
#----------------------------------------
# 何種類あるか
$HmonumentNumber = 3;

# 名前
@HmonumentName = (
	'モノリス', 
	'平和記念碑', 
	'戦いの碑',
);

# ポップアップナビ解説部分(設定によって書き換える必要あり)
$HnaviExp.=<<"END";
MONIMENT0 = "";
MONIMENT1 = "";
MONIMENT2 = "";
END

# 画像ファイル
@HmonumentImage = (
	'monument0.gif',
	'monument1.gif',
	'monument2.gif',
);

# 記念碑発射を使うか？(0:禁止)
$HuseBigMissile = 0;

#----------------------------------------
# アイテム
#----------------------------------------
# アイテムを使うか？(0:禁止)
$HuseItem = 1;

# 同盟ですべての「キーアイテム」を獲得するとゲームを終了する？(0:しない 1:する)
$HallyItemComplete = 1;

# 名前
@HitemName = (
	'クリスタル', # 総称
	'グリーン・クリスタル',
	'レッド・クリスタル',
	'イエロー・クリスタル',
	'ブルー・クリスタル',
	'シルバー・クリスタル',
	'ホワイト・クリスタル',
	'ダーク・クリスタル',

	'ルナ',
	'サラマンダー',
	'ウンディーネ',
	'ドリアード',
	'ジン',
	'ノーム',
	'ウィスプ',
);
#@HitemName = (
#	'フェアリーストーン', # 総称
#	'ルナ',
#	'サラマンダー',
#	'ウンディーネ',
#	'ドリアード',
#	'ジン',
#	'ノーム',
#	'ウィスプ',
#	'シェイド'
#);

# 特殊能力設定
# ['key item',
#	 'どの島でも補給可能', 'ジャミング消去', '保有可能艦艇数+α', '射程を広げるHex数', '攻撃誤差を1Hex縮める確率',
#	 'コマンド実行回数', '食料最大値倍率', '資金最大値倍率', '収穫倍率', '収入倍率', '艦艇攻撃回数倍率', '破壊力倍率'
#	 '艦艇維持食料倍率', '艦艇維持費倍率', '食料消費倍率', 'コマンド費倍率', '破壊力増加'
# ]
@HitemSpecial = (
#    鍵, 補給, ジ消, 保有, 射程, 縮率, コ回, 食max, 金max, 収穫, 収入, 攻数, 破倍, 維食, 維費, 食消, コ費, 地震, 台風, 隕石, 巨隕, 噴火, 火災, 津波, 破＋
	[ 0,    0,    0,    0,    0,    0,    1,     1,     1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    0], # ダミー(変更不可：アイテムを持たない島の設定に使用)
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
#  0:key item(この属性を持つアイテムをすべて集めるとゲーム終了)[0:属性なし,1:属性あり]
#  1:どの島でも補給可能[0:属性なし,1:属性あり]
#  2:ジャミングが消える(ジャミング・モード有効時のみ効果あり)[0:属性なし,1:属性あり]
#  3:保有可能艦艇数を増やす[0:通常,保有可能艦艇数の設定値に注意して正整数を設定すること]
#  4:射程距離を広げるHex数[0:通常,艦艇の能力設定値に注意して正整数を設定すること]
#  5:艦艇の命中率UP:艦艇の攻撃誤差を一定確率で1Hex縮める[0:通常,1〜100:%単位で指定]
#  6:1ターンに実行するコマンド数[1:通常,もちろん正整数，注意して設定すること]
#  7:食料の最大値の倍率[1:通常,(正数を指定:1より大きければプラスアイテム、小さければマイナスアイテム)]
#  8:資金の最大値の倍率[1:通常,(正数を指定:1より大きければプラスアイテム、小さければマイナスアイテム)]
#  9:収穫(食料)の倍率[1:通常,(正数を指定:1より大きければプラスアイテム、小さければマイナスアイテム)]
# 10:収入(資金)の倍率[1:通常,(正数を指定:1より大きければプラスアイテム、小さければマイナスアイテム)]
# 11:艦艇の攻撃回数の倍率[1:通常,(正整数を指定:1より大きければプラスアイテム)]
# 12:艦艇の破壊力の倍率[1:通常,(正整数を指定:1より大きければプラスアイテム)]
# 13:艦艇の維持食料の倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 14:艦艇の維持資金の倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 15:食料の消費の倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 16:コマンドのコストの倍率[1:通常,(正整数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 17:地震発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 18:台風発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 19:隕石発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 20:巨大隕石発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 21:噴火発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 22:火災発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 23:津波発生倍率[1:通常,(正数を指定:1より大きければマイナスアイテム、小さければプラスアイテム)]
# 24:艦艇の破壊力プラス[0:通常,(整数を指定:0より大きければプラスアイテム)]
# アイテムを複数保有する場合、1〜6,24は最大のものが有効、7〜23はすべての倍率を乗じたものになる。

# 画像ファイル
@HitemImage = (
	'item0.gif', # ダミー
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

# アイテム獲得・奪取確率(総獲得経験値÷下に設定した数値)
# 獲得：巨大怪獣退治の時(0:判定しない)
$HitemGetDenominator = 1000;

# 獲得：怪獣退治の時(0:判定しない)
$HitemGetDenominator2 = 10000;

# 獲得：残骸売却の時(0:判定しない)
$HitemGetDenominator3 = 1000;

# 奪取：アイテム保持島の艦艇撃沈の時(0:判定しない 1:最後の1艦(1港)を破壊した時にすべて奪取)
$HitemSeizeDenominator = 100;

# ターン杯ごとに上位の島から順にひとつずつkey itemを与えるか？(クリスタル争奪戦用)
$HitemGivePerTurn = 0; # 0:与えない、1:与える(上位の島から)、2:与える(下位の島から)

#----------------------------------------
# Battle Field 独自設定
#----------------------------------------
# 所属不明艦の出現率(0.01%単位で面積は無関係。0にすると単位面積あたりプレイヤー島の2倍)
$HdisNavyBF = 0;

# 怪獣の出現率(0.01%単位で面積は無関係。0にすると単位面積あたりプレイヤー島の2倍)
$HdisMonsterBF = 0;

# 巨大怪獣の出現率(0.01%単位で面積は無関係。0にすると単位面積あたりプレイヤー島の2倍)
$HdisHugeBF = 0;

# 友好国設定を無効にする？(0:しない 1:する) ※艦艇の補給・索敵・攻撃のみ友好国設定を無効にします
$HamityInvalid = 1;

# アイテムの能力を無効にする？(0:しない 1:する) ※攻撃回数2倍・射程を広げる・全島補給可能・命中率UP・破壊力２倍のみ無効にします
$HitemInvalid = 1;

# 艦艇の能力をアップする？(0:しない n:プラスorマイナス数値指定)
@HnavyFireBF = ( 0, 0, 0, 0); # 攻撃数Fire 攻撃範囲(誤差)FireHex 射程範囲FireRange 破壊力damage

#----------------------------------------
# 天候
#----------------------------------------
# 天候を使うか？(0:禁止)
$HuseWeather = 1;

@HweatherName = (
	'天候', # 総称
	'快晴',
	'晴れ',
	'曇り',
	'濃霧',
	'雨',
	'豪雨',
);

# 天候比率(%で配分しなくてもよい。ただし、配列の最初の要素は、必ず0にしておくこと。)
@HweatherRatio = ( 0, 3, 6, 3, 2, 5, 1);

# 特殊能力
@HweatherSpecial = ( 0, 0x3dc, 0x4cb, 0xa07, 0x970, 0xd24, 0xe11);
# 特殊能力の内容は、！注(0:0, 1:-7, 2:-6, 3:-5, 4:-4, 5:-3, 6:-2, 7:-1, 8:0, 9:+1, a:+2, b:+3, c:+4, d:+5, e:+6, f:+7)
# 0x1〜0xF 気温変化
$HweatherSpecialRatio[0] = 1; # 気温変化数値の倍率
$HrKion = 2; # ランダム要素(+-)
# 0x10〜0xF0 気圧変化
$HweatherSpecialRatio[1] = 5; # 気圧変化数値の倍率
$HrKiatu = 50; # ランダム要素(+-)
# 0x100〜0xF00 湿度変化
$HweatherSpecialRatio[2] = 2; # 湿度変化数値の倍率
$HrSitudo = 15; # ランダム要素(+-)

# 画像ファイル
@HweatherImage = (
	'weather0.gif', # ダミー
	'weather1.gif',
	'weather2.gif',
	'weather3.gif',
	'weather4.gif',
	'weather5.gif',
	'weather6.gif',
);

#----------------------------------------
# 賞関係(最大32種類)
#----------------------------------------
# ターン杯を何ターン毎に出すか
$HturnPrizeUnit = 100;

# 賞の名前
# kind: どの要素で決まるか(ターン杯は上位何島までの受賞か数値指定)
# ptr: ext領域の場合、何番目の要素で決まるか
# threshold: ptrの示す値が幾つになったら受賞か
# money: 賞金
# name: 賞の名前
$Hprize[0]  = { 'name' => 'ターン杯',     'kind' => '1',      'ptr' => 0,  'threshold' => 0,     'contribution' => 0,    'money' => 300 };
$Hprize[1]  = { 'name' => '繁栄賞',       'kind' => 'pop',    'ptr' => 0,  'threshold' => 3000,  'contribution' => 0,    'money' => 3000 };
$Hprize[2]  = { 'name' => '超繁栄賞',     'kind' => 'pop',    'ptr' => 0,  'threshold' => 5000,  'contribution' => 0,    'money' => 5000 };
$Hprize[3]  = { 'name' => '究極繁栄賞',   'kind' => 'pop',    'ptr' => 0,  'threshold' => 10000, 'contribution' => 0,    'money' => 10000 };
$Hprize[4]  = { 'name' => '平和賞',       'kind' => 'achive', 'ptr' => 0,  'threshold' => 200,   'contribution' => 0,    'money' => 200 };
$Hprize[5]  = { 'name' => '超平和賞',     'kind' => 'achive', 'ptr' => 0,  'threshold' => 500,   'contribution' => 0,    'money' => 500 };
$Hprize[6]  = { 'name' => '究極平和賞',   'kind' => 'achive', 'ptr' => 0,  'threshold' => 800,   'contribution' => 0,    'money' => 800 };
$Hprize[7]  = { 'name' => '災難賞',       'kind' => 'damage', 'ptr' => 0,  'threshold' => 500,   'contribution' => 0,    'money' => 500 };
$Hprize[8]  = { 'name' => '超災難賞',     'kind' => 'damage', 'ptr' => 0,  'threshold' => 1000,  'contribution' => 0,    'money' => 1000 };
$Hprize[9]  = { 'name' => '究極災難賞',   'kind' => 'damage', 'ptr' => 0,  'threshold' => 2000,  'contribution' => 0,    'money' => 2000 };
$Hprize[10] = { 'name' => '救国勲章',     'kind' => 'ext',    'ptr' => 1,  'threshold' => 20000, 'contribution' => 0,    'money' => 0 };
$Hprize[11] = { 'name' => '優等救国勲章', 'kind' => 'ext',    'ptr' => 1,  'threshold' => 50000, 'contribution' => 0,    'money' => 0 };
$Hprize[12] = { 'name' => '突撃勲章',     'kind' => 'ext',    'ptr' => 2,  'threshold' => 5,     'contribution' => 500,  'money' => 0 };
$Hprize[13] = { 'name' => '優等突撃勲章', 'kind' => 'ext',    'ptr' => 2,  'threshold' => 10,    'contribution' => 1000, 'money' => 0 };
$Hprize[14] = { 'name' => '騎士勲章',     'kind' => 'ext',    'ptr' => 3,  'threshold' => 10,    'contribution' => 500,  'money' => 0 };
$Hprize[15] = { 'name' => '優等騎士勲章', 'kind' => 'ext',    'ptr' => 3,  'threshold' => 20,    'contribution' => 1000, 'money' => 0 };
$Hprize[16] = { 'name' => '遊撃勲章',     'kind' => 'ext',    'ptr' => 10, 'threshold' => 50,    'contribution' => 1000, 'money' => 0 };
$Hprize[17] = { 'name' => '優等遊撃勲章', 'kind' => 'ext',    'ptr' => 10, 'threshold' => 100,   'contribution' => 5000, 'money' => 0 };
$Hprize[18] = { 'name' => '十字勲章',     'kind' => 'ext',    'ptr' => 4,  'threshold' => 1000,  'contribution' => 500,  'money' => 0 };
$Hprize[19] = { 'name' => '優等十字勲章', 'kind' => 'ext',    'ptr' => 4,  'threshold' => 2000,  'contribution' => 1000, 'money' => 0 };
$Hprize[20] = { 'name' => '御盾勲章',     'kind' => 'ext',    'ptr' => 5,  'threshold' => 50,    'contribution' => 200,  'money' => 0 };
$Hprize[21] = { 'name' => '敢闘勲章',     'kind' => 'ext',    'ptr' => 6,  'threshold' => 50,    'contribution' => 200,  'money' => 0 };
$Hprize[22] = { 'name' => '鉄壁勲章',     'kind' => 'ext',    'ptr' => 7,  'threshold' => 30,    'contribution' => 1000, 'money' => 0 };

#----------------------------------------------------------------------
# その他拡張用の設定(基本的には，変更不可)
#----------------------------------------------------------------------
# ext[0] 勝利フラグ
# ext[1] 功績point(=貢献度x10)
# ext[2] 破壊した防衛施設の数
# ext[3] 破壊したミサイル基地の数
# ext[4] 救出した難民の合計人口
# ext[5] 受けたミサイル数
# ext[6] 発射したミサイル数
# ext[7] 防衛施設で弾いたミサイル数
# ext[8] 派遣した艦艇の数
# ext[9] 派遣された艦艇の数
# ext[10] 破壊した艦艇の数
#----------------------------------------
# 入力文字数の制限(全角文字数で指定)
#----------------------------------------
# 文字制限をオーバーした時、処理を中断するか？(0:しない 1:する)
$HlengthAlert = 1;

$HlengthIslandName  = 15;   # 島の名前
$HlengthOwnerName   = 15;   # 島の所有者の名前
$HlengthMessage     = 40;   # トップページに表示される各島のコメント
$HlengthLbbsName    = 15;   # 「観光掲示板」の投稿者名
$HlengthLbbsMessage = 60;   # 「観光掲示板」の投稿
$HlengthFleetName   = 10;   # 艦隊の名前
$HlengthAllyName    = 15;   # 同盟の名前
$HlengthAllyComment = 40;   # 「各同盟の状況」欄に表示される盟主のコメント
$HlengthAllyTitle   = 30;   # 「同盟の情報」欄の上に表示される盟主メッセージのタイトル
$HlengthAllyMessage = 1500; # 「同盟の情報」欄の上に表示される盟主メッセージ
$HlengthPresentLog  = 100;  # 管理人によるプレゼントモードのメッセージ
#----------------------------------------
# 外見関係
#----------------------------------------
# <BODY>タグのオプション,タイトルはhako-init.cgiへ移動しました

# タグ
# タイトル文字
$HtagTitle_ = '<div class="title">';
$H_tagTitle = '</div>';

# 大きい文字
$HtagBig_ = '<span class="big">';
$H_tagBig = '</span>';

# 島の名前など
$HtagName_ = '<span class="islName">';
$H_tagName = '</span>';

# 薄くなった島の名前
$HtagName2_ = '<span class="islName2">';
$H_tagName2 = '</span>';

# 順位の番号など
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

# 順位表における見だし
$HtagTH_ = '<span class="head">';
$H_tagTH = '</span>';

# 開発計画の名前
$HtagComName_ = '<span class="command">';
$H_tagComName = '</span>';

# 開発計画の名前 ターン消費あり (入力ずみコマンド欄)
$HtagComName1_ = '<span class="command1">';
$HcomNameColor1 = '#A08000'; # CSSの色とそろえる方がいいかも
# 開発計画の名前 ターン消費なし (入力ずみコマンド欄)
$HtagComName2_ = '<span class="command2">';
$HcomNameColor2 = '#0080A0'; # CSSの色とそろえる方がいいかも

# 災害
$HtagDisaster_ = '<span class="disaster">';
$H_tagDisaster = '</span>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# お金
$HtagMoney_ = '<span class="money">';
$H_tagMoney = '</span>';

# 食料
$HtagFood_ = '<span class="food">';
$H_tagFood = '</span>';

# 通常の文字色
$HnormalColor_ = '<span class="normal">';
$H_normalColor = '</span>';

# 順位表、セルの属性
$HbgTitleCell   = 'class=TitleCell';   # 順位表見出し
$HbgNumberCell  = 'class=NumberCell';  # 順位表順位
$HbgNameCell    = 'class=NameCell';    # 順位表島の名前
$HbgInfoCell    = 'class=InfoCell';    # 順位表島の情報
$HbgCommentCell = 'class=CommentCell'; # 順位表コメント欄
$HbgInputCell   = 'class=InputCell';   # 開発計画フォーム
$HbgMapCell     = 'class=MapCell';     # 開発計画地図
$HbgCommandCell = 'class=CommandCell'; # 開発計画入力済み計画

# 最近の天気の色属性
$headNameCellcolor = 'class=headNameCellcolor'; # 最近の天気のヘッダ部分のセル色
$pointCellcolor    = 'class=pointCellcolor';    # 最近の天気の天気部分のセル色
$pointCellcolor2   = 'class=pointCellcolor2';   # 最近の天気の気象数値のセル色
$nameCellcolor     = 'class=nameCellcolor';     # 最近の天気の島名の表示部分のセル色

$tomorrowColor     = 'class=TomorrowColor';     # 最近の天気の明日以降の文字色
$todayColor        = 'class=TodayColor';        # 最近の天気の今日の文字色
$yesterdayColor    = 'class=YesterdayColor';    # 最近の天気の昨日以前の文字色

#----------------------------------------------------------------------
# これ以降のスクリプトは、変更されることを想定していませんが、
# いじってもかまいません。
# コマンドの名前、値段などは解りやすいと思います。
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 各種定数
#----------------------------------------------------------------------
# コマンド

# 計画番号の設定
# 0 内政(開発)
$HcomPrepare  = 1; # 整地
$HcomPrepare2 = 2; # 地ならし
$HcomPrepare3 = 3; # 一括地ならし
$HcomReclaim  = 4; # 埋め立て
$HcomReclaim2 = 5; # 高速埋め立て
$HcomDestroy  = 6; # 掘削
$HcomDestroy2 = 7; # 高速掘削


# 1 内政(建設)
$HcomFarm        = 21; # 農場整備
$HcomFastFarm    = 22; # 高速農場整備
$HcomFactory     = 23; # 工場建設
$HcomFastFactory = 24; # 高速工場建設
$HcomMountain    = 25; # 採掘場整備
$HcomMonument    = 31; # 記念碑建造
$HcomBouha       = 32; # 防波堤設置
$HcomSellTree    = 26; # 伐採
$HcomPlant       = 27; # 植林
$HcomPlant2      = 28; # 高速植林


@HcomComplex = (); # 複合施設
if(!$HuseComplex) { # 使わない場合の処理
	@HcomplexName = ();
	@HcomplexComName = ();
}
foreach (0..$#HcomplexComName) {
	$HcomComplex[$_] = 41 + $_; # 41〜
}
$HcomComplex[0] = 40 if($HcomComplex[0] eq '');

# 2 内政(運営)
$HcomDoNothing  = 91; # *静観
$HcomSell       = 92; # *食料輸出
$HcomBuy        = 93; # *食料輸入
$HcomPropaganda = 94; # *誘致活動
$HcomGiveup     = 95; # *島の放棄

# 3 海軍(建造)
@HcomNavy = ();
#foreach (0..$#HnavyName) {
#	$HcomNavy[$_] = 101 + $_; # 101〜132
#}
#$HcomNavy[0] = 100 if($HcomNavy[0] eq '');




# 手動入力に変更する
$HcomNavy[0]  = 101; # 軍港
$HcomNavy[1]  = 102; # カメレオン
$HcomNavy[2]  = 103; # スパイダー
$HcomNavy[3]  = 104; # シュミット
$HcomNavy[4]  = 105; # ホーク
$HcomNavy[5]  = 106; # 投げ網
$HcomNavy[6]  = 107; # 護国
$HcomNavy[7]  = 108; # メテオ
$HcomNavy[8]  = 109; # 対潜
$HcomNavy[9]  = 110; # 水雷
$HcomNavy[10] = 111; # 防空
$HcomNavy[11] = 112; # 対地
$HcomNavy[12] = 113; # ひゅうが
$HcomNavy[13] = 114; # 零式
$HcomNavy[14] = 115; # 金剛
$HcomNavy[15] = 116; # フォートレス
$HcomNavy[16] = 117; # タイタニック
$HcomNavy[17] = 118; # 大和

$HcomNavy[18] = 119; # 海上防衛
$HcomNavy[19] = 120; # 採掘
$HcomNavy[20] = 121; # 網

# 海外発進
$HcomNavy2[0] = 351; # シュミット海外
$HcomNavy2[1] = 352; # ホーク海外
$HcomNavy2[2] = 353; # 護国海外
$HcomNavy2[3] = 354; # フォートレス海外

# 4 指令(作戦)
$HcomNavyMove        = 201; # 隊移動(派遣・帰還を統合)
#$HcomNavySend        = 202; # 艦隊派遣
#$HcomNavyReturn      = 203; # 艦隊帰還
$HcomNavyForm        = 211; # 隊編成
#$HcomNavyExpell      = 212; # 艦艇除籍（艦隊を抜けて敵になる）旧「目標艦指定」
$HcomNavyDestroy     = 213; # 艦艇破棄
$HcomNavyWreckRepair = 214; # 残骸修理
$HcomNavyWreckSell   = 215; # 残骸売却
$HcomMoveTarget      = 216; # 移動操縦　旧「旗艦・怪獣操作」
$HcomMoveMission     = 217; # 移動指令
#$HcomNavyMission     = 218; # 艦艇指令変更
$HcomNavyTarget      = 219; # 一斉攻撃
$Hcomshikin           = 220; # 資金繰り
$Hcomgoalsetpre      = 221; # 目的地指令(対象)
$Hcomgoalset         = 222; # 目的地指令(目標)
$Hcomremodel         = 223; # 艦艇改修(対潜/水雷/防空/対地)
$Hcomwork            = 224; # スパイダー展開
$HcomSellPort        = 225; # 軍港払下げ
$HcomBuyPort         = 226; # 軍港買収
$HcomWarpA           = 227; # 艦艇指定移動(移動元)
$HcomWarpB           = 228; # 艦艇指定移動(移動先)


# 5 外交
$HcomMoney      = 301; # *資金援助
$HcomFood       = 302; # *食料援助
$HcomAmity      = 311; # *友好国属性変更
$HcomAlly       = 312; # *同盟加盟・脱退
$HcomDeWar      = 321; # *宣戦布告
$HcomCeasefire  = 322; # *停戦打診

# 6 軍事(建設)
$HcomDbase    = 331; # 防衛施設建設
$HcomHaribote = 332; # ハリボテ設置
$HcomSeaMine  = 333; # 機雷設置
$HcomCore     = 340; # コア設置
$HcomBase     = 341; # ミサイル基地建設
$HcomSbase    = 342; # 海底基地建設
$HcomDbase2   = 334; # 高速防衛施設建設

# 7 軍事(攻撃)
@HcomMissile = ();
foreach (0..$#HmissileName) {
	$HcomMissile[$_] = 361 + $_; # 351〜360
}

#if($HcomMissile[0] eq '') {
#	$HcomMissile[0] = 350;
#} else {
#	foreach (0..$#HmissileName) { # ST属性チェック
#		$STcheck{$HcomMissile[$_]} = 1 if($HmissileSpecial[$_] & 0x1);
#	}
#}

$HcomSendMonster   = 361; # 怪獣派遣
$HcomSendMonsterST = 362; # ST怪獣派遣

# 8 自動系
$HcomAutoPrepare  = 401; # フル整地
$HcomAutoPrepare2 = 402; # フル地ならし
$HcomAutoDelete   = 403; # 全コマンド消去
$HcomAutoReclaim  = 404; # 浅瀬埋め立て
$HcomAutoDestroy  = 405; # 浅瀬掘削
$HcomAutoSellTree = 406; # 伐採
$HcomAutoForestry = 407; # 伐採と植林

# 順番
my @comList = (
	# 0 内政(開発)
	 $HcomPrepare, $HcomPrepare2, $HcomPrepare3,
	 $HcomReclaim, $HcomReclaim2, $HcomDestroy, $HcomDestroy2,
	# 1 内政(建設)
#	 $HcomFarm, $HcomFastFarm, $HcomFactory, $HcomFastFactory, $HcomSellTree, $HcomPlant, $HcomPlant2,
	 $HcomBouha, @HcomComplex,
	# 2 内政(運営)
	 $HcomSell, $HcomBuy,  
	 $HcomDoNothing, $HcomPropaganda, $HcomGiveup,
	# 3 海軍(建造)
	 @HcomNavy,
	# 4 指令(作戦)
	 $HcomNavyMove,# $HcomNavySend, $HcomNavyReturn,
	 $HcomNavyForm, $HcomNavyDestroy, $HcomMoveTarget,
	 $HcomNavyWreckRepair, $HcomNavyWreckSell, $Hcomshikin,
	 $Hcomgoalsetpre, $Hcomgoalset, #$HcomWarpA, $HcomWarpB, #$HcomMoveMission, $HcomNavyTarget,
         $Hcomremodel, $Hcomwork, #$HcomBuyPort, $HcomSellPort,
	# 5 外交
	 $HcomMoney, $HcomFood, $HcomAmity, $HcomAlly, $HcomDeWar, $HcomCeasefire,
	# 6 軍事(建設)
	 $HcomCore, 
	 $HcomBase, $HcomDbase, $HcomDbase2, $HcomSbase, $HcomHaribote, $HcomSeaMine,
	# 7 軍事(攻撃)
#	 @HcomMissile,
	 $HcomSendMonster, $HcomSendMonsterST,
         $HcomNavy2[0], $HcomNavy2[1], $HcomNavy2[2], $HcomNavy2[3],

	# 8 自動系
	 $HcomAutoReclaim, $HcomAutoDestroy, $HcomAutoSellTree, $HcomAutoForestry,
	 $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoDelete
	);

#-------------------------------------------------------------------------
# フラグチェック(変更不要)
	my $flagcheck = 0;
	$HuseFlag = 0;
	foreach(@HnavySpecial) {
		if($_ & 0x80) {
			$flagcheck = 1;
		} elsif(!$HsuicideAbility && ($_ & 0x2000000)) {
			$_ |= 0x80; # 旗艦・移動操縦でなければ体当たりしない場合，能力のつけ忘れをフォロー
		}
	}
	foreach(@HmonsterSpecial, @HhugeMonsterSpecial) {
		if($_ & 0x80) {
			$flagcheck = 1;
			last;
		}
	}
	$HuseFlag = $flagcheck; # 能力があっても旗艦・移動操縦させたくない場合は，$flagcheckを0にする。
	if($HcomNavy[0] == 100) {
		$HcountLandPort = 0;
		$HuseFlag       = 0;
		$HusePriority   = 0;
		$HnavyUnknown   = 0;
		$HdisNavyBF     = 0;
	}
# フラグチェックここまで
#-------------------------------------------------------------------------
# コマンドリスト生成(変更不要)
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
$HcommandTotal = $#HcomList + 1; # コマンドの種類
foreach (@HcomList) {
	$HcomUse{$_} = 1;
}

# コマンド分割
# このコマンド分割だけは、自動入力系のコマンドは設定しないで下さい。
@HcommandDivido = (
	'内政(造成),0,20',    # 開発マップ
	'内政(建設),21,40',   # 開発マップ
	"内政(建設),$HcomComplex[0],$HcomComplex[$#HcomplexComName]",   # 開発マップ
	'内政(運営),91,100',
	"海軍,$HcomNavy[0],$HcomNavy[$#HcomNavy]", # 開発マップ
	'作戦指令,201,230',  # 開発マップ 目標マップ
	'外交,301,330',
	'軍事施設,331,350', # 開発マップ
	'攻撃,351,370', # 目標マップ
);



$HcommandAuto = '自動系,401,410';

# 注意：スペースは入れないように
# ○→	'開発,0,10',  # 計画番号00〜10
# ×→	'開発, 0  ,10  ',  # 計画番号00〜10

# 計画の名前と簡易説明、コスト、ターン消費
$HcomName[$HcomPrepare]         = '整地';
$HcomMsgs[$HcomPrepare]         = '荒地、建物系を平地にします。';
$HcomCost[$HcomPrepare]         = 5;
$HcomTurn[$HcomPrepare]         = 1;
$HcomName[$HcomPrepare2]        = '地ならし';
$HcomMsgs[$HcomPrepare2]        = 'ターン消費なしの整地、たくさんやるほど地震の確率が上昇';
$HcomCost[$HcomPrepare2]        = 100;
$HcomTurn[$HcomPrepare2]        = 0;
$HcomName[$HcomPrepare3]        = '一括地ならし';
$HcomMsgs[$HcomPrepare3]        = 'このコマンドひとつで、すべての荒れ地を地ならしします。';
$HcomCost[$HcomPrepare3]        = "荒地数x${HcomCost[$HcomPrepare2]}";
$HcomTurn[$HcomPrepare3]        = 0;
$HcomName[$HcomReclaim]         = '埋め立て';
$HcomMsgs[$HcomReclaim]         = '海→浅瀬→荒地。陸の周囲のみ可能です。';
$HcomCost[$HcomReclaim]         = 150;
$HcomTurn[$HcomReclaim]         = 1;
$HcomName[$HcomReclaim2]        = '高速埋め立て';
$HcomMsgs[$HcomReclaim2]        = 'ターン消費なしの埋め立て。';
$HcomCost[$HcomReclaim2]        = 3000;
$HcomTurn[$HcomReclaim2]        = 0;
$HcomName[$HcomDestroy]         = '掘削';
$HcomMsgs[$HcomDestroy]         = '荒地→浅瀬→海。海で数量指定すると油田探し。';
$HcomCost[$HcomDestroy]         = 200;
$HcomTurn[$HcomDestroy]         = 1;
$HcomName[$HcomDestroy2]        = '高速掘削';
$HcomMsgs[$HcomDestroy2]        = 'ターン消費なしの掘削';
$HcomCost[$HcomDestroy2]        = 4000;
$HcomTurn[$HcomDestroy2]        = 0;
#$HcomName[$HcomSellTree]        = '伐採';
#$HcomMsgs[$HcomSellTree]        = '森で実行すると平地に変化し資金化。';
#$HcomCost[$HcomSellTree]        = 0;
#$HcomTurn[$HcomSellTree]        = 1 - $HnoturnSellTree;
#$HcomName[$HcomPlant]           = '植林';
#$HcomMsgs[$HcomPlant]           = '平地、町系で実行可能。';
#$HcomCost[$HcomPlant]           = 50;
#$HcomTurn[$HcomPlant]           = 1;
#$HcomName[$HcomPlant2]           = '高速植林';
#$HcomMsgs[$HcomPlant2]           = '平地、町系で実行可能。';
#$HcomCost[$HcomPlant2]           = 1000;
#$HcomTurn[$HcomPlant2]           = 0;

#$HcomName[$HcomFarm]            = '農場整備';
#$HcomMsgs[$HcomFarm]            = '食糧源となる施設。最大5万。(複数可)';
#$HcomCost[$HcomFarm]            = 20;
#$HcomTurn[$HcomFarm]            = 1;
#$HcomName[$HcomFastFarm]        = '高速農場整備';
#$HcomMsgs[$HcomFastFarm]        = 'ターン消費なしの農場整備。(複数可)';
#$HcomCost[$HcomFastFarm]        = 500;
#$HcomTurn[$HcomFastFarm]        = 0;
#$HcomName[$HcomFactory]         = '工場建設';
#$HcomMsgs[$HcomFactory]         = '資金源となる施設。最大10万(複数可)';
#$HcomCost[$HcomFactory]         = 100;
#$HcomTurn[$HcomFactory]         = 1;
#$HcomName[$HcomFastFactory]     = '高速工場建設';
#$HcomMsgs[$HcomFastFactory]     = 'ターン消費なしの工場建設。(複数可)';
#$HcomCost[$HcomFastFactory]     = 2500;
#$HcomTurn[$HcomFastFactory]     = 0;

foreach (0..$#HcomplexComName) {
	$HcomName[$HcomComplex[$_]] = $HcomplexComName[$_];
	$HcomMsgs[$HcomComplex[$_]] = $HcomplexComMsgs[$_];
	$HcomCost[$HcomComplex[$_]] = $HcomplexComCost[$_];
	$HcomTurn[$HcomComplex[$_]] = $HcomplexComTurn[$_];
}
$HcomName[$HcomBase]            = 'ミサイル基地建設';
$HcomMsgs[$HcomBase]            = 'ミサイルを撃つのに必要。';
$HcomCost[$HcomBase]            = 300;
$HcomTurn[$HcomBase]            = 1;
$HcomName[$HcomMonument]        = '記念碑建造';
$HcomMsgs[$HcomMonument]        = "$AfterNameのシンボル。追加建設すると・・・";
$HcomCost[$HcomMonument]        = 9999;
$HcomTurn[$HcomMonument]        = 1;
$HcomName[$HcomCore]            = 'コア設置';
$HcomMsgs[$HcomCore]            = "$AfterNameのコア。";
$HcomCost[$HcomCore]            = 9999;
$HcomTurn[$HcomCore]            = 1;
$HcomName[$HcomHaribote]        = 'ハリボテ設置';
$HcomMsgs[$HcomHaribote]        = '見た目が防衛施設、視覚効果以外意味無し？';
$HcomCost[$HcomHaribote]        = 0;
$HcomTurn[$HcomHaribote]        = 0;
$HcomName[$HcomBouha]           = '防波堤設置';
$HcomMsgs[$HcomBouha]           = '周囲２マスを津波の被害から守ります';
$HcomCost[$HcomBouha]           = 500;
$HcomTurn[$HcomBouha]           = 1;
$HcomName[$HcomDbase]           = '防衛施設建設';
$HcomMsgs[$HcomDbase]           = '周囲のミサイルを防ぐ。';
$HcomCost[$HcomDbase]           = 1000;
$HcomTurn[$HcomDbase]           = 1;
$HcomName[$HcomDbase2]          = '高速防衛施設建設';
$HcomMsgs[$HcomDbase2]          = '周囲のミサイルを防ぐ。';
$HcomCost[$HcomDbase2]          = 3000;
$HcomTurn[$HcomDbase2]          = 0;
$HcomName[$HcomMountain]        = '採掘場整備';
$HcomMsgs[$HcomMountain]        = '資金源となる施設。災害に強い。最大20万(複数可)。';
$HcomCost[$HcomMountain]        = 300;
$HcomTurn[$HcomMountain]        = 1;
$HcomName[$HcomSeaMine]         = '機雷設置';
$HcomMsgs[$HcomSeaMine]         = '海に設置。すでにあれば除去。数量で破壊力指定。';
$HcomCost[$HcomSeaMine]         = 300;
$HcomTurn[$HcomSeaMine]         = 1;
$HcomName[$HcomSbase]           = '海底基地建設';
$HcomMsgs[$HcomSbase]           = '海にミサイル基地を作る';
$HcomCost[$HcomSbase]           = 8000;
$HcomTurn[$HcomSbase]           = 1;

foreach (0..$#HmissileName) {
	$HcomName[$HcomMissile[$_]] = $HmissileName[$_] . '発射';
	$HcomMsgs[$HcomMissile[$_]] = $HmissileMsgs[$_];
	$HcomCost[$HcomMissile[$_]] = $HmissileCost[$_];
	$HcomTurn[$HcomMissile[$_]] = $HmissileTurn[$_];
}

$HcomName[$HcomSendMonster]     = '怪獣派遣';
$HcomMsgs[$HcomSendMonster]     = '怪獣を出現させる。';
$HcomCost[$HcomSendMonster]     = '@種別費';
$HcomTurn[$HcomSendMonster]     = 1;
$HcomName[$HcomSendMonsterST]   = 'ST怪獣派遣';
$HcomMsgs[$HcomSendMonsterST]   = '怪獣を出現させる、むやみに出現させるのはやめましょう';
$HcomCost[$HcomSendMonsterST]   = '@種別費';
$HcomTurn[$HcomSendMonsterST]   = 0; # STの連続は不可

#foreach (0..$#HnavyName) {
#	$HcomName[$HcomNavy[$_]] = $HnavyName[$_] . (($HnavySpecial[$_] & 0x8) ? '建設' : '建造');
#	$HcomMsgs[$HcomNavy[$_]] = $HnavyName[$_] . 'を' . (($HnavySpecial[$_] & 0x8) ? '建設' : '建造');
#	$HcomCost[$HcomNavy[$_]] = $HnavyCost[$_];
#	$HcomTurn[$HcomNavy[$_]] = 1;
#}

# 手動入力に変更
$HcomName[$HcomNavy[0]]     = '軍港建設';
$HcomMsgs[$HcomNavy[0]]     = '軍港を建設します';
$HcomCost[$HcomNavy[0]]     = $HnavyCost[0];
$HcomTurn[$HcomNavy[0]]     = 1;
$HcomName[$HcomNavy[1]]     = 'カメレオン対獣艇建造';
$HcomMsgs[$HcomNavy[1]]     = 'カメレオン対獣艇を建造します';
$HcomCost[$HcomNavy[1]]     = $HnavyCost[1];
$HcomTurn[$HcomNavy[1]]     = 1;
$HcomName[$HcomNavy[2]]     = 'スパイダー工作艇建造';
$HcomMsgs[$HcomNavy[2]]     = 'スパイダー工作艇を建造します';
$HcomCost[$HcomNavy[2]]     = $HnavyCost[2];
$HcomTurn[$HcomNavy[2]]     = 1;
$HcomName[$HcomNavy[3]]     = 'シュミット戦闘機発進';
$HcomMsgs[$HcomNavy[3]]     = 'シュミット戦闘機を発進します';
$HcomCost[$HcomNavy[3]]     = $HnavyCost[3];
$HcomTurn[$HcomNavy[3]]     = 0;
$HcomName[$HcomNavy[4]]     = 'ホーク攻撃機発進';
$HcomMsgs[$HcomNavy[4]]     = 'ホーク攻撃機を発進します';
$HcomCost[$HcomNavy[4]]     = $HnavyCost[4];
$HcomTurn[$HcomNavy[4]]     = 0;
$HcomName[$HcomNavy[5]]     = '投網漁船建造';
$HcomMsgs[$HcomNavy[5]]     = '投網漁船を建造します';
$HcomCost[$HcomNavy[5]]     = $HnavyCost[5];
$HcomTurn[$HcomNavy[5]]     = 1;
$HcomName[$HcomNavy[6]]     = '護国攻撃機発進';
$HcomMsgs[$HcomNavy[6]]     = '護国攻撃機を発進します';
$HcomCost[$HcomNavy[6]]     = $HnavyCost[6];
$HcomTurn[$HcomNavy[6]]     = 0;
$HcomName[$HcomNavy[7]]     = 'メテオ潜航艇建造';
$HcomMsgs[$HcomNavy[7]]     = 'メテオ建造艇を建造します';
$HcomCost[$HcomNavy[7]]     = $HnavyCost[7];
$HcomTurn[$HcomNavy[7]]     = 1;
$HcomName[$HcomNavy[8]]     = '霞級駆逐艦(対潜型)建造';
$HcomMsgs[$HcomNavy[8]]     = '霞級駆逐艦(対潜型)を建造します';
$HcomCost[$HcomNavy[8]]     = $HnavyCost[8];
$HcomTurn[$HcomNavy[8]]     = 1;
$HcomName[$HcomNavy[9]]     = '霞級駆逐艦(水雷型)建造';
$HcomMsgs[$HcomNavy[9]]     = '霞級駆逐艦(水雷型)を建造します';
$HcomCost[$HcomNavy[9]]     = $HnavyCost[9];
$HcomTurn[$HcomNavy[9]]     = 1;
$HcomName[$HcomNavy[10]]    = '霞級駆逐艦(防空型)建造';
$HcomMsgs[$HcomNavy[10]]    = '霞級駆逐艦(防空型)を建造します';
$HcomCost[$HcomNavy[10]]    = $HnavyCost[10];
$HcomTurn[$HcomNavy[10]]    = 1;
$HcomName[$HcomNavy[11]]    = '霞級駆逐艦(対地型)建造';
$HcomMsgs[$HcomNavy[11]]    = '霞級駆逐艦(対地型)を建造します';
$HcomCost[$HcomNavy[11]]    = $HnavyCost[11];
$HcomTurn[$HcomNavy[11]]    = 1;
$HcomName[$HcomNavy[12]]    = 'ひゅうが級護衛空母建造';
$HcomMsgs[$HcomNavy[12]]    = 'ひゅうが級護衛空母を建造します';
$HcomCost[$HcomNavy[12]]    = $HnavyCost[12];
$HcomTurn[$HcomNavy[12]]    = 1;
$HcomName[$HcomNavy[13]]    = '零式潜水艦建造';
$HcomMsgs[$HcomNavy[13]]    = '零式潜水艦を建造します';
$HcomCost[$HcomNavy[13]]    = $HnavyCost[13];
$HcomTurn[$HcomNavy[13]]    = 1;
$HcomName[$HcomNavy[14]]    = '金剛級戦艦建造';
$HcomMsgs[$HcomNavy[14]]    = '金剛級戦艦を建造します';
$HcomCost[$HcomNavy[14]]    = $HnavyCost[14];
$HcomTurn[$HcomNavy[14]]    = 1;
$HcomName[$HcomNavy[15]]    = 'フォートレス爆撃機発進';
$HcomMsgs[$HcomNavy[15]]    = 'フォートレス爆撃機を発進します';
$HcomCost[$HcomNavy[15]]    = $HnavyCost[15];
$HcomTurn[$HcomNavy[15]]    = 0;
$HcomName[$HcomNavy[16]]    = '豪華客船タイタニック建造';
$HcomMsgs[$HcomNavy[16]]    = '豪華客船タイタニックをを建造します';
$HcomCost[$HcomNavy[16]]    = $HnavyCost[16];
$HcomTurn[$HcomNavy[16]]    = 1;
$HcomName[$HcomNavy[17]]    = '大和級巨大戦艦建造';
$HcomMsgs[$HcomNavy[17]]    = '大和級巨大戦艦を建造します';
$HcomCost[$HcomNavy[17]]    = $HnavyCost[17];
$HcomTurn[$HcomNavy[17]]    = 1;


$HcomName[$HcomNavy2[0]]     = 'シュミット戦闘機海外発進';
$HcomMsgs[$HcomNavy2[0]]     = 'シュミット戦闘機を発進します';
$HcomCost[$HcomNavy2[0]]     = $HnavyCost[3];
$HcomTurn[$HcomNavy2[0]]     = 0;
$HcomName[$HcomNavy2[1]]     = 'ホーク攻撃機海外発進';
$HcomMsgs[$HcomNavy2[1]]     = 'ホーク攻撃機を発進します';
$HcomCost[$HcomNavy2[1]]     = $HnavyCost[4];
$HcomTurn[$HcomNavy2[1]]     = 0;
$HcomName[$HcomNavy2[2]]     = '護国攻撃機海外発進';
$HcomMsgs[$HcomNavy2[2]]     = '護国攻撃機を発進します';
$HcomCost[$HcomNavy2[2]]     = $HnavyCost[6];
$HcomTurn[$HcomNavy2[2]]     = 0;
$HcomName[$HcomNavy2[3]]    = 'フォートレス爆撃機海外発進';
$HcomMsgs[$HcomNavy2[3]]    = 'フォートレス爆撃機を発進します';
$HcomCost[$HcomNavy2[3]]    = $HnavyCost[15];
$HcomTurn[$HcomNavy2[3]]    = 0;


$HcomName[$HcomNavyMove]        = '隊移動';
$HcomMsgs[$HcomNavyMove]        = "派遣・帰還の区別なく$AfterNameから$AfterNameへ艦隊を移動します";
$HcomCost[$HcomNavyMove]        = 0;
$HcomTurn[$HcomNavyMove]        = 1;
$HcomName[$HcomNavySend]        = '艦隊派遣';
$HcomMsgs[$HcomNavySend]        = '艦隊を派遣します';
$HcomCost[$HcomNavySend]        = 0;
$HcomTurn[$HcomNavySend]        = 1;
$HcomName[$HcomNavyReturn]      = '艦隊帰還';
$HcomMsgs[$HcomNavyReturn]      = '派遣艦隊を帰還します';
$HcomCost[$HcomNavyReturn]      = 0;
$HcomTurn[$HcomNavyReturn]      = 1;
$HcomName[$HcomNavyForm]        = '隊編成';
$HcomMsgs[$HcomNavyForm]        = '艦艇の所属艦隊を数量指定で変更します';
$HcomCost[$HcomNavyForm]        = 0;
$HcomTurn[$HcomNavyForm]        = 0;
$HcomName[$HcomNavyExpell]      = '艦艇除籍';
$HcomMsgs[$HcomNavyExpell]      = '艦艇を所属不明にかえます';
$HcomCost[$HcomNavyExpell]      = 0;
$HcomTurn[$HcomNavyExpell]      = 0;
$HcomName[$HcomNavyDestroy]     = '艦艇破棄';
$HcomMsgs[$HcomNavyDestroy]     = '艦艇を海にかえます';
$HcomCost[$HcomNavyDestroy]     = 0;
$HcomTurn[$HcomNavyDestroy]     = 0;
$HcomName[$HcomNavyWreckRepair] = '残骸修理';
$HcomMsgs[$HcomNavyWreckRepair] = '修理した艦艇は艦隊に加わります';
$HcomCost[$HcomNavyWreckRepair] = '@実費';
$HcomTurn[$HcomNavyWreckRepair] = 1;
$HcomName[$HcomNavyWreckSell]   = '残骸売却';
$HcomMsgs[$HcomNavyWreckSell]   = '売却時に金塊を発見することもあります';
$HcomCost[$HcomNavyWreckSell]   = '@時価';
$HcomTurn[$HcomNavyWreckSell]   = 1;
$HcomName[$HcomMoveTarget]      = '移動操縦';
$HcomMsgs[$HcomMoveTarget]      = '旗艦に対して移動方向を指示できます';
$HcomCost[$HcomMoveTarget]      = 0;
$HcomTurn[$HcomMoveTarget]      = 0;
$HcomName[$Hcomgoalsetpre]      = '目的地指令(対象)';
$HcomMsgs[$Hcomgoalsetpre]      = '移動地点指示の準備を行います';
$HcomCost[$Hcomgoalsetpre]      = 0;
$HcomTurn[$Hcomgoalsetpre]      = 0;
$HcomName[$Hcomgoalset]         = '目的地指令(目標)';
$HcomMsgs[$Hcomgoalset]         = '移動地点を指示します';
$HcomCost[$Hcomgoalset]         = 0;
$HcomTurn[$Hcomgoalset]         = 0;
$HcomName[$HcomWarpA]           = '艦艇指定移動(移動元)';
$HcomMsgs[$HcomWarpA]           = '艦艇を軍港から別の軍港へ移動させます';
$HcomCost[$HcomWarpA]           = 0;
$HcomTurn[$HcomWarpA]           = 0;
$HcomName[$HcomWarpB]           = '艦艇指定移動(移動先)';
$HcomMsgs[$HcomWarpB]           = '艦艇を軍港から別の軍港へ移動させます';
$HcomCost[$HcomWarpB]           = 0;
$HcomTurn[$HcomWarpB]           = 1;
$HcomName[$Hcomremodel]         = '艦艇改修(対潜/水雷/防空/対地)';
$HcomMsgs[$Hcomremodel]         = '霞級駆逐艦を改修します';
$HcomCost[$Hcomremodel]         = 0;
$HcomTurn[$Hcomremodel]         = 0;
$HcomName[$Hcomwork]            = '艦艇展開(軍港/海防/採掘/定置)';
$HcomMsgs[$Hcomwork]            = 'スパイダー工作艇を展開します';
$HcomCost[$Hcomwork]            = 0;
$HcomTurn[$Hcomwork]            = 1;
$HcomName[$HcomSellPort]        = '軍港払下げ';
$HcomMsgs[$HcomSellPort]        = '軍港を民間に払い下げます';
$HcomCost[$HcomSellPort]        = 0;
$HcomTurn[$HcomSellPort]        = 1;
$HcomName[$HcomBuyPort]         = '軍港買収';
$HcomMsgs[$HcomBuyPort]         = '民間の軍港を買収します';
$HcomCost[$HcomBuyPort]         = 6000;
$HcomTurn[$HcomBuyPort]         = 1;

$HcomName[$HcomMoveMission]     = '移動指令';
$HcomMsgs[$HcomMoveMission]     = '艦隊に対して移動目標を指示できます。解除するまで有効です。一の位が艦隊番号・十の位に9をつけると解除';
$HcomCost[$HcomMoveMission]     = 0;
$HcomTurn[$HcomMoveMission]     = 0;
$HcomName[$HcomNavyMission]     = '艦艇指令変更';
$HcomMsgs[$HcomNavyMission]     = '通常(0)・巡航(1)・退治(2)・停船(3)の切り替え。十の位で艦隊指定できます';
$HcomCost[$HcomNavyMission]     = 0;
$HcomTurn[$HcomNavyMission]     = 0;
$HcomName[$HcomNavyTarget]      = '一斉攻撃';
$HcomMsgs[$HcomNavyTarget]      = '指定した地点を射程内にもつ艦艇の攻撃対象にする指令です';
$HcomCost[$HcomNavyTarget]      = 1000;
$HcomTurn[$HcomNavyTarget]      = 1;
$HcomName[$Hcomshikin]           = '臨時収入';
$HcomMsgs[$Hcomshikin]           = "2000$HunitMoney入金あり。";
$HcomCost[$Hcomshikin]           = 0;
$HcomTurn[$Hcomshikin]           = 1;

$HcomName[$HcomAmity]           = '友好国に設定・解除';
$HcomMsgs[$HcomAmity]           = "設定した$AfterNameへは艦艇攻撃しなくなります";
$HcomCost[$HcomAmity]           = 0;
$HcomTurn[$HcomAmity]           = 0;
$HcomName[$HcomAlly]            = '同盟へ加盟・脱退';
$HcomMsgs[$HcomAlly]            = "盟主もしくは同盟所属の$AfterNameを指定します";
$HcomCost[$HcomAlly]            = 0;
$HcomTurn[$HcomAlly]            = 1;
$HcomName[$HcomDeWar]           = '宣戦布告';
$HcomMsgs[$HcomDeWar]           = '交戦国に指定するコマンドです';
$HcomCost[$HcomDeWar]           = 0;
$HcomTurn[$HcomDeWar]           = 0;
$HcomName[$HcomCeasefire]       = '停戦打診';
$HcomMsgs[$HcomCeasefire]       = '交戦状態を解除するためには合意が必要です';
$HcomCost[$HcomCeasefire]       = 0;
$HcomTurn[$HcomCeasefire]       = 0;

$HcomName[$HcomSell]            = '食料輸出';
$HcomMsgs[$HcomSell]            = '食料を資金にかえます';
$HcomCost[$HcomSell]            = -1000;
$HcomTurn[$HcomSell]            = 0;
$HcomName[$HcomBuy]             = '食料輸入';
$HcomMsgs[$HcomBuy]             = '資金を食料にかえます';
$HcomCost[$HcomBuy]             = 100;
$HcomTurn[$HcomBuy]             = 0;
$HcomName[$HcomMoney]           = '資金援助';
$HcomMsgs[$HcomMoney]           = '援助量を数量指定します';
$HcomCost[$HcomMoney]           = 100;
$HcomTurn[$HcomMoney]           = 0;
$HcomName[$HcomFood]            = '食料援助';
$HcomMsgs[$HcomFood]            = '援助量を数量指定します';
$HcomCost[$HcomFood]            = -100;
$HcomTurn[$HcomFood]            = 0;
$HcomName[$HcomPropaganda]      = '誘致活動';
$HcomMsgs[$HcomPropaganda]      = '人口が増えます';
$HcomCost[$HcomPropaganda]      = 1000;
$HcomTurn[$HcomPropaganda]      = 1;
$HcomName[$HcomGiveup]          = "${AfterName}の放棄";
$HcomMsgs[$HcomGiveup]          = '島がなくなります';
$HcomCost[$HcomGiveup]          = 0;
$HcomTurn[$HcomGiveup]          = 1;
$HcomName[$HcomDoNothing]       = '静観';
$HcomMsgs[$HcomDoNothing]       = "$HdoNothingMoney$HunitMoney入金あり。自動放棄に注意！";
$HcomCost[$HcomDoNothing]       = 0;
$HcomTurn[$HcomDoNothing]       = 1; # 0にしても1。ムダです(^^)V

$HcomName[$HcomAutoPrepare]     = '整地自動入力';
$HcomMsgs[$HcomAutoPrepare]     = '今ある荒地にすべて整地をセット';
$HcomCost[$HcomAutoPrepare]     = 0;
$HcomTurn[$HcomAutoPrepare]     = 0;
$HcomName[$HcomAutoPrepare2]    = '地ならし自動入力';
$HcomMsgs[$HcomAutoPrepare2]    = '今ある荒地にすべて地ならしをセット';
$HcomCost[$HcomAutoPrepare2]    = 0;
$HcomTurn[$HcomAutoPrepare2]    = 0;
$HcomName[$HcomAutoDelete]      = '全計画を白紙撤回';
$HcomMsgs[$HcomAutoDelete]      = '計画を全て入れなおしたい時に';
$HcomCost[$HcomAutoDelete]      = 0;
$HcomTurn[$HcomAutoDelete]      = 0;
$HcomName[$HcomAutoReclaim]     = '浅瀬埋め立て自動入力';
$HcomMsgs[$HcomAutoReclaim]     = '今ある浅瀬にすべて埋め立てをセット';
$HcomCost[$HcomAutoReclaim]     = 0;
$HcomTurn[$HcomAutoReclaim]     = 0;
$HcomName[$HcomAutoDestroy]     = '浅瀬掘削自動入力';
$HcomMsgs[$HcomAutoDestroy]     = '今ある浅瀬にすべて掘削をセット';
$HcomCost[$HcomAutoDestroy]     = 0;
$HcomTurn[$HcomAutoDestroy]     = 0;
$HcomName[$HcomAutoSellTree]    = '伐採自動入力';
$HcomMsgs[$HcomAutoSellTree]    = '数量の数(単位百)より少ない森が対象';
$HcomCost[$HcomAutoSellTree]    = 0;
$HcomTurn[$HcomAutoSellTree]    = 0;
$HcomName[$HcomAutoForestry]    = '伐採＆植林自動入力';
$HcomMsgs[$HcomAutoForestry]    = '数量の数(単位百)より少ない森を伐採し、新たに植林しなおす。';
$HcomCost[$HcomAutoForestry]    = 0;
$HcomTurn[$HcomAutoForestry]    = 0;

1;