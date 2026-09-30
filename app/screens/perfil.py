# -*- coding: utf-8 -*-
"""Pantalla de perfil: nivel, reputación y aportes del usuario."""

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.screen import MDScreen


class PantallaPerfil(MDScreen):
    inicial = StringProperty("")
    usuario = StringProperty("")
    nivel = StringProperty("")
    nivel_icono = StringProperty("account-outline")
    puntos = NumericProperty(0)
    progreso = NumericProperty(0)
    falta_txt = StringProperty("")
    publicados = NumericProperty(0)
    reportes = NumericProperty(0)
    opiniones = NumericProperty(0)
    utiles = NumericProperty(0)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        u = app.cuentas.actual
        if u is None:
            return
        e = app.cuentas.estadisticas(u["id"], app.puntos)
        n = app.nivel(u["id"])
        self.inicial = u["nombre"][:1].upper()
        self.usuario = "@" + u["usuario"]
        self.nivel = n["nombre"]
        self.nivel_icono = n["icono"]
        self.puntos = n["puntos"]
        self.progreso = n["progreso"]
        if n["siguiente"]:
            self.falta_txt = "Te faltan %d puntos para ser %s." % (n["faltan"], n["siguiente"])
        else:
            self.falta_txt = "Llegaste al nivel más alto. ¡Gracias por ayudar!"
        self.publicados = e["publicados"]
        self.reportes = e["reportes"]
        self.opiniones = e["opiniones"]
        self.utiles = e["utiles"]
