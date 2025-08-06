import re

class GuidanceAndInsightEngine:
    """Inspired by AEON-9, this engine finds thematic patterns in conversations."""
    def __init__(self):
        self.themes = {
            "duality": ["but", "however", "on the other hand", "either", "or"],
            "minimalism": ["simple", "focus", "core", "essence", "just", "only"],
            "tension": ["stress", "anxious", "pressure", "deadline", "conflict", "difficult"],
            "negative_space": ["pause", "nothing", "empty", "silence", "lack of"],
        }

    def generate_insight(self, conversation_history, latest_text):
        """
        Generates a simple, thematic insight based on keyword spotting.
        This is a heuristic model to be expanded upon later.
        """
        full_text = " ".join([msg.get('text', '') for msg in conversation_history])
        full_text += " " + latest_text
        full_text = full_text.lower()

        # Count occurrences of keywords for each theme
        theme_scores = {theme: 0 for theme in self.themes}
        for theme, keywords in self.themes.items():
            for keyword in keywords:
                theme_scores[theme] += len(re.findall(r'\b' + keyword + r'\b', full_text))

        # Find the most prominent theme, if any
        max_score = 0
        dominant_theme = None
        for theme, score in theme_scores.items():
            if score > max_score:
                max_score = score
                dominant_theme = theme
        
        if dominant_theme and max_score > 2: # Require at least 3 keyword hits
            return f"The theme of '{dominant_theme}' seems present in our discussion."
        
        return "The conversation is still unfolding."