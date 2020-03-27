import numpy as np
import cv2 as cv
import math

# used to detect whether P is on line AB
def is_line(A,B,P):
    v_AB = (B[0]-A[0],B[1]-A[1])
    v_n = (-v_AB[1],v_AB[0])
    v_AP = (P[0]-A[0],P[1]-A[1])
    # dot result is 0 means P is on AB
    if np.dot(v_AP,v_n) == 0:
        return 1
    else:
        return 0

# bend knee
def is_ready_knee(points):
    RHip = points[8]
    LHip = points[11]
    RKnee = points[9]
    LKnee = points[12]
    RAnkle = points[10]
    LAnkle = points[13]
    r_h_a_dict = points_dist(RHip, RAnkle)
    l_h_a_dict = points_dist(LHip, LAnkle)
    r_k = points_dist(RKnee, RHip) + points_dist(RKnee, RAnkle)
    l_k = points_dist(LKnee, LHip) + points_dist(LKnee, LAnkle)
    delta = 5
    # not bend arm
    if abs(r_k - r_h_a_dict) < 5 and abs(l_k - l_h_a_dict) < 5:
        return 0
    else:
        return 1

# suitable distance between ankles
def is_ready_ankle(points):
    RAnkle = points[10]
    LAnkle = points[13]
    RShouder = points[2]
    LShoulder = points[5]
    ankle_dis = abs(RAnkle[0]-LAnkle[0])
    shoulder_dis = abs(RShouder[0]-LShoulder[0])
    delta = 10
    if abs(ankle_dis-shoulder_dis) > delta:
        return 0
    else:
        return 1

# detect only use one hand to grip racket
def is_two_hand(img,points,rac_ball):
    LWrist = points[7]
    temp = rac_ball['tennis racket'] #x/y/w/h
    if LWrist[0]>=temp[0] and LWrist[0]<=(temp[0]+temp[2]) and LWrist[1]>=temp[1] and LWrist[1]<=(temp[1]+temp[3]):
        # in rectangle means use two hand
        return 1
    else:
        return 0


def points_dist(A, B):
    a = np.array(A)
    b = np.array(B)
    v = a - b
    return math.hypot(v[0],v[1])

# bend arm
def is_ready_arm(points):
    RShouder = points[2]
    RElbow = points[3]
    RWrist = points[4]
    LShouder = points[5]
    LElbow = points[6]
    LWrist = points[7]
    r_s_w_dict = points_dist(RShouder,RWrist)
    l_s_w_dict = points_dist(LShouder,LWrist)
    r_e = points_dist(RElbow,RShouder)+points_dist(RElbow,RWrist)
    l_e = points_dist(LElbow,LShouder)+points_dist(LElbow,LWrist)
    delta = 5
    # not bend arm
    if abs(r_e-r_s_w_dict)<5 and abs(l_e-l_s_w_dict)<5:
        return 0
    else:
        return 1

# put text on img
def ready_text(img,points,rac_ball):
    right_color = (255, 255, 255)
    wrong_color = (0, 0, 255)
    cv.putText(img, 'Ready Stage', (150,150), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    if is_ready_ankle(points):
        cv.putText(img, 'right ankle distance', (150,185), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'Wrong ankle distance', (150, 185), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    if is_ready_knee(points):
        cv.putText(img, 'right bend knee', (150, 210), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'not bend knee', (150, 210), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    if is_ready_arm(points):
        cv.putText(img, 'right bend arm', (150, 245), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'not bend arm', (150, 245), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    if is_two_hand(img,points,rac_ball):
        cv.putText(img, 'two hand', (150, 280), cv.FONT_HERSHEY_COMPLEX, 1, right_color, 2, 4)
    else:
        cv.putText(img, 'one hand', (150, 280), cv.FONT_HERSHEY_COMPLEX, 1, wrong_color, 2, 4)
    return img