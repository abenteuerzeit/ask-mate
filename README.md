# AskMate

## TL;DR: 
AskMate is a question and answer platform that allows users to ask and answer questions, upvote or downvote questions and answers, and view a list of registered users. This sprint focuses on adding features such as user registration, login, and tracking the user who created each question, answer, and comment. To install AskMate, you will need Python 3.7 or later and pip, and will also need to set up a PostgreSQL database. The application will be running on `http://localhost:5000` after running python server.py.

## Sprint 3
This is the third sprint for the AskMate web application, which is a platform for users to ask and answer questions. The goal of this sprint is to add new features to the application, including user registration, login, and the ability to view a list of registered users. The application will also be updated to track the user who created each question, answer, and comment.

In this sprint, the development team will learn about web routing and redirects, the Gitflow workflow, advanced SQL commands, user authentication with sessions, hashed passwords, the Jinja2 templating engine, and basic DOM manipulation in JavaScript.

The tasks for this sprint include:
- Adding the ask-mate-3 repository as a remote to the repository from the previous sprint, then pulling and merging the code into it.
- Implementing a registration page that allows users to create a new account with a username (email address) and password. The new account should be saved in the database and the user should be redirected to the main page upon successful registration.
- Implementing a login page that allows registered users to log in with their username (email address) and password. Only logged-in users should be able to ask or answer questions.
- Implementing a page that displays a list of registered users with their attributes, including username, registration date, number of asked questions, answers, comments, and reputation (if implemented).
- Updating the application to track the user who created each question, answer, and comment.
- Implementing a user page that displays the user's attributes and a list of the questions, answers, and comments they have created.
- Implementing a feature that allows users to upvote or downvote questions, answers, and comments.
- Implementing a feature that displays the current logged-in user's name on the main page.
- Implementing a feature that allows users to edit their own questions and answers.
- Implementing a feature that displays the number of views for each question.

## Installation
To install Ask-Mate, you will need Python 3.7 or later and pip.
To configure the virtual environment for the Flask server, you will need to follow these steps:

1. Clone the repository and navigate to the root directory of the project:
    ```
    git clone https://github.com/abenteuerzeit/ask-mate.git
    cd ask-mate
    ```
2. Create a virtual environment and activate it:
    ```
    python3 -m venv env
    source env/bin/activate
    ```
3. The requirements.txt file lists the Python packages that are required for the project. This will install all the necessary Python packages, including Flask, that are required for the project. These packages can be installed by running `pip install -r requirements.txt` in a terminal, while in the project directory and with the virtual environment activated. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
4. You will also need a PostgreSQL database to run the project. You can download and install PostgreSQL from the [official website](https://www.postgresql.org/download/) or using your operating system's package manager.

5. Once you have PostgreSQL installed, create a new database and user for the project. You can do this using the `createdb` and `createuser` command-line utilities or by using a graphical tool such as [pgAdmin](https://www.pgadmin.org/).

6. Once the database and user are created, you need to set the environment variables to the values you used in `.env`. The .env file is used to store environment variables for the project. These variables can be accessed by the application at runtime. To use these variables in the application, you will need to use a package like python-dotenv to load the variables from the file. Then, you can access the variables in your Python code using `os.environ.get("VARIABLE_NAME")`, replacing `VARIABLE_NAME` with the name of the desired variable. It is important to note that the `.env` file should not be committed to version control or shared publicly, as it may contain sensitive information like passwords. Instead, it is common to use a separate `.env.example` file that contains dummy values for the environment variables:
    ```
    <PSQL_USER_NAME>: the username of the PostgreSQL user you created
    <PSQL_PASSWORD>: the password of the PostgreSQL user you created
    <PSQL_HOST>: the hostname or IP address of the machine where the PostgreSQL server is running
    <PSQL_DB_NAME>: the name of the PostgreSQL database you created
    ```
7. As a user, I would like to see a small drop in reputation when a user's question or answer is voted down.
- **A user loses reputation when:**
- their question is voted down: −2
- their answer is voted down: −2

Replace the `<PSQL_USER_NAME>`, `<PSQL_PASSWORD>`, `<PSQL_HOST>`, and `<PSQL_DB_NAME>` placeholders with the actual values you used for the database and user.

## PyCharm Virtual Environment

To run this project, you will need to have Python, PyCharm, and PostgreSQL installed on your machine.

1. Clone the repository and open the project in PyCharm.
2. Create a new Python virtual environment by going to `File > Settings > Project: [Project Name] > Project Interpreter`. Click on the gear icon and select "Add Local". Create a new virtual environment using the Python executable in your system.
3. Activate the virtual environment by going to the terminal in PyCharm and entering the command `source venv/bin/activate`
4. Install the required packages by navigating to the project directory in the terminal and entering the command `pip install -r requirements.txt`
5. Create a new PostgreSQL database and add the details (username, password, host, and database name) to the `.env` file.
6. In the terminal, navigate to the project directory and enter the command `psql -U [user name] -d [database name] -f sample_data/sample_data.sql` to load the sample data into the database.
7. Run the server by going to `Run > Run...` in the PyCharm menu and selecting `server.py`.
8. Open a web browser and go to `http://localhost:5000/` to view the website.

## Database Dump
Before running the application, you will need to create a PostgreSQL database and user with the connection details specified in the .env file. You can then create the necessary tables in the database by running the SQL commands in the `sample_data/sample_data.sql` file.
The sample_data folder contains a PostgreSQL database dump that can be used to populate the database with sample data. To use the sample data, you will need to have PostgreSQL installed on your machine and set up a new database for the project.

To load the sample data, open a terminal and navigate to the project directory. Then, enter the command psql -U <username> -d <database_name> -f sample_data/sample_data.sql, replacing <username> with your PostgreSQL username and <database_name> with the name of the database you created for the project. This will execute the SQL commands in the file and load the sample data into the database.

## Start

Once the dependencies are installed, you can start the application by running `python server.py` in your terminal. 
This will start the Flask development server, and the application will be available at `http://localhost:5000/` in your web browser.
You can access it by opening your web browser and entering this address.
If you make any changes to the code, you will need to stop the server and start it again for the changes to take effect.

## Features
- Ask and answer questions on various topics
- Upvote or downvote both questions and answers
- View a list of registered users with their attributes and a list of the questions, answers, and comments they have created
- User registration and login
- Edit your own questions and answers
- Display the number of views for each question 

## Technologies
- Python
- Flask
- PostgreSQL
- Jinja2
- JavaScript
- HTML5
- CSS3

## Development team
- [Adrian Mróz](https://www.linkedin.com/in/abenteuerzeit/) 
- [Piotr Palacz](https://www.linkedin.com/in/piotr-palacz-6ab556197/)
- [Ryszard Majchrzak](https://www.linkedin.com/in/ryszard-majchrzak-795b70219/)

## Usage
To use the application, open your web browser and navigate to http://localhost:5000.

You can ask and answer questions, view a list of registered users, and upvote or downvote questions, answers, and comments if you are logged in. You can also edit or delete your own questions and answers.

## Contributing
If you would like to contribute to the development of AskMate, please follow the Gitflow Workflow.

### Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Push your branch to your fork.
Create a pull request to the develop branch of the main repository.
