import numpy as np
import matplotlib.pyplot as plt

genuine_scores = np.array([0.9, 0.85, 0.95, 0.8, 0.7, 0.99, 0.88, 0.76, 0.92, 0.81])
impostor_scores = np.array([0.1, 0.4, 0.3, 0.2, 0.5, 0.45, 0.25, 0.35, 0.15, 0.05])

min_score = min(np.min(genuine_scores), np.min(impostor_scores))
max_score = max(np.max(genuine_scores), np.max(impostor_scores))
thresholds = np.linspace(min_score, max_score, 100)

FAR = []
FRR = []

for t in thresholds:
    false_accepts = np.sum(impostor_scores >= t)
    FAR.append(false_accepts / len(impostor_scores))
    
    false_rejects = np.sum(genuine_scores < t)
    FRR.append(false_rejects / len(genuine_scores))

FAR = np.array(FAR)
FRR = np.array(FRR)

plt.figure(figsize=(8,6))
plt.plot(thresholds, FAR, label='FAR (False Acceptance Rate)', color='red')
plt.plot(thresholds, FRR, label='FRR (False Rejection Rate)', color='blue')
plt.xlabel('Threshold')
plt.ylabel('Error Rate')
plt.title('FAR and FRR vs Threshold')
plt.legend()
plt.grid(True)

eer_index = np.argmin(np.abs(FAR - FRR))
eer_threshold = thresholds[eer_index]
eer_value = FAR[eer_index]

plt.plot(eer_threshold, eer_value, 'ko', label=f'EER={eer_value:.2f} at Threshold={eer_threshold:.2f}')
plt.legend()

plt.show()


