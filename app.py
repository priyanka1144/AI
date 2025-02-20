from flask import Flask, request, render_template_string, session, redirect, url_for
import random
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Mock database for user profiles
user_profiles = {}

# Mock data for weather (simulating an API response)
mock_weather_data = {
    "Dhaka": {"temperature": "30°C", "condition": "Sunny"},
    "Chittagong": {"temperature": "28°C", "condition": "Partly Cloudy"},
    "Sylhet": {"temperature": "25°C", "condition": "Rainy"},
    "Khulna": {"temperature": "32°C", "condition": "Hot and Humid"},
    "Rajshahi": {"temperature": "31°C", "condition": "Sunny"}
}

# List of Bangladeshi jokes
jokes = [
    "কেন বাংলাদেশি মানুষ সবসময় খুশি? কারণ তারা সবসময় রিক্সা চালায়!",
    "বাংলাদেশের পাখি উড়তে গিয়ে থাকে কেন? কারণ আকাশটা বাংলাদেশি!",
    "কেন বাংলাদেশি ছেলেরা পড়াশোনা করে? কারণ তারা ভালো চাকরির স্বপ্ন দেখে!"
]

# List of motivational quotes in Bangla
quotes = [
    "আজ না হলে কাল, কাল না হলে পরশু – সফলতা অবশ্যই আসবে।",
    "চেষ্টা করতে থাকো, একদিন সফলতা তোমার হাতে চলে আসবে।",
    "বাংলাদেশি জাতির মত৯ শক্তিশালী হও, কারণ তোমার দেশ তোমার গর্ব।"
]

# HTML Template for the Chatbot Interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 300px;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
        }
        p {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>Chatbot</h1>
    {% if not session.get('logged_in') %}
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register here</a>.</p>
    {% else %}
    <p>Welcome, {{ session['username'] }}!</p>
    <form method="POST">
        <input type="text" name="user_input" placeholder="Type your message..." required>
        <button type="submit">Send</button>
    </form>
    <p><strong>Chatbot:</strong> {{ response }}</p>
    <p><a href="/logout">Logout</a></p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"].lower()

        # Greetings
        if "hello" in user_input or "hi" in user_input or "assalamu alaikum" in user_input:
            response = "Assalamu Alaikum! আমি আপনাকে কীভাবে সহায়তা করতে পারি?"

        # Weather
        elif "weather" in user_input:
            city = user_input.split("weather")[1].strip().capitalize()
            weather = mock_weather_data.get(city, "দুঃখিত, এই শহরের আবহাওয়ার তথ্য পাওয়া যায়নি।")
            if isinstance(weather, dict):
                response = f"{city} শহরে আবহাওয়া {weather['condition']} এবং তাপমাত্রা {weather['temperature']}."
            else:
                response = weather

        # Jokes
        elif "joke" in user_input or "জোকস" in user_input:
            response = random.choice(jokes)

        # Quotes
        elif "quote" in user_input or "উৎসাহ" in user_input:
            response = random.choice(quotes)

        # Math Operations
        elif "calculate" in user_input or "গণিত" in user_input:
            try:
                expression = user_input.split("calculate")[1].strip() if "calculate" in user_input else user_input.split("গণিত")[1].strip()
                result = eval(expression)
                response = f"ফলাফল: {result}."
            except Exception as e:
                response = "দুঃখিত, আমি এটি গণনা করতে পারিনি। অনুগ্রহ করে ইনপুটটি পরীক্ষা করুন।"

        # Games
        elif "play game" in user_input or "খেলা" in user_input:
            if "number" in user_input:
                response = play_number_game()
            elif "rock paper scissors" in user_input:
                response = play_rock_paper_scissors()
            else:
                response = "কোন খেলা খেলতে চান? সংখ্যা অনুমান খেলা ('play number game') বা রক-পেপার-সিসার্স ('play rock paper scissors')."

        # Farewells
        elif "bye" in user_input or "goodbye" in user_input or "বাই" in user_input:
            response = "আল্লাহ হাফেজ! ভালো থাকবেন।"

        # Unknown Input
        else:
            response = "দুঃখিত, আমি এটি বুঝতে পারিনি। অনুগ্রহ করে পুনরায় চেষ্টা করুন।"

    return render_template_string(HTML_TEMPLATE, response=response)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in user_profiles and user_profiles[username]["password"] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("chatbot"))
        else:
            return "Invalid username or password. Please try again."
    return render_template_string(HTML_TEMPLATE, response="")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in user_profiles:
            return "Username already exists. Please choose another one."
        user_profiles[username] = {"password": password}
        return "Registration successful! Please <a href='/login'>login</a>."
    return render_template_string(HTML_TEMPLATE, response="")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))

def play_number_game():
    secret_number = random.randint(1, 100)
    attempts = 0
    response = "Let's play a number guessing game! I'm thinking of a number between 1 and 100. Can you guess it?"
    while True:
        guess = int(input("Your guess: "))
        attempts += 1
        if guess < secret_number:
            response += "Too low! Try again."
        elif guess > secret_number:
            response += "Too high! Try again."
        else:
            response += f"Congratulations! You guessed the number {secret_number} in {attempts} attempts."
            break
    return response

def play_rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    user_choice = input("Choose rock, paper, or scissors: ").lower()
    if user_choice not in choices:
        return "Invalid choice. Please choose rock, paper, or scissors."
    if user_choice == computer_choice:
        return f"It's a tie! Both chose {user_choice}."
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return f"You win! Computer chose {computer_choice}."
    else:
        return f"You lose! Computer chose {computer_choice}."

if __name__ == "__main__":
    app.run(debug=True)