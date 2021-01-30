from flask import Flask,render_template,request,redirect,url_for,flash,abort
import sqlite3 as sql
from datetime import datetime,timedelta
import time as t
from threading import Thread
import requests
import json
'''import RPi.GPIO as m

m.setmode(m.BCM)
m.setup(17,m.OUT)
m.setwarnings(False)
m.output(17,0)
def longbell():
    m.output(17,1)
    t.sleep(6)
    m.output(17,0)

def shortbell():
    m.output(17,1)
    t.sleep(2)
    m.output(17,0)
    t.sleep(1)'''
app=Flask(__name__)
app.secret_key = 'PBSAasdertyuiop2020'
user_pass = {0:"user",1:"password"}
di = {0:"decision"}

def new(start,end,d_s,d_l,c,act):
    dates = {}
    if len(start)!=0 and len(end)!=0:
        a = datetime.strptime(start,"%Y-%m-%d")
        b = datetime.strptime(end,"%Y-%m-%d")
        delta = b-a
        #print(act)
        #print("Total number of days: ",delta.days)
        print("The following dates are scheduled: ")
        di[0] = act
        #print(di)
        dates = {}
        for i in range(0,delta.days):
            day = a + timedelta(days=i)
            dates[str(day)[0:10]] = i+1
            print(str(day)[0:10])
        #print("Total dates dictionary:",dates)
        q = 0
        s_k = list(d_s.keys())
        while q< len(dates) and act== di.get(0):
            p = 0 
            while p < len(d_s)+len(d_l) and act==di.get(0):
                date = t.strftime("%Y-%m-%d")
                m = t.strftime("%H:%M:%S")
                if m in d_l and date in dates:
                    print(m)
                    p = 1 if d_l.get(m) is None else d_l.get(m)
                    #print("p = ",p)
                    q = len(dates) if dates.get(date) is None else dates.get(date)
                    #print("q = ",q)
                    print("long bell")
                    #longbell()
                    t.sleep(1)
                elif m in d_s and date in dates:
                    print(m)
                    p = 1 if d_s.get(m) is None else d_s.get(m)
                    #print("p = ",p)
                    q = len(dates) if dates.get(date) is None else dates.get(date)
                    #print("q = ",q)
                    r = c.get(m)
                    print("The bell should ring", r," times")
                    for i in range(r):
                        print("bell rings")
                        #shortbell()
                        t.sleep(1)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title = '404'), 404
@app.route('/')
def login():
    user_pass[0]="user"
    user_pass[1]="password"
    return render_template('login.html')
@app.route('/loginvalidation',methods = ["POST"])
def loginvalid():
    username = request.form['username']
    password = request.form['password']
    if username=="admin" and password=="asdf":
        user_pass[0] = username
        user_pass[1] = password 
        return render_template('login1.html')
    else:
        return render_template('login.html')

def DATA(d_s,d_l,c,act):
    con = sql.connect('real2.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS DATA')
    cur.execute("CREATE TABLE IF NOT EXISTS DATA(SNO INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL,SHORT TEXT NOT NULL,LONG TEXT NOT NULL, COUNT TEXT NOT NULL)")
    cur.execute("INSERT INTO DATA(NAME,SHORT,LONG,COUNT) VALUES (?,?,?,?)",(act,json.dumps(d_s),json.dumps(d_l),json.dumps(c)))
    cursor = cur.execute('SELECT * FROM DATA')
    for row in cursor:
        act = row[1]
        short_bell = json.loads(row[2])
        long_bell = json.loads(row[3])
        count = json.loads(row[4])


@app.route('/dynamic',methods = ["POST"])
def create_schedule():
    a = request.form
    print(a['time_table'])
    print(a['time_table_purpose'])
    con = sql.connect("real.db")
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS TIMETABLE')
    cur.execute('''CREATE TABLE IF NOT EXISTS TIMETABLE(SNO INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL,PURPOSE TEXT NOT NULL)''')
    cur.execute("INSERT INTO TIMETABLE(NAME,PURPOSE) VALUES (?,?)",(a['time_table'],a['time_table_purpose']))
    con.commit()
    con.close()
    return redirect(url_for('create'))

