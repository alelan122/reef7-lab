// Missione: mappa dei reef da sostenere (continenti da world-atlas, proiezione centrata sull'Indo-Pacifico).
(async () => {
  const box = document.getElementById("reef-map");
  if (!box || !window.d3 || !window.topojson) return;
  const svg = box.querySelector("svg");
  const ns = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent = svg) => {
    const n = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    parent.appendChild(n);
    return n;
  };
  const points = JSON.parse(box.dataset.points);
  const W = 1000, H = 500;
  const projection = d3.geoNaturalEarth1().rotate([-110, 0]).fitExtent([[10, 10], [W - 10, H - 10]], { type: "Sphere" });
  const path = d3.geoPath(projection);

  try {
    const world = await (await fetch(box.dataset.world)).json();
    const land = topojson.feature(world, world.objects.land);
    el("path", { d: path({ type: "Sphere" }), class: "sphere" });
    el("path", { d: path(d3.geoGraticule10()), class: "graticule" });
    el("path", { d: path(land), class: "land" });
  } catch {
    box.classList.add("no-land"); // senza connessione ai dati del mondo restano solo i punti
  }

  // rotta che collega i reef nell'ordine degli obiettivi
  const route = { type: "LineString", coordinates: points.map((p) => [p.lon, p.lat]) };
  el("path", { d: path(route), class: "route" });

  for (const p of points) {
    const [x, y] = projection([p.lon, p.lat]);
    const g = el("a", { href: `#g${p.n}`, class: `pin${p.active ? " active" : ""}`, transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})` });
    if (p.active) el("circle", { r: 18, class: "pulse" }, g);
    el("circle", { r: 11, class: "dot" }, g);
    const t = el("text", { y: 4, class: "num" }, g);
    t.textContent = p.n;
    // posizione dell'etichetta scelta per non sovrapporsi ai reef vicini
    const pos = [[/^Bali/, [-16, 26, "end"]], [/^Maldiv/, [-16, -10, "end"]], [/Barrier/, [-16, 28, "end"]], [/^Moorea/, [0, -20, "middle"]]].find(([r]) => r.test(p.name))?.[1] || [16, -12, "start"];
    const label = el("text", { x: pos[0], y: pos[1], "text-anchor": pos[2], class: "label" }, g);
    label.textContent = p.name;
  }
})();
