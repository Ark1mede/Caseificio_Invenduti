import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titolo dell'applicazione
st.title("Analisi del Guadagno Netto")

# Slider per variabili (modificato da 1kg a 0.5kg)
quantita_venduta = st.slider("Quantità venduta (kg)", 0.0, 10.0, 5.0, 0.25)  # Da 0.0 a 10.0 kg, passo di 0.25 kg
prezzo_vendita = st.slider("Prezzo di vendita (€/kg)", 10.0, 20.0, 13.0, 0.5)
percentuale_invenduto = st.slider("Percentuale invenduto (%)", 0, 100, 10)
costi_fissi = st.slider("Costi fissi (€)", 0, 1000, 100)

# Calcoli
quantita_invenduta = quantita_venduta * (percentuale_invenduto / 100)
guadagno_netto = (quantita_venduta - quantita_invenduta) * prezzo_vendita - costi_fissi

# Visualizza il guadagno netto
st.write(f"**Guadagno netto: {guadagno_netto:.2f} €**")

# Grafico Guadagno netto
x = np.linspace(0, 100, 100)
y = (quantita_venduta - (x / 100) * quantita_venduta) * prezzo_vendita - costi_fissi

plt.plot(x, y)
plt.title("Guadagno Netto in Funzione dell'Invenduto")
plt.xlabel("Percentuale invenduto (%)")
plt.ylabel("Guadagno netto (€)")
st.pyplot(plt)

# Bottone per calcolare il BEP (Break Even Point)
if st.button("BEP"):
    # Calcola il guadagno netto = 0
    percentuale_bep = (costi_fissi / (prezzo_vendita * quantita_venduta)) * 100
    st.write(f"Percentuale invenduto per BEP: {percentuale_bep:.2f}%")
