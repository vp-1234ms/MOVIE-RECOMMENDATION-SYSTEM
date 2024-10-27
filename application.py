from flask import Flask, request, app,render_template,redirect
from flask import Response
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

@app.route("/result", methods=["GET", "POST"])
@cross_origin()
def home():
    if request.method == 'POST':
        movie_genre = request.form.getlist('mycheckbox1')
        movie_year = request.form.getlist('mycheckbox2')
        movie_certification = request.form.getlist('mycheckbox3')
        
        data = pd.read_csv('Final.csv')
        
        # Filter by Genre
        if movie_genre:
            data = data[data['genre'].str.contains('|'.join(movie_genre))]
        
        # Filter by Year
        if movie_year:
            data = data[data['year'].str.contains('|'.join(movie_year))]
        
        # Filter by Certification if selected
        if movie_certification:
            data = data[data['certificate'].str.contains('|'.join(movie_certification))]
        
        # If no data remains, return a message to the result page
        if data.empty:
            return render_template("result.html", message="No movies found for selected filters.")
        
        # Prepare data for rendering if there are results
        movie_names = data['title'].to_list()
        movie_img = data['image'].to_list()
        movie_ratings = data['rating'].to_list()
        movie_year = data['year'].to_list()
        x = len(movie_img)  # Set x only if data is not empty
        
        return render_template(
            "result.html",
            movieimage=movie_img,
            moviename=movie_names,
            movierating=movie_ratings,
            movieyear=movie_year,
            x=x
        )




if __name__=="__main__":
    app.run(host="0.0.0.0")
