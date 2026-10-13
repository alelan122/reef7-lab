// Audit di automazione: tre passi di domande, stima delle ore recuperabili, report completo in cambio dell'email.
// Le stime usano ipotesi prudenti per ogni attività e sono dichiarate nel report.
(() => {
  const root = document.getElementById("audit");
  if (!root) return;
  const en = document.documentElement.lang === "en";
  const svcPage = en ? "services.html" : "servizi.html";
  const contactPage = en ? "contact.html" : "contatti.html";
  const endpoint = `https://formsubmit.co/ajax/${(window.REEF && window.REEF.email) || "lancioni.ale@gmail.com"}`;
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
    teaser_p: "Get the full report: priorities, what to automate first and a 3-step plan, also as a PDF.",
    name: "Name", email: "Work email", company: "Company", consent: "I agree to Reef 7 Lab using these details to send me the report and get back to me.",
    unlock: "See the full report", sending: "Preparing…", bad_email: "Check the email address.", need_consent: "Consent is needed to send the report.",
    r_title: "Automation report", r_for: "for", k_week: "hours a week", k_year: "working days a year", k_value: "a year in time value",
    r_tasks: "Where the time goes", r_now: "h today", r_saved: "recoverable", r_prio: "What to automate first", r_build: "What we would build",
    r_plan: "A plan in 3 steps", plan: ["First step", "Second step", "Third step"],
    plan_connect: "Connect the tools you already use, so data flows on its own and nobody copies it by hand.",
    plan_measure: "Measure the results with a dashboard: hours saved, response times and sales, always up to date.",
    r_tools: "Notes on your tools", r_pain: "You told us", r_note: "Indicative estimate based on your answers and on conservative assumptions about how much of each activity can be automated (shown next to each one). We check the real numbers together, with your data.",
    pdf: "Download PDF", call: "Book a free call", restart: "Start over", sent_fail: "We couldn't send your details, but here's your report anyway.",
    auto: (p) => `automatable: about ${p}%`, subject: "New automation audit",
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
    teaser_p: "Ricevi il report completo: priorità, cosa automatizzare per primo e un piano in 3 passi, anche in PDF.",
    name: "Nome", email: "Email di lavoro", company: "Azienda", consent: "Acconsento a che Reef 7 Lab usi questi dati per inviarmi il report e ricontattarmi.",
    unlock: "Vedi il report completo", sending: "Preparo il report…", bad_email: "Controlla l'indirizzo email.", need_consent: "Serve il consenso per inviarti il report.",
    r_title: "Report di automazione", r_for: "per", k_week: "ore a settimana", k_year: "giornate lavorative l'anno", k_value: "l'anno di valore del tempo",
    r_tasks: "Dove va il tempo", r_now: "ore oggi", r_saved: "recuperabili", r_prio: "Cosa automatizzare per primo", r_build: "Cosa costruiremmo",
    r_plan: "Un piano in 3 passi", plan: ["Primo passo", "Secondo passo", "Terzo passo"],
    plan_connect: "Collegare gli strumenti che usate già, così i dati scorrono da soli e nessuno li copia più a mano.",
    plan_measure: "Misurare i risultati con una dashboard: ore risparmiate, tempi di risposta e vendite, sempre aggiornati.",
    r_tools: "Note sui vostri strumenti", r_pain: "Ci hai detto", r_note: "Stima indicativa basata sulle tue risposte e su ipotesi prudenti su quanto di ogni attività si può automatizzare (indicato accanto a ciascuna). I numeri reali li verifichiamo insieme, sui tuoi dati.",
    pdf: "Scarica il PDF", call: "Prenota una call gratuita", restart: "Ricomincia", sent_fail: "Non siamo riusciti a inviare i tuoi dati, ma ecco comunque il tuo report.",
    auto: (p) => `automatizzabile: circa il ${p}%`, subject: "Nuovo audit di automazione",
  };

  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const fmt = (n) => (Math.round(n * 2) / 2).toLocaleString(en ? "en-GB" : "it-IT");
  const money = (n) => (en ? "€" : "") + (Math.round(n / 100) * 100).toLocaleString(en ? "en-GB" : "it-IT") + (en ? "" : " €");
  const pills = (name, opts, type = "radio") => `<div class="picks">${opts.map((o, i) => `<label class="pick"><input type="${type}" name="${name}" value="${i}"><span>${esc(o)}</span></label>`).join("")}</div>`;

  root.innerHTML = `
  <div class="form-card au-card">
    <div class="q-progress"><span class="q-count"></span><span class="q-name"></span><i><b></b></i></div>
    <form class="au-form" novalidate>
      <fieldset class="au-step" data-i="0">
        <div class="q-field" data-req="sector"><p class="q-label">${T.sector}</p>${pills("sector", T.sectors)}</div>
        <div class="q-field" data-req="team"><p class="q-label">${T.team}</p>${pills("team", T.teams)}</div>
      </fieldset>
      <fieldset class="au-step" data-i="1" hidden>
        <p class="q-label">${T.tasks_q}<small>${T.tasks_hint}</small></p>
        <div class="au-tasks">${TASKS.map(([k, label], i) => `
          <div class="au-task" data-i="${i}">
            <label class="au-check"><input type="checkbox" name="task" value="${i}"><span>${esc(label)}</span></label>
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
  <article class="au-report" hidden></article>`;

  const card = root.querySelector(".au-card"), form = root.querySelector(".au-form");
  const steps = [...form.querySelectorAll(".au-step")];
  const back = form.querySelector(".au-back"), next = form.querySelector(".au-next"), msg = form.querySelector(".au-msg");
  const gate = root.querySelector(".au-gate"), lead = root.querySelector(".au-lead"), report = root.querySelector(".au-report");
  let cur = 0;

  const progress = (i) => {
    card.querySelector(".q-count").textContent = T.step_of.replace("{a}", i + 1).replace("{b}", 4);
    card.querySelector(".q-name").textContent = T.steps[i];
    card.querySelector(".q-progress b").style.width = `${((i + 1) / 4) * 100}%`;
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
          "Fonte": "Audit di automazione", "Nome": name, "Email": email, "Azienda": company || "—", "Settore": a.sector, "Persone in azienda": a.team,
          "Attività manuali (ore/sett.)": a.tasks.map((t) => `${t.label}: ${t.hours}`).join("; "),
          "Ore recuperabili stimate a settimana": fmt(a.saved), "Priorità": a.tasks.slice(0, 3).map((t) => t.label).join("; "),
          "Strumenti": a.tools.map((t) => t[1]).join(", ") || "—", "Problema principale": a.pain || "—", "Costo orario": a.cost || "—",
        }),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || out.success === false || out.success === "false") throw new Error();
    } catch { ok = false; }
    renderReport(a, { name, company }, ok);
  });

  function renderReport(a, who, sentOk) {
    card.hidden = true;
    const top = a.tasks.slice(0, 3);
    const max = Math.max(...a.tasks.map((t) => t.hours));
    const date = new Date().toLocaleDateString(en ? "en-GB" : "it-IT", { day: "numeric", month: "long", year: "numeric" });
    const days = (a.saved * WEEKS) / 8;
    const many = a.tools.length >= 3 || a.tasks.some((t) => t.key === "data" || t.key === "orders");
    const plan = [top[0].build, many && top[0].svc !== "09" ? T.plan_connect : (top[1] ? top[1].build : T.plan_connect), top[2] && !many ? top[2].build : T.plan_measure];
    const q = new URLSearchParams({ need: "", team: a.team, goal: `${T.r_title}: ${fmt(a.saved)} ${T.k_week}` });
    report.innerHTML = `
      <header class="au-r-head">
        <p class="mono">Reef 7 Lab · ${date}</p>
        <h2>${T.r_title}${who.company ? ` <em>${T.r_for} ${esc(who.company)}</em>` : ""}</h2>
        <p class="au-r-meta">${esc(a.sector)} · ${esc(a.team)} ${en ? "people" : "persone"}</p>
      </header>
      ${sentOk ? "" : `<p class="au-warn">${T.sent_fail}</p>`}
      <div class="au-kpis">
        <div><b>${fmt(a.saved)}</b><span>${T.k_week}</span></div>
        <div><b>${Math.round(days).toLocaleString(en ? "en-GB" : "it-IT")}</b><span>${T.k_year}</span></div>
        ${a.cost ? `<div><b>${money(a.saved * WEEKS * a.cost)}</b><span>${T.k_value}</span></div>` : ""}
      </div>
      <section><h3>${T.r_tasks}</h3>
        <div class="au-bars">${a.tasks.map((t) => `
          <div class="au-bar"><p>${esc(t.label)}<small>${T.auto(Math.round(t.f * 100))}</small></p>
            <div class="au-track"><i style="width:${(t.hours / max) * 100}%"></i><b style="width:${(t.saved / max) * 100}%"></b></div>
            <span>${fmt(t.hours)} ${T.r_now} · <strong>${fmt(t.saved)} ${T.r_saved}</strong></span></div>`).join("")}</div>
      </section>
      <section><h3>${T.r_prio}</h3>
        <ol class="au-prio">${top.map((t) => `<li><b>${esc(t.label)}</b><p><span class="mono">${T.r_build}</span>${esc(t.build)} <a href="${svcPage}#s${t.svc}">→</a></p></li>`).join("")}</ol>
      </section>
      <section><h3>${T.r_plan}</h3>
        <ol class="au-plan">${plan.map((p, i) => `<li><span class="mono">${T.plan[i]}</span><p>${esc(p)}</p></li>`).join("")}</ol>
      </section>
      ${a.tools.length ? `<section><h3>${T.r_tools}</h3><ul class="au-tools">${a.tools.map((t) => `<li><b>${esc(t[1])}</b> ${esc(t[2])}</li>`).join("")}</ul></section>` : ""}
      ${a.pain ? `<section><h3>${T.r_pain}</h3><blockquote>“${esc(a.pain)}”</blockquote></section>` : ""}
      <p class="au-note">${T.r_note}</p>
      <div class="au-actions"><a class="btn" href="${contactPage}?${q}#contact-form">${T.call} →</a><button type="button" class="btn ghost au-pdf">${T.pdf}</button><button type="button" class="btn ghost au-restart">${T.restart}</button></div>`;
    report.hidden = false;
    report.querySelector(".au-pdf").addEventListener("click", () => window.print());
    report.querySelector(".au-restart").addEventListener("click", () => location.reload());
    report.scrollIntoView({ block: "start", behavior: "smooth" });
  }

  show(0);
})();
