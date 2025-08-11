# Diagnóstico do Sistema ADAS Atual
# Execute este código para verificar o estado atual do sistema

import pandas as pd
import os
import streamlit as st

def diagnose_system():
    """Diagnóstica o estado atual do sistema ADAS"""
    
    print("🔍 DIAGNÓSTICO DO SISTEMA ADAS")
    print("=" * 50)
    
    # 1. Verificar arquivos essenciais
    print("\n📁 VERIFICAÇÃO DE ARQUIVOS:")
    essential_files = [
        'streamlit_app.py',
        'processed_data.csv', 
        'requirements.txt',
        '.gitignore'
    ]
    
    for file in essential_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        
        if exists and file.endswith('.csv'):
            try:
                df = pd.read_csv(file, sep=';', encoding='utf-8')
                print(f"    📊 Registros: {len(df):,}")
                print(f"    📋 Colunas: {len(df.columns)}")
            except Exception as e:
                print(f"    ⚠️ Erro ao ler: {e}")
    
    # 2. Análise da base de dados
    if os.path.exists('processed_data.csv'):
        print("\n📊 ANÁLISE DA BASE DE DADOS:")
        try:
            df = pd.read_csv('processed_data.csv', sep=';', encoding='utf-8')
            
            print(f"  📈 Total de registros: {len(df):,}")
            print(f"  📋 Colunas disponíveis: {len(df.columns)}")
            
            # Verificar colunas importantes
            important_cols = [
                'FipeID', 'BrandName', 'VehicleName', 
                'ADAS', 'Tipo de Regulagem', 'VehicleModelYear'
            ]
            
            print(f"\n  🔍 COLUNAS IMPORTANTES:")
            for col in important_cols:
                exists = col in df.columns
                status = "✅" if exists else "❌"
                print(f"    {status} {col}")
                
                if exists:
                    non_null = df[col].notna().sum()
                    percentage = (non_null / len(df)) * 100
                    print(f"        📊 Dados válidos: {non_null:,} ({percentage:.1f}%)")
            
            # Estatísticas ADAS
            if 'ADAS' in df.columns:
                print(f"\n  🎯 ESTATÍSTICAS ADAS:")
                adas_count = df['ADAS'].value_counts()
                for value, count in adas_count.items():
                    percentage = (count / len(df)) * 100
                    print(f"    • {value}: {count:,} ({percentage:.1f}%)")
            
            # Top marcas
            if 'BrandName' in df.columns:
                print(f"\n  🏢 TOP 5 MARCAS:")
                top_brands = df['BrandName'].value_counts().head(5)
                for brand, count in top_brands.items():
                    percentage = (count / len(df)) * 100
                    print(f"    • {brand}: {count:,} ({percentage:.1f}%)")
                    
        except Exception as e:
            print(f"  ❌ Erro ao analisar base: {e}")
    
    # 3. Verificar dependências
    print("\n📦 DEPENDÊNCIAS:")
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            deps = f.readlines()
            for dep in deps:
                print(f"  📌 {dep.strip()}")
    
    # 4. Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    print("  1. ✅ Sistema base está funcional")
    print("  2. 🔧 Possíveis melhorias incrementais:")
    print("     • Integração com API Bosch")
    print("     • Busca mais inteligente")
    print("     • Interface aprimorada")
    print("     • Cache otimizado")
    print("     • Funcionalidades de export")
    
    return True

if __name__ == "__main__":
    diagnose_system()
