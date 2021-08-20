from flask import Flask, render_template, request, session
from DBConnection import Db
app = Flask(__name__)
app.secret_key = "abc"
# -------------------------------------------------------------------------------------------------------------------------------#
#Admin Begins#
# -------------------------------------------------------------------------------------------------------------------------------#
#--------------add-disease--and--view-disease--and--edit-disease---and-delete-disease-begins-----------------------------------------------------------------#


@app.route("/adm_add_disease")
def adm_add_disease():
    return render_template('/admin/add_disease.html')


@app.route("/adm_add_disease_post", methods=['post'])
def adm_add_disease_post():
    i = Db()
    name = request.form['add_disease_name']
    image = request.files['add_disease_image']
    image.save('C:\\Users\\rsmp\\Desktop\\Skin_Disease_Recognition_Project\\Skin-Disease-Recognition\\static\\disease_images\\'+image.filename)
    path = '/static/disease_images/'+image.filename
    description = request.form['add_disease_description']
    qry = "INSERT INTO disease(NAME,image,descriptions)VALUES('" + \
        name+"','"+path+"','"+description+"')"
    ans = i.insert(qry)
    return adm_view_disease()

    #**********view-disease-begins************#


@app.route('/adm_view_disease')
def adm_view_disease():
    v = Db()
    qry = "SELECT * FROM disease"
    res = v.select(qry)
    print(res)
    return render_template('/admin/view_disease.html', val=res)

    #disease_search_section_starts#


@app.route('/adm_view_disease_post', methods=['post'])
def adm_view_disease_post():
    v = Db()
    name = request.form['disease_search_name']
    qry = "SELECT * FROM disease WHERE NAME LIKE '%"+name+"%'"
    res = v.select(qry)
    print(res)
    return render_template('/admin/view_disease.html', val=res)
    #disease_search_section_ends#
    #***********view-disease-ends**************#

    #***********edit-disease-begins************#


@app.route('/adm_edit_disease/<disease_id>')
def adm_edit_disease(disease_id):
    e = Db()
    session['disease_id'] = disease_id
    qry = "SELECT * FROM disease WHERE disease_id='" + disease_id + "'"
    ans = e.selectOne(qry)
    print(ans)
    return render_template('/admin/edit_disease.html', val=ans)


@app.route('/adm_edit_disease_post', methods=['post'])
def adm_edit_disease_post():
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

    #***********edit-disease-ends**************#

    #***********delete-disease-begins**********#


@app.route('/adm_delete_disease/<disease_id>')
def delete_student(disease_id):
    d = Db()
    qry = "DELETE FROM disease WHERE disease_id='" + disease_id + "'"
    res = d.delete(qry)
    return adm_view_disease()

    #*******delete-disease-ends***************#


#--------------add-disease--and--view-disease--and--edit-disease--and --delete-disease ends---------------------------------------------------------------#

#--------------add-doctor--and--view-doctor--and--edit-doctor--and --delete-doctor begins-----------------------------------------------------------------#

@app.route("/adm_add_doctor")
def adm_add_doctor():
    return render_template('/admin/add_doctor.html')


@app.route("/adm_add_doctor_post", methods=['post'])
def adm_add_doctor_post():
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
    return adm_view_doctor()

    #*******viewdoctor begins*************#


@app.route('/adm_view_doctor', methods=['get'])
def adm_view_doctor():
    v = Db()
    qry = "SELECT * FROM doctor"
    res = v.select(qry)
    print(res)
    return render_template('/admin/view_doctor.html', val=res)

    #doctor_search_section_starts#


@app.route('/adm_view_doctor_post', methods=['post'])
def adm_view_doctor_post():
    v = Db()
    name = request.form['doctor_search_name']
    qry = "SELECT * FROM doctor WHERE NAME LIKE '%"+name+"%'"
    res = v.select(qry)
    print(res)
    return render_template('/admin/view_doctor.html', val=res)
    #doctor_search_section_ends#
    #********viewdoctor ends****************#

    #********edit doctor begins*************#


