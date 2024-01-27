import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import numpy as np
import matplotlib.pyplot as plt
from visualization_msgs.msg import MarkerArray, Marker
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose
# wave, goal , my, thruster l,r,lv,rv
def euler_from_quaternion(quaternion):                                                                   
        """クオータニオンからオイラー角を計算する関数                                                        
        Converts quaternion (w in last place) to euler roll, pitch, yaw                                           
        quaternion = [x, y, z, w]                                                                                 
        Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.                           
        """                                                                                                      
        x = quaternion.x                                                                                          
        y = quaternion.y                                                                                          
        z = quaternion.z                                                                                          
        w = quaternion.w                                                                                          
                                                                                                                  
        sinr_cosp = 2 * (w * x + y * z)                                                                           
        cosr_cosp = 1 - 2 * (x * x + y * y)                                                                       
        roll      = np.arctan2(sinr_cosp, cosr_cosp)                                                              
                                                                                                                  
        sinp  = 2 * (w * y - z * x)                                                                               
        pitch = np.arcsin(sinp)                                                                                   
                                                                                                                  
        siny_cosp = 2 * (w * z + x * y)                                                                           
        cosy_cosp = 1 - 2 * (y * y + z * z)                                                                       
        yaw = np.arctan2(siny_cosp, cosy_cosp)                                                                    
                                         
        return roll, pitch, yaw

#座標を受け取って描画するだけの関数
def rviz_marker(self, position: np.ndarray, label: str, idx: int, goal_index: int):
    marker_child = Marker()
    marker_child.header.frame_id = "wamv/wamv/base_link/front_left_camera_sensor"
    marker_child.header.stamp = self.get_clock().now().to_msg()
    marker_child.ns = label
    marker_child.id = idx
    marker_child.type = Marker.SPHERE
    marker_child.action = Marker.ADD
        
    marker_child.pose.position.x = position[0]
    marker_child.pose.position.y = position[1]
    marker_child.scale.x = marker_child.scale.y = marker_child.scale.z = 1.0
    if(idx == goal_index): #ゴールの色は赤色
        marker_child.color.r = 1.0
        marker_child.color.g = 0.0
        marker_child.color.b = 0.0
        marker_child.color.a = 1.0
    elif(idx == goal_index+1): #ゴールの色は赤色
        marker_child.color.r = 1.0
        marker_child.color.g = 1.0
        marker_child.color.b = 0.0
        marker_child.color.a = 1.0
    elif(idx == goal_index-1): #スタートの色は青色
        marker_child.color.r = 0.0
        marker_child.color.g = 0.0
        marker_child.color.b = 1.0
        marker_child.color.a = 1.0
    else: #他のマーカは黄色
        marker_child.color.r = 0.0
        marker_child.color.g = 1.0
        marker_child.color.b = 1.0
        marker_child.color.a = 1.0
    
    if(idx == 100):
        marker_child.type = Marker.MESH_RESOURCE
        marker_child.mesh_resource = "file:///home/gaia-22/ac_search/vrx_ws/src/navigaitonGUI/mesh/WAM-V-Base.dae"
        marker_child.mesh_use_embedded_materials = True

    return marker_child

