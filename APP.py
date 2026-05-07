import streamlit as st
import pandas as pd
import joblib

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Customer AI Dashboard", layout="wide")

# ADD CSS HERE (RIGHT PLACE)

st.markdown("""
<style>



/* Keep header but make it clean */
header {
    background: transparent !important;
}

/* Position toggle button */
button[kind="header"] {
    position: fixed !important;
    top: 70px !important;
    left: 15px !important;
    z-index: 9999 !important;

    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 6px !important;
}

/* Hover */
button[kind="header"]:hover {
    background: rgba(255,255,255,0.2) !important;
}

/* Icon */
button[kind="header"] svg {
    fill: white !important;
}



/* ===== MAIN BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background-color: #000000;
}

/* ===== FORCE ALL TEXT WHITE ===== */
body, h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: white !important;
}

/* ===== SIDEBAR DARK ===== */
[data-testid="stSidebar"] {
    background-color: #0a0a0a;
}

/* ===== NEON PINK INPUT FIELDS ===== */
input, select {
    background-color: rgba(255, 20, 147, 0.10) !important;  /* 💖 10% neon pink */
    color: white !important;
    border-radius: 10px !important;

    border: 1px solid rgba(255, 20, 147, 0.4) !important;

    box-shadow: 0 0 8px rgba(255, 20, 147, 0.5);  /* glow effect */
}

/* ===== HOVER GLOW ===== */
input:focus, select:focus {
    outline: none !important;
    border: 1px solid rgba(255, 20, 147, 0.9) !important;
    box-shadow: 0 0 12px rgba(255, 20, 147, 0.9);
}


/* ===== METRIC CARDS (GLASS EFFECT) ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.10);
    border-radius: 12px;
    padding: 15px;
    backdrop-filter: blur(6px);
}

/* ===== EXPANDER / CUSTOMER DETAILS ===== */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.10);
    border-radius: 12px;
    backdrop-filter: blur(6px);
}

/* ===== ALERTS (keep readable for Smart Decision Engine) ===== */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.08);
    color: white !important;
    border-radius: 10px;
}

/* ===== BUTTON ===== */
button {
    background-color: rgba(255,255,255,0.10) !important;
    color: white !important;
    border-radius: 8px !important;
}

.round-gif {
    width: 120px;
    height: 120px;
    overflow: hidden;
    border-radius: 16px;
}

.round-gif img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: scale(1.3);   /* zoom */
}


</style>
""", unsafe_allow_html=True)



# =========================
# LOAD DATA + MODEL
# =========================
df = pd.read_csv("final_full_dataset.csv")
model = joblib.load("GradientBoostingRegressor.pkl")

# =========================
# 🎨 CUSTOM STYLE (PREMIUM UI)
# =========================
st.markdown("""
<style>
.metric-card {
    padding: 15px;
    border-radius: 12px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: black;
    text-align: center;
}
.risk-low {color: green; font-weight: bold;}
.risk-medium {color: orange; font-weight: bold;}
.risk-high {color: red; font-weight: bold;}

</style>
""", unsafe_allow_html=True)

# =========================
# 🚀 TITLE
# =========================
# st.title("🚀 Customer Intelligence AI Platform")

col1, col2 = st.columns([1,6])

