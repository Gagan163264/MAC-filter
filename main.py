
from flask import Flask, render_template, redirect, url_for, request, session, flash
from macfilter import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

pwd = "pwd.txt"
scheduler = BackgroundScheduler()
scheduler.configure(timezone="utc")
job = scheduler.add_job(cleaner, 'interval', days=1)
scheduler.start()

def loadpwd():
    pwdf = "pwd.txt"
    try:
        with open(pwdf, 'r') as file:
            #config = json.loads(file.read())
            config = json.loads(decrypt(file.read()))
    except IOError:
        config = {}
    return config

@app.route('/home', methods=['GET', 'POST'])
def home():
    user_id = request.cookies.get('SessionCookie')
    if user_id in session:
        if request.method == 'POST':
            if request.form['sbtn'] == 'Add Record':
                return redirect(url_for('add'))
            elif request.form['sbtn'] == 'Delete Record':
                return redirect(url_for('remove'))
            else:
                return redirect(url_for('update'))
        return render_template('home.html', response = displayMAC())
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = request.cookies.get('SessionCookie')
    if user_id in session:
        response = None
        if request.method == 'POST':
            name = request.form['name']
            MAC = request.form['MAC']
            phno = request.form['mob']
            nmon = request.form['nmon']
            print(name, MAC, phno)
            addMAC([phno,MAC,name,nmon])
            return redirect(url_for('home'))
        return render_template('add.html', response=response)
    else:
        return redirect(url_for('login'))

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    user_id = request.cookies.get('SessionCookie')
    if user_id in session:
        response = ''
        if request.method == 'POST':
            MAC = request.form['MAC']
            phno = request.form['mob']
            if not delMAC([phno, MAC]):
                response = "No matching record found"
            else:
                response = "Record deleted\n\n\n"
                return redirect(url_for('home'))
        return render_template('remove.html', response=response+displayMAC())
    else:
        return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    user_id = request.cookies.get('SessionCookie')
    if user_id in session:
        response = ''
        if request.method == 'POST':
            MAC = request.form['MAC']
            phno = request.form['mob']
            nmon = request.form['nom']
            val =  updateMAC([phno, MAC,nmon])
            if val[0]==0:
                response = "No matching record found\n\n\n"
            elif val[0]==-1:
                response = "Cannot remove previous and current month\n\n\n"
            else:
                if val[1]>0:
                    response = "Accept cost of "+str(val[1])+" months"
                else:
                    response = "Refund cost of "+str(-1*val[1])+" months"
                response+="\n\n\n"
        return render_template('update.html', response=response+displayMAC())
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    pwd=loadpwd()
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        if uname not in pwd.keys() or password != pwd[uname][0]:
            error = 'Invalid Credentials. Please try again.'
        else:
            response = redirect(url_for('home'))
            response.set_cookie('SessionCookie', uname, max_age = 600)
            session[uname]='USERNAME'
            return response
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
