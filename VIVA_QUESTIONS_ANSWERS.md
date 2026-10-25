# SIH26168: AI-ML Based Intelligent Dead Reckoning System
## Comprehensive Hackathon Viva Voce Q&A Guide (50 Questions)
**Category:** ISRO / Smart Vehicles  
**Problem Statement:** Seamless Navigation & IMU Sensor Drift Mitigation during GNSS Outages

---

### Section A: Dataset Loading & Understanding

#### 1. What is the objective of your machine learning problem?
**Answer:**  
The objective is to eliminate accumulated positional and heading drift in vehicular dead reckoning during GNSS (GPS) outages (e.g., in long tunnels, dense urban canyons, and underpasses). Standard low-cost MEMS IMUs (accelerometers and gyroscopes) suffer from thermo-mechanical noise, bias instabilities, and non-holonomic vehicle dynamics, causing cubic position error accumulation ($O(t^3)$) within seconds. Our AI-ML model maps short temporal windows of noisy 6-DoF IMU measurements directly to continuous forward velocity ($v_x$) and yaw rate ($\dot{\psi}$) along with aleatoric uncertainty ($\log \sigma^2$), which are then fused into a 5-state Extended Kalman Filter (EKF) to maintain continuous, jump-free navigation.

#### 2. What is the target variable in your dataset?
**Answer:**  
The model has a dual regression target vector at each time step:
1. **Forward Velocity ($v \in \mathbb{R}_{\ge 0}$, in m/s):** The vehicle's longitudinal forward ground speed.
2. **Yaw Angular Rate ($\dot{\psi} \in \mathbb{R}$, in rad/s):** The rotational rate of change of vehicle heading in the local tangent frame.
Additionally, the network predicts their respective aleatoric log-variances ($\log \sigma_v^2, \log \sigma_{\dot{\psi}}^2$) via a heteroscedastic loss formulation to quantify prediction uncertainty.

#### 3. Is your problem classification, regression, or clustering? Why?
**Answer:**  
It is a **continuous multivariate time-series regression** problem. Vehicle speed and yaw rate are continuous kinematic physical quantities that vary smoothly over time. Discretizing them into classes (classification) would introduce quantization errors that cause jittery jumps in dead reckoning integration. Clustering is unsupervised and inapplicable because ground-truth odometry and geodetic reference trajectories from RTK-GPS / VBOX HD2 are available for supervised training.

#### 4. How many records and features are present in the dataset?
**Answer:**  
In our IO-VNBD benchmark and synchronized simulation dataset:
* **Features:** 6 primary time-series input channels sampled at 50 Hz ($T = 0.02$ s):
  * 3-Axis Specific Force (Linear Acceleration): $a_x, a_y, a_z$ (in m/s$^2$)
  * 3-Axis Angular Velocity (Gyroscope): $\omega_x, \omega_y, \omega_z$ (in rad/s)
* **Sliding Window Dimensions:** Windows of 50 samples (1.0 second duration) $\times$ 6 channels = $[B, 50, 6]$ tensor per inference step.
* **Records:** Over 8,000+ sliding window instances for single benchmark runs, and tens of thousands across multi-driver runs (e.g., IO-VNBD Driver A through F recordings covering urban, suburban, and highway regimes).

#### 5. Which features are numerical and which are categorical?
**Answer:**  
* **Numerical Features:** All primary inputs are continuous floating-point signals:
  * Accelerometer measurements ($a_x, a_y, a_z \in \mathbb{R}$)
  * Gyroscope measurements ($\omega_x, \omega_y, \omega_z \in \mathbb{R}$)
  * GNSS ground-truth metrics (Speed, Bearing, Latitude, Longitude, HDOP)
* **Categorical Features:** Meta-information used during data splitting and validation filtering, such as device mounting location (`DASHBOARD`, `CUPHOLDER`, `POCKET`) and road surface type (`ASPHALT`, `COBBLESTONE`), which are not passed as direct inputs to the edge regression core to ensure mounting-agnostic generalization.

