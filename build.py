"""Genera il sito Reef 7 Lab in italiano (cartella principale) e in inglese (cartella en/).

Uso:  python build.py
Testi ed email si cambiano qui sotto; poi si rilancia lo script.
"""
import hashlib
import math
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "lancioni.ale@gmail.com"
SITE_URL = "https://alelan122.github.io/reef7-lab/"
_DIMS = {}
def img_dims(rel):
    """width/height reali di un'immagine locale, da scrivere nel tag <img>."""
    if rel not in _DIMS:
        try:
            from PIL import Image
            with Image.open(Path(__file__).parent / rel) as im:
                _DIMS[rel] = f' width="{im.width}" height="{im.height}"'
        except Exception:
            _DIMS[rel] = ""
    return _DIMS[rel]
# indirizzo del Worker dell'Agent AI (projects/reef7-agent): vuoto = demo guidata
AGENT_URL = ""

# Regole di sicurezza delle pagine: script solo dal sito (più lo script in pagina, riconosciuto dalla sua impronta),
# niente plugin, invii dei moduli solo verso il sito o FormSubmit, connessioni solo verso i servizi usati.
import base64 as _b64, hashlib as _hl
INLINE_JS = 'window.REEF = { email: "%s", agent: "%s" };'
def csp_meta(inline_js):
    h = _b64.b64encode(_hl.sha256(inline_js.encode("utf-8")).digest()).decode()
    agent = " " + AGENT_URL.split("/", 3)[0] + "//" + AGENT_URL.split("/", 3)[2] if AGENT_URL.startswith("https://") else ""
    pol = ("default-src 'self'; "
           f"script-src 'self' https://cdn.jsdelivr.net 'sha256-{h}'; "
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
           "font-src 'self' https://fonts.gstatic.com; "
           "img-src 'self' data: https:; "
           f"connect-src 'self' https://formsubmit.co https://cdn.jsdelivr.net https://*.workers.dev https://dns.google https://observatory-api.mdn.mozilla.net{agent}; "
           "frame-src 'self' https://alelan122.github.io; "
           "object-src 'none'; base-uri 'self'; form-action 'self' https://formsubmit.co; upgrade-insecure-requests")
    return f'<meta http-equiv="Content-Security-Policy" content="{pol}">\n  <meta name="referrer" content="strict-origin-when-cross-origin">'
# versione dei file di stile e script: cambia quando cambiano, così il browser non usa copie vecchie

# ---------------- Missione: il 5% degli introiti al mare ----------------
SHARE = 5        # percentuale degli introiti di ogni progetto destinata al mare
RAISED = 0       # euro già destinati finora: aggiornalo dopo ogni donazione e rilancia lo script
# obiettivi in ordine: (latitudine, longitudine, obiettivo in euro, organizzazione, sito)
GOALS = [
    (27.26, 33.81, 5000, "HEPCA", "https://www.hepca.org"),
    (4.17, 73.50, 7500, "Reefscapers", "https://reefscapers.com"),
    (10.09, 99.84, 10000, "New Heaven Reef Conservation", "https://www.newheavenreefconservation.org"),
    (-8.70, 115.20, 12500, "Coral Triangle Center", "https://coraltrianglecenter.org"),
    (-1.90, 130.20, 15000, "Misool Foundation", "https://www.misoolfoundation.org"),
    (-18.30, 147.70, 20000, "Great Barrier Reef Foundation", "https://www.barrierreef.org"),
    (-17.53, -149.83, 30000, "Coral Gardeners", "https://coralgardeners.org"),
]
MT = {
"it": {
    "title": "Mission · Reef 7 Lab", "desc": "Reef 7 Lab vuole aiutare a proteggere sette barriere coralline, un progetto alla volta.",
    "h1": "Un progetto alla volta, <em>per il mare</em>.",
    "sub": "Il nostro nome viene dal reef, e il reef è in pericolo: dagli anni '50 la copertura di corallo vivo nel mondo si è dimezzata. Per questo vogliamo che il nostro lavoro aiuti chi, ogni giorno, protegge la flora e la fauna marina.",
    "stats": [],
    "how_h": "Come funzionerà", "how": [("Il nostro obiettivo", "Vogliamo che ogni sito, app o sistema che realizziamo contribuisca a proteggere il mare."),
                                      ("Un reef alla volta", "Ci concentreremo su un reef per volta: raggiunto un obiettivo, passeremo al successivo."),
                                      ("Sempre trasparenti", "Racconteremo qui ogni passo avanti, reef dopo reef.")],
    "map_h": "Il 7 del <em>nostro nome</em>", "map_p": "Sette barriere coralline tra le più preziose del pianeta, dal Mar Rosso alla Polinesia. Sono loro il 7 di Reef 7.",
    "goals_h": "I reef che vogliamo aiutare", "goals_p": "Sette barriere coralline, una dopo l'altra: dal Mar Rosso verso il Pacifico.",
    "places": [("Mar Rosso", "Egitto", "Boe d'ormeggio che proteggono le barriere dalle ancore."),
               ("Maldive", "Oceano Indiano", "Trapianto di coralli su strutture che ne favoriscono la ricrescita."),
               ("Koh Tao", "Thailandia", "Vivai e restauro dei coralli nel Golfo di Thailandia."),
               ("Bali", "Indonesia", "Conservazione e formazione nel cuore del Triangolo dei Coralli."),
               ("Raja Ampat", "Indonesia", "Aree marine protette e pattugliamento contro la pesca illegale."),
               ("Grande Barriera Corallina", "Australia", "Ricerca e ripristino del reef più grande del mondo."),
               ("Moorea", "Polinesia francese", "Coltivazione di coralli più resistenti all'aumento delle temperature.")],
    "raised_of": "{r} raccolti di {t}", "active": "Primo obiettivo", "next": "Prossimo", "done": "Raggiunto",
    "partner": "Organizzazione", "visit": "Sito",
    "note": "Le organizzazioni indicate sono quelle a cui intendiamo destinare i contributi; non rappresentano una partnership ufficiale.",
    "why_k": "La nostra storia", "why_h": "Per noi il mare <em>non è uno slogan</em>.",
    "why_p": ["Prima di fondare Reef 7 Lab, Alessandro è stato per diversi anni membro attivo di 2hands Ancona, il gruppo di volontari che ripulisce spiagge e coste dai rifiuti.",
              "Oggi vuole portare lo stesso impegno nel lavoro di Reef 7 Lab: fare in modo che i progetti che realizziamo aiutino a proteggere il mare da cui prendiamo il nome."],
    "home_k": "Missione", "home_h": "Un progetto alla volta, <em>per il mare</em>.", "home_p": "Il 7 nel nostro nome sono sette barriere coralline che vogliamo aiutare a proteggere, una alla volta, con il nostro lavoro. Si comincia da qui:",
    "home_a": "Scopri la missione",
},
"en": {
    "title": "Mission · Reef 7 Lab", "desc": "Reef 7 Lab wants to help protect seven coral reefs, one project at a time.",
    "h1": "One project at a time, <em>for the sea</em>.",
    "sub": "Our name comes from the reef, and reefs are in danger: since the 1950s, the world's living coral cover has halved. That's why we want our work to help the people who protect marine flora and fauna every day.",
    "stats": [],
    "how_h": "How it will work", "how": [("Our goal", "We want every website, app or system we build to help protect the sea."),
                                     ("One reef at a time", "We'll focus on one reef at a time: once a goal is reached, we'll move to the next."),
                                     ("Always transparent", "We'll share every step forward here, reef by reef.")],
    "map_h": "The 7 in <em>our name</em>", "map_p": "Seven of the most precious coral reefs on the planet, from the Red Sea to Polynesia. They are the 7 in Reef 7.",
    "goals_h": "The reefs we want to help", "goals_p": "Seven coral reefs, one after another: from the Red Sea out to the Pacific.",
    "places": [("Red Sea", "Egypt", "Mooring buoys that protect reefs from anchor damage."),
               ("Maldives", "Indian Ocean", "Coral transplants onto frames that help reefs regrow."),
               ("Koh Tao", "Thailand", "Coral nurseries and reef restoration in the Gulf of Thailand."),
               ("Bali", "Indonesia", "Conservation and training at the heart of the Coral Triangle."),
               ("Raja Ampat", "Indonesia", "Marine protected areas and patrols against illegal fishing."),
               ("Great Barrier Reef", "Australia", "Research and restoration of the world's largest reef."),
               ("Moorea", "French Polynesia", "Growing corals that can withstand warmer seas.")],
    "raised_of": "{r} raised of {t}", "active": "First goal", "next": "Next", "done": "Reached",
    "partner": "Organisation", "visit": "Website",
    "note": "The organisations listed are those we intend to direct our contributions to; this does not represent an official partnership.",
    "why_k": "Our story", "why_h": "For us, the sea <em>isn't a slogan</em>.",
    "why_p": ["Before founding Reef 7 Lab, Alessandro spent several years as an active member of 2hands Ancona, the volunteer group that cleans beaches and coastlines of litter.",
              "Today he wants to bring that same commitment to Reef 7 Lab's work: making sure the projects we build help protect the sea we're named after."],
    "home_k": "Mission", "home_h": "One project at a time, <em>for the sea</em>.", "home_p": "The 7 in our name is seven coral reefs we want to help protect, one at a time, through our work. It starts here:",
    "home_a": "Discover the mission",
},
}

# ---------------- Lavori: progetti reali, senza dati privati ----------------
# frame: "browser" (sito navigabile dentro il portfolio), "phone" (app navigabile), "scroll" (schermata da scorrere), "mock" (grafica senza dati)
WORK = [
    {"key": "hubdemo", "frame": "browser", "url": "work/hub-demo/index.html", "src": "work/hub-demo/index.html", "thumb": "assets/work/thumb-hubdemo.jpg", "bar": "reef7lab · Hub aziendale"},
    {"key": "tenka", "frame": "gallery", "url": None, "src": ["assets/work/tenka-dashboard-v2.jpg", "assets/work/tenka-tracker-v2.jpg", "assets/work/tenka-login.jpg"], "thumb": "assets/work/thumb-tenka-v2.jpg"},
    {"key": "fullpeak", "frame": "scroll", "url": "https://fullpeak.store/products/full-peak-magnesium-complex", "src": "assets/work/fullpeak-pdp.jpg", "thumb": "assets/work/thumb-fullpeak.jpg"},
    {"key": "dailypeak", "frame": "phone", "url": "work/my-daily-peak/index.html", "src": "work/my-daily-peak/index.html", "thumb": "assets/work/thumb-dailypeak.jpg"},
    {"key": "maisenzagioie", "frame": "browser", "url": "work/maisenzagioie/index.html", "src": "work/maisenzagioie/index.html", "thumb": "assets/work/thumb-maisenzagioie.jpg"},
    {"key": "maisenzagioie3d", "frame": "browser", "url": "work/maisenzagioie-3d/index.html", "src": "work/maisenzagioie-3d/index.html", "thumb": "assets/work/thumb-maisenzagioie3d.jpg", "bar": "reef7lab · Configuratore 3D"},
    {"key": "crmdemo", "frame": "browser", "url": "work/crm-demo/index.html", "src": "work/crm-demo/index.html", "thumb": "assets/work/thumb-crmdemo.jpg", "bar": "reef7lab · CRM vendite"},
    {"key": "kasinolatino", "frame": "browser", "url": "https://alelan122.github.io/kasino-latino-anteprima/", "src": "https://alelan122.github.io/kasino-latino-anteprima/", "thumb": "assets/work/thumb-kasinolatino.jpg", "bar": "reef7lab · Kasino Latino"},
]
WT = {
"it": {
    "title": "Projects · Reef 7 Lab", "desc": "Una selezione di progetti di Reef 7 Lab: applicazioni, siti e strumenti per aziende.",
    "h1": "Il nostro lavoro, <em>dal vivo</em>.",
    "sub": "Una selezione di sistemi che abbiamo progettato e sviluppato, dall'idea alla messa online. Dove possibile, puoi navigarli direttamente da questa pagina.",
    "labels": {"client": "Cliente", "type": "Tipo", "year": "Anno"},
    "open": {"browser": "Apri il sito", "phone": "Apri la demo", "scroll": "Visita il negozio"},
    "hint_demo": "Demo navigabile",
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
        "maisenzagioie3d": {"name": "Configuratore 3D", "client": "Concept per Maisenzagioie", "type": "Configuratore 3D e realtà aumentata", "year": "2026",
                            "lead": "La collana si disegna e si guarda da ogni lato, prima ancora di essere annodata.",
                            "text": "Ogni scelta, dal modello al colore del filo fino alla pietra, ricostruisce la collana in 3D in tempo reale: niente foto da scattare per ogni combinazione, il modello è generato dal codice. Dal telefono si può appoggiare sul tavolo in realtà aumentata, a grandezza reale, e ogni collana creata ha un suo link da condividere.",
                            "points": ["Collana generata in 3D a ogni scelta", "Vista dettaglio su pietre, perline e intreccio", "Prova in realtà aumentata dal telefono, senza app", "Link condivisibile per ogni combinazione"],
                            "note": "Concept navigabile: prova a cambiare filo e pietra."},
        "hubdemo": {"name": "Hub aziendale", "client": "Demo · coaching nutrizionale online", "type": "Hub di tutte le piattaforme interne", "year": "2026",
                    "lead": "Tutte le piattaforme dell'azienda in un posto solo, con lo stato di ognuna sempre sotto controllo.",
                    "text": "CRM vendite, app delle coach, app clienti, email marketing, contenuti, selezione del personale: ogni piattaforma interna ha la sua scheda, con indirizzo, tipo di accesso e a cosa serve. In alto lo stato di ogni servizio, ricontrollato in automatico; sotto gli strumenti della direzione e le pagine pubbliche.",
                    "points": ["Piattaforme interne, direzione e pubblico in un'unica vista", "Stato e tempi di risposta di ogni servizio", "Accessi chiari per ogni strumento", "Il CRM vendite si apre direttamente dall'hub"],
                    "note": "Demo con dati di esempio: apri il CRM Vendite dalla prima scheda."},
        "crmdemo": {"name": "CRM vendite", "client": "Demo · coaching nutrizionale online", "type": "CRM su misura per team di vendita", "year": "2026",
                    "lead": "Il CRM costruito sul processo di vendita di un'azienda di coaching online, dal funnel al contratto.",
                    "text": "Lo stesso modello che abbiamo portato in produzione per un'azienda del fitness online: pipeline con le fasi reali (chiamata a freddo, candidatura, discovery, demo, acconto), scheda di ogni contatto con classificazione e briefing AI, cash incassato contro l'obiettivo con proiezione e semaforo, insoluti, classifica e commissioni calcolate sull'incassato.",
                    "points": ["Cash, proiezione e traiettoria verso l'obiettivo", "Pipeline kanban e lista, con motivo obbligatorio sulle perse", "Scheda lead con classificazione e briefing AI", "Insoluti, classifica e commissioni a scaglioni"],
                    "note": "Demo con dati di esempio: apri Lead e sposta un contatto in \"Chiusa\", incassato, classifica e commissioni si aggiornano da soli."},
        "kasinolatino": {"name": "Kasino Latino", "client": "Kasino Latino A.S.D.", "type": "Sito per una scuola di ballo", "year": "2026",
                         "lead": "Il nuovo sito di una scuola di salsa e bachata con tre sedi nelle Marche.",
                         "text": "Orari, sedi e corsi sono il cuore del sito: si filtrano per giorno, mostrano sempre la prossima lezione disponibile e portano dritti alla prenotazione della prova gratuita, anche su WhatsApp. Per la scuola, aggiornare la stagione significa cambiare una sola lista: tabelle, filtri e messaggi si aggiornano da soli.",
                         "points": ["Orari filtrabili per sede e per giorno", "Prenotazione della lezione di prova, anche via WhatsApp", "Istruttori, serate e gallery", "Veloce sul telefono, dove arrivano quasi tutte le visite"],
                         "note": "Anteprima navigabile del sito."},
    },
    "home_h": "Progetti", "home_p": "Una selezione di progetti recenti, da esplorare dal vivo.", "home_a": "Tutti i progetti",
    "partners_k": "Partner", "partners_h": "Partner, <em>non semplici clienti</em>.",
    "partners_p": "Lavoriamo al fianco di aziende che hanno scelto la tecnologia e l'intelligenza artificiale come leva di crescita. Con loro non ci limitiamo a consegnare un progetto: costruiamo insieme, giorno dopo giorno, i sistemi su cui si regge il loro business.",
    "partners_cta": ("Vuoi crescere con noi?", "Diventa partner"),
    "case": {"k": "Caso studio · Asia Baldoni Fitness × Tartufoli Group", "h": "Da 54 software a <em>un'unica piattaforma</em>.",
             "p": "Per un'azienda a sette cifre del fitness online abbiamo tagliato circa l'83% dei costi software e reso il lavoro operativo fino a 40 volte più veloce.",
             "kpis": [("−83%", "costi software", "da circa 60.000 a circa 10.000 l'anno"), ("40×", "più veloce", "il lavoro che prima si faceva a mano"),
                      ("−99%", "costo delle email", "100.000 invii: da quasi 1.000 $ a circa 10 €"), ("~20", "persone ogni giorno", "vendite, coach, marketing e direzione")],
             "before_k": "Prima", "before": ["54 software, spesso due o tre per la stessa cosa", "Ore perse a copiare dati da un tool all'altro", "Nessuna visione d'insieme sull'azienda"],
             "after_k": "Oggi", "after": ["Una piattaforma costruita sul loro modo di lavorare", "Il lavoro operativo richiede una frazione del tempo", "Ogni lead, call e pagamento in un'unica vista"],
             "more": "Leggi come ci siamo arrivati",
             "full": {
                 "k": "Caso studio", "h": "Meno 83% di costi software. <em>Un team 40 volte più veloce.</em>",
                 "lead": "Asia Baldoni Fitness è un'azienda a sette cifre del fitness online, con circa venti persone tra vendite, coach, marketing e operations. Era cresciuta in fretta, e per stare al passo si era appoggiata a 54 software diversi. Insieme a Tartufoli Group li abbiamo sostituiti con un'unica piattaforma, costruita sul loro modo di lavorare.",
                 "facts": [("Azienda", "Fitness online, fatturato a sette cifre"), ("Chi la usa", "Circa 20 persone, ogni giorno"), ("Tempi", "Meno di 6 mesi, da aprile a settembre 2026"), ("Ruolo", "Partner tecnologico, al fianco di Tartufoli Group")],
                 "ch": [
                     ("Il problema: crescere costava sempre di più", ["Ogni nuova esigenza portava un nuovo abbonamento. Un CRM per le vendite, un altro strumento per le email, uno per le landing, uno per i calendari, e altri strumenti ancora solo per farli parlare tra loro. A metà 2026 la spesa software era arrivata al 6,3% dei ricavi, più del doppio dell'obiettivo.",
                                                                    "Il costo però era la parte visibile. Quella nascosta era il tempo: ogni lead veniva copiato da un sistema all'altro, ogni automazione andava costruita a mano, ogni intoppo finiva sulla scrivania di una persona sola. E con i dati sparsi in decine di posti, nessuno poteva vedere davvero come stava andando l'azienda."]),
                     ("Perché ha funzionato: prima la mappa, poi il codice", ["Non siamo partiti dalla tecnologia, ma dal processo. Abbiamo mappato uno per uno tutti i flussi: da dove arriva ogni contatto, quali email riceve e quando, cosa succede a ogni passaggio di fase, chi deve fare cosa. Quella mappa è diventata la specifica esatta da ricostruire.",
                                                                                "Per questo la piattaforma non è un software generico adattato: segue le fasi reali della vendita, i ruoli reali del team e le regole reali delle commissioni. Chi la usa ritrova il proprio lavoro, solo senza gli ostacoli."]),
                     ("In quanto tempo: meno di sei mesi", ["Ad aprile l'analisi dei 54 strumenti. A luglio il nuovo CRM vendite era già in uso da tutto il team. Ad agosto la mappatura completa delle email, a settembre le email su infrastruttura propria. Ogni mese, un pezzo in più e un abbonamento in meno."]),
                     ("Con quale sforzo per il team: il minimo", ["Ogni sistema nuovo ha lavorato accanto al vecchio finché non ha funzionato da solo, e solo allora il vecchio è stato spento. Il team ha continuato a lavorare come sempre, e le segnalazioni venivano risolte giorno per giorno.",
                                                                     "Oggi le venditrici vedono in ogni scheda quali email ha aperto un contatto e quali video ha guardato. La direzione vede incassato, traiettoria e andamento del team in tempo reale. Una segmentazione o una nuova automazione, che prima richiedeva ore, si fa in pochi minuti."]),
                 ],
                 "steps_k": "Le tappe", "steps": [("Aprile 2026", "Ogni strumento e ogni costo analizzati, uno per uno"), ("Luglio 2026", "Il team vendita lavora su un CRM costruito sul suo processo"), ("Agosto 2026", "Tutte le email e le automazioni mappate e ricostruite"), ("Settembre 2026", "Email marketing in casa, con costi di invio quasi azzerati")],
                 "res_k": "I risultati", "res": [("−83%", "costi software", "Da circa 60.000 a circa 10.000 l'anno: oltre 50.000 che ogni anno tornano nella crescita."), ("40×", "più veloce", "Il lavoro operativo che prima si faceva a mano, saltando da un software all'altro.")],
                 "res2": [("−99%", "costo delle email", "100.000 invii: da quasi 1.000 $ a circa 10 €"), ("1", "sola fonte dei dati", "dal primo contatto alla cliente"), ("5", "abbonamenti eliminati", "e nessun dato da copiare a mano")],
                 "replaced_k": "Oggi in un unico posto", "replaced": ["CRM vendite", "Email marketing", "Automazioni", "Prenotazioni", "Pagamenti", "Area clienti"],
                 "src": "Spesa software comunicata da Tartufoli Group (settembre 2026); tempi stimati sul lavoro operativo prima e dopo la migrazione.",
                 "cta": ("Quanto stai pagando, in soldi e in ore, per i tuoi software? In 30 minuti di call te lo diciamo.", "Prenota la call"),
             }},
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
    "hint_demo": "Interactive demo",
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
        "maisenzagioie3d": {"name": "3D configurator", "client": "Concept for Maisenzagioie", "type": "3D configurator and augmented reality", "year": "2026",
                            "lead": "The necklace is designed and seen from every angle, before it's even knotted.",
                            "text": "Every choice, from the model to the thread colour and the stone, rebuilds the necklace in 3D in real time: no photo shoot for every combination, the model is generated by code. On a phone it can be placed on the table in augmented reality, at real size, and every design gets its own shareable link.",
                            "points": ["Necklace generated in 3D with every choice", "Detail view of stones, beads and weave", "Augmented reality try-on from the phone, no app", "Shareable link for every combination"],
                            "note": "Interactive concept: try changing the thread and the stone."},
        "hubdemo": {"name": "Company hub", "client": "Demo · online nutrition coaching", "type": "Hub for every internal platform", "year": "2026",
                    "lead": "Every company platform in one place, with the status of each one always in view.",
                    "text": "Sales CRM, coach app, client app, email marketing, content, hiring: every internal platform has its own card, with address, access type and purpose. At the top, the status of every service, checked automatically; below, leadership tools and public pages.",
                    "points": ["Internal platforms, leadership and public pages in one view", "Status and response time of every service", "Clear access for every tool", "The sales CRM opens straight from the hub"],
                    "note": "Demo with sample data (in Italian): open the Sales CRM from the first card."},
        "crmdemo": {"name": "Sales CRM", "client": "Demo · online nutrition coaching", "type": "Custom CRM for sales teams", "year": "2026",
                    "lead": "A CRM built around an online coaching company's sales process, from funnel to contract.",
                    "text": "The same model we brought to production for an online fitness company: a pipeline with the real stages (cold call, application, discovery, demo, deposit), a profile for every lead with AI classification and briefing, cash collected against target with projection and traffic light, overdue payments, leaderboard and commissions calculated on cash collected.",
                    "points": ["Cash, projection and trajectory to target", "Kanban and list pipeline, with a required reason for lost deals", "Lead profile with AI classification and briefing", "Overdue payments, leaderboard and tiered commissions"],
                    "note": "Demo with sample data (in Italian): open Lead and move a contact to \"Chiusa\", cash, leaderboard and commissions update on their own."},
        "kasinolatino": {"name": "Kasino Latino", "client": "Kasino Latino A.S.D.", "type": "Website for a dance school", "year": "2026",
                         "lead": "The new website for a salsa and bachata school with three locations in central Italy.",
                         "text": "Schedules, locations and classes are the heart of the site: they filter by day, always show the next available class and lead straight to booking a free trial, WhatsApp included. For the school, updating the season means editing a single list: tables, filters and messages update themselves.",
                         "points": ["Schedules filtered by location and day", "Free trial booking, WhatsApp included", "Instructors, events and gallery", "Fast on mobile, where almost every visit comes from"],
                         "note": "Browsable website preview."},
    },
    "home_h": "Projects", "home_p": "A selection of recent projects, ready to explore live.", "home_a": "All projects",
    "partners_k": "Partners", "partners_h": "Partners, <em>not just clients</em>.",
    "partners_p": "We work alongside companies that have chosen technology and artificial intelligence as a lever for growth. We don't deliver a project and disappear: together, day after day, we build the systems their business runs on.",
    "partners_cta": ("Want to grow with us?", "Become a partner"),
    "case": {"k": "Case study · Asia Baldoni Fitness × Tartufoli Group", "h": "From 54 tools to <em>one platform</em>.",
             "p": "For a seven-figure online fitness company we cut software costs by about 83% and made operational work up to 40 times faster.",
             "kpis": [("−83%", "software costs", "from about 60,000 to about 10,000 a year"), ("40×", "faster", "work that used to be done by hand"),
                      ("−99%", "email costs", "100,000 sends: from almost $1,000 to about €10"), ("~20", "people every day", "sales, coaching, marketing and leadership")],
             "before_k": "Before", "before": ["54 tools, often two or three for the same job", "Hours lost copying data between tools", "No overall view of the business"],
             "after_k": "Today", "after": ["One platform built around how they work", "Operational work takes a fraction of the time", "Every lead, call and payment in one view"],
             "more": "Read how we got there",
             "full": {
                 "k": "Case study", "h": "83% lower software costs. <em>A team 40 times faster.</em>",
                 "lead": "Asia Baldoni Fitness is a seven-figure online fitness company, with around twenty people across sales, coaching, marketing and operations. It had grown fast, and to keep up it had come to rely on 54 different tools. Together with Tartufoli Group we replaced them with a single platform, built around the way they work.",
                 "facts": [("Company", "Online fitness, seven-figure revenue"), ("Used by", "Around 20 people, every day"), ("Timeline", "Under 6 months, April to September 2026"), ("Role", "Technology partner, alongside Tartufoli Group")],
                 "ch": [
                     ("The problem: growth kept getting more expensive", ["Every new need brought a new subscription. One CRM for sales, another tool for email, one for landing pages, one for calendars, and yet more tools just to make them talk to each other. By mid-2026 software spend had reached 6.3% of revenue, more than twice the target.",
                                                                          "Cost was only the visible part. The hidden part was time: every lead copied from one system to another, every automation built by hand, every hiccup landing on one person's desk. And with data scattered across dozens of places, nobody could really see how the business was doing."]),
                     ("Why it worked: the map first, then the code", ["We didn't start from technology, but from the process. We mapped every flow one by one: where each lead comes from, which emails it receives and when, what happens at each stage, who does what. That map became the exact specification to rebuild.",
                                                                      "That's why the platform isn't generic software bent into shape: it follows the real sales stages, the real team roles and the real commission rules. People who use it find their own work, just without the obstacles."]),
                     ("How long it took: under six months", ["In April, the analysis of all 54 tools. By July the new sales CRM was used by the whole team. In August, the complete email map; in September, email on their own infrastructure. Every month, one more piece in place and one less subscription."]),
                     ("How much effort for the team: the bare minimum", ["Each new system ran alongside the old one until it worked on its own, and only then was the old one switched off. The team kept working as usual, and issues were fixed day by day.",
                                                                    "Today the sales team sees in every profile which emails a lead opened and which videos they watched. Leadership sees revenue, trajectory and team performance in real time. A segment or a new automation, which used to take hours, now takes minutes."]),
                 ],
                 "steps_k": "Milestones", "steps": [("April 2026", "Every tool and every cost analysed, one by one"), ("July 2026", "The sales team works on a CRM built around its process"), ("August 2026", "Every email and automation mapped and rebuilt"), ("September 2026", "Email marketing in-house, with sending costs close to zero")],
                 "res_k": "Results", "res": [("−83%", "software costs", "From about 60,000 to about 10,000 a year: over 50,000 reinvested in growth, every year."), ("40×", "faster", "Operational work that used to be done by hand, jumping from one tool to another.")],
                 "res2": [("−99%", "email costs", "100,000 sends: from almost $1,000 to about €10"), ("1", "single source of data", "from first contact to client"), ("5", "subscriptions removed", "and no data to copy by hand")],
                 "replaced_k": "Now in one place", "replaced": ["Sales CRM", "Email marketing", "Automations", "Bookings", "Payments", "Client area"],
                 "src": "Software spend provided by Tartufoli Group (September 2026); time estimated on operational work before and after the migration.",
                 "cta": ("How much are your tools costing you, in money and in hours? We'll tell you in a 30-minute call.", "Book the call"),
             }},
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


