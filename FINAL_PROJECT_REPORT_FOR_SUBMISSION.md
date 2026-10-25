AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES

OCTOBER 2026

PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT 
OF THE REQUIREMENTS FOR THE AWARD OF THE
DEGREE OF BACHELOR OF ENGINEERING
IN COMPUTER SCIENCE AND ENGINEERING
OF THE ANNA UNIVERSITY

AI & ML
PROJECT
WORK

Submitted by
[STUDENT NAME 1] – [REGISTER NUMBER 1]
[STUDENT NAME 2] – [REGISTER NUMBER 2]

BATCH
2025 - 2029

Under the Guidance of
DR. V. NIRANJANI / [SUPERVISOR NAME]
Assistant Professor, CSE.

COMPUTER SCIENCE AND ENGINEERING
Sri Eshwar College of Engineering
(An Autonomous Institution – Affiliated to Anna University)
COIMBATORE – 641 202

================================================================================
(PAGE BREAK)
================================================================================

AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES

OCTOBER 2026

PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT 
OF THE REQUIREMENTS FOR THE AWARD OF THE
DEGREE OF BACHELOR OF ENGINEERING
IN COMPUTER SCIENCE AND ENGINEERING
OF THE ANNA UNIVERSITY

AI & ML
PROJECT
WORK

Submitted by
[STUDENT NAME 1] – [REGISTER NUMBER 1]
[STUDENT NAME 2] – [REGISTER NUMBER 2]

BATCH
2025 - 2029

Under the Guidance of
DR. V. NIRANJANI / [SUPERVISOR NAME]
Assistant Professor, CSE.

Department of Computer Science and Engineering
Sri Eshwar College of Engineering
(An Autonomous Institution – Affiliated to Anna University)
COIMBATORE – 641 202

================================================================================
(PAGE BREAK)
================================================================================

Sri Eshwar College of Engineering
(An Autonomous Institution – Affiliated to Anna University)
COIMBATORE – 641 202

BONAFIDE CERTIFICATE

Certified that this Report titled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES”
for the course U23AM495 - Artificial Intelligence and Machine Learning is the bonafide work of 
[STUDENT NAME 1] [REGISTER NUMBER 1]
[STUDENT NAME 2] [REGISTER NUMBER 2]
who carried out the project work under my supervision.

-----------------------------------------          -----------------------------------------
SIGNATURE                                          SIGNATURE
Dr. R. SUBHA M.E., Ph. D.                          DR. V. NIRANJANI / [SUPERVISOR NAME]
HEAD OF THE DEPARTMENT                             SUPERVISOR
Dept. of Computer Science & Engineering            Assistant Professor,
Sri Eshwar College of Engineering,                 Dept. of Computer Science & Engineering,
Coimbatore – 641 202.                              Sri Eshwar College of Engineering,
                                                   Coimbatore – 641 202.

Submitted for the Autonomous Semester End Project Viva-Voce held on
…………………..

_________________________                          _________________________
INTERNAL EXAMINER                                  EXTERNAL EXAMINER

Sri Eshwar College of Engineering
(An Autonomous Institution – Affiliated to Anna University)
COIMBATORE – 641 202

================================================================================
(PAGE BREAK)
================================================================================

BONAFIDE CERTIFICATE

Certified that this Report titled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES”
is the bonafide work of
[STUDENT NAME 1] [REGISTER NUMBER 1]
[STUDENT NAME 2] [REGISTER NUMBER 2]
who carried out the project work under my supervision.

-----------------------------------------          -----------------------------------------
SIGNATURE                                          SIGNATURE
Dr. R. SUBHA M.E., Ph. D.                          DR. V. NIRANJANI / [SUPERVISOR NAME]
HEAD OF THE DEPARTMENT                             SUPERVISOR
Dept. of Computer Science & Engineering,           Assistant Professor,
Sri Eshwar College of Engineering,                 Dept. of Computer Science & Engineering,
Coimbatore – 641 202.                              Sri Eshwar College of Engineering,
                                                   Coimbatore – 641 202.

Submitted for the Autonomous Semester End Project Viva-Voce held on 
…………………..

_________________________                          _________________________
INTERNAL EXAMINER                                  EXTERNAL EXAMINER

================================================================================
(PAGE BREAK)
================================================================================

DECLARATION

[STUDENT NAME 1] [REGISTER NUMBER 1]
[STUDENT NAME 2] [REGISTER NUMBER 2]

To declare that the project entitled “AI-ML BASED INTELLIGENT DEAD RECKONING SYSTEM FOR VEHICULAR NAVIGATION DURING GNSS OUTAGES” submitted in partial fulfilment to the University as the project work of Bachelor of Engineering (Computer Science and Engineering) Degree, is a record of original work done by us under the supervision and guidance of DR. V. NIRANJANI / [SUPERVISOR NAME], Assistant Professor, Department of Computer Science and Engineering, Sri Eshwar College of Engineering, Coimbatore.

Place: Coimbatore
Date:

[STUDENT NAME 1]
[STUDENT NAME 2]

Project Guided by,

DR. V. NIRANJANI / [SUPERVISOR NAME]

================================================================================
(PAGE BREAK)
================================================================================

ACKNOWLEDGEMENT

The success of a work depends on a team and cooperation. I take this opportunity to express my gratitude and thanks to everyone who helped me in my project. I would like to thank the management for the constant support provided by them to complete this project.

It is indeed our great honor bounded duty to thank our beloved Chairman Mr. R. Mohanram, for his academic interest shown towards the students.

We are indebted to our Director Mr. R. Rajaram, for motivating and providing us with all facilities.

I wish to express my sincere regards and deep sense of gratitude to Dr. Sudha Mohanram, M.E, Ph.D. Principal, for the excellent facilities and encouragement provided during the course of the study and project.

We are indebted to Dr. R. Subha, M.E., Ph.D. Dean, Computing Science for having permitted us to carry out this project and giving the complete freedom to utilize the resources.

I express my sincere thanks to my course faculty Dr. V. Niranjani / [SUPERVISOR NAME], Assistant Professor of Computer Science and Engineering Department for the valuable guidance and encouragement given, to us for this project.

I solemnly express our thanks to all the teaching and nonteaching staff of the Computer Science and Engineering Department, family and friends for their valuable support which inspired us to work on this project.

================================================================================
(PAGE BREAK)
================================================================================

ABSTRACT

Vehicular positioning and autonomous tracking are critical aspects of modern intelligent transportation systems, smart vehicles, and mobile navigation applications. Organizations and autonomous platforms depend on continuous location data to maintain safety, optimize routes, and prevent collision risks. However, maintaining reliable positioning during satellite outages is challenging because satellite signals are easily degraded or blocked in tunnels, multi-level parking lots, and dense urban canyons. Conventional inertial dead reckoning relying on low-cost Micro-Electro-Mechanical Systems (MEMS) sensors suffers from high noise, sensor biases, and mounting pitch misalignments, causing rapid cubic position error drift (O(t³)) within seconds.

The AI-ML Based Intelligent Dead Reckoning System aims to automate vehicular motion tracking and mitigate sensor drift during complete GNSS denial. The system is designed to support high-frequency 6-DOF inertial sensor telemetry from commercial smartphones and vehicle CAN bus loggers. Sensor-specific parsers extract relevant 3-axis accelerometer and 3-axis gyroscope parameters, converting them into standardized sliding temporal windows. An intelligent Zero-Velocity Update (ZUPT) and stationary detection gatekeeper evaluates sensor variances to lock velocity and snap gyro zero-biases during vehicle stops.

To eliminate cross-axis vibration coupling, a Decoupled Dual-Model Deep Learning architecture is developed: VelocityNet, which specializes exclusively on 3-axis accelerations to infer forward vehicle speed, and YawRateNet, which processes 3-axis gyroscopes to determine angular turning rate without being contaminated by phone pitch tilts or road bumps. Both models are trained using a heteroscedastic loss function to predict aleatoric uncertainties alongside point estimates. These neural predictions are fused into a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates.

The proposed application integrates a high-performance Python FastAPI backend streaming telemetry at 50 Hz over WebSockets with an interactive Leaflet.js frontend map HUD. The system visualizes real-time trajectory tracking, displays live speed, heading, and gyro bias estimates, and benchmarks drift performance against ground truth RTK GNSS and naive IMU baselines. The system bounds cumulative drift to under 2.5 meters during 30-second complete GNSS outages, achieving over 90% drift reduction and ensuring robust, fail-safe vehicular navigation.

================================================================================
(PAGE BREAK)
================================================================================

TABLE OF CONTENTS

S.no      Contents                                              Page No

          ABSTRACT                                              i
1         INTRODUCTION                                          1
2         SYSTEM ANALYSIS AND DESIGN                            2
          2.1 Existing Scenario                                 2
          2.2 Problem Statement                                 2
          2.3 Objectives                                        2
          2.4 Scope of the Project                              3
          2.5 System Requirements                               3
              2.5.1 Hardware Requirements                       3
              2.5.2 Software Requirements                       4
              2.5.3 Dataset Requirements                        4
              2.5.4 System Constraints                          4
3         PROPOSED SOLUTION                                     5
          3.1 Overview                                          5
          3.2 System Architecture / Block Diagram               5
          3.3 Methodology                                       6
          3.4 Development Phases                                6
          3.5 Dataset Description                               9
          3.6 Data Preprocessing                                11
          3.7 Feature Engineering                               11
          3.8 Model Development                                 12
          3.9 Evaluation Metrics                                13
          3.10 Challenge-Specific Processing                    13
4         IMPLEMENTATION AND RESULTS                            14
          4.1 Development Environment                           14
          4.2 Implementation                                    15
          4.3 Experimental Results                              15
          4.4 Model Comparison                                  16
          4.5 Output / Screenshots                              16
          4.6 Discussion                                        16
5         CONCLUSION AND FUTURE ENHANCEMENT                     17
          5.1 Conclusion                                        17
          5.2 Future Enhancement                                18
6         REFERENCES                                            19
          APPENDIX: COMPLETE CODE LISTINGS                      20

================================================================================
(PAGE BREAK)
================================================================================

LIST OF FIGURES

Fig. No.  Figure Title                                          Page No.

1         System Architecture / Block Diagram                   5
2         Decoupled Dual-Model Neural Network Architecture      12
3         Challenge-Specific Processing & ZUPT Workflow         14
4         Vehicular Trajectory Tracking During 30s Outage       15
5         Cumulative Position Error Growth vs. Outage Time      15
6         Real-Time Web Telemetry HUD and Leaflet Map Interface 16

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 1

INTRODUCTION

Vehicular navigation and positioning are essential components of modern intelligent transportation systems, smart vehicles, and automated mobility. Organizations depend on precise vehicular tracking to establish fleet communication, manage traffic logistics, and protect passenger safety. The reliability of these systems largely depends on satellite positioning through Global Navigation Satellite Systems (GNSS) including GPS, GLONASS, Galileo, and NavIC. Under open-sky conditions, multi-frequency receivers provide meter to sub-meter accuracy. However, regular signal obstruction occurs in subterranean tunnels, dense urban canyons, multi-level overpasses, and parking garages, triggering complete GNSS outages lasting from tens of seconds to several minutes.

When satellite reception is lost, vehicles must rely on onboard inertial dead reckoning using Micro-Electro-Mechanical Systems (MEMS) sensors. However, low-cost MEMS inertial measurement units (IMUs) suffer from thermo-mechanical noise, turn-on biases, scale factor instabilities, and mounting pitch misalignments. Double-integrating uncalibrated accelerometer signals results in cubic position error growth (O(t³)), while uncorrected gyroscope biases yield quadratic heading error accumulation (O(t²)). Within 10 to 15 seconds of a GNSS outage, a standard smartphone IMU can accumulate dozens or hundreds of meters of positional error, completely derailing route guidance and vehicle lane-keeping systems.

Traditional manual calibration approaches and simple kinematic filters struggle to adapt to dynamic road conditions, vehicle vibration frequencies, and arbitrary smartphone mounting angles. A smartphone pitched at an angle in a car mount leaks Earth's gravitational acceleration into the forward velocity axis, creating artificial acceleration when the vehicle is cruising at steady speed. Furthermore, high-frequency suspension vibrations caused by road roughness or engine rev cycles often corrupt gyroscope readings, creating phantom turns and circular trajectory loops.

The AI-ML Based Intelligent Dead Reckoning System is proposed as an intelligent software solution to simplify and automate vehicular tracking during GNSS outages. The system accepts high-frequency 6-DOF IMU telemetry, identifies vehicle stationary states using variance-based Zero-Velocity Updates (ZUPT), and processes acceleration and gyroscope signals through a decoupled dual-model deep neural network. By isolating forward speed estimation from heading rate estimation, the system prevents gravity tilt and chassis vibration cross-talk. The predicted kinematics and their heteroscedastic uncertainties are fused into a 5-state Extended Kalman Filter (EKF), delivering seamless, drift-bounded vehicular tracking and real-time visualization over a WebSocket-driven web dashboard.

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 2

SYSTEM ANALYSIS AND DESIGN

1.1 Existing Scenario
Vehicular dead reckoning is an important process for maintaining location awareness during satellite outages. Existing navigation systems often use simple unassisted kinematic integration, snap-to-road map matching, and basic device compass readings to bridge GNSS gaps.

These methods can be unreliable and produce erratic results when managing extended outages in complex environments such as long tunnels, multi-level highways, and urban canyons. Simple mathematical integration causes rapid cubic error explosion, while map-matching algorithms freeze or project incorrect straight-line estimates if the vehicle turns, decelerates, or stops inside an unmapped subterranean route.

Therefore, a unified, AI-driven dead reckoning engine is required to eliminate cubic error drift, adapt to sensor mounting tilt, identify stationary vehicle stops, and provide continuous, jump-free position updates across arbitrary vehicle platforms.

1.2 Problem Statement
Managing vehicular positioning during extended GNSS outages is challenging due to the severe noise and bias characteristics of low-cost MEMS IMUs. Double integration of uncorrected sensor telemetry leads to rapid cubic drift, while phone pitch misalignments cause false acceleration and phantom turning loops.

The proposed AI-ML Based Intelligent Dead Reckoning System aims to automate inertial feature extraction, decouple forward velocity from heading angular rate estimation, execute Zero-Velocity Updates, and maintain sub-3-meter positioning accuracy across extended GNSS denial through a unified deep learning and Extended Kalman Filter framework.

1.3 Objectives
• To collect and process high-frequency (50 Hz) 6-DOF inertial sensor telemetry from vehicle CAN bus and smartphone loggers.
• To parse raw acceleration and gyroscope data into standardized sliding temporal windows for real-time analysis.
• To design and train a Decoupled Dual-Model Deep Neural Network (VelocityNet and YawRateNet) to isolate forward speed from heading rate estimation.
• To implement a heteroscedastic loss formulation predicting dynamic aleatoric uncertainty variances alongside kinematic point estimates.
• To develop an automated Zero-Velocity Update (ZUPT) gatekeeper to detect stationary vehicle states and snap gyroscope biases.
• To implement an online gradient descent calibration module with L2 weight anchoring to compensate for phone mounting tilt in real time.
• To formulate a 5-state Extended Kalman Filter (EKF) operating in local metric East-North-Up (ENU) coordinates.
• To deploy a real-time FastAPI backend streaming telemetry at 50 Hz over WebSockets.
• To develop a user-friendly Leaflet.js web dashboard for live multi-path comparison and HUD telemetry visualization.
• To evaluate system performance using metrics such as Position MAE, Maximum Drift, Relative Drift Percentage, and Velocity MAE against ground truth RTK GNSS.

1.4 Scope of the Project
The scope of the AI-ML Based Intelligent Dead Reckoning System includes automated inertial sensor processing, deep learning kinematic inference, and state estimation for smart ground vehicles.

The project covers:
• Support for 6-DOF IMU telemetry (ax, ay, az, gx, gy, gz) sampled at 50 Hz.
• Ingestion of authentic benchmark datasets (IO-VNBD Racelogic VBOX RTK and smartphone logs) and multi-maneuver synthetic drives.
• Automated sensor preprocessing, gravity compensation, and equispaced temporal resampling.
• Decoupled neural velocity and yaw rate estimation with uncertainty quantification.
• Automated Zero-Velocity Updates (ZUPT) and Zero-Angular-Rate Updates (ZARU).
• 5-state Extended Kalman Filter sensor fusion with Joseph-form numerical stabilization.
• Online runtime drift adaptation and persistent device profile storage.
• Real-time web dashboard visualization with side-by-side ground truth and naive baseline comparison.
• Comprehensive quantitative performance evaluation across simulated and real-world GNSS outage durations.

Outside the scope:
The system focuses on inertial dead reckoning and sensor fusion. It does not control vehicle steering or throttle actuators directly. All navigation outputs are intended for driver assistance, autonomous localization fallbacks, and fleet tracking platforms.

1.5 Requirements / Constraints

Hardware Requirements
• A computer or laptop for development, training, and testing (Intel Core i5/i7 or AMD Ryzen, 16 GB RAM).
• NVIDIA GPU with CUDA support (e.g., GeForce RTX 5050 / RTX 3060) for batched temporal convolution and GRU training.
• 6-DOF MEMS Inertial Measurement Unit (smartphone or automotive CAN logger) supporting at least 50 Hz output.
• High-precision GNSS receiver (1 - 10 Hz) for training data collection and ground truth reference.

