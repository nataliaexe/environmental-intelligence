"use client";

import { useState } from "react";
import type { CSSProperties } from "react";

type IconName =
  | "grid"
  | "map"
  | "activity"
  | "radio"
  | "settings"
  | "search"
  | "bell"
  | "arrow"
  | "droplet"
  | "thermometer"
  | "leaf"
  | "sun"
  | "play"
  | "pause"
  | "check"
  | "wind";

type Region = {
  id: string;
  name: string;
  shortName: string;
  health: number;
  status: "Estável" | "Atenção" | "Crítico";
  temperature: number;
  humidity: number;
  soil: number;
  sensors: number;
  x: number;
  y: number;
};

const regions: Region[] = [
  {
    id: "north",
    name: "Setor Norte",
    shortName: "Norte",
    health: 92,
    status: "Estável",
    temperature: 24.8,
    humidity: 68,
    soil: 54,
    sensors: 8,
    x: 63,
    y: 29,
  },
  {
    id: "reserve",
    name: "Reserva Central",
    shortName: "Reserva",
    health: 76,
    status: "Atenção",
    temperature: 29.4,
    humidity: 51,
    soil: 36,
    sensors: 12,
    x: 44,
    y: 54,
  },
  {
    id: "south",
    name: "Setor Sul",
    shortName: "Sul",
    health: 88,
    status: "Estável",
    temperature: 26.1,
    humidity: 63,
    soil: 48,
    sensors: 6,
    x: 27,
    y: 76,
  },
];

const alerts = [
  {
    id: 1,
    level: "high",
    label: "Risco de seca",
    region: "Reserva Central",
    detail: "Umidade do solo abaixo do limite recomendado",
    time: "há 12 min",
    icon: "sun" as const,
  },
  {
    id: 2,
    level: "medium",
    label: "Temperatura elevada",
    region: "Reserva Central",
    detail: "Temperatura 4,2 °C acima da média local",
    time: "há 38 min",
    icon: "thermometer" as const,
  },
  {
    id: 3,
    level: "low",
    label: "Sensor reconectado",
    region: "Setor Norte",
    detail: "Nó ambiental voltou a transmitir dados",
    time: "há 1 h",
    icon: "radio" as const,
  },
];

const chartValues = [
  41, 46, 44, 49, 45, 54, 51, 57, 53, 61, 58, 64, 59, 67, 63, 72, 68, 75, 70,
  77, 73, 81, 76, 84,
];

const scenarios = [
  { value: "heatwave", label: "Onda de calor", icon: "sun" as const },
  { value: "drought", label: "Seca", icon: "leaf" as const },
  { value: "wildfire", label: "Incêndio florestal", icon: "wind" as const },
];

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.7,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true as const,
  };

  const shapes = {
    grid: <><rect x="3.5" y="3.5" width="7" height="7" rx="1.5" /><rect x="13.5" y="3.5" width="7" height="7" rx="1.5" /><rect x="3.5" y="13.5" width="7" height="7" rx="1.5" /><rect x="13.5" y="13.5" width="7" height="7" rx="1.5" /></>,
    map: <><path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z" /><path d="M9 3v15M15 6v15" /></>,
    activity: <><path d="M3 12h4l3-8 4 16 3-8h4" /></>,
    radio: <><path d="M5 9.5a10 10 0 0 1 14 0M8 12.5a5.8 5.8 0 0 1 8 0M11 15.5a1.7 1.7 0 0 1 2 0" /><circle cx="12" cy="19" r="1" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="m19.4 15 .1.1 1.4 1.1-1.4 2.4-1.7-.7a8 8 0 0 1-1.7 1l-.3 1.8h-2.8l-.3-1.8a8 8 0 0 1-1.7-1l-1.7.7-1.4-2.4L7.9 15a7 7 0 0 1 0-2l-.1-.1-1.4-1.1 1.4-2.4 1.7.7a8 8 0 0 1 1.7-1l.3-1.8h2.8l.3 1.8a8 8 0 0 1 1.7 1l1.7-.7 1.4 2.4-1.4 1.1a7 7 0 0 1-.6 2Z" /></>,
    search: <><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4.5 4.5" /></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 21h4" /></>,
    arrow: <><path d="M5 12h14M13 6l6 6-6 6" /></>,
    droplet: <><path d="M12 3.5S5.5 11 5.5 15a6.5 6.5 0 0 0 13 0c0-4-6.5-11.5-6.5-11.5Z" /><path d="M9 15.5a3 3 0 0 0 3 3" /></>,
    thermometer: <><path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4.5 4.5 0 1 0 4 0Z" /><path d="M12 12v6" /></>,
    leaf: <><path d="M20.5 3.5C11 3.5 4 6 4 13a5 5 0 0 0 5 5c7 0 9.5-7 11.5-14.5Z" /><path d="M3.5 21c3-6 7-9 12-11" /></>,
    sun: <><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" /></>,
    play: <><path d="m8 5 11 7-11 7V5Z" /></>,
    pause: <><path d="M9 5v14m6-14v14" /></>,
    check: <><path d="m5 12 4 4L19 6" /></>,
    wind: <><path d="M3 8h12a3 3 0 1 0-3-3M2 12h17a3 3 0 1 1-3 3M4 16h6a2 2 0 1 1-2 2" /></>,
  };

  return <svg {...common}>{shapes[name]}</svg>;
}

