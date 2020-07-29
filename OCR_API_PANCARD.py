# import the necessary packages
import os
from flask import Flask, request, render_template
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

#specify the default folder from where the files will be selected and uploaded
PROJECT_HOME = os.path.dirname(os.path.realpath("C:\\Users\\91933\\DHIYO EVERYTHING"))
UPLOAD_FOLDER  = '{}\\DHIYO EVERYTHING'.format(PROJECT_HOME)

#folder uploaded
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

#to access that particular folder to upload the files and display it in this format
@app.route("/", methods=['GET','POST'])
def upload():
    return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="/success" method="post" enctype="multipart/form-data">
          <p><input type="file" name="file"/>
             <input type="submit" value="Upload">
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'], ))

#main logic to process the OCR on the uploaded file and display it on the local website by rendering the html template
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = request.files['file']
        name=f.filename
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'    
    im = cv2.imread(name)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(gray, config=config)
    print(text)

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
    print(data) 
    return render_template("success.html", text= data) 

if __name__ == "__main__":
    app.debug = False
    app.run()
