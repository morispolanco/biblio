import streamlit as st
import requests

# Cargar la clave de API desde los secrets de Streamlit
serper_api_key = st.secrets["serper_api_key"]

# Función para hacer la solicitud a la API de Serper
def fetch_bibliography_serper(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
     
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        # Extraer los primeros resultados si están disponibles
        if 'organic' in result:
            return result['organic'][:5]  # Limitar a los primeros 15 resultados
        else:
            return "No se encontraron resultados."
    else:
        return f"Error {response.status_code}: No se pudo conectar a la API de Serper."

# Título de la aplicación
st.title("Búsqueda de Bibliografía Académica")

# Entrada del usuario
user_query = st.text_input("Introduce el tema que deseas buscar:")

# Botón para iniciar la búsqueda
if st.button("Buscar"):
    if user_query:
        st.subheader("Resultados de Serper:")
        serper_results = fetch_bibliography_serper(user_query)
        
        if isinstance(serper_results, list):
            for idx, result in enumerate(serper_results):
                st.write(f"**{idx+1}. {result['title']}**")
                st.write(f"Enlace: {result['link']}")
                st.write(f"Resumen: {result['snippet']}")
                st.write("------")
        else:
            st.write(serper_results)
    else:
        st.warning("Por favor, introduce un tema para buscar.")
