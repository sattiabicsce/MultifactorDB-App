import PySimpleGUI as sg

class AuthenticationFactorManagement:
    def __init__(self, db_connection, device_id, role):
        self.db_connection = db_connection
        self.device_id = device_id  # DeviceID is used to filter authentication factors
        self.role = role

    def layout(self):
        buttons = []
        if self.role == 'Admin':
            buttons = [sg.Button('Add Auth Factor'), sg.Button('Edit Auth Factor'), sg.Button('Delete Auth Factor'),
                       sg.Button('Pick Random Auth Factor')]
        elif self.role == 'DataWriter':
            buttons = [sg.Button('Add Auth Factor'), sg.Button('Pick Random Auth Factor')]
        return [
            [sg.Text(f"Authentication Factors for Device ID: {self.device_id}")],
            [sg.Table(values=[],
                      headings=['AuthFactorID', 'AuthFactorName', 'Security', 'Intrusiveness', 'Accuracy', 'Privacy'],
                      key='-AUTHFACTOR_TABLE-', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_EXTENDED)],
            buttons,
            [sg.Button('Back')]
        ]

    def fetch_auth_factors(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT AuthFactorID, AuthFactorName, Security, Intrusiveness, Accuracy, Privacy FROM AuthenticationFactor WHERE DeviceID = %s"
        cursor.execute(query, (self.device_id,))
        auth_factors = cursor.fetchall()
        connection.close()
        return auth_factors

    def add_auth_factor(self, auth_factor_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO AuthenticationFactor (AuthFactorName, Security, Intrusiveness, Accuracy, Privacy, Passive, Effort, UserPref, DeviceID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, auth_factor_data)
        connection.commit()
        connection.close()

    def edit_auth_factor(self, auth_factor_id, auth_factor_data):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "UPDATE AuthenticationFactor SET AuthFactorName=%s, Security=%s, Intrusiveness=%s, Accuracy=%s, Privacy=%s WHERE AuthFactorID=%s AND DeviceID=%s"
        cursor.execute(query, (*auth_factor_data, auth_factor_id, self.device_id))
        connection.commit()
        connection.close()

    def delete_auth_factors(self, auth_factor_ids):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        query = "DELETE FROM AuthenticationFactor WHERE AuthFactorID IN (%s) AND DeviceID = %s" % (','.join(['%s'] * len(auth_factor_ids)),)
        cursor.execute(query, (*auth_factor_ids, self.device_id))
        connection.commit()
        connection.close()

    def open_add_auth_factor_window(self):
        layout = [
            [sg.Text('Auth Factor Name'), sg.Input(key='-AUTH_FACTOR_NAME-')],
            [sg.Text('Security (1-10)'), sg.Input(key='-SECURITY-')],
            [sg.Text('Intrusiveness (1-10)'), sg.Input(key='-INTRUSIVENESS-')],
            [sg.Text('Accuracy (1-10)'), sg.Input(key='-ACCURACY-')],
            [sg.Text('Privacy (1-10)'), sg.Input(key='-PRIVACY-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Add Authentication Factor', layout, modal=True)

    def open_edit_auth_factor_window(self, auth_factor_data):
        layout = [
            [sg.Text('Auth Factor Name'), sg.Input(auth_factor_data['AuthFactorName'], key='-AUTH_FACTOR_NAME-')],
            [sg.Text('Security (1-10)'), sg.Input(auth_factor_data['Security'], key='-SECURITY-')],
            [sg.Text('Intrusiveness (1-10)'), sg.Input(auth_factor_data['Intrusiveness'], key='-INTRUSIVENESS-')],
            [sg.Text('Accuracy (1-10)'), sg.Input(auth_factor_data['Accuracy'], key='-ACCURACY-')],
            [sg.Text('Privacy (1-10)'), sg.Input(auth_factor_data['Privacy'], key='-PRIVACY-')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        return sg.Window('Edit Authentication Factor', layout, modal=True)
