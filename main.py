import asyncio
import random
from datetime import datetime
from pathlib import Path
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


def main():
    today = datetime.now().strftime("%Y-%m-%d")

    # Use the date to keep the same message for the same day.
    random.seed(today)
    message = random.choice(MESSAGES)

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


if __name__ == "__main__":
    main()
