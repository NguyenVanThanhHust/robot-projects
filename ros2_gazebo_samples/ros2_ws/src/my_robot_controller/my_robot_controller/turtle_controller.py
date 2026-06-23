import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.get_logger().info('TurtleControllerNode has been started.')
        self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # self.timer = self.create_timer(1.0, self.timer_callback)
    def pose_callback(self, pose_msg: Pose):
        cmd = Twist()
        if pose_msg.x > 9.0 or pose_msg.x < 2.0 or pose_msg.y > 9.0 or pose_msg.y < 2.0:
            cmd.linear.x = 0.5
            cmd.angular.z = 0.5
        else:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
        self.get_logger().info(f'Published velocity command to move the turtle.')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':    
    main()