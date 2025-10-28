import streamlit as st
from generator import genereer_pdf

st.set_page_config(page_title="Vastgoed DCF | Balan’z", page_icon="🏢")

st.title("🏢 DCF-waardering vastgoed – met lening")

st.markdown("""
Voer hieronder de parameters in om de **contante waarde (DCF)** en het **verwachte rendement**
van een vastgoedproject te berekenen.
""")

# --- Basisgegevens ---
st.header("🔹 Basisgegevens")
aankoop = st.number_input("Aankoopprijs (€)", value=500000.0, step=10000.0)
kosten = st.number_input("Bijkomende kosten (€)", value=25000.0, step=1000.0)
huur = st.number_input("Jaarlijkse huur (jaar 1, €)", value=24000.0, step=1000.0)
inflatie = st.number_input("Inflatievoet (%)", value=2.0, step=0.1)
looptijd = st.number_input("Looptijd (jaren)", value=10, step=1)
restwaarde = st.number_input("Restwaarde na looptijd (€)", value=550000.0, step=10000.0)
discontovoet = st.number_input("Discontovoet (%)", value=6.0, step=0.1)
waardegroei = st.number_input("Waardegroei vastgoed (%)", value=2.0, step=0.1)


# --- Financiering ---
st.header("💰 Financiering")
lening = st.number_input("Leningbedrag (€)", value=300000.0, step=10000.0)
rente_lening = st.number_input("Rentevoet lening (%)", value=3.0, step=0.1)
duur_lening = st.number_input("Looptijd lening (jaren)", value=15, step=1)

if st.button("Bereken en genereer rapport"):
    pdf_pad, resultaten = genereer_pdf(
        aankoop, kosten, huur, inflatie, looptijd, restwaarde,
        discontovoet, lening, rente_lening, duur_lening, waardegroei
    )

    st.success(f"📊 Netto contante waarde (DCF): **€ {resultaten['dcf']:,.2f}**")
    st.write(f"Gemiddeld jaarlijks rendement: **{resultaten['roi']:.2f}%**")

    with open(pdf_pad, "rb") as pdf:
        st.download_button("📄 Download PDF-rapport", pdf, file_name="Vastgoed_DCF_Balanz.pdf")
