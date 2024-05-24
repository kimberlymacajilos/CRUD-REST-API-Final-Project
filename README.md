# CRUD-REST-API-Final-Project

Overview
This project utilizes Flask for creating a REST API with CRUD operations, JWT token-based authentication, and MySQL Workbench for database management. Postman serves as the client for testing API endpoints.

Ensure you have the following software installed:

- VSCODE or any Python IDE
- MySQL Workbench
- Postman

Setup
1. Download Files (api.py and test.py)
2. Create and activate your virtual environment. Search how to create virtual environment
3. Create a MySQL database or use an existing one
4. Install required Python packages in your virtual environment
   - pip install Flask
   - pip install Flask-MySQLdb
   - pip install Flask-JWT-Extended
5. Open api.py and adjust the following configurations
   - Modify MYSQL_USER and MYSQL_PASSWORD if using different credentials.
   - Set MYSQL_DB to your database schema name.
   - Update username and password in the login function.

Running the Project
1. Start the server
   - Run api.py in your IDE or terminal to start the Flask server.
2. Using Postman
   - Set the request type to POST and enter the address (e.g., 127.0.0.1:5000/login).
   - Set the body to JSON format and enter your username and password:
     {
       "username": "yourusername",
       "password": "yourpassword"
     }
   - Send the request to obtain an access token.

   To access the Data
   - Use the access token for authorization (select bearer token in Postman's Authorization tab).
   - Perform CRUD operations (POST, GET, PUT, DELETE) on your API endpoints (127.0.0.1:5000/your-endpoint).

Testing
1. Modify test.py. Customize the functions in test.py to test specific API endpoints.
2. Update username and password in test.py for JWT authentication.
3. Execute test.py to validate the functionality of your API endpoints.
