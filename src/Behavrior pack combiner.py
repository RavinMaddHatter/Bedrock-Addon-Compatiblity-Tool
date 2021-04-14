import json
import os
import shutil
from os import listdir
from os import path
from os.path import isfile, join
from zipfile import ZipFile 
from shutil import copyfile
from glob import glob

import threading
import ntpath


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
def addDeathCounter(path_to_bp):
    copy_ac(path_to_bp,"death_counter_j5cfmnkccwt7ppim3lsyue.json")
    copy_animation(path_to_bp,"death_counter_start_j5cfmnkccwt7ppim3lsyue.json")
    add_a_c_to_player(path_to_bp,
                      "controller.animation.death_counter_j5cfmnkccwt7ppim3lsyue",
                      "death_counter_j5cfmnkccwt7ppim3lsyue")
    add_a_c_to_player(path_to_bp,
                      "animation.start_death_counter_j5cfmnkccwt7ppim3lsyue",
                      "start_death_counter_j5cfmnkccwt7ppim3lsyue",
                      addtoscript=False)

    
    
def addOPS(path_to_bp):
    copy_ac(path_to_bp,"one_player_sleep_njorunnb628pievrfeckwx.json")
    add_a_c_to_player(path_to_bp,
                      "controller.animation.one_player_sleep_uuid_njorunnb628pievrfeckwx",
                      "ops_njorunnb628pievrfeckwx")
def copy_ac(path_to_bp,ac_name):
    path_to_a_c=join(path_to_bp,"animation_controllers") 
    if not(os.path.isdir(path_to_a_c)):
        os.mkdir(path_to_a_c)
    
    copyfile(join("lookups",ac_name),join(path_to_a_c,ac_name))
def copy_animation(path_to_bp,ani_name):
    path_to_animations=join(path_to_bp,"animations") 
    if not(os.path.isdir(path_to_animations)):
        os.mkdir(path_to_animations)
    copyfile(join("lookups",ani_name),join(path_to_animations,ani_name))
def add_a_c_to_player(path_to_bp,a_c_handle,ac_common_handle,addtoscript=True):
    result = [y for x in os.walk(path_to_bp) for y in glob(os.path.join(x[0], '*.json'))]
    for file in result:
        with open(file, 'r+') as f:
            data = json.load(f)
            if "minecraft:entity" in data.keys():
                if data["minecraft:entity"]["description"]["identifier"]=="minecraft:player":
                    if "scripts" not in data["minecraft:entity"]["description"].keys() and addtoscript:
                        data["minecraft:entity"]["description"]["scripts"]={"animate":[]}
                    if "animations" not in data["minecraft:entity"]["description"].keys():
                        data["minecraft:entity"]["description"]["animations"]={}
                    if addtoscript:
                        data["minecraft:entity"]["description"]["scripts"]["animate"].append(ac_common_handle)
                    data["minecraft:entity"]["description"]["animations"][ac_common_handle]=a_c_handle
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate() 
def edit_manifests(path_to_bp , packs):
    with open(join(path_to_bp,"manifest.json"), 'r+') as f:
        data = json.load(f)
        data["header"]["description"]+=", modified by a RavinMaddHatters pack merge tool to include: {}".format(packs)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate() 

    
def mergePacks(path,death=False,ops=False):
    cwd = os.getcwd()
    path_to_save="temp"
    with ZipFile(path, 'r') as zipObj:
        zipObj.extractall(path_to_save)
    manifests=find_all("manifest.json",path_to_save)
    path_to_bp=""
    for mani in manifests:
        with open(mani) as f:
            packmani = json.load(f)
        for sub in packmani["modules"]:
            if "data"== sub["type"]:
                path_to_bp=os.path.dirname(mani)
    pack =""
    if death:
        addDeathCounter(path_to_bp)
        pack+="Death Counter"
    if ops:
        if len(pack)>0:
            pack+=", "
        pack+="One player sleep"
        addOPS(path_to_bp)
    if death or ops:
        edit_manifests(path_to_bp,pack)
    temp_path=join(cwd,path_to_save)
    os.chdir(temp_path)
    pack_name=ntpath.basename(path)

    file_paths = []
    for directory,_,_ in os.walk(temp_path):
        files=glob(os.path.join(directory, "*.*"))
        for file in files:
            print(os.getcwd())
            print(file)
            file_paths.append(file.replace(os.getcwd()+"\\",""))

    with ZipFile(pack_name, 'x') as zip:
        for file in file_paths:
            print(file)
            zip.write(file)
    os.chdir(cwd)
    copyfile(join(path_to_save,pack_name),"merged_"+pack_name)
    shutil.rmtree(path_to_save)
    print("packs have been merged and processing is completed, please use merged_"+pack_name)
    
    
if __name__ == "__main__":
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import StringVar, Button, Label, Entry, Tk, Checkbutton, END, ACTIVE
    from tkinter import filedialog, Scale,DoubleVar,HORIZONTAL,IntVar,Listbox, ANCHOR
    def browsepack():
        #browse for a structure file.
        packPath.set(filedialog.askopenfilename(filetypes=(
            ("addon", "*.mcaddon *.MCADDON"),("zip", "*.zip *.ZIP") )))
    def make_pack_from_gui():
        mergePacks(packPath.get(),death=death_counter_check.get(),ops=ops_counter_check.get())
    root = Tk()
    death_counter_check = IntVar()
    ops_counter_check = IntVar()
    packPath = StringVar()
    death_check = Checkbutton(root, text="Death Counter", variable=death_counter_check, onvalue=1, offvalue=0)
    ops_check = Checkbutton(root, text="One Player Sleep", variable=ops_counter_check, onvalue=1, offvalue=0)
    browsButton = Button(root, text="Browse", command=browsepack)
    packButton = Button(root, text="make pack", command=make_pack_from_gui)
    path_entry = Entry(root, textvariable=packPath, width=30)
    r=0
    path_entry.grid(row=r, column=0)
    browsButton.grid(row=r, column=1)
    r+=1
    death_check.grid(row=r, column=0,columnspan=2)
    r+=1
    ops_check.grid(row=r, column=0,columnspan=2)
    r+=1
    packButton.grid(row=r, column=1)

    
    root.mainloop()
    root.quit()
