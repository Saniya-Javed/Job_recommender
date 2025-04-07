from flask import Flask, render_template,  request, redirect, url_for, jsonify
import sqlite3
import base64
import pickle
import pickle
import json
import requests
import time
from pprint import pprint

app = Flask(__name__)

with open('jobs.pkl', 'rb') as f:
    pickled_model = pickle.load(f)

roll=['AI ML Specialist','API Specialist','Application Support Engineer','Business Analyst','Customer Service Executive', 'Cyber Security Specialist','Data Scientist'
    ,'Database Administrator','Graphics Designer','Hardware Engineer','Helpdesk Engineer','Information Security Specialist','Networking Engineer',
    'Project Manager','Software Developer','Software tester','Technical Writer']

connection = sqlite3.connect('job_recommend.db')
curcsor = connection.cursor()

curcsor.execute("create table if not exists admin(username TEXT, password TEXT)")
curcsor.execute("CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, gmail TEXT, profile BLOB, resume TEXT)")
curcsor.execute("create table if not exists academics(gmail TEXT, course TEXT, university TEXT, result TEXT, passout TEXT)")
curcsor.execute("create table if not exists summury(gmail TEXT, summuries TEXT)")
curcsor.execute("create table if not exists activity(gmail TEXT, activities TEXT)")
curcsor.execute("create table if not exists strength(gmail TEXT, strengths TEXT)")
curcsor.execute("create table if not exists personal(fname TEXT, lname TEXT, bday TEXT, gender TEXT, pnum TEXT, gmail TEXT, caddress TEXT, paddress TEXT, languages TEXT, marital TEXT, declaration TEXT)")
curcsor.execute("create table if not exists other(objective TEXT, skill TEXT, tool TEXT, db TEXT, sos TEXT , title TEXT, srvr TEXT, pos TEXT, team TEXT, tech TEXT, desp TEXT, gmail TEXT)")
curcsor.execute("create table if not exists jobs(title TEXT, applylink TEXT, jobdescription TEXT, companyname TEXT, location TEXT, salary TEXT, skills TEXT, enddate TEXT, source TEXT, experience TEXT, gmail TEXT)")

def send_msg(msg):
    import telepot
    bot = telepot.Bot("6303507420:AAEM4z686sOLRiy2F2FSfV_9gYDIKPoQ_HU")
    bot.sendMessage("1713688024", str(msg))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buildresume')
def buildresume():
    f = open('session.txt', 'r')
    email = f.read()
    f.close()
    return render_template('buildresume.html', email=email)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route("/exam",methods=["POST","GET"])
def exam():
    if request.method == 'POST':
        data = request.form
        print("===================================")
        print(data)
        user_answers = []
        for key in data:
            user_answers.append(int(data[key]))
            
        print(user_answers)
        answers = [3,4,1,1,3]
        score = 0
        
        for i in range(5):
            if user_answers[i] == answers[i]:
                score = score + 5
        print(score)

        if score >= 20:
            text="You Are Excellent !!"
        elif (score >= 10 and score < 20):
            text="You Can Be Better !!"
        else:
            text="You Should Work Hard !!"
            
        print("===================================")
        return jsonify(text)
    return jsonify("error")

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        data = request.form
        skills = []
        for key in data:
            skills.append(int(data[key]))
        print(skills)
        out = pickled_model.predict([skills])
        print(roll[out[0]])
        return render_template('jobs.html', pred=roll[out[0]])
    return render_template('jobs.html')

