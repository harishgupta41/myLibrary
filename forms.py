from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, TextAreaField

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
    ], render_kw={'class':'form-control'})
    submit=SubmitField('Verify',render_kw={'class':'verify-otp-btn btn btn-primary'})
    csrf_token = StringField('CSRF Token')

class AddBookForm(FlaskForm):
    bookId= StringField('ISBN',[validators.length(min=13,max=13,message='ISBN should be of 13 digits'),
                                validators.DataRequired(message='ISBN should be provided')])
    bookName= StringField('Book Name',[
        validators.DataRequired(message="Book name cannot be empty"),
        validators.length(max=500)
    ])
    author=StringField('Author',[
        validators.DataRequired(message="Author's name should be filled"),
        validators.length(max=200)
    ])
    description=TextAreaField('Book Description',[
        validators.length(max=5000,message='should not exceede 5000 characters')
    ])
    publisher=StringField('Publisher',[validators.length(max=200)])
    gener=StringField('Gener',[
        validators.DataRequired(message="Gener should be filled"),
        validators.length(max=200)
    ])
    save=SubmitField('Save Details',render_kw={'class':'addUser-btn'})
    submit=SubmitField('Add Book',render_kw={'class':'addBook-btn'})
    csrf_token = StringField('CSRF Token')

class AddUserForm(FlaskForm):
    name=StringField("Full Name",[
        validators.DataRequired(message="Name must pe provided"),
        validators.length(max=100)
    ])
    phone=StringField("Phone",[
        validators.DataRequired(message="Phone number with country code"),
        validators.length(min=10,max=10,message='phone number should be of 10 digits')
    ])
    mail=StringField("Mail ID",[
        validators.DataRequired(message="Mail cannot be empty"),
        validators.length(max=100)
    ])
    save=SubmitField('Save Details',render_kw={'class':'addUser-btn'})
    submit=SubmitField('Add User',render_kw={'class':'addUser-btn'})
    csrf_token = StringField('CSRF Token')