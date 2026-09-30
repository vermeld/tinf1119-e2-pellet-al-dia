# -*- coding: utf-8 -*-
"""Pantalla de detalle: info del punto, confiabilidad, reportes y opiniones."""

from kivy.app import App
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget

from .. import confianza, geo
from ..utils import describir, hace, plata
from ..widgets import OpinionCard

EXPLICACION = (
    "De 0 a 5 estrellas, según tres cosas:\n\n"
    "• Frescura (40 %): qué tan reciente es el último reporte. Pierde valor en 12 horas.\n"
    "• Respaldo (40 %): cuántos reportes de las últimas 24 h dicen lo mismo. "
    "Un solo reporte nunca basta.\n"
    "• Reputación (20 %): el nivel de quien reportó. Nuevo, Confiable o Experto.\n\n"
    "Amarillo: 5 estrellas (excelente). Verde: de 2 a 4½. "
    "Rojo: 1½ o menos (poco confiable).\n\n"
    "La reputación sube cuando otros marcan tus opiniones como útiles, "
    "y baja si las marcan como no útiles."
)


class PantallaDetalle(MDScreen):
    punto_id = NumericProperty(0)
    color_estado = ListProperty([0, 0, 0, 1])
    color_conf = ListProperty([0, 0, 0, 1])
    color_conf_texto = ListProperty([0, 0, 0, 1])
    conf_valor = NumericProperty(0)
    promedio = NumericProperty(0)
    tiene_opinion = BooleanProperty(False)
    mi_reporte = StringProperty("")  # 'si', 'no' o '' (no dice)

    def on_pre_enter(self, *args):
        self.mostrar()
        self.cargar_mi_opinion()
        self.ids.scroll.scroll_y = 1

    def mostrar(self):
        app = App.get_running_app()
        p = app.buscar(self.punto_id)
        if p is None:
            return
        d = describir(p)
        i = self.ids
        i.nombre.text = p["nombre"]
        i.subtitulo.text = d["subtitulo"]
        i.estado.text = "Puede que ya no quede" if d["dudoso"] else d["estado"]
        i.icono_estado.icon = d["icono"]
        if d["dudoso"]:
            i.precio.text = "Último dato: %s" % d["estado"].lower()
        elif p["hay"] and p["precio"]:
            i.precio.text = "%s el saco de 15 kg" % plata(p["precio"])
        elif p["hay"]:
            i.precio.text = "Precio no informado"
        else:
            i.precio.text = "Alguien avisó que se acabó"
        i.direccion.texto = "%s, %s" % (p["direccion"], p["comuna"])
        i.distancia.texto = "A " + geo.texto_caminando(
            geo.distancia(app.pos_usuario, (p["lat"], p["lon"])))
        i.horario.texto = d["horario"]
        i.visto.texto = d["visto"]
        self.color_estado = list(getattr(app, d["color"]))

        c = app.confianza(p)
        self.conf_valor = c["estrellas"]
        i.conf_titulo.text = "%s de 5%s" % (
            c["numero"], "" if c["nivel"] == "Confiable" else "\n" + c["nivel"])
        i.conf_detalle.text = c["detalle"]
        self.color_conf = list(getattr(app, c["color"]))
        self.color_conf_texto = list(getattr(app, c["color_texto"]))

        prom, n = confianza.estrellas(p)
        self.promedio = prom
        i.estrellas_txt.text = ("Opiniones: %.1f de 5 (%d)" % (prom, n)).replace(".", ",") \
            if n else "Aún sin opiniones"
        self.mostrar_opiniones(p)

    def mostrar_opiniones(self, p):
        app = App.get_running_app()
        caja = self.ids.opiniones
        caja.clear_widgets()
        if not p["comentarios"]:
            caja.add_widget(MDLabel(text="Nadie ha opinado todavía. ¡Sé el primero!",
                                    theme_text_color="Secondary", adaptive_height=True))
        # las más útiles primero, como en las tiendas de apps
        orden = sorted(p["comentarios"], key=lambda c: (sum(c["votos"].values()), c["t"]),
                       reverse=True)
        yo = str(app.uid) if app.uid else None
        for c in orden:
            autor = app.cuentas.buscar(c["uid"])
            niv = app.nivel(c["uid"])
            caja.add_widget(OpinionCard(
                punto_id=p["id"],
                comentario_id=c["id"],
                autor=autor["nombre"] if autor else "Usuario",
                nivel="%s · %d pts" % (niv["nombre"], niv["puntos"]),
                nivel_icono=niv["icono"],
                estrellas=c["estrellas"],
                texto=c["texto"],
                cuando=hace(c["t"]),
                utiles=sum(1 for v in c["votos"].values() if v > 0),
                no_utiles=sum(1 for v in c["votos"].values() if v < 0),
                mi_voto=c["votos"].get(yo, 0) if yo else 0,
                propia=c["uid"] == app.uid,
            ))
        self.ids.titulo_opiniones.text = "Opiniones de vecinos (%d)" % len(p["comentarios"])

    # ---- tu opinión

    def cargar_mi_opinion(self):
        app = App.get_running_app()
        p = app.buscar(self.punto_id)
        mia = app.mi_opinion(p) if (p and app.con_sesion) else None
        self.tiene_opinion = mia is not None
        self.ids.selector_estrellas.valor = mia["estrellas"] if mia else 0
        self.ids.texto_opinion.text = mia["texto"] if mia else ""
        self.ids.error_opinion.text = ""
        self.mi_reporte = ""

    def publicar_opinion(self):
        app = App.get_running_app()
        estrellas = self.ids.selector_estrellas.valor
        texto = self.ids.texto_opinion.text.strip()
        if not estrellas:
            self.ids.error_opinion.text = "Elige de 1 a 5 estrellas."
            return
        if len(texto) < 5:
            self.ids.error_opinion.text = "Escribe al menos 5 caracteres."
            self.ids.texto_opinion.focus = True
            return
        if len(texto) > 280:
            self.ids.error_opinion.text = "Máximo 280 caracteres (llevas %d)." % len(texto)
            return
        hay = {"si": True, "no": False}.get(self.mi_reporte)
        if app.opinar(self.punto_id, estrellas, texto, hay):
            nueva = not self.tiene_opinion
            self.mostrar()
            self.cargar_mi_opinion()
            app.avisar("¡Gracias! Tu opinión ya está publicada." if nueva
                       else "Actualizaste tu opinión.")

    def votar(self, comentario_id, valor):
        app = App.get_running_app()
        if app.votar(self.punto_id, comentario_id, valor):
            self.mostrar_opiniones(app.buscar(self.punto_id))

    # ---- reportar stock

    def explicar_confianza(self):
        dialogo = MDDialog(
            MDDialogIcon(icon="shield-check"),
            MDDialogHeadlineText(text="Confiabilidad del dato"),
            MDDialogSupportingText(text=EXPLICACION, halign="left"),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(MDButtonText(text="Entendido"), style="text",
                         on_release=lambda *a: dialogo.dismiss()),
            ),
        )
        dialogo.open()

    def pedir_confirmacion(self, hay):
        """Pide confirmar antes de cambiar el dato que ven todos."""
        app = App.get_running_app()
        if not app.requiere_cuenta("reportar el stock"):
            return
        if hay:
            titulo, texto, icono = (
                "¿Confirmas que hay pellet?",
                "Se marcará como visto ahora y sumará una confirmación.",
                "check-circle",
            )
        else:
            titulo, texto, icono = (
                "¿Confirmas que ya no hay?",
                "El punto quedará como «Sin stock» para todos.",
                "close-circle",
            )

        self._dialogo = MDDialog(
            MDDialogIcon(icon=icono),
            MDDialogHeadlineText(text=titulo),
            MDDialogSupportingText(text=texto),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(MDButtonText(text="Cancelar"), style="text",
                         on_release=lambda *a: self._dialogo.dismiss()),
                MDButton(MDButtonText(text="Sí, confirmar"), style="filled",
                         on_release=lambda *a: self._confirmar(hay)),
                spacing="8dp",
            ),
        )
        self._dialogo.open()

    def _confirmar(self, hay):
        self._dialogo.dismiss()
        app = App.get_running_app()
        if app.confirmar(self.punto_id, hay):
            self.mostrar()
            app.avisar("¡Gracias! Actualizaste el punto para todos.")
