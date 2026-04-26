import numpy as np
import pandas as pd
import requests
import zipfile
import io
import ast
import inspect
import textwrap

# =========================
# 1. Download the dataset
# =========================
url = "/Users/johnricor/Downloads/MyAnimeList-Database-master.zip"
r = requests.get(url, stream=True)

z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

# =========================
# 2. Load and clean the data
# =========================
anime_data = pd.read_csv("MyAnimeList-Database-master/data/anime.csv")
anime_data_extracted = anime_data[anime_data["Score"] != "Unknown"].copy()
anime_data_extracted["Score"] = pd.to_numeric(anime_data_extracted["Score"])

# =========================
# 3. Homework function
# =========================
def homework(anime_data_extracted):
    result = anime_data_extracted.groupby("Type")["Score"].mean().sort_values(ascending=False)
    return result

# =========================
# 4. Public tests
# =========================
def hw2_public_tests(homework_func):
    print("=== HW2 Public Tests ===")

    source = textwrap.dedent(inspect.getsource(homework_func))
    tree = ast.parse(source)

    print("Test 1: No import statements in function...", end=" ")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            print("NG")
            if isinstance(node, ast.Import):
                names = ", ".join(alias.name for alias in node.names)
            else:
                names = node.module
            print(f" Found import statement: '{names}'")
            print(" Remove all import statements before submitting.")
            return
    print("OK")

    print("Test 2: No data loading code in function...", end=" ")
    blocked_calls = {"read_csv", "read_excel", "read_json", "read_html",
                     "get", "post", "ZipFile", "extractall", "urlopen"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_name = ""
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                func_name = node.func.id
            if func_name in blocked_calls:
                print("NG")
                print(f" Found data loading call: '{func_name}()'")
                print(" Do not include data downloading/loading code in your function.")
                return
    print("OK")

    print("Test 3: No hardcoded file paths or URLs...", end=" ")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value
            if val.startswith("http") or ".csv" in val or ".zip" in val:
                print("NG")
                print(f" Found hardcoded path/URL: '{val[:60]}...'")
                print(" Do not include file paths or URLs in your function.")
                return
    print("OK")

    print("=== All Public Tests Passed ===")

# =========================
# 5. Run tests and output
# =========================
if __name__ == "__main__":
    hw2_public_tests(homework)
    print()
    print(homework(anime_data_extracted))