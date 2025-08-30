# EcoQuests: The Sustainable Lifestyle Game

## Overview

EcoQuests is a gamified application designed to encourage sustainable living. The platform rewards users with experience points (XP) for completing eco-friendly quests, such as using public transport or participating in volunteer activities. By integrating gamification principles like user profiles, leaderboards, and skill progression, EcoQuests aims to make sustainability an engaging and rewarding experience.

## Features

  * **User Authentication**: Secure user registration and login.
  * **User Profiles**: Customizable profiles with an eco-rank, XP, and level progression.
  * **Dynamic Quests**:
      * **Transport Quests**: The app provides transport recommendations (e.g., walk, bicycle, bus) based on real-time traffic, weather, and distance data.
      * **Volunteer Quests**: Users can find local environmental volunteer opportunities.
  * **Gamification**:
      * **XP and Leveling**: Earn XP for completing quests to level up your user profile.
      * **Eco-Ranks**: Progress through ranks like Bronze, Silver, and Gold.
      * **Leaderboard**: Compete with friends on a global and friend-based leaderboard.
      * **Social Groups**: Add friends and form groups to track progress and compete together.

## Technology Stack

  * **Backend**: Django with Django REST Framework.
  * **Database**: Django's default ORM and database configurations.
  * **APIs**:
      * **Groq API**: Used for making smart decisions on transport modes.
      * **TomTom API**: Provides traffic and routing information.
      * **Weatherbit API**: Supplies real-time weather data.
      * **Photon (Komoot) API**: For converting addresses to geographical coordinates (lat/long).
      * **Volunteer Connector API**: Powers the search for local volunteer opportunities.

## Getting Started

### Prerequisites

Make sure you have the following installed:

  * Python 3.8+
  * pip
  * Git

### Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Set up a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: The `requirements.txt` file is not included in the provided code, but you will need to create one by listing the necessary packages like `django`, `djangorestframework`, `requests`, `pandas`, `python-dotenv`, `httpx`, `math`, and `asyncio`.*

4.  **Set up environment variables**:
    Create a `.env` file in the project's root directory and add your API keys. This is crucial for the application to function correctly.

    ```bash
    # .env
    GROQ_API="your_groq_api_key"
    WEATHER_KEY="your_weatherbit_api_key"
    TRAFFIC_KEY="your_tomtom_api_key"
    GROQ_MODEL="your_groq_model"
    ```

5.  **Run database migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Start the development server**:

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The following are the primary API endpoints available.

### User Endpoints

| Endpoint                      | Method | Description                                    |
| ----------------------------- | ------ | ---------------------------------------------- |
| `/user/register`              | `POST`   | Creates a new user account.                      |
| `/user/login`                 | `POST`   | Authenticates a user and returns a token.        |
| `/user/profile`               | `GET`    | Retrieves the current user's profile information.|
| `/user/group`                 | `POST`   | Adds a friend to a user's group.                 |
| `/user/friends`               | `GET`    | Lists all friends of the current user.           |
| `/user/leaderboard`           | `GET`    | Fetches the leaderboard of friends by XP.        |

### Quest Endpoints

| Endpoint                      | Method | Description                                                               |
| ----------------------------- | ------ | ------------------------------------------------------------------------- |
| `/quests/transport`           | `GET`    | Provides a transport recommendation based on real-time data.              |
| `/quests/volunteer`           | `GET`    | Searches and returns available environmental volunteer opportunities.       |
| `/quests/complete_quest`      | `POST`   | Submits a quest completion and grants XP to the user.                      |

## Code Structure

  * `models.py`: Defines the database models for `User` and `Group`. It includes a custom `UserManager` for handling user creation and a `save` method on the `User` model to automatically generate a `quest_id`.
  * `urls.py`: Manages the URL routing for the API, mapping each endpoint to its corresponding view function.
  * `views.py`: Contains the core logic for the API endpoints, handling user authentication, quest logic, and API calls to third-party services.
  * `serializers.py`: Defines the serializers for converting Django models to and from JSON format, primarily used for user registration and login.
  * `admin.py`: (Currently empty) Can be used to register models with the Django admin interface.

## How It Works

1.  **Transport Decision**: The `decideTransportOperation` view in `views.py` asynchronously fetches data from multiple APIs.
      * It uses **Photon** to get the coordinates of the user's home and work addresses.
      * It then calls the **TomTom** API to get traffic conditions and distance.
      * The **Weatherbit** API provides current weather information.
      * Finally, all this data is sent to the **Groq API** with a prompt to determine the most eco-friendly transport mode (e.g., "walk", "bus", "bicycle").
2.  **Quest Completion**: The `complete_quest` view handles quest submissions. When a user uploads a file as proof of completion, the system awards a random amount of XP and updates their profile.
3.  **User Progression**: The `User` model automatically updates the `quest_id` on save. The `quest.py` file contains the logic for leveling up and unlocking skills based on accumulated XP, though this logic isn't fully integrated with the Django models in the provided code.

## Contributing

Contributions are welcome\! If you'd like to improve EcoQuests, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing-feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.
