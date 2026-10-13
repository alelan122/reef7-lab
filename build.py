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
    "title": "Mission · Reef 7 Lab", "desc": "Ogni progetto di Reef 7 Lab sostiene chi protegge la flora e la fauna marina.",
    "h1": "Ogni progetto <em>protegge il mare</em>.",
    "sub": "Il nostro nome viene dal reef, e il reef è in pericolo: dagli anni '50 la copertura di corallo vivo nel mondo si è dimezzata. Per questo ogni progetto che realizziamo sostiene chi lavora ogni giorno per proteggere la flora e la fauna marina.",
    "stats": [],
    "how_h": "Come funziona", "how": [("Ogni progetto conta", "Ogni sito, app o sistema che consegniamo contribuisce a proteggere il mare, dal primo giorno."),
                                      ("Un reef alla volta", "Concentriamo l'impegno su un reef per volta. Raggiunto l'obiettivo, passiamo al successivo."),
                                      ("Sempre trasparenti", "Aggiorniamo questa pagina ogni volta che un obiettivo viene raggiunto.")],
    "map_h": "Il 7 del <em>nostro nome</em>", "map_p": "Sette barriere coralline tra le più preziose del pianeta, dal Mar Rosso alla Polinesia. Sono loro il 7 di Reef 7.",
    "goals_h": "Prossimi obiettivi", "goals_p": "Sette reef, uno dopo l'altro. Ogni progetto ci avvicina al prossimo.",
    "places": [("Koh Tao", "Thailandia", "Vivai e restauro dei coralli nel Golfo di Thailandia."),
               ("Mar Rosso", "Egitto", "Boe d'ormeggio che proteggono le barriere dalle ancore."),
               ("Raja Ampat", "Indonesia", "Aree marine protette e pattugliamento contro la pesca illegale."),
               ("Bali", "Indonesia", "Conservazione e formazione nel cuore del Triangolo dei Coralli."),
               ("Maldive", "Oceano Indiano", "Trapianto di coralli su strutture che ne favoriscono la ricrescita."),
               ("Moorea", "Polinesia francese", "Coltivazione di coralli più resistenti all'aumento delle temperature."),
               ("Grande Barriera Corallina", "Australia", "Ricerca e ripristino del reef più grande del mondo.")],
    "raised_of": "{r} raccolti di {t}", "active": "In corso", "next": "Prossimo", "done": "Raggiunto",
    "partner": "Organizzazione", "visit": "Sito",
    "note": "Le organizzazioni indicate sono quelle a cui intendiamo destinare i contributi; non rappresentano una partnership ufficiale.",
    "why_k": "La nostra storia", "why_h": "Per noi il mare <em>non è uno slogan</em>.",
    "why_p": ["Prima di fondare Reef 7 Lab, Alessandro è stato per diversi anni membro attivo di 2hands Ancona, il gruppo di volontari che ripulisce spiagge e coste dai rifiuti.",
              "Oggi quell'impegno continua nel lavoro: ogni progetto che realizziamo aiuta a proteggere il mare da cui prendiamo il nome."],
    "home_k": "Mission", "home_h": "Ogni progetto <em>protegge il mare</em>.", "home_p": "Il 7 nel nostro nome sono sette barriere coralline. Ogni progetto che realizziamo aiuta a proteggerle, una alla volta. Ora stiamo sostenendo:",
    "home_a": "Scopri la missione",
},
"en": {
    "title": "Mission · Reef 7 Lab", "desc": "Every Reef 7 Lab project supports the people protecting marine flora and fauna.",
    "h1": "Every project <em>protects the sea</em>.",
    "sub": "Our name comes from the reef, and reefs are in danger: since the 1950s, the world's living coral cover has halved. That's why every project we deliver supports the people working every day to protect marine flora and fauna.",
    "stats": [],
    "how_h": "How it works", "how": [("Every project counts", "Every website, app or system we deliver helps protect the sea, from day one."),
                                     ("One reef at a time", "We focus our support on one reef at a time. Once the goal is reached, we move to the next."),
                                     ("Always transparent", "We update this page every time a goal is reached.")],
    "map_h": "The 7 in <em>our name</em>", "map_p": "Seven of the most precious coral reefs on the planet, from the Red Sea to Polynesia. They are the 7 in Reef 7.",
    "goals_h": "Next goals", "goals_p": "Seven reefs, one after another. Every project brings us closer to the next.",
    "places": [("Koh Tao", "Thailand", "Coral nurseries and reef restoration in the Gulf of Thailand."),
               ("Red Sea", "Egypt", "Mooring buoys that protect reefs from anchor damage."),
               ("Raja Ampat", "Indonesia", "Marine protected areas and patrols against illegal fishing."),
               ("Bali", "Indonesia", "Conservation and training at the heart of the Coral Triangle."),
               ("Maldives", "Indian Ocean", "Coral transplants onto frames that help reefs regrow."),
               ("Moorea", "French Polynesia", "Growing corals that can withstand warmer seas."),
               ("Great Barrier Reef", "Australia", "Research and restoration of the world's largest reef.")],
    "raised_of": "{r} raised of {t}", "active": "In progress", "next": "Next", "done": "Reached",
    "partner": "Organisation", "visit": "Website",
    "note": "The organisations listed are those we intend to direct our contributions to; this does not represent an official partnership.",
    "why_k": "Our story", "why_h": "For us, the sea <em>isn't a slogan</em>.",
    "why_p": ["Before founding Reef 7 Lab, Alessandro spent several years as an active member of 2hands Ancona, the volunteer group that cleans beaches and coastlines of litter.",
              "Today that commitment carries on through our work: every project we deliver helps protect the sea we're named after."],
    "home_k": "Mission", "home_h": "Every project <em>protects the sea</em>.", "home_p": "The 7 in our name is seven coral reefs. Every project we deliver helps protect them, one at a time. Right now we're supporting:",
    "home_a": "Discover the mission",
},
}

