"""Genera il sito Reef 7 Lab in italiano (cartella principale) e in inglese (cartella en/).

Uso:  python build.py
Testi, prezzi ed email si cambiano qui sotto; poi si rilancia lo script.
"""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "lancioni.ale@gmail.com"
PAGES = ["home", "work", "services", "pricing", "studio", "contact"]
SLUG = {
    "it": {"home": "index.html", "work": "lavori.html", "services": "servizi.html", "pricing": "prezzi.html", "studio": "studio.html", "contact": "contatti.html"},
    "en": {"home": "index.html", "work": "work.html", "services": "services.html", "pricing": "pricing.html", "studio": "studio.html", "contact": "contact.html"},
}

T = {
"it": {
    "nav": {"work": "Lavori", "services": "Servizi", "pricing": "Prezzi", "studio": "Studio", "contact": "Contatti"},
    "menu": "Menu", "close": "Chiudi", "pages": "Pagine",
    "foot_line": "Reef 7 Lab · studio di sviluppo · Italia",
    "end": 'Hai un progetto in mente? <a href="{contact}">Parliamone.</a>',
    "free_slot": "Posto libero",
    "services": [
        ("01", "Siti web", "Siti veloci, curati e facili da aggiornare, pensati per trasformare le visite in richieste.", "da 1.490 €", "2-3 settimane",
         "Un sito che spiega bene cosa fate e porta richieste, veloce da caricare e facile da aggiornare da soli.",
         ["Fino a 5 pagine, ottimizzate per il telefono", "SEO di base e statistiche delle visite", "Modulo contatti collegato alla vostra email", "30 giorni di assistenza dopo il lancio"]),
        ("02", "Soluzioni AI", "Prendo un lavoro che oggi fate a mano (email, documenti, report, lead) e lo automatizzo.", "da 990 €", "1-2 settimane",
         "Scegliamo un'attività ripetitiva che oggi vi porta via ore e la affidiamo all'AI, con controlli dove servono.",
         ["Un processo alla volta: email, documenti, report, lead", "Prima e dopo misurati in ore risparmiate", "Guida scritta e video per il team", "Possibilità di estenderla ad altri processi"]),
        ("03", "Company brain", "Procedure e documenti dell'azienda in un assistente che risponde al team e cita le fonti.", "da 2.500 €", "3-4 settimane",
         "Tutto quello che sa l'azienda, in un assistente che risponde al team citando il documento giusto.",
         ["Procedure, manuali e documenti in un unico posto", "Risposte con le fonti, niente invenzioni", "Ognuno vede solo ciò a cui ha accesso", "Aggiornamenti mensili (290 €/mese)"]),
        ("04", "Dashboard", "I numeri che contano in una pagina, collegati ai vostri strumenti e aggiornati da soli.", "da 1.800 €", "2-3 settimane",
         "I numeri che guardate ogni settimana, in una pagina, senza copiare dati a mano da un foglio all'altro.",
         ["Collegata ai vostri strumenti (Shopify, Stripe, fogli, CRM)", "Aggiornamento automatico", "Accessi diversi per ruolo", "Manutenzione e nuovi grafici (150 €/mese)"]),
        ("05", "App su misura", "Dal problema a un'app funzionante: login, database, pannello di gestione.", "da 4.900 €", "4-8 settimane",
         "Quando un software generico non basta: un'app costruita su come lavorate davvero.",
         ["Discovery con prototipo cliccabile", "Login, database e pannello di gestione", "Pubblicazione e documentazione", "Codice e dati di vostra proprietà"]),
    ],
    "care": ("06", "Reef Care", "Dopo il lancio il progetto non resta solo: hosting, aggiornamenti, backup e piccole modifiche con un canone fisso.",
             ["Hosting, backup e aggiornamenti di sicurezza", "Piccole modifiche ogni mese", "Supporto diretto, senza ticket", "Reef Care+: sviluppo continuo da 1.490 €/mese"], "continuativo", "149-399 €/mese"),
    "home": {
        "title": "Reef 7 Lab · Siti, app e soluzioni AI",
        "desc": "Reef 7 Lab è uno studio di sviluppo: siti, app su misura, soluzioni AI, company brain e dashboard per aziende.",
        "h1": "Costruisco il software su cui <em>gira</em> la tua azienda.",
        "sub": "Reef 7 Lab è il mio studio di sviluppo. Faccio <b>siti, app su misura, soluzioni AI e dashboard</b>, e seguo pochi progetti alla volta, dalla prima idea alla messa online.",
        "spec": [("Studio", "Reef 7 Lab, Italia"), ("Lavoro con", "PMI, startup, professionisti"), ("Stack", "Next.js, Supabase, Python, Claude"), ("Si parte da", "Un audit AI gratuito di 30 minuti")],
        "work_h": "Lavori", "work_p": "Il primo cliente di Reef 7 è Reef 7: il gestionale con cui porto avanti lo studio ogni giorno.",
        "case_t": "Reef 7 HQ", "case_p": "Calendario, CRM, preventivi e fatture in un'unica app",
        "slot_h": "Il prossimo caso studio può essere il tuo.", "slot_p": "I primi tre progetti hanno il 30% di sconto, in cambio di una testimonianza.", "slot_a": "Candidati",
        "svc_h": "Cosa faccio", "svc_p": "Ogni progetto parte da un problema concreto. Il prezzo lo concordiamo per iscritto prima di iniziare.", "svc_all": "Tutti i servizi",
        "how_h": "Come lavoro", "how_p": "Prima capiamo, poi costruiamo. Ogni settimana vedi a che punto siamo.",
        "steps": [("Settimana 1", "Discovery", "Analizziamo il problema. Ricevi un prototipo cliccabile, il piano e il preventivo definitivo."),
                  ("Settimane 2-6", "Sviluppo", "Costruisco a tappe, con una demo ogni settimana. Correggiamo la rotta presto, non alla fine."),
                  ("Consegna", "Lancio", "Messa online, formazione e documentazione. Codice, dati e accessi restano vostri."),
                  ("Dopo", "Manutenzione", "Con Reef Care il progetto resta aggiornato, sicuro e cresce quando serve.")],
    },
    "work": {
        "title": "Lavori · Reef 7 Lab", "desc": "Casi studio di Reef 7 Lab.",
        "h1": "Prima l'ho costruito <em>per me</em>.",
        "sub": "Reef 7 HQ è il gestionale dello studio. Lo uso ogni giorno per clienti, progetti, preventivi e fatture, ed è il modo più onesto per mostrarti come lavoro.",
        "facts": [("Progetto", "Reef 7 HQ"), ("Tipo", "App desktop e web"), ("Anno", "2026"), ("Tecnologie", "Electron, JavaScript, Python, Cloudflare Access")],
        "story": [("Il problema.", "Calendario, attività, clienti, preventivi e fatture stavano in cinque strumenti diversi. Ogni giorno perdevo tempo a passare dall'uno all'altro e i numeri non tornavano mai."),
                  ("Cosa ho costruito.", "Un'unica app: legge Google Calendar, organizza le attività per priorità, misura il tempo di lavoro, tiene clienti e progetti in un CRM, prepara preventivi e fatture in PDF e pubblica il portfolio con un clic."),
                  ("Come funziona.", "Gira sul computer e online, con gli stessi dati. I dati sono cifrati e l'accesso alla versione web passa da un login protetto."),
                  ("Cosa ne puoi ricavare tu.", "Lo stesso approccio funziona per un gestionale interno, un portale clienti o una dashboard: si parte da come lavorate oggi, non da un software generico.")],
        "slot_h": "Qui ci sarà il tuo progetto.", "slot_p": "Sto cercando i primi tre clienti: 30% di sconto in cambio di una testimonianza e del permesso di raccontare il lavoro.", "slot_a": "Raccontami il progetto",
    },
    "services_p": {
        "title": "Servizi · Reef 7 Lab", "desc": "Siti web, soluzioni AI, company brain, dashboard, app su misura e manutenzione.",
        "h1": "Sei modi per lavorare <em>meglio</em>, con meno software.",
        "sub": "Ogni servizio ha un prezzo di partenza e tempi chiari. Se non sai da dove iniziare, si parte da una Discovery: 490 €, scalati dal progetto.",
        "end": 'Non sai quale ti serve? <a href="{contact}">Facciamo un audit gratuito.</a>',
    },
    "pricing": {
        "title": "Prezzi · Reef 7 Lab", "desc": "Prezzi di partenza dei servizi di Reef 7 Lab.",
        "h1": "Prezzi chiari, <em>prima</em> di iniziare.",
        "sub": "Questi sono i prezzi di partenza. Quello definitivo lo fissiamo per iscritto dopo la Discovery, e non cambia strada facendo. IVA esclusa.",
        "cols": ("Servizio", "Cosa include", "Tempi", "Prezzo"),
        "rows": [("Discovery", "Analisi, prototipo cliccabile, piano e preventivo preciso. Scalata dal progetto.", "3-5 giorni", "490 €"),
                 ("Sito web", "Fino a 5 pagine, mobile, SEO di base, contatti e statistiche.", "2-3 settimane", "da 1.490 €"),
                 ("Soluzione AI", "Un processo automatizzato con l'AI, con guida e video.", "1-2 settimane", "da 990 €"),
                 ("Dashboard", "KPI collegati ai vostri strumenti, accessi per ruolo. + 150 €/mese.", "2-3 settimane", "da 1.800 €"),
                 ("Company brain", "Le conoscenze dell'azienda in un assistente con le fonti. + 290 €/mese.", "3-4 settimane", "da 2.500 €"),
                 ("App su misura", "Discovery, MVP con login, database e pannello di gestione.", "4-8 settimane", "da 4.900 €"),
                 ("Reef Care", "Hosting, aggiornamenti, backup, piccole modifiche e supporto.", "al mese", "149-399 €"),
                 ("Reef Care+", "Sviluppo continuo in abbonamento, una richiesta alla volta.", "al mese", "da 1.490 €")],
        "offer_k": "Offerta di lancio", "offer_h": "I primi tre clienti hanno il 30% di sconto.",
        "offer_p": "In cambio ti chiedo una testimonianza e il permesso di raccontare il progetto nel portfolio.", "offer_a": "Prenota un posto →",
        "faq_h": "Domande", "faq_p": "Se la tua non c'è, scrivimi.",
        "faq": [("Cos'è l'audit AI gratuito?", "Una call di 30 minuti in cui guardiamo come lavora la tua azienda e dove l'AI può farvi risparmiare tempo. Esci con due o tre idee concrete, anche se poi non lavoriamo insieme."),
                ("Perché la Discovery è a pagamento?", "Perché è già lavoro vero: alla fine hai un prototipo, un piano e un preventivo preciso, che restano tuoi. Se poi procediamo, i 490 € vengono scalati dal progetto."),
                ("Come si paga?", "Di solito 50% all'avvio e 50% alla consegna. Per i progetti più lunghi dividiamo per tappe."),
                ("E se il progetto va in ritardo?", "Se non consegno entro la data concordata, hai il 10% di sconto. Le date le fissiamo insieme dopo la Discovery."),
                ("Di chi sono il codice e i dati?", "Tuoi. Alla consegna ricevi codice, accessi e documentazione, e i dati restano nei tuoi account.")],
    },
    "studio": {
        "title": "Studio · Reef 7 Lab", "desc": "Chi c'è dietro Reef 7 Lab e come lavora.",
        "h1": "Uno studio piccolo, <em>di proposito</em>.", "photo_alt": "Alessandro, fondatore di Reef 7 Lab",
        "prose": [("Sono Alessandro e Reef 7 Lab è il mio studio.", "Prima di aprirlo mi sono occupato di software, automazioni e funnel: è lì che ho visto quanto tempo si perde con strumenti scollegati e lavori fatti a mano."),
                  ("", "Oggi costruisco siti, app e soluzioni AI per aziende che vogliono lavorare meglio senza riempirsi di abbonamenti. Lavoro con pochi clienti alla volta, così parli sempre con chi scrive il codice."),
                  ("Il nome.", "Una barriera corallina è fatta di tanti organismi diversi che crescono collegati. È così che penso il software: pezzi diversi (un sito, un'automazione, una dashboard) che parlano tra loro invece di restare isolati.")],
        "rules_h": "Come lavoro", "rules_p": "Quattro regole che valgono per ogni progetto.",
        "rules": [("Prezzo fisso", "Il preventivo è scritto dopo la Discovery e non cambia strada facendo."),
                  ("Demo ogni settimana", "Vedi il progetto funzionare mentre cresce, non solo alla fine."),
                  ("Tutto vostro", "Codice, dati e accessi restano a voi. Nessun vincolo con me."),
                  ("Risultati misurati", "Ogni progetto ha un obiettivo in ore risparmiate o richieste in più, e lo controlliamo.")],
        "tools_h": "Strumenti", "tools_p": "Tecnologie moderne, leggere da mantenere e senza costi nascosti.",
        "tools": [("Siti e app", "Next.js, React, TypeScript"), ("Dati e accessi", "Supabase, Postgres"), ("AI", "Claude, MCP, Python"), ("Pubblicazione", "Vercel, Cloudflare")],
    },
    "contact": {
        "title": "Contatti · Reef 7 Lab", "desc": "Scrivi a Reef 7 Lab per un audit AI gratuito o un preventivo.",
        "h1": "Raccontami cosa vorresti <em>migliorare</em>.",
        "sub": "Anche solo un'idea va bene. Ti rispondo con una proposta per l'audit gratuito di 30 minuti.",
        "or": "Oppure compila qui", "or_p": "Il pulsante apre la tua email con il messaggio già pronto.",
        "f": {"name": "Nome", "company": "Azienda", "want": "Ti interessa", "msg": "Il progetto",
              "ph": "Es. rispondiamo ogni giorno alle stesse domande dei clienti e vorremmo automatizzarlo",
              "opts": ["Audit AI gratuito", "Sito web", "Soluzione AI", "Company brain", "Dashboard", "App su misura", "Non lo so ancora"],
              "note": "Rispondo di solito entro un giorno lavorativo.", "send": "Invia →"},
        "end": 'Preferisci una call? <a href="{contact}">Scrivimi e la fissiamo.</a>',
    },
},
"en": {
    "nav": {"work": "Work", "services": "Services", "pricing": "Pricing", "studio": "Studio", "contact": "Contact"},
    "menu": "Menu", "close": "Close", "pages": "Pages",
    "foot_line": "Reef 7 Lab · development studio · Italy",
    "end": 'Got a project in mind? <a href="{contact}">Let\'s talk.</a>',
    "free_slot": "Open slot",
    "services": [
        ("01", "Websites", "Fast, well-crafted sites that are easy to update and built to turn visits into enquiries.", "from €1,490", "2-3 weeks",
         "A site that explains clearly what you do and brings in enquiries. Quick to load, easy to update yourself.",
         ["Up to 5 pages, built for mobile", "Basic SEO and visitor analytics", "Contact form wired to your inbox", "30 days of support after launch"]),
        ("02", "AI solutions", "I take a task you still do by hand (email, documents, reports, leads) and automate it.", "from €990", "1-2 weeks",
         "We pick a repetitive task that eats your team's hours and hand it to AI, with checks where they matter.",
         ["One process at a time: email, documents, reports, leads", "Before and after measured in hours saved", "Written guide and video for the team", "Easy to extend to other processes"]),
        ("03", "Company brain", "Your procedures and documents in an assistant that answers the team and cites its sources.", "from €2,500", "3-4 weeks",
         "Everything your company knows, in an assistant that answers your team and points to the right document.",
         ["Procedures, manuals and docs in one place", "Answers with sources, no guessing", "Everyone sees only what they're allowed to", "Monthly updates (€290/month)"]),
        ("04", "Dashboards", "The numbers that matter on one page, connected to your tools and updated automatically.", "from €1,800", "2-3 weeks",
         "The numbers you check every week, on one page, without copying data between spreadsheets.",
         ["Connected to your tools (Shopify, Stripe, sheets, CRM)", "Updates automatically", "Role-based access", "Maintenance and new charts (€150/month)"]),
        ("05", "Custom apps", "From a problem to a working app: login, database and admin panel.", "from €4,900", "4-8 weeks",
         "When off-the-shelf software doesn't fit: an app built around how you actually work.",
         ["Discovery with a clickable prototype", "Login, database and admin panel", "Deployment and documentation", "You own the code and the data"]),
    ],
    "care": ("06", "Reef Care", "After launch your project isn't left alone: hosting, updates, backups and small changes for a flat monthly fee.",
             ["Hosting, backups and security updates", "Small changes every month", "Direct support, no ticket queue", "Reef Care+: ongoing development from €1,490/month"], "ongoing", "€149-399/month"),
    "home": {
        "title": "Reef 7 Lab · Websites, apps and AI solutions",
        "desc": "Reef 7 Lab is a development studio building websites, custom apps, AI solutions, company brains and dashboards.",
        "h1": "I build the software your business <em>runs</em> on.",
        "sub": "Reef 7 Lab is my development studio. I make <b>websites, custom apps, AI solutions and dashboards</b>, and I take on a few projects at a time, from first idea to launch.",
        "spec": [("Studio", "Reef 7 Lab, Italy"), ("I work with", "SMBs, startups, professionals"), ("Stack", "Next.js, Supabase, Python, Claude"), ("Start with", "A free 30-minute AI audit")],
        "work_h": "Work", "work_p": "Reef 7's first client is Reef 7: the system I use to run the studio every day.",
        "case_t": "Reef 7 HQ", "case_p": "Calendar, CRM, proposals and invoices in one app",
        "slot_h": "Your project could be the next case study.", "slot_p": "The first three projects get 30% off in exchange for a testimonial.", "slot_a": "Apply",
        "svc_h": "What I do", "svc_p": "Every project starts from a real problem. We agree on the price in writing before any work begins.", "svc_all": "All services",
        "how_h": "How I work", "how_p": "Understand first, then build. Every week you see where things stand.",
        "steps": [("Week 1", "Discovery", "We dig into the problem. You get a clickable prototype, a plan and a fixed quote."),
                  ("Weeks 2-6", "Build", "I build in stages with a demo every week, so we adjust early, not at the end."),
                  ("Handover", "Launch", "Deployment, training and documentation. Code, data and access stay yours."),
                  ("After", "Care", "With Reef Care your project stays updated, secure and keeps growing when you need it.")],
    },
    "work": {
        "title": "Work · Reef 7 Lab", "desc": "Reef 7 Lab case studies.",
        "h1": "I built it <em>for myself</em> first.",
        "sub": "Reef 7 HQ is the studio's operating system. I use it every day for clients, projects, proposals and invoices, and it's the most honest way to show you how I work.",
        "facts": [("Project", "Reef 7 HQ"), ("Type", "Desktop and web app"), ("Year", "2026"), ("Built with", "Electron, JavaScript, Python, Cloudflare Access")],
        "story": [("The problem.", "Calendar, tasks, clients, proposals and invoices lived in five different tools. I lost time every day switching between them, and the numbers never added up."),
                  ("What I built.", "One app: it reads Google Calendar, ranks tasks by priority, tracks working time, keeps clients and projects in a CRM, generates proposals and invoices as PDFs and publishes the portfolio in one click."),
                  ("How it works.", "It runs on desktop and on the web with the same data. Data is encrypted, and the web version sits behind a protected login."),
                  ("What it means for you.", "The same approach works for an internal tool, a client portal or a dashboard: we start from how you work today, not from generic software.")],
        "slot_h": "Your project goes here.", "slot_p": "I'm looking for my first three clients: 30% off in exchange for a testimonial and permission to share the work.", "slot_a": "Tell me about your project",
    },
    "services_p": {
        "title": "Services · Reef 7 Lab", "desc": "Websites, AI solutions, company brains, dashboards, custom apps and maintenance.",
        "h1": "Six ways to work <em>better</em>, with less software.",
        "sub": "Every service has a starting price and a clear timeline. Not sure where to begin? Start with a Discovery: €490, credited toward the project.",
        "end": 'Not sure which one you need? <a href="{contact}">Book a free audit.</a>',
    },
    "pricing": {
        "title": "Pricing · Reef 7 Lab", "desc": "Starting prices for Reef 7 Lab services.",
        "h1": "Clear prices, <em>before</em> we start.",
        "sub": "These are starting prices. The final price is set in writing after the Discovery and doesn't change along the way. VAT excluded.",
        "cols": ("Service", "What's included", "Timeline", "Price"),
        "rows": [("Discovery", "Analysis, clickable prototype, plan and fixed quote. Credited toward the project.", "3-5 days", "€490"),
                 ("Website", "Up to 5 pages, mobile-ready, basic SEO, contact form and analytics.", "2-3 weeks", "from €1,490"),
                 ("AI solution", "One process automated with AI, with a guide and video.", "1-2 weeks", "from €990"),
                 ("Dashboard", "KPIs connected to your tools, role-based access. + €150/month.", "2-3 weeks", "from €1,800"),
                 ("Company brain", "Your company's knowledge in an assistant that cites sources. + €290/month.", "3-4 weeks", "from €2,500"),
                 ("Custom app", "Discovery, MVP with login, database and admin panel.", "4-8 weeks", "from €4,900"),
                 ("Reef Care", "Hosting, updates, backups, small changes and support.", "per month", "€149-399"),
                 ("Reef Care+", "Ongoing development on subscription, one request at a time.", "per month", "from €1,490")],
        "offer_k": "Launch offer", "offer_h": "The first three clients get 30% off.",
        "offer_p": "In return I ask for a testimonial and permission to feature the project in my portfolio.", "offer_a": "Claim a spot →",
        "faq_h": "Questions", "faq_p": "If yours isn't here, just ask.",
        "faq": [("What's the free AI audit?", "A 30-minute call where we look at how your company works and where AI could save you time. You leave with two or three concrete ideas, even if we never work together."),
                ("Why is the Discovery paid?", "Because it's real work: you end up with a prototype, a plan and a fixed quote that are yours to keep. If we go ahead, the €490 is credited toward the project."),
                ("How does payment work?", "Usually 50% upfront and 50% on delivery. Longer projects are split into milestones."),
                ("What if the project runs late?", "If I miss the agreed delivery date, you get 10% off. We set the dates together after the Discovery."),
                ("Who owns the code and the data?", "You do. At handover you get the code, access and documentation, and the data stays in your accounts.")],
    },
    "studio": {
        "title": "Studio · Reef 7 Lab", "desc": "Who's behind Reef 7 Lab and how it works.",
        "h1": "A small studio, <em>on purpose</em>.", "photo_alt": "Alessandro, founder of Reef 7 Lab",
        "prose": [("I'm Alessandro, and Reef 7 Lab is my studio.", "Before starting it I worked on software, automations and funnels, and saw how much time companies lose to disconnected tools and manual work."),
                  ("", "Today I build websites, apps and AI solutions for companies that want to work better without piling up subscriptions. I take on a few clients at a time, so you always talk to the person writing the code."),
                  ("The name.", "A coral reef is made of many different organisms growing together, connected. That's how I think about software: different pieces (a site, an automation, a dashboard) that talk to each other instead of sitting in silos.")],
        "rules_h": "How I work", "rules_p": "Four rules for every project.",
        "rules": [("Fixed price", "The quote is written after the Discovery and doesn't change along the way."),
                  ("Weekly demos", "You see the project working as it grows, not just at the end."),
                  ("You own it", "Code, data and access are yours. No lock-in."),
                  ("Measured results", "Every project has a goal in hours saved or extra enquiries, and we check it.")],
        "tools_h": "Tools", "tools_p": "Modern technology that's light to maintain, with no hidden costs.",
        "tools": [("Sites and apps", "Next.js, React, TypeScript"), ("Data and auth", "Supabase, Postgres"), ("AI", "Claude, MCP, Python"), ("Hosting", "Vercel, Cloudflare")],
    },
    "contact": {
        "title": "Contact · Reef 7 Lab", "desc": "Get in touch with Reef 7 Lab for a free AI audit or a quote.",
        "h1": "Tell me what you'd like to <em>improve</em>.",
        "sub": "A rough idea is fine. I'll reply with a time for the free 30-minute audit.",
        "or": "Or fill this in", "or_p": "The button opens your email with the message ready to send.",
        "f": {"name": "Name", "company": "Company", "want": "Interested in", "msg": "Your project",
              "ph": "E.g. we answer the same customer questions every day and want to automate it",
              "opts": ["Free AI audit", "Website", "AI solution", "Company brain", "Dashboard", "Custom app", "Not sure yet"],
              "note": "I usually reply within one business day.", "send": "Send →"},
        "end": 'Prefer a call? <a href="{contact}">Email me and we\'ll set one up.</a>',
    },
},
}

