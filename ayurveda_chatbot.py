from ayurveda_bot import calculate_dosha, get_imbalance, get_advice, extract_symptoms, get_advanced_questions, calculate_advanced_dosha

def show_intro():
    print("\n🪷 Namaste 🙏")
    print("I Dhara — your personal Ayurveda wellness assistant.")
    print("I help balance your body & mind using ancient wisdom.\n")

    print("💬 How can I help you today?\n")

    print("Quick options:")
    print("1️⃣ Check my dosha imbalance (Advanced Quiz)")
    print("2️⃣ I feel stressed or anxious")
    print("3️⃣ Suggest diet for today")
    print("4️⃣ Improve sleep naturally")
    print("5️⃣ Boost energy & immunity")
    print("6️⃣ Seasonal health tips")
    print("7️⃣ Ask your own question\n")


def handle_quick_option(choice):
    if choice == "1":
        return "START_QUIZ"
    elif choice == "2":
        return "Stress may indicate Vata imbalance. Try warm tea, deep breathing & early sleep."
    elif choice == "3":
        return "Eat warm, freshly cooked meals. Avoid processed & cold foods."
    elif choice == "4":
        return "Sleep tip: Oil massage feet, avoid screens before bed, drink warm milk."
    elif choice == "5":
        return "Boost energy with ginger tea, morning sunlight & light exercise."
    elif choice == "6":
        return "Seasonal tip: Eat according to weather. Prefer cooling foods in summer & warm foods in winter."
    else:
        return None



def print_dosha_bar_chart(scores):
    """
    Prints a simple ASCII bar chart for the dosha scores.
    """
    total = sum(scores.values())
    if total == 0:
        return

    print("\n📊 Dosha Balance Chart:")
    max_label_length = 5
    bar_length = 20
    
    for dosha, score in scores.items():
        percent = (score / total) * 100
        # Calculate bar width
        filled_length = int(bar_length * score // total)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"{dosha:<{max_label_length}} : {bar} {int(percent)}%")

def run_dosha_quiz():
    print("\n📝 Starting Advanced Dosha Assessment...")
    print("Please answer the following questions to help us understand your balance.")
    print("(Type 'exit' at any time to cancel)\n")
    
    questions = get_advanced_questions()
    user_answers = []
    
    for i, q_data in enumerate(questions):
        print(f"\nQ{i+1}: {q_data['question']}")
        for j, (option_text, _) in enumerate(q_data['options']):
            print(f"  {j+1}. {option_text}")
            
        while True:
            user_input = input("   Select an option (number): ").strip().lower()
            
            if user_input in ["exit", "quit", "cancel"]:
                 print("   ❌ Quiz cancelled.")
                 return

            try:
                choice = int(user_input)
                if 1 <= choice <= len(q_data['options']):
                    user_answers.append((i, choice - 1))
                    break
                else:
                    print("   Invalid choice. Please select a valid number.")
            except ValueError:
                print("   Please enter a number or 'exit'.")

    scores = calculate_advanced_dosha(user_answers)
    imbalance = get_imbalance(scores)
    advice = get_advice(imbalance)

    print_dosha_bar_chart(scores)
    
    print(f"\n⚠ Detected Imbalance: {imbalance}")
    print("\n✅ Recommended Diet:", advice["diet"])
    print("✅ Lifestyle:", advice["lifestyle"])
    print("❌ Avoid:", advice["avoid"])


def chatbot():
    show_intro()

    while True:
        try:
            user_input = input("\nYou: ")
        except KeyboardInterrupt:
            print("\n🤖 Stay healthy & balanced. Namaste 🙏")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "bye", "quit"]:
            print("\n🤖 Stay healthy & balanced. Namaste 🙏")
            break

        # Quick options
        quick_reply = handle_quick_option(user_input)
        
        if quick_reply == "START_QUIZ":
            run_dosha_quiz()
            continue
            
        if quick_reply:
            print("\n🤖", quick_reply)
            continue


        # Natural symptom detection
        symptoms = extract_symptoms(user_input)

        if symptoms:
            scores = calculate_dosha(symptoms)
            imbalance = get_imbalance(scores)
            advice = get_advice(imbalance)

            print("\n🧠 Dosha Analysis:", scores)
            print(f"\n⚠ Detected Imbalance: {imbalance}")
            print("\n✅ Recommended Diet:", advice["diet"])
            print("✅ Lifestyle:", advice["lifestyle"])
            print("❌ Avoid:", advice["avoid"])

        else:
            print("\n🤖 I understand. Ayurveda focuses on balance.")
            print("Could you describe your symptoms or choose an option?")


if __name__ == "__main__":
    chatbot()
