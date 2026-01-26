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
st.markdown("""
This tool visualizes the relationship between the Null Hypothesis ($H_0$) and a specific Alternative Hypothesis ($H_a$). 
Adjust the sliders to see how the Significance Level ($\\alpha$), Effect Size, and Sample Size change the likelihood of making errors.
""")

# 3. Sidebar Controls for "Vibe" and Parameters
with st.sidebar:
    st.header("Simulation Parameters")
    
    alpha = st.slider("Significance Level (α)", 0.01, 0.20, 0.05, step=0.01, 
                      help="The probability of rejecting a true null hypothesis (Type I Error).")
    
    mu_null = 0.0
    
    mu_alt = st.slider("Alternative Mean (μ_a)", 0.5, 4.0, 2.0, step=0.1,
                       help="The true mean under the Alternative Hypothesis (Effect Size).")
    
    sigma = st.number_input("Population Std Dev (σ)", value=1.0, min_value=0.1)
    
    n = st.number_input("Sample Size (n)", min_value=1, value=4, step=1,
                        help="Increasing n decreases the Standard Error, 'narrowing' the curves.")

# 4. Statistical Calculations
# Standard Error: SE = sigma / sqrt(n)
se = sigma / np.sqrt(n)

# Critical Value (Z-score for a right-tailed test)
z_crit = norm.ppf(1 - alpha, mu_null, se)

# Calculate Power: P(Reject H0 | Ha is true)
# Power = Area under Ha curve to the right of the critical value
power = 1 - norm.cdf(z_crit, mu_alt, se)
beta = 1 - power  # Type II Error

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 6))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

# Null Distribution Curve (H0)
y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null Hypothesis ($H_0$)", color="black", lw=2)

# Alternative Distribution Curve (Ha)
y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alt Hypothesis ($H_a$)", color="blue", lw=2, linestyle="--")

# Shading Type I Error (Alpha)
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label=f"α (Type I Error)")

# Shading Type II Error (Beta)
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label=f"β (Type II Error)")

# Shading Power (1 - Beta)
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label=f"Power (1 - β)")

# Vertical Line for Critical Value
ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Critical Value ({z_crit:.2f})")

# Chart Formatting
ax.set_title(f"Visualizing Error and Power (n={n}, α={alpha})", fontsize=14)
ax.set_xlabel("Sample Mean ($\dotsb$)", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right", frameon=True)
ax.grid(axis='y', alpha=0.3)

# Display the Plot
st.pyplot(fig)



# 6. Summary Metrics
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Alpha (α)", f"{alpha:.2f}")
m2.metric("Beta (β)", f"{beta:.3f}")
m3.metric("Power (1-β)", f"{power:.3f}", delta=f"{power:.2f}", delta_color="normal")
m4.metric("Standard Error", f"{se:.3f}")

# 7. Instructional Context (The "LMS" Touch)
with st.expander("🎓 Interpret the Results"):
    st.write(f"""
    - **Type I Error (α):** There is a **{alpha*100:.0f}%** chance you will say the mean has changed when it actually hasn't.
    - **Type II Error (β):** There is a **{beta*100:.1f}%** chance you will fail to detect the change even though the mean is actually {mu_alt}.
    - **Power:** You have a **{power*100:.1f}%** chance of correctly detecting the effect.
    
    **Teacher's Challenge:** Try increasing the Sample Size ($n$) to 10 or 20. Notice how the curves get 'skinnier' and the Power increases without changing $\\alpha$!
    """)
