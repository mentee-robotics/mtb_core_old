from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os
from launch.conditions import LaunchConfigurationEquals
from launch.actions import DeclareLaunchArgument
from ament_index_python import get_package_share_directory

def generate_launch_description():
    
    package_name = 'state_publisher'

    launch_me = LaunchDescription()

    namespace = DeclareLaunchArgument("namespace", default_value='')
        
    publish_frequency = DeclareLaunchArgument("publish_frequency", default_value='50.0')
    
    pkg_share = launch_ros.substitutions.FindPackageShare(package='state_publisher').find('state_publisher')

    urdf_file = DeclareLaunchArgument("urdf_file", default_value=[pkg_share, '/description/urdf/', 'happy.urdf'],
                                    description='Absolute path to robot urdf file')
    
    joints_pub_rate = DeclareLaunchArgument("joints_pub_rate", default_value='10',
                                 description='The rate at which to publish updates to the /joint_states topic. Defaults to 10 [Hz]'
    )   
    
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='state_publisher',
        namespace=LaunchConfiguration('namespace'),
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('urdf_file')]),
            'publish_frequency': LaunchConfiguration('publish_frequency'),
            'use_tf_static':False, 
            'ignore_timestamp':False
        }]
    )

    launch_me.add_action(namespace)
    launch_me.add_action(urdf_file)
    launch_me.add_action(publish_frequency)
    launch_me.add_action(joints_pub_rate)
    launch_me.add_action(robot_state_publisher_node)
    
    return launch_me