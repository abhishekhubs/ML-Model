
# ayurveda_bot.py
# Helper functions for the Ayurveda Chatbot

def extract_symptoms(text):
    """
    Extracts potential symptoms from user text.
    For simplicity, we'll just split by commas and strip whitespace if the input looks like a list,
    or look for keywords.
    """
    text = text.lower()
    
    found_symptoms = []
    
    # Check for direct comma-separated input
    if "," in text:
        parts = [p.strip() for p in text.split(",")]
        # Filter strictly if desired, or just pass them through
        return parts
        
    keyword_list = ["dry", "cold", "light", "anxiety", "insomnia", "bloating", "gas", "constipation", "pain", "tremors",
                   "hot", "sharp", "acid", "anger", "inflammation", "rashes", "heartburn", "fever", "burning", 
                   "heavy", "oily", "slow", "lethargy", "congestion", "mucus", "weight gain", "swelling", "depression"]
                   
    # Check for keywords in sentence if no commas
    for keyword in keyword_list:
        if keyword in text:
             found_symptoms.append(keyword)

    return found_symptoms if found_symptoms else None

def calculate_dosha(symptoms):
    """
    Calculates dosha scores based on symptoms.
    Returns a dictionary with scores for Vata, Pitta, and Kapha.
    """
    scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    
    # Simple mapping of symptoms to doshas
    vata_symptoms = ["dry", "cold", "light", "anxiety", "insomnia", "bloating", "gas", "constipation", "pain", "tremors"]
    pitta_symptoms = ["hot", "sharp", "acid", "anger", "inflammation", "rashes", "heartburn", "fever", "burning"]
    kapha_symptoms = ["heavy", "oily", "slow", "lethargy", "congestion", "mucus", "weight gain", "swelling", "depression"]
    
    if isinstance(symptoms, list):
        for symptom in symptoms:
            s = symptom.lower()
            # Check for partial matches or exact matches
            for v in vata_symptoms:
                if v in s: scores["Vata"] += 1
            for p in pitta_symptoms:
                if p in s: scores["Pitta"] += 1
            for k in kapha_symptoms:
                if k in s: scores["Kapha"] += 1
                
    return scores



# Data for Advanced Dosha Scoring
DOSHA_QUESTIONS = [
    {
        "question": "How would you describe your emotional state currently?",
        "options": [
            ("Anxiety, Fear", {"Vata": 2}),
            ("Irritability, Anger", {"Pitta": 2}),
            ("Sadness, Attachment", {"Kapha": 2}),
            ("Restlessness", {"Vata": 1}),
            ("Frustration", {"Pitta": 1}),
            ("Laziness", {"Kapha": 1})
        ]
    },
    {
        "question": "How is your energy level?",
        "options": [
            ("Very Low", {"Kapha": 2}),
            ("Unstable", {"Vata": 2}),
            ("Intense / Overactive", {"Pitta": 2}),
            ("Sluggish", {"Kapha": 1})
        ]
    },
    {
        "question": "What is your dominant thought pattern?",
        "options": [
            ("Overthinking", {"Vata": 2}),
            ("Perfectionism", {"Pitta": 2}),
            ("Rumination", {"Kapha": 2}),
            ("Racing thoughts", {"Vata": 1}),
            ("Critical thinking", {"Pitta": 1})
        ]
    },
    {
        "question": "How is your sleep quality?",
        "options": [
            ("Light / Broken sleep", {"Vata": 2}),
            ("Waking at 2–3 AM", {"Pitta": 2}),
            ("Oversleeping", {"Kapha": 2}),
            ("Trouble falling asleep", {"Vata": 1})
        ]
    }
]

def get_advanced_questions():
    """Returns the list of questions for advanced scoring."""
    return DOSHA_QUESTIONS

def calculate_advanced_dosha(answers):
    """
    Calculates scores based on the list of selected options.
    'answers' is a list of tuples (question_index, option_index).
    """
    scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    
    for q_idx, o_idx in answers:
        if 0 <= q_idx < len(DOSHA_QUESTIONS):
            options = DOSHA_QUESTIONS[q_idx]["options"]
            if 0 <= o_idx < len(options):
                points = options[o_idx][1]
                for dosha, value in points.items():
                    scores[dosha] += value
                    
    return scores

