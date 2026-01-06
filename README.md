# Supabase Cotações - Edge Functions

Sistema de Edge Functions para processamento de cotações de securitização. Implementa os 3 fluxos principais: Tela Inicial, Calculadora de Custos e Gerador de Proposta.

---

## 📋 Pré-requisitos

- **Node.js** v16+ (https://nodejs.org/)
- **Supabase CLI** (instale com: `npm install -g supabase`)
- **Git** (para versionamento)
- **Conta Supabase** (https://supabase.com/)

---

## 🚀 Setup Inicial

### 1. Clonar o Repositório

```bash
git clone seu-repositorio-url
cd supabase-cotacoes
```

### 2. Instalar Dependências

```bash
npm install
```

### 3. Fazer Login no Supabase

```bash
supabase login
```

Isso abrirá uma janela no navegador. Faça login com sua conta Supabase.

### 4. Vincular ao Projeto Supabase

```bash
supabase link --project-ref seu-project-ref
```

Substitua `seu-project-ref` pelo ID do seu projeto Supabase.

Para encontrar o ID:
1. Vá para https://supabase.com/dashboard
2. Clique no seu projeto
3. Vá em Settings → General
4. Copie o "Reference ID"

---

## 📁 Estrutura de Pastas

```
supabase-cotacoes/
├── supabase/
│   ├── functions/
│   │   ├── fluxo-0-listar-emissoes/
│   │   │   └── index.ts
│   │   ├── fluxo-0-detalhes-emissao/
│   │   │   └── index.ts
│   │   ├── fluxo-1-criar-emissao/
│   │   │   └── index.ts
│   │   ├── fluxo-1-atualizar-emissao/
│   │   │   └── index.ts
│   │   ├── fluxo-1-salvar-custos/
│   │   │   └── index.ts
│   │   ├── fluxo-2-gerar-pdf/
│   │   │   └── index.ts
│   │   └── fluxo-2-finalizar-proposta/
│   │       └── index.ts
│   └── config.toml
├── .gitignore
├── package.json
└── README.md
```

---

## 🔧 Desenvolvimento

### Listar Functions

```bash
npm run list
```

### Criar Nova Function

```bash
supabase functions new nome-da-funcao
```

### Editar Function

Abra o arquivo `supabase/functions/nome-da-funcao/index.ts` em seu editor.

### Testar Localmente

```bash
npm run dev
```

Isso inicia um servidor local do Supabase. As functions estarão disponíveis em:
- `http://localhost:54321/functions/v1/fluxo-0-listar-emissoes`
- `http://localhost:54321/functions/v1/fluxo-1-criar-emissao`
- etc.

### Fazer Deploy

```bash
# Deploy todas as functions
npm run deploy

# Ou deploy específico de um fluxo
npm run deploy:fluxo0
npm run deploy:fluxo1
npm run deploy:fluxo2
```

---

## 🌐 Endpoints Disponíveis

### Fluxo 0: Tela Inicial

| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/fluxo-0-listar-emissoes` | Listar cotações com filtros |
| GET | `/fluxo-0-detalhes-emissao/{id}` | Detalhes completos de uma cotação |

### Fluxo 1: Calculadora

| Método | Endpoint | Função |
|--------|----------|--------|
| POST | `/fluxo-1-criar-emissao` | Criar nova cotação |
| PUT | `/fluxo-1-atualizar-emissao/{id}` | Atualizar dados da cotação |
| POST | `/fluxo-1-salvar-custos/{id}` | Salvar custos |

### Fluxo 2: Proposta

| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/fluxo-2-gerar-pdf/{id}` | Gerar HTML/PDF da proposta |
| PUT | `/fluxo-2-finalizar-proposta/{id}` | Finalizar e enviar proposta |

---

## 🔐 Autenticação

Todas as functions requerem autenticação via JWT token do Supabase.

### Exemplo de Requisição

```bash
curl -X GET 'https://seu-projeto.supabase.co/functions/v1/fluxo-0-listar-emissoes' \
  -H 'Authorization: Bearer seu-token-jwt' \
  -H 'Content-Type: application/json'
```

Para obter um token JWT:
1. Vá para https://supabase.com/dashboard
2. Clique no seu projeto
3. Vá em Settings → API
4. Copie o "anon key" ou "service_role key"

---

## 🔄 Workflow de Desenvolvimento em Equipe

### 1. Criar uma Branch

```bash
git checkout -b feature/nome-da-feature
```

### 2. Fazer Alterações

Edite os arquivos em `supabase/functions/`

### 3. Testar Localmente

```bash
npm run dev
```

### 4. Fazer Commit

```bash
git add .
git commit -m "feat: descrição da alteração"
```

### 5. Push para Repositório

```bash
git push origin feature/nome-da-feature
```

### 6. Abrir Pull Request

No GitHub/GitLab, abra um Pull Request para que outros revisem.

### 7. Merge e Deploy

Após aprovação, faça merge em `main` e execute:

```bash
npm run deploy
```

---

## 📝 Padrões de Código

### Estrutura de uma Function

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  // Handle CORS
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    // Seu código aqui
    return new Response(
      JSON.stringify({ success: true, data: {} }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
        status: 200,
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
        status: 400,
      }
    );
  }
});
```

---

## 🆘 Troubleshooting

### Erro: "supabase: command not found"

**Solução:** Instale Supabase CLI globalmente
```bash
npm install -g supabase
```

### Erro: "Project not found"

**Solução:** Verifique o project-ref
```bash
supabase projects list
supabase link --project-ref seu-id-correto
```

### Erro: "Port 54321 already in use"

**Solução:** Pare o servidor anterior
```bash
supabase stop
npm run dev
```

### Erro: "Docker is not running"

**Solução:** Instale e inicie Docker Desktop
- https://www.docker.com/products/docker-desktop

---

## 📚 Recursos Úteis

- [Documentação Supabase](https://supabase.com/docs)
- [Edge Functions Guide](https://supabase.com/docs/guides/functions)
- [Deno Documentation](https://deno.land/manual)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Consulte a documentação Supabase
3. Abra uma issue no repositório

---

## 📄 Licença

MIT

---

## 👥 Contribuidores

- Seu Nome
- Nome do Colega 1
- Nome do Colega 2

---

**Última atualização:** Janeiro 2026

