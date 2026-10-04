# -*- coding: utf-8 -*-
"""Pantalla «Calidad del aire hoy»: episodio del PDA y qué hacer."""

import webbrowser

from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.screen import MDScreen

from .. import pda


# Lógica de la PANTALLA CALIDAD DEL AIRE HOY (interfaz en kv/pda.kv).
class PantallaPDA(MDScreen):
    titulo = StringProperty("")
    corto = StringProperty("")
    icono = StringProperty("weather-windy")
    color = ListProperty([0, 0, 0, 1])

    # Al entrar, muestra el episodio de hoy.
    def on_pre_enter(self, *args):
        self.mostrar()

    # Pone el título, el color y los consejos del episodio actual.
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

    # BOTÓN «Simular otro día (demo)».
    def simular_otro_dia(self):
        app = App.get_running_app()
        app.episodio = pda.siguiente(app.episodio)
        self.mostrar()

    # BOTÓN «Ver pronóstico oficial»: abre la página en el navegador.
    def abrir_oficial(self):
        webbrowser.open(pda.URL_OFICIAL)
