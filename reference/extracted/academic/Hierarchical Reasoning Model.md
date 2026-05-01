---
date: 2025-08-04
researcher:
  - Guan Wang
  - Jin Li
  - Yuhao Sun 
  - Xing Chen
  - Changling Liu
  - Yue Wu
  - Meng Lu
  - Sen Song
  - Yasin Abbasi Yadkori
organisation:
  - Sapient Intelligence, Singapore
  - Tsinghua University
url:
  - https://arxiv.org/abs/2506.21734
tags:
  - Technology
  - Artificial_Intelligence
  - Deep_Learning
  - Neural_Networks
  - Computational_Neuroscience
---
# Model Penalaran Hirarkis (Hierarchical Reasoning Model)

## Abstrak

Penalaran, sebagai proses merancang dan mengeksekusi urutan tindakan yang kompleks dan berorientasi pada tujuan, tetap menjadi tantangan kritis dalam kecerdasan buatan (AI). Model bahasa besar (LLM) saat ini terutama menggunakan teknik Chain-of-Thought (CoT) yang mengalami masalah dekomposisi tugas yang rapuh, kebutuhan data yang ekstensif, dan latensi tinggi.

Terinspirasi oleh pemrosesan hirarkis dan multi-timescale dalam otak manusia, kami mengusulkan Model Penalaran Hirarkis (HRM), arsitektur rekuren yang memperoleh kedalaman komputasi yang signifikan sambil mempertahankan stabilitas dan efisiensi pelatihan. HRM mengeksekusi tugas penalaran sekuensial dalam satu forward pass tanpa supervisi eksplisit pada proses perantara, melalui dua modul rekuren yang saling bergantung:

- **Modul tingkat tinggi**: Bertanggung jawab untuk perencanaan abstrak yang lambat
- **Modul tingkat rendah**: Menangani komputasi cepat dan detail

Dengan hanya 27 juta parameter, HRM mencapai kinerja luar biasa pada tugas penalaran kompleks menggunakan hanya 1000 sampel pelatihan. Model ini beroperasi tanpa pra-pelatihan atau data CoT, namun mencapai kinerja hampir sempurna pada tugas menantang termasuk teka-teki Sudoku kompleks dan pencarian jalur optimal dalam labirin besar. Selanjutnya, HRM mengungguli model yang jauh lebih besar dengan jendela konteks yang jauh lebih panjang pada Abstraction and Reasoning Corpus (ARC), tolok ukur kunci untuk mengukur kemampuan kecerdasan umum buatan.

## 1. Pendahuluan

Deep learning, sesuai namanya, muncul dari gagasan menumpuk lebih banyak lapisan untuk mencapai peningkatan kekuatan representasi dan kinerja yang lebih baik. Namun demikian, meskipun keberhasilan luar biasa dari model bahasa besar, arsitektur intinya secara paradoks dangkal. Hal ini memberikan batasan fundamental pada kemampuan yang paling dicari: penalaran.

Kedalaman tetap dari Transformer standar menempatkannya dalam kelas kompleksitas komputasi seperti AC^0 atau TC^0, yang mencegahnya menyelesaikan masalah yang memerlukan waktu polinomial. LLM tidak Turing-lengkap dan dengan demikian tidak dapat, setidaknya secara murni end-to-end, mengeksekusi penalaran algoritmik kompleks yang diperlukan untuk perencanaan yang sengaja atau tugas manipulasi simbolik.

Literatur LLM sebagian besar mengandalkan Chain-of-Thought (CoT) prompting untuk penalaran. CoT meng eksternalisasi penalaran ke dalam bahasa tingkat token dengan memecah tugas kompleks menjadi langkah-langkah perantara yang lebih sederhana, menghasilkan teks secara sekuensial menggunakan model yang dangkal. Namun, CoT untuk penalaran adalah penopang, bukan solusi yang memuaskan. Ia bergantung pada dekomposisi yang rapuh dan didefinisikan manusia di mana satu langkah salah atau urutan langkah yang salah dapat menggagalkan seluruh proses penalaran.

