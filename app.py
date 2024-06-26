from flask import Flask, render_template, redirect, url_for, session, make_response,request
from forms import LoginForm, OTPForm, AddBookForm, AddUserForm
import methods
import mysql.connector
from mysql.connector import Error
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MinorProjectLibraryManagementSystem'

# Configure MySQL database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="library"
    )
    cursor = db.cursor()
    # creating tables in database if they don't exist
    cursor.execute('''create table if not exists users (
        userId VARCHAR(64) NOT NULL PRIMARY KEY,
        fname VARCHAR(100) NOT NULL,
        phone VARCHAR(13) NOT NULL,
        mail_id VARCHAR(100) NOT NULL,
        fine INT(5) DEFAULT 0
    )''')
    cursor.execute('''create table if not exists books (
        title VARCHAR(500) NOT NULL,
        isbn_bn VARCHAR(64) NOT NULL PRIMARY KEY,
        author VARCHAR(200) NOT NULL,
        description VARCHAR(5000) NOT NULL,
        Publisher VARCHAR(200),
        gener VARCHAR(200)
    )''')
    cursor.execute('''create table if not exists issued_books (
        isbn_bn VARCHAR(64) NOT NULL,
        issuer VARCHAR(100) NOT NULL,
        issue_date DATE NOT NULL,
        return_date DATE NOT NULL,
        book_name VARCHAR(100) NOT NULL,
        author VARCHAR(100) NOT NULL,
        issuer_id VARCHAR(64) NOT NULL
    )''')
    cursor.execute('''create table if not exists admin (
        username VARCHAR(20) NOT NULL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        password VARCHAR(64) NOT NULL,
        phone VARCHAR(13) NOT NULL,
        mail VARCHAR(100) NOT NULL
    )''')
    db.commit()
except Error as e:
    print("Database connection error: ",e)


# rendering admin login page
@app.route('/')
def index():
    form = LoginForm()
    error=request.args.get('error')
    return render_template('login.html',form=form,error=error)

# working logic for admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cursor.execute("SELECT * FROM admin WHERE username = '{0}' AND password = '{1}'".format(username,methods.sha256(password)))
        user = cursor.fetchall()
        if user:
            try:
                sotp=methods.sendOTP(user[0][3])
            except:
                return "<h1>Vonage Client API Expired!\nPlease get a new key!</h1>"
            session['otp']=methods.sha256(sotp)
            resp=make_response(redirect(url_for('otp')))
            resp.set_cookie('admin',username)
            return resp
    return redirect(url_for('index',error="User Not Found"))

# rendering otp-verification page
@app.route('/otp')
def otp():
    form=OTPForm()
    error=request.args.get('error')
    return render_template('otp.html',form=form,error=error)

# verifying otp and loggin in admin
@app.route('/verifyotp', methods=['GET', 'POST'])
def verifyotp():
    form = OTPForm()
    if form.validate_on_submit():
        rotp = form.otp.data
        if(methods.sha256(rotp) == session['otp']):
            session.pop('otp',None)
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('otp',error="Invalid OTP!"))
    resp=make_response(redirect(url_for('login')))
    resp.set_cookie('admin','',max_age=0)
    return resp

# rendering admin dashboard
@app.route('/dashboard')
def dashboard():
    if 'admin' in request.cookies:
        cursor.execute("select (select count(distinct userId) from users) as user_count, (select count(distinct isbn_bn) from books) as book_count")
        counts=cursor.fetchone()
        print(counts)
        cursor.execute("select * from issued_books")
        books=cursor.fetchall()
        return render_template('dashboard.html',title='admin-dashboard',counts=counts,books=books, today=datetime.now().date())
    return redirect(url_for('index'))
    
# rendering form to add book
@app.route('/addBook')
def addBook():
    if 'admin' in request.cookies:
        form=AddBookForm()
        return render_template('addBook.html',title='add-book',form=form)
    return redirect(url_for('index'))

# working logic to add book
@app.route('/adding_book', methods=['GET', 'POST'])
def adding_book():
    form = AddBookForm()
    if form.validate_on_submit():
        bookId=form.bookId.data
        book_name = form.bookName.data
        author = form.author.data
        description = form.description.data
        publisher = form.publisher.data
        gener = form.gener.data
        cursor.execute("insert into books values('{0}','{1}','{2}','{3}','{4}','{5}')".format(book_name, bookId, author, description, publisher, gener))
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_book.html', form=form)

