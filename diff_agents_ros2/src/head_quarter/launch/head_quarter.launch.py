from launch import LaunchDescription
from launch_ros.actions import Node
import os
import launch_ros.parameter_descriptions
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    params_dir = LaunchConfiguration(
        'params_dir',
        default=os.path.join(
            get_package_share_directory('head_quarter'),
            'config',
            'params.yaml',
        )
    )

    return LaunchDescription([
        Node(
            package='head_quarter',
            executable='head_quarter',
            parameters=[params_dir]
        )
    ])