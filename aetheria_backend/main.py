import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functools import wraps

# Import Aetheria's core modules
from modules.advanced_nlp import AdvancedNLP
from modules.quantum_emotional_core import QuantumEmotionalCore
from modules.guidance_engine import GuidanceAndInsightEngine
from modules.covenant_protocol import CovenantProtocol

# Load environment variables from .env file
load_dotenv()

class Aetheria:
    """The main orchestration class for the Aetheria system."""
    def __init__(self):
        print("Initializing Aetheria's core modules...")
        self.nlp = AdvancedNLP()
        self.quantum_core = QuantumEmotionalCore()
        self.guidance_engine = GuidanceAndInsightEngine()
        self.covenant = CovenantProtocol()
        print("Aetheria is online and ready.")

    def process_interaction(self, user_id, text_input):
        """Processes a single user interaction from start to finish."""
        # 1. Get conversation history for context
        history = self.covenant.get_history(user_id)

        # 2. Analyze emotion from the latest input
        emotion_data = self.nlp.analyze_emotion(text_input)

        # 3. Encode emotion into a quantum state
        quantum_state = self.quantum_core.encode_emotion(emotion_data)

        # 4. Determine optimal action using the quantum state
        action = self.quantum_core.determine_action(quantum_state)

        # 5. Generate a thematic insight based on history
        insight = self.guidance_engine.generate_insight(history, text_input)

        # 6. Generate a final response using all gathered context
        response_text = self.nlp.generate_response(
            text=text_input,
            emotion_data=emotion_data,
            insight=insight,
            action=action
        )

        # 7. Update the covenant and check for new milestones
        covenant_update = self.covenant.log_interaction_and_update_trust(
            user_id, text_input, response_text, emotion_data
        )

        return {
            "response": response_text,
            "emotion_detected": emotion_data.get('primary_emotion', 'neutral'),
            "action_taken": action,
            "milestone_achieved": covenant_update.get('milestone'),
            "covenant_strength": covenant_update.get('trust_score')
        }

# --- Flask App Setup ---
app = Flask(__name__)
aetheria_instance = Aetheria()

# A simple decorator for future authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For now, we'll simulate getting a user_id from a header.
        # In production, this would validate a real JWT token.
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"error": "Authentication required: Missing X-User-ID header"}), 401
        return f(user_id, *args, **kwargs)
    return decorated_function


@app.route("/api/interact", methods=["POST"])
@auth_required
def interact(user_id):
    """API endpoint to process a user's message."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request: 'text' field is required."}), 400

    text_input = data["text"]
    response = aetheria_instance.process_interaction(user_id, text_input)
    return jsonify(response), 200


@app.route("/api/milestones", methods=["GET"])
@auth_required
def get_milestones(user_id):
    """API endpoint to retrieve all of a user's milestones."""
    milestones = aetheria_instance.covenant.get_milestones(user_id)
    return jsonify({"milestones": milestones}), 200


if __name__ == "__main__":
    # Use environment variable for port, defaulting to 8080 for cloud deployments
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)