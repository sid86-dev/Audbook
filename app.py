from flask import Flask, render_template, request, send_file, abort
from werkzeug.utils import secure_filename
from os import walk
from gtts import gTTS
import PyPDF2

import os
import json

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = params['upload_location']

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/extraction", methods=["GET", "POST"])
def extraction():
    dir = "static/pdfs"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = "static/Audio"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

        # saving file

    if request.method == "POST":
        f = request.files['file1']
        f.save(os.path.join(
        app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # main function
        filenames = next(walk(app.config['UPLOAD_FOLDER']), (None, None, []))[2] 
        a = filenames[0]   
        b = a.split(".")
        c = b[0]
        filename_read = c + ".pdf"
        filename_audio = c 
        app.config['GET_FOLDER'] = f"C:\\SID PROGRAMMER\\Audbook\\static\\pdfs\\{filename_read}"
        loc = app.config['GET_FOLDER']
        read = PyPDF2.PdfFileReader(loc)

        pages = read.numPages
        text=""
        for n in range(0, pages):
            text = text + read.getPage(n).extractText()

        analyzed_text = ""
        punctions = '''"#$%&'()*+-/:;<=>?@[\]^_`{|}~™˜˚˛˝˙ˆ˚ˇˇ˘'''
        for char in text:
            if char not in punctions:
                analyzed_text = analyzed_text + char

        realanyzed_text = ""
        for char in analyzed_text:
            if char != "\n" and char != "\r":
                realanyzed_text = realanyzed_text + char

        print(realanyzed_text)
        # save as audio
        app.config['DOWNLOAD_FOLDER'] = f"C:\\SID PROGRAMMER\\Audbook\\static\\Audio\\{filename_audio}.mp3"
        app.config['AUDIO_FOLDER'] = f"C:\\SID PROGRAMMER\\Audbook\\static\\Audio\\{filename_audio}.mp3"
        language = 'en'
        speaker = gTTS(text=realanyzed_text, lang=language, slow=False)
        speaker.save(app.config['AUDIO_FOLDER'])
        loc = f"\static\Audio\{filename_audio}.mp3"
        print(loc)
    return render_template('extraction.html', output1=realanyzed_text, audio=loc)

    
@app.route("/download")
def download():
    try:
        return send_file(app.config['DOWNLOAD_FOLDER'] , as_attachment=True)
    except FileNotFoundError:
        abort(404)
if __name__ == "__main__":
    app.run(debug=True)