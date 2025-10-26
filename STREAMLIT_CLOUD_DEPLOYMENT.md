# 🚀 Panduan Deploy Fertique AI ke Streamlit Community Cloud

## Overview
Panduan lengkap untuk deploy aplikasi **Fertique AI** ke **Streamlit Community Cloud** - platform hosting gratis resmi dari Streamlit.

---

## ✅ Persiapan Sebelum Deploy

### 1. Pastikan File-File Berikut Sudah Ada:
- ✅ `requirements.txt` - Daftar dependencies Python
- ✅ `app_agribusiness.py` - Aplikasi utama
- ✅ `.streamlit/config.toml` - Konfigurasi Streamlit
- ✅ `.gitignore` - File yang tidak perlu di-upload ke GitHub

### 2. Verifikasi Dependencies
Pastikan `requirements.txt` berisi semua library yang dibutuhkan:
```
folium>=0.20.0
gtts>=2.5.4
numpy>=2.3.4
openpyxl>=3.1.5
pandas>=2.3.3
plotly>=6.3.1
qrcode>=8.2
reportlab>=4.4.4
scikit-learn>=1.7.2
speechrecognition>=3.14.3
streamlit>=1.50.0
streamlit-aggrid>=1.1.9
streamlit-audiorecorder>=0.0.6
stripe>=13.0.1
```

---

## 📤 Langkah 1: Upload Project ke GitHub

### A. Buat Repository Baru di GitHub
1. **Pergi ke GitHub:** https://github.com/new
2. **Nama repository:** `fertique-ai` (atau nama lain yang Anda inginkan)
3. **Visibility:** Public (gratis) atau Private (butuh upgrade Streamlit)
4. **JANGAN centang** "Add a README file" atau "Add .gitignore"
5. **Klik:** "Create repository"

### B. Upload Project dari Replit ke GitHub

**Opsi 1: Menggunakan Git di Replit Shell**

```bash
# 1. Inisialisasi Git (jika belum)
git init

# 2. Tambahkan semua file
git add .

# 3. Buat commit pertama
git commit -m "Initial commit - Fertique AI Platform"

# 4. Tambahkan remote GitHub (ganti USERNAME dan REPO_NAME)
git remote add origin https://github.com/USERNAME/fertique-ai.git

# 5. Push ke GitHub
git branch -M main
git push -u origin main
```

**Catatan:** Jika diminta username/password, gunakan:
- **Username:** username GitHub Anda
- **Password:** Personal Access Token (bukan password biasa)
  - Buat token di: https://github.com/settings/tokens
  - Permissions: `repo` (full control)

**Opsi 2: Download & Upload Manual**

Jika cara Git tidak berhasil:
1. **Download project dari Replit:**
   - Klik "..." menu di Files panel
   - Pilih "Download as zip"
   
2. **Extract file zip** di komputer Anda

3. **Upload ke GitHub:**
   - Buka repository GitHub yang baru dibuat
   - Klik "uploading an existing file"
   - Drag & drop semua file dan folder
   - Klik "Commit changes"

---

## 🌐 Langkah 2: Deploy ke Streamlit Community Cloud

### A. Login ke Streamlit Community Cloud
1. **Pergi ke:** https://share.streamlit.io
2. **Klik:** "Sign in with GitHub"
3. **Authorize:** Izinkan Streamlit mengakses GitHub Anda

### B. Deploy Aplikasi Baru
1. **Klik:** "New app" (tombol di kanan atas)

2. **Isi Form Deploy:**
   ```
   Repository:       username/fertique-ai
   Branch:           main
   Main file path:   app_agribusiness.py
   ```

