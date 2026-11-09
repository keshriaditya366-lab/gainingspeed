import time
from datetime import datetime

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🟢 Test script started.")
    print("Sleeping for 10 hours...")
    
    total_hours = 10
    for hour in range(1, total_hours + 1):
        # Sleep for 1 hour (3600 seconds)
        time.sleep(3600)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏳ Hour {hour}/{total_hours} completed.")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔴 10 hours complete. Exiting.")

if __name__ == "__main__":
    main()
