import numpy as np
import cv2 as cv
import math


def points_dist(A, B):
    a = np.array(A)
    b = np.array(B)
    v = a - b
    return math.hypot(v[0],v[1])


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



def shot_position(last_points,last_rac_ball):
    chest = last_points[14][1]
    rhip = last_points[8][1]
    temp = last_rac_ball['sports ball']
    ball = temp[1] + temp[3] / 2
    if chest <= ball and ball <= rhip:
        print("chest/hip/ball positions:",chest,rhip,ball)
        return 1
    elif ball > chest:
        return 'high'
    elif ball < rhip:
        return 'low'


def is_downward_rac(last_points,last_rac_ball):
    RWrist = last_points[4][1]
    temp = last_rac_ball['tennis racket']
    rac = temp[1]+temp[3]/2
    print("rwrist/rac:",RWrist,rac)
    if rac > RWrist:
        return 1
    else:
        return 0


# put text on img
def shot_result(img, first_points,last_points, last_rac_ball):
    res_is_rotate_hip = is_rotate_hip(first_points, last_points)
    res_shot_position = shot_position(last_points,last_rac_ball)
    res_is_downward_rac = is_downward_rac(last_points,last_rac_ball)
    return res_is_rotate_hip,res_shot_position,res_is_downward_rac

def shot_text(img,res_is_rotate_hip,res_shot_position,res_is_downward_rac):
    right_color = (255, 255, 255)
    wrong_color = (0, 0, 255)
    cv.putText(img, 'Shot Stage', (0, 150), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    if res_is_rotate_hip == 1:
        cv.putText(img, 'Enough hip rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not enough hip rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    if res_shot_position == 1:
        cv.putText(img, 'Suitable shot position', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    elif res_shot_position == 'high':
        cv.putText(img, 'shot position TOO HIGH', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    else:
        cv.putText(img, 'shot position TOO LOW', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    if res_is_downward_rac == 1:
        cv.putText(img, 'Downward racket', (0, 255), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not downward racket', (0, 255), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    return img
