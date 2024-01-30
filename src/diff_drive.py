import math
import numpy as np
import time
import matplotlib.pyplot as plt

class MovingPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.speed = 0
        self.heading = 0  # 船体角（ラジアン）
        self.max_angular_velocity = np.radians(10)  # 最大角速度を1秒あたり10度に設定
        self.angular_velocity = 0

    def update_position(self, time_interval):
        delta_x = self.speed * math.cos(self.heading) * time_interval
        delta_y = self.speed * math.sin(self.heading) * time_interval
        self.x += delta_x
        self.y += delta_y

    def set_speed(self, speed):
        self.speed = speed

    def set_target_heading(self, target_heading):
        # 最大角速度で目標船体角に向かうように制御
        delta_heading = target_heading - self.heading
        delta_heading = np.arctan2(np.sin(delta_heading), np.cos(delta_heading))  # 角度の差を[-π, π]に調整
        sign = np.sign(delta_heading)
        self.angular_velocity = sign * min(self.max_angular_velocity, abs(delta_heading))

    def get_speed(self):
        return self.speed

    def get_heading(self):
        return self.heading

# ... 以前の関数や変数の定義

# 目標船体角を指定
target_heading = np.radians(45)  # 例として45度に設定

# 時間ごとに更新
for _ in range(600):  # 600回(計一時間)の更新サイクル
    for i in range(num_ships):
        # 航行タスクの力を計算
        navigation_force = calculate_navigation_force([ships[i].x, ships[i].y], target_positions[i])

        # エリアの端に対する斥力を計算
        boundary_repulsion = calculate_boundary_repulsion([ships[i].x, ships[i].y], area_size)

        # ランダムな力を計算
        random_force = np.random.uniform(-2, 2, size=2)  # 例として(-2, 2)の範囲でランダムな力を生成

        # 合力を計算
        total_force = navigation_force + random_force + boundary_repulsion

        # 船の速度を更新
        ships[i].set_speed(np.linalg.norm(total_force))

        # 船の船体角を更新
        ships[i].set_target_heading(target_heading)

        # 船の位置を更新
        ships[i].update_position(6)  # 6秒ごとに更新

        # カバレッジマップを更新
        update_coverage_map(coverage_map, [ships[i].x, ships[i].y], area_size)

        # 目標地点に到達したら新しいランダムな目標地点を設定
        if np.linalg.norm([ships[i].x - target_positions[i, 0], ships[i].y - target_positions[i, 1]]) < 5:
            target_positions[i] = np.random.rand(2) * (area_size*0.8) + (area_size*0.1)

        # データを保存
        trajectory_x[i].append(ships[i].x)
        trajectory_y[i].append(ships[i].y)
        velocities[i].append(ships[i].speed)
        angular_velocities[i].append(ships[i].angular_velocity)

# カバレッジ率を計算
coverage_rate = calculate_coverage_rate(coverage_map)
print(f"Coverage Rate: {coverage_rate * 100:.2f}%")

# ... 以前のプロット部分
