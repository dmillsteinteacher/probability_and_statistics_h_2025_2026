import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_page_config(
    page_title="Stats Lab: Focus Fuel",
    page_icon="⚖️",
    layout="wide"
)

# 2. The Narrative Scenario
st.title("🧪 The 'Focus Fuel' Experiment")
st.markdown("### Context: Testing a New Study Supplement")

st.info("""
**The Story:** A startup has developed *Focus Fuel*, a drink they claim increases test scores. 
As the lead researcher, you must design a study to prove it works. 

* **The Null Hypothesis (H0):** The drink is a placebo. Mean score increase = **0**.
* **The Alternative Hypothesis (Ha):** The drink works. Mean score increases by the **Effect Size** you set.
""")

# 3. Sidebar Controls
with st.sidebar:
    st.header("Design Your Study")
    
    alpha = st.slider("Significance Level (alpha)", 0.01, 0.20, 0.05, step=0.01,
                      help="How much 'False Alarm' risk are you willing to take?")
    
    mu_null = 0.0
    
    mu_alt = st.slider("Alternative Mean (Effect Size)", 0.5, 5.0, 2.0, step=0.1,
                       help="How many points do we honestly expect the drink to add?")
    
    sigma = st.number_input("Population Noise (sigma)", value=2.0, min_value=0.1)
    
    n = st.number_input("Sample Size (n)", min_value=1, value=10, step=1)

# 4. Statistical Calculations
se = sigma / np.sqrt(n)
z_crit = norm.ppf(1 - alpha, mu_null, se)
power = 1 - norm.cdf(z_crit, mu_alt, se)
beta = 1 - power 

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 5))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

# Distribution Curves
y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null Hypothesis (Placebo)", color="black", lw=2)

y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alt Hypothesis (Focus Fuel)", color="blue", lw=2, linestyle="--")



# Shading regions
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Type I Error (False Alarm)")
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label="Type II Error (Missed Detection)")
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power (Correct Discovery)")

ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Evidence Threshold ({z_crit:.2f})")

ax.set_title("Will your study detect the difference?", fontsize=14)
ax.set_xlabel("Average Score Points Gained", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right")
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)

# 6. Result Metrics
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("False Alarm Risk (alpha)", f"{alpha*100:.0f}%")
m2.metric("Missed Discovery Risk (beta)", f"{beta*100:.1f}%")
m3.metric("Discovery Power (1 - beta)", f"{power*100:.1f}%")

# 7. THE TRADEOFFS SECTION
st.divider()
st.header("⚖️ Analyzing the Trade-offs")
st.write("Reflect on how your study design choices impact your results.")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("The 'Strictness' Trade-off (Alpha)")
    st.write(f"You currently have Alpha at **{alpha*100:.0f}%**. If you lower this to be more certain, you move the 'Evidence Threshold' to the right.")
    st.write("**Question:** When you make it harder to have a 'False Alarm,' what happens to your overall Power to discover the drink's effect?")

    st.subheader("The 'Truth' Trade-off (Effect Size)")
    st.write(f"The Expected Increase is set to **{mu_alt} points**. This represents how effective the drink actually is.")
    st.write("**Question:** If the drink is only *slightly* better than a placebo, why does your study suddenly need more participants to reach the same Power?")

with col_b:
    st.subheader("The 'Investment' Trade-off (n)")
    st.write(f"You are testing **{n} students**. This affects the 'Standard Error' ({se:.3f}).")
    st.write("**Question:** Increasing $n$ makes the curves narrower. How does this 'squeezing' effect help you distinguish between a placebo and the real drink?")

    st.subheader("The 'Certainty' Trade-off (Beta vs. Power)")
    st.write(f"Your Missed Detection risk (Beta) is **{beta*100:.1f}%**.")
    st.write("**Question:** Is it worse to tell the company their drink works when it doesn't (Alpha), or to tell them it doesn't work when it actually does (Beta)?")

# --- 8. STABILITY PADDING (Ensures file is read completely) ---
st.divider()
st.caption("2026 Honors Stats Lab - Simulation End")
st.write("")
st.write("")
st.write("")
# --- END OF FILE ---
