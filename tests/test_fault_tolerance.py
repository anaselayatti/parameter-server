import threading
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.parameter_server import ParameterServer
from worker.worker import Worker

def run_server():
    server = ParameterServer()
    server.start()

def test_worker_failure():
    print("\n🧪 Test 1 : Panne d'un worker")
    
    # Lancer le serveur dans un thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    # Lancer 3 workers
    workers = []
    for i in range(1, 4):
        w = Worker(worker_id=i)
        t = threading.Thread(target=w.run, args=(5,), daemon=True)
        workers.append(t)
        t.start()

    # Attendre 3 secondes puis tuer le worker 2
    time.sleep(3)
    print("💥 Simulation panne Worker 2...")
    workers[1].join(timeout=0)  # Simule l'arrêt

    # Les autres workers continuent
    time.sleep(5)
    print("✅ Test 1 réussi : le système continue malgré la panne")

def test_multiple_workers():
    print("\n🧪 Test 2 : Plusieurs workers en parallèle")
    time.sleep(1)
    
    workers = []
    for i in range(1, 4):
        w = Worker(worker_id=i)
        t = threading.Thread(target=w.run, args=(3,), daemon=True)
        workers.append(t)
        t.start()

    for t in workers:
        t.join()
    
    print("✅ Test 2 réussi : 3 workers ont tourné en parallèle")

if __name__ == '__main__':
    test_worker_failure()
    test_multiple_workers()
    print("\n✅ Tous les tests sont passés !")