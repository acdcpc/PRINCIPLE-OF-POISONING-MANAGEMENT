import streamlit as st

st.set_page_config(page_title="Pediatric Poisoning Management", layout="centered")

st.title("🩺 Principles of Poisoning Management in Children")
st.markdown("Algorithmic Tool with Exact Weight-Based Dosing")
st.info("Total doses calculated precisely for entered weight. Use clinical judgment.")

# Input section
with st.expander("📋 Enter Patient Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age_years = st.number_input("Age (years)", min_value=0, max_value=18, value=5)
        weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=100.0, value=20.0, step=0.1)
    with col2:
        time_since = st.text_input("Time since exposure (e.g., '1 hour', 'unknown')", "unknown")
        suspected_toxin = st.text_input("Suspected toxin (e.g., acetaminophen, iron, digoxin, CCB, organophosphate)", "").strip().lower()

    symptoms = st.multiselect(
        "Select symptoms / toxidrome",
        options=[
            "Altered consciousness / GCS <15",
            "Seizures",
            "Hypoglycemia",
            "Respiratory distress",
            "Bradycardia / Hypotension",
            "Arrhythmias / AV block",
            "Hyperkalemia",
            "Excessive secretions / SLUDGE",
            "Miosis",
            "Mydriasis",
            "Vomiting / Aspiration risk",
            "Corrosive ingestion",
            "Hydrocarbon ingestion"
        ]
    )

    intentional = st.checkbox("Intentional ingestion / Self-harm")

# Improved dose calculator — bold total dose
def dose_calc(dose_per_kg, unit="mg", max_dose=None, min_dose=None, fixed=False):
    if fixed:
        return f"**{dose_per_kg} {unit}**"
    dose = dose_per_kg * weight_kg
    if max_dose and dose > max_dose:
        dose = max_dose
        capped = " (capped at max)"
    else:
        capped = ""
    if min_dose and dose < min_dose:
        dose = min_dose
    total_dose = f"**{dose:.1f} {unit}**{capped}"
    per_kg = f"({dose_per_kg} {unit}/kg)"
    return f"{total_dose} {per_kg}"

if st.button("🔍 Generate Plan"):
    st.markdown("---")
    st.subheader(f"Management Plan: Age {age_years} yrs, Weight {weight_kg:.1f} kg")

    # 1. Stabilization
    st.markdown("### 1. ABCD Stabilization")
    st.markdown("""
    - Airway: Secure if GCS <8 or aspiration risk → Intubate PRN
    - Breathing: O2 if SpO₂ <94%
    - Circulation: IV access, treat shock
    - Disability: **Check BG now**; Exposure: Temp/seizure control
    """)

    if "Hypoglycemia" in symptoms or "Altered consciousness" in symptoms:
        st.warning("🚨 Hypoglycemia – Bolus dextrose NOW (UpToDate)")
        if age_years < 1:
            st.markdown(f"- **D10W bolus**: {dose_calc(2.5, unit='mL D10W')} (average 2–3 mL/kg)")
        else:
            st.markdown(f"- **D10W bolus**: {dose_calc(3.5, unit='mL D10W')} (average 2–5 mL/kg)")
        st.markdown("- Follow with GIR 5–8 mg/kg/min infusion")

    # 2. Decontamination
    st.markdown("### 2. Selective Decontamination")
    hours = None
    try:
        hours = float(time_since.split()[0]) if time_since != "unknown" else None
    except:
        hours = None

    if hours is not None and hours <= 2:
        if "Corrosive ingestion" not in symptoms and "Hydrocarbon ingestion" not in symptoms:
            st.success(f"✅ Activated Charcoal: {dose_calc(1, max_dose=50, unit='g')}")
    else:
        st.info("Charcoal not indicated >2 hrs unless sustained-release")

    # 3. Antidotes
    st.markdown("### 3. Antidotes & Targeted Therapy")
    toxin = suspected_toxin

    if "acetaminophen" in toxin or "paracetamol" in toxin:
        st.success("N-AC IV (UpToDate 21-hr protocol)")
        st.markdown(f"- Loading dose: {dose_calc(150, unit='mg')} over 1 hour")
        st.markdown(f"- Second dose: {dose_calc(50, unit='mg')} over 4 hours")
        st.markdown(f"- Third dose: {dose_calc(100, unit='mg')} over 16 hours")

    if "iron" in toxin:
        st.success("Deferoxamine if severe")
        st.markdown(f"- Start: {dose_calc(5, unit='mg/hour')} IV (titrate up to 15 mg/kg/hr)")

    if "digoxin" in toxin:
        st.success("Digoxin Fab if life-threatening")
        st.info("Empiric pediatric dose: 2–5 vials depending on severity (consult toxicologist for exact calculation)")

    if "calcium channel" in toxin or "ccb" in toxin:
        st.success("HIET + Calcium")
        st.markdown(f"- Insulin bolus: {dose_calc(1, unit='units')} IV")
        st.markdown(f"- Calcium gluconate 10%: {dose_calc(0.6, max_dose=20, unit='mL')} slow IV")

    if "beta blocker" in toxin:
        st.success("Glucagon + HIET")
        st.markdown(f"- Glucagon: {dose_calc(0.05, max_dose=5, unit='mg')} IV bolus")

    if "organophosphate" in toxin:
        st.success("Pralidoxime")
        st.markdown(f"- Loading: {dose_calc(30, max_dose=2000, unit='mg')} IV")

    if "opioid" in toxin:
        st.success(f"Naloxone: {dose_calc(0.04, max_dose=2, unit='mg')} IV (titrate)")

    if "sulfonylurea" in toxin:
        st.success(f"Octreotide: {dose_calc(1.5, max_dose=100, unit='mcg')} SC/IV")

    if "cyanide" in toxin:
        st.success(f"Hydroxocobalamin: {dose_calc(70, max_dose=5000, unit='mg')} IV")

    # Disposition
    st.markdown("### 4. Disposition")
    if any(s in symptoms for s in ["Altered consciousness / GCS <15", "Seizures", "Bradycardia / Hypotension"]) or toxin:
        st.error("🚨 Admit to ward/HDU/ICU")
    else:
        st.success("✅ Observe 6–12 hours if low-risk")

    if intentional:
        st.warning("🧠 Intentional → Psychiatric evaluation + safeguarding")

    st.markdown("---")
    st.caption("Doses from UpToDate Pediatric Toxicology (2025).")

else:
    st.info("Enter details and click 'Generate Plan'")

# Footer
st.markdown("---")
st.markdown("""
**Developed by:**  
Dr. Prakash Thapa, MD, FPCCM  
Pediatric Intensivist  
Patan Academy of Health Sciences, Lalitpur, Nepal  

**Contact for feedback or improvements:**  
Email: prakashthapa_paed@pahs.edu.np  

Thank you for using this tool!
""")