# Rapport - Serveur de Paramètres Distribué

**Groupe :** 4IIR IADATA 4  
**Réalisé par :** Anas ELAYATTI - Steven HASSAN Kabre  
**Module :** Systèmes Distribués  
**Sujet :** 28 - Serveur de Paramètres (Parameter Server)

---

## 1. Introduction
Le Parameter Server est une architecture de Machine Learning distribué 
où plusieurs workers calculent des gradients en parallèle et un serveur 
central agrège ces gradients pour mettre à jour un modèle global.

## 2. Architecture
- **Serveur central** : stocke les poids du modèle global
- **Workers** : calculent les gradients sur leurs données locales
- **Communication** : sockets TCP avec échange de messages JSON

## 3. Algorithme Asynchrone
1. Le worker récupère les poids actuels du serveur
2. Il calcule les gradients sur son mini-batch local
3. Il envoie les gradients au serveur
4. Le serveur met à jour les poids immédiatement sans attendre les autres workers

## 4. Théorème CAP
Notre système favorise **AP (Availability + Partition Tolerance)** :
- Disponibilité : le serveur répond toujours
- Tolérance aux pannes : si un worker tombe, le système continue
- Cohérence sacrifiée : les workers peuvent recevoir des poids obsolètes (stale gradients)

## 5. Problème des Stale Gradients
En mode asynchrone, un worker peut calculer des gradients sur des poids 
obsolètes car le serveur a déjà été mis à jour par d'autres workers.
Observé dans nos tests : Worker 2 reçoit version 9 pendant que le serveur est à version 11.

## 6. Simulation de Pannes
- **Test 1** : Arrêt du Worker 2 en pleine exécution → les Workers 1 et 3 continuent
- **Test 2** : 3 workers en parallèle → convergence jusqu'à la version 24
- **Résultat** : Le système est tolérant aux pannes

## 7. Guide d'utilisation

### Lancement manuel
```bash
# Terminal 1 - Serveur
python server/parameter_server.py

# Terminal 2 - Worker 1
python worker/worker.py 1

# Terminal 3 - Worker 2
python worker/worker.py 2
```

### Lancement avec Docker
```bash
docker-compose up
```

### Lancement des tests
```bash
python tests/test_fault_tolerance.py
```

## 8. Conclusion
Le système démontre les principes fondamentaux d'un système distribué :
asynchronisme, tolérance aux pannes et gestion des stale gradients.