#### 6. How did you identify missing values?
**Answer:**  
We evaluated time-series continuity by verifying monotonic timestamps ($t_{i} - t_{i-1} \approx \Delta t = 0.02$ s). Missing samples (dropped sensor packets over Android HAL or serial bus) and corrupt frames were identified using:
1. `np.isnan()` and `np.isinf()` masking across all 6 IMU columns.
2. Timestamp gap detection: flagging any $\Delta t > 1.5 \times \text{expected\_dt}$ (30 ms at 50 Hz).
3. Zero/Null Island checks on GNSS streams ($\text{lat} = 0.0, \text{lon} = 0.0$) and satellite count $< 4$.

#### 7. What data-quality issues did you observe?
**Answer:**  
Four major data-quality phenomena were discovered and addressed:
1. **Engine & Chassis Vibration Resonance:** High-frequency vibration spikes (20–40 Hz) superposed on true translational accelerations.
2. **Mounting Pitch/Tilt Gravity Leakage:** A phone pitched at an angle $\theta$ leaks Earth's gravity ($g \sin \theta \approx 9.81 \sin \theta$) directly into the forward acceleration axis, creating artificial acceleration when cruising at constant speed.
3. **Sensor Thermal Drift & Turn-on Bias:** Gyroscope zero-rate output wanders over time ($b_{yaw} \ne 0$), generating runaway rotational errors.
4. **GNSS Multipath & Dropouts:** High Dilution of Precision (HDOP $> 5.0$) and complete packet loss in urban canyons and tunnels.

#### 8. Why is understanding the dataset important before model building?
**Answer:**  
In inertial navigation, naive deep learning easily overfits to vehicle-specific vibrations or route-specific geometry. Understanding the sensor physics (ISO 8855 vs. ENU coordinate frames, sensor noise density, sample rate jitter, and gravity leakage) ensures:
* Correct temporal window sizing (e.g., 50 samples / 1 second captures enough vibration cycles without introducing integration lag).
* Correct coordinate frame transformations (converting compass azimuth $0^\circ = \text{North}$ to ENU radians $0 = \text{East}$).
* Designing models that generalize across different vehicle mountings and road terrains.

#### 9. Which feature appears to have the strongest relationship with the target?
**Answer:**  
* For **Forward Speed ($v$):** Longitudinal specific force ($a_x$) and the variance of vertical acceleration ($\sigma_{a_z}^2$, vibration amplitude increases with rolling speed).
* For **Yaw Rate ($\dot{\psi}$):** Vertical-axis angular velocity ($\omega_z$), which directly reflects vehicle rotation rate, subject to sensor bias offset.

#### 10. Did you identify any duplicate records or irrelevant columns?
**Answer:**  
Yes. In raw vehicle telemetry logs (such as VBOX HD2 or Android sensor framework dumps):
* **Irrelevant columns:** Ambient light, battery temperature, device screen state, and satellite PRN numbers were stripped.
* **Duplicate timestamps:** Caused by asynchronous sensor event listener callbacks polling faster than the hardware IMU sample rate; deduplicated by strict temporal resampling.

---

### Section B: Data Preprocessing

#### 11. How did you handle missing values?
**Answer:**  
* For small IMU dropouts ($\le 3$ missing frames / 60 ms): We used cubic spline interpolation on acceleration and continuous angular rate interpolation with boundary-safe phase unwrapping.
* For larger dropouts ($> 100$ ms): Windows containing gaps were discarded from the training set to prevent artificial linear interpolation slopes from biasing the convolutional kernels.
* For GNSS dropouts in ground-truth training: We used bidirectional kinematic dead reckoning bridging valid RTK-GPS fixes.

