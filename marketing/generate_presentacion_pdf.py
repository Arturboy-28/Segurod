#!/usr/bin/env python3
"""Generate SmartApps Seguros commercial presentation PDF."""

from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "SmartApps-Seguros-Presentacion-Comercial.pdf"

BLUE = (11, 107, 203)
VIOLET = (123, 63, 228)
INK = (18, 36, 63)
MUTED = (74, 93, 120)
SOFT = (245, 248, 255)
LINE = (217, 227, 242)
WHITE = (255, 255, 255)

FONT = "DejaVu"
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
            self.image(str(ASSETS / "smartapps-seguros-logo.png"), 14, 7, 12)
        self.set_xy(28, 8)
        self.set_font(FONT, "B", 12)
        self.set_text_color(*INK)
        self.cell(80, 7, "SmartApps Seguros")
        self.set_xy(-70, 8)
        self.set_font(FONT, "", 10)
        self.set_text_color(*MUTED)
        self.cell(56, 7, "Presentación comercial", align="R")
        self.line(14, 21, 196, 21)
        self.set_y(26)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_draw_color(*LINE)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_y(-12)
        self.set_font(FONT, "", 9)
        self.set_text_color(*MUTED)
        self.cell(
            0,
            6,
            f"SmartApps Seguros  |  Página {self.page_no() - 1}/4  |  Documento de presentación",
            align="C",
        )

    def h1(self, text):
        self.set_font(FONT, "B", 24)
        self.set_text_color(*BLUE)
        self.multi_cell(0, 11, text)
        self.ln(3)

    def h2(self, text):
        self.set_font(FONT, "B", 15)
        self.set_text_color(*INK)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body(self, text):
        self.set_font(FONT, "", 12)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 6.5, text)
        self.ln(3)

    def bullet(self, text, bold_prefix=""):
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(*VIOLET)
        self.ellipse(x + 1, y + 2.2, 2.6, 2.6, style="F")
        self.set_xy(x + 8, y)
        if bold_prefix:
            self.set_font(FONT, "B", 12)
            self.set_text_color(*INK)
            w = self.get_string_width(bold_prefix + " ")
            self.cell(w, 6.5, bold_prefix + " ")
            self.set_font(FONT, "", 12)
            self.set_text_color(*MUTED)
            self.multi_cell(0, 6.5, text)
        else:
            self.set_font(FONT, "", 12)
            self.set_text_color(*MUTED)
            self.multi_cell(0, 6.5, text)
        self.ln(2)

    def card_box(self, x, y, w, h, title, lines):
        self.set_fill_color(*SOFT)
        self.set_draw_color(*LINE)
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 5, y + 4)
        self.set_font(FONT, "B", 12)
        self.set_text_color(*INK)
        self.cell(w - 10, 7, title)
        self.set_xy(x + 5, y + 13)
        self.set_font(FONT, "", 10.5)
        self.set_text_color(*MUTED)
        for line in lines:
            self.set_x(x + 5)
            self.multi_cell(w - 10, 5.4, f"• {line}")


