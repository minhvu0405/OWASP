from flask import Flask, render_template, redirect, url_for, request, Markup, make_response
from random import randint
import hashlib, subprocess, os
from app import app, mysql
email = "example@pdx.edu"
name = "Minh Vu"
num01 = randint(0,1)
num02 = randint(0,2)
num05 = randint(0,5)
num07 = randint(0,7)
def hash(string):
    return hashlib.sha224(string).hexdigest()
def generatecode(string):
    str1 = hash(email)
    str2 = hash(name)
    str3 = hash(string)
    return str1[2:11].upper() + str2[4:13] + str3[-7:]
@app.route('/')
def cookie():
    resp = make_response(render_template('welcome.html'))
    str1 = hash(name)
    str2 = hash('thisisacookie')
    cookie = str1[1:5] + str1[2:8] + str2[2:6]
    resp.set_cookie('yourcookie', cookie)
    return resp
def random(n1,n2):
    return randint(n1,n2)   
@app.route('/index')
def index():
	return render_template('welcome.html')
    
@app.route('/welcome')
def welcome():
	return render_template('welcome.html') 
    
@app.route('/login', methods =['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
          email = request.form['email']
          password = request.form['password']
          if email and password:
              conn = mysql.connect()
              cursor = conn.cursor()
              email = str(email)
              password = str(password)
              query = 'SELECT * FROM Student WHERE email = %s AND password = %s'
              args = email,password
              cursor.execute(query,args)
              n = cursor.rowcount
              if n == 1:
                  return redirect(url_for('welcome'))
              else:
                  error = 'Please try again'
    return render_template('login.html',error = error)
    
@app.route('/brute', methods =['GET','POST'])
def brute():
    error = None
    success = None
    code = None
    userid = ['tom','harry','peter','linda','emma','jane']
    password = ['123456','password','qwerty','123456789','12345678','1234']
    info = 'id is ' + userid[num05]
    if request.method == 'GET':
        user = request.args.get('username')
        passwd = request.args.get('password')
        if user and passwd:
            if user == userid[num05] and passwd == password[num05]:
                success = 'Successful'
                code = generatecode('homeworknumber1')
            else: 
                error = "Please try again!"   
    return render_template('brute.html',error = error,success = success,info = info,code = code)
   
@app.route('/ping', methods =['GET','POST'])
def ping():
    error = None
    result = []
    print generatecode('homeworkping')
    if request.method == 'POST':
        cmd = request.form['command']
        if os.name == 'nt':
            proc = subprocess.Popen("ping %s" %cmd, shell=True, stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen("ping -c 3 %s" %cmd, shell=True, stdout=subprocess.PIPE)
        for line in iter(proc.stdout.readline,''):
            result.append(line.rstrip())
    return render_template('ping.html',error = error, result = result)

@app.route('/sqlinjection', methods =['GET','POST'])
def sqlinjection():
    error = None
    success = None
    code = generatecode('homeworknumber5')
    result = []
    conn = mysql.connect()
    cursor = conn.cursor()
    num = 0
    check = 0
    if request.method == 'POST':
        userid = request.form['id']
        userid = str(userid)
        query = 'SELECT userId,userName,FirstName  FROM User WHERE userID = %s' %userid
        try:
            cursor.execute(query)
            a = cursor.fetchall()
            num = cursor.rowcount        
        except Exception as err:
            error = str(err)
            
        query = 'SELECT userId,userName,FirstName  FROM User'
        cursor.execute(query)
        check = cursor.rowcount
        i = 0
        while i < num:
            result.append('ID: ' + str(a[i][0]))
            result.append('username: ' +  str(a[i][1]))
            result.append('First Name: ' + str(a[i][2]))
            i = i + 1
        if int(num) == int(check):
            success = 'Successful!' 
    return render_template('sqlinjection.html',success = success, error = error,result = result,code = code)
    
@app.route('/resetpassword', methods =['GET','POST'])
def resetpassword():
    msg = None
    success = None
    error = None
    admin = ['admin','administrator']
    flag = 0
    if request.method == 'GET':
        name = request.args.get('name')
        if not name:
            flag = 1
        name = str(name)
        name = name.lower()
        if flag != 1 and name == admin[num01]:
            return redirect(url_for('securequestion'))
        elif flag == 1:
            error = None
        else:
            error = 'not admin'
    return render_template('resetpassword.html', msg = msg,success = success, error = error)
    
@app.route('/securequestion', methods =['GET','POST']) 
def securequestion():
    code = None
    msg = None
    success = None
    error = None
    flag = 0
    color = request.args.get('color')
    if not color:
        flag = 1
    color = str(color)
    color = color.lower()
    mycolor = ['blue','yellow','green','red','orange','purple','black','white']
    if flag != 1 and color == mycolor[num07]:
        success = 'Successful!'
        code = generatecode('homeworknumber1')
    elif flag == 1:
        error = None
    else:
        error = 'Please try again!'
    return render_template('resetpassword-1.html', msg = msg,success = success, error = error,code = code) 
           
@app.route('/xss_r', methods =['GET','POST'])
def xss_r():
    msg = None
    success = None
    error = None
    code = generatecode('homeworknumber4')
    if request.method == 'GET':
        name = request.args.get('name')
        check = str(name)
        if '<script>' in check and '</script>' in check and 'document.cookie' in check:
            success = 'Successful!'
        if name:
             msg = Markup('<pre> Hello %s </pre>' % name)
    return render_template('xss_r.html', msg = msg,success = success, error = error,code = code)
    
@app.route('/tampering', methods =['GET','POST'])
def tampering():
    error = None
    success = None
    origin = 5000
    quantity = 1
    result = origin*quantity
    code = generatecode('homeworknumber2')
    if request.method == 'POST':
        price = request.form['price']
        quantity = request.form['quantity']
        result = int(price)*int(quantity)
        if int(price) < origin:
            success = 'You purchased the TV with the price $' + price
        else:
            error = 'Please try to purchase again!'
    return render_template('tampering.html', error = error, success = success, result = result, quantity = quantity,code = code)   

@app.route('/sample', methods =['GET','POST'])
def sample():
    error = None
    success = None
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        new = request.args.get('newpassword')
        conf = request.args.get('confirmedpassword')
        if new != conf:
            error = 'Confirmed password unmatched. Please try again!'
        else:
            if new:
                newpass = str(new)
                newpass = hashlib.md5(newpass)
                query = 'UPDATE User SET password = %s WHERE userName="admin"'
                cursor.execute(query,newpass)
                conn.commit()
                success = 'Changed the password successfully'
    return render_template('sample.html',error = error,success = success)
    
@app.route('/sample_medium', methods =['GET','POST'])
def sample_medium():
    error = None
    success = None
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        if str(request.referrer) != 'http://127.0.0.1:5000/csrf_medium' and request.referrer != None:
            error = 'http renderred not match'
            return render_template('csrf.html',error = error,success = success)
        else:
            new = request.form['newpassword']
            conf = request.form['confirmedpassword']
            if new != conf:
                error = 'Confirmed password unmatched. Please try again!'
            else:
                if new:
                    newpass = str(new)
                    newpass = hashlib.md5(newpass)
                    query = 'UPDATE User SET password = %s WHERE userName="admin"'
                    cursor.execute(query,newpass)
                    conn.commit()
                    success = 'Changed the password successfully'
    return render_template('sample_medium.html',error = error,success = success)
    
@app.route('/csrf', methods =['GET','POST'])
def csrf():
    error = None
    success = None
    msg = None
    code = generatecode('homeworknumber5')
    require = ['transfer','send','deposit']
    money = ['560','1150','5430','65000','75340','85650']
    parameter = require[num02] + '=' + money[num05]
    print parameter
    if request.method == 'POST':
        msg = request.form['message']
        if msg:
            check = str(msg)
            check = check.lower()
            referrer = str(request.referrer)
            print referrer
            if '<img' in msg and 'src' in msg and referrer in msg and parameter in msg:
                success = "Successful!"
            if '<img' in msg and referrer in msg: 
                error = "You're close!"
    return render_template('csrf.html',error = error,success = success,parameter = parameter,code = code)
    
@app.route('/insecurelogin', methods =['GET','POST'])
def insecurelogin():
    error = None
    success = None
    msg = None
    if request.method == 'POST':
        userID = request.form['username']
        password = request.form['password']
        if str(userID) == 'User' and str(password) == 'a2Hkio8lm%':
            return redirect(url_for('pswquestion'))
        else:
            error = 'User/password not match'
    return render_template('insecurelogin.html', error = error, success = success) 
     
@app.route('/pswquestion', methods =['GET','POST'])
def pswquestion():
    error = None
    success = None
    msg = None
    if request.method == 'POST':
        password = request.form['password']
        if password:
            if str(password) == 'a2Hkio8lm%':
                success = "Successful!"
            else:
                error = "Wrong Password..."
    return render_template('insecurelogin-1.html', error = error, success = success)

@app.route('/forcedbrowsing', methods =['GET','POST'])
def forcedbrowsing():
    admin = ['admin','administrator','authenticator','hidden','secret','private']
    conf = ['conf','.conf','config','.config','configuration','.configuration','setting','.setting']
    msg = admin[num05] + conf[num07]
    info = msg
    error = None
    success = None
    code = None
    if request.method == 'POST':
        name = request.form['name']
        if name == 'admin.conf' or name == 'adminconf':
            success = "Successful!"
            code = generatecode('homeworknumber8')
        else:
            error = "Try again..."
    return render_template('forcedbrowsing.html',info = info, error = error, success = success, code = code)
    
@app.route('/admin.config', methods =['GET','POST'])
def secretconfiguration():
    success = "Found"
    print success   
    return render_template('hiddenconf.html')    