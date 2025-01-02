import requests

def fetch_and_filter_table(output_file="test.txt"):
    """
    1. Fetches the raw markdown content from the GitHub URL.
    2. Locates the lines after '| Company | Role | Location | Application/Link | Date Posted |'
       and stops before '<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->'
    3. Filters out any lines containing '🛂' or '🔒'.
    4. Writes the filtered text to the specified output file.
    """
    url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/README.md"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch content from {url}")

    content_lines = response.text.splitlines()

    # Identify the start and end markers
    start_marker = "| Company | Role | Location | Application/Link | Date Posted |"
    end_marker = "<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->"

    start_index = -1
    end_index = -1

    for i, line in enumerate(content_lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break  # Found the end marker, no need to keep searching

    if start_index == -1 or end_index == -1 or end_index <= start_index:
        raise ValueError("Could not find the specified table boundaries in the file.")

    # Extract lines between the markers
    table_lines = content_lines[start_index : end_index]

    # Filter out lines containing "🛂" or "🔒"
    filtered_lines = [
        line for line in table_lines
        if "🛂" not in line and "🔒" not in line
    ]

    # Join into a single string
    filtered_table_text = "\n".join(filtered_lines)

    # Write the filtered text to test.txt (or user-specified output file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(filtered_table_text)

    print(f"Filtered table text written to {output_file}")


if __name__ == "__main__":
    fetch_and_filter_table("temp.txt")
