import socket
import numpy as np
import json
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Worker:
    def __init__(self, worker_id, server_host='localhost', server_port=9999):
        self.worker_id = worker_id
        self.server_host = server_host
        self.server_port = server_port

    def send_request(self, request):
        """Envoie une requête au serveur et retourne la réponse"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_host, self.server_port))
        s.send(json.dumps(request).encode())
        response = json.loads(s.recv(4096).decode())
        s.close()
        return response

    def get_weights(self):
        """Récupère les poids depuis le serveur"""
        request = {'type': 'get_weights', 'worker_id': self.worker_id}
        response = self.send_request(request)
        logging.info(f"Worker {self.worker_id} - Poids reçus (version {response['version']})")
        return response['weights'], response['version']

    def compute_gradients(self, weights):
        """Simule le calcul des gradients sur un mini-batch local"""
        # Simulation d'un calcul de gradient (aléatoire pour la démo)
        time.sleep(random.uniform(0.5, 2.0))  # Simule le temps de calcul
        gradients = [random.uniform(-0.1, 0.1) for _ in weights]
        return gradients

    def push_gradients(self, gradients):
        """Envoie les gradients au serveur"""
        request = {
            'type': 'push_gradients',
            'worker_id': self.worker_id,
            'gradients': gradients
        }
        response = self.send_request(request)
        logging.info(f"Worker {self.worker_id} - Gradients envoyés - Version serveur : {response['version']}")

    def run(self, iterations=10):
        """Boucle principale du worker"""
        logging.info(f"🚀 Worker {self.worker_id} démarré")
        for i in range(iterations):
            logging.info(f"Worker {self.worker_id} - Itération {i+1}/{iterations}")

            # 1. Récupérer les poids
            weights, version = self.get_weights()

            # 2. Calculer les gradients
            gradients = self.compute_gradients(weights)

            # 3. Envoyer les gradients
            self.push_gradients(gradients)

        logging.info(f"✅ Worker {self.worker_id} terminé")

if __name__ == '__main__':
    import sys
    worker_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    worker = Worker(worker_id=worker_id)
    worker.run(iterations=10)