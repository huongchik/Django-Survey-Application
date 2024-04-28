# Survey Django Application

## Description

This Django-based application allows the creation, management, and participation in surveys, similar to Google Forms. Users can create surveys and questions through the admin interface, and participants can answer questions through a web interface. The application supports conditional logic for displaying questions based on previous answers. Users need to register and log in to participate in the surveys.

For testing, the application is accessible at [http://194.53.54.26:8001/surveys](http://194.53.54.26:8001/surveys).

## Features

- **Admin Interface**: Admin users can create and manage surveys, questions, and answers.
- **Conditional Questions**: Questions can be set to appear based on the responses to previous questions.
- **User Responses**: Participants' responses are saved and linked to their respective surveys and questions.
- **Web Interface**: Users can participate in surveys and their responses are dynamically updated based on the survey structure.
- **User Registration and Login**: Users must register and log in to participate in surveys, ensuring personalized and secure participation.

## Installation

### Manual Setup

1. **Clone the repository**:
    ```
    git clone https://github.com/huongchik/Django-Survey-Application.git
    cd survey-app
    ```

2. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

3. **Migrate the database**:
    ```
    python manage.py migrate
    ```

4. **Create an admin user**:
    ```
    python manage.py createsuperuser
    ```

5. **Run the server**:
    ```
    python manage.py runserver
    ```

### Docker Setup

1. **Build the Docker containers**:
    ```
    docker-compose build
    ```

2. **Start the project**:
    ```
    docker-compose up
    ```

This will set up the necessary services and start the development server accessible via the configured port.

## Usage

### Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin`. Use the credentials created during the `createsuperuser` step to log in.

- **Creating a Survey**: Navigate to the Surveys section and click "Add". Fill in the details such as title, start, and end dates.
- **Adding Questions**: Within a survey, you can add questions directly. Specify the type (text, choice, or multiple choice), dependencies, and required answers if applicable.
- **Managing Answers**: Questions have inline sections where answers can be added or edited.

### Participating in Surveys

- Access surveys at the designated URL provided by the server.
- **User Registration and Login**: Before participating, users must register and log in through the user interface.
- **Survey Participation**: Participants can choose a survey, view questions, and submit their responses based on the question format and dependencies.


