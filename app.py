from flask import Flask, render_template, send_from_directory, send_file, request, jsonify
from datetime import datetime
from PIL import Image
import random, string, qrcode, io

############################## PRINCIPAL ##############################

# Création de l'app Flask
app = Flask(__name__, template_folder='src', static_folder='src')

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour les langues
@app.route('/<lang>')
def lang(lang=None):
    if lang == 'fr':
        return render_template('fr/index.html')
    elif lang == 'en':
        return render_template('en/index.html')
    # Erreur si aucune langue n'est spécifiée
    return jsonify({'error': 'Language not found, please specify an existing language in the URL (/fr or /en)'})

# Redirection du fichier
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

####################### REDIRECTION VERS LANGUE #########################

# Détection de la langue et de l'endpoint demandé
@app.route('/<lang>/<endpoint>', methods=['GET'])
def redirect_page(lang, endpoint):
    # Si aucune langue n'est spécifiée, renvoyer un message d'erreur
    if lang not in ['fr', 'en']:
        return jsonify({'error': 'Please specify language in the URL (/fr or /en)'})
    
    # Fonction exécutée en fonction du service demandé
    if endpoint == 'color':
        return generate_color(lang)
    elif endpoint == 'domain':
        return generate_domain(lang)
    elif endpoint == 'lorem':
        return generate_lorem(lang)
    elif endpoint == 'personal':
        return generate_personal(lang)
    elif endpoint == 'qrcode':
        return generate_qrcode(lang)
    elif endpoint == 'token':
        return generate_token(lang)
    elif endpoint == 'username':
        return generate_username(lang)
    else:
        return jsonify({'error': 'Endpoint not found'})

####################### FONCTIONS DES ENDPOINTS #########################

# Génération de couleurs
def generate_color(lang):
    r, g, b = [random.randint(0, 255) for _ in range(3)]
    return jsonify({'hex': '#{0:02x}{1:02x}{2:02x}'.format(r, g, b), 'rgb': f'rgb({r}, {g}, {b})'})

# Génération de domaine
def generate_domain(lang):
    noms = ['example', 'site', 'test', 'demo']
    extensions = ['.com', '.fr', '.eu', '.dev', '.net', '.org', '.io']
    domain = random.choice(noms) + random.choice(extensions)
    return jsonify({'domain': domain, 'random_name': random.choice(noms), 'random_tld': random.choice(extensions)})

# Génération de texte Lorem
def generate_lorem(lang):
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras viverra, dui non cursus accumsan, lectus leo euismod augue, a gravida odio sapien quis elit. Vivamus vehicula nisi vitae lacinia elementum. Ut id velit quis velit feugiat elementum. Vivamus vulputate, nisl ac placerat laoreet, ex nisl suscipit ligula, volutpat dapibus elit neque non orci. Pellentesque quis lacus efficitur, egestas nisl vitae, tincidunt justo. In gravida enim et egestas dapibus. Cras tempus libero ut sapien efficitur egestas. Sed commodo volutpat suscipit. Proin vulputate ante nec lacus consequat ullamcorper. Pellentesque facilisis massa quam, in auctor neque imperdiet sit amet. Maecenas sagittis aliquam eleifend. Sed dapibus, urna ut molestie fringilla, orci lorem aliquet lacus, nec interdum tortor lacus eu mauris. Curabitur vitae faucibus mi. Duis eget tempus justo. Curabitur placerat nisl eu sem dictum, eget placerat lectus vehicula. Fusce sit amet ipsum in libero aliquam mattis sit amet quis mi. Suspendisse sollicitudin consequat diam sit amet luctus. Nunc dapibus dolor vel sagittis faucibus. Donec et lorem ante. Praesent bibendum ultricies dui, at posuere leo vulputate eu. Integer gravida ex vitae erat accumsan egestas. Sed id tellus nec felis volutpat congue. Ut eget suscipit tellus, et tempus massa. Aliquam id semper diam, feugiat congue arcu. Nunc pulvinar et nisi eu elementum. Morbi condimentum sapien at sapien gravida, vitae lacinia orci condimentum. Suspendisse scelerisque urna quis euismod mattis. Pellentesque pulvinar pretium massa at varius. In pulvinar, velit ac mattis scelerisque, mauris nibh aliquam ipsum, sed aliquam tellus erat quis lectus. Nunc semper enim a felis ultrices convallis. Etiam velit magna, porta nec dui sit amet, venenatis gravida ipsum. In vitae magna et orci consequat cursus id vitae ex. Nulla pharetra massa vel felis malesuada porttitor. Etiam convallis tellus a sodales ullamcorper. Sed hendrerit sollicitudin erat, sit amet sodales magna dignissim nec. Curabitur ut enim eget dolor tincidunt bibendum. Fusce fermentum quam et finibus laoreet. Aliquam vel sem vitae turpis sollicitudin tempus. Nam rutrum risus ultricies quam tempor mattis. Pellentesque at dui felis. Cras maximus malesuada metus vitae iaculis. Aliquam erat volutpat. Nunc facilisis pretium tellus, ut tincidunt lectus eleifend a. In vel lacinia est. Integer tristique non metus pulvinar vestibulum. Fusce sit amet velit vel libero viverra semper et vel sem. In justo libero, semper a mi varius, aliquet commodo eros. Pellentesque porttitor tellus sit amet est varius luctus. Mauris placerat porta eros. Aliquam et mi id justo auctor semper ac vitae tellus. Donec auctor porttitor enim, at ornare ante ornare vel. Pellentesque sagittis ligula vitae libero vestibulum eleifend. Duis sit amet ullamcorper leo. Integer id dui velit. Quisque posuere nulla ligula, at consectetur metus finibus quis. Vestibulum sit amet neque iaculis, malesuada ipsum eget, feugiat nibh. Donec id ultricies enim, tincidunt volutpat arcu. Etiam vitae metus in mauris semper tempus. In dapibus neque at lorem pulvinar congue. Etiam ultrices tristique leo id interdum"
    argument = request.args.get('len', '')
    if not argument.isdigit() or int(argument) < 1:
        argument = 1

    sentences = text.split('. ')
    output = '. '.join(sentences[:int(argument)])
    return jsonify({'text': output + '.'})

