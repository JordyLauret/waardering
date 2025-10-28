import streamlit as st
from generator import genereer_pdf

st.set_page_config(page_title="Eenvoudig DCF-model | Balan’z", page_icon="💶")

st.title("💶 Eenvoudig DCF-model – Balan’z demo")

st.markdown("""
Voer hieronder de parameters in en klik op **Genereer rapport** om een PDF te maken met de berekende contante waarde (DCF).
""")

# Invoerparameters
waarde = st.number_input("💰 Jaarlijkse kasstroom (€)", min_value=0.0, value=100000.0, step=1000.0)
discontovoet = st.number_input("📉 Discontovoet (%)", min_value=0.1, value=8.0, step=0.1)
looptijd = st.number_input("⏳ Looptijd (jaren)", min_value=1, value=5, step=1)

if st.button("Genereer rapport"):
    # Berekening DCF
    r = discontovoet / 100
    dcf = waarde * (1 - (1 + r) ** (-looptijd)) / r

    st.success(f"De contante waarde van de kasstromen bedraagt **€ {dcf:,.2f}**")

    # PDF genereren
    pdf_path = genereer_pdf(waarde, discontovoet, looptijd, dcf)
    with open(pdf_path, "rb") as pdf:
        st.download_button("📄 Download PDF-rapport", pdf, file_name="DCF_Rapport_Balanz.pdf")
