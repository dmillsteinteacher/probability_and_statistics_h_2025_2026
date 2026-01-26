import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_page_config(
    page_title="Hypothesis Error & Power",
    page_icon="📊",
    layout="wide"
)

# 2. App Title and Introduction
st.title("📊 Hypothesis Testing: Type I & II Errors and Power")
st.markdown("Adjust parameters to see how the Significance Level (alpha), Effect Size, and Sample Size change the likelihood of making errors.")

# 3. Sidebar Controls
with st.sidebar:
    st.header("Simulation Parameters")
    
    alpha = st.slider("Significance Level (alpha)", 0.01, 0.20, 0.05, step=0.01)
    
    mu_null = 0.0
    
    mu_alt = st.slider("Alternative Mean (mu_a)", 0.5, 4.0, 2.0, step=0.1)
    
    sigma = st.number_input("Population Std Dev (sigma)", value=1.0, min_value=0.1)
    
    n = st.number_input("Sample Size (n)", min_value=1, value=4, step=1)

# 4. Statistical Calculations
# Standard Error: SE = sigma / sqrt(n)
se = sigma / np.sqrt(n)

# Critical Value (Z-score for a right-tailed test)
z_crit = norm.ppf(1 - alpha, mu_null, se)

# Calculate Power and Beta
power = 1 - norm.cdf(z_crit, mu_alt, se)
beta = 1 - power 

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 6))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

# Null Distribution Curve (H0)
y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null Hypothesis (H0)", color="black", lw=2)

# Alternative Distribution Curve (Ha)
y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alt Hypothesis (Ha)", color="blue", lw=2, linestyle="--")

# Shading regions
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Alpha (Type I Error)")
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label="Beta (Type II Error)")
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power (1 - Beta)")

# Vertical Line for Critical Value
ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Critical Value ({z_crit:.2f})")

# Chart Formatting
ax.set_title(f"Visualizing Error and Power (n={n})", fontsize=14)
ax.set_xlabel("Sample Mean (x-bar)", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right")
ax.grid(axis='y', alpha=0.3)

# Display the Plot
st.pyplot(fig)



# 6. Summary Metrics
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Alpha (alpha)", f"{alpha:.2f}")
m2.metric("Beta (beta)", f"{beta:.3f}")
m3.metric("Power (1-beta)", f"{power:.3f}")
m4.metric("Std Error", f"{se:.3f}")

# 7. Instructional Context (Simplified formatting to prevent SyntaxErrors)
st.divider()
st.header("🎓 Interpretation")

st.write(f"- **Type I Error (alpha):** There is a {alpha*100:.0f}% chance you will reject a true Null Hypothesis.")
st.write(f"- **Type II Error (beta):** There is a {beta*100:.1f}% chance you will fail to detect the change.")
st.write(f"- **Power:** You have a {power*100:.1f}% chance of correctly detecting the effect.")

st.info("Try increasing the Sample Size (n) to see how the Standard Error drops and Power increases!")

# Padding at the bottom
st.write("")
st.write("")
