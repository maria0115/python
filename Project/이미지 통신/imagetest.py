import cnn_model
import keras
from tensorflow.keras import datasets, layers, models
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

im_rows = 32 # 이미지의 높이
im_cols = 32 # 이미지의 너비
im_color = 3 # 이미지의 색공간
in_shape = (im_rows, im_cols, im_color)
nb_classes = 2

LABELS = ["도넛","햄버거"]
#CALORIES = [588, 118, 648]
CALORIES = ["452.2", "671"]
# 저장한 CNN 모델 읽어 들이기
model = cnn_model.get_model(in_shape, nb_classes)
model.load_weights('./image/photos-model.hdf5')

def check_photo(path):
    # 이미지 읽어 들이기
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    img = Image.open(path)
    img = img.convert("RGB") # 색공간 변환하기
    img = img.resize((im_cols, im_rows)) # 크기 변경하기

    # 데이터 변환하기
    x = np.asarray(img)
    x = x.reshape(-1, im_rows, im_cols, im_color)
    x = x / 255

    # 예측하기
    pre = model.predict([x])[0]
    idx = pre.argmax()
    per = int(pre[idx] * 100)
    return (idx, per)

def check_photo_str(path):
    idx, per = check_photo(path)
    # 응답하기
    return '{"'+'이름":'+'"'+LABELS[idx]+'",'+'"'+'칼로리'+'"'+':"'+CALORIES[idx]+'",'+'"'+'정확도'+'"'+':"'+str(per)+'"}'
