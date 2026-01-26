import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration
st.set_page_config(
    page_title="Hypothesis Tradeoffs",
    page_icon="⚖️",
    layout="wide"
)

# 2. Context
st.title("⚖️ Hypothesis Testing: The Art of the Tradeoff")
st.markdown("""
In statistics, you can't have it all. When we test a new treatment, we are constantly balancing the risk of being wrong against the cost of the study. 
Use the sliders to explore how these variables compete with one another.
""")

# 3. Sidebar Controls
with st.sidebar:
    st.header("The Levers of Power")
    
    alpha = st.slider("Significance Level (alpha)", 0.01, 0.20, 0.05, step=0.01,
                      help="The 'Strictness' of your study.")
    
    mu_null = 0.0
    
    mu_alt = st.slider("Effect Size (mu_a)", 0.5, 5.0, 2.0, step=0.1,
                       help="How much of a difference the treatment actually makes.")
    
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

y_null = norm.pdf(x, mu_null, se)
ax.plot(x, y_null, label="Null Hypothesis (H0)", color="black", lw=2)

y_alt = norm.pdf(x, mu_alt, se)
ax.plot(x, y_alt, label="Alt Hypothesis (Ha)", color="blue", lw=2, linestyle="--")

# Shading regions
ax.fill_between(x, y_null, where=(x >= z_crit), color="red", alpha=0.4, label="Type I Error (False Alarm)")
ax.fill_between(x, y_alt, where=(x < z_crit), color="blue", alpha=0.2, label="Type II Error (Missed Detection)")
ax.fill_between(x, y_alt, where=(x >= z_crit), color="green", alpha=0.3, label="Power (Correct Discovery)")

ax.axvline(z_crit, color="red", linestyle=":", lw=2, label=f"Critical Value ({z_crit:.2f})")

ax.set_title("The Overlap of Truth and Error", fontsize=14)
ax.set_xlabel("Observed Sample Mean", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.legend(loc="upper right")
ax.grid(axis='y', alpha=0.3)

st.pyplot(fig)



# 6. Metrics
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Alpha (False Alarm Risk)", f"{alpha*100:.0f}%")
m2.metric("Beta (Missing the Truth)", f"{beta*100:.1f}%")
m3.metric("Power (Discovery Probability)", f"{power*100:.1f}%")

# 7. THE TRADEOFFS SECTION
st.divider()
st.header("🔍 Analysis of Tradeoffs")

t1, t2 = st.columns(2)

with t1:
    st.subheader("Slider 1: Significance Level (alpha)")
    st.write("**The Tradeoff:** Decreasing alpha makes you a 'stricter' scientist, but what happens to the green Power region?")
    st.write("*Question:* If you reduce your risk of a False Alarm to 1%, how much harder is it to actually discover the effect?")

    st.subheader("Slider 2: Effect Size (mu_a)")
    st.write("**The Tradeoff:** This is often out of your control. It represents how 'obvious' the truth is.")
    st.write("*Question:* As the two curves move further apart, why does Power increase even if you don't change your sample size?")

with t2:
    st.subheader("Slider 3: Sample Size (n)")
    st.write("**The Tradeoff:** In the real world, $n$ costs money and time. It 'squashes' the curves to make them skinnier.")
    st.write("*Question:* If you double your sample size, how does that affect the Standard Error and the overlap between the two hypotheses?")

    st.subheader("Slider 4: Population Noise (sigma)")
    st.write("**The Tradeoff:** This represents the natural variation in your data.")
    st.write("*Question:* If your data is extremely 'noisy' (High sigma), how much more 'Power' do you lose compared to a very consistent population?")

# Bottom padding
st.write("")
st.write("")
