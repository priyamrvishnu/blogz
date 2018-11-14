from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:popcorn4@localhost:8889/build-a-blog'
app.config ['AQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)

class Blog(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120))
    blog_content = db.Column(db. Text)

    def __init__ (self, title, blog_content):
        self.title = title
        self.blog_content = blog_content

@app.route('/', defaults={'id':0})
@app.route('/display/<int:id>')
def index(id):
    if id:
        update_blog=Blog.query.get(id)
        return render_template('display.html',title="Add a Blog", update_blog=update_blog)

    update_blog = Blog.query.filter_by().all()
    return render_template('first.html',title="Build a Blog", 
         update_blog=update_blog )


@app.route('/todos', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        task_title= request.form['title']
        task_blog_content= request.form['blog_content']
        if task_title=='':
            error="Please specify the blog title"
            return redirect ('/todos?title_error='+error )
        if task_blog_content=='':
            error="please specify the blog content"
            return redirect ('/todos?blog_content_error=' +error +'&title='+task_title)
        update_blog =Blog(task_title,task_blog_content)
        db.session.add(update_blog)
        db.session.commit()
        return render_template('display.html',title="Add a Blog", update_blog=update_blog)
    else:
        title_error=request.args.get("title_error")
        blog_content_error= request.args.get("blog_content_error")
        task_title=request.args.get("title")
        if not task_title:
            task_title=''
        return render_template ('todos.html', title= "Add a Blog", title_error=title_error, blog_content_error=blog_content_error)


if __name__ == '__main__':
    app.run() 