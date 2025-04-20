import os
import sqlite3
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from mysql.connector import errorcode
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor(buffered=True)
    if request.method == 'POST':
        data = request.get_json()
        if data['role'] == 'Doctor':
            sql = 'SELECT * FROM doctor WHERE Doctor_ID = %s AND Password = %s'
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
        elif data['role'] == 'Patient':
            sql = 'SELECT * FROM patient WHERE SSN = %s AND Password = %s'
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
        else:
            sql = 'SELECT * FROM pharmacy WHERE Pharmacy_ID = %s AND Password = %s'
            val = (data['id'], data['password'])
            cursor.execute(sql, val)
            rlt = cursor.fetchall()
            cnx.close
            if len(rlt) == 1:
                return jsonify({'message': 'Login credintials successful', 'state': 't', 'role': data['role']})
            else:
                return jsonify({'message': 'Login credintials unsuccessful', 'state': 'f', 'role': data['role']})
    
@app.route('/register', methods=['POST'])
def register():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    if request.method == 'POST':
        data = request.get_json()
        cursor = cnx.cursor(buffered=True)
        if data['role'] == 'Doctor':
            sql = 'SELECT COUNT(*) FROM doctor WHERE Doctor_ID = %s'
            val = (data['dr_id'],)
            cursor.execute(sql, val)
            resp = cursor.fetchone()
            if resp[0] == 0:
                sql = 'INSERT INTO doctor (Doctor_ID, Type, Name, Phone, Address_Zip_Code, Address_State, Address_City, Address_Street, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                val = (data['dr_id'], data['dr_type'], data['name'], data['phone'], data['zip'], data['state'], data['city'], data['street'], data['password'])
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received successfully'})
            else:
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received unsuccessfully'})

        elif data['role'] == 'Patient':
            sql = 'SELECT COUNT(*) FROM patient WHERE SSN = %s'
            val = (data['ssn'],)
            cursor.execute(sql, val)
            resp = cursor.fetchone()
            if resp[0] == 0:
                sql = 'INSERT INTO patient (SSN, Name, Gender, Phone, Birthday, Address_Zip_Code, Address_State, Address_City, Address_Street, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                val = (data['ssn'], data['name'], data['gender'], data['phone'], data['dob'], data['zip'], data['state'], data['city'], data['street'], data['password'])
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received successfully'})
            else:
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received unsuccessfully'})
        elif data['role'] == "Pharmacy":
            sql = 'SELECT COUNT(*) FROM pharmacy WHERE Pharmacy_ID = %s'
            val = (data['pharma_id'],)
            cursor.execute(sql, val)
            resp = cursor.fetchone()
            if resp[0] == 0:
                sql = 'INSERT INTO pharmacy (Pharmacy_ID, Pharmacy_Name, Hours, Phone, Address_Zip_Code, Address_State, Address_City, Address_Street, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                val = (data['pharma_id'], data['name'], data['hours'], data['phone'], data['zip'], data['state'], data['city'], data['street'], data['password'])
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received successfully'})
            else:
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Registration data received unsuccessfully'})
        else: 
            cnx.commit()
            cnx.close()
            return jsonify({'message': 'Registration data received unsuccessfully'}) 
    
