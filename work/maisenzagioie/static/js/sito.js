/*
  Maisenzagioie · il poco JavaScript del sito.

  Fa cinque cose:
    1. apre e chiude il menu sul telefono
    2. disegna il filo quando entra nello schermo
    3. cambia le schede del catalogo senza ricaricare la pagina
    4. nella pagina "Crea la tua" aggiorna il prezzo mentre si sceglie
    5. nella pagina Contatti cambia il suggerimento in base al motivo

  Senza JavaScript il sito funziona comunque: le schede diventano link normali,
  e newsletter e animazione del titolo non ne hanno bisogno.
*/

// 1. MENU --------------------------------------------------------------------
// <dialog> col metodo showModal() trattiene da solo il focus dentro al menu e
// si chiude col tasto Esc. Alla chiusura il focus torna al bottone che l'ha aperto.

const menu = document.querySelector(".menu");
const apriMenu = document.querySelector("[data-apri-menu]");
const chiudiMenu = document.querySelector("[data-chiudi-menu]");

if (menu && apriMenu && chiudiMenu) {
  apriMenu.addEventListener("click", () => menu.showModal());
  chiudiMenu.addEventListener("click", () => menu.close());
  menu.addEventListener("close", () => apriMenu.focus());

  // toccando una voce che porta a un'altra parte della stessa pagina,
  // il menu si chiude, altrimenti resterebbe sopra
  menu.querySelectorAll("a").forEach((voce) => {
    voce.addEventListener("click", () => menu.close());
  });
}

// 2. IL FILO -----------------------------------------------------------------
// Quando un filo diventa visibile gli si aggiunge la classe "visto":
// il CSS fa il resto (sito.css, sezione Animazioni).

const fili = document.querySelectorAll(".filo");

if ("IntersectionObserver" in window) {
  const osservatore = new IntersectionObserver(
    (voci) => {
      voci.forEach((voce) => {
        if (voce.isIntersecting) {
          voce.target.classList.add("visto");
          osservatore.unobserve(voce.target); // si disegna una volta sola
        }
      });
    },
    { threshold: 0.3 }
  );
  fili.forEach((filo) => osservatore.observe(filo));
} else {
  // browser molto vecchi: il filo si mostra subito, già disegnato
  fili.forEach((filo) => filo.classList.add("visto"));
}

// 3. LE SCHEDE DEL CATALOGO ---------------------------------------------------
// Senza JavaScript ogni scheda è un link che ricarica la pagina. Qui invece si
// cambia la griglia sul posto: si mostra un pannello, si nascondono gli altri.

const schede = [...document.querySelectorAll('[role="tab"][data-categoria]')];
const testata = document.querySelector(".testata");
const filaSchede = document.querySelector(".categorie");

function apriScheda(scheda) {
  const categoria = scheda.dataset.categoria;

  schede.forEach((s) => {
    const aperta = s === scheda;
    s.setAttribute("aria-selected", aperta ? "true" : "false");
    s.tabIndex = aperta ? 0 : -1; // col Tab si entra solo nella scheda aperta
    document.getElementById(s.getAttribute("aria-controls")).hidden = !aperta;
  });

  // l'indirizzo segue la scheda: ricaricando o condividendo il link si
  // ritrova la stessa categoria
  history.replaceState(null, "", `?categoria=${categoria}#i-pezzi`);

  // se si era scesi dentro la griglia, si torna all'inizio di quella nuova,
  // subito sotto testata e schede
  const pannello = document.getElementById(scheda.getAttribute("aria-controls"));
  const coperto = testata.offsetHeight + filaSchede.offsetHeight;
  const inizio = pannello.getBoundingClientRect().top;
  if (inizio < coperto) {
    window.scrollTo({ top: window.scrollY + inizio - coperto - 12, behavior: "smooth" });
  }
}

schede.forEach((scheda, i) => {
  scheda.addEventListener("click", (evento) => {
    evento.preventDefault(); // niente ricarica: ci pensa apriScheda
    apriScheda(scheda);
  });

  // frecce sinistra e destra per passare da una scheda all'altra
  scheda.addEventListener("keydown", (evento) => {
    const passo = { ArrowRight: 1, ArrowLeft: -1 }[evento.key];
    if (!passo) return;
    evento.preventDefault();
    const prossima = schede[(i + passo + schede.length) % schede.length];
    prossima.focus();
    apriScheda(prossima);
  });
});

