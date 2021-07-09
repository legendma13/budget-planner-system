import sqlite3
import mysql.connector
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

mydb = mysql.connector.connect(
    host="localhost",
    database="plan",
    user="root",
    password=""
)

app = Flask(__name__)
app.secret_key = 'mysecretkey'


def connection():
    con = sqlite3.connect('admin.db')
    con.row_factory = sqlite3.Row
    return con


@app.route("/calculator", methods=('GET', 'POST'))
def calculate():
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']
        if operation == 'add':
            result = float(num1) + float(num2)
            return render_template('calculator.html', result=result)
        elif operation == 'subtract':
            result = float(num1) - float(num2)
            return render_template('calculator.html', result=result)
        elif operation == 'multiply':
            result = float(num1) * float(num2)
            return render_template('calculator.html', result=result)
        elif operation == 'divide':
            result = float(num1) / float(num2)
            return render_template('calculator.html', result=result)
        else:
            return render_template('calculator.html')
    return render_template('calculator.html')


@app.route('/change', methods=('GET', 'POST'))
def change():
    con = connection()

    if request.method == 'POST':
        user = request.form['user']
        cpass = request.form['Cpass']
        npass = request.form['Npass']
        copass = request.form['Copass']
        if not copass:
            flash('Confirm Password is required!')
        else:
            if npass != copass:
                flash('Error Password Incorrect!')
            con.execute('UPDATE administrator SET username = ?, password = ?'
                        ' WHERE id = 1',
                        (user, npass))
            con.commit()
            con.close()
            return redirect('home')
    return render_template('change.html')


@app.route('/reset', methods=('GET', 'POST'))
def reset():
    con = connection()
    admin = 'admin'
    passw = '1234'
    if request.method == 'POST':
        con.execute('UPDATE administrator SET username = ?, password = ?'
                    ' WHERE id = 1',
                    (admin, passw))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('reset.html')


@app.route('/<string:id>/home', methods=('GET', 'POST'))
def home(id):
    myc = mydb.cursor()
    myc.execute('SELECT * FROM ' + id + '')
    plan = myc.fetchall()
    myc.execute('SELECT t_budget from title_data where title = "' + id + '"')
    pl = myc.fetchone()
    value = pl
    sum = 0

    for x in plan:
        sum = int(sum) + int(x[2])
    if request.method == 'POST':
        budget = request.form['budget']
        amount = request.form['amount']
        t = (budget, amount)
        if not budget:
            flash('Budget Title is required!')
        else:
            myc.execute('INSERT INTO ' + id + ' (budget_f, amount) VALUES (%s, %s)', t)
            mydb.commit()
            myc.close()
            return redirect('home')
    I = id
    da = id
    return render_template('index.html', plan=plan, su=sum, I=I, da=da, pl=value)


@app.route('/<string:data>/<int:id>/edit', methods=('GET', 'POST'))
def edit(data, id):
    myc = mydb.cursor()
    myc.execute('SELECT * FROM ' + data + '')
    plan = myc.fetchall()
    myc.execute('SELECT t_budget from title_data where title = "' + data + '"')
    pl = myc.fetchone()
    value = pl
    sum = 0
    I = data
    for x in plan:
        sum = int(sum) + int(x[2])
    if request.method == 'POST':
        budget = request.form['budget_f']
        amount = request.form['amount']
        t = (budget, amount)
        if not budget:
            flash('Budget Title is required!')
        else:
            myc.execute('UPDATE ' + data + ' SET budget_f=%s, amount=%s WHERE id=' + str(id) + '', t)
            mydb.commit()
            myc.close()
            return redirect('edit')

    return render_template('edit.html', plan=plan, su=sum, I=I, pl=value)


@app.route('/<string:daa>/<int:id>/delete', methods=('POST', 'GET'))
def delete(daa, id):
    if request.method == 'POST':
        myc = mydb.cursor()
        myc.execute('DELETE FROM ' + daa + ' WHERE id = ' + str(id) + '')
        mydb.commit()
        myc.close()
        flash('successfully deleted!')
        print(daa)
        return redirect('/'+daa+'/home')


@app.route('/home', methods=('GET', 'POST'))
def index():
    myc = mydb.cursor()
    myc.execute('SELECT * FROM title_data')
    sh = myc.fetchall()
    if request.method == 'POST':
        title = request.form['table']
        t_budget = request.form['t_budget']

        t = (title, t_budget)
        if not title:
            flash('title is needed')
        else:
            myc.execute('DROP TABLE IF EXISTS ' + title + ';')
            myc.execute('CREATE TABLE ' + title + '(id INT AUTO_INCREMENT PRIMARY KEY,budget_f Text NOT NULL,amount '
                                                  'varchar(255))')
            myc.execute('INSERT INTO title_data(title, t_budget) VALUES (%s, %s)', t)
            mydb.commit()
            return redirect('/home')
    return render_template('home.html', sh=sh)


@app.route('/<string:sid>/del_plan', methods=('POST', 'GET'))
def del_plan(sid):
    myc = mydb.cursor()
    myc.execute('DROP TABLE ' + sid + '')
    myc.execute('DELETE FROM title_data WHERE title = "' + sid + '"')
    mydb.commit()
    myc.close()
    return redirect('/home')


@app.route('/', methods=('GET', 'POST'))
def login():
    con = connection()
    if request.method == 'POST':
        use = con.execute('SELECT * FROM administrator where id = 1').fetchall()
        for x in use:
            user = x[1]
            passw = x[2]
        username = request.form['username']
        password = request.form['password']

        if user == username and passw == password:
            return redirect('home')
        else:
            flash('Username or Password is incorrect')
            return redirect('/')

    return render_template('login.html')


app.run(host="localhost", debug=True)
