from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "farmer_portal"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("farmers.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS queries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT)""")

    conn.commit()
    conn.close()

init_db()

# ---------------- MULTILINGUAL ----------------

translations = {

"en":{
"title":"Farmer Portal",
"crop":"Crop Recommendation",
"scheme":"Government Schemes",
"queries":"Farmer Queries"
},

"te":{
"title":"రైతు పోర్టల్",
"crop":"పంట సూచన",
"scheme":"ప్రభుత్వ పథకాలు",
"queries":"రైతు ప్రశ్నలు"
},

"hi":{
"title":"किसान पोर्टल",
"crop":"फसल सुझाव",
"scheme":"सरकारी योजनाएँ",
"queries":"किसान प्रश्न"
}

}

# ADD THIS BELOW THE TRANSLATIONS

crop_labels = {

"en":{
"title":"Crop Recommendation",
"nitrogen":"Nitrogen",
"phosphorus":"Phosphorus",
"potassium":"Potassium",
"temperature":"Temperature",
"humidity":"Humidity",
"ph":"Soil pH",
"rainfall":"Rainfall"
},

"te":{
"title":"పంట సూచన",
"nitrogen":"నత్రజని",
"phosphorus":"భాస్వరం",
"potassium":"పొటాషియం",
"temperature":"ఉష్ణోగ్రత",
"humidity":"ఆర్ద్రత",
"ph":"మట్టి pH",
"rainfall":"వర్షపాతం"
},

"hi":{
"title":"फसल सुझाव",
"nitrogen":"नाइट्रोजन",
"phosphorus":"फास्फोरस",
"potassium":"पोटैशियम",
"temperature":"तापमान",
"humidity":"नमी",
"ph":"मिट्टी pH",
"rainfall":"वर्षा"
}

}
scheme_labels = {

"en":{
"title":"Government Scheme Eligibility",
"name":"Farmer Name",
"age":"Farmer Age",
"income":"Annual Income",
"land":"Land Area (Acres)",
"aadhaar":"Upload Aadhaar",
"button":"Check Eligibility & Download Certificate"
},

"te":{
"title":"ప్రభుత్వ పథకాల అర్హత",
"name":"రైతు పేరు",
"age":"రైతు వయస్సు",
"income":"వార్షిక ఆదాయం",
"land":"భూమి విస్తీర్ణం (ఎకరాలు)",
"aadhaar":"ఆధార్ అప్‌లోడ్ చేయండి",
"button":"అర్హత పరిశీలించండి & సర్టిఫికేట్ డౌన్‌లోడ్"
},

"hi":{
"title":"सरकारी योजना पात्रता",
"name":"किसान का नाम",
"age":"किसान की आयु",
"income":"वार्षिक आय",
"land":"भूमि क्षेत्र (एकड़)",
"aadhaar":"आधार अपलोड करें",
"button":"पात्रता जांचें और प्रमाणपत्र डाउनलोड करें"
}

}

# ---------------- LANGUAGE ----------------

@app.route("/set_lang/<lang>")
def set_lang(lang):

    session["lang"] = lang

    page = request.referrer

    if page:
        return redirect(page)

    return redirect("/dashboard")
