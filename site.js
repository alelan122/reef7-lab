// Reef 7 Lab: luce dell'acqua nell'hero, menu su telefono, modulo contatti.
(() => {
  const top = document.querySelector(".top");
  const menu = document.querySelector(".menu");
  const label = menu.textContent;
  menu.addEventListener("click", () => {
    const open = top.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
    menu.textContent = open ? menu.dataset.close : label;
  });

  // gallerie di schermate: le schede mostrano una schermata alla volta
  document.querySelectorAll("[data-gallery]").forEach((g) => {
    const imgs = g.querySelectorAll(".fr-shots img");
    const tabs = g.nextElementSibling.querySelectorAll("button");
    tabs.forEach((t, i) => t.addEventListener("click", () => {
      imgs.forEach((im, j) => { im.hidden = j !== i; });
      tabs.forEach((b, j) => b.setAttribute("aria-pressed", String(j === i)));
    }));
  });

  // su telefono i blocchi lunghi si aprono a richiesta (su desktop il pulsante è nascosto)
  const en = document.documentElement.lang === "en";
  document.querySelectorAll(".svc, .case, .principle, .about-bio, .project-info").forEach((el) => {
    const more = el.dataset.more || (en ? "Read more" : "Scopri di più"), less = en ? "Show less" : "Mostra meno";
    const b = document.createElement("button");
    b.type = "button"; b.className = "fold-btn"; b.textContent = more; b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", () => { const o = el.classList.toggle("open"); b.textContent = o ? less : more; b.setAttribute("aria-expanded", o); });
    el.classList.add("fold");
    el.appendChild(b);
  });

  // modulo contatti in tre passi: controlla ogni passo, poi invia tutte le risposte via FormSubmit (arrivano nella casella del Lab)
  const form = document.getElementById("contact-form");
  if (form) {
    const d = form.dataset;
    const steps = [...form.querySelectorAll(".q-step")];
    const back = form.querySelector(".q-back"), next = form.querySelector(".q-next"), send = form.querySelector(".q-send");
    const msg = form.querySelector(".form-msg");
    let cur = 0;

    // arrivo dalla demo dell'agente: le risposte date in chat precompilano il modulo
    const qs = new URLSearchParams(location.search);
    if (qs.has("need")) {
      const vals = qs.get("need").split("|");
      form.querySelectorAll('input[name="need"]').forEach((x) => { x.checked = vals.includes(x.value); });
      ["team", "when"].forEach((k) => form.querySelectorAll(`input[name="${k}"]`).forEach((x) => { x.checked = x.value === qs.get(k); }));
      if (qs.get("goal") && !form.goal.value) form.goal.value = `${qs.get("goal")}: `;
    }

    const show = (i) => {
      cur = i;
      steps.forEach((s, j) => { s.hidden = j !== i; });
      back.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      send.hidden = i !== steps.length - 1;
      form.querySelector(".q-count").textContent = d.stepOf.replace("{a}", i + 1).replace("{b}", steps.length);
      form.querySelector(".q-name").textContent = steps[i].dataset.name;
      form.querySelector(".q-progress b").style.width = `${((i + 1) / steps.length) * 100}%`;
      msg.textContent = "";
    };

    // campi obbligatori del passo: testo, email, consenso e gruppi di scelta
    const valid = (step) => {
      let first = null;
      step.querySelectorAll("input[required], textarea[required]").forEach((el) => {
        const bad = el.type === "checkbox" ? !el.checked : !el.value.trim() || (el.type === "email" && !el.validity.valid);
        el.closest(".field, .check").classList.toggle("invalid", bad);
        if (bad && !first) first = el;
      });
      step.querySelectorAll(".q-field[data-required]").forEach((g) => {
        const bad = !g.querySelector("input:checked");
        g.classList.toggle("invalid", bad);
        if (bad && !first) first = g.querySelector("input");
      });
      if (first) first.focus();
      return !first;
    };

    next.addEventListener("click", () => { if (valid(steps[cur])) { show(cur + 1); form.scrollIntoView({ block: "nearest", behavior: "smooth" }); } });
    back.addEventListener("click", () => show(cur - 1));
    form.addEventListener("input", (e) => e.target.closest(".field, .check, .q-field")?.classList.remove("invalid"));
    form.addEventListener("change", (e) => e.target.closest(".q-field")?.classList.remove("invalid"));
    form.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.tagName === "INPUT" && cur < steps.length - 1) { e.preventDefault(); next.click(); } });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!valid(steps[cur])) return;
      const f = new FormData(form);
      if (f.get("_honey")) return; // compilato solo dai bot
      const all = (k) => f.getAll(k).join(", ") || "—";
      const one = (k) => (f.get(k) || "").toString().trim() || "—";
      const label = send.innerHTML;
      send.disabled = true;
      send.textContent = d.sending;
      try {
        const res = await fetch(d.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            _subject: `${d.subject}: ${one("company")} · ${all("need")}`,
            _replyto: one("email"), _template: "table", _captcha: "false",
            "Di cosa ha bisogno": all("need"), "Obiettivo": one("goal"),
            "Azienda": one("company"), "Sito": one("site"), "Settore": one("sector"), "Persone in azienda": one("team"), "Strumenti usati": one("tools"),
            "Quando partire": one("when"), "Budget indicativo": one("budget"),
            "Nome": one("nome"), "Ruolo": one("role"), "Email": one("email"), "Telefono": one("phone"), "Come ci ha conosciuto": one("source"),
          }),
        });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || out.success === false || out.success === "false") throw new Error(out.message || res.status);
        form.hidden = true;
        form.parentElement.querySelector(".form-ok").hidden = false;
        form.parentElement.querySelector("h2").hidden = true;
      } catch {
        msg.innerHTML = `${d.err} <a href="mailto:${d.email}">${d.email}</a>.`;
        send.disabled = false;
        send.innerHTML = label;
      }
    });
  }

  // un unico sistema: le schede mostrano un flusso alla volta e scorrono da sole finché non ne scegli una
  const flow = document.querySelector("[data-flow]");
  if (flow) {
    const tabs = flow.querySelectorAll(".flow-tabs button");
    const panels = flow.querySelectorAll(".flow-panel");
    let current = 0, timer = null;
    const show = (i) => {
      current = i;
      panels.forEach((p, j) => { p.hidden = j !== i; });
      tabs.forEach((t, j) => t.setAttribute("aria-pressed", String(j === i)));
    };
    tabs.forEach((t, i) => t.addEventListener("click", () => { clearInterval(timer); show(i); }));
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const io = new IntersectionObserver(([e]) => {
        clearInterval(timer);
        if (e.isIntersecting && !flow.dataset.picked) timer = setInterval(() => show((current + 1) % panels.length), 6000);
      }, { threshold: 0.4 });
      io.observe(flow);
      tabs.forEach((t) => t.addEventListener("click", () => { flow.dataset.picked = "1"; }));
    }
  }

  // caustiche: la luce che filtra dalla superficie e danza sul fondale (shader WebGL)
  const canvas = document.getElementById("water");
  if (!canvas || !canvas.offsetParent) return; // nella versione B il canvas è nascosto
  const gl = canvas.getContext("webgl", { antialias: false, alpha: true, premultipliedAlpha: false });
  if (!gl) return;
  const vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const fs = `precision mediump float;
uniform vec2 r;uniform float t;
float caustic(vec2 uv,float time){
  vec2 p=mod(uv*6.2831,6.2831)-250.;vec2 i=p;float c=1.;float inten=.005;
  for(int n=0;n<4;n++){float tt=time*(1.-(3.5/float(n+1)));
    i=p+vec2(cos(tt-i.x)+sin(tt+i.y),sin(tt-i.y)+cos(tt+i.x));
    c+=1./length(vec2(p.x/(sin(i.x+tt)/inten),p.y/(cos(i.y+tt)/inten)));}
  c/=4.;c=1.17-pow(c,1.4);return pow(abs(c),8.);}
void main(){
  vec2 uv=gl_FragCoord.xy/r;vec2 q=vec2(uv.x*r.x/r.y,uv.y)*.55;
  float c=caustic(q,t*.18);
  float depth=smoothstep(0.,1.,uv.y);
  vec3 deep=vec3(.016,.031,.059);vec3 mid=vec3(.03,.16,.32);vec3 lit=vec3(.37,.88,.95);
  vec3 col=mix(deep,mid,depth*.9);
  col+=lit*c*(.18+.55*depth);
  float rays=pow(max(0.,sin((uv.x+uv.y*.35)*9.+t*.25)*.5+.5),6.)*depth*.12;
  col+=lit*rays;
  gl_FragColor=vec4(col,1.);}`;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uR = gl.getUniformLocation(prog, "r"), uT = gl.getUniformLocation(prog, "t");

  // risoluzione ridotta: l'effetto è morbido e resta leggero anche sui portatili
  const resize = () => {
    const scale = Math.min(window.devicePixelRatio || 1, 1) * 0.6;
    canvas.width = Math.max(1, canvas.clientWidth * scale);
    canvas.height = Math.max(1, canvas.clientHeight * scale);
    gl.viewport(0, 0, canvas.width, canvas.height);
  };
  resize();
  window.addEventListener("resize", resize);

  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
  const start = performance.now();
  const frame = (now) => {
    if (visible) {
      gl.uniform2f(uR, canvas.width, canvas.height);
      gl.uniform1f(uT, still ? 12 : (now - start) / 1000 + 12);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    if (!still) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
})();
