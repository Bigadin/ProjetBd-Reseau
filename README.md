# JustFlick

JustFlick est une application web développée dans le cadre du programme de Licence 3 en Informatique, qui permet aux utilisateurs de suivre les films qu'ils ont vus ou souhaitent regarder, de découvrir de nouveaux films, de trouver des séances de cinéma à proximité, et bien plus encore.

## Table des matières
1. [Fonctionnalités](#fonctionnalités)
2. [Technologies](#technologies)
3. [Structure des dossiers](#structure-des-dossiers)
4. [Liens Utiles](#liens-utiles)
5. [Équipe](#équipe)

---

## Fonctionnalités
- **Suivi des films** : ajoutez des films à votre liste de visionnage et gérez ceux que vous avez déjà vus ou non.
- **Recherche de films** : trouvez des informations sur les films, y compris leurs options de streaming disponibles.
- **Recommandations aléatoires** : utilisez la fonction "shuffle" pour recevoir des suggestions basées sur vos critères, comme le genre ou l'ambiance.
- **Cinémas à proximité** : consultez les horaires de séance dans les cinémas proches de vous.
- **Évaluations et tendances** : visualisez les films les mieux notés et ceux qui sont populaires en ce moment.

## Technologies
### Frontend
1. **ReactJS** - Framework JavaScript pour la construction d'interfaces utilisateur dynamiques et interactives.
2. **TailwindCSS** - Framework de style CSS pour un design moderne et réactif.
3. **GSAP (GreenSock Animation Platform)** - Bibliothèque d'animations JavaScript pour des effets visuels fluides et engageants.

### Backend
- **FASTAPI**
- **API TMDB** - Utilisation de l'API The Movie Database pour récupérer des données de films.
- **MOVIEGLU API**

### Intégration

- **Axios** : Nous avons utilisé Axios comme bibliothèque cliente HTTP pour interagir efficacement avec les API. Il simplifie le processus d'envoi de requêtes et de gestion des réponses.

- **CORS** : Nous avons configuré le CORS (Cross-Origin Resource Sharing) pour permettre des requêtes API sécurisées entre origines depuis notre frontend React. Le serveur backend a été configuré pour autoriser les requêtes provenant du domaine JustFlick, assurant ainsi une récupération fluide des données à partir d'API tierces.

## Structure des dossiers
```
JustFlick/
│
├── frontend/
│   ├── public/            # contient robot.txt, sitemap.xml
│   ├── src/
│   │   ├── components/    # Composants React pour les différentes parties de l'interface utilisateur
│   │   ├── constants/     # Variables et constantes globales pour l'application
│   │   ├── pages/         # Pages principales de l'application
│   │   └── styles/        # Fichiers de style globaux (complémentaires à TailwindCSS)
│   └── App.jsx            # Point d'entrée de l'application et gestion des routes
│
├── backend/
│   ├── app/               # Contient la logique serveur et les appels API
│   │   ├── core/          # Configuration et services de base de l'application backend
│   │   ├── routes/        # Routes pour les différentes fonctionnalités de l'API backend
│   │   └── main.py        # Point d'entrée du serveur
│
└── README.md
```

## Liens Utiles
- **Site Web** : [JustFlick](https://justflick.netlify.app/)
- **Documentation de l'API Backend** : [JustFlick API Documentation](https://justflick-production.up.railway.app/docs)
- **Base de données** : [BD](https://phpmyadmin.alwaysdata.com/phpmyadmin/index.php)

## Équipe
- **Amina El-Abed**
- **Aktham Serat Achiri**
- **Amine Mouaici**
- **Yanis Hemdane**
