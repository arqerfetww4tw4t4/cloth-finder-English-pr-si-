# app.py
# EINFACHE STREAMLIT-APP FÜR EIN SCHULPROJEKT
# Idee: Bild hochladen (zur Identifikation) + Produktname eingeben
# Dann Online-Preise vergleichen und günstigstes Angebot anzeigen

import streamlit as st
import requests

# -------------------- KONFIG --------------------
SERPAPI_KEY = "d0830ba352bf8acfc0015f156b901df5666478acddc71b4865e10e127290900a"
# ------------------------------------------------

st.set_page_config(page_title="Klamotten Preisfinder", page_icon="🛒")

st.title("🛒 Klamotten Preisfinder")
st.write("Lade ein Bild hoch und gib den Namen des Kleidungsstücks ein. Die App sucht online nach dem günstigsten Preis.")

# Bild Upload
uploaded_file = st.file_uploader("Bild vom Kleidungsstück hochladen", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Hochgeladenes Bild", use_container_width=True)

# Produkteingabe
product_name = st.text_input("Name des Kleidungsstücks (z.B. 'Nike Hoodie schwarz')")

# Suche starten
if st.button("Günstigsten Preis suchen"):
    if not product_name:
        st.error("Bitte gib einen Produktnamen ein.")
    else:
        with st.spinner("Suche nach Preisen im Internet..."):
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google_shopping",
                "q": product_name,
                "api_key": SERPAPI_KEY,
                "hl": "de",
                "gl": "de"
            }

            response = requests.get(url, params=params)
            data = response.json()

            if "shopping_results" not in data:
                st.error("Keine Ergebnisse gefunden.")
            else:
                cheapest = None

                for item in data["shopping_results"]:
                    if "price" in item:
                        price_str = item["price"].replace("€", "").replace(",", ".")
                        try:
                            price = float(price_str)
                            if cheapest is None or price < cheapest["price"]:
                                cheapest = {
                                    "price": price,
                                    "title": item.get("title", "Unbekannt"),
                                    "link": item.get("link", "")
                                }
                        except:
                            pass

                if cheapest:
                    st.success("Günstigstes Angebot gefunden!")
                    st.write(f"**Produkt:** {cheapest['title']}")
                    st.write(f"**Preis:** {cheapest['price']} €")
                    
                    # Google Link richtig einrücken und funktionierend
                    search_name = cheapest['title'].replace(' ', '+')
                    google_link = f"https://www.google.com/search?q={search_name}+Nike+billig"
                    st.markdown(f"[Zum Shop]({google_link})", unsafe_allow_html=True)
                else:
                    st.error("Preise konnten nicht gelesen werden.")
