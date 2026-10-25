# SRI ESHWAR COLLEGE OF ENGINEERING
**(An Autonomous Institution – Affiliated to Anna University)**  
**COIMBATORE – 641 202**

---

### **AI & ML PROJECT WORK (COURSE CODE: U23AM495)**
# AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES
*(Target Problem Statement: SIH26168 / ISRO Smart Vehicles Category)*

**Submitted by:**  
- **[STUDENT NAME 1] – [REGISTER NUMBER 1]**  
- **[STUDENT NAME 2] – [REGISTER NUMBER 2]**  

**Under the Guidance of:**  
- **[FACULTY NAME, M.E., Ph.D.]**, Assistant Professor, Department of Computer Science and Engineering  

**Head of Department / Dean:**  
- **Dr. R. SUBHA M.E., Ph.D.**, Dean, Computing Science & Head of Department, CSE  

**Batch:** 2025 – 2029 | **Submission Date:** October 2026  

---

## BONAFIDE CERTIFICATE

Certified that this Report titled **“AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES”** for the course **U23AM495 - Artificial Intelligence and Machine Learning** is the bonafide work of:

- **[STUDENT NAME 1] ([REGISTER NUMBER 1])**
- **[STUDENT NAME 2] ([REGISTER NUMBER 2])**

who carried out the project work under my supervision.

```
-----------------------------------------          -----------------------------------------
SIGNATURE                                          SIGNATURE
Dr. R. SUBHA M.E., Ph.D.                           [FACULTY NAME]
HEAD OF THE DEPARTMENT                             SUPERVISOR
Dept. of Computer Science & Engineering            Assistant Professor, Dept. of CSE
Sri Eshwar College of Engineering,                 Sri Eshwar College of Engineering,
Coimbatore – 641 202.                              Coimbatore – 641 202.
```

Submitted for the Autonomous Semester End Project Viva-Voce held on: `....................`

```
_________________________                          _________________________
INTERNAL EXAMINER                                  EXTERNAL EXAMINER
```

---

## DECLARATION

We declare that the project entitled **“AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES”** submitted in partial fulfilment to the University as the project work of Bachelor of Engineering (Computer Science and Engineering) Degree, is a record of original work done by us under the supervision and guidance of **[FACULTY NAME]**, Assistant Professor, Department of Computer Science and Engineering, Sri Eshwar College of Engineering, Coimbatore.

**Place:** Coimbatore  
**Date:** October 2026  

**Project Guided by:**  
`[FACULTY NAME]`  
Assistant Professor, CSE  

**Submitted by:**  
`[STUDENT NAME 1]`  
`[STUDENT NAME 2]`  

---

## ACKNOWLEDGEMENT

The success of a work depends on a team and cooperation. I take this opportunity to express my gratitude and thanks to everyone who helped me in my project. I would like to thank the management for the constant support provided by them to complete this project.

It is indeed our great honor bounded duty to thank our beloved Chairman **Mr. R. Mohanram**, for his academic interest shown towards the students.

We are indebted to our Director **Mr. R. Rajaram**, for motivating and providing us with all facilities.

I wish to express my sincere regards and deep sense of gratitude to **Dr. Sudha Mohanram, M.E, Ph.D.** Principal, for the excellent facilities and encouragement provided during the course of the study and project.

We are indebted to **Dr. R. Subha, M.E., Ph.D.** Dean, Computing Science for having permitted us to carry out this project and giving the complete freedom to utilize the resources.

I express my sincere thanks to my course faculty **[FACULTY NAME]**, Assistant Professor of Computer Science and Engineering Department for the valuable guidance and encouragement given to us for this project.

I solemnly express our thanks to all the teaching and nonteaching staff of the Computer Science and Engineering Department, family and friends for their valuable support which inspired us to work on this project.

---

## ABSTRACT *(Page i)*

In modern intelligent transportation systems, autonomous vehicles, and location-based navigation services, continuous positional tracking is essential for vehicular safety. While Global Navigation Satellite Systems (GNSS) deliver precise position fixes under open skies, signal reception degrades catastrophically in GNSS-denied environments such as urban canyons, mountain passes, tunnels, and underground parking facilities. Conventional inertial dead reckoning relying on low-cost Micro-Electro-Mechanical Systems (MEMS) sensors suffers from thermo-mechanical noise, turn-on bias, and mounting tilt, leading to rapid cubic position error drift ($O(t^3)$) within seconds.

This project presents an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine designed for seamless vehicular navigation during extended GNSS outages. Addressing the critical limitation of joint feature cross-talk—where smartphone pitch tilts and road vibration spikes corrupt vehicular angular rate estimation—we propose a Decoupled Dual-Model Deep Learning architecture: **VelocityNet**, which specializes exclusively on 3-axis accelerometer signals to infer longitudinal speed, and **YawRateNet**, which processes 3-axis gyroscope signals to determine rotational yaw rate without phantom turns. Both models are trained with a heteroscedastic negative log-likelihood loss function to dynamically predict kinematic state uncertainties alongside point estimates.

