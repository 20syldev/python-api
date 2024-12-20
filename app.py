import base64, firebase_admin, io, json, math, os, qrcode, random, requests, string, uuid
from datetime import datetime
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, render_template, request, send_file, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont

############################## PRINCIPAL ##############################

# Créer l'app Flask, charger le dotenv & activer CORS
app = Flask(__name__, template_folder='src', static_folder='src')
load_dotenv()
CORS(app)

# Variables Firebase
firebase_init = False
firebase_app = None

# Page d'accueil
@app.route('/')
def index(): return app.response_class(response=json.dumps({ 'en': 'https://api.sylvain.pro/en', 'fr': 'https://api.sylvain.pro/fr' }, indent=2), status=200, mimetype='application/json')

# Route pour les langues
@app.route('/<lang>/', methods=['GET'])
def lang(lang=None):
    if lang == 'en':
        return render_template('en/index.html')
    elif lang == 'fr':
        return render_template('fr/index.html')
    return app.response_class(response=json.dumps({ 'error': 'Language not found, please specify an existing language in the URL (/fr or /en)' }, indent=2), status=200, mimetype='application/json')

# Redirection du fichier
@app.route('/<path:filename>/', methods=['GET'])
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

################# REDIRECTION VERS ENDPOINTS & LANGUE ###################

# Détection de la langue et de l'endpoint demandé
@app.route('/<lang>/<endpoint>/', methods=['GET'])
def redirect_page(lang, endpoint):
    if lang not in ['fr', 'en']:
        return app.response_class(response=json.dumps({ 'error': 'Please specify language in the URL (/fr or /en)' }, indent=2), status=200, mimetype='application/json')
    if endpoint == 'algorithms':
        return algorithms(lang)
    elif endpoint == 'captcha':
        return captcha(lang)
    elif endpoint == 'color':
        return color(lang)
    elif endpoint == 'domain':
        return domain(lang)
    elif endpoint == 'infos':
        return infos(lang)
    elif endpoint == 'lorem':
        return lorem(lang)
    elif endpoint == 'personal':
        return personal(lang)
    elif endpoint == 'qrcode':
        return qr_code(lang)
    elif endpoint == 'token':
        return token(lang)
    elif endpoint == 'versions':
        return versions(lang)
    elif endpoint == 'username':
        return username(lang)
    else:
        if lang == 'en': return app.response_class(response=json.dumps({ 'error': 'Endpoint not found' }, indent=2), status=200, mimetype='application/json')
        elif lang == 'fr': return app.response_class(response=json.dumps({ 'erreur': 'Endpoint introuvable' }, indent=2), status=200, mimetype='application/json')

####################### FONCTION FIREBASE #########################

def get_data(collection, document):
    global firebase_init, firebase_app
    if not firebase_init:
        firebaseConfig = credentials.Certificate({
            'type': 'service_account',
            'project_id': os.getenv('FIREBASE_PROJECT_ID'),
            'private_key_id': os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            'private_key': os.getenv('FIREBASE_PRIVATE_KEY'),
            'client_email': os.getenv('FIREBASE_CLIENT_EMAIL'),
            'client_id': os.getenv('FIREBASE_CLIENT_ID'),
            'auth_uri': os.getenv('FIREBASE_AUTH_URI'),
            'token_uri': os.getenv('FIREBASE_TOKEN_URI')
        })
        firebase_app = initialize_app(firebaseConfig)
        firebase_init = True
    return firestore.client().collection(collection).document(document).get().to_dict()

####################### FONCTIONS DES ENDPOINTS #########################

