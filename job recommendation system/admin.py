import sqlite3

con = sqlite3.connect('job_recommend.db')
cr = con.cursor()

cr.execute("create table if not exists admin(username TEXT, password TEXT)")

cr.execute("insert into admin values('admin', 'admin')")
con.commit()
