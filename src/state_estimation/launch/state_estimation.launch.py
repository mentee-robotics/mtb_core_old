from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():
    package_name = 'state_estimation'
    
    launch_me = LaunchDescription()

    namespace = DeclareLaunchArgument('namespace', default_value='')

    use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='false')

    odom_base_link_params = DeclareLaunchArgument('odom_base_link_params', 
                                                  default_value=os.path.join(get_package_share_directory(package_name), 'config', 'odom_base_link_ekf.yaml')
    )

    map_odom_params = DeclareLaunchArgument('map_odom_params', 
                                            default_value=os.path.join(get_package_share_directory(package_name), 'config', 'map_odom_ekf.yaml')
    )
    

    robot_localization_odom_base_link = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_odom_base_link',
        namespace=LaunchConfiguration('namespace'),
        output='screen',
        parameters=[LaunchConfiguration('odom_base_link_params'),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    robot_localization_map_odom = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_map_odom',
        namespace=LaunchConfiguration('namespace'),
        output='screen',
        parameters=[LaunchConfiguration('map_odom_params'),
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[('odometry/filtered', 'odometry/filtered_map'),
                    ('accel/filtered', 'accel/filtered_map')
        ]
    )

    launch_me.add_action(namespace)
    launch_me.add_action(use_sim_time)
    launch_me.add_action(odom_base_link_params)
    launch_me.add_action(map_odom_params)
    launch_me.add_action(robot_localization_odom_base_link)
    launch_me.add_action(robot_localization_map_odom)

    return launch_me