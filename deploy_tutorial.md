# Tutorial: Build and Deploy

This guide explains how to build and deploy the Banking Transaction Simulator.

## Prerequisites
- Docker installed locally (for testing build).
- A GitHub account.
- An account on a cloud provider (e.g., [Render](https://render.com/), [Railway](https://railway.app/), or [Fly.io](https://fly.io/)). This guide uses **Render** as an example.

## Local Build (Docker)

To verify the application builds correctly locally:

1.  **Build the image:**
    ```bash
    docker build -t transacoes-bancarias .
    ```

2.  **Run with Docker Compose (includes Database):**
    ```bash
    docker-compose -f infra/docker-compose.yml up --build
    ```
    The API will be available at `http://localhost:8000`.

## Deployment on Render

### 1. Database Setup
The application requires a PostgreSQL database.
1.  Go to the Render Dashboard.
2.  Click **New +** -> **PostgreSQL**.
3.  Name: `transacoes-db`.
4.  Region: Choose one close to you.
5.  Plan: **Free**.
6.  Click **Create Database**.
7.  Copy the **Internal DB URL** (if deploying app on Render) or **External DB URL**. You will need the connection details: `Hostname`, `Port`, `Database`, `Username`, `Password`.

### 2. Application Deployment
1.  Push your code to a GitHub repository.
2.  Go to the Render Dashboard.
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository.
5.  **Name:** `transacoes-api`.
6.  **Runtime:** **Docker**.
7.  **Region:** Same as your database.
8.  **Instance Type:** **Free**.
9.  **Environment Variables:**
    Add the following variables (using values from your created database):
    - `DB_HOST`: The hostname of your database (e.g., `dpg-xxxx.oregon-postgres.render.com`).
    - `DB_PORT`: `5432`.
    - `DB_USER`: Your database username.
    - `DB_PASSWORD`: Your database password.
    - `DB_NAME`: Your database name.
    - `PORT`: `8000` (The internal port the app listens on).

10. Click **Create Web Service**.

Render will build the Docker image and deploy it. Once finished, you will get a public URL (e.g., `https://transacoes-api.onrender.com`).

## Verification
You can access the API documentation (Swagger UI) at:
`https://<your-app-url>/docs`
