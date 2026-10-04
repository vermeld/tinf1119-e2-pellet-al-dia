# Guía del código: dónde está cada cosa

Para encontrar un botón o una pantalla en VS Code, presiona **Ctrl+Shift+F** (buscar en todos los archivos) y escribe la etiqueta:

| Si te preguntan por… | Busca |
|---|---|
| un botón | `BOTÓN «` y el texto del botón, ej. `BOTÓN «Cómo llegar»` |
| una pestaña de la barra de abajo | `PESTAÑA «Mapa»` (también `Lista` o `Perfil`) |
| una pantalla | `PANTALLA` + su nombre, ej. `PANTALLA DETALLE` |
| un campo para escribir | `CAMPO «`, ej. `CAMPO «Dirección exacta»` |
| una tarjeta o un aviso | `TARJETA` o `AVISO PDA` |
| la validación | `VALIDACIÓN` |
| las estrellas de confiabilidad | `CÁLCULO DE LAS ESTRELLAS` (app/confianza.py) |

Cada pantalla tiene **dos archivos**: el `.kv` (cómo se ve: botones, textos, colores) y el `.py` (qué hace: la lógica). En el `.kv`, la línea `on_release:` dice qué función se ejecuta al presionar el botón; esa función está en el `.py` con un comentario que dice el mismo nombre del botón.

## Barra de abajo (pestañas)

Interfaz: [`app/kv/raiz.kv`](../app/kv/raiz.kv) · Lógica: `app/pelletapp.py (ir_a, al_cambiar_pestana)`

