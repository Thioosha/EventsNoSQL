# 🎉 Réservation d'Événements — Projet NoSQL (EPT)

Mini-outil de **réservation d’événements** développé avec **Django** & **MongoDB (MongoEngine)** — réalisé dans le cadre du projet NoSQL à l’EPT.

---

## 📸 Aperçu de l’Application

Voici quelques captures d’écran de l’interface utilisateur :

### 🔐 Page de Connexion  

![Page de Connexion](static/img/ApercuSite/login.gif)

### 📝 Page d’Inscription  

![Page d’Inscription](static/img/ApercuSite/inscription.gif)

### 🎉 Formulaire de Création d’Événement  

![Formulaire de Création d’Événement](static/img/ApercuSite/creer_event.gif)

### 📅 Liste des Événements  

![Liste des Événements](static/img/ApercuSite/all_events.gif)

### 🛎️ Rechercher un Événement  

![Rechercher un Événement](static/img/ApercuSite/rechercher.gif)

### 🔍 Détails d’un Événement et Réservation

![Détails d’un Événement](static/img/ApercuSite/event_detail.gif)

### 👤 Dashboard Utilisateur  

![Dashboard Utilisateur](static/img/ApercuSite/Dashboard.gif)

### 🧑‍💼 Dashboard Organisateur  

![Dashboard Organisateur](static/img/ApercuSite/Dashboard_organisateur.gif)

### ⚙️ Paramètres Utilisateur  

![Paramètres Utilisateur](static/img/ApercuSite/settings.gif)

## ⚙️ Prérequis

Avant tout, **assurez-vous d’avoir** :

- Python **3.11+**
- pip
- Git
- **MongoDB Compass**
- **mongosh** (Shell Mongo)
- Un compte MongoDB Atlas (création ici si besoin : <https://www.mongodb.com/cloud/atlas/register> )

---

## Connexion à la base MongoDB Atlas

Ce projet est connecté à une **base de données cloud** partagée via **MongoDB Atlas**.

> ✅ **Étapes obligatoires pour accéder à la base :**

1. **Créer un compte MongoDB Atlas** si ce n’est pas encore fait :
   <https://www.mongodb.com/cloud/atlas/register>

2. **Accepter l’invitation** de la propriétaire du projet à rejoindre le cluster partagé.  

3. Une fois accepté :
   - Se connecter au cluster sur Atlas
   - Copier le lien de la connexion
   - Ouvrir **MongoDB Compass**
   - Coller le lien de la connexion :

---

## Lancer le projet en local

### 1. Cloner le dépôt & installer l’environnement

```bash
git clone https://github.com/Thioosha/EventsNoSQL.git
cd EventsNoSQL
python -m venv venv
venv/Scripts/activate  # sous Windows
pip install -r requirements.txt
