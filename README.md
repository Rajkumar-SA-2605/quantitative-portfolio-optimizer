# 🛡️ Quantitative Portfolio Analytics & Optimization Engine


An interactive dashboard that uses **Modern Portfolio Theory (MPT)** to analyze equity portfolios, break down risk, and provide data-driven recommendations for diversification.

This engine pre-computes metrics for ~300 NSE stocks, allowing for real-time analysis without API latency.

## ✨ Core Features

*   **Efficient Frontier Visualization:** See where your portfolio stands in the risk-return universe.
*   **Risk Decomposition:** Mathematically splits your portfolio's total risk into **Systematic (Market) Risk** and **Unsystematic (Diversifiable) Risk**.
*   **Proprietary Recommendation Algorithm:** Ranks potential stock additions based on their ability to minimize your unsystematic risk.
*   **Value-Weighted Analysis:** Calculates portfolio metrics using true weights based on `Price × Quantity`.

## 🚀 How to Run

1.  **Clone the Repository**
    ```
    git clone https://github.com/YOUR_USERNAME/quantitative-portfolio-optimizer.git
    cd quantitative-portfolio-optimizer
    ```

2.  **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```
    streamlit run app.py
    ```
    On the first run, the app will auto-generate the `assets_metrics.json` file. This may take 1-2 minutes. Subsequent runs will be instant.

## ⚙️ The Quantitative Engine: How it Works

The dashboard is built on three core financial models:

### 1. Markowitz Mean-Variance Optimization
This is the foundation of the Efficient Frontier. We simulate thousands of portfolios to map the relationship between risk and return.

*   **Expected Return ($E[R_p]$):**
    ![Expected Return](assets/expected_return_white.png)

*   **Portfolio Variance ($\sigma_p^2$):**
    ![Variance](assets/variance_white.png)

    Where:
    - $\mathbf{w}$ is the vector of asset weights.
    - $\mathbf{\Sigma}$ is the covariance matrix of asset returns.

### 2. Risk Decomposition (Systematic vs. Unsystematic)
We use the **Capital Asset Pricing Model (CAPM)** framework to separate risks.

*   **Portfolio Beta ($\beta_p$):** Measures your portfolio's volatility relative to the market (NIFTY 50).
    ![Beta](assets/beta_white.png)

*   **Systematic Risk:** The portion of risk tied to the market.
    ![Systematic Risk](assets/systematic_white.png)

*   **Unsystematic Risk:** The portion of risk unique to your assets, which can be diversified away.
    ![Unsystematic Risk](assets/unsystematic_white.png)


### 3. Proprietary Recommendation Algorithm
This engine finds the best stocks to add to your portfolio to reduce unsystematic risk.
1.  **Iterate:** For each of the 300+ stocks in our universe...
2.  **Simulate:** Temporarily add the candidate stock to your portfolio (at a 10% weight).
3.  **Measure:** Recalculate the new portfolio's total volatility ($\sigma_{new}$).
4.  **Rank:** The "best" stocks are those that cause the largest drop in volatility ($\sigma_{old} - \sigma_{new}$).

## 📂 Project Structure
![Project Structure](assets/project_structure_white.png)

