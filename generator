from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import date

def genereer_pdf(waarde, discontovoet, looptijd, dcf):
    """Genereert een eenvoudig PDF-rapport met DCF-berekening."""

    bestand = "DCF_Rapport_Balanz.pdf"
    doc = SimpleDocTemplate(bestand, pagesize=A4)
    styles = getSampleStyleSheet()
    elementen = []

    titel_style = ParagraphStyle('Titel', parent=styles['Title'], textColor=colors.HexColor("#2E4053"))
    normaal = styles["Normal"]

    # Titel
    elementen.append(Paragraph("💶 Waarderingsrapport – Eenvoudig DCF-model", titel_style))
    elementen.append(Spacer(1, 12))
    elementen.append(Paragraph(f"Datum: {date.today().strftime('%d/%m/%Y')}", normaal))
    elementen.append(Spacer(1, 24))

    # Parameters
    data = [
        ["Parameter", "Waarde"],
        ["Jaarlijkse kasstroom (€)", f"{waarde:,.2f}"],
        ["Discontovoet (%)", f"{discontovoet:.2f}%"],
        ["Looptijd (jaren)", str(looptijd)],
    ]
    tabel = Table(data, hAlign="LEFT", colWidths=[8*cm, 6*cm])
    tabel.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4053")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elementen.append(Paragraph("### Ingevoerde parameters", normaal))
    elementen.append(tabel)
    elementen.append(Spacer(1, 24))

    # Resultaat
    elementen.append(Paragraph(f"De berekende **contante waarde (DCF)** bedraagt <b>€ {dcf:,.2f}</b>.", normaal))
    elementen.append(Spacer(1, 24))

    elementen.append(Paragraph(
        "Deze berekening is een vereenvoudigde waarderingsbenadering op basis van constante kasstromen en een vaste discontovoet.",
        normaal
    ))

    doc.build(elementen)
    return bestand
