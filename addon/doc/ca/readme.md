#NVDA Remote Access
Versió 1.3

Benvingut al complement d'accés remot de NVDA, que et permetrà connectar-te a un altre equip que executi el lector de pantalla gratuït NVDA. És igual que siguis a l'altra banda de l'habitació o a l'altra banda del món. Connectar-se és simple, i hi ha molt poques ordres per aprendre. Pots connectar-te a l'equip d'una altra persona, o permetre a una persona de confiança que es connecti al teu sistema per realitzar un manteniment rutinari, diagnosticar un problema, o ensenyar-te alguna cosa.

##Abans de començar

Cal tenir instal·lat NVDA en els dos equips, i obtenir el complement NVDA Remote Access.
La instal·lació de NVDA i del complement no varia respecte a d'altres. Si necessites més informació, pots trobar-la a la guia d'usuari de NVDA.

##Iniciar una sessió remota a través d'un servidor extern
###L'equip controlat
1. Obre el menú d'NVDA, eines, remot, connectar.
2. Tria client en el primer grup de botons d'opció.
3. Tria permetre que controlin aquest equip en el segon grup de botons d'opció.
4. Al camp equip o servidor, introdueix el servidor al qual et vas a connectar, per exemple nvdaremote.com.
5. Introdueix una clau en el camp clau, o prem el botó generar clau.
La clau és el que altres faran servir per controlar el teu equip.
La màquina controlada i tots els seus clients han d'utilitzar la mateixa clau.
6. Prem acceptar. Fet això, escoltaràs un xiulet i connectat.

###Controlar un altre equip
1. Obre el menú d'NVDA, eines, remot, connectar.
2. Tria client en el primer grup de botons d'opció.
3. Selecciona controlar un altre equip en el segon grup de botons d'opció.
4. Al camp equip o servidor, introdueix el servidor al qual et vas a connectar, per exemple nvdaremote.com.
5. Introdueix una clau en el camp clau, o prem el botó generar clau.
La màquina controlada i tots els seus clients han d'utilitzar la mateixa clau.
6. Prem acceptar. Fet això, escoltaràs un xiulet i connectat.

##Connexions directes
L'opció servidor en el diàleg connectar permet establir una connexió directa.
Un cop seleccionada, tria la manera en què es comportarà el teu equip durant la connexió.
L'altra persona es connectarà fent servir el contrari.

Un cop seleccionat el mode, pots utilitzar el botó obtenir IP externa per obtenir la teva adreça IP externa i assegurar-te que el port està obert correctament.
Si portcheck detecta que el teu port (per defecte 6837) no està obert, apareixerà una advertència.
Obre el port i torna-ho a provar de nou.
Nota: el procés d'obrir ports està fora del propòsit d'aquest document. Consulta la documentació que acompanya al teu router per a més informació.

Introdueix una clau en el camp clau, o prem generar. L'altra persona necessitarà la teva IP externa juntament amb la clau per connectar. Si has introduït un port diferent al que es fa servir per defecte (6837) al camp port, assegura't de que l'altra persona afegeix el port alternatiu a la direcció de l'equip fent servir el format &lt;ip externa>:&lt;puerto>.

Un cop premis acceptar, estaràs connectat.
Quan l'altra persona es connecti, podràs fer servir NVDA Remote amb normalitat.

##Enviament de pulsacions de teclat
Un cop la sessió està connectada, el controlador pot prémer F11 per enviar pulsacions de teclat.
Quan NVDA digui enviament de tecles activat, les tecles que premis aniran a l'equip remot. Prem F11 de nou per aturar l'enviament de tecles i tornar a l'equip controlador.
Per a més compatibilitat, assegura't que les distribucions de teclat de les dues màquines coincideixen.

##Enviar ctrl + alt + supr
Encara que l'enviament de tecles estigui activat, la combinació ctrl + alt + supr no es pot enviar com la resta.
Si necessites enviar ctrl + alt + supr, i el sistema remot es troba a l'escriptori segur, tria aquesta opció.

##Control remot d'un equip desatès

A vegades pots voler controlar un dels teus propis equips remotament. Això és especialment útil si et trobes viatjant, i vols controlar el pc de casa des del portàtil, o controlar un equip en una habitació de casa teva mentre ets fora amb un altre pc. Amb una preparació una mica avançada això es fa possible.

1. Entra al menú de NVDA, tria eines ia continuació remot. Finalment, prem intro en opcions.
2. Marca la casella que diu "Connectar automàticament al servidor de control en arrencar".
3. Tria si faràs servir un servidor de control remot o crearàs un servidor local.
4. Si crees el teu propi servidor, hauràs d'assegurar-te que el port introduït en el camp port (per defecte 6837) està obert en l'equip controlat i els equips controladors poden connectar-se a ell.
5. Si vols fer servir un servidor de control remot, omple els camps equip o servidor i clau, prem tabulador fins a acceptar, i prem intro. Tingues en compte que l'opció generar clau no es troba disponible en aquesta situació. És millor escriure una clau que es pugui recordar per a que puguis fer-la servir fàcilment des de qualsevol lloc remot.  

Nota: les opcions relacionades amb connectar automàticament en arrencar en el diàleg d'opcions no tenen efecte fins que no es reinicia NVDA.

##Silenciar la veu en l'equip remot
Si no vols sentir la veu de l'ordinador remot, és tan simple com anar al menú de NVDA, eines, remot. Baixa amb fletxa avall fins sentir silenciar veu de l'equip remot, i prem intro.

##Finalitzar una sessió remota

Per finalitzar una sessió remota, fes el següent:

1. En l'equip controlador, prem F11 per deixar d'enviar pulsacions de teclat. Hauries d'escoltar el missatge: "Enviament de tecles desactivat.". Si sents un missatge dient que l'enviament de tecles està activat, prem F11 de nou.

2. Accedeix al menú de NVDA, eines, remot, i prem intro en desconnectar.

##Enviar porta-retalls
L'opció enviar porta-retalls en el menú remot et permet enviar text des del teu portapapers.
Quan estigui activada, qualsevol text al porta-retalls s'enviarà als altres equips.

##Configura NVDA Remote perquè funcioni a l'escriptori segur

Perquè NVDA Remote funcioni a l'escriptori segur, el complement ha d'estar instal·lat al NVDA que s'executa a l'escriptori segur.

1. Al menú de NVDA, selecciona preferències, i a continuació opcions generals.

2. Prem tabulador fins al botó Utilitzar opcions actualment guardades en l'autentificació (logon) i altres pantalles segures (requereix privilegis d'administrador), i prem intro.

3. Respon sí a les advertències sobre copiar la configuració i els complements, i respon a l'advertència del control de comptes d'usuari que hauria d'aparèixer.

4. Quan la configuració s'hagi copiat, prem intro per acceptar la confirmació. Prem tabulador fins a acceptar i prem intro de nou per sortir del diàleg.

Quan NVDA Remote estigui instal·lat a l'escriptori segur, si et controlen en una sessió remota,
l'escriptori segur serà llegit quan s'entri en ell.

##Contribucions
Ens agradaria donar el nostre reconeixement als següents contribuents que, entre d'altres, han ajudat a que el projecte NVDA Remote sigui una realitat.
 
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
