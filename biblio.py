import streamlit as st
import requests

# Cargar la clave de API desde los secrets de Streamlit
serply_api_key = st.secrets["serply_api_key"]

# Función para hacer la solicitud a la API de Serply
def fetch_bibliography_serply(query):
    url = f"https://api.serply.io/v1/scholar/{query.replace(' ', '+')}"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": serply_api_key
    }
     
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        # Extraer los primeros resultados si están disponibles
        if 'results' in result:
            return result['results'][:5]  # Limitar a los primeros 5 resultados
        else:
            return "No se encontraron resultados."
    else:
        return f"Error {response.status_code}: No se pudo conectar a la API de Serply."

# Título de la aplicación
st.title("Búsqueda de Bibliografía Académica")

# Entrada del usuario
user_query = st.text_input("Introduce el tema que deseas buscar:")

# Botón para iniciar la búsqueda
if st.button("Buscar"):
    if user_query:
        st.subheader("Resultados de Serply:")
        serply_results = fetch_bibliography_serply(user_query)
        
        if isinstance(serply_results, list):
            for idx, result in enumerate(serply_results):
                st.write(f"**{idx+1}. {result['title']}**")
                st.write(f"Enlace: {result['link']}")
                st.write(f"Resumen: {result['snippet']}")
                st.write("------")
        else:
            st.write(serply_results)
    else:
        st.warning("Por favor, introduce un tema para buscar.")
