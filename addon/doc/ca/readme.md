# NVDA Remote Access
Versió 2.0

Benvingut al complement d'accés remot de NVDA, que et permetrà connectar-te a un altre equip que executi el lector de pantalla gratuït NVDA. És igual que siguis a l'altra banda de l'habitació o a l'altra banda del món. Connectar-se és simple, i hi ha molt poques ordres per aprendre. Pots connectar-te a l'equip d'una altra persona, o permetre a una persona de confiança que es connecti al teu sistema per realitzar un manteniment rutinari, diagnosticar un problema, o ensenyar-te alguna cosa.

##Abans de començar

Cal tenir instal·lat NVDA en els dos equips, i obtenir el complement NVDA Remote Access.
La instal·lació de NVDA i del complement no varia respecte a d'altres. Si necessites més informació, pots trobar-la a la guia d'usuari de NVDA.

## Actualitzacions

Quan actualitzis el complement, si has instal·lat NVDA Remote a l'escriptori segur, és recomanable que l'actualitzis també allà.
Per fer-ho, primer actualitza el complement normalment. Després, obre el menú de NVDA, preferències, Opcions Generals, i prem el botó etiquetat com "utilitzar opcions actualment guardades a l'autenticacó (logon) i altres pantalles segures (requereix privilegis d'administrador)".

##Iniciar una sessió remota a través d'un servidor extern
###En l'equip controlat
1. Obre el menú d'NVDA, eines, remot, connectar.
2. Tria client en el primer grup de botons d'opció.
3. Tria permetre que controlin aquest equip en el segon grup de botons d'opció.
4. Al camp equip o servidor, introdueix el servidor al qual et vas a connectar, per exemple nvdaremote.com. Quan el servidor faci servir un port diferent al que aquest complement utilitza per defecte, pots introduir la seva direcció en format &lt;equipo&gt;:&lt;puerto&gt;, per exemple nvdaremote.com:1234.
5. Introdueix una clau en el camp clau, o prem el botó generar clau.
La clau és el que altres faran servir per controlar el teu equip.
L'equip controlat i tots els seus clients han d'utilitzar la mateixa clau.
6. Prem acceptar. Fet això, escoltaràs un xiulet i connectat.

###A l'equip des del que es controla
1. Obre el menú d'NVDA, eines, remot, connectar.
2. Tria client en el primer grup de botons d'opció.
3. Selecciona controlar un altre equip en el segon grup de botons d'opció.
4. Al camp equip o servidor, introdueix el servidor al qual et vas a connectar, per exemple nvdaremote.com. Quan el servidor faci servir un port diferent al que aquest complement utilitza per defecte, pots introduir la seva direcció en format &lt;equipo&gt;:&lt;puerto&gt;, per exemple nvdaremote.com:1234.
5. Introdueix una clau en el camp clau, o prem el botó generar clau.
L'equip controlat i tots els seus clients han d'utilitzar la mateixa clau.
6. Prem acceptar. Fet això, escoltaràs un xiulet i connectat.

##Connexions directes
L'opció servidor en el diàleg connectar permet establir una connexió directa.
Un cop seleccionada, tria la manera en què es comportarà el teu equip durant la connexió.
L'altra persona es connectarà fent servir el contrari.

Un cop seleccionat el mode, pots utilitzar el botó obtenir IP externa per obtenir la teva adreça IP externa i assegurar-te que el port està obert correctament.
Si portcheck detecta que el teu port (per defecte 6837) no està obert, apareixerà una advertència.
Obre el port i torna-ho a provar de nou.
Nota: el procés d'obrir ports està fora del propòsit d'aquest document. Consulta la documentació que acompanya al teu router per a més informació.

Introdueix una clau en el camp clau, o prem generar. L'altra persona necessitarà la teva IP externa juntament amb la clau per connectar. Si has introduït un port diferent al que es fa servir per defecte (6837) al camp port, assegura't de que l'altra persona afegeix el port alternatiu a la direcció de l'equip fent servir el format &lt;ip externa&gt;:&lt;puerto&gt;.

Un cop premis acceptar, estaràs connectat.
Quan l'altra persona es connecti, podràs fer servir NVDA Remote amb normalitat.

##Control sobre l'equip remot
Un cop la sessió està connectada, l'usuari de l'equip controlador pot prémer F11 per començar a controlar l'equip remot (per exemple, enviant pulsacions de teclat o entrada Braille). 
Quan NVDA digui controlant equip remot, les tecles que premis en el teu teclat o pantalla braille aniran a l'equip remot. Més encara, si l'equip controlador disposa d'una pantalla braille, la informació remota es mostrarà en ella. Prem F11 de nou per aturar l'enviament de pulsacions i tornar a l'equip controlador.
Per a més compatibilitat, assegura't que les distribucions de teclat de les dues màquines coincideixen.

