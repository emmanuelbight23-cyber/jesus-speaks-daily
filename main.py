import asyncio
import random
from datetime import datetime
from pathlib import Path
import os
import json
import urllib.request
import urllib.error
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip

CHANNEL_NAME = "Jesus Speaks Daily"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

MESSAGES = [
    {
        "title": "God Has Not Forgotten You",
        "verse": "Isaiah 49:15-16",
        "message": (
            "Sometimes life becomes difficult, and you wonder "
            "whether God remembers you. Do not lose hope. "
            "God sees your tears, understands your struggles, "
            "and knows your name. Even when the answer seems "
            "delayed, keep trusting Him. Your present situation "
            "does not determine your future. Pray today, remain "
            "faithful, and take the next step in faith."
        ),
        "prayer": (
            "Heavenly Father, strengthen my faith when I feel "
            "forgotten. Help me trust Your promises and walk "
            "in Your wisdom. In Jesus' name, Amen."
        ),
    },
    {
        "title": "God Will Give You Strength",
        "verse": "Isaiah 40:31",
        "message": (
            "You do not have to face every challenge in your "
            "own strength. When you feel tired, turn to God "
            "in prayer. Take each day one step at a time. "
            "Waiting on the Lord is not giving up. It is "
            "choosing to trust Him while continuing to do "
            "what is right. Let faith guide your decisions today."
        ),
        "prayer": (
            "Lord, renew my strength and teach me to depend "
            "on You. Give me courage, patience, and wisdom "
            "for today. In Jesus' name, Amen."
        ),
    },
    {
        "title": "Choose Faith Over Fear",
        "verse": "2 Timothy 1:7",
        "message": (
            "Fear can make tomorrow look impossible before "
            "today has even finished. Pause, breathe, and "
            "remember that you can bring your worries to God. "
            "Faith does not mean you will never feel afraid. "
            "It means you can seek God's help while moving "
            "forward with wisdom and courage. Take one positive "
            "step today instead of allowing fear to control you."
        ),
        "prayer": (
            "Father, replace my fear with courage, love, "
            "and a sound mind. Guide my steps and help me "
            "trust You. In Jesus' name, Amen."
        ),
    },
    {
        "title": "Trust God's Timing",
        "verse": "Ecclesiastes 3:11",
        "message": "Do not let waiting steal your peace. God can work through seasons you do not understand. Keep praying, preparing, and doing what is right. Your story is not over.",
        "prayer": "Father, help me trust Your timing. Give me patience and wisdom. In Jesus' name, Amen."
    },
    {
        "title": "You Are Never Alone",
        "verse": "Deuteronomy 31:8",
        "message": "Even when you feel alone, remember that God promises to go before His people. Take courage and face today with hope. You do not have to carry every burden alone.",
        "prayer": "Lord, remind me that You are with me. Give me courage and guide my steps. Amen."
    },
    {
        "title": "Peace in the Storm",
        "verse": "John 14:27",
        "message": "Trouble around you does not have to control your heart. Jesus offers a peace deeper than your circumstances. Pause, pray, and take the next wise step.",
        "prayer": "Jesus, calm my heart and teach me to rest in Your peace. Amen."
    },
    {
        "title": "God Gives Wisdom",
        "verse": "James 1:5",
        "message": "When you do not know what decision to make, ask God for wisdom. Pray, seek good counsel, and choose what is right. You do not need to have every answer today.",
        "prayer": "Father, give me wisdom for every decision. Guide my choices. In Jesus' name, Amen."
    },
    {
        "title": "Do Not Grow Weary",
        "verse": "Galatians 6:9",
        "message": "Do not give up on doing good because results are slow. Keep showing kindness, working honestly, and planting good seeds. Small faithful steps matter.",
        "prayer": "Lord, renew my strength and help me remain faithful. Amen."
    },
    {
        "title": "The Lord Is Your Shepherd",
        "verse": "Psalm 23:1",
        "message": "God cares for you and guides you. When the road ahead feels uncertain, trust Him to lead you. You are not forgotten, and you can seek His direction every day.",
        "prayer": "Good Shepherd, lead me in the right path and help me trust Your care. Amen."
    },
    {
        "title": "Be Strong and Courageous",
        "verse": "Joshua 1:9",
        "message": "Courage does not mean you never feel afraid. It means you keep moving toward what is right while trusting God. Face today's responsibilities one step at a time.",
        "prayer": "Lord, make me strong and courageous. Guide me through today's challenges. Amen."
    },
    {
        "title": "Your Hope Is in God",
        "verse": "Romans 15:13",
        "message": "Hope is more than wishing everything will be easy. Trust that God can sustain you through every season. Keep praying, loving, and believing.",
        "prayer": "God of hope, fill my heart with joy, peace, and faith. Amen."
    },
    {
        "title": "Let Your Light Shine",
        "verse": "Matthew 5:16",
        "message": "Your actions can point others toward goodness. A patient response, an honest choice, or a kind word can make a difference. Let your life reflect God's love.",
        "prayer": "Father, let my words and actions reflect Your goodness today. Amen."
    },
    {
        "title": "Cast Your Worries on God",
        "verse": "1 Peter 5:7",
        "message": "You do not have to carry every worry alone. Bring your anxieties to God in prayer. Focus on the next wise step and remember that He cares for you.",
        "prayer": "Father, I bring my worries to You. Help me trust You and act wisely. Amen."
    },
        {
        "title": "Mercy Is New Every Morning",
        "verse": "Lamentations 3:22-23",
        "message": "Yesterday does not have to define today. God's mercy is new every morning. Learn from your mistakes, begin again, and walk forward with faith.",
        "prayer": "Lord, thank You for fresh mercy. Help me live today with gratitude. Amen."
    },
    {
        "title": "Walk by Faith",
        "verse": "2 Corinthians 5:7",
        "message": "You may not see the whole road ahead, but you can trust God while taking responsible steps today. Do not let uncertainty stop you from moving forward.",
        "prayer": "Father, strengthen my faith and guide my steps. Amen."
    },
    {
        "title": "Love One Another",
        "verse": "John 13:34-35",
        "message": "Show love through patience, kindness, forgiveness, and honesty. Your actions can make someone's day brighter. Let Christ's love guide your behaviour.",
        "prayer": "Jesus, teach me to love others with patience and kindness. Amen."
    },
    {
        "title": "God Is Our Refuge",
        "verse": "Psalm 46:1",
        "message": "When life feels unstable, remember that God is your refuge and strength. Turn to Him in prayer and face each challenge one step at a time.",
        "prayer": "God, be my refuge and give me strength today. Amen."
    },
    {
        "title": "Commit Your Plans to God",
        "verse": "Proverbs 16:3",
        "message": "Bring your plans before God. Work diligently, make wise decisions, and remain willing to learn. Let honesty and faith guide your ambitions.",
        "prayer": "Father, direct my plans and bless the work of my hands. Amen."
    },
    {
        "title": "God Will Never Forsake You",
        "verse": "Hebrews 13:5",
        "message": "Whatever season you are facing, remember God's promise to remain with His people. Keep your heart encouraged and continue walking in faith.",
        "prayer": "Lord, help me remember Your presence and trust Your promises. Amen."
    },
    {
        "title": "Be Still and Know God",
        "verse": "Psalm 46:10",
        "message": "Sometimes the best thing you can do is pause, pray, and remember who God is. Do not let the noise around you steal your time with Him.",
        "prayer": "Father, quiet my heart and help me draw closer to You. Amen."
    },
    {
        "title": "A Heart of Gratitude",
        "verse": "1 Thessalonians 5:18",
        "message": "Even on difficult days, there are reasons to thank God. Gratitude helps you recognise His goodness in ordinary moments. Never stop giving thanks.",
        "prayer": "Lord, give me a grateful heart in every season. Amen."
    },
    {
        "title": "God Can Make a Way",
        "verse": "Isaiah 43:19",
        "message": "A closed door does not mean your journey is over. Stay prayerful, remain wise, and be open to new opportunities. God can bring hope into unexpected places.",
        "prayer": "Father, guide me into the opportunities You have prepared. Amen."
    },
    {
        "title": "Seek God First",
        "verse": "Matthew 6:33",
        "message": "Put God at the centre of your decisions, ambitions, and relationships. Let His wisdom shape your priorities as you work toward your goals.",
        "prayer": "Lord, help me seek Your kingdom first in everything I do. Amen."
    },
        {
        "title": "The Joy of the Lord",
        "verse": "Nehemiah 8:10",
        "message": "Your strength does not depend only on how easy life feels. Find joy in God's goodness and let His promises encourage you through difficult moments.",
        "prayer": "Lord, restore my joy and strengthen my heart. Amen."
    },
    {
        "title": "God Hears Your Prayers",
        "verse": "1 John 5:14",
        "message": "Never underestimate the value of sincere prayer. Bring your needs, fears, and hopes before God. Trust Him as you wait and continue doing what is right.",
        "prayer": "Father, thank You for hearing me. Help me trust Your wisdom. Amen."
    },
    {
        "title": "Forgive as Christ Forgave",
        "verse": "Ephesians 4:32",
        "message": "Forgiveness can be difficult, but bitterness can weigh heavily on your heart. Ask God to help you release resentment and respond with grace and wisdom.",
        "prayer": "Jesus, give me a forgiving heart and help me walk in love. Amen."
    },
    {
        "title": "You Are God's Workmanship",
        "verse": "Ephesians 2:10",
        "message": "Your life has purpose. Use your gifts to serve others, make a positive difference, and honour God through the work you do today.",
        "prayer": "Father, help me discover and fulfil the good purpose You have for my life. Amen."
    },
    {
        "title": "Wait on the Lord",
        "verse": "Isaiah 40:31",
        "message": "Waiting can be difficult, but do not allow impatience to make you lose hope. Keep trusting God, renewing your strength, and taking faithful steps.",
        "prayer": "Lord, renew my strength as I wait on You. Amen."
    },
    {
        "title": "Walk in God's Love",
        "verse": "1 John 4:19",
        "message": "God's love gives us a reason to love others. Let compassion guide your words, let kindness guide your actions, and let your life reflect Christ.",
        "prayer": "Father, help me share Your love wherever I go. Amen."
    },
    {
        "title": "The Lord Is Faithful",
        "verse": "2 Thessalonians 3:3",
        "message": "Circumstances may change, but God's faithfulness remains. Hold on to your faith, stand firm in His promises, and keep moving forward with hope.",
        "prayer": "Faithful God, strengthen my heart and keep me steadfast. Amen."
    },
]


