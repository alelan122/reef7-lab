"""Genera il sito Reef 7 Lab in italiano (cartella principale) e in inglese (cartella en/).

Uso:  python build.py
Testi ed email si cambiano qui sotto; poi si rilancia lo script.
"""
import hashlib
import math
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "lancioni.ale@gmail.com"
# versione dei file di stile e script: cambia quando cambiano, così il browser non usa copie vecchie

# ---------------- Missione: il 5% degli introiti al mare ----------------
SHARE = 5        # percentuale degli introiti di ogni progetto destinata al mare
RAISED = 0       # euro già destinati finora: aggiornalo dopo ogni donazione e rilancia lo script
# obiettivi in ordine: (latitudine, longitudine, obiettivo in euro, organizzazione, sito)
GOALS = [
    (10.09, 99.84, 5000, "New Heaven Reef Conservation", "https://www.newheavenreefconservation.org"),
    (27.26, 33.81, 7500, "HEPCA", "https://www.hepca.org"),
    (-1.90, 130.20, 10000, "Misool Foundation", "https://www.misoolfoundation.org"),
    (-8.70, 115.20, 12500, "Coral Triangle Center", "https://coraltrianglecenter.org"),
    (4.17, 73.50, 15000, "Reefscapers", "https://reefscapers.com"),
    (-17.53, -149.83, 20000, "Coral Gardeners", "https://coralgardeners.org"),
    (-18.30, 147.70, 30000, "Great Barrier Reef Foundation", "https://www.barrierreef.org"),
]
MT = {
"it": {
    "title": "Missione · Reef 7 Lab", "desc": "Il 5% degli introiti di ogni progetto di Reef 7 Lab va a chi protegge la flora e la fauna marina.",
    "h1": f"Il {SHARE}% di ogni progetto <em>torna al mare</em>.",
    "sub": f"Il nostro nome viene dal reef, e il reef è in pericolo: dagli anni '50 la copertura di corallo vivo nel mondo si è dimezzata. Per questo il {SHARE}% degli introiti di ogni progetto va a organizzazioni che proteggono la flora e la fauna marina.",
    "stats": [(f"{SHARE}%", "degli introiti di ogni progetto"), (None, "destinati al mare finora"), (str(len(GOALS)), "reef da sostenere, uno dopo l'altro")],
    "how_h": "Come funziona", "how": [("Ogni progetto", f"Il {SHARE}% di ciò che il cliente paga viene accantonato fin dal primo giorno."),
                                      ("Un obiettivo alla volta", "Il fondo va al reef in corso. Raggiunto l'obiettivo, si passa al successivo."),
                                      ("Tutto trasparente", "Questa pagina mostra i fondi destinati e l'avanzamento di ogni obiettivo.")],
    "map_h": "I reef che <em>sosterremo</em>", "map_p": "Sette barriere coralline tra le più preziose del pianeta, dal Mar Rosso alla Polinesia.",
    "goals_h": "Prossimi obiettivi", "goals_p": "Come una raccolta fondi: ogni barra si riempie con i progetti che realizziamo.",
    "places": [("Koh Tao", "Thailandia", "Vivai e restauro dei coralli nel Golfo di Thailandia."),
               ("Mar Rosso", "Egitto", "Boe d'ormeggio e protezione delle barriere dalle ancore."),
               ("Raja Ampat", "Indonesia", "Aree marine protette e pattugliamento contro la pesca illegale."),
               ("Bali", "Indonesia", "Conservazione e formazione nel Triangolo dei Coralli."),
               ("Maldive", "Oceano Indiano", "Trapianto di coralli su strutture di ricrescita."),
               ("Moorea", "Polinesia francese", "Coltivazione di coralli più resistenti al calore."),
               ("Grande Barriera Corallina", "Australia", "Ricerca e ripristino del reef più grande del mondo.")],
    "raised_of": "{r} raccolti di {t}", "active": "In corso", "next": "Prossimo", "done": "Raggiunto",
    "partner": "Organizzazione", "visit": "Sito",
    "note": "Le organizzazioni indicate sono quelle a cui intendiamo destinare i contributi; non rappresentano una partnership ufficiale.",
    "why_k": "Non è marketing", "why_h": "Il mare, prima di tutto, <em>da volontari</em>.",
    "why_p": ["Prima di Reef 7 Lab, Alessandro è stato per diversi anni membro attivo di 2hands Ancona, il gruppo di volontari che ripulisce spiagge e coste dai rifiuti.",
              "Reef 7 Lab porta lo stesso impegno nel lavoro di ogni giorno: ogni progetto che realizziamo contribuisce a proteggere il mare da cui prendiamo il nome."],
    "home_k": "Missione", "home_h": f"Il {SHARE}% torna <em>al mare</em>.", "home_p": f"Ogni progetto che realizziamo finanzia la protezione delle barriere coralline. Il prossimo obiettivo:",
    "home_a": "Scopri la missione",
},
"en": {
    "title": "Mission · Reef 7 Lab", "desc": "5% of revenue from every Reef 7 Lab project goes to organisations protecting marine life.",
    "h1": f"{SHARE}% of every project <em>goes back to the sea</em>.",
    "sub": f"Our name comes from the reef, and reefs are in danger: since the 1950s, the world's living coral cover has halved. That's why {SHARE}% of revenue from every project goes to organisations protecting marine flora and fauna.",
    "stats": [(f"{SHARE}%", "of revenue from every project"), (None, "given to the ocean so far"), (str(len(GOALS)), "reefs to support, one after another")],
    "how_h": "How it works", "how": [("Every project", f"{SHARE}% of what the client pays is set aside from day one."),
                                     ("One goal at a time", "The fund goes to the current reef. Once the goal is reached, we move to the next."),
                                     ("Fully transparent", "This page shows the funds given and the progress of every goal.")],
    "map_h": "The reefs we'll <em>support</em>", "map_p": "Seven of the most precious coral reefs on the planet, from the Red Sea to Polynesia.",
    "goals_h": "Next goals", "goals_p": "Like a crowdfunding campaign: every bar fills up with the projects we deliver.",
    "places": [("Koh Tao", "Thailand", "Coral nurseries and reef restoration in the Gulf of Thailand."),
               ("Red Sea", "Egypt", "Mooring buoys that protect reefs from anchor damage."),
               ("Raja Ampat", "Indonesia", "Marine protected areas and patrols against illegal fishing."),
               ("Bali", "Indonesia", "Conservation and training in the Coral Triangle."),
               ("Maldives", "Indian Ocean", "Coral transplants onto regrowth frames."),
               ("Moorea", "French Polynesia", "Growing heat-resistant corals."),
               ("Great Barrier Reef", "Australia", "Research and restoration of the world's largest reef.")],
    "raised_of": "{r} raised of {t}", "active": "In progress", "next": "Next", "done": "Reached",
    "partner": "Organisation", "visit": "Website",
    "note": "The organisations listed are those we intend to direct our contributions to; this does not represent an official partnership.",
    "why_k": "Not a marketing line", "why_h": "The sea came first, <em>as volunteers</em>.",
    "why_p": ["Before Reef 7 Lab, Alessandro spent several years as an active member of 2hands Ancona, the volunteer group that cleans beaches and coastlines of litter.",
              "Reef 7 Lab brings the same commitment to everyday work: every project we deliver helps protect the sea we're named after."],
    "home_k": "Mission", "home_h": f"{SHARE}% goes back <em>to the sea</em>.", "home_p": "Every project we deliver funds the protection of coral reefs. Our next goal:",
    "home_a": "Discover the mission",
},
}


