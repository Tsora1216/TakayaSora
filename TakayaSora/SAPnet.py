import sqlite3
import numpy as np
import pandas as pd
import mne
import os


def SQL_SetUp(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # データベースファイルが存在する場合は処理を終了
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = cursor.fetchall()
    if existing_tables:
        print("Database already exists. Exiting setup.")
        conn.close()
        return

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            angle FLOAT,
            distance FLOAT,
            activation FLOAT DEFAULT 0,
            description TEXT
        )
    ''')
    
    """
        ("直進", 333.44, 1.12, 0),#１番の知識
        ("左寄りの直進", 345.97, 1.03, 0),#２番の知識
        ("右寄りの直進", 0, 1, 0),#１番の知識
        ("右寄りの直進", 14.04, 1.03, 0),#１番の知識
        ("直進", 26.56, 1.12, 0)#１番の知識
    """

    data = [
        ("直進", 18.44, 1.12, 0),#１番の知識
        ("左寄りの直進", 25.97, 1.03, 0),#２番の知識
        ("右寄りの直進", 45, 1, 0),#１番の知識
        ("右寄りの直進", 59.04, 1.03, 0),#１番の知識
        ("直進", 71.56, 1.12, 0)#１番の知識
    ]

    # データを挿入
    cursor.executemany("INSERT INTO knowledge (description, angle, distance, activation) VALUES (?, ?, ?, ?)", data)

    conn.commit()
    conn.close()

def SQL_GetData(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # データを取得してDataFrameに格納
    cursor.execute("SELECT * FROM knowledge")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    conn.close()

    return df

# 新しいデータを追加
def SAP_net(df,new_angle,new_distance):
    new_id = len(df) + 1
    new_activation = -1.0
    new_description = '障害物'

    new_data = pd.DataFrame({
        'id': [new_id],
        'activation': [new_activation],
        'description': [new_description],
        'angle': [new_angle],
        'distance': [new_distance]
    })

    input_df = pd.concat([df, new_data], ignore_index=True)

    # idとdescriptionを結合した文字列を作成
    input_df['id_description'] = input_df['id'].astype(str) + '_' + input_df['description']

    # ベクトルとして角度と距離を使用するため、データを準備
    vectors = input_df[['angle', 'distance']]

    # ベクトル間のユークリッド距離を計算
    distances = np.linalg.norm(vectors.values[:, np.newaxis] - vectors.values, axis=2)

    # クロス表に距離を格納
    cross_table = pd.DataFrame(distances, index=input_df['id_description'], columns=input_df['id_description'])

    # ユークリッド距離を求めたcross_table
    #print(cross_table)

    # ユークリッド距離の評価指標を計算し、再度DataFrameに格納
    max_distance = np.nanmax(cross_table.values)  # ユークリッド距離の最大値（NaNを除く）
    evaluated_values = 1 - cross_table.values / max_distance
    activation_table = pd.DataFrame(evaluated_values, index=cross_table.index, columns=cross_table.columns)

    # ユークリッド距離を正規化した値をdfに格納
    #print(activation_table)

    # 評価指標を1/10にスケーリング
    activation_table_div10 = activation_table / 10
    activation_table_min1 = 1-activation_table

    input_df2=input_df.copy()

    for i in range(len(activation_table_div10.columns)-1):
        activity_value_temp = activation_table_div10.loc[activation_table_div10.columns[i], activation_table_div10.columns[-1]]
        input_df2.loc[input_df2['id_description'] == activation_table_div10.columns[i], 'activation'] += activity_value_temp

    # 画像を格納するリスト
    images = []

    while not (input_df2['activation'] > 1).any():
        for i in range(len(activation_table_div10.columns)):
            for j in range(len(activation_table_div10.columns)):
                if i==j:
                    continue
                activity_value_temp = activation_table_div10.loc[activation_table_div10.columns[i], activation_table_div10.columns[j]]
                input_df2.loc[input_df2['id_description'] == activation_table_div10.columns[i], 'activation'] += activity_value_temp
            input_df2['activation'] = input_df2['activation'] - 0.01
    return input_df2

def selection(input_df2):
    # descriptionの最大値を持つレコードを出力
    max_description = input_df2['activation'].max()
    max_records = input_df2[input_df2['activation'] == max_description]
    select_knowledge = max_records['id_description'][0]
    return select_knowledge

def dataframe_fix(data):
    # 一番最後の列を削除
    data = data.iloc[:, :-1]
    # 一番最後の行を削除
    data = data.iloc[:-1, :]
    
    return data

def apply_forgetting(data):
    data['activation'] =  data['activation']-0.5
    return data

def edf4csv(edf_filepath):
    csv_filepath = os.path.splitext(edf_filepath)[0] + ".csv"
    edf = mne.io.read_raw_edf(edf_filepath)
    header = ','.join(edf.ch_names)
    np.savetxt(csv_filepath, edf.get_data().T, delimiter=',', header=header)

def edf4csv_folder(edf_folderpath):
    edf_files = []
    for root, dirs, files in os.walk(edf_folderpath):
        for file in files:
            if file.endswith(".edf"):
                edf_files.append(os.path.join(root, file))
    for file_path in edf_files:
        csv_filepath = os.path.splitext(file_path)[0] + ".csv"
        edf = mne.io.read_raw_edf(file_path)
        header = ','.join(edf.ch_names)
        np.savetxt(csv_filepath, edf.get_data().T, delimiter=',', header=header)
