# Eye Tracking System - Version 2.0
## Git Setup & Project Initialization Guide

This document explains how to properly set up Git for this project.

## Git Configuration

### Git Version
- **2.55.0.windows.5**

### User Identity
- **Name:** insert name
- **Email:** : insert email

---

## Steps

### 1. Install Git (One-Time)
Download Git for Windows and install with default settings from [git.scm.com](https://git-scm.com)

### 2: Verify Installaion 
Open **Git Bash** and run:
```bash git --version```

### 3: Configure Your Identity (One-Time)
Open **Git Bash** run:

```bash
git config --global user.name "insert name"
git config --global user.email "insert email"
```

### 4: Verify Your Identity
Open **Git Bash** and run:
```bash
git config --list
```

### 5: Setup defaults
Open **Git Bash** and run:

```bash
# Use LF line endings (recommended for most projects)
git config --global core.autocrlf input

# Make status/branch info colored
git config --global color.ui auto
```

### 6. Create a new repository 
In the **VS Code** terminal, run:

```bash
git init
```

### 7. Create a `.gitignore` file

1. In the **Explorer** panel (left sidebar), right-click your project root folder → **New File...**
2. Name the file `.gitignore`
3. Paste in the content you want to ignore (see below) 

### 8. Create a repo on GitHub (web)
1. Go to [github/com/new](https://github.com/new)
2. **Repository name:** `EyeTrackingSystem`
3. Check *Add a README file*
4. **Do not** add a `.gitignore` - you already have one locally 
5. Click **Create repository**

### 9. Connect to Github Repo (web)
1. Navigate to your the **VS Code terminal**
2. Link your local repo to the new remote 
```bash
git remote add origin
https://github.com/GreenFern18/Eye-Tracking-System.git
```
3. Make sure you're onthe main branch
```bash
git branch -M main
```
4. Stage everything (if you haven't committed yet)
```bash
git add .
```
5. First commit
```bash
git commit -m "Initial commit: Eye Tracking System v2.0"
```
6. Push (this will prompt for your GitHub credentials/token)
git push -u origin main