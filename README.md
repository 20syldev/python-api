<div align="center">
  <a href="https://api.sylvain.pro"><img src="https://github.com/20syldev/api/blob/main/src/api.png" alt="Logo" width="25%" height="auto"></a>

# API Publique - Sylvain
  [![Badge1](https://img.shields.io/badge/Version%20:-v1.2.0-ee6464?labelColor=23272A)](https://api.sylvain.pro)
  [![Badge2](https://img.shields.io/badge/Statut%20:-En%20ligne-42b85f?labelColor=23272A)](https://api.sylvain.pro)
</div>

---

## À propos de l'API
Voici mon API personnelle, disponible sur le domaine [sylvain.pro](https://api.sylvain.pro). 
Mais vous pouvez aussi l'utiliser, car tous les **endpoints** sont disponibles au public !

## Les caractéristiques
- Hébergé **24h/7j**
- Utilisation simple
- Rapidité et design facile
- Endpoint multiples :
  - Voir la page d'accueil pour les découvrir !

## Récupérer une donnée
Exemple sur `api.sylvain.pro/token`, qui récupère la clé renvoyée.
### Python
```py
import requests

print(requests.get("https://api.sylvain.pro/token").json()["key"])
```

### JavaScript (Node.js)
```
npm install https
```
```js
const https = require('https');

https.get('https://api.sylvain.pro/token', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log(JSON.parse(data).key);
    });
});
```