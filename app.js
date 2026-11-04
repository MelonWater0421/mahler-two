/**
 * Mahler Symphony No. 2 ("Resurrection") — Standalone GitHub Pages Application Controller
 * Supports Desktop & Mobile viewports, 5 movements, DTW time calibration, Religious Context, and Polyphony Synth
 */
(function () {
  function formatTime(sec) {
    const s = Math.max(0, Math.floor(sec));
    const m = Math.floor(s / 60);
    const r = s % 60;
    return String(m).padStart(2, '0') + ':' + String(r).padStart(2, '0');
  }

  function init() {
    const data = window.SYMPHONY_DATA;
    if (!data) return;
    const engine = new window.SymphonyAtlasEngine(data);
    let lang = 'bilingual';

    const mvtTabs = document.getElementById('mvt-tabs');
    const anchorRail = document.getElementById('anchor-rail');
    const canvas = document.getElementById('rms-canvas');
    const stageInspector = document.getElementById('stage-inspector');
    const stageList = document.getElementById('stage-list');
    const theologyGrid = document.getElementById('theology-grid');
    const langBtn = document.getElementById('lang-toggle');
    const themeBtn = document.getElementById('theme-toggle');

    function render() {
      const mvt = engine.currentMovement;
      const active = engine.getActiveStage();

      // Render Movement Tabs
      if (mvtTabs) {
        mvtTabs.innerHTML = data.movements
          .map(
            (m, idx) =>
              `<button class="btn ${idx === engine.currentMvtIndex ? 'active' : ''}" data-mvt="${idx}">
                Mvt ${m.id} (${m.bars}m · ${formatTime(m.duration_sec)})
              </button>`
          )
          .join('');
        mvtTabs.querySelectorAll('button').forEach((b) => {
          b.addEventListener('click', () => {
            engine.currentMvtIndex = Number(b.getAttribute('data-mvt'));
            engine.seek(0.4);
            render();
          });
        });
      }

      // Render Rehearsal Anchors
      if (anchorRail) {
        anchorRail.innerHTML = mvt.anchors
          .map(
            (a) =>
              `<button class="btn" data-sec="${a.sec}">${a.reh} · m.${a.bar} (${a.dynamic})</button>`
          )
          .join('');
        anchorRail.querySelectorAll('button').forEach((b) => {
          b.addEventListener('click', () => {
            engine.seek(Number(b.getAttribute('data-sec')));
            render();
          });
        });
      }

      engine.renderWaveform(canvas);

      // Render Live Stage Inspector
      const mvtCtx =
        data.religious_context &&
        data.religious_context.movements_context &&
        data.religious_context.movements_context[String(mvt.id)];

      if (stageInspector) {
        stageInspector.innerHTML = `
          <div style="font-family:monospace;font-size:12px;color:var(--text-secondary);">
            Stage ${active.stage_index}/${mvt.stages.length} · Bars ${active.bar}–${active.bar_end} · ${active.reh} · ${formatTime(active.sec)}–${formatTime(active.sec_end)}
          </div>
          <h2 style="margin:8px 0 4px;font-size:20px;">${lang === 'en' ? active.title_en : active.title}</h2>
          ${lang === 'bilingual' ? `<div style="font-size:14px;color:var(--text-secondary);margin-bottom:10px;">${active.title_en}</div>` : ''}
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;">
            <div style="padding:12px;border-radius:8px;background:var(--bg-elevated);">
              <strong style="font-size:12px;color:var(--accent-gold-light);">Foreground Principal Voice</strong>
              <p style="font-size:13px;margin-top:4px;">${lang === 'en' ? active.fg_en : active.fg}</p>
            </div>
            <div style="padding:12px;border-radius:8px;background:var(--bg-elevated);">
              <strong style="font-size:12px;color:#38bdf8;">Background Texture & Pedal</strong>
              <p style="font-size:13px;margin-top:4px;">${lang === 'en' ? active.bg_en : active.bg}</p>
            </div>
          </div>
          ${
            active.vocal_text
              ? `<div style="padding:12px;border-radius:8px;border:1px solid var(--accent-gold);margin:12px 0;">
                  <div style="font-style:italic;font-weight:600;">“${active.vocal_text.de}”</div>
                  <div style="font-size:13px;margin-top:4px;">${active.vocal_text.zh}</div>
                  <div style="font-size:12px;color:var(--text-secondary);">${active.vocal_text.en}</div>
                </div>`
              : ''
          }
          <p style="font-size:14px;margin-top:10px;">${lang === 'en' ? active.desc_en : active.desc}</p>
          ${lang === 'bilingual' ? `<p style="font-size:13px;color:var(--text-secondary);margin-top:6px;">${active.desc_en}</p>` : ''}
          <div style="margin-top:12px;padding:10px;border-radius:8px;background:var(--bg-elevated);font-size:12px;">
            <strong>Listening Cue:</strong> ${lang === 'en' ? active.cue_en : active.cue_zh}
          </div>
          ${
            mvtCtx
              ? `<div style="margin-top:12px;padding:12px;border-radius:8px;border:1px solid var(--border-subtle);font-size:12px;">
                  <strong>${lang === 'en' ? mvtCtx.theme_en : mvtCtx.theme_zh}</strong>
                  <p style="margin-top:4px;color:var(--text-secondary);">${lang === 'en' ? mvtCtx.summary_en : mvtCtx.summary_zh}</p>
                </div>`
              : ''
          }
        `;
      }

      // Render Stage List
      if (stageList) {
        stageList.innerHTML = mvt.stages
          .map(
            (s) => `
          <button class="stage-card ${s.id === active.id ? 'active' : ''}" data-sec="${s.sec}">
            <div style="font-size:11px;font-family:monospace;color:var(--text-secondary);">
              #${s.stage_index} · Bars ${s.bar}–${s.bar_end} · ${s.reh} · ${formatTime(s.sec)}
            </div>
            <div style="font-weight:600;font-size:14px;margin-top:4px;">${lang === 'en' ? s.title_en : s.title}</div>
            ${lang === 'bilingual' ? `<div style="font-size:12px;color:var(--text-secondary);">${s.title_en}</div>` : ''}
          </button>`
          )
          .join('');
        stageList.querySelectorAll('button').forEach((b) => {
          b.addEventListener('click', () => {
            engine.seek(Number(b.getAttribute('data-sec')));
            render();
          });
        });
      }

      // Render Theological & Religious Context Pillars
      if (theologyGrid && data.religious_context) {
        theologyGrid.innerHTML = data.religious_context.pillars
          .map(
            (p) => `
          <article class="stage-card">
            <div style="font-size:11px;font-family:monospace;color:var(--accent-gold-light);">
              ${lang === 'en' ? p.tag_en : p.tag_zh}
            </div>
            <h3 style="font-size:16px;margin:6px 0;">${lang === 'en' ? p.title_en : p.title_zh}</h3>
            <p style="font-size:13px;color:var(--text-secondary);">${lang === 'en' ? p.body_en : p.body_zh}</p>
          </article>`
          )
          .join('');
      }
    }

    if (canvas) {
      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        engine.seek(ratio * engine.currentMovement.duration_sec);
        render();
      });
    }

    if (langBtn) {
      langBtn.addEventListener('click', () => {
        lang = lang === 'bilingual' ? 'zh' : lang === 'zh' ? 'en' : 'bilingual';
        langBtn.textContent = 'Lang: ' + lang.toUpperCase();
        render();
      });
    }

    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        document.documentElement.classList.toggle('light');
        render();
      });
    }

    render();
  }

  window.addEventListener('DOMContentLoaded', init);
})();
