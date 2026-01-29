import matplotlib
# Set backend to Agg (Anti-Grain Geometry) for non-interactive server/serverless environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def generate_dashboard(user_data):
    """
    Generates a dashboard image from user data.
    Returns: BytesIO object containing the PNG image.
    """
    expenses = user_data.get('expenses', [])
    habits = user_data.get('habits', [])
    moods = user_data.get('moods', [])

    # Create a figure with subplots
    fig = plt.figure(figsize=(10, 8))
    
    # 1. Expenses (Pie Chart)
    ax1 = plt.subplot(2, 2, 1)
    if expenses:
        totals = {}
        for e in expenses:
            desc = e['desc']
            amt = e['amount']
            totals[desc] = totals.get(desc, 0) + amt
        
        ax1.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%', startangle=90)
        ax1.set_title('Expense Breakdown')
    else:
        ax1.text(0.5, 0.5, 'No Expense Data', ha='center')
        ax1.axis('off')

    # 2. Habits (Simple Count Bar Chart)
    ax2 = plt.subplot(2, 2, 2)
    if habits:
        habit_counts = {}
        for h in habits:
            desc = h['desc']
            habit_counts[desc] = habit_counts.get(desc, 0) + 1
        
        ax2.bar(habit_counts.keys(), habit_counts.values(), color='skyblue')
        ax2.set_title('Habit Streaks')
    else:
        ax2.text(0.5, 0.5, 'No Habit Data', ha='center')
        ax2.axis('off')
        
    # 3. Mood (Text Summary for now, or simple line if values are numeric)
    ax3 = plt.subplot(2, 1, 2) # Bottom row, full width
    if moods:
         # Extract numeric values if possible, else just show recent moods
        mood_texts = [m['mood'] for m in moods]
        ax3.axis('off')
        ax3.text(0.5, 0.5, f"Recent Moods:\n{', '.join(mood_texts[-5:])}", ha='center', fontsize=12)
        ax3.set_title('Mood Log')
    else:
        ax3.text(0.5, 0.5, 'No Mood Data', ha='center')
        ax3.axis('off')

    plt.tight_layout()
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf
