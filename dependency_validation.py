import sys
import importlib.util

def check_import(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False
        return True
    except ModuleNotFoundError:
        return False

# Critical dependencies for UFO project
critical_deps = [
    'azure.identity',
    'faiss',
    'cv2',
    'yaml',
    'pywinauto',
    'pyautogui',
    'sentence_transformers',
    'langchain',
    'lxml',
    'openai',
    'numpy',
    'torch'
]

# Check each dependency
missing = []
installed = []

for dep in critical_deps:
    # Handle special case where import name differs from package name
    if dep == 'yaml':
        check_name = 'yaml'
    elif dep == 'cv2':
        check_name = 'cv2'
    else:
        check_name = dep
    
    if check_import(check_name):
        installed.append(dep)
    else:
        missing.append(dep)

# Print results
print("=== UFO² Dependency Validation ===")
print(f"Total dependencies checked: {len(critical_deps)}")
print(f"Successfully installed: {len(installed)}")

if missing:
    print(f"\nMissing dependencies ({len(missing)}):")
    for dep in missing:
        print(f" - {dep}")
    sys.exit(1)
else:
    print("\nAll critical dependencies are installed successfully!")
    sys.exit(0)
