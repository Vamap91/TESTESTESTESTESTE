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
    .vehicle-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 1rem 0;
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

# Função de busca simples
def search_vehicles(query, df):
    if not query:
        return []
    
    query = query.upper().strip()
    results = []
    
    # Busca por FIPE ID
    if query.isdigit():
        matches = df[df['FipeID'].astype(str) == query]
        if not matches.empty:
            return matches.to_dict('records')
    
    # Busca por texto
    for _, row in df.iterrows():
        score = 0
        
        # Busca na marca
        if query in str(row['BrandName']).upper():
            score += 50
        
        # Busca no modelo
        if query in str(row['VehicleName']).upper():
            score += 40
        
        # Busca na abreviação
        if query in str(row['Abreviacao']).upper():
            score += 30
        
        if score > 0:
            result = row.to_dict()
            result['search_score'] = score
            results.append(result)
    
    return sorted(results, key=lambda x: x.get('search_score', 0), reverse=True)[:5]

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
    
    st.info("ℹ️ Usando dados de demonstração")

# Interface de busca
st.subheader("🔍 Buscar Veículo")

col1, col2 = st.columns([4, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="Digite código FIPE, marca ou modelo (ex: BMW, 92983, Polo)",
        help="Busque por código FIPE, marca ou modelo do veículo"
    )

with col2:
    search_button = st.button("🔍 Buscar", type="primary")

# Processar busca
if search_button and search_query:
    with st.spinner("🔄 Buscando..."):
        results = search_vehicles(search_query, df)
    
    if results:
        st.success(f"✅ Encontrados {len(results)} veículo(s)")
        
        for i, vehicle in enumerate(results):
            st.markdown(f"""
            <div class="vehicle-card">
                <h3>🚗 {vehicle['BrandName']} {vehicle['VehicleName']}</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div><strong>Ano:</strong> {vehicle['VehicleModelYear']}</div>
                    <div><strong>FIPE:</strong> {vehicle['FipeID']}</div>
                    <div><strong>ADAS:</strong> {'✅ Sim' if vehicle['ADAS'] == 'Sim' else '❌ Não'}</div>
                    <div><strong>Calibração:</strong> {vehicle['TipoRegulagem']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.error(f"❌ Nenhum veículo encontrado para: '{search_query}'")
        st.info("💡 Dicas: Tente 'BMW', 'Polo', ou '92983'")

# Mostrar base de dados
st.markdown("---")
st.subheader("📊 Base de Dados Completa")
st.dataframe(df, use_container_width=True)

# Teste
st.markdown("---")
st.subheader("🔍 Teste do Passo 3")
if st.button("Teste Busca"):
    st.success("✅ Sistema de busca funcionando!")
    st.balloons()

st.write(f"**Versão do Streamlit:** {st.__version__}")
