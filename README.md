# Awesome Radio Map Estimation

> A living, community-curated research hub for **Radio Map Estimation** — spanning
> radio environment maps (REM), spectrum cartography, pathloss prediction, and
> channel knowledge maps (CKM).

<!-- AUTO:badges START -->
[![CI](https://github.com/DongYang26/awesome-radio-map-estimation/actions/workflows/validate.yml/badge.svg)](https://github.com/DongYang26/awesome-radio-map-estimation/actions/workflows/validate.yml)
[![Deploy](https://github.com/DongYang26/awesome-radio-map-estimation/actions/workflows/deploy.yml/badge.svg)](https://github.com/DongYang26/awesome-radio-map-estimation/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen)](https://dongyang26.github.io/awesome-radio-map-estimation/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Data License: CC-BY-4.0](https://img.shields.io/badge/Data%20License-CC--BY--4.0-blue.svg)](LICENSE-DATA)
![Papers](https://img.shields.io/badge/papers-392-informational)
<!-- AUTO:badges END -->

[**Explore the interactive Research Map →**](https://dongyang26.github.io/awesome-radio-map-estimation/)

## What is this?

**Radio Map Estimation** is the problem of reconstructing or predicting a spatial
map of a radio quantity — received signal strength, pathloss, SINR, spectral
power, or channel gain — across a geographic area, from sparse field measurements
and/or environmental information such as building layouts and terrain. It is the
backbone of spectrum management, network planning, coverage analysis, localization,
and emerging 6G / integrated sensing-and-communication systems.

This repository is **more than a paper list**. It is a structured, self-updating
knowledge base:

- **Structured paper database** — every paper is a single, schema-validated YAML
  file under [`data/papers/`](data/papers). One file per paper, no merge conflicts.
- **Research Map** — three complementary views of the field: a **taxonomy tree**
  (methods, by family), an **evolution timeline** (how the field moved), and a
  searchable, filterable **landscape matrix** (every paper × every dimension).
- **Datasets & benchmarks** — a catalog of the datasets the community builds on.
- **Newcomer reading path** — a curated route through the landmark papers.
- **Self-updating** — a weekly GitHub Action discovers new papers on arXiv and
  Semantic Scholar and opens a pull request for maintainer review.

The interactive site is the best way to browse; this README is the offline,
GitHub-rendered mirror.

## Scope

Four sub-families of the field are in scope:

| Subfield | What it covers |
|----------|----------------|
| **REM** | Radio map / radio environment map estimation from sparse measurements |
| **Spectrum Cartography** | Power-spectrum maps, spectrum-occupancy estimation |
| **Pathloss Prediction** | Pathloss / propagation maps from environment data (e.g. RadioUNet) |
| **CKM** | Channel knowledge maps for 6G / ISAC |

## Statistics

<!-- AUTO:stats START -->
**392** papers · **4** subfields · **20** milestone papers

Coverage spans **1996–2026**.
By subfield — Channel Knowledge Maps (CKM): 47, Radio Environment Maps (REM): 181, Pathloss Prediction: 127, Spectrum Cartography: 37.
<!-- AUTO:stats END -->

## Taxonomy

<!-- AUTO:taxonomy START -->
- **Interpolation-based** — Methods that estimate radio maps by interpolating from sparse spatial measurements without explicit propagation models.
  - **Kriging** — Geostatistical interpolation using variogram-modelled spatial correlations; also known as Gaussian process regression on a lattice.
  - **IDW** — Inverse Distance Weighting — assigns measurement influence proportional to the inverse of distance to the query point.
  - **Matrix Completion** — Recovers a dense radio map by completing a partially observed measurement matrix via low-rank or sparse constraints.
  - **Gaussian Process** — Bayesian non-parametric interpolation that provides both mean estimates and uncertainty bounds over the spatial field.
- **Model-based / Physics-based** — Methods grounded in electromagnetic propagation theory or environment geometry to predict signal distributions.
  - **Ray Tracing** — Simulates electromagnetic wave propagation by tracing ray paths through the environment to compute path loss and multipath effects.
- **Learning-based (Deep Learning)** — Data-driven methods that learn radio propagation patterns from measurements or simulations using neural network architectures.
  - **CNN** — Convolutional Neural Networks that exploit spatial locality to infer signal strength maps from sparse inputs or environment features.
  - **GAN** — Generative Adversarial Networks used to synthesise or super-resolve radio maps with realistic spatial structure.
  - **Transformer** — Attention-based models that capture long-range spatial dependencies across measurement locations for radio map estimation.
  - **INR** — Implicit Neural Representations that encode the radio map as a continuous function of coordinates, enabling query at arbitrary resolution.
  - **Diffusion** — Score-based or DDPM-style generative models that iteratively denoise a signal field to produce high-fidelity radio maps.
  - **GNN** — Graph Neural Networks that model sensors or locations as nodes and propagate information along spatial or connectivity edges.
  - **RNN** — Recurrent Neural Networks applied to sequential or trajectory-based measurement data for radio map construction.
  - **Autoencoder** — Encoder-decoder architectures that learn compact latent representations of radio environments for reconstruction or completion.
- **Application — Using Radio Maps / CKM** — Papers that USE a radio environment or channel knowledge map for a downstream task (beamforming, ISAC, channel estimation, localization, …) rather than proposing an estimation method. Includes CKM concept and tutorial papers.
<!-- AUTO:taxonomy END -->

## Papers

<!-- AUTO:papers START -->
### Radio Environment Maps (REM)

- [FM-RME: Foundation Model Empowered Radio Map Estimation](https://arxiv.org/abs/2602.22231) — Dong Yang, Yue Wang, Songyang Zhang et al., 2026 ⭐
- [A Tutorial on Learning-Based Radio Map Construction: Data, Paradigms, and Physics-Awareness](https://arxiv.org/abs/2603.17499) — Xiucheng Wang, Yuhao Pan, Nan Cheng, 2026
- [DF-3DRME: A Data-Friendly Learning Framework for 3D Radio Map Estimation based on Super-Resolution Technique](https://arxiv.org/abs/2604.00676) — Lin Zhu, Weifeng Zhu, Shuowen Zhang et al., 2026
- [Learned Elevation Models as a Lightweight Alternative to LiDAR for Radio Environment Map Estimation](https://arxiv.org/abs/2604.05520) — Ljupcho Milosheski, Fedja Movcnik, Mihael Mohorvcivc et al., 2026
- [Beam-Aware Radio Map Estimation With Physics-Consistent Parametric Modeling for Unknown Multiple Satellites](https://arxiv.org/abs/2605.07763) — Xiucheng Wang, Nan Cheng, Zhisheng Yin et al., 2026
- [Eliminating Premature Termination in Multihop Rendezvous for Cognitive Radio-based Emergency Response Network](https://arxiv.org/abs/2605.22325) — Zahid Ali, Saritha Unnikrishnan, Eoghan Furey et al., 2026
- [Tri-Domain Multiuser MIMO Precoding Optimization and Channel Estimation with Spatial-EM Reconfigurable Antenna](https://arxiv.org/abs/2605.23682) — Yining Li, Ziwei Wan, Zhen Gao et al., 2026
- [SIM-Aided Near-Field Channel and Localization Estimation With Dimensionality Reduction: A Multiport Network Theory Approach](https://arxiv.org/abs/2605.23779) — Andrea Abrardo, Bartoli Giulio, 2026
- [A Measurement-Based Parameterization of Physics Reflection Models for Terahertz Communication](https://arxiv.org/abs/2605.23795) — Taihao Zhang, Chenzhou Lin, Cunhua Pan et al., 2026
- [Advanced AI Service Provisioning in O-RAN through LLM Engine Integration](https://arxiv.org/abs/2605.23809) — Seyed Bagher Hashemi Natanzi, Pranshav Gajja, Bo Tang et al., 2026
- [Ray-Tracing vs. 3GPP TDL: Power Delay Profile Analysis in Outdoor-to-Indoor and Indoor Channels](https://arxiv.org/abs/2605.23831) — Julia Andrusenko, Chloe Makdad, 2026
- [RadioFormer3D: Weakly Supervised 3D Radio Map Estimation in Low-Altitude Airspace via Generative Modeling](https://arxiv.org/abs/2605.29538) — Zheng Fang, Junjie Liu, Kangjun Liu et al., 2026
- [Design-Oriented Modeling of TSV Substrate Noise Coupling to Ring VCOs](https://arxiv.org/abs/2605.29867) — Ilias Exouzidis, Alberto Garcia-Ortiz, George Floros et al., 2026
- [Software Platform for Hybrid Pseudo-Random Sequence Generation and Predictability Analysis Based on LFSR and Mersenne Twister](https://arxiv.org/abs/2605.30977) — Ali Abdolrahimi Zarnagh, Ali Motazedifard, 2026
- [DRIFT: Joint Channel Estimation and Prediction Towards Pilotless 6G Non-Terrestrial Networks](https://arxiv.org/abs/2605.31065) — Bruno De Filippo, Carla Amatetti, Alessandro Vanelli-Coralli, 2026
- [SQEEZ: Energy-efficient Location Sharing for Mobile Ad Hoc Networks](https://arxiv.org/abs/2605.31339) — Ram Ramanathan, Dmitrii Dugaev, Ryan Conyac et al., 2026
- [Sensing with Random Signals: The Role of Time Sharing](https://arxiv.org/abs/2605.31353) — Yi Geng, Wenyi Zhang, 2026
- [ISAC-Enabled Grant-Free Uplink via Artificial-Path Delay Modulation](https://arxiv.org/abs/2605.31366) — Ruiqi Kong, He Chen, 2026
- [Cooperative Uplink Channel Estimation in User-Centric Cell-free Massive MIMO Communication Networks](https://arxiv.org/abs/2605.31510) — Pourya Behmandpoor, Marc Moonen, 2026
- [Distributionally Robust Physical-Layer Security for Satellite Communication via Aerial Reconfigurable Intelligent Surface](https://arxiv.org/abs/2605.31526) — Zhaole Wang, Xiao Tang, Naijin Liu et al., 2026
- [Wireless Foundation Models: State-of-the-Art and Open Challenges](https://arxiv.org/abs/2609.04707) — Alonso M. Pacheco Huachaca, Juan J. Rodriguez Rodriguez, Ahmed Aboulfotouh et al., 2026
- [A Data-Driven Transfer Learning Method for Indoor Radio Map Estimation](https://doi.org/10.1109/TVT.2025.3609207) — Rahul Kumar Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2026
- [Constructing 4D Radio Map in LEO Satellite Networks with Limited Samples](https://arxiv.org/abs/2501.02775) — Haoxuan Yuan, Zhe Chen, Zheng Lin et al., 2025
- [Physics-Informed Representation Alignment for Sparse Radio-Map Reconstruction](https://arxiv.org/abs/2501.19160) — Haozhe Jia, Wenshuo Chen, Zhihui Huang et al., 2025
- [Trajectory Map-Matching in Urban Road Networks Based on RSS Measurements](https://arxiv.org/abs/2502.01280) — Zheng Xing, Weibing Zhao, 2025
- [Channel Gain Map Construction Based on Subregional Learning and Prediction](https://arxiv.org/abs/2502.15733) — Jiayi Chen, Ruifeng Gao, Jue Wang et al., 2025
- [Advancing THz Radio Map Construction and Obstacle Sensing: An Integrated Generative Framework in ISAC](https://arxiv.org/abs/2503.23055) — Tianyu Hu, Shuai-Han Wang, Yunhang Xie et al., 2025
- [Machine Learning based Radio Environment Map Estimation for Indoor Visible Light Communication](https://arxiv.org/abs/2507.19149) — Helena Serpi, C. Politi, 2025
- [DT-Aided Resource Management in Spectrum Sharing Integrated Satellite-Terrestrial Networks](https://arxiv.org/abs/2507.20789) — Hung Nguyen-Kha, Vu Nguyen Ha, T. Nguyen et al., 2025
- [PINN and GNN-based RF Map Construction for Wireless Communication Systems](https://arxiv.org/abs/2507.22513) — Lizhou Liu, Xiaohui Chen, Zihan Tang et al., 2025
- [RadioMamba: Breaking the Accuracy-Efficiency Trade-Off in Radio Map Construction via a Hybrid Mamba-UNet](https://arxiv.org/abs/2508.09140) — Honggang Jia, Nan Cheng, Xiucheng Wang et al., 2025
- [A Fine-Grained 3D Radio Map Construction Paradigm With Ultra-Low Sampling Rates by Large Generative Models](https://arxiv.org/abs/2509.11571) — Zhiyuan Liu, Qingyu Liu, Shuhang Zhang et al., 2025
- [Unsupervised Radio Map Construction in Mixed LoS/NLoS Indoor Environments](https://arxiv.org/abs/2510.08015) — Zheng Xing, Junting Chen, 2025
- [Physics-Informed Neural Networks for MIMO Beam Map and Environment Reconstruction](https://arxiv.org/abs/2510.21238) — Wangqian Chen, Junting Chen, Shuguang Cui, 2025
- [Structure-Aware Near-Field Radio Map Recovery via RBF-Assisted Matrix Completion](https://arxiv.org/abs/2511.06710) — Hao Sun, Xianghao Yu, Junting Chen, 2025
- [Adversarial Learning-Based Radio Map Reconstruction for Fingerprinting Localization](https://arxiv.org/abs/2511.14495) — Jiaming Zhang, Jiajun He, Tianyu Lu et al., 2025
- [A Gaussian Splatting Approach to Continuous Radio Map Construction](https://doi.org/10.1109/INFOCOMWKSHPS65812.2025.11153005) — Anthony Chen, Shiwen Mao, Zhu Li et al., 2025
- [A Graph Neural Network-Based Radio Map Construction With Uncertainty Prediction](https://doi.org/10.1109/IEEECONF67917.2025.11443759) — Fatema Islam Tania, Seung-Jun Kim, 2025
- [A Recent Survey on Radio Map Estimation Methods for Wireless Networks](https://doi.org/10.3390/electronics14081564) — Bin Feng, Meng Zheng, Wei Liang et al., 2025
- [A Sampling Method for Radio Environment Map Reconstruction Based on Multiarea Gudmundson Model](https://doi.org/10.1109/JSEN.2025.3559083) — Rui Zhang, Fang Ye, Jingchao Li et al., 2025
- [A UAV Radio Frequency Fingerprint Recognition System Based on Time-Frequency Maps](https://doi.org/10.1109/ICITES66466.2025.11274303) — Dong Wang, Tao Long, 2025
- [AIGC-Based Radio Map Construction for Channel Estimation in Low-Altitude Economy](https://doi.org/10.1109/ICCCWorkshops67136.2025.11148098) — Bin Yang, Wei Zhang, Shengli Zhang, 2025
- [An Accurate Radio Environment Map Reconstruction Method](https://doi.org/10.1109/JSEN.2025.3562214) — Yazhou Sun, Longhui Wang, Jian Wang, 2025
- [3-D Radio Map Estimation Based on Active Measurement Trajectory Selection](https://doi.org/10.1109/LWC.2025.3557556) — Zhibo Chen, Heng Wang, Daoxing Guo, 2025
- [Collaborative Spectrum Sensing for Multi-UAV System: A U-Net Approach With Uncertainty Awareness](https://doi.org/10.1109/TVT.2025.3566494) — Jie Shi, Jiaxin Wu, Jingzheng Chong et al., 2025
- [Deep Learning for Radio Map Estimation in Wireless Communication Networks](https://doi.org/10.1145/3797161.3797212) — Haokai Zhang, Zhiyuan You, Jianmiao Liu et al., 2025
- [FedRME: Importance-Aware Cooperative Radio Map Estimation Empowered by Vertical Federated Learning](https://doi.org/10.1109/ICCWorkshops67674.2025.11162141) — Hexuan Ma, Zezhong Zhang, Kai Chen et al., 2025
- [Grid-Free Radio Map Estimation via Unsupervised Implicit Continuous Representation](https://doi.org/10.1109/LSP.2025.3601038) — Xiaonan Chen, Jun Wang, 2025
- [Bayesian Radio Map Estimation: Fundamentals and Implementation via Diffusion Models](https://doi.org/10.48550/arXiv.2502.09998) — Tien Ngoc Ha, Daniel Romero, 2025
- [Leveraging Transfer Learning for Radio Map Estimation via Mixture of Experts](https://doi.org/10.1109/TCCN.2025.3570469) — Rahul Kumar Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2025
- [Land Feature Aware Radio Environment Map Construction using Radio Oriented Heterogeneous Multitask Gaussian Process](https://doi.org/10.1109/GLOBECOM59602.2025.11432161) — Haoxian Liu, Kai Chen, Zezhong Zhang et al., 2025
- [Paying Deformable Attention to Sparse Spatial Observations for Deep Radio Map Estimation](https://github.com/AkonLau/DAT-Unet) — Kangjun Liu, Chunyan Qiu, Ke Chen et al., 2025
- [MAE-Based Radio Map Construction for Wi-Fi Fingerprint Indoor Localization](https://doi.org/10.1109/LCOMM.2025.3582075) — Yishuo Cheng, Liye Zhang, 2025
- [MoDeFA: Multiobserver and Denoising-Enhanced Fingerprint Augmentation for Semi-Supervised Wi-Fi RSS-Based Indoor Positioning](https://doi.org/10.1109/JIOT.2025.3573967) — Tian-Jie Xiang, Yuanjiang Sun, Gang Shen, 2025
- [Movable Access Point-Aided Integrated Visible Light Communication and Sensing Networks](https://doi.org/10.1109/LWC.2024.3521192) — Zohaib Saghir, Sylvester B. Aboagye, 2025
- [Novel Radio Environment Map Construction Scheme for 3-D and Full Band for Modern Internet of Things Applications](https://doi.org/10.1109/JIOT.2024.3520611) — Shoubin Zhang, Zhimeng Li, Haojin Li et al., 2025
- [Physics-Inspired Distributed Radio Map Estimation](https://doi.org/10.1109/ICC52391.2025.11161293) — Dong Yang, Yue Wang, Songyang Zhang et al., 2025
- [Radio Coverage Estimation and Ray Tracing with Digital Terrain Models in the Matlab Environment](https://doi.org/10.1109/WECONF65186.2025.11017262) — G. Fokin, V. Starikov, Vladimir Sevidov, 2025
- [Radio-Frequency Map Optimization for Indoor Positioning and Tracking](https://doi.org/10.35377/saucis...1644762) — F. Daníş, 2025
- [Radio Map Reconstruction Based on Deep Denoising Regularization for UAV Communications](https://doi.org/10.1109/TVT.2025.3542768) — Haotai Zhao, Qing Hao, Yunxiang He et al., 2025
- [RadioFormer: A Multiple-Granularity Radio Map Estimation Transformer with 1‱ Spatial Sampling](https://arxiv.org/abs/2504.19161) — Zheng Fang, Kangjun Liu, Ke Chen et al., 2025
- [Radiotrace: Bridging Diffusion Priors and RSS Measurements for Accurate Radio Map Estimation](https://doi.org/10.1109/MLSP62443.2025.11204335) — Liu Yang, Qiang Li, Zhuo Cao et al., 2025
- [Denoising Diffusion Probabilistic Model for Radio Map Estimation in Generative Wireless Networks](https://doi.org/10.1109/TCCN.2025.3529879) — Xuanhao Luo, Zhizhen Li, Zhiyuan Peng et al., 2025
- [Scalable AI-assisted optical radio environment map estimation for indoor visible-light communication systems (AI-VLCmaps)](https://doi.org/10.1117/12.3065355) — Helena Serpi, Dimitris Alexandropoulos, C. Politi, 2025
- [Self-Supervised Learning Informed Radio Environment Map Estimation with Few Samples](https://doi.org/10.1109/GLOBECOM59602.2025.11431663) — Jianping Ma, Zezhong Zhang, Junting Chen et al., 2025
- [Smartphone-Based WiFi RTT/RSS/PDR/Map Indoor Positioning System Using Particle Filter](https://doi.org/10.1109/TIM.2024.3509549) — Meng Sun, Yunjia Wang, Qianxin Wang et al., 2025
- [Time-Variant Radio Map Reconstruction With Optimized Distributed Sensors in Dynamic Spectrum Environments](https://doi.org/10.22541/au.172893971.19345105/v1) — Qianhao Gao, Qiuming Zhu, Zhipeng Lin et al., 2025
- [WiFi-Diffusion: Achieving Fine-Grained WiFi Radio Map Estimation With Ultra-Low Sampling Rate by Diffusion Models](https://doi.org/10.1109/JSAC.2025.3584562) — Zhiyuan Liu, Shuhang Zhang, Qingyu Liu et al., 2025
- [Radio Map Estimation Based on Generative Artificial Intelligence: Evolution from Point-Level to Cell-Level Prediction](https://doi.org/10.1109/MCOM.005.2400027) — Yi Zheng, Ji Wang, Wenwu Xie et al., 2025
- [Radio Map-Based Spectrum Sharing for Joint Communication and Sensing](https://arxiv.org/abs/2401.02118) — Xinran Fang, W. Feng, Yunfei Chen et al., 2024
- [Fast and Accurate Cooperative Radio Map Estimation Enabled by GAN](https://arxiv.org/abs/2402.02729) — Zezhong Zhang, Guangxu Zhu, Junting Chen et al., 2024
- [Sparse Bayesian Learning-Based Hierarchical Construction for 3D Radio Environment Maps Incorporating Channel Shadowing](https://arxiv.org/abs/2403.08323) — Jie Wang, Qiuming Zhu, Zhipeng Lin et al., 2024
- [Diffraction and Scattering Aware Radio Map and Environment Reconstruction Using Geometry Model-Assisted Deep Learning](https://arxiv.org/abs/2403.00229) — Wangqian Chen, Junting Chen, 2024
- [Deep-Learning-Based Radio Map Reconstruction for V2X Communications](https://ieeexplore.ieee.org/ielx7/25/4356907/10292913.pdf) — Sandra Roger, Mattia Brambilla, Bernardo Camajori Tedeschini et al., 2024
- [Distributed Radio Map Reconstruction Based on Semi-Asynchronous Federated Learning Generative Adversarial Networks](https://doi.org/10.1109/ICCCWorkshops62562.2024.10693836) — Yuqi Hou, Yang Huang, Xiaomin Chen, 2024
- [Enhancing Indoor Millimeter Radio Communication: A Probabilistic Approach to RSS Map Estimation](https://doi.org/10.1109/CCNC51664.2024.10454887) — Daiki Kodama, Kenji Ohira, Hideyuki Shimonishi et al., 2024
- [Estimation of Radio Map in the Indoor Environment: Experimental Measurement](https://doi.org/10.1109/WPMC63271.2024.10863186) — A. M. C. Jahanavi, Navin Kumar, V. Kumar et al., 2024
- [Indoor Radio Environment Map Construction using Node Position Estimation for Smart Factories](https://doi.org/10.1109/PIMRC59610.2024.10817191) — Hayato Mukasa, Kohei Yuzawa, Takeo Fujii et al., 2024
- [Radio Environment Map Construction Based on Privacy-Centric Federated Learning](https://ieeexplore.ieee.org/ielx7/6287639/10380310/10440080.pdf) — Shafi Ullah Khan, Carla E. García, Taewoong Hwang et al., 2024
- [Machine Learning Based Radio Environment Map Construction for Cellular Networks](https://doi.org/10.1109/AP-S/INC-USNC-URSI52054.2024.10686580) — Vasileios P. Rekkas, S. Sotiroudis, Z. Zaharis et al., 2024
- [Neural architecture search for radio map reconstruction with partially labeled data](https://doi.org/10.3233/ICA-240732) — A. Malkova, Massih-Reza Amini, Benoît Denis et al., 2024
- [On the Construction of Channel Gain Map: Model-Based or Model-Free Approach?](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683332) — Weina Xie, Xiaoli Xu, Zhuoyin Dai et al., 2024
- [Online Trajectory Optimization for Energy-Efficient Cellular-Connected UAVs With Map Reconstruction](https://doi.org/10.1109/TVT.2023.3323349) — Haitao Zhao, Qing Hao, Hao Huang et al., 2024
- [Optimizing Ray Tracing Techniques for Generating Large-Scale 3D Radio Frequency Maps](https://inria.hal.science/hal-04546462/file/WoWMoM2024.pdf) — Bernard Tamba Sandouno, C. Barakat, T. Turletti et al., 2024
- [Radio Map Reconstruction Based on Transformer from Sparse Measurement](https://doi.org/10.1109/ICCT62411.2024.10946503) — Zhibo Chen, Daoxing Guo, Ning Yang et al., 2024
- [Real Time Reconstruction of Radio Environment Maps in Indoor Millimeter-Wave Beamforming with Beam Changes](https://doi.org/10.23919/CNSM62983.2024.10814612) — Takumi Bushi, Toshiro Nakahira, Shoko Shinohara et al., 2024
- [Data-Driven Radio Environment Map Estimation Using Graph Neural Networks](https://doi.org/10.1109/ICCWorkshops59551.2024.10615637) — Ali Shibli, Tahar Zanouda, 2024
- [RM-Gen: Conditional Diffusion Model-Based Radio Map Generation for Wireless Networks](https://doi.org/10.23919/IFIPNetworking62109.2024.10619829) — Xuanhao Luo, Zhizhen Li, Zhiyuan Peng et al., 2024
- [RobUNet: A Radio Map Construction Method with A Strong Generalization Capability](https://doi.org/10.1109/GLOBECOM52923.2024.10901772) — Shuai Shao, Kangjun Liu, Qingyu Liu et al., 2024
- [A Deep-Learning Approach to a Volumetric Radio Environment Map Construction for UAV-Assisted Networks](https://downloads.hindawi.com/journals/ijap/2024/9062023.pdf) — Bezawit Sahilu Shawel, Dereje H. Woldegebreal, Sofie Pollin, 2024
- [Sparse Bayesian Learning-Based 3-D Radio Environment Map Construction—Sampling Optimization, Scenario-Dependent Dictionary Construction, and Sparse Recovery](https://doi.org/10.1109/TCCN.2023.3319539) — Jie Wang, Qiuming Zhu, Zhipeng Lin et al., 2024
- [Spectrum Sensing Method Based on STFT-RADN in Cognitive Radio Networks](https://doi.org/10.3390/s24175792) — Anyi Wang, Tao Zhu, Qifeng Meng, 2024
- [Towards the Metaverse: Distributed Radio Map Reconstruction based on Federated Learning Generative Adversarial Networks](https://doi.org/10.1109/IWCMC61514.2024.10592435) — Yang Huang, Yuqi Hou, Qiuming Zhu et al., 2024
- [UAV-Aided 3D Building Map Reconstruction from RSS Measurements: A Diffraction-Based Approach](https://doi.org/10.1109/ICET61945.2024.10672783) — Zhiqiang Tan, Yuanhao Jiang, Limin Xiao et al., 2024
- [Neural Representation for Wireless Radiation Field Reconstruction: A 3D Gaussian Splatting Approach](https://github.com/wenchaozheng/WRF-GSplus) — Chaozheng Wen, Jingwen Tong, Yingdong Hu et al., 2024
- [UAV-Aided Radio Map Construction Exploiting Environment Semantics](https://arxiv.org/abs/2107.10574) — Wenjie Liu, Junting Chen, 2023
- [3D Radio Map Reconstruction Based on Generative Adversarial Networks Under Constrained Aircraft Trajectories](https://doi.org/10.1109/TVT.2023.3239556) — Tianyu Hu, Yang Huang, Junting Chen et al., 2023
- [Analytical Performance Bounds for Radio Map Estimation](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683442) — Daniel Romero, Tien Ngoc Ha, Raju Shrestha et al., 2023
- [Automatic Indoor Radio Map Construction and Localization via Multipath Fingerprint Extrapolation](https://doi.org/10.1109/TWC.2023.3237359) — Qiao Li, Xuewen Liao, Ang Li et al., 2023
- [Blockage-Aware Radio Map Construction via Exploiting the Diffraction and Obstruction Structure](https://doi.org/10.1109/GLOBECOM54140.2023.10437033) — Wangqian Chen, Junting Chen, 2023
- [DeepREM: Deep-Learning-Based Radio Environment Map Estimation From Sparse Measurements](https://ieeexplore.ieee.org/ielx7/6287639/10005208/10127968.pdf) — Andrea Cháves-Villota, Carlos A. Viteri-Mera, 2023
- [IndoorRSSINet - Deep learning based 2D RSSI map prediction for indoor environments with application to wireless localization](https://doi.org/10.1109/COMSNETS56262.2023.10041394) — N. Raj, V. B. S., 2023
- [Location-free Indoor Radio Map Estimation using Transfer learning](https://doi.org/10.1109/VTC2023-Spring57618.2023.10200979) — R. Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2023
- [Observation Data and 3D Map-based Radio Environment Estimation for Drone Wireless Communications](https://doi.org/10.1109/ICUFN57995.2023.10199770) — S. Yamada, T. Fujii, Katsuya Suto et al., 2023
- [Path Planning for Adaptive CSI Map Construction With A3C in Dynamic Environments](https://doi.org/10.1109/TMC.2021.3131318) — Xiaoqiang Zhu, Tie Qiu, W. Qu et al., 2023
- [Received signal strength reconstruction using pix2pix generative adversarial network](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1049/ell2.12988) — Haochang Wu, Hao Qin, Xingqi Zhang, 2023
- [Radio Map Estimation with Deep Dual Path Autoencoders and Skip Connection Learning](https://doi.org/10.1109/PIMRC56721.2023.10293748) — W. Locke, Nikita Lokhmachev, Yan Huang et al., 2023
- [Spectrum Sensing Based on Graph Weighted Aggregation Operator](https://doi.org/10.1109/LCOMM.2023.3314805) — Yuxin Li, Guangyue Lu, Yinghui Ye, 2023
- [VariFi: Variational Inference for Indoor Pedestrian Localization and Tracking Using IMU and WiFi RSS](https://doi.org/10.1109/JIOT.2022.3232740) — He Huang, Jianfei Yang, Xu Fang et al., 2023
- [Spectrum Surveying: Active Radio Map Estimation With Autonomous UAVs](https://arxiv.org/abs/2201.04125) — Raj K. Shrestha, Daniel Romero, Sundeep Chepuri, 2022
- [Propagation Map Reconstruction via Interpolation Assisted Matrix Completion](https://arxiv.org/abs/2207.13473) — Haolin Sun, Junting Chen, 2022
- [Exemplar-Based Radio Map Reconstruction of Missing Areas Using Propagation Priority](https://arxiv.org/abs/2209.04566) — Songyang Zhang, Tianhang Yu, Jonathan Tivald et al., 2022
- [RME-GAN: A Learning Framework for Radio Map Estimation Based on Conditional Generative Adversarial Network](https://arxiv.org/abs/2212.12817) — Songyang Zhang, Achintha Wijesinghe, Zhi Ding, 2022 ⭐
- [Construction of Wideband Radio Environment Map Based on Compressed Sensing](https://doi.org/10.1109/WCSP55476.2022.10039453) — Ensong Yang, Hui Yu, Xiaohao Mo et al., 2022
- [Deep Transfer Learning Based Radio Map Estimation for Indoor Wireless Communications](https://doi.org/10.1109/spawc51304.2022.9833974) — Rahul Kumar Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2022
- [K-Nearest Neighbors Gaussian Process Regression for Urban Radio Map Reconstruction](https://doi.org/10.1109/LCOMM.2022.3207210) — Yifang Zhang, Shaowei Wang, 2022
- [Model and Transfer Spatial-Temporal Knowledge for Fine-Grained Radio Map Reconstruction](https://doi.org/10.1109/tccn.2021.3133844) — Kehan Li, Chao Li, B. Yu et al., 2022
- [RF signal shape reconstruction technology on the 2D space for indoor localization](https://doi.org/10.1109/iceic54506.2022.9748389) — Changsoo Yu, B. Shin, C. Kang et al., 2022
- [Self-Learning for Received Signal Strength Map Reconstruction with Neural Architecture Search](https://arxiv.org/abs/2105.07768) — A. Malkova, Loïc Pauletto, C. Villien et al., 2021
- [Three-Way Deep Neural Network for Radio Frequency Map Generation and Source Localization](https://arxiv.org/abs/2111.12175) — K. Gill, Son Nguyen, M. M. Thein et al., 2021
- [Chaotic Compressive Spectrum Sensing Based on Chebyshev Map for Cognitive Radio Networks](https://www.mdpi.com/2073-8994/13/3/429/pdf?version=1615545630) — Salma Benazzouza, Mohammed Ridouani, Fatima Salahdine et al., 2021
- [Dynamic Radio Map Using Statistical Hypothesis Testing](https://ieeexplore.ieee.org/ielx7/6687307/9530839/09310285.pdf) — Keita Katagiri, Koya Sato, Kei Inage et al., 2021
- [Experimental Analysis of Block-Sparsity-Based Spectrum Sensing Techniques for Cognitive Radar](https://doi.org/10.1109/TAES.2020.3021810) — A. Aubry, V. Carotenuto, A. De Maio et al., 2021
- [Graph Laplacian-Based Sequential Smooth Estimator for Three-Dimensional RSS Map](https://doi.org/10.1587/TRANSCOM.2020CQP0003) — T. Matsuda, F. Ono, S. Hara, 2021
- [Space-Frequency-Interpolated Radio Map](https://ieeexplore.ieee.org/ielx7/25/9353678/09316892.pdf) — Koya Sato, Katsuya Suto, Kei Inage et al., 2021
- [Wireless Signal Propagation Prediction Based on Computer Vision Sensing Technology for Forestry Security Monitoring](https://www.mdpi.com/1424-8220/21/17/5688/pdf?version=1629799914) — Jialuan He, Zirui Xing, Tianqi Xiang et al., 2021
- [Radio Environment Maps for Dynamic Frequency Selection in V2X Communications](https://arxiv.org/abs/2203.11604) — Paweł Sroka, P. Kryszkiewicz, Adrian Kliks, 2020
- [Algorithm for Electromagnetic Power Estimation in Radio Environment Map](https://doi.org/10.14445/23488549/ijece-v7i5p108) — Tilal Elsheikh Ahmed Osman, Osman Mudathir Elfadil, 2020
- [Design of Optimal Non-Uniform Quantizer in Imperfect Noisy Reporting Channels for Collaborative Spectrum Sensing](https://doi.org/10.1109/TVT.2020.3015219) — Masoumeh Naderipour, Amirhossein Taherpour, Abbas Taherpour et al., 2020
- [Radio environment map construction by adaptive ordinary Kriging algorithm based on affinity propagation clustering](https://doi.org/10.1177/1550147720922484) — Haiyang Xia, Song Zha, Jijun Huang et al., 2020
- [A cooperative spectrum sensing method based on information geometry and fuzzy c-means clustering algorithm](https://jwcn-eurasipjournals.springeropen.com/track/pdf/10.1186/s13638-019-1338-z) — Shunchao Zhang, Yonghua Wang, Jiangfan Li et al., 2019
- [A novel radio map construction method with reduced human efforts for Wi-Fi localisation system](https://doi.org/10.1504/IJSNET.2019.10023451) — Qiyue Li, Heng Xu, Wei Sun et al., 2019
- [Adaptive Compressed Wideband Spectrum Sensing Based on Radio Environment Map Dedicated for Space Information Networks](https://doi.org/10.1007/978-3-030-19153-5_12) — Xiaoluan Zhang, Youping Zhao, Hongbin Chen, 2019
- [BS-to-Ground Channel Reconstruction With 3D Obstacle Map Based on RSS Measurements](https://ieeexplore.ieee.org/ielx7/6287639/8600701/08769845.pdf) — Chenchen Fan, Xiaofeng Zhong, Jie Wei, 2019
- [Radio Environment Map Construction by Kriging Algorithm Based on Mobile Crowd Sensing](https://doi.org/10.1155/2019/4064201) — Zhifeng Han, J. Liao, Q. Qi et al., 2019
- Real-time Cooperative Spectrum Sensing : Reliable Localization of Unknown Interferers in Shared Spectrum — K. Kulkarni, N. Franchi, G. Fettweis, 2019
- [Spectrum sensing by higher-order SVM-based detection](https://doi.org/10.23919/EUSIPCO.2019.8903028) — A. Coluccia, A. Fascista, G. Ricci, 2019
- [Engineering Radio Map for Wireless Resource Management](https://arxiv.org/abs/1807.08235) — Suzhi Bi, Jiangbin Lyu, Z. Ding et al., 2018
- [A Novel System for WiFi Radio Map Automatic Adaptation and Indoor Positioning](https://doi.org/10.1109/TVT.2018.2867065) — Ye Tao, Long Zhao, 2018
- [Kernelized Generalized Likelihood Ratio Test for Spectrum Sensing in Cognitive Radio](https://doi.org/10.1109/tvt.2018.2824023) — Lily Li, Shujie Hou, A. Anderson, 2018
- [Constructing Accurate Radio Environment Maps with Kriging Interpolation in Cognitive Radio Networks](https://doi.org/10.1109/CSQRWC.2018.8455448) — Danlei Mao, Wei Shao, Zuping Qian et al., 2018 ⭐
- [Multiple jammer localization and transmission power estimation for radio environment map](https://doi.org/10.1109/ICMCIS.2018.8398717) — V. L. Nir, B. Scheers, 2018
- [Opportunistic map based Flexible Hybrid Duplex Systems in Dynamic Spectrum Access](https://doi.org/10.1109/DySPAN.2018.8610496) — Soo-Min Kim, Han Cha, Seong-Lyun Kim et al., 2018
- [Radio environment map to support frequency allocation in military communications systems](https://doi.org/10.23919/URSI.2018.8406717) — M. Suchanski, P. Kaniewski, J. Romanik et al., 2018
- [Scheduling of Collaborative Sequential Compressed Sensing Over Wide Spectrum Band](https://doi.org/10.1109/tnet.2017.2787647) — Jie Zhao, Qiang Liu, Xin Wang et al., 2018
- [Spatial Angular Spectrum Sensing for Non-Geostationary Satellite Systems](https://doi.org/10.1109/GLOCOM.2018.8647520) — Chi Zhang, Chunxiao Jiang, Jin Jin et al., 2018
- [Two-dimensional spectrum sensing for cognitive radar](https://doi.org/10.1109/RADAR.2018.8378665) — A. Aubry, A. De Maio, Mark A. Govoni, 2018
- [An Active Sequential Xampling Detector for Spectrum Sensing](https://doi.org/10.1109/tccn.2018.2808528) — Lorenzo Ferrari, A. Scaglione, 2017
- [Identification of C-Band Radio Frequency Interferences from Sentinel-1 Data](https://www.mdpi.com/2072-4292/9/11/1183/pdf?version=1511274949) — A. Monti-Guarnieri, D. Giudici, A. Recchia, 2017
- [Kriging-Based Interference Power Constraint: Integrated Design of the Radio Environment Map and Transmission Power](https://doi.org/10.1109/tccn.2017.2653189) — Koya Sato, T. Fujii, 2017
- [Optimizing SOM for cell towers distribution](https://doi.org/10.1109/NTICT.2017.7976136) — H. K. Hoomod, I. Al-Mejibli, Abbas IssaJabboory, 2017
- [Radio Environment Map-Aided Doppler Shift Estimation in LTE Railway](https://doi.org/10.1109/TVT.2016.2599558) — Zhanwei Hou, Yiqing Zhou, Lin Tian et al., 2017
- [Radio Environment Map Estimation Based on Communication Cost Modeling for Heterogeneous Networks](https://roderic.uv.es/bitstreams/532899d7-3982-4eaf-a170-5f6bf3f5076d/download) — Fabiola Frantzis, Vinay-Prasad Chowdappa, C. Botella et al., 2017
- [Space-time correlation based fast regional spectrum sensing in cognitive radio](https://doi.org/10.1109/CC.2017.7942316) — Sai Huang, Yuanyuan Yao, Zhiyong Feng et al., 2017
- [SNR Degradation in GNSS-R Measurements Under the Effects of Radio-Frequency Interference](https://upcommons.upc.edu/bitstream/2117/102031/1/JSTARS15_vF.C.pdf) — J. Querol, Alberto Alonso Arroyo, Raul Onrubia Ibáñez et al., 2016
- [Spectrum sensing experimentation for LTE and WiFi unlicensed band operation](https://scindeks-clanci.ceon.rs/data/pdf/1821-3251/2016/1821-32511602076M.pdf) — N. Milosevic, Z. Nikolic, F. Jelenkovic et al., 2016
- [A Centralized PSD Map Construction by Distributed Compressive Sensing](https://doi.org/10.1109/LCOMM.2015.2391265) — M. Eslami, F. Torkamani-Azar, E. Mehrshahi, 2015
- [A new cooperative spectrum sensing with radio environment map in cognitive radio networks](https://doi.org/10.1109/ICAIOT.2015.7111533) — Yi Chen, Hang Zhang, Hang Hu et al., 2015
- [A new self-organizing map topology for real-time spectrum sensing and fast convergence](https://doi.org/10.1109/EUROCON.2015.7313761) — Liudas Stasionis, A. Serackis, 2015
- [Building accurate radio environment maps from multi-fidelity spectrum sensing data](https://doi.org/10.1007/s11276-015-1111-0) — S. Ulaganathan, D. Deschrijver, Mostafa Pakparvar et al., 2015
- [Channel quality map construction scheme using location information for heterogeneous wireless network](https://doi.org/10.11425/SST.4.83) — H. Oguma, Atsushi Koizumi, K. Norishima et al., 2015
- [Cooperative Spectrum Sensing](https://doi.org/10.1007/978-3-319-01718-1_3) — Huseyin Birkan Yilmaz, Salim Eryigit, T. Tuğcu, 2015
- [Kriging-Based Interference Power Constraint for Spectrum Sharing Based on Radio Environment Map](https://doi.org/10.1109/GLOCOMW.2015.7414008) — Koya Sato, T. Fujii, 2015
- [Location Estimation-Based Radio Environment Map Construction in Fading Channels](https://doi.org/10.1002/wcm.2367) — Huseyin Birkan Yilmaz, Tuna Tugcu, 2015 ⭐
- [Secure distributed estimation of radio environment map in hierarchical wireless Cognitive Radio networks](https://doi.org/10.1109/CCDC.2015.7162152) — Jianzhi Liu, Cailian Chen, Shichao Mi et al., 2015
- [Spectrum sensing for the unlicensed band cognitive radio](https://doi.org/10.1109/TELFOR.2015.7377458) — N. Milosevic, Z. Nikolic, F. Jelenkovic et al., 2015
- [The indirect self-tuning method for constructing radio environment map using omnidirectional or directional transmitter antenna](https://jwcn-eurasipjournals.springeropen.com/counter/pdf/10.1186/s13638-015-0297-2) — Marko Pesko, T. Javornik, Luka Vidmar et al., 2015
- [Distributed estimation for Radio Environment Map in cognitive radio networks](https://doi.org/10.1109/CHICC.2014.6896670) — Jianzhi Liu, Hui Han, Cailian Chen et al., 2014
- [Fast Spectrum Sensing: A Combination of Channel Correlation and Markov Model](https://doi.org/10.1109/MILCOM.2014.73) — Mingfei Gao, Xiao Yan, Yuchi Zhang et al., 2014
- [Probabilistic radio-frequency fingerprinting and localization on the run](https://doi.org/10.1002/bltj.21649) — Piotr Wojciech Mirowski, Dimitris Milioris, Phil Whiting et al., 2014
- [Radio environment map based maximum a posteriori Doppler shift estimation for LTE-R](https://doi.org/10.1109/HMWC.2014.7000241) — Yiqing Zhou, 2014
- [Radio Environment Maps: The Survey of Construction Methods](https://doi.org/10.3837/tiis.2014.11.008) — Marko Pesko, Tomaž Javornik, Andrej Košir et al., 2014 ⭐
- [Sparse Bayesian Hierarchical Prior Modeling Based Cooperative Spectrum Sensing in Wideband Cognitive Radio Networks](https://doi.org/10.1109/LSP.2014.2311902) — Feng Li, Zongben Xu, 2014
- [Transmitter location estimation for radio environment map construction using software defined radio](https://doi.org/10.1109/SCVT.2014.7046715) — M. Ozsahin, T. Tuğcu, 2014
- [Multiagent Reinforcement Learning Based Spectrum Sensing Policies for Cognitive Radio Networks](https://doi.org/10.1109/JSTSP.2013.2259797) — J. Lundén, Sanjeev R. Kulkarni, V. Koivunen et al., 2013
- Cooperative spectrum sensing and radio environment map construction in cognitive radio networks (Bilişsel radyo ağlarında işbirlikçi spektrum algılama ve frekans haritası oluşturma) — Huseyin Birkan Yilmaz, 2012
- [Efficient training for fingerprint based positioning using matrix completion](https://doi.org/10.5281/ZENODO.43028) — Sofia Nikitaki, G. Tsagkatakis, P. Tsakalides, 2012
- [Reconstruction of radio map from sparse RSS data by discontinuity preserving smoothing](https://doi.org/10.1145/2401603.2401653) — Wonsun Bong, Y. C. Kim, 2012
- [Cooperative Spectrum Sensing with a Progressive MAP Detection Algorithm](https://doi.org/10.1109/GLOCOM.2011.6134258) — Guoqing Zhou, Jingxian Wu, K. Sohraby, 2011
- [Dynamic Radio Map Construction for WLAN Indoor Location](https://doi.org/10.1109/IHMSC.2011.110) — Huimin Wang, Lin Ma, Yubin Xu et al., 2011
- [Approximate Calibration-Free Trajectory Reconstruction in a Wireless Network](https://doi.org/10.1109/TSP.2008.919090) — A. Almudevar, 2008

### Spectrum Cartography

- [Accelerating Regularized Attention Kernel Regression for Spectrum Cartography](https://doi.org/10.48550/arXiv.tao-laker-2026) — Liping Tao, Chee Wei Tan, 2026
- [Sensing Radio Maps via Bayesian Tensor Learning](https://doi.org/10.1109/ICC52391.2025.11161174) — Zhongtao Chen, Lei Cheng, Yik-Chung Wu, 2025
- [GPRT: A Gaussian Process Regression-Based Radio Map Construction Method for Rugged Terrain](https://doi.org/10.1109/JIOT.2025.3554507) — Guokai Chen, Yongxiang Liu, Jianzhao Zhang et al., 2025
- [Dynamic Spectrum Cartography: Reconstructing Spatial-Spectral-Temporal Radio Frequency Map via Tensor Completion](https://doi.org/10.1109/TSP.2025.3531872) — Xiaonan Chen, Jun Wang, Qingyang Huang, 2025
- [SC-GAN: A Spectrum Cartography with Satellite Internet Based on Pix2Pix Generative Adversarial Network](https://doi.org/10.23919/JCC.fa.2024-0269.202502) — Zhiqiang Pan, Bangning Zhang, Wang Heng et al., 2025
- [Domain-Factored Untrained Deep Prior for Spectrum Cartography](https://doi.org/10.1109/LSP.2025.3599714) — Subash Timilsina, Sagar Shrestha, Lei Cheng et al., 2025
- [Radio Environment Map Reconstruction via Tensor Completion: Bayesian and Semantic Approaches](https://doi.org/10.1109/TVT.2025.3531124) — Xuegang Wang, Fanggang Wang, Boxiang He, 2025
- [Temporal Spectrum Cartography in Low-Altitude Economy Networks: A Generative AI Framework With Multi-Agent Learning](https://doi.org/10.1109/TMC.2025.3647029) — Changyuan Zhao, Ruichen Zhang, Jiacheng Wang et al., 2025
- [GLIP: Electromagnetic Field Exposure Map Completion by Deep Generative Networks](https://arxiv.org/abs/2405.03384) — Mohammed Mallik, D. Gaillot, Laurent Clavier, 2024
- [A Spectrum Map Prediction Approach Based on](https://doi.org/10.1109/ICTC61510.2024.10602089) — Shoushuai He, Lei Zhu, Lu Yu et al., 2024
- [Dynamic Spectrum Cartography via Emitter Separation-Based Tensor Completion](https://doi.org/10.1109/ICC51166.2024.10622998) — Xiaonan Chen, Jun Wang, 2024
- [Fast 3-D Radio Map Reconstruction via Cross Tensor Approximation](https://doi.org/10.1109/JIOT.2024.3454817) — Chunmei Li, Z. Dou, Yun Lin, 2024
- [Infinite Limits of Convolutional Neural Network for Urban Electromagnetic Field Exposure Reconstruction](https://doi.org/10.1109/ACCESS.2024.3380835) — Mohammed Mallik, Baptiste Allaert, Esteban Egea-Lopez et al., 2024
- [3D Spectrum Awareness for Radio Dynamic Zones Using Kriging and Matrix Completion](https://doi.org/10.1109/DySPAN60163.2024.10632739) — Mushfiqur Rahman, Seungmo Maeng, Ismail Guvenc et al., 2024
- [Tensor-Based Parametric Spectrum Cartography From Irregular Off-Grid Samplings](https://doi.org/10.1109/LSP.2023.3257723) — Xiaonan Chen, Jun Wang, Guoyong Zhang et al., 2023
- [TRASC: Tensor-Based Radio Spectrum Cartography Using Plate Splines and Tensor CP Decomposition](https://doi.org/10.1109/FNWF58287.2023.10520367) — Mohsen Joneidi, Nazanin Rahnavard, Faramarz Hejazi, 2023
- [Kriging-Based 3-D Spectrum Awareness for Radio Dynamic Zones Using Aerial Spectrum Sensors](https://arxiv.org/abs/2307.06310) — Seungmo Maeng, Ozgur Ozdemir, Ismail Guvenc et al., 2023
- [Quantized Radio Map Estimation Using Tensor and Deep Generative Models](https://arxiv.org/abs/2303.01770) — Subash Timilsina, Sagar Shrestha, Xiao Fu, 2023
- [Radio Map Estimation: A data-driven approach to spectrum cartography](https://arxiv.org/abs/2202.03269) — Daniel Romero, Seung-Jun Kim, 2022 ⭐
- [UAV-Based Volumetric Measurements toward Radio Environment Map Construction and Analysis](https://www.mdpi.com/1424-8220/22/24/9705/pdf?version=1671175849) — Antoni Ivanov, Bilal Muhammad, Krasimir Tonchev et al., 2022
- [Deep Generative Model Learning for Blind Spectrum Cartography with NMF-Based Radio Map Disaggregation](https://doi.org/10.1109/ICASSP39728.2021.9413382) — Subash Shrestha, Xiao Fu, Min-Fong Hong, 2021
- [Deep Spectrum Cartography: Completing Radio Map Tensors Using Learned Neural Models](https://doi.org/10.1109/tsp.2022.3145190) — Subash Shrestha, Xiao Fu, Min-Fong Hong, 2021 ⭐
- [Location Based Joint Spectrum Sensing and Radio Resource Allocation in Cognitive Radio Enabled LTE-U Systems](https://doi.org/10.1109/TVT.2020.2966514) — Qi Yang, Yi-Feng Huang, Yin-Chen Yen et al., 2020
- [Spectrum Cartography via Coupled Block-Term Tensor Decomposition](https://doi.org/10.1109/tsp.2020.2993530) — Guoyong Zhang, Xiao Fu, Jun Wang et al., 2019 ⭐
- [Data-Driven Spectrum Cartography via Deep Completion Autoencoders](http://arxiv.org/pdf/1911.12810) — Yves Teganya, Daniel Romero, 2019 ⭐
- [Predictive spectrum occupancy probability‐based spatio‐temporal dynamic channel allocation map for future cognitive wireless networks](https://doi.org/10.1002/ett.3442) — Anirudh Agarwal, R. Gangopadhyay, 2018
- [Location-Free Spectrum Cartography](https://arxiv.org/abs/1812.11539) — Yves Teganya, Daniel Romero, Luis Miguel Lopez Ramos et al., 2018
- [Spectrally Efficient Data-Adaptive Spectrum Cartography](https://doi.org/10.1109/TSP.2017.2659650) — Daniel Romero, Seung-Jun Kim, Georgios B. Giannakis et al., 2017 ⭐
- [A Joint Tensor Completion and Prediction Scheme for Multi-Dimensional Spectrum Map Construction](https://ieeexplore.ieee.org/ielx7/6287639/7419931/07742926.pdf) — Mengyun Tang, Guoru Ding, Qihui Wu et al., 2016
- [Multi-dimensional spectrum map construction: A tensor perspective](https://doi.org/10.1109/WCSP.2016.7752600) — Mengyun Tang, Guoru Ding, Zhen Xue et al., 2016
- [Spectrum Cartography Using Quantized Observations](https://doi.org/10.1109/ICASSP.2015.7178572) — Daniel Romero, Seung-Jun Kim, Roberto Lopez-Valcarce et al., 2015
- [Stochastic Semiparametric Regression for Spectrum Cartography](https://doi.org/10.1109/CAMSAP.2015.7383849) — Daniel Romero, Seung-Jun Kim, Georgios B. Giannakis, 2015
- [Wireless Sensor Network for Spectrum Cartography Based on Kriging Interpolation](https://doi.org/10.1109/PIMRC.2012.6362597) — Gabriele Boccolini, Gustavo Hernandez-Penaloza, Baltasar Beferull-Lozano, 2012
- [Compressed Sensing Construction of Spectrum Map for Routing in Cognitive Radio Networks](https://doi.org/10.1002/wcm.2338) — Sung-Yin Shih, Kwang-Cheng Chen, 2011
- [Distributed Spectrum Sensing for Cognitive Radio Networks by Exploiting Sparsity](https://doi.org/10.1109/TSP.2009.2038417) — Juan Andres Bazerque, Georgios B. Giannakis, 2010 ⭐
- [Group-Lasso on Splines for Spectrum Cartography](http://arxiv.org/pdf/1010.0274) — Juan Andres Bazerque, Gonzalo Mateos, Georgios B. Giannakis, 2010 ⭐
- [Informed Spectrum Usage in Cognitive Radio Networks: Interference Cartography](https://doi.org/10.1109/PIMRC.2008.4699911) — Afef Ben Hadj Alaya-Feki, Sana Ben Jemaa, Berna Sayrac et al., 2008 ⭐

### Pathloss Prediction

- [R$^{2}$Net: 2D Deep Residual Learning with Height Embedding for 3D Radio Map Estimation](https://arxiv.org/abs/2605.18127) — Huiting Rao, Junyuan Wang, Huiling Zhu et al., 2026
- [A Machine Learning Framework for Large-Scale Static Wireless Mesh Networks](https://arxiv.org/abs/2605.23811) — Julia Andrusenko, 2026
- [Perceptual-Quality based AMC for Enhanced mmWave Spectral Efficiency: Concept and Experiment](https://arxiv.org/abs/2605.31499) — Kıvanç Değirmenci, Hasan Atalay Günel, Mohaned Chraiti et al., 2026
- [A physics-informed machine-learning model for wireless signal path loss prediction in underground infrastructure monitoring](https://doi.org/10.1016/j.tust.2026.107776) — Shuang Nie, Fei Wang, Qunfang Hu et al., 2026
- [A two-stage machine learning approach to path loss prediction at 5.9 GHz: benchmarking empirical and data-driven models for V2V highway scenarios](https://doi.org/10.1007/s12243-026-01178-5) — H. Fhima, H. Zormati, J. Chebil et al., 2026
- [Data-driven path loss prediction for urban V2V communications at 5.9 GHz: a two-stage machine learning framework](https://doi.org/10.1088/2631-8695/ae3b9f) — H. Fhima, H. Zormati, J. Chebil et al., 2026
- [Effective Outdoor Pathloss Prediction: A Multi-Layer Segmentation Approach With Weighting Map](https://doi.org/10.1109/tvt.2026.3658966) — Yuan Gao, Tao Wen, Wenjing Xie et al., 2026
- [Machine Learning Approach for the Modelling and Prediction of Path Loss Over GSM 4 & 5G Channels in Kano Metropolis, Nigeria](https://doi.org/10.46654/dy29kr76) — Hamza Ahmad Masari, A. Akinbolati, M. Sani, 2026
- [Machine-Learning-Based Path Loss Prediction and Data-Leakage-Avoidance Modeling for UAV Links](https://doi.org/10.1109/PACET68758.2026.11498248) — Achilleas Theocharopoulos, N. Moraitis, Athanasios D. Panagopoulos, 2026
- [Machine-Learning-Based Urban Path Loss Prediction at 900 MHz: Principal Component Analysis, Clustering, Feature Importance and Regression](https://doi.org/10.1109/OJAP.2025.3629578) — José Lorente-López, Ignacio Rodríguez-Rodríguez, J. Rodríguez et al., 2026
- [Model-Aided Learning for Sparse Received Signal Strength Indicator Radio Map Prediction and Wireless Signal Management in Internet of Things Environments](https://doi.org/10.1109/access.2026.3717372) — Ming-Kun Lu, A. Taparugssanagorn, 2026
- [On the Effectiveness of Radio Environmental Map Prediction Through Image-Based Deep Learning](https://doi.org/10.1109/tap.2026.3676109) — Mohammad Hossein Zadeh, M. Barbiroli, E. Vitucci et al., 2026
- [Path loss prediction for V2V communication using an advanced hybrid machine learning model based on real measurements](https://doi.org/10.1088/2631-8695/ae5e1f) — H. Zormati, J. Chebil, Jamel Bel Hadj Taher, 2026
- [RadioYNet: Efficient 3-D Path Loss Map Prediction With Height-Aware Feature Fusion](https://doi.org/10.1109/LAWP.2026.3693859) — Chengkai Liu, Guo Xia, Zeyu Cui et al., 2026
- [REM-Net+: Quantified 3D Radio Environment Map Construction Guided by Radio Propagation Model](https://doi.org/10.1109/TVT.2025.3623917) — Qi Chen, Ming Huang, Jingjing Yang, 2026
- [Investigating Map-Based Path Loss Models: A Study of Feature Representations in Convolutional Neural Networks](https://arxiv.org/abs/2501.07534) — Ryan G. Dempsey, Jonathan Ethier, H. Yanikomeroglu, 2025
- [TransPathNet: A Novel Two-Stage Framework for Indoor Radio Map Prediction](https://arxiv.org/abs/2501.16023) — Xin Li, Ran Liu, Saihua Xu et al., 2025
- [RadioDiff-Inverse: Diffusion Enhanced Bayesian Inverse Estimation for ISAC Radio Map Construction](https://arxiv.org/abs/2504.14298) — Xiucheng Wang, Zhongsheng Fang, Nan Cheng et al., 2025
- [RadioDiff-3D: A 3D× 3D Radio Map Dataset and Generative Diffusion Based Benchmark for 6G Environment-Aware Communication](https://arxiv.org/abs/2507.12166) — Xiucheng Wang, Qiming Zhang, Nan Cheng et al., 2025
- [A Multi-Scale Feature Extraction and Fusion U-Net for Pathloss Prediction in UAV-Assisted mmWave Radio Networks](https://arxiv.org/abs/2509.09606) — Sajjad Hussain, 2025
- [Machine Learning-based Path Loss Prediction in Suburban Environment in the Sub-6 GHz Band](https://arxiv.org/abs/2510.00696) — Ferdaous Tarhouni, M. Alzubi, M. Alouini, 2025
- [LLM4PG: Adapting Large Language Model for Pathloss Map Generation via Synesthesia of Machines](https://arxiv.org/abs/2511.02423) — Mingran Sun, Lu Bai, Xiang Cheng et al., 2025
- [WiCo-PG: Wireless Channel Foundation Model for Pathloss Map Generation via Synesthesia of Machines](https://arxiv.org/abs/2511.15030) — Mingran Sun, Lu Bai, Ziwei Huang et al., 2025
- [3D Urban Radio Map Estimation Based on UAV Sparse Measurement Data](https://doi.org/10.1109/ICCC68654.2025.11437905) — Wenqiang Chen, Xinwei Chen, Xiaofeng Zhong et al., 2025
- [A comparative analysis of machine learning models based on weighted input parameters for V2V path loss prediction in highway, rural, suburban, and urban environments](https://doi.org/10.1016/j.compeleceng.2025.110722) — N. Sağır, Zeynep Hasırcı Tuğcu, 2025
- [A deep-learning-based reconstruction method for 3D low-altitude propagation fields](https://doi.org/10.1117/12.3083929) — Chen Liang, Tianqi Xiang, Ya Liu et al., 2025
- [A Novel Hybrid Path Loss Prediction Model for 5G Midband Networks Using Empirical, Machine Learning, and Feature Prioritization Techniques](https://doi.org/10.1155/ijap/3277479) — F. Shaibu, E. N. Onwuka, N. Salawu et al., 2025
- [Channel Gain Map Estimation for Wireless Networks Based on Scatterer Model](https://doi.org/10.1109/TWC.2025.3557417) — He Sun, Lipeng Zhu, Rui Zhang, 2025
- [Efficient Indoor Radio Map Prediction with Improved Transformers and Active Sampling Strategies](https://doi.org/10.1109/MLSP62443.2025.11204304) — Zhihao Zheng, Limin Xiao, Ming Zhao et al., 2025
- [Enhancing Convolutional Models for Indoor Radio Mapping via Ray Marching](https://doi.org/10.1109/ICASSP49660.2025.10888520) — Mengfan Wu, Marco Skocaj, M. Boban, 2025
- [Evaluating the effectiveness of machine learning models for path loss prediction at 3.5 GHz with focus on feature prioritization](https://doi.org/10.4314/njt.v43i4.15) — F. Shaibu, E. N. Onwuka, N. Salawu et al., 2025
- [IPP-Net: A Generalizable Deep Neural Network Model for Indoor Pathloss Radio Map Prediction](https://doi.org/10.1109/ICASSP49660.2025.10890663) — Bin Feng, Meng Zheng, Wei Liang et al., 2025
- [Generalizable Indoor Path Loss Prediction](https://doi.org/10.1109/ICASSP49660.2025.10887696) — Cheick Tidiani Cisse, Oumaya Baala, V. Guillet et al., 2025
- [The First Indoor Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/ICASSP49660.2025.10889381) — Stefanos Bakirtzis, Çagkan Yapar, Kehai Qiu et al., 2025
- [IRM-Net: An Enhanced Attention Networks for Indoor Radio Map Estimation](https://doi.org/10.1109/MLSP62443.2025.11204298) — Qi Chen, Haidong Tan, Jingjing Yang et al., 2025
- [Sparse-Guided RadioUNet with Adaptive Sampling for the MLSP 2025 Sampling-Assisted Pathloss Radio Map Prediction Data Competition](https://doi.org/10.1109/MLSP62443.2025.11204292) — Ryoichi Kojima, Satoshi Ito, Tatsuya Nagao et al., 2025
- [Machine Learning-Based Path Loss Prediction Model for Wireless Sensor Networks in Urban Environments](https://doi.org/10.1109/COMP-SIF65618.2025.10969954) — H. R, S. M, Manjula Yerva et al., 2025
- [Machine Learning-Based Path Loss Prediction With Novel Diffraction and Morphology Features](https://doi.org/10.1109/LAWP.2025.3554519) — Beom Kwon, Hyeongyong Lim, Jaedon Park et al., 2025
- [Machine Learning-Based Underground Mine Path Loss Prediction Using mm-Wave Massive MIMO Measurements](https://doi.org/10.1109/TAP.2025.3595952) — S. Hadji, M. Nedil, 2025
- [Machine Learning-Based Vehicle-to-Ship Path Loss Prediction Using Offshore Measurements](https://doi.org/10.1109/VTC2025-Fall65116.2025.11310125) — Zheng Lv, Xiaoying Zhang, Xiaoran Liu et al., 2025
- [Machine Learning Driven Path Loss Prediction for 5G Networks in Smart Cities Metro Station Environments](https://doi.org/10.1109/ICDT63985.2025.10986662) — P. Yadav, Satyendra Sharma, P. Singh, 2025
- [Machine learning for improved path loss prediction in urban vehicle-to-infrastructure communication systems](https://doi.org/10.3389/frai.2025.1597981) — Mongi Ben Ameur, J. Chebil, M. Habaebi et al., 2025
- [Mmwave Path Loss Prediction using Machine Learning and Deep Learning Techniques](https://doi.org/10.1109/GIEST66547.2025.11387216) — Harsha Harrison, Chinnu Jacob, B. Babu et al., 2025
- [On the Impact of Terrain Types in Deep Neural Network-Based Surrogates of Radio Maps](https://doi.org/10.23919/ICMU65253.2025.11219164) — Fukuharu Tanaka, Takamasa Higuchi, Masaki Takanashi et al., 2025
- [Optimizing Path Loss Prediction for Air-Ground Communication Systems Using Hybrid Machine Learning Models: A Case Study of Linear Regression and PSO-Optimized Gradient Boosting Regressor](https://doi.org/10.36348/sjet.2025.v10i06.005) — Abdulaziz Maiwada, E. Adetiba, A. Ahmed et al., 2025
- [Path Loss Analysis and RSRP Prediction using Machine Learning Models](https://doi.org/10.1109/ETCOM66606.2025.11436508) — K. Srinivas, K. Jyostna, Ch. Pranaya Kumar et al., 2025
- [Path Loss Prediction in Wireless Communication Using Machine Learning](https://doi.org/10.1109/INCET64471.2025.11140119) — Praveen Kadakol, Bhargav Joshi, Rohan Chunamuri et al., 2025
- [Path Loss Prediction Using Machine Learning with Extended Features](https://doi.org/10.1109/AP-S/CNC-USNC-URSI55537.2025.11266241) — Jonathan Ethier, Mathieu Châteauvert, Ryan G. Dempsey et al., 2025
- [Radio Map Prediction via Neural Networks with Ground Truth Shortcuts and Selective Sampling](https://doi.org/10.1109/MLSP62443.2025.11204216) — Mengfan Wu, Marco Skocaj, M. Boban, 2025
- [RMTransformer: Accurate Radio Map Construction and Coverage Prediction](https://doi.org/10.1109/VTC2025-Spring65109.2025.11174709) — Yuxuan Li, Cheng Zhang, Wen Wang et al., 2025
- [Saipp-Net: A Sampling-Assisted Indoor Pathloss Prediction Method for Wireless Communication Systems](https://doi.org/10.1109/MLSP62443.2025.11204326) — Bin Feng, Meng Zheng, Wei Liang et al., 2025
- [SamplerUNet: Data Efficient Pathloss Map Prediction](https://doi.org/10.1109/IEEECONF67917.2025.11443800) — Omer Gokalp Serbetci, Pradeep Mahtiyarasu, A. Molisch, 2025
- [SIP2Net: Situational-Aware Indoor Pathloss-Map Prediction Network for Radio Map Generation](https://doi.org/10.1109/ICASSP49660.2025.10890319) — Wenlihan Lu, Ziyi Lu, Jia Yan et al., 2025
- [Enhancing Pathloss Estimation with Vision Transformers and Direct Wave Power Integration](https://doi.org/10.23919/eusipco63237.2025.11226433) — Yuuki Tachioka, 2025
- [U-Net Based Indoor Radio Map Prediction Under Sparse Sampling](https://doi.org/10.1109/MLSP62443.2025.11204227) — Tianxiang Xing, Leyi Zou, Tejas Bharadwaj et al., 2025
- [U-Net for Indoor Pathloss Prediction from Sparse Measurements with Physics-Based Features](https://doi.org/10.1109/MLSP62443.2025.11204276) — K. Petrosyan, Rafayel Mkrtchyan, Hrant Khachatrian et al., 2025
- [The Sampling-Assisted Pathloss Radio Map Prediction Competition](https://doi.org/10.1109/MLSP62443.2025.11204278) — Çagkan Yapar, Stefanos Bakirtzis, Andra Lutu et al., 2025
- [Simulation-Enhanced Data Augmentation for Machine Learning Pathloss Prediction](https://arxiv.org/abs/2402.01969) — Ahmed P. Mohamed, Byunghyun Lee, Yaguang Zhang et al., 2024
- [Radio Map Prediction From Aerial Images and Application to Coverage Optimization](https://arxiv.org/abs/2410.17264) — Fabian Jaensch, Giuseppe Caire, B. Demir, 2024
- [A Comparative Analysis of Machine Learning Ensemble Methods for Accurate Path Loss Prediction](https://doi.org/10.52783/jes.8467) — Awal Halifa, E. A. Ampomah, K. Gyasi et al., 2024
- [A Deep Probabilistic Machine Learning Approach to Ray Tracing Path Loss Prediction at 900 MHz](https://doi.org/10.1109/TAP.2024.3465840) — S. Sotiroudis, M. Matin, Shaohua Wan et al., 2024
- [A Machine Learning Approach for Path Loss Prediction Using Combination of Regression and Classification Models](https://doi.org/10.3390/s24175855) — I. Iliev, Y. Velchev, Peter Z. Petkov et al., 2024
- [A Machine Learning Approach for the Prediction of Indoor Propagation Path-Loss in the Tera-Hertz Bands](https://doi.org/10.1109/access.2024.3472549) — Nagma Elburki, Affes Sofiéne, 2024
- [ANALYSIS OF 5G CELLULAR TECHNOLOGY PATHLOSS PREDICTION ON MICRO URBAN CELLS USING ABG PREDICTION MODEL IN PONTIANAK CITY](https://jurnal.untan.ac.id/index.php/TELECTRICAL/article/download/69802/pdf) — Alfodaniel Theodorus Barahama, Fitri Imansyah, Eka Kusumawardhani, 2024
- [Comparing Exponential Decay Models for Path Loss Prediction at 5.8 GHz Using Machine Learning Techniques](https://doi.org/10.1109/LACAP63752.2024.10876251) — Leoni Marti Miranda Saravia, Alejandro Rommel Miranda Saravia, Marcelo Molina Silva et al., 2024
- [Comparison of Machine Learning Algorithms for Propagation Path Loss Prediction Using Ray Tracing Data](https://doi.org/10.1109/ICTC62082.2024.10826992) — Chaewon Yoon, Junseok Kim, Hyuk-Je Kim et al., 2024
- [Enhanced Path Loss Prediction Using Machine Learning and Modified COST-Hata Model for High-Frequency Wireless Networks](https://doi.org/10.52783/jes.8642) — Awal Halifa, K. Gyasi, E. A. Ampomah et al., 2024
- [Enhancing Path Loss Prediction Through Explainable Machine Learning Approach](https://doi.org/10.1109/WINCOM62286.2024.10655363) — Ibrahim Yazici, Emrecan Özkan, Emre Gures, 2024
- [Exploring Machine Learning Techniques for Path Loss Prediction in LoRa Networks](https://doi.org/10.1109/ISWCS61526.2024.10639055) — R. Ballestrin, J. Feijó, M. Feldman et al., 2024
- [Geometrical Features Based-mmWave UAV Path Loss Prediction Using Machine Learning for 5G and Beyond](https://doi.org/10.1109/OJCOMS.2024.3450089) — Sajjad Hussain, Syed F. N. Bacha, A. Cheema et al., 2024
- [Intelligent Path Loss Prediction for IoT Connectivity in 5G Networks using Hybrid Machine Learning Techniques](https://doi.org/10.1109/SEB4SDG60871.2024.10630409) — Samuel Robinson, Anthony Imianvan, 2024
- [Machine-Learning-Based Path Loss Prediction for In-Cabin Wireless Networks](https://doi.org/10.1109/ICMLCN59089.2024.10624765) — N. Moraitis, Lefteris Tsipi, D. Vouyioukas, 2024
- [Machine-Learning-Based Path Loss Prediction for Vehicle-to-Vehicle Communication in Highway Environments](https://doi.org/10.3390/app14177545) — N. Sağır, Zeynep Hasırcı Tuğcu, 2024
- [Marine Radio Path Loss Prediction under Different Wind Speeds Based on Machine Learning](https://doi.org/10.1109/APCAP62011.2024.10882102) — Tao Jin, Shuo Feng, Hongjuan Zhou et al., 2024
- [Overview of the First Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/OJSP.2024.3419563) — Çagkan Yapar, Fabian Jaensch, Ron Levie et al., 2024
- [Path Loss Prediction Model Based on Enhanced Environment Characterization](https://doi.org/10.1109/ISAPE62431.2024.10840580) — Longwei Wang, Fei Du, Bo Zhu et al., 2024
- [RadioDiff: An Effective Generative Diffusion Model for Sampling-Free Dynamic Radio Map Construction](https://github.com/UNIC-Lab/RadioDiff) — Xiucheng Wang, Keda Tao, Nan Cheng et al., 2024 ⭐
- [UAV-Assisted Active Sparse Crowdsensing for Ground Signal Map Construction Based on 3-D Spatial–Temporal Correlation](https://doi.org/10.1109/JIOT.2024.3399409) — Chengyong Liu, Kun Zhu, Chaoquan Tao et al., 2024
- [Vision Transformers for Efficient Indoor Pathloss Radio Map Prediction](https://doi.org/10.3390/electronics14101905) — Edvard Ghukasyan, Hrant Khachatrian, Rafayel Mkrtchyan et al., 2024
- [Distributed Split Learning for Map-Based Signal Strength Prediction Empowered by Deep Vision Transformer](https://doi.org/10.1109/TVT.2023.3320643) — Haiyao Yu, Changyang She, Chentao Yue et al., 2024
- [A Robust Machine Learning Approach for Path Loss Prediction in 5G Networks with Nested Cross Validation](https://arxiv.org/abs/2310.01030) — Ibrahim Yazici, Emre Gures, 2023
- [A Scalable and Generalizable Pathloss Map Prediction](https://arxiv.org/abs/2312.03950) — Ju-Hyung Lee, A. Molisch, 2023
- [A Kriging-Based Radio Environment Map Construction and Channel Estimation System in Threatening Environments](https://doi.org/10.1109/ACCESS.2023.3267973) — Ying Gao, T. Fujii, 2023
- [Accurate Energy Efficiency Prediction in Sub-6GHz Radio Access Networks Based on Pathloss Modeling Using Kriging Methods](https://doi.org/10.1109/ICCWorkshops57953.2023.10283548) — Hao-Jen Fu, Timothy O'Farrell, 2023
- [Analysis of Millimeter Wave Path Loss Prediction using Machine Learning Techniques](https://doi.org/10.1109/WiSPNET57748.2023.10134020) — V. R, V. G, S. Ramanathan et al., 2023
- [Augmented RF Propagation Modeling](https://doi.org/10.1109/JRFID.2023.3285452) — Serhat Tadik, Michael A. Varner, Frost Mitchell et al., 2023
- [Transformer-Based Neural Surrogate for Link-Level Path Loss Prediction from Variable-Sized Maps](https://arxiv.org/abs/2310.04570) — Thomas M. Hehn, Tribhuvanesh Orekondy, O. Shental et al., 2023
- [The First Pathloss Radio Map Prediction Challenge](https://arxiv.org/abs/2310.07658) — Çagkan Yapar, Fabian Jaensch, Ron Levie et al., 2023
- [Agile Radio Map Prediction Using Deep Learning](https://doi.org/10.1109/icassp49357.2023.10096546) — Enes Krijestorac, Hazem Sallouha, Shamik Sarkar et al., 2023
- [PMNet: Large-Scale Channel Prediction System for ICASSP 2023 First Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/ICASSP49357.2023.10095257) — Ju-Hyung Lee, Joohan Lee, Seong-Bae Lee et al., 2023
- [Machine Learning-Assisted Path Loss Prediction Across Multiple Frequency Bands using a Multi-Fidelity Surrogate Model](https://doi.org/10.1109/IWS58240.2023.10222265) — Meng Zhao, Cheng Yi, Haiming Wang et al., 2023
- [Path Loss Prediction for Vehicular-to-Infrastructure Communication Using Machine Learning Techniques](https://doi.org/10.1109/VCC60689.2023.10474798) — Yoiz Nuñez, Lisandro Lovisolo, L. da Silva Mello et al., 2023
- [Path Loss Prediction in Urban Areas: A Machine Learning Approach](https://doi.org/10.1109/LAWP.2022.3225792) — I. Rafie, Soo Yong Lim, M. Chung, 2023
- [A Deep Learning-Based Indoor Radio Estimation Method Driven by 2.4 GHz Ray-Tracing Data](https://ieeexplore.ieee.org/ielx7/6287639/6514899/10347228.pdf) — Changwoo Pyo, Hirokazu Sawada, Takeshi Matsumura, 2023
- [Deep Learning-Based Path Loss Prediction for Outdoor Wireless Communication Systems](https://doi.org/10.1109/icassp49357.2023.10095501) — Kehai Qiu, Stefanos Bakirtzis, Hui Song et al., 2023
- [RNN-Based Path Loss Modeling with Variable-Size Map Data in Urban Environments](https://doi.org/10.1109/VTC2023-Spring57618.2023.10199449) — Tatsuya Nagao, Takahiro Hayashi, 2023
- [REM-U-Net: Deep Learning Based Agile REM Prediction With Energy-Efficient Cell-Free Use Case](https://ieeexplore.ieee.org/ielx7/8782710/9006934/10474197.pdf) — Hazem Sallouha, Shamik Sarkar, Enes Krijestorac et al., 2023
- [TeraHertz Path-Loss Prediction Indoor using Machine Learning](https://doi.org/10.1109/IC_ASET58101.2023.10151166) — Nagma Elburki, Affes Sofiéne, 2023
- [Machine Learning-Based Urban Canyon Path Loss Prediction Using 28 GHz Manhattan Measurements](https://arxiv.org/abs/2202.05107) — Ankit Gupta, Jinfeng Du, D. Chizhik et al., 2022
- [PMNet: Robust Pathloss Map Prediction via Supervised Learning](https://arxiv.org/abs/2211.10527) — Ju-Hyung Lee, Omer Gokalp Serbetci, Dhruv Selvam et al., 2022 ⭐
- [Basic Study of Map Image Processing for Simple Path Loss Prediction Using CNN](https://doi.org/10.1109/iWEM52897.2022.9993557) — K. Itoi, H. Nakabayashi, 2022
- [LARGE INTELLIGENT SURFACE-ASSISTED WIRELESS COMMUNICATION AND PATH LOSS PREDICTION MODEL BASED ON ELECTROMAGNETICS AND MACHINE LEARNING ALGORITHMS](https://www.jpier.org/ac_api/download.php?id=22013002) — Wael S. Elshennawy, 2022
- [PATH LOSS PREDICTION BASED ON MACHINE LEARNING TECHNIQUES: SUPPORT VECTOR MACHINE, ARTIFICIAL NEURAL NETWORK, AND MULTILINEAR REGRESSION MODEL](https://www.openjournalsnigeria.org.ng/journals/index.php/ojps/article/download/393/191) — J. Idogho, G. George, 2022
- [Path Loss Prediction in Tropical Regions Using Machine Learning Techniques: A Case Study](https://www.mdpi.com/2079-9292/11/17/2711/pdf?version=1662027650) — O. J. Famoriji, T. Shongwe, 2022
- [Path-Loss Prediction of Millimeter-wave using Machine Learning Techniques](https://doi.org/10.1109/LATINCOM56090.2022.10000523) — Yoiz Nuñez, LISANDRO LOVISOLO, L. Mello et al., 2022
- [Pseudo Ray-Tracing: Deep Learning Assisted Outdoor mm-Wave Path Loss Prediction](https://doi.org/10.1109/lwc.2022.3175091) — Kehai Qiu, Stefanos Bakirtzis, Hui Song et al., 2022
- [Radio Environment Map of an LTE Deployment Based on Machine Learning Estimation of Signal Levels](https://biblio.ugent.be/publication/01GX36XYPXKB35WX7JAGRXKTSZ/file/01GX37CMWKASNB67NCVVDE2JP2.pdf) — Yosvany Hervis Santana, D. Plets, Rodney Martinez Alonso et al., 2022
- [Regression of Large-Scale Path Loss Parameters Using Deep Neural Networks](https://doi.org/10.1109/lawp.2022.3174357) — Mustafa Bal, Ahmed Marey, H. Ates et al., 2022
- [LocUNet: Fast Urban Positioning Using Radio Maps and Deep Learning](https://doi.org/10.1109/icassp43922.2022.9747240) — Çagkan Yapar, R. Levie, Gitta Kutyniok et al., 2022
- [Predictive Modeling of Millimeter-Wave Vegetation-Scattering Effect Using Hybrid Physics-Based and Data-Driven Approach](https://doi.org/10.1109/TAP.2021.3118463) — Peize Zhang, Cheng Yi, Bensheng Yang et al., 2022
- [CDI Maps: Dynamic Estimation of the Radio Environment for Predictive Resource Allocation](https://doi.org/10.1109/pimrc50174.2021.9569310) — D. Külzer, S. Stańczak, Mladen Botsov, 2021
- [ML-based delay–angle-joint path loss prediction for UAV mmWave channels](https://doi.org/10.1007/s11276-021-02817-6) — Kai Mao, Benzhe Ning, Qiuming Zhu et al., 2021
- [Performance evaluation of machine learning methods for path loss prediction in rural environment at 3.7 GHz](https://doi.org/10.1007/s11276-021-02682-3) — N. Moraitis, Lefteris Tsipi, D. Vouyioukas et al., 2021
- [Radio Map Estimation Using a Generative Adversarial Network and Related Business Aspects](https://doi.org/10.1109/wpmc52694.2021.9700474) — S. Vankayala, Swaraj Kumar, Ishaan Roy et al., 2021
- [Radio Propagation Estimation in a Long-Range Environment using a Deep Neural Network](https://doi.org/10.23919/EuCAP51087.2021.9411398) — Satoshi Ito, Takahiro Hayashi, 2021
- [DRaGon: Mining Latent Radio Channel Information from Geographical Data Leveraging Deep Learning](https://arxiv.org/abs/2112.07941) — Benjamin Sliwa, Melina Geis, Caner Bektas et al., 2021
- [The determination of pathloss model for ultra‐high‐frequency television transmission in Onitsha, Anambra state, Nigeria](https://doi.org/10.1002/dac.4716) — Nurudeen Oladapo Olatoye, Erumena Constance Ekoko, Ogirima Mohammed Sani et al., 2021
- [Real-Time Outdoor Localization Using Radio Maps: A Deep Learning Approach](https://arxiv.org/abs/2106.12556) — Çagkan Yapar, R. Levie, Gitta Kutyniok et al., 2021 ⭐
- [Pathloss Prediction using Deep Learning with Applications to Cellular Optimization and Efficient D2D Link Scheduling](https://doi.org/10.1109/ICASSP40776.2020.9053347) — Ron Levie, Çagkan Yapar, Gitta Kutyniok et al., 2020
- [Path Loss Prediction Based on Machine Learning Techniques: Principal Component Analysis, Artificial Neural Network, and Gaussian Process](https://www.mdpi.com/1424-8220/20/7/1927/pdf?version=1586396974) — Han-Shin Jo, Chanshin Park, Eunhyoung Lee et al., 2020
- [Radio Environment Map Construction with Joint Space-Frequency Interpolation](https://doi.org/10.1109/ICAIIC48513.2020.9065217) — Koya Sato, Kei Inage, T. Fujii, 2020
- [RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks](https://arxiv.org/abs/1911.09002) — Ron Levie, Çağkan Yapar, Gitta Kutyniok et al., 2019 ⭐
- [Path Loss Prediction Based on Machine Learning: Principle, Method, and Data Expansion](https://www.mdpi.com/2076-3417/9/9/1908/pdf?version=1557393866) — Yan Zhang, Jinxiao Wen, Guanshu Yang et al., 2019
- [Radio Environment Map Updating Procedure Based on Hypothesis Testing](https://doi.org/10.1109/DySPAN.2019.8935724) — Keita Katagiri, T. Fujii, 2019
- [Received signal strength and local terrain profile data for radio network planning and optimization at GSM frequency bands](https://doi.org/10.1016/j.dib.2017.12.036) — S. Popoola, Atayero, N. Faruk, 2017
- Feature Extraction for Neural Network Wave Propagation Loss Models from Field Measurements and Digital Elevation Map — Seomin Yang, Hyukjoon Lee, 1999
- [Propagation Measurements and Models for Wireless Communications Channels](https://doi.org/10.1109/35.468198) — Theodore S. Rappaport, 1996 ⭐

### Channel Knowledge Maps (CKM)

- [Channel Knowledge Map Construction via Guided Flow Matching](https://arxiv.org/abs/2601.06156) — Ziyu Huang, Yong Zeng, Shen Fu et al., 2026
- [BeamCKMDiff: Beam-Aware Channel Knowledge Map Construction via Diffusion Transformer](https://arxiv.org/abs/2601.10207) — Le Zhao, Yining Wang, Xinyi Wang et al., 2026
- [Data-Model Co-Driven Continuous Channel Map Construction: A Perceptive Foundation for Embodied Intelligent Agents in 6G Networks](https://arxiv.org/abs/2604.01060) — Tianrun Qi, Cheng-Xiang Wang, Chen-Yen Huang et al., 2026
- [A Novel 6G Dynamic Channel Map Based on a Hybrid Channel Model](https://arxiv.org/abs/2604.15083) — Tianrun Qi, Chengxiang Wang, Chen-Yen Huang et al., 2026
- [28 GHz Indoor Continuous-Space Channel Measurements and AI-Enabled 6G Channel Map Construction](https://doi.org/10.1109/tcomm.2026.3690362) — Tianrun Qi, Cheng-Xiang Wang, Chen-Yen Huang et al., 2026
- [Wireless Channel Map Enabled Instantaneous Channel State Information Acquisition in High-Mobility Scenarios](https://doi.org/10.1109/TCOMM.2026.3663282) — Yinglan Bu, Cheng-Xiang Wang, Chen-Yen Huang et al., 2026
- [CKMImageNet: A Dataset for AI-Based Channel Knowledge Map Toward Environment-Aware Communication and Sensing](https://arxiv.org/abs/2504.09849) — Zijian Wu, Di Wu, Shen Fu et al., 2025
- [Beamforming-Codebook-Aware Channel Knowledge Map Construction for Multi-Antenna Systems](https://arxiv.org/abs/2505.16132) — Haohan Wang, Xu Shi, Hengyu Zhang et al., 2025
- [6D Channel Knowledge Map Construction via Bidirectional Wireless Gaussian Splatting](https://arxiv.org/abs/2510.26166) — Juncong Zhou, Chao Hu, Guanlin Wu et al., 2025
- [Channel Knowledge Map-Assisted Dual-Domain Tracking and Predictive Beamforming for High-Mobility Wireless Networks](https://doi.org/10.1109/TWC.2026.3654755) — Ruolin Du, Zhiqiang Wei, Zai Yang et al., 2025
- [Joint Trajectory and Transmit Power Design for Cellular-Connected UAVs via Differentiable Channel Knowledge Map](https://doi.org/10.1109/TVT.2025.3567741) — Yuan Li, Xinyao Wang, Zhong Zheng et al., 2025
- [Scene Structure Based Neural Radio-Frequency Radiance Fields for Channel Knowledge Map Construction](https://doi.org/10.1109/LWC.2025.3615621) — Kai Liu, Wenjun Jiang, Xiaojun Yuan, 2025
- [Channel Knowledge Map Construction: Recent Advances and Open Challenges](https://doi.org/10.1109/mwc.2026.3668205) — Zixiang Ren, Juncong Zhou, Jie Xu et al., 2025
- [Deep Learning-Based Millimeter Wave Beam Recommendation via Channel Knowledge Map](https://doi.org/10.1109/LWC.2025.3551496) — Chen Shao, Chunshan Liu, Lou Zhao et al., 2025
- [Trajectory Optimization for Cellular-Connected UAV in Complex Environment With Partial CKM](https://doi.org/10.1109/TCOMM.2026.3689212) — Yuxuan Song, Haiquan Lu, Chiya Zhang et al., 2025
- [Point Cloud Environment-Based Channel Knowledge Map Construction](https://doi.org/10.48550/arXiv.2503.01234) — Yancheng Wang, Wei Guo, Chuan Huang et al., 2025
- [Towards Precise Channel Knowledge Map: Exploiting Environmental Information from 2D Visuals to 3D Point Clouds](https://doi.org/10.48550/arXiv.2502.01234) — Yancheng Wang, Chuan Huang, Songyang Zhang et al., 2025
- [BeamCKM: A Framework of Channel Knowledge Map Construction for Multi-Antenna Systems](https://github.com/github-whh/BeamCKM) — Haohan Wang, Xu Shi, Hengyu Zhang et al., 2025
- [Channel Knowledge Map-Aided Channel Prediction With Measurements-Based Evaluation](https://doi.org/10.1109/TCOMM.2024.3487310) — Xianling Wang, Yi-xing Shi, Tianci Wang et al., 2025
- [You May Use the Same Channel Knowledge Map for Environment-Aware NLoS Sensing and Communication](https://doi.org/10.1109/TWC.2026.3678277) — Di Wu, Zhuoyin Dai, Yong Zeng, 2025
- [Channel Knowledge Map Construction via Physics-Inspired Diffusion Model Without Prior Observations](https://doi.org/10.48550/arXiv.2506.01234) — Yunzhe Zhu, Xuewen Liao, Zhenzhen Gao et al., 2025
- [An I2I Inpainting Approach for Efficient Channel Knowledge Map Construction](https://arxiv.org/abs/2406.09822) — Zhe-Xue Jin, Li You, Jue Wang et al., 2024
- [Interference-Cancellation-Based Channel Knowledge Map Construction and Its Applications to Channel Estimation](https://arxiv.org/abs/2409.00461) — Wenjun Jiang, Xiaojun Yuan, Boyu Teng et al., 2024
- [IMNet: Interference-Aware Channel Knowledge Map Construction and Localization](https://arxiv.org/abs/2412.01279) — Le Zhao, Zesong Fei, Xinyi Wang et al., 2024
- [6G Dynamic Channel Map Construction Based on AI and Image Processing](https://doi.org/10.1109/ICCT62411.2024.10946643) — Lixiang Song, Junling Li, Tong Wu et al., 2024
- [Can Channel Knowledge Map Help to Predict Instantaneous MIMO Channel State Information?](https://doi.org/10.1109/WCNC57260.2024.10570728) — Xianling Wang, Yi-xing Shi, Tianci Wang et al., 2024
- [Channel Knowledge Map Construction with Laplacian Pyramid Reconstruction Network](https://doi.org/10.1109/WCNC57260.2024.10570885) — Zhe-Xue Jin, Li You, Jue Wang et al., 2024
- [Deep Machine Learning-Based AoD Map and AoA Map Construction for Wireless Networks](https://doi.org/10.1109/VTC2024-Spring62846.2024.10683141) — Ronghong Mo, Yiyang Pei, Sumei Sun et al., 2024
- [Energy Minimization for Federated Learning Based Radio Map Construction](https://doi.org/10.1109/tmlcn.2024.3453212) — Fahui Wu, Yunfei Gao, Lin Xiao et al., 2024
- [A Deep Learning Framework for Wireless Radiation Field Reconstruction and Channel Prediction](https://arxiv.org/abs/2403.03241) — Haofan Lu, Christopher Vattheuer, Baharan Mirzasoleiman et al., 2024
- [Channel Knowledge Map Construction Based on a UAV-Assisted Channel Measurement System](https://doi.org/10.3390/drones8050191) — Yanheng Qiu, Xiaomin Chen, Kai Mao et al., 2024
- [Deep Learning-Based CKM Construction with Image Super-Resolution](https://doi.org/10.1109/VTC2025-Spring65109.2025.11174933) — Shiyu Wang, Xiaoli Xu, Yong Zeng, 2024
- [Environment-Aware Channel Estimation via Integrating Channel Knowledge Map and Dynamic Sensing Information](https://doi.org/10.1109/LWC.2024.3482357) — Di Wu, Yuelong Qiu, Yong Zeng et al., 2024
- [CKMImageNet: A Comprehensive Dataset to Enable Channel Knowledge Map Construction via Computer Vision](https://doi.org/10.1109/ICCCWorkshops62562.2024.10693754) — Di Wu, Zijian Wu, Yuelong Qiu et al., 2024
- [Aerial Video Streaming Over 3D Cellular Networks: An Environment and Channel Knowledge Map Approach](https://doi.org/10.1109/TWC.2023.3289501) — Cheng Zhan, Han Hu, Zhi Liu et al., 2024
- [RF-3DGS: Wireless Channel Modeling With Radio Radiance Field and 3D Gaussian Splatting](https://github.com/SunLab-UGA/RF-3DGS) — Lihao Zhang, Haijian Sun, S. Berweger et al., 2024
- [Strategic Application of AIGC for UAV Trajectory Design: A Channel Knowledge Map Approach](https://arxiv.org/abs/2412.00386) — Chiya Zhang, Ting Wang, Rubing Han et al., 2024
- [Prototyping and Experimental Results for ISAC-Based Channel Knowledge Map](https://doi.org/10.1109/TVT.2025.3545785) — Chaoyue Zhang, Zhiwen Zhou, Xiaoli Xu et al., 2024
- [How Much Data Is Needed for Channel Knowledge Map Construction?](https://arxiv.org/abs/2312.06966) — Xiaoli Xu, Yong Zeng, 2023
- [Millimeter Wave Wireless Channel Knowledge Map Construction Based on Path Matching and Environment Partitioning](https://downloads.hindawi.com/journals/wcmc/2023/6671048.pdf) — Zeyang Li, Qidong Gao, Wence Zhang et al., 2023
- [Environment-Aware Joint Active/Passive Beamforming for RIS-Aided Communications Leveraging Channel Knowledge Map](https://ieeexplore.ieee.org/ielx7/4234/5534602/10108969.pdf) — E. Taghavi, Ramin Hashemi, N. Rajatheva et al., 2023
- [Environment-Aware Coordinated Multi-Point mmWave Beam Alignment Via Channel Knowledge Map](https://doi.org/10.1109/ICCWorkshops57953.2023.10283607) — Di Wu, Yong Zeng, 2023
- [A Tutorial on Environment-Aware Communications via Channel Knowledge Map for 6G](https://arxiv.org/abs/2309.07460) — Yong Zeng, Junting Chen, Jie Xu et al., 2023 ⭐
- [Environment-Aware Hybrid Beamforming by Leveraging Channel Knowledge Map](https://arxiv.org/abs/2206.08707) — Di Wu, Yong Zeng, Shize Jin et al., 2022
- [Channel Knowledge Map (CKM)-Assisted Multi-UAV Wireless Network: CKM Construction and UAV Placement](https://arxiv.org/abs/2207.01931) — Haoyun Li, Peiming Li, Jie Xu et al., 2022
- [Channel Knowledge Map for Environment-Aware Communications: EM Algorithm for Map Construction](https://arxiv.org/abs/2108.06960) — Kun Li, Peiming Li, Yong Zeng et al., 2021
- [Toward Environment-Aware 6G Communications via Channel Knowledge Map](https://doi.org/10.1109/MWC.001.2000327) — Yong Zeng, Xiaoli Xu, 2021 ⭐
<!-- AUTO:papers END -->

## Datasets & Benchmarks

<!-- AUTO:datasets START -->
| Dataset | Description | Papers using |
|---------|-------------|--------------|
| [CKMImageNet](https://doi.org/10.1109/ICCCWorkshops62562.2024.10693754) | Large-scale ray-tracing dataset pairing location-tagged numerical channel knowledge (path loss, delay spread, etc.) with co-registered environmental images across diverse outdoor scenarios. Purpose-built to enable computer-vision methods for Channel Knowledge Map construction in 6G research. | 4 |
| [ICASSP 2023 Pathloss Radio Map Prediction Challenge Dataset](https://arxiv.org/abs/2310.07658) | Standardized outdoor urban pathloss dataset released alongside the first ICASSP pathloss map prediction challenge. Provides building maps, transmitter locations, and pathloss ground truth for training, validation, and held-out test splits to enable fair comparison across deep-learning approaches. | 4 |
| [ICASSP 2025 Indoor Pathloss Challenge Dataset](https://doi.org/10.1109/ICASSP49660.2025.10889381) | Indoor directional pathloss dataset introduced for the ICASSP 2025 challenge. Covers diverse floor plans with directional antenna emission patterns, extending outdoor challenge benchmarking methodology to indoor propagation environments. | 2 |
| [RadioMapSeer (RadioUNet Dataset)](https://radiomapseer.github.io) | Large-scale simulated urban outdoor pathloss dataset generated with WinProp ray-tracing over 700 diverse city maps at 256×256 resolution. Provides transmitter location, building footprint, and pathloss ground-truth maps; the de-facto benchmark for outdoor pathloss radio map estimation since 2021. | 10 |
| [Spectrum Cartography Synthetic / Simulation Datasets](https://github.com/uiano/spectrum_surveying_with_UAVs) | A family of synthetic datasets used across spectrum cartography literature, generated via stochastic propagation models (log-distance path loss + shadowing) or tensor-based multi-source emitter models. Used widely to benchmark Kriging, group-lasso, and tensor-completion spectrum cartography methods. | 7 |
| [WiFi Indoor Measurement Datasets](https://arxiv.org/abs/2502.10472) | Real-world indoor WiFi received-signal-strength (RSS) datasets collected in office and campus environments at varying sample densities. Used to benchmark diffusion and learning-based methods for fine-grained indoor radio map estimation at ultra-low sampling rates. | 4 |
<!-- AUTO:datasets END -->

## Contributing

Contributions are welcome. To add or correct a paper, open an issue with the
**Add a paper** form, or submit a pull request adding one file to
[`data/papers/`](data/papers). See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the
field reference in [`schema/README.md`](schema/README.md).

The paper list and the sections above are **generated** — do not hand-edit them.
Edit the YAML in `data/`; CI regenerates this README on merge.

## License

- **Code** (`scripts/`, `site/`): MIT — see [`LICENSE`](LICENSE).
- **Data & content** (`data/`, generated README and site content): CC-BY-4.0 —
  see [`LICENSE-DATA`](LICENSE-DATA).
