import pandas as pd
import pdfplumber
import docx
import requests
import os
import json
import time
from urllib.parse import urlparse
from tqdm import tqdm
from openai import OpenAI, RateLimitError, APIError # <-- Import OpenAI
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# We'll use gpt-4o-mini - it's fast, cheap, and very smart.
OPENAI_MODEL = "gpt-4o-mini" 

JOB_DESCRIPTION = """
We are building an AI-powered enterprise SaaS platform. We’re looking for curious minds who think in systems and build for scale for a Backend Engineering Internship.

What you’ll do:
- Architect, build, and optimize AI-driven backend systems for Enstine.
- Work on data pipelines, APIs, and AI integration layers.
- Collaborate on research-to-production deployment of ML workflows.

What we expect:
- Strong computer science fundamentals (data structures, algorithms, OS, networks).
- Proficiency in Python, Java or any modern programming language.
- Understanding of SQL/NoSQL databases.
- Curiosity and hands-on experience in AI/ML, model training, and inference workflows.
- Bonus: Familiarity with frameworks like LangGraph, CrewAI, AutoGen, or similar AI
orchestration tools.
"""

INPUT_CSV = 'candidates.csv'
OUTPUT_CSV = 'candidates_ranked.csv'
RESUME_WEIGHT = 0.7  # 70% of the score is from the resume
GITHUB_WEIGHT = 0.3  # 30% is from GitHub

def extract_text_from_resume(file_path):
    """Extracts raw text from a PDF or DOCX file."""
    if not os.path.exists(file_path):
        print(f"  Error: File not found at {file_path}")
        return None
        
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            print(f"  Warning: Unsupported file type: {file_path}")
            return None
            
        if not text.strip():
            print(f"  Warning: No text extracted from {file_path} (possibly an image-based PDF).")
            return None
            
        return text
    except Exception as e:
        print(f"  Error reading file {file_path}: {e}")
        return None

def analyze_github_profile(github_url, github_token):
    """Fetches structured data from the GitHub API."""
    try:
        username = urlparse(github_url).path.strip('/')
        if not username:
            return "Error: Could not parse username from URL."

        # GitHub token is now optional but recommended
        headers = { "Accept": "application/vnd.github.v3+json" }
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers)
        if user_response.status_code != 200:
            return f"Error: Could not fetch GitHub user. Status: {user_response.status_code}"
            
        user_data = user_response.json()
        bio = user_data.get('bio', 'No bio provided.')
        
        repos_url = user_data.get('repos_url') + "?sort=pushed&per_page=5"
        repos_response = requests.get(repos_url, headers=headers)
        repos_data = repos_response.json()
        
        summary = f"GitHub Profile for: {username}\nBio: {bio}\n\nRecent Repositories:\n"
        
        if not repos_data or isinstance(repos_data, dict): # Check if it's an error dict
            summary += "- No public repositories found or API limit hit."
            return summary

        for repo in repos_data:
            repo_name = repo.get('name', 'N/A')
            repo_desc = repo.get('description', 'No description.')
            repo_lang = repo.get('language', 'N/A')
            summary += f"\n- Repo: {repo_name}\n  Language: {repo_lang}\n  Description: {repo_desc}\n"
            
        return summary
        
    except Exception as e:
        print(f"  Error analyzing GitHub profile: {e}")
        return f"Error: Could not analyze profile. {e}"

