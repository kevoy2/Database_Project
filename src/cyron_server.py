import os
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
from mysql.connector import errorcode
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    if request.method == 'POST':
        data = request.get_json()
        if data['role'] == 'Doctor':
            sql = "SELECT * FROM Doctor WHERE DoctorId = %s AND Pass = %s"
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close()
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
        elif data['role'] == 'Patient':
            sql = "SELECT * FROM Patient WHERE SSN = %s AND Pass = %s"
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close()
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
        else:
            sql = "SELECT * FROM Pharmacy WHERE PharmacyId = %s AND Pass = %s"
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close()
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
    
@app.route('/register', methods=['POST'])
def register():
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    if request.method == 'POST':
        sql = ""
        data = request.get_json()
        if data['role'] == 'Doctor':
            sql = "INSERT INTO Doctor (DoctorId, Name, DoctorType, Phone, Street, City, State, Pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (data['dr_id'],data['name'], data['dr_type'], data['phone'], data['street'], data['city'], data['state'], data['password'])
            cursor.execute(sql, val)
        elif data['role'] == 'Patient':
            sql = "INSERT INTO Patient (SSN, Name, Gender, Phone, Street, City, State, Pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (data['ssn'], data['name'], data['gender'], data['phone'], data['street'], data['city'], data['state'], data['password'])
            cursor.execute(sql, val)
        else:
            sql = "INSERT INTO Pharmacy (PharmacyId,Name, Hours, Phone, Street, City, State, Pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (data['pharma_id'],data['name'], data['hours'], data['phone'], data['street'], data['city'], data['state'], data['password'])
            cursor.execute(sql, val)
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Registration data received successfully'})

# Patient lookup
@app.route('/patient/<ssn>', methods=['GET'])
def get_patient(ssn):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT SSN, Name, Gender, Phone, Street, City, State FROM Patient WHERE SSN = %s", (ssn,))
    result = cursor.fetchone()
    cnx.close()()
    return jsonify(result)

# updates patient info
@app.route('/patient/<ssn>', methods=['PUT'])
def update_patient(ssn):
    data = request.get_json()
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    sql = "UPDATE Patient SET Name = %s,Gender = %s, Phone = %s, Street = %s, City = %s, State = %s WHERE SSN = %s"
    val = (data['name'],data['gender'], data['phone'], data['street'], data['city'], data['state'], ssn)
    cursor.execute(sql, val)
    cnx.commit()
    cnx.close()()
    return jsonify({'message': 'Patient updated'})

# delete's patient info
@app.route('/patient/<ssn>', methods=['DELETE'])
def delete_patient(ssn):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM Patient WHERE SSN = %s", (ssn,))
    cnx.commit()
    cnx.close()()
    return jsonify({'message': 'Patient deleted'})

