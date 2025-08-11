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

# Função para criar dados de demonstração
@st.cache_data
def create_demo_data():
    return pd.DataFrame({
        'FipeID': [92983, 95432, 87621, 73291, 84512],
        'VehicleModelYear': [2024, 2023, 2024, 2025, 2023],
        'BrandName': ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'AUDI', 'TOYOTA'],
        'VehicleName': [
            '118i M Sport 1.5 TB 12V Aut. 5p',
            'Polo TSI 1.0 200 Aut. 5p',
            'A-Class A200 1.3 TB Aut.',
            'A3 Sedan 1.4 TFSI Aut.',
            'Corolla 2.0 XEi Aut.'
        ],
        'Abreviacao': ['118i M Sport', 'Polo TSI', 'A200', 'A3 Sedan', 'Corolla XEi'],
        'ADAS': ['Sim', 'Sim', 'Sim', 'Sim', 'Sim'],
        'TipoRegulagem': ['Dinamica', 'Estatica', 'Dinamica', 'Estatica/Dinamica', 'Dinamica']
    })

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔧 Sistema Inteligente de Calibração ADAS</h1>
    <p>Plataforma profissional para calibração de sistemas ADAS</p>
</div>
""", unsafe_allow_html=True)

# Carregar dados
df = create_demo_data()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    st.markdown("---")
    
    st.subheader("📊 Estatísticas")
    total_vehicles = len(df)
    vehicles_with_adas = len(df[df['ADAS'] == 'Sim'])
    unique_brands = df['BrandName'].nunique()
    
    st.metric("Total de Veículos", total_vehicles)
    st.metric("Veículos com ADAS", vehicles_with_adas)
    st.metric("Marcas Únicas", unique_brands)