# ---------------- LOGIN + REGISTER ----------------
@app.route("/", methods=["GET","POST"])
def login():

    message = ""

    if request.method == "POST":

        action = request.form["action"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("farmers.db")
        c = conn.cursor()

        if action == "register":

            c.execute("SELECT * FROM users WHERE username=?",(username,))
            existing = c.fetchone()

            if existing:
                message = "User already exists. Please login."
            else:
                c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
                conn.commit()
                message = "Registration successful. Please login."

        if action == "login":

            c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
            user = c.fetchone()

            if user:
                session["user"] = username
                conn.close()
                return redirect("/dashboard")
            else:
                message = "Account not found. Please register first."

        conn.close()

    return render_template("login.html",message=message)

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    lang = session.get("lang","en")

    return render_template("dashboard.html",t=translations[lang])

# ---------------- CROP PAGE ----------------

@app.route("/crop")
def crop():

    lang = session.get("lang","en")

    return render_template(
        "crop.html",
        labels=crop_labels[lang],
        result=""
    )

# ---------------- CROP PREDICTION ----------------

@app.route("/predict_crop", methods=["POST"])
def predict_crop():

    lang = session.get("lang","en")

    try:
        n = float(request.form["nitrogen"])
        p = float(request.form["phosphorus"])
        k = float(request.form["potassium"])
        temp = float(request.form["temperature"])
        hum = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rain = float(request.form["rainfall"])

        score = n + p + k + temp + hum + ph + rain

        crops = [
            "Rice",
            "Wheat",
            "Maize",
            "Cotton",
            "Sugarcane",
            "Banana",
            "Mango"
        ]

        result = crops[int(score) % len(crops)]

        return render_template(
            "crop.html",
            labels=crop_labels[lang],
            result="Recommended Crop: " + result
        )

    except:
        return render_template(
            "crop.html",
            labels=crop_labels[lang],
            result="Please enter valid numbers."
        )

# ---------------- SCHEME PAGE ----------------

@app.route("/scheme")
def scheme():

    lang = session.get("lang","en")

    return render_template(
        "scheme.html",
        labels=scheme_labels[lang]
    )

# ---------------- CHECK SCHEME ----------------

@app.route("/check_scheme", methods=["POST"])
def check_scheme():

    name = request.form["name"]
    age = int(request.form["age"])
    income = float(request.form["income"])
    land = float(request.form["land"])

    aadhaar = request.files["aadhaar"]

    if aadhaar.filename == "":
        return "Please upload Aadhaar to continue."

    path = os.path.join(UPLOAD_FOLDER, aadhaar.filename)
    aadhaar.save(path)

    schemes = []

    # Scheme eligibility based on income

    if income <= 100000:
        schemes.append("PM-Kisan Samman Nidhi")

    if income <= 150000:
        schemes.append("Small and Marginal Farmer Support Scheme")

    if income <= 200000:
        schemes.append("Pradhan Mantri Fasal Bima Yojana")

    if age <= 40:
        schemes.append("Young Farmer Development Scheme")

    if land <= 2:
        schemes.append("Soil Health Card Scheme")

    schemes.append("Kisan Credit Card")
    schemes.append("PM Krishi Sinchai Yojana")

    # ---------- PDF Certificate ----------

    filename = "scheme_certificate.pdf"

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Government Scheme Eligibility Certificate", styles["Title"]))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"Farmer Name: {name}", styles["Normal"]))
    story.append(Paragraph(f"Age: {age}", styles["Normal"]))
    story.append(Paragraph(f"Income: ₹{income}", styles["Normal"]))
    story.append(Paragraph(f"Land Area: {land} acres", styles["Normal"]))

    story.append(Spacer(1,20))

    story.append(Paragraph("Eligible Government Schemes:", styles["Heading2"]))

    for s in schemes:
        story.append(Paragraph("• " + s, styles["Normal"]))

    doc = SimpleDocTemplate(filename)
    doc.build(story)

    return send_file(filename, as_attachment=True)

    # -------- PDF --------

    pdf = "certificate.pdf"

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Farmer Eligibility Certificate",styles["Title"]))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"Name: {name}",styles["Normal"]))
    story.append(Paragraph(f"Age: {age}",styles["Normal"]))
    story.append(Paragraph(f"Income: {income}",styles["Normal"]))
    story.append(Paragraph(f"Land: {land} acres",styles["Normal"]))

    story.append(Spacer(1,20))

    story.append(Paragraph("Eligible Government Schemes:",styles["Heading2"]))

    for s in schemes:
        story.append(Paragraph("• "+s,styles["Normal"]))

    doc = SimpleDocTemplate(pdf)
    doc.build(story)

    return send_file(pdf,as_attachment=True)

# ---------------- QUERIES PAGE ----------------

@app.route("/queries")
def queries():
    return render_template("queries.html", answer="")

# ---------------- CHATBOT ----------------

def chatbot(q):

    q = q.lower()

    if "rice" in q:
        return "Rice grows well in warm climates with good rainfall."

    elif "wheat" in q:
        return "Wheat grows in cooler climates."

    elif "fertilizer" in q:
        return "Balanced NPK fertilizers improve crop yield."

    elif "water" in q:
        return "Drip irrigation saves water and improves yield."

    elif "scheme" in q:
        return "Visit Government Schemes dashboard."

    else:
        return "Please ask agriculture related questions."

@app.route("/ask", methods=["POST"])
def ask():

    question = request.form["question"]

    answer = chatbot(question)

    conn = sqlite3.connect("farmers.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO queries(question,answer) VALUES(?,?)",
        (question, answer)
    )

    conn.commit()
    conn.close()

    return render_template("queries.html", answer=answer)
# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)