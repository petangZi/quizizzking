# REDZ QUIZIZZ NOTIFBOT 🔥 v1.0 Termux Edition (Tanpa Admin Link)
# 📲 Manual click, bot bantu strategi dan jawaban lewat notifikasi
# Dibuat oleh: REDZBOT HACKDIVISION

import os
import time
import requests

# === MASUKKAN QUIZ ID JOIN (BUKAN ADMIN) ===
QUIZ_ID = input("🧠 Masukkan Quiz ID Join (bukan link admin): ")

# === NOTIFIKASI TERMUX ===
def kirim_notif(judul, konten):
    try:
        os.system(f'termux-notification -t "{judul}" -c "{konten}"')
    except Exception as e:
        print("[ERROR Notif]", e)

# === AMBIL QUIZ VIA QUIZIZZ REST (TRICK TANPA ADMIN) ===
def ambil_data_via_shortcut(quiz_id):
    try:
        url = f"https://quizizz.com/_api/main/join/shortLink/{quiz_id}"
        res = requests.get(url)
        res.raise_for_status()
        info = res.json()

        real_id = info['data']['quiz']['_id']
        nama_quiz = info['data']['quiz']['name']

        print(f"\n🔥 Quiz terdeteksi: {nama_quiz} (ID: {real_id})")

        soal_url = f"https://quizizz.com/_api/main/quiz/{real_id}"
        res2 = requests.get(soal_url)
        res2.raise_for_status()
        data = res2.json()

        return data["data"]["questions"]

    except Exception as e:
        print("❌ Gagal ambil soal:", e)
        return []

# === LOGIKA STRATEGI & JAWABAN ===
def logic_soal(questions):
    for idx, q in enumerate(questions):
        soal = q['structure']['query']
        opsi = q['structure']['options']
        jawaban_benar = []
        list_opsi = []

        for o in opsi:
            teks = o['text'].replace("\n", " ").strip()
            if o.get('isCorrect'): jawaban_benar.append(teks)
            list_opsi.append(f"{'✅' if o.get('isCorrect') else '❌'} {teks}")

        strategi = "Serang langsung!" if any("serang" in x.lower() for x in jawaban_benar) else "Main aman dulu 🛡️"

        teks_notif = f"🧠 {soal}\n\n{chr(10).join(list_opsi)}\n\n🎯 Jawaban: {', '.join(jawaban_benar)}\n💡 Strategi: {strategi}"
        kirim_notif(f"Soal #{idx+1}", teks_notif)
        print(f"\n[#{idx+1}] {soal}\nJawaban: {', '.join(jawaban_benar)} | Strategi: {strategi}")
        time.sleep(1.2)

# === MAIN ===
def main():
    print("\n📲 REDZBOT NOTIF-SOLVER v1.0 AKTIF 🔥")
    questions = ambil_data_via_shortcut(QUIZ_ID)
    if questions:
        logic_soal(questions)
    else:
        print("⚠️ Tidak ditemukan soal dari ID tersebut.")

if __name__ == "__main__":
    main()