def build():
    pdf = Deck(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 14, 14)

    # ---- COVER ----
    pdf.add_page()
    if (ASSETS / "smartapps-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-logo.png"), 14, 14, 18)
    pdf.set_xy(36, 16)
    pdf.set_font(FONT, "B", 11)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "SMARTAPPS  |  SUITE EMPRESARIAL")
    pdf.set_xy(36, 23)
    pdf.set_font(FONT, "", 10)
    pdf.cell(0, 6, "Presentación comercial del proyecto")

    if (ASSETS / "smartapps-seguros-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-seguros-logo.png"), 14, 42, 48)

    pdf.set_xy(68, 48)
    pdf.set_font(FONT, "B", 30)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 13, "SmartApps Seguros")
    pdf.set_xy(68, 63)
    pdf.set_font(FONT, "", 13)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(125, 6.5, "ERP SaaS para la administración integral de empresas de seguros")

    # Slogan banner
    pdf.set_fill_color(*BLUE)
    pdf.rect(14, 100, 182, 48, style="F")
    pdf.set_xy(20, 108)
    pdf.set_font(FONT, "B", 18)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(170, 9, '"Todo tu negocio de seguros, en un solo lugar."')
    pdf.set_xy(20, 128)
    pdf.set_font(FONT, "", 12)
    pdf.multi_cell(
        170,
        6,
        "Creando alianzas que impulsan tu negocio de seguros.\n"
        "Un solo sistema para cotizar, administrar cartera, comisiones y atender clientes.",
    )

    pdf.set_xy(14, 160)
    pdf.set_font(FONT, "B", 14)
    pdf.set_text_color(*INK)
    pdf.cell(0, 8, "Nuestra promesa", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 12)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 6.5, "Un solo sistema para administrar todo tu negocio de seguros.")

    pdf.set_xy(14, 185)
    for i, (title, desc) in enumerate(
        [
            ("Cotiza y cierra", "WhatsApp + web móvil\nManual o API"),
            ("Opera y retiene", "Cartera, renovaciones\ny comisiones"),
            ("Decide con datos", "Panel CEO por ramo,\nagente y periodo"),
        ]
    ):
        x = 14 + i * 62
        pdf.set_fill_color(*SOFT)
        pdf.set_draw_color(*LINE)
        pdf.rect(x, 185, 58, 38, style="DF")
        pdf.set_xy(x + 4, 190)
        pdf.set_font(FONT, "B", 12)
        pdf.set_text_color(*BLUE)
        pdf.cell(50, 7, title)
        pdf.set_xy(x + 4, 200)
        pdf.set_font(FONT, "", 10.5)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(50, 5.2, desc)

    pdf.set_xy(14, 245)
    pdf.set_font(FONT, "B", 12)
    pdf.set_text_color(*INK)
    pdf.cell(0, 7, "Desarrollado por SmartApps", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        5.5,
        "Plataforma SaaS multi-tenant para agentes, promotorías y brokers en México y Latinoamérica.",
    )

    # ---- PAGE 2 ----
    pdf.add_page()
    pdf.h1("Por qué SmartApps Seguros")
    pdf.body(
        "Plataforma tecnológica desarrollada por SmartApps para transformar la operación de agentes, "
        "promotorías y empresas del sector asegurador: comercial, administrativa y financiera en un solo lugar."
    )

    pdf.h2("Eslogan y mensajes de venta")
    for bold, rest in [
        ("Todo tu negocio de seguros, en un solo lugar.", ""),
        ("Creando alianzas que impulsan tu negocio de seguros.", ""),
        ("Deja el Excel.", "Lleva tu agencia a la nube."),
        ("Cotiza hoy. Renueva siempre.", "Cobra tus comisiones a tiempo."),
        ("Tu oficina, tu marca, tus reglas", "- en un ERP SaaS."),
        ("Un solo sistema", "para administrar todo tu negocio de seguros."),
    ]:
        pdf.bullet(rest, bold_prefix=bold)

    pdf.ln(2)
    pdf.h2("Para quién es")
    for t in [
        "Agentes y oficinas independientes",
        "Promotorías y brokers",
        "Equipos multiagente / multi sucursal",
        "Quien vende por WhatsApp y necesita orden operativo y financiero",
    ]:
        pdf.bullet(t)

    pdf.ln(2)
    y = pdf.get_y()
    pdf.card_box(
        14,
        y,
        88,
        52,
        "Misión (resumen)",
        [
            "Impulsar la transformación digital del sector asegurador",
            "Plataforma segura, intuitiva y escalable",
            "Mayor productividad y rentabilidad",
        ],
    )
    pdf.card_box(
        108,
        y,
        88,
        52,
        "Visión (resumen)",
        [
            "Ser la plataforma SaaS líder en MX y LATAM",
            "Reconocida por innovación y confiabilidad",
            "Tecnología de clase mundial para seguros",
        ],
    )

    # ---- PAGE 3: FEATURES ----
    pdf.add_page()
    pdf.h1("Características del sistema")
    pdf.body("Capacidades definidas en el diseño del producto (núcleo confirmado).")

    features = [
        ("Cotización WhatsApp", "Flujo conversacional y envío de enlace web"),
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
        ("Auditoría", "Quién hizo qué y cuándo"),
        ("Multi razón social + SAT", "Varios RFC y certificados CSD"),
    ]

    col_w = 90
    row_h = 15.5
    start_y = pdf.get_y()
    for i, (title, desc) in enumerate(features):
        col = i % 2
        row = i // 2
        x = 14 + col * (col_w + 4)
        y = start_y + row * row_h
        if y > 268:
            break
        pdf.set_fill_color(*SOFT)
        pdf.set_draw_color(*LINE)
        pdf.rect(x, y, col_w, row_h - 1.2, style="DF")
        pdf.set_xy(x + 3, y + 1.8)
        pdf.set_font(FONT, "B", 11)
        pdf.set_text_color(*INK)
        pdf.cell(col_w - 6, 5.5, title)
        pdf.set_xy(x + 3, y + 7.5)
        pdf.set_font(FONT, "", 9.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(col_w - 6, 5, desc)

    # ---- PAGE 4 ----
    pdf.add_page()
    pdf.h1("Arquitectura y expansión")
    pdf.body(
        "Cada capacidad vive en un módulo (mod-*). Las nuevas funciones se agregan sin romper el resto del sistema."
    )

    pdf.h2("Tipos de módulo")
    rows = [
        ("Core", "Tenancy, usuarios, config, SAT, auditoría", "Oficina aislada y configurable"),
        ("Comercial", "Cotización, WhatsApp, web, APIs", "Captas y cotizas más rápido"),
        ("Operación", "Cartera, agenda, renovaciones, comisiones", "Retienes cartera y cobras bien"),
        ("Experiencia", "Portal agente, cliente, CEO, PWA", "Cada actor ve lo suyo"),
    ]
    pdf.set_fill_color(*SOFT)
    pdf.set_draw_color(*LINE)
    pdf.set_font(FONT, "B", 11)
    pdf.set_text_color(*INK)
    for i, h in enumerate(["Tipo", "Módulos", "Beneficio"]):
        w = [30, 88, 64][i]
        pdf.cell(w, 9, h, border=1, fill=True)
    pdf.ln()
    for tipo, mods, ben in rows:
        pdf.set_font(FONT, "B", 10.5)
        pdf.set_text_color(*INK)
        pdf.cell(30, 10, tipo, border=1)
        pdf.set_font(FONT, "", 10.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(88, 10, mods, border=1)
        pdf.cell(64, 10, ben, border=1)
        pdf.ln()

    pdf.ln(6)
    pdf.h2("En roadmap (ideas ERP / AMS)")
    y = pdf.get_y()
    pdf.card_box(
        14,
        y,
        88,
        56,
        "Operación avanzada",
        [
            "Recibos de prima y cobranza / mora",
            "Conciliación de borderó / planilla",
            "Siniestros ligeros",
            "Endosos y cancelaciones",
        ],
    )
    pdf.card_box(
        108,
        y,
        88,
        56,
        "Crecimiento comercial",
        [
            "Embudo de ventas y bitácora 360",
            "Bandeja WhatsApp multiagente",
            "Cross-sell por ramo",
            "Export contable e integraciones",
        ],
    )
    pdf.set_y(y + 62)

    pdf.set_fill_color(*SOFT)
    pdf.rect(14, pdf.get_y(), 182, 28, style="F")
    pdf.set_xy(18, pdf.get_y() + 6)
    pdf.set_font(FONT, "B", 12)
    pdf.set_text_color(*BLUE)
    pdf.multi_cell(
        174,
        6.5,
        '"La tecnología debe trabajar para las personas, no las personas para la tecnología."',
    )

    pdf.ln(8)
    pdf.set_font(FONT, "B", 16)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 9, "Solicita una demo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "", 11)
    pdf.set_text_color(*MUTED)
    pdf.cell(
        0,
        6,
        "Todo tu negocio de seguros, en un solo lugar.  |  Desarrollado por SmartApps",
        align="C",
    )

    # ---- PAGE 5 ----
    pdf.add_page()
    if (ASSETS / "smartapps-seguros-logo.png").exists():
        pdf.image(str(ASSETS / "smartapps-seguros-logo.png"), 75, 45, 60)
    pdf.set_y(115)
    pdf.set_font(FONT, "B", 28)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 14, "SmartApps Seguros", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(FONT, "B", 16)
    pdf.set_text_color(*VIOLET)
    pdf.multi_cell(0, 8, '"Todo tu negocio de seguros, en un solo lugar."', align="C")
    pdf.ln(2)
    pdf.set_font(FONT, "B", 13)
    pdf.set_text_color(*BLUE)
    pdf.multi_cell(0, 7, "Creando alianzas que impulsan tu negocio de seguros.", align="C")
    pdf.ln(4)
    pdf.set_font(FONT, "", 12)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        6.5,
        "Cotiza por WhatsApp o web. Administra cartera y comisiones.\n"
        "Atiende a tus clientes con portal y alertas. Decide con el panel CEO.",
        align="C",
    )
    pdf.ln(12)
    pdf.set_fill_color(*BLUE)
    y = pdf.get_y()
    pdf.rect(55, y, 100, 14, style="F")
    pdf.set_text_color(*WHITE)
    pdf.set_font(FONT, "B", 13)
    pdf.cell(0, 14, "Solicita una demo", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(14)
    pdf.set_font(FONT, "", 11)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "Desarrollado por SmartApps", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(
        0,
        6,
        "ERP SaaS para la administración integral de empresas de seguros",
        align="C",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
