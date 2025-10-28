import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import date

def genereer_pdf(aankoop, kosten, huur, inflatie, looptijd, restwaarde, discontovoet,
                 lening, rente_lening, duur_lening):

    bestand = "Vastgoed_DCF_Balanz.pdf"
    doc = SimpleDocTemplate(bestand, pagesize=landscape(A4), leftMargin=1.5*cm, rightMargin=1.5*cm)
    styles = getSampleStyleSheet()
    normaal = styles["Normal"]
    titel = ParagraphStyle('Titel', parent=styles['Title'], textColor=colors.HexColor("#2E4053"))

    # --- Parameters ---
    totale_investering = aankoop + kosten
    eigen_inbreng = totale_investering - lening

    inflatie_m = (1 + inflatie/100)**(1/12) - 1
    discontovoet_m = (1 + discontovoet/100)**(1/12) - 1
    rente_m = (1 + rente_lening/100)**(1/12) - 1

    maanden = int(looptijd * 12)
    duur_lening_m = int(duur_lening * 12)

    # --- Leningberekening ---
    if lening > 0 and duur_lening_m > 0:
        maandlast = lening * (rente_m * (1 + rente_m)**duur_lening_m) / ((1 + rente_m)**duur_lening_m - 1)
    else:
        maandlast = 0

    restschuld = lening
    maanden_lijst = np.arange(1, maanden + 1)
    huur_maand, netto_cf, pv_cf, restschuld_lijst = [], [], [], []

    huur_m0 = huur / 12  # maandelijkse huur start

    for t in maanden_lijst:
        huur_t = huur_m0 * (1 + inflatie_m)**(t - 1)
        if t <= duur_lening_m:
            rente_t = restschuld * rente_m
            kapitaal_t = maandlast - rente_t
            restschuld -= kapitaal_t
            leninglast_t = maandlast
        else:
            leninglast_t = 0

        cf = huur_t - leninglast_t
        pv = cf / ((1 + discontovoet_m)**t)
        huur_maand.append(huur_t)
        netto_cf.append(cf)
        pv_cf.append(pv)
        restschuld_lijst.append(restschuld)

    pv_rest = restwaarde / ((1 + discontovoet_m)**maanden)
    dcf = sum(pv_cf) + pv_rest - eigen_inbreng
    roi = (dcf / eigen_inbreng) * 100 if eigen_inbreng > 0 else 0

    # --- PDF-opbouw ---
    elementen = []
    elementen.append(Paragraph("🏢 Vastgoedwaardering via DCF-model (maandelijks)", titel))
    elementen.append(Spacer(1, 10))
    elementen.append(Paragraph(f"Datum: {date.today().strftime('%d/%m/%Y')}", normaal))
    elementen.append(Spacer(1, 20))

    data = [
        ["Parameter", "Waarde"],
        ["Aankoopprijs", f"€ {aankoop:,.0f}"],
        ["Bijkomende kosten", f"€ {kosten:,.0f}"],
        ["Totale investering", f"€ {totale_investering:,.0f}"],
        ["Lening", f"€ {lening:,.0f}"],
        ["Eigen inbreng", f"€ {eigen_inbreng:,.0f}"],
        ["Discontovoet (jaarlijks)", f"{discontovoet:.1f}%"],
        ["Rente lening (jaarlijks)", f"{rente_lening:.1f}%"],
        ["Inflatie", f"{inflatie:.1f}%"],
        ["Looptijd analyse", f"{looptijd} jaar"],
    ]
    tabel = Table(data, colWidths=[8*cm, 8*cm])
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

    # --- Grafiek ---
    plt.figure(figsize=(7,3))
    plt.plot(maanden_lijst, netto_cf, color="#2E86C1", label="Netto kasstroom per maand")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.xlabel("Maand")
    plt.ylabel("Kasstroom (€)")
    plt.title("Kasstromen per maand")
    plt.legend()
    plt.tight_layout()
    plt.savefig("kasstromen_maandelijks.png", dpi=120)
    plt.close()

    elementen.append(Image("kasstromen_maandelijks.png", width=18*cm, height=8*cm))
    elementen.append(Spacer(1, 20))

    # --- Samenvattende tabel (elke 12 maanden) ---
    jaar_data = [["Jaar", "Gemiddelde huur/maand", "Netto CF/maand", "PV maand"]]
    for j in range(1, looptijd + 1):
        start, eind = (j-1)*12, j*12
        jaar_data.append([
            j,
            f"€ {np.mean(huur_maand[start:eind]):,.0f}",
            f"€ {np.mean(netto_cf[start:eind]):,.0f}",
            f"€ {np.mean(pv_cf[start:eind]):,.0f}",
        ])

    jaar_tabel = Table(jaar_data, colWidths=[3*cm, 5*cm, 5*cm, 5*cm])
    jaar_tabel.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4053")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey)
    ]))
    elementen.append(Paragraph("📅 Samenvatting per jaar (gemiddelden per maand)", normaal))
    elementen.append(jaar_tabel)
    elementen.append(Spacer(1, 18))

    uitleg = """
    <b>Over dit model</b><br/><br/>
    Deze berekening werkt op maandbasis en gebruikt de <i>Discounted Cash Flow (DCF)</i>-methode
    om te bepalen wat de toekomstige huurinkomsten en restwaarde vandaag waard zijn.  
    De grafiek toont hoe de maandelijkse kasstroom evolueert, rekening houdend met inflatie, aflossingen en rente.
    """
    elementen.append(Paragraph(uitleg, normaal))
    doc.build(elementen)

    resultaten = {"dcf": dcf, "roi": roi}
    return bestand, resultaten
