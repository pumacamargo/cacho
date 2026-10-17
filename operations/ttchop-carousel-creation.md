---
title: Creación de carruseles editoriales de TTChop
created: 2026-10-17
updated: 2026-10-17
type: runbook
tags: [sistema, runbook, api]
status: active
confidence: high
related: [ttchop-webapps, ttchop-automatizaciones]
---

# Creación de carruseles editoriales de TTChop

Runbook para historias de Reddit adaptadas a carrusel y otros carruseles
editoriales. Distingue el carrusel gestionado por TTChop2 (Firestore/app) del
flujo local de PNGs con fondos Kie.ai. Relacionado con [[ttchop-webapps]] y
[[ttchop-automatizaciones]].

## Elegir el flujo antes de generar

### A. Carrusel guardado en TTChop2

Usa la pestaña **Carousels** de TTChop2 cuando Arturo quiere que el carrusel
quede en su biblioteca, con estado, callbacks, fondos y PNGs finales en Firebase.
Requiere una sesión autenticada, `projectId: ttchop2`, las plantillas guardadas
adecuadas y verificación del estado final `ready`. Sigue el procedimiento y el
security gate de `ttchop-server-ops`: no invoques `/carousel/create`,
`/regenerate`, `/delete` ni `/recompose` con identidad indicada por el cliente
mientras la autorización del endpoint no haya sido verificada. No suplantes al
usuario con Firebase Admin.

### B. Borrador local de PNGs (flujo Kie.ai + composición local)

Usa este flujo cuando Arturo pide recibir las imágenes PNG en el chat y no pide
que el proyecto se escriba en Firestore. **No requiere iniciar sesión en
TTChop2**: genera fondos directamente en Kie.ai y compone el texto localmente.
No crea un documento de carrusel, no sube a Firebase/Storage y no publica en
TikTok. Esta fue la ruta usada para el carrusel de historia del 2026-10-17 y es
el precedente local documentado el 2026-10-16.

La llamada directa al proveedor usa créditos: genera únicamente tras una
instrucción explícita de Arturo para crear el carrusel/las imágenes. Antes de
regenerar slides, pedir autorización si implica gasto adicional no incluido en
lo ya aprobado.

## Procedimiento local Kie.ai + composición

1. **Historia y fuente**
   - Para una historia inspirada en Reddit, primero localiza y lee un post público;
     guarda permalink, subreddit y fecha solo como procedencia interna en Cacho.
   - Resume las afirmaciones sin tratarlas como hechos verificados; adapta la
     historia con prosa original, sin copiar texto ni exponer handles.
   - Mantén el arte narrativo: no pongas “Reddit”, subreddit, usuario/handle ni
     disclaimers de ficción dentro de las láminas, salvo que Arturo lo pida.
   - Usa exactamente el texto aprobado y el idioma solicitado.

2. **Brief visual**
   - Escoge una dirección visual apropiada y nómbrala ante Arturo. Para el
     precedente del 2026-10-17 se eligió **Candid Professional Women**: fotografía
     editorial candid y realista, protagonista adulta japonesa consistente,
     iluminación natural, paleta cinematográfica sobria y espacio negativo a la
     izquierda para el texto.
   - La descripción resumida de un `carousel_style` en esta wiki no equivale al
     `visualBible` completo guardado en Firestore. Si se necesita el prompt exacto
     de la plantilla del usuario, léelo desde una sesión autenticada; en un
     borrador local no afirmes haber cargado la plantilla cuando solo estás
     usando su dirección visual como brief.
   - Escribe `imagePrompt` en inglés. Repite rasgos visibles del mismo personaje
     adulto en cada escena. Incluye negativos: sin texto, letras, carteles, logos,
     marcas de agua, interfaz ni menores. Deja caras y acción fuera de la zona de
     overlay.

