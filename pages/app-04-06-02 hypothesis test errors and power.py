import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_config = st.set_page_config(
    page_title="Stats Lab: Hypothesis Basics",
    page_icon="📊",
    layout="wide"
)

# 2. Narrative Intro
st.title("📊 Visualizing Hypothesis Errors & Power")
st.markdown("""
This lab explores the fundamental tension in statistical decision-making. 
We compare the **Null Hypothesis ($H_0$)**, representing no effect, 
against the **Alternative Hypothesis ($H_a$)**, representing a real-world change.
""")

# 3. Sidebar Controls
with st.sidebar:
    st.header("The Math Levers")
    
    alpha = st.slider("Significance Level (α)", 0.01, 0.20, 0.05, step=0.01,
                      help="The probability of a Type I Error (False Alarm).")
    
    st.divider()
    mu_null = 0.0
    mu_alt = st.slider("Effect Size (Expected Mean)", 0.5, 5.0, 2.0, step=0.1,
                       help="How far apart the 'Truth' is from the 'Null'.")
    
    sigma = st.number_input("Population Std Dev (σ)", value=2.0, min_value=0.1)
    
    n = st.number_input("Sample Size (n)", min_value=1, value=10, step=1,
                        help="Increasing n makes the curves narrower.")

# 4. Statistical Calculations
se = sigma / np.sqrt(n)
z_crit = norm.ppf(1 - alpha, mu_null, se)
power = 1 - norm.cdf(z_crit, mu_alt, se)
beta = 1 - power 

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 5))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null Hypothesis ($H_0$)", color="black", lw=2)

y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alt Hypothesis ($H_a$)", color="blue", lw=2, linestyle="--")



# Shading the regions
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Alpha (Type I Error)")
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label="Beta (Type II Error)")
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power (1 - β)")

ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Critical Value ({z_crit:.2f})")

# Labels & Styling
ax.set_title("Distribution of Sample Means", fontsize=14)
ax.set_xlabel("Sample Mean (x-bar)", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right", frameon=True)
ax.grid(axis='y', alpha=0.2)

st.pyplot(fig)

# 6. Dashboard Metrics
st.divider()
c1, c2, c3, c4 = st.columns(4)
c
