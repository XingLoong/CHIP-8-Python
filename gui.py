import PySimpleGUI as sg
import threading
import subprocess
import os
import sys

def run_emulator(rom_path):
    """Launch the emulator in a separate process."""
    subprocess.Popen([sys.executable, "main.py", rom_path])

def main():
    sg.theme("DarkBlue3")

    layout = [
        [sg.Text("CHIP-8 Emulator", font=("Any", 16))],
        [sg.InputText(key="-ROM-", size=(40,1)), sg.FileBrowse("Browse", file_types=(("CHIP-8 ROMs", "*.ch8"),))],
        [sg.Button("Load ROM"), sg.Button("Quit")],
        [sg.StatusBar("Idle", key="-STATUS-")]
    ]

    window = sg.Window("CHIP-8 Frontend", layout, finalize=True)

    emulator_thread = None

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, "Quit"):
            break

        elif event == "Load ROM":
            rom_path = values["-ROM-"]
            if not rom_path or not os.path.exists(rom_path):
                window["-STATUS-"].update("Please select a valid ROM.")
                continue

            window["-STATUS-"].update(f"Running {os.path.basename(rom_path)}")
            
            # Kill existing emulator if running
            if emulator_thread and emulator_thread.is_alive():
                window["-STATUS-"].update("Restarting emulator...")
                # Here you'd signal emulator to quit, for now just continue
            
            # Start emulator
            emulator_thread = threading.Thread(target=run_emulator, args=(rom_path,), daemon=True)
            emulator_thread.start()

    window.close()

if __name__ == "__main__":
    main()
