# Project Overview & Technical Architecture
## AI-ML Based Intelligent Dead Reckoning System (SIH26168)
### Problem Category: ISRO / Smart Vehicles

---

## 1. General Explanation: What Does This Project Do?

### The Core Problem
Modern autonomous vehicles, navigation systems, and smart mobility applications rely heavily on **GNSS** (Global Navigation Satellite Systems such as GPS, NavIC, Galileo, GLONASS) to determine their position on Earth. 

However, satellite signals are fragile:
- When a vehicle enters a **tunnel**, drives through an **underpass**, navigates dense **urban canyons** with skyscrapers, or experiences **signal spoofing/jamming**, satellite signals are completely lost.
- Traditional navigation systems fall back to **Pure IMU Dead Reckoning** (using the vehicle's or smartphone's accelerometer and gyroscope). 
- Because position is the **double mathematical integral of acceleration** ($\iint a \, dt^2$), even microscopic sensor noise, thermal bias, and vibrations compound **quadratically ($O(t^2)$)**. Within just 15 to 30 seconds of driving with pure IMU integration, position error easily exceeds 100 meters, causing the virtual vehicle on the map to spin out, swerve, or fly off the road.

### What This System Does
This project provides an **Intelligent Neural-Inertial Dead Reckoning (IDR) and Sensor Fusion Engine**:
1. It acts as an intelligent backup navigation brain that continuously runs alongside satellite navigation.
2. While satellite reception is healthy, the system observes how the vehicle moves and automatically learns the subtle hardware imperfections, mounting tilt, and drift of the sensors.
3. The moment satellite signals cut off (e.g., inside an 800-meter tunnel or a 50-second blackout), the system instantly takes over. Instead of blindly integrating raw noisy accelerometer readings, it uses a **deep learning neural network (1D-CNN + BiGRU)** fused with **physics-informed vehicle kinematics** to predict the vehicle's true speed, turn rate, and road curvature.
4. An **Extended Kalman Filter (EKF)** fuses these predictions into smooth, lane-accurate coordinates on the map.
5. The moment satellite reception returns, the system seamlessly hands control back to satellite positioning without any visual jumping or trajectory jitter.

---

## 2. Real-World Analogy

Imagine walking through a room with your eyes wide open (Active GNSS). You know exactly where you are. 

Now imagine closing your eyes tightly for 60 seconds while continuing to walk through hallways and turning corners (GNSS Blackout):
- **Naive IMU Integration**: Trying to calculate your exact position strictly by counting the tiny vibrations in your feet and multiplying by time squared. Within 10 steps, a tiny misjudgment makes you think you have walked through a brick wall.
- **Intelligent Dead Reckoning (Our Approach)**: Your brain's inner ear (vestibular system) recognizes how walking *feels* (your cadence, momentum, lean during turns, and stopping at obstacles). You know your walking pace is roughly 1.3 m/s, you feel when you slow down or turn 90 degrees, and when you stop, you don't hallucinate that you are still flying forward. When you open your eyes, you are right where you anticipated.

---

## 3. Technologies & Stack Used

| Component / Layer | Technology / Framework | Purpose |
| :--- | :--- | :--- |
| **Deep Learning Framework** | **PyTorch 2.x (CUDA & CPU)** | Designing, training, and running the 1D-CNN + BiGRU dual-head neural network. |
| **Edge Deployment & Acceleration**| **ONNX Runtime / TorchScript** | Optimized edge inference with sub-2-millisecond latency per IMU window. |
| **State Estimation & Fusion** | **Extended Kalman Filter (EKF)** | 5-state nonlinear state estimator operating in local Cartesian metric space. |
| **Geodetic Coordinates** | **Bowring's Closed-Form WGS84** | Bidirectional conversion between geodetic (Latitude, Longitude) and local ENU (East, North, Up) coordinates. |
| **Kinematics & Physics Engine** | **NumPy & Python Math** | Forward acceleration integration, centripetal turn limits ($v = \|a_y\| / \|\omega_z\|$), road pitch estimation, and dual-variance ZUPT. |
| **Benchmark Datasets** | **IO-VNBD Dataset** | High-precision Racelogic VBOX RTK (29 columns) and consumer Smartphone (24 columns) 5.0 km road driving runs. |
| **Backend Web Server** | **FastAPI & Uvicorn** | High-throughput asynchronous REST endpoints and real-time WebSocket server streaming at 50 Hz. |
| **Frontend Map Dashboard** | **Leaflet.js + HTML5 / CSS3 / Vanilla JS** | Material Design 3 interface featuring live polyline tracks, HUD dials, telemetry cards, and interactive playback controls. |
| **Unit & Integration Testing** | **Pytest** | 29 automated test cases covering math, transforms, EKF stability, dataset schemas, and API routes. |

