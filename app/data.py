# -*- coding: utf-8 -*-
"""Datos de ejemplo (Temuco) usados la primera vez que corre la app.

Los nombres de los locales y de las personas son ficticios. Las coordenadas son
aproximadas y están en los sectores indicados.

Las cuentas de ejemplo no tienen contraseña: no se puede entrar con ellas.
Solo existen para que los puntos tengan reportes y opiniones de otros vecinos.
Para probar la app hay que crear una cuenta propia en la pantalla «Crear cuenta».
"""

from .utils import hace_rato

# id -> nombre visible
USUARIOS_EJEMPLO = {
    1: "Camila R.", 2: "Jorge M.", 3: "Paula V.", 4: "Ignacio S.", 5: "Marcela T.",
    6: "Felipe C.", 7: "Daniela P.", 8: "Rodrigo A.", 9: "Javiera L.", 10: "Tomás V.",
}


def usuarios_iniciales():
    return [
        {"id": uid, "nombre": nombre, "usuario": "vecino%d" % uid,
         "sal": None, "hash": None, "creado": hace_rato(60 * 24 * 30)}
        for uid, nombre in USUARIOS_EJEMPLO.items()
    ]


def _p(id_, nombre, tipo, sector, direccion, lat, lon, hay, sacos, precio,
       desde, hasta, reportes, comentarios=()):
    """reportes: lista de (usuario_id, hay, hace_minutos); el primero es el más nuevo.
    comentarios: lista de (usuario_id, estrellas, texto, hace_minutos, votos)."""
    autor_id, _, minutos = reportes[0]
    return {
        "id": id_, "nombre": nombre, "tipo": tipo, "comuna": sector,
        "direccion": direccion, "lat": lat, "lon": lon,
        "hay": hay, "sacos": sacos, "precio": precio,
        "visto": hace_rato(minutos), "desde": desde, "hasta": hasta,
        "autor": USUARIOS_EJEMPLO[autor_id], "autor_id": autor_id,
        "creador_id": reportes[-1][0],
        "confirmas": sum(1 for _, h, _m in reportes if h == hay) - 1,
        "reportes": [{"uid": u, "hay": h, "t": hace_rato(m)} for u, h, m in reportes],
        "comentarios": [
            {"id": "%d-%d" % (id_, i), "uid": u, "estrellas": e, "texto": t,
             "t": hace_rato(m), "votos": {str(k): v for k, v in votos.items()}}
            for i, (u, e, t, m, votos) in enumerate(comentarios, 1)
        ],
    }


def datos_iniciales():
    puntos = [
        _p(1, "Ferretería Los Aromos", "tienda", "Centro", "Manuel Montt 850",
           -38.73860, -72.59700, True, 40, 5490, "09:00", "20:00",
           [(1, True, 25), (7, True, 70), (8, True, 150), (2, True, 300)],
           [(1, 5, "Llegó camión en la mañana, hay harto. Atienden rápido.", 30,
             {2: 1, 3: 1, 7: 1, 8: 1}),
            (6, 4, "Buen precio para el centro, pero hay fila a la hora de almuerzo.", 400,
             {1: 1, 9: 1})]),
        _p(2, "Copec Av. Alemania", "tienda", "Av. Alemania", "Av. Alemania 0590",
           -38.73720, -72.61080, False, 0, None, "00:00", "23:59",
           [(2, False, 70), (9, False, 120), (1, False, 200)],
           [(2, 2, "Se les acabó ayer y no saben cuándo repone el proveedor.", 75,
             {1: 1, 9: 1, 5: 1})]),
        _p(3, "Don Nelson (vende en su casa)", "persona", "Pueblo Nuevo", "Pasaje Los Copihues 145",
           -38.71650, -72.57900, True, 12, 4990, "10:00", "19:00",
           [(3, True, 160), (10, True, 400)],
           [(3, 5, "Muy amable, el pellet viene seco. Hay que tocar el timbre.", 170,
             {10: 1, 6: 1}),
            (4, 3, "Me costó encontrar el pasaje, pero vale la pena.", 900, {})]),
        _p(4, "Distribuidora Araucanía Pellet", "tienda", "Amanecer", "Av. Javiera Carrera 1440",
           -38.75200, -72.61500, True, 6, 5890, "08:30", "19:00",
           [(4, True, 890)],
           [(4, 3, "Quedaban pocos sacos, parece que se acaba pronto.", 890, {5: -1})]),
        _p(5, "Barraca El Roble", "tienda", "Labranza", "Camino a Labranza 2200",
           -38.76300, -72.72800, False, 0, None, "09:00", "18:00",
           [(5, False, 310), (4, True, 600), (8, False, 700)]),
        _p(6, "Sra. Rosa (vende por saco)", "persona", "Santa Rosa", "Las Quilas 950",
           -38.75550, -72.58850, True, 8, 4800, "10:00", "20:00",
           [(6, True, 40), (4, False, 55), (5, False, 80)],
           [(6, 4, "Vende de a uno o dos sacos, ideal si no tienes auto.", 45, {3: 1, 7: 1}),
            (4, 1, "Fui y me dijeron que no quedaba.", 95, {6: -1, 3: -1, 7: -1})]),
        _p(7, "Ferretería Maquehue", "tienda", "Padre Las Casas", "Av. Maquehue 1020",
           -38.77050, -72.59800, True, 20, 5190, "09:00", "19:30",
           [(7, True, 95), (1, True, 130), (2, True, 260), (8, True, 400), (9, True, 500)],
           [(7, 5, "Siempre tienen stock y dan boleta. Recomendado.", 100,
             {1: 1, 2: 1, 8: 1, 9: 1, 10: 1})]),
        _p(8, "Maderas Fundo El Carmen", "tienda", "Fundo El Carmen", "Av. Los Poetas 01500",
           -38.71000, -72.63500, True, 30, 5390, "08:00", "18:00",
           [(8, True, 15), (1, True, 60)]),
        _p(9, "Minimarket Pedro de Valdivia", "tienda", "Pedro de Valdivia", "Av. Pedro de Valdivia 1350",
           -38.72350, -72.61800, False, 0, None, "08:00", "22:00",
           [(9, False, 20), (2, False, 45), (7, False, 90), (1, True, 600)]),
        _p(10, "Leñería Don Juan", "persona", "Centro", "Lautaro 1180",
           -38.73500, -72.58450, True, 15, 5200, "09:30", "18:30",
           [(10, True, 55), (3, True, 140), (1, True, 220)],
           [(10, 4, "Vende pellet y leña seca. Acepta transferencia.", 60, {1: 1, 3: 1})]),
    ]
    # qué vende cada punto; el resto vende pellet
    combustible = {5: "lena", 7: "ambos", 8: "lena", 10: "ambos"}
    for p in puntos:
        p["combustible"] = combustible.get(p["id"], "pellet")
    return puntos
