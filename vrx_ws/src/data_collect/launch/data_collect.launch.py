import os
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    params_dir = LaunchConfiguration(
        'params_dir',
        default=os.path.join(
            get_package_share_directory('data_collect'),
                'config',
                'waveData.yaml')
    )
    
    return LaunchDescription([
        launch_ros.actions.Node(
            package='data_collect',
            executable='data_collect_node',
            parameters=[params_dir]
        )
    ])