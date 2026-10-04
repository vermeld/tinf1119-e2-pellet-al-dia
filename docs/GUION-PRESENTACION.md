# Guion de la presentación E2 (7 a 8 min + 3 preguntas)

## 1. Problema y usuario (1 min), criterio A
- **Problema:** en invierno cuesta encontrar pellet y nadie se entera a tiempo de las restricciones del PDA.
- **Evidencia:** las 2 personas que usan pellet tuvieron problemas para encontrarlo. Una necesitó «Unos 7 viajes» en auto; la otra: «En el supermercado no habin asique me tuve que conseguir 3 bolsas».
- **Usuario:** familias de Temuco y Padre Las Casas que calefaccionan con pellet o leña, sobre todo con niños, adultos mayores o personas con problemas respiratorios.
- **La solución en una frase:** *Pellet al Día* muestra dónde hay pellet o leña seca **ahora**, qué tan confiable es el dato, cómo llegar, y si hoy hay restricción del PDA.

## 2. Fundamentación UX/UI (2 a 3 min), criterios A y D2
- **Metodología:** pauta de entrevista de 15 preguntas abiertas, registrada en un formulario de Google el 04/10/2026, a 3 personas: 45–59 años de Padre Las Casas, 60 o más de Temuco y 18–29 de Temuco.
- **Recorre 4 filas de la matriz.** Para cada una: lo que dijeron → lo que diseñé.
  1. «No encontrar Pelet» es lo que más frustra (2 de 2 usuarios de pellet) → la **Lista** abre filtrada en *Con stock* y ordenada por cercanía.
  2. «Saber dónde hay de manera sencilla y si realmente queda en ese lugar» → **«Visto hace X»**, «Sigue habiendo / Ya no hay» y **confiabilidad en estrellas**.
  3. «Unos 7 viajes» en auto → **«Cómo llegar» a pie o en auto**, directo al punto.
  4. Ninguna de las 3 personas conoce el PDA ni se entera a tiempo (P1: «Nada»; P3: «Donde yo vivo no tengo restricciones») → **aviso del PDA arriba de la Lista**, con la aclaración de que rige en todo Temuco y Padre Las Casas.
- **Accesibilidad:** la persona de 60 o más es la que más se esfuerza → botones grandes, lenguaje simple, solo 3 pestañas y Ayuda en el Perfil.
- **Sé honesto con la limitación:** son 3 personas, así que los resultados muestran una tendencia. Como próximo paso queda entrevistar a vendedores.

## 3. Demo en vivo (2 a 3 min), criterios B, C y D3
**Antes de empezar:** conéctate a internet, abre `python main.py` y recorre el
mapa un poco para que las teselas queden en caché. Si ya tenías una sesión
abierta, ve a Perfil y presiona «Cerrar sesión» para partir desde Entrar.

0. **Crear cuenta**: primero pon una contraseña corta para mostrar la validación, después crea la cuenta de verdad. La app abre en la **Lista**.
   - Toca el aviso **«Hoy: Alerta ambiental»**: muestra qué hacer y que rige en todo Temuco y Padre Las Casas. Presiona «Simular otro día (demo)» para ver la Preemergencia.
   - De vuelta en la Lista, muestra las estrellas de confiabilidad (amarillas, verdes y rojas) y qué vende cada punto (pellet o leña seca). Luego ve a la pestaña **Mapa**.
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
- Próximo paso: obtener el PDA del pronóstico oficial y avisar con notificaciones, un servidor compartido para que todos vean los mismos datos, compilar el APK con Buildozer y entrevistar a más personas y a vendedores.

## Preguntas probables (prepárate)
- **¿El PDA es real?** En la maqueta, el episodio es un dato de ejemplo (se cambia con «Simular otro día»). La versión final lo tomaría del pronóstico oficial (airechile.mma.gob.cl) y avisaría con notificaciones, que están fuera del alcance de la E2.
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
- **Pero la pauta dice que la autenticación está fuera de alcance.** No se exige ni se penaliza. La agregué porque P2 pidió saber «si realmente queda en ese lugar». Para confiar en un dato hay que saber quién lo dio, y las cuentas permiten pesar cada reporte según la reputación de su autor.
