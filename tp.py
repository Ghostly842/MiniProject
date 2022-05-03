import streamlit as st
import cv2 as cv2
from PIL import Image
import numpy as np
import pytesseract
def welcome():
    
    st.title('Image Processing using Streamlit')
    
    st.subheader('A simple app that shows different image processing algorithms. You can choose the options'
             + ' from the left. I have implemented only a few to show how it works on Streamlit. ')
    
    st.image('logo.png',use_column_width=True)

selected_box = st.sidebar.selectbox(
'Choose one of the following',
('Welcome','Image Processing')
)

def load_image(filename):
    img=cv2.imread(filename)
    return img


def photo():
    st.header("Thresholding, Edge Detection and Contours")
    img=st.file_uploader('Upload images')
    if img is not None:
        image=Image.open(img)
        col1,col2=st.columns([0.5,0.5])
        with col1:
            st.markdown('<p style="text-align:center;">Original</p>',unsafe_allow_html=True)
            st.image(image,caption='Original Image')

        with col2:
            st.markdown('<p style="text-align:center;">Grayscale</p>',unsafe_allow_html=True)
            converted_img=np.array(image.convert('RGB'))
            gray_scale=cv2.cvtColor(converted_img,cv2.COLOR_RGB2GRAY)
            st.image(gray_scale,caption="GRAYSCALED IMAGE")

    
        x = st.slider('Change d:',min_value =0,max_value = 255)
        y = st.slider('Change sigmaColour',min_value =0,max_value = 255)
        z = st.slider('Change sigmaSpace',min_value =0,max_value = 255)
        thresh1 = cv2.bilateralFilter(gray_scale,x,y,z)
        st.image(thresh1, use_column_width=True,clamp = True)
            
        edged = cv2.Canny(thresh1,170,200)
        # Find contours based on Edges
        cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #Ok so here cnts is contours which means that it is like the curve joining all the points
        # Create copy of original image to draw all contours
        cv2.drawContours(edged, cnts, -1, (0,255,0), 3)
        #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
        cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
        NumberPlateCnt = None #we currently have no Number plate contour

        # Top 30 Contours
        cv2.drawContours(edged, cnts, -1, (0,255,0), 3)
        count = 0
        idx =7
        for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                # print ("approx = ",approx)
                if len(approx) == 4:  # Select the contour with 4 corners
                    NumberPlateCnt = approx #This is our approx Number Plate Contour

                    # Crop those contours and store it in Cropped Images folder
                    x, y, w, h = cv2.boundingRect(c) #This will find out co-ord for plate
                    new_img =thresh1 [y:y + h, x:x + w] #Create new image
                    cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img) #Store new image
                    idx+=1

                    break
        
        st.title("CLick to see the final output")
        if(st.button('OUPUT')):
            Cropped_img_loc = 'Cropped Images-Text/7.png'
            st.image(Cropped_img_loc, use_column_width=True,clamp = True)
            text=pytesseract.image_to_string(Cropped_img_loc,lang='eng')
            st.title(text)



if selected_box == 'Welcome':
    # welcome() 
    welcome()    
if selected_box == 'Image Processing':
    # photo()
    photo()