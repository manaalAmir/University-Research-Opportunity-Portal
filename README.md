# University Research Opportunity Portal

## Project Overview

The University Research Opportunity Portal is a web-based application designed to help students discover research opportunities offered by faculty members. It provides a centralized place to view, create, update, and delete research opportunities.

## Technologies Used

- **Backend:** Python and Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, and JavaScript
- **API Testing:** Postman

## Features

- Create new research opportunities.
- View all available research opportunities.
- Retrieve a specific opportunity using its ID.
- Update existing research opportunities.
- Change an opportunity's status between Open and Closed.
- Delete research opportunities.
- Validate input data and return appropriate error responses.
- Store research opportunities in a MySQL database.

## Project Structure

```text
University Research Opportunity Portal/
├── backend/
├── frontend/
├── database/
├── postman/
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the project:

- Python 3
- XAMPP with MySQL, or a compatible MySQL server
- Visual Studio Code
- The VS Code Live Server extension (for the frontend)
- Postman (optional, for API testing)

## Database Setup

1. Open XAMPP Control Panel and start MySQL.
2. Open MySQL Workbench or phpMyAdmin.
3. Open the `database/schema.sql` file from this project.
4. Execute the SQL script. It creates the `ResearchOpportunity` database and the `opportunities` table.
5. Ensure MySQL is running on port `3306`, or update the port configuration if necessary.

## Backend Setup

Open a terminal in the project's `backend` folder.

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt and run:

```bat
venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside `backend/` using the following settings. Replace the values if your local MySQL configuration differs.

```text
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=ResearchOpportunity
```

The example assumes that MySQL's `root` account has no password. If your MySQL account uses a password, enter it in `DB_PASSWORD`.

Do not upload `.env` to GitHub.

### 5. Run the backend

```powershell
python app.py
```

The Flask API should be available at:

`http://127.0.0.1:5000`

Keep this terminal running while using the frontend.

## Frontend Setup

1. Open the project in Visual Studio Code.
2. Open the `frontend` folder.
3. Right-click `index.html`.
4. Select **Open with Live Server**.
5. The frontend should open in your browser.

Make sure the Flask backend and MySQL are running before testing the frontend.

## API Testing with Postman

1. Open Postman.
2. Import the collection JSON file from the `postman` folder.
3. Ensure the backend is running at `http://127.0.0.1:5000`.
4. Send the requests in the collection to test creating, retrieving, updating, and deleting opportunities, as well as validation and not-found responses.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/opportunities` | Retrieve all opportunities |
| GET | `/api/opportunities/<id>` | Retrieve one opportunity |
| POST | `/api/opportunities` | Create an opportunity |
| PUT | `/api/opportunities/<id>` | Update an opportunity |
| DELETE | `/api/opportunities/<id>` | Delete an opportunity |

## API Testing

The exported Postman collection is available in the `postman` folder. It contains requests for creating, retrieving, updating, and deleting opportunities, changing opportunity status, and testing validation and not-found responses.

## Security Note

Database credentials are stored in a local `.env` file and are not committed to the repository.