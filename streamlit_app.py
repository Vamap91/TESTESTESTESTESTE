import streamlit as st
import pandas as pd
import os

# Configuração da página - DEVE ser a primeira linha Streamlit
st.set_page_config(
    page_title="Sistema ADAS Pro",
    page_icon="🔧",
    layout="wide"
)

# CSS Simplificado
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
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_vehicle_data():
    """Carrega dados com fallback para demo se CSV não existir"""
    
    # Tentar carregar CSV real primeiro
    if os.path.exists('processed_data.csv'):
        try:
            df = pd.read_csv('processed_data.csv', sep=';', encoding='utf-8')
            return df, f"✅ Base real carregada: {len(df):,} veículos"
        except Exception as e:
            st.error(f"Erro ao ler CSV: {e}")
    
    # Fallback: dados de demonstração
    demo_data = {
        'FipeID': [92983, 95432, 87654, 76543, 65432],
        'VehicleModelYear': [2024, 2023, 2024, 2023, 2022],
        'BrandName': ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'AUDI', 'VOLVO'],
        'VehicleName': [
            '118i M Sport 1.5 TB 12V Aut. 5p',
            'Polo TSI 1.0 200 Aut. 5p', 
            'C-Class C200 2.0 TB Aut.',
            'A3 Sedan 1.4 TFSI Aut.',
            'XC60 T5 2.0 TB Aut. AWD'
        ],
        'Abreviação de descrição': [
            'BMW 118i M Sport',
            'Polo TSI 200',
            'Mercedes C200',
            'Audi A3 Sedan',
            'Volvo XC60 T5'
        ],
        'ADAS': ['Sim', 'Sim', 'Sim', 'Sim', 'Sim'],
        'ADAS no Parabrisa': ['Sim', 'Não', 'Sim', 'Sim', 'Sim'],
        'Adas no Parachoque': ['Sim', 'Sim', 'Não', 'Sim', 'Sim'],
        'Tipo de Regulagem': ['Dinâmica', 'Estática', 'Dinâmica', 'Estática', 'Dinâmica'],
        'Camera no Retrovisor': ['Sim', 'Não', 'Sim', 'Sim', 'Sim'],
        'Faróis Matrix': ['Sim', 'Não', 'Sim', 'Sim', 'Não']
    }
    
    df = pd.DataFrame(demo_data)
    return df, "⚠️ Usando dados de demonstração (5 veículos)"

def search_vehicles(query, df):
    """Busca inteligente nos veículos"""
    if not query or df.empty:
        return []
    
    query = query.upper().strip()
    results = []
    
    # Busca por FIPE ID exato
    if query.isdigit():
        fipe_matches = df[df['FipeID'].astype(str) == query]
        if not fipe_matches.empty:
            return fipe_matches.to_dict('records')
    
    # Busca textual com score
    for _, row in df.iterrows():
        score = 0
        
        # Score por marca (peso maior)
        if query in str(row.get('BrandName', '')).upper():
            score += 50
        
        # Score por nome do veículo
        if query in str(row.get('VehicleName', '')).upper():
            score += 40
        
        # Score por abreviação
        if query in str(row.get('Abreviação de descrição', '')).upper():
            score += 35
        
        # Score por ano
        if query in str(row.get('VehicleModelYear', '')):
            score += 25
        
        # Score por FIPE parcial
        if query in str(row.get('FipeID', '')):
            score += 20
        
        if score >= 20:  # Threshold mínimo
            result = row.to_dict()
            result['search_score'] = score
            results.append(result)
    
    # Ordenar por relevância e limitar a 10
    return sorted(results, key=lambda x: x.get('search_score', 0), reverse=True)[:10]

# MAIN APP
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔧 Sistema Inteligente de Calibração ADAS</h1>
        <p>Plataforma Profissional para Consulta de Sistemas ADAS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df, status_message = load_vehicle_data()
    st.info(status_message)
    
    # Sidebar com estatísticas
    with st.sidebar:
        st.header("📊 Estatísticas")
        st.metric("Total de Veículos", f"{len(df):,}")
        
        if 'ADAS' in df.columns:
            adas_count = (df['ADAS'] == 'Sim').sum()
            st.metric("Veículos com ADAS", f"{adas_count:,}")
        
        if 'BrandName' in df.columns:
            st.metric("Marcas Disponíveis", df['BrandName'].nunique())
            
            st.write("**Marcas na Base:**")
            brands = df['BrandName'].value_counts()
            for brand, count in brands.items():
                st.write(f"• {brand}: {count}")
    
    # Interface de busca
    st.subheader("🔍 Buscar Veículo")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input(
            "Digite para buscar:",
            placeholder="Ex: BMW, Polo, 92983, 2024",
            help="Busque por marca, modelo, código FIPE ou ano"
        )
    
    with col2:
        search_button = st.button("🔍 Buscar", type="primary")
    
    # Processar busca
    if search_button and search_query:
        with st.spinner("Buscando..."):
            results = search_vehicles(search_query, df)
        
        if results:
            st.success(f"✅ Encontrados {len(results)} resultado(s)")
            
            for vehicle in results:
                # Card do veículo
                st.markdown(f"""
                <div class="vehicle-card">
                    <h3>🚗 {vehicle.get('BrandName', 'N/A')} - {vehicle.get('VehicleName', 'N/A')}</h3>
                    <p><strong>Ano:</strong> {vehicle.get('VehicleModelYear', 'N/A')} | 
                       <strong>FIPE:</strong> {vehicle.get('FipeID', 'N/A')} | 
                       <strong>ADAS:</strong> {'✅' if vehicle.get('ADAS') == 'Sim' else '❌'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detalhes ADAS
                if vehicle.get('ADAS') == 'Sim':
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**🎯 Características ADAS:**")
                        features = [
                            ('ADAS no Parabrisa', 'ADAS no Parabrisa'),
                            ('ADAS no Parachoque', 'Adas no Parachoque'),
                            ('Câmera Retrovisor', 'Camera no Retrovisor'),
                            ('Faróis Matrix', 'Faróis Matrix')
                        ]
                        
                        for name, key in features:
                            value = vehicle.get(key, 'N/A')
                            icon = "✅" if value == "Sim" else "❌" if value == "Não" else "❓"
                            st.write(f"• {name}: {icon}")
                    
                    with col2:
                        st.write("**⚙️ Informações Técnicas:**")
                        if vehicle.get('Tipo de Regulagem'):
                            st.write(f"• **Tipo de Calibração:** {vehicle['Tipo de Regulagem']}")
                        if vehicle.get('Abreviação de descrição'):
                            st.write(f"• **Modelo:** {vehicle['Abreviação de descrição']}")
                    
                    # Link para Bosch
                    st.info("""
                    📚 **Para calibração específica:**
                    • Consulte: https://help.boschdiagnostics.com/DAS3000/
                    • Use equipamento certificado (DAS 3000, VCDS, ODIS)
                    • Sempre siga o manual oficial do fabricante
                    """)
                
                st.markdown("---")
        
        else:
            st.error(f"❌ Nenhum resultado para: '{search_query}'")
            st.info("💡 Tente: 'BMW', 'Polo', 'Mercedes' ou códigos FIPE")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🔧 Sistema ADAS Pro | ⚠️ Sempre consulte documentação oficial para calibração</p>
    </div>
    """, unsafe_allow_html=True)

# Executar app
if __name__ == "__main__":
    main()
