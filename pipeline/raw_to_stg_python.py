"""Survey ETL pipeline notes.

Purpose:
    Read survey data from a Google Sheet and save it as a CSV file.

ETL steps:
    Extract: Read the data from the Google Sheet.
    Transform: Apply custom column names and check the column count.
    Load: Save the prepared data in the raw folder.

Folder purposes:
    raw: Stores the latest incoming data from the source.
    error: Stores a file when the pipeline cannot save it successfully.
    target: Reserved for cleaned and transformed data in a later stage.
    archive: Reserved for older raw files so previous runs are kept.

Current flow:
    Google Sheet -> raw CSV
                         |
                         +-> error if saving fails

The target and archive folders are not used by this current script yet.
They can be added when the cleaning and history stages are built.
"""

# Import pandas so we can work with the sheet as a table.
import pandas as pd

# Import Path to create folder and file paths.
from pathlib import Path

# Import shutil to move a failed file.
import shutil

# Use the Google Sheet's CSV export link for the first worksheet.
sheet_url = "https://docs.google.com/spreadsheets/d/1OzDHmE7ts9aI2fmqPUTJYUCLTCGTtHuQBYF2tquoRrg/export?format=csv&gid=0"

# Read the sheet with its original column names.
sheet_data = pd.read_csv(sheet_url)

# Display the first five rows of the loaded sheet.
sheet_data.head()


df = sheet_data

# Set the main project folder.
project_folder = Path(r"F:\Big Data\Survey")

# Set the folder for successful raw files.
raw_folder = project_folder / "raw"

# Set the folder for files that fail.
error_folder = project_folder / "error"

# Create the raw folder if it is missing.
raw_folder.mkdir(exist_ok=True)

# Create the error folder if it is missing.
error_folder.mkdir(exist_ok=True)

# Set the CSV file name.
file_name = "survey_responses.csv"

# Set the file path inside the raw folder.
raw_file = raw_folder / file_name

# Set the file path inside the error folder.
error_file = error_folder / file_name

try:
    # Define the custom names for the 11 columns.
    custom_columns = [
        "response_time",
        "python_level",
        "background",
        "class_direction",
        "python_topics",
        "architecture_topics",
        "learning_style",
        "expectations_rating",
        "pace",
        "difficulty",
        "theory_practice_balance"
    ]

    # Check that there is one custom name for every DataFrame column.
    if len(df.columns) != len(custom_columns):
        raise ValueError(
            f"Column count mismatch: data has {len(df.columns)} columns, "
            f"but custom_columns has {len(custom_columns)} names."
        )

    # Apply the custom column names before saving the DataFrame.
    df.columns = custom_columns

    # Show the custom names being used in the CSV.
    print(f"Custom columns: {list(df.columns)}")

    # Save the DataFrame as a CSV in the raw folder.
    df.to_csv(raw_file, index=False)

    # Confirm that the file was saved.
    print(f"File saved to: {raw_file}")
except Exception as error:
    # Check whether a partly written file exists.
    if raw_file.exists():
        # Move the failed file to the error folder.
        shutil.move(str(raw_file), str(error_file))

        # Confirm that the file was moved.
        print(f"File moved to error folder: {error_file}")

    # Display the reason for the failure.
    print(f"Save failed: {error}")
