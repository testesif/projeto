from flask import Flask, request, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/mydatabase'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Senha para acessar o dashboard
DASHBOARD_PASSWORD = "adminproj"  # Defina sua senha aqui

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def media():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            new_submission = Submission(
                name=name,
                email=email,
                filename=filename
            )
            db.session.add(new_submission)
            db.session.commit()
            
            return redirect(url_for('success'))
    
    return render_template('upload.html')

@app.route('/')
def success():
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    # Verifica se a senha foi enviada no cabeçalho de autenticação
    auth = request.authorization
    if not auth or auth.username != "admin" or auth.password != DASHBOARD_PASSWORD:
        # Retorna um erro 401 (Não autorizado) e solicita autenticação
        return (
            "Acesso negado. Por favor, insira as credenciais corretas.",
            401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )
    
    # Se a autenticação for bem-sucedida, exibe o dashboard
    submissions = Submission.query.all()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dashboard.html', submissions=submissions, files=files)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5001)