def euro(v, lang):
    s = f"{v:,.0f}"
    return (s.replace(",", ".") + " €") if lang == "it" else ("€" + s)


def goal_state():
    """Distribuisce i fondi raccolti sugli obiettivi in ordine: (raccolto, percentuale) per ciascuno, e l'indice di quello in corso."""
    left, out, active = RAISED, [], None
    for i, (*_, target, _o, _u) in enumerate(GOALS):
        got = min(left, target)
        left -= got
        out.append((got, round(got / target * 100)))
        if active is None and got < target:
            active = i
    return out, active


VERSION = hashlib.md5(b"".join((ROOT / f).read_bytes() for f in ["styles.css", "alt-overrides.css", "site.js", "mission.js"])).hexdigest()[:8]
SLUG = {
    "it": {"home": "index.html", "services": "servizi.html", "solutions": "soluzioni.html", "mission": "missione.html", "studio": "lab.html", "contact": "contatti.html"},
    "en": {"home": "index.html", "services": "services.html", "solutions": "solutions.html", "mission": "mission.html", "studio": "lab.html", "contact": "contact.html"},
}
NAV = ["services", "solutions", "mission", "studio"]

T = {
"it": {
    "nav": {"services": "Servizi", "solutions": "Soluzioni", "mission": "Missione", "studio": "Lab", "contact": "Contatti"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot": "© 2026 Reef 7 Lab · Sviluppo software e intelligenza artificiale",
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
        "title": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "desc": "Siti, applicazioni, intelligenza artificiale e dashboard su misura, collegati in un unico ecosistema.",
        "kicker": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "h1": "Il tuo business, <em>connesso</em>.",
        "sub": "Siti, applicazioni e intelligenza artificiale su misura, collegati in un unico ecosistema. Meno lavoro manuale, decisioni più rapide, una crescita che si accumula.",
        "b1": "Parliamo del progetto", "b2": "Scopri i servizi",
        "eco_k": "Il problema che risolviamo",
        "eco_h": "I tuoi strumenti, finalmente <em>in squadra</em>.",
        "eco_p": "Il cliente scrive su WhatsApp, l'ordine arriva dall'e-commerce, la fattura parte da un altro programma e i numeri finiscono in un Excel che nessuno aggiorna. Colleghiamo tutto in un unico sistema: ogni informazione entra una volta sola e arriva dove serve.",
        "tools": ["Email", "WhatsApp", "Excel", "CRM", "E-commerce", "Contabilità"],
        "before": ("Oggi", ["Dati copiati a mano da un programma all'altro", "Ogni reparto con la sua versione dei numeri", "Decisioni prese su dati vecchi"]),
        "after": ("Con Reef 7 Lab", ["Ogni dato inserito una volta sola", "Un'unica fonte di verità per tutta l'azienda", "Numeri aggiornati in tempo reale"]),
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
        "title": "Lab · Reef 7 Lab", "desc": "La filosofia del reef: come Reef 7 Lab progetta software che cresce connesso.",
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
        "seven_p": "Il 7 sta per i giorni della settimana. I sistemi che costruiamo non vanno in ferie e non staccano alle sei: lavorano sette giorni su sette, <span class=\"dim\">anche quando il vostro team riposa.</span>",
        "who_big": "Dietro Reef 7 Lab c'è <em>Alessandro</em>.",
        "who": ["Negli ultimi anni ha progettato software, automazioni e funnel di vendita per aziende in crescita, vedendo da vicino quanto valore si disperde tra strumenti scollegati e processi manuali.",
                "Ha fondato Reef 7 Lab per portare alle aziende ciò che di solito è riservato ai grandi gruppi: sistemi su misura, intelligenza artificiale applicata e un interlocutore che conosce ogni riga del progetto.",
                "Il legame con il mare è personale: per diversi anni è stato membro attivo di 2hands Ancona, il gruppo di volontari che ripulisce spiagge e coste dai rifiuti."],
        "sign": ("Alessandro", "Fondatore, Reef 7 Lab"),
        "photo_alt": "Alessandro, fondatore di Reef 7 Lab",
    },
    "contact": {
        "title": "Contatti · Reef 7 Lab", "desc": "Contatta Reef 7 Lab per un nuovo progetto.",
        "h1": "Raccontaci dove vuoi <em>arrivare</em>.",
        "sub": "Una prima conversazione di 30 minuti, senza impegno: capiamo il contesto e ti diciamo con franchezza se, e come, possiamo aiutarti.",
        "info": [("Email", None), ("Tempi di risposta", "Entro un giorno lavorativo"), ("Dove", "Italia · lavoriamo anche da remoto"), ("Lingue", "Italiano, English")],
        "next_k": "Cosa succede dopo",
        "next": [("Ci scrivi", "Raccontaci obiettivi, tempi e contesto. Bastano poche righe."),
                 ("Ti rispondiamo", "Entro un giorno lavorativo, con le prime domande e una proposta di data."),
                 ("Prima consulenza", "30 minuti, gratuita e senza impegno, per capire se e come possiamo aiutarti.")],
        "form_h": "Richiedi una consulenza",
        "f": {"name": "Nome e cognome", "email": "Email di lavoro", "company": "Azienda", "want": "Di cosa hai bisogno",
              "msg": "Raccontaci il progetto", "ph": "Obiettivi, tempi e cosa vorresti migliorare",
              "opts": ["Sito web", "Applicazione su misura", "Intelligenza artificiale", "Company brain", "Dashboard e dati", "Non lo so ancora"],
              "privacy": "Acconsento al trattamento dei miei dati per essere ricontattato in merito alla richiesta.",
              "req": "Campi obbligatori", "send": "Invia la richiesta", "sending": "Invio in corso…",
              "ok_h": "Richiesta inviata.", "ok_p": "Grazie! Ti risponderemo entro un giorno lavorativo all'indirizzo che ci hai indicato.",
              "err": "Invio non riuscito. Riprova o scrivici direttamente a"},
        "subject": "Nuova richiesta dal sito",
    },
},
"en": {
    "nav": {"services": "Services", "solutions": "Solutions", "mission": "Mission", "studio": "Lab", "contact": "Contact"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot": "© 2026 Reef 7 Lab · Software and AI development",
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
        "title": "Reef 7 Lab · Software and AI development",
        "desc": "Custom websites, applications, AI and dashboards, connected into a single ecosystem.",
        "kicker": "Reef 7 Lab · Software and AI development",
        "h1": "Your business, <em>connected</em>.",
        "sub": "Custom websites, applications and AI, connected into a single ecosystem. Less manual work, faster decisions, growth that compounds.",
        "b1": "Start a project", "b2": "Explore services",
        "eco_k": "The problem we solve",
        "eco_h": "Your tools, finally <em>working together</em>.",
        "eco_p": "A client messages on WhatsApp, the order comes in through your store, the invoice goes out from another program and the numbers end up in a spreadsheet nobody updates. We connect everything into one system: every piece of information is entered once and reaches wherever it's needed.",
        "tools": ["Email", "WhatsApp", "Spreadsheets", "CRM", "E-commerce", "Accounting"],
        "before": ("Today", ["Data copied by hand from one program to another", "Every team with its own version of the numbers", "Decisions made on outdated data"]),
        "after": ("With Reef 7 Lab", ["Every piece of data entered once", "One source of truth for the whole company", "Numbers updated in real time"]),
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
        "title": "Lab · Reef 7 Lab", "desc": "The reef philosophy: how Reef 7 Lab designs software that grows connected.",
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
        "seven_p": "The 7 stands for the days of the week. The systems we build don't take holidays or clock off at six: they work seven days a week, <span class=\"dim\">even while your team rests.</span>",
        "who_big": "Behind Reef 7 Lab is <em>Alessandro</em>.",
        "who": ["In recent years he has designed software, automations and sales funnels for growing companies, seeing first-hand how much value leaks away between disconnected tools and manual processes.",
                "He founded Reef 7 Lab to bring companies what is usually reserved for large groups: custom systems, applied artificial intelligence and a single point of contact who knows every line of the project.",
                "His connection to the sea is personal: for several years he was an active member of 2hands Ancona, the volunteer group that cleans beaches and coastlines of litter."],
        "sign": ("Alessandro", "Founder, Reef 7 Lab"),
        "photo_alt": "Alessandro, founder of Reef 7 Lab",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Contact Reef 7 Lab about a new project.",
        "h1": "Tell us where you want to <em>go</em>.",
        "sub": "A first 30-minute conversation, with no commitment: we learn the context and tell you frankly whether, and how, we can help.",
        "info": [("Email", None), ("Response time", "Within one business day"), ("Based in", "Italy · working remotely"), ("Languages", "English, Italiano")],
        "next_k": "What happens next",
        "next": [("You write to us", "Tell us about your goals, timeline and context. A few lines are enough."),
                 ("We reply", "Within one business day, with a few first questions and a proposed date."),
                 ("First consultation", "30 minutes, free and with no commitment, to see whether and how we can help.")],
        "form_h": "Request a consultation",
        "f": {"name": "Full name", "email": "Work email", "company": "Company", "want": "What do you need",
              "msg": "Tell us about the project", "ph": "Goals, timeline and what you'd like to improve",
              "opts": ["Website", "Custom application", "Artificial intelligence", "Company brain", "Dashboards and data", "Not sure yet"],
              "privacy": "I agree to the processing of my data so you can get back to me about this request.",
              "req": "Required fields", "send": "Send request", "sending": "Sending…",
              "ok_h": "Request sent.", "ok_p": "Thank you! We'll reply within one business day at the address you provided.",
              "err": "Something went wrong. Please try again or email us directly at"},
        "subject": "New enquiry from the website",
    },
},
}


