# -*- coding: utf-8 -*-
"""Episodios del Plan de Descontaminación Atmosférica (PDA) de Temuco y Padre Las Casas.

En la maqueta el episodio del día es un dato de ejemplo (se puede cambiar para
la demo). En la versión final se obtendría del pronóstico oficial del
Ministerio del Medio Ambiente (airechile.mma.gob.cl).

Los textos son orientativos: las reglas exactas, horarios y excepciones las
informa la autoridad cada día.
"""

URL_OFICIAL = "https://airechile.mma.gob.cl"

# orden de menor a mayor gravedad
ORDEN = ["bueno", "alerta", "preemergencia", "emergencia"]

NIVELES = {
    "bueno": {
        "titulo": "Sin episodio",
        "corto": "Hoy no hay restricciones",
        "icono": "weather-windy",
        "color": (0.106, 0.478, 0.263, 1),
        "hacer": [
            ("fire", "Puedes calefaccionar con normalidad."),
            ("water-off", "Usa leña seca: la húmeda produce más humo y calienta menos."),
        ],
    },
    "alerta": {
        "titulo": "Alerta ambiental",
        "corto": "Evita el humo visible",
        "icono": "alert",
        "color": (0.604, 0.388, 0.0, 1),
        "hacer": [
            ("smoke-detector-variant-alert", "No debe salir humo visible de tu chimenea."),
            ("water-off", "Usa solo leña seca y no apagues la estufa cerrando el tiraje."),
            ("account-heart", "Cuida a niños, adultos mayores y personas con problemas respiratorios."),
        ],
    },
    "preemergencia": {
        "titulo": "Preemergencia ambiental",
        "corto": "Restricción para estufas a leña",
        "icono": "alert-octagon",
        "color": (0.729, 0.176, 0.145, 1),
        "hacer": [
            ("fireplace-off", "Rige la prohibición de usar calefactores a leña en el horario que indique la autoridad."),
            ("radiator", "Si puedes, usa pellet, gas o calefacción eléctrica."),
            ("home-alert", "Evita actividad física al aire libre."),
        ],
    },
    "emergencia": {
        "titulo": "Emergencia ambiental",
        "corto": "Restricción más estricta",
        "icono": "alert-octagram",
        "color": (0.478, 0.106, 0.090, 1),
        "hacer": [
            ("fireplace-off", "Rige la prohibición de usar calefactores a leña. Revisa también si hay restricción para otros artefactos."),
            ("radiator", "Usa la alternativa más limpia que tengas: eléctrica, gas o pellet."),
            ("home-alert", "Mantén a las personas vulnerables bajo techo."),
        ],
    },
}


def siguiente(nivel):
    """Para la demo: pasa al siguiente episodio (bueno → alerta → … → bueno)."""
    return ORDEN[(ORDEN.index(nivel) + 1) % len(ORDEN)]
