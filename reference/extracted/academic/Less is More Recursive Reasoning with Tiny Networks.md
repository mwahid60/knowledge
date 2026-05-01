---
date: 2025-10-06
researcher:
  - Alexia Jolicoeur-Martineau
organisation:
  - Samsung SAIL Montréal
url:
  - https://arxiv.org/abs/2510.04871
tags:
  - Technology
  - Artificial_Intelligence
  - Deep_Learning
  - Neural_Networks
  - Recursive_Reasoning
---
# Less is More: Penalaran Rekursif dengan Jaringan Kecil (Tiny Networks)

## Abstrak

Model Penalaran Hirarkis (Hierarchical Reasoning Model - HRM) adalah pendekatan baru yang menggunakan dua jaringan neural kecil yang berulang pada frekuensi yang berbeda. Metode yang terinspirasi biologis ini mengalahkan Model Bahasa Besar (LLMs) pada tugas teka-teki yang sulit seperti Sudoku, Maze, dan ARC-AGI, dilatih dengan model kecil (27M parameter) pada data kecil (~1000 contoh). HRM memiliki prospek besar untuk menyelesaikan masalah sulit dengan jaringan kecil, tetapi belum dipahami dengan baik dan mungkin masih suboptimal.

Kami mengusulkan Tiny Recursive Model (TRM), pendekatan penalaran rekursif yang jauh lebih sederhana yang mencapai generalisasi yang jauh lebih tinggi daripada HRM, sambil menggunakan satu jaringan kecil dengan hanya 2 lapisan. Dengan hanya 7M parameter, TRM memperoleh 45% akurasi tes pada ARC-AGI-1 dan 8% pada ARC-AGI-2, lebih tinggi daripada sebagian besar LLM (misalnya, Deepseek R1, o3-mini, Gemini 2.5 Pro) dengan kurang dari 0,01% parameter.

## 1. Pendahuluan

Meskipun kuat, Model Bahasa Besar (LLMs) dapat kesulitan pada masalah tanya-jawab yang sulit. Karena mereka menghasilkan jawaban secara auto-regresif, ada risiko kesalahan yang tinggi karena satu token yang tidak benar dapat membuat jawaban tidak valid. Untuk meningkatkan keandalan, LLM mengandalkan Chain-of-thoughts (CoT) dan Test-Time Compute (TTC).

CoT berusaha meniru penalaran manusia dengan meminta LLM untuk menyampling jejak penalaran langkah demi langkah sebelum memberikan jawaban. Meskipun dapat meningkatkan akurasi, CoT mahal, memerlukan data penalaran berkualitas tinggi (yang mungkin tidak tersedia), dan dapat rapuh karena penalaran yang dihasilkan mungkin salah. Untuk lebih meningkatkan keandalan, komputasi waktu-tes dapat digunakan dengan melaporkan jawaban yang paling umum dari K atau jawaban dengan imbalan tertinggi.

Namun, ini mungkin tidak cukup. LLM dengan CoT dan TTC tidak cukup untuk mengalahkan setiap masalah. Meskipun LLM telah membuat kemajuan signifikan pada ARC-AGI sejak 2019, akurasi tingkat manusia masih belum tercapai (6 tahun kemudian, pada saat penulisan paper ini). Selain itu, LLM kesulitan pada ARC-AGI-2 yang lebih baru (misalnya, Gemini 2.5 Pro hanya memperoleh 4,9% akurasi tes dengan jumlah TTC yang tinggi).

Sebuah arah alternatif baru-baru ini diusulkan oleh Wang et al. (2025). Mereka mengusulkan cara baru melalui Model Penalaran Hirarkis (HRM) yang mereka kembangkan, yang memperoleh akurasi tinggi pada tugas teka-teki di mana LLM kesulitan (misalnya, penyelesaian Sudoku, pencarian jalur Maze, dan ARC-AGI). HRM adalah model pembelajaran terawasi dengan dua inovasi utama:

1. **Penalaran hirarkis rekursif**: terdiri dari mengulangi beberapa kali melalui dua jaringan kecil (f L pada frekuensi tinggi dan f H pada frekuensi rendah) untuk memprediksi jawaban. Setiap jaringan menghasilkan fitur laten yang berbeda.
2. **Deep supervision**: terdiri dari meningkatkan jawaban melalui beberapa langkah supervisi sambil membawa dua fitur laten sebagai inisialisasi untuk langkah-langkah perbaikan.

