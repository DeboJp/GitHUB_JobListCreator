# DeboJp-GitHUB_JobListCreator

This project automates the process of fetching, cleaning, and updating a list of job postings from a GitHub repository, specifically designed to handle the [SimplifyJobs/Summer2025-Internships](https://github.com/SimplifyJobs/Summer2025-Internships) repository's `dev` branch. The main goal is to efficiently identify and isolate newly added job postings, overcoming the challenge of random insertion positions within the GitHub board and having a custom manipulatable list.

## Features

-   **Automated Data Fetching:** Uses `update.py` to fetch the latest job postings from the target GitHub repository, filtering out entries with specific markers (e.g., "🛂" or "🔒").
-   **Markdown to CSV Conversion:** Employs `translatetxttocsv.py` to convert the fetched Markdown table into a structured CSV format. It handles repeated company entries (indicated by "↳"), extracts valid application links, and determines whether the job location is in the US.
-   **Duplicate Removal:** Implements a mechanism in `main.py` to compare the newly fetched data against a previously cleaned dataset (`clean.csv`), ensuring that only unique job postings are retained in `new_clean.csv`.
-   **Error Handling:** Includes basic error handling to manage potential issues during the process, such as network errors or file format inconsistencies.

## Directory Structure
└── DeboJp-GitHUB_JobListCreator/
├── clean.csv # Stores the previously cleaned, unique job postings.
├── datanew.txt # Intermediate file holding the raw, filtered Markdown table.
├── main.py # Orchestrates the update, conversion, and duplicate removal process.
├── new_clean.csv # Contains the newly fetched, cleaned, and unique job postings.
├── translatetxttocsv.py # Converts the Markdown table to CSV, adding location-based filtering.
├── update.py # Fetches and filters the raw Markdown table from the GitHub repository.
└── Prev Test Files/ # Holds previous test files for development and debugging.


## How It Works

1. **Fetching Data (`update.py`):**
    -   Fetches the raw Markdown content from the specified GitHub repository URL.
    -   Identifies the table section within the Markdown content.
    -   Filters out lines containing unwanted markers ("🛂" or "🔒"). // international and locked/closed positions (for initial csv).
    -   Writes the filtered Markdown table to `datanew.txt`.

2. **Converting to CSV (`translatetxttocsv.py`):**
    -   Reads the `datanew.txt` file.
    -   Parses the Markdown table structure, handling repeated company entries.
    -   Extracts the first valid application link (excluding "https://simplify" prefixed links).
    -   Removes any "?utm\_source=Simplify&ref=Simplify" from the links.
    -   Determines if the location is in the US based on common patterns and state abbreviations.
    -   Appends an "Is\_US\_Location" column with "Yes" or "No".
    -   Reverses the order of rows (excluding the header).
    -   Writes the processed data to `new_clean.csv`.

3. **Removing Duplicates (`main.py`):**
    -   Reads the existing `clean.csv` (if it exists) into a set of tuples for efficient duplicate checking.
    -   Reads the `new_clean.csv`.
    -   Compares the rows in `new_clean.csv` against `clean.csv`.
    -   Rewrites `new_clean.csv`, keeping only the unique rows (that are not present in `clean.csv`).

4. **Orchestration (`main.py`):**
    -   Sequentially runs `update.py`, `translatetxttocsv.py`, and the duplicate removal logic.
    -   Handles potential exceptions during the process.

## Future Plans

-   **Support for Multiple Websites:** Extend the project to fetch and process job postings from multiple websites, creating a consolidated output.
-   **Scheduling:** Integrate a task scheduler (e.g., `cron` or GitHub Actions) to automatically run the update process at regular intervals.
-   **Web Interface:** Develop a user-friendly web interface to visualize and interact with the collected job postings. (maybe)

## Usage

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/DeboJp-GitHUB_JobListCreator.git
cd DeboJp-GitHUB_JobListCreator