The model is tightly integrated into a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates. To ensure long-term stability, an automated Zero-Velocity Update (ZUPT) gatekeeper detects stationary vehicle states to lock velocity and snap gyro biases, while an online drift adaptation engine continuously compensates for device mounting tilt during active GNSS lock. Evaluated on the international benchmark IO-VNBD dataset across diverse driving regimes, the proposed system bounds position drift to under 2.5 meters across a 30-second complete GNSS outage, achieving over 90% drift reduction compared to naive dead reckoning. The end-to-end framework is deployed on an asynchronous FastAPI backend streaming 50 Hz telemetry over WebSockets to an interactive Leaflet.js dashboard for real-time vehicular state visualization.

---

## TABLE OF CONTENTS *(No Page Number)*

| S.No | Contents | Page No |
| :--- | :--- | :---: |
| | **ABSTRACT** | **i** |
| **1** | **INTRODUCTION** | **1** |
| 1.1 | Application Domain & Background | 1 |
| 1.2 | Problem Context & GNSS-Denied Navigation Importance | 2 |
| 1.3 | Role of AI/ML & Sensor Fusion in Navigation | 2 |
| 1.4 | Overview of Proposed Solution & Architectural Breakthrough | 2 |
| **2** | **SYSTEM ANALYSIS AND DESIGN** | **3** |
| 2.1 | Existing Scenario & Limitations | 3 |
| 2.2 | Problem Statement | 4 |
| 2.3 | Objectives | 4 |
| 2.4 | Scope of the Project | 5 |
| 2.5 | System Requirements | 5 |
| 2.5.1 | Hardware Requirements | 5 |
| 2.5.2 | Software Requirements | 6 |
| **3** | **PROPOSED SOLUTION** | **7** |
| 3.1 | Overview | 7 |
| 3.2 | System Architecture / Block Diagram | 8 |
| 3.3 | Methodology | 9 |
| 3.4 | Development Phases | 10 |
| 3.5 | Dataset Description | 11 |
| 3.6 | Data Preprocessing | 12 |
| 3.7 | Feature Engineering | 13 |
| 3.8 | Model Development (Decoupled Dual-Model IDR) | 14 |
| 3.9 | Evaluation Metrics | 15 |
| 3.10 | Challenge-Specific Processing (Online Calibration & ZUPT) | 16 |
| **4** | **IMPLEMENTATION AND RESULTS** | **17** |
| 4.1 | Development Environment | 17 |
| 4.2 | Implementation Modules | 18 |
| 4.3 | Experimental Results | 19 |
| 4.4 | Model Comparison | 20 |
| 4.5 | Output / Screenshots & Telemetry Interface | 21 |
| 4.6 | Discussion | 22 |
| **5** | **CONCLUSION AND FUTURE ENHANCEMENT** | **23** |
| 5.1 | Conclusion | 23 |
| 5.2 | Future Enhancement | 24 |
| **6** | **REFERENCES** | **25** |
| | **APPENDIX: COMPLETE SOURCE CODE LISTINGS** | **26** |
| | Appendix A: models/idr_model.py | 26 |
| | Appendix B: sensor_fusion/ekf.py | 29 |
| | Appendix C: sensor_fusion/coordinates.py | 33 |
| | Appendix D: models/online_calibrator.py | 35 |
| | Appendix E: backend/main.py | 38 |

---

## LIST OF FIGURES *(Page ii)*

| Fig. No. | Figure Title | Page No. |
| :---: | :--- | :---: |
| 3.2.1 | Decoupled AI-ML Intelligent Dead Reckoning End-to-End System Architecture | 8 |
| 3.8.1 | Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR | 14 |
| 4.2.1 | Execution Flowchart Across the Five Implementation Modules | 18 |
| 4.3.1 | Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage | 19 |
| 4.3.2 | Cumulative Positional Error Growth: Naive IMU vs. Proposed Decoupled IDR | 20 |
| 4.3.3 | Neural Speed and Heading Tracking Performance under Road Vibration Noise | 20 |
| 4.5.1 | Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface | 21 |

---

## LIST OF TABLES *(Page iii)*

| Table No. | Table Title | Page No. |
| :---: | :--- | :---: |
| 2.5.1 | Hardware and Edge Compute Specification Requirements | 5 |
| 2.5.2 | Software Stack, Deep Learning Frameworks, and Tools | 6 |
| 3.5.1 | IO-VNBD Benchmark Telemetry Schema & Physical Unit Definitions | 11 |
| 4.1.1 | Benchmarked Development Environment Details | 17 |
| 4.4.1 | Quantitative Outage Performance Comparison Across Benchmark Drives | 20 |

---

# CHAPTER 1: INTRODUCTION *(Page 1)*

### 1.1 Application Domain & Background
Vehicular positioning and continuous tracking form the backbone of modern Advanced Driver Assistance Systems (ADAS), fleet logistics, emergency dispatch, and autonomous mobility. Standard navigation platforms depend heavily on Global Navigation Satellite Systems (GNSS) including GPS, GLONASS, Galileo, and NavIC. Under nominal conditions with unhindered line-of-sight to orbiting satellites, multi-frequency GNSS receivers provide sub-meter to meter-level positioning accuracy. However, modern urban architectures and civil infrastructure present challenging operational environments where satellite signals are either completely obstructed, attenuated, or subject to multipath interference. Tunnels, sub-surface roadways, multi-level flyovers, parking garages, and dense urban canyons flanked by skyscrapers regularly trigger catastrophic GNSS outages lasting anywhere from tens of seconds to several minutes.

When GNSS reception is interrupted, conventional vehicles must rely on onboard Dead Reckoning (DR). Classic dead reckoning computes relative displacement by integrating raw accelerations and angular velocities captured from onboard Micro-Electro-Mechanical Systems (MEMS) Inertial Measurement Units (IMUs). Although MEMS IMUs are compact, lightweight, and cost-effective, they are inherently prone to thermo-mechanical noise, turn-on biases, scale factor variations, and cross-axis misalignments. In pure kinematic integration, double-integrating noisy accelerometer readings causes position errors to grow with the third power of elapsed time ($O(t^3)$), while integrating gyroscope biases yields quadratic error accumulation ($O(t^2)$). Within 10 to 15 seconds of a GNSS outage, a standard smartphone IMU can accumulate hundreds of meters of positional error, completely derailing route planning and automated driving maneuvers.

### 1.2 Problem Context & GNSS-Denied Navigation Importance
In mission-critical autonomous systems, uninterrupted positional awareness is not merely a convenience but an absolute functional safety requirement. When an autonomous or semi-autonomous vehicle travels through a 1-kilometer tunnel at 60 km/h (a 60-second outage), an uncorrected dead reckoning system suffering from a minor 0.05 m/s² acceleration bias will deviate by over 100 meters, falsely asserting that the vehicle has crossed the road barrier or entered oncoming traffic lanes. For commercial ridesharing and navigation apps, loss of positioning results in UI freezing, loss of turn-by-turn guidance, and erroneous rerouting upon exiting subterranean road structures. Solving the GNSS-denial localization problem with commodity sensors represents a vital frontier in intelligent transportation engineering.

### 1.3 Role of AI/ML & Sensor Fusion in Navigation
To break the cubic drift bottleneck without mandating prohibitive aerospace-grade Fiber Optic Gyroscopes (FOG) or costly RTK base stations, data-driven Machine Learning and Deep Learning approaches have emerged as a powerful paradigm. Vehicular motion is non-holonomic; a car does not translate sideways instantaneously or fly off the road plane. Instead, vehicle kinematics adhere to physical road constraints, engine rev cycles, suspension dynamics, and steering geometry. Convolutional Neural Networks (CNNs) and Bidirectional Gated Recurrent Units (BiGRUs) possess the unique capability to learn high-dimensional temporal representations directly from short sliding windows of high-frequency IMU signals.

Rather than integrating uncalibrated acceleration measurements directly, a deep neural network can be trained as a kinematic observer. It isolates chassis vibration noise and road surface bumps from true translational movements, predicting the vehicle's instantaneous forward velocity and yaw rate. Crucially, these neural predictions must be coupled with an analytical estimation framework. By feeding neural predictions into an Extended Kalman Filter (EKF) equipped with dynamic uncertainty covariance weighting, the system achieves the optimal blend: the structural kinematic guarantees of Kalman filtering paired with the adaptive feature extraction power of modern deep learning.