# ---------------- Lavori: progetti reali, senza dati privati ----------------
# frame: "browser" (sito navigabile dentro il portfolio), "phone" (app navigabile), "scroll" (schermata da scorrere), "mock" (grafica senza dati)
WORK = [
    {"key": "tenka", "frame": "gallery", "url": None, "src": ["assets/work/tenka-dashboard-v2.jpg", "assets/work/tenka-tracker-v2.jpg", "assets/work/tenka-login.jpg"], "thumb": "assets/work/thumb-tenka-v2.jpg"},
    {"key": "fullpeak", "frame": "scroll", "url": "https://fullpeak.store/products/full-peak-magnesium-complex", "src": "assets/work/fullpeak-pdp.jpg", "thumb": "assets/work/thumb-fullpeak.jpg"},
    {"key": "dailypeak", "frame": "phone", "url": "work/my-daily-peak/index.html", "src": "work/my-daily-peak/index.html", "thumb": "assets/work/thumb-dailypeak.jpg"},
    {"key": "maisenzagioie", "frame": "browser", "url": "work/maisenzagioie/index.html", "src": "work/maisenzagioie/index.html", "thumb": "assets/work/thumb-maisenzagioie.jpg"},
]
WT = {
"it": {
    "title": "Projects · Reef 7 Lab", "desc": "Una selezione di progetti di Reef 7 Lab: applicazioni, siti e strumenti per aziende.",
    "h1": "Il nostro lavoro, <em>dal vivo</em>.",
    "sub": "Una selezione di sistemi che abbiamo progettato e sviluppato, dall'idea alla messa online. Dove possibile, puoi navigarli direttamente da questa pagina.",
    "labels": {"client": "Cliente", "type": "Tipo", "year": "Anno"},
    "open": {"browser": "Apri il sito", "phone": "Apri la demo", "scroll": "Visita il negozio"},
    "hint": {"browser": "Sito navigabile", "phone": "Demo interattiva", "scroll": "Anteprima della pagina", "gallery": "Schermate dell'app", "mock": "Applicazione privata"},
    "shots": ["Dashboard", "Tracker", "Accesso"],
    "projects": {
        "tenka": {"name": "Tenka OS", "client": "Tenka", "type": "Applicazione web su misura", "year": "2026",
                  "lead": "Una piattaforma interna che riunisce in un solo posto tutto ciò che serve per gestire un e-commerce.",
                  "text": "Vendite e spesa pubblicitaria arrivano da sole da Shopify e Meta, i margini di ogni offerta si calcolano in automatico e il team lavora su obiettivi e procedure condivise, in un'unica interfaccia.",
                  "points": ["Sincronizzazione automatica con Shopify e Meta Ads", "Margini e punto di pareggio per ogni offerta", "Piani di lavoro a 12 settimane per ogni persona del team", "Knowledge base interna e accesso con verifica in due passaggi"],
                  "note": "Schermate con dati dimostrativi: l'app è privata e i dati reali restano riservati. Demo dal vivo su richiesta."},
        "fullpeak": {"name": "Full Peak", "client": "Full Peak", "type": "Pagina prodotto Shopify", "year": "2026",
                     "lead": "La pagina prodotto di un brand di integratori, costruita per trasformare le visite in ordini.",
                     "text": "Ogni sezione risponde a una domanda di chi sta per acquistare: cosa contiene il prodotto, perché funziona, quanto conviene e cosa ne pensano gli altri clienti. Il tutto pensato per chi compra dal telefono.",
                     "points": ["Offerta e bundle chiari fin dal primo sguardo", "Benefici e ingredienti spiegati in modo semplice", "Recensioni e prova sociale in evidenza", "Esperienza ottimizzata per mobile"],
                     "note": "I negozi Shopify non possono essere incorporati in altri siti: scorri l'anteprima o apri la pagina dal pulsante."},
        "dailypeak": {"name": "My Daily Peak", "client": "Full Peak", "type": "Web app per i clienti, integrata in Shopify", "year": "2026",
                      "lead": "Un'app che accompagna il cliente dopo l'acquisto e lo aiuta a raggiungere il suo obiettivo.",
                      "text": "Chi acquista sceglie cosa vuole migliorare e riceve un piano giorno per giorno: un check-in di pochi secondi, una piccola abitudine e i progressi sempre visibili. L'app vive dentro il negozio, è riservata a chi ha acquistato e ricorda il riordino al momento giusto.",
                      "points": ["Piano personalizzato sull'obiettivo del cliente", "Check-in quotidiano in pochi secondi", "Progressi e traguardi settimana dopo settimana", "Integrata nel tema Shopify, senza app esterne"],
                      "note": "Demo con dati di prova: puoi provarla qui accanto."},
        "maisenzagioie": {"name": "Maisenzagioie", "client": "Marica Viciglione", "type": "Sito su misura per un brand artigianale", "year": "2026",
                          "lead": "Un sito su misura per un brand di gioielli in macramè fatti a mano.",
                          "text": "Il sito racconta l'artigianalità di ogni pezzo e permette di creare la propria collana scegliendo fili e pietre. Dietro le quinte, un pannello semplice consente alla titolare di aggiornare prodotti e prezzi in autonomia, senza dipendere da nessuno.",
                          "points": ["Configuratore per creare la propria collana", "Catalogo organizzato per collezioni", "Pannello di gestione semplice e privato", "Design su misura e caricamento rapido"],
                          "note": "Anteprima navigabile del sito."},
    },
    "home_h": "Projects", "home_p": "Una selezione di progetti recenti, da esplorare dal vivo.", "home_a": "Tutti i progetti",
    "partners_k": "Partner", "partners_h": "Partner, <em>non semplici clienti</em>.",
    "partners_p": "Lavoriamo al fianco di aziende che hanno scelto la tecnologia e l'intelligenza artificiale come leva di crescita. Con loro non ci limitiamo a consegnare un progetto: costruiamo insieme, giorno dopo giorno, i sistemi su cui si regge il loro business.",
    "partners_cta": ("Vuoi crescere con noi?", "Diventa partner"),
    "partners": [("Asia Baldoni Fitness", "Partner tecnologico", "Fitness femminile online",
                  "Al fianco del team nello sviluppo di strumenti interni, automazioni e soluzioni di intelligenza artificiale che supportano vendite e operations."),
                 ("Tartufoli Group", "Partner strategico", "Il gruppo di Asia Baldoni Fitness",
                  "Una collaborazione di lungo periodo per l'infrastruttura digitale e l'adozione dell'intelligenza artificiale nei brand del gruppo.")],
},
"en": {
    "title": "Projects · Reef 7 Lab", "desc": "A selection of Reef 7 Lab projects: applications, websites and tools for businesses.",
    "h1": "Our work, <em>live</em>.",
    "sub": "A selection of systems we've designed and built, from first idea to launch. Where possible, you can browse them right from this page.",
    "labels": {"client": "Client", "type": "Type", "year": "Year"},
    "open": {"browser": "Open the website", "phone": "Open the demo", "scroll": "Visit the store"},
    "hint": {"browser": "Live website", "phone": "Interactive demo", "scroll": "Page preview", "gallery": "App screenshots", "mock": "Private application"},
    "shots": ["Dashboard", "Tracker", "Sign-in"],
    "projects": {
        "tenka": {"name": "Tenka OS", "client": "Tenka", "type": "Custom web application", "year": "2026",
                  "lead": "An internal platform that brings everything needed to run an e-commerce business into one place.",
                  "text": "Sales and ad spend flow in automatically from Shopify and Meta, the margins of every offer are calculated on their own, and the team works from shared goals and procedures, in a single interface.",
                  "points": ["Automatic sync with Shopify and Meta Ads", "Margins and break-even point for every offer", "12-week work plans for every team member", "Internal knowledge base and two-step verification"],
                  "note": "Screenshots with sample data: the app is private and real data stays confidential. Live demo on request."},
        "fullpeak": {"name": "Full Peak", "client": "Full Peak", "type": "Shopify product page", "year": "2026",
                     "lead": "The product page of a supplement brand, built to turn visits into orders.",
                     "text": "Every section answers a question shoppers have right before buying: what's in the product, why it works, how good the deal is and what other customers think. All of it designed for people who shop on their phone.",
                     "points": ["Offers and bundles clear at a glance", "Benefits and ingredients explained simply", "Reviews and social proof up front", "Optimised for mobile"],
                     "note": "Shopify stores can't be embedded in other websites: scroll the preview or open the page with the button."},
        "dailypeak": {"name": "My Daily Peak", "client": "Full Peak", "type": "Customer web app, built into Shopify", "year": "2026",
                      "lead": "An app that stays with customers after they buy and helps them reach their goal.",
                      "text": "Customers choose what they want to improve and get a day-by-day plan: a check-in that takes seconds, one small habit and progress that's always visible. The app lives inside the store, is reserved for customers and reminds them to reorder at the right moment.",
                      "points": ["A plan tailored to each customer's goal", "Daily check-in in a few seconds", "Progress and milestones week after week", "Built into the Shopify theme, no external apps"],
                      "note": "Demo with sample data: try it right here."},
        "maisenzagioie": {"name": "Maisenzagioie", "client": "Marica Viciglione", "type": "Custom website for an artisan brand", "year": "2026",
                          "lead": "A custom website for a brand of handmade macramé jewellery.",
                          "text": "The site tells the story of the craftsmanship behind every piece and lets visitors design their own necklace by choosing threads and stones. Behind the scenes, a simple panel lets the owner update products and prices on her own, without depending on anyone.",
                          "points": ["Configurator to design your own necklace", "Catalogue organised by collection", "Simple, private management panel", "Custom design and fast loading"],
                          "note": "Browsable website preview."},
    },
    "home_h": "Projects", "home_p": "A selection of recent projects, ready to explore live.", "home_a": "All projects",
    "partners_k": "Partners", "partners_h": "Partners, <em>not just clients</em>.",
    "partners_p": "We work alongside companies that have chosen technology and artificial intelligence as a lever for growth. We don't deliver a project and disappear: together, day after day, we build the systems their business runs on.",
    "partners_cta": ("Want to grow with us?", "Become a partner"),
    "partners": [("Asia Baldoni Fitness", "Technology partner", "Online women's fitness",
                  "Working alongside the team to develop internal tools, automations and AI solutions that support sales and operations."),
                 ("Tartufoli Group", "Strategic partner", "The group behind Asia Baldoni Fitness",
                  "A long-term collaboration on digital infrastructure and the adoption of artificial intelligence across the group's brands.")],
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
    "it": {"home": "index.html", "work": "lavori.html", "services": "servizi.html", "solutions": "soluzioni.html", "mission": "missione.html", "studio": "lab.html", "contact": "contatti.html"},
    "en": {"home": "index.html", "work": "work.html", "services": "services.html", "solutions": "solutions.html", "mission": "mission.html", "studio": "lab.html", "contact": "contact.html"},
}
NAV = ["work", "services", "solutions", "mission", "studio"]

T = {
"it": {
    "nav": {"work": "Projects", "services": "Services", "solutions": "Solutions", "mission": "Mission", "studio": "Lab", "contact": "Contact"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot": "© 2026 Reef 7 Lab · Sviluppo software e intelligenza artificiale",
    "cta_k": "Nuovo progetto", "cta_h": "Costruiamo il tuo <em>reef</em>.",
    "services": [
        ("01", "Digitale", "Siti web e landing page", "Siti e pagine di vendita che trasformano le visite in contatti.",
         "Il sito è spesso il primo contatto con un cliente. Progettiamo siti e landing page che spiegano subito il valore, accompagnano verso il contatto e si aggiornano senza dover chiamare nessuno.",
         ["Struttura e testi pensati per convertire", "Design su misura, nessun template", "Landing page e funnel per le campagne", "Ottimizzazione per Google e per il telefono", "Ogni richiesta tracciata"]),
        ("02", "Digitale", "Applicazioni su misura", "Il software si adatta a come lavori. Non il contrario.",
         "Se il tuo team passa più tempo ad aggirare un gestionale che a usarlo, il problema non è il team. Progettiamo gestionali, portali clienti e strumenti interni attorno ai processi reali della tua azienda.",
         ["Analisi dei processi e prototipo cliccabile", "Applicazioni web e desktop", "Accessi e permessi per ruolo", "Integrazione con gli strumenti che usi già", "Nuove funzioni man mano che cresci"]),
        ("03", "Vendite", "CRM su misura", "Lead, trattative e provvigioni in un unico strumento, costruito sul tuo modo di vendere.",
         "Un CRM generico costringe il team commerciale ad adattarsi. Costruiamo CRM su misura: ogni lead arriva già assegnato, le trattative avanzano per fasi, pagamenti e provvigioni si calcolano da soli e la direzione vede risultati e classifica in tempo reale.",
         ["Pipeline e fasi definite sul tuo processo", "Assegnazione automatica dei lead", "Pagamenti e provvigioni calcolati in automatico", "Classifica e KPI del team, anche su uno schermo in ufficio", "Collegato a sito, prenotazioni ed email"]),
        ("04", "Vendite", "Prenotazioni e agenda commerciale", "Un sistema di prenotazione tuo, che assegna ogni appuntamento alla persona giusta.",
         "I potenziali clienti prenotano da soli una call. Il sistema distribuisce gli appuntamenti tra i commerciali, riporta ogni contatto al suo referente e invia i promemoria, così diminuiscono le assenze.",
         ["Pagina di prenotazione con il tuo brand", "Distribuzione automatica tra i commerciali", "Ogni contatto torna sempre al suo referente", "Promemoria automatici", "Appuntamenti registrati direttamente nel CRM"]),
        ("05", "Vendite", "Email marketing e automazioni", "Sequenze email che lavorano per te, con la consegna sotto controllo.",
         "Dal benvenuto al follow-up dopo una call, le email partono al momento giusto in base a ciò che fa ogni contatto. Curiamo anche la parte tecnica che decide se un'email arriva in casella o finisce nello spam.",
         ["Sequenze automatiche per ogni fase del cliente", "Segmentazione in base al comportamento", "Riscaldamento dei domini e gestione delle liste", "Statistiche di apertura e risposta", "Un'alternativa alle piattaforme a canone"]),
        ("06", "Intelligenza artificiale", "Automazioni con l'AI", "Le ore spese in lavoro ripetitivo tornano al tuo team.",
         "Rispondere alle stesse email, copiare dati, compilare report: è lavoro che non fa crescere nessuno. Lo affidiamo all'intelligenza artificiale, con un controllo umano dove serve, e misuriamo quanto tempo ti restituisce.",
         ["Analisi delle attività che costano più tempo", "Email, documenti e report automatici", "Contatti qualificati e smistati da soli", "Controllo umano nei passaggi delicati", "Tempo risparmiato misurato"]),
        ("07", "Intelligenza artificiale", "Company brain", "Tutto quello che sa la tua azienda, a una domanda di distanza.",
         "Procedure, documenti, risposte già date ai clienti: il sapere della tua azienda è sparso tra cartelle, chat e persone. Lo raccogliamo in un assistente che risponde al team in pochi secondi e indica sempre da dove viene l'informazione.",
         ["Raccolta e organizzazione dei documenti", "Risposte con la fonte, sempre verificabili", "Ognuno vede solo ciò che gli compete", "Contenuti aggiornati nel tempo", "Dati riservati e protetti"]),
        ("08", "Gestione", "Dashboard e controllo di gestione", "Vendite, cassa e margini in un'unica vista, sempre aggiornata.",
         "Se per capire come sta andando l'azienda servono tre persone e un Excel, decidi sempre in ritardo. Colleghiamo le tue fonti in dashboard per la direzione: indicatori commerciali, flussi di cassa, marginalità e bilancio, aggiornati da soli.",
         ["Indicatori commerciali e di marketing", "Flussi di cassa e marginalità", "Viste dedicate per direzione e team", "Aggiornamento automatico dalle tue fonti", "Accessi protetti per ruolo"]),
        ("09", "Gestione", "Hub aziendale e integrazioni", "Tutti gli strumenti dell'azienda collegati e raggiungibili da un unico punto.",
         "Un portale interno da cui ogni persona accede agli strumenti che le servono, con un unico database alla base. Colleghiamo i software tra loro tramite API e webhook, così i dati si muovono da soli.",
         ["Portale interno con accessi per ruolo", "Un unico database per tutte le applicazioni", "Integrazioni via API e webhook", "Organigramma e procedure sempre a portata di mano", "Sicurezza e backup inclusi"]),
        ("10", "Gestione", "Dagli abbonamenti a strumenti tuoi", "Sostituiamo i software a canone con strumenti tuoi, integrati tra loro.",
         "CRM, email, prenotazioni, automazioni: molte aziende pagano ogni mese più abbonamenti che fanno cose simili e non si parlano. Analizziamo i costi e sostituiamo quelli che conviene con strumenti tuoi, più semplici e collegati.",
         ["Analisi dei software in uso e dei costi", "Piano di migrazione senza interruzioni", "Dati trasferiti e verificati", "Strumenti integrati tra loro", "Meno costi ricorrenti nel tempo"]),
    ],
    "sectors": [
        {"t": "Team commerciali", "d": "Più tempo in chiamata, meno tempo su Excel.",
         "pain": "I commerciali aggiornano fogli di calcolo invece di vendere, i contatti si perdono tra un'agenda e l'altra e le provvigioni si calcolano a mano a fine mese.",
         "build": ["Un CRM costruito sul tuo processo di vendita", "Prenotazioni distribuite automaticamente tra i commerciali", "Sequenze email che seguono ogni contatto dopo la call", "Provvigioni e classifica calcolate in automatico"],
         "out": "Un team che passa più tempo con i clienti e una direzione che vede i risultati in tempo reale.", "svc": ["03", "04", "05", "08"]},
        {"t": "E-commerce", "d": "Più vendite, senza più lavoro manuale.",
         "pain": "Ordini, campagne e assistenza vivono in strumenti diversi. Scopri a fine mese cosa ha funzionato, quando è troppo tardi per correggere.",
         "build": ["Pagine prodotto pensate per convertire", "Dashboard con vendite, spesa pubblicitaria e margine reale", "Assistenza ai clienti gestita dall'intelligenza artificiale", "App per i clienti dopo l'acquisto, integrata nel negozio"],
         "out": "Sai ogni giorno quanto guadagni davvero, e il team si concentra sulla crescita invece di rincorrere gli ordini.", "svc": ["01", "08", "06", "02"]},
        {"t": "Studi professionali", "d": "Meno burocrazia, più tempo per i clienti.",
         "pain": "Documenti da cercare, scadenze da ricordare e le stesse domande dei clienti ogni settimana: ore preziose che non puoi fatturare.",
         "build": ["Un portale riservato per i clienti", "Documenti archiviati e classificati in automatico", "Un assistente che conosce le procedure dello studio", "Promemoria automatici per scadenze e appuntamenti"],
         "out": "Più ore dedicate alla consulenza, meno errori e clienti che si sentono davvero seguiti.", "svc": ["02", "07", "06", "04"]},
        {"t": "Formazione e coaching", "d": "Un percorso digitale all'altezza di ciò che insegni.",
         "pain": "Corsi su una piattaforma, community su un'altra, vendite gestite a mano: gli studenti si perdono tra un passaggio e l'altro.",
         "build": ["Landing page e funnel per le iscrizioni", "Call di vendita prenotate e assegnate in automatico", "Email che accompagnano ogni studente dall'iscrizione al risultato", "Un assistente che risponde alle domande degli studenti"],
         "out": "Più iscrizioni, studenti più coinvolti e un'attività che cresce senza moltiplicare il lavoro.", "svc": ["01", "04", "05", "07"]},
        {"t": "Agenzie e servizi B2B", "d": "Clienti seguiti meglio, con meno passaggi a mano.",
         "pain": "Richieste via email, stato dei lavori in un foglio condiviso, report preparati a mano ogni mese per ogni cliente.",
         "build": ["Un portale clienti con stato dei lavori e documenti", "Report per i clienti generati in automatico", "Richieste smistate al referente giusto", "Una knowledge base interna per il team"],
         "out": "Clienti informati senza doverlo chiedere, e un team che lavora sui progetti invece che sulle email.", "svc": ["02", "08", "06", "07"]},
        {"t": "Aziende in crescita", "d": "Cresci senza perdere il controllo.",
         "pain": "Più clienti vogliono dire più fogli di calcolo, più abbonamenti e più errori. Gli strumenti che bastavano due anni fa oggi rallentano tutto.",
         "build": ["Un hub interno con tutti gli strumenti e un unico database", "Dashboard per la direzione su vendite, cassa e margini", "Software in abbonamento sostituiti da strumenti tuoi", "Gestionali costruiti sui tuoi processi"],
         "out": "Un'unica fonte di verità per tutta l'azienda, decisioni prese su dati certi e meno costi ricorrenti.", "svc": ["09", "08", "10", "02"]},
    ],
    "home": {
        "title": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "desc": "Reef 7 Lab sviluppa siti, applicazioni, intelligenza artificiale e dashboard su misura, collegati in un unico sistema.",
        "kicker": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "h1": "Il tuo business, <em>connesso</em>.",
        "sub": "Siti, applicazioni e intelligenza artificiale progettati per lavorare insieme. Meno lavoro manuale, decisioni più rapide, una crescita che si accumula nel tempo.",
        "b1": "Parliamo del tuo progetto", "b2": "Scopri i servizi",
        "eco_k": "Integrazione dei sistemi",
        "eco_h": "Un unico sistema per <em>tutta l'azienda</em>.",
        "eco_p": "Colleghiamo gli strumenti che usi già e automatizziamo i passaggi tra l'uno e l'altro. I dati entrano una volta sola e arrivano dove servono, già pronti per essere usati. Ecco tre esempi di ciò che costruiamo:",
        "values": ["Nessun dato inserito due volte", "Numeri affidabili, aggiornati da soli", "Il team libero dal lavoro ripetitivo"],
        "flows": [
            {"tab": "Vendite e marketing", "in": ["Shopify", "Meta Ads"], "core": "Sincronizzazione automatica", "out": "Margine di oggi", "kind": "dash", "manual": ["Esporti gli ordini da Shopify", "Copi la spesa da Meta Ads", "Incolli tutto in Excel", "Calcoli il margine a mano"], "manual_end": "Numeri pronti dopo giorni",
             "rows": ["Vendite", "Spesa pubblicitaria", "Margine reale"], "live": "Aggiornato in automatico",
             "value": "Sai ogni giorno quanto guadagni davvero, senza aprire un foglio di calcolo."},
            {"tab": "Clienti", "in": ["WhatsApp", "Email"], "core": "Risposta e qualifica con l'AI", "out": "Nuovo contatto nel CRM", "kind": "crm", "manual": ["Leggi i messaggi su più canali", "Rispondi uno per uno", "Copi il contatto nel CRM", "Ti segni quando richiamare"], "manual_end": "Alcuni contatti si perdono",
             "rows": ["Richiesta ricevuta", "Risposta inviata in automatico", "Follow-up programmato"], "live": "Assegnato al commerciale",
             "value": "Ogni richiesta riceve una risposta immediata e nessun contatto si perde per strada."},
            {"tab": "Amministrazione", "in": ["Ordini", "Pagamenti"], "core": "Documenti generati in automatico", "out": "Fattura e report pronti", "kind": "doc", "manual": ["Controlli ordini e pagamenti", "Compili la fattura", "La registri in contabilità", "Prepari il report del mese"], "manual_end": "Ore di lavoro ogni mese",
             "rows": ["Fattura", "Registrazione contabile", "Report mensile"], "live": "Pronto da inviare",
             "value": "Fatture e report si preparano da soli, senza errori di trascrizione."},
        ],
        "flow_lbl": ("Dati in entrata", "Il sistema", "Il risultato"),
        "rows_lbl": ("Oggi, a mano", "Con il sistema, in automatico", "passaggi a mano"),
        "svc_h": "Services", "svc_p": "Dal sito al CRM, dall'intelligenza artificiale al controllo di gestione: competenze diverse che lavorano insieme.", "svc_all": "Tutti i servizi",
        "sol_h": "Solutions", "sol_p": "Per ogni settore combiniamo i servizi giusti in un unico sistema. Ecco alcuni esempi.", "sol_all": "Tutte le soluzioni",
        "reef_h": "Progettati come <em>un reef</em>", "reef_p": "Il reef è tra gli ecosistemi più efficienti della Terra. I suoi cinque principi guidano ogni progetto.",
        "reef_words": ["Diversità", "Simbiosi", "Connessione", "Crescita stratificata", "Resilienza"], "reef_a": "La nostra filosofia",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Siti web, applicazioni su misura, intelligenza artificiale, company brain e dashboard.",
        "h1": "Dieci competenze, <em>un solo</em> sistema.",
        "sub": "Dal sito che porta clienti al gestionale che fa girare l'azienda: le combiniamo in base ai tuoi obiettivi, mai partendo da un pacchetto preconfezionato.",
    },
    "solutions": {
        "title": "Solutions · Reef 7 Lab", "desc": "Soluzioni software per e-commerce, studi professionali, formazione e aziende in crescita.",
        "h1": "Soluzioni costruite <em>sul tuo settore</em>.",
        "sub": "Ogni settore ha i suoi colli di bottiglia. Per ognuno combiniamo i servizi giusti in un sistema unico: ecco i casi che affrontiamo più spesso.",
        "lbl": ("La sfida", "Cosa costruiamo", "Il risultato", "Servizi coinvolti"),
    },
    "studio": {
        "title": "Lab · Reef 7 Lab", "desc": "La filosofia del reef: come Reef 7 Lab progetta software che cresce connesso.",
        "h1": "La filosofia <em>del reef</em>.",
        "sub": "Una barriera corallina copre meno dell'1% dei fondali, eppure ospita un quarto di tutta la vita marina. Il suo segreto non è la grandezza: è l'architettura. È il modello che seguiamo in ogni sistema che costruiamo.",
        "principles": [
            ("01", "Diversità", "In un reef convivono migliaia di specie, ognuna con un ruolo preciso. Nessuna fa tutto: ognuna fa una cosa in modo eccellente. Nel software è lo stesso. Un sito, un'automazione, un assistente, una dashboard: strumenti diversi, scelti per ciò che sanno fare meglio. Mai tecnologia fine a se stessa."),
            ("02", "Simbiosi", "Il corallo vive grazie alle alghe che ospita, e le alghe grazie al corallo. Insieme costruiscono ciò che da soli non potrebbero. Così lavorano persone e tecnologia nei nostri sistemi: l'intelligenza artificiale si prende il lavoro ripetitivo, le persone ciò che richiede giudizio, creatività e relazioni."),
            ("03", "Connessione", "In un reef nulla vive isolato. Correnti, nutrienti e specie si muovono in un'unica rete, e ogni parte rafforza le altre. I nostri sistemi parlano tra loro: un dato entra una volta sola e arriva ovunque serva. Niente silos, niente copia e incolla, niente versioni diverse della stessa verità."),
            ("04", "Crescita stratificata", "Il corallo cresce pochi millimetri l'anno, strato su strato, e costruisce strutture che durano secoli. Progettiamo con la stessa pazienza: prima fondamenta solide, poi funzioni che si aggiungono nel tempo. Il risultato è un software che accumula valore invece di invecchiare."),
            ("05", "Resilienza", "Un reef sano resiste alle tempeste e si adatta quando le correnti cambiano. Il software deve fare lo stesso. Costruiamo architetture flessibili, pronte a evolvere con la tua azienda, con il mercato e con le tecnologie che devono ancora arrivare."),
        ],
        "seven_k": "Perché 7", "seven_h": "Sette reef, <em>un nome</em>.", "seven_a": "Scopri i sette reef",
        "seven_p": "Il 7 sono sette barriere coralline, dal Mar Rosso alla Polinesia, che ci siamo impegnati a proteggere. Ogni progetto che realizziamo ci avvicina a una di loro: è il numero che ci ricorda per chi lavoriamo, oltre che per i nostri clienti.",
        "who_big": "Dietro Reef 7 Lab c'è <em>Alessandro</em>.",
        "who": ["Negli ultimi anni ha progettato software, automazioni e funnel di vendita per aziende in crescita, vedendo da vicino quanto valore si perde tra strumenti scollegati e processi manuali.",
                "Ha fondato Reef 7 Lab per offrire alle aziende ciò che di solito è riservato ai grandi gruppi: sistemi su misura, intelligenza artificiale applicata e un unico interlocutore che conosce ogni riga del progetto.",
                "Il legame con il mare è personale: per diversi anni è stato membro attivo di 2hands Ancona, il gruppo di volontari che ripulisce spiagge e coste dai rifiuti."],
        "sign": ("Alessandro", "Fondatore, Reef 7 Lab"),
        "photo_alt": "Alessandro, fondatore di Reef 7 Lab",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Contatta Reef 7 Lab per un nuovo progetto.",
        "h1": "Raccontaci dove vuoi <em>arrivare</em>.",
        "sub": "Bastano poche righe su obiettivi e ostacoli. Nella prima conversazione, 30 minuti senza impegno, capiamo il contesto e ti diciamo con franchezza se e come possiamo aiutarti.",
        "info": [("Email", None), ("Tempi di risposta", "Entro un giorno lavorativo"), ("Dove", "Italia · lavoriamo anche da remoto"), ("Lingue", "Italiano, English")],
        "next_k": "Cosa succede dopo",
        "next": [("Ci scrivi", "Raccontaci obiettivi, tempi e contesto. Poche righe sono più che sufficienti."),
                 ("Ti rispondiamo", "Entro un giorno lavorativo, con qualche prima domanda e una proposta di data."),
                 ("Prima consulenza", "30 minuti, gratuita e senza impegno, per capire insieme se e come possiamo aiutarti.")],
        "form_h": "Parliamo del tuo progetto",
        "f": {"name": "Nome e cognome", "email": "Email di lavoro", "company": "Azienda", "want": "Di cosa hai bisogno",
              "msg": "Raccontaci il progetto", "ph": "Obiettivi, tempi e cosa vorresti migliorare",
              "opts": ["Sito web o landing page", "Applicazione su misura", "CRM e vendite", "Prenotazioni ed email marketing", "Intelligenza artificiale", "Company brain", "Dashboard e controllo di gestione", "Integrazioni e software di proprietà", "Non lo so ancora"],
              "privacy": "Acconsento al trattamento dei miei dati per essere ricontattato in merito alla richiesta.",
              "req": "Campi obbligatori", "send": "Invia la richiesta", "sending": "Invio in corso…",
              "ok_h": "Richiesta inviata.", "ok_p": "Grazie! Ti risponderemo entro un giorno lavorativo all'indirizzo che ci hai indicato.",
              "err": "Invio non riuscito. Riprova o scrivici direttamente a"},
        "subject": "Nuova richiesta dal sito",
    },
},
"en": {
    "nav": {"work": "Projects", "services": "Services", "solutions": "Solutions", "mission": "Mission", "studio": "Lab", "contact": "Contact"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot": "© 2026 Reef 7 Lab · Software and AI development",
    "cta_k": "New project", "cta_h": "Let's build your <em>reef</em>.",
    "services": [
        ("01", "Digital", "Websites and landing pages", "Websites and sales pages that turn visits into enquiries.",
         "Your website is often the first contact a client has with you. We design websites and landing pages that explain the value straight away, guide people towards getting in touch, and can be updated without calling anyone.",
         ["Structure and copy built to convert", "Custom design, no templates", "Landing pages and funnels for campaigns", "Optimised for Google and for mobile", "Every enquiry tracked"]),
        ("02", "Digital", "Custom applications", "Software that fits the way you work. Not the other way round.",
         "If your team spends more time working around a system than using it, the problem isn't the team. We design management tools, client portals and internal software around the way your company really works.",
         ["Process analysis and clickable prototype", "Web and desktop applications", "Role-based access and permissions", "Integration with the tools you already use", "New features as you grow"]),
        ("03", "Sales", "Custom CRM", "Leads, deals and commissions in one tool, built around the way you sell.",
         "A generic CRM forces your sales team to adapt. We build custom CRMs: every lead arrives already assigned, deals move through clear stages, payments and commissions calculate themselves, and leadership sees results and rankings in real time.",
         ["Pipeline and stages designed around your process", "Automatic lead assignment", "Payments and commissions calculated automatically", "Team leaderboard and KPIs, even on a screen in the office", "Connected to your website, bookings and email"]),
        ("04", "Sales", "Bookings and sales calendar", "Your own booking system, assigning every appointment to the right person.",
         "Prospects book a call on their own. The system distributes appointments across your sales team, sends every contact back to their own rep and sends reminders, so fewer people miss their call.",
         ["Booking page with your branding", "Automatic distribution across the sales team", "Every contact always returns to their rep", "Automatic reminders", "Appointments logged straight into the CRM"]),
        ("05", "Sales", "Email marketing and automation", "Email sequences that work for you, with deliverability under control.",
         "From the welcome email to the follow-up after a call, emails go out at the right moment based on what each contact does. We also handle the technical side that decides whether an email lands in the inbox or in spam.",
         ["Automated sequences for every customer stage", "Segmentation based on behaviour", "Domain warm-up and list management", "Open and reply statistics", "An alternative to subscription platforms"]),
        ("06", "AI", "AI automation", "The hours lost to repetitive work go back to your team.",
         "Answering the same emails, copying data, filling in reports: work that helps no one grow. We hand it to AI, with human checks where they matter, and measure exactly how much time it gives back.",
         ["Finding the tasks that cost the most time", "Automated email, documents and reports", "Leads qualified and routed automatically", "Human review at the critical steps", "Time saved, measured"]),
        ("07", "AI", "Company brain", "Everything your company knows, one question away.",
         "Procedures, documents, answers already given to clients: your company's knowledge is scattered across folders, chats and people. We bring it together in an assistant that answers your team in seconds and always shows where the information comes from.",
         ["Collecting and organising documents", "Answers with sources, always verifiable", "Everyone sees only what they should", "Content that stays up to date", "Private, protected data"]),
        ("08", "Operations", "Dashboards and financial control", "Sales, cash and margins in one view, always up to date.",
         "If understanding how the company is doing takes three people and a spreadsheet, you'll always decide too late. We connect your sources into dashboards for leadership: sales metrics, cash flow, margins and financial statements, updated on their own.",
         ["Sales and marketing metrics", "Cash flow and margins", "Dedicated views for leadership and teams", "Automatic updates from your sources", "Role-based secure access"]),
        ("09", "Operations", "Company hub and integrations", "All your company's tools connected and reachable from one place.",
         "An internal portal where everyone accesses the tools they need, built on a single database. We connect your software through APIs and webhooks, so data moves on its own.",
         ["Internal portal with role-based access", "One database for every application", "Integrations through APIs and webhooks", "Org chart and procedures always at hand", "Security and backups included"]),
        ("10", "Operations", "From subscriptions to your own tools", "We replace subscription software with tools you own, all connected.",
         "CRM, email, bookings, automation: many companies pay for several monthly subscriptions that do similar things and don't talk to each other. We analyse the costs and replace the ones worth replacing with your own tools, simpler and connected.",
         ["Review of the software you use and what it costs", "Migration plan with no downtime", "Data transferred and verified", "Tools that work together", "Lower recurring costs over time"]),
    ],
    "sectors": [
        {"t": "Sales teams", "d": "More time on calls, less time in spreadsheets.",
         "pain": "Reps update spreadsheets instead of selling, contacts get lost between calendars and commissions are calculated by hand at the end of the month.",
         "build": ["A CRM built around your sales process", "Bookings distributed automatically across the team", "Email sequences that follow up every contact after the call", "Commissions and leaderboard calculated automatically"],
         "out": "A team that spends more time with clients, and leadership that sees results in real time.", "svc": ["03", "04", "05", "08"]},
        {"t": "E-commerce", "d": "More sales, without more manual work.",
         "pain": "Orders, campaigns and support live in different tools. You find out what worked at the end of the month, when it's too late to fix.",
         "build": ["Product pages built to convert", "A dashboard with sales, ad spend and real margin", "Customer support handled by AI", "A post-purchase customer app built into the store"],
         "out": "You know every day how much you're really making, and your team focuses on growth instead of chasing orders.", "svc": ["01", "08", "06", "02"]},
        {"t": "Professional firms", "d": "Less paperwork, more time for clients.",
         "pain": "Documents to find, deadlines to remember and the same client questions every week: valuable hours you can't bill.",
         "build": ["A private client portal", "Documents filed and classified automatically", "An assistant that knows the firm's procedures", "Automatic reminders for deadlines and appointments"],
         "out": "More hours for advisory work, fewer mistakes and clients who feel genuinely looked after.", "svc": ["02", "07", "06", "04"]},
        {"t": "Education and coaching", "d": "A digital journey as good as what you teach.",
         "pain": "Courses on one platform, community on another, sales handled by hand: students get lost between one step and the next.",
         "build": ["Landing pages and funnels for sign-ups", "Sales calls booked and assigned automatically", "Emails that guide every student from sign-up to results", "An assistant that answers students' questions"],
         "out": "More sign-ups, more engaged students and a business that grows without multiplying the workload.", "svc": ["01", "04", "05", "07"]},
        {"t": "Agencies and B2B services", "d": "Clients looked after better, with fewer manual steps.",
         "pain": "Requests by email, project status in a shared spreadsheet, reports put together by hand every month for every client.",
         "build": ["A client portal with project status and documents", "Client reports generated automatically", "Requests routed to the right person", "An internal knowledge base for the team"],
         "out": "Clients stay informed without having to ask, and the team works on projects instead of email.", "svc": ["02", "08", "06", "07"]},
        {"t": "Growing companies", "d": "Grow without losing control.",
         "pain": "More clients mean more spreadsheets, more subscriptions and more mistakes. The tools that were enough two years ago now slow everything down.",
         "build": ["An internal hub with every tool on a single database", "Leadership dashboards for sales, cash and margins", "Subscription software replaced by tools you own", "Management systems built around your processes"],
         "out": "A single source of truth for the whole company, decisions made on solid data and lower recurring costs.", "svc": ["09", "08", "10", "02"]},
    ],
    "home": {
        "title": "Reef 7 Lab · Software and AI development",
        "desc": "Reef 7 Lab builds custom websites, applications, AI and dashboards, connected into a single system.",
        "kicker": "Reef 7 Lab · Software and AI development",
        "h1": "Your business, <em>connected</em>.",
        "sub": "Websites, applications and AI designed to work together. Less manual work, faster decisions and growth that compounds over time.",
        "b1": "Let's talk about your project", "b2": "Explore services",
        "eco_k": "Systems integration",
        "eco_h": "One system for <em>the whole company</em>.",
        "eco_p": "We connect the tools you already use and automate the steps between them. Data is entered once and reaches wherever it's needed, ready to use. Here are three examples of what we build:",
        "values": ["No data entered twice", "Reliable numbers that update themselves", "A team freed from repetitive work"],
        "flows": [
            {"tab": "Sales and marketing", "in": ["Shopify", "Meta Ads"], "core": "Automatic sync", "out": "Today's margin", "kind": "dash", "manual": ["Export orders from Shopify", "Copy ad spend from Meta Ads", "Paste it all into a spreadsheet", "Work out the margin by hand"], "manual_end": "Numbers ready days later",
             "rows": ["Sales", "Ad spend", "Real margin"], "live": "Updated automatically",
             "value": "You know every day how much you're really making, without opening a spreadsheet."},
            {"tab": "Customers", "in": ["WhatsApp", "Email"], "core": "AI replies and qualifies", "out": "New contact in the CRM", "kind": "crm", "manual": ["Read messages across channels", "Reply to each one", "Copy the contact into the CRM", "Note when to call back"], "manual_end": "Some leads get lost",
             "rows": ["Request received", "Reply sent automatically", "Follow-up scheduled"], "live": "Assigned to sales",
             "value": "Every request gets an immediate reply and no lead slips through the cracks."},
            {"tab": "Admin", "in": ["Orders", "Payments"], "core": "Documents generated automatically", "out": "Invoice and report ready", "kind": "doc", "manual": ["Check orders and payments", "Fill in the invoice", "Record it in the accounts", "Prepare the monthly report"], "manual_end": "Hours of work every month",
             "rows": ["Invoice", "Accounting entry", "Monthly report"], "live": "Ready to send",
             "value": "Invoices and reports prepare themselves, with no copy-and-paste errors."},
        ],
        "flow_lbl": ("Incoming data", "The system", "The result"),
        "rows_lbl": ("Today, by hand", "With the system, automatically", "manual steps"),
        "svc_h": "Services", "svc_p": "From websites to CRM, from AI to financial control: different disciplines that work together.", "svc_all": "All services",
        "sol_h": "Solutions", "sol_p": "For each industry we combine the right services into a single system. Here are a few examples.", "sol_all": "All solutions",
        "reef_h": "Designed like <em>a reef</em>", "reef_p": "The reef is one of the most efficient ecosystems on Earth. Its five principles guide every project.",
        "reef_words": ["Diversity", "Symbiosis", "Connection", "Layered growth", "Resilience"], "reef_a": "Our philosophy",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Websites, custom applications, artificial intelligence, company brain and dashboards.",
        "h1": "Ten disciplines, <em>one</em> system.",
        "sub": "From the website that brings in clients to the system that runs the company: we combine them around your goals, never starting from an off-the-shelf package.",
    },
    "solutions": {
        "title": "Solutions · Reef 7 Lab", "desc": "Software solutions for e-commerce, professional firms, education and growing companies.",
        "h1": "Solutions built <em>for your industry</em>.",
        "sub": "Every industry has its bottlenecks. For each one we combine the right services into a single system: here are the cases we tackle most often.",
        "lbl": ("The challenge", "What we build", "The outcome", "Services involved"),
    },
    "studio": {
        "title": "Lab · Reef 7 Lab", "desc": "The reef philosophy: how Reef 7 Lab designs software that grows connected.",
        "h1": "The reef <em>philosophy</em>.",
        "sub": "Coral reefs cover less than 1% of the ocean floor, yet they're home to a quarter of all marine life. Their secret isn't size: it's architecture. That's the model behind every system we build.",
        "principles": [
            ("01", "Diversity", "Thousands of species share a reef, each with a precise role. None does everything; each does one thing exceptionally well. Software works the same way. A website, an automation, an assistant, a dashboard: different tools, each chosen for what it does best. Never technology for its own sake."),
            ("02", "Symbiosis", "Coral lives thanks to the algae it hosts, and the algae thanks to the coral. Together they build what neither could alone. That's how people and technology work in our systems: AI takes on the repetitive work, people take on what needs judgment, creativity and relationships."),
            ("03", "Connection", "Nothing on a reef lives in isolation. Currents, nutrients and species move through a single network, and every part strengthens the others. Our systems talk to each other: data is entered once and reaches everywhere it's needed. No silos, no copy and paste, no competing versions of the truth."),
            ("04", "Layered growth", "Coral grows a few millimetres a year, layer upon layer, building structures that last for centuries. We design with the same patience: solid foundations first, then features added over time. The result is software that gains value instead of ageing."),
            ("05", "Resilience", "A healthy reef weathers storms and adapts when currents shift. Software should do the same. We build flexible architectures, ready to evolve with your company, the market and the technologies still to come."),
        ],
        "seven_k": "Why 7", "seven_h": "Seven reefs, <em>one name</em>.", "seven_a": "Meet the seven reefs",
        "seven_p": "The 7 is seven coral reefs, from the Red Sea to Polynesia, that we've committed to protect. Every project we deliver brings us closer to one of them: it's the number that reminds us who we work for, beyond our clients.",
        "who_big": "Behind Reef 7 Lab is <em>Alessandro</em>.",
        "who": ["In recent years he has designed software, automations and sales funnels for growing companies, seeing first-hand how much value gets lost between disconnected tools and manual processes.",
                "He founded Reef 7 Lab to give companies what is usually reserved for large groups: custom systems, applied artificial intelligence and a single point of contact who knows every line of the project.",
                "His connection to the sea is personal: for several years he was an active member of 2hands Ancona, the volunteer group that cleans beaches and coastlines of litter."],
        "sign": ("Alessandro", "Founder, Reef 7 Lab"),
        "photo_alt": "Alessandro, founder of Reef 7 Lab",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Contact Reef 7 Lab about a new project.",
        "h1": "Tell us where you want to <em>go</em>.",
        "sub": "A few lines about your goals and obstacles are enough. In a first 30-minute conversation, with no commitment, we learn the context and tell you frankly whether, and how, we can help.",
        "info": [("Email", None), ("Response time", "Within one business day"), ("Based in", "Italy · working remotely"), ("Languages", "English, Italiano")],
        "next_k": "What happens next",
        "next": [("You write to us", "Tell us about your goals, timeline and context. A few lines are plenty."),
                 ("We reply", "Within one business day, with a few first questions and a proposed date."),
                 ("First consultation", "30 minutes, free and with no commitment, to work out together whether and how we can help.")],
        "form_h": "Let's talk about your project",
        "f": {"name": "Full name", "email": "Work email", "company": "Company", "want": "What do you need",
              "msg": "Tell us about the project", "ph": "Goals, timeline and what you'd like to improve",
              "opts": ["Website or landing page", "Custom application", "CRM and sales", "Bookings and email marketing", "Artificial intelligence", "Company brain", "Dashboards and financial control", "Integrations and owned software", "Not sure yet"],
              "privacy": "I agree to the processing of my data so you can get back to me about this request.",
              "req": "Required fields", "send": "Send request", "sending": "Sending…",
              "ok_h": "Request sent.", "ok_p": "Thank you! We'll reply within one business day at the address you provided.",
              "err": "Something went wrong. Please try again or email us directly at"},
        "subject": "New enquiry from the website",
    },
},
}



def eco(H, pre):
    """Sezione 'Un unico sistema': tre flussi concreti, ognuno da dati in entrata a sistema a risultato, con schede."""
    li, lc, lo = H["flow_lbl"]

    def mini(f):
        rows = f["rows"]
        if f["kind"] == "dash":
            bars = (30, 44, 38, 56, 52, 70, 86)
            spark = "".join(f'<b style="height:{h}%"></b>' for h in bars)
            body = f'<div class="mu-spark">{spark}</div>' + "".join(f'<div class="mu-row"><span>{r}</span><i style="--w:{w}%"></i></div>' for r, w in zip(rows, (78, 46, 64)))
        elif f["kind"] == "crm":
            body = '<div class="mu-contact"><span class="mu-avatar"></span><div><b></b><i></i></div></div>' + "".join(f'<div class="mu-step"><span class="tick">✓</span>{r}</div>' for r in rows)
        else:
            body = '<div class="mu-doc"><div class="mu-doc-head"><b></b><i></i></div><i></i><i></i><i class="short"></i></div>' + "".join(f'<div class="mu-step"><span class="tick">✓</span>{r}</div>' for r in rows)
        return f'<div class="mu mu-{f["kind"]}">{body}<p class="mu-live"><span class="dot"></span>{f["live"]}</p></div>'

    tabs = "".join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}">{f["tab"]}</button>' for i, f in enumerate(H["flows"]))
    rb, ra, rsteps = H["rows_lbl"]
    panels = "".join(f"""
      <div class="flow-panel"{"" if i == 0 else " hidden"}>
        <div class="fl-row fl-before">
          <div class="fl-row-head"><span class="mono">{rb}</span><span class="count">{len(f["manual"])} {rsteps}</span></div>
          <ol class="manual">{"".join(f'<li><span class="n">{j}</span>{m}</li>' for j, m in enumerate(f["manual"], 1))}<li class="end">{f["manual_end"]}</li></ol>
        </div>
        <div class="fl-row fl-after">
          <div class="fl-row-head"><span class="mono">{ra}</span><span class="count on">0 {rsteps}</span></div>
          <div class="fl-grid">
            <div class="fl-col fl-in"><span class="mono">{li}</span>{"".join(f'<span class="chip-src">{x}</span>' for x in f["in"])}</div>
            <div class="fl-link"><i></i></div>
            <div class="fl-col fl-core"><span class="mono">{lc}</span><span class="core"><img src="{pre}assets/reef7-logo.png" alt="" width="40" height="40"><b>{f["core"]}</b></span></div>
            <div class="fl-link"><i></i></div>
            <div class="fl-col fl-out"><span class="mono">{lo}</span><div class="out-card"><b class="out-title">{f["out"]}</b>{mini(f)}</div></div>
          </div>
        </div>
        <p class="fl-value">{f["value"]}</p>
      </div>""" for i, f in enumerate(H["flows"]))
    values = "".join(f"<li>{v}</li>" for v in H["values"])
    return f"""<div class="eco2">
    <div class="eco-copy">
      <p class="mono">{H['eco_k']}</p>
      <h2>{H['eco_h']}</h2>
      <p class="eco-lead">{H['eco_p']}</p>
      <ul class="eco-values">{values}</ul>
    </div>
    <div class="flow" data-flow>
      <div class="flow-tabs" role="group">{tabs}</div>
      <div class="flow-stage">{panels}
      </div>
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
      <p class="goal-org"><span class="mono">{M['partner']}</span> <a href="{url}" target="_blank" rel="noopener">{org} ↗</a></p>
    </article>"""

    # lavori: cornici navigabili (browser, telefono), schermata da scorrere o grafica senza dati
    W = WT[lang]

    def tenka_mock():
        side = "".join(f"<i>{x}</i>" for x in (["Dashboard", "Numeri", "Offerte", "Tracker", "Knowledge"] if lang == "it" else ["Dashboard", "Numbers", "Offers", "Tracker", "Knowledge"]))
        kpis = "".join(f'<div><span>{x}</span><b></b></div>' for x in (["Fatturato", "ROAS", "Margine"] if lang == "it" else ["Revenue", "ROAS", "Margin"]))
        return f"""<div class="tk"><div class="tk-side"><span class="tk-logo"></span>{side}</div>
        <div class="tk-main"><div class="tk-kpis">{kpis}</div>
          <div class="tk-chart">{"".join(f'<b style="height:{h}%"></b>' for h in (34, 42, 38, 51, 47, 58, 63, 60, 71, 69, 78, 84))}</div>
          <div class="tk-rows"><span></span><span></span><span></span></div></div></div>"""

    def frame(w):
        p = W["projects"][w["key"]]
        kind = w["frame"]
        bar = f'<div class="fr-bar"><i></i><i></i><i></i><span>{w["url"].replace("https://", "") if w["url"] and w["url"].startswith("http") else "reef7lab · " + p["name"]}</span></div>'
        if kind == "browser":
            return f'<div class="fr fr-browser">{bar}<iframe src="{pre}{w["src"]}" title="{p["name"]}" loading="lazy"></iframe></div>'
        if kind == "phone":
            return f'<div class="fr-phone-wrap"><div class="fr fr-phone"><span class="notch"></span><iframe src="{pre}{w["src"]}" title="{p["name"]}" loading="lazy"></iframe></div></div>'
        if kind == "scroll":
            return f'<div class="fr fr-browser">{bar}<div class="fr-scroll" tabindex="0" aria-label="{p["name"]}"><img src="{pre}{w["src"]}" alt="{p["name"]}" loading="lazy" width="1200"></div></div>'
        if kind == "gallery":
            # schermate dell'app con schede per passare dall'una all'altra
            imgs = "".join(f'<img src="{pre}{s}" alt="{p["name"]} · {W["shots"][j]}" loading="lazy" width="1424" height="835"{"" if j == 0 else " hidden"}>' for j, s in enumerate(w["src"]))
            tabs = "".join(f'<button type="button" aria-pressed="{"true" if j == 0 else "false"}">{W["shots"][j]}</button>' for j in range(len(w["src"])))
            return f'<div class="fr fr-browser fr-gallery" data-gallery>{bar}<div class="fr-shots">{imgs}</div></div><div class="shot-tabs">{tabs}</div>'
        return f'<div class="fr fr-browser fr-mock">{bar}{tenka_mock()}</div>'

    def project(i, w):
        p = W["projects"][w["key"]]
        lb = W["labels"]
        href = w["url"] if (w["url"] or "").startswith("http") else (pre + w["url"] if w["url"] else None)
        link = f'<a class="link" href="{href}" target="_blank" rel="noopener">{W["open"][w["frame"]]} ↗</a>' if href else ""
        return f"""<article class="project" id="{w['key']}">
  <div class="project-info">
    <span class="mono">{i:02d} · {W['hint'][w['frame']]}</span>
    <h2>{p['name']}</h2>
    <p class="project-lead">{p['lead']}</p>
    <p>{p['text']}</p>
    <ul class="project-points">{"".join(f"<li>{x}</li>" for x in p['points'])}</ul>
    <dl class="project-meta"><div><dt>{lb['client']}</dt><dd>{p['client']}</dd></div><div><dt>{lb['type']}</dt><dd>{p['type']}</dd></div><div><dt>{lb['year']}</dt><dd>{p['year']}</dd></div></dl>
    {link}
    <p class="project-note">{p['note']}</p>
  </div>
  <div class="project-frame">{frame(w)}</div>
</article>"""

    def work_card(w):
        p = W["projects"][w["key"]]
        img = f'<img src="{pre}{w["thumb"]}" alt="" loading="lazy">' if w["thumb"] else tenka_mock()
        return f'<a class="work-card2" href="{u("work")}#{w["key"]}"><div class="wc-img">{img}</div><div class="wc-meta"><h3>{p["name"]}</h3><p>{p["type"]}</p></div></a>'

    work_cards = "".join(work_card(w) for w in WORK)
    partners = "".join(f'<div class="partner"><span class="partner-tag">{tag}</span><b class="partner-name">{n}</b><span class="partner-what">{w}</span><p>{d}</p></div>' for n, tag, w, d in W["partners"])
    cq, ca = W["partners_cta"]
    partners_html = f"""<section class="block partners-block"><div class="wrap partners-in">
  <div><p class="mono">{W['partners_k']}</p><h2>{W['partners_h']}</h2><p class="partners-p">{W['partners_p']}</p>
    <p class="partners-cta">{cq} <a class="link" href="{u('contact')}">{ca} {arrow}</a></p></div>
  <div class="partners">{partners}</div>
</div></section>"""
    out["work"] = page("work", W["title"], W["desc"], head_block(L["nav"]["work"], W["h1"], W["sub"]) + f"""
<section class="wrap projects">{"".join(project(i, w) for i, w in enumerate(WORK, 1))}
</section>
{partners_html}""")

    # home
    H = L["home"]
    rows = "".join(f"""
    <a class="svc-row" href="{u('services')}#s{n}"><span class="mono">{g}</span><h3>{t}</h3><p>{d}</p><span class="go" aria-hidden="true">→</span></a>""" for n, g, t, d, *_ in L["services"] if n in ("01", "02", "03", "06", "07", "08"))
    sectors = "".join(f"""
    <a class="sector" href="{u('solutions')}#k{i}"><span class="mono">0{i}</span><h3>{x['t']}</h3><p>{x['d']}</p><ul>{"".join(f"<li>{b}</li>" for b in x['build'][:3])}</ul></a>""" for i, x in enumerate(L["sectors"][:3], 1))
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
  <div class="head"><h2>{W['home_h']}</h2><p>{W['home_p']}</p></div>
  <div class="work-grid">{work_cards}</div>
  <a class="link" href="{u('work')}">{W['home_a']} {arrow}</a>
</div></section>
{partners_html}
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
    # servizi divisi per gruppo: un'etichetta all'inizio di ogni gruppo
    svc, last = "", None
    for n, g, t, short, long, li in L["services"]:
        if g != last:
            svc += f'\n  <p class="svc-group mono">{g}</p>'
            last = g
        svc += f"""
  <article class="svc" id="s{n}">
    <span class="mono">{n}</span>
    <div><h2>{t}</h2><p class="tag">{short}</p><p class="lead">{long}</p></div>
    <div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
  </article>"""
    out["services"] = page("services", SP["title"], SP["desc"], head_block(L["nav"]["services"], SP["h1"], SP["sub"]) + f"""
<section class="wrap" style="padding-bottom:clamp(80px,10vw,150px)">{svc}
</section>""")

    # soluzioni
    SO = L["solutions"]; lb = SO["lbl"]
    svc_name = {n: t for n, _g, t, *_ in L["services"]}
    cases = "".join(f"""
  <article class="case" id="k{i}">
    <span class="mono">0{i}</span>
    <div><h2>{x['t']}</h2><p class="lead">{x['d']}</p>
      <p class="case-svc-k mono">{lb[3]}</p>
      <div class="case-svc">{"".join(f'<a href="{u("services")}#s{n}">{svc_name[n]}</a>' for n in x['svc'])}</div></div>
    <div><dl>
      <div><dt>{lb[0]}</dt><dd>{x['pain']}</dd></div>
      <div><dt>{lb[1]}</dt><dd><ul class="case-build">{"".join(f"<li>{b}</li>" for b in x['build'])}</ul></dd></div>
      <div><dt>{lb[2]}</dt><dd class="case-out">{x['out']}</dd></div>
    </dl></div>
  </article>""" for i, x in enumerate(L["sectors"], 1))
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
<section class="block" style="border-top:0;padding-top:0"><div class="wrap">
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
<section class="block"><div class="wrap seven">
  <div><p class="mono">{St['seven_k']}</p><h2>{St['seven_h']}</h2><p>{St['seven_p']}</p>
    <a class="link" href="{u('mission')}">{St['seven_a']} {arrow}</a></div>
  <div class="reef-map seven-map" id="reef-map" data-points="{map_data}" data-world="https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-110m.json">
    <svg viewBox="0 0 1000 500" role="img" aria-label="{St['seven_h'].replace('<em>', '').replace('</em>', '')}"></svg>
  </div>
</div></section>
<section class="block"><div class="wrap about">
  <div class="portrait"><img src="{pre}assets/alessandro.jpg" alt="{St['photo_alt']}" width="512" height="512"></div>
  <div><p class="big">{St['who_big']}</p>{who}
    <div class="sign"><b>{St['sign'][0]}</b><span>{St['sign'][1]}</span></div></div>
</div></section>""", extra=libs + f'\n<script src="{pre}mission.js?v={VERSION}"></script>')

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
    for old in ["prezzi.html", "studio.html", "en/pricing.html", "en/studio.html"]:
        (ROOT / old).unlink(missing_ok=True)
        (ROOT / "alt" / old).unlink(missing_ok=True)
    for lang in T:
        build(lang)
    # versione B: stesso contenuto, stile editoriale (styles.css + alt-overrides.css)
    alt_css = (ROOT / "styles.css").read_text(encoding="utf-8") + "\n" + (ROOT / "alt-overrides.css").read_text(encoding="utf-8")
    (ROOT / "alt.css").write_text(alt_css, encoding="utf-8")
    for lang in T:
        build(lang, "alt")