// 4. LA PAGINA "CREA LA TUA" -------------------------------------------------
// Aggiorna il prezzo mentre si sceglie, fa comparire la barra d'acquisto sul
// telefono e segna la miniatura della foto che si sta guardando.
// I prezzi veri stanno in dati/configuratore.py: qui si rifà solo la somma.

const configuratore = document.querySelector("[data-configuratore]");

if (configuratore) {
  // 117 € invece di 117,00 €: i decimali solo quando ci sono davvero
  const euro = (n) =>
    new Intl.NumberFormat("it-IT", {
      style: "currency", currency: "EUR", minimumFractionDigits: n % 1 ? 2 : 0,
    }).format(n);
  const scrivi = (selettore, testo) =>
    document.querySelectorAll(selettore).forEach((el) => (el.textContent = testo));

  function aggiornaPrezzi() {
    // il modello porta con sé i prezzi di collana, bracciale e cavigliera
    const modello = configuratore.querySelector('input[name="modello"]:checked').dataset;
    const centro = configuratore.querySelector('input[name="centro"]:checked');
    const collana = Number(modello.collana) + Number(centro?.dataset.aggiunta ?? 0);
    const separatiDi = (voce) =>
      voce.dataset.pezzi.split(" ").filter(Boolean)
        .reduce((somma, pezzo) => somma + Number(modello[pezzo]), collana);

    // il prezzo di ogni offerta, con le scelte di adesso, e quanto costerebbero
    // gli stessi pezzi comprati uno per uno (il prezzo barrato)
    configuratore.querySelectorAll('input[name="set"]').forEach((voce) => {
      const separati = separatiDi(voce);
      const scheda = voce.closest(".set__voce");
      scheda.querySelector("[data-prezzo-set]").textContent = euro(separati - Number(voce.dataset.sconto));
      const barrato = scheda.querySelector("[data-separati-set]");
      if (barrato) barrato.textContent = euro(separati);
    });

    // l'offerta scelta: totale ovunque compaia (scheda, bottone, barra in basso)
    const set = configuratore.querySelector('input[name="set"]:checked');
    const separati = separatiDi(set);
    const totale = separati - Number(set.dataset.sconto);
    scrivi("[data-totale]", euro(totale));
    scrivi("[data-separati]", euro(separati));
    scrivi("[data-risparmio]", euro(separati - totale));
    configuratore.querySelectorAll("[data-prezzo-pezzo]").forEach((el) => {
      el.textContent = euro(Number(modello[el.dataset.prezzoPezzo]));
    });

    // "Comprati uno per uno" e "Risparmi" hanno senso solo se c'è uno sconto
    const conSconto = separati > totale;
    configuratore
      .querySelectorAll(".prezzo-offerta__separati, .prezzo-offerta__risparmio")
      .forEach((el) => (el.hidden = !conSconto));

    // la pila: si vede solo il contenuto dell'offerta scelta
    configuratore.querySelectorAll("[data-contenuto-set]").forEach((ul) => {
      ul.hidden = ul.dataset.contenutoSet !== set.value;
    });
  }

  configuratore.addEventListener("change", aggiornaPrezzi);
  aggiornaPrezzi();

  // i link "Fai una richiesta speciale" aprono anche il modulo, non solo ci arrivano
  const apriSpeciale = document.querySelector("[data-apri-speciale]");
  document.querySelectorAll('a[href="#richiesta-speciale"]').forEach((link) => {
    link.addEventListener("click", () => { if (apriSpeciale) apriSpeciale.open = true; });
  });

  // le tendine (filo e centro). Scelto un colore o una pietra, il pallino e il
  // nome in alto cambiano subito, poi la tendina si chiude da sola. Si chiude
  // anche con "Fatto", con "Chiudi" in alto, con Esc o toccando fuori.
  const tendine = [...configuratore.querySelectorAll("[data-tendina]")];

  const chiudi = (tendina, { focus = false } = {}) => {
    if (!tendina.open) return;
    tendina.open = false;
    const testa = tendina.querySelector("summary");
    // chiudendo, la pagina si accorcia: se la scelta è finita sopra lo
    // schermo, la riportiamo in vista (succede soprattutto sul telefono)
    if (testa.getBoundingClientRect().top < 80) {
      testa.scrollIntoView({ block: "center", behavior: "smooth" });
    }
    if (focus) testa.focus({ preventScroll: true });
  };

  tendine.forEach((tendina) => {
    tendina.addEventListener("change", (evento) => {
      const dati = evento.target.dataset;
      tendina.querySelector("[data-pallino]").style.background = dati.colore;
      tendina.querySelector("[data-nome-scelto]").textContent = dati.nome;
      const prezzo = tendina.querySelector("[data-prezzo-scelto]");
      if (prezzo) prezzo.textContent = Number(dati.aggiunta) ? `+ ${euro(Number(dati.aggiunta))}` : "incluso";
      // un attimo di pausa: si vede la scelta evidenziata prima che si chiuda
      setTimeout(() => chiudi(tendina), 350);
    });
    tendina.querySelector("[data-chiudi-tendina]")?.addEventListener("click", () => chiudi(tendina, { focus: true }));
    // aprendone una, l'altra si chiude
    tendina.addEventListener("toggle", () => {
      if (tendina.open) tendine.forEach((altra) => altra !== tendina && (altra.open = false));
    });
  });

  document.addEventListener("click", (evento) => {
    tendine.forEach((tendina) => !tendina.contains(evento.target) && chiudi(tendina));
  });
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape") tendine.forEach((tendina) => chiudi(tendina, { focus: true }));
  });

  // "la ricevi tra il … e il …": ricalcolata sul giorno di chi guarda,
  // saltando sabato e domenica (come consegna_stimata in configuratore.py)
  const consegna = document.querySelector("[data-consegna]");
  if (consegna) {
    const piuGiorniLavorativi = (giorno, quanti) => {
      const d = new Date(giorno);
      while (quanti > 0) {
        d.setDate(d.getDate() + 1);
        if (d.getDay() !== 0 && d.getDay() !== 6) quanti--;
      }
      return d;
    };
    const comeData = (d) => {
      const testo = d.toLocaleDateString("it-IT", { day: "numeric", month: "long" });
      return d.getDate() === 1 ? testo.replace(/^1 /, "1° ") : testo;
    };
    const pronta = piuGiorniLavorativi(new Date(), Number(consegna.dataset.lavorazione));
    consegna.querySelector("[data-consegna-da]").textContent = comeData(
      piuGiorniLavorativi(pronta, Number(consegna.dataset.spedizioneMin))
    );
    consegna.querySelector("[data-consegna-a]").textContent = comeData(
      piuGiorniLavorativi(pronta, Number(consegna.dataset.spedizioneMax))
    );
  }

  // barra d'acquisto: compare quando il bottone principale è passato sopra lo
  // schermo, cioè dopo averlo superato (non prima di arrivarci).
  // Si controlla a ogni scorrimento: così funziona anche se si arriva più in
  // basso con un salto, per esempio da un link.
  const bottone = document.querySelector("[data-bottone-principale]");
  const barra = document.querySelector("[data-barra-acquisto]");
  if (bottone && barra) {
    const controllaBarra = () => {
      barra.hidden = bottone.getBoundingClientRect().bottom > 0;
    };
    window.addEventListener("scroll", controllaBarra, { passive: true });
    controllaBarra();
  }

  // galleria: la miniatura della foto visibile viene evidenziata
  const galleria = document.querySelector("[data-galleria]");
  const miniature = [...document.querySelectorAll("[data-miniatura]")];
  if (galleria && miniature.length && "IntersectionObserver" in window) {
    const viste = [...galleria.children];
    const osservaFoto = new IntersectionObserver(
      (voci) => {
        voci.forEach((voce) => {
          if (!voce.isIntersecting) return;
          const i = viste.indexOf(voce.target);
          miniature.forEach((m, j) => m.setAttribute("aria-current", i === j ? "true" : "false"));
        });
      },
      { root: galleria, threshold: 0.6 }
    );
    viste.forEach((v) => osservaFoto.observe(v));

    // toccando una miniatura la galleria scorre, senza far saltare la pagina
    miniature.forEach((m, i) => {
      m.addEventListener("click", (evento) => {
        evento.preventDefault();
        galleria.scrollTo({ left: viste[i].offsetLeft, behavior: "smooth" });
      });
    });
  }
}

// 5. LA PAGINA CONTATTI ------------------------------------------------------
// Sotto il messaggio c'è un suggerimento su cosa scrivere: cambia con il
// motivo scelto. I testi stanno in dati/contatti.py (MOTIVI).

const moduloContatti = document.querySelector("[data-modulo-contatti]");

if (moduloContatti) {
  const suggerimento = moduloContatti.querySelector("[data-suggerimento-testo]");
  moduloContatti.addEventListener("change", (evento) => {
    if (evento.target.name === "motivo") {
      suggerimento.textContent = evento.target.dataset.suggerimento;
    }
  });
}
