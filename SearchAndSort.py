class SearchAndSort:
    @staticmethod
    def search_data(connection, search_term):
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE FirstName LIKE %s OR LastName LIKE %s OR Username LIKE %s"
        cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        connection.close()
        return results
