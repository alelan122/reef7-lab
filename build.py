"""Genera il sito Reef 7 Lab in italiano (cartella principale) e in inglese (cartella en/).

Uso:  python build.py
Testi ed email si cambiano qui sotto; poi si rilancia lo script.
"""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "lancioni.ale@gmail.com"
SLUG = {
    "it": {"home": "index.html", "services": "servizi.html", "solutions": "soluzioni.html", "studio": "studio.html", "contact": "contatti.html"},
    "en": {"home": "index.html", "services": "services.html", "solutions": "solutions.html", "studio": "studio.html", "contact": "contact.html"},
}
NAV = ["services", "solutions", "studio"]

T = {
"it": {
    "nav": {"services": "Servizi", "solutions": "Soluzioni", "studio": "Studio", "contact": "Contatti"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot": "© 2026 Reef 7 Lab · Studio di sviluppo software",
    "cta_k": "Nuovo progetto", "cta_h": "Pronti a far crescere il vostro <em>reef</em>?",
    "services": [
        ("01", "Siti web", "Siti che trasformano i visitatori in clienti, non in statistiche.",
         "Il sito è la prima stretta di mano con un cliente. Lo progettiamo perché trasmetta autorevolezza in pochi secondi, risponda alle obiezioni prima che vengano poste e porti richieste, non solo visite.",
         ["Strategia, struttura e testi orientati alla conversione", "Design su misura, mai da template", "Velocità di caricamento ai vertici", "Visibilità sui motori di ricerca", "Misurazione di ogni contatto generato"]),
        ("02", "Applicazioni su misura", "Software costruito sul vostro modo di lavorare. Non il contrario.",
         "Quando il software generico costringe l'azienda ad adattarsi, è il momento di invertire la rotta. Costruiamo gestionali, portali clienti e strumenti interni modellati esattamente sui vostri processi.",
         ["Analisi dei processi e prototipo navigabile", "Applicazioni web e desktop", "Ruoli e permessi per ogni utente", "Integrazione con gli strumenti già in uso", "Evoluzione continua dopo il lancio"]),
        ("03", "Intelligenza artificiale", "Il lavoro ripetitivo lo fa l'AI. Il vostro team torna a ciò che conta.",
         "Ogni azienda ha attività che consumano ore senza creare valore. Le individuiamo, le affidiamo all'intelligenza artificiale e restituiamo al team il tempo per vendere, creare e decidere.",
         ["Mappatura delle attività ad alto impatto", "Email, documenti e report gestiti in automatico", "Contatti qualificati e smistati in tempo reale", "Supervisione umana dove serve", "Tempo risparmiato misurato, non stimato"]),
        ("04", "Company brain", "Tutto ciò che sa la vostra azienda, disponibile in un secondo.",
         "Procedure, documenti, decisioni passate: il sapere dell'azienda vive in cartelle, chat e nella testa delle persone. Lo riuniamo in un assistente che risponde al team in tempo reale e cita sempre la fonte.",
         ["Raccolta e organizzazione della conoscenza", "Risposte verificabili, con la fonte", "Accesso calibrato sul ruolo di ciascuno", "Contenuti sempre aggiornati", "Dati aziendali riservati e protetti"]),
        ("05", "Dashboard e dati", "Smettete di inseguire i numeri. Fateveli arrivare.",
         "Le decisioni migliori nascono da dati chiari, non da fogli di calcolo aggiornati a mano. Uniamo le fonti sparse in una vista unica che mostra in tempo reale ciò che conta davvero.",
         ["Definizione degli indicatori che guidano il business", "Collegamento a tutte le fonti di dati", "Aggiornamento automatico", "Viste dedicate per direzione e team", "Avvisi sulle variazioni che richiedono attenzione"]),
    ],
    "sectors": [
        ("E-commerce", "Crescere nelle vendite senza crescere nel lavoro manuale.",
         ["Dashboard di vendite e margini", "Assistenza clienti automatizzata", "Strumenti per ordini e magazzino"],
         "Vendite, campagne e assistenza vivono in strumenti separati. I numeri arrivano tardi e le decisioni si prendono a sensazione.",
         "Un unico sistema che unisce vendite, pubblicità e margini in tempo reale, con l'assistenza di primo livello affidata all'intelligenza artificiale.",
         "Decisioni prese sui dati di oggi, margini sotto controllo e un team libero di concentrarsi sulla crescita."),
        ("Studi professionali", "Meno ore sulla burocrazia, più ore sui clienti.",
         ["Portali clienti riservati", "Archiviazione automatica dei documenti", "Assistente sulle procedure dello studio"],
         "Documenti, scadenze e richieste ripetitive assorbono le ore che dovrebbero andare alla consulenza.",
         "Un portale clienti riservato, documenti archiviati e classificati in automatico e un assistente che conosce a fondo le procedure dello studio.",
         "Più ore fatturabili, meno errori e un servizio percepito come più attento e più rapido."),
        ("Formazione e coaching", "Esperienze digitali all'altezza dei vostri contenuti.",
         ["Piattaforme per corsi e community", "Funnel e automazioni di vendita", "Assistente per studenti e team"],
         "Contenuti di valore dispersi tra piattaforme diverse e processi di vendita gestiti a mano.",
         "Una piattaforma su misura per corsi e community, collegata a funnel e automazioni che accompagnano ogni studente dal primo contatto al risultato.",
         "Un'esperienza coerente che fidelizza e un'attività che scala senza moltiplicare il lavoro del team."),
        ("Aziende in crescita", "Ordine nei processi, fiducia nei numeri.",
         ["Gestionali su misura", "Integrazione degli strumenti esistenti", "Dashboard per la direzione"],
         "Fogli di calcolo, email e software scollegati rallentano l'azienda proprio quando dovrebbe accelerare.",
         "Un gestionale costruito sui vostri processi, integrato con gli strumenti già in uso, con una dashboard che dà alla direzione il quadro completo.",
         "Un'unica fonte di verità per tutta l'azienda e una crescita che non fa perdere il controllo."),
    ],
    "home": {
        "title": "Reef 7 Lab · Studio di sviluppo software",
        "desc": "Siti, applicazioni, intelligenza artificiale e dashboard su misura, collegati in un unico ecosistema.",
        "kicker": "Reef 7 Lab · Studio di sviluppo software",
        "h1": "Il tuo business, <em>connesso</em>.",
        "sub": "Siti, applicazioni e intelligenza artificiale su misura, collegati in un unico ecosistema. Meno lavoro manuale, decisioni più rapide, una crescita che si accumula.",
        "b1": "Parliamo del progetto", "b2": "Scopri i servizi",
        "marquee": ["Siti web", "Applicazioni", "Intelligenza artificiale", "Company brain", "Dashboard", "Automazioni"],
        "statement": 'Alla maggior parte delle aziende non mancano gli strumenti. Ne ha troppi, e non si parlano. <span class="dim">Noi costruiamo l\'ecosistema che li unisce e li fa lavorare per voi.</span>',
        "svc_h": "Servizi", "svc_p": "Cinque discipline, un solo obiettivo: un'azienda più veloce, più informata, più difficile da raggiungere.", "svc_all": "Tutti i servizi",
        "sol_h": "Soluzioni", "sol_p": "Ogni settore ha i suoi colli di bottiglia. Questi sono quelli che trasformiamo più spesso in vantaggi.", "sol_all": "Tutte le soluzioni",
        "reef_h": "Progettati come <em>un reef</em>", "reef_p": "Il reef è uno degli ecosistemi più efficienti della Terra. I suoi cinque principi guidano ogni sistema che costruiamo.",
        "reef_words": ["Diversità", "Simbiosi", "Connessione", "Crescita stratificata", "Resilienza"], "reef_a": "La nostra filosofia",
    },
    "services_p": {
        "title": "Servizi · Reef 7 Lab", "desc": "Siti web, applicazioni su misura, intelligenza artificiale, company brain e dashboard.",
        "h1": "Tecnologia su misura, <em>senza</em> compromessi.",
        "sub": "Dal sito che porta clienti al sistema che governa l'azienda: ogni soluzione nasce dai vostri obiettivi, non da un catalogo.",
    },
    "solutions": {
        "title": "Soluzioni · Reef 7 Lab", "desc": "Soluzioni software per e-commerce, studi professionali, formazione e aziende in crescita.",
        "h1": "Dove gli altri vedono limiti, noi vediamo <em>leve</em>.",
        "sub": "Ogni settore ha i suoi colli di bottiglia. Li conosciamo da vicino, e sappiamo come trasformarli in vantaggi competitivi.",
        "lbl": ("La sfida", "La soluzione", "Il risultato"),
    },
    "studio": {
        "title": "Studio · Reef 7 Lab", "desc": "La filosofia del reef: come Reef 7 Lab progetta software che cresce connesso.",
        "h1": "La filosofia <em>del reef</em>.",
        "sub": "Una barriera corallina copre meno dell'1% dei fondali, eppure ospita un quarto di tutta la vita marina. Il suo segreto non è la grandezza: è l'architettura. È il modello che seguiamo in ogni sistema che costruiamo.",
        "principles": [
            ("01", "Diversità", "In un reef convivono migliaia di specie, ognuna con un ruolo preciso. Nessuna fa tutto, ognuna fa una cosa in modo eccellente. Nel software è lo stesso: un sito, un'automazione, un assistente, una dashboard. Strumenti diversi, scelti per ciò che sanno fare meglio. Mai tecnologia fine a se stessa."),
            ("02", "Simbiosi", "Il corallo vive grazie alle alghe che ospita, e le alghe vivono grazie al corallo. Due organismi che, insieme, costruiscono ciò che da soli non potrebbero. Così lavorano persone e tecnologia nei nostri sistemi: l'intelligenza artificiale si prende il lavoro ripetitivo, le persone ciò che richiede giudizio, creatività e relazioni."),
            ("03", "Connessione", "In un reef nulla vive isolato. Correnti, nutrienti e specie si muovono in un'unica rete, e ogni parte rafforza le altre. I nostri sistemi parlano tra loro: un dato entra una volta sola e arriva ovunque serva. Niente silos, niente copia e incolla, niente versioni diverse della stessa verità."),
            ("04", "Crescita stratificata", "Il corallo cresce pochi millimetri l'anno, strato su strato, e costruisce strutture che durano secoli. Progettiamo con la stessa pazienza: fondamenta solide prima di tutto, poi funzioni che si aggiungono nel tempo. Il risultato è software che accumula valore, invece di invecchiare."),
            ("05", "Resilienza", "Un reef sano resiste alle tempeste e si adatta al cambiamento delle correnti. Il software deve fare lo stesso. Costruiamo architetture flessibili, pronte a evolvere con l'azienda, con il mercato e con le tecnologie che ancora devono arrivare."),
        ],
        "seven_k": "Perché 7",
        "seven_p": "Il 7 è un omaggio ai cantieri navali, dove ogni scafo è costruito su misura, con precisione artigianale, per affrontare il mare aperto. È lo spirito con cui costruiamo software: <span class=\"dim\">fatto a mano, pensato per durare, pronto per le acque difficili.</span>",
        "who_big": "Dietro Reef 7 Lab c'è <em>Alessandro</em>.",
        "who": ["Negli ultimi anni ha progettato software, automazioni e funnel di vendita per aziende in crescita, vedendo da vicino quanto valore si disperde tra strumenti scollegati e processi manuali.",
                "Ha fondato Reef 7 Lab per portare alle aziende ciò che di solito è riservato ai grandi gruppi: sistemi su misura, intelligenza artificiale applicata e un interlocutore che conosce ogni riga del progetto."],
        "sign": ("Alessandro", "Fondatore, Reef 7 Lab"),
        "photo_alt": "Alessandro, fondatore di Reef 7 Lab",
    },
    "contact": {
        "title": "Contatti · Reef 7 Lab", "desc": "Contatta Reef 7 Lab per un nuovo progetto.",
        "h1": "Raccontaci dove vuoi <em>arrivare</em>.",
        "sub": "Una prima conversazione di 30 minuti, senza impegno: capiamo il contesto e ti diciamo con franchezza se, e come, possiamo aiutarti.",
        "or": "Oppure compila il modulo", "or_p": "Il pulsante apre la tua email con il messaggio già pronto.",
        "f": {"name": "Nome", "company": "Azienda", "want": "Area di interesse", "msg": "Il progetto",
              "ph": "Obiettivi, tempi, cosa vorresti migliorare",
              "opts": ["Sito web", "Applicazione su misura", "Intelligenza artificiale", "Company brain", "Dashboard e dati", "Altro"],
              "note": "Rispondiamo entro un giorno lavorativo.", "send": "Invia"},
    },
},
"en": {
    "nav": {"services": "Services", "solutions": "Solutions", "studio": "Studio", "contact": "Contact"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot": "© 2026 Reef 7 Lab · Software development studio",
    "cta_k": "New project", "cta_h": "Ready to grow your <em>reef</em>?",
    "services": [
        ("01", "Websites", "Sites that turn visitors into clients, not statistics.",
         "Your website is the first handshake with a client. We design it to project authority in seconds, answer objections before they're raised and bring in enquiries, not just traffic.",
         ["Conversion-focused strategy, structure and copy", "Custom design, never templates", "Top-tier loading speed", "Search engine visibility", "Every lead tracked and measured"]),
        ("02", "Custom applications", "Software built around the way you work. Not the other way round.",
         "When off-the-shelf software forces your business to adapt, it's time to change course. We build management systems, client portals and internal tools shaped precisely around your processes.",
         ["Process analysis and clickable prototype", "Web and desktop applications", "Roles and permissions for every user", "Integration with the tools you already use", "Continuous evolution after launch"]),
        ("03", "Artificial intelligence", "AI handles the repetitive work. Your team gets back to what matters.",
         "Every company has tasks that eat hours without creating value. We find them, hand them to AI and give your team back the time to sell, create and decide.",
         ["Mapping high-impact tasks", "Email, documents and reports handled automatically", "Leads qualified and routed in real time", "Human oversight where it counts", "Time saved measured, not estimated"]),
        ("04", "Company brain", "Everything your company knows, available in a second.",
         "Procedures, documents, past decisions: company knowledge lives in folders, chats and people's heads. We bring it together in an assistant that answers your team instantly and always cites the source.",
         ["Collecting and structuring knowledge", "Verifiable answers, with sources", "Access tailored to each role", "Always up-to-date content", "Company data kept private and secure"]),
        ("05", "Dashboards and data", "Stop chasing the numbers. Let them come to you.",
         "Great decisions come from clear data, not hand-updated spreadsheets. We bring scattered sources into a single view that shows what really matters, in real time.",
         ["Defining the metrics that drive the business", "Connecting every data source", "Automatic updates", "Dedicated views for leadership and teams", "Alerts on changes that need attention"]),
    ],
    "sectors": [
        ("E-commerce", "Grow sales without growing manual work.",
         ["Sales and margin dashboards", "Automated customer support", "Tools for orders and inventory"],
         "Sales, campaigns and support live in separate tools. The numbers arrive late and decisions are made on gut feel.",
         "One system that brings sales, advertising and margins together in real time, with first-line support handled by AI.",
         "Decisions made on today's data, margins under control and a team free to focus on growth."),
        ("Professional firms", "Fewer hours on paperwork, more hours with clients.",
         ["Private client portals", "Automatic document filing", "Assistant trained on the firm's procedures"],
         "Documents, deadlines and repetitive requests absorb the hours that should go to advisory work.",
         "A private client portal, documents filed and classified automatically, and an assistant that knows the firm's procedures inside out.",
         "More billable hours, fewer errors and a service clients perceive as more attentive and faster."),
        ("Education and coaching", "Digital experiences that match the quality of your content.",
         ["Course and community platforms", "Sales funnels and automation", "Assistant for students and team"],
         "Valuable content scattered across platforms, with sales processes run by hand.",
         "A custom course and community platform, connected to funnels and automations that guide every student from first contact to results.",
         "A consistent experience that builds loyalty, and a business that scales without multiplying the team's workload."),
        ("Growing companies", "Order in your processes, confidence in your numbers.",
         ["Custom management systems", "Integration of existing tools", "Executive dashboards"],
         "Spreadsheets, email and disconnected software slow the company down just when it should accelerate.",
         "A management system built on your processes, integrated with your existing tools, with a dashboard that gives leadership the full picture.",
         "A single source of truth for the whole company, and growth that never costs you control."),
    ],
    "home": {
        "title": "Reef 7 Lab · Software development studio",
        "desc": "Custom websites, applications, AI and dashboards, connected into a single ecosystem.",
        "kicker": "Reef 7 Lab · Software development studio",
        "h1": "Your business, <em>connected</em>.",
        "sub": "Custom websites, applications and AI, connected into a single ecosystem. Less manual work, faster decisions, growth that compounds.",
        "b1": "Start a project", "b2": "Explore services",
        "marquee": ["Websites", "Applications", "Artificial intelligence", "Company brain", "Dashboards", "Automation"],
        "statement": 'Most companies aren\'t short of tools. They have too many, and none of them talk. <span class="dim">We build the ecosystem that connects them and puts them to work for you.</span>',
        "svc_h": "Services", "svc_p": "Five disciplines, one goal: a company that's faster, better informed and harder to catch.", "svc_all": "All services",
        "sol_h": "Solutions", "sol_p": "Every industry has its bottlenecks. These are the ones we most often turn into advantages.", "sol_all": "All solutions",
        "reef_h": "Designed like <em>a reef</em>", "reef_p": "The reef is one of the most efficient ecosystems on Earth. Its five principles shape every system we build.",
        "reef_words": ["Diversity", "Symbiosis", "Connection", "Layered growth", "Resilience"], "reef_a": "Our philosophy",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Websites, custom applications, artificial intelligence, company brain and dashboards.",
        "h1": "Custom technology, <em>no</em> compromises.",
        "sub": "From the website that brings in clients to the system that runs the company: every solution starts from your goals, not from a catalogue.",
    },
    "solutions": {
        "title": "Solutions · Reef 7 Lab", "desc": "Software solutions for e-commerce, professional firms, education and growing companies.",
        "h1": "Where others see limits, we see <em>leverage</em>.",
        "sub": "Every industry has its bottlenecks. We know them up close, and we know how to turn them into competitive advantages.",
        "lbl": ("The challenge", "The solution", "The outcome"),
    },
    "studio": {
        "title": "Studio · Reef 7 Lab", "desc": "The reef philosophy: how Reef 7 Lab designs software that grows connected.",
        "h1": "The reef <em>philosophy</em>.",
        "sub": "Coral reefs cover less than 1% of the ocean floor, yet they're home to a quarter of all marine life. Their secret isn't size: it's architecture. That's the model behind every system we build.",
        "principles": [
            ("01", "Diversity", "Thousands of species share a reef, each with a precise role. None does everything; each does one thing exceptionally well. Software works the same way: a website, an automation, an assistant, a dashboard. Different tools, each chosen for what it does best. Never technology for its own sake."),
            ("02", "Symbiosis", "Coral lives thanks to the algae it hosts, and the algae live thanks to the coral. Together they build what neither could alone. That's how people and technology work in our systems: AI takes on the repetitive work, people take on what needs judgment, creativity and relationships."),
            ("03", "Connection", "Nothing on a reef lives in isolation. Currents, nutrients and species move through a single network, and every part strengthens the others. Our systems talk to each other: data is entered once and reaches everywhere it's needed. No silos, no copy and paste, no competing versions of the truth."),
            ("04", "Layered growth", "Coral grows a few millimetres a year, layer upon layer, building structures that last for centuries. We design with the same patience: solid foundations first, then features added over time. The result is software that compounds in value instead of ageing."),
            ("05", "Resilience", "A healthy reef weathers storms and adapts as currents shift. Software should do the same. We build flexible architectures, ready to evolve with the business, the market and the technologies yet to come."),
        ],
        "seven_k": "Why 7",
        "seven_p": "The 7 is a tribute to shipyards, where every hull is built to measure, with craftsman's precision, to face the open sea. It's the spirit in which we build software: <span class=\"dim\">made by hand, built to last, ready for rough waters.</span>",
        "who_big": "Behind Reef 7 Lab is <em>Alessandro</em>.",
        "who": ["In recent years he has designed software, automations and sales funnels for growing companies, seeing first-hand how much value leaks away between disconnected tools and manual processes.",
                "He founded Reef 7 Lab to bring companies what is usually reserved for large groups: custom systems, applied artificial intelligence and a single point of contact who knows every line of the project."],
        "sign": ("Alessandro", "Founder, Reef 7 Lab"),
        "photo_alt": "Alessandro, founder of Reef 7 Lab",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Contact Reef 7 Lab about a new project.",
        "h1": "Tell us where you want to <em>go</em>.",
        "sub": "A first 30-minute conversation, with no commitment: we learn the context and tell you frankly whether, and how, we can help.",
        "or": "Or use the form", "or_p": "The button opens your email with the message ready to send.",
        "f": {"name": "Name", "company": "Company", "want": "Area of interest", "msg": "Your project",
              "ph": "Goals, timeline, what you'd like to improve",
              "opts": ["Website", "Custom application", "Artificial intelligence", "Company brain", "Dashboards and data", "Other"],
              "note": "We reply within one business day.", "send": "Send"},
    },
},
}


def build(lang):
    L, S = T[lang], SLUG[lang]
    other = "en" if lang == "it" else "it"
    pre = "" if lang == "it" else "../"
    alt_dir = "en/" if lang == "it" else "../"
    u = lambda k: S[k]
    arrow = '<span class="arr" aria-hidden="true">→</span>'

    def page(key, title, desc, body, hero=False):
        links = "".join(f'<a href="{u(k)}"{" aria-current=\"page\"" if k == key else ""}>{L["nav"][k]}</a>' for k in NAV)
        cur = ' aria-current="page"' if key == "contact" else ""
        foot_links = "".join(f'<a href="{u(k)}">{L["nav"][k]}</a>' for k in NAV + ["contact"])
        alt = f"{alt_dir}{SLUG[other][key]}"
        band = "" if key == "contact" else f"""
<section class="cta-band"><div class="wrap"><a href="{u('contact')}">
  <div><p class="mono">{L['cta_k']}</p><h2>{L['cta_h']}</h2></div><span class="circle" aria-hidden="true">→</span>
</a></div></section>"""
        return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#04080f">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{pre}assets/reef7-logo.png">
  <link rel="alternate" hreflang="{other}" href="{alt}">
  <link rel="icon" href="{pre}assets/favicon.png">
  <link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}styles.css">
</head>
<body>
<header class="top{'' if hero else ' solid'}"><div class="wrap top-in">
  <a class="logo" href="{u('home')}"><img src="{pre}assets/reef7-logo.png" alt="" width="34" height="34">Reef 7 Lab</a>
  <nav aria-label="{L['pages']}">{links}<a href="{u('contact')}" class="cta"{cur}>{L['nav']['contact']}</a></nav>
  <a class="lang" href="{alt}" hreflang="{other}" lang="{other}">{other.upper()}</a>
  <button class="menu" aria-expanded="false" data-close="{L['close']}">{L['menu']}</button>
</div></header>
<main>
{body}
</main>{band}
<footer class="foot"><div class="wrap foot-in">
  <span>{L['foot']}</span>
  <nav aria-label="{L['pages']}">{foot_links}</nav>
  <a class="r" href="mailto:{EMAIL}">{EMAIL}</a>
</div></footer>
<script>window.REEF = {{ email: "{EMAIL}" }};</script>
<script src="{pre}site.js"></script>
</body>
</html>
"""

    def head_block(kicker, h1, sub=""):
        return f"""<section class="page-head"><div class="wrap">
  <p class="mono">{kicker}</p>
  <h1>{h1}</h1>{f'<p class="sub">{sub}</p>' if sub else ''}
</div></section>"""

    out = {}

    # home
    H = L["home"]
    rows = "".join(f"""
    <a class="svc-row" href="{u('services')}#s{n}"><span class="mono">{n}</span><h3>{t}</h3><p>{d}</p><span class="go" aria-hidden="true">→</span></a>""" for n, t, d, *_ in L["services"])
    words = "".join(f"<span>{w}</span>" for w in H["marquee"])
    sectors = "".join(f"""
    <a class="sector" href="{u('solutions')}#k{i}"><span class="mono">0{i}</span><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></a>""" for i, (t, d, li, *_) in enumerate(L["sectors"][:3], 1))
    reef_words = "".join(f'<div><span class="mono">0{i}</span><b>{w}</b></div>' for i, w in enumerate(H["reef_words"], 1))
    out["home"] = page("home", H["title"], H["desc"], f"""<section class="hero">
  <canvas id="water" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <p class="mono">{H['kicker']}</p>
    <h1>{H['h1']}</h1>
    <div class="hero-foot">
      <p>{H['sub']}</p>
      <div class="actions"><a class="btn" href="{u('contact')}">{H['b1']} {arrow}</a><a class="btn ghost" href="{u('services')}">{H['b2']}</a></div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{words}{words}</div></div>
<section class="statement"><div class="wrap"><p>{H['statement']}</p></div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{H['svc_h']}</h2><p>{H['svc_p']}</p></div>
  <div class="svc-list">{rows}
  </div>
  <a class="link" href="{u('services')}">{H['svc_all']} {arrow}</a>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{H['sol_h']}</h2><p>{H['sol_p']}</p></div>
  <div class="sectors">{sectors}
  </div>
  <a class="link" href="{u('solutions')}">{H['sol_all']} {arrow}</a>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{H['reef_h']}</h2><p>{H['reef_p']}</p></div>
  <div class="principles">{reef_words}</div>
  <a class="link" href="{u('studio')}">{H['reef_a']} {arrow}</a>
</div></section>""", hero=True)

    # servizi
    SP = L["services_p"]
    svc = "".join(f"""
  <article class="svc" id="s{n}">
    <span class="mono">{n}</span>
    <div><h2>{t}</h2><p class="tag">{short}</p><p class="lead">{long}</p></div>
    <div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
  </article>""" for n, t, short, long, li in L["services"])
    out["services"] = page("services", SP["title"], SP["desc"], head_block(L["nav"]["services"], SP["h1"], SP["sub"]) + f"""
<section class="wrap" style="padding-bottom:clamp(80px,10vw,150px)">{svc}
</section>""")

    # soluzioni
    SO = L["solutions"]; lb = SO["lbl"]
    cases = "".join(f"""
  <article class="case" id="k{i}">
    <span class="mono">0{i}</span>
    <div><h2>{t}</h2><p class="lead">{d}</p></div>
    <div><dl><div><dt>{lb[0]}</dt><dd>{a}</dd></div><div><dt>{lb[1]}</dt><dd>{b}</dd></div><div><dt>{lb[2]}</dt><dd>{c}</dd></div></dl></div>
  </article>""" for i, (t, d, _, a, b, c) in enumerate(L["sectors"], 1))
    out["solutions"] = page("solutions", SO["title"], SO["desc"], head_block(L["nav"]["solutions"], SO["h1"], SO["sub"]) + f"""
<section class="wrap" style="padding-bottom:clamp(80px,10vw,150px)">{cases}
</section>""")

    # studio
    St = L["studio"]
    pr = "".join(f"""
  <article class="principle"><span class="mono">{n}</span><h2>{t}</h2><p>{d}</p></article>""" for n, t, d in St["principles"])
    who = "".join(f"<p>{p}</p>" for p in St["who"])
    out["studio"] = page("studio", St["title"], St["desc"], head_block(L["nav"]["studio"], St["h1"], St["sub"]) + f"""
<section class="wrap principle-list">{pr}
</section>
<section class="statement" style="border-top:1px solid var(--rule)"><div class="wrap">
  <p class="mono" style="margin-bottom:28px">{St['seven_k']}</p>
  <p>{St['seven_p']}</p>
</div></section>
<section class="block"><div class="wrap about">
  <div class="portrait"><img src="{pre}assets/alessandro.jpg" alt="{St['photo_alt']}" width="512" height="512"></div>
  <div><p class="big">{St['who_big']}</p>{who}
    <div class="sign"><b>{St['sign'][0]}</b><span>{St['sign'][1]}</span></div></div>
</div></section>""")

    # contatti
    C = L["contact"]; F = C["f"]
    opts = "".join(f"<option>{o}</option>" for o in F["opts"])
    out["contact"] = page("contact", C["title"], C["desc"], head_block(L["nav"]["contact"], C["h1"], C["sub"]) + f"""
<section class="wrap" style="padding-bottom:clamp(56px,7vw,100px)"><a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a></section>
<section class="block"><div class="wrap contact-grid">
  <div><p class="mono">{C['or']}</p><p style="color:var(--muted);margin-top:14px;max-width:340px">{C['or_p']}</p></div>
  <form class="form" id="contact-form">
    <label><span class="mono">{F['name']}</span><input name="nome" required autocomplete="name"></label>
    <label><span class="mono">{F['company']}</span><input name="azienda" autocomplete="organization"></label>
    <label class="full"><span class="mono">{F['want']}</span><select name="servizio">{opts}</select></label>
    <label class="full"><span class="mono">{F['msg']}</span><textarea name="messaggio" required placeholder="{F['ph']}"></textarea></label>
    <div class="send full"><p>{F['note']}</p><button class="btn" type="submit">{F['send']} {arrow}</button></div>
  </form>
</div></section>""")

    folder = ROOT if lang == "it" else ROOT / "en"
    folder.mkdir(exist_ok=True)
    for key, html in out.items():
        (folder / S[key]).write_text(html, encoding="utf-8")
        print("ok", lang, S[key])


if __name__ == "__main__":
    # toglie le pagine delle versioni precedenti (prezzi e lavori)
    for old in ["lavori.html", "prezzi.html", "en/work.html", "en/pricing.html"]:
        (ROOT / old).unlink(missing_ok=True)
    for lang in T:
        build(lang)
