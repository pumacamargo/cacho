# 📊 Contexto de Trading de Opciones

## Objetivos y Estrategia

| Parámetro | Valor |
|-----------|-------|
| **Objetivo** | Generar ingresos vendiendo opciones (puts y calls) |
| **Estrategia** | Wheel (repetible, genera premium) |
| **Presupuesto** | 3,000 USD |
| **Broker** | Webull |
| **Meta** | 20-40% anual (~$600-1,200/año) |

---

## 🎡 Wheel Strategy

La estrategia wheel tiene **3 fases**:

### FASE 1: VENTA DE PUT

- Vendes put OTM (fuera del dinero)
- Recibes premium
- Si el precio baja y es asignado, compras 100 acciones

### FASE 2: POSESIÓN DE STOCK (opcional)

- Si fuiste asignado, ahora tienes 100 acciones

### FASE 3: VENTA DE CALL CUBIERTO

- Vendes call sobre las acciones que posees
- Recibes más premium
- Si es asignado, vendes las acciones con ganancia

**Ciclo**: 4-8 semanas
**Ganancia esperada**: 4-8% por ciclo

---

## ⚙️ Parámetros de Entrada

### Venta de PUT

| Parámetro | Valor |
|-----------|-------|
| **Stock price** | < $30 USD |
| **DTE** | 30-45 días a expiración |
| **Delta** | -0.35 a -0.25 (30-35% out of the money) |
| **IV Rank** | > 60% (volatilidad alta = más premium) |
| **Open Interest** | > 500 |
| **Bid-Ask spread** | < $0.15 |

### Salida

- **Take Profit**: 50% de ganancia (cierre rápido, menos riesgo)
- **Usar Limit Order** para automatizar

---

## 🔍 Búsqueda de Stocks

### En Webull: Market → Options → Screener

**Filtros principales**:
- Symbols: Whole Market
- Days to Expire: 30 to 45
- Volume: 500 to 136,340
- Open Interest: 500 to 525,654
- Delta: -0.35 to -0.25

**Después de resultados, filtra manualmente**:
- Stock price < $30
- IV Rank > 60%
- Bid-Ask spread < $0.15

**Frecuencia**: Revisa cada 2-3 días para nuevas oportunidades

---

## 🏭 Industrias Recomendadas para Wheel Strategy

### Criterios de Selección

Al elegir stocks para vender puts, priorizar industrias que combinen:
- ✅ **Alta volatilidad** (IV > 60%) = Mejor premium
- ✅ **Stocks < $30** = Compatible con presupuesto de $3,000
- ✅ **Potencial largo plazo** = Si te asignan, puedes mantener con confianza
- ✅ **Liquidez** = Open Interest > 500, Bid-Ask < $0.15

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

Con $3,000 de presupuesto, **enfoque conservador**:
- **1 posición activa** a la vez (vender 1 put contract)
- Rotar entre 2-3 sectores diferentes
- Ejemplo:
  - Ciclo 1: Energía limpia
  - Ciclo 2: Biotech
  - Ciclo 3: Energía limpia
  - Evitar concentración excesiva

**Si crece el capital a $6,000+**:
- Puedes tener 2 posiciones simultáneas en sectores diferentes

---

## 📋 Checklist Pre-Trade

Antes de vender PUT en cualquier stock:
- [ ] ¿IV Rank > 60%?
- [ ] ¿Stock price < $30?
- [ ] ¿Open Interest > 500?
- [ ] ¿Entiendo el negocio de la empresa?
- [ ] ¿Estaría cómodo manteniendo 100 acciones si me asignan?
- [ ] ¿La industria tiene vientos a favor a largo plazo?
- [ ] ¿Premium > 4% del margen requerido?

Si respuesta es NO a cualquiera → **Buscar otro stock**

---

## 📝 Registro y Seguimiento

- **Último registro**: [Actualizar con fecha]