## Compartir la teva sessió

Per a compartir un enllaç que permeti a algú més unir-se fàcilment a la teva sessió de NVDA Remote, selecciona Copiar enllaç en el menú remot.
Si estàs connectat com a controlador, aquest enllaç permetrà a qualsevol connectar-se i ser controlat.
Si pel contrari has configurat el teu equip per ser controlat, l'enllaç permetrà a la gent amb la que ho comparteixis controlar-ho.
Moltes aplicacions permeten als usuaris activar aquest enllaç automàticament, però si no s'obre des d'una aplicació específica, pots copiar-lo i obrir-lo des del diàleg executar.

##Enviar ctrl + alt + supr
Encara que l'enviament de tecles estigui activat, la combinació ctrl + alt + supr no es pot enviar com la resta.
Si necessites enviar ctrl + alt + supr, i el sistema remot es troba a l'escriptori segur, tria aquesta opció.

##Control remot d'un equip desatès

De vegades pots voler controlar un dels teus propis equips remotament. Això és especialment útil si et trobes viatjant, i vols controlar el pc de casa des del portàtil, o controlar un equip en una habitació de casa teva mentre ets fora amb un altre pc. Amb una preparació una mica avançada això es fa possible.

1. Entra al menú de NVDA, tria eines ia continuació remot. Finalment, prem intro en opcions.
2. Marca la casella que diu "Connectar automàticament al servidor de control en arrencar".
3. Tria si faràs servir un servidor de control remot o crearàs un servidor local.
4. Tria permetre que controlin aquest equip en el segon grup de botons d'opció.
5. Si crees el teu propi servidor, hauràs d'assegurar-te que el port introduït en el camp port (per defecte 6837) està obert en l'equip controlat i els equips controladors poden connectar-se a ell.
6. Si vols fer servir un servidor de control remot, omple els camps equip o servidor i clau, prem tabulador fins a acceptar, i prem intro. Tingues en compte que l'opció generar clau no es troba disponible en aquesta situació. És millor escriure una clau que es pugui recordar per a que puguis fer-la servir fàcilment des de qualsevol lloc remot.  

Per a un ús avançat, pots també configurar NVDA Remote per a que es connecti a un servidor local o remot en mode controlador. Si vols això, selecciona controlar un altre equip en el segon grup de botons d'opció.

Nota: les opcions relacionades amb connectar automàticament en arrencar en el diàleg d'opcions no tenen efecte fins que no es reinicia NVDA.

##Silenciar la veu en l'equip remot
Si no vols sentir la veu de l'ordinador remot o sons específics de NVDA, és tan simple com anar al menú de NVDA, eines, remot. Baixa amb fletxa avall fins sentir silenciar equip remot, i prem intro. Tingues en compte que aquesta opció no desactivarà la sortida braille remota a la pantalla controladora quan l'equip controlador estigui enviant pulsacions.


##Finalitzar una sessió remota

Per finalitzar una sessió remota, fes el següent:

1. En l'equip controlador, prem F11 per deixar de controlar l'equip remot. Hauries d'escoltar o llegir el missatge: "Controlant equip local.". Si en comptes d'això sents o llegeixes un missatge dient que estàs controlant l'equip remot, prem F11 de nou.

2. Accedeix al menú de NVDA, eines, remot, i prem intro en desconnectar.

##Enviar porta-retalls
L'opció enviar porta-retalls en el menú remot et permet enviar text des del teu porta-retalls.
Quan estigui activada, qualsevol text al porta-retalls s'enviarà als altres equips.

##Configura NVDA Remote per a que funcioni a l'escriptori segur

Per a que NVDA Remote funcioni a l'escriptori segur, el complement ha d'estar instal·lat al NVDA que s'executa a l'escriptori segur.

1. Al menú de NVDA, selecciona preferències, i a continuació opcions generals.

2. Prem tabulador fins al botó Utilitzar opcions actualment guardades en l'autenticació (logon) i altres pantalles segures (requereix privilegis d'administrador), i prem intro.

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
* Babbage B.V.
* Leonard de Ruijter

## Registre de canvis

### Versió 2.0

* Suport per a braille remot 
* Suport per a enllaços nvdaremote://
* S'han centrat els diàlegs per a que encaixin amb tots els demés de NVDA
* Arreglat portcheck per a que apunti a un domini que nosaltres controlem, portcheck.nvdaremote.com
* Suport de connexió automàtica a un servidor de control en mode mestre
* Arreglat error de renderitzat en la documentació.
* Actualització a la versió 2 del protocol, que inclou un camp d'origen en cada missatge remot
* Neteja important del codi que permetrà modificar-lo més fàcilment en el futur.



