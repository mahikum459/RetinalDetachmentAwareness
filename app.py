import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Retinal Detachment Risk Assessment",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    h1 {
        color: #1e3a8a;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #1e40af;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3b82f6;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .clinical-notice {
        background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .clinical-notice h3 {
        color: #1e40af;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .clinical-notice p {
        color: #334155;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stMetric"] label {
        font-size: 1rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

def calculate_percentage(points):
    """Convert points to percentage risk using interpolation"""
    if points == 0:
        return 1
    elif points <= 5:
        return 1 + (points / 5) * 7
    elif points <= 10:
        return 8 + ((points - 5) / 5) * 22
    elif points <= 15:
        return 30 + ((points - 10) / 5) * 30
    elif points <= 20:
        return 60 + ((points - 15) / 5) * 15
    elif points <= 25:
        return 75 + ((points - 20) / 5) * 10
    else:
        return min(90, 85 + (points - 25) * 0.5)

def main():
    # Header
    st.markdown("# 👁️ Retinal Detachment Risk Assessment")
    st.markdown('<p class="subtitle">This assessment helps determine how urgently you should see an eye care professional based on your risk factors and symptoms.</p>', unsafe_allow_html=True)
    
    points = 0
    emergency_override = False
    
    # Demographics Section
    st.markdown("## 📋 A) Demographics")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years): *", min_value=0, max_value=120, value=None, step=1, placeholder="Enter your age")
        if age is not None:
            if age >= 70:
                points += 3
            elif age >= 60:
                points += 2
            elif age >= 40:
                points += 1
    with col2:
        sex = st.radio("Sex assigned at birth: *", ["Female", "Male"], index=None)
        if sex == "Male":
            points += 1
    
    # Eye History Section
    st.markdown("## 👁️ B) Eye History")
    
    col1, col2 = st.columns(2)
    with col1:
        prior_rd = st.radio("Ever diagnosed with retinal detachment in either eye? *", ["No", "Yes"], index=None)
        if prior_rd == "Yes":
            points += 5
        
        cataract = st.radio("Cataract surgery in this eye? *", ["No", "Yes", "Not sure"], index=None)
        if cataract == "Yes":
            points += 2
        
        yag = st.radio("Nd:YAG posterior capsulotomy (laser) in this eye? *", ["No", "Yes", "Not sure"], index=None)
        if yag == "Yes":
            points += 2
    
    with col2:
        myopia = st.radio("Do you wear glasses/contacts for nearsightedness (myopia)? *", ["No", "Yes"], index=None)
        if myopia == "Yes":
            myopia_level = st.radio("Approximate prescription: *", ["None", "Mild (< -3D)", "Moderate (-3 to -6D)", "High (≤ -6D)", "Don't know"], index=None)
            if myopia_level == "Mild (< -3D)":
                points += 1
            elif myopia_level == "Moderate (-3 to -6D)":
                points += 2
            elif myopia_level == "High (≤ -6D)":
                points += 4
        
        retinal_condition = st.radio("Any known retinal condition (e.g., lattice degeneration) diagnosed by an eye doctor (this eye)? *", ["No", "Yes", "Not sure"], index=None)
        if retinal_condition == "Yes":
            points += 4
        
        eye_trauma = st.radio("Any prior significant eye trauma to this eye? *", ["No", "Yes"], index=None)
        if eye_trauma == "Yes":
            points += 3
    
    # Systemic/Family History Section
    st.markdown("## 🧬 C) Systemic / Family History")
    col1, col2 = st.columns(2)
    with col1:
        diabetes = st.radio("Do you have diabetes? *", ["No", "Yes", "Not sure"], index=None)
        if diabetes == "Yes":
            points += 1
    with col2:
        family_history = st.radio("Family history of retinal detachment? *", ["No", "Yes", "Not sure"], index=None)
        if family_history == "Yes":
            points += 3
    
    # Current Symptoms Section
    st.markdown("## ⚠️ D) Current Symptoms")
    
    col1, col2 = st.columns(2)
    with col1:
        floaters = st.radio("New floaters in the last few days (this eye)? *", ["No", "Yes"], index=None)
        if floaters == "Yes":
            points += 3
            floaters_onset = st.radio("If yes, started: *", ["More than 48 hours ago", "Within 48 hours"], key="floaters_onset", index=None)
            if floaters_onset == "Within 48 hours":
                points += 1
        
        flashes = st.radio("Flashes of light in the last few days (this eye)? *", ["None", "Occasional", "Frequent"], index=None)
        if flashes == "Occasional":
            points += 2
            flashes_onset = st.radio("If occasional/frequent, started: *", ["More than 48 hours ago", "Within 48 hours"], key="flashes_onset", index=None)
            if flashes_onset == "Within 48 hours":
                points += 1
        elif flashes == "Frequent":
            points += 3
            flashes_onset = st.radio("If occasional/frequent, started: *", ["More than 48 hours ago", "Within 48 hours"], key="flashes_onset2", index=None)
            if flashes_onset == "Within 48 hours":
                points += 1
        
        shadow = st.radio("Dark shadow/curtain/veil in vision (this eye)? *", ["No", "Yes"], index=None)
        if shadow == "Yes":
            points += 8
            shadow_onset = st.radio("If yes, how long ago? *", ["More than 24 hours ago", "Within 24 hours"], key="shadow_onset", index=None)
            if shadow_onset == "Within 24 hours":
                points += 2
                emergency_override = True
    
    with col2:
        vision_decrease = st.radio("Sudden decrease in vision (this eye)? *", ["No", "Yes"], index=None)
        if vision_decrease == "Yes":
            points += 5
            vision_onset = st.radio("If yes, onset: *", ["More than 24 hours ago", "Within 24 hours"], key="vision_onset", index=None)
            if vision_onset == "Within 24 hours":
                points += 2
                emergency_override = True
        
        pain = st.radio("New double vision or severe eye pain (this eye)? *", ["No", "Yes"], index=None)
        if pain == "Yes":
            points += 1
    
    # Visual Function Section
    st.markdown("## 📊 E) Visual Function & Follow-up")
    col1, col2 = st.columns(2)
    with col1:
        vision_level = st.radio("Approximate vision in this eye (without correction): *", 
                               ["20/20 or better", "20/30–20/60", "20/80–20/200", "Worse than 20/200", "Don't know"], index=None)
        if vision_level == "20/30–20/60":
            points += 1
        elif vision_level == "20/80–20/200":
            points += 2
        elif vision_level == "Worse than 20/200":
            points += 3
    with col2:
        last_exam = st.radio("Date of last dilated eye exam (if known): *", 
                            ["Within 2 years", "More than 2 years ago", "Never"], index=None)
        if last_exam == "More than 2 years ago":
            points += 1
        elif last_exam == "Never":
            points += 2
    
    # Lifestyle/Triggers Section
    st.markdown("## 🏋️ F) Lifestyle / Recent Triggers")
    recent_triggers = st.multiselect("Recent potential triggers in the last 3 months (check all that apply): *", 
                                     ["Heavy head/eye trauma", "Contact sports", 
                                      "Heavy lifting/physical strain immediately before symptoms", 
                                      "None", "Not sure"])
    if "Heavy head/eye trauma" in recent_triggers or "Contact sports" in recent_triggers:
        points += 3
    if "Heavy lifting/physical strain immediately before symptoms" in recent_triggers:
        points += 1
    
    # Calculate Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Validation - check if all required fields are filled
    missing_fields = []
    if age is None:
        missing_fields.append("Age")
    if sex is None:
        missing_fields.append("Sex assigned at birth")
    if prior_rd is None:
        missing_fields.append("Prior retinal detachment")
    if cataract is None:
        missing_fields.append("Cataract surgery")
    if yag is None:
        missing_fields.append("Nd:YAG capsulotomy")
    if myopia is None:
        missing_fields.append("Myopia")
    if myopia == "Yes" and myopia_level is None:
        missing_fields.append("Myopia prescription level")
    if retinal_condition is None:
        missing_fields.append("Known retinal condition")
    if eye_trauma is None:
        missing_fields.append("Prior eye trauma")
    if diabetes is None:
        missing_fields.append("Diabetes")
    if family_history is None:
        missing_fields.append("Family history of retinal detachment")
    if floaters is None:
        missing_fields.append("New floaters")
    if floaters == "Yes" and floaters_onset is None:
        missing_fields.append("Floaters onset timing")
    if flashes is None:
        missing_fields.append("Flashes of light")
    if flashes in ["Occasional", "Frequent"] and flashes_onset is None:
        missing_fields.append("Flashes onset timing")
    if shadow is None:
        missing_fields.append("Dark shadow/curtain/veil")
    if shadow == "Yes" and shadow_onset is None:
        missing_fields.append("Shadow onset timing")
    if vision_decrease is None:
        missing_fields.append("Sudden decrease in vision")
    if vision_decrease == "Yes" and vision_onset is None:
        missing_fields.append("Vision decrease onset timing")
    if pain is None:
        missing_fields.append("Double vision or eye pain")
    if vision_level is None:
        missing_fields.append("Approximate vision")
    if last_exam is None:
        missing_fields.append("Date of last dilated eye exam")
    if len(recent_triggers) == 0:
        missing_fields.append("Recent potential triggers")
    
    @st.dialog("📊 Your Risk Assessment Results", width="large")
    def show_results(points, percentage, emergency_override):
        # Metrics
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("Estimated Risk Percentage", f"{percentage:.1f}%")
        with col2:
            if emergency_override or points >= 15:
                risk_tier = "VERY HIGH"
            elif points >= 10:
                risk_tier = "HIGH"
            elif points >= 5:
                risk_tier = "MODERATE"
            else:
                risk_tier = "LOW"
            st.metric("Risk Tier", risk_tier)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Risk Assessment and Recommendations
        if emergency_override or points >= 15:
            st.error("### 🚨 VERY HIGH RISK - EMERGENCY ACTION REQUIRED")
            st.markdown("""
            <div style='background-color: #fee2e2; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #dc2626;'>
                <h4 style='color: #991b1b; margin-top: 0;'>You are at VERY HIGH RISK for retinal detachment</h4>
                <p style='color: #7f1d1d; font-size: 1.1rem; font-weight: 600;'>
                ⚠️ SEEK EMERGENCY EYE CARE TODAY (SAME DAY)
                </p>
                <p style='color: #7f1d1d;'>
                Your symptoms and risk factors indicate a potential retinal detachment emergency. 
                Contact an ophthalmologist or go to an emergency room with ophthalmology services immediately. 
                Prompt treatment can prevent permanent vision loss.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif points >= 10:
            st.warning("### ⚠️ HIGH RISK - URGENT EVALUATION NEEDED")
            st.markdown(f"""
            <div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #f59e0b;'>
                <h4 style='color: #92400e; margin-top: 0;'>You are at HIGH RISK for retinal detachment ({percentage:.1f}%)</h4>
                <p style='color: #78350f; font-size: 1.1rem; font-weight: 600;'>
                📞 URGENT: Schedule evaluation within 24 hours
                </p>
                <p style='color: #78350f;'>
                Contact an eye care professional today to schedule an urgent examination. 
                Your risk factors warrant prompt attention to prevent potential vision loss.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif points >= 5:
            st.info("### ℹ️ MODERATE RISK - SCHEDULE APPOINTMENT SOON")
            st.markdown(f"""
            <div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #3b82f6;'>
                <h4 style='color: #1e40af; margin-top: 0;'>You are at MODERATE RISK for retinal detachment ({percentage:.1f}%)</h4>
                <p style='color: #1e3a8a; font-size: 1.1rem; font-weight: 600;'>
                📅 Schedule eye exam within 1–3 days
                </p>
                <p style='color: #1e3a8a;'>
                While not an emergency, your symptoms warrant timely evaluation. 
                Contact your eye care provider to schedule an appointment. 
                Seek care sooner if symptoms worsen.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("### ✅ LOW RISK - MONITOR SYMPTOMS")
            st.markdown(f"""
            <div style='background-color: #d1fae5; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #10b981;'>
                <h4 style='color: #065f46; margin-top: 0;'>You are at LOW RISK for retinal detachment ({percentage:.1f}%)</h4>
                <p style='color: #064e3b; font-size: 1.1rem; font-weight: 600;'>
                👁️ Continue monitoring your symptoms
                </p>
                <p style='color: #064e3b;'>
                Your current risk is low. Monitor your vision and seek care if you develop new symptoms 
                such as sudden floaters, flashes of light, or vision changes. 
                Maintain regular eye exams as recommended by your eye care provider.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Important Note
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Important**: This screening tool helps determine the urgency of eye care based on evidence-based risk factors. Early detection and treatment of retinal detachment can preserve vision and prevent blindness.")
    
    if st.button("🔍 Calculate My Risk Assessment", type="primary"):
        if missing_fields:
            st.error(f"⚠️ Please complete all required fields (*) before calculating. Missing: {', '.join(missing_fields)}")
        else:
            percentage = calculate_percentage(points)
            show_results(points, percentage, emergency_override)

if __name__ == "__main__":
    main()
