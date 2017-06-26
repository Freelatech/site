from application import db

class Agendamento(db.Model):
    __tablename__='agendamentos'
    id=db.Column(db.Integer, primary_key=True)
    dest_user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    service_id=db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    horario=db.Column(db.Text, nullable=False)

class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    username = db.Column(db.String)
    passwordhsh = db.Column(db.String)
    method = db.Column(db.String)
        
class Classe(db.Model):
    __tablename__='classes'
    id=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String)
    subclasses = db.relationship('Subclasse', backref='classe', lazy='dynamic')
    diferenciais = db.relationship('Diferencial', backref='classe', lazy='dynamic')
    
class Diferencial(db.Model):
    __tablename__='diferenciais'
    id=db.Column(db.Integer, primary_key=True)
    classe_id=db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    nome=db.Column(db.String)
        
class Opfin(db.Model):
    __tablename__='opfin'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    valor=db.Column(db.Numeric(8,2), nullable=False)
    tipo=db.Column(db.Integer, nullable=False)
    
class Service(db.Model):
    __tablename__='services'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.Text, default="")
    imageurl=db.Column(db.String, default="https://www.neto.com.au/assets/images/default_product.gif")
    videourl=db.Column(db.String)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    horarios=db.Column(db.Text, nullable=False)
    subclass_id=db.Column(db.Integer, db.ForeignKey("subclasses.id"))
    status=db.Column(db.Integer)
    agendados=db.relationship('Agendamento', backref='service', lazy='dynamic')
    
class Subclasse(db.Model):
    __tablename__='subclasses'
    id=db.Column(db.Integer, primary_key=True)
    classe_id=db.Column(db.Integer, db.ForeignKey("classes.id"))
    nome=db.Column(db.String)
    services=db.relationship('Service', backref='subclasse', lazy='dynamic')
    
class Transaction(db.Model):
    __tablename__='transactions'
    id=db.Column(db.Integer, primary_key=True)
    orig_user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    orig_user=db.relationship('User', backref='transactasorig', foreign_keys=orig_user_id)
    orig_value=db.Column(db.Numeric(8,2), nullable=False)
    dest_user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dest_user=db.relationship('User', backref='transactasdest', foreign_keys=dest_user_id)
    dest_value=db.Column(db.Numeric(8,2), nullable=False)
    service_id=db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    def __repr__(self):
        return '%i' % (self.id)
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, default="")
    email = db.Column(db.String)
    telefone = db.Column(db.String, default="")
    profilepicurl = db.Column(db.String, default="http://4.bp.blogspot.com/-zsbDeAUd8aY/US7F0ta5d9I/AAAAAAAAEKY/UL2AAhHj6J8/s1600/facebook-default-no-profile-pic.jpg")
    description = db.Column(db.Text, default="")
    money = db.Column(db.Numeric(8,2), default=0)
    services = db.relationship('Service', backref='author', lazy='dynamic')
    agendamentos = db.relationship('Agendamento', backref='dest_user', lazy='dynamic')
    auth = db.relationship('Auth', backref='user', uselist=False)
    operações = db.relationship('Opfin', backref='user', lazy='dynamic')
    referrer_id = db.Column(db.Integer, db.ForeignKey(id))
    referrees = db.relationship('User', backref=db.backref('referrer', remote_side='User.id'))
    def __repr__(self):
        return '<User %r>' % (self.email)

