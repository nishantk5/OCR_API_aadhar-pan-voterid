from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
import os
import cv2 # OpenCV2
import numpy as np
from PIL import Image
import base64
import re

def get_address(lis):
    st = ""
    for i in lis:
        st = st+" "+i
    return st

def get_img1(img):
    dim = (800, 600)#Resizing the image
    open_cv_image = np.array(img)
    # Convert RGB to BGR
    img = open_cv_image[:, :, ::-1].copy()
    img = cv2.resize(img, dim, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    rotated = img[120: 285 + 265, 260:190 + 600]#Croping the image to English written Address in Aadhar
    return rotated

def get_result1(d):
    z = 0
    text2 = []
    text = ""
    for i in d['text']:
        if int(d['conf'][z]) > 80:
            text2.append(i)
            text = text + i
        z = z + 1

    res = {}
    for i in text2:
        add = ""
        z = text2.index(i)
        if i.isdigit() and len(i) == 6:# Matching for Pincode
            res["Pincode"] = i
            res["Address"] = get_address(text2[1:z - 1])
            pincode = geolocator.geocode(res["Pincode"])# Calling Geopy to get the town,state etc.
            address = str(pincode.address)
            try:
                lis = address.split(",")
                res['Country'] = lis[-1]
                res['State'] = lis[-3]
                if res['State'] == "Karnataka":
                    for j in lis:
                        if 'taluk' in j:
                            res['Town'] = str(j)
                            if 'district' in j:
                                res['District'] = str(j)
                else:
                    res['City'] = lis[-4]
            except:
                res['Error'] = "Can't able to get the details"
    return res
