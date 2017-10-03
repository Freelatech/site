from wtforms import Form, BooleanField, StringField, DateField, DateTimeField, DecimalField, FileField, FloatField, HiddenField, IntegerField, PasswordField, RadioField, SelectField, SelectMultipleField, SubmitField, TextField, TextAreaField, validators, widgets

choices=[]
for j in range(0,48):
    for i in range(0,7):
        value=i*48+j
        label=''
        if j<20:
            label=label+'0'
        label=label+str(int((j-j%2)/2))+':'
        if j%2==1:
            label=label+'3'
        else:
            label=label+'0'
        label=label+'0'
        choices.append(tuple((value,label)))

class LoginForm(Form):
    email = StringField(u'email', [validators.required(message="email inválido"), validators.Email(message="email inválido")])
    senha = PasswordField(u'senha', [validators.required(), validators.length(min=6)])
    submit = SubmitField('')

class RegisterForm(Form):
    email = StringField(u'email', [validators.required(), validators.Email()])
    nome = StringField(u'nome', [validators.required()])
    senha = PasswordField(u'senha', [validators.required(), validators.length(min=6)])
    senha1 = PasswordField(u'confirme', [validators.required(), validators.EqualTo('senha', message='Senhas não combinam')])
    submit = SubmitField('')


class CertForm(Form):
    local = StringField(u'Instituição', [validators.required()])
    nome = StringField(u'Nome', [validators.required()])
    anoinicio = IntegerField(u'Ano de Início', [validators.required()])
    anotermino = IntegerField(u'Ano de Conclusão', [validators.required()])
    descricao = StringField(u'Descricão', [validators.required()])
    submit = SubmitField('')

class EducForm(Form):
    instituicao = StringField(u'Instituição', [validators.required()])
    curso = StringField(u'Curso', [validators.required()])
    anoinicio = IntegerField(u'Ano de Início', [validators.required()])
    anotermino = IntegerField(u'Ano de Conclusão', [validators.required()])
    descricao = StringField(u'Descricão', [validators.required()])
    submit = SubmitField('')

class ExpForm(Form):
    local = StringField(u'Instituição', [validators.required()])
    funcao = StringField(u'Nome', [validators.required()])
    anoinicio = IntegerField(u'Ano de Início', [validators.required()])
    anotermino = IntegerField(u'Ano de Conclusão', [validators.required()])
    descricao = StringField(u'Descricão', [validators.required()])
    submit = SubmitField('')

class PrestForm(Form):
    videourl = StringField(u'URL vídeo', [validators.optional()])
    imageurl = StringField(u'URL foto', [validators.optional()])
    descricao = TextAreaField(u'Descrição', [validators.optional()])
    sobre = TextAreaField(u'Sobre mim', [validators.optional()])
    preco = DecimalField(u'Preço', [validators.optional()])
    submit = SubmitField('')