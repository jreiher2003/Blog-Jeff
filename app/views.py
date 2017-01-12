import json
import requests
from app import app, db, github # pragma no cover
from flask import render_template, redirect, \
    url_for, request, session, flash, g # pragma no cover
from flask.ext.login import login_user, logout_user, login_required, current_user # pragma no cover
from forms import LoginForm, MessageForm, RegisterForm # pragma no cover
from app.models import User, BlogPost, bcrypt # pragma no cover



@app.route('/')# pragma no cover
@app.route('/blog', methods=['GET', 'POST'])# pragma no cover
@app.route('/blog/<int:page>', methods=['GET','POST'])# pragma no cover
def blog(page=1):
    error = None
    form = LoginForm(request.form)
    posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page,5,False)
    return render_template(
        'blog.html', 
        posts=posts,
        form=form,
        error=error
        )

@app.route("/profile/<path:user_id>/<path:name>", methods=["GET", "POST"])
@login_required
def profile(name, user_id):
    profile = User.query.filter_by(id=user_id).one()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        avatar_url = request.form["avatar_url"]
        profile.name = username
        profile.email = email
        profile.avatar_url = avatar_url
        db.session.add(profile)
        db.session.commit()
        flash("Just updated your profile!", "info")
        return redirect(url_for(
            'profile', 
            name=name, 
            user_id=user_id)
        )
    return render_template(
        "profile.html", 
        name=name, 
        profile=profile
        )


@app.route("/blog/<int:blog_id>/<path:blog_title>/")
def blog_post(blog_id, blog_title):
    error = None
    form = LoginForm(request.form)
    blogpost = db.session.query(BlogPost).filter_by(id=blog_id).one()
    return render_template(
        'blog-post.html', 
        blogpost=blogpost,
        form=form,
        error=error
        )


@app.route("/blog/<int:author_id>/newpost/", methods=["GET","POST"])
@login_required
def new_blogpost(author_id):
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        newpost = BlogPost(
            title=form.title.data, 
            description=form.description.data,
            author_id=current_user.id)
        db.session.add(newpost)
        db.session.commit()
        flash('your post was successful', 'success')
        return redirect(url_for('blog'))
    return render_template(
        'create-post.html', 
        form=form, 
        error=error
        )


@app.route("/blog/<int:author_id>/<int:blog_id>/edit/", methods=["GET","POST"])
@login_required
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
    return render_template(
        'edit-post.html', 
        editpost=editpost, 
        form=form, 
        error=error
        )


@app.route("/blog/<int:author_id>/<int:blog_id>/delete/",methods=["GET","POST"])
@login_required
def delete_blogpost(author_id, blog_id):
    deletepost = db.session.query(BlogPost).filter_by(id=blog_id).one()
    if request.method == "POST":
        db.session.delete(deletepost)
        db.session.commit()
        flash("Post Deleted", "danger")
        return redirect(url_for('blog'))

    return render_template(
        'delete-post.html',
        deletepost=deletepost
        )

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.after_request
def after_request(response):
    db.session.remove()
    return response

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('blog')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(github_access_token=access_token)
        db.session.add(user)
    user.github_access_token = access_token
    db.session.commit()

    session['user_id'] = user.id
    return render_template("blog.html", session=session)

@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('blog'))

@app.route('/user')
def user():
    return str(github.get('user'))

# @app.route('/login', methods=["GET","POST"])# pragma no cover
# def login():
#     error = None
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         user = User.query.filter_by(name=form.username.data).first()
#         if user is not None and bcrypt.check_password_hash(
#             user.password, 
#             form.password.data):
#             remember_me = form.remember_me.data
#             login_user(user, remember_me)
#             flash("You Were Signin in. Yea!", 'success')
#             referer = request.headers["Referer"]
#             return redirect(referer)
#         else:
#             flash("<strong>Invalid Credentials.</strong> Please try again.", "danger")
#             referer = request.headers["Referer"]
#             return redirect(referer)
#     return render_template(
#         "login.html",
#         form=form,
#         error=None
#         )    


# @app.route('/logout')# pragma no cover
# @login_required
# def logout():
#     logout_user()
#     session.pop('logged_in', None)
#     flash('You were logged out.', 'warning')
#     referer = request.headers["Referer"]
#     return redirect(referer)


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
        user.filename = "profile_pic.jpg"
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Congrats on your new account!", "success")
        return redirect(url_for("blog"))
    return render_template(
        "register.html", 
        form=form, 
        error=error)


##################################################################
###############  AWS s3  #########################################
##################################################################
import time, os, json, base64, hmac, urllib
from hashlib import sha1

@app.route('/sign_s3/')
def sign_s3():
    # Collect information on the file from the GET parameters of the request:
    object_name = urllib.quote_plus(request.args.get('file_name'))
    mime_type = request.args.get('file_type')
    # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"
    # Generate the StringToSign:
    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, os.environ["S3_BUCKET"], object_name)
    # Generate the signature with which the StringToSign can be signed:
    signature = base64.encodestring(hmac.new(os.environ["AWS_SECRET_KEY"], string_to_sign.encode('utf8'), sha1).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.quote_plus(signature.strip())
    # Build the URL of the file in anticipation of its imminent upload:
    url = 'https://%s.s3.amazonaws.com/%s' % (os.environ["S3_BUCKET"], object_name)
    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, os.environ["AWS_ACCESS_KEY"], expires, signature),
        'url': url,
        })
    return content