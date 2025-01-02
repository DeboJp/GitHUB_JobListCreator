import subprocess
import csv
import os


def run_update():
    """
    Runs update.py to fetch the latest data and save it to test.txt.
    """
    print("Running update.py to fetch latest data...")
    subprocess.run(["python3", "update.py"], check=True)


def run_translate():
    """
    Runs translatetxttocsv.py to convert test.txt to new_clean.csv.
    """
    print("Running translatetxttocsv.py to generate new_clean.csv...")
    subprocess.run(["python3", "translatetxttocsv.py"], check=True)


def remove_duplicates(clean_file="clean.csv", new_file="new_clean.csv"):
    """
    Removes rows from new_clean.csv that already exist in clean.csv.
    
    Args:
        clean_file (str): Path to the current clean.csv file.
        new_file (str): Path to the newly generated new_clean.csv file.
    """
    print("Removing duplicates from new_clean.csv...")

    # Read current clean.csv
    if not os.path.exists(clean_file):
        print(f"{clean_file} does not exist. Assuming no duplicates to remove.")
        clean_data = []
    else:
        with open(clean_file, "r", encoding="utf-8") as f:
            clean_data = set(tuple(row) for row in csv.reader(f))

    # Read new_clean.csv
    with open(new_file, "r", encoding="utf-8") as f:
        new_data = list(csv.reader(f))

    if not new_data:
        print("new_clean.csv is empty. Nothing to process.")
        return

    # Separate header and data rows
    header = new_data[0]
    new_rows = set(tuple(row) for row in new_data[1:])

    # Remove duplicates
    unique_rows = new_rows - clean_data

    # Rewrite new_clean.csv with only unique rows
    with open(new_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sorted(unique_rows))

    print(f"Updated {new_file} to contain only unique rows.")


if __name__ == "__main__":
    try:
        run_update()  # Step 1: Fetch the latest data
        run_translate()  # Step 2: Convert the fetched data into a CSV
        remove_duplicates("clean.csv", "new_clean.csv")  # Step 3: Remove duplicates from new_clean.csv
    except Exception as e:
        print(f"An error occurred: {e}")
