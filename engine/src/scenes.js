        // EP.01 timeline (Vintage Sketch Studio). C[n] = cut where scene n+1 starts; P(n) = [start, end] of phrase n; W/T(n, "word") = spoken time.
        const C = [@CUTS];
        const DUR = @DUR;
        const NS = @NSCENES;
        const P = (n) => PH[n - 1];
        const fw = (n, w, fb) => T(n, w) ?? fb;
        for (let n = 1; n <= NS; n++) pushIn(n, Math.max(0, C[n - 1] - 0.4), Math.min(DUR, C[n] + 0.4), 1.05);
        tl.set(inner(1), { opacity: 1 }, 0);

        // torn-paper boil: every torn sticker/card swaps edge frames at 8 fps
        for (let k = 0; k < DUR * 8; k++) tl.set("#root", { attr: { "data-f": k % 3 } }, k / 8);

        // ---------- host (.pz pose layers) ----------
        function hIn(n, t, end) {
          const h = S(n).querySelector(".host"), pz = h.querySelectorAll(".pz"), br = h.querySelector(".br");
          tl.set(pz[0], { opacity: 1 }, t);
          tl.fromTo(h, { y: 90, scale: 0.94, rotation: -2 }, { y: 0, scale: 1, rotation: 0, duration: 0.34, ease: "back.out(1.7)", immediateRender: false }, t);
          const reps = Math.max(1, Math.floor((end - t - 0.35) / 1.1));
          tl.fromTo(br, { scale: 1, rotation: 0 }, { scale: 1.015, rotation: 0.6, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: reps - 1, immediateRender: false }, t + 0.35);
          cue(t, "paper", 0.7);
        }
        function hPose(n, idx, t, sound = "flick") {
          const h = S(n).querySelector(".host");
          h.querySelectorAll(".pz").forEach((p, i) => tl.set(p, { opacity: i === idx ? 1 : 0 }, t));
          tl.fromTo(h, { y: 40, scale: 0.95 }, { y: 0, scale: 1, duration: 0.24, ease: "back.out(2.2)", immediateRender: false }, t);
          if (sound) cue(t, sound, 0.8);
        }
        function swap(a, b, t) { blurOut(a, t - 0.12, 0.16); tl.set(b, { opacity: 1 }, t); }
        function card(sel, t, sound = "paper", g = 0.9) { show(sel, t, 0.3, { y: 70, scale: 0.85 }, sound, g); }
        function sv(sel, t, d = 0.35, sound = "pencil") { tl.set(sel, { opacity: 1 }, t); draw(sel, t, d, sound); }
        function count(sel, t, d, to, fmt = (v) => v.toLocaleString("en-US")) {
          const N = 14; for (let i = 0; i <= N; i++) tl.set(sel, { textContent: fmt(Math.round(to * Math.pow(i / N, 0.6))) }, t + d * i / N);
          cue(t, "tick", 0.7); cue(t + d, "stampsoft", 0.8);
        }

        // ---------- sketch transitions ----------
        const tSmudge = (n, cut) => { tBlur(n, cut); cue(cut - 0.16, "shh", 0.5); };
        const tPage = (n, cut) => tSlide(n, cut);
        function tPencil(n, cut) {  // new page appears as a rough pencil pass, then settles
          tl.set(inner(n), { opacity: 1 }, cut); tl.set(inner(n - 1), { opacity: 0 }, cut);
          tl.fromTo(inner(n), { filter: "grayscale(1) contrast(1.8) brightness(1.25)", scale: 1.04 }, { filter: "grayscale(0) contrast(1) brightness(1)", scale: 1, duration: 0.34, ease: "power2.out", immediateRender: false }, cut);
          cue(cut - 0.05, "pencil", 0.9);
        }
        function tErase(n, cut) {  // eraser wipe left to right
          tl.set(inner(n), { opacity: 1 }, cut - 0.18);
          tl.fromTo(inner(n), { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.36, ease: "power2.inOut", immediateRender: false }, cut - 0.18);
          tl.set(inner(n), { clipPath: "none" }, cut + 0.19); tl.set(inner(n - 1), { opacity: 0 }, cut + 0.19);
          cue(cut - 0.18, "scratch", 0.8);
        }
        function tInk(n, cut) {  // sepia ink dip
          tl.fromTo("#sepia", { opacity: 0 }, { opacity: 0.9, duration: 0.18, ease: "power2.in", immediateRender: false }, cut - 0.18);
          tl.to("#sepia", { opacity: 0, duration: 0.32, ease: "power2.out" }, cut);
          tl.set(inner(n), { opacity: 1 }, cut); tl.set(inner(n - 1), { opacity: 0 }, cut);
          cue(cut - 0.18, "whoosh-low", 0.7);
        }
        function tSlow(n, cut) {
          tl.fromTo(inner(n), { opacity: 0, filter: "blur(14px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "power1.out", immediateRender: false }, cut - 0.3);
          tl.to(inner(n - 1), { opacity: 0, duration: 0.5, ease: "power1.in" }, cut - 0.3);
          cue(cut - 0.3, "shh", 0.6);
        }
        function tFlash(n, cut) { flash(cut - 0.04, 0.8); tl.set(inner(n), { opacity: 1 }, cut); tl.set(inner(n - 1), { opacity: 0 }, cut); }
        const TR = { 2: tSmudge, 3: tPage, 4: tPencil, 5: tErase, 6: tPage, 7: tSmudge, 8: tPencil, 9: tPage, 10: tErase, 11: tSmudge, 12: tPage, 13: tSmudge, 14: tInk, 15: tSlow, 16: tFlash, 17: tPage };
        for (let n = 2; n <= NS; n++) TR[n](n, C[n - 1]);

        const TY = (n) => typeIn("#" + sid(n), "tick");

        // 01 hook
        TY(1); tl.fromTo("#s01-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out", immediateRender: false }, 0.1);
        hIn(1, 0.0, C[1]);
        // 02
        TY(2); hIn(2, C[1] + 0.05, C[2]);
        ["#s02-b1", "#s02-b2", "#s02-b3", "#s02-b4"].forEach((s, i) => show(s, P(2)[0] + 0.5 + i * 0.4, 0.26, { y: 30, scale: 0.6 }, "pop", 0.6));
        // 03
        TY(3); hIn(3, C[2] + 0.05, C[3]); card("#s03-id", fw(3, "ชาวกรีก", P(3)[0] + 1));
        // 04
        TY(4); hIn(4, C[3] + 0.05, C[4]);
        count("#s04-n", fw(4, "2,400", P(4)[0] + 1), 0.6, 2400);
        tl.set("#s04-tl", { opacity: 1 }, P(4)[0] + 0.3); draw("#s04-tl", P(4)[0] + 0.3, 0.6);
        show("#s04-l", P(4)[0] + 0.8, 0.25, { y: 10 }, null); show("#s04-r", P(4)[0] + 1.0, 0.25, { y: 10 }, null);
        // 05
        TY(5); hIn(5, C[4] + 0.05, C[5]);
        ["#s05-b1", "#s05-b2", "#s05-b3"].forEach((s, i) => show(s, P(5)[0] + 0.4 + i * 0.35, 0.26, { y: 30, scale: 0.6 }, "pop", 0.6));
        const t5 = fw(5, "ตั้งคำถาม", P(5)[0] + 2.6);
        swap("#s05-a", "#s05-b", t5); ["#s05-b1", "#s05-b2", "#s05-b3"].forEach((s) => blurOut(s, t5 - 0.1, 0.2)); sv("#s05-q", t5 + 0.05, 0.4, "scratch");
        // 06
        TY(6); hIn(6, C[5] + 0.05, C[6]);
        card("#s06-c1", P(7)[0], "slap"); show("#s06-ht", P(7)[0] + 0.3, 0.26, { scale: 0.4 }, "pop", 0.6);
        card("#s06-c2", P(8)[0], "slap"); tl.set("#s06-sc", { opacity: 1 }, P(8)[0] + 0.3); draw("#s06-sc", P(8)[0] + 0.3, 0.5);
        // 07
        TY(7); hIn(7, C[6] + 0.05, C[7]); card("#s07-c", P(9)[0] + 0.3);
        sv("#s07-ck", P(9)[0] + 0.7, 0.3, "scratch");
        const t7 = fw(9, "ถูกต้อง", P(9)[1] - 0.6); blurOut("#s07-ck", t7 - 0.05, 0.15); sv("#s07-q", t7, 0.35, "scratch"); shake(cam(7), t7 + 0.3, 6);
        // 08
        TY(8); hIn(8, C[7] + 0.05, C[8]); card("#s08-c", P(10)[0] + 0.5);
        show("#s08-mg", fw(10, "ตรวจสอบ", P(10)[0] + 2), 0.3, { scale: 0.6 }, "whoosh", 0.5);
        tl.to("#s08-mg", { x: -260, y: 160, duration: 1.4, ease: "sine.inOut" }, fw(10, "ตรวจสอบ", P(10)[0] + 2) + 0.3);
        // 09
        TY(9); hIn(9, C[8] + 0.05, C[9]); card("#s09-c", P(12)[0]);
        const t9 = fw(12, "กลับ", P(12)[0] + 1.3);
        swap("#s09-a", "#s09-b", t9); sv("#s09-x", t9, 0.25, "scratch"); hPose(9, 1, t9 + 0.1); shake(cam(9), t9 + 0.2, 6);
        // 10
        TY(10); hIn(10, C[9] + 0.05, C[10]); tl.set("#s10-sc", { opacity: 1 }, fw(13, "งานเขียน", P(13)[0] + 1.3)); draw("#s10-sc", fw(13, "งานเขียน", P(13)[0] + 1.3), 0.7);
        // 11
        TY(11); hIn(11, C[10] + 0.05, C[11]);
        card("#s11-a1", C[10] + 0.1); sv("#s11-ar", P(14)[0] + 0.6, 0.3, "whoosh"); card("#s11-a2", fw(14, "เพลโต", P(14)[0] + 0.7), "stampsoft");
        swap("#s11-a", "#s11-b", P(15)[0]);
        // 12
        TY(12); hIn(12, C[11] + 0.05, C[12]);
        const t12 = fw(17, "ถูกตัดสิน", P(17)[0] + 0.5), t12b = fw(17, "ประหาร", 39.806);
        swap("#s12-a", "#s12-b", t12); stamp("#s12-seal", t12b, -10, cam(12)); flash(t12b + 0.16, 0.5); hPose(12, 1, t12b + 0.18, null);
        // 13
        TY(13); hIn(13, C[12] + 0.05, C[13]); card("#s13-c", C[12] + 0.15);
        show("#s13-i1", fw(17, "ทำให้เยาวชน", 41.566), 0.25, { x: -30 }, "key", 0.9);
        show("#s13-i2", fw(17, "ไม่เคารพ", 42.966), 0.25, { x: -30 }, "key", 0.9);
        // 14
        TY(14); tl.set("#s14-cup", { opacity: 1 }, P(18)[0] + 0.4); draw("#s14-cup", P(18)[0] + 0.4, 1.0); cue(fw(18, "ดื่มยาพิษ", P(18)[0] + 1.3), "pour", 0.7);
        // 15
        TY(15); show("#s15-lr", P(19)[0] + 0.5, 0.8, { scale: 0.9 }, "shh", 0.5);
        // 16
        TY(16); hIn(16, C[15] + 0.05, C[16]); sv("#s16-q", fw(20, "วิธีตั้งคำถาม", P(20)[0] + 0.5) + 0.2, 0.4, "scratch");
        const t16 = fw(20, "ยังคงมีอิทธิพลต่อปรัชญา", P(20)[0] + 2.2);
        swap("#s16-a", "#s16-b", t16); blurOut("#s16-q", t16 - 0.1, 0.2);
        tl.set("#s16-tl", { opacity: 1 }, t16 + 0.1); draw("#s16-tl", t16 + 0.1, 0.6); show("#s16-l", t16 + 0.4, 0.25, { y: 10 }, null); show("#s16-r", t16 + 0.7, 0.25, { y: 10 }, "ding");
        // 17 CTA
        TY(17); hIn(17, C[16] + 0.05, C[17]);
        const t17 = fw(21, "อย่าลืม", P(21)[0] + 1.0);
        swap("#s17-a", "#s17-b", t17); card("#s17-lk", fw(21, "ไลก์", t17 + 0.5), "pop"); card("#s17-fl", fw(21, "และติดตาม", t17 + 0.9), "pop");
        swap("#s17-b", "#s17-c", P(22)[0]); blurOut("#s17-lk", P(22)[0], 0.2); blurOut("#s17-fl", P(22)[0], 0.2);
        tl.to(inner(17), { opacity: 0, duration: 0.35, ease: "power1.in" }, DUR - 0.35);
        tl.set("#s17-ht, #s17-pl", { opacity: 1 }, 0);
