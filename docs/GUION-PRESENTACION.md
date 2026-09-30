# Guion de la presentación E2 (7 a 8 min + 3 preguntas)

## 1. Problema y usuario (1 min), criterio A
- «En invierno, [X %] de los encuestados de Temuco fue a un local y no había pellet.» *(dato real)*
- Usuario: [perfil del diagnóstico]. Socio comunitario: [nombre].
- La solución en una frase: un mapa colaborativo de Temuco que muestra dónde hay pellet **ahora** y te lleva caminando.

## 2. Fundamentación UX/UI (2 a 3 min), criterios A y D2
- Metodología: [N] entrevistas + [N] encuestas, a [quiénes].
- Recorre 4 filas de la matriz (no todas). Para cada una: **lo que dijeron → lo que diseñé**.
  1. «[cita sobre recorrer locales]» → el inicio es un mapa con pines verde, ámbar y rojo.
  2. «[cita sobre no saber llegar / pasajes]» → «Cómo llegar» con la ruta a pie.
  3. «[cita sobre datos viejos o desconfianza]» → «Visto hace X» y la pregunta «¿Había pellet?» al llegar.
  4. [% de usuarios mayores o poco tecnológicos] → Lista como inicio, barra de solo 3 pestañas, Ayuda en el Perfil, ícono + texto + color.

## 3. Demo en vivo (2 a 3 min), criterios B, C y D3
**Antes de empezar:** conéctate a internet, abre `python main.py` y recorre el
mapa un poco para que las teselas queden en caché. Si ya tenías una sesión
abierta, ve a Perfil y presiona «Cerrar sesión» para partir desde Entrar.

0. **Crear cuenta**: primero pon una contraseña corta para mostrar la validación, después crea la cuenta de verdad. La app abre en la **Lista**. Muestra las estrellas de confiabilidad (amarillas, verdes y rojas) y luego ve a la pestaña **Mapa**.
1. **Mapa**: muestra los pines y el filtro *Solo con stock*. Toca **Leñería Don Juan** o **Ferretería Los Aromos** (están cerca, unos 500 m a 1 km). Aparece la tarjeta con el estado y los minutos a pie.
2. Presiona **Cómo llegar**: la app pregunta **¿Caminando o en auto?**. Elige *En auto*: la ruta respeta el sentido de las calles y el banner muestra los metros y minutos que faltan. Menciona que el mapa solo muestra calles, sin números de casas ni íconos, para que se lea fácil.
3. Presiona **Simular viaje** (o *Simular caminata*, si elegiste a pie): tu punto azul avanza, la ruta recorrida se pone gris y bajan los metros. Explica que en el celular esto lo hace el GPS.
4. Al llegar aparece **«¡Llegaste! ¿Había pellet?»**. Responde *Sí había*: el punto suma una confirmación.
5. Pestaña **Lista**: está ordenada por cercanía y cada punto muestra su **confiabilidad en estrellas**: amarillas con 5 (Ferretería Los Aromos), verdes en el medio y rojas con 1½ o menos (Distribuidora Araucanía, un dato viejo de un usuario nuevo). Toca **Sra. Rosa** (3½ estrellas): hay reportes que se contradicen. Presiona «¿Cómo se calcula?».
   - Baja hasta las opiniones: marca una como **Útil** y otra como **No útil** (así sube o baja la reputación de su autor).
   - Escribe tu opinión con estrellas y marca «Sí había»: la confiabilidad sube.
   - Pestaña **Perfil**: ya tienes puntos de reputación y ves cuántos te faltan para el siguiente nivel. Muestra **«¿Tienes dudas?» → Ayuda**.
6. En la **Lista**, presiona **Publicar un punto**. Presiona Publicar vacío para mostrar la **validación**. Llena los datos, **marca la ubicación en el mapa** y confirma en el diálogo. El punto nuevo aparece en el mapa.
7. Muestra el código en 30 segundos: `kv/mapa.kv` (interfaz) al lado de `screens/mapa.py` (lógica), y `pelletapp.py` con el `MDScreenManager` y la barra inferior.

**Si falla internet:** los puntos, la lista, el detalle y el formulario funcionan
igual. La ruta aparece como una línea recta aproximada.

## 4. Dificultades, aprendizaje y próximo paso (1 min)
- Dificultades: integrar un mapa real (`mapview`) con KivyMD 2.0, calcular el avance sobre la ruta, y un bug de KivyMD con las tarjetas que corregimos en `compat.py`.
- Aprendizaje: separar interfaz y lógica, y diseñar a partir de la evidencia y no del gusto propio.
- Próximo paso: servidor compartido para que todos vean los mismos datos, compilar el APK con Buildozer y probar con usuarios reales en Temuco.

## Preguntas probables (prepárate)
- **¿Por qué solo 3 pestañas y la Lista primero?** Ver la sección d) de la fundamentación: primero se busca, la lista es más fácil de leer que un mapa y menos pestañas simplifican la barra.
- **¿Cómo navegas entre pantallas?** `MDScreenManager` + `MDNavigationBar`. `app.ir_a(nombre)` cambia `sm.current` y marca la pestaña. La dirección del deslizamiento depende del orden de las pestañas.
- **¿Cómo se dibuja la ruta?** `RutaLayer` (un `MapLayer`) convierte cada lat/lon a pixeles con `get_window_xy_from` y dibuja una `Line`. Se redibuja cada vez que mueves el mapa.
- **¿Cómo sabe cuánto falta?** `geo.mas_cercano()` busca el punto de la ruta más cercano a ti, y se suma la distancia de lo que queda (Haversine).
- **¿De dónde sale la ruta?** De servidores OSRM de OpenStreetMap: perfil peatonal o de auto, según lo que elija el usuario. Se piden con `UrlRequest` (asíncrono, no congela la app). Si falla, se usa una línea recta.
- **¿Y el GPS?** En Android se usa `plyer.gps` (`ubicacion.py`). En el PC se simula.
- **¿Cómo se conecta el .kv con el .py?** Con la regla `<PantallaMapa>:`, los `ids` y propiedades Kivy (`navegando`, `sel_id`, `nav_restante`) que el .kv observa.
- **¿Dónde está la validación?** En `PantallaFormulario.validar()`, `cuentas.validar_registro()` y `PantallaDetalle.publicar_opinion()`.
- **¿Cómo guardas las contraseñas?** Nunca en texto plano: se guarda un hash PBKDF2-SHA256 con una sal aleatoria por usuario. Al entrar se compara con `hmac.compare_digest`.
- **¿Cómo se calcula la confiabilidad?** `estrellas = 5 × (0,4 × frescura + 0,4 × respaldo + 0,2 × reputación)`, redondeado a la media estrella (ver `confianza.py`). Amarillo = 5, rojo ≤ 1½, verde el resto.
- **¿Por qué estrellas y no porcentaje?** Todos las entienden sin hacer cálculos, y el color resume el nivel de un vistazo.
- **¿Y si alguien miente?** Su opinión recibe votos «No útil», baja su reputación y sus reportes pesan menos. Además, un solo reporte nunca da 5 estrellas.
- **Pero la pauta dice que la autenticación está fuera de alcance.** No se exige ni se penaliza. La agregamos porque [cita o dato de tu investigación sobre desconfianza en los datos].
