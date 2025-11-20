import streamlit as st

def calculate_percentage(points):
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
    st.title("Retinal Detachment Risk Assessment")
    st.write("Complete this questionnaire to assess your risk of retinal detachment.")
    st.warning("⚠️ **Medical Disclaimer**: This tool is for informational purposes only and does not replace professional medical advice. If you have concerns about your eye health, please consult an eye care professional immediately.")
    
    st.markdown("---")
    
    points = 0
    emergency_override = False
    
    st.header("A) Demographics")
    age = st.number_input("Age (years):", min_value=0, max_value=120, value=30, step=1)
    if age >= 70:
        points += 3
    elif age >= 60:
        points += 2
    elif age >= 40:
        points += 1
    
    sex = st.radio("Sex assigned at birth:", ["Female", "Male"])
    if sex == "Male":
        points += 1
    
    st.markdown("---")
    st.header("B) Eye History")
    
    prior_rd = st.radio("Ever diagnosed with retinal detachment in either eye?", ["No", "Yes"])
    if prior_rd == "Yes":
        points += 5
    
    cataract = st.radio("Cataract surgery in this eye?", ["No", "Yes", "Not sure"])
    if cataract == "Yes":
        points += 2
    
    yag = st.radio("Nd:YAG posterior capsulotomy (laser) in this eye?", ["No", "Yes", "Not sure"])
    if yag == "Yes":
        points += 2
    
    myopia = st.radio("Do you wear glasses/contacts for nearsightedness (myopia)?", ["No", "Yes"])
    if myopia == "Yes":
        myopia_level = st.radio("Approximate prescription:", ["None", "Mild (< -3D)", "Moderate (-3 to -6D)", "High (≤ -6D)", "Don't know"])
        if myopia_level == "Mild (< -3D)":
            points += 1
        elif myopia_level == "Moderate (-3 to -6D)":
            points += 2
        elif myopia_level == "High (≤ -6D)":
            points += 4
    
    retinal_condition = st.radio("Any known retinal condition (e.g., lattice degeneration) diagnosed by an eye doctor (this eye)?", ["No", "Yes", "Not sure"])
    if retinal_condition == "Yes":
        points += 4
    
    eye_trauma = st.radio("Any prior significant eye trauma to this eye?", ["No", "Yes"])
    if eye_trauma == "Yes":
        points += 3
    
    st.markdown("---")
    st.header("C) Systemic / Family History")
    
    diabetes = st.radio("Do you have diabetes?", ["No", "Yes", "Not sure"])
    if diabetes == "Yes":
        points += 1
    
    family_history = st.radio("Family history of retinal detachment?", ["No", "Yes", "Not sure"])
    if family_history == "Yes":
        points += 3
    
    st.markdown("---")
    st.header("D) Current Symptoms")
    
    floaters = st.radio("New floaters in the last few days (this eye)?", ["No", "Yes"])
    if floaters == "Yes":
        points += 3
        floaters_onset = st.radio("If yes, started:", ["More than 48 hours ago", "Within 48 hours"], key="floaters_onset")
        if floaters_onset == "Within 48 hours":
            points += 1
    
    flashes = st.radio("Flashes of light in the last few days (this eye)?", ["None", "Occasional", "Frequent"])
    if flashes == "Occasional":
        points += 2
        flashes_onset = st.radio("If occasional/frequent, started:", ["More than 48 hours ago", "Within 48 hours"], key="flashes_onset")
        if flashes_onset == "Within 48 hours":
            points += 1
    elif flashes == "Frequent":
        points += 3
        flashes_onset = st.radio("If occasional/frequent, started:", ["More than 48 hours ago", "Within 48 hours"], key="flashes_onset2")
        if flashes_onset == "Within 48 hours":
            points += 1
    
    shadow = st.radio("Dark shadow/curtain/veil in vision (this eye)?", ["No", "Yes"])
    if shadow == "Yes":
        points += 8
        shadow_onset = st.radio("If yes, how long ago?", ["More than 24 hours ago", "Within 24 hours"], key="shadow_onset")
        if shadow_onset == "Within 24 hours":
            points += 2
            emergency_override = True
    
    vision_decrease = st.radio("Sudden decrease in vision (this eye)?", ["No", "Yes"])
    if vision_decrease == "Yes":
        points += 5
        vision_onset = st.radio("If yes, onset:", ["More than 24 hours ago", "Within 24 hours"], key="vision_onset")
        if vision_onset == "Within 24 hours":
            points += 2
            emergency_override = True
    
    pain = st.radio("New double vision or severe eye pain (this eye)?", ["No", "Yes"])
    if pain == "Yes":
        points += 1
    
    st.markdown("---")
    st.header("E) Visual Function & Follow-up")
    
    vision_level = st.radio("Approximate vision in this eye (without correction):", ["20/20 or better", "20/30–20/60", "20/80–20/200", "Worse than 20/200", "Don't know"])
    if vision_level == "20/30–20/60":
        points += 1
    elif vision_level == "20/80–20/200":
        points += 2
    elif vision_level == "Worse than 20/200":
        points += 3
    
    last_exam = st.radio("Date of last dilated eye exam (if known):", ["Within 2 years", "More than 2 years ago", "Never"])
    if last_exam == "More than 2 years ago":
        points += 1
    elif last_exam == "Never":
        points += 2
    
    st.markdown("---")
    st.header("F) Lifestyle / Recent Triggers (last 3 months)")
    
    recent_triggers = st.multiselect("Recent potential triggers (check all that apply):", 
                                     ["Heavy head/eye trauma", "Contact sports", "Heavy lifting/physical strain immediately before symptoms", "None", "Not sure"])
    if "Heavy head/eye trauma" in recent_triggers or "Contact sports" in recent_triggers:
        points += 3
    if "Heavy lifting/physical strain immediately before symptoms" in recent_triggers:
        points += 1
    
    st.markdown("---")
    
    if st.button("Calculate My Risk", type="primary"):
        percentage = calculate_percentage(points)
        
        st.markdown("---")
        st.header("📊 Your Results")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Points", points)
        with col2:
            st.metric("Estimated Risk", f"{percentage:.1f}%")
        
        if emergency_override or points >= 15:
            st.error("### 🚨 VERY HIGH RISK (Emergency)")
            st.error("**You are at VERY HIGH RISK for retinal detachment.**")
            st.error("**⚠️ Please seek emergency eye care TODAY (same day).**")
        elif points >= 10:
            st.warning("### ⚠️ HIGH RISK")
            st.warning(f"**You are at HIGH RISK for retinal detachment ({percentage:.1f}%).**")
            st.warning("**Urgent evaluation within 24 hours is recommended.**")
        elif points >= 5:
            st.info("### ℹ️ MODERATE RISK")
            st.info(f"**You are at MODERATE RISK for retinal detachment ({percentage:.1f}%).**")
            st.info("**Schedule eye exam within 1–3 days, sooner if symptoms worsen.**")
        else:
            st.success("### ✅ LOW RISK")
            st.success(f"**You are at LOW RISK for retinal detachment ({percentage:.1f}%).**")
            st.success("**Monitor and seek care if new/worsening symptoms appear.**")
        
        st.markdown("---")
        st.info("💡 **Remember**: This assessment is a screening tool only. If you have any concerns about your vision or eye health, please contact an eye care professional immediately.")

if __name__ == "__main__":
    main()