| Línea | Qué es |
|---|---|
| [18](../app/kv/raiz.kv#L18) | BARRA DE ABAJO (navegación) con las 3 pestañas. |
| [23](../app/kv/raiz.kv#L23) | PESTAÑA «Lista»: el botón de la lista. Es la pantalla de inicio. |
| [29](../app/kv/raiz.kv#L29) | PESTAÑA «Mapa»: este es el botón del mapa en la barra de abajo. |
| [34](../app/kv/raiz.kv#L34) | PESTAÑA «Perfil»: el botón del perfil (reputación, ayuda y cerrar sesión). |

## Pantalla Entrar

Interfaz: [`app/kv/entrar.kv`](../app/kv/entrar.kv) · Lógica: `app/screens/entrar.py`

| Línea | Qué es |
|---|---|
| [9](../app/kv/entrar.kv#L9) | PANTALLA ENTRAR (inicio de sesión): aparece al abrir la app si nadie ha entrado. |
| [48](../app/kv/entrar.kv#L48) | CAMPO «Usuario». |
| [61](../app/kv/entrar.kv#L61) | CAMPO «Contraseña». |
| [70](../app/kv/entrar.kv#L70) | BOTÓN «Mostrar / Ocultar contraseña». |
| [88](../app/kv/entrar.kv#L88) | BOTÓN «Entrar»: revisa el usuario y la contraseña. |
| [95](../app/kv/entrar.kv#L95) | BOTÓN «Crear una cuenta»: va a la pantalla de registro. |
| [104](../app/kv/entrar.kv#L104) | BOTÓN «Seguir sin cuenta (solo mirar)»: entra a la lista sin cuenta. |

## Pantalla Crear cuenta

Interfaz: [`app/kv/registro.kv`](../app/kv/registro.kv) · Lógica: `app/screens/registro.py`

| Línea | Qué es |
|---|---|
| [1](../app/kv/registro.kv#L1) | PANTALLA CREAR CUENTA (registro). La validación está en app/cuentas.py (validar_registro). |
| [11](../app/kv/registro.kv#L11) | BOTÓN «←»: vuelve a Entrar. |
| [30](../app/kv/registro.kv#L30) | CAMPO «Tu nombre». |
| [41](../app/kv/registro.kv#L41) | CAMPO «Nombre de usuario». |
| [52](../app/kv/registro.kv#L52) | CAMPO «Contraseña». |
| [63](../app/kv/registro.kv#L63) | CAMPO «Repite la contraseña». |
| [81](../app/kv/registro.kv#L81) | BOTÓN «Crear mi cuenta». |
| [89](../app/kv/registro.kv#L89) | BOTÓN «Ya tengo cuenta»: vuelve a Entrar. |

## Pantalla Lista (inicio)

Interfaz: [`app/kv/lista.kv`](../app/kv/lista.kv) · Lógica: `app/screens/lista.py`

| Línea | Qué es |
|---|---|
| [1](../app/kv/lista.kv#L1) | PANTALLA LISTA (inicio): es la primera que aparece al entrar. |
| [24](../app/kv/lista.kv#L24) | AVISO PDA «Hoy: Alerta ambiental»: la franja de color (su diseño está en kv/pda.kv). |
| [36](../app/kv/lista.kv#L36) | BOTÓN «Con stock» (filtro): muestra solo los puntos donde hay. |
| [43](../app/kv/lista.kv#L43) | BOTÓN «Todos» (filtro): muestra todos los puntos, con y sin stock. |
| [50](../app/kv/lista.kv#L50) | BOTÓN de sector («Todo Temuco»): abre el menú para elegir un sector. |
| [60](../app/kv/lista.kv#L60) | LISTA DE PUNTOS: lista.py agrega aquí una tarjeta (PuntoCard) por cada punto. |
| [71](../app/kv/lista.kv#L71) | BOTÓN «Publicar un punto»: abre el formulario para publicar (pantalla 'form'). |

## Aviso y pantalla del PDA

Interfaz: [`app/kv/pda.kv`](../app/kv/pda.kv) · Lógica: `app/screens/pda.py`

| Línea | Qué es |
|---|---|
| [2](../app/kv/pda.kv#L2) | AVISO PDA: la franja de color con el episodio del día («Hoy: Alerta ambiental»). |
| [42](../app/kv/pda.kv#L42) | PANTALLA CALIDAD DEL AIRE HOY (PDA). Los textos de cada nivel están en app/pda.py. |
| [52](../app/kv/pda.kv#L52) | BOTÓN «←»: vuelve a la lista. |
| [68](../app/kv/pda.kv#L68) | TARJETA GRANDE con el episodio de hoy (el color cambia según el nivel). |
| [113](../app/kv/pda.kv#L113) | TARJETA «¿Qué hago hoy?»: screens/pda.py la llena con los consejos del nivel. |
| [128](../app/kv/pda.kv#L128) | TARJETA «Los niveles del PDA»: qué significa Alerta, Preemergencia y Emergencia. |
| [155](../app/kv/pda.kv#L155) | BOTÓN «Ver pronóstico oficial»: abre airechile.mma.gob.cl en el navegador. |
| [162](../app/kv/pda.kv#L162) | BOTÓN «Simular otro día (demo)»: cambia el episodio para mostrarlo en la presentación. |

## Tarjetas de la lista y de las opiniones

Interfaz: [`app/kv/widgets.kv`](../app/kv/widgets.kv) · Lógica: `app/screens/lista.py y detalle.py`

| Línea | Qué es |
|---|---|
| [52](../app/kv/widgets.kv#L52) | TARJETA DE PUNTO (PuntoCard): cada tarjeta de la Lista. Al tocarla se abre el detalle. |
| [295](../app/kv/widgets.kv#L295) | TARJETA DE OPINIÓN (OpinionCard): autor, nivel, estrellas, texto y votos. |
| [353](../app/kv/widgets.kv#L353) | BOTÓN «Útil» (pulgar arriba): vota que la opinión sirve. La propia no se puede votar. |
| [363](../app/kv/widgets.kv#L363) | BOTÓN «No útil» (pulgar abajo). |

## Pantalla Detalle

Interfaz: [`app/kv/detalle.kv`](../app/kv/detalle.kv) · Lógica: `app/screens/detalle.py`

| Línea | Qué es |
|---|---|
| [11](../app/kv/detalle.kv#L11) | PANTALLA DETALLE: se abre al tocar un punto en la lista o el botón «Detalle» del mapa. |
| [22](../app/kv/detalle.kv#L22) | BOTÓN «←» (volver): regresa a la pantalla anterior. |
| [60](../app/kv/detalle.kv#L60) | TARJETA DE ESTADO: verde (hay), roja (sin stock) o ámbar (dato viejo). |
| [97](../app/kv/detalle.kv#L97) | TARJETA DE CONFIABILIDAD: estrellas de 0 a 5 (el cálculo está en app/confianza.py). |
| [135](../app/kv/detalle.kv#L135) | BOTÓN «¿Cómo se calcula?»: explica la fórmula de las estrellas. |
| [144](../app/kv/detalle.kv#L144) | TARJETA de datos: dirección, distancia, horario y quién lo vio. |
| [166](../app/kv/detalle.kv#L166) | BOTÓN «Cómo llegar» del detalle: va al mapa y pregunta si vas a pie o en auto. |
| [179](../app/kv/detalle.kv#L179) | BOTÓN «Ver en el mapa»: muestra el punto en el mapa. |
| [196](../app/kv/detalle.kv#L196) | BOTÓN «Sigue habiendo» (verde): confirma que todavía hay stock. |
| [213](../app/kv/detalle.kv#L213) | BOTÓN «Ya no hay» (rojo): avisa que se acabó. |
| [235](../app/kv/detalle.kv#L235) | LISTA DE OPINIONES: detalle.py agrega aquí una tarjeta (OpinionCard) por opinión. |
| [243](../app/kv/detalle.kv#L243) | TARJETA «Deja tu opinión»: solo se ve si entraste con tu cuenta. |
| [258](../app/kv/detalle.kv#L258) | ESTRELLAS PARA CALIFICAR (1 a 5): al tocar una estrella cambia 'valor'. |
| [279](../app/kv/detalle.kv#L279) | BOTÓN «Sí había» de la opinión (opcional, también suma un reporte). |
| [285](../app/kv/detalle.kv#L285) | BOTÓN «No había» de la opinión. |
| [291](../app/kv/detalle.kv#L291) | CAMPO de texto de la opinión. |
| [313](../app/kv/detalle.kv#L313) | BOTÓN «Publicar opinión»: guarda la opinión (publicar_opinion en detalle.py). |
| [322](../app/kv/detalle.kv#L322) | TARJETA para quien no tiene cuenta: invita a entrar o a crear una. |
| [338](../app/kv/detalle.kv#L338) | BOTÓN «Entrar» (desde el detalle). |
| [344](../app/kv/detalle.kv#L344) | BOTÓN «Crear cuenta» (desde el detalle). |

## Pantalla Mapa

Interfaz: [`app/kv/mapa.kv`](../app/kv/mapa.kv) · Lógica: `app/screens/mapa.py`

| Línea | Qué es |
|---|---|
| [12](../app/kv/mapa.kv#L12) | PANTALLA MAPA: la pestaña del medio. |
| [15](../app/kv/mapa.kv#L15) | EL MAPA de Temuco (clase MapaPellet en app/mapa.py). |
| [23](../app/kv/mapa.kv#L23) | TARJETA de arriba con el título y los filtros. Se esconde mientras navegas (top: 3). |
| [51](../app/kv/mapa.kv#L51) | BOTÓN «Todos» del mapa: muestra todos los pines. |
| [57](../app/kv/mapa.kv#L57) | BOTÓN «Solo con stock» del mapa: deja solo los pines donde hay. |
| [72](../app/kv/mapa.kv#L72) | BANNER AZUL de navegación: metros y minutos que faltan. |
| [119](../app/kv/mapa.kv#L119) | BOTÓN «+»: acercar el mapa (zoom). |
| [123](../app/kv/mapa.kv#L123) | BOTÓN «−»: alejar el mapa. |
| [127](../app/kv/mapa.kv#L127) | BOTÓN «centrar en mí» (la mira): vuelve el mapa a tu ubicación. |
| [133](../app/kv/mapa.kv#L133) | TARJETA DEL PUNTO SELECCIONADO: aparece abajo al tocar un pin. |
| [152](../app/kv/mapa.kv#L152) | BOTÓN «X»: cierra la tarjeta del punto. |
| [186](../app/kv/mapa.kv#L186) | BOTÓN «Detalle»: abre la pantalla de detalle del punto. |
| [194](../app/kv/mapa.kv#L194) | BOTÓN «Cómo llegar» (azul): pregunta si vas caminando o en auto |
| [212](../app/kv/mapa.kv#L212) | TARJETA DE NAVEGACIÓN: aparece abajo mientras vas a un punto. |
| [233](../app/kv/mapa.kv#L233) | BOTÓN «Simular caminata» / «Simular viaje» / «Pausar»: mueve tu punto por la ruta. |
| [244](../app/kv/mapa.kv#L244) | BOTÓN «Terminar»: corta la navegación y borra la ruta. |

## Pantalla Publicar (formulario)

Interfaz: [`app/kv/formulario.kv`](../app/kv/formulario.kv) · Lógica: `app/screens/formulario.py`

| Línea | Qué es |
|---|---|
| [8](../app/kv/formulario.kv#L8) | PANTALLA PUBLICAR (formulario): se abre con «Publicar un punto» en la Lista. |
| [19](../app/kv/formulario.kv#L19) | BOTÓN «X» (cerrar): cancela y vuelve a la lista. |
| [38](../app/kv/formulario.kv#L38) | CAMPO «Local o persona que vende». |
| [54](../app/kv/formulario.kv#L54) | BOTÓN «Tienda o bencinera» (tipo de punto). |
| [62](../app/kv/formulario.kv#L62) | BOTÓN «Particular»: alguien que vende en su casa. |
| [76](../app/kv/formulario.kv#L76) | BOTÓN «Pellet» (qué vende). |
| [82](../app/kv/formulario.kv#L82) | BOTÓN «Leña seca» (qué vende). |
| [88](../app/kv/formulario.kv#L88) | BOTÓN «Ambos»: pellet y leña. |
| [97](../app/kv/formulario.kv#L97) | BOTÓN de sector: abre el menú con los sectores de Temuco. |
| [106](../app/kv/formulario.kv#L106) | CAMPO «Dirección exacta». |
| [119](../app/kv/formulario.kv#L119) | BOTÓN «Ubicación en el mapa»: abre la pantalla para marcar el lugar (kv/elegir.kv). |
| [148](../app/kv/formulario.kv#L148) | BOTÓN «Sí había»: había stock cuando fuiste. |
| [164](../app/kv/formulario.kv#L164) | BOTÓN «No había»: oculta los campos de sacos y precio. |
| [190](../app/kv/formulario.kv#L190) | CAMPO «Sacos que quedaban» (solo números). |
| [201](../app/kv/formulario.kv#L201) | CAMPO «Precio por saco» (solo números). |
| [216](../app/kv/formulario.kv#L216) | CAMPO «Hora en que pasaste» (formato HH:MM). |
| [226](../app/kv/formulario.kv#L226) | BOTÓN «Ahora»: pone la hora actual. |
| [239](../app/kv/formulario.kv#L239) | CAMPO «Abre» (hora de apertura). |
| [245](../app/kv/formulario.kv#L245) | CAMPO «Cierra» (hora de cierre). |
| [263](../app/kv/formulario.kv#L263) | BOTÓN «Publicar»: valida todo y muestra el resumen antes de publicar (revisar). |

## Pantalla Marca dónde está

Interfaz: [`app/kv/elegir.kv`](../app/kv/elegir.kv) · Lógica: `app/screens/elegir.py`

| Línea | Qué es |
|---|---|
| [1](../app/kv/elegir.kv#L1) | PANTALLA «Marca dónde está»: se abre desde el formulario. |
| [12](../app/kv/elegir.kv#L12) | BOTÓN «←»: vuelve al formulario. |
| [46](../app/kv/elegir.kv#L46) | BOTÓN «Estoy aquí»: centra el mapa en tu ubicación. |
| [54](../app/kv/elegir.kv#L54) | BOTÓN «Usar este lugar»: guarda el centro del mapa como ubicación del punto. |

## Pantalla Perfil

Interfaz: [`app/kv/perfil.kv`](../app/kv/perfil.kv) · Lógica: `app/screens/perfil.py`

| Línea | Qué es |
|---|---|
| [24](../app/kv/perfil.kv#L24) | PANTALLA PERFIL: la tercera pestaña. La lógica está en screens/perfil.py. |
| [60](../app/kv/perfil.kv#L60) | AVATAR: la inicial de tu nombre dentro de un círculo. |
| [104](../app/kv/perfil.kv#L104) | TARJETA DE REPUTACIÓN: tus puntos y la barra hasta el siguiente nivel. |
| [140](../app/kv/perfil.kv#L140) | TARJETA «Cómo ganar reputación». |
| [164](../app/kv/perfil.kv#L164) | BOTÓN «¿Tienes dudas?»: abre la pantalla de Ayuda. |
| [192](../app/kv/perfil.kv#L192) | BOTÓN «Cerrar sesión». |
| [225](../app/kv/perfil.kv#L225) | BOTÓN «Entrar» (perfil sin cuenta). |
| [232](../app/kv/perfil.kv#L232) | BOTÓN «Crear una cuenta» (perfil sin cuenta). |
| [241](../app/kv/perfil.kv#L241) | BOTÓN «¿Tienes dudas?» (Ayuda, también sin cuenta). |

## Pantalla Ayuda

Interfaz: [`app/kv/ayuda.kv`](../app/kv/ayuda.kv) · Lógica: `—`

| Línea | Qué es |
|---|---|
| [1](../app/kv/ayuda.kv#L1) | PANTALLA AYUDA: se abre desde Perfil › «¿Tienes dudas?». Son solo textos explicativos. |
| [11](../app/kv/ayuda.kv#L11) | BOTÓN «←»: vuelve al perfil. |
| [29](../app/kv/ayuda.kv#L29) | TARJETA «Qué significa cada color». |
| [53](../app/kv/ayuda.kv#L53) | TARJETA «En 4 pasos». |
| [77](../app/kv/ayuda.kv#L77) | TARJETA «¿Puedo confiar en el dato?». |
| [101](../app/kv/ayuda.kv#L101) | TARJETA «Calidad del aire (PDA)». |
| [119](../app/kv/ayuda.kv#L119) | TARJETA «En el computador (demo)». |
| [137](../app/kv/ayuda.kv#L137) | BOTÓN «Entendido»: vuelve al perfil. |

## Otros archivos de lógica (app/)

| Archivo | Qué hace |
|---|---|
| `main.py` | Punto de partida: `python main.py` abre la app |
| `app/pelletapp.py` | La app completa: crea las pantallas, guarda los datos y maneja la navegación (`ir_a`) |
| `app/cuentas.py` | Crear cuenta, entrar, contraseñas con hash y niveles de reputación |
| `app/confianza.py` | Cálculo de las estrellas de confiabilidad |
| `app/pda.py` | Textos, colores y consejos de cada nivel del PDA |
| `app/mapa.py` | El mapa, los pines, el punto azul y la línea de la ruta |
| `app/rutas.py` | Pide la ruta a pie o en auto por internet |
| `app/ubicacion.py` | GPS en el celular o ubicación simulada en el computador |
| `app/geo.py` | Distancias y minutos a pie o en auto |
| `app/utils.py` | Formato de precios, fechas y textos de cada punto |
| `app/data.py` | Los puntos y vecinos de ejemplo |
| `app/config.py` | Configuración: sectores, colores, servidores de mapa y rutas |
| `app/compat.py` | Arreglo de un error de KivyMD 2.0 con las tarjetas |
