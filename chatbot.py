import difflib
import os
import re
import sys
import time
from datetime import datetime

BOT_NAME = "AI Chatbot"
AUTHOR_NAME = "Arooj Fatima"
TYPING_DELAY = 0.012  
BANNER_WIDTH = 60

EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "good bye", "see you", "close"}
UTILITY_COMMANDS = {"help", "clear"}


RESPONSES = {

    "hello": "Hello! How are you doing today?",
    "hi": "Hi there! Nice to meet you.",
    "hey": "Hey! How can I help you?",
    "hii": "Hello! How are you doing today?",
    "helloo": "Hello! How are you doing today?",
    "yo": "Hey! How can I help you?",
    "hola": "Hola! How can I help you today?",
    "good morning": "Good morning! Have a great day ahead.",
    "good afternoon": "Good afternoon! Hope your day is going well.",
    "good evening": "Good evening! How has your day been?",
    "good night": "Good night! Sweet dreams.",
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "how are you doing": "I'm doing great, thanks for asking! How about you?",
    "whats up": "Not much, just here ready to chat with you!",
    "what's up": "Not much, just here ready to chat with you!",
    "im fine": "Glad to hear that!",
    "i am fine": "Glad to hear that!",
    "im good": "That's great to hear!",
    "im not good": "I'm sorry to hear that. I hope things get better soon.",
    "im sad": "I'm sorry you're feeling that way. Take care of yourself.",

    "your name": f"My name is {BOT_NAME}.",
    "what is your name": f"My name is {BOT_NAME}.",
    "who are you": f"I'm {BOT_NAME}, a rule-based chatbot.",
    "who made you": f"I was created by {AUTHOR_NAME}.",
    "who created you": f"I was created by {AUTHOR_NAME}.",
    "who built you": f"I was created by {AUTHOR_NAME}.",

    "what is ai": "AI stands for Artificial Intelligence -- the simulation of "
                  "human intelligence by machines, especially computer systems.",
    "what is artificial intelligence": "AI stands for Artificial Intelligence -- "
                  "the simulation of human intelligence by machines, especially "
                  "computer systems.",
    "what can you do": "I can chat with greetings, answer questions about myself "
                  "and AI, tell you the date and time, and more. Type 'help' to "
                  "see everything I understand.",

    "thanks": "You're welcome!",
    "thank you": "My pleasure!",
    "thanks a lot": "Happy to help, anytime!",
}

KEYWORD_RESPONSES = {
    "artificial intelligence": "AI stands for Artificial Intelligence -- "
                  "machines simulating human intelligence.",
    "your name": f"My name is {BOT_NAME}.",
    "who made you": f"I was created by {AUTHOR_NAME}.",
    "weather": "I can't check live weather -- I'm a rule-based chatbot with no "
               "internet access.",
    "joke": "I'm rule-based, so I don't know jokes yet -- but I'm happy to chat!",
    "name": f"My name is {BOT_NAME}.",
    "thank": "You're welcome!",
    "ai": "AI stands for Artificial Intelligence.",
}


def _handle_date() -> str:
    """Return today's date."""
    return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}."


def _handle_time() -> str:
    """Return the current time."""
    return f"The current time is {datetime.now().strftime('%I:%M %p')}."


def _handle_day() -> str:
    """Return the current day of the week."""
    return f"Today is {datetime.now().strftime('%A')}."

DYNAMIC_COMMANDS = {
    "date": _handle_date,
    "today's date": _handle_date,
    "what is the date": _handle_date,
    "time": _handle_time,
    "what is the time": _handle_time,
    "day": _handle_day,
    "what day is it": _handle_day,
}


def sanitize_input(raw_text: str) -> str:
    """Normalize raw user input for reliable dictionary matching.

    Steps: trim outer whitespace, lowercase, collapse repeated internal
    whitespace, and strip a single trailing punctuation mark.
    """
    cleaned = raw_text.strip().lower()
    cleaned = " ".join(cleaned.split())
    cleaned = cleaned.rstrip("?!.,")
    return cleaned


def find_keyword_response(user_input: str) -> str | None:
    """Search KEYWORD_RESPONSES for the longest matching whole-word phrase."""
    for keyword in sorted(KEYWORD_RESPONSES, key=len, reverse=True):
        if re.search(rf"\b{re.escape(keyword)}\b", user_input):
            return KEYWORD_RESPONSES[keyword]
    return None

def suggest_closest_phrase(user_input: str) -> str | None:
    """Suggest the closest known phrase for an unrecognized input."""
    known_phrases = set(RESPONSES) | set(DYNAMIC_COMMANDS) | UTILITY_COMMANDS | EXIT_COMMANDS
    matches = difflib.get_close_matches(user_input, known_phrases, n=1, cutoff=0.6)
    return matches[0] if matches else None


def generate_response(user_input: str) -> str:
    """Route sanitized input through the rule-based decision pipeline."""
    exact_response = RESPONSES.get(user_input)
    if exact_response is not None:
        return exact_response

    handler = DYNAMIC_COMMANDS.get(user_input)
    if handler is not None:
        return handler()
    keyword_response = find_keyword_response(user_input)
    if keyword_response is not None:
        return keyword_response
    suggestion = suggest_closest_phrase(user_input)
    if suggestion:
        return (f"Sorry, I didn't quite catch that. Did you mean '{suggestion}'? "
                f"Type 'help' to see what I can do.")
    return "Sorry! I don't understand that. Type 'help' to see what I can do."

def bot_say(message: str) -> None:
    """Print a bot response with a light character-by-character effect."""
    sys.stdout.write("Bot: ")
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        if TYPING_DELAY:
            time.sleep(TYPING_DELAY)
    print()


def print_banner() -> None:
    """Display the chatbot's startup banner."""
    print("=" * BANNER_WIDTH)
    print(f"Welcome to {BOT_NAME}".center(BANNER_WIDTH))
    print("A Rule-Based Conversational Agent | DecodeLabs".center(BANNER_WIDTH))
    print("=" * BANNER_WIDTH)
    print("Type 'help' to see what I can do, or 'bye' to exit.")
    print("=" * BANNER_WIDTH)


def print_help() -> None:
    """Display the list of supported commands and topics."""
    print(
        "\n"
        "Here's what I can help you with:\n\n"
        "  GREETINGS      hello, hi, hey, good morning/afternoon/evening/night\n"
        "  SMALL TALK     how are you, what's up, im fine, im sad\n"
        "  ABOUT ME       your name, who made you, what can you do\n"
        "  ABOUT AI       what is ai\n"
        "  DATE & TIME    date, time, day\n"
        "  COMMANDS       help, clear, bye / exit / quit\n\n"
        "Just type naturally -- I'll do my best to understand you!\n"
    )


def clear_screen() -> None:
    """Clear the console and redraw the banner."""
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()

def main() -> None:
    """Run the chatbot's continuous input-process-output loop."""
    print_banner()

    while True:
        try:
            raw_text = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print()
            bot_say("Goodbye! Have a nice day.")
            break

        user_input = sanitize_input(raw_text)

        if not user_input:
            bot_say("Please type something so I can help you.")
            continue

        if user_input in EXIT_COMMANDS:
            bot_say("Goodbye! Have a nice day.")
            break

        if user_input == "help":
            print_help()
            continue

        if user_input == "clear":
            clear_screen()
            continue

        bot_say(generate_response(user_input))


if __name__ == "__main__":
    main()