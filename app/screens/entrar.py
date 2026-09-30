# -*- coding: utf-8 -*-
"""Pantalla de inicio de sesión."""

from kivy.app import App
from kivymd.uix.screen import MDScreen


class PantallaEntrar(MDScreen):

    def on_pre_enter(self, *args):
        self.ids.clave.text = ""
        self.ids.error.text = ""
        self.ids.usuario.error = self.ids.clave.error = False

    def alternar_ver_clave(self):
        self.ids.clave.password = not self.ids.clave.password

    def entrar(self):
        i = self.ids
        i.usuario.error = i.clave.error = False
        if not i.usuario.text.strip():
            i.usuario.error = True
            i.error.text = "Escribe tu usuario."
            return
        if not i.clave.text:
            i.clave.error = True
            i.error.text = "Escribe tu contraseña."
            return
        ok, msj = App.get_running_app().entrar(i.usuario.text, i.clave.text)
        if not ok:
            i.clave.error = True
            i.clave.text = ""
            i.error.text = msj

    def solo_mirar(self):
        app = App.get_running_app()
        app.ir_a("lista")
        app.avisar("Modo solo mirar. Crea una cuenta para opinar.")
