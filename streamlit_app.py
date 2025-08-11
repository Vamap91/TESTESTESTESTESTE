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
    .calibration-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .step-box {
        background: #fff3cd;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 3px solid #ffc107;
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

# Função para obter instruções de calibração
def get_calibration_instructions(brand, calibration_type):
    instructions_db = {
        'BMW': {
            'title': '🔧 Calibração BMW ADAS',
            'duration': '60-90 minutos',
            'difficulty': 'Intermediário',
            'steps': [
                'Conectar DAS 3000 ou equipamento compatível BMW',
                'Verificar códigos de defeito e limpar se necessário',
                'Verificar pressão dos pneus conforme especificação BMW',
                'Selecionar "BMW" → "Sistemas ADAS" no equipamento',
                'Escolher tipo de calibração (Estática/Dinâmica)',
                'Seguir procedimento guiado no equipamento',
                'Realizar test drive para validação (se dinâmica)',
                'Verificar funcionamento de todos os sistemas ADAS'
            ],
            'requirements': [
                'Equipamento DAS 3000 ou compatível BMW',
                'Superfície plana e nivelada para calibração estática',
                'Pista de teste adequada para calibração dinâmica',
                'Condições climáticas favoráveis (sem chuva intensa)',
                'Pneus calibrados conforme especificação',
                'Alinhamento e geometria da direção em dia'
            ],
            'warnings': [
                'Verificar recalls de software antes da calibração',
                'Não realizar calibração com códigos de defeito ativos',
                'Temperatura ambiente deve estar entre 5°C e 35°C'
            ]
        },
        'VOLKSWAGEN': {
            'title': '🔧 Calibração Volkswagen ADAS',
            'duration': '30-60 minutos',
            'difficulty': 'Básico',
            'steps': [
                'Conectar VCDS, ODIS ou equipamento compatível',
                'Verificar e limpar códigos de defeito',
                'Posicionar veículo conforme especificações VW',
                'Instalar targets de calibração específicos VW/Audi',
                'Acessar Central de Conforto → Sistemas ADAS',
                'Executar "Calibração da Câmera Frontal"',
                'Aguardar conclusão sem mover o veículo',
                'Verificar funcionamento dos sistemas'
            ],
            'requirements': [
                'VCDS, ODIS ou equipamento compatível',
                'Targets específicos do grupo VW/Audi',
                'Ambiente com iluminação controlada',
                'Bateria com carga mínima de 12,5V',
                'Sistema de direção centralizado'
            ],
            'warnings': [
                'Respeitar distâncias exatas para targets',
                'Não mover o veículo durante calibração estática',
                'Verificar se para-brisa não possui trincas'
            ]
        },
        'MERCEDES-BENZ': {
            'title': '🔧 Calibração Mercedes-Benz ADAS',
            'duration': '60-120 minutos',
            'difficulty': 'Avançado',
            'steps': [
                'Conectar Star Diagnosis ou DAS 3000',
                'Selecionar modelo específico do veículo Mercedes',
                'Acessar menu "Sistemas de Assistência ao Condutor"',
                'Selecionar "Calibração Radar/Câmera"',
                'Verificar geometria e altura da suspensão',
                'Seguir procedimento guiado passo a passo',
                'Confirmar alinhamento de todos os sensores',
                'Realizar test drive de validação completo'
            ],
            'requirements': [
                'Star Diagnosis ou DAS 3000 atualizado',
                'Reflectores específicos Mercedes-Benz',
                'Verificação da altura correta da suspensão',
                'Pressão dos pneus conforme especificação MB',
                'Centro de alinhamento certificado Mercedes'
            ],
            'warnings': [
                'Alguns modelos requerem atualização de software obrigatória',
                'Verificar se suspensão não foi modificada',
                'Temperatura de operação: -10°C a +50°C'
            ]
        }
    }
    
    # Instruções padrão para marcas não mapeadas
    default_instructions = {
        'title': f'🔧 Calibração {brand} ADAS',
        'duration': '45-75 minutos',
        'difficulty': 'Intermediário',
        'steps': [
            'Conectar equipamento de diagnóstico adequado',
            'Verificar pré-requisitos do sistema',
            'Seguir procedimento específico do fabricante',
            'Realizar validação conforme manual técnico'
        ],
        'requirements': [
            'Equipamento compatível com a marca',
            'Manual técnico atualizado',
            'Ambiente adequado para calibração'
        ],
        'warnings': [
            'Consultar documentação específica',
            'Verificar atualizações disponíveis'
        ]
    }
    
    return instructions_db.get(brand, default_instructions)

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
            # Card do veículo
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
            
            # Instruções de calibração
            if vehicle['ADAS'] == 'Sim':
                instructions = get_calibration_instructions(
                    vehicle['BrandName'], 
                    vehicle['TipoRegulagem']
                )
                
                # Header das instruções
                st.markdown(f"""
                <div class="calibration-header">
                    <h3>{instructions['title']}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                        <div><strong>⏱️ Duração:</strong> {instructions['duration']}</div>
                        <div><strong>📊 Dificuldade:</strong> {instructions['difficulty']}</div>
                        <div><strong>🔧 Tipo:</strong> Calibração Profissional</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Procedimento e requisitos
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📝 Procedimento Passo a Passo")
                    for j, step in enumerate(instructions['steps'], 1):
                        st.markdown(f"""
                        <div class="step-box">
                            <strong>Passo {j}:</strong> {step}
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.subheader("📋 Requisitos")
                    for req in instructions['requirements']:
                        st.write(f"• {req}")
                    
                    st.subheader("⚠️ Avisos Importantes")
                    for warning in instructions['warnings']:
                        st.warning(f"⚠️ {warning}")
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📋 Gerar Relatório", key=f"report_{i}"):
                        st.success("✅ Relatório gerado!")
                        st.info("💾 Funcionalidade de download será implementada")
                
                with col2:
                    if st.button(f"⭐ Favoritar", key=f"fav_{i}"):
                        st.success("⭐ Adicionado aos favoritos!")
                
                with col3:
                    if st.button(f"🔧 Troubleshooting", key=f"trouble_{i}"):
                        st.info("🔧 Guia de solução de problemas em desenvolvimento")
            
            st.markdown("---")
    
    else:
        st.error(f"❌ Nenhum veículo encontrado para: '{search_query}'")
        st.info("💡 Dicas: Tente 'BMW', 'Polo', ou '92983'")

# Mostrar base de dados
st.markdown("---")
st.subheader("📊 Base de Dados Completa")
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🔧 <strong>Sistema ADAS Pro</strong> | Desenvolvido para profissionais da área automotiva</p>
    <p>💡 Sugestões? Entre em contato: desenvolvimento@adas.com</p>
</div>
""", unsafe_allow_html=True)

st.write(f"**Versão do Streamlit:** {st.__version__}")
