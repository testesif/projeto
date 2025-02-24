from flask import Flask, render_template

app = Flask(__name__)

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)