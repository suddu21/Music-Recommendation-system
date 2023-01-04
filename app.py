from flask import Flask, request, render_template,redirect,url_for
import pandas as pd
from recommend import rec
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login_form():
    error = None
    if request.method == 'POST':
        user=request.form['user']
        password=request.form['password']

        try:
            with open('credentials.json') as fp:
                creds=json.loads(fp.read())
            if user not in creds.keys():
                error = 'Invalid Credentials. Please try again.'
            elif creds[user] != password:
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect('/template')
        except:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)



@app.route('/registration')
def registration():
    return render_template('registration.html')



@app.route('/registration', methods=['GET', 'POST'])
def registration_form():
    error=None
    user = request.form['user']
    password = request.form['password']

    try:
        with open('credentials.json') as credentials:
            creds = json.loads(credentials.read())
        if user in creds.keys():
            error = 'User already exists. Please try again.'
            return render_template('registration.html', error=error)
        creds[user]=password
    except:
        creds = {}
        creds[user]=password
    with open("credentials.json", "w") as fp:
        json.dump(creds,fp)

    """with shelve.open('users') as db:
        db[email] = password"""

    return redirect('/login')



@app.route('/template')
def template():
    return render_template('template.html')



@app.route('/template', methods=['POST'])
def my_form_post():
    text = request.form['text']
    file = open('song.txt','w')
    file.write(str(text))
    file.close()
    #subprocess.call(["python3", "recommend.py",'{}'.format(text)])
    rec()
    return redirect('/upload')



@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    with open ("song.txt", "r") as myfile:
        data=myfile.readlines()
    #print(str(data[0]))
    data=pd.read_csv('songs.csv')
    return render_template('view.html',tables=[data.to_html(classes='name',index=False)],titles = ['Songs'])



if __name__=='__main__':
    app.run()