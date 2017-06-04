#NVDA Remote Access
Versión 2.0

Bienvenido al complemento NVDA Remote Access, el cual te permitirá conectarte a otro equipo que ejecute el lector de pantallas gratuito NVDA. No hace ninguna diferencia si te encuentras al otro lado del cuarto, o al otro lado del mundo. Conectarse es simple, y hay muy pocos comandos que recordar. Puedes conectarte al equipo de otra persona, o permitir que una persona de confianza se conecte a tu sistema para realizar mantenimientos de rutina, diagnosticar un problema o suministrar entrenamiento.

##Antes de comenzar

necesitarás haber instalado NVDA en ambos equipos, y obtener el complemento NVDA Remote Access.
Tanto la instalación de NVDA como del complemento Remote Access son estándar. Si necesitas más información, puedes encontrarla en la guía de usuario de NVDA.

##Actualizar

Cuando actualices el complemento, si has instalado NVDA remote en el escritorio seguro, se recomienda que también actualices la copia en el escritorio seguro. 
para hacer esto, primero actualiza tu complemento existente, luego abre el menú de NVDA, preferencias, configuración general, y presiona el botón etiquetado como Utilizar configuración actualmente guardada en el  logueo y otras pantallas seguras (requiere privilegios de administrador)". 

##iniciar una  sesión remota a través de un servidor
###el equipo a ser controlado
1. Abrir el menú de NVDA, herramientas, Remoto, Connectar.
2. Seleccionar cliente en el primer grupo de botones radiales.
3. Seleccionar permitir que se controle esta máquina en el segundo conjunto de botones radiales.
4. en el campo host, ingresa el host del servidor al que te estás conectando, por ejemplo, nvdaremote.com. Cuando el servidor en particular utilice un puerto alternativo, puedes ingresar el host de la forma &lt;host&gt;:&lt;port&gt;, 
5. Ingresa una clave en el campo clave, o presiona el botón generar clave.
La clave es lo que los demás usarán para controlar tu equipo.
El equipo que está siendo controlado y todos sus clientes necesitan utilizar la misma clave.
6. Presiona aceptar. Una vez terminado, oirás un tono y conectado.

##En la máquina que haya de ser el equipo controlador

1. Abrir el menú de NVDA, herramientas, remoto, conectar. 
2. Seleccionar cliente en el primer grupo de botones radiales. 
3. Seleccionar "controlar otra máquina" en el segundo conjunto de botones radiales.
4. en el campo host, ingresa el host del servidor al que te estás conectando, por ejemplo, nvdaremote.com. Cuando el servidor particular utilice un puerto alternativo, puedes ingresar el host en el formato &lt;host&gt;:&lt;puerto&gt;, por ejemplo nvdaremote.com:1234.
5. Ingresa una clave en el campo clave, o presiona el botón generar clave.
El equipo que está siendo controlado y todos sus clientes necesitan utilizar la misma clave.
6. Presiona aceptar. Una vez termines, oirás un tono y conectado.

##Conexiones directas
La opción servidor del diálogo Connectar te permite configurar una conexión directa.
Una vez que selecciones esto, selecciona de qué modo te vas a conectar.
La otra persona se conectará ti utilizando el modo contrario.

Una vez se seleccione el modo, puedes usar el botón obtener ip externa para conseguir tu Dirección ip externa y
asegurarte de que el  puerto ingresado en el campo "puerto" se redirija correctamente.
Si portChec detecta que tu puerto (6837 por defecto) no se puede alcanzar, aparecerá una advertencia.
Abre el puerto y vuelve a intentarlo.
Nota: el proceso para abrir puertos va más allá del alcance  de este documento. Por favor, consulta la información suministrada con tu router para más instrucciones.

Ingresa una clave en el campo clave, o presiona generar. La otra persona necesitará tanto tu IP externa como la clave para conectarse. Si ingresaste un puerto diferente del predeterminado (6837) en el campo "puerto", aseguúrate de que la otra persona agregue el puerto alternativo a la dirección del host en el formato &lt;ip externa&gt;:&lt;puerto&gt;.

Una vez que se presione aceptar, estarás conectado.
Cuando la otra persona se conecte, puedes usar NVDA Remote normalmente.

##Controlando la máquina remota

Una vez que la sesión se establezca, el usuario de la máquina controladora puede presionar f11 para  empezar a controlar la máquina remota (e.g. enviando comandos de teclado o entrada braille).
Cuando NVDA diga controlando máquina remota, las teclas que presiones en el teclado o en la pantalla braille irán hacia la máquina remota. Además, cuando la máquina controladora utilice una pantalla braille, ésta mostrará la información de la máquina remota. Vuelve a presionar f11 para dejar de enviar comandos de teclado y regresar a la máquina controladora.
Para una mejor compatibilidad, Porfavor asegúrate que las distribuciones de teclado coincidan en ambas máquinas.

