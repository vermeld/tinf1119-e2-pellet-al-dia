# -*- coding: utf-8 -*-
"""Widgets reutilizables, con su parte visual definida en los .kv."""

from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.navigationbar import MDNavigationItem


# La raíz de la app: pantallas arriba y barra de pestañas abajo (kv/raiz.kv).
class Raiz(MDBoxLayout):
    """Pantallas + barra de navegación inferior (kv/raiz.kv)."""


# Cada PESTAÑA de la barra de abajo (Lista, Mapa, Perfil).
class ItemNav(MDNavigationItem):
    """Pestaña de la barra inferior; 'pantalla' es el nombre de la pantalla que abre."""

    pantalla = StringProperty("")
    icono = StringProperty("")
    texto = StringProperty("")


# TARJETA DE PUNTO de la lista (su diseño está en kv/widgets.kv).
class PuntoCard(MDCard):
    """Tarjeta de un punto de venta. Al tocarla se abre el detalle."""

    punto_id = NumericProperty(0)
    nombre = StringProperty("")
    subtitulo = StringProperty("")
    precio_txt = StringProperty("")
    estado = StringProperty("")
    icono_estado = StringProperty("check-circle")
    direccion = StringProperty("")
    horario = StringProperty("")
    visto_txt = StringProperty("")
    color_banda = ListProperty([0, 0, 0, 1])
    color_visto = ListProperty([0, 0, 0, 1])
    conf_valor = NumericProperty(0)          # estrellas de confiabilidad (0 a 5)
    conf_numero = StringProperty("")
    conf_color = ListProperty([0, 0, 0, 1])
    conf_color_texto = ListProperty([0, 0, 0, 1])
    estrellas_txt = StringProperty("")       # promedio de opiniones


# TARJETA DE OPINIÓN del detalle (diseño en kv/widgets.kv).
class OpinionCard(MDCard):
    """Opinión de un usuario sobre un punto, con botones Útil / No útil."""

    punto_id = NumericProperty(0)
    comentario_id = StringProperty("")
    autor = StringProperty("")
    nivel = StringProperty("")
    nivel_icono = StringProperty("account-outline")
    estrellas = NumericProperty(0)
    texto = StringProperty("")
    cuando = StringProperty("")
    utiles = NumericProperty(0)
    no_utiles = NumericProperty(0)
    mi_voto = NumericProperty(0)  # 1 útil, -1 no útil, 0 sin voto
    propia = BooleanProperty(False)
