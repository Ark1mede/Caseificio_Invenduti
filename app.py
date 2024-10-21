import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Imposta due colonne per la disposizione degli slider
col1, col2 = st.columns(2)

# Slider nelle due colonne
with col1:
    costo_mozzarella = st.slider("Costo di produzione (€/0.5kg)", 5.0, 15.0, 8.0, step=0.5)
    costo_consegna = st.slider("Costo di consegna (€)", 0.0, 10.0, 2.5, step=0.5)
with col2:
    prezzo_vendita = st.slider("Prezzo di vendita (€/0.5kg)", 10.0, 20.0, 13.0, step=0.5)
    quantita_venduta = st.slider("Quantità venduta per consegna (0.5kg)", 0.5, 10.0, 1.0, step=0.5)

numero_consegne = st.slider("Numero di consegne", 1, 20, 3)

# Funzione per calcolare il guadagno netto
def calcola_guadagno_netto(percentuale_invenduto):
    costo_totale_mozzarella = costo_mozzarella * quantita_venduta * numero_consegne
    prezzo_totale_vendite = prezzo_vendita * quantita_venduta * numero_consegne
    costo_totale_consegna = costo_consegna * numero_consegne
    guadagno_netto = prezzo_totale_vendite - costo_totale_mozzarella - costo_totale_consegna
    costo_invenduto = costo_mozzarella * quantita_venduta * (percentuale_invenduto / 100) * numero_consegne
    return guadagno_netto - costo_invenduto

# Calcola il BEP
def calcola_bep():
    for percentuale in np.arange(0, 100, 0.01):
        if calcola_guadagno_netto(percentuale) <= 0:
            return percentuale
    return 100  # Se non si trova un BEP, restituisce 100%

bep = calcola_bep()

# Crea il grafico
plt.figure(figsize=(10, 6))

# Calcola i valori per il grafico
percentuali_invenduto = np.arange(1, 51, 1)
quantita_invenduta = [quantita_venduta * numero_consegne * (p / 100) for p in percentuali_invenduto]
guadagni_netti = [calcola_guadagno_netto(p) for p in percentuali_invenduto]

# Plotta la quantità degli invenduti
plt.plot(percentuali_invenduto, quantita_invenduta, label='Quantità invenduta', color='blue')

# Plotta la linea del BEP
plt.axvline(x=bep, color='red', linestyle='--', label=f'BEP ({bep:.2f}%)')

# Configura il grafico
plt.title("Quantità invenduta e Break-Even Point")
plt.xlabel("Percentuale di invenduto (%)")
plt.ylabel("Quantità invenduta (0.5kg)")
plt.ylim(0, max(quantita_invenduta) * 1.1)  # Imposta il limite dell'asse Y
plt.legend()
plt.grid(True)

# Mostra il grafico in Streamlit
st.pyplot(plt)

# Visualizza il BEP
st.markdown(f"<h2 style='text-align: center;'>Il Break-Even Point è raggiunto al {bep:.2f}% di invenduto</h2>", unsafe_allow_html=True)

# Calcola e visualizza il guadagno netto attuale
percentuale_invenduto_attuale = st.slider("Percentuale di invenduto attuale (%)", 0, 100, 10)
guadagno_netto_attuale = calcola_guadagno_netto(percentuale_invenduto_attuale)
st.markdown(f"<h2 style='text-align: center;'>Guadagno netto attuale: {guadagno_netto_attuale:.2f} €</h2>", unsafe_allow_html=True)
