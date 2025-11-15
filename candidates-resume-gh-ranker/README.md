## Goes through the resumes (pdf) and GitHub profile (url) and ranks them according to the JD

### Note:
- Put all the resumes into resumes/ folder (only supports pdf and docx)
- Then run create_csv.py (this will create a candidates.csv in the root project folder)
- Make changes in the candidates.csv accordinbgly (paste in the GitHub links for the candidates)
- Finally run rank_candidates.py

---
```graphql
candidates-resume-gh-ranker/
│── existing files
........
│── .env            
│── resumes/        
```
---

### .env format
```env
OPENAI_API_KEY=
GEMINI_API_KEY=
GITHUB_TOKEN=
```
---

### How to get the GITHUB_TOKEN?
#### GitHub Personal Access Token (PAT):

- This is essential for reliably reading GitHub profiles. Without it, you will be rate-limited and blocked very quickly.
- Go to your GitHub Developer Settings.
- Click "Generate new token" > "Generate new token (classic)".
- Give it a name (e.g., "CandidateRanker").
- Set an expiration (e.g., 7 days).
- Check the public_repo scope. This is all you need.
- Click "Generate token" and copy it immediately. You won't see it again.
- Paste the token into your .env (GITHUB_TOKEN=)

---

### check_models.py:
> WILL CHECK THE FOR THE GEMINI'S SUPPORTED MODELS

