from flask import Flask, render_template
import os
import json

app = Flask(__name__, template_folder=".") 

@app.route('/')
@app.route('/index') 
def index(): 
    args = {
        "customer_name" : "Sigma",
        "booking_code": "BAC23",
        "start": "02-02-2024",
        "end": "03-02-2024",
        "number_of_rooms": "2",
        "room_type": "Deluxe",
        "bed_type": "Single",
        "allow_smoking": "0",
        "incl_breakfast": "1",
        "price": "599000",
        "phone_number": "08123123123",
        "email": "sigmaapha@gmail.com",
        "company": "Hotel Daily Inn"
    }

    return render_template(f'booking_email.html', data=args)

if __name__ == '__main__': 
    app.run() 