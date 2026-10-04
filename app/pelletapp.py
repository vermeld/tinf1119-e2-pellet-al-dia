# -*- coding: utf-8 -*-
"""Clase principal de la app Pellet al Día (KivyMD)."""

import json
import os
import uuid
from datetime import datetime

from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import SlideTransition
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from . import compat, confianza, config, pda
from .cuentas import Cuentas
from .data import datos_iniciales
from .mapa import MapaPellet
from .screens.ayuda import PantallaAyuda
from .screens.detalle import PantallaDetalle
from .screens.elegir import PantallaElegir
from .screens.entrar import PantallaEntrar
from .screens.formulario import PantallaFormulario
from .screens.lista import PantallaLista
from .screens.mapa import PantallaMapa
from .screens.pda import PantallaPDA
from .screens.perfil import PantallaPerfil
from .screens.registro import PantallaRegistro
from .ubicacion import Ubicacion
from .widgets import ItemNav, OpinionCard, Raiz

KV_DIR = os.path.join(os.path.dirname(__file__), "kv")
KV_ARCHIVOS = ("widgets.kv", "raiz.kv", "mapa.kv", "lista.kv", "detalle.kv",
               "formulario.kv", "elegir.kv", "ayuda.kv", "entrar.kv", "registro.kv",
               "perfil.kv", "pda.kv")
# Orden de las pestañas: define hacia dónde se desliza la transición.
PESTANAS = ["lista", "mapa", "perfil"]
INICIO = "lista"  # la primera pantalla después de entrar
SIN_BARRA = ("entrar", "registro")  # pantallas que ocupan todo, sin barra inferior
ARCHIVO_DATOS = "puntos_temuco_v2.json"

compat.aplicar()  # parche KivyMD 2.0.0 (ver compat.py)

# En escritorio simulamos una pantalla de celular. En Android se ignora.
if platform not in ("android", "ios"):
    Window.size = (config.VENTANA_ANCHO, config.VENTANA_ALTO)


# Fecha y hora actual en texto (así se guarda en los reportes y opiniones).
def ahora():
    return datetime.now().isoformat(timespec="seconds")


