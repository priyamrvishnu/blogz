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
    username=db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks= db.relationship('Blog', backref ='owner', lazy='dynamic')

    def __init__(self, username, password, email):
        self.email = email
        self.username=username
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
    username = request.form['username']
    passwd = request.form['password']
    confi_pass = request.form['verify']
    e_mail = request.form['email']

    username_error = ''
    passwd_error = ''
    confi_pass_error=''
    e_mail_error=''

    numupper =0
    numlower =0
    numdigit=0
    for c in username:
        if c.isupper():
            numupper = numupper + 1
        if c.islower():
            numlower = numlower + 1
        if c.isdigit():
            numdigit = numdigit + 1


    if numupper <= 0:
        username_error=('username must contain at least one uppercase character')
        
       
    if numlower <= 0:
        username_error=('username must contain at least one lowercase character')
        

    if len(username)<6:
        username_error = ('username must be greater than 6 characters')
        
          
    if numdigit <= 0:
        username_error= ('username must contain at least one number')
           

    numupper =0
    numlower =0
    numdigit=0
    for c in passwd:
        if c.isupper():
           numupper = numupper + 1
        if c.islower():
            numlower = numlower + 1
        if c.isdigit():
            numdigit = numdigit + 1

    if numupper <= 0:
        passwd_error=('password must contain at least one uppercase character')
        passwd=''

    elif numlower <= 0:
        passwd_error=('password must contain at least one lowercase character')
        passwd=''

    elif len(passwd)<8:
        passwd_error = ('password must be greater than 8 characters')
        passwd=''

    else:
        if numdigit <= 0:
            passwd_error= ('password must contain at least one number')
            passwd=''
    
    if confi_pass == passwd:
        confi_pass=''
    else:
        confi_pass_error= ('Password does not Match')   

    if '@' not in e_mail or '.com' not in e_mail:
        e_mail_error=('Not a valid email')



    if not username_error and not passwd_error and not confi_pass_error and not e_mail_error:
        return render_template('login.html', name= username)
    else:
        return redirect('/?username_error='+username_error+
        '&passwd_error='+passwd_error+
        '&confi_pass_error='+confi_pass_error+
        '&e_mail_error='+e_mail_error+
        '&username='+username+
        '&passwd='+passwd+
        '&confi_pass='+confi_pass+
        '&e_mail='+e_mail)   

    existing_user= User.query.filter_by(email=email).first()
    if not existing_user:
        new_user=User(username,password,email)
        db.session.add(new_user)
        db.session.commit()
        session['email']=email
        return redirect('/')
    else:
        flash("You already have an account. Please login")
        return redirect('/login')  
    return render_template('signup.html',pgtitle="Signup")           
    
    
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

@app.route('/', defaults={'id':0,'username':''})
@app.route('/display/<int:id>',defaults={'username':''})
@app.route('/display/<username>',defaults={'id':0})
def index(id, username):
    user_name=User.query.filter_by().all()
    if id:
        update_blog = Blog.query.get(id)
        return render_template('display.html',title="Details of Blogs", 
         update_blog=update_blog )
    if email:
        user_blog=User.query.filter_by(username=username).first()
        tasks=Blog.query.filter_by(owner=user_blog).all()
        return render_template('singleUser.html',title="Add a Blog", tasks=tasks)
    
    return render_template('first.html', title="Blog Users!", user_name=user_name)

if __name__ == '__main__':
    app.run() 