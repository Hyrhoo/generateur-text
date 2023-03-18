# generateur-text

un programme qui génère des textes depuis une base de donner

### To do liste:
- [x] couper la base de données en textes
- [x] couper les textes en mots
- [ ] charger les mots dans le format de donnée prévue
- [ ] généré du texte
    - [ ] calcule coeff pour chaque mots
        - [ ] coeff multi = 1 pour le plus loins et + 1 à chaque fois qu'on ce raproche du mot actuelle diviser par le totale
        - [ ] coeff de selection = coeff multi précédent / coeff multi suivant
    - [ ] séléction aléatoire avec `random.random()` donc 0 <= coeff <= 1