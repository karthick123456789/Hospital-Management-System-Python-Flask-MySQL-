

from flask import Flask, render_template, redirect, request, url_for

from db import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/add',methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "insert into patients (name,age,disease) values (%s,%s,%s)",
            (name,age,disease)
        )
        con.commit()

        cur.close()

        return redirect(url_for('view_patients'))
    return render_template("add_patient.html")

@app.route('/delete-patient/<int:id>')
def delete_patient(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "delete from appointments where patient_id = %s",(id)
    )
    cur.execute(
        "delete from patients  where id = %s",(id)
    )
    con.commit()
    cur.close()
    return redirect(url_for('view_patients'))

@app.route('/patients')

def view_patients():
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from patients")

    patients = cur.fetchall()
    cur.close()
    return render_template("view_patient.html",patients=patients)

@app.route('/doctors')
def view_doctors():
    con = get_connection()
    cur = con.cursor()
    cur.execute("select * from doctors")

    doctors = cur.fetchall()
    cur.close()
    return render_template("view_doctor.html",doctors=doctors)

@app.route("/book" , methods=['GET','POST'])
def book_appointment():
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "select id,name from patients"
    )
    patients = cur.fetchall()
    cur.execute("select id,name from doctors")
    doctors = cur.fetchall()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date  = request.form['date']

        cur.execute(
            "insert into appointments (patient_id,doctor_id,date) values (%s,%s,%s)",
            (patient_id,doctor_id,date)
        )
        con.commit()
        cur.close()
        return redirect(url_for('view_appointments'))
    cur.close()
    return render_template("book_appointment.html", patients=patients, doctors=doctors)

@app.route("/appointments")
def view_appointments():

    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """select a.id, p.name, d.name, a.date
        from appointments a
        join patients p on a.patient_id = p.id
        join doctors d on a.doctor_id = d.id
        """)
    appointments = cur.fetchall()
    cur.close()

    return render_template("view_appointments.html", appointments=appointments)

@app.route("/add-doctors",methods=['GET','POST'])
def add_doctors():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']

        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "insert into doctors (name,specialization) values (%s,%s)",
            (name,specialization)
        )
        con.commit()
        cur.close()
        return redirect(url_for('view_doctors'))
    return render_template("add_doctor.html")

@app.route("/edit-doctor/<int:id>",methods=['GET','POST'])
def edit_doctor(id):
    con = get_connection()
    cur = con.cursor()

    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']

        cur.execute(
            "update doctors set name = %s, specialization = %s where id = %s",
            (name,specialization,id)
        )
        con.commit()

        return redirect(url_for('view_doctors'))
    cur.execute("select * from doctors where id = %s",(id))
    doctor = cur.fetchone()
    cur.close()

    return render_template('/edit-doctor.html',doctor=doctor)


if __name__ == '__main__':
    app.run(debug=True)
