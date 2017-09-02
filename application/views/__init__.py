from application import app, db
from sqlalchemy import or_
from flask import flash, jsonify, redirect, render_template, request, session, url_for
import json
from collections import OrderedDict
from passlib.apps import custom_app_context as pwd_context
from application.helpers import env, login_required
from application.models import Auth, Classe, Educ, Experiencia, Cert, Horario, Prestador, Subclasse, Sugestao, Suporte, User

@app.route("/")
def index():
    try:
        teste=session["user_id"]
        return redirect(url_for('encontre'))
    except:
        return render_template("index.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/encontre")
def encontre():
    kwargs={}
    if request.args.get("classe")!=None:
        kwargs['classe_id']=request.args.get("classe")
    if request.args.get("subclasse")!=None:
        kwargs['subclasse_id']=request.args.get("subclasse")
    dlist=request.args.getlist("dia")
    hlist=request.args.getlist("hor")
    dargs={}
    hargs={}
    for d in dlist:
        dargs[d]=True
    for h in hlist:
        hargs[h]=True
    teste=Prestador.query.filter(or_(*dargs)).filter(or_(*hargs)).filter_by(**kwargs).all()
    classes=Classe.query.order_by(Classe.nome).all()
    string="{"
    for i in range(len(classes)):
        string=string+'"'+str(classes[i].id)+'":"'+classes[i].nome+'"'
        if (i != len(classes) -1):
            string=string+","
    string=string+"}"
    jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
    print (request.args.getlist("dia"))
    #x=Prestador.query.all()
    #teste=x[0].horarios.filter_by(status=True).all()
    #teste=Prestador.query.filter(Prestador.horarios[10].has(status=False)).all()
    return render_template("encontre.html", classes=jsonstring, teste=teste)

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
        session["tempeduc"]=[]
        session["tempcert"]=[]
        session["tempexp"]=[]
        db.session.commit()
        try:
            return redirect(url_for(request.args.get("dest")))
        except:
            return redirect(url_for('index'))

    else:
        try:
            teste=session["user_id"]
            return redirect(url_for('encontre'))
        except:
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

@app.route("/oferecer", methods=["GET","POST"])
def oferecer():
    if request.method=="POST":
        prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
        prest.videourl=request.form.get("videourl")
        prest.descricao=request.form.get("descricao")
        prest.sobre=request.form.get("sobre")
        prest.classe_id=request.form.get("classe")
        prest.subclasse_id=request.form.get("subclasse")
        prest.preco=request.form.get("preco")
        hor=Horario.query.filter_by(prest_id=prest.id).order_by(Horario.horario).all()
        horlist=request.form.getlist('horario')
        print(horlist)
        prest.seg=False
        prest.ter=False
        prest.qua=False
        prest.qui=False
        prest.sex=False
        prest.sab=False
        prest.dom=False
        prest.man=False
        prest.tar=False
        prest.noi=False
        prest.mad=False
        horlist = list(map(int, horlist))
        if len(horlist)>0:
            for h in horlist:
                if(h<48):
                    prest.dom=True
                    break;
            for h in horlist:
                if(h>=48 and h<96):
                    prest.seg=True
                    break;
            for h in horlist:
                if(h>=96 and h<144):
                    prest.ter=True
                    break;
            for h in horlist:
                if(h>=144 and h<192):
                    prest.qua=True
                    break;
            for h in horlist:
                if(h>=192 and h<240):
                    prest.qui=True
                    break;
            for h in horlist:
                if(h>=240 and h<288):
                    prest.sex=True
                    break;
            for h in horlist:
                if(h>=288 and h<336):
                    prest.sab=True
                    break;
            for h in horlist:
                if(h%48>=12 and h%48<24):
                    prest.man=True
                    break;
            for h in horlist:
                if(h%48>=24 and h%48<36):
                    prest.tar=True
                    break;
            for h in horlist:
                if(h%48>=36):
                    prest.noi=True
                    break;
            for h in horlist:
                if(h%48<12):
                    prest.mad=True
                    break;
            horlist.sort()
            print(horlist)
            horlist.append(0)
            print(horlist)
            atual=0;
            for i in range(0,336):
                if hor[i].horario==horlist[atual]:
                    hor[i].status=True
                    atual=atual+1
                    print(atual)
                    print(hor[i].horario)
                else:
                    hor[i].status=False
                db.session.add(hor[i])
        else:
            for i in range(0,336):
                hor[i].status=False
                db.session.add(hor[i])
        db.session.add(prest)
        for x in session["tempexp"]:
            db.session.add(x)
        for x in session["tempcert"]:
            db.session.add(x)
        for x in session["tempeduc"]:
            db.session.add(x)
        db.session.commit()
        session["tempexp"]=[]
        session["tempcert"]=[]
        session["tempeduc"]=[]
        return redirect(url_for('encontre'))
    else:
        teste=session["user_id"]
        classes=Classe.query.order_by(Classe.nome).all()
        string="{"
        for i in range(len(classes)):
            string=string+'"'+str(classes[i].id)+'":"'+classes[i].nome+'"'
            if (i != len(classes) -1):
                string=string+","
        string=string+"}"
        jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
        prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
        educ=Educ.query.filter_by(prest_id=session["user_id"]).all()
        cert=Cert.query.filter_by(prest_id=session["user_id"]).all()
        exp=Experiencia.query.filter_by(prest_id=session["user_id"]).all()
        hor=Horario.query.filter_by(prest_id=prest.id, status=True).order_by(Horario.horario%48).all()
        new_hor=Horario(
                prest_id=prest.id,
                horario=337,
                status=True
            )
        hor.append(new_hor)
        return render_template("oferecer.html",classes=jsonstring,prest=prest,educ=educ,cert=cert,exp=exp,tempeduc=session["tempeduc"],tempcert=session["tempcert"],tempexp=session["tempexp"],hor=hor)

