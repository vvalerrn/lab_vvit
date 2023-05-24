from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database='service_db',
                        user='postgres',
                        password='kthfcfif2',
                        host='localhost',
                        port='5432')
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username),
                                                                                              str(password)))
                records = list(cursor.fetchall())
                if records:
                    return render_template('account.html', full_name=records[0][1], username=username,
                                           password=password)
                else:
                    return render_template('account.html', error="Account with such data doesn't exist")
            else:
                return render_template('account.html', error="Empty fields for password or username")

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('login')
        password = request.form.get('password')

        cursor.execute('SELECT * FROM SERVICE.USERS WHERE login=%s', [str(username)])
        record = list(cursor.fetchall())
        if record:
            return render_template('registration.html', error='Account with such login already exist')
        else:
            if (username and password and name) and (len(username) != username.count(' ')
                                                     and len(password) != password.count(' ')
                                                     and len(name) != name.count(' ')):
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(username), str(password)))
                conn.commit()
            else:
                return render_template('registration.html', error='You entered incorrect data for registration. '
                                                                  'Please, enter the correct name, login and password')
            conn.commit()

        return redirect('/login/')

    return render_template('registration.html')
