from flask import render_template, redirect,url_for,request,flash,abort,jsonify
from flask.helpers import make_response
from diseasePrediction.models import Users,Diseases
from diseasePrediction import app,db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user,login_required
from diseasePrediction.AImodel import NaiveBayes


@app.route('/',methods=['POST','GET'])
def home():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/prediction',methods=['POST','GET'])
@login_required
def prediction():
    return render_template('prediction.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    return render_template('signup.html')

@app.route('/profile',methods=['POST','GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='GET':
        return "send symptoms here"
    symptoms=request.get_json()
    symptom1=symptoms['symptom1']
    symptom2=symptoms['symptom2']
    symptom3=symptoms['symptom3']
    symptom4=symptoms['symptom4']
    symptom5=symptoms['symptom5']
    symptom6=symptoms['symptom6']

    disease=NaiveBayes(symptom1,symptom2,symptom3,symptom4,symptom5,symptom6)
    if(disease!='Not Found'):
        addDisease=Diseases(name=disease,user_id=current_user.id)
        db.session.add(addDisease)
        db.session.commit()
    response = jsonify({'disease': disease})
    response.headers.add('Access-Control-Allow-Origin', 'true')
    return response


@app.route('/register',methods=['POST','GET'])
def register():
    userinfo=request.get_json()
    name=userinfo['username']
    email=userinfo['email']
    passwd=userinfo['passwd']
    useremail=Users.query.filter_by(email=email).first()
    userusername=Users.query.filter_by(name=name).first()
    if useremail or userusername:
        return make_response(jsonify({"result":"failure"}),400)
    hashed_password=generate_password_hash(passwd, method='sha256')
    new_user=Users(name=name,email=email,passwd=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({"result":"success"}),200)


@app.route('/get-userinfo',methods=['GET','POST'])
def getUserInfo():
    if(current_user.is_authenticated):
        currentUserInfo={
            "authenticated":current_user.is_authenticated,
            "name":current_user.name,
        }
    else:
        currentUserInfo={
            "authenticated":current_user.is_authenticated,
            "name":"",
        }
    return jsonify(currentUserInfo)



@app.route('/loginData',methods=['POST','GET'])
def loginData():
    userData=request.get_json()
    username=userData['username']
    passwd=userData['passwd']
    user=Users.query.filter_by(name=username).first()
    if user:
        if check_password_hash(user.passwd,passwd):
            login_user(user)
            return make_response(jsonify({'result':'success'}),200)
        else:
            return make_response(jsonify({'result':'failure'}),400)
    else:
        return make_response(jsonify({'result':'failure'}),400)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



@app.route('/profileData')
def profileData():
    diseases=Diseases.query.filter_by(user_id=current_user.id).all()
    diseasesJSON={
        "username":current_user.name,
        "diseases":[]
    }
    for disease in diseases:
        diseaseJSON={"name":disease.name,"date":disease.date_predicted}
        diseasesJSON['diseases'].append(diseaseJSON)
    return jsonify(diseasesJSON)
