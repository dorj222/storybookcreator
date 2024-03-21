# Storybook Co-Creator

This application, developed with Django, functions as the backend system for a Unity frontend application, forming a cohesive Human-AI interactive environment. The platform is central to a thesis project aimed at exploring perceived ownership in human-AI co-creations, with a specific focus on the process of children's storybook creation. Empowered with Django, Django Ninja, and various AI models, it ensures smooth management of storybooks, image operations, and story descriptions in multiple languages.

## Features

- **Storybooks Management:** Facilitates the creation, retrieval, update, and deletion of storybooks via dedicated REST API endpoints
- **Image Management:** Utilizes Stable Diffusion XL Turbo for the enhancement of images and provides supportive REST API endpoints for image-related operations
- **Description Management:** Integrates BLIP and TinyLlama AI models to generate story descriptions for storybooks and allows their management via dedicated REST API endpoints
- **Multilingual Support:** Incorporates Seamless LLM model to translate English text into German, supported by a designated REST API endpoint
- **SQLite Database:** The application uses SQLite for data storage

## Requirements

- Python 3.x
- Django
- Django Ninja
- SQLite

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/dorj222/storybookcreator.git
    cd storybookcreator
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
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
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
    wget https://civitai.com
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
  - `GET /storybooks`: Retrieve all storybooks
  - `GET /storybooks/{storybook_id}`: Retrieve a storybook by ID
  - `POST /storybooks`: Create a new storybook
  - `PUT /storybooks/{storybook_id}`: Update a storybook by ID
  - `DELETE /storybooks/{storybook_id}`: Delete a storybook by ID

- **Images:**
  - `GET /images/{storybook_id}`: Retrieve images associated with a storybook
  - `POST /images/{storybook_id}`: Upload a new image for a storybook
  - `PUT /images/{image_id}`: Update an image by ID
  - `DELETE /images/{image_id}`: Delete an image by ID

- **Descriptions:**
  - `GET /descriptions/getall/{storybook_id}/`: Retrieve all descriptions associated with a storybook
  - `GET /descriptions/{description_id}/`: Retrieve a description by ID
  - `POST /descriptions/{storybook_id}/{image_id}`: Upload a new description
  - `PUT /descriptions/{description_id}`: Update a description by ID
  - `DELETE /descriptions/{description_id}`: Delete a description by ID

- **LLM Features**
  - `PUT /chat/translations`: Translate an English text to a target language
  - `PUT /chat/titles`: Generate a storybook title

## License

This project is licensed under the [MIT License](LICENSE).
