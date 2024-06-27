from flask import Flask, render_template, request
import spacy
from spacy.matcher import PhraseMatcher

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Define the conversation pairs
responses = {
    "hi": "Hi, I'm your HotelBot. How can I help you?",
    "types of rooms": "We have single, double, and suite rooms available.",
    "book a room": "You can book a room through our website or by calling our reservation desk.",
    "check-in time": "Our check-in time is from 2 PM onwards.",
    "check-out time": "Our check-out time is by 12 PM.",
    "free Wi-Fi": "Yes, we offer complimentary Wi-Fi for all our guests.",
    "breakfast included": "Yes, breakfast is included in the room rate.",
    "swimming pool": "Yes, we have an outdoor swimming pool.",
    "parking available": "Yes, we have free parking available for our guests.",
    "allow pets": "Unfortunately, we do not allow pets at our hotel.",
    "cancel booking": "Yes, you can cancel your booking. Please refer to our cancellation policy on the website.",
    "cancellation policy": "You can cancel your booking for free up to 24 hours before check-in.",
    "airport shuttle": "Yes, we offer airport shuttle service. Please contact our front desk for more details.",
    "restaurants nearby": "Yes, there are several restaurants within walking distance from the hotel.",
    "fitness center": "Yes, we have a fully-equipped fitness center available for our guests.",
    "extra bed": "Yes, extra beds are available upon request for an additional charge.",
    "room service": "Yes, we offer 24-hour room service.",
    "minibar": "Yes, all rooms are equipped with a minibar.",
    "connecting rooms": "Yes, we have connecting rooms available. Please request this during your booking.",
    "get to hotel from airport": "You can take our airport shuttle service, a taxi, or public transportation.",
    "laundry services": "Yes, we offer laundry and dry cleaning services.",
    "early check-in": "Early check-in is subject to availability. Please contact our front desk for more information.",
    "business center": "Yes, we have a business center with computers and printers available for our guests.",
    "shopping centers nearby": "Yes, there is a shopping center just a few minutes away from the hotel.",
    "payment methods": "We accept all major credit cards, debit cards, and cash.",
    "wheelchair accessible rooms": "Yes, we have wheelchair accessible rooms available.",
    "safe in room": "Yes, all rooms are equipped with a safe.",
    "discounts or promotions": "Yes, we offer various discounts and promotions throughout the year. Please check our website for current offers.",
    "book room for someone else": "Yes, you can book a room for someone else. Please provide their details during the booking process.",
    "smoking rooms": "No, our hotel is completely non-smoking.",
    "pet policy": "We do not allow pets in the hotel.",
    "cribs for babies": "Yes, cribs are available upon request.",
    "hairdryer": "Yes, all rooms are equipped with a hairdryer.",
    "tours or sightseeing packages": "Yes, we can arrange tours and sightseeing packages for you. Please contact the front desk for more information.",
    "store luggage": "Yes, we offer luggage storage services.",
    "iron and ironing board": "Yes, all rooms come with an iron and ironing board.",
    "conference rooms": "Yes, we have conference rooms available for meetings and events.",
    "attractions nearby": "Yes, there are several attractions nearby. Our front desk can provide you with more information and recommendations.",
    "loyalty program": "Yes, we have a loyalty program for our frequent guests. Please ask at the front desk for more details.",
    "pay upon arrival": "Yes, you can choose to pay upon arrival.",
    "currency exchange services": "Yes, we offer currency exchange services at the front desk.",
    "telephone in room": "Yes, all rooms are equipped with a telephone.",
    "book room for day use": "Yes, day-use bookings are available. Please contact our reservations team for more information.",
    "babysitting services": "Yes, babysitting services are available upon request.",
    "modify booking": "You can modify your booking by contacting our reservations team or through our website.",
    "rooms with a view": "Yes, we have rooms with beautiful views. Please request this during your booking.",
    "staff languages": "Our staff speaks multiple languages, including English, Spanish, and French.",
    "late check-out": "Late check-out is subject to availability and may incur an additional charge.",
    "on-site restaurant": "Yes, we have an on-site restaurant that serves breakfast, lunch, and dinner.",
    "room with kitchenette": "Yes, we have rooms with kitchenettes available. Please request this during your booking.",
    "age requirement for check-in": "Yes, the minimum age for check-in is 18 years old."
}

# Add patterns to the
for key in responses:
    pattern = nlp(key)
    matcher.add(key, [pattern])

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    doc = nlp(userText)
    matches = matcher(doc)
    
    if matches:
        best_match = max(matches, key=lambda x: x[1])
        response_key = nlp.vocab.strings[best_match[0]]
        return responses[response_key]
    else:
        return "I'm sorry, I don't understand your question."

if __name__ == "__main__":
    app.run(debug=True)

