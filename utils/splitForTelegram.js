/**
 * Divide un texto en chunks para respetar el límite de caracteres de Telegram (4096)
 * Limpia caracteres problemáticos y corta por caracteres (no por líneas)
 * @param {string} texto - Texto a dividir
 * @param {number} maxChars - Máximo de caracteres por mensaje (default: 4096)
 * @returns {array} Array de strings, cada uno <= maxChars y limpio
 */
function splitForTelegram(texto, maxChars = 4096) {
  // Limpia caracteres problemáticos
  texto = texto
    .replace(/"/g, '"')  // Comillas dobles curvas → rectas
    .replace(/'/g, "'")  // Comillas simples curvas → rectas
    .replace(/[""'']/g, '') // Quita comillas especiales
    .trim();

  if (texto.length <= maxChars) {
    return [texto];
  }

  const chunks = [];
  let inicio = 0;

  // Corta por caracteres (no depende de saltos de línea)
  while (inicio < texto.length) {
    // Intenta cortar en maxChars
    let chunk = texto.substring(inicio, inicio + maxChars);

    // Si no es el último chunk, retrocede al último espacio
    if (inicio + maxChars < texto.length) {
      const ultimoEspacio = chunk.lastIndexOf(' ');
      if (ultimoEspacio > maxChars / 2) { // Solo si es un espacio "razonable"
        chunk = chunk.substring(0, ultimoEspacio);
      }
    }

    chunks.push(chunk.trim());
    inicio += chunk.length + 1;
  }

  return chunks;
}

module.exports = { splitForTelegram };

/**
 * USAGE EN N8N:
 *
 * 1. Function Node (después de Claude API):
 * ────────────────────────────────────────
 * const { splitForTelegram } = require('./utils/splitForTelegram.js');
 * const respuestaClaudeCompleta = items[0].json.response.content[0].text;
 * const mensajes = splitForTelegram(respuestaClaudeCompleta, 4096);
 * return [{ json: { mensajes: mensajes } }];
 *
 * 2. Loop Node:
 * ────────────────────────────────────────
 * Loop over: {{ $node['Function'].json.mensajes }}
 *
 * 3. Dentro del Loop - Telegram Send Message:
 * ────────────────────────────────────────
 * Message: {{ $item().json }}
 */
