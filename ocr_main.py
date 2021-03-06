from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pytesseract import pytesseract ,Output # using pytesseract as tess
from PIL import Image
from adrear import *
from adfront import *
from PANCARD_OCR_function import *
from voter_rear import *
from voter_front import *
app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
UPLOAD_FOLDER='./uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route("/", methods = ['GET', 'POST'])
def home():
    prop = {}
    res = {}
    if request.method == 'POST':
        f = request.files['file']
        key = request.form.get('var')
        img = Image.open(f.stream)
        config = r'--oem 3 --psm 6'  ## works well
        if key == '1':## Aadhaar Rear side to get pincode,state,town and address
            img_rear = get_img1(img)
            d = pytesseract.image_to_data(img_rear, lang='eng', output_type=Output.DICT, config=config)
            res = get_result1(d)
            return jsonify(res)
        elif key == '2':
            name_front = get_name_img(img)
            img_front =  get_img2(img)
            d = pytesseract.image_to_data(img_front, lang='eng', output_type=Output.DICT, config=config)
            res = {}
            res = get_result2(d)
            res['name'] = get_name2(d)
            return jsonify(res)
        elif key == '3': #PAN CARD OCR
            res = panocr(img)
            return jsonify(res)
        elif key == '4': #VOTERID OCR REAR
            data = Voter_IDREAR(img)
            return jsonify(data)
        elif key == '5': # Voter ID front
            data = Voter_IDFRONT(img)
            return jsonify(data)

    return render_template('index.html')

            


if __name__ == '__main__':
    app.run(debug=True)