VERSION = hashlib.md5(b"".join((ROOT / f).read_bytes() for f in ["styles.css", "alt-overrides.css", "site.js", "mission.js", "agent.js", "audit.js", "audit-data.js", "security-check.js", "security-page.js"])).hexdigest()[:8]
# impronta di tutto il sito (contenuti compresi): se online è diversa, la pagina in cache si ricarica da sola
BUILD = hashlib.md5(b"".join((ROOT / f).read_bytes() for f in ["build.py", "styles.css", "site.js", "mission.js", "agent.js", "audit.js", "audit-data.js", "security-check.js", "security-page.js"])).hexdigest()[:10]
SLUG = {
    "it": {"home": "index.html", "work": "lavori.html", "services": "servizi.html", "security": "sicurezza.html", "check": "sicurezza-check.html", "solutions": "soluzioni.html", "mission": "missione.html", "studio": "lab.html", "contact": "contatti.html", "audit": "audit.html"},
    "en": {"home": "index.html", "work": "work.html", "services": "services.html", "security": "security.html", "check": "security-check.html", "solutions": "solutions.html", "mission": "mission.html", "studio": "lab.html", "contact": "contact.html", "audit": "audit.html"},
}
NAV = ["work", "services", "security", "solutions", "studio", "mission"]

T = {
"it": {
    "nav": {"work": "Progetti", "services": "Servizi", "security": "Sicurezza", "solutions": "Soluzioni", "mission": "Missione", "studio": "Chi siamo", "contact": "Contattaci"},
    "nav_d": {"work": "I lavori fatti, da provare dal vivo", "services": "Cosa possiamo costruire per te", "security": "Siti, app e agenti AI al sicuro", "solutions": "Esempi per il tuo settore", "mission": "Il nostro impegno per il mare", "studio": "Il metodo e chi c'è dietro", "contact": "Raccontaci il tuo progetto"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot": "© 2026 Reef 7 Lab · Sviluppo software e intelligenza artificiale",
    "cta_k": "Nuovo progetto", "cta_h": "Costruiamo il tuo <em>reef</em>.",
    "founder": {"k": "Chi c'è dietro Reef 7 Lab", "h": "Ti seguo io, dall'inizio alla fine.",
                "p": "Sono Alessandro, fondatore di Reef 7 Lab. Affidare a qualcuno i processi della tua azienda è una decisione importante, e la tratto come tale. Prima studio come lavori. Poi ti dico con chiarezza cosa conviene fare, quanto costa e in quanto tempo. Nessuna sorpresa a metà progetto, e dopo la consegna resto il tuo riferimento.",
                "points": [["Asia Baldoni Fitness", "Partner tecnologico: gran parte di 54 software sostituiti da una piattaforma interna"], ["Tupitago", "Co-fondatore di una startup di sviluppo vincitrice di un bando della Regione Marche"], ["E-commerce", "Software e marketing per Veneziana, Breeez e Full Peak"], ["5 lingue", "Formazione tra Italia, Germania e Spagna"]],
                "cta": "Prenota la call gratuita", "a": "La mia storia",
                "risk": "Una call di 30 minuti, gratuita, per capire da dove conviene partire nella tua azienda. Ti rispondo entro un giorno lavorativo.",
                "contact_h": "Ti rispondo io", "contact_p": "Leggo ogni richiesta personalmente e ti rispondo entro un giorno lavorativo, con le prime idee."},
    "services": [
        ("31", "Guadagnare di più", "Sistema di vendita, dal contatto all'incasso", "Ogni contatto seguito fino al pagamento, senza che nessuno si perda per strada.",
         "È il sistema con cui abbiamo visto crescere un'azienda a sette cifre: ogni contatto viene assegnato in pochi minuti alla persona giusta, passa da chiamata, qualifica e chiusura con ruoli chiari, chi non chiude viene ripreso al momento giusto e ogni incasso torna al venditore e alla campagna che l'hanno generato. Lo costruiamo sul tuo processo, con i tuoi numeri.",
         ["Assegnazione automatica in pochi minuti, con regole e pesi", "Ruoli chiari: primo contatto, qualifica, chiusura", "Briefing AI prima di ogni call", "Contenuti da mandare scelti in base all'obiezione", "Obiettivo, traiettoria e diagnosi se si è sotto"]),
        ("28", "Guadagnare di più", "Recupero contatti e trattative perse", "I contatti che hai già pagato tornano a diventare clienti.",
         "Ogni azienda ha un cassetto pieno di contatti mai richiamati e trattative chiuse con un \"ci penso\". Costruiamo regole che li ripescano da sole: un contatto fermo da mezz'ora viene assegnato, una call non chiusa torna dopo qualche settimana a un'altra persona, con contenuti scelti sull'obiezione emersa.",
         ["Contatti fermi assegnati in automatico dopo pochi minuti", "Call non chiuse riprese al momento giusto", "Riassegnazione a un'altra persona se nessuno si muove", "Priorità di contatto sempre chiare", "Tutto tracciato, senza doppioni"]),
        ("29", "Guadagnare di più", "Upsell, rinnovi e clienti che tornano", "Il cliente che hai già è il più facile da far crescere.",
         "La vendita più semplice è al cliente soddisfatto, al momento giusto. Usiamo i dati che hai già, come acquisti, utilizzo e risultati, per proporre upgrade, rinnovi e riacquisti quando il cliente è pronto: un promemoria al venditore a metà percorso, una sequenza al cliente fermo, un'offerta a chi sta ottenendo risultati.",
         ["Proposte di upgrade a metà percorso, calcolate da sole", "Rinnovi e riacquisti ricordati in automatico", "Segnali d'uso e di risultato nella scheda cliente", "Sequenze per i clienti fermi o in uscita", "Fatturato per cliente nel tempo sempre in vista"]),
        ("30", "Guadagnare di più", "Obiettivi, provvigioni e classifica del team", "Un team commerciale che vede ogni giorno dove sta andando, e perché.",
         "Quando le provvigioni si calcolano a mano a fine mese, nessuno sa davvero quanto sta guadagnando finché è tardi. Colleghiamo incassi e CRM: provvigioni a scaglioni sull'incassato, quote per chi ha fissato l'appuntamento, bonus di team, classifica settimanale e mensile e una traiettoria che dice in tempo reale se l'obiettivo è alla portata.",
         ["Provvigioni a scaglioni calcolate sull'incassato", "Quote per chi fissa e per chi chiude", "Classifica settimanale e mensile", "Traiettoria e proiezione sull'obiettivo", "Bonus di team con soglie chiare"]),
        ("18", "Guadagnare di più", "Recensioni e passaparola", "I clienti soddisfatti diventano il tuo miglior canale di vendita.",
         "La maggior parte dei clienti contenti non lascia una recensione solo perché nessuno gliela chiede al momento giusto. Automatizziamo la richiesta dopo l'acquisto o la visita, ascoltiamo in privato chi non è soddisfatto prima che scriva in pubblico e premiamo chi porta nuovi clienti.",
         ["Richieste di recensione al momento giusto, su Google e sul sito", "Chi non è soddisfatto viene ascoltato in privato", "Programma di passaparola con premi tracciati", "Recensioni migliori mostrate sul sito e nelle pagine prodotto", "Voto medio e nuove recensioni sotto controllo"]),
        ("23", "Guadagnare di più", "Tracciamento e attribuzione", "Sai da dove arriva ogni cliente, fino all'incasso.",
         "Senza tracciamento le campagne ottimizzano sulle visite, non sulle vendite. Colleghiamo pagine, moduli, CRM e piattaforme pubblicitarie: ogni contatto porta con sé la sua fonte, ogni vendita torna alla campagna che l'ha generata e Meta e Google ricevono gli eventi che contano davvero.",
         ["UTM e fonte salvati su ogni contatto", "Eventi di conversione verso Meta e Google", "Dalla campagna all'incasso, non solo al clic", "Moduli e sorgenti sempre distinguibili", "Report per canale, campagna e venditore"]),
        ("11", "Intelligenza artificiale", "Agenti AI per le vendite", "Ogni contatto riceve una risposta in pochi secondi, a qualsiasi ora.",
         "Un lead che aspetta un giorno è un lead che si raffredda. L'agente risponde su sito, WhatsApp ed email, fa le domande giuste per capire chi è pronto a comprare, fissa la call nell'agenda del commerciale e aggiorna il CRM. I casi delicati passano sempre a una persona.",
         ["Risposta immediata su sito, WhatsApp ed email", "Lead qualificati con le tue domande", "Call fissate nell'agenda del commerciale giusto", "CRM aggiornato senza inserimenti a mano", "Passaggio a una persona quando serve"]),
        ("06", "Intelligenza artificiale", "Automazioni, con e senza AI", "Le ore spese in lavoro ripetitivo tornano al tuo team.",
         "Rispondere alle stesse email, copiare dati, compilare report: è lavoro che non fa crescere nessuno. Lo automatizziamo: con regole e integrazioni dove basta un flusso preciso, con l'intelligenza artificiale dove serve capire testi e decidere, sempre con un controllo umano nei passaggi delicati. E misuriamo quanto tempo ti restituisce.",
         ["Analisi delle attività che costano più tempo", "Flussi automatici tra i tuoi software, senza AI", "Agenti AI per email, documenti e richieste", "Contatti qualificati e smistati da soli", "Controllo umano nei passaggi delicati", "Tempo risparmiato misurato"]),
        ("12", "Intelligenza artificiale", "Assistenti vocali AI", "Un assistente al telefono che risponde, prenota e richiama.",
         "Le chiamate perse sono clienti persi. L'assistente vocale risponde con una voce naturale, in più lingue, prende appuntamenti, conferma e ricorda le prenotazioni e richiama chi non ha risposto. Ogni conversazione arriva al team già trascritta e riassunta.",
         ["Risposte al telefono a qualsiasi ora", "Prenotazioni, conferme e promemoria", "Richiami dei contatti persi", "Più lingue, voce naturale", "Trascrizione e riassunto di ogni chiamata"]),
        ("07", "Intelligenza artificiale", "Company brain", "Tutto quello che sa la tua azienda, a una domanda di distanza.",
         "Procedure, documenti, risposte già date ai clienti: il sapere della tua azienda è sparso tra cartelle, chat e persone. Lo raccogliamo in un assistente che risponde al team in pochi secondi e indica sempre da dove viene l'informazione.",
         ["Raccolta e organizzazione dei documenti", "Risposte con la fonte, sempre verificabili", "Ognuno vede solo ciò che gli compete", "Contenuti aggiornati nel tempo", "Dati riservati e protetti"]),
        ("13", "Intelligenza artificiale", "Analisi delle chiamate di vendita", "Ogni call diventa una lezione per tutto il team.",
         "Le call dei commerciali vengono trascritte e analizzate: quanto si è seguito lo script, quali obiezioni sono emerse, dove si è persa la trattativa. Chi guida il team vede subito su cosa lavorare, e ogni commerciale riceve suggerimenti concreti dopo ogni chiamata.",
         ["Trascrizione automatica delle call", "Punteggio rispetto al tuo script di vendita", "Obiezioni ricorrenti in evidenza", "Suggerimenti per ogni commerciale", "Report per chi guida il team"]),
        ("26", "Intelligenza artificiale", "Formazione AI per il team", "Il tuo team usa l'intelligenza artificiale sul lavoro vero, da subito.",
         "Gli strumenti di intelligenza artificiale rendono davvero solo quando conoscono l'azienda. Li impostiamo con il contesto della tua azienda, i tuoi processi e il tuo tono di voce, e formiamo il team su casi reali: email, analisi, documenti, automazioni.",
         ["Assistenti AI impostati con il contesto aziendale", "Formazione pratica sui processi di ogni reparto", "Libreria condivisa di istruzioni e modelli", "Regole chiare su dati e privacy", "Accompagnamento nelle prime settimane"]),
        ("36", "Sicurezza", "Messa in sicurezza di siti e app esistenti", "Costruiti per il web di ieri. Esposti agli attacchi di oggi.",
         "Quando il tuo sito o il tuo gestionale sono nati, attaccarli richiedeva tempo e una persona competente. Oggi lo fa un programma, senza sosta e quasi a costo zero: prova password rubate altrove, cerca componenti con falle note, interroga ogni modulo e ogni API. Analizziamo quello che hai, ti mostriamo da dove si entra e chiudiamo ogni varco in ordine di gravità. Senza rifare tutto, senza fermare il lavoro.",
         ["Verifica di siti, app, e-commerce e gestionali, anche datati", "Componenti, plugin e librerie vulnerabili aggiornati o isolati", "Difese contro bot, furto di account e accessi in massa", "Moduli e API protetti da abusi e raccolta automatica di dati", "Piano per gravità: subito, nelle prossime settimane, strutturale"]),
        ("37", "Sicurezza", "Accessi, password e persone", "Il modo più facile per entrare resta una porta lasciata aperta.",
         "Un pannello di prova protetto dalla password 123456 ha esposto i dati legati a milioni di candidature di lavoro. Non serviva un genio, bastava un accesso dimenticato. Ex collaboratori ancora attivi, password condivise in chat, chiavi mai cambiate, integrazioni autorizzate anni fa: facciamo l'inventario di chi entra dove, chiudiamo ciò che non serve e rendiamo la sicurezza semplice per tutto il team.",
         ["Inventario di account, chiavi di servizio e integrazioni autorizzate", "Accessi revocati a chi non ne ha più bisogno", "Doppio fattore e gestore di password per tutto il team", "Permessi per ruolo: ognuno vede solo ciò che gli serve", "Formazione contro phishing e truffe, anche vocali e scritte con l'AI"]),
        ("38", "Sicurezza", "Email e truffe a tuo nome", "Le truffe migliori arrivano da un indirizzo che sembra il tuo.",
         "Una fattura falsa inviata ai tuoi clienti dal tuo dominio, un fornitore che chiede di cambiare IBAN, un messaggio vocale con la voce del titolare: oggi le truffe sono scritte, e perfino parlate, con l'AI, e sembrano vere. Proteggiamo il tuo dominio perché nessuno possa scrivere a nome tuo, e prepariamo il team a riconoscere i tentativi prima che costino.",
         ["SPF, DKIM e DMARC impostati fino al blocco delle email false", "Avvisi quando qualcuno prova a usare il tuo dominio", "Doppia conferma per pagamenti e cambi di IBAN", "Prove di phishing realistiche per il team", "Una procedura chiara su cosa fare davanti a un'email strana"]),
        ("32", "Sicurezza", "Verifica di siti e app costruiti con l'AI", "Online in un weekend. Aperti a chiunque per mesi?",
         "Quando alcuni ricercatori hanno analizzato 1.645 app pubblicate con un noto generatore basato sull'AI, 170 lasciavano leggere a chiunque elenchi di utenti, pagamenti o chiavi. Non per un attacco raffinato: per regole del database mai scritte. Gli strumenti AI costruiscono in fretta, ma non pensano a chi proverà a entrare. Noi sì: cerchiamo gli errori tipici uno per uno, li correggiamo e ti restituiamo un progetto che puoi far crescere senza pensieri.",
         ["Chiavi e segreti cercati nel codice e in tutta la cronologia del repository", "Regole del database verificate tabella per tabella", "Ruoli e permessi provati entrando con utenti diversi", "Pagine riservate e API provate senza login", "Report chiaro, con le correzioni già applicate"]),
        ("33", "Sicurezza", "Sicurezza di chatbot e agenti AI", "Più un agente può fare, più costa un suo errore.",
         "Una sola email preparata ad arte bastava a far consegnare dati aziendali a un assistente AI diffusissimo, senza un clic. Un agente di sviluppo ha cancellato un database di produzione durante un blocco delle modifiche. Un'integrazione di chatbot compromessa ha aperto i CRM di centinaia di aziende. Mettiamo il tuo agente alla prova con gli stessi attacchi, gli togliamo i permessi che non gli servono e mettiamo una persona davanti a ogni azione che conta.",
         ["Prove contro istruzioni nascoste in email, documenti e pagine web", "Permessi minimi: l'agente raggiunge solo ciò che gli serve", "Conferma umana prima delle azioni che spostano dati o denaro", "Ambienti separati: nessun esperimento sui dati veri", "Registro completo di conversazioni e azioni"]),
        ("34", "Sicurezza", "Privacy e dati quando usi l'AI", "Ogni prompt è un dato che esce dall'azienda.",
         "Contratti incollati in una chat, elenchi clienti caricati per un'analisi, email riassunte da un assistente: ogni volta i dati lasciano l'azienda, spesso senza che nessuno sappia dove finiscono e per quanto restano. Ricostruiamo questi flussi, togliamo i dati personali dove non servono e scegliamo servizi e impostazioni compatibili con il GDPR, insieme al tuo consulente legale. Così il team usa l'AI ogni giorno senza esporre i clienti.",
         ["Mappa dei dati che passano dai servizi AI", "Dati personali rimossi o mascherati prima dell'invio", "Fornitori, server e contratti compatibili con il GDPR", "Informativa e registro dei trattamenti aggiornati", "Regole chiare per il team sull'uso quotidiano dell'AI"]),
        ("35", "Sicurezza", "Sorveglianza e continuità di servizio", "Se qualcosa si rompe, lo sai prima dei tuoi clienti.",
         "Il backup che non si ripristina, l'aggiornamento rimandato da mesi, il sito che cade il venerdì sera: sono i problemi che costano di più e che nessuno vede finché non è tardi. Teniamo d'occhio siti, app e gestionali ogni giorno, proviamo davvero i ripristini e applichiamo gli aggiornamenti con un calendario preciso. Ogni mese ricevi un rapporto chiaro, scritto per chi decide e non per chi programma.",
         ["Monitoraggio continuo, con avviso immediato", "Backup automatici e prove di ripristino reali", "Difese contro bot e attacchi che bloccano il sito", "Aggiornamenti di sicurezza a calendario", "Rapporto mensile leggibile anche da chi non è tecnico"]),
        ("03", "Vendite e incassi", "CRM su misura", "Lead, trattative e provvigioni in un unico strumento, costruito sul tuo modo di vendere.",
         "Un CRM generico costringe il team commerciale ad adattarsi. Costruiamo CRM su misura: ogni lead arriva già assegnato, le trattative avanzano per fasi, pagamenti e provvigioni si calcolano da soli e la direzione vede risultati e classifica in tempo reale.",
         ["Pipeline e fasi definite sul tuo processo", "Assegnazione automatica dei lead", "Pagamenti e provvigioni calcolati in automatico", "Classifica e KPI del team, anche su uno schermo in ufficio", "Collegato a sito, prenotazioni ed email"]),
        ("04", "Vendite e incassi", "Prenotazioni e agenda commerciale", "Un sistema di prenotazione tuo, che assegna ogni appuntamento alla persona giusta.",
         "I potenziali clienti prenotano da soli una call. Il sistema distribuisce gli appuntamenti tra i commerciali, riporta ogni contatto al suo referente e invia i promemoria, così diminuiscono le assenze.",
         ["Pagina di prenotazione con il tuo brand", "Distribuzione automatica tra i commerciali", "Ogni contatto torna sempre al suo referente", "Promemoria automatici", "Appuntamenti registrati direttamente nel CRM"]),
        ("05", "Vendite e incassi", "Email marketing e automazioni", "Sequenze email che lavorano per te, con la consegna sotto controllo.",
         "Dal benvenuto al follow-up dopo una call, le email partono al momento giusto in base a ciò che fa ogni contatto. Curiamo anche la parte tecnica che decide se un'email arriva in casella o finisce nello spam.",
         ["Sequenze automatiche per ogni fase del cliente", "Segmentazione in base al comportamento", "Riscaldamento dei domini e gestione delle liste", "Statistiche di apertura e risposta", "Un'alternativa alle piattaforme a canone"]),
        ("22", "Vendite e incassi", "Email che arrivano davvero", "Se le email finiscono nello spam, il copy non c'entra.",
         "Spesso il problema non è cosa scrivi ma se arriva: domini non autenticati, liste mai pulite, invii a tutto il database. Controlliamo DNS, reputazione, liste e automazioni e misuriamo le aperture vere, non quelle gonfiate dai filtri automatici. In un audit reale il 68% delle aperture dichiarate non era mai avvenuto.",
         ["Autenticazione del dominio: SPF, DKIM e DMARC", "Aperture reali separate da quelle automatiche", "Pulizia delle liste e regole di esclusione", "Automazioni senza invii doppi né rientri", "Riscaldamento graduale dei nuovi domini"]),
        ("24", "Vendite e incassi", "Incassi, rate e insoluti", "Ogni rata incassata in tempo, senza rincorrere nessuno.",
         "Pagamenti a rate, contratti e solleciti gestiti a mano sono soldi che arrivano in ritardo, o non arrivano. Colleghiamo pagamenti, contratti e CRM: promemoria prima della scadenza, sollecito il giorno stesso, riconciliazione automatica con Stripe e ogni incasso attribuito alla persona giusta.",
         ["Contratti e piani di rata registrati una volta sola", "Promemoria automatici prima e dopo la scadenza", "Riconciliazione automatica con Stripe", "Insoluti sempre in vista", "Incasso attribuito al venditore giusto"]),
        ("10", "Meno software, meno costi", "Dagli abbonamenti a strumenti tuoi", "Sostituiamo i software a canone con strumenti tuoi, integrati tra loro.",
         "CRM, email, prenotazioni, automazioni: molte aziende pagano ogni mese più abbonamenti che fanno cose simili e non si parlano. Analizziamo i costi e sostituiamo quelli che conviene con strumenti tuoi, più semplici e collegati.",
         ["Analisi dei software in uso e dei costi", "Piano di migrazione senza interruzioni", "Dati trasferiti e verificati", "Strumenti integrati tra loro", "Meno costi ricorrenti nel tempo"]),
        ("20", "Meno software, meno costi", "Radiografia dei sistemi", "Scopri come si parlano davvero i tuoi software, e quanto ti costano.",
         "Apriamo uno per uno gli strumenti che usate e misuriamo cosa succede davvero: quali collegamenti funzionano, quali dati si duplicano, quali automazioni girano a vuoto e dove ci sono chiavi o accessi esposti. In un caso reale un solo contatto attraversava cinque sistemi e sei destinazioni, e nessuno sapeva quale dei cinque comandasse.",
         ["Mappa di tutti gli strumenti e dei collegamenti reali", "Duplicazioni, errori e automazioni ferme, misurati", "Costi software per categoria e peso sui ricavi", "Sicurezza: chiavi, accessi e webhook esposti", "Piano in ordine di impatto: subito, questa settimana, strutturale"]),
        ("21", "Meno software, meno costi", "Email marketing di proprietà", "Le stesse email di sempre, a una frazione del costo.",
         "Le piattaforme di email marketing fanno pagare in base ai contatti, anche quando la maggior parte non apre nulla. Costruiamo un sistema di invio tuo sulla stessa infrastruttura che usano le grandi piattaforme: in un caso reale 100.000 invii sono passati da quasi 1.000 dollari a circa 10 euro, con aperture e clic visibili nella scheda di ogni contatto.",
         ["Invio su infrastruttura professionale, pagato a email", "Automazioni e segmenti come prima, collegati al CRM", "Aperture e clic nella scheda di ogni contatto", "Passaggio graduale, senza perdere la reputazione del dominio", "Segmenti creati chiedendoli in linguaggio naturale"]),
        ("09", "Meno software, meno costi", "Hub aziendale e integrazioni", "Tutti gli strumenti dell'azienda collegati e raggiungibili da un unico punto.",
         "Un portale interno da cui ogni persona accede agli strumenti che le servono, con un unico database alla base. Colleghiamo i software tra loro tramite API e webhook, così i dati si muovono da soli.",
         ["Portale interno con accessi per ruolo", "Un unico database per tutte le applicazioni", "Integrazioni via API e webhook", "Organigramma e procedure sempre a portata di mano", "Sicurezza e backup inclusi"]),
        ("08", "Gestione", "Dashboard e controllo di gestione", "Vendite, cassa e margini in un'unica vista, sempre aggiornata.",
         "Se per capire come sta andando l'azienda servono tre persone e un Excel, decidi sempre in ritardo. Colleghiamo le tue fonti in dashboard per la direzione: indicatori commerciali, flussi di cassa, marginalità e bilancio, aggiornati da soli.",
         ["Indicatori commerciali e di marketing", "Flussi di cassa e marginalità", "Viste dedicate per direzione e team", "Aggiornamento automatico dalle tue fonti", "Accessi protetti per ruolo"]),
        ("19", "Gestione", "Ordini, magazzino e fornitori", "Ordini, giacenze e consegne in un'unica vista, su ogni canale.",
         "Quando gli ordini arrivano da negozio, marketplace, telefono e agenti, le giacenze non tornano mai e qualcuno passa le giornate a ricopiare. Colleghiamo canali, magazzino, corrieri e fornitori: ogni ordine segue il suo percorso da solo e sai sempre cosa c'è, cosa manca e cosa sta arrivando.",
         ["Ordini da tutti i canali in un unico pannello", "Giacenze sincronizzate, con avvisi di sottoscorta", "Etichette, corrieri e tracking automatici", "Riordini ai fornitori preparati in automatico", "Resi gestiti dall'inizio al rimborso"]),
        ("25", "Gestione", "Organigramma, onboarding e supporto interno", "Ogni persona sa a chi chiedere, e i problemi si risolvono prima.",
         "Quando l'azienda cresce, le domande interne finiscono sempre sulle stesse persone. Costruiamo un organigramma consultabile e ricercabile, percorsi di onboarding per chi entra e un canale di segnalazione con un modello chiaro, che una routine riepiloga ogni giorno.",
         ["Organigramma ricercabile per persona, ruolo e competenza", "Onboarding con guide e video per ogni ruolo", "Segnalazioni con un modello unico e priorità", "Riepilogo automatico ogni giorno dei problemi aperti", "Documentazione degli strumenti sempre aggiornata"]),
        ("01", "Digitale", "Siti web e landing page", "Siti e pagine di vendita che trasformano le visite in contatti.",
         "Il sito è spesso il primo contatto con un cliente. Progettiamo siti e landing page che spiegano subito il valore, accompagnano verso il contatto e si aggiornano senza dover chiamare nessuno.",
         ["Struttura e testi pensati per convertire", "Design su misura, nessun template", "Landing page e funnel per le campagne", "Ottimizzazione per Google e per il telefono", "Ogni richiesta tracciata"]),
        ("02", "Digitale", "Applicazioni su misura", "Il software si adatta a come lavori. Non il contrario.",
         "Se il tuo team passa più tempo ad aggirare un gestionale che a usarlo, il problema non è il team. Progettiamo gestionali, portali clienti e strumenti interni attorno ai processi reali della tua azienda.",
         ["Analisi dei processi e prototipo cliccabile", "Applicazioni web e desktop", "Accessi e permessi per ruolo", "Integrazione con gli strumenti che usi già", "Nuove funzioni man mano che cresci"]),
        ("27", "Digitale", "App clienti e percorsi online", "Corsi, percorsi e clienti in un'app tua, non in affitto.",
         "Videocorsi su una piattaforma, percorsi su un'altra, community su una terza: il cliente si perde e tu paghi tre canoni. Costruiamo un'app con il tuo marchio dove il cliente segue il percorso, guarda le lezioni e parla con il suo coach, collegata a CRM e pagamenti, con un'area dedicata per i coach.",
         ["Percorsi, lezioni e progressi di ogni cliente", "Area coach per seguire ogni cliente", "Accesso attivato dal pagamento", "Collegata a CRM, email e pagamenti", "Migrazione dalle piattaforme attuali senza perdere clienti"]),
        ("17", "Digitale", "Area clienti e portali riservati", "I tuoi clienti trovano tutto da soli, senza scriverti per chiedere.",
         "Documenti da inviare, stato dei lavori, scadenze, pagamenti: ogni domanda di un cliente è una mail o una telefonata in più. Costruiamo un'area riservata con il tuo marchio dove ogni cliente carica i documenti, segue l'avanzamento, scarica fatture e riceve gli avvisi al momento giusto.",
         ["Accesso riservato per ogni cliente, con il tuo marchio", "Caricamento documenti con promemoria automatici", "Stato dei lavori e scadenze sempre visibili", "Fatture, contratti e firme online", "Collegata al tuo CRM e al gestionale"]),
        ("14", "Digitale", "Configuratori 3D e realtà aumentata", "Il cliente vede il prodotto prima di comprarlo, esattamente come lo vuole.",
         "Un prodotto che si può ruotare, personalizzare e provare nel proprio spazio vende più di una foto. Costruiamo configuratori 3D e anteprime in realtà aumentata che funzionano direttamente dal browser, senza app da scaricare, collegati al tuo catalogo e ai tuoi prezzi.",
         ["Modelli 3D da ruotare e personalizzare", "Prova in realtà aumentata dal telefono", "Prezzo aggiornato a ogni scelta", "Nessuna app da scaricare", "Collegati a catalogo e ordini"]),
        ("15", "Mercati esteri", "Siti ed e-commerce multilingue", "Parla ai clienti di ogni paese nella loro lingua, davvero.",
         "Tradurre un sito non basta: ogni mercato ha le sue parole, i suoi dubbi e le sue abitudini d'acquisto. Adattiamo testi, pagine e comunicazioni in italiano, inglese, spagnolo, tedesco e cinese, con un unico pannello per gestire tutte le versioni.",
         ["Contenuti adattati a ogni mercato, non solo tradotti", "Italiano, inglese, spagnolo, tedesco e cinese", "Un unico pannello per tutte le lingue", "Email e assistenza nella lingua del cliente", "Visibilità sui motori di ricerca di ogni paese"]),
        ("16", "Mercati esteri", "Ponte con la Cina", "Fornitori, ordini e clienti cinesi, gestiti come se fossero dietro l'angolo, ovunque sia la tua azienda.",
         "Lavorare con la Cina significa lingue, fusi orari, piattaforme e software diversi, che tu sia in Italia, in Europa o altrove. Colleghiamo i sistemi dei fornitori cinesi ai tuoi, così ordini, spedizioni e controlli di qualità si seguono da un'unica vista; prepariamo sito, contenuti e assistenza per i clienti cinesi; curiamo la comunicazione in cinese con l'aiuto dell'intelligenza artificiale e una revisione umana.",
         ["Integrazione tra i software dei fornitori cinesi e i tuoi", "Ordini, spedizioni e controlli qualità in un'unica vista", "Comunicazione in cinese con fornitori, partner e clienti", "Sito e assistenza pensati per i clienti cinesi", "Per aziende di ogni paese, con controllo umano nei passaggi importanti"]),
    ],
    "sectors": [
        {"t": "Team commerciali", "d": "Più tempo in chiamata, meno tempo su Excel.",
         "pain": "I commerciali aggiornano fogli di calcolo invece di vendere, i contatti si perdono tra un'agenda e l'altra e le provvigioni si calcolano a mano a fine mese.",
         "build": ["Un CRM costruito sul tuo processo di vendita", "Prenotazioni distribuite automaticamente tra i commerciali", "Sequenze email che seguono ogni contatto dopo la call", "Provvigioni e classifica calcolate in automatico"],
         "out": "Un team che passa più tempo con i clienti e una direzione che vede i risultati in tempo reale.", "svc": ["31", "28", "30", "13"]},
        {"t": "E-commerce", "d": "Più vendite, senza più lavoro manuale.",
         "pain": "Ordini, campagne e assistenza vivono in strumenti diversi. Scopri a fine mese cosa ha funzionato, quando è troppo tardi per correggere.",
         "build": ["Pagine prodotto pensate per convertire", "Dashboard con vendite, spesa pubblicitaria e margine reale", "Assistenza ai clienti gestita dall'intelligenza artificiale", "App per i clienti dopo l'acquisto, integrata nel negozio"],
         "out": "Sai ogni giorno quanto guadagni davvero, e il team si concentra sulla crescita invece di rincorrere gli ordini.", "svc": ["01", "23", "19", "18"]},
        {"t": "Studi professionali", "d": "Meno burocrazia, più tempo per i clienti.",
         "pain": "Documenti da cercare, scadenze da ricordare e le stesse domande dei clienti ogni settimana: ore preziose che non puoi fatturare.",
         "build": ["Un portale riservato per i clienti", "Documenti archiviati e classificati in automatico", "Un assistente che conosce le procedure dello studio", "Promemoria automatici per scadenze e appuntamenti"],
         "out": "Più ore dedicate alla consulenza, meno errori e clienti che si sentono davvero seguiti.", "svc": ["17", "07", "12", "04"]},
        {"t": "Formazione e coaching", "d": "Un percorso digitale all'altezza di ciò che insegni.",
         "pain": "Corsi su una piattaforma, community su un'altra, vendite gestite a mano: gli studenti si perdono tra un passaggio e l'altro.",
         "build": ["Landing page e funnel per le iscrizioni", "Call di vendita prenotate e assegnate in automatico", "Email che accompagnano ogni studente dall'iscrizione al risultato", "Un assistente che risponde alle domande degli studenti"],
         "out": "Più iscrizioni, studenti più coinvolti e un'attività che cresce senza moltiplicare il lavoro.", "svc": ["31", "27", "29", "24"]},
        {"t": "Agenzie e servizi B2B", "d": "Clienti seguiti meglio, con meno passaggi a mano.",
         "pain": "Richieste via email, stato dei lavori in un foglio condiviso, report preparati a mano ogni mese per ogni cliente.",
         "build": ["Un portale clienti con stato dei lavori e documenti", "Report per i clienti generati in automatico", "Richieste smistate al referente giusto", "Una knowledge base interna per il team"],
         "out": "Clienti informati senza doverlo chiedere, e un team che lavora sui progetti invece che sulle email.", "svc": ["17", "08", "06", "07"]},
        {"t": "Aziende in crescita", "d": "Cresci senza perdere il controllo.",
         "pain": "Più clienti vogliono dire più fogli di calcolo, più abbonamenti e più errori. Gli strumenti che bastavano due anni fa oggi rallentano tutto.",
         "build": ["Un hub interno con tutti gli strumenti e un unico database", "Dashboard per la direzione su vendite, cassa e margini", "Software in abbonamento sostituiti da strumenti tuoi", "Gestionali costruiti sui tuoi processi"],
         "out": "Un'unica fonte di verità per tutta l'azienda, decisioni prese su dati certi e meno costi ricorrenti.", "svc": ["20", "10", "21", "09"]},
    ],
    "home": {
        "title": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "desc": "Reef 7 Lab sviluppa siti, applicazioni, intelligenza artificiale e dashboard su misura, collegati in un unico sistema.",
        "kicker": "Reef 7 Lab · Sviluppo software e intelligenza artificiale",
        "h1": "Il tuo business, <em>connesso</em>.",
        "sub": "Siti, applicazioni e intelligenza artificiale progettati per lavorare insieme. Meno lavoro manuale, decisioni più rapide, una crescita che si accumula nel tempo.",
        "b1": "Parliamo del tuo progetto", "b2": "Scopri i servizi",
        "eco_core": "Il tuo sistema", "eco_nodes": [("Sito", "◎"), ("CRM", "◇"), ("Email", "✉"), ("Pagamenti", "€"), ("Agenda", "◷"), ("Dashboard", "▤")],
        "eco_k": "Integrazione dei sistemi",
        "eco_h": "Un unico sistema per <em>tutta l'azienda</em>.",
        "eco_p": "Colleghiamo gli strumenti che usi già e automatizziamo i passaggi tra l'uno e l'altro. I dati entrano una volta sola e arrivano dove servono, già pronti per essere usati.",
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
        "svc_h": "Servizi", "svc_p": "Dal sito al CRM, dall'intelligenza artificiale al controllo di gestione: competenze diverse che lavorano insieme.", "svc_all": "Tutti i servizi",
        "sol_h": "Soluzioni", "sol_p": "Per ogni settore combiniamo i servizi giusti in un unico sistema. Ecco alcuni esempi.", "sol_all": "Tutte le soluzioni",
        "reef_h": "Progettati come <em>un reef</em>", "reef_p": "Il reef è tra gli ecosistemi più efficienti della Terra. I suoi cinque principi guidano ogni progetto.",
        "reef_words": ["Diversità", "Simbiosi", "Connessione", "Crescita stratificata", "Resilienza"], "reef_a": "La nostra filosofia",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Siti web, applicazioni su misura, agenti AI, assistenti vocali, company brain, dashboard e progetti con la Cina.",
        "h1": "Tutte le competenze, <em>un solo</em> sistema.",
        "sub": "Dal sito che porta clienti al gestionale che fa girare l'azienda: le combiniamo in base ai tuoi obiettivi, mai partendo da un pacchetto preconfezionato.",
    },
    "solutions": {
        "title": "Solutions · Reef 7 Lab", "desc": "Soluzioni software per e-commerce, studi professionali, formazione e aziende in crescita.",
        "h1": "Soluzioni costruite <em>sul tuo settore</em>.",
        "sub": "Ogni settore ha i suoi colli di bottiglia. Per ognuno combiniamo i servizi giusti in un sistema unico: ecco i casi che affrontiamo più spesso.",
        "lbl": ("La sfida", "Cosa costruiamo", "Il risultato", "Servizi coinvolti"),
    },
    "studio": {
        "title": "Chi siamo · Reef 7 Lab", "desc": "La filosofia del reef: come Reef 7 Lab progetta software che cresce connesso.",
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
        "seven_p": "Il 7 sono sette barriere coralline, dal Mar Rosso alla Polinesia, che vogliamo aiutare a proteggere. Ogni progetto che realizziamo ci avvicina a questo obiettivo: è il numero che ci ricorda per chi lavoriamo, oltre che per i nostri clienti.",
        "who_big": "Dietro Reef 7 Lab c'è <em>Alessandro</em>.",
        "who": ["Alessandro costruisce software che fanno crescere le aziende. Ha iniziato nel 2023 co-fondando Tupitago, una startup di sviluppo: ne ha guidato marketing, prodotto e ricerca, fino a vincere un bando della Regione Marche. Nel 2025 ha passato il testimone al socio, e Tupitago continua a crescere.",
                "Da allora ha fatto crescere tre brand e-commerce, Veneziana, Breeez e Full Peak, curando tutto quello che sta dietro una vendita: il sito, le campagne, le email, l'assistenza. Con i fornitori cinesi ha costruito i collegamenti tra i loro software e quelli italiani, e ha gestito lui stesso i rapporti in cinese.",
                "Oggi lavora al fianco di Asia Baldoni Fitness e Tartufoli Group, dove ha contribuito a sostituire gran parte dei 54 software dell'azienda con un'unica piattaforma interna, riducendo i costi software di circa l'83%.",
                "La sua formazione è internazionale: una laurea in Mediazione linguistica, un semestre all'Università di Heidelberg, la prima della Germania, e un tirocinio in un'agenzia di marketing a Tenerife. Lavora in cinque lingue, italiano, inglese, spagnolo, tedesco e cinese: i progetti con clienti, partner e fornitori all'estero non si perdono nella traduzione.",
                "Il mare, per lui, è una questione personale: per anni è stato volontario attivo di 2hands Ancona, che ripulisce spiagge e coste dai rifiuti."],
        "creds": [("Tupitago · 2023–2025", "Co-fondatore, vincitrice di un bando della Regione Marche"), ("3 brand e-commerce", "Software e marketing per Veneziana, Breeez, Full Peak"),
                  ("Heidelberg · 2024", "Università di Heidelberg, semestre con borsa di studio d'eccellenza"), ("Tenerife · 2023", "Tirocinio in un'agenzia di marketing"),
                  ("5 lingue", "Laurea in Mediazione linguistica, 2025"), ("Partner", "Asia Baldoni Fitness e Tartufoli Group")],
        "sign": ("Alessandro", "Fondatore, Reef 7 Lab"),
        "photo_alt": "Alessandro, fondatore di Reef 7 Lab",
        "more": "Leggi tutta la storia",
    },
    "audit": {
        "title": "Audit di automazione gratuito · Reef 7 Lab", "desc": "In due minuti scopri quante ore a settimana il tuo team potrebbe recuperare e cosa automatizzare per primo.",
        "k": "Audit gratuito", "h1": "Quanto tempo può <em>recuperare</em> il tuo team?",
        "sub": "Rispondi a poche domande sul lavoro che fate ancora a mano. Ricevi una stima delle ore recuperabili, le priorità e un piano in 3 passi, anche in PDF.",
        "pts": ["2 minuti", "Report personalizzato", "Gratis, senza impegno"],
        "home_k": "Audit gratuito", "home_h": "Quante ore perde ogni settimana <em>il tuo team</em>?", "home_p": "In due minuti scopri cosa conviene automatizzare per primo e quanto tempo potresti recuperare.", "home_a": "Fai l'audit", "home_k2": "2 minuti · gratis",
        "vis_k": "Esempio di report", "vis_u": "ore a settimana recuperabili", "vis": [("Copiare dati tra programmi", 8), ("Rispondere ai nuovi contatti", 4.8), ("Preparare report e numeri", 3)],
        "contact_p": "Non sai ancora da dove partire?", "contact_a": "Fai prima l'audit gratuito",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Raccontaci il tuo progetto: ti rispondiamo entro un giorno lavorativo con le prime idee.",
        "h1": "Parliamo del tuo <em>prossimo passo</em>.",
        "sub": "Rispondi a qualche domanda: in due minuti ci dai il quadro della tua azienda e noi arriviamo alla prima call già preparati, con idee concrete.",
        "info": [("Email", None), ("Risposta", "Entro un giorno lavorativo"), ("Dove", "Italia · lavoriamo anche da remoto"), ("Lingue", "Italiano, English, Español, Deutsch, 中文")],
        "next_k": "Come funziona",
        "next": [("Compili il modulo", "Due minuti per raccontarci obiettivi, situazione attuale e tempi."),
                 ("Analizziamo il tuo caso", "Entro un giorno lavorativo ti scriviamo con le prime idee e una proposta di data."),
                 ("Call strategica gratuita", "30 minuti per mostrarti cosa si può costruire o automatizzare nella tua azienda, e da dove conviene partire.")],
        "form_h": "Iniziamo dal tuo progetto",
        "steps": ["Il progetto", "La tua azienda", "Tempi e contatti"],
        "f": {"need": "Di cosa hai bisogno?", "need_hint": "Puoi sceglierne più di uno",
              "need_opts": ["Sito web o landing page", "App o gestionale su misura", "CRM e vendite", "Prenotazioni ed email marketing", "Automazioni (con o senza AI)", "Agenti AI e assistenti vocali", "Company brain", "Dashboard e controllo di gestione", "Integrazioni tra software", "Multilingue o progetti con la Cina", "Sicurezza di siti, app e agenti AI", "Non lo so ancora"],
              "goal": "Qual è l'obiettivo principale?", "goal_ph": "Es. vogliamo smettere di gestire i contatti su Excel e sapere ogni giorno quanto vende ogni commerciale",
              "company": "Nome dell'azienda", "site": "Sito web", "site_ph": "www.tuazienda.it",
              "sector": "Settore", "sector_ph": "Es. e-commerce, studio professionale, formazione",
              "team": "Quante persone lavorano in azienda?", "team_opts": ["1-5", "6-20", "21-50", "Oltre 50"],
              "tools": "Quali strumenti usate oggi?", "tools_ph": "Es. Shopify, Excel, HubSpot, WhatsApp, Calendly",
              "when": "Quando vorresti partire?", "when_opts": ["Subito", "Entro 1-3 mesi", "Entro 6 mesi", "Sto valutando"],
              "budget": "Budget indicativo", "budget_opts": ["0 – 1.000 €", "1.000 – 5.000 €", "5.000 – 15.000 €", "15.000 – 50.000 €", "Oltre 50.000 €", "Da definire insieme"],
              "name": "Nome e cognome", "role": "Ruolo", "role_ph": "Es. titolare, direttore commerciale", "email": "Email di lavoro", "phone": "Telefono", "phone_ph": "Facoltativo",
              "source": "Come ci hai conosciuto?", "source_opts": ["Passaparola", "Google", "Social", "LinkedIn", "Altro"],
              "privacy": "Acconsento al trattamento dei miei dati per essere ricontattato in merito alla richiesta.",
              "next": "Avanti", "back": "Indietro", "send": "Invia la richiesta", "sending": "Invio in corso…", "req": "Obbligatorio",
              "ok_h": "Richiesta ricevuta.", "ok_p": "Grazie! Analizziamo la tua situazione e ti scriviamo entro un giorno lavorativo con le prime idee e una proposta di data per la call.",
              "err": "Invio non riuscito. Riprova o scrivici direttamente a", "step_of": "Passo {a} di {b}"},
        "subject": "Nuova richiesta dal sito",
    },
},
"en": {
    "nav": {"work": "Projects", "services": "Services", "security": "Security", "solutions": "Solutions", "mission": "Mission", "studio": "Lab", "contact": "Contact"},
    "nav_d": {"work": "Work you can try live", "services": "What we can build for you", "security": "Sites, apps and AI agents, secured", "solutions": "Examples for your industry", "mission": "Our commitment to the sea", "studio": "Our method and the people behind it", "contact": "Tell us about your project"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot": "© 2026 Reef 7 Lab · Software and AI development",
    "cta_k": "New project", "cta_h": "Let's build your <em>reef</em>.",
    "founder": {"k": "Who is behind Reef 7 Lab", "h": "I'm with you from start to finish.",
                "p": "I'm Alessandro, founder of Reef 7 Lab. Handing over your company's processes is an important decision, and I treat it as one. First I study how you work. Then I tell you clearly what makes sense, what it costs and how long it takes. No surprises halfway through, and after delivery I remain your point of contact.",
                "points": [["Asia Baldoni Fitness", "Technology partner: most of 54 tools replaced by one internal platform"], ["Tupitago", "Co-founder of a software startup that won a Marche Region grant"], ["E-commerce", "Software and marketing for Veneziana, Breeez and Full Peak"], ["5 languages", "Trained across Italy, Germany and Spain"]],
                "cta": "Book the free call", "a": "My story",
                "risk": "A free 30-minute call to work out where it makes sense to start in your company. I reply within one business day.",
                "contact_h": "I'll reply myself", "contact_p": "I read every request personally and reply within one business day, with first ideas."},
    "services": [
        ("31", "Grow revenue", "Sales system, from lead to cash", "Every lead followed through to payment, with nobody lost along the way.",
         "It's the system we watched help a seven-figure company grow: every lead is assigned to the right person within minutes, moves through call, qualification and close with clear roles, those who don't close are picked up again at the right moment, and every payment goes back to the rep and the campaign that generated it. We build it on your process, with your numbers.",
         ["Automatic assignment within minutes, with rules and weights", "Clear roles: first contact, qualification, close", "AI briefing before every call", "Follow-up content chosen by objection", "Target, trajectory and diagnosis when you're behind"]),
        ("28", "Grow revenue", "Lead and lost-deal recovery", "The leads you already paid for turn back into customers.",
         "Every company has a drawer full of leads never called back and deals closed with an \"I'll think about it\". We build rules that pick them up on their own: a lead idle for half an hour gets assigned, a call that didn't close comes back after a few weeks to another person, with content chosen on the objection that came up.",
         ["Idle leads assigned automatically within minutes", "Unclosed calls picked up at the right moment", "Reassigned to someone else if nobody moves", "Contact priorities always clear", "Everything logged, no duplicates"]),
        ("29", "Grow revenue", "Upsells, renewals and returning customers", "The customer you already have is the easiest to grow.",
         "The easiest sale is to a happy customer, at the right moment. We use the data you already have, such as purchases, usage and results, to offer upgrades, renewals and repeat purchases when the customer is ready: a reminder to the rep halfway through, a sequence to inactive customers, an offer to those getting results.",
         ["Upgrade offers halfway through, calculated automatically", "Renewals and repeat purchases reminded automatically", "Usage and results signals on the customer profile", "Sequences for inactive or leaving customers", "Revenue per customer over time always in view"]),
        ("30", "Grow revenue", "Targets, commissions and team leaderboard", "A sales team that sees every day where it's heading, and why.",
         "When commissions are calculated by hand at month end, nobody really knows what they're earning until it's too late. We connect payments and CRM: tiered commissions on cash collected, shares for whoever booked the appointment, team bonuses, weekly and monthly leaderboards, and a trajectory that tells you in real time whether the target is within reach.",
         ["Tiered commissions calculated on cash collected", "Shares for whoever books and whoever closes", "Weekly and monthly leaderboard", "Trajectory and projection to target", "Team bonuses with clear thresholds"]),
        ("18", "Grow revenue", "Reviews and referrals", "Happy customers become your best sales channel.",
         "Most happy customers don't leave a review simply because nobody asks at the right moment. We automate the request after a purchase or visit, listen privately to unhappy customers before they post in public, and reward the people who bring you new clients.",
         ["Review requests at the right moment, on Google and on your site", "Unhappy customers are heard in private", "Referral programme with tracked rewards", "Best reviews shown on your site and product pages", "Average rating and new reviews under control"]),
        ("23", "Grow revenue", "Tracking and attribution", "You know where every customer comes from, all the way to payment.",
         "Without tracking, campaigns optimise for visits, not sales. We connect pages, forms, CRM and ad platforms: every contact carries its source, every sale goes back to the campaign that generated it, and Meta and Google receive the events that really matter.",
         ["UTMs and source saved on every contact", "Conversion events sent to Meta and Google", "From campaign to cash, not just to the click", "Forms and sources always distinguishable", "Reports by channel, campaign and sales rep"]),
        ("11", "AI", "AI sales agents", "Every lead gets an answer within seconds, at any hour.",
         "A lead that waits a day is a lead that goes cold. The agent replies on your website, WhatsApp and email, asks the right questions to see who is ready to buy, books the call in the rep's calendar and updates the CRM. Sensitive cases always go to a person.",
         ["Instant replies on website, WhatsApp and email", "Leads qualified with your questions", "Calls booked with the right rep", "CRM updated with no manual entry", "Hand-off to a person when needed"]),
        ("06", "AI", "Automation, with and without AI", "The hours lost to repetitive work go back to your team.",
         "Answering the same emails, copying data, filling in reports: work that helps no one grow. We automate it: with rules and integrations where a precise workflow is enough, with AI where text needs to be understood and decisions made, always with human review at the critical steps. And we measure exactly how much time it gives back.",
         ["Finding the tasks that cost the most time", "Automated workflows between your tools, no AI needed", "AI agents for email, documents and requests", "Leads qualified and routed automatically", "Human review at the critical steps", "Time saved, measured"]),
        ("12", "AI", "AI voice assistants", "A phone assistant that answers, books and calls back.",
         "Missed calls are missed customers. The voice assistant answers with a natural voice, in several languages, books appointments, confirms and reminds bookings and calls back anyone who didn't pick up. Every conversation reaches the team already transcribed and summarised.",
         ["Phone answered at any hour", "Bookings, confirmations and reminders", "Call-backs for missed contacts", "Multiple languages, natural voice", "Transcript and summary of every call"]),
        ("07", "AI", "Company brain", "Everything your company knows, one question away.",
         "Procedures, documents, answers already given to clients: your company's knowledge is scattered across folders, chats and people. We bring it together in an assistant that answers your team in seconds and always shows where the information comes from.",
         ["Collecting and organising documents", "Answers with sources, always verifiable", "Everyone sees only what they should", "Content that stays up to date", "Private, protected data"]),
        ("13", "AI", "Sales call analysis", "Every call becomes a lesson for the whole team.",
         "Sales calls are transcribed and analysed: how closely the script was followed, which objections came up, where the deal was lost. Team leads see right away what to work on, and every rep gets concrete suggestions after each call.",
         ["Automatic call transcription", "Score against your sales script", "Recurring objections highlighted", "Suggestions for every rep", "Reports for team leads"]),
        ("26", "AI", "AI training for your team", "Your team uses AI on real work, from day one.",
         "AI tools only really pay off when they know your company. We set them up with your company's context, processes and tone of voice, and train your team on real cases: emails, analysis, documents, automations.",
         ["AI assistants set up with your company context", "Hands-on training on each team's processes", "Shared library of instructions and templates", "Clear rules on data and privacy", "Support through the first weeks"]),
        ("36", "Security", "Securing existing websites and apps", "Built for yesterday's web. Exposed to today's attacks.",
         "When your website or internal tool was built, attacking it took time and a skilled person. Today a program does it nonstop, at almost no cost: it tries passwords stolen elsewhere, looks for components with known flaws and probes every form and API. We analyse what you have, show you where the way in is and close every gap by severity. Without rebuilding everything, without stopping your work.",
         ["Review of websites, apps, stores and internal tools, even older ones", "Vulnerable components, plugins and libraries updated or isolated", "Defences against bots, account takeover and mass login attempts", "Forms and APIs protected from abuse and automated data harvesting", "A plan by severity: right away, in the coming weeks, structural"]),
        ("37", "Security", "Access, passwords and people", "The easiest way in is still a door left open.",
         "A test admin panel protected by the password 123456 exposed data tied to millions of job applications. It didn't take a genius, just a forgotten login. Former collaborators still active, passwords shared in chat, keys never rotated, integrations authorised years ago: we take stock of who can get in where, close what isn't needed and make security simple for your whole team.",
         ["Inventory of accounts, service keys and authorised integrations", "Access revoked for anyone who no longer needs it", "Two-factor login and a password manager for the whole team", "Role-based permissions: everyone sees only what they need", "Training against phishing and scams, including voice and AI-written ones"]),
        ("38", "Security", "Email and scams in your name", "The best scams come from an address that looks like yours.",
         "A fake invoice sent to your customers from your domain, a supplier asking to change bank details, a voice message with the owner's voice: today scams are written, and even spoken, with AI, and they look real. We protect your domain so nobody can write in your name, and train your team to spot attempts before they cost you.",
         ["SPF, DKIM and DMARC set all the way to blocking fake emails", "Alerts when someone tries to use your domain", "Double confirmation for payments and bank detail changes", "Realistic phishing tests for your team", "A clear procedure for what to do with a strange email"]),
        ("32", "Security", "Security review for AI-built websites and apps", "Live in a weekend. Open to anyone for months?",
         "When researchers analysed 1,645 apps published with a well-known AI app builder, 170 let anyone read user lists, payments or keys. Not because of a clever attack, but because database rules were never written. AI tools build fast, but they don't think about who will try to get in. We do: we hunt down the typical mistakes one by one, fix them and hand back a project you can grow without worry.",
         ["Keys and secrets searched for in the code and the full repository history", "Database rules checked table by table", "Roles and permissions tested by logging in as different users", "Private pages and APIs tested without logging in", "A clear report, with the fixes already applied"]),
        ("33", "Security", "Security for chatbots and AI agents", "The more an agent can do, the more its mistakes cost.",
         "A single crafted email was enough to make a widely used AI assistant hand over company data, without a single click. A coding agent deleted a production database during a code freeze. A compromised chatbot integration opened the CRMs of hundreds of companies. We put your agent through the same attacks, strip the permissions it doesn't need and put a person in front of every action that matters.",
         ["Tests against instructions hidden in emails, documents and web pages", "Least privilege: the agent reaches only what it needs", "Human approval before actions that move data or money", "Separate environments: no experiments on real data", "A full log of conversations and actions"]),
        ("34", "Security", "Privacy and data when you use AI", "Every prompt is data leaving your company.",
         "Contracts pasted into a chat, customer lists uploaded for analysis, emails summarised by an assistant: each time, data leaves your company, often with nobody knowing where it ends up or how long it stays. We trace these flows, strip personal data where it isn't needed and choose services and settings that fit GDPR, together with your legal advisor. Your team uses AI every day without exposing your customers.",
         ["A map of the data that goes through AI services", "Personal data removed or masked before it is sent", "Providers, servers and contracts that fit GDPR", "Privacy notice and processing records kept up to date", "Clear rules for your team on everyday AI use"]),
        ("35", "Security", "Monitoring and service continuity", "If something breaks, you know before your customers do.",
         "The backup that won't restore, the update postponed for months, the site that goes down on a Friday night: these are the problems that cost the most and that nobody sees until it's too late. We watch your sites, apps and internal tools every day, actually test restores and apply updates on a fixed schedule. Every month you get a clear report, written for decision makers, not for developers.",
         ["Continuous monitoring with instant alerts", "Automatic backups and real restore tests", "Defences against bots and attacks that take the site down", "Security updates on a schedule", "A monthly report readable by non-technical people"]),
        ("03", "Sales and payments", "Custom CRM", "Leads, deals and commissions in one tool, built around the way you sell.",
         "A generic CRM forces your sales team to adapt. We build custom CRMs: every lead arrives already assigned, deals move through clear stages, payments and commissions calculate themselves, and leadership sees results and rankings in real time.",
         ["Pipeline and stages designed around your process", "Automatic lead assignment", "Payments and commissions calculated automatically", "Team leaderboard and KPIs, even on a screen in the office", "Connected to your website, bookings and email"]),
        ("04", "Sales and payments", "Bookings and sales calendar", "Your own booking system, assigning every appointment to the right person.",
         "Prospects book a call on their own. The system distributes appointments across your sales team, sends every contact back to their own rep and sends reminders, so fewer people miss their call.",
         ["Booking page with your branding", "Automatic distribution across the sales team", "Every contact always returns to their rep", "Automatic reminders", "Appointments logged straight into the CRM"]),
        ("05", "Sales and payments", "Email marketing and automation", "Email sequences that work for you, with deliverability under control.",
         "From the welcome email to the follow-up after a call, emails go out at the right moment based on what each contact does. We also handle the technical side that decides whether an email lands in the inbox or in spam.",
         ["Automated sequences for every customer stage", "Segmentation based on behaviour", "Domain warm-up and list management", "Open and reply statistics", "An alternative to subscription platforms"]),
        ("22", "Sales and payments", "Emails that actually arrive", "If your emails land in spam, the copy isn't the problem.",
         "Often the problem isn't what you write but whether it arrives: unauthenticated domains, lists never cleaned, sends to the whole database. We check DNS, reputation, lists and automations, and measure real opens, not the ones inflated by automatic filters. In a real audit, 68% of reported opens had never happened.",
         ["Domain authentication: SPF, DKIM and DMARC", "Real opens separated from automatic ones", "List cleaning and suppression rules", "Automations without double sends or re-entries", "Gradual warm-up of new domains"]),
        ("24", "Sales and payments", "Payments, instalments and overdue", "Every instalment collected on time, without chasing anyone.",
         "Instalment plans, contracts and reminders handled by hand mean money that arrives late, or never. We connect payments, contracts and CRM: reminders before the due date, a follow-up on the day, automatic Stripe reconciliation and every payment attributed to the right person.",
         ["Contracts and instalment plans recorded once", "Automatic reminders before and after the due date", "Automatic Stripe reconciliation", "Overdue payments always in view", "Cash attributed to the right sales rep"]),
        ("10", "Fewer tools, lower costs", "From subscriptions to your own tools", "We replace subscription software with tools you own, all connected.",
         "CRM, email, bookings, automation: many companies pay for several monthly subscriptions that do similar things and don't talk to each other. We analyse the costs and replace the ones worth replacing with your own tools, simpler and connected.",
         ["Review of the software you use and what it costs", "Migration plan with no downtime", "Data transferred and verified", "Tools that work together", "Lower recurring costs over time"]),
        ("20", "Fewer tools, lower costs", "Systems X-ray", "Find out how your software really talks to each other, and what it costs you.",
         "We open the tools you use one by one and measure what really happens: which connections work, which data is duplicated, which automations run for nothing and where keys or access are exposed. In a real case a single contact went through five systems and six destinations, and nobody knew which of the five was in charge.",
         ["Map of every tool and its real connections", "Duplicates, errors and stalled automations, measured", "Software costs by category and share of revenue", "Security: exposed keys, access and webhooks", "A plan by impact: today, this week, structural"]),
        ("21", "Fewer tools, lower costs", "Owned email marketing", "The same emails as always, at a fraction of the cost.",
         "Email marketing platforms charge by contact, even when most contacts never open anything. We build your own sending system on the same infrastructure the big platforms use: in a real case 100,000 sends went from almost $1,000 to about €10, with opens and clicks visible on every contact's profile.",
         ["Sending on professional infrastructure, paid per email", "Automations and segments as before, connected to the CRM", "Opens and clicks on every contact's profile", "Gradual switch, without losing domain reputation", "Segments created by asking in plain language"]),
        ("09", "Fewer tools, lower costs", "Company hub and integrations", "All your company's tools connected and reachable from one place.",
         "An internal portal where everyone accesses the tools they need, built on a single database. We connect your software through APIs and webhooks, so data moves on its own.",
         ["Internal portal with role-based access", "One database for every application", "Integrations through APIs and webhooks", "Org chart and procedures always at hand", "Security and backups included"]),
        ("08", "Management", "Dashboards and financial control", "Sales, cash and margins in one view, always up to date.",
         "If understanding how the company is doing takes three people and a spreadsheet, you'll always decide too late. We connect your sources into dashboards for leadership: sales metrics, cash flow, margins and financial statements, updated on their own.",
         ["Sales and marketing metrics", "Cash flow and margins", "Dedicated views for leadership and teams", "Automatic updates from your sources", "Role-based secure access"]),
        ("19", "Management", "Orders, stock and suppliers", "Orders, stock and deliveries in one view, across every channel.",
         "When orders come from your store, marketplaces, phone and agents, stock never adds up and someone spends their days copying. We connect channels, warehouse, couriers and suppliers: every order follows its path on its own and you always know what's in stock, what's missing and what's on its way.",
         ["Orders from every channel in one panel", "Synced stock, with low-stock alerts", "Automatic labels, couriers and tracking", "Supplier reorders prepared automatically", "Returns handled from request to refund"]),
        ("25", "Management", "Org chart, onboarding and internal support", "Everyone knows who to ask, and problems get solved sooner.",
         "As a company grows, internal questions always land on the same people. We build a searchable org chart, onboarding paths for new hires and a reporting channel with a clear template, summarised every day by a routine.",
         ["Org chart searchable by person, role and skill", "Onboarding with guides and videos for every role", "Reports with one template and clear priority", "Automatic daily summary of open issues", "Tool documentation always up to date"]),
        ("01", "Digital", "Websites and landing pages", "Websites and sales pages that turn visits into enquiries.",
         "Your website is often the first contact a client has with you. We design websites and landing pages that explain the value straight away, guide people towards getting in touch, and can be updated without calling anyone.",
         ["Structure and copy built to convert", "Custom design, no templates", "Landing pages and funnels for campaigns", "Optimised for Google and for mobile", "Every enquiry tracked"]),
        ("02", "Digital", "Custom applications", "Software that fits the way you work. Not the other way round.",
         "If your team spends more time working around a system than using it, the problem isn't the team. We design management tools, client portals and internal software around the way your company really works.",
         ["Process analysis and clickable prototype", "Web and desktop applications", "Role-based access and permissions", "Integration with the tools you already use", "New features as you grow"]),
        ("27", "Digital", "Client apps and online programmes", "Courses, programmes and clients in an app you own, not rent.",
         "Video courses on one platform, programmes on another, community on a third: clients get lost and you pay three subscriptions. We build a branded app where clients follow their programme, watch lessons and talk to their coach, connected to CRM and payments, with a dedicated area for coaches.",
         ["Programmes, lessons and progress for every client", "Coach area to follow every client", "Access unlocked by payment", "Connected to CRM, email and payments", "Migration from current platforms without losing clients"]),
        ("17", "Digital", "Client portals", "Your clients find everything themselves, without writing to ask.",
         "Documents to send, work status, deadlines, payments: every client question is one more email or phone call. We build a branded private area where each client uploads documents, follows progress, downloads invoices and gets reminders at the right time.",
         ["Private, branded access for every client", "Document upload with automatic reminders", "Work status and deadlines always visible", "Invoices, contracts and online signatures", "Connected to your CRM and management system"]),
        ("14", "Digital", "3D configurators and augmented reality", "Customers see the product before they buy it, exactly the way they want it.",
         "A product you can rotate, customise and place in your own space sells better than a photo. We build 3D configurators and augmented reality previews that run straight in the browser, with no app to download, connected to your catalogue and prices.",
         ["3D models to rotate and customise", "Augmented reality try-on from the phone", "Price updated with every choice", "No app to download", "Connected to catalogue and orders"]),
        ("15", "International", "Multilingual websites and e-commerce", "Speak to customers in every country in their own language, for real.",
         "Translating a website isn't enough: every market has its own words, doubts and buying habits. We adapt copy, pages and communication in Italian, English, Spanish, German and Chinese, with a single panel to manage every version.",
         ["Content adapted to each market, not just translated", "Italian, English, Spanish, German and Chinese", "One panel for every language", "Email and support in the customer's language", "Search visibility in every country"]),
        ("16", "International", "Bridge to China", "Chinese suppliers, orders and customers, handled as if they were around the corner, wherever your company is.",
         "Working with China means different languages, time zones, platforms and software, whether you're in Italy, elsewhere in Europe or beyond. We connect your Chinese suppliers' systems to yours, so orders, shipments and quality checks are tracked in one view; we prepare your website, content and customer care for Chinese customers; and we handle communication in Chinese with the help of AI and human review.",
         ["Integration between your Chinese suppliers' software and yours", "Orders, shipments and quality checks in one view", "Communication in Chinese with suppliers, partners and customers", "Website and customer care designed for Chinese customers", "For companies in any country, with human review at the important steps"]),
    ],
    "sectors": [
        {"t": "Sales teams", "d": "More time on calls, less time in spreadsheets.",
         "pain": "Reps update spreadsheets instead of selling, contacts get lost between calendars and commissions are calculated by hand at the end of the month.",
         "build": ["A CRM built around your sales process", "Bookings distributed automatically across the team", "Email sequences that follow up every contact after the call", "Commissions and leaderboard calculated automatically"],
         "out": "A team that spends more time with clients, and leadership that sees results in real time.", "svc": ["31", "28", "30", "13"]},
        {"t": "E-commerce", "d": "More sales, without more manual work.",
         "pain": "Orders, campaigns and support live in different tools. You find out what worked at the end of the month, when it's too late to fix.",
         "build": ["Product pages built to convert", "A dashboard with sales, ad spend and real margin", "Customer support handled by AI", "A post-purchase customer app built into the store"],
         "out": "You know every day how much you're really making, and your team focuses on growth instead of chasing orders.", "svc": ["01", "23", "19", "18"]},
        {"t": "Professional firms", "d": "Less paperwork, more time for clients.",
         "pain": "Documents to find, deadlines to remember and the same client questions every week: valuable hours you can't bill.",
         "build": ["A private client portal", "Documents filed and classified automatically", "An assistant that knows the firm's procedures", "Automatic reminders for deadlines and appointments"],
         "out": "More hours for advisory work, fewer mistakes and clients who feel genuinely looked after.", "svc": ["17", "07", "12", "04"]},
        {"t": "Education and coaching", "d": "A digital journey as good as what you teach.",
         "pain": "Courses on one platform, community on another, sales handled by hand: students get lost between one step and the next.",
         "build": ["Landing pages and funnels for sign-ups", "Sales calls booked and assigned automatically", "Emails that guide every student from sign-up to results", "An assistant that answers students' questions"],
         "out": "More sign-ups, more engaged students and a business that grows without multiplying the workload.", "svc": ["31", "27", "29", "24"]},
        {"t": "Agencies and B2B services", "d": "Clients looked after better, with fewer manual steps.",
         "pain": "Requests by email, project status in a shared spreadsheet, reports put together by hand every month for every client.",
         "build": ["A client portal with project status and documents", "Client reports generated automatically", "Requests routed to the right person", "An internal knowledge base for the team"],
         "out": "Clients stay informed without having to ask, and the team works on projects instead of email.", "svc": ["17", "08", "06", "07"]},
        {"t": "Growing companies", "d": "Grow without losing control.",
         "pain": "More clients mean more spreadsheets, more subscriptions and more mistakes. The tools that were enough two years ago now slow everything down.",
         "build": ["An internal hub with every tool on a single database", "Leadership dashboards for sales, cash and margins", "Subscription software replaced by tools you own", "Management systems built around your processes"],
         "out": "A single source of truth for the whole company, decisions made on solid data and lower recurring costs.", "svc": ["20", "10", "21", "09"]},
    ],
    "home": {
        "title": "Reef 7 Lab · Software and AI development",
        "desc": "Reef 7 Lab builds custom websites, applications, AI and dashboards, connected into a single system.",
        "kicker": "Reef 7 Lab · Software and AI development",
        "h1": "Your business, <em>connected</em>.",
        "sub": "Websites, applications and AI designed to work together. Less manual work, faster decisions and growth that compounds over time.",
        "b1": "Let's talk about your project", "b2": "Explore services",
        "eco_core": "Your system", "eco_nodes": [("Website", "◎"), ("CRM", "◇"), ("Email", "✉"), ("Payments", "€"), ("Calendar", "◷"), ("Dashboard", "▤")],
        "eco_k": "Systems integration",
        "eco_h": "One system for <em>the whole company</em>.",
        "eco_p": "We connect the tools you already use and automate the steps between them. Data is entered once and reaches wherever it's needed, ready to use.",
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
        "title": "Services · Reef 7 Lab", "desc": "Websites, custom applications, AI agents, voice assistants, company brain, dashboards and China projects.",
        "h1": "Every discipline, <em>one</em> system.",
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
        "seven_p": "The 7 is seven coral reefs, from the Red Sea to Polynesia, that we want to help protect. Every project we build brings us closer to that goal: it's the number that reminds us who we work for, beyond our clients.",
        "who_big": "Behind Reef 7 Lab is <em>Alessandro</em>.",
        "who": ["Alessandro builds software that helps companies grow. He started in 2023 by co-founding Tupitago, a software startup: he led its marketing, product and research, all the way to winning a Marche Region grant. In 2025 he handed over to his co-founder, and Tupitago keeps growing.",
                "Since then he has grown three e-commerce brands, Veneziana, Breeez and Full Peak, owning everything behind a sale: the website, the campaigns, the emails, the customer care. With Chinese suppliers he built the bridges between their software and Italian systems, and handled the relationships in Chinese himself.",
                "Today he works alongside Asia Baldoni Fitness and Tartufoli Group, where he helped replace most of the company's 54 tools with one internal platform, cutting software costs by about 83%.",
                "His background is international: a degree in Language Mediation, a semester at Heidelberg University, Germany's first, and a marketing internship in Tenerife. He works in five languages, Italian, English, Spanish, German and Chinese: projects with clients, partners and suppliers abroad never get lost in translation.",
                "For him, the sea is personal: for years he was an active volunteer with 2hands Ancona, cleaning beaches and coastlines of litter."],
        "creds": [("Tupitago · 2023–2025", "Co-founder, winner of a Marche Region grant"), ("3 e-commerce brands", "Software and marketing for Veneziana, Breeez, Full Peak"),
                  ("Heidelberg · 2024", "Heidelberg University, semester on a merit scholarship"), ("Tenerife · 2023", "Internship at a marketing agency"),
                  ("5 languages", "Degree in Language Mediation, 2025"), ("Partners", "Asia Baldoni Fitness and Tartufoli Group")],
        "sign": ("Alessandro", "Founder, Reef 7 Lab"),
        "photo_alt": "Alessandro, founder of Reef 7 Lab",
        "more": "Read the full story",
    },
    "audit": {
        "title": "Free automation audit · Reef 7 Lab", "desc": "In two minutes, find out how many hours a week your team could win back and what to automate first.",
        "k": "Free audit", "h1": "How much time could your team <em>win back</em>?",
        "sub": "Answer a few questions about the work you still do by hand. Get an estimate of the hours you could recover, your priorities and a 3-step plan, also as a PDF.",
        "pts": ["2 minutes", "Personalised report", "Free, no commitment"],
        "home_k": "Free audit", "home_h": "How many hours does <em>your team</em> lose every week?", "home_p": "In two minutes, find out what's worth automating first and how much time you could win back.", "home_a": "Take the audit", "home_k2": "2 minutes · free",
        "vis_k": "Sample report", "vis_u": "hours a week to win back", "vis": [("Copying data between tools", 8), ("Replying to new leads", 4.8), ("Putting together reports", 3)],
        "contact_p": "Not sure where to start yet?", "contact_a": "Take the free audit first",
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Tell us about your project: we'll reply within one business day with first ideas.",
        "h1": "Let's talk about your <em>next step</em>.",
        "sub": "Answer a few questions: in two minutes you give us the picture of your business, and we come to the first call prepared, with concrete ideas.",
        "info": [("Email", None), ("Reply", "Within one business day"), ("Based in", "Italy · working remotely"), ("Languages", "English, Italiano, Español, Deutsch, 中文")],
        "next_k": "How it works",
        "next": [("Fill in the form", "Two minutes to tell us about your goals, current setup and timeline."),
                 ("We review your case", "Within one business day we send you first ideas and a proposed date."),
                 ("Free strategy call", "30 minutes to show you what could be built or automated in your business, and where to start.")],
        "form_h": "Let's start with your project",
        "steps": ["The project", "Your company", "Timeline and contact"],
        "f": {"need": "What do you need?", "need_hint": "You can pick more than one",
              "need_opts": ["Website or landing page", "Custom app or management system", "CRM and sales", "Bookings and email marketing", "Automation (with or without AI)", "AI agents and voice assistants", "Company brain", "Dashboards and financial control", "Software integrations", "Multilingual or China projects", "Security for websites, apps and AI agents", "Not sure yet"],
              "goal": "What's your main goal?", "goal_ph": "E.g. we want to stop managing leads in spreadsheets and know every day how much each rep is selling",
              "company": "Company name", "site": "Website", "site_ph": "www.yourcompany.com",
              "sector": "Industry", "sector_ph": "E.g. e-commerce, professional services, education",
              "team": "How many people work at the company?", "team_opts": ["1-5", "6-20", "21-50", "50+"],
              "tools": "Which tools do you use today?", "tools_ph": "E.g. Shopify, spreadsheets, HubSpot, WhatsApp, Calendly",
              "when": "When would you like to start?", "when_opts": ["Right away", "Within 1-3 months", "Within 6 months", "Just exploring"],
              "budget": "Indicative budget", "budget_opts": ["€0 – €1,000", "€1,000 – €5,000", "€5,000 – €15,000", "€15,000 – €50,000", "Over €50,000", "To be defined together"],
              "name": "Full name", "role": "Role", "role_ph": "E.g. owner, head of sales", "email": "Work email", "phone": "Phone", "phone_ph": "Optional",
              "source": "How did you hear about us?", "source_opts": ["Word of mouth", "Google", "Social media", "LinkedIn", "Other"],
              "privacy": "I agree to the processing of my data so you can get back to me about this request.",
              "next": "Next", "back": "Back", "send": "Send request", "sending": "Sending…", "req": "Required",
              "ok_h": "Request received.", "ok_p": "Thank you! We'll review your situation and get back to you within one business day with first ideas and a proposed date for the call.",
              "err": "Something went wrong. Please try again or email us directly at", "step_of": "Step {a} of {b}"},
        "subject": "New enquiry from the website",
    },
},
}



T["it"]["security"] = {
    "title": "Cybersicurezza per siti, app e agenti AI · Reef 7 Lab",
    "k": "Cybersicurezza per PMI",
    "desc": "Cybersicurezza per PMI: gli attacchi sono già automatici. Mettiamo al sicuro siti, app e gestionali, nuovi e datati, e gli agenti AI che usi: verifica, correzione e guardia continua.",
    "h1": "Gli attacchi sono già <em>automatici</em>. Le tue difese?",
    "sub": "Scrivi il tuo dominio: in 3 minuti scopri cosa vede un attaccante, quanto sei esposto e cosa sistemare per primo. Gratis, senza installare nulla.",
    "feed": {"k": "Simulazione · attacco automatico", "live": "in corso", "dom": "tuazienda.it", "rows": [["03:12:04", "Bot", "prova 2.400 password rubate sul tuo login", "bad"], ["03:12:41", "Agente AI", "cerca plugin e versioni PHP con falle note", "bad"], ["03:13:09", "Scanner", "bussa a 380 indirizzi nascosti del sito", "mid"], ["03:13:55", "Truffa", "email «abbiamo cambiato IBAN» ai tuoi clienti, a nome tuo", "bad"], ["03:14:20", "Bot", "copia listino e contatti dei clienti", "mid"]], "q": "Le tue difese?", "a": "Scoprilo in 3 minuti"},
    "dom_ph": "tuazienda.it",
    "dom_btn": "Controlla gratis",
    "dom_note": "Solo dati pubblici. Nessuna prova invasiva, nessun impegno.",
    "route_k": "Da dove partire",
    "route_h": "Qual è la <em>tua situazione</em>?",
    "route_p": "Scegli il tuo caso: il check parte già impostato.",
    "routes": [
        ("old", "Ho un sito o un e-commerce da qualche anno", "WordPress, plugin, gestionali: è lì che gli attacchi automatici cercano per primi.", "Controlla il tuo sito"),
        ("ai", "Ho fatto un sito o un'app con l'AI", "Funziona. Ma qualcuno ha controllato chi può leggere i dati?", "Controlla il tuo progetto"),
        ("agent", "Usiamo chatbot o agenti AI", "Leggono email, documenti e CRM. Vediamo cosa possono fare, e cosa no.", "Controlla i tuoi agenti"),
        ("inc", "È successo qualcosa di strano", "Email sospette, accessi che non riconosci, sito modificato: scrivici e partiamo subito.", "Scrivici adesso"),
    ],
    "get_h": "Cosa ricevi <em>in 3 minuti</em>",
    "get_p": "Un report chiaro, scritto per chi decide.",
    "get": [
        "Il tuo livello di esposizione: basso, medio, alto o critico",
        "Cosa vede chi attacca dal tuo dominio: protezioni del sito ed email a tuo nome",
        "Le 3 priorità da cui partire, con cosa puoi fare già oggi da solo",
        "Una copia del report per email, e la mia risposta entro un giorno lavorativo",
    ],
    "fix_h": "Cosa <em>sistemiamo</em>",
    "fix_p": "Solo dove serve. Senza rifare tutto, senza fermare il lavoro.",
    "fix_more": "Cosa comprende",
    "end_h": "Il primo passo richiede <em>3 minuti</em>.",
    "end_p": "Scrivi il tuo dominio. Se poi vuoi parlarne, ti rispondo io entro un giorno.",
    "now_k": "Perché adesso",
    "now_h": "Il tempo per rimediare <em>si è accorciato</em>.",
    "now": [
        ("7 su 10", "dei siti gira su PHP, il linguaggio in cui il 21 ottobre 2026 un'AI ha trovato falle critiche.", "AP / PBS NewsHour", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
        ("Poche ore", "tra l'annuncio di quelle falle e i primi milioni di tentativi di attacco.", "AP / PBS NewsHour", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
        ("51%", "del traffico web è ormai automatico: bot e agenti, non persone.", "Imperva, Bad Bot Report 2025", "https://www.imperva.com/blog/2025-imperva-bad-bot-report-how-ai-is-supercharging-the-bot-threat/"),
    ],
    "now_end": "Non serve allarmarsi. Serve muoversi prima.",
    "loss_k": "Cosa rischi davvero",
    "loss_h": "Non rischi il sito. <em>Rischi i soldi.</em>",
    "loss_p": "Per chi attacca, il sito è solo la porta. Quello che cerca sono i tuoi soldi, i tuoi dati e i tuoi clienti.",
    "losses": [
        ("money", "Un bonifico sul conto sbagliato", "Arriva un'email del tuo fornitore, dal suo indirizzo vero: «abbiamo cambiato IBAN». Paghi. Nessun virus, solo una casella violata, e quei soldi non tornano."),
        ("bank", "Banca e pagamenti in mano a un altro", "Dalla tua email si azzerano le password di banca, Stripe, PayPal e marketplace. Di solito basta una password riutilizzata, senza doppio fattore."),
        ("data", "I dati dei tuoi clienti in vendita", "Una lista clienti copiata non si recupera più. E il GDPR prevede sanzioni fino a 20 milioni di euro o al 4% del fatturato mondiale, con 72 ore per avvisare il Garante."),
        ("lock", "L'azienda ferma, in attesa di un riscatto", "In una notte file, gestionale e backup diventano illeggibili. Chi li ha cifrati chiede un riscatto, e pagare non garantisce di riavere nulla. Ogni giorno di fermo è fatturato perso."),
        ("users", "I tuoi clienti truffati a nome tuo", "Fatture false che partono dal tuo dominio, un checkout manomesso che copia le carte. I soldi li perdono i tuoi clienti; la fiducia la perdi tu."),
        ("alert", "La reputazione bruciata in un giorno", "Pagine truffa sul tuo sito, Google che lo segnala come pericoloso, recensioni piene di clienti arrabbiati. Bastano poche ore per bruciarla, servono anni per ricostruirla."),
    ],
    "loss_src": ("GDPR, articoli 33 e 83", "https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016R0679"),
    "loss_cta": "Scopri cosa rischi tu: fai il check gratuito",
    "scan": {"k": "Esempio di check", "dom": "tuazienda.it", "live": "analisi completata", "rows": [
            ("Protezioni del sito", "F", "bad"),
            ("Email a tuo nome", "Non protetta", "bad"),
            ("Piattaforma", "PHP da aggiornare", "mid"),
            ("Accessi", "2 ex collaboratori attivi", "mid"),
        ], "lvl": "Esposizione", "lvl_v": "Alta", "prio": "3 priorità pronte nel report"},
    "check_hint": "Spunta quello che ti riguarda",
    "check_ok": "Ha senso parlarne. Il check gratuito ti dice da dove partire.",
    "gain_h": "Cosa <em>ottieni</em>",
    "gain_p": "Non un documento da archiviare: risultati che vedi.",
    "gains": [
        ("Sai dove sei esposto", "Una mappa chiara di tutto ciò che si vede da fuori e di quanto vale ogni rischio, scritta per chi decide."),
        ("Le falle gravi chiuse per prime", "Si parte da ciò che mette a rischio soldi e dati. Il resto segue un piano con tempi precisi."),
        ("Niente da rifare, niente da fermare", "Lavoriamo su quello che hai già, su copie o fuori orario. Il team continua a lavorare come sempre."),
        ("Qualcuno di guardia, sempre", "Monitoraggio, aggiornamenti e un rapporto al mese. Tu pensi all'azienda, al resto pensiamo noi."),
    ],
    "start_h": "Come <em>iniziare</em>",
    "start_p": "Tre passi. I primi due sono gratuiti.",
    "start": [
        ("Check di esposizione", "Gratis · 3 minuti", "Scrivi il tuo dominio e ricevi subito il livello di esposizione e le 3 priorità."),
        ("Ricognizione", "Gratis · 30 minuti", "Guardiamo insieme il risultato: cosa conviene fare, in che ordine, in quanto tempo."),
        ("Intervento", "Proposta scritta", "Interventi, tempi e costi messi per iscritto prima di partire. Nessuna sorpresa."),
    ],
    "start_promise": "Se nella ricognizione non troviamo nulla da migliorare, te lo diciamo. E finisce lì.",
    "sub_src": ("Fonte: AP / PBS NewsHour, ottobre 2026", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
    "alert_k": "21 ottobre 2026",
    "alert_h": "Un'AI ha trovato falle critiche nel linguaggio di 7 siti su 10. <em>Poche ore dopo, milioni di tentativi di attacco.</em>",
    "alert_p": "Le falle erano in PHP, il linguaggio di WordPress, di gran parte degli e-commerce e di moltissimi gestionali: permettevano di prendere il controllo del server a distanza. L'FBI ha consigliato di spegnere i siti non aggiornabili subito. Giappone, Regno Unito e Finlandia hanno messo offline parte dei servizi pubblici.",
    "alert_pts": [
        ("Cosa è successo", "Un'AI ha trovato falle critiche in PHP: permettono di prendere il controllo del server a distanza."),
        ("Chi riguarda", "Chi ha un sito WordPress, un e-commerce o un gestionale web: circa 7 siti su 10."),
        ("Cosa fare", "Verificare subito che il sito sia aggiornato. L'FBI ha consigliato di spegnere quelli che non lo sono."),
    ],
    "alert_q": "Il tuo sito gira su PHP? È già aggiornato?",
    "alert_a": "Scoprilo con il check di esposizione",
    "alert_src": ("AP / PBS NewsHour, 22 ottobre 2026", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
    "b1": "Fai il check gratuito",
    "b2": "Come lavoriamo",
    "risks_h": "Cosa è <em>cambiato</em>",
    "risks_p": "In poche settimane l'attacco è diventato un software che lavora da solo. Gran parte di ciò che è online è stato pensato per un web più lento.",
    "risks": [
        ("Tra la scoperta e l'attacco passano ore", "Una falla rimasta nel codice per oltre dieci anni è stata trovata da un'AI, e nelle ore dopo l'annuncio sono partiti milioni di tentativi di sfruttarla. Aggiornare tra una settimana vuol dire arrivare tardi. Non scegli tu se essere un bersaglio: basta essere online."),
        ("Si pubblica prima di controllare", "Un'app generata con l'AI va online in un weekend. Regole d'accesso, chiavi e permessi spesso non li ha mai guardati nessuno."),
        ("Gli assistenti hanno le chiavi di casa", "Chatbot e agenti leggono email, documenti e CRM, e possono agire. Per manipolarli non serve violarli: basta scrivere la cosa giusta nel posto giusto."),
    ],
    "cases_k": "Perché non aspettare",
    "cases_h": "Non è teoria. <em>È cronaca.</em>",
    "cases_p": "Casi pubblici, con le fonti. Tutti evitabili.",
    "cases": [
        ("Settembre 2025", "Un'AI ha attaccato 30 organizzazioni. Quasi da sola.", "Un gruppo sponsorizzato da uno stato ha usato un agente AI per svolgere in autonomia l'80-90% del lavoro operativo contro una trentina di organizzazioni: ricognizione, ricerca di falle, furto di credenziali.", "Il lavoro di una squadra di attaccanti, fatto da una macchina.", "Anthropic", "https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf"),
        ("Agosto 2025", "Un chatbot bucato. I CRM di centinaia di aziende copiati.", "Con i token di accesso rubati all'integrazione di un chatbot di vendita, gli attaccanti hanno estratto dati dai CRM di oltre 700 organizzazioni, comprese aziende di sicurezza informatica, cercando chiavi e password.", "Ogni strumento collegato ai tuoi dati è una porta in più.", "TechTarget", "https://www.techtarget.com/cybersecurity/news/366630934/News-brief-Salesloft-Drift-breach-update-and-timeline"),
        ("Giugno 2025", "Nessun clic. Bastava un'email per portare fuori i dati.", "Una sola email preparata ad arte bastava a far consegnare dati interni a un server esterno da un assistente AI aziendale diffusissimo, senza che l'utente cliccasse nulla. Corretto prima che venisse sfruttato.", "Per un assistente AI, anche un'email è un ordine.", "BleepingComputer", "https://www.bleepingcomputer.com/news/security/zero-click-ai-data-leak-flaw-uncovered-in-microsoft-365-copilot/"),
        ("2025", "Fatte con l'AI. Una su dieci lasciava tutto aperto.", "Su 1.645 app pubblicate con un noto generatore basato sull'AI, i ricercatori ne hanno trovate 170 che lasciavano leggere a chiunque utenti, pagamenti o chiavi.", "Funzionare non vuol dire essere protetti.", "Superblocks", "https://www.superblocks.com/blog/lovable-vulnerabilities"),
        ("Luglio 2025", "13.000 documenti d'identità. Aperti a chiunque.", "Un'app di incontri ha esposto circa 72.000 immagini, tra cui 13.000 selfie e documenti d'identità, da uno spazio di archiviazione accessibile dall'esterno.", "Basta un'impostazione sbagliata.", "CyberInsider", "https://cyberinsider.com/tea-app-suffers-data-breach-exposing-72000-users-photos-and-private-messages/"),
        ("Luglio 2025", "La password era 123456. Dietro, fino a 64 milioni di candidature.", "La piattaforma di selezione con chatbot usata da una grande catena di fast food aveva un pannello di prova protetto da 123456, senza doppio fattore: aperti i dati di fino a 64 milioni di candidature.", "Un pannello dimenticato è una porta di servizio aperta.", "BleepingComputer", "https://www.bleepingcomputer.com/news/security/123456-password-exposed-chats-for-64-million-mcdonalds-job-chatbot-applications/"),
    ],
    "areas": [
        ("Ciò che è già online", "Quello che <em>hai già</em>", "Il sito di cinque anni fa, il gestionale su misura, l'e-commerce con plugin mai aggiornati: sono i primi posti dove cercano gli attacchi automatici. Li rinforziamo senza rifarli.", ["36", "35"]),
        ("L'AI che usi", "L'AI, <em>senza sorprese</em>", "Siti e app generati con l'AI, chatbot e agenti collegati ai tuoi dati: controlliamo cosa possono leggere e fare, e fissiamo confini chiari.", ["32", "33", "34"]),
        ("Persone ed email", "Persone <em>ed email</em>", "Spesso non serve una falla: basta un accesso dimenticato o un'email che sembra vera. Chiudiamo anche questa porta.", ["37", "38"]),
    ],
    "steps_h": "Come <em>lavoriamo</em>",
    "steps_p": "Quattro fasi, sempre autorizzate da te per iscritto.",
    "steps": [
        ("Ricognizione", "Mappiamo tutto ciò che si vede da fuori: domini, pagine, moduli, API, accessi e integrazioni. Spesso è la prima mappa completa che l'azienda abbia mai avuto."),
        ("Attacco simulato", "Proviamo a entrare con le tecniche di oggi, comprese quelle automatiche e quelle contro gli agenti AI. Ogni falla viene dimostrata, non ipotizzata."),
        ("Messa in sicurezza", "Chiudiamo le falle in ordine di gravità e ti spieghiamo cosa abbiamo cambiato, in parole semplici."),
        ("Guardia continua", "Le tecniche d'attacco cambiano ogni mese. Monitoriamo, aggiorniamo e ripetiamo le verifiche a ogni cambiamento importante."),
    ],
    "faq_h": "Le domande che <em>ci fanno</em>",
    "faq": [
        ("Siamo piccoli: chi vuoi che ci attacchi?", "Nessuno ti sceglie. Gli attacchi automatici provano tutto ciò che è online, senza guardare chi sei. Le piccole aziende sono spesso le più facili: nessuno le controlla."),
        ("Il sito ce l'ha fatto un'agenzia seria.", "Il giorno della consegna era probabilmente a posto. Da allora sono cambiati i componenti, le tecniche d'attacco e chi ha un accesso. La sicurezza non è un collaudo: è manutenzione."),
        ("Usiamo piattaforme famose, ci pensano loro.", "Proteggono i loro server. Impostazioni, accessi, dati e integrazioni restano a te: è lì che nascono quasi tutti i casi di cronaca."),
        ("Dovremo fermare il lavoro?", "No. Ogni prova è autorizzata per iscritto e si fa su copie o in orari concordati."),
        ("E se non trovate niente?", "È la notizia migliore, e te la diamo per iscritto: avrai la mappa completa dei tuoi sistemi e la certezza di dove sei."),
    ],
    "check_k": "Ti riguarda se",
    "check_h": "Due sì bastano per <em>parlarne</em>.",
    "check": [
        "Il sito o l'app hanno qualche anno e da allora nessuno li ha più ricontrollati",
        "I clienti lasciano dati, documenti o pagamenti in un modulo o in un'area riservata",
        "Hai costruito qualcosa con l'intelligenza artificiale e l'hai messo online",
        "Un chatbot o un agente AI legge le tue email, i tuoi documenti o il tuo CRM",
        "Persone che non lavorano più con te potrebbero avere ancora un accesso",
        "Non sapresti dire quando è stato fatto l'ultimo backup, né se si ripristina davvero",
    ],
    "check_a": "Fai il check gratuito",
    "check_note": "Tre minuti, gratis: livello di esposizione, cosa si vede dal tuo dominio e 3 priorità.",
    "box_h": "Gli attacchi sono già <em>automatici</em>.",
    "box_p": "Agenti e bot lavorano giorno e notte su tutto ciò che hai online. Mettiamo al sicuro quello che hai già, quello che costruisci con l'AI e gli agenti che usi.",
    "box_a": "Scopri la sicurezza",
    "alt_contact": "Preferisci scriverci? Vai ai contatti",
    "need": "Sicurezza di siti, app e agenti AI",
}
T["it"]["check"] = {
    "title": "Check di esposizione gratuito · Reef 7 Lab",
    "desc": "In 3 minuti scopri cosa vede chi attacca dal tuo dominio, il tuo livello di esposizione e le 3 priorità da cui partire.",
    "k": "Check di esposizione", "h1": "Quanto è <em>esposta</em> la tua azienda?",
    "sub": "Guardiamo il tuo dominio come lo vede chi attacca, con controlli pubblici e non invasivi, e ti facciamo poche domande mirate. Ricevi il tuo livello di esposizione e le 3 priorità da cui partire, con cosa puoi fare già oggi.",
    "pts": ["3 minuti", "Controlli veri sul tuo dominio", "Gratis, senza impegno"],
}
T["en"]["security"] = {
    "title": "Cybersecurity for websites, apps and AI agents · Reef 7 Lab",
    "k": "Cybersecurity for SMBs",
    "desc": "Attacks are already automated. We secure websites, apps and internal tools, new and old, and the AI agents you use: review, fixes and continuous watch.",
    "h1": "Attacks are already <em>automated</em>. Are your defences?",
    "sub": "Enter your domain: in 3 minutes you'll see what an attacker sees, how exposed you are and what to fix first. Free, nothing to install.",
    "feed": {"k": "Simulation · automated attack", "live": "in progress", "dom": "yourcompany.com", "rows": [["03:12:04", "Bot", "tries 2,400 stolen passwords on your login", "bad"], ["03:12:41", "AI agent", "looks for plugins and PHP versions with known flaws", "bad"], ["03:13:09", "Scanner", "knocks on 380 hidden addresses of your site", "mid"], ["03:13:55", "Scam", "\"we've changed our bank details\" emailed to your customers, in your name", "bad"], ["03:14:20", "Bot", "copies your price list and customer contacts", "mid"]], "q": "Your defences?", "a": "Find out in 3 minutes"},
    "dom_ph": "yourcompany.com",
    "dom_btn": "Check for free",
    "dom_note": "Public data only. No intrusive tests, no commitment.",
    "route_k": "Where to start",
    "route_h": "What's <em>your situation</em>?",
    "route_p": "Pick your case: the check starts already set up.",
    "routes": [
        ("old", "We've had a website or online store for a few years", "WordPress, plugins, internal tools: that's where automated attacks look first.", "Check your site"),
        ("ai", "We built a site or app with AI", "It works. But has anyone checked who can read the data?", "Check your project"),
        ("agent", "We use chatbots or AI agents", "They read email, documents and CRMs. Let's see what they can do, and what they can't.", "Check your agents"),
        ("inc", "Something strange has happened", "Suspicious emails, logins you don't recognise, an altered site: write to us and we'll start right away.", "Write to us now"),
    ],
    "get_h": "What you get <em>in 3 minutes</em>",
    "get_p": "A clear report, written for decision makers.",
    "get": [
        "Your exposure level: low, medium, high or critical",
        "What an attacker sees from your domain: site protections and email in your name",
        "The 3 priorities to start from, with what you can do today on your own",
        "A copy of the report by email, and my reply within one working day",
    ],
    "fix_h": "What we <em>fix</em>",
    "fix_p": "Only where needed. No rebuild, no downtime.",
    "fix_more": "What's included",
    "end_h": "The first step takes <em>3 minutes</em>.",
    "end_p": "Enter your domain. If you then want to talk, I'll reply within a day.",
    "now_k": "Why now",
    "now_h": "The time to react <em>has shrunk</em>.",
    "now": [
        ("7 in 10", "websites run on PHP, the language in which an AI found critical flaws on October 21, 2026.", "AP / PBS NewsHour", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
        ("Hours", "between the announcement of those flaws and the first millions of attack attempts.", "AP / PBS NewsHour", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
        ("51%", "of web traffic is now automated: bots and agents, not people.", "Imperva, Bad Bot Report 2025", "https://www.imperva.com/blog/2025-imperva-bad-bot-report-how-ai-is-supercharging-the-bot-threat/"),
    ],
    "now_end": "No need to panic. Just move first.",
    "loss_k": "What's really at stake",
    "loss_h": "You're not risking your website. <em>You're risking money.</em>",
    "loss_p": "To an attacker, your website is just the door. What they're after is your money, your data and your customers.",
    "losses": [
        ("money", "A payment to the wrong account", "An email arrives from your supplier, from their real address: \"we've changed our bank details\". You pay. No virus, just one hacked inbox, and that money doesn't come back."),
        ("bank", "Your bank and payments in someone else's hands", "From your email, someone can reset the passwords for your bank, Stripe, PayPal and marketplaces. Usually one reused password without two-factor login is enough."),
        ("data", "Your customers' data up for sale", "A copied customer list can't be recovered. And GDPR allows fines of up to 20 million euros or 4% of worldwide turnover, with 72 hours to notify the authority."),
        ("lock", "Your business stopped, waiting on a ransom", "Overnight, files, systems and backups become unreadable. Whoever encrypted them demands a ransom, and paying guarantees nothing. Every day offline is lost revenue."),
        ("users", "Your customers scammed in your name", "Fake invoices sent from your domain, a tampered checkout copying cards. Your customers lose the money; you lose their trust."),
        ("alert", "Your reputation burned in a day", "Scam pages on your site, Google flagging it as dangerous, reviews full of angry customers. It takes hours to burn, years to rebuild."),
    ],
    "loss_src": ("GDPR, Articles 33 and 83", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679"),
    "loss_cta": "Find out what you risk: take the free check",
    "scan": {"k": "Sample check", "dom": "yourcompany.com", "live": "analysis complete", "rows": [
            ("Site protections", "F", "bad"),
            ("Email in your name", "Not protected", "bad"),
            ("Platform", "PHP needs updating", "mid"),
            ("Access", "2 former staff still active", "mid"),
        ], "lvl": "Exposure", "lvl_v": "High", "prio": "3 priorities ready in the report"},
    "check_hint": "Tick what applies to you",
    "check_ok": "Worth a conversation. The free check tells you where to start.",
    "gain_h": "What you <em>get</em>",
    "gain_p": "Not a document for a drawer: results you can see.",
    "gains": [
        ("You know where you're exposed", "A clear map of everything visible from outside and what each risk is worth, written for decision makers."),
        ("Serious flaws closed first", "We start with what puts money and data at risk. The rest follows a plan with precise timelines."),
        ("Nothing to rebuild, nothing to stop", "We work on what you already have, on copies or after hours. Your team keeps working as usual."),
        ("Someone on watch, always", "Monitoring, updates and one report a month. You run the business, we handle the rest."),
    ],
    "start_h": "How to <em>start</em>",
    "start_p": "Three steps. The first two are free.",
    "start": [
        ("Exposure check", "Free · 3 minutes", "Enter your domain and instantly get your exposure level and 3 priorities."),
        ("Review call", "Free · 30 minutes", "We go through the result together: what to do, in what order, how long it takes."),
        ("The work", "Written proposal", "Work, timelines and costs in writing before we start. No surprises."),
    ],
    "start_promise": "If the review shows nothing worth improving, we'll tell you. And that's it.",
    "sub_src": ("Source: AP / PBS NewsHour, October 2026", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
    "alert_k": "October 21, 2026",
    "alert_h": "An AI found critical flaws in the language behind 7 in 10 websites. <em>Within hours, millions of attack attempts.</em>",
    "alert_p": "The flaws were in PHP, the language behind WordPress, most online stores and countless internal tools: they let attackers take control of the server remotely. The FBI advised taking offline any site that couldn't be updated right away. Japan, the UK and Finland took parts of their public services offline.",
    "alert_pts": [
        ("What happened", "An AI found critical flaws in PHP: they let attackers take control of the server remotely."),
        ("Who it affects", "Anyone with a WordPress site, an online store or a web-based internal tool: about 7 in 10 websites."),
        ("What to do", "Check right away that your site is updated. The FBI advised taking offline any site that isn't."),
    ],
    "alert_q": "Does your site run on PHP? Is it already updated?",
    "alert_a": "Find out with the exposure check",
    "alert_src": ("AP / PBS NewsHour, October 22, 2026", "https://pbs.org/newshour/nation/ai-discovered-a-software-vulnerability-that-could-impact-70-of-websites-worldwide-the-rush-is-on-to-patch-it"),
    "b1": "Take the free check",
    "b2": "How we work",
    "risks_h": "What has <em>changed</em>",
    "risks_p": "In a matter of weeks, attacking became software that works on its own. Much of what is online was designed for a slower web.",
    "risks": [
        ("Hours between discovery and attack", "A flaw that sat in the code for over a decade was found by an AI, and within hours of the announcement millions of attempts to exploit it began. Updating next week means arriving too late. You don't choose whether to be a target: being online is enough."),
        ("Shipped before it's checked", "An AI-generated app goes live in a weekend. Access rules, keys and permissions have often never been looked at by anyone."),
        ("Assistants hold the house keys", "Chatbots and agents read email, documents and CRMs, and they can act. You don't need to hack them to manipulate them: you just write the right thing in the right place."),
    ],
    "cases_k": "Why not wait",
    "cases_h": "Not theory. <em>Headlines.</em>",
    "cases_p": "Public cases, with sources. All avoidable.",
    "cases": [
        ("September 2025", "An AI attacked 30 organisations. Almost on its own.", "A state-sponsored group used an AI agent to carry out 80-90% of the operational work on its own against around thirty organisations: reconnaissance, vulnerability hunting, credential theft.", "A team of attackers' work, done by a machine.", "Anthropic", "https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf"),
        ("August 2025", "One chatbot breached. Hundreds of company CRMs copied.", "Using access tokens stolen from a sales chatbot integration, attackers pulled data from the CRMs of more than 700 organisations, including security companies, hunting for keys and passwords.", "Every tool connected to your data is one more door.", "TechTarget", "https://www.techtarget.com/cybersecurity/news/366630934/News-brief-Salesloft-Drift-breach-update-and-timeline"),
        ("June 2025", "No clicks. One email was enough to leak the data.", "A single crafted email was enough to make a widely used enterprise AI assistant send internal data to an outside server, without the user clicking anything. Fixed before it was exploited.", "To an AI assistant, even an email is an order.", "BleepingComputer", "https://www.bleepingcomputer.com/news/security/zero-click-ai-data-leak-flaw-uncovered-in-microsoft-365-copilot/"),
        ("2025", "Built with AI. One in ten left everything open.", "Out of 1,645 apps published with a well-known AI app builder, researchers found 170 that let anyone read users, payments or keys.", "Working is not the same as protected.", "Superblocks", "https://www.superblocks.com/blog/lovable-vulnerabilities"),
        ("July 2025", "13,000 ID documents. Open to anyone.", "A dating app exposed around 72,000 images, including 13,000 selfies and ID documents, from a storage space reachable from outside.", "One wrong setting is enough.", "CyberInsider", "https://cyberinsider.com/tea-app-suffers-data-breach-exposing-72000-users-photos-and-private-messages/"),
        ("July 2025", "The password was 123456. Behind it, up to 64 million applications.", "The chatbot hiring platform used by a major fast-food chain had a test panel protected by 123456, with no two-factor login: data from up to 64 million job applications was open.", "A forgotten panel is an open service entrance.", "BleepingComputer", "https://www.bleepingcomputer.com/news/security/123456-password-exposed-chats-for-64-million-mcdonalds-job-chatbot-applications/"),
    ],
    "areas": [
        ("What is already online", "What you <em>already have</em>", "The website from five years ago, the custom internal tool, the store with plugins never updated: the first places automated attacks look. We harden them without rebuilding.", ["36", "35"]),
        ("The AI you use", "AI, <em>without surprises</em>", "AI-generated sites and apps, chatbots and agents connected to your data: we check what they can read and do, and set clear boundaries.", ["32", "33", "34"]),
        ("People and email", "People <em>and email</em>", "Often no flaw is needed: a forgotten login or an email that looks real is enough. We close that door too.", ["37", "38"]),
    ],
    "steps_h": "How we <em>work</em>",
    "steps_p": "Four phases, always authorised by you in writing.",
    "steps": [
        ("Discovery", "We map everything visible from outside: domains, pages, forms, APIs, logins and integrations. It's often the first complete map the company has ever had."),
        ("Simulated attack", "We try to get in with today's techniques, including automated ones and those aimed at AI agents. Every flaw is demonstrated, not assumed."),
        ("Hardening", "We close the gaps by severity and explain what we changed, in plain words."),
        ("Continuous watch", "Attack techniques change every month. We monitor, update and repeat checks at every significant change."),
    ],
    "faq_h": "The questions <em>we get</em>",
    "faq": [
        ("We're small: who would bother attacking us?", "Nobody picks you. Automated attacks try everything that's online, regardless of who you are. Small companies are often the easiest: nobody is watching them."),
        ("A serious agency built our website.", "On delivery day it was probably fine. Since then the components, the attack techniques and who has access have all changed. Security isn't a one-off test: it's maintenance."),
        ("We use well-known platforms, they take care of it.", "They protect their servers. Settings, access, data and integrations stay with you: that's where almost every headline starts."),
        ("Will we have to stop working?", "No. Every test is authorised in writing and runs on copies or at agreed times."),
        ("What if you find nothing?", "That's the best news, and we put it in writing: you get a complete map of your systems and certainty about where you stand."),
    ],
    "check_k": "This is for you if",
    "check_h": "Two yeses are <em>enough to talk</em>.",
    "check": [
        "Your website or app is a few years old and nobody has checked it since",
        "Customers leave data, documents or payments in a form or a private area",
        "You built something with AI and put it online",
        "A chatbot or AI agent reads your email, your documents or your CRM",
        "People who no longer work with you might still have access",
        "You couldn't say when the last backup was made, or whether it really restores",
    ],
    "check_a": "Take the free check",
    "check_note": "Three minutes, free: exposure level, what's visible from your domain and 3 priorities.",
    "box_h": "Attacks are already <em>automated</em>.",
    "box_p": "Agents and bots work day and night on everything you have online. We secure what you already have, what you build with AI and the agents you use.",
    "box_a": "Explore security",
    "alt_contact": "Prefer to write to us? Go to contact",
    "need": "Security for websites, apps and AI agents",
}
T["en"]["check"] = {
    "title": "Free exposure check · Reef 7 Lab",
    "desc": "In 3 minutes, see what an attacker sees from your domain, your exposure level and the 3 priorities to start from.",
    "k": "Exposure check", "h1": "How <em>exposed</em> is your business?",
    "sub": "We look at your domain the way an attacker sees it, with public, non-intrusive checks, and ask a few focused questions. You get your exposure level and the 3 priorities to start from, with what you can do today.",
    "pts": ["3 minutes", "Real checks on your domain", "Free, no commitment"],
}


def eco(H, pre):
    """Sezione 'Un unico sistema': gli strumenti dell'azienda attorno a un unico centro, con i dati che scorrono."""
    values = "".join(f"<li>{v}</li>" for v in H["values"])
    # sei strumenti disposti in cerchio attorno al centro
    import math
    nodes, lines = "", ""
    for i, (label, ico) in enumerate(H["eco_nodes"]):
        ang = -math.pi / 2 + i * 2 * math.pi / len(H["eco_nodes"])
        x, y = 50 + 38 * math.cos(ang), 50 + 38 * math.sin(ang)
        nodes += f'<span class="hub-node" style="left:{x:.1f}%;top:{y:.1f}%"><i aria-hidden="true">{ico}</i>{label}</span>'
        lines += f'<line x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}"/><circle class="pulse" r=".9" style="--x:{x - 50:.1f}px;--y:{y - 50:.1f}px;animation-delay:{i * .45:.2f}s" cx="50" cy="50"/>'
    return f"""<div class="eco3">
    <div class="eco-copy">
      <p class="mono">{H['eco_k']}</p>
      <h2>{H['eco_h']}</h2>
      <p class="eco-lead">{H['eco_p']}</p>
      <ul class="eco-values">{values}</ul>
    </div>
    <div class="hubviz" aria-hidden="true">
      <svg viewBox="0 0 100 100" class="hub-lines"><circle cx="50" cy="50" r="38" class="ring"/>{lines}</svg>
      {nodes}
      <span class="hub-core"><img src="{pre}assets/logo-88.png" alt="" width="44" height="44"><b>{H['eco_core']}</b></span>
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
        links = "".join(f'<a href="{u(k)}" title="{L["nav_d"][k]}"{" aria-current=\"page\"" if k == key else ""}><span class="nav-l">{L["nav"][k]}</span><span class="nav-d">{L["nav_d"][k]}</span></a>' for k in NAV)
        cur = ' aria-current="page"' if key == "contact" else ""
        foot_links = "".join(f'<a href="{u(k)}">{L["nav"][k]}</a>' for k in NAV + ["contact"])
        alt = f"{alt_dir}{SLUG[other][key]}"
        # sulle pagine di vendita della sicurezza resta una sola azione: niente fascia generica
        band = "" if key in ("contact", "security", "check") else f"""
<section class="cta-band"><div class="wrap"><a href="{u('contact')}">
  <div><p class="mono">{L['cta_k']}</p><h2>{L['cta_h']}</h2></div><span class="circle" aria-hidden="true">→</span>
</a></div></section>"""
        inline_js = INLINE_JS % (EMAIL, AGENT_URL)
        url_of = lambda lg, k: SITE_URL + ("" if lg == "it" else "en/") + ("" if k == "home" else SLUG[lg][k])
        self_url, other_url, it_url = url_of(lang, key), url_of(other, key), url_of("it", key)
        jsonld = ""
        if key == "home" and not variant:
            import json as _json
            data = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Reef 7 Lab", "url": SITE_URL, "logo": SITE_URL + "assets/reef7-logo.png",
                    "image": SITE_URL + "assets/og-card.jpg", "email": EMAIL, "description": desc, "areaServed": "IT", "knowsLanguage": ["it", "en", "es", "de", "zh"],
                    "founder": {"@type": "Person", "name": "Alessandro Lancioni", "jobTitle": "Founder", "image": SITE_URL + "assets/alessandro.jpg"}}
            jsonld = '\n  <script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>"
        return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  {csp_meta(inline_js)}
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#04080f">
  <link rel="canonical" href="{self_url}">
  <link rel="alternate" hreflang="{lang}" href="{self_url}">
  <link rel="alternate" hreflang="{other}" href="{other_url}">
  <link rel="alternate" hreflang="x-default" href="{it_url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Reef 7 Lab">
  <meta property="og:locale" content="{'it_IT' if lang == 'it' else 'en_US'}">
  <meta property="og:url" content="{self_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE_URL}assets/og-card.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">{jsonld}
  <link rel="icon" href="{pre}assets/favicon.png">
  <link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}{css}?v={VERSION}">
</head>
<body data-page="{key}" data-build="{BUILD}">
<a class="skip" href="#main">{"Salta al contenuto" if lang == "it" else "Skip to content"}</a>
<header class="top{'' if hero else ' solid'}"><div class="wrap top-in">
  <a class="logo" href="{u('home')}"><img src="{pre}assets/logo-68.png" alt="" width="34" height="34">Reef 7 Lab</a>
  <nav aria-label="{L['pages']}">{links}<a href="{u('contact')}" class="cta" title="{L['nav_d']['contact']}"{cur}><span class="nav-l">{L['nav']['contact']}</span><span class="nav-d">{L['nav_d']['contact']}</span></a></nav>
  <a class="lang" href="{alt}" hreflang="{other}" lang="{other}">{other.upper()}</a>
  <button class="menu" aria-expanded="false" data-close="{L['close']}">{L['menu']}</button>
</div></header>
<main id="main">
{body}
</main>{band}
<footer class="foot"><div class="wrap foot-in">
  <span>{L['foot']}</span>
  <nav aria-label="{L['pages']}">{foot_links}</nav>
  <a class="r" href="mailto:{EMAIL}">{EMAIL}</a>
</div></footer>
<script>{inline_js}</script>
<script src="{pre}site.js?v={VERSION}"></script>
<script src="{pre}agent.js?v={VERSION}"></script>{extra}
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
        bar = f'<div class="fr-bar"><i></i><i></i><i></i><span>{w.get("bar") or w["url"].replace("https://", "") if w["url"] and w["url"].startswith("http") else "reef7lab · " + p["name"]}</span></div>'
        if kind == "browser":
            return f'<div class="fr fr-browser">{bar}<iframe src="{w["src"] if w["src"].startswith("http") else pre + w["src"]}" title="{p["name"]}" loading="lazy"></iframe></div>'
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
        is_demo = w["key"] in ("crmdemo", "hubdemo", "maisenzagioie3d")
        open_t = W["open"]["phone"] if is_demo else W["open"].get(w["frame"], "")
        link = f'<a class="link" href="{href}" target="_blank" rel="noopener">{open_t} ↗</a>' if href else ""
        return f"""<article class="project" id="{w['key']}">
  <div class="project-info">
    <span class="mono">{i:02d} · {W['hint_demo'] if w['key'] in ("crmdemo", "hubdemo", "maisenzagioie3d") else W['hint'][w['frame']]}</span>
    <h2>{p['name']}</h2>
    <p class="project-lead">{p['lead']}</p>
    <p>{p['text']}</p>
    <ul class="project-points">{"".join(f"<li>{x}</li>" for x in p['points'])}</ul>
    <dl class="project-meta"><div><dt>{lb['client']}</dt><dd>{p['client']}</dd></div><div><dt>{lb['type']}</dt><dd>{p['type']}</dd></div><div><dt>{lb['year']}</dt><dd>{p['year']}</dd></div></dl>
    {link}
    <p class="project-note">{p['note']}</p>
  </div>
  <div class="project-frame">{frame(w)}{f'<a class="pf-thumb" href="{href}" target="_blank" rel="noopener"><img src="{pre}{w["thumb"]}"{img_dims(w["thumb"])} alt="{p["name"]}" loading="lazy"><span>{open_t} ↗</span></a>' if href and w.get("thumb") else (f'<span class="pf-thumb"><img src="{pre}{w["thumb"]}"{img_dims(w["thumb"])} alt="{p["name"]}" loading="lazy"></span>' if w.get("thumb") else "")}</div>
</article>"""

    def work_card(w):
        p = W["projects"][w["key"]]
        img = f'<img src="{pre}{w["thumb"]}"{img_dims(w["thumb"])} alt="" loading="lazy">' if w["thumb"] else tenka_mock()
        return f'<a class="work-card2" href="{u("work")}#{w["key"]}"><div class="wc-img">{img}</div><div class="wc-meta"><h3>{p["name"]}</h3><p>{p["type"]}</p></div></a>'

    work_cards = "".join(work_card(w) for w in WORK)
    # home: solo tre progetti in evidenza, uno grande e due affiancati
    # home: una sola riga di quattro progetti
    HOME_WORK = ["crmdemo", "tenka", "fullpeak", "maisenzagioie3d"]
    FEAT = ["maisenzagioie3d", "tenka", "fullpeak"]
    FEAT_IMG = {"maisenzagioie3d": "assets/work/feat-maisenzagioie3d.jpg"}
    def feat_card(i, key):
        w = next(x for x in WORK if x["key"] == key)
        p = W["projects"][key]
        return f"""<a class="feat-card" href="{u('work')}#{key}"><img src="{pre}{FEAT_IMG.get(key, w['thumb'])}"{img_dims(FEAT_IMG.get(key, w['thumb']))} alt="" loading="lazy">
      <span class="feat-n mono">0{i}</span>
      <div class="feat-meta"><div><h3>{p['name']}</h3><p>{p['type']}</p></div><span class="feat-go" aria-hidden="true">→</span></div></a>"""
    feat_cards = "".join(feat_card(i, k) for i, k in enumerate(FEAT, 1))
    partners = "".join(f'<div class="partner"><span class="partner-tag">{tag}</span><b class="partner-name">{n}</b><span class="partner-what">{w}</span><p>{d}</p></div>' for n, tag, w, d in W["partners"])
    cq, ca = W["partners_cta"]
    CS = W["case"]
    partners_html = f"""<section class="block partners-block"><div class="wrap partners-in">
  <div><p class="mono">{W['partners_k']}</p><h2>{W['partners_h']}</h2><p class="partners-p">{W['partners_p']}</p>
    <p class="partners-cta">{cq} <a class="link" href="{u('contact')}">{ca} {arrow}</a></p></div>
  <div class="partners">{partners}</div>
</div></section>"""
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    stat = lambda xs, tag="small": "".join(f'<div><b>{a}</b><span>{b}</span><{tag}>{c}</{tag}></div>' for a, b, c in xs)
    case_home = f"""<section class="block case-block"><div class="wrap"><div class="pcase">
  <div class="case-head"><p class="mono">{CS['k']}</p><h2>{CS['h']}</h2><p>{CS['p']}</p></div>
  <div class="case-kpis">{stat(CS['kpis'])}</div>
  <div class="case-ba"><div class="ba-b"><p class="mono">{CS['before_k']}</p><ul>{li(CS['before'])}</ul></div><span class="ba-arrow" aria-hidden="true">→</span><div class="ba-a"><p class="mono">{CS['after_k']}</p><ul>{li(CS['after'])}</ul></div></div>
  <a class="link" href="{u('work')}#caso-abf" style="margin-top:26px">{CS['more']} {arrow}</a>
</div></div></section>"""
    F = CS["full"]
    case_full = f"""<section class="block cs" id="caso-abf"><div class="wrap">
  <header class="cs-head"><p class="mono">{F['k']}</p><h2>{F['h']}</h2><p class="cs-lead">{F['lead']}</p>
    <dl class="cs-facts">{"".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in F['facts'])}</dl></header>
  <div class="cs-res"><p class="mono">{F['res_k']}</p><div class="case-hero">{stat(F['res'], "p")}</div><div class="case-kpis cs-k3">{stat(F['res2'])}</div></div>
  <div class="cs-body">
    <div class="cs-text">{"".join(f"<section><h3>{t}</h3>{''.join(f'<p>{x}</p>' for x in ps)}</section>" for t, ps in F['ch'])}</div>
    <aside class="cs-side">
      <div class="cs-box"><p class="mono">{F['steps_k']}</p><ol class="cs-steps">{"".join(f"<li><b>{d}</b><span>{t}</span></li>" for d, t in F['steps'])}</ol></div>
      <div class="cs-box"><p class="mono">{F['replaced_k']}</p><ul class="cs-tags">{"".join(f"<li>{x}</li>" for x in F['replaced'])}</ul></div>
    </aside>
  </div>
  <p class="case-src">{F['src']}</p>
  <p class="cs-cta">{F['cta'][0]} <a class="link" href="{u('contact')}">{F['cta'][1]} {arrow}</a></p>
</div></section>"""
    out["work"] = page("work", W["title"], W["desc"], head_block(L["nav"]["work"], W["h1"], W["sub"]) + f"""
<section class="wrap projects">{"".join(project(i, w) for i, w in enumerate(WORK, 1))}
</section>
{case_full}
{partners_html}""")

    # home
    H = L["home"]
    rows = "".join(f"""
    <a class="svc-row" href="{u('security') if g == L['nav']['security'] else u('services')}#s{n}"><span class="mono">{g}</span><h3>{t}</h3><p>{d}</p><span class="go" aria-hidden="true">→</span></a>""" for n, g, t, d, *_ in L["services"] if n in ("31", "11", "28", "36", "10", "06", "20"))
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
<section class="block au-promo-block"><div class="wrap"><a class="au-promo" href="{u('audit')}">
  <div class="au-promo-txt"><p class="mono">{L['audit']['home_k']} · {L['audit']['home_k2']}</p><h2>{L['audit']['home_h']}</h2><p>{L['audit']['home_p']}</p>
    <span class="btn">{L['audit']['home_a']} {arrow}</span></div>
  <div class="au-promo-vis" aria-hidden="true"><div class="apv">
    <p class="mono">{L['audit']['vis_k']}</p>
    <div class="apv-num"><b>{str(sum(h for _, h in L['audit']['vis'])).replace('.', ',' if lang == 'it' else '.')}</b><span>{L['audit']['vis_u']}</span></div>
    {"".join(f'<div class="apv-row"><span>{t}</span><em>{str(h).replace(".", "," if lang == "it" else ".")}</em><i><b style="width:{h / 8 * 100:.0f}%"></b></i></div>' for t, h in L['audit']['vis'])}
  </div></div>
</a></div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{W['home_h']}</h2><p>{W['home_p']}</p></div>
  <div class="work-grid">{"".join(work_card(next(x for x in WORK if x["key"] == k)) for k in HOME_WORK)}</div>
  <a class="link" href="{u('work')}">{W['home_a']} ({len(WORK)}) {arrow}</a>
</div></section>
{partners_html}
{case_home}
<section class="block founder-block"><div class="wrap founder">
  <img class="founder-img" src="{pre}assets/alessandro.jpg" alt="{L['studio']['photo_alt']}" width="1024" height="1024" decoding="async">
  <div class="founder-txt"><p class="mono">{L['founder']['k']}</p><h2>{L['founder']['h']}</h2><p class="founder-p">{L['founder']['p']}</p>
    <ul class="founder-pts">{"".join(f"<li><b>{k}</b><span>{v}</span></li>" for k, v in L['founder']['points'])}</ul>
    <div class="founder-act"><a class="btn" href="{u('contact')}">{L['founder']['cta']} <span class="arr">→</span></a><a class="link" href="{u('studio')}">{L['founder']['a']} {arrow}</a></div>
    <p class="founder-risk">{L['founder']['risk']}</p></div>
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
<section class="block"><div class="wrap">
  <div class="head"><h2>{H['reef_h']}</h2><p>{H['reef_p']}</p></div>
  <div class="principles">{reef_words}</div>
  <a class="link" href="{u('studio')}">{H['reef_a']} {arrow}</a>
</div></section>
<section class="block ocean"><div class="wrap ocean-in">
  <div><p class="mono">{M['home_k']}</p><h2>{M['home_h']}</h2><p class="ocean-p">{M['home_p']}</p>
    <a class="link" href="{u('mission')}">{M['home_a']} {arrow}</a></div>
  <div class="goals">{goal_card(active)}</div>
</div></section>""", hero=True)

    # servizi
    SP = L["services_p"]
    # servizi divisi per gruppo: un'etichetta all'inizio di ogni gruppo
    svc, last, i = "", None, 0
    SEC = L["security"]
    sicurezza = [x for x in L["services"] if x[1] == L["nav"]["security"]]
    for (n, g, t, short, long, li) in L["services"]:
        if g != last:
            svc += f'\n  <p class="svc-group mono">{g}</p>'
            last = g
            if g == L["nav"]["security"]:
                i += 1
                svc += f"""
  <article class="svc sec-box" id="sicurezza">
    <span class="mono">{i:02d}</span>
    <div><h2>{SEC['box_h']}</h2><p class="lead">{SEC['box_p']}</p>
      <a class="btn" href="{u('security')}">{SEC['box_a']} {arrow}</a></div>
    <div><ul class="sec-links">{"".join(f'<li><a href="{u("security")}#s{x[0]}">{x[2]}</a></li>' for x in sicurezza)}</ul></div>
  </article>"""
        if g == L["nav"]["security"]:
            continue
        i += 1
        svc += f"""
  <article class="svc" id="s{n}">
    <span class="mono">{i:02d}</span>
    <div><h2>{t}</h2><p class="tag">{short}</p><p class="lead">{long}</p></div>
    <div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
  </article>"""
    out["services"] = page("services", SP["title"], SP["desc"], head_block(L["nav"]["services"], SP["h1"], SP["sub"]) + f"""
<section class="wrap" style="padding-bottom:clamp(80px,10vw,150px)">{svc}
</section>""")

    # sicurezza: pagina di vendita con esempio di report, servizi a schede, metodo a tappe e lista interattiva
    SE = L["security"]
    per_n = {x[0]: x for x in L["services"]}
    ICO = {
        "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
        "shield": '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
        "flow": '<path d="M4 12h12"/><path d="m12 6 6 6-6 6"/><path d="M20 5v14"/>',
        "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 10v4M18 10v4"/>',
        "bank": '<path d="M3 10 12 4l9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
        "data": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
        "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c2 .7 3.2 2.5 3.5 5.2"/>',
        "alert": '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17.5v.01"/>',
    }
    ico = lambda k: f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICO[k]}</svg>'
    titolo = lambda t: (lambda x: f"{x[0]}. <em>{x[1]}</em>" if len(x) == 2 else t)(t.split(". ", 1))
    casi = "".join(f"""
    <article class="sec-caso"><p class="mono">{q}</p><h3>{titolo(t)}</h3><p>{d}</p><p class="sec-lez">{lz}</p><a href="{url}" target="_blank" rel="noopener">{fonte} ↗</a></article>""" for q, t, d, lz, fonte, url in SE["cases"])
    more = "Come lavoriamo" if lang == "it" else "How we do it"
    aree, k_svc = "", 0
    for j, (k, h, d, nums) in enumerate(SE["areas"], 1):
        cards = ""
        for n in nums:
            k_svc += 1
            _n, _g, t, short, long, li = per_n[n]
            cards += f"""
    <article class="sec-svc" id="s{n}">
      <span class="mono">{k_svc:02d}</span>
      <h3>{t}</h3><p class="sec-svc-tag">{short}</p>
      <ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>
      <details><summary>{more}</summary><p>{long}</p></details>
    </article>"""
        aree += f"""
<section class="block sec-area"><div class="wrap">
  <div class="head"><div><p class="mono sec-k">0{j} / 0{len(SE["areas"])}</p><h2>{h}</h2></div><p>{d}</p></div>
  <div class="sec-svcs n{len(nums)}">{cards}
  </div>
</div></section>"""
    fasi = "".join(f'<li><span class="sec-step-n">{i}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(SE["steps"], 1))
    faq = "".join(f'<details class="sec-faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in SE["faq"])
    ora = "".join(f'<div><b>{n}</b><p>{d}</p><a href="{url}" target="_blank" rel="noopener">{src} ↗</a></div>' for n, d, src, url in SE["now"])
    guadagni = "".join(f'<div class="sec-gain"><i>{ico(k)}</i><b>{t}</b><p>{d}</p></div>' for k, (t, d) in zip(["map", "shield", "flow", "eye"], SE["gains"]))
    inizio = "".join(f'<li><span class="mono">0{i}</span><b>{t}</b><em>{k}</em><p>{d}</p></li>' for i, (t, k, d) in enumerate(SE["start"], 1))
    SC = SE["scan"]
    righe = "".join(f'<div class="sec-scan-r {c}" style="--d:{0.5 + i * 0.45}s"><span>{a}</span><b>{v}</b></div>' for i, (a, v, c) in enumerate(SC["rows"]))
    FD = SE["feed"]
    log = "".join(f'<li class="{c}" style="--d:{0.4 + i * 0.55}s"><time class="mono">{t}</time><b>{w}</b><span>{x}</span></li>' for i, (t, w, x, c) in enumerate(FD["rows"]))
    hero = f"""<section class="page-head sec-hero"><div class="wrap sec-hero-g">
  <div>
    <p class="mono">{SE['k']}</p>
    <h1>{SE['h1']}</h1>
    <p class="sub">{SE['sub']}</p>
    <form class="sec-dom" action="{u('check')}" method="get">
      <label class="sr-only" for="dom-top">{SE['dom_ph']}</label>
      <input id="dom-top" name="d" type="text" inputmode="url" autocomplete="url" required maxlength="200" placeholder="{SE['dom_ph']}">
      <button class="btn" type="submit">{SE['dom_btn']} {arrow}</button>
    </form>
    <p class="sec-dom-note">{SE['dom_note']}</p>
  </div>
  <a class="sec-feed" href="{u('check')}" aria-label="{FD['a']}">
    <div class="sec-feed-top"><span class="sec-scan-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="mono">{FD['k']}</span><span class="sec-feed-live mono"><span class="sec-dot" aria-hidden="true"></span>{FD['live']}</span></div>
    <p class="sec-feed-dom mono">→ {FD['dom']}</p>
    <ol class="sec-feed-log">{log}</ol>
    <div class="sec-feed-end" style="--d:{0.4 + len(FD['rows']) * 0.55}s"><b>{FD['q']}</b><span>{FD['a']} →</span></div>
  </a>
</div></section>"""
    perdite = "".join(f'<div class="sec-loss"><i>{ico(k)}</i><b>{t}</b><p>{d}</p></div>' for k, t, d in SE["losses"])
    out["security"] = page("security", SE["title"], SE["desc"], hero + f"""
<section class="sec-alert"><div class="wrap">
  <p class="mono"><span class="sec-dot" aria-hidden="true"></span>{SE['now_k']} · {SE['alert_k']}</p>
  <h2>{SE['alert_h']}</h2>
  <div class="sec-alert-b"><dl class="sec-alert-pts">{"".join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in SE['alert_pts'])}</dl>
    <div class="sec-alert-cta"><b>{SE['alert_q']}</b><a class="btn" href="{u('check')}">{SE['alert_a']} {arrow}</a><a class="sec-alert-src" href="{SE['alert_src'][1]}" target="_blank" rel="noopener">{SE['alert_src'][0]} ↗</a></div></div>
</div></section>
<section class="block sec-losses-b"><div class="wrap">
  <div class="head"><div><p class="mono sec-k">{SE['loss_k']}</p><h2>{SE['loss_h']}</h2></div><p>{SE['loss_p']}</p></div>
  <div class="sec-losses">{perdite}</div>
  <div class="sec-losses-end"><a class="btn" href="{u('check')}">{SE['loss_cta']} {arrow}</a><a class="sec-alert-src" href="{SE['loss_src'][1]}" target="_blank" rel="noopener">{SE['loss_src'][0]} ↗</a></div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{SE['gain_h']}</h2><p>{SE['gain_p']}</p></div>
  <div class="sec-gains">{guadagni}</div>
</div></section>{aree}
<section class="block" id="metodo"><div class="wrap">
  <div class="head"><h2>{SE['steps_h']}</h2><p>{SE['steps_p']}</p></div>
  <ol class="sec-steps">{fasi}</ol>
</div></section>
<section class="block" id="casi"><div class="wrap">
  <div class="head"><div><p class="mono sec-k">{SE['cases_k']}</p><h2>{SE['cases_h']}</h2></div><p>{SE['cases_p']}</p></div>
  <div class="sec-casi">{casi}
  </div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{SE['start_h']}</h2><p>{SE['start_p']}</p></div>
  <ol class="sec-start">{inizio}</ol>
  <div class="sec-start-end"><a class="btn" href="{u('check')}">{SE['b1']} {arrow}</a><p>{SE['start_promise']}</p></div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><h2>{SE['faq_h']}</h2></div>
  <div class="sec-faqs">{faq}</div>
</div></section>
<section class="block"><div class="wrap sec-final">
  <p class="mono sec-k">{SE['check_k']}</p>
  <h2>{SE['check_h']}</h2>
  <p class="sec-final-hint">{SE['check_hint']}</p>
  <ul class="sec-check sec-check-i">{"".join(f'<li><label><input type="checkbox"><span>{x}</span></label></li>' for x in SE['check'])}</ul>
  <div class="sec-final-cta"><a class="btn" href="{u('check')}">{SE['check_a']} {arrow}</a><p class="sec-final-ok" aria-live="polite" data-ok="{SE['check_ok']}"></p></div>
  <p class="sec-note">{SE['check_note']} <a href="{u('contact')}?need={SE['need'].replace(' ', '%20')}#contact-form">{SE['alt_contact']}</a></p>
</div></section>""", extra=f'\n<script src="{pre}security-page.js?v={VERSION}"></script>')

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
<section class="block about-first"><div class="wrap about">
  <div class="portrait"><img src="{pre}assets/alessandro.jpg" alt="{St['photo_alt']}" width="1024" height="1024"></div>
  <div><p class="big">{St['who_big']}</p><div class="about-bio" data-more="{St['more']}">{who}</div>
    <ul class="creds">{"".join(f"<li><b>{k}</b><span>{v}</span></li>" for k, v in St['creds'])}</ul>
    <div class="sign"><b>{St['sign'][0]}</b><span>{St['sign'][1]}</span></div></div>
</div></section>
<section class="wrap principle-list">{pr}
</section>""")

    # contatti: modulo in tre passi
    C = L["contact"]; F = C["f"]
    info = "".join(f'<li><span class="mono">{k}</span>{f"<a href=\"mailto:{EMAIL}\">{EMAIL}</a>" if v is None else f"<span>{v}</span>"}</li>' for k, v in C["info"])
    steps_side = "".join(f'<li><span class="n">{i}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(C["next"], 1))
    pills = lambda name, opts, kind="radio": "".join(f'<label class="pick"><input type="{kind}" name="{name}" value="{o}"><span>{o}</span></label>' for o in opts)
    req = f'<em class="req">· {F["req"]}</em>'
    st = C["steps"]
    form = f"""<form class="form qform" id="contact-form" novalidate data-endpoint="https://formsubmit.co/ajax/{EMAIL}" data-subject="{C['subject']}"
      data-sending="{F['sending']}" data-err="{F['err']}" data-email="{EMAIL}" data-step-of="{F['step_of']}">
      <div class="q-progress"><span class="q-count">{F['step_of'].format(a=1, b=3)}</span><span class="q-name">{st[0]}</span><i><b style="width:33%"></b></i></div>
      <fieldset class="q-step" data-step="1" data-name="{st[0]}">
        <div class="q-field full" data-group="need" data-required><p class="q-label">{F['need']} {req}<small>{F['need_hint']}</small></p><div class="picks">{pills("need", F['need_opts'], "checkbox")}</div></div>
        <label class="field full"><span>{F['goal']} {req}</span><textarea name="goal" required rows="4" placeholder="{F['goal_ph']}"></textarea></label>
      </fieldset>
      <fieldset class="q-step" data-step="2" data-name="{st[1]}" hidden>
        <label class="field"><span>{F['company']} {req}</span><input name="company" required autocomplete="organization"></label>
        <label class="field"><span>{F['site']}</span><input name="site" placeholder="{F['site_ph']}" autocomplete="url"></label>
        <label class="field full"><span>{F['sector']}</span><input name="sector" placeholder="{F['sector_ph']}"></label>
        <div class="q-field full" data-group="team"><p class="q-label">{F['team']}</p><div class="picks">{pills("team", F['team_opts'])}</div></div>
        <label class="field full"><span>{F['tools']}</span><input name="tools" placeholder="{F['tools_ph']}"></label>
      </fieldset>
      <fieldset class="q-step" data-step="3" data-name="{st[2]}" hidden>
        <div class="q-field full" data-group="when" data-required><p class="q-label">{F['when']} {req}</p><div class="picks">{pills("when", F['when_opts'])}</div></div>
        <div class="q-field full" data-group="budget"><p class="q-label">{F['budget']}</p><div class="picks">{pills("budget", F['budget_opts'])}</div></div>
        <label class="field"><span>{F['name']} {req}</span><input name="nome" required autocomplete="name"></label>
        <label class="field"><span>{F['role']}</span><input name="role" placeholder="{F['role_ph']}" autocomplete="organization-title"></label>
        <label class="field"><span>{F['email']} {req}</span><input name="email" type="email" required autocomplete="email"></label>
        <label class="field"><span>{F['phone']}</span><input name="phone" type="tel" placeholder="{F['phone_ph']}" autocomplete="tel"></label>
        <label class="field full"><span>{F['source']}</span><select name="source"><option value=""></option>{"".join(f"<option>{o}</option>" for o in F['source_opts'])}</select></label>
        <label class="check full"><input type="checkbox" name="privacy" required><span>{F['privacy']}</span></label>
      </fieldset>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="q-nav full">
        <button type="button" class="btn ghost q-back" hidden>{F['back']}</button>
        <button type="button" class="btn q-next">{F['next']} {arrow}</button>
        <button type="submit" class="btn q-send" hidden>{F['send']} {arrow}</button>
      </div>
      <p class="form-msg full" role="status" aria-live="polite"></p>
    </form>"""
    out["contact"] = page("contact", C["title"], C["desc"], head_block(L["nav"]["contact"], C["h1"], C["sub"]) + f"""
<section class="block contact"><div class="wrap contact-grid">
  <aside class="contact-side">
    <div class="contact-me"><img src="{pre}assets/alessandro.jpg" alt="{L['studio']['photo_alt']}" width="1024" height="1024"><div><b>{L['founder']['contact_h']}</b><p>{L['founder']['contact_p']}</p></div></div>
    <p class="mono" style="margin-bottom:18px">{C['next_k']}</p>
    <ol class="next-steps">{steps_side}</ol>
    <p class="au-side">{L['audit']['contact_p']} <a class="link" href="{u('audit')}">{L['audit']['contact_a']} {arrow}</a></p>
    <ul class="contact-info" style="margin-top:44px">{info}</ul>
  </aside>
  <div class="form-card">
    <div class="contact-me cm-mobile"><img src="{pre}assets/alessandro.jpg" alt="{L['studio']['photo_alt']}" width="1024" height="1024"><div><b>{L['founder']['contact_h']}</b><p>{L['founder']['contact_p']}</p></div></div>
    <h2>{C['form_h']}</h2>
    {form}
    <div class="form-ok" hidden><span class="tick" aria-hidden="true">✓</span><h3>{F['ok_h']}</h3><p>{F['ok_p']}</p></div>
  </div>
</div></section>""")

    # audit di automazione: domande, stima e report generati da audit.js
    A = L["audit"]
    out["audit"] = page("audit", A["title"], A["desc"], head_block(A["k"], A["h1"], A["sub"]) + f"""
<section class="block au-block"><div class="wrap">
  <ul class="au-pts">{"".join(f"<li>{x}</li>" for x in A['pts'])}</ul>
  <div id="audit"></div>
</div></section>""", extra=f'\n<script src="{pre}audit-data.js?v={VERSION}"></script>\n<script src="{pre}audit.js?v={VERSION}"></script>')

    CK = L["check"]
    out["check"] = page("check", CK["title"], CK["desc"], head_block(CK["k"], CK["h1"], CK["sub"]) + f"""
<section class="block au-block"><div class="wrap">
  <ul class="au-pts">{"".join(f"<li>{x}</li>" for x in CK['pts'])}</ul>
  <div id="check"></div>
</div></section>""", extra=f'\n<script src="{pre}security-check.js?v={VERSION}"></script>')

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
    (ROOT / "version.txt").write_text(BUILD, encoding="utf-8")
    # sitemap con le due lingue collegate, robots e pagina 404
    rows = []
    for k in SLUG["it"]:
        urls = {lg: SITE_URL + ("" if lg == "it" else "en/") + ("" if k == "home" else SLUG[lg][k]) for lg in ("it", "en")}
        for lg in ("it", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{urls[x]}"/>' for x in ("it", "en")) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{urls["it"]}"/>'
            rows.append(f"  <url><loc>{urls[lg]}</loc>{alts}</url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /alt/\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (ROOT / "404.html").write_text(f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Pagina non trovata · Reef 7 Lab</title><link rel="icon" href="/reef7-lab/assets/favicon.png">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#04080f;color:#eef3f8;font:17px/1.6 "Segoe UI",system-ui,sans-serif;text-align:center;padding:24px}}h1{{font-size:44px;margin:14px 0 6px;letter-spacing:-.03em}}p{{color:#93a3b5;margin:0 0 26px}}a{{display:inline-block;margin:4px;padding:12px 22px;border-radius:999px;background:#eef3f8;color:#04080f;text-decoration:none;font-weight:600}}a.g{{background:none;color:#eef3f8;box-shadow:inset 0 0 0 1px rgba(238,243,248,.25)}}img{{width:64px;height:64px}}</style></head>
<body><main><img src="/reef7-lab/assets/logo-68.png" alt=""><h1>Pagina non trovata</h1><p>Questa pagina non esiste o è stata spostata. · This page doesn't exist.</p>
<a href="/reef7-lab/">Torna alla home</a><a class="g" href="/reef7-lab/en/">English</a></main></body></html>
""", encoding="utf-8")
    # versione B: stesso contenuto, stile editoriale (styles.css + alt-overrides.css)
    alt_css = (ROOT / "styles.css").read_text(encoding="utf-8") + "\n" + (ROOT / "alt-overrides.css").read_text(encoding="utf-8")
    (ROOT / "alt.css").write_text(alt_css, encoding="utf-8")
    for lang in T:
        build(lang, "alt")
