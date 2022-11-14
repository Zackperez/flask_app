import json
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from random import choice

app = Flask (__name__)

CORS(app)
# Mysql Connection
app.config['MYSQL_HOST'] = 'bd-sbr-ia.ctl0hwzog7zq.us-east-1.rds.amazonaws.com' 
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Zacksykes.2018'
app.config['MYSQL_DB'] = 'sistema_de_reglas'
mysql = MySQL(app)

@app.route('/get_user_info')
def recibir_usuario_info():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario')
        rv = cur.fetchall()
        cur.close()
        payload = []
        usuarios_contenido = {} 
        for result in rv:
            usuarios_contenido = {'id del usuario':result[0], 'id_preguntas': result[1]}
            payload.append(usuarios_contenido)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"error":e})

@app.route('/get_all_user_questions') #Muestra todos los registros
def recibir_preguntas_usuario():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Preguntas')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {"nose":rv}
        for result in rv:
            print({"id_preguntas":result[0],"id_respuestas":result[1],"id_usuario":result[2],"Pregunta 1":result[3],"Pregunta 2":result[4],"Pregunta 3":result[5],"Pregunta 4":result[6],"Pregunta 5":result[7]})
        
        return jsonify(content)
    except Exception as e:
        print(e)
        return jsonify({"error":e})

@app.route('/get_user/<id>',methods=['GET'])
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario_Respuestas WHERE Id_Usuario = %s', (id))
        rv = cur.fetchall()
        cur.close()
        content = {rv}
        web = {"nose":rv}
        sbr(rv)
        return jsonify(web)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/add_contact', methods=['POST'])
def agregar_respuestas():
    try:
        if request.method == 'POST':
            respuesta1 = request.json['Respuesta_1']
            respuesta2 = request.json['Respuesta_2']       
            respuesta3 = request.json['Respuesta_3']        
            respuesta4 = request.json['Respuesta_4']     
            respuesta5 = request.json['Respuesta_5']       
 #INSERT INTO notificacion (id_blog,fecha, notificacion) VALUES  (ultimo_id_blog,fechaAdd, 'Registro Exitoso');
            cur = mysql.connection.cursor()
            id = 0
            cur.execute("INSERT INTO Respuestas (Respuesta_1,Respuesta_2,Respuesta_3,Respuesta_4,Respuesta_5) VALUES (%s,%s,%s,%s,%s)", (respuesta1,respuesta2,respuesta3,respuesta4,respuesta5))
            cur.close()
            mysql.connection.commit()
            return jsonify({"informacion":"Registro exitoso de respuestas"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})



@app.route('/add_user', methods=['POST'])
def agregar_usuario():
    try:
        if request.method == 'POST':
            Nombre = request.json['Nombre']
            Apellido = request.json['Apellido']
            Respuesta_abdominal= request.json['Respuesta_abdominal']
            Respuesta_diarrea = request.json['Respuesta_diarrea']
            Respuesta_estrenimiento = request.json['Respuesta_estrenimiento']
            Respuesta_acidez = request.json['Respuesta_acidez']
            Respuesta_vomitos = request.json['Respuesta_vomitos']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Usuario_Respuestas (Nombre, Apellido, Respuesta_abdominal, Respuesta_diarrea, Respuesta_estrenimiento, Respuesta_acidez, Respuesta_vomitos) VALUES (%s,%s,%s,%s,%s,%s,%s)", (Nombre,Apellido,Respuesta_abdominal,Respuesta_diarrea,Respuesta_estrenimiento ,Respuesta_acidez,Respuesta_vomitos))
            cur.close()
            mysql.connection.commit()
            return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})
        
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


from sistema_basado_reglas.sistemadereglas import *
from sistema_basado_reglas.reglas import *

def sbr(informacion):

    engine = sistemadereglas()

    engine.reset()

    lista_informacion = list(informacion)
    lista_uso = lista_informacion[0]
    #print("id_usuario",lista_uso[0])
    #print("nombre",lista_uso[1])
    #print("apellido",lista_uso[2])
    resp_abdominal = lista_uso[3]
    resp_diarrea = lista_uso[4]
    resp_estrenimiento = lista_uso[5]
    resp_acidez = lista_uso[6]
    resp_vomitos = lista_uso[7]


    engine.declare(reglas(resp_abdominal = resp_abdominal))
    engine.declare(reglas(resp_diarrea = resp_diarrea))
    engine.declare(reglas(resp_estrenimiento = resp_estrenimiento))
    engine.declare(reglas(resp_acidez = resp_acidez))
    engine.declare(reglas(resp_vomitos = resp_vomitos))

    engine.run() 


if __name__ == '__main__':
    app.run(debug = True, port = 4000)