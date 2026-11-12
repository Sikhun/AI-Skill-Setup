        // ---------- Vintage sketch props: sepia pencil line (.ink) + red chalk (.chalk), wobble via #rough / #chalkf ----------
        // Use: <div class="svg" data-svg="name" style="..."></div>. Paths draw on with draw(sel, t).
        const PI = 'class="ink"', CH = (w = 12) => `class="chalk" stroke-width="${w}" filter="url(#chalkf)"`;
        const HATCH = '#7A5C43';
        const SV = {
          bub: () => `<svg viewBox="0 0 260 200"><g filter="url(#rough)"><path ${PI} d="M40 30 Q130 8 220 30 Q250 60 236 110 Q220 140 150 142 L110 186 L112 142 Q40 140 26 104 Q16 60 40 30Z" fill="#F7F0DF"/>
            <circle cx="90" cy="88" r="9" fill="${HATCH}"/><circle cx="130" cy="88" r="9" fill="${HATCH}"/><circle cx="170" cy="88" r="9" fill="${HATCH}"/></g></svg>`,
          bubq: () => `<svg viewBox="0 0 260 200"><g filter="url(#rough)"><path ${PI} d="M40 30 Q130 8 220 30 Q250 60 236 110 Q220 140 150 142 L110 186 L112 142 Q40 140 26 104 Q16 60 40 30Z" fill="#F7F0DF"/>
            <path ${CH(10)} d="M106 62 Q108 40 132 40 Q156 42 154 62 Q152 78 132 84 L132 100"/><circle cx="132" cy="120" r="7" fill="#A8432A"/></g></svg>`,
          qmark: () => `<svg viewBox="0 0 240 340"><path ${CH(26)} d="M48 96 Q48 22 122 20 Q196 22 196 92 Q196 148 132 172 Q118 180 118 214 L118 236"/>
            <path ${CH(26)} d="M110 296 L126 300"/></svg>`,
          heart: () => `<svg viewBox="0 0 200 180"><g filter="url(#rough)"><path ${PI} d="M100 164 Q20 110 22 62 Q26 18 66 18 Q92 18 100 48 Q108 18 134 18 Q174 18 178 62 Q180 110 100 164Z" fill="#E9C9B6"/>
            <path d="M44 60 Q46 40 64 34" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/></g></svg>`,
          scales: () => `<svg viewBox="0 0 300 300"><g filter="url(#rough)">
            <path ${PI} d="M150 40 L150 262 M100 268 L200 268 M120 262 L180 262"/><circle cx="150" cy="34" r="12" fill="#E6D6A8" stroke="#3A2A1E" stroke-width="5"/>
            <path ${PI} d="M40 70 L260 70"/><path ${PI} d="M60 70 L28 160 M60 70 L92 160 M240 70 L208 160 M240 70 L272 160"/>
            <path ${PI} d="M20 160 Q60 200 100 160 Z" fill="#E6D6A8"/><path ${PI} d="M200 160 Q240 200 280 160 Z" fill="#E6D6A8"/>
            <path d="M138 90 L138 250" stroke="${HATCH}" stroke-width="2" opacity=".6"/></g></svg>`,
          check: () => `<svg viewBox="0 0 200 160"><path ${CH(22)} d="M24 86 L76 136 L178 22"/></svg>`,
          magni: () => `<svg viewBox="0 0 300 300"><g filter="url(#rough)"><circle cx="118" cy="118" r="88" fill="rgba(255,255,255,.25)" stroke="#3A2A1E" stroke-width="10"/>
            <circle cx="118" cy="118" r="72" fill="none" stroke="${HATCH}" stroke-width="3" opacity=".6"/><path d="M70 82 Q86 60 112 56" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".8"/>
            <path ${PI} d="M184 184 L278 278" stroke-width="26"/><path d="M184 184 L278 278" stroke="#B08A3E" stroke-width="14" stroke-linecap="round"/></g></svg>`,
          scroll: () => `<svg viewBox="0 0 420 330"><g filter="url(#rough)">
            <path ${PI} d="M60 60 L360 60 L360 270 L60 270 Z" fill="#F2E6C8"/>
            <path ${PI} d="M40 40 Q40 80 60 80 L60 60 Q60 40 40 40 Z M380 290 Q380 250 360 250 L360 270 Q360 290 380 290Z" fill="#E2D2A8"/>
            <path ${PI} d="M40 40 L40 250 Q40 290 60 290 L380 290" /><path ${PI} d="M60 60 Q40 60 40 40"/>
            <path ${PI} stroke-width="3" d="M96 110 L320 110 M96 146 L300 146 M96 182 L324 182 M96 218 L250 218"/>
            <path ${PI} d="M300 230 Q360 120 410 20 Q380 110 318 236 Z" fill="#E6D6A8"/><path ${PI} stroke-width="3" d="M312 220 Q360 130 402 34"/></g></svg>`,
          cup: () => `<svg viewBox="0 0 360 320"><g filter="url(#rough)">
            <path ${PI} d="M30 70 Q180 100 330 70 Q320 170 180 180 Q40 170 30 70Z" fill="#E6D6A8"/>
            <path ${PI} d="M30 70 Q180 40 330 70"/><path ${PI} d="M60 76 Q180 96 300 76" stroke-width="3"/>
            <path ${PI} d="M28 90 Q-6 80 6 110 Q14 130 46 126 M332 90 Q366 80 354 110 Q346 130 314 126"/>
            <path ${PI} d="M170 180 L166 250 Q120 262 116 286 L244 286 Q240 262 194 250 L190 180" fill="#E6D6A8"/>
            <path d="M60 110 Q180 150 300 110" stroke="${HATCH}" stroke-width="3" fill="none" opacity=".7"/>
            <path ${CH(9)} d="M240 156 Q244 186 238 212"/><circle cx="238" cy="226" r="8" fill="#A8432A"/></g></svg>`,
          arrow: () => `<svg viewBox="0 0 300 140"><path ${CH(14)} d="M16 100 Q120 10 270 60"/><path ${CH(14)} d="M232 26 L272 60 L226 86"/></svg>`,
          plus: () => `<svg viewBox="0 0 200 200"><g filter="url(#rough)"><circle cx="100" cy="100" r="80" fill="#F7F0DF" stroke="#3A2A1E" stroke-width="7"/>
            <path ${CH(18)} d="M100 56 L100 144 M56 100 L144 100"/></g></svg>`,
          strike: () => `<svg viewBox="0 0 400 80" preserveAspectRatio="none"><path ${CH(14)} d="M8 52 Q120 22 220 40 Q300 52 392 24"/></svg>`,
          xmark: () => `<svg viewBox="0 0 200 200"><path ${CH(18)} d="M30 30 L170 170 M170 32 L32 170"/></svg>`,
          timeline: () => `<svg viewBox="0 0 860 140"><g filter="url(#rough)"><path ${PI} d="M20 70 L840 70 M20 40 L20 100 M840 40 L840 100 M20 70 L56 52 M20 70 L56 88 M840 70 L804 52 M840 70 L804 88"/>
            <path ${PI} stroke-width="3" d="M184 60 L184 80 M348 60 L348 80 M512 60 L512 80 M676 60 L676 80"/></g></svg>`,
          laurel: () => { let h = '<svg viewBox="0 0 420 330"><g filter="url(#rough)">'; const cx = 210, cy = 160, rx = 170, ry = 115, D = Math.PI / 180, Pt = (t) => [cx + rx * Math.cos(t), cy + ry * Math.sin(t)];
            for (const [t0, t1] of [[100, 225], [80, -45]]) { let d = ''; for (let i = 0; i <= 24; i++) { const [x, y] = Pt((t0 + (t1 - t0) * i / 24) * D); d += (i ? ' L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }
              h += `<path d="${d}" class="ink" stroke-width="3"/>`;
              for (let i = 1; i <= 8; i++) { const t = (t0 + (t1 - t0) * i / 8.6) * D; const [x, y] = Pt(t); let a = Math.atan2(ry * Math.cos(t), -rx * Math.sin(t)) / D; if (t1 < t0) a += 180;
                for (const o of [-1, 1]) h += `<ellipse cx="0" cy="-17" rx="8" ry="18" transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(a + 90 + o * 48).toFixed(0)})" fill="#E2CC98" stroke="#3A2A1E" stroke-width="2.5"/>`; } }
            return h + '</g></svg>'; },
          circ: () => `<svg viewBox="0 0 400 160" preserveAspectRatio="none"><path ${CH(8)} d="M200 10 C80 4 10 40 20 84 C34 140 330 150 384 100 C420 60 330 8 190 14 C170 16 150 22 140 28"/></svg>`,
        };
        document.querySelectorAll("[data-svg]").forEach((el) => { el.innerHTML = SV[el.dataset.svg](el.dataset.c); });
        // loose background pencil scribbles (seeded per scene)
        function rnd(s) { return () => { s = (s * 16807) % 2147483647; return s / 2147483647; }; }
        document.querySelectorAll("svg.scrib").forEach((sv) => { const r = rnd(+sv.dataset.seed); let h = "";
          for (let i = 0; i < 40; i++) { const edge = r() < .8; const x = edge ? (r() < .5 ? r() * 230 : 850 + r() * 230) : r() * 1080, y = r() * 1920; let d = `M${x.toFixed(0)} ${y.toFixed(0)}`;
            const n = 2 + Math.floor(r() * 4); for (let k = 0; k < n; k++) { const dx = (r() - .5) * 260, dy = (r() - .5) * 160; d += ` q${(dx * r()).toFixed(0)} ${(dy * 2 * r() - dy).toFixed(0)} ${dx.toFixed(0)} ${dy.toFixed(0)}`; }
            h += `<path d="${d}" fill="none" stroke="#5a4130" stroke-width="${(0.8 + r() * 1.6).toFixed(1)}" stroke-linecap="round" opacity="${(0.3 + r() * .5).toFixed(2)}"/>`; }
          sv.innerHTML = h; });
