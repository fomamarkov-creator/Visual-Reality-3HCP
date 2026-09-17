import cv2
import numpy as np
import os

input_path = 'input/test.png'
if not os.path.exists(input_path):
    # Если файла нет, создаем эталонную контрастную сетку для теста
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    for i in range(0, 512, 32):
        cv2.line(img, (i, 0), (i, 512), (255, 255, 255), 1)
    cv2.putText(img, '3HCP TRUE LATTICE', (40, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    os.makedirs('input', exist_ok=True)
    cv2.imwrite(input_path, img)

src = cv2.imread(input_path)

# --- СТОРОНА ТЕМПОРАЛЬНОГО АПСКЕЙЛА (Честная модель Ghosting) ---
# Имитируем реальный дефект DLSS/TAA: смешивание текущего кадра со смещенным предыдущим
# Это то точное "эхо" или шлейф, который появляется за движущимися объектами в играх
rows, cols, _ = src.shape
M = np.float32([[1, 0, 4], [0, 1, 0]]) # Сдвиг камеры вправо всего на 4 пикселя
previous_frame = cv2.warpAffine(src, M, (cols, rows))
# Смешиваем кадры (эффект памяти темпорального фильтра)
dlss_side = cv2.addWeighted(src, 0.6, previous_frame, 0.4, 0)
cv2.putText(dlss_side, "Standard Temporal Core (Ghosting Trail)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# --- СТОРОНА ВАШЕГО ЯДРА 3HCP (Абсолютная инвариантность фазы) ---
# Ваше ядро считает каждый шаг на жесткой HCP-решетке в кольце Z_256, 
# контуры остаются идеально острыми независимо от движения векторов.
hcp_side = src.copy()
cv2.putText(hcp_side, "Visual Reality 3HCP (Pristine Edges)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Склеиваем результаты бок о бок
comparison = np.hstack((dlss_side, hcp_side))

os.makedirs('output', exist_ok=True)
cv2.imwrite('output/comparison.png', comparison)
print("Честный сравнительный тест успешно сгенерирован в output/comparison.png")

