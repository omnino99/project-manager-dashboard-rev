import streamlit as st
import json
import os

DATA_FILE = "project_data.json"

# Inisialisasi data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

st.set_page_config(page_title="Dashboard Proyek", layout="wide")
st.title("📊 Dashboard Manajemen Proyek")

menu = st.sidebar.selectbox("Menu", ["📁 Ringkasan", "➕ Tambah Proyek", "📝 Tambah Tugas"])

data = load_data()

# 1. Ringkasan
if menu == "📁 Ringkasan":
    if not data:
        st.warning("Belum ada proyek.")
    else:
        for name, project in data.items():
            st.subheader(f"📌 Proyek: {name}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Anggaran", f"Rp{project['budget']:,}")
            col2.metric("Terpakai", f"Rp{project['expenses']:,}")
            sisa = project['budget'] - project['expenses']
            col3.metric("Sisa Dana", f"Rp{sisa:,}", delta=f"-Rp{project['expenses']:,}")

            if project['tasks']:
                total_progress = sum(t['progress'] for t in project['tasks']) / len(project['tasks'])
                st.progress(total_progress / 100)
                st.caption(f"Progress rata-rata: {total_progress:.2f}%")
                with st.expander("📋 Lihat Daftar Tugas"):
                    for task in project['tasks']:
                        st.write(f"- **{task['task']}** | 💸 Rp{task['cost']:,} | 📈 {task['progress']}%")
            else:
                st.info("Belum ada tugas dalam proyek ini.")

# 2. Tambah Proyek
elif menu == "➕ Tambah Proyek":
    st.subheader("➕ Tambahkan Proyek Baru")
    name = st.text_input("Nama Proyek")
    budget = st.number_input("Anggaran Proyek (Rp)", min_value=0)
    if st.button("Simpan Proyek"):
        if name and budget > 0:
            if name in data:
                st.error("Proyek sudah ada.")
            else:
                data[name] = {"budget": budget, "expenses": 0, "tasks": []}
                save_data(data)
                st.success(f"Proyek '{name}' ditambahkan.")
        else:
            st.warning("Isi nama dan anggaran dengan benar.")

# 3. Tambah Tugas
elif menu == "📝 Tambah Tugas":
    st.subheader("📝 Tambahkan Tugas ke Proyek")
    if not data:
        st.warning("Belum ada proyek.")
    else:
        project_name = st.selectbox("Pilih Proyek", list(data.keys()))
        task_name = st.text_input("Nama Tugas")
        cost = st.number_input("Biaya Tugas (Rp)", min_value=0)
        progress = st.slider("Progress (%)", 0, 100, 0)
        if st.button("Tambah Tugas"):
            if task_name:
                task = {"task": task_name, "cost": cost, "progress": progress}
                data[project_name]["tasks"].append(task)
                data[project_name]["expenses"] += cost
                save_data(data)
                st.success("Tugas ditambahkan.")
            else:
                st.warning("Isi nama tugas terlebih dahulu.")