@app.route('/perscribe', methods=['POST'])
def addPerscribe():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    data = request.get_json()
    cursor = cnx.cursor(buffered=True)
    sql = 'SELECT COUNT(*) FROM patient WHERE SSN=%s'
    val = (data['ssn'],)
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 1:
        sql = 'SELECT D.Drug_ID, D.Generic_Name FROM takes T JOIN drug D ON T.Drug_ID = D.Drug_ID WHERE T.SSN = %s'
        val = (data['ssn'],)
        cursor.execute(sql, val)
        current_drugs = cursor.fetchall()
        flagged = []
        blocked = []
        sql = 'SELECT Generic_Name FROM drug WHERE Drug_ID = %s'
        val = (data['meds'],)
        cursor.execute(sql, val)
        name = cursor.fetchone()
        print(data['override'])
        for drug in current_drugs:
            print(drug)
            print(name[0])
            sql = 'SELECT Risk_Level FROM interactions WHERE Drug_ID = %s AND Interacts_With = %s'
            val = (drug[0], name[0])
            cursor.execute(sql, val)
            result = cursor.fetchone()
            print(result)
            if result:
                risk = result[0]
                if risk.lower() == 'major':
                    blocked.append(drug[1])
                elif risk.lower() in ['moderate', 'low']:
                    flagged.append({'with': drug[1], 'risk': risk})
        if len(blocked) != 0 and data['override'] == 'n':
            cnx.close()
            return jsonify({'message': 'Drug interaction too severe.'})
        sql = 'INSERT INTO Takes (SSN, Drug_ID) VALUES (%s, %s)'
        val = (data['ssn'], data['meds'])
        cursor.execute(sql, val)
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Perscrition added successfully.'})
    else: 
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'The patient do not exist.'})
    
@app.route('/view-perscription', methods=['POST'])
def showPerscribe():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor(buffered=True)
    data = request.get_json()
    sql = 'SELECT COUNT(*) FROM drug D, takes T WHERE D.Drug_ID = T.Drug_ID AND T.SSN = %s'
    val = (data['id'],)
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] >= 1:
        cursor.execute(sql, val)
        sql = 'SELECT D.Drug_ID, D.Generic_Name, D.DEA_Schedule, D.Common_Uses FROM drug D, takes T WHERE D.Drug_ID = T.Drug_ID AND T.SSN = %s'
        val = (data['id'],)
        cursor.execute(sql, val)
        resp = cursor.fetchall()
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Drug data retrieved successfully', 'resp': resp})
    else:
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'No perscriptions are assigned'})
    
@app.route('/add-patient', methods=['POST'])
def addPatient():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor(buffered=True)
    data = request.get_json()
    sql = 'SELECT COUNT(*) FROM patient WHERE SSN=%s AND Name=%s AND Address_Zip_Code=%s'
    val = (data['ssn'], data['name'], data['zip'])
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 1:
        sql = 'SELECT COUNT(*) FROM sees WHERE SSN=%s AND Doctor_ID=%s'
        val = (data['ssn'], data['id'])
        cursor.execute(sql, val)
        resp = cursor.fetchone()
        if resp[0] == 0:
            sql = 'SELECT COUNT(*) FROM sees WHERE SSN=%s'
            val = (data['ssn'],)
            cursor.execute(sql, val)
            resp = cursor.fetchone()
            if resp[0] == 0:
                sql = 'INSERT INTO sees (SSN, Doctor_ID) VALUES (%s, %s)'
                val = (data['ssn'], data['id'])
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'Doctor added the patient successfully'})
            else:
                cnx.commit()
                cnx.close()
                return jsonify({'message': 'The patient already has a doctor'})
        else:
            cnx.commit()
            cnx.close()
            return jsonify({'message': 'You already added this patient'}) 
    else: 
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Patient is not in database'})
    
@app.route('/view-patient', methods=['POST'])
def viewPatient():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor(buffered=True)
    data = request.get_json()
    sql = 'SELECT COUNT(*) FROM patient WHERE SSN=%s'
    val = (data['ssn'],)
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 1:
        sql = 'SELECT COUNT(*) FROM sees WHERE SSN=%s AND Doctor_ID=%s'
        val = (data['ssn'], data['id'])
        cursor.execute(sql, val)
        resp = cursor.fetchone()
        if resp[0] == 1:
            sql = 'SELECT SSN, Name, Gender, Name FROM patient WHERE SSN=%s'
            val = (data['ssn'],)
            cursor.execute(sql, val)
            resp = cursor.fetchone()
            sql = 'SELECT Condition_Code FROM has WHERE SSN=%s'
            val = (data['ssn'],)
            cursor.execute(sql, val)
            codes = cursor.fetchall()
            sql = 'SELECT D.Generic_Name FROM drug D, takes T WHERE D.Drug_ID = T.Drug_ID AND T.SSN=%s'
            val = (data['ssn'],)
            cursor.execute(sql, val)
            names = cursor.fetchall()
            cnx.commit()
            cnx.close()
            return jsonify({'message': 'Patient data received successfully', 'ssn': resp[0], 'name': resp[1], 'gender': resp[2], 'phone': resp[3], 'codes': codes, 'meds': names })
        else:
            cnx.commit()
            cnx.close()
            return jsonify({'message': 'Patient is not assigned to you'})
    else: 
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Patient is not in database'})
    
@app.route('/view-doctor', methods=['POST'])
def showDoctor():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor(buffered=True)
    data = request.get_json()
    sql = 'SELECT COUNT(*) FROM doctor D, sees S WHERE D.Doctor_ID = S.Doctor_ID AND S.SSN = %s'
    val = (data['id'],)
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 1:
        cursor.execute(sql, val)
        sql = 'SELECT D.Doctor_ID, D.Name, D.Type, D.Phone FROM doctor D, sees S WHERE D.Doctor_ID = S.Doctor_ID AND S.SSN = %s'
        val = (data['id'],)
        cursor.execute(sql, val)
        resp = cursor.fetchone()
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Doctor data received successfully', 'id': resp[0], 'name': resp[1], 'type': resp[2], 'phone': resp[3]})
    else:
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'No doctor is assigned',})

@app.route('/add-stock', methods=['POST'])
def restock():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    data = request.get_json()
    data['quan'] = int(data['quan'])
    cursor = cnx.cursor(buffered=True)
    sql = 'SELECT COUNT(*) FROM stock WHERE Pharmacy_ID=%s AND Drug_ID=%s'
    val = (data['pharma'], data['meds'])
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 0:
        sql = 'INSERT INTO stock (Pharmacy_ID, Drug_ID, Quantity) VALUES (%s, %s, %s)'
        val = (data['pharma'], data['meds'], data['quan'])
        cursor.execute(sql, val)
    else:
        sql = 'UPDATE stock SET Quantity=Quantity+%s WHERE Pharmacy_ID=%s AND Drug_ID=%s'
        val = (data['quan'], data['pharma'], data['meds'])
        cursor.execute(sql, val)
    cnx.commit()
    cnx.close()
    return jsonify({'message': 'Stock added successfully'})

@app.route('/remove-stock', methods=['POST'])
def unstock():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    data = request.get_json()
    cursor = cnx.cursor(buffered=True)
    sql = 'SELECT COUNT(*) FROM stock WHERE Pharmacy_ID=%s AND Drug_ID=%s'
    val = (data['pharma'], data['del'])
    cursor.execute(sql, val)
    resp = cursor.fetchone()
    if resp[0] == 0:
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'You don\'t have that medicine in stock.'})
    else:
        sql = 'DELETE FROM stock WHERE Pharmacy_ID=%s AND Drug_ID=%s'
        val = (data['pharma'], data['del'])
        cursor.execute(sql, val)
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Stock deleted successfully'})
    
@app.route('/view-stock', methods=['POST'])
def viewStock():
    cnx = mysql.connector.connect(user=os.getenv('USER'), password=os.getenv('PASS'), host=os.getenv('HOST'), database=os.getenv('DB'))
    cursor = cnx.cursor()
    data = request.get_json()
    if request.method == 'POST':
        sql = 'SELECT D.Generic_Name, S.Quantity FROM drug D, stock S WHERE D.Drug_ID=S.Drug_ID AND S.Pharmacy_ID=%s AND D.DEA_Schedule<>%s'
        val = (data['pharma'], data['exempt'])
        cursor.execute(sql, val)
        result = cursor.fetchall()
        x = [row[0] for row in result]
        y = [row[1] for row in result]
        cnx.commit()
        cnx.close()
        return jsonify({'message': 'Graphing stocks was successfully', 'x': x, 'y': y})