import streamlit as st
import streamlit.components.v1 as components
import requests
import os


GOOGLE_API_KEY = os.getenv("api_maps")

st.title("🧪 Test géolocalisation navigateur")

components.html("""
<script>
(async () => {
  try {
    const output = document.createElement('pre');
    output.style.color = 'green';
    output.style.fontSize = '16px';
    document.body.appendChild(output);

    output.textContent += "📍 Initialisation script JS...\\n";

    if (!navigator.geolocation) {
      output.textContent += "❌ Géolocalisation non supportée par ce navigateur.\\n";
      return;
    }

    output.textContent += "🟢 navigator.geolocation disponible\\n";

    navigator.geolocation.getCurrentPosition(
      function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        output.textContent += `✅ Coordonnées obtenues :\\nLatitude: ${latitude}\\nLongitude: ${longitude}\\n`;
        const newUrl = `${window.location.pathname}?latitude=${latitude}&longitude=${longitude}`;
        output.textContent += `🔁 Redirection vers : ${newUrl}\\n`;
        setTimeout(() => window.location.replace(newUrl), 1000);
      },
      function(error) {
        output.style.color = 'red';
        output.textContent += "❌ Erreur lors de la récupération de la position :\\n";
        output.textContent += error.message + "\\n";
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  } catch (err) {
    const output = document.createElement('pre');
    output.style.color = 'red';
    output.textContent = "🔥 Exception dans le script JS :\\n" + err.message;
    document.body.appendChild(output);
  }
})();
</script>
""", height=400)

# Lecture éventuelle dans l'URL
latitude = st.query_params.get("latitude")
longitude = st.query_params.get("longitude")

if latitude and longitude:
    st.success(f"Position obtenue : {latitude}, {longitude}")
else:
    st.info("⏳ Attente de la géolocalisation...")
