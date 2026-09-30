# -*- coding: utf-8 -*-
"""Cuentas de usuario: registro, inicio de sesión y reputación.

Las contraseñas nunca se guardan en texto plano: se guarda un hash PBKDF2-SHA256
con una "sal" aleatoria por usuario. Por ahora todo se guarda en el dispositivo
(usuarios.json). Con un servidor, esta misma lógica pasaría al backend.
"""

import hashlib
import hmac
import json
import os
import re
import secrets
from datetime import datetime

from .data import usuarios_iniciales

ITERACIONES = 120_000

# Reputación: cuántos puntos da cada acción
PTS_VOTO_UTIL = 2        # alguien marcó tu opinión como útil
PTS_VOTO_NO_UTIL = -2    # alguien la marcó como no útil
PTS_REPORTE = 1          # reportaste si había o no había
PTS_PUBLICAR = 2         # publicaste un punto nuevo
PTS_OPINION = 1          # escribiste una opinión

# (puntos mínimos, nombre, peso de sus reportes en la confiabilidad, ícono)
NIVELES = [
    (0, "Nuevo", 0.5, "account-outline"),
    (6, "Confiable", 0.8, "account-check"),
    (15, "Experto", 1.0, "shield-star"),
]


def _hash(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), bytes.fromhex(sal), ITERACIONES).hex()


def validar_registro(nombre, usuario, clave, clave2):
    """Devuelve (campo, mensaje) con el primer error, o None si todo está bien."""
    if len(nombre.strip()) < 2:
        return "nombre", "Escribe tu nombre (como te verán los demás)."
    if not re.fullmatch(r"[a-zA-Z0-9._]{3,20}", usuario):
        return "usuario", "El usuario debe tener de 3 a 20 letras, números, punto o guion bajo."
    if len(clave) < 6:
        return "clave", "La contraseña debe tener al menos 6 caracteres."
    if clave != clave2:
        return "clave2", "Las contraseñas no coinciden."
    return None


class Cuentas:
    def __init__(self, carpeta):
        self.archivo = os.path.join(carpeta, "usuarios.json")
        self.usuarios = []
        self.sesion_id = None
        self.cargar()

    # ---- archivo

    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                self.usuarios = datos["usuarios"]
                self.sesion_id = datos.get("sesion")
                return
            except (ValueError, OSError, KeyError):
                pass
        self.usuarios = usuarios_iniciales()
        self.sesion_id = None

    def guardar(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({"usuarios": self.usuarios, "sesion": self.sesion_id},
                          f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    # ---- sesión

    def buscar(self, uid):
        for u in self.usuarios:
            if u["id"] == uid:
                return u
        return None

    def por_usuario(self, usuario):
        usuario = usuario.strip().lower()
        for u in self.usuarios:
            if u["usuario"].lower() == usuario:
                return u
        return None

    @property
    def actual(self):
        return self.buscar(self.sesion_id) if self.sesion_id else None

    def registrar(self, nombre, usuario, clave):
        """Crea la cuenta y deja la sesión abierta. Devuelve (ok, mensaje)."""
        if self.por_usuario(usuario):
            return False, "Ese nombre de usuario ya existe. Prueba con otro."
        sal = secrets.token_hex(16)
        u = {
            "id": max([x["id"] for x in self.usuarios], default=0) + 1,
            "nombre": nombre.strip(),
            "usuario": usuario.strip(),
            "sal": sal,
            "hash": _hash(clave, sal),
            "creado": datetime.now().isoformat(timespec="seconds"),
        }
        self.usuarios.append(u)
        self.sesion_id = u["id"]
        self.guardar()
        return True, "¡Bienvenido/a, %s!" % u["nombre"]

    def entrar(self, usuario, clave):
        u = self.por_usuario(usuario)
        # mismo mensaje en ambos casos: no revelamos qué usuarios existen
        if u is None or not u["hash"] or not hmac.compare_digest(_hash(clave, u["sal"]), u["hash"]):
            return False, "Usuario o contraseña incorrectos."
        self.sesion_id = u["id"]
        self.guardar()
        return True, "Hola de nuevo, %s." % u["nombre"]

    def salir(self):
        self.sesion_id = None
        self.guardar()

    # ---- reputación

    def estadisticas(self, uid, puntos):
        e = {"publicados": 0, "reportes": 0, "opiniones": 0, "utiles": 0, "no_utiles": 0}
        clave = str(uid)
        for p in puntos:
            if p.get("creador_id") == uid:
                e["publicados"] += 1
            e["reportes"] += sum(1 for r in p.get("reportes", []) if r["uid"] == uid)
            for c in p.get("comentarios", []):
                if c["uid"] == uid:
                    e["opiniones"] += 1
                    e["utiles"] += sum(1 for k, v in c["votos"].items() if v > 0 and k != clave)
                    e["no_utiles"] += sum(1 for k, v in c["votos"].items() if v < 0 and k != clave)
        e["puntos"] = max(0, e["publicados"] * PTS_PUBLICAR + e["reportes"] * PTS_REPORTE
                          + e["opiniones"] * PTS_OPINION + e["utiles"] * PTS_VOTO_UTIL
                          + e["no_utiles"] * PTS_VOTO_NO_UTIL)
        return e

    def nivel(self, uid, puntos):
        """Devuelve un dict con nombre, peso, ícono, puntos y cuánto falta para subir."""
        pts = self.estadisticas(uid, puntos)["puntos"]
        actual = NIVELES[0]
        siguiente = None
        for i, niv in enumerate(NIVELES):
            if pts >= niv[0]:
                actual = niv
                siguiente = NIVELES[i + 1] if i + 1 < len(NIVELES) else None
        return {
            "nombre": actual[1], "peso": actual[2], "icono": actual[3], "puntos": pts,
            "siguiente": siguiente[1] if siguiente else None,
            "faltan": (siguiente[0] - pts) if siguiente else 0,
            "progreso": 100 if not siguiente else
            100 * (pts - actual[0]) / (siguiente[0] - actual[0]),
        }
