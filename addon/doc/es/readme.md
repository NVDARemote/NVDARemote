#NVDA Remote Access
Versión 1.0

Bienvenido al complemento de acceso remoto de NVDA, que te permitirá conectarte a otro equipo que ejecute el lector de pantalla gratuito NVDA. Da igual que estés al otro lado de la habitación o al otro lado del mundo. Conectarse es simple, y hay muy pocos comandos que aprenderse. Puedes conectarte al equipo de otra persona, o permitir a una persona de confianza que se conecte a tu sistema para realizar un mantenimiento rutinario, diagnosticar un problema, o enseñarte algo.

##Antes de empezar

Es necesario tener instalado NVDA en ambos equipos, y obtener el complemento NVDA Remote Access.
La instalación de NVDA y del complemento no varía con respecto a otras. Si necesitas más información, puedes encontrarla en la guía de usuario de NVDA.

##Iniciar una sesión remota a través de un servidor externo
###El equipo controlado
1. Abre el menú de NVDA, herramientas, remoto, conectar.
2. Elige cliente en el primer grupo de botones de opción.
3. Elige permitir que controlen este equipo en el segundo grupo de botones de opción.
4. En el campo equipo, introduce el servidor al que te vas a conectar, por ejemplo nvdaremote.com.
5. Introduce una clave en el campo clave, o pulsa el botón generar clave.
La clave es lo que otros usarán para controlar tu equipo.
La máquina controlada y todos sus clientes deben usar la misma clave.
6. Pulsa aceptar. Hecho esto, escucharás un pitido y conectado.

###Controlar otro equipo
1. Abre el menú de NVDA, herramientas, remoto, conectar.
2. Elige cliente en el primer grupo de botones de opción.
3. Selecciona controlar otro equipo en el segundo grupo de botones de opción.
4. En el campo equipo, introduce el servidor al que te vas a conectar, por ejemplo nvdaremote.com.
5. Introduce una clave en el campo clave, o pulsa el botón generar clave.
La clave es lo que otros usarán para controlar tu equipo.
La máquina controlada y todos sus clientes deben usar la misma clave.
6. Pulsa aceptar. Hecho esto, escucharás un pitido y conectado.

##Conexiones directas
La opción servidor en el diálogo conectar permite establecer una conexión directa.
Una vez seleccionada, elige el modo en el que se comportará tu equipo durante la conexión.
La otra persona se conectará usando el contrario.

Una vez seleccionado el modo, puedes usar el botón obtener IP externa para obtener tu dirección IP externa y asegurarte de que el puerto está abierto correctamente.
Si portcheck detecta que el puerto 6837 no está abierto, aparecerá una advertencia.
Abre el puerto e inténtalo de nuevo.
Nota: el proceso de abrir puertos está fuera del propósito de este documento. Consulta la documentación que acompaña a tu router para más información.

Introduce una clave en el campo clave, o pulsa generar. La otra persona necesitará tu IP externa junto con la clave para conectar.

Una vez pulses aceptar, estarás conectado.
Cuando la otra persona se conecte, podrás usar NVDA Remote con normalidad.

##Envío de pulsaciones de teclado
Una vez la sesión está conectada, el controlador puede pulsar f11 para enviar pulsaciones de teclado.
Cuando NVDA diga envío de teclas activado, las teclas que pulses irán al equipo remoto. Pulsa f11 de nuevo para detener el envío de teclas y volver al equipo controlador.
Para mayor compatibilidad, asegúrate de que las distribuciones de teclado de ambas máquinas coinciden.

##Enviar ctrl+alt+supr
A pesar de que el envío de teclas esté activado, la combinación ctrl+alt+supr no se puede enviar como el resto.
Si necesitas enviar ctrl+alt+supr, y el sistema remoto se encuentra en el escritorio seguro, usa este comando.

##Control remoto de un equipo desatendido

A veces puedes querer controlar uno de tus propios equipos remotamente. Esto es especialmente útil si te encuentras viajando, y quieres controlar el pc de casa desde el portátil, o controlar un equipo en una habitación de tu casa mientras estás fuera con otro pc. Con una preparación un poco avanzada esto se hace posible.

1. Entra en el menú de NVDA, elige herramientas y a continuación remoto. Finalmente, pulsa intro en opciones.
2. Marca la casilla que dice "Conectar automáticamente al servidor de control al arrancar".
3. Rellena los campos equipo y clave, pulsa tabulador hasta aceptar, y pulsa intro.
4. Ten en cuenta que la opción generar clave no se encuentra disponible en esta situación. Es mejor escribir una clave que se pueda recordar para que puedas usarla fácilmente desde cualquier lugar remoto.

##Silenciar la voz en el equipo remoto
Si no quieres oír la voz del ordenador remoto, es tan simple como ir al menú de NVDA, herramientas, remoto. Baja con flecha abajo hasta oír silenciar voz del equipo remoto, y pulsa intro.

##Finalizar una sesión remota

Para finalizar una sesión remota, haz lo siguiente:

1. En el equipo controlador, pulsa f11 para dejar de enviar pulsaciones de teclado. Deberías escuchar el mensaje: "Envío de teclas desactivado.". Si oyes un mensaje diciendo que el envío de teclas está activado, pulsa f11 nuevamente.

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
el escritorio seguro será leído cuando se entre en él.

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
* Tyler W Kavanaugh
* Casey Mathews
