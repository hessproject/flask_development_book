from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from forms import NameForm
from datetime import datetime

#Config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'
Bootstrap(app)
Moment(app)
#manager = Manager(app) <- allows for command line options shell and runserver

#Forms, should be moved to own file

#200 Routes
@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

#Error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

#Main Function
if __name__ == '__main__':
    #manager.run() <- uncomment to enable command line options
    app.run(debug=True)