---

## 4. Key Technical Terms & Concepts Explained

### 1. Dead Reckoning (DR)
The process of calculating one's current position by advancing a previously determined position using estimated speeds, elapsed time, and direction of motion.

### 2. GNSS vs. GPS
- **GNSS (Global Navigation Satellite System)**: The overarching term for all satellite positioning constellations globally (GPS [USA], NavIC [India], Galileo [EU], GLONASS [Russia], BeiDou [China]).
- **GPS**: A specific American satellite constellation that is part of GNSS.

### 3. IMU (Inertial Measurement Unit) & 6-DOF
An electronic device measuring specific force and angular rate:
- **3-axis Accelerometer**: Measures linear acceleration ($a_x, a_y, a_z$) including Earth's gravity ($9.81\,\text{m/s}^2$).
- **3-axis Gyroscope**: Measures angular rotation rate ($\omega_x, \omega_y, \omega_z$) around the vehicle's roll, pitch, and yaw axes.
- **6-DOF (Six Degrees of Freedom)**: The combination of 3 translational axes (forward, lateral, vertical) and 3 rotational axes (roll, pitch, yaw).

### 4. Quadratic Drift Problem ($O(t^2)$)
In classical physics:
$$\text{Velocity: } v(t) = v_0 + \int_0^t a(\tau) \, d\tau$$
$$\text{Position: } p(t) = p_0 + \int_0^t v(\tau) \, d\tau = p_0 + v_0 t + \iint_0^t a(\tau) \, d\tau^2$$
If an accelerometer has a tiny constant calibration bias $\epsilon = 0.05\,\text{m/s}^2$:
$$\text{Position Error} = \frac{1}{2} \epsilon t^2$$
- At $t = 10\text{s}$, error $= 2.5\text{ meters}$.
- At $t = 60\text{s}$, error $= 90\text{ meters}$.
- At $t = 120\text{s}$, error $= 360\text{ meters}$.
This quadratic compounding makes pure accelerometer integration unusable for vehicle navigation without continuous external constraints.

### 5. 1D-CNN (Temporal 1D Convolutional Neural Network)
Instead of processing 2D image pixels, a 1D-CNN slides convolutional filter kernels over a temporal time window (50 samples representing 1 second of IMU data). It automatically extracts high-level vibration patterns, engine frequency signatures, and suspension responses while rejecting random noise spikes.

### 6. BiGRU (Bidirectional Gated Recurrent Unit)
A specialized recurrent neural network (RNN) that processes temporal sequential data both forward in time (past to present) and backward in time (present to past). This allows the network to understand the contextual arc of vehicle maneuvers—such as whether a momentary deceleration is the start of a full stop or simply gear shifting.

### 7. Heteroscedastic Aleatoric Uncertainty
- **Aleatoric Uncertainty**: Inherent noise and randomness in the physical input data (e.g., rough gravel roads vs. smooth asphalt).
- **Heteroscedastic**: The uncertainty is *not constant*—it varies dynamically depending on the current vehicle state.
- The neural network has dual output heads:
  1. Mean predictions ($\mu_v, \mu_\omega$): Predicted forward velocity and turn rate.
  2. Variance predictions ($\sigma_v^2, \sigma_\omega^2$): The model's self-estimated predictive uncertainty.
When the vehicle encounters an unpredictable bump, $\sigma^2$ naturally expands, signaling to the Kalman filter to place less trust in the measurement.

### 8. Extended Kalman Filter (EKF)
An optimal recursive mathematical estimator for non-linear dynamic systems:
- **State Vector ($x$)**: 5 dynamic states:
  $$x = \begin{bmatrix} p_E & p_N & v & \psi & b_\psi \end{bmatrix}^T$$
  (East position, North position, forward velocity, heading yaw angle, and gyroscope yaw bias).
