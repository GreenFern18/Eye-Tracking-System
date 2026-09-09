# Python Setup in VS Code

**Operation System** Windows 11
**VS Code Version** 1.136.2
**Python Version**  3.13.15

Follow these steps **once per project** to get a working Python
environment.

---

## 1. Prerequisites

Python 3.13 installed
Run `python --version` in a terminal

VS Code installed
**Python Extension** in VSC Code

---

## 2. Install the Python Extension in VS Code

1. Open VS Code → click the **Extensions** icon in the left sidebar
2. Search for **Python** by **Microsoft**
3. Click **Install**.

---

## 3. Open Your Project Folder

```
File → Open Folder → select your project directory
```

This gives VS Code a **workspace root**. Everything below runs
relative to this folder.

---

## 4. Open the Integrated Terminal

```
Terminal → New Terminal
```

The terminal opens at your project root. You should see your OS
prompt.

---

## 5. Create a Virtual Environment

Run **one** of these commands (pick whichever you prefer):

### Option A - `venv` (built into Python, recommend)

```powershell
python -m venv .venv
```

**Only run this once per project** If `.venv` already
exists, skip to step 6.

---

## 6. Activate the Virtual Environment

**Why** Activation adds the venv's `Scripts` folder to your
PATH so `python` and `pip` point *inside the venv* instead of
the system-wide install

### Windows PowerShell (default VS Code terminal)

```powershell
.venv\Scripts\Activate.ps1
```

If you see *running scripts is disabled on this system*,
run once in an **admin** PowerShell:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

...then close and reopen VS Code.

### Confirm it's active

Your prompt should now be prefixed with the venv name:

```
(.venv) PS C:\path\to\projects>
```

Also verify:

```powershell
python --version
# → Python 3.13.x (from the venv, not the system)

where python
# → C:\path\to\project\.venv\Scripts\python.exe    ← venv path first
```

---

## 7. Install Packages into the Venv

```powershell
# Upgrade pip itself first (good habit)
python -m pip install --upgrade pip

# Then install whatever you need
python -m pip install requests flask
```

**Always use `python -m pip ...`** (or just `pip ...` while
the venv is active) instead of bare `pip`, to guarentee you're
hitting the venv.

---

##