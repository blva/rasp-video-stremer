from flask import render_template, flash, redirect, Response
from app import app
from app.forms import LoginForm
from app.camera import VideoCamera

import numpy as np
from datetime import datetime

timestamps = np.zeros(100)
i = 0

@app.route('/')
def home():
    return redirect('/connect')

@app.route('/reboot')
def reboot():
    return "Aguarde enquanto o sistema reinicia e conecte-se em sua rede local"

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/video_feed')
    return render_template('login.html', title='Sign In', form=form)

def gen(camera):
    global i
    global timestamps
    while True:
        frame = camera.get_frame()
        if i < 100:
            timestamps[i] = datetime.timestamp(datetime.now())
            i += 1
        if i == 100:
            print(np.mean(1/np.diff(timestamps)))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    render_template('stream.html')
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
