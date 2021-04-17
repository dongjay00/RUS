import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model

IMG_SIZE = (34, 26)

def crop_eye(img, eye_points):
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]
    margin_x, margin_y = w / 2, h / 2
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)
    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]
    return eye_img, eye_rect

def model():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    eye_model = load_model('blink_eyes.h5')
    phone_model = load_model("keras_model.h5")

    # image 입력
    cap = cv2.VideoCapture('images/10.png')
    eyes = 0
    result = ""

    ret, frame = cap.read()

    frame = cv2.resize(frame, dsize=(0, 0), fx=0.5, fy=0.5)

    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)        

    if faces:
        for i,face in enumerate(faces):
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)

            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

            pred_l = eye_model.predict(eye_input_l)
            pred_r = eye_model.predict(eye_input_r)

            # visualize
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

    frame_fliped = cv2.flip(frame, 1)
    size = (224, 224)
    frame_resized = cv2.resize(frame_fliped, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    preprocessed = frame_normalized.reshape((1, 224, 224, 3))

    predict = phone_model.predict(preprocessed)

    # predict 0 = normal,  1 = phone,  2 = sleep,  3 = empty

    normal = predict[0,0]
    phone = predict[0,1]
    sleep = predict[0,2]
    empty = predict[0,3]
    max_val = max(predict[0])

    if eyes == "close" or max_val == sleep:
        result = "sleep"
    elif max_val == empty:
        result = "empty"
    elif max_val == phone:
        result = "other"
    else:
        result = "normal"

    return result

print(model())