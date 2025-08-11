import streamlit as st
import pandas as pd
import os

# Configuração da página
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

# Mapeamento específico de calibração por marca - PILOTO
BOSCH_CALIBRATION_LINKS = {
    'ALFA ROMEO': {
        'camera_frontal': [
            {
                'name': 'Calibração da câmera frontal (Opção 1)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/417.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Opção 2)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/407.pdf'
            }
        ],
        'radar_frontal': [
            {
                'name': 'Calibração do radar frontal',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/438.pdf'
            }
        ]
    },
    
    'AUDI': {
        'camera_360': [
            {
                'name': 'Calibração da câmera 360 graus (visão surround)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/498.pdf'
            }
        ],
        'camera_frontal': [
            {
                'name': 'Calibração da câmera frontal (Opção 1)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/418.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Opção 2)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/382.pdf'
            }
        ],
        'camera_traseira': [
            {
                'name': 'Calibração da câmera traseira',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/512.pdf'
            }
        ],
        'radar_frontal': [
            {
                'name': 'Calibração do radar frontal',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/438.pdf'
            }
        ],
        'radar_traseiro': [
            {
                'name': 'Calibração do radar traseiro',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/578.pdf'
            }
        ],
        'lidar': [
            {
                'name': 'Calibração Lidar',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/522.pdf'
            }
        ]
    },
    
    'BENTLEY': {
        'camera_frontal': [
            {
                'name': 'Calibração da câmera frontal (Opção 1)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/462.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Opção 2)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/463.pdf'
            }
        ],
        'radar_frontal': [
            {
                'name': 'Calibração do radar frontal',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/438.pdf'
            }
        ]
    },
    
    'BMW': {
        'radar_frontal': [
            {
                'name': 'Calibração do radar frontal BMW/MINI',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/496.pdf'
            }
        ]
    },
    
    'MINI': {
        'radar_frontal': [
            {
                'name': 'Calibração do radar frontal BMW/MINI',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/496.pdf'
            }
        ]
    },
    
    'MERCEDES': {
        'camera_frontal': [
            {
                'name': 'Calibração da câmera frontal (Padrão)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/425.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Alternativa)',
                'link': 'http://mediathek.bosch-automotive.com/files/common/documents/1690/386072.pdf'
            }
        ],
        'camera_frontal_ar': [
            {
                'name': 'Calibração da câmera frontal (Augmented Reality) - Opção 1',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/539.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Augmented Reality) - Opção 2',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/540.pdf'
            }
        ],
        'camera_traseira': [
            {
                'name': 'Calibração da câmera traseira',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/508.pdf'
            }
        ]
    },
    
    'MERCEDES-BENZ': {
        'camera_frontal': [
            {
                'name': 'Calibração da câmera frontal (Padrão)',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/425.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Alternativa)',
                'link': 'http://mediathek.bosch-automotive.com/files/common/documents/1690/386072.pdf'
            }
        ],
        'camera_frontal_ar': [
            {
                'name': 'Calibração da câmera frontal (Augmented Reality) - Opção 1',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/539.pdf'
            },
            {
                'name': 'Calibração da câmera frontal (Augmented Reality) - Opção 2',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/540.pdf'
            }
        ],
        'camera_traseira': [
            {
                'name': 'Calibração da câmera traseira',
                'link': 'http://mediathek.bosch-automotive.com/files/bosch_wa/989/508.pdf'
            }
        ]
    }
}

def get_calibration_links(brand_name, vehicle_data):
    """Retorna links específicos de calibração baseado na marca e características do veículo"""
    if not brand_name:
        return []
    
    # Normalizar nome da marca
    brand_upper = brand_name.upper().strip()
    
    # Verificar se a marca está no piloto
    if brand_upper not in BOSCH_CALIBRATION_LINKS:
        return []
    
    brand_links = BOSCH_CALIBRATION_LINKS[brand_upper]
    available_links = []
    
    # Mapear características do veículo para tipos de calibração
    characteristics = {
        'ADAS no Parabrisa': vehicle_data.get('ADAS no Parabrisa', ''),
        'Adas no Parachoque': vehicle_data.get('Adas no Parachoque', ''),
        'Camera no Retrovisor': vehicle_data.get('Camera no Retrovisor', ''),
        'Faróis Matrix': vehicle_data.get('Faróis Matrix', '')
    }
    
    # Câmera frontal (ADAS no parabrisa)
    if characteristics['ADAS no Parabrisa'] == 'Sim':
        if 'camera_frontal' in brand_links:
            available_links.extend(brand_links['camera_frontal'])
        # Para Mercedes, verificar se tem AR
        if brand_upper in ['MERCEDES', 'MERCEDES-BENZ'] and 'camera_frontal_ar' in brand_links:
            available_links.extend(brand_links['camera_frontal_ar'])
    
    # Radar frontal (ADAS no parachoque)
    if characteristics['Adas no Parachoque'] == 'Sim':
        if 'radar_frontal' in brand_links:
            available_links.extend(brand_links['radar_frontal'])
    
    # Câmera traseira (baseado em câmera retrovisor)
    if characteristics['Camera no Retrovisor'] == 'Sim':
        if 'camera_traseira' in brand_links:
            available_links.extend(brand_links['camera_traseira'])
        if 'radar_traseiro' in brand_links:
            available_links.extend(brand_links['radar_traseiro'])
    
    # Para Audi, adicionar opções especiais
    if brand_upper == 'AUDI':
        if 'camera_360' in brand_links:
            available_links.extend(brand_links['camera_360'])
        if 'lidar' in brand_links:
            available_links.extend(brand_links['lidar'])
    
    return available_links

