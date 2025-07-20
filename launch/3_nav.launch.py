import os
from launch import LaunchDescription
from launch_ros.actions import Node

nav2_mr_sim_dir = os.environ.get('NAV2_MR_SIM_DIR')
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'yaml_filename': f'{nav2_mr_sim_dir}/map/turtlebot3_world_map/map.yaml'},
                {'use_sim_time': True}
            ]
        ),
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[
                f'{nav2_mr_sim_dir}/configs/nav2_params.yaml',
                {'use_sim_time': True}
            ]
        ),

        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[
                f'{nav2_mr_sim_dir}/configs/nav2_params.yaml',
                {'default_bt_xml_filename': f'{nav2_mr_sim_dir}/configs/simp_bt.xml'}
            ],
            env={'RCL_LOG_LEVEL': 'debug'}  # Set log level to debug for detailed output
        ),

        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[f'{nav2_mr_sim_dir}/configs/nav2_params.yaml']
        ),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[f'{nav2_mr_sim_dir}/configs/nav2_params.yaml']
        ),

        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[f'{nav2_mr_sim_dir}/configs/nav2_params.yaml']
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'autostart': True},
                {'node_names': [
                    'map_server',
                    'amcl',
                    'planner_server',
                    'controller_server',
                    'recoveries_server',
                    'bt_navigator'
                ]}
            ]
        ),
    ])
