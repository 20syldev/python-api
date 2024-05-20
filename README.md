<div align="center">
  <a href="https://api.sylvain.pro"><img src="https://github.com/20syldev/api/blob/main/src/api.png" alt="Logo" width="25%" height="auto"></a>

# API Publique - Sylvain
  [![Version](https://custom-icon-badges.demolab.com/badge/Version%20:-v1.4.7-ee6464?logo=api.sylvain.pro&labelColor=23272A)](https://github.com/20syldev/api/releases/latest)
  [![Statut](https://img.shields.io/badge/Statut%20:-En%20ligne-42b85f?labelColor=23272A)](https://api.sylvain.pro)
  [![Langue](https://img.shields.io/badge/Langue%20:-FR-3857ab?labelColor=23272A)](https://github.com/20syldev/api#readme)
</div>

---

[![Changer](https://img.shields.io/badge/Lang%20:-EN-3857ab?labelColor=23272A)](https://github.com/20syldev/api/blob/main/README.en.md)
> *Click [here](https://github.com/20syldev/api/blob/main/README.en.md) to view the english version, or click on the button above.*

## À propos de l'API
Voici mon API personnelle, disponible sur le domaine [sylvain.pro](https://api.sylvain.pro), en français et en anglais. 
Vous pouvez l'utiliser **sans limitations**, car tous les **endpoints** sont publics !
> *L'API peut prendre quelques secondes à charger, mais une fois fait, tout fonctionne très rapidement et les appels en console sont instantanés.*

## Les caractéristiques
- Hébergé **24h/7j**
- Utilisation simple
- Disponible en anglais
- Endpoint multiples :
  - Voir la [page d'accueil](https://api.sylvain.pro/fr) pour les découvrir !

## Récupérer une donnée
Exemple sur **[api.sylvain.pro/fr/token](https://api.sylvain.pro/fr/token)**, qui récupère la clé renvoyée.
### Python
```py
import requests

print(requests.get("https://api.sylvain.pro/fr/token").json()["key"])
```

### JavaScript
```js
fetch('https://api.sylvain.pro/fr/token')
  .then(response => response.json())
  .then(data => console.log(data.key));
```

### Node.js
```
npm install https
```
```js
const https = require('https');

https.get('https://api.sylvain.pro/fr/token', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log(JSON.parse(data).key);
    });
});
```
