# Data-driven Drought Classification for Indian Subdivisions

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

\[
\mu_m = \text{mean rainfall in month } m
\]

Then we define the monthly weight:

\[
w_m = \frac{\mu_m}{\sum_{k \in \text{months}} \mu_k}
\]

So months with typically higher rainfall get higher weight.

### 2. Weighted annual rainfall index

For a given year (or user-provided scenario), with monthly rainfall \( R_m \),
we compute the weighted annual index:

\[
W = \sum_{m \in \text{months}} w_m \cdot R_m
\]

If some user months are missing, we fill them with the historical mean of that month
for the region before computing \( W \).

### 3. Drought thresholds from historical distribution

For the chosen region, we compute the weighted annual index \( W \) for each
historical year, and then estimate quantile-based thresholds:

- Extreme drought threshold: \( T_\text{extreme} = Q_{0.20}(W) \)
- Moderate drought threshold: \( T_\text{moderate} = Q_{0.40}(W) \)
- Mild drought threshold: \( T_\text{mild} = Q_{0.60}(W) \)

where \( Q_p \) denotes the empirical \( p \)-th quantile.

### 4. Drought classification rule

For a user year with index \( W_\text{user} \):

- If \( W_\text{user} < T_\text{extreme} \) → **Extreme Drought**
- Else if \( W_\text{user} < T_\text{moderate} \) → **Moderate Drought**
- Else if \( W_\text{user} < T_\text{mild} \) → **Mild Drought**
- Else → **No Drought**

### 5. Percentile / probability metric

Let \( W_1, W_2, \dots, W_N \) be the historical weighted annual values.

We compute:

```python
annual = historical['weighted_annual']
p = (annual < W_user).mean()
dryness_percentile =  p*100

## How to run

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   
Ensure Rainfall_Data_LL.csv is placed at the path expected by test.py
or update csv_path in the code.
