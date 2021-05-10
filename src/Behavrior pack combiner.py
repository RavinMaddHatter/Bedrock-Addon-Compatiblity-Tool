import json
import os
import shutil
from os import listdir
from os import path
from os.path import isfile, join
from zipfile import ZipFile 
from shutil import copyfile
from glob import glob
import ntpath
import threading
import re

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
                      "start_death_counter_j5cfmnkccwt7ppim3lsyue")

def addWeatherClear(path_to_bp):
    copy_ac(path_to_bp,"clear_weather_out_of_bed_njorunnb628pievrfeckwx.json")
    
    add_a_c_to_player(path_to_bp,
                      "controller.animation.clear_weather_out_of_bed_njorunnb628pievrfeckwx",
                      "clear_weather_id_out_of_bed_njorunnb628pievrfeckwx")
    
def addOPS(path_to_bp):
    copy_ac(path_to_bp,"one_player_sleep_njorunnb628pievrfeckwx.json")
    
    add_a_c_to_player(path_to_bp,
                      "controller.animation.one_player_sleep_njorunnb628pievrfeckwx",
                      "one_player_sleep_njorunnb628pievrfeckwx")
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
    found=False
    for file in result:
        print(file)
        with open(file, 'r+') as f:
            data=""
            for line in f:
                data+=line
            data=re.sub("\/\/[^\n]*\n", '', data )
            data = json.loads(data)
            if type(data) is dict:
                if "minecraft:entity" in data.keys():
                    if data["minecraft:entity"]["description"]["identifier"]=="minecraft:player":
                        found=True
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
    print(found)
    if not found:
        path_to_a_c=join(path_to_bp,"entities") 
        if not(os.path.isdir(path_to_a_c)):
            os.mkdir(path_to_a_c)
        copyfile(join("lookups","player.json"),join(path_to_a_c,"player.json"))
    
        copy_ac(path_to_bp,"one_player_sleep_njorunnb628pievrfeckwx.json")
        
def edit_manifests(path_to_bp , packs):
    with open(join(path_to_bp,"manifest.json"), 'r+') as f:
        data = json.load(f)
        data["header"]["description"]+=", modified by a RavinMaddHatters pack merge tool to include: {}".format(packs)
        
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate() 

    
def mergePacks(path,death=False,ops=False,clearWeather=False):
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
    if clearWeather:
        addWeatherClear(path_to_bp)
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

def loadJsonKillComments(jsonFile):
    data=""
    with open(jsonFile, 'r+') as f:
        
        for line in f:
            data+=line
    data=re.sub("\/\/[^\n]*\n", '', data )
    data = json.loads(data)
    return data
def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []
    keys=[]

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)
            keys.append([key])

        elif isinstance(value, dict):
            results,recurKeys = get_recursively(value, field)
            for result in results:
                fields_found.append(result)
            for recurKey in recurKeys:
                tempKey=[key]
                tempKey+=recurKey
                keys.append(tempKey)

        elif isinstance(value, list):
            for ind in range(len(value)):
                item=value[ind]
                if isinstance(item, dict):
                    more_results,more_recurKeys = get_recursively(item, field)
                    
                    for another_result in more_results:
                        fields_found.append(another_result)
                    for more_recurkey in more_recurKeys:
                        tempKey=[ind]
                        tempKey+=more_recurkey
                        keys.append(tempKey)
                        

    return fields_found, keys
