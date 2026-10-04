# -*- coding: utf-8 -*-
"""Confiabilidad del dato de stock de un punto, de 0 a 5 estrellas (con medias).

Combina tres cosas, cada una entre 0 y 1:

  frescura  (40 %): qué tan reciente es el último reporte. 1 si es de ahora,
                    baja en línea recta hasta 0 a las 12 horas.
  respaldo  (40 %): cuántos reportes de las últimas 24 h dicen lo mismo que el
                    estado actual. Cada reporte pesa según el nivel de quien lo hizo
                    (0,5 a 1) y pierde la mitad de su peso cada 6 horas. Se divide
                    por el total de reportes, pero como mínimo por 2: un solo
                    reporte nunca da respaldo completo.
  reputación (20 %): el nivel de quien hizo el último reporte
                    (Nuevo 0,5 · Confiable 0,8 · Experto 1,0).

puntaje = 0,4 × frescura + 0,4 × respaldo + 0,2 × reputación   (entre 0 y 1)
estrellas = puntaje × 5, redondeado a la media estrella más cercana

Color de las estrellas:
  5 estrellas            → amarillo (dato excelente)
  1½ estrellas o menos   → rojo (poco confiable)
  entre 2 y 4½ estrellas → verde
"""

from datetime import datetime

HORAS_FRESCURA = 12
HORAS_VENTANA = 24
VIDA_MEDIA_H = 6
MIN_PESO = 2.0  # peso de reportes necesario para respaldo completo


def _horas(iso):
    try:
        return max(0.0, (datetime.now() - datetime.fromisoformat(iso)).total_seconds() / 3600)
    except (ValueError, TypeError):
        return 999.0


# CÁLCULO DE LAS ESTRELLAS de confiabilidad de un punto (la fórmula está arriba).
def calcular(p, cuentas, puntos):
    reportes = sorted(p.get("reportes", []), key=lambda r: r["t"], reverse=True)
    if not reportes:
        return _resultado(0.0, 0, "Sin reportes todavía")

    pesos = {}  # caché del peso por usuario

    def peso(uid):
        if uid not in pesos:
            pesos[uid] = cuentas.nivel(uid, puntos)["peso"]
        return pesos[uid]

    ultimo = reportes[0]
    frescura = max(0.0, 1 - _horas(ultimo["t"]) / HORAS_FRESCURA)

    a_favor = total = 0.0
    recientes = 0
    for r in reportes:
        h = _horas(r["t"])
        if h > HORAS_VENTANA:
            continue
        recientes += 1
        w = peso(r["uid"]) * 0.5 ** (h / VIDA_MEDIA_H)
        total += w
        if r["hay"] == p["hay"]:
            a_favor += w
    respaldo = a_favor / max(total, MIN_PESO)

    reputacion = peso(ultimo["uid"])
    puntaje = 0.4 * frescura + 0.4 * respaldo + 0.2 * reputacion

    autor = cuentas.buscar(ultimo["uid"])
    nombre = autor["nombre"] if autor else "alguien"
    nivel = cuentas.nivel(ultimo["uid"], puntos)["nombre"]
    if recientes == 1:
        detalle = "1 reporte en 24 h · último de %s (%s)" % (nombre, nivel)
    else:
        detalle = "%d reportes en 24 h · último de %s (%s)" % (recientes, nombre, nivel)
    return _resultado(puntaje, recientes, detalle)


# Pasa el puntaje (0 a 1) a estrellas (0 a 5, con medias).
def a_estrellas(puntaje):
    """0..1 -> 0, 0.5, 1, ... 5 (a la media estrella más cercana)."""
    return round(max(0.0, min(1.0, puntaje)) * 10) / 2


def texto_numero(estrellas):
    """4.5 -> '4,5' · 5.0 -> '5'"""
    return ("%g" % estrellas).replace(".", ",")


# Elige el color: amarillo (5 estrellas), rojo (1½ o menos) o verde.
def _resultado(puntaje, recientes, detalle):
    estrellas = a_estrellas(puntaje)
    if estrellas >= 5:
        nivel, color, color_texto = "Excelente", "C_ORO", "C_ORO_TEXTO"
    elif estrellas <= 1.5:
        nivel, color, color_texto = "Poco confiable", "C_NOHAY", "C_NOHAY"
    else:
        nivel, color, color_texto = "Confiable", "C_HAY", "C_HAY"
    return {
        "estrellas": estrellas, "nivel": nivel,
        "color": color,              # color de las estrellas
        "color_texto": color_texto,  # color del texto (el amarillo puro no se lee sobre blanco)
        # la palabra solo en los extremos: el color nunca va solo
        "texto": "Confiabilidad %s de 5%s" % (
            texto_numero(estrellas), "" if nivel == "Confiable" else " · " + nivel.lower()),
        "numero": texto_numero(estrellas),
        "detalle": detalle, "recientes": recientes,
    }


# Promedio de las estrellas que pusieron las personas en sus opiniones.
def estrellas(p):
    """Promedio de estrellas de las opiniones: (promedio, cantidad)."""
    notas = [c["estrellas"] for c in p.get("comentarios", [])]
    if not notas:
        return 0.0, 0
    return sum(notas) / len(notas), len(notas)


def texto_estrellas(p):
    prom, n = estrellas(p)
    if not n:
        return "Sin opiniones"
    # sin el símbolo ★: la fuente Roboto no lo trae; el ícono "star" va en el .kv
    return ("%.1f (%d)" % (prom, n)).replace(".", ",")