@app.route('/profile')
def profile():
    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()
    
    f = open('session.txt', 'r')
    email = f.read()
    f.close()

    cursor.execute("SELECT resume FROM user WHERE gmail = '"+email+"'")
    result = cursor.fetchone()
    print(result[0])

    if result[0] == 'yes':
        cursor.execute("SELECT profile FROM user WHERE gmail = '"+email+"'")
        dp = cursor.fetchone()

        cursor.execute("SELECT * FROM other WHERE gmail = '"+email+"'")
        result = cursor.fetchone()
        
        objective, skill, tool, db, sos, title, srvr, pos, team, tech, desp = result[:-1]

        cursor.execute("SELECT * FROM personal WHERE gmail = '"+email+"'")
        result = cursor.fetchone()

        fname, lname, bday, gender, pnum, gid, caddress, paddress, languages, marital, declaration = result
        fullname = fname+' '+lname

        cursor.execute("SELECT course, university, result, passout FROM academics WHERE gmail = '"+email+"'")
        academic = cursor.fetchall()

        cursor.execute("SELECT summuries FROM summury WHERE gmail = '"+email+"'")
        summury = cursor.fetchall()

        cursor.execute("SELECT activities FROM activity WHERE gmail = '"+email+"'")
        activity = cursor.fetchall()

        cursor.execute("SELECT strengths FROM strength WHERE gmail = '"+email+"'")
        strength = cursor.fetchall()

        cursor.execute("SELECT profile FROM user WHERE gmail = '"+email+"'")
        dp = cursor.fetchone()
        dp = dp[0].decode('utf-8')

        return render_template('profile.html', dp=dp, ud=result[0], objective=objective, declaration=declaration,marital=marital,
            languages=languages,paddress=paddress, caddress=caddress,gid=gid,pnum=pnum,gender=gender,bday=bday,
            fullname=fullname,lname=lname,fname=fname,strength=strength,activities=activity,desp=desp,tech=tech,
            team=team,pos=pos,srvr=srvr,title=title,sos=sos,db=db,tool=tool,skill=skill,summury=summury,academic=academic)
    else:
        return render_template('profile.html')

@app.route('/download')
def download():
    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()
    
    f = open('session.txt', 'r')
    email = f.read()
    f.close()

    cursor.execute("SELECT profile FROM user WHERE gmail = '"+email+"'")
    dp = cursor.fetchone()

    cursor.execute("SELECT * FROM other WHERE gmail = '"+email+"'")
    result = cursor.fetchone()
    
    objective, skill, tool, db, sos, title, srvr, pos, team, tech, desp = result[:-1]

    cursor.execute("SELECT * FROM personal WHERE gmail = '"+email+"'")
    result = cursor.fetchone()

    fname, lname, bday, gender, pnum, gid, caddress, paddress, languages, marital, declaration = result
    fullname = fname+' '+lname

    cursor.execute("SELECT course, university, result, passout FROM academics WHERE gmail = '"+email+"'")
    academic = cursor.fetchall()

    cursor.execute("SELECT summuries FROM summury WHERE gmail = '"+email+"'")
    summury = cursor.fetchall()

    cursor.execute("SELECT activities FROM activity WHERE gmail = '"+email+"'")
    activity = cursor.fetchall()

    cursor.execute("SELECT strengths FROM strength WHERE gmail = '"+email+"'")
    strength = cursor.fetchall()

    cursor.execute("SELECT profile FROM user WHERE gmail = '"+email+"'")
    dp = cursor.fetchone()
    dp = dp[0].decode('utf-8')

    return render_template('resume.html', dp=dp, ud=result[0], objective=objective, declaration=declaration,marital=marital,
        languages=languages,paddress=paddress, caddress=caddress,gid=gid,pnum=pnum,gender=gender,bday=bday,
        fullname=fullname,lname=lname,fname=fname,strength=strength,activities=activity,desp=desp,tech=tech,
        team=team,pos=pos,srvr=srvr,title=title,sos=sos,db=db,tool=tool,skill=skill,summury=summury,academic=academic)