def eco(H, pre):
    """Sezione prima/dopo: strumenti sparsi e scollegati, poi gli stessi collegati a un unico centro."""
    tools = H["tools"]
    # prima: posizioni sparse, leggermente ruotate, con collegamenti interrotti
    spots = [(22, 24, -6), (70, 18, 5), (48, 50, -3), (18, 74, 4), (78, 62, -5), (55, 86, 3)]
    broken = [(0, 2), (1, 4), (3, 5), (2, 4)]
    seg = ""
    for a, b in broken:
        (x1, y1, _), (x2, y2, _) = spots[a], spots[b]
        for (sx, sy), (ex, ey) in (((x1, y1), (x2, y2)), ((x2, y2), (x1, y1))):
            mx, my = sx + (ex - sx) * .38, sy + (ey - sy) * .38
            seg += f'<line x1="{sx}" y1="{sy}" x2="{mx:.1f}" y2="{my:.1f}"/>'
    # dopo: in cerchio attorno al centro, con il flusso dei dati
    ring = [(50 + 36 * math.cos(math.radians(-90 + i * 60)), 50 + 38 * math.sin(math.radians(-90 + i * 60))) for i in range(6)]
    lines = "".join(f'<line x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}" style="animation-delay:{-i * .35:.2f}s"/>' for i, (x, y) in enumerate(ring))
    # una sola scena: ogni strumento conosce la posizione "prima" e "dopo", il CSS anima il passaggio
    pills = "".join(f'<span class="pill" style="--bx:{bx}%;--by:{by}%;--br:{br}deg;--ax:{ax:.1f}%;--ay:{ay:.1f}%;--d:{i * 70}ms">{t}</span>'
                    for i, (t, (bx, by, br), (ax, ay)) in enumerate(zip(tools, spots, ring)))
    li = lambda items, cls: "".join(f'<li class="{cls}">{x}</li>' for x in items)
    (bk, bl), (ak, al) = H["before"], H["after"]
    return f"""<div class="eco is-after" data-eco>
    <div class="eco-copy">
      <p class="mono">{H['eco_k']}</p>
      <h2>{H['eco_h']}</h2>
      <p class="eco-lead">{H['eco_p']}</p>
      <div class="eco-toggle" role="group">
        <button type="button" data-state="before" aria-pressed="false">{bk}</button>
        <button type="button" data-state="after" aria-pressed="true">{ak}</button>
      </div>
      <ul class="eco-list before-list">{li(bl, "x")}</ul>
      <ul class="eco-list after-list">{li(al, "ok")}</ul>
    </div>
    <div class="eco-stage" aria-hidden="true">
      <svg viewBox="0 0 100 100" preserveAspectRatio="none"><g class="broken">{seg}</g><g class="links">{lines}</g></svg>
      {pills}
      <span class="hub"><img src="{pre}assets/reef7-logo.png" alt="" width="64" height="64"></span>
    </div>
  </div>"""


