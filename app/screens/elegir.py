# -*- coding: utf-8 -*-
"""Pantalla para elegir en el mapa la ubicación de un punto nuevo."""

from kivy.app import App
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from ..mapa import icono


# Lógica de la PANTALLA «Marca dónde está» (interfaz en kv/elegir.kv).
class PantallaElegir(MDScreen):
    pin = StringProperty(icono("pin_elegir"))

    # Al entrar: centra el mapa en la ubicación ya marcada o en la tuya.
    def on_pre_enter(self, *args):
        form = App.get_running_app().sm.get_screen("form")
        if form.lat is not None:
            self.ids.mapa.center_on(form.lat, form.lon)
        else:
            self.ir_a_mi_ubicacion()

    # BOTÓN «Estoy aquí».
    def ir_a_mi_ubicacion(self):
        app = App.get_running_app()
        self.ids.mapa.zoom = 16
        self.ids.mapa.center_on(*app.pos_usuario)

    # BOTÓN «Usar este lugar»: el centro del mapa (donde está el pin) es la ubicación.
    def usar(self):
        """El centro del mapa es donde apunta el pin."""
        app = App.get_running_app()
        mapa = self.ids.mapa
        c = mapa.get_latlon_at(mapa.width / 2, mapa.height / 2)
        app.sm.get_screen("form").poner_ubicacion(c.lat, c.lon)
        app.ir_a("form", "right")
