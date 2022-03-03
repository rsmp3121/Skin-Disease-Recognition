from grpc import Status
from flask_mail import Mail, Message
from sklearn.ensemble import RandomForestClassifier
from logging import log
from os import name, stat
import os
from flask import Flask, json, render_template, request, session, url_for, jsonify, flash
from flask.templating import render_template_string
from skimage import feature
from werkzeug.datastructures import Headers
from werkzeug.utils import redirect
from DBConnection import Db
import cv2
import pandas as pd

import time
import datetime
from encodings.base64_codec import base64_decode
import base64


app = Flask(__name__)
app.secret_key = "abc"


# -----------------dont touch

# mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dermz3121@gmail.com'
app.config['MAIL_PASSWORD'] = '#3121dermz'
app.config['MAIL_DEFAULT_SENDER'] = 'dermz3121@gmail.com'
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# -------------------------------------------------------------------------------------------------------------------------------#
#Admin Begins#
# -------------------------------------------------------------------------------------------------------------------------------#
#--------------add-disease--and--view-disease--and--edit-disease---and-delete-disease-begins-----------------------------------------------------------------#


@app.route("/adm_add_disease")
def adm_add_disease():
    if session['alid'] == "1":
        return render_template("admin/add_disease.html")
    else:
        return redirect(url_for('adm_login'))


