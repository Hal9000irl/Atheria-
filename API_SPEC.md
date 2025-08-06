# Aetheria API Specification v1.0

## Base URL: (Provided by Google Cloud Run deployment)

---

### **Endpoint: `/api/interact`**

* **Method:** `POST`
* **Description:** Processes a single user utterance and returns Aetheria's response.
* **Request Body:**
    ```json
    {
      "text": "string"
    }
    ```
* **Success Response (200 OK):**
    ```json
    {
      "response": "string",
      "emotion_detected": "string",
      "action_taken": "string",
      "milestone_achieved": "object | null",
      "covenant_strength": "float"
    }
    ```
* **Error Response (400 Bad Request):**
    ```json
    {
      "error": "string"
    }
    ```

---

### **Endpoint: `/api/milestones`**

* **Method:** `GET`
* **Description:** Retrieves all achieved emotional milestones for the authenticated user.
* **Request Body:** None
* **Success Response (200 OK):**
    ```json
    {
      "milestones": [
        {
          "milestone_id": "string",
          "description": "string",
          "timestamp": "string (ISO 8601)",
          "emotion": "string"
        }
      ]
    }
    ```

---
# Database Schema (Firestore)

* **Root Collection:** `users`
    * **Document:** `{userId}` (from Firebase Auth)
        * **Subcollection:** `profile`
            * **Document:** `data`
                * `{ name: "string", created_at: "timestamp" }`
        * **Subcollection:** `conversations`
            * **Document:** `{conversationId}` (auto-generated)
                * `{ text: "string", sender: "user|aetheria", timestamp: "timestamp", emotion: "string" }`
        * **Subcollection:** `emotional_milestones`
            * **Document:** `{milestoneId}` (auto-generated)
                * `{ description: "string", trigger_text: "string", timestamp: "timestamp" }`
        * **Subcollection:** `covenant_state`
             * **Document:** `current`
                * `{ trust_score: "float", last_interaction: "timestamp" }`