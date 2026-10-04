# -*- coding: utf-8 -*-
"""Pantalla Mapa: puntos de venta en Temuco y navegación a pie o en auto hasta uno."""

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy_garden.mapview import MarkerMapLayer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget

from .. import confianza, config, geo
from ..mapa import MarcadorYo, PinPunto, RutaLayer, icono
from ..rutas import pedir_ruta
from ..utils import describir

PIN_POR_COLOR = {"C_HAY": "pin_hay", "C_NOHAY": "pin_nohay", "C_DUDA": "pin_duda"}


class PantallaMapa(MDScreen):
    solo_con = BooleanProperty(False)

    # punto seleccionado (tarjeta inferior)
    sel_id = NumericProperty(0)
    sel_nombre = StringProperty("")
    sel_estado = StringProperty("")
    sel_icono = StringProperty("check-circle")
    sel_color = ListProperty([0, 0, 0, 1])
    sel_distancia = StringProperty("")
    sel_conf_valor = NumericProperty(0)
    sel_conf_numero = StringProperty("")
    sel_conf_color = ListProperty([0, 0, 0, 1])
    sel_conf_color_texto = ListProperty([0, 0, 0, 1])
    sel_estrellas = StringProperty("")

    # navegación
    navegando = BooleanProperty(False)
    buscando_ruta = BooleanProperty(False)
    simulando = BooleanProperty(False)
    nav_restante = StringProperty("")
    nav_nota = StringProperty("")
    nav_progreso = NumericProperty(0)
    modo = StringProperty("pie")  # 'pie' o 'auto'

    def on_kv_post(self, base_widget):
        mapa = self.ids.mapa
        self.capa_ruta = RutaLayer()
        self.capa_pines = MarkerMapLayer()
        self.capa_yo = MarkerMapLayer()
        # el orden importa: la ruta queda bajo los pines y "tú" encima de todo
        mapa.add_layer(self.capa_ruta)
        mapa.add_layer(self.capa_pines)
        mapa.add_layer(self.capa_yo)
        self.yo = MarcadorYo()
        self.pines = []
        self.ruta = []
        self.destino_id = 0
        self._largo_total = 1

        app = App.get_running_app()
        mapa.add_marker(self.yo, layer=self.capa_yo)
        app.bind(pos_usuario=self.al_moverse)
        Clock.schedule_once(lambda dt: self.al_moverse(app, app.pos_usuario))

    def on_pre_enter(self, *args):
        self.refrescar()

    def on_solo_con(self, *args):
        self.refrescar()

    # ---- pines

    def refrescar(self, *args):
        app = App.get_running_app()
        mapa = self.ids.mapa
        for pin in self.pines:
            mapa.remove_marker(pin)
        self.pines = []

        for p in app.puntos:
            if self.solo_con and not p["hay"] and p["id"] != self.destino_id:
                continue
            d = describir(p)
            pin = PinPunto(punto_id=p["id"], lat=p["lat"], lon=p["lon"],
                           source=icono(PIN_POR_COLOR[d["color"]]))
            pin.bind(on_release=lambda w: self.seleccionar(w.punto_id))
            mapa.add_marker(pin, layer=self.capa_pines)
            self.pines.append(pin)

        if self.sel_id:
            self.seleccionar(self.sel_id, centrar=False)

    def seleccionar(self, punto_id, centrar=True):
        app = App.get_running_app()
        p = app.buscar(punto_id)
        if p is None:
            self.sel_id = 0
            return
        d = describir(p)
        self.sel_nombre = p["nombre"]
        self.sel_estado = "Puede que ya no quede" if d["dudoso"] else d["estado"]
        self.sel_icono = d["icono"]
        self.sel_color = list(getattr(app, d["color"]))
        metros = geo.distancia(app.pos_usuario, (p["lat"], p["lon"]))
        self.sel_distancia = "%s · %s" % (d["subtitulo"], geo.texto_caminando(metros))
        c = app.confianza(p)
        self.sel_conf_valor = c["estrellas"]
        self.sel_conf_numero = c["numero"]
        self.sel_conf_color = list(getattr(app, c["color"]))
        self.sel_conf_color_texto = list(getattr(app, c["color_texto"]))
        self.sel_estrellas = confianza.texto_estrellas(p)
        self.sel_id = punto_id
        if centrar:
            self.ids.mapa.center_on(p["lat"], p["lon"])

    def cerrar_seleccion(self):
        self.sel_id = 0

    # ---- controles del mapa

    def acercar(self, paso):
        mapa = self.ids.mapa
        mapa.zoom = max(3, min(19, mapa.zoom + paso))

    def centrar_en_mi(self):
        app = App.get_running_app()
        self.ids.mapa.center_on(*app.pos_usuario)

    def doble_toque(self, lat, lon):
        """Sin GPS (escritorio) el doble toque mueve tu ubicación simulada."""
        app = App.get_running_app()
        if app.ubicacion.hay_gps or self.navegando:
            return
        app.ubicacion.mover_a((lat, lon))
        if self.sel_id:
            self.seleccionar(self.sel_id, centrar=False)
        app.avisar("Tu ubicación simulada ahora está aquí.")

    # ---- navegación

    def elegir_modo(self, punto_id):
        """«Cómo llegar»: pregunta si vas caminando o en auto."""
        app = App.get_running_app()
        p = app.buscar(punto_id)
        if p is None:
            return
        metros = geo.distancia(app.pos_usuario, (p["lat"], p["lon"]))

        def opcion(modo, detalle):
            m = config.MODOS[modo]
            return MDListItem(
                MDListItemLeadingIcon(icon=m["icono"]),
                MDListItemHeadlineText(text=m["nombre"]),
                MDListItemSupportingText(text=detalle),
                on_release=lambda *a: self._elegido(punto_id, modo),
            )

        self._dialogo_modo = MDDialog(
            MDDialogIcon(icon="directions"),
            MDDialogHeadlineText(text="¿Cómo vas a ir?"),
            MDDialogSupportingText(text="Hacia %s (a %s en línea recta)"
                                   % (p["nombre"], geo.texto_distancia(metros))),
            MDDialogContentContainer(
                opcion("pie", "Por veredas y pasajes"),
                opcion("auto", "Respeta el sentido de las calles"),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(MDButtonText(text="Cancelar"), style="text",
                         on_release=lambda *a: self._dialogo_modo.dismiss()),
            ),
        )
        self._dialogo_modo.open()

    def _elegido(self, punto_id, modo):
        self._dialogo_modo.dismiss()
        self.navegar_a(punto_id, modo)

    def navegar_a(self, punto_id, modo="pie"):
        app = App.get_running_app()
        p = app.buscar(punto_id)
        if p is None:
            return
        self.terminar_navegacion()
        self.modo = modo
        self.destino_id = punto_id
        self.seleccionar(punto_id, centrar=False)
        self.buscando_ruta = True
        self.nav_restante = "Buscando ruta…"
        self.nav_nota = ""
        pedir_ruta(app.pos_usuario, (p["lat"], p["lon"]), modo, self._ruta_lista)

    def _ruta_lista(self, ruta, aproximada, velocidad):
        if not self.buscando_ruta:
            return  # el usuario canceló mientras se calculaba
        self.buscando_ruta = False
        self.ruta = ruta
        self._velocidad = velocidad
        self._largo_total = max(geo.largo(ruta), 1)
        self.capa_ruta.poner(ruta)
        self.navegando = True
        if aproximada:
            self.nav_nota = "Ruta aproximada en línea recta (sin conexión)"
        elif self.modo == "auto":
            self.nav_nota = "Ruta en auto, respetando el sentido de las calles"
        else:
            self.nav_nota = "Ruta caminando por las calles"
        mapa = self.ids.mapa
        mapa.zoom = 16
        mapa.center_on(*App.get_running_app().pos_usuario)
        self._actualizar_avance(App.get_running_app().pos_usuario)

    def alternar_simulacion(self):
        app = App.get_running_app()
        if app.ubicacion.simulando:
            app.ubicacion.detener()
        else:
            app.ubicacion.simular(self.ruta, config.MODOS[self.modo]["simulada"])
        self.simulando = app.ubicacion.simulando

    def terminar_navegacion(self):
        app = App.get_running_app()
        app.ubicacion.detener()
        self.simulando = False
        self.navegando = False
        self.buscando_ruta = False
        self.ruta = []
        self.destino_id = 0
        self.capa_ruta.limpiar()
        self.refrescar()

    def al_moverse(self, app, pos):
        self.yo.lat, self.yo.lon = pos
        self.capa_yo.reposition()
        if self.navegando:
            self._actualizar_avance(pos)

    def _actualizar_avance(self, pos):
        idx = geo.mas_cercano(self.ruta, pos, desde=self.capa_ruta.avance)
        restante = geo.distancia(pos, self.ruta[idx]) + geo.largo(self.ruta[idx:])
        self.capa_ruta.avance = idx
        self.capa_ruta.reposition()
        self.nav_restante = geo.texto_viaje(restante, self._velocidad,
                                            config.MODOS[self.modo]["texto"])
        self.nav_progreso = 100 * (1 - restante / self._largo_total)
        self._seguir(pos)

        if geo.distancia(pos, self.ruta[-1]) <= config.MODOS[self.modo]["llegada"]:
            self._llegar()

    def _seguir(self, pos):
        """Recentra el mapa solo si te acercas al borde (evita que 'tiemble')."""
        mapa = self.ids.mapa
        x, y = mapa.get_window_xy_from(pos[0], pos[1], mapa.zoom)
        mx, my = mapa.width * 0.3, mapa.height * 0.3
        if not (mapa.x + mx < x < mapa.right - mx and mapa.y + my < y < mapa.top - my):
            mapa.center_on(*pos)

    def _llegar(self):
        app = App.get_running_app()
        punto_id = self.destino_id
        p = app.buscar(punto_id)
        self.terminar_navegacion()
        self.seleccionar(punto_id, centrar=False)

        def responder(hay):
            self._dialogo.dismiss()
            if hay is not None and app.confirmar(punto_id, hay):
                self.refrescar()
                app.avisar("¡Gracias! Actualizaste el punto para todos.")

        self._dialogo = MDDialog(
            MDDialogIcon(icon="map-marker-check"),
            MDDialogHeadlineText(text="¡Llegaste!"),
            MDDialogSupportingText(text="Estás en %s.\n¿Había stock?" % p["nombre"]),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Después"), style="text",
                         on_release=lambda *a: responder(None)),
                MDWidget(),
                MDButton(MDButtonText(text="No había"), style="outlined",
                         on_release=lambda *a: responder(False)),
                MDButton(MDButtonText(text="Sí había"), style="filled",
                         on_release=lambda *a: responder(True)),
                spacing="8dp",
            ),
            auto_dismiss=False,
        )
        self._dialogo.open()
