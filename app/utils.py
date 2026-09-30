# -*- coding: utf-8 -*-
"""Utilidades de formato de fecha, hora y dinero."""

import re
from datetime import datetime, timedelta

from .config import HORAS_PARA_DUDAR


def plata(valor):
    """5290 -> '$5.290'"""
    return "$" + format(int(valor), ",d").replace(",", ".")


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


def es_viejo(iso):
    try:
        t = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return True
    return datetime.now() - t > timedelta(hours=HORAS_PARA_DUDAR)


def hora_valida(texto):
    return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", texto.strip()))


def hace_rato(minutos):
    return (datetime.now() - timedelta(minutes=minutos)).isoformat(timespec="seconds")


def describir(p):
    """Textos que se muestran de un punto, compartidos por la lista y el detalle.

    'color' es el nombre del color de la app (C_HAY, C_NOHAY, C_DUDA).
    """
    dudoso = p["hay"] and es_viejo(p["visto"])

    if p["hay"]:
        estado = "Hay pellet · quedaban %d sacos" % p["sacos"]
        precio = "%s\n[size=12sp]saco 15 kg[/size]" % plata(p["precio"]) if p["precio"] else ""
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
        "subtitulo": "%s · %s" % (tipo, p["comuna"]),
        "horario": "Atiende de %s a %s" % (p["desde"], p["hasta"]),
    }