def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = f"{line} {word}".strip()

        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines


def create_background(message, date_text):
    width, height = 720, 1280
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    # Create a peaceful blue-to-purple gradient.
    for y in range(height):
        ratio = y / height
        color = (
            int(15 + 35 * ratio),
            int(30 + 10 * ratio),
            int(75 + 65 * ratio),
        )

        for x in range(width):
            pixels[x, y] = color

    draw = ImageDraw.Draw(image)

    # Decorative golden circles.
    draw.ellipse((500, 100, 660, 260), outline=(210, 180, 110), width=3)
    draw.ellipse((530, 130, 630, 230), outline=(210, 180, 110), width=2)

    title_font = get_font(43, True)
    verse_font = get_font(29, True)
    body_font = get_font(25)
    small_font = get_font(21)

    margin = 48
    max_width = width - margin * 2
    y = 100

    draw.text(
        (margin, y),
        CHANNEL_NAME,
        font=get_font(31, True),
        fill=(245, 211, 145),
    )
    y += 90

    for line in wrap_text(
        draw, message["title"], title_font, max_width
    ):
        draw.text(
            (margin, y),
            line,
            font=title_font,
            fill=(255, 255, 255),
        )
        y += 58

    y += 20

    draw.rounded_rectangle(
        (margin, y, width - margin, y + 65),
        radius=15,
        fill=(45, 58, 105),
        outline=(210, 180, 110),
        width=2,
    )

    draw.text(
        (margin + 18, y + 15),
        message["verse"],
        font=verse_font,
        fill=(255, 221, 150),
    )

    y += 105

    draw.text(
        (margin, y),
        "TODAY'S ENCOURAGEMENT",
        font=get_font(23, True),
        fill=(245, 211, 145),
    )
    y += 48

    for line in wrap_text(
        draw, message["message"], body_font, max_width
    ):
        if y > 800:
            break

        draw.text(
            (margin, y),
            line,
            font=body_font,
            fill=(245, 245, 250),
        )
        y += 38

    y = max(y + 35, 900)

    draw.line(
        (margin, y, width - margin, y),
        fill=(210, 180, 110),
        width=2,
    )
    y += 25

    draw.text(
        (margin, y),
        "LET US PRAY",
        font=get_font(25, True),
        fill=(255, 221, 150),
    )
    y += 45

    for line in wrap_text(
        draw, message["prayer"], small_font, max_width
    ):
        if y > 1130:
            break

        draw.text(
            (margin, y),
            line,
            font=small_font,
            fill=(255, 255, 255),
        )
        y += 31

    draw.text(
        (margin, 1200),
        f"Jesus Speaks Daily | {date_text}",
        font=get_font(17),
        fill=(210, 210, 225),
    )

    return image


