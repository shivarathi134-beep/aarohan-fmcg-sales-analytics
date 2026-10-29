# GitHub Publishing Guide

1. Create a new **empty** GitHub repository named `aarohan-fmcg-sales-analytics` (do not prepopulate README/LICENSE because the project already contains them).
2. Install Git for Windows if needed. Open Terminal in the extracted project directory.
3. Run:

```bash
git init
git add .
git status
git commit -m "Add Aarohan FMCG analytics portfolio project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aarohan-fmcg-sales-analytics.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. If you already initialized the local repository, do not repeat `git init`; check `git status` and `git remote -v` first.

Before pushing, review `git status` and ensure no passwords, connection strings, credentials, employer/client data, downloaded private data or unnecessary large files are staged. This project uses synthetic data. The ZIP includes project data and outputs; you may use GitHub Releases if you prefer to distribute a separate bundle. Do not upload a `.pbix` before building and validating it yourself.

**Publishing status:** no repository has been created or pushed on your behalf. This guide is for your manual publishing.