@app.route('/adm_edit_doctor/<doctor_id>')
def adm_edit_doctor(doctor_id):
    e = Db()
    session['doctor_id'] = doctor_id
    qry = "SELECT * FROM doctor WHERE doctor_id='" + doctor_id + "'"
    ans = e.selectOne(qry)
    print(ans)
    return render_template('/admin/edit_doctor.html', val=ans)


@app.route('/adm_edit_doctor_post', methods=['post'])
def adm_edit_doctor_post():
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

    #*******-edit doctor ends-****************#

    #********delete doctor begins-************#


@app.route('/adm_delete_doctor/<doctor_id>')
def adm_delete_doctor(doctor_id):
    d = Db()
    qry = "DELETE FROM doctor WHERE doctor_id='" + doctor_id + "'"
    res = d.delete(qry)
    return adm_view_doctor()

    #*********delete doctor ends**************#
#--------------add-doctor--and--view-doctor ends---------------------------------------------------------------------------------------------------------#

#--------------admin route-begins------------------------------------------------------------------------------------------------------------------------------#


@app.route("/adm_admin")
def adm_admin():
    return render_template('/admin/Admin.html')
#--------------admin route-ends-------------------------------------------------------------------------------------------------#


#---------------login------------------------------------------------------------------------------------------------------#


@app.route("/adm_login")
def adm_login():
    return render_template('/admin/login.html')


@app.route("/adm_login_post", methods=['post'])
def adm_login_post():
    i = Db()
    username = request.form['login_name']
    password = request.form['login_password']
    qry = "SELECT * FROM login WHERE username='" + \
        username+"' AND PASSWORD='"+password+"'"
    ans = i.selectOne(qry)
    if ans is not None:
        type = ans['usertype']
        if type == 'admin':
            return render_template('/admin/Admin.html')
        elif type == 'doctor':
            session["lid"] = ans["login_id"]
            return render_template('/doctor/home.html')
        else:
            return 'Invalid Username/Password'
    else:
        return 'Invalid Username/Password'


#---------------login ends--------------------------------------#

#--------------------feedback-begins----------------------------#


@app.route('/adm_view_feedback')
def adm_view_feedback():
    v = Db()
    qry = "SELECT feedback.*,user.* FROM USER,feedback WHERE feedback.user_id = user.login_id"
    ans = v.select(qry)

    return render_template('/admin/view_feedback.html', val=ans)


#---------------------feedback-ends----------------------------#

#--------------------user-begins-------------------------------#


@app.route('/adm_view_user')
def adm_view_user():
    v = Db()
    qry = "SELECT * FROM USER"
    ans = v.select(qry)

    return render_template('/admin/view_user.html', val=ans)

    #*******user_search_section_starts******#


@app.route('/adm_view_user_post', methods=['post'])
def adm_view_user_post():
    v = Db()
    name = request.form['user_search_name']
    qry = "SELECT * FROM user WHERE NAME LIKE '%"+name+"%'"
    res = v.select(qry)

    return render_template('/admin/view_user.html', val=res)
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
    v = Db()
    qry = "SELECT * FROM disease"
    res = v.select(qry)
    return render_template('/doctor/doctor_view_disease.html', val=res)
# -----------------------------------doctor-view-disease-section-ends----------------------------------------------------------------#

# schedule section begins--------------------------------------------------------------------------------------------------------------

# adding schedule by doctor begins


@app.route('/doctor_schedule_management')
def doctor_schedule_management():
    return render_template('/doctor/doctor_schedule_management.html')


@app.route('/doctor_schedule_management_post', methods=['post'])
def doctor_schedule_management_post():
    i = Db()
    from_time = request.form['from_time']
    to_time = request.form['to_time']
    date = request.form['date']
    qry = "INSERT INTO SCHEDULE(DATE,from_time,to_time,doctor_id)VALUES('"+date+"','" + \
        from_time+"','"+to_time+"','"+str(session['lid'])+"')"
    ans = i.insert(qry)
    print(ans)
    return doctor_schedule_management()
# adding schedule by doctor begins