async def create_voiceover(text, audio_path):
    voice = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural",
        rate="+0%",
    )
    await voice.save(str(audio_path))

def post_video_to_youtube(video_path, title, description):
    api_key = os.getenv("POSTWIRE_API_KEY")

    if not api_key:
        print("POSTWIRE_API_KEY is missing. Skipping publishing.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        size_bytes = os.path.getsize(video_path)

        upload_request = urllib.request.Request(
            "https://postwire.io/api/media/upload-url",
            data=json.dumps({
                "content_type": "video/mp4",
                "size_bytes": size_bytes,
            }).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(upload_request, timeout=60) as response:
            upload_info = json.loads(response.read().decode("utf-8"))

        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()

        put_request = urllib.request.Request(
            upload_info["upload_url"],
            data=video_bytes,
            headers={"Content-Type": "video/mp4"},
            method="PUT",
        )

        with urllib.request.urlopen(put_request, timeout=120) as response:
            response.read()

        finalize_url = (
            "https://postwire.io/api/media/finalize?"
            + urllib.parse.urlencode({"path": upload_info["path"]})
        )

        finalize_request = urllib.request.Request(
            finalize_url,
            headers={"Authorization": f"Bearer {api_key}"},
            method="GET",
        )

        with urllib.request.urlopen(finalize_request, timeout=60) as response:
            media_info = json.loads(response.read().decode("utf-8"))

        post_data = {
            "platforms": ["youtube"],
            "video_url": media_info["media_url"],
            "text": description,
            "options": {
                "youtube": {
                    "title": title[:100],
                   "privacy": "public",
                }
            },
        }

        post_request = urllib.request.Request(
            "https://postwire.io/api/post",
            data=json.dumps(post_data).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(post_request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))

        print("POSTWIRE RESPONSE:", json.dumps(result))

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        print(f"POSTWIRE HTTP ERROR {error.code}: {details}")
        raise

    except Exception as error:
        print(f"POSTWIRE PUBLISHING ERROR: {error}")
        raise
    

def main():
    today = datetime.now().strftime("%Y-%m-%d")

    # Rotate messages daily.
day_number = datetime.strptime(today, "%Y-%m-%d").timetuple().tm_yday
message = MESSAGES[(day_number - 1) % len(MESSAGES)]
    narration = (
        f"Welcome to {CHANNEL_NAME}. "
        f"Today's message is: {message['title']}. "
        f"Today's Bible verse is {message['verse']}. "
        f"{message['message']} "
        f"Let us pray. {message['prayer']} "
        "May God bless you today. Amen."
    )

    audio_path = OUTPUT_DIR / "voiceover.mp3"
    image_path = OUTPUT_DIR / "background.png"
    video_path = OUTPUT_DIR / f"jesus_speaks_{today}.mp4"

    print("Creating today's Christian message...")

    background = create_background(message, today)
    background.save(image_path)

    print("Generating English voiceover...")
    asyncio.run(create_voiceover(narration, audio_path))

    print("Combining background and narration into video...")

    audio = AudioFileClip(str(audio_path))
    video = ImageClip(str(image_path)).set_duration(audio.duration)
    video = video.set_audio(audio)

    video.write_videofile(
        str(video_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        logger="bar",
    )

    video.close()
    audio.close()

    print(f"VIDEO CREATED SUCCESSFULLY: {video_path}")
    post_video_to_youtube(
        video_path,
        f"{message['title']} | {message['verse']}",
        (
            f"{message['message']}\n\n"
            f"Verse: {message['verse']}\n\n"
            f"Prayer: {message['prayer']}\n\n"
            "Subscribe to Jesus Speaks Daily for daily encouragement."
        ),
    )

if __name__ == "__main__":
    main()
