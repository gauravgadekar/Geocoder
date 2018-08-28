from flask import Flask,render_template,send_file,request
from werkzeug import secure_filename
import pandas
from geopy.geocoders import Nominatim
import os

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    global file
    if request.method=='POST':
        file=request.files["file"]
        file.save(secure_filename(file.filename))
        num=Nominatim(timeout=3)
        n=num.geocode
        df=pandas.read_csv(file.filename)
        if ('Address' in df.columns):
            df["Address"]=df["Address"]+","+df["City"]+","+ df["State"]+","+ df["Country"]
            df["Cordinates"]=df["Address"].apply(num.geocode)
            df["Latitude"]=df["Cordinates"].apply(lambda x: x.latitude if x!=None else None)
            df["Longitude"]=df["Cordinates"].apply(lambda x: x.longitude if x!=None else None)
            df.to_csv("geocoded_"+file.filename,sep=",")
            os.remove(file.filename)
            return render_template('index.html',btn='table.html',tables=[df.to_html(classes='geo')],
            titles = ['na'])
        elif ('address' in df.columns):
                df["address"]=df["address"]+","+df["City"]+","+ df["State"]+","+ df["Country"]
                df["Cordinates"]=df["address"].apply(num.geocode)
                df["Latitude"]=df["Cordinates"].apply(lambda x: x.latitude if x!=None else None)
                df["Longitude"]=df["Cordinates"].apply(lambda x: x.longitude if x!=None else None)
                df.to_csv("geocoded_"+file.filename,sep=",")
                os.remove(file.filename)
                return render_template('index.html',btn='table.html',tables=[df.to_html(classes='geo')],
                titles = ['na'])
        else:
            return render_template('index.html',text="Address column does not exist!")

@app.route("/table")
def table():
    return send_file("geocoded_"+file.filename, attachment_filename="geocoded.csv", as_attachment=True)



if __name__=='__main__':
    app.debug=True
    app.run()