@app.route('/scheduledisplayer',methods= ['POST','GET'])
def scheduledisplayer():
    try:
        con = sql.connect("real.db")
        con.row_factory = sql.Row 
        cur = con.cursor()
        #cur.execute("SELECT SNO,NAME,PURPOSE FROM TIMETABLE")
        cur.execute("SELECT * FROM TIMETABLE")
        rows = cur.fetchall()
        print(rows)
        return render_template('scheduledisplayer.html',items= rows)
    except:
        flash("Server Error")
        return render_template("create.html")

@app.route('/create', methods = ["POST","GET"])
def create():
    time = []
    text = []
    bell = []
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        if request.method=="POST":
            print(request.form)
            if request.form.get("external")=="submit":
                data = request.form.to_dict(flat=False)
                total = len(data)+1
                t = int(total/3)
                for i in range(0,t):
                    ti=data['time'+str(i)]
                    te=data['text'+str(i)]
                    be=data['select'+str(i)]
                    time.append(ti)
                    text.append(te)
                    bell.append(be)
                con = sql.connect("real1.db") 
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS SchoolBells(SNO INTEGER PRIMARY KEY AUTOINCREMENT,TIME TEXT NOT NULL,BELLS TEXT NOT NULL,COUNT INT NOT NULL)''')
                for i in range(0,len(time)):
                    if len(str(time[i][0]))!= 0 and len(str(text[i][0]))!=0:
                        cur.execute("INSERT INTO SchoolBells(TIME,COUNT,BELLS) VALUES (?,?,?)",(str(time[i][0]),str(text[i][0]),str(bell[i][0]),))
                cursor = cur.execute("SELECT * FROM SchoolBells")
                con.commit()
                con.close()
                #print("database saved")
                flash("Successfully Saved")
                di[0] = "decision"
                act = "create"
                d_s = {}
                d_l = {}
                c = {}
                for i in range(0,t):
                    if bell[i][0] == 'short bell':
                        d_s[time[i][0]] = i
                        c[time[i][0]]=int(text[i][0])
                    if bell[i][0] == 'long bell':
                        d_l[time[i][0]] = i
                #thr = Thread(target= new, args=[d_s,d_l,c,act])
                #thr.start()
                thr = Thread(target = DATA,  args = [d_s,d_l,c,act])
                thr.start()
                return redirect(url_for('scheduledisplayer'))
            elif request.form.get("external")=="display":
                return redirect(url_for('alarmschedule'))
            elif request.form.get("external")=="clear":
                return redirect(url_for('clear'))
            elif request.form.get("external")=="logout":
                return redirect(url_for('login'))
            return render_template('create.html')
        else:
            flash("Server Error")
            return render_template("create.html")
    else:
        abort(404)

@app.route('/clear',methods=["GET","POST"])
def clear():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        try:
            con = sql.connect("real1.db") 
            cur = con.cursor()
            cur.execute("DROP TABLE SchoolBells")
            con.commit()
            con.close()
            #print("table dropped successfully")
            flash("Successfully Cleared the Database")
            return redirect(url_for('create'))
        except:
            return "<h1>Error, Table is already deleted</<h1>"
    else:
        abort(404)

@app.route("/alarmschedule",methods=["GET","POST"])
def alarmschedule():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        if request.method=="POST":
            if request.form.get("external")=="submit":
                return redirect(url_for('create'))
            elif request.form.get("external")=="clear":
                return redirect(url_for('clear'))
            elif request.form.get("external")=="display":
                return redirect(url_for('alarmschedule'))

        try:
            con = sql.connect("real1.db")
            con.row_factory = sql.Row 
            cur = con.cursor()
            cur.execute("SELECT SNO,TIME,BELLS,COUNT FROM SchoolBells")
            rows = cur.fetchall()
            return render_template('scheduledisplayer1.html',items= rows)
        except:
            return "<h1>Error , create a table</h1>"
    else:
        abort(404)

@app.route('/decision',methods = ['GET','POST'])
def decision():
    a = request.form
    print(a)

if __name__=='__main__':
    app.run(debug = True)
    #app.run(host='0.0.0.0',port=8080,debug=True,use_reloader=True)
        