Analisis independen pada tolok ukur ARC-AGI menunjukkan bahwa deep supervision tampaknya menjadi pendorong utama dari peningkatan kinerja. Menggunakan deep supervision menggandakan akurasi dibandingkan supervisi satu-langkah (dari 19% menjadi 39% akurasi), sementara penalaran hirarkis rekursif hanya sedikit meningkatkan akurasi dibandingkan model reguler dengan satu forward pass (dari 35,7% menjadi 39,0% akurasi). Ini menunjukkan bahwa penalaran di berbagai langkah supervisi berharga, tetapi rekursi yang dilakukan di setiap langkah supervisi tidak terlalu penting.

Dalam karya ini, kami menunjukkan bahwa manfaat dari penalaran rekursif dapat ditingkatkan secara masif, menjadikannya jauh lebih dari sekadar inkremental. Kami mengusulkan Tiny Recursive Model (TRM), pendekatan yang lebih baik dan disederhanakan menggunakan jaringan kecil yang jauh lebih kecil dengan hanya 2 lapisan yang mencapai generalisasi yang jauh lebih tinggi daripada HRM pada berbagai masalah.

## 2. Latar Belakang

### 2.1 Struktur dan Tujuan HRM

Fokus HRM adalah pembelajaran terawasi. Diberikan input, hasilkan output. Baik input maupun output diasumsikan memiliki bentuk [B, L], di mana B adalah ukuran batch dan L adalah panjang konteks.

HRM berisi empat komponen yang dapat dipelajari:
- **Input embedding** f I (·; θ I )
- **Jaringan rekuren tingkat rendah** f L (·; θ L )
- **Jaringan rekuren tingkat tinggi** f H (·; θ H )
- **Output head** fO (·; θO )

Setiap jaringan adalah arsitektur Transformer 4-lapisan dengan RMSNorm, tanpa bias, rotary embeddings, dan fungsi aktivasi SwiGLU.

### 2.2 Rekursi pada Dua Frekuensi Berbeda

Diberikan hyperparameter yang digunakan oleh Wang et al. (2025) (n = 2 langkah f L, 1 langkah f H; dilakukan T = 2 kali), forward pass HRM dilakukan sebagai berikut:

1. x ← f I (x̃)
2. z L ← f L (z L + z H + x) tanpa gradien
3. z L ← f L (z L + z H + x) tanpa gradien
4. z H ← f H (z L + z H ) tanpa gradien
5. z L ← f L (z L + z H + x) tanpa gradien
6. z L ← z L .detach()
7. z H ← z H .detach()
8. z L ← f L (z L + z H + x) dengan gradien
9. z H ← f H (z L + z H ) dengan gradien
10. ŷ ← argmax(fO (z H ))

di mana ŷ adalah jawaban output yang diprediksi.

### 2.3 Deep Supervision

Untuk meningkatkan kedalaman efektif, deep supervision digunakan. Ini terdiri dari menggunakan kembali fitur laten sebelumnya (z H dan z L) sebagai inisialisasi untuk forward pass berikutnya. Ini memungkinkan model untuk berpenalaran atas banyak iterasi dan meningkatkan fitur latennya (z L dan z H) sampai (diharapkan) konvergen ke solusi yang benar. Paling banyak Nsup = 16 langkah supervisi digunakan.

### 2.4 Adaptive Computational Time (ACT)

Dengan deep supervision, setiap mini-batch dari contoh data harus digunakan untuk Nsup = 16 langkah supervisi sebelum beralih ke mini-batch berikutnya. Ini mahal, dan ada keseimbangan yang harus dicapai antara mengoptimalkan beberapa contoh data untuk banyak langkah supervisi versus mengoptimalkan banyak contoh data dengan lebih sedikit langkah supervisi.

## 3. Metodologi

### 3.1 Tiny Recursive Model (TRM)

