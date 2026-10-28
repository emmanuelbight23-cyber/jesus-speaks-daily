 from datetime import datetime
from pathlib import Path
import random

CHANNEL_NAME = "Jesus Speaks Daily"

MESSAGES = [
    {
        "title": "God Has Not Forgotten You",
        "verse": "Isaiah 49:15-16",
        "message": (
            "Sometimes life becomes difficult, and you may wonder "
            "whether God remembers you. Do not lose hope. God sees "
            "your tears, understands your struggles, and knows your "
            "name. Even when the answer seems delayed, keep trusting "
            "Him. Your present situation does not determine your future. "
            "Pray today, remain faithful, and take the next step in faith."
        ),
        "prayer": (
            "Heavenly Father, strengthen my faith when I feel forgotten. "
            "Help me trust Your promises and walk in Your wisdom. Amen."
        ),
    },
    {
        "title": "God Will Give You Strength",
        "verse": "Isaiah 40:31",
        "message": (
            "You do not have to face every challenge in your own strength. "
            "When you feel tired, turn to God in prayer. Take each day "
            "one step at a time. Remember that waiting on the Lord is "
            "not giving up. It is choosing to trust Him while you continue "
            "doing what is right. Let faith guide your decisions today."
        ),
        "prayer": (
            "Lord, renew my strength and teach me to depend on You. "
            "Give me courage, patience, and wisdom for today. Amen."
        ),
    },
    {
        "title": "Choose Faith Over Fear",
        "verse": "2 Timothy 1:7",
        "message": (
            "Fear can make tomorrow look impossible before today has "
            "even finished. Pause, breathe, and remember that you can "
            "bring your worries to God. Faith does not mean you will "
            "never feel afraid. It means you can seek God's help while "
            "moving forward with wisdom and courage. Take one positive "
            "step today instead of allowing fear to control your choices."
        ),
        "prayer": (
            "Father, replace my fear with courage, love, and a sound mind. "
            "Guide my steps and help me trust You. Amen."
        ),
    },
]


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    message = random.choice(MESSAGES)

    script = f"""
{CHANNEL_NAME}
Date: {today}

TITLE: {message['title']}

BIBLE VERSE: {message['verse']}

WELCOME:
Welcome to Jesus Speaks Daily. Take a moment to receive today's
message of faith, hope, and encouragement.

DAILY MESSAGE:
{message['message']}

PRAYER:
{message['prayer']}

CLOSING:
If this message encouraged you, share it with someone who needs hope.
Subscribe to Jesus Speaks Daily for more Bible-based encouragement.

May God bless you and keep you today.
"""

    output = Path("output")
    output.mkdir(exist_ok=True)

    filename = output / f"daily_message_{today}.txt"
    filename.write_text(script.strip() + "\n", encoding="utf-8")

    print("=" * 40)
    print(CHANNEL_NAME)
    print("Daily Christian script generated!")
    print(f"Date: {today}")
    print(f"Title: {message['title']}")
    print(f"Bible verse: {message['verse']}")
    print(f"Saved to: {filename}")
    print("=" * 40)


if __name__ == "__main__":
    main()
