import tkinter as tk
from zipfile import ZipFile
import os
import yaml
import platform

current_directory = ""
permissions = {}

def open_yaml():
    try:
        with open('C://Users/user/Desktop/МИРЭА/Конфигурационное управление/Домашнее задание №1/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            archive_path = config['virtual_filesystem']['archive_path']
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования: {e}")
    except FileNotFoundError:
        print("Файл не найден. Проверьте путь.")
    except KeyError:
        print("Ключ 'virtual_filesystem' или 'archive_path' отсутствует в конфигурации.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return archive_path

def command(cmd=None):
    global current_directory
    
    if cmd:
        command = cmd
    else:
        command = input_area.get("1.0", tk.END)[:-1]


    #write(archive_path + '/files.zip/' + current_directory + ' ' + command)

    if command == "ls": 
        with ZipFile("files.zip", "a") as myzip:
            return ls([name for name in myzip.namelist() if name.startswith(current_directory)])
    elif command == "exit": 
        exit()
    elif command.startswith("cd"):
        try:
            path = command.replace("cd ", "", 1)
            return cd(path)
        except IndexError:
            return write("Bad syntax for cd. Use: cd <file_path>\n")
    elif command.startswith('cat'):
        try:
            path = command.replace("cat ", "", 1)
            return cat(path)
        except IndexError:
            return write("Bad syntax for cd. Use: cat <file_path>\n")
    elif command.startswith('echo'):
        text = command.replace("echo ", "", 1)
        return echo(text)
    elif command.startswith("rm"):
        try:
            path = command.replace("rm ", "", 1)
            return rm(path)
        except IndexError:
            return write("Bad syntax for rm. Use: cd <file_path>\n")      
    else:
        return write("Bad syntax or unknown command.\n")

def ls(name_list):
    directories = set()
    files = set()
    
    for name in name_list:
        # Удаление части пути до текущей директории
        relative_path = name[len(current_directory):]

        # Если есть поддиректории, то это директория
        if relative_path.endswith("/"):
            directories.add(relative_path.split("/")[0] + "/")
        else:
            # Если это файл, добавляем его полностью (с расширением)
            files.add(relative_path)

    # Объединение директорий и файлов для вывода
    all_items = sorted(directories | files)
    
    if all_items:
        rslt = ""
        for item in all_items:
            if current_directory + item in permissions:
                mode_str = oct(permissions[current_directory + item])[2:]
                rslt += write(f"{mode_str} {item}")
            else:
                if len(item) != 0:
                    rslt += write(f"--- {item}")
                else:
                    continue
        write()
        return rslt
    else:
        return write("No files or directories found\n")

def cd(path):
    global current_directory
    with ZipFile("files.zip") as myzip:
        if path == "/":  # Если пользователь хочет перейти в корень
            current_directory = ""  # Корень архива
            lbl = updateLabel()
            return write("Returned to root directory\n"), current_directory, lbl
        elif any(name.startswith(path) for name in myzip.namelist()):
            current_directory = path if path.endswith("/") else path + "/"
            lbl = updateLabel()
            return write(f"Changed directory to {current_directory}\n"), current_directory, lbl
        else:
            return write(f"Directory {path} not found\n"), current_directory

def cat(path):
    with ZipFile("files.zip", 'r') as myzip:
        content = myzip.read(path).decode()
        return write(content)

def echo(text):
    return write(text)

def rm(path):
    with ZipFile("files.zip", "r") as zin:
        with ZipFile("files.zip.tmp", "w") as zout:
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                if path != item.filename:
                    zout.writestr(item, buffer)
    if platform.system() == "Windows":
        os.system('del files.zip')            # Используйте 'del' для удаления
        os.system('ren files.zip.tmp files.zip')  # Используйте 'ren' для переименования
    else:
        os.system('rm files.zip')             # Используйте 'rm' для удаления в Unix
        os.system('mv files.zip.tmp files.zip')  # Используйте 'mv' для переименования в Unix
    return write(f"File {path} was deleted")

def updateLabel():
    try:
        label.config(text=f"PATH: {current_directory}")
        return f"PATH: {current_directory}"
    except:
        return f"PATH: {current_directory}"

def write(text=""):
    try:
        output_area.configure(state=tk.NORMAL)
        output_area.insert(tk.END, text+"\n")
        output_area.configure(state=tk.DISABLED)
        return text
    except:
        return text

def clear():
    output_area.configure(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)
    output_area.configure(state=tk.DISABLED)

if __name__ == "__main__":
    archive_path = open_yaml()

    root = tk.Tk()
    root.title(f"OS emulator")
    root.geometry("450x320")
    label = tk.Label(text=f"PATH: {current_directory}")
    label.pack()

    output_area = tk.Text(root, height=10, width=65, state=tk.DISABLED)
    output_area.pack(pady=10)

    input_area = tk.Text(root, height=2, width=45)
    input_area.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    exec_button = tk.Button(button_frame, text="Run", command=command)
    exec_button.pack(side=tk.LEFT, padx=10)

    clear_button = tk.Button(button_frame, text="Clear", command=clear)
    clear_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()