3. **Acceso seguro y solicitud de imágenes**
   - Kie.ai está configurado en `vps-projects`; el nombre de la variable es
     `KIEAI_API_KEY` dentro de `ttchop-server/.env`. Lee el secreto solo dentro
     del proceso local del VPS; jamás lo imprimas, copies al chat/wiki ni lo
     registres en argumentos o logs.
   - Endpoint documentado: `POST https://api.kie.ai/api/v1/jobs/createTask`;
     modelo usado en el precedente local: `bytedance/seedream-v4-text-to-image`
     (`imageModel: seedream-v4`), tamaño `portrait_16_9`, seed entre 0 y 999999.
   - Seedream permite hasta 6 imágenes por tarea. Para un carrusel de 7 fondos,
     prepara una tarea de 6 y otra de 1. El prompt del lote debe decir
     explícitamente `Generate exactly 6 separate images` y enumerar `Image 1` …
     `Image 6` con la escena de cada slide; usa la misma biblia visual en ambas
     tareas. En la tarea individual no envíes `max_images`.
   - Antes de esperar callbacks/polling, persiste en un manifiesto local el
     `taskId`, slots asociados, modelo, seed, prompts, hora de envío y créditos
     estimados. Tras completarse, registra `creditsConsumed` real de cada tarea.
     Si el comando SSH/CLI vence mientras Kie sigue trabajando, **no vuelvas a
     enviar las tareas**: recupera los `taskId` del manifiesto y consulta
     `GET /api/v1/jobs/recordInfo?taskId=…`.
   - Revisa `code` aunque HTTP sea 200; confirma `data.state == success`, extrae
     `data.resultJson.resultUrls` y exige que el total coincida con el número de
     slots. Descarga las URLs temporales inmediatamente. No escribas a Firestore
     ni uses el endpoint de creación de carruseles para evitar la sesión.

4. **Composición local**
   - Usa fondos sin texto. Compón el overlay en una capa aparte; precedente:
     PNG vertical 1080×1920, Noto Sans CJK, texto blanco con sombra suave,
     gradiente oscuro lateral, contador y barra de progreso.
   - Para japonés, ajusta los saltos por frases y puntuación (kinsoku); no envuelvas
     de forma ciega por cantidad de caracteres. Mantén el bloque legible y sin
     tapar ojos, caras, manos o el objeto narrativo importante. Portada sin
     título independiente: empieza directamente con el gancho narrativo.

5. **QA y entrega**
   - Confirma siete slides si ese es el guion aprobado; revisa una hoja de
     contacto y abre portada, slide más denso y cierre a resolución completa.
   - Verifica dimensiones 1080×1920, texto no cortado, contraste, caracteres
     japoneses, continuidad de edad/rostro/ropa, causalidad de escenas y ausencia
     de letras/logos accidentales en el fondo. Regenera solo los slots defectuosos
     y con autorización para el gasto adicional.
   - Envía los PNG individuales en orden; el ZIP es opcional, no sustituye los
     PNGs. Indica si es borrador local o si quedó guardado en TTChop2. No publiques
     sin autorización explícita.

## Costos y límites registrados

- La referencia de precios del proyecto estima Seedream v4 en **5 créditos por
  imagen**, batch máximo 6. Siete imágenes equivalen a **35 créditos estimados**;
  confirma `creditsConsumed` de Kie.ai para el gasto real.
- En el borrador del 2026-10-17 se recibieron siete fondos con una leve variación
  de tono de cabello entre escenas. El proceso completó aunque el comando SSH
  inicial excedió el tiempo de espera del cliente; los `taskId` y el gasto real
  no quedaron recuperables porque no se guardó un manifiesto. Evitarlo con el
  paso 3: persistir IDs antes de polling y registrar el resultado por escrito.
- No hay dato fiable del modelo exacto del carrusel del 2026-10-16; no atribuirle
  retrospectivamente `seedream-v4`. Para el del 2026-10-17, el modelo usado fue
  `bytedance/seedream-v4-text-to-image`; el coste documentado sigue siendo una
  estimación porque el valor real de `creditsConsumed` no se capturó.

## Procedencia editorial: ejemplo 2026-10-17

La historia japonesa sobre la amiga que abusó de la hospitalidad durante la
recuperación se inspiró en un relato anónimo de **r/EntitledPeople**, recopilado
en **r/BestofRedditorUpdates**. El post original figura fechado **2026-01-16** y
la actualización, **2026-01-17**. Se registra solo como premisa editorial, no
como relato verificado. El permalink de recopilación es:
https://www.reddit.com/r/BestofRedditorUpdates/comments/1qldw9m/my_friend_took_advantage_of_me_when_i_was_in_the/

Las imágenes del ejemplo usaron la dirección visual Candid Professional Women,
texto japonés superpuesto localmente, sin rótulos de Reddit. Se entregaron siete
PNGs individuales 1080×1920 y un ZIP opcional; no se guardaron en TTChop2 ni se
publicaron.