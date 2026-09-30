# -*- coding: utf-8 -*-
"""Pantalla de formulario para publicar un nuevo punto."""

from datetime import datetime

from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget

from .. import config
from ..utils import hora_valida, plata


class PantallaFormulario(MDScreen):
    hay = BooleanProperty(True)
    es_tienda = BooleanProperty(True)
    comuna = StringProperty(config.SECTORES[0])
    lat = ObjectProperty(None, allownone=True)
    lon = ObjectProperty(None, allownone=True)

    def on_pre_enter(self, *args):
        self.ids.error.text = ""

    def abrir_comunas(self, boton):
        items = [
            {"text": c, "on_release": lambda c=c: self._elegir_comuna(c)}
            for c in config.SECTORES
        ]
        self._menu = MDDropdownMenu(caller=boton, items=items, position="bottom")
        self._menu.open()

    def _elegir_comuna(self, comuna):
        self.comuna = comuna
        self._menu.dismiss()

    def poner_ubicacion(self, lat, lon):
        self.lat, self.lon = lat, lon
        self.ids.error.text = ""

    def poner_hora_actual(self):
        self.ids.hora.text = datetime.now().strftime("%H:%M")

    # ---- validación

    def _falla(self, campo, mensaje):
        if campo is not None:
            campo.error = True
            campo.focus = True
        self.ids.error.text = mensaje
        return None

    def validar(self):
        """Devuelve el punto armado, o None si algo falta (y muestra el error)."""
        i = self.ids
        for campo in (i.nombre, i.direccion, i.sacos, i.precio, i.hora, i.desde, i.hasta):
            campo.error = False

        if not i.nombre.text.strip():
            return self._falla(i.nombre, "Falta el nombre del local o de quien vende.")
        if not i.direccion.text.strip():
            return self._falla(i.direccion, "Falta la dirección donde está el pellet.")
        if self.lat is None:
            return self._falla(None, "Marca en el mapa dónde está el punto.")
        if self.hay and not i.sacos.text.strip():
            return self._falla(i.sacos, "Pon cuántos sacos viste, aunque sea aproximado.")
        if self.hay and not i.precio.text.strip():
            return self._falla(i.precio, "Pon el precio por saco para que le sirva a los demás.")
        if self.hay and int(i.precio.text) < 500:
            return self._falla(i.precio, "Ese precio parece muy bajo. Revisa que sea por saco.")
        for campo, nombre in ((i.desde, "de apertura"), (i.hasta, "de cierre")):
            if not hora_valida(campo.text):
                return self._falla(campo, "La hora %s tiene que ir en formato HH:MM." % nombre)

        visto = datetime.now()
        if i.hora.text.strip():
            if not hora_valida(i.hora.text):
                return self._falla(i.hora, "La hora en que pasaste tiene que ir en formato HH:MM.")
            hh, mm = i.hora.text.strip().split(":")
            candidato = visto.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
            if candidato <= visto:
                visto = candidato

        self.ids.error.text = ""
        app = App.get_running_app()
        return {
            "id": app.nuevo_id(),
            "nombre": i.nombre.text.strip(),
            "tipo": "tienda" if self.es_tienda else "persona",
            "comuna": self.comuna,
            "direccion": i.direccion.text.strip(),
            "lat": self.lat,
            "lon": self.lon,
            "hay": self.hay,
            "sacos": int(i.sacos.text) if self.hay else 0,
            "precio": int(i.precio.text) if self.hay else None,
            "visto": visto.isoformat(timespec="seconds"),
            "desde": i.desde.text.strip(),
            "hasta": i.hasta.text.strip(),
            "confirmas": 0,
        }

    # ---- publicar

    def revisar(self):
        """Valida y muestra un resumen para confirmar antes de publicar."""
        if not App.get_running_app().requiere_cuenta("publicar un punto"):
            return
        punto = self.validar()
        if punto is None:
            return

        if punto["hay"]:
            stock = "Hay pellet: %d sacos a %s" % (punto["sacos"], plata(punto["precio"]))
        else:
            stock = "No había pellet"
        resumen = "%s\n%s, sector %s\n%s\nAtiende de %s a %s" % (
            punto["nombre"], punto["direccion"], punto["comuna"], stock,
            punto["desde"], punto["hasta"],
        )

        self._dialogo = MDDialog(
            MDDialogIcon(icon="send"),
            MDDialogHeadlineText(text="¿Publicamos este punto?"),
            MDDialogSupportingText(text=resumen),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(MDButtonText(text="Corregir"), style="text",
                         on_release=lambda *a: self._dialogo.dismiss()),
                MDButton(MDButtonText(text="Publicar"), style="filled",
                         on_release=lambda *a: self._publicar(punto)),
                spacing="8dp",
            ),
        )
        self._dialogo.open()

    def _publicar(self, punto):
        self._dialogo.dismiss()
        app = App.get_running_app()
        app.agregar_punto(punto)
        self.limpiar()
        app.ver_en_mapa(punto["id"])
        app.avisar("¡Listo! Tu punto ya aparece en el mapa.")

    def limpiar(self):
        i = self.ids
        for campo in (i.nombre, i.direccion, i.sacos, i.precio, i.hora):
            campo.text = ""
            campo.error = False
        i.error.text = ""
        self.hay = True
        self.es_tienda = True
        self.lat = self.lon = None

    def cancelar(self):
        self.limpiar()
        App.get_running_app().ir_a("lista", "right")
