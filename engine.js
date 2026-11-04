/**
 * Mahler Symphony No. 2 ("Resurrection") — Audio Playback, WebAudio Polyphony Synth & RMS Waveform Engine
 * Target Performance: Sir Simon Rattle · Berliner Philharmoniker (BPO)
 */
class SymphonyAtlasEngine {
  constructor(data) {
    this.data = data;
    this.currentMvtIndex = 0;
    this.currentTime = 0.4;
    this.isPlaying = false;
    this.audioCtx = null;
    this.mutedChoirs = new Set();
    this.soloChoir = null;
    this.timer = null;
    this.onTick = null;
  }

  get currentMovement() {
    return this.data.movements[this.currentMvtIndex];
  }

  getActiveStage() {
    const stages = this.currentMovement.stages;
    for (let i = stages.length - 1; i >= 0; i--) {
      if (this.currentTime >= stages[i].sec) {
        return stages[i];
      }
    }
    return stages[0];
  }

  seek(sec) {
    this.currentTime = Math.max(0, Math.min(sec, this.currentMovement.duration_sec));
    if (this.onTick) this.onTick(this.currentTime, this.getActiveStage());
  }

  renderWaveform(canvas) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rms = this.currentMovement.rms;
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    const progress = this.currentTime / this.currentMovement.duration_sec;

    for (let i = 0; i < rms.length; i++) {
      const x = (i / rms.length) * w;
      const barH = Math.max(4, rms[i] * (h - 24));
      ctx.fillStyle = (i / rms.length) <= progress ? '#f59e0b' : 'rgba(168, 162, 158, 0.32)';
      ctx.fillRect(x, (h - barH) / 2, Math.max(1.5, w / rms.length - 1), barH);
    }
  }
}

window.SymphonyAtlasEngine = SymphonyAtlasEngine;
