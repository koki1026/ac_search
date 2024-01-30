import math
import numpy as np
import time
import matplotlib.pyplot as plt

class MovingPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.speed = 0
        self.angular_velocity = 0

    def update_position(self, time_interval):
        delta_x = self.speed * math.cos(math.radians(self.angular_velocity)) * time_interval
        delta_y = self.speed * math.sin(math.radians(self.angular_velocity)) * time_interval
        self.x += delta_x
        self.y += delta_y

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity

    def get_angular_velocity(self):
        return self.angular_velocity

def calculate_navigation_force(current_position, target_position):
    direction_vector = np.array([target_position[0] - current_position[0],
                                 target_position[1] - current_position[1]])
    normalized_direction = direction_vector / np.linalg.norm(direction_vector)
    navigation_force = normalized_direction * 5  # 例として力の大きさを5に設定
    return navigation_force

def calculate_boundary_repulsion(current_position, area_size, repulsion_distance=5):
    repulsion_force = np.zeros(2)

    # エリアの端に近づいた場合、斥力をかける
    if current_position[0] < repulsion_distance:
        repulsion_force[0] += 1 / (current_position[0] + 1e-5)
    elif current_position[0] > area_size - repulsion_distance:
        repulsion_force[0] -= 1 / (area_size - current_position[0] + 1e-5)

    if current_position[1] < repulsion_distance:
        repulsion_force[1] += 1 / (current_position[1] + 1e-5)
    elif current_position[1] > area_size - repulsion_distance:
        repulsion_force[1] -= 1 / (area_size - current_position[1] + 1e-5)

    return repulsion_force

# 船の数を指定
num_ships = 3

# 船の初期位置をランダムに生成
initial_positions = np.random.rand(num_ships, 2) * 20  # 0から20の範囲でランダムな座標を生成
ships = [MovingPoint(x, y) for x, y in initial_positions]

# エリアのサイズを指定
area_size = 1000

# 目標地点を各船ごとにランダムに生成
target_positions = np.random.rand(num_ships, 2) * (area_size*0.8) + (area_size*0.1)  # エリアの64%以内にそれぞれの船の目標地点を生成

# 軌跡の座標を保存するリスト（各船ごとにリストを用意）
trajectory_x = [[] for _ in range(num_ships)]
trajectory_y = [[] for _ in range(num_ships)]

# 各船ごとに速度と角速度のリストを用意
velocities = [[] for _ in range(num_ships)]
angular_velocities = [[] for _ in range(num_ships)]

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

        # 船の速度と角速度を更新
        ships[i].set_speed(np.linalg.norm(total_force))
        ships[i].set_angular_velocity(np.degrees(np.arctan2(total_force[1], total_force[0])))

        # 船の位置を更新
        ships[i].update_position(6)  # 6秒ごとに更新

        # 目標地点に到達したら新しいランダムな目標地点を設定
        if np.linalg.norm([ships[i].x - target_positions[i, 0], ships[i].y - target_positions[i, 1]]) < 5:
            target_positions[i] = np.random.rand(2) * (area_size*0.8) + (area_size*0.1)

        # データを保存
        trajectory_x[i].append(ships[i].x)
        trajectory_y[i].append(ships[i].y)
        velocities[i].append(ships[i].speed)
        angular_velocities[i].append(ships[i].angular_velocity)

# 軌跡をプロット
for i in range(num_ships):
    plt.plot(trajectory_x[i], trajectory_y[i], marker='o', label=f'Ship {i+1}')

# 目標地点をプロット
for i in range(num_ships):
    plt.plot(target_positions[i, 0], target_positions[i, 1], marker='x', markersize=10, color='red', label=f'Target {i+1}')

# エリアの境界を描画
plt.plot([0, area_size, area_size, 0, 0], [0, 0, area_size, area_size, 0], color='black', linestyle='--', label='Area Boundary')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Trajectory with Navigation Task and Boundary Repulsion')
plt.legend()
plt.grid(True)
plt.show()
