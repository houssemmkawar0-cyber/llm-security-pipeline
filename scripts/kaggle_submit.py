#!/usr/bin/env python3
# scripts/kaggle_submit.py
import subprocess, time, os, json, sys

def push_kernel(kernel_dir: str):
    """Push le kernel vers Kaggle"""
    print(f"📤 Push vers Kaggle: {kernel_dir}")
    result = subprocess.run(
        ["kaggle", "kernels", "push", "-p", kernel_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"❌ Erreur push: {result.stderr}")
        return None
    print("✅ Kernel poussé")
    return True

def wait_for_completion(kernel_id: str, timeout: 7200):
    """Polling jusqu'à complétion"""
    print(f"⏳ Attente complétion: {kernel_id}")
    start = time.time()
    
    while time.time() - start < timeout:
        result = subprocess.run(
            ["kaggle", "kaggle", "kernels", "status", "-p", kernel_id],
            capture_output=True, text=True
        )
        status = result.stdout.lower()
        
        if "complete" in status:
            print("✅ Exécution terminée")
            return True
        elif "error" in status or "failed" in status:
            print(f"❌ Échec: {result.stdout}")
            return False
        
        print(f"   Status: {status.strip()} (attente...)")
        time.sleep(30)
    
    print("⏰ Timeout atteint")
    return False

def download_output(kernel_id: str, output_dir: str):
    """Télécharger les résultats"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"📥 Téléchargement résultats vers {output_dir}")
    
    result = subprocess.run(
        ["kaggle", "kernels", "output", kernel_id, "-p", output_dir],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"✅ Résultats téléchargés")
        return True
    else:
        print(f"❌ Erreur download: {result.stderr}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel-dir", required=True, help="Dossier du kernel")
    parser.add_argument("--kernel-id", required=True, help="username/kernel-name")
    parser.add_argument("--output-dir", default="./results", help="Dossier sortie")
    args = parser.parse_args()
    
    if not push_kernel(args.kernel_dir):
        sys.exit(1)
    
    if not wait_for_completion(args.kernel_id):
        sys.exit(1)
    
    if not download_output(args.kernel_id, args.output_dir):
        sys.exit(1)
    
    print("🎉 Pipeline Kaggle terminé avec succès")
    sys.exit(0)