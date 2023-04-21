import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from std_msgs.msg import Float32MultiArray
from math import *
import numpy as np

class MinimalSubscriber(Node):
	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription( Float32MultiArray, 'topic', self.listener_callback, 10)
		self.subscription  
		self.subscription2 = self.create_subscription(Pose,'topic1',self.return_inverse,10)
		self.subscription2

	def listener_callback(self, msg):
		quat1,quat2,quat3 = msg.data
		A1 = np.mat([[cos(quat1),0,-sin(quat1),0],[sin(quat1),0,cos(quat1),0],[0,-1,0,1],[0,0,0,1]])
		A2 = np.mat([[cos(quat2),-sin(quat2),0,cos(quat2)],[sin(quat2),cos(quat2),0,sin(quat2)],[0,0,1,0],[0,0,0,1]])
		A3 = np.mat([[cos(quat3),-sin(quat3),0,cos(quat3)],[sin(quat3),cos(quat3),0,sin(quat3)],[0,0,1,0],[0,0,0,1]])
		H = A1*A2*A3
		self.get_logger().info('The resulting pose is \n{}'.format(H))
		
	def return_inverse(self,msg2):
		end_x = msg2.position.x
		end_y = msg2.position.y
		end_z = msg2.position.z
		link1 = 1
		link2 = 1
		link3 = 1
		r = sqrt(end_x**2+ end_y**2)
		s = end_z - link1
		D = (r**2+s**2-link2**2-link3**2)/(2*link2*link3)
		quat1 = atan2(end_y,end_x)
		quat3 = -atan2(-sqrt(1-D**2),D)
		quat2 = -atan2(s,r) - atan2(link3*sin(quat3),link2+link3*cos(quat3))
		self.get_logger().info('The resulting joint angles are:\nq1:{}\nq2:{}\nq3:{}'.format(quat1,quat2,quat3))
		
def main(args=None):
	rclpy.init(args=args)

	minimal_subscriber = MinimalSubscriber()

	rclpy.spin(minimal_subscriber)

	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	minimal_subscriber.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()
