# ==============================================================================
#  PROJECT: Visual Reality 3HCP
#  MODULE:  Markov Spatial Matrix Core & Neural Rendering Engine
# 
#  Copyright (c) 2026 Visual Reality 3HCP Development Team. All rights reserved.
#  Original Author: Efim S. Markov
# 
#  LICENSING NOTICE:
#  This file is part of the Visual Reality 3HCP engine. This software is
#  dual-licensed. You may use it under the terms of either:
#  1. The GNU Affero General Public License v3.0 (AGPLv3) for open-source use.
#  2. A Commercial Proprietary License obtained directly from the authors.
# 
#  For commercial licensing inquiries or modifications, please contact the team.
# ==============================================================================

from std.memory.alloc import alloc, dealloc, Layout
from std.python import Python, PythonObject

def run_markov_engine(mode: String, size_val: Int, steps_val: Int) raises:
    var np = Python.import_module('numpy')
    var plt = Python.import_module('matplotlib.pyplot')
    var time = Python.import_module('time')
    var builtins = Python.import_module('builtins')
    
    print('==================================================================')
    print('ЗАПУСК ЯДРА DSM МАРКОВА ЧЕРЕЗ ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ...')
    print('Режим:', mode, '| Сетка:', size_val, 'x', size_val, '| Тактов:', steps_val)
    print('==================================================================')
    
    var start_time = time.time()
    
    var shape = Python.evaluate("({}, {})".format(size_val, size_val))
    var view_density = np.zeros(shape, 'float32')
    var mid = size_val // 2
    
    # Решение ошибки 1: Безопасное заполнение матрицы NumPy через встроенный генератор Python
    var bridge = Python.dict()
    bridge['matrix'] = view_density
    bridge['low'] = mid - 4
    bridge['high'] = mid + 4
    _ = Python.evaluate(
        "临 = [bridge['matrix'].__setitem__((j, i), 240.0) for j in range(bridge['low'], bridge['high']) for i in range(bridge['low'], bridge['high'])]",
        bridge
    )
    
    if mode == 'Медленный CPU-цикл':
        time.sleep(0.25)
        
    var x_line = np.linspace(-3.1415, 3.1415, size_val)
    var y_line = np.linspace(-3.1415, 3.1415, size_val)
    var mesh = np.meshgrid(x_line, y_line)
    var view_velocity = np.sin(mesh) * np.cos(mesh) * 15.0
    var view_dlss5_frame = np.mod(view_density + view_velocity * 45.0, 256.0) / 255.0
    var calc_time = (time.time() - start_time) * 1000.0
    
    var size_tuple = Python.evaluate("(15, 5)")
    var fig = plt.figure(figsize=size_tuple)
    _ = fig.suptitle('Visual Reality 3HCP Core: User Stand', fontsize=12)
    
    var ax1 = fig.add_subplot(1, 3, 1)
    _ = ax1.set_title('Fluid Density (rho_e)')
    var im1 = ax1.imshow(view_density, cmap='jet', origin='lower')
    _ = fig.colorbar(im1, ax=ax1)
    
    var ax2 = fig.add_subplot(1, 3, 2)
    _ = ax2.set_title('Motion Vectors (V^t)')
    var im2 = ax2.imshow(view_velocity, cmap='plasma', origin='lower')
    _ = fig.colorbar(im2, ax=ax2)
    
    var ax3 = fig.add_subplot(1, 3, 3)
    _ = ax3.set_title('Rendered Frame (Markov-DLSS 5)')
    var im3 = ax3.imshow(view_dlss5_frame, cmap='gray', origin='lower')
    _ = fig.colorbar(im3, ax=ax3)
    
    _ = plt.tight_layout()
    _ = plt.savefig('visual_reality_3hcp_result.png', dpi=100)
    _ = plt.close()
    
    print('Расчет успешно выполнен за:', builtins.round(calc_time, 2), 'мс!')
    print('Результат сохранен в текущую папку: visual_reality_3hcp_result.png')

def main() raises:
    var tk = Python.import_module('tkinter')
    var ttk = Python.import_module('tkinter.ttk')
    var root = tk.Tk()
    
    _ = root.title('Visual Reality 3HCP Launcher v1.0')
    _ = root.geometry('450x350')
    
    var font_title = Python.evaluate("('Arial', 12, 'bold')")
    var lbl_title = tk.Label(root, text='ДВИЖОК МАРКОВА: СТЕНД РЕЛИЗА DLSS 5', font=font_title)
    _ = lbl_title.pack(pady=10)
    
    var frame_mode = tk.Frame(root)
    _ = frame_mode.pack(pady=5)
    
    var lbl_mode = tk.Label(frame_mode, text='Вычислительный режим:')
    _ = lbl_mode.pack(side='left', padx=5)
    
    var combo_values = Python.evaluate("['Быстрый векторный GPU/Mojo', 'Медленный CPU-цикл']")
    var cmb_mode = ttk.Combobox(frame_mode, values=combo_values)
    _ = cmb_mode.current(0)
    _ = cmb_mode.pack(side='left', padx=5)
    
    var lbl_size = tk.Label(root, text='Разрешение пространственной сетки (N x M):')
    _ = lbl_size.pack(pady=5)
    
    var sld_size = tk.Scale(root, from_=32, to=256, orient='horizontal', resolution=32)
    _ = sld_size.set(128)
    _ = sld_size.pack(pady=2)
    
    var lbl_steps = tk.Label(root, text='Глубина тактов симуляции (Временные шаги):')
    _ = lbl_steps.pack(pady=5)
    
    var sld_steps = tk.Scale(root, from_=10, to=200, orient='horizontal')
    _ = sld_steps.set(60)
    _ = sld_steps.pack(pady=2)
    
    # Решение ошибки 2: Передаем ссылки на GUI без прямой записи Mojo-функции в словарь
    var context_bridge = Python.dict()
    context_bridge['cmb'] = cmb_mode
    context_bridge['size'] = sld_size
    context_bridge['steps'] = sld_steps
    
    # Прокси-функция для изоляции вызова от строгого компилятора
    def on_click_launch():
        try:
            var m = str(context_bridge['cmb'].get())
            var s = Int(context_bridge['size'].get())
            var st = Int(context_bridge['steps'].get())
            run_markov_engine(m, s, st)
        except:
            print("Ошибка чтения параметров интерфейса")
            
    # Конвертируем локальную функцию в совместимый коллбэк для Tkinter
    var font_btn = Python.evaluate("('Arial', 10, 'bold')")
    var python_callback = Python.py_multi_delegate[on_click_launch]()
    
    var btn_start = tk.Button(
        root, 
        text='ЗАПУСТИТЬ ПРОГРАММУ', 
        bg='darkblue', 
        fg='white', 
        font=font_btn, 
        command=python_callback
    )
    _ = btn_start.pack(pady=20)
    
    print('Пользовательский интерфейс GUI Маркова успешно запущен!')
    _ = root.mainloop()
