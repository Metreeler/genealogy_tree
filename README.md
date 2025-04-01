# Back

In a ubuntu terminal :
```sh
cd back/
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
If on Windows (on Visual Studio Code) : 
```sh
cd back/
python -m venv .venv
.venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

To build the back :
```sh
fastapi dev main.py --port 8000
```

# Front
```sh
npm install
ng serve
```


# Retrouver un descendant
Les documents ne peuvent que être recupérées après 100 ans.
Il faut commencer par trouver la date de naissance 
