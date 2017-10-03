from application import app, db
from sqlalchemy import or_
from flask import flash, jsonify, make_response, redirect, render_template, request, session, url_for
import json
#import admin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import random
import string
from collections import OrderedDict
from passlib.apps import custom_app_context as pwd_context
from application.helpers import env, login_required, createUser, getUserInfo, getUserID
from application.models import Auth, Classe, Educ, Experiencia, Cert, Horario, Prestador, Subclasse, Sugestao, Suporte, User
from application.forms import LoginForm, RegisterForm, PrestForm, ExpForm

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"
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
    prest=Prestador.query.filter(or_(*dargs)).filter(or_(*hargs)).filter_by(**kwargs).all()
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
    return render_template("encontre.html", classes=jsonstring, prest=prest)

@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        print("passou")
        try:
            prevrows = User.query.filter_by(email=form.email.data).one()
            rows = Auth.query.filter_by(user_id=prevrows.id).one()
        except:
            try:
                rows = Auth.query.filter_by(username=form.email.data).one()
            except:
                return render_template("entrar.html", message="email/usuário inexistente", dest=request.args.get("dest"))
        # ensure username exists and password is correct
        if not pwd_context.verify(form.senha.data, rows.passwordhsh):
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
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
        session['state'] = state
        try:
            teste=session["user_id"]
            return redirect(url_for('encontre'))
        except:
            return render_template("entrar.html", STATE=state, dest=request.args.get("dest"),form=form)

@app.route("/fbconnect")
def fbconnect():
    print ("1")
    if request.args.get('state') != session['state']:
        print("if")
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("else")
    access_token = request.data
    print ("access token received %s" % access_token)


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % app_id, app_secret, access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data['email']
    session['facebook_id'] = data['id']

    # The token must be stored in the session in order to properly logout
    session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    #see if user exists
    #if not create one

    output = ''
    output += '<h1>Welcome, '
    output += session['username']

    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return reponse
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")

@app.route("/gconnect", methods=["POST"])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #If there was an error in the access info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        respnse.headers['Content-Type']
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        responde = make_response(
            json.dumps("Token's client ID does not match app's"),401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentias.access_token, 'alt': "json"}
    answer = request.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    session['provider'] = 'google'

    #ver se o usuário existe, se não, criar um novo
    #Implementar aqui

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

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
    form = PrestForm(request.form)
    if request.method=="POST" and form.validate():
        prest=Prestador.query.filter_by(user_id=session["user_id"]).one()
        prest.imageurl=form.imageurl.data
        prest.videourl=form.videourl.data
        prest.descricao=form.descricao.data
        prest.sobre=form.sobre.data
        prest.classe_id=request.form.get("classe")
        prest.subclasse_id=request.form.get("subclasse")
        prest.preco=form.preco.data
        hor=Horario.query.filter_by(prest_id=prest.id).order_by(Horario.horario).all()
        horlist=request.form.get("horario")
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
        form.videourl.data=prest.videourl
        form.imageurl.data=prest.imageurl
        form.descricao.data=prest.descricao
        form.sobre.data=prest.sobre
        form.preco.data=prest.preco
        hor.append(new_hor)
        return render_template("oferecer.html",form=form,classes=jsonstring,prest=prest,educ=educ,cert=cert,exp=exp,tempeduc=session["tempeduc"],tempcert=session["tempcert"],tempexp=session["tempexp"],hor=hor)

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
    form=RegisterForm(request.form)
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST" and form.validate():

        #query database for username
        userrows = Auth.query.filter_by(username=form.nome.data).all()

        # ensure username exists and password is correct
        if len(userrows) != 0:
            return render_template("registrar.html", message="Usuário já em uso")

        #query database for username
        emailrows = User.query.filter_by(email=form.email.data).all()

        # ensure username exists and password is correct
        if len(emailrows) != 0:
            return render_template("registrar.html", message="Email já em uso")


        new_user = User(
                         email=form.email.data,
                        )
        db.session.add(new_user)
        db.session.flush()
        user_id=new_user.id
        new_auth = Auth(
                        user_id=new_user.id,
                        username=form.nome.data,
                        passwordhsh=pwd_context.hash(form.senha.data),
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
        return render_template("registrar.html", form=form)


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
    form=ExpForm(request.form)
    print(form.local.data)
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
