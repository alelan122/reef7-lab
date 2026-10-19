// Audit di automazione: tre passi di domande, stima delle ore recuperabili, report completo in cambio dell'email.
// Le stime usano ipotesi prudenti per ogni attività e sono dichiarate nel report.
(() => {
  const root = document.getElementById("audit");
  if (!root) return;
  const en = document.documentElement.lang === "en";
  const svcPage = en ? "services.html" : "servizi.html";
  const contactPage = en ? "contact.html" : "contatti.html";
  const endpoint = `https://formsubmit.co/ajax/${(window.REEF && window.REEF.email) || "lancioni.ale@gmail.com"}`;
  const MAIL = (window.REEF && window.REEF.email) || "lancioni.ale@gmail.com";
  const base = en ? "../" : "";
  const WEEKS = 46; // settimane lavorative in un anno

  // attività e soluzioni per settore: vedi audit-data.js
  const D = window.R7_AUDIT[en ? "en" : "it"];
  let si = D.sectors.length - 1, TASKS = D.sectors[si].tasks;
  const TOOLS = en ? [
    ["excel", "Excel or Google Sheets", "Spreadsheets are often the first bottleneck: moving that data into a database or a custom CRM removes errors and conflicting versions."],
    ["whatsapp", "WhatsApp", "On WhatsApp, an AI agent can reply to and qualify leads even outside office hours."],
    ["email", "Gmail or Outlook", "Repetitive emails are among the first things to automate, keeping your tone of voice."],
    ["crm", "A CRM (HubSpot, Salesforce…)", "Your CRM can be connected to your other tools, or replaced by one built around your process."],
    ["shopify", "Shopify or another e-commerce", "Orders, ad spend and costs can flow into a single dashboard showing your real margin."],
    ["calendly", "Calendly or a booking tool", "Bookings can be assigned automatically to the right person and land straight in the CRM."],
    ["erp", "Management or accounting software", "Your management software can become the heart of your data once it's connected to everything else."],
    ["paper", "Paper and notebooks", "Starting from paper is an advantage: the right system can be designed from scratch."],
  ] : [
    ["excel", "Excel o Google Fogli", "I fogli di calcolo sono spesso il primo collo di bottiglia: portare quei dati in un database o in un CRM su misura toglie errori e versioni diverse."],
    ["whatsapp", "WhatsApp", "Su WhatsApp un agente AI può rispondere e qualificare i contatti anche fuori orario."],
    ["email", "Gmail o Outlook", "Le email ripetitive sono tra le prime cose da automatizzare, mantenendo il tuo tono di voce."],
    ["crm", "Un CRM (HubSpot, Salesforce…)", "Il CRM che usi può essere collegato agli altri strumenti, oppure sostituito da uno costruito sul tuo processo."],
    ["shopify", "Shopify o un altro e-commerce", "Ordini, spese pubblicitarie e costi possono finire in un'unica dashboard con il margine reale."],
    ["calendly", "Calendly o un sistema di prenotazione", "Le prenotazioni possono essere assegnate in automatico alla persona giusta e finire direttamente nel CRM."],
    ["erp", "Gestionale o software di contabilità", "Il gestionale può diventare il centro dei dati, una volta collegato a tutto il resto."],
    ["paper", "Carta e quaderni", "Partire dalla carta è un vantaggio: il sistema giusto si può progettare da zero."],
  ];
  const T = en ? {
    steps: ["Your company", "Manual work", "Tools", "Your report"], step_of: "Step {a} of {b}",
    sector: "What industry are you in?", sectors: ["E-commerce", "Professional services", "Education and coaching", "B2B sales", "Local business", "Other"],
    team: "How many people work at the company?", teams: ["1-5", "6-20", "21-50", "50+"],
    tasks_q: "What does your team still do by hand?", tasks_hint: "Select the activities and estimate the weekly hours for the whole team.",
    hours: "h/week", tools_q: "Which tools do you use today?", tools_hint: "Pick all that apply.",
    pain: "What's the most frustrating thing in your day-to-day? (optional)", pain_ph: "E.g. we lose leads because we reply too late",
    cost: "Average hourly cost of a team member (optional)", cost_ph: "E.g. 25", cost_hint: "Used only to estimate the value of the time saved.",
    next: "Next", back: "Back", calc: "Calculate", need_task: "Select at least one activity.", need_pick: "Choose an option.",
    teaser_k: "Your estimate", teaser: (h) => `Your team could win back about <b>${h} hours a week</b>.`,
    teaser_p: "Get the full report: priorities, what to automate first and a 3-step plan. You'll see it right away, as a PDF too, and I'll send you a copy by email.",
    name: "Name", email: "Work email", company: "Company", consent: "I agree to Reef 7 Lab using these details to send me a copy of the report and get back to me.",
    unlock: "See the full report", sending: "Preparing…", bad_email: "Check the email address.", need_consent: "Consent is needed to send the report.",
    r_title: "Automation report", r_for: "for", k_week: "hours a week", k_year: "working days a year", k_value: "a year in time value",
    r_tasks: "Where the time goes", r_now: "h today", r_saved: "recoverable", r_prio: "What to automate first", r_build: "What I would build",
    r_plan: "A plan in 3 steps", plan: ["First step", "Second step", "Third step"],
    plan_measure: "Measure the results with a dashboard: hours saved, response times and sales, always up to date.",
    plan_call: "A free 30-minute call: we go through this report on your real numbers and choose where to start.",
    plan_build: (x, sol) => `I build the first solution, starting from “${x}”, connected to the tools you already use: ${sol.charAt(0).toLowerCase() + sol.slice(1)}`,
    r_tools: "Notes on your tools", r_pain: "You told me", r_note: "Indicative estimate based on your answers and on conservative assumptions about how much of each activity can be automated (shown next to each one). We'll check the real numbers together, on your data.",
    pdf: "Download PDF", call: "Book a free call", restart: "Start over", sent_fail: "Your details didn't reach me, so no copy was sent by email. Download the PDF or write to me at {email} and I'll get back to you.",
    sent_ok: (e) => `A copy is on its way to <b>${e}</b>.`,
    sign_h: "I'll write to you myself", sign_p: "I read every report personally. Within one business day you'll get an email from me with first ideas on where to start.", sign_n: "Alessandro Lancioni · Founder, Reef 7 Lab",
    mail_intro: (n) => `Hi ${n},\n\nhere is a copy of your automation report from Reef 7 Lab.`, mail_end: "I read every report personally: within one business day I'll write to you with first ideas on where to start.\n\nAlessandro Lancioni\nReef 7 Lab", mail_link: "Redo the audit or book a call:",
    auto: (p) => `automatable: about ${p}%`, subject: "New automation audit",
    live_k: "Live estimate", live_empty: "Select the activities your team does by hand: the estimate updates as you go.",
    sum_k: "In short", sum_first: "First move", fte: (x) => `about ${x} full-time ${x === "1" ? "person" : "people"}`, month: (h, v) => `Every month as things are: about ${h} hours of manual work${v ? `, worth ${v}` : ""}.`,
    tier: [["Contained", "The margin is contained: it's worth starting from one simple automation and measuring it."], ["Concrete", "The margin is concrete: one or two targeted changes are enough to feel the difference."], ["High", "The margin is wide: it's worth starting soon from the first priority."]],
    pot: "Automation potential", effort: ["Quick win", "Medium project", "Structured project"],
    ctx_h: "The context", src: "Sources",
    stats: {
      speed: ["~7×", "Companies that follow up on a lead within an hour are nearly 7 times more likely to reach a decision maker than those that wait one more hour.", "Harvard Business Review, “The Short Life of Online Sales Leads”, 2011"],
      data: ["9+ h", "In a survey of 500 professionals, manually moving data from emails, PDFs and spreadsheets takes over 9 hours a week per person.", "Parseur / QuestionPro survey, 2025 (vendor study)"],
      rep: ["40%+", "Over 40% of workers spend at least a quarter of their week on manual, repetitive tasks.", "Smartsheet, automation in the workplace survey"],
      it: ["15.7%", "In Italy only 15.7% of SMEs use at least one AI technology (in Germany, 26% of companies): starting now is still an advantage.", "Istat, Imprese e ICT, 2025"],
      mck: ["~30%", "By 2030, automation could cover about 30% of hours worked.", "McKinsey Global Institute, Generative AI and the future of work in America, 2023"],
    },
    next_h: "The next step", next_p: "Book a free 30-minute call: we go through this report together, on your real numbers.",
    live_get: "What you'll get", get: ["Hours and value you could win back", "What to automate first", "A 3-step plan, also as a PDF"],
  } : {
    steps: ["La tua azienda", "Lavoro manuale", "Strumenti", "Il tuo report"], step_of: "Passo {a} di {b}",
    sector: "In che settore lavori?", sectors: ["E-commerce", "Studio o consulenza", "Formazione e coaching", "Vendita B2B", "Attività locale", "Altro"],
    team: "Quante persone lavorano in azienda?", teams: ["1-5", "6-20", "21-50", "Oltre 50"],
    tasks_q: "Cosa fa ancora a mano il tuo team?", tasks_hint: "Seleziona le attività e stima le ore a settimana per tutto il team.",
    hours: "ore/sett.", tools_q: "Quali strumenti usate oggi?", tools_hint: "Scegli tutti quelli che usate.",
    pain: "Qual è la cosa più frustrante nel lavoro di tutti i giorni? (facoltativo)", pain_ph: "Es. perdiamo contatti perché rispondiamo troppo tardi",
    cost: "Costo orario medio di una persona del team (facoltativo)", cost_ph: "Es. 25", cost_hint: "Serve solo a stimare il valore del tempo recuperato.",
    next: "Avanti", back: "Indietro", calc: "Calcola", need_task: "Seleziona almeno un'attività.", need_pick: "Scegli un'opzione.",
    teaser_k: "La tua stima", teaser: (h) => `Il tuo team potrebbe recuperare circa <b>${h} ore a settimana</b>.`,
    teaser_p: "Ricevi il report completo: priorità, cosa automatizzare per primo e un piano in 3 passi. Lo vedi subito, anche in PDF, e te ne mando una copia per email.",
    name: "Nome", email: "Email di lavoro", company: "Azienda", consent: "Acconsento a che Reef 7 Lab usi questi dati per inviarmi una copia del report e ricontattarmi.",
    unlock: "Vedi il report completo", sending: "Preparo il report…", bad_email: "Controlla l'indirizzo email.", need_consent: "Serve il consenso per inviarti il report.",
    r_title: "Report di automazione", r_for: "per", k_week: "ore a settimana", k_year: "giornate lavorative l'anno", k_value: "l'anno di valore del tempo",
    r_tasks: "Dove va il tempo", r_now: "ore oggi", r_saved: "recuperabili", r_prio: "Cosa automatizzare per primo", r_build: "Cosa costruirei",
    r_plan: "Un piano in 3 passi", plan: ["Primo passo", "Secondo passo", "Terzo passo"],
    plan_measure: "Misuriamo i risultati con una dashboard: ore risparmiate, tempi di risposta e vendite, sempre aggiornati.",
    plan_call: "Una call gratuita di 30 minuti: guardiamo questo report sui tuoi numeri reali e scegliamo da dove partire.",
    plan_build: (x, sol) => `Costruisco la prima soluzione, partendo da “${x}”, collegata agli strumenti che usate già: ${sol.charAt(0).toLowerCase() + sol.slice(1)}`,
    r_tools: "Note sui vostri strumenti", r_pain: "Mi hai detto", r_note: "Stima indicativa basata sulle tue risposte e su ipotesi prudenti su quanto di ogni attività si può automatizzare (indicato accanto a ciascuna). I numeri reali li verifichiamo insieme, sui tuoi dati.",
    pdf: "Scarica il PDF", call: "Prenota una call gratuita", restart: "Ricomincia", sent_fail: "I tuoi dati non mi sono arrivati, quindi la copia per email non è partita. Scarica il PDF oppure scrivimi a {email} e ti rispondo io.",
    sent_ok: (e) => `Una copia sta arrivando a <b>${e}</b>.`,
    sign_h: "Ti scrivo io", sign_p: "Leggo ogni report personalmente. Entro un giorno lavorativo ricevi una mia email con le prime idee su da dove partire.", sign_n: "Alessandro Lancioni · Fondatore di Reef 7 Lab",
    mail_intro: (n) => `Ciao ${n},\n\necco la copia del tuo report di automazione di Reef 7 Lab.`, mail_end: "Leggo ogni report personalmente: entro un giorno lavorativo ti scrivo con le prime idee su da dove partire.\n\nAlessandro Lancioni\nReef 7 Lab", mail_link: "Rifai l'audit o prenota una call:",
    auto: (p) => `automatizzabile: circa il ${p}%`, subject: "Nuovo audit di automazione",
    live_k: "Stima in diretta", live_empty: "Seleziona le attività che il tuo team fa a mano: la stima si aggiorna mentre scegli.",
    sum_k: "In sintesi", sum_first: "La prima mossa", fte: (x) => `circa ${x} ${x === "1" ? "persona" : "persone"} a tempo pieno`, month: (h, v) => `Ogni mese, restando così: circa ${h} ore di lavoro manuale${v ? `, per un valore di ${v}` : ""}.`,
    tier: [["Contenuto", "Il margine è contenuto: conviene partire da una sola automazione semplice e misurarla."], ["Concreto", "Il margine è concreto: uno o due interventi mirati bastano per vedere la differenza."], ["Alto", "Il margine è ampio: conviene partire presto dalla prima priorità."]],
    pot: "Potenziale di automazione", effort: ["Vittoria rapida", "Progetto medio", "Progetto strutturato"],
    ctx_h: "Il contesto", src: "Fonti",
    stats: {
      speed: ["~7×", "Le aziende che ricontattano un contatto entro un'ora hanno quasi 7 volte più probabilità di parlare con chi decide rispetto a chi aspetta un'ora in più.", "Harvard Business Review, “The Short Life of Online Sales Leads”, 2011"],
      data: ["9+ ore", "In un sondaggio su 500 professionisti, spostare a mano dati da email, PDF e fogli di calcolo occupa più di 9 ore a settimana a persona.", "Sondaggio Parseur / QuestionPro, 2025 (studio di un fornitore)"],
      rep: ["40%+", "Oltre il 40% dei lavoratori passa almeno un quarto della settimana in attività manuali e ripetitive.", "Smartsheet, sondaggio sull'automazione nel lavoro"],
      it: ["15,7%", "In Italia solo il 15,7% delle PMI usa almeno una tecnologia di intelligenza artificiale (in Germania il 26% delle imprese): chi parte ora parte ancora in vantaggio.", "Istat, Imprese e ICT, 2025"],
      mck: ["~30%", "Entro il 2030 l'automazione potrebbe coprire circa il 30% delle ore lavorate.", "McKinsey Global Institute, Generative AI and the future of work in America, 2023"],
    },
    next_h: "Il prossimo passo", next_p: "Prenota una call gratuita di 30 minuti: guardiamo insieme questo report, sui tuoi numeri reali.",
    live_get: "Cosa ricevi", get: ["Ore e valore che puoi recuperare", "Cosa automatizzare per primo", "Un piano in 3 passi, anche in PDF"],
  };

  // dati di contesto mostrati in base alle attività scelte
  const statsFor = (a) => {
    const k = new Set(a.tasks.map((t) => t.icon)), out = [];
    const subI = a.sub ? (D.subs[a.si] || []).indexOf(a.sub) : -1;
    const ONLY = { 1: [0], 2: [1] }; // dato legale solo per gli studi legali, dato corsi solo per i corsi online
    const own = ONLY[a.si] && subI >= 0 && !ONLY[a.si].includes(subI) ? null : D.sectors[a.si].stat;
    if (k.has("leads") || k.has("support") || k.has("phone")) out.push("speed");
    if (k.has("data") || k.has("orders") || k.has("docs")) out.push("data");
    if (out.length < 2) out.push("rep");
    out.push(a.ti === 3 || en ? "mck" : "it");
    const list = out.map((x) => T.stats[x]);
    return (own ? [own, ...list] : list).slice(0, 3);
  };
  const recsOf = (a) => {
    const have = new Set(a.tasks.slice(0, 3).map((t) => t.svc)), out = [];
    const add = (x) => { if (!have.has(x) && !out.includes(x) && D.svc[x] && !(x === "25" && a.ti === 0)) out.push(x); };
    const BY_SUB = {
      0: [["19", "23", "18"], ["21", "23", "18"], ["14", "23", "19"], ["23", "19", "18"]],
      1: [["07", "17", "12"], ["17", "24", "06"], ["17", "08", "06"], ["12", "04", "18"]],
      2: [["11", "23", "24"], ["27", "24", "05"], ["27", "24", "04"]],
      3: [["19", "03", "17"], ["17", "19", "03"], ["03", "23", "11"]],
      4: [["12", "18", "04"], ["18", "04", "05"], ["18", "01", "05"], ["12", "04", "18"]],
    };
    const GOAL = [["23", "11", "18"], ["20", "10", "21"], ["06", "08", "07", "25"], ["17", "07", "11"]];
    const subI = a.sub ? (D.subs[a.si] || []).indexOf(a.sub) : -1;
    const heavy = a.sw >= 2 || a.spend >= 2;
    if (a.gi === 1) add("20");
    (BY_SUB[a.si] ? BY_SUB[a.si][subI >= 0 ? subI : 0] : ["08", "06"]).forEach(add);
    if (heavy) add("20");
    if (a.gi >= 0) GOAL[a.gi].forEach(add);
    if (heavy) add("10");
    if (a.ti >= 2) add("26");
    return out.slice(0, 3);
  };
  const tierOf = (h) => (h >= 15 ? 2 : h >= 6 ? 1 : 0);
  // soluzione su misura o rapida, in base a dimensione del team e ore in gioco
  const custom = (ti, h) => ti >= 2 || (ti === 1 && h >= 10) || h >= 15;
  const ICON = {
    star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2-5.5-2.9-5.5 2.9 1-6.2L3 9.6l6.2-.9z"/>',
    leads: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    data: '<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M4 16V5a1 1 0 0 1 1-1h11"/>',
    reports: '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    booking: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
    followup: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    docs: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    questions: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    support: '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2" y="14" width="5" height="6" rx="2"/><rect x="17" y="14" width="5" height="6" rx="2"/>',
    orders: '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
  };
  const icon = (k) => `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${ICON[k]}</svg>`;
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const fmt = (n) => (Math.round(n * 2) / 2).toLocaleString(en ? "en-GB" : "it-IT");
  const money = (n) => (en ? "€" : "") + String(Math.round(n / 100) * 100).replace(/\B(?=(\d{3})+(?!\d))/g, en ? "," : ".") + (en ? "" : " €");
  const pills = (name, opts, type = "radio") => `<div class="picks">${opts.map((o, i) => `<label class="pick"><input type="${type}" name="${name}" value="${i}"><span>${esc(o)}</span></label>`).join("")}</div>`;

  root.innerHTML = `
  <div class="au-layout">
  <div class="form-card au-card">
    <ol class="au-stepper">${T.steps.map((x, i) => `<li><span>${i + 1}</span><b>${x}</b></li>`).join("")}</ol>
    <form class="au-form" novalidate>
      <fieldset class="au-step" data-i="0">
        <div class="q-field" data-req="sector"><p class="q-label">${T.sector}</p>${pills("sector", T.sectors)}</div>
        <div class="q-field au-sub" data-req="sub" hidden><p class="q-label">${D.sub_q}</p><div class="au-sub-picks"></div></div>
        <div class="q-field" data-req="team"><p class="q-label">${T.team}</p>${pills("team", T.teams)}</div>
        <div class="q-field" data-req="goal"><p class="q-label">${D.goal_q}</p>${pills("goal", D.goals)}</div>
      </fieldset>
      <fieldset class="au-step" data-i="1" hidden>
        <p class="q-label">${T.tasks_q}<small>${T.tasks_hint}</small></p>
        <div class="au-tasks"></div>
      </fieldset>
      <fieldset class="au-step" data-i="2" hidden>
        <div class="q-field"><p class="q-label">${T.tools_q}<small>${T.tools_hint}</small></p>${pills("tool", TOOLS.map((t) => t[1]), "checkbox")}</div>
        <div class="q-field"><p class="q-label">${D.sw_q}</p>${pills("sw", D.sw)}</div>
        <div class="q-field"><p class="q-label">${D.spend_q}</p>${pills("spend", D.spend)}</div>
        <label class="field"><span>${T.pain}</span><textarea name="pain" rows="3" maxlength="500" placeholder="${T.pain_ph}"></textarea></label>
        <label class="field au-cost"><span>${T.cost}</span><input name="cost" type="number" min="0" max="500" inputmode="decimal" placeholder="${T.cost_ph}"><small>${T.cost_hint}</small></label>
        <label class="field"><span>${D.site_q}</span><input name="site" type="text" maxlength="200" autocomplete="url" placeholder="${D.site_ph}"><small>${D.site_hint}</small></label>
      </fieldset>
      <div class="q-nav"><button type="button" class="btn ghost au-back" hidden>${T.back}</button><button type="button" class="btn au-next">${T.next} →</button></div>
      <p class="form-msg au-msg" role="status" aria-live="polite"></p>
    </form>
    <div class="au-gate" hidden>
      <p class="mono">${T.teaser_k}</p><h2 class="au-teaser"></h2><p class="au-teaser-p">${T.teaser_p}</p>
      <form class="au-lead" novalidate>
        <label class="field"><span>${T.name}</span><input name="name" required autocomplete="name"></label>
        <label class="field"><span>${T.company}</span><input name="company" autocomplete="organization"></label>
        <label class="field full"><span>${T.email}</span><input name="email" type="email" required autocomplete="email"></label>
        <label class="check full"><input type="checkbox" name="consent" required><span>${T.consent}</span></label>
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button type="submit" class="btn full">${T.unlock} →</button>
        <p class="form-msg full au-msg2" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
  <aside class="au-live" aria-live="polite">
    <p class="mono">${T.live_k}</p>
    <div class="au-live-num"><b>0</b><span>${T.k_week}</span></div>
    <p class="au-live-days"><b>0</b> ${T.k_year}</p>
    <div class="au-live-bars"></div>
    <p class="au-live-empty">${T.live_empty}</p>
    <div class="au-live-get"><p class="mono">${T.live_get}</p><ul>${T.get.map((x) => `<li>${x}</li>`).join("")}</ul></div>
  </aside>
  </div>
  <article class="au-report" hidden></article>`;

  const card = root.querySelector(".au-card"), form = root.querySelector(".au-form");
  const steps = [...form.querySelectorAll(".au-step")];
  const back = form.querySelector(".au-back"), next = form.querySelector(".au-next"), msg = form.querySelector(".au-msg");
  const gate = root.querySelector(".au-gate"), lead = root.querySelector(".au-lead"), report = root.querySelector(".au-report");
  let cur = 0;

  const progress = (i) => {
    card.querySelectorAll(".au-stepper li").forEach((li, j) => { li.classList.toggle("done", j < i); li.classList.toggle("now", j === i); });
    root.classList.toggle("live-on", i >= 1);
  };
  const show = (i) => {
    cur = i;
    steps.forEach((s, j) => { s.hidden = j !== i; });
    back.hidden = i === 0;
    next.textContent = (i === steps.length - 1 ? T.calc : T.next) + " →";
    msg.textContent = "";
    progress(i);
  };

  // ore per attività: il cursore si attiva quando l'attività è selezionata
  const renderTasks = (i) => {
    si = i; TASKS = D.sectors[i].tasks;
    const box = form.querySelector(".au-tasks");
    box.innerHTML = TASKS.map((t, j) => `
      <div class="au-task" data-i="${j}">
        <label class="au-check"><input type="checkbox" name="task" value="${j}"><i class="au-ico">${icon(t[1])}</i><span>${esc(t[2])}</span></label>
        <div class="au-hours"><input type="range" min="1" max="40" step="1" value="5" aria-label="${esc(t[2])} · ${T.hours}"><output>5</output><small>${T.hours}</small></div>
      </div>`).join("");
    box.querySelectorAll(".au-task").forEach((row) => {
      const cb = row.querySelector("input[type=checkbox]"), range = row.querySelector("input[type=range]"), out = row.querySelector("output");
      const sync = () => { row.classList.toggle("on", cb.checked); range.disabled = !cb.checked; };
      cb.addEventListener("change", sync);
      range.addEventListener("input", () => { out.textContent = range.value; });
      sync();
    });
  };
  renderTasks(si);
  const subBox = form.querySelector(".au-sub");
  form.querySelectorAll('input[name="sector"]').forEach((r) => r.addEventListener("change", () => {
    const list = D.subs[+r.value] || [];
    subBox.hidden = !list.length;
    subBox.classList.remove("invalid");
    subBox.querySelector(".au-sub-picks").innerHTML = list.length ? pills("sub", list.map((x) => x[0])) : "";
  }));
  form.addEventListener("change", (e) => e.target.closest(".q-field")?.classList.remove("invalid"));

  const valid = () => {
    if (cur === 0) {
      let ok = true;
      steps[0].querySelectorAll("[data-req]").forEach((g) => { if (g.hidden) return; const bad = !g.querySelector("input:checked"); g.classList.toggle("invalid", bad); if (bad) ok = false; });
      if (!ok) msg.textContent = T.need_pick;
      return ok;
    }
    if (cur === 1 && !form.querySelector('input[name="task"]:checked')) { msg.textContent = T.need_task; return false; }
    return true;
  };

  // calcolo: ore recuperabili per attività, ordinate dalla più grande
  const answers = () => {
    const f = new FormData(form);
    const tasks = [...form.querySelectorAll(".au-task.on")].map((row) => {
      const t = TASKS[+row.dataset.i], h = +row.querySelector("input[type=range]").value, ti = +new FormData(form).get("team");
      const c = custom(ti, h);
      return { key: t[0], icon: t[1], label: t[2], f: t[3], svc: t[4], eff: t[5], light: t[6], full: t[7], kpi: t[8], custom: c, build: c ? t[7] : t[6], hours: h, saved: h * t[3] };
    });
    // l'obiettivo pesa sull'ordine: le attività che lo servono salgono
    const gi = f.get("goal") === null ? -1 : +f.get("goal");
    const GOAL_OF = { leads: [0, 3], followup: [0], star: [0], booking: [0, 3], data: [1, 2], reports: [1, 2], docs: [1, 2], orders: [1, 2], support: [3, 2], questions: [2, 3], phone: [3, 0] };
    const w = (t) => t.saved * ((GOAL_OF[t.icon] || []).includes(gi) ? 1.6 : 1);
    tasks.sort((a, b) => w(b) - w(a));
    const saved = tasks.reduce((s, t) => s + t.saved, 0);
    const cost = Math.max(0, parseFloat(f.get("cost")) || 0);
    return {
      si: +f.get("sector"), ti: +f.get("team"), sector: T.sectors[+f.get("sector")], team: T.teams[+f.get("team")], tasks, saved,
      tools: f.getAll("tool").map((i) => TOOLS[+i]), pain: (f.get("pain") || "").toString().trim(), cost,
      sub: f.get("sub") === null ? null : (D.subs[+f.get("sector")] || [])[+f.get("sub")] || null, gi,
      sw: f.get("sw") === null ? -1 : +f.get("sw"), spend: f.get("spend") === null ? -1 : +f.get("spend"),
      site: (f.get("site") || "").toString().trim().slice(0, 200),
    };
  };

  const live = root.querySelector(".au-live");
  let shown = 0, raf = null;
  const updateLive = () => {
    const a = answers();
    const target = a.saved;
    live.classList.toggle("has", a.tasks.length > 0);
    live.querySelector(".au-live-days b").textContent = Math.round((target * WEEKS) / 8).toLocaleString(en ? "en-GB" : "it-IT");
    const max = Math.max(1, ...a.tasks.map((t) => t.hours));
    live.querySelector(".au-live-bars").innerHTML = a.tasks.slice(0, 4).map((t) =>
      `<div><span>${icon(t.icon)}${esc(t.label)}</span><i><b style="width:${(t.saved / max) * 100}%"></b></i><em>${fmt(t.saved)}</em></div>`).join("");
    cancelAnimationFrame(raf);
    const from = shown, t0 = performance.now();
    const step = (now) => {
      const k = Math.min(1, (now - t0) / 450), e = 1 - Math.pow(1 - k, 3);
      shown = from + (target - from) * e;
      live.querySelector(".au-live-num b").textContent = fmt(shown);
      if (k < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  };
  form.addEventListener("input", updateLive);
  form.addEventListener("change", updateLive);

  next.addEventListener("click", () => {
    if (!valid()) return;
    if (cur === 0) { const ns = +new FormData(form).get("sector"); if (ns !== si) { renderTasks(ns); updateLive(); } }
    if (cur < steps.length - 1) { show(cur + 1); card.scrollIntoView({ block: "nearest", behavior: "smooth" }); return; }
    const a = answers();
    form.hidden = true;
    gate.hidden = false;
    progress(3);
    gate.querySelector(".au-teaser").innerHTML = T.teaser(fmt(a.saved));
    lead.querySelector("input").focus();
  });
  back.addEventListener("click", () => show(cur - 1));

  // piano in 3 passi: usato nel report a schermo e nella copia per email
  const planOf = (a) => {
    const first = a.tasks[0].label, kpis = a.tasks.slice(0, 2).map((t) => t.kpi).join(en ? " and " : " e ");
    return [T.plan_call, T.plan_build(first.charAt(0).toLowerCase() + first.slice(1), a.tasks[0].build), D.measure(kpis)];
  };
  const mailText = (a, name) => {
    const plan = planOf(a), L = [];
    L.push(T.mail_intro(name), "", `${D.sector_k} (${a.sector}, ${a.team}): ${D.sectors[a.si].intro}`, "");
    L.push(`${fmt(a.saved)} ${T.k_week} · ${Math.round((a.saved * WEEKS) / 8)} ${T.k_year}` + (a.cost ? ` · ${money(a.saved * WEEKS * a.cost)} ${T.k_value}` : ""), "");
    L.push(`${T.pot}: ${Math.round((a.saved / a.tasks.reduce((x, t) => x + t.hours, 0)) * 100)}% · ${T.tier[tierOf(a.saved)][0]}. ${T.tier[tierOf(a.saved)][1]}`, "");
    if (a.gi >= 0) L.push(D.goal_line[a.gi], "");
    L.push(T.r_tasks.toUpperCase());
    a.tasks.forEach((t) => L.push(`- ${t.label}: ${fmt(t.hours)} ${T.r_now}, ${fmt(t.saved)} ${T.r_saved}`));
    L.push("", T.r_prio.toUpperCase());
    a.tasks.slice(0, 3).forEach((t, i) => L.push(`${i + 1}. ${t.label}`, `   ${D.opt[0]}: ${t.light}`, `   ${D.opt[1]}: ${t.full}`, `   ${D.rec}: ${D.opt[t.custom ? 1 : 0].toLowerCase()} · ${D.kpi}: ${t.kpi}`));
    L.push("", T.r_plan.toUpperCase());
    plan.forEach((x, i) => L.push(`${i + 1}. ${x}`));
    const rc = recsOf(a);
    if (rc.length) { L.push("", D.rec_h.toUpperCase()); rc.forEach((x) => L.push(`- ${D.svc[x][0]}: ${D.svc[x][1]}`)); }
    L.push("", T.r_note, "", T.mail_end, "", `${T.mail_link} ${location.href.split("#")[0]}`);
    return L.join("\n");
  };
  const r7code = (o) => "R7L1." + btoa(unescape(encodeURIComponent(JSON.stringify({ v: 1, lang: document.documentElement.lang || "it", at: new Date().toISOString(), ...o })))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  lead.addEventListener("submit", async (e) => {
    e.preventDefault();
    const m2 = lead.querySelector(".au-msg2");
    const f = new FormData(lead);
    if (f.get("_honey")) return;
    const email = (f.get("email") || "").toString().trim(), name = (f.get("name") || "").toString().trim();
    if (!name) { lead.name.focus(); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { m2.textContent = T.bad_email; lead.email.focus(); return; }
    if (!lead.consent.checked) { m2.textContent = T.need_consent; return; }
    const a = answers();
    const company = (f.get("company") || "").toString().trim();
    const btn = lead.querySelector("button");
    btn.disabled = true; btn.textContent = T.sending; m2.textContent = "";
    let ok = true;
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `${T.subject}: ${company || name} · ${fmt(a.saved)} h/sett.`, _replyto: email, _template: "table", _captcha: "false",
          _autoresponse: mailText(a, name), "Fonte": "Audit di automazione", "Nome": name, email, "Azienda": company || "—", "Settore": a.sector, "Dettaglio settore": a.sub ? a.sub[0] : "—", "Persone in azienda": a.team, "Obiettivo": a.gi >= 0 ? D.goals[a.gi] : "—",
          "Software usati": a.sw >= 0 ? D.sw[a.sw] : "—", "Spesa software al mese": a.spend >= 0 ? D.spend[a.spend] : "—", "Sito": a.site || "—",
          "Attività manuali (ore/sett.)": a.tasks.map((t) => `${t.label}: ${t.hours}`).join("; "),
          "Ore recuperabili stimate a settimana": fmt(a.saved), "Priorità": a.tasks.slice(0, 3).map((t) => t.label).join("; "),
          "Strumenti": a.tools.map((t) => t[1]).join(", ") || "—", "Problema principale": a.pain || "—", "Costo orario": a.cost || "—",
          "Codice Reef 7": r7code({ ch: "audit", name, email, company, sector: a.sector + (a.sub ? ` · ${a.sub[0]}` : ""), team: a.team, site: a.site, goal: a.gi >= 0 ? D.goals[a.gi] : "", saved: a.saved, tasks: a.tasks.map((t) => [t.label, t.hours]), tools: a.tools.map((t) => t[1]), pain: a.pain || "", cost: a.cost || "" }),
        }),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || out.success === false || out.success === "false") throw new Error();
    } catch { ok = false; }
    renderReport(a, { name, company, email }, ok);
  });

  function renderReport(a, who, sentOk) {
    card.hidden = true;
    root.querySelector(".au-layout").hidden = true;
    root.classList.remove("live-on");
    const top = a.tasks.slice(0, 3);
    const max = Math.max(...a.tasks.map((t) => t.hours));
    const date = new Date().toLocaleDateString(en ? "en-GB" : "it-IT", { day: "numeric", month: "long", year: "numeric" });
    const days = (a.saved * WEEKS) / 8;
    const plan = planOf(a);
    const total = a.tasks.reduce((x, t) => x + t.hours, 0), pct = Math.round((a.saved / total) * 100);
    const tier = tierOf(a.saved), fte = (Math.round((a.saved / 40) * 10) / 10).toLocaleString(en ? "en-GB" : "it-IT");
    const perMonth = a.saved * 4.33, stats = statsFor(a);
    const contact = new URL(contactPage, location.href).href.split("?")[0];
    const q = new URLSearchParams({ need: "", team: a.team, goal: `${T.r_title}: ${fmt(a.saved)} ${T.k_week}` });
    report.innerHTML = `
      <header class="au-r-head">
        <p class="au-r-brand"><img src="${base}assets/logo-68.png" alt="" width="28" height="28"><b>Reef 7 Lab</b><span class="mono">${date}</span></p>
        <h2>${T.r_title}${who.company ? ` <em>${T.r_for} ${esc(who.company)}</em>` : ""}</h2>
        <p class="au-r-meta">${esc(a.sector)}${a.sub && a.sub[1] !== undefined && a.sub[0] !== (en ? "Other" : "Altro") ? ` · ${esc(a.sub[0])}` : ""} · ${esc(a.team)} ${en ? "people" : "persone"}${a.site ? ` · ${esc(a.site)}` : ""}</p>
      </header>
      ${sentOk ? `<p class="au-ok">${T.sent_ok(esc(who.email))}</p>` : `<p class="au-warn">${T.sent_fail.replace("{email}", `<a href="mailto:${MAIL}">${MAIL}</a>`)}</p>`}
      <div class="au-sum">
        <div class="au-sum-txt"><p class="mono">${T.sum_k}</p>
          <p class="au-sum-v"><b>${T.tier[tier][0]}</b> · ${T.tier[tier][1]}</p>
          <p class="au-sum-first"><span class="mono">${T.sum_first}</span>${esc(top[0].label)}: ${esc(top[0].build.charAt(0).toLowerCase() + top[0].build.slice(1))}</p>
          <a class="btn au-sum-cta" href="${contactPage}?${q}#contact-form">${D.cta_top} →</a></div>
        <div class="au-gauge" style="--p:${pct}"><b>${pct}%</b><span>${T.pot}</span></div>
      </div>
      <div class="au-sector"><p class="mono">${D.sector_k} · ${esc(a.sector)} · ${esc(a.team)} ${en ? "people" : "persone"}</p><p>${D.sectors[a.si].intro}${a.sub && a.sub[1] ? " " + a.sub[1] : ""}</p><p class="au-scope">${D.scope[a.ti]}</p>${a.gi >= 0 ? `<p class="au-goal">${D.goal_line[a.gi]}</p>` : ""}</div>
      <div class="au-kpis">
        <div><b>${fmt(a.saved)}</b><span>${T.k_week}</span></div>
        <div><b>${Math.round(days).toLocaleString(en ? "en-GB" : "it-IT")}</b><span>${T.k_year}</span></div>
        ${a.cost ? "" : `<div><b>${fte}</b><span>${T.fte(fte).replace(fte + " ", "")}</span></div>`}
        ${a.cost ? `<div><b>${money(a.saved * WEEKS * a.cost)}</b><span>${T.k_value}</span></div>` : ""}
      </div>
      <p class="au-month">${T.month(fmt(perMonth), a.cost ? money(perMonth * a.cost) : "")} ${en ? "That's" : "Equivale a"} ${T.fte(fte)}.</p>
      <section><h3>${T.r_tasks}</h3>
        <div class="au-bars">${a.tasks.map((t) => `
          <div class="au-bar"><p>${esc(t.label)}<small>${T.auto(Math.round(t.f * 100))}</small></p>
            <div class="au-track"><i style="width:${(t.hours / max) * 100}%"></i><b style="width:${(t.saved / max) * 100}%"></b></div>
            <span>${fmt(t.hours)} ${T.r_now} · <strong>${fmt(t.saved)} ${T.r_saved}</strong></span></div>`).join("")}</div>
      </section>
      <section><h3>${T.r_prio}</h3>
        <ol class="au-prio">${top.map((t) => `<li><b>${esc(t.label)}</b><em class="au-eff e${t.custom ? t.eff : Math.max(0, t.eff - 1)}">${T.effort[t.custom ? t.eff : Math.max(0, t.eff - 1)]}</em>
          <div class="au-opts">${[t.light, t.full].map((x, j) => `<div class="au-opt${t.custom === !!j ? " rec" : ""}"><span class="mono">${D.opt[j]}${t.custom === !!j ? ` · ${D.rec}` : ""}</span><p>${esc(x)}</p></div>`).join("")}</div>
          <p class="au-why">${D.why[t.custom ? 1 : 0]} <span>${D.kpi}: ${esc(t.kpi)}.</span> <a href="${svcPage}#s${t.svc}">${en ? "See the service" : "Vedi il servizio"} →</a></p></li>`).join("")}</ol>
      </section>
      <section><h3>${T.r_plan}</h3>
        <ol class="au-plan">${plan.map((p, i) => `<li><span class="mono">${T.plan[i]}</span><p>${esc(p)}</p></li>`).join("")}</ol>
      </section>
      ${a.sw >= 0 || a.spend >= 0 ? `<section><h3>${D.sw_h}</h3><p class="au-swp">${D.sw_line(a.sw >= 0 ? D.sw[a.sw] : "", a.spend >= 0 ? D.spend[a.spend] : "")} ${a.sw >= 2 || a.spend >= 2 ? D.sw_many : a.sw === 1 || a.spend === 1 ? D.sw_mid : D.sw_few}</p></section>` : ""}
      ${(() => { const r = recsOf(a); return r.length ? `<section><h3>${D.rec_h}</h3><div class="au-recs">${r.map((x) => `<a class="au-rec" href="${svcPage}#s${x}"><b>${D.svc[x][0]}</b><p>${D.svc[x][1]}</p></a>`).join("")}</div></section>` : ""; })()}
      <section><h3>${T.ctx_h}</h3>
        <div class="au-ctx">${stats.map((x, i) => `<div><b>${x[0]}</b><p>${x[1]}<sup>${i + 1}</sup></p></div>`).join("")}</div>
      </section>
      ${a.tools.length ? `<section><h3>${T.r_tools}</h3><ul class="au-tools">${a.tools.map((t) => `<li><b>${esc(t[1])}</b> ${esc(t[2])}</li>`).join("")}</ul></section>` : ""}
      ${a.pain ? `<section><h3>${T.r_pain}</h3><blockquote>“${esc(a.pain)}”</blockquote></section>` : ""}
      <div class="au-sign"><img src="${base}assets/alessandro.jpg" alt="" width="72" height="72"><div><b>${T.sign_h}</b><p>${T.sign_p}</p><span>${T.sign_n} · ${MAIL}</span></div></div>
      <div class="au-next"><div><p class="mono">${T.next_h}</p><p>${T.next_p}</p></div><a class="btn" href="${contactPage}?${q}#contact-form">${T.call} →</a><span class="au-next-url">${contact}</span></div>
      <p class="au-note">${T.r_note}</p>
      <p class="au-src"><b>${T.src}</b> ${stats.map((x, i) => `${i + 1}. ${x[2]}`).join(" · ")}</p>
      <div class="au-actions"><a class="btn" href="${contactPage}?${q}#contact-form">${T.call} →</a><button type="button" class="btn ghost au-pdf">${T.pdf}</button><button type="button" class="btn ghost au-restart">${T.restart}</button></div>`;
    report.hidden = false;
    report.querySelector(".au-pdf").addEventListener("click", () => window.print());
    report.querySelector(".au-restart").addEventListener("click", () => location.reload());
    report.scrollIntoView({ block: "start", behavior: "smooth" });
  }

  show(0);
})();
