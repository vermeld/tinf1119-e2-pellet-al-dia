# -*- coding: utf-8 -*-
"""Widgets del mapa: MapView (estilo Esri calles), pines, "tú" y la línea de la ruta."""

import os

from kivy.app import App
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy_garden.mapview import MapLayer, MapMarker, MapSource, MapView
from kivy_garden.mapview import downloader

from . import config

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

# Los servidores de mapas bloquean descargas sin un User-Agent que identifique la app.
downloader.USER_AGENT = config.USER_AGENT


def icono(nombre):
    return os.path.join(ASSETS, nombre + ".png")


def carpeta_cache():
    cache = os.path.join(App.get_running_app().user_data_dir, "cache_mapa")
    os.makedirs(cache, exist_ok=True)
    return cache


def fuente_mapa():
    """Mapa limpio (solo calles y nombres), guardado en caché en la carpeta de la app."""
    cache = carpeta_cache()
    return MapSource(
        url=config.TILES_URL,
        cache_key=config.TILES_CACHE,
        min_zoom=0,
        max_zoom=19,
        tile_size=256,
        image_ext=config.TILES_EXT,
        attribution=config.TILES_ATRIBUCION,
        cache_dir=cache,
    )


class MapaPellet(MapView):
    """MapView centrado en Temuco, con evento de doble toque (lat, lon)."""

    __events__ = ("on_doble_toque",)

    def __init__(self, **kwargs):
        kwargs.setdefault("map_source", fuente_mapa())
        kwargs.setdefault("cache_dir", carpeta_cache())  # los Tile usan esta carpeta
        kwargs.setdefault("lat", config.CENTRO_TEMUCO[0])
        kwargs.setdefault("lon", config.CENTRO_TEMUCO[1])
        kwargs.setdefault("zoom", config.ZOOM_INICIAL)
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.is_double_tap and self.collide_point(*touch.pos):
            c = self.get_latlon_at(touch.x - self.x, touch.y - self.y)
            self.dispatch("on_doble_toque", c.lat, c.lon)
            return True
        return super().on_touch_down(touch)

    def on_doble_toque(self, lat, lon):
        pass


class PinPunto(MapMarker):
    """Pin de un punto de venta; su color depende del stock."""

    punto_id = NumericProperty(0)


class MarcadorYo(MapMarker):
    """Punto azul "tú estás aquí"."""

    def __init__(self, **kwargs):
        kwargs.setdefault("source", icono("yo"))
        super().__init__(anchor_x=0.5, anchor_y=0.5, **kwargs)

    def on_touch_down(self, touch):
        return False  # no tapa los toques al mapa


class RutaLayer(MapLayer):
    """Dibuja la ruta: lo que falta en azul y lo ya caminado en gris."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruta = []
        self.avance = 0  # índice del vértice hasta donde ya caminaste

    def poner(self, ruta):
        self.ruta = list(ruta)
        self.avance = 0
        self.reposition()

    def limpiar(self):
        self.ruta = []
        self.canvas.clear()

    def reposition(self):
        self.canvas.clear()
        mapa = self.parent
        if not self.ruta or mapa is None:
            return
        zoom = mapa.zoom

        def xy(tramo):
            pts = []
            for lat, lon in tramo:
                pts.extend(mapa.get_window_xy_from(lat, lon, zoom))
            return pts

        hecho = self.ruta[:self.avance + 1]
        falta = self.ruta[self.avance:]
        with self.canvas:
            if len(hecho) > 1:
                Color(0.55, 0.58, 0.6, 0.9)
                Line(points=xy(hecho), width=dp(3), cap="round", joint="round")
            if len(falta) > 1:
                Color(1, 1, 1, 1)  # borde blanco para que resalte sobre el mapa
                Line(points=xy(falta), width=dp(5.5), cap="round", joint="round")
                Color(*config.C_RUTA)
                Line(points=xy(falta), width=dp(4), cap="round", joint="round")
