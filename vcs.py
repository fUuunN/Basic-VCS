import os
import shutil
import hashlib
import json
from datetime import datetime

def get_repo_path():
    """Mevcut çalışma dizinini döndürür."""
    return os.getcwd()

def get_vcs_path(repo_path):
    """VCS verilerinin saklanacağı .vcs dizininin yolunu döndürür."""
    return os.path.join(repo_path, '.vcs')

def get_commits_path(vcs_path):
    """Commits dizininin yolunu döndürür."""
    return os.path.join(vcs_path, 'commits')

def init():
    """Yeni bir VCS deposu başlatır."""
    repo_path = get_repo_path()
    vcs_path = get_vcs_path(repo_path)
    commits_path = get_commits_path(vcs_path)
    
    if not os.path.exists(vcs_path):
        os.makedirs(vcs_path)
        os.makedirs(commits_path)
        print(f"Initialized empty VCS repository in {vcs_path}")
    else:
        print("VCS repository already exists.")

def commit(message, user_name):
    """Değişiklikleri commit yapar."""
    repo_path = get_repo_path()
    vcs_path = get_vcs_path(repo_path)
    commits_path = get_commits_path(vcs_path)
    
    commit_hash = generate_commit_hash(repo_path)
    commit_path = os.path.join(commits_path, commit_hash)
    shutil.copytree(repo_path, commit_path, ignore=shutil.ignore_patterns('.vcs'))
    save_commit(commit_hash, message, user_name, vcs_path)
    print(f"Committed changes: {message}")

def revert(commit_hash):
    """Belirtilen commit hash'ine geri döner."""
    repo_path = get_repo_path()
    vcs_path = get_vcs_path(repo_path)
    commits_path = get_commits_path(vcs_path)
    
    commit_path = os.path.join(commits_path, commit_hash)
    if os.path.exists(commit_path):
        for item in os.listdir(repo_path):
            if item != '.vcs':
                item_path = os.path.join(repo_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        shutil.copytree(commit_path, repo_path, dirs_exist_ok=True)
        print(f"Reverted to commit {commit_hash}")
    else:
        print("Commit hash not found.")

def list_commits():
    """Tüm commit hash'lerini listeler."""
    repo_path = get_repo_path()
    vcs_path = get_vcs_path(repo_path)
    commits_path = get_commits_path(vcs_path)
    
    commits = os.listdir(commits_path)
    commits.sort()  # Sadece hash'leri sıraya koyar
    for commit in commits:
        print(f"Hash: {commit}")

def generate_commit_hash(repo_path):
    """Depodaki dosyaların içeriğinden bir commit hash'i oluşturur."""
    hasher = hashlib.sha1()
    for root, dirs, files in os.walk(repo_path):
        for fname in files:
            if '.vcs' in root:
                continue
            file_path = os.path.join(root, fname)
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
    return hasher.hexdigest()

def save_commit(commit_hash, message, user_name, vcs_path):
    """Commit bilgilerini .json dosyasına kaydeder."""
    commit_info = {
        'hash': commit_hash,
        'message': message,
        'user': user_name,
        'timestamp': datetime.now().isoformat()
    }
    with open(os.path.join(vcs_path, f"{commit_hash}.json"), 'w') as f:
        json.dump(commit_info, f, indent=4)
