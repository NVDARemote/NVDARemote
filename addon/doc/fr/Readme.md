﻿#NVDA Remote Access
Version 1.2

Bienvenue à NVDA Remote Access, un module qui vous permettra de vous connecter à un ordinateur distant exécutant le lecteur d'écran libre et gratuit NVDA, que vous soyez dans la même pièce ou au bout du monde. La connexion est simple et ne nécessite de mémoriser que quelques commandes. Vous pouvez vous connecter à l'ordinateur d'une autre personne ou autoriser une personne de confiance à se connecter à votre système, afin d'accomplir des tâches de maintenance, diagnostiquer un problème ou encore dispenser une formation.

##Avant De Commencer

Vous aurez besoin d'avoir préalablement installé [NVDA](http://www.nvda-fr.org/download.php) sur les deux ordinateurs ainsi que le [module complémentaire NVDARemote.](http://nvdaremote.com/download/) Les deux installations respectent une procédure standard. Si vous avez besoin de plus d'informations à ce sujet, vous pouvez consulter le [guide de l'utilisateur de NVDA.](http://www.nvda-fr.org/documentation.php)

##Démarrage d'une session distante à travers un serveur Relai
###Sur l'ordinateur contrôlé
1. Ouvrez le menu NVDA, Outils, Accès distant, Se Connecter.
2. Choisissez "Client" pour le premier bouton radio.
3. Sélectionnez "Permettre le contrôle de cet ordinateur" dans le second ensemble de boutons radio.
4. Dans le champ "Addresse du serveur", saisissez l'IP ou le nom d'hôte du serveur relai auquel vous vous connectez, par exemple NVDARemote.com.
5. Entrez une clé dans le champ "Clé" ou appuyez sur le bouton "Générer la Clé" pour en générer une. 
Cette clé est celle que les autres devront saisir pour contrôler l'ordinateur. 
L'ordinateur contrôlé ainsi que tous ses clients doivent utiliser la même clé.
6. Appuyez sur OK. Une fois fait, vous entendrez un signal sonore ainsi que le message "connecté au serveur de contrôle".

###Sur l'ordinateur contrôleur
1. Ouvrez le menu NVDA, Outils, Accès distant, Se Connecter.
2. Choisissez "Client" pour le premier bouton radio.
3. Sélectionnez "Contrôler un autre ordinateur" dans le second ensemble de boutons radio.
4. Dans le champ "Adresse du serveur", saisissez l'IP ou le nom d'hôte du serveur relai auquel vous vous connectez, par exemple NVDARemote.com.
5. Entrez une clé dans le champ "Clé" ou appuyez sur le bouton "Générer la Clé" pour en générer une. 
L'ordinateur contrôlé ainsi que tous ses clients doivent utiliser la même clé.
6. Appuyez sur OK. Une fois fait, vous entendrez un signal sonore ainsi que le message "connecté!".

##Connexion directe
L'option "Serveur" du dialogue de connexion vous permet d'établir une connexion directe. 
Lorsque cette option est sélectionnée, choisissez ensuite le mode dans lequel la connexion devra s'établir, contrôleur ou contrôlée.
L'autre personne se connectera à votre ordinateur en sélectionnant le mode opposé.

Une fois ceci fait, vous pouvez utiliser le bouton "Obtenir l'adresse IP publique" pour obtenir votre adresse IP et vous assurer que le port de connexion est correctement redirigé. 
Si la procédure de vérification détecte que le port 6837 n'est pas accessible, vous recevrez un message d'avertissement. Redirigez le port et réessayez. 
Note : le processus de redirection de ports ne s'inscrivant pas dans l'objectif de ce document, veuillez consulter la documentation de votre routeur.

Saisissez une clé dans le champ "Clé" ou appuyez sur "Générer la Clé". L'autre personne aura besoin de votre adresse IP ainsi que de cette même clé pour se connecter.

Quand vous aurez validé sur OK, vous serez connecté. 
Une fois l'autre personne connectée, vous pourrez utiliser NVDARemote normalement.

##Envoi de commandes
Dès que la session a démarré, l'utilisateur de l'ordinateur contrôleur peut appuyer sur la touche F11 afin de commencer à envoyer des commandes. 
A partir du moment où NVDA dit: "Transmission des touches activée", toutes les commandes exécutées par le contrôleur seront effectives sur l'ordinateur distant. Appuyez à nouveau sur F11 pour interrompre l'envoi de commandes et revenir à l'ordinateur contrôleur.
Pour une compatibilité optimale, assurez-vous que les configurations clavier des deux ordinateurs correspondent entre elles.

##Envoyer Ctrl+Alt+Suppr
Pendant l'envoi de commandes, il n'est pas possible d'envoyer la combinaison de touches Ctrl+Alt+Suppr de manière classique. 
Si vous devez envoyer cette commande mais que le système distant est en mode bureau sécurisé, utilisez alors la commande de menu "Envoyer Ctrl+Alt+Suppr".

##Contrôler un ordinateur distant sans intervention utilisateur
Parfois, vous aurez peut-être besoin de vous connecter à l'un de vos ordinateurs personnels à distance. Ceci peut s'avérer particulièrement utile lorsque vous êtes en voyage et que vous souhaitez contrôler l'ordinateur de la maison depuis votre ordinateur portable, ou encore qu'il vous soit nécessaire d'intervenir sur un ordinateur se trouvant dans une pièce de votre domicile alors que vous vous situez à l'extérieur de celle-ci avec un autre ordinateur. Il suffit pour cela d'une petite opération préalable pour rendre le processus simple et confortable.

1. Rendez-vous dans le menu NVDA et choisissez Outils puis Accès distant. Validez ensuite sur Options.
2. cochez la case intitulée "Se connecter automatiquement au serveur de contrôle au démarrage".
3. Remplissez les champs Adresse du serveur et Clé, faites Tabulation jusqu'à OK et validez avec Entrée. 
4. Veuillez noter que le bouton "Générer la clé" n'est pas disponible dans cette situation. Il est préférable que vous définissiez une clé dont vous pourrez vous rappeler facilement et que vous pourrez utiliser où que vous soyez.

##Couper le son de la synthèse vocale de l'ordinateur distant
Si vous ne souhaitez pas entendre la synthèse vocale de l'ordinateur distant, rendez-vous simplement dans le menu NVDA, outils puis Accès distant, puis descendez avec les flèches jusqu'à "Couper le son de la synthèse vocale distante" et validez avec Entrée.


##Terminer une session distante

Pour mettre fin à une session distante, procédez comme suit :

1. Sur l'ordinateur contrôleur, appuyez sur F11 pour arrêter l'envoi de commandes. Vous devriez entendre le message "Transmission des touches désactivée". Si vous entendez "Transmission des touches activée", appuyez sur F11 une nouvelle fois.

2. Rendez-vous dans le menu NVDA, Outils puis Accès distant et faites entrée sur l'option "Se déconnecter".

##Envoyer le presse-Papiers
L'option "Envoyer le presse-papiers" présente dans le menu Accès Distant vous permet d'envoyer du texte depuis votre presse-papiers. 
Une fois activée, tout texte présent dans votre presse-papiers sera envoyé à l'ordinateur distant.

##Configurer NVDARemote pour fonctionner sur le bureau sécurisé

Afin que NVDARemote marche en mode bureau sécurisé, il faut que le module complémentaire soit installé sur la version de NVDA s'exécutant sur le bureau sécurisé.

1. Depuis le menu de NVDA, sélectionnez Préférences, puis Paramètres généraux.

2. Faites Tabulation jusqu'au bouton intitulé "Utiliser les paramètres NVDA actuellement sauvegardés pour l'écran de connexion à Windows (nécessite des privilèges administrateur)" et appuyez sur Entrée.

3. Répondez Oui aux questions relatives à la copie de vos paramètres et modules complémentaires et répondez Oui à l'invite du contrôle de compte d'utilisateur qui pourrait apparaître.

4. Une fois les paramètres copiés, appuyez sur Entrée pour valider le bouton OK et fermer cette boîte de dialogue.

5. Faites Tabulation jusqu'à OK et validez pour fermer les préférences de NVDA.

Une fois NVDARemote installé sur le bureau sécurisé et que votre ordinateur fait l'objet d'un contrôle distant, le bureau sécurisé sera vocalisé lorsque le focus basculera sur ce dernier.

##Contributions
Nous aimerions remercier les contributeurs suivants qui, parmi tant d'autres, ont aidé à ce que le projet NVDARemote devienne une réalité.

* Hai Nguyen Ly
* Chris Westbrook
* Thomas Huebner
* John F Crosotn III
* Darrell Shandrow
* D Williams
* Matthew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews
