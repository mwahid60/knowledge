---
date: 2025-10-06
researcher:
  - Qizheng Zhang
  - Changran Hu 
  - Shubhangi Upasani 
  - Boyuan Ma 
  - Fenglu Hong 
  - Vamsidhar Kamanuru 
  - Jay Rainton 
  - Chen Wu 
  - Mengmeng Ji 
  - Hanchen Li 
  - Urmish Thakker 
  - James Zou 
  - Kunle Olukotun
organisation:
  - Stanford University
  - SambaNova Systems, Inc.
  - UC Berkeley
url:
  - https://arxiv.org/abs/2510.04618
tags:
  - Technology
  - Artificial_Intelligence
  - Natural_Language_Processing
  - LLM_Agents
  - Context_Engineering
---
# Agentic Context Engineering: Konteks yang Berevolusi untuk Model Bahasa yang Meningkatkan Diri Sendiri

## Abstrak

Aplikasi model bahasa besar (LLM) seperti agen dan penalaran domain-spesifik semakin mengandalkan adaptasi konteks—memodifikasi input dengan instruksi, strategi, atau bukti, daripada pembaruan bobot. Pendekatan sebelumnya meningkatkan kegunaan tetapi sering menderita bias keringkasan (brevity bias), yang menghilangkan wawasan domain demi ringkasan yang ringkas, dan keruntuhan konteks (context collapse), di mana penulisan ulang iteratif mengikis detail dari waktu ke waktu.

Berdasarkan memori adaptif yang diperkenalkan oleh Dynamic Cheatsheet, kami memperkenalkan ACE (Agentic Context Engineering), sebuah kerangka kerja yang memperlakukan konteks sebagai playbook yang berevolusi yang mengakumulasi, menyempurnakan, dan mengatur strategi melalui proses modular generasi, refleksi, dan kurasi. ACE mencegah keruntuhan dengan pembaruan terstruktur dan inkremental yang melestarikan pengetahuan detail dan diskalakan dengan model konteks panjang.

Di berbagai tolok ukur agen dan domain-spesifik, ACE mengoptimalkan konteks baik secara offline (misalnya, prompt sistem) maupun online (misalnya, memori agen), secara konsisten mengungguli baseline yang kuat: +10,6% pada agen dan +8,6% pada keuangan, sambil secara signifikan mengurangi latensi adaptasi dan biaya rollout. Pentingnya, ACE dapat beradaptasi secara efektif tanpa supervisi berlabel dan sebaliknya dengan memanfaatkan umpan balik eksekusi alami. Pada papan peringkat AppWorld, ACE menyamai agen tingkat produksi peringkat teratas pada rata-rata keseluruhan dan melampauinya pada pemisahan test-challenge yang lebih sulit, meskipun menggunakan model open-source yang lebih kecil. Hasil ini menunjukkan bahwa konteks yang komprehensif dan berevolusi memungkinkan sistem LLM yang diskalakan, efisien, dan meningkatkan diri sendiri dengan overhead rendah.

## 1. Pendahuluan

Aplikasi AI modern berbasis model bahasa besar (LLM), seperti agen LLM dan sistem AI komposit, semakin bergantung pada adaptasi konteks. Alih-alih memodifikasi bobot model, adaptasi konteks meningkatkan kinerja setelah pelatihan model dengan memasukkan instruksi yang dijelaskan, langkah-langkah penalaran terstruktur, atau format input domain-spesifik langsung ke dalam input model. Konteks menjadi dasar bagi banyak komponen sistem AI, termasuk prompt sistem yang memandu tugas hilir, memori yang membawa fakta dan pengalaman masa lalu, dan bukti faktual yang mengurangi halusinasi dan melengkapi pengetahuan.

Berdasarkan konteks daripada bobot menawarkan beberapa keuntungan utama. Konteks dapat diinterpretasikan dan dijelaskan untuk pengguna dan pengembang, memungkinkan integrasi pengetahuan baru secara cepat pada runtime, dan dapat dibagi di berbagai model atau modul dalam sistem komposit. Sementara itu, kemajuan dalam LLM konteks panjang dan inferensi yang efisien secara konteks seperti penggunaan ulang cache KV membuat pendekatan berbasis konteks semakin praktis untuk deployment.

Meskipun ada kemajuan ini, pendekatan yang ada untuk adaptasi konteks menghadapi dua keterbatasan utama:

**Pertama, bias keringkasan**: banyak pengoptimasi prompt memprioritaskan instruksi yang ringkas dan dapat diterapkan secara luas daripada akumulasi yang komprehensif. Abstraksi seperti itu dapat menghilangkan heuristik domain-spesifik, panduan penggunaan alat, atau mode kegagalan umum yang penting dalam praktik.

**Kedua, keruntuhan konteks**: metode yang mengandalkan penulisan ulang monolitik oleh LLM sering terdegradasi menjadi ringkasan yang lebih pendek dan kurang informatif dari waktu ke waktu, menyebabkan penurunan kinerja yang tajam.

Kami berpendapat bahwa konteks harus berfungsi bukan sebagai ringkasan yang ringkas, tetapi sebagai playbook yang komprehensif dan berevolusi—detail, inklusif, dan kaya dengan wawasan domain. Berbeda dengan manusia, yang sering mendapat manfaat dari generalisasi yang ringkas, LLM lebih efektif ketika diberikan konteks yang panjang dan detail dan dapat menyuling relevansi secara otonom.

## 2. Latar Belakang dan Motivasi

### 2.1 Adaptasi Konteks

Adaptasi konteks (atau rekayasa konteks) mengacu pada metode yang meningkatkan perilaku model dengan membangun atau memodifikasi input ke LLM, daripada mengubah bobotnya. State of the art saat ini memanfaatkan umpan balik bahasa alami. Dalam paradigma ini, model bahasa memeriksa konteks saat ini bersama dengan sinyal seperti jejak eksekusi, langkah-langkah penalaran, atau hasil validasi, dan menghasilkan umpan balik bahasa alami tentang bagaimana konteks harus direvisi.

Metode-metode yang representatif meliputi:
- **Reflexion**: merefleksikan kegagalan untuk meningkatkan perencanaan agen
- **TextGrad**: mengoptimalkan prompt melalui umpan balik tekstual seperti gradien
- **GEPA**: menyempurnakan prompt secara iteratif berdasarkan jejak eksekusi
- **Dynamic Cheatsheet**: membangun memori eksternal yang mengakumulasi strategi dan pelajaran dari keberhasilan dan kegagalan masa lalu selama inferensi

### 2.2 Keterbatasan Metode Adaptasi Konteks yang Ada

**Bias Keringkasan (The Brevity Bias)**

Keterbatasan berulang dari metode adaptasi konteks adalah bias keringkasan: kecenderungan optimasi untuk runtuh ke arah prompt yang pendek dan generik. Konvergensi ini tidak hanya menyempitkan ruang pencarian tetapi juga mempropagasi kesalahan berulang.

**Keruntuhan Konteks (Context Collapse)**

Keterbatasan kedua adalah keruntuhan konteks: degradasi konteks menjadi ringkasan yang kurang informatif dari waktu ke waktu. Ketika konteks ditulis ulang secara monolitik oleh LLM tanpa struktur, konteks sering kehilangan informasi penting.

## 3. Metodologi

### 3.1 Kerangka Kerja ACE

ACE (Agentic Context Engineering) adalah kerangka kerja untuk adaptasi konteks komprehensif baik dalam pengaturan offline (misalnya, optimasi prompt sistem) maupun online (misalnya, adaptasi memori pada waktu tes). Alih-alih mengompresi konteks ke dalam ringkasan yang disuling, ACE memperlakukannya sebagai playbook yang berevolusi yang mengakumulasi dan mengatur strategi dari waktu ke waktu.

Berdasarkan arsitektur agentic dari Dynamic Cheatsheet, ACE menggabungkan alur kerja modular generasi, refleksi, dan kurasi, sambil menambahkan pembaruan terstruktur dan inkremental yang dipandu oleh prinsip tumbuh-dan-sempurnakan. Desain ini melestarikan pengetahuan domain-spesifik yang detail, mencegah keruntuhan konteks, dan menghasilkan konteks yang tetap komprehensif dan dapat diskalakan sepanjang adaptasi.

### 3.2 Proses Modular

Kerangka kerja ACE terdiri dari tiga komponen utama:

1. **Generasi**: Membuat strategi dan konten baru berdasarkan input dan tugas
2. **Refleksi**: Mengevaluasi keberhasilan dan kegagalan untuk meningkatkan konteks
3. **Kurasi**: Mengorganisir dan memelihara konteks untuk mencegah keruntuhan

### 3.3 Prinsip Tumbuh-dan-Sempurnakan

ACE menggunakan pembaruan delta inkremental yang terstruktur daripada penulisan ulang monolitik. Pendekatan ini:
- Melestarikan detail yang ada
- Menambahkan pengetahuan baru secara bertahap
- Mencegah hilangnya informasi selama iterasi
- Diskalakan dengan model konteks panjang

## 4. Hasil dan Evaluasi

### 4.1 Tolok Ukur dan Kinerja

ACE dievaluasi pada dua kategori aplikasi LLM yang paling diuntungkan dari konteks yang komprehensif dan berevolusi:

#### Agen (Agents)
- **AppWorld**: Tolok ukur agen yang menantang
- **Peningkatan**: +10,6% dibandingkan baseline yang kuat

#### Penalaran Domain-Spesifik
- **Analisis Keuangan (FiNER)**: Peningkatan +8,6%
- **Penalaran Numerik (Formula)**: Peningkatan signifikan

### 4.2 Hasil pada AppWorld Leaderboard

Pada papan peringkat AppWorld:
- ACE menyamai agen tingkat produksi peringkat teratas (IBM-CUGA yang didukung oleh GPT-4.1) pada rata-rata keseluruhan
- ACE melampaui agen tersebut pada pemisahan test-challenge yang lebih sulit
- ACE menggunakan model open-source yang lebih kecil (DeepSeek-V3.1)

### 4.3 Efisiensi dan Biaya

ACE menunjukkan efisiensi yang luar biasa:
- **Latensi adaptasi**: 86,9% lebih rendah daripada metode adaptif yang ada (rata-rata)
- **Biaya rollout**: Signifikan lebih rendah
- **Jumlah rollout**: Secara signifikan lebih sedikit

### 4.4 Belajar Tanpa Supervisi

Pentingnya, ACE dapat membangun konteks yang efektif tanpa supervisi berlabel, sebaliknya memanfaatkan umpan balik eksekusi dan sinyal lingkungan—bahan kunci untuk LLM dan agen yang meningkatkan diri sendiri.

## 5. Diskusi

### 5.1 Keunggulan ACE

1. **Konteks Komprehensif**: Tidak mengorbankan detail demi keringkasan
2. **Evolusi Terstruktur**: Pembaruan inkremental yang terorganisir
3. **Skalabilitas**: Berfungsi dengan model konteks panjang modern
4. **Efisiensi**: Latensi rendah dan biaya operasional yang minimal
5. **Independensi Supervisi**: Dapat belajar dari umpan balik eksekusi alami

### 5.2 Implikasi untuk Masa Depan

Hasil ini menunjukkan bahwa konteks yang komprehensif dan berevolusi memungkinkan sistem LLM yang diskalakan, efisien, dan meningkatkan diri sendiri dengan overhead rendah. Pendekatan ini membuka jalan bagi:
- Agen AI yang lebih mampu dan andal
- Integrasi pengetahuan domain yang lebih baik
- Sistem yang dapat beradaptasi secara kontinu tanpa pelatihan ulang
- Pengurangan biaya dan latensi untuk aplikasi AI praktis

## 6. Kesimpulan

ACE (Agentic Context Engineering) mewakili kemajuan signifikan dalam adaptasi konteks untuk model bahasa besar. Dengan memperlakukan konteks sebagai playbook yang berevolusi daripada ringkasan statis, ACE mengatasi keterbatasan fundamental dari pendekatan yang ada: bias keringkasan dan keruntuhan konteks.

Melalui proses modular generasi, refleksi, dan kurasi, dengan pembaruan inkremental yang terstruktur, ACE mampu:
- Mencapai peningkatan kinerja signifikan (+10,6% pada agen, +8,6% pada keuangan)
- Mengoperasikan dengan latensi yang jauh lebih rendah (86,9% pengurangan)
- Beradaptasi tanpa supervisi berlabel menggunakan umpan balik eksekusi
- Bersaing dengan agen tingkat produksi pada tolok ukur yang menantang

Pendekatan ini menunjukkan bahwa konteks yang komprehensif dan terstruktur, yang berevolusi dari waktu ke waktu, adalah kunci untuk membangun sistem LLM yang benar-benar mampu meningkatkan diri sendiri dengan overhead minimal.

## Daftar Pustaka

1. General Data Protection Regulation article 17: Right to erasure. EU Regulation 2016/679, 2016. Official consolidated text.

2. California consumer privacy act, civil code §1798.105: Right to delete. State of California Civil Code, 2018.

3. Rishabh Agarwal, Avi Singh, Lei Zhang, Bernd Bohnet, Luis Rosias, Stephanie Chan, Biao Zhang, Ankesh Anand, Zaheer Abbas, Azade Nova, et al. Many-shot in-context learning. Advances in Neural Information Processing Systems, 37:76930–76966, 2024.

4. Lakshya A Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J Ryan, Meng Jiang, et al. Gepa: Reflective prompt evolution can outperform reinforcement learning. arXiv preprint arXiv:2507.19457, 2025.

5. AppWorld. Leaderboard. https://appworld.dev/leaderboard, 2025. Accessed: 2025-09-20.

6. Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-rag: Learning to retrieve, generate, and critique through self-reflection. 2024.

7. Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al. Improving language models by retrieving from trillions of tokens. In International conference on machine learning, pages 2206–2240. PMLR, 2022.

8. Lucas Bourtoule, Varun Chandrasekaran, Christopher Choquette-Choo, Hengrui Jia, Adelin Travers, Baiwu Zhang, David Lie, and Nicolas Papernot. Machine unlearning. IEEE Symposium on Security and Privacy, pages 141–159, 2021.

9. Tom Brown et al. Language models are few-shot learners. In NeurIPS, 2020.

10. Yinzhi Cao and Junfeng Yang. Towards making systems forget with machine unlearning. In IEEE Symposium on Security and Privacy, 2015.

11. Tianxiang Chen, Zhentao Tan, Xiaofan Bo, Yue Wu, Tao Gong, Qi Chu, Jieping Ye, and Nenghai Yu. Flora: Effortless context construction to arbitrary length and scale. arXiv preprint arXiv:2507.19786, 2025.

12. Yeounoh Chung, Gaurav T Kakkar, Yu Gan, Brenton Milne, and Fatma Ozcan. Is long context all you need? leveraging llm's extended context for nl2sql. arXiv preprint arXiv:2501.12372, 2025.

13. DeepSeek-AI. Deepseek-v3 technical report, 2024.

14. DSPy. dspy.gepa: Reflective prompt optimizer. https://dspy.ai/api/optimizers/GEPA/overview/, 2025. Accessed: 2025-09-24.

15. DSPy. dspy.miprov2. https://dspy.ai/api/optimizers/MIPROv2/, 2025. Accessed: 2025-09-24.

16. Shuzheng Gao, Chaozheng Wang, Cuiyun Gao, Xiaoqian Jiao, Chun Yong Chong, Shan Gao, and Michael Lyu. The prompt alchemist: Automated llm-tailored prompt optimization for test case generation. arXiv preprint arXiv:2501.01329, 2025.

17. In Gim, Guojun Chen, Seung-seob Lee, Nikhil Sarda, Anurag Khandelwal, and Lin Zhong. Prompt cache: Modular attention reuse for low-latency inference. Proceedings of Machine Learning and Systems, 6:325–338, 2024.

18. Neel Guha, Julian Nyarko, Daniel Ho, Christopher Ré, Adam Chilton, Alex Chohlas-Wood, Austin Peters, Brandon Waldon, Daniel Rockmore, Diego Zambrano, et al. Legalbench: A collaboratively built benchmark for measuring legal reasoning in large language models. Advances in neural information processing systems, 36:44123–44279, 2023.

19. Ishaan Gulrajani and David Lopez-Paz. In search of lost domain generalization. In ICLR, 2021.

20. Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. arXiv:2106.09685, 2021.

21. Maxwell L Hutchinson, Erin Antono, Brenna M Gibbons, Sean Paradiso, Julia Ling, and Bryce Meredig. Overcoming data scarcity with transfer learning. arXiv preprint arXiv:1711.05099, 2017.

22. Mingjian Jiang, Yangjun Ruan, Luis Lastras, Pavan Kapanipathi, and Tatsunori Hashimoto. Putting it all into context: Simplifying agents with lclms. arXiv preprint arXiv:2505.08120, 2025.

23. Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, and Ashish Sabharwal. Decomposed prompting: A modular approach for solving complex tasks. arXiv preprint arXiv:2210.02406, 2022.

24. Pang Wei Koh, Shiori Sagawa, Henrik Marklund, Sang Michael Xie, Marvin Zhang, Akshay Balsubramani, Weihua Hu, Michihiro Yasunaga, Richard Lanas Phillips, Irena Gao, et al. Wilds: A benchmark of in-the-wild distribution shifts. In International conference on machine learning, pages 5637–5664. PMLR, 2021.

25. Wonbeom Lee, Jungi Lee, Junghwan Seo, and Jaewoong Sim. {InfiniGen}: Efficient generative inference of large language models with dynamic {KV} cache management. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 155–172, 2024.

26. Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. In EMNLP, 2021.

27. Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in neural information processing systems, 33:9459–9474, 2020.

28. Xiang Lisa Li and Percy Liang. Prefix-tuning: Optimizing continuous prompts for generation. ACL, 2021.

29. Shiyang Liu et al. Rethinking machine unlearning for large language models. arXiv:2402.08787, 2024.

30. Yuhan Liu, Hanchen Li, Yihua Cheng, Siddhant Ray, Yuyang Huang, Qizheng Zhang, Kuntai Du, Jiayi Yao, Shan Lu, Ganesh Ananthanarayanan, et al. Cachegen: Kv cache compression and streaming for fast large language model serving. In Proceedings of the ACM SIGCOMM 2024 Conference, pages 38–56, 2024.

31. Zhining Liu, Rana Ali Amjad, Ravinarayana Adkathimar, Tianxin Wei, and Hanghang Tong. Selfelicit: Your language model secretly knows where is the relevant evidence. arXiv preprint arXiv:2502.08767, 2025.

32. Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman, Beidi Chen, and Xia Hu. Kivi: A tuning-free asymmetric 2bit quantization for kv cache. arXiv preprint arXiv:2402.02750, 2024.

33. Lefteris Loukas, Manos Fergadiotis, Ilias Chalkidis, Eirini Spyropoulou, Prodromos Malakasiotis, Ion Androutsopoulos, and Georgios Paliouras. Finer: Financial numeric entity recognition for xbrl tagging. arXiv preprint arXiv:2203.06482, 2022.

34. Yansheng Mao, Jiaqi Li, Fanxu Meng, Jing Xiong, Zilong Zheng, and Muhan Zhang. Lift: Improving long context understanding through long input fine-tuning. arXiv preprint arXiv:2412.13626, 2024.

35. Sami Marreed, Alon Oved, Avi Yaeli, Segev Shlomov, Ido Levy, Offer Akrabi, Aviad Sela, Asaf Adi, and Nir Mashkif. Towards enterprise-ready computer using generalist agent. arXiv preprint arXiv:2503.01861, 2025.

36. Krista Opsahl-Ong, Michael J Ryan, Josh Purtell, David Broman, Christopher Potts, Matei Zaharia, and Omar Khattab. Optimizing instructions and demonstrations for multi-stage language model programs. arXiv preprint arXiv:2406.11695, 2024.

37. Sinno Jialin Pan and Qiang Yang. A survey on transfer learning. IEEE Transactions on Knowledge and Data Engineering, 22(10):1345–1359, 2010.

38. Shishir G Patil, Tianjun Zhang, Xin Wang, and Joseph E Gonzalez. Gorilla: Large language model connected with massive apis. Advances in Neural Information Processing Systems, 37:126544–126565, 2024.

39. Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole. Yarn: Efficient context window extension of large language models. arXiv preprint arXiv:2309.00071, 2023.

40. Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36:8634–8652, 2023.

41. Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. Dynamic cheatsheet: Test-time learning with adaptive memory. arXiv preprint arXiv:2504.07952, 2025.

42. Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. Dynamic cheatsheet: Test-time learning with adaptive memory. https://github.com/suzgunmirac/dynamic-cheatsheet, 2025. Accessed: 2025-09-24.

43. Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, and Niranjan Balasubramanian. Appworld: A controllable world of apps and people for benchmarking interactive coding agents. arXiv preprint arXiv:2407.18901, 2024.

44. Dannong Wang, Jaisal Patel, Daochen Zha, Steve Y Yang, and Xiao-Yang Liu. Finlora: Benchmarking lora methods for fine-tuning llms on financial datasets. arXiv preprint arXiv:2505.19819, 2025.

45. Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. arXiv preprint arXiv:2203.11171, 2022.

46. Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. Agent workflow memory. arXiv preprint arXiv:2409.07429, 2024.

47. Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837, 2022.

48. Wujiang Xu, Kai Mei, Hang Gao, Juntao Tan, Zujie Liang, and Yongfeng Zhang. A-mem: Agentic memory for llm agents. arXiv preprint arXiv:2502.12110, 2025.

49. John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. Swe-agent: Agent-computer interfaces enable automated software engineering. Advances in Neural Information Processing Systems, 37:50528–50652, 2024.

50. Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering. arXiv preprint arXiv:1809.09600, 2018.

51. Jiayi Yao, Hanchen Li, Yuhan Liu, Siddhant Ray, Yihua Cheng, Qizheng Zhang, Kuntai Du, Shan Lu, and Junchen Jiang. Cacheblend: Fast large language model serving for rag with cached knowledge fusion. In Proceedings of the Twentieth European Conference on Computer Systems, pages 94–109, 2025.

52. Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In International Conference on Learning Representations (ICLR), 2023.

53. Jiacheng Ye, Chengzu Li, Lingpeng Kong, and Tao Yu. Generating data for symbolic language with large language models. arXiv preprint arXiv:2305.13917, 2023.

54. Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Zhi Huang, Carlos Guestrin, and James Zou. Textgrad: Automatic" differentiation" via text. arXiv preprint arXiv:2406.07496, 2024.

55. Matei Zaharia, Omar Khattab, Lingjiao Chen, Jared Quincy Davis, Heather Miller, Chris Potts, James Zou, Michael Carbin, Jonathan Frankle, Naveen Rao, and Ali Ghodsi. The shift from models to compound ai systems. https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/, 2024.

56. Genghan Zhang, Weixin Liang, Olivia Hsu, and Kunle Olukotun. Adaptive self-improvement llm agentic system for ml library development. arXiv preprint arXiv:2502.02534, 2025.

57. Qizheng Zhang, Ali Imran, Enkeleda Bardhi, Tushar Swamy, Nathan Zhang, Muhammad Shahbaz, and Kunle Olukotun. Caravan: Practical online learning of {In-Network}{ML} models with labeling agents. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 325–345, 2024.

58. Qizheng Zhang, Michael Wornow, and Kunle Olukotun. Cost-efficient serving of llm agents via test-time plan caching. arXiv preprint arXiv:2506.14852, 2025.

59. Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan, Kin Hei Lee, Zihan Wang, Ka Yiu Lee, Guchun Zhang, Kun Shao, Linyi Yang, et al. Agentfly: Fine-tuning llm agents without fine-tuning llms. arXiv preprint arXiv:2508.16153, 2025.

60. Fuzhen Zhuang, Zhiyuan Qi, Keyu Duan, Dongbo Xi, Yongchun Zhu, Hengshu Zhu, Hui Xiong, and Qing He. A comprehensive survey on transfer learning. arXiv:1911.02685, 2019.

---

**Referensi**: arXiv:2510.04618v1 [cs.LG] 6 Oct 2025

**Kontak**: qizhengz@stanford.edu, changran.hu@sambanovasystems.com