Pendekatan yang lebih efisien diperlukan untuk meminimalkan kebutuhan data ini. Menuju tujuan ini, kami mengeksplorasi "penalaran laten", di mana model melakukan komputasi dalam ruang keadaan tersembunyinya. Hal ini selaras dengan pemahaman bahwa bahasa adalah alat untuk komunikasi manusia, bukan substrat dari pemikiran itu sendiri; otak mempertahankan rantai penalaran yang panjang dan koheren dengan efisiensi luar biasa dalam ruang laten, tanpa terjemahan konstan kembali ke bahasa.

Otak manusia menyediakan cetak biru yang menarik untuk mencapai kedalaman komputasi efektif yang kurang dimiliki oleh model buatan kontemporer. Ia mengatur komputasi secara hirarkis di seluruh wilayah kortikal yang beroperasi pada timescales yang berbeda, memungkinkan penalaran multi-tahap yang mendalam. Loop umpan balik rekuren secara iteratif menyempurnakan representasi internal, memungkinkan area tingkat tinggi yang lambat untuk memandu, dan sirkuit tingkat rendah yang cepat untuk mengeksekusi—pemrosesan bawahan sambil mempertahankan koherensi global.

Terinspirasi oleh arsitektur biologis hirarkis dan multi-timescale ini, kami mengusulkan Model Penalaran Hirarkis (HRM). HRM dirancang untuk secara signifikan meningkatkan kedalaman komputasi efektif. Ia memiliki dua modul rekuren yang digabungkan: modul tingkat tinggi (H) untuk penalaran abstrak dan sengaja, dan modul tingkat rendah (L) untuk komputasi cepat dan detail.

## 2. Metodologi

### 2.1 Arsitektur HRM

HRM mengeksekusi tugas penalaran sekuensial dalam satu forward pass tanpa supervisi eksplisit pada proses perantara. Arsitektur ini terdiri dari:

**Modul Tingkat Tinggi (H)**
- Bertanggung jawab untuk perencanaan abstrak yang lambat
- Mengoperasikan pada timescale yang lebih lambat
- Menangani pemrosesan abstrak dan perencanaan strategis

**Modul Tingkat Rendah (L)**
- Menangani komputasi cepat dan detail
- Mengoperasikan pada timescale yang lebih cepat
- Menangani eksekusi operasional dan pemrosesan detail

Kedua modul ini saling bergantung dan bekerja sama untuk menyelesaikan tugas penalaran kompleks.

### 2.2 Karakteristik Utama

| Karakteristik | Spesifikasi |
|---------------|-------------|
| Jumlah Parameter | 27 juta |
| Sampel Pelatihan | ~1000 per tugas |
| Pra-pelatihan | Tidak diperlukan |
| Data CoT | Tidak diperlukan |
| Forward Pass | Tunggal |

## 3. Hasil dan Evaluasi

### 3.1 Tolok Ukur Kinerja

HRM dievaluasi pada beberapa tolok ukur standar:

#### ARC-AGI (Abstraction and Reasoning Corpus)
- **ARC-AGI-1**: 960 contoh pelatihan
- **ARC-AGI-2**: 1120 contoh pelatihan

#### Sudoku-Extreme (9x9)
- 1000 contoh pelatihan

#### Maze-Hard (30x30)
- 1000 contoh pelatihan

### 3.2 Perbandingan Kinerja

HRM dengan hanya ~27M parameter dan pelatihan langsung dari input tanpa chain of thoughts, berhasil mengungguli model state-of-the-art CoT pada tolok ukur induktif (ARC-AGI) dan teka-teki pencarian pohon simbolik yang menantang (Sudoku-Extreme, Maze-Hard) di mana model CoT gagal sepenuhnya.

#### Hasil pada ARC-AGI-1
- HRM: 21.2%
- Claude 3.7 8K: 15.8%
- o3-mini-high: 21.0%
- Deepseek R1: 34.5%

#### Hasil pada ARC-AGI-2
- HRM: 40.3%
- Claude 3.7 8K: 0.9%
- o3-mini-high: 1.3%
- Deepseek R1: 5.0%

#### Hasil pada Sudoku-Extreme (9x9)
- HRM: 55.0%
- Claude 3.7 8K: 0.0%
- o3-mini-high: 0.0%
- Deepseek R1: 0.0%

#### Hasil pada Maze-Hard (30x30)
- HRM: 74.5%
- Claude 3.7 8K: 0.0%
- o3-mini-high: 0.0%
- Deepseek R1: 0.0%

## 4. Diskusi

### 4.1 Keunggulan HRM

1. **Efisiensi Data**: Dengan hanya 1000 sampel pelatihan, HRM mencapai kinerja yang luar biasa
2. **Efisiensi Parameter**: Hanya 27 juta parameter, jauh lebih sedikit dibandingkan model LLM modern
3. **Tanpa Pra-pelatihan**: Model dapat dilatih dari awal tanpa memerlukan pra-pelatihan besar
4. **Forward Pass Tunggal**: Menghilangkan kebutuhan untuk menghasilkan rantai pemikiran yang panjang
5. **Stabilitas Pelatihan**: Mempertahankan stabilitas pelatihan meskipun memiliki kedalaman komputasi yang signifikan

### 4.2 Implikasi untuk AI

Hasil ini menggarisbawahi potensi HRM sebagai kemajuan transformatif menuju komputasi universal dan sistem penalaran tujuan umum. Dengan meniru pemrosesan hirarkis dan multi-timescale dalam otak manusia, HRM menunjukkan bahwa pendekatan yang lebih mirip biologi dapat mengatasi keterbatasan fundamental dari arsitektur Transformer yang dangkal.

## 5. Kesimpulan

Model Penalaran Hirarkis (HRM) mewakili kemajuan signifikan dalam bidang penalaran AI. Dengan menggabungkan dua modul rekuren yang beroperasi pada timescales berbeda—satu untuk perencanaan abstrak dan satu untuk komputasi detail—HRM mencapai kedalaman komputasi yang signifikan sambil mempertahankan stabilitas dan efisiensi pelatihan.

Kinerja yang dicapai pada tolok ukur yang menantang seperti ARC-AGI, Sudoku-Extreme, dan Maze-Hard, terutama dengan sumber daya yang minimal (27 juta parameter dan 1000 sampel pelatihan), menunjukkan potensi besar dari pendekatan ini. HRM mengungguli model yang jauh lebih besar pada tugas-tugas ini, menunjukkan bahwa efisiensi dan desain arsitektur yang tepat dapat lebih penting daripada sekadar penskalaan ukuran model.

Kode tersedia di: [github.com/sapientinc/HRM](https://github.com/sapientinc/HRM)

## Daftar Pustaka

1. Ian Goodfellow, Yoshua Bengio, and Aaron Courville. Deep Learning. MIT Press, 2016.
2. Kaiming He, X. Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 770–778, 2015.
3. Lena Strobl. Average-hard attention transformers are constant-depth uniform threshold circuits, 2023.
4. Tom Bylander. Complexity results for planning. In Proceedings of the 12th International Joint Conference on Artificial Intelligence - Volume 1, IJCAI'91, page 274–279, San Francisco, CA, USA, 1991.
5. William Merrill and Ashish Sabharwal. A logic for expressing log-precision transformers. In Neural Information Processing Systems, 2023.
6. David Chiang. Transformers in DLOGTIME-uniform TC0. Transactions on Machine Learning Research, 2025.
7. Lucas Lehnert, Sainbayar Sukhbaatar, DiJia Su, Qinqing Zheng, Paul McVay, Michael Rabbat, and Yuandong Tian. Beyond a*: Better planning with transformers via search dynamics bootstrapping. In First Conference on Language Modeling, 2024.
8. Wilfried Bounsi, Borja Ibarz, Andrew Dudzik, Jessica B. Hamrick, Larisa Markeeva, Alex Vitvitskyi, Razvan Pascanu, and Petar Velivckovi'c. Transformers meet neural algorithmic reasoners. ArXiv, abs/2406.09308, 2024.
9. William Merrill and Ashish Sabharwal. The parallelism tradeoff: Limitations of log-precision transformers. Transactions of the Association for Computational Linguistics, 11:531–545, 2023.
10. Jason Wei, Yi Tay, et al. Chain-of-thought prompting elicits reasoning in large language models, 2022. arXiv preprint arXiv:2201.11903.
11. William Merrill and Ashish Sabharwal. The expressive power of transformers with chain of thought. In ICLR, 2024.
12. Xinyun Chen, Ryan A. Chi, Xuezhi Wang, and Denny Zhou. Premise order matters in reasoning with large language models. ArXiv, abs/2402.08939, 2024.
13. Rongwu Xu, Zehan Qi, and Wei Xu. Preemptive answer "attacks" on chain-of-thought reasoning. In Annual Meeting of the Association for Computational Linguistics, 2024.
14. Pablo Villalobos, Anson Ho, Jaime Sevilla, Tamay Besiroglu, Lennart Heim, and Marius Hobbhahn. Will we run out of data? limits of llm scaling based on human-generated data. arXiv preprint arXiv:2211.04325, 2022.
15. Xinghao Chen, Anhao Zhao, Heming Xia, Xuan Lu, Hanlin Wang, Yanjun Chen, Wei Zhang, Jian Wang, Wenjie Li, and Xiaoyu Shen. Reasoning beyond language: A comprehensive survey on latent chain-of-thought reasoning, 2025.
16. Xuan Shen, Yizhou Wang, Xiangxi Shi, Yanzhi Wang, Pu Zhao, and Jiuxiang Gu. Training large language models to reason in a continuous latent space. arXiv preprint arXiv:2412.07423, 2024.
17. Evelina Fedorenko, Steven T Piantadosi, and Edward AF Gibson. Language is primarily a tool for communication rather than thought. Nature, 630(8017):575–586, 2024.
18. Hongyu Wang, Shuming Ma, Li Dong, Shaohan Huang, Dongdong Zhang, and Furu Wei. Deepnet: Scaling transformers to 1,000 layers. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024.
19. Timothy P Lillicrap and Adam Santoro. Backpropagation through time and the brain. Current Opinion in Neurobiology, 55:82–89, 2019.
20. John D Murray, Alberto Bernacchia, David J Freedman, Ranulfo Romo, Jonathan D Wallis, Xinying Cai, Camillo Padoa-Schioppa, Tatiana Pasternak, Hyojung Seo, Daeyeol Lee, et al. A hierarchy of intrinsic timescales across primate cortex. Nature neuroscience, 17(12):1661–1663, 2014.
21. Roxana Zeraati, Yan-Liang Shi, Nicholas A Steinmetz, Marc A Gieselmann, Alexander Thiele, Tirin Moore, Anna Levina, and Tatiana A Engel. Intrinsic timescales in the visual cortex change with selective attention and reflect spatial connectivity. Nature communications, 14(1):1858, 2023.
22. Julia M Huntenburg, Pierre-Louis Bazin, and Daniel S Margulies. Large-scale gradients in human cortical organization. Trends in cognitive sciences, 22(1):21–31, 2018.
23. Victor AF Lamme and Pieter R Roelfsema. The distinct modes of vision offered by feedforward and recurrent processing. Trends in neurosciences, 23(11):571–579, 2000.
24. Andre M Bastos, W Martin Usrey, Rick A Adams, George R Mangun, Pascal Fries, and Karl J Friston. Canonical microcircuits for predictive coding. Neuron, 76(4):695–711, 2012.
25. Klara Kaleb, Barbara Feulner, Juan Gallego, and Claudia Clopath. Feedback control guides credit assignment in recurrent neural networks. Advances in Neural Information Processing Systems, 37:5122–5144, 2024.
26. Timothy P Lillicrap, Adam Santoro, Luke Marris, Colin J Akerman, and Geoffrey Hinton. Backpropagation and the brain. Nature Reviews Neuroscience, 21(6):335–346, 2020.
27. François Chollet. On the measure of intelligence (abstraction and reasoning corpus), 2019. arXiv preprint arXiv:1911.01547.
28. Francois Chollet, Mike Knoop, Gregory Kamradt, and Bryan Landers. Arc prize 2024: Technical report. ArXiv, abs/2412.04604, 2024.
29. Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers, and Henry Pinkard. Arc-agi-2: A new challenge for frontier ai reasoning systems. arXiv preprint arXiv:2505.11831, 2025.
30. György Buzsáki. Gamma, alpha, delta, and theta oscillations govern cognitive processes. International Journal of Psychophysiology, 39:241–248, 2000.
31. György Buzsáki. Rhythms of the Brain. Oxford university press, 2006.
32. Anja Pahor and Norbert Jaušovec. Theta–gamma cross-frequency coupling relates to the level of human intelligence. Intelligence, 46:283–290, 2014.
33. Adriano BL Tort, Robert W Komorowski, Joseph R Manns, Nancy J Kopell, and Howard Eichenbaum. Theta–gamma coupling increases during the learning of item–context associations. Proceedings of the National Academy of Sciences, 106(49):20942–20947, 2009.
34. Benjamin Scellier and Yoshua Bengio. Equilibrium propagation: Bridging the gap between energy-based models and backpropagation. Frontiers in Computational Neuroscience, 11, 2016.
35. Guillaume Bellec, Franz Scherr, Anand Subramoney, Elias Hajek, Darjan Salaj, Robert Legenstein, and Wolfgang Maass. A solution to the learning dilemma for recurrent networks of spiking neurons. Nature Communications, 11, 07 2020.
36. Shaojie Bai, J Zico Kolter, and Vladlen Koltun. Deep equilibrium models. In Advances in Neural Information Processing Systems, pages 690–701, 2019.
37. Zhengyang Geng, Xinyu Zhang, Shaojie Bai, Yisen Wang, and Zhouchen Lin. On training implicit models. ArXiv, abs/2111.05177, 2021.
38. Katarina Begus and Elizabeth Bonawitz. The rhythm of learning: Theta oscillations as an index of active learning in infancy. Developmental Cognitive Neuroscience, 45:100810, 2020.
39. Shaojie Bai, Zhengyang Geng, Yash Savani, and J. Zico Kolter. Deep Equilibrium Optical Flow Estimation. In 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 610–620, 2022.
40. Zaccharie Ramzi, Florian Mannel, Shaojie Bai, Jean-Luc Starck, Philippe Ciuciu, and Thomas Moreau. Shine: Sharing the inverse estimate from the forward pass for bi-level optimization and implicit models. ArXiv, abs/2106.00553, 2021.
41. Shaojie Bai, Vladlen Koltun, and J. Zico Kolter. Stabilizing equilibrium models by jacobian regularization. In International Conference on Machine Learning, 2021.
42. Daniel Kahneman and P Egan. Thinking, fast and slow (farrar, straus and giroux, new york), 2011.
43. Matthew D Lieberman. Social cognitive neuroscience: a review of core processes. Annu. Rev. Psychol., 58(1):259–289, 2007.
44. Randy L Buckner, Jessica R Andrews-Hanna, and Daniel L Schacter. The brain's default network: anatomy, function, and relevance to disease. Annals of the new York Academy of Sciences, 1124(1):1–38, 2008.
45. Marcus E Raichle. The brain's default mode network. Annual review of neuroscience, 38(1):433–447, 2015.
46. Andrew Westbrook and Todd S Braver. Cognitive effort: A neuroeconomic approach. Cognitive, Affective, & Behavioral Neuroscience, 15:395–415, 2015.
47. Richard S. Sutton and Andrew G. Barto. Reinforcement Learning: An Introduction. MIT Press, Cambridge, MA, 2018.
48. Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis Antonoglou, Daan Wierstra, and Martin A. Riedmiller. Playing atari with deep reinforcement learning. ArXiv, abs/1312.5602, 2013.
49. Matteo Gallici, Mattie Fellows, Benjamin Ellis, Bartomeu Pou, Ivan Masmitja, Jakob Nicolaus Foerster, and Mario Martin. Simplifying deep temporal difference learning, 2025.
50. Shuo Xie and Zhiyuan Li. Implicit bias of adamw: L inf norm constrained optimization. ArXiv, abs/2404.04454, 2024.
51. Lucas Prieto, Melih Barsbey, Pedro A. M. Mediano, and Tolga Birdal. Grokking at the edge of numerical stability. In The Thirteenth International Conference on Learning Representations, 2025.
52. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in neural information processing systems, pages 5998–6008, 2017.
53. Meta AI. Llama 3: State-of-the-art open weight language models. Technical report, Meta, 2024.
54. Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer: Enhanced transformer with rotary position embedding. Neurocomputing, 568:127063, 2024.
55. Noam M. Shazeer. Glu variants improve transformer. ArXiv, abs/2002.05202, 2020.
56. Biao Zhang and Rico Sennrich. Root mean square layer normalization. ArXiv, abs/1910.07467, 2019.
57. Günter Klambauer, Thomas Unterthiner, Andreas Mayr, and Sepp Hochreiter. Self-normalizing neural networks. In Neural Information Processing Systems, 2017.
58. JAX Developers. jax.nn.initializers.lecun_normal. Google Research, 2025.
59. Yann LeCun, Léon Bottou, Genevieve B Orr, and Klaus-Robert Müller. Efficient backprop. In Neural networks: Tricks of the trade, pages 9–50. Springer, 2002.
60. Katie E Everett, Lechao Xiao, Mitchell Wortsman, Alexander A Alemi, Roman Novak, Peter J Liu, Izzeddin Gur, Jascha Sohl-Dickstein, Leslie Pack Kaelbling, Jaehoon Lee, and Jeffrey Pennington. Scaling exponents across parameterizations and optimizers. In Forty-first International Conference on Machine Learning, 2024.
61. Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization, 2017.
62. Rasmus Berg Palm, Ulrich Paquet, and Ole Winther. Recurrent relational networks. In Neural Information Processing Systems, 2017.
63. Jieyi Long. Large language model guided tree-of-thought. ArXiv, abs/2305.08291, 2023.
64. Yilun Du, Jiayuan Mao, and Josh Tenenbaum. Learning iterative reasoning through energy diffusion. ArXiv, abs/2406.11179, 2024.
65. Kyubyong Park. Can convolutional neural networks crack sudoku puzzles? https://github.com/Kyubyong/sudoku, 2018.
66. Single-digit techniques. https://hodoku.sourceforge.net/en/tech_singles.php. Accessed: 2025-06-16.
67. Tom Dillion. Tdoku: A fast sudoku solver and generator. https://t-dillon.github.io/tdoku/, 2025.
68. Jeffrey Seely, Yuki Imajuku, Tianyu Zhao, Edoardo Cetin, and Llion Jones. Sudoku-bench: Evaluating creative reasoning with sudoku variants. arXiv preprint arXiv:2505.16135, 2025.
69. Luke Darlow, Ciaran Regan, Sebastian Risi, Jeffrey Seely, and Llion Jones. Continuous thought machines. arXiv preprint arXiv:2505.05522, 2025.
70. DiJia Su, Sainbayar Sukhbaatar, Michael Rabbat, Yuandong Tian, and Qinqing Zheng. Dualformer: Controllable fast and slow thinking by learning with randomized reasoning traces, 2025.
71. Lucas Lehnert, Sainbayar Sukhbaatar, DiJia Su, Qinqing Zheng, Paul McVay, Michael Rabbat, and Yuandong Tian. Beyond a*: Better planning with transformers via search dynamics bootstrapping. In First Conference on Language Modeling, 2024.
72. Mubbasir Kapadia, Francisco Garcia, Cory D. Boatright, and Norman I. Badler. Dynamic search on the gpu. In 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 3332–3337, 2013.
73. Isaac Liao and Albert Gu. Arc-agi without pretraining, 2025.
74. Lorenzo Posani, Shuqi Wang, Samuel P Muscinelli, Liam Paninski, and Stefano Fusi. Rarely categorical, always high-dimensional: how the neural code changes along the cortical hierarchy. bioRxiv, pages 2024–11, 2025.
75. Mattia Rigotti, Omri Barak, Melissa R. Warden, Xiao-Jing Wang, Nathaniel D. Daw, Earl K. Miller, and Stefano Fusi. The importance of mixed selectivity in complex cognitive tasks. Nature, 497:585–590, 2013.
76. Valerio Mante, David Sussillo, Krishna V. Shenoy, and William T. Newsome. Context-dependent computation by recurrent dynamics in prefrontal cortex. Nature, 503(7474):78–84, 2013.
77. Earl K. Miller and Jonathan D. Cohen. An integrative theory of prefrontal cortex function. Annual Review of Neuroscience, 24(1):167–202, 2001.
78. Wolfgang Maass. Real-time computing without stable states: a new framework for neural computation based on perturbations. Neural Computation, 14(11):2531–2560, 2002.
79. Ege Altan, Sara A. Solla, Lee E. Miller, and Eric J. Perreault. Estimating the dimensionality of the manifold underlying multi-electrode neural recordings. PLoS Computational Biology, 17(11):e1008591, 2021.
80. Vardan Papyan, X. Y. Han, and David L. Donoho. Prevalence of neural collapse during the terminal phase of deep learning training. Proceedings of the National Academy of Sciences, 117(40):24652–24663, 2020.
81. Cong Fang, Hangfeng He, Qi Long, and Weijie J. Su. Exploring deep neural networks via layer–peeled model: Minority collapse in imbalanced training. Proceedings of the National Academy of Sciences, 118(43):e2103091118, 2021.
82. Zhihui Zhu, Tianyu Ding, Jinxin Zhou, Xiao Li, Chong You, Jeremias Sulam, and Qing Qu. A geometric analysis of neural collapse with unconstrained features. In Advances in Neural Information Processing Systems, volume 34 of NeurIPS, pages 29820–29834, 2021.
83. Alex Graves, Greg Wayne, and Ivo Danihelka. Neural turing machines, 2014.
84. Alex Graves, Greg Wayne, Malcolm Reynolds, Tim Harley, Ivo Danihelka, Agnieszka Grabska-Barwińska, Sergio Gómez Colmenarejo, Edward Grefenstette, Tiago Ramalho, John Agapiou, et al. Hybrid computing using a neural network with dynamic external memory. Nature, 538(7626):471–476, 2016.
85. Lukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In ICLR, 2016.
86. Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, and Tom Goldstein. Scaling up test-time compute with latent reasoning: A recurrent depth approach, 2025.
87. Tiedong Liu and Kian Hsiang Low. Goat: Fine-tuned llama outperforms gpt-4 on arithmetic tasks. ArXiv, abs/2305.14201, 2023.
88. Alex Graves. Adaptive computation time for recurrent neural networks. ArXiv, abs/1603.08983, 2016.
89. Andrea Banino, Jan Balaguer, and Charles Blundell. Pondernet: Learning to ponder. ArXiv, abs/2107.05407, 2021.
90. Chris Eliasmith, Terrence C Stewart, Xuan Choo, Trevor Bekolay, Travis DeWolf, Yichuan Tang, and Daniel Rasmussen. A large-scale model of the functioning brain. science, 338(6111):1202–1205, 2012.
91. James CR Whittington, Timothy H Muller, Shirley Mark, Guifen Chen, Caswell Barry, Neil Burgess, and Timothy EJ Behrens. The tolman-eichenbaum machine: unifying space and relational memory through generalization in the hippocampal formation. Cell, 183(5):1249–1263, 2020.
92. Lars Buesing, Johannes Bill, Bernhard Nessler, and Wolfgang Maass. Neural dynamics as sampling: a model for stochastic computation in recurrent networks of spiking neurons. PLoS computational biology, 7(11):e1002211, 2011.
93. Salah Hihi and Yoshua Bengio. Hierarchical recurrent neural networks for long-term dependencies. In D. Touretzky, M.C. Mozer, and M. Hasselmo, editors, Advances in Neural Information Processing Systems, volume 8. MIT Press, 1995.
94. Jan Koutník, Klaus Greff, Faustino J. Gomez, and Jürgen Schmidhuber. A clockwork rnn. In International Conference on Machine Learning, 2014.
95. Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Lukasz Kaiser. Universal transformers, 2018. arXiv preprint arXiv:1807.03819.
96. Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Lucas Liu, Baolin Peng, Hao Cheng, Xuehai He, Kuan Wang, Jianfeng Gao, Weizhu Chen, Shuohang Wang, Simon Shaolei Du, and Yelong Shen. Reinforcement learning for reasoning in large language models with one training example, 2025.
97. Niklas Muennighoff. s1: Simple test-time scaling. arXiv preprint arXiv:2502.23456, 2025.
98. Liang Wen, Yunke Cai, Fenrui Xiao, Xin He, Qi An, Zhenyu Duan, Yimin Du, Junchen Liu, Lifu Tang, Xiaowei Lv, Haosheng Zou, Yongchao Deng, Shousheng Jia, and Xiangzheng Zhang. Light-r1: Curriculum sft, dpo and rl for long cot from scratch and beyond, 2025.
99. Xuefeng Li, Haoyang Zou, and Pengfei Liu. Limr: Less is more for rl scaling, 2025.
100. Tri Dao and Albert Gu. Transformers are ssms: Generalized models and efficient algorithms through structured state space duality. ArXiv, abs/2405.21060, 2024.
101. Han Guo, Songlin Yang, Tarushii Goel, Eric P Xing, Tri Dao, and Yoon Kim. Log-linear attention. arXiv preprint arXiv:2506.04761, 2025.

---

**Referensi**: arXiv:2506.21734v3 [cs.AI] 4 Aug 2025

**Penulis Korespondensi**: research@sapient.inc
