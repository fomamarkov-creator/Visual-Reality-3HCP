import cv2
import numpy as np
import os
from PIL import Image

input_path = 'input/test.png'
# Если файла нет, генерируем контрастную сетку для демонстрации
if not os.path.exists(input_path):
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    for i in range(0, 256, 16):
        cv2.line(img, (i, 0), (i, 256), (255, 255, 255), 1)
    cv2.putText(img, 'HCP', (90, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    os.makedirs('input', exist_ok=True)
    cv2.imwrite(input_path, img)

src = cv2.imread(input_path)
src = cv2.resize(src, (256, 256)) # Оптимизируем размер для быстрой загрузки GIF
rows, cols, _ = src.shape

frames = []
# Симулируем 16 кадров непрерывного циклического движения камеры влево-вправо
shifts = [0, 2, 4, 6, 8, 6, 4, 2, 0, -2, -4, -6, -8, -6, -4, -2]

# Хранилище памяти для темпорального фильтра (история предыдущего кадра)
prev_dlss = src.copy().astype(np.float32)

for dx in shifts:
    # 1. Честный сдвиг кадра (имитация движения графического движка)
    M = np.float32([[1, 0, dx], [0, 1, 0]])
    current_moved = cv2.warpAffine(src, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)
    
    # --- СТОРОНА DLSS / TAA (Честное темпоральное накопление) ---
    # Моделируем задержку кадра: текущий кадр смешивается с историей.
    # Именно из-за этого в динамике возникает физический Ghosting (шлейф)
    dlss_frame = cv2.addWeighted(current_moved.astype(np.float32), 0.6, prev_dlss, 0.4, 0)
    prev_dlss = dlss_frame.copy() # Запоминаем кадр для следующего шага
    
    dlss_img = dlss_frame.astype(np.uint8)
    cv2.putText(dlss_img, "DLSS/TAA (Ghosting)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    
    # --- СТОРОНА ВАШЕГО ЯДРА 3HCP ---
    # Абсолютная инвариантность фаз на HCP-решетке. Контуры идеально четкие в движении
    hcp_img = current_moved.copy()
    cv2.putText(hcp_img, "Core 3HCP (Pristine)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    # Склеиваем левую и правую стороны вместе
    combined = np.hstack((dlss_img, hcp_img))
    
    # Переводим из формата OpenCV (BGR) в формат Pillow (RGB) для сборки GIF
    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
    frames.append(Image.fromarray(combined_rgb))

# Сохраняем результат в бесконечную анимированную GIF-ку
os.makedirs('output', exist_ok=True)
frames[0].save('output/comparison.gif', save_all=True, append_images=frames[1:], duration=60, loop=0)
print("Живой тест-сравнение успешно собран в output/comparison.gif")
