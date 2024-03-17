import streamlit as st
import cv2
import numpy as np
from keras.models import load_model

model = load_model('../models/plant_disease.h5')
# print(model)
CLASS_NAMES = ['Corn-Common_rust', 'Potato-Early_blight', 'Tomato-Bacterial_spot']

# Streamlit texts
st.title("Plant Disease Detection")
st.markdown("Upload an image of the plant leaf")

# Streamlit components
plant_image = st.file_uploader("Choose an image...", type="jpg")
submit = st.button('Predict')

# By ButtonClick - prepocessing image + prediction
if submit:
    if plant_image is not None:
        
        # converting the file to an opencv image.
        file_bytes = np.asarray(bytearray(plant_image.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # showing the image on UI
        st.image(opencv_image, channels="BGR")
        st.write(opencv_image.shape)

        # prepocessing - resizing the image
        opencv_image = cv2.resize(opencv_image, (256,256))
        # prepocessing - converting image to 4 Dimension
        opencv_image.shape = (1,256,256,3)
        
        # prediction
        Y_pred = model.predict(opencv_image)
        result = CLASS_NAMES[np.argmax(Y_pred)]
        st.title(str("This is "+result.split('-')[0]+ " leaf with " + result.split('-')[1]))
