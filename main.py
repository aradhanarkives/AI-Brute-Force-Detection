import sys
import subprocess
from pathlib import Path


print("==========================================")
print(" AI-BASED BRUTE FORCE ATTACK DETECTOR")
print("==========================================")

print("\nAvailable Modules:")
print("1. Single Login Detection")
print("2. Real-Time Monitoring")
print("3. View Identity Memory")
print("4. View Attack Pattern Memory")
print("5. View Decision Recovery Memory")

print("\nProject setup completed successfully.")

choice = input("\nEnter your choice: ")

project_folder = Path(__file__).resolve().parent


if choice == "1":
    print("\nOpening Single Login Detection...")

    subprocess.run([
        sys.executable,
        str(project_folder / "combined_detector.py")
    ])


elif choice == "2":
    print("\nOpening Real-Time Monitoring...")

    subprocess.run([
        sys.executable,
        str(project_folder / "monitoring" / "realtime_monitor.py")
    ])


elif choice == "3":
    print("\nOpening Identity Memory...")

    subprocess.run([
        sys.executable,
        str(project_folder / "identity_memory.py")
    ])


elif choice == "4":
    print("\nOpening Attack Pattern Memory...")

    subprocess.run([
        sys.executable,
        str(project_folder / "view_attack_memory.py")
    ])


elif choice == "5":
    print("\nOpening Decision Recovery Memory...")

    subprocess.run([
        sys.executable,
        str(project_folder / "view_decision_memory.py")
    ])


else:
    print("\nInvalid choice.")


input("\nPress Enter to exit...")