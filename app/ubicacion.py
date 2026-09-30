# -*- coding: utf-8 -*-
"""Ubicación del usuario: GPS real en Android y simulada en escritorio."""

from kivy.clock import Clock
from kivy.utils import platform

from . import geo


class Ubicacion:
    """Mantiene app.pos_usuario al día.

    - Android: usa el GPS del teléfono (plyer).
    - Escritorio: parte en la Plaza Aníbal Pinto y permite simular una caminata
      por la ruta, para la demo.
    """

    def __init__(self, app):
        self.app = app
        self._evento = None
        self._ruta = None
        self._recorrido = 0

    def iniciar(self):
        if platform == "android":
            try:
                from android.permissions import Permission, request_permissions
                request_permissions([Permission.ACCESS_FINE_LOCATION,
                                     Permission.ACCESS_COARSE_LOCATION])
                from plyer import gps
                gps.configure(on_location=self._on_gps)
                gps.start(minTime=1000, minDistance=1)
                self.app.hay_gps = True
            except Exception:  # sin permiso o sin GPS: seguimos con la simulada
                self.app.hay_gps = False

    @property
    def hay_gps(self):
        return self.app.hay_gps

    def _on_gps(self, **datos):
        # plyer llama desde otro hilo: pasamos el dato al hilo de Kivy
        pos = (datos["lat"], datos["lon"])
        Clock.schedule_once(lambda dt: self.mover_a(pos))

    def mover_a(self, pos):
        self.app.pos_usuario = [pos[0], pos[1]]

    # ---- caminata simulada (escritorio)

    @property
    def simulando(self):
        return self._evento is not None

    def simular(self, ruta, velocidad):
        """Avanza por la ruta a 'velocidad' m/s, desde donde estás ahora."""
        self.detener()
        self._velocidad = velocidad
        self._ruta = ruta
        self._total = geo.largo(ruta)
        self._recorrido = geo.largo(ruta[:geo.mas_cercano(ruta, self.app.pos_usuario) + 1])
        self._evento = Clock.schedule_interval(self._paso, 1 / 15)

    def _paso(self, dt):
        self._recorrido += self._velocidad * dt
        pos, _ = geo.punto_en(self._ruta, self._recorrido)
        self.mover_a(pos)
        if self._recorrido >= self._total:
            self.detener()

    def detener(self):
        if self._evento is not None:
            self._evento.cancel()
            self._evento = None
