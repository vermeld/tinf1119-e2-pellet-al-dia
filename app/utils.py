# -*- coding: utf-8 -*-
"""Utilidades de formato de fecha, hora y dinero."""

import re
from datetime import datetime, timedelta

from .config import COMBUSTIBLES, HORAS_PARA_DUDAR


# Formato de dinero chileno.
def plata(valor):
    """5290 -> '$5.290'"""
    return "$" + format(int(valor), ",d").replace(",", ".")


# Convierte una fecha en «hace 25 min», «hace 3 h», etc.
def hace(iso):
    """Convierte una marca de tiempo en 'hace 25 min'."""
    try:
        t = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return "sin fecha"
    minutos = int((datetime.now() - t).total_seconds() // 60)
    if minutos < 2:
        return "recién"
    if minutos < 60:
        return "hace %d min" % minutos
    horas = minutos // 60
    if horas < 24:
        return "hace %d h" % horas
    return t.strftime("el %d/%m a las %H:%M")


# ¿El dato tiene más de 6 horas? Entonces se muestra en ámbar («Puede que ya no quede»).
def es_viejo(iso):
    try:
        t = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return True
    return datetime.now() - t > timedelta(hours=HORAS_PARA_DUDAR)


# Revisa que una hora esté en formato HH:MM (la usa la validación del formulario).
def hora_valida(texto):
    return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", texto.strip()))


# Fecha de hace X minutos (para los datos de ejemplo).
def hace_rato(minutos):
    return (datetime.now() - timedelta(minutes=minutos)).isoformat(timespec="seconds")


# Arma los textos de un punto (estado, precio, color, etc.) que usan la lista y el detalle.
def describir(p):
    """Textos que se muestran de un punto, compartidos por la lista y el detalle.

    'color' es el nombre del color de la app (C_HAY, C_NOHAY, C_DUDA).
    """
    dudoso = p["hay"] and es_viejo(p["visto"])
    combustible = p.get("combustible", "pellet")
    que = {"pellet": "pellet", "lena": "leña seca", "ambos": "pellet y leña"}[combustible]
    unidad = "saco de leña" if combustible == "lena" else "saco 15 kg"

    if p["hay"]:
        if p["sacos"]:
            estado = "Hay %s · quedaban %d sacos" % (que, p["sacos"])
        else:  # alguien confirmó que hay, pero sin decir cuántos sacos
            estado = "Hay %s" % que
        precio = "%s\n[size=12sp]%s[/size]" % (plata(p["precio"]), unidad) if p["precio"] else ""
        color, icono = "C_HAY", "check-circle"
    else:
        estado = "Sin stock"
        precio = ""
        color, icono = "C_NOHAY", "close-circle"

    if dudoso:
        visto = "Visto %s. Puede que ya no quede." % hace(p["visto"])
        color, icono = "C_DUDA", "alert-circle"
    else:
        visto = "Visto %s por %s" % (hace(p["visto"]), p["autor"])
        if p["confirmas"]:
            visto += " · %d confirmaciones" % p["confirmas"]

    tipo = "Tienda" if p["tipo"] == "tienda" else "Particular"

    return {
        "estado": estado,
        "precio": precio,
        "color": color,
        "icono": icono,
        "visto": visto,
        "dudoso": dudoso,
        "tipo": tipo,
        "subtitulo": "%s · %s · %s" % (que[0].upper() + que[1:], tipo, p["comuna"]),
        "combustible": combustible,
        "unidad": unidad,
        "horario": "Atiende de %s a %s" % (p["desde"], p["hasta"]),
    }
