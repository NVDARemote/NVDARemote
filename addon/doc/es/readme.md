#NVDA Remote Access
Versión 2.0

Bienvenido al complemento de acceso remoto de NVDA, que te permitirá conectarte a otro equipo que ejecute el lector de pantalla gratuito NVDA. Da igual que estés al otro lado de la habitación o al otro lado del mundo. Conectarse es simple, y hay muy pocas órdenes que aprenderse. Puedes conectarte al equipo de otra persona, o permitir a una persona de confianza que se conecte a tu sistema para realizar un mantenimiento rutinario, diagnosticar un problema, o enseñarte algo.

##Antes de empezar

Es necesario tener instalado NVDA en ambos equipos, y obtener el complemento NVDA Remote Access.
La instalación de NVDA y del complemento no varía con respecto a otras. Si necesitas más información, puedes encontrarla en la guía de usuario de NVDA.

## Actualizaciones

Cuando actualices el complemento, si has instalado NVDA Remote en el escritorio seguro, es recomendable que lo actualices también allí.
Para hacerlo, primero actualiza el complemento normalmente. Después, abre el menú de NVDA, preferencias, Opciones Generales, y pulsa el botón etiquetado como "Utilizar opciones actualmente guardadas en la autentificación (logon) y otras pantallas seguras (requiere privilegios de administrador)".

##Iniciar una sesión remota a través de un servidor externo
###En el equipo controlado
1. Abre el menú de NVDA, herramientas, remoto, conectar.
2. Elige cliente en el primer grupo de botones de opción.
3. Elige permitir que controlen este equipo en el segundo grupo de botones de opción.
4. En el campo equipo o servidor, introduce el servidor al que te vas a conectar, por ejemplo nvdaremote.com. Cuando el servidor use un puerto distinto al que este complemento utiliza por defecto, puedes introducir su dirección en formato &lt;equipo&gt;:&lt;puerto&gt;, por ejemplo nvdaremote.com:1234.
5. Introduce una clave en el campo clave, o pulsa el botón generar clave.
La clave es lo que otros usarán para controlar tu equipo.
El equipo controlado y todos sus clientes deben usar la misma clave.
6. Pulsa aceptar. Hecho esto, escucharás un pitido y conectado.

###En el equipo desde el que se controla
1. Abre el menú de NVDA, herramientas, remoto, conectar.
2. Elige cliente en el primer grupo de botones de opción.
3. Selecciona controlar otro equipo en el segundo grupo de botones de opción.
4. En el campo equipo o servidor, introduce el servidor al que te vas a conectar, por ejemplo nvdaremote.com. Cuando el servidor use un puerto distinto al que este complemento utiliza por defecto, puedes introducir su dirección en formato &lt;equipo&gt;:&lt;puerto&gt;, por ejemplo nvdaremote.com:1234.
5. Introduce una clave en el campo clave, o pulsa el botón generar clave.
El equipo controlado y todos sus clientes deben usar la misma clave.
6. Pulsa aceptar. Hecho esto, escucharás un pitido y conectado.

##Conexiones directas
La opción servidor en el diálogo conectar permite establecer una conexión directa.
Una vez seleccionada, elige el modo en el que se comportará tu equipo durante la conexión.
La otra persona se conectará usando el contrario.

Una vez seleccionado el modo, puedes usar el botón obtener IP externa para obtener tu dirección IP externa y asegurarte de que el puerto que has introducido en el campo puerto está abierto correctamente.
Si portcheck detecta que tu puerto (por defecto 6837) no está abierto, aparecerá una advertencia.
Abre el puerto e inténtalo de nuevo.
Nota: el proceso de abrir puertos está fuera del propósito de este documento. Consulta la documentación que acompaña a tu router para más información.

Introduce una clave en el campo clave, o pulsa generar. La otra persona necesitará tu IP externa junto con la clave para conectar. Si has introducido un puerto distinto al que se usa por defecto (6837) en el campo puerto, asegúrate de que la otra persona añade el puerto alternativo a la dirección del equipo usando el formato &lt;ip externa&gt;:&lt;puerto&gt;.

Una vez pulses aceptar, estarás conectado.
Cuando la otra persona se conecte, podrás usar NVDA Remote con normalidad.

##Control sobre el equipo remoto
Una vez la sesión está conectada, el usuario del equipo controlador puede pulsar f11 para empezar a controlar el equipo remoto (por ejemplo, enviando pulsaciones de teclado o entrada Braille).
Cuando NVDA diga controlando equipo remoto, las teclas que pulses en tu teclado o pantalla braille irán al equipo remoto. Más aún, si el equipo controlador dispone de una pantalla braille, la información remota se mostrará en ella. Pulsa f11 de nuevo para detener el envío de pulsaciones y volver al equipo controlador.
Para mayor compatibilidad, asegúrate de que las distribuciones de teclado de ambas máquinas coinciden.

## Compartir tu sesión