- **Prediction Step**: Projects the vehicle forward in time using kinematic motion equations and updates the error covariance matrix ($P$).
- **Update Step**: When observations arrive (either GNSS coordinates or neural network pseudo-odometry), computes the **Kalman Gain ($K$)** to blend prediction with measurement based on their relative uncertainties.

### 9. Local Tangent Plane (ENU) & Bowring WGS84 Transformation
- Earth is an oblate spheroid defined by the **WGS84** reference ellipsoid (semi-major axis $a \approx 6,378,137\,\text{m}$, flattening $f \approx 1/298.257$).
- Because measuring distances in angular degrees (latitude, longitude) introduces severe trigonometric distortion across different latitudes, the system converts geodetic coordinates into a local Cartesian coordinate frame measured in metric meters:
  - **East ($E$)**: Meters traveled eastward.
  - **North ($N$)**: Meters traveled northward.
  - **Up ($U$)**: Meters altitude relative to the local reference point.
- **Bowring's algorithm** provides closed-form, non-iterative micro-millimeter precision between geodetic and local ENU coordinates.

### 10. Pseudo-Odometry
Vehicles without direct wheel encoder interfaces (or during wheel slip) rely on external estimations of speed and turning rate. Because our neural network outputs forward speed and yaw rate, these act as virtual wheel encoders ("pseudo-odometers") fed into the EKF update equations.

### 11. Centripetal Turn Constraint
When any wheeled vehicle executes a turn, Newtonian physics dictates that lateral acceleration ($a_y$), forward speed ($v$), and angular yaw rate ($\omega_z$) satisfy:
$$a_y = v \cdot \omega_z \implies v_{\text{turn}} = \frac{|a_y|}{|\omega_z|}$$
During a blackout, our kinematics engine uses this relationship as an independent physical boundary: turning speed cannot exceed what the lateral centripetal acceleration allows, preventing turn runaway or speed collapses.

### 12. Road Pitch Grade Compensation
When driving uphill or downhill, gravity projects onto the vehicle's longitudinal axis ($g \cdot \sin(\theta)$). Without pitch compensation, an accelerometer perceives gravity as constant forward braking or rearward acceleration. The system continuously estimates road grade angle $\theta$ and subtracts the gravitational component:
$$a_{\text{fwd}} = a_x - b_a - g \cdot \sin(\theta)$$

### 13. ZUPT (Zero-Velocity Update) & ZARU (Zero-Angular-Rate Update)
- **ZUPT**: When a vehicle stops at a traffic light or junction, its true physical velocity is exactly $0.0\,\text{m/s}$.
- The system monitors variance in acceleration and gyroscope readings. When variance falls below empirical thresholds, it locks the vehicle velocity to zero and zeroes out residual integration drag, eliminating stop crawl.
- **ZARU**: When stationary, any recorded rotation is purely gyroscope bias drift. The system resets the gyroscope bias ($b_\psi$), recalibrating the sensor for free while idling.

### 14. Online Gradient Descent (OGD)
A lightweight runtime machine learning algorithm that adjusts linear scale and offset parameters while driving under good satellite visibility, ensuring that changing ambient temperatures or phone mount shifting do not degrade navigation accuracy.

---

## 5. End-to-End Workflow: What Happens During a Drive

```text
[1. Clear Sky Driving]
       │
       ├─ GNSS updates arrive at 1-10 Hz (high accuracy).
       ├─ EKF corrects position and velocity states.
       ├─ Online Calibrator compares ML predictions vs. GNSS ground truth.
       └─ Gyroscope bias and device scale factors are continuously fine-tuned.
       │
       ▼
[2. Entering Tunnel / GNSS Blackout Window]
       │
       ├─ Satellite signal drops to 0 fixes.
       ├─ Authoritative Outage Flag activates.
       ├─ EKF seamlessly switches measurement source from GNSS to Neural Pseudo-Odometry.
       └─ Kinematics Engine engages centripetal bounds and road pitch compensation.
       │
       ▼
[3. Inside the Tunnel (e.g. 50-second outage)]
       │
       ├─ 1D-CNN + BiGRU predicts forward speed and yaw rate from 50-sample IMU windows.
       ├─ Forward acceleration integration prevents speed lag during acceleration bursts.
       ├─ Centripetal turn constraint maintains precise trajectory curvature around bends.
       └─ Dual-variance ZUPT prevents false drift if the vehicle stops in tunnel traffic.
       │
       ▼
[4. Exiting the Tunnel]
       │
       ├─ Satellite lock is reacquired.
       ├─ GNSS measurements immediately resume feeding the EKF update equations.
       ├─ Trajectory converges smoothly without sudden coordinate snapping.
       └─ Calibration profile is saved to disk for subsequent drives.
```