class expertGUI(Node):
    def __init__(self):
        super().__init__('expert_gui_node')

        self.myPos = [0.0]*2 #自分の位置を保存
        self.myAng = 0.0 #自分の角度を保存
        self.myAngOri = [0.0]*4 #自分の四元角度を保存

        self.passing_point_num = 50 #用意する通過地点の数
        self.episode_point_num = self.passing_point_num-10 #エピソードの通過地点の数
        #通過地点の座標
        self.passing_point = np.zeros((self.passing_point_num, 2))
        #目指す通過地点のインデックス
        self.nextPointIndex = 0
        preAng = 0.0
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = preAng + np.random.rand()*180.0-90.0
            preAng = angle
            #ポイントの中身を更新(i=0の時は船の現在地からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = self.myPos[0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.myPos[1] + distance*np.cos(np.radians(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.cos(np.radians(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))

        # エピソードの開始を受け取るコールバック関数(=reset関数)
        self.done_sub = self.create_subscription(
            Bool,
            '/vrx/reset',
            self.reset_callback,
            10
        )
        # エピソードの終了をパブリッシュするためのパブリッシャ
        self.done_pub = self.create_publisher(
            Bool,
            "/vrx/done",
            10
        )
        # マーカーをパブリッシュするためのパブリッシャ
        self.marker_pub = self.create_publisher(
            MarkerArray,
            "/vrx/markers",
            10
        )
        # index番号をパブリッシュするためのパブリッシャ
        self.index_pub = self.create_publisher(
            Int32,
            "/vrx/index",
            10
        )
        # poseデータをパブリッシュするためのパブリッシャ
        self.pose_pub = self.create_publisher(
            PoseArray,
            "/vrx/pose",
            10
        )
        # imuデータをサブスクライブするためのサブスクライバ
        self.collect_imu_sub = self.create_subscription(
            Imu,
            '/world/sydney_regatta/model/wamv/link/wamv/imu_wamv_link/sensor/imu_wamv_sensor/imu',
            self.imu_data_callback,
            10
        )
        # poseデータをサブスクライブするためのサブスクライバ
        #船の現在地を計算するために使用
        self.collect_Pose_sub = self.create_subscription(
             PoseArray,
             '/world/sydney_regatta/dynamic_pose/info',
             self.pose_data_callback,
             10
        )
        
    def imu_data_callback(self,msg):
        self.myAngOri[0] = msg.orientation.x
        self.myAngOri[1] = msg.orientation.y
        self.myAngOri[2] = msg.orientation.z
        self.myAngOri[3] = msg.orientation.w
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]

    def pose_data_callback(self, msg):
        self.myPos[0] = msg.poses[1].position.x
        self.myPos[1] = msg.poses[1].position.y
        markers = MarkerArray() #すべてのマーカーをエキスパートに表示するための変数
        poses = PoseArray() #すべてのポイントの位置と船体位置をパブリッシュするための変数

        #船体の位置をパブリッシュ
        pose = Pose()
        pose.position.x = self.myPos[0]
        pose.position.y = self.myPos[1]
        myPos0 = [0.0]*2
        poses.poses.append(pose) #船体の位置をアペンド
        markers.markers.append(rviz_marker(self, myPos0, "wam_v", 100, self.nextPointIndex)) #船の位置をマーカーとして追加

        #通過地点をパブリッシュし、マーカーとして追加
        for i in range(self.passing_point_num):
            pose = Pose()
            pose.position.x = self.passing_point[i][0]
            pose.position.y = self.passing_point[i][1]
            poses.poses.append(pose) #通過地点をアペンド
            relativePos = [0.0]*2
            relativePos[0] = self.passing_point[i][0] - self.myPos[0]
            relativePos[1] = self.passing_point[i][1] - self.myPos[1]
            relativeVector = [0.0]*2
            distance = np.linalg.norm(relativePos)
            radian = math.atan2(relativePos[1], relativePos[0])
            angle = radian - self.myAng
            relativeVector[0] = np.cos(angle)*distance
            relativeVector[1] = np.sin(angle)*distance

            markers.markers.append(rviz_marker(self, relativeVector, "buoy", i, self.nextPointIndex)) #船体を固定したときの相対通過地点をマーカーとして追加
        
        #次の通過地点に到達しているかの判定
        goal_dis = [0.0]*2
        goal_dis[0] = np.abs(self.myPos[0]-self.passing_point[self.nextPointIndex][0])
        goal_dis[1] = np.abs(self.myPos[1]-self.passing_point[self.nextPointIndex][1])
        if(np.linalg.norm(goal_dis) < 3.0):
            if(self.nextPointIndex == self.episode_point_num):
                self.nextPointIndex = 0
                done = Bool()
                done.data = True
                self.done_pub.publish(done)
            else:
                self.nextPointIndex += 1
        index = Int32()
        index.data = self.nextPointIndex

        # index番号をパブリッシュ
        self.index_pub.publish(index)
        #すべてのポイントと船体位置をパブリッシュ
        self.pose_pub.publish(poses)
        #すべてのマーカーをパブリッシュ
        self.marker_pub.publish(markers)

    #エピソードの開始を受け取ったときに呼び出される関数
    def reset_callback(self, msg):
        self.nextPointIndex = 0
        preAng = np.degrees(self.myAng)
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = preAng + np.random.rand()*180.0-90.0
            preAng = angle
            #ポイントの中身を更新(i=0の時は船の現在地からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = self.myPos[0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.myPos[1] + distance*np.cos(np.radians(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.cos(np.radians(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))


def main(args=None):
    rclpy.init(args=args)
    expert_gui_node = expertGUI()
    rclpy.spin(expert_gui_node)
    expert_gui_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

                
        