# Mapeamento das marcas para links da documentação Bosch (fallback)
BOSCH_LINKS = {
    'ALFA ROMEO': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'AUDI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'BENTLEY': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'BMW': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MINI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'CITROEN': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'CUPRA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'DAIHATSU': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'FIAT': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'JEEP': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'FORD': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'HONDA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'HYUNDAI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'INFINITI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'IVECO': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'KIA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'LAMBORGHINI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'LEXUS': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MAN': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MASERATI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MAZDA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MERCEDES': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MERCEDES-BENZ': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'MITSUBISHI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'NISSAN': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'OPEL': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'PEUGEOT': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'POLESTAR': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'PORSCHE': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'RENAULT': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'SEAT': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'SKODA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'SMART': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'SUBARU': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'SUZUKI': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'TOYOTA': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'VOLKSWAGEN': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'VOLVO': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default',
    'LAND ROVER': 'https://help.boschdiagnostics.com/DAS3000/#/home/Onepager/pt/default'
}

def get_bosch_link(brand_name):
    """Retorna o link específico da Bosch para a marca"""
    if not brand_name:
        return None
    
    # Normalizar nome da marca
    brand_upper = brand_name.upper().strip()
    
    # Verificar variações comuns
    brand_mapping = {
        'BMW/MINI': 'BMW',
        'FIAT/JEEP': 'FIAT',
        'MERCEDES-BENZ': 'MERCEDES',
        'VOLVO CAMINHÕES': 'VOLVO'
    }
    
    brand_normalized = brand_mapping.get(brand_upper, brand_upper)
    
    return BOSCH_LINKS.get(brand_normalized)

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

