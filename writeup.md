# Credit Quant Assessment

## 1. Pricing Credit Default Swaps

### 1.1 Methodology for Pricing Credit Default Swaps

Credit Default Swaps (CDS) are priced based on two main components:
- **Premium Leg:** The present value of periodic premium payments made by the protection buyer.
- **Protection Leg:** The expected present value of the contingent default payment from the protection seller.

### 1.2 Models for CDS Pricing
CDS pricing models are categorized into:
#### Reduced-Form Models
- **Jarrow-Turnbull (Single-Factor Hazard Rate Model):** Assumes an exogenous Poisson process for default.
- **Duffie-Singleton (Stochastic Intensity Model):** Allows the hazard rate to follow a stochastic process.
- **Jump-to-Default Models:** Extend hazard rate models by incorporating sudden credit spread jumps.

#### Structural Models
- **Merton Model:** Default occurs when firm value falls below a debt threshold.
- **Black-Cox Model:** Extends Merton by allowing early default if the asset value breaches a barrier.
- **Longstaff-Schwartz Model:** Uses Monte Carlo to model the first passage time to default.

### 1.3 Assumptions
- **Reduced-Form Models:** Assume default is an external event, independent of firm fundamentals.
- **Structural Models:** Link default to a firm’s asset dynamics and capital structure.

---

### 1.4 Python Implementation
#### Key Inputs:
- **Risk-Free Rate (rf_rate)**
- **Credit Spread (credit_spread)**
- **Recovery Rate (recovery_rate)**
- **CDS Coupon Rate (coupon)**
- **Time to maturity (tenor)**
- **Upfront payment (upfront)**

#### Example Pricing of a 5-Year CDS
**Given Parameters:**
- Recovery Rate: 40%
- Credit Spread: 1%
- Risk-Free Rate: 4%
- CDS Coupon: 1%
- No upfront payment

**Python Code Implementation:** *(See attached `cds.py` file)*

---

### 1.5 Par Spread as a Function of Recovery Rate
The relationship between the par spread and recovery rate is graphed using the implemented model.

---

## 2. Credit Curve Stripping

### 2.1 Methodology for Credit Curve Stripping
Stripping the credit curve from multiple CDS contracts involves:
1. **Bootstrapping Hazard Rates:** Using market CDS spreads across tenors to solve for piecewise-constant hazard rates.
2. **Survival Probability Estimation:** Using \( P(T) = e^{-\int_0^T \lambda(u) du} \)
3. **Curve Construction:** Iteratively solving for hazard rates using a numerical solver.

### 2.2 Python Implementation
A prototype credit curve stripper is implemented assuming a single CDS quote. *(See `cds.py` for details.)*

---

## Instructions to Run the Solution
### 3.1 Prerequisites
Ensure you have Python 3 installed along with the required dependencies. You can install them using:
```sh
pip install numpy argparse matplotlib scipy
```

### 3.2 Running the Script
The script `cds.py` provides a command-line interface (CLI) for pricing a CDS and stripping a credit curve. The following options are available:

#### **Basic CDS Pricing:**
```sh
python cds.py p --rf_rate 0.02
```

#### **Stripping a Credit Curve:**
```sh
python cds.py s --upfront 0.01
```

#### **Explanation of Arguments:**
- `--tenor`: CDS contract maturity in years.
- `--credit_spread`: Market CDS spread in decimal format (e.g., 0.01 for 100bp).
- `--rf_rate`: Constant risk-free rate in decimal format (e.g., 0.04 for 4%).
- `--recovery_rate`: Assumed recovery rate upon default in decimal format (e.g., 0.4 for 40%).
- `--coupon`: CDS coupon rate in decimal format (e.g., 0.01 for 100bp).
- `--upfront`: Upfront payment in decimal format (e.g., 0.01 for 1%).
