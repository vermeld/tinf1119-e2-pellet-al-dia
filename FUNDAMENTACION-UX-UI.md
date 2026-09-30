# Fundamentación UX/UI de Ubica Pellet

> ⚠️ **PLANTILLA POR COMPLETAR.** Lo que aparece entre `[corchetes]` debe
> reemplazarse con los datos **reales** de tus entrevistas y encuestas. Las
> decisiones de diseño ya están implementadas en la app; falta respaldarlas con
> evidencia (criterios A1 y A2 de la pauta: 15 pts). Si algún hallazgo no
> coincide con lo que dijeron tus usuarios, borra esa fila o cámbiala.

## a) Metodología de investigación

| Instrumento | Cantidad | A quiénes | Cómo y cuándo |
|---|---|---|---|
| Entrevista semiestructurada | [N] | [ej.: usuarios de estufa a pellet de Temuco / socio comunitario X] | [presencial/online, fecha, duración aprox.] |
| Encuesta | [N respuestas] | [perfil] | [Google Forms, difundida por …, fecha] |

Socio comunitario: [nombre y breve descripción].
Preguntas clave del instrumento: [3 o 4 preguntas principales].

## b) Resultados principales

| # | Hallazgo | Evidencia |
|---|---|---|
| H1 | Se pierde tiempo y dinero recorriendo locales sin stock | [cita: "…" — Entrevistado/a 2] · [X % dice haber ido a un local sin pellet] |
| H2 | Lo que más importa es **dónde hay ahora**, más que el precio | [% que prioriza disponibilidad sobre precio] |
| H3 | La información que circula (WhatsApp/Facebook) queda vieja rápido | [cita] |
| H4 | También venden particulares, no solo tiendas | [recuento / cita] |
| H5 | El precio por saco varía mucho entre puntos | [rango de precios reportados] |
| H6 | Parte de los usuarios tiene poca familiaridad con apps / son mayores | [% mayores de 50, o cita] |
| H7 | Desconfían de datos de desconocidos | [cita] |
| H8 | Buscan pellet **cerca de su casa** y muchos se mueven a pie o en micro | [% que va a pie / cita] |
| H9 | Cuesta ubicar direcciones de vendedores particulares (pasajes, casas) | [cita] |
| H10 | Quieren saber **quién** dio el dato y si esa persona es confiable | [cita / %] |
| H11 | Valoran las **opiniones** de otros compradores (atención, calidad, precio) | [% que lee reseñas antes de comprar] |

## c) Matriz hallazgo → decisión de diseño

| Hallazgo | Decisión en la interfaz | Dónde está en la app | Por qué |
|---|---|---|---|
| H1, H2, H8 | La pantalla de inicio es la **Lista**, ordenada por cercanía; el **mapa de Temuco** con pines de colores es la segunda pestaña | `lista.kv`, `mapa.kv` | Primero se responde «dónde hay» en un formato fácil de leer; el mapa sirve para ubicar y llegar |
| H8, H9 | Botón **«Cómo llegar»**, que pregunta **«¿Caminando o en auto?»**: ruta por veredas o respetando el sentido de las calles, con metros y minutos que faltan | `mapa.py → elegir_modo()`, `rutas.py` | Resuelve el «¿cómo llego?», sobre todo a casas en pasajes. Los sacos de 15 kg pesan, y muchos van en auto a comprar varios [dato de tu encuesta] |
| H6 | **Mapa limpio**: solo calles y sus nombres, sin números de casas ni íconos de comercios | `config.TILES_URL` | Menos ruido visual, y la ruta y los pines se distinguen mejor |
| H8 | **Tu punto avanza mientras caminas** y la parte recorrida se pinta en gris | `ubicacion.py`, `RutaLayer` | Es el mismo modelo mental de Google Maps, que el usuario ya conoce |
| H3, H7 | Al llegar, la app pregunta **«¿Había pellet?»** | `mapa.py → _llegar()` | Consigue confirmaciones justo cuando el dato es más confiable |
| H8 | La lista se ordena **por cercanía** y cada punto muestra «a 850 m» | `lista.py` | Lo cercano es lo que realmente sirve |
| H2 | Cada tarjeta muestra el **estado de stock en negrita, con ícono y color** justo debajo del nombre | `PuntoCard` en `widgets.kv` | Jerarquía visual: el estado se lee antes que la dirección |
| H3 | Cada dato dice **«Visto hace X min»**. Pasadas 6 horas se pone ámbar y dice «Puede que ya no quede» | `utils.describir()`, `config.HORAS_PARA_DUDAR` | El usuario sabe cuánto confiar en el dato |
| H3, H7 | Botones **«Sigue habiendo» / «Ya no hay»** en el detalle, más el contador de confirmaciones | `detalle.kv`, `app.confirmar()` | Otros vecinos validan el dato, lo que genera confianza |
| H4 | En el formulario se elige el tipo: **Tienda o bencinera / Particular** | `formulario.kv` | Refleja los dos tipos de vendedor que existen |
| H5 | Se muestra el **precio por saco de 15 kg** arriba a la derecha de la tarjeta | `PuntoCard` | Permite comparar de un vistazo |
| H1 | **Filtro por sector** de Temuco (Centro, Amanecer, Labranza…) con `MDDropdownMenu` | `lista.kv` | La gente piensa en su barrio, no en coordenadas |
| H7, H10 | **Cuentas de usuario**: publicar, reportar y opinar requieren entrar; se muestra quién hizo cada reporte | `entrar.kv`, `registro.kv`, `app.requiere_cuenta()` | Un dato con nombre es más confiable que uno anónimo |
| H7, H10 | **Confiabilidad en estrellas (0 a 5, con medias)**: amarillas con 5, verdes de 2 a 4½ y rojas con 1½ o menos. Aparece en el mapa, la lista y el detalle, con «¿Cómo se calcula?» | `confianza.py`, `EstrellasConf`, `detalle.kv` | Las estrellas se entienden sin saber de porcentajes, y el color resume el nivel de un vistazo |
| H10 | **Reputación y niveles** (Nuevo, Confiable, Experto): los reportes de usuarios con más reputación pesan más | `cuentas.py`, `perfil.kv` | Premia a quien aporta bien y reduce el peso de los datos falsos |
| H11 | **Opiniones con estrellas** y votos **Útil / No útil**. Las más útiles se muestran primero | `OpinionCard`, `detalle.py` | Es el mismo modelo de las tiendas de apps y de Google Maps, que el usuario ya conoce |
| H6 | Opción **«Seguir sin cuenta (solo mirar)»** | `entrar.kv` | Quien solo quiere consultar no se topa con una barrera |
| H9 | Para publicar se **marca el lugar moviendo el mapa bajo un pin fijo** | `elegir.kv` | Es más fácil que escribir coordenadas y más preciso que solo la dirección |
| H6 | Hay una pantalla de **Ayuda** con los colores explicados y 4 pasos | `ayuda.kv` | Sirve para quien usa la app por primera vez |
| H6 | **Diálogo de confirmación** antes de publicar o cambiar un dato, y **Snackbar** de éxito | `formulario.py`, `detalle.py` | Evita errores y da feedback claro |
| H6 | Validación con **mensajes en lenguaje simple** («Falta la dirección…»), y el campo con error se marca en rojo | `formulario.py → validar()` | Se entiende qué corregir sin jerga técnica |

