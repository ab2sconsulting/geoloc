import streamlit as st
import streamlit.components.v1 as components
import requests

GOOGLE_API_KEY = os.getenv("api_maps")

# ====== TITRE ======
st.title("📍 Localisation instantanée")

# ====== JAVASCRIPT POUR RÉCUPÉRER LA GÉOLOCALISATION ======
components.html(
    """
    <script>
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const params = new URLSearchParams({latitude, longitude});
            window.location.href = window.location.pathname + "?" + params.toString();
        },
        function(error) {
            document.body.innerHTML = "<p style='color:red;'>Erreur de géolocalisation : " + error.message + "</p>";
        });
    </script>
    """,
    height=0
)

# ====== EXTRAIRE COORDONNÉES GPS DE L'URL ======
query_params = st.query_params
latitude = query_params.get("latitude", None)
longitude = query_params.get("longitude", None)

# ====== AFFICHER L'ADRESSE SI COORDONNÉES DISPONIBLES ======
if latitude and longitude:
    st.success("📌 Coordonnées détectées !")

    # Appel à l'API Google Maps pour reverse geocoding
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            address = data['results'][0]['formatted_address']
            st.markdown(f"### ✅ Vous êtes au :\n**{address}**")
        else:
            st.error("❌ Adresse introuvable avec ces coordonnées.")
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API Google Maps : {e}")
else:
    st.info("📲 En attente d'autorisation de localisation…\nMerci d'autoriser la géolocalisation dans votre navigateur.")
