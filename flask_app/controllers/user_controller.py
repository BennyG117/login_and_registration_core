from flask_app import app
from flask import render_template, redirect, request, session, flash, Flask
#two above should always be at top^

from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




# Home Route
@app.route('/')
def input_home():
    return render_template("dashboard.html")


# Route for login check for user login 
@app.route('/login_user', methods=['POST'])
def loginCheck():

    #check if email exists in db
    login_data = {'email':request.form['email']}
    user_in_db = User.get_oneByEmail(login_data)

    if not user_in_db: 
        #flash messages have category*
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    # check if unhashed pw correct
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')

    #if valid then progress...    
    session['user_id'] = user_in_db.id
    
    return redirect(f'/success/{user_in_db.id}')


# Route to save registration information
@app.route('/register_user', methods=['POST'])
def successful_register():

    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #! may need to add at end of thread above: ".decode('utf-8')"
    
    newUser_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.save(newUser_data)

    session['user_id'] = user_id

    return redirect(f'/success/{user_id}')

# Route to log out
@app.route('/logout')
def logout():
    session.clear()
    # may require session.pop('first_name / or other key:id') #
    return redirect('/')


# Route to successful login / Transfers user to success page
@app.route('/success/<int:id>')
def show_success(id):

        if 'user_id' not in session:
            flash('Please login or Register', 'warning')
            return redirect('/')
        newUser = User.get_oneById({'id': id})

        return render_template('success.html', newUser=newUser)



# Route to validate registration requirements 


# Route to validate login requirements

