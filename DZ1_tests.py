import sys, DZ1_GUI
from DZ1_GUI import *
from zipfile import ZipFile

zip_path = "files.zip"

# Тестирование yaml
def test_yaml():
    result = open_yaml()
    assert "C:/Users/user/Desktop/МИРЭА/Конфигурационное управление/Домашнее задание №1" in result

# Тестирование ls
def test_ls():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("newtest/", "")
        myzip.writestr("newtest/testfile.txt", "Test content")
    result = ls(["newtest/", "newtest/testfile.txt"])
    assert "newtest/" in result
    assert "testfile.txt" in result

def test_ls_empty():
    result = ls([])
    assert "No files or directories found" in result

# Тестирование cd
def test_cd():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("newtest/", "")
    cur_dir = cd("newtest")[1]
    lbl = cd("newtest")[2]
    assert cur_dir == "newtest/"
    assert lbl == f"PATH: {DZ1_GUI.current_directory}"

def test_cd_invalid_path():
    msg = cd("non_existing_dir")[0]
    assert "Directory non_existing_dir not found" in msg

# Тестирование cat
def test_cat():
    with ZipFile("files.zip", 'w') as myzip:
        myzip.writestr("newtest/", "")
        myzip.writestr("newtest/testfile.txt", "Test content")
    result = cat("newtest/testfile.txt")
    assert "Test content" in result

# Тестирование echo
def test_echo():
    result = echo("test complited x1")
    assert "test complited x1" in result

# Тестирование rm
def test_rm():
    with ZipFile("files.zip", 'w') as myzip:
        myzip.writestr("newtest/", "")
        myzip.writestr("newtest/testfile.txt", "Test content")
    result = rm("newtest/testfile.txt")
    assert "File newtest/testfile.txt was deleted" in result

# Тестирование команды ls
def test_command_ls():
    with ZipFile(zip_path, "w") as myzip:
        DZ1_GUI.current_directory = ""
        myzip.writestr("test_file.txt", "Test content")
    result = command("ls")
    assert "test_file.txt" in result

def test_command_ls_empty():
    with ZipFile(zip_path, "w") as myzip:
        myzip.writestr("newtest/", "")
        DZ1_GUI.current_directory = "newtest/"
    result = command("ls")
    assert "" in result

# Тестирование команды cd
def test_command_cd():
    result = command("cd newtest/")[1]
    lbl = command("cd newtest/")[2]
    assert result == "newtest/"
    assert lbl == f"PATH: {DZ1_GUI.current_directory}"

def test_command_cd_invalid():
    result = command("cd non_existing_dir")[0]
    assert "Directory non_existing_dir not found" in result

# Тестирование cat
def test_command_cat():
    with ZipFile("files.zip", 'w') as myzip:
        myzip.writestr("newtest/", "")
        myzip.writestr("newtest/testfile.txt", "Test content")
    result = command("cat newtest/testfile.txt")
    assert "Test content" in result

# Тестирование команды echo
def test_command_echo():
    result = command("echo test complited x2")
    assert "test complited x2" in result

# Тестирование rm
def test_command_rm():
    with ZipFile("files.zip", 'w') as myzip:
        myzip.writestr("newtest/", "")
        myzip.writestr("newtest/testfile.txt", "Test content")
    result = command("rm newtest/testfile.txt")
    assert "File newtest/testfile.txt was deleted" in result