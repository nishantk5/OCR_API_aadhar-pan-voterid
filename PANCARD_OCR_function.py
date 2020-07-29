# import the necessary packages
import os
from imutils import paths
import cv2
import pytesseract
import numpy as np
import re

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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(image, config=config)

    text1=[]
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    textlist = list(filter(None, text1))
    pantextlist = list(filter(None, text1))

    name=[]
    for item in textlist:
        remove_lower = lambda text: re.sub('[a-z]', '', item)
        if remove_lower:
            textlist.remove(item)
        name.append(get_name(item))
    name = list(filter(None, name))  
    for item in name:  
        if item.find("INCOME")!=-1:
            name.remove(item)
        if item.find("GOVT")!=-1:
            name.remove(item)                         
                    
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
        data['Father Name'] = name[1]
    except:   
        data['Name'] = ''
        data['Father Name'] = ''         
    data['Date of Birth'] = get_dob(text)        
    data['PAN'] = alphanumeric
    return(data)
