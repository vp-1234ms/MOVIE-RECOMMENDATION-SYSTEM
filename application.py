from flask import Flask,request,render_template,redirect
import pandas as pd
import re
from flask_cors import CORS,cross_origin
application = Flask(__name__)
app=application
@app.route("/",methods=["GET","POST"])
@cross_origin()
def start():
     data=pd.read_csv('Final.csv')
     l=data['genre'].to_list()
     h=[]
     for i in l:
          h.append(i.split(','))
     v=[]
     for i in h:
          for j in i:
               v.append(j)
     s=set(v)
     Genre=list(s)
     G=[]
     for i in Genre:
          G.append(i.strip())
     s=set(G)
     Genre=list(s)
     Genre.sort()

     l=data['year'].to_list()
     h=[]
     for i in l:
          try:
               h.append(re.findall(r'\d+',i)[0])
          except Exception as e:
               pass
     s=set(h)
     Year=list(s)
     G=[]
     for i in Year:
          G.append(i.strip())
     Year=G
     Year.sort(reverse=True)

     l=data['certificate'].to_list()
     s=set(l)
     Certificate=list(s)
     G=[]
     for i in Certificate:
          G.append(i.strip())
     Certificate=G

     return render_template("index.html",genre=Genre,x=len(Genre),year=Year,y=len(Year),certification=Certificate,z=len(Certificate))

@app.route("/result",methods=["GET","POST"])
@cross_origin()
def home():
     if request.method=='POST':
          movie_genre=request.form.getlist('mycheckbox1')
          movieyear=request.form.getlist('mycheckbox2')
          movie_certification=request.form.getlist('mycheckbox3')
          print(movie_genre)
          print(movieyear)
          print(movie_certification)
          data=pd.read_csv('Final.csv')
          data=data[data['genre'].str.contains('|'.join(movie_genre))]
          if(len(movieyear)!=0):
               data=data[data['year'].str.contains('|'.join(movieyear))]
          data=data[data['certificate'].str.contains('|'.join(movie_certification))]
          data=data.sort_values(by=['year'],ascending=False)
          data=data.sort_values(by=['year'],ascending=False)
          movie_names=data['title'].to_list()
          movie_img=data['image'].to_list()
          movie_ratings=data['rating'].to_list()
          movie_year=data['year'].to_list()
          return render_template("result.html",movieimage=movie_img,moviename=movie_names,movierating=movie_ratings,movieyear=movie_year,x=len(movie_img))

if __name__=="__main__":
    app.run(host="0.0.0.0")
