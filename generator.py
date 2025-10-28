import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import date

def genereer_pdf(aankoop, kosten, huur, inflatie, looptijd, restwaarde, discontovoet,
                 lening, rente_lening, duur_lening):
    bestand = "Vastgoed_DCF_Balanz.pdf"
    doc = SimpleDocTemplate(bestand, pagesize=A4)
    styles = getSampleStyleSheet()
    normaal = styles["Normal"]
    titel = ParagraphStyle('Titel', parent=styles['Title'], textColor=colors.HexColor("#2E4053"))

    # --- Berekeningen ---
    i = inflatie / 100
    r = discontovoet / 100
    rl = rente_lening / 100

    totale_investering = aankoop + kosten
    eigen_inbreng = totale_investering - lening

    # jaarlijkse annuïteit lening
    if lening > 0 and duur_lening > 0:
        annuiteit = lening * (rl * (1 + rl)**duur_lening) / ((1 + rl)**duur_lening - 1)
    else:
        annuiteit = 0

    restschuld = lening
    jaren = np.arange(1, looptijd + 1)
    huur_per_jaar, netto_cf, pv_cf = [], [], []

    for t in jaren:
        huur_t = huur * (1 + i)**(t - 1)
        if t <= duur_lening:
            rente_t = restschuld * rl
            kapitaal_t = annuiteit - rente_t
            restschuld -= kapitaal_t
            aflossing_totaal = annuiteit
        else:
            aflossing_totaal = 0
        cf = huur_t - aflossing_totaal
        pv = cf / ((1 + r)**t)
        huur_per_jaar.append(huur_t)
        netto_cf.append(cf)
        pv_cf.append(pv)

    pv_rest = restwaarde / ((1 + r)**looptijd)
    dcf = sum(pv_cf) + pv_rest - eigen_inbreng
    roi = (dcf / eigen_inbreng) * 100 if eigen_inbreng > 0 else 0

    # --- PDF-opbouw ---
    elementen = []
    elementen.append(Paragraph("🏢 Vastgoedwaardering via DCF-model", titel))
    elementen.append(Spacer(1, 12))
    elementen.append(Paragraph(f"Datum: {date.today().strftime('%d/%m/%Y')}", normaal))
    elementen.append(Spacer(1, 24))

    data = [
        ["Parameter", "Waarde"],
        ["Aankoopprijs", f"€ {aankoop:,.0f}"],
        ["Bijkomende kosten", f"€ {kosten:,.0f}"],
        ["Totale investering", f"€ {totale_investering:,.0f}"],
        ["Lening", f"€ {lening:,.0f}"],
        ["Eigen inbreng", f"€ {eigen_inbreng:,.0f}"],
        ["Discontovoet", f"{discontovoet:.1f}%"],
        ["Rente lening", f"{rente_lening:.1f}%"],
        ["Inflatie", f"{inflatie:.1f}%"],
        ["Looptijd analyse", f"{looptijd} jaren"],
    ]
    tabel = Table(data, colWidths=[8*cm, 6*cm])
    tabel.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4053")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    elementen.append(tabel)
    elementen.append(Spacer(1, 18))
    elementen.append(Paragraph(f"<b>Netto contante waarde:</b> € {dcf:,.0f}", normaal))
    elementen.append(Paragraph(f"<b>Gemiddeld rendement:</b> {roi:.2f}%", normaal))
    elementen.append(Spacer(1, 18))

    # --- Grafiek kasstromen ---
    plt.figure(figsize=(5,3))
    plt.bar(jaren, huur_per_jaar, color="#AED6F1", label="Bruto huur")
    plt.bar(jaren, netto_cf, color="#2E86C1", label="Netto kasstroom")
    plt.xlabel("Jaar")
    plt.ylabel("€")
    plt.title("Jaarlijkse kasstromen")
    plt.legend()
    plt.tight_layout()
    plt.savefig("kasstromen.png", dpi=120)
    plt.close()

    elementen.append(Image("kasstromen.png", width=14*cm, height=7*cm))
    elementen.append(Spacer(1, 18))

    uitleg = """
    <b>Over dit model</b><br/><br/>
    Deze berekening gebruikt de <i>Discounted Cash Flow-methode (DCF)</i> om te bepalen wat de toekomstige huurinkomsten
    en de restwaarde van het gebouw vandaag waard zijn.  
    Wanneer er een lening wordt aangegaan, worden de jaarlijkse aflossingen in mindering gebracht
    om de netto-kasstroom te berekenen.  
    Zo zie je hoe financiering, inflatie en rendement samen de waarde van het vastgoed beïnvloeden.
    """
    elementen.append(Paragraph(uitleg, normaal))
    doc.build(elementen)

    resultaten = {"dcf": dcf, "roi": roi}
    return bestand, resultaten
