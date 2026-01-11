# AMailer

AMailer is a secure and anonymous email sending service. It allows users to send messages without revealing their identity.

## Features

*   **Anonymous Sending:** Send emails without registration.
*   **Secure:** Uses SMTP with TLS encryption.
*   **Modern UI:** Clean and responsive interface built with Pico.css and custom styling.
*   **Validation:** Real-time input validation.
*   **Rate Limiting:** (Implied) Protection against abuse.

## Tech Stack

*   **Backend:** Python 3.11, FastAPI, Uvicorn, Pydantic, aiosmtplib.
*   **Frontend:** HTML5, CSS3 (Pico.css), Vanilla JavaScript.
*   **Containerization:** Docker / Podman.
*   **Testing:** Pytest, HTTPX.

## Getting Started

### Prerequisites

*   Docker or Podman
*   Make (optional, for convenience)

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AMailer
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root directory based on `.env.example`:
    ```env
    SMTP_SERVER=smtp.mail.ru
    SMTP_PORT=465
    SMTP_USERNAME=your_email@mail.ru
    SMTP_PASSWORD=your_app_password
    SMTP_FROM_EMAIL=your_email@mail.ru
    ```
    > **WARNING:** Never commit your `.env` file to version control. It contains sensitive passwords.

3.  **Run with Make:**
    ```bash
    make build
    make run
    ```
    The application will be available at `http://localhost:8000`.

4.  **Development Mode (Hot Reload):**
    ```bash
    make dev
    ```

### Hosting

This project is deployed on **Amvera**: [https://amailer-dfsavffc.amvera.io/](https://amailer-dfsavffc.amvera.io/)

### Project Structure

*   `app/`: Backend application code (API routes, services, schemas).
*   `static/`: Frontend assets (HTML, CSS, JS).
*   `tests/`: Unit and integration tests.
*   `main.py`: Application entry point.