@app.route('/doctor_view_schedule')
def doctor_view_schedule():
    v = Db()
    qry = "SELECT * FROM SCHEDULE WHERE doctor_id='"+str(session['lid'])+"'"
    ans = v.select(qry)
    print(ans)
    return render_template('/doctor/doctor_view_schedule.html', val=ans)


@app.route('/doctor_view_schedule_post', methods=['post'])
def doctor_view_schedule_post():
    s = Db()
    search_date = request.form['search_schedule_date']
    qry = "SELECT * FROM schedule WHERE date LIKE '%" + \
        search_date+"%' AND doctor_id='"+str(session['lid'])+"'"
    ans = s.select(qry)
    return render_template('/doctor/doctor_view_schedule.html', val=ans)


@app.route('/doctor_edit_schedule/<schedule_id>')
def doctor_edit_schedule(schedule_id):
    e = Db()
    session['schedule_id'] = schedule_id
    qry = "SELECT * FROM SCHEDULE WHERE schedule_id='" + schedule_id + "'"
    ans = e.selectOne(qry)
    print('---------------------')
    print(ans)
    return render_template('/doctor/doctor_edit_schedule.html', val=ans)


@app.route('/doctor_edit_schedule_post', methods=['post'])
def doctor_edit_schedule_post():
    e = Db()
    from_time = request.form['from_time']
    to_time = request.form['to_time']
    date = request.form['date']
    qry = "UPDATE SCHEDULE SET from_time='"+from_time+"' ,to_time='"+to_time + \
        "',DATE='"+date+"' WHERE schedule_id='"+str(session['schedule_id'])+"'"
    ans = e.update(qry)
    return doctor_view_schedule()


@app.route('/doctor_delete_schedule/<schedule_id>')
def doctor_delete_schedule(schedule_id):
    d = Db()

    qry = "DELETE FROM SCHEDULE WHERE schedule_id='"+schedule_id+"'"

    res = d.delete(qry)
    return doctor_view_schedule()

# schedule section ends--------------------------------------------------------------------------------------------------------------


# doctor-view-profile-section begins--------------------------------------------------------------------------------------------------------------

@app.route('/doctor_view_profile')
def doctor_view_profile():
    v = Db()

    qry = "SELECT * FROM doctor where login_id='"+str(session["lid"])+"'"
    res = v.selectOne(qry)

    return render_template('/doctor/doctor_view_profile.html', val=res)


@app.route('/doctor_view_profile_post', methods=['post'])
def doctor_view_profile_post():
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

# doctor-view-profile-section ends--------------------------------------------------------------------------------------------------------------

# doctor-view-user-section begins--------------------------------------------------------------------------------------------------------------


@app.route('/doctor_view_user')
def doctor_view_user():
    v = Db()
    qry = "SELECT * FROM user"
    ans = v.select(qry)
    print(ans)
    return render_template('/doctor/doctor_view_user.html', val=ans)


@app.route('/doctor_view_user_post', methods=['post'])
def doctor_view_user_post():
    v = Db()
    name = request.form['user_search_name']
    qry = "SELECT * FROM user WHERE NAME LIKE '%"+name+"%'"
    res = v.select(qry)
    print(res)
    return render_template('/doctor/doctor_view_user.html', val=res)
# doctor-view-user-section ends--------------------------------------------------------------------------------------------------------------

# doctor-change_password-section begins--------------------------------------------------------------------------------------------------------------


@app.route('/doctor_change_password')
def doctor_change_password():
    return render_template('/doctor/doctor_change_password.html')


@app.route('/doctor_change_password_post', methods=['post', 'get'])
def doctor_change_password_post():
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
            return render_template('/admin/login.html')
        else:
            print('cpass and new pass not same')
            return render_template('/doctor/doctor_change_password.html')

    else:
        print('Invalid')
        return render_template('/doctor/doctor_change_password.html')

# doctor-change_password-section ends--------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------#
    # Doctor Ends#               /\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/
# -------------------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":
    app.run(port=8000, debug=True)
