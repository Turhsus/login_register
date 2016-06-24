from system.core.controller import *

class Login(Controller):
    def __init__(self, action):
        super(Login, self).__init__(action)
        
        self.load_model('LoginModel')
        self.db = self._app.db
   
    def index(self):
        if 'id' in session:
            return redirect('/login/success')
        else:
            return self.load_view('index.html')

    def enter(self):
        if request.form['action'] == 'register':
            user_info = {
                'input': request.form['action'],
                'first': request.form['first_name'],
                'last': request.form['last_name'],
                'email': request.form['email'],
                'password': request.form['Password'],
                'confirm': request.form['confirm']
            }
            create_status = self.models['LoginModel'].create_user(user_info)
            if create_status['valid'] == True:
                session['id'] = create_status['user']['id']
                session['name'] = create_status['user']['first_name']
                return redirect('/login/success')
            else:
                for error in create_status['errors']:
                    flash(error)
                return redirect('/')
        elif request.form['action'] == 'login':
            user_info = {
                'email': request.form['email'],
                'password': request.form['Password']
            }
            print "Got user info"
            login_status = self.models['LoginModel'].login_user(user_info)
            print "Querried login DB"
            if login_status['valid'] == True:
                session['id'] = login_status['user']['id']
                session['name'] = login_status['user']['first_name']
                return redirect('/login/success')
            else:
                for error in login_status['errors']:
                    flash(error)
                return redirect('/')


    def success(self):
        if 'id' in session:
            return self.load_view('success.html')
        else:
            flash("not logged in!")
            return redirect('/')

    def logout(self):
        session.clear()
        flash('Logged out!')
        return redirect('/')




