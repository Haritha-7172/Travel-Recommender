from app import get_db_connection
import logging
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id=None, name=None, email=None, password=None, dest_pref=None, bud_pref=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.dest_pref = dest_pref
        self.bud_pref = bud_pref

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    user_id=user_data['user_id'],
                    name=user_data['Name'],
                    email=user_data['Email'],
                    password=user_data['password'],
                    dest_pref=user_data['dest_pref'],
                    bud_pref=user_data['Bud_pref']
                )
            return None
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    user_id=user_data['user_id'],
                    name=user_data['Name'],
                    email=user_data['Email'],
                    password=user_data['password'],
                    dest_pref=user_data['dest_pref'],
                    bud_pref=user_data['Bud_pref']
                )
            return None
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def create(self):
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        try:
            hashed_password = generate_password_hash(self.password)
            query = """
            INSERT INTO User (Name, Email, password, dest_pref, Bud_pref)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.name, self.email, hashed_password, self.dest_pref, self.bud_pref))
            conn.commit()
            self.user_id = cursor.lastrowid
            return True
        except mysql.connector.Error as err:
            logging.error(f"Database error in create user: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def login(email, password):
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            return user
        return None


class Destination:
    def __init__(self, dest_id=None, name=None, type=None, avg_cost=None):
        self.dest_id = dest_id
        self.name = name
        self.type = type
        self.avg_cost = avg_cost

    @staticmethod
    def get_all():
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Destination")
            destinations = []
            for row in cursor.fetchall():
                destinations.append(Destination(
                    dest_id=row['dest_id'],
                    name=row['Name'],
                    type=row['Type'],
                    avg_cost=row['avg_cost']
                ))
            return destinations
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(dest_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Destination WHERE dest_id = %s", (dest_id,))
            dest_data = cursor.fetchone()
            if dest_data:
                return Destination(
                    dest_id=dest_data['dest_id'],
                    name=dest_data['Name'],
                    type=dest_data['Type'],
                    avg_cost=dest_data['avg_cost']
                )
            return None
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search(dest_type=None, budget=None, climate=None, accommodation_type=None, days=None):
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
            SELECT DISTINCT d.dest_id, d.Name, d.Type, d.avg_cost 
            FROM Destination d
            JOIN stays s ON d.dest_id = s.dest_id 
            LEFT JOIN Accommodation a ON s.Acc_id = a.Acc_id
            JOIN Chooses c ON d.dest_id = c.dest_id
            JOIN Budget b ON c.Bud_id = b.Bud_id
            WHERE 1=1
            """
            params = []
            
            if dest_type:
                query += " AND d.Type = %s"
                params.append(dest_type)
            
            if budget:
                query += " AND d.avg_cost <= %s"
                params.append(budget)
            
            #if climate:
                #query += " AND c.climate = %s"
                #params.append(climate)
                
            #if accommodation_type and accommodation_type.lower() != "any":
                #query += " AND a.type = %s"
                #params.append(accommodation_type)


                
            if days:
                query += " AND b.duration >= %s"
                params.append(days)
                
            cursor.execute(query, tuple(params))
            
            destinations = []
            for row in cursor.fetchall():
                destinations.append(Destination(
                    dest_id=row['dest_id'],
                    name=row['Name'],
                    type=row['Type'],
                    avg_cost=row['avg_cost']
                ))
            return destinations
        except mysql.connector.Error as err:
            logging.error(f"Database error in search: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_destination_details(dest_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            # Get destination info
            cursor.execute("SELECT * FROM Destination WHERE dest_id = %s", (dest_id,))
            dest_data = cursor.fetchone()
            if not dest_data:
                return None
                
            # Get accommodation options
            cursor.execute("""
                SELECT a.* FROM Accommodation a
                JOIN stays s ON a.Acc_id = s.Acc_id
                WHERE s.dest_id = %s
            """, (dest_id,))
            accommodations = cursor.fetchall()
            
            # Get activities
            cursor.execute("""
                SELECT Act_name, Act_cost FROM Activities
                WHERE dest_id = %s
            """, (dest_id,))
            activities = cursor.fetchall()
            
            # Get climate info
            cursor.execute("""
                SELECT DISTINCT c.climate FROM Chooses c
                WHERE c.dest_id = %s
            """, (dest_id,))
            climate_data = cursor.fetchall()
            climate = [c['climate'] for c in climate_data] if climate_data else []
            
            return {
                'destination': dest_data,
                'accommodations': accommodations,
                'activities': activities,
                'climate': climate
            }
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()


class Accommodation:
    def __init__(self, acc_id=None, name=None, type=None, cost_per_night=None):
        self.acc_id = acc_id
        self.name = name
        self.type = type
        self.cost_per_night = cost_per_night

    @staticmethod
    def get_types():
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT type FROM Accommodation")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return []
        finally:
            cursor.close()
            conn.close()


class Budget:
    def __init__(self, bud_id=None, duration=None, total_bud=None):
        self.bud_id = bud_id
        self.duration = duration
        self.total_bud = total_bud


class Activity:
    def __init__(self, act_name=None, act_cost=None, dest_id=None):
        self.act_name = act_name
        self.act_cost = act_cost
        self.dest_id = dest_id
