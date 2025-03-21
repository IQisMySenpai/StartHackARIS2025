### Algorithm Logic Document Summary

#### Brazil

**Products:**
1. **Stress Buster**
   - **Description:** Helps plants tolerate and recover from abiotic stress (cold, heat, drought, wounding).
   - **Crops:** Soybean, Corn, Cotton

2. **Nutrient Booster**
   - **Description:** Increases nutrient use efficiency.
   - **Crops:** Soybean, Corn

3. **Yield Booster**
   - **Description:** Ensures maximum productivity.
   - **Crops:** Soybean, Corn, Cotton

---

#### India

**Products:**
1. **Stress Buster**
   - **Description:** Helps plants tolerate and recover from abiotic stress (cold, heat, drought, wounding).
   - **Crops:** Rice, Wheat, Cotton

2. **Yield Booster**
   - **Description:** Ensures maximum productivity.
   - **Crops:** Rice, Wheat, Cotton

---

### Algorithms Logic

#### 1. Stress Buster

**A. Diurnal Heat Stress Risk (Daytime)**
- **Scale:** 0 (no stress) to 9 (maximum stress)
- **Equation:**
  - \( \text{Diurnal heat stress} = 0 \) for \( TMAX \leq TMaxOptimum \)
  - \( \text{Diurnal heat stress} = 9 \times \left( \frac{TMAX - TMaxOptimum}{TMaxLimit - TMaxOptimum} \right) \) for \( TMaxOptimum < TMAX < TMaxLimit \)
  - \( \text{Diurnal heat stress} = 9 \) for \( TMAX \geq TMaxLimit \)

**Crops and Temperatures:**
- Soybean: TMaxOptimum = 32°C, TmaxLimit = 45°C
- Corn: TMaxOptimum = 33°C, TmaxLimit = 44°C
- Cotton: TMaxOptimum = 32°C, TmaxLimit = 38°C
- Rice: TMaxOptimum = 32°C, TmaxLimit = 38°C
- Wheat: TMaxOptimum = 25°C, TmaxLimit = 32°C

**B. Nighttime Heat Stress Risk**
- **Scale:** 0 (no stress) to 9 (maximum stress)
- **Equation:**
  - \( \text{Nighttime heat stress} = 0 \) for \( TMIN < TMinOptimum \)
  - \( \text{Nighttime heat stress} = 9 \times \left( \frac{TMIN - TMinOptimum}{TMinLimit - TMinOptimum} \right) \) for \( TMinOptimum \leq TMIN < TMinLimit \)
  - \( \text{Nighttime heat stress} = 9 \) for \( TMIN \geq TMinLimit \)

**Crops and Temperatures:**
- Soybean: TMinOptimum = 22°C, TminLimit = 28°C
- Corn: TMinOptimum = 22°C, TminLimit = 28°C
- Cotton: TMinOptimum = 20°C, TminLimit = 25°C
- Rice: TMinOptimum = 22°C, TminLimit = 28°C
- Wheat: TMinOptimum = 15°C, TminLimit = 20°C

**C. Frost Stress**
- **Equation:**
  - \( \text{Frost stress} = 0 \) for \( TMIN \geq TMinNoFrost \)
  - \( \text{Frost stress} = 9 \times \left[ \frac{|TMIN - TMinNoFrost|}{|TminFrost - TMinNoFrost|} \right] \) for \( TMIN < TMinNoFrost \)
  - \( \text{Frost stress} = 9 \) for \( TMIN \leq TMinFrost \)

**Crops and Temperatures:**
- Soybean: TMinNoFrost = 4°C, TminFrost = -3°C
- Corn: TMinNoFrost = 4°C, TminFrost = -3°C
- Cotton: TMinNoFrost = 4°C, TminFrost = -3°C
- Rice: NA
- Wheat: NA

**D. Drought Risk**
- **Drought Index (DI):**
  - \( DI = \frac{(P - E) + SM}{T} \)
  - **Variables:**
    - \( P \): Cumulative rainfall (mm)
    - \( E \): Cumulative evaporation (mm)
    - \( SM \): Soil moisture content (mm or %)
    - \( T \): Average temperature (°C)

- **Interpretation :**
  - \( DI > 1 \): No risk
  - \( DI = 1 \): Medium risk
  - \( DI < 1 \): High risk

---

#### 2. Yield Booster

**A. Yield Risk Calculation**
- **Approaches:**
  1. Gather historical yield data from growers to assess risk and recommend biosimulation.
  2. Calculate yield risk using the formula below.

- **Yield Risk Formula:**
  \[
  YR = w_1 \cdot (GDD - GDD_{opt})^2 + w_2 \cdot (P - P_{opt})^2 + w_3 \cdot (pH - pH_{opt})^2 + w_4 \cdot (N - N_{opt})^2
  \]
  
  **Where:**
  - \( GDD \): Actual Growing Degree Days
  - \( GDD_{opt} \): Optimal Growing Degree Days
  - \( P \): Actual rainfall (mm)
  - \( P_{opt} \): Optimal rainfall for growth (mm)
  - \( pH \): Actual soil pH
  - \( pH_{opt} \): Optimal soil pH
  - \( N \): Actual available nitrogen in the soil (kg/ha)
  - \( N_{opt} \): Optimal nitrogen availability for soybean (kg/ha)
  - \( w_1, w_2, w_3, w_4 \): Weighting factors for each variable.

**Example Weighting Factors:**
- \( w_1 \) (GDD): 0.3
- \( w_2 \) (Precipitation): 0.3
- \( w_3 \) (pH): 0.2
- \( w_4 \) (Nitrogen): 0.2

**Optimal Values for Crops:**

| Crop Name | GDD Optimal | Precipitation Optimal | pH Optimal | N Optimal (kg/ha) |
|-----------|-------------|-----------------------|-------------|--------------------|
| Soybean   | 2400-3000   | 450-700 mm            | 6.0-6.8     | 0-0.026            |
| Corn      | 2700-3100   | 500-800 mm            | 6.0-6.8     | 0.077-0.154        |
| Cotton    | 2200-2600   | 700-1300 mm           | 6.0-6.5     | 0.051-0.092        |
| Rice      | 2000-2500   | 1000-1500 mm          | 5.5-6.5     | 0.051-0.103        |
| Wheat     | 2000-2500   | 1000-1500 mm          | 5.5-6.5     | 0.051-0.103        |

**B. Growing Degree Days (GDD) Calculation:**
\[
GDD = \left( \frac{T_{max} + T_{min}}{2} \right) - T_{base}
\]
**Where:**
- \( T_{max} \): Maximum daily temperature
- \( T_{min} \): Minimum daily temperature
- \( T_{base} \): Base temperature (threshold for plant growth)