#### 12. Why did you choose mean/median/mode imputation or another technique?
**Answer:**  
Mean/median/mode imputation is **strictly invalid for continuous high-frequency inertial time-series data**. Imputing the mean creates abrupt non-physical step discontinuities in acceleration ($da/dt = \text{jerk} \to \infty$) and breaks frequency-domain characteristics. We chose **kinematic interpolation with angular unwrapping** because vehicular motion is governed by physical laws with continuous velocity and bounded acceleration.

#### 13. How did you handle categorical variables?
**Answer:**  
Categorical metadata (e.g., driver ID, vehicle model, smartphone model) were intentionally excluded from the online inference input tensor. By restricting inputs strictly to 6-DoF calibrated inertial vectors and training across diverse drivers and phone mountings, the model learns universal inertial dynamics rather than memorizing categorical identifiers.

#### 14. What is the difference between Label Encoding and One-Hot Encoding?
**Answer:**  
* **Label Encoding:** Assigns an integer $[0, 1, 2, \dots]$ to each category. This imposes an unintended ordinal mathematical relationship ($0 < 1 < 2$), which can confuse regression distance metrics.
* **One-Hot Encoding:** Creates binary indicator vectors for each unique category, preventing false ordinal relationships at the expense of expanding feature dimensionality.
* *In our project:* Categorical variables are not fed into the regression network.

#### 15. Why is feature scaling required for some ML algorithms?
**Answer:**  
Raw accelerometer data ($a \approx 0 \text{ to } 20 \text{ m/s}^2$) and gyroscope data ($\omega \approx 0 \text{ to } 0.5 \text{ rad/s}$) operate on completely different numerical scales (differing by 1–2 orders of magnitude). Without scaling:
1. Gradients for high-magnitude features dominate the optimizer step, causing oscillating or slow convergence.
2. Neural network activation functions (LeakyReLU, Sigmoid, Tanh) can saturate or operate in asymmetrical sensitivity regions.

#### 16. Which scaling technique did you use and why?
**Answer:**  
We used **Robust Z-score Standardization with dynamic scaling**:
$$z = \frac{x - \mu}{\sigma}$$
* Acceleration channels: Scaled with global vehicular empirical statistics ($\mu_a \approx 0, \sigma_a \approx 3.0 \text{ m/s}^2$).
* Gyroscope channels: Scaled by typical vehicular turn rates ($\mu_\omega \approx 0, \sigma_\omega \approx 0.25 \text{ rad/s}$).
Standardization maintains physical zero points (critical for detecting stationary vehicle states during ZUPT) unlike Min-Max normalization $[0, 1]$, which would destroy negative deceleration and turn directions.

#### 17. How did you detect and handle outliers?
**Answer:**  
* **Detection:** Physical domain boundary constraints. A standard commercial ground vehicle cannot exceed $3.0g$ ($29.4 \text{ m/s}^2$) acceleration or $120^\circ/\text{s}$ ($2.09 \text{ rad/s}$) yaw rate under non-crash conditions. Any sensor spikes exceeding these kinematic bounds or $5\sigma$ rolling variance were flagged as sensor collision artifacts (e.g., dropping the smartphone in the cabin).
* **Handling:** Hard saturation clipping (`np.clip`) to the maximum physical vehicular envelope to prevent gradient explosion during backpropagation.

#### 18. What is data leakage? Did your preprocessing introduce any leakage?
**Answer:**  
Data leakage occurs when information from outside the training dataset (such as validation or test sets) is inadvertently used to train the model.  
**No leakage was introduced:**
1. Sliding windows were constructed **strictly within isolated continuous driving trajectories**. Windows never straddle the boundary between train and test drives.
2. Normalization parameters ($\mu, \sigma$) were computed exclusively on the training fold and applied transitively to the test fold.
3. Test sets consisted of completely unseen driver runs and distinct geographic routes.

#### 19. Why should preprocessing be fitted only on the training data?
**Answer:**  
Fitting preprocessing (e.g., calculating mean, variance, or scale parameters) across the combined dataset leaks statistical distribution properties of the test set into the model. In real-world deployment, the vehicle will encounter unseen future roads with unknown distributions; evaluating on test sets preprocessed using their own statistics provides an over-optimistic, invalid estimate of generalizability.

