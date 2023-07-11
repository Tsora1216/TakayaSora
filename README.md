# 概要
Package名：TakayaSora<br>
使用項目A：SAP-Net用のパッケージ<br>
使用項目B：EDFファイル用のパッケージ<br>

## インストール
```bat
pip install git+https://github.com/Tsora1216/TakayaSora
```

# SAP-Net Package
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

# EDF4CSV Package
## 一つのEDFファイルをCSVファイルに変換
この関数の使用方法としては、ファイルパスを一つのパラメータとして渡してあげる形で使用してください。
```Python
edf4csv("Sample.edf")
```

渡したEDFファイルパスと同じ階層、同じファイル名でCSVファイルが生成される<br>
実行後は下記のような出力となる。<br>
![](https://gyazo.com/66b3de15c5b304b7200fc9df8fa4f30c.png)

## 複数のEDFファイルをCSVファイルに変換
この関数の使用方法としては、フォルダパスを一つのパラメータとして渡してあげる形で使用してください。
```Python
edf4csv_folder("./sample/")
```

渡したEDFフォルダパスと同じ階層、同じファイル名でCSVファイルが生成される<br>
実行後は下記のような出力となる。<br>
![](https://gyazo.com/d732841a7977587deb5da48776e99cf4.png)

