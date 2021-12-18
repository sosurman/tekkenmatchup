from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User, Friend
from flask_app.models.matchup import Matchup
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    return redirect('/dashboard')
    
@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')
    
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    return render_template("homepage.html",user=user, matchups = Matchup.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/friends')
def friends():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
    }
    user = User.get_one(data)
    users = User.get_all()
    friend_id = Friend.get_all(data)
    print(friend_id)
    return render_template("friends.html",user=user, users = users, friend_id = friend_id)

@app.route('/friends/add',methods=['POST'])
def addfriend():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
        "friend_id": request.form['friend']
    }
    friend_id = request.form['friend']
    friends = Friend.savefriendship(data)
    print(friends)
    return redirect("/friends")