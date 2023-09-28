from flask import Flask, render_template, request, flash, redirect, url_for, session
from mysql import connector

connection = connector.connect(host="localhost",user="root",password='',database='student_registration') 

app = Flask(__name__)
app.secret_key = 'student_registraion'


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        db = connection.cursor()
        # db.execute('SELECT * FROM students')
        db.execute('SELECT students.*, courses.* FROM students INNER JOIN courses on students.course = courses.id ')
        students = db.fetchall()

        username = session.get('username','Guest')
        # return students
        return render_template('dashboard.html',students = students , username= username)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        if not email or  "@" not in email:
            flash('Valid email is required', 'error')
            return redirect(url_for('login'))

        if not password:
            flash('Password is required', 'error')
            return redirect(url_for('login'))
        
        db = connection.cursor()
        # db.execute(f'SELECT * FROM user WHERE email = {email} AND password = {password}')
        db.execute('SELECT * FROM user WHERE email = %s and password = %s',(email, password))

        user = db.fetchone()
        db.close()

        if user:
            session['username'] = user[1]
            flash('Login Successfully!', 'success')
            return redirect(url_for("dashboard"))
        else:
            flash('Credentials does\'t matched!', 'error')
            return redirect(url_for('login'))

@app.route('/register-student', methods = ['GET','POST'])
def register_student():
    if 'username' in session:
        username = session.get('username','Guest')

        if request.method == 'GET':
            db = connection.cursor()
            db.execute('SELECT * FROM courses')
            courses = db.fetchall()
            db.close()
            return render_template('register_student.html',courses = courses,username=username)
        else:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            gender = request.form['gender']
            course = request.form['course']
            address = request.form['address']
            joining_date = request.form['joining_date']

            if name and phone and email and gender and course and address and joining_date:
                db =connection.cursor()
                db.execute('INSERT INTO students (name, phone,email,gender,course,address,joining_date) VALUES(%s,%s,%s,%s,%s,%s,%s)',(name, phone,email,gender,course,address,joining_date))
                connection.commit()
                db.close()
                flash('Student Registered Successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Please enter Valid values', 'error')
                return redirect(url_for('register_student'))

    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()