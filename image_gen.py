import streamlit as st
import requests
import io
from PIL import Image

HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer hf_your_token_here"}

def query_hf(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return None
    return response.content

def generate_image_ui():
    st.markdown("---")
    st.subheader("🎨 Nano Banana (Stable Mode)")
    
    prompt = st.text_input("Опиши картинку:", placeholder="Например: Скелет человека в полный рост")
    
    if st.button("Сгенерировать"):
        if not prompt:
            st.warning("Введите текст!")
            return

        with st.spinner("Нейросеть рисует..."):
            image_bytes = query_hf({"inputs": prompt})
            
            if image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=prompt)
                except:
                    st.error("Ошибка обработки изображения.")
            else:
                st.error("Сервер перегружен или токен неверный.")
