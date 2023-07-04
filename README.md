# TakayaSora
## インストール方法
git clone https://github.com/Tsora1216/TakayaSora.git

使用できる関数は下記のとおりです。

## データベースのセットアップ
SQL_SetUp("database.sqlite")

## データの取得と表示
df = SQL_GetData("database.sqlite")
print(df)

## 角度と距離を入力
angle = float(input('角度を入力してください: '))
distance = float(input('距離を入力してください: '))

## SAP-netにベクトル情報を渡して拡散
SAP_df = SAP_net(df,angle,distance)

## SAP-netが選んだ知識を出力
select_knowledge = selection(SAP_df)
print(SAP_df)
print(select_knowledge)

##　edfファイルをcsvファイルに変換する