# render form to add user
@app.route('/addUser')
def addUser():
    if 'admin' in request.cookies:
        form=AddUserForm()
        return render_template('addUser.html',title='add-user',form=form)
    return redirect(url_for('index'))

# working logic to add user
@app.route('/adding_user', methods=['GET', 'POST'])
def adding_user():
    form = AddUserForm()
    if form.validate_on_submit():
        cursor.execute('select userId from users')
        id=cursor.fetchall()
        print(id)
        userid=methods.uniqueId(id)
        print(userid)
        username = form.name.data
        email = form.mail.data
        phone = form.phone.data
        phone = "+91"+phone
        # Add user to database
        cursor.execute("insert into users values('{0}','{1}','{2}','{3}',{4})".format(userid, username, phone, email,0))
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_user.html', form=form)

# render user page
@app.route('/searchUser')
def searchUser():
    if 'admin' in request.cookies:
        cursor.execute("select * from users where fine>0")
        fine=cursor.fetchall()
        cursor.execute("select * from users limit 10")
        data=cursor.fetchall()
        # print(data)
        return render_template('searchUser.html',title="users-all",data=data,fine=fine)
    return redirect(url_for('index'))

# searching user in database
@app.route('/searchigUser', methods=['GET','POST'])
def searchingUser():
    if 'admin' in request.cookies:
        if request.method=='POST':
            query=request.form['query']
            cursor.execute("select * from users where ( userId like '%{0}%' or fname like '{0}%' or phone like '%{0}%' or mail_id like '%{0}%')".format(query))
            data=cursor.fetchall()
            return render_template('searchUser.html',title="users-all",data=data)
        return redirect(url_for('searchUser'))
    return redirect(url_for('index'))

# showing individual users profile
@app.route('/showUser')
def showUser():
    if 'admin' in request.cookies:
        userid=request.args.get('id')
        cursor.execute("select * from users where userId='{0}'".format(userid))
        data=cursor.fetchall()
        return render_template('userDetails.html',title='user-{0}'.format(userid),data=data)
    return redirect(url_for('index'))

# edit user details form 
@app.route('/editUser')
def editUser():
    if 'admin' in request.cookies:
        form=AddUserForm()
        userid=request.args.get('id')
        cursor.execute("select * from users where userId='{0}'".format(userid))
        data=cursor.fetchall()
        return render_template('editUserDetails.html',title='edit-user-{0}'.format(userid),data=data,form=form)
    return redirect(url_for('index'))

# saving edited details
@app.route('/savingUser',methods=['POST'])
def savingUser():
    if 'admin' in request.cookies:
        form = AddUserForm()
        if form.validate_on_submit():
            userid=request.args.get('id')
            # print(userid)
            username = form.name.data
            email = form.mail.data
            phone = form.phone.data
            cursor.execute("update users set fname='{0}', phone='{1}', mail_id='{2}' where userId='{3}'".format(username,phone,email,userid))
            db.commit()
            return redirect(url_for('dashboard'))
        return redirect(url_for('editUser'))
    return redirect(url_for('index'))

# delete user
@app.route('/deleteUser')
def deleteUser():
    if 'admin' in request.cookies:
        userid=request.args.get('id')
        cursor.execute("delete from users where userId='{0}'".format(userid))
        db.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

# books template 
@app.route('/searchBooks')
def searchBooks():
    if 'admin' in request.cookies:
        cursor.execute("select * from books limit 10")
        data=cursor.fetchall()
        # print(data)
        return render_template('searchBook.html',title='books-all',data=data)
    return redirect(url_for('index'))

# searching for book in database
@app.route('/searchingBook', methods=['GET','POST'])
def searchingBook():
    if 'admin' in request.cookies:
        if request.method=='POST':
            query=request.form['query']
            cursor.execute("select * from books where ( title like '%{0}%' or isbn_bn like '%{0}%' or author like '{0}%' or Publisher like '{0}%' or gener like '%{0}%')".format(query))
            data=cursor.fetchall()
            return render_template('searchBook.html',title='books-all',data=data)
        return redirect(url_for('searchBooks'))
    return redirect(url_for('index'))

# show book details
@app.route('/showBook')
def showBook():
    if 'admin' in request.cookies:
        bookid=request.args.get('id')
        cursor.execute("select * from books where isbn_bn='{0}'".format(bookid))
        data=cursor.fetchall()
        cursor.execute("select * from issued_books where isbn_bn='{0}'".format(bookid))
        status=cursor.fetchall()
        if (status):
            status='Unavailable'
        else:
            status='Available'
        return render_template('bookDetails.html',title='book-{0}'.format(bookid),data=data,status=status)
    return redirect(url_for('index'))

