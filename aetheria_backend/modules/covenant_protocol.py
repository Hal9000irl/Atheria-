import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

class CovenantProtocol:
    """Manages all database interactions with Firestore, tracking the
    user-Aetheria relationship (the 'covenant')."""
    def __init__(self):
        print("Initializing Covenant Protocol (Firestore)...")
        # Use GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
        if not firebase_admin._apps:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("Firestore client initialized.")

    def _get_user_ref(self, user_id):
        return self.db.collection("users").document(user_id)

    def get_history(self, user_id, limit=20):
        """Retrieves the last N messages for a given user."""
        messages_ref = self._get_user_ref(user_id).collection("conversations")
        query = messages_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def get_milestones(self, user_id):
        """Retrieves all milestones for a given user."""
        milestones_ref = self._get_user_ref(user_id).collection("emotional_milestones")
        docs = milestones_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        return [doc.to_dict() for doc in docs]

    def log_interaction_and_update_trust(self, user_id, user_text, aetheria_text, emotion_data):
        """Logs a conversation turn and updates the covenant state."""
        user_ref = self._get_user_ref(user_id)
        batch = self.db.batch()
        timestamp = datetime.now(timezone.utc)

        # Log user message
        convo_ref_user = user_ref.collection("conversations").document()
        batch.set(convo_ref_user, {
            "text": user_text, "sender": "user", "timestamp": timestamp
        })

        # Log Aetheria's message
        convo_ref_aetheria = user_ref.collection("conversations").document()
        batch.set(convo_ref_aetheria, {
            "text": aetheria_text, "sender": "aetheria", "timestamp": timestamp,
            "emotion_context": emotion_data.get('primary_emotion')
        })

        # Update trust score and covenant state
        covenant_ref = user_ref.collection("covenant_state").document("current")
        
        # Simple trust update logic
        trust_increment = 0.0
        if emotion_data.get('primary_emotion') in ['love', 'joy']:
            trust_increment = 0.01
        elif emotion_data.get('primary_emotion') in ['sadness', 'fear']:
            trust_increment = 0.02 # Trust grows more when vulnerability is shown
        elif emotion_data.get('primary_emotion') in ['anger', 'disgust']:
            trust_increment = -0.01

        update_data = {
            "last_interaction": timestamp,
            "trust_score": firestore.Increment(trust_increment),
            "total_interactions": firestore.Increment(1)
        }
        batch.set(covenant_ref, update_data, merge=True)
        
        batch.commit()

        # Check for new milestones (after commit)
        new_milestone = self._check_for_milestones(user_id, emotion_data)
        
        current_covenant_state = covenant_ref.get().to_dict() or {}
        
        return {
            "milestone": new_milestone,
            "trust_score": current_covenant_state.get('trust_score', 0.5) + trust_increment
        }

    def _check_for_milestones(self, user_id, emotion_data):
        """Checks if a new milestone has been achieved and logs it."""
        # This is a simplified example. A real system would have more complex checks.
        milestone = None
        if emotion_data.get('primary_emotion') == 'fear' and emotion_data.get('intensity') > 0.8:
            milestone = {
                "description": "A Moment of Deep Vulnerability",
                "emotion": "fear"
            }
        
        if milestone:
            milestones_ref = self._get_user_ref(user_id).collection("emotional_milestones")
            milestones_ref.add({
                **milestone,
                "timestamp": datetime.now(timezone.utc)
            })
            return milestone
        return None