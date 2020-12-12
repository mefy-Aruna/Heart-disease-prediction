import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pickle
from numpy import math

from flask import session

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = "Secret"

model = pickle.load(open('RF1.pkl', 'rb'))
#json_file = open('model.json', 'r')

#loaded_model_json = json_file.read()
#json_file.close()

#loaded_model = model_from_json(loaded_model_json)

#loaded_model.load_weights("model9954.h5")
#print("Loaded model from disk")

@app.route('/')
def home():
    return render_template('index1.html')

##using ML
@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''

    if("text" == "M"):
        text = 0
    else:
        text =1

    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    
   # prediction = model.predict_proba(final_features)
    prediction =  model.predict(final_features)


    output = prediction[0]
    if output<0.7:
        output1='Normal'
    elif output>0.7:
        output1='10yr CHD risk'


    return render_template('index2.html', prediction_text='The Patient is {}'.format(output))

###using formula
@app.route('/predict1',methods=['POST'])
@cross_origin()
def predict1():
    '''
    For rendering results on HTML GUI
    '''
    
    #int_features = [float(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]
    totChol= request.form.get("Total Cholesterol")
    HDL = request.form.get("HDL")
    Dia= request.form.get("Diabetes")
    Smoke= request.form.get("Smoking")
    SBP = request.form.get("Systolic BP")
    Age = request.form.get("Age")
    hyp=request.form.get("antiHypertensive treatment")
    gender= request.form.get("Gender")
    session['totChol']= int(totChol)
    session['HDL']= int(HDL)
    session['Dia']=int(Dia)
    session['Smoke']= int(Smoke)
    session['SBP']= int(SBP)
    session['Age']= int(Age)
    session['hyp']=int(hyp)
    session['gender']=int(gender)
    
    if int(hyp)==1 and int(gender)==0:
        case=1
        result = math.exp((3.06117*math.log(int(Age)))+(1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99881*math.log(int(SBP)))-23.9802)
    elif int(hyp)==0 and int(gender)==0:
        case=2
        result = math.exp((3.06117*math.log(int(Age)))+(1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99303*math.log(int(SBP)))-23.9802)
    elif int( hyp)==1 and int(gender)==1:
        case=3
        result = math.exp((2.32888*math.log(int(Age)))+(1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.82263*math.log(int(SBP)))-26.1931)
    elif int(hyp)==0 and int(gender)==1:
        case=4
        result = math.exp((2.32888*math.log(int(Age)))+(1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.76157*math.log(int(SBP)))-26.1931)
    # if int(gender)==0:
    #         cvd = 1-(pow(0.88936,result))
    # elif int(gender)==1:
    #         cvd = 1-(pow(0.95012,result))
    if int(gender)==0:
            cvd = 1-(pow(0.88936,math.exp(result)))
    elif int(gender)==1:
            cvd = 1-(pow(0.95012,math.exp(result)))

    if case==1:
        heartAge = (1/math.exp(3.06117))* (math.log((math.log((1-cvd),0.88936))/(math.exp((1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99881*math.log(int(SBP)))-23.9802)    )))
    elif case==2:
        heartAge = (1/math.exp(3.06117))* (math.log(((math.log((1-cvd),0.88936))/(math.exp((1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99303*math.log(int(SBP)))-23.9802)))))
    elif case==3:
        heartAge = (1/math.exp(2.3288))* (math.log(((math.log((1-cvd),0.95012))/(math.exp((1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.82263*math.log(int(SBP)))-26.1931)))))
    elif case==4:
        heartAge = (1/math.exp(2.3288))* (math.log(((math.log((1-cvd),0.95012))/(math.exp((1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.76157*math.log(int(SBP)))-26.1931)))))
    heartAge1=round(100*heartAge,2)                 
    output=cvd
    if output<0.7:
        output1='Normal'
    elif output>0.7:
        output1='10yr CHD risk'

    session['cvdRisk']= int(output)
    session['case'] = int(case)
    
    return render_template('index3.html', prediction_text1='cvd risk result {}'.format(cvd),prediction_text2='Heart Age(in years)= {} '.format(heartAge1))

    #return render_template('index2.html', prediction_text='The Patient is {}'.format(heartAge))

###heart age

# @app.route('/predict2',methods=['POST'])
# @cross_origin()
# def predict2():
#     '''
#     For rendering results on HTML GUI
#     '''
#     cvd=session.get('cvdRisk')
#     case= session.get('case')
#     totChol=session.get('totChol')
#     HDL=session.get('HDL')
#     Dia=session.get('Dia')
#     Smoke=session.get('Smoke')
#     SBP=session.get('SBP')
#     # if case==1:
#     #     heartAge = (1/math.exp(3.06117))* ((math.log((1-cvd),0.88936))/(math.exp((1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99881*math.log(int(SBP)))-23.9802)))
#     # elif case==2:
#     #     heartAge = (1/math.exp(3.06117))* ((math.log((1-cvd),0.88936))/(math.exp((1.1237*math.log(int(totChol)))-(0.93263*math.log(int(HDL)))+(0.57367*int(Dia))+(0.65451*int(Smoke))+(1.99303*math.log(int(SBP)))-23.9802)))
#     # elif case==3:
#     #     heartAge = (1/math.exp(2.3288))* ((math.log((1-cvd),0.95012))/(math.exp((1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.82263*math.log(int(SBP)))-26.1931)))
#     # elif case==4:
#     #     heartAge = (1/math.exp(2.3288))* ((math.log((1-cvd),0.95012))/(math.exp((1.20904*math.log(int(totChol)))-(0.70833*math.log(int(HDL)))+(0.69154*int(Dia))+(0.52873*int(Smoke))+(2.76157*math.log(int(SBP)))-26.1931)))
                                         
#     return render_template('index3.html', prediction_text='Heart age ={}'.format(heartAge))
    
if __name__ == "__main__":
    app.run(debug=True) 