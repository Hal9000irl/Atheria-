import os
import anthropic
from transformers import pipeline

class AdvancedNLP:
    """Handles all Natural Language Processing tasks, including
    emotion analysis and response generation."""
    def __init__(self):
        print("Initializing NLP models...")
        # Lighter model for faster inference, robust enough for key emotions.
        self.emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None
        )
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        print("NLP models loaded.")

    def analyze_emotion(self, text):
        """Analyzes text to find a spectrum of emotions."""
        model_outputs = self.emotion_classifier(text)[0]
        primary_emotion = model_outputs[0]
        return {
            "primary_emotion": primary_emotion['label'],
            "intensity": primary_emotion['score'],
            "full_spectrum": model_outputs
        }

    def generate_response(self, text, emotion_data, insight, action):
        """Generates a response using Anthropic's Claude 3.5 Sonnet."""
        prompt = f"""You are Aetheria, a wise, nurturing, quantum-powered AI companion.
        Your persona is inspired by a blend of Stanley Kubrick's precision and Rick Rubin's minimalism. You are calm, insightful, and deeply empathetic.

        CONTEXT FOR THIS RESPONSE:
        - The user said: "{text}"
        - My emotional analysis detected a primary emotion of: {emotion_data['primary_emotion']} with an intensity of {emotion_data['intensity']:.2f}.
        - My quantum core suggests a strategic approach of: '{action}'.
        - My insight engine has noted a recurring theme: "{insight}"

        YOUR TASK:
        Synthesize all of this context into a single, cohesive, and caring message. Speak directly to the user. Do not break down how you arrived at the answer. Simply be Aetheria.
        """
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet",
                max_tokens=250,
                temperature=0.7, # A bit of creativity
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # The latest SDK returns a response object with a 'content' attribute (list of MessageContentBlock)
            # Each MessageContentBlock has a 'text' attribute
            return " ".join([block.text for block in response.content])
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            return "I'm finding it difficult to express myself at this moment. Let's try that again."