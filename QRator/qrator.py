import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(['python', script_name])

def menu():
    # Dictionary with keys as menu options, values as tuples of (description, script name)
    scripts = {
        '1': ('Credential Thief Clone Attack', 'runner.py'),
        '2': ('Installation Attacks', 'xssnotcomingsoon.py'),
        '3': ('Ready Templates', 'xssnotcomingsoon.py'),
        '4': ('XSS (#coming_not_soon)\n', 'xssnotcomingsoon.py'),
    '9': ('Settings', None),
    '10': ('Credits\n\n', None),
    '99': ('Quit\n', None),

    }

    while True:
        print("\n QRator\n  \n Created by d1screet\n  \n Version 1.0.1 \n \nTool Menu:")
        for key, value in scripts.items():
            print(f"{key}: {value[0]}")

        choice = input("Please select an option: ")

        if choice in scripts:
            if choice == '99':
                print("Quitting the menu.")
                break
            else:
                script_name = scripts[choice][1]
                run_script(script_name)
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    menu()