3. **Advanced settings** (opsional):
   - **App URL:** Pilih custom URL seperti `fertique-ai` 
     (akan jadi: https://fertique-ai.streamlit.app)
   - **Python version:** 3.11 (default)

4. **Klik:** "Deploy!"

### C. Tunggu Proses Deployment
- ⏱️ Proses biasanya **3-5 menit**
- 📦 Streamlit akan install semua dependencies dari `requirements.txt`
- ✅ Setelah selesai, aplikasi akan otomatis terbuka

---

## 🎯 Setelah Deploy Berhasil

### URL Aplikasi Anda
Aplikasi akan tersedia di:
```
https://[your-app-name].streamlit.app
```

Contoh: `https://fertique-ai.streamlit.app`

### Features yang Otomatis Aktif:
✅ **HTTPS/SSL** - Koneksi aman otomatis  
✅ **Auto-update** - Setiap push ke GitHub, app otomatis update  
✅ **Free hosting** - Gratis selamanya untuk public apps  
✅ **Custom domain** - Bisa pakai domain sendiri (settings)  

---

## 🔧 Troubleshooting - Jika Ada Error

### Error 1: "ModuleNotFoundError"
**Penyebab:** Library tidak ada di `requirements.txt`

**Solusi:**
1. Tambahkan library yang kurang ke `requirements.txt`
2. Commit & push ke GitHub:
   ```bash
   git add requirements.txt
   git commit -m "Update requirements"
   git push
   ```
3. Streamlit akan otomatis redeploy

### Error 2: "Your app is having trouble loading"
**Penyebab:** Ada error di code Python

**Solusi:**
1. Klik "Manage app" di Streamlit dashboard
2. Klik "Logs" untuk lihat error detail
3. Fix error di code
4. Push update ke GitHub

### Error 3: "Resource limits exceeded"
**Penyebab:** Aplikasi menggunakan terlalu banyak memory/CPU

**Solusi:**
1. Optimize code untuk reduce memory usage
2. Gunakan `@st.cache_data` untuk cache data
3. Upgrade ke Streamlit Pro ($20/month) untuk limits lebih besar

### Error 4: File gambar/asset tidak muncul
**Penyebab:** Path file tidak relatif

**Solusi:**
- Pastikan semua path menggunakan relative path:
  ```python
  # ✅ Good
  st.image("attached_assets/logo-fertique.jpg")
  
  # ❌ Bad
  st.image("/home/runner/attached_assets/logo-fertique.jpg")
  ```

---

## 🔐 Mengelola Secrets (API Keys)

Jika aplikasi Anda menggunakan API keys (Stripe, Twilio, dll):

### 1. Buat File Secrets di Streamlit Cloud
1. Pergi ke **Streamlit dashboard**
2. Klik **app Anda** → "..." menu → "Settings"
3. Klik tab **"Secrets"**

### 2. Tambahkan Secrets
Format TOML:
```toml
# Stripe
STRIPE_PUBLIC_KEY = "pk_live_xxxxxxxxxxxxx"
STRIPE_SECRET_KEY = "sk_live_xxxxxxxxxxxxx"

# Twilio
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxx"
TWILIO_PHONE_NUMBER = "+1234567890"

# OpenAI (jika pakai)
OPENAI_API_KEY = "sk-xxxxxxxxxxxxx"
```

### 3. Akses Secrets di Code
```python
import streamlit as st

# Akses secrets
stripe_key = st.secrets["STRIPE_SECRET_KEY"]
twilio_sid = st.secrets["TWILIO_ACCOUNT_SID"]
```

---

## 🔄 Update Aplikasi

### Auto-update dari GitHub:
Setiap kali Anda push update ke GitHub, Streamlit akan otomatis redeploy!

```bash
# 1. Edit code di Replit atau local
# 2. Commit changes
git add .
git commit -m "Update feature X"

# 3. Push ke GitHub
git push

# 4. Streamlit otomatis detect & redeploy! ✨
```

### Manual Reboot:
Jika perlu restart manual:
1. Pergi ke **Streamlit dashboard**
2. Klik **app Anda** → "..." menu
3. Klik **"Reboot app"**

---

## 📊 Monitoring & Analytics

### Melihat Logs:
1. **Streamlit dashboard** → Your app → "..." → "Logs"
2. Lihat real-time logs untuk debugging

### Melihat Usage Stats:
1. **Streamlit dashboard** → Your app → "Analytics"
2. Lihat:
   - Jumlah visitors
   - Page views
   - Active users

---

## 💰 Free Tier Limits

Streamlit Community Cloud **gratis** dengan batasan:

| Resource | Limit |
|----------|-------|
| **Apps** | 1 app gratis, unlimited apps dengan GitHub Pro |
| **Memory** | 1 GB RAM per app |
| **CPU** | Shared CPU |
| **Storage** | 1 GB per app |
| **Bandwidth** | Unlimited |
| **Uptime** | 24/7 (tapi bisa sleep jika tidak ada traffic) |

### Upgrade ke Pro ($20/month):
✅ Unlimited apps  
✅ 4 GB RAM per app  
✅ Dedicated CPU  
✅ Priority support  
✅ Custom authentication  

---

## 🌍 Custom Domain (Opsional)

Ingin pakai domain sendiri seperti `www.fertique-ai.com`?

### Langkah-langkah:
1. **Beli domain** (dari Namecheap, GoDaddy, dll)

2. **Update DNS settings** di domain registrar:
   ```
   Type: CNAME
   Name: www (atau @)
   Value: [your-app-name].streamlit.app
   TTL: 3600
   ```

3. **Update Streamlit settings:**
   - Dashboard → Your app → "..." → "Settings"
   - Tab "General" → "Custom domain"
   - Masukkan domain Anda
   - Klik "Save"

4. **Tunggu DNS propagation** (24-48 jam)

---

## ✅ Checklist Sebelum Deploy

- [ ] `requirements.txt` sudah lengkap
- [ ] `.gitignore` sudah exclude file yang tidak perlu
- [ ] Semua file path menggunakan relative path
- [ ] API keys dipindahkan ke Secrets (bukan hardcode)
- [ ] Test aplikasi di local Replit berjalan tanpa error
- [ ] Repository GitHub sudah dibuat dan public
- [ ] Files sudah di-push ke GitHub

---

## 🎉 Selamat!

Aplikasi **Fertique AI** Anda sekarang sudah LIVE di internet dan bisa diakses siapa saja!

**Next Steps:**
1. 📱 Share URL ke pengguna: `https://[your-app].streamlit.app`
2. 📊 Monitor analytics untuk lihat traffic
3. 🔄 Update aplikasi dengan push ke GitHub
4. 🌟 Tambahkan custom domain untuk branding profesional

---

## 📞 Support

**Streamlit Community Cloud Issues:**
- Docs: https://docs.streamlit.io/deploy
- Forum: https://discuss.streamlit.io
- Status: https://streamlitstatus.com

**Fertique AI Support:**
- Email: support@fertique-ai.com
- Website: www.fertique-ai.com

---

**Copyright © 2025 PT. Sentra Karya Integrasi Global**