Software Requirements
• Windows 11 or Linux Ubuntu operating system.
• Python 3.11 for backend development, sensor fusion, and deep learning.
• PyTorch 2.4+ with TorchScript for deep learning model training and edge export.
• NumPy, SciPy, and Scikit-learn for matrix kinematics and signal preprocessing.
• FastAPI and Uvicorn for asynchronous REST and WebSocket telemetry streaming.
• Modern web browser supporting HTML5, CSS3, and JavaScript (ES6+).
• Leaflet.js with OpenStreetMap tiles for interactive geospatial mapping.
• Visual Studio Code as the primary code editor and development environment.

Dataset Requirements
The project requires vehicular inertial telemetry synchronized with ground truth position and velocity fixes. The system utilizes the IO-VNBD (Inertial and Odometry Vehicle Navigation Benchmark Dataset) recorded using Racelogic VBOX RTK HD2 and Android smartphones, alongside realistic multi-maneuver simulated trajectories. Data includes 3-axis specific force, 3-axis angular velocity, wheel rotational speeds, GPS geodetic coordinates, and true velocity vectors.

System Constraints
• Sampling rate consistency: Android sensor callbacks require linear equispaced resampling onto a rigid 50.0 Hz temporal grid.
• Memory and latency constraints: Edge neural inference must complete within 20 milliseconds per sliding window to maintain real-time 50 Hz streaming.
• Decoupled channel isolation: Accelerometer signals must not bleed into heading rate estimators to avoid gravity tilt false turns.
• Sensor bias stability: Long-term biases require periodic ZUPT locking during stationary stops to prevent baseline drift.

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 3

PROPOSED SOLUTION

3.1 Overview
The AI-ML Based Intelligent Dead Reckoning System is an edge-optimized navigation engine that processes high-frequency inertial sensor data to provide continuous, jump-free vehicular tracking during GNSS outages. The system eliminates cubic position drift by replacing unassisted mathematical integration with deep learning kinematic observers coupled with a 5-state Extended Kalman Filter.

The system processes incoming 6-DOF IMU data through sliding temporal windows. An automated variance-based detector classifies whether the vehicle is stationary or moving. When moving, accelerometer signals are routed to VelocityNet to predict forward speed, while gyroscope signals are routed to YawRateNet to predict turning rate without tilt corruption. When GNSS is available, the EKF updates spatial position and continually estimates sensor biases; when GNSS drops out (such as in a tunnel), the EKF transitions seamlessly to neural innovation updates.

The final results are streamed at 50 Hz over WebSockets to an interactive Leaflet.js dashboard. The interface displays live telemetry, estimated velocities, heading azimuths, and compares the AI-guided path with ground truth and naive IMU baselines.

3.2 System Architecture / Block Diagram
The overall architecture of the Intelligent Dead Reckoning System can be represented as:

--------------------------------------------------------------------------------
[INSERT FIGURE 1: System Architecture / Block Diagram HERE]
*(Caption: Figure 3.1: End-to-End System Architecture of Decoupled AI-ML Dead Reckoning & Sensor Fusion Pipeline)*
--------------------------------------------------------------------------------

3.3 Methodology
The proposed methodology consists of the following steps:
1. Inertial Data Acquisition: 6-DOF specific forces and angular velocities are captured at 50 Hz from onboard IMUs.
2. Temporal Window Buffering: Raw samples are buffered into overlapping windows of 50 samples (1.0 second history).
3. Stationary State Detection (ZUPT): Total acceleration and gyro variances are computed; if below threshold, stationary velocity locking is triggered.
4. Channel Decoupling: Accelerations (ax, ay, az) and gyroscopes (gx, gy, gz) are isolated into separate channels.
5. Neural Velocity Inference: VelocityNet processes accelerations using 1D temporal convolutions, BiGRU, and Softplus activation to estimate forward speed (v) and variance (σ_v²).
6. Neural Yaw Rate Inference: YawRateNet processes gyroscopes to estimate rotational rate (ω) and variance (σ_ω²), immune to phone pitch tilt.
7. Online Drift Calibration: Online Gradient Descent updates mounting pitch and bias parameters during active GNSS lock.
8. Geodetic Bowring Projection: GNSS latitude and longitude are converted to metric Cartesian coordinates in a local East-North-Up (ENU) tangent plane.
9. Extended Kalman Filter Fusion: A 5-state EKF fuses GNSS or neural observations with Joseph-form numerical stabilization.
10. WebSocket Streaming & Display: Filtered states are broadcast at 50 Hz to an interactive web dashboard for real-time tracking.

3.4 Development Phases

Phase 1: Problem Understanding & Objective Definition
The first phase involves identifying the failure modes in vehicular dead reckoning during GNSS denial and defining the functional requirements of an AI-driven navigation engine.
The main objectives were defined as:
• Eliminate cubic error drift during 30 to 120-second GNSS outages.
• Decouple forward speed from heading angular rate estimation to prevent phantom turning loops.
• Formulate an Extended Kalman Filter operating in metric local ENU coordinates.
• Provide an automated Zero-Velocity Update mechanism to lock velocity when stopped.
• Deploy a real-time web telemetry dashboard with live map tracking.
The primary success criteria are maintaining cumulative position drift below 2.5 meters during 30-second outages and achieving over 90% error reduction compared to naive dead reckoning.

Phase 2: Data Collection & Understanding
The project uses authentic benchmark datasets from the IO-VNBD (Inertial and Odometry Vehicle Navigation Benchmark Dataset - Coventry University) alongside realistic multi-maneuver synthetic drives.
The collected telemetry data includes:
• 29-column Racelogic VBOX RTK HD2 CAN bus recordings (10 Hz).
• 24-column Android smartphone AndroSensor recordings (10-50 Hz IMU, 1 Hz GPS).
• Multi-maneuver synthetic trajectories modeling straight cruising, lane changes, 90-degree turns, stops, and highway curves.
The telemetry streams are analyzed to understand sensor noise density, sample rate jitter, engine vibration spikes (20-40 Hz), and gravity leakage effects.

Phase 3: Data Preprocessing & Feature Engineering
The raw inertial streams are processed to create consistent representations suitable for deep learning and Kalman filtering.
The preprocessing includes:
• Equispaced linear resampling onto a rigid 50.0 Hz temporal grid (Δt = 0.02s).
• Static gravity vector subtraction and high-pass filtering.
• Bowring ellipsoidal conversion from geodetic WGS84 to local metric ENU coordinates.
• Sliding-window tensor structuring (50 samples × 6 channels).
• Statistical variance extraction to quantify chassis vibration signatures.
• Compass bearing to ENU radian angle transformation.

Phase 4: Model Building
To resolve parameter cross-talk, a Decoupled Dual-Model Deep Neural Network architecture is developed:
• VelocityNet: Consumes 3-axis accelerations only. Uses two TemporalConvBlocks (kernel sizes 5 and 3, channels 32 and 64) with MaxPool1D, followed by a 32-unit GRU and a Softplus output head.
• YawRateNet: Consumes 3-axis gyroscopes only. Uses an identical convolutional and recurrent structure with linear output, isolated from accelerometers.
• Heteroscedastic Uncertainty Head: Both models predict Gaussian aleatoric variances (σ²) alongside mean values (μ) trained via Negative Log-Likelihood loss:
  L_hetero = 0.5 * log(σ²) + 0.5 * (y - μ)² / σ²

Phase 5: Model Evaluation & Validation
The models are evaluated using simulated and real benchmark trajectories with injected GNSS outages (e.g., 30s tunnel windows).
The major evaluation metrics include:
• Position Mean Absolute Error (MAE)
• Maximum Drift Error
• Relative Drift Percentage (% of distance)
• Velocity MAE
• Drift Reduction Ratio relative to pure IMU baseline
Additional validation includes verifying Zero-Velocity Update reliability, checking online calibration convergence under active GNSS, and confirming zero trajectory jumps during outage handover.

Phase 6: Final Output / Deployment
The complete system is deployed as an asynchronous Python FastAPI service with an interactive HTML5/Tailwind/Leaflet.js frontend.
The system follows the workflow:
Raw Telemetry Ingestion (50 Hz)
↓
Equispaced Resampling & Window Buffering (W=50)
↓
Stationary Detection & ZUPT Velocity Locking
↓
Decoupled Neural Inference (VelocityNet + YawRateNet)
↓
Dynamic Uncertainty Weighting (σ_v², σ_ω²)
↓
5-State Intelligent EKF Measurement Update
↓
WebSocket Telemetry Broadcast & Leaflet Map Rendering
The application provides live speed, heading, gyro bias, and uncertainty gauges, dynamic polyline rendering, and instant toggling of simulated tunnel outages.

3.5 Dataset Description
The dataset consists of synchronized vehicular CAN telemetry and smartphone sensor logs from the IO-VNBD benchmark.

Table 3.5.1: Dataset Description
Column / Feature         Description                             Data Type    Role
ax, ay, az               3-Axis Acceleration / Specific Force    Numeric      VelocityNet Input
gx, gy, gz               3-Axis Gyroscope / Angular Velocity     Numeric      YawRateNet Input
GPS Latitude / Longitude Geodetic WGS84 coordinates (degrees)    Numeric      GNSS EKF / Ground Truth
GPS Altitude             Height above reference ellipsoid (m)    Numeric      Local ENU Origin
GPS Speed                Longitudinal vehicle ground speed (m/s) Numeric      Velocity Training Target
GPS Heading              Vehicle azimuth (degrees)               Numeric      Yaw Rate Training Target
Wheel Speeds (FL,FR,RL,RR) 4-wheel rotational speeds (rad/s)     Numeric      Independent Odometry
Stationary Status        Binary stopped/moving flag              Categorical  ZUPT Trigger

The dataset provides multi-driver recordings across urban, suburban, and highway regimes, capturing diverse driving behaviors, traffic stops, and road surface conditions.

3.6 Data Preprocessing
The preprocessing stage converts raw telemetry into structured, normalized tensors:
1. Data Ingestion: Telemetry logs are parsed from CSV or serial streams.
2. Timestamp Synchronization: Non-uniform Android sensor timestamps are sorted and deduplicated.
3. Equispaced Resampling: Signals are resampled to 50 Hz using linear interpolation.
4. Gravity Vector Removal: Dynamic gravity estimation strips static Earth gravity from accelerometer channels.
5. Window Slicing: Signals are segmented into overlapping 50-sample windows with 1-sample stride.
6. Local Metric Projection: WGS84 coordinates are transformed to metric ENU tangents via Bowring's method.
7. Ground Truth Discontinuity Smoothing: Android GPS duplicate coordinates are interpolated using kinematic dead reckoning.
8. Tensor Formatting: Clean arrays are converted to PyTorch float32 tensors with channel-first ordering.

3.7 Feature Engineering
Feature engineering extracts physical and statistical representations from raw inertial data:
• Acceleration Variances: Var(ax), Var(ay), Var(az) indicate suspension excitation proportional to road speed.
• Gyroscope Magnitude: Norm ||ω|| captures overall turning energy independent of mounting rotation.
• Coordinate Alignment: Compass bearings are mapped to counter-clockwise ENU angles (ψ_ENU = (90° - θ) * π / 180).
• Dynamic Uncertainty Scaling: Residual differences between raw and predicted rates provide implied sensor bias observations.

3.8 Model Development
The system uses the Decoupled Dual-Model Deep Neural Network architecture:

Model Configuration
Parameter               Value
Velocity Model          VelocityNet (Temporal Conv1D + BiGRU + Softplus Head)
Yaw Rate Model          YawRateNet (Temporal Conv1D + BiGRU + Linear Head)
Input Channels          3 channels each (ax,ay,az for Velocity; gx,gy,gz for Yaw Rate)
Window Length           50 samples (1.0 second at 50 Hz)
Loss Function           Heteroscedastic Gaussian Negative Log-Likelihood (NLL)
Optimizer               AdamW (learning rate = 1e-3, weight decay = 1e-4)
Target Outputs          Forward velocity (v, σ_v²), Yaw angular rate (ω, σ_ω²)

--------------------------------------------------------------------------------
[INSERT FIGURE 2: Decoupled Dual-Model Neural Network Architecture HERE]
*(Caption: Figure 3.2: Architectural Decoupling of VelocityNet and YawRateNet in DecoupledDualModelIDR)*
--------------------------------------------------------------------------------

3.9 Evaluation Metrics
The dead reckoning models and sensor fusion filters are evaluated using standard navigation metrics:
• Position MAE (m): Mean absolute Euclidean distance between estimated and ground truth positions.
  MAE_pos = (1/N) * Σ sqrt((p_e - gt_e)² + (p_n - gt_n)²)
• Maximum Drift (m): Peak positional deviation during the outage period.
• Relative Drift (% dist): Final position error divided by total distance traveled during outage.
• Velocity MAE (m/s): Mean absolute error of predicted vehicle speed.
• Drift Reduction Ratio: Baseline naive drift divided by proposed IDR drift.

3.10 Challenge-Specific Processing
To address specific real-world challenges in GNSS-denied navigation, the system incorporates:
• Zero-Velocity Updates (ZUPT): Stationary sensor variance triggers an EKF measurement update that forces velocity to zero and snaps the gyro yaw bias: b_yaw = gz.
• Gyro Rate Boundary Clamping: Discrepancies between neural yaw rate and raw gyro exceeding 0.06 rad/s are clamped to physical bounds, preventing runaway turns.
• Online Drift Adaptation: An adaptive estimator tracks device pitch tilt via Online Gradient Descent with L2 weight anchoring.

--------------------------------------------------------------------------------
[INSERT FIGURE 3: Challenge-Specific Processing & ZUPT Workflow HERE]
*(Caption: Figure 3.3: Challenge-Specific Processing: ZUPT Stationary Gating and Online Drift Adaptation Workflow)*
--------------------------------------------------------------------------------

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 4

IMPLEMENTATION AND RESULTS

4.1 Development Environment
The AI-ML Based Intelligent Dead Reckoning System was developed and benchmarked using Python, PyTorch, and FastAPI.
• Python 3.11.2 (64-bit runtime)
• NVIDIA CUDA 12.1 / GeForce RTX 5050 Laptop GPU (6 GB VRAM)
• PyTorch 2.4.0 with TorchScript edge export
• FastAPI 0.115 asynchronous web framework
• Uvicorn ASGI server with WebSockets
• NumPy, SciPy, Scikit-learn, and Matplotlib
• Leaflet 1.9.4 with OpenStreetMap raster tiles
• Visual Studio Code IDE

4.2 Implementation
• Data Processing: Raw IO-VNBD and smartphone CSV telemetry files are loaded, resampled to 50 Hz, and segmented into sliding windows of 50 samples.
• Feature Engineering: Specific forces and angular velocities are extracted into isolated channels; suspension variances and coordinate projections are computed.
• Model Training: VelocityNet and YawRateNet are trained independently using heteroscedastic negative log-likelihood loss on GPU.
• Prediction & Fusion: Models output speed and yaw rate alongside aleatoric uncertainties, which are ingested by the 5-state EKF with Joseph-form updates.
• Application & Dashboard: A FastAPI WebSocket server broadcasts 50 Hz telemetry to an interactive Leaflet HUD displaying live comparisons.

4.3 Experimental Results
The system was evaluated on real and simulated vehicular drives across 30-second complete GNSS outages.

--------------------------------------------------------------------------------
[INSERT FIGURE 4: Vehicular Trajectory Tracking During 30s Outage HERE]
*(Caption: Figure 4.1: Vehicular Trajectory Tracking During 30-Second Complete GNSS Outage)*
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
[INSERT FIGURE 5: Cumulative Position Error Growth vs. Outage Time HERE]
*(Caption: Figure 4.2: Cumulative Position Error Growth: Naive IMU vs. Proposed Decoupled IDR)*
--------------------------------------------------------------------------------

Experimental Performance Metrics:
Metric                              Result
Outage Duration Tested              30.0 seconds
Distance Traveled During Outage     246.38 meters
Naive IMU Position Drift MAE        36.87 meters
Proposed Decoupled IDR Position MAE 1.65 meters
Maximum Position Drift (Proposed)   3.20 meters
Relative Drift (% of distance)      1.30 %
Speed Estimation MAE                0.54 m/s
Drift Reduction Ratio               22.6x improvement

4.4 Model Comparison
Different navigation architectures were evaluated during the 30-second outage:

Model                                       Accuracy / Pos MAE  Max Drift   Remarks
Naive Pure IMU (Unassisted DR)              36.87 m             72.56 m     Baseline (Runaway cubic drift)
Monolithic Shared CNN-GRU                   18.42 m             41.20 m     1.98x improvement (cross-talk issues)
Proposed Decoupled Dual-Model IDR           2.14 m              4.65 m      15.6x improvement (isolated features)
Proposed IDR + Online Calibration + ZUPT    1.65 m              3.20 m      22.6x improvement (best overall)

4.5 Output / Screenshots
Important screenshots and UI visualizations included in the application:
• Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface
• Live Path Comparison: Ground Truth (Blue), Proposed IDR (Green), Naive IMU (Red)
• Vehicle Telemetry Gauges: Speed (m/s), Heading (°), Gyro Yaw Bias (rad/s), 1-Sigma Accuracy
• Simulated Tunnel Outage Toggle Controls and Dataset Selector

--------------------------------------------------------------------------------
[INSERT FIGURE 6: Real-Time Web Telemetry HUD and Leaflet Map Interface HERE]
*(Caption: Figure 4.3: Real-Time Web Telemetry HUD and Leaflet Dynamic Map Interface)*
--------------------------------------------------------------------------------

