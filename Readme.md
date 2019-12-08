# Dependencies
- Python 3.6+
- Django 2.2 + 
- pandas, numpy, django-cors-headers
- React _(used for the dashboard rendering)_. throughout the project directory, this is in the folder called dashboard.


 # Procedure to get the application running on development machine
- Clone the application
- To run the backend web server side, with the appropriate venv activated, navigate to the project directory, make sure all dependencies are installed. Run **py manage.py runserver** assuming you are on windows based machine
- for the fronted, go to the dashboard folder inside the project directory, run **npm install** to install the JS packages used. After successful completion, then go ahead and run **npm start**. Alternatively, you can serve the build folder on a web server as static files
- There we go
# Running the command that picks the files 
- Setup a task/cron job that runs the command **py manage.py process_received_file**. this could run daily.
# NB
- The received file is expected to be named _dataset.csv_ and this should be placed in the folder _received_files_ which is should be within the project directory
- After the received file has been processed, it is moved to the folder _processed_files_ and this is renamed in the format **processed{YYYY-MM-DD}.csv**

# Email settings
In the settings files of the django project, declare valid email settings.
