### Configuration d'un Pipeline CI/CD avec Sécurité Intégrée

### Objectif

**Mettre en place un pipeline CI/CD pour votre projet, en intégrant des outils de sécurité comme SonarQube et Snyk pour analyser le code et vérifier les vulnérabilités des dépendances.**

## Prérequis

- **Un compte GitHub.**
- **Un dépôt GitHub contenant votre projet.**
- **Un compte SonarCloud pour l'analyse du code.**
- **Un compte Snyk pour la gestion des vulnérabilités.**

## Étape 1 : Créer un Dépôt GitHub

Si vous n'avez pas encore de dépôt pour votre projet, suivez ces étapes :

- **Rendez-vous sur GitHub.**
- **Créez un nouveau dépôt en cliquant sur New.**
- **Configurez le nom du dépôt, choisissez une visibilité (privé ou public), puis cliquez sur Create repository.**

## Étape 2 : Configurer GitHub Actions

Créer un répertoire pour les workflows GitHub Actions :

- **Dans votre dépôt GitHub, créez un répertoire .github/workflows/**
- **Ajoutez un fichier .yml dans ce répertoire. Nom de fichier recommandé : ci-cd-pipeline.yml.**

## Étape 3 : Configurer SonarQube et Snyk

# SonarQube: Créez un compte sur SonarCloud :

- **Rendez-vous sur SonarCloud.**
- **Créez un compte et configurez un projet pour votre dépôt GitHub.**
  Obtenez un Token API :

- **Allez dans My Account > Security > Generate Token.**
- **Donnez un nom au token et enregistrez-le.**
  Ajouter le Token à GitHub :

- **Rendez-vous sur GitHub, dans le dépôt de votre projet.**
- **Allez dans Settings > Secrets and variables > Actions.**
- **Cliquez sur New repository secret.**
- **Ajoutez un secret appelé SONAR_TOKEN et collez le token généré depuis SonarCloud.**

# Snyk:Créez un compte sur Snyk :

Rendez-vous sur Snyk.

- **Créez un compte et générez un Token API.**
- **Ajouter le Token à GitHub :**

- **Allez dans Settings > Secrets and variables > Actions.**
- **Cliquez sur New repository secret.**
- **Ajoutez un secret appelé SNYK_TOKEN et insérez le token API de Snyk.**

## Étape 4 : Créer le Workflow GitHub Actions

Voici un exemple de fichier ci-cd-pipeline.yml à ajouter dans le répertoire .github/workflows/ de votre projet

## Une fois votre fichier YAML créé :

À chaque commit ou pull request vers la branche principale (main), GitHub Actions déclenchera automatiquement le pipeline.
Le pipeline exécutera les analyses de sécurité (SonarQube et Snyk), les tests et compilera l'application si nécessaire.
Résultats Attendus

### Rapport SonarQube : Vous pourrez voir les résultats de l'analyse du code et les éventuelles vulnérabilités directement sur SonarCloud.

### Rapport Snyk : Le pipeline vérifiera les dépendances et signalera les vulnérabilités connues.