@app.route('/adminhome')
def adminhome():
    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    return render_template('adminpage.html', result=result)

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        connection = sqlite3.connect('job_recommend.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        if name == 'admin@gmail.com' and password == 'admin123':
            cursor.execute("SELECT * FROM user")
            result = cursor.fetchall()
            return render_template('adminpage.html', result=result)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('job_recommend.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        cursor.execute("SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'")
        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            cursor.execute("SELECT gmail FROM user WHERE name = '"+name+"' AND password= '"+password+"'")
            result = cursor.fetchone()
            
            f = open('session.txt', 'w')
            f.write(result[0])
            f.close()

            return redirect(url_for('profile'))

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('job_recommend.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        dp = request.form['dp']
        
        cursor.execute("SELECT * FROM user WHERE gmail = '"+email+"'")
        result = cursor.fetchall()

        if len(result) == 0:
            with open(dp, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            
            List =  [name, password, mobile, email, my_string, 'no']
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", List)
            connection.commit()

            return render_template('index.html', msg='Successfully Registered')
        else:
            return render_template('index.html', msg='email already exissts')

    return render_template('index.html')

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        objective = request.form['objective']
        skill = request.form['skill']
        tool = request.form['tool']
        db = request.form['db']
        sos = request.form['sos']
        title = request.form['title']
        srvr = request.form['srvr']
        pos = request.form['pos']
        team = request.form['team']
        tech = request.form['tech']
        desp = request.form['desp']

        fname = request.form['fname'] 
        lname = request.form['lname']
        fullname = fname+' '+lname
        bday = request.form['bday']
        gender = request.form['gender']
        pnum = request.form['pnum']
        gid = request.form['gid']
        caddress = request.form['caddress']
        paddress = request.form['paddress']
        languages = request.form['languages']
        marital = request.form['marital']
        declaration = request.form['declaration']

        other_info = [objective, skill, tool, db, sos, title, srvr, pos, team, tech, desp, gid]
        personal_info = [fname, lname, bday, gender, pnum, gid, caddress, paddress, languages, marital, declaration]
        academic=[]
        i=0
        while True:
            try:
                course = request.form['course['+str(i)+']']
                university = request.form['university['+str(i)+']']
                result = request.form['result['+str(i)+']']
                passout = request.form['passout['+str(i)+']']
                academic.append([gid, course, university, result,  passout])
                i += 1
            except Exception as e:
                print(str(e))
                break    
        summury = [] 
        j=0
        while True:
            try:
                sm = request.form['summury['+str(j)+']']
                summury.append([gid, sm])
                j += 1
            except Exception as e:
                print(str(e))
                break
       
        activities = [] 
        k=0
        while True:
            try:
                ac = request.form['activities['+str(k)+']']
                activities.append([gid, ac])
                k += 1
            except Exception as e:
                print(str(e))
                break
        
        strength = [] 
        l=0
        while True:
            try:
                st = request.form['strength['+str(l)+']']
                strength.append([gid, st])
                l += 1
            except Exception as e:
                print(str(e))
                break
        
        print(objective, declaration,marital,languages,paddress
        ,caddress,gid,pnum,gender,bday,fullname,lname,fname,strength,
        activities,desp,tech,team,pos,srvr,title,sos,db,tool,skill,summury,academic)

        connection = sqlite3.connect('job_recommend.db')
        cursor = connection.cursor()

        for row in academic:
            cursor.execute("insert into academics values(?, ?, ?, ?, ?)", row)
            connection.commit()

        for row in summury:
            cursor.execute("insert into summury values(?, ?)", row)
            connection.commit()
        
        for row in activities:
            cursor.execute("insert into activity values(?, ?)", row)
            connection.commit()
        
        for row in strength:
            cursor.execute("insert into strength values(?, ?)", row)
            connection.commit()

        cursor.execute("insert into personal values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", personal_info)
        connection.commit()
        
        cursor.execute("insert into other values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", other_info)
        connection.commit()

        cursor.execute("update user set resume = 'yes' where gmail = '"+gid+"'")
        connection.commit()

        return redirect(url_for('profile'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/posts/<job>')
def posts(job):
    print(job)
    try:
        timestamp = time.time()
        headers = json.load(open('headers.json'))
        json_filename = './files/timesjobs.json'
        fp = open(json_filename, 'w')

        url = 'https://jobbuzz.timesjobs.com/jobbuzz/loadMoreJobs.json?companyIds=&locationnames=198130$&aosValues=&sortby=Y&from=filter&faids=&txtKeywords='+job+'&pSize=19'
        response = requests.get(url)
        jobs = json.loads(response.text)
        jobs = jobs['jobsList']

        joblist = []
        heading = ['title', 'apply link', 'job description', 'company name', 'location', 'salary', 'skills', 'enddate', 'source', 'experience']
        pprint(heading)
        for job in jobs:
            row = dict.fromkeys(headers)
            title = job['title']
            applylink = 'http://www.timesjobs.com/candidate/' + job['jdUrl']
            jd = job['jobDesc']
            companyname = job['companyName']
            location = job['Location']
            salary = job['salary']
            skills = ", ".join([x.strip().strip("\"") for x in job['keySkills']])
            enddate = job['expiry']
            source = 'timesjobs'
            experience = job['experience'] + " yrs"
            joblist.append([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])
            pprint([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])            
        json.dump(joblist, fp)
        fp.close()
        return render_template('posts.html', joblist=joblist, heading=heading)

    except Exception as ex:
        return render_template('posts.html', msg='posts not found')

@app.route('/jobsearch', methods=['GET', 'POST'])
def jobsearch():
    if request.method == 'POST':
        job = request.form['job']
        print(job)
        try:
            timestamp = time.time()
            headers = json.load(open('headers.json'))
            json_filename = './files/timesjobs.json'
            fp = open(json_filename, 'w')
            
            url = 'https://jobbuzz.timesjobs.com/jobbuzz/loadMoreJobs.json?companyIds=&locationnames=198130$&aosValues=&sortby=Y&from=filter&faids=&txtKeywords='+job+'&pSize=19'
            response = requests.get(url)
            jobs = json.loads(response.text)
            jobs = jobs['jobsList']

            joblist = []
            heading = ['title', 'apply link', 'job description', 'company name', 'location', 'salary', 'skills', 'enddate', 'source', 'experience']
            pprint(heading)
            for job in jobs:
                row = dict.fromkeys(headers)
                title = job['title']
                applylink = 'http://www.timesjobs.com/candidate/' + job['jdUrl']
                jd = job['jobDesc']
                companyname = job['companyName']
                location = job['Location']
                salary = job['salary']
                skills = ", ".join([x.strip().strip("\"") for x in job['keySkills']])
                enddate = job['expiry']
                source = 'timesjobs'
                experience = job['experience'] + " yrs"
                joblist.append([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])
                pprint([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])            
            json.dump(joblist, fp)
            fp.close()
 
            return render_template('allpost.html', joblist=joblist, heading=heading)

        except Exception as ex:
            print(ex)
            return render_template('allpost.html', msg='posts not found')
    
    return render_template('index.html')


@app.route('/jobsearch1', methods=['GET', 'POST'])
def jobsearch1():
    if request.method == 'POST':
        job = request.form['job']
        print(job)
        try:
            timestamp = time.time()
            headers = json.load(open('headers.json'))
            json_filename = './files/timesjobs.json'
            fp = open(json_filename, 'w')
            
            url = 'https://jobbuzz.timesjobs.com/jobbuzz/loadMoreJobs.json?companyIds=&locationnames=198130$&aosValues=&sortby=Y&from=filter&faids=&txtKeywords='+job+'&pSize=19'
            response = requests.get(url)
            jobs = json.loads(response.text)
            jobs = jobs['jobsList']

            joblist = []
            heading = ['title', 'apply link', 'job description', 'company name', 'location', 'salary', 'skills', 'enddate', 'source', 'experience']
            pprint(heading)
            for job in jobs:
                row = dict.fromkeys(headers)
                title = job['title']
                applylink = 'http://www.timesjobs.com/candidate/' + job['jdUrl']
                jd = job['jobDesc']
                companyname = job['companyName']
                location = job['Location']
                salary = job['salary']
                skills = ", ".join([x.strip().strip("\"") for x in job['keySkills']])
                enddate = job['expiry']
                source = 'timesjobs'
                experience = job['experience'] + " yrs"
                joblist.append([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])
                pprint([title, applylink, jd, companyname, location, salary, skills, enddate, source, experience])            
            json.dump(joblist, fp)
            fp.close()
 
            return render_template('posts.html', joblist=joblist, heading=heading)

        except Exception as ex:
            print(ex)
            return render_template('posts.html', msg='posts not found')
    
    return render_template('search.html')

@app.route('/view/<email>')
def view(email):
    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM other WHERE gmail = '"+email+"'")
    result = cursor.fetchone()
    
    objective, skill, tool, db, sos, title, srvr, pos, team, tech, desp = result[:-1]

    cursor.execute("SELECT * FROM personal WHERE gmail = '"+email+"'")
    result = cursor.fetchone()

    fname, lname, bday, gender, pnum, gid, caddress, paddress, languages, marital, declaration = result
    fullname = fname+' '+lname

    cursor.execute("SELECT course, university, result, passout FROM academics WHERE gmail = '"+email+"'")
    academic = cursor.fetchall()

    cursor.execute("SELECT summuries FROM summury WHERE gmail = '"+email+"'")
    summury = cursor.fetchall()

    cursor.execute("SELECT activities FROM activity WHERE gmail = '"+email+"'")
    activity = cursor.fetchall()

    cursor.execute("SELECT strengths FROM strength WHERE gmail = '"+email+"'")
    strength = cursor.fetchall()

    return render_template('viewresume.html', ud=result[0], objective=objective, declaration=declaration,marital=marital,
        languages=languages,paddress=paddress, caddress=caddress,gid=gid,pnum=pnum,gender=gender,bday=bday,
        fullname=fullname,lname=lname,fname=fname,strength=strength,activities=activity,desp=desp,tech=tech,
        team=team,pos=pos,srvr=srvr,title=title,sos=sos,db=db,tool=tool,skill=skill,summury=summury,academic=academic)

@app.route('/appliedjobs')
def appliedjobs():
    f = open('session.txt', 'r')
    email = f.read()
    f.close()

    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()

    cursor.execute("select * from jobs where gmail = '"+email+"'")
    joblist = cursor.fetchall()

    heading = ['title', 'apply link', 'job description', 'company name', 'location', 'salary', 'skills', 'enddate', 'source', 'experience']
    return render_template('appliedjobs.html', joblist=joblist, heading=heading)

@app.route('/applied_jobs/<In>')
def applied_jobs(In):
    f = open('session.txt', 'r')
    email = f.read()
    f.close()

    data = json.load(open('./files/timesjobs.json'))
    data = data[int(In)]

    data.append(email)

    print(data)

    connection = sqlite3.connect('job_recommend.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    connection.commit()

    send_msg('Successfully applied for job {}'.format(data[1]))
    return redirect(url_for('appliedjobs'))

@app.route('/update_pass', methods=['GET', 'POST'])
def update_pass():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        otp = int(request.form['otp'])

        f = open('OTP.txt', 'r')
        otp1 = f.readline()
        otp1 = int(otp1)
        f.close()

        if otp == otp1:
            con = sqlite3.connect('job_recommend.db')
            cr = con.cursor()
            
            cr.execute("SELECT * FROM user WHERE gmail = '"+email+"'")
            result = cr.fetchall()
            if result:
                cr.execute("update user set password = '"+password+"' where gmail = '"+email+"' ")
                con.commit()

                return render_template('index.html', msg="password updated successfully")
            else:
                return render_template('index.html', msg="Entered wrong mail id")
        else:
            return render_template('index.html', msg="Entered wrong otp")
    return render_template('index.html')

@app.route('/getotp')
def getotp():
    import random
    number = random.randint(1000,9999)
    number = str(number)
    print(number)
    f = open('OTP.txt', 'w')
    f.write(number)
    f.close()
    send_msg(number)
    return jsonify('otp sent')

@app.route('/select/<email>')
def select(email):
    print(email)
    send_msg('hi {}, you are selected'.format(email))
    return redirect(url_for('adminhome'))

@app.route('/reject/<email>')
def reject(email):
    print(email)
    send_msg('hi {}, you are rejected'.format(email))
    return redirect(url_for('adminhome'))

if __name__ == "__main__":
    app.run(debug=True)