def build(lang, variant=""):
    """variant="" genera il sito principale; variant="alt" la versione B (stile editoriale) nella cartella alt/."""
    L, S = T[lang], SLUG[lang]
    other = "en" if lang == "it" else "it"
    pre = ("../" if variant else "") + ("" if lang == "it" else "../")
    css = "alt.css" if variant else "styles.css"
    alt_dir = "en/" if lang == "it" else "../"
    u = lambda k: S[k]
    arrow = '<span class="arr" aria-hidden="true">→</span>'

    def page(key, title, desc, body, hero=False, extra=""):
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
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}{css}?v={VERSION}">
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
<script src="{pre}site.js?v={VERSION}"></script>{extra}
</body>
</html>
"""

    def head_block(kicker, h1, sub=""):
        return f"""<section class="page-head"><div class="wrap">
  <p class="mono">{kicker}</p>
  <h1>{h1}</h1>{f'<p class="sub">{sub}</p>' if sub else ''}
</div></section>"""

    out = {}

    # missione: stato degli obiettivi e scheda di ogni reef
    M = MT[lang]
    states, active = goal_state()
    active = active if active is not None else len(GOALS) - 1

    def goal_card(i):
        lat, lon, target, org, url = GOALS[i]
        place, country, what = M["places"][i]
        got, pct = states[i]
        status = M["done"] if pct >= 100 else M["active"] if i == active else M["next"]
        cls = "done" if pct >= 100 else "active" if i == active else ""
        return f"""<article class="goal {cls}" id="g{i + 1}">
      <div class="goal-top"><span class="goal-n">{i + 1:02d}</span><span class="chip">{status}</span></div>
      <h3>{place}</h3><p class="goal-country mono">{country}</p>
      <p class="goal-what">{what}</p>
      <div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}"><i style="width:{max(pct, 0)}%"></i></div>
      <div class="goal-num"><span>{M['raised_of'].format(r=euro(got, lang), t=euro(target, lang))}</span><b>{pct}%</b></div>
      <p class="goal-org"><span class="mono">{M['partner']}</span> <a href="{url}" target="_blank" rel="noopener">{org} ↗</a></p>
    </article>"""

    # home
    H = L["home"]
    rows = "".join(f"""
    <a class="svc-row" href="{u('services')}#s{n}"><span class="mono">{n}</span><h3>{t}</h3><p>{d}</p><span class="go" aria-hidden="true">→</span></a>""" for n, t, d, *_ in L["services"])
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
<section class="block"><div class="wrap">
  {eco(H, pre)}
</div></section>
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
<section class="block ocean"><div class="wrap ocean-in">
  <div><p class="mono">{M['home_k']}</p><h2>{M['home_h']}</h2><p class="ocean-p">{M['home_p']}</p>
    <a class="link" href="{u('mission')}">{M['home_a']} {arrow}</a></div>
  <div class="goals">{goal_card(active)}</div>
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

    # missione
    stats = "".join(f'<div><b>{v if v is not None else euro(RAISED, lang)}</b><p>{t}</p></div>' for v, t in M["stats"])
    how = "".join(f'<div><span class="mono">0{i}</span><b>{t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(M["how"], 1))
    points = [{"n": i + 1, "lat": g[0], "lon": g[1], "name": M["places"][i][0], "active": i == active} for i, g in enumerate(GOALS)]
    import json
    map_data = json.dumps(points, ensure_ascii=False).replace('"', "&quot;")
    cards = "".join(goal_card(i) for i in range(len(GOALS)))
    why = "".join(f"<p>{p}</p>" for p in M["why_p"])
    libs = """
