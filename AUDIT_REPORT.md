# Mahler 2 audio alignment and polyphony audit

Date: 2026-11-04. Verdict: **PARTIAL — required acoustic gates do not pass.**

The implementation replaces fabricated acoustic envelopes and miniature MIDI stubs with measured audio diagnostics, 158 provisional alignment anchors, 16 sourced polyphonic scenes, and playable multi-track MIDI anthologies. It also restores the data interface expected by the existing player. It does **not** certify complete Kaplan/IGMG score accuracy or 80 ms score-to-recording alignment.

## Required verification result

Executed `python3 tools/blueprint.py`; exit status **1**, intentionally propagated because Gates 3 and 4 fail. The final measured run printed:

```text
[PASS] Gate 1: Syntax & Zero-Contamination -> Node.js syntax valid · 0 foreign symphony contaminations
[PASS] Gate 2: Granularity & Bilingual Completeness -> 194 stages · Avg 26.148814s (≤38s) · 0 missing ZH/EN fields · 0 continuity errors · 0 polyphony errors · 0 anchor errors
[FAIL] Gate 3: Measured Silence-Gap Check -> 11 stage starts below -37.5 dB relative to movement peak RMS · 80 ms analysis frames
[FAIL] Gate 4: Measured Dynamic Fidelity -> 6/19 fff/ffff stage windows contain measured normalized RMS ≥0.82
```

The generated artifacts remain reviewable even when verification fails; `qa_report.overall_passed` is false. No threshold was relaxed, no audio values were boosted, and failures were not converted into passes.

## Recording provenance conflict

