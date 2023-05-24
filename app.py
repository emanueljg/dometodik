from flask import *
from dataclasses import dataclass
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)



login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    USERS = []
    
    def __init__(self, id): 
        self._id = id
        self.USERS.append(self)

    @property
    def id(self):
        return str(self._id)

    @classmethod
    def _that_has(cls, **attrs):
        return next((usr for usr in cls.USERS
                        if all(getattr(usr, k)== v for k, v in attrs.items())), 
                    None)

    @classmethod
    def with_login(cls, email, password):
        return cls._that_has(email=email, password=password)

@dataclass
class Content:
    special: bool = False
    protected: bool = False
    
ALL_CONTENTS = (
    login = Content('login', special=True),
    logout = Content('logout', special=True, protected=True),
    home = Content('home'),
    members = Content('members'),
)

@app.context_processor
def content_with(**attrs)
    return [c for c in ALL_CONTENTS 
            if all(getattr(c, k) == v for k, v in attrs.items())]



ADMIN = User(1)
ADMIN.email = 'admin@dometodik.se'
ADMIN.password = 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

GENERIC_CONTENT = (
    # 'login',  
    'home',
    'members'
)

SPECIAL_CONTENT = ( 
    'login'
    'logout'
)

ALL_CONTENTS = GENERIC_CONTENT + SPECIAL_CONTENT


def base_render(content='home', failed_login=False):
    contents 
    if current_user.is_authenticated:
        pass
    else:
        
    return render_template('base.html', 
                           content=content,
                           ALL_CONTENTS=ALL_CONTENTS,
                           failed_login=failed_login)


@app.route('/login', methods=(['POST']))
def login():
    """Login a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    found_user = User.with_login(email, password)
    if found_user:
        flask_login.login_user(User(found_user['id']))
        return redirect('/')
    else:
        return base_render(content='login', failed_login=True) 
        

@app.route('/logout', methods=(['GET']))
def logout():
    logout_user()
    return redirect('/')


@app.route(f'/<any({GENERIC_CONTENT.join(", ")}):content')
def content_route(content):
    return base_render(content=content)

@app.route('/')
def base():
    return redirect(url_for('/home'))

