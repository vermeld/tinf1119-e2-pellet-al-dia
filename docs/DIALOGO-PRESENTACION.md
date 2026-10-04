# Diálogo para exponer — Pellet al Día

Duración total: **7 a 8 minutos** más 3 preguntas. Los tiempos son aproximados.
Lo que está en *cursiva* es lo que **haces**; el resto es lo que **dices**.
No hay que memorizarlo palabra por palabra: úsalo como guía y dilo con tus palabras.

**Antes de empezar**
- Conecta el computador a internet.
- Abre la app con `python main.py` y recorre un poco el mapa (así queda guardado aunque falle internet).
- Si tenías una sesión abierta, ve a Perfil › «Cerrar sesión» para partir desde Entrar.
- Deja abiertos en VS Code `app/kv/lista.kv` y `app/screens/lista.py`, para mostrarlos en la demo.

---

## Parte 1 · Problema y usuario (1 minuto)

### Diapositiva 1 — Portada (15 s)

> Buenos días. Soy Gabriel Neculman y les voy a presentar **Pellet al Día**, una maqueta funcional hecha en Kivy y KivyMD. Es una app para saber dónde hay pellet, qué tan confiable es ese dato y si hoy hay restricción del Plan de Descontaminación, en Temuco y Padre Las Casas.

### Diapositiva 2 — El problema (45 s)

> Partamos por el problema. En invierno, encontrar pellet es como buscar a ciegas. Una de las personas que consulté, una señora de más de 60 años de Temuco, me contó que necesitó **«unos 7 viajes»** en auto para encontrar pellet. Otra persona, de Padre Las Casas, fue al supermercado, no había, y tuvo que conseguir 3 bolsas por contactos.
>
> Y hay un segundo problema: cuando le pregunté qué sabía de las restricciones del PDA, la respuesta fue simplemente **«Nada»**. A ninguna de las tres personas le llega esa información a tiempo.

---

## Parte 2 · Fundamentación UX/UI (2 a 3 minutos)

### Diapositiva 3 — Cómo investigué (30 s)

> Para investigar armé una pauta de **15 preguntas abiertas**, en cuatro bloques: el hogar, cómo consiguen el combustible, las restricciones del PDA y un cierre. Algo importante: **ninguna pregunta mencionaba una aplicación**, para no influir en lo que me respondían.
>
> La registré en un formulario de Google y la respondieron tres personas de perfiles distintos: un adulto de Padre Las Casas que vive en departamento, una adulta mayor de Temuco y una persona joven que usa leña. Es una muestra pequeña, así que hablo de **tendencias**, no de conclusiones definitivas.

### Diapositiva 4 — Lo que encontré (40 s)

> Encontré tres patrones. **Dos de dos** usuarios de pellet no lo encontraron cuando lo necesitaban: uno en abril y otra en agosto. Y para los dos, eso es justamente lo que más les frustra.
>
> **Tres de tres** no conocen bien el PDA ni se enteran a tiempo. Y **dos de tres** sienten que el precio sube cuando escasea.
>
> La frase que mejor resume lo que necesitan es de la persona 2: quiere *«saber dónde hay de manera sencilla y si realmente queda en ese lugar»*. Esa frase guió casi todo el diseño.

### Diapositiva 5 — De la evidencia al diseño (50 s)

> Esta es la matriz que une lo que dijeron con lo que diseñé.
>
> Como lo que más frustra es no encontrar pellet, la **Lista abre filtrada en «Con stock»** y ordenada por cercanía.
>
> Como quieren saber si realmente queda, cada punto dice **hace cuánto se vio**, se puede confirmar con «Sigue habiendo» o «Ya no hay», y tiene una **confiabilidad en estrellas**.
>
> Para los 7 viajes en auto está **«Cómo llegar»**, a pie o en auto, directo al punto.
>
> Como nadie se entera del PDA, puse el **aviso del día en la primera pantalla**.
>
> Y como pidieron precios accesibles y más zonas de venta, el **precio está a la vista** y **cualquier vecino puede publicar** un punto.

### Diapositiva 6 — Estructura (25 s)

> La app tiene solo **tres pestañas**, en el orden en que se usan. Primero la **Lista**, que es el inicio: arriba el aviso del PDA y abajo los puntos más cercanos. Elegí una lista y no el mapa como inicio porque se lee de arriba abajo, sin tener que manejar un mapa, pensando en la persona de más edad. Al centro está el **Mapa**, y al final el **Perfil**, donde está la reputación y la ayuda.

### Diapositiva 7 — Confiabilidad (25 s)

