import rclpy
import math as m
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'topic',
            self.listener_callback,
            10)
        self.flag=0
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
    	string=String()
    	string1=String()
    	if(self.flag==0):
    	    quat1=msg.data[0]
    	    quat2=msg.data[1]
    	    quat3=msg.data[2]
    	    d1=1
    	    d2=1
    	    d3=1
    	    self.get_logger().info('I recieved q1: "%f" ' %msg.data[0] )	
    	    self.get_logger().info('I recieved q2: "%f" ' %msg.data[1] )	
    	    self.get_logger().info('I recieved q3: "%f" ' %msg.data[2] )		
    	    cos1=m.cos(quat1)
    	    cos2=m.cos(quat2)
    	    cos3=m.cos(quat3)
    	    sin1=m.sin(quat1)
    	    sin2=m.sin(quat2)
    	    sin3=m.sin(quat3)
    	    Homo_Mat=[[cos1*(cos2*cos3-sin2*sin3),-1*cos1*(cos1*sin3+sin2*cos3),-1*sin1,(cos1*cos2*(d2+d3*cos3))-(d3*cos1*sin2*sin3)],[sin1*(cos2*cos3-sin2*sin3),-1*sin1*(cos2*sin3+sin2*cos3),cos1,(sin1*cos2*(d2+d3*cos3)-d3*sin1*sin2*sin3)],[(-1*sin2*cos3)-cos2*sin3,(sin2*sin3)-(cos2*cos3),0,d1-(sin2*(d2+d3*cos3))-d3*sin3*cos2],[0,0,0,1]]
    	    string1=''
    	    for i in Homo_Mat:
    	    	string=' '.join(str(e) for e in i)
    	    	string1 +='['+ string + ']'
    	    	
    	    self.get_logger().info('The Homogenous matrix is "%s"' %string1)	
    	    self.flag=1
    	

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
