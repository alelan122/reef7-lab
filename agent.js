// Demo dell'agente vendite: qualifica il visitatore, consiglia servizi e un progetto simile, e raccoglie il contatto.
// Il sito è statico, quindi capisce il testo libero con regole semplici: gli agenti che costruiamo per i clienti usano l'AI vera.
(() => {
  if (document.body.dataset.page === "contact") return;
  const en = document.documentElement.lang === "en";
  const svcPage = en ? "services.html" : "servizi.html";
  const workPage = en ? "work.html" : "lavori.html";
  const contactPage = en ? "contact.html" : "contatti.html";
  const endpoint = `https://formsubmit.co/ajax/${(window.REEF && window.REEF.email) || "lancioni.ale@gmail.com"}`;

  const T = en ? {
    open: "Talk to our AI agent", title: "Reef 7 agent", status: "Demo · replies in seconds", ph: "Type a message…", send: "Send",
    teaser: "Want to find out in 30 seconds what we could automate in your business?",
    hello: "Hi! I'm a demo of the sales agents we build. I'll ask you a few quick questions and tell you how we can help. What does your business need most?",
    goals: {
      sales: ["More leads and sales", "Got it. The bottleneck is often speed: leads that wait a day go cold, and follow-ups get forgotten."],
      manual: ["Less manual work", "Makes sense. Copying data, answering the same emails, building reports by hand: that's the first work to hand over to automation."],
      data: ["Numbers under control", "Clear. The goal is one view where sales, cash and margins are always up to date, without chasing spreadsheets."],
      abroad: ["Selling abroad", "Great. Languages, local markets and foreign suppliers are where we can make a real difference: we work in five languages, Chinese included."],
      unsure: ["Not sure yet", "No problem, that's exactly what the first call is for. Let's start with the basics."],
    },
    sector_q: "What industry are you in?",
    sectors: { ecom: "E-commerce", services: "Professional services", edu: "Education and coaching", b2b: "B2B sales", local: "Local business", craft: "Brand or craft" },
    team_q: (s) => `${s}, good. How many people work at the company?`, team: ["1-5", "6-20", "21-50", "50+"],
    when_q: "And when would you like to start?", when: ["Right away", "Within 1-3 months", "Within 6 months", "Just exploring"],
    hot: "Perfect, let's move fast then.", warm: "Good, there's time to design it properly.",
    sum: "Here's what I understood:", k_goal: "Goal", k_sector: "Industry", k_team: "Team", k_when: "Start", k_svc: "We'd suggest",
    case: (name, url) => `A project close to yours: <a href="${url}">${name} →</a>`,
    next_q: "How would you like to continue?", c_book: "Book a free call", c_here: "Leave my details here",
    book: "Perfect: the form is already filled in with your answers.", book_btn: "Go to the form",
    name_q: "Great. What's your name?", email_q: (n) => `Nice to meet you, ${n}. What's the best email to reach you?`, email_bad: "That email doesn't look right, can you check it?",
    consent_q: "Last thing: may we use these details to get back to you about this request?", yes: "Yes, I agree", no: "No thanks",
    sending: "Sending…", sent: (n) => `Done, ${n}! Alessandro will get back to you within one business day with first ideas and a date for the call.`,
    fail: "Sending didn't work. You can use the form instead:", declined: "No problem. You can always use the contact form:",
    restart: "Start over", huh: "I'm not sure I understood. Pick one of the options, or put it another way.",
    note: "Guided demo. The agents we build for you use real AI, connected to your CRM and calendar, on your website, WhatsApp and email.",
    svc: { "11": "AI sales agents", "03": "Custom CRM", "13": "Sales call analysis", "06": "Automation, with and without AI", "12": "AI voice assistants", "08": "Dashboards", "09": "Company hub", "15": "Multilingual websites", "16": "Italy-China bridge", "07": "Company brain", "14": "3D configurators", "01": "Websites" },
    need: { sales: ["CRM and sales", "AI agents and voice assistants"], manual: ["Automation (with or without AI)"], data: ["Dashboards and financial control"], abroad: ["Multilingual or China projects"], unsure: ["Not sure yet"] },
    subject: "New lead from the AI agent", typing: "typing",
  } : {
    open: "Parla con il nostro agente AI", title: "Agente Reef 7", status: "Demo · risponde in pochi secondi", ph: "Scrivi un messaggio…", send: "Invia",
    teaser: "Vuoi scoprire in 30 secondi cosa potremmo automatizzare nella tua azienda?",
    hello: "Ciao! Sono una demo degli agenti di vendita che costruiamo. Ti faccio qualche domanda veloce e ti dico come possiamo aiutarti. Di cosa ha più bisogno la tua azienda?",
    goals: {
      sales: ["Più contatti e vendite", "Chiaro. Spesso il collo di bottiglia è la velocità: un contatto che aspetta un giorno si raffredda, e i follow-up si dimenticano."],
      manual: ["Meno lavoro manuale", "Ha senso. Copiare dati, rispondere alle stesse email, fare report a mano: è il primo lavoro da affidare all'automazione."],
      data: ["Numeri sotto controllo", "Capito. L'obiettivo è un'unica vista con vendite, cassa e margini sempre aggiornati, senza rincorrere fogli Excel."],
      abroad: ["Vendere all'estero", "Ottimo. Lingue, mercati locali e fornitori esteri sono il terreno dove possiamo fare davvero la differenza: lavoriamo in cinque lingue, cinese compreso."],
      unsure: ["Non lo so ancora", "Nessun problema, la prima call serve proprio a questo. Partiamo dalle basi."],
    },
    sector_q: "In che settore lavori?",
    sectors: { ecom: "E-commerce", services: "Studio o consulenza", edu: "Formazione e coaching", b2b: "Vendita B2B", local: "Attività locale", craft: "Brand o artigianato" },
    team_q: (s) => `${s}, bene. Quante persone lavorano in azienda?`, team: ["1-5", "6-20", "21-50", "Oltre 50"],
    when_q: "E quando vorresti partire?", when: ["Subito", "Entro 1-3 mesi", "Entro 6 mesi", "Sto valutando"],
    hot: "Perfetto, allora andiamo veloci.", warm: "Bene, c'è il tempo per progettarlo come si deve.",
    sum: "Ecco cosa ho capito:", k_goal: "Obiettivo", k_sector: "Settore", k_team: "Team", k_when: "Partenza", k_svc: "Ti consigliamo",
    case: (name, url) => `Un progetto vicino al tuo: <a href="${url}">${name} →</a>`,
    next_q: "Come preferisci proseguire?", c_book: "Prenota una call gratuita", c_here: "Lascio i miei contatti qui",
    book: "Perfetto: il modulo è già compilato con le tue risposte.", book_btn: "Vai al modulo",
    name_q: "Ottimo. Come ti chiami?", email_q: (n) => `Piacere, ${n}. A quale email ti possiamo scrivere?`, email_bad: "Questa email non sembra corretta, puoi controllarla?",
    consent_q: "Ultima cosa: possiamo usare questi dati per ricontattarti in merito alla richiesta?", yes: "Sì, acconsento", no: "No, grazie",
    sending: "Invio in corso…", sent: (n) => `Fatto, ${n}! Alessandro ti scrive entro un giorno lavorativo con le prime idee e una data per la call.`,
    fail: "L'invio non è riuscito. Puoi usare il modulo:", declined: "Nessun problema. Puoi sempre usare il modulo contatti:",
    restart: "Ricomincia", huh: "Non sono sicuro di aver capito. Scegli una delle opzioni, oppure dimmelo in un altro modo.",
    note: "Demo guidata. Gli agenti che costruiamo per te usano l'AI vera, collegata al tuo CRM e al tuo calendario, su sito, WhatsApp ed email.",
    svc: { "11": "Agenti AI per le vendite", "03": "CRM su misura", "13": "Analisi delle call", "06": "Automazioni", "12": "Assistenti vocali AI", "08": "Dashboard", "09": "Hub aziendale", "15": "Siti multilingue", "16": "Ponte Italia-Cina", "07": "Company brain", "14": "Configuratori 3D", "01": "Siti web" },
    need: { sales: ["CRM e vendite", "Agenti AI e assistenti vocali"], manual: ["Automazioni (con o senza AI)"], data: ["Dashboard e controllo di gestione"], abroad: ["Multilingue o progetti con la Cina"], unsure: ["Non lo so ancora"] },
    subject: "Nuovo contatto dall'agente AI", typing: "sta scrivendo",
  };

  // servizi consigliati per obiettivo, ritoccati dal settore; progetto del portfolio più vicino al settore
  const REC = { sales: ["11", "03", "13"], manual: ["06", "12", "07"], data: ["08", "09"], abroad: ["15", "16"], unsure: ["07", "11"] };
  const SECTOR_SVC = { ecom: "14", local: "12", edu: "11", services: "07", b2b: "13", craft: "01" };
  const CASE = { ecom: ["Full Peak", "fullpeak"], services: ["Tenka OS", "tenka"], edu: ["My Daily Peak", "dailypeak"], b2b: ["Tenka OS", "tenka"], local: ["Kasino Latino", "kasinolatino"], craft: ["Maisenzagioie", "maisenzagioie"] };

  // comprensione del testo libero: parole chiave per ogni risposta possibile
  const KW = {
    goal: { sales: /vend|client|lead|contatt|fattur|sales|sell|customer|revenue/, manual: /manual|automa|tempo|ripetit|excel|time|repetit|copia|copy/, data: /dati|numer|dashboard|margin|report|cassa|data|number|cash|kpi/, abroad: /ester|cina|chin|lingu|internaz|abroad|export|languag|foreign|mercat/, unsure: /non so|boh|not sure|don.?t know|vediamo|dunno/ },
    sector: { ecom: /e-?comm|shop|negozio online|store|amazon|online/, services: /studio|consul|profession|avvocat|commercialist|agenz|agency|servizi|services|law|account/, edu: /formaz|corso|corsi|coach|course|training|educa|accadem|scuola online/, b2b: /b2b|commercial|rete vendita|industr|azienda|manufactur|wholesale/, local: /palestr|gym|ristor|restaurant|bar|negozio|locale|local|scuola|school|salon|hotel|clinic|studio medico/, craft: /artigian|handmade|gioiel|craft|brand|moda|fashion|design/ },
    when: [/subito|\bora\b|adesso|asap|right away|\bnow\b|immediat|urgent/, /mes[ei]|month|presto|soon|1-3|\btre\b|three/, /\b6\b|\bsei\b|\bsix\b|anno|year/, /valut|explor|not sure|vedr|pensando|thinking/],
  };
  const teamFrom = (txt) => {
    const n = parseInt((txt.match(/\d+/) || [])[0], 10);
    if (isNaN(n)) return /solo|da solo|alone|just me|freelance/.test(txt) ? 0 : -1;
    return n <= 5 ? 0 : n <= 20 ? 1 : n <= 50 ? 2 : 3;
  };
  const match = (map, txt) => Object.keys(map).find((k) => map[k].test(txt));

  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const launcher = el("button", "ag-launch", `<span class="ag-dot" aria-hidden="true"></span><span>${T.open}</span>`);
  launcher.type = "button";
  launcher.setAttribute("aria-expanded", "false");
  const panel = el("section", "ag-panel");
  panel.hidden = true;
  panel.setAttribute("aria-label", T.title);
  panel.innerHTML = `<header class="ag-head"><span class="ag-avatar" aria-hidden="true">R7</span><div><b>${T.title}</b><small>${T.status}</small></div>
    <button type="button" class="ag-x" aria-label="×">×</button></header>
    <div class="ag-log" role="log" aria-live="polite"></div><div class="ag-chips"></div>
    <form class="ag-input"><input type="text" placeholder="${T.ph}" aria-label="${T.ph}" autocomplete="off" disabled><button type="submit" aria-label="${T.send}" disabled>↑</button></form>`;
  document.body.append(launcher, panel);
  const log = panel.querySelector(".ag-log"), chips = panel.querySelector(".ag-chips");
  const input = panel.querySelector(".ag-input input"), sendBtn = panel.querySelector(".ag-input button");
  let started = false, pending = null, teaser = null;

  // invito discreto dopo qualche secondo, una sola volta per visita
  let seen = false;
  try { seen = sessionStorage.getItem("ag-teaser") === "1"; } catch {}
  if (!seen) setTimeout(() => {
    if (started) return;
    teaser = el("button", "ag-teaser", `${T.teaser}<span aria-hidden="true">×</span>`);
    teaser.type = "button";
    teaser.addEventListener("click", (e) => { const x = e.target.tagName === "SPAN"; teaser.remove(); teaser = null; if (!x) toggle(true); });
    document.body.append(teaser);
    try { sessionStorage.setItem("ag-teaser", "1"); } catch {}
  }, 9000);

  const toggle = (open) => {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", open);
    launcher.classList.toggle("on", open);
    if (teaser) { teaser.remove(); teaser = null; }
    if (open && !started) { started = true; run(); }
    if (open && !input.disabled) input.focus();
  };
  launcher.addEventListener("click", () => toggle(panel.hidden));
  panel.querySelector(".ag-x").addEventListener("click", () => toggle(false));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) toggle(false); });

  const scroll = () => { log.scrollTop = log.scrollHeight; };
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const say = async (html) => {
    const t = el("div", "ag-msg bot ag-typing", `<i></i><i></i><i></i><span class="sr">${T.typing}</span>`);
    log.append(t); scroll();
    await wait(Math.min(1400, 350 + html.replace(/<[^>]+>/g, "").length * 9));
    t.className = "ag-msg bot"; t.innerHTML = html; scroll();
  };
  const me = (txt) => { log.append(el("div", "ag-msg me", esc(txt))); scroll(); };

  // una domanda: pulsanti rapidi e/o testo libero; parse() restituisce il valore o null se non ha capito
  const ask = (opts, parse) => new Promise((resolve) => {
    chips.innerHTML = "";
    opts.forEach(([val, label]) => {
      const b = el("button", "ag-chip", label); b.type = "button";
      b.addEventListener("click", () => done(val, label));
      chips.append(b);
    });
    const done = (val, label) => { chips.innerHTML = ""; pending = null; input.value = ""; input.disabled = sendBtn.disabled = true; me(label); resolve(val); };
    pending = parse ? async (txt) => {
      const v = parse(txt);
      if (v != null) return done(v, txt);
      me(txt); input.value = ""; await say(T.huh);
    } : null;
    input.disabled = sendBtn.disabled = !parse;
    if (parse && !panel.hidden) input.focus();
    scroll();
  });
  panel.querySelector(".ag-input").addEventListener("submit", (e) => {
    e.preventDefault();
    const txt = input.value.trim();
    if (txt && pending) pending(txt);
  });

  async function run() {
    log.innerHTML = "";
    const st = {};
    await say(T.hello);
    st.goal = await ask(Object.entries(T.goals).map(([k, v]) => [k, v[0]]), (t) => match(KW.goal, t.toLowerCase()) || null);
    await say(T.goals[st.goal][1]);
    await say(T.sector_q);
    st.sector = await ask(Object.entries(T.sectors), (t) => match(KW.sector, t.toLowerCase()) || null);
    await say(T.team_q(T.sectors[st.sector]));
    const ti = await ask(T.team.map((x, i) => [i, x]), (t) => { const i = teamFrom(t.toLowerCase()); return i < 0 ? null : i; });
    st.team = T.team[ti];
    await say(T.when_q);
    const wi = await ask(T.when.map((x, i) => [i, x]), (t) => { const l = t.toLowerCase(); const i = [0, 3, 2, 1].find((k) => KW.when[k].test(l)); return i == null ? null : i; });
    st.when = T.when[wi];
    await say(wi <= 1 ? T.hot : T.warm);

    const ids = [...new Set([...REC[st.goal], SECTOR_SVC[st.sector]])].slice(0, 3);
    st.recs = ids.map((id) => T.svc[id]);
    const recs = ids.map((id) => `<a href="${svcPage}#s${id}">${T.svc[id]}</a>`).join("");
    const [caseName, caseId] = CASE[st.sector];
    await say(`${T.sum}<dl class="ag-sum"><div><dt>${T.k_goal}</dt><dd>${T.goals[st.goal][0]}</dd></div><div><dt>${T.k_sector}</dt><dd>${T.sectors[st.sector]}</dd></div><div><dt>${T.k_team}</dt><dd>${st.team}</dd></div><div><dt>${T.k_when}</dt><dd>${st.when}</dd></div><div><dt>${T.k_svc}</dt><dd class="ag-recs">${recs}</dd></div></dl>`);
    await say(T.case(caseName, `${workPage}#${caseId}`));

    await say(T.next_q);
    const how = await ask([["book", T.c_book], ["here", T.c_here]]);
    const q = new URLSearchParams({ need: T.need[st.goal].join("|"), team: st.team, when: st.when, goal: `${T.goals[st.goal][0]} · ${T.sectors[st.sector]}` });
    const formLink = `${contactPage}?${q}#contact-form`;
    if (how === "book") {
      await say(`${T.book}<div class="ag-actions"><a class="ag-book" href="${formLink}">${T.book_btn} →</a></div>`);
      return finish();
    }
    await say(T.name_q);
    st.name = await ask([], (t) => t.slice(0, 80));
    await say(T.email_q(esc(st.name.split(" ")[0])));
    let email = null;
    while (!email) {
      const v = await ask([], (t) => t);
      if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) email = v; else await say(T.email_bad);
    }
    st.email = email;
    await say(T.consent_q);
    const ok = await ask([["yes", T.yes], ["no", T.no]]);
    if (ok === "no") { await say(`${T.declined}<div class="ag-actions"><a class="ag-book" href="${formLink}">${T.book_btn} →</a></div>`); return finish(); }
    const wait1 = el("div", "ag-msg bot", T.sending); log.append(wait1); scroll();
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `${T.subject}: ${st.name} · ${T.goals[st.goal][0]}`, _replyto: st.email, _template: "table", _captcha: "false",
          "Nome": st.name, "Email": st.email, "Obiettivo": T.goals[st.goal][0], "Settore": T.sectors[st.sector],
          "Persone in azienda": st.team, "Quando partire": st.when, "Servizi consigliati": st.recs.join(", "), "Fonte": "Agente AI del sito",
        }),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || out.success === false || out.success === "false") throw new Error();
      wait1.remove();
      await say(T.sent(esc(st.name.split(" ")[0])));
    } catch {
      wait1.remove();
      await say(`${T.fail}<div class="ag-actions"><a class="ag-book" href="${formLink}">${T.book_btn} →</a></div>`);
    }
    finish();
  }

  async function finish() {
    log.append(el("p", "ag-note", T.note));
    chips.innerHTML = "";
    pending = null; input.value = ""; input.disabled = sendBtn.disabled = true;
    const b = el("button", "ag-chip", T.restart); b.type = "button";
    b.addEventListener("click", run);
    chips.append(b);
    scroll();
  }
})();
