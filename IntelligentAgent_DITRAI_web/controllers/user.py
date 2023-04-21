from flask import Blueprint, render_template,request,redirect,flash
from flask_login import login_user, logout_user
from models.user import User,db
from main import bcrypt
users=Blueprint("users",__name__,url_prefix="/",template_folder="../templates/user")

@users.route("/",methods=['POST','GET'])
def login():
    try:
        if request.method=="POST":
            username=request.form["username"]
            password=request.form["password"]
            next_page = request.args.get("next")
            print(username)
            print(password)
            user:User= User.query.filter_by(username=username).first()
            print(user.username)
            print(user.password)
            if user == None:
                flash("Usuario no existe")
                return render_template("login.html")
            
            if bcrypt.check_password_hash(user.password, password) :
                login_user(user)
                if(next_page != None): #check for next page the user wanted to access and redirect if any
                    return redirect(next_page)
                return redirect ("/home")
            else:
                flash("contraseña incorrecta")
                return render_template("login.html")
    except:
        flash("login error !!")
        return render_template("login.html")

    return render_template("login.html")

@users.route('/register',methods=['POST','GET'])
def register():
    try:
        if request.method=="POST":
            name=request.form["name"]
            username=request.form["username"]
            password=request.form["password"]
            password=bcrypt.generate_password_hash(password,10).decode('utf-8')

            user=User(name,username,password)
            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect("/")
    except:
        flash("error occured, could be invalid username/email")
        return render_template('register.html')

    return render_template('register.html')

@users.route("/restricted")
def restricted():
    return render_template("restricted.html")

@users.route('/logout')
def logout():
    logout_user()
    return redirect("/")