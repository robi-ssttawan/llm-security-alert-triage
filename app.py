import streamlit as st
import json
from g4f.client import Client

# Config Halaman Web
st.set_page_config(
    page_title="LLM Security Alert Triage",
    page_icon="🛡️",
    layout="wide"
)

# Header Utama
st.title("🛡️ LLM-Powered Security Alert Triage System")
st.caption("Automated SOC Log Analysis with AI & MITRE ATT&CK Mapping")
st.markdown("---")

# Sidebar - Contoh Log Siap Pakai
st.sidebar.header("📋 Sample Log Prompts")
sample_logs = {
    "SSH Brute Force": "2026-07-30 01:15:22 WARNING AuthFailed user=admin src_ip=192.168.1.50 count=150 attempt_failed",
    "SQL Injection Attack": "2026-07-30 03:22:10 ERROR WebServer GET /product?id=1' UNION SELECT username, password FROM users-- src_ip=45.33.21.9",
    "Phishing Suspicious Executable": "2026-07-30 08:45:00 ALERT EndpointProtection File payload.exe downloaded from http://malicious-domain.com/login.php user=johndoe",
    "Valid Account Anomaly": "2026-07-30 11:05:00 WARNING VPN login successful user=ceo_alice src_ip=185.220.101.5 (Location: Russia) prior_ip=110.12.5.1 (Location: Indonesia)"
}

selected_sample = st.sidebar.selectbox("Pilih Contoh Log buat Coba-coba:", list(sample_logs.keys()))

# Input Log dari User
default_log = sample_logs[selected_sample]
user_log = st.text_area("📥 Masukkan Raw Security Log:", value=default_log, height=100)

# Inisialisasi AI Client
client = Client()

# Tombol Eksekusi Triage
if st.button("🚀 Analisis Log Sekarang", type="primary"):
    if not user_log.strip():
        st.warning("Harap masukkan teks log terlebih dahulu!")
    else:
        with st.spinner("AI sedang menganalisis log dan memetakan ke MITRE ATT&CK..."):
            prompt = f"""
            Kamu adalah seorang Analis Senior SOC (Security Operations Center).
            Analisis log keamanan berikut dan kembalikan hasilnya HANYA dalam format JSON valid (tanpa teks ekstra/penjelasan lain).

            Log Mentah:
            {user_log}

            Format JSON wajib seperti ini:
            {{
              "summary": "penjelasan singkat masalah",
              "severity": "Low/Medium/High/Critical",
              "mitre_technique_id": "ID teknik misal T1110",
              "mitre_technique_name": "Nama teknik misal Brute Force",
              "actionable_recommendations": [
                "rekomendasi 1",
                "rekomendasi 2"
              ]
            }}
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                result_text = response.choices[0].message.content.strip()

                # Cleaning markdown
                if result_text.startswith("```"):
                    result_text = result_text.split("\n", 1)[1]
                    result_text = result_text.rsplit("\n", 1)[0]
                    if result_text.startswith("json"):
                        result_text = result_text[4:].strip()

                data = json.loads(result_text)

                # --- TAMPILAN HASIL ANALISIS DIBAGI KEDALAM KOTAK-KOTAK KEREN ---
                st.success("✅ Analisis Berhasil Selesai!")
                
                col1, col2, col3 = st.columns(3)
                
                # Badge Severity Warna-warni
                severity = data.get("severity", "Medium")
                if severity in ["Critical", "High"]:
                    col1.error(f"**Severity:** {severity}")
                elif severity == "Medium":
                    col1.warning(f"**Severity:** {severity}")
                else:
                    col1.info(f"**Severity:** {severity}")

                col2.metric("MITRE Technique ID", data.get("mitre_technique_id", "N/A"))
                col3.metric("Technique Name", data.get("mitre_technique_name", "N/A"))

                st.subheader("📌 Ringkasan Insiden")
                st.info(data.get("summary", "-"))

                st.subheader("💡 Rekomendasi Tindakan (Actionable Advice)")
                for idx, rec in enumerate(data.get("actionable_recommendations", []), 1):
                    st.write(f"**{idx}.** {rec}")

                # JSON Raw Expander
                with st.expander("🔍 Lihat Raw JSON Response"):
                    st.json(data)

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses log: {e}")