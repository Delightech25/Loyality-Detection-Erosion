# Loyality-Detection-Erosion


A Flask-based web application designed to track user/customer engagement, detect signs of loyalty erosion (churn/defection), and trigger retention strategies.

## 🚀 Features

* **User Data Tracking:** Log and view interaction/transaction data.
* **Erosion / Churn Detection:** Identify users showing decreased activity or signs of disengagement.
* **Interactive Dashboard:** Simple Flask web UI for viewing reports and stats.

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** SQLite (`database.db`)
* **Frontend:** HTML5, CSS3 / Jinja2 Templates

## 📦 Project Structure

```text
Loyality-Detection-Erosion/
│── static/          # Static assets (CSS, JS, Images)
│── templates/       # HTML templates (Jinja2)
│── app.py           # Main application entry point
│── database.db      # SQLite database file
└── requirements.txt # Python dependencies```


⚙️ Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/Delightech25/Loyality-Detection-Erosion.git](https://github.com/Delightech25/Loyality-Detection-Erosion.git)
cd Loyality-Detection-Erosion

Create a virtual environment (optional but recommended):

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install required packages:

Bash
pip install -r requirements.txt
Run the application:

Bash
python app.py
Open in browser:
Navigate to http://127.0.0.1:5000 in your web browser.

📜 License
This project is available under the MIT License.


---

### Tips to keep in mind:
* **`requirements.txt`:** Ensure all required Python packages (like `Flask`) are listed in your `requirements.txt` so others can install them with `pip install -r requirements.txt`.
* **Database best practice:** If `database.db
