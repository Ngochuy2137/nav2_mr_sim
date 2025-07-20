import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

nav2_mr_sim_dir = os.environ.get('NAV2_MR_SIM_DIR')

def generate_launch_description():
    # File paths
    
    urdf_file_path = f'{nav2_mr_sim_dir}/urdf/diff_robot.urdf'
    rviz_config_file_path = f'{nav2_mr_sim_dir}/urdf/rviz.rviz'
    # world_file_path = f'{nav2_mr_sim_dir}/worlds/monza_track.world'
    world_file_path = f'{nav2_mr_sim_dir}/worlds/turtlebot3_world.world'
    controller_config_file_path = f'{nav2_mr_sim_dir}/configs/diff_drive_controller.yaml'
    map_file = f'{nav2_mr_sim_dir}/src/my_map.yaml'

    # Load robot description from URDF file
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument(
            name='model',
            default_value=urdf_file_path,
            description='Absolute path to robot URDF file'),
        DeclareLaunchArgument(
            name='rvizconfig',
            default_value=rviz_config_file_path,
            description='Absolute path to RViz config file'),
        DeclareLaunchArgument(
            name='world',
            default_value=world_file_path,
            description='Absolute path to world file'),
        DeclareLaunchArgument(
            name='x', default_value='-0.142601', description='Initial x position of the robot'),
        DeclareLaunchArgument(
            name='y', default_value='-2.065040', description='Initial y position of the robot'),
        DeclareLaunchArgument(
            name='z', default_value='0.150008', description='Initial z position of the robot'),
        DeclareLaunchArgument(
            name='R', default_value='-0.000005', description='Initial roll orientation of the robot'),
        DeclareLaunchArgument(
            name='P', default_value='0.000040', description='Initial pitch orientation of the robot'),
        DeclareLaunchArgument(
            name='Y', default_value='-0.062120', description='Initial yaw orientation of the robot'),

        # Gazebo launch
        # ExecuteProcess(
        #     cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', LaunchConfiguration('world')],
        #     output='screen'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('gazebo_ros'),
                    'launch',
                    'gazebo.launch.py'
                )
            ),
            launch_arguments={'world': world_file_path}.items()
        ),


        # Spawn the robot in Gazebo
        Node(package='gazebo_ros', executable='spawn_entity.py',
             arguments=[
                 '-file', LaunchConfiguration('model'),
                 '-entity', 'nav2_mr_sim',
                 '-x', LaunchConfiguration('x'),
                 '-y', LaunchConfiguration('y'),
                 '-z', LaunchConfiguration('z'),
                 '-R', LaunchConfiguration('R'),
                 '-P', LaunchConfiguration('P'),
                 '-Y', LaunchConfiguration('Y')],
             output='screen'),

        # Publish the robot state (robot_description topic)
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen',
             parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
             remappings=[("/diff_drive_controller/cmd_vel_unstamped", "/cmd_vel")]),
            
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_lidar',
            arguments=['0', '0', '0.15', '0', '0', '0', 'base_link', 'base_scan'],
            output='screen'
        ),


        # Start the controller manager and load controller configurations
        Node(package='controller_manager', executable='ros2_control_node',
             output='screen',
             parameters=[
                 {'use_sim_time': True},  # Use simulation time
                 {'robot_description': robot_desc},  # Robot description from robot_state_publisher
                 controller_config_file_path  # Path to controller YAML
             ]),

        # Launch RViz
        Node(package='rviz2', executable='rviz2',
             name='rviz2',
             output='screen',
             arguments=['-d', LaunchConfiguration('rvizconfig')]),
    ])
