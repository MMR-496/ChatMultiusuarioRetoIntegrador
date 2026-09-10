# Chat por sockets (cliente-servidor)
Este programa se trata de un chat de consola elaborado con Python. Un servidor se queda escuchando conexiones y varios clientes se pueden conectar al mismo tiempo y enviarse mensajes entre ellos. En resumen, es un chat grupal sencillo

# Funcionamiento
A grandes rasgos, el servidor espera clientes todo el tiempo, cada vez que alguien e conecta abre un nuevo hilo, propio de ese cliente en específico. Así se puede habar con varias personas sin que se bloquee el servicio a los demás.

Del lado del cliente pasa algo parecido, ya que no se puede estar escribiendo y escuchando mensajes a la vez en un solo hilo, el cliente usa dos hilos, uno para cuando el usuario escribo y el otro corriendo aparte solo para avisar cuando llega un nuevo mensaje.

El servidor lleva un registro de quién está conectado (usando un diccionario) y con eso puede reenviar cada mensaje a todos los demás menos a quien lo mandó. Cuando alguien se va el servidor se da cuenta porque deja de recibir datos de esa persona, lo borra de su lista y le avisa a los demás que esa persona ya no está
