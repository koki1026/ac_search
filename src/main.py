import time
import numpy as np
import keyboard

def calculate_combined_force(current_speed, current_angle_degrees):
    # 現在の速度と角度からベクトルを作成
    current_vector = np.array([current_speed * np.cos(np.radians(current_angle_degrees)),
                               current_speed * np.sin(np.radians(current_angle_degrees))])

    # ランダムな速度と角度を生成
    random_speed = np.random.uniform(0, 10)  # 0から10までのランダムな速度を生成
    random_angle_degrees = np.random.uniform(0, 360)  # 0から360までのランダムな角度を生成

    # ランダムな速度と角度からベクトルを作成
    random_vector = np.array([random_speed * np.cos(np.radians(random_angle_degrees)),
                              random_speed * np.sin(np.radians(random_angle_degrees))])

    # 合成ベクトルを計算（ベクトルの合計）
    combined_vector = current_vector + random_vector

    return combined_vector

# 現在の速度と角度（例：速度5、角度30度）
current_speed = 5
current_angle_degrees = 30

while True:
    # 関数を呼び出して合力を計算
    result = calculate_combined_force(current_speed, current_angle_degrees)
    # 合力の大きさを計算
    result_speed = np.linalg.norm(result)

    # 結果を表示
    print(f"現在の速度: {current_speed}")
    print(f"現在の角度: {current_angle_degrees} 度")
    print(f"合力: {result}")

    #現在値を更新
    current_speed = result_speed
    current_angle_degrees = np.degrees(np.arctan2(result[1], result[0]))

    # 1秒待機
    time.sleep(1)

    if keyboard.is_pressed('q'):
        print("終了キーが入力されたのでプログラムを終了します")
        break
