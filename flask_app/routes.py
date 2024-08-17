from flask import render_template, url_for, flash, redirect
from flask_app.forms import RegisterationFormn, LoginFormn
from flask_app.models import User, Post
from flask_app import app, db, bcrypt

############################### Global Variable Declaration ################################

posts = [
    {
        'author': 'Swaroop.GS',
        'title': 'Lies of Narendra Modi',
        'content': 'Modi has a “purana rishta” - an old relationship – with lies and untruths and that bears no repetition. Indian news television, or whatever passes off for it, is beyond redemption. It is rotting at the bottom of a bottomless pit. What needs to be underscored is the coverage in India’s English language newspapers. Two of them had Modi’s astonishing claim on their front page: The Times of India and the Indian Express. And both did perfect stenography. They simply narrated what Modi had said, without attempting even a semblance of a fact-check, the basic function of any journalist. ‘If I do Hindu-Muslim, won’t be fit for public life: PM Modi’, said the TOI headline and the story provided no context or background for readers to judge his claim. ‘The day I do Hindu-Muslim, I will be unworthy of public life… I will not do it, it’s my resolve: PM Modi,’ said the Express headline. Though its story reproduced quotes from his April 21 Banswara speech, it failed to point out the obvious: that the PM was making an obvious misrepresentation of his remarks.Modi’s speech at Banswara is crystal clear in its words and language. It is not a dog whistle, it an open and loud howl for human consumption that is recorded on video. Given the undeniable nature of his remarks, Modi’s disingenuous claim did not merit a stenographic report. It needed to be reported as a fact check, so that readers and viewers could be armed with the necessary health warnings. [See here and here]. The India Cable is a newsletter so was even more direct: We told our readers yesterday that Modi had lied.',
        'date_posted': 'August 08, 2024'
    },
    {
        'author': 'Supriya.J',
        'title': 'Facts of Nirmala Sitharaman',
        'content': 'First of all, let’s understand who will decide whether Nirmala Sitharaman is a good finance minister or not. And what are the criteria to judge her performance? Ideally in the office, your Boss will do your appraisal or competency evaluation. He will decide whether you are good or not. So the onus and authority of judging Nirmala Sitharaman as the Finance Minister are with Modi Ji. Modi Ji must have been pleased with her performance as the Defense Minister in his first term, so he has given her the all-important Finance Ministry. During the Rafale deal controversy, Madam Sitharaman fought valiantly in Modi’s favor. Modi Ji must have been very highly impressed with her fighting spirit and loyalty. So it seems Madam Sitharaman has duly earned her position in the new cabinet. As such it’s Modi Ji and only Modi Ji going to evaluate her as the Finance Minister.',
        'date_posted': 'August 07, 2024'
    }
]

############################### Home page ##################################################
@app.route("/")
@app.route("/home") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def home():
    return render_template("home.html", posts=posts)


############################### About page #################################################
@app.route("/about") #route is a decorator that is used to handle all the backend stuff and retun the o/p of the called function
def about():
    return render_template('about.html', title='About') 

############################### Registeration page #########################################

@app.route("/register", methods= ['GET', 'POST'])
def register(): 
    form = RegisterationFormn()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! Please procced to login!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title= "Register", form=form)

############################### Login page #################################################

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginFormn()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        hashed_password = user.password
        password = bcrypt.check_password_hash(hashed_password, form.password.data)
        print(password)
        if user and password:
            flash(f"Logged in to the Account for {form.email.data}", "success")
            return redirect(url_for('home'))
        else:
            flash(f"Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title= "Login", form=form)