<script src="https://cdn.jsdelivr.net/npm/d3-array@3.2.4/dist/d3-array.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-geo@3.1.1/dist/d3-geo.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js"></script>"""
    out["mission"] = page("mission", M["title"], M["desc"], head_block(L["nav"]["mission"], M["h1"], M["sub"]) + f"""
<section class="wrap"><div class="figures">{stats}</div></section>
<section class="block" style="border-top:0"><div class="wrap">
  <div class="head"><h2>{M['how_h']}</h2></div>
  <div class="how">{how}</div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{M['map_h']}</h2><p>{M['map_p']}</p></div>
  <div class="reef-map" id="reef-map" data-points="{map_data}" data-world="https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-110m.json">
    <svg viewBox="0 0 1000 500" role="img" aria-label="{M['map_h'].replace('<em>', '').replace('</em>', '')}"></svg>
  </div>
  <ol class="map-legend">{"".join(f'<li><a href="#g{p["n"]}"><span>{p["n"]:02d}</span>{p["name"]}</a></li>' for p in points)}</ol>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{M['goals_h']}</h2><p>{M['goals_p']}</p></div>
  <div class="goals">{cards}</div>
  <p class="goal-note">{M['note']}</p>
</div></section>
<section class="block"><div class="wrap why">
  <p class="mono">{M['why_k']}</p>
  <div><h2>{M['why_h']}</h2>{why}</div>
