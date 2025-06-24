import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3
from datetime import datetime, timedelta
import bcrypt

class AuthManager:
    def __init__(self):
        self.config_file = 'config/config.yaml'
        self.db_file = 'data/users.db'
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for user management and usage tracking"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                plan TEXT DEFAULT 'basic',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                usage_limit INTEGER DEFAULT 100
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                processing_time REAL,
                success BOOLEAN DEFAULT 1,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_end TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_config(self):
        """Load authentication configuration"""
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
            return config
        except FileNotFoundError:
            st.error("Configuration file not found. Please contact administrator.")
            return None
            
    def get_authenticator(self):
        """Get streamlit authenticator instance"""
        config = self.load_config()
        if config:
            return stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )
        return None
        
    def register_user(self, username, email, name, password, role='user', plan='basic'):
        """Register a new user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute('''
                INSERT INTO users (username, email, name, password_hash, role, plan)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, name, password_hash, role, plan))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def log_usage(self, username, tool_name, action, file_size=None, processing_time=None, success=True):
        """Log user activity"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usage_logs (username, tool_name, action, file_size, processing_time, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, tool_name, action, file_size, processing_time, success))
        
        conn.commit()
        conn.close()
        
    def get_user_usage(self, username, days=30):
        """Get user usage statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tool_name, action, COUNT(*) as count, 
                   AVG(processing_time) as avg_time,
                   SUM(file_size) as total_size
            FROM usage_logs 
            WHERE username = ? AND timestamp >= datetime('now', '-{} days')
            GROUP BY tool_name, action
        '''.format(days), (username,))
        
        results = cursor.fetchall()
        conn.close()
        return results
        
    def get_all_users(self):
        """Get all users for admin dashboard"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, email, name, role, plan, created_date, last_login, is_active
            FROM users
            ORDER BY created_date DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
        
    def update_last_login(self, username):
        """Update user's last login timestamp"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
        
    def get_usage_stats(self):
        """Get overall usage statistics for admin dashboard"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Active users (logged in last 30 days)
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE last_login >= datetime('now', '-30 days')
        ''')
        active_users = cursor.fetchone()[0]
        
        # Total usage events
        cursor.execute('SELECT COUNT(*) FROM usage_logs')
        total_usage = cursor.fetchone()[0]
        
        # Usage by tool
        cursor.execute('''
            SELECT tool_name, COUNT(*) as count
            FROM usage_logs
            GROUP BY tool_name
            ORDER BY count DESC
        ''')
        tool_usage = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_usage': total_usage,
            'tool_usage': tool_usage
        }