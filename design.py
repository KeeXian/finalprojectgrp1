import streamlit as st

import cv2 as cv
import cvlib
from cvlib.object_detection import draw_bbox

st.title("Wildlife Detection App")

if 'wildlife' not in st.session_state:
    st.session_state['wildlife'] = 0

list_of_wildlife = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'person']

def process_picture(img_file):
    with open("temp.png", "wb") as f:
        f.write(img_file.getbuffer())

    img = cv.imread("temp.png")
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bbox, label, conf = cvlib.detect_common_objects(img)
    for i in range(len(label)):
        if label[i] not in list_of_wildlife:
            label.pop(i)
            bbox.pop(i)
            conf.pop(i)

    output_image = draw_bbox(img, bbox, label, conf)

    st.session_state.wildlife = len(label)
    return output_image


uploaded_file = st.file_uploader('Upload a picture of a cat', type=['png'])
if uploaded_file:
    with open('picture.jpg', 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    img = cv.imread("picture.jpg")
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    bbox, label, conf = cvlib.detect_common_objects(img)
    for i in range(len(label)):
        if label[i] not in list_of_wildlife:
            label.pop(i)
            bbox.pop(i)
            conf.pop(i)

    output_image = draw_bbox(img, bbox, label, conf)

    st.image(output_image)
    st.session_state.wildlife = len(label)


picture = st.camera_input('Webcam')
if picture:
    st.image(process_picture(picture))
st.write("Number of wildlife detected: ", st.session_state.wildlife)