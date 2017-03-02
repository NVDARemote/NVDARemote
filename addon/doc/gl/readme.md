#NVDA Remote Access
Versión 2.0

Benvido ao complemento de acceso remoto de NVDA, que che permitirá conectarte a outro equipo que execute o lector de pantalla de balde NVDA. Da igual que esteas ó outro lado da habitación ou ó outro lado do mundo. Conectarse é simple, e hai moi poucos comandos que aprenderse. Podes conectarte ao equipo doutra persoa, ou permitir a unha persoa de confianza que se conecte ao teu sistema para realizar un mantemento rutinario, diagnosticar un problema, ou ensinarche algo.

##Actualización

Cando se actualice o complemento, se instalaches NVDA Remote no escritorio seguro, recoméndase que actualices tamén a copia do escritorio seguro.
Para facer isto, primeiro actualiza o complementeo existente. De seguido abre o menú de NVDA, preferencias, Opcións Xerais, e preme o botón etiquetado coa "Utilizar opcións actualmente gardadas do logon e outras pantallas seguras (require privilexios de administrador)".

##Antes de comezar

É necesario ter instalado NVDA en ambos os dous equipos, e obter o complemento NVDA Remote Access.
A instalación de NVDA e do complemento non varía con respecto a outras. Se necesitas máis información, podes encontrala na guía de usuario de NVDA.

##Iniciar unha sesión remota a través dun servidor externo
###O equipo controlado
1. Abre o menú de NVDA, ferramentas, remoto, conectar.
2. Elixe cliente no primeiro grupo de botóns de opción.
3. Elixe permitir que controlen este equipo no segundo grupo de botóns de opción.
4. No campo equipo ou servidor, introduce o servidor ao que te vas a conectar, por exemplo nvdaremote.com. Cando o servidor remoto utiliza un porto diferente (ao 6837), pode introducir o nome na forma &lt;servidor&gt;:&lt;porto&gt;, por exemplo nvdaremote.com:1234.
5. Introduce unha clave no campo clave, ou preme o botón xerar clave.
A clave é o que outros utilizarán para controlar o teu equipo.
A máquina controlada e todos os seus clientes deben usar a mesma clave.
6. Pulsa aceptar. Feito isto, escoitarás un son e conectado.

###Controlar outro equipo
1. Abre o menú de NVDA, ferramentas, remoto, conectar.
2. Elixe cliente no primeiro grupo de botóns de opción.
3. Elixe controlar outro equipo no segundo grupo de botóns de opción.
4. No campo equipo ou servidor, introduce o servidor ao que te vas a conectar, por exemplo nvdaremote.com. Cando o servidor remoto utiliza un porto diferente (ao 6837), pode introducir o nome na forma &lt;servidor&gt;:&lt;porto&gt;, por exemplo nvdaremote.com:1234.
5. Introduce unha clave no campo clave, ou preme o botón xerar clave.
A clave é o que outros utilizarán para controlar o teu equipo.
A máquina controlada e todos os seus clientes deben usar a mesma clave.
6. Pulsa aceptar. Feito isto, escoitarás un son e conectado.

##Conexións directas
A opción servidor no diálogo conectar permite establecer una conexión directa.
Unha vez seleccionada, elixe o modo no que se comportará o teu equipo durante a sesión.
A outra persoa conectarase utilizando o contrario.

Unha vez seleccionado o modo, podes usar o botón obter IP externo para obter o teu enderezo IP externo e asegurarte de que o porto introducido no campo "porto" está reenviado(aberto) correctamente.
Se portcheck detecta que o porto (por defecto 6837) non se pode alcanzar dende Internet, aparecerá una advertencia.
Reenvía(abre) o porto e inténtao de novo.
Nota: o proceso de reenviar portos está fóra do propósito deste documento. Consulta a documentación que acompaña ao teu router para máis información.

Introduce unha clave no campo clave, ou preme xerar. A outra persoa necesitará o teu IP externo xunto coa clave para conectar. Se se introduciu un porto diferente ao predeterminado (6837) no campo "porto", asegúrate de que a outra persoa engade o porto ó enderezo do equipo na forma &lt;IP externo&gt;:&lt;porto&gt;.

Unha vez premas aceptar, estarás conectado.
Cando a outra persoa se conecte, poderás usar NVDA Remote con normalidade.

