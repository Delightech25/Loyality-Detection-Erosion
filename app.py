from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import pandas as pd
import random
import io
import plotly.express as px

app = Flask(__name__)
app.secret_key = "secret123"

DB="database.db"


def init_db():

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    brand TEXT,
    quantity INTEGER,
    date TEXT)
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":

        u=request.form["username"]
        p=request.form["password"]

        conn=sqlite3.connect(DB)
        cur=conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))

        user=cur.fetchone()
        conn.close()

        if user:
            session["user"]=u
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        u=request.form["username"]
        p=request.form["password"]

        conn=sqlite3.connect(DB)
        cur=conn.cursor()

        try:
            cur.execute("INSERT INTO users(username,password) VALUES (?,?)",(u,p))
            conn.commit()
        except:
            return "Username already exists"

        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn=sqlite3.connect(DB)
    df=pd.read_sql_query("SELECT * FROM purchases",conn)
    conn.close()

    risk_table=[]
    suspicious=[]

    brand_chart=""
    loyalty_chart=""
    trend_chart=""
    heatmap_chart=""

    if not df.empty:

        grouped=df.groupby(["customer","brand"]).size().unstack(fill_value=0)

        for customer in grouped.index:

            brands=grouped.loc[customer]

            score=brands.max()/brands.sum()

            if score>0.75:
                risk="Low"
                action="Send loyalty reward"

            elif score>0.5:
                risk="Medium"
                action="Offer discount coupon"

            else:
                risk="High"
                action="Urgent retention offer"
                suspicious.append(customer)

            risk_table.append({
                "customer":customer,
                "score":round(score,2),
                "risk":risk,
                "action":action
            })

        brand_totals=df.groupby("brand")["quantity"].sum()

        fig1=px.bar(x=brand_totals.index,y=brand_totals.values,title="Brand Distribution")
        brand_chart=fig1.to_html(full_html=False)

        customers=[r["customer"] for r in risk_table]
        scores=[r["score"] for r in risk_table]

        fig2=px.bar(x=customers,y=scores,title="Customer Loyalty Scores")
        loyalty_chart=fig2.to_html(full_html=False)

        trend=df.groupby("date")["quantity"].sum()
        fig3=px.line(x=trend.index,y=trend.values,title="Purchase Trend")
        trend_chart=fig3.to_html(full_html=False)

        heatmap=px.imshow(grouped,title="Customer Brand Loyalty Heatmap")
        heatmap_chart=heatmap.to_html(full_html=False)

    return render_template("dashboard.html",
                           risk_table=risk_table,
                           brand_chart=brand_chart,
                           loyalty_chart=loyalty_chart,
                           trend_chart=trend_chart,
                           heatmap_chart=heatmap_chart)


@app.route("/add",methods=["POST"])
def add():

    customer=request.form["customer"]
    brand=request.form["brand"]
    quantity=request.form["quantity"]
    date=request.form["date"]

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute(
    "INSERT INTO purchases(customer,brand,quantity,date) VALUES (?,?,?,?)",
    (customer,brand,quantity,date))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/generate")
def generate():

    customers=["C1","C2","C3","C4","C5"]
    brands=["BrandA","BrandB","BrandC"]

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    for i in range(30):

        cur.execute(
        "INSERT INTO purchases(customer,brand,quantity,date) VALUES (?,?,?,?)",
        (
        random.choice(customers),
        random.choice(brands),
        random.randint(1,5),
        "2025-02-"+str(random.randint(1,28))
        )
        )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/upload",methods=["POST"])
def upload():

    file=request.files["file"]

    df=pd.read_excel(file)

    conn=sqlite3.connect(DB)
    df.to_sql("purchases",conn,if_exists="append",index=False)
    conn.close()

    return redirect("/dashboard")


@app.route("/download")
def download():

    conn=sqlite3.connect(DB)
    df=pd.read_sql_query("SELECT * FROM purchases",conn)
    conn.close()

    output=io.BytesIO()

    with pd.ExcelWriter(output,engine="openpyxl") as writer:
        df.to_excel(writer,index=False)

    output.seek(0)

    return send_file(output,
                     download_name="loyalty_report.xlsx",
                     as_attachment=True)


@app.route("/clear")
def clear():

    conn=sqlite3.connect(DB)
    cur=conn.cursor()

    cur.execute("DELETE FROM purchases")

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)