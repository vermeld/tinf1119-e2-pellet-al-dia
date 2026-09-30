# -*- coding: utf-8 -*-
"""Genera los íconos del mapa (pines de colores y punto "tú estás aquí").

Se ejecuta una sola vez:  python tools/generar_iconos.py
Requiere Pillow (pip install pillow). La app solo usa los PNG ya generados.
"""

import os

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "assets")
S = 4  # supersampling para bordes suaves

COLORES = {
    "pin_hay": (27, 122, 67),
    "pin_nohay": (186, 45, 37),
    "pin_duda": (154, 99, 0),
    "pin_elegir": (33, 33, 33),  # pin fijo al centro para elegir ubicación
}


def pin(color, ancho=44, alto=60):
    w, h = ancho * S, alto * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = w // 2 - 2 * S
    cx, cy = w // 2, r + 2 * S
    # sombra suave en la base
    d.ellipse([cx - 7 * S, h - 7 * S, cx + 7 * S, h - 1 * S], fill=(0, 0, 0, 70))
    # gota: círculo + triángulo hacia la punta
    borde = (255, 255, 255, 255)
    d.polygon([(cx - r * 0.72, cy + r * 0.62), (cx + r * 0.72, cy + r * 0.62), (cx, h - 4 * S)], fill=borde)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=borde)
    r2 = r - 3 * S
    d.polygon([(cx - r2 * 0.70, cy + r2 * 0.66), (cx + r2 * 0.70, cy + r2 * 0.66), (cx, h - 8 * S)], fill=color)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=color)
    # centro blanco
    r3 = r2 * 0.42
    d.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=borde)
    return im.resize((ancho, alto), Image.LANCZOS)


def yo(tam=34):
    w = tam * S
    im = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, w, w], fill=(26, 115, 232, 60))          # halo
    m = w * 0.22
    d.ellipse([m, m, w - m, w - m], fill=(255, 255, 255, 255))  # borde
    m2 = w * 0.30
    d.ellipse([m2, m2, w - m2, w - m2], fill=(26, 115, 232, 255))
    return im.resize((tam, tam), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for nombre, color in COLORES.items():
        pin(color).save(os.path.join(SALIDA, nombre + ".png"))
    yo().save(os.path.join(SALIDA, "yo.png"))
    print("Íconos generados en", os.path.abspath(SALIDA))