##Envío de pulsacións de teclado
Unha vez a sesión está conectada, o controlador pode premer f11 para enviar pulsacións de teclado.
Cando NVDA diga envío de teclas activado, as teclas que premas irán ao equipo remoto. Pulsa f11 de novo para deter o envío de teclas e volver ao equipo controlador.
Para maior compatibilidade, asegúrate de que as distribucións de teclado de ambas máquinas coinciden.

##Enviar ctrl+alt+supr
A pesares de que o envío de teclas estea activado, a combinación ctrl+alt+supr non se pode enviar coma o resto.
Se necesitas enviar ctrl+alt+supr, e o sistema remoto se encontra no escritorio seguro, usa este comando.

##Control remoto dun equipo desatendido

Ás veces podes querer controlar un dos teus propios equipos remotamente. Isto é especialmente útil se te encontras viaxando, e queres controlar o ordenador da casa dende o portátil, ou controlar un equipo nunha habitación da túa casa mentres estás fóra con outro equipo. Cunha preparación un pouco avanzada isto faise posible.

1. Entra no menú de NVDA, elixe ferramentas e a continuación remoto. Finalmente, ulsa intro en opcións.
2. Marca a casilla "Conectar automaticamente ao servidor de control ao arrancar".
3. Selecciona entre utilizar un servidor de control remoto ou hospedar a conexión localmente.
4. Se hospedas a conexión ti mesmo, necesitarás asegurarte de que o porto introducido no campo homónimo (por defecto 6837) no equipo controlado pode ser alcanzado dende os equipos controladores.
5. Se desexas utilizar un servidor de control remoto, enche os campos equipo e clave, preme tabulador ata aceptar, e pulsa intro. A opción xerar clave non se atopa dispoñible nesta situación. É mellor escribir unha clave que se poida recordar para que poidas usala facilmente dende calqueira lugar remoto.

Nota: As opcións relacionadas coa autoconexión ao inicio no diálogo de opcións non se aplicarán ata que NVDA se reinicie.


##Silenciar a voz no equipo remoto
Se non queres escoitar a voz do ordenador remoto, é tan simple coma ir ao menú de NVDA, ferramentas, remoto. Baixa con flecha abaixo hasta oír silenciar voz do equipo remoto, e preme intro.

##Finalizar unha sesión remota

Para finalizar unha sesión remota, fai o seguinte:

1. No equipo controlador, pulsa f11 para deixar de enviar pulsacións de teclado. Deberías escoitar a mensaxe: "Envío de teclas desactivado.". Se oes unha mesaxe dicindo que o envío de teclas está activado, pulsa f11 novamente.

2. Accede ao menú de NVDA, ferramentas, remoto, e pulsa intro en desconectar.

##Enviar portapapeis
A opción enviar portapapeis no menú remoto permíteche enviar texto dende o teu portapapeis.
Cando estea activada, calqueira texto no portapapeis enviarase ós outros equipos.

##Configurar NVDA Remote para que funcione no escritorio seguro

Para que NVDA Remote funcione no escritorio seguro, o complemento debe estar instalado no NVDA que se executa no escritorio seguro.

1. No menú de NVDA, selecciona preferencias, e a continuación opcións xerais.

2. Pulsa tabulador ata o botón Utilizar opcións actualmente gardadas na autentificación (logon) e outras pantallas seguras (require privilexios de administrador), e pulsa Intro.

3. Responde sí ás advertencias sobre copiar a configuración e os complementos, e responde á advertencia do control de contas de usuario que debería aparecer.

4. Cando a configuración se haxa copiado, preme intro para aceptar a confirmación. Pulsa tabulador ata aceptar e preme intro de novo para salir do diálogo.
En canto NVDA Remote estea instalado no escritorio seguro, se te controlan en unha sesión remota,
o escritorio seguro será leído cando se entre nel.

##Contribucións
Gustaríanos dar o noso recoñecemento aos seguintes contribuíntes que, entre outros, axudaron a que o proxecto NVDA Remote fora unha realidade.

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

##Rexistro de cambios

###Versión 2.0

* Soporte para braille remoto
* Soporte para ligas nvdaremote://.
* Diálogos centrados para estar conforme co resto do NVDA
* Arranxado portcheck para apuntar a un dominio que nós controlamos, portcheck.nvdaremote.com
* Soporte para conectarse automaticamente a un servidor de control en modo mestro.
* Arranxado erro de representación na documentación.
* Actualización á versión 2 do protocolo, que inclúe un campo orixe para todas as mensaxes remotas
* Limpeza significativa de código para permitir modificacións máis sinxelas no futuro.

Traducido ao galego por Iván Novegil &lt;info@inovegil.site40.net&gt;