import os
from launch import LaunchDescription
from launch_ros.actions import Node

nav2_mr_sim_dir = os.environ.get('NAV2_MR_SIM_DIR')
def generate_launch_description():
    slam_params_file_path = f'{nav2_mr_sim_dir}/configs/slam_params.yaml'

    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_params_file_path, {'use_sim_time': True}],
            # remappings=[
            #     ('/map', '/map'),
            #     ('/initialpose', '/initialpose'),
            #     ('/amcl_pose', '/amcl_pose')
            # ]
        ),
    ])
