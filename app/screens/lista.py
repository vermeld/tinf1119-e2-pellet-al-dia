# -*- coding: utf-8 -*-
"""Pantalla principal: lista de puntos con pellet, con filtros."""

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from .. import confianza, geo
from ..utils import describir, es_viejo
from ..widgets import PuntoCard

TODO_TEMUCO = "Todo Temuco"


class PantallaLista(MDScreen):
    solo_con = BooleanProperty(True)
    comuna = StringProperty(TODO_TEMUCO)

    def on_pre_enter(self, *args):
        self.refrescar()

    def on_solo_con(self, *args):
        self.refrescar()

    def on_comuna(self, *args):
        self.refrescar()

    def poner_filtro(self, solo_con):
        self.solo_con = solo_con

    def abrir_comunas(self, boton):
        app = App.get_running_app()
        items = [
            {"text": c, "on_release": lambda c=c: self._elegir_comuna(c)}
            for c in app.opciones_sector()
        ]
        self._menu = MDDropdownMenu(caller=boton, items=items, position="bottom")
        self._menu.open()

    def _elegir_comuna(self, comuna):
        self.comuna = comuna
        self._menu.dismiss()

    def refrescar(self, *args):
        if "lista" not in self.ids:
            return  # aún no se aplica el .kv
        app = App.get_running_app()

        puntos = [p for p in app.puntos if p["hay"] or not self.solo_con]
        if self.comuna != TODO_TEMUCO:
            puntos = [p for p in puntos if p["comuna"] == self.comuna]
        # primero lo más cerca de ti, como en una app de mapas
        puntos.sort(key=lambda p: geo.distancia(app.pos_usuario, (p["lat"], p["lon"])))

        con_stock = sum(1 for p in app.puntos if p["hay"] and not es_viejo(p["visto"]))
        if con_stock == 1:
            self.ids.resumen.text = "1 punto con stock reportado en las últimas horas."
        elif con_stock:
            self.ids.resumen.text = "%d puntos con stock reportados en las últimas horas." % con_stock
        else:
            self.ids.resumen.text = "Nadie ha reportado stock reciente. Si encontraste, avisa."

        contenedor = self.ids.lista
        contenedor.clear_widgets()

        if not puntos:
            contenedor.add_widget(MDLabel(
                text="No hay puntos con este filtro.\nSi viste pellet en tu barrio, publícalo.",
                halign="center", theme_text_color="Secondary",
                size_hint_y=None, height=dp(120),
            ))
            return

        for p in puntos:
            contenedor.add_widget(self._tarjeta(p, app))

    def _tarjeta(self, p, app):
        d = describir(p)
        c = app.confianza(p)
        return PuntoCard(
            conf_valor=c["estrellas"],
            conf_numero=c["numero"],
            conf_color=list(getattr(app, c["color"])),
            conf_color_texto=list(getattr(app, c["color_texto"])),
            estrellas_txt=confianza.texto_estrellas(p),
            punto_id=p["id"],
            nombre=p["nombre"],
            subtitulo="%s · a %s" % (d["subtitulo"], geo.texto_distancia(
                geo.distancia(app.pos_usuario, (p["lat"], p["lon"])))),
            precio_txt=d["precio"],
            estado=d["estado"],
            icono_estado=d["icono"],
            direccion=p["direccion"],
            horario=d["horario"],
            visto_txt=d["visto"],
            color_banda=list(getattr(app, d["color"])),
            color_visto=list(app.C_DUDA) if d["dudoso"] else list(app.theme_cls.onSurfaceVariantColor),
        )
