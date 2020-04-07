import numpy as np
import cv2 as cv
import math

def points_dist(A, B):
    a = np.array(A)
    b = np.array(B)
    v = a - b
    return math.hypot(v[0], v[1])

def is_rotate_hip(first_points,last_points):
    f_RHip = first_points[8]
    f_LHip = first_points[11]
    f_h_dist = points_dist(f_LHip, f_RHip)
    l_RHip = last_points[8]
    l_LHip = last_points[11]
    l_h_dist = points_dist(l_LHip, l_RHip)
    print(f_h_dist, l_h_dist)
    print('rwrist:',last_points[4])
    if abs(f_h_dist - l_h_dist) > 20:
        # enough rotation
        return 1
    else:
        return 0

def is_wave_rac(last_points,last_rac_ball):
    temp = last_rac_ball['tennis racket']
    rac_x = temp[0]
    LWrist_x = last_points[7][0]
    if LWrist_x > rac_x:
        print('last lwrist-rac x:',LWrist_x,rac_x)
        return 1
    else:
        return 0


def aftershot_result(first_points,last_points,first_rac_ball,last_rac_ball):
    res_is_rotate_hip = is_rotate_hip(first_points,last_points)
    res_is_wave_rac = is_wave_rac(last_points,last_rac_ball)
    return res_is_rotate_hip,res_is_wave_rac

def aftershot_text(img, res_is_rotate_hip,res_is_wave_rac):
    right_color = (255, 255, 255)
    wrong_color = (0, 0, 255)
    cv.putText(img, 'AfterShot Stage', (0, 150), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2, 4)
    if res_is_rotate_hip:
        cv.putText(img, 'Enough shoulder rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not enough shoulder rotate', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

    if res_is_wave_rac:
        cv.putText(img, 'Enough wave', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not enough wave', (0, 220), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    return img