# Fonctions utiles
def algorithms(lang):
    tool = request.args.get('tool', '')
    value = request.args.get('value', '')

    if tool not in ['anagram', 'factorial', 'fibonacci', 'palindrome', 'reverse']:
        if lang == 'en':
            return app.response_class(response=json.dumps({ 'error': 'Please provide a valid algorithm (?tool={Algorithm})' }, indent=2), status=200, mimetype='application/json')
        elif lang == 'fr':
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir un algorithme valide (?tool={Algorithme})' }, indent=2), status=200, mimetype='application/json')
        else:
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir un algorithme valide (?tool={Algorithme})' }, indent=2), status=200, mimetype='application/json')

    elif not value:
        if lang == 'en':
            return app.response_class(response=json.dumps({ 'error': 'Please provide a valid value (&value={Value})' }, indent=2), status=200, mimetype='application/json')
        elif lang == 'fr':
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Valeur})' }, indent=2), status=200, mimetype='application/json')
        else:
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Valeur})' }, indent=2), status=200, mimetype='application/json')

    if tool == 'anagram':
        value2 = request.args.get('value2', '')

        if not value2:
            if lang == 'en':
                return app.response_class(response=json.dumps({ 'error': 'Please provide a second valid input (&value2={Input})' }, indent=2), status=200, mimetype='application/json')
            elif lang == 'fr':
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une seconde valeur valide (&value2={Valeur})' }, indent=2), status=200, mimetype='application/json')
            else:
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une seconde valeur valide (&value2={Valeur})' }, indent=2), status=200, mimetype='application/json')

        return app.response_class(response=json.dumps({ 'answer': sorted(value) == sorted(value2) }, indent=2), status=200, mimetype='application/json')
    
    elif tool == 'factorial':
        value = int(value)
        try:
            if value >= 1500:
                value = 1500
            answer = math.factorial(value)

        except:
            if lang == 'en':
                return app.response_class(response=json.dumps({ 'error': 'Please provide a valid input (&value={Number})' }, indent=2), status=200, mimetype='application/json')
            elif lang == 'fr':
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Nombre})' }, indent=2), status=200, mimetype='application/json')
            else:
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Nombre})' }, indent=2), status=200, mimetype='application/json')

        return app.response_class(response=json.dumps({ 'answer': answer}, indent=2), status=200, mimetype='application/json')

    elif tool == 'fibonacci':
        fib = [0, 1]
        value = int(value)
        try:
            if value >= 10000:
                value = 10000
            for i in range(2, value):
                fib.append(fib[-1] + fib[-2])

        except:
            if lang == 'en':
                return app.response_class(response=json.dumps({ 'error': 'Please provide a valid input (&value={Number})' }, indent=2), status=200, mimetype='application/json')
            elif lang == 'fr':
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Nombre})' }, indent=2), status=200, mimetype='application/json')
            else:
                return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une valeur valide (&value={Nombre})' }, indent=2), status=200, mimetype='application/json')

        return app.response_class(response=json.dumps({ 'answer': fib[:value]}, indent=2), status=200, mimetype='application/json')
    
    elif tool == 'palindrome':
        return app.response_class(response=json.dumps({ 'answer': value == value[::-1]}, indent=2), status=200, mimetype='application/json')
    
    elif tool == 'reverse':
        return app.response_class(response=json.dumps({ 'answer': value[::-1]}, indent=2), status=200, mimetype='application/json')

# Génération de captcha
def captcha(lang):
    captcha = request.args.get('text', '')

    if not captcha:
        if lang == 'en':
            return app.response_class(response=json.dumps({ 'error': 'Please provide a valid argument (?text={Text})' }, indent=2), status=200, mimetype='application/json')
        elif lang == 'fr':
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir un argument valide (?text={Texte})' }, indent=2), status=200, mimetype='application/json')
        else:
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir un argument valide (?text={Texte})' }, indent=2), status=200, mimetype='application/json')

    size = 60
    font = ImageFont.truetype("src/Captcha-Font.otf", size)
    witdh = len(captcha) * size
    image = Image.new('RGB', (witdh, 100), color=(255, 255, 255))
    
    d = ImageDraw.Draw(image)
    x = (image.width + 20 - witdh) / 2
    y = (image.height - size) / 2
    
    char_width = size * 1
    
    for char in captcha:
        color = (random.randint(0, 192), random.randint(0, 192), random.randint(0, 192))
        d.text((x, y), char, fill=color, font=font)
        x += char_width

    for _ in range(100):
        d.point((random.randint(0, 400), random.randint(0, 100)), fill=(0, 0, 0))

    img_buffer = io.BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')

# Génération de couleurs
def color(lang):
    r, g, b = [random.randint(0, 255) for _ in range(3)]
    return app.response_class(response=json.dumps({ 'hex': '#{0:02x}{1:02x}{2:02x}'.format(r, g, b), 'rgb': f'rgb({r}, {g}, {b})' }, indent=2), status=200, mimetype='application/json')

# Génération de domaine
def domain(lang):
    noms = ['example', 'site', 'test', 'demo', 'page', 'web']
    extensions = ['.com', '.fr', '.eu', '.dev', '.net', '.org', '.io', '.tech', '.biz', '.info', '.co', '.app']
    
    domain = random.choice(noms) + random.choice(extensions)
    return app.response_class(response=json.dumps({ 'domain': domain, 'random_name': random.choice(noms), 'random_tld': random.choice(extensions) }, indent=2), status=200, mimetype='application/json')

