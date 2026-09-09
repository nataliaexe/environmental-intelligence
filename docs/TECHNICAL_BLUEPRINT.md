# Earth Forward — Technical Blueprint

## 1. Identidade do Projeto

### Nome provisorio
TrioRestore

### Tema
Earth Forward — Restauracao planetaria autonoma

### Visao
Uma plataforma integrada de restauracao ambiental que trata solo, agua e ar com tres frentes de acao autonoma: enxame de micro-robos terrestres, folhas artificiais aquaticas e floresta sintetica aerea.

### Proposta de valor
Nao e apenas monitoramento. E restauracao ativa.

---

## 2. Os Tres Modulos

| Modulo | Frente | Problema real | Acao |
|---|---|---|---|
| TerraFormers | Solo | 35% do solo agricola mundial degradado | Enxame de micro-robos restaura solo com plantio, inoculacao e aeracao |
| AquaLeaves | Agua | Acidificacao e eutrofizacao de rios e lagos | Folhas artificiais flutuantes capturam CO2 da agua e liberam oxigenio |
| SynthForest | Ar | Excesso de CO2 e ilhas de calor urbanas | Arvores mecanicas capturam CO2, geram energia e resfriam microclima |

---

## 3. Estado da Arte (Base Cientifica)

### TerraFormers — Robos de Restauracao

Pesquisas atuais comprovam a viabilidade de robos agricolas leves e modulares:

- SwarmFarm Robotics (Australia): robos autonomos leves que reduzem compactacao do solo
- Texas A&M: enxames de robos terrestres melhoram cobertura de intervencao no campo
- Robos de restauracao podem semear, aerar e inocular microrganismos especificos

**Desafio:** micro-robos em terrenos irregulares com atuadores e coordenacao de enxame.

### AquaLeaves — Fotosintese Artificial

Tecnologias similares existem em laboratorio:

- Universidade de Cambridge: "folhas artificiais" flutuantes que dividem agua em H2 e O2 e reduzem CO2
- Fotobiorreatores com microalgas absorvem CO2 e liberam O2
- Sistemas flutuantes de cultivo de algas podem reoxigenar agua poluida

**Desafio:** prototipagem e testes em campo com biorreatores flutuantes.

### SynthForest — Arvores Sinteticas

Conceitos reais comprovam a captura artificial de carbono:

- Klaus Lackner (ASU): "arvores mecanicas" capturam CO2 1000x mais rapido que arvores naturais
- CityTree/MossTree: estruturas com musgo filtram particulas e resfriam microclimas
- Painels solares integrados para energia e sombreamento

**Desafio:** prototipos hibridos que combinam captura de CO2 com geracao de energia.

### Conclusao da Pesquisa

As tres frentes tem respaldo em pesquisas atuais. O que NAO existe e a integracao das tres em uma plataforma unica com pipeline de dados compartilhado.

---

## 4. Arquitetura Geral
RESTORE CORE (Backend)
|
+----------+-----------+-----------+
| | | |
TerraFormers AquaLeaves SynthForest
| | |
+----------+-----------+-----------+
|
SIMULADOR / HARDWARE
|
DASHBOARD UNIFICADA
text


### Camada 1: Core (Backend)

Pipeline de inteligencia ambiental:

Sensor Data -> Fusion -> Anomaly Detection -> Event Engine -> Risk Engine -> Mission Planner -> Safety -> Actuator -> Verification
text


### Camada 2: Modulos (Domain)

Cada modulo e um perfil de capacidades e acoes sobre o mesmo pipeline.

### Camada 3: Interface

- Simulador (visual) ou Hardware (fisico)
- Dashboard (metricas e visualizacao)

---

## 5. Tecnologias

### Backend

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| FastAPI | API REST |
| Pydantic | Validacao de dados |
| SQLAlchemy | ORM |
| PostgreSQL | Persistencia relacional |
| TimescaleDB | Series temporais |
| MQTT (futuro) | Comunicacao com hardware |

### Simulacao

| Tecnologia | Uso |
|---|---|
| Python | Motor de simulacao |
| Three.js | Visualizacao 3D |
| Plotly | Graficos |

### Hardware (fase futura)

| Tecnologia | Uso |
|---|---|
| ESP32 | Unidade de processamento |
| Sensores | Umidade, pH, CO2, temperatura |
| Atuadores | Bracos, bombas, valvulas |

---

## 6. Estrutura de Pastas

