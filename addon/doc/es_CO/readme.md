#NVDA Remote Access
Versión 1.0

Bienvenido al complemento NVDA Remote Access, el cual te permitirá conectarte a otro equipo que ejecute el lector de pantallas gratuito NVDA. No hace ninguna diferencia si te encuentras al otro lado de la habitación, o al otro lado del mundo. Conectarse es simple, y hay muy pocos comandos que recordar . Puedes conectarte al equipo de otra persona, o permitir que una persona de confianza se conecte a tu sistema para realizar mantenimientos de rutina, diagnosticar un problema o suministrar entrenamiento.

##Antes de comenzar

necesitarás haber instalado NVDA en ambos equipos, y obtener el complemento NVDA Remote Access .
Tanto la instalación de NVDA como del complemento Remote Access son estándar. Si necesitas más información, puedes encontrarla en la guía de usuario de NVDA.

##iniciar una  sesión remota a través de un servidor
###el equipo a ser controlado
1. Abrir el menú de NVDA, herramientas, Remoto, Connectar.
2. Seleccionar cliente en el primer grupo de botones de opción.
3. Seleccionar permitir que se controle esta máquina en el segundo conjunto de botones de opción.
4. en el campo host, ingresa el host del servidor al que te estás conectando, por ejemplo, nvdaremote.com.
5. Ingresa una clave en el campo clave, o presiona el botón generar clave.
La clave es lo que los demás usarán para controlar tu equipo.
El equipo que está siendo controlado y todos sus clientes necesitan utilizar la misma clave.
6. Presiona aceptar. Una vez terminado, oirás un tono y conectado.

###El equipo controlador
1. Abrir el menú de NVDA, herramientas, Remoto, Connectar.
2. Seleccionar cliente en el primer grupo de botones de opción.
3. Seleccionar  controlar otra máquina en el segundo conjunto de botones de opción.
4. en el campo host, ingresa el host del servidor al que te estás conectando, por ejemplo, nvdaremote.com.
5. Ingresa una clave en el campo clave, o presiona el botón generar clave.
El equipo que está siendo controlado y todos sus clientes necesitan utilizar la misma clave.
6. Presiona aceptar. Una vez terminado, oirás un tono y conectado.

##Conexiones directas
La opción servidor del diálogo Connectar te permite configurar una conexión directa.
Una vez que selecciones esto, selecciona de qué modo te vas a conectar.
La otra persona se conectará ti utilizando el modo contrario.

Una vez se seleccione el modo, puedes usar el botón obtener ip externa para conseguir tu Dirección ip externa y
asegurarte que tu puerto se abra correctamente.
Si portChec detecta que tu puerto (6837) no se puede alcanzar, aparecerá un aviso.
Abre el puerto y vuelve a intentarlo.
Nota: el proceso para abrir puertos va más allá de este documento. Por favor, consulta la información suministrada con tu router para más instrucciones.

Ingresa una clave en el campo clave, o presiona generar. La otra persona necesitará tanto tu IP externa como la clave para conectarse.

Una vez que se presione aceptar, estarás conectado.
Cuando la otra persona se conecte, puedes usar NVDA Remote normalmente.

##Envío de comandos de teclado
Una vez que la sesión se establezca, la máquina controladora puede entonces presionar f11 para comenzar a enviar comandos de teclado.
Cuando NVDA diga enviando comandos de teclado, las teclas que presiones irán hacia la máquina remota. Vuelve a presionar f11 para dejar de enviar comandos de teclado y regresar a la máquina controladora.
Para una mejor compatibilidad, Porfavor asegúrate que las distribuciones de teclado coincidan en ambas máquinas.

##enviar Ctrl+Alt+Supr
Mientras se estén enviando comandos de teclado, no es posible enviar el comando CTRL+Alt+Supr normalmente.
Si necesitas enviar CTRL+Alt+supr, Y el sistema remoto está en el escritorio seguro, usa este comando.

##Controlar un equipo desatendido remotamente

A veces, puede que desees controlar uno de tus propios equipos remotamente. Esto es especialmente útil si te encuentras de viaje, y deseas controlar la PC de tu casa desde el portátil, o puede que quieras controlar un equipo que está en un cuarto de tu casa, mientras estás sentado en la puerta con otra PC. una preparación avanzada hace que esto sea conveniente y posible.

1. ingresa al menú de NVDA, y selecciona herramientas, y luego remote. Finalmente, presiona enter en opciones.
2. Verifica la casilla que dice: "Conectarse automáticamente al servidor de control al arrancar".
3. rellena los campos host y clave, Tabula hasta aceptar, y presiona enter. 
4. Por favor ten en cuenta: La opción generar clave no está disponible en esta situación. Es mejor que pienses en una clave que recuerdes de forma que puedas usarla fácilmente desde cualquier ubicación remota.

##silenciar la voz del equipo remoto
Si no deseas oír la respuesta de voz del equipo remoto, simplemente accede al menú de NVDA, herramientas, y Remoto. Baja con flecha hasta silenciar voz remota, y presiona enter. 


##Finalizar una sesión remota

Para finalizar una sesión remota, haz lo siguiente:

1. En el equipo controlador, presiona f11 para dejar de enviar comandos de teclado. Deberías oír el mensaje: "sin enviar comandos de teclado." Si en su lugar oyes un mensaje de que estás enviando comandos de teclado, presiona f11 una vez más.

2. Accede al menú de NVDA, luego herramientas, Remoto, y pressiona enter en desconectar.

##Enviar portapapeles
La opción enviar texto del portapapeles del menú remoto te permite enviar texto desde tu portapapeles.
cuando está activado, cualquier texto en el portapapeles se enviará a las otras máquinas.

##Configurar NVDA remote para que funcione en un escritorio seguro

Para que NVDA Remote funcione en el escritorio seguro, el complemento debe estar instalado en la función de escritorio seguro de NVDA.

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
