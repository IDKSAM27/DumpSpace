import os
import pandas as pd

# 1. SET THIS to the folder where all your downloaded resumes are.
RESUME_FOLDER = 'resumes' 

# 2. SET THIS to what you want your output CSV file to be named.
OUTPUT_CSV = 'candidates.csv'

def scan_resumes(folder_path):
    candidate_data = []
    
    print(f"Scanning folder: {folder_path}...")
    
    # Check if the folder actually exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'.")
        print("Please create the folder and put your resumes in it.")
        return None

    # Loop through every file in the specified folder
    for filename in os.listdir(folder_path):
        
        # Check for PDF and Word documents
        if filename.endswith('.pdf') or filename.endswith('.docx'):
            
            # Get the full, absolute path to the file
            full_path = os.path.abspath(os.path.join(folder_path, filename))
            
            # Use the filename without extension as a 'Name'
            # You will likely edit this in the CSV later
            name = os.path.splitext(filename)[0]
            
            # Add the data to our list
            candidate_data.append({
                'Name': name,
                'Resume_Path': full_path
            })
            
    print(f"Found {len(candidate_data)} resumes.")
    return candidate_data

def save_to_csv(data_list, csv_filename):
    """
    Saves the list of data to a CSV file using pandas.
    """
    if not data_list:
        print("No resume data found, CSV will not be created.")
        return

    df = pd.DataFrame(data_list)
    
    # Add empty columns for the data we'll get later.
    # This sets up your master file perfectly.
    df['GitHub_URL'] = ''
    df['Resume_Score'] = 0
    df['Resume_Summary'] = ''
    df['GitHub_Score'] = 0
    df['GitHub_Summary'] = ''
    df['Final_Score'] = 0
    
    # Re-order columns for clarity
    columns_order = [
        'Name', 
        'Resume_Path', 
        'GitHub_URL', 
        'Resume_Score', 
        'Resume_Summary',
        'GitHub_Score',
        'GitHub_Summary',
        'Final_Score'
    ]
    df = df[columns_order]

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)
    print(f"Successfully created '{csv_filename}'!")

if __name__ == "__main__":
    resume_data = scan_resumes(RESUME_FOLDER)
    if resume_data:
        save_to_csv(resume_data, OUTPUT_CSV)
        