def search_vehicles(query, df, year_filter=None):
    """Busca inteligente nos veículos com filtro de ano"""
    if df.empty:
        return []
    
    # Aplicar filtro de ano primeiro
    filtered_df = df.copy()
    if year_filter and year_filter != "Todos os anos":
        try:
            year_int = int(year_filter)
            filtered_df = filtered_df[filtered_df['VehicleModelYear'] == year_int]
        except ValueError:
            pass
    
    # Se não há query, retornar apenas filtro de ano
    if not query:
        if year_filter and year_filter != "Todos os anos":
            return filtered_df.head(20).to_dict('records')  # Limitar a 20 resultados
        else:
            return []
    
    query = query.upper().strip()
    results = []
    
    # Busca por FIPE ID exato
    if query.isdigit():
        fipe_matches = filtered_df[filtered_df['FipeID'].astype(str) == query]
        if not fipe_matches.empty:
            return fipe_matches.to_dict('records')
    
    # Busca textual com score
    for _, row in filtered_df.iterrows():
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
    
    # Filtros de busca
    col1, col2, col3 = st.columns([3, 1.5, 1])
    
    with col1:
        search_query = st.text_input(
            "Digite para buscar:",
            placeholder="Ex: BMW, Polo, 92983",
            help="Busque por marca, modelo ou código FIPE"
        )
    
    with col2:
        # Filtro de ano
        years_available = sorted(df['VehicleModelYear'].unique(), reverse=True)
        year_filter = st.selectbox(
            "📅 Filtrar por Ano:",
            options=["Todos os anos"] + [str(year) for year in years_available],
            help="Selecione um ano específico"
        )
    
    with col3:
        search_button = st.button("🔍 Buscar", type="primary")
    
    # Processar busca
    if search_button or search_query or (year_filter and year_filter != "Todos os anos"):
        with st.spinner("Buscando..."):
            results = search_vehicles(search_query, df, year_filter)
        
        if results:
            # Mostrar filtros aplicados
            filters_applied = []
            if search_query:
                filters_applied.append(f"Termo: '{search_query}'")
            if year_filter and year_filter != "Todos os anos":
                filters_applied.append(f"Ano: {year_filter}")
            
            filter_text = " | ".join(filters_applied) if filters_applied else "Todos"
            st.success(f"✅ Encontrados {len(results)} resultado(s) - Filtros: {filter_text}")
            
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
                    
                    # Links específicos de calibração para o piloto
                    brand_name = vehicle.get('BrandName', '')
                    calibration_links = get_calibration_links(brand_name, vehicle)
                    
                    if calibration_links:
                        st.success(f"""
                        🎯 **Links Específicos de Calibração para {brand_name}:**
                        """)
                        
                        # Organizar links por categoria
                        st.markdown("### 📋 **Instruções Específicas Disponíveis:**")
                        
                        for i, link_data in enumerate(calibration_links):
                            col_link1, col_link2 = st.columns([3, 1])
                            
                            with col_link1:
                                st.markdown(f"""
                                **📖 {link_data['name']}**  
                                *Compatível com as características detectadas neste veículo*
                                """)
                            
                            with col_link2:
                                st.markdown(f"""
                                <a href="{link_data['link']}" target="_blank">
                                    <button style="
                                        background: linear-gradient(90deg, #dc3545, #c82333);
                                        color: white;
                                        border: none;
                                        padding: 8px 16px;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        font-weight: bold;
                                        width: 100%;
                                        font-size: 12px;
                                    ">
                                        📄 Abrir PDF
                                    </button>
                                </a>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                        
                        # Resumo das características que geraram os links
                        st.info(f"""
                        ✅ **Links baseados nas características detectadas:**
                        • ADAS no Parabrisa: {vehicle.get('ADAS no Parabrisa', 'N/A')}
                        • ADAS no Parachoque: {vehicle.get('Adas no Parachoque', 'N/A')}
                        • Câmera Retrovisor: {vehicle.get('Camera no Retrovisor', 'N/A')}
                        • Faróis Matrix: {vehicle.get('Faróis Matrix', 'N/A')}
                        """)
                        
                        # Aviso importante
                        st.warning("""
                        ⚠️ **IMPORTANTE - PILOTO ATIVO:**
                        • Estes links são específicos para **{brand_name}**
                        • Sempre verifique a compatibilidade exata do modelo
                        • Use apenas equipamento certificado (DAS 3000, etc.)
                        • Siga rigorosamente as instruções do PDF
                        """.format(brand_name=brand_name))
                    
                    else:
                        # Para marcas não cobertas pelo piloto
                        if brand_name.upper() in ['ALFA ROMEO', 'AUDI', 'BENTLEY', 'BMW', 'MINI', 'MERCEDES', 'MERCEDES-BENZ']:
                            st.warning(f"""
                            🔧 **{brand_name} - Piloto em Desenvolvimento**
                            • Esta marca está em nossa base piloto
                            • Links específicos serão exibidos conforme características detectadas
                            • Para este veículo específico, consulte manual geral
                            """)
                        else:
                            st.info(f"""
                            📚 **{brand_name} - Consulta Manual Necessária**
                            • Esta marca ainda não está no piloto de links específicos
                            • Consulte a documentação geral da Bosch
                            • Em breve teremos links específicos para mais marcas
                            """)
                        
                        # Link para documentação geral
                        st.markdown(f"""
                        <a href="https://help.boschdiagnostics.com/DAS3000/" target="_blank">
                            <button style="
                                background: linear-gradient(90deg, #007bff, #0056b3);
                                color: white;
                                border: none;
                                padding: 10px 20px;
                                border-radius: 5px;
                                cursor: pointer;
                                font-weight: bold;
                                width: 100%;
                            ">
                                📖 Acessar Documentação Geral Bosch
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
        
        else:
            filter_msg = f" com filtros aplicados" if (search_query or year_filter != "Todos os anos") else ""
            st.error(f"❌ Nenhum resultado encontrado{filter_msg}")
            st.info("💡 Tente: 'BMW', 'Polo', 'Mercedes' ou códigos FIPE")
    
    # Exibir dica quando não há busca
    elif not search_query and (not year_filter or year_filter == "Todos os anos"):
        st.info("💡 **Dica:** Digite um termo de busca ou selecione um ano para começar")
        
        # Mostrar algumas estatísticas interessantes
        st.subheader("📊 Resumo da Base")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_adas = (df['ADAS'] == 'Sim').sum()
            st.metric("Veículos com ADAS", f"{total_adas:,}")
        
        with col2:
            if 'Tipo de Regulagem' in df.columns:
                dinamica = (df['Tipo de Regulagem'] == 'Dinâmica').sum()
                st.metric("Calibração Dinâmica", f"{dinamica:,}")
        
        with col3:
            if 'Tipo de Regulagem' in df.columns:
                estatica = (df['Tipo de Regulagem'] == 'Estática').sum()
                st.metric("Calibração Estática", f"{estatica:,}")
        
        with col4:
            years_range = f"{df['VehicleModelYear'].min()}-{df['VehicleModelYear'].max()}"
            st.metric("Faixa de Anos", years_range)
    
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