@app.route("/ofereça")
def ofereça():
    try:
        teste=session["user_id"]
        return redirect(url_for("oferecer"))
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
    rule=str(request.url_rule)
    rule=rule[1:]
    return render_template("nos.html", route=rule)

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
        new_prest = Prestador(
                user_id=new_user.id,
            )
        db.session.add(new_auth)
        db.session.add(new_prest)
        db.session.flush()
        for i in range(0,336):
            new_hor = Horario(
                prest_id=new_prest.id,
                horario=i,
                status=False
                )
            db.session.add(new_hor)
        db.session.commit()
        # redirect user to home page
        return redirect(url_for("entrar"))

    else:
        return render_template("registrar.html")


@app.route("/sair", methods=["GET","POST"])
def sair():
    session.clear()
    return redirect(url_for("index"))

@app.route("/sugestoes", methods=["GET", "POST"])
def sugestoes():
    if request.method == "POST":
        new_sugest=Sugestao(
            email=request.form.get("email"),
            nome=request.form.get("nome"),
            sugestao=request.form.get("sugestao")
            )
        db.session.add(new_sugest)
        db.session.commit()
        return render_template("sugestoes.html")
    else:
        return render_template("sugestoes.html")

@app.route("/suporte", methods=["GET", "POST"])
def suporte():
    if request.method == "POST":
        new_suport=Suporte(
            email=request.form.get("email"),
            nome=request.form.get("nome"),
            assunto=request.form.get("assunto"),
            mensagem=request.form.get("mensagem")
            )
        db.session.add(new_suport)
        db.session.commit()
        return render_template("suporte.html")
    else:
        return render_template("suporte.html")

@app.route("/termos")
def termos():
    rule=str(request.url_rule)
    rule=rule[1:]
    return render_template("nos.html", route=rule)

@app.route("/educ", methods=["POST"])
def educ():
    try:
        prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
    except:
        new_prest=Prestador(
                user_id=session["user_id"]
            )
        db.session.add(new_prest)
        db.session.flush()
        prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
    new_educ=Educ(
                prest_id=prest.id,
                instituicao=request.form.get("instituicao"),
                curso=request.form.get("curso"),
                anoinicio=request.form.get("anoinicio"),
                anoconclusao=request.form.get("anoconclusao"),
                descricao=request.form.get("descricao")
            )
    session["tempeduc"].append(new_educ)
    return "success"

@app.route("/certificacao", methods=["POST"])
def certificacao():
    prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
    new_cert=Cert(
                prest_id=prest.id,
                local=request.form.get("local"),
                nome=request.form.get("nome"),
                anoinicio=request.form.get("anoinicio"),
                anoconclusao=request.form.get("anoconclusao"),
                descricao=request.form.get("descricao")
            )
    session["tempcert"].append(new_cert)
    return "success"

@app.route("/experiencia", methods=["POST"])
def experiencia():
    prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
    new_exp=Experiencia(
                prest_id=prest.id,
                local=request.form.get("local"),
                funcao=request.form.get("funcao"),
                anoinicio=request.form.get("anoinicio"),
                anoconclusao=request.form.get("anoconclusao"),
                descricao=request.form.get("descricao")
            )
    #db.session.add(new_exp)
    #a=len(session["temp"])
    #session["temp"][a]=new_exp
    session["tempexp"].append(new_exp)
    return "success"

@app.route("/teste", methods=["GET", "POST"])
def teste():
    if request.method=="POST":
        new_subclass=Subclasse(
                classe_id=request.form.get("classid"),
                nome=request.form.get("nome")
            )
        db.session.add(new_subclass)
        db.session.commit()
        classes=Classe.query.order_by(Classe.nome).all()
        string="{"
        for i in range(len(classes)):
            string=string+'"'+str(classes[i].id)+'":"'+classes[i].nome+'"'
            if (i != len(classes) -1):
                string=string+","
        string=string+"}"
        jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
        return render_template("teste.html", classes=jsonstring)
    else:
        classes=Classe.query.order_by(Classe.nome).all()
        string="{"
        for i in range(len(classes)):
            string=string+'"'+str(classes[i].id)+'":"'+classes[i].nome+'"'
            if (i != len(classes) -1):
                string=string+","
        string=string+"}"
        jsonstring=json.loads(string, object_pairs_hook=OrderedDict)
        return render_template("teste.html",classes=jsonstring)

@app.route("/trabalhe")
def trabalhe():
    return render_template("trabalhe.html")

@app.route("/verifyuser/<pat>")
def verifyuser(pat):
    rows = Auth.query.filter_by(username=pat).all()
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
