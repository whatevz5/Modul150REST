'''
Author: Ethen Spielmann IABM15c
Modul: 150
Project: First Rest-API project
File: Main file from project with all the index rules
'''

from flask import Flask, jsonify, request, render_template, redirect, url_for
import data_source as ds
import urllib

#overall global variable for username
username = ""

#creating rest-api server
app = Flask(__name__)


#index page handling
@app.route('/index/')
def index():
    # calling html page
    return render_template('index.html')

#index page handling
@app.route('/profile/')
def profile():
    if username == "":
        # calling html page
        return render_template('index.html')
    else:
        # calling html page
        return render_template('profile.html')

#index page handling
@app.route('/login/')
def login():
    # calling html page
    return render_template('login.html')

#index page handling
@app.route('/logout/')
def logout():
    global username
    username = ""
    # calling html page
    return render_template('index.html')

#index page handling
@app.route('/login_error/')
def login_f():
    # calling html page
    return render_template('login_f.html')

#index page handling
@app.route('/register/')
def register():
    # calling html page
    return render_template('register.html')

#index page handling
@app.route('/register_error/')
def register_f():
    # calling html page
    return render_template('register_f.html')

#index page handling
@app.route('/edit_done/')
def edit_done():
    # calling html page
    return render_template('edit_done.html')

#index page handling
@app.route('/check_login/', methods=['POST'])
def check_login():
    if request.method == 'POST':
        global username
        #getting data from form
        username = request.form['username']
        userpass = request.form['pass']
        #checking if user exists in db
        if ds.check_user(username, userpass):
            # calling html page
            return redirect(url_for('profile'))
        else:
            # calling html page
            return redirect(url_for('login_f'))
    else:
        return "WRONG METHOD USED. USE POST"

#index page handling
@app.route('/check_register/', methods=['POST'])
def check_register():
    if request.method == 'POST':
        error = False
        try:
            # saving data from form
            useremail = request.form['email']
            username = request.form['username']
            userpass = request.form['pass']
            # checking that every field isnt empty
            if useremail != "" and username != "" and userpass != "":
                # checking if user exists in db
                if ds.check_user_exist(useremail, username):
                    error = True
                else:
                    # inserting user into db
                    ds.insert_user(useremail, username, userpass)
            else:
                error = True
            if error:
                # calling html page
                return redirect(url_for('register_f'))
            else:
                # calling html page
                return redirect(url_for('login'))
        except:
            # calling html page
            return redirect(url_for('register_f'))        
    else:
        return "WRONG METHOD USED. USE POST"

#index page handling
@app.route('/myinfo/')
def myinfo():
    global username
    if username == "":
        # calling html page
        return render_template('index.html')
    else:
        # getting user data from db
        result = ds.get_user_data(username)
        # calling html page
        return render_template("myinfo.html", result=result)

#index page handling
@app.route('/deleteAcc/')
def deleteAcc():
    # calling html page
    return render_template('delete_confirm.html')

#index page handling
@app.route('/deleteAccYes/')
def deleteAccYes():
    global username
    if username == "":
        # calling html page
        return render_template('index.html')
    else:
        # deleting user from db
        ds.delete_user(username)
        username = ""
        # calling html page
        return render_template('index.html')

#index page handling
@app.route('/editAcc/')
def edditAcc():
    if username == "":
        # calling html page
        return render_template('index.html')
    else:
        # getting user data from db
        result = ds.get_user_data(username)
        # calling html page
        return render_template('edit_acc.html', result=result)

#index page handling
@app.route('/editAcc_go', methods=['POST'])
def editAccGo():
        global username
        # getting data from form
        newname = request.form['username']
        userpass = request.form['password']
        # updating user in data_source
        ds.update_user(username, newname, userpass)
        username = newname
        # calling html page
        return render_template('edit_done.html')

# Main starting the program
if __name__ == '__main__':
    app.run(debug=True)