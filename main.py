import streamlit as st
import requests
import json

st.set_page_config(page_title="RayBot L1 Dashboard", layout="wide")

# Hardcoded Supabase config
SUPABASE_URL = "https://jubcotqsbvguwzklngzd.supabase.co"
FUNCTION_URL = f"{SUPABASE_URL}/functions/v1/raybot-inference"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1YmNvdHFzYnZndXd6a2xuZ3pkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1NDIwNzAsImV4cCI6MjA3NTExODA3MH0.r1yz9l6pqZ1AfOIRRd2micoeLTnhE84S5ksuQTg4WC4"

st.title("🚀 RayBot L1 Manual Inference")
st.markdown("**Click below to trigger live Gold signal → Telegram**")

# Sidebar controls
st.sidebar.header("Inference Settings")
days = st.sidebar.slider("Days of data", 30, 730, 365)
interval = st.sidebar.selectbox("Interval", ["1h", "1d", "30m"])
account_balance = st.sidebar.number_input("Account balance", 1000, 100000, 10000)
risk_pct = st.sidebar.slider("Risk %", 0.1, 5.0, 2.0)

if st.button("🔥 TRIGGER INFERENCE → TELEGRAM", type="primary", use_container_width=True):
    with st.spinner("Running RayBot L1 inference..."):
        headers = {
            "Authorization": f"Bearer {ANON_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"days": days, "interval": interval, "account_balance": account_balance, "risk_pct": risk_pct}
        
        try:
            response = requests.post(FUNCTION_URL, headers=headers, json=payload, timeout=30)
            result = response.json()
            
            if result.get("status") == "success":
                st.success(f"✅ **{result['signal']} SIGNAL SENT TO TELEGRAM!**")
                st.balloons()
                st.metric("Probability", f"{result['probability']*100:.1f}%")
                st.caption("Check your Telegram private channel!")
            elif result.get("status") == "neutral":
                st.info("ℹ️ NEUTRAL signal - No Telegram alert sent")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown')}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

# Status info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Timeout", "30s")
with col2:
    st.metric("Edge Function", "raybot-inference")
with col3:
    st.metric("Status", "🟢 LIVE")

st.markdown("---")
st.markdown("**Cron Jobs Running:**")
st.markdown("- 00:00 UTC weekdays (Asian open)")
st.markdown("- Every 5min signals")