# Génération d'informations personnelles
def generate_personal(lang):
    noms = ['John Doe', 'Jane Martin', 'Michael Johnson', 'Emily Davis', 'Alexis Barbos']
    emails = ['john@example.com', 'jane@example.com', 'michael@example.com', 'emily@example.com', 'alexis@example.com']
    tel = ['123-456-7890', '06 78 90 12 34', '7911 123456', '678 901 234', '163 555 1584']
    pays = ['US', 'FR', 'UK', 'ES', 'DE']
    job = ['Writer', 'Artist', 'Musician', 'Explorer', 'Scientist', 'Engineer', 'Athlete', 'Doctor', 'Teacher', 'Lawyer', 'Entrepreneur', 'Actor', 'Dancer', 'Photographer', 'Architect', 'Pilot', 'Designer', 'Journalist', 'Veterinarian']
    carte = ' '.join([str(random.randint(1000, 9999)) for _ in range(4)])
    cvc = random.randint(100, 999)
    annee = str(random.randint(datetime.now().year, datetime.now().year + 3))[-2:]
    mois = random.randint(1, 12)
    
    i = random.randint(0, len(noms) - 1)
    
    if mois < 10:
        date = f"0{mois}/{annee}"
    else:
        date = f"{mois}/{annee}"
        
    return jsonify({'name': noms[i], 'email': emails[i], 'tel': tel[i], 'localisation': pays[i], 'job': random.choice(job), 'card': carte, 'cvc': cvc, 'expiration': date})

# Génération de QR code
def generate_qrcode(lang):
    url = request.args.get('url', '')
    if not url:
        if lang == 'en':
            return jsonify({'error': 'Please provide a valid argument (?url={URL})'})
        elif lang == 'fr':
            return jsonify({'erreur': 'Veuillez fournir un argument valide (?url={URL})'})
        else:
            return jsonify({'erreur': 'Veuillez fournir un argument valide (?url={URL})'})

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=18, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')

# Génération de token
def generate_token(lang):
    argument = request.args.get('len', '')
    if not argument.isdigit():
        argument = '24'
    elif int(argument) < 12:
        argument = '12'
    elif int(argument) > 4096:
        argument = '4096'
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int(argument)))
    
    return jsonify({'key': token})

# Génération de nom d'utilisateur
def generate_username(lang):
    adj = ['Happy', 'Silly', 'Clever', 'Creative', 'Brave', 'Gentle', 'Kind', 'Funny', 'Wise', 'Charming', 'Sincere', 'Resourceful', 'Patient', 'Energetic', 'Adventurous', 'Ambitious', 'Courageous', 'Courteous', 'Determined']
    ani = ['Cat', 'Dog', 'Tiger', 'Elephant', 'Monkey', 'Penguin', 'Dolphin', 'Lion', 'Bear', 'Fox', 'Owl', 'Giraffe', 'Zebra', 'Koala', 'Rabbit', 'Squirrel', 'Panda', 'Horse', 'Wolf', 'Eagle']
    job = ['Writer', 'Artist', 'Musician', 'Explorer', 'Scientist', 'Engineer', 'Athlete', 'Chef', 'Doctor', 'Teacher', 'Lawyer', 'Entrepreneur', 'Actor', 'Dancer', 'Photographer', 'Architect', 'Pilot', 'Designer', 'Journalist', 'Veterinarian']
    
    choix = random.choice(['adj_num', 'ani_num',  'pro_num',  'adj_ani',  'adj_ani_num', 'adj_pro', 'pro_ani', 'pro_ani_num'])
    nombre = str(random.randint(0, 99))
    if choix == 'adj_num':
        username = random.choice(adj) + nombre
    elif choix == 'ani_num':
        username = random.choice(ani) + nombre
    elif choix == 'pro_num':
        username = random.choice(job) + nombre
    elif choix == 'adj_ani':
        username = random.choice(adj) + random.choice(ani)
    elif choix == 'adj_ani_num':
        username = random.choice(adj) + random.choice(ani) + nombre
    elif choix == 'adj_pro':
        username = random.choice(adj) + random.choice(job)
    elif choix == 'pro_ani':
        username = random.choice(job) + random.choice(ani)
    elif choix == 'pro_ani_num':
        username = random.choice(job) + random.choice(ani) + nombre
    
    return jsonify({'username': username, 'adjective': adj, 'animal': ani, 'job': job, 'number': nombre})

################################# HOST ###################################

# Host
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

##########################################################################
