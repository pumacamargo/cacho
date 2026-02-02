# Template Google Sheets - Portafolio de Inversiones 2026

## 📋 Estructura General

Este template tiene 6 hojas (sheets):
1. **DASHBOARD** - Vista resumida y distribución
2. **PORTAFOLIO ACTUAL** - Todas tus posiciones actuales
3. **HISTORIAL TRANSACCIONES** - Log de compras/ventas
4. **CUENTAS** - Resumen por tipo de cuenta
5. **SEÑALES ALERTA** - Monitor de indicadores clave
6. **CONFIGURACIÓN** - Datos base (tipos de cambio, targets)

---

## 🎯 SHEET 1: DASHBOARD

### Sección A: Resumen de Cuentas

```
| Cuenta | Saldo CAD | % Total |
|--------|-----------|---------|
| RRSP | [=SUM(CUENTAS!...)] | [=A2/SUM($A$2:$A$5)] |
| Cash CAD | | |
| TFSA | | |
| Japón | | |
| Opciones | | |
| NISA | | |
| TOTAL | | 100% |
```

### Sección B: Distribución Actual vs Target

```
| Categoría | Actual CAD | % Actual | Target % | Desviación | ✅/⚠️ |
|-----------|-----------|----------|----------|------------|-------|
| Activos Productivos | | | 40% | | |
| REITs/Infraestructura | | | 15% | | |
| Metales & Commodities | | | 20% | | |
| Cash + CETES | | | 20% | | |
| Crypto | | | 5% | | |
```

**Fórmulas:**
- `% Actual` = `Actual CAD / SUM(Actual CAD)`
- `Desviación` = `% Actual - Target %`
- `✅/⚠️` = `IF(ABS(Desviación)<=0.05, "✅", "⚠️")`

---

## 📊 SHEET 2: PORTAFOLIO ACTUAL

Estructura: Una fila por posición actual

