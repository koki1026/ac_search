import launch
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
  packages_dir = get_package_share_directory("diff_agent")
  urdf = os.path.join(packages_dir, "robot.urdf")
  pkg_head_quarter = get_package_share_directory("head_quarter")

  head_quarter = launch.actions.IncludeLaunchDescription(
    PythonLaunchDescriptionSource([pkg_head_quarter + "/head_quarter.launch.py"]),
  )

  return launch.LaunchDescription([
    head_quarter,

    Node(
      package="rviz2",
      executable="rviz2",
      name="rviz2"),

    Node(
      package='joint_state_publisher',
      executable='joint_state_publisher',
      name='joint_state_publisher',
      arguments=[urdf]),

    Node(
      package='robot_state_publisher',
      executable='robot_state_publisher',
      name='robot_state_publisher',
      arguments=[urdf]),

    Node(
      package="ros_gz_bridge",
      executable="parameter_bridge",
      arguments=[
        '/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
        '/agent_command_topic@geometry_msgs/msg/Twist@gz.msgs.Twist',
      ],
    )

  ])
