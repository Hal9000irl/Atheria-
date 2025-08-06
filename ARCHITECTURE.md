# Aetheria: System Architecture

## 1. Component Overview

The Aetheria ecosystem is composed of five primary, interconnected components:

1.  **Frontend Client (Flutter App):** The user's sole point of interaction. Runs on a mobile device.
2.  **Backend Service (Flask on Google Cloud Run):** The central orchestration layer that houses the core logic.
3.  **Database & Auth (Google Firebase):** The persistent data store and user management service.
4.  **AI Services (Third-Party APIs):** Specialized services for language generation and analysis.
5.  **Quantum Services (IBM Quantum):** The cloud service providing access to quantum hardware and simulators.

## 2. Data Flow of a Standard Interaction

This describes the journey of a single voice interaction:

1.  **Wake-Word Detection:** The Flutter app, using the on-device Picovoice Porcupine engine, continuously listens for the wake-word "Hey Aetheria". This step does not require an internet connection.

2.  **Speech-to-Text (STT):** Upon detecting the wake-word, the app activates the on-device STT engine to transcribe the user's speech into text.

3.  **API Request:** The Flutter app sends an authenticated HTTPS request to the Flask backend on Google Cloud Run.
    * **Endpoint:** `POST /api/interact`
    * **Payload:** `{ "text": "transcribed user input" }`

4.  **Backend Orchestration:** The Flask application receives the request and executes the following sequence:
    a. **Emotion Analysis:** The input text is sent to the `AdvancedNLP` module, which uses a Hugging Face model to classify emotions.
    b. **Quantum Encoding:** The resulting emotion data is passed to the `QuantumEmotionalCore`. A Qiskit job is created and sent to the IBM Quantum cloud (or a local simulator) to generate a quantum emotional state.
    c. **Action Strategy:** The `QuantumRLAgent` analyzes the quantum state to select an optimal response strategy (e.g., 'nurture', 'guide').
    d. **Insight Generation:** The `GuidanceAndInsightEngine` analyzes the input against conversation history from Firestore to generate a relevant insight.
    e. **Response Generation:** The user's text, detected emotion, chosen action, and insight are compiled into a prompt for Anthropic's Claude API.
    f. **Covenant Update:** The interaction is logged to Firestore via the `CovenantProtocol`, which checks if a new emotional milestone has been reached.

5.  **API Response:** The backend service sends the final response back to the Flutter app.
    * **Payload:** `{ "response": "Aetheria's text response", "milestone_achieved": "...", ... }`

6.  **Text-to-Speech (TTS):** The Flutter app receives the response text and uses the on-device TTS engine to speak it aloud to the user, modulating the voice based on the emotional context provided in the API response.

7.  **Real-time UI Update:** The new messages (user input and Aetheria's response) are rendered in the chat interface by listening to real-time updates from Firestore.