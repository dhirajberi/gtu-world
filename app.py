from flask import *
import requests
import os
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gtuworld.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

upload_location = os.getcwd() + "/static/img/blog"
app.config['UPLOAD_FOLDER'] = upload_location

db = SQLAlchemy(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gtuworld.official@gmail.com'
app.config['MAIL_PASSWORD'] = 'beri@007'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Model for blog page
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(20), default="Dhiraj Beri")
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title

# Admin Panel
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check if username and password is correct or not
        if username=="dhiraj" and password=="beri@007":
            blogs = Blog.query.all()
            return render_template('admin.html', blogs=blogs)
        else:
            return render_template('login.html')
    return render_template('login.html')

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        msg = Message(
            f'New message recieved by {name}',
            sender ='gtuworld.official@gmail.com',
            recipients = ['digitalberi@gmail.com']
        )
        msg.body = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """
        mail.send(msg)
        return "Your message send successfully"

    return redirect('/#contact')

# Blog Page
@app.route('/blog')
def blog():
    # Fetch
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

# Add blog post
@app.route('/admin/add-blog', methods=['GET', 'POST'])
def add_blog():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        slug = request.form['slug']
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        content = request.form['content']

        blog = Blog(
            title = title,
            description = description,
            author = "Dhiraj Beri",
            slug = slug,
            image = secure_filename(image.filename),
            content = content
        )
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog')
    return render_template('add-blog.html')

# Update blog post
@app.route('/admin/update-blog/<string:slug>', methods=['GET', 'POST'])
def update_blog(slug):
    if request.method=='POST':
        blogpost = Blog.query.filter_by(slug=slug).first()

        title = request.form['title']
        description = request.form['description']
        slug = request.form['slug']
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        content = request.form['content']

        blogpost.title = title
        blogpost.description = description
        blogpost.slug = slug
        blogpost.image = secure_filename(image.filename)
        blogpost.content = content

        db.session.commit()
        return redirect('/blog')

    blogpost = Blog.query.filter_by(slug=slug).first()
    return render_template('update-blog.html', blogpost=blogpost)

# Delete blog post
@app.route('/admin/delete-blog/<string:slug>', methods=['GET', 'POST'])
def delete_blog(slug):
    blogpost = Blog.query.filter_by(slug=slug).first()
    db.session.delete(blogpost)
    db.session.commit()
    return redirect('/blog')

# Truncate blog database (dummy records)
@app.route('/truncate-blogs')
def truncate_blogs():
    db.session.query(Blog).delete()
    db.session.commit()
    return render_template('/blog')

# Blogpost Page
@app.route('/blog/<string:slug>')
def blogpost(slug):
    blogpost = Blog.query.filter_by(slug=slug).first()
    title = blogpost.title
    description = blogpost.description
    image = blogpost.image
    author = blogpost.author
    content = blogpost.content
    return render_template('blog-single.html', title=title, image=image, author=author, content=content, description=description, slug=slug)

# Policy Page
@app.route('/privacy-policy')
def policy():
    return render_template('privacy-policy.html')

# robots.txt
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

# ads.txt
@app.route("/ads.txt")
def ads():
    return send_from_directory("static", "ads.txt")

# sitemap.xml
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

# GTU Papers
@app.route('/gtu-papers', methods=['GET', 'POST'])
def papers():
    if request.method == 'POST':
        branch = request.form['branch']
        code = request.form['code']
        print(branch, code)

        paper1 = f"https://www.gtu.ac.in/uploads/W2021/{branch}/{code}.pdf"
        paper2 = f"https://www.gtu.ac.in/uploads/W2020/{branch}/{code}.pdf"
        paper3 = f"https://www.gtu.ac.in/uploads/W2019/{branch}/{code}.pdf"
        paper4 = f"https://www.gtu.ac.in/uploads/W2018/{branch}/{code}.pdf"
        paper5 = f"https://www.gtu.ac.in/uploads/W2017/{branch}/{code}.pdf"
        paper6 = f"https://www.gtu.ac.in/uploads/S2021/{branch}/{code}.pdf"
        paper7 = f"https://www.gtu.ac.in/uploads/S2020/{branch}/{code}.pdf"
        paper8 = f"https://www.gtu.ac.in/uploads/S2019/{branch}/{code}.pdf"
        paper9 = f"https://www.gtu.ac.in/uploads/S2018/{branch}/{code}.pdf"

        r1 = requests.get(paper1)
        r2 = requests.get(paper2)
        r3 = requests.get(paper3)
        r4 = requests.get(paper4)
        r5 = requests.get(paper5)
        r6 = requests.get(paper6)
        r7 = requests.get(paper7)
        r8 = requests.get(paper8)
        r9 = requests.get(paper9)

        papers = {}
        if r1.status_code == 200:
            papers["w2021"] = paper1
        if r2.status_code == 200:
            papers["W2020"] = paper2
        if r3.status_code == 200:
            papers["W2019"] = paper3
        if r4.status_code == 200:
            papers["W2018"] = paper4
        if r5.status_code == 200:
            papers["W2017"] = paper5
        if r6.status_code == 200:
            papers["S2021"] = paper5
        if r7.status_code == 200:
            papers["S2020"] = paper5
        if r8.status_code == 200:
            papers["S2019"] = paper5
        if r9.status_code == 200:
            papers["S2018"] = paper5

        return render_template('papers.html', papers=papers)
    return render_template('papers.html')

# GTU Syllabus
@app.route('/gtu-syllabus', methods=['GET', 'POST'])
def syllabus():
    if request.method == 'POST':
        code = request.form.get('code')
        syllabus_url = f'https://s3-ap-southeast-1.amazonaws.com/gtusitecirculars/Syallbus/{code}.pdf'
        r = requests.get(syllabus_url)

        if r.status_code == 200:
            return render_template('syllabus.html', syllabus_url=syllabus_url)
        else:
            message = "Invalid Code"
            return render_template('syllabus.html', message=message)

    return render_template('syllabus.html')

# Recommendations
@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

# Solution
# @app.route('/solution', methods=['GET', 'POST'])
# def solution():
#     if request.method=="POST":
#         question = request.form.get('question')
#         # call API to get solution
#         url = f"http://localhost:5000/search/{question}"
#         r = requests.get(url)
#         data = r.json()
#         return render_template('solution.html', data=data)
#
#     # by default java for fullfill the page
#     url = f"http://localhost:5000/search/java"
#     r = requests.get(url)
#     data = r.json()
#     return render_template('solution.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)