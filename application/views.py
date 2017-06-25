from application import app, db
from flask import flash, jsonify, redirect, render_template, request, session, url_for
import json
from collections import OrderedDict
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from passlib.apps import custom_app_context as pwd_context
from application.helpers import env, login_required
from application.models import Agendamento, Auth, Classe, Diferencial, Opfin, Service, Subclasse, Transaction, User

admin = Admin(app, name='usomix', template_mode='bootstrap3')
admin.add_view(ModelView(Agendamento, db.session))
admin.add_view(ModelView(Auth, db.session))
admin.add_view(ModelView(Classe, db.session))
admin.add_view(ModelView(Opfin, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(Subclasse, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(User, db.session))

@app.route("/")
def index():
    teste=User.query.all()
    print(teste[0].auth.username)
    return render_template("index.html")
  
@app.route("/blog")
def blog():
    return render_template("blog.html")
    
@app.route("/encontre")
def encontre():
    return render_template("encontre.html")
    
@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    if request.method == "POST":
        if not request.form.get("email"):
            return render_template("entrar.html", message="Não há email", dest=request.args.get("dest"))
        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("entrar.html", message="Não há senha", dest=request.args.get("dest"))
        #query database for username
        try:
            prevrows = User.query.filter_by(email=request.form.get("email")).one()
            rows = Auth.query.filter_by(user_id=prevrows.id).one()
        except:
            try:
                rows = Auth.query.filter_by(username=request.form.get("email")).one()
            except:
                return render_template("entrar.html", message="email/usuário inexistente", dest=request.args.get("dest"))
        # ensure username exists and password is correct
        if not pwd_context.verify(request.form.get("password"), rows.passwordhsh):
            return render_template("entrar.html", message="email/usuário ou senha incorretos", dest=request.args.get("dest"))
        session["user_id"] = rows.user_id
        session["user_name"] = rows.username.upper()
        db.session.commit()
        try:
            return redirect(url_for(request.args.get("dest")))
        except:
            return redirect(url_for('index'))
        
    else:
        return render_template("entrar.html",dest=request.args.get("dest"))
    
@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")
    
    
@app.route("/getsubclasses/<classid>")
def getsubclasses(classid):
    subclasses=Subclasse.query.filter_by(classe_id=classid).order_by(Subclasse.nome).all()
    string="{"
    for i in range(len(subclasses)):
        string=string+'"'+str(subclasses[i].id)+'":"'+subclasses[i].nome+'"'
        if (i != len(subclasses) -1):
            string=string+","
    string=string+"}"
    jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
    return jsonify(jsonstring)
    
@app.route("/indique")
def indique():
    return render_template("indique.html")
    
@app.route("/myusers")
@login_required
def myusers():
    myuser = Auth.query.filter_by(id=session["user_id"]).all()
    return jsonify(myuser[0].serialize())
    #return render_template("entrar.html")
    
    
    
@app.route("/ofereça", methods=["GET", "POST"])
def ofereça():
    if request.method == "POST":
        new_service = Service(
            name=request.form.get("nomeser"), 
            description=request.form.get("description"), 
            imageurl=request.form.get("imageurl"), 
            videourl=request.form.get("videourl"),
            user_id=session["user_id"],
            horarios="Not yet",
            classe=request.form.get("classe"),
            subclasse=request.form.get("subclasse")
            )
        db.session.add(new_service)
        try:
            db.session.commit()
        except:
            return render_template("ofereça.html", message="There was an error, please try again")
        return redirect(url_for('index'))
    else:
        try:
            teste=session["user_id"]
            classes=Classe.query.order_by(Classe.nome).all()
            print (classes)
            string="{"
            for i in range(len(classes)):
                string=string+'"'+str(classes[i].id)+'":"'+classes[i].nome+'"'
                if (i != len(classes) -1):
                    string=string+","
            string=string+"}"
            print (string)
            jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
            return render_template("oferecer.html", classes=jsonstring)
        except:
            return render_template("ofereça.html")
        
@app.route("/perfil", methods=["GET","POST"])
@login_required
def perfil():
    if request.method=="POST":
        rows = User.query.filter_by(id=session["user_id"]).one()
        rows.email=request.form.get("email")
        rows.fullname=request.form.get("nome")
        rows.telefone=request.form.get("telefone")
        db.session.add(rows)
        db.session.commit()
        return render_template("perfil.html", email=rows.email, fullname=rows.fullname, telefone=rows.telefone)
    else:
        rows = User.query.filter_by(id=session["user_id"]).one()
        db.session.commit()
        return render_template("perfil.html", email=rows.email, fullname=rows.fullname, telefone=rows.telefone)
    
@app.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")
    
@app.route("/registrar",  methods=["GET", "POST"])
def registrar():
    """Register user"""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("email"):
            return render_template("registrar.html", message="Não há email")
        
        #ensure username was submitted
        elif not request.form.get("username"):
            return render_template("registrar.html", message="Não há nome de usuário")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("registrar.html", message="Não há senha")
            
        elif len(request.form.get("password"))<6:
            return render_template("registrar.html", message="Senha muito curta")
            
        elif request.form.get("password")!=request.form.get("password2"):
            return render_template("registrar.html", message="Senhas diferentes")

        #query database for username
        userrows = Auth.query.filter_by(username=request.form.get("username")).all()

        # ensure username exists and password is correct
        if len(userrows) != 0:
            return render_template("registrar.html", message="Usuário já em uso")
            
        #query database for username
        emailrows = User.query.filter_by(email=request.form.get("email")).all()

        # ensure username exists and password is correct
        if len(emailrows) != 0:
            return render_template("registrar.html", message="Email já em uso")
        
        
        new_user = User(                       
                         email=request.form.get("email"), 
                        )
        db.session.add(new_user)
        db.session.flush()
        user_id=new_user.id
        new_auth = Auth(
                        user_id=new_user.id, 
                        username=request.form.get("username"), 
                        passwordhsh=pwd_context.hash(request.form.get("password")), 
                        method="Common"
                        )
        db.session.add(new_auth)
        db.session.commit()
        # redirect user to home page
        return redirect(url_for("entrar"))
        
    else:
        return render_template("registrar.html")
        
        
@app.route("/sair", methods=["GET","POST"])
def sair():
    session.clear()
    return redirect(url_for("index"))
    
@app.route("/sugestoes")
def sugestoes():
    return render_template("sugestoes.html")

@app.route("/suporte")
def suporte():
    return render_template("suporte.html")
    
@app.route("/termos")
def termos():
    rule=str(request.url_rule)
    rule=rule[1:]
    return render_template("nos.html", route=rule)
    
@app.route("/teste", methods=["GET", "POST"])
def teste():
    if request.method=="POST":
        new_subclass=Subclasse(
                classe_id=request.form.get("classid"),
                nome=request.form.get("nome")
            )
        db.session.add(new_subclass)
        db.session.commit()
        return render_template("teste.html")
    else:
        return render_template("teste.html")
    
@app.route("/trabalhe")
def trabalhe():
    return render_template("trabalhe.html")
    
@app.route("/verifyuser/<pat>")
def verifyuser(pat):
    rows = Auth.query.filter_by(username=pat).first()
    if len(rows) != 0:
       return jsonify({"userexists":True})
    return jsonify({"userexists":False})
    
@app.route("/verifyemail/<path:path>")
def verifyemail(path):
    rows = User.query.filter_by(email=path).all()
    if len(rows) != 0:
       return jsonify({"emailexists":True})
    return jsonify({"emailexists":False})
  
        
@app.route("/<path:path>")
def errhandler(path):
    return render_template("error.html")
