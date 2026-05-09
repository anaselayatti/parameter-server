import socket
import threading
import numpy as np
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ParameterServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.weights = np.zeros(10).tolist()  # Modèle global (10 paramètres)
        self.version = 0
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        logging.info(f"✅ Parameter Server démarré sur le port {self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            logging.info(f"🔗 Worker connecté : {address}")
            thread = threading.Thread(target=self.handle_worker, args=(client_socket,))
            thread.start()

    def handle_worker(self, client_socket):
        try:
            data = client_socket.recv(4096).decode()
            request = json.loads(data)

            if request['type'] == 'get_weights':
                # Worker demande les poids
                response = {
                    'weights': self.weights,
                    'version': self.version
                }
                logging.info(f"📤 Poids envoyés (version {self.version})")

            elif request['type'] == 'push_gradients':
                # Worker envoie ses gradients
                gradients = request['gradients']
                worker_id = request['worker_id']

                with self.lock:
                    # Mise à jour asynchrone des poids
                    learning_rate = 0.01
                    self.weights = [
                        w - learning_rate * g
                        for w, g in zip(self.weights, gradients)
                    ]
                    self.version += 1

                logging.info(f"📥 Gradients reçus du Worker {worker_id} - Version {self.version}")
                response = {'status': 'ok', 'version': self.version}

            client_socket.send(json.dumps(response).encode())

        except Exception as e:
            logging.error(f"❌ Erreur : {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    server = ParameterServer()
    server.start()