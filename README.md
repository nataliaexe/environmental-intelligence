# Cortex

**Plataforma de inteligência ambiental e resiliência.**

Cortex é um projeto em desenvolvimento para monitorar condições ambientais,
identificar sinais de risco e apoiar decisões de resposta. A visão de longo
prazo é conectar sensores, modelos de análise, simulações e equipes ou agentes
de campo em um fluxo único — mantendo qualquer ação física sujeita a regras de
segurança e, quando necessário, à aprovação humana.

> **Estado atual:** o repositório contém um dashboard MVP com dados
> demonstrativos, uma API FastAPI inicial e uma base de persistência em
> PostgreSQL/TimescaleDB. O dashboard ainda não está conectado à API. Os dados
> exibidos na interface não são medições reais nem previsões.

## Conteúdo

- [O que o MVP faz hoje](#o-que-o-mvp-faz-hoje)
- [Como funciona](#como-funciona)
- [Arquitetura e tecnologias](#arquitetura-e-tecnologias)
- [Começar a desenvolver](#começar-a-desenvolver)
- [API disponível](#api-disponível)
- [Testes](#testes)
- [Limitações conhecidas](#limitações-conhecidas)
- [Evolução planejada](#evolução-planejada)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Princípios do projeto](#princípios-do-projeto)

## O que o MVP faz hoje

### Dashboard

A aplicação web apresenta uma visão demonstrativa de um ecossistema monitorado:

- indicadores de saúde do ecossistema, alertas, sensores e temperatura;
- mapa esquemático com regiões selecionáveis e respectivos indicadores;
- resumo regional de temperatura, umidade do ar e umidade do solo;
- gráfico ilustrativo de estabilidade ambiental, com seleção de período;
- lista de alertas demonstrativos que podem ser reconhecidos na interface;
- seletor de cenários ambientais e controle demonstrativo de início e término.

As interações do dashboard — seleção de regiões e períodos, reconhecimento de
alertas e simulação — acontecem localmente no navegador. Os valores da tela são
definidos no frontend e não são sincronizados com sensores, banco de dados ou
API.

### Backend

A API inicial oferece:

- endpoints de saúde e identificação do serviço;
- uma representação de ambiente de demonstração com regiões, sensores e um
  agente;
- recebimento, validação e persistência de telemetria;
- consultas de telemetria recente e da leitura mais recente de um sensor;
- consulta de eventos ambientais ativos e filtrados por região;
- controle básico do estado de uma simulação em memória.

O código também contém componentes de domínio e serviços em evolução para
análise de anomalias, eventos, avaliação e propagação de risco, segurança,
missões e coordenação de agentes. Esses componentes ainda não formam um fluxo
completo acionado pelo dashboard ou por uma única operação pública da API.

## Como funciona

### Fluxo existente

```text
Dashboard demonstrativo (Next.js)
  └── dados e interações locais, sem integração com a API

Cliente ou dispositivo
  └── POST /api/telemetry
        └── validação do payload
              └── persistência no PostgreSQL/TimescaleDB

Cliente da API
  ├── consulta telemetria: GET /api/telemetry/...
  ├── consulta ambiente demonstrativo: GET /api/environment
  ├── consulta eventos persistidos: GET /api/events...
  └── controla estado de simulação em memória: /api/simulation/...
```

Uma leitura de telemetria precisa informar o sensor, a região, o horário da
medição e os valores ambientais. O backend valida os campos, registra o horário
de recebimento e persiste a leitura. A consulta de eventos lê eventos ativos já
persistidos; o endpoint de telemetria ainda não está conectado automaticamente
a um pipeline de detecção de anomalias.

### Fluxo pretendido

```text
Sensores ou simulador
  → ingestão e validação
  → persistência de séries temporais
  → fusão e análise de observações
  → detecção de anomalias e geração de eventos
  → avaliação e propagação de risco
  → planejamento de resposta
  → autorização e execução segura
  → verificação do resultado e atualização do dashboard
```

Esse fluxo é a direção arquitetural do projeto, não uma promessa de que todas
as etapas já estejam integradas ou prontas para operação.

## Arquitetura e tecnologias

| Camada | Tecnologia | Uso atual |
|---|---|---|
| Interface web | Next.js, React, TypeScript e Tailwind CSS | Dashboard demonstrativo e interações locais |
| API | Python, FastAPI e Pydantic | Endpoints REST, validação de payload e documentação OpenAPI |
| Persistência | PostgreSQL, TimescaleDB e SQLAlchemy | Modelos e persistência de telemetria, eventos e entidades ambientais |
| Evolução do esquema | Alembic | Migrações do banco |
| Testes | pytest | Testes de domínio, importação, persistência e integração |
| Infraestrutura local | Docker Compose | Serviço PostgreSQL/TimescaleDB |

MQTT, dispositivos ESP32, visualização geográfica real, análise baseada em
modelos de machine learning e integração do dashboard com a API são
possibilidades de evolução; não são requisitos necessários para experimentar a
interface atual.

## Começar a desenvolver

### Pré-requisitos

- Node.js compatível com Next.js 16 (Node.js 20.9 ou superior) e npm;
- Python 3.10 ou superior;
- Docker e Docker Compose, para executar o banco local.

### 1. Configurar o banco

Na raiz do repositório, crie o arquivo local de configuração:

```bash
cp .env.example .env
```

Acrescente ao `.env` uma senha local para o Compose e a URL de conexão usada
pela API e pelas migrações:

```dotenv
POSTGRES_PASSWORD=dev-password
DATABASE_URL=postgresql+psycopg://environmental:dev-password@127.0.0.1:5433/environmental_intelligence
```

Inicie o serviço:

```bash
docker compose --env-file .env -f infra/docker-compose.yml up -d
```

O banco fica disponível na porta `5433` do host. O contêiner inicializa a
extensão TimescaleDB; as tabelas da aplicação são criadas pelas migrações do
Alembic.

### 2. Instalar dependências e preparar o backend

O manifesto atual de `backend/requirements.txt` não lista todas as dependências
importadas pelo backend. Para o ambiente local, instale também SQLAlchemy,
Alembic, o driver PostgreSQL e pytest:

```bash
python -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements.txt
python -m pip install sqlalchemy alembic "psycopg[binary]" pytest
```

No Windows PowerShell, ative o ambiente com:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Execute as migrações e inicie a API:

```bash
cd backend
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A documentação interativa da API fica em
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). O estado de
simulação é mantido em memória e reinicia quando o processo da API é reiniciado.

Opcionalmente, carregue os dados básicos de desenvolvimento após aplicar as
migrações:

```bash
python -m app.infrastructure.database.seed.development
```

### 3. Executar o dashboard

Em outro terminal:

```bash
cd frontend
npm ci
npm run dev
```

Acesse [http://localhost:3000](http://localhost:3000). A interface é
demonstrativa e não depende da API para exibir seus dados atuais.

## API disponível

Com o backend em execução, os endpoints atuais são:

| Método | Caminho | Descrição |
|---|---|---|
| `GET` | `/` | Nome, versão e estado do serviço |
| `GET` | `/health` | Verificação simples de saúde da API |
| `GET` | `/api/environment` | Ambiente demonstrativo com regiões, sensores e agente |
| `POST` | `/api/telemetry` | Valida e persiste uma leitura ambiental |
| `GET` | `/api/telemetry/latest?limit=50` | Lista leituras recentes; limite entre 1 e 100 |
| `GET` | `/api/telemetry/sensor/{sensor_id}` | Retorna a leitura mais recente de um sensor |
| `GET` | `/api/events` | Lista eventos ambientais ativos |
| `GET` | `/api/events/region/{region_id}` | Lista eventos de uma região |
| `GET` | `/api/simulation/status` | Consulta o estado atual da simulação |
| `POST` | `/api/simulation/start` | Inicia o estado de simulação para um cenário |
| `POST` | `/api/simulation/stop` | Interrompe a simulação em memória |

Exemplo de envio de telemetria:

```bash
curl -X POST http://127.0.0.1:8000/api/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "SENSOR-001",
    "region_id": "REGION-001",
    "timestamp": "2026-10-27T13:00:00Z",
    "temperature": 28.5,
    "humidity": 60,
    "soil_moisture": 55,
    "light": 500
  }'
```

Os campos `humidity` e `soil_moisture` aceitam valores de 0 a 100; `light`
precisa ser não negativo. O sensor e a região informados precisam existir no
banco devido às referências relacionais.

Exemplo de início de simulação:

```bash
curl -X POST http://127.0.0.1:8000/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"scenario": "heatwave"}'
```

Os cenários aceitos pela API são `heatwave`, `drought`, `wildfire`, `flood` e
`earthquake`. Atualmente, iniciar uma simulação apenas altera seu estado em
memória; não executa uma simulação ambiental nem altera telemetria ou eventos.

## Testes

Com o ambiente Python do backend ativado:

```bash
cd backend
pytest
```

Os testes que usam o banco precisam de uma instância PostgreSQL/TimescaleDB
acessível pela variável `DATABASE_URL`, com as migrações aplicadas. O teste
manual de estilo e build do frontend pode ser executado com:

```bash
cd frontend
npm run lint
npm run build
```

## Limitações conhecidas

- Os indicadores, o mapa, o gráfico e os alertas do dashboard são dados
  estáticos de demonstração.
- O dashboard não consulta nem envia dados para o backend.
- A simulação da interface altera apenas o estado visual local; a simulação da
  API, por sua vez, é apenas um estado em memória. As duas não são conectadas.
- O endpoint `/api/environment` retorna um ambiente definido no código, não
  dados carregados do banco.
- O endpoint de telemetria persiste observações, mas ainda não as encaminha
  automaticamente para detecção de anomalias, criação de eventos ou resposta.
- Não há autenticação, autorização de usuários da aplicação ou implantação de
  produção configuradas.
- O manifesto de dependências Python precisa ser completado para que a
  instalação do backend seja reproduzível somente a partir dos arquivos de
  dependências.

## Evolução planejada

Estas etapas descrevem possibilidades para o produto; não estão incluídas no
MVP atual.

### 1. Conectar o dashboard à API

- substituir dados demonstrativos por dados obtidos da API;
- apresentar estados de carregamento, erro e ausência de dados;
- atualizar indicadores e alertas de acordo com região e intervalo;
- documentar a configuração da URL da API por ambiente.

### 2. Fechar o ciclo da telemetria

- completar e fixar as dependências do backend;
- padronizar unidades, timestamps, identificação de sensores e validação;
- ligar a ingestão persistida a snapshots, detecção de anomalias e geração de
  eventos;
- expor no dashboard a origem, o horário e a confiança dos dados.

### 3. Transformar simulação em ferramenta de análise

- avançar do estado de início/parada para cenários que geram observações
  ambientais simuladas;
- modelar a evolução de riscos, regiões e agentes ao longo do tempo;
- comparar resultados de cenários e persistir execuções para consulta posterior.

### 4. Operacionalizar respostas com segurança

- ligar eventos à avaliação de risco, ao planejamento de missões e à atribuição
  de agentes;
- registrar evidências, decisões, aprovações humanas e resultados;
- manter limites e políticas de segurança antes de qualquer ação no mundo
  físico.

### 5. Integrar fontes e implantação

- adicionar ingestão por MQTT e adaptadores de hardware quando houver
  dispositivos disponíveis;
- incorporar mapas geográficos e séries temporais reais;
- adicionar autenticação, autorização, observabilidade, backups e implantação
  com configurações específicas por ambiente.

## Estrutura do repositório

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # Rotas e schemas HTTP
│   │   ├── core/            # Configuração
│   │   ├── domain/          # Entidades e contratos de domínio
│   │   ├── infrastructure/  # Banco, repositórios e seed
│   │   └── services/        # Análise, eventos, risco, missões e simulação
│   ├── migrations/          # Migrações Alembic
│   └── tests/               # Testes unitários e de integração
├── docs/
│   └── TECHNICAL_BLUEPRINT.md
├── frontend/
│   └── app/                 # Dashboard Next.js
└── infra/
    └── docker-compose.yml   # PostgreSQL/TimescaleDB local
```

## Princípios do projeto

1. Construir e validar o núcleo de inteligência antes de depender de hardware.
2. Manter sensores e dispositivos físicos opcionais durante o desenvolvimento.
3. Usar simulação para testar hipóteses e arquitetura antes de qualquer
   intervenção real.
4. Tratar segurança, evidência e revisão humana como partes do fluxo de
   resposta.
5. Priorizar impacto ambiental positivo e transparência sobre a origem dos
   dados.
