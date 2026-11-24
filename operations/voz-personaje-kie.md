---
title: Voz de personaje con Gemini TTS en kie.ai (voz Charon)
created: 2026-11-24
updated: 2026-11-24
type: runbook
tags: [runbook, voz, tts, kie, gemini]
status: active
confidence: high
related: [traduccion-video-pumasvoice-sincronizada, ttchop-video-generation]
---

# Voz de personaje con Gemini TTS en kie.ai — voz **Charon**

Receta para generar el diálogo del personaje (locutor carismático, amigable, con energía de comercial) usando **Gemini 3.8 Flash TTS** a través de kie.ai. **Voz elegida por Arturo: `Charon`** (2026-11-24), tras comparar Fenrir, Autonoe, Sadachbia y Charon con la misma frase.

## Por qué kie.ai y no otra cosa

- **kie** es el más barato y ya está pagado en el proyecto: ~**0.03 créditos por segundo** de audio (una frase de 9 s ≈ 0.30 créditos).
- **No puede diseñar timbre**: kie solo acepta `voice_name` de una lista **fija de 71 voces** (o un clon temporal `replica` desde audio). El timbre lo pone la voz elegida; el campo `style` solo dirige la actuación. Si algún día se necesita un timbre que no existe en esas 71, hay que ir a ElevenLabs (Voice Design + guardar voz) o a Google.
- **IDs tipo `voice_pl1zhbthxsj7` no sirven en kie**: son de la librería de Google y no están en el enum. Verificado en el esquema.

## La receta exacta que funciona

`POST https://api.kie.ai/api/v1/jobs/createTask` con `Authorization: Bearer $KIEAI_API_KEY` (la clave está en `ttchop-server/.env` del host `100.68.238.117`).

```json
{
  "model": "google/gemini-3-8-flash-tts",
  "input": {
    "temperature": 1,
    "speakers": [{ "speaker_id": "Speaker 1", "voice_name": "Charon" }],
    "dialogue_turns": [{
      "speaker_id": "Speaker 1",
      "style": "Charismatic TV commercial host with a rich, warm, bright and energetic voice. Fast-paced and expressive with punchy articulation, rhythmic delivery, dramatic micro-pauses and playful pitch variation. Sounds like someone smiling while talking, genuinely amazed and eager to share. Shifts between friendly conversation, playful excitement and bursts of enthusiasm. Theatrical but authentic, witty, never monotone, never shouty, never formal.",
      "text": "見てこれ！<gasp> ピアスの穴がなくても大丈夫！ <laugh> 挟むだけなのに、全然落ちないんだよ。これ本気でヤバくない！？"
    }]
  }
}
```

**Ese `style` es el aprobado** (el que se usó en las cuatro voces del test final). No cambiarlo sin motivo: es lo que le da el carácter.

Sondear el resultado: `GET /api/v1/jobs/recordInfo?taskId=<id>` → `data.state` (`success`/`fail`), `data.resultJson` con `resultUrls[]` (**temporales: descargar de inmediato**) y `data.creditsConsumed` (costo real por tarea). Saldo: `GET /api/v1/chat/credit`.

## Las voces que YA usan los videos de TTChop (definidas)

Están en el **`README.md` de ttchop-server**, sección *“Voice IDs de ElevenLabs”*:

| Mercado | Voz | ID | Notas |
|---|---|---|---|
| 🇯🇵 JP | **Announcer** (masculino) | `gU0LNdkMOQCOrPrwtbee` | **La default de los videos japoneses** |
| 🇲🇽 MX | **Jessica** (femenino) | `cgSgspJ2msm6clMCkdW9` | La default de los videos mexicanos |
| — | **PumaVoice01** (clonada) | `ve7BOdejheJbgrBriBx4` | Traducciones y videos con la voz de Arturo |

- El `scheduler` **no tiene la voz en el código**: la lee de una **plantilla de voz en Firestore** (`voiceId`) y falla con *“No voiceId found (check voice template)”* si no existe. Por eso siempre se oye la misma voz: la plantilla la fija.
- **Ajustes fijos del pipeline** (`pipeline/elevenlabs.js`): `eleven_v3`, `stability: 0`, `style: 0`, `similarity_boost: 0`, `speed: 0.5` (por debajo del mínimo documentado de 0.7 — ya anotado como duda en el archivo).
- **Convención de velocidad**: el ritmo no se pide a ElevenLabs, se ajusta **después con FFmpeg** `atempo` a **1.4×–1.5×**, más pausas de **0.3–0.34 s** entre líneas (patrón usado en los videos aprobados).

Conclusión práctica: **para que un video nuevo suene como los demás, hay que usar la misma voz y el mismo tratamiento (velocidad + pausas)**, no solo el mismo texto.

## Orden de preferencia (definido por Arturo, 2026-11-24)