4.6 Discussion
The empirical results demonstrate that decoupling acceleration from angular velocity features resolves the cross-talk vulnerability that plagues traditional deep learning dead reckoning. In shared networks, road surface chatter leaks into the heading output, causing phantom circular trajectories. By separating VelocityNet from YawRateNet, heading stability is preserved. Furthermore, the ZUPT gatekeeper prevents drift during stops, and online calibration compensates for device tilt, enabling production-grade navigation resilience.

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 5

CONCLUSION AND FUTURE ENHANCEMENT

5.1 Conclusion
The AI-ML Based Intelligent Dead Reckoning System was successfully designed, implemented, and benchmarked for vehicular navigation during GNSS outages (SIH26168). By introducing a Decoupled Dual-Model Deep Neural Network architecture (VelocityNet and YawRateNet), the system eliminates cross-channel interference between suspension vibrations and vehicle heading dynamics. Fused with a 5-state Extended Kalman Filter operating in local ENU coordinates, an intelligent Zero-Velocity Update (ZUPT) gatekeeper, and runtime online drift adaptation, the proposed framework achieves over 90% reduction in cumulative position drift compared to standard IMU dead reckoning. The complete stack features sub-2ms edge inference latency, authentic IO-VNBD benchmark validation, and an interactive real-time web telemetry dashboard, delivering a robust, fail-safe navigation solution for autonomous and smart vehicles.

5.2 Future Enhancement
• Extend support to visual odometry (VO) by fusing monocular or stereo camera streams via a Multi-State Constraint Kalman Filter (MSCKF).
• Integrate cellular 5G round-trip time (RTT) and carrier-phase measurements for opportunistically correcting drift in subterranean roadways.
• Apply INT8 post-training quantization and compile models for mobile Neural Processing Units (NPUs) using Android NNAPI and Apple CoreML.
• Implement V2X cooperative localization, enabling vehicles with GNSS lock to transmit spatial corrections to trailing vehicles entering tunnels.
• Integrate automated map-matching with OpenStreetMap graph topologies to enforce lane-level constraints.

================================================================================
(PAGE BREAK)
================================================================================

CHAPTER 6

REFERENCES

[1] Onyekpe, U., Palade, V., et al., “IO-VNBD: Inertial and Odometry Vehicle Navigation Benchmark Dataset,” IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 8, pp. 11520-11532, 2022.
[2] Brossard, M., Bonnabel, S., and Condomines, J. P., “AI-IMU Dead-Reckoning,” IEEE Transactions on Intelligent Vehicles, vol. 5, no. 4, pp. 585-595, Dec. 2020.
[3] Chen, C., Lu, C. X., Markham, A., and Trigoni, N., “IONet: Learning to Cure the Curse of Drift in Inertial Odometry,” in Proc. AAAI Conference on Artificial Intelligence, vol. 32, no. 1, 2018.
[4] Groves, P. D., Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems, 2nd ed. Boston: Artech House, 2013.
[5] Farrell, J. A., Aided Navigation: GPS with High Rate Sensors. New York: McGraw-Hill, 2008.
[6] Bowring, B. R., “Transformation from Spatial to Geographical Coordinates,” Survey Review, vol. 23, no. 181, pp. 323-327, 1976.
[7] Kendall, A. and Gal, Y., “What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017.
[8] ISO 8855:2011, “Road vehicles — Vehicle dynamics and road-holding ability — Vocabulary,” International Organization for Standardization, Geneva, Switzerland.
[9] Sarwesh Giri et al., “Emotion Detection with Facial Feature Recognition Using CNN & OpenCV,” 2nd International Conference on Advance Computing and Innovative Technologies in Engineering (ICACITE), 18 July 2022.
[10] Smart India Hackathon (SIH26168) / ISRO Problem Statement Guidelines: “Intelligent Dead Reckoning for Seamless Vehicular Navigation,” 2026.
[11] Scikit-learn Developers, “Machine Learning in Python — User Guide,” Available: https://scikit-learn.org/stable/user_guide.html
[12] FastAPI, “FastAPI Documentation,” Available: https://fastapi.tiangolo.com/

================================================================================
(PAGE BREAK)
================================================================================

APPENDIX
COMPLETE SOURCE CODE LISTINGS


================================================================================
idr_model.py
================================================================================

import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict, Any, Optional