def get_imbalance(scores):
    """
    Determines the dominant imbalance based on scores.
    Detects Dual-Dosha if scores are close (within 1 point).
    """
    if not scores:
        return "None"
    
    if all(v == 0 for v in scores.values()):
        return "Unknown"

    # Sort scores by value descending
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    first = sorted_scores[0]
    second = sorted_scores[1]
    
    # If the top two are close (difference <= 1) and not zero
    if (first[1] - second[1]) <= 1 and second[1] > 0:
        return f"{first[0]}-{second[0]}"
        
    return first[0]

def get_advice(dosha):
    """
    Returns advice based on the dominant dosha imbalance.
    Includes Dual-Dosha types.
    """
    # Base advice for single doshas
    vata_advice = {
        "diet": "Warm, oily, heavy foods. Sweet, sour, and salty tastes.",
        "lifestyle": "Routine, warmth, oil massage (Abhyanga), gentle yoga.",
        "avoid": "Cold, dry, raw foods. Irregular schedules."
    }
    pitta_advice = {
        "diet": "Cool, slightly dry, heavy foods. Sweet, bitter, and astringent tastes.",
        "lifestyle": "Stay cool, avoid direct sun, non-competitive activities.",
        "avoid": "Hot, spicy, oily, sour, and salty foods. Excessive heat."
    }
    kapha_advice = {
        "diet": "Warm, light, dry foods. Pungent, bitter, and astringent tastes.",
        "lifestyle": "Vigorous exercise, variety, rising early, dry massage.",
        "avoid": "Heavy, oily, sweet, sour, and salty foods. Excessive sleep."
    }

    advice_db = {
        "Vata": vata_advice,
        "Pitta": pitta_advice,
        "Kapha": kapha_advice,
        # Dual types - combining recommendations
        "Vata-Pitta": {
             "diet": "Warm but not hot, nourishing foods. Sweet taste is best. Avoid very spicy or very dry foods.",
             "lifestyle": "Gentle exercise, meditation to calm the mind (Vata) and cool the emotions (Pitta).",
             "avoid": "Chili peppers, raw onions, fasting, running in hot sun."
        },
        "Pitta-Vata": { # Same as Vata-Pitta usually, but handling order
             "diet": "Warm but not hot, nourishing foods. Sweet taste is best. Avoid very spicy or very dry foods.",
             "lifestyle": "Gentle exercise, meditation to calm the mind (Vata) and cool the emotions (Pitta).",
             "avoid": "Chili peppers, raw onions, fasting, running in hot sun."
        },
        "Pitta-Kapha": {
             "diet": "Light, dry, and cool foods. Bitter and astringent tastes. Lots of leafy greens.",
             "lifestyle": "Active exercise but avoid overheating. Competitive sports are okay in moderation.",
             "avoid": "Oily, heavy, sour, and salty foods. Deep fried items."
        },
        "Kapha-Pitta": {
             "diet": "Light, dry, and cool foods. Bitter and astringent tastes. Lots of leafy greens.",
             "lifestyle": "Active exercise but avoid overheating. Competitive sports are okay in moderation.",
             "avoid": "Oily, heavy, sour, and salty foods. Deep fried items."
        },
        "Vata-Kapha": {
             "diet": "Warm, light, and dry foods. Pungent and astringent tastes. Ginger tea is excellent.",
             "lifestyle": "Stay active and warm. Avoid napping during the day. Variety in routine.",
             "avoid": "Cold, heavy, and oily foods. Ice cream, yogurt, cheese."
        },
        "Kapha-Vata": {
             "diet": "Warm, light, and dry foods. Pungent and astringent tastes. Ginger tea is excellent.",
             "lifestyle": "Stay active and warm. Avoid napping during the day. Variety in routine.",
             "avoid": "Cold, heavy, and oily foods. Ice cream, yogurt, cheese."
        },
        "Unknown": {
             "diet": "Could not determine specifics. Generally: eat fresh, seasonal foods.",
             "lifestyle": "Maintain balance.",
             "avoid": "Processed foods."
        },
        "None": {
             "diet": "Balanced.",
             "lifestyle": "Healthy.",
             "avoid": "Junk."
        }
    }
    return advice_db.get(dosha, advice_db.get("Unknown"))
