import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sistema ADAS Pro",
    page_icon="🔧",
    layout="wide"
)

# CSS básico
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔧 Sistema Inteligente de Calibração ADAS</h1>
    <p>Plataforma profissional para calibração de sistemas ADAS</p>
</div>
""", unsafe_allow_html=True)

# Teste de funcionamento
st.subheader("🔍 Teste de Funcionamento")
st.write("Se você vê isso, a estrutura básica está funcionando!")

if st.button("Teste Estrutura"):
    st.success("✅ Estrutura funcionando!")

st.write(f"**Versão do Streamlit:** {st.__version__}")