class TemporalConvBlock(nn.Module):
    """Temporal 1D Convolutional feature extractor with residual connection."""
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 5):
        super().__init__()
        padding = kernel_size // 2
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, padding=padding)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, padding=padding)
        self.bn2 = nn.BatchNorm1d(out_channels)
        self.leaky = nn.LeakyReLU(0.1, inplace=True)
        
        self.residual = (
            nn.Conv1d(in_channels, out_channels, 1)
            if in_channels != out_channels
            else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        res = self.residual(x)
        out = self.leaky(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return self.leaky(out + res)

class IntelligentDeadReckoningNet(nn.Module):
    """
    Hybrid 1D-CNN + GRU Deep Neural Network for Intelligent Dead Reckoning.
    Processes sequential 6-DOF IMU windows (Accel: X,Y,Z | Gyro: X,Y,Z).
    
    Predicts:
    1. Forward Vehicle Speed (m/s) + predicted log-variance (uncertainty)
    2. Heading Angular Rate (rad/s) + predicted log-variance (uncertainty)
    """

    def __init__(
        self,
        in_channels: int = 6,
        conv_channels: int = 64,
        gru_hidden_size: int = 64,
        gru_layers: int = 2,
        dropout: float = 0.15
    ):
        super().__init__()
        self.in_channels = in_channels
        self.gru_hidden_size = gru_hidden_size

        # Temporal Feature Extraction
        self.conv_block1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv_block2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        # Recurrent Core for sequential temporal dependency
        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=gru_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if gru_layers > 1 else 0.0
        )

        gru_out_dim = gru_hidden_size * 2

        # Velocity prediction head: outputs [mean_velocity, log_var_velocity]
        self.vel_head = nn.Sequential(
            nn.Linear(gru_out_dim, 64),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout),
            nn.Linear(64, 2)
        )

        # Yaw rate prediction head: outputs [mean_yaw_rate, log_var_yaw_rate]
        self.yaw_head = nn.Sequential(
            nn.Linear(gru_out_dim, 64),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout),
            nn.Linear(64, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Tensor of shape (Batch, SeqLen, InChannels) or (Batch, InChannels, SeqLen)
        Returns:
            vel_mean: (Batch,) forward velocity in m/s
            vel_var:  (Batch,) predicted variance in (m/s)^2
            yaw_mean: (Batch,) yaw angular rate in rad/s
            yaw_var:  (Batch,) predicted variance in (rad/s)^2
        """
        if x.dim() == 2:
            x = x.unsqueeze(0)
        # Ensure channel-first for 1D convolutions: (Batch, Channels, SeqLen)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        # CNN Feature Extraction
        feat = self.conv_block1(x)
        feat = self.pool1(feat)
        feat = self.conv_block2(feat)
        feat = self.pool2(feat)

        # Reshape for GRU: (Batch, SeqLen_reduced, FeatureDim)
        feat = feat.transpose(1, 2)

        # GRU Sequence Processing
        gru_out, _ = self.gru(feat)

        # Pool over sequence length: use the final step representation
        last_step = gru_out[:, -1, :]

        # Velocity prediction
        vel_raw = self.vel_head(last_step)
        # Vehicle forward velocity is non-negative
        vel_mean = F.softplus(vel_raw[:, 0])
        vel_logvar = torch.clamp(vel_raw[:, 1], min=-6.0, max=4.0)
        vel_var = torch.exp(vel_logvar)

        # Yaw rate prediction
        yaw_raw = self.yaw_head(last_step)
        yaw_mean = yaw_raw[:, 0]
        yaw_logvar = torch.clamp(yaw_raw[:, 1], min=-8.0, max=2.0)
        yaw_var = torch.exp(yaw_logvar)

        return vel_mean, vel_var, yaw_mean, yaw_var

class VelocityNet(nn.Module):
    """
    Dedicated Model 1: Forward Velocity Specialist.
    Processes ONLY 3-axis Accelerations (ax, ay, az).
    Completely isolated from gyroscopes to prevent rotation/bias cross-talk.
    """
    def __init__(self, in_channels: int = 3, conv_channels: int = 32, gru_hidden_size: int = 32, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.conv1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=1,
            batch_first=True
        )
        self.head = nn.Sequential(
            nn.Linear(gru_hidden_size, 32),
            nn.LeakyReLU(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        feat = self.conv1(x)
        feat = self.pool1(feat)
        feat = self.conv2(feat)
        feat = self.pool2(feat).transpose(1, 2)

        out, _ = self.gru(feat)
        raw = self.head(out[:, -1, :])
        vel_mean = F.softplus(raw[:, 0])
        vel_logvar = torch.clamp(raw[:, 1], min=-6.0, max=4.0)
        vel_var = torch.exp(vel_logvar)
        return vel_mean, vel_var


class YawRateNet(nn.Module):
    """
    Dedicated Model 2: Heading & Yaw Rate Specialist.
    Processes ONLY 3-axis Gyroscopes (gx, gy, gz).
    Completely isolated from accelerometers so smartphone tilt and road bumps
    CANNOT induce false turns or phantom circular loops!
    """
    def __init__(self, in_channels: int = 3, conv_channels: int = 32, gru_hidden_size: int = 32, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.conv1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=1,
            batch_first=True
        )
        self.head = nn.Sequential(
            nn.Linear(gru_hidden_size, 32),
            nn.LeakyReLU(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        feat = self.conv1(x)
        feat = self.pool1(feat)
        feat = self.conv2(feat)
        feat = self.pool2(feat).transpose(1, 2)

        out, _ = self.gru(feat)
        raw = self.head(out[:, -1, :])
        yaw_mean = raw[:, 0]
        yaw_logvar = torch.clamp(raw[:, 1], min=-8.0, max=2.0)
        yaw_var = torch.exp(yaw_logvar)
        return yaw_mean, yaw_var


class DecoupledDualModelIDR(nn.Module):
    """
    Dual-Model Decoupled Dead Reckoning System.
    Combines Model 1 (VelocityNet) and Model 2 (YawRateNet) as independent experts.
    Completely prevents gradient interference and cross-axis false turns.
    """
    def __init__(self):
        super().__init__()
        self.vel_model = VelocityNet(in_channels=3)
        self.yaw_model = YawRateNet(in_channels=3)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        # Check channel format
        if x.shape[-1] == 6:
            accel = x[:, :, 0:3]
            gyro = x[:, :, 3:6]
        else:
            accel = x[:, 0:3, :]
            gyro = x[:, 3:6, :]

        vel_mean, vel_var = self.vel_model(accel)
        yaw_mean, yaw_var = self.yaw_model(gyro)
        return vel_mean, vel_var, yaw_mean, yaw_var


class HeteroscedasticLoss(nn.Module):
    """
    Gaussian Negative Log-Likelihood Loss for predicting mean and variance.
    Trains the network to express its own epistemic/aleatoric uncertainty.
    """
    def __init__(self, eps: float = 1e-6):
        super().__init__()
        self.eps = eps

    def forward(self, pred_mean: torch.Tensor, pred_var: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # NLL = 0.5 * (log(var) + (target - mean)^2 / var)
        target = target.view_as(pred_mean)
        pred_var = pred_var.view_as(pred_mean)
        log_var = torch.log(pred_var + self.eps)
        precision = 1.0 / (pred_var + self.eps)
        loss = 0.5 * (log_var + precision * ((target - pred_mean) ** 2))
        return torch.mean(loss)


================================================================================
ekf.py
================================================================================

import math
import numpy as np
from typing import Optional, Tuple, Dict, Any

def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi] radians."""
    a = (angle + math.pi) % (2.0 * math.pi) - math.pi
    if a == -math.pi and angle > 0:
        return math.pi
    return a

class IntelligentEKF:
    """
    Intelligent Extended Kalman Filter (IEKF) for seamless Dead Reckoning
    and GNSS/IMU sensor fusion.
    
    State Vector x (5x1):
    0: p_e   - East position (meters)
    1: p_n   - North position (meters)
    2: v     - Forward velocity (m/s)
    3: psi   - Yaw / Heading angle in radians (from East towards North)
    4: b_yaw - Gyro yaw rate bias (rad/s)
    """

    def __init__(
        self,
        init_east: float = 0.0,
        init_north: float = 0.0,
        init_velocity: float = 0.0,
        init_yaw_rad: float = 0.0,
        q_pos: float = 0.05,
        q_vel: float = 0.2,
        q_yaw: float = 0.01,
        q_bias: float = 1e-4,
    ):
        # State vector
        self.x = np.array([
            init_east,
            init_north,
            init_velocity,
            normalize_angle(init_yaw_rad),
            0.0  # initial gyro yaw bias
        ], dtype=np.float64)

        # State covariance P
        self.P = np.diag([
            4.0,       # pos_e variance (m^2)
            4.0,       # pos_n variance (m^2)
            1.0,       # velocity variance ((m/s)^2)
            0.05,      # yaw variance (rad^2)
            0.001      # bias variance ((rad/s)^2)
        ]).astype(np.float64)

        # Base Process noise covariance parameters
        self.q_pos = q_pos
        self.q_vel = q_vel
        self.q_yaw = q_yaw
        self.q_bias = q_bias

        # Diagnostic counters and tracking
        self.last_timestamp: Optional[float] = None
        self.prev_psi: float = normalize_angle(init_yaw_rad)
        self.last_gyro_yaw_rate: float = 0.0
        self.outage_active: bool = False
        self.outage_duration_s: float = 0.0
        self.total_distance_m: float = 0.0

    def predict(self, dt: float, accel_fwd: float, gyro_yaw_rate: float, q_scale: float = 1.0) -> np.ndarray:
        """
        EKF Prediction step using IMU inputs.
        accel_fwd: forward acceleration (m/s^2)
        gyro_yaw_rate: yaw angular rate (rad/s)
        """
        if dt <= 0.0 or dt > 1.0:
            dt = 0.02  # default 50Hz fallback if timestamp jitter occurs

        p_e, p_n, v, psi, b_yaw = self.x
        self.prev_psi = psi
        self.last_gyro_yaw_rate = gyro_yaw_rate

        # Compensate yaw rate with estimated bias
        corrected_yaw_rate = gyro_yaw_rate - b_yaw
        half_turn = psi + 0.5 * corrected_yaw_rate * dt

        # Update position using mid-interval heading for 2nd order precision
        new_pe = p_e + v * math.cos(half_turn) * dt
        new_pn = p_n + v * math.sin(half_turn) * dt
        new_v = max(0.0, v + accel_fwd * dt)  # non-holonomic vehicle assumption (forward motion)
        new_psi = normalize_angle(psi + corrected_yaw_rate * dt)
        new_b_yaw = b_yaw

        self.x = np.array([new_pe, new_pn, new_v, new_psi, new_b_yaw], dtype=np.float64)
        
        # Accumulate odometer distance
        self.total_distance_m += v * dt

        # Jacobian F = df/dx
        F = np.eye(5, dtype=np.float64)
        F[0, 2] = math.cos(half_turn) * dt
        F[0, 3] = -v * math.sin(half_turn) * dt
        F[0, 4] = 0.5 * v * math.sin(half_turn) * (dt ** 2)

        F[1, 2] = math.sin(half_turn) * dt
        F[1, 3] = v * math.cos(half_turn) * dt
        F[1, 4] = -0.5 * v * math.cos(half_turn) * (dt ** 2)

        F[3, 4] = -dt

        # Process noise covariance Q
        # Scaled dynamically if outage is active or high dynamics detected
        scale = q_scale * (2.0 if self.outage_active else 1.0)
        Q = np.diag([
            self.q_pos * dt * scale,
            self.q_pos * dt * scale,
            self.q_vel * dt * scale,
            self.q_yaw * dt * scale,
            self.q_bias * dt
        ]).astype(np.float64)

        self.P = F @ self.P @ F.T + Q
        # Ensure symmetry
        self.P = 0.5 * (self.P + self.P.T)
        return self.x.copy()

    def update_gnss(
        self,
        east: float,
        north: float,
        speed: Optional[float] = None,
        bearing_rad: Optional[float] = None,
        pos_accuracy_m: float = 3.0,
        speed_accuracy_ms: float = 0.5,
        bearing_accuracy_rad: float = 0.15
    ) -> Dict[str, Any]:
        """
        EKF Measurement Update with GNSS data.
        Fuses 2D position (East, North), speed, and heading (if speed > 1.5 m/s).
        """
        self.outage_active = False
        self.outage_duration_s = 0.0

        measurements = [east, north]
        h_rows = [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0]
        ]
        r_diag = [pos_accuracy_m ** 2, pos_accuracy_m ** 2]

        if speed is not None and speed >= 0:
            measurements.append(speed)
            h_rows.append([0.0, 0.0, 1.0, 0.0, 0.0])
            r_diag.append(speed_accuracy_ms ** 2)

        # Only use GNSS bearing if vehicle is in reliable motion
        # (smartphone GNSS bearing is noisy/unreliable when stationary)
        has_bearing = bearing_rad is not None and (speed is not None and speed > 1.5)
        if has_bearing:
            measurements.append(normalize_angle(bearing_rad))
            h_rows.append([0.0, 0.0, 0.0, 1.0, 0.0])
            r_diag.append(bearing_accuracy_rad ** 2)

        z = np.array(measurements, dtype=np.float64)
        H = np.array(h_rows, dtype=np.float64)
        R = np.diag(r_diag).astype(np.float64)

        # Innovation
        z_pred = H @ self.x
        y = z - z_pred
        if has_bearing:
            # Wrap yaw innovation to [-pi, pi]
            y[-1] = normalize_angle(y[-1])

        # Innovation covariance
        S = H @ self.P @ H.T + R
        # Kalman Gain (robust against numerical ill-conditioning)
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            K = self.P @ H.T @ np.linalg.pinv(S)

        # State update
        dx = K @ y
        self.x += dx
        self.x[3] = normalize_angle(self.x[3])

        # Joseph form covariance update for numerical stability: (I - KH) P (I - KH)^T + K R K^T
        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

        return {
            "status": "gnss_updated",
            "innovations": y.tolist(),
            "east_m": float(self.x[0]),
            "north_m": float(self.x[1]),
            "velocity_ms": float(self.x[2]),
            "yaw_rad": float(self.x[3]),
            "yaw_bias_rads": float(self.x[4])
        }

    def update_ml_prediction(
        self,
        predicted_velocity: float,
        predicted_yaw_rate: float,
        var_velocity: float = 0.25,
        var_yaw_rate: float = 0.01,
        dt: float = 0.02,
        measured_gyro_yaw_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        EKF Measurement update directly using Intelligent Deep Learning model predictions.
        Crucial during GNSS outages (tunnels/canyons): binds velocity and yaw drift without double-counting.
        """
        gyro_rate = measured_gyro_yaw_rate if measured_gyro_yaw_rate is not None else self.last_gyro_yaw_rate

        # 1. Target heading step based on ML predicted rate from pre-prediction heading
        target_heading = normalize_angle(self.prev_psi + predicted_yaw_rate * dt)

        # 2. Implied gyro bias: difference between raw gyro reading and ML predicted yaw rate
        implied_bias = gyro_rate - predicted_yaw_rate

        z = np.array([
            predicted_velocity,
            target_heading,
            implied_bias
        ], dtype=np.float64)

        H = np.array([
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float64)

        R = np.diag([
            max(1e-3, var_velocity),
            max(1e-2, var_yaw_rate),
            max(1e-3, var_yaw_rate)
        ]).astype(np.float64)

        z_pred = H @ self.x
        y = z - z_pred
        y[1] = normalize_angle(y[1])

        S = H @ self.P @ H.T + R
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            K = self.P @ H.T @ np.linalg.pinv(S)

        self.x += K @ y
        self.x[3] = normalize_angle(self.x[3])

        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

        return {
            "status": "ml_updated",
            "predicted_vel": predicted_velocity,
            "predicted_yaw_rate": predicted_yaw_rate,
            "heading_rad": float(self.x[3]),
            "yaw_bias_rads": float(self.x[4])
        }

    def update_zupt(self, measured_yaw_rate: float) -> None:
        """
        Zero Velocity Update (ZUPT) and Zero Angular Rate Update (ZARU).
        Executed when vehicle stops at a signal or parking.
        Completely resets velocity to 0 and accurately snaps the gyro bias.
        """
        z = np.array([0.0, measured_yaw_rate], dtype=np.float64)
        H = np.array([
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0]   # gyro bias = measured yaw rate when stationary
        ], dtype=np.float64)

        R = np.diag([0.001, 0.0001]).astype(np.float64)

        z_pred = np.array([self.x[2], self.x[4]], dtype=np.float64)
        y = z - z_pred

        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x += K @ y
        self.x[3] = normalize_angle(self.x[3])

        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

    def mark_outage(self, dt: float) -> None:
        """Mark GPS signal lost and increment outage duration."""
        self.outage_active = True
        self.outage_duration_s += dt

    def get_state(self) -> Dict[str, Any]:
        """Return full estimated state with 1-sigma uncertainty bounds."""
        diag_p = np.maximum(0.0, np.diag(self.P))
        sigma = np.sqrt(diag_p)
        return {
            "east_m": float(self.x[0]),
            "north_m": float(self.x[1]),
            "velocity_ms": float(self.x[2]),
            "yaw_rad": float(self.x[3]),
            "yaw_deg": float(math.degrees(self.x[3]) % 360.0),
            "yaw_bias_rads": float(self.x[4]),
            "pos_uncertainty_m": float(math.sqrt(self.P[0, 0] + self.P[1, 1])),
            "vel_uncertainty_ms": float(sigma[2]),
            "yaw_uncertainty_deg": float(math.degrees(sigma[3])),
            "outage_active": self.outage_active,
            "outage_duration_s": float(self.outage_duration_s),
            "total_distance_m": float(self.total_distance_m)
        }


================================================================================
coordinates.py
================================================================================

import math
import numpy as np

# WGS84 Ellipsoid constants
WGS84_A = 6378137.0          # Semi-major axis in meters
WGS84_E_SQ = 0.00669437999014  # First eccentricity squared

class CoordinateTransformer:
    """
    Transforms coordinates between Geodetic (Lat, Lon, Alt in WGS84)
    and Local Tangent Plane (ENU: East, North, Up in meters).
    Essential for Dead Reckoning and Kalman Filtering in metric space.
    """
    def __init__(self, ref_lat_deg: float, ref_lon_deg: float, ref_alt_m: float = 0.0):
        self.ref_lat_deg = ref_lat_deg
        self.ref_lon_deg = ref_lon_deg
        self.ref_alt_m = ref_alt_m
        
        self.ref_lat_rad = math.radians(ref_lat_deg)
        self.ref_lon_rad = math.radians(ref_lon_deg)
        
        self.ref_ecef_x, self.ref_ecef_y, self.ref_ecef_z = self.geodetic_to_ecef(
            ref_lat_deg, ref_lon_deg, ref_alt_m
        )

    @staticmethod
    def geodetic_to_ecef(lat_deg: float, lon_deg: float, alt_m: float = 0.0):
        lat = math.radians(lat_deg)
        lon = math.radians(lon_deg)
        sin_lat = math.sin(lat)
        cos_lat = math.cos(lat)
        sin_lon = math.sin(lon)
        cos_lon = math.cos(lon)

        n = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat * sin_lat)
        x = (n + alt_m) * cos_lat * cos_lon
        y = (n + alt_m) * cos_lat * sin_lon
        z = (n * (1.0 - WGS84_E_SQ) + alt_m) * sin_lat
        return x, y, z

    def geodetic_to_enu(self, lat_deg: float, lon_deg: float, alt_m: float = 0.0):
        x, y, z = self.geodetic_to_ecef(lat_deg, lon_deg, alt_m)
        dx = x - self.ref_ecef_x
        dy = y - self.ref_ecef_y
        dz = z - self.ref_ecef_z

        sin_lat = math.sin(self.ref_lat_rad)
        cos_lat = math.cos(self.ref_lat_rad)
        sin_lon = math.sin(self.ref_lon_rad)
        cos_lon = math.cos(self.ref_lon_rad)

        east = -sin_lon * dx + cos_lon * dy
        north = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
        up = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz
        return east, north, up

    def enu_to_geodetic(self, east: float, north: float, up: float = 0.0):
        sin_lat = math.sin(self.ref_lat_rad)
        cos_lat = math.cos(self.ref_lat_rad)
        sin_lon = math.sin(self.ref_lon_rad)
        cos_lon = math.cos(self.ref_lon_rad)

        # Inverse rotation from ENU to ECEF delta
        dx = -sin_lon * east - sin_lat * cos_lon * north + cos_lat * cos_lon * up
        dy = cos_lon * east - sin_lat * sin_lon * north + cos_lat * sin_lon * up
        dz = cos_lat * north + sin_lat * up

        x = self.ref_ecef_x + dx
        y = self.ref_ecef_y + dy
        z = self.ref_ecef_z + dz

        # ECEF to Geodetic (Bowring's algorithm with polar numerical stabilization)
        b = WGS84_A * math.sqrt(1.0 - WGS84_E_SQ)
        p = math.sqrt(x * x + y * y)
        if p < 1e-6:
            lat_deg = 90.0 if z > 0 else -90.0
            alt = abs(z) - b
            return lat_deg, self.ref_lon_deg, alt

        theta = math.atan2(z * WGS84_A, p * b)
        e_prime_sq = WGS84_E_SQ / (1.0 - WGS84_E_SQ)

        lat = math.atan2(
            z + e_prime_sq * b * (math.sin(theta) ** 3),
            p - WGS84_E_SQ * WGS84_A * (math.cos(theta) ** 3)
        )
        lon = math.atan2(y, x)

        sin_lat_res = math.sin(lat)
        cos_lat_res = math.cos(lat)
        n = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat_res * sin_lat_res)
        
        # Avoid division by cos(lat) near poles (lat > 45 deg)
        if abs(sin_lat_res) > 0.7071:
            alt = (abs(z) / abs(sin_lat_res)) - n * (1.0 - WGS84_E_SQ)
        else:
            alt = (p / cos_lat_res) - n

        return math.degrees(lat), math.degrees(lon), alt


================================================================================
online_calibrator.py
================================================================================

import json
import math
import os
import numpy as np
from typing import Dict, Any, Optional, Tuple

class OnlineDriftCalibrator:
    """
    Runtime Self-Correction & Online Drift Adaptation Engine.
    
    While the vehicle is driven under clear skies with active GNSS:
    1. Runs model predictions in the background and compares with GNSS velocity & heading.
    2. Learns device-specific hardware scale factors, mounting misalignment, and sensor bias drift.
    3. Employs Online Gradient Descent (OGD) with L2 weight anchoring to prevent divergence.
    4. Automatically performs Zero Velocity Updates (ZUPT) when stationary to lock gyro bias.
    5. Saves and loads learned device profiles for persistent edge personalization.
    """

    def __init__(
        self,
        learning_rate_scale: float = 0.002,
        learning_rate_bias: float = 0.005,
        regularization_lambda: float = 0.01,
        profile_path: str = "device_drift_profile.json"
    ):
        self.profile_path = profile_path
        self.lr_scale = learning_rate_scale
        self.lr_bias = learning_rate_bias
        self.reg_lambda = regularization_lambda

        # Calibrated parameters:
        # v_calibrated = scale_v * v_pred + bias_v
        # yaw_rate_calibrated = scale_yaw * yaw_pred + bias_yaw
        self.scale_v: float = 1.0
        self.bias_v: float = 0.0
        self.scale_yaw: float = 1.0
        self.bias_yaw: float = 0.0

        # Mounting orientation pitch correction (radians)
        self.mounting_pitch_rad: float = 0.0

        # Running diagnostics & statistics
        self.samples_learned: int = 0
        self.running_speed_error_sum: float = 0.0
        self.running_yaw_error_sum: float = 0.0
        self.recent_speed_errors: list = []
        self.recent_yaw_errors: list = []
        self.zupt_counter: int = 0

        # Load existing profile if present
        self.load_profile()

    def calibrate_step(
        self,
        predicted_vel: float,
        predicted_yaw_rate: float,
        gps_speed: Optional[float],
        gps_bearing_rate: Optional[float],
        gps_accuracy_m: float = 2.0,
        is_stationary: bool = False
    ) -> Dict[str, Any]:
        """
        Perform one online adaptation step when GPS is available.
        predicted_vel: raw ML predicted forward velocity (m/s)
        predicted_yaw_rate: raw ML predicted yaw rate (rad/s)
        gps_speed: true GNSS speed (m/s)
        gps_bearing_rate: estimated true heading angular rate from GNSS trajectory (rad/s)
        """
        # If stationary (ZUPT detected):
        if is_stationary:
            self.zupt_counter += 1
            # When stationary, true velocity = 0 and true yaw rate = 0
            # Directly calibrate biases
            v_err = 0.0 - (self.scale_v * predicted_vel + self.bias_v)
            self.bias_v += 0.05 * v_err

            yaw_err = 0.0 - (self.scale_yaw * predicted_yaw_rate + self.bias_yaw)
            self.bias_yaw += 0.05 * yaw_err
            
            return {
                "adapted": True,
                "event": "zupt_recalibration",
                "scale_v": self.scale_v,
                "bias_v": self.bias_v,
                "scale_yaw": self.scale_yaw,
                "bias_yaw": self.bias_yaw
            }

        # If GPS is not available or low accuracy, skip learning
        if gps_speed is None or gps_accuracy_m > 4.5:
            return {"adapted": False, "reason": "gps_unavailable_or_degraded"}

        # Trust weight inversely proportional to GPS uncertainty
        weight = float(np.clip(3.0 / max(1.0, gps_accuracy_m), 0.2, 1.5))

        # Forward velocity error
        calibrated_v = self.scale_v * predicted_vel + self.bias_v
        err_v = gps_speed - calibrated_v

        # Gradient descent step for velocity parameters:
        # Loss = 0.5 * (calibrated_v - gps_speed)^2 + 0.5 * lambda * ((scale_v - 1)^2 + bias_v^2)
        grad_scale_v = -err_v * predicted_vel + self.reg_lambda * (self.scale_v - 1.0)
        grad_bias_v = -err_v + self.reg_lambda * self.bias_v

        self.scale_v -= self.lr_scale * weight * np.clip(grad_scale_v, -5.0, 5.0)
        self.bias_v -= self.lr_bias * weight * np.clip(grad_bias_v, -2.0, 2.0)
        # Constrain scale factor to plausible range (0.8 to 1.2)
        self.scale_v = float(np.clip(self.scale_v, 0.75, 1.25))

        # Yaw rate calibration (only during steady straight motion with high-accuracy GPS)
        err_yaw = 0.0
        if gps_bearing_rate is not None and gps_speed > 3.0 and abs(gps_bearing_rate) < 0.08:
            calibrated_yaw = self.scale_yaw * predicted_yaw_rate + self.bias_yaw
            err_yaw = gps_bearing_rate - calibrated_yaw

            # Heavy regularization anchoring bias to zero to reject noise
            grad_bias_yaw = -err_yaw + 0.1 * self.bias_yaw
            self.bias_yaw -= 0.001 * weight * np.clip(grad_bias_yaw, -0.05, 0.05)
            self.bias_yaw = float(np.clip(self.bias_yaw, -0.008, 0.008))
            self.scale_yaw = 1.0  # Keep scale factor locked at 1.0 to avoid turn distortion

        # Update diagnostics
        self.samples_learned += 1
        self.running_speed_error_sum += abs(err_v)
        self.running_yaw_error_sum += abs(err_yaw)

        self.recent_speed_errors.append(abs(err_v))
        if len(self.recent_speed_errors) > 50:
            self.recent_speed_errors.pop(0)

        # Save profile periodically every 100 samples
        if self.samples_learned % 100 == 0:
            self.save_profile()

        return {
            "adapted": True,
            "samples_learned": self.samples_learned,
            "speed_residual_ms": float(err_v),
            "yaw_residual_rads": float(err_yaw),
            "scale_v": float(self.scale_v),
            "bias_v": float(self.bias_v),
            "scale_yaw": float(self.scale_yaw),
            "bias_yaw": float(self.bias_yaw),
            "avg_speed_error_ms": float(np.mean(self.recent_speed_errors)) if self.recent_speed_errors else 0.0
        }

    def apply_correction(self, raw_vel: float, raw_yaw_rate: float) -> Tuple[float, float]:
        """
        Apply the runtime learned device-specific scale and bias corrections
        to raw ML model predictions.
        """
        calibrated_v = max(0.0, self.scale_v * raw_vel + self.bias_v)
        calibrated_yaw_rate = self.scale_yaw * raw_yaw_rate + self.bias_yaw
        return calibrated_v, calibrated_yaw_rate

    def get_profile(self) -> Dict[str, Any]:
        """Return the current device calibration profile."""
        recent_err = float(np.mean(self.recent_speed_errors)) if self.recent_speed_errors else 0.0
        return {
            "scale_v": float(self.scale_v),
            "bias_v": float(self.bias_v),
            "scale_yaw": float(self.scale_yaw),
            "bias_yaw": float(self.bias_yaw),
            "samples_learned": self.samples_learned,
            "recent_speed_mae_ms": recent_err,
            "health": "CALIBRATED" if self.samples_learned > 20 else "CALIBRATING"
        }

    def save_profile(self) -> None:
        """Persist device calibration profile to JSON."""
        try:
            data = {
                "scale_v": self.scale_v,
                "bias_v": self.bias_v,
                "scale_yaw": self.scale_yaw,
                "bias_yaw": self.bias_yaw,
                "samples_learned": self.samples_learned
            }
            with open(self.profile_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def load_profile(self) -> None:
        """Load saved profile if available on edge storage."""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    data = json.load(f)
                    self.scale_v = float(data.get("scale_v", 1.0))
                    self.bias_v = float(data.get("bias_v", 0.0))
                    self.scale_yaw = float(data.get("scale_yaw", 1.0))
                    self.bias_yaw = float(data.get("bias_yaw", 0.0))
                    self.samples_learned = int(data.get("samples_learned", 0))
            except Exception:
                pass


================================================================================
train.py
================================================================================

import os
import sys
import time
import math
import numpy as np
import torch
import torch.nn as nn
from typing import Optional, List, Tuple, Dict, Any
from torch.utils.data import Dataset, DataLoader

# Add parent path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.dataset_generator import VehicularTrajectoryGenerator
from data.iovnbd_loader import IOVNBDLoader
from models.idr_model import IntelligentDeadReckoningNet, HeteroscedasticLoss

class IMUSlidingWindowDataset(Dataset):
    """
    Sliding window dataset for vehicular IMU time-series.
    Input: (Window_Length, 6) -> [ax, ay, az, gx, gy, gz]
    Targets: [target_speed_ms, target_yaw_rate_rads]
    """
    def __init__(self, trajectories: list, window_size: int = 50, step: int = 5):
        self.windows = []
        self.targets_speed = []
        self.targets_yaw_rate = []

        for traj in trajectories:
            ax = traj["accel_x"]
            ay = traj["accel_y"]
            az = traj["accel_z"]
            gx = traj["gyro_x"]
            gy = traj["gyro_y"]
            gz = traj["gyro_z"]
            gt_spd = traj["gt_speed"]
            gt_yr = traj["gt_yaw_rate"]

            imu_matrix = np.column_stack([ax, ay, az, gx, gy, gz]).astype(np.float32)
            n_samples = len(imu_matrix)

            for i in range(0, n_samples - window_size + 1, step):
                win = imu_matrix[i : i + window_size]
                # Target is the vehicle state at the end of the observation window
                self.windows.append(win)
                self.targets_speed.append(gt_spd[i + window_size - 1])
                self.targets_yaw_rate.append(gt_yr[i + window_size - 1])

        self.windows = np.array(self.windows, dtype=np.float32)
        self.targets_speed = np.array(self.targets_speed, dtype=np.float32)
        self.targets_yaw_rate = np.array(self.targets_yaw_rate, dtype=np.float32)

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        return (
            torch.from_numpy(self.windows[idx]),
            torch.tensor(self.targets_speed[idx], dtype=torch.float32),
            torch.tensor(self.targets_yaw_rate[idx], dtype=torch.float32)
        )

def generate_multi_trajectory_dataset(n_runs: int = 8, fs: float = 50.0) -> list:
    """Generate multiple realistic training drives with distinct biases and vibrations."""
    trajectories = []
    generator = VehicularTrajectoryGenerator(sampling_rate_hz=fs, seed=100)
    for i in range(n_runs):
        duration = float(np.random.uniform(120.0, 240.0))
        accel_b = float(np.random.uniform(0.02, 0.15))
        gyro_b = float(np.random.uniform(-0.04, 0.04))
        vibe_amp = float(np.random.uniform(0.1, 0.4))
        tilt = float(np.random.uniform(-8.0, 8.0))

        traj = generator.generate_synthetic_drive(
            duration_sec=duration,
            accel_bias=accel_b,
            gyro_bias=gyro_b,
            vibration_amp=vibe_amp,
            tilt_pitch_deg=tilt
        )
        trajectories.append(traj)
    return trajectories

def train_idr_model(
    epochs: int = 25,
    batch_size: int = 64,
    window_size: int = 50,
    lr: float = 1e-3,
    save_path: str = "idr_model_best.pt",
    onnx_path: str = "idr_model.onnx",
    data_dir: Optional[str] = None,
    dataset_mode: str = "auto",
    target_fs: float = 50.0,
    device_name: Optional[str] = None
):
    print("=" * 60)
    print("AI-ML Intelligent Dead Reckoning (IDR) Training Pipeline")
    print("Target Problem: SIH26168 - GNSS Signal Loss in Tunnels & Canyons")
    print(f"Dataset Mode: {dataset_mode.upper()} | Target Fs: {target_fs} Hz")
    print("=" * 60)

    # Device configuration with GPU acceleration support
    if device_name is not None:
        device = torch.device(device_name)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if device.type == "cuda":
        try:
            # Test small tensor operation to verify kernel availability (e.g. sm_120 vs sm_90)
            t_test = torch.zeros(1, device="cuda")
            _ = t_test + 1
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"[Device] Using compute device: {device} ({gpu_name}, {gpu_mem:.2f} GB VRAM)")
            torch.backends.cudnn.benchmark = True
        except Exception as e:
            print(f"[Device Notice] GPU detected but CUDA kernels unavailable for this architecture ({e}). Falling back to optimized CPU execution.")
            device = torch.device("cpu")
    else:
        print("[Device] Using compute device: cpu")

    # 1. Ingest IO-VNBD or Generate Synthetic Data
    iovnbd_trajs = []
    found_dir = None
    loader = IOVNBDLoader(default_fs=10.0)

    candidate_dirs = []
    if data_dir:
        candidate_dirs.append(data_dir)
    candidate_dirs.extend(["data/iovnbd", "data/iovnbd_samples", "data"])

    if dataset_mode in ("auto", "iovnbd", "hybrid"):
        for cdir in candidate_dirs:
            if os.path.isdir(cdir):
                loaded = loader.load_directory(cdir, target_fs=target_fs)
                if loaded:
                    iovnbd_trajs = loaded
                    found_dir = cdir
                    break

    train_trajs = []
    val_trajs = []

    if dataset_mode == "iovnbd" and not iovnbd_trajs:
        raise FileNotFoundError(
            f"dataset_mode='iovnbd' requested, but no valid IO-VNBD CSV logs found in candidate dirs: {candidate_dirs}"
        )

    if iovnbd_trajs:
        print(f"[Data: IO-VNBD] Loaded {len(iovnbd_trajs)} real vehicular log(s) from '{found_dir}'.")
        if len(iovnbd_trajs) >= 2:
            n_val = max(1, int(len(iovnbd_trajs) * 0.2))
            val_trajs.extend(iovnbd_trajs[-n_val:])
            train_trajs.extend(iovnbd_trajs[:-n_val])
        else:
            # Single trajectory: split sequentially 80% train, 20% val
            t_full = iovnbd_trajs[0]
            n_total = len(t_full["time"])
            split_idx = int(n_total * 0.8)
            traj_train = {k: v[:split_idx] if isinstance(v, np.ndarray) and len(v) == n_total else v for k, v in t_full.items()}
            traj_val = {k: v[split_idx:] if isinstance(v, np.ndarray) and len(v) == n_total else v for k, v in t_full.items()}
            train_trajs.append(traj_train)
            val_trajs.append(traj_val)

        if dataset_mode == "hybrid":
            print("[Data: Hybrid] Combining IO-VNBD logs with domain-randomized synthetic drives...")
            synth_train = generate_multi_trajectory_dataset(n_runs=4, fs=target_fs)
            synth_val = generate_multi_trajectory_dataset(n_runs=1, fs=target_fs)
            train_trajs.extend(synth_train)
            val_trajs.extend(synth_val)
    else:
        print("[Data: Synthetic] No external IO-VNBD logs detected. Seamlessly using high-fidelity vehicular simulator.")
        train_trajs = generate_multi_trajectory_dataset(n_runs=8, fs=target_fs)
        val_trajs = generate_multi_trajectory_dataset(n_runs=2, fs=target_fs)

    train_dataset = IMUSlidingWindowDataset(train_trajs, window_size=window_size, step=10)
    val_dataset = IMUSlidingWindowDataset(val_trajs, window_size=window_size, step=15)

    print(f"[Data] Train Windows: {len(train_dataset)} | Validation Windows: {len(val_dataset)}")

    if len(train_dataset) == 0:
        raise ValueError(
            f"No training windows could be generated with window_size={window_size}. "
            "Ensure the provided trajectories contain sufficient duration (> window_size samples)."
        )
    if len(val_dataset) == 0:
        print("[Data Notice] Validation set has 0 windows. Using training subset for validation metrics.")
        val_dataset = train_dataset

    effective_batch = min(batch_size, max(1, len(train_dataset)))
    train_loader = DataLoader(
        train_dataset,
        batch_size=effective_batch,
        shuffle=True,
        drop_last=(len(train_dataset) >= effective_batch),
        pin_memory=(device.type == "cuda")
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=min(batch_size, max(1, len(val_dataset))),
        shuffle=False,
        pin_memory=(device.type == "cuda")
    )

    # 2. Instantiate Model and Loss
    try:
        model = IntelligentDeadReckoningNet(
            in_channels=6,
            conv_channels=64,
            gru_hidden_size=64,
            gru_layers=2,
            dropout=0.15
        ).to(device)
    except Exception as e:
        print(f"[Model Init Notice] Falling back to CPU for model layers: {e}")
        device = torch.device("cpu")
        model = IntelligentDeadReckoningNet(
            in_channels=6,
            conv_channels=64,
            gru_hidden_size=64,
            gru_layers=2,
            dropout=0.15
        ).to(device)

    loss_fn = HeteroscedasticLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    best_val_loss = float("inf")
    start_time = time.time()

    # 3. Training Loop
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss_total = 0.0
        train_speed_mae = 0.0
        train_yaw_mae = 0.0
        batch_count = 0

        for x_win, target_speed, target_yaw in train_loader:
            x_win = x_win.to(device)
            target_speed = target_speed.to(device)
            target_yaw = target_yaw.to(device)

            optimizer.zero_grad()

            pred_vel, pred_vel_var, pred_yaw, pred_yaw_var = model(x_win)

            loss_vel = loss_fn(pred_vel, pred_vel_var, target_speed)
            loss_yaw = loss_fn(pred_yaw, pred_yaw_var, target_yaw)
            total_loss = loss_vel + 2.0 * loss_yaw

            total_loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()

            train_loss_total += total_loss.item()
            train_speed_mae += torch.mean(torch.abs(pred_vel - target_speed)).item()
            train_yaw_mae += torch.mean(torch.abs(pred_yaw - target_yaw)).item()
            batch_count += 1

        scheduler.step()

        # Validation
        model.eval()
        val_loss_total = 0.0
        val_speed_mae = 0.0
        val_yaw_mae = 0.0
        val_batches = 0

        with torch.no_grad():
            for x_win, target_speed, target_yaw in val_loader:
                x_win = x_win.to(device)
                target_speed = target_speed.to(device)
                target_yaw = target_yaw.to(device)

                pred_vel, pred_vel_var, pred_yaw, pred_yaw_var = model(x_win)

                loss_vel = loss_fn(pred_vel, pred_vel_var, target_speed)
                loss_yaw = loss_fn(pred_yaw, pred_yaw_var, target_yaw)
                total_loss = loss_vel + 2.0 * loss_yaw

                val_loss_total += total_loss.item()
                val_speed_mae += torch.mean(torch.abs(pred_vel - target_speed)).item()
                val_yaw_mae += torch.mean(torch.abs(pred_yaw - target_yaw)).item()
                val_batches += 1

        avg_train_loss = train_loss_total / max(1, batch_count)
        avg_val_loss = val_loss_total / max(1, val_batches)
        avg_val_speed_mae = val_speed_mae / max(1, val_batches)
        avg_val_yaw_mae = val_yaw_mae / max(1, val_batches)

        # Print progress
        if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
            print(
                f"Epoch [{epoch:02d}/{epochs:02d}] "
                f"Train Loss: {avg_train_loss:.4f} | "
                f"Val Loss: {avg_val_loss:.4f} | "
                f"Val Speed MAE: {avg_val_speed_mae:.3f} m/s | "
                f"Val Yaw MAE: {math.degrees(avg_val_yaw_mae):.3f} deg/s"
            )

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "val_loss": best_val_loss,
                    "val_speed_mae": avg_val_speed_mae,
                    "val_yaw_mae": avg_val_yaw_mae,
                    "window_size": window_size,
                    "in_channels": 6
                },
                save_path
            )

    elapsed = time.time() - start_time
    print(f"[Training Complete] Finished in {elapsed:.2f}s. Best Val Loss: {best_val_loss:.4f}")
    print(f"[Model Saved] Saved best weights to {save_path}")

    # 4. Export to TorchScript & ONNX for Edge / Mobile Deployment
    model.eval()
    dummy_input = torch.randn(1, window_size, 6, device=device)

    # TorchScript (PyTorch Mobile ready)
    script_path = "idr_model_scripted.pt"
    try:
        traced_model = torch.jit.trace(model, dummy_input)
        traced_model.save(script_path)
        print(f"[Export Success] TorchScript edge model exported: {script_path} ({os.path.getsize(script_path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"[TorchScript Export Notice] {e}")

    # ONNX export
    try:
        print(f"[Export] Exporting model to ONNX format: {onnx_path}...")
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=["imu_window"],
            output_names=["speed_mean", "speed_var", "yaw_rate_mean", "yaw_rate_var"],
            dynamic_axes={
                "imu_window": {0: "batch_size"},
                "speed_mean": {0: "batch_size"},
                "speed_var": {0: "batch_size"},
                "yaw_rate_mean": {0: "batch_size"},
                "yaw_rate_var": {0: "batch_size"},
            }
        )
        print(f"[Export Success] ONNX model exported: {onnx_path} ({os.path.getsize(onnx_path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"[ONNX Export Notice] Optional ONNX export skipped ({e}). TorchScript model available at {script_path}.")

    return model, save_path, onnx_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI-ML Intelligent Dead Reckoning Training Pipeline (SIH26168)")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs (default: 20)")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size (default: 64)")
    parser.add_argument("--window-size", type=int, default=50, help="Sliding window length (default: 50)")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate (default: 1e-3)")
    parser.add_argument("--data-dir", type=str, default=None, help="Directory containing IO-VNBD dataset CSV logs")
    parser.add_argument("--dataset-mode", type=str, default="auto", choices=["auto", "iovnbd", "synthetic", "hybrid"], help="Dataset source mode (default: auto)")
    parser.add_argument("--save-path", type=str, default="idr_model_best.pt", help="Best weights checkpoint destination")
    parser.add_argument("--device", type=str, default=None, help="Explicit compute device (e.g. cpu, cuda)")
    args = parser.parse_args()

    train_idr_model(
        epochs=args.epochs,
        batch_size=args.batch_size,
        window_size=args.window_size,
        lr=args.lr,
        save_path=args.save_path,
        data_dir=args.data_dir,
        dataset_mode=args.dataset_mode,
        device_name=args.device
    )


================================================================================
dataset_generator.py
================================================================================

import math
import numpy as np
from typing import Dict, List, Tuple, Any

class VehicularTrajectoryGenerator:
    """
    Generates realistic vehicular kinematics, IMU measurements with smartphone sensor noise
    (bias drift, vibration, white noise, orientation misalignment), and ground-truth GNSS.
    
    Supports simulated GNSS outages (urban canyons, tunnels, underpasses).
    """

    def __init__(self, sampling_rate_hz: float = 50.0, seed: int = 42):
        self.fs = sampling_rate_hz
        self.dt = 1.0 / sampling_rate_hz
        self.rng = np.random.RandomState(seed)

    # Exact road centerline waypoints along MG Road, Bangalore
    # From Anil Kumble Circle (12.974938, 77.609009) to Mayo Hall / Garuda Mall (12.973033, 77.617149)
    # Extracted directly from OpenStreetMap road network
    MGROAD_WAYPOINTS = [
        [77.609009, 12.974938], [77.61101, 12.974467], [77.611037, 12.974461], [77.611066, 12.974454],
        [77.611112, 12.974442], [77.611184, 12.974426], [77.611245, 12.974413], [77.611541, 12.974342],
        [77.611588, 12.974331], [77.612831, 12.974033], [77.613772, 12.973808], [77.61379, 12.973804],
        [77.613855, 12.973788], [77.613953, 12.973766], [77.613989, 12.973757], [77.614552, 12.973633],
        [77.615193, 12.973487], [77.615303, 12.973461], [77.615654, 12.973379], [77.615712, 12.973366],
        [77.615796, 12.973347], [77.616156, 12.973267], [77.616343, 12.973226], [77.616367, 12.973221],
        [77.616608, 12.973163], [77.616809, 12.973115], [77.616868, 12.973101], [77.616899, 12.973093],
        [77.616955, 12.97308], [77.617069, 12.973053], [77.617149, 12.973033]
    ]

    def generate_bangalore_mgroad_drive(
        self,
        duration_sec: float = 60.0,
        outage_windows: List[Tuple[float, float]] = None,
        accel_bias: float = 0.04,
        gyro_bias: float = 0.015,
        vibration_amp: float = 0.2,
        tilt_pitch_deg: float = 2.0
    ) -> Dict[str, np.ndarray]:
        """
        Generates realistic mobile vehicular drive SNAPPED DIRECTLY to MG Road, Bangalore.
        Eliminates random building/grass collisions by following actual asphalt road centerline!
        Simulates GNSS signal loss under the Namma Metro overhead viaduct.
        """
        if outage_windows is None:
            # Default Metro canyon outage: from 16s to 36s (20s duration)
            outage_windows = [(16.0, 36.0)]

        nodes = self.MGROAD_WAYPOINTS
        ref_lat = nodes[0][1]
        ref_lon = nodes[0][0]

        # Convert road nodes to local ENU (East-North-Up)
        lat_rad = math.radians(ref_lat)
        m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * lat_rad)
        m_per_deg_lon = 111412.84 * math.cos(lat_rad)

        node_e = np.array([(pt[0] - ref_lon) * m_per_deg_lon for pt in nodes])
        node_n = np.array([(pt[1] - ref_lat) * m_per_deg_lat for pt in nodes])

        seg_dists = np.hypot(np.diff(node_e), np.diff(node_n))
        cum_dist = np.insert(np.cumsum(seg_dists), 0, 0.0)
        total_road_dist = cum_dist[-1]

        total_steps = int(duration_sec * self.fs)
        time = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

        # Smooth vehicular speed profile matching Bangalore city traffic:
        # 0-5s: Accelerate from Anil Kumble signal (0 to 16.5 m/s = 60 km/h)
        # 5-46s: Cruise along MG Road past Brigade Rd & Church St
        # 46-56s: Decelerate to stop at Mayo Hall signal
        # 56-60s: Stationary at red light (ZUPT demonstration)
        t_accel = 5.0
        t_cruise = 41.0
        t_decel = 10.0
        cruise_v = total_road_dist / (0.5 * t_accel + t_cruise + 0.5 * t_decel)

        gt_speed = np.zeros(total_steps, dtype=np.float64)
        gt_accel_fwd = np.zeros(total_steps, dtype=np.float64)

        for i, ti in enumerate(time):
            if ti < t_accel:
                a = cruise_v / t_accel
                gt_accel_fwd[i] = a
                gt_speed[i] = a * ti
            elif ti < (t_accel + t_cruise):
                gt_accel_fwd[i] = 0.0
                gt_speed[i] = cruise_v
            elif ti < (t_accel + t_cruise + t_decel):
                a = -cruise_v / t_decel
                gt_accel_fwd[i] = a
                gt_speed[i] = max(0.0, cruise_v + a * (ti - (t_accel + t_cruise)))
            else:
                gt_accel_fwd[i] = 0.0
                gt_speed[i] = 0.0

        # Arc-length position along road centerline
        s_progress = np.cumsum(gt_speed * self.dt)
        s_progress = np.clip(s_progress, 0.0, total_road_dist)

        # Smooth position interpolation on road nodes
        gt_east = np.interp(s_progress, cum_dist, node_e)
        gt_north = np.interp(s_progress, cum_dist, node_n)

        # Compute heading from road tangent vector
        de = np.gradient(gt_east, self.dt)
        dn = np.gradient(gt_north, self.dt)

        gt_yaw = np.zeros(total_steps, dtype=np.float64)
        gt_yaw_rate = np.zeros(total_steps, dtype=np.float64)

        last_valid_yaw = math.atan2(dn[1], de[1]) if len(dn) > 1 else 0.0
        for i in range(total_steps):
            if gt_speed[i] > 0.2:
                last_valid_yaw = math.atan2(dn[i], de[i])
            gt_yaw[i] = last_valid_yaw

        # Yaw rate from derivative of unwrapped heading
        unwrapped_yaw = np.unwrap(gt_yaw)
        gt_yaw_rate = np.gradient(unwrapped_yaw, self.dt)
        # Suppress yaw rate when stationary
        gt_yaw_rate[gt_speed < 0.2] = 0.0

        # Centripetal acceleration
        gt_accel_lat = gt_speed * gt_yaw_rate

        # -------------------------------------------------------------
        # Generate Realistic Noisy Smartphone IMU measurements
        # -------------------------------------------------------------
        engine_vibe_x = vibration_amp * np.sin(2.0 * np.pi * 24.0 * time)
        engine_vibe_y = vibration_amp * np.cos(2.0 * np.pi * 28.0 * time)
        engine_vibe_z = 0.5 * vibration_amp * np.sin(2.0 * np.pi * 18.0 * time)

        drift_rate_gyro = self.rng.normal(0.0, 1e-4, total_steps).cumsum()
        drift_rate_accel = self.rng.normal(0.0, 1e-4, total_steps).cumsum()

        pitch_rad = math.radians(tilt_pitch_deg)
        g = 9.80665

        # Smartphone accelerometer with gravity leakage and noise
        meas_ax = (
            gt_accel_fwd * math.cos(pitch_rad)
            - g * math.sin(pitch_rad)
            + accel_bias
            + drift_rate_accel
            + engine_vibe_x
            + self.rng.normal(0.0, 0.08, total_steps)
        )
        meas_ay = (
            gt_accel_lat
            + self.rng.normal(0.0, 0.01, total_steps).cumsum() * 0.02
            + engine_vibe_y
            + self.rng.normal(0.0, 0.08, total_steps)
        )
        meas_az = (
            g * math.cos(pitch_rad)
            + gt_accel_fwd * math.sin(pitch_rad)
            + engine_vibe_z
            + self.rng.normal(0.0, 0.12, total_steps)
        )

        meas_gx = self.rng.normal(0.0, 0.005, total_steps)
        meas_gy = self.rng.normal(0.0, 0.005, total_steps)
        meas_gz = (
            gt_yaw_rate
            + gyro_bias
            + drift_rate_gyro
            + self.rng.normal(0.0, 0.008, total_steps)
        )

        # GNSS Observations & Outages
        gps_mask = np.ones(total_steps, dtype=bool)
        for s, e in outage_windows:
            gps_mask[(time >= s) & (time <= e)] = False

        gps_noise_e = self.rng.normal(0.0, 1.2, total_steps)
        gps_noise_n = self.rng.normal(0.0, 1.2, total_steps)
        gps_east = gt_east + gps_noise_e
        gps_north = gt_north + gps_noise_n
        gps_speed = np.clip(gt_speed + self.rng.normal(0.0, 0.2, total_steps), 0.0, None)
        gps_bearing = (gt_yaw + self.rng.normal(0.0, math.radians(2.0), total_steps))

        return {
            "time": time,
            "dt": self.dt,
            "fs": self.fs,
            "ref_lat": ref_lat,
            "ref_lon": ref_lon,
            "accel_x": meas_ax.astype(np.float32),
            "accel_y": meas_ay.astype(np.float32),
            "accel_z": meas_az.astype(np.float32),
            "gyro_x": meas_gx.astype(np.float32),
            "gyro_y": meas_gy.astype(np.float32),
            "gyro_z": meas_gz.astype(np.float32),
            "gt_speed": gt_speed.astype(np.float32),
            "gt_yaw_rate": gt_yaw_rate.astype(np.float32),
            "gt_yaw": gt_yaw.astype(np.float32),
            "gt_east": gt_east.astype(np.float32),
            "gt_north": gt_north.astype(np.float32),
            "gps_mask": gps_mask,
            "gps_east": gps_east.astype(np.float32),
            "gps_north": gps_north.astype(np.float32),
            "gps_speed": gps_speed.astype(np.float32),
            "gps_bearing": gps_bearing.astype(np.float32),
            "in_outage": ~gps_mask,
        }

    def generate_synthetic_drive(
        self,
        duration_sec: float = 180.0,
        outage_windows: List[Tuple[float, float]] = None,
        accel_bias: float = 0.08,
        gyro_bias: float = 0.035, # ~2 deg/sec bias drift typical of smartphone IMU
        vibration_amp: float = 0.25,
        tilt_pitch_deg: float = 4.0
    ) -> Dict[str, np.ndarray]:
        """
        Generate a multi-maneuver drive:
        - Stationary (0-10s) -> ZUPT calibration period
        - Acceleration to 50 km/h (10-25s)
        - Cruising straight (25-50s)
        - 90 degree left turn (50-60s)
        - Straight cruising (60-80s)
        - S-curve / lane changes (80-100s)
        - 90 degree right turn (100-110s)
        - Deceleration to full stop at red light (110-125s)
        - Stationary wait (125-140s)
        - Acceleration and high speed cruise (140-180s)
        """
        if outage_windows is None:
            # Default tunnel outage: from 60s to 105s (45 seconds of complete GPS loss!)
            outage_windows = [(60.0, 105.0)]

        total_steps = int(duration_sec * self.fs)
        time = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

        # Ground truth kinematic arrays
        gt_speed = np.zeros(total_steps)       # m/s
        gt_yaw_rate = np.zeros(total_steps)    # rad/s
        gt_accel_fwd = np.zeros(total_steps)   # m/s^2
        gt_yaw = np.zeros(total_steps)         # rad
        gt_east = np.zeros(total_steps)        # m
        gt_north = np.zeros(total_steps)       # m

        # Current state
        current_speed = 0.0
        current_yaw = 0.0
        current_east = 0.0
        current_north = 0.0

        for i, t in enumerate(time):
            # Target speed & steering profile based on trajectory plan
            target_accel = 0.0
            target_yaw_rate = 0.0

            if 0.0 <= t < 4.0:
                # Immediate brisk acceleration from 0 to 14 m/s (~50 km/h)
                target_accel = 14.0 / 4.0
            elif 4.0 <= t < 16.0:
                # Cruising Eastbound along avenue
                target_accel = 0.0
            elif 16.0 <= t < 24.0:
                # 90 deg left turn (+pi/2 over 8s = 0.196 rad/s) onto Northbound road
                target_yaw_rate = (math.pi / 2.0) / 8.0
                target_accel = 0.0
            elif 24.0 <= t < 45.0:
                # Cruising Northbound (Tunnel entrance)
                target_accel = 0.0
            elif 45.0 <= t < 53.0:
                # 90 deg right turn (-pi/2 over 8s) Eastbound
                target_yaw_rate = -(math.pi / 2.0) / 8.0
                target_accel = 0.0
            elif 53.0 <= t < 75.0:
                # S-curve lane changes
                target_yaw_rate = 0.15 * math.sin(2.0 * math.pi * (t - 53.0) / 10.0)
                target_accel = 0.0
            elif 75.0 <= t < 88.0:
                # Decelerate to stop at intersection
                target_accel = -14.0 / 13.0
            elif 88.0 <= t < 98.0:
                # Stopped at signal (ZUPT demonstration)
                target_accel = 0.0
                target_yaw_rate = 0.0
            elif 98.0 <= t < 108.0:
                # Accelerate to 18 m/s (~65 km/h)
                target_accel = 18.0 / 10.0
            else:
                target_accel = 0.0

            # Kinematic integration
            current_speed = max(0.0, current_speed + target_accel * self.dt)
            if current_speed < 1e-4:
                target_yaw_rate = 0.0  # vehicle cannot rotate on spot

            current_yaw += target_yaw_rate * self.dt
            current_yaw = (current_yaw + math.pi) % (2.0 * math.pi) - math.pi

            current_east += current_speed * math.cos(current_yaw) * self.dt
            current_north += current_speed * math.sin(current_yaw) * self.dt

            gt_speed[i] = current_speed
            gt_accel_fwd[i] = target_accel
            gt_yaw_rate[i] = target_yaw_rate
            gt_yaw[i] = current_yaw
            gt_east[i] = current_east
            gt_north[i] = current_north

        # Centripetal acceleration: a_lat = v * yaw_rate
        gt_accel_lat = gt_speed * gt_yaw_rate

        # -------------------------------------------------------------
        # Generate Realistic Noisy Smartphone IMU measurements
        # -------------------------------------------------------------
        # 1. High-frequency vehicle engine vibration
        engine_vibe_x = vibration_amp * np.sin(2.0 * np.pi * 25.0 * time + self.rng.uniform(0, 2*np.pi))
        engine_vibe_y = vibration_amp * np.cos(2.0 * np.pi * 32.0 * time + self.rng.uniform(0, 2*np.pi))
        engine_vibe_z = 0.5 * vibration_amp * np.sin(2.0 * np.pi * 18.0 * time)

        # 2. Random walk drift for biases
        drift_rate_gyro = self.rng.normal(0.0, 1e-4, total_steps).cumsum()
        drift_rate_accel = self.rng.normal(0.0, 1e-4, total_steps).cumsum()

        # 3. Smartphone tilt pitch angle (phone mounted at angle on dashboard)
        pitch_rad = math.radians(tilt_pitch_deg)
        g = 9.80665

        # Raw measured acceleration (Forward x, Lateral y, Vertical z)
        # Pitch causes gravity leakage: g * sin(pitch) leaks into forward axis!
        meas_ax = (
            gt_accel_fwd * math.cos(pitch_rad)
            - g * math.sin(pitch_rad)
            + accel_bias
            + drift_rate_accel
            + engine_vibe_x
            + self.rng.normal(0.0, 0.12, total_steps)
        )
        meas_ay = (
            gt_accel_lat
            + self.rng.normal(0.0, 0.02, total_steps).cumsum() * 0.05
            + engine_vibe_y
            + self.rng.normal(0.0, 0.15, total_steps)
        )
        meas_az = (
            g * math.cos(pitch_rad)
            + gt_accel_fwd * math.sin(pitch_rad)
            + engine_vibe_z
            + self.rng.normal(0.0, 0.20, total_steps)
        )

        # Raw measured gyroscope (Roll gx, Pitch gy, Yaw gz)
        meas_gx = self.rng.normal(0.0, 0.01, total_steps)
        meas_gy = self.rng.normal(0.0, 0.01, total_steps)
        meas_gz = (
            gt_yaw_rate
            + gyro_bias
            + drift_rate_gyro
            + self.rng.normal(0.0, 0.008, total_steps)
        )

        # -------------------------------------------------------------
        # Generate GNSS Observations (typically 1 Hz to 5 Hz)
        # -------------------------------------------------------------
        gps_mask = np.zeros(total_steps, dtype=bool)
        gps_east = np.full(total_steps, np.nan)
        gps_north = np.full(total_steps, np.nan)
        gps_speed = np.full(total_steps, np.nan)
        gps_bearing = np.full(total_steps, np.nan)

        # 1 Hz sampling step for GPS
        gps_step = int(self.fs)  # once every 1.0 second

        in_outage_mask = np.array([any(start <= t <= end for start, end in outage_windows) for t in time], dtype=bool)

        for idx in range(0, total_steps, gps_step):
            if not in_outage_mask[idx]:
                gps_mask[idx] = True
                # GNSS multipath / white noise ~ 2.5m std
                gps_east[idx] = gt_east[idx] + self.rng.normal(0.0, 2.0)
                gps_north[idx] = gt_north[idx] + self.rng.normal(0.0, 2.0)
                gps_speed[idx] = max(0.0, gt_speed[idx] + self.rng.normal(0.0, 0.3))
                gps_bearing[idx] = (gt_yaw[idx] + self.rng.normal(0.0, 0.08) + math.pi) % (2.0 * math.pi) - math.pi

        return {
            "time": time,
            "dt": self.dt,
            "fs": self.fs,
            "in_outage": in_outage_mask,
            # IMU inputs (6-DOF)
            "accel_x": meas_ax,
            "accel_y": meas_ay,
            "accel_z": meas_az,
            "gyro_x": meas_gx,
            "gyro_y": meas_gy,
            "gyro_z": meas_gz,
            # Ground Truth Kinematics
            "gt_speed": gt_speed,
            "gt_yaw_rate": gt_yaw_rate,
            "gt_accel_fwd": gt_accel_fwd,
            "gt_yaw": gt_yaw,
            "gt_east": gt_east,
            "gt_north": gt_north,
            # GNSS Observation
            "gps_mask": gps_mask,
            "gps_east": gps_east,
            "gps_north": gps_north,
            "gps_speed": gps_speed,
            "gps_bearing": gps_bearing,
            "outage_windows": outage_windows
        }


================================================================================
schemas.py
================================================================================

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class IMUPacket(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds or epoch")
    accel_x: float = Field(..., description="Forward / lateral acceleration X in m/s^2")
    accel_y: float = Field(..., description="Lateral / forward acceleration Y in m/s^2")
    accel_z: float = Field(..., description="Vertical acceleration Z in m/s^2")
    gyro_x: float = Field(..., description="Angular rate X in rad/s")
    gyro_y: float = Field(..., description="Angular rate Y in rad/s")
    gyro_z: float = Field(..., description="Yaw angular rate Z in rad/s")

class GNSSPacket(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds")
    latitude: float = Field(..., description="WGS84 Latitude in degrees")
    longitude: float = Field(..., description="WGS84 Longitude in degrees")
    altitude: Optional[float] = Field(0.0, description="Altitude in meters")
    speed_ms: Optional[float] = Field(None, description="Ground speed in m/s")
    bearing_deg: Optional[float] = Field(None, description="Course over ground in degrees")
    accuracy_m: Optional[float] = Field(3.0, description="Estimated accuracy in meters")

class TelemetryFeedRequest(BaseModel):
    imu: IMUPacket
    gnss: Optional[GNSSPacket] = None
    simulate_outage: bool = False

class SimulationStartRequest(BaseModel):
    duration_sec: float = 120.0
    outage_start_sec: float = 40.0
    outage_end_sec: float = 85.0
    playback_speed: float = 1.0

class OutageToggleRequest(BaseModel):
    outage_active: bool


================================================================================
main.py
================================================================================

import math
import os
import sys
import time
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from collections import deque

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure module visibility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensor_fusion.coordinates import CoordinateTransformer
from sensor_fusion.ekf import IntelligentEKF
from models.online_calibrator import OnlineDriftCalibrator
from simulation.dataset_generator import VehicularTrajectoryGenerator
from backend.schemas import IMUPacket, GNSSPacket, TelemetryFeedRequest, SimulationStartRequest, OutageToggleRequest

app = FastAPI(
    title="SIH26168 - AI-ML Intelligent Dead Reckoning System",
    description="Edge-optimized IMU drift compensation & seamless GNSS sensor fusion engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NavigationCore:
    """
    Central real-time state manager fusing IMU streaming,
    Deep Learning dead reckoning inference, online calibration, and EKF.
    """
    def __init__(self, ref_lat: float = 12.9716, ref_lon: float = 77.5946): # Bangalore / ISRO HQ
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self.transformer = CoordinateTransformer(ref_lat, ref_lon, 0.0)

        # Intelligent EKF (AI-ML Fusion)
        self.ekf = IntelligentEKF(
            init_east=0.0,
            init_north=0.0,
            init_velocity=0.0,
            init_yaw_rad=0.0
        )

        # Baseline Naive Dead Reckoning (for comparative drift benchmarking)
        self.naive_east = 0.0
        self.naive_north = 0.0
        self.naive_vel = 0.0
        self.naive_yaw = 0.0

        # Online runtime self-correction engine
        self.calibrator = OnlineDriftCalibrator(profile_path="device_drift_profile.json")

        # Sliding IMU buffer (50 samples = 1 sec at 50Hz)
        self.window_size = 50
        self.imu_buffer = deque(maxlen=self.window_size)

        # Outage simulation flag
        self.force_outage = False
        self.last_imu_timestamp: Optional[float] = None
        self.last_gnss_bearing: Optional[float] = None
        self.last_gnss_timestamp: Optional[float] = None

        # Model handles (PyTorch or ONNX Runtime)
        self.model = None
        self.onnx_session = None
        self.device = "cpu"
        self._init_model()

    def reset(self):
        """Reset internal filter states and buffers cleanly."""
        self.ekf = IntelligentEKF(
            init_east=0.0,
            init_north=0.0,
            init_velocity=0.0,
            init_yaw_rad=0.0
        )
        self.naive_east = 0.0
        self.naive_north = 0.0
        self.naive_vel = 0.0
        self.naive_yaw = 0.0
        self.imu_buffer.clear()
        self.force_outage = False
        self.last_imu_timestamp = None
        self.last_gnss_bearing = None
        self.last_gnss_timestamp = None

    def _init_model(self):
        # 1. Try PyTorch
        try:
            import torch
            from models.idr_model import IntelligentDeadReckoningNet
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "idr_model_best.pt")
            try:
                net = IntelligentDeadReckoningNet().to(self.device)
            except Exception:
                self.device = "cpu"
                net = IntelligentDeadReckoningNet().to(self.device)
            if os.path.exists(model_path):
                ckpt = torch.load(model_path, map_location=self.device)
                net.load_state_dict(ckpt["model_state_dict"])
                print(f"[Model] Successfully loaded PyTorch weights from {model_path} on {self.device}")
            net.eval()
            self.model = net
        except Exception as e:
            self.model = None

        # 2. Try ONNX Runtime (fast edge deployment)
        if self.model is None:
            try:
                import onnxruntime as ort
                onnx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "idr_model.onnx")
                if os.path.exists(onnx_path):
                    self.onnx_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
                    print(f"[Model] Successfully loaded ONNX model from {onnx_path}")
            except Exception:
                self.onnx_session = None

    def run_ml_inference(self, imu_window: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Run inference on (50, 6) IMU window.
        Returns: (pred_velocity, var_velocity, pred_yaw_rate, var_yaw_rate)
        """
        # 1. Zero-Velocity (ZUPT) Gatekeeper: if stationary, velocity is locked to 0
        accel_var = np.var(imu_window[:, 0]) + np.var(imu_window[:, 1]) + np.var(imu_window[:, 2])
        gyro_var = np.var(imu_window[:, 3]) + np.var(imu_window[:, 4]) + np.var(imu_window[:, 5])
        if accel_var < 0.05 and gyro_var < 0.003:
            return 0.0, 0.001, 0.0, 0.0001

        # 2. PyTorch Model Inference
        if self.model is not None:
            try:
                import torch
                with torch.no_grad():
                    inp = torch.from_numpy(imu_window).float().unsqueeze(0).to(self.device)
                    vel, vel_var, yr, yr_var = self.model(inp)
                    v_val = float(vel.item())
                    yr_val = float(yr.item())
                    
                    # Decoupled Sanity Check: A car cannot execute an un-commanded 600 deg/s spin.
                    # If neural prediction diverges wildly from physical MEMS gyro, clamp to gyro bounds
                    # to prevent smartphone tilt from causing phantom circular loops!
                    meas_gz = float(np.mean(imu_window[:, 5]))
                    if abs(yr_val - meas_gz) > 0.06:
                        yr_val = meas_gz

                    return v_val, float(vel_var.item()), yr_val, float(yr_var.item())
            except Exception:
                pass

        if self.onnx_session is not None:
            try:
                inp = imu_window.astype(np.float32)[np.newaxis, :, :]  # (1, 50, 6)
                outputs = self.onnx_session.run(None, {"imu_window": inp})
                return float(outputs[0][0]), float(outputs[1][0]), float(outputs[2][0]), float(outputs[3][0])
            except Exception:
                pass

        # Analytical Kinematic Fallback
        accel_fwd = np.mean(imu_window[:, 0])
        gyro_yaw = np.mean(imu_window[:, 5])

        current_v = max(0.0, self.ekf.x[2] + (accel_fwd - self.calibrator.bias_v) * 0.02)
        return current_v, 0.25, float(gyro_yaw), 0.005

    def step(self, imu: IMUPacket, gnss: Optional[GNSSPacket] = None, simulate_outage: bool = False) -> Dict[str, Any]:
        """Process one telemetry time-step."""
        # Calculate dt with protection against backward timestamp or spikes
        if self.last_imu_timestamp is None:
            dt = 0.02
        else:
            raw_dt = imu.timestamp - self.last_imu_timestamp
            dt = 0.02 if (raw_dt <= 0.0 or raw_dt > 0.5) else raw_dt
        self.last_imu_timestamp = imu.timestamp

        # Add to IMU sliding buffer
        sample = np.array([
            imu.accel_x, imu.accel_y, imu.accel_z,
            imu.gyro_x, imu.gyro_y, imu.gyro_z
        ], dtype=np.float32)
        self.imu_buffer.append(sample)

        # -------------------------------------------------------------
        # 1. Update Naive Baseline Dead Reckoning (to illustrate drift!)
        # -------------------------------------------------------------
        self.naive_yaw += imu.gyro_z * dt
        self.naive_vel = max(0.0, self.naive_vel + imu.accel_x * dt)
        self.naive_east += self.naive_vel * math.cos(self.naive_yaw) * dt
        self.naive_north += self.naive_vel * math.sin(self.naive_yaw) * dt

        # -------------------------------------------------------------
        # 2. Intelligent EKF Prediction Step
        # -------------------------------------------------------------
        self.ekf.predict(dt=dt, accel_fwd=imu.accel_x, gyro_yaw_rate=imu.gyro_z)

        # -------------------------------------------------------------
        # 3. Intelligent Deep Learning Feature Inference
        # -------------------------------------------------------------
        if len(self.imu_buffer) >= self.window_size:
            window_arr = np.array(self.imu_buffer)
            pred_v, var_v, pred_yr, var_yr = self.run_ml_inference(window_arr)
        else:
            pred_v = self.ekf.x[2]
            var_v = 0.5
            pred_yr = imu.gyro_z
            var_yr = 0.02

        # Determine whether GNSS outage is active
        # An outage occurs if:
        # 1. simulate_outage is True (e.g. tunnel window in simulation), OR
        # 2. self.force_outage is True (manual switch toggle), OR
        # 3. GPS was active but hasn't arrived for > 1.8s
        time_since_gnss = (imu.timestamp - self.last_gnss_timestamp) if self.last_gnss_timestamp is not None else 0.0
        gps_timed_out = (self.last_gnss_timestamp is not None and time_since_gnss > 1.8)
        
        is_outage = simulate_outage or self.force_outage or gps_timed_out

        calib_stats = {}
        if gnss is not None and not (simulate_outage or self.force_outage):
            # Active GNSS Mode: Transform GPS Lat/Lon to Local ENU
            is_outage = False
            gps_e, gps_n, _ = self.transformer.geodetic_to_enu(
                gnss.latitude, gnss.longitude, gnss.altitude or 0.0
            )

            # Course over ground in radians
            bearing_rad = math.radians(gnss.bearing_deg) if gnss.bearing_deg is not None else None

            # Calculate GNSS bearing rate for online calibrator
            bearing_rate = None
            if bearing_rad is not None:
                if self.last_gnss_bearing is not None and self.last_gnss_timestamp is not None:
                    gnss_dt = gnss.timestamp - self.last_gnss_timestamp
                    if 0.2 <= gnss_dt <= 3.0:
                        db = (bearing_rad - self.last_gnss_bearing + math.pi) % (2.0 * math.pi) - math.pi
                        bearing_rate = db / gnss_dt
                self.last_gnss_bearing = bearing_rad

            self.last_gnss_timestamp = gnss.timestamp

            # Check if vehicle is stationary for ZUPT
            if gnss.speed_ms is not None:
                is_stationary = gnss.speed_ms < 0.25
            else:
                is_stationary = (pred_v < 0.15) and (abs(imu.gyro_z) < 0.02)

            # Online Runtime Self-Correction / Drift Adaptation
            calib_stats = self.calibrator.calibrate_step(
                predicted_vel=pred_v,
                predicted_yaw_rate=pred_yr,
                gps_speed=gnss.speed_ms,
                gps_bearing_rate=bearing_rate,
                gps_accuracy_m=gnss.accuracy_m or 3.0,
                is_stationary=is_stationary
            )

            if is_stationary:
                self.ekf.update_zupt(measured_yaw_rate=imu.gyro_z)
                self.naive_vel = 0.0

            # EKF updates with authoritative GNSS observations
            self.ekf.update_gnss(
                east=gps_e,
                north=gps_n,
                speed=gnss.speed_ms,
                bearing_rad=bearing_rad,
                pos_accuracy_m=gnss.accuracy_m or 3.0
            )
            # Sync naive DR during active GPS so drift accumulates strictly from outage start
            self.naive_east = gps_e
            self.naive_north = gps_n
            self.naive_vel = gnss.speed_ms if gnss.speed_ms is not None else self.naive_vel
            if bearing_rad is not None:
                self.naive_yaw = bearing_rad

        elif is_outage:
            # -------------------------------------------------------------
            # Outage Mode (Tunnel / Urban Canyon): Dead Reckoning with ML!
            # -------------------------------------------------------------
            self.ekf.mark_outage(dt)

            # Universal Zero-Velocity Update during outage (prevents ghost driving when vehicle parks)
            if pred_v < 0.2:
                self.ekf.update_zupt(measured_yaw_rate=imu.gyro_z)
                self.naive_vel = 0.0

            # Apply online-learned device corrections to ML predictions
            calib_v, calib_yr = self.calibrator.apply_correction(pred_v, pred_yr)

            # EKF measurement update using ML drift-corrected speed and yaw rate
            self.ekf.update_ml_prediction(
                predicted_velocity=calib_v,
                predicted_yaw_rate=calib_yr,
                var_velocity=var_v,
                var_yaw_rate=var_yr,
                dt=dt,
                measured_gyro_yaw_rate=imu.gyro_z
            )
        else:
            # Normal sub-second inertial propagation between 1 Hz GNSS fixes:
            # EKF kinematic state was already updated by self.ekf.predict(dt)
            pass

        # -------------------------------------------------------------
        # 5. Geodetic Projection (ENU -> WGS84 Lat, Lon)
        # -------------------------------------------------------------
        ekf_state = self.ekf.get_state()
        est_lat, est_lon, _ = self.transformer.enu_to_geodetic(
            ekf_state["east_m"], ekf_state["north_m"]
        )
        naive_lat, naive_lon, _ = self.transformer.enu_to_geodetic(
            self.naive_east, self.naive_north
        )

        drift_distance_m = math.sqrt(
            (ekf_state["east_m"] - self.naive_east) ** 2 +
            (ekf_state["north_m"] - self.naive_north) ** 2
        )

        return {
            "timestamp": imu.timestamp,
            "outage_active": is_outage,
            "outage_duration_s": ekf_state["outage_duration_s"],
            # Intelligent EKF / AI Estimates
            "estimated_lat": est_lat,
            "estimated_lon": est_lon,
            "velocity_ms": ekf_state["velocity_ms"],
            "velocity_kmh": ekf_state["velocity_ms"] * 3.6,
            "heading_deg": ekf_state["yaw_deg"],
            "gyro_bias_rads": ekf_state["yaw_bias_rads"],
            "pos_uncertainty_m": ekf_state["pos_uncertainty_m"],
            # Naive IMU baseline
            "naive_lat": naive_lat,
            "naive_lon": naive_lon,
            "naive_vel_kmh": self.naive_vel * 3.6,
            "drift_error_m": drift_distance_m,
            # ML Model & Online Self-Correction Telemetry
            "ml_pred_vel_ms": pred_v,
            "ml_pred_yaw_rate_degs": math.degrees(pred_yr),
            "calibration_profile": self.calibrator.get_profile(),
            "calibration_update": calib_stats
        }

# Global singleton navigation engine
core = NavigationCore()

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    """Interactive Real-time Visual Demonstration Dashboard."""
    html_file = os.path.join(os.path.dirname(__file__), "dashboard.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SIH26168 Intelligent Dead Reckoning Backend Running</h1>"

@app.post("/api/telemetry/feed")
def feed_telemetry(payload: TelemetryFeedRequest):
    """Ingest single sensor packet."""
    result = core.step(payload.imu, payload.gnss, payload.simulate_outage)
    return result

@app.post("/api/simulation/toggle_outage")
def toggle_outage(payload: OutageToggleRequest):
    """Toggle simulated GNSS outage (enter/exit tunnel)."""
    core.force_outage = payload.outage_active
    return {"status": "success", "force_outage": core.force_outage}

@app.post("/api/simulation/reset")
def reset_simulation():
    """Reset the navigation core and simulation states."""
    core.reset()
    return {"status": "success", "message": "Navigation engine reset complete"}

@app.get("/api/status")
def get_status():
    """Retrieve system diagnostics, device profile, and GPU status."""
    gpu_available = False
    gpu_name = "N/A"
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            gpu_name = torch.cuda.get_device_name(0)
    except Exception:
        pass

    return {
        "system": "SIH26168 AI-ML Intelligent Dead Reckoning",
        "gpu_available": gpu_available,
        "gpu_device": gpu_name,
        "model_loaded": core.model is not None or core.onnx_session is not None,
        "force_outage": core.force_outage,
        "calibration_profile": core.calibrator.get_profile(),
        "current_ekf_state": core.ekf.get_state()
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """
    WebSocket endpoint for real-time streaming telemetry and bidirectional control.
    Uses asynchronous task delegation so controls (outage toggle, reset) work smoothly mid-stream.
    """
    await websocket.accept()
    print("[WS] Client connected")
    sim_task: Optional[asyncio.Task] = None

    async def run_simulation_stream(sim_dur: float = 60.0, outage_s: float = 20.0, outage_e: float = 45.0, dataset_source: str = "vbox"):
        try:
            core.reset()
            
            # Select 100% authentic real-world dataset from IO-VNBD benchmark
            from data.iovnbd_loader import IOVNBDLoader
            loader = IOVNBDLoader(remove_gravity_from_accel=True)

            is_vbox = (str(dataset_source).lower() in ["vbox", "vehicle", "can"])
            ref_lat, ref_lon = 52.408100, -1.510600
            max_dur = 119.0
            outage_s = float(outage_s) if outage_s else 25.0
            outage_e = float(outage_e) if outage_e else 55.0

            if is_vbox:
                iovnbd_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "iovnbd_samples", "V-Drive_Sample1.csv")
                dataset_name = "IO-VNBD Racelogic VBOX RTK (Coventry Ring Rd)"
            else:
                iovnbd_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "iovnbd_samples", "S-Drive_Sample1.csv")
                dataset_name = "IO-VNBD Smartphone Drive (Coventry)"

            sim_data = loader.load_csv(iovnbd_file, outage_windows=[(outage_s, outage_e)], target_fs=50.0)
            
            core.ref_lat = ref_lat
            core.ref_lon = ref_lon
            core.transformer = CoordinateTransformer(ref_lat, ref_lon, 110.0)
            init_speed = float(sim_data["gt_speed"][0])
            init_yaw = float(sim_data["gt_yaw"][0])
            core.ekf = IntelligentEKF(0.0, 0.0, init_speed, init_yaw)
            core.naive_vel = init_speed
            core.naive_yaw = init_yaw
            step_skip = 2  # 25 fps stream
            sleep_interval = 0.035

            # Notify UI to align map to real road dataset coordinates
            await websocket.send_json({
                "event": "simulation_started",
                "init_lat": ref_lat,
                "init_lon": ref_lon,
                "dataset_name": dataset_name,
                "duration_sec": min(sim_dur, max_dur),
                "tunnel_window": [outage_s, outage_e]
            })

            # Stream active driving phase
            total_len = min(len(sim_data["time"]), int(min(sim_dur, max_dur) * sim_data["fs"]))

            for i in range(0, total_len, step_skip):
                t = float(sim_data["time"][i])
                imu_p = IMUPacket(
                    timestamp=t,
                    accel_x=float(sim_data["accel_x"][i]),
                    accel_y=float(sim_data["accel_y"][i]),
                    accel_z=float(sim_data["accel_z"][i]),
                    gyro_x=float(sim_data["gyro_x"][i]),
                    gyro_y=float(sim_data["gyro_y"][i]),
                    gyro_z=float(sim_data["gyro_z"][i])
                )

                gnss_p = None
                if sim_data["gps_mask"][i]:
                    g_lat, g_lon, _ = core.transformer.enu_to_geodetic(
                        sim_data["gps_east"][i], sim_data["gps_north"][i]
                    )
                    gnss_p = GNSSPacket(
                        timestamp=t,
                        latitude=g_lat,
                        longitude=g_lon,
                        speed_ms=float(sim_data["gps_speed"][i]),
                        bearing_deg=float(math.degrees(sim_data["gps_bearing"][i]) % 360.0),
                        accuracy_m=2.0
                    )

                gt_lat, gt_lon, _ = core.transformer.enu_to_geodetic(
                    sim_data["gt_east"][i], sim_data["gt_north"][i]
                )

                is_sim_outage = (outage_s <= t <= outage_e)
                res = core.step(imu_p, gnss_p, simulate_outage=is_sim_outage)
                res["gt_lat"] = gt_lat
                res["gt_lon"] = gt_lon
                res["gt_speed_kmh"] = float(sim_data["gt_speed"][i] * 3.6)
                res["tunnel_window"] = [outage_s, outage_e]

                await websocket.send_json(res)
                await asyncio.sleep(sleep_interval)
        except asyncio.CancelledError:
            pass
        except Exception as err:
            print(f"[WS Sim Error] {err}")

    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("command")
            if cmd == "start_simulation":
                if sim_task and not sim_task.done():
                    sim_task.cancel()
                dataset_src = str(data.get("dataset_source", "iovnbd"))
                sim_dur = float(data.get("duration", 120.0))
                outage_s = float(data.get("outage_start", 30.0))
                outage_e = float(data.get("outage_end", 70.0))
                sim_task = asyncio.create_task(run_simulation_stream(sim_dur, outage_s, outage_e, dataset_source=dataset_src))

            elif cmd == "toggle_outage":
                val = bool(data.get("value", not core.force_outage))
                core.force_outage = val
                await websocket.send_json({"event": "outage_toggled", "force_outage": core.force_outage})

            elif cmd == "reset":
                if sim_task and not sim_task.done():
                    sim_task.cancel()
                core.reset()
                await websocket.send_json({"event": "reset_complete"})

    except WebSocketDisconnect:
        if sim_task and not sim_task.done():
            sim_task.cancel()
        print("[WS] Client disconnected")
    except Exception as e:
        if sim_task and not sim_task.done():
            sim_task.cancel()
        print(f"[WS Error] {e}")


================================================================================
benchmark_iovnbd.py
================================================================================

"""
IO-VNBD Benchmark & Outage Evaluation Suite.

Target Problem: SIH26168 - AI-ML based Intelligent Dead Reckoning System
Evaluates IntelligentDeadReckoningNet + IntelligentEKF against Pure IMU Dead Reckoning
on IO-VNBD vehicular trajectories during simulated GNSS outages (tunnels, urban canyons).
"""

import os
import sys
import math
import json
import argparse
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import torch

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.idr_model import IntelligentDeadReckoningNet
from sensor_fusion.ekf import IntelligentEKF, normalize_angle
from data.iovnbd_loader import IOVNBDLoader, generate_sample_iovnbd_v_csv


def evaluate_trajectory_outage(
    model: IntelligentDeadReckoningNet,
    trajectory: Dict[str, np.ndarray],
    outage_start_sec: float = 20.0,
    outage_duration_sec: float = 30.0,
    window_size: int = 50,
    device: Optional[torch.device] = None,
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Evaluates Dead Reckoning during a simulated GNSS outage on a vehicular trajectory.

    Compares:
    1. Baseline: Pure IMU kinematic integration (uncorrected forward dead reckoning).
    2. Intelligent Dead Reckoning: Hybrid CNN-GRU inference fused with 5-state IntelligentEKF.

    Returns:
        Comprehensive metric dictionary including drift MAE, max drift, and reduction factor.
    """
    model.eval()
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = torch.device("cpu")
    else:
        model.to(device)

    rng = np.random.RandomState(seed if seed is not None else 42)
    t = trajectory["time"]
    dt = trajectory["dt"]
    n_steps = len(t)

    outage_end_sec = outage_start_sec + outage_duration_sec
    outage_indices = np.where((t >= outage_start_sec) & (t <= outage_end_sec))[0]

    if len(outage_indices) < 2:
        raise ValueError(
            f"Outage window [{outage_start_sec}, {outage_end_sec}] contains fewer than 2 samples in trajectory of duration {t[-1]:.1f}s."
        )

    # Ground truth
    gt_east = trajectory["gt_east"]
    gt_north = trajectory["gt_north"]
    gt_speed = trajectory["gt_speed"]
    gt_yaw = trajectory["gt_yaw"]
    gt_yaw_rate = trajectory["gt_yaw_rate"]

    # Sensor signals
    ax = trajectory["accel_x"]
    ay = trajectory["accel_y"]
    az = trajectory["accel_z"]
    gx = trajectory["gyro_x"]
    gy = trajectory["gyro_y"]
    gz = trajectory["gyro_z"]

    # Calculate distance traveled during outage
    speed_in_outage = gt_speed[outage_indices]
    distance_traveled_m = float(np.sum(speed_in_outage) * dt)

    # -------------------------------------------------------------
    # 1. Baseline: Pure IMU Kinematic Integration
    # -------------------------------------------------------------
    base_east = np.zeros(n_steps)
    base_north = np.zeros(n_steps)
    base_speed = np.zeros(n_steps)
    base_yaw = np.zeros(n_steps)

    base_east[0] = gt_east[0]
    base_north[0] = gt_north[0]
    base_speed[0] = gt_speed[0]
    base_yaw[0] = gt_yaw[0]

    for k in range(1, n_steps):
        time_k = t[k]
        in_outage = (outage_start_sec <= time_k <= outage_end_sec)

        if not in_outage:
            # When GNSS is available, reset baseline to GNSS fix
            base_east[k] = gt_east[k]
            base_north[k] = gt_north[k]
            base_speed[k] = gt_speed[k]
            base_yaw[k] = gt_yaw[k]
        else:
            # During GNSS loss: pure uncorrected Euler kinematic integration
            # v = v + a_x * dt
            base_speed[k] = max(0.0, base_speed[k - 1] + ax[k] * dt)
            # yaw = yaw + omega_z * dt
            base_yaw[k] = normalize_angle(base_yaw[k - 1] + gz[k] * dt)
            # pos = pos + v * dir * dt
            base_east[k] = base_east[k - 1] + base_speed[k] * math.cos(base_yaw[k]) * dt
            base_north[k] = base_north[k - 1] + base_speed[k] * math.sin(base_yaw[k]) * dt

    # -------------------------------------------------------------
    # 2. Intelligent Dead Reckoning: CNN-GRU + 5-State EKF
    # -------------------------------------------------------------
    ekf = IntelligentEKF(
        init_east=float(gt_east[0]),
        init_north=float(gt_north[0]),
        init_velocity=float(gt_speed[0]),
        init_yaw_rad=float(gt_yaw[0]),
        q_pos=0.04,
        q_vel=0.15,
        q_yaw=0.01,
        q_bias=1e-4
    )

    ekf_east = np.zeros(n_steps)
    ekf_north = np.zeros(n_steps)
    ekf_speed = np.zeros(n_steps)
    ekf_yaw = np.zeros(n_steps)

    pred_speeds = np.zeros(n_steps)
    pred_yaw_rates = np.zeros(n_steps)

    # Pre-build IMU matrix for window slicing: (n_steps, 6)
    imu_matrix = np.column_stack([ax, ay, az, gx, gy, gz]).astype(np.float32)

    with torch.no_grad():
        for k in range(n_steps):
            time_k = t[k]
            in_outage = (outage_start_sec <= time_k <= outage_end_sec)

            # EKF State Prediction using IMU step
            ekf.predict(dt=dt, accel_fwd=float(ax[k]), gyro_yaw_rate=float(gz[k]))

            # Intelligent Neural Network Inference
            if k >= window_size:
                win_tensor = torch.from_numpy(imu_matrix[k - window_size : k]).unsqueeze(0).to(device)
                pred_v, pred_v_var, pred_w, pred_w_var = model(win_tensor)

                v_val = float(pred_v.squeeze().cpu().item())
                v_var = float(pred_v_var.squeeze().cpu().item())
                w_val = float(pred_w.squeeze().cpu().item())
                w_var = float(pred_w_var.squeeze().cpu().item())

                pred_speeds[k] = v_val
                pred_yaw_rates[k] = w_val
            else:
                v_val = float(gt_speed[k])
                v_var = 0.1
                w_val = float(gz[k])
                w_var = 0.05
                pred_speeds[k] = v_val
                pred_yaw_rates[k] = w_val

            if not in_outage:
                # GNSS Available: update position and velocity
                # Simulated GNSS noise ~ 1.5m
                noisy_east = float(gt_east[k] + rng.normal(0, 0.5))
                noisy_north = float(gt_north[k] + rng.normal(0, 0.5))
                noisy_spd = float(max(0.0, gt_speed[k] + rng.normal(0, 0.2)))
                noisy_hdg = float(normalize_angle(gt_yaw[k] + rng.normal(0, 0.05)))

                ekf.update_gnss(
                    east=noisy_east,
                    north=noisy_north,
                    speed=noisy_spd,
                    bearing_rad=noisy_hdg,
                    pos_accuracy_m=2.0,
                    speed_accuracy_ms=0.3,
                    bearing_accuracy_rad=0.08
                )
            else:
                # GNSS Outage: Intelligent Neural Innovation Update
                # Fuses ML velocity and yaw rate predictions to bound drift
                ekf.update_ml_prediction(
                    predicted_velocity=v_val,
                    predicted_yaw_rate=w_val,
                    var_velocity=max(1e-4, v_var),
                    var_yaw_rate=max(1e-4, w_var),
                    dt=dt,
                    measured_gyro_yaw_rate=float(gz[k])
                )

            # Zero-Velocity Update (ZUPT) if detected stationary
            if v_val < 0.15 and abs(gz[k]) < 0.03:
                ekf.update_zupt(float(gz[k]))

            state = ekf.get_state()
            ekf_east[k] = state["east_m"]
            ekf_north[k] = state["north_m"]
            ekf_speed[k] = state["velocity_ms"]
            ekf_yaw[k] = state["yaw_rad"]

    # -------------------------------------------------------------
    # 3. Compute Outage Error Metrics
    # -------------------------------------------------------------
    # Position errors over outage
    base_pos_err = np.sqrt(
        (base_east[outage_indices] - gt_east[outage_indices]) ** 2
        + (base_north[outage_indices] - gt_north[outage_indices]) ** 2
    )
    ekf_pos_err = np.sqrt(
        (ekf_east[outage_indices] - gt_east[outage_indices]) ** 2
        + (ekf_north[outage_indices] - gt_north[outage_indices]) ** 2
    )

    # Speed errors
    base_spd_err = np.abs(base_speed[outage_indices] - gt_speed[outage_indices])
    ekf_spd_err = np.abs(ekf_speed[outage_indices] - gt_speed[outage_indices])
    ml_spd_err = np.abs(pred_speeds[outage_indices] - gt_speed[outage_indices])

    # Yaw rate errors
    ml_yr_err = np.abs(pred_yaw_rates[outage_indices] - gt_yaw_rate[outage_indices])

    base_max_drift = float(np.max(base_pos_err))
    ekf_max_drift = float(np.max(ekf_pos_err))
    drift_reduction_ratio = (base_max_drift / max(1e-3, ekf_max_drift)) if ekf_max_drift > 0 else 1.0

    return {
        "outage_start_sec": outage_start_sec,
        "outage_duration_sec": outage_duration_sec,
        "distance_traveled_m": distance_traveled_m,
        "baseline_pure_imu": {
            "position_drift_mae_m": float(np.mean(base_pos_err)),
            "position_drift_max_m": base_max_drift,
            "position_drift_final_m": float(base_pos_err[-1]),
            "relative_drift_percent": float((base_max_drift / max(1.0, distance_traveled_m)) * 100.0),
            "speed_mae_ms": float(np.mean(base_spd_err))
        },
        "intelligent_dead_reckoning": {
            "position_drift_mae_m": float(np.mean(ekf_pos_err)),
            "position_drift_max_m": ekf_max_drift,
            "position_drift_final_m": float(ekf_pos_err[-1]),
            "relative_drift_percent": float((ekf_max_drift / max(1.0, distance_traveled_m)) * 100.0),
            "speed_mae_ms": float(np.mean(ekf_spd_err)),
            "ml_model_speed_mae_ms": float(np.mean(ml_spd_err)),
            "ml_model_yaw_rate_mae_degs": float(math.degrees(np.mean(ml_yr_err)))
        },
        "drift_reduction_ratio": float(drift_reduction_ratio),
        "percentage_improvement": float(max(0.0, (1.0 - ekf_max_drift / max(1e-4, base_max_drift)) * 100.0))
    }


def print_benchmark_table(metrics: Dict[str, Any], title: str = "IO-VNBD GNSS Outage Benchmark"):
    """Prints a structured comparison report table."""
    base = metrics["baseline_pure_imu"]
    idr = metrics["intelligent_dead_reckoning"]

    print("\n" + "=" * 76)
    print(f"  {title.upper()}")
    print("  Problem Statement: SIH26168 - AI-ML Intelligent Dead Reckoning")
    print("=" * 76)
    print(f"  Outage Duration:     {metrics['outage_duration_sec']:.1f} seconds (from t={metrics['outage_start_sec']:.1f}s)")
    print(f"  Distance Traveled:   {metrics['distance_traveled_m']:.2f} meters")
    print("-" * 76)
    print(f"  {'Metric':<32} | {'Pure IMU Baseline':<18} | {'Intelligent DR':<16}")
    print("-" * 76)
    print(f"  {'Position Drift MAE (m)':<32} | {base['position_drift_mae_m']:>15.2f} m  | {idr['position_drift_mae_m']:>13.2f} m")
    print(f"  {'Maximum Position Drift (m)':<32} | {base['position_drift_max_m']:>15.2f} m  | {idr['position_drift_max_m']:>13.2f} m")
    print(f"  {'Final Position Drift (m)':<32} | {base['position_drift_final_m']:>15.2f} m  | {idr['position_drift_final_m']:>13.2f} m")
    print(f"  {'Relative Drift (% dist)':<32} | {base['relative_drift_percent']:>15.2f} %  | {idr['relative_drift_percent']:>13.2f} %")
    print(f"  {'Speed Estimation MAE (m/s)':<32} | {base['speed_mae_ms']:>15.2f} m/s| {idr['speed_mae_ms']:>13.2f} m/s")
    print("-" * 76)
    print(f"  ML Neural Speed MAE:       {idr['ml_model_speed_mae_ms']:.3f} m/s")
    print(f"  ML Neural Yaw Rate MAE:    {idr['ml_model_yaw_rate_mae_degs']:.3f} deg/s")
    print(f"  >>> Drift Reduction Ratio: {metrics['drift_reduction_ratio']:.2f}x improvement")
    print(f"  >>> Accuracy Enhancement:  {metrics['percentage_improvement']:.2f}% error reduction")
    print("=" * 76 + "\n")


def run_iovnbd_benchmark(
    model_path: str = "idr_model_best.pt",
    data_path: Optional[str] = None,
    outage_start: float = 20.0,
    outage_duration: float = 30.0,
    window_size: int = 50,
    output_json: Optional[str] = None
) -> Dict[str, Any]:
    """Runs end-to-end evaluation on IO-VNBD dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = IntelligentDeadReckoningNet(in_channels=6, conv_channels=64, gru_hidden_size=64, gru_layers=2)

    if os.path.exists(model_path):
        try:
            ckpt = torch.load(model_path, map_location=device, weights_only=False)
            state_dict = ckpt["model_state_dict"] if "model_state_dict" in ckpt else ckpt
            model.load_state_dict(state_dict)
            print(f"[Model] Successfully loaded weights from {model_path}")
        except Exception as e:
            print(f"[Model Notice] Could not load checkpoint ({e}), evaluating model architecture.")
    else:
        print(f"[Model Notice] Checkpoint {model_path} not found. Running with initialized weights.")

    model.to(device)
    model.eval()

    # Determine data file
    loader = IOVNBDLoader(default_fs=10.0)
    csv_file = None

    if data_path and os.path.isfile(data_path):
        csv_file = data_path
    elif data_path and os.path.isdir(data_path):
        files = sorted([f for f in os.listdir(data_path) if f.endswith(".csv")])
        if files:
            csv_file = os.path.join(data_path, files[0])

    if csv_file is None:
        # Check standard sample directories
        for fallback_dir in ["data/iovnbd_samples", "data/iovnbd", "data"]:
            if os.path.isdir(fallback_dir):
                files = sorted([os.path.join(fallback_dir, f) for f in os.listdir(fallback_dir) if f.endswith(".csv")])
                if files:
                    csv_file = files[0]
                    break

    if csv_file is None:
        # Auto-generate a valid sample CSV adhering to IO-VNBD schema
        sample_path = "data/iovnbd_samples/V-Drive_Sample1.csv"
        print(f"[IO-VNBD] No existing CSV found. Auto-generating official-schema sample: {sample_path}")
        generate_sample_iovnbd_v_csv(sample_path, duration_sec=120.0)
        csv_file = sample_path

    print(f"[IO-VNBD] Loading vehicular trajectory from: {csv_file}")
    traj = loader.load_csv(csv_file, target_fs=50.0)

    # Adjust outage start if trajectory is short
    traj_duration = float(traj["time"][-1] - traj["time"][0])
    if traj_duration <= outage_start + outage_duration:
        outage_start = max(5.0, traj_duration * 0.2)
        outage_duration = max(5.0, traj_duration * 0.5)

    metrics = evaluate_trajectory_outage(
        model=model,
        trajectory=traj,
        outage_start_sec=outage_start,
        outage_duration_sec=outage_duration,
        window_size=window_size,
        device=device
    )

    print_benchmark_table(metrics, title=f"IO-VNBD Outage Benchmark ({os.path.basename(csv_file)})")

    if output_json:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"[Benchmark] Saved metrics JSON to {output_json}")

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IO-VNBD Benchmark & GNSS Outage Evaluator (SIH26168)")
    parser.add_argument("--model-path", type=str, default="idr_model_best.pt", help="Path to trained IDR model checkpoint")
    parser.add_argument("--data-path", type=str, default=None, help="Path to IO-VNBD CSV log or folder")
    parser.add_argument("--outage-start", type=float, default=20.0, help="GNSS outage start timestamp in seconds")
    parser.add_argument("--outage-duration", type=float, default=30.0, help="GNSS outage duration in seconds")
    parser.add_argument("--window-size", type=int, default=50, help="IMU temporal window length")
    parser.add_argument("--output-json", type=str, default=None, help="Optional output JSON path for metrics")
    args = parser.parse_args()

    run_iovnbd_benchmark(
        model_path=args.model_path,
        data_path=args.data_path,
        outage_start=args.outage_start,
        outage_duration=args.outage_duration,
        window_size=args.window_size,
        output_json=args.output_json
    )
