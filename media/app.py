from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/mydatabase'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

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
            
            return "Arquivo enviado com sucesso!"
    
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5001)