function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <Icon name="leaf" size={21} />
    </span>
  );
}

function Sparkline({ color, variant = 0 }: { color: string; variant?: number }) {
  const patterns = [
    "0,27 14,24 26,27 39,15 52,19 65,10 78,14 91,5 104,9",
    "0,22 14,18 26,21 39,10 52,16 65,8 78,13 91,4 104,8",
    "0,8 14,13 26,9 39,18 52,12 65,21 78,15 91,23 104,18",
    "0,20 14,16 26,20 39,13 52,18 65,8 78,14 91,6 104,10",
  ];
  return (
    <svg className="sparkline" viewBox="0 0 104 30" aria-hidden="true">
      <polyline
        points={patterns[variant]}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function HealthChart() {
  const points = chartValues
    .map((value, index) => `${(index / (chartValues.length - 1)) * 720},${138 - value * 1.1}`)
    .join(" ");
  return (
    <svg
      className="health-chart"
      viewBox="0 0 720 160"
      role="img"
      aria-label="Gráfico de estabilidade ambiental nas últimas 24 horas"
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="#468568" stopOpacity=".2" />
          <stop offset="100%" stopColor="#468568" stopOpacity="0" />
        </linearGradient>
      </defs>
      {[30, 65, 100, 135].map((y) => (
        <line key={y} x1="0" x2="720" y1={y} y2={y} className="chart-gridline" />
      ))}
      <polygon points={`0,160 ${points} 720,160`} fill="url(#chartFill)" />
      <polyline
        points={points}
        fill="none"
        stroke="#438667"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
}

function EcosystemMap({
  selected,
  onSelect,
}: {
  selected: string;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="map-canvas" aria-label="Mapa esquemático das regiões monitoradas">
      <div className="map-grid" />
      <svg className="map-river" viewBox="0 0 600 360" preserveAspectRatio="none" aria-hidden="true">
        <path d="M387 -20 C290 40 410 75 330 122 S395 188 284 224 S321 301 214 380" />
        <path className="river-core" d="M387 -20 C290 40 410 75 330 122 S395 188 284 224 S321 301 214 380" />
      </svg>
      <div className="map-label map-label-north">CORREDOR NORTE</div>
      <div className="map-label map-label-reserve">RESERVA CENTRAL</div>
      <div className="map-label map-label-south">ZONA SUL</div>
      {regions.map((region) => (
        <button
          key={region.id}
          type="button"
          className={`map-node ${region.status === "Atenção" ? "map-node-warn" : ""} ${selected === region.id ? "map-node-selected" : ""}`}
          style={{ left: `${region.x}%`, top: `${region.y}%` }}
          onClick={() => onSelect(region.id)}
          aria-label={`Selecionar ${region.name}, saúde ${region.health}%`}
          aria-pressed={selected === region.id}
        >
          <span className="map-node-pulse" />
          <span className="map-node-dot" />
          <span className="map-tooltip">
            <strong>{region.shortName}</strong>
            <span>Saúde {region.health}%</span>
          </span>
        </button>
      ))}
      <span className="map-scale"><span /> 2 km</span>
      <span className="map-compass">N <span>↑</span></span>
    </div>
  );
}

export default function Home() {
  const [selectedRegion, setSelectedRegion] = useState("reserve");
  const [timeRange, setTimeRange] = useState("24 horas");
  const [scenario, setScenario] = useState("heatwave");
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [acknowledged, setAcknowledged] = useState<number[]>([]);
  const [activeNav, setActiveNav] = useState("Visão geral");

  const currentRegion = regions.find((region) => region.id === selectedRegion) ?? regions[1];
  const openAlerts = alerts.filter((alert) => !acknowledged.includes(alert.id));
  const activeScenario = scenarios.find((item) => item.value === scenario) ?? scenarios[0];
  const statusClass = currentRegion.status === "Estável" ? "stable" : currentRegion.status === "Atenção" ? "attention" : "critical";

  function acknowledgeAlert(id: number) {
    setAcknowledged((current) => [...current, id]);
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#overview" onClick={() => setActiveNav("Visão geral")}>
          <BrandMark />
          <span className="brand-name">cortex<span>.</span></span>
        </a>

        <div className="workspace-switcher">
          <span className="workspace-avatar">F</span>
          <span className="workspace-copy"><strong>Floresta Atlântica</strong><small>Workspace de pesquisa</small></span>
          <span className="switcher-chevron">⌄</span>
        </div>

        <p className="nav-caption">MONITORAMENTO</p>
        <nav className="primary-nav" aria-label="Navegação principal">
          {[
            { label: "Visão geral", icon: "grid" as const, href: "#overview" },
            { label: "Mapa ambiental", icon: "map" as const, href: "#mapa" },
            { label: "Alertas", icon: "activity" as const, href: "#alertas", count: openAlerts.length },
            { label: "Sensores", icon: "radio" as const, href: "#sensores" },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className={`nav-item ${activeNav === item.label ? "nav-item-active" : ""}`}
              onClick={() => setActiveNav(item.label)}
            >
              <Icon name={item.icon} size={18} />
              <span>{item.label}</span>
              {"count" in item && item.count !== undefined && item.count > 0 && <span className="nav-count">{item.count}</span>}
            </a>
          ))}
        </nav>

        <p className="nav-caption tools-caption">FERRAMENTAS</p>
        <nav className="primary-nav" aria-label="Ferramentas">
          <a
            href="#simulacao"
            className={`nav-item ${activeNav === "Simulações" ? "nav-item-active" : ""}`}
            onClick={() => setActiveNav("Simulações")}
          >
            <Icon name="activity" size={18} />
            <span>Simulações</span>
          </a>
          <a
            href="#configuracoes"
            className={`nav-item ${activeNav === "Configurações" ? "nav-item-active" : ""}`}
            onClick={() => setActiveNav("Configurações")}
          >
            <Icon name="settings" size={18} />
            <span>Configurações</span>
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="system-card">
            <span className="system-indicator" />
            <span><strong>Sistema operacional</strong><small>Última sincronização há 2 min</small></span>
            <Icon name="arrow" size={15} />
          </div>
          <button className="profile-button" type="button">
            <span className="profile-avatar">MC</span>
            <span className="profile-copy"><strong>Marina Costa</strong><small>Pesquisadora</small></span>
            <span className="switcher-chevron">···</span>
          </button>
        </div>
      </aside>

      <div className="main-column" id="overview">
        <header className="topbar">
          <div className="breadcrumbs"><span>Workspace</span><span className="breadcrumb-divider">/</span><strong>Visão geral</strong></div>
          <div className="topbar-actions">
            <span className="demo-pill"><span /> AMBIENTE DEMONSTRATIVO</span>
            <button type="button" className="icon-button search-button" aria-label="Buscar"><Icon name="search" /></button>
            <button type="button" className="icon-button notification-button" aria-label={`${openAlerts.length} alertas não reconhecidos`}><Icon name="bell" /><span /></button>
            <span className="topbar-divider" />
            <span className="today-label">Terça-feira, 27 de outubro</span>
          </div>
        </header>

        <div className="page-content">
          <section className="welcome-row">
            <div>
              <p className="eyebrow"><span className="eyebrow-line" /> TERÇA-FEIRA, 27 OUTUBRO 2026</p>
              <h1>Bom dia, Marina <span className="wave">✳</span></h1>
              <p className="welcome-subtitle">Acompanhe a saúde do seu ecossistema em tempo real.</p>
            </div>
            <a className="export-button" href="#mapa"><Icon name="map" size={16} /> Explorar mapa <Icon name="arrow" size={15} /></a>
          </section>

          <section className="metrics-grid" aria-label="Indicadores ambientais">
            <article className="metric-card">
              <div className="metric-top"><span className="metric-icon green"><Icon name="leaf" /></span><span className="metric-change positive">↑ 2,4%</span></div>
              <p className="metric-label">Saúde do ecossistema</p>
              <div className="metric-reading"><strong>84</strong><span>/ 100</span></div>
              <div className="metric-foot"><span>vs. semana passada</span><Sparkline color="#4d9b78" variant={0} /></div>
            </article>
            <article className="metric-card">
              <div className="metric-top"><span className="metric-icon amber"><Icon name="activity" /></span><span className="metric-change warning-change">+ 1 novo</span></div>
              <p className="metric-label">Alertas ativos</p>
              <div className="metric-reading"><strong>{openAlerts.length.toString().padStart(2, "0")}</strong><span> eventos</span></div>
              <div className="metric-foot"><span>{openAlerts.filter((alert) => alert.level === "high").length} prioridade alta</span><Sparkline color="#d49a46" variant={1} /></div>
            </article>
            <article className="metric-card">
              <div className="metric-top"><span className="metric-icon blue"><Icon name="radio" /></span><span className="metric-change positive">● Operacionais</span></div>
              <p className="metric-label">Sensores conectados</p>
              <div className="metric-reading"><strong>26</strong><span>/ 28</span></div>
              <div className="metric-foot"><span>92,8% de disponibilidade</span><Sparkline color="#5792b4" variant={2} /></div>
            </article>
            <article className="metric-card">
              <div className="metric-top"><span className="metric-icon violet"><Icon name="wind" /></span><span className="metric-change neutral-change">em 3 regiões</span></div>
              <p className="metric-label">Temperatura média</p>
              <div className="metric-reading"><strong>26,8</strong><span>°C</span></div>
              <div className="metric-foot"><span>Dentro da faixa esperada</span><Sparkline color="#9281ba" variant={3} /></div>
            </article>
          </section>

          <section className="overview-grid">
            <article className="panel map-panel" id="mapa">
              <div className="panel-heading">
                <div><p className="section-kicker">DISTRIBUIÇÃO ESPACIAL</p><h2>Mapa ambiental</h2></div>
                <button className="subtle-select" type="button" aria-label="Período do mapa">Últimas 24h <span>⌄</span></button>
              </div>
              <EcosystemMap selected={selectedRegion} onSelect={setSelectedRegion} />
              <div className="map-footer">
                <span className="map-legend"><i className="legend-dot green-dot" /> Estável <i className="legend-dot amber-dot" /> Atenção <i className="legend-dot red-dot" /> Crítico</span>
                <span className="map-live"><span /> Atualizado agora</span>
              </div>
            </article>

            <article className="panel region-panel">
              <div className="panel-heading">
                <div><p className="section-kicker">RESUMO DA REGIÃO</p><h2>{currentRegion.name}</h2></div>
                <span className={`status-pill ${statusClass}`}><i /> {currentRegion.status}</span>
              </div>
              <div className="health-score">
                <div className="score-ring" style={{ "--score": `${currentRegion.health * 3.6}deg` } as CSSProperties}>
                  <div><strong>{currentRegion.health}</strong><span>saúde</span></div>
                </div>
                <div className="health-copy"><strong>Ecossistema saudável</strong><span>Indicadores dentro dos parâmetros de segurança.</span><span className="health-trend">↗ +3 pts <small>nesta semana</small></span></div>
              </div>
              <div className="region-readings">
                <div className="reading-item"><span className="reading-icon temp"><Icon name="thermometer" size={16} /></span><span className="reading-copy"><small>Temperatura</small><strong>{currentRegion.temperature.toFixed(1).replace(".", ",")}<em>°C</em></strong></span><span className="reading-trend">↗</span></div>
                <div className="reading-item"><span className="reading-icon humidity"><Icon name="droplet" size={16} /></span><span className="reading-copy"><small>Umidade do ar</small><strong>{currentRegion.humidity}<em>%</em></strong></span><span className="reading-trend down">↘</span></div>
                <div className="reading-item"><span className="reading-icon soil"><Icon name="leaf" size={16} /></span><span className="reading-copy"><small>Umidade do solo</small><strong>{currentRegion.soil}<em>%</em></strong></span><span className={`reading-trend ${currentRegion.soil < 40 ? "down" : ""}`}>↗</span></div>
              </div>
              <div className="region-meta"><span><Icon name="radio" size={14} /> {currentRegion.sensors} sensores ativos</span><span>Dados há 2 min</span></div>
            </article>
          </section>

          <section className="lower-grid">
            <article className="panel chart-panel" id="sensores">
              <div className="panel-heading chart-heading">
                <div><p className="section-kicker">TENDÊNCIA DOS INDICADORES</p><h2>Estabilidade ambiental</h2></div>
                <div className="range-toggle" role="group" aria-label="Intervalo do gráfico">
                  {["24 horas", "7 dias"].map((range) => (
                    <button key={range} type="button" className={timeRange === range ? "range-active" : ""} onClick={() => setTimeRange(range)}>{range}</button>
                  ))}
                </div>
              </div>
              <div className="chart-summary"><strong>82,4 <span>pts</span></strong><span className="chart-up">↗ 4,8% <small>vs. período anterior</small></span></div>
              <div className="chart-area"><div className="chart-y-labels"><span>100</span><span>75</span><span>50</span><span>25</span></div><HealthChart /></div>
              <div className="chart-x-labels">{(timeRange === "24 horas" ? ["00h", "04h", "08h", "12h", "16h", "20h", "Agora"] : ["Qua", "Qui", "Sex", "Sáb", "Dom", "Seg", "Ter"]).map((label) => <span key={label}>{label}</span>)}</div>
            </article>

            <article className="panel alerts-panel" id="alertas">
              <div className="panel-heading">
                <div><p className="section-kicker">ACOMPANHAMENTO</p><h2>Alertas recentes <span className="heading-count">{openAlerts.length}</span></h2></div>
                <a className="text-link" href="#alertas">Ver todos <Icon name="arrow" size={14} /></a>
              </div>
              <div className="alerts-list">
                {openAlerts.length === 0 ? (
                  <div className="empty-alerts"><span className="empty-check"><Icon name="check" size={17} /></span><strong>Tudo em dia</strong><span>Todos os alertas foram reconhecidos.</span></div>
                ) : openAlerts.map((alert) => (
                  <div className="alert-item" key={alert.id}>
                    <span className={`alert-icon alert-${alert.level}`}><Icon name={alert.icon} size={16} /></span>
                    <div className="alert-copy"><div><strong>{alert.label}</strong><time>{alert.time}</time></div><span>{alert.region}</span><small>{alert.detail}</small></div>
                    <button className="ack-button" type="button" onClick={() => acknowledgeAlert(alert.id)} aria-label={`Reconhecer alerta: ${alert.label}`}><Icon name="check" size={15} /></button>
                  </div>
                ))}
              </div>
            </article>
          </section>

          <section className="simulation-banner" id="simulacao">
            <div className="simulation-mark"><Icon name="activity" size={20} /></div>
            <div className="simulation-copy"><span>LABORATÓRIO DE CENÁRIOS</span><strong>{simulationRunning ? `Simulação em andamento: ${activeScenario.label}` : "Prepare-se para o inesperado"}</strong><small>{simulationRunning ? "Cenário demonstrativo ativo. Nenhum dado real está sendo alterado." : "Explore como o ecossistema pode reagir a eventos ambientais."}</small></div>
            <div className="simulation-controls">
              <label className="scenario-picker"><span className="sr-only">Cenário ambiental</span><select value={scenario} onChange={(event) => setScenario(event.target.value)}>{scenarios.map((item) => <option value={item.value} key={item.value}>{item.label}</option>)}</select><span className="select-chevron">⌄</span></label>
              <button className={`run-button ${simulationRunning ? "running" : ""}`} type="button" onClick={() => setSimulationRunning((running) => !running)}><Icon name={simulationRunning ? "pause" : "play"} size={15} />{simulationRunning ? "Encerrar" : "Iniciar simulação"}</button>
            </div>
          </section>
          <footer className="page-footer"><span>© 2026 Cortex Environmental Intelligence</span><span>Construído para proteger o que importa <span className="footer-leaf">✳</span></span></footer>
        </div>
      </div>
    </main>
  );
}
