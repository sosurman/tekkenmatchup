from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.matchup import Matchup
from flask_app.models.user import User


@app.route('/new/matchup')
def new_matchup():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_matchup.html',user=User.get_one(data))


@app.route('/create/matchup',methods=['POST'])
def create_matchup():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Matchup.validate_matchup(request.form):
        return redirect('/new/matchup')
    data = {
        #"name": request.form["name"],
        "userchar": request.form["userchar"], #description
        "opponent": request.form["opponent"], #instructions
        "move": request.form["move"], #instructions
        "punish": request.form["punish"], #instructions
        "num_of_frames": (request.form["num_of_frames"]), #under30
        "user_id": session["user_id"]
    }
    Matchup.save(data)
    return redirect('/dashboard')

@app.route('/edit/matchup/<int:id>')
def edit_matchup(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_matchup.html",edit=Matchup.get_one(data),user=User.get_one(user_data))

@app.route('/update/matchup',methods=['POST'])
def update_matchup():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Matchup.validate_matchup(request.form):
        return redirect('/new/matchup')
    data = {
        #"name": request.form["name"],
        "userchar": request.form["userchar"], #description
        "opponent": request.form["opponent"], #instuctions
        "move": request.form["move"], #instuctions
        "punish": request.form["punish"], #instuctions
        "num_of_frames": (request.form["num_of_frames"]), #under 30
        "id": request.form['id']
    }
    Matchup.update(data)
    return redirect('/dashboard')

@app.route('/matchup/<int:id>')
def show_matchup(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    report = Matchup.get_by_id(data)
    return render_template("show_matchup.html", matchup=Matchup.get_one(data),user=User.get_one(user_data), report = report)

@app.route('/destroy/matchup/<int:id>')
def destroy_matchup(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Matchup.destroy(data)
    return redirect('/dashboard')