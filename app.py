from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///exam.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = "clubtest"

class Passive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)   
    mail = db.Column(db.String(255), nullable=False)
    m_pass = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False) 
    roll = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer) 

    def __repr__(self) -> str:
        return f"{self.id} {self.name} {self.mail} {self.m_pass} {self.year} {self.roll} {self.marks}"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    que = db.Column(db.String(255), nullable=False)  
    op1 = db.Column(db.String(255), nullable=False)  
    op2 = db.Column(db.String(255), nullable=False)  
    op3 = db.Column(db.String(255), nullable=False)  
    op4 = db.Column(db.String(255), nullable=False)  
    cans = db.Column(db.String(255), nullable=False)  
    year = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} {self.que} {self.op1} {self.op2} {self.op3} {self.op4} {self.cans}"

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/login')
def login():
    return render_template('home.html')

@app.route('/passive-log', methods=['GET', 'POST'])
def passive_log():
    if request.method == 'POST':
        mail = request.form['mail']
        passw = request.form['pass']
        print(mail)
        print(passw)
        # if mail == "passive@gmail.com" and passw == "password":
        #     session["user"] = mail            
        #     return redirect(url_for('register'))
        # if mail == "admin@gmail.com" and passw == "admin123":
        #     return redirect(url_for('dashboard'))
        # else:
        #     return render_template('index.html')
        umail = Passive.query.filter_by(mail=mail).first()
        if umail:
            if passw==umail.m_pass:
                session["user"] = mail
                return redirect(url_for('exam'))
        return redirect(url_for('passive_log'))

@app.route('/', methods=['GET', 'POST'])
def register():        
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        m_pass = request.form['pass']        
        year = request.form['year']    
        roll = request.form['roll'] 
        marks = 0       
        stud = Passive(name=name, mail=mail, m_pass=m_pass, year=year, roll=roll, marks=marks)        
        db.session.add(stud)        
        db.session.commit()        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/addquestion', methods=['GET', 'POST'])
def dash():
    return render_template('addquestion.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('results.html')    

@app.route('/addques', methods=['GET', 'POST'])
def addques():
    print("Entered in function")
    if request.method == 'POST':
        print("Entered in if")
        que = request.form['ques']        
        op1 = request.form['op1']        
        op2 = request.form['op2']
        op3 = request.form['op3']
        op4 = request.form['op4']
        cans = request.form['cans']
        year = request.form['year']        
        ques = Question(que=que, op1=op1, op2=op2, op3=op3, op4=op4, cans=cans, year=year)
        db.session.add(ques)        
        db.session.commit()
        return render_template('addquestion.html')
        # return "Success"
    return render_template('dash.html')

@app.route('/exam', methods=['GET', 'POST'])
def exam():
    mail = session["user"]
    stud = Passive.query.filter_by(mail=mail).first()
    # if stud.year == "TY":
    #     return "TY"
    # if stud.year == "SY":
    ques = Question.query.filter_by(year=stud.year)
    # ques = Question.query.all()
    return render_template('exam.html', ques=ques)    

@app.route('/allquestion', methods=['GET', 'POST'])
def allquestion():
    ques = Question.query.filter_by(year="SY")
    return render_template('allquestions.html', ques=ques)    

@app.route('/tyquestion', methods=['GET', 'POST'])
def tyquestion():
    ques = Question.query.filter_by(year="TY")
    return render_template('tyquestions.html', ques=ques)  


@app.route('/check', methods=['GET', 'POST'])
def check():
    result = 0
    mail = session["user"]
    stud = Passive.query.filter_by(mail=mail).first()
    # question = Question.query.all()
    question = Question.query.filter_by(year=stud.year)
    for quest in question:
        quest_id = str(quest.id)
        print("Question id : "+quest_id)
        select = request.form[quest_id]   
        print("Selected id : "+ select)
        correct = quest.cans
        if select == correct:
            result = result + 1
            print("correct")
        else:
            print("wrong")
    
    # marks = str(result)
    marks = result
    # mail = session["user"]
    # stud_det = Passive.query.filter_by(mail=mail).first()
    stud.marks = marks
    db.session.add(stud)
    db.session.commit()
    # stud_det = Stud.query.filter_by(mob=mob).first()       
    # print(marks)
    marks = str(result)
    print(marks)
    return redirect(url_for('submit'))

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/syresult', methods=['GET', 'POST'])
def syresult():
    res = Passive.query.filter_by(year="SY")
    return render_template('results.html', res=res) 

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
