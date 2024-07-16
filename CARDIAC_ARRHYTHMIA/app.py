from flask import Flask, render_template, request, flash, redirect
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
import pickle
knn=pickle.load(open("model/model.pkl","rb"))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            import requests
            import pandas as pd
            data=requests.get("https://api.thingspeak.com/channels/2484579/feeds.json?api_key=O2NSHRKEY803DCTN&results=2")
            hb=data.json()['feeds'][-1]['field1']
            temp=data.json()['feeds'][-1]['field2']
            ecg=data.json()['feeds'][-1]['field3']
            print(f"heart beat : {hb} \n temperature : {temp} \n ECG : {ecg}")
            return render_template('fetal.html',hb=hb,temp=temp,ecg=ecg)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided Patient,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Patient Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/specialists')
def specialists():
    return render_template('doctors.html')

@app.route("/fetalPage", methods=['GET', 'POST'])
def fetalPage():
    import requests
    import pandas as pd
    data=requests.get("https://api.thingspeak.com/channels/2484579/feeds.json?api_key=O2NSHRKEY803DCTN&results=2")
    hb=data.json()['feeds'][-1]['field1']
    temp=data.json()['feeds'][-1]['field2']
    ecg=data.json()['feeds'][-1]['field3']
    print(f"heart beat : {hb} \n temperature : {temp} \n ECG : {ecg}")
    return render_template('fetal.html',hb=hb,temp=temp,ecg=ecg)




@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        Gender = request.form['Gender']
        height = request.form['height']
        Weight = request.form['Weight']
        ECG = request.form['ECG']
        Heart_Rate = request.form['Heart_Rate']
        Temperature = request.form['Temperature']
        data = np.array([[age, Gender, height, Weight, ECG, Heart_Rate, Temperature]])
        my_prediction = knn.predict(data)
        result = my_prediction[0]
        
        print(result)

        
        if result == 1 :
            res='Normal'
        elif result == 2: 
            res='Ischemic changes (Coronary Artery)'
        elif result == 3:
            res='Old Anterior Myocardial Infarction'
        elif result == 4:
            res='Old Inferior Myocardial Infarction'
        elif result == 5:
            res='Sinus tachycardia'
        elif result == 6:
            res='Ventricular Premature Contraction (PVC)'
        elif result == 7:
            res='Supraventricular Premature Contraction'
        elif result == 8:
            res='Left bundle branch block'
        elif result == 9 :
            res='Right bundle branch block'
        elif result == 10:
            res='Left ventricle hypertrophy'
        elif result == 14:
            res='Atrial Fibrillation or Flutter'
        elif result == 15:
            res='Others1'
        elif result == 16:
            res='Others2' 
        print(res)

           
        return render_template('predict.html',name=name, pred = result,status=res)

    return render_template('predict.html')

if __name__ == '__main__':
	app.run(debug = True)