# view doctor info
@app.route('/doctor/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT DoctorId, Name, DoctorType, Phone, Street, City, State FROM Doctor WHERE DoctorId = %s", (doctor_id,))
    result = cursor.fetchone()
    cnx.close()()
    return jsonify(result)

# update doctor info
@app.route('/doctor/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    data = request.get_json()
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    sql = "UPDATE Doctor SET Name = %s, DoctorType = %s, Phone = %s, Street = %s, City = %s, State = %s WHERE DoctorId = %s"
    val = (data['name'], data['dr_type'], data['phone'], data['street'], data['city'], data['state'], doctor_id)
    cursor.execute(sql, val)
    cnx.commit()
    cnx.close()()
    return jsonify({'message': 'Doctor updated'})

# delete doctor ingofo
@app.route('/doctor/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM Doctor WHERE DoctorId = %s", (doctor_id,))
    cnx.commit()
    cnx.close()()
    return jsonify({'message': 'Doctor deleted'})

# get pharmacy info
@app.route('/pharmacy/<pharma_id>', methods=['GET'])
def get_pharmacy(pharma_id):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT PharmacyId, Name, Hours, Phone, Street, City, State FROM Pharmacy WHERE PharmacyId = %s", (pharma_id,))
    result = cursor.fetchone()
    cnx.close()()
    return jsonify(result)

# update pharmacy info
@app.route('/pharmacy/<pharma_id>', methods=['PUT'])
def update_pharmacy(pharma_id):
    data = request.get_json()
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    sql = "UPDATE Pharmacy SET Name = %s, Hours = %s, Phone = %s, Street = %s, City = %s, State = %s WHERE PharmacyId = %s"
    val = (data['name'], data['hours'], data['phone'], data['street'], data['city'], data['state'], pharma_id)
    cursor.execute(sql, val)
    cnx.commit()
    cnx.close()()
    return jsonify({'message': 'Pharmacy updated'})

# delete pharmacy info
@app.route('/pharmacy/<pharma_id>', methods=['DELETE'])
def delete_pharmacy(pharma_id):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM Pharmacy WHERE PharmacyId = %s", (pharma_id,))
    cnx.commit()
    cnx.close()
    return jsonify({'message': 'Pharmacy deleted'})

# patient look up for doctors
@app.route('/doctor/<doctor_id>/patients', methods=['GET'])
def get_doctor_patients(doctor_id):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"), host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT SSN, PatientName, Phone, Street, City, State
        FROM Patient
        WHERE PrimaryDoctorId = %s
    """
    cursor.execute(sql, (doctor_id,))
    results = cursor.fetchall()
    cnx.close()
    return jsonify(results)

# get pharmacy stock
@app.route('/pharmacies/<pharmacy_id>/stock', methods=['GET'])
def get_pharmacy_stock(pharmacy_id):
    role = request.headers.get('role', None)  # Optional: sent by frontend

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    base_query = """
        SELECT d.DrugName, d.DEA_Schedule, s.Quantity
        FROM Stock s
        JOIN Drug d ON s.DrugId = d.DrugId
        WHERE s.PharmacyId = %s
    """

    if role == 'Patient':
        # Filter out Schedule II for patients
        base_query += " AND d.DEA_Schedule != 'CII'"

    cursor.execute(base_query, (pharmacy_id,))
    stock = cursor.fetchall()
    cnx.close()
    return jsonify(stock)


# search pharmacy by name
@app.route('/pharmacies/search_by_name', methods=['GET'])
def search_pharmacies_by_name():
    name = request.args.get('name')

    if not name:
        return jsonify({"error": "Missing pharmacy name"}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("""
        SELECT PharmacyId, Name, Hours, Phone, Street, City, State
        FROM Pharmacy
        WHERE Name LIKE %s
    """, ('%' + name + '%',))  # supports partial matches

    results = cursor.fetchall()
    cnx.close()()
    return jsonify(results)

# assign new meds to patient
@app.route('/takes', methods=['POST'])
def assign_medication_to_patient():
    data = request.get_json()
    ssn = data.get('ssn')
    new_drug_id = data.get('drug_id')
    override = data.get('override', False)  # default to False

    if not ssn or not new_drug_id:
        return jsonify({'error': 'Missing patient SSN or drug ID'}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    # Step 1: Get current drugs the patient is taking
    cursor.execute("""
        SELECT d.DrugId, d.DrugName
        FROM Takes t
        JOIN Drug d ON t.DrugId = d.DrugId
        WHERE t.SSN = %s
    """, (ssn,))
    current_drugs = cursor.fetchall()

    # Step 2: Check for interactions
    flagged = []
    blocked = []
    for drug in current_drugs:
        cursor.execute("""
            SELECT RiskLevel
            FROM Interactions
            WHERE DrugId = %s AND InteractsWith = %s
        """, (new_drug_id, drug['DrugName']))
        result = cursor.fetchone()
        if result:
            risk = result['RiskLevel']
            if risk.lower() == 'major':
                blocked.append(drug['DrugName'])
            elif risk.lower() in ['moderate', 'low']:
                flagged.append({'with': drug['DrugName'], 'risk': risk})

    # Step 3: Decide if it can be assigned
    if blocked and not override:
        cnx.close()()
        return jsonify({
            'error': 'Drug interaction too severe.',
            'conflicts': blocked,
            'message': 'Use "override": true to force the assignment.'
        }), 400

    # Step 4: Assign drug
    cursor.execute("INSERT INTO Takes (SSN, DrugId) VALUES (%s, %s)",
                   (ssn, new_drug_id))
    cnx.commit()
    cnx.close()()

    if blocked and override:
        return jsonify({
            'message': 'Drug assigned despite major interaction.',
            'forced_over': blocked
        })
    elif flagged:
        return jsonify({
            'message': 'Drug assigned with caution.',
            'warnings': flagged
        })
    else:
        return jsonify({'message': 'Medication assigned successfully'})



#views which medicine patient is taking
@app.route('/takes/<ssn>', methods=['GET'])
def get_patient_medications(ssn):
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.DrugName, t.Dosage
        FROM Takes t
        JOIN Drug d ON t.DrugId = d.DrugId
        WHERE t.SSN = %s
    """, (ssn,))
    
    meds = cursor.fetchall()
    cnx.close()()
    return jsonify(meds)

#updates stock at a pharmacy
@app.route('/stock', methods=['PUT'])
def update_pharmacy_stock():
    data = request.get_json()
    pharmacy_id = data.get('pharmacy_id')
    drug_id = data.get('drug_id')
    quantity = data.get('quantity')

    if not pharmacy_id or not drug_id or quantity is None:
        return jsonify({'error': 'Missing pharmacy_id, drug_id, or quantity'}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()

    # Check if stock entry exists
    cursor.execute("""
        SELECT * FROM Stock
        WHERE PharmacyId = %s AND DrugId = %s
    """, (pharmacy_id, drug_id))
    exists = cursor.fetchone()

    if exists:
        # Update quantity
        cursor.execute("""
            UPDATE Stock
            SET Quantity = %s
            WHERE PharmacyId = %s AND DrugId = %s
        """, (quantity, pharmacy_id, drug_id))
    else:
        # Insert new stock record
        cursor.execute("""
            INSERT INTO Stock (PharmacyId, DrugId, Quantity)
            VALUES (%s, %s, %s)
        """, (pharmacy_id, drug_id, quantity))

    cnx.commit()
    cnx.close()()

    return jsonify({'message': 'Stock updated successfully'})

#adds a drug search
@app.route('/drugs/search', methods=['GET'])
def search_drugs():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing drug name'}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT DrugId, DrugName, Type FROM Drug WHERE DrugName LIKE %s", ('%' + name + '%',))
    results = cursor.fetchall()
    cnx.close()
    return jsonify(results)

# returns all patient, pharmacy, and doctor data
@app.route('/patients', methods=['GET'])
def get_all_patients():
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT SSN, Name, Phone FROM Patient")
    results = cursor.fetchall()
    cnx.close()
    return jsonify(results)

# deletes a medication from patients profile
@app.route('/takes', methods=['DELETE'])
def delete_patient_medication_by_name():
    ssn = request.args.get('ssn')
    drug_name = request.args.get('drug_name')

    if not ssn or not drug_name:
        return jsonify({'error': 'Missing SSN or drug_name'}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()

    # Get the DrugId from DrugName
    cursor.execute("SELECT DrugId FROM Drug WHERE DrugName = %s", (drug_name,))
    result = cursor.fetchone()

    if not result:
        cnx.close()
        return jsonify({'error': 'Drug not found'}), 404

    drug_id = result[0]

    # Now delete from Takes
    cursor.execute("DELETE FROM Takes WHERE SSN = %s AND DrugId = %s", (ssn, drug_id))
    cnx.commit()
    cnx.close()

    return jsonify({'message': f'{drug_name} removed from patient'})

# deletes a patient medication by ID
@app.route('/takes', methods=['DELETE'])
def delete_patient_medication_by_ID():
    ssn = request.args.get('ssn')
    drug_id = request.args.get('drug_id')

    if not ssn or not drug_id:
        return jsonify({'error': 'Missing SSN or drug_id'}), 400

    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASS"),
                                  host=os.getenv("HOST"), database=os.getenv("DB"))
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM Takes WHERE SSN = %s AND DrugId = %s", (ssn, drug_id))
    cnx.commit()
    cnx.close()

    return jsonify({'message': 'Medication removed from patient'})
