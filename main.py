from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:popcorn4@localhost:8889/blogz'
app.config ['SQLALCHEMY_ECHO']=True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.secret_key = "#19821604ayirp"

class Blog(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120))
    blog_content = db.Column(db. Text)
    completed = db.Column(db.Boolean)
    owner_id= db.Column(db. Integer, db.ForeignKey('user.id'))

    def __init__ (self, title, blog_content,owner):
        self.title = title
        self.blog_content = blog_content
        self.completed= False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks= db.relationship('Blog', backref ='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email= request.form ['email']
        password = request.form ['password']
        user= User.query.filter_by(email= email).first()

        if user and user.password == password:
            session['email']= email
            flash("Logged in")
            return redirect('/todos')
        else:
            flash('User password incorrect or user does not exists', 'error')
            

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        email= request.form ['email']
        password = request.form ['password']
        verify = request.form['verify']
        existing_user= User.query.filter_by(email=email).first()
        if not existing_user:
            new_user=User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email']=email
            return redirect('/')
        else:
            #TODO user better response messaging
            return "<h1>Duplicate User </h1>"
    return render_template('signup.html')           
    
    
@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    return redirect('/')




"""@app.route('/', defaults={'id':0})
@app.route('/display/<int:id>')
def index(id):
    if id:
        update_blog=Blog.query.get(id)
        return render_template('display.html',title="Add a Blog", update_blog=update_blog)

    update_blog = Blog.query.filter_by().all()
    return render_template('first.html',title="Build a Blog", 
         update_blog=update_blog )"""


@app.route('/todos', methods=['POST', 'GET'])
def add_blog():
    owner = User.query.filter_by(email= session['email']).first()
    if request.method == 'POST':
        task_title= request.form['title']
        task_blog_content= request.form['blog_content']
        if task_title=='':
            error="Please specify the blog title"
            return redirect ('/todos?title_error='+error )
        if task_blog_content=='':
            error="please specify the blog content"
            return redirect ('/todos?blog_content_error=' +error +'&title='+task_title)
        update_blog =Blog(task_title,task_blog_content,owner)
        db.session.add(update_blog)
        db.session.commit()
        return render_template('display.html',title="Add a Blog", update_blog=update_blog)
    else:
        title_error=request.args.get("title_error")
        blog_content_error= request.args.get("blog_content_error")
        task_title=request.args.get("title")
        if not task_title:
            task_title=''
        return render_template ('todos.html', title= "Add a Blog", title_error=title_error, 
        blog_content_error=blog_content_error)

@app.route('/', defaults={'id':0,'email':''})
@app.route('/display/<int:id>',defaults={'email':''})
@app.route('/display/<email>',defaults={'id':0})
def index(id, email):
    user_name=User.query.filter_by().all()
    if id:
        update_blog = Blog.query.get(id)
        return render_template('display.html',title="Details of Blogs", 
         update_blog=update_blog )
    if email:
        user_blog=User.query.filter_by(email=email).first()
        update_blog=Blog.query.filter_by(owner=user_blog).first()
        return render_template('singleUser.html',title="Add a Blog", update_blog=update_blog)
    
    return render_template('first.html', title="Blog Users!", user_name=user_name)

if __name__ == '__main__':
    app.run() 