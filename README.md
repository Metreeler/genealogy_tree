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
## Étape 1:
- Trouver l'acte de naissance de la personne A dans la bonne ville à la bonne date
- Cet acte nous donne normalement :
  - Le nom des parents B et C
  - Leurs âges
  - Leurs villes de naissance
## Étape 2:
- Explorer les tables décennales de la ville où est né la personne A et trouver le mariage des parents B et C dans la période (date de naissance de la mère + 20 ans) - (naissance de personne A)
- Cela donne la date de mariage des parents B et C
## Étape 3:
- Trouver l'acte de mariage des parents B et C
- Cela nous donne normalement:
  - la date et la commune de naissance des parents B et C
  - le nom des parents des parents B et C
## Étape 4:
- Avec la date et la commune de naissance des parents B et C répéter les étapes 1, 2 et 3
