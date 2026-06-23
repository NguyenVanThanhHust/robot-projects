import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

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

        if pose_msg.x > 5.0:
            self.call_set_pen_service(0, 0, 255, 3, 0)
        elif pose_msg.x < 2.0:
            self.call_set_pen_service(255, 0, 0, 3, 0)
        elif pose_msg.y > 5.0:
            self.call_set_pen_service(0, 255, 0, 3, 0)
        elif pose_msg.y < 2.0:
            self.call_set_pen_service(0, 0, 255, 3, 0) 
        else:
            self.call_set_pen_service(0, 255, 255, 3, 0) 

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, '/turtle1/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
        future = client.call_async(request)
        future.add_done_callback(self.callback_set_pen)
    
    def callback_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'service callback failed with exception: {e}')
            return
        self.get_logger().info(f'Set pen response: {response}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':    
    main()