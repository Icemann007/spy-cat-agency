# 😼 Spy Cat Agency API

A robust backend RESTful API for the Spy Cat Agency, designed to manage field operatives (cats), top-secret missions, and high-value targets. This service provides a complete system for creating cats, orchestrating missions with multiple targets, and tracking their progress from assignment to completion.

Built with a focus on **validation** and **correct business logic**, featuring:
* 🛡️ **Complex Validation Rules**: Ensures data integrity, such as preventing deletion of assigned missions or freezing notes on completed targets.
* 🔗 **Third-Party Service Integration**: Validates cat breeds against the official TheCatAPI.
* 🚀 **Nested Operations**: Allows creating a mission and its targets in a single atomic request.
* 📚 **Auto-generated Swagger Documentation**: Interactive and detailed API documentation powered by `drf-spectacular`.

---

## 🚀 Key Features

* **Spy Cats Management**: Full CRUD operations for spy cats, with specialized, secure updates for sensitive data like salary.
* **Mission Control**: Create missions with a defined range of targets (1-3) in a single request. Delete missions only if they are not assigned.
* **Cat Assignment**: Assign available cats to unassigned missions. The system validates that a cat is not already on an active mission.
* **Target Updates**: Update target notes and mark targets as complete. The API enforces rules to prevent modification of completed items.
* **Automatic Mission Completion**: A mission is automatically marked as complete once all its associated targets are completed.
* **External Breed Validation**: Ensures that only real cat breeds are added to the system by validating against TheCatAPI.

---

## 🛠️ Requirements

* Python 3.10+
---

## 📥 Installation

### 💻 Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Icemann007/spy-cat-agency
    cd spy-cat-agency-api
    ```

2.  **Create and activate a virtual environment:**

    * On **Windows**:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

    * On **macOS/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables:**
    Create a `.env` file in the project root based on the provided `.env.sample`. Update it with your configuration:
    ```ini
    # Django settings
    SECRET_KEY="your-super-secret-key-for-django"

    # TheCatAPI URL for breed validation
    CAT_API_URL="https://api.thecatapi.com/v1/breeds"
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

---

## ⚙️ API Endpoints & Workflow

The API is structured around two main resources: **Cats** and **Missions**. Below is a comprehensive guide to all available endpoints.

### 😼 Spy Cats Endpoints

These endpoints manage the roster of spy cat operatives.

---

#### List Cats
* **Endpoint**: `GET /api/cats/`
* **Description**: Retrieves a list of all spy cats currently in the system.
* **Success Response (`200 OK`)**:
    ```json
    [
        {
            "id": 1,
            "name": "Whiskers",
            "years_of_experience": 5,
            "breed": "Siamese",
            "salary": "5000.00"
        }
    ]
    ```

---

#### Create a Cat
* **Endpoint**: `POST /api/cats/`
* **Description**: Adds a new spy cat to the agency.
* **Business Logic**:
    * The `breed` is validated against TheCatAPI to ensure it's a real breed.
    * `salary` must be a positive value.
* **Request Body**:
    ```json
    {
      "name": "Shadow",
      "years_of_experience": 3,
      "breed": "Bombay",
      "salary": "3500.00"
    }
    ```

---

#### Retrieve a Specific Cat
* **Endpoint**: `GET /api/cats/{id}/`
* **Description**: Fetches the detailed profile of a single spy cat by their ID.

---

#### Update a Cat's Salary
* **Endpoint**: `PATCH /api/cats/{id}/`
* **Description**: Updates **only the salary** of a specific cat. Any other fields sent in the request will be ignored for security reasons.
* **Request Body**:
    ```json
    {
      "salary": "5500.00"
    }
    ```

---

#### Delete a Cat
* **Endpoint**: `DELETE /api/cats/{id}/`
* **Description**: Permanently removes a spy cat from the agency roster.
* **Success Response**: `204 No Content`

---


### 🎯 Missions & Targets Endpoints

These endpoints are for creating and managing missions.

---

#### List Missions
* **Endpoint**: `GET /api/missions/`
* **Description**: Retrieves a list of all missions, including their assigned cat (if any) and nested targets.

---

#### Create a Mission
* **Endpoint**: `POST /api/missions/`
* **Description**: Creates a new mission along with its targets in a single atomic request.
* **Business Logic**:
    * A mission must be created with 1 to 3 targets.
* **Request Body**:
    ```json
    {
      "targets": [
        {
          "name": "Dr. Evil's Volcano Lair",
          "country": "Iceland",
          "notes": "Intel suggests a secret entrance behind the waterfall."
        }
      ]
    }
    ```

---

#### Retrieve a Specific Mission
* **Endpoint**: `GET /api/missions/{id}/`
* **Description**: Fetches detailed information about a single mission, including its status, assigned cat, and all targets.

---

#### Assign a Cat to a Mission
* **Endpoint**: `PATCH /api/missions/{id}/assign/`
* **Description**: Assigns an available cat to an unassigned mission.
* **Business Logic**:
    * A cat cannot be assigned if they are already on another active (incomplete) mission.
* **Request Body**:
    ```json
    {
      "cat_id": 1
    }
    ```

---

#### Update a Mission's Target
* **Endpoint**: `PATCH /api/missions/{mission_id}/targets/{target_id}/`
* **Description**: Updates the `notes` or `is_complete` status of a single target within a mission.
* **Business Logic**:
    * `notes` cannot be updated if the target or the entire mission is already complete.
    * If this update marks the **last** incomplete target as complete, the parent mission's `is_complete` status will automatically be set to `true`.
* **Request Body Examples**:
    * To update notes:
        ```json
        { "notes": "Target acquired. Awaiting extraction." }
        ```
    * To complete the target:
        ```json
        { "is_complete": true }
        ```

---

#### Delete a Mission
* **Endpoint**: `DELETE /api/missions/{id}/`
* **Description**: Deletes a mission.
* **Business Logic**:
    * A mission **cannot** be deleted if it already has a cat assigned to it.
    * If you attempt to delete an assigned mission, the server will return a `409 Conflict` error.
* **Success Response**: `204 No Content`

## ✅ Setup Complete

You have successfully reviewed the project setup and API documentation. The application is now ready for deployment and use.

For any further questions, please refer to the auto-generated Swagger documentation or inspect the source code.
