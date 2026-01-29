# NOTE: In a serverless environment (Vercel), this in-memory database will RESET 
# frequently. For persistent storage, you should use an external database 
# like MongoDB Atlas, Vercel KV, or Supabase.
# This implementation is for DEMONSTRATION purposes to satisfy the "Easy/Free" constraint immediately.

class SimpleDB:
    def __init__(self):
        # Dictionary structure: {user_id: {'expenses': [], 'habits': [], 'moods': []}}
        self._db = {}

    def get_user_data(self, user_id):
        if user_id not in self._db:
            self._db[user_id] = {'expenses': [], 'habits': [], 'moods': []}
        return self._db[user_id]

    def add_expense(self, user_id, amount, desc):
        data = self.get_user_data(user_id)
        data['expenses'].append({'amount': amount, 'desc': desc})

    def add_habit(self, user_id, desc):
        data = self.get_user_data(user_id)
        data['habits'].append({'desc': desc})

    def add_mood(self, user_id, mood):
        data = self.get_user_data(user_id)
        data['moods'].append({'mood': mood})

    def get_stats(self, user_id):
        return self.get_user_data(user_id)

# Singleton instance
db = SimpleDB()
