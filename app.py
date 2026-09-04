from flask import Flask
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os

app = Flask(__name__)

def ejecutar_broma():
    correo_destino = "JOELGARCIAMAESTREJGM@GMAIL.COM" 
    remitente = "hackingcalavera@gmail.com"
    
    # Tu contraseña de aplicación (asegúrate de que siga activa si la generaste recientemente)
    password = "sgje uooy laaw pdms" 

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)

        # 1. Enviar los primeros 19 correos de advertencia
        for i in range(19):
            # Nuevo cuerpo del mensaje
            cuerpo = "Jhon, no te enseñaron que no debes confiar en QR que no sabes de donde vienen!!, soy tu AMIGUE SECRETE.\n\nESPERA EL ÚLTIMO MENSAJE QUE SE ENCUENTRA LA PISTA PARA TU REGALO."
            msg = MIMEText(cuerpo)
            
            # Nuevo asunto del mensaje
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
        
        # Ruta donde está tu video (asumiendo que app.py está en la raíz de tu proyecto)
        ruta_video = "EL-3REO.mp4"
        
        # Lógica para adjuntar el archivo
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
            print(f"ERROR: No se encontró el video en la ruta '{ruta_video}'. Asegúrate de que app.py esté al lado de la carpeta public.")
        except Exception as e_adjunto:
            print(f"ERROR al adjuntar el video: {e_adjunto}")

        server.quit()
        
    except Exception as e:
        print(f"Error general: {e}")

@app.route('/activar')
def activar_broma():
    hilo = threading.Thread(target=ejecutar_broma)
    hilo.start()
    return "Ejecutando", 200

if __name__ == '__main__':
    app.run(port=5000)