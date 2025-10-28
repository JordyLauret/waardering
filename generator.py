from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import date
import matplotlib.pyplot as plt
import numpy as np

def genereer_pdf(waarde, discontovoet, looptijd, dcf):
    """Genereert een eenvoudig PDF-rapport met DCF-berekening, uitleg en grafiek."""

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
    elementen.append(Spacer(1, 18))

    # --- Grafiek genereren ---
    jaren = np.arange(1, looptijd + 1)
    r = discontovoet / 100
    contante_waarden = [waarde / ((1 + r) ** j) for j in jaren]

    plt.figure(figsize=(5,3))
    plt.bar(jaren, [waarde]*looptijd, color="#AED6F1", label="Kasstroom per jaar (€)")
    plt.bar(jaren, contante_waarden, color="#2E86C1", label="Contante waarde (€)")
    plt.xlabel("Jaar")
    plt.ylabel("Waarde (€)")
    plt.title("Visualisatie van de DCF-berekening")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafiek_dcf.png", dpi=120)
    plt.close()

    elementen.append(Paragraph("### Visualisatie van kasstromen", normaal))
    elementen.append(Image("grafiek_dcf.png", width=14*cm, height=8*cm))
    elementen.append(Spacer(1, 24))

    # Uitleg over DCF
    uitleg_tekst = """
    <b>Wat is een DCF-waardering?</b><br/><br/>
    De <i>Discounted Cash Flow-methode (DCF)</i> is een veelgebruikte manier om de waarde van een onderneming te bepalen.  
    Ze vertrekt vanuit het idee dat een bedrijf vandaag zoveel waard is als de som van zijn toekomstige kasstromen –  
    maar dan herleid naar hun waarde van vandaag.<br/><br/>
    Elke euro die het bedrijf in de toekomst zal genereren, wordt verdisconteerd met een discontovoet.  
    Die discontovoet weerspiegelt het rendement dat investeerders verwachten als vergoeding voor het risico dat ze nemen.<br/><br/>
    De DCF-methode is een fundamentele waarderingstechniek omdat ze de focus legt op de <b>reële prestaties en kasstromen</b>  
    van een onderneming, in plaats van enkel op marktvergelijkingen of boekhoudkundige cijfers.<br/><br/>
    Deze berekening in dit rapport is een vereenvoudigde versie, bedoeld om inzicht te geven in de principes van waardering  
    en het effect van rendement en tijd op de bedrijfswaarde.
    """

    elementen.append(Paragraph(uitleg_tekst, normaal))
    elementen.append(Spacer(1, 24))

    doc.build(elementen)
    return bestand
