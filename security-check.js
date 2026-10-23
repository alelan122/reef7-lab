// Check di esposizione: controlli pubblici sul dominio (Mozilla Observatory, SPF e DMARC via DNS pubblici),
// poche domande, livello di esposizione e 3 priorità. Il voto si vede subito, il report completo in cambio dell'email.
// Solo controlli passivi: nessuna scansione invasiva del sito di chi compila.
(() => {
  const root = document.getElementById("check");
  if (!root) return;
  const en = document.documentElement.lang === "en";
  const MAIL = (window.REEF && window.REEF.email) || "lancioni.ale@gmail.com";
  const endpoint = `https://formsubmit.co/ajax/${MAIL}`;
  const base = en ? "../" : "";
  const secPage = en ? "security.html" : "sicurezza.html";
  const svcPage = en ? "services.html" : "servizi.html";
  const contactPage = en ? "contact.html" : "contatti.html";
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const T = en ? {
    steps: ["Your domain", "What you have online", "Habits", "Your report"], step_of: (a, b) => `Step ${a} of ${b}`,
    domain_q: "Your company's website", domain_ph: "yourcompany.com", domain_hint: "We only use public information, read through Google DNS and Mozilla Observatory. No intrusive tests.",
    scan: "Check", scanning: "We're looking at your site the way an attacker sees it…", no_site: "We don't have a website",
    bad_domain: "Enter a domain like yourcompany.com", not_found: "This domain doesn't seem to exist: check the spelling.",
    r_web: "Site protections", r_mail: "Email in your name", r_na: "not available right now", r_fail: (f, n) => `${f} of ${n} checks not passed`,
    mail_ok: "Protected: fake emails in your name are blocked", mail_mon: "Monitoring only: fake emails in your name still get through",
    mail_none: "Not protected: anyone can send an email that looks like it comes from you", spf_none: "SPF missing",
    have_q: "What do you have online?", have_hint: "Select everything that applies",
    have: ["Brochure website", "Online store", "Customer area with login", "Internal app or management tool", "Site or app built with AI tools", "Chatbot or AI agent connected to email, documents or CRM", "Integrations between software (CRM, payments, automations)"],
    age_q: "How long has your main website been online?", ages: ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years", "I don't know"],
    php_q: "Does your site run on WordPress, WooCommerce, PrestaShop, Magento or another PHP platform?", phps: ["Yes", "No", "I don't know"],
    maint_q: "Who looks after it today?", maints: ["We do, in-house", "The agency that built it, still active", "Nobody since it was delivered", "I don't know"],
    yn: ["Yes", "No", "I don't know"],
    habits: [
      ["mfa", "Two-factor login is active on email, hosting, payments and CRM"],
      ["off", "When someone leaves, their access is removed the same day"],
      ["pw", "Passwords are shared in chat, email or spreadsheets", true],
      ["bak", "A backup has actually been restored at least once in the last 6 months"],
      ["upd", "Website, plugins and components are updated regularly"],
      ["aid", "The team pastes customer data into AI tools", true],
      ["agt", "A chatbot or AI agent can send emails or change data without a person approving", true],
    ],
    sector_q: "What industry are you in?", sectors: ["E-commerce", "Professional services", "Education and coaching", "B2B sales", "Local business", "Health and wellness", "Other"],
    team_q: "How many people work at the company?", teams: ["1-5", "6-20", "21-50", "50+"],
    role_q: "Your role", roles: ["Owner", "Manager", "Technical", "Other"],
    inc_q: "Has anything happened in recent months?", incs: ["Nothing", "Suspicious emails or attempted scams", "An account or data compromised", "The site went down or was altered"],
    back: "Back", next: "Next", see: "See my result", need_pick: "Choose an answer to continue.", need_domain: "Check your domain first, or choose “we don't have a website”.",
    live_k: "What an attacker sees", live_empty: "Enter your domain: the checks run in a few seconds.", live_level: "Exposure so far",
    levels: ["Low", "Medium", "High", "Critical"],
    level_p: [
      "Your foundations are solid. A few refinements and regular checks are enough to keep it that way.",
      "There are open doors, none of them dramatic yet. Fixed now, they cost little; left alone, they add up.",
      "Some of your doors are easy to find for anyone looking. It's worth acting in the coming weeks, starting with the first priority.",
      "Several serious risks at once: today these are exactly the conditions automated attacks look for. It's worth acting this week.",
    ],
    gate_k: "Your result", gate_h: (l, n) => `Exposure: <em>${l}</em>. We found ${n} point${n === 1 ? "" : "s"} to fix.`,
    gate_p: "Get the full report: what an attacker sees from your domain, your 3 priorities with what to do today, and how we fix them. A copy also arrives by email.",
    name: "Name", company: "Company", email: "Work email", consent: "I agree to be contacted by Reef 7 Lab about this report. Details are sent through FormSubmit.",
    unlock: "Get the full report", sending: "Sending…", bad_email: "Check your email address.", need_consent: "Tick the box to receive the report.",
    subject: "Security check", r_title: "Exposure check", r_for: "for",
    sent_ok: (e) => `A copy is on its way to <b>${e}</b>.`, sent_fail: "Your details didn't reach me, so the email copy wasn't sent. Download the PDF or write to me at {email}.",
    r_seen: "What an attacker sees from your domain", r_details: "Full public details", r_prio: "Your 3 priorities", r_good: "What's already working",
    p_why: "Why it matters", p_today: "What you can do today", p_us: "What we do", p_when: "When", when: ["Right away", "In the coming weeks", "Structural"],
    see_svc: "See the service", r_all: "Other points to fix",
    sign_h: "I'll write to you myself", sign_p: "I read every check personally. Within one working day you'll get an email from me to set up a free 30-minute review of your systems.", sign_n: "Alessandro Lancioni · Founder of Reef 7 Lab",
    add: "Add details", pdf: "Download PDF", restart: "Start again",
    note: "This is an indicative check based on public information and your answers: it doesn't replace a full review, but it tells you where to start. Weights: each risk counts 1 to 3 points depending on severity; Low 0-5, Medium 6-11, High 12-18, Critical 19+.",
    mail_intro: (n) => `Hi ${n},\n\nhere is your Reef 7 Lab exposure check.`, mail_end: "I read every check personally: within one working day I'll write to you to set up a free 30-minute review.\n\nAlessandro Lancioni\nReef 7 Lab",
    from_agent: "We continue from your chat with the AI agent.",
  } : {
    steps: ["Il tuo dominio", "Cosa hai online", "Le abitudini", "Il tuo report"], step_of: (a, b) => `Passo ${a} di ${b}`,
    domain_q: "Il sito della tua azienda", domain_ph: "tuazienda.it", domain_hint: "Usiamo solo informazioni pubbliche, lette tramite Google DNS e Mozilla Observatory. Nessuna prova invasiva.",
    scan: "Controlla", scanning: "Stiamo guardando il tuo sito come lo vede chi attacca…", no_site: "Non abbiamo un sito",
    bad_domain: "Scrivi un dominio come tuazienda.it", not_found: "Questo dominio non sembra esistere: controlla come l'hai scritto.",
    r_web: "Protezioni del sito", r_mail: "Email a tuo nome", r_na: "non disponibile in questo momento", r_fail: (f, n) => (f === 1 ? `1 controllo su ${n} non superato` : `${f} controlli su ${n} non superati`),
    mail_ok: "Protetto: le email false a tuo nome vengono bloccate", mail_mon: "Solo monitoraggio: le email false a tuo nome passano ancora",
    mail_none: "Non protetto: chiunque può mandare un'email che sembra arrivare da te", spf_none: "SPF assente",
    have_q: "Cosa hai online?", have_hint: "Seleziona tutto quello che c'è",
    have: ["Sito vetrina", "E-commerce", "Area clienti con login", "Gestionale o app interna", "Sito o app costruiti con strumenti di intelligenza artificiale", "Chatbot o agente AI collegato a email, documenti o CRM", "Integrazioni tra software (CRM, pagamenti, automazioni)"],
    age_q: "Da quanto è online il sito principale?", ages: ["Meno di 1 anno", "1-3 anni", "3-5 anni", "Più di 5 anni", "Non lo so"],
    php_q: "Il sito usa WordPress, WooCommerce, PrestaShop, Magento o un'altra piattaforma in PHP?", phps: ["Sì", "No", "Non lo so"],
    maint_q: "Chi se ne occupa oggi?", maints: ["Noi, internamente", "L'agenzia che l'ha fatto, ancora attiva", "Nessuno, da quando è stato consegnato", "Non lo so"],
    yn: ["Sì", "No", "Non lo so"],
    habits: [
      ["mfa", "Il doppio fattore è attivo su email, hosting, pagamenti e CRM"],
      ["off", "Quando qualcuno lascia l'azienda, i suoi accessi vengono tolti lo stesso giorno"],
      ["pw", "Le password vengono condivise in chat, email o fogli di calcolo", true],
      ["bak", "Un backup è stato davvero ripristinato almeno una volta negli ultimi 6 mesi"],
      ["upd", "Sito, plugin e componenti vengono aggiornati con regolarità"],
      ["aid", "Il team incolla dati di clienti in strumenti di intelligenza artificiale", true],
      ["agt", "Un chatbot o agente AI può inviare email o modificare dati senza la conferma di una persona", true],
    ],
    sector_q: "In che settore lavori?", sectors: ["E-commerce", "Servizi e studi professionali", "Formazione e coaching", "Vendite B2B", "Attività locale", "Salute e benessere", "Altro"],
    team_q: "Quante persone lavorano in azienda?", teams: ["1-5", "6-20", "21-50", "50+"],
    role_q: "Il tuo ruolo", roles: ["Titolare", "Responsabile", "Tecnico", "Altro"],
    inc_q: "Negli ultimi mesi è successo qualcosa?", incs: ["Niente", "Email sospette o truffe tentate", "Un account o dei dati compromessi", "Il sito è stato fermo o modificato"],
    back: "Indietro", next: "Avanti", see: "Vedi il risultato", need_pick: "Scegli una risposta per continuare.", need_domain: "Prima controlla il dominio, oppure scegli “non abbiamo un sito”.",
    live_k: "Cosa vede chi attacca", live_empty: "Scrivi il tuo dominio: i controlli durano pochi secondi.", live_level: "Esposizione finora",
    levels: ["Bassa", "Media", "Alta", "Critica"],
    level_p: [
      "Le basi sono solide. Bastano qualche rifinitura e controlli regolari per restare così.",
      "Ci sono porte aperte, nessuna ancora drammatica. Sistemate ora costano poco; lasciate lì, si sommano.",
      "Alcune tue porte sono facili da trovare per chi le cerca. Conviene intervenire nelle prossime settimane, partendo dalla prima priorità.",
      "Più rischi seri insieme: sono esattamente le condizioni che oggi cercano gli attacchi automatici. Conviene intervenire questa settimana.",
    ],
    gate_k: "Il tuo risultato", gate_h: (l, n) => `Esposizione: <em>${l}</em>. Abbiamo trovato ${n} ${n === 1 ? "punto" : "punti"} da sistemare.`,
    gate_p: "Ricevi il report completo: cosa vede chi attacca dal tuo dominio, le tue 3 priorità con cosa fare già oggi e come le risolviamo noi. Una copia arriva anche per email.",
    name: "Nome", company: "Azienda", email: "Email di lavoro", consent: "Accetto di essere ricontattato da Reef 7 Lab su questo report. I dati arrivano tramite FormSubmit.",
    unlock: "Ricevi il report completo", sending: "Invio…", bad_email: "Controlla l'indirizzo email.", need_consent: "Spunta la casella per ricevere il report.",
    subject: "Check sicurezza", r_title: "Check di esposizione", r_for: "per",
    sent_ok: (e) => `Una copia sta arrivando a <b>${e}</b>.`, sent_fail: "I tuoi dati non mi sono arrivati, quindi la copia per email non è partita. Scarica il PDF oppure scrivimi a {email}.",
    r_seen: "Cosa vede chi attacca dal tuo dominio", r_details: "Dettaglio pubblico completo", r_prio: "Le tue 3 priorità", r_good: "Cosa va già bene",
    p_why: "Perché conta", p_today: "Cosa puoi fare oggi", p_us: "Cosa facciamo noi", p_when: "Quando", when: ["Subito", "Nelle prossime settimane", "Strutturale"],
    see_svc: "Vedi il servizio", r_all: "Altri punti da sistemare",
    sign_h: "Ti scrivo io", sign_p: "Leggo ogni check personalmente. Entro un giorno lavorativo ricevi una mia email per fissare una ricognizione gratuita di 30 minuti sui tuoi sistemi.", sign_n: "Alessandro Lancioni · Fondatore di Reef 7 Lab",
    add: "Aggiungi dettagli", pdf: "Scarica il PDF", restart: "Ricomincia",
    note: "È un check orientativo, basato su informazioni pubbliche e sulle tue risposte: non sostituisce una verifica completa, ma ti dice da dove partire. Pesi: ogni rischio vale da 1 a 3 punti secondo la gravità; Bassa 0-5, Media 6-11, Alta 12-18, Critica 19 e oltre.",
    mail_intro: (n) => `Ciao ${n},\n\necco il tuo check di esposizione di Reef 7 Lab.`, mail_end: "Leggo ogni check personalmente: entro un giorno lavorativo ti scrivo per fissare una ricognizione gratuita di 30 minuti.\n\nAlessandro Lancioni\nReef 7 Lab",
    from_agent: "Continuiamo dalla chat con l'agente AI.",
  };

  // rischi: titolo, perché conta (con il caso di cronaca), cosa fare oggi, servizio, quando (0 subito, 1 settimane, 2 strutturale)
  const R = en ? {
    php: ["Your site runs on PHP: check it's updated now", "On October 21, 2026 an AI found critical flaws in PHP, the language behind about 7 in 10 websites: they let attackers take control of the server. Within hours of the announcement, millions of attack attempts began, and the FBI advised taking offline any site that couldn't be updated right away.", "Ask whoever manages the site today whether PHP and the platform were updated after October 21. If they can't answer, treat it as not updated.", ["sec", "36"], 0],
    web: ["Your site doesn't use the browser's basic protections", "Without these settings, a site is easier to impersonate, tamper with or abuse. Working is not the same as protected: researchers found 170 out of 1,645 AI-built apps leaving data open to anyone.", "Ask whoever manages the site to enforce HTTPS and enable the security headers (HSTS, CSP): these are settings, not a rebuild.", ["sec", "36"], 1],
    mail: ["Anyone can send emails in your name", "It's the favourite tool of scams: a fake invoice or a password request that looks like it comes from you, sent to your customers and suppliers.", "Publish a DMARC record in monitoring mode (p=none), read the reports for two weeks, then move to quarantine.", ["sec", "38"], 0],
    old: ["A website nobody looks after anymore", "Agents look precisely for old components with known flaws: it's the cheapest way in, and it works on thousands of sites at once.", "Ask for the list of components and plugins with their versions: that alone says a lot.", ["sec", "36"], 0],
    ai: ["A site or app built with AI, never checked", "In a scan of 1,645 apps made with a well-known AI builder, 170 let anyone read users, payments or keys, because database rules were never written.", "Open your site in a private window and try to reach private pages without logging in: if they open, it's urgent.", ["sec", "32"], 0],
    agt: ["An AI agent that can act on its own", "A single crafted email was enough to make a widely used AI assistant hand over company data. Another agent deleted a production database during a code freeze.", "Remove the agent's permission to send emails or delete data until a person approves each action.", ["sec", "33"], 0],
    mfa: ["Accounts without two-factor login", "A test panel protected by 123456, without two-factor login, exposed data tied to up to 64 million job applications.", "Turn on two-factor login today for email, hosting and payments: about 10 minutes per account.", ["sec", "37"], 0],
    off: ["Access left open for people who have left", "Many breaches don't start from a technical flaw but from a login nobody remembered to close: stolen tokens from one integration opened the CRMs of 700 companies.", "List who has access to email, hosting, CRM and payments, and remove anyone who no longer works with you.", ["sec", "37"], 0],
    pw: ["Passwords shared in chat or spreadsheets", "Whoever gets into one inbox or chat finds the keys to everything else.", "Move shared passwords into a team password manager and change the most important ones.", ["sec", "37"], 1],
    bak: ["Backups never tested", "A backup that has never been restored is a hope, not a backup. When an AI agent wiped a database, it was a working backup that saved the data.", "Ask whoever manages your systems to restore a backup onto a copy: if they can't, you don't have a backup.", ["sec", "35"], 1],
    upd: ["Updates done irregularly", "Every postponed update is a known flaw left open, published for anyone to read.", "Set one day a month for updates, always after a backup.", ["sec", "36"], 1],
    aid: ["Customer data pasted into AI tools", "Every prompt is data leaving the company: often nobody knows where it ends up or how long it stays.", "Set a simple rule: no customer names, emails or documents in public AI chats, only in approved business tools.", ["sec", "34"], 1],
    inc: ["Something has already happened", "An incident is often the visible part of a larger door. It's worth understanding how it happened before it happens again.", "Change the passwords of the accounts involved, turn on two-factor login and keep any suspicious emails as evidence.", ["sec", "36"], 0],
  } : {
    php: ["Il tuo sito gira su PHP: verifica subito che sia aggiornato", "Il 21 ottobre 2026 un'AI ha trovato falle critiche in PHP, il linguaggio di circa 7 siti su 10: permettono di prendere il controllo del server. Nelle ore dopo l'annuncio sono partiti milioni di tentativi di attacco, e l'FBI ha consigliato di spegnere i siti che non si possono aggiornare subito.", "Chiedi oggi a chi gestisce il sito se PHP e la piattaforma sono stati aggiornati dopo il 21 ottobre. Se non sa risponderti, consideralo non aggiornato.", ["sec", "36"], 0],
    web: ["Il sito non usa le protezioni di base dei browser", "Senza queste impostazioni un sito è più facile da imitare, manomettere o sfruttare. Funzionare non vuol dire essere protetti: i ricercatori hanno trovato 170 app su 1.645, fatte con l'AI, che lasciavano i dati aperti a chiunque.", "Chiedi a chi gestisce il sito di rendere obbligatorio l'HTTPS e di attivare le intestazioni di sicurezza (HSTS, CSP): sono impostazioni, non un rifacimento.", ["sec", "36"], 1],
    mail: ["Chiunque può mandare email a nome tuo", "È lo strumento preferito delle truffe: una fattura falsa o una richiesta di password che sembra arrivare da te, inviata ai tuoi clienti e fornitori.", "Pubblica un record DMARC in modalità monitoraggio (p=none), leggi i rapporti per due settimane e poi passa a quarantine.", ["sec", "38"], 0],
    old: ["Un sito che nessuno guarda più", "Gli agenti cercano proprio componenti vecchi con falle note: è il modo più economico per entrare, e funziona su migliaia di siti insieme.", "Fatti dare l'elenco di componenti e plugin con la loro versione: già quello dice molto.", ["sec", "36"], 0],
    ai: ["Un sito o un'app costruiti con l'AI, mai verificati", "Su 1.645 app fatte con un noto generatore basato sull'AI, 170 lasciavano leggere a chiunque utenti, pagamenti o chiavi, perché le regole del database non erano mai state scritte.", "Apri il sito in una finestra in incognito e prova a raggiungere le pagine riservate senza login: se si aprono, è urgente.", ["sec", "32"], 0],
    agt: ["Un agente AI che può agire da solo", "Una sola email preparata ad arte bastava a far consegnare dati aziendali a un assistente AI diffusissimo. Un altro agente ha cancellato un database di produzione durante un blocco delle modifiche.", "Togli all'agente il permesso di inviare email o cancellare dati finché una persona non conferma ogni azione.", ["sec", "33"], 0],
    mfa: ["Account senza doppio fattore", "Un pannello di prova protetto da 123456, senza doppio fattore, ha esposto i dati legati a fino a 64 milioni di candidature di lavoro.", "Attiva oggi il doppio fattore su email, hosting e pagamenti: circa 10 minuti per account.", ["sec", "37"], 0],
    off: ["Accessi aperti di chi non c'è più", "Molte violazioni non partono da una falla tecnica, ma da un accesso che nessuno ha chiuso: i token rubati a una sola integrazione hanno aperto i CRM di 700 aziende.", "Fai la lista di chi ha accesso a email, hosting, CRM e pagamenti, e togli chi non lavora più con te.", ["sec", "37"], 0],
    pw: ["Password condivise in chat o nei fogli di calcolo", "Chi entra in una casella email o in una chat trova le chiavi di tutto il resto.", "Sposta le password condivise in un gestore di password del team e cambia le più importanti.", ["sec", "37"], 1],
    bak: ["Backup mai provati", "Un backup mai ripristinato è una speranza, non un backup. Quando un agente AI ha cancellato un database, a salvare i dati è stato un backup funzionante.", "Chiedi a chi gestisce i sistemi di ripristinare un backup su una copia: se non ci riesce, non hai un backup.", ["sec", "35"], 1],
    upd: ["Aggiornamenti fatti senza regolarità", "Ogni aggiornamento rimandato è una falla nota lasciata aperta, pubblicata e leggibile da chiunque.", "Fissa un giorno al mese per gli aggiornamenti, sempre dopo un backup.", ["sec", "36"], 1],
    aid: ["Dati dei clienti incollati negli strumenti AI", "Ogni prompt è un dato che esce dall'azienda: spesso nessuno sa dove finisce e per quanto resta.", "Stabilisci una regola semplice: niente nomi, email o documenti di clienti nelle chat AI pubbliche, solo in strumenti aziendali approvati.", ["sec", "34"], 1],
    inc: ["È già successo qualcosa", "Un incidente è spesso la parte visibile di una porta più grande. Conviene capire come è successo prima che succeda di nuovo.", "Cambia le password degli account coinvolti, attiva il doppio fattore e conserva le email sospette come prova.", ["sec", "36"], 0],
  };
  const GOOD = en ? {
    web: "Your site uses the main browser protections", mail: "Your domain blocks fake emails in your name", mfa: "Two-factor login is active",
    off: "Access is removed when someone leaves", pw: "Passwords aren't shared in chats or spreadsheets", bak: "Your backups have been tested with a real restore",
    upd: "Updates are done regularly", aid: "Customer data stays out of AI tools", agt: "Your AI agent asks for approval before acting", maint: "Someone actively looks after your site",
  } : {
    web: "Il sito usa le principali protezioni dei browser", mail: "Il dominio blocca le email false a tuo nome", mfa: "Il doppio fattore è attivo",
    off: "Gli accessi vengono tolti quando qualcuno se ne va", pw: "Le password non girano in chat o nei fogli", bak: "I backup sono stati provati con un ripristino vero",
    upd: "Gli aggiornamenti sono regolari", aid: "I dati dei clienti restano fuori dagli strumenti AI", agt: "L'agente AI chiede conferma prima di agire", maint: "Qualcuno segue il sito in modo attivo",
  };

  const pills = (name, opts, type = "radio") => `<div class="picks">${opts.map((o, i) => `<label class="pick"><input type="${type}" name="${name}" value="${i}"><span>${esc(o)}</span></label>`).join("")}</div>`;
  const q = (name, label, opts, type) => `<div class="q-field" data-req="${name}"><p class="q-label">${label}</p>${pills(name, opts, type)}</div>`;

  root.innerHTML = `
  <div class="au-layout">
  <div class="form-card au-card">
    <div class="au-prog"><div class="au-prog-bar"><i></i></div><p><span class="mono au-prog-n"></span><b class="au-prog-t"></b></p></div>
    <p class="au-from-agent" hidden>${T.from_agent}</p>
    <form class="au-form" novalidate>
      <fieldset class="au-step" data-i="0">
        <label class="field ck-domain"><span>${T.domain_q}</span>
          <span class="ck-row"><input name="domain" type="text" inputmode="url" autocomplete="url" maxlength="200" placeholder="${T.domain_ph}"><button type="button" class="btn ck-scan">${T.scan}</button></span>
          <small>${T.domain_hint}</small></label>
        <p class="ck-status" role="status" aria-live="polite"></p>
        <div class="ck-found" hidden></div>
        <label class="check ck-nosite"><input type="checkbox" name="nosite"><span>${T.no_site}</span></label>
      </fieldset>
      <fieldset class="au-step" data-i="1" hidden>
        <div class="q-field"><p class="q-label">${T.have_q}<small>${T.have_hint}</small></p>${pills("have", T.have, "checkbox")}</div>
        ${q("age", T.age_q, T.ages)}
        ${q("php", T.php_q, T.phps)}
        ${q("maint", T.maint_q, T.maints)}
      </fieldset>
      <fieldset class="au-step" data-i="2" hidden>
        ${T.habits.map(([k, label]) => `<div class="q-field ck-yn" data-req="${k}" data-k="${k}"><p class="q-label">${esc(label)}</p>${pills(k, T.yn)}</div>`).join("")}
      </fieldset>
      <fieldset class="au-step" data-i="3" hidden>
        ${q("sector", T.sector_q, T.sectors)}
        ${q("team", T.team_q, T.teams)}
        ${q("role", T.role_q, T.roles)}
        ${q("inc", T.inc_q, T.incs)}
      </fieldset>
      <div class="q-nav"><button type="button" class="btn ghost au-back" hidden>← ${T.back}</button><span></span><button type="button" class="btn au-go">${T.next} →</button></div>
      <p class="form-msg au-msg" role="status" aria-live="polite"></p>
    </form>
    <div class="au-gate" hidden>
      <p class="mono">${T.gate_k}</p><h2 class="au-teaser"></h2><p class="au-teaser-p">${T.gate_p}</p>
      <form class="au-lead" novalidate>
        <label class="field"><span>${T.name}</span><input name="name" required maxlength="80" autocomplete="name"></label>
        <label class="field"><span>${T.company}</span><input name="company" maxlength="80" autocomplete="organization"></label>
        <label class="field full"><span>${T.email}</span><input name="email" type="email" required autocomplete="email"></label>
        <label class="check full"><input type="checkbox" name="consent" required><span>${T.consent}</span></label>
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button type="submit" class="btn full">${T.unlock} →</button>
        <p class="form-msg full au-msg2" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
  <aside class="au-live ck-live" aria-live="polite">
    <p class="mono">${T.live_k}</p>
    <div class="ck-live-res"></div>
    <p class="au-live-empty">${T.live_empty}</p>
    <div class="ck-live-level" hidden><p class="mono">${T.live_level}</p><b></b><i class="ck-meter"><b></b></i></div>
  </aside>
  </div>
  <article class="au-report" hidden></article>`;

  const card = root.querySelector(".au-card"), form = root.querySelector(".au-form");
  const steps = [...form.querySelectorAll(".au-step")];
  const back = form.querySelector(".au-back"), next = form.querySelector(".au-go"), msg = form.querySelector(".au-msg");
  const gate = root.querySelector(".au-gate"), lead = root.querySelector(".au-lead"), report = root.querySelector(".au-report");
  const live = root.querySelector(".ck-live");
  let cur = 0;

  // ---------- controlli pubblici sul dominio ----------
  const scan = { domain: "", done: false, web: null, mail: null, running: false };
  const clean = (v) => String(v || "").trim().toLowerCase().replace(/^[a-z]+:\/\//, "").replace(/[/?#].*$/, "").replace(/:\d+$/, "").replace(/\.$/, "");
  const validDomain = (d) => /^(?=.{4,200}$)([a-z0-9](-*[a-z0-9])*\.)+[a-z]{2,}$/.test(d);
  const withTimeout = (p, ms) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms))]);
  const txt = async (name) => {
    const r = await withTimeout(fetch(`https://dns.google/resolve?name=${encodeURIComponent(name)}&type=TXT`), 8000);
    const j = await r.json();
    return { status: j.Status, records: (j.Answer || []).filter((a) => a.type === 16).map((a) => String(a.data).replace(/"\s*"/g, "").replace(/^"|"$/g, "")) };
  };
  const checkMail = async (d) => {
    const [root_, dm] = await Promise.all([txt(d), txt(`_dmarc.${d}`)]);
    if (root_.status === 3) return { notFound: true };
    const spf = root_.records.some((x) => /^v=spf1/i.test(x));
    const rec = dm.records.find((x) => /^v=DMARC1/i.test(x)) || "";
    const p = (rec.match(/;\s*p=\s*(\w+)/i) || [])[1];
    return { spf, dmarc: rec ? (p || "none").toLowerCase() : null };
  };
  const checkWeb = async (h) => {
    const r = await withTimeout(fetch(`https://observatory-api.mdn.mozilla.net/api/v2/scan?host=${encodeURIComponent(h)}`, { method: "POST" }), 30000);
    const j = await r.json();
    if (!r.ok || j.error || !/^[A-F][+-]?$/.test(String(j.grade))) return null;
    // ogni dato esterno è ostile: numeri come numeri, link solo verso la pagina pubblica di Mozilla
    const url = typeof j.details_url === "string" && j.details_url.startsWith("https://developer.mozilla.org/") ? j.details_url : null;
    return { grade: String(j.grade), failed: Number(j.tests_failed) || 0, total: Number(j.tests_quantity) || 0, url };
  };
  const mailLine = (m) => (m.dmarc === "reject" || m.dmarc === "quarantine" ? T.mail_ok : m.dmarc === "none" ? T.mail_mon : T.mail_none) + (m.spf ? "" : ` · ${T.spf_none}`);
  const tone = (bad) => (bad === 0 ? "ok" : bad === 1 ? "mid" : "bad");
  const webBad = (w) => (!w ? 0 : /^[DF]/.test(w.grade) ? 2 : /^C/.test(w.grade) ? 1 : 0);
  const mailBad = (m) => (!m ? 0 : !m.dmarc ? 2 : m.dmarc === "none" || !m.spf ? 1 : 0);
  const resHtml = () => {
    const rows = [];
    rows.push(`<div class="ck-res ${scan.web ? tone(webBad(scan.web)) : "na"}"><span class="mono">${T.r_web}</span>${scan.web ? `<b class="ck-grade">${esc(scan.web.grade)}</b><p>${T.r_fail(scan.web.failed, scan.web.total)}</p>` : `<p>${T.r_na}</p>`}</div>`);
    rows.push(`<div class="ck-res ${scan.mail ? tone(mailBad(scan.mail)) : "na"}"><span class="mono">${T.r_mail}</span><p>${scan.mail ? mailLine(scan.mail) : T.r_na}</p></div>`);
    return rows.join("");
  };
  const runScan = async () => {
    const input = form.domain, d = clean(input.value), status = form.querySelector(".ck-status"), found = form.querySelector(".ck-found");
    if (!validDomain(d)) { status.textContent = T.bad_domain; input.focus(); return; }
    if (scan.running) return;
    input.value = d;
    Object.assign(scan, { domain: d, done: false, web: null, mail: null, running: true });
    form.nosite.checked = false;
    status.innerHTML = `<span class="ck-spin" aria-hidden="true"></span>${T.scanning}`;
    found.hidden = true;
    const apex = d.replace(/^www\./, "");
    const [m, w] = await Promise.allSettled([checkMail(apex), checkWeb(d)]);
    scan.running = false;
    if (m.status === "fulfilled" && m.value.notFound) { status.textContent = T.not_found; return; }
    scan.mail = m.status === "fulfilled" ? m.value : null;
    scan.web = w.status === "fulfilled" ? w.value : null;
    scan.done = true;
    status.textContent = "";
    found.innerHTML = resHtml();
    found.hidden = false;
    updateLive();
  };
  form.querySelector(".ck-scan").addEventListener("click", runScan);
  form.nosite.addEventListener("change", () => { if (form.nosite.checked) { Object.assign(scan, { domain: "", done: false, web: null, mail: null }); form.querySelector(".ck-found").hidden = true; updateLive(); } });

  // ---------- risposte e punteggio ----------
  const answers = () => {
    const f = new FormData(form), g = (k) => (f.get(k) === null ? -1 : +f.get(k));
    const have = f.getAll("have").map(Number);
    const h = {}; T.habits.forEach(([k]) => { h[k] = g(k); });
    return { have, age: g("age"), php: g("php"), maint: g("maint"), h, sector: g("sector"), team: g("team"), role: g("role"), inc: g("inc"), agent: have.includes(5), aiBuilt: have.includes(4) };
  };
  const score = (a) => {
    const risks = [], good = [];
    const add = (k, w) => risks.push({ k, w });
    const wb = webBad(scan.web);
    if (scan.web) { if (/^[DF]/.test(scan.web.grade)) add("web", 3); else if (/^C/.test(scan.web.grade)) add("web", 2); else if (/^B/.test(scan.web.grade)) add("web", 1); else good.push("web"); }
    if (scan.mail) { const w = (!scan.mail.dmarc ? 3 : scan.mail.dmarc === "none" ? 1 : 0) + (scan.mail.spf ? 0 : 2); if (w) add("mail", w); else good.push("mail"); }
    let old = 0;
    if (a.age === 3 || a.age === 4) old += 2;
    if (a.maint === 2) old += 3; else if (a.maint === 3) old += 2;
    if (old) add("old", Math.min(old, 5)); else if (a.maint === 0 || a.maint === 1) good.push("maint");
    if (a.php === 0) add("php", a.h.upd === 0 ? 2 : 3); else if (a.php === 2) add("php", 2);
    if (a.aiBuilt) add("ai", 2);
    // abitudini: "no" e "non lo so" contano come rischio; per le domande invertite è il "sì" a pesare
    const W = { mfa: 3, off: 3, pw: 2, bak: 2, upd: 2, aid: 2, agt: 3 };
    T.habits.forEach(([k, , inv]) => {
      if (k === "agt" && !a.agent) return;
      const v = a.h[k]; if (v < 0) return;
      const bad = inv ? v !== 1 : v !== 0;
      if (bad) add(k, v === 2 ? Math.max(1, W[k] - 1) : W[k]); else good.push(k);
    });
    if (a.inc > 0) add("inc", 3);
    const total = risks.reduce((s, r) => s + r.w, 0);
    const level = total >= 19 ? 3 : total >= 12 ? 2 : total >= 6 ? 1 : 0;
    // se è già successo qualcosa, è la prima priorità
    risks.sort((x, y) => (y.k === "inc") - (x.k === "inc") || y.w - x.w || R[x.k][4] - R[y.k][4]);
    return { risks, good, total, level, wb };
  };

  const updateLive = () => {
    const resBox = live.querySelector(".ck-live-res"), empty = live.querySelector(".au-live-empty"), lv = live.querySelector(".ck-live-level");
    const has = scan.done || cur > 0;
    // nel primo passo i risultati sono già nel modulo: qui si vedono dal secondo in poi
    resBox.innerHTML = scan.done && cur > 0 ? resHtml() : "";
    empty.hidden = scan.done || form.nosite.checked;
    lv.hidden = !has;
    if (has) {
      const s = score(answers());
      lv.querySelector("b").textContent = T.levels[s.level];
      lv.className = `ck-live-level l${s.level}`;
      lv.querySelector(".ck-meter b").style.width = `${Math.min(100, (s.total / 24) * 100)}%`;
    }
  };
  form.addEventListener("change", (e) => { e.target.closest(".q-field")?.classList.remove("invalid"); updateLive(); });

  // ---------- passi ----------
  const progress = (i) => {
    const n = steps.length;
    card.querySelector(".au-prog-bar i").style.width = `${Math.min(100, ((i + 1) / (n + 1)) * 100)}%`;
    card.querySelector(".au-prog-n").textContent = i < n ? T.step_of(i + 1, n) : "";
    card.querySelector(".au-prog-t").textContent = T.steps[Math.min(i, T.steps.length - 1)];
  };
  const toCard = () => {
    const top = card.getBoundingClientRect().top;
    if (top < 70 || top > window.innerHeight * 0.4) window.scrollTo({ top: window.scrollY + top - 90, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  };
  const show = (i, dir = 1) => {
    cur = i;
    steps.forEach((s, j) => { s.hidden = j !== i; s.classList.toggle("bwd", j === i && dir < 0); });
    back.hidden = i === 0;
    next.textContent = (i === steps.length - 1 ? T.see : T.next) + " →";
    msg.textContent = "";
    // la domanda sull'agente compare solo se c'è un chatbot o agente
    if (i === 2) { const ag = steps[2].querySelector('[data-k="agt"]'); ag.hidden = !answers().agent; }
    progress(i);
    updateLive();
  };
  const valid = () => {
    if (cur === 0) {
      if (scan.running) { msg.textContent = T.scanning; return false; }
      if (!scan.done && !form.nosite.checked) {
        const d = clean(form.domain.value);
        if (validDomain(d)) { runScan(); msg.textContent = T.scanning; return false; }
        msg.textContent = T.need_domain; return false;
      }
      return true;
    }
    let ok = true;
    steps[cur].querySelectorAll("[data-req]").forEach((g) => { if (g.hidden) return; const bad = !g.querySelector("input:checked"); g.classList.toggle("invalid", bad); if (bad) ok = false; });
    if (!ok) msg.textContent = T.need_pick;
    return ok;
  };
  form.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    e.preventDefault();
    if (e.target.name === "domain") runScan(); else next.click();
  });
  next.addEventListener("click", () => {
    if (!valid()) return;
    if (cur < steps.length - 1) { show(cur + 1); toCard(); return; }
    const s = score(answers());
    form.hidden = true; gate.hidden = false;
    progress(steps.length);
    gate.querySelector(".au-teaser").innerHTML = T.gate_h(T.levels[s.level].toLowerCase(), s.risks.length);
    toCard();
    lead.querySelector("input").focus();
  });
  back.addEventListener("click", () => { show(cur - 1, -1); toCard(); });

  // ---------- report ----------
  const svcHref = ([kind, n]) => (kind === "svc" ? `${svcPage}#s${n}` : `${secPage}#s${n}`);
  const mailText = (a, s, name) => {
    const L = [T.mail_intro(name), "", `${T.levels[s.level].toUpperCase()}: ${T.level_p[s.level]}`, ""];
    if (scan.done) {
      L.push(T.r_seen.toUpperCase(), `${scan.domain}`);
      L.push(`- ${T.r_web}: ${scan.web ? `${scan.web.grade} · ${T.r_fail(scan.web.failed, scan.web.total)}` : T.r_na}`);
      L.push(`- ${T.r_mail}: ${scan.mail ? mailLine(scan.mail) : T.r_na}`, "");
    }
    L.push(T.r_prio.toUpperCase());
    s.risks.slice(0, 3).forEach((r, i) => {
      const x = R[r.k];
      L.push(`${i + 1}. ${x[0]} (${T.when[x[4]]})`, `   ${T.p_why}: ${x[1]}`, `   ${T.p_today}: ${x[2]}`, `   ${T.p_us}: ${new URL(svcHref(x[3]), location.href).href}`);
    });
    if (s.risks.length > 3) L.push("", T.r_all.toUpperCase(), ...s.risks.slice(3).map((r) => `- ${R[r.k][0]}`));
    if (s.good.length) L.push("", T.r_good.toUpperCase(), ...s.good.map((k) => `- ${GOOD[k]}`));
    L.push("", T.note, "", T.mail_end);
    return L.join("\n");
  };

  lead.addEventListener("submit", async (e) => {
    e.preventDefault();
    const m2 = lead.querySelector(".au-msg2"), f = new FormData(lead);
    if (f.get("_honey")) return;
    // campi liberi corti e senza parentesi quadre: nessuno può falsificare l'oggetto dell'email ("[URGENTE]")
    const free = (k) => (f.get(k) || "").toString().replace(/[\[\]<>]/g, "").trim().slice(0, 80);
    const email = (f.get("email") || "").toString().trim().slice(0, 160), name = free("name"), company = free("company");
    if (!name) { lead.name.focus(); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { m2.textContent = T.bad_email; lead.email.focus(); return; }
    if (!lead.consent.checked) { m2.textContent = T.need_consent; return; }
    const a = answers(), s = score(a);
    const btn = lead.querySelector("button");
    btn.disabled = true; btn.textContent = T.sending; m2.textContent = "";
    const urgent = a.inc > 0;
    const tag = `[${urgent ? (en ? "URGENT" : "URGENTE") + " · " : ""}${T.levels[s.level].toUpperCase()}]`;
    let ok = true;
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          _subject: `${tag} ${T.subject}: ${company || name} · ${scan.domain || "—"}`, _replyto: email, _template: "table", _captcha: "false",
          _autoresponse: mailText(a, s, name),
          "Fonte": new URLSearchParams(location.search).get("src") === "agent" ? "Check di esposizione (dall'Agent AI)" : "Check di esposizione",
          "Livello": `${T.levels[s.level]} (${s.total} punti)`, "Urgente": urgent ? T.incs[a.inc] : "no",
          "Nome": name, email, "Azienda": company || "—", "Dominio": scan.domain || "nessun sito",
          "Protezioni del sito": scan.web ? `${scan.web.grade} · ${scan.web.failed}/${scan.web.total} non superati · ${scan.web.url}` : "—",
          "Email a nome dell'azienda": scan.mail ? `DMARC ${scan.mail.dmarc || "assente"} · SPF ${scan.mail.spf ? "presente" : "assente"}` : "—",
          "Online": a.have.map((i) => T.have[i]).join("; ") || "—", "Età del sito": a.age >= 0 ? T.ages[a.age] : "—", "PHP / WordPress": a.php >= 0 ? T.phps[a.php] : "—", "Chi se ne occupa": a.maint >= 0 ? T.maints[a.maint] : "—",
          "Abitudini": T.habits.filter(([k]) => a.h[k] >= 0).map(([k, l]) => `${l}: ${T.yn[a.h[k]]}`).join("; "),
          "Settore": a.sector >= 0 ? T.sectors[a.sector] : "—", "Persone": a.team >= 0 ? T.teams[a.team] : "—", "Ruolo": a.role >= 0 ? T.roles[a.role] : "—",
          "Priorità": s.risks.slice(0, 3).map((r) => R[r.k][0]).join("; "), "Altri punti": s.risks.slice(3).map((r) => R[r.k][0]).join("; ") || "—",
        }),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || out.success === false || out.success === "false") throw new Error();
    } catch { ok = false; }
    renderReport(a, s, { name, company, email }, ok);
  });

  function renderReport(a, s, who, sentOk) {
    root.querySelector(".au-layout").hidden = true;
    const date = new Date().toLocaleDateString(en ? "en-GB" : "it-IT", { day: "numeric", month: "long", year: "numeric" });
    const top = s.risks.slice(0, 3), rest = s.risks.slice(3);
    const qs = new URLSearchParams({ need: en ? "Security for websites, apps and AI agents" : "Sicurezza di siti, app e agenti AI", goal: `${T.r_title}: ${T.levels[s.level]}${scan.domain ? ` · ${scan.domain}` : ""}` });
    report.innerHTML = `
      <header class="au-r-head">
        <p class="au-r-brand"><img src="${base}assets/logo-68.png" alt="" width="28" height="28"><b>Reef 7 Lab</b><span class="mono">${date}</span></p>
        <h2>${T.r_title}${who.company ? ` <em>${T.r_for} ${esc(who.company)}</em>` : ""}</h2>
        <p class="au-r-meta">${a.sector >= 0 ? esc(T.sectors[a.sector]) : ""}${a.team >= 0 ? ` · ${esc(T.teams[a.team])} ${en ? "people" : "persone"}` : ""}${scan.domain ? ` · ${esc(scan.domain)}` : ""}</p>
      </header>
      ${sentOk ? `<p class="au-ok">${T.sent_ok(esc(who.email))}</p>` : `<p class="au-warn">${T.sent_fail.replace("{email}", `<a href="mailto:${MAIL}">${MAIL}</a>`)}</p>`}
      <div class="ck-level l${s.level}"><p class="mono">${T.gate_k}</p><h3>${en ? "Exposure" : "Esposizione"}: <em>${T.levels[s.level]}</em></h3><p>${T.level_p[s.level]}</p><i class="ck-meter"><b style="width:${Math.min(100, (s.total / 24) * 100)}%"></b></i></div>
      ${scan.done ? `<section><h3>${T.r_seen}</h3><p class="ck-dom mono">${esc(scan.domain)}</p><div class="ck-found">${resHtml()}</div>${scan.web && scan.web.url ? `<p class="ck-det"><a href="${esc(scan.web.url)}" target="_blank" rel="noopener">${T.r_details} ↗</a></p>` : ""}</section>` : ""}
      ${top.length ? `<section><h3>${T.r_prio}</h3><ol class="ck-prio">${top.map((r) => { const x = R[r.k]; return `<li><div class="ck-p-head"><b>${x[0]}</b><em class="ck-when w${x[4]}">${T.when[x[4]]}</em></div>
          <dl><div><dt>${T.p_why}</dt><dd>${x[1]}</dd></div><div><dt>${T.p_today}</dt><dd>${x[2]}</dd></div><div><dt>${T.p_us}</dt><dd><a href="${svcHref(x[3])}">${T.see_svc} →</a></dd></div></dl></li>`; }).join("")}</ol></section>` : ""}
      ${rest.length ? `<section><h3>${T.r_all}</h3><ul class="ck-list">${rest.map((r) => `<li>${R[r.k][0]}</li>`).join("")}</ul></section>` : ""}
      ${s.good.length ? `<section><h3>${T.r_good}</h3><ul class="ck-list ck-good">${s.good.map((k) => `<li>${GOOD[k]}</li>`).join("")}</ul></section>` : ""}
      <div class="au-sign"><img src="${base}assets/alessandro.jpg" alt="" width="72" height="72"><div><b>${T.sign_h}</b><p>${T.sign_p}</p><span>${T.sign_n} · ${MAIL}</span></div></div>
      <p class="au-note">${T.note}</p>
      <div class="au-actions"><a class="btn" href="${contactPage}?${qs}#contact-form">${T.add} →</a><button type="button" class="btn ghost au-pdf">${T.pdf}</button><button type="button" class="btn ghost au-restart">${T.restart}</button></div>`;
    report.hidden = false;
    report.querySelector(".au-pdf").addEventListener("click", () => window.print());
    report.querySelector(".au-restart").addEventListener("click", () => location.reload());
    report.scrollIntoView({ block: "start", behavior: "smooth" });
  }

  // dominio passato nell'indirizzo (es. dall'Agent AI): parte subito il controllo
  const P = new URLSearchParams(location.search);
  if (P.get("src") === "agent") root.querySelector(".au-from-agent").hidden = false;
  show(0);
  if (P.get("d")) { form.domain.value = P.get("d"); runScan(); }
  // situazione scelta nella pagina Sicurezza: le risposte corrispondenti sono già spuntate
  const SEG = { old: [0], ai: [4], agent: [5] }[P.get("seg")];
  if (SEG) SEG.forEach((i) => { const x = form.querySelector(`input[name="have"][value="${i}"]`); if (x) x.checked = true; });
})();
