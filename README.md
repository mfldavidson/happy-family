# Happy Family Game
An application to allow users to play the game Happy Family (description and rules to follow) remotely over video conference.

# How to Run
_After the first time running through these steps, you can skip right to #6_
1. Clone the repository to your machine.
2. Set up a virtual environment and activate it.
3. Navigate to the directory where requirements.txt is located in the repo. Install all requirements by entering `pip install -r requirements.txt` in your shell.
4. Navigate to the directory where manage.py is located in the repo. Create the database by entering `python manage.py makemigrations` then `python manage.py migrate` in your shell from the same directory as manage.py.
5. Load the game status values by entering `python manage.py loaddata gamestatus.json` in your shell. This is required for the app to work properly.
6. Run the application by entering `python manage.py runserver` in your shell.