#### 20. How did you divide the data into training and testing sets?
**Answer:**  
We utilized **Trajectory-Level Split (Group-K-Fold by Drive Session)** rather than random frame shuffling:
* Random row shuffling on time-series data is invalid because overlapping windows $[t_{i}, t_{i+50}]$ and $[t_{i+1}, t_{i+51}]$ share 98% identical data, causing catastrophic data leakage.
* We partitioned entire distinct driving sessions: e.g., 8 trajectories for training (80%) and 2 full separate runs for validation/testing (20%), verifying generalization across distinct road profiles and phone mounting orientations.

---

### Section C: Feature Engineering & Selection

#### 21. Why did you select these particular features?
**Answer:**  
The 6-DoF inertial triad ($a_x, a_y, a_z, \omega_x, \omega_y, \omega_z$) provides the minimal, complete set of rigid-body kinematic measurements in 3D space:
* $a_x$ (Longitudinal acceleration) governs forward velocity dynamics ($v = \int a_x dt$).
* $a_y$ (Lateral acceleration) and $\omega_z$ (Yaw rate) are coupled through centripetal acceleration ($a_{lat} = v \cdot \omega_z$), providing an internal cross-constraint for velocity estimation during turns.
* $a_z$ captures road bump vibrations, allowing the network to infer vehicle speed from chassis suspension oscillation frequency.

#### 22. What is feature selection?
**Answer:**  
Feature selection is the process of isolating the most relevant, non-redundant subset of features from the raw dataset to optimize model accuracy, reduce computational latency, and prevent the curse of dimensionality. In our edge deployment, keeping feature count minimal (6 channels) ensures sub-millisecond inference on mobile CPUs.

#### 23. What is the difference between feature selection and feature extraction?
**Answer:**  
* **Feature Selection:** Selects a subset of existing original features without transforming them (e.g., selecting $a_x, a_y, a_z, \omega_x, \omega_y, \omega_z$ and discarding magnetometer/barometer).
* **Feature Extraction:** Projects or transforms the original feature space into a new, lower-dimensional set of latent representations (e.g., our 1D Temporal Convolutional layers extracting 128 latent feature maps from raw IMU windows).

