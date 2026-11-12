        const tl = gsap.timeline({ paused: true });
        const cues = [];
        const cue = (t, name, g = 1) => cues.push([+t.toFixed(3), name, g]);
        const sid = (n) => "s" + String(n).padStart(2, "0");
        const S = (n) => document.getElementById(sid(n));
        const inner = (n) => S(n).querySelector(".inner");
        const cam = (n) => S(n).querySelector(".cam");
        const $$ = (sel) => Array.from(document.querySelectorAll(sel));

        // typewriter-by-word: every .w gets its spoken time (data-t, or W(data-n, data-w | text))
        function typeIn(sel, sound = "blip") {
          let last = 0; const out = [];
          $$(sel + " .w, " + sel + ".w").forEach((el) => {
            let t = el.dataset.t ? +el.dataset.t : (el.dataset.n ? W(+el.dataset.n, el.dataset.w || el.textContent) : null);
            if (t == null) t = last + 0.12; last = t; out.push(t);
            tl.fromTo(el, { opacity: 0, y: 12, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.14, ease: "power2.out", immediateRender: false }, t);
            if (sound) cue(t, sound, 1);
          });
          return out;
        }
        const T = (n, word) => W(n, word);  // lookup without typing (cursor advances; use for unique words)
        function blurOut(sel, t, d = 0.25) { tl.to(sel, { opacity: 0, filter: "blur(16px)", y: -10, duration: d, ease: "power1.in" }, t); }
        function show(sel, t, d = 0.3, from = { y: 40, scale: 0.9 }, sound = "paper", g = 0.8) {
          tl.set(sel, { opacity: 0 }, 0);
          tl.fromTo(sel, { opacity: 0, ...from }, { opacity: 1, y: 0, x: 0, scale: 1, duration: d, ease: "back.out(1.6)", immediateRender: false }, t);
          if (sound) cue(t, sound, g);
        }
        function stamp(sel, t, rot = -8, shakeCam = null) {
          tl.set(sel, { opacity: 0 }, 0);
          tl.fromTo(sel, { opacity: 0, scale: 2.3, rotation: rot - 14 }, { opacity: 0.95, scale: 1, rotation: rot, duration: 0.16, ease: "power4.in", immediateRender: false }, t);
          cue(t + 0.14, "stamp", 1);
          if (shakeCam) shake(shakeCam, t + 0.16, 7);
        }
        function draw(sel, t, d = 0.3, sound = "pencil") {  // red-ink stroke draws on
          $$(sel + " path").forEach((p) => { const L = p.getTotalLength ? p.getTotalLength() : 1000; p.style.strokeDasharray = L; p.style.strokeDashoffset = L; tl.to(p, { strokeDashoffset: 0, duration: d, ease: "power1.inOut" }, t); });
          if (sound) cue(t, sound, 1);
        }
        function shake(target, t, amp = 10) {
          [amp, -amp * 0.8, amp * 0.6, -amp * 0.4, amp * 0.2, 0].forEach((x, i) => tl.to(target, { x, y: (i % 2 ? -1 : 1) * amp * 0.4 * (1 - i / 6), duration: 0.035, ease: "none" }, t + i * 0.035));
        }
        function flash(t, g = 1) { tl.fromTo("#flash", { opacity: 0.9 }, { opacity: 0, duration: 0.28, ease: "power2.out", immediateRender: false }, t); cue(t, "flash", g); }
        // host: slide-up + 95->100% pop on entry and on every pose change, idle breathing
        function hostIn(n, t, end) {
          const h = S(n).querySelector(".host"); const imgs = h.querySelectorAll("img"); const br = h.querySelector(".br");
          tl.set(imgs[0], { opacity: 1 }, t);
          tl.fromTo(h, { y: 60, scale: 0.95 }, { y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)", immediateRender: false }, t);
          const reps = Math.max(1, Math.floor((end - t - 0.35) / 1.1));
          tl.fromTo(br, { scale: 1 }, { scale: 1.015, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: reps - 1, immediateRender: false }, t + 0.35);
        }
        function pose(n, idx, t, sound = "flick") {
          const h = S(n).querySelector(".host");
          h.querySelectorAll("img").forEach((im, i) => tl.set(im, { opacity: i === idx ? 1 : 0 }, t));
          tl.fromTo(h, { y: 40, scale: 0.95 }, { y: 0, scale: 1, duration: 0.24, ease: "back.out(2.2)", immediateRender: false }, t);
          if (sound) cue(t, sound, 0.8);
        }
        function pushIn(n, t0, t1, to = 1.04) { tl.fromTo(cam(n), { scale: 1 }, { scale: to, duration: t1 - t0, ease: "none", immediateRender: false }, t0); }
        function blinds(n, t0, t1) { const b = S(n).querySelector(".blinds"); if (b) tl.fromTo(b, { x: 0 }, { x: -60, duration: t1 - t0, ease: "none", immediateRender: false }, t0); }
        function swapIn(sel, t) { tl.set(sel, { opacity: 1 }, t); }

        // ---------- transitions (0.2–0.4s) ----------
        function tBlur(n, cut) {
          tl.fromTo(inner(n), { opacity: 0, filter: "blur(20px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "power2.out", immediateRender: false }, cut - 0.16);
          tl.to(inner(n - 1), { opacity: 0, filter: "blur(16px)", duration: 0.28, ease: "power1.in" }, cut - 0.14);
          cue(cut - 0.16, "whoosh", 0.4);
        }
        function tDip(n, cut) {
          tl.to(inner(n - 1), { opacity: 0, duration: 0.2, ease: "power1.in" }, cut - 0.22);
          tl.fromTo(inner(n), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out", immediateRender: false }, cut + 0.02);
          cue(cut - 0.22, "whoosh-low", 0.5);
        }
        function tBurn(n, cut) {
          tl.fromTo("#burn", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1.3, duration: 0.16, ease: "power2.in", immediateRender: false }, cut - 0.16);
          tl.to("#burn", { opacity: 0, duration: 0.26, ease: "power2.out" }, cut);
          tl.set(inner(n), { opacity: 1 }, cut); tl.set(inner(n - 1), { opacity: 0 }, cut);
          cue(cut - 0.16, "burn", 0.8);
        }
        function tIris(n, cut, x = "50%", y = "62%") {  // spotlight iris wipe with a warm rim
          tl.set(inner(n), { opacity: 1 }, cut - 0.2);
          tl.fromTo(inner(n), { clipPath: `circle(0% at ${x} ${y})` }, { clipPath: `circle(85% at ${x} ${y})`, duration: 0.4, ease: "power2.in", immediateRender: false }, cut - 0.2);
          tl.set(inner(n), { clipPath: "none" }, cut + 0.21);
          tl.set(inner(n - 1), { opacity: 0 }, cut + 0.21);
          cue(cut - 0.2, "whoosh", 0.45);
        }
        function tSlide(n, cut) {  // card/page slide up over the previous scene
          tl.set(inner(n), { opacity: 1 }, cut - 0.18);
          tl.fromTo(inner(n), { y: 1920, rotation: 3 }, { y: 0, rotation: 0, duration: 0.36, ease: "power3.out", immediateRender: false }, cut - 0.18);
          tl.to(inner(n - 1), { y: -180, opacity: 0, duration: 0.36, ease: "power2.in" }, cut - 0.18);
          cue(cut - 0.18, "paper", 0.9);
        }
