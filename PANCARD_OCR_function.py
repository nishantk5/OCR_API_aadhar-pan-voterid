# import the necessary packages
import os
import cv2
import pytesseract
import numpy as np
import re
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
def get_dob(txt):
    try:
        match = re.search(r'(\d+/\d+/\d+)',txt)
        return(match.group(1))
    except:
        return("None")   

def get_pan(txt):
    try:
        match = re.search(r'\b([A-Z]+[0-9]+|[0-9]+[A-Z]+)[A-Z0-9]*\b', txt)
        return(match.group(1))
    except:
        return("None")           

def get_name(txt):
    try:
        result = re.findall(r"[A-Z ]+", txt)
        if result[0]!=' ':
            return(result[0])        
    except:
        pass

def panocr(image):
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = ('-l eng --oem 1 --psm 3')
    dim = (550, 400)
    open_cv_image = np.array(image)
    # Convert RGB to BGR
    img = open_cv_image[:, :, ::-1].copy()
    img = cv2.resize(image, dim, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray, 120, 220, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(gray, config=config)
    # print(text)
    text1=[]
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    textlist = list(filter(None, text1))
    pantextlist = list(filter(None, text1))
    # print(textlist)

    name=[]
    for item in textlist:
        #print(item)
        remove_lower = lambda text: re.sub('[a-z]', '', item)
        if remove_lower:
            textlist.remove(item)
        name.append(get_name(item))
    name = list(filter(None, name))  
    # print(name)
    for item in name:  
        if item.find("INCOME")!=-1:
            name.remove(item)
        if item.find("GOVT")!=-1:
            name.remove(item)    
    # print(name)                             
                    
    pan=''
    alphanumeric =''
    for item in pantextlist:
        if (get_pan(item))!='None':
            pan = item
    for character in pan:
        if character.isalnum():
            alphanumeric += character        

    data = {}
    try:
        data['Name'] = name[0]
    except:   
        data['Name'] = ''         
    data['Date of Birth'] = get_dob(text)        
    data['PAN'] = alphanumeric
    return(data)

# panocr(Image.open("p6.jpeg"))
