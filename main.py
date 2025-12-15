import streamlit as st

st.set_page_config(page_title="Pediatric Poisoning Management", layout="centered")

st.title("🩺 Principles of Poisoning Management in Children")
st.markdown("Created by Dr.Prakash Thapa,Pediatric Intensivist")

st.info(
    "This tool provides guidance based on standard protocols. Always consult poison center/toxicologist when available.")

# Input section
with st.expander("📋 Enter Patient Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=0, max_value=18, value=5)
        weight = st.number_input("Weight (kg)", min_value=2.0, max_value=100.0, value=20.0, step=0.5)
    with col2:
        time_since = st.text_input("Time since exposure (e.g., 1 hour)", "")
        suspected_toxin = st.text_input("Suspected toxin/substance (e.g., paracetamol, kerosene, organophosphate)", "")

    symptoms = st.multiselect(
        "Select symptoms / toxidrome signs",
        options=[
            "Altered consciousness / GCS <15",
            "Seizures",
            "Hypoglycemia suspected",
            "Respiratory distress",
            "Bradycardia / Hypotension",
            "Excessive secretions / SLUDGE",
            "Miosis (pinpoint pupils)",
            "Mydriasis (dilated pupils)",
            "Hyperthermia",
            "Vomiting / Aspiration risk",
            "Corrosive ingestion suspected",
            "Hydrocarbon ingestion suspected"
        ]
    )

    intentional = st.checkbox("Intentional ingestion / Self-harm suspected")

# Process and show algorithm
if st.button("🔍 Generate Management Plan"):
    st.markdown("---")
    st.subheader("Immediate Management Algorithm")

    # Step 1: ABCD
    st.markdown("### 1. Immediate Stabilization (ABCD)")
    st.markdown("""
    - **Airway**: Assess and secure  
      → If GCS <8, excessive secretions, or aspiration risk → **Prepare for intubation**
    - **Breathing**: Provide oxygen if SpO₂ <94%  
    - **Circulation**: Establish IV access, treat shock  
    - **Disability**: 
      → **Check blood glucose IMMEDIATELY**  
      → Correct hypoglycemia (give D10% or D25% bolus)
    - **Exposure**: Control temperature, manage seizures (benzodiazepines)
    """)

    if "Hypoglycemia suspected" in symptoms or "Altered consciousness" in symptoms:
        st.warning("🚨 Hypoglycemia likely — treat urgently with glucose!")

    # Step 2: History & Risk
    st.markdown("### 2. History & Risk Assessment")
    st.write(f"- Age: {age} years | Weight: {weight} kg")
    if time_since:
        st.write(f"- Time since exposure: {time_since}")
    if suspected_toxin:
        st.write(f"- Suspected toxin: **{suspected_toxin.title()}**")

    # Decontamination recommendations
    st.markdown("### 3. Gastrointestinal Decontamination (Selective Only)")

    if time_since and ("hour" in time_since.lower() or "hours" in time_since.lower()):
        try:
            hours = float(''.join(filter(str.isdigit, time_since)))
            if hours <= 2:
                if "Corrosive" not in symptoms and "Hydrocarbon" not in symptoms:
                    st.success("✅ Consider **Activated Charcoal** (1 g/kg, max 50g) if potentially toxic ingestion")
                else:
                    st.error("❌ Activated charcoal contraindicated (corrosive/hydrocarbon)")
            else:
                st.info("⏰ >2 hours: Activated charcoal usually not helpful unless sustained-release preparation")
        except:
            st.info("Consider activated charcoal only if within 1–2 hours and benefit outweighs risk")

    if "Corrosive ingestion suspected" in symptoms:
        st.error("🚨 CORROSIVE: NO gastric lavage or charcoal → Dilute with water/milk if early")
    if "Hydrocarbon ingestion suspected" in symptoms:
        st.error("🚨 HYDROCARBON: High aspiration risk → NO lavage or charcoal")

    # Specific antidotes
    st.markdown("### 4. Consider Specific Antidotes (If Indicated & Available)")

    toxin_lower = suspected_toxin.lower() if suspected_toxin else ""

    if "paracetamol" in toxin_lower or "acetaminophen" in toxin_lower:
        st.success("💉 **N-acetylcysteine** — Start if risk of toxicity (use nomogram if levels available)")
    elif "organophosphate" in toxin_lower or "pesticide" in toxin_lower or "Excessive secretions" in symptoms:
        st.success("💉 **Atropine** (for secretions) + **Pralidoxime**")
    elif "opioid" in toxin_lower or "Miosis" in symptoms:
        st.success("💉 **Naloxone** — titrate IV (0.01–0.1 mg/kg)")
    elif "benzodiazepine" in toxin_lower:
        st.warning("Flumazenil — rarely used in children (seizure risk)")
    elif "methanol" in toxin_lower or "ethylene glycol" in toxin_lower:
        st.success("💉 **Fomepizole** (preferred) or Ethanol + Hemodialysis")
    elif "iron" in toxin_lower:
        st.info("Whole bowel irrigation may be needed; deferoxamine if severe")
    else:
        st.info("No specific antidote indicated based on input. Focus on supportive care.")

    # Disposition
    st.markdown("### 5. Monitoring & Disposition")

    high_risk = (
            "Altered consciousness" in symptoms or
            "Seizures" in symptoms or
            "Respiratory distress" in symptoms or
            intentional or
            suspected_toxin
    )

    if high_risk:
        st.error("🚨 **Admit to ward/ICU** for close monitoring")
        if "Altered consciousness" in symptoms:
            st.write("• GCS monitoring essential")
    else:
        st.success("✅ May observe for 6–12 hours if low risk and asymptomatic")

    if intentional:
        st.warning("🧠 Intentional ingestion → Mandatory psychiatric evaluation + safeguarding")

    st.markdown("### 6. Prevention Counseling")
    st.write("Educate caregivers on safe storage, child-resistant containers, and reading labels.")

    st.markdown("---")
    st.caption(
        "Based on AAP, RCH Melbourne, EXTRIP, WHO, and UpToDate guidelines (2025). Always use clinical judgment.")

else:
    st.info("Fill in patient details and click 'Generate Management Plan' to get recommendations.")

# Footer
st.markdown("---")
st.markdown("Made for rapid bedside use in resource-limited settings | Not a substitute for specialist advice")