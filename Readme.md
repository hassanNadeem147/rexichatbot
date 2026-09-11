# RexiChatbot

RexiChatbot is an AI application with:

- A FastAPI backend
- A PostgreSQL user database
- Login and registration
- AI operations for summarizing, explaining, translating, and podcast writing
- A browser frontend served by Nginx
- Docker support for the backend and frontend

## How The Application Works

1. The frontend runs in a browser at `http://localhost:3000`.
2. The frontend sends login, registration, and chat requests to the backend.
3. The backend runs at `http://localhost:8000`.
4. The backend connects to PostgreSQL and creates the `users` table at startup.
5. The backend sends text requests to the configured Google Gemini model.

This project does not create a PostgreSQL container. PostgreSQL must already be installed and running on the host computer.

## Main Features

- Create a user account
- Log in and receive a JWT access token
- Summarize text
- Explain a topic
- Translate text into another language
- Generate a two-speaker podcast script with Host and Guest turns
- View the API documentation in Swagger UI

## Requirements

Install these tools before starting:

- Docker Desktop with Docker Compose
- PostgreSQL 14 or newer
- A Google Gemini API key

For local, non-Docker development, also install Python 3.12 or newer.

## Environment Configuration

The backend reads settings from `.env`. The real `.env` file must not be committed or shared because it contains secrets.

Create `.env` in the project root and fill these variable names with your own local values. Do not paste real values into this README or into GitHub:

```env
GOOGLE_API_KEY=<your_google_api_key>
GOOGLE_MODEL=gemini-3.5-flash-lite
TEMPERATURE=0.7

DATABASE_USER=postgres
DATABASE_PASSWORD=<your_database_password>
DATABASE_HOST=host.docker.internal
DATABASE_PORT=5432
DATABASE_NAME=users

JWT_SECRET_KEY=<your_long_random_jwt_secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The current Docker setup uses `host.docker.internal` so the backend container can reach PostgreSQL on Windows and Docker Desktop. Make sure PostgreSQL accepts connections on port `5432`, and make sure the database named `users` exists.

Create the database from `psql` if it does not exist:

```powershell
psql -U postgres -h localhost -c "CREATE DATABASE users;"
```

If the database already exists, PostgreSQL will return an error. That is safe to ignore.

## Start With Docker

Open PowerShell in the project folder:

```powershell
cd D:\dockerpractice\2nd\RexiChatbot
```

Build the images and start both services in the background:

```powershell
docker compose up -d --build
```

This starts:

| Service | Container port | Computer URL |
| --- | ---: | --- |
| Backend | 8000 | `http://localhost:8000` |
| Frontend | 80 | `http://localhost:3000` |

Open the application at `http://localhost:3000`.

Open the backend API documentation at `http://localhost:8000/docs`.

## Docker Commands

Show running services:

```powershell
docker compose ps
```

Follow logs for both services:

```powershell
docker compose logs -f
```

Follow backend logs only:

```powershell
docker compose logs -f backend
```

Follow frontend logs only:

```powershell
docker compose logs -f frontend
```

Show the last 100 log lines:

```powershell
docker compose logs --tail=100
```

Restart services:

```powershell
docker compose restart
```

Stop and remove containers and the Compose network:

```powershell
docker compose down
```

Stop and remove containers, network, and anonymous volumes:

```powershell
docker compose down -v
```

Rebuild everything after changing Python or frontend code:

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

Build one service only:

```powershell
docker compose build backend
docker compose build frontend
```

Open a shell inside a container:

```powershell
docker compose exec backend sh
docker compose exec frontend sh
```

## Check That Services Work

Check the backend health endpoint:

```powershell
Invoke-RestMethod http://localhost:8000/
```

Check the frontend response:

```powershell
Invoke-WebRequest http://localhost:3000/ | Select-Object StatusCode
```

Both commands should return HTTP status `200`. The backend response should contain `status: Healthy`.

## API Examples

### Register a user

The password must contain exactly 8 characters because of the current request schema.

```powershell
$body = @{
    fullname = "John Doe"
    username = "johndoe12"
    email = "john@example.com"
    password = "<eight-character-password>"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8000/auth/register `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Log in