Para compartir un enlace que permita a alguien más unirse fácilmente a tu sesión de NVDA Remote, selecciona Copiar enlace en el menú remoto.
Si estás conectado como controlador, este enlace permitirá a cualquiera conectarse y ser controlado.
Si por el contrario has configurado tu equipo para ser controlado, el enlace permitirá a la gente con la que lo compartas controlarlo.
Muchas aplicaciones permiten a los usuarios activar este enlace automáticamente, pero si no se abre desde una aplicación específica, puedes copiarlo y abrirlo desde el diálogo ejecutar.


##Enviar ctrl+alt+supr
Aunque el envío de teclas esté activado, la combinación ctrl+alt+supr no se puede enviar como el resto.
Si necesitas enviar ctrl+alt+supr, y el sistema remoto se encuentra en el escritorio seguro, elige esta opción.

##Control remoto de un equipo desatendido

A veces puedes querer controlar uno de tus propios equipos remotamente. Esto es especialmente útil si te encuentras viajando, y quieres controlar el pc de casa desde el portátil, o controlar un equipo en una habitación de tu casa mientras estás fuera con otro pc. Con una preparación un poco avanzada esto se hace posible.

1. Entra en el menú de NVDA, elige herramientas y a continuación remoto. Finalmente, pulsa intro en opciones.
2. Marca la casilla que dice "Conectar automáticamente al servidor de control al arrancar".
3. Elige si vas a usar un servidor de control remoto o a crear un servidor local.
4. Elige permitir que controlen este equipo en el segundo grupo de botones de opción.
5. Si creas tu propio servidor, tendrás que asegurarte de que el puerto introducido en el campo puerto (por defecto 6837) está abierto en el equipo controlado y los equipos controladores pueden conectarse a él.
6. Si quieres usar un servidor de control remoto, rellena los campos equipo o servidor y clave, pulsa tabulador hasta aceptar, y pulsa intro. Ten en cuenta que la opción generar clave no se encuentra disponible en esta situación. Es mejor escribir una clave que se pueda recordar para que puedas usarla fácilmente desde cualquier lugar remoto.

Para un uso avanzado, puedes también configurar NVDA Remote para que se conecte a un servidor local o remoto en modo controlador. Si quieres esto, selecciona controlar otro equipo en el segundo grupo de botones de opción.

Nota: las opciones relacionadas con conectar automáticamente al arrancar en el diálogo de opciones no tienen efecto hasta que se reinicia NVDA.


##Silenciar la voz en el equipo remoto
Si no quieres oír la voz del ordenador remoto o sonidos específicos de NVDA, es tan simple como ir al menú de NVDA, herramientas, remoto. Baja con flecha abajo hasta oír silenciar equipo remoto, y pulsa intro. Ten en cuenta que esta opción no desactivará la salida braille remota a la pantalla controladora cuando el equipo controlador esté enviando pulsaciones.


##Finalizar una sesión remota

Para finalizar una sesión remota, haz lo siguiente:

1. En el equipo controlador, pulsa f11 para dejar de controlar el equipo remoto. Deberías escuchar o leer el mensaje: "Controlando equipo local". Si en vez de eso oyes o lees un mensaje diciendo que estás controlando el equipo remoto, pulsa f11 nuevamente.

2. Accede al menú de NVDA, herramientas, remoto, y pulsa intro en desconectar.

##Enviar portapapeles
La opción enviar portapapeles en el menú remoto te permite enviar texto desde tu portapapeles.
Cuando esté activada, cualquier texto en el portapapeles se enviará a los otros equipos.

##Configurar NVDA Remote para que funcione en el escritorio seguro

Para que NVDA Remote funcione en el escritorio seguro, el complemento debe estar instalado en el NVDA que se ejecuta en el escritorio seguro.

1. En el menú de NVDA, selecciona preferencias, y a continuación opciones generales.

2. Pulsa tabulador hasta el botón Utilizar opciones actualmente guardadas en la autentificación (logon) y otras pantallas seguras (requiere privilegios de administrador), y pulsa Intro.

3. Responde sí a las advertencias sobre copiar la configuración y los complementos, y responde a la advertencia del control de cuentas de usuario que debería aparecer.

4. Cuando la configuración se haya copiado, pulsa intro para aceptar la confirmación. Pulsa tabulador hasta aceptar y pulsa intro de nuevo para salir del diálogo.

En cuanto NVDA Remote esté instalado en el escritorio seguro, si te controlan en una sesión remota,
el escritorio seguro tendrá soporte de voz y braille cuando se entre en él.

##Contribuciones
Nos gustaría dar nuestro reconocimiento a los siguientes contribuyentes que, entre otros, han ayudado a que el proyecto NVDA Remote sea una realidad.

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

## Registro de cambios

### Versión 2.0

* Soporte para braille remoto
* Soporte para enlaces nvdaremote://
* Se han centrado los diálogos para que encajen con todos los demás de NVDA
* Arreglado portcheck para que apunte a un dominio que nosotros controlamos, portcheck.nvdaremote.com
* Soporte de conexión automática a un servidor de control en modo maestro
* Arreglado error de renderizado en la documentación
* Actualización a la versión 2 del protocolo, que incluye un campo de origen en cada mensaje remoto
* Limpieza importante del código que permitirá modificarlo más fácilmente en el futuro

