import streamlit as st
import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def generate_image(prompt):
    try:

        model = genai.ImageGenerationModel("imagen-3") 
        result = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            safety_filter_level="block_some",
            aspect_ratio="1:1"
        )

        image = result.images[0]
        return image
    except Exception as e:
        return f"Ошибка доступа к Nano Banana: {e}"

def generate_image_ui():
    st.subheader("🎨 Nano Banana Image Gen")
    img_prompt = st.text_input("Опиши иллюстрацию для урока:")
    if st.button("Сгенерировать"):
        with st.spinner("Рисую..."):
            res = generate_image(img_prompt)
            if isinstance(res, str):
                st.error(res)
            else:
                st.image(res._pil_image, caption=img_prompt)
