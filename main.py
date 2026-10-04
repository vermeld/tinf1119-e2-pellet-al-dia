# -*- coding: utf-8 -*-
"""Pellet al Día — dónde hay pellet o leña seca y alertas PDA en Temuco.

Ejecutar:
    pip install -r requirements.txt
    python main.py
"""

from kivy.config import Config

# En escritorio, el clic derecho de Kivy deja un punto rojo (simula multitáctil).
# Se desactiva; debe ir antes de crear la ventana.
Config.set("input", "mouse", "mouse,multitouch_on_demand")

from app.pelletapp import PelletApp  # noqa: E402

if __name__ == "__main__":
    PelletApp().run()