trio-restore/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── routes/
│ │ │ │ ├── terraformers.py
│ │ │ │ ├── aqua_leaves.py
│ │ │ │ ├── synth_forest.py
│ │ │ │ └── dashboard.py
│ │ │ └── schemas/
│ │ │ ├── terraformers.py
│ │ │ ├── aqua_leaves.py
│ │ │ └── synth_forest.py
│ │ ├── domain/
│ │ │ ├── terraformers.py
│ │ │ ├── aqua_leaves.py
│ │ │ └── synth_forest.py
│ │ ├── services/
│ │ │ ├── terraformers/
│ │ │ │ ├── detection.py
│ │ │ │ ├── restoration.py
│ │ │ │ └── verification.py
│ │ │ ├── aqua_leaves/
│ │ │ │ ├── detection.py
│ │ │ │ ├── oxygenation.py
│ │ │ │ └── verification.py
│ │ │ └── synth_forest/
│ │ │ ├── detection.py
│ │ │ ├── capture.py
│ │ │ └── verification.py
│ │ └── infrastructure/
│ │ └── database/
│ │ └── models/
│ │ ├── terraformers.py
│ │ ├── aqua_leaves.py
│ │ └── synth_forest.py
│ └── tests/
│ ├── test_terraformers.py
│ ├── test_aqua_leaves.py
│ └── test_synth_forest.py
├── simulator/
│ ├── world.py
│ ├── terraformers/
│ ├── aqua_leaves/
│ └── synth_forest/
├── frontend/
│ ├── app/
│ └── public/
└── docs/
└── TECHNICAL_BLUEPRINT.md
text


---

## 7. Modelos de Dados

### TerraFormers (Solo)

TerraFormerReading:
id: str
region_id: str
soil_moisture: float (0-100)
soil_ph: float
organic_matter: float (0-100)
compaction: float (0-100)
biodiversity_index: float (0-1)
timestamp: datetime
source_type: str (sensor | simulator)
source_id: str
text


### AquaLeaves (Agua)

AquaLeafReading:
id: str
region_id: str
co2_dissolved: float (ppm)
oxygen_dissolved: float (mg/L)
ph: float
temperature: float
timestamp: datetime
source_type: str
source_id: str
text


### SynthForest (Ar)

SynthForestReading:
id: str
region_id: str
co2_ppm: float
oxygen_ppm: float
solar_energy: float (watts)
temperature: float
timestamp: datetime
source_type: str
source_id: str
text


---

## 8. Pipeline de Inteligencia (reaproveitado)

O backend atual ja tem um pipeline generico:

Sensor Data
-> Feature Extraction
-> Rule Detection
-> Statistical Anomaly Detection
-> Fusion
-> Anomaly Assessment
-> Event Engine
-> Risk Engine
-> Mission Planner
-> Safety Engine
-> Actuator Command
-> Verification
text


### Adaptacao para cada modulo

| Etapa | TerraFormers | AquaLeaves | SynthForest |
|---|---|---|---|
| Feature | umidade, pH, compactacao | CO2 dissolvido, O2, pH | CO2, O2, temp |
| Rule | umidade < 20 = anom | O2 < 5 = anom | CO2 > 800 = anom |
| Event | solo_degradado | agua_acidificada | co2_elevado |
| Risk | risco_perda_safra | risco_colapso_aquatico | risco_termico |
| Mission | restaurar_solo | oxigenar_agua | capturar_co2 |
| Action | plantar + inocular + aerar | ativar_fotossintese | ativar_captura |
| Verify | vegetacao_cresceu | O2 > 7 | CO2 < 600 |

---

## 9. API Endpoints

### TerraFormers

POST /api/v1/terraformers/readings Enviar leitura
GET /api/v1/terraformers/readings/latest Ultimas leituras
POST /api/v1/terraformers/detect Detectar degradacao
POST /api/v1/terraformers/restore Iniciar restauracao
GET /api/v1/terraformers/status Status do modulo
text


### AquaLeaves

POST /api/v1/aqua-leaves/readings Enviar leitura
GET /api/v1/aqua-leaves/readings/latest Ultimas leituras
POST /api/v1/aqua-leaves/detect Detectar acidificacao
POST /api/v1/aqua-leaves/oxygenate Iniciar oxigenacao
GET /api/v1/aqua-leaves/status Status do modulo
text


### SynthForest

POST /api/v1/synth-forest/readings Enviar leitura
GET /api/v1/synth-forest/readings/latest Ultimas leituras
POST /api/v1/synth-forest/detect Detectar CO2 elevado
POST /api/v1/synth-forest/capture Iniciar captura
GET /api/v1/synth-forest/status Status do modulo
text


### Dashboard

GET /api/v1/dashboard/overview Visao geral
GET /api/v1/dashboard/metrics Metricas agregadas
GET /api/v1/dashboard/timeline Linha do tempo
text


---

