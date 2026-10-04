# -*- coding: utf-8 -*-
"""Pantalla para crear una cuenta nueva."""

from kivy.app import App
from kivymd.uix.screen import MDScreen

from ..cuentas import validar_registro


# Lógica de la PANTALLA CREAR CUENTA (interfaz en kv/registro.kv).
class PantallaRegistro(MDScreen):

    # Al entrar: deja los campos vacíos.
    def on_pre_enter(self, *args):
        for campo in ("nombre", "usuario", "clave", "clave2"):
            self.ids[campo].text = ""
            self.ids[campo].error = False
        self.ids.error.text = ""

    # BOTÓN «Crear mi cuenta»: valida los datos y crea la cuenta.
    def crear(self):
        i = self.ids
        for campo in ("nombre", "usuario", "clave", "clave2"):
            i[campo].error = False

        falla = validar_registro(i.nombre.text, i.usuario.text.strip(), i.clave.text, i.clave2.text)
        if falla:
            campo, mensaje = falla
            i[campo].error = True
            i[campo].focus = True
            i.error.text = mensaje
            return

        ok, msj = App.get_running_app().registrar(i.nombre.text, i.usuario.text.strip(), i.clave.text)
        if not ok:
            i.usuario.error = True
            i.error.text = msj
