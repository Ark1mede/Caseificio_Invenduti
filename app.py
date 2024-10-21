import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Imposta due colonne per la disposizione degli slider
col1, col2 = st.columns(2)

# Slider nelle due colonne
with col1:
    costo_mozzarella = st.slider("Costo di produzione (€/0.5kg)", 5, 15, 8)  # Costo per 0.5 kg
    costo_consegna = st.slider("Costo di consegna (€)", 0, 10, 5)
with col2:
    prezzo_vendita = st.slider("Prezzo di vendita (€/0.5kg)", 10, 20, 13)  # Prezzo per 0.5 kg
    quantita_venduta = st.slider("Quantità venduta per consegna (0.5kg)", 1, 20, 6)  # Quantità in 0.5 kg

numero_consegne = st.slider("Numero di consegne", 1, 20, 10)
percentuale_invenduto = st.slider("Percentuale di invenduto (%)", 0, 100, 10)

# Calcola i costi e i guadagni
costo_totale_mozzarella = costo_mozzarella * quantita_venduta * numero_consegne  # Costo totale per 0.5 kg
prezzo_totale_vendite = prezzo_vendita * quantita_venduta * numero_consegne  # Prezzo totale per 0.5 kg
costo_totale_consegna = costo_consegna * numero_consegne
guadagno_netto = prezzo_totale_vendite - costo_totale_mozzarella - costo_totale_consegna
costo_invenduto = costo_mozzarella * quantita_venduta * (percentuale_invenduto / 100) * numero_consegne  # Costo invenduto
guadagno_netto_dopo_invenduto = guadagno_netto - costo_invenduto

# Visualizza il guadagno netto con il testo centrato e in grassetto, font 32
st.markdown(f"<h1 style='text-align: center; font-weight: bold; font-size:32px;'>Guadagno netto: {guadagno_netto_dopo_invenduto:.2f} €</h1>", unsafe_allow_html=True)

# Aggiungi il pulsante BEP (Break-Even Point)
if st.button("Calcola BEP"):
    if guadagno_netto != 0:
        # Calcola la percentuale di invenduto che rende il guadagno netto pari a zero
        bep_percentuale_invenduto = (guadagno_netto / (costo_mozzarella * quantita_venduta * numero_consegne)) * 100  # Percentuale invenduto per pareggio
        bep_percentuale_invenduto = max(0, min(bep_percentuale_invenduto, 100))  # Assicurati che sia tra 0 e 100
        st.markdown(f"<h2 style='text-align: center;'>Il BEP è raggiunto con il {bep_percentuale_invenduto:.2f}% di invenduto</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center;'>Il guadagno netto è già a zero</h2>", unsafe_allow_html=True)

# Calcola i guadagni per diversi valori di quantità venduta
quantita_range = np.arange(1, 41, 1)  # Modificato per riflettere la nuova gamma
guadagni_dopo_invenduto = []

for q in quantita_range:
    costo_totale_mozzarella = costo_mozzarella * q * numero_consegne  # Costo totale per 0.5 kg
    prezzo_totale_vendite = prezzo_vendita * q * numero_consegne  # Prezzo totale per 0.5 kg
    guadagno_netto = prezzo_totale_vendite - costo_totale_mozzarella - costo_totale_consegna
    costo_invenduto = costo_mozzarella * q * (percentuale_invenduto / 100) * numero_consegne  # Costo invenduto
    guadagni_dopo_invenduto.append(guadagno_netto - costo_invenduto)

# Estendere i valori negativi
guadagni_dopo_invenduto += [-10 * i for i in range(1, 11)]  # Aggiungi 10 valori negativi

# Crea il grafico
plt.figure(figsize=(10, 5))
plt.plot(quantita_range, guadagni_dopo_invenduto[:40], marker='o')  # Usa solo i primi 40 valori
plt.title("Guadagno netto dopo invenduto in base alla quantità venduta")
plt.xlabel("Quantità venduta (0.5kg)")
plt.ylabel("Guadagno netto dopo invenduto (euro)")
plt.grid()
plt.axhline(0, color='red', linestyle='--')  # Linea del punto di pareggio
st.pyplot(plt)  # Mostra il grafico in Streamlit
