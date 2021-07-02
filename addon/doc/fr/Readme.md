# NVDA Remote Access
Version 2.3

Bienvenue à NVDA Remote Access, une extension qui vous permettra de vous connecter à un ordinateur distant exécutant le lecteur d'écran libre et gratuit NVDA, que vous soyez dans la même pièce ou au bout du monde. La connexion est simple et ne nécessite de mémoriser que quelques commandes. Vous pouvez vous connecter à l'ordinateur d'une autre personne ou autoriser une personne de confiance à se connecter à votre système, afin d'accomplir des tâches de maintenance, diagnostiquer un problème ou encore dispenser une formation.

## Avant De Commencer

Vous aurez besoin d'avoir préalablement installé [NVDA](http://www.nvda-fr.org/download.php) sur les deux ordinateurs ainsi que [l'extension NVDARemote.](http://nvdaremote.com/download/) Les deux installations respectent une procédure standard. Si vous avez besoin de plus d'informations à ce sujet, vous pouvez consulter le [guide de l'utilisateur de NVDA.](http://www.nvda-fr.org/documentation.php)
L'installation de NVDA comme celle de NVDA Remote Access est standard, consultez le guide de l'utilisateur de NVDA pour plus d'information.

## Mise à jour

Lors de la mise à jour de l'extension, si vous avez installé l'accès distant NVDA dans le bureau sécurisé (dialogue d'ouverture de session, écrans sécurisés UAC...) il est recommandé de mettre à jour l'extension pour ces écrans.
Pour ce faire, commencez par mettre à jour l'extension. Puis dans le menu NVDA, Préférences, Paramètres généraux, activez le bouton " Utiliser les paramètres NVDA actuellement sauvegardés pour l'écran de connexion et sur les écrans sécurisés (nécessite des privilèges administrateur) ".

## Démarrage d'une session distante à travers un serveur relai
### Sur l'ordinateur à contrôler
1. Ouvrez le menu NVDA, Outils, Accès distant, Se Connecter.
2. Choisissez " Client " dans le premier ensemble de boutons radio.
3. Sélectionnez " Permettre le contrôle de cet ordinateur " dans le second ensemble de boutons radio.
4. Dans le champ " Adresse du serveur ", saisissez l'IP ou l'adresse du serveur relai auquel vous vous connectez, par exemple NVDARemote.com. Au cas où le serveur utilise un port alternatif, vous pouvez saisir l'adresse du serveur sous la forme &lt;adresse&gt;:&lt;port&gt;, comme dans : nvdaremote.com:1234.
5. Entrez une clé dans le champ " Clé " ou appuyez sur le bouton " Générer la Clé ".
Cette clé est celle que les autres utiliseront pour contrôler l'ordinateur.
L'ordinateur contrôlé ainsi que tous ses clients doivent utiliser la même clé.
6. Appuyez sur OK. Une fois ceci fait, vous entendrez un signal sonore ainsi que le message " connecté au serveur de contrôle ".

### Sur l'ordinateur contrôleur
1. Ouvrez le menu NVDA, Outils, Accès distant, Se Connecter.
2. Choisissez " Client " dans le premier ensemble de boutons radio.
3. Sélectionnez " Contrôler un autre ordinateur " dans le second ensemble de boutons radio.
4. Dans le champ " Adresse du serveur ", saisissez l'IP ou l'adresse du serveur relai auquel vous vous connectez, par exemple NVDARemote.com. Au cas où le serveur utilise un port alternatif, vous pouvez saisir l'adresse du serveur sous la forme &lt;adresse&gt;:&lt;port&gt;, comme dans : nvdaremote.com:1234.
5. Entrez une clé dans le champ " Clé " ou appuyez sur le bouton " Générer la Clé ".
L'ordinateur contrôlé ainsi que tous ses clients doivent utiliser la même clé.
6. Appuyez sur OK. Une fois ceci fait, vous entendrez un signal sonore ainsi que le message " connecté ! ".

## Connexion directe
L'option " Serveur " du dialogue Se Connecter vous permet d'établir une connexion directe.
Une fois l'option sélectionnée, choisissez le mode dans lequel votre connexion devra s'établir, contrôleur ou contrôlé.
L'autre personne se connectera à votre ordinateur en sélectionnant le mode opposé.

Quand le mode est sélectionné, vous pouvez utiliser le bouton "Obtenir l'adresse IP publique" pour obtenir votre adresse IP et vous assurer que le port de connexion (indiqué dans le champ " Port ", est correctement redirigé.
Si la procédure de vérification détecte que le port spécifié (6837 par défaut) n'est pas accessible, un avertissement s'affiche.
Redirigez le port et réessayez. 
Remarque : le processus de redirection de ports ne s'inscrivant pas dans l'objectif de ce document, veuillez consulter la documentation de votre routeur pour plus de détails.

Saisissez une clé dans le champ "Clé" ou appuyez sur " Générer la Clé ". L'autre personne aura besoin de votre adresse IP ainsi que de cette même clé pour se connecter.

Sitôt le bouton OK activé, vous serez connecté.
Quand l'autre partie est connectée, vous pourrez utiliser NVDARemote normalement.

## Contrôler l'ordinateur distant

Dès que la session est ouverte, l'utilisateur de l'ordinateur contrôleur peut appuyer sur F11 pour commencer à contrôler l'ordinateur distant, par ex. : en envoyant des touches clavier ou de la saisie Braille.
Lorsque NVDA dit : " Transmission des touches activée ", toutes les touches que vous actionnerez sur le clavier ou sur le terminal Braille iront vers l'ordinateur distant. De plus, si l'ordinateur contrôleur est doté d'un terminal Braille, les informations de l'ordinateur contrôlées y seront affichées. Appuyez à nouveau sur F11 pour interrompre l'envoi de commandes et revenir à l'ordinateur contrôleur.
Pour une compatibilité optimale, assurez-vous que les configurations clavier des deux ordinateurs correspondent.

## Partager votre session

Pour partager un lien permettant à quelqu'un d'autre de rejoindre facilement votre session d'accès distant NVDA, choisissez le menu "copier le lien" dans le sous-menu Accès distant.
Si vous êtes connecté en tant qu'ordinateur contrôleur, ce lien permet à quelqu'un d'autre de se connecter et être contrôlé.
Si, en revanche, vous avez configuré votre ordinateur pour être contrôlé, les personnes avec qui vous avez partagé ce lien pourront contrôler votre machine.
De nombreuses applications permettent aux utilisateurs d'activer ce lien automatiquement, mais s'il ne s'exécute pas au sein d'une application précise, le lien peut être copié dans le presse-papiers et utilisé dans la commande Exécuter.


## Envoyer Ctrl+Alt+Suppr
Pendant l'envoi de commandes, il n'est pas possible d'envoyer la combinaison de touches Ctrl+Alt+Suppr de façon normale.
Si vous devez envoyer cette commande mais que le système distant est en mode bureau sécurisé, utilisez alors la commande de menu "Envoyer Ctrl+Alt+Suppr".

## Contrôler un ordinateur distant sans assistance

Parfois, vous aurez peut-être besoin de vous connecter à l'un de vos ordinateurs personnels à distance. Ceci peut s'avérer particulièrement utile lorsque vous êtes en voyage et que vous souhaitez contrôler l'ordinateur de la maison depuis votre ordinateur portable, ou encore qu'il vous est nécessaire d'intervenir sur un ordinateur se trouvant dans une pièce de votre domicile alors que vous vous situez à l'extérieur de celle-ci avec un autre ordinateur. Il suffit pour cela d'une petite opération avancée pour rendre le processus simple et confortable.

1. Rendez-vous dans le menu NVDA et choisissez Outils puis Accès distant. Validez ensuite sur Options.
2. Cochez la case intitulée " Se connecter automatiquement au serveur de contrôle au démarrage ".
3. Déterminez s'il faut utiliser un serveur relai ou héberger la connexion localement.
4. Sélectionnez " Permettre le contrôle de cet ordinateur " dans le second ensemble de boutons radio.
5. Si vous hébergez le serveur, (mode serveur), assurez-vous que le port spécifié dans le champ " Port " sur l'ordinateur contrôlé (6837 par défaut) est accessible à l'ordinateur contrôleur.
6. Si vous souhaitez utiliser un serveur relai, renseignez les champs Adresse du serveur et Clé, tabulez jusqu'à OK puis appuyez sur Entrée. Le bouton Générer la clé n'est pas disponible dans ce cas. Le mieux est que vous vous conceviez une clé dont vous vous rappellerez facilement de façon à pouvoir l'utiliser d'un endroit distant.

Pour une utilisation avancée, vous pouvez aussi configurer NVDA Remote pour qu'il se connecte automatiquement à un serveur relai local ou distant en mode contrôleur. Si c'est cela que vous voulez, sélectionnez Contrôler un autre ordinateur dans le second ensemble de boutons radio.
Remarque : Les options concernant la connexion automatique au démarrage ne s'appliquent que lorsque NVDA est relancé.


## Couper le son de l'ordinateur distant
Si vous ne souhaitez pas entendre la synthèse vocale ainsi que les sons de NVDA de l'ordinateur distant, rendez-vous simplement dans le menu NVDA, outils puis Accès distant, puis descendez avec les flèches jusqu'à " Couper le son distant " et validez avec Entrée. Veuillez noter que cette option ne désactivera pas le terminal Braille distant pour l'écran à contrôler lorsque l'ordinateur contrôleur envoi des commandes.


## Fermer une session distante

Pour mettre fin à une session distante, procédez comme suit :

1. Sur l'ordinateur contrôleur, appuyez sur F11 pour arrêter l'envoi de commandes. Vous devriez entendre le message " Transmission des touches désactivée ". Si vous entendez " Transmission des touches activée ", appuyez sur F11 une nouvelle fois.

2. Rendez-vous dans le menu NVDA, Outils puis Accès distant et faites entrée sur l'option " Se déconnecter ".

## Envoyer le presse-papiers
L'option " Envoyer le presse-papiers " présente dans le menu Accès Distant vous permet d'envoyer du texte depuis votre presse-papiers.
Une fois activée, tout texte présent dans votre presse-papiers sera envoyé à l'ordinateur distant.

## Configurer NVDARemote pour fonctionner sur le bureau sécurisé

Pour que NVDARemote fonctionne sur un bureau sécurisé, il faut que l'extension soit installée sur la version de NVDA qui s'y exécute.

1. Depuis le menu de NVDA, sélectionnez Préférences, puis Paramètres généraux.

2. Faites Tabulation jusqu'au bouton intitulé " Utiliser les paramètres NVDA actuellement sauvegardés pour l'écran de connexion et sur les écrans sécurisés (nécessite des privilèges administrateur) " et appuyez sur Entrée.

3. Répondez Oui aux questions relatives à la copie de vos paramètres et extensions et répondez Oui à l'invite du contrôle de compte d'utilisateur qui apparaîtrait.
4. Une fois les paramètres copiés, appuyez sur Entrée pour valider le bouton OK. Refaites Tabulation jusqu'à OK. Enfin, refaites Entrée pour fermer ce dialogue.

Une fois NVDARemote installé sur le bureau sécurisé et que votre ordinateur est contrôlé, le bureau sécurisé sera sonorisé et affiché en Braille lorsqu'il est focalisé.

## Contributions
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
* Babbage B.V.
* Leonard de Ruijter
* NV Access
* Reef Turner

## Historique des chamgements

### Version 2.3
* Migré vers Python 3
*  Support   Python 2 abandonné
* Mise à jour pour retrouver l'API modifié dans NVDA 2019.3, y compris :
  - Refacteur de la parole
  - Changements  pour les afficheurs Braille

### Version 2.2

* Support  IPv6
* Support pour les nouvelles versions de NVDA 2018.3 ainsi que des versions plus anciennes
* Support pour des gestes spécifique au modèle de terminal Braille

### Version 2.1

* Correction de la connexion qui n'est pas sauvegarder lorsque cet ordinateur va être contrôlé
* Ajout d'un script pour envoyer le presse-papiers avec Ctrl+Maj+NVDA+C
* La saisie en braille fonctionne maintenant en mode navigation
* Support des gestes spécifique au modèle de terminal Braille
* Les bips générés par NVDA Remote ne bloquera plus NVDA

### Version 2.0

* Support du braille distant
* Support des liens nvdaremote://
* Boîtes de dialogue centrées pour se conformer aux autres dialogues de NVDA
* Correction de portcheck pour pointer sur un domaine contrôlé par l'équipe de NVDARemote,  portcheck.nvdaremote.com
* Support de la connexion automatique à un serveur de contrôle en mode maître
* Correction du rendu dans la documentation
* Protocole mis à jour vers la version 2, qui inclus un champ "origin" dans chaque message distant
* Nettoyage du code, permettant une meilleure maintenance future

## Modification  de NVDA Remote

Vous pouvez cloner ce dépôt pour modifier le NVDA Remote.

### Dépendances tiers

Ceux-ci peuvent être installés avec pip :
- Markdown
- scons
- python-gettext

### Empaquetage de l'extension pour sa distribution :

1. Ouvrez une ligne de commande, changer à la racine de ce dépôt
2. Exécutez la commande **scons**. L'extension créée, s'il n'y a pas d'erreur, sera placée dans le répertoire actuel.