#### 24. How can irrelevant features affect model performance?
**Answer:**  
Including non-informative channels (e.g., ambient temperature, device proximity sensor, or noisy raw magnetic field distorted by the vehicle's steel chassis):
1. Adds random noise that degrades model generalization.
2. Increases model parameter count and edge inference latency.
3. Increases the risk of the recurrent network learning spurious correlations (overfitting).

#### 25. What is correlation, and how did you use it in your project?
**Answer:**  
Correlation quantifies the linear or monotonic relationship between two variables (ranging from $-1$ to $+1$). In our project:
* We evaluated Pearson and Spearman correlations between IMU channels and vehicle ground speed.
* We verified the strong physical correlation between $\omega_z$ and the GPS heading derivative ($r > 0.92$), confirming that the sensor coordinate axes were correctly mapped to vehicle body coordinates.

#### 26. Did you remove highly correlated features? Why?
**Answer:**  
In standard tabular models, collinear features are dropped to prevent multicollinearity. However, in physical sensor fusion, collinearities reflect physical laws (e.g., $a_y$ and $\omega_z$ during turns). Instead of dropping them, we retained all 6 DoF channels so the 1D-CNN can learn cross-channel kinematic constraints ($a_y \approx v \cdot \omega_z$), which allows the network to estimate speed even when accelerometer integration drifts.

#### 27. What is dimensionality reduction?
**Answer:**  
Dimensionality reduction transforms high-dimensional data into a compact representation while retaining the maximum variance or task-relevant information. In our neural network, 1D MaxPooling layers (`pool1`, `pool2`) perform temporal dimensionality reduction, condensing a 50-step sequence down to high-level temporal representations before feeding into the GRU layers.

#### 28. Why might reducing the number of features improve a model?
**Answer:**  
1. **Mitigates Overfitting:** Fewer free parameters reduce the model's capacity to memorize noise.
2. **Accelerates Convergence:** Faster gradient propagation across smaller weight matrices.
3. **Optimizes TinyML/Edge Efficiency:** Reduces RAM buffer consumption, cache misses, and battery draw on smartphone chipsets.

#### 29. In PCA, what does explained variance mean?
**Answer:**  
In Principal Component Analysis (PCA), explained variance measures the proportion of the dataset's total mathematical variance that is captured by each principal component (eigenvector of the covariance matrix). A cumulative explained variance of 95% across the top $k$ components indicates that $k$ dimensions retain 95% of the information content of the original dataset.

#### 30. Why is scaling particularly important before applying PCA?
**Answer:**  
PCA is an orthogonal linear projection based on maximizing variance. If features are on different scales (e.g., acceleration in m/s$^2$ vs. gyro in rad/s), features with numerically larger scales will artificially dominate the variance calculation, causing the principal components to align with units rather than true underlying physical patterns.

---

### Section D: Model Implementation

#### 31. Why did you select your particular machine learning algorithm?
**Answer:**  
We engineered a **Hybrid 1D-CNN + Bi-directional GRU Deep Neural Network**:
* **1D-CNN (Temporal Convolutional Block with Residual Skip):** Acts as an adaptive FIR filter. It excels at extracting local temporal features and filtering out high-frequency chassis vibrations and bump impacts.
* **Gated Recurrent Unit (GRU):** Processes the temporal sequence of extracted features, modeling inertial integration over time and long-term sensor drift dependencies. We chose GRU over LSTM because GRU has fewer parameters (3 gates vs. 4 gates), achieves faster convergence, and runs with lower latency on mobile edge runtimes.

#### 32. How does your selected algorithm work at a high level?
**Answer:**  
```
Raw IMU Window [B, 50, 6] 
  ──► Conv1D (k=5) + BatchNorm + LeakyReLU + Residual Skip ──► MaxPool(2)
  ──► Conv1D (k=3) + BatchNorm + LeakyReLU + Residual Skip ──► MaxPool(2)
  ──► 2-Layer GRU (hidden_size=64, dropout=0.15) ──► Latent State h_T
  ──► Head 1: Forward Speed (v) + Uncertainty (log σ_v²)
  ──► Head 2: Yaw Rate (ω) + Uncertainty (log σ_ω²)
```
The predicted mean values feed into the EKF measurement update, while the predicted variances $\sigma^2$ dynamically adjust the Kalman measurement noise covariance matrix $R_t$.

#### 33. What are the major assumptions or limitations of your model?
**Answer:**  
* **Assumptions:** Non-holonomic ground vehicle constraints (the vehicle predominantly moves forward along its longitudinal axis without lateral sliding or flight).
* **Limitations:** If the smartphone is completely loose and tumbling freely in the cabin during a turn, body-frame acceleration axes undergo rapid unmodeled rotations unless compensated by attitude-quaternion pre-rotation.

#### 34. What is the difference between training data and testing data?
**Answer:**  
* **Training Data:** The dataset utilized by the optimization algorithm (AdamW) to compute loss gradients and iteratively update network weights and biases via backpropagation.
* **Testing Data:** An independent, held-out dataset of unseen vehicle trajectories used exclusively to evaluate the generalized performance, drift accumulation, and out-of-distribution robustness of the final model.

#### 35. What is overfitting?
**Answer:**  
Overfitting occurs when a model learns the detail and noise of the training data to the extent that it negatively impacts performance on new, unseen data. In our context: the model would memorize specific road bumps on a training route rather than learning general relationship between vibration frequency and vehicle speed, resulting in low training loss but high validation drift.

#### 36. What is underfitting?
**Answer:**  
Underfitting occurs when the model is too simple to capture the underlying structure of the data. For example, using a simple linear regression model to predict speed from raw acceleration without temporal windowing fails because velocity depends on the integral of past states rather than an instantaneous scalar mapping.

#### 37. How can you reduce overfitting?
**Answer:**  
We implemented five concrete regularization techniques:
1. **Residual Conv Blocks with Dropout ($p = 0.15$):** Prevents co-adaptation of hidden features.
2. **Weight Decay (AdamW, $1 \times 10^{-4}$):** $L_2$ regularization penalizing excessively large weights.
3. **Cosine Annealing Learning Rate Scheduler:** Smoothly decays learning rate from $10^{-3}$ to $10^{-5}$ to find wide, generalizable local minima.
4. **Domain Randomization Data Augmentation:** Injecting synthetic sensor bias drifts ($\pm 0.15\text{ m/s}^2$, $\pm 0.04\text{ rad/s}$), vibration amplitudes, and mounting pitch angles during training.
5. **Early Stopping:** Saving checkpoints based on validation loss rather than training loss.

#### 38. What is the purpose of hyperparameter tuning?
**Answer:**  
Hyperparameter tuning optimizes configuration variables that are not learned directly by model weights (e.g., learning rate, convolution kernel sizes, GRU hidden dimensions, sliding window length). Tuning balances model expressive capacity against computational latency and memory consumption on the target edge device.

#### 39. What is the difference between a parameter and a hyperparameter?
**Answer:**  
* **Parameter:** Internal model variables learned directly from data during training via optimization (e.g., convolution filter weights $W$, batch norm scales $\gamma$, GRU recurrent weights $W_{hh}$, and bias vectors $b$).
* **Hyperparameter:** External configuration settings established prior to training (e.g., learning rate $\alpha = 10^{-3}$, batch size $B = 64$, window length $L = 50$, GRU hidden units $H = 64$).

#### 40. Why might an ensemble model perform better than a single model?
**Answer:**  
An ensemble combines predictions from multiple models to reduce variance and improve robustness. In our architecture, the **AI-ML Neural Network + Extended Kalman Filter (EKF)** acts as a physics-informed hybrid ensemble: the neural network estimates complex non-linear speed and turn rates from noise, while the kinematic EKF applies Newtonian physical motion equations and error covariance tracking to filter residual outliers.

---

### Section E: Evaluation & Interpretation

#### 41. Which evaluation metric did you use and why?
**Answer:**  
Because this is a continuous inertial navigation regression problem, classification metrics (accuracy/F1) are inapplicable. We utilized:
1. **Mean Absolute Error (MAE) on Speed (m/s):** $\text{MAE}_v = \frac{1}{N}\sum |v_{true} - \hat{v}|$, providing an intuitive metric of speed accuracy.
2. **Mean Absolute Error (MAE) on Yaw Rate (deg/s):** Measuring heading change fidelity per second.
3. **Maximum & Final Position Drift (m) over Outage Duration ($T_{outage}$):**
   $$\text{Drift Error} = \sqrt{(p_E - \hat{p}_E)^2 + (p_N - \hat{p}_N)^2}$$
   Evaluating the real-world impact of dead reckoning drift over 30–60 second GNSS outages.
4. **Heteroscedastic Negative Log-Likelihood Loss (NLL):**
   $$\mathcal{L} = \frac{1}{2}\exp(-s)(y - \hat{y})^2 + \frac{1}{2}s \quad \text{where } s = \log \sigma^2$$
   Balancing prediction accuracy against calibrated uncertainty estimation.

#### 42. What is a confusion matrix?
**Answer:**  
A confusion matrix is an $N \times N$ table used to evaluate the performance of a classification model by comparing actual ground-truth classes against model predictions, categorizing results into True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN).

