# -*- coding: utf-8 -*-
"""Parche para un bug de KivyMD 2.0.0.

El efecto "ripple" crea un Fbo con el tamaño del widget al construirlo. Los
widgets de alto adaptable (MDCard, MDSnackbar) nacen con alto 0 y en varias
tarjetas gráficas (ej. Intel Iris Xe) eso lanza
"FBO Initialization failed: Incomplete attachment". Aquí forzamos un tamaño
mínimo de 1x1; el ripple se redimensiona solo al tocar el widget.
"""

from kivy.graphics import ClearBuffers, ClearColor, Color, Fbo, Rectangle
from kivymd.uix.behaviors import ripple_behavior


def _init_fbos_seguro(self):
    self._phase = 0.0
    self.ripple_pos = (0, 0)
    tam = (max(self.width, 1), max(self.height, 1))
    self.fbo = Fbo(size=tam, group="m3_ripple_behavior")
    self.set_shader(self.fbo)
    with self.fbo:
        ClearColor(0, 0, 0, 0)
        ClearBuffers()
        Color(1, 1, 1, 1)
        self.rect = Rectangle(pos=(0, 0), size=tam)


def aplicar():
    for nombre in dir(ripple_behavior):
        clase = getattr(ripple_behavior, nombre)
        if isinstance(clase, type) and "init_fbos" in vars(clase):
            clase.init_fbos = _init_fbos_seguro
