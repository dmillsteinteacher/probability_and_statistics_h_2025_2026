
import streamlit as st

# 1. Setup the browser tab title and icon
st.set_page_config(
    page_title="Prob & Stats H | 2025-2026",
    page_icon="📊",
    layout="wide"
)

# 2. Hero Section
st.title("🎲 Probability & Statistics Honors")
st.markdown(f"### *School Year 2025-2026*")
st.divider()

# 3. Main Layout: Two Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Welcome to the Interactive Lab")
    st.write("""
    This site hosts the custom-built simulations and data analysis tools we use 
    during our honors curriculum. These tools are designed to help you visualize 
    complex distributions and run large-scale simulations that would be 
    impossible to do by hand.
    """)
    
    st.info("👈 **Student Tip:** If you don't see the list of labs, click the **arrow** in the top-left corner to open the sidebar.")

with col2:
    st.header("Quick Links")
    # You can update these URLs to your actual school links
    st.button("🔗 Canvas Dashboard", use_container_width=True)
    st.button("📈 Desmos Graphing Calc", use_container_width=True)
    st.button("📝 Formula Sheet (PDF)", use_container_width=True)

# 4. Footer
st.divider()
st.caption("Developed by [Your Name] • Powered by Streamlit & Vibe Coding")