#### 43. Explain TP, TN, FP, and FN in your problem.
**Answer:**  
While velocity estimation is a continuous regression task, our **Stationary Detection / Zero Velocity Update (ZUPT) sub-module** performs binary classification:
* **True Positive (TP):** Vehicle is genuinely stopped (at a red light) and model correctly classifies it as stationary ($v = 0$), clamping gyro drift.
* **True Negative (TN):** Vehicle is cruising at 60 km/h and model correctly classifies it as in motion.
* **False Positive (FP - Dangerous):** Vehicle is driving at 50 km/h, but model mistakenly classifies it as stationary, zeroing EKF velocity and losing track.
* **False Negative (FN):** Vehicle is stationary, but model assumes it is creeping forward, allowing slight bias drift to accumulate.

#### 44. What is the difference between precision and recall?
**Answer:**  
* **Precision:** $\frac{TP}{TP + FP}$ — Out of all instances the model predicted as positive, how many were truly positive?
* **Recall:** $\frac{TP}{TP + FN}$ — Out of all actual positive instances, how many did the model correctly identify?

#### 45. When would recall be more important than precision?
**Answer:**  
In medical diagnosis (e.g., detecting cancer) or collision avoidance systems: missing a true condition (FN) is catastrophic, so high recall is prioritized even if it causes a few false alarms (lower precision).

