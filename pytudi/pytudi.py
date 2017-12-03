from flask import Flask, session, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask.ext.login import current_user
from sqlalchemy.orm import relationship, backref
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thuctappythonvccloud'
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):

    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    book = db.relationship('Book', backref='owner', lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):

    username = StringField(
        'username', validators=[
            InputRequired(), Length(
                min=5, max=20)])

    password = PasswordField(
        'password', validators=[
            InputRequired(), Length(
                min=5, max=20)])

    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):

    email = StringField(
        'email', validators=[
            InputRequired(), Email(
                message='Invalid email'), Length(
                max=50)])

    username = StringField(
        'username', validators=[
            InputRequired(), Length(
                min=4, max=15)])

    password = PasswordField(
        'password', validators=[
            InputRequired(), Length(
                min=8, max=80)])


class Book(db.Model):

    __tablename__ = "book"
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    price = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class CreateForm(FlaskForm):

    title = StringField(
        'title', validators=[
            InputRequired(), Length(
                min=1, max=50)])

    author = StringField(
        'author', validators=[
            InputRequired(), Length(
                min=3, max=50)])

    price = StringField(
        'price', validators=[
            InputRequired(), Length(
                min=4, max=10)])

    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            success = login_user(user)
            if success:
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/managers', methods=['GET', 'POST'])
@login_required
def show():
    books = Book.query.join(User).filter(
        Book.owner_id == session['user_id']).order_by(
        Book.title, Book.author, Book.price).all()
    return render_template(
        'managers.html',
        books=books)

@app.route('/managers/create', methods=['GET', 'POST'])
def create():
    create = True
    form = CreateForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            owner_id=session['user_id'])
        db.session.add(new_book)
        db.session.commit()
        flash('You have successfully create a new book.')
        return redirect(url_for('show'))
    return render_template('manager.html', form=form, create=create)

@app.route("/managers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    create = False
    book = Book.query.get_or_404(id)
    form = CreateForm(obj=book)
    if request.method == 'POST' and form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.price = form.price.data
        db.session.add(book)
        db.session.commit()
        flash('You have successfully edit the book.')
        return redirect(url_for('show'))
    return render_template('manager.html', form=form, create=create, book=book)

@app.route("/managers/delete", methods=["POST"])
@login_required
def delete():
    title = request.form.get("title")
    author = request.form.get("author")
    price = request.form.get("price")
    book = Book.query.filter_by(
        title=title,
        author=author,
        price=price).first()
    db.session.delete(book)
    db.session.commit()
    flash('You have successfully deleted the book.')
    return redirect(url_for('show'))


if __name__ == '__main__':
    app.run(debug=True)

