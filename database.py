from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialiser le client Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_project_request(user_id: str, username: str, message: str, language: str) -> None:
    """
    Save a project request to Supabase
    """
    try:
        data = {
            'user_id': user_id,
            'username': username,
            'message': message,
            'language': language,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        result = supabase.table('project_requests').insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error saving project request: {e}")
        return None

def save_support_request(user_id: str, username: str, message: str, language: str) -> None:
    """
    Save a support request to Supabase
    """
    try:
        data = {
            'user_id': user_id,
            'username': username,
            'message': message,
            'language': language,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        result = supabase.table('support_requests').insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error saving support request: {e}")
        return None