APP_SHOT = """<div class="shot"><div class="grid"></div>
        <div class="app"><div class="side"><i></i><i></i><i></i><i></i><i></i></div>
          <div class="main"><div class="hd"></div><div class="kp"><span></span><span></span><span></span></div><div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div></div></div>
      </div>"""


def build(lang):
    L, S = T[lang], SLUG[lang]
    other = "en" if lang == "it" else "it"
    pre = "" if lang == "it" else "../"           # percorso degli asset
    alt_dir = "en/" if lang == "it" else "../"     # cartella dell'altra lingua
    u = lambda k: S[k]
    kicker = lambda txt: f'<p class="mono" style="margin-bottom:22px">{txt}</p>'

    def page(key, title, desc, body, end_line=None):
        links = "".join(f'<a href="{u(k)}"{" aria-current=\"page\"" if k == key else ""}>{L["nav"][k]}</a>' for k in ["work", "services", "pricing", "studio"])
        cur = ' aria-current="page"' if key == "contact" else ""
        foot_links = "".join(f'<a href="{u(k)}">{L["nav"][k]}</a>' for k in ["work", "services", "pricing", "studio", "contact"])
        end_html = (end_line or L["end"]).format(contact=u("contact"))
        alt = f"{alt_dir}{SLUG[other][key]}"
        return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#060c15">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{pre}assets/reef7-logo.png">
  <link rel="alternate" hreflang="{other}" href="{alt}">
  <link rel="icon" href="{pre}assets/favicon.png">
  <link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}styles.css">
