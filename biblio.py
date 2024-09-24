import streamlit as st
import requests
import json

# Cargar las claves de API desde los secrets de Streamlit
together_api_key = st.secrets["together_api_key"]
serper_api_key = st.secrets["serper_api_key"]

# Función para hacer la solicitud a la API de Together
def fetch_bibliography_together(query):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return "Error al obtener respuesta de la API de Together"

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
        return result['organic'][0]['snippet']
    else:
        return "Error al obtener respuesta de la API de Serper"

# Título de la aplicación
st.title("Búsqueda de Bibliografía")

# Entrada del usuario
user_query = st.text_input("Introduce el tema que deseas buscar:")

# Botón para iniciar la búsqueda
if st.button("Buscar"):
    if user_query:
        # Buscar bibliografía con Together
        st.subheader("Resultados de Together:")
        together_result = fetch_bibliography_together(user_query)
        st.write(together_result)

        # Buscar bibliografía con Serper
        st.subheader("Resultados de Serper:")
        serper_result = fetch_bibliography_serper(user_query)
        st.write(serper_result)
    else:
        st.warning("Por favor, introduce un tema para buscar.")
