# -*- coding: utf-8 -*-
"""Pantalla «Calidad del aire hoy»: episodio del PDA y qué hacer."""

import webbrowser

from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.screen import MDScreen

from .. import pda


class PantallaPDA(MDScreen):
    titulo = StringProperty("")
    corto = StringProperty("")
    icono = StringProperty("weather-windy")
    color = ListProperty([0, 0, 0, 1])

    def on_pre_enter(self, *args):
        self.mostrar()

    def mostrar(self):
        app = App.get_running_app()
        n = pda.NIVELES[app.episodio]
        self.titulo = n["titulo"]
        self.corto = n["corto"]
        self.icono = n["icono"]
        self.color = list(n["color"])
        caja = self.ids.que_hacer
        caja.clear_widgets()
        from kivy.factory import Factory
        for icono, texto in n["hacer"]:
            caja.add_widget(Factory.FilaIcono(icono=icono, texto=texto))

    def simular_otro_dia(self):
        app = App.get_running_app()
        app.episodio = pda.siguiente(app.episodio)
        self.mostrar()

    def abrir_oficial(self):
        webbrowser.open(pda.URL_OFICIAL)