TRM adalah pendekatan penalaran rekursif yang jauh lebih sederhana yang menggunakan satu jaringan kecil dengan hanya 2 lapisan. Model ini secara rekursif meningkatkan jawaban yang diprediksikan y dengan jaringan kecil. Dimulai dengan pertanyaan input x yang di-embed dan jawaban awal y yang di-embed, serta laten z. Untuk hingga Nsup = 16 langkah perbaikan, model mencoba meningkatkan jawabannya y. Caranya adalah dengan:

1. Secara rekursif memperbarui n kali laten z-nya diberikan pertanyaan x, jawaban saat ini y, dan laten saat ini z (penalaran rekursif)
2. Kemudian memperbarui jawabannya y diberikan jawaban saat ini y dan laten saat ini z

Proses rekursif ini memungkinkan model untuk secara progresif meningkatkan jawabannya (berpotensi mengatasi kesalahan dari jawaban sebelumnya) dengan cara yang sangat efisien parameter sambil meminimalkan overfitting.

### 3.2 Perbedaan Utama dengan HRM

| Aspek | HRM | TRM |
|-------|-----|-----|
| Jumlah Jaringan | 2 (f L dan f H) | 1 |
| Lapisan per Jaringan | 4 | 2 |
| Total Parameter | 27M | 7M |
| Teorema Fixed Point | Diperlukan | Tidak diperlukan |
| Justifikasi Biologis | Kompleks | Sederhana |
| Hirarki | Ya | Tidak |
| Proses Halting | Ekstra forward pass | Dihilangkan |

## 4. Hasil dan Evaluasi

### 4.1 Tolok Ukur

Model dievaluasi pada tolok ukur berikut:

**Sudoku-Extreme**
- 1000 augmentasi pengacakan per contoh data
- Tugas penyelesaian Sudoku 9x9 yang sulit

**Maze-Hard (30x30)**
- 8 transformasi dihedral per contoh data
- Pencarian jalur optimal dalam labirin besar

**ARC-AGI**
- 1000 augmentasi data per contoh data (permutasi warna, transformasi grup dihedral, dan translasi)
- ARC-AGI-1: 800 tugas
- ARC-AGI-2: 1120 tugas (versi yang lebih sulit)

### 4.2 Hasil Perbandingan

#### Sudoku-Extreme
- TRM (tanpa self-attention): **87,4%** akurasi tes
- TRM (dengan self-attention): 77,4%
- HRM: 55%

#### Maze-Hard (30x30)
- TRM (dengan self-attention): **85%**
- HRM: 75%

#### ARC-AGI-1
- TRM-Att (Ours): **44,6%**
- HRM: 40,3%
- Grok-4-thinking: 66,7%
- Bespoke (Grok-4): 79,6%
- Gemini 2.5 Pro 32K: 37,0%
- o3-mini-high: 34,5%
- Deepseek R1: 5,0%

#### ARC-AGI-2
- TRM-Att (Ours): **7,8%**
- HRM: 5,0%
- Bespoke (Grok-4): 29,4%
- Grok-4-thinking: 16,0%
- Gemini 2.5 Pro 32K: 4,9%
- o3-mini-high: 3,0%
- Deepseek R1: 1,3%

## 5. Analisis

### 5.1 Keunggulan TRM

1. **Kesederhanaan**: TRM jauh lebih sederhana daripada HRM, tanpa memerlukan teorema fixed point, justifikasi biologis kompleks, atau hirarki
2. **Efisiensi Parameter**: Mengurangi jumlah parameter dari 27M menjadi 7M (kurang dari 0,01% parameter LLM)
3. **Generalisasi yang Lebih Baik**: Mencapai generalisasi yang signifikan lebih tinggi pada berbagai masalah
4. **Proses Halting yang Disederhanakan**: Menghilangkan kebutuhan untuk ekstra forward pass

### 5.2 Temuan Penting

- Mengganti self-attention dengan MLP berfungsi sangat baik pada Sudoku-Extreme (meningkatkan akurasi tes sebesar 10%), tetapi buruk pada dataset lain
- TRM dengan self-attention menggeneralisasi lebih baik pada sebagian besar tugas (mungkin karena bias induktif dan overcapacity)
- Pilihan arsitektur yang optimal mungkin berbeda untuk dataset yang berbeda

