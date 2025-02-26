# my_health_app
A webApp to help the user make the right decision about his nutrition.
### How to run and test:
This step-by-step guide is based on linux commands. Adapt them to your system if necessary.

1. Open the terminal and clone the repository:
`$ git clone https://github.com/daniele-bnm/my_health_app.git`
2. Now open the terminal the same of the project to use the following commands. Make sure to have Python 3.12 or higher.
3. Create a virtual environment:
`$ python3 -m venv myenv`
4. Activate the virtual environment:
`$ source myenv/bin/activate`
5. Install the required packages:
`$ pip install -r requirements.txt`
6. **Open the config.py file and configure the database:**
change the username, password and database name accordingly to your configuration. The format is:
`SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/name_of_the_db'`
7. Run:
`$ python3 run.py`

Change the python3 command with the one of your python version and system.

Link to download the database with already some data to try the app: https://drive.google.com/file/d/1pEK4J9YxtdeN414zM8_cNEsyMrlWpbzQ/view?usp=sharing

Next time you'll run the application, make sure to activate the virtual environment before running it.
Just repeat step 4 and 7 in the correct folder.

Repo now Archived.
Email me if you need anything :)
