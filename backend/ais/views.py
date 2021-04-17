from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
from rest_framework import status
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants

import base64
# Create your views here.

IMG_SIZE = (34, 26)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./ais/shape_predictor_68_face_landmarks.dat')

eye_model = load_model('./ais/eyes.h5')
phone_model = load_model("./ais/motion.h5")

MODEL_PATH = './ais/yolov4-416'
IOU_THRESHOLD = 0.45
SCORE_THRESHOLD = 0.25
INPUT_SIZE = 416

saved_model_loaded = tf.saved_model.load(MODEL_PATH, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

def crop_eye(img, eyes):
    x1, y1 = np.amin(eyes, axis=0)
    x2, y2 = np.amax(eyes, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]
    margin_x, margin_y = w / 2, h / 2
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)
    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]
    return eye_img, eye_rect

def model(img_url):
    # image 입력
    cap = cv2.VideoCapture(img_url)
    eyes = 0
    result = ""
    obj_ret = []
    ret, frame = cap.read()
    # object detect
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_input = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))
    img_input = img_input / 255.
    img_input = img_input[np.newaxis, ...].astype(np.float32)
    img_input = tf.constant(img_input)
    pred_bbox = infer(img_input)

    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=IOU_THRESHOLD,
        score_threshold=SCORE_THRESHOLD
    )
    n = valid_detections.numpy()[0]

    for i in range(n):
        if classes.numpy()[0,i] == 0.0:
            obj_ret.append("person")
        if classes.numpy()[0,i] == 67.0:
            obj_ret.append("phone")

    # eye detect
    frame = cv2.resize(frame, dsize=(0, 0), fx=0.5, fy=0.5)
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if faces:
        for i,face in enumerate(faces):
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)
            eye_img_l, eye_rect_l = crop_eye(gray, eyes=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eyes=shapes[42:48])
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            pred_l = eye_model.predict(eye_input_l)
            pred_r = eye_model.predict(eye_input_r)
            state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'
            state_l = state_l % pred_l
            state_r = state_r % pred_r
            if state_l[0] == "-" and state_r[0] == "-":
                eyes = "close"
            else:
                eyes = "open"        
    else:
        eyes = "empty"

    # motions
    frame_fliped = cv2.flip(frame, 1)
    frame_resized = cv2.resize(frame_fliped, (224, 224), interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    preprocessed = frame_normalized.reshape((1, 224, 224, 3))
    predict = phone_model.predict(preprocessed)
    normal = predict[0,0]
    sleep = predict[0,1]
    other = predict[0,2]
    max_val = max(predict[0])

    if "person" not in obj_ret:
        result = "empty"
    elif "phone" in obj_ret:
        result = "other"

    if not result:
        if eyes == "close" or max_val == sleep:
            result = "sleep"
        elif max_val == normal:
            result = "normal"
        else:
            result = "other"

    return result

@api_view(['POST'])
def upload_image(request):
    img_string = request.data['img_base64']
    
    result = model(img_string) # img 주소를 스트링으로 넣어줄것
    real_result = 0
    if result == 'normal':
        real_result = 1
    elif result == 'sleep':
        real_result = 2
    elif result == 'empty':
        real_result = 3
    else:
        real_result = 4

    return Response({"result": real_result}, status=status.HTTP_201_CREATED)
