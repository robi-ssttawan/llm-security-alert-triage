import json
from g4f.client import Client

client = Client()

raw_log = "2026-07-30 01:15:22 WARNING AuthFailed user=admin src_ip=192.168.1.50 count=150 attempt_failed"

# Prompt memaksa AI mengembalikan JSON murni
prompt = f"""
Kamu adalah seorang Analis Senior SOC (Security Operations Center).
Analisis log keamanan berikut dan kembalikan hasilnya HANYA dalam format JSON valid (tanpa teks ekstra/penjelasan lain).

Log Mentah:
{raw_log}

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

print("Sedang memproses log ke format JSON...\n")

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.choices[0].message.content.strip()
    
    # Membersihkan jika AI menyertakan markdown ```json ... ```
    if result_text.startswith("```"):
        result_text = result_text.split("\n", 1)[1]
        result_text = result_text.rsplit("\n", 1)[0]
        if result_text.startswith("json"):
            result_text = result_text[4:].strip()

    # Parsing teks dari AI menjadi objek JSON/Dictionary Python
    data = json.loads(result_text)

    print("=== HASIL JSON TRIAGE (SUCCESS) ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Bukti bahwa ini sudah jadi data JSON terstruktur
    print("\n--- Akses Data Spesifik ---")
    print(f"Severity Level : {data['severity']}")
    print(f"MITRE ID       : {data['mitre_technique_id']} ({data['mitre_technique_name']})")

except Exception as e:
    print("Terjadi error:", e)