## 10. Como Funciona o Fluxo Completo

### Cenario 1: Solo Degradado (TerraFormers)

1. Enxame mede umidade = 12% e compactacao = 80% (anomalia)
2. Backend detecta solo degradado
3. Event Engine gera evento: "solo_degradado"
4. Risk Engine avalia: risco ALTO
5. Mission Planner cria missao: "restaurar_solo"
6. Swarm Coordinator distribui robos
7. Robos plantam sementes, inoculam micro-organismos, aeram solo
8. Sensores medem umidade = 45% e compactacao = 30%
9. Verification confirma: solo em recuperacao
10. Dashboard mostra timeline de restauracao

### Cenario 2: Agua Acidificada (AquaLeaves)

1. Folhas artificiais medem O2 = 3 mg/L e pH = 5.5 (anomalia)
2. Backend detecta acidificacao
3. Event Engine gera evento: "agua_acidificada"
4. Risk Engine avalia: risco ALTO
5. Mission Planner cria missao: "oxigenar_agua"
6. Atuador ativa fotossintese artificial
7. Folhas capturam CO2 dissolvido e liberam O2
8. Sensores medem O2 = 8 mg/L e pH = 6.8
9. Verification confirma: agua saudavel
10. Dashboard mostra melhora da qualidade

### Cenario 3: CO2 Elevado (SynthForest)

1. Arvores mecanicas medem CO2 = 950 ppm (anomalia)
2. Backend detecta CO2 alto
3. Event Engine gera evento: "co2_elevado"
4. Risk Engine avalia: risco ALTO
5. Mission Planner cria missao: "capturar_co2"
6. Atuador ativa captura fotossintetica
7. Arvores capturam CO2 e geram energia
8. Sensores medem CO2 = 580 ppm
9. Verification confirma: ar limpo
10. Dashboard mostra reducao de CO2

---

## 11. Plano de Implementacao (hoje)

### Fase 1: Domain Models (TerraFormers primeiro)

Criar as classes de dominio. Comecar pelo TerraFormers como modulo piloto.

### Fase 2: Database Models

Criar models SQLAlchemy para persistencia.

### Fase 3: Repositories

Criar repositories para acesso ao banco.

### Fase 4: Services

Criar services de deteccao, missao e acao.

### Fase 5: API Routes

Expor endpoints REST.

### Fase 6: Tests

Testes unitarios e de integracao.

### Fase 7: Migration

Aplicar migration no PostgreSQL/TimescaleDB.

### Fase 8: Expansao

Replicar para AquaLeaves e SynthForest.

---

## 12. Metricas de Sucesso

| Metrica | TerraFormers | AquaLeaves | SynthForest |
|---|---|---|---|
| Deteccao | < 30s | < 10s | < 10s |
| Acao | < 5min | < 30s | < 30s |
| Verificacao | < 1h | < 60s | < 60s |
| Precisao | > 85% | > 90% | > 90% |

---

## 13. Criterios de Avaliacao do Hackathon

| Criterio | Como atender |
|---|---|
| Inovacao | Tres frentes de restauracao autonoma em uma plataforma |
| Impacto | Solo, agua e ar tratados simultaneamente |
| Viabilidade | Hardware barato, software open source |
| Demonstracao | Simulacao visual + metricas em tempo real |
| Escalabilidade | Arquitetura modular, protocolos padronizados |

---

## 14. Riscos e Mitigacoes

| Risco | Mitigacao |
|---|---|
| Falta de tempo | Focar em software, hardware como bonus |
| Complexidade | Modularizar ao maximo, testar cada modulo isolado |
| Integracao | APIs padronizadas desde o inicio |
| Apresentacao | Simulacao visual forte + dashboard clara |
| Falsos positivos | Calibracao com especialistas ambientais |
| Dano ecologico | Acoes reversiveis, validacao humana para intervencao |

---

## 15. Proximos Passos (hoje)

1. Criar models de dominio (TerraFormers primeiro)
2. Criar models de banco
3. Criar repositories
4. Criar services
5. Criar rotas API
6. Criar testes
7. Aplicar migration
8. Rodar testes
9. Validar fluxo completo
10. Expandir para AquaLeaves e SynthForest

---

## 16. Regras do Projeto

1. Sem emojis no codigo
2. Python 3.10+ com type hints
3. Testes para cada modulo
4. Migration para cada mudanca de schema
5. Nenhum bypass de autorizacao
6. World Model como source of truth
7. Simulador e projecao, nao verdade
8. Compilar e testar apos cada bloco
9. Especialistas ambientais no loop de validacao
10. Acoes reversiveis e auditaveis

---

Fim do documento.
