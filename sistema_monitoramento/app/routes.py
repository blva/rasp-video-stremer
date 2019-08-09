from flask import render_template, flash, redirect
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
        return redirect('/reboot')
    return render_template('login.html', title='Sign In', form=form)

if __name__ == "__main__":
    app.run(debug=True)