with col1:
    st.markdown("""
    <div class="round-gif">
        <img src="https://i.pinimg.com/originals/dd/50/b6/dd50b6932dfd6ff35c020c63f7e1213f.gif">
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.title("Customer Intelligence AI Platform")

# =========================
# 🎯 LAYER 1: INPUT SEARCH
# =========================
st.sidebar.header("🔍 Search Customer")

user_id = st.sidebar.text_input("🆔 User ID")
name = st.sidebar.text_input("👤 Name")
email = st.sidebar.text_input("📧 Email ID")
location = st.sidebar.selectbox("📍 Location", ["All"] + sorted(df["location"].unique()))

# 🔘 PREDICT BUTTON
predict_btn = st.sidebar.button("🚀 Predict Customer")

# FILTER
filtered_df = df.copy()

if user_id:
        filtered_df = filtered_df[filtered_df["user_id"].astype(str) == user_id]

if email:
    filtered_df = filtered_df[filtered_df["email_address"] == email]

if name:
    filtered_df = filtered_df[filtered_df["name"].str.contains(name, case=False)]

if location != "All":
    filtered_df = filtered_df[filtered_df["location"] == location]

# =========================
# RESULT
# =========================
if len(filtered_df) == 0:
    st.warning("❌ No customer found")
    st.stop()

customer = filtered_df.iloc[0]

st.success(f"✅ Customer Found: {customer['name']}")

# Clean column names
df.columns = df.columns.str.strip()

if predict_btn:

    if len(filtered_df) == 0:
        st.warning("❌ No customer found")
        st.stop()

    customer = filtered_df.iloc[0]

    st.success(f"✅ Customer Found: {customer.get('name', 'Unknown')}")
    
    # =========================
# 📅 TENURE + EXPIRY LOGIC
# =========================
import pandas as pd

today = pd.Timestamp.today()

# Convert dates safely
start_date = pd.to_datetime(customer.get('membership_start_date'), errors='coerce')
end_date = pd.to_datetime(customer.get('membership_end_date'), errors='coerce')

today = pd.Timestamp.today()

# ---- Tenure ----
if pd.notnull(start_date):
    tenure_days = (today - start_date).days   # ✅ fix
    
    years = tenure_days // 365
    months = (tenure_days % 365) // 30

    tenure_display = f"{years}y {months}m"
else:
    tenure_display = "N/A"

# ---- Expiry ----
if pd.notnull(end_date):
    days_remaining = (end_date - today).days

    if days_remaining < 0:
        expiry_display = f"Expired {abs(days_remaining)} days ago"
    else:
        expiry_display = f"{days_remaining} days remaining"
else:
    expiry_display = "N/A"
    
# =========================
# 📅 TENURE (PLAN BASED)
# =========================

plan = customer.get('subscription_plan', 'Unknown')

if pd.notnull(start_date):

    tenure_days = (today - start_date).days

    if plan == "Annual":
        years = tenure_days // 365
        months = (tenure_days % 365) // 30
        tenure_display = f"{years}y {months}m"

    elif plan == "Monthly":
        months = tenure_days // 30
        days = tenure_days % 30
        tenure_display = f"{months}m {days}d"

    else:
        # fallback
        tenure_display = f"{tenure_days} days"

else:
    tenure_display = "N/A"

# =========================
# 🎯 LAYER 2: POPUP DASHBOARD
# =========================
with st.expander("📊 View Customer Intelligence Dashboard", expanded=True):

    st.markdown("## 🧠 Customer Profile Overview")

    # =========================
    # KPI CARDS
    # =========================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📊 Churn Probability", f"{customer['churn_probability']*100:.2f}%")
    col2.metric("⚠️ Risk Level", customer["risk_level"])
    col3.metric("💎 Loyalty Score", round(customer["loyalty_score"], 3))
    col4.metric("📅 Tenure", tenure_display)
    col5.metric("Loyalty Segment", customer['loyalty_segment'])

    # =========================
    # RISK GAUGE
    # =========================
    prob = customer["churn_probability"]

    st.markdown("### 🎯 Risk Gauge")
    st.progress(int(prob * 100))

    if prob < 0.3:
        st.success("🟢 Low Risk")
    elif prob < 0.7:
        st.warning("🟡 Medium Risk")
    elif prob < 0.9:
        st.error("🟠 High Risk")
    else:
        st.error("🔴 Critical Risk")

    st.markdown("---")
    # =========================
    # 🧾 CUSTOMER BASIC INFO
    # =========================

    st.subheader("👤 Customer Overview")

    colA, colB, colC = st.columns(3)

    with colA:
        st.write(f"🆔 User ID: {customer['user_id']}")

    with colB:
        st.write(f"👤 Name: {customer['name']}")
  
    with colC:
        st.write(f"📧 Email: {customer['email_address']}")
        
    st.markdown("---")
        
    # =========================
    # PROFILE DETAILS
    # =========================
     
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👤 Personal Info")
        st.write(f"Gender: {customer['gender']}")
        st.write(f"Location: {customer['location']}")
        st.write(f"Age: {customer['age']}")
        st.write(f"Start: {customer['membership_start_date']}")
        st.write(f"End: {customer['membership_end_date']}")

    with col2:
        st.subheader("📦 Subscription")

        st.write(f"Plan: {customer['subscription_plan']}")
        st.write(f"Renewal: {customer['renewal_status']}")
        st.write(f"Monthly User: {customer['monthly_user']}")
        # st.write(f"Expiring Soon: {customer['is_expiring_soon']}")
        
        flag = customer.get('is_expiring_soon', 0)

        expiring_text = "Yes" if flag == 1 else "No"

        st.write(f"Expiring Soon: {expiring_text}")

    
    with col3:
        st.subheader("📱 Usage")
        st.write(f"Devices: {customer['devices_used']}")
        st.write(f"Usage: {customer['usage_frequency']}")
        st.write(f"Engagement: {customer['engagement_metrics']}")
        st.write(f"Score: {round(customer['engagement_score'], 3)}")

    st.markdown("---")

    # =========================
    # BEHAVIOR
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📉 Engagement")
        st.write(f"Drop: {round(customer['engagement_drop'], 4)}")
        st.write(f"Low Engagement: {customer['low_engagement']}")
        st.write(f"Per Day: {round(customer['engagement_per_day'], 4)}")

    with col2:
        st.subheader("📞 Support")
        st.write(f"Interactions: {customer['customer_support_interactions']}")
        st.write(f"High Support: {customer['high_support']}")
        st.write(f"Ratio: {round(customer['support_vs_engagement'], 4)}")

    with col3:
        st.subheader("⭐ Feedback")
        st.write(f"Rating: {customer['feedback_ratings']}")
        st.write(f"Bucket: {customer['feedback_bucket']}")
        st.write(f"Score: {round(customer['norm_feedback'], 3)}")

    st.markdown("---")

    # =========================
    # MODEL OUTPUT
    # =========================
    st.subheader("🤖 AI Prediction")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Predicted Churn: {customer['predicted_churn']}")
        st.write(f"Probability: {customer['predicted_churn_prob']:.3f}")
        st.write(f"Loyalty Segment: {customer['loyalty_segment']}")
        st.write(f"Risk of leaving Plateform: {customer['risk_level']}")

    with col2:
        st.write(f"Behavior Score: {round(customer['behavior_score'], 3)}")
        # st.write(f"Expiry Urgency: {customer['expiry_urgency']}")
        st.write(f"New Customer: {customer['new_customer']}")

    st.markdown("---")

    # =========================
# 🎯 SMART DECISION ENGINE
# =========================
st.subheader("🎯 Smart Decision Engine")

loyalty_percent = customer["loyalty_score"] * 100
churn_percent = customer["churn_probability"] * 100
feedback = customer["feedback_ratings"]
genre = customer["favorite_genres"]
plan = customer["subscription_plan"]
purchase = customer["purchase_history"]

# =========================
# 🔥 RULE ENGINE
# =========================
decision_reason = []

if churn_percent > 70 and feedback < 3:
    st.error("🚨 Critical Customer")

    st.markdown("### 🛠 Retention Strategy")
    st.warning(customer["biz_retention_strategy"])

    st.markdown("### 🎁 Special Offer")
    st.info("Heavy discount + priority support")

    decision_reason.append(f"High churn ({churn_percent:.1f}%)")
    decision_reason.append(f"Low feedback ({feedback})")

elif churn_percent > 70:
    st.error("⚠️ High Churn Risk")

    st.markdown("### 🛠 Retention Strategy")
    st.warning(customer["biz_retention_strategy"])

    decision_reason.append(f"High churn ({churn_percent:.1f}%)")

# =========================
# 🎯 LOW LOYALTY → PROMOTION
# =========================
elif loyalty_percent < 30:
    st.info("🎁 Low Loyalty Customer")

    st.markdown("### 🎯 Promotion Strategy")

    if plan == "Basic":
        st.success("Offer Premium Upgrade")
        decision_reason.append("User on Basic plan")

    elif genre in ["Action", "Sci-Fi", "Drama"]:
        st.success(f"Promote {genre} premium content")
        decision_reason.append(f"User prefers {genre}")

    else:
        st.success("Send personalized offers")
        decision_reason.append("Low loyalty behavior")

# =========================
# 💎 LOYAL CUSTOMER → CROSS SELL
# =========================
elif loyalty_percent > 70:
    st.success("💎 Loyal Customer")

    st.markdown("### 🔁 Cross Recommendation")

    recs = []
    reasons = []

    if plan == "Monthly":
        recs.append("Upgrade to Annual Plan")
        reasons.append("Monthly plan → Annual saves cost")

    if genre in ["Drama", "Comedy", "Action", "Sci-Fi"]:
        recs.append(f"Recommend {genre} premium bundle")
        reasons.append(f"User likes {genre}")

    if purchase == "Electronics":
        recs.append("Bundle with device streaming plan")
        reasons.append("User buys electronics → multi-device usage")

    if purchase == "Books":
        recs.append("Recommend audiobook combo")
        reasons.append("User prefers books")

    if not recs:
        recs.append("Recommend trending content")
        reasons.append("Fallback recommendation")

    for r, reason in zip(recs, reasons):
        st.info(r)
        st.caption(f"👉 Why: {reason}")

    decision_reason.append("High loyalty → upsell/cross-sell")
    
else:
    st.success("✅ Stable Customer")
    st.markdown("### 🌱 Growth Strategy")
    st.info("Upsell + recommend popular content")

    decision_reason.append("Balanced customer")

# =========================
# ⭐ LOW FEEDBACK → IMPROVE
# =========================
st.markdown("### ⭐ Feedback Insight")

if feedback < 4:
    st.warning("Low Feedback Customer")
    st.info("Improve service + follow-up")

    decision_reason.append(f"Low feedback ({feedback})")
else:
    st.success("Good Feedback")
    
# =========================
# 🌱 DEFAULT → GROWTH
# =========================
st.markdown("### 🌱 Additional Growth Opportunity")

if churn_percent < 50 and loyalty_percent < 70:
    st.info("Recommend engagement campaigns")

elif loyalty_percent > 70:
    st.info("Upsell premium features / bundles")

elif churn_percent > 70:
    st.warning("Focus on retention before growth")

else:
    st.info("Maintain engagement and monitor behavior")

# =========================
# 🧠 WHY THIS DECISION
# =========================
st.markdown("### 🧠 Why this decision?")

for reason in decision_reason:
    st.caption(f"👉 {reason}")