### 5.3 Batasan dan Tantangan

Meskipun pendekatan ini menghasilkan generalisasi yang lebih baik pada 4 tolok ukur, setiap pilihan yang dibuat tidak dijamin optimal pada setiap dataset. Hukum penskalaan diperlukan untuk mengparametrisasi jaringan-jaringan ini secara optimal.

Meskipun kami menyederhanakan dan meningkatkan deep recursion, pertanyaan mengapa rekursi membantu begitu banyak dibandingkan dengan menggunakan jaringan yang lebih besar dan lebih dalam masih harus dijelaskan; kami menduga ini berkaitan dengan overfitting, tetapi kami tidak memiliki teori untuk mendukung penjelasan ini.

Saat ini, model penalaran rekursif seperti HRM dan TRM adalah metode pembelajaran terawasi daripada model generatif. Ini berarti diberikan pertanyaan input, mereka hanya dapat memberikan satu jawaban deterministik. Dalam banyak pengaturan, beberapa jawaban ada untuk satu pertanyaan. Dengan demikian, akan menarik untuk memperluas TRM ke tugas generatif.

## 6. Kesimpulan

Kami mengusulkan Tiny Recursion Models (TRM), pendekatan penalaran rekursif sederhana yang mencapai generalisasi yang kuat pada tugas sulit menggunakan satu jaringan kecil yang berulang pada fitur penalaran latennya dan secara progresif meningkatkan jawaban akhirnya.

Berbeda dengan Model Penalaran Hirarkis (HRM), TRM tidak memerlukan teorema fixed point, justifikasi biologis kompleks, dan hirarki. Ini secara signifikan mengurangi jumlah parameter dengan memotong jumlah lapisan menjadi dua dan mengganti dua jaringan dengan satu jaringan kecil. Ini juga menyederhanakan proses halting, menghilangkan kebutuhan untuk forward pass ekstra. Secara keseluruhan, TRM jauh lebih sederhana daripada HRM, sambil mencapai generalisasi yang lebih baik.

Hasil yang dicapai:
- Sudoku-Extreme: 87% (peningkatan dari 55% HRM)
- Maze-Hard: 85% (peningkatan dari 75% HRM)
- ARC-AGI-1: 45% (peningkatan dari 40% HRM)
- ARC-AGI-2: 8% (peningkatan dari 5% HRM)

Dengan hanya 7M parameter, TRM mengungguli sebagian besar LLM yang jauh lebih besar pada tolok ukur ini, menunjukkan bahwa efisiensi arsitektur dan rekursi dapat lebih penting daripada sekadar penskalaan ukuran model.

## Daftar Pustaka

1. ARC Prize Foundation. The Hidden Drivers of HRM's Performance on ARC-AGI. https://arcprize.org/blog/hrm-analysis, 2025a. [Online; accessed 2025-09-15].

2. ARC Prize Foundation. ARC-AGI Leaderboard. https://arcprize.org/leaderboard, 2025b. [Online; accessed 2025-09-24].

3. Bai, S., Kolter, J. Z., and Koltun, V. Deep equilibrium models. Advances in neural information processing systems, 32, 2019.

4. Bai, X. and Melas-Kyriazi, L. Fixed point diffusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 9430–9440, 2024.

5. Brock, A., Donahue, J., and Simonyan, K. Large scale gan training for high fidelity natural image synthesis. arXiv preprint arXiv:1809.11096, 2018.

6. Chollet, F. On the measure of intelligence. arXiv preprint arXiv:1911.01547, 2019.

7. Chollet, F., Knoop, M., Kamradt, G., Landers, B., and Pinkard, H. Arc-agi-2: A new challenge for frontier ai reasoning systems. arXiv preprint arXiv:2505.11831, 2025.

8. Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung, H. W., Sutton, C., Gehrmann, S., et al. Palm: Scaling language modeling with pathways. Journal of Machine Learning Research, 24(240):1–113, 2023.

9. Dillion, T. Tdoku: A fast sudoku solver and generator. https://t-dillon.github.io/tdoku/, 2025.

10. Elman, J. L. Finding structure in time. Cognitive science, 14(2):179–211, 1990.

