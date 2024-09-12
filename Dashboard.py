import PySimpleGUI as sg

class AdminDashboard:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @staticmethod
    def layout():
        return [
            [sg.Text('Admin Dashboard')],
            [sg.Input(key='-SEARCH-', enable_events=True), sg.Button('Search')],
            [sg.Button('Add Data'), sg.Button('Edit Data'), sg.Button('Delete Data')],
            [sg.Table(values=[],
                      headings=['UserID', 'FirstName', 'LastName', 'Username', 'JobTitle', 'ClearanceLevel', 'Role'],
                      key='-USER_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            [sg.Button('View Smartphones'), sg.Button('Logout')]
        ]

    def fetch_all_users(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UserID, FirstName, LastName, Username, Password, JobTitle, ClearanceLevel, Role FROM Users"
        cursor.execute(query)
        users = cursor.fetchall()
        connection.close()
        return users

    def add_data(self, user_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO Users (FirstName, LastName, Username, Password, JobTitle, ClearanceLevel, Role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, user_data)
        connection.commit()
        connection.close()

    def edit_data(self, user_id, user_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "UPDATE Users SET FirstName=%s, LastName=%s, Username=%s, Password=%s, JobTitle=%s, ClearanceLevel=%s, Role=%s WHERE UserID=%s"
        cursor.execute(query, (*user_data, user_id))
        connection.commit()
        connection.close()

    def delete_data(self, user_ids):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "DELETE FROM Users WHERE UserID IN (%s)" % ','.join(['%s'] * len(user_ids))
        cursor.execute(query, user_ids)
        connection.commit()
        connection.close()

    def search_data(self, search_term):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UserID, FirstName, LastName, Username, Password, JobTitle, ClearanceLevel, Role FROM Users WHERE FirstName LIKE %s OR LastName LIKE %s OR Username LIKE %s"
        cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        connection.close()
        return results

    def open_add_data_window(self):
        layout = [
            [sg.Text('First Name'), sg.Input(key='-FIRST_NAME-')],
            [sg.Text('Last Name'), sg.Input(key='-LAST_NAME-')],
            [sg.Text('Username'), sg.Input(key='-USERNAME-')],
            [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
            [sg.Text('Job Title'), sg.Input(key='-JOB_TITLE-')],
            [sg.Text('Clearance Level'), sg.Combo(['TS', 'S', 'P', 'NA'], key='-CLEARANCE_LEVEL-')],
            [sg.Text('Role'), sg.Combo(['Admin', 'Owner', 'DataWriter'], key='-ROLE-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Add User Data', layout, modal=True)

    def open_edit_data_window(self, user_data):
        layout = [
            [sg.Text('First Name'), sg.Input(user_data['FirstName'], key='-FIRST_NAME-')],
            [sg.Text('Last Name'), sg.Input(user_data['LastName'], key='-LAST_NAME-')],
            [sg.Text('Username'), sg.Input(user_data['Username'], key='-USERNAME-')],
            [sg.Text('Password'), sg.Input(user_data['Password'], password_char='*', key='-PASSWORD-')],
            [sg.Text('Job Title'), sg.Input(user_data['JobTitle'], key='-JOB_TITLE-')],
            [sg.Text('Clearance Level'), sg.Combo(['TS', 'S', 'P', 'NA'], default_value=user_data['ClearanceLevel'], key='-CLEARANCE_LEVEL-')],
            [sg.Text('Role'), sg.Combo(['Admin', 'Owner', 'DataWriter'], default_value=user_data['Role'], key='-ROLE-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Edit User Data', layout, modal=True)



class OwnerDashboard:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def layout(self):
        return [
            [sg.Text('Owner Dashboard')],
            [sg.Table(values=[], headings=['DeviceID', 'PhoneNumber', 'SimCard'], key='-DEVICE_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            [sg.Button('View Authentication Factors'), sg.Button('View Smartphone Details')],
            [sg.Button('Logout')]
        ]

    def fetch_owner_devices(self, user_id):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DeviceID, PhoneNumber, SimCard FROM SmartPhones WHERE OwnerID = %s"
        cursor.execute(query, (user_id,))
        devices = cursor.fetchall()
        connection.close()
        return devices


class DataWriterDashboard:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def layout(self):
        return [
            [sg.Text('Data Writer Dashboard')],
            [sg.Input(key='-SEARCH-', enable_events=True), sg.Button('Search')],
            [sg.Button('Add Data')],
            [sg.Table(values=[],
                      headings=['UserID', 'FirstName', 'LastName', 'Username', 'JobTitle', 'ClearanceLevel', 'Role'],
                      key='-USER_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            [sg.Button('View Smartphones'), sg.Button('Logout')]
        ]

    def fetch_all_users(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UserID, FirstName, LastName, Username, JobTitle, ClearanceLevel, Role FROM Users"
        cursor.execute(query)
        users = cursor.fetchall()
        connection.close()
        return users

    def search_data(self, search_term):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UserID, FirstName, LastName, Username, Password, JobTitle, ClearanceLevel, Role FROM Users WHERE FirstName LIKE %s OR LastName LIKE %s OR Username LIKE %s"
        cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        connection.close()
        return results

    def open_add_data_window(self):
        layout = [
            [sg.Text('First Name'), sg.Input(key='-FIRST_NAME-')],
            [sg.Text('Last Name'), sg.Input(key='-LAST_NAME-')],
            [sg.Text('Username'), sg.Input(key='-USERNAME-')],
            [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
            [sg.Text('Job Title'), sg.Input(key='-JOB_TITLE-')],
            [sg.Text('Clearance Level'), sg.Combo(['TS', 'S', 'P', 'NA'], key='-CLEARANCE_LEVEL-')],
            [sg.Text('Role'), sg.Combo(['Admin', 'Owner', 'DataWriter'], key='-ROLE-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Add User Data', layout, modal=True)
