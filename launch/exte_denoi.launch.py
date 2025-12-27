import launch
import launch_ros.actions

def generate_launch_description():
    exte_img = launch_ros.actions.Node(
        package='img_pkg',
        executable='exte_img',
        output='screen',
        parameters=[{
            'image_path': '/home/akira/ros2_ws/src/img_pkg/picture/image_01.jpg',
            'fps': 5,
            'width': 640,
            'height': 480,
        }],
    )

    denoi_img = launch_ros.actions.Node(
        package='img_pkg',
        executable='denoi_img',
        output='screen',
    )

    return launch.LaunchDescription([exte_img, denoi_img])
