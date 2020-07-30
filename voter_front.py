import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

def Voter_IDFRONT(img):
    dim = (500, 400)
    open_cv_image = np.array(img)
    # Convert RGB to BGR
    img = open_cv_image[:, :, ::-1].copy()
    img = cv2.resize(img, dim, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    # crop_img = rotated[150:180 + 230, 189:259 + 450]
    crop_img = img[200:, :]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    d = pytesseract.image_to_data(gray, lang='eng', output_type=Output.DICT, config=config)
    tt = []
    z = 0
    text = ""
    for j in d['text']:
        if int(d['conf'][z]) > 10:
            tt.append(j)
            text = text + j
        z = z + 1
    res = {}
    res['Name'] = get_name5(tt)
    res['Father name'] = get_father_name5(tt)
    res['DOB'] = get_dob5(text)
    res["Gender"] = get_gender5(tt)
    return res



def get_name5(tt):
    s = ""
    tt = refine5((tt))
    for i in tt:
        if i.startswith("Name"):
            index = tt.index(i)
            if tt[index + 1] == ":":
                s = s+tt[index + 2].strip() + " " + tt[index + 3].strip()
                i = tt[index + 4]
                if sum(1 for c in i if c.isupper()) == 1:  # Count the no of Capital Letters:
                    s = s + " " + tt[index + 4].strip()
                break
            else:
                s = s+tt[index + 1].strip() + " " + tt[index + 2].strip()
                i = tt[index + 3]
                if sum(1 for c in i if c.isupper()) == 1:  # Count the no of Capital Letters:
                    s = s+ " " + tt[index + 3].strip()

                break
    if s == "":
        s = "NOT FOUND"
    return s
def get_father_name5(tt):
    d = ""
    tt = refine5((tt))
    for i in tt:
        if i.startswith("Father"):
            index = tt.index(i)
            if tt[index + 2] == ":":
                d = d+tt[index + 3].strip() + " " + tt[index + 4].strip()
                i = tt[index + 5]
                if sum(1 for c in i if c.isupper()) == 1:  # Count the no of Capital Letters:
                    d = d + " " + tt[index + 4].strip()
                break
            else:
                d = d+tt[index + 2].strip() + " " + tt[index + 3].strip()
                i = tt[index + 3]
                if sum(1 for c in i if c.isupper()) == 1:  # Count the no of Capital Letters:
                    d = d + " " + tt[index + 3].strip()
    if d == "":
        return 'NOT FOUND'
    else:
        return d

def get_gender5(lines): # Retreivng gender
    gender = ""
    try:
        for i in lines:
            if i.startswith('FE') or i.startswith("Female") or i.startswith("/F") or i.startswith("Fe"):
                gender = 'Female'
                break
            elif i.startswith("MA") or i.startswith("Male") or i.startswith("Ma") or i.startswith("=Ma") :
                gender = 'Male'
                break
            else :
                pass
    except:
        pass
    if gender == "":
        return"NOT FOUND"
    else :
        return gender

def get_dob5(l):
    all = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", l)
    s = ""
    for i in all:  # TODO make a sperate function for DOB
        s = s + i
    return s

def refine5(lis):
    c = 0
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~]')
    pattern = re.compile('[A-Z]+[a-z]+$')
    things = ["DOB","of","Birth","Year","Male","Female","FEMALE","MALE","Date"]# Removing unwanted strings
    for i in lis:
            i = str(i)
            if i[0].islower() :
                lis.remove(i)
                continue
            if i == " ":
                lis.remove(i)
                continue
            if not (regex.search(i) == None):
                lis.remove(i)
                continue

    final = []
    for i in lis:
        if not i in things:
            final.append(i)
            continue
    return final