> Para responder a «si realmente queda», cada dato muestra su confiabilidad de **0 a 5 estrellas**. Se calcula con qué tan reciente es el reporte, cuántos vecinos lo confirman y la reputación de quien lo reportó. Son **amarillas con 5, verdes en el medio y rojas con una y media o menos**, siempre con el número al lado.
>
> Para eso hay cuentas y opiniones con votos «Útil» o «No útil». Quiero ser honesto: las cuentas son una **decisión derivada**. Nadie me las pidió, pero para confiar en un dato hay que saber quién lo dio.

### Diapositiva 8 — Llegar y estar informado (20 s)

> «Cómo llegar» pregunta si vas **caminando o en auto**, muestra la ruta y los minutos que faltan, y tu punto avanza mientras te mueves. Y la pantalla **Calidad del aire hoy** explica qué hacer según el episodio, y aclara que la restricción rige en **todo Temuco y Padre Las Casas**, porque una persona creía que en su sector no había restricciones.

---

## Parte 3 · Demo en vivo (2 a 3 minutos)

### Diapositiva 9 — Demo en vivo

> Ahora les muestro la app funcionando.

1. *Crear cuenta. Escribe una contraseña corta (ej. «123») y presiona «Crear mi cuenta».*
   > Primero creo una cuenta. Si pongo una contraseña muy corta, la app me avisa con un mensaje simple. *(Corrige la contraseña y crea la cuenta.)* Ahora sí, y la app me lleva directo a la Lista.

2. *Toca la franja «Hoy: Alerta ambiental».*
   > Arriba está el aviso del PDA. Si lo toco, veo qué hacer hoy. *(Presiona «Simular otro día (demo)».)* En la maqueta este dato es de ejemplo, así que con este botón simulo otro día: ahora es Preemergencia y cambian el color y los consejos.

3. *Vuelve con «←». Muestra las tarjetas.*
   > En la Lista cada punto muestra qué vende, el precio, el estado y la confiabilidad en estrellas. Por ejemplo, esta ferretería tiene 5 estrellas amarillas porque varios vecinos lo confirmaron hace poco.

4. *Ve a la pestaña «Mapa». Toca el pin de Leñería Don Juan › «Cómo llegar» › «En auto» › «Simular viaje».*
   > En el mapa toco un punto y presiono «Cómo llegar». Me pregunta cómo voy a ir; elijo en auto, y la ruta respeta el sentido de las calles. Como el computador no tiene GPS, simulo el viaje: el punto azul avanza y bajan los metros. *(Espera «¡Llegaste!».)* Al llegar, la app me pregunta si había stock. *(Responde «Sí había».)* Así el dato se mantiene al día.

5. *En la Lista, toca un punto › baja hasta las opiniones › marca «Útil» en una › escribe tu opinión.*
   > En el detalle puedo votar si una opinión me sirvió. Eso le sube la reputación a quien la escribió. También puedo dejar mi propia opinión con estrellas.

6. *En la Lista, presiona «Publicar un punto» › presiona «Publicar» sin llenar nada.*
   > Si alguien encuentra un punto nuevo, lo publica aquí. Si intento publicar vacío, la validación me marca qué falta. *(Llena el nombre, la dirección y la ubicación en el mapa, y publica.)*

7. *Muestra en VS Code `app/kv/lista.kv` junto a `app/screens/lista.py`.*
   > Por último, el código. La interfaz está en archivos **.kv** y la lógica en **.py**. Por ejemplo, aquí está el botón «Publicar un punto» en el .kv, y su `on_release` llama a la función que cambia de pantalla.

**Si falla internet:** di «Sin internet el mapa no carga, pero la lista, el detalle y el formulario funcionan igual», y sigue con los pasos 3, 5 y 6.

### Diapositiva 10 — Cómo está construida (20 s)

> En resumen técnico: la interfaz está en **12 archivos .kv** y la lógica en Python, con una clase por pantalla. La navegación usa **MDScreenManager** con 10 pantallas y una barra inferior. Uso componentes de **KivyMD con Material Design**: barra superior, tarjetas, botones, campos de texto, diálogos y mensajes. Y el mapa usa **mapview** con rutas de OSRM.

---

## Parte 4 · Cierre (1 minuto)

### Diapositiva 11 — Para quién y con qué límites (25 s)

> Pensé la app para quien más se esfuerza: botones grandes, lenguaje simple, el color siempre acompañado de texto, y se puede usar sin cuenta.
>
> Y también quiero ser honesto con los límites: consulté solo a 3 personas. No les pregunté si estarían dispuestas a reportar stock, así que eso es un **supuesto** que hay que validar. Tampoco entrevisté a vendedores. Y la opción de leña seca tiene respaldo débil, porque la persona que usa leña no tiene problemas para conseguirla.

### Diapositiva 12 — Cierre (30 s)

