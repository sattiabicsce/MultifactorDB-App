class UserAuthentication:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate_user(self, username, password):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE Username=%s AND Password=%s"  # Ensure passwords are hashed
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        connection.close()
        return user
