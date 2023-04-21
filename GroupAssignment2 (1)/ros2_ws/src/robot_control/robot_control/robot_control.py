#import all the dependencies required to run the node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from pdcontrol_interface.srv import JointRef
import numpy as np
from math import *
import csv

#initilize the robot_fk class by inheriting the Node class from rclpy.node
class robot_pdcontrol(Node):
	#define the constructor for the class
	def __init__(self):
		#call the parent node constructor and give the name to the node
		super().__init__('robot_pdcontrol')
		
		#initilaize current states, reference values, torques
		self.q1_ref=0.0;
		self.q2_ref=0.0;
		self.q3_ref=0.0;
		self.q1=0.0;
		self.q2=0.0;
		self.q3=0.0;
		self.q1_dot=0.0;
		self.q2_dot=0.0;
		self.q3_dot=0.0;
		self.u1 = 0.0;
		self.u2 = 0.0;
		self.u3 = 0.0;
		
		#open file and creater writer
		self.f = open('/home/ankush/Desktop/plot.csv','w')
		self.writer = csv.writer(self.f)
		self.writer.writerow(['q1','q2','q3','u1','u2'])
		
		#create subscriber joint_states
		self.sub = self.create_subscription(JointState,'joint_states',self.callback_sub,10)
		self.sub
		
		#create service joint_ref
		self.srv = self.create_service(JointRef,'joint_reference',self.callback_service)
		
		#create effort publisher
		self.pub = self.create_publisher(Float64MultiArray,'forward_effort_controller/commands',10)
		
	#define callback function for forward kinematics
	def callback_sub(self,msg):
		#current joint states
		self.q1 = msg.position[0]
		self.q2 = msg.position[1]
		self.q3 = msg.position[2]
		self.q1_dot = msg.velocity[0]
		self.q2_dot = msg.velocity[1]
		self.q3_dot = msg.velocity[2]
	        
	        ##if self.q1_ref == 0 and self.q2_ref == 0 and self.q3_ref == 0 :
	        ##self.u1 = 0
	        ##self.u2 = 0 
	        ##self.u3 = 0
	        ##
	        ##else  
	        
	
	         	
		#joint1 control
		kp1 = 30
		kd1 = 22
		e1 = self.q1-self.q1_ref
		e1_dot = self.q1_dot-0
		self.u1 = -kp1*e1-kd1*e1_dot
		
		#joint2 control
		kp2 = 24
		kd2 = 16
		e2 = self.q2 - self.q2_ref
		e2_dot = self.q2_dot - 0
		self.u2 = -kp2*e2-kd2*e2_dot
		
		#joint3 control
		kp3 = 150
		kd3 = 60
		e3 = self.q3 - self.q3_ref
		e3_dot = self.q3_dot-0
		self.u3 = -kp3*e3-kd3*e3_dot
		
		#publish control inputs
		torq = Float64MultiArray()
		torq.data = [self.u1,self.u2,self.u3]
		self.pub.publish(torq)
		data = [self.q1,self.q2,self.q3,self.u1,self.u1]
		self.writer.writerow(data)
			
				
	def callback_service(self,request,response):
		self.q1_ref = request.q1
		self.q2_ref = request.q2
		self.q3_ref = request.q3
		response.n = 1.0
		return response
	def close_file(self):
		self.f.close()

#defining the main function
def main(args=None):
	#initialize rclpy and create node
	rclpy.init(args=args)
	robo_ctrl = robot_pdcontrol()
	rclpy.spin(robo_ctrl)
	#destroy node
	robo_ctrl.destroy_node()
	robo_ctrl.close_file()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
