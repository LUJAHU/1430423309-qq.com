import numpy as np
import cv2 as cv
import math


# calculate distance between two points
def points_dist(A, B):
    a = np.array(A)
    b = np.array(B)
    v = a - b
    return math.hypot(v[0],v[1])


# detect whether bend arm
def is_bend_arm(last_points):
    RShouder = last_points[2]
    RElbow = last_points[3]
    RWrist = last_points[4]
    r_s_w_dict = points_dist(RShouder, RWrist)
    r_e = points_dist(RElbow, RShouder) + points_dist(RElbow, RWrist)
    delta = 5
    print("bend arm:", r_e, r_s_w_dict)
    # not bend arm
    if abs(r_e - r_s_w_dict) > delta:
        print("bend arm:",r_e,r_s_w_dict)
        return 1
    else:
        return 0


# detect whether suitable shot time
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


# detect racket's direction
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
def shot_result(img, last_points, last_rac_ball):
    res_is_bend_arm = is_bend_arm(last_points)
    res_shot_position = shot_position(last_points,last_rac_ball)
    res_is_downward_rac = is_downward_rac(last_points,last_rac_ball)
    return res_is_bend_arm,res_shot_position,res_is_downward_rac


def shot_text(img,res_is_bend_arm,res_shot_position,res_is_downward_rac):
    right_color = (255, 255, 255)
    wrong_color = (0, 0, 255)
    cv.putText(img, 'Shot Stage', (0, 150), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    if res_is_bend_arm == 1:
        cv.putText(img, 'Bend arm', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Not bend arm', (0, 185), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)

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
