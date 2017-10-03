from application import db

class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    username = db.Column(db.String)
    passwordhsh = db.Column(db.String)
    method = db.Column(db.String)
    def __repr__(self):
        return '%r' % (self.username)

class Classe(db.Model):
    __tablename__='classes'
    id=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String)
    subclasses = db.relationship('Subclasse', backref='classe', lazy='dynamic')
    prestadores = db.relationship('Prestador', backref='classe', lazy='dynamic')
    def __repr__(self):
        return '%r' % (self.nome)

class Educ(db.Model):
    __tablename__='educ'
    id=db.Column(db.Integer, primary_key=True)
    prest_id=db.Column(db.Integer, db.ForeignKey("prestadores.id"))
    instituicao=db.Column(db.String, default="")
    curso=db.Column(db.String, default="")
    anoinicio=db.Column(db.Integer, default=0)
    anoconclusao=db.Column(db.Integer, default=0)
    descricao=db.Column(db.Text, default="")

class Experiencia(db.Model):
    __tablename__='experiencia'
    id=db.Column(db.Integer, primary_key=True)
    prest_id=db.Column(db.Integer, db.ForeignKey("prestadores.id"))
    local=db.Column(db.String, default="")
    funcao=db.Column(db.String, default="")
    anoinicio=db.Column(db.Integer, default=0)
    anoconclusao=db.Column(db.Integer, default=0)
    descricao=db.Column(db.Text, default="")

class Cert(db.Model):
    __tablename__='cert'
    id=db.Column(db.Integer, primary_key=True)
    prest_id=db.Column(db.Integer, db.ForeignKey("prestadores.id"))
    local=db.Column(db.String, default="")
    nome=db.Column(db.String, default="")
    anoinicio=db.Column(db.Integer, default=0)
    anoconclusao=db.Column(db.Integer, default=0)
    descricao=db.Column(db.Text, default="")

class Horario(db.Model):
    __tablename__='horario'
    prest_id=db.Column(db.Integer, db.ForeignKey("prestadores.id"), primary_key=True)
    horario=db.Column(db.Integer, primary_key=True)
    status=db.Column(db.Boolean)

class Prestador(db.Model):
    __tablename__='prestadores'
    id=db.Column(db.Integer, primary_key=True)
    descricao=db.Column(db.Text, default="")
    sobre=db.Column(db.Text, default="")
    imageurl=db.Column(db.String, default="")
    videourl=db.Column(db.String, default="")
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    classe_id=db.Column(db.Integer, db.ForeignKey("classes.id"), default=0)
    subclasse_id=db.Column(db.Integer, db.ForeignKey("subclasses.id"), default=0)
    preco=db.Column(db.Numeric(10,2), default=0.00)
    status=db.Column(db.Integer, default=0)
    seg=db.Column(db.Boolean, default=False)
    ter=db.Column(db.Boolean, default=False)
    qua=db.Column(db.Boolean, default=False)
    qui=db.Column(db.Boolean, default=False)
    sex=db.Column(db.Boolean, default=False)
    sab=db.Column(db.Boolean, default=False)
    dom=db.Column(db.Boolean, default=False)
    man=db.Column(db.Boolean, default=False)
    tar=db.Column(db.Boolean, default=False)
    noi=db.Column(db.Boolean, default=False)
    mad=db.Column(db.Boolean, default=False)
    educ=db.relationship('Educ', backref='prestador', lazy='dynamic')
    experiencia=db.relationship('Experiencia', backref='prestador', lazy='dynamic')
    cert=db.relationship('Cert', backref='prestador', lazy='dynamic')
    horarios=db.relationship('Horario', backref='prestador', lazy='dynamic')

class Subclasse(db.Model):
    __tablename__='subclasses'
    id=db.Column(db.Integer, primary_key=True)
    classe_id=db.Column(db.Integer, db.ForeignKey("classes.id"))
    nome=db.Column(db.String)
    prestador=db.relationship('Prestador', backref='subclasse', lazy='dynamic')
    def __repr__(self):
        return '%r' % (self.nome)

class Sugestao(db.Model):
    __tablename__='sugestoes'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String)
    nome=db.Column(db.String)
    sugestao=db.Column(db.Text)

class Suporte(db.Model):
    __tablename__='suporte'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String)
    nome=db.Column(db.String)
    assunto=db.Column(db.String)
    mensagem=db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nomecomp = db.Column(db.String, default="")
    email = db.Column(db.String)
    telefone = db.Column(db.String, default="")
    urlfoto = db.Column(db.String, default="http://4.bp.blogspot.com/-zsbDeAUd8aY/US7F0ta5d9I/AAAAAAAAEKY/UL2AAhHj6J8/s1600/facebook-default-no-profile-pic.jpg")
    money = db.Column(db.Numeric(8,2), default=0)
    auth = db.relationship('Auth', backref='user', uselist=False)
    referrer_id = db.Column(db.Integer, db.ForeignKey(id))
    referrees = db.relationship('User', backref=db.backref('referrer', remote_side='User.id'))
    prest = db.relationship('Prestador', backref='username', lazy='dynamic')
    def __repr__(self):
        return '%r' % (self.auth)

