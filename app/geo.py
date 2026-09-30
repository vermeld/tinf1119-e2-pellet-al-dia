# -*- coding: utf-8 -*-
"""Cálculos geográficos simples: distancias y avance sobre una ruta.

Una ruta es una lista de puntos (lat, lon).
"""

from math import asin, cos, radians, sin, sqrt

from .config import VELOCIDAD_CAMINANDO

RADIO_TIERRA = 6371000  # metros


def distancia(a, b):
    """Distancia en metros entre dos puntos (lat, lon), fórmula de Haversine."""
    lat1, lon1, lat2, lon2 = map(radians, (a[0], a[1], b[0], b[1]))
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * RADIO_TIERRA * asin(sqrt(h))


def largo(ruta):
    return sum(distancia(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1))


def punto_en(ruta, metros):
    """Punto de la ruta tras recorrer 'metros' desde el inicio, y el índice del tramo."""
    for i in range(len(ruta) - 1):
        tramo = distancia(ruta[i], ruta[i + 1])
        if metros <= tramo:
            t = metros / tramo if tramo else 0
            lat = ruta[i][0] + (ruta[i + 1][0] - ruta[i][0]) * t
            lon = ruta[i][1] + (ruta[i + 1][1] - ruta[i][1]) * t
            return (lat, lon), i
        metros -= tramo
    return ruta[-1], len(ruta) - 1


def mas_cercano(ruta, pos, desde=0):
    """Índice del vértice de la ruta más cercano a pos (sin retroceder de 'desde')."""
    mejor, mejor_d = desde, float("inf")
    for i in range(desde, len(ruta)):
        d = distancia(ruta[i], pos)
        if d < mejor_d:
            mejor, mejor_d = i, d
    return mejor


def texto_distancia(metros):
    if metros < 1000:
        return "%d m" % (round(metros / 10) * 10)
    return ("%.1f km" % (metros / 1000)).replace(".", ",")


def minutos_caminando(metros):
    return max(1, round(metros / VELOCIDAD_CAMINANDO / 60))


def texto_caminando(metros):
    return "%s · %d min a pie" % (texto_distancia(metros), minutos_caminando(metros))


def texto_viaje(metros, velocidad, texto_modo):
    """'1,2 km · 4 min en auto' con la velocidad media de la ruta (m/s)."""
    minutos = max(1, round(metros / velocidad / 60))
    return "%s · %d min %s" % (texto_distancia(metros), minutos, texto_modo)