11. Fedus, W., Zoph, B., and Shazeer, N. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. Journal of Machine Learning Research, 23(120):1–39, 2022.

12. Geng, Z. and Kolter, J. Z. Torchdeq: A library for deep equilibrium models. arXiv preprint arXiv:2310.18605, 2023.

13. Hendrycks, D. and Gimpel, K. Gaussian error linear units (gelus). arXiv preprint arXiv:1606.08415, 2016.

14. Jang, Y., Kim, D., and Ahn, S. Hierarchical graph generation with k2-trees. In ICML 2023 Workshop on Structured Probabilistic Inference Generative Modeling, 2023.

15. Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and Amodei, D. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361, 2020.

16. Kingma, D. P. and Ba, J. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.

17. Krantz, S. G. and Parks, H. R. The implicit function theorem: history, theory, and applications. Springer Science & Business Media, 2002.

18. LeCun, Y. Une procedure d'apprentissage ponr reseau a seuil asymetrique. Proceedings of cognitiva 85, pp. 599–604, 1985.

19. Lehnert, L., Sukhbaatar, S., Su, D., Zheng, Q., Mcvay, P., Rabbat, M., and Tian, Y. Beyond a*: Better planning with transformers via search dynamics bootstrapping. arXiv preprint arXiv:2402.14083, 2024.

20. Lillicrap, T. P. and Santoro, A. Backpropagation through time and the brain. Current opinion in neurobiology, 55:82–89, 2019.

21. Loshchilov, I. and Hutter, F. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.

22. Moskvichev, A., Odouard, V. V., and Mitchell, M. The conceptarc benchmark: Evaluating understanding and generalization in the arc domain. arXiv preprint arXiv:2305.07141, 2023.

23. Palm, R., Paquet, U., and Winther, O. Recurrent relational networks. Advances in neural information processing systems, 31, 2018.

24. Park, K. Can convolutional neural networks crack sudoku puzzles? https://github.com/Kyubyong/sudoku, 2018.

25. Prieto, L., Barsbey, M., Mediano, P. A., and Birdal, T. Grokking at the edge of numerical stability. arXiv preprint arXiv:2501.04697, 2025.

26. Rumelhart, D. E., Hinton, G. E., and Williams, R. J. Learning internal representations by error propagation. Technical report, 1985.

27. Shazeer, N. Glu variants improve transformer. arXiv preprint arXiv:2002.05202, 2020.

28. Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G., and Dean, J. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017.

29. Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling llm test-time compute optimally can be more effective than scaling model parameters. arXiv preprint arXiv:2408.03314, 2024.

30. Song, Y. and Ermon, S. Improved techniques for training score-based generative models. Advances in neural information processing systems, 33:12438–12448, 2020.

31. Su, J., Ahmed, M., Lu, Y., Pan, S., Bo, W., and Liu, Y. Roformer: Enhanced transformer with rotary position embedding. Neurocomputing, 568:127063, 2024.

32. Tolstikhin, I. O., Houlsby, N., Kolesnikov, A., Beyer, L., Zhai, X., Unterthiner, T., Yung, J., Steiner, A., Keysers, D., Uszkoreit, J., et al. Mlp-mixer: An all-mlp architecture for vision. Advances in neural information processing systems, 34:24261–24272, 2021.

33. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. Advances in neural information processing systems, 30, 2017.

34. Wang, G., Li, J., Sun, Y., Chen, X., Liu, C., Wu, Y., Lu, M., Song, S., and Yadkori, Y. A. Hierarchical reasoning model. arXiv preprint arXiv:2506.21734, 2025.

35. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837, 2022.

36. Werbos, P. Beyond regression: New tools for prediction and analysis in the behavioral sciences. PhD thesis, Committee on Applied Mathematics, Harvard University, Cambridge, MA, 1974.

37. Werbos, P. J. Generalization of backpropagation with application to a recurrent gas market model. Neural networks, 1(4):339–356, 1988.

38. Zhang, B. and Sennrich, R. Root mean square layer normalization. Advances in Neural Information Processing Systems, 32, 2019.

---

**Referensi**: arXiv:2510.04871v1 [cs.LG] 6 Oct 2025

**Kontak**: alexia.j@samsung.com

**Institusi**: Samsung SAIL Montréal
