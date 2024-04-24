from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField ,FileField

import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

class audioForm(FlaskForm):
    audio = FileField("Audio File")
    submit = SubmitField("Extract") 


todo = ["1","1"]
@app.route('/',methods = ["POST",'GET'])
def index():
    return render_template("index.html")


@app.route('/summarize_audio',methods = ["POST",'GET'])
def audio():
    if request.method == 'POST':
        res = request.values.get('audio')
        print(res)
    else :
        res = "Please enter your data"
    return render_template("form.html" , template_form = audioForm() , res = res)



@app.route('/summarize_video',methods = ["POST",'GET'])
def video():
    if request.method == 'POST':
        res = request.values.get('audio')
        print(res)
    else :
        res = "Please enter your data"
    return render_template("form.html" , template_form = audioForm() , res = res)



if __name__ == '__main__':
    app.run(debug=True)
