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

  // [chiave, attività, quota automatizzabile (ipotesi prudente), servizio, cosa costruiremmo]
  const TASKS = en ? [
    ["leads", "Replying to enquiries and new leads", 0.6, "11", "An AI agent that replies instantly on your website, WhatsApp and email, qualifies the lead and books the call."],
    ["data", "Copying data between tools and spreadsheets", 0.8, "09", "Connecting your tools so data is entered once and reaches everywhere it's needed."],
    ["reports", "Putting together reports and numbers", 0.75, "08", "A dashboard that updates itself with sales, cash and margins."],
    ["booking", "Booking appointments and sending reminders", 0.7, "04", "Online bookings assigned to the right person, with automatic confirmations and reminders."],
    ["followup", "Follow-ups and emails to customers", 0.65, "05", "Email sequences that go out at the right moment based on what each contact does."],
    ["docs", "Quotes, invoices and documents", 0.5, "06", "Documents generated automatically from the data you already have, ready to check and send."],
    ["questions", "Looking up information and answering internal questions", 0.5, "07", "A company brain: everything your company knows, one question away."],
    ["support", "Repetitive customer support", 0.5, "11", "An AI assistant that answers frequent questions and hands delicate cases to a person."],
    ["orders", "Managing orders, shipments and returns", 0.6, "09", "Orders, shipments and returns tracked in one view, with automatic customer updates."],
    ["phone", "Answering the phone and calling back", 0.5, "12", "A voice assistant that answers, books and calls back the people you missed."],
  ] : [
    ["leads", "Rispondere a richieste e nuovi contatti", 0.6, "11", "Un agente AI che risponde subito su sito, WhatsApp ed email, qualifica il contatto e fissa la call."],
    ["data", "Copiare dati tra programmi e fogli Excel", 0.8, "09", "Collegare i tuoi strumenti, così un dato si inserisce una volta sola e arriva ovunque serva."],
    ["reports", "Preparare report e numeri", 0.75, "08", "Una dashboard che si aggiorna da sola con vendite, cassa e margini."],
    ["booking", "Fissare appuntamenti e mandare promemoria", 0.7, "04", "Prenotazioni online assegnate alla persona giusta, con conferme e promemoria automatici."],
    ["followup", "Follow-up ed email ai clienti", 0.65, "05", "Sequenze email che partono al momento giusto in base a cosa fa ogni contatto."],
    ["docs", "Preventivi, fatture e documenti", 0.5, "06", "Documenti generati in automatico dai dati che hai già, pronti da controllare e inviare."],
    ["questions", "Cercare informazioni e rispondere a domande interne", 0.5, "07", "Un company brain: tutto quello che sa la tua azienda, a una domanda di distanza."],
    ["support", "Assistenza clienti ripetitiva", 0.5, "11", "Un assistente AI che risponde alle domande frequenti e passa a una persona i casi delicati."],
    ["orders", "Gestire ordini, spedizioni e resi", 0.6, "09", "Ordini, spedizioni e resi tracciati in un'unica vista, con aggiornamenti automatici ai clienti."],
    ["phone", "Rispondere al telefono e richiamare", 0.5, "12", "Un assistente vocale che risponde, prenota e richiama chi non sei riuscito a sentire."],
  ];
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
    plan_build: (x) => `I build the first solution, starting from “${x}”, connected to the tools you already use. Then we add the rest one piece at a time.`,
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
    plan_build: (x) => `Costruisco la prima soluzione, partendo da “${x}”, collegata agli strumenti che usate già. Poi aggiungiamo il resto un pezzo alla volta.`,
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

  const EFFORT = { leads: 1, data: 1, reports: 0, booking: 0, followup: 0, docs: 1, questions: 2, support: 1, orders: 1, phone: 2 };
  // dati di contesto mostrati in base alle attività scelte
  const statsFor = (a) => {
    const k = new Set(a.tasks.map((t) => t.key)), out = [];
    if (k.has("leads") || k.has("support") || k.has("phone")) out.push("speed");
    if (k.has("data") || k.has("orders") || k.has("docs")) out.push("data");
    if (out.length < 2) out.push("rep");
    out.push(a.team === T.teams[3] ? "mck" : "it");
    return out.map((x) => T.stats[x]);
  };
  const tierOf = (h) => (h >= 15 ? 2 : h >= 6 ? 1 : 0);
  const ICON = {
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
  const money = (n) => (en ? "€" : "") + (Math.round(n / 100) * 100).toLocaleString(en ? "en-GB" : "it-IT") + (en ? "" : " €");
  const pills = (name, opts, type = "radio") => `<div class="picks">${opts.map((o, i) => `<label class="pick"><input type="${type}" name="${name}" value="${i}"><span>${esc(o)}</span></label>`).join("")}</div>`;

  root.innerHTML = `
  <div class="au-layout">
  <div class="form-card au-card">
    <ol class="au-stepper">${T.steps.map((x, i) => `<li><span>${i + 1}</span><b>${x}</b></li>`).join("")}</ol>
    <form class="au-form" novalidate>
      <fieldset class="au-step" data-i="0">
        <div class="q-field" data-req="sector"><p class="q-label">${T.sector}</p>${pills("sector", T.sectors)}</div>
        <div class="q-field" data-req="team"><p class="q-label">${T.team}</p>${pills("team", T.teams)}</div>
      </fieldset>
      <fieldset class="au-step" data-i="1" hidden>
        <p class="q-label">${T.tasks_q}<small>${T.tasks_hint}</small></p>
        <div class="au-tasks">${TASKS.map(([k, label], i) => `
          <div class="au-task" data-i="${i}">
            <label class="au-check"><input type="checkbox" name="task" value="${i}"><i class="au-ico">${icon(k)}</i><span>${esc(label)}</span></label>
            <div class="au-hours"><input type="range" min="1" max="40" step="1" value="5" aria-label="${esc(label)} · ${T.hours}"><output>5</output><small>${T.hours}</small></div>
          </div>`).join("")}</div>
      </fieldset>
      <fieldset class="au-step" data-i="2" hidden>
        <div class="q-field"><p class="q-label">${T.tools_q}<small>${T.tools_hint}</small></p>${pills("tool", TOOLS.map((t) => t[1]), "checkbox")}</div>
        <label class="field"><span>${T.pain}</span><textarea name="pain" rows="3" maxlength="500" placeholder="${T.pain_ph}"></textarea></label>
        <label class="field au-cost"><span>${T.cost}</span><input name="cost" type="number" min="0" max="500" inputmode="decimal" placeholder="${T.cost_ph}"><small>${T.cost_hint}</small></label>
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
  form.querySelectorAll(".au-task").forEach((row) => {
    const box = row.querySelector("input[type=checkbox]"), range = row.querySelector("input[type=range]"), out = row.querySelector("output");
    const sync = () => { row.classList.toggle("on", box.checked); range.disabled = !box.checked; };
    box.addEventListener("change", sync);
    range.addEventListener("input", () => { out.textContent = range.value; });
    sync();
  });
  form.addEventListener("change", (e) => e.target.closest(".q-field")?.classList.remove("invalid"));

  const valid = () => {
    if (cur === 0) {
      let ok = true;
      steps[0].querySelectorAll("[data-req]").forEach((g) => { const bad = !g.querySelector("input:checked"); g.classList.toggle("invalid", bad); if (bad) ok = false; });
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
      const t = TASKS[+row.dataset.i], h = +row.querySelector("input[type=range]").value;
      return { key: t[0], label: t[1], f: t[2], svc: t[3], build: t[4], hours: h, saved: h * t[2] };
    }).sort((a, b) => b.saved - a.saved);
    const saved = tasks.reduce((s, t) => s + t.saved, 0);
    const cost = Math.max(0, parseFloat(f.get("cost")) || 0);
    return {
      sector: T.sectors[+f.get("sector")], team: T.teams[+f.get("team")], tasks, saved,
      tools: f.getAll("tool").map((i) => TOOLS[+i]), pain: (f.get("pain") || "").toString().trim(), cost,
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
      `<div><span>${icon(t.key)}${esc(t.label)}</span><i><b style="width:${(t.saved / max) * 100}%"></b></i><em>${fmt(t.saved)}</em></div>`).join("");
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
    const first = a.tasks[0].label;
    return [T.plan_call, T.plan_build(first.charAt(0).toLowerCase() + first.slice(1)), T.plan_measure];
  };
  const mailText = (a, name) => {
    const plan = planOf(a), L = [];
    L.push(T.mail_intro(name), "");
    L.push(`${fmt(a.saved)} ${T.k_week} · ${Math.round((a.saved * WEEKS) / 8)} ${T.k_year}` + (a.cost ? ` · ${money(a.saved * WEEKS * a.cost)} ${T.k_value}` : ""), "");
    L.push(`${T.pot}: ${Math.round((a.saved / a.tasks.reduce((x, t) => x + t.hours, 0)) * 100)}% · ${T.tier[tierOf(a.saved)][0]}. ${T.tier[tierOf(a.saved)][1]}`, "");
    L.push(T.r_tasks.toUpperCase());
    a.tasks.forEach((t) => L.push(`- ${t.label}: ${fmt(t.hours)} ${T.r_now}, ${fmt(t.saved)} ${T.r_saved}`));
    L.push("", T.r_prio.toUpperCase());
    a.tasks.slice(0, 3).forEach((t, i) => L.push(`${i + 1}. ${t.label}: ${t.build}`));
    L.push("", T.r_plan.toUpperCase());
    plan.forEach((x, i) => L.push(`${i + 1}. ${x}`));
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
          _autoresponse: mailText(a, name), "Fonte": "Audit di automazione", "Nome": name, email, "Azienda": company || "—", "Settore": a.sector, "Persone in azienda": a.team,
          "Attività manuali (ore/sett.)": a.tasks.map((t) => `${t.label}: ${t.hours}`).join("; "),
          "Ore recuperabili stimate a settimana": fmt(a.saved), "Priorità": a.tasks.slice(0, 3).map((t) => t.label).join("; "),
          "Strumenti": a.tools.map((t) => t[1]).join(", ") || "—", "Problema principale": a.pain || "—", "Costo orario": a.cost || "—",
          "Codice Reef 7": r7code({ ch: "audit", name, email, company, sector: a.sector, team: a.team, saved: a.saved, tasks: a.tasks.map((t) => [t.label, t.hours]), tools: a.tools.map((t) => t[1]), pain: a.pain || "", cost: a.cost || "" }),
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
        <p class="au-r-meta">${esc(a.sector)} · ${esc(a.team)} ${en ? "people" : "persone"}</p>
      </header>
      ${sentOk ? `<p class="au-ok">${T.sent_ok(esc(who.email))}</p>` : `<p class="au-warn">${T.sent_fail.replace("{email}", `<a href="mailto:${MAIL}">${MAIL}</a>`)}</p>`}
      <div class="au-sum">
        <div class="au-sum-txt"><p class="mono">${T.sum_k}</p>
          <p class="au-sum-v"><b>${T.tier[tier][0]}</b> · ${T.tier[tier][1]}</p>
          <p class="au-sum-first"><span class="mono">${T.sum_first}</span>${esc(top[0].label)}: ${esc(top[0].build)}</p></div>
        <div class="au-gauge" style="--p:${pct}"><b>${pct}%</b><span>${T.pot}</span></div>
      </div>
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
        <ol class="au-prio">${top.map((t) => `<li><b>${esc(t.label)}</b><em class="au-eff e${EFFORT[t.key]}">${T.effort[EFFORT[t.key]]}</em><p><span class="mono">${T.r_build}</span>${esc(t.build)} <a href="${svcPage}#s${t.svc}">→</a></p></li>`).join("")}</ol>
      </section>
      <section><h3>${T.r_plan}</h3>
        <ol class="au-plan">${plan.map((p, i) => `<li><span class="mono">${T.plan[i]}</span><p>${esc(p)}</p></li>`).join("")}</ol>
      </section>
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