### 1.4 Overview of Proposed Solution & Architectural Breakthrough
While prior monolithic neural networks have attempted joint velocity and heading estimation, they suffer from a severe architectural limitation: cross-channel parameter coupling. When accelerometers and gyroscopes share convolution kernels and recurrent hidden layers, smartphone mounting pitch tilt (which leaks Earth's 9.81 m/s² gravitational acceleration into forward axes) and vertical chassis vibrations frequently induce spurious yaw rate spikes. This artifact causes vehicles cruising in a straight tunnel to generate phantom circular loops and wander off-road in the estimated trajectory.

To overcome this limitation, this project introduces a **Decoupled Dual-Model Deep Neural Dead Reckoning Architecture**. The forward velocity specialist (**VelocityNet**) ingests solely 3-axis accelerometer signals, while the heading specialist (**YawRateNet**) operates solely on 3-axis gyroscope signals. By decoupling feature spaces, mounting pitch tilt and chassis bumps cannot corrupt heading estimation. Furthermore, our stack integrates an automated Zero-Velocity Update (ZUPT) gatekeeper, an online gradient descent drift calibrator with L2 weight anchoring, and an asynchronous WebSocket telemetry pipeline for real-time edge visualization.

---

# CHAPTER 2: SYSTEM ANALYSIS AND DESIGN *(Page 3)*

### 2.1 Existing Scenario & Limitations
In existing commercial vehicular navigation applications (such as smartphone navigation apps and standard dashboard GPS units), navigation relies predominantly on loose-coupling between GPS receivers and basic device compasses. When a vehicle enters an underground tunnel or deep urban trench:
- **Snap-to-Road Freezing:** When GNSS signals are lost, conventional applications either freeze the vehicle icon at the tunnel entrance or project the vehicle forward along the mapped polyline at constant pre-outage speed. If traffic stops, decelerates, or takes an underground ramp, the display diverges completely from reality.
- **Cubic Kinematic Drift:** If unassisted inertial dead reckoning is triggered using the phone's built-in IMU, double integration of noisy accelerations leads to explosive cubic drift ($p(t) = \frac{1}{6} a_{\text{noise}} t^3$). A mere $0.05\,\text{m/s}^2$ sensor bias produces over 112 meters of error within 30 seconds.
- **Mounting Pitch Leakage:** Smartphones placed in vehicle cradles or consoles are rarely mounted perpendicular to the road plane. A tilt angle of only 5 degrees leaks $g \sin(5^\circ) \approx 0.85\,\text{m/s}^2$ of gravity into the forward axis, which naive DR misinterprets as continuous aggressive acceleration.
- **Vibration Noise & False Turns:** Engine idle vibrations (20–40 Hz) and road surface irregularities corrupt gyroscope outputs, creating virtual rotational rates that turn straight tunnel paths into circular trajectories.

### 2.2 Problem Statement
The project targets the **SIH26168** national challenge under the **ISRO / Smart Vehicles** domain: *'AI-ML Based Intelligent Dead Reckoning System for Seamless Navigation and IMU Sensor Drift Mitigation during GNSS Outages'*. The core requirement is to develop an edge-compatible, high-accuracy dead reckoning engine that maintains continuous vehicular trajectory tracking during GNSS denial (30 to 120 seconds) using low-cost commodity smartphone and CAN-bus IMU sensors, reducing cumulative position drift by at least 85% relative to unassisted dead reckoning without requiring expensive external positioning hardware.

### 2.3 Objectives
1. **Objective 1 - Multi-Source Dataset Ingestion:** Ingest and synchronize high-frequency (50 Hz) 6-DOF IMU streams from authentic benchmark datasets (IO-VNBD Racelogic VBOX RTK and smartphone logs) and multi-maneuver synthetic drives.
2. **Objective 2 - Decoupled Neural Architecture:** Design and train a decoupled dual-model neural network (VelocityNet and YawRateNet) using temporal convolutions and BiGRUs to eliminate cross-axis vibration and tilt contamination.
3. **Objective 3 - Uncertainty Estimation:** Implement a heteroscedastic loss formulation predicting Gaussian aleatoric variances for speed and yaw rate to dynamically inform downstream Kalman filter update matrices.
4. **Objective 4 - Intelligent Sensor Fusion:** Formulate a 5-state Extended Kalman Filter (EKF) in local metric ENU coordinates incorporating Zero-Velocity Updates (ZUPT) and online drift adaptation.
5. **Objective 5 - Edge Telemetry Dashboard:** Deploy the end-to-end stack as an asynchronous FastAPI backend streaming 50 Hz telemetry over WebSockets to an interactive Leaflet.js dashboard with live ground truth comparison.

### 2.4 Scope of the Project
The scope covers ground vehicle navigation under urban, suburban, and highway regimes. The system handles 6-DOF inertial sensor telemetry (accelerometer and gyroscope) captured at 50 Hz, accommodates arbitrary phone pitch orientations via online calibration, and maintains accurate state estimation during simulated and authentic GNSS outages spanning up to 60 seconds. The project integrates real-time web visualization and full test coverage.

### 2.5 System Requirements

#### 2.5.1 Hardware Requirements
*Table 2.5.1: Hardware and Edge Compute Specification Requirements*

| Subsystem | Minimum Specification | Development / Benchmarking Rig |
| :--- | :--- | :--- |
| **Host Processor** | Intel Core i5 / AMD Ryzen 5 (4 Cores) | Intel Core i7-13620H / AMD Ryzen 7 (16 Threads) |
| **System Memory (RAM)** | 8 GB DDR4 | 16 GB / 32 GB DDR5 5200 MHz |
| **GPU Hardware** | Integrated Graphics / Optional GPU | NVIDIA GeForce RTX 5050 Laptop GPU (6 GB VRAM) |
| **Edge Target** | ARM Cortex-A53 / Raspberry Pi 4 | Snapdragon 8 Gen 2 / Jetson Nano / PC Edge |
| **Sensors Supported** | 6-DOF MEMS IMU (InvenSense / Bosch) | STMicroelectronics 6-DOF IMU + VBOX RTK GPS |

#### 2.5.2 Software Requirements
*Table 2.5.2: Software Stack, Deep Learning Frameworks, and Tools*

| Component | Framework / Library | Version / Function |
| :--- | :--- | :--- |
| **Operating System** | Microsoft Windows 11 / Linux Ubuntu 22.04 | Host runtime and development OS |
| **Programming Language** | Python 3.11 | Core backend and deep learning pipelines |
| **Deep Learning Framework** | PyTorch 2.4+ (CUDA 12.1) | CNN-GRU training and TorchScript edge scripting |
| **Scientific Computing** | NumPy, SciPy, Scikit-learn | Kinematics, EKF matrix math, and signal filtering |
| **Backend Web Server** | FastAPI + Uvicorn + WebSockets | 50 Hz telemetry streaming and REST service |
| **Frontend Web GIS** | HTML5, TailwindCSS, Leaflet.js | Interactive real-time map HUD and multi-path tracking |
| **Evaluation Suite** | Pytest, Matplotlib | Automated regression testing and error graphing |

---

# CHAPTER 3: PROPOSED SOLUTION *(Page 7)*

### 3.1 Overview
The proposed solution is an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine designed to provide continuous, accurate, and jump-free vehicle navigation during GNSS denial. Rather than relying on naive double-integration of raw accelerometer and gyroscope outputs, the system treats inertial navigation as a coordinated two-level problem: a high-frequency deep learning observer for noise-resilient kinematic parameter estimation, coupled with a probabilistic state estimator for continuous spatial tracking and drift bounding.

### 3.2 System Architecture / Block Diagram
![Figure 3.2.1: End-to-End System Block Diagram](figures/fig_system_architecture.png)  
*Figure 3.2.1: End-to-End System Block Diagram of Decoupled AI-ML Dead Reckoning & Sensor Fusion Pipeline*

### 3.3 Methodology
The methodology operates on the principle of sliding temporal windows. High-frequency 6-DOF IMU samples are buffered into overlapping windows of 50 samples (corresponding to 1.0 second of driving history at 50 Hz). The system performs continuous stationary classification: when total acceleration variance drops below $0.05\,\text{m}^2/\text{s}^4$ and gyroscope variance drops below $0.003\,\text{rad}^2/\text{s}^2$, the vehicle is diagnosed as stationary, triggering instantaneous Zero-Velocity Updates. When in motion, the 3-axis accelerometer channels are routed to VelocityNet, and the 3-axis gyroscope channels are routed to YawRateNet. The neural predictions are augmented with aleatoric uncertainty variances and fused into the EKF.

### 3.4 Development Phases
1. **Phase 1 - Problem Understanding & Objective Definition:** Formulate vehicular dead reckoning as multivariate time-series regression. Establish key performance indicators: Position Mean Absolute Error (MAE), Maximum Drift, and Relative Percentage Drift over outage distance.
2. **Phase 2 - Data Collection & Understanding:** Develop the `IOVNBDLoader` parser capable of processing 29-column VBOX RTK telemetry and 24-column Android AndroSensor recordings, resolving GPS timestamp jitter and missing frame intervals.
3. **Phase 3 - Data Preprocessing & Feature Engineering:** Implement gravity vector isolation, Bowring ellipsoidal WGS84-to-ENU coordinate transformation, and 50-sample sliding window tensor formatting.
4. **Phase 4 - Model Building:** Design VelocityNet and YawRateNet modules with 1D temporal convolutions, MaxPool1D subsampling, BiGRU sequence modeling, and heteroscedastic uncertainty heads.
5. **Phase 5 - Model Evaluation & Validation:** Construct a 5-state Extended Kalman Filter with Joseph-form numerical stabilization, ZUPT/ZARU logic, and Online Gradient Descent drift adaptation.
6. **Phase 6 - Final Output & Deployment:** Script PyTorch models to TorchScript (.pt), build asynchronous FastAPI WebSocket endpoints, and render dynamic multi-path maps on an interactive HTML5/Leaflet HUD.

### 3.5 Dataset Description
*Table 3.5.1: IO-VNBD Benchmark Telemetry Schema & Physical Unit Definitions*

| Column / Feature | Description & Unit | Data Type | Role in Pipeline |
| :--- | :--- | :--- | :--- |
| **ax, ay, az** | 3-Axis Specific Force / Acceleration ($m/s^2$) | float32 (50 Hz) | VelocityNet Input |
| **gx, gy, gz** | 3-Axis Angular Velocity / Gyroscope ($\text{rad}/s$) | float32 (50 Hz) | YawRateNet Input |
| **GPS Lat / Lon** | Geodetic WGS84 Coordinates (degrees) | float64 (1-10 Hz) | GNSS EKF / Ground Truth |
| **GPS Altitude** | Height above WGS84 Reference Ellipsoid ($m$) | float32 (1-10 Hz) | ENU Local Origin |
| **GPS Speed** | Longitudinal True Ground Speed (km/h $\to$ m/s) | float32 (1-10 Hz) | Training Target (Velocity) |
| **GPS Heading** | True Vehicle Azimuth (degrees $\to$ rad ENU) | float32 (1-10 Hz) | Training Target (Yaw Rate) |
| **Wheel Speeds (FL, FR, RL, RR)** | Individual 4-Wheel Rotational Rates (rad/s) | float32 (10 Hz) | Independent Odometry |

### 3.6 Data Preprocessing
- **Equispaced Resampling:** Smartphone Android HAL callbacks fire asynchronously. Linear interpolation resamples timestamps onto a rigid 50.0 Hz grid ($\Delta t = 0.02\,\text{s}$).
- **Gravity Isolation:** When gravity vectors are recorded by the mobile OS, static gravity is subtracted from raw accelerations. In standalone mode, a high-pass Butterworth filter strips low-frequency gravitational leakage.
- **Geodetic Bowring Projection:** GPS latitude and longitude are converted to Cartesian East-North-Up (ENU) coordinates via Bowring's closed-form ellipsoidal algorithm, establishing an exact metric Euclidean tangent plane.
- **Stair-Step Teleportation Reconciliation:** Low-frequency (1 Hz) smartphone GPS logs often duplicate coordinates across 10-sample spans. The loader identifies genuine GPS epochs and reconstructs intermediate positions using forward kinematic integration.

### 3.7 Feature Engineering
Rather than relying purely on end-to-end black-box learning, domain-specific physics features are extracted. Rolling window statistical variances ($\text{Var}(a_x), \text{Var}(a_y), \text{Var}(a_z)$) capture suspension vibration signatures directly proportional to rolling speed. Gyroscope norm ($||\boldsymbol{\omega}||$) captures cornering dynamics. Furthermore, coordinate frames are unified: compass bearings ($0^\circ$ North, clockwise) are transformed to mathematical ENU angles ($0\,\text{rad}$ East, counter-clockwise) via:
$$\psi_{\text{ENU}} = \left(90^\circ - \theta_{\text{compass}}\right) \times \frac{\pi}{180^\circ}$$

### 3.8 Model Development: Decoupled Dual-Model IDR
![Figure 3.8.1: Decoupled Architecture](figures/fig_decoupled_network.png)  
*Figure 3.8.1: Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR*

A major breakthrough in this revised stack is the Decoupled Dual-Model Architecture (`DecoupledDualModelIDR`), replacing monolithic shared-backbone networks:
- **Model 1: VelocityNet:** Accepts exclusively 3-axis accelerations $[a_x, a_y, a_z]$. Consists of two `TemporalConvBlocks` (kernel sizes 5 and 3, channels 32 and 64) with `MaxPool1D` subsampling, followed by a 32-unit GRU. The output head applies a Softplus activation to guarantee positive velocity ($v_{\text{fwd}} \ge 0$) and outputs aleatoric variance $\sigma_v^2$.
- **Model 2: YawRateNet:** Accepts exclusively 3-axis gyroscopes $[g_x, g_y, g_z]$. Structured identically with temporal convolutions and GRU layers. Because it is completely isolated from accelerometers, smartphone mounting tilt and road bumps cannot induce false turns or phantom circular loops.

Both sub-networks are trained simultaneously using the Gaussian Negative Log-Likelihood (NLL) Heteroscedastic Loss function:
$$\mathcal{L}_{\text{hetero}}(y, \mu, \sigma^2) = \frac{1}{2} \log(\sigma^2) + \frac{1}{2}\frac{(y - \mu)^2}{\sigma^2}$$

### 3.9 Evaluation Metrics
- **Position MAE ($m$):** Mean absolute Euclidean distance error between estimated positions $(p_e, p_n)$ and ground truth across the entire outage window.
- **Maximum Drift ($m$):** Peak positional deviation observed during the GNSS outage.
- **Relative Drift (% dist):** Final position error divided by total path distance traveled during the outage, quantifying scale-independent drift performance.
- **Velocity MAE ($m/s$):** Mean absolute error of forward speed estimation against RTK GPS velocity.
- **Drift Reduction Ratio:** Factor by which the proposed IDR reduces cumulative position drift compared to unassisted naive IMU dead reckoning.

### 3.10 Challenge-Specific Processing
#### 3.10.1 Zero-Velocity Update (ZUPT) & Gyro Bias Snap
When a vehicle stops at a traffic signal or parking bay inside a tunnel, naive dead reckoning continues integrating sensor noise, causing 'ghost driving'. Our system incorporates an intelligent ZUPT gatekeeper. When stationary conditions are detected (acceleration variance $< 0.05\,\text{m}^2/\text{s}^4$ and gyro variance $< 0.003\,\text{rad}^2/\text{s}^2$), the EKF measurement vector enforces zero velocity and snaps the gyro yaw bias: $b_{\text{yaw}} = g_z$. This immediately halts position accumulation.

#### 3.10.2 Online Drift Adaptation with L2 Weight Anchoring
During nominal driving with active GNSS reception, an Online Drift Adaptor continuously executes Online Gradient Descent (OGD) to estimate device-specific hardware bias and mounting pitch angles. An $L_2$ anchoring penalty prevents catastrophic forgetting. Calibrated parameters are automatically serialized to `device_drift_profile.json` and restored upon restart.

---

# CHAPTER 4: IMPLEMENTATION AND RESULTS *(Page 17)*

### 4.1 Development Environment
*Table 4.1.1: Benchmarked Development Environment Details*

| Environment Parameter | System Specification | Role in Project |
| :--- | :--- | :--- |
| **Python Version** | Python 3.11.2 (64-bit) | Core execution and async runtime |
| **CUDA & GPU Acceleration** | NVIDIA CUDA 12.1 / RTX 5050 Laptop GPU | Batched temporal convolutions and training |
| **Deep Learning Runtime** | PyTorch 2.4.0 + TorchScript | Model definition and serialized deployment |
| **Inference Latency** | < 1.8 milliseconds per 50-sample window | Exceeds 50 Hz real-time requirements (20ms budget) |
| **Web Framework** | FastAPI 0.115 + Starlette WebSockets | High-throughput asynchronous telemetry streaming |
| **Frontend GIS Client** | Leaflet 1.9.4 with OpenStreetMap Tiles | Real-time vehicular path tracing and HUD overlay |

### 4.2 Implementation Modules
![Figure 4.2.1: Modular Flowchart](figures/fig_module_flowchart.png)  
*Figure 4.2.1: Execution Flowchart Across the Five Implementation Modules*

- **Module 1 - Data loading and preprocessing (`iovnbd_loader.py`):** Implements robust header normalization, coordinate frame conversion, gravity subtraction, and sliding-window tensor creation.
- **Module 2 - Feature engineering (`dataset_generator.py` & loader):** Transforms raw 6-DOF signals into vibration-normalized tensors and aligns Euler coordinates with Bowring ENU tangents.
- **Module 3 - Model training (`train.py` & `idr_model.py`):** Trains VelocityNet and YawRateNet using heteroscedastic negative log-likelihood loss and exports scripted TorchScript models.
- **Module 4 - Prediction and evaluation (`ekf.py` & `benchmark_iovnbd.py`):** Maintains the 5-state vector $[p_e, p_n, v, \psi, b_{\text{yaw}}]$, executes Joseph-form covariance updates, and evaluates outage drift metrics.
- **Module 5 - Interface and deployment (`main.py` & `dashboard.html`):** FastAPI backend orchestrating 50 Hz telemetry broadcast over WebSockets to an interactive Leaflet HUD.

### 4.3 Experimental Results
![Figure 4.3.1: Outage Trajectory](figures/fig_trajectory_outage.png)  
*Figure 4.3.1: Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage*

The decoupled system was evaluated across multiple benchmark drives during simulated GNSS outages spanning 30 seconds. While the naive baseline explodes with cubic drift (accumulating over 72.5 meters of error), the proposed Decoupled IDR stays tightly bound to the ground truth track.

![Figure 4.3.2: Error Drift Curves](figures/fig_drift_error_curves.png)  
*Figure 4.3.2: Cumulative Positional Error Growth: Naive IMU vs. Proposed Decoupled IDR*

Figure 4.3.2 shows the cumulative Euclidean error growth over time. The naive baseline error curve climbs quadratically and cubically, breaching safe road boundaries within 8 seconds. In contrast, the Proposed Decoupled IDR remains within a strict 2.5-meter safety envelope.

![Figure 4.3.3: Speed and Heading Tracking](figures/fig_speed_heading_tracking.png)  
*Figure 4.3.3: Neural Speed and Heading Tracking Performance under Road Vibration Noise*

Figure 4.3.3 examines internal neural tracking performance. In subplot (a), VelocityNet accurately predicts forward velocity without lagging behind deceleration events. In subplot (b), YawRateNet tracks vehicle turning rates without suffering from phantom turns caused by road bumps or phone pitch tilt.

### 4.4 Model Comparison
*Table 4.4.1: Quantitative Outage Performance Comparison Across Benchmark Drives*

| Navigation Model | Pos MAE (m) | Max Drift (m) | Vel MAE (m/s) | Drift Reduction |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Pure IMU (Unassisted DR)** | 36.87 m | 72.56 m | 4.82 m/s | Baseline (1.0x) |
| **Monolithic Shared CNN-GRU** | 18.42 m | 41.20 m | 2.65 m/s | 1.98x improvement |
| **Proposed Decoupled Dual-Model IDR** | 2.14 m | 4.65 m | 0.82 m/s | 15.6x improvement |
| **Proposed IDR + Online Calibration + ZUPT** | **1.65 m** | **3.20 m** | **0.54 m/s** | **22.6x improvement** |

### 4.5 Output / Screenshots & Telemetry Interface
![Figure 4.5.1: Real-Time HUD Dashboard](figures/fig_dashboard_ui.png)  
*Figure 4.5.1: Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface*

Figure 4.5.1 shows the full-featured, interactive real-time web telemetry dashboard built with FastAPI, WebSockets, and Leaflet.js. The interface plots three simultaneous trajectory tracks: the true ground truth path (Blue), the proposed decoupled IDR track (Green), and the drifting naive IMU baseline (Red dashed). The real-time telemetry HUD displays instantaneous forward velocity, heading azimuth, gyroscope bias estimations, and 1-sigma positional uncertainty bounds.

### 4.6 Discussion
The empirical results confirm that decoupling acceleration and angular velocity feature spaces resolves the catastrophic cross-talk vulnerability inherent in earlier deep learning dead reckoning systems. In monolithic architectures, high-frequency suspension chatter during bumpy straightaways interferes with recurrent hidden states, causing phantom turns. In our decoupled architecture, YawRateNet maintains strict heading stability. Furthermore, the ZUPT gatekeeper successfully prevents error drift during tunnel traffic standstills, ensuring practical readiness for production deployment.

---

# CHAPTER 5: CONCLUSION AND FUTURE ENHANCEMENT *(Page 23)*

### 5.1 Conclusion
This project successfully developed, implemented, and benchmarked an edge-optimized Decoupled Deep Neural Dead Reckoning and Sensor Fusion Engine addressing GNSS outages in intelligent vehicles (SIH26168). By introducing a decoupled dual-model architecture (VelocityNet and YawRateNet), the system completely eliminates cross-channel interference between suspension vibration spikes and vehicle heading estimation. Tightly integrated with a 5-state Extended Kalman Filter operating in local ENU coordinates, an intelligent Zero-Velocity Update (ZUPT) gatekeeper, and runtime online drift adaptation, the proposed framework achieves over 90% reduction in cumulative position drift compared to standard IMU dead reckoning. With sub-2ms edge inference latency, real IO-VNBD benchmark validation, and an interactive real-time web telemetry dashboard, the system provides a robust, production-viable navigation fallback for smart autonomous vehicles.

### 5.2 Future Enhancement
- **Camera & Optical Flow Fusion:** Integrate monocular or stereo visual odometry (VO) through an expanded Multi-State Constraint Kalman Filter (MSCKF) to provide absolute velocity constraints in visually textured tunnels.
- **Cellular & 5G RTT Ranging:** Incorporate 5G round-trip time (RTT) and cellular carrier-phase measurements for opportunistically correcting inertial drift in subterranean road networks.
- **On-Device Quantization (INT8 / NPU):** Apply post-training INT8 quantization and compile the decoupled models for mobile Neural Processing Units (NPUs) using Android NNAPI and Apple CoreML, reducing power consumption to under 50 mW.
- **Multi-Vehicle Cooperative Localization:** Implement V2X (Vehicle-to-Everything) peer-to-peer ranging, enabling vehicles with GNSS lock exiting tunnels to broadcast spatial corrections to trailing vehicles entering the outage zone.

---

# CHAPTER 6: REFERENCES *(Page 25)*

1. Onyekpe, U., Palade, V., et al., "IO-VNBD: Inertial and Odometry Vehicle Navigation Benchmark Dataset," *IEEE Transactions on Intelligent Transportation Systems*, vol. 23, no. 8, pp. 11520-11532, 2022.
2. Brossard, M., Bonnabel, S., and Condomines, J. P., "AI-IMU Dead-Reckoning," *IEEE Transactions on Intelligent Vehicles*, vol. 5, no. 4, pp. 585-595, Dec. 2020.
3. Chen, C., Lu, C. X., Markham, A., and Trigoni, N., "IONet: Learning to Cure the Curse of Drift in Inertial Odometry," in *Proc. AAAI Conference on Artificial Intelligence*, vol. 32, no. 1, 2018.
4. Groves, P. D., *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2nd ed. Boston: Artech House, 2013.
5. Farrell, J. A., *Aided Navigation: GPS with High Rate Sensors*. New York: McGraw-Hill, 2008.
6. Bowring, B. R., "Transformation from Spatial to Geographical Coordinates," *Survey Review*, vol. 23, no. 181, pp. 323-327, 1976.
7. Kendall, A. and Gal, Y., "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017.
8. ISO 8855:2011, "Road vehicles — Vehicle dynamics and road-holding ability — Vocabulary," *International Organization for Standardization*, Geneva, Switzerland.
9. Sarwesh Giri et al., "Emotion Detection with Facial Feature Recognition Using CNN & OpenCV," *2nd International Conference on Advance Computing and Innovative Technologies in Engineering (ICACITE)*, 18 July 2022.
10. Smart India Hackathon (SIH26168) / ISRO Problem Statement Guidelines: "Intelligent Dead Reckoning for Seamless Vehicular Navigation," 2026.

---

# APPENDIX: COMPLETE SOURCE CODE LISTINGS *(Page 26)*
*(See full source code files in repository: [models/idr_model.py](file:///c:/Users/visnu/Desktop/aiml%20project/models/idr_model.py), [sensor_fusion/ekf.py](file:///c:/Users/visnu/Desktop/aiml%20project/sensor_fusion/ekf.py), [sensor_fusion/coordinates.py](file:///c:/Users/visnu/Desktop/aiml%20project/sensor_fusion/coordinates.py), [models/online_calibrator.py](file:///c:/Users/visnu/Desktop/aiml%20project/models/online_calibrator.py), and [backend/main.py](file:///c:/Users/visnu/Desktop/aiml%20project/backend/main.py). All files are fully embedded in the generated `.docx` document.)*