---

## 6. Codebase Architecture & File Roles

| File Path | Functional Role in the Project |
| :--- | :--- |
| [`backend/main.py`](file:///c:/Users/visnu/Desktop/aiml%20project/backend/main.py) | **Central Orchestrator**: Houses the `NavigationCore` class, loads trajectory data, drives the 50 Hz simulation loop, handles WebSocket commands, and manages manual outage overrides. |
| [`backend/dashboard.html`](file:///c:/Users/visnu/Desktop/aiml%20project/backend/dashboard.html) | **User Interface HUD**: Material Design 3 dashboard with Leaflet map, live trajectory overlays (Blue = Ground Truth, Green = AI DR, Red = Naive IMU), speedometers, confidence meters, and interactive playback buttons. |
| [`backend/schemas.py`](file:///c:/Users/visnu/Desktop/aiml%20project/backend/schemas.py) | **Data Models**: Pydantic schemas validating IMU packets, GNSS fixes, and telemetry payloads. |
| [`models/idr_model.py`](file:///c:/Users/visnu/Desktop/aiml%20project/models/idr_model.py) | **Deep Learning Architecture**: PyTorch implementation of the 1D-CNN feature extractor + Bidirectional GRU with heteroscedastic uncertainty heads. |
| [`models/online_calibrator.py`](file:///c:/Users/visnu/Desktop/aiml%20project/models/online_calibrator.py) | **Runtime Self-Correction**: Implements Online Gradient Descent, bias estimation, and device profile serialization (`device_drift_profile.json`). |
| [`models/train.py`](file:///c:/Users/visnu/Desktop/aiml%20project/models/train.py) | **Training Pipeline**: Supports training on real IO-VNBD datasets, synthetic drives, or hybrid combinations, and exports trained weights to PyTorch (`.pt`) and TorchScript. |
| [`sensor_fusion/ekf.py`](file:///c:/Users/visnu/Desktop/aiml%20project/sensor_fusion/ekf.py) | **Sensor Fusion Core**: 5-state Extended Kalman Filter implementing state propagation, covariance updates, Kalman gain calculation, and ZUPT clamping. |
| [`sensor_fusion/coordinates.py`](file:///c:/Users/visnu/Desktop/aiml%20project/sensor_fusion/coordinates.py) | **Geodesy Math**: Closed-form Bowring algorithm converting WGS84 Geodetic coordinates (Lat, Lon, Alt) to Local Cartesian Tangent Plane (East, North, Up). |
| [`data/iovnbd_loader.py`](file:///c:/Users/visnu/Desktop/aiml%20project/data/iovnbd_loader.py) | **Dataset Ingestion**: Parses 29-column VBOX RTK and 24-column Smartphone CSV logs from Coventry University's IO-VNBD benchmark. |
| [`benchmark_iovnbd.py`](file:///c:/Users/visnu/Desktop/aiml%20project/benchmark_iovnbd.py) | **Offline Benchmark Suite**: Runs quantitative evaluations comparing Naive IMU vs. AI Dead Reckoning drift across specified outage windows. |
| [`run_backend.py`](file:///c:/Users/visnu/Desktop/aiml%20project/run_backend.py) | **Application Entrypoint**: Launches the Uvicorn web server hosting the dashboard on port `8080`. |
| [`tests/`](file:///c:/Users/visnu/Desktop/aiml%20project/tests/) | **Automated Quality Suite**: 29 unit and integration tests verifying mathematical correctness, EKF stability, dataset parsing, and API behavior. |

---

## 7. Summary & Impact

By combining **deep learning temporal feature extraction**, **physics-informed vehicle dynamics**, and an **Extended Kalman Filter**, this project solves the fundamental limitation of traditional dead reckoning:
- It eliminates the runaway $O(t^2)$ double-integration drift of raw consumer sensors.
- It provides a reliable, self-calibrating navigation safety net suitable for autonomous ground vehicles, smart mobility services, and mission-critical navigation under GNSS-denied environments.