```
| Ticker | Nombre | Cuenta | Categoría | Shares | Precio CAD | Valor CAD | % Portfolio | Notas |
|--------|--------|--------|-----------|--------|-----------|-----------|------------|-------|
| EQIX | Equinix | RRSP | REITs | 50 | 525.00 | 26,250 | 11.5% | Data Center |
| DLR | Digital Realty | RRSP | REITs | 75 | 135.00 | 10,125 | 4.4% | Infraestructura |
| NVDA | Nvidia | TFSA | Semiconductores | 25 | 850.00 | 21,250 | 9.3% | High Beta |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Columnas Clave:**
- `Valor CAD` = `Shares * Precio CAD` (actualizar precios manualmente o via API)
- `% Portfolio` = `Valor CAD / SUM(Valor CAD)`

---

## 📝 SHEET 3: HISTORIAL TRANSACCIONES

Estructura: Un registro por cada compra/venta

```
| Fecha | Tipo | Ticker | Nombre | Cuenta | Shares | Precio | Comisión | Valor Total | Notas |
|-------|------|--------|--------|--------|--------|--------|----------|-------------|-------|
| 2026-02-01 | BUY | EQIX | Equinix | RRSP | 50 | 520.00 | 10 | 26,010 | Compra inicial |
| 2026-02-03 | BUY | NVDA | Nvidia | TFSA | 25 | 840.00 | 5 | 21,005 | High Beta |
| 2026-02-15 | SELL | DLR | Digital | RRSP | 10 | 138.00 | 8 | 1,372 | Toma ganancias |
```

**Cálculos:**
- `Valor Total` = `(Shares * Precio) + Comisión` (si es BUY) o `(Shares * Precio) - Comisión` (si es SELL)
- Rastrea ganancia/pérdida: `Precio Venta - Precio Promedio Compra`

---

## 💼 SHEET 4: CUENTAS

Resumen dinámico por cada cuenta

```
| Cuenta | Tipo | Saldo Total CAD | Equity | Cash | Crypto | Target % | Actual % | Estado |
|--------|------|-----------------|--------|------|--------|----------|----------|--------|
| RRSP | Inversión LP | 100,000 | 95,000 | 5,000 | 0 | 43.7% | 43.7% | ✅ |
| Cash CAD | Liquidez | 100,000 | 0 | 95,000 | 5,000 | 43.7% | 43.7% | ✅ |
| TFSA | Agresivo | 12,000 | 12,000 | 0 | 0 | 5.2% | 5.2% | ✅ |
| Japón | Cobertura | 17,000 | 16,000 | 1,000 | 0 | 7.4% | 7.4% | ✅ |
| Opciones | Trading | 0 | 0 | 0 | 0 | — | 0% | Nuevo |
| NISA | Japón Tax-Free | 0 | 0 | 0 | 0 | — | 0% | Nuevo |
| TOTAL | | 229,000 | 223,000 | 101,000 | 5,000 | 100% | 100% | ✅ |
```

---

## ⚠️ SHEET 5: SEÑALES ALERTA

Monitor de indicadores clave

```
| Indicador | Señal Actual | Threshold | Status | Acción |
|-----------|-------------|-----------|--------|--------|
| ASML Guidance | -2% | -5% | 🟢 OK | Monitorear |
| HBM Prices YoY | -8% | -20% | 🟢 OK | Monitorear |
| Gas Natural $/MMBTU | 3.50 | <2.00 | 🟢 OK | Monitorear |
| High Yield Spreads | 450 bps | >600 bps | 🟢 OK | Monitorear |
| USD/CAD | 1.38 | <1.30 | 🟢 OK | Aumentar CETES si <1.30 |
| JPY/USD | 155 | <170 | 🟢 OK | Aumentar exportadores si <170 |
| VIX | 14 | >20 | 🟢 OK | Risk-Off si >20 |
```

---

## ⚙️ SHEET 6: CONFIGURACIÓN

Datos base y referencias

```
| Parámetro | Valor | Notas |
|-----------|-------|-------|
| Fecha Actualización | 2026-02-01 | Cambiar según necesario |
| USD/CAD | 1.38 | Actualizar manualmente |
| MXN/CAD | 0.0192 | Para convertir CETES |
| JPY/CAD | 0.00864 | Para convertir cuenta Japón |
| CAD Líquido Mínimo | 5,000 | No bajar de esto |
| Cash Ready to Deploy | 15,000 | Pólvora seca |
| Rebalanceo Trimestral | Q1, Q2, Q3, Q4 | 1 viernes de cada trimestre |
```

### Targets de Distribución
```
| Categoría | Target % | Target CAD |
|-----------|----------|-----------|
| Activos Productivos | 40% | 91,600 |
| REITs/Infraestructura | 15% | 34,350 |
| Metales & Commodities | 20% | 45,800 |
| Cash + CETES | 20% | 45,800 |
| Crypto | 5% | 11,450 |
```

---

## 🛠️ CÓMO CONFIGURAR EN GOOGLE SHEETS

### Paso 1: Crear las 6 hojas
1. Abre Google Sheets
2. Crea un nuevo sheet llamado "Portfolio 2026"
3. Renombra la primera hoja a "DASHBOARD"
4. Crea 5 hojas más: PORTAFOLIO ACTUAL, HISTORIAL, CUENTAS, SEÑALES, CONFIGURACIÓN

### Paso 2: Configurar CONFIGURACIÓN
- Llena los parámetros base (tipos de cambio, targets)
- Usa referencias de celda (ej: `=$C$2` para USD/CAD)

### Paso 3: Crear PORTAFOLIO ACTUAL
- Usa esta estructura
- `Valor CAD` = `=D3*E3` (Shares × Precio)
- `% Portfolio` = `=G3/SUM($G$3:$G$100)`

### Paso 4: Crear HISTORIAL TRANSACCIONES
- Cada vez que compres/vendas, agrega una fila
- Usa SUMA condicionales para calcular costo promedio por ticker

### Paso 5: Crear CUENTAS
- Usa SUMIF para sumar por cuenta
- Ej: `=SUMIF('PORTAFOLIO ACTUAL'!B:B,"RRSP",'PORTAFOLIO ACTUAL'!G:G)`

### Paso 6: Crear DASHBOARD
- Usa referencias a CUENTAS y PORTAFOLIO ACTUAL
- Agrega gráficos de torta para distribución actual vs target

### Paso 7: Crear SEÑALES ALERTA
- Columna de status con condicionales
- `=IF(B2>C2,"🔴 ALERTA","🟢 OK")`

---

## 📌 TIPS PARA GOOGLE SHEETS

### Validación de Datos (Dropdowns)
- Crear dropdown en columna "Tipo" (BUY/SELL)
- Crear dropdown en columna "Cuenta" (RRSP, Cash, TFSA, Japón, Opciones, NISA)
- Crear dropdown en columna "Categoría" (ver categorías en contexto.md)

### Formateo Condicional
- Rojo si `Desviación > +5%` (sobreexpuesto)
- Amarillo si `Desviación > +2%` (levemente sobreexpuesto)
- Verde si `|Desviación| <= 2%` (balanceado)

### Gráficos
- Gráfico de torta: Distribución Actual vs Target (lado a lado)
- Gráfico de línea: Evolución del portafolio en el tiempo
- Gráfico de barras: Valor por categoría

### Formulas Avanzadas
- `=SUMPRODUCT()` para calcular costo promedio por acción
- `=VLOOKUP()` para traer datos de otras hojas
- `=SPARKLINE()` para mini gráficos de tendencia

---

## 🆕 CUENTAS NUEVAS: OPCIONES Y NISA

### Columna Adicional en PORTAFOLIO ACTUAL

Agregar columna para cada tipo de posición:

```
| ... | Tipo Posición | Vencimiento | Strike | Premium |
|-----|---------------|-------------|--------|---------|
| | Stock | — | — | — |
| | Call | 2026-03-15 | 130.00 | 2.50 |
| | Put | 2026-04-20 | 120.00 | 1.75 |
| | NISA Stock | — | — | — |
```

### Sheet Adicional: OPCIONES DETALLADO

```
| Fecha Apertura | Ticker | Tipo | Strike | Vencimiento | Precio Entrada | Premium Recibido | P&L Actual | Estado |
|-------|--------|------|--------|------------|---------------|-----------------|--------------|--------|
| 2026-02-01 | SPY | Call | 560 | 2026-03-15 | 2.50 | 250 | +50 | Abierto |
| 2026-02-03 | QQQ | Put | 420 | 2026-03-20 | 1.75 | 175 | -25 | Abierto |
```

### NISA (Nippon Individual Savings Account)

```
| Ticker | Nombre | Shares | Precio JPY | Valor JPY | Valor CAD | Notas |
|--------|--------|--------|-----------|-----------|----------|-------|
| 9501.T | Tokyo Electric | 100 | 1,850 | 185,000 | 1,597 | Utilities |
| 4502.T | Takeda Pharma | 50 | 3,200 | 160,000 | 1,382 | Pharma |
```

---

## 📊 EJEMPLO INICIAL (Números Ficticios para Test)

**PORTAFOLIO ACTUAL:**
```
EQIX, 50 shares, 525, RRSP → 26,250 CAD
DLR, 75 shares, 135, RRSP → 10,125 CAD
NVDA, 25 shares, 850, TFSA → 21,250 CAD
MNT.TO, 200 shares, 125, Cash → 25,000 CAD (Oro)
BTCC.B.TO, 2,000 shares, 2.50, Cash → 5,000 CAD (Crypto)
```

**TOTAL:** 87,625 CAD invertido
**CASH DISPONIBLE:** 141,375 CAD

---

## 🎯 PASOS PRÓXIMOS

1. **Copiar este template a Google Sheets**
2. **Llenar PORTAFOLIO ACTUAL con tus posiciones reales**
3. **Configurar validaciones y formateo condicional**
4. **Crear gráficos de dashboard**
5. **Usar HISTORIAL TRANSACCIONES para cada cambio**
6. **Revisar mensualmente, rebalancear trimestralmente**