# Affichage d'informations sur l'API
def infos(lang):
    info = get_data('api', 'infos')
    endpoints = info.get('endpoints', '')
    return app.response_class(response=json.dumps({ 'endpoints': endpoints}, indent=2), status=200, mimetype='application/json')

# Génération de texte Lorem
def lorem(lang):
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras viverra, dui non cursus accumsan, lectus leo euismod augue, a gravida odio sapien quis elit. Vivamus vehicula nisi vitae lacinia elementum. Ut id velit quis velit feugiat elementum. Vivamus vulputate, nisl ac placerat laoreet, ex nisl suscipit ligula, volutpat dapibus elit neque non orci. Pellentesque quis lacus efficitur, egestas nisl vitae, tincidunt justo. In gravida enim et egestas dapibus. Cras tempus libero ut sapien efficitur egestas. Sed commodo volutpat suscipit. Proin vulputate ante nec lacus consequat ullamcorper. Pellentesque facilisis massa quam, in auctor neque imperdiet sit amet. Maecenas sagittis aliquam eleifend. Sed dapibus, urna ut molestie fringilla, orci lorem aliquet lacus, nec interdum tortor lacus eu mauris. Curabitur vitae faucibus mi. Duis eget tempus justo. Curabitur placerat nisl eu sem dictum, eget placerat lectus vehicula. Fusce sit amet ipsum in libero aliquam mattis sit amet quis mi. Suspendisse sollicitudin consequat diam sit amet luctus. Nunc dapibus dolor vel sagittis faucibus. Donec et lorem ante. Praesent bibendum ultricies dui, at posuere leo vulputate eu. Integer gravida ex vitae erat accumsan egestas. Sed id tellus nec felis volutpat congue. Ut eget suscipit tellus, et tempus massa. Aliquam id semper diam, feugiat congue arcu. Nunc pulvinar et nisi eu elementum. Morbi condimentum sapien at sapien gravida, vitae lacinia orci condimentum. Suspendisse scelerisque urna quis euismod mattis. Pellentesque pulvinar pretium massa at varius. In pulvinar, velit ac mattis scelerisque, mauris nibh aliquam ipsum, sed aliquam tellus erat quis lectus. Nunc semper enim a felis ultrices convallis. Etiam velit magna, porta nec dui sit amet, venenatis gravida ipsum. In vitae magna et orci consequat cursus id vitae ex. Nulla pharetra massa vel felis malesuada porttitor. Etiam convallis tellus a sodales ullamcorper. Sed hendrerit sollicitudin erat, sit amet sodales magna dignissim nec. Curabitur ut enim eget dolor tincidunt bibendum. Fusce fermentum quam et finibus laoreet. Aliquam vel sem vitae turpis sollicitudin tempus. Nam rutrum risus ultricies quam tempor mattis. Pellentesque at dui felis. Cras maximus malesuada metus vitae iaculis. Aliquam erat volutpat. Nunc facilisis pretium tellus, ut tincidunt lectus eleifend a. In vel lacinia est. Integer tristique non metus pulvinar vestibulum. Fusce sit amet velit vel libero viverra semper et vel sem. In justo libero, semper a mi varius, aliquet commodo eros. Pellentesque porttitor tellus sit amet est varius luctus. Mauris placerat porta eros. Aliquam et mi id justo auctor semper ac vitae tellus. Donec auctor porttitor enim, at ornare ante ornare vel. Pellentesque sagittis ligula vitae libero vestibulum eleifend. Duis sit amet ullamcorper leo. Integer id dui velit. Quisque posuere nulla ligula, at consectetur metus finibus quis. Vestibulum sit amet neque iaculis, malesuada ipsum eget, feugiat nibh. Donec id ultricies enim, tincidunt volutpat arcu. Etiam vitae metus in mauris semper tempus. In dapibus neque at lorem pulvinar congue. Etiam ultrices tristique leo id interdum'
    argument = request.args.get('len', '')
    if not argument.isdigit() or int(argument) < 1:
        argument = 1

    sentences = text.split('. ')
    output = '. '.join(sentences[:int(argument)])
    return app.response_class(response=json.dumps({ 'text': output + '.' }, indent=2), status=200, mimetype='application/json')

