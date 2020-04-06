import numpy as np
import cv2 as cv
import math


# calculate distance between two points
def points_dist(A, B):
    a = np.array(A)
    b = np.array(B)
    v = a - b
    return math.hypot(v[0], v[1])


# detect whether rotate shoulder
def is_rotate_shoulder(first_points,last_points,first_rac_ball,last_rac_ball):
    f_RShouder = first_points[2]
    f_LShoulder = first_points[5]
    f_s_dist = points_dist(f_LShoulder,f_RShouder)
    l_RShouder = last_points[2]
    l_LShoulder = last_points[5]
    l_s_dist = points_dist(l_LShoulder,l_RShouder)
    print("s_dist:",f_s_dist,l_s_dist)
    # use distance between shoulders
    if abs(f_s_dist-l_s_dist) > 70:
        # enough rotation
        return 1
    else:
        return 0


# detect whether rotate arm
def is_rotate_arm(first_points,last_points):
    f_RElbow = first_points[3]
    f_LElbow = first_points[6]
    f_e_dist = points_dist(f_LElbow, f_RElbow)
    l_RElbow = last_points[3]
    l_LElbow = last_points[6]
    l_e_dist = points_dist(l_LElbow, l_RElbow)
    print("elbow:",f_e_dist, l_e_dist)
    if abs(f_e_dist-l_e_dist)>100:
        return 1
    else:
        return 0


# detect whether rotate hip
def is_rotate_hip(first_points,last_points):
    f_RHip = first_points[8]
    f_LHip = first_points[11]
    f_h_dist = points_dist(f_LHip, f_RHip)
    l_RHip = last_points[8]
    l_LHip = last_points[11]
    l_h_dist = points_dist(l_LHip, l_RHip)
    print(f_h_dist, l_h_dist)
    if abs(f_h_dist - l_h_dist) > 20:
        # enough rotation
        return 1
    else:
        return 0


def swing_result(first_points,last_points,first_rac_ball,last_rac_ball):
    res_is_rotate_shoulder = is_rotate_shoulder(first_points, last_points, first_rac_ball, last_rac_ball)
    res_is_rotate_arm = is_rotate_arm(first_points, last_points)
    res_is_rotate_hip = is_rotate_hip(first_points, last_points)
    return res_is_rotate_shoulder,res_is_rotate_arm,res_is_rotate_hip


# put text on img
def swing_text(img, res_is_rotate_shoulder,res_is_rotate_arm,res_is_rotate_hip):
    right_color = (255, 255, 255)
    wrong_color = (0, 0, 255)
    cv.putText(img, 'Swing Stage', (0, 150), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    if res_is_rotate_shoulder:
        cv.putText(img, 'Enough shoulder rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not ebough shoulder rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    if res_is_rotate_arm:
        cv.putText(img, 'Enough arm rotate', (0, 255), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not ebough arm rotate', (0, 255), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    if res_is_rotate_hip:
        cv.putText(img, 'Enough hip rotate', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not ebough hip rotate', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    return img

