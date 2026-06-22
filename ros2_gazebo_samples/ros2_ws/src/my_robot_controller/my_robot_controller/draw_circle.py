import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DrawCircleNode(Node):
    def __init__(self):
        super().__init__('draw_circle_node')
        self.get_logger().info('DrawCircleNode has been started.')
        self.command_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(1.0, self.send_velocity_command)

    def send_velocity_command(self):
        msg = Twist()
        msg.linear.x = 2.0 
        msg.angular.z = 1.0
        self.command_publisher.publish(msg)
        self.get_logger().info('Published velocity command to draw a circle.')  

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f'Hello, ROS 2! Counter: {self.counter}')

def main(args=None):
    rclpy.init(args=args)
    node = DrawCircleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    