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

@app.route('/username', methods=['GET'])
def generate_username():
    adj = ['Happy', 'Silly', 'Clever', 'Creative', 'Brave', 'Gentle', 'Kind', 'Funny', 'Wise', 'Charming', 'Sincere', 'Resourceful', 'Patient', 'Energetic', 'Adventurous', 'Ambitious', 'Courageous', 'Courteous', 'Determined']
    ani = ['Cat', 'Dog', 'Tiger', 'Elephant', 'Monkey', 'Penguin', 'Dolphin', 'Lion', 'Bear', 'Fox', 'Owl', 'Giraffe', 'Zebra', 'Koala', 'Rabbit', 'Squirrel', 'Panda', 'Horse', 'Wolf', 'Eagle']
    pro = ['Writer', 'Artist', 'Musician', 'Explorer', 'Scientist', 'Engineer', 'Athlete', 'Chef', 'Doctor', 'Teacher', 'Lawyer', 'Entrepreneur', 'Actor', 'Dancer', 'Photographer', 'Architect', 'Pilot', 'Designer', 'Journalist', 'Veterinarian']
    
    choix = random.choice(['adj_num', 'ani_num',  'pro_num',  'adj_ani',  'adj_ani_num', 'adj_pro', 'pro_ani', 'pro_ani_num'])
    nombre = str(random.randint(0, 99))
    if choix == 'adj_num':
        username = random.choice(adj) + nombre
    elif choix == 'ani_num':
        username = random.choice(ani) + nombre
    elif choix == 'pro_num':
        username = random.choice(pro) + nombre
    elif choix == 'adj_ani':
        username = random.choice(adj) + random.choice(ani)
    elif choix == 'adj_ani_num':
        username = random.choice(adj) + random.choice(ani) + nombre
    elif choix == 'adj_pro':
        username = random.choice(adj) + random.choice(pro)
    elif choix == 'pro_ani':
        username = random.choice(pro) + random.choice(ani)
    elif choix == 'pro_ani_num':
        username = random.choice(pro) + random.choice(ani) + nombre
    
    return jsonify({'username': username, 'adjectif': adj, 'animal': ani, 'profession': pro, 'nombre': nombre})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'erreur': 'Veuillez fournir un endpoint valide'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)