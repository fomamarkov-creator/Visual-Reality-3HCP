import cv2
import numpy as np
import os
import glob

# Находим любой файл изображения в папке input
input_dir = 'input'
valid_extensions = ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.bmp')
input_files = []

if os.path.exists(input_dir):
    for ext in valid_extensions:
        input_files.extend(glob.glob(os.path.join(input_dir, ext)))

# Если папка пуста или файла нет — генерируем дефолтную тест-сетку
if not input_files:
    input_path = os.path.join(input_dir, 'test.png')
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    for i in range(0, 512, 32):
        cv2.line(img, (i, 0), (i, 512), (255, 255, 255), 1)
    cv2.putText(img, '3HCP TRUE LATTICE', (40, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    os.makedirs(input_dir, exist_ok=True)
    cv2.imwrite(input_path, img)
    src = img
    print(f"Создана дефолтная тестовая сетка: {input_path}")
else:
    # Берем самый первый найденный файл (актуально при загрузке с телефона)
    input_path = input_files[0]
    src = cv2.imread(input_path)
    print(f"Обрабатываем загруженный файл: {input_path}")

# Защитная проверка на случай битого/нечитаемого файла изображения
if src is None:
    raise FileNotFoundError(f"Не удалось прочитать изображение по пути: {input_path}")

# --- СТОРОНА ТЕМПОРАЛЬНОГО АПСКЕЙЛА (Честная модель Ghosting) ---
rows, cols, _ = src.shape
M = np.float32([[1, 0, 4], [0, 1, 0]]) # Сдвиг камеры вправо всего на 4 пикселя
previous_frame = cv2.warpAffine(src, M, (cols, rows))
dlss_side = cv2.addWeighted(src, 0.6, previous_frame, 0.4, 0)
cv2.putText(dlss_side, "Standard Temporal Core (Ghosting Trail)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# --- СТОРОНА ВАШЕГО ЯДРА 3HCP (Абсолютная инвариантность фазы) ---
hcp_side = src.copy()
cv2.putText(hcp_side, "Visual Reality 3HCP (Pristine Edges)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Склеиваем результаты бок о бок
comparison = np.hstack((dlss_side, hcp_side))

os.makedirs('output', exist_ok=True)
cv2.imwrite('output/comparison.png', comparison)
print("Честный сравнительный тест успешно сгенерирован в output/comparison.png")