def get_combined_score_openai(client, model_name, resume_text, github_data, jd):
    """
    Sends ONE combined prompt to OpenAI and gets back a clean JSON score.
    Includes robust retry-logic for rate limit errors.
    """
    
    system_prompt = f"""
    You are an expert technical recruiter. Your task is to analyze a candidate's
    Resume and GitHub profile against a Job Description.
    Provide your response *only* in the following JSON format, with no other text.
    {{
      "resume_score": <An integer score from 0-100 for the RESUME fit>,
      "github_score": <An integer score from 0-100 for the GITHUB project relevance>
    }}
    """
    
    user_prompt = f"""
    --- JOB DESCRIPTION ---
    {jd}
    
    --- 1. CANDIDATE RESUME TEXT ---
    {resume_text}
    
    --- 2. CANDIDATE GITHUB DATA ---
    {github_data}
    """
    
    while True:
        try:
            response = client.chat.completions.create(
                model=model_name,
                response_format={"type": "json_object"}, # <-- This ensures clean JSON
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            # Parse the JSON string from the response
            response_data = json.loads(response.choices[0].message.content)
            return response_data
            
        except RateLimitError as e:
            print("  --- Rate Limit Hit ---")
            print("  Sleeping for 30 seconds...")
            time.sleep(30)
            print("  Retrying...")
            continue
            
        except APIError as e:
            print(f"  An OpenAI API error occurred: {e}")
            return None # Fail this candidate
        
        except Exception as e:
            print(f"  An unexpected error occurred during API call: {e}")
            return None # Fail this candidate

def main():
    if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        print("ERROR: Please set your OPENAI_API_KEY in the script.")
        return
        
    # We no longer need the GITHUB_TOKEN, but it's good for reliability
    # You can remove it if you don't have one
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Warning: GITHUB_TOKEN not set. GitHub analysis may be rate-limited.")

    # Initialize the OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Load the CSV
    try:
        # We still define the dtypes for columns that exist in the CSV
        df = pd.read_csv(INPUT_CSV, dtype={
            'Resume_Summary': 'str', 
            'GitHub_Summary': 'str', 
            'Final_Score': 'float'
        })
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {INPUT_CSV}")
        return

    print(f"Starting to process {len(df)} candidates using OpenAI {OPENAI_MODEL}...")

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Ranking Candidates"):
        
        if pd.isna(row['GitHub_URL']) or not str(row['GitHub_URL']).strip():
            continue 

        if row['Final_Score'] > 0:
            continue

        print(f"\nProcessing {row['Name']} (Row {index})...")
        
        resume_text = "No resume text could be extracted."
        github_data = "No GitHub data could be fetched."
        
        try:
            # --- 1. Gather Data ---
            print("  Extracting resume text...")
            extracted_resume = extract_text_from_resume(row['Resume_Path'])
            if extracted_resume:
                resume_text = extracted_resume

            print("  Fetching GitHub data...")
            fetched_github = analyze_github_profile(row['GitHub_URL'], github_token)
            if fetched_github:
                github_data = fetched_github

            # --- 2. Make ONE API Call ---
            print("  Sending combined data to OpenAI for analysis...")
            analysis = get_combined_score_openai(
                client, OPENAI_MODEL, resume_text, github_data, JOB_DESCRIPTION
            )
            
            if analysis:
                # --- 3. Populate DataFrame (No Summaries) ---
                resume_score = analysis.get('resume_score', 0)
                github_score = analysis.get('github_score', 0)
                
                df.loc[index, 'Resume_Score'] = resume_score
                df.loc[index, 'GitHub_Score'] = github_score
                
                # --- 4. Calculate Weighted Score ---
                final_score = (resume_score * RESUME_WEIGHT) + (github_score * GITHUB_WEIGHT)
                df.loc[index, 'Final_Score'] = round(final_score, 2)
                
                print(f"  Done. Resume: {resume_score}, GitHub: {github_score}, Final: {final_score}")
                
            else:
                print("  Error: OpenAI analysis failed.")
                df.loc[index, 'Final_Score'] = -1

            # --- 5. Save progress ---
            if (index + 1) % 5 == 0:
                df.to_csv(OUTPUT_CSV, index=False)

        except Exception as e:
            print(f"\n--- CRITICAL ERROR on {row['Name']} (Row {index}) ---")
            print(f"  Error: {e}")
            df.loc[index, 'Final_Score'] = -1 
            
        # We can sleep for 1 second. OpenAI's rate limits are high.
        # The function itself will sleep if it hits a limit.
        time.sleep(1) 

    # --- Final Sort and Save ---
    print("\nProcessing complete. Sorting and saving final results...")
    df_final = df.sort_values(by='Final_Score', ascending=False)
    df_final.to_csv(OUTPUT_CSV, index=False)

    print(f"Success! All candidates have been ranked and saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
    