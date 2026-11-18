# 01 — Brand and Principles

## Brand platform

**Name:** FALCON  
**Concept:** Obsidian Command — a calm, precise, night-ready command console.  
**Personality:** Precise, calm, authoritative, premium, tactical, trustworthy and quiet-until-it-matters.  
**Tagline:** “Every camera, intelligent.”  
**Hindi tagline:** “हर कैमरा, बुद्धिमान।” (reviewed translation required before production)

The interface is an operational tool, not a marketing surface. It should be calm in normal operation and unmistakable when urgent. Video and evidence remain visually primary; decorative motifs never cover data.

## Wordmark and mark

Use the custom angular wing/falcon mark from `apps/dashboard/public/brand/falcon-mark.svg`. Two chevrons form a forward-facing wing with negative-space head/eye. The mark is single-color by default; the two-color option uses Radar Cyan for the upper wing and Seal Gold only on the small integrity variant. Do not depict a realistic bird, weapon, flag or national insignia.

- Horizontal lockup: mark, then FALCON wordmark; wordmark uses Sora 700 and `0.18em` tracking.
- Stacked lockup: mark centered above the wordmark; tagline is optional below at 12 px minimum.
- Clear space: at least the mark's eye diameter on all sides.
- Minimum mark size: 16 px for favicon/UI only if the eye and chevrons remain distinct; otherwise use a simple chevron silhouette. Print minimum 8 mm.
- Minimum wordmark width: 96 px digital.
- Dark background: light wordmark/mark; light background: Obsidian ink; monochrome: one solid color.
- Never stretch, rotate, outline, add a glow, recolor with severity, apply gradients to the wordmark, or use Seal Gold outside integrity-ledger contexts.

## Terrain and radar motifs

Terrain contours are abstract topographic linework at 3–4% opacity on login, empty states and overview backgrounds only. Radar sweep is reserved for a quiet loading/empty illustration; no sweep runs behind live video or alert text. Decorative marks are hidden from assistive technology (`aria-hidden="true"`).

## Control-room principles

1. **Three-second glance:** current site, live connection, critical alert count and clock are identifiable within three seconds.
2. **One primary action:** each route has one visually dominant task; destructive or privileged actions are not visually primary.
3. **Progressive disclosure:** show event summary first, details and metadata on demand.
4. **Calm default:** no continuous motion, blinking badge or sound in normal state.
5. **Error prevention:** preserve selected records; require confirmation when impact is significant; explain irreversible actions.
6. **Keyboard-first:** primary actions remain reachable without a pointer and keep visible focus.
7. **Distance legibility:** Wall density uses 16 px minimum for operational text and prioritizes status over metadata.
8. **Alarm-fatigue control:** critical has a stable icon/label and a restrained pulse; other severities do not animate.
9. **Human decision:** FRS and ANPR results are candidates; no automated enforcement or identity assertion.
10. **Offline honesty:** distinguish site-local service health from HQ connectivity and show the timestamp of stale data.

## Voice and tone

Use calm, factual, short, active-voice text. Say what happened and what the user can do next. Avoid exclamation marks, blame, vague “something went wrong” messages and unconfirmed success language.

| Context | English | Hindi example |
|---|---|---|
| Normal | “All cameras are connected.” | “सभी कैमरे जुड़े हुए हैं।” |
| Alert | “Intrusion detected · Camera 07 · North fence.” | “घुसपैठ का पता चला · कैमरा 07 · उत्तरी सीमा।” |
| Failure | “The stream is unavailable. Check camera health or retry.” | “स्ट्रीम उपलब्ध नहीं है। कैमरे की स्थिति जाँचें या फिर प्रयास करें।” |
| FRS limitation | “Candidate match. Human review is required.” | “संभावित मिलान। मानवीय समीक्षा आवश्यक है।” |

Hindi examples are draft copy and require native-language review. Never translate machine enums, IDs, hashes, plate strings or model output.
