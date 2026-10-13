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
    "title": "Missione · Reef 7 Lab", "desc": "Ogni progetto di Reef 7 Lab sostiene chi protegge la flora e la fauna marina.",
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
    "home_k": "Missione", "home_h": "Ogni progetto <em>protegge il mare</em>.", "home_p": "Il 7 nel nostro nome sono sette barriere coralline. Ogni progetto che realizziamo aiuta a proteggerle, una alla volta. Ora stiamo sostenendo:",
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
    "title": "Lavori · Reef 7 Lab", "desc": "Progetti realizzati da Reef 7 Lab: applicazioni, siti e strumenti per aziende.",
    "h1": "Progetti che lavorano <em>ogni giorno</em>.",
    "sub": "Alcuni dei sistemi che abbiamo progettato e costruito. I siti qui sotto sono veri: puoi esplorarli e cliccarli direttamente in questa pagina.",
    "labels": {"client": "Cliente", "type": "Tipo", "year": "Anno"},
    "open": {"browser": "Apri il sito", "phone": "Apri la demo", "scroll": "Visita il sito"},
    "hint": {"browser": "Sito navigabile: clicca e scorri", "phone": "Demo interattiva: prova l'app", "scroll": "Scorri per vedere la pagina", "gallery": "Schermate dell'app", "mock": "Applicazione privata"},
    "shots": ["Dashboard", "Tracker", "Accesso"],
    "projects": {
        "tenka": {"name": "Tenka OS", "client": "Tenka", "type": "Applicazione web su misura", "year": "2026",
                  "lead": "Il sistema operativo di un business e-commerce, in un'unica piattaforma.",
                  "text": "Vendite e spesa pubblicitaria si sincronizzano da sole, i margini di ogni offerta si calcolano in automatico e il team lavora su obiettivi condivisi, con tutte le procedure dell'azienda raccolte in una knowledge base interna.",
                  "points": ["Dati di vendita e advertising sincronizzati in automatico", "Margini e redditività di ogni offerta", "Knowledge base interna con procedure e documenti", "Accesso protetto con verifica in due passaggi"],
                  "note": "Schermate con dati dimostrativi: l'app è privata e i dati reali restano riservati. Demo dal vivo su richiesta."},
        "dailypeak": {"name": "My Daily Peak", "client": "Full Peak", "type": "Web app per i clienti, integrata in Shopify", "year": "2026",
                      "lead": "Un piano giornaliero personale che accompagna il cliente dopo l'acquisto.",
                      "text": "Chi acquista sceglie un obiettivo, fa un check-in di pochi secondi al giorno e vede i propri progressi settimana dopo settimana. L'app è riservata ai clienti, vive dentro il negozio e ricorda il riordino al momento giusto.",
                      "points": ["Piano costruito sull'obiettivo del cliente", "Accesso riservato a chi ha acquistato", "Progressi e traguardi settimanali", "Integrata nel tema Shopify, senza app esterne"],
                      "note": "Demo con dati di prova."},
        "fullpeak": {"name": "Full Peak", "client": "Full Peak", "type": "Negozio online Shopify", "year": "2026",
                     "lead": "Il negozio online di un brand di integratori, pensato per convertire.",
                     "text": "Una pagina prodotto che spiega il valore in pochi secondi, offerte chiare, recensioni dei clienti in primo piano e un'esperienza costruita per chi acquista dal telefono.",
                     "points": ["Pagina prodotto orientata alla conversione", "Offerte e bundle", "Recensioni e prova sociale", "Esperienza ottimizzata per mobile"],
                     "note": "Il negozio non può essere incorporato: scorri l'anteprima o visitalo dal pulsante."},
        "maisenzagioie": {"name": "Maisenzagioie", "client": "Marica Viciglione", "type": "Sito su misura per un brand artigianale", "year": "2026",
                          "lead": "Il sito di un brand di gioielli in macramè fatti a mano.",
                          "text": "Catalogo per collezioni, un configuratore per creare la propria collana scegliendo fili e pietre e un pannello privato con cui la titolare aggiorna prodotti e prezzi in autonomia.",
                          "points": ["Configuratore \"Crea la tua collana\"", "Catalogo per collezioni", "Pannello di gestione privato", "Design su misura e caricamento rapido"],
                          "note": "Anteprima del sito."},
    },
    "home_h": "Lavori", "home_p": "Alcuni progetti recenti. Puoi esplorarli dal vivo nella pagina Lavori.", "home_a": "Tutti i lavori",
},
"en": {
    "title": "Work · Reef 7 Lab", "desc": "Projects by Reef 7 Lab: applications, websites and tools for businesses.",
    "h1": "Projects that work <em>every day</em>.",
    "sub": "A few of the systems we've designed and built. The websites below are real: you can explore and click through them right on this page.",
    "labels": {"client": "Client", "type": "Type", "year": "Year"},
    "open": {"browser": "Open the website", "phone": "Open the demo", "scroll": "Visit the website"},
    "hint": {"browser": "Live website: click and scroll", "phone": "Interactive demo: try the app", "scroll": "Scroll to see the page", "gallery": "App screenshots", "mock": "Private application"},
    "shots": ["Dashboard", "Tracker", "Sign-in"],
    "projects": {
        "tenka": {"name": "Tenka OS", "client": "Tenka", "type": "Custom web application", "year": "2026",
                  "lead": "The operating system of an e-commerce business, in a single platform.",
                  "text": "Sales and ad spend sync automatically, the margins of every offer are calculated on their own, and the team works towards shared goals, with all company procedures gathered in an internal knowledge base.",
                  "points": ["Sales and advertising data synced automatically", "Margins and profitability for every offer", "Internal knowledge base with procedures and documents", "Secure access with two-step verification"],
                  "note": "Screenshots with sample data: the app is private and real data stays confidential. Live demo on request."},
        "dailypeak": {"name": "My Daily Peak", "client": "Full Peak", "type": "Customer web app, built into Shopify", "year": "2026",
                      "lead": "A personal daily plan that stays with customers after they buy.",
                      "text": "Customers pick a goal, check in for a few seconds a day and see their progress week after week. The app is reserved for customers, lives inside the store and reminds them to reorder at the right moment.",
                      "points": ["A plan built around each customer's goal", "Access reserved for people who bought", "Weekly progress and milestones", "Built into the Shopify theme, no external apps"],
                      "note": "Demo with sample data."},
        "fullpeak": {"name": "Full Peak", "client": "Full Peak", "type": "Shopify online store", "year": "2026",
                     "lead": "The online store of a supplement brand, built to convert.",
                     "text": "A product page that explains the value in seconds, clear offers, customer reviews front and centre, and an experience designed for people who shop on their phone.",
                     "points": ["Conversion-focused product page", "Offers and bundles", "Reviews and social proof", "Optimised for mobile"],
                     "note": "The store can't be embedded: scroll the preview or visit it with the button."},
        "maisenzagioie": {"name": "Maisenzagioie", "client": "Marica Viciglione", "type": "Custom website for an artisan brand", "year": "2026",
                          "lead": "The website of a brand of handmade macramé jewellery.",
                          "text": "A catalogue by collection, a configurator to design your own necklace by choosing threads and stones, and a private panel the owner uses to update products and prices on her own.",
                          "points": ["\"Design your necklace\" configurator", "Catalogue by collection", "Private management panel", "Custom design and fast loading"],
                          "note": "Website preview."},
    },
    "home_h": "Work", "home_p": "A few recent projects. You can explore them live on the Work page.", "home_a": "All work",
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
    "nav": {"work": "Lavori", "services": "Servizi", "solutions": "Soluzioni", "mission": "Missione", "studio": "Lab", "contact": "Contatti"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot": "© 2026 Reef 7 Lab · Sviluppo software e intelligenza artificiale",
    "cta_k": "Nuovo progetto", "cta_h": "Costruiamo il tuo <em>reef</em>.",
    "services": [
        ("01", "Siti web", "Il primo venditore della tua azienda, attivo giorno e notte.",
         "Chi arriva sul tuo sito decide in pochi secondi se fidarsi. Costruiamo siti che rispondono subito alle domande giuste, accompagnano verso il contatto e si aggiornano senza dover chiamare nessuno.",
         ["Struttura e testi pensati per convertire", "Design su misura, nessun template", "Caricamento rapido su ogni dispositivo", "Ottimizzazione per Google", "Ogni richiesta tracciata"]),
        ("02", "Applicazioni su misura", "Il software si adatta a come lavori. Non il contrario.",
         "Se il tuo team passa più tempo ad aggirare un gestionale che a usarlo, il problema non è il team. Progettiamo gestionali, portali clienti e strumenti interni attorno ai processi reali della tua azienda.",
         ["Analisi dei processi e prototipo cliccabile", "Applicazioni web e desktop", "Accessi e permessi per ruolo", "Integrazione con gli strumenti che usi già", "Nuove funzioni man mano che cresci"]),
        ("03", "Intelligenza artificiale", "Le ore spese in lavoro ripetitivo tornano al tuo team.",
         "Rispondere alle stesse email, copiare dati, compilare report: è lavoro che non fa crescere nessuno. Lo affidiamo all'intelligenza artificiale, con un controllo umano dove serve, e misuriamo quanto tempo ti restituisce.",
         ["Analisi delle attività che costano più tempo", "Email, documenti e report automatici", "Contatti qualificati e smistati da soli", "Controllo umano nei passaggi delicati", "Tempo risparmiato misurato"]),
        ("04", "Company brain", "Tutto quello che sa la tua azienda, a una domanda di distanza.",
         "Procedure, documenti, risposte già date ai clienti: il sapere della tua azienda è sparso tra cartelle, chat e persone. Lo raccogliamo in un assistente che risponde al team in pochi secondi e indica sempre da dove viene l'informazione.",
         ["Raccolta e organizzazione dei documenti", "Risposte con la fonte, sempre verificabili", "Ognuno vede solo ciò che gli compete", "Contenuti aggiornati nel tempo", "Dati riservati e protetti"]),
        ("05", "Dashboard e dati", "I numeri che contano, senza aprire dieci programmi.",
         "Se per sapere come sta andando il mese devi chiedere a tre persone e aspettare un Excel, decidi sempre in ritardo. Colleghiamo le tue fonti di dati in un'unica dashboard, aggiornata da sola e leggibile in un colpo d'occhio.",
         ["Scelta degli indicatori che guidano il business", "Collegamento a tutte le fonti di dati", "Aggiornamento automatico", "Viste diverse per direzione e team", "Avvisi quando qualcosa cambia"]),
    ],
    "sectors": [
        ("E-commerce", "Vendi di più senza assumere qualcuno per gestire il caos.",
         ["Dashboard di vendite e margini", "Assistenza clienti automatizzata", "Strumenti per ordini e magazzino"],
         "Ordini, campagne e assistenza vivono in strumenti diversi. Scopri a fine mese cosa ha funzionato, quando è troppo tardi per correggere.",
         "Un sistema che riunisce vendite, pubblicità e margini in un'unica vista, con le domande più frequenti dei clienti gestite dall'intelligenza artificiale.",
         "Sai ogni giorno quanto guadagni davvero, e il team si occupa di crescere invece di rincorrere gli ordini."),
        ("Studi professionali", "Meno burocrazia, più tempo per i clienti.",
         ["Portali clienti riservati", "Archiviazione automatica dei documenti", "Assistente sulle procedure dello studio"],
         "Documenti da cercare, scadenze da ricordare, le stesse domande dei clienti ogni settimana: ore preziose che non puoi fatturare.",
         "Un portale riservato per i clienti, documenti che si archiviano da soli e un assistente che conosce a fondo le procedure dello studio.",
         "Più ore dedicate alla consulenza, meno errori e clienti che si sentono davvero seguiti."),
        ("Formazione e coaching", "Un'esperienza digitale all'altezza di ciò che insegni.",
         ["Piattaforme per corsi e community", "Funnel e automazioni di vendita", "Assistente per studenti e team"],
         "Corsi su una piattaforma, community su un'altra, vendite gestite a mano: gli studenti si perdono tra un passaggio e l'altro.",
         "Un'unica piattaforma per corsi e community, collegata a funnel e automazioni che accompagnano ogni studente dall'iscrizione al risultato.",
         "Studenti più coinvolti, più rinnovi e un'attività che cresce senza moltiplicare il lavoro."),
        ("Aziende in crescita", "Cresci senza perdere il controllo.",
         ["Gestionali su misura", "Integrazione degli strumenti esistenti", "Dashboard per la direzione"],
         "Più clienti vogliono dire più fogli di calcolo, più email, più errori. Gli strumenti che bastavano due anni fa oggi rallentano tutto.",
         "Un gestionale costruito sui tuoi processi, collegato agli strumenti che usi già, con una dashboard che mostra alla direzione il quadro completo.",
         "Un'unica fonte di verità per tutta l'azienda e decisioni prese su dati certi."),
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
        "eco_p": "Nella maggior parte delle aziende i dati vivono in strumenti separati: messaggi, ordini, fatture, fogli di calcolo. Colleghiamo questi strumenti in un'unica piattaforma, così le informazioni si aggiornano da sole e gli indicatori che contano sono sempre disponibili in un solo posto.",
        "tools": ["Email", "WhatsApp", "Excel", "CRM", "E-commerce", "Contabilità"],
        "before": ("Prima", ["Gli stessi dati inseriti più volte, in programmi diversi", "Informazioni sparse e difficili da confrontare", "Report preparati a mano, spesso già superati"]),
        "after": ("Dopo", ["Ogni dato inserito una sola volta", "Informazioni collegate e sempre aggiornate", "Indicatori chiari per decisioni consapevoli"]),
        "card": ("Dashboard", ["Vendite", "Margini", "Clienti"], "Aggiornata in tempo reale"),
        "status": ("Prima: ogni strumento lavora da solo e i dati restano isolati.", "Dopo: gli strumenti condividono i dati e tutto è visibile in un'unica dashboard."),
        "svc_h": "Servizi", "svc_p": "Cinque competenze che lavorano insieme, per un'azienda più veloce e più lucida nelle decisioni.", "svc_all": "Tutti i servizi",
        "sol_h": "Soluzioni", "sol_p": "Ogni settore ha i suoi colli di bottiglia. Ecco quelli che conosciamo meglio.", "sol_all": "Tutte le soluzioni",
        "reef_h": "Progettati come <em>un reef</em>", "reef_p": "Il reef è tra gli ecosistemi più efficienti della Terra. I suoi cinque principi guidano ogni progetto.",
        "reef_words": ["Diversità", "Simbiosi", "Connessione", "Crescita stratificata", "Resilienza"], "reef_a": "La nostra filosofia",
    },
    "services_p": {
        "title": "Servizi · Reef 7 Lab", "desc": "Siti web, applicazioni su misura, intelligenza artificiale, company brain e dashboard.",
        "h1": "Cinque competenze, <em>un solo</em> sistema.",
        "sub": "Dal sito che porta clienti al gestionale che fa girare l'azienda: ogni soluzione parte dai tuoi obiettivi, mai da un pacchetto preconfezionato.",
    },
    "solutions": {
        "title": "Soluzioni · Reef 7 Lab", "desc": "Soluzioni software per e-commerce, studi professionali, formazione e aziende in crescita.",
        "h1": "Ogni settore ha il suo <em>collo di bottiglia</em>.",
        "sub": "Lo conosciamo da vicino, e sappiamo come trasformarlo in un vantaggio. Questi sono i casi che affrontiamo più spesso.",
        "lbl": ("La sfida", "La soluzione", "Il risultato"),
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
        "title": "Contatti · Reef 7 Lab", "desc": "Contatta Reef 7 Lab per un nuovo progetto.",
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
              "opts": ["Sito web", "Applicazione su misura", "Intelligenza artificiale", "Company brain", "Dashboard e dati", "Non lo so ancora"],
              "privacy": "Acconsento al trattamento dei miei dati per essere ricontattato in merito alla richiesta.",
              "req": "Campi obbligatori", "send": "Invia la richiesta", "sending": "Invio in corso…",
              "ok_h": "Richiesta inviata.", "ok_p": "Grazie! Ti risponderemo entro un giorno lavorativo all'indirizzo che ci hai indicato.",
              "err": "Invio non riuscito. Riprova o scrivici direttamente a"},
        "subject": "Nuova richiesta dal sito",
    },
},
"en": {
    "nav": {"work": "Work", "services": "Services", "solutions": "Solutions", "mission": "Mission", "studio": "Lab", "contact": "Contact"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot": "© 2026 Reef 7 Lab · Software and AI development",
    "cta_k": "New project", "cta_h": "Let's build your <em>reef</em>.",
    "services": [
        ("01", "Websites", "Your company's best salesperson, working day and night.",
         "Visitors decide in seconds whether to trust you. We build websites that answer the right questions straight away, guide people towards getting in touch, and can be updated without calling anyone.",
         ["Structure and copy built to convert", "Custom design, no templates", "Fast loading on every device", "Optimised for Google", "Every enquiry tracked"]),
        ("02", "Custom applications", "Software that fits the way you work. Not the other way round.",
         "If your team spends more time working around a system than using it, the problem isn't the team. We design management tools, client portals and internal software around the way your company really works.",
         ["Process analysis and clickable prototype", "Web and desktop applications", "Role-based access and permissions", "Integration with the tools you already use", "New features as you grow"]),
        ("03", "Artificial intelligence", "The hours lost to repetitive work go back to your team.",
         "Answering the same emails, copying data, filling in reports: work that helps no one grow. We hand it to AI, with human checks where they matter, and measure exactly how much time it gives back.",
         ["Finding the tasks that cost the most time", "Automated email, documents and reports", "Leads qualified and routed automatically", "Human review at the critical steps", "Time saved, measured"]),
        ("04", "Company brain", "Everything your company knows, one question away.",
         "Procedures, documents, answers already given to clients: your company's knowledge is scattered across folders, chats and people. We bring it together in an assistant that answers your team in seconds and always shows where the information comes from.",
         ["Collecting and organising documents", "Answers with sources, always verifiable", "Everyone sees only what they should", "Content that stays up to date", "Private, protected data"]),
        ("05", "Dashboards and data", "The numbers that matter, without opening ten programs.",
         "If finding out how the month is going means asking three people and waiting for a spreadsheet, you'll always decide too late. We connect your data sources into a single dashboard that updates itself and reads at a glance.",
         ["Choosing the metrics that drive the business", "Connecting every data source", "Automatic updates", "Different views for leadership and teams", "Alerts when something changes"]),
    ],
    "sectors": [
        ("E-commerce", "Sell more without hiring someone to manage the chaos.",
         ["Sales and margin dashboards", "Automated customer support", "Tools for orders and inventory"],
         "Orders, campaigns and support live in different tools. You find out what worked at the end of the month, when it's too late to fix.",
         "One system that brings sales, advertising and margins into a single view, with the most common customer questions handled by AI.",
         "You know every day how much you're really making, and your team focuses on growth instead of chasing orders."),
        ("Professional firms", "Less paperwork, more time for clients.",
         ["Private client portals", "Automatic document filing", "Assistant trained on the firm's procedures"],
         "Documents to find, deadlines to remember, the same client questions every week: valuable hours you can't bill.",
         "A private client portal, documents that file themselves and an assistant that knows the firm's procedures inside out.",
         "More hours for advisory work, fewer mistakes and clients who feel genuinely looked after."),
        ("Education and coaching", "A digital experience as good as what you teach.",
         ["Course and community platforms", "Sales funnels and automation", "Assistant for students and team"],
         "Courses on one platform, community on another, sales handled by hand: students get lost between one step and the next.",
         "One platform for courses and community, connected to funnels and automations that guide every student from sign-up to results.",
         "More engaged students, more renewals and a business that grows without multiplying the workload."),
        ("Growing companies", "Grow without losing control.",
         ["Custom management systems", "Integration of existing tools", "Executive dashboards"],
         "More clients mean more spreadsheets, more emails, more mistakes. The tools that were enough two years ago now slow everything down.",
         "A management system built around your processes, connected to the tools you already use, with a dashboard that gives leadership the full picture.",
         "A single source of truth for the whole company, and decisions made on solid data."),
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
        "eco_p": "In most companies, data lives in separate tools: messages, orders, invoices, spreadsheets. We connect these tools into a single platform, so information updates itself and the metrics that matter are always available in one place.",
        "tools": ["Email", "WhatsApp", "Spreadsheets", "CRM", "E-commerce", "Accounting"],
        "before": ("Before", ["The same data entered several times, in different programs", "Scattered information that's hard to compare", "Reports prepared by hand, often already out of date"]),
        "after": ("After", ["Every piece of data entered once", "Connected information, always up to date", "Clear metrics for informed decisions"]),
        "card": ("Dashboard", ["Sales", "Margins", "Clients"], "Updated in real time"),
        "status": ("Before: each tool works on its own and data stays isolated.", "After: the tools share their data and everything is visible in a single dashboard."),
        "svc_h": "Services", "svc_p": "Five disciplines that work together, for a company that moves faster and decides more clearly.", "svc_all": "All services",
        "sol_h": "Solutions", "sol_p": "Every industry has its bottlenecks. These are the ones we know best.", "sol_all": "All solutions",
        "reef_h": "Designed like <em>a reef</em>", "reef_p": "The reef is one of the most efficient ecosystems on Earth. Its five principles guide every project.",
        "reef_words": ["Diversity", "Symbiosis", "Connection", "Layered growth", "Resilience"], "reef_a": "Our philosophy",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Websites, custom applications, artificial intelligence, company brain and dashboards.",
        "h1": "Five disciplines, <em>one</em> system.",
        "sub": "From the website that brings in clients to the system that runs the company: every solution starts from your goals, never from an off-the-shelf package.",
    },
    "solutions": {
        "title": "Solutions · Reef 7 Lab", "desc": "Software solutions for e-commerce, professional firms, education and growing companies.",
        "h1": "Every industry has its <em>bottleneck</em>.",
        "sub": "We know them up close, and we know how to turn them into an advantage. These are the cases we tackle most often.",
        "lbl": ("The challenge", "The solution", "The outcome"),
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
    # pacchetti di dati che viaggiano dagli strumenti verso il centro
    packets = "".join(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="50" y2="50" style="animation-delay:{-i * .45:.2f}s"/>' for i, (x, y) in enumerate(ring))
    ct, rows, live = H["card"]
    bars = [(28, 40, 36, 55, 68, 92), (45, 38, 52, 60, 58, 78), (22, 30, 44, 41, 62, 84)]
    card_rows = "".join(
        f'<div class="hc-row"><span>{name}</span><i class="spark">{"".join(f"<b style=\"height:{h}%\"></b>" for h in bars[j])}</i></div>'
        for j, name in enumerate(rows))
    sb, sa = H["status"]
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
    <div class="eco-visual">
    <div class="eco-stage" aria-hidden="true">
      <svg viewBox="0 0 100 100" preserveAspectRatio="none"><g class="broken">{seg}</g><g class="links">{lines}</g><g class="packets">{packets}</g></svg>
      {pills}
      <div class="hub-card">
        <div class="hc-top"><img src="{pre}assets/reef7-logo.png" alt="" width="22" height="22"><b>{ct}</b></div>
        {card_rows}
        <p class="hc-live"><span class="dot"></span>{live}</p>
      </div>
    </div>
    <p class="eco-status"><span class="s-before">{sb}</span><span class="s-after">{sa}</span></p>
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
    out["work"] = page("work", W["title"], W["desc"], head_block(L["nav"]["work"], W["h1"], W["sub"]) + f"""
<section class="wrap projects">{"".join(project(i, w) for i, w in enumerate(WORK, 1))}
</section>""")

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
  <div class="head"><h2>{W['home_h']}</h2><p>{W['home_p']}</p></div>
  <div class="work-grid">{work_cards}</div>
  <a class="link" href="{u('work')}">{W['home_a']} {arrow}</a>
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
<section class="block"><div class="wrap why">
  <p class="mono">{St['seven_k']}</p>
  <div><h2>{St['seven_h']}</h2><p>{St['seven_p']}</p>
    <a class="link" href="{u('mission')}">{St['seven_a']} {arrow}</a></div>
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