# edit book details
@app.route('/editBook')
def editBook():
    if 'admin' in request.cookies:
        form=AddBookForm()
        bookid=request.args.get('id')
        cursor.execute("select * from books where isbn_bn='{0}'".format(bookid))
        data=cursor.fetchall()
        return render_template('editBookDetails.html',title='edit-book-{0}'.format(bookid),data=data,form=form)
    return redirect(url_for('index'))

# saving edited details of book
@app.route('/savingBook',methods=['POST'])
def savingBook():
    if 'admin' in request.cookies:
        form = AddBookForm()
        if form.validate_on_submit():
            bookid=request.args.get('id')
            # print(userid)
            bookId=form.bookId.data
            book_name = form.bookName.data
            author = form.author.data
            description = form.description.data
            publisher = form.publisher.data
            gener = form.gener.data
            cursor.execute("update books set title='{0}', author='{1}', description='{2}', Publisher='{3}', isbn_bn='{4}', gener='{5}' where isbn_bn='{6}'".format(book_name,author,description,publisher,bookId,gener,bookid))
            db.commit()
            return redirect(url_for('dashboard'))
        return redirect(url_for('editBook'))
    return redirect(url_for('index'))

# deleting book from database
@app.route('/deleteBook')
def deleteBook():
    if 'admin' in request.cookies:
        bookid=request.args.get('id')
        cursor.execute("delete from books where isbn_bn='{0}'".format(bookid))
        db.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

# issue book form
@app.route('/issueBook')
def issueBook():
    if 'admin' in request.cookies:
        bookid=request.args.get('id')
        if (bookid):
            return render_template('issueBook.html',title='issue-{0}'.format(bookid),bookid=bookid)
        return render_template('issueBook.html',title='issue-Book')
    return redirect(url_for('index'))

# saving issuer and book details in database
@app.route('/issuingBook', methods=['POST','GET'])
def issuingBook():
    if 'admin' in request.cookies:
        if request.method=='POST':
            bookid=request.form['isbn']
            userid=request.form['userid']
            cursor.execute("select isbn_bn from issued_books where isbn_bn='{0}'".format(bookid))
            status=cursor.fetchone()
            if (status):
                return "book already issued by some other user"
            cursor.execute("select * from books where isbn_bn='{0}'".format(bookid))
            book=cursor.fetchone()
            cursor.execute("select * from users where userId='{0}'".format(userid))
            user=cursor.fetchone()
            cursor.execute("insert into issued_books values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(bookid,user[1],datetime.now().date(),datetime.now().date()+timedelta(days=7),book[0],book[2],userid))
            db.commit()
            return redirect('dashboard')
    return redirect(url_for('index'))

# return book form
@app.route('/returnBook')
def returnBook():
    if 'admin' in request.cookies:
        return render_template('returnBook.html',title='return-book')
    return redirect(url_for('index'))

# returning book and calculating fine if any and writing it in database
@app.route('/returningBook', methods=['POST','GET'])
def returningBook():
    if 'admin' in request.cookies:
        if request.method=='POST':
            bookid=request.form['bookid']
            cursor.execute('select return_date,issuer_id,isbn_bn from issued_books where isbn_bn="{0}"'.format(bookid))
            data=cursor.fetchone()
            if data:
                return_date=data[0]
                issuer=data[1]
                bookid=data[2]
                if return_date<datetime.now().date():
                    fine=10*(datetime.now().date()-return_date).days
                    cursor.execute("update users set fine={0} where userID='{0}'".format(fine,issuer))
                    db.commit()
                cursor.execute("delete from issued_books where isbn_bn='{0}'".format(bookid))
                db.commit()
                return redirect('dashboard')
    return redirect(url_for('index'))

# clearing users fine
@app.route('/payFine')
def payFine():
    if 'admin' in request.cookies:
        userid=request.args.get('id')
        cursor.execute("update users set fine=0 where userId='{0}'".format(userid))
        db.commit()
        return redirect('searchUser')
    return redirect(url_for('index'))

# logout admin
@app.route('/logout')
def logout():
    resp=make_response(render_template("logout.html"))
    resp.set_cookie('admin','',max_age=0)
    return resp

# driver code for server
if __name__ == '__main__':
    app.run(debug=True)
