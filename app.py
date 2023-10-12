import os
import sqlite3 as sql
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('member/login.html')

@app.route('/member/join', methods = ['POST', 'GET'])
def join():
    if request.method == 'POST':
        pass
    else:
        return render_template('member/join.html')

@app.route('/board/')
def board():
    con = sql.connect('database.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM homepage")

    rows = cur.fetchall()
    return render_template('board/index.html', rows = rows)

@app.route('/board/write')
def write():
    return render_template('board/write.html')

@app.route('/board/<int:num>')
def view(num):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM homepage WHERE num=?", (num, ))
    post = cur.fetchall()
    return render_template('board/view.html', post=post)

@app.route('/board/update', methods = ['POST'])
def edit():
    if request.method == 'POST':
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM homepage WHERE num=?", (int(request.form['num']), ))
        post = cur.fetchall()
        return render_template('board/edit.html', post=post)

@app.route('/board/resadd', methods = ['POST'])
def add():
    if request.method == 'POST':
        try:
            id = request.form['userid']
            pw = request.form['pw']
            title = request.form['title']
            content = request.form['content']
            
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT MAX(num) FROM homepage")
                num = cur.fetchall()
                try:
                    cur.execute("INSERT INTO homepage (num, userid, pw, title, content) VALUES (?,?,?,?,?)", (int(num[0][0]) + 1, id, pw, title, content))
                except:
                    cur.execute("INSERT INTO homepage (num, userid, pw, title, content) VALUES (?,?,?,?,?)", (1, id, pw, title, content))
                    
                con.commit()
                msg = "업로드 성공"
        except:
            con.rollback()
            msg = "업로드 실패"
        
        finally:
            return msg
        
@app.route('/board/resdel', methods = ['POST'])
def delete():
    if request.method == 'POST':
        try:
            num = request.form['num']
            
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM homepage WHERE num=?", (int(num), ))
                
                con.commit()
                msg = "삭제 성공"
        except:
            con.rollback()
            msg = "삭제 실패"
        
        finally:
            return msg
        
@app.route('/board/resup', methods = ['POST'])
def update():
    if request.method == 'POST':
        try:
            id = request.form['userid']
            pw = request.form['pw']
            title = request.form['title']
            content = request.form['content']
            
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE homepage SET userid = ?, pw = ?, title = ?, content = ?", (id, pw, title, content))
                
                con.commit()
                msg = "수정 성공"
        except:
            con.rollback()
            msg = "수정 실패"
        
        finally:
            return msg

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)