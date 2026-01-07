#!/usr/bin/env python3
"""
Script para popular o Supabase Cloud com dados fakes
Usa os campos CORRETOS da tabela emissoes
"""

import requests
import json
from datetime import datetime, timedelta
import random

# Configuração
SUPABASE_URL = "https://gthtvpujwukbfgokghne.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd0aHR2cHVqd3VrYmZnb2tnaG5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc3MDU4MjYsImV4cCI6MjA4MzI4MTgyNn0.viQaLgE8Kk32DCtEAUEglxCR8bwBwhrIqAh_JIfdxv4"

# Headers para requisições
headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Dados fake
nomes_empresas = [
    "Tech Solutions", "Global Finance", "Inovação Brasil",
    "Capital Ventures", "Smart Investments", "Future Corp",
    "Digital Assets", "Quantum Finance", "Prime Capital"
]

categorias = ["DEB", "CRA", "CRI", "NC", "CR"]
status_list = ["rascunho", "enviada", "aceita", "estruturando", "estruturada"]

print("=" * 80)
print("POPULADOR DE SUPABASE CLOUD - VERSÃO CORRIGIDA")
print("=" * 80)

# ============================================================================
# 1. CRIAR EMISSÕES (com campos corretos)
# ============================================================================
print("\n📊 Criando emissões no Supabase Cloud...")

emissoes = []
for i in range(5):
    emissao = {
        "numero_emissao": f"EMIT-{2025}-{1000+i}",
        "demandante_proposta": random.choice(nomes_empresas),
        "empresa_destinataria": random.choice(nomes_empresas),
        "categoria": random.choice(categorias),
        "volume": float(random.randint(1000000, 50000000)),
        "quantidade_series": random.randint(1, 5),
        "valor_mobiliario": float(random.randint(1000000, 50000000)),
        "status_proposta": random.choice(status_list),
        "fee_estruturacao": round(random.uniform(0.5, 5.0), 2),
        "fee_gestao": round(random.uniform(0.5, 3.0), 2),
        "fee_coordenador_lider": round(random.uniform(0.5, 2.0), 2),
        "fee_colocacao": round(random.uniform(0.5, 2.0), 2),
        "observacao": f"Emissão de {random.choice(categorias)} para financiamento",
    }
    emissoes.append(emissao)

emissoes_ids = {}
for emissao in emissoes:
    try:
        url = f"{SUPABASE_URL}/rest/v1/emissoes"
        response = requests.post(url, json=emissao, headers=headers)
        
        if response.status_code in [200, 201]:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                emissoes_ids[emissao["numero_emissao"]] = data[0]["id"]
                print(f"  ✅ {emissao['numero_emissao']} - {emissao['categoria']} - R$ {emissao['volume']:,.0f}")
            else:
                print(f"  ⚠️  {emissao['numero_emissao']}: Resposta vazia - {response.text[:100]}")
        else:
            print(f"  ⚠️  {emissao['numero_emissao']}: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"  ❌ {emissao['numero_emissao']}: {str(e)[:50]}")

print(f"\n✅ Total de emissões criadas: {len(emissoes_ids)}")

# ============================================================================
# 2. CRIAR SÉRIES
# ============================================================================
print("\n📈 Criando séries...")

series_count = 0
for emissao_num, emissao_id in list(emissoes_ids.items())[:3]:
    for j in range(random.randint(1, 3)):
        serie = {
            "id_emissao": emissao_id,
            "numero_serie": f"SERIE-{j+1}",
            "valor_emissao": float(random.randint(100000, 10000000)),
            "data_emissao": datetime.now().isoformat(),
            "data_integralizacao": (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat(),
            "data_vencimento": (datetime.now() + timedelta(days=random.randint(365, 1825))).isoformat(),
            "taxa_juros": round(random.uniform(0.5, 15.0), 2),
        }
        try:
            url = f"{SUPABASE_URL}/rest/v1/series"
            response = requests.post(url, json=serie, headers=headers)
            
            if response.status_code in [200, 201]:
                series_count += 1
                print(f"  ✅ {emissao_num} - {serie['numero_serie']} - R$ {serie['valor_emissao']:,.0f}")
            else:
                print(f"  ⚠️  {emissao_num} - {serie['numero_serie']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {emissao_num} - {serie['numero_serie']}: {str(e)[:50]}")

print(f"\n✅ Total de séries criadas: {series_count}")

# ============================================================================
# 3. CRIAR CUSTOS
# ============================================================================
print("\n💸 Criando custos...")

tipos_custos = [
    "taxa_estruturacao",
    "taxa_agente_fiduciario",
    "taxa_securitizadora",
    "taxa_liquidante",
    "taxa_custodia",
    "taxa_auditoria",
]

custos_count = 0
for emissao_num, emissao_id in list(emissoes_ids.items())[:2]:
    for tipo_custo in tipos_custos[:random.randint(3, 6)]:
        custo = {
            "id_emissao": emissao_id,
            "tipo": tipo_custo,
            "valor": float(random.randint(5000, 100000)),
            "descricao": f"Custo de {tipo_custo.replace('_', ' ')}",
        }
        try:
            url = f"{SUPABASE_URL}/rest/v1/custos"
            response = requests.post(url, json=custo, headers=headers)
            
            if response.status_code in [200, 201]:
                custos_count += 1
                print(f"  ✅ {tipo_custo}: R$ {custo['valor']:,.0f}")
            else:
                print(f"  ⚠️  {tipo_custo}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {tipo_custo}: {str(e)[:50]}")

print(f"\n✅ Total de custos criados: {custos_count}")

# ============================================================================
# RESUMO
# ============================================================================
print("\n" + "=" * 80)
print("✅ POPULAÇÃO CONCLUÍDA!")
print("=" * 80)
print(f"\n📊 Resumo:")
print(f"  • Emissões criadas: {len(emissoes_ids)}")
print(f"  • Séries criadas: {series_count}")
print(f"  • Custos criados: {custos_count}")
print(f"\n🎉 Dados foram para o Supabase Cloud!")
print(f"\n💡 Próximo passo: Teste as functions novamente!")
print("\n")
