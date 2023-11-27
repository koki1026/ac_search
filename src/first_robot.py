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
        # 速度と角速度から新しい座標を計算
        delta_x = self.speed * math.cos(math.radians(self.angular_velocity)) * time_interval
        delta_y = self.speed * math.sin(math.radians(self.angular_velocity)) * time_interval

        # 新しい座標に移動
        self.x += delta_x
        self.y += delta_y

    def set_speed(self, speed):
        self.speed = speed

    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity

# 使用例
point = MovingPoint()

# 速度と角速度を設定
point.set_speed(5)
point.set_angular_velocity(45)
# 軌跡の座標を保存するリスト
trajectory_x = []
trajectory_y = []
velocities = []  # 速度のリスト
angular_velocities = []  # 角速度のリスト

# 時間ごとに更新
for _ in range(10):
    point.update_position(5)  # 1秒ごとに更新
    point.set_speed(np.random.uniform(0, 10))
    point.set_angular_velocity(np.random.uniform(0, 360))
    print(f"Current Position: ({point.x}, {point.y})")
    trajectory_x.append(point.x)
    trajectory_y.append(point.y)
    velocities.append(point.speed)
    angular_velocities.append(point.angular_velocity)
    time.sleep(1)

# 軌跡をプロット
plt.plot(trajectory_x, trajectory_y, marker='o', label='Moving Point')

# 各点での速度と角速度のベクトルを矢印でプロット
for i in range(len(trajectory_x)):
    plt.arrow(
        trajectory_x[i], trajectory_y[i],
        velocities[i] * math.cos(math.radians(angular_velocities[i])),
        velocities[i] * math.sin(math.radians(angular_velocities[i])),
        head_width=0.5, head_length=0.5, fc='red', ec='red'
    )

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Trajectory of Radom Moving Point')
plt.legend()
plt.grid(True)
plt.show()