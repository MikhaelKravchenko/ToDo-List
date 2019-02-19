from flask import Flask, request, Response, jsonify, render_template, session, url_for, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json
import utils as Utils

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

@app.route("/")
def index():
    if not Utils.isUserLoggedIn(session):
        return render_template('registerOrLogin.html')
    
    to_do_list = Utils.getAllToDoItemsFromDB(session.get('username'))

    return render_template('index.html', to_do_list = to_do_list)


@app.route("/registerOrLogin", methods=['POST'])
def registerNewUser():
    if request.form['log_reg'] == 'login':
        if Utils.checkIfUserExists(request.form['username']):
            session['username'] = request.form['username']
        else:
            return render_template('registerOrLogin.html', status = 'That username does not exist, please register!')
    elif request.form['log_reg'] == 'register':
        if Utils.checkIfUserExists(request.form['username']):
            return render_template('registerOrLogin.html', status = 'Sorry! That username is already taken!')
        elif len(request.form['username']) < 4:
            return render_template('registerOrLogin.html', status = 'Username should be of at least 4 characters!')
        
        Utils.addUserToDB(request.form['username'])
        session['username'] = request.form['username']

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if not Utils.isUserLoggedIn(session):
        return render_template('registerOrLogin.html')

    session.pop('username', None)

    return redirect(url_for('index'))


@app.route("/getAll")
def getAllToDoItems():
    if not Utils.isUserLoggedIn(session):
        return render_template('registerOrLogin.html')

    return jsonify(Utils.getAllToDoItemsFromDB(session.get('username')))


@app.route("/add", methods=['POST'])
def addToDoItem():
    if not Utils.isUserLoggedIn(session):
        return render_template('registerOrLogin.html')

    description = request.form['desc']

    if len(description) > 0:
        Utils.addToDoItemToDB(session.get('username'), description)

    return redirect(url_for('index'))


@app.route("/complete/<int:item_id>")
def markToDoItemAsComplete(item_id):
    if not Utils.isUserLoggedIn(session):
        return render_template('registerOrLogin.html')

    result = Utils.markToDoItemAsComplete(session.get('username'), item_id)

    if result == False:
        return Response('{"message": "Item not found."}', status=404, mimetype='application/json')

    return redirect(url_for('index'))


if __name__ == "__main__":
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = ''

    app.run(port=8181)
