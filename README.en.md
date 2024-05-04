<div align="center">
  <a href="https://api.sylvain.pro/en"><img src="https://github.com/20syldev/api/blob/main/src/api.png" alt="Logo" width="25%" height="auto"></a>

# Public API - Sylvain
  [![Version](https://img.shields.io/badge/Version%20:-v1.3.6-ee6464?labelColor=23272A)](https://github.com/20syldev/api/releases/latest)
  [![Status](https://img.shields.io/badge/Status%20:-En%20ligne-42b85f?labelColor=23272A)](https://api.sylvain.pro/en)
  [![Lang](https://img.shields.io/badge/Lang%20:-EN-3857ab?labelColor=23272A)](https://github.com/20syldev/api#readme)
</div>

---

[![Change](https://img.shields.io/badge/Langue%20:-FR-3857ab?labelColor=23272A)](https://github.com/20syldev/api#readme)
> *Cliquez [ici](https://github.com/20syldev/api#readme) pour voir la version française, ou cliquez sur le bouton ci-dessus.*

## About the API
This is my personal API, available on the [sylvain.pro](https://api.sylvain.pro/en) domain, in French and English. 
You can use it **without limitations**, as all **endpoints** are public!
> *The API may take a few seconds to load, but once it's done, everything works very quickly and requests are executed instantly.*

## Features
- Hosted **24h/7d**
- Easy to use
- Available in French
- Multiple endpoints :
  - See the [home page](https://api.sylvain.pro/en) to discover them!

## Getting a key
Example on **[api.sylvain.pro/en/token](https://api.sylvain.pro/en/token)**, which retrieves the returned key.
### Python
```py
import requests

print(requests.get("https://api.sylvain.pro/en/token").json()["key"])
```

### JavaScript (Node.js)
```
npm install https
```
```js
const https = require('https');

https.get('https://api.sylvain.pro/en/token', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log(JSON.parse(data).key);
    });
});
```