# LA APP COMPLETA. Aquí se arman las pantallas, se guardan los datos y se maneja la
# navegación. Los botones de los .kv llaman a funciones de esta clase con «app.algo()».
class PelletApp(MDApp):
    title = "Pellet al Día"

    # Colores con significado (semáforo de stock). El resto lo pone el tema Material.
    C_HAY = ListProperty(list(config.C_HAY))
    C_NOHAY = ListProperty(list(config.C_NOHAY))
    C_DUDA = ListProperty(list(config.C_DUDA))
    C_RUTA = ListProperty(list(config.C_RUTA))
    C_ORO = ListProperty(list(config.C_ORO))
    C_ORO_TEXTO = ListProperty(list(config.C_ORO_TEXTO))

    SECTORES = ListProperty(config.SECTORES)

    # Dónde está el usuario (lat, lon). La pantalla Mapa lo sigue.
    pos_usuario = ListProperty(list(config.UBICACION_SIMULADA))
    hay_gps = BooleanProperty(False)

    # Episodio del PDA de hoy (dato de ejemplo en la maqueta, ver pda.py)
    episodio = StringProperty(config.EPISODIO_DEMO)
    titulo_episodio = StringProperty("")
    corto_episodio = StringProperty("")
    icono_episodio = StringProperty("alert")
    color_episodio = ListProperty([0, 0, 0, 1])

    # Sesión: los .kv se actualizan solos cuando cambian
    con_sesion = BooleanProperty(False)
    nombre_usuario = StringProperty("")

    # build() se ejecuta una vez al abrir la app: carga los datos y las cuentas,
    # lee los archivos .kv y crea todas las pantallas dentro del ScreenManager.
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = config.PALETA

        self.on_episodio(self, self.episodio)
        self.archivo = os.path.join(self.user_data_dir, ARCHIVO_DATOS)
        self.puntos = self.cargar()
        self.cuentas = Cuentas(self.user_data_dir)
        self._actualizar_sesion()
        self.ubicacion = Ubicacion(self)
        self.anterior = INICIO

        for nombre, clase in (("MapaPellet", MapaPellet), ("Raiz", Raiz),
                              ("ItemNav", ItemNav), ("OpinionCard", OpinionCard)):
            Factory.register(nombre, cls=clase)
        for nombre in KV_ARCHIVOS:
            Builder.load_file(os.path.join(KV_DIR, nombre))

        raiz = Raiz()
        self.sm = raiz.ids.sm
        self.nav = raiz.ids.nav
        self.sm.transition = SlideTransition(duration=0.2)
        for clase, nombre in ((PantallaEntrar, "entrar"), (PantallaRegistro, "registro"),
                              (PantallaMapa, "mapa"), (PantallaLista, "lista"),
                              (PantallaDetalle, "detalle"), (PantallaFormulario, "form"),
                              (PantallaElegir, "elegir"), (PantallaPerfil, "perfil"),
                              (PantallaPDA, "pda"),
                              (PantallaAyuda, "ayuda")):
            self.sm.add_widget(clase(name=nombre))

        # con sesión guardada se entra directo al mapa
        self.sm.transition.duration = 0
        self.ir_a(INICIO if self.con_sesion else "entrar")
        self.sm.transition.duration = 0.2
        return raiz

    # Cuando la ventana ya está abierta: enciende el GPS (solo en el celular).
    def on_start(self):
        self.ubicacion.iniciar()

    # ---- datos

    # Lee los puntos guardados en el archivo JSON (la primera vez usa los de ejemplo).
    def cargar(self):
        puntos = None
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    puntos = json.load(f)
            except (ValueError, OSError):
                pass
        puntos = puntos or datos_iniciales()
        for p in puntos:  # por si vienen de una versión anterior
            p.setdefault("reportes", [])
            p.setdefault("comentarios", [])
            p.setdefault("autor_id", None)
            p.setdefault("creador_id", None)
            p.setdefault("combustible", "pellet")
        return puntos

    # Guarda los puntos en el archivo JSON para que no se pierdan al cerrar.
    def guardar(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(self.puntos, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # sin permisos de escritura: la sesión sigue funcionando en memoria

    # Número para un punto nuevo (el mayor que existe + 1).
    def nuevo_id(self):
        return max([p["id"] for p in self.puntos], default=0) + 1

    # Busca un punto por su número (id).
    def buscar(self, punto_id):
        for p in self.puntos:
            if p["id"] == punto_id:
                return p
        return None

    # Estrellas de confiabilidad de un punto (el cálculo está en confianza.py).
    def confianza(self, p):
        return confianza.calcular(p, self.cuentas, self.puntos)

    # Nivel de reputación de un usuario: Nuevo, Confiable o Experto.
    def nivel(self, uid):
        return self.cuentas.nivel(uid, self.puntos)

    # Cuando cambia el episodio del PDA, actualiza el título, el color y el ícono del aviso.
    def on_episodio(self, app, valor):
        n = pda.NIVELES[valor]
        self.titulo_episodio = n["titulo"]
        self.corto_episodio = n["corto"]
        self.icono_episodio = n["icono"]
        self.color_episodio = list(n["color"])

    # ---- cuentas

    # Actualiza si hay alguien conectado y su nombre (los .kv lo usan para mostrar u ocultar cosas).
    def _actualizar_sesion(self):
        u = self.cuentas.actual
        self.con_sesion = u is not None
        self.nombre_usuario = u["nombre"] if u else ""

    # Número del usuario conectado (None si nadie entró).
    @property
    def uid(self):
        return self.cuentas.sesion_id

    # Crear cuenta: la llama el BOTÓN «Crear mi cuenta» (screens/registro.py).
    def registrar(self, nombre, usuario, clave):
        ok, msj = self.cuentas.registrar(nombre, usuario, clave)
        if ok:
            self._actualizar_sesion()
            self.ir_a(INICIO)
            self.avisar(msj)
        return ok, msj

    # Iniciar sesión: la llama el BOTÓN «Entrar» (screens/entrar.py).
    def entrar(self, usuario, clave):
        ok, msj = self.cuentas.entrar(usuario, clave)
        if ok:
            self._actualizar_sesion()
            self.ir_a(INICIO)
            self.avisar(msj)
        return ok, msj

    # Cerrar sesión: la llama el BOTÓN «Cerrar sesión» del perfil.
    def salir(self):
        self.cuentas.salir()
        self._actualizar_sesion()
        self.ir_a("entrar", "right")

    # Si nadie entró, muestra el diálogo «Necesitas una cuenta» y devuelve False.
    # Se usa antes de publicar, reportar, opinar o votar.
    def requiere_cuenta(self, para_que):
        """True si hay sesión. Si no, explica por qué hace falta y ofrece entrar."""
        if self.con_sesion:
            return True

        def ir(pantalla):
            dialogo.dismiss()
            self.ir_a(pantalla)

        dialogo = MDDialog(
            MDDialogIcon(icon="account-lock-outline"),
            MDDialogHeadlineText(text="Necesitas una cuenta"),
            MDDialogSupportingText(
                text="Para %s entra con tu cuenta. Así los vecinos saben quién "
                     "reporta y pueden confiar en el dato." % para_que),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Ahora no"), style="text",
                         on_release=lambda *a: dialogo.dismiss()),
                MDButton(MDButtonText(text="Crear cuenta"), style="text",
                         on_release=lambda *a: ir("registro")),
                MDButton(MDButtonText(text="Entrar"), style="filled",
                         on_release=lambda *a: ir("entrar")),
                spacing="4dp",
            ),
        )
        dialogo.open()
        return False

    # ---- acciones de la comunidad (todas requieren sesión)

    # Guarda un punto nuevo publicado desde el formulario.
    def agregar_punto(self, punto):
        u = self.cuentas.actual
        punto.update({
            "autor": u["nombre"], "autor_id": u["id"], "creador_id": u["id"],
            "reportes": [{"uid": u["id"], "hay": punto["hay"], "t": punto["visto"]}],
            "comentarios": [],
        })
        self.puntos.insert(0, punto)
        self.guardar()

    # BOTONES «Sigue habiendo» / «Ya no hay» (y «¿Había stock?» al llegar):
    # guarda el reporte, cambia el estado del punto y así cambian sus estrellas.
    def confirmar(self, punto_id, hay):
        """Un usuario reporta si hay o no hay pellet. Mantiene vivo el mapa."""
        p = self.buscar(punto_id)
        if p is None or not self.requiere_cuenta("reportar el stock"):
            return False
        u = self.cuentas.actual
        p["hay"] = hay
        p["visto"] = ahora()
        p["autor"], p["autor_id"] = u["nombre"], u["id"]
        p["confirmas"] = p["confirmas"] + 1 if hay else 0
        if not hay:
            p["sacos"] = 0
        p["reportes"].insert(0, {"uid": u["id"], "hay": hay, "t": p["visto"]})
        self.guardar()
        return True

    # La opinión que ya escribió el usuario en este punto, si existe.
    def mi_opinion(self, p):
        return next((c for c in p["comentarios"] if c["uid"] == self.uid), None)

    # BOTÓN «Publicar opinión»: guarda o reemplaza la opinión del usuario.
    def opinar(self, punto_id, estrellas, texto, hay=None):
        """Crea o reemplaza la opinión del usuario. 'hay' opcional también reporta stock."""
        p = self.buscar(punto_id)
        if p is None or not self.requiere_cuenta("opinar"):
            return False
        previa = self.mi_opinion(p)
        if previa:
            previa.update({"estrellas": estrellas, "texto": texto, "t": ahora()})
        else:
            p["comentarios"].insert(0, {
                "id": uuid.uuid4().hex[:8], "uid": self.uid, "estrellas": estrellas,
                "texto": texto, "t": ahora(), "votos": {},
            })
        if hay is not None:
            self.confirmar(punto_id, hay)  # también guarda
        else:
            self.guardar()
        return True

    # BOTONES «Útil» / «No útil» de una opinión.
    def votar(self, punto_id, comentario_id, valor):
        """valor: 1 = útil, -1 = no útil. Votar lo mismo otra vez quita el voto."""
        p = self.buscar(punto_id)
        if p is None or not self.requiere_cuenta("calificar opiniones"):
            return False
        c = next((c for c in p["comentarios"] if c["id"] == comentario_id), None)
        if c is None or c["uid"] == self.uid:
            return False  # no se vota la opinión propia
        clave = str(self.uid)
        if c["votos"].get(clave) == valor:
            del c["votos"][clave]
        else:
            c["votos"][clave] = valor
        self.guardar()
        return True

    # ---- navegación

    # Sectores para el menú, con «Todo Temuco» al principio.
    def opciones_sector(self):
        return ["Todo Temuco"] + list(config.SECTORES)

    # CAMBIAR DE PANTALLA. Todos los botones que llevan a otra pantalla usan esta función.
    # También esconde la barra de abajo en Entrar y Crear cuenta, y marca la pestaña activa.
    def ir_a(self, pantalla, direccion=None):
        actual = self.sm.current
        if direccion is None:
            if actual in PESTANAS and pantalla in PESTANAS:
                direccion = "left" if PESTANAS.index(pantalla) > PESTANAS.index(actual) else "right"
            else:
                direccion = "left"
        self.sm.transition.direction = direccion
        self.sm.current = pantalla

        # barra inferior: oculta al entrar o registrarse
        ocultar = pantalla in SIN_BARRA
        self.nav.opacity = 0 if ocultar else 1
        self.nav.disabled = ocultar
        self.nav.size_hint_y = None
        self.nav.height = 0 if ocultar else dp(80)
        # marca la pestaña correspondiente sin disparar otra vez el evento
        if pantalla in PESTANAS:
            for item in self.nav.children:
                item.active = item.pantalla == pantalla

    # Se ejecuta al tocar una PESTAÑA de la barra de abajo (Lista, Mapa o Perfil).
    def al_cambiar_pestana(self, item):
        if self.sm.current != item.pantalla:
            self.ir_a(item.pantalla)

    # Abre el detalle de un punto (al tocar una tarjeta o el BOTÓN «Detalle» del mapa).
    def ver_detalle(self, punto_id):
        if self.sm.current != "detalle":
            self.anterior = self.sm.current
        detalle = self.sm.get_screen("detalle")
        detalle.punto_id = punto_id
        if self.sm.current == "detalle":
            detalle.on_pre_enter()  # ya estaba abierta: on_pre_enter no se dispara solo
        self.ir_a("detalle", "left")

    # BOTÓN «←» del detalle: vuelve a la pantalla de donde se vino.
    def volver(self):
        self.ir_a(self.anterior, "right")

    # BOTÓN «Ver en el mapa»: va al mapa y selecciona el punto.
    def ver_en_mapa(self, punto_id):
        self.ir_a("mapa")
        self.sm.get_screen("mapa").seleccionar(punto_id)

    # BOTÓN «Cómo llegar» del detalle: va al mapa y pregunta si vas a pie o en auto.
    def como_llegar(self, punto_id):
        self.ir_a("mapa")
        self.sm.get_screen("mapa").elegir_modo(punto_id)

    # BOTÓN «Restaurar datos de ejemplo» (Ayuda › En el computador): vuelve a poner
    # los 10 puntos de ejemplo con horas frescas. Las cuentas no se borran.
    def restaurar_ejemplo(self):
        def si(*args):
            dialogo.dismiss()
            self.puntos = datos_iniciales()
            self.guardar()
            self.ir_a("lista")
            self.avisar("Listo: se restauraron los datos de ejemplo.")

        dialogo = MDDialog(
            MDDialogIcon(icon="restore"),
            MDDialogHeadlineText(text="¿Restaurar los datos de ejemplo?"),
            MDDialogSupportingText(
                text="Vuelven los 10 puntos de ejemplo con horas recientes. Se borran los "
                     "puntos, reportes y opiniones que hayas agregado. Tu cuenta no se borra."),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Cancelar"), style="text",
                         on_release=lambda *a: dialogo.dismiss()),
                MDButton(MDButtonText(text="Restaurar"), style="filled", on_release=si),
                spacing="8dp",
            ),
        )
        dialogo.open()

    # Mensaje corto que aparece abajo (Snackbar), ej. «¡Gracias! …».
    def avisar(self, texto):
        MDSnackbar(
            MDSnackbarText(text=texto),
            y=dp(96),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.92,
            duration=2.5,
        ).open()

    # En el celular: guarda los datos si la app pasa a segundo plano.
    def on_pause(self):
        self.guardar()
        return True

    # Al cerrar la app: guarda los datos.
    def on_stop(self):
        self.guardar()
