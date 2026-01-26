import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_page_config(
    page_title="Hypothesis Testing Scenario",
    page_icon="🧪",
    layout="wide"
)

# 2. The Narrative Context
st.title("🧪 The 'Focus Fuel' Experiment")
st.subheader("Scenario: Testing a New Study Supplement")

st.markdown("""
**The Situation:** A company claims their new drink, *Focus Fuel*, increases math test scores. 
As a statistician, you are running a study to see if this is true.

* **Null Hypothesis ($H_0$):** The drink does nothing. The mean score increase is **0**.
* **Alternative Hypothesis ($H_a$):** The drink works! The mean score increases by the **Effect Size** you set below.
""")

st.info("🎯 **Goal:** Your job is to find the 'Sweet Spot' where you have enough **Power** to prove the drink works without having too high of a risk of a **Type I Error** (Alpha).")

# 3. Sidebar Controls
with st.sidebar:
    st.header("Experiment Settings")
    
    alpha = st.slider("Significance Level (alpha)", 0.01, 0.20, 0.05, step=0.01,
                      help="The risk you take of saying the drink works when it actually doesn't.")
    
    mu_null = 0.0
    
    mu_alt = st.slider("Expected Score Increase (mu_a)", 0.5, 5.0, 2.0, step=0.1,
                       help="If the drink works, how many points do we expect it to add to a score?")
    
    sigma = st.number_input("Standard Deviation of Scores (sigma)", value=2.0, min_value=0.1)
    
    n = st.number_input("Number of Students in Study (n)", min_value=1, value=10, step=1)

# 4. Statistical Calculations
se = sigma / np.sqrt(n)
z_crit = norm.ppf(1 - alpha, mu_null, se)
power = 1 - norm.cdf(z_crit, mu_alt, se)
beta = 1 - power 

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 6))
x = np.linspace(mu_null - 4*se, mu_alt + 4*se, 1000)

y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="H0: Drink is Useless", color="black", lw=2)

y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Ha: Drink Works", color="blue", lw=2, linestyle="--")

# Shading
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Type I Error (False Alarm)")
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label="Type II Error (Missed Detection)")
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power (Success!)")

ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Evidence Threshold ({z_crit:.2f})")

ax.set_title("Distribution of Average Test Score Increases", fontsize=14)
ax.set_xlabel("Average Points Gained", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right")
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)



# 6. Result Metrics with Narrative Labels
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("False Alarm Risk (alpha)", f"{alpha*100:.0f}%")
m2.metric("Missed Discovery Risk (beta)", f"{beta*100:.1f}%")
m3.metric("Discovery Power", f"{power*100:.1f}%")

# 7. Student Discussion Questions
st.divider()
with st.expander("📝 Discussion Questions for Lab Report"):
    st.write("""
    1. **The Budget Crisis:** If hiring more students ($n$) is expensive, what happens to your ability to detect the drink's effect?
    2. **The Strict Scientist:** If you lower Alpha to 0.01 (to be very sure), what happens to your **Power**? Why is this a trade-off?
    3. **The 'Miracle' Drink:** If the drink is incredibly effective (Large Effect Size), do you need a large sample size to prove it works?
    """)

# Bottom padding
st.write("")
st.write("")
