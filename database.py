import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase")
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise

def save_project_request(user_id: str, username: str, message: str, language: str) -> dict:
    """Enregistre une nouvelle demande de projet"""
    try:
        data = {
            'user_id': str(user_id),
            'username': username,
            'message': message,
            'language': language,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        result = supabase.table('project_requests').insert(data).execute()
        print(f"Project request saved: {result}")
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du projet: {e}")
        raise

def save_support_request(user_id: str, username: str, message: str, language: str) -> dict:
    """Enregistre une nouvelle demande de support"""
    try:
        data = {
            'user_id': str(user_id),
            'username': username,
            'message': message,
            'language': language,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        result = supabase.table('support_requests').insert(data).execute()
        print(f"Support request saved: {result}")
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la demande de support: {e}")
        raise
