# 📊 Contexto de Trading de Opciones

## Objetivos y Estrategia

| Parámetro | Valor |
|-----------|-------|
| **Objetivo** | Generar ingresos semanales vendiendo puts, y ganancias adicionales con covered calls |
| **Estrategia** | Sell Puts Semanales + Covered Call (si asignan) |
| **Presupuesto** | 3,000 USD |
| **Broker** | Webull |
| **Meta** | $300-500/mes (5-8% mensual) |

---

## 🎡 Estrategia: Sell Puts Semanales + Covered Call

La estrategia tiene **2 fases**:

### FASE 1: VENTA DE PUTS SEMANALES

- Vendes puts OTM (fuera del dinero) cada semana
  - Estructura: **1 put cerrándose cada semana** = flujo consistente
  - Pueden ser 1, 2 o más contratos según el precio del stock y margen disponible
  - Vende nuevo put cada semana para mantener el flujo
- Recibes premium cada semana
- Dejas que expiren naturalmente (sin take profit de 50%)
- Si no te asignan → Ganancias limpias

### FASE 2: VENTA DE CALL CUBIERTO (SOLO si asignan)

- Si fuiste asignado: ahora tienes 100 acciones
- Vendes 1 call cubierto de 4-6 semanas
- Strike: **50% sobre tu precio de entrada**
- **Take Profit de 50%**: Cierras la posición cuando ganes 50% en el call

**Ciclo normal**: 4-8 semanas (si hay asignación)
**Ganancia esperada**: ~1.5% semanal de tu capital en Fase 1 + prima adicional de Fase 2 si asignan

---

## ⚙️ Parámetros de Entrada

### Venta de PUT Semanal (FASE 1)

| Parámetro | Valor |
|-----------|-------|
| **Stock price** | $15-60 USD |
| **DTE** | 7 días a expiración |
| **Delta** | -0.25 a -0.15 (2-3 delta, conservador) |
| **IV Rank** | > 30% (más alto = mejores premios) |
| **Open Interest** | > 500 |
| **Bid-Ask spread** | < $0.15 |
| **Prima mínima** | 1.5% de tu capital por contrato |

### Gestión FASE 1

- **Salida**: Dejas que expire naturalmente en 7 días
- **Sin take profit de 50%** en puts semanales
- Si precio baja peligrosamente → considera cerrar antes

### Venta de CALL Cubierto (FASE 2 - solo si asignan)

| Parámetro | Valor |
|-----------|-------|
| **DTE** | 4-6 semanas |
| **Strike** | 50% sobre precio de entrada |
| **Take Profit** | 50% de ganancia (cierre automático) |
| **Herramienta** | Usar Limit Order para automatizar |

---

## 🔍 Búsqueda de Stocks

### En Webull: Market → Options → Screener

**Filtros principales**:
- Symbols: Whole Market
- Days to Expire: 7 to 7 (solo opciones semanales)
- Volume: 50+ (menos restrictivo para semanales)
- Open Interest: 500 to 525,654
- Delta: -0.25 to -0.15

**Después de resultados, filtra manualmente**:
- Stock price: $15-60
- IV Rank > 30% (cuanto más alto = mejores premios)
- Bid-Ask spread < $0.15
- Prima de put ≥ 1.5% de tu capital por contrato
- **Que entiendas la empresa** (posibilidad de asignación)

**Frecuencia**: Revisa **cada semana** para identificar puttos semanales a vender
- Después de tu put actual, identifica el siguiente para la siguiente semana
- Esto crea el flujo continuo de ingresos

---

## 🏭 Industrias Recomendadas para Puts Semanales

### Criterios de Selección

Al elegir stocks para vender puts semanales, priorizar industrias que combinen:
- ✅ **Volatilidad decent** (IV Rank > 30%) = Premios semanales atractivos
- ✅ **Stocks $15-60** = Compatible con presupuesto de $3,000 y asignación
- ✅ **Potencial a mediano plazo** = Si te asignan, puedes mantener 4-6 semanas con confianza
- ✅ **Liquidez** = Open Interest > 500, Bid-Ask < $0.15
- ✅ **Opciones semanales disponibles** = Trading todos los viernes

---

### 1. 🔋 Energía Limpia y Gas Natural

**⚠️ Consideraciones**:
- Sector cíclico, puede tener drawdowns significativos
- Gas natural es "puente" 2025-2028, no largo plazo extremo

---

### 2. 🧬 Biotecnología Small/Mid Cap

**Áreas de enfoque**:
- Oncología
- GLP-1 (obesidad, diabetes)
- Terapias genéticas (CRISPR)

**⚠️ Consideraciones**:
- **Alto riesgo**: Puede caer 50%+ en días por malas noticias de FDA
- Investigar pipeline antes de vender put
- Preferir empresas con múltiples catalizadores

---

### 3. 💻 Semiconductores y Tech Small Cap

**⚠️ Consideraciones**:
- Cuidado con ciclo de semis (riesgo overcapacity 2027-2028)
- Preferir diversificación geográfica (no 100% China)

---

### 4. 📊 ETFs Sectoriales

**⚠️ Consideraciones**:
- Verificar precio < $30
- Si asignan ETF, tienes exposición diversificada al sector

---

### 5. ❌ Industrias a Evitar

**No recomendadas para wheel con este presupuesto**:
- **Penny stocks** (< $5): Demasiado riesgo, bid-ask spreads horribles
- **Retail tradicional**: Declive estructural
- **Real estate comercial**: Problemas post-pandemia
- **Criptomonedas**: Volatilidad extrema sin fundamentos

---

## 🎯 Estrategia de Diversificación

Con $3,000 de presupuesto, **enfoque en la misma empresa**:
- **Enfoque concentrado**: Operas 1 sola empresa (mejor entendimiento, especialización)
- **Puts semanales en cascada**: Separados 1 semana para crear flujo consistente
  - Semana 1: Vender put(s) que vence en 7 días
  - Semana 2: Vender nuevo(s) put(s) (los anteriores están cerrándose)
  - Semana 3: Los puts de semana 1 expiran, repites con nuevos
  - Resultado: **1 semana cerrándose cada semana**, margen reutilizable

**Diversificación futura** (cuando crezca a $6,000+):
- Mantén 1 empresa principal (puts semanales)
- Alterna covered calls con 1-2 empresas secundarias si hay asignaciones
- Ejemplo:
  - Semanas 1-4: Puts en Empresa A
  - Si asignan: Covered calls 4-6 semanas, luego vuelves a Empresa A
  - Mientras tanto: Si hay tiempo, pequeñas posiciones en Empresa B

---

## 📋 Checklist Pre-Trade

Antes de vender PUT en cualquier stock:
- [ ] ¿IV Rank > 30%?
- [ ] ¿Stock price entre $15-60?
- [ ] ¿Open Interest > 500?
- [ ] ¿Bid-Ask spread < $0.15?
- [ ] ¿Prima ≥ 1.5% de mi capital por contrato?
- [ ] ¿Entiendo el negocio de la empresa?
- [ ] ¿Estaría cómodo manteniendo 100 acciones si me asignan? (Fase 2)
- [ ] ¿La industria tiene potencial a mediano plazo?
- [ ] ¿Hay opciones semanales disponibles?

Si respuesta es NO a cualquiera → **Buscar otro stock**

---

## 📝 Registro y Seguimiento

- **Último registro**: [Actualizar con fecha]
