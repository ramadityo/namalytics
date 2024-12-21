import streamlit as st
import pandas as pd

from PIL import Image
from ultralytics import YOLO
import cv2
import tempfile

st.set_page_config(page_title="Object Detection Web App")

st.write(
    """
    # Object Detection Web App

    Selamat datang di Aplikasi Object Detection sederhana! 🚀 Aplikasi ini dibuat untuk mengidentifikasi nama mahasiswa yang terdaftar di UPJ secara real-time. Selamat mencoba!
    """
)

class Detection:
    def detect(img):
        model = YOLO('model/best.pt')  
        results = model(img)         
        rgb_image = results[0].plot()[:, :, ::-1]  
        return rgb_image, results[0].speed 


cap = cv2.VideoCapture(1)
frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")

while cap.isOpened() and not stop_button_pressed:
    ret, frame = cap.read()
    
    if not ret:
        st.write("Video sudah selesai direkam")
        break

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_result, stats = Detection.detect(frame)


    frame_placeholder.image(img_result, channels="RGB")

    if stop_button_pressed:
        break

cap.release()
