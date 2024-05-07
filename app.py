from flask import Flask, render_template, request, flash ,redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField ,FileField
from werkzeug.utils import secure_filename
import os
import requests

from moviepy.editor import VideoFileClip


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
	  
UPLOAD_FOLDER = './static/files/'
ALLOWED_EXTENSIONS = { "mp4" , "mp3"}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + "/video"
app.config['EXTRACTED_FOLDER'] = UPLOAD_FOLDER + "/audio"



class audioForm(FlaskForm):
    audio = FileField("Audio File")
    submit = SubmitField("Extract") 
class videoForm(FlaskForm):
    audio = FileField("Audio File")
    submit = SubmitField("Extract") 




def textSummarizer(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()[0]['summary_text']

def VideotoAudio(mp4_file , mp3_file):
    # load the video
    print(mp4_file)
    print(mp3_file)
    video_clip = VideoFileClip(mp4_file)
    # Extract the audio from the video clip
    audio_clip = video_clip.audio
    # Write the audio to a separate file
    audio_clip.write_audiofile(mp3_file)

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()
    print("Audio extraction successful!")
    return  mp3_file

#  using whisper
def AudiotoText(text_file):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    with open(text_file, "rb") as f:
        data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()['text']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/',methods = ["POST",'GET'])
def index():
    return render_template("index.html")


@app.route('/summarize_audio',methods = ["POST",'GET'])
def audio():

    form = audioForm()
    if request.method == 'POST':
        summarize = 0 
        print(request.files)
        # check if the post request has the file part
        if 'audio' not in request.files:
            res = 'No file part'
            return redirect(request.url)
        file = request.files['audio']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            res = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.audio.data.save(file_path)
            result = AudiotoText(file_path)
            res =result
            summary = textSummarizer(res)

    else :
        res = "Please enter your data"
        summary = 0
    return render_template("form.html" , template_form = audioForm() , res = res , summary = summary)



@app.route('/summarize_video',methods = ["POST",'GET'])
def video():
    form = videoForm()
    if request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        if 'audio' not in request.files:
            res = 'No file part'
            return redirect(request.url)
        file = request.files['audio']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            res = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.audio.data.save(file_path)
            output_path = os.path.join(app.config['EXTRACTED_FOLDER'], filename[:-4] + ".mp3")
            VideotoAudio(file_path , output_path)
            res = AudiotoText(output_path)
            summary = textSummarizer(res)
            print(summary)
    else :
        res = "Please enter your data"
        summary = 0 
    return render_template("form.html" , template_form = videoForm() , res = res , summary = summary)



if __name__ == '__main__':
    app.run(debug=True)
