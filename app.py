from flask import Flask, render_template, send_from_directory, request
import random
import string

app = Flask(__name__, template_folder="src", static_folder="src")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/password', methods=['GET'])
def generate_password():
    token = request.args.get('len', '')
    if not token.isdigit():
        token = '24'
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(int(token)))
    
    return {'key': password}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)