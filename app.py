# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 05:20:10 2021

@author: jawah
"""

from flask import Flask, render_template, request
import jsonify
import requests
import sklearn
import pickle

app = Flask(__name__)
model = pickle.load(open('model_rf.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods= ['POST'])
def predict():
    if request.method == 'POST':
        national_inv = int(request.form['national_inv'])
        lead_time = int(request.form['lead_time'])
        in_transit_qty = int(request.form['in_transit_qty'])
        forecast_3_month = int(request.form['forecast_3_month'])
        sales_1_month = int(request.form['sales_1_month'])
        min_bank = float(request.form['min_bank'])
        potential_issue = request.form['potential_issue']
        if(potential_issue =='Yes'):
            potential_issue=1
        else:
            potential_issue=0
        perf_6_month_avg = float(request.form['perf_6_month_avg'])
        deck_risk = request.form['deck_risk']
        if(deck_risk =='Yes'):
            deck_risk=1
        else:
            deck_risk=0
        oe_constraint = request.form['oe_constraint']
        if(oe_constraint =='Yes'):
            oe_constraint=1
        else:
            oe_constraint=0
        ppap_risk = request.form['ppap_risk']
        if(ppap_risk =='Yes'):
            ppap_risk=1
        else:
            ppap_risk=0
        stop_auto_buy = request.form['stop_auto_buy']
        if(stop_auto_buy =='Yes'):
            stop_auto_buy=1
        else:
            stop_auto_buy=0
        rev_stop = request.form['rev_stop']
        if(rev_stop =='Yes'):
            rev_stop=1
        else:
            rev_stop=0
        
        prediction=model.predict([[national_inv,lead_time,in_transit_qty,forecast_3_month,sales_1_month,min_bank,
                                   potential_issue,perf_6_month_avg,deck_risk,oe_constraint,ppap_risk,stop_auto_buy,rev_stop]])
        if prediction==1:
            return render_template('result.html', prediction_text= "That Product will be purchased again",
                                   message= "So, we should keep more stock of this product. Otherwise we will lose the trust of the customer ")
        else:
            return render_template('result.html', prediction_text= "That Product will not be purchased again",
                                   message= "So, we don't have to keep more stock of this product and that will help us to avoid some financial loss ")
    
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
    