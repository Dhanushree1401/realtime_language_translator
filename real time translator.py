from tkinter import *
from tkinter import ttk
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import os
import threading

# Initialize window
root = Tk()
root.geometry('1100x600')
root.resizable(0, 0)
root.title('Real-time Translator with Voice Input and Idiom Conversion')
root['bg'] = '#1c1c1c'

# Translator & language setup
language = list(LANGUAGES.keys())
lang_code_dict = LANGUAGES

# Title
Label(root, text="🌍 Language Translator 🌍", font="Arial 22 bold", bg='#1c1c1c', fg='white').grid(row=0, column=0, columnspan=3, pady=10)

# Input Text
Label(root, text="Enter Text", font='arial 13 bold', bg='white smoke').grid(row=1, column=0, padx=10)
Input_text = Text(root, height=3, width=50, wrap=WORD)
Input_text.grid(row=1, column=1, padx=10)

# Output Text
Label(root, text="Output", font='arial 13 bold', bg='white smoke').grid(row=3, column=0, padx=10)
Output_text = Text(root, font='arial 10', height=5, wrap=WORD, padx=5, pady=5, width=50)
Output_text.grid(row=3, column=1, padx=10)

# Input Language ComboBox
input_lang = ttk.Combobox(root, values=language, width=22)
input_lang.set("english")
input_lang.grid(row=1, column=2, padx=10)

# Destination Language ComboBox
dest_lang = ttk.Combobox(root, values=language, width=22)
dest_lang.set('Translation Language')
dest_lang.grid(row=2, column=0, padx=(20, 5), pady=5, ipady=4)

# Idioms dictionary
idioms_dict = {
     "break the ice": "start a conversation",
    "piece of cake": "something very easy",
    "once in a blue moon": "very rarely",
    "barking up the wrong tree": "to pursue the wrong course of action",
    "hit the nail on the head": "to describe exactly what is causing a situation or problem",
    "spill the beans": "reveal a secret",
    "cost an arm and a leg": "very expensive",
    "under the weather": "feeling ill", 
    "let the cat out of the bag": "reveal a secret unintentionally",
    "burn the midnight oil": "work late into the night",
    "kick the bucket": "to die",
    "bite the bullet": "to endure a painful situation",
    "the ball is in your court": "it's your decision or responsibility now",
    "pull someone's leg": "to tease or joke with someone",
    "cold feet": "to feel nervous or hesitant about something",
    "jump on the bandwagon": "to join others in doing something popular",
    "on the fence": "undecided or unsure about something",
    "the best of both worlds": "an ideal situation that combines two different things",
    "hit the books": "to study hard",
    "a blessing in disguise": "something that seems bad at first but results in something good",
    "cut corners": "to do something in the easiest or cheapest way",
    "get out of hand": "to become uncontrollable",
    "it's not rocket science": "it's not very complicated",
    "the early bird catches the worm": "those who start early have an advantage",
    "when pigs fly": "something that will never happen",
    "to have a chip on your shoulder": "to hold a grudge or be angry about something",
    "to steal someone's thunder": "to take credit for someone else's achievements",
    "you can't judge a book by its cover": "you shouldn't judge someone or something based only on appearance",
    "the elephant in the room": "an obvious problem that people avoid discussing",
    "keep your chin up": "stay positive in a difficult situation",
    "break a leg": "good luck, especially before a performance",
    "let sleeping dogs lie": "to avoid bringing up old problems",
    "hit the ground running": "to start something and proceed at a fast pace",
    "the straw that broke the camel's back": "a minor action that causes a major reaction",
    "costs a pretty penny": "to be very expensive",
    "bite off more than you can chew": "to take on a task that is way too big",
    "cut the mustard": "to perform satisfactorily or meet expectations",
    "to be in hot water": "to be in trouble or facing consequences",
    "the tip of the iceberg": "the small part of a much larger problem",
    "to throw in the towel": "to give up or admit defeat",
    "to go out on a limb": "to take a risk",
    "to take with a grain of salt": "to view something with skepticism",
    "to make a mountain out of a molehill": "to exaggerate a minor issue",
    "to add fuel to the fire": "to make a situation worse",
    "to get a second wind": "to regain energy after fatigue",
    "to hit the sack": "to go to bed",
    "to pull the wool over someone's eyes": "to deceive someone",
    "to take the bull by the horns": "to confront a difficult situation directly",
    "to throw caution to the wind": "to take a risk without worrying about the consequences",
    "to bite the hand that feeds you": "to harm someone who has helped you",
    "to have a heart of gold": "to be very kind and generous",
    "to go the extra mile": "to make a special effort to achieve something",
    "to put all your eggs in one basket": "to risk everything on a single venture",
    "to get your act together": "to organize oneself or one's life effectively",
    "to put your money where your mouth is": "to take action to support what you say",
    "to be on the same page": "to have a shared understanding or agreement",
    "to have your head in the clouds": "to be out of touch with reality",
    "to rain on someone's parade": "to spoil someone's plans or enthusiasm",
    "to go back to the drawing board": "to start over with a new plan after a failure",
    "to bite the bullet": "to face a difficult situation with courage",
    "to jump the gun": "to act before the proper time",
    "to face the music": "to confront the consequences of one's actions",
    "to put the cart before the horse": "to do things in the wrong order",
    "to throw in the towel": "to give up on something",
    "to beat around the bush": "to avoid getting to the point",
    "to kill two birds with one stone": "to accomplish two tasks with a single effort",
    "to throw in the towel": "to give up or admit defeat",
    "to have a sweet tooth": "to love sweet foods",
    "to make ends meet": "to have enough money to cover expenses",
    "to let the cat out of the bag": "to reveal a secret accidentally",
    "to hit the nail on the head": "to describe exactly what is causing a situation or problem",
    "to know the ropes": "to understand the details of a situation",
    "to hold your horses": "to wait or be patient",
    "to have bigger fish to fry": "to have more important things to deal with",
    "to keep your fingers crossed": "to hope for a good outcome",
    "to burn the candle at both ends": "to work excessively hard",
    "to put a sock in it": "to tell someone to be quiet",
    "to have a skeleton in the closet": "to have a secret that could damage one's reputation",
    "to take a rain check": "to postpone a plan for later",
    "to turn a blind eye": "to ignore something that you know is wrong",
    "to shoot the breeze": "to engage in casual or idle conversation",
    "to hit the ground running": "to start an activity with enthusiasm and energy",
    "to play it by ear": "to improvise as one goes along",
    "to give someone the cold shoulder": "to ignore someone intentionally",
    "to look a gift horse in the mouth": "to criticize something that has been received as a gift",
    "to miss the boat": "to miss an opportunity",
    "to pull yourself together": "to regain control of your emotions",
    "to run out of steam": "to lose energy or motivation",
    "to see eye to eye": "to agree with someone",
    "to stand the test of time": "to be enduring or long-lasting",
    "to take the cake": "to be the best or worst of a particular type",
    "to throw someone under the bus": "to betray someone for personal gain",
    "to wear your heart on your sleeve": "to openly show your emotions",
    "to work like a dog": "to work very hard",
    "to write something off": "to dismiss something as unimportant",
    "to go down in flames": "to fail spectacularly",
    "to get the ball rolling": "to start an activity or process",
    "to hit the jackpot": "to have great success or good fortune",
    "to go out of your way": "to make a special effort to do something",
    "to keep an eye on": "to watch or monitor something closely",
    "to take it with a grain of salt": "to not take something too seriously",
    "to be on thin ice": "to be in a precarious or risky situation",
    "to bite the dust": "to die or fail",
    "to get the show on the road": "to start an activity or process",
    "to break the bank": "to be very expensive",
    "to call it a day": "to stop working for the day",
    "to drive someone up the wall": "to annoy or irritate someone",
    "to fall on deaf ears": "to be ignored or not heard",
    "to gather dust": "to be left unused or neglected",
    "to hang in the balance": "to be in a situation of uncertainty",
    "to jump through hoops": "to go through a lot of effort to achieve something",
    "to keep your options open": "to remain flexible and not commit to one option",
    "to lose your touch": "to lose the ability to do something well"
}

