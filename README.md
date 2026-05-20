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
![Papers](https://img.shields.io/badge/papers-107-informational)
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
**107** papers · **4** subfields · **20** milestone papers

Coverage spans **1996–2026**.
By subfield — Channel Knowledge Maps (CKM): 26, Radio Environment Maps (REM): 25, Pathloss Prediction: 28, Spectrum Cartography: 28.
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
- [3-D Radio Map Estimation Based on Active Measurement Trajectory Selection](https://doi.org/10.1109/LWC.2025.3557556) — Zhibo Chen, Heng Wang, Daoxing Guo, 2025
- [Grid-Free Radio Map Estimation via Unsupervised Implicit Continuous Representation](https://doi.org/10.1109/LSP.2025.3601038) — Xiaonan Chen, Jun Wang, 2025
- [Bayesian Radio Map Estimation: Fundamentals and Implementation via Diffusion Models](https://doi.org/10.48550/arXiv.2502.09998) — Tien Ngoc Ha, Daniel Romero, 2025
- [Leveraging Transfer Learning for Radio Map Estimation via Mixture of Experts](https://doi.org/10.1109/TCCN.2025.3570469) — Rahul Kumar Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2025
- [Paying Deformable Attention to Sparse Spatial Observations for Deep Radio Map Estimation](https://github.com/AkonLau/DAT-Unet) — Kangjun Liu, Chunyan Qiu, Ke Chen et al., 2025
- [Physics-Inspired Distributed Radio Map Estimation](https://doi.org/10.1109/ICC52391.2025.11161293) — Dong Yang, Yue Wang, Songyang Zhang et al., 2025
- [RadioFormer: A Multiple-Granularity Radio Map Estimation Transformer with 1‱ Spatial Sampling](https://arxiv.org/abs/2504.19161) — Zheng Fang, Kangjun Liu, Ke Chen et al., 2025
- [Denoising Diffusion Probabilistic Model for Radio Map Estimation in Generative Wireless Networks](https://doi.org/10.1109/TCCN.2025.3529879) — Xuanhao Luo, Zhizhen Li, Zhiyuan Peng et al., 2025
- [WiFi-Diffusion: Achieving Fine-Grained WiFi Radio Map Estimation With Ultra-Low Sampling Rate by Diffusion Models](https://doi.org/10.1109/JSAC.2025.3584562) — Zhiyuan Liu, Shuhang Zhang, Qingyu Liu et al., 2025
- [Radio Map Estimation Based on Generative Artificial Intelligence: Evolution from Point-Level to Cell-Level Prediction](https://doi.org/10.1109/MCOM.005.2400027) — Yi Zheng, Ji Wang, Wenwu Xie et al., 2025
- [Diffraction and Scattering Aware Radio Map and Environment Reconstruction Using Geometry Model-Assisted Deep Learning](https://arxiv.org/abs/2403.00229) — Wangqian Chen, Junting Chen, 2024
- [Radio Environment Map Construction Based on Privacy-Centric Federated Learning](https://ieeexplore.ieee.org/ielx7/6287639/10380310/10440080.pdf) — Shafi Ullah Khan, Carla E. García, Taewoong Hwang et al., 2024
- [Data-Driven Radio Environment Map Estimation Using Graph Neural Networks](https://doi.org/10.1109/ICCWorkshops59551.2024.10615637) — Ali Shibli, Tahar Zanouda, 2024
- [A Deep-Learning Approach to a Volumetric Radio Environment Map Construction for UAV-Assisted Networks](https://downloads.hindawi.com/journals/ijap/2024/9062023.pdf) — Bezawit Sahilu Shawel, Dereje H. Woldegebreal, Sofie Pollin, 2024
- [Neural Representation for Wireless Radiation Field Reconstruction: A 3D Gaussian Splatting Approach](https://github.com/wenchaozheng/WRF-GSplus) — Chaozheng Wen, Jingwen Tong, Yingdong Hu et al., 2024
- [UAV-Aided Radio Map Construction Exploiting Environment Semantics](https://arxiv.org/abs/2107.10574) — Wenjie Liu, Junting Chen, 2023
- [DeepREM: Deep-Learning-Based Radio Environment Map Estimation From Sparse Measurements](https://ieeexplore.ieee.org/ielx7/6287639/10005208/10127968.pdf) — Andrea Cháves-Villota, Carlos A. Viteri-Mera, 2023
- [Radio Map Estimation with Deep Dual Path Autoencoders and Skip Connection Learning](https://doi.org/10.1109/PIMRC56721.2023.10293748) — W. Locke, Nikita Lokhmachev, Yan Huang et al., 2023
- [Spectrum Surveying: Active Radio Map Estimation With Autonomous UAVs](https://arxiv.org/abs/2201.04125) — Raj K. Shrestha, Daniel Romero, Sundeep Chepuri, 2022
- [RME-GAN: A Learning Framework for Radio Map Estimation Based on Conditional Generative Adversarial Network](https://arxiv.org/abs/2212.12817) — Songyang Zhang, Achintha Wijesinghe, Zhi Ding, 2022 ⭐
- [Deep Transfer Learning Based Radio Map Estimation for Indoor Wireless Communications](https://doi.org/10.1109/spawc51304.2022.9833974) — Rahul Kumar Jaiswal, Mohamed Elnourani, Siddharth Deshmukh et al., 2022
- [Constructing Accurate Radio Environment Maps with Kriging Interpolation in Cognitive Radio Networks](https://doi.org/10.1109/CSQRWC.2018.8455448) — Danlei Mao, Wei Shao, Zuping Qian et al., 2018 ⭐
- [Location Estimation-Based Radio Environment Map Construction in Fading Channels](https://doi.org/10.1002/wcm.2367) — Huseyin Birkan Yilmaz, Tuna Tugcu, 2015 ⭐
- [Radio Environment Maps: The Survey of Construction Methods](https://doi.org/10.3837/tiis.2014.11.008) — Marko Pesko, Tomaž Javornik, Andrej Košir et al., 2014 ⭐

### Spectrum Cartography

- [Accelerating Regularized Attention Kernel Regression for Spectrum Cartography](https://doi.org/10.48550/arXiv.tao-laker-2026) — Liping Tao, Chee Wei Tan, 2026
- [Sensing Radio Maps via Bayesian Tensor Learning](https://doi.org/10.1109/ICC52391.2025.11161174) — Zhongtao Chen, Lei Cheng, Yik-Chung Wu, 2025
- [GPRT: A Gaussian Process Regression-Based Radio Map Construction Method for Rugged Terrain](https://doi.org/10.1109/JIOT.2025.3554507) — Guokai Chen, Yongxiang Liu, Jianzhao Zhang et al., 2025
- [Dynamic Spectrum Cartography: Reconstructing Spatial-Spectral-Temporal Radio Frequency Map via Tensor Completion](https://doi.org/10.1109/TSP.2025.3531872) — Xiaonan Chen, Jun Wang, Qingyang Huang, 2025
- [SC-GAN: A Spectrum Cartography with Satellite Internet Based on Pix2Pix Generative Adversarial Network](https://doi.org/10.23919/JCC.fa.2024-0269.202502) — Zhiqiang Pan, Bangning Zhang, Wang Heng et al., 2025
- [Domain-Factored Untrained Deep Prior for Spectrum Cartography](https://doi.org/10.1109/LSP.2025.3599714) — Subash Timilsina, Sagar Shrestha, Lei Cheng et al., 2025
- [Radio Environment Map Reconstruction via Tensor Completion: Bayesian and Semantic Approaches](https://doi.org/10.1109/TVT.2025.3531124) — Xuegang Wang, Fanggang Wang, Boxiang He, 2025
- [Temporal Spectrum Cartography in Low-Altitude Economy Networks: A Generative AI Framework With Multi-Agent Learning](https://doi.org/10.1109/TMC.2025.3647029) — Changyuan Zhao, Ruichen Zhang, Jiacheng Wang et al., 2025
- [Dynamic Spectrum Cartography via Emitter Separation-Based Tensor Completion](https://doi.org/10.1109/ICC51166.2024.10622998) — Xiaonan Chen, Jun Wang, 2024
- [Infinite Limits of Convolutional Neural Network for Urban Electromagnetic Field Exposure Reconstruction](https://doi.org/10.1109/ACCESS.2024.3380835) — Mohammed Mallik, Baptiste Allaert, Esteban Egea-Lopez et al., 2024
- [3D Spectrum Awareness for Radio Dynamic Zones Using Kriging and Matrix Completion](https://doi.org/10.1109/DySPAN60163.2024.10632739) — Mushfiqur Rahman, Seungmo Maeng, Ismail Guvenc et al., 2024
- [Tensor-Based Parametric Spectrum Cartography From Irregular Off-Grid Samplings](https://doi.org/10.1109/LSP.2023.3257723) — Xiaonan Chen, Jun Wang, Guoyong Zhang et al., 2023
- [TRASC: Tensor-Based Radio Spectrum Cartography Using Plate Splines and Tensor CP Decomposition](https://doi.org/10.1109/FNWF58287.2023.10520367) — Mohsen Joneidi, Nazanin Rahnavard, Faramarz Hejazi, 2023
- [Kriging-Based 3-D Spectrum Awareness for Radio Dynamic Zones Using Aerial Spectrum Sensors](https://arxiv.org/abs/2307.06310) — Seungmo Maeng, Ozgur Ozdemir, Ismail Guvenc et al., 2023
- [Quantized Radio Map Estimation Using Tensor and Deep Generative Models](https://arxiv.org/abs/2303.01770) — Subash Timilsina, Sagar Shrestha, Xiao Fu, 2023
- [Radio Map Estimation: A data-driven approach to spectrum cartography](https://arxiv.org/abs/2202.03269) — Daniel Romero, Seung-Jun Kim, 2022 ⭐
- [Deep Generative Model Learning for Blind Spectrum Cartography with NMF-Based Radio Map Disaggregation](https://doi.org/10.1109/ICASSP39728.2021.9413382) — Subash Shrestha, Xiao Fu, Min-Fong Hong, 2021
- [Deep Spectrum Cartography: Completing Radio Map Tensors Using Learned Neural Models](https://doi.org/10.1109/tsp.2022.3145190) — Subash Shrestha, Xiao Fu, Min-Fong Hong, 2021 ⭐
- [Spectrum Cartography via Coupled Block-Term Tensor Decomposition](https://doi.org/10.1109/tsp.2020.2993530) — Guoyong Zhang, Xiao Fu, Jun Wang et al., 2019 ⭐
- [Data-Driven Spectrum Cartography via Deep Completion Autoencoders](http://arxiv.org/pdf/1911.12810) — Yves Teganya, Daniel Romero, 2019 ⭐
- [Location-Free Spectrum Cartography](https://arxiv.org/abs/1812.11539) — Yves Teganya, Daniel Romero, Luis Miguel Lopez Ramos et al., 2018
- [Spectrally Efficient Data-Adaptive Spectrum Cartography](https://doi.org/10.1109/TSP.2017.2659650) — Daniel Romero, Seung-Jun Kim, Georgios B. Giannakis et al., 2017 ⭐
- [Spectrum Cartography Using Quantized Observations](https://doi.org/10.1109/ICASSP.2015.7178572) — Daniel Romero, Seung-Jun Kim, Roberto Lopez-Valcarce et al., 2015
- [Stochastic Semiparametric Regression for Spectrum Cartography](https://doi.org/10.1109/CAMSAP.2015.7383849) — Daniel Romero, Seung-Jun Kim, Georgios B. Giannakis, 2015
- [Wireless Sensor Network for Spectrum Cartography Based on Kriging Interpolation](https://doi.org/10.1109/PIMRC.2012.6362597) — Gabriele Boccolini, Gustavo Hernandez-Penaloza, Baltasar Beferull-Lozano, 2012
- [Distributed Spectrum Sensing for Cognitive Radio Networks by Exploiting Sparsity](https://doi.org/10.1109/TSP.2009.2038417) — Juan Andres Bazerque, Georgios B. Giannakis, 2010 ⭐
- [Group-Lasso on Splines for Spectrum Cartography](http://arxiv.org/pdf/1010.0274) — Juan Andres Bazerque, Gonzalo Mateos, Georgios B. Giannakis, 2010 ⭐
- [Informed Spectrum Usage in Cognitive Radio Networks: Interference Cartography](https://doi.org/10.1109/PIMRC.2008.4699911) — Afef Ben Hadj Alaya-Feki, Sana Ben Jemaa, Berna Sayrac et al., 2008 ⭐

### Pathloss Prediction

- [Effective Outdoor Pathloss Prediction: A Multi-Layer Segmentation Approach With Weighting Map](https://doi.org/10.1109/tvt.2026.3658966) — Yuan Gao, Tao Wen, Wenjing Xie et al., 2026
- [IPP-Net: A Generalizable Deep Neural Network Model for Indoor Pathloss Radio Map Prediction](https://doi.org/10.1109/ICASSP49660.2025.10890663) — Bin Feng, Meng Zheng, Wei Liang et al., 2025
- [The First Indoor Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/ICASSP49660.2025.10889381) — Stefanos Bakirtzis, Çagkan Yapar, Kehai Qiu et al., 2025
- [Sparse-Guided RadioUNet with Adaptive Sampling for the MLSP 2025 Sampling-Assisted Pathloss Radio Map Prediction Data Competition](https://doi.org/10.1109/MLSP62443.2025.11204292) — Ryoichi Kojima, Satoshi Ito, Tatsuya Nagao et al., 2025
- [RMTransformer: Accurate Radio Map Construction and Coverage Prediction](https://doi.org/10.1109/VTC2025-Spring65109.2025.11174709) — Yuxuan Li, Cheng Zhang, Wen Wang et al., 2025
- [Enhancing Pathloss Estimation with Vision Transformers and Direct Wave Power Integration](https://doi.org/10.23919/eusipco63237.2025.11226433) — Yuuki Tachioka, 2025
- [The Sampling-Assisted Pathloss Radio Map Prediction Competition](https://doi.org/10.1109/MLSP62443.2025.11204278) — Çagkan Yapar, Stefanos Bakirtzis, Andra Lutu et al., 2025
- [Geometrical Features Based-mmWave UAV Path Loss Prediction Using Machine Learning for 5G and Beyond](https://doi.org/10.1109/OJCOMS.2024.3450089) — Sajjad Hussain, Syed F. N. Bacha, A. Cheema et al., 2024
- [Overview of the First Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/OJSP.2024.3419563) — Çagkan Yapar, Fabian Jaensch, Ron Levie et al., 2024
- [RadioDiff: An Effective Generative Diffusion Model for Sampling-Free Dynamic Radio Map Construction](https://github.com/UNIC-Lab/RadioDiff) — Xiucheng Wang, Keda Tao, Nan Cheng et al., 2024 ⭐
- [Vision Transformers for Efficient Indoor Pathloss Radio Map Prediction](https://doi.org/10.3390/electronics14101905) — Edvard Ghukasyan, Hrant Khachatrian, Rafayel Mkrtchyan et al., 2024
- [Distributed Split Learning for Map-Based Signal Strength Prediction Empowered by Deep Vision Transformer](https://doi.org/10.1109/TVT.2023.3320643) — Haiyao Yu, Changyang She, Chentao Yue et al., 2024
- [Transformer-Based Neural Surrogate for Link-Level Path Loss Prediction from Variable-Sized Maps](https://arxiv.org/abs/2310.04570) — Thomas M. Hehn, Tribhuvanesh Orekondy, O. Shental et al., 2023
- [The First Pathloss Radio Map Prediction Challenge](https://arxiv.org/abs/2310.07658) — Çagkan Yapar, Fabian Jaensch, Ron Levie et al., 2023
- [Agile Radio Map Prediction Using Deep Learning](https://doi.org/10.1109/icassp49357.2023.10096546) — Enes Krijestorac, Hazem Sallouha, Shamik Sarkar et al., 2023
- [PMNet: Large-Scale Channel Prediction System for ICASSP 2023 First Pathloss Radio Map Prediction Challenge](https://doi.org/10.1109/ICASSP49357.2023.10095257) — Ju-Hyung Lee, Joohan Lee, Seong-Bae Lee et al., 2023
- [A Deep Learning-Based Indoor Radio Estimation Method Driven by 2.4 GHz Ray-Tracing Data](https://ieeexplore.ieee.org/ielx7/6287639/6514899/10347228.pdf) — Changwoo Pyo, Hirokazu Sawada, Takeshi Matsumura, 2023
- [Deep Learning-Based Path Loss Prediction for Outdoor Wireless Communication Systems](https://doi.org/10.1109/icassp49357.2023.10095501) — Kehai Qiu, Stefanos Bakirtzis, Hui Song et al., 2023
- [REM-U-Net: Deep Learning Based Agile REM Prediction With Energy-Efficient Cell-Free Use Case](https://ieeexplore.ieee.org/ielx7/8782710/9006934/10474197.pdf) — Hazem Sallouha, Shamik Sarkar, Enes Krijestorac et al., 2023
- [PMNet: Robust Pathloss Map Prediction via Supervised Learning](https://arxiv.org/abs/2211.10527) — Ju-Hyung Lee, Omer Gokalp Serbetci, Dhruv Selvam et al., 2022 ⭐
- [Pseudo Ray-Tracing: Deep Learning Assisted Outdoor mm-Wave Path Loss Prediction](https://doi.org/10.1109/lwc.2022.3175091) — Kehai Qiu, Stefanos Bakirtzis, Hui Song et al., 2022
- [LocUNet: Fast Urban Positioning Using Radio Maps and Deep Learning](https://doi.org/10.1109/icassp43922.2022.9747240) — Çagkan Yapar, R. Levie, Gitta Kutyniok et al., 2022
- [Predictive Modeling of Millimeter-Wave Vegetation-Scattering Effect Using Hybrid Physics-Based and Data-Driven Approach](https://doi.org/10.1109/TAP.2021.3118463) — Peize Zhang, Cheng Yi, Bensheng Yang et al., 2022
- [DRaGon: Mining Latent Radio Channel Information from Geographical Data Leveraging Deep Learning](https://arxiv.org/abs/2112.07941) — Benjamin Sliwa, Melina Geis, Caner Bektas et al., 2021
- [Real-Time Outdoor Localization Using Radio Maps: A Deep Learning Approach](https://arxiv.org/abs/2106.12556) — Çagkan Yapar, R. Levie, Gitta Kutyniok et al., 2021 ⭐
- [Pathloss Prediction using Deep Learning with Applications to Cellular Optimization and Efficient D2D Link Scheduling](https://doi.org/10.1109/ICASSP40776.2020.9053347) — Ron Levie, Çagkan Yapar, Gitta Kutyniok et al., 2020
- [RadioUNet: Fast Radio Map Estimation With Convolutional Neural Networks](https://arxiv.org/abs/1911.09002) — Ron Levie, Çağkan Yapar, Gitta Kutyniok et al., 2019 ⭐
- [Propagation Measurements and Models for Wireless Communications Channels](https://doi.org/10.1109/35.468198) — Theodore S. Rappaport, 1996 ⭐

### Channel Knowledge Maps (CKM)

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
- [A Deep Learning Framework for Wireless Radiation Field Reconstruction and Channel Prediction](https://arxiv.org/abs/2403.03241) — Haofan Lu, Christopher Vattheuer, Baharan Mirzasoleiman et al., 2024
- [Channel Knowledge Map Construction Based on a UAV-Assisted Channel Measurement System](https://doi.org/10.3390/drones8050191) — Yanheng Qiu, Xiaomin Chen, Kai Mao et al., 2024
- [Deep Learning-Based CKM Construction with Image Super-Resolution](https://doi.org/10.1109/VTC2025-Spring65109.2025.11174933) — Shiyu Wang, Xiaoli Xu, Yong Zeng, 2024
- [Environment-Aware Channel Estimation via Integrating Channel Knowledge Map and Dynamic Sensing Information](https://doi.org/10.1109/LWC.2024.3482357) — Di Wu, Yuelong Qiu, Yong Zeng et al., 2024
- [CKMImageNet: A Comprehensive Dataset to Enable Channel Knowledge Map Construction via Computer Vision](https://doi.org/10.1109/ICCCWorkshops62562.2024.10693754) — Di Wu, Zijian Wu, Yuelong Qiu et al., 2024
- [Aerial Video Streaming Over 3D Cellular Networks: An Environment and Channel Knowledge Map Approach](https://doi.org/10.1109/TWC.2023.3289501) — Cheng Zhan, Han Hu, Zhi Liu et al., 2024
- [RF-3DGS: Wireless Channel Modeling With Radio Radiance Field and 3D Gaussian Splatting](https://github.com/SunLab-UGA/RF-3DGS) — Lihao Zhang, Haijian Sun, S. Berweger et al., 2024
- [Strategic Application of AIGC for UAV Trajectory Design: A Channel Knowledge Map Approach](https://arxiv.org/abs/2412.00386) — Chiya Zhang, Ting Wang, Rubing Han et al., 2024
- [Prototyping and Experimental Results for ISAC-Based Channel Knowledge Map](https://doi.org/10.1109/TVT.2025.3545785) — Chaoyue Zhang, Zhiwen Zhou, Xiaoli Xu et al., 2024
- [Environment-Aware Joint Active/Passive Beamforming for RIS-Aided Communications Leveraging Channel Knowledge Map](https://ieeexplore.ieee.org/ielx7/4234/5534602/10108969.pdf) — E. Taghavi, Ramin Hashemi, N. Rajatheva et al., 2023
- [Environment-Aware Coordinated Multi-Point mmWave Beam Alignment Via Channel Knowledge Map](https://doi.org/10.1109/ICCWorkshops57953.2023.10283607) — Di Wu, Yong Zeng, 2023
- [A Tutorial on Environment-Aware Communications via Channel Knowledge Map for 6G](https://arxiv.org/abs/2309.07460) — Yong Zeng, Junting Chen, Jie Xu et al., 2023 ⭐
- [Channel Knowledge Map (CKM)-Assisted Multi-UAV Wireless Network: CKM Construction and UAV Placement](https://arxiv.org/abs/2207.01931) — Haoyun Li, Peiming Li, Jie Xu et al., 2022
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