def check_compatiblity(Base,Cross):
    path_to_base="base"
    path_to_cross="Cross"
    with ZipFile(Base, 'r') as zipObj:
        zipObj.extractall(path_to_base)
        
    with ZipFile(Cross, 'r') as zipObj:
        zipObj.extractall(path_to_cross)
    result = [y for x in os.walk(path_to_base) for y in glob(os.path.join(x[0], '*.json'))] 
    base_handles=[]
    for file in result:
        print(file)
        data=loadJsonKillComments(file)
        try:
            fields_found, keys=get_recursively(data,"identifier")
        except:
            fields_found=[]
            keys=[]
        base_handles+=fields_found
    result2 = [y for x in os.walk(path_to_cross) for y in glob(os.path.join(x[0], '*.json'))] 
    cross_handles=[]
    for file in result2:
        print(file)
        data=loadJsonKillComments(file)
        try:
            fields_found, keys=get_recursively(data,"identifier")
        except:
            fields_found=[]
            keys=[]
        cross_handles+=fields_found
    print(base_handles)
    print(cross_handles)
    shutil.rmtree(path_to_base)
    shutil.rmtree(path_to_cross)
    return set(base_handles).intersection(set(cross_handles))
if __name__ == "__main__":
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import StringVar, Button, Label, Entry, Tk, Checkbutton, END, ACTIVE
    from tkinter import filedialog, Scale,DoubleVar,HORIZONTAL,IntVar,Listbox, ANCHOR
    def browsepack():
        #browse for a structure file.
        packPath.set(filedialog.askopenfilename(filetypes=(
            ("addon", "*.mcaddon *.MCADDON *.MCPACK *mcpack"),("zip", "*.zip *.ZIP") )))
    def make_pack_from_gui():
        mergePacks(packPath.get(),
                   death=death_counter_check.get(),
                   ops=ops_counter_check.get(),
                   clearWeather=clear_counter_check.get())
        
    def crossCheckPacksGui():
        base_pack=packPath.get()
        if len(base_pack)>0:
            cross_pack=(filedialog.askopenfilename(filetypes=(
                ("Addon to Cross Check", "*.mcaddon *.MCADDON *.MCPACK *.MCPACK" ),("zip", "*.zip *.ZIP") )))
            intersections=check_compatiblity(base_pack,cross_pack)
            print(intersections)
            if len(intersections)!=0:
                printInt="\n".join(intersections)
                messagebox.showerror("Not Compatible","The two packs are not compatible because they both modify the following game features: \n{}".format(printInt))
            else:
                messagebox.showinfo("Compatible","The two packs are likely compatible")
            
        else:
            messagebox.showerror("No Base Pack", "You must first select a base pack to check compatiblity")
             
        
    root = Tk()
    root.title("Addon Checker")
    core_pack=Label(root, text="Core Pack")
    add_ins=Label(root, text="Common Additions (will be added to the core pack):")
    death_counter_check = IntVar()
    ops_counter_check = IntVar()
    clear_counter_check = IntVar()
    packPath = StringVar()
    death_check = Checkbutton(root, text="Death Counter", variable=death_counter_check, onvalue=1, offvalue=0)
    ops_check = Checkbutton(root, text="One Player Sleep", variable=ops_counter_check, onvalue=1, offvalue=0)

    clear_check = Checkbutton(root, text="One player sleep with clear weather", variable=clear_counter_check, onvalue=1, offvalue=0)
    browsButton = Button(root, text="Browse", command=browsepack)
    packButton = Button(root, text="Merge in Packs", command=make_pack_from_gui)
    Cross_check = Button(root, text="Cross Check a Pack", command=crossCheckPacksGui)
    path_entry = Entry(root, textvariable=packPath, width=30)
    r=0
    core_pack.grid(row=r, column=0,columnspan=2)
    r+=1
    path_entry.grid(row=r, column=0)
    browsButton.grid(row=r, column=1)
    r+=1
    add_ins.grid(row=r, column=0,columnspan=2)
    r+=1
    death_check.grid(row=r, column=0,columnspan=2)
    r+=1
    ops_check.grid(row=r, column=0,columnspan=2)
    r+=1
    clear_check.grid(row=r, column=0,columnspan=2)
    r+=1
    Cross_check.grid(row=r, column=0)
    packButton.grid(row=r, column=1)

    
    root.mainloop()
    root.quit()
