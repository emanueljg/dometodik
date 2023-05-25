from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dataclasses import dataclass
from typing import Collection, ClassVar


app = Flask(__name__)
app.secret_key = '9a5696420b61932bf0690347fd0a7653e62091ff8f359dc1bbfbec461caf22d3'

login_manager = LoginManager()
login_manager.init_app(app)

def _obj_has_attrs(o, **attrs):
    return all(
        getattr(o, k) == v for k, v in attrs.items()
    )

def stuff_with_attrs(everything: Collection,
                     **attrs):
    """
    Helper func for getting all objs 
    in a collection having the given attrs.
    """
    return { 
        ok: ov for ok, ov in everything.items() 
            if _obj_has_attrs(ov, **attrs)
    } if type(everything) is dict \
    else (
        o for o in everything 
            if _obj_has_attrs(o, **attrs)
    )


class User(UserMixin):
    USERS = {}
    
    def __init__(self, id, email, password): 
        self._id = id
        self.email = email
        self.password = password
        self.USERS[str(id)] = self

    @property
    def id(self):
        return str(self._id)

    @classmethod
    def _that_has(cls, **attrs):
        return next(iter(stuff_with_attrs(cls.USERS, **attrs).values()), None)

    @classmethod
    def with_login(cls, email, password):
        return cls._that_has(email=email, password=password)

@dataclass
class Content:
    name: str
    special: bool = False
    protected: bool = False
    is_login: bool = False

    ALL: ClassVar[dict[str, 'Content']] = {}

    def __post_init__(self):
        self.ALL[self.name] = self

    @property
    def capitalized(self):
        return (self.name[0].upper() + self.name[1:])

    @property
    def html(self):
        return self.name + '.html'

    def _css_classify(self, stub, routed_content):
        s = stub
        if self == routed_content: 
            s += ' selected'         
        return s

    def css_classify_button(self, routed_content):
        return self._css_classify('contentButton', routed_content)

    def css_classify_content(self, routed_content):
        return self._css_classify('content', routed_content)
       
    @classmethod
    def with_attrs(cls, **attrs):
        return stuff_with_attrs(cls.ALL, **attrs)

    @classmethod
    def NORMALS(cls):
        return cls.with_attrs(special=False)

    @classmethod
    def PROTECTEDS(cls):
        return cls.with_attrs(protected=True)
        
    @classmethod
    def UNPROTECTEDS(cls):
        return cls.with_attrs(protected=False)

    @classmethod
    def contextual_contents(cls):
        return \
            cls.with_attrs(is_login=False) \
                if current_user.is_authenticated else \
            cls.UNPROTECTEDS()
    
Content('login', is_login=True)
Content('logout', special=True, protected=True)
Content('home')
Content('members')

ADMIN = User(1, 'admin@dometodik.se', 'admin')

@login_manager.user_loader
def load_user(user_id):
    return User.USERS[user_id]

def base_render(content='home', failed_login=False):
    return render_template('base.html', 
                           content=Content.ALL[content],
                           Content=Content,
                           failed_login=failed_login)


@app.route('/login', methods=(['POST']))
def login():
    """Login a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    found_user = User.with_login(email, password)
    if found_user:
        login_user(User.USERS[found_user.id])
        return redirect('/')
    else:
        return base_render(content='login', failed_login=True) 
        

@app.route('/logout', methods=(['GET']))
def logout():
    logout_user()
    return redirect('/')


@app.route(f'/<any({", ".join(Content.NORMALS())}):content>')
def content_route(content):
    return base_render(content=content)

@app.route('/')
def base():
    return redirect('/home')

