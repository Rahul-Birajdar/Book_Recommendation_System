import pickle
import numpy as np
import pandas as pd
from flask import *
from sqlite3 import *
from hashlib import md5

app=Flask(__name__)
app.secret_key="ganesh_stays_at_abc_station"

@app.route("/",methods=["GET","POST"])
def home():
    if "un" not in session:   
        return redirect(url_for("login"))
    if request.method=="POST":
        session.pop("un")
        return redirect(url_for("login"))
    else:
        un=session["un"]
        return render_template("logout.html",msg=un)

@app.route("/login",methods=["GET","POST"])
def login():
    if "un" in session:
        return redirect(url_for("index"))
    elif request.method=="POST":
        un=request.form["un"]
        pw=request.form["pw"]
        epw=md5(pw.encode()).hexdigest()
        con=None
        try:
            con=connect("users.db")
            cursor=con.cursor()
            sql="select * from student where username='%s' and password='%s'"
            cursor.execute(sql%(un,epw))
            data=cursor.fetchall()
            if len(data)==0:
                msg="Invalid Login"
                return render_template("login.html",msg=msg)
            else:
                session["un"]=un
                return redirect(url_for('index'))
        except Exception as e:
            msg="issue " + str(e)
            return render_template("signup.html",msg=msg)
        finally:
            if con is not None:
                con.close()
    else:
        return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if "un" in session:
        return redirect(url_for("index"))
    elif request.method=="POST":
        un=request.form["un"]
        pw1=request.form["pw1"]
        pw2=request.form["pw2"]
        epw=md5(pw1.encode()).hexdigest()
        if pw1==pw2:
            con=None
            try:
                con=connect("users.db")
                cursor=con.cursor()
                sql="insert into student values('%s','%s')"
                cursor.execute(sql%(un,epw))
                con.commit()
                return redirect(url_for("login"))
            except Exception as e:
                con.rollback()
                msg="issue " + str(e)
                return render_template("signup.html",msg=msg)
            finally:
                if con is not None:
                    con.close()
        else:
            msg="Passwords did not match"
            return render_template("signup.html",msg=msg)
    else:
        return render_template("signup.html")

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("login"))

popular_books = pickle.load(open('popular_books.pkl', 'rb'))
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

@app.route('/index')
def index():
    return render_template('index.html',
                           book_names=list(popular_books['title'].values),
                           authors=list(popular_books['author'].values),
                           votes=list(popular_books['num_ratings'].values),
                           ratings=list(popular_books['avg_ratings'].values),
                           images=list(popular_books['image'].values),
                           link=list(popular_books['link'].values),)
                           
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["POST"])
def recommend():
    user_input = request.form.get("user_input")
    try:
        book_index = np.where(book_pivot.index == user_input)[0][0]
    except IndexError:
        return render_template('recommend.html', data=[])
    
    suggested_items = sorted(list(enumerate(similarity_score[book_index])), key=lambda x: x[1], reverse=True)[1:5]
    book_list = list(books["title"].values)
    
    data = []
    for i in suggested_items:
        item = []
        temp = books[books["title"] == book_pivot.index[i[0]]]
        item.extend(temp.drop_duplicates("title")['title'].values)
        item.extend(temp.drop_duplicates("title")['author'].values)
        item.extend(temp.drop_duplicates("title")['image'].values)
        item.extend(temp.drop_duplicates("title")['link'].values)
        data.append(item)
    return render_template('recommend.html', data=data)

@app.route('/logout')
def logout():
    session.pop("un")
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True,use_reloader=True)