#### 46. When would precision be more important than recall?
**Answer:**  
In spam filtering or **stationary ZUPT triggering in vehicular dead reckoning**: falsely predicting that a fast-moving vehicle is stationary (FP) completely zeros the navigation state at 60 km/h, corrupting position. Therefore, ZUPT classification requires near-100% precision.

#### 47. What is the F1-score?
**Answer:**  
The F1-score is the harmonic mean of precision and recall:
$$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
It provides a single balanced metric when there is an uneven class distribution and both false positives and false negatives carry significant costs.

#### 48. Why can accuracy be misleading for an imbalanced dataset?
**Answer:**  
If a dataset contains 99% driving frames and only 1% stationary frames (e.g., a continuous highway trajectory), a trivial model that always predicts "driving" achieves 99% accuracy while having 0% recall on stationary detection. It fails to identify the critical minority class completely.

#### 49. How did you compare different models?
**Answer:**  
We conducted comparative benchmarking across three paradigms:
1. **Pure Naive IMU Dead Reckoning (Baseline):** Raw double-integration of accelerometer and gyroscope without ML.
2. **Pure Deep Learning Model:** Directly integrating predicted velocity without Kalman filtering.
3. **Proposed AI-ML + EKF Sensor Fusion with Online Self-Correction (Full System):**  
*Benchmarking Metric:* We evaluated final positional drift after a simulated 30-second GNSS blackout:
* *Pure Naive IMU:* Drifts $> 120\text{ to } 200\text{ meters}$ rapidly into buildings due to uncompensated bias.
* *Proposed AI-ML + EKF Engine:* Constrains drift to under $10\text{ to } 15\text{ meters}$ ($> 85\%$ error reduction).

#### 50. If your model performs poorly after deployment, what would you investigate first?
**Answer:**  
We would execute a 4-step diagnostic root-cause protocol:
1. **Sensor Calibration & Unit Sanity:** Verify whether the smartphone's Sensor HAL delivers acceleration in m/s$^2$ vs. $g$, and verify the gyroscope axis coordinate convention (ISO 8855 body frame vs. Android device coordinate frame).
2. **Mounting Orientation Misalignment:** Check whether the phone was mounted with an unexpected pitch/roll angle causing severe gravity leakage into the longitudinal axis.
3. **Covariance Tuning ($Q$ and $R$ matrices in EKF):** Investigate if measurement noise covariance $R$ was over-confident, causing the filter to over-react to sensor noise rather than trusting kinematic propagation.
4. **Runtime Drift Calibrator Convergence:** Inspect `device_drift_profile.json` to verify if the online gradient descent converged on the hardware's scale factor ($S_v$) and gyro bias ($B_{yaw}$) during pre-outage GNSS availability.