```powershell
$body = @{
    username = "johndoe12"
    password = "<eight-character-password>"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8000/auth/login `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

The login response contains an `access_token` and user information. The frontend stores this token in the browser for the current login session.

### Send a chat request

```powershell
$body = @{
    text = "Explain the history of Pakistan"
    operation = "explain"
    target_language = "English"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8000/chat/ `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Valid operation values are `summarize`, `explain`, `translate`, and `podcast`.

## Run Without Docker

This mode needs PostgreSQL running locally and a valid `.env` file.

Create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the backend from the project root:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

For local execution outside Docker, set this value in `.env`:

```env
DATABASE_HOST=localhost
```

Docker is recommended because it serves the frontend at `http://localhost:3000`. The frontend can also be opened from `frontend/index.html` or served with any static file server.

## Git And GitHub

Run these commands from the project folder. Replace `<github-repository-url>` with the URL of your own empty GitHub repository.

Check the current repository state:

```powershell
git status
```

Initialize Git if this folder is not already a repository:

```powershell
git init
git branch -M main
```

Review the files that will be committed. Confirm that `.env` is not listed:

```powershell
git status --short
```

Add the project files and create the first commit:

```powershell
git add .
git status
git commit -m "Initial RexiChatbot project"
```

Connect the local project to GitHub and push the `main` branch:

```powershell
git remote add origin <github-repository-url>
git remote -v
git push -u origin main
```

For later changes:

```powershell
git status
git add .
git commit -m "Describe the change"
git push
```

Clone the project on another computer:

```powershell
git clone <github-repository-url>
cd RexiChatbot
```

After cloning, create a new local `.env` file yourself. Never copy secrets into GitHub. The `.gitignore` and `.dockerignore` files are configured to exclude `.env`.

## Project Structure

```text
RexiChatbot/
|-- app/
|   |-- api/routes/              FastAPI routes for auth and chat
|   |-- config/settings.py       Environment settings
|   |-- core/security.py         Password hashing and JWT creation
|   |-- database/                SQLAlchemy engine, models, and startup setup
|   |-- graph/                   LangGraph workflow and AI nodes
|   |-- logging/logger.py        Console and file logging
|   |-- schemas/                 Request and response validation
|   |-- services/                User and authentication services
|   `-- main.py                  FastAPI application entrypoint
|-- frontend/
|   |-- index.html               Frontend HTML shell
|   |-- script.js                Login, registration, and chat behavior
|   |-- styles.css               Frontend styling
|   `-- Dockerfile               Nginx image for the frontend
|-- app/Dockerfile               Backend Docker image
|-- docker-compose.yaml          Backend and frontend services
|-- requirements.txt             Python dependencies
|-- .env                         Local settings; never commit this file
`-- Readme.md                    This guide
```

## Troubleshooting

### Backend exits during startup

Check backend logs:

```powershell
docker compose logs backend
```

Common causes are a missing `.env`, an invalid Google API key, or PostgreSQL not being reachable from Docker.

### Database connection errors

Check that PostgreSQL is running and listening on port `5432`. Confirm these values in `.env`:

```env
DATABASE_HOST=host.docker.internal
DATABASE_PORT=5432
DATABASE_NAME=users
DATABASE_USER=postgres
DATABASE_PASSWORD=your_postgres_password
```

### Port 3000 or 8000 is already in use

Find the process using a port:

```powershell
Get-NetTCPConnection -LocalPort 3000,8000 -ErrorAction SilentlyContinue
```

Stop the current Compose project:

```powershell
docker compose down
```

### The browser shows an old frontend

Rebuild the frontend without the Docker cache:

```powershell
docker compose build --no-cache frontend
docker compose up -d frontend
```

Then refresh the browser with `Ctrl+F5`.

### View all container names and ports

```powershell
docker ps -a
```

## Security Notes

- Never commit `.env`.
- Keep API keys, database passwords, JWT secrets, and user passwords outside GitHub.
- Use a long random value for `JWT_SECRET_KEY`.
- Do not use development secrets in production.
- Restrict CORS origins before production deployment.
### Contact me: hassan07892026@outlook.com
