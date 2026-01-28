/**
 * Parsea comandos de nota del formato /not{categoria} nota
 * @param {string} texto - Texto con comando (ej: "/notgym esto es una nota")
 * @returns {object} Objeto con parsed data o error
 */
function parseNota(texto) {
  // Mapeo de abreviaturas a carpetas
  const categorias = {
    'gym': 'gym',
    'med': 'meditacion',
    'nut': 'nutricion',
    'opt': 'options',
    'tra': 'trading',
    'inv': 'inversiones'
  };

  // Regex: /not{categoria} resto del texto
  const regex = /^\/not(\w+)\s+(.*)/i;
  const match = texto.match(regex);

  if (!match) {
    return {
      error: true,
      mensaje: "Formato inválido. Usa: /not{categoria} tu nota"
    };
  }

  const abreviatura = match[1].toLowerCase();
  const nota = match[2];
  const categoria = categorias[abreviatura];

  if (!categoria) {
    return {
      error: true,
      mensaje: `Categoría '${abreviatura}' no encontrada. Usa: gym, med, nut, opt, tra, inv`
    };
  }

  return {
    error: false,
    comando: '/not',
    abreviatura: abreviatura,
    categoria: categoria,
    nota: nota,
    carpetaGit: `data/${categoria}/notas.json`
  };
}

module.exports = { parseNota };

/**
 * EJEMPLOS DE USO EN N8N:
 *
 * En un Function Node:
 * ────────────────────────────────────────
 * const { parseNota } = require('./utils/parseNota.js');
 * const entrada = $input.first().json.mensaje;
 * const resultado = parseNota(entrada);
 * return [{ json: resultado }];
 *
 * O directamente en el Function Node (sin require):
 * ────────────────────────────────────────
 * function parseNota(texto) {
 *   const categorias = {
 *     'gym': 'gym',
 *     'med': 'meditacion',
 *     'nut': 'nutricion',
 *     'opt': 'options',
 *     'tra': 'trading',
 *     'inv': 'inversiones'
 *   };
 *   const regex = /^\/not(\w+)\s+(.*)/i;
 *   const match = texto.match(regex);
 *   if (!match) {
 *     return { error: true, mensaje: "Formato inválido" };
 *   }
 *   const abreviatura = match[1].toLowerCase();
 *   const nota = match[2];
 *   const categoria = categorias[abreviatura];
 *   if (!categoria) {
 *     return { error: true, mensaje: `Categoría '${abreviatura}' no encontrada` };
 *   }
 *   return {
 *     error: false,
 *     comando: '/not',
 *     abreviatura: abreviatura,
 *     categoria: categoria,
 *     nota: nota,
 *     carpetaGit: `data/${categoria}/notas.json`
 *   };
 * }
 *
 * MAPEO DE CATEGORÍAS:
 * - gym → gym
 * - med → meditacion
 * - nut → nutricion
 * - opt → options
 * - tra → trading
 * - inv → inversiones
 */
