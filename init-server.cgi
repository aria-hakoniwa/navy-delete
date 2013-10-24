#----------------------------------------------------------------------
# 箱庭諸島 海戦 JS ver7.xx
# サーバー設定モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# The Return of Neptune: http://no-one.s53.xrea.com/
#----------------------------------------------------------------------

# デバッグモード(1だと、「ターンを進める」ボタンが使用できる)
$Hdebug = 0;

#----------------------------------------
# サーバー
#----------------------------------------
# このファイルを置くディレクトリ
$HbaseDir = 'http://muhochitai.com/navy';

# 画像ファイルを置くディレクトリ
$HimageDir = 'http://muhochitai.com/navy/hakogif';

# 外部jsファイル、設定一覧(setup.html)を置くディレクトリ
$efileDir = "${HbaseDir}";
# $HbaseDirから$efileDirへの相対パス(『ローカル設定』できるようにしたい場合は、このままでいいでしょう)
$HefileDir = '.';


# CSSを置くディレクトリ
$HcssDir = "${HbaseDir}";
# デフォルトCSSファイルの名前
$HcssDefault = 'style.css';

# パスワードファイル名
# マスタパスワードと特殊パスワードは暗号化されてパスワードファイルに記憶されています。
$HpasswordFile = 'passwd.cgi';

# GMT に対する JST の時差（サーバの時刻が狂っている時だけ調整してください）
$Hjst = 32400; # 9時間

# 管理者名
$HadminName = 'なちゅらる・��';

# 管理者のメールアドレス
$Hemail = 'navy@muhochitai.com';

# 掲示板アドレス
#$Hbbs = 'http://サーバー/掲示板.cgi';
# 通常の掲示板もYY-BOARDを利用する場合
$Hbbs = "http://jbbs.livedoor.jp/game/26601/";

# ホームページのアドレス
$Htoppage = 'http://park14.wakwak.com/~dai/sharechat/hakoniwa.html';

## 画像のローカル設定の説明ページ
$imageExp = "${HbaseDir}/e.html";
# ローカル画像圧縮ファイル(ダウンロードしてもらう)
$localImg = "${HimageDir}/navyimg.zip";

# ディレクトリのパーミッション
# 通常は0755でよいが、0777、0705、0704等でないとできないサーバーもあるらしい
$HdirMode = 0755;

# データディレクトリの名前
# ここで設定した名前のディレクトリ以下にデータが格納されます。
# デフォルトでは'data'となっていますが、セキュリティのため
# なるべく違う名前に変更してください。
$HdirName    = 'VuNkoOOo';   # メインデータ,島データ,ログデータ
$HlogdirName = 'ubraei';    # ローカル掲示板データ,歴代記録
$HsavedirName = 'lqjuasedfh';  # 地形セーブデータ(トーナメント関連)

# メインデータの名前
$HmainData = 'hakojima.cgi';

# 島データの名前(この前に'島ID'がつきます)
$HsubData = 'island.cgi';

# コマンドデータの名前(この前に'島ID'がつきます)
$HcommandData = 'command.cgi';

# ログデータの名前
$HlogData = 'hakolog.cgi';
#！注：ver6.36.8以前のログは読めません。移行した場合、サーバ上に古いデータが残ってしまいますから、手動で削除してください。

# 島データのアップロードを使う。(0:禁止)
$HuseUpload = 1; # 禁止を推奨します
# アップロードスクリプト(ロックしないので名称変更推奨)
$HuploadFile = "${HbaseDir}/hako-upload.cgi";

# データの書き込み方

# ロックの方式
# 1 ディレクトリ<mkdir>
# 2 システムコール(可能ならば最も望ましい)<flock>
# 3 シンボリックリンク<symlink>
# 4 通常ファイル(あまりお勧めでない)<unlink>
# 5 リネーム<rename>
$lockMode = 5;
# (注)
# 4,5を選択する場合には、'lockfile'という、パーミション666の空のファイルを、
# このファイルと同位置に置いて下さい。

# gzipを使用して圧縮伝送する？ 0 : 未使用  1 : 使用
$Hgzip = 0;

# gzipのインストール先
$HpathGzip = '/usr/bin';

$oroti = 0;# BASE HREFを無効にする極道な広告対策(1で有効)

1;