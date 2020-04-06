import cv2 as cv
import numpy as np
import argparse
import time


parser = argparse.ArgumentParser(
        description='This script is used to demonstrate OpenPose human pose estimation network '
                    'from https://github.com/CMU-Perceptual-Computing-Lab/openpose project using OpenCV. '
                    'The sample and model are simplified and could be used for a single person on the frame.')
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')


args = parser.parse_args()

# Empty list to store the detected key points
BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                   "Background": 15}

POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                   ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                   ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]
net = cv.dnn.readNet("./model/pose.prototxt", "./model/pose.caffemodel")


# get key points
def get_points(frame):
    points = []
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    inp = cv.dnn.blobFromImage(frame, 0.003922, (368, 368),
                               (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inp)
    out = net.forward()

    assert (len(BODY_PARTS) <= out.shape[1])
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Add a point if it's confidence is higher than threshold.
        threshold = 0.1
        points.append((int(x), int(y)) if conf > threshold else None)
    return points

# draw skeleton on img
def draw_skeleton(frame,points):
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert (partFrom in BODY_PARTS)
        assert (partTo in BODY_PARTS)
        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
    return frame


# detect racket and tennis
def detect_racket_tennis(frame):
    weightsPath = './model/yolov3.weights'
    configPath = './model/yolov3.cfg'
    labelsPath = './model/coco.names'
    CONFIDENCE = 0.5
    THRESHOLD = 0.4
    net = cv.dnn.readNetFromDarknet(configPath, weightsPath)
    print("[INFO] loading YOLO from disk...")

    # load img, convert to blob
    img = frame
    blobImg = cv.dnn.blobFromImage(img, 1.0 / 255.0, (416, 416), None, True,
                                   False)
    net.setInput(blobImg)

    outInfo = net.getUnconnectedOutLayersNames()
    start = time.time()
    layerOutputs = net.forward(outInfo)
    end = time.time()
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))
    (H, W) = img.shape[:2]
    boxes = []
    confidences = []
    classIDs = []
    for out in layerOutputs:
        for detection in out:
            # 拿到置信度
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > CONFIDENCE:
                box = detection[0:4] * np.array([W, H, W, H])  # 将边界框放会图片尺寸
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)
    with open(labelsPath, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3),
                               dtype="uint8")
    rac_ball = {}
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            if classIDs[i] == 32 or classIDs[i] == 38:
                rac_ball[labels[classIDs[i]]] = (x, y, w, h)
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                # 32->sports ball 38->tennis racket
                text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
                cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color,
                           2)  # cv.FONT_HERSHEY_SIMPLEX字体风格、0.5字体大小、粗细2px
    return img, rac_ball


# get first frame and last frame
def get_first_last_frame(path):
    cap = cv.VideoCapture(path)
    count_frame = cap.get(7)
    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    flag1, first_frame = cap.read()
    cap.set(cv.CAP_PROP_POS_FRAMES, count_frame - 1)
    flag2, last_frame = cap.read()
    if flag1 and flag2:
        return first_frame, last_frame

# get data of key points, racket and tennis
def get_data(img):
    img, rac_ball = detect_racket_tennis(img)
    points = get_points(img)
    draw_skeleton(img,points)
    return img,rac_ball,points


