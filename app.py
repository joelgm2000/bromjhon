from flask import Flask
from flask_cors import CORS  # <-- Importante para aceptar peticiones de Firebase
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os

app = Flask(__name__)
CORS(app)  # <-- Habilita CORS para permitir llamadas desde Firebase

def ejecutar_broma():
    correo_destino = "JOELGARCIAMAESTREJGM@GMAIL.COM" 
    remitente = "hackingcalavera@gmail.com"
    password = "sgje uooy laaw pdms" 

    try:
        print("Conectando con el servidor SMTP de Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        print("¡Login exitoso en Gmail!")

        # 1. Enviar los primeros 19 correos de advertencia
        for i in range(19):
            cuerpo = "Jhon, no te enseñaron que no debes confiar en QR que no sabes de donde vienen!!, soy tu AMIGUE SECRETE.\n\nESPERA EL ÚLTIMO MENSAJE QUE SE ENCUENTRA LA PISTA PARA TU REGALO."
            msg = MIMEText(cuerpo)
            
            msg['Subject'] = f"Alerta de Seguridad #{i+1} - ESPERA EL ULTIMO MENSAJE SE ENCUENTRA LA PISTA."
            msg['From'] = remitente
            msg['To'] = correo_destino
            
            server.send_message(msg)
            print(f"Mensaje {i+1}/20 enviado.")
            time.sleep(3)

        # 2. Enviar el último correo (el número 20) con el video ADJUNTO
        print("Preparando el último correo con el video...")
        msg_final = MIMEMultipart()
        msg_final['Subject'] = "Ubicación de tu regalo (Final)"
        msg_final['From'] = remitente
        msg_final['To'] = correo_destino
        
        cuerpo_final = "Aquí tienes tu pista. Reproduce el video adjunto para ver la ubicación:"
        msg_final.attach(MIMEText(cuerpo_final, 'plain'))
        
        ruta_video = "EL-3REO.mp4"
        
        try:
            with open(ruta_video, "rb") as adjunto:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(adjunto.read())
            
            encoders.encode_base64(parte)
            parte.add_header(
                'Content-Disposition',
                f'attachment; filename=EL-3REO.mp4'
            )
            msg_final.attach(parte)
            
            server.send_message(msg_final)
            print("Mensaje 20/20 enviado con el video adjunto. Broma completada con éxito.")
            
        except FileNotFoundError:
            print(f"ERROR CRÍTICO: No se encontró el archivo '{ruta_video}' en el repositorio de Render.")
        except Exception as e_adjunto:
            print(f"ERROR CRÍTICO al adjuntar el video: {e_adjunto}")

        server.quit()
        
    except Exception as e:
        print(f"ERROR CRÍTICO DE AUTENTICACIÓN O SMTP: {e}")
        
@app.route('/activar', methods=['GET', 'POST'])
def activar_broma():
    hilo = threading.Thread(target=ejecutar_broma)
    hilo.start()
    return "Ejecutando", 200

if __name__ == '__main__':
    app.run(port=5000)