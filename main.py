import cv2 as cv
from get_data_pic import get_first_last_frame,get_data
from ready import ready_text
from swing import swing_result,swing_text
from shot import shot_result,shot_text
from aftershot import aftershot_result,aftershot_text

def ready(video_path):
    cap = cv.VideoCapture(video_path)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('./result/ready_result.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        hasframe, frame = cap.read()
        if hasframe is True:
            img,rac_ball, points = get_data(frame)
            img = ready_text(img,points,rac_ball)
            cv.imshow('ready', img)
            out.write(img)
        else:
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cap.release()
    cv.destroyAllWindows()


def swing(video_path):
    first_frame, last_frame = get_first_last_frame(video_path)
    img,first_rac_ball, first_points = get_data(first_frame)
    img,last_rac_ball, last_points = get_data(last_frame)
    res_is_rotate_shoulder, res_is_rotate_arm, res_is_rotate_hip,res_is_downward_rac = swing_result(first_points,last_points,
                                                                     first_rac_ball, last_rac_ball)
    cap = cv.VideoCapture(video_path)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('./result/swing_result.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        hasframe, frame = cap.read()
        if hasframe is True:
            img = swing_text(frame, res_is_rotate_shoulder, res_is_rotate_arm, res_is_rotate_hip,res_is_downward_rac)
            # img, rac_ball, points = get_data(img)
            cv.imshow('swing', img)
            out.write(img)
        else:
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cap.release()
    cv.destroyAllWindows()


def shot(video_path):
    first_frame, last_frame = get_first_last_frame(video_path)
    img,first_rac_ball, first_points = get_data(first_frame)
    img,last_rac_ball, last_points = get_data(last_frame)
    res_is_bend_arm, res_shot_position, res_is_downward_rac = shot_result(last_frame, first_points, last_points, last_rac_ball)
    cap = cv.VideoCapture(video_path)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('./result/shot_result.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        hasframe, frame = cap.read()
        if hasframe is True:
            img = shot_text(frame,res_is_bend_arm,res_shot_position,res_is_downward_rac)
            # img, rac_ball, points = get_data(img)
            cv.imshow('shot', img)
            out.write(img)
        else:
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cap.release()
    cv.destroyAllWindows()

def aftershot(video_path):
    first_frame, last_frame = get_first_last_frame(video_path)
    first_frame, first_rac_ball, first_points = get_data(first_frame)
    img, last_rac_ball, last_points = get_data(last_frame)
    res_is_rotate_hip,res_is_wave_rac = aftershot_result(first_points, last_points, first_rac_ball, last_rac_ball)
    cap = cv.VideoCapture(video_path)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('./result/aftershot_result.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        hasframe, frame = cap.read()
        if hasframe is True:
            img = aftershot_text(frame,res_is_rotate_hip,res_is_wave_rac)
            # img, rac_ball, points = get_data(img)
            cv.imshow('Aftershot', img)
            out.write(img)
        else:
            break
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    cap.release()
    cv.destroyAllWindows()



