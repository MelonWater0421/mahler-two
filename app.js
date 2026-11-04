/**
 * Mahler Symphony No. 2 ("Resurrection") — UI State Machine & Bilingual Controller
 */
(function () {
  function initAtlas() {
    if (!window.SYMPHONY_DATA) return;
    const engine = new window.SymphonyAtlasEngine(window.SYMPHONY_DATA);
    const canvas = document.getElementById('rms-canvas');
    const stageList = document.getElementById('stage-list');
    let lang = 'bilingual';

    function render() {
      engine.renderWaveform(canvas);
      const active = engine.getActiveStage();
      if (!stageList) return;
      stageList.innerHTML = engine.currentMovement.stages
        .map(
          (s) => `
        <article class="stage-card ${s.id === active.id ? 'active' : ''}" data-sec="${s.sec}">
          <div style="font-size:12px;color:#a8a29e;">Bar ${s.bar}–${s.bar_end} · ${s.reh} · ${s.sec.toFixed(1)}s</div>
          <h3 style="margin:6px 0;font-size:16px;">${lang === 'en' ? s.title_en : s.title}</h3>
          ${lang === 'bilingual' ? `<div style="font-size:13px;color:#d6d3d1;margin-bottom:6px;">${s.title_en}</div>` : ''}
          <p style="font-size:13px;color:#a8a29e;">${lang === 'en' ? s.desc_en : s.desc}</p>
        </article>`
        )
        .join('');
    }

    if (canvas) {
      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const ratio = (e.clientX - rect.left) / rect.width;
        engine.seek(ratio * engine.currentMovement.duration_sec);
        render();
      });
    }

    render();
  }

  window.addEventListener('DOMContentLoaded', initAtlas);
})();
