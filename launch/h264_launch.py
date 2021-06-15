"""
h264 test
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    camera_name = 'my_camera'
    config_dir = os.path.join(get_package_share_directory('gscam2'), 'cfg')
    camera_config = 'file://' + os.path.join(config_dir, 'my_camera.ini')

    return LaunchDescription([
        Node(
            package='gscam2',
            executable='gscam_main',
            output='screen',
            name='gscam_main',
            namespace=camera_name,
            parameters=[{
                'gscam_config': 'udpsrc port=5602 ! queue ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer ! rtph264depay ! h264parse config-interval=-1 ! capsfilter caps="video/x-h264,stream-format=byte-stream,alignment=au"',
                'sync_sink': False,
                'image_encoding': 'h264',
                'camera_info_url': camera_config,
                'camera_name': camera_name,
            }],
            remappings=[
                ('/image_raw', '/' + camera_name + '/image_raw'),
                ('/camera_info', '/' + camera_name + '/camera_info'),
            ],
        ),

        Node(
            package='image_transport',
            executable='republish',
            output='screen',
            name='republish_node',
            namespace=camera_name,
            arguments=[
                'h264',  # Input
                'raw',  # Output
            ], remappings=[
                ('in', 'image_raw'),
                ('in/compressed', 'image_raw/compressed'),
                ('in/theora', 'image_raw/theora'),
                ('in/h264', 'image_raw/h264'),
                ('out', 'repub_raw'),
                ('out/compressed', 'repub_raw/compressed'),
                ('out/theora', 'repub_raw/theora'),
                ('out/theora', 'repub_raw/h264'),
            ],
        ),
    ])
