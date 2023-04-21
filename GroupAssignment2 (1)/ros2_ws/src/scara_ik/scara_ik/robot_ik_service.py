from srv_interface.srv import InvKinematics

import rclpy
from rclpy.node import Node
import math

class service_ik(Node):

    def __init__(self):
        super().__init__('service_ik')
        self.srv = self.create_service(InvKinematics, 'inverse_kinematics', self.ik_callback)

    def ik_callback(self, request, response):
        l0 = 2
        l1 = 1
        l2 = 1
        l3 = 1
        
        x = request.x
        y = request.y
        z = request.z
        
        D = (x**2+y**2-l1**2-l2**2)/(2*l1*l2)
        theta2 = math.atan(D/(math.sqrt(1-D**2)))
        theta1 = math.atan(y/x) - theta2
        d3 = l0-z
        
        response.q1 = theta1
        response.q2 = theta2
        response.q3 = d3
        
        self.get_logger().info('Incoming request\nx: %f y: %f z: %f' % (x, y, z))
	
        return response


def main(args=None):
    rclpy.init(args=args)

    inverse_service = service_ik()

    rclpy.spin(inverse_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
