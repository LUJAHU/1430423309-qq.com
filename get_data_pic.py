import cv2 as cv
import numpy as np
import argparse
import time
from ready import ready_text
from swing import  swing_text

parser = argparse.ArgumentParser(
        description='This script is used to demonstrate OpenPose human pose estimation network '
                    'from https://github.com/CMU-Perceptual-Computing-Lab/openpose project using OpenCV. '
                    'The sample and model are simplified and could be used for a single person on the frame.')
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')


args = parser.parse_args()

# Empty list to store the detected keypoints
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                   "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                   "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                   ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                   ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]
net = cv.dnn.readNet("pose.prototxt", "pose.caffemodel")


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


import os
yolo_dir = 'E:/skeleton/'
net_yolo = cv.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
def detect_racket_tennis(frame):
    weightsPath = os.path.join(yolo_dir, 'yolov3.weights')  # 权重文件
    configPath = os.path.join(yolo_dir, 'yolov3.cfg')  # 配置文件
    labelsPath = os.path.join(yolo_dir, 'coco.names')  # label名称
    # imgPath = os.path.join(yolo_dir, '140.jpg')  # 测试图像
    CONFIDENCE = 0.5  # 过滤弱检测的最小概率
    THRESHOLD = 0.4  # 非最大值抑制阈值
    # 加载网络、配置权重
    net = cv.dnn.readNetFromDarknet(configPath, weightsPath)  # #  利用下载的文件
    print("[INFO] loading YOLO from disk...")  # # 可以打印下信息

    # 加载图片、转为blob格式、送入网络输入层
    # img = cv.imread(imgPath)
    # ret, img = cap.read()
    img = frame
    blobImg = cv.dnn.blobFromImage(img, 1.0 / 255.0, (416, 416), None, True,
                                   False)  # # net需要的输入是blob格式的，用blobFromImage这个函数来转格式
    net.setInput(blobImg)  # # 调用setInput函数将图片送入输入层

    # 获取网络输出层信息（所有输出层的名字），设定并前向传播
    outInfo = net.getUnconnectedOutLayersNames()  # # 前面的yolov3架构也讲了，yolo在每个scale都有输出，outInfo是每个scale的名字信息，供net.forward使用
    start = time.time()
    layerOutputs = net.forward(outInfo)  # 得到各个输出层的、各个检测框等信息，是二维结构。
    end = time.time()
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))  # # 可以打印下信息

    # 拿到图片尺寸
    (H, W) = img.shape[:2]
    # 过滤layerOutputs
    # layerOutputs的第1维的元素内容: [center_x, center_y, width, height, objectness, N-class score data]
    # 过滤后的结果放入：
    boxes = []  # 所有边界框（各层结果放一起）
    confidences = []  # 所有置信度
    classIDs = []  # 所有分类ID

    # # 1）过滤掉置信度低的框框
    for out in layerOutputs:  # 各个输出层
        for detection in out:  # 各个框框
            # 拿到置信度
            scores = detection[5:]  # 各个类别的置信度
            classID = np.argmax(scores)  # 最高置信度的id即为分类id
            confidence = scores[classID]  # 拿到置信度

            # 根据置信度筛查
            if confidence > CONFIDENCE:
                box = detection[0:4] * np.array([W, H, W, H])  # 将边界框放会图片尺寸
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # # 2）应用非最大值抑制(non-maxima suppression，nms)进一步筛掉
    idxs = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)  # boxes中，保留的box的索引index存入idxs
    # 得到labels列表
    with open(labelsPath, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')
    # 应用检测结果
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3),
                               dtype="uint8")  # 框框显示颜色，每一类有不同的颜色，每种颜色都是由RGB三个值组成的，所以size为(len(labels), 3)
    rac_ball = {}
    if len(idxs) > 0:
        for i in idxs.flatten():  # indxs是二维的，第0维是输出层，所以这里把它展平成1维
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            if classIDs[i] == 32 or classIDs[i] == 38:
                rac_ball[labels[classIDs[i]]] = (x, y, w, h)
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)  # 线条粗细为2px
                # 32->sports ball 38->tennis racket
                text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
                cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color,
                           2)  # cv.FONT_HERSHEY_SIMPLEX字体风格、0.5字体大小、粗细2px
    return img, rac_ball

def get_first_last_frame(path):
    cap = cv.VideoCapture(path)
    count_frame = cap.get(7)
    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    flag1, first_frame = cap.read()
    cap.set(cv.CAP_PROP_POS_FRAMES, count_frame - 1)
    flag2, last_frame = cap.read()
    if flag1 and flag2:
        return first_frame, last_frame

def get_data(img):
    img, rac_ball = detect_racket_tennis(img)
    points = get_points(img)
    return rac_ball,points


