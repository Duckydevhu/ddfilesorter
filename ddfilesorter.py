import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import json
import os
import shutil
from datetime import datetime

# Főablak létrehozása
root = tk.Tk()
root.title("Fájlrendszerező")
root.geometry("800x450")

# Ikon beállítása
try:
    if os.path.exists("icon.ico"):
        root.iconbitmap("icon.ico")
    elif os.path.exists("icon.png"):
        logo = tk.PhotoImage(file="icon.png")
        root.iconphoto(False, logo)
except tk.TclError:
    print("Nem sikerült betölteni az ikont.")
    # Ezen a ponton az alkalmazás tovább fut, csak ikon nélkül

# Konfigurációs fájl neve
CONFIG_FILE = "config.json"

# Változók a könyvtárakhoz
input_dir = tk.StringVar()
output_dir = tk.StringVar()
extensions_str = tk.StringVar()
date_selection_type = tk.StringVar(value="mtime")
dates_str = tk.StringVar()
size_unit = tk.StringVar(value="kb")
sizes_str = tk.StringVar()
case_sensitive = tk.BooleanVar(value=False)
names_str = tk.StringVar()

def select_input_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_dir.set(directory)

def select_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_dir.set(directory)

def save_config():
    config = {
        "input_directory": input_dir.get(),
        "output_directory": output_dir.get(),
        "extensions": extensions_str.get(),
        "date_selection_type": date_selection_type.get(),
        "dates": dates_str.get(),
        "size_unit": size_unit.get(),
        "sizes": sizes_str.get(),
        "case_sensitive": case_sensitive.get(),
        "names": names_str.get()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                input_dir.set(config.get("input_directory", ""))
                output_dir.set(config.get("output_directory", ""))
                extensions_str.set(config.get("extensions", ""))
                date_selection_type.set(config.get("date_selection_type", "mtime"))
                dates_str.set(config.get("dates", ""))
                size_unit.set(config.get("size_unit", "kb"))
                sizes_str.set(config.get("sizes", ""))
                case_sensitive.set(config.get("case_sensitive", False))
                names_str.set(config.get("names", ""))
        except json.JSONDecodeError:
            messagebox.showerror("Hiba", "Hiba a konfigurációs fájl betöltésekor.")

def on_closing():
    save_config()
    root.destroy()

# ----------------- Rendezés funkciók -----------------

def organize_by_extension():
    # ... (A kód többi része változatlan) ...
    input_path = input_dir.get()
    output_path = output_dir.get()
    extensions_raw = extensions_str.get()

    if not input_path or not os.path.isdir(input_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes bemeneti könyvtárat!")
        return
    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes kimeneti könyvtárat!")
        return

    groups = []
    current_group_str = ""
    in_group = False
    
    for char in extensions_raw:
        if char == '(':
            if in_group:
                messagebox.showerror("Hiba", "Érvénytelen kiterjesztés formátum. Egymásba ágyazott zárójelek nem megengedettek.")
                return
            in_group = True
            current_group_str = ""
        elif char == ')':
            if not in_group:
                messagebox.showerror("Hiba", "Érvénytelen kiterjesztés formátum. Nyitó zárójel nélkül.")
                return
            group_extensions = [ext.strip().lstrip('.').lower() for ext in current_group_str.split(',') if ext.strip()]
            if not group_extensions:
                messagebox.showerror("Hiba", "Egy csoport nem lehet üres.")
                return
            
            if len(group_extensions) > 1:
                group_name = '_'.join(group_extensions)
            else:
                group_name = group_extensions[0]
            
            groups.append({'name': group_name, 'extensions': group_extensions})
            in_group = False
            current_group_str = ""
        elif in_group:
            current_group_str += char
        elif char not in ' ,':
            if char == '*':
                groups.append({'name': 'egyeb', 'extensions': ['*']})
            else:
                ext = char.strip().lstrip('.').lower()
                groups.append({'name': ext, 'extensions': [ext]})
    
    if in_group:
        messagebox.showerror("Hiba", "Hiányzó záró zárójel.")
        return
    if not groups:
        messagebox.showerror("Hiba", "Kérlek adj meg legalább egy kiterjesztést vagy csoportot!")
        return

    for group in groups:
        dir_path = os.path.join(output_path, group['name'])
        os.makedirs(dir_path, exist_ok=True)

    moved_files_count = 0
    files_to_process = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

    for group in groups:
        for filename in list(files_to_process):
            src_path = os.path.join(input_path, filename)
            file_ext = os.path.splitext(filename)[1].lstrip('.').lower()
            
            if '*' in group['extensions']:
                is_moved = False
                for other_group in groups:
                    if '*' not in other_group['extensions'] and file_ext in other_group['extensions']:
                        is_moved = True
                        break
                
                if not is_moved:
                    dest_dir = os.path.join(output_path, group['name'])
                    dest_path = os.path.join(dest_dir, filename)
                    shutil.move(src_path, dest_path)
                    moved_files_count += 1
                    files_to_process.remove(filename)

            elif file_ext in group['extensions']:
                dest_dir = os.path.join(output_path, group['name'])
                dest_path = os.path.join(dest_dir, filename)
                shutil.move(src_path, dest_path)
                moved_files_count += 1
                files_to_process.remove(filename)
    
    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            try:
                os.rmdir(item_path)
            except OSError as e:
                print(f"Hiba az üres mappa törlésekor: {item_path} - {e}")

    messagebox.showinfo("Rendezés kész", f"A rendezés sikeresen befejeződött! Áthelyezett fájlok száma: {moved_files_count}")

def organize_by_date():
    # ... (A kód többi része változatlan) ...
    input_path = input_dir.get()
    output_path = output_dir.get()
    dates_raw = dates_str.get()
    date_type = date_selection_type.get()
    
    if not input_path or not os.path.isdir(input_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes bemeneti könyvtárat!")
        return
    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes kimeneti könyvtárat!")
        return
    if not dates_raw:
        messagebox.showerror("Hiba", "Kérlek adj meg legalább egy dátumot vagy intervallumot!")
        return

    conditions = [cond.strip().replace(" ", "") for cond in dates_raw.split(',') if cond.strip()]
    date_format = "%Y.%m.%d"
    moved_files_count = 0
    files_to_process = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

    for cond in conditions:
        if '-' in cond:
            start_date_str, end_date_str = cond.split('-', 1)
            try:
                start_date = datetime.strptime(start_date_str, date_format) if start_date_str else None
                end_date = datetime.strptime(end_date_str, date_format) if end_date_str else None
            except ValueError:
                messagebox.showerror("Hiba", f"Érvénytelen dátum formátum: {cond}. Használd a YYYY.MM.DD formátumot.")
                return

            folder_name = cond.replace('.', '_')
            dest_dir = os.path.join(output_path, folder_name)
            os.makedirs(dest_dir, exist_ok=True)
            
            for filename in list(files_to_process):
                src_path = os.path.join(input_path, filename)
                try:
                    timestamp = os.path.getmtime(src_path) if date_type == "mtime" else os.path.getctime(src_path)
                    file_date = datetime.fromtimestamp(timestamp).replace(hour=0, minute=0, second=0, microsecond=0)
                except OSError:
                    continue

                is_match = False
                if start_date and not end_date:
                    is_match = file_date >= start_date
                elif not start_date and end_date:
                    is_match = file_date < end_date
                elif start_date and end_date:
                    is_match = start_date <= file_date < end_date
                
                if is_match:
                    shutil.move(src_path, os.path.join(dest_dir, filename))
                    moved_files_count += 1
                    files_to_process.remove(filename)
        
        else:
            try:
                exact_date = datetime.strptime(cond, date_format)
            except ValueError:
                messagebox.showerror("Hiba", f"Érvénytelen dátum formátum: {cond}. Használd a YYYY.MM.DD formátumot.")
                return

            folder_name = cond.replace('.', '_')
            dest_dir = os.path.join(output_path, folder_name)
            os.makedirs(dest_dir, exist_ok=True)
            
            for filename in list(files_to_process):
                src_path = os.path.join(input_path, filename)
                try:
                    timestamp = os.path.getmtime(src_path) if date_type == "mtime" else os.path.getctime(src_path)
                    file_date = datetime.fromtimestamp(timestamp).replace(hour=0, minute=0, second=0, microsecond=0)
                except OSError:
                    continue
                
                if file_date == exact_date:
                    shutil.move(src_path, os.path.join(dest_dir, filename))
                    moved_files_count += 1
                    files_to_process.remove(filename)

    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            try:
                os.rmdir(item_path)
            except OSError:
                pass

    messagebox.showinfo("Rendezés kész", f"A rendezés sikeresen befejeződött! Áthelyezett fájlok száma: {moved_files_count}")

def organize_by_size():
    # ... (A kód többi része változatlan) ...
    input_path = input_dir.get()
    output_path = output_dir.get()
    sizes_raw = sizes_str.get()
    unit = size_unit.get()
    
    if not input_path or not os.path.isdir(input_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes bemeneti könyvtárat!")
        return
    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes kimeneti könyvtárat!")
        return
    if not sizes_raw:
        messagebox.showerror("Hiba", "Kérlek adj meg legalább egy méretet vagy intervallumot!")
        return

    unit_factor = 1
    if unit == 'kb':
        unit_factor = 1024
    elif unit == 'mb':
        unit_factor = 1024 * 1024
    elif unit == 'gb':
        unit_factor = 1024 * 1024 * 1024

    conditions = [cond.strip().replace(" ", "") for cond in sizes_raw.split(',') if cond.strip()]
    moved_files_count = 0
    files_to_process = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

    for cond in conditions:
        folder_name = cond.replace('-', '_')
        dest_dir = os.path.join(output_path, folder_name + unit)
        os.makedirs(dest_dir, exist_ok=True)
        
        if '-' in cond:
            start_str, end_str = cond.split('-', 1)
            try:
                start_size = int(start_str) * unit_factor if start_str else None
                end_size = int(end_str) * unit_factor if end_str else None
            except ValueError:
                messagebox.showerror("Hiba", "A méretnek egész számnak kell lennie!")
                return
            
            for filename in list(files_to_process):
                src_path = os.path.join(input_path, filename)
                try:
                    file_size = os.path.getsize(src_path)
                except OSError:
                    continue
                
                is_match = False
                if start_size is not None and end_size is None:
                    is_match = file_size >= start_size
                elif start_size is None and end_size is not None:
                    is_match = file_size < end_size
                elif start_size is not None and end_size is not None:
                    is_match = start_size <= file_size < end_size
                
                if is_match:
                    shutil.move(src_path, os.path.join(dest_dir, filename))
                    moved_files_count += 1
                    files_to_process.remove(filename)

        else:
            try:
                exact_size = int(cond) * unit_factor
            except ValueError:
                messagebox.showerror("Hiba", "A méretnek egész számnak kell lennie!")
                return

            for filename in list(files_to_process):
                src_path = os.path.join(input_path, filename)
                try:
                    file_size = os.path.getsize(src_path)
                except OSError:
                    continue
                
                if file_size == exact_size:
                    shutil.move(src_path, os.path.join(dest_dir, filename))
                    moved_files_count += 1
                    files_to_process.remove(filename)

    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            try:
                os.rmdir(item_path)
            except OSError:
                pass

    messagebox.showinfo("Rendezés kész", f"A rendezés sikeresen befejeződött! Áthelyezett fájlok száma: {moved_files_count}")

def organize_by_name():
    # ... (A kód többi része változatlan) ...
    input_path = input_dir.get()
    output_path = output_dir.get()
    names_raw = names_str.get()
    case_sensitive_val = case_sensitive.get()

    if not input_path or not os.path.isdir(input_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes bemeneti könyvtárat!")
        return
    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("Hiba", "Kérlek válassz egy érvényes kimeneti könyvtárat!")
        return
    if not names_raw:
        messagebox.showerror("Hiba", "Kérlek adj meg legalább egy keresési mintát!")
        return

    patterns = [p.strip() for p in names_raw.split(',') if p.strip()]
    moved_files_count = 0
    files_to_process = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

    for pattern in patterns:
        folder_name = pattern.replace('!', '').replace('*', '_').replace('__', '_')
        dest_dir = os.path.join(output_path, folder_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        negation = pattern.startswith('!')
        search_pattern = pattern.lstrip('!')
        
        starts_with = search_pattern.endswith('*') and not search_pattern.startswith('*')
        ends_with = search_pattern.startswith('*') and not search_pattern.endswith('*')
        contains = search_pattern.startswith('*') and search_pattern.endswith('*')
        
        search_text = search_pattern.strip('*')

        for filename in list(files_to_process):
            file_to_check = filename
            if not case_sensitive_val:
                file_to_check = filename.lower()
                search_text_lower = search_text.lower()
            else:
                search_text_lower = search_text
            
            is_match = False
            if starts_with and file_to_check.startswith(search_text_lower):
                is_match = True
            elif ends_with and file_to_check.endswith(search_text_lower):
                is_match = True
            elif contains and search_text_lower in file_to_check:
                is_match = True
            elif not starts_with and not ends_with and not contains and file_to_check == search_text_lower:
                is_match = True

            if negation:
                is_match = not is_match
            
            if is_match:
                src_path = os.path.join(input_path, filename)
                shutil.move(src_path, os.path.join(dest_dir, filename))
                moved_files_count += 1
                files_to_process.remove(filename)
    
    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            try:
                os.rmdir(item_path)
            except OSError:
                pass

    messagebox.showinfo("Rendezés kész", f"A rendezés sikeresen befejeződött! Áthelyezett fájlok száma: {moved_files_count}")

# ----------------- Felület elrendezése -----------------

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

directory_frame = tk.Frame(main_frame)
directory_frame.pack(fill=tk.X, pady=(0, 10))
tk.Label(directory_frame, text="Bemeneti könyvtár:", anchor="w").grid(row=0, column=0, sticky="w", pady=2)
tk.Entry(directory_frame, textvariable=input_dir, state="readonly").grid(row=1, column=0, sticky="ew", padx=(0, 5))
tk.Button(directory_frame, text="Választás", command=select_input_directory).grid(row=1, column=1)
tk.Label(directory_frame, text="Kimeneti könyvtár:", anchor="w").grid(row=2, column=0, sticky="w", pady=2)
tk.Entry(directory_frame, textvariable=output_dir, state="readonly").grid(row=3, column=0, sticky="ew", padx=(0, 5))
tk.Button(directory_frame, text="Választás", command=select_output_directory).grid(row=3, column=1)
directory_frame.grid_columnconfigure(0, weight=1)

notebook = ttk.Notebook(main_frame)
notebook.pack(fill=tk.BOTH, expand=True, pady=10)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Rendezés kiterjesztés szerint")
tk.Label(tab1, text="Add meg a kiterjesztéseket (pl. jpg, png, (bmp, gif)):").pack(anchor="w", padx=10, pady=(10, 5))
tk.Entry(tab1, textvariable=extensions_str).pack(fill=tk.X, padx=10)

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Rendezés dátum szerint")
radio_frame_date = tk.Frame(tab2)
radio_frame_date.pack(anchor="w", padx=10, pady=(10, 0))
tk.Label(radio_frame_date, text="Figyelt dátumtípus:").pack(side=tk.LEFT)
tk.Radiobutton(radio_frame_date, text="Létrehozás", variable=date_selection_type, value="ctime").pack(side=tk.LEFT, padx=(10, 0))
tk.Radiobutton(radio_frame_date, text="Módosítás", variable=date_selection_type, value="mtime").pack(side=tk.LEFT)
tk.Label(tab2, text="Add meg a dátumokat és intervallumokat (pl. 2025.01.01, 2025.02.01-2025.03.01):").pack(anchor="w", padx=10, pady=(10, 5))
tk.Entry(tab2, textvariable=dates_str).pack(fill=tk.X, padx=10)

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Rendezés méret szerint")
radio_frame_size = tk.Frame(tab3)
radio_frame_size.pack(anchor="w", padx=10, pady=(10, 0))
tk.Label(radio_frame_size, text="Mértékegység:").pack(side=tk.LEFT)
tk.Radiobutton(radio_frame_size, text="KB", variable=size_unit, value="kb").pack(side=tk.LEFT, padx=(10, 0))
tk.Radiobutton(radio_frame_size, text="MB", variable=size_unit, value="mb").pack(side=tk.LEFT)
tk.Radiobutton(radio_frame_size, text="GB", variable=size_unit, value="gb").pack(side=tk.LEFT)
tk.Label(tab3, text="Add meg a méreteket és intervallumokat (pl. -500, 500-1000, 1000-):").pack(anchor="w", padx=10, pady=(10, 5))
tk.Entry(tab3, textvariable=sizes_str).pack(fill=tk.X, padx=10)

tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Rendezés fájlnév szerint")
case_check_frame = tk.Frame(tab4)
case_check_frame.pack(anchor="w", padx=10, pady=(10, 0))
tk.Checkbutton(case_check_frame, text="Kisbetű/nagybetű érzékeny", variable=case_sensitive).pack(side=tk.LEFT)
tk.Label(tab4, text="Add meg a keresési mintákat (pl. abc*, !*abc*, *xyz):").pack(anchor="w", padx=10, pady=(10, 5))
tk.Entry(tab4, textvariable=names_str).pack(fill=tk.X, padx=10)

def start_sort():
    selected_tab_id = notebook.select()
    selected_tab_text = notebook.tab(selected_tab_id, "text")
    if selected_tab_text == "Rendezés kiterjesztés szerint":
        organize_by_extension()
    elif selected_tab_text == "Rendezés dátum szerint":
        organize_by_date()
    elif selected_tab_text == "Rendezés méret szerint":
        organize_by_size()
    elif selected_tab_text == "Rendezés fájlnév szerint":
        organize_by_name()

sort_button_frame = tk.Frame(main_frame)
sort_button_frame.pack(fill=tk.X, pady=(10, 0))
tk.Button(sort_button_frame, text="Rendezés", command=start_sort).pack(side=tk.RIGHT)

load_config()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()