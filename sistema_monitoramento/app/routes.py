from flask import render_template, flash, redirect, Response
from app import app
from app.forms import LoginForm

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
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)