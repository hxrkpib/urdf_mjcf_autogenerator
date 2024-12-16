from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 获取包的共享目录
    package_share_directory = get_package_share_directory('model_generator')

    # 定义机器人描述内容
    robot_description_content = '<robot name="empty"><link name="base_link"></link></robot>'

    # 定义RViz配置文件的路径
    rviz_config_file = os.path.join(
        package_share_directory, 'rviz', 'default.rviz')

    return LaunchDescription([
        # 声明 'data_path' 启动参数
        DeclareLaunchArgument(
            'data_path',
            default_value='',  # 设置默认值为空字符串
            description='Path to the data directory'
        ),

        # 声明 'param_file' 启动参数，并使用 PathJoinSubstitution 拼接路径
        DeclareLaunchArgument(
            'param_file',
            default_value=PathJoinSubstitution([
                LaunchConfiguration('data_path'),
                'config',
                'zeros.yaml'
            ]),
            description='Path to the parameter YAML file'
        ),

        # 启动 'model_generator' 节点
        Node(
            package='model_generator',
            executable='model_generator',
            name='model_generator',
            output='screen',
            parameters=[{'data_path': LaunchConfiguration('data_path')}],
        ),

        # 启动 'robot_state_publisher' 节点
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),

        # 启动 'joint_state_publisher_gui' 节点，并加载参数文件
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            parameters=[
                {'rate': 200},  # 直接在参数列表中设置 'rate'
                LaunchConfiguration('param_file')  # 加载参数文件
            ],
        ),

        # 启动 RViz2 节点，并加载配置文件（如果存在）
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=[
                '-d', rviz_config_file
            ] if os.path.exists(rviz_config_file) else []
        )
    ])
