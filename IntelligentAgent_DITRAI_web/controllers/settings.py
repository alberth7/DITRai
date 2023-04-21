from flask import Blueprint, render_template,request,redirect,flash, url_for
from flask_login import login_user, logout_user
from models.settingDitrai import SettingDitrai, db
from models.settingRouter import SettingRouter, db
from models.settingApi_ML import SettingApi_ML, db
from models.settingServer import SettingServer, db
from main import bcrypt
import subprocess
import unittest



settings=Blueprint("settings",__name__,url_prefix="/",template_folder="../templates/settings")


@settings.route('/settings', methods=['GET'])
def setting():
    # Obtener los datos de la tabla SettingDitrai
    data = SettingDitrai.query.first()
    return render_template('settings.html', data_settings=data)

@settings.route('/settings', methods=['POST'])
def setting_post():
    data = SettingDitrai.query.first()
    if 'submit1' in request.form:
        # Obtener los datos enviados desde el formulario
        chat_id = request.form['chat_id']
        telegramToken = request.form['telegramToken']
        monitorSystem = request.form['monitorSystem']
        frecuencyGetTableTrafict = request.form['frecuencyGetTableTrafict']
        timeFrecuencyGetTableTrafict = request.form['timeFrecuencyGetTableTrafict']
        # Actualizar el campo chatId
        data.chatId = chat_id
        data.telegramToken = telegramToken
        data.monitorSystem = monitorSystem
        data.frecuencyGetTableTrafict = frecuencyGetTableTrafict
        data.timeFrecuencyGetTableTrafict = timeFrecuencyGetTableTrafict

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash("Datos actualizados correctamente !!!", 'success')
        # Redirigir a la vista de configuración
        return render_template('settings.html', data_settings=data)
        
    elif 'submit2' in request.form:
        if data.beginEnd == 1:
            flash("El software DITRai ya se encuentra encendido ...", 'danger')
        else:
            data.beginEnd = 1
            db.session.commit()
            command = "sudo systemctl restart ditrai.service"  # comando a ejecutar
            output = subprocess.check_output(command, shell=True)  # ejecutar el comando y guardar la salida
            print(output)
            mensaje ="EL comando se ejecuto con exitos!"
            flash("El software DITRai fue encendido ...",  'success')
        return redirect(url_for('settings.setting'))
        
    elif 'submit3' in request.form:
        if data.beginEnd == 0:
            flash("El software DITRai ya se encuentra apagado ...", 'danger')
        else:
            data.beginEnd = 0
            db.session.commit()
            command = "sudo systemctl stop ditrai.service"  # comando a ejecutar
            output = subprocess.check_output(command, shell=True)  # ejecutar el comando y guardar la salida
            print(output)
            mensaje ="EL comando se ejecuto con exitos!"
            flash("El software DITRai fue apagado ...",  'success')
        return redirect(url_for('settings.setting'))
        
    return redirect(url_for('settings.setting'))


        

@settings.route("/execute")
def execute():
    data = SettingDitrai.query.first()
    # Actualizar el campo chatId
    if data.beginEnd == 0:
        data.beginEnd = 1    
        db.session.commit()
        command = "pwd"  # comando a ejecutar
        output = subprocess.check_output(command, shell=True)  # ejecutar el comando y guardar la salida
        print(output)
        mensaje ="EL comando se ejecuto con exitos!"
    else:
        mensaje ="EL comando ya fue ejecutado"
    
    flash("Datos actualizados correctamente!!!!!!!")
    return redirect(url_for('settings.settingAPI_ML'))
    #return render_template('settings.html', data_settings=data, mensaje=mensaje)


@settings.route("/executeApagar")
def executeApagar():
    command = "ls -lsa"  # comando a ejecutar
    output = subprocess.check_output(command, shell=True)  # ejecutar el comando y guardar la salida
    data = SettingDitrai.query.first()
    # Actualizar el campo chatId
    data.beginEnd = 0
    db.session.commit()
    flash("Datos actualizados correctamente")
    print(output)
    return render_template('settings.html', data_settings=data)

# models ML

@settings.route('/settingAPI_ML', methods=['GET'])
def settingAPI_ML():
    # Obtener los datos de la tabla SettingDitrai
    data = SettingApi_ML.query.first()
    return render_template('settingsAPI_ML.html', data_settings=data)

@settings.route('/settingAPI_ML', methods=['POST'])
def setting_postAPI_ML():
    # Obtener los datos enviados desde el formulario
    model_1 = request.form['model_1']
    model_2 = request.form['model_2']
    # Obtener la instancia de la tabla SettingDitrai
    data = SettingApi_ML.query.first()
    # Actualizar el campo chatId
    data.model_1 = model_1
    data.model_2 = model_2

    # Guardar los cambios en la base de datos
    db.session.commit()
    flash("Datos actualizados correctamente")
    # Redirigir a la vista de configuración
    #return redirect(url_for('/settings'))
    return render_template('settingsAPI_ML.html', data_settings=data)

# Router

@settings.route('/settingRouter', methods=['GET'])
def settingRouter():
    # Obtener los datos de la tabla SettingDitrai
    data = SettingRouter.query.first()
    return render_template('settingRouter.html', data_settings=data)

@settings.route('/settingRouter', methods=['POST'])
def settingRouter_post():
    # Obtener los datos enviados desde el formulario
    host = request.form['host']
    user = request.form['user']
    password = request.form['password']
    port = request.form['port']
    sshPath = request.form['sshPath']
    # Obtener la instancia de la tabla SettingDitrai
    data = SettingRouter.query.first()
    # Actualizar el campo chatId
    data.host = host
    data.user = user
    data.password = password
    data.port = port
    data.sshPath = sshPath
    # Guardar los cambios en la base de datos
    db.session.commit()
    flash("Datos actualizados correctamente")
    # Redirigir a la vista de configuración
    #return redirect(url_for('/settings'))
    return render_template('settingRouter.html', data_settings=data)

# Server

@settings.route('/settingServer', methods=['GET'])
def settingServer():
    # Obtener los datos de la tabla SettingDitrai
    data = SettingServer.query.first()
    return render_template('settingServer.html', data_settings=data)

@settings.route('/settingServer', methods=['POST'])
def settingServer_post():
    # Obtener los datos enviados desde el formulario
    dbName = request.form['dbName']
    userDB = request.form['userDB']
    passwordDB = request.form['passwordDB']
    hostDB = request.form['hostDB']
    portDB = request.form['portDB']
    # Obtener la instancia de la tabla SettingDitrai
    data = SettingServer.query.first()
    # Actualizar el campo chatId
    data.dbName = dbName
    data.userDB = userDB
    data.passwordDB = passwordDB
    data.hostDB = hostDB
    data.portDB = portDB
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    flash("Datos actualizados correctamente")
    # Redirigir a la vista de configuración
    #return redirect(url_for('/settings'))
    return render_template('settingServer.html', data_settings=data)