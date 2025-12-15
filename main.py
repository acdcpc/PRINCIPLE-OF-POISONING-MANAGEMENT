import streamlit as st

st.set_page_config(page_title="Pediatric Poisoning Management", layout="centered")

st.title("🩺 Principles of Poisoning Management in Children")
st.markdown("**Algorithmic Tool with Weight-Based Dosing** – UpToDate-Aligned (2025)")
st.info("Doses per UpToDate pediatric toxicology guidelines.Use clinical judgment.")

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

# Dose calculator function
def dose_calc(dose_per_kg, unit="mg", max_dose=None, min_dose=None, fixed=False):
    if fixed:
        return f"{dose_per_kg} {unit}"
    dose = dose_per_kg * weight_kg
    if max_dose and dose > max_dose:
        dose = max_dose
    if min_dose and dose < min_dose:
        dose = min_dose
    return f"{dose:.1f} {unit} ({dose_per_kg} {unit}/kg)"

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
        if age_years < 1:  # Neonate/infant
            st.markdown(f"- **D10W bolus: 2–3 mL/kg IV** → {dose_calc(2.5, unit='mL D10W')} (0.2–0.3 g/kg glucose)")
        else:
            st.markdown(f"- **D10W bolus: 2–5 mL/kg IV** → {dose_calc(3.5, unit='mL D10W')} (0.2–0.5 g/kg glucose)")
        st.markdown("- Follow with GIR 5–8 mg/kg/min infusion (titrate to BG >70 mg/dL)")

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

    # 3. Antidotes (UpToDate-aligned, weight-based)
    st.markdown("### 3. Antidotes & Targeted Therapy")
    toxin = suspected_toxin

    if "acetaminophen" in toxin or "paracetamol" in toxin:
        st.success("N-AC IV (UpToDate 21-hr protocol)")
        st.markdown(f"- Load: {dose_calc(150, unit='mg')} over 1 hr")
        st.markdown(f"- 50 mg/kg over 4 hr: {dose_calc(50, unit='mg')}")
        st.markdown(f"- 100 mg/kg over 16 hr: {dose_calc(100, unit='mg')} (max 10 g total/day)")

    if "iron" in toxin:
        st.success("Deferoxamine if severe (UpToDate: serum Fe >350 mcg/dL or shock)")
        st.markdown(f"- IV infusion: 5–15 mg/kg/hr → Start {dose_calc(5, unit='mg/hr')} (max 6 g/day)")

    if "digoxin" in toxin:
        st.success("Digoxin Fab (UpToDate: if arrhythmias/hyperK/massive OD)")
        st.info("Dose: (serum dig ng/mL × wt × 0.6)/0.5 vials; empiric 2–5 vials (80–200 mg) in kids")
        st.markdown(f"- Empiric suggestion: 3–5 vials depending on severity")

    if "calcium channel" in toxin or "ccb" in toxin:
        st.success("HIET + Ca (UpToDate)")
        st.markdown(f"- Insulin bolus: 1 unit/kg IV → {dose_calc(1, unit='units')}")
        st.markdown("- Infusion: 0.5–1 unit/kg/hr → Start 0.5 units/kg/hr")
        st.markdown(f"- Ca gluconate 10%: 0.5–1 mL/kg IV → {dose_calc(0.6, max_dose=20, unit='mL')}")

    if "beta blocker" in toxin:
        st.success("HIET + Glucagon (UpToDate)")
        st.markdown(f"- Glucagon bolus: {dose_calc(0.05, max_dose=5, unit='mg')} (0.05–0.1 mg/kg)")

    if "organophosphate" in toxin:
        st.success("Atropine + Pralidoxime (UpToDate)")
        st.markdown(f"- Pralidoxime load: {dose_calc(30, max_dose=2000, unit='mg')} (25–50 mg/kg)")
        st.info("Atropine titrate to secretions: 0.02–0.05 mg/kg IV q3–5min")

    if "opioid" in toxin:
        st.success(f"Naloxone: {dose_calc(0.04, max_dose=2, unit='mg')} IV (0.01–0.1 mg/kg titrate)")

    if "sulfonylurea" in toxin:
        st.success(f"Octreotide: {dose_calc(1.5, max_dose=100, unit='mcg')} SC/IV q6–12h (1–2 mcg/kg)")

    if "cyanide" in toxin:
        st.success(f"Hydroxocobalamin: {dose_calc(70, max_dose=5000, unit='mg')} IV (70 mg/kg, max 5g)")

    # 4. Disposition
    st.markdown("### 4. Disposition & Monitoring")
    if any(s in symptoms for s in ["Altered consciousness / GCS <15", "Seizures", "Bradycardia / Hypotension", "Arrhythmias / AV block"]) or toxin:
        st.error("🚨 Admit to ward/HDU/ICU")
    else:
        st.success("✅ Observe 6–12 hrs if low-risk and asymptomatic")

    if intentional:
        st.warning("🧠 Intentional ingestion → Mandatory psychiatric evaluation + safeguarding")

    st.markdown("### 5. Prevention Counseling")
    st.write("Educate caregivers: safe storage, child-resistant containers, proper medication disposal.")

    st.markdown("---")
    st.caption("Doses from UpToDate Pediatric Toxicology (2025). Verify with local protocols.")

else:
    st.info("Enter patient details above and click 'Generate Plan' to get recommendations.")

# Footer with Creator Info
st.markdown("---")
st.markdown("""
**Developed by:**  
Dr. Prakash Thapa, MD, FPCCM  
Pediatric Intensivist  
Patan Academy of Health Sciences, Lalitpur, Nepal  

**Contact for suggestions / improvements:**  
Email: prakashthapa_paed@pahs.edu.np  

Thank you for using this tool. Feedback is welcome to make it better for clinical use!
""")
st.markdown("Rapid bedside tool for resource-limited settings | Not a substitute for specialist advice")