def replace_idioms(text):
    for idiom, meaning in idioms_dict.items():
        text = text.replace(idiom, meaning)
    return text

# Info Message Label and Box
bg_color = "#f0f0f0"
info_label = Label(root, text="Info", font='arial 14 bold', bg=bg_color)
info_label.grid(row=9, columnspan=4, padx=10, pady=(10, 0))
message_display = Text(root, font='arial 10', height=5, wrap=WORD, padx=5, pady=5, width=100, bg=bg_color)
message_display.grid(row=10, columnspan=4, padx=10, pady=(10, 20))

def update_message(message):
    message_display.delete(1.0, END)
    message_display.insert(END, message)

def Translate():
    try:
        selected_lang = dest_lang.get()
        dest_lang_code = lang_code_dict.get(selected_lang.lower())
        if not dest_lang_code:
            update_message("Translation error: Invalid destination language selected")
            return

        input_text = Input_text.get("1.0", END)
        input_text_with_meaning = replace_idioms(input_text)
        translated_text = GoogleTranslator(source='auto', target=dest_lang_code).translate(input_text_with_meaning)
        Output_text.delete(1.0, END)
        Output_text.insert(END, translated_text)
        update_message("Translation successful!")
        Speak(translated_text)
    except Exception as e:
        update_message(f"Translation error: {e}")

def Listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_message("Listening...")
        try:
            selected_input_lang = input_lang.get()
            input_lang_code = lang_code_dict.get(selected_input_lang.lower())
            if not input_lang_code:
                update_message("Speech error: Invalid input language selected")
                return
            audio_data = recognizer.listen(source)
            update_message("Recognizing...")
            text = recognizer.recognize_google(audio_data, language=input_lang_code)
            update_message(f"Recognized Text: {text}")
            Input_text.delete("1.0", END)
            Input_text.insert(END, text + "\n")
        except sr.UnknownValueError:
            update_message("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            update_message(f"Could not request results; {e}")

def Speak(text):
    try:
        target_lang_code = lang_code_dict.get(dest_lang.get().lower(), 'en')
        tts = gTTS(text=text, lang=target_lang_code)
        tts.save("output.mp3")
        os.system("start output.mp3")  # Use "afplay" for Mac or "xdg-open" for Linux
    except Exception as e:
        update_message(f"Speech error: {e}")

# Buttons
listen_btn = Button(root, text='🎤 Speak', font='arial 12 bold', pady=5, command=lambda: threading.Thread(target=Listen).start(), bg='lightblue', activebackground='green')
listen_btn.grid(row=1, column=3, padx=10)

trans_btn = Button(root, text='🈯 Translate', font='arial 12 bold', pady=5, command=lambda: threading.Thread(target=Translate).start(), bg='orange', activebackground='green')
trans_btn.grid(row=2, column=1, pady=10)

root.mainloop()