The orchestra’s official catalog identifies the October 2010 sessions with Royal, Kožená and Rundfunkchor Berlin, but gives Movement I as **24:16 (1456 s)**. The bundled file and required contract give **22:34 (1354 s)**: a **102 s difference**. Official II–IV timings are 10:11 / 11:33 / 5:20; the seven Finale chapters total 35:01, compared with the bundled 35:03. This does not establish the cause of the differences, but prevents certification of the bundled first movement as the complete unedited catalog release. The files contain encoder tags, without album or performer authentication. [Official Berliner Philharmoniker Recordings tracklist](https://www.berliner-philharmoniker-recordings.com/simon-rattle-the-berlin-years-tracklist?___store=rec_en).

The duration requirements and audio assets were retained. Calibration therefore targets the **bundled files with the supplied attribution**, with the provenance discrepancy exposed in the bilingual player notes and anchor metadata. Replacing or expanding the MP3s is outside the allowed file targets.

## Alignment method and tempo curves

The previous 54 anchors were replaced by 158 estimates: 30 / 28 / 32 / 28 / 40. Audio was decoded to mono 8 kHz; a Hann STFT used 8192 samples and a 4000-sample hop (0.5 s). Spectrally whitened twelve-bin chroma was compared with pitched-note chroma from the credited Junji Miki digitization. Cosine-distance DTW used symmetricP1 slope constraints and a normalized diagonal band of ±0.16. An independent symmetric2 path supplies a sensitivity check. Parameters, individual source URLs, checksums and coordinates are recorded in `tools/anchors.json`. [Digitizer catalog and attribution](https://gustavmahler.com/midi.html).

The 0.5 s hop, approximately 1.024 s analysis window, and 80 ms RMS frames describe sampling, **not measured score-timestamp error**. There is no manually annotated ground-truth timing set. The former `dtw_tolerance_sec=0.08` claim was removed. Timing hints are explicitly heuristic, not confidence intervals or certified error bounds.

| Movement | Anchors before → after | Median absolute shift (s) | Maximum shift (s) | Seconds per display bar, min–max | Maximum DTW-path disagreement (s) |
|---|---:|---:|---:|---:|---:|
| 1 | 13 → 30 | 25.895 | 68.000 | 1.4222–4.8487 | 46.739 |
| 2 | 8 → 28 | 4.356 | 14.444 | 1.6152–2.4733 | 19.318 |
| 3 | 9 → 32 | 9.162 | 28.517 | 0.9565–1.6919 | 12.525 |
| 4 | 7 → 28 | 6.368 | 25.510 | 0.9750–5.1800 | 3.000 |
| 5 | 17 → 40 | 44.896 | 150.961 | 0.9547–7.1600 | 42.000 |

**27 anchors** have inter-path disagreement above 3 s; maximum disagreement is **46.739 s**. Repeated orchestral material and sparse/quiet passages remain ambiguous. A denser anchor count alone does not prove improved absolute accuracy. All anchors have paired English/Chinese event descriptions, strictly increasing coordinates, and exclusive end boundaries 446 / 300 / 582 / 141 / 765.

The bar axes deliberately preserve the task’s counts: 445 / 299 / 581 / 140 / 764. They are not all equivalent to printed score bars. The source has setup/pickup measures; its Urlicht ruler contains approximately 68 full measures plus a pickup, rather than 140. Movement IV’s requested display grid is consequently a documented proportional conversion. Finale free-time subdivisions also differ around the Great Summons and chorus. `source_q` and `source_grid_bar` retain the digitization’s coordinates; scene jumps interpolate **source quarter positions**, rather than silently treating all rulers as identical.

The automatically estimated chorus coordinate is approximately 1228.353 s, compared with the official chapter boundary at 1226 s; the O-glaube coordinate is 1617.5 s, compared with the chapter boundary at 1616 s. Chapter boundaries are not certified first-note times. The old chorus anchor was 1297.72 s.

## Stage timing and acoustic measurement

Compilation now writes only `data.js` and the five authorized MIDI files. It does not overwrite RMS JSON assets or create public/src mirrors. Each movement includes actual measured RMS frames, source-file SHA-256, decoded duration and a peak-pooled 600-point display waveform. The player uses this embedded measured waveform.

For each non-overlapping 80 ms frame, RMS is `sqrt(sum(x²)/N)`. Normalized energy is frame RMS divided by the maximum measured frame RMS of that movement. Gate 3 uses `20 log10(normalized RMS) < -37.5`; absolute dBFS values are retained separately. Gate 4 uses actual normalized frame RMS ≥0.82 inside the stage window, without the former padded search. A level of 0.82 is within **1.724 dB** of the movement’s single loudest RMS frame; a printed dynamic is not by itself a guarantee of that level.

The old generator clamped its invented envelope to at least 0.08 and raised annotated climax windows to 0.90–0.95. Those operations made silence/dynamic passes circular. They have been removed. An independent initial readout of the old mapping found only 2/20 annotated windows meeting the measured peak criterion, despite the old reported 20/20 pass.

| Movement | Stages | Decoded duration (s) | Peak absolute frame RMS | Below-floor starts | Climax windows passing / checked |
|---|---:|---:|---:|---:|---:|
| 1 | 58 | 1354.000000 | 0.385620931 | 3 | 0/1 |
| 2 | 22 | 611.226750 | 0.240354628 | 0 | 0/0 |
| 3 | 25 | 692.826750 | 0.512575853 | 0 | 1/1 |
| 4 | 12 | 320.213375 | 0.157080593 | 0 | 0/0 |
| 5 | 77 | 2103.000000 | 0.438823798 | 8 | 5/17 |

There are **194 stages**, mean **26.148814 s**, range **5.73–81.52 s**. The contract specifies an average limit, not a maximum for every stage. The former 157.21 s Finale coda card is now five shorter cards. Bar/time boundaries are contiguous through each movement’s end; opening guide nodes follow the initial low-level preroll. Forced minimum durations and last-bar/end-boundary mistakes were removed.

Eleven generic silence-to-sound corrections move interpolated boundaries forward by at most **0.41 s** (configured limit 0.5 s). Their original times and changes remain in each stage. A separate, SHA-bound source-supported exception addresses Finale bar 142: its rehearsal marker is a general pause at 405.0 s, with no source notes before q507; the listening card begins at the first qualifying sound at **409.36 s**, while preserving the marker time and evidence. This is a 4.36 s rest-to-first-attack correction, not a general tolerance increase.

Floating-point indexing at exactly 4.56 s and 275.84 s formerly selected the preceding 80 ms frame. A tiny arithmetic tolerance before floor/ceil resolves this defect; both intended frames pass. This does not move either musical timestamp.

## Published-score checks and corrected descriptions

The available primary score is an early published UE reprint, not the requested Kaplan/IGMG critical edition. Its images were visually checked using the PDF skill workflow. No claim of an exhaustive critical-edition audit is made. [Published full-score scan](https://ks15.imslp.org/files/imglnks/usimg/e/e2/IMSLP415748-PMLP49406-GMahler_Symphony_No.2_fe_UE_reprint_RSL1.pdf).

| Passage | Primary-score finding | Implemented correction |
|---|---|---|
| I, bars 180–193, printed pp.22–24 | After rehearsal 11; fp/ff attacks alternate with quieter textures. Rehearsal 12 is later, at bar 196. | Corrected rehearsal label and removed the false uniformly extreme-storm description in both languages. |
| I, rehearsal 16 / bar 254, printed p.32 | “Sehr langsam beginnend”; reduced low strings p/pp, then quiet English horn and ppp violins. | Replaced the invented extreme E-flat-minor tutti storm with the quiet slow-development recollection. Retained the quiet location. |
| I, bar 291, printed p.36 | Rehearsal 18; “a tempo subito. Molto più mosso”; fff strings and brass. | Corrected rehearsal and tempo description; retained a genuine climax claim even though its measured peak 0.6868906 fails the 0.82 gate. |
| V, rehearsal 10, printed p.148 | General pause, then pp/p low winds, trombones and tuba; quiet strings enter later. | Corrected the inherited loud chorale description, retained the score marker and separately calibrated the listening onset. |
| V, rehearsal 31, printed p.186 | “Langsam. Misterioso”; extremely soft vocal entry. | Kept the quiet chorus entry; did not move it to a louder phrase to pass the floor. |

The old first-movement extreme-dynamic claims at bars 180 and 254 and the Finale bar-142 parent affected six automatically labeled subwindows. Correcting them changed the tested set; these are not six improved acoustic matches. Gate 4 also now checks visible focus/background/role text, which previously omitted the organ-and-bells apotheosis. Its five coda cards are included in the final **19-window** check.

Two pitch checks expose why source-based replacement mattered: the opening low-string figure includes C3–B2–C3–D3–E-flat3, whereas the old stub substituted a generic ascending scale; Urlicht’s opening vocal notes are D-flat4–D-flat4–E-flat4–F4, rather than the old D-flat/E-flat/F-sharp outline. The score also shows soft string accompaniment under the Urlicht entrance, contradicting the inherited claim that it was unaccompanied.

Other inherited annotations still require review, particularly Finale rehearsal 13 and the long Mit-Flügeln/Sterben build: rehearsal labels, changing dynamics and uniform subdivision descriptions cannot be certified from the present spot checks. Keeping their measured failures is preferable to selectively reclassifying every failing window.

## Remaining below-floor starts

An RMS threshold detects level, not the distinction between expressive pianissimo and a musical rest. For example, source SATB notes begin immediately at the chorus coordinate, but the measured onset is −46.3645 dB relative to the movement peak. Moving it several seconds to a louder syllable would damage correspondence. After the supported general-pause correction, the following **11** violations remain:

| Stage | Display bar | Start (s) | Relative dB | Absolute dBFS |
|---|---:|---:|---:|---:|
| m1-s25 | 118 | 396.94 | -45.3199 | -53.5967 |
| m1-s41 | 254 | 762.65 | -43.9693 | -52.2462 |
| m1-s53 | 392 | 1225.50 | -37.9476 | -46.2243 |
| m5-s9 | 43 | 108.44 | -53.9542 | -61.1084 |
| m5-s10 | 48 | 131.68 | -37.7342 | -44.8884 |
| m5-s53 | 472 | 1228.35 | -46.3645 | -53.5187 |
| m5-s54 | 482 | 1288.42 | -44.9889 | -52.1431 |
| m5-s57 | 512 | 1426.77 | -42.6237 | -49.7779 |
| m5-s58 | 524 | 1480.13 | -50.2652 | -57.4193 |
| m5-s61 | 560 | 1617.50 | -52.5495 | -59.7035 |
| m5-s66 | 630 | 1774.05 | -51.4490 | -58.6032 |

Other candidate above-floor samples require shifts of approximately 0.69–8.42 s, without evidence that they represent the same phrase boundary. Source note onsets also exist at the quiet first-movement bars 118 and 392. These levels must not simply be called dead silence.

## Remaining dynamic-window diagnostics

| Stage | Bar | Window (s) | Measured normalized peak | Peak time (s) | Result |
|---|---:|---:|---:|---:|---|
| m1-s44 | 291 | 881.38–907.48 | 0.6868906 | 884.56 | FAIL |
| m3-s23 | 441 | 513.50–554.86 | 1.0000000 | 535.44 | PASS |
| m5-s1 | 1 | 0.48–6.84 | 0.5939044 | 3.60 | FAIL |
| m5-s2 | 7 | 6.84–12.89 | 0.8165078 | 12.80 | FAIL |
| m5-s3 | 13 | 12.89–19.57 | 0.5722081 | 12.96 | FAIL |
| m5-s4 | 20 | 19.57–25.30 | 0.2335998 | 20.72 | FAIL |
| m5-s25 | 176 | 543.50–593.00 | 0.5587948 | 551.60 | FAIL |
| m5-s26 | 187 | 593.00–632.63 | 0.8021477 | 623.92 | FAIL |
| m5-s27 | 198 | 632.63–654.98 | 0.8464304 | 632.64 | PASS |
| m5-s28 | 209 | 654.98–673.97 | 0.3669474 | 673.28 | FAIL |
| m5-s69 | 672 | 1859.37–1881.92 | 0.1367403 | 1872.96 | FAIL |
| m5-s70 | 682 | 1881.92–1904.48 | 0.5551953 | 1897.92 | FAIL |
| m5-s71 | 692 | 1904.48–1925.61 | 0.7045715 | 1911.60 | FAIL |
| m5-s72 | 702 | 1925.61–1945.79 | 0.8251564 | 1944.80 | PASS |
| m5-s73 | 712 | 1945.79–1982.86 | 1.0000000 | 1979.60 | PASS |
| m5-s74 | 723 | 1982.86–2017.73 | 0.8185831 | 1986.64 | FAIL |
| m5-s75 | 733 | 2017.73–2049.87 | 0.9959421 | 2023.84 | PASS |
| m5-s76 | 744 | 2049.87–2070.53 | 0.6291983 | 2068.16 | FAIL |
| m5-s77 | 754 | 2070.53–2103.00 | 0.8482170 | 2089.68 | PASS |

## Polyphonic scenes and voice leading

The 16 scenes contain **80 independently addressable stems and 4,470 notes**, with 4–6 stems and 3–5 family keys per scene. MIDI-derived source quarter positions, velocities, program identities, URLs and SHA-256 hashes are embedded in the authoring script. Compilation is offline and needs no source download. Each note retains source rhythm, register, rest and simultaneity; no counterpoint was invented by looping the original stubs. Selected stems are reductions of the source digitization, not a replacement for every orchestral staff.

Hz is computed as `440 × 2^((midi−69)/12)`. Beat offsets are quarter-note units; seconds equal beats ×60/tempo_bpm. Both seconds (`t`, `d`, `f`) and player beat/MIDI fields (`start`, `dur`, `midi`) are supplied consistently. Integer source pitches give A4=440 concert tuning; unpitched General MIDI percussion keys are explicitly approximations, not measured acoustic frequencies.

| Movement / scene | Source quarters | Teaching tempo (BPM) | Duration (s) | Stems / families | Notes |
|---|---:|---:|---:|---:|---:|
| 1.1 — Funeral theme: bass tread and wind lament | 100–132 | 84 | 22.857143 | 5 / 3 | 169 |
| 1.2 — E major second subject: strings, flute and horn | 192–224 | 76 | 25.263158 | 5 / 3 | 158 |
| 1.3 — Development: winds and horn over cello motion | 832–864 | 96 | 20.000000 | 5 / 3 | 373 |
| 2.1 — Ländler: violin and cello dialogue | 33–60 | 68 | 23.823529 | 5 / 3 | 176 |
| 2.2 — Triplet episode: interlocking strings and horn | 60–97.5 | 68 | 33.088235 | 5 / 3 | 721 |
| 2.3 — Late dance: flute, clarinet and strings | 354–393 | 70 | 33.428571 | 5 / 3 | 562 |
| 3.1 — Circling fishes: clarinet and string motion | 48–87 | 108 | 21.666667 | 5 / 3 | 235 |
| 3.2 — D major middle section: trumpet, horn and strings | 319.5–354 | 100 | 20.700000 | 5 / 4 | 475 |
| 3.3 — Crisis passage: brass, winds and strings | 687–723 | 104 | 20.769231 | 5 / 4 | 378 |
| 4.1 — Urlicht: alto and brass chorale | 4–60 | 54 | 62.222222 | 5 / 4 | 70 |
| 4.2 — Urlicht middle passage: alto, oboe and strings | 103–140 | 58 | 38.275862 | 4 / 3 | 63 |
| 4.3 — Eternal light: solo voice and chamber coda | 240–268 | 56 | 30.000000 | 5 / 3 | 91 |
| 5.1 — Finale premonition: winds, brass and low strings | 459–503 | 96 | 27.500000 | 5 / 5 | 296 |
| 5.2 — Great Summons: flute and distant brass | 1715–1759 | 60 | 44.000000 | 4 / 3 | 136 |
| 5.3 — Resurrection: SATB chorus and instrumental response | 1829.5–1910.5 | 66 | 73.636364 | 6 / 3 | 276 |
| 5.4 — Resurrection hymn: chorus, brass and organ | 2830.5–2886.5 | 70 | 48.000000 | 6 / 5 | 291 |

Movement I separates violin, cello, reed and horn lines so the bass tread can be heard against the wind lament; the E-major example preserves independent horn entries beneath the violin phrase. The development example keeps moving cello notes distinct from sustained/reiterated wind material.

Movement II separates violin and cello dialogue instead of labeling one monophonic stub as both instruments. The triplet scene preserves the staggered motion of both violin groups and cellos against clarinet and horn; the late dance uses independent flute and clarinet filigree. Movement III retains continuous string motion, reed accents and the D-major trumpet/horn conversation. The crisis scene contains separate high-wind and brass motion rather than a single held synthetic dissonance.

Urlicht retains an independent alto line, brass chorale and string support, followed by distinct oboe/violin/cello and clarinet/harp responses. The Finale includes distant-brass/flute dialogue, four separate SATB lines with an instrumental response, and a hymn reduction with chorus, brass, strings, organ and a separate bell stem. Auxiliary glockenspiel/bell events in the digitization were separated from its soprano instrument switches, rather than rendered as vocal notes.

Excerpts range from **20.000000 to 73.636364 s** on their declared phrase rulers; shorter final note releases leave natural phrase-end rests. Boundary-clipped source notes remain marked. Fixed teaching tempi preserve source-relative rhythms but do not reproduce every performed fermata, rubato, articulation or timbral nuance. Exhaustive critical-edition pitch/rhythm confirmation is outstanding.

## MIDI serialization and external playback checks

Each download is a **Format-1, 480 PPQN anthology of every scene for its movement**. A conductor track contains a matching tempo event, time signature and named scene marker at each scene boundary. Source stems have named tracks, GM program changes, velocity, pan and volume; channel 10 is reserved for explicitly unpitched percussion. Absolute events are sorted before delta encoding; note-offs precede same-tick rearticulation, rests and chords are preserved, and a general VLQ encoder handles long deltas. Two quarter-note beats separate scenes. End events reset sustain and release remaining voices.

Independent `mido` parsing compared **all 4,470 note-on/off pairs** against the generated scene schedule: **0 tick timing error, 0 pitch/velocity mismatches, 0 orphan note-offs, 0 hanging notes and 0 cent conversion error**. **777 chord onsets** survived serialization. All 16 tempo, meter and scene-marker events matched their scenes.

| Movement | File bytes before → after | MIDI tracks | Notes | Playback duration (s) |
|---|---:|---:|---:|---:|
| 1 | 244 → 7460 | 16 | 700 | 71.127840 |
| 2 | 182 → 13395 | 16 | 1459 | 93.869757 |
| 3 | 213 → 10541 | 16 | 1088 | 65.447024 |
| 4 | 180 → 3412 | 15 | 224 | 134.789287 |
| 5 | 257 → 10658 | 22 | 999 | 198.204561 |

## Player compatibility and regression verification

The compiler restores metadata, movement duration/barCount/audio fields, motifs, stage start/foreground/background/cues, and synth bpm/totalBeats/track-note fields expected by the unchanged `app.js` and `engine.js`. Source-note overlap supplies estimated bar activity to the existing radar; its coordinates remain explicitly provisional. Four checked passages expose usable full-score page links. The Finale replay control points to the start of its coda.

Validation completed:

- Python compilation and actual Node.js syntax parsing passed; zero listed foreign-work contamination strings.
- Fifteen structural/negative-injection regressions passed, including wrong duration, missing translation, detuning, bad anchors, invalid JS, contamination, silent onset, quiet climax and proof that changing dynamic annotations cannot boost measured RMS.
- Four additional checks passed: exact-frame boundaries at 4.56 and 275.84 s, the source-supported general-pause onset, and rejection of that override when the audio checksum differs. Together with the fifteen regressions, this is **19 checks**.
- LinkeDOM executed the unchanged player through all five movements, sixteen scene tabs, eighty voice mute/unmute controls, bilingual toggles and 4,470 mocked WebAudio note schedules without an error.
- Actual local streaming returned HTTP 206 and the correct 16-byte MIDI prefix for a range request.
- The computer-use browser host was unavailable, so no visual browser or audible DAW performance certification is claimed. DOM/media checks use mocks; MIDI semantics use independent parsing.
- `git diff --check` passed. Repeating compilation reproduced all six generated artifacts byte-for-byte, with zero writes to tracked files outside the allowed targets. Final data.js SHA-256: `78a82f35c4797b2269b2397b9d7de365ca7ac4a323005f8ab5a8b4331d1e95b5`.

Backend: local bounded audio/data readouts, one movement at a time; no simulation, solver campaign, GPU or cluster submission. This follows the workspace instruction allowing short local data-only analysis. Toolchain: Python 3.15.2, FFmpeg 8.1, Node.js 24.22.1; temporary independent MIDI parser mido 1.3.3. A timed compiler run took **8.832949 s** wall time and returned the expected failure for the genuine acoustic residuals.

## Git scope and remaining work

Pre-existing RMS JSON edits and untracked `.codex_worker/`, `TASK_CONTRACT.md`, `public/`, and `src/` artifacts were preserved in local stash **52bad3e03c3a14a933528c0a50f2826922a01a42** before committing the allowed deliverables. They are not included in this task’s commits. No new governance files were created. No repository-root AGENTS.md was present; `/Users/jack/Documents/Template_Writing/AGENTS.md` was read and followed.

The code/report commit is pushed to `origin/main` before HANDOFF.json is written. The handoff is then committed and pushed separately, followed by clean-status and HEAD/origin-main equality verification.

To claim PASS, the remaining work requires an authenticated audio/trim reference for Movement I, an agreed score bar ruler for Urlicht and Finale free time, direct Kaplan/IGMG verification, manual review of the 27 ambiguous alignment points, and a resolution of the fixed acoustic criteria against actual soft vocal entries and changing dynamics. The present implementation deliberately preserves these failures and the evidence needed to review them.
