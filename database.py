from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client with custom options
options = {
    'auth': {
        'autoRefreshToken': True,
        'persistSession': False
    },
    'db': {
        'schema': 'public'
    }
}

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options)
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise

async def save_project_request(user_id: str, username: str, message: str, language: str):
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

async def save_support_request(user_id: str, username: str, message: str, language: str):
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
