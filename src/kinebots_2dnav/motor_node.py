#!/usr/bin/env python
import rospy
import pigpio
from geometry_msgs.msg import Twist

pi = pigpio.pi()
PWM_FREQUENCY = 8000
LEFT_MOTOR_SPEED = 12  # PWM1
RIGHT_MOTOR_SPEED = 13  # PWM2
LEFT_MOTOR_DIR = 23  # DIR1
RIGHT_MOTOR_DIR = 24  # DIR2

def callback(msg):
    linear = msg.linear.x
    angular = msg.angular.z
    left_motor_speed = 1000000
    right_motor_speed = 1000000
    if angular > 0.5:
        left_motor_direction = 1
        right_motor_direction = 0
    elif angular < -0.5:
        left_motor_direction = 0
        right_motor_direction = 1
    elif linear > 0.1:
        print('hi')
        left_motor_direction = 0
        right_motor_direction = 0
    elif linear < -0.1:
        left_motor_direction = 1
        right_motor_direction = 1
    else:
        left_motor_direction = 0
        right_motor_direction = 0
        left_motor_speed = 0.0
        right_motor_speed = 0.0
    pi.hardware_PWM(LEFT_MOTOR_SPEED, PWM_FREQUENCY,
            left_motor_speed)
    pi.hardware_PWM(RIGHT_MOTOR_SPEED, PWM_FREQUENCY,
            right_motor_speed)
    pi.write(LEFT_MOTOR_DIR, left_motor_direction)
    pi.write(RIGHT_MOTOR_DIR, right_motor_direction)

def listener():
    # Set up the GPIO pins.
    pi.set_mode(LEFT_MOTOR_SPEED, pigpio.OUTPUT)
    pi.set_mode(RIGHT_MOTOR_SPEED, pigpio.OUTPUT)
    pi.set_mode(LEFT_MOTOR_DIR, pigpio.OUTPUT)
    pi.set_mode(RIGHT_MOTOR_DIR, pigpio.OUTPUT)
    pi.hardware_PWM(LEFT_MOTOR_SPEED, PWM_FREQUENCY, 0)
    pi.hardware_PWM(RIGHT_MOTOR_SPEED, PWM_FREQUENCY, 0)

    rospy.init_node('cmd_vel_listener')
    rospy.Subscriber('/cmd_vel', Twist, callback)

    # spin() keeps python from exiting until this node is stopped.
    rospy.spin()

if __name__ == '__main__':
    listener()
