#!/usr/bin/env python3
"""
Script pour exécuter et récupérer les résultats du notebook
"""

import subprocess
import time
import json
import os

NOTEBOOK_ID = "mkawarhoussem/promptfoo-ollama-yimchi-mrigil-hamdoulah"
KERNEL_DIR = "./kaggle_kernel"
OUTPUT_DIR = "./results"

def run_notebook():
    print(f"🚀 Exécution du notebook {NOTEBOOK_ID}")
    
    # Push
    result = subprocess.run(
        f"cd {KERNEL_DIR} && kaggle kernels push -p .",
        shell=True, capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
        return False
    
    # Attente
    print("⏳ Attente de l'exécution...")
    for i in range(60):
        status = subprocess.run(
            f"kaggle kernels status {NOTEBOOK_ID}",
            shell=True, capture_output=True, text=True
        ).stdout.lower()
        
        if "complete" in status:
            print("✅ Exécution terminée")
            break
        time.sleep(30)
    
    # Téléchargement
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    subprocess.run(
        f"kaggle kernels output {NOTEBOOK_ID} -p {OUTPUT_DIR}",
        shell=True
    )
    
    # Afficher résultats
    results_file = os.path.join(OUTPUT_DIR, "results.json")
    if os.path.exists(results_file):
        with open(results_file) as f:
            data = json.load(f)
            print(f"📊 Résultat: {'JAILBREAK' if data.get('is_jailbreak') else 'SAFE'}")
            print(f"   ASR: {data.get('asr', 0)}%")
    
    return True

if __name__ == "__main__":
    run_notebook()