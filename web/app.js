/* Helix — a perpetuals-style trading front end with a simulated market engine
 * and a paper-trading account persisted in localStorage.
 * Markets Alpaca covers (US stocks, ETFs and its crypto pairs) use real Alpaca
 * prices and bars, fetched through server.py so the API keys stay server-side;
 * every other market runs on a random-walk simulator. */
(() => {
  "use strict";

  // ───────────────────────── Market catalog ─────────────────────────
  const CATS = [
    ["fav", "★"], ["all", "All"], ["crypto", "Crypto"], ["stocks", "Stocks"], ["startups", "Startups"],
    ["indices", "Indices / ETFs"], ["commodities", "Commodities"], ["fx", "FX"], ["rates", "Rates"],
  ];
  const DAILY_VOL = { crypto: 0.035, stocks: 0.02, startups: 0.03, indices: 0.011, commodities: 0.02, fx: 0.005, rates: 0.015 };

  // sym, name, category, max leverage, price, 24h vol, open interest, 24h change, icon colour, glyph, description
  const RAW = [
    ["BTC", "Bitcoin", "crypto", 40, 81682, 2.72e9, 3.57e9, 0.0142, "#f7931a", "₿", "Bitcoin is the first decentralized cryptocurrency, a peer-to-peer electronic cash system with a fixed supply of 21 million coins secured by proof-of-work mining."],
    ["HYPE", "HYPE", "crypto", 10, 94.056, 1.39e9, 2.18e9, 0.1792, "#50d2c1", "≈", "HYPE is the native token of Hyperliquid, a high-performance layer-1 blockchain built around a fully on-chain order book exchange for perpetual futures."],
    ["ETH", "Ethereum", "crypto", 25, 2365.1, 1.14e9, 2.62e9, 0.0133, "#3c3c3d", "Ξ", "Ethereum is a programmable blockchain that runs smart contracts. Its native asset, ether, pays for computation and secures the network through proof-of-stake."],
    ["ZEC", "Zcash", "crypto", 10, 1343.0, 388.75e6, 686.92e6, 0.0522, "#e8a923", "ⓩ", "Zcash is a privacy cryptocurrency that uses zero-knowledge proofs to let users shield transaction details. It shares Bitcoin's 21 million coin cap and halving schedule."],
    ["SOL", "Solana", "crypto", 20, 182.42, 512.3e6, 1.21e9, -0.0081, "#9945ff", "◎", "Solana is a high-throughput layer-1 blockchain that combines proof-of-history timestamps with proof-of-stake for fast, low-cost transactions."],
    ["XRP", "XRP", "crypto", 20, 2.4512, 210.4e6, 640.1e6, 0.0057, "#23292f", "✕", "XRP is the native asset of the XRP Ledger, an open-source blockchain designed for fast, low-cost cross-border payments."],
    ["DOGE", "Dogecoin", "crypto", 10, 0.18234, 140.2e6, 310.5e6, -0.0214, "#c2a633", "Ð", "Dogecoin started as a meme in 2013 and grew into one of the most widely held cryptocurrencies, with an inflationary supply and low fees."],
    ["BNB", "BNB", "crypto", 10, 1105.2, 98.1e6, 220.4e6, 0.0031, "#f3ba2f", "◆", "BNB powers BNB Chain and is used for transaction fees, staking and discounts across the Binance ecosystem."],
    ["AVAX", "Avalanche", "crypto", 10, 24.312, 61.2e6, 140.7e6, -0.0132, "#e84142", "▲", "Avalanche is a smart-contract platform built around subnets, letting projects launch custom blockchains with their own rules."],
    ["LINK", "Chainlink", "crypto", 10, 17.824, 55.4e6, 120.8e6, 0.0211, "#2a5ada", "⬡", "Chainlink is a decentralized oracle network that delivers off-chain data such as prices to smart contracts."],
    ["SUI", "Sui", "crypto", 10, 3.1205, 72.9e6, 150.3e6, 0.0412, "#4da2ff", "S", "Sui is a layer-1 blockchain using the Move language and an object-centric data model for parallel transaction execution."],
    ["SKHX", "SK Hynix", "stocks", 10, 1142.9, 667.0e6, 290.07e6, 0.0049, "#ea0029", "SK", "SK Hynix is a South Korean memory chipmaker and one of the largest suppliers of DRAM and high-bandwidth memory used in AI accelerators."],
    ["GOOGL", "GOOGL", "stocks", 20, 286.35, 529.12e6, 297.78e6, -0.1173, "#4285f4", "G", "Alphabet is the parent company of Google, spanning search, advertising, YouTube, Android, cloud computing and AI research."],
    ["NVDA", "NVIDIA", "stocks", 20, 201.52, 488.4e6, 402.1e6, 0.0234, "#76b900", "N", "NVIDIA designs GPUs and the data-center systems that train and run most of today's AI models."],
    ["AAPL", "Apple", "stocks", 20, 268.81, 233.9e6, 190.2e6, -0.0042, "#555555", "A", "Apple designs the iPhone, Mac, iPad and wearables, and runs a growing services business across the App Store, iCloud and Apple Music."],
    ["TSLA", "Tesla", "stocks", 20, 452.33, 402.7e6, 351.6e6, 0.0318, "#cc0000", "T", "Tesla builds electric vehicles, batteries and energy storage, and develops self-driving software and humanoid robots."],
    ["MSFT", "Microsoft", "stocks", 20, 541.2, 180.3e6, 160.4e6, 0.0071, "#00a4ef", "⊞", "Microsoft makes Windows, Office and Azure cloud services, and is a major investor in frontier AI."],
    ["AMZN", "Amazon", "stocks", 20, 228.41, 160.1e6, 140.2e6, -0.0063, "#ff9900", "a", "Amazon runs the world's largest online store and Amazon Web Services, the biggest cloud platform."],
    ["META", "Meta", "stocks", 20, 751.3, 150.6e6, 133.9e6, 0.0122, "#0668e1", "∞", "Meta owns Facebook, Instagram, WhatsApp and Threads, and builds AI models and mixed-reality hardware."],
    ["OPENAI", "OpenAI", "startups", 3, 1240.5, 45.2e6, 88.1e6, 0.0412, "#10a37f", "◎", "Synthetic pre-IPO exposure to OpenAI, priced from secondary-market transactions and implied valuation."],
    ["SPACEX", "SpaceX", "startups", 3, 212.4, 31.8e6, 65.3e6, 0.0122, "#1b1b1b", "X", "Synthetic pre-IPO exposure to SpaceX, the launch and Starlink satellite-internet company."],
    ["STRIPE", "Stripe", "startups", 3, 41.82, 12.4e6, 30.2e6, -0.0087, "#635bff", "S", "Synthetic pre-IPO exposure to Stripe, the online payments infrastructure company."],
    ["SPX", "S&P 500", "indices", 50, 7714.2, 303.47e6, 520.3e6, -0.0029, "#d62828", "S&P", "The S&P 500 tracks 500 of the largest U.S. listed companies and is the most widely followed benchmark of the U.S. stock market."],
    ["XYZ100", "XYZ 100", "indices", 30, 29444, 367.29e6, 410.6e6, -0.0086, "#1c1c1a", "100", "XYZ 100 is a synthetic index of the 100 largest non-financial companies listed on the Nasdaq exchange."],
    ["DJI", "Dow 30", "indices", 50, 47850, 120.2e6, 200.5e6, 0.0021, "#1d3557", "DJ", "The Dow Jones Industrial Average is a price-weighted index of 30 large U.S. blue-chip companies."],
    ["SPY", "SPDR S&P 500 ETF", "indices", 20, 768.9, 40e6, 90e6, 0, "#c8102e", "SPY", "SPY is the largest exchange-traded fund tracking the S&P 500 index."],
    ["QQQ", "Invesco QQQ", "indices", 20, 715.0, 30e6, 70e6, 0, "#0b5cab", "QQQ", "QQQ is an exchange-traded fund tracking the Nasdaq-100 index of large non-financial companies."],
    ["DIA", "SPDR Dow Jones ETF", "indices", 20, 522.0, 8e6, 20e6, 0, "#1d3557", "DIA", "DIA is an exchange-traded fund tracking the Dow Jones Industrial Average."],
    ["GLD", "SPDR Gold Shares", "commodities", 20, 367.7, 25e6, 60e6, 0, "#c9a227", "GLD", "GLD is the largest exchange-traded fund backed by physical gold bullion."],
    ["SLV", "iShares Silver Trust", "commodities", 20, 47.25, 12e6, 30e6, 0, "#9ea3a8", "SLV", "SLV is an exchange-traded fund backed by physical silver."],
    ["USO", "United States Oil Fund", "commodities", 10, 165.5, 6e6, 15e6, 0, "#333333", "USO", "USO is an exchange-traded fund that tracks the price of WTI crude oil futures."],
    ["WTI", "WTI Crude Oil", "commodities", 20, 100.58, 341.65e6, 380.2e6, -0.0259, "#111111", "●", "West Texas Intermediate is the benchmark grade of U.S. crude oil, priced at Cushing, Oklahoma."],
    ["XAU", "Gold", "commodities", 25, 4012.3, 290.4e6, 610.8e6, 0.0062, "#d4af37", "Au", "Gold has been a store of value for millennia and remains a key reserve asset and hedge against inflation and currency debasement."],
    ["XAG", "Silver", "commodities", 20, 48.215, 88.3e6, 140.1e6, 0.0141, "#a8a9ad", "Ag", "Silver is both a precious metal and an industrial input used in solar panels, electronics and batteries."],
    ["NATGAS", "Natural Gas", "commodities", 10, 3.4121, 40.2e6, 66.5e6, -0.0312, "#3a86ff", "▲", "Henry Hub natural gas is the U.S. benchmark for gas used in heating and power generation."],
    ["COPPER", "Copper", "commodities", 10, 5.1234, 30.1e6, 52.4e6, 0.0055, "#b87333", "Cu", "Copper is the bellwether industrial metal, used in wiring, construction and electric vehicles."],
    ["EURUSD", "EUR / USD", "fx", 50, 1.1642, 140.4e6, 320.8e6, 0.0011, "#003399", "€", "The euro against the U.S. dollar, the most traded currency pair in the world."],
    ["GBPUSD", "GBP / USD", "fx", 50, 1.3321, 62.3e6, 120.1e6, -0.0018, "#012169", "£", "The British pound against the U.S. dollar, known as 'cable'."],
    ["USDJPY", "USD / JPY", "fx", 50, 152.84, 70.5e6, 150.2e6, 0.0024, "#bc002d", "¥", "The U.S. dollar against the Japanese yen, highly sensitive to interest-rate differentials."],
    ["US10Y", "US 10Y Yield", "rates", 20, 4.0121, 50.2e6, 140.3e6, -0.0074, "#2b2d42", "10Y", "The yield on the 10-year U.S. Treasury note, the global benchmark for long-term borrowing costs."],
    ["US2Y", "US 2Y Yield", "rates", 20, 3.5124, 30.2e6, 90.1e6, -0.0041, "#4a4e69", "2Y", "The yield on the 2-year U.S. Treasury note, closely tied to expectations for Federal Reserve policy."],
  ];
  const FEATURED = ["BTC", "SPX", "WTI", "XYZ100"];
  // Our symbol → Alpaca symbol. Crypto pairs use the v1beta3 crypto API, the rest the v2 stocks API.
  const ALPACA = {
    BTC: "BTC/USD", ETH: "ETH/USD", HYPE: "HYPE/USD", SOL: "SOL/USD", XRP: "XRP/USD", DOGE: "DOGE/USD", AVAX: "AVAX/USD", LINK: "LINK/USD",
    GOOGL: "GOOGL", NVDA: "NVDA", AAPL: "AAPL", TSLA: "TSLA", MSFT: "MSFT", AMZN: "AMZN", META: "META",
    SPY: "SPY", QQQ: "QQQ", DIA: "DIA", GLD: "GLD", SLV: "SLV", USO: "USO",
  };

  const markets = RAW.map(([sym, name, cat, maxLev, price, vol24, oi, chg24, color, glyph, desc]) => ({
    sym, name, cat, maxLev, price, vol24, oi, chg24, color, glyph, desc,
    anchor: price, real: false, realMid: null, series: {}, live: [], alpaca: ALPACA[sym] || null,
  }));
  const bySym = Object.fromEntries(markets.map((m) => [m.sym, m]));

  // ───────────────────────── Helpers ─────────────────────────
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const randn = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const uid = () => Math.random().toString(36).slice(2, 10);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function decimalsFor(p) {
    const a = Math.abs(p);
    if (a < 1) return 5;
    return clamp(5 - (Math.floor(Math.log10(a)) + 1), 0, 5);
  }
  const nf = {};
  function fmtNum(v, d) {
    const k = d;
    if (!nf[k]) nf[k] = new Intl.NumberFormat("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
    return nf[k].format(v);
  }
  const fmtPrice = (p, d = decimalsFor(p)) => "$" + fmtNum(p, d);
  const fmtUsd = (v, d = 2) => (v < 0 ? "-$" : "$") + fmtNum(Math.abs(v), d);
  const fmtSigned = (v, d = 2) => (v >= 0 ? "+$" : "-$") + fmtNum(Math.abs(v), d);
  const fmtPct = (v, d = 2) => (v >= 0 ? "+" : "") + (v * 100).toFixed(d) + "%";
  function fmtCompact(v) {
    const a = Math.abs(v);
    if (a >= 1e9) return "$" + (v / 1e9).toFixed(2) + "B";
    if (a >= 1e6) return "$" + (v / 1e6).toFixed(2) + "M";
    if (a >= 1e3) return "$" + (v / 1e3).toFixed(2) + "K";
    return "$" + v.toFixed(2);
  }
  function fmtTape(v) {
    if (v >= 1e6) return "$" + +(v / 1e6).toFixed(1) + "M";
    if (v >= 1e3) return "$" + +(v / 1e3).toFixed(1) + "K";
    return "$" + Math.round(v);
  }
  const fmtTime = (t) => new Date(t).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  const fmtDateTime = (t) => new Date(t).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  const iconHTML = (m, cls = "") => `<span class="mk-icon ${cls}" style="background:${m.color}">${esc(m.glyph)}</span>`;
  const STAR = `<svg viewBox="0 0 24 24" width="18" height="18"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.8z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>`;

  // ───────────────────────── Price history ─────────────────────────
  const RANGES = {
    live: { label: "Past minute", window: 60000 },
    "1d": { label: "Past day", n: 288, step: 300e3 },
    "1w": { label: "Past week", n: 336, step: 1800e3 },
    "1m": { label: "Past month", n: 180, step: 4 * 3600e3 },
    "1y": { label: "Past year", n: 365, step: 86400e3 },
  };

  // Brownian bridge in log space from startPrice to endPrice, with OHLC per point.
  function bridge(endPrice, startPrice, n, step, sigma, now) {
    const w = [0];
    for (let i = 1; i < n; i++) w.push(w[i - 1] + randn() * sigma);
    const last = w[n - 1];
    const target = Math.log(startPrice / endPrice);
    const b0 = w[0] - last;
    const out = [];
    let prev = startPrice;
    for (let i = 0; i < n; i++) {
      const c = (target - b0) * (n - 1 - i) / (n - 1);
      const p = endPrice * Math.exp(w[i] - last + c);
      const o = i === 0 ? p : prev;
      const wig = Math.abs(randn()) * sigma * 0.5;
      out.push({ t: now - (n - 1 - i) * step, o, h: Math.max(o, p) * (1 + wig), l: Math.min(o, p) * (1 - wig), p });
      prev = p;
    }
    return out;
  }

  function getSeries(m, range) {
    if (range === "live") return m.live;
    if (!m.series[range]) {
      const r = RANGES[range];
      const sigma = DAILY_VOL[m.cat] * Math.sqrt(r.step / 86400e3);
      let start;
      if (range === "1d") start = m.price / (1 + m.chg24);
      else start = m.price * Math.exp(randn() * DAILY_VOL[m.cat] * Math.sqrt(r.n * r.step / 86400e3) * 0.8);
      m.series[range] = bridge(m.price, start, r.n, r.step, sigma, Date.now());
    }
    return m.series[range];
  }

  function seedLive(m) {
    const now = Date.now();
    const sigma = tickSigma(m);
    const pts = bridge(m.price, m.price * Math.exp(randn() * sigma * 10), 150, 1000, sigma, now);
    m.live = pts.map(({ t, p }) => ({ t, p }));
  }
  const tickSigma = (m) => (DAILY_VOL[m.cat] / Math.sqrt(86400)) * 4;

  // ───────────────────────── Persistent state ─────────────────────────
  const KEY = "helix-state-v2";
  const START_CASH = 10;
  const FEE = 0.00045;   // per side, on notional
  const SPREAD = 0.0002; // half-spread paid on market orders
  const MAINT = 0.9;     // auto-close when losses reach 90% of the amount

  const defaults = () => ({
    cash: START_CASH, positions: [], orders: [], history: [], favorites: ["BTC", "ZEC"],
    selected: "ZEC", equity: [], refCode: uid().slice(0, 6).toUpperCase(), referrals: [], refEarned: 0,
    deposits: START_CASH,
  });
  let S;
  try { S = Object.assign(defaults(), JSON.parse(localStorage.getItem(KEY) || "{}")); } catch { S = defaults(); }
  if (!bySym[S.selected]) S.selected = "ZEC";
  let saveTimer = null;
  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {} }, 150);
  }

  // UI-only state
  const U = {
    side: "long", lev: 10, range: "live", ctype: "line", tab: "about", page: "trade",
    scPct: 10, dd: { open: false, cat: "all", sort: "vol", dir: -1, mode: "names", query: "", kb: -1 },
    mkCat: "all", pro: false, hoverX: null, yMin: null, yMax: null,
  };
  const sel = () => bySym[S.selected];

  // ───────────────────────── Account math ─────────────────────────
  const dir = (side) => (side === "long" ? 1 : -1);
  const pnlOf = (pos, mark = bySym[pos.sym].price) => (mark - pos.entry) * pos.units * dir(pos.side);
  const liqPrice = (entry, lev, side) => entry * (1 - dir(side) * MAINT / lev);
  const reservedInOrders = () => S.orders.reduce((a, o) => a + o.amount + o.fee, 0);
  function equity() {
    return S.cash + reservedInOrders() + S.positions.reduce((a, p) => a + p.margin + pnlOf(p), 0);
  }

  function toast(msg, kind = "") {
    const el = document.createElement("div");
    el.className = "toast " + kind;
    el.innerHTML = msg;
    $("#toasts").appendChild(el);
    setTimeout(() => { el.style.transition = "opacity .4s"; el.style.opacity = "0"; setTimeout(() => el.remove(), 400); }, 3800);
  }

  function openPosition({ sym, side, lev, amount, fee, entry, tp, sl }) {
    const pos = {
      id: uid(), sym, side, lev, margin: amount, openFee: fee, entry,
      units: (amount * lev) / entry, liq: liqPrice(entry, lev, side), tp: tp || null, sl: sl || null, t: Date.now(),
    };
    S.positions.push(pos);
    pushTape(amount * lev, side, true);
    toast(`<b>${side === "long" ? "Long" : "Short"} ${sym} ${lev}×</b> opened · ${fmtUsd(amount)} at ${fmtPrice(entry)}`, "good");
    save();
    return pos;
  }

  function closePosition(id, reason = "Closed") {
    const i = S.positions.findIndex((p) => p.id === id);
    if (i < 0) return;
    const pos = S.positions[i];
    const m = bySym[pos.sym];
    let exit = m.price;
    if (reason === "Closed") exit = m.price * (1 - dir(pos.side) * SPREAD);
    let pnl = pnlOf(pos, exit);
    let fee = exit * pos.units * FEE;
    if (reason === "Auto-closed") { pnl = -pos.margin * MAINT; fee = 0; exit = pos.liq; }
    S.cash += Math.max(0, pos.margin + pnl - fee);
    S.positions.splice(i, 1);
    const net = pnl - fee - pos.openFee;
    S.history.unshift({ id: pos.id, sym: pos.sym, side: pos.side, lev: pos.lev, margin: pos.margin, entry: pos.entry, exit, pnl: net, reason, t: Date.now(), opened: pos.t });
    if (S.history.length > 300) S.history.length = 300;
    toast(`<b>${pos.sym} ${pos.side} ${pos.lev}×</b> ${reason.toLowerCase()} · <span class="${net >= 0 ? "pos" : "neg"}">${fmtSigned(net)}</span>`, net >= 0 ? "good" : "bad");
    save();
  }

  function cancelOrder(id) {
    const i = S.orders.findIndex((o) => o.id === id);
    if (i < 0) return;
    const o = S.orders[i];
    S.cash += o.amount + o.fee;
    S.orders.splice(i, 1);
    toast(`Limit ${o.side} ${o.sym} cancelled`);
    save();
  }

  // Runs every tick: fill limits, trigger TP/SL and auto-close.
  function checkTriggers() {
    for (const o of [...S.orders]) {
      const m = bySym[o.sym];
      if ((o.side === "long" && m.price <= o.limit) || (o.side === "short" && m.price >= o.limit)) {
        S.orders.splice(S.orders.indexOf(o), 1);
        openPosition({ ...o, entry: o.limit });
      }
    }
    for (const p of [...S.positions]) {
      const px = bySym[p.sym].price, d = dir(p.side);
      if ((px - p.liq) * d <= 0) closePosition(p.id, "Auto-closed");
      else if (p.tp && (px - p.tp) * d >= 0) closePosition(p.id, "Take profit");
      else if (p.sl && (px - p.sl) * d <= 0) closePosition(p.id, "Stop loss");
    }
  }

  // ───────────────────────── Market engine ─────────────────────────
  function tick() {
    const now = Date.now();
    for (const m of markets) {
      const s = tickSigma(m);
      if (m.real) {
        m.price = m.realMid;
      } else {
        const rev = Math.log(m.anchor / m.price) * 0.002;
        m.price *= Math.exp(randn() * s + rev);
      }
      if (!m.real) {
        m.vol24 += Math.abs(randn()) * m.vol24 * 2e-6;
        m.oi *= 1 + randn() * 1e-4;
      }
      m.live.push({ t: now, p: m.price });
      if (m.live.length > 600) m.live.shift();
      for (const [k, arr] of Object.entries(m.series)) {
        const last = arr[arr.length - 1];
        if (now - last.t >= RANGES[k].step) {
          arr.push({ t: now, o: last.p, h: Math.max(last.p, m.price), l: Math.min(last.p, m.price), p: m.price });
          arr.shift();
        } else {
          last.p = m.price; last.h = Math.max(last.h, m.price); last.l = Math.min(last.l, m.price);
        }
      }
      if (!m.real && m.series["1d"]) m.chg24 = m.price / m.series["1d"][0].p - 1;
    }
    checkTriggers();
    accrueReferrals();
    if (now - (S.equity.at(-1)?.t || 0) > 10000) {
      S.equity.push({ t: now, v: equity() });
      if (S.equity.length > 800) S.equity.shift();
      save();
    }
    if (Math.random() < 0.55) spawnSocial();
    updateUI();
  }

  // Alpaca market data. server.py proxies /api/alpaca/* and adds the API keys;
  // without it (e.g. index.html opened from disk) only crypto works, since
  // Alpaca serves crypto data without keys.
  const ALPACA_DIRECT = "https://data.alpaca.markets";
  const alpaca = { base: null, stocks: false };
  const isCrypto = (m) => m.alpaca && m.alpaca.includes("/");
  async function alpacaGet(path, params) {
    const qs = new URLSearchParams(params).toString();
    const r = await fetch(`${alpaca.base}/${path}?${qs}`);
    if (!r.ok) throw new Error(`Alpaca ${r.status}`);
    return r.json();
  }
  async function initAlpaca() {
    try {
      const r = await fetch("api/config");
      const cfg = r.ok ? await r.json() : {};
      if (cfg.alpaca) { alpaca.base = "api/alpaca"; alpaca.stocks = true; }
    } catch { /* no proxy */ }
    if (!alpaca.base) alpaca.base = ALPACA_DIRECT;
    await pollAlpaca();
    setInterval(pollAlpaca, 3000);
  }
  function applySnapshot(m, snap) {
    const px = snap?.latestTrade?.p;
    if (!(px > 0)) return;
    if (!m.real) {
      // First real print: rescale the seeded history and drop simulated ranges.
      m.live = [{ t: Date.now(), p: px }];
      m.series = {};
      m.real = true;
      m.price = px;
      loadRealCandles(m, "1d");
      if (sel() === m) onMarketChange(false);
    }
    m.realMid = px;
    m.anchor = px;
    const prev = snap.prevDailyBar?.c;
    if (prev > 0) m.chg24 = px / prev - 1;
    const day = snap.dailyBar;
    if (day && day.v > 0) m.vol24 = day.v * (day.vw || px);
  }
  async function pollAlpaca() {
    const crypto = markets.filter(isCrypto);
    const stocks = markets.filter((m) => m.alpaca && !isCrypto(m));
    const jobs = [
      alpacaGet("v1beta3/crypto/us/snapshots", { symbols: crypto.map((m) => m.alpaca).join(",") })
        .then((d) => crypto.forEach((m) => applySnapshot(m, d.snapshots?.[m.alpaca]))),
    ];
    if (alpaca.stocks) {
      jobs.push(alpacaGet("v2/stocks/snapshots", { symbols: stocks.map((m) => m.alpaca).join(",") })
        .then((d) => stocks.forEach((m) => applySnapshot(m, d[m.alpaca]))));
    }
    await Promise.allSettled(jobs);
  }

  const ALPACA_TF = { "1d": "5Min", "1w": "30Min", "1m": "4Hour", "1y": "1Day" };
  const candleReq = {};
  async function loadRealCandles(m, range) {
    const key = m.sym + range;
    if (!m.real || range === "live" || candleReq[key]) return;
    candleReq[key] = true;
    try {
      const r = RANGES[range];
      const span = r.n * r.step;
      const now = Date.now();
      // Stocks only trade ~6.5h a day, so look back far enough to cover weekends.
      const lookback = isCrypto(m) ? span : Math.max(span * 1.6, 5 * 86400e3);
      const path = isCrypto(m) ? "v1beta3/crypto/us/bars" : "v2/stocks/bars";
      const params = { symbols: m.alpaca, timeframe: ALPACA_TF[range], start: new Date(now - lookback).toISOString(), limit: 10000 };
      let bars = [];
      for (let page = 0; page < 5; page++) {
        const d = await alpacaGet(path, params);
        bars = bars.concat(d.bars?.[m.alpaca] || []);
        if (!d.next_page_token) break;
        params.page_token = d.next_page_token;
      }
      let pts = bars.map((b) => ({ t: Date.parse(b.t), o: b.o, h: b.h, l: b.l, p: b.c }));
      const recent = pts.filter((p) => p.t >= now - span);
      pts = recent.length >= 20 ? recent : pts.slice(-r.n);
      if (pts.length >= 2) {
        m.series[range] = pts;
        if (sel() === m) { U.yMin = null; renderAbout(); }
      } else candleReq[key] = false;
    } catch { candleReq[key] = false; }
  }

  // ───────────────────────── Trade tape + social ─────────────────────────
  const NAMES_A = ["quiet", "lucky", "brave", "sly", "calm", "swift", "bold", "giga", "based", "wild", "zen", "turbo", "salty", "frosty", "sunny"];
  const NAMES_B = ["otter", "whale", "falcon", "panda", "degen", "monk", "fox", "yak", "koala", "lynx", "shark", "tiger", "orca", "heron", "bison"];
  const AV_COLORS = ["#2e8b67", "#d2554f", "#3a86ff", "#9945ff", "#e8a923", "#1c1c1a", "#f05a28", "#50a5b8"];
  const randomUser = () => NAMES_A[(Math.random() * NAMES_A.length) | 0] + "_" + NAMES_B[(Math.random() * NAMES_B.length) | 0];
  const tape = [];
  function pushTape(notional, side, mine = false) {
    tape.push({ v: notional, side, mine });
    if (tape.length > 7) tape.shift();
    renderTape();
  }
  function renderTape() {
    const n = tape.length;
    $("#tape").innerHTML = tape.map((t, i) =>
      `<li class="${t.side}${t.mine ? " mine" : ""}" style="opacity:${(1 - (n - 1 - i) * 0.12).toFixed(2)}"><span class="plus">+</span>${fmtTape(t.v)}</li>`).join("");
  }
  let lastTape = 0;
  function maybeTape() {
    const now = Date.now();
    if (now - lastTape < 1400 + Math.random() * 2600) return;
    lastTape = now;
    pushTape(Math.exp(randn() * 1.5 + 4), Math.random() < 0.58 ? "long" : "short");
  }

  const feed = [];
  function spawnSocial() {
    const m = markets[Math.floor(Math.random() * Math.random() * markets.length)];
    const side = Math.random() < 0.58 ? "long" : "short";
    const lev = [1, 2, 3, 5, 10, Math.min(20, m.maxLev), m.maxLev][(Math.random() * 7) | 0];
    const amt = Math.exp(randn() * 1.4 + 3.5);
    const closing = Math.random() < 0.3;
    feed.unshift({ who: randomUser(), m: m.sym, side, lev: Math.min(lev, m.maxLev), amt, closing, pnl: closing ? amt * randn() * 0.6 : 0, t: Date.now() });
    if (feed.length > 60) feed.pop();
    if (U.page === "social") renderSocialFeed(true);
  }
  const leaders = Array.from({ length: 12 }, () => ({ who: randomUser(), pnl: Math.exp(randn() + 7) }));

  // ───────────────────────── Chart ─────────────────────────
  const canvas = $("#chart");
  const ctx = canvas.getContext("2d");
  const GREEN = "#2e8b67", RED = "#d2554f";

  function niceStep(span, count) {
    const raw = span / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const n = raw / mag;
    return (n < 1.5 ? 1 : n < 2.25 ? 2 : n < 3.5 ? 2.5 : n < 7.5 ? 5 : 10) * mag;
  }
  function timeLabel(t, range) {
    const d = new Date(t);
    if (range === "live") return fmtTime(t);
    if (range === "1d") return d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
    if (range === "1w") return d.toLocaleDateString("en-US", { weekday: "short", day: "numeric" }) + " " + d.toLocaleTimeString("en-US", { hour: "numeric" });
    if (range === "1m") return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    return d.toLocaleDateString("en-US", { month: "short", year: "2-digit" });
  }
  function visiblePoints(m, now) {
    if (U.range === "live") {
      const t0 = now - RANGES.live.window;
      const pts = m.live.filter((p) => p.t >= t0 - 2000);
      pts.push({ t: now, p: m.price });
      return { pts, t0, t1: now };
    }
    // Ranged charts are spaced by bar index, so market closures don't show as long flat gaps.
    const pts = getSeries(m, U.range).map((p, i) => ({ ...p, t: i, time: p.t }));
    return { pts, t0: 0, t1: pts.length - 1 };
  }
  function candlesFrom(pts, range, t0) {
    const out = [];
    if (range === "live") {
      const map = new Map();
      for (const p of pts) {
        const k = Math.floor(p.t / 3000) * 3000;
        if (k < t0 - 3000) continue;
        const c = map.get(k);
        if (!c) map.set(k, { t: k + 1500, o: p.p, h: p.p, l: p.p, c: p.p });
        else { c.h = Math.max(c.h, p.p); c.l = Math.min(c.l, p.p); c.c = p.p; }
      }
      return [...map.values()];
    }
    const k = Math.max(1, Math.ceil(pts.length / 72));
    for (let i = 0; i < pts.length; i += k) {
      const g = pts.slice(i, i + k);
      out.push({
        t: (g[0].t + g.at(-1).t) / 2, o: g[0].o ?? g[0].p, c: g.at(-1).p,
        h: Math.max(...g.map((x) => x.h ?? x.p)), l: Math.min(...g.map((x) => x.l ?? x.p)),
      });
    }
    return out;
  }

  function drawChart() {
    const wrap = $("#chartWrap");
    const W = wrap.clientWidth, H = wrap.clientHeight;
    if (!W || !H) return;
    const dpr = window.devicePixelRatio || 1;
    if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    const m = sel();
    const now = Date.now();
    const { pts, t0, t1 } = visiblePoints(m, now);
    if (pts.length < 2) return;
    const narrow = W < 600;
    const L = 0, R = W - (narrow ? 78 : 100), T = 24, B = H - 40;
    const candles = U.ctype === "candle" ? candlesFrom(pts, U.range, t0) : null;

    let lo = Infinity, hi = -Infinity;
    if (candles) for (const c of candles) { lo = Math.min(lo, c.l); hi = Math.max(hi, c.h); }
    else for (const p of pts) { if (p.t >= t0 - 1) { lo = Math.min(lo, p.p); hi = Math.max(hi, p.p); } }
    if (hi - lo < m.price * 1e-5) { hi += m.price * 5e-5; lo -= m.price * 5e-5; }
    const pad = (hi - lo) * 0.12;
    lo -= pad; hi += pad;
    if (U.yMin == null) { U.yMin = lo; U.yMax = hi; }
    U.yMin += (lo - U.yMin) * 0.12; U.yMax += (hi - U.yMax) * 0.12;
    const yMin = U.yMin, yMax = U.yMax;
    const X = (t) => L + ((t - t0) / (t1 - t0)) * (R - L);
    const Y = (p) => B - ((p - yMin) / (yMax - yMin)) * (B - T);
    const first = U.range === "live" ? (pts.find((p) => p.t >= t0) || pts[0]).p : pts[0].p;
    const up = m.price >= first;
    const col = up ? GREEN : RED;
    const d = decimalsFor(m.price);

    // Y-axis labels
    ctx.font = `${narrow ? 11 : 12.5}px "JetBrains Mono", monospace`;
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#8a8883";
    const step = niceStep(yMax - yMin, 6);
    for (let v = Math.ceil(yMin / step) * step; v <= yMax; v += step) {
      const y = Y(v);
      if (y < T - 4 || y > B + 4 || Math.abs(y - Y(m.price)) < 18) continue;
      ctx.fillText(fmtPrice(v, Math.max(d, step < 1 ? Math.ceil(-Math.log10(step)) : 0)), R + 18, y);
    }

    // X-axis labels
    ctx.textBaseline = "alphabetic";
    const nLab = narrow ? 2 : 4;
    const realTime = (t) => (U.range === "live" ? t : pts[clamp(Math.round(t), 0, pts.length - 1)].time);
    const endLabel = U.range === "live" ? "now" : timeLabel(realTime(t1), U.range);
    const endW = ctx.measureText(endLabel).width;
    for (let i = 0; i < nLab; i++) {
      const t = t0 + ((t1 - t0) * i) / nLab;
      const s = timeLabel(realTime(t), U.range), w = ctx.measureText(s).width;
      ctx.fillText(s, i === 0 ? 0 : clamp(X(t) - w / 2, 0, R - endW - w - 16), H - 8);
    }
    ctx.fillText(endLabel, R - endW, H - 8);

    // Plot area clip
    ctx.save();
    ctx.beginPath(); ctx.rect(L, T - 10, R - L + 6, B - T + 20); ctx.clip();

    if (candles) {
      const cw = Math.max(2, ((R - L) / Math.max(candles.length, 20)) * 0.62);
      for (const c of candles) {
        const x = X(c.t), g = c.c >= c.o;
        ctx.strokeStyle = ctx.fillStyle = g ? GREEN : RED;
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(x, Y(c.h)); ctx.lineTo(x, Y(c.l)); ctx.stroke();
        const yo = Y(c.o), yc = Y(c.c);
        ctx.fillRect(x - cw / 2, Math.min(yo, yc), cw, Math.max(1, Math.abs(yc - yo)));
      }
    } else {
      // Area
      const grad = ctx.createLinearGradient(0, T, 0, B);
      grad.addColorStop(0, up ? "rgba(46,139,103,0.20)" : "rgba(210,85,79,0.18)");
      grad.addColorStop(1, up ? "rgba(46,139,103,0.06)" : "rgba(210,85,79,0.04)");
      ctx.beginPath();
      pts.forEach((p, i) => (i ? ctx.lineTo(X(p.t), Y(p.p)) : ctx.moveTo(X(p.t), Y(p.p))));
      ctx.lineTo(X(pts.at(-1).t), B + 20); ctx.lineTo(X(pts[0].t), B + 20); ctx.closePath();
      ctx.fillStyle = grad; ctx.fill();
      // Glow + line
      const line = () => { ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo(X(p.t), Y(p.p)) : ctx.moveTo(X(p.t), Y(p.p)))); };
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      line(); ctx.strokeStyle = up ? "rgba(46,139,103,0.18)" : "rgba(210,85,79,0.18)"; ctx.lineWidth = 7; ctx.stroke();
      line(); ctx.strokeStyle = col; ctx.lineWidth = 2.4; ctx.stroke();
    }
    ctx.restore();

    // Your positions and orders on this market
    const marks = [
      ...S.positions.filter((p) => p.sym === m.sym).map((p) => ({ v: p.entry, c: p.side === "long" ? GREEN : RED, t: `${p.side.toUpperCase()} ${p.lev}×` })),
      ...S.positions.filter((p) => p.sym === m.sym).map((p) => ({ v: p.liq, c: "#b0aea8", t: "AUTO-CLOSE" })),
      ...S.orders.filter((o) => o.sym === m.sym).map((o) => ({ v: o.limit, c: "#6c6a65", t: `LIMIT ${o.side.toUpperCase()}` })),
    ];
    ctx.font = '600 10.5px "JetBrains Mono", monospace';
    for (const mk of marks) {
      const y = Y(mk.v);
      if (y < T || y > B) continue;
      ctx.strokeStyle = mk.c; ctx.lineWidth = 1; ctx.setLineDash([6, 4]);
      ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke(); ctx.setLineDash([]);
      const tw = ctx.measureText(mk.t).width + 10;
      ctx.fillStyle = mk.c; roundRect(R - tw - 40, y - 9, tw, 18, 4); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.textBaseline = "middle"; ctx.fillText(mk.t, R - tw - 35, y + 1);
    }

    // Current price line, dot, pill
    const yNow = Y(m.price), xNow = X(U.range === "live" ? now : t1);
    ctx.strokeStyle = "rgba(0,0,0,0.18)"; ctx.setLineDash([4, 5]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(L, yNow); ctx.lineTo(R, yNow); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(xNow, yNow, 5.5, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.font = `600 ${narrow ? 11.5 : 13.5}px "JetBrains Mono", monospace`;
    const label = fmtPrice(m.price);
    const pw = ctx.measureText(label).width + 14;
    ctx.fillStyle = "#e6e4df"; roundRect(R + 8, yNow - 15, pw, 30, 6); ctx.fill();
    ctx.fillStyle = "#1c1c1a"; ctx.textBaseline = "middle"; ctx.fillText(label, R + 15, yNow + 1);

    // Hover crosshair
    const tip = $("#chartTip");
    if (U.hoverX != null && U.hoverX >= L && U.hoverX <= R) {
      const tH = t0 + ((U.hoverX - L) / (R - L)) * (t1 - t0);
      let best = pts[0];
      for (const p of pts) if (Math.abs(p.t - tH) < Math.abs(best.t - tH)) best = p;
      const hx = X(best.t), hy = Y(best.p);
      ctx.strokeStyle = "rgba(0,0,0,0.3)"; ctx.setLineDash([3, 4]);
      ctx.beginPath(); ctx.moveTo(hx, T - 10); ctx.lineTo(hx, B); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(hx, hy, 4, 0, Math.PI * 2); ctx.fill();
      const chg = best.p / first - 1;
      tip.innerHTML = `<div>${fmtPrice(best.p)} <span style="color:${chg >= 0 ? "#6fd3a6" : "#ff8b85"}">${fmtPct(chg)}</span></div><div>${U.range === "live" ? fmtTime(best.t) : fmtDateTime(best.time)}</div>`;
      tip.hidden = false;
      const tw = tip.offsetWidth;
      tip.style.left = clamp(hx + 12, 0, W - tw - 4) + "px";
      tip.style.top = clamp(hy - 46, 0, H - 40) + "px";
    } else tip.hidden = true;
  }
  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  canvas.addEventListener("mousemove", (e) => { U.hoverX = e.offsetX; });
  canvas.addEventListener("mouseleave", () => { U.hoverX = null; });
  canvas.addEventListener("touchmove", (e) => { const r = canvas.getBoundingClientRect(); U.hoverX = e.touches[0].clientX - r.left; }, { passive: true });
  canvas.addEventListener("touchend", () => { U.hoverX = null; });

  function frame() {
    if (U.page === "trade" && !document.hidden) drawChart();
    requestAnimationFrame(frame);
  }

  // ───────────────────────── Header / price ─────────────────────────
  function renderPriceHeader() {
    const m = sel();
    const s = fmtPrice(m.price);
    const dot = s.indexOf(".");
    $("#bigPrice").innerHTML = dot < 0 ? s : `${s.slice(0, dot)}<span class="dim">${s.slice(dot)}</span>`;
    let ref;
    if (U.range === "live") {
      const t0 = Date.now() - 60000;
      ref = (m.live.find((p) => p.t >= t0) || m.live[0] || { p: m.price }).p;
    } else ref = getSeries(m, U.range)[0].p;
    const diff = m.price - ref, pct = diff / ref;
    const cls = diff >= 0 ? "pos" : "neg";
    $("#priceChange").innerHTML = `<span class="${cls}">${diff >= 0 ? "▲" : "▼"} ${fmtPrice(Math.abs(diff), Math.max(2, decimalsFor(m.price)))} (${(Math.abs(pct) * 100).toFixed(2)}%)</span> <span class="lbl">· ${RANGES[U.range].label}</span>`;
    document.title = `${fmtNum(m.price, decimalsFor(m.price))} · ${m.sym} | Helix`;
    $("#hdrPortfolio").textContent = fmtUsd(equity());
    $("#hdrCash").textContent = fmtUsd(S.cash);
  }

  function renderAbout() {
    const m = sel();
    const d1 = getSeries(m, "1d"), m1 = getSeries(m, "1m");
    const hi = (a) => Math.max(...a.map((p) => p.h ?? p.p)), lo = (a) => Math.min(...a.map((p) => p.l ?? p.p));
    $("#aboutDesc").innerHTML = esc(m.desc) + ` <span class="muted">${m.real ? "Live prices and charts from Alpaca." : m.alpaca ? "Loading Alpaca data…" : "Simulated prices (not available on Alpaca)."}</span>`;
    const stats = [
      ["24h volume", fmtCompact(m.vol24)], ["Open positions", fmtCompact(m.oi)],
      ["24h change", `<span class="${m.chg24 >= 0 ? "pos" : "neg"}">${fmtPct(m.chg24)}</span>`], ["Max leverage", m.maxLev + "×"],
      ["24h high", fmtNum(hi(d1), decimalsFor(m.price))], ["24h low", fmtNum(lo(d1), decimalsFor(m.price))],
      ["Month high", fmtNum(hi(m1), decimalsFor(m.price))], ["Month low", fmtNum(lo(m1), decimalsFor(m.price))],
    ];
    $("#aboutStats").innerHTML = stats.map(([k, v]) => `<div><span>${k}</span><strong>${k.includes("high") || k.includes("low") ? "$" : ""}${v}</strong></div>`).join("");
  }

  // ───────────────────────── Tables ─────────────────────────
  function positionsHTML(list) {
    if (!list.length) return `<div class="empty">No open positions</div>`;
    return `<div class="table-scroll"><table class="grid"><thead><tr><th>Market</th><th>Side</th><th>Amount</th><th>Value</th><th>Entry</th><th>Mark</th><th>Auto-close</th><th>TP / SL</th><th>PnL</th><th></th></tr></thead><tbody>${
      list.map((p) => {
        const m = bySym[p.sym];
        return `<tr><td class="mkt"><span class="inner" data-goto="${p.sym}">${iconHTML(m)}${p.sym}</span></td>
          <td><span class="side-tag ${p.side}">${p.side === "long" ? "Long" : "Short"} ${p.lev}×</span></td>
          <td>${fmtUsd(p.margin)}</td><td data-f="val-${p.id}"></td><td>${fmtPrice(p.entry)}</td><td data-f="mark-${p.id}"></td>
          <td>${fmtPrice(p.liq)}</td><td>${p.tp ? fmtPrice(p.tp) : "–"} / ${p.sl ? fmtPrice(p.sl) : "–"}</td>
          <td data-f="pnl-${p.id}"></td><td><button class="btn-sm danger" data-close-pos="${p.id}">Close</button></td></tr>`;
      }).join("")}</tbody></table></div>`;
  }
  function updatePositionCells() {
    for (const p of S.positions) {
      const m = bySym[p.sym], pnl = pnlOf(p), pct = pnl / p.margin;
      $$(`[data-f="mark-${p.id}"]`).forEach((el) => (el.textContent = fmtPrice(m.price)));
      $$(`[data-f="val-${p.id}"]`).forEach((el) => (el.textContent = fmtUsd(p.margin + pnl)));
      $$(`[data-f="pnl-${p.id}"]`).forEach((el) => (el.innerHTML = `<span class="${pnl >= 0 ? "pos" : "neg"}">${fmtSigned(pnl)} (${fmtPct(pct, 1)})</span>`));
    }
  }
  function ordersHTML(list) {
    if (!list.length) return `<div class="empty">No open orders</div>`;
    return `<div class="table-scroll"><table class="grid"><thead><tr><th>Market</th><th>Side</th><th>Type</th><th>Limit</th><th>Mark</th><th>Amount</th><th>TP / SL</th><th>Placed</th><th></th></tr></thead><tbody>${
      list.map((o) => `<tr><td class="mkt"><span class="inner" data-goto="${o.sym}">${iconHTML(bySym[o.sym])}${o.sym}</span></td>
        <td><span class="side-tag ${o.side}">${o.side === "long" ? "Long" : "Short"} ${o.lev}×</span></td><td>Limit</td>
        <td>${fmtPrice(o.limit)}</td><td data-f="omark-${o.id}">${fmtPrice(bySym[o.sym].price)}</td><td>${fmtUsd(o.amount)}</td>
        <td>${o.tp ? fmtPrice(o.tp) : "–"} / ${o.sl ? fmtPrice(o.sl) : "–"}</td><td>${fmtDateTime(o.t)}</td>
        <td><button class="btn-sm" data-cancel="${o.id}">Cancel</button></td></tr>`).join("")}</tbody></table></div>`;
  }
  function historyHTML(list) {
    if (!list.length) return `<div class="empty">No trades yet</div>`;
    return `<div class="table-scroll"><table class="grid"><thead><tr><th>Market</th><th>Side</th><th>Amount</th><th>Entry</th><th>Exit</th><th>PnL</th><th>Result</th><th>Closed</th></tr></thead><tbody>${
      list.slice(0, 100).map((h) => `<tr><td class="mkt"><span class="inner" data-goto="${h.sym}">${iconHTML(bySym[h.sym])}${h.sym}</span></td>
        <td><span class="side-tag ${h.side}">${h.side === "long" ? "Long" : "Short"} ${h.lev}×</span></td><td>${fmtUsd(h.margin)}</td>
        <td>${fmtPrice(h.entry)}</td><td>${fmtPrice(h.exit)}</td><td class="${h.pnl >= 0 ? "pos" : "neg"}">${fmtSigned(h.pnl)}</td>
        <td style="font-family:var(--sans)">${h.reason}</td><td>${fmtDateTime(h.t)}</td></tr>`).join("")}</tbody></table></div>`;
  }

  let tableSig = "";
  function renderTables(force) {
    const sig = S.positions.map((p) => p.id).join() + "|" + S.orders.map((o) => o.id).join() + "|" + S.history.length + "|" + U.page;
    if (force || sig !== tableSig) {
      tableSig = sig;
      $("#tab-positions").innerHTML = positionsHTML(S.positions);
      $("#tab-orders").innerHTML = ordersHTML(S.orders);
      $("#tab-history").innerHTML = historyHTML(S.history);
      if (U.page === "portfolio") {
        $("#pfPositions").innerHTML = positionsHTML(S.positions);
        $("#pfOrders").innerHTML = ordersHTML(S.orders);
        $("#pfHistory").innerHTML = historyHTML(S.history);
      }
      const setCnt = (id, n) => { const el = $(id); el.hidden = !n; el.textContent = n; };
      setCnt("#cntPositions", S.positions.length);
      setCnt("#cntOrders", S.orders.length);
      setCnt("#cntHistory", S.history.length);
    }
    updatePositionCells();
    for (const o of S.orders) $$(`[data-f="omark-${o.id}"]`).forEach((el) => (el.textContent = fmtPrice(bySym[o.sym].price)));
  }

  document.addEventListener("click", (e) => {
    const c = e.target.closest("[data-close-pos]");
    if (c) return closePosition(c.dataset.closePos), renderTables(true);
    const x = e.target.closest("[data-cancel]");
    if (x) return cancelOrder(x.dataset.cancel), renderTables(true);
    const g = e.target.closest("[data-goto]");
    if (g) { selectMarket(g.dataset.goto); location.hash = "#trade"; }
  });

  // ───────────────────────── Order panel ─────────────────────────
  const amountInput = $("#amountInput"), limitInput = $("#limitInput"), tpInput = $("#tpInput"), slInput = $("#slInput");
  const num = (el) => { const v = parseFloat(String(el.value).replace(/[^0-9.]/g, "")); return isFinite(v) ? v : 0; };
  const orderType = () => $("#orderType").value;
  const maxAmount = () => Math.floor((S.cash / (1 + U.lev * FEE)) * 100) / 100;

  function levMarks(max) {
    if (max <= 3) return [...new Set([1, 2, max])];
    return [...new Set([1, Math.round(max * 0.2), Math.round(max * 0.5), max])].filter((v) => v >= 1);
  }
  function renderSlider() {
    const m = sel();
    const max = m.maxLev;
    const inp = $("#levInput");
    inp.max = max;
    inp.value = U.lev;
    const f = max === 1 ? 1 : (U.lev - 1) / (max - 1);
    // Thumb is ~42px wide; keep its centre inside the track at both ends.
    $("#levFill").style.width = `calc(42px + ${f} * (100% - 42px))`;
    const thumb = $("#levThumb");
    thumb.textContent = U.lev + "×";
    thumb.style.left = `calc(27px + ${f} * (100% - 54px))`;
    $("#levSlider").classList.toggle("short", U.side === "short");
    const marks = levMarks(max);
    const pos = (v) => `calc(21px + ${max === 1 ? 0 : (v - 1) / (max - 1)} * (100% - 42px))`;
    $("#levTicks").innerHTML = marks.slice(1, -1).map((v) => `<span style="left:${pos(v)}"></span>`).join("");
    $("#levMarks").innerHTML = marks.map((v) => `<span data-lev="${v}" style="left:${pos(v)}">${v}×</span>`).join("");
  }

  function readOrder() {
    const m = sel();
    const type = orderType();
    const amount = num(amountInput);
    const ref = type === "limit" && num(limitInput) > 0 ? num(limitInput) : m.price * (1 + dir(U.side) * SPREAD);
    const notional = amount * U.lev;
    const fee = notional * FEE;
    const tpsl = $("#tpslToggle").checked;
    return { m, type, amount, ref, notional, fee, tp: tpsl ? num(tpInput) : 0, sl: tpsl ? num(slInput) : 0 };
  }

  function validate(o) {
    const d = dir(U.side);
    if (!o.amount) return "Enter an amount";
    if (o.amount < 1) return "Minimum amount is $1";
    if (o.amount + o.fee > S.cash + 1e-9) return "Insufficient cash";
    if (o.type === "limit" && !(num(limitInput) > 0)) return "Enter a limit price";
    if (o.tp && (o.tp - o.ref) * d <= 0) return `Take profit must be ${d > 0 ? "above" : "below"} entry`;
    if (o.sl && (o.sl - o.ref) * d >= 0) return `Stop loss must be ${d > 0 ? "below" : "above"} entry`;
    if (o.sl && (o.sl - liqPrice(o.ref, U.lev, U.side)) * d <= 0) return "Stop loss is past auto-close";
    return null;
  }

  function renderOrderPanel() {
    const o = readOrder();
    const m = o.m;
    $("#availCash").textContent = fmtUsd(S.cash);
    const pct = U.scPct / 100;
    $("#scTitle").textContent = `If price ${U.side === "long" ? "rises" : "falls"} ${+U.scPct.toFixed(2)}%`;
    const gain = o.notional * pct;
    const sv = $("#scValue");
    sv.textContent = o.amount ? fmtSigned(gain) : "$0.00";
    sv.classList.toggle("pos", !!o.amount);
    $("#scLiq").textContent = o.amount ? fmtPrice(liqPrice(o.ref, U.lev, U.side)) : "–";
    $("#scSize").textContent = o.amount ? `${fmtUsd(o.notional)} · ${fmtNum(o.notional / o.ref, o.notional / o.ref < 1 ? 5 : 3)} ${m.sym}` : "–";
    $("#scFee").textContent = o.amount ? fmtUsd(o.fee, o.fee < 0.1 ? 4 : 2) : "–";
    const hint = (el, px) => {
      if (!px) return (el.textContent = "");
      const r = ((px - o.ref) / o.ref) * dir(U.side) * U.lev * o.amount;
      el.innerHTML = o.amount ? `<span class="${r >= 0 ? "pos" : "neg"}">${fmtSigned(r)}</span>` : "";
    };
    hint($("#tpHint"), o.tp); hint($("#slHint"), o.sl);
    const err = validate(o);
    const btn = $("#submitBtn");
    btn.disabled = !!err;
    btn.className = "submit" + (err ? "" : " " + U.side);
    btn.textContent = err || `${o.type === "limit" ? "Place limit " : ""}${U.side === "long" ? "Long" : "Short"} ${m.sym} · ${fmtUsd(o.amount)}`;
  }

  function submitOrder() {
    const o = readOrder();
    if (validate(o)) return;
    const m = o.m;
    S.cash -= o.amount + o.fee;
    const base = { sym: m.sym, side: U.side, lev: U.lev, amount: o.amount, fee: o.fee, tp: o.tp || null, sl: o.sl || null };
    const marketable = o.type === "limit" && (o.ref - m.price) * dir(U.side) >= 0;
    if (o.type === "market" || marketable) {
      openPosition({ ...base, entry: o.type === "market" ? o.ref : m.price });
    } else {
      S.orders.push({ ...base, id: uid(), limit: o.ref, t: Date.now() });
      toast(`Limit ${U.side} ${m.sym} placed at ${fmtPrice(o.ref)}`);
      save();
    }
    amountInput.value = "";
    tpInput.value = slInput.value = "";
    renderTables(true);
    renderOrderPanel();
    setTab(o.type === "market" || marketable ? "positions" : "orders");
  }

  $("#sideToggle").addEventListener("click", (e) => {
    const b = e.target.closest("[data-side]");
    if (!b) return;
    U.side = b.dataset.side;
    $$("#sideToggle button").forEach((x) => x.classList.toggle("active", x === b));
    renderSlider(); renderOrderPanel();
  });
  $("#quickAmounts").addEventListener("click", (e) => {
    const b = e.target.closest("[data-amt]");
    if (!b) return;
    amountInput.value = b.dataset.amt === "max" ? maxAmount().toFixed(2) : b.dataset.amt;
    renderOrderPanel();
  });
  [amountInput, limitInput, tpInput, slInput].forEach((el) => el.addEventListener("input", () => {
    el.value = el.value.replace(/[^0-9.]/g, "").replace(/(\..*)\./g, "$1");
    renderOrderPanel();
  }));
  $("#levInput").addEventListener("input", (e) => { U.lev = +e.target.value; renderSlider(); renderOrderPanel(); });
  $("#levMarks").addEventListener("click", (e) => { const s = e.target.closest("[data-lev]"); if (s) { U.lev = +s.dataset.lev; renderSlider(); renderOrderPanel(); } });
  $("#tpslToggle").addEventListener("change", (e) => { $("#tpslBox").hidden = !e.target.checked; renderOrderPanel(); });
  $("#orderType").addEventListener("change", () => {
    const lim = orderType() === "limit";
    $("#limitRow").hidden = !lim;
    if (lim && !limitInput.value) limitInput.value = sel().price.toFixed(decimalsFor(sel().price));
    renderOrderPanel();
  });
  $("#limitMid").addEventListener("click", () => { limitInput.value = sel().price.toFixed(decimalsFor(sel().price)); renderOrderPanel(); });
  $("#scPcts").addEventListener("click", (e) => {
    const b = e.target.closest("[data-pct]");
    if (!b) return;
    $$("#scPcts button").forEach((x) => x.classList.toggle("active", x === b));
    if (b.dataset.pct === "custom") {
      b.hidden = true;
      const inp = $("#scCustom"); inp.hidden = false; inp.focus();
      return;
    }
    $("#scCustom").hidden = true; $("#scCustomBtn").hidden = false;
    U.scPct = +b.dataset.pct; renderOrderPanel();
  });
  $("#scCustom").addEventListener("input", (e) => { const v = parseFloat(e.target.value); if (v > 0) { U.scPct = Math.min(v, 1000); renderOrderPanel(); } });
  $("#scCustom").addEventListener("blur", (e) => {
    if (!(parseFloat(e.target.value) > 0)) { e.target.hidden = true; $("#scCustomBtn").hidden = false; }
  });
  $("#submitBtn").addEventListener("click", submitOrder);
  amountInput.addEventListener("keydown", (e) => { if (e.key === "Enter") submitOrder(); });

  // Pro: order book
  function renderOrderbook() {
    if (!U.pro) return;
    const m = sel(), d = decimalsFor(m.price);
    const tick = Math.pow(10, -d) * Math.max(1, Math.round(m.price * 0.00005 / Math.pow(10, -d)));
    const mk = (side) => {
      let tot = 0;
      return Array.from({ length: 8 }, (_, i) => {
        const px = m.price + (side === "ask" ? 1 : -1) * tick * (i + 1);
        const sz = Math.exp(randn() * 0.8) * (5000 / m.price) * (1 + i * 0.3);
        tot += sz;
        return { px, sz, tot };
      });
    };
    const asks = mk("ask"), bids = mk("bid");
    const maxT = Math.max(asks.at(-1).tot, bids.at(-1).tot);
    const sd = m.price > 1000 ? 4 : m.price > 10 ? 2 : 0;
    const row = (r, cls) => `<div class="ob-row ${cls}"><div class="bar" style="width:${(r.tot / maxT) * 100}%"></div><span>${fmtNum(r.px, d)}</span><span>${fmtNum(r.sz, sd)}</span><span>${fmtNum(r.tot, sd)}</span></div>`;
    $("#obAsks").innerHTML = asks.slice().reverse().map((r) => row(r, "ask")).join("");
    $("#obBids").innerHTML = bids.map((r) => row(r, "bid")).join("");
    $("#obMid").textContent = `${fmtPrice(m.price)}  ·  spread ${fmtNum(tick * 2, d)}`;
  }
  $("#proBtn").addEventListener("click", () => {
    U.pro = !U.pro;
    $("#proBtn").classList.toggle("active", U.pro);
    $("#orderbook").hidden = !U.pro;
    if (U.page !== "trade") location.hash = "#trade";
    renderOrderbook();
  });

  // ───────────────────────── Market dropdown ─────────────────────────
  const dd = U.dd;
  function filtered(cat, query) {
    const q = query.trim().toLowerCase();
    let list = markets.filter((m) => cat === "all" || (cat === "fav" ? S.favorites.includes(m.sym) : m.cat === cat));
    if (q) list = markets.filter((m) => m.sym.toLowerCase().includes(q) || m.name.toLowerCase().includes(q));
    return list;
  }
  function sortList(list, key, d) {
    const get = { name: (m) => m.name.toLowerCase(), price: (m) => m.price, chg: (m) => m.chg24, oi: (m) => m.oi, vol: (m) => m.vol24 }[key];
    return list.slice().sort((a, b) => (get(a) > get(b) ? 1 : get(a) < get(b) ? -1 : 0) * d);
  }
  const label = (m) => (dd.mode === "names" ? m.name : m.sym);
  function catButtons(active) {
    return CATS.map(([k, v]) => `<button data-cat="${k}" class="${k === active ? "active" : ""}">${v}</button>`).join("");
  }
  let ddRows = [];
  function renderDD() {
    $("#ddCats").innerHTML = catButtons(dd.cat);
    $$("#ddNameMode button").forEach((b) => b.classList.toggle("active", b.dataset.mode === dd.mode));
    const list = filtered(dd.cat, dd.query);
    const cards = dd.cat === "all" && !dd.query ? FEATURED.map((s) => bySym[s]) : sortList(list, "vol", -1).slice(0, 4);
    $("#ddCards").innerHTML = cards.map((m) => `
      <div class="card" data-sym="${m.sym}" role="button">
        <div class="card-top">${iconHTML(m)}<span class="name">${esc(label(m))}</span><span class="lev-badge">${m.maxLev}×</span>
          <button class="star ${S.favorites.includes(m.sym) ? "on" : ""}" data-star="${m.sym}">${STAR}</button></div>
        <div class="card-price" data-c="price-${m.sym}">${fmtPrice(m.price)}</div>
        <div class="card-meta">Vol <span class="chip" data-c="vol-${m.sym}">${fmtCompact(m.vol24)}</span>
          <span class="chip ${m.chg24 >= 0 ? "pos" : "neg"}" data-c="chg-${m.sym}">${fmtPct(m.chg24)}</span></div>
      </div>`).join("");
    ddRows = sortList(list, dd.sort, dd.dir);
    dd.kb = clamp(dd.kb, -1, ddRows.length - 1);
    $("#ddBody").innerHTML = ddRows.length ? ddRows.map((m, i) => `
      <div class="dd-row ${i === dd.kb ? "kb" : ""}" data-sym="${m.sym}">
        <button class="star ${S.favorites.includes(m.sym) ? "on" : ""}" data-star="${m.sym}">${STAR}</button>
        <div class="mkt">${iconHTML(m)}<span class="nm">${esc(label(m))}</span><span class="lev-badge">${m.maxLev}×</span></div>
        <div class="num" data-c="price-${m.sym}">${fmtPrice(m.price)}</div>
        <div><span class="chip ${m.chg24 >= 0 ? "pos" : "neg"}" data-c="chg-${m.sym}">${fmtPct(m.chg24)}</span></div>
        <div class="num" data-c="oi-${m.sym}">${fmtCompact(m.oi)}</div>
        <div class="num" data-c="vol-${m.sym}">${fmtCompact(m.vol24)}</div>
      </div>`).join("") : `<div class="empty">No markets match “${esc(dd.query)}”</div>`;
    $$("#ddHead [data-sort]").forEach((b) => {
      b.classList.toggle("sorted", b.dataset.sort === dd.sort);
      b.innerHTML = b.textContent.replace(/[⌄⌃]/g, "").trim() + (b.dataset.sort === dd.sort ? ` <i>${dd.dir < 0 ? "⌄" : "⌃"}</i>` : "");
    });
    const totalVol = markets.reduce((a, m) => a + m.vol24, 0);
    $("#ddFoot").innerHTML = `<span>${list.length} markets</span><span>${fmtCompact(totalVol)} volume</span>`;
  }
  // In-place number refresh so clicks are never lost to a re-render.
  function refreshMarketCells(root) {
    for (const m of markets) {
      root.querySelectorAll(`[data-c="price-${m.sym}"]`).forEach((el) => (el.textContent = fmtPrice(m.price)));
      root.querySelectorAll(`[data-c="vol-${m.sym}"]`).forEach((el) => (el.textContent = fmtCompact(m.vol24)));
      root.querySelectorAll(`[data-c="oi-${m.sym}"]`).forEach((el) => (el.textContent = fmtCompact(m.oi)));
      root.querySelectorAll(`[data-c="chg-${m.sym}"]`).forEach((el) => {
        el.textContent = fmtPct(m.chg24);
        el.className = "chip " + (m.chg24 >= 0 ? "pos" : "neg");
      });
    }
  }
  function openDD() {
    if (U.page !== "trade") location.hash = "#trade";
    dd.open = true; $("#marketDD").hidden = false; renderDD();
  }
  function closeDD() {
    dd.open = false; $("#marketDD").hidden = true; dd.query = ""; dd.kb = -1;
    $("#searchInput").value = "";
  }
  function toggleFav(sym) {
    const i = S.favorites.indexOf(sym);
    if (i >= 0) S.favorites.splice(i, 1); else S.favorites.push(sym);
    save();
  }
  $("#marketPicker").addEventListener("click", (e) => { e.stopPropagation(); dd.open ? closeDD() : openDD(); });
  $("#marketDD").addEventListener("click", (e) => {
    e.stopPropagation();
    const st = e.target.closest("[data-star]");
    if (st) { toggleFav(st.dataset.star); renderDD(); if (U.page === "markets") renderMarketsPage(); return; }
    const c = e.target.closest("[data-cat]");
    if (c) { dd.cat = c.dataset.cat; dd.query = ""; $("#searchInput").value = ""; renderDD(); return; }
    const md = e.target.closest("[data-mode]");
    if (md) { dd.mode = md.dataset.mode; renderDD(); return; }
    const so = e.target.closest("[data-sort]");
    if (so) {
      if (dd.sort === so.dataset.sort) dd.dir *= -1; else { dd.sort = so.dataset.sort; dd.dir = so.dataset.sort === "name" ? 1 : -1; }
      renderDD(); return;
    }
    const r = e.target.closest("[data-sym]");
    if (r) { selectMarket(r.dataset.sym); closeDD(); }
  });
  document.addEventListener("click", (e) => {
    if (dd.open && !e.target.closest(".search")) closeDD();
    if (!e.target.closest(".avatar-wrap")) $("#avatarMenu").hidden = true;
  });

  const search = $("#searchInput");
  search.addEventListener("focus", () => { if (!dd.open) openDD(); });
  search.addEventListener("input", () => { dd.query = search.value; dd.kb = search.value ? 0 : -1; if (!dd.open) openDD(); else renderDD(); });
  search.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { dd.kb = Math.min(dd.kb + 1, ddRows.length - 1); renderDD(); e.preventDefault(); }
    else if (e.key === "ArrowUp") { dd.kb = Math.max(dd.kb - 1, 0); renderDD(); e.preventDefault(); }
    else if (e.key === "Enter" && ddRows[Math.max(dd.kb, 0)]) { selectMarket(ddRows[Math.max(dd.kb, 0)].sym); closeDD(); search.blur(); }
    else if (e.key === "Escape") { closeDD(); search.blur(); }
  });
  document.addEventListener("keydown", (e) => {
    const typing = /INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName);
    if (e.key === "/" && !typing) { e.preventDefault(); search.focus(); }
    if (e.key === "Escape") { closeDD(); $("#depositModal").hidden = true; }
  });

  // ───────────────────────── Market selection ─────────────────────────
  function selectMarket(sym) {
    if (!bySym[sym]) return;
    S.selected = sym;
    save();
    onMarketChange(true);
  }
  function onMarketChange(resetLev) {
    const m = sel();
    $("#selIcon").outerHTML = iconHTML(m, "lg").replace('class="mk-icon lg"', 'class="mk-icon lg" id="selIcon"');
    $("#opIcon").outerHTML = iconHTML(m).replace('class="mk-icon "', 'class="mk-icon" id="opIcon"');
    $("#selSym").textContent = m.sym;
    $("#opSym").textContent = m.sym;
    $("#selLev").textContent = m.maxLev + "×";
    if (resetLev) U.lev = m.maxLev;
    U.lev = clamp(U.lev, 1, m.maxLev);
    U.yMin = null;
    tape.length = 0; renderTape();
    if (orderType() === "limit") limitInput.value = m.price.toFixed(decimalsFor(m.price));
    loadRealCandles(m, U.range);
    loadRealCandles(m, "1d");
    loadRealCandles(m, "1m");
    renderSlider(); renderOrderPanel(); renderAbout(); renderPriceHeader(); renderOrderbook();
  }

  // ───────────────────────── Chart controls + tabs ─────────────────────────
  $("#ranges").addEventListener("click", (e) => {
    const b = e.target.closest("[data-range]");
    if (!b) return;
    U.range = b.dataset.range; U.yMin = null;
    $$("#ranges [data-range]").forEach((x) => x.classList.toggle("active", x === b));
    $(".range-select").firstChild.textContent = b.textContent + " ";
    loadRealCandles(sel(), U.range);
    renderPriceHeader();
  });
  $$(".chart-types button").forEach((b) => b.addEventListener("click", () => {
    U.ctype = b.dataset.ctype; U.yMin = null;
    $$(".chart-types button").forEach((x) => x.classList.toggle("active", x === b));
  }));
  function setTab(t) {
    U.tab = t;
    $$("#bottomTabs button").forEach((b) => b.classList.toggle("active", b.dataset.tab === t));
    ["about", "positions", "orders", "history"].forEach((k) => ($("#tab-" + k).hidden = k !== t));
  }
  $("#bottomTabs").addEventListener("click", (e) => { const b = e.target.closest("[data-tab]"); if (b) setTab(b.dataset.tab); });

  // ───────────────────────── Pages ─────────────────────────
  function sparkSVG(m) {
    const s = getSeries(m, "1d");
    const ps = s.filter((_, i) => i % 4 === 0 || i === s.length - 1).map((p) => p.p);
    const lo = Math.min(...ps), hi = Math.max(...ps), w = 120, h = 36;
    const pts = ps.map((p, i) => `${((i / (ps.length - 1)) * w).toFixed(1)},${(h - 3 - ((p - lo) / (hi - lo || 1)) * (h - 6)).toFixed(1)}`).join(" ");
    return `<svg class="spark" viewBox="0 0 ${w} ${h}"><polyline points="${pts}" fill="none" stroke="${ps.at(-1) >= ps[0] ? GREEN : RED}" stroke-width="1.6"/></svg>`;
  }
  function renderMarketsPage() {
    $("#mkCats").innerHTML = catButtons(U.mkCat);
    const list = sortList(filtered(U.mkCat, ""), "vol", -1);
    $("#mkTable").innerHTML = `<div class="dd-row dd-head"><span></span><span>Market</span><span>Last price</span><span>24h change</span><span>Open positions</span><span>Volume</span><span>24h</span></div>` +
      (list.length ? list.map((m) => `
      <div class="dd-row" data-open="${m.sym}">
        <button class="star ${S.favorites.includes(m.sym) ? "on" : ""}" data-star="${m.sym}">${STAR}</button>
        <div class="mkt">${iconHTML(m)}<span class="nm">${esc(m.name)}</span><span class="lev-badge">${m.maxLev}×</span></div>
        <div class="num" data-c="price-${m.sym}">${fmtPrice(m.price)}</div>
        <div><span class="chip ${m.chg24 >= 0 ? "pos" : "neg"}" data-c="chg-${m.sym}">${fmtPct(m.chg24)}</span></div>
        <div class="num" data-c="oi-${m.sym}">${fmtCompact(m.oi)}</div>
        <div class="num" data-c="vol-${m.sym}">${fmtCompact(m.vol24)}</div>
        <div data-spark="${m.sym}">${sparkSVG(m)}</div>
      </div>`).join("") : `<div class="empty">Star a market to add it to your favorites</div>`);
  }
  $("#page-markets").addEventListener("click", (e) => {
    const st = e.target.closest("[data-star]");
    if (st) { toggleFav(st.dataset.star); renderMarketsPage(); return; }
    const c = e.target.closest("[data-cat]");
    if (c) { U.mkCat = c.dataset.cat; renderMarketsPage(); return; }
    const r = e.target.closest("[data-open]");
    if (r) { selectMarket(r.dataset.open); location.hash = "#trade"; }
  });

  function renderSocialFeed(onlyNew) {
    const ul = $("#socialFeed");
    const item = (f) => {
      const c = AV_COLORS[f.who.length % AV_COLORS.length];
      const what = f.closing
        ? `closed <b>${f.m}</b> ${f.side} ${f.lev}×`
        : `opened <b>${f.m}</b> <span class="side-tag ${f.side}">${f.side === "long" ? "Long" : "Short"} ${f.lev}×</span>`;
      const amt = f.closing ? `<span class="amt ${f.pnl >= 0 ? "pos" : "neg"}">${fmtSigned(f.pnl)}</span>` : `<span class="amt">${fmtUsd(f.amt)}</span>`;
      return `<li><span class="uav" style="background:${c}">${f.who[0].toUpperCase()}</span><span class="who">${f.who}</span><span class="what">${what}</span>${amt}<time>${fmtTime(f.t)}</time></li>`;
    };
    if (onlyNew && ul.children.length) {
      ul.insertAdjacentHTML("afterbegin", item(feed[0]));
      while (ul.children.length > 40) ul.lastChild.remove();
    } else ul.innerHTML = feed.slice(0, 40).map(item).join("");
  }
  function renderLeaderboard() {
    leaders.forEach((l) => (l.pnl *= 1 + randn() * 0.01));
    const you = { who: "you", pnl: equity() - S.deposits, me: true };
    const all = [...leaders, you].sort((a, b) => b.pnl - a.pnl);
    $("#leaderboard").innerHTML = all.map((l, i) => `<li${l.me ? ' style="font-weight:700"' : ""}><span class="rank">${i + 1}</span><span class="uav" style="background:${l.me ? "#1c1c1a" : AV_COLORS[l.who.length % AV_COLORS.length]}">${l.who[0].toUpperCase()}</span><span class="who">${l.who}</span><span class="mono ${l.pnl >= 0 ? "pos" : "neg"}">${fmtSigned(l.pnl)}</span></li>`).join("");
  }

  function renderPortfolio() {
    const eq = equity();
    const upnl = S.positions.reduce((a, p) => a + pnlOf(p), 0);
    const realized = S.history.reduce((a, h) => a + h.pnl, 0);
    $("#pfSummary").innerHTML = [
      ["Portfolio value", fmtUsd(eq)], ["Cash", fmtUsd(S.cash)],
      ["Unrealized PnL", `<span class="${upnl >= 0 ? "pos" : "neg"}">${fmtSigned(upnl)}</span>`],
      ["Realized PnL", `<span class="${realized >= 0 ? "pos" : "neg"}">${fmtSigned(realized)}</span>`],
    ].map(([k, v]) => `<div><span>${k}</span><strong>${v}</strong></div>`).join("");
    drawEquity();
  }
  function drawEquity() {
    const c = $("#equityChart"), x = c.getContext("2d");
    const W = c.clientWidth, H = c.clientHeight, dpr = window.devicePixelRatio || 1;
    c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    const data = [...S.equity, { t: Date.now(), v: equity() }];
    x.clearRect(0, 0, W, H);
    x.font = '12px "JetBrains Mono", monospace'; x.fillStyle = "#8a8883";
    if (data.length < 3) { x.fillText("Your portfolio value will chart here as you trade.", 10, H / 2); return; }
    let lo = Math.min(...data.map((d) => d.v)), hi = Math.max(...data.map((d) => d.v));
    if (hi - lo < 1) { hi += 0.5; lo -= 0.5; }
    const t0 = data[0].t, t1 = data.at(-1).t;
    const X = (t) => ((t - t0) / (t1 - t0 || 1)) * (W - 90), Y = (v) => H - 20 - ((v - lo) / (hi - lo)) * (H - 40);
    const up = data.at(-1).v >= data[0].v;
    x.beginPath(); data.forEach((d, i) => (i ? x.lineTo(X(d.t), Y(d.v)) : x.moveTo(X(d.t), Y(d.v))));
    x.strokeStyle = up ? GREEN : RED; x.lineWidth = 2; x.stroke();
    x.lineTo(X(t1), H); x.lineTo(0, H); x.closePath(); x.fillStyle = up ? "rgba(46,139,103,0.12)" : "rgba(210,85,79,0.1)"; x.fill();
    x.fillStyle = "#8a8883"; x.fillText(fmtUsd(hi), W - 84, Y(hi) + 4); x.fillText(fmtUsd(lo), W - 84, Y(lo) + 4);
  }

  function accrueReferrals() {
    for (const r of S.referrals) {
      if (Math.random() < 0.08) {
        const rebate = Math.exp(randn() * 0.8 - 3);
        r.earned += rebate; S.refEarned += rebate; S.cash += rebate; S.deposits += rebate;
      }
    }
  }
  function renderReferrals() {
    $("#refLink").value = `${location.origin === "null" ? "https://helix.io" : location.origin}/?ref=${S.refCode}`;
    $("#refStats").innerHTML = [["Referred traders", S.referrals.length], ["Total earned", fmtUsd(S.refEarned)], ["Rebate rate", "10%"], ["Your code", S.refCode]]
      .map(([k, v]) => `<div><span>${k}</span><strong>${v}</strong></div>`).join("");
    $("#refList").innerHTML = S.referrals.map((r) => `<li><span>${r.who}</span><span>${fmtSigned(r.earned)}</span></li>`).join("");
  }
  $("#refCopy").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText($("#refLink").value); } catch { $("#refLink").select(); document.execCommand("copy"); }
    toast("Referral link copied", "good");
  });
  $("#refAdd").addEventListener("click", () => {
    S.referrals.push({ who: randomUser(), earned: 0, t: Date.now() });
    save(); renderReferrals(); toast("New trader joined with your link", "good");
  });

  function route() {
    const page = (location.hash || "#trade").slice(1);
    U.page = ["trade", "markets", "social", "portfolio", "referrals"].includes(page) ? page : "trade";
    $$(".page").forEach((p) => (p.hidden = p.id !== "page-" + U.page));
    $$(".mainnav a").forEach((a) => a.classList.toggle("active", a.dataset.nav === U.page));
    if (U.page !== "trade") closeDD();
    if (U.page === "markets") renderMarketsPage();
    if (U.page === "social") { renderSocialFeed(); renderLeaderboard(); }
    if (U.page === "portfolio") { renderTables(true); renderPortfolio(); }
    if (U.page === "referrals") renderReferrals();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);

  // ───────────────────────── Deposit + account ─────────────────────────
  const depModal = $("#depositModal");
  $("#depositBtn").addEventListener("click", () => { depModal.hidden = false; $("#depositInput").value = ""; $("#depositInput").focus(); });
  depModal.addEventListener("click", (e) => {
    if (e.target === depModal || e.target.closest("[data-close]")) depModal.hidden = true;
    const b = e.target.closest("[data-dep]");
    if (b) $("#depositInput").value = b.dataset.dep;
  });
  function doDeposit() {
    const v = num($("#depositInput"));
    if (!(v > 0)) return;
    const amt = Math.min(v, 1e7);
    S.cash += amt; S.deposits += amt; save();
    depModal.hidden = true;
    toast(`Deposited ${fmtUsd(amt)}`, "good");
    updateUI();
  }
  $("#depositConfirm").addEventListener("click", doDeposit);
  $("#depositInput").addEventListener("keydown", (e) => { if (e.key === "Enter") doDeposit(); });
  $("#avatarBtn").addEventListener("click", (e) => { e.stopPropagation(); $("#avatarMenu").hidden = !$("#avatarMenu").hidden; });
  $("#avatarMenu").addEventListener("click", (e) => {
    if (e.target.dataset.act === "reset" && confirm("Reset your demo account? Positions, orders and history will be cleared.")) {
      const fav = S.favorites;
      S = defaults(); S.favorites = fav; save();
      renderTables(true); onMarketChange(false); updateUI(); route();
      toast("Demo account reset");
    }
  });

  // ───────────────────────── Main UI update ─────────────────────────
  let slowTick = 0;
  function updateUI() {
    renderPriceHeader();
    renderOrderPanel();
    renderTables(false);
    if (U.page === "trade") maybeTape();
    if (dd.open) refreshMarketCells($("#marketDD"));
    renderOrderbook();
    slowTick++;
    if (slowTick % 5 === 0 && U.tab === "about") renderAbout();
    if (U.page === "markets") {
      refreshMarketCells($("#page-markets"));
      if (slowTick % 10 === 0) $$("[data-spark]").forEach((el) => (el.innerHTML = sparkSVG(bySym[el.dataset.spark])));
    }
    if (U.page === "portfolio") renderPortfolio();
    if (U.page === "social" && slowTick % 3 === 0) renderLeaderboard();
    if (U.page === "referrals" && slowTick % 3 === 0) renderReferrals();
  }

  // ───────────────────────── Boot ─────────────────────────
  markets.forEach((m) => { seedLive(m); getSeries(m, "1d"); });
  for (let i = 0; i < 12; i++) spawnSocial();
  U.lev = sel().maxLev;
  onMarketChange(false);
  renderTables(true);
  setTab("about");
  route();
  setInterval(tick, 1000);
  initAlpaca();
  window.addEventListener("resize", () => { if (U.page === "portfolio") drawEquity(); });
  requestAnimationFrame(frame);
})();
