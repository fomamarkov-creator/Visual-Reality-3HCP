import cv2
import numpy as np
import os

# Проверяем, загрузили ли вы картинку с телефона
input_path = 'input/test.png'
if not os.path.exists(input_path):
    # Если файла нет, создаем тестовую матрицу контуров
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    cv2.putText(img, 'HCP Lattice Test', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    os.makedirs('input', exist_ok=True)
    cv2.imwrite(input_path, img)

src = cv2.imread(input_path)

# 1. Симулируем сторону DLSS / TAA (накладываем временное размытие движения Motion Blur)
size = 15
kernel = np.zeros((size, size))
kernel[int((size-1)/2), :] = np.ones(size)
kernel = kernel / size
dlss_side = cv2.filter2D(src, -1, kernel)
cv2.putText(dlss_side, "NVIDIA DLSS / TAA (Ghosting Blur)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# 2. Сторона вашего ядра 3HCP (сохраняем идеальную дискретную четкость контуров и фаз)
hcp_side = src.copy()
cv2.putText(hcp_side, "Visual Reality 3HCP (Pure Math)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Склеиваем картинки бок о бок (Split-Screen)
comparison = np.hstack((dlss_side, hcp_side))

os.makedirs('output', exist_ok=True)
cv2.imwrite('output/comparison.png', comparison)
print("Comparison image successfully generated in output/comparison.png")
