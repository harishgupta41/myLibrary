from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class LoginForm(FlaskForm):
    username = StringField('Username',[
        validators.DataRequired(message="Username is required"),
        validators.Length(min=8, max=20, message="Username must be between 8 and 20 characters"),
    ])
    password = PasswordField('Password',[
        validators.DataRequired(message="Password is required"),
        validators.length(min=8,message="Password must be of a minimum 8 characters")
   ])
    submit= SubmitField('Login',render_kw={'class':'submit-btn'})

    csrf_token = StringField('CSRF Token')

class OTPForm(FlaskForm):
    otp = StringField('OTP',[
        validators.DataRequired(message="OTP must be filled"),
    ])
    submit=SubmitField('Verify',render_kw={'class':'verify-otp-btn'})
    csrf_token = StringField('CSRF Token')

class AddBookForm(FlaskForm):
    bookId= StringField('ISBN')
    bookName= StringField('Book Name',[
        validators.DataRequired(message="Book name cannot be empty")
    ])
    author=StringField('Author',[
        validators.DataRequired(message="Author's name should be filled")
    ])
    description=StringField('Book Description')
    publisher=StringField('Publisher')
    gener=StringField('Gener',[
        validators.DataRequired(message="Gener should be filled")
    ])
    save=SubmitField('Save Details',render_kw={'class':'addUser-btn'})
    submit=SubmitField('Add Book',render_kw={'class':'addBook-btn'})
    csrf_token = StringField('CSRF Token')

class AddUserForm(FlaskForm):
    name=StringField("Full Name",[
        validators.DataRequired(message="Name must pe provided")
    ])
    phone=StringField("Phone",[
        validators.DataRequired(message="Phone number with country code")
    ])
    mail=StringField("Mail ID",[
        validators.DataRequired(message="Mail cannot be empty"),
    ])
    save=SubmitField('Save Details',render_kw={'class':'addUser-btn'})
    submit=SubmitField('Add User',render_kw={'class':'addUser-btn'})
    csrf_token = StringField('CSRF Token')