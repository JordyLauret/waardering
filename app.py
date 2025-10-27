import streamlit as st
from pathlib import Path
from generator import generate_pdf
import tempfile

st.set_page_config(page_title="Balan'z – Waarderingsrapport", layout="centered")
st.title("Balan'z – Waarderingsrapport (MVP)")
st.write("Upload een Excel met aannames/berekeningen en genereer een PDF-rapport.")

client = st.text_input("Klantnaam", value="Sisu BV")
file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
if file is not None:
    with tempfile.TemporaryDirectory() as tmpd:
        xlsx_path = Path(tmpd) / file.name
        with open(xlsx_path, "wb") as f:
            f.write(file.read())
        pdf_path = Path(tmpd) / "Waarderingsrapport.pdf"
        try:
            generate_pdf(xlsx_path, pdf_path, client_name=client)
            st.success("Rapport gegenereerd.")
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=f"Waarderingsrapport_{client}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Kon rapport niet genereren: {e}")
