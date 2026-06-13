import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket

class KinematicsWifiBridge(Node):
    def __init__(self):
        super().__init__('kinematics_wifi_bridge')
        

        self.wheel_base = 0.17
        self.wheel_radius = 0.03
        
   
        self.esp_ip = '192.168.1.100'  
        self.esp_port = 8080
        
       
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.esp_ip, self.esp_port))
            self.get_logger().info(f"Connected with ESP32: {self.esp_ip}")
        except Exception as e:
            self.get_logger().error(f"Connection fail! Is the ESP turned on ? Error: {e}")
        

        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.get_logger().info("Brain ready , waiting for /cmd_vel ....")
        
        
        

    def cmd_vel_callback(self, msg):
       
        v = msg.linear.x
        w = msg.angular.z
        
        
        v_r = v + (w * self.wheel_base) / 2.0
        v_l = v - (w * self.wheel_base) / 2.0
        
        
        w_r = v_r / self.wheel_radius
        w_l = v_l / self.wheel_radius
        
        
        pwm_r = int(w_r * 10) 
        pwm_l = int(w_l * 10)
        
        
        command_str = f"{pwm_l},{pwm_r}\n"
        
        
        try:
            self.sock.sendall(command_str.encode('utf-8'))
            self.get_logger().info(f"data sent: {command_str.strip()}")
        except Exception as e:
            self.get_logger().error(f"There was a problem sending data: {e}")
            
            
            
            
            

def main(args=None):
    rclpy.init(args=args)
    node = KinematicsWifiBridge()
    rclpy.spin(node)
    node.sock.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
