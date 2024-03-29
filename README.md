# PySide-HUG
Small project focused on creating a REST API for file upload and user access, and an windows app to consume this service.
Used as a technical appraisal by a company that ended up not hiring me.

## Implementation

### Requirements

* python3
* python-virtualenv
* python-pip
### Install

In your terminal:

1. Create a VirtualEnv:
```
virtualenv PySide-HUG\
```
2. Navigate into it:
```
cd PySide-HUG\
```
3. Activate the env source to your terminal:
```
.\Scripts\activate
```
4. Clone the repository:
```
git clone https://github.com/JGabrielGruber/PySide-HUG.git
```
5. Navigate into the project folder:
```
cd PySide-HUG\
```
6. Install the requirements:
```
pip install -r requirements.txt
```

### Observation
This project use TAB(not space) of the size 4.

### API usage
In your terminal, and inside the project folder:

1. Navigate to the api src folder:
```
cd api\
```
2. Start the hug server:
```
hug -f app.py
```

### APP usage
In your terminal, and inside the project folder:

1. Navigate to the app src folder:
```
cd app\
```
2. Start the App:
```
python app.py
```
