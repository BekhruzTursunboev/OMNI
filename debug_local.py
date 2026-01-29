from bot_logic.analyzer import Analyzer
from bot_logic.database import db
import sys

def run_test():
    analyzer = Analyzer()
    user_id = 12345

    print("--- 1. Testing NLP Analyzer ---")
    inputs = [
        "Spent $15 on Lunch",
        "Spent 50 on Groceries",
        "Drank water",
        "Ran 5km",
        "Feeling happy",
        "Day was productive"
    ]

    for text in inputs:
        res = analyzer.analyze(text)
        print(f"Input: '{text}' -> Result: {res}")
        if res:
            if res['type'] == 'expense':
                db.add_expense(user_id, res['amount'], res['description'])
            elif res['type'] == 'habit':
                db.add_habit(user_id, res['description'])
            elif res['type'] == 'mood':
                db.add_mood(user_id, res.get('value', 'unknown'))

    print("\n--- 2. Testing Database ---")
    data = db.get_user_data(user_id)
    print(f"User Data: {data}")

    print("\n--- 3. Testing Visualizer ---")
    try:
        from bot_logic.visualizer import generate_dashboard
        buf = generate_dashboard(data)
        with open("d:/bot/test_dashboard.png", "wb") as f:
            f.write(buf.getvalue())
        print("Success! Dashboard saved to 'd:/bot/test_dashboard.png'. Check this file!")
    except ImportError:
        print("WARNING: 'matplotlib' not found. Skipping visualization test.")
    except Exception as e:
        print(f"Error generating dashboard: {e}")

if __name__ == "__main__":
    run_test()
