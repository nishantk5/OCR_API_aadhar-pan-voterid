import pytesseract
from pytesseract import Output
from PIL import Image
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
import cv2
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
def Voter_IDREAR(img):
    config = ('-l eng --oem 1 --psm 3')
    open_cv_image = np.array(img)
    # Convert RGB to BGR
    img = open_cv_image[:, :, ::-1].copy()
    d = pytesseract.image_to_data(img, lang='eng', output_type=Output.DICT, config=config)
    print(d)

    tt = []
    z = 0
    for j in d['text']:
        if int(d['conf'][z]) > 10:
            j = strs = re.sub(r'[?|$|.|!]',r'',j)
            tt.append(j)
        z = z + 1
    print(tt)
    res = get_result4(tt)

    return res


def get_address(lis):
    st = ""
    for i in lis:
        st = st + " " + i
    return st


def get_result4(d):
    res = {}
    for i in d:
        add = ""
        z = d.index(i)
        if i.isdigit() and len(i) == 6:
            res["Pincode"] = i
            res["Address"] = get_address(d[1:z - 1])
            pincode = geolocator.geocode(res["Pincode"])
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
