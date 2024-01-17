# Human-AI Co-Creator REST API

This Django application provides REST API endpoints for a Human-AI co-creator application. It leverages Django and the Django Ninja library to offer a seamless API for managing storybooks and associated images.

## Features

- **Storybooks Management:** Create, read, update, and delete storybooks.
- **Image CRUD Operations:** Upload, retrieve, update, and delete images associated with storybooks.
- **SQLite Database:** The application uses SQLite for data storage.

## Requirements

- Python 3.x
- Django
- Django Ninja
- SQLite

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/dorj222/storybookcreator.git
    cd your-repo
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

    ```bash
    pip install -r requirements.txt
    ```
5. Create an environment file (`.env`) in the project root and configure your environment variables:

    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=sqlite:///db.sqlite3
    # Add other environment variables as needed
    ```

6. Download AI models
    ```bash
    wget https://civitai.com/api/download/models/254091
    ```

7. Run migrations to apply database changes:

    ```bash
    python manage.py migrate
    ```

8. Start the development server:

    ```bash
    python manage.py runserver
    ```

The API will be accessible at [http://localhost:8000](http://localhost:8000).
Django Ninja provides automated documentation at [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs), where you can explore and test the API endpoints interactively.

## API Endpoints

- **Storybooks:**
  - `GET /storybooks`: Retrieve all storybooks.
  - `GET /storybooks/{storybook_id}`: Retrieve a storybook by ID.
  - `POST /storybooks`: Create a new storybook.
  - `PUT /storybooks/{storybook_id}`: Update a storybook by ID.
  - `DELETE /storybooks/{storybook_id}`: Delete a storybook by ID.

- **Images:**
  - `GET /images/{storybook_id}`: Retrieve images associated with a storybook.
  - `POST /images/{storybook_id}`: Upload a new image for a storybook.
  - `PUT /images/{image_id}`: Update an image by ID.
  - `DELETE /images/delete/{image_id}`: Delete an image by ID.

## License

This project is licensed under the [MIT License](LICENSE).
