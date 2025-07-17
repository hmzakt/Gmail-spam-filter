from flask import Flask, jsonify
from flask_cors import CORS
import joblib
from gmail_flow import fetch_latest_emails, clean_email_text, auth, move_to_spam

model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
service = auth()

app = Flask(__name__)
CORS(app)  

@app.route("/api/get-mails", methods=["GET"])
def get_mails():
    mails, msg_ids = fetch_latest_emails(service, max_results=10)
    cleaned_emails = [clean_email_text(e) for e in mails]
    predictions = model.predict(vectorizer.transform(cleaned_emails))

    response = []
    for i, (label, msg_id) in enumerate(zip(predictions,msg_ids), 1):
        response.append({
            "id": i,
            "text": mails[i-1][:200], 
            "label": "Spam" if label == 1 else "Not Spam"
        })

    return jsonify(response)

@app.route("/api/filter-spam", methods=["POST"])
def filter_and_move_spam():
    try:
        mails, msg_ids = fetch_latest_emails(service, max_results=10)
        cleaned_emails = [clean_email_text(m) for m in mails]
        predictions = model.predict(vectorizer.transform(cleaned_emails))

        moved = []
        for raw, label, msg_id in zip(mails, predictions, msg_ids):
            if label == 1:  
                move_to_spam(service, msg_id)
                moved.append({
                    "msg_id": msg_id,
                    "text": raw[:200]
                })

        return jsonify({
            "message": f"Moved {len(moved)} messages to spam.",
            "moved": moved
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


