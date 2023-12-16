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