1. **OPCIÓN 1 — `Charon`** (Gemini 3.8 Flash TTS vía **kie.ai**). Es la voz elegida para el personaje: cálida, masculina, con presencia de comercial. Receta exacta en la sección de arriba.
2. **PLAN B — `Announcer`** (ElevenLabs, mercado JP) — `gU0LNdkMOQCOrPrwtbee`. La que usan hoy los videos japoneses.
3. **PLAN B — `Jessica`** (ElevenLabs, mercado MX) — `cgSgspJ2msm6clMCkdW9`.
4. **PLAN B — `PumaVoice01`** (ElevenLabs, clonada) — `ve7BOdejheJbgrBriBx4`. Para traducciones con la voz de Arturo.

**Aviso técnico:** Charon vive en **kie**, y el pipeline actual de TTChop solo sabe hablar con **ElevenLabs** (`pipeline/elevenlabs.js`). Poner Charon como default automático **no es cambiar un ID**: requiere añadir una rama de TTS por kie en `ttchop-server` (submit a `createTask`, sondeo de `recordInfo`, descarga del MP3 temporal, y el mismo tratamiento de velocidad/pausas con FFmpeg). Mientras eso no se haga, Charon se usa **a mano** con la receta de esta página.

## Lineamientos de emoción (lo aprendido en las pruebas)

1. **El `style` no cambia la garganta, solo la actuación.** Si una voz suena femenina o plana, no se arregla con más adjetivos: se cambia la voz base.
2. **No pedir “high-pitched / squeaky” a una voz masculina.** Empuja al falsete — pasó con Puck, Fenrir y Achird, que salieron afeminadas. Para masculino: `rich, warm, masculine voice`, y añadir `never falsetto`.
3. **Sumar, no reemplazar.** “Amigable” no es lo opuesto de “exagerado”: `Exaggerated cartoon voice … but warm and friendly` funciona; quitar la exageración para meter la amistad deja una voz de locutora plana (error cometido y corregido).
4. **Las etiquetas van dentro de `text`**, entre ángulos: `<laugh>`, `<gasp>`, `<sigh>`, `<whisper>`, `<snicker>`, `<sob>`, `<yawn>`, `<snort>`, `<tsk>`.
5. **Una etiqueta por frase o cláusula.** Amontonarlas atropella la lectura.
6. **El contraste es lo que suena exagerado**: una línea con `<whisper>` entre dos exclamadas suena el doble de intensa que todo gritado.
7. **La puntuación es dirección de actuación.** `！？` alarga y sube; `…` crea pausa; los cortes de línea dan aire; las frases cortas pegan más que una larga.
8. **Texto de reacción, no de ficha de producto.** Una descripción informativa aplana cualquier voz; una exclamación con reacción la despierta.
9. **`temperature: 1`** es el valor usado; da variación sin descontrol.
10. **Prompts largos se obedecen a medias.** El prompt de diseño de ~1,100 caracteres metido en `style` funcionó peor que la versión corta de actuación (~450 caracteres).

## Costo medido (2026-11-24, Gemini 3.8 Flash TTS)

| Muestra | Duración | Créditos |
|---|---:|---:|
| Lumi (japonés, 6.6 s) | 6.6 s | 0.21 |
| Jessica / ElevenLabs V3 (5.6 s) | 5.6 s | 0.56 |
| Puck (español, 6.2 s) | 6.2 s | 0.20 |
| Lumi / Zephyr / Riko (8.2–8.7 s) | ~8.5 s | 0.26–0.28 |
| Puck / Fenrir / Achird (9.0–9.7 s) | ~9.4 s | 0.29–0.31 |
| Prompt literal EN + actuación JA (9.6–10.1 s) | ~9.9 s | 0.30–0.32 |
| **Fenrir / Autonoe / Sadachbia / Charon** (8.7–9.4 s) | ~9.2 s | **0.28–0.30** |

**Regla práctica: ~0.03 créditos por segundo de audio.** ElevenLabs vía kie sale ~3× más caro que Gemini.

## Voces probadas y veredicto

- **Charon** — elegida. Cálida, masculina, con presencia; aguanta el registro de comercial sin sonar gritona.
- **Fenrir** — “excitable”; más energética, algo más caricaturesca.
- **Autonoe** — **femenina** en el catálogo de Google (ojo si se busca masculino).
- **Sadachbia** — masculina, “lively”.
- **Puck** — masculina, “upbeat”; salió afeminada con el prompt de tono agudo.
- **Lumi** — la preferida en las primeras pruebas (japonesa, cálida).
- **Zephyr**, **Riko**, **Achird** — probadas; Achird particularmente cálida.

## Regla de gasto

**Nunca generar sin un “sí” explícito de Arturo**, ni pruebas de 0.2 créditos. Proponer, decir el costo estimado y esperar.

## Rutas

Scripts de las pruebas en `/root/.hermes/cache/scratch/momoko-voice/` (`kie_tts_demo.py`, `kie_tts_amigable.py`, `kie_tts_masculinas.py`, `kie_tts_prompt_arturo.py`, `kie_tts_cuatro.py`). Los MP3 quedan en `demo/`, `amigable/`, `masculinas/`, `prompt_arturo/`, `cuatro/`. Scratch se limpia: lo esencial está en esta página.