## d) Justificación de la estructura y navegación

La barra inferior tiene solo **3 pestañas, en este orden: Lista · Mapa · Perfil**.

1. **Lista** (inicio y primera pestaña): responde «¿dónde hay pellet cerca de mí?» sin tocar nada. Está ordenada por cercanía, muestra el estado, el precio y la confiabilidad en estrellas, y se lee de arriba abajo, sin tener que manejar un mapa. Esto sirve más a quien tiene poca familiaridad con la tecnología (H6). El botón **Publicar un punto** está fijo bajo la lista, porque publicar es la acción que sigue después de revisar.
2. **Mapa** (al centro): ubica los puntos y guía caminando con «Cómo llegar» (H8, H9). Queda al centro para alcanzarlo con el pulgar desde la Lista.
3. **Perfil** (última): nivel y reputación. Ahí está también **«¿Tienes dudas?» → Ayuda**, disponible incluso sin cuenta, donde el usuario la busca cuando la necesita, sin ocupar una pestaña.

Pantallas secundarias: Detalle, Publicar, Elegir ubicación, Ayuda, Entrar y Crear cuenta. Se abren desde las pestañas y tienen su botón de volver en la `MDTopAppBar`.

Tener menos pestañas hace la barra más simple, y cada pestaña tiene un ícono y un texto más grandes. Entre pestañas, la transición se desliza según el orden de la barra.

## e) Diversidad y accesibilidad

- **El color nunca va solo.** El estado siempre combina ícono (✔ / ! / ✖), texto y color. Así funciona para personas con daltonismo.
- **Contraste alto**: el texto blanco va sobre verde, rojo y ámbar oscuros, y el texto principal sobre la superficie clara del tema Material.
- **Texto de los botones de acción a 16 sp en negrita**, y botones de 52 dp de alto: son áreas táctiles grandes.
- **Lenguaje cotidiano** en todos los textos («Sí había», «Ya no hay pellet», «Cuéntanos qué viste»), sin tecnicismos.
- **Ejemplos en cada campo** (helper text) y botón **«Ahora»** para no tener que escribir la hora.
- Los campos de sacos y precio **se ocultan si no había pellet**, así hay menos campos que llenar.
- **La ruta muestra minutos a pie además de metros**: es más fácil de entender para quien no calcula distancias.
- La confiabilidad usa **estrellas**, un formato conocido por cualquier persona que haya visto una reseña, en vez de porcentajes. Además del color, siempre muestra el **número** («3,5») y, en los extremos, la palabra («Excelente», «Poco confiable»). Así no depende solo del color.
- En los errores de inicio de sesión se usa lenguaje simple («Usuario o contraseña incorrectos.») y hay un botón para **mostrar la contraseña** mientras se escribe.
- Si no hay conexión, la ruta se muestra como una **línea recta aproximada** y la app lo avisa, en vez de fallar.
- [Agregar cualquier otro hallazgo de diversidad de tu investigación: edad, conectividad, etc.]
