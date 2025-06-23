from flask import Flask, jsonify, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash

import os

from Backend.accountTypeMannager import authAdmin, fetchUsers, updateAccountType

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "./Database/tables.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "SomeSecret"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    accounttype = db.Column(db.String(50), nullable=False, default="User")

class Crops(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropname = db.Column(db.String(50), nullable=False)
    seedprice = db.Column(db.String(50), nullable=False)
    lowestsellingprice = db.Column(db.Integer, nullable=False)

class Sales(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cropid = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    quantitysold = db.Column(db.Integer, nullable=False)
    profitmade = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    crops = db.relationship('Crops', backref='sales', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField("Email", validators=[InputRequired(), Length(min=5, max=50), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class PasswordUpdateForm(FlaskForm):
    newpassword = PasswordField("NewPassword", validators=[InputRequired(), Length(min=6, max=80)])
    confirmpassword = PasswordField("ConfirmPassword", validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField("Update Password")

class AccountForm(FlaskForm):
    accounttype = StringField("Account Type", validators=[InputRequired()])
    submit = SubmitField("Update Account Type")

class SaleForm(FlaskForm):
    cropname = StringField("Crop Name", validators=[InputRequired()])
    season = StringField("Season", validators=[InputRequired()])
    quantitysold = StringField("Quantity Sold", validators=[InputRequired()])
    revenue = StringField("Revenue", validators=[InputRequired()])
    submit = SubmitField("Add Sale")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        if Users.query.filter_by(username=form.username.data).first():
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("signup"))
        if Users.query.filter_by(email=form.email.data).first():
            flash("Email already exists. Please choose a different one.")
            return redirect(url_for("signup"))
        hashed_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("You've been registered successfully, now you can log in.")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember)
            return redirect(url_for("index"))
        flash("Your credentials are invalid.")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. See you soon!")
    return redirect(url_for("login"))

@app.route('/accountTypeMannager/<int:userid>', methods=['GET', 'POST'])
@login_required
def accountTypeMannager(userid):
    form = AccountForm()
    UID = current_user.id
    if form.validate_on_submit():
        userId = userid
        accountType = form.accounttype.data
        if updateAccountType(UID,userId, accountType) == "User " + str(userId) + " updated to account type " + accountType:
            flash("Account type updated successfully.")
        else:
            flash("Failed to update account type. You may not have permission to do this.")
        return redirect(url_for("index"))
    return render_template("accountTypeMannager.html", form=form, userid=userid)
    
@app.route('/users', methods=['GET'])
@login_required
def users():
    UID = current_user.id
    users = fetchUsers(UID)
    if isinstance(users, list):
        return render_template("users.html", users=users)
    else:
        flash("Could not fetch users.")
        return redirect(url_for("index"))

@app.route('/crops', methods=['GET'])
@login_required
def crops():
    crops = Crops.query.all()
    return render_template("crops.html", crops=crops)

@app.route('/sales', methods=['GET'])
@login_required
def sales():
    if authAdmin(current_user.id) == True:
        sales = Sales.query.all()
        return render_template("sales.html", sales=sales)
    else:
        sales = Sales.query.filter_by(userid=current_user.id).all()
        return render_template("sales.html", sales=sales)
    
@app.route('/addSale', methods=['GET','POST'])
@login_required
def addSale():
    form = SaleForm()
    if form.validate_on_submit():
        userid = current_user.id
        cropname = form.cropname.data
        season = form.season.data
        quantitysold = form.quantitysold.data
        revenue = form.revenue.data
        
        crop = Crops.query.filter_by(cropname=cropname).first()
        if not crop:
            flash("Crop not found.")
            return redirect(url_for("addSale"))
        
        new_sale = Sales(userid=userid, cropid=crop.id, season=season, quantitysold=quantitysold, profitmade=revenue)
        db.session.add(new_sale)
        db.session.commit()
        flash("Sale added successfully.")
        return redirect(url_for("sales"))
    
    return render_template("addSale.html", form=form)

@app.route('/deleteSale/<int:saleid>', methods=['GET','POST'])
@login_required
def deleteSale(saleid):
    sale = Sales.query.get_or_404(saleid)
    if sale.userid == current_user.id or authAdmin(current_user.id):
        db.session.delete(sale)
        db.session.commit()
        flash("Sale deleted successfully.")
    else:
        flash("You do not have permission to delete this sale.")
    return redirect(url_for("sales"))

@app.route('/updatePassword/<int:userid>', methods=['POST', 'GET'])
@login_required
def updatePassword(userid):
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        if form.newpassword.data != form.confirmpassword.data:
            flash("Passwords do not match.")
            return redirect(url_for("updatePassword", userid=current_user.id))
        
        if userid == current_user.id or authAdmin(current_user.id):
            user = Users.query.get_or_404(userid)
            user.password = generate_password_hash(form.newpassword.data, method="pbkdf2:sha256")
            db.session.commit()
            flash("Password updated successfully.")
            return redirect(url_for("index"))
        else:
            flash("Permission denied. You can only update your own password.")
            return redirect(url_for("updatePassword", userid=current_user.id))

    return render_template("updatePassword.html", form=form, userid=userid)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
