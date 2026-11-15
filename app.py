import streamlit as st

st.set_page_config(page_title="Spider Hot", page_icon="🕷️")

st.title("🕷️ Spider Hot")
st.subheader("Central de tendências do TikTok")

st.info("Sua aranha inteligente está sendo preparada!")

nicho = st.text_input("Qual nicho você quer pesquisar?", "Hot 18+")

if st.button("Pesquisar tendências"):
    st.success(f"Pesquisa preparada para: {nicho}")
