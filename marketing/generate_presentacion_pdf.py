#!/usr/bin/env python3
"""Generate SmartApps Seguros commercial presentation PDF."""

from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "SmartApps-Seguros-Presentacion-Comercial.pdf"

BLUE = (11, 107, 203)
VIOLET = (123, 63, 228)
MAGENTA = (224, 17, 138)
INK = (18, 36, 63)
MUTED = (74, 93, 120)
SOFT = (245, 248, 255)
LINE = (217, 227, 242)
WHITE = (255, 255, 255)


FONT = "DejaVu"
FONT_B = "DejaVu"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


class Deck(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font(FONT, "", str(FONT_DIR / "DejaVuSans.ttf"))
        self.add_font(FONT, "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*LINE)
        self.set_line_width(0.2)
        if (ASSETS / "smartapps-seguros-logo.png").exists():
            self.image(str(ASSETS / "smartapps-seguros-logo.png"), 14, 8, 10)
        self.set_xy(26, 9)
        self.set_font(FONT, "B", 9)
        self.set_text_color(*INK)
        self.cell(80, 6, "SmartApps Seguros")
        self.set_xy(-60, 9)
        self.set_font(FONT, "", 8)
        self.set_text_color(*MUTED)
        self.cell(46, 6, "Presentación comercial", align="R")
        self.line(14, 20, 196, 20)
        self.set_y(24)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_draw_color(*LINE)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_y(-12)
        self.set_font(FONT, "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"SmartApps Seguros  |  Página {self.page_no() - 1}/4  |  Documento de presentación", align="C")

    def h1(self, text):
        self.set_font(FONT, "B", 18)
        self.set_text_color(*BLUE)
        self.multi_cell(0, 9, text)
        self.ln(2)

    def h2(self, text):
        self.set_font(FONT, "B", 12)
        self.set_text_color(*INK)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font(FONT, "", 10)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 5.2, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*VIOLET)
        self.ellipse(x + 1, y + 1.7, 2.2, 2.2, style="F")
        self.set_xy(x + 7, y)
        self.set_font(FONT, "", 9.5)
        self.set_text_color(*MUTED)
        if bold_prefix:
            self.set_font(FONT, "B", 9.5)
            self.set_text_color(*INK)
            w = self.get_string_width(bold_prefix + " ")
            self.cell(w, 5, bold_prefix + " ")
            self.set_font(FONT, "", 9.5)
            self.set_text_color(*MUTED)
            self.multi_cell(0, 5, text)
        else:
            self.multi_cell(0, 5, text)
        self.ln(1)

    def card_box(self, x, y, w, h, title, lines):
        self.set_fill_color(*SOFT)
        self.set_draw_color(*LINE)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 4, y + 3)
        self.set_font(FONT, "B", 10)
        self.set_text_color(*INK)
        self.cell(w - 8, 6, title)
        self.set_xy(x + 4, y + 11)
        self.set_font(FONT, "", 8.5)
        self.set_text_color(*MUTED)
        for line in lines:
            self.set_x(x + 4)
            self.multi_cell(w - 8, 4.4, f"• {line}")


def build():
    pdf = Deck(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 14, 14)

    # ---- COVER ----
    pdf.add_page()
    if (ASSETS / "smartapps-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-logo.png"), 14, 16, 16)
    pdf.set_xy(33, 18)
    pdf.set_font(FONT, "B", 9)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, "SMARTAPPS  |  SUITE EMPRESARIAL")
    pdf.set_xy(33, 24)
    pdf.set_font(FONT, "", 8)
    pdf.cell(0, 5, "Presentación comercial del proyecto")

    if (ASSETS / "smartapps-seguros-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-seguros-logo.png"), 14, 48, 42)

    pdf.set_xy(62, 52)
    pdf.set_font(FONT, "B", 26)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 11, "SmartApps Seguros")
    pdf.set_xy(62, 64)
    pdf.set_font(FONT, "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(120, 5.5, "ERP SaaS para la administración integral de empresas de seguros")

    # Slogan banner
    pdf.set_fill_color(*BLUE)
    pdf.rect(14, 105, 182, 38, style="F")
    pdf.set_xy(20, 112)
    pdf.set_font(FONT, "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(170, 7, '"Todo tu negocio de seguros, en un solo lugar."')
    pdf.set_xy(20, 128)
    pdf.set_font(FONT, "", 10)
    pdf.multi_cell(170, 5, "Un solo sistema para cotizar, administrar cartera, comisiones y atender clientes.")

    pdf.set_xy(14, 160)
    pdf.set_font(FONT, "B", 11)
    pdf.set_text_color(*INK)
    pdf.cell(0, 7, "Nuestra promesa", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 10)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 5.5, "Un solo sistema para administrar todo tu negocio de seguros.")

    pdf.set_xy(14, 185)
    for i, (title, desc) in enumerate([
        ("Cotiza y cierra", "WhatsApp + web móvil\nManual o API"),
        ("Opera y retiene", "Cartera, renovaciones\ny comisiones"),
        ("Decide con datos", "Panel CEO por ramo,\nagente y periodo"),
    ]):
        x = 14 + i * 62
        pdf.set_fill_color(*SOFT)
        pdf.set_draw_color(*LINE)
        pdf.rect(x, 185, 58, 32, style="DF")
        pdf.set_xy(x + 4, 189)
        pdf.set_font(FONT, "B", 10)
        pdf.set_text_color(*BLUE)
        pdf.cell(50, 6, title)
        pdf.set_xy(x + 4, 197)
        pdf.set_font(FONT, "", 8.5)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(50, 4.2, desc)

    pdf.set_xy(14, 250)
    pdf.set_font(FONT, "B", 9)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, "Desarrollado por SmartApps", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 8.5)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 4.5, "Plataforma SaaS multi-tenant para agentes, promotorías y brokers en México y Latinoamérica.")

    # ---- PAGE 2: VALUE + SLOGANS ----
    pdf.add_page()
    pdf.h1("Por qué SmartApps Seguros")
    pdf.body(
        "Plataforma tecnológica desarrollada por SmartApps para transformar la operación de agentes, "
        "promotorías y empresas del sector asegurador: comercial, administrativa y financiera en un solo lugar."
    )

    pdf.h2("Eslogan y mensajes de venta")
    for bold, rest in [
        ("Todo tu negocio de seguros, en un solo lugar.", ""),
        ("Deja el Excel.", "Lleva tu agencia a la nube."),
        ("Cotiza hoy. Renueva siempre.", "Cobra tus comisiones a tiempo."),
        ("Tu oficina, tu marca, tus reglas", "- en un ERP SaaS."),
        ("Un solo sistema", "para administrar todo tu negocio de seguros."),
    ]:
        pdf.bullet(rest, bold_prefix=bold)

    pdf.ln(3)
    pdf.h2("Para quien es")
    for t in [
        "Agentes y oficinas independientes",
        "Promotorias y brokers",
        "Equipos multiagente / multi sucursal",
        "Quien vende por WhatsApp y necesita orden operativo y financiero",
    ]:
        pdf.bullet(t)

    pdf.ln(3)
    y = pdf.get_y()
    pdf.card_box(14, y, 88, 42, "Mision (resumen)", [
        "Impulsar la transformación digital del sector asegurador",
        "Plataforma segura, intuitiva y escalable",
        "Mayor productividad y rentabilidad",
    ])
    pdf.card_box(108, y, 88, 42, "Vision (resumen)", [
        "Ser la plataforma SaaS líder en MX y LATAM",
        "Reconocida por innovación y confiabilidad",
        "Tecnologia de clase mundial para seguros",
    ])
    pdf.set_y(y + 48)

    # ---- PAGE 3: FEATURES ----
    pdf.add_page()
    pdf.h1("Características del sistema")
    pdf.body("Capacidades definidas en el diseno del producto (núcleo confirmado).")

    features = [
        ("Cotizacion WhatsApp", "Flujo conversacional y envío de enlace web"),
        ("Cotizador web móvil", "Wizard completo desde el celular"),
        ("Manual / API / mixto", "Activa aseguradoras al tener sandbox"),
        ("Agenda y seguimientos", "Citas, tareas y recordatorios"),
        ("Cartera de clientes", "Pólizas, ramos, estatus y documentos"),
        ("Renovaciones automáticas", "Alertas 45/30/15/7 días"),
        ("Comisiones por aseguradora", "Tablas % que paga cada compañía"),
        ("Comisiones internas", "Split por usuario / vendedor"),
        ("Facturación a compañías", "Pendiente / facturada / por pagar / pagada"),
        ("Panel CEO", "Cotizaciones, ventas y cortes por ramo"),
        ("Portal del cliente", "Pólizas, vencimientos y documentos"),
        ("Push + PWA", "Agregar a inicio iPhone / Android"),
        ("Marca de la oficina", "Logo, datos, direcciones, correo"),
        ("Usuarios y permisos", "CEO, admin, vendedor, asistente"),
        ("Auditoria", "Quien hizo que y cuando"),
        ("Multi razón social + SAT", "Varios RFC y certificados CSD"),
    ]

    col_w = 90
    start_y = pdf.get_y()
    for i, (title, desc) in enumerate(features):
        col = i % 2
        row = i // 2
        x = 14 + col * (col_w + 4)
        y = start_y + row * 14
        if y > 270:
            break
        pdf.set_fill_color(*SOFT)
        pdf.set_draw_color(*LINE)
        pdf.rect(x, y, col_w, 12.5, style="DF")
        pdf.set_xy(x + 3, y + 1.5)
        pdf.set_font(FONT, "B", 8.5)
        pdf.set_text_color(*INK)
        pdf.cell(col_w - 6, 4.5, title)
        pdf.set_xy(x + 3, y + 6.2)
        pdf.set_font(FONT, "", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(col_w - 6, 4, desc)

    # ---- PAGE 4: MODULES + ROADMAP ----
    pdf.add_page()
    pdf.h1("Arquitectura y expansión")
    pdf.body(
        "Cada capacidad vive en un modulo (mod-*). Las nuevas funciones se agregan sin romper el resto del sistema."
    )

    pdf.h2("Tipos de modulo")
    rows = [
        ("Core", "Tenancy, usuarios, config, SAT, auditoria", "Oficina aislada y configurable"),
        ("Comercial", "Cotizacion, WhatsApp, web, APIs", "Captas y cotizas más rápido"),
        ("Operacion", "Cartera, agenda, renovaciones, comisiones", "Retienes cartera y cobras bien"),
        ("Experiencia", "Portal agente, cliente, CEO, PWA", "Cada actor ve lo suyo"),
    ]
    # table header
    pdf.set_fill_color(*SOFT)
    pdf.set_draw_color(*LINE)
    pdf.set_font(FONT, "B", 8.5)
    pdf.set_text_color(*INK)
    for i, h in enumerate(["Tipo", "Modulos", "Beneficio"]):
        w = [28, 90, 64][i]
        pdf.cell(w, 7, h, border=1, fill=True)
    pdf.ln()
    pdf.set_font(FONT, "", 8)
    pdf.set_text_color(*MUTED)
    for tipo, mods, ben in rows:
        pdf.set_font(FONT, "B", 8)
        pdf.set_text_color(*INK)
        pdf.cell(28, 8, tipo, border=1)
        pdf.set_font(FONT, "", 8)
        pdf.set_text_color(*MUTED)
        pdf.cell(90, 8, mods, border=1)
        pdf.cell(64, 8, ben, border=1)
        pdf.ln()

    pdf.ln(6)
    pdf.h2("En roadmap (ideas ERP / AMS)")
    y = pdf.get_y()
    pdf.card_box(14, y, 88, 48, "Operacion avanzada", [
        "Recibos de prima y cobranza / mora",
        "Conciliación de borderó / planilla",
        "Siniestros ligeros",
        "Endosos y cancelaciones",
    ])
    pdf.card_box(108, y, 88, 48, "Crecimiento comercial", [
        "Embudo de ventas y bitácora 360",
        "Bandeja WhatsApp multiagente",
        "Cross-sell por ramo",
        "Export contable e integraciones",
    ])
    pdf.set_y(y + 56)

    pdf.set_fill_color(*SOFT)
    pdf.rect(14, pdf.get_y(), 182, 22, style="F")
    pdf.set_xy(18, pdf.get_y() + 5)
    pdf.set_font(FONT, "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.multi_cell(174, 5.5, '"La tecnología debe trabajar para las personas, no las personas para la tecnología."')

    pdf.ln(10)
    pdf.set_font(FONT, "B", 14)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 8, "Solicita una demo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 9)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, "Todo tu negocio de seguros, en un solo lugar.  |  Desarrollado por SmartApps", align="C")

    # ---- PAGE 5: CLOSE ----
    pdf.add_page()
    if (ASSETS / "smartapps-seguros-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-seguros-logo.png"), 80, 55, 50)
    pdf.set_y(115)
    pdf.set_font(FONT, "B", 24)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 12, "SmartApps Seguros", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "B", 13)
    pdf.set_text_color(*VIOLET)
    pdf.multi_cell(0, 7, '"Todo tu negocio de seguros, en un solo lugar."', align="C")
    pdf.ln(4)
    pdf.set_font(FONT, "", 10)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        5.5,
        "Cotiza por WhatsApp o web. Administra cartera y comisiones.\n"
        "Atiende a tus clientes con portal y alertas. Decide con el panel CEO.",
        align="C",
    )
    pdf.ln(10)
    pdf.set_fill_color(*BLUE)
    pdf.rect(65, pdf.get_y(), 80, 12, style="F")
    pdf.set_text_color(*WHITE)
    pdf.set_font(FONT, "B", 11)
    pdf.cell(0, 12, "Solicita una demo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(14)
    pdf.set_font(FONT, "", 9)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 5, "Desarrollado por SmartApps", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "ERP SaaS para la administración integral de empresas de seguros", align="C")

    pdf.output(str(OUT))
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
