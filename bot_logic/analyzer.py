import re
from datetime import datetime

class Analyzer:
    def __init__(self):
        self.patterns = {
            'expense': [
                r"spent \$?(\d+) on (.+)",
                r"bought (.+) for \$?(\d+)",
                r"cost \$?(\d+) for (.+)",
                r"paid \$?(\d+) for (.+)"
            ],
            'habit': [
                r"drank water",
                r"worked out",
                r"read (.+)",
                r"meditated",
                r"ran (\d+)km"
            ],
            'mood': [
                r"feeling (.+)",
                r"i am (.+)",
                r"mood is (\d+)/10",
                r"day was (.+)"
            ]
        }

    def analyze(self, text):
        text = text.lower().strip()
        
        # Check Expenses
        for p in self.patterns['expense']:
            match = re.search(p, text)
            if match:
                # Handle varying group positions (money first or money second)
                groups = match.groups()
                amount, item = None, None
                
                # Simple logic: digit is amount, string is item
                for g in groups:
                    if g.isdigit():
                        amount = int(g)
                    else:
                        item = g
                        
                if amount and item:
                    return {
                        "type": "expense",
                        "amount": amount,
                        "description": item,
                        "timestamp": datetime.now().isoformat()
                    }

        # Check Habits
        for p in self.patterns['habit']:
            if re.search(p, text):
                return {
                    "type": "habit",
                    "description": text,
                    "timestamp": datetime.now().isoformat()
                }

        # Check Mood
        for p in self.patterns['mood']:
            match = re.search(p, text)
            if match:
                return {
                    "type": "mood",
                    "value": match.group(1),
                    "timestamp": datetime.now().isoformat()
                }

        return None
