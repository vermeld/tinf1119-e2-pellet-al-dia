# Fundamentación UX/UI de Pellet al Día

Proyecto individual de Gabriel Neculman para TINF1119 Desarrollo Móvil (A+S), evaluación E2.
El detalle completo de la investigación está en la *Plantilla de Investigación de
Necesidades y Problemas Reales* y la pauta de entrevista, ambas en
[docs/investigacion/](docs/investigacion/). Este documento resume esa
evidencia y muestra cómo se tradujo en la interfaz.

## a) Metodología de investigación

| Instrumento | Aplicación | Participantes |
|---|---|---|
| **Pauta de entrevista** de **15 preguntas abiertas** en 4 bloques: contexto del hogar, abastecimiento de combustible, restricciones del PDA y cierre | Se registró mediante un **formulario de Google** el **04/10/2026**. Las preguntas buscan descubrir el problema sin mencionar ninguna aplicación | **3 personas** que calefaccionan con leña o pellet |

| Persona | Comuna | Edad | Calefacción | Quién compra el combustible |
|---|---|---|---|---|
| P1 | Padre Las Casas (departamento) | 45 a 59 | Estufa a pellet | Él mismo |
| P2 | Temuco | 60 o más | Pellet (antes, leña) | Su esposo o su hijo, en auto |
| P3 | Temuco (cerca de un río) | 18 a 29 | Leña | Su padre, a un conocido |

**Limitación:** la muestra es pequeña (3 personas). Los resultados muestran una
tendencia que conviene confirmar con más entrevistas, incluidos vendedores de
pellet y leña, que no alcanzaron a ser entrevistados.

## b) Resultados principales

Las citas son textuales, tal como cada persona escribió su respuesta en el formulario.

| # | Hallazgo | Evidencia |
|---|---|---|
| **H1** | **Cuesta encontrar pellet en pleno invierno** (2 de 3; las 2 que usan pellet) | P1: «En el supermercado no habin asique me tuve que conseguir 3 bolsas». P2: «No había Pelet en ningún lado». Los meses más difíciles: abril (P1) y agosto (P2) |
| **H2** | **Buscar cuesta tiempo y viajes**, en auto en el caso de P2 | P2: «Unos 7 viajes», «Tenemos que ir de manera presencial en auto». P1: «1 horas aprox si voy al super a comprar» |
| **H3** | **La información está dispersa**: cada uno busca por su lado | P1: «En paginas de sectores, supermercados y eso». P2 busca en redes sociales y compra «generalmente en una frutería». P3: «Vemos los precios con los que ofrecen leña en los pasajes» |
| **H4** | **Quieren saber dónde hay, de forma simple y confiable** | P2: «Saber dónde hay de manera sencilla y si realmente queda en ese lugar». P1: «Precios mas accesibles y principalmente mas zonas de ventas» |
| **H5** | **Lo que más frustra es no encontrar pellet** (2 de 2 usuarios de pellet) | P1: «Pillar pelet cuando vamos a mitad de invierno». P2: «No encontrar Pelet» |
| **H6** | **Nadie conoce bien el PDA ni se entera a tiempo** (3 de 3) | Sobre las restricciones: P1 «Nada», P2 «No mucho», P3 «Se que uno puede hacer fuego hasta cierta hora nomás». ¿Le llega a tiempo? P1 «No mucha la verdad», P2 «No». P3 cree que «Donde yo vivo no tengo restricciones» |
| **H7** | **El precio sube cuando escasea** (2 de 3) | P2: «cada vez que hay poco sube mucho». P1: «antes era mucho mas accesibles los precios» |
| **H8** | **Han recibido leña húmeda o de mala calidad** (2 de 3) | P1: «algunas leñas estaban pesimas». P2: «Si, hemos recibido quejas» |
| **H9** | **Hay personas vulnerables al frío y al humo en el hogar** (3 de 3) | P1: «mi hija que lamentablemente se la psa resfriada». P2 es ella misma la más afectada. P3: el humo de los vecinos le duele en los ojos «al punto de casi no poder ver bien» |
| **H10** | **Los perfiles son distintos**: la persona de 60 años o más es la que más se esfuerza, y quien usa leña planifica | P2 hizo unos 7 viajes. P3 compra leña seca en verano: «Somos precavidos con el tema de la leña» |

## c) Matriz hallazgo → decisión de diseño

La columna **Respaldo** distingue qué nace de la evidencia y qué no:
- **Directo:** lo dijeron las personas.
- **Derivado:** se infiere de lo que dijeron.
- **Supuesto:** todavía no está validado (ver la sección f).

