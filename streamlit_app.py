# Debug dos Problemas Atuais - Sistema ADAS
# Execute este script para identificar os problemas

import os
import sys
import pandas as pd

def debug_current_issues():
    """Identifica problemas específicos que impedem a execução"""
    
    print("🔧 DEBUG - PROBLEMAS ATUAIS")
    print("=" * 40)
    
    # 1. Verificar se o streamlit_app.py existe e é válido
    print("\n📝 VERIFICANDO streamlit_app.py:")
    
    if not os.path.exists('streamlit_app.py'):
        print("  ❌ Arquivo streamlit_app.py NÃO encontrado!")
        print("  💡 Solução: Criar o arquivo principal")
        return False
    
    print("  ✅ Arquivo encontrado")
    
    # 2. Verificar sintaxe do Python
    print("\n🐍 VERIFICANDO SINTAXE PYTHON:")
    try:
        with open('streamlit_app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            compile(content, 'streamlit_app.py', 'exec')
        print("  ✅ Sintaxe Python válida")
    except SyntaxError as e:
        print(f"  ❌ ERRO DE SINTAXE: {e}")
        print(f"  📍 Linha {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"  ❌ ERRO ao ler arquivo: {e}")
        return False
    
    # 3. Verificar se processed_data.csv existe
    print("\n📊 VERIFICANDO DADOS:")
    
    if not os.path.exists('processed_data.csv'):
        print("  ❌ Arquivo processed_data.csv NÃO encontrado!")
        print("  💡 Este é provavelmente o PROBLEMA PRINCIPAL")
        print("  📋 Soluções possíveis:")
        print("     1. Adicionar o arquivo CSV real")
        print("     2. Criar dados de teste")
        print("     3. Modificar código para funcionar sem o arquivo")
        return False
    
    print("  ✅ Arquivo CSV encontrado")
    
    # 4. Verificar se consegue ler o CSV
    try:
        df = pd.read_csv('processed_data.csv', sep=';', encoding='utf-8')
        print(f"  ✅ CSV lido com sucesso: {len(df)} registros")
        
        # Verificar colunas essenciais
        required_columns = ['FipeID', 'BrandName', 'VehicleName', 'ADAS']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"  ⚠️ Colunas faltando: {missing_columns}")
            print(f"  📋 Colunas disponíveis: {list(df.columns)}")
        else:
            print("  ✅ Colunas essenciais presentes")
            
    except Exception as e:
        print(f"  ❌ ERRO ao ler CSV: {e}")
        print("  💡 Possíveis problemas:")
        print("     • Encoding incorreto")
        print("     • Separador incorreto")
        print("     • Arquivo corrompido")
        return False
    
    # 5. Verificar dependências
    print("\n📦 VERIFICANDO DEPENDÊNCIAS:")
    
    try:
        import streamlit
        print(f"  ✅ Streamlit: {streamlit.__version__}")
    except ImportError:
        print("  ❌ Streamlit não instalado")
        print("  💡 Execute: pip install streamlit")
        return False
    
    try:
        import pandas
        print(f"  ✅ Pandas: {pandas.__version__}")
    except ImportError:
        print("  ❌ Pandas não instalado")
        return False
    
    # 6. Testar execução básica do Streamlit
    print("\n🚀 TESTE DE EXECUÇÃO:")
    print("  💡 Para testar, execute:")
    print("     streamlit run streamlit_app.py")
    print("")
    print("  🔍 Se der erro, verifique:")
    print("     • Porta 8501 disponível")
    print("     • Firewall liberado")
    print("     • Streamlit Cloud configurado")
    
    return True

def suggest_fixes():
    """Sugere correções baseadas nos problemas encontrados"""
    
    print("\n🛠️ CORREÇÕES SUGERIDAS:")
    print("=" * 30)
    
    if not os.path.exists('processed_data.csv'):
        print("\n❗ PROBLEMA CRÍTICO: Falta o arquivo de dados")
        print("\n📋 SOLUÇÕES IMEDIATAS:")
        print("1. 🔄 SOLUÇÃO RÁPIDA - Criar dados de teste:")
        print("   • Modificar código para funcionar sem o CSV real")
        print("   • Usar dados de demonstração embutidos")
        
        print("\n2. 📁 SOLUÇÃO COMPLETA - Adicionar CSV real:")
        print("   • Localizar o arquivo processed_data.csv original")
        print("   • Verificar se está no diretório correto")
        print("   • Confirmar encoding UTF-8 e separador ';'")
        
        print("\n3. 🚀 SOLUÇÃO DE EMERGÊNCIA - Sistema sem CSV:")
        print("   • Modificar para buscar dados online")
        print("   • Usar base de dados alternativa")
    
    print("\n💡 QUAL SOLUÇÃO VOCÊ PREFERE?")
    print("A) Modificar código para funcionar sem CSV (mais rápido)")
    print("B) Localizar e corrigir o arquivo CSV original")
    print("C) Criar sistema híbrido com fallback")

if __name__ == "__main__":
    if debug_current_issues():
        print("\n✅ Sistema parece estar OK")
    else:
        suggest_fixes()
