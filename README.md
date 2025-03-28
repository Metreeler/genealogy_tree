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

