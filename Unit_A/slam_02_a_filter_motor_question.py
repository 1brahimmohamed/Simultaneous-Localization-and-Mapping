# Implement the first move model for the Lego robot.
# 02_a_filter_motor
# Claus Brenner, 31 OCT 2012
from math import sin, cos, pi
import numpy as np
from pylab import *
from lego_robot import *


# This function takes the old (x, y, heading) pose and the motor ticks
# (ticks_left, ticks_right) and returns the new (x, y, heading).
def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width):
    # Find out if there is a turn at all.
    if motor_ticks[0] == motor_ticks[1]:
        # No turn. Just drive straight.

        # --->>> Implement your code to compute x, y, theta here.

        l = motor_ticks[0] * ticks_to_mm
        r = motor_ticks[1] * ticks_to_mm
        x, y, theta_new = old_pose[0], old_pose[1], old_pose[2]
        x = x + (l * np.cos(theta_new))
        y = y + (r * np.sin(theta_new))

        return x, y, theta_new

    else:
        # Turn. Compute alpha, R, etc.
        l = motor_ticks[0] * ticks_to_mm
        r = motor_ticks[1] * ticks_to_mm

        # alpha = ((r - l)/w)
        alpha = (abs(l - r) / robot_width)

        # Radius = left/alpha
        R = l / alpha

        #  _  _      _ _                      _          _ 
        # | Cx |  = | x |  - (R + width/2) * | sin(theta) |
        # |_Cy_|    |_y_|                    |_cos(theta)_|  
    
        old_pose_vector = np.array([old_pose[0], old_pose[1]])          # [x,y]

        old_theta_vector = np.array([np.sin(old_pose[2]), -np.cos(old_pose[2])])    #[sin(theta),cos(theta)]

        center_vector = old_pose_vector - ((R + (robot_width / 2)) * old_theta_vector)  #[cx, cy]


        # theta_new = (theta_old + alpha) mod 2 pi
        theta_new = (old_pose[2] + alpha) % (2 * np.pi)         

        # compute new pose =>
        #  _  _      _  _                      _            _ 
        # | X' |  = | Cx |  - (R + width/2) * |   sin(theta) |
        # |_Y'_|    |_Cy_|                    |_ -cos(theta)_|  
        
        new_pose = center_vector + (R + (robot_width / 2)) * np.array([np.sin(theta_new), -np.cos(theta_new)])

        # --->>> Implement your code to compute x, y, theta here.

        new_pose_with_angle = (new_pose[0], new_pose[1], theta_new)
        
        return new_pose_with_angle


if __name__ == '__main__':
    # Empirically derived conversion from ticks to mm.
    ticks_to_mm = 0.349

    # Measured width of the robot (wheel gauge), in mm.
    robot_width = 150.0

    # Read data.
    logfile = LegoLogfile()
    logfile.read("robot4_motors.txt")

    # Start at origin (0,0), looking along x axis (alpha = 0).
    pose = (0.0, 0.0, 0.0)

    # Loop over all motor tick records generate filtered position list.
    filtered = []
    for ticks in logfile.motor_ticks:
        pose = filter_step(pose, ticks, ticks_to_mm, robot_width)
        filtered.append(pose)

    # Draw result.
    for pose in filtered:
        print(pose)
        plot([p[0] for p in filtered], [p[1] for p in filtered], 'bo')
    show()
