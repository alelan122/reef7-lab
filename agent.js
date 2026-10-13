// Demo dell'agente vendite: una conversazione guidata che qualifica il visitatore e lo porta alla call.
// È una dimostrazione con risposte predefinite (il sito è statico): gli agenti che costruiamo usano l'AI vera.
(() => {
  if (document.body.dataset.page === "contact") return;
  const en = document.documentElement.lang === "en";
  const svcPage = en ? "services.html" : "servizi.html";
  const contactPage = en ? "contact.html" : "contatti.html";

  const T = en ? {
    open: "Talk to our AI agent", title: "Reef 7 agent", status: "Demo · online",
    hello: "Hi! I'm a demo of the sales agents we build. In 30 seconds I'll figure out how we can help you. What does your business need most?",
    goals: [
      ["sales", "More leads and sales", "Got it. Usually the bottleneck is response speed and follow-up: leads that wait go cold."],
      ["manual", "Less manual work", "Makes sense. Repetitive tasks are the first thing to hand over to automation, with or without AI."],
      ["data", "Numbers under control", "Clear. The goal is one view where sales, cash and margins are always up to date."],
      ["abroad", "Selling abroad", "Great. Languages, markets and foreign suppliers are where we can make a real difference."],
      ["unsure", "Not sure yet", "No problem, that's what the first call is for. Let's get the basics."],
    ],
    team_q: "How many people work at your company?", team: ["1-5", "6-20", "21-50", "50+"],
    when_q: "And when would you like to start?", when: ["Right away", "Within 1-3 months", "Within 6 months", "Just exploring"],
    sum: "Here's what I understood:", k_goal: "Goal", k_team: "Team", k_when: "Start", k_svc: "We'd suggest",
    close: "Next step: a free 30-minute strategy call. I've already filled in the form for you.",
    book: "Book the call", restart: "Start over",
    note: "This is a guided demo. The agents we build for you use real AI, connected to your CRM and calendar, on your website, WhatsApp and email.",
    svc: { "11": "AI sales agents", "03": "Custom CRM", "06": "Automation, with and without AI", "12": "AI voice assistants", "08": "Dashboards and financial control", "09": "Company hub and integrations", "15": "Multilingual websites", "16": "Italy-China bridge", "07": "Company brain" },
    need: { sales: ["CRM and sales", "AI agents and voice assistants"], manual: ["Automation (with or without AI)"], data: ["Dashboards and financial control"], abroad: ["Multilingual or China projects"], unsure: ["Not sure yet"] },
    typing: "typing",
  } : {
    open: "Parla con il nostro agente AI", title: "Agente Reef 7", status: "Demo · online",
    hello: "Ciao! Sono una demo degli agenti di vendita che costruiamo. In 30 secondi capisco come possiamo aiutarti. Di cosa ha più bisogno la tua azienda?",
    goals: [
      ["sales", "Più contatti e vendite", "Chiaro. Spesso il collo di bottiglia è la velocità di risposta e il follow-up: i contatti che aspettano si raffreddano."],
      ["manual", "Meno lavoro manuale", "Ha senso. Le attività ripetitive sono le prime da affidare all'automazione, con o senza AI."],
      ["data", "Numeri sotto controllo", "Capito. L'obiettivo è un'unica vista con vendite, cassa e margini sempre aggiornati."],
      ["abroad", "Vendere all'estero", "Ottimo. Lingue, mercati e fornitori esteri sono il terreno dove possiamo fare davvero la differenza."],
      ["unsure", "Non lo so ancora", "Nessun problema, la prima call serve proprio a questo. Partiamo dalle basi."],
    ],
    team_q: "Quante persone lavorano in azienda?", team: ["1-5", "6-20", "21-50", "Oltre 50"],
    when_q: "E quando vorresti partire?", when: ["Subito", "Entro 1-3 mesi", "Entro 6 mesi", "Sto valutando"],
    sum: "Ecco cosa ho capito:", k_goal: "Obiettivo", k_team: "Team", k_when: "Partenza", k_svc: "Ti consigliamo",
    close: "Prossimo passo: una call strategica gratuita di 30 minuti. Ho già compilato il modulo per te.",
    book: "Prenota la call", restart: "Ricomincia",
    note: "Questa è una demo guidata. Gli agenti che costruiamo per te usano l'AI vera, collegata al tuo CRM e al tuo calendario, su sito, WhatsApp ed email.",
    svc: { "11": "Agenti AI per le vendite", "03": "CRM su misura", "06": "Automazioni, con e senza AI", "12": "Assistenti vocali AI", "08": "Dashboard e controllo di gestione", "09": "Hub aziendale e integrazioni", "15": "Siti multilingue", "16": "Ponte Italia-Cina", "07": "Company brain" },
    need: { sales: ["CRM e vendite", "Agenti AI e assistenti vocali"], manual: ["Automazioni (con o senza AI)"], data: ["Dashboard e controllo di gestione"], abroad: ["Multilingue o progetti con la Cina"], unsure: ["Non lo so ancora"] },
    typing: "sta scrivendo",
  };
  const REC = { sales: ["11", "03"], manual: ["06", "12"], data: ["08", "09"], abroad: ["15", "16"], unsure: ["07", "11"] };

  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const launcher = el("button", "ag-launch", `<span class="ag-dot" aria-hidden="true"></span><span>${T.open}</span>`);
  launcher.type = "button";
  launcher.setAttribute("aria-expanded", "false");
  const panel = el("section", "ag-panel");
  panel.hidden = true;
  panel.setAttribute("aria-label", T.title);
  panel.innerHTML = `<header class="ag-head"><span class="ag-avatar" aria-hidden="true">R7</span><div><b>${T.title}</b><small>${T.status}</small></div>
    <button type="button" class="ag-x" aria-label="×">×</button></header>
    <div class="ag-log" role="log" aria-live="polite"></div><div class="ag-chips"></div>`;
  document.body.append(launcher, panel);
  const log = panel.querySelector(".ag-log"), chips = panel.querySelector(".ag-chips");
  const state = {};
  let started = false;

  const toggle = (open) => {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", open);
    launcher.classList.toggle("on", open);
    if (open && !started) { started = true; run(); }
  };
  launcher.addEventListener("click", () => toggle(panel.hidden));
  panel.querySelector(".ag-x").addEventListener("click", () => toggle(false));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) toggle(false); });

  const scroll = () => { log.scrollTop = log.scrollHeight; };
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const say = async (html, delay = 650) => {
    const t = el("div", "ag-msg bot ag-typing", `<i></i><i></i><i></i><span class="sr">${T.typing}</span>`);
    log.append(t); scroll();
    await wait(delay);
    t.className = "ag-msg bot"; t.innerHTML = html; scroll();
  };
  const me = (txt) => { log.append(el("div", "ag-msg me", txt)); scroll(); };
  const ask = (opts) => new Promise((resolve) => {
    chips.innerHTML = "";
    opts.forEach(([val, label]) => {
      const b = el("button", "ag-chip", label); b.type = "button";
      b.addEventListener("click", () => { chips.innerHTML = ""; me(label); resolve(val); });
      chips.append(b);
    });
  });

  async function run() {
    log.innerHTML = "";
    await say(T.hello, 500);
    const goal = await ask(T.goals.map(([k, l]) => [k, l]));
    const g = T.goals.find((x) => x[0] === goal);
    state.goal = goal; state.goalLabel = g[1];
    await say(g[2]);
    await say(T.team_q, 500);
    state.team = await ask(T.team.map((x) => [x, x]));
    await say(T.when_q);
    state.when = await ask(T.when.map((x) => [x, x]));
    const recs = REC[goal].map((id) => `<a href="${svcPage}#s${id}">${T.svc[id]}</a>`).join("");
    await say(`${T.sum}<dl class="ag-sum"><div><dt>${T.k_goal}</dt><dd>${state.goalLabel}</dd></div><div><dt>${T.k_team}</dt><dd>${state.team}</dd></div><div><dt>${T.k_when}</dt><dd>${state.when}</dd></div><div><dt>${T.k_svc}</dt><dd class="ag-recs">${recs}</dd></div></dl>`, 900);
    const q = new URLSearchParams({ need: T.need[goal].join("|"), team: state.team, when: state.when, goal: state.goalLabel });
    await say(`${T.close}<div class="ag-actions"><a class="ag-book" href="${contactPage}?${q}#contact-form">${T.book} →</a><button type="button" class="ag-again">${T.restart}</button></div><p class="ag-note">${T.note}</p>`);
    log.querySelector(".ag-again")?.addEventListener("click", run);
  }
})();
