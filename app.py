import streamlit as st
import joblib
import sqlite3
from datetime import datetime
import pandas as pd

# ---------- MODEL ----------
model = joblib.load("model.pkl")

# ---------- DB ----------
conn = sqlite3.connect("history.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    result TEXT,
    confidence REAL,
    time TEXT
)
""")
conn.commit()

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Spam Dashboard", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #f4f7fb; }

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #1f4e79;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR NAVIGATION (IMPROVED) ----------
st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📜 History", "📊 Analytics"]
)

# =====================================================
# 🏠 HOME
# =====================================================
if menu == "🏠 Home":

    st.markdown("<div class='title'>📧 Spam Email Detector</div>", unsafe_allow_html=True)

    email = st.text_area("Enter Email Text", height=150)

    if st.button("🚀 Predict Spam"):
        if email.strip():

            pred = model.predict([email])[0]
            prob = model.predict_proba([email])[0]
            confidence = max(prob) * 100

            result = "SPAM" if pred == 1 else "NOT SPAM"

            c.execute(
                "INSERT INTO history (email, result, confidence, time) VALUES (?, ?, ?, ?)",
                (email, result, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

            if pred == 1:
                st.error(f"🚨 SPAM DETECTED ({confidence:.2f}%)")
            else:
                st.success(f"✅ NOT SPAM ({confidence:.2f}%)")

        else:
            st.warning("Please enter email text")

# =====================================================
# 📜 HISTORY (TABLE FORMAT)
# =====================================================
elif menu == "📜 History":

    st.markdown("<div class='title'>📜 Prediction History</div>", unsafe_allow_html=True)

    # ---------- CLEAR ALL ----------
    if st.button("🗑 Clear All History"):
        c.execute("DELETE FROM history")
        conn.commit()
        st.success("All history deleted!")
        st.rerun()

    # ---------- FETCH ----------
    rows = c.execute("""
        SELECT id, email, result, confidence, time
        FROM history
    """).fetchall()

    if len(rows) == 0:
        st.info("No history available")

    else:

        # ---------- TABLE HEADER ----------
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

        with col1:
            st.markdown("**Email**")
        with col2:
            st.markdown("**Result**")
        with col3:
            st.markdown("**Confidence**")
        with col4:
            st.markdown("**Time**")
        with col5:
            st.markdown("**Action**")

        st.markdown("---")

        # ---------- ROWS ----------
        for row in rows:
            id_, email, result, confidence, time = row

            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

            with col1:
                st.write(email[:40] + "..." if len(email) > 40 else email)

            with col2:
                st.write(result)

            with col3:
                st.write(f"{confidence:.2f}%")

            with col4:
                st.write(time)

            with col5:
                if st.button("🗑", key=f"del_{id_}"):
                    c.execute("DELETE FROM history WHERE id = ?", (id_,))
                    conn.commit()
                    st.rerun()
# =====================================================
# 📊 ANALYTICS
# =====================================================
elif menu == "📊 Analytics":

    st.markdown("<div class='title'>📊 Analytics Dashboard</div>", unsafe_allow_html=True)

    rows = c.execute("SELECT result, confidence FROM history").fetchall()

    if len(rows) == 0:
        st.info("No data available")

    else:

        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame(rows, columns=["result", "confidence"])

        spam_count = len(df[df["result"] == "SPAM"])
        safe_count = len(df[df["result"] == "NOT SPAM"])
        total = len(df)

        # ---------- SUMMARY ----------
        st.write("### 📌 Summary")
        st.write("Total Emails:", total)
        st.write("Spam Emails:", spam_count)
        st.write("Safe Emails:", safe_count)

        st.markdown("---")

        # =====================================================
        # 🟢 TOP ROW (SIDE BY SIDE SMALL CHARTS)
        # =====================================================
        col1, col2 = st.columns(2)

        # ---------- PIE CHART ----------
        with col1:
            st.write("### 🥧 Spam Ratio")

            fig1, ax1 = plt.subplots(figsize=(3, 3))
            ax1.pie(
                [spam_count, safe_count],
                labels=["Spam", "Not Spam"],
                autopct="%1.0f%%",
                colors=["red", "green"]
            )
            ax1.axis("equal")

            st.pyplot(fig1)

        # ---------- BAR CHART ----------
        with col2:
            st.write("### 📊 Count")

            fig2, ax2 = plt.subplots(figsize=(3, 3))
            ax2.bar(
                ["Spam", "Safe"],
                [spam_count, safe_count],
                color=["red", "green"]
            )

            ax2.set_ylabel("Emails")

            st.pyplot(fig2)

        # =====================================================
        # 🔵 BOTTOM ROW (LARGE CONFIDENCE CHART)
        # =====================================================
        st.markdown("---")

        st.write("### 📈 Confidence Levels (Detailed View)")

        fig3, ax3 = plt.subplots(figsize=(8, 3))

        ax3.plot(df["confidence"], marker='o', color="#1f4e79")

        ax3.set_ylabel("Confidence %")
        ax3.set_xlabel("Email Index")

        st.pyplot(fig3)