##Compartir tu sesión

Para compartir un enlace de forma que alguien más pueda unirse fácilmente a tu sesión de NVDA remote, selecciona copiar enlace desde el menú remote.
Si estás conectado como controlador, este enlace le permitirá a alguien más conectarse y ser controlado. 
Si en su lugar has configurado tu equipo para ser controlado, el enlace  permitirá que las personas con quienes lo compartas controlen tu máquina. 
Muchas aplicaciones permitirán a los usuarios activar este enlace automáticamente, pero si no se ejecuta desde una aplicación específica, puede copiarse al portapapeles y ejecutarse desde el diálogo ejecutar. 


##enviar Ctrl+Alt+Supr
Mientras se estén enviando comandos de teclado, no es posible enviar el comando CTRL+Alt+Supr normalmente.
Si necesitas enviar CTRL+Alt+supr, Y el sistema remoto está en el escritorio seguro, usa este comando.

##Controlar un equipo desatendido remotamente

A veces, puede que desees controlar uno de tus propios equipos remotamente. Esto es especialmente útil si estás de viaje, y deseas controlar la PC de tu casa desde el portátil, o puede que quieras controlar un equipo que está en un cuarto de tu casa, mientras estás sentado en la puerta con otra PC. una preparación avanzada hace que esto sea conveniente y posible.

1. ingresa al menú de NVDA, y selecciona herramientas, y luego remote. Finalmente, presiona enter en opciones.
2. Verifica la casilla que dice: "Conectarse automáticamente al servidor de control al arrancar".
3. Selecciona si usar un servidor remoto o llevar la conexión localmente. 
4. selecciona permitir que se controle esta máquina en el segundo conjunto de botones radiales. 
5. si llevas la conexión tú mismo, necesitarás asegurarte que se pueda acceder al puerto ingresado en el campo "puerto" (6837 por defecto) en la máquina controlada desde la máquina controladora. 
6. Si deseas usar un servidor sobre la marcha, rellena los campos host y clave, Tabula hasta aceptar, y presiona enter. La opción generar clave no está disponible en esta situación. Es mejor que pienses en una clave que recuerdes de forma que puedas usarla fácilmente desde cualquier ubicación remota.
Para un uso avanzado, puedes también configurar NVDA Remote para que se conecte automáticamente a un servidor local o remoto sobre la marcha en modo controlador. Si así lo deseas, selecciona controlar otra máquina en el segundo conjunto de botones radiales. 

nota: las opciones relacionadas con la conexión automática al arrancar en el diálogo "opciones" no aplicarán hasta que se reinicie NVDA. 

##silenciar la voz del equipo remoto
Si no deseas oír la respuesta de voz del equipo remoto, simplemente accede al menú de NVDA, herramientas, y Remoto. Baja con flecha hasta silenciar voz remota, y presiona enter. Por favor ten en cuenta que, esta opción no desabilitará la entrada braille remota en la pantalla controladora cuando la máquina controladora esté enviando comandos de teclado. 


##Finalizar una sesión remota

Para finalizar una sesión remota, haz lo siguiente:

1. En el equipo controlador, presiona f11 para dejar de controlar la máquina remota. Deberías oír o leer el mensaje: "controlando máquina local". Si en su lugar oyes o lees un mensaje de que estás controlando la máquina remota, presiona f11 una vez más.

2. Accede al menú de NVDA, luego herramientas, Remoto, y pressiona enter en desconectar.

##Enviar portapapeles
La opción enviar texto del portapapeles del menú remoto te permite enviar texto desde tu portapapeles.
cuando está activado, cualquier texto en el portapapeles se enviará a las otras máquinas.

##Configurar NVDA remote para que funcione en un escritorio seguro

Para que NVDA Remote funcione en el escritorio seguro, el complemento debe estar instalado en la copia de NVDA que se ejecuta en el escritorio seguro.

1. Desde el menú de NVDA, selecciona preferencias, luego Configuración general.

2. Tabula hasta el botón Utilizar configuraciones actualmente guardadas en el  logueo y otras pantallas seguras (requiere privilegios de administrador) y presiona enter.

3. Responde sí a las solicitudes sobre el copiado de configuraciones y sobre el copiado de plugins, y responde a la solicitud de control de cuentas de usuario que pueda aparecer.

4. Cuando se copien las configuraciones, presiona enter para pasar por alto el botón aceptar. tabúla hasta aceptar y enter una vez más para salir del diálogo.

Una vez que NVDA Remote se instale en el escritorio seguro, si te están controlando actualmente en una sesión remota, el escritorio seguro se leerá cuando se cambie a él.

##Contribuciones
Nos complacemos en dar  reconocimiento a los siguientes contribuyentes, entre otros, quienes ayudaron a que el proyecto NVDA Remote se hiciera realidad.

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


Traducido a español de colombia por : Slanovani. 