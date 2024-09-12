import PySimpleGUI as sg

class SmartphoneManagement:
    def __init__(self, db_connection, user_id, role):
        self.db_connection = db_connection
        self.user_id = user_id
        self.role = role

    def layout(self):
        buttons = []
        if self.role == 'Admin':
            buttons = [sg.Button('Add Smartphone'), sg.Button('Edit Smartphone'), sg.Button('Delete Smartphone')]
        elif self.role == 'DataWriter':
            buttons = [sg.Button('Add Smartphone')]
        return [
            [sg.Text(f"Smartphones for User ID: {self.user_id}")],
            [sg.Table(values=[], headings=['DeviceID', 'PhoneNumber', 'SimCard'], key='-SMARTPHONE_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            buttons,
            [sg.Button('View Authentication Factors'), sg.Button('View Smartphone Details')],
            [sg.Button('Back')]
        ]

    def fetch_smartphones(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DeviceID, PhoneNumber, SimCard FROM SmartPhones WHERE UserID = %s"
        cursor.execute(query, (self.user_id,))
        smartphones = cursor.fetchall()
        connection.close()
        return smartphones

    def fetch_smartphone_by_id(self, device_id):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DeviceID, PhoneNumber, SimCard FROM SmartPhones WHERE DeviceID = %s"
        cursor.execute(query, (device_id,))
        smartphone = cursor.fetchone()  # Fetches the single row that matches the DeviceID
        connection.close()
        return smartphone

    def add_smartphone(self, smartphone_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO SmartPhones (PhoneNumber, SimCard, UserID, OwnerID) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, smartphone_data)
        connection.commit()
        connection.close()

    def edit_smartphone(self, device_id, smartphone_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "UPDATE SmartPhones SET PhoneNumber=%s, SimCard=%s WHERE DeviceID=%s AND UserID=%s"
        cursor.execute(query, (*smartphone_data, device_id, self.user_id))
        connection.commit()
        connection.close()

    def delete_smartphones(self, device_ids):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "DELETE FROM SmartPhones WHERE DeviceID IN (%s)" % ','.join(['%s'] * len(device_ids))
        cursor.execute(query, device_ids)
        connection.commit()
        connection.close()

    def open_add_smartphone_window(self):
        layout = [
            [sg.Text('Phone Number'), sg.Input(key='-PHONE_NUMBER-')],
            [sg.Text('Sim Card (1 or 0)'), sg.Input(key='-SIM_CARD-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Add Smartphone', layout, modal=True)

    def open_edit_smartphone_window(self, smartphone_data):
        layout = [
            [sg.Text('Phone Number'), sg.Input(smartphone_data['PhoneNumber'], key='-PHONE_NUMBER-')],
            [sg.Text('Sim Card (1 or 0)'), sg.Input(smartphone_data['SimCard'], key='-SIM_CARD-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Edit Smartphone', layout, modal=True)