> La mayor dificultad fue integrar un mapa real con KivyMD 2.0, calcular cómo avanzas sobre la ruta y resolver un error de la librería con las tarjetas.
>
> Lo que más aprendí: yo partí creyendo que el problema era la contaminación por la leña. La investigación me mostró que lo que más les complica a las personas es **encontrar pellet a tiempo y enterarse de las restricciones**. Diseñar desde la evidencia y no desde mi idea inicial cambió la app.
>
> Como próximo paso: tomar el PDA del pronóstico oficial con notificaciones, tener un servidor para que todos vean los mismos datos, y entrevistar a más personas, incluidos vendedores.

### Diapositiva 13 — Gracias (5 s)

> Muchas gracias. Quedo atento a sus preguntas.

---

## Preguntas probables y cómo responder

Para encontrar cualquier botón en el código: **Ctrl+Shift+F** en VS Code y busca `BOTÓN «` + el nombre. La lista completa está en [GUIA-DEL-CODIGO.md](GUIA-DEL-CODIGO.md).

**«¿Dónde está el botón del mapa?»**
> *(Busca `PESTAÑA «Mapa»`.)* Está en `kv/raiz.kv`, en la barra de abajo. Es un `ItemNav` con `pantalla: 'mapa'`. Al tocarlo se llama a `app.al_cambiar_pestana()`, que usa `ir_a()` en `pelletapp.py` para cambiar de pantalla en el ScreenManager.

**«¿Qué hace el botón "Cómo llegar"?»**
> *(Busca `BOTÓN «Cómo llegar»`.)* En `kv/mapa.kv` su `on_release` llama a `root.elegir_modo()`, que está en `screens/mapa.py`. Esa función abre el diálogo «¿Cómo vas a ir?», y después `navegar_a()` le pide la ruta al servidor con `rutas.py`.

**«¿Cómo se conecta el .kv con el .py?»**
> El .kv tiene una regla con el nombre de la clase, por ejemplo `<PantallaLista>:`, que se aplica a la clase `PantallaLista` del .py. Desde el .kv llamo funciones con `root.algo()` (la pantalla) o `app.algo()` (la app). Desde el .py accedo a los widgets con `self.ids`. Y las propiedades de Kivy, como `solo_con`, actualizan la interfaz solas cuando cambian.

**«¿Cómo funciona la navegación?»**
> Todas las pantallas están dentro de un `MDScreenManager` en `kv/raiz.kv`. La función `ir_a()` de `pelletapp.py` cambia `sm.current` a la pantalla que quiero, y la transición se desliza a la izquierda o a la derecha según el orden de las pestañas.

**«¿Dónde está la validación?»**
> *(Busca `VALIDACIÓN`.)* La del formulario está en `validar()` de `screens/formulario.py`: revisa los campos obligatorios, que el precio sea un número razonable y que las horas estén en formato HH:MM. La del registro está en `validar_registro()` de `cuentas.py`. Si algo falla, el campo se marca en rojo y aparece un mensaje simple.

**«¿Cómo se calculan las estrellas?»**
> *(Busca `CÁLCULO DE LAS ESTRELLAS`.)* En `confianza.py`: 40 % qué tan reciente es el reporte, 40 % cuántos reportes lo respaldan y 20 % la reputación de quien reportó. Eso da un puntaje de 0 a 1, que se multiplica por 5 y se redondea a la media estrella.

**«¿Cómo guardas las contraseñas?»**
> Nunca en texto plano. En `cuentas.py` se guarda un hash PBKDF2 con una "sal" aleatoria por usuario. Al entrar, se calcula el hash de lo que escribiste y se compara con el guardado.

**«¿El PDA es real?»**
> En la maqueta es un dato de ejemplo, por eso está el botón «Simular otro día». En la versión final se tomaría del pronóstico oficial de airechile.mma.gob.cl y llegaría como notificación, pero las notificaciones quedan fuera del alcance de esta evaluación.

**«La pauta dice que las cuentas están fuera del alcance. ¿Por qué las agregaste?»**
> No se exigen ni se penalizan. Las agregué porque la persona 2 pidió saber «si realmente queda en ese lugar», y para confiar en un dato hay que saber quién lo dio. Las cuentas permiten que cada reporte pese según la reputación de quien lo hizo.

**«¿Y si alguien miente?»**
> Su opinión recibe votos «No útil», baja su reputación y sus reportes pesan menos. Además, un solo reporte nunca da 5 estrellas: se necesitan varios vecinos que lo confirmen.

**«¿Usaste inteligencia artificial?»**
> Sí, y lo declaré en el README, como pide la pauta. La usé como apoyo para programar y documentar. La investigación, las entrevistas, las ideas y las decisiones de qué incluir son mías, y puedo explicar cómo funciona cada parte.
