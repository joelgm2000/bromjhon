from flask import Flask
from flask_cors import CORS
import threading
import resend
import time
import base64

app = Flask(__name__)
CORS(app)

# Tu API Key de Resend recién creada
resend.api_key = "re_2yfP5trd_CxXC7KQwvGUhUC6YumC2FNhj"

def ejecutar_broma():
    correo_destino = "JOELGARCIAMAESTREJGM@GMAIL.COM" 
    remitente = "onboarding@resend.dev" # Remitente oficial gratuito de pruebas de Resend

    try:
        print("Iniciando envío de la broma a través de la API de Resend...")

        # 1. Enviar los primeros 19 correos de advertencia
        for i in range(19):
            cuerpo = "Jhon, no te enseñaron que no debes confiar en QR que no sabes de donde vienen!!, soy tu AMIGUE SECRETE.\n\nESPERA EL ÚLTIMO MENSAJE QUE SE ENCUENTRA LA PISTA PARA TU REGALO."
            
            params = {
                "from": f"Amigue Secreto <{remitente}>",
                "to": [correo_destino],
                "subject": f"Alerta de Seguridad #{i+1} - ESPERA EL ULTIMO MENSAJE SE ENCUENTRA LA PISTA.",
                "text": cuerpo,
            }
            
            email = resend.Emails.send(params)
            print(f"Mensaje {i+1}/20 enviado. ID: {email.get('id')}")
            time.sleep(3)

        # 2. Enviar el último correo (el número 20) con el video ADJUNTO
        print("Preparando el último correo con el video adjunto...")
        ruta_video = "EL-3REO.mp4"
        
        try:
            with open(ruta_video, "rb") as f:
                contenido_video = f.read()
            
            video_base64 = base64.b64encode(contenido_video).decode('utf-8')

            params_final = {
                "from": f"Amigue Secreto <{remitente}>",
                "to": [correo_destino],
                "subject": "Ubicación de tu regalo (Final)",
                "text": "Aquí tienes tu pista. Reproduce el video adjunto para ver la ubicación:",
                "attachments": [
                    {
                        "filename": "EL-3REO.mp4",
                        "content": video_base64
                    }
                ]
            }
            
            email_final = resend.Emails.send(params_final)
            print(f"Mensaje 20/20 enviado con éxito. ID: {email_final.get('id')}")
            
        except FileNotFoundError:
            print(f"ERROR CRÍTICO: No se encontró el archivo '{ruta_video}' en el repositorio de Render.")
        except Exception as e_adjunto:
            print(f"ERROR al adjuntar el video: {e_adjunto}")
        
    except Exception as e:
        print(f"ERROR CRÍTICO con la API de Resend: {e}")

@app.route('/activar', methods=['GET', 'POST'])
def activar_broma():
    hilo = threading.Thread(target=ejecutar_broma)
    hilo.start()
    return "Ejecutando", 200

if __name__ == '__main__':
    app.run(port=5000)