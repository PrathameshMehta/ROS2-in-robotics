#import all the dependencies required to run the node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import numpy as np
from math import *

#initilize the robot_fk class by inheriting the Node class from rclpy.node
class robot_fk(Node):
	#define the constructor for the class
	def __init__(self):
		#call the parent node constructor and give the name to the node
		super().__init__('robot_fk')
		#create subscriber
		self.publisher_ = self.create_publisher(Float64MultiArray,'pose',10)
		self.subscription = self.create_subscription(JointState,'joint_states',self.callback_fk,10)
		self.subscription
								
	#define callback function for forward kinematics
	def callback_fk(self,msg):
		l0 = 2
		l1 = 1
		l2 = 1
		l3 = 1
		#extract angles from msg
		q1,q2,d3 = msg.position
		#calculate the homogenous transformation matrix
		A1 = np.mat([[cos(q1), -sin(q1), 0, l1*cos(q1)],[sin(q1), cos(q1), 0, l1*sin(q1)],[0,0,1,l0],[0,0,0,1]])
		A2 = np.mat([[cos(q2), -sin(q2), 0, l2*cos(q2)],[sin(q2), cos(q2), 0, l2*sin(q2)],[0,0,1,0],[0,0,0,1]])
		A3 = np.mat([[1,0,0,0],[0,1,0,0],[0,0,1,-d3],[0,0,0,1]])
		T = A1*A2*A3
		#end effector pose
		x = T[0,3]
		y = T[1,3]
		z = T[2,3]
		#publish pose to topic 'pose'
		pub_msg = Float64MultiArray()
		pub_msg.data = [x,y,z]
		self.publisher_.publish(pub_msg)
		#print the resulting matrix to the terminal
		#self.get_logger().info('The resulting pose is \n{}'.format(T))
		
		
#defining the main function
def main(args=None):
	#initialize rclpy and create node
	rclpy.init(args=args)
	robo_fk = robot_fk()
	rclpy.spin(robo_fk)
	#destroy node
	robo_fk.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
