import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="The Decision Dashboard", layout="wide")

st.title("🎯 The Decision Dashboard: Errors & Power")
st.markdown("""
This app explores the dynamic tension between **Type I Error**, **Type II Error**, and **Power**. 
Use the sliders to see how your choices as a researcher change the 'physical' areas of these probabilities.
""")

# --- Sidebar Controls ---
st.sidebar.header("🕹️ Control Panel")
alpha = st.sidebar.slider("Significance Level (α) - Type I Error Rate", 0.01, 0.20, 0.05, step=0.01)
n = st.sidebar.slider("Sample Size (n) - The Power Lever", 5, 100, 25)
effect_size = st.sidebar.slider("True Shift in Mean (Δ) - Effect Size", 0.1, 2.0, 0.8)
sigma = 1.0  # Assumed population SD for simplicity

# --- Math Logic ---
se = sigma / np.sqrt(n)
# Null is at 0, Alternative is at 'effect_size'
null_mean = 0
alt_mean = effect_size

# Calculate Critical Value (Right-tailed test)
z_crit = norm.ppf(1 - alpha)
x_crit = null_mean + (z_crit * se)

# Calculate Power and Beta
power = 1 - norm.cdf(x_crit, loc=alt_mean, scale=se)
beta = 1 - power

# --- Dashboard Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Alpha (α)", f"{alpha:.2f}", help="Prob. of rejecting a true Null (False Alarm)")
col2.metric("Beta (β)", f"{beta:.2%}", help="Prob. of failing to reject a false Null (Missed Signal)")
col3.metric("Power (1-β)", f"{power:.2%}", help="Prob. of correctly rejecting a false Null (Success)")

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(-1, alt_mean + 3*se, 500)

# Null Distribution (Blue)
y_null = norm.pdf(x, null_mean, se)
ax.plot(x, y_null, label="Null World ($H_0$)", color="#1f77b4", lw=2)
ax.fill_between(x, y_null, where=(x >= x_crit), color="red", alpha=0.3, label="Type I Error (α)")

# Alternative Distribution (Green)
y_alt = norm.pdf(x, alt_mean, se)
ax.plot(x, y_alt, label="Alt World ($H_a$)", color="#2ca02c", lw=2, linestyle="--")
ax.fill_between(x, y_alt, where=(x >= x_crit), color="green", alpha=0.3, label="Power ($1-β$)")
ax.fill_between(x, y_alt, where=(x < x_crit), color="orange", alpha=0.3, label="Type II Error (β)")

# Vertical Decision Line
ax.axvline(x_crit, color="black", linestyle=":", lw=2, label=f"Decision Line (x={x_crit:.3f})")

# Formatting
ax.set_title(f"Dynamic Tension: n={n}, α={alpha}, Power={power:.2%}")
ax.set_xlabel("Sample Mean ($\overline{x}$)")
ax.set_yticks([])
ax.legend(loc='upper right', fontsize='small')
st.pyplot(fig)

# --- Expository Narrative ---
st.info(f"**Insight:** By choosing α={alpha}, you are drawing a line at **{x_crit:.3f}**. "
        f"Anything to the right of this line is 'Evidence for Discovery'. "
        f"Notice how increasing **n** to {n} makes the curves skinnier, reducing the 'Orange' overlap and boosting your Power.")
