import os
import json
import cv2 # OpenCV2
import numpy as np
from PIL import Image
import base64
import re
import imutils

def get_img2(img):
    filename2 = './uploads/img.png'
    img = cv2.imread(filename2)
    dim = (800, 600)
    img = cv2.resize(img, dim, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    rotated = img[135: 260 + 265, 10:190 + 530]
    cv2.imwrite(filename2, rotated)
    return rotated

def get_name_img(img):
    filename2 = './uploads/img.png'
    filename3 = './uploads/name.png'
    img.save(filename2, dpi=(300, 300))
    img = cv2.imread(filename2)
    dim = (800, 600)
    img = cv2.resize(img, dim, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    im = img[150:275, 10:190 + 520]
    cv2.imwrite(filename3, im)
    return im


def get_result2(d):
    res = {}
    text = ""
    text2 = []
    z = 0
    for i in d['text']:
        if int(d['conf'][z]) > 50:
            text2.append(i)
            text = text + i + " "
        z = z + 1
    res['DOB'] = get_dob2(text)
    if res['DOB'] == "":
        l = len(text2)
        for i in text2:
            if "Year of Birth" or 'Birth' in i:
                index1 = text2.index(i)
                if (index1 + 1) < l:
                    if text2[index1 + 1].isdigit() and (
                            int(text2[index1 + 1]) >= 1940 and (int(text2[index1 + 1]) < 2018)):
                        res['DOB'] = text2[index1 + 1]
                        break
                if (index1 + 2) < l - 2:
                    if text2[index1 + 2].isdigit() and (
                            int(text2[index1 + 2]) >= 1940 and (int(text2[index1 + 2]) < 2018)):
                        res['DOB'] = text2[index1 + 2]
                        break

    res["Gender"] = get_gender2(text2)
    return res

def get_gender2(lines):
    gender = ""
    try:
        for i in lines:
            if i.startswith('FE') or i.startswith("Female") or i.startswith("/F"):
                gender = 'Female'
                break
            elif i.startswith("MA") or i.startswith("Male") or i.startswith("/M"):
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

def get_dob2(l):
    all = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", l)
    s = ""
    for i in all:  # TODO make a sperate function for DOB
        s = s + i
    return s

def refine2(lis):
    lis = [item for item in lis if item.isalpha()]
    c = 0
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    pattern = re.compile('[A-Z]+[a-z]+$')
    things = ["DOB","of","Birth","Year","Male","Female","FEMALE","MALE","Father","Date"]
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
            if sum(1 for c in i if c.isupper())>2:#Count the no of Capital Letters
                lis.remove(i)

    final = []
    for i in lis:
        if not i in things:
            final.append(i)
            continue
    return final


def get_name2(d2):
    tt = []
    z = 0
    for j in d2['text']:
        if int(d2['conf'][z]) > 50:
            tt.append(j)
        z = z + 1
    if len(tt) >= 1:
        tt = refine2(tt)
        name = ""
        if len(tt) >= 1:
            name = name + tt[0] + " "
        else:
            name = "NOT FOUND"
        if len(tt) >= 2:
            name = name + tt[1] + " "
        if len(tt) >= 3:
            name = name + tt[2]
        return name
    else:
        return "NOT FOUND "

