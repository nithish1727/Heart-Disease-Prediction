from flask import Flask, render_template, request, flash,url_for,session,redirect
import joblib
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

app = Flask(__name__)

app.secret_key = "dshdkashkdjhkj"

ML_models = joblib.load('static/ML_Models.pkl')

code_github_link = "https://github.com/Nithish2032/Heart-disease-prediction"
heart_disease_info_link = "https://en.wikipedia.org/wiki/Cardiovascular_disease"
tutorial_link =""

packet={}
packet['website-name'] ="Heart Disease Predictor"
packet['nav-items'] = ['Home','Analytics','Code','Info','About','Tutorial']

packet['contacts']  = [
    {'name':'Kandepi Nithish',
    'id' : "2021H1030103H",
     'email':'h20211030103@hyderabad.bits-pilani.ac.in'},
    {'name':'Chaitanya Gollapudy',
     'id' : "2021H1030091H",
     'email':'h20211030091@hyderabad.bits-pilani.ac.in m'},
    {'name':'Jagruti Omprakash holani',
     'id' : "2021H1030122H",
     'email':'h20211030122@hyderabad.bits-pilani.ac.in '}
]


def is_float(num) :
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_features():
    errors = []
    features = {}
    print(request.form)
    Age = request.form['Age']
    RestingBP = request.form['RestingBP']
    MaxHR = request.form['MaxHR']
    OldPeak = request.form['OldPeak']
    Cholesterol = request.form['Cholesterol']


    #Age
    if not Age.isnumeric() or not 1 <= float(Age) <= 125 : 
        errors.append("Enter a valid age.")
    else:
        features['age'] = float(request.form['Age'])

    #resting_blood_pressure
    if not RestingBP.isnumeric() or not 50 <= float(RestingBP) <= 200: 
        errors.append("Enter a valid resting BP.")
    else:
        features['resting_blood_pressure'] = float(request.form['RestingBP'])

    #cholesterol
    if not Cholesterol.isnumeric() or not 0 <= float(Cholesterol) <= 500: 
        errors.append("Enter a valid cholesterol.")
    else:
        features['cholesterol'] = float(request.form['Cholesterol'])

    #fasting_blood_sugar
    features['fasting_blood_sugar'] = float(request.form['FBS'])

    #max_heart_rate_achieved
    if not MaxHR.isnumeric() or not 50 <= float(MaxHR) <= 200: 
        errors.append("Enter a valid heart rate.")
    else:
        features['max_heart_rate_achieved'] = float(request.form['MaxHR'])
    
    #exercise_induced_angina
    features['exercise_induced_angina'] = float(request.form['ExAngina'])

    #st_depression
    if not (OldPeak.isnumeric() or is_float(OldPeak)) or not -10 <= float(OldPeak) <= 10: 
        errors.append("Enter a valid old peak.")
    else:
        features['st_depression'] = float(request.form['OldPeak'])

    #sex_male
    features['sex_male'] = int(request.form['Sex'])
    
    #chest_pain_type_Atypical Angina
    if int(request.form['ChestPain']) == 1:
        features['chest_pain_type_Atypical Angina'] = 1
    else:
        features['chest_pain_type_Atypical Angina'] = 0

    #chest_pain_type_Non-anginal Pain
    if int(request.form['ChestPain']) == 2:
        features['chest_pain_type_Non-anginal Pain'] = 1
    else:
        features['chest_pain_type_Non-anginal Pain'] = 0
    
    #chest_pain_type_Typical Angina
    if int(request.form['ChestPain']) == 0:
        features['chest_pain_type_Typical Angina'] = 1
    else:
        features['chest_pain_type_Typical Angina'] = 0
    
    #rest_ecg_Normal
    if int(request.form['RESTECG']) == 0:
        features['rest_ecg_Normal'] = 1
    else:
        features['rest_ecg_Normal'] = 0
    
    #rest_ecg_ST-T wave abnormality
    if int(request.form['RESTECG']) == 1:
        features['rest_ecg_ST-T wave abnormality'] = 1
    else:
        features['rest_ecg_ST-T wave abnormality'] = 0
    
    #st_slope_Flat
    if int(request.form['STSlope']) == 1:
        features['st_slope_Flat'] = 1
    else:
        features['st_slope_Flat'] = 0

    #st_slope_Upsloping
    if int(request.form['STSlope']) == 0:
        features['st_slope_Upsloping'] = 1
    else:
        features['st_slope_Upsloping'] = 0


    return errors,features

def predict_heart_disease(features):
    for key,val in features.items():
        features[key] = [val]

    print("-"*30)
    print(features.values())
    print("-"*30)
    
    df = pd.DataFrame(features)
    print(df)
    predicted = ML_models['soft_voting_model'].predict(df)[0]
    print("Predicted "+str(predicted))

    if predicted == 0:
        result = "No heart disease present"
    else:
        result = "Heart disease present"

    for key,value in ML_models.items():
        predicted = value.predict(df)[0]
        print(key,predicted)

    return result


@app.route("/",methods=['GET','POST'])
@app.route("/Home",methods=['GET','POST'])
def home():
    packet['current-page'] = 'Home'

    if request.method == 'POST':
        errors,features = get_features()
        if not errors:   
            packet['predict'] = predict_heart_disease(features)
        packet['errors'] = errors
        
    else:
       packet['predict'] = ""   

    print(packet)

    return render_template("index.html",packet=packet)

@app.route("/Analytics")
def Analytics():
    packet['current-page'] = 'Analytics'
    flash("This is nome")
    return render_template("analytics.html",packet=packet)

@app.route("/Code")
def Code():
    return redirect(code_github_link) 


@app.route("/Info")
def Info():
    return redirect(heart_disease_info_link)

@app.route("/About")
def About():
    packet['current-page'] = 'About'
    return render_template("about.html",packet=packet)

@app.route("/Tutorial",methods=['GET','POST'])
def Tutorial():
    packet['current-page'] = 'Tutorial'
    packet['tutorial_link'] = tutorial_link
    return render_template("tutorial.html",packet=packet)


if __name__=="__main__":
    app.run(debug=True)
    