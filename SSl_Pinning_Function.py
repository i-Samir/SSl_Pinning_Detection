import os
import zipfile
import re
import subprocess

def get_apk_file_content(apk_file_path):
    """
    Extracts the DEX file from the APK file and returns the SMALI code as a string.
    """
    subprocess.run(["apktool", "d", apk_file_path, "-o", "output_dir"], check=True)
    dex_file = "output_dir/smali/classes.dex"
    with open(dex_file, "rb") as f:
        dex_bytes = f.read()
    return disassemble_dex(dex_bytes)

def disassemble_dex(dex_bytes):
    """
    Disassembles the DEX file into SMALI code and returns it as a string.
    """
    try:
        dex_file = "classes.dex"
        with open(dex_file, "wb") as f:
            f.write(dex_bytes)
        subprocess.run(["d2j-dex2smali", dex_file], stdout=subprocess.PIPE)
        with open("classes.dex.smali", "r") as f:
            return f.read()
    finally:
        if os.path.exists(dex_file):
            os.remove(dex_file)
        if os.path.exists("classes.dex.smali"):
            os.remove("classes.dex.smali")

def check_ssl_pinning_functions(apk_content, ssl_pinning_functions):
    """
    Checks for the specified SSL pinning certificate functions in the SMALI code of the APK file.
    """
    for function in ssl_pinning_functions:
        if function in apk_content:
            print ("SSL pinning function '{function}' found in the SMALI code of the APK file.")
            break

# Example usage
apk_file_path = input("Enter the path to the APK file: ")
ssl_pinning_functions = [x.strip() for x in input("Enter the SSL pinning function names (comma-separated): ").split(",")]
apk_content = get_apk_file_content(apk_file_path)
check_ssl_pinning_functions(apk_content, ssl_pinning_functions)
