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

@app.route('/token', methods=['GET'])
def generate_token():
    argument = request.args.get('len', '')
    if not argument.isdigit():
        argument = '24'
    elif int(argument) < 12:
        argument = '12'
    elif int(argument) > 4096:
        argument = '4096'
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(int(argument)))
    
    return {'key': token}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)