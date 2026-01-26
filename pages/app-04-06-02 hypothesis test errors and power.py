import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_page_config(
    page_title="Focus Fuel: Research Sim",
    page_icon="⚖️",
    layout="wide"
)

# 2. The Narrative Scenario
st.title("🧪 The 'Focus Fuel' Research Simulator")
st.markdown("### Context: You are the Lead Scientist")

st.info("""
**The Mission:** Your company has $15,000 to prove *Focus Fuel* works. 
Every student you recruit costs **$500**. You must design a study with high **Power**, 
keep the **False Alarm** risk low, and stay under **Budget**.
""")

# 3. Sidebar Controls
with st.sidebar:
    st.header("Design Parameters")
    
    alpha = st.slider("Significance Level (alpha)", 0.01, 0.20, 0.05, step=0.01)
    
    test_type = st.radio("Test Direction", ["One-Tailed (Predicting Increase)", "Two-Tailed (Predicting Change)"])
    
    st.divider()
    mu_null = 0.0
    mu_alt = st.slider("Expected Effect Size (mu_a)", 0.5, 5.0, 2.0, step=0.1)
    sigma = st.number_input("Population Noise (sigma)", value=2.0, min_value=0.1)
    
    st.divider()
    n = st.number_input("Sample Size (n)", min_value=1, value=10, step=1)
    
    st.divider()
    run_sim = st.button("🚀 Run One Study (Sample)")

# 4. Statistical Calculations
se = sigma / np.sqrt(n)
cost = n * 500
budget_remaining = 15000 - cost

# Critical Value and Power Logic
if test_type == "One-Tailed (Predicting Increase)":
    z_crit = norm.ppf(1 - alpha, mu_null, se)
    power = 1 - norm.cdf(z_crit, mu_alt, se)
else:
    z_crit_low = norm.ppf(alpha/2, mu_null, se)
    z_crit = norm.ppf(1 - alpha/2, mu_null, se)
    power = (1 - norm.cdf(z_crit, mu_alt, se)) + norm.cdf(z_crit_low, mu_alt, se)

beta = 1 - power 

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 5))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null (Placebo)", color="black", lw=2)

y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alternative (Focus Fuel)", color="blue", lw=2, linestyle="--")

# Shading
if test_type == "One-Tailed (Predicting Increase)":
    ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Alpha (False Alarm)")
    ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power")
    ax.axvline(z_crit, color="red", linestyle=":", label="Evidence Threshold")
else:
    ax.fill_between(x, y_null, where=(x >= z_crit) | (x <= z_crit_low), color="red", alpha=0.4, label="Alpha (False Alarm)")
    ax.fill_between(x, y_alt, where=(x >= z_crit) | (x <= z_crit_low), color="green", alpha=0.3, label="Power")
    ax.axvline(z_crit, color="red", linestyle=":")
    ax.axvline(z_crit_low, color="red", linestyle=":", label="Thresholds")

# "Run Study" Simulation Dot
if run_sim:
    sample_mean = np.random.normal(mu_alt, se)
    ax.scatter(sample_mean, 0.02, color="gold", s=200, zorder=5, label="Your Study Result", edgecolor="black")
    if (test_type == "One-Tailed (Predicting Increase)" and sample_mean >= z_crit) or \
       (test_type == "Two-Tailed (Predicting Change)" and (sample_mean >= z_crit or sample_mean <= z_crit_low)):
        st.balloons()
        st.success(f"SUCCESS! Your study found a significant result (Mean = {sample_mean:.2f})")
    else:
        st.error(f"FAILED. Your study result (Mean = {sample_mean:.2f}) was not significant.")

ax.legend(loc="upper right")
ax.set_title("Study Design Dashboard")
st.pyplot(fig)



# 6. Dashboard Metrics
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Study Cost", f"${cost:,}", delta=f"Budget: ${budget_remaining:,}", delta_color="normal")
c2.metric("Discovery Power", f"{power*100:.1f}%")
c3.metric("Alpha (Risk)", f"{alpha*100:.0f}%")
c4.metric("Standard Error", f"{se:.3f}")

# 7. THE TRADEOFFS SECTION
st.divider()
st.header("⚖️ Analyzing the Trade-offs")

t1, t2 = st.columns(2)

with t1:
    st.subheader("The Cost
