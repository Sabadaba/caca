# Implementando un Cloud Gaming Service

Un Cloud Gaming Service es un servicio en que el procesamiento gráfico asociado a un videojuego se realiza en un servidor. El jugador se conecta desde su equipo (cliente) al servidor y recibe desde este los cuadros (frames) del videojuego de forma muy similar a un servicio de streaming. De esta forma  un cliente con un computador relativamente básico podrá disfrutar de videojuegos de alto estándar gráfico (siempre y cuando tenga una buena conexión al servidor).

En este proyecto ustedes deben escribir un *codec* para la transmisión de los cuadros (frames) del videojuego. La codificación debe:
- aplicar una transformación al dominio de frecuencia
- cuantizar los datos transformados, el nivel de cuantización debe ser configurable
- codificar los datos cuantizados utilizando un código de largo variable 
- explotar la redundancia entre frames sucesivos

El *codec* debe también ser capaz de decodificar los frames en el cliente, es decir realizar el proceso inverso al descrito anteriormente.

Para simplificar se utilizarán imágenes en escala de grises.

## Indicaciones para la implementación

Implemente las funciones `code` y `decode` en el script `src/mycodec.py`

Puede estudiar los demás scripts en `src/` pero no es necesario modificarlos

- Para enviar los mensajes se utiliza la librería [ZeroMQ](https://pyzmq.readthedocs.io/en/latest/index.htmlhttps://pyzmq.readthedocs.io/en/latest/index.html)
- Para visualizar los cuadros se utiliza OpenCV

Para desarrollar y probar su codec se recomienda crear un ambiente de conda con al menos `opencv`, `numpy` y  `pyzmq`

## Sobre como probar su implementación 

Para iniciar la transmisión de frames a una IP `1.2.3.4`:

    python src/transmitter.py --IP 1.2.3.4

Puede usar la IP `0.0.0.0` para transmitir a su propio equipo. Para transmistir a un equipo que no está en su red local se recomienda configurar una red virtual con [ZeroTier](https://zerotier.atlassian.net/wiki/spaces/SD/pages/8454145/Getting+Started+with+ZeroTier)

Una vez que haya lanzado el transmisor, abra otro terminal e inicie el receptor con

    python src/receive.py 

Esto debería abrir una ventana de opencv donde se comenzarán a mostrar los frames del juego

Mate el transmisor con Control+C y el receptor se detendrá automáticamente. Al terminar, el receptor retornará el promedio y desviación estándar del tiempo entre frames sucesivos.

## Indicaciones sobre la experimentación 

Seleccionen al menos tres niveles de cuantización. Hagan una tabla con el nivel de cuantización, el error de distorsión y el peso final del mensaje codificado. Muestre ejemplos gráficos del resultado de cuantización y hagan comentarios con respecto a la calidad de la imagen. 

Note que el tiempo entre frames está influenciado por varios factores, entre ellos:
- El tamaño del mensaje codificado (depende sólo del codec)
- El ancho de banda entre transmisor y receptor (depende de su conexión a internet)
- La velocidad de procesamiento del equipo transmisor y receptor, respectivamente

Haga una tabla con las características generales de los computadores y ancho de banda teórico de cada integrante del grupo. Luego los integrantes tomarán turnos para actuar como transmisor y receptor. Un grupo de $N$ integrantes deberá hacer $3N^2$ experimentos de medición de tiempo.

Por ejemplo para un grupo de dos personas A y B:
- A es transmisor y receptor
- A es transmisor y B receptor
- A es receptor y B transmisor
- B es transmisor y receptor
Y en cada uno de los casos anteriores se medirn los tiempos para los tres niveles de cuantización

Redacte un informe formal con los resultados y análisis de sus experimentos.

## Sobre la evaluación

- El proyecto se evaluará en base a un informe, una demostración y los códigos en su repositorio github
- El plazo de entrega del informe es el Miércoles 20 de Abril a las 10:00am a través de siveducmd. Sólo se aceptará formato pdf
- El sistema github classrooms dejará de aceptar *commits* a la hora indicada en el punto anterior. Los códigos se evaluarán en base al último *commit* de la rama *main*. Haga *commits* con avances regulares ya que se evaluará su progreso.
- El Miércoles 20 de Abril a las 10:00 los grupos exhibirán su proyecto funcionando frente al profesor y contestarán preguntas sobre su implementación
- Se espera que sigan el [código de ética de la ACM](https://www.acm.org/code-of-ethics)
- Consultas de preferencia por discord
