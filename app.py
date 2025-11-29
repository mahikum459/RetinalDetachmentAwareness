import streamlit as st
import os
import psycopg2
from psycopg2 import sql

# Database functions for view counter
def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_counter_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS view_counter (
                id SERIAL PRIMARY KEY,
                counter_name VARCHAR(50) UNIQUE NOT NULL,
                count INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            INSERT INTO view_counter (counter_name, count) 
            VALUES ('assessments', 0) 
            ON CONFLICT (counter_name) DO NOTHING
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        pass

def increment_counter():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE view_counter SET count = count + 1 
            WHERE counter_name = 'assessments'
            RETURNING count
        """)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        return 0

def get_counter():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT count FROM view_counter WHERE counter_name = 'assessments'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else 0
    except Exception as e:
        return 0

# Initialize counter table on startup
init_counter_table()

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
</style>
""", unsafe_allow_html=True)

# Translations
TRANSLATIONS = {
    "English": {
        "title": "👁️ Retinal Detachment Risk Assessment",
        "subtitle": "This assessment helps determine how urgently you should see an eye care professional based on your risk factors and symptoms.",
        "language": "Language:",
        "section_a": "📋 A) Demographics",
        "age": "Age (years): *",
        "age_placeholder": "Enter your age",
        "sex": "Sex assigned at birth: *",
        "female": "Female",
        "male": "Male",
        "section_b": "👁️ B) Eye History",
        "prior_rd": "Ever diagnosed with retinal detachment in either eye? *",
        "cataract": "Cataract surgery in this eye? *",
        "yag": "Nd:YAG posterior capsulotomy (laser) in this eye? *",
        "myopia": "Do you wear glasses/contacts for nearsightedness (myopia)? *",
        "myopia_level": "Approximate prescription: *",
        "myopia_none": "None",
        "myopia_mild": "Mild (< -3D)",
        "myopia_moderate": "Moderate (-3 to -6D)",
        "myopia_high": "High (≤ -6D)",
        "dont_know": "Don't know",
        "retinal_condition": "Any known retinal condition (e.g., lattice degeneration) diagnosed by an eye doctor (this eye)? *",
        "eye_trauma": "Any prior significant eye trauma to this eye? *",
        "yes": "Yes",
        "no": "No",
        "not_sure": "Not sure",
        "section_c": "🧬 C) Systemic / Family History",
        "diabetes": "Do you have diabetes? *",
        "family_history": "Family history of retinal detachment? *",
        "section_d": "⚠️ D) Current Symptoms",
        "floaters": "New floaters in the last few days (this eye)? *",
        "floaters_onset": "If yes, started: *",
        "flashes": "Flashes of light in the last few days (this eye)? *",
        "flashes_none": "None",
        "flashes_occasional": "Occasional",
        "flashes_frequent": "Frequent",
        "flashes_onset": "If occasional/frequent, started: *",
        "shadow": "Dark shadow/curtain/veil in vision (this eye)? *",
        "shadow_onset": "If yes, how long ago? *",
        "vision_decrease": "Sudden decrease in vision (this eye)? *",
        "vision_onset": "If yes, onset: *",
        "pain": "New double vision or severe eye pain (this eye)? *",
        "onset_48h": "Within 48 hours",
        "onset_more_48h": "More than 48 hours ago",
        "onset_24h": "Within 24 hours",
        "onset_more_24h": "More than 24 hours ago",
        "section_e": "📊 E) Visual Function & Follow-up",
        "vision_level": "Approximate vision in this eye (without correction): *",
        "vision_2020": "20/20 or better (0D)",
        "vision_2030": "20/30–20/60 (-0.5D to -1.5D)",
        "vision_2080": "20/80–20/200 (-2.0D to -4.0D)",
        "vision_worse": "Worse than 20/200 (> -4.0D)",
        "last_exam": "Date of last dilated eye exam (if known): *",
        "exam_within_2": "Within 2 years",
        "exam_more_2": "More than 2 years ago",
        "exam_never": "Never",
        "section_f": "🏋️ F) Lifestyle / Recent Triggers",
        "triggers": "Recent potential triggers in the last 3 months (check all that apply): *",
        "trigger_trauma": "Heavy head/eye trauma",
        "trigger_sports": "Contact sports",
        "trigger_lifting": "Heavy lifting/physical strain immediately before symptoms",
        "trigger_none": "None",
        "calculate_btn": "🔍 Calculate My Risk Assessment",
        "reset_btn": "🔄 Start New Assessment",
        "missing_fields": "⚠️ Please complete all required fields (*) before calculating. Missing:",
        "results_title": "Your Risk Assessment Results",
        "disclaimer": "This retinal detachment risk screener provides guidance on how urgently you should seek an eye care evaluation based on your responses. It does not establish a diagnosis or replace an examination by an eye care professional. The recommendations may not account for all individual medical factors. If you are experiencing new or worsening symptoms, contact a qualified eye specialist immediately or seek emergency care.",
        "risk_percentage": "Estimated Risk Percentage",
        "risk_tier": "Risk Tier",
        "very_high": "VERY HIGH",
        "high": "HIGH",
        "moderate": "MODERATE",
        "low": "LOW",
        "very_high_title": "🚨 VERY HIGH RISK - EMERGENCY ACTION REQUIRED",
        "very_high_msg": "You are at VERY HIGH RISK for retinal detachment",
        "very_high_action": "⚠️ SEEK EMERGENCY EYE CARE TODAY (SAME DAY)",
        "very_high_detail": "Your symptoms and risk factors indicate a potential retinal detachment emergency. Contact an ophthalmologist or go to an emergency room with ophthalmology services immediately. Prompt treatment can prevent permanent vision loss.",
        "high_title": "⚠️ HIGH RISK - URGENT EVALUATION NEEDED",
        "high_msg": "You are at HIGH RISK for retinal detachment",
        "high_action": "📞 URGENT: Schedule evaluation within 24 hours",
        "high_detail": "Contact an eye care professional today to schedule an urgent examination. Your risk factors warrant prompt attention to prevent potential vision loss.",
        "moderate_title": "ℹ️ MODERATE RISK - SCHEDULE APPOINTMENT SOON",
        "moderate_msg": "You are at MODERATE RISK for retinal detachment",
        "moderate_action": "📅 Schedule eye exam within 1–3 days",
        "moderate_detail": "While not an emergency, your symptoms warrant timely evaluation. Contact your eye care provider to schedule an appointment. Seek care sooner if symptoms worsen.",
        "low_title": "✅ LOW RISK - MONITOR SYMPTOMS",
        "low_msg": "You are at LOW RISK for retinal detachment",
        "low_action": "👁️ Continue monitoring your symptoms",
        "low_detail": "Your current risk is low. Monitor your vision and seek care if you develop new symptoms such as sudden floaters, flashes of light, or vision changes. Maintain regular eye exams as recommended by your eye care provider.",
        "important_note": "💡 **Important**: This screening tool helps determine the urgency of eye care based on evidence-based risk factors. Early detection and treatment of retinal detachment can preserve vision and prevent blindness."
    },
    "Español": {
        "title": "👁️ Evaluación del Riesgo de Desprendimiento de Retina",
        "subtitle": "Esta evaluación ayuda a determinar con qué urgencia debe consultar a un profesional de la salud ocular según sus factores de riesgo y síntomas.",
        "language": "Idioma:",
        "section_a": "📋 A) Demografía",
        "age": "Edad (años): *",
        "age_placeholder": "Ingrese su edad",
        "sex": "Sexo asignado al nacer: *",
        "female": "Femenino",
        "male": "Masculino",
        "section_b": "👁️ B) Historia Ocular",
        "prior_rd": "¿Alguna vez fue diagnosticado con desprendimiento de retina en cualquier ojo? *",
        "cataract": "¿Cirugía de cataratas en este ojo? *",
        "yag": "¿Capsulotomía posterior Nd:YAG (láser) en este ojo? *",
        "myopia": "¿Usa lentes/lentes de contacto para miopía? *",
        "myopia_level": "Prescripción aproximada: *",
        "myopia_none": "Ninguna",
        "myopia_mild": "Leve (< -3D)",
        "myopia_moderate": "Moderada (-3 a -6D)",
        "myopia_high": "Alta (≤ -6D)",
        "dont_know": "No sé",
        "retinal_condition": "¿Alguna condición retiniana conocida (ej., degeneración lattice) diagnosticada por un oftalmólogo (este ojo)? *",
        "eye_trauma": "¿Algún trauma ocular significativo previo en este ojo? *",
        "yes": "Sí",
        "no": "No",
        "not_sure": "No estoy seguro/a",
        "section_c": "🧬 C) Historia Sistémica / Familiar",
        "diabetes": "¿Tiene diabetes? *",
        "family_history": "¿Historia familiar de desprendimiento de retina? *",
        "section_d": "⚠️ D) Síntomas Actuales",
        "floaters": "¿Nuevas moscas volantes en los últimos días (este ojo)? *",
        "floaters_onset": "Si es sí, comenzó: *",
        "flashes": "¿Destellos de luz en los últimos días (este ojo)? *",
        "flashes_none": "Ninguno",
        "flashes_occasional": "Ocasionales",
        "flashes_frequent": "Frecuentes",
        "flashes_onset": "Si ocasionales/frecuentes, comenzó: *",
        "shadow": "¿Sombra/cortina/velo oscuro en la visión (este ojo)? *",
        "shadow_onset": "Si es sí, ¿hace cuánto tiempo? *",
        "vision_decrease": "¿Disminución repentina de la visión (este ojo)? *",
        "vision_onset": "Si es sí, inicio: *",
        "pain": "¿Visión doble nueva o dolor ocular severo (este ojo)? *",
        "onset_48h": "Dentro de 48 horas",
        "onset_more_48h": "Hace más de 48 horas",
        "onset_24h": "Dentro de 24 horas",
        "onset_more_24h": "Hace más de 24 horas",
        "section_e": "📊 E) Función Visual y Seguimiento",
        "vision_level": "Visión aproximada en este ojo (sin corrección): *",
        "vision_2020": "20/20 o mejor (0D)",
        "vision_2030": "20/30–20/60 (-0.5D a -1.5D)",
        "vision_2080": "20/80–20/200 (-2.0D a -4.0D)",
        "vision_worse": "Peor que 20/200 (> -4.0D)",
        "last_exam": "Fecha del último examen ocular con dilatación (si se conoce): *",
        "exam_within_2": "Dentro de 2 años",
        "exam_more_2": "Hace más de 2 años",
        "exam_never": "Nunca",
        "section_f": "🏋️ F) Estilo de Vida / Desencadenantes Recientes",
        "triggers": "Desencadenantes potenciales recientes en los últimos 3 meses (marque todos los que apliquen): *",
        "trigger_trauma": "Trauma fuerte en cabeza/ojos",
        "trigger_sports": "Deportes de contacto",
        "trigger_lifting": "Levantamiento pesado/esfuerzo físico inmediatamente antes de los síntomas",
        "trigger_none": "Ninguno",
        "calculate_btn": "🔍 Calcular Mi Evaluación de Riesgo",
        "reset_btn": "🔄 Iniciar Nueva Evaluación",
        "missing_fields": "⚠️ Por favor complete todos los campos requeridos (*) antes de calcular. Faltan:",
        "results_title": "Resultados de Su Evaluación de Riesgo",
        "disclaimer": "Este evaluador de riesgo de desprendimiento de retina proporciona orientación sobre la urgencia con la que debe buscar una evaluación de atención ocular según sus respuestas. No establece un diagnóstico ni reemplaza un examen por un profesional de atención ocular. Las recomendaciones pueden no tener en cuenta todos los factores médicos individuales. Si experimenta síntomas nuevos o que empeoran, comuníquese con un especialista ocular calificado inmediatamente o busque atención de emergencia.",
        "risk_percentage": "Porcentaje de Riesgo Estimado",
        "risk_tier": "Nivel de Riesgo",
        "very_high": "MUY ALTO",
        "high": "ALTO",
        "moderate": "MODERADO",
        "low": "BAJO",
        "very_high_title": "🚨 RIESGO MUY ALTO - ACCIÓN DE EMERGENCIA REQUERIDA",
        "very_high_msg": "Usted está en RIESGO MUY ALTO de desprendimiento de retina",
        "very_high_action": "⚠️ BUSQUE ATENCIÓN OFTALMOLÓGICA DE EMERGENCIA HOY (MISMO DÍA)",
        "very_high_detail": "Sus síntomas y factores de riesgo indican una posible emergencia de desprendimiento de retina. Contacte a un oftalmólogo o vaya a una sala de emergencias con servicios de oftalmología inmediatamente. El tratamiento rápido puede prevenir la pérdida permanente de la visión.",
        "high_title": "⚠️ RIESGO ALTO - EVALUACIÓN URGENTE NECESARIA",
        "high_msg": "Usted está en RIESGO ALTO de desprendimiento de retina",
        "high_action": "📞 URGENTE: Programe evaluación dentro de 24 horas",
        "high_detail": "Contacte a un profesional del cuidado ocular hoy para programar un examen urgente. Sus factores de riesgo requieren atención inmediata para prevenir la pérdida potencial de la visión.",
        "moderate_title": "ℹ️ RIESGO MODERADO - PROGRAME CITA PRONTO",
        "moderate_msg": "Usted está en RIESGO MODERADO de desprendimiento de retina",
        "moderate_action": "📅 Programe examen ocular dentro de 1–3 días",
        "moderate_detail": "Aunque no es una emergencia, sus síntomas requieren evaluación oportuna. Contacte a su proveedor de cuidado ocular para programar una cita. Busque atención antes si los síntomas empeoran.",
        "low_title": "✅ RIESGO BAJO - MONITOREE SÍNTOMAS",
        "low_msg": "Usted está en RIESGO BAJO de desprendimiento de retina",
        "low_action": "👁️ Continúe monitoreando sus síntomas",
        "low_detail": "Su riesgo actual es bajo. Monitoree su visión y busque atención si desarrolla nuevos síntomas como moscas volantes repentinas, destellos de luz o cambios en la visión. Mantenga exámenes oculares regulares según lo recomendado por su proveedor de cuidado ocular.",
        "important_note": "💡 **Importante**: Esta herramienta de detección ayuda a determinar la urgencia de la atención ocular basada en factores de riesgo basados en evidencia. La detección y tratamiento tempranos del desprendimiento de retina pueden preservar la visión y prevenir la ceguera."
    },
    "हिंदी": {
        "title": "👁️ रेटिना डिटैचमेंट जोखिम मूल्यांकन",
        "subtitle": "यह मूल्यांकन आपके जोखिम कारकों और लक्षणों के आधार पर यह निर्धारित करने में मदद करता है कि आपको कितनी जल्दी नेत्र चिकित्सा पेशेवर से मिलना चाहिए।",
        "language": "भाषा:",
        "section_a": "📋 A) जनसांख्यिकी",
        "age": "उम्र (वर्ष): *",
        "age_placeholder": "अपनी उम्र दर्ज करें",
        "sex": "जन्म के समय निर्धारित लिंग: *",
        "female": "महिला",
        "male": "पुरुष",
        "section_b": "👁️ B) नेत्र इतिहास",
        "prior_rd": "क्या कभी किसी भी आंख में रेटिना डिटैचमेंट का निदान हुआ है? *",
        "cataract": "इस आंख में मोतियाबिंद सर्जरी? *",
        "yag": "इस आंख में Nd:YAG पोस्टीरियर कैप्सुलोटॉमी (लेज़र)? *",
        "myopia": "क्या आप निकट दृष्टिदोष (मायोपिया) के लिए चश्मा/कॉन्टैक्ट लेंस पहनते हैं? *",
        "myopia_level": "अनुमानित प्रिस्क्रिप्शन: *",
        "myopia_none": "कोई नहीं",
        "myopia_mild": "हल्का (< -3D)",
        "myopia_moderate": "मध्यम (-3 से -6D)",
        "myopia_high": "उच्च (≤ -6D)",
        "dont_know": "पता नहीं",
        "retinal_condition": "क्या नेत्र चिकित्सक द्वारा कोई ज्ञात रेटिना स्थिति (जैसे, लैटिस डिजनरेशन) का निदान किया गया है (इस आंख में)? *",
        "eye_trauma": "इस आंख में कोई पूर्व महत्वपूर्ण आंख का आघात? *",
        "yes": "हाँ",
        "no": "नहीं",
        "not_sure": "निश्चित नहीं",
        "section_c": "🧬 C) प्रणालीगत / पारिवारिक इतिहास",
        "diabetes": "क्या आपको मधुमेह है? *",
        "family_history": "रेटिना डिटैचमेंट का पारिवारिक इतिहास? *",
        "section_d": "⚠️ D) वर्तमान लक्षण",
        "floaters": "पिछले कुछ दिनों में नए फ्लोटर्स (इस आंख में)? *",
        "floaters_onset": "यदि हाँ, शुरू हुआ: *",
        "flashes": "पिछले कुछ दिनों में प्रकाश की चमक (इस आंख में)? *",
        "flashes_none": "कोई नहीं",
        "flashes_occasional": "कभी-कभी",
        "flashes_frequent": "बार-बार",
        "flashes_onset": "यदि कभी-कभी/बार-बार, शुरू हुआ: *",
        "shadow": "दृष्टि में गहरी छाया/पर्दा/घूंघट (इस आंख में)? *",
        "shadow_onset": "यदि हाँ, कितने समय पहले? *",
        "vision_decrease": "दृष्टि में अचानक कमी (इस आंख में)? *",
        "vision_onset": "यदि हाँ, शुरुआत: *",
        "pain": "नई दोहरी दृष्टि या गंभीर आंख दर्द (इस आंख में)? *",
        "onset_48h": "48 घंटों के भीतर",
        "onset_more_48h": "48 घंटे से अधिक समय पहले",
        "onset_24h": "24 घंटों के भीतर",
        "onset_more_24h": "24 घंटे से अधिक समय पहले",
        "section_e": "📊 E) दृश्य कार्य और फॉलो-अप",
        "vision_level": "इस आंख में अनुमानित दृष्टि (सुधार के बिना): *",
        "vision_2020": "20/20 या बेहतर (0D)",
        "vision_2030": "20/30–20/60 (-0.5D से -1.5D)",
        "vision_2080": "20/80–20/200 (-2.0D से -4.0D)",
        "vision_worse": "20/200 से खराब (> -4.0D)",
        "last_exam": "अंतिम डायलेटेड आई परीक्षा की तारीख (यदि ज्ञात हो): *",
        "exam_within_2": "2 वर्षों के भीतर",
        "exam_more_2": "2 वर्ष से अधिक पहले",
        "exam_never": "कभी नहीं",
        "section_f": "🏋️ F) जीवनशैली / हाल के ट्रिगर्स",
        "triggers": "पिछले 3 महीनों में हाल के संभावित ट्रिगर्स (सभी लागू चुनें): *",
        "trigger_trauma": "सिर/आंख में भारी आघात",
        "trigger_sports": "संपर्क खेल",
        "trigger_lifting": "लक्षणों से ठीक पहले भारी उठाना/शारीरिक तनाव",
        "trigger_none": "कोई नहीं",
        "calculate_btn": "🔍 मेरे जोखिम मूल्यांकन की गणना करें",
        "reset_btn": "🔄 नया मूल्यांकन शुरू करें",
        "missing_fields": "⚠️ कृपया गणना करने से पहले सभी आवश्यक फ़ील्ड (*) भरें। गुम:",
        "results_title": "आपके जोखिम मूल्यांकन के परिणाम",
        "disclaimer": "यह रेटिनल डिटैचमेंट जोखिम स्क्रीनर आपकी प्रतिक्रियाओं के आधार पर मार्गदर्शन प्रदान करता है कि आपको कितनी तत्काल नेत्र देखभाल मूल्यांकन लेनी चाहिए। यह निदान स्थापित नहीं करता है या नेत्र देखभाल पेशेवर द्वारा परीक्षा का स्थान नहीं लेता है। सिफारिशें सभी व्यक्तिगत चिकित्सा कारकों को ध्यान में नहीं रख सकती हैं। यदि आप नए या बिगड़ते लक्षणों का अनुभव कर रहे हैं, तो तुरंत किसी योग्य नेत्र विशेषज्ञ से संपर्क करें या आपातकालीन देखभाल लें।",
        "risk_percentage": "अनुमानित जोखिम प्रतिशत",
        "risk_tier": "जोखिम स्तर",
        "very_high": "बहुत उच्च",
        "high": "उच्च",
        "moderate": "मध्यम",
        "low": "कम",
        "very_high_title": "🚨 बहुत उच्च जोखिम - आपातकालीन कार्रवाई आवश्यक",
        "very_high_msg": "आप रेटिना डिटैचमेंट के बहुत उच्च जोखिम में हैं",
        "very_high_action": "⚠️ आज (उसी दिन) आपातकालीन नेत्र देखभाल प्राप्त करें",
        "very_high_detail": "आपके लक्षण और जोखिम कारक संभावित रेटिना डिटैचमेंट आपातकाल का संकेत देते हैं। तुरंत एक नेत्र रोग विशेषज्ञ से संपर्क करें या नेत्र विज्ञान सेवाओं वाले आपातकालीन कक्ष में जाएं। त्वरित उपचार स्थायी दृष्टि हानि को रोक सकता है।",
        "high_title": "⚠️ उच्च जोखिम - तत्काल मूल्यांकन आवश्यक",
        "high_msg": "आप रेटिना डिटैचमेंट के उच्च जोखिम में हैं",
        "high_action": "📞 तत्काल: 24 घंटों के भीतर मूल्यांकन निर्धारित करें",
        "high_detail": "तत्काल परीक्षा निर्धारित करने के लिए आज ही एक नेत्र देखभाल पेशेवर से संपर्क करें। आपके जोखिम कारक संभावित दृष्टि हानि को रोकने के लिए त्वरित ध्यान की मांग करते हैं।",
        "moderate_title": "ℹ️ मध्यम जोखिम - जल्द ही नियुक्ति निर्धारित करें",
        "moderate_msg": "आप रेटिना डिटैचमेंट के मध्यम जोखिम में हैं",
        "moderate_action": "📅 1–3 दिनों के भीतर आंखों की जांच निर्धारित करें",
        "moderate_detail": "हालांकि यह आपातकाल नहीं है, आपके लक्षण समय पर मूल्यांकन की आवश्यकता रखते हैं। नियुक्ति निर्धारित करने के लिए अपने नेत्र देखभाल प्रदाता से संपर्क करें। यदि लक्षण बिगड़ते हैं तो जल्द ही देखभाल प्राप्त करें।",
        "low_title": "✅ कम जोखिम - लक्षणों की निगरानी करें",
        "low_msg": "आप रेटिना डिटैचमेंट के कम जोखिम में हैं",
        "low_action": "👁️ अपने लक्षणों की निगरानी जारी रखें",
        "low_detail": "आपका वर्तमान जोखिम कम है। अपनी दृष्टि की निगरानी करें और यदि आप अचानक फ्लोटर्स, प्रकाश की चमक, या दृष्टि में परिवर्तन जैसे नए लक्षण विकसित करते हैं तो देखभाल प्राप्त करें। अपने नेत्र देखभाल प्रदाता द्वारा अनुशंसित नियमित नेत्र परीक्षाएं बनाए रखें।",
        "important_note": "💡 **महत्वपूर्ण**: यह स्क्रीनिंग उपकरण साक्ष्य-आधारित जोखिम कारकों के आधार पर नेत्र देखभाल की तात्कालिकता निर्धारित करने में मदद करता है। रेटिना डिटैचमेंट का शीघ्र पता लगाना और उपचार दृष्टि को संरक्षित कर सकता है और अंधेपन को रोक सकता है।"
    }
}

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
    # Initialize form version for reset functionality
    if "form_version" not in st.session_state:
        st.session_state.form_version = 0
    
    # Check for reset flag and increment form version to reset all widgets
    if st.session_state.get("reset_form", False):
        st.session_state.form_version += 1
        st.session_state.reset_form = False
    
    # Create a key prefix based on form version - this resets all widgets when version changes
    v = st.session_state.form_version
    
    # Language Selector
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        language = st.selectbox("🌐", ["English", "Español", "हिंदी"], label_visibility="collapsed", key=f"language_select_{v}")
    
    t = TRANSLATIONS[language]
    
    # Header
    st.markdown(f"# {t['title']}")
    st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)
    
    # Disclaimer at the beginning of the app
    st.warning(t["disclaimer"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    points = 0
    emergency_override = False
    
    # Demographics Section
    st.markdown(f"## {t['section_a']}")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(t["age"], min_value=0, max_value=120, value=None, step=1, placeholder=t["age_placeholder"], key=f"age_{v}")
        if age is not None:
            if age >= 70:
                points += 3
            elif age >= 60:
                points += 2
            elif age >= 40:
                points += 1
    with col2:
        sex = st.radio(t["sex"], [t["female"], t["male"]], index=None, key=f"sex_{v}")
        if sex == t["male"]:
            points += 1
    
    # Eye History Section
    st.markdown(f"## {t['section_b']}")
    
    col1, col2 = st.columns(2)
    with col1:
        prior_rd = st.radio(t["prior_rd"], [t["no"], t["yes"]], index=None, key=f"prior_rd_{v}")
        if prior_rd == t["yes"]:
            points += 5
        
        cataract = st.radio(t["cataract"], [t["no"], t["yes"], t["not_sure"]], index=None, key=f"cataract_{v}")
        if cataract == t["yes"]:
            points += 2
        
        yag = st.radio(t["yag"], [t["no"], t["yes"], t["not_sure"]], index=None, key=f"yag_{v}")
        if yag == t["yes"]:
            points += 2
    
    with col2:
        myopia = st.radio(t["myopia"], [t["no"], t["yes"]], index=None, key=f"myopia_{v}")
        if myopia == t["yes"]:
            myopia_level = st.radio(t["myopia_level"], [t["myopia_none"], t["myopia_mild"], t["myopia_moderate"], t["myopia_high"], t["dont_know"]], index=None, key=f"myopia_level_{v}")
            if myopia_level == t["myopia_mild"]:
                points += 1
            elif myopia_level == t["myopia_moderate"]:
                points += 2
            elif myopia_level == t["myopia_high"]:
                points += 4
        
        retinal_condition = st.radio(t["retinal_condition"], [t["no"], t["yes"], t["not_sure"]], index=None, key=f"retinal_condition_{v}")
        if retinal_condition == t["yes"]:
            points += 4
        
        eye_trauma = st.radio(t["eye_trauma"], [t["no"], t["yes"]], index=None, key=f"eye_trauma_{v}")
        if eye_trauma == t["yes"]:
            points += 3
    
    # Systemic/Family History Section
    st.markdown(f"## {t['section_c']}")
    col1, col2 = st.columns(2)
    with col1:
        diabetes = st.radio(t["diabetes"], [t["no"], t["yes"], t["not_sure"]], index=None, key=f"diabetes_{v}")
        if diabetes == t["yes"]:
            points += 1
    with col2:
        family_history = st.radio(t["family_history"], [t["no"], t["yes"], t["not_sure"]], index=None, key=f"family_history_{v}")
        if family_history == t["yes"]:
            points += 3
    
    # Current Symptoms Section
    st.markdown(f"## {t['section_d']}")
    
    col1, col2 = st.columns(2)
    with col1:
        floaters = st.radio(t["floaters"], [t["no"], t["yes"]], index=None, key=f"floaters_{v}")
        if floaters == t["yes"]:
            points += 3
            floaters_onset = st.radio(t["floaters_onset"], [t["onset_more_48h"], t["onset_48h"]], key=f"floaters_onset_{v}", index=None)
            if floaters_onset == t["onset_48h"]:
                points += 1
        
        flashes = st.radio(t["flashes"], [t["flashes_none"], t["flashes_occasional"], t["flashes_frequent"]], index=None, key=f"flashes_{v}")
        if flashes == t["flashes_occasional"]:
            points += 2
            flashes_onset = st.radio(t["flashes_onset"], [t["onset_more_48h"], t["onset_48h"]], key=f"flashes_onset_{v}", index=None)
            if flashes_onset == t["onset_48h"]:
                points += 1
        elif flashes == t["flashes_frequent"]:
            points += 3
            flashes_onset = st.radio(t["flashes_onset"], [t["onset_more_48h"], t["onset_48h"]], key=f"flashes_onset2_{v}", index=None)
            if flashes_onset == t["onset_48h"]:
                points += 1
        
        shadow = st.radio(t["shadow"], [t["no"], t["yes"]], index=None, key=f"shadow_{v}")
        if shadow == t["yes"]:
            points += 8
            shadow_onset = st.radio(t["shadow_onset"], [t["onset_more_24h"], t["onset_24h"]], key=f"shadow_onset_{v}", index=None)
            if shadow_onset == t["onset_24h"]:
                points += 2
                emergency_override = True
    
    with col2:
        vision_decrease = st.radio(t["vision_decrease"], [t["no"], t["yes"]], index=None, key=f"vision_decrease_{v}")
        if vision_decrease == t["yes"]:
            points += 5
            vision_onset = st.radio(t["vision_onset"], [t["onset_more_24h"], t["onset_24h"]], key=f"vision_onset_{v}", index=None)
            if vision_onset == t["onset_24h"]:
                points += 2
                emergency_override = True
        
        pain = st.radio(t["pain"], [t["no"], t["yes"]], index=None, key=f"pain_{v}")
        if pain == t["yes"]:
            points += 1
    
    # Visual Function Section
    st.markdown(f"## {t['section_e']}")
    col1, col2 = st.columns(2)
    with col1:
        vision_level = st.radio(t["vision_level"], 
                               [t["vision_2020"], t["vision_2030"], t["vision_2080"], t["vision_worse"], t["dont_know"]], index=None, key=f"vision_level_{v}")
        if vision_level == t["vision_2030"]:
            points += 1
        elif vision_level == t["vision_2080"]:
            points += 2
        elif vision_level == t["vision_worse"]:
            points += 3
    with col2:
        last_exam = st.radio(t["last_exam"], 
                            [t["exam_within_2"], t["exam_more_2"], t["exam_never"]], index=None, key=f"last_exam_{v}")
        if last_exam == t["exam_more_2"]:
            points += 1
        elif last_exam == t["exam_never"]:
            points += 2
    
    # Lifestyle/Triggers Section
    st.markdown(f"## {t['section_f']}")
    recent_triggers = st.multiselect(t["triggers"], 
                                     [t["trigger_trauma"], t["trigger_sports"], 
                                      t["trigger_lifting"], 
                                      t["trigger_none"], t["not_sure"]], key=f"triggers_{v}")
    if t["trigger_trauma"] in recent_triggers or t["trigger_sports"] in recent_triggers:
        points += 3
    if t["trigger_lifting"] in recent_triggers:
        points += 1
    
    # Calculate Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Validation
    missing_fields = []
    if age is None:
        missing_fields.append(t["age"].replace(": *", ""))
    if sex is None:
        missing_fields.append(t["sex"].replace(": *", ""))
    if prior_rd is None:
        missing_fields.append(t["prior_rd"].replace("? *", ""))
    if cataract is None:
        missing_fields.append(t["cataract"].replace("? *", ""))
    if yag is None:
        missing_fields.append(t["yag"].replace("? *", ""))
    if myopia is None:
        missing_fields.append(t["myopia"].replace("? *", ""))
    if myopia == t["yes"] and myopia_level is None:
        missing_fields.append(t["myopia_level"].replace(": *", ""))
    if retinal_condition is None:
        missing_fields.append(t["retinal_condition"].replace("? *", ""))
    if eye_trauma is None:
        missing_fields.append(t["eye_trauma"].replace("? *", ""))
    if diabetes is None:
        missing_fields.append(t["diabetes"].replace("? *", ""))
    if family_history is None:
        missing_fields.append(t["family_history"].replace("? *", ""))
    if floaters is None:
        missing_fields.append(t["floaters"].replace("? *", ""))
    if floaters == t["yes"] and floaters_onset is None:
        missing_fields.append(t["floaters_onset"].replace(": *", ""))
    if flashes is None:
        missing_fields.append(t["flashes"].replace("? *", ""))
    if flashes in [t["flashes_occasional"], t["flashes_frequent"]] and flashes_onset is None:
        missing_fields.append(t["flashes_onset"].replace(": *", ""))
    if shadow is None:
        missing_fields.append(t["shadow"].replace("? *", ""))
    if shadow == t["yes"] and shadow_onset is None:
        missing_fields.append(t["shadow_onset"].replace("? *", ""))
    if vision_decrease is None:
        missing_fields.append(t["vision_decrease"].replace("? *", ""))
    if vision_decrease == t["yes"] and vision_onset is None:
        missing_fields.append(t["vision_onset"].replace(": *", ""))
    if pain is None:
        missing_fields.append(t["pain"].replace("? *", ""))
    if vision_level is None:
        missing_fields.append(t["vision_level"].replace(": *", ""))
    if last_exam is None:
        missing_fields.append(t["last_exam"].replace(": *", ""))
    if len(recent_triggers) == 0:
        missing_fields.append(t["triggers"].replace(": *", ""))
    
    @st.dialog(t["results_title"], width="large")
    def show_results(points, percentage, emergency_override):
        # Metrics
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric(t["risk_percentage"], f"{percentage:.1f}%")
        with col2:
            if emergency_override or points >= 15:
                risk_tier = t["very_high"]
            elif points >= 10:
                risk_tier = t["high"]
            elif points >= 5:
                risk_tier = t["moderate"]
            else:
                risk_tier = t["low"]
            st.metric(t["risk_tier"], risk_tier)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Risk Assessment and Recommendations
        if emergency_override or points >= 15:
            st.error(f"### {t['very_high_title']}")
            st.markdown(f"""
            <div style='background-color: #fee2e2; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #dc2626;'>
                <h4 style='color: #991b1b; margin-top: 0;'>{t['very_high_msg']}</h4>
                <p style='color: #7f1d1d; font-size: 1.1rem; font-weight: 600;'>
                {t['very_high_action']}
                </p>
                <p style='color: #7f1d1d;'>
                {t['very_high_detail']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif points >= 10:
            st.warning(f"### {t['high_title']}")
            st.markdown(f"""
            <div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #f59e0b;'>
                <h4 style='color: #92400e; margin-top: 0;'>{t['high_msg']} ({percentage:.1f}%)</h4>
                <p style='color: #78350f; font-size: 1.1rem; font-weight: 600;'>
                {t['high_action']}
                </p>
                <p style='color: #78350f;'>
                {t['high_detail']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif points >= 5:
            st.info(f"### {t['moderate_title']}")
            st.markdown(f"""
            <div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #3b82f6;'>
                <h4 style='color: #1e40af; margin-top: 0;'>{t['moderate_msg']} ({percentage:.1f}%)</h4>
                <p style='color: #1e3a8a; font-size: 1.1rem; font-weight: 600;'>
                {t['moderate_action']}
                </p>
                <p style='color: #1e3a8a;'>
                {t['moderate_detail']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"### {t['low_title']}")
            st.markdown(f"""
            <div style='background-color: #d1fae5; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #10b981;'>
                <h4 style='color: #065f46; margin-top: 0;'>{t['low_msg']} ({percentage:.1f}%)</h4>
                <p style='color: #064e3b; font-size: 1.1rem; font-weight: 600;'>
                {t['low_action']}
                </p>
                <p style='color: #064e3b;'>
                {t['low_detail']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Important Note
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(t["important_note"])
        
        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t["reset_btn"], type="secondary", use_container_width=True):
            # Set reset flag and rerun to clear form
            st.session_state["reset_form"] = True
            st.rerun()
    
    if st.button(t["calculate_btn"], type="primary"):
        if missing_fields:
            st.error(f"{t['missing_fields']} {', '.join(missing_fields)}")
        else:
            # Increment the assessment counter
            increment_counter()
            percentage = calculate_percentage(points)
            show_results(points, percentage, emergency_override)
    
    # Hidden admin view - only accessible via URL parameter ?admin=retina2024
    query_params = st.query_params
    if query_params.get("admin") == "retina2024":
        st.markdown("---")
        st.markdown("### 🔐 Admin View (Hidden)")
        counter_value = get_counter()
        st.metric("Total Assessments Completed", counter_value)

if __name__ == "__main__":
    main()
