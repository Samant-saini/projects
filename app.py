from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))



@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        arr_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        arr_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Duration_hours = abs(arr_hour - dep_hour)
        Duration_mins = abs(arr_min - dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline=request.form['airline']
        if(airline=='Air_India'):
            Air_India = 1
            Vistara = 0
            

        # elif (airline=='Vistara'):
        #     Air_India = 0
        #     Vistara = 1
             

       
      
        

        
       
       
        else:
            Air_India = 0
            Vistara = 1
           

        # print(Jet_Airways,
        #     IndiGo,
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)

        # Source
        # Banglore = 0 (not in column)
        Source1 = request.form["Source"]
        if (Source1 == 'Bangalore'):
            Bangalore=1
            Chennai=0
            Delhi=0
            Hyderabad=0
            Kolkata=0
            Mumbai=0

        elif (Source1 == 'Chennai'):
            Bangalore=0
            Chennai=1
            Delhi=0
            Hyderabad=0
            Kolkata=0
            Mumbai=0

        elif (Source1 == 'Delhi'):
            Bangalore=0
            Chennai=0
            Delhi=1
            Hyderabad=0
            Kolkata=0
            Mumbai=0

        elif (Source1 == 'Hyderabad'):
            Bangalore=0
            Chennai=0
            Delhi=0
            Hyderabad=1
            Kolkata=0
            Mumbai=0
        elif (Source1 == 'Kolkata'):
            Bangalore=0
            Chennai=0
            Delhi=0
            Hyderabad=0
            Kolkata=1
            Mumbai=0

        else:
            Bangalore=0
            Chennai=0
            Delhi=0
            Hyderabad=0
            Kolkata=0
            Mumbai=1

        # print(s_Delhi,
        #     s_Kolkata,
        #     s_Mumbai,
        #     s_Chennai)

        # Destination
        # Banglore = 0 (not in column)
        Source = request.form["Destination"]
        if (Source == 'Bangalore'):
            destination_Bangalore = 1
            destination_Chennai = 0
            destination_Delhi = 0
            destination_Hyderabad = 0
            destination_Kolkata = 0
            destination_Mumbai=0
        
        elif (Source == 'Chennai'):

            destination_Bangalore = 0
            destination_Chennai = 1
            destination_Delhi = 0
            destination_Hyderabad = 0
            destination_Kolkata = 0
            destination_Mumbai=0

        elif (Source == 'Delhi'):
            destination_Bangalore = 0
            destination_Chennai = 0
            destination_Delhi = 1
            destination_Hyderabad = 0
            destination_Kolkata = 0
            destination_Mumbai=0

        elif (Source == 'Hyderabad'):
            destination_Bangalore = 0
            destination_Chennai = 0
            destination_Delhi = 0
            destination_Hyderabad = 1
            destination_Kolkata = 0
            destination_Mumbai=0

        elif (Source == 'Kolkata'):
            destination_Bangalore = 0
            destination_Chennai = 0
            destination_Delhi = 0
            destination_Hyderabad = 0
            destination_Kolkata = 1
            destination_Mumbai=0

        else:
            destination_Bangalore = 0
            destination_Chennai = 0
            destination_Delhi = 0
            destination_Hyderabad = 0
            destination_Kolkata = 0
            destination_Mumbai=1

        
        

        
        prediction=model.predict([[
            stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arr_hour,
            arr_min,
            Duration_hours,
            Duration_mins,
            Air_India,
            Vistara,
            Bangalore,
            Chennai,
            Delhi,
            Hyderabad,
            Kolkata,
            Mumbai,
            destination_Bangalore,
            destination_Chennai,
            destination_Delhi,
            destination_Hyderabad,
            destination_Kolkata,
            destination_Mumbai
            
            
           
        ]])

        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)