from app import app, db, uploaded_photos # pragma no cover
from flask import render_template, redirect, \
    url_for, request, session, flash # pragma no cover
from flask.ext.login import login_user, logout_user, login_required, current_user # pragma no cover
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from forms import LoginForm, MessageForm, RegisterForm # pragma no cover
from app.models import User, BlogPost, Photos, bcrypt # pragma no cover


@app.route('/')# pragma no cover
@app.route('/home')# pragma no cover
def index():
    return render_template('index.html')

@app.route("/profile/<path:user_id>/<path:name>", methods=["GET", "POST"])
def profile(name, user_id):
    profile = User.query.filter_by(id=user_id).one()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        photo = request.files["photo"]
        try:
            filename = uploaded_photos.save(photo)
        except UploadNotAllowed:
            flash("The upload was not allowed")
        else:
            profile.name = username
            profile.email = email
            photo = Photo(filename=filename, user_id=profile.id)
            db.session.add(profile)
            db.session.add(photo)
            db.session.commit()
            flash("Just updated your profile!")
            return redirect("index.html")
    return render_template("profile.html", name=name, profile=profile)

@app.route('/show')
def hello_world():
    photos = Photos.query.all()
    return render_template("all_photos.html", photos=photos)
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        photo = request.files["photo"]
        title = request.form["title"]
        caption = request.form["caption"]
        if not (photo and title and caption):
            flash("You must fill in all the fields")
        else:
            try:
                filename = uploaded_photos.save(photo)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                post = Photos(title=title, caption=caption, filename=filename)
                db.session.add(post)
                db.session.commit()
                flash("Post is successful")
                return redirect(url_for("hello_world"))
    return render_template('upload.html')


@app.route('/photo/<id>')
def show(id):
    photo = Photo.load(id)
    if photo is None:
        abort(404)
    url = photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)

@app.route('/blog', methods=['GET', 'POST'])# pragma no cover
@app.route('/blog/<int:page>', methods=['GET','POST'])# pragma no cover
def blog(page=1):
    posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page,5,False)
    return render_template('blog.html', 
                            posts=posts)


@app.route("/blog/<int:blog_id>/<path:blog_title>/")
def blog_post(blog_id, blog_title):
    blogpost = db.session.query(BlogPost).filter_by(id=blog_id).one()
    return render_template('blog-post.html', 
                            blogpost=blogpost)


@app.route("/blog/<int:author_id>/newpost/", methods=["GET","POST"])
def new_blogpost(author_id):
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        newpost = BlogPost(title=form.title.data, 
                           description=form.description.data,
                           author_id=current_user.id)
        db.session.add(newpost)
        db.session.commit()
        flash('your post was successful', 'success')
        return redirect(url_for('blog'))

    return render_template('create-post.html', 
                            form=form, 
                            error=error)


@app.route("/blog/<int:author_id>/<int:blog_id>/edit/", methods=["GET","POST"])
def edit_blogpost(author_id, blog_id):
    error = None
    editpost = db.session.query(BlogPost).filter_by(id=blog_id).one()
    form = MessageForm(obj=editpost)
    if form.validate_on_submit():
        editpost.title = form.title.data
        editpost.description = form.description.data
        db.session.add(editpost)
        db.session.commit()
        flash("Post successfully edited", "success")
        return redirect(url_for('blog'))
    
    return render_template('edit-post.html', 
                            editpost=editpost, 
                            form=form, 
                            error=error)
        

@app.route("/blog/<int:author_id>/<int:blog_id>/delete/",methods=["GET","POST"])
def delete_blogpost(author_id, blog_id):
    deletepost = db.session.query(BlogPost).filter_by(id=blog_id).one()
    if request.method == "POST":
        db.session.delete(deletepost)
        db.session.commit()
        flash("Post Deleted", "danger")
        return redirect(url_for('blog'))

    return render_template('delete-post.html',
                            deletepost=deletepost)


@app.route('/login', methods=["GET", "POST"])# pragma no cover
def login():
    error = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(name=request.form['username']).first()
        if user is not None and bcrypt.check_password_hash(
                                user.password, 
                                request.form['password']):
            remember_me = form.remember_me.data
            login_user(user,remember_me)
            flash("You Were Signin in. Yea!", 'success')
            return redirect(url_for('blog'))
        else:
            flash("<strong>Invalid Credentials.</strong> Please try again.", "danger")
            return redirect(url_for('login'))

    return render_template("login.html", 
                            form=form, 
                            error=error)    


@app.route('/logout')# pragma no cover
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash('You were logged out.', 'warning')
    return redirect(url_for('index'))


@app.route("/register", methods=["GET","POST"])# pragma no cover
def register():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Congrats on your new account!", "success")
        return redirect(url_for("blog"))
    return render_template("register.html", form=form, error=error)

