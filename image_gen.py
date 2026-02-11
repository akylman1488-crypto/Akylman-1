import streamlit as st
import requests
import io
from PIL import Image

HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query_hf(payload):
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except:
        return None

def generate_image_ui():
    st.markdown("---")
    st.subheader("🎨 Nano Banana (Stable Mode)")
    
    prompt = st.text_input("Опиши картинку:", placeholder="Например: Атом золота под микроскопом")
    
    if st.button("Сгенерировать"):
        if not prompt:
            st.warning("Введите описание!")
            return

        with st.spinner("Нейросеть рисует..."):
            image_bytes = query_hf({"inputs": prompt})
            
            if image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=prompt, use_container_width=True)
                except Exception as e:
                    st.error(f"Ошибка обработки: {e}")
            else:
                st.error("Сервер HF временно недоступен или токен заблокирован GitHub.")
                st.info("Нажми 'Allow Secret' на GitHub или обнови токен в коде.")
