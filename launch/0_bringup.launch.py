import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

nav2_mr_sim_dir = os.environ.get('NAV2_MR_SIM_DIR')

def generate_launch_description():
    return LaunchDescription([
        # 1. Gazebo: world + robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_mr_sim_dir, 'launch', '1_gazebo.launch.py')
            )
        ),

        # 2. SLAM: slam_toolbox
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_mr_sim_dir, 'launch', '2_slam.launch.py')
            )
        ),
    ])
        