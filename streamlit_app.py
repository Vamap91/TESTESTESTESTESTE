import streamlit as st
import pandas as pd
import os

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
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .data-section {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .status-positive {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados REAIS
@st.cache_data
def load_vehicle_data(uploaded_file=None):
    """Carrega dados reais do CSV"""
    try:
        if uploaded_file is not None:
            # Arquivo enviado pelo usuário
            df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
            return df, "arquivo_enviado", len(df)
        
        # Tentar carregar arquivo local primeiro
        if os.path.exists('processed_data.csv'):
            df = pd.read_csv('processed_data.csv', sep=';', encoding='utf-8')
            return df, "arquivo_local", len(df)
        
        # Fallback para dados mínimos
        return pd.DataFrame({
            'FipeID': [92983, 95432],
            'VehicleModelYear': [2024, 2023],
            'BrandName': ['BMW', 'VOLKSWAGEN'],
            'VehicleName': ['118i M Sport 1.5 TB 12V Aut. 5p', 'Polo TSI 1.0 200 Aut. 5p'],
            'ADAS': ['Sim', 'Sim'],
            'Tipo de Regulagem': ['Dinamica', 'Estatica']
        }), "dados_demo", 2
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(), "erro", 0

# Função de busca inteligente
def search_vehicles(query, df):
    if not query or df.empty:
        return []
    
    query = query.upper().strip()
    results = []
    
    # Busca por FIPE ID
    if query.isdigit():
        fipe_matches = df[df['FipeID'].astype(str).str.contains(query)]
        if not fipe_matches.empty:
            return fipe_matches.to_dict('records')
    
    # Busca textual
    for _, row in df.iterrows():
        score = 0
        
        # Score por marca
        if query in str(row.get('BrandName', '')).upper():
            score += 50
        
        # Score por modelo
        if query in str(row.get('VehicleName', '')).upper():
            score += 40
        
        # Score por abreviação
        if 'Abreviação de descrição' in row and query in str(row.get('Abreviação de descrição', '')).upper():
            score += 35
        
        # Score por ano
        if query in str(row.get('VehicleModelYear', '')):
            score += 25
        
        if score > 20:  # Threshold mais baixo para mais resultados
            result = row.to_dict()
            result['search_score'] = score
            results.append(result)
    
    return sorted(results, key=lambda x: x.get('search_score', 0), reverse=True)[:10]

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔧 Sistema Inteligente de Calibração ADAS</h1>
    <p>Plataforma profissional para calibração de sistemas ADAS</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Upload opcional do CSV
    uploaded_file = st.file_uploader(
        "📁 Carregar Base Personalizada",
        type=['csv'],
        help="Opcional: Envie um arquivo CSV personalizado"
    )
    
    st.markdown("---")

# Carregar dados
df, data_source, total_records = load_vehicle_data(uploaded_file)

# Status dos dados
if data_source == "arquivo_enviado":
    st.success(f"✅ Arquivo personalizado carregado: {total_records:,} veículos")
elif data_source == "arquivo_local":
    st.success(f"✅ Base de dados carregada: {total_records:,} veículos com dados ADAS")
elif data_source == "dados_demo":
    st.warning("⚠️ Usando dados de demonstração limitados")
else:
    st.error("❌ Erro ao carregar dados")

# Estatísticas na sidebar
with st.sidebar:
    if not df.empty:
        st.subheader("📊 Estatísticas da Base")
        
        # Métricas básicas
        st.metric("Total de Veículos", f"{len(df):,}")
        
        if 'ADAS' in df.columns:
            adas_count = (df['ADAS'] == 'Sim').sum()
            adas_percent = (adas_count / len(df) * 100) if len(df) > 0 else 0
            st.metric("Veículos com ADAS", f"{adas_count:,} ({adas_percent:.1f}%)")
        
        if 'BrandName' in df.columns:
            unique_brands = df['BrandName'].nunique()
            st.metric("Marcas na Base", unique_brands)
        
        # Top 5 marcas
        if 'BrandName' in df.columns and len(df) > 5:
            st.write("**Top 5 Marcas:**")
            top_brands = df['BrandName'].value_counts().head(5)
            for brand, count in top_brands.items():
                st.write(f"• {brand}: {count:,}")

# Interface de busca
st.subheader("🔍 Buscar Veículo na Base ADAS")

col1, col2 = st.columns([4, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="Digite código FIPE, marca, modelo ou ano (ex: BMW, 92983, Polo, 2024)",
        help="Busque por qualquer informação do veículo"
    )

with col2:
    search_button = st.button("🔍 Buscar", type="primary")

# Processar busca
if search_button and search_query:
    with st.spinner("🔄 Buscando na base de dados..."):
        results = search_vehicles(search_query, df)
    
    if results:
        st.success(f"✅ Encontrados {len(results)} veículo(s) para: '{search_query}'")
        
        for i, vehicle in enumerate(results):
            # Card do veículo
            st.markdown(f"""
            <div class="vehicle-card">
                <h3>🚗 {vehicle.get('BrandName', 'N/A')} {vehicle.get('VehicleName', 'N/A')}</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                    <div><strong>Ano:</strong> {vehicle.get('VehicleModelYear', 'N/A')}</div>
                    <div><strong>FIPE ID:</strong> {vehicle.get('FipeID', 'N/A')}</div>
                    <div><strong>ADAS:</strong> {'✅ Sim' if vehicle.get('ADAS') == 'Sim' else '❌ Não'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detalhes ADAS se disponível
            if vehicle.get('ADAS') == 'Sim':
                st.markdown('<div class="status-positive">', unsafe_allow_html=True)
                st.write("**✅ Este veículo possui sistemas ADAS**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Características ADAS:**")
                    
                    # Mostrar dados reais do CSV
                    adas_features = [
                        ('ADAS no Parabrisa', 'ADAS no Parabrisa'),
                        ('ADAS no Parachoque', 'Adas no Parachoque'),
                        ('Câmera Retrovisor', 'Camera no Retrovisor'),
                        ('Faróis Matrix', 'Faróis Matrix')
                    ]
                    
                    for display_name, col_name in adas_features:
                        if col_name in vehicle:
                            value = vehicle[col_name]
                            if pd.notna(value):
                                icon = "✅" if value == "Sim" else "❌" if value == "Não" else "❓"
                                st.write(f"• {display_name}: {icon}")
                
                with col2:
                    st.write("**⚙️ Informações Técnicas:**")
                    
                    # Informações técnicas do CSV
                    tech_info = [
                        ('Tipo de Regulagem', 'Tipo de Regulagem'),
                        ('Abreviação', 'Abreviação de descrição'),
                        ('Seção', 'Secao'),
                        ('Descrição', 'Descrição')
                    ]
                    
                    for display_name, col_name in tech_info:
                        if col_name in vehicle and pd.notna(vehicle[col_name]):
                            value = vehicle[col_name]
                            if len(str(value)) < 100:  # Evitar textos muito longos
                                st.write(f"• **{display_name}:** {value}")
                
                # Link para documentação oficial
                st.info("""
                📚 **Para instruções de calibração específicas:**
                • Consulte o manual técnico do fabricante
                • Acesse a documentação Bosch: https://help.boschdiagnostics.com/DAS3000/
                • Use equipamento certificado (DAS 3000, VCDS, ODIS, etc.)
                """)
            
            else:
                st.warning("⚠️ Este veículo não possui sistemas ADAS registrados na base.")
            
            st.markdown("---")
    
    else:
        st.error(f"❌ Nenhum veículo encontrado para: '{search_query}'")
        st.info("💡 **Dicas:** Tente termos como 'BMW', 'Polo', 'Mercedes', ou códigos FIPE")

# Mostrar informações sobre a base
if not df.empty and data_source == "arquivo_local":
    st.markdown("---")
    st.subheader("📊 Informações da Base de Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📁 Fonte", "processed_data.csv")
    
    with col2:
        if 'ADAS' in df.columns:
            calibration_types = df['Tipo de Regulagem'].value_counts()
            st.write("**Tipos de Calibração:**")
            for cal_type, count in calibration_types.head(3).items():
                if pd.notna(cal_type):
                    st.write(f"• {cal_type}: {count:,}")
    
    with col3:
        st.write("**Colunas Disponíveis:**")
        st.write(f"• {len(df.columns)} campos por veículo")
        if len(df.columns) > 15:
            st.write("• Base completa carregada ✅")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔧 <strong>Sistema ADAS Pro</strong> | Dados técnicos baseados em informações oficiais</p>
    <p>⚠️ Sempre consulte a documentação oficial do fabricante para procedimentos de calibração</p>
</div>
""", unsafe_allow_html=True)
