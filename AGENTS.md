# AGENTS.md

Panduan komprehensif untuk asisten koding yang bekerja di repository knowledge base berbasis Obsidian ini.

---

## 1. INFORMASI UMUM

### 1.1 Deskripsi Repository
Repository ini adalah knowledge base berbasis Obsidian untuk mendokumentasikan berita, penelitian, dan informasi. Terdiri dari:
- **knowledge/**: File analisis dan sintesis utama
- **reference/**: File referensi individual (academic, information, news)
- **logs/**: Catatan aktivitas harian

### 1.2 Bahasa
- **Bahasa utama**: Bahasa Indonesia
- **Istilah resmi**: Gunakan bahasa Inggris untuk nama perusahaan, institusi, dan istilah teknis
- **Tags**: Bahasa Inggris (kecuali yang diizinkan, lihat bagian Tags)

### 1.3 Workflow Penelitian
Ketika diminta melakukan penelitian:
1. **Cek Index** - Baca `reference/index.md` terlebih dahulu
2. **Cari Referensi** - Jika topik ada, baca file referensi yang relevan
3. **Web Search** - Hanya jika informasi tidak cukup di index
4. **Salin Informasi** - Salin informasi yang kamu temukan di internet ke dalam folder yang sesuai seperti berikut :
	1. `/news` : Jika sumbernya berasal dari portal berita
	2. `/information` : Jika informasi tersebut tidak lekang akan waktu, misal informasi sejarah, profil perusahaan, identitas seseorang dan lainnya.
	3. `/academic` : Bersumber dari artikel penelitian yang valid dan dapat dipertanggungjawabkan 
5. **Buat File Research Baru** - Ikuti konvensi penamaan dan format
6. **Update Index** - Tambahkan entri baru ke `reference/index.md`

Notes:
> Pencarian informasi harus dilakukan mengikuti pola Root Cause Analysis, misal topik penelitian adalah "kemenangan prabowo dalam pemilu 2024" yang mana itu merupakan akibat dari "keberpihakan jokowi dalam mendukung prabowo" maka pencarian informasi yang kamu lakukan adalah kenapa jokowi berpihak ke prabowo? setelah mendapatkan informasi dan memverifikasinya, buatkan salinan informasi tersebut ke dalam folder extracted sesuai dengan tipenya.

### 1.4 Aturan Wiki Link
- **Gunakan format markdown standar**: `[Alias](/path/to/file/File%20Name.md)`
- **Jangan gunakan format Obsidian**: `[[Nama File]]`
- Contoh: `[PHK Sepanjang 2025](/knowledge/PHK%20Sepanjang%202025.md)`

---

## 2. STRUKTUR REPOSITORY

```
/Users/mwahid2004/Library/CloudStorage/OneDrive-Personal/Notes/Knowledge/
├── knowledge/                    # File analisis utama (synthesized)
│   ├── index.md                  # Index knowledge files
│   ├── PHK Sepanjang 2025.md
│   ├── Kerugian Nasabah Bank Sepanjang 2025.md
│   └── Pelanggaran Hukum Aparat Negara Sepanjang 2025.md
├── logs/                         # Catatan aktivitas harian
│   └── 2026-05-01.md
├── reference/
│   ├── index.md                  # Index referensi
│   ├── extracted/
│   │   ├── academic/             # Penelitian akademik
│   │   ├── information/          # Informasi umum/profil perusahaan
│   │   └── news/                 # Kasus berita individual
│   └── raw/                      # PDF dan dokumen mentah
├── .obsidian/                    # Konfigurasi Obsidian (gitignored)
└── .venv/                        # Python venv (gitignored)
```

---

## 3. ATURAN TAGS

### 3.1 Aturan Umum Tags
- **Jumlah**: Tepat 5 tags untuk reference files
- **Format**: Title_Case dengan underscore untuk multi-word
- **Contoh**: `Bank_DKI`, `Social_Behavior`

### 3.2 Tags dalam Bahasa Indonesia (Dibolehkan)
Tags berikut HARUS ditulis dalam bahasa Indonesia:
- **Location**: Nama provinsi atau "Nasional"
  - Contoh: `Jawa_Tengah`, `Jakarta`, `Nasional`
- **Subject**: Nama perusahaan atau institusi Indonesia
  - Contoh: `Sritex`, `Bank_DKI`, `eFishery`, `BNI`, `TNI`
- **BUMN**: Gunakan istilah `BUMN` (bukan `State_Owned_Enterprise`)

### 3.3 Tags dalam Bahasa Inggris (Wajib)
Selain location, subject, dan BUMN, SEMUA tags lainnya HARUS dalam bahasa Inggris:
- **Category**: `Textile`, `Banking`, `Startup`, `Manufacturing`, `Technology`
- **Descriptive**: `Layoffs`, `Bankruptcy`, `Fraud`, `Hacking`, `Corruption`
- **Academic**: `Psychology`, `Social_Behavior`, `Personality`

### 3.4 Contoh Benar dan Salah
**Benar**:
```yaml
tags:
  - Sritex          # Subject (Indonesia)
  - Jawa_Tengah     # Location (Indonesia)
  - Textile         # Category (Inggris)
  - Layoffs         # Descriptive (Inggris)
  - Bankruptcy      # Descriptive (Inggris)
```

**Salah**:
```yaml
tags:
  - Tekstil         # ❌ Harus: Textile
  - PHK             # ❌ Harus: Layoffs
  - Pailit          # ❌ Harus: Bankruptcy
  - Keuangan        # ❌ Harus: Finance
  - Berita          # ❌ Harus: News
```

---

## 4. KNOWLEDGE FILES

### 4.1 Definisi
File analisis komprehensif yang menyintesis data dari multiple reference files.

### 4.2 Penamaan File
- Gunakan nama deskriptif dalam bahasa Indonesia
- Format: `<Topik Research>.md`
- Contoh: `PHK Sepanjang 2025.md`, `Kerugian Nasabah Bank Sepanjang 2025.md`

### 4.3 Front Matter
```yaml
---
created_at: YYYY-MM-DD
tags:
  - Research_Type # pilih salah satu yang paling sesuai [News_Research, Academic_Research]
  - Category
  - Descriptive_Tag1
  - Descriptive_Tag2
  - Descriptive_Tag3
reference:
  - "[Alias](/path/to/file.md)"
---
```

### 4.4 Struktur Konten
Wajib mengikuti urutan berikut:
1. **Overview** - Ringkasan umum dan statistik utama
2. **Tabel Utama** - Data lengkap dalam HTML table
3. **Tabel Ringkasan** - Summary per kategori/kuartal/industri
4. **Analisis** - Root cause & effect chain (WAJIB)
5. **Rekomendasi** - Saran kebijakan berbasis data
6. **Metodologi** - Catatan verifikasi dan sumber

Notes:
> Setiap point penjelasan harus disampaikan dengan cukup detail dan informatif sehingga pembaca dapat memahami hasil dari research yang sudah kamu buat tersebut.

### 4.5 Format Tabel
**Tabel Utama (HTML)**:
```html
<table>
<thead>
<tr>
  <th width="8%">Kolom1</th>
  <th width="10%">Kolom2</th>
</tr>
</thead>
<tbody>
<tr>
  <td>Data</td>
  <td>Data</td>
</tr>
</tbody>
</table>
```

Notes:
> Gunakan tabel html jika kamu membutuhkan tabel yang kompleks, misal kamu butuh merge cell, listed value, dan sebagainya. Jika kamu tidak membutuhkan tabel yang kompleks seperti itu, maka buat dalam markdown tabel saja.

**Tabel Ringkasan (Markdown)**:
```markdown
| Kategori | Jumlah |
|----------|--------|
| Kategori | 5      |
```

---

## 5. REFERENCE FILES

### 5.1 Academic Files
**Lokasi**: `reference/extracted/academic/`

#### 5.1.1 Penamaan File
- Gunakan judul akademik dalam bahasa Inggris
- Format: `<Judul Penelitian>.md`
- Contoh: `Hierarchical Reasoning Model.md`, `The Aging Epigenome.md`

#### 5.1.2 Front Matter
```yaml
---
date: YYYY-MM-DD
published_by:
  - Nama Jurnal
  - Nama Penulis
url:
  - https://doi.org/xxxxx
tags:
  - Main_Category
  - Sub_Category
  - Descriptive_Tag
  - Descriptive_Tag
  - Descriptive_Tag
---
```

#### 5.1.3 Struktur Konten
1. **Abstrak** - Ringkasan penelitian
2. **Metodologi** - Cara penelitian dilakukan
3. **Hasil** - Temuan utama
4. **Kesimpulan** - Implikasi penelitian
5. **Daftar Pustaka** - Format numbered list

#### 5.1.4 Format Daftar Pustaka
```markdown
## Daftar Pustaka

1. Author, A. A., & Author, B. B. (Year). Title of the article. *Journal Name*, volume(issue), pages. https://doi.org/xxxxx
2. Author, C. C. (Year). Title of the book. Publisher.
```
- Gunakan `## Daftar Pustaka`
- Nomor urut
- Gunakan italic (`*text*`) untuk nama jurnal dan buku

---

### 5.2 Information Files
**Lokasi**: `reference/extracted/information/`

#### 5.2.1 Penamaan File
- Gunakan nama perusahaan atau topik
- Format: `<Nama Perusahaan>.md`
- Contoh: `Panca Global Sekuritas.md`, `Gudang Garam.md`

#### 5.2.2 Front Matter
```yaml
---
date: YYYY-MM-DD
published_by:
  - Sumber 1
  - Sumber 2
url:
  - https://example.com/source1
  - https://example.com/source2
tags:
  - Subject
  - Information-type # [Company_Profile, Person_Profile, History, General_Information]
  - Afiliasi_atau_Hubungan_Tertentu # Contoh BUMN, Djarum_Group dll
  - Category
  - Tag_5
---
```

#### 5.2.3 Struktur Konten (Profil Perusahaan)
Wajib mengikuti urutan:
1. **Ringkasan** - Paragraf overview + tabel atribut (Nama resmi, Kode emiten, Industri, Didirikan, Kantor pusat, Wilayah operasi, Situs web)
2. **Sejarah Berdiri** - Kronologi dengan sub-bab era (Awal Mula, Era Pertumbuhan, Transformasi, Era Modern)
3. **Kinerja Keuangan** - Tabel metrik (Pendapatan, Laba bersih, Total aset, Total ekuitas, Karyawan) dengan tahun
4. **Kepemilikan Saham** - Tabel pemegang saham utama + riwayat kepemilikan
5. **Kepemimpinan Perusahaan** - Tabel direksi/komisaris terkini + riwayat
6. **Profil Direksi/Komisaris** (opsional) - Karir detail pemimpin kunci
7. **Industri & Bidang Usaha** - Daftar berurut segmen bisnis
8. **Produk & Layanan** - Tabel produk/layanan per kategori
9. **Afiliasi & Anak Usaha** - Tabel anak perusahaan/afiliasi
10. **Fakta Menarik Tambahan** - Daftar berurut 8-10 fakta unik

#### 5.2.4 Formatting Rules
- Gunakan `---` untuk memisahkan section utama
- Gunakan markdown table untuk data sederhana
- Gunakan HTML table hanya jika format kompleks diperlukan
- Sertakan tahun pada data keuangan (contoh: "Kinerja Keuangan (2023)")
- Bahasa: Indonesia (kecuali istilah resmi dalam Inggris)

#### 5.2.5 Catatan Penting
- Verifikasi ulang informasi yang kamu temukan di internet itu adalah valid.
- Jika ada informasi penting yang kamu temukan di sosial media yang disampaikan oleh seseorang yang tidak dapat kamu verifikasi kebenarannya maka jelaskan bahwa itu informasi tersebut belum terverifikasi.
- Jangan masukkan data yang tidak jelas yang bisa mengakibatkan bias dalam analisis kedepannya.

---

### 5.3 News Files
**Lokasi**: `reference/extracted/news/`

#### 5.3.1 Penamaan File
- Format: `<subjek>-<deskripsi-singkat>-<lokasi>-<YYYY-MM>.md`
- Gunakan lowercase dengan hyphens
- Contoh: `tni-al-tembak-bos-rental-banten-2025-01.md`

#### 5.3.2 Front Matter
```yaml
---
date: YYYY-MM-DD
published_by:
  - Media 1
  - Media 2
url:
  - https://example.com/article1
  - https://example.com/article2
tags:
  - Subject
  - Location
  - Category
  - Descriptive_Tag
  - Descriptive_Tag
---
```

#### 5.3.3 Struktur Konten
Wajib mengikuti urutan:
1. **Ringkasan** - Paragraf singkat kasus
2. **Detail Kasus** - Fakta-fakta utama dengan bullet points
3. **Perkembangan Hukum** - Status hukum dan proses peradilan
4. **Respons Institusi** - Tanggapan pihak terkait
5. **Analisis Konteks** - Analisis singkat

#### 5.3.4 Aturan URL
- Minimal 3 sumber berita independen
- Sertakan URL lengkap di front matter dan di bagian Referensi
- Jangan pernah menebak URL - gunakan URL terverifikasi dari hasil pencarian

#### 5.2.5 Catatan Penting
- Verifikasi ulang informasi yang kamu temukan di internet itu adalah valid.
- Jika ada informasi penting yang kamu temukan di sosial media yang disampaikan oleh seseorang yang tidak dapat kamu verifikasi kebenarannya maka jelaskan bahwa itu informasi tersebut belum terverifikasi.
- Jangan masukkan data yang tidak jelas yang bisa mengakibatkan bias dalam analisis kedepannya.

---

## 6. ANALISIS GUIDELINES

### 6.1 Root Cause Analysis (RCA)
Setiap analisis kasus HARUS menjelaskan **sebab dan akibat** secara komprehensif:

#### 6.1.1 Identifikasi Root Cause
Jangan hanya menyebut faktor, tapi jelaskan **mekanisme** kenapa faktor tersebut menyebabkan masalah.

**Contoh Buruk**:
> "Perang dagang AS-China menyebabkan PHK"

**Contoh Baik**:
> "Tarif impor 145% oleh AS terhadap produk China (Mei 2025) memaksa eksportir China mencari pasar alternatif. China melakukan dumping produk tekstil ke Indonesia dengan harga 30-40% di bawah harga pasar. Produk impor ini membanjiri pasar domestik, menyebabkan penurunan permintaan lokal 25%. Perusahaan tekstil lokal kehilangan pendapatan, tidak mampu membayar utang, dan akhirnya bangkrut → PHK massal"

#### 6.1.2 Chain of Effects
Jelaskan rantai dampak secara berurutan:
- **Trigger** (pemicu) → **Direct Effect** (dampak langsung) → **Indirect Effect** (dampak tidak langsung) → **Final Impact** (dampak akhir)

**Contoh**:
> Kenaikan suku bunga The Fed 5,5% → arus modal keluar dari emerging markets → pelemahan rupiah 12% → biaya impor bahan baku naik → biaya produksi naik 18% → harga jual tidak kompetitif → penurunan order 30% → PHK

**Note**:
> lakukan eksplorasi dari rantai sebab akibat yang terjadi misalnya "kenapa The FED menaikkan suku bunga?" bisa jadi ada penyebab kenapa The FED menaikkan suku bunga tersebut, dan bisa jadi The FED menaikkan suku bunga bukanlah penyebab paling awal dari rantai Root Cause Analysis ini atau masih ada dampak lanjutan dari terjadinya PHK sehingga PHK bukanlah dampak paling akhir dari hasil analisis tersebut.

#### 6.1.3 Multiple Perspectives
Analisis harus mencakup:
- **Faktor Eksternal**: Geopolitik, ekonomi global, kebijakan negara lain
- **Faktor Internal**: Manajemen, kebijakan perusahaan, teknologi
- **Faktor Struktural**: Regulasi, infrastruktur, rantai pasok

#### 6.1.4 Quantitative Impact
Sertakan angka dan persentase jika tersedia untuk mengukur dampak.

### 6.2 Standard Analysis Sections
Sertakan analisis berikut jika relevan:
1. **Pola Temporal** - Pola waktu dengan breakdown kuartal
2. **Modus Dominan** - Modus operandi dominan dengan contoh spesifik
3. **Root Cause & Effect Chain** - Sebab-akibat komprehensif (WAJIB)
4. **Pola Impunitas** - Pola impunitas
5. **Kesesuaian Hukuman** - Analisis hukuman vs undang-undang
6. **Data Konteks** - Konteks dari LSM/organisasi HAM
7. **Rekomendasi** - Rekomendasi spesifik dan actionable

---

## 7. WRITING STYLE

### 7.1 Aturan Umum
- **Bahasa**: Bahasa Indonesia
- **Tone**: Objektif, faktual, analitis
- **Sitasi**: Selalu cantumkan sumber dengan URL
- **Tanggal**: Format DD Bulan YYYY (contoh: 15 Januari 2025)
- **Angka**: Gunakan pemisah ribuan (contoh: Rp 2,65 miliar)

### 7.2 Format Markdown
- **Indentasi**: 2 spasi untuk list item bersarang, 4 spasi untuk code blocks
- **Line breaks**: Gunakan baris kosong antar section dan paragraf
- **Heading**: `##` untuk section utama, `###` untuk subsection, `####` untuk section minor
- **List**: `-` untuk unordered, `1.` untuk ordered
- **Bold/italic**: `**bold**` untuk penekanan, `*italic*` untuk kutipan atau istilah asing
- **Quotes**: `>` untuk blockquotes dari sumber
- **Code blocks**: Triple backticks dengan identifier bahasa jika diperlukan
- **Horizontal rules**: `---` untuk memisahkan section utama

---

## 8. GIT WORKFLOW

- **Jangan commit** kecuali diminta eksplisit oleh pengguna
- Cek git status sebelum melakukan perubahan
- Jangan pernah commit secrets atau credentials
- Gunakan commit message deskriptif jika diminta commit

---

## 9. ERROR HANDLING & VERIFICATION

- Selalu verifikasi fakta dengan minimal 2 sumber independen
- Gunakan Tavily search untuk verifikasi URL
- Cross-reference tanggal, nama, dan angka di berbagai media
- Tandai informasi tidak pasti dengan "diduga" atau "belum dikonfirmasi"
- Jangan pernah membuat atau menebak URL, tanggal, atau fakta

---

## 10. PROHIBITED ACTIONS

- Jangan membuat/modifikasi file di `.obsidian/` atau `.venv/`
- Jangan menghapus entry `.gitignore`
- Jangan menebak URL - gunakan URL terverifikasi dari hasil pencarian
- Jangan membuat placeholder content
- Jangan memodifikasi file tanpa membaca terlebih dahulu

---

## 11. OBSIDIAN INTEGRATION

Repository ini dioptimalkan untuk Obsidian:
- Wiki links menggunakan format markdown standar: `[Alias](/path/to/file.md)`
- Tags untuk navigasi graph view
- HTML tables render dengan baik di Obsidian
- YAML front matter untuk dataview queries

---

*Terakhir diperbarui: 2026-05-01*
