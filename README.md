<div align="center">
  <a href="https://api.sylvain.pro"><img src="https://github.com/20syldev/python-api/blob/main/src/api.png" alt="Logo" width="25%" height="auto"></a>

  # API Python - Sylvain
  [![Version](https://custom-icon-badges.demolab.com/badge/Version%20:-v1.5.0-ee6464?logo=api.sylvain.pro&labelColor=23272A)](https://github.com/20syldev/python-api/releases/latest)
  [![Statut](https://img.shields.io/badge/Statut%20:-Archivé-e39f1b?labelColor=23272A)](https://api.sylvain.pro)
</div>

---

## À propos de l'API
Voici mon API personnelle, disponible sur le domaine [api.sylvain.pro](https://api.sylvain.pro), en français et en anglais. 
Vous pouvez l'utiliser **sans limitations**, car tous les **endpoints** sont publics !

## Les caractéristiques
- Hébergé **24h/7j**
- Utilisation simple
- Disponible en anglais
- Documentation : **[docs.sylvain.pro](https://docs.sylvain.pro)**

## Récupérer une donnée
Exemple sur **api.sylvain.pro/<version>/token**, qui récupère la clé renvoyée.
### Python
```py
import requests

print(requests.get('https://api.sylvain.pro/<version>/token').json()['key'])
```

### JavaScript
```js
fetch('https://api.sylvain.pro/<version>/token')
  .then(response => response.json())
  .then(data => console.log(data.key));
```

### Node.js
```
npm install https
```
```js
const https = require('https');

https.get('https://api.sylvain.pro/<version>/token', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log(JSON.parse(data).key);
    });
});
```