# Génération d'informations personnelles
def personal(lang):
    carte = ' '.join([str(random.randint(1000, 9999)) for _ in range(4)])
    cvc = random.randint(100, 999)
    emails = ['john@example.com', 'jane@example.com', 'michael@example.com', 'emily@example.com', 'alexis@example.com']
    job = ['Writer', 'Artist', 'Musician', 'Explorer', 'Scientist', 'Engineer', 'Athlete', 'Doctor', 'Teacher', 'Lawyer', 'Entrepreneur', 'Actor', 'Dancer', 'Photographer', 'Architect', 'Pilot', 'Designer', 'Journalist', 'Veterinarian']
    noms = ['John Doe', 'Jane Martin', 'Michael Johnson', 'Emily Davis', 'Alexis Barbos']
    pays = ['US', 'FR', 'UK', 'ES', 'DE']
    tel = ['123-456-7890', '06 78 90 12 34', '7911 123456', '678 901 234', '163 555 1584']

    annee = str(random.randint(datetime.now().year, datetime.now().year + 3))[-2:]
    mois = random.randint(1, 12)
    
    i = random.randint(0, len(noms) - 1)
    
    if mois < 10:
        date = f'0{mois}/{annee}'
    else:
        date = f'{mois}/{annee}'
        
    return app.response_class(response=json.dumps({ 'card': carte, 'cvc': cvc, 'email': emails[i], 'expiration': date, 'job': random.choice(job), 'localisation': pays[i], 'name': noms[i], 'tel': tel[i]}, indent=2), status=200, mimetype='application/json')

# Génération de QR code
def qr_code(lang):
    url = request.args.get('url', '')
    if not url:
        if lang == 'en':
            return app.response_class(response=json.dumps({ 'error': 'Please provide a valid url (?url={URL})' }, indent=2), status=200, mimetype='application/json')
        elif lang == 'fr':
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une URL valide (?url={URL})' }, indent=2), status=200, mimetype='application/json')
        else:
            return app.response_class(response=json.dumps({ 'erreur': 'Veuillez fournir une URL valide (?url={URL})' }, indent=2), status=200, mimetype='application/json')

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=18, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')

# Génération de token
def token(lang):
    longueur = request.args.get('len', '')
    tokenType = request.args.get('type', '')

    if not longueur.isdigit():
        longueur = 24
    else:
        longueur = int(longueur)
        if longueur < 12:
            longueur = 12
        elif longueur > 4096:
            longueur = 4096

    if tokenType == 'alpha':
        token = ''.join(random.choice(string.ascii_letters) for _ in range(longueur))
    elif tokenType == 'alphanum':
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(longueur))
    elif tokenType == 'base64':
        random_bytes = bytearray(random.getrandbits(8) for _ in range(longueur))
        token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        token = token[:longueur]
    elif tokenType == 'hex':
        token_bytes = bytearray(random.randint(0, 255) for _ in range(longueur))
        token = token_bytes.hex()
        token = token[:longueur]
    elif tokenType == 'num':
        token = ''.join(random.choice(string.digits) for _ in range(longueur))
    elif tokenType == 'punct':
        token = ''.join(random.choice(string.punctuation) for _ in range(longueur))
    elif tokenType == 'urlsafe':
        token = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(longueur))
    elif tokenType == 'uuid':
        token = str(uuid.uuid4())
    else:
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(longueur))
    
    return app.response_class(response=json.dumps({ 'key': token}, indent=2), status=200, mimetype='application/json')

# Affichage des versions de mes projets
def versions(lang):
    version = get_data('api', 'projets')
    api = version.get('api', '')
    coop_api = version.get('coop_api', '')
    coop_status = version.get('coop_status', '')
    database = version.get('database', '')
    doc_coopbot = version.get('doc_coopbot', '')
    gemsync = version.get('gemsync', '')
    gitsite = version.get('gitsite', '')
    nitrogen = version.get('nitrogen', '')
    portfolio = version.get('portfolio', '')
    wrkit = version.get('wrkit', '')
    zpki = version.get('zpki', '')

    return app.response_class(response=json.dumps({ 'api': api, 'coop_api': coop_api, 'coop_status': coop_status, 'database': database, 'doc_coopbot': doc_coopbot, 'gemsync': gemsync, 'gitsite': gitsite, 'nitrogen': nitrogen, 'portfolio': portfolio, 'wrkit': wrkit, 'zpki': zpki }, indent=2), status=200, mimetype='application/json')

# Génération de nom d'utilisateur
def username(lang):
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
    
    return app.response_class(response=json.dumps({ 'adjective': adj, 'animal': ani, 'job': job, 'number': nombre, 'username': username }, indent=2), status=200, mimetype='application/json')

################################# HOST ###################################

# Host
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

##########################################################################