</head>
<body>
<div class="page">
<header class="top">
  <a class="logo" href="{u('home')}"><img src="{pre}assets/reef7-logo.png" alt="" width="30" height="30">Reef 7 Lab</a>
  <nav aria-label="{L['pages']}">{links}<a href="{u('contact')}" class="cta"{cur}>{L['nav']['contact']}</a></nav>
  <a class="lang" href="{alt}" hreflang="{other}" lang="{other}">{other.upper()}</a>
  <button class="menu" aria-expanded="false" data-close="{L['close']}">{L['menu']}</button>
</header>
<main>
{body}
</main>
<footer class="end">
  <h2>{end_html}</h2>
  <div class="end-row">
    <span>{L['foot_line']}</span>
    <nav aria-label="{L['pages']}">{foot_links}</nav>
    <a class="r" href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</footer>
</div>
<script>window.REEF = {{ email: "{EMAIL}" }};</script>
<script src="{pre}site.js"></script>
</body>
</html>
"""

    out = {}
    # home
    H = L["home"]
    rows = "".join(f"""
      <a class="row" href="{u('services')}#s{n}"><span class="mono">{n}</span><h3>{t}</h3><p>{d}</p><span class="price-tag">{p}<small>{w}</small></span></a>""" for n, t, d, p, w, *_ in L["services"])
    spec = "".join(f'<div><p class="mono">{a}</p><p>{b}</p></div>' for a, b in H["spec"])
    steps = "".join(f'<li><span class="mono">{a}</span><h3>{b}</h3><p>{c}</p></li>' for a, b, c in H["steps"])
    out["home"] = page("home", H["title"], H["desc"], f"""  <section class="intro">
    <h1>{H['h1']}</h1>
    <p class="sub">{H['sub']}</p>
    <img class="art" src="{pre}assets/reef-deco.svg" alt="" aria-hidden="true">
  </section>
  <div class="spec">{spec}</div>
  <section class="block">
    <div class="block-head"><h2>{H['work_h']}</h2><p>{H['work_p']}</p></div>
    <div class="work">
      <a class="work-card" href="{u('work')}">
        {APP_SHOT}
        <div class="meta"><div><h3>{H['case_t']}</h3><p>{H['case_p']}</p></div><span class="mono">2026</span></div>
      </a>
      <div class="slot">
        <span class="mono">{L['free_slot']}</span>
        <div><h3>{H['slot_h']}</h3><p>{H['slot_p']}</p></div>
        <a class="more u" href="{u('contact')}">{H['slot_a']}</a>
      </div>
    </div>
  </section>
  <section class="block">
    <div class="block-head"><h2>{H['svc_h']}</h2><p>{H['svc_p']}</p></div>
    <div class="rows">{rows}
    </div>
    <a class="more u" href="{u('services')}">{H['svc_all']}</a>
  </section>
  <section class="block">
    <div class="block-head"><h2>{H['how_h']}</h2><p>{H['how_p']}</p></div>
    <ol class="steps">{steps}</ol>
  </section>""")

    # work
    W = L["work"]
    facts = "".join(f'<li><p class="mono">{a}</p><p>{b}</p></li>' for a, b in W["facts"])
    story = "".join(f"<p><b>{a}</b> {b}</p>" for a, b in W["story"])
    out["work"] = page("work", W["title"], W["desc"], f"""  <section class="intro small">
    {kicker(L['nav']['work'])}
    <h1>{W['h1']}</h1>
    <p class="sub">{W['sub']}</p>
  </section>
  <section class="block" style="padding-top:0"><div class="work-card">{APP_SHOT}</div></section>
  <section class="block" id="reef7-hq">
    <div class="two"><ul class="list">{facts}</ul><div class="prose">{story}</div></div>
  </section>
  <section class="block">
    <div class="slot" style="min-height:0;gap:28px">
      <span class="mono">{L['free_slot']}</span>
      <div><h3>{W['slot_h']}</h3><p>{W['slot_p']}</p></div>
      <a class="more u" href="{u('contact')}">{W['slot_a']}</a>
    </div>
  </section>""")

    # services
    SP = L["services_p"]
    items = [(n, t, long, li, w, p) for n, t, _, p, w, long, li in L["services"]] + [L["care"][:4] + (L["care"][4], L["care"][5])]
    svc = "".join(f"""
    <article class="svc" id="s{n}">
      <span class="mono">{n}</span>
      <div><h2>{t}</h2><p class="lead">{d}</p></div>
      <div><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><div class="foot"><span>{w}</span><span>{p}</span></div></div>
    </article>""" for n, t, d, li, w, p in items)
    out["services"] = page("services", SP["title"], SP["desc"], f"""  <section class="intro small">
    {kicker(L['nav']['services'])}
    <h1>{SP['h1']}</h1>
    <p class="sub">{SP['sub']}</p>
  </section>
  <section style="padding-bottom:clamp(72px,9vw,128px)">{svc}
  </section>""", SP["end"])

    # pricing
    P = L["pricing"]
    trs = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="num">{d}</td></tr>' for a, b, c, d in P["rows"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in P["faq"])
    c = P["cols"]
    out["pricing"] = page("pricing", P["title"], P["desc"], f"""  <section class="intro small">
    {kicker(L['nav']['pricing'])}
    <h1>{P['h1']}</h1>
    <p class="sub">{P['sub']}</p>
  </section>
  <section class="block" style="padding-top:0">
    <table class="table">
      <thead><tr><th>{c[0]}</th><th>{c[1]}</th><th>{c[2]}</th><th class="num">{c[3]}</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
  </section>
  <section class="block">
    <div class="paper">
      <div><p class="mono" style="margin-bottom:18px">{P['offer_k']}</p><h2>{P['offer_h']}</h2></div>
      <div><p>{P['offer_p']}</p><p style="margin-top:22px"><a class="btn" href="{u('contact')}">{P['offer_a']}</a></p></div>
    </div>
  </section>
  <section class="block">
    <div class="block-head"><h2>{P['faq_h']}</h2><p>{P['faq_p']}</p></div>
    <div class="faq">{faq}</div>
  </section>""")

    # studio
    St = L["studio"]
    prose = "".join(f"<p>{f'<b>{a}</b> ' if a else ''}{b}</p>" for a, b in St["prose"])
    rules = "".join(f'<li><p class="mono">{a}</p><p>{b}</p></li>' for a, b in St["rules"])
    tools = "".join(f'<li><p class="mono">{a}</p><p>{b}</p></li>' for a, b in St["tools"])
    out["studio"] = page("studio", St["title"], St["desc"], f"""  <section class="intro small">
    {kicker(L['nav']['studio'])}
    <h1>{St['h1']}</h1>
  </section>
  <section class="block" style="padding-top:0">
    <div class="two">
      <div class="portrait"><img src="{pre}assets/alessandro.jpg" alt="{St['photo_alt']}" width="512" height="512"></div>
      <div class="prose">{prose}</div>
    </div>
  </section>
  <section class="block">
    <div class="block-head"><h2>{St['rules_h']}</h2><p>{St['rules_p']}</p></div>
    <ul class="list">{rules}</ul>
  </section>
  <section class="block">
    <div class="block-head"><h2>{St['tools_h']}</h2><p>{St['tools_p']}</p></div>
    <ul class="list">{tools}</ul>
  </section>""")

    # contact
    C = L["contact"]; F = C["f"]
    opts = "".join(f"<option>{o}</option>" for o in F["opts"])
    out["contact"] = page("contact", C["title"], C["desc"], f"""  <section class="intro small">
    {kicker(L['nav']['contact'])}
    <h1>{C['h1']}</h1>
    <p class="sub">{C['sub']}</p>
  </section>
  <section class="block" style="padding-top:0">
    <a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a>
  </section>
  <section class="block">
    <div class="two">
      <div><p class="mono">{C['or']}</p><p style="color:var(--muted);margin-top:14px;max-width:340px">{C['or_p']}</p></div>
      <form class="form" id="contact-form">
        <label><span class="mono">{F['name']}</span><input name="nome" required autocomplete="name"></label>
        <label><span class="mono">{F['company']}</span><input name="azienda" autocomplete="organization"></label>
        <label class="full"><span class="mono">{F['want']}</span><select name="servizio">{opts}</select></label>
        <label class="full"><span class="mono">{F['msg']}</span><textarea name="messaggio" required placeholder="{F['ph']}"></textarea></label>
        <div class="send full"><p>{F['note']}</p><button class="btn" type="submit">{F['send']}</button></div>
      </form>
    </div>
  </section>""", C["end"])

    folder = ROOT if lang == "it" else ROOT / "en"
    folder.mkdir(exist_ok=True)
    for key, html in out.items():
        (folder / S[key]).write_text(html, encoding="utf-8")
        print("ok", lang, S[key])


if __name__ == "__main__":
    for lang in T:
        build(lang)
