import PySimpleGUI as sg

class SmartphoneDetailsManagement:
    def __init__(self, db_connection, device_id, role):
        self.db_connection = db_connection
        self.device_id = device_id
        self.role = role

    def layout(self):
        buttons = []
        if self.role == 'Admin':
            buttons = [sg.Button('Add Smartphone Details'), sg.Button('Edit Smartphone Details'), sg.Button('Delete Smartphone Details')]
        elif self.role == 'DataWriter':
            buttons = [sg.Button('Add Smartphone Details')]
        return [
            [sg.Text(f"Smartphone Details for Device ID: {self.device_id}")],
            [sg.Table(values=[], headings=['DetailID', 'Latitude', 'Longitude', 'CurrentIP', 'AvailableMemory', 'Battery'], key='-DETAILS_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            buttons,
            [sg.Button('Back')]
        ]

    def fetch_smartphone_details(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DetailID, Latitude, Longitude, CurrentIP, AvailableMemory, Battery FROM SmartPhoneDetails WHERE DeviceID = %s"
        cursor.execute(query, (self.device_id,))
        details = cursor.fetchall()
        connection.close()
        return details

    def add_smartphone_details(self, details_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO SmartPhoneDetails (DeviceID, Latitude, Longitude, CurrentIP, AvailableMemory, Battery) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, details_data)
        connection.commit()
        connection.close()

    def edit_smartphone_details(self, detail_id, details_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "UPDATE SmartPhoneDetails SET Latitude=%s, Longitude=%s, CurrentIP=%s, AvailableMemory=%s, Battery=%s WHERE DetailID=%s"
        cursor.execute(query, (*details_data, detail_id))
        connection.commit()
        connection.close()

    def delete_smartphone_details(self, detail_ids):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "DELETE FROM SmartPhoneDetails WHERE DetailID IN (%s)" % ','.join(['%s'] * len(detail_ids))
        cursor.execute(query, detail_ids)
        connection.commit()
        connection.close()

    def open_add_details_window(self):
        layout = [
            [sg.Text('Latitude'), sg.Input(key='-LATITUDE-')],
            [sg.Text('Longitude'), sg.Input(key='-LONGITUDE-')],
            [sg.Text('Current IP'), sg.Input(key='-CURRENT_IP-')],
            [sg.Text('Available Memory'), sg.Input(key='-AVAILABLE_MEMORY-')],
            [sg.Text('Battery (%)'), sg.Input(key='-BATTERY-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Add Smartphone Details', layout, modal=True)

    def open_edit_details_window(self, details_data):
        layout = [
            [sg.Text('Latitude'), sg.Input(details_data['Latitude'], key='-LATITUDE-')],
            [sg.Text('Longitude'), sg.Input(details_data['Longitude'], key='-LONGITUDE-')],
            [sg.Text('Current IP'), sg.Input(details_data['CurrentIP'], key='-CURRENT_IP-')],
            [sg.Text('Available Memory'), sg.Input(details_data['AvailableMemory'], key='-AVAILABLE_MEMORY-')],
            [sg.Text('Battery (%)'), sg.Input(details_data['Battery'], key='-BATTERY-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Edit Smartphone Details', layout, modal=True)
