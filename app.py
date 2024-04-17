from flask import Flask, render_template, send_from_directory, send_file, request, jsonify
from datetime import datetime
from PIL import Image
import random, string, qrcode, io

app = Flask(__name__, template_folder='src', static_folder='src')

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
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int(argument)))
    
    return jsonify({'key': token})

@app.route('/qrcode', methods=['GET'])
def generate_qrcode():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'erreur': 'Veuillez fournir un argument valide (?url={URL})'})

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=18, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')

@app.route('/domain', methods=['GET'])
def generate_domain():
    noms = ['example', 'site', 'test', 'demo']
    extensions = ['.com', '.fr', '.eu', '.dev', '.net', '.org', '.io']
    domain = random.choice(noms) + random.choice(extensions)
    return jsonify({'domain': domain, 'random_name': random.choice(noms), 'random_tld': random.choice(extensions)})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'erreur': 'Veuillez fournir un endpoint valide'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)