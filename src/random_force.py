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

def calculate_combined_force(current_speed, current_angle_degrees):
    current_vector = np.array([current_speed * np.cos(np.radians(current_angle_degrees)),
                               current_speed * np.sin(np.radians(current_angle_degrees))])
    random_speed = np.random.uniform(0, 10)
    random_angle_degrees = np.random.uniform(0, 360)
    random_vector = np.array([random_speed * np.cos(np.radians(random_angle_degrees)),
                              random_speed * np.sin(np.radians(random_angle_degrees))])
    combined_vector = current_vector + random_vector
    return combined_vector

# 船の数を指定
num_ships = 5  # 例として5隻の船を指定

# 各船の初期位置をランダムに生成
initial_positions = np.random.rand(num_ships, 2) * 20 - 10  # -10から10の範囲でランダムな座標を生成
ships = [MovingPoint(x, y) for x, y in initial_positions]

# 軌跡の座標を保存するリスト（各船ごとにリストを用意）
trajectory_x = [[] for _ in range(num_ships)]
trajectory_y = [[] for _ in range(num_ships)]

# 各船ごとに速度と角速度のリストを用意
velocities = [[] for _ in range(num_ships)]
angular_velocities = [[] for _ in range(num_ships)]

# 時間ごとに更新
for _ in range(10):
    for i in range(num_ships):
        ships[i].update_position(5)
        result = calculate_combined_force(ships[i].get_speed(), ships[i].get_angular_velocity())
        ships[i].set_speed(np.linalg.norm(result))
        ships[i].set_angular_velocity(np.degrees(np.arctan2(result[1], result[0])))
        trajectory_x[i].append(ships[i].x)
        trajectory_y[i].append(ships[i].y)
        velocities[i].append(ships[i].speed)
        angular_velocities[i].append(ships[i].angular_velocity)
    time.sleep(1)

# 軌跡をプロット
for i in range(num_ships):
    plt.plot(trajectory_x[i], trajectory_y[i], marker='o', label=f'Ship {i+1}')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Trajectory of Multiple Ships with Random Force')
plt.legend()
plt.grid(True)
plt.show()