| Hallazgo | Decisión en la interfaz | Dónde está | Respaldo | Por qué |
|---|---|---|---|---|
| H1, H5 | La pantalla de inicio es la **Lista**, filtrada en **«Con stock»** y ordenada **por cercanía** | `lista.kv`, `lista.py` | Directo | Responde lo que más frustra («No encontrar Pelet») sin tocar nada |
| H4 | Cada punto muestra **«Visto hace X min»** y tiene botones **«Sigue habiendo» / «Ya no hay»** | `detalle.kv`, `app.confirmar()` | Directo | Responde a «si realmente queda en ese lugar». Un dato sin hora repetiría el problema de las redes sociales |
| H6 | **Aviso «Hoy: Alerta / Preemergencia / Emergencia»** arriba de la Lista; al tocarlo se abre **«Calidad del aire hoy»** con qué hacer y un enlace al pronóstico oficial | `pda.kv`, `pda.py` | Directo | A ninguna de las 3 personas le llega la información a tiempo. En la primera pantalla la ven sin buscarla |
| H6 | El aviso dice **«Rige en todo Temuco y Padre Las Casas»** | `pda.kv` | Directo | Corrige la confusión de P3 («Donde yo vivo no tengo restricciones») |
| H7 | El **precio por saco** se ve arriba a la derecha de cada tarjeta | `PuntoCard` | Directo | P1 pide «Precios mas accesibles»; con los precios a la vista se pueden comparar cuando suben |
| H2 | **«Cómo llegar» pregunta «¿Caminando o en auto?»** y muestra la ruta y los minutos que faltan | `mapa.py → elegir_modo()`, `rutas.py` | Derivado | P2 hizo «Unos 7 viajes» en auto: con un destino confirmado se va directo, sin recorrer locales |
| H4 | **Confiabilidad en estrellas (0 a 5)**: amarillas con 5, verdes de 2 a 4½ y rojas con 1½ o menos. Se calcula con la frescura del dato, cuántos lo confirman y la reputación de quien reporta | `confianza.py`, `EstrellasConf` | Derivado | Responde a «si realmente queda» de un vistazo |
| H4 | **Cuentas, opiniones y votos «Útil / No útil»** con niveles de reputación | `cuentas.py`, `perfil.kv`, `OpinionCard` | Derivado | Para confiar en un dato hay que saber quién lo dio. Nadie lo pidió textualmente |
| H3, H4 | **Cualquier vecino puede publicar un punto**, incluidos particulares; la ubicación se marca en el mapa | `formulario.kv`, `elegir.kv` | Derivado + Supuesto | Reúne lo que hoy está en páginas, redes, fruterías y pasajes, y suma «mas zonas de ventas» (P1). **Supuesto:** que la gente esté dispuesta a reportar |
| H9 | Consejos de cuidado para **niños, adultos mayores y personas con problemas respiratorios** en días de episodio | `pda.py` | Derivado | Las 3 personas tienen a alguien afectado por el frío o el humo. Aborda en parte el problema del humo de P3 |
| H10 | **Botones grandes, lenguaje cotidiano, color siempre con texto, solo 3 pestañas y Ayuda** | `widgets.kv`, `ayuda.kv` | Derivado | La persona de 60 o más es la que más se esfuerza y la que más necesita simplicidad |
| (H8) | Cada punto indica **qué vende: Pellet, Leña seca o Ambos** | `formulario.kv`, `utils.describir()` | Supuesto | **Respaldo débil:** la única persona que usa leña no tiene problemas para conseguirla. Se incluye porque el problema definido en la plantilla habla de «leña seca o pellet», y porque 2 personas mencionaron leña de mala calidad. **El foco de la app es el pellet** |

## d) Justificación de la estructura y navegación

La barra inferior tiene solo **3 pestañas: Lista · Mapa · Perfil**.

1. **Lista** (inicio): arriba, el **aviso del PDA del día** (H6). Debajo, los puntos con stock ordenados por cercanía (H1, H5), con estado, precio y confiabilidad. Una lista se lee de arriba abajo, sin tener que manejar un mapa (H10). El botón **Publicar un punto** está fijo abajo (H3).
2. **Mapa** (al centro): ubica los puntos y lleva a ellos con «Cómo llegar», a pie o en auto (H2).
3. **Perfil**: reputación del usuario y acceso a **Ayuda** («¿Tienes dudas?»), también disponible sin cuenta.

Pantallas secundarias: Detalle, Publicar, Elegir ubicación, Calidad del aire hoy,
Ayuda, Entrar y Crear cuenta. Todas tienen el botón de volver en la `MDTopAppBar`.
Para consultar no hace falta cuenta («Seguir sin cuenta»); solo se pide para
publicar, reportar u opinar.

## e) Diversidad y accesibilidad

- **Adultos mayores** (P2, 60 años o más): botones de 52 dp, textos de botón de 16 sp en negrita, lenguaje cotidiano («Sí había», «Ya no hay») y pocas pestañas.
- **El color nunca va solo:** el estado del stock lleva ícono y texto; la confiabilidad lleva estrellas, número y palabra en los extremos; el PDA lleva ícono y nombre del episodio.
- **Distintos medios de transporte** (P2 en auto, P1 al supermercado): rutas a pie o en auto.
- **Distintos combustibles** (P1 y P2 usan pellet, P3 usa leña): cada punto indica si vende pellet, leña seca o ambos.
- **Sin cuenta también sirve:** quien solo quiere mirar no se topa con una barrera.
- **Sin buena conexión:** si falla internet, la ruta se muestra como una línea recta aproximada y la lista sigue funcionando.
- **Privacidad:** no se piden datos personales más allá de un nombre visible, y la contraseña se guarda con hash.

## f) Supuestos sin validar y próximos pasos

Lo que la investigación **no** demuestra, y conviene validar:
1. **Que las personas estén dispuestas a reportar stock y precio.** La app depende de esos reportes, pero la pauta no lo preguntó. Es lo primero que hay que confirmar.
2. **Que los vendedores quieran informar su stock.** No se entrevistó a ninguno.
3. **Que la leña seca sea un problema de abastecimiento.** La única persona que usa leña la compra en verano sin problemas: «Somos precavidos con el tema de la leña».
4. **Que la escasez de pellet empuje a usar leña húmeda.** Lo dice la hipótesis de la plantilla, pero ninguna persona lo mencionó: ante la falta de pellet buscaron en redes, hicieron viajes o usaron contactos.
5. **El humo de los vecinos** (el problema principal de P3) solo se aborda en parte, con la pantalla de calidad del aire y los consejos de cuidado.

Próximos pasos:
- Obtener el episodio del PDA del **pronóstico oficial** y enviarlo como **notificación** (fuera del alcance de la E2).
- Entrevistar a más personas y a **vendedores de pellet y leña**, preguntando directamente si reportarían stock y precio.