</div></section>""", extra=libs + f'\n<script src="{pre}mission.js?v={VERSION}"></script>')

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
    info = "".join(f'<li><span class="mono">{k}</span>{f"<a href=\"mailto:{EMAIL}\">{EMAIL}</a>" if v is None else f"<span>{v}</span>"}</li>' for k, v in C["info"])
    steps = "".join(f'<li><span class="n">{i}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(C["next"], 1))
    out["contact"] = page("contact", C["title"], C["desc"], head_block(L["nav"]["contact"], C["h1"], C["sub"]) + f"""
<section class="block contact"><div class="wrap contact-grid">
  <aside class="contact-side">
    <ul class="contact-info">{info}</ul>
    <p class="mono" style="margin:48px 0 18px">{C['next_k']}</p>
    <ol class="next-steps">{steps}</ol>
  </aside>
  <div class="form-card">
    <h2>{C['form_h']}</h2>
    <form class="form" id="contact-form" novalidate data-endpoint="https://formsubmit.co/ajax/{EMAIL}" data-subject="{C['subject']}"
      data-sending="{F['sending']}" data-err="{F['err']}" data-email="{EMAIL}">
      <label class="field"><span>{F['name']} *</span><input name="nome" required autocomplete="name"></label>
      <label class="field"><span>{F['email']} *</span><input name="email" type="email" required autocomplete="email"></label>
      <label class="field"><span>{F['company']}</span><input name="azienda" autocomplete="organization"></label>
      <label class="field"><span>{F['want']}</span><select name="servizio">{opts}</select></label>
      <label class="field full"><span>{F['msg']} *</span><textarea name="messaggio" required rows="5" placeholder="{F['ph']}"></textarea></label>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label class="check full"><input type="checkbox" name="privacy" required><span>{F['privacy']} *</span></label>
      <div class="send full"><p>* {F['req']}</p><button class="btn" type="submit">{F['send']} {arrow}</button></div>
      <p class="form-msg full" role="status" aria-live="polite"></p>
    </form>
    <div class="form-ok" hidden><span class="tick" aria-hidden="true">✓</span><h3>{F['ok_h']}</h3><p>{F['ok_p']}</p></div>
  </div>
</div></section>""")

    base = ROOT / variant if variant else ROOT
    folder = base if lang == "it" else base / "en"
    folder.mkdir(parents=True, exist_ok=True)
    for key, html in out.items():
        (folder / S[key]).write_text(html, encoding="utf-8")
        print("ok", variant or "main", lang, S[key])


if __name__ == "__main__":
    # toglie le pagine delle versioni precedenti (prezzi e lavori)
    for old in ["lavori.html", "prezzi.html", "studio.html", "en/work.html", "en/pricing.html", "en/studio.html"]:
        (ROOT / old).unlink(missing_ok=True)
        (ROOT / "alt" / old).unlink(missing_ok=True)
    for lang in T:
        build(lang)
    # versione B: stesso contenuto, stile editoriale (styles.css + alt-overrides.css)
    alt_css = (ROOT / "styles.css").read_text(encoding="utf-8") + "\n" + (ROOT / "alt-overrides.css").read_text(encoding="utf-8")
    (ROOT / "alt.css").write_text(alt_css, encoding="utf-8")
    for lang in T:
        build(lang, "alt")
