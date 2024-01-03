# Team-Beta-GenAI
GenAI Hackathon project with Service Now : Automating Chatbot self-services.

# Installations
#### Install Flask

```bash
pip install Flask
``` 

# Create a Virtual Environment
```bash
python -m venv venv
``` 
<br>
 
```bash 
venv\Scripts\activate
```

# To Run Flask app
#### Start with installing requirements <br>
> Note: this is yet to be setup: 

```bash
pip3 install -r requirements.txt
```

#### Normally Run the application: 
```bash 
flask run 
```
#### Run with Debug for dynamic changes to reflect
```bash
flask --app run.py --debug run 
```

# Git Commands
NOTE:
- Always make changes in your local branch and not main
- Always pull from main andmake sure the merge conflicts if any are resolved. 
To pull from main
```bash
git pull origin main
```
To pull from branch onto your local branch copy
```bash
git pull origin <branchname>
```

### Check list of conflict files
```bash
git diff --name-only --diff-filter=U --relative
```

### Check current branch
```bash
git branch
```
To list all branches: 
```bash
git branch -a
```
### Switch between branches
```bash
git checkout <branch_name>
```

### Fetch new changes from main on local main.

```bash
git fetch
```

### To commit follow the steps:
Check status of of your branch
```bash
git status
```
Add the files to be commited
```bash
git add .
```
Commit the changes into your local branch
```bash
git commit -m '<commit message>'
```
Push commited changes to local branch
```bash
git push
```
### Pull Requests
- Go to your Github repository on the web browser and navigate to your branch. 
- Pull from main and make sure all merge conflicts are resolved.
- Create a pull request and assign reviewer. Add details to description as much as possible.


<br>

# ANONYMOUS COMMANDS
### Run without creating byte files.
```bash
python -B run.py
```