from flask import Flask, render_template, request, session
from DBConnection import Db
app = Flask(__name__)
app.secret_key = "abc"
#--------------add-disease--and--view-disease--and--edit-disease---and-delete-disease-begins-----------------------------------------------------------------#


@app.route("/adm_add_disease")
def adm_add_disease():
    return render_template('/admin/add_disease.html')


@app.route("/adm_add_disease_post", methods=['post'])
def adm_add_disease_post():
    i = Db()
    name = request.form['add_disease_name']
    image = request.files['add_disease_image']
    image.save(
        'F:\\Skin_Disease_Recogniton\\static\\disease_images\\' + image.filename)
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
                "F:\\Skin_Disease_Recogniton\\static\\disease_images\\" + image.filename)
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
        'F:\\Skin_Disease_Recogniton\\static\\disease_images\\' + image.filename)
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
                'F:\\Skin_Disease_Recogniton\\static\\disease_images\\' + image.filename)
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

#--------------admin-begins------------------------------------------------------------------------------------------------------------------------------#


@app.route("/adm_admin")
def adm_admin():
    return render_template('/admin/Admin.html')
#--------------amdin-ends-------------------------------------------------------------------------------------------------#


#---------------login-------------------------------------------#


@app.route("/adm_login")
def adm_login():
    return render_template('/admin/login.html')


@app.route("/adm_login_post", methods=['post'])
def adm_login_post():
    i = Db()
    username = request.form['login_name']
    password = request.form['login_password']
    qry = "INSERT INTO login(username,PASSWORD)VALUES('" + \
        username+"','"+password+"')"
    ans = i.insert(qry)
    return adm_login()
#---------------login ends--------------------------------------#

#--------------------feedback-begins----------------------------#


@app.route('/adm_view_feedback')
def adm_view_feedback():
    return render_template('/admin/view_feedback.html')
#---------------------feedback-ends----------------------------#

#--------------------user-begins-------------------------------#


@app.route('/adm_view_user')
def adm_view_user():
    return render_template('/admin/view_user.html')

#------------------------user-ends-----------------------------#


if __name__ == "__main__":
    app.run(port=8000, debug=True)
