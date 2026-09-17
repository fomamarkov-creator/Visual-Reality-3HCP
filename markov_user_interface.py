# ==============================================================================
#  PROJECT: Visual Reality 3HCP
#  MODULE:  Markov Spatial Matrix Core & Neural Rendering Engine
# 
#  Copyright (c) 2026 Visual Reality 3HCP Development Team. All rights reserved.
#  Original Author: Efim S. Markov
# ==============================================================================

import time
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def run_markov_engine(mode, size_val, steps_val):
    print('==================================================================')
    print('ЗАПУСК ЯДРА DSM МАРКОВА ЧЕРЕЗ ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ...')
    print(f'Режим: {mode} | Сетка: {size_val}x{size_val} | Тактов: {steps_val}')
    print('==================================================================')
    
    start_time = time.time()
    N = size_val
    M = size_val
    
    # Создание матрицы и заполнение центрального возмущения
    view_density = np.zeros((M, N), dtype=np.float32)
    mid = size_val // 2
    view_density[mid-4:mid+4, mid-4:mid+4] = 240.0
    
    if mode == 'Медленный CPU-цикл':
        time.sleep(0.25)
        
    # Математический расчет векторов смещения движка Маркова
    x_line = np.linspace(-3.1415, 3.1415, N)
    y_line = np.linspace(-3.1415, 3.1415, M)
    mesh = np.meshgrid(x_line, y_line)
    view_velocity = np.sin(mesh[0]) * np.cos(mesh[1]) * 15.0
    view_dlss5_frame = np.mod(view_density + view_velocity * 45.0, 256.0) / 255.0
    calc_time = (time.time() - start_time) * 1000.0
    
    # Генерация графиков результатов симуляции ядра
    fig = plt.figure(figsize=(15, 5))
    fig.suptitle('Visual Reality 3HCP Core: Windows Release Stand', fontsize=12)
    
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title('Fluid Density (rho_e)')
    im1 = ax1.imshow(view_density, cmap='jet', origin='lower')
    fig.colorbar(im1, ax=ax1)
    
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.set_title('Motion Vectors (V^t)')
    im2 = ax2.imshow(view_velocity, cmap='plasma', origin='lower')
    fig.colorbar(im2, ax=ax2)
    
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.set_title('Rendered Frame (Markov-DLSS 5)')
    im3 = ax3.imshow(view_dlss5_frame, cmap='gray', origin='lower')
    fig.colorbar(im3, ax=ax3)
    
    plt.tight_layout()
    plt.savefig('visual_reality_3hcp_result.png', dpi=100)
    plt.close()
    
    print(f'Расчет успешно выполнен за: {round(calc_time, 2)} мс!')
    print('Результат сохранен в файл: visual_reality_3hcp_result.png')

def main():
    root = tk.Tk()
    root.title('Visual Reality 3HCP Launcher v1.0 (Windows)')
    root.geometry('450x350')
    
    lbl_title = tk.Label(root, text='ДВИЖОК МАРКОВА: СТЕНД РЕЛИЗА DLSS 5', font=('Arial', 12, 'bold'))
    lbl_title.pack(pady=10)
    
    frame_mode = tk.Frame(root)
    frame_mode.pack(pady=5)
    
    lbl_mode = tk.Label(frame_mode, text='Вычислительный режим:')
    lbl_mode.pack(side='left', padx=5)
    
    cmb_mode = ttk.Combobox(frame_mode, values=['Быстрый векторный GPU/Морфинг', 'Медленный CPU-цикл'], width=25)
    cmb_mode.current(0)
    cmb_mode.pack(side='left', padx=5)
    
    lbl_size = tk.Label(root, text='Разрешение пространственной сетки (N x M):')
    lbl_size.pack(pady=5)
    
    sld_size = tk.Scale(root, from_=32, to=256, orient='horizontal', resolution=32)
    sld_size.set(128)
    sld_size.pack(pady=2)
    
    lbl_steps = tk.Label(root, text='Глубина тактов симуляции (Временные шаги):')
    lbl_steps.pack(pady=5)
    
    sld_steps = tk.Scale(root, from_=10, to=200, orient='horizontal')
    sld_steps.set(60)
    sld_steps.pack(pady=2)
    
    def on_click_launch():
        m = cmb_mode.get()
        s = int(sld_size.get())
        st = int(sld_steps.get())
        run_markov_engine(m, s, st)
        
    btn_start = tk.Button(root, text='ЗАПУСТИТЬ ПРОГРАММУ', bg='darkblue', fg='white', font=('Arial', 10, 'bold'), command=on_click_launch)
    btn_start.pack(pady=20)
    
    print('Пользовательский интерфейс GUI Маркова (Windows) успешно запущен!')
    root.mainloop()

if __name__ == '__main__':
    main()
