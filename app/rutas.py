# -*- coding: utf-8 -*-
"""Pide una ruta a pie o en auto a un servidor OSRM (OpenStreetMap).

Si no hay internet o el servidor falla, se usa una línea recta como respaldo
para que la navegación igual funcione.
"""

import json

from kivy.network.urlrequest import UrlRequest

from .config import MODOS, RUTAS_URL, USER_AGENT


def pedir_ruta(origen, destino, modo, al_terminar):
    """modo: 'pie' o 'auto'.
    al_terminar(ruta, aproximada, velocidad) recibe una lista de (lat, lon) y la
    velocidad media en m/s (distancia / duración que calcula el servidor)."""
    url = RUTAS_URL[modo].format(lat1=origen[0], lon1=origen[1], lat2=destino[0], lon2=destino[1])
    velocidad_respaldo = MODOS[modo]["velocidad"]

    def ok(req, resultado):
        try:
            if isinstance(resultado, (str, bytes)):
                resultado = json.loads(resultado)
            r = resultado["routes"][0]
            coords = r["geometry"]["coordinates"]
            ruta = [(lat, lon) for lon, lat in coords]  # GeoJSON viene como lon, lat
            velocidad = (r["distance"] / r["duration"]) if r.get("duration") else velocidad_respaldo
            # la ruta parte y termina en la calle: la unimos al punto exacto
            al_terminar([tuple(origen)] + ruta + [tuple(destino)], False, velocidad)
        except (KeyError, IndexError, TypeError, ValueError):
            respaldo()

    def respaldo(*args):
        al_terminar([tuple(origen), tuple(destino)], True, velocidad_respaldo)

    UrlRequest(
        url,
        on_success=ok,
        on_failure=respaldo,
        on_error=respaldo,
        req_headers={"User-Agent": USER_AGENT},
        timeout=8,
    )