@app.route("/adm_add_disease_post", methods=['post'])
def adm_add_disease_post():
    if session['alid'] == "1":
        i = Db()
        name = request.form['add_disease_name']
        image = request.files['add_disease_image']
        image.save('C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\'+image.filename)
        path = '/static/disease_images/'+image.filename
        description = request.form['add_disease_description']
        qry = "INSERT INTO disease(NAME,image,descriptions)VALUES('" + \
            name+"','"+path+"','"+description+"')"
        ans = i.insert(qry)
        return adm_add_disease()
    else:
        return redirect(url_for('adm_login'))

    #**********view-disease-begins************#


@app.route('/adm_view_disease')
def adm_view_disease():
    if session['alid'] == "1":
        v = Db()
        qry = "SELECT * FROM disease"
        res = v.select(qry)
        print(res)
        return render_template('/admin/view_disease.html', val=res)
    else:
        return redirect(url_for('adm_login'))

    #disease_search_section_starts#


@app.route('/adm_view_disease_post', methods=['post'])
def adm_view_disease_post():
    if session['alid'] == "1":
        v = Db()
        name = request.form['disease_search_name']
        qry = "SELECT * FROM disease WHERE NAME LIKE '%"+name+"%'"
        res = v.select(qry)
        print(res)
        return render_template('/admin/view_disease.html', val=res)
    else:
        return redirect(url_for('adm_login'))

    #disease_search_section_ends#
    #***********view-disease-ends**************#

    #***********edit-disease-begins************#


@app.route('/adm_edit_disease/<disease_id>')
def adm_edit_disease(disease_id):
    if session['alid'] == "1":
        e = Db()
        session['disease_id'] = disease_id
        qry = "SELECT * FROM disease WHERE disease_id='" + disease_id + "'"
        ans = e.selectOne(qry)
        print(ans)
        return render_template('/admin/edit_disease.html', val=ans)

    else:
        return redirect(url_for('adm_login'))


@app.route('/adm_edit_disease_post', methods=['post'])
def adm_edit_disease_post():
    if session['alid'] == "1":
        e = Db()
        name = request.form['edit_disease_name']

        description = request.form['edit_disease_description']
        if "edit_disease_image" in request.files:
            image = request.files['edit_disease_image']
            if image.filename != "":
                image.save(
                    "C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\" + image.filename)
                path = "static/disease_images/" + image.filename
                qry = "UPDATE disease SET NAME='"+name+"',image='"+path+"',descriptions='" + \
                    description+"' WHERE disease_id= '" + \
                    str(session['disease_id'])+"'"
                res = e.update(qry)
            else:
                qry = "UPDATE disease SET NAME='"+name+"',descriptions='" + \
                    description+"' WHERE disease_id= '" + \
                    str(session['disease_id'])+"'"
                res = e.update(qry)
        else:
            qry = "UPDATE disease SET NAME='"+name+"',descriptions='" + \
                description+"' WHERE disease_id= '" + \
                str(session['disease_id'])+"'"
            res = e.update(qry)
        return adm_view_disease()
    else:
        return redirect(url_for('adm_login'))

    #***********edit-disease-ends**************#

    #***********delete-disease-begins**********#


@app.route('/adm_delete_disease/<disease_id>')
def delete_student(disease_id):
    if session['alid'] == "1":
        d = Db()
        qry = "DELETE FROM disease WHERE disease_id='" + disease_id + "'"
        res = d.delete(qry)
        return adm_view_disease()
    else:
        return redirect(url_for('adm_login'))

    #*******delete-disease-ends***************#


#--------------add-disease--and--view-disease--and--edit-disease--and --delete-disease ends---------------------------------------------------------------#

#--------------add-doctor--and--view-doctor--and--edit-doctor--and --delete-doctor begins-----------------------------------------------------------------#

@app.route("/adm_add_doctor")
def adm_add_doctor():
    if session['alid'] == "1":
        return render_template('/admin/add_doctor.html')
    else:
        return redirect(url_for('adm_login'))


@app.route("/adm_add_doctor_post", methods=['post'])
def adm_add_doctor_post():
    if session['alid'] == "1":
        i = Db()
        name = request.form['add_doctor_name']
        gender = request.form['add_doctor_radio']
        qualification = request.form['add_doctor_qualification']
        experience = request.form['add_doctor_experience']
        image = request.files['add_doctor_image']
        image.save(
            'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\' + image.filename)
        path = '/static/disease_images/'+image.filename
        place = request.form['add_doctor_place']
        post = request.form['add_doctor_post']
        pin = request.form['add_doctor_pin']
        email = request.form['add_doctor_email']
        contact = request.form['add_doctor_contact']
        qry1 = "INSERT INTO login(username,PASSWORD,usertype)VALUES('" + \
            email+"','"+contact+"','doctor')"
        res = i.insert(qry1)
        qry = "INSERT INTO doctor(NAME,gender,qualification,experience,image,place,post,pin,email,contact,login_id)VALUES('"+name+"','" + \
            gender+"','"+qualification+"','"+experience+"','"+path+"','" + \
            place+"','"+post+"','"+pin+"','"+email + \
            "','"+contact+"','"+str(res)+"')"

        ans = i.insert(qry)
        return adm_add_doctor()
    else:
        return redirect(url_for('adm_login'))

    #*******viewdoctor begins*************#


@app.route('/adm_view_doctor', methods=['get'])
def adm_view_doctor():
    if session['alid'] == "1":
        v = Db()
        qry = "SELECT * FROM doctor"
        res = v.select(qry)
        print(res)
        return render_template('/admin/view_doctor.html', val=res)
    else:
        return redirect(url_for('adm_login'))

    #doctor_search_section_starts#


@app.route('/adm_view_doctor_post', methods=['post'])
def adm_view_doctor_post():
    if session['alid'] == "1":
        v = Db()
        name = request.form['doctor_search_name']
        qry = "SELECT * FROM doctor WHERE NAME LIKE '%"+name+"%'"
        res = v.select(qry)
        print(res)
        return render_template('/admin/view_doctor.html', val=res)
    else:
        return redirect(url_for('adm_login'))

    #doctor_search_section_ends#
    #********viewdoctor ends****************#

    #********edit doctor begins*************#


@app.route('/adm_edit_doctor/<doctor_id>')
def adm_edit_doctor(doctor_id):
    if session['alid'] == "1":
        e = Db()
        session['doctor_id'] = doctor_id
        qry = "SELECT * FROM doctor WHERE doctor_id='" + doctor_id + "'"
        ans = e.selectOne(qry)
        print(ans)
        return render_template('/admin/edit_doctor.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


@app.route('/adm_edit_doctor_post', methods=['post'])
def adm_edit_doctor_post():
    if session['alid'] == "1":
        e = Db()
        name = request.form['edit_doctor_name']
        gender = request.form['edit_doctor_gender']
        qualification = request.form['edit_doctor_qualification']
        experience = request.form['edit_doctor_experience']

        place = request.form['edit_doctor_place']
        post = request.form['edit_doctor_post']
        pin = request.form['edit_doctor_pin']
        email = request.form['edit_doctor_email']
        contact = request.form['edit_doctor_contact']
        if "edit_doctor_image" in request.files:
            image = request.files['edit_doctor_image']
            if image.filename != "":
                image.save(
                    'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\' + image.filename)
                path = '/static/disease_images/'+image.filename
                qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',image='"+path + \
                    "',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email + \
                    "',contact='"+contact+"' WHERE doctor_id='" + \
                    str(session['doctor_id'])+"'"
                res = e.update(qry)
            else:
                qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',place='" + \
                    place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',contact='" + \
                    contact+"' WHERE doctor_id='"+str(session['doctor_id'])+"'"
                res = e.update(qry)
        else:
            qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email + \
                "',contact='"+contact+"' WHERE doctor_id='" + \
                str(session['doctor_id'])+"'"
            res = e.update(qry)
        return adm_view_doctor()
    else:
        return redirect(url_for('adm_login'))

    #*******-edit doctor ends-****************#

    #********delete doctor begins-************#


@app.route('/adm_delete_doctor/<doctor_id>')
def adm_delete_doctor(doctor_id):
    if session['alid'] == "1":
        d = Db()
        qry = "DELETE FROM doctor WHERE doctor_id='" + doctor_id + "'"
        res = d.delete(qry)
        return adm_view_doctor()
    else:
        return redirect(url_for('adm_login'))

    #*********delete doctor ends**************#
#--------------add-doctor--and--view-doctor ends---------------------------------------------------------------------------------------------------------#

#--------------admin route-begins------------------------------------------------------------------------------------------------------------------------------#


@app.route("/adm_admin")
def adm_admin():
    if session['alid'] == "1":
        return render_template('/admin/Admin.html')
    else:
        return redirect(url_for('adm_login'))

#--------------admin route-ends-------------------------------------------------------------------------------------------------#


#---------------login------------------------------------------------------------------------------------------------------#


@app.route("/adm_login")
def adm_login():
    return render_template('/login.html')


@app.route("/adm_login_post", methods=['post'])
def adm_login_post():
    i = Db()
    error = None
    username = request.form['login_name']
    password = request.form['login_password']
    qry = "SELECT * FROM login WHERE username='" + \
        username+"' AND PASSWORD='"+password+"'"
    ans = i.selectOne(qry)
    if ans is not None:
        type = ans['usertype']
        session["lid"] = ans["login_id"]

        if type == 'admin':
            session['alid'] = "1"
            # return render_template('/admin/Admin.html')

            return render_template('/admin/index.html')

        elif type == 'doctor':
            session['alid'] = "2"
            return render_template('/doctor/home.html')
        else:
            error = 'Invalid credentials'
            return render_template('/login.html', error=error)
            # return "<script>alert('Invalid Username or Password');window.location='/'</script>"
    else:
        error = 'Invalid credentials'
        return render_template('/login.html', error=error)


#---------------login ends--------------------------------------#

#--------------------feedback-begins----------------------------#


@app.route('/adm_view_feedback')
def adm_view_feedback():
    if session['alid'] == "1":
        v = Db()
        qry = "SELECT feedback.*,user.* FROM USER,feedback WHERE feedback.user_id = user.login_id"
        ans = v.select(qry)

        return render_template('/admin/view_feedback.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


#---------------------feedback-ends----------------------------#

#--------------------user-begins-------------------------------#


@app.route('/adm_view_user')
def adm_view_user():
    if session['alid'] == "1":
        v = Db()
        qry = "SELECT * FROM USER"
        ans = v.select(qry)

        return render_template('/admin/view_user.html', val=ans)
    else:
        return redirect(url_for('adm_login'))

    #*******user_search_section_starts******#


@app.route('/adm_view_user_post', methods=['post'])
def adm_view_user_post():
    if session['alid'] == "1":
        v = Db()
        name = request.form['user_search_name']
        qry = "SELECT * FROM user WHERE NAME LIKE '%"+name+"%'"
        res = v.select(qry)

        return render_template('/admin/view_user.html', val=res)
    else:
        return redirect(url_for('adm_login'))

    #*******user_search_section_ends******#

#------------------------user-ends-----------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
    #Admin Ends#
# -------------------------------------------------------------------------------------------------------------------------------#


# -------------------------------------------------------------------------------------------------------------------------------#
    # Doctor Begins#             /\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/
# -------------------------------------------------------------------------------------------------------------------------------#

# -----------------------------------doctor-view-disease-section-begins----------------------------------------------------------------#
@app.route('/doctor_view_disease')
def doctor_view_disease():
    if session['alid'] == "2":
        v = Db()
        qry = "SELECT * FROM disease"
        res = v.select(qry)
        return render_template('/doctor/doctor_view_disease.html', val=res)
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_view_disease_post', methods=['post'])
def doctor_view_disease_post():
    if session['alid'] == "2":
        s = Db()
        search_disease = request.form['disease_search_name']
        qry = "SELECT * FROM disease WHERE NAME LIKE '%"+search_disease+"%'"
        ans = s.select(qry)
        return render_template('/doctor/doctor_view_disease.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


# -----------------------------------doctor-view-disease-section-ends----------------------------------------------------------------#

# schedule section begins--------------------------------------------------------------------------------------------------------------

# adding schedule by doctor begins


@app.route('/doctor_schedule_management')
def doctor_schedule_management():
    if session['alid'] == "2":
        return render_template('/doctor/doctor_schedule_management.html')
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_schedule_management_post', methods=['post'])
def doctor_schedule_management_post():
    if session['alid'] == "2":
        i = Db()
        from_time = request.form['from_time']
        to_time = request.form['to_time']
        date = request.form['date']
        qry = "INSERT INTO SCHEDULE(DATE,from_time,to_time,doctor_id)VALUES('"+date+"','" + \
            from_time+"','"+to_time+"','"+str(session['lid'])+"')"
        ans = i.insert(qry)
        print(ans)
        return doctor_schedule_management()
    else:
        return redirect(url_for('adm_login'))

# adding schedule by doctor begins


@app.route('/doctor_view_schedule')
def doctor_view_schedule():
    if session['alid'] == "2":
        v = Db()
        qry = "SELECT * FROM SCHEDULE WHERE doctor_id='" + \
            str(session['lid'])+"'"
        ans = v.select(qry)
        print(ans)
        return render_template('/doctor/doctor_view_schedule.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_view_schedule_post', methods=['post'])
def doctor_view_schedule_post():
    if session['alid'] == "2":
        s = Db()
        from_date = request.form['search_from_date']
        to_date = request.form['search_to_date']
        # qry = "SELECT * FROM schedule WHERE date LIKE '%" + \
        #     search_date+"%' AND doctor_id='"+str(session['lid'])+"'"
        qry = "SELECT * FROM SCHEDULE WHERE DATE BETWEEN '"+from_date + \
            "' AND '"+to_date+"' AND doctor_id='"+str(session['lid'])+"'"
        ans = s.select(qry)
        return render_template('/doctor/doctor_view_schedule.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_edit_schedule/<schedule_id>')
def doctor_edit_schedule(schedule_id):
    if session['alid'] == "2":
        e = Db()
        session['schedule_id'] = schedule_id
        qry = "SELECT * FROM SCHEDULE WHERE schedule_id='" + schedule_id + "'"
        ans = e.selectOne(qry)
        print('---------------------')
        print(ans)
        return render_template('/doctor/doctor_edit_schedule.html', val=ans)
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_edit_schedule_post', methods=['post'])
def doctor_edit_schedule_post():
    if session['alid'] == "2":
        e = Db()
        from_time = request.form['from_time']
        to_time = request.form['to_time']
        date = request.form['date']
        qry = "UPDATE SCHEDULE SET from_time='"+from_time+"' ,to_time='"+to_time + \
            "',DATE='"+date+"' WHERE schedule_id='" + \
            str(session['schedule_id'])+"'"
        ans = e.update(qry)
        return doctor_view_schedule()
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_delete_schedule/<schedule_id>')
def doctor_delete_schedule(schedule_id):
    if session['alid'] == "2":
        d = Db()

        qry = "DELETE FROM SCHEDULE WHERE schedule_id='"+schedule_id+"'"

        res = d.delete(qry)
        return doctor_view_schedule()
    else:
        return redirect(url_for('adm_login'))


# schedule section ends--------------------------------------------------------------------------------------------------------------


# doctor-view-profile-section begins--------------------------------------------------------------------------------------------------------------

@app.route('/doctor_view_profile')
def doctor_view_profile():
    if session['alid'] == "2":
        v = Db()

        qry = "SELECT * FROM doctor where login_id='"+str(session["lid"])+"'"
        res = v.selectOne(qry)

        return render_template('/doctor/doctor_view_profile.html', val=res)
    else:
        return redirect(url_for('adm_login'))


#*********doctor-edit-profile-begins*****#


@app.route('/doctor_view_profile_post', methods=['post'])
def doctor_view_profile_post():
    if session['alid'] == "2":
        e = Db()
        lid = session['lid']
        name = request.form['edit_doctor_name']
        gender = request.form['edit_doctor_gender']
        qualification = request.form['edit_doctor_qualification']
        experience = request.form['edit_doctor_experience']

        place = request.form['edit_doctor_place']
        post = request.form['edit_doctor_post']
        pin = request.form['edit_doctor_pin']
        email = request.form['edit_doctor_email']
        contact = request.form['edit_doctor_contact']
        if "edit_doctor_image" in request.files:
            print("S")
            image = request.files['edit_doctor_image']
            if image.filename != "":
                image.save(
                    'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\' + image.filename)
                path = '/static/disease_images/'+image.filename
                qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',image='"+path + \
                    "',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email + \
                    "',contact='"+contact+"' WHERE login_id='" + \
                    str(lid)+"'"
                res = e.update(qry)
            else:
                qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',place='" + \
                    place+"',post='"+post+"',pin='"+pin+"',email='"+email+"',contact='" + \
                    contact+"' WHERE login_id='"+str(lid)+"'"
                res = e.update(qry)
        else:
            qry = "UPDATE doctor SET NAME='"+name+"',gender='"+gender+"',qualification='"+qualification+"',experience='"+experience+"',place='"+place+"',post='"+post+"',pin='"+pin+"',email='"+email + \
                "',contact='"+contact+"' WHERE login_id='" + \
                str(lid)+"'"
            res = e.update(qry)
            # print(res)
        return doctor_view_profile()
    else:
        return redirect(url_for('adm_login'))

    #*********doctor-edit-profile-begins*****#

# doctor-view-profile-section ends--------------------------------------------------------------------------------------------------------------

# doctor-view-user-section begins--------------------------------------------------------------------------------------------------------------


@app.route('/doctor_view_user')
def doctor_view_user():
    if session['alid'] == "2":
        v = Db()
        qry = "SELECT * FROM user"
        ans = v.select(qry)
        print(ans)
        return render_template('/doctor/doctor_view_user.html', val=ans)

    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_view_user_post', methods=['post'])
def doctor_view_user_post():
    if session['alid'] == "2":
        v = Db()
        name = request.form['user_search_name']
        qry = "SELECT * FROM user WHERE NAME LIKE '%" + \
            name+"%' "
        res = v.select(qry)
        print(res)
        return render_template('/doctor/doctor_view_user.html', val=res)

    else:
        return redirect(url_for('adm_login'))

# doctor-view-user-section ends--------------------------------------------------------------------------------------------------------------

# doctor-change_password-section begins--------------------------------------------------------------------------------------------------------------


@app.route('/doctor_change_password')
def doctor_change_password():
    if session['alid'] == "2":
        return render_template('/doctor/doctor_change_password.html')

    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_change_password_post', methods=['post'])
def doctor_change_password_post():
    if session['alid'] == "2":
        v = Db()
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        qry = "SELECT * FROM login WHERE login_id='"+str(session['lid'])+"'"
        ans = v.selectOne(qry)
        print(qry)
        if ans['password'] == current_password:
            if confirm_password == new_password:
                qry = "UPDATE login SET PASSWORD='"+new_password + \
                    "' where login_id='"+str(session['lid'])+"'"
                res = v.update(qry)
                return render_template('/login.html')
            else:
                print('cpass and new pass not same')
                return render_template('/doctor/doctor_change_password.html')

        else:
            print('Invalid')
            return render_template('/doctor/doctor_change_password.html')

    else:
        return redirect(url_for('adm_login'))


@app.route('/logout')
def logout():
    session['alid'] = "0"
    return render_template('login.html')


# doctor-change_password-section ends--------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------#
    # Doctor Ends#               /\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/
# -------------------------------------------------------------------------------------------------------------------------------#


@app.route("/doctor_chat/<id>/<name>")
def doctor_chat(id, name):
    session['toid'] = id
    from_id = str(session["lid"])
    session["name"] = name
    return render_template("doctor/chat.html", toid=id, fid=from_id)


# refresh messages chatlist
@app.route("/emp_chat_chk", methods=['post'])
def emp_chat_chk():
    uid = str(session["toid"])
    qry = "select date,time,message,from_id from chat where (from_id='" + str(
        session['lid']) + "' and to_id='" + uid + "') or ((from_id='" + uid + "' and to_id='" + str(
        session['lid']) + "')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    print(res)
    return jsonify(res)


@app.route("/emp_chat_post", methods=['POST'])
def emp_chat_post():
    id = str(session["toid"])
    ta = request.form["ta"]
    qry = "insert into chat(date,time,message,from_id,to_id) values(CURDATE(),CURTIME(),'" + \
        ta+"','"+str(session['lid'])+"','"+id+"')"
    d = Db()
    d.insert(qry)
    # return jsonify(res)
    return render_template('doctor/chat.html', toid=id)


# @app.route("/emp_chat_p/<msg>")
# def emp_chat_p(msg):
#     id = str(session["toid"])
#     ta = msg
#     qry = "insert into chat(date,time,message,from_id,to_id) values(CURDATE(),CURTIME(),'" + \
#         ta+"','"+str(session['lid'])+"','"+id+"')"
#     print(qry)
#     d = Db()
#     d.insert(qry)
#     qry = "select DATE_FORMAT(date,'%d%m%y') as date,time,message,from_id from chat where (from_id='" + str(
#         session['lid']) + "' and to_id='" + id + "') or ((from_id='" + id + "' and to_id='" + str(
#         session['lid']) + "')) order by chat_id desc"
#     c = Db()
#     res = c.select(qry)
#     print(res)
#     # return jsonify(res)
#     # return render_template('doctor/chat.html', toid=id)
#     return jsonify(status="ok")

# login page


@app.route('/')
def login_page():
    return render_template("index.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('/admin/dashboard.html')


@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('/doctor/doctor-dashboard.html')

# Landing Page


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/profile_new')
def profile_new():
    return render_template('/doctor/profile-new.html')

# ---------login-temp-anim-codepen


# @app.route('/anim_log')
# def anim_log():
#     return render_template('login-anim.html')
# user

@app.route('/user_login', methods=['post'])
def user_login():
    i = Db()
    username = request.form['username']
    password = request.form['password']
    qry = "SELECT * FROM login WHERE username='" + \
        username+"' AND PASSWORD='"+password+"'"
    ans = i.selectOne(qry)
    if ans is not None:
        type = ans['usertype']
        if type == "user":
            qry1 = "select * from user where login_id = '" + \
                str(ans['login_id'])+"'"
            res = i.selectOne(qry1)
            return jsonify(status="ok", name=res['name'], image=res['image'], lid=ans['login_id'], type=ans['usertype'])
        else:
            return jsonify(status="no")
    else:
        return jsonify(status="no")


@app.route('/user_view_profile', methods=['post'])
def user_view_profile():
    v = Db()
    login_id = request.form['loginId']
    qry = "select DATE_FORMAT(date_of_birth,'%d-%m-%y') as date_of_birth,name,gender,image,place,post,pin,email,contact from user where login_id ='"+login_id+"'"
    ans = v.selectOne(qry)

    ans = v.selectOne(qry)
    if ans is not None:
        return jsonify(status="ok", name=ans['name'], gender=ans['gender'], date_of_birth=ans['date_of_birth'], image=ans['image'], place=ans['place'], post=ans['post'], pin=ans['pin'], email=ans['email'], contact=ans['contact'])
    else:
        return jsonify(status="no")


@app.route('/user_view_doctorSchedule', methods=['post'])
def user_view_doctorSchedule():
    v = Db()
    login_id = request.form['login_id']
    qry = "select * from doctor where doctor_id='"+login_id+"'"
    ans = v.selectOne(qry)

    if ans is not None:
        return jsonify(status="ok", name=ans['name'], gender=ans['gender'], qualification=ans['qualification'], experience=ans['experience'], image=ans['image'], place=ans['place'], post=ans['post'], pin=ans['pin'], email=ans['email'], contact=ans['contact'], users=data)
    else:
        return jsonify(status="no")


@app.route('/user_view_doctors', methods=['post'])
def user_view_doctors():
    v = Db()

    qry = "select * from doctor"
    ans = v.select(qry)
    # print(ans)
    return jsonify(status="ok", data=ans)


@app.route('/user_register', methods=['post'])
def user_register():
    i = Db()
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    image = request.form['img']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    email = request.form['email']
    phone = request.form['phone']

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(image)
    fh = open("C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\user_images\\" + timestr + ".jpg", "wb")
    path = "/static/user_images/" + timestr + ".jpg"
    fh.write(a)
    fh.close()

    qry1 = "INSERT INTO login(username,PASSWORD,usertype)VALUES('" + \
        email+"','"+phone+"','user')"
    ans1 = i.insert(qry1)
    qry = "INSERT INTO USER(NAME,gender,date_of_birth,image,place,post,pin,email,contact,login_id)VALUES('" + name+"','"+gender+"','"+dob+"','"+path+"','"+place+"','" + \
        post+"','"+pin+"','"+email+"','"+phone+"','"+str(ans1)+"')"

    ans = i.insert(qry)
    return jsonify(status="ok",)


@app.route('/user_UploadImage', methods=['post'])
def upload_Image():
    i = Db()
    image = request.form['diseaseImage']
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print("=================okkkkkkkkk")

    a = base64.b64decode(image)
    fh = open("C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\userDisease_Images\\" + timestr + ".jpg", "wb")
    path = "/static/userDisease_Images/" + timestr + ".jpg"
    fh.write(a)
    fh.close()

    return jsonify(status="ok")


@app.route('/view_doctorMore', methods=["post"])
def view_doctorMore():
    i = Db()
    lid = request.form['lid']
    qry = "select * from doctor where login_id='"+lid+"'"
    ans = i.selectOne(qry)
    qry1 = "SELECT DATE_FORMAT(date,'%d-%m-%y') as date,from_time,to_time,doctor_id,schedule_id FROM schedule WHERE doctor_id='" + \
        lid+"' AND date>= CURDATE()"
    data = i.select(qry1)
    print(data)
    return jsonify(status="ok", name=ans['name'], gender=ans['gender'], qualification=ans['qualification'], experience=ans['experience'], image=ans['image'], place=ans['place'], post=ans['post'], email=ans['email'], pin=ans['pin'], contact=ans['contact'], users=data)


@app.route('/in_message', methods=['POST'])
def message():
    c = Db()
    fr_id = request.form["fid"]
    to_id = request.form["toid"]
    message = request.form["msg"]
    print("------------------------------------------------"+message)
    query7 = "INSERT INTO chat(from_id,to_id,message,date,time) VALUES ('" + \
        fr_id + "' ,'" + to_id + "','" + message + "',CURDATE(),CURTIME())"
    print(query7)
    m = c.insert(query7)
    if m == 1:
        return jsonify(status='send')
    else:
        return jsonify(status='failed')


@app.route('/view_message2', methods=['POST'])
def msg():
    fid = request.form["fid"]
    toid = request.form["toid"]
    lmid = request.form['lastmsgid']
    query = "SELECT from_id,message,date,chat_id FROM chat WHERE chat_id>'"+lmid + \
        "' AND ((to_id='"+toid+"' AND  from_id='"+fid+"') OR (to_id='" + \
        fid+"' AND from_id='"+toid+"')  )  ORDER BY chat_id ASC"
    c = Db()
    res = c.select(query)
    return jsonify(status='ok', res1=res)


@app.route('/user_SendFeedback', methods=['post'])
def user_SendFeedback():
    i = Db()
    feedback = request.form['feedback']
    lid = request.form['loginId']
    qry = "insert into feedback(feedback,user_id,date)values('" + \
        feedback+"','"+lid+"',curdate())"
    ans = i.insert(qry)
    return jsonify(status="ok")


@app.route('/user_bookdoctor', methods=['post'])
def user_bookdoctor():
    i = Db()
    doc_id = request.form['doc_id']
    lid = request.form['loginId']
    sch_id = request.form['schedule_id']
    # qry = "insert into feedback(feedback,user_id,date)values('" + \ feedback+"','"+lid+"',curdate())"
    # ans = i.insert(qry)
    return jsonify(status="ok")


@app.route('/user_bookSchedule', methods=['post'])
def user_bookSchedule():
    i = Db()
    schedule_id = request.form['schedule_id']
    user_id = request.form['user_id']
    qry = "INSERT INTO book(schedule_id,user_id,STATUS)VALUES('" + \
        schedule_id+"','"+user_id+"','ok')"
    res = i.insert(qry)
    return jsonify(status="ok")


@app.route('/user_viewBookSchedule', methods=['post'])
def user_viewBookSchedule():
    i = Db()
    qry = "select * from book"
    res = i.insert(qry)
    return jsonify(status="ok")


@app.route('/userviewmyshedule', methods=['post'])
def userviewmyshedule():
    i = Db()
    lid = request.form['lid']
    timestr = time.strftime("%d-%m-%Y")
    qry = "SELECT `book`.*,`schedule`.*,`doctor`.`name`,`doctor`.`qualification` FROM `doctor`,`schedule`,`book`,USER WHERE `book`.`schedule_id`=`schedule`.`schedule_id` AND `book`.`user_id`=`user`.`login_id` AND `user`.`login_id`='" + \
        lid+"''' AND `schedule`.`doctor_id`=`doctor`.`login_id` ORDER BY `book`.`book_id` desc"
    res = i.select(qry)
    # print('--------------------------')
    # print(res)
    return jsonify(status="ok", data=res)


@app.route('/userBookCancel', methods=['post'])
def userBookCancel():
    i = Db()
    bid = request.form['bid']
    qry = "delete from book  where book_id = '"+bid+"'"
    res = i.delete(qry)
    return jsonify(status="ok")


@app.route('/user_view_profile1', methods=['post'])
def user_view_profile1():
    v = Db()
    login_id = request.form['loginId']
    qry = "select DATE_FORMAT(date_of_birth,'%d-%m-%y') as date_of_birth, name,gender,image,place,post,pin,email,contact from user where login_id ='"+login_id+"'"
    ans = v.selectOne(qry)
    print(ans)
    if ans is not None:
        return jsonify(status="ok", name=ans['name'], gender=ans['gender'], date_of_birth=ans['date_of_birth'], image=ans['image'], place=ans['place'], post=ans['post'], pin=ans['pin'], email=ans['email'], contact=ans['contact'])
    else:
        return jsonify(status="no")

# DATE_FORMAT(date_of_birth,'%d%m%y')
# DATA_FORMAT(date,'%d%m%y') as date

# --------------


@app.route('/user_p_Page', methods=['post'])
def user_p_Page():
    v = Db()
    login_id = request.form['loginId']
    qry = "select * from user where login_id ='"+login_id+"'"
    ans = v.selectOne(qry)
    if ans is not None:
        return jsonify(status="ok", name=ans['name'], gender=ans['gender'], date_of_birth=ans['date_of_birth'], image=ans['image'], place=ans['place'], post=ans['post'], pin=ans['pin'], contact=ans['contact'], email=ans['email'])
    else:
        return jsonify(status="no")


@app.route('/user_update_profile', methods=['post'])
def user_update_profile():
    i = Db()
    p_Name = request.form['name']
    p_Gen = request.form['gender']
    p_DOB = request.form['dob']

    p_Place = request.form['place']
    p_Post = request.form['post']
    p_Pin = request.form['pin']
    p_Contact = request.form['phone']
    image = request.form['img']
    lid = request.form['login_id']
    if image == "aa":
        qry = "update user set name = '"+p_Name+"',gender ='"+p_Gen+"',date_of_birth='"+p_DOB + \
            "',place='"+p_Place+"',post='" + \
            p_Post+"',pin='"+p_Pin+"',contact='"+p_Contact+"' where login_id='"+lid+"'"
        ans = i.update(qry)
        print('----------------')
        print(ans)
        return jsonify(status="ok")
    else:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        print(timestr)
        a = base64.b64decode(image)
        fh = open("C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\user_images\\" + timestr + ".jpg", "wb")
        path = "/static/user_images/" + timestr + ".jpg"
        fh.write(a)
        fh.close()

        qry = "update user set name = '"+p_Name+"',gender ='"+p_Gen+"',date_of_birth='"+p_DOB + \
            "',image='"+path+"',place='"+p_Place+"',post='" + \
            p_Post+"',pin='"+p_Pin+"',contact='"+p_Contact+"' where login_id='"+lid+"'"
        ans = i.update(qry)
        print('----------------')
        print(ans)
        return jsonify(status="ok")


@app.route('/data_train')
def data_train():
    print("Data-----------")
    import numpy as np
    from skimage import io, color, img_as_ubyte

    from skimage.feature import greycomatrix, greycoprops
    from sklearn.metrics.cluster import entropy
    # img = cv2.imread(path)
    # aa = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
    #       'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']
    aa = ['athelets_foot', 'atopic_dermatisis_on_hand', 'black_mole', 'chicken_pox',
          'cracked_heels', 'facial_acne', 'normal_skin_body', 'normal_skin_face', 'normal_skin_hand', 'normal_skin_leg']
    for i in aa:
        print(i)
    # search = str(input('Enter the folder name'))
    # path = 'C:\\Users\\rsmp\\Desktop\\dataset\\train\\' + search
    # a = os.listdir(path)
    # b = str(a)
    # print(b)
    alllist = []

    features = []
    labels = []

    # ===========================================================

    for myfolders in aa:
        path = 'C:\\Users\\rsmp\\Desktop\\dataSet_New\\train\\' + \
            str(myfolders)

        # path = 'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\dataset_train_backup\\datasetBackup-17-01-22\\train\\' + \
        #     str(myfolders)
        a = os.listdir(path)
        for ii in a:
            rgbImg = io.imread(str(path+"\\"+str(ii)))
            grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

            distances = [1, 2, 3]
            angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
            properties = ['energy', 'homogeneity',
                          'dissimilarity', 'correlation', 'contrast']

            glcm = greycomatrix(grayImg,
                                distances=distances,
                                angles=angles,
                                symmetric=True,
                                normed=True)

            feats = np.hstack([greycoprops(glcm, 'homogeneity').ravel()
                              for prop in properties])
            feats1 = np.hstack([greycoprops(glcm, 'energy').ravel()
                               for prop in properties])
            feats2 = np.hstack(
                [greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
            feats3 = np.hstack(
                [greycoprops(glcm, 'correlation').ravel() for prop in properties])
            feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel()
                               for prop in properties])

            k = np.mean(feats)
            l = np.mean(feats1)
            m = np.mean(feats2)
            n = np.mean(feats3)
            o = np.mean(feats4)
            # print(k)
            # print(l)
            # print(m)
            # print(n)
            # print(o)

            features.append([k, l, m, n, o])
            labels.append(myfolders)
            disease = myfolders
            # print(disease)
            aa = [k, l, m, n, o, disease]
            alllist.append(aa)
            data = pd.DataFrame(
                alllist, columns=['f1', 'f2', 'f3', 'f4', 'f5', 'Disease'])

            data.to_csv(
                'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\dataSet1.csv')

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.1, random_state=0)

    from sklearn.ensemble import RandomForestClassifier
    a = RandomForestClassifier(n_estimators=100)

    a.fit(features, labels)

    m = a.predict(X_test)

    from sklearn.metrics import accuracy_score

    s = accuracy_score(y_test, m)

    print(s, "acccuracy")

    return disease


@app.route('/testing')
def testing():
    import numpy as np
    from skimage import io, color, img_as_ubyte

    from skimage.feature import greycomatrix, greycoprops
    from sklearn.metrics.cluster import entropy
    path = 'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\aa.jpg'

    rgbImg = io.imread(path)
    grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

    distances = [1, 2, 3]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['energy', 'homogeneity',
                  'dissimilarity', 'correlation', 'contrast']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)

    feats = np.hstack([greycoprops(glcm, 'homogeneity').ravel()
                       for prop in properties])
    feats1 = np.hstack([greycoprops(glcm, 'energy').ravel()
                        for prop in properties])
    feats2 = np.hstack(
        [greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
    feats3 = np.hstack(
        [greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel()
                        for prop in properties])

    k = np.mean(feats)
    l = np.mean(feats1)
    m = np.mean(feats2)
    n = np.mean(feats3)
    o = np.mean(feats4)
    print(k)
    print(l)
    print(m)
    print(n)
    print(o)

    aa = [k, l, m, n, o]

    df = pd.read_csv('dataSet.csv')
    attributes = df.values[:, 0:5]
    print(len(attributes))
    label = df.values[:, 6]
    print(len(label))
    str(df)
    # for i in df:
    #     print(i)
    # b = str(df)
    print(attributes)
    print(label)
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        attributes, label, test_size=0.1, random_state=42)

    from sklearn.ensemble import RandomForestClassifier
    a = RandomForestClassifier(n_estimators=100)

    a.fit(X_train, y_train)

    predictedresult = a.predict([aa])
    print(predictedresult)
    print("ppp")
    # actualresult = y_test
    # testdata = X_test

    # l = len(testdata)

    # from sklearn.metrics import accuracy_score

    # sc = accuracy_score(actualresult, predictedresult)

    # print(sc)
    return str(predictedresult[0])

# --------------------------


@app.route('/doctor_Detect_Disease')
def doctor_Detect_Disease():
    if session['alid'] == "2":
        return render_template('/doctor/doctor_detect.html')
    else:
        return redirect(url_for('adm_login'))


@app.route('/doctor_Detect_Disease_post', methods=['post'])
def doctor_Detect_Disease_post():
    import numpy as np
    from skimage import io, color, img_as_ubyte

    from skimage.feature import greycomatrix, greycoprops
    from sklearn.metrics.cluster import entropy

    image = request.files['upload_Detect_Image']
    image.save('C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\static\\testImage\\'+image.filename)
    path = 'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\testImage\\'+image.filename

    rgbImg = io.imread(path)
    grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

    distances = [1, 2, 3]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['energy', 'homogeneity',
                  'dissimilarity', 'correlation', 'contrast']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)

    feats = np.hstack([greycoprops(glcm, 'homogeneity').ravel()
                       for prop in properties])
    feats1 = np.hstack([greycoprops(glcm, 'energy').ravel()
                        for prop in properties])
    feats2 = np.hstack(
        [greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
    feats3 = np.hstack(
        [greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel()
                        for prop in properties])

    k = np.mean(feats)
    l = np.mean(feats1)
    m = np.mean(feats2)
    n = np.mean(feats3)
    o = np.mean(feats4)
    print(k)
    print(l)
    print(m)
    print(n)
    print(o)

    aa = [k, l, m, n, o]
    # aa = [0.23373460057159642, 0.020627420771578593,
    #       5.61478747481891, 0.989042781659751, 93.16512844374235]

    # df = pd.read_csv(
    #     'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\dataSet1.csv')
    # attributes = df.values[:, 1:6]
    # print(attributes)
    # # print(len(attributes))
    # label = df.values[:, 6]
    # print(label)
    # # print(len(label))
    # str(df)

    # # print(attributes)
    # # print(label)

    # from sklearn.ensemble import RandomForestClassifier
    # a = RandomForestClassifier()

    # a.fit(attributes, label)

    predictedresult = a.predict([aa])
    res = str(predictedresult)[1:-1]
    print(res)
    if res == 'normal_skin_body' or res == 'normal_skin_face' or res == 'normal_skin_hand' or res == 'normal_skin_leg':
        res1 = "normal skin conditions no ubnormalities detected"
        print(res1)
    else:
        print("skin conditions ubnormalities")
    res = res.replace("'", "")
    res1 = res.replace('_', " ")
    qry = "select * from disease where name='"+res1+"'"
    i = Db()
    ans = i.selectOne(qry)
    print('---------------------')
    print(ans)
    print(msg)
    # return str(predictedresult[0])
    return render_template('/doctor/doctor_detect.html', res=res1)


df = pd.read_csv(
    'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\dataSet1.csv')
attributes = df.values[:, 1:6]
# print(attributes)
# print(len(attributes))
label = df.values[:, 6]
# print(label)
# print(len(label))
# str(df)

# print(attributes)
# print(label)

a = RandomForestClassifier()

a.fit(attributes, label)


@app.route('/user_Detect_Disease_post', methods=['post'])
def user_Detect_Disease_post():
    import numpy as np
    from skimage import io, color, img_as_ubyte

    from skimage.feature import greycomatrix, greycoprops
    from sklearn.metrics.cluster import entropy
    i = Db()

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)

    image = request.files['upload_Detect_Image']
    image.save('C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\static\\userDisease_Images\\'+timestr+".jpg")
    path = 'C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\userDisease_Images\\'+timestr+".jpg"

    rgbImg = io.imread(path)
    grayImg = img_as_ubyte(color.rgb2gray(rgbImg))

    distances = [1, 2, 3]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['energy', 'homogeneity',
                  'dissimilarity', 'correlation', 'contrast']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)

    feats = np.hstack([greycoprops(glcm, 'homogeneity').ravel()
                       for prop in properties])
    feats1 = np.hstack([greycoprops(glcm, 'energy').ravel()
                        for prop in properties])
    feats2 = np.hstack(
        [greycoprops(glcm, 'dissimilarity').ravel() for prop in properties])
    feats3 = np.hstack(
        [greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'contrast').ravel()
                        for prop in properties])

    k = np.mean(feats)
    l = np.mean(feats1)
    m = np.mean(feats2)
    n = np.mean(feats3)
    o = np.mean(feats4)

    print(k, l, m, n, o)
    # print(l)
    # print(m)
    # print(n)
    # print(o)

    aa = [k, l, m, n, o]
    # aa = [0.23373460057159642, 0.020627420771578593,
    #       5.61478747481891, 0.989042781659751, 93.16512844374235]

    predictedresult = a.predict([aa])
    print(predictedresult)
    print("ppp")
    res = predictedresult
    # return str(predictedresult[0])

    qry = "select * from disease where name='"+res[0]+"'"
    print(qry)
    ans = i.selectOne(qry)

    print(ans)

    return jsonify(status="ok", name=ans['name'], image=ans['image'], descriptions=ans['descriptions'])


@app.route('/user_view_doctors_search', methods=['post'])
def user_view_doctors_search():

    s = request.form["s"]

    v = Db()

    qry = "select * from doctor where name like '%"+s+"%'"
    ans = v.select(qry)
    # print(ans)
    return jsonify(status="ok", data=ans)


@app.route('/user_Change_Password', methods=['post'])
def user_Change_Password():
    i = Db()

    lid = request.form['lid']
    confirmPass = request.form['confirm_password']
    qry = "update login set password='"+confirmPass+"' where login_id='"+lid+"'"
    ans = i.update(qry)
    return jsonify(status="ok")


# @app.route('/and_forgetpassword', methods=['post'])
# def forget_Password():
#     i = Db()
#     import random
#     # password = random.randint(1000, 10000)
#     email = request.form['email']
#     user = 'user'
#     qry = "select * from login where username='"+email+"' and usertype='"+user+"'"
#     print(qry)
#     ans = i.selectOne(qry)
#     print(ans)
#     if ans != None:

#         msg = Message(subject="Hello", sender='dermz3121@gmail.com', recipients=[email],
#                       body="  Your password for login is : "+str(ans["password"]))

#         mail.send(msg)
#         return jsonify(status="ok")

#     else:
#         return jsonify(status="not")
@app.route('/and_forgetpassword', methods=['post'])
def forget_Password():
    i = Db()
    lid = request.form['lid']
    import random
    password = random.randint(1000, 10000)
    pass1 = str(password)

    qry1 = "update login set password='"+pass1+"' where login_id='"+lid+"'"
    ans1 = i.insert(qry1)
    print(ans1)

    email = request.form['email']
    user = 'user'
    qry = "select * from login where username='"+email+"' and usertype='"+user+"'"
    print(qry)
    ans = i.selectOne(qry)
    print(ans)
    if ans != None:

        msg = Message(subject="Hello There", sender='dermz3121@gmail.com', recipients=[email],
                      body="  Your password for login is : "+str(ans["password"]))

        mail.send(msg)
        return jsonify(status="ok")

    else:
        return jsonify(status="not")


@app.route('/doctor_view_booked')
def doctor_view_booked():
    lid = session['lid']
    v = Db()
    qry = "SELECT schedule.*,book.*, user.* FROM book INNER JOIN USER ON book.user_id=user.login_id INNER JOIN SCHEDULE ON schedule.schedule_id=book.schedule_id WHERE schedule.doctor_id = '" + \
        str(lid)+"'"
    ans = v.select(qry)
    print(ans)
    # return ans
    return render_template('/doctor/doctor_view_booked.html', val=ans)


@app.route('/doctor_view_booked_post', methods=['post'])
def doctor_view_booked_post():
    if session['alid'] == "2":
        v = Db()
        name = request.form['user_search_name']
        qry = "SELECT * FROM user,schedule WHERE user.NAME LIKE '%" + \
            name+"%' "
        res = v.select(qry)

        return render_template('/doctor/doctor_view_booked.html', val=res)

    else:
        return redirect(url_for('adm_login'))


# @app.route('/doctor_forgetPassword')
# def doctor_forgetPassword():
#     return render_template('/doctor/doctor_forget_password.html')


# @app.route('/doctor_forgetPassword_post', methods=['post'])
# def doctor_forgetPassword_post():
#     i = Db()

#     import random
#     password = random.randint(1000, 10000)
#     pass1 = str(password)
#     if session['alid'] == "1":
#         forget_uname = request.form['forget_name']
#         qry2 = "select * from login where username='"+forget_uname+"'"
#         ans2 = i.select(qry2)

#         qry1 = "update login set password='"+pass1+"' where login_id='"+lid+"'"
#         ans1 = i.update(qry1)
#         print(ans1)

#         user = 'doctor'
#         qry = "select * from login where username='" + \
#             forget_uname+"' and usertype='"+user+"'"
#         print(qry)
#         ans = i.selectOne(qry)
#         print(ans)
#         if ans != None:
#             msg = Message(subject="Hello There", sender='dermz3121@gmail.com', recipients=[forget_uname],
#                           body="  Your password for login is : "+str(ans["password"]))

#             mail.send(msg)
#             return render_template('/doctor/doctor_forget_password.html')

#         else:
#             return "errror"

# ----------------------------------------------------------------------------


# @app.route('/doctor_forgetPassword_post', methods=['post'])
# def doctor_forgetPassword_post():
#     db= Db()
#     email=request.form['email']
#     qry="SELECT * FROM login WHERE username='"+email+"'"
#     res=db.selectOne(qry)
#     if res is not None:
#         type = res["type"]
#         log_id=str(res["log_id"])
#         password=res["password"]
#         if (type == "admin"):
#             name="admin"
#         elif type == "parent":
#             qry1="SELECT * FROM parents WHERE log_id='"+log_id+"'"
#             res1=db.selectOne(qry1)
#             name=res1["name"]
#         elif type == "teacher":
#             qry2="SELECT * FROM teachers WHERE log_id='"+log_id+"'"
#             res2=db.selectOne(qry2)
#             name=res2["name"]
#         else:
#             name=""
#         if name !="":
#             s = smtplib.SMTP(host='smtp.gmail.com', port=587)
#             s.starttls()
#             s.login("malabrkidslearning@gmail.com", "kids@malabar")
#             msg = MIMEMultipart()  # create a message.........."
#             message = "Messege from DNTL"
#             msg['From'] = "malabrkidslearning@gmail.com"
#             msg['To'] = email
#             msg['Subject'] = "Hai "+name+" Your Password For Kids Learning Web App"
#             body = "Your Account Password Reset Successfully. You Can login using This password - " + str(password)
#             msg.attach(MIMEText(body, 'plain'))
#             s.send_message(msg)
#             return '''<script>alert (" We have emailed your password ! ");window.location='/'</script>'''
#         else:
#              return '''<script>alert (" Invalid user ! ");window.location='/resetpassword'</script>'''

#     else:
#          return '''<script>alert (" Invalid user ! ");window.location='/resetpassword'</script>'''


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0', threaded=False)
