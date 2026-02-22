# Data-driven Drought Classification for Indian Subdivisions

This project builds a weighted rainfall index to estimate drought severity
for Indian Meteorological Department (IMD) subdivisions using historical rainfall data.

A small Python tool that uses historical rainfall data to classify drought severity
(Extreme / Moderate / Mild / No Drought) for IMD subdivisions using a weighted
annual rainfall index.

## Data

Input CSV (e.g. `Rainfall_Data_LL.csv`) is expected to contain at least:

- `SUBDIVISION` – region name (e.g. *East Uttar Pradesh*)
- `YEAR` – calendar year
- Monthly columns: `JAN, FEB, ..., DEC`
- `ANNUAL` – annual rainfall (not directly used for the index, but kept)

The code currently:
- Drops rows with missing values in any monthly column.
- Filters by `SUBDIVISION` to build a region-specific historical series.

## Methodology

### 1. Monthly weights

For each region, we compute the mean rainfall for each month across all years:

W = Σ(weight × rainfall)

Then we define the monthly weight:

wₘ = μₘ / Σ(μₖ for all months k)
weight(month) = mean_rainfall_of_month ÷ total_mean_rainfall_of_all_months

So months with typically higher rainfall get higher weight.

### 2. Weighted annual rainfall index

For a given year (or user-provided scenario), with monthly rainfall \( R_m \),
we compute the weighted annual index:

W = Σ(wₘ × Rₘ)

Where:

- wₘ = monthly weight
- Rₘ = rainfall in month m

If some user months are missing, we fill them with the historical mean of that month
for the region before computing .

### 3. Drought thresholds from historical distribution

For the chosen region, we compute the weighted annual index \( W \) for each
historical year, and then estimate quantile-based thresholds:

T_extreme  = 20th percentile of historical weighted index  
T_moderate = 40th percentile of historical weighted index  
T_mild     = 60th percentile of historical weighted index



### 4. Drought classification rule

For a user year with index \( W_\text{user} \):

If W_user < T_extreme  → Extreme Drought  
Else if W_user < T_moderate → Moderate Drought  
Else if W_user < T_mild → Mild Drought  
Else → No Drought


### 5. Percentile / probability metric

p = count(historical_W < W_user) ÷ total_historical_years

dryness_percentile = p × 100
We compute:

```python
annual = historical['weighted_annual']
p = (annual < W_user).mean()
dryness_percentile =  p*100
```

## How to run

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt ```
   
Ensure Rainfall_Data_LL.csv is placed at the path expected by test.py
or update csv_path in the code.
