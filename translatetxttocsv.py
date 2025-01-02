import csv
import re

def convert_txt_to_csv(txt_file_path, csv_file_path):
    """
    Converts a Markdown table-like text file to a CSV file with columns:
      [Company, Role, Location, Application/Link, Date Posted, Is_US_Location]

    1. "↳" indicates a repeated Company from the previous row.
    2. Extracts the first valid (non-"https://simplify" prefixed) link from 'Application/Link'
       and removes "?utm_source=Simplify&ref=Simplify" if present.
    3. Determines whether the location is in the USA or not, 
       and appends "Yes"/"No" in the final 'Is_US_Location' column.

    Args:
        txt_file_path (str): Path to the input text file.
        csv_file_path (str): Path to the output CSV file.
    """

    # Helper: Identify if a location is in the US
    def is_us_location(loc: str) -> bool:
        # Common US strings:
        if re.search(r'(usa|united states)', loc, re.IGNORECASE):
            return True
        # List of two-letter state abbreviations
        us_states = [
            "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
            "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
            "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
            "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
            "WI","WY"
        ]
        # Patterns like "San Jose, CA" or "San Jose, CA, USA"
        state_pattern = r',\s+(' + '|'.join(us_states) + r')(,?\s*(USA|United States)?)?$'
        if re.search(state_pattern, loc, re.IGNORECASE):
            return True
        # Handle well-known city shortcuts like "NYC", "Washington, DC", etc.
        special_us_cities = {"nyc", "washington d.c.", "washington, dc", "dc", "remote in usa"}
        if loc.strip().lower() in special_us_cities:
            return True
        return False

    # Read all lines
    with open(txt_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Find header line (the one before the "| --- | --- | --- |" separator)
    header_line_index = -1
    for i, line in enumerate(lines):
        if re.match(r'\| -+ \| -+ \| -+ \| -+ \| -+ \|', line.strip()):
            header_line_index = i - 1
            break

    if header_line_index == -1:
        print("Error: Could not find a valid header line. Make sure your table is Markdown formatted.")
        return

    # Parse header
    header_line = lines[header_line_index].strip()
    header_items = [col.strip() for col in header_line.strip('|').split('|')]

    # We will add the "Is_US_Location" column at the end
    header_items.append("Is_US_Location")

    # Data lines start after the header and its separator line
    data_lines = lines[header_line_index + 2:]

    # Prepare to parse data
    data = []
    previous_company = ""

    # Process each data row
    for line in data_lines:
        line = line.strip()
        # Skip empty or non-table lines
        if not line or line.startswith('---') or not line.startswith('|'):
            continue

        # Split columns
        items = [col.strip() for col in line.strip('|').split('|')]

        # We expect at least 5 columns (Company, Role, Location, Application/Link, Date Posted)
        if len(items) < 5:
            print(f"Skipping malformed line: {line}")
            continue

        # Handle "↳" for repeated Company
        if items[0] == "↳":
            items[0] = previous_company
        else:
            previous_company = items[0]

        # Remove HTML tags from everything except the link column
        for idx in range(len(items)):
            if idx != 3:  # 3 is "Application/Link"
                items[idx] = re.sub(r'<[^>]*>', '', items[idx])

        # Extract first valid link in 'Application/Link'
        link_column = items[3]
        clean_link = ""
        href_matches = re.findall(r'<a href="([^"]+)"', link_column)
        for match in href_matches:
            if not match.startswith("https://simplify"):
                clean_link = re.sub(r'\?utm_source=Simplify&ref=Simplify', '', match)
                break
        items[3] = clean_link

        # Determine if US-based
        location = items[2]
        items.append("Yes" if is_us_location(location) else "No")

        data.append(items)

    # Write CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header_items)
        writer.writerows(data)

if __name__ == "__main__":
    txt_file = "raw.txt"   # Replace with your actual input file path
    csv_file = "clean5.csv"  # Replace with your desired output file path
    convert_txt_to_csv(txt_file, csv_file)
    print(f"Successfully converted {txt_file} to {csv_file}")
