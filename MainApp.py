from AuthenticationFactorManagement import AuthenticationFactorManagement
from Dashboard import AdminDashboard, OwnerDashboard, DataWriterDashboard
from DatabaseConnection import DatabaseConnection
from SmartphoneDetailsManagement import SmartphoneDetailsManagement
from SmartphoneManagement import SmartphoneManagement
from UserAuthentication import UserAuthentication
import PySimpleGUI as sg
import re

class MainApp:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.auth = UserAuthentication(db_connection)
        self.admin_dashboard = AdminDashboard(db_connection)
        self.data_writer_dashboard = DataWriterDashboard(db_connection)
        self.owner_dashboard = OwnerDashboard(db_connection)

    # Layout and input prompt for login with the buttons
    def login_window(self):
        layout = [
            [sg.Text('Username'), sg.Input(key='-USERNAME-')],
            [sg.Text('Password'), sg.Input(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login'), sg.Button('Exit')]
        ]
        return sg.Window('Login', layout)

    # Determines what layout to show upon login based on the role of user who logged in.
    def main_window(self, user):
        role = user['Role']
        layout = []

        if role == 'Admin':
            layout = self.admin_dashboard.layout()  # Call on instance, not class
        elif role == 'Owner':
            layout = self.owner_dashboard.layout()  # Call on instance, not class
        elif role == 'DataWriter':
            layout = self.data_writer_dashboard.layout()  # Call on instance, not class
        else:
            sg.popup('Unknown role!')

        return sg.Window('Smart Device Management', layout, finalize=True)

    # Handles all procedures within the smartphone dashboard for the admin and datawriter
    def smartphone_management_window(self, user_id, role):
        smartphone_management = SmartphoneManagement(self.db_connection, user_id, role)
        layout = smartphone_management.layout()
        window = sg.Window(f'Smartphone Management - User ID {user_id}', layout, finalize=True)

        smartphones = smartphone_management.fetch_smartphones()
        window['-SMARTPHONE_TABLE-'].update(
            values=[[s['DeviceID'], s['PhoneNumber'], s['SimCard']] for s in smartphones])

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Back':
                window.close()
                break

            if event == 'Add Smartphone' and role in ['Admin', 'DataWriter']:
                add_window = smartphone_management.open_add_smartphone_window()
                while True:
                    add_event, add_values = add_window.read()
                    if add_event == 'Submit':
                        # Validate that all required fields are filled
                        if not add_values['-PHONE_NUMBER-'] or not add_values['-SIM_CARD-']:
                            sg.popup("Please fill in all required fields.")
                            continue

                        # Validate phone number format (0)1234567890
                        phone_number = add_values['-PHONE_NUMBER-'].strip()
                        if not re.match(r"^\(\d\)\d{10}$", phone_number):
                            sg.popup("Invalid value entered: Phone number must be in the format (0)1234567890.")
                            continue

                        # Validate SimCard value is 0 or 1
                        sim_card_value = add_values['-SIM_CARD-'].strip()
                        if sim_card_value not in ['0', '1']:
                            sg.popup("Invalid value entered: SimCard must be either 0 or 1.")
                            continue

                        sim_card_value = int(sim_card_value)  # Convert SimCard to integer after validation

                        smartphone_data = (
                            phone_number, sim_card_value, user_id, user_id
                        )
                        smartphone_management.add_smartphone(smartphone_data)
                        smartphones = smartphone_management.fetch_smartphones()
                        window['-SMARTPHONE_TABLE-'].update(
                            values=[[s['DeviceID'], s['PhoneNumber'], s['SimCard']] for s in smartphones])
                        add_window.close()
                        break
                    elif add_event == 'Cancel' or add_event == sg.WINDOW_CLOSED:
                        add_window.close()
                        break

            elif event == 'Edit Smartphone' and role == 'Admin':
                selected_rows = values['-SMARTPHONE_TABLE-']
                if selected_rows:
                    device_id = smartphones[selected_rows[0]]['DeviceID']
                    smartphone_data = smartphone_management.fetch_smartphone_by_id(device_id)
                    edit_window = smartphone_management.open_edit_smartphone_window(smartphone_data)
                    while True:
                        edit_event, edit_values = edit_window.read()
                        if edit_event == 'Submit':
                            # Validate that all required fields are filled
                            if not edit_values['-PHONE_NUMBER-'] or not edit_values['-SIM_CARD-']:
                                sg.popup("Please fill in all required fields.")
                                continue

                            # Validate phone number format (0)1234567890
                            phone_number = edit_values['-PHONE_NUMBER-'].strip()
                            if not re.match(r"^\(\d\)\d{10}$", phone_number):
                                sg.popup("Invalid value entered: Phone number must be in the format (0)1234567890.")
                                continue

                            # Validate SimCard value is 0 or 1
                            sim_card_value = edit_values['-SIM_CARD-'].strip()
                            if sim_card_value not in ['0', '1']:
                                sg.popup("Invalid value entered: SimCard must be either 0 or 1.")
                                continue

                            sim_card_value = int(sim_card_value)  # Convert SimCard to integer after validation

                            updated_smartphone_data = (
                                phone_number, sim_card_value, device_id
                            )
                            smartphone_management.edit_smartphone(device_id, updated_smartphone_data)
                            smartphones = smartphone_management.fetch_smartphones()
                            window['-SMARTPHONE_TABLE-'].update(
                                values=[[s['DeviceID'], s['PhoneNumber'], s['SimCard']] for s in smartphones])
                            edit_window.close()
                            break
                        elif edit_event == 'Cancel' or edit_event == sg.WINDOW_CLOSED:
                            edit_window.close()
                            break

            elif event == 'Delete Smartphone' and role == 'Admin':
                selected_rows = values['-SMARTPHONE_TABLE-']
                if selected_rows:
                    device_ids = [smartphones[row]['DeviceID'] for row in selected_rows]
                    confirmation = sg.popup_yes_no("Are you sure you want to delete the selected smartphone(s)?")
                    if confirmation == 'Yes':
                        smartphone_management.delete_smartphones(device_ids)
                        smartphones = smartphone_management.fetch_smartphones()
                        window['-SMARTPHONE_TABLE-'].update(
                            values=[[s['DeviceID'], s['PhoneNumber'], s['SimCard']] for s in smartphones])

            elif event == 'View Authentication Factors':
                selected_rows = values['-SMARTPHONE_TABLE-']
                if selected_rows:
                    device_id = smartphones[selected_rows[0]]['DeviceID']
                    window.hide()
                    self.auth_factor_management_window(device_id, role)
                    window.un_hide()

            elif event == 'View Smartphone Details':
                selected_rows = values['-SMARTPHONE_TABLE-']
                if selected_rows:
                    device_id = smartphones[selected_rows[0]]['DeviceID']
                    window.hide()
                    self.smartphone_details_management_window(device_id, role)
                    window.un_hide()

    # Handles all procedures with auth factors when logged in as a admin or datawriter
    def auth_factor_management_window(self, device_id, role):
        auth_factor_management = AuthenticationFactorManagement(self.db_connection, device_id, role)
        layout = auth_factor_management.layout()
        window = sg.Window(f'Authentication Factor Management - Device ID {device_id}', layout, finalize=True)

        auth_factors = auth_factor_management.fetch_auth_factors()
        window['-AUTHFACTOR_TABLE-'].update(values=[[af['AuthFactorID'], af['AuthFactorName'], af['Security'], af['Intrusiveness'], af['Accuracy'], af['Privacy']] for af in auth_factors])

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Back':
                window.close()
                break
            if event == 'Add Auth Factor':
                add_window = auth_factor_management.open_add_auth_factor_window()
                while True:
                    add_event, add_values = add_window.read()
                    if add_event == 'Submit':
                        auth_factor_data = (
                            add_values['-AUTH_FACTOR_NAME-'], add_values['-SECURITY-'], add_values['-INTRUSIVENESS-'],
                            add_values['-ACCURACY-'], add_values['-PRIVACY-'], 0, 0, '', device_id  # Passing DeviceID with auth factor data
                        )
                        auth_factor_management.add_auth_factor(auth_factor_data)
                        auth_factors = auth_factor_management.fetch_auth_factors()
                        window['-AUTHFACTOR_TABLE-'].update(values=[[af['AuthFactorID'], af['AuthFactorName'], af['Security'], af['Intrusiveness'], af['Accuracy'], af['Privacy']] for af in auth_factors])
                        add_window.close()
                        break
                    elif add_event == 'Cancel' or add_event == sg.WINDOW_CLOSED:
                        add_window.close()
                        break
            elif event == 'Edit Auth Factor' and role == 'Admin':
                selected_rows = values['-AUTHFACTOR_TABLE-']
                if selected_rows:
                    auth_factor_id = auth_factors[selected_rows[0]]['AuthFactorID']
                    auth_factor_data = {
                        'AuthFactorName': auth_factors[selected_rows[0]]['AuthFactorName'],
                        'Security': auth_factors[selected_rows[0]]['Security'],
                        'Intrusiveness': auth_factors[selected_rows[0]]['Intrusiveness'],
                        'Accuracy': auth_factors[selected_rows[0]]['Accuracy'],
                        'Privacy': auth_factors[selected_rows[0]]['Privacy']
                    }
                    edit_window = auth_factor_management.open_edit_auth_factor_window(auth_factor_data)
                    while True:
                        edit_event, edit_values = edit_window.read()
                        if edit_event == 'Submit':
                            updated_auth_factor_data = (
                                edit_values['-AUTH_FACTOR_NAME-'], edit_values['-SECURITY-'], edit_values['-INTRUSIVENESS-'],
                                edit_values['-ACCURACY-'], edit_values['-PRIVACY-']
                            )
                            auth_factor_management.edit_auth_factor(auth_factor_id, updated_auth_factor_data)
                            auth_factors = auth_factor_management.fetch_auth_factors()
                            window['-AUTHFACTOR_TABLE-'].update(values=[[af['AuthFactorID'], af['AuthFactorName'], af['Security'], af['Intrusiveness'], af['Accuracy'], af['Privacy']] for af in auth_factors])
                            edit_window.close()
                            break
                        elif edit_event == 'Cancel' or edit_event == sg.WINDOW_CLOSED:
                            edit_window.close()
                            break
            elif event == 'Delete Auth Factor' and role == 'Admin':
                selected_rows = values['-AUTHFACTOR_TABLE-']
                if selected_rows:
                    auth_factor_ids = [auth_factors[row]['AuthFactorID'] for row in selected_rows]
                    auth_factor_management.delete_auth_factors(auth_factor_ids)
                    auth_factors = auth_factor_management.fetch_auth_factors()
                    window['-AUTHFACTOR_TABLE-'].update(values=[[af['AuthFactorID'], af['AuthFactorName'], af['Security'], af['Intrusiveness'], af['Accuracy'], af['Privacy']] for af in auth_factors])

            elif event == 'Pick Random Auth Factor':
                # Filter authentication factors based on the criteria
                valid_factors = [af for af in auth_factors if
                                 af['Security'] > 5 and af['Intrusiveness'] > 5 and af['Accuracy'] > 5 and af['Privacy'] > 5]
                if valid_factors:
                    # Pick a random authentication factor
                    import random
                    selected_factor = random.choice(valid_factors)
                    sg.popup(
                        f"Randomly selected Authentication Factor:\n\nID: {selected_factor['AuthFactorID']}\nName: {selected_factor['AuthFactorName']}\nSecurity: {selected_factor['Security']}\nIntrusiveness: {selected_factor['Intrusiveness']}\nAccuracy: {selected_factor['Accuracy']}\nPrivacy: {selected_factor['Privacy']}")
                else:
                    sg.popup("No authentication factors meet the criteria.")

    # Handles all procedures with the smartphone details when logged in as an admin and datawriter
    def smartphone_details_management_window(self, device_id, role):
        smartphone_details_management = SmartphoneDetailsManagement(self.db_connection, device_id, role)
        layout = smartphone_details_management.layout()
        window = sg.Window(f'Smartphone Details Management - Device ID {device_id}', layout, finalize=True)

        details = smartphone_details_management.fetch_smartphone_details()
        window['-DETAILS_TABLE-'].update(values=[[d['DetailID'], d['Latitude'], d['Longitude'], d['CurrentIP'], d['AvailableMemory'], d['Battery']] for d in details])

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Back':
                window.close()
                break
            if event == 'Add Smartphone Details':
                add_window = smartphone_details_management.open_add_details_window()
                while True:
                    add_event, add_values = add_window.read()
                    if add_event == 'Submit':
                        details_data = (
                            device_id, add_values['-LATITUDE-'], add_values['-LONGITUDE-'], add_values['-CURRENT_IP-'],
                            add_values['-AVAILABLE_MEMORY-'], add_values['-BATTERY-']
                        )
                        smartphone_details_management.add_smartphone_details(details_data)
                        details = smartphone_details_management.fetch_smartphone_details()
                        window['-DETAILS_TABLE-'].update(values=[[d['DetailID'], d['Latitude'], d['Longitude'], d['CurrentIP'], d['AvailableMemory'], d['Battery']] for d in details])
                        add_window.close()
                        break
                    elif add_event == 'Cancel' or add_event == sg.WINDOW_CLOSED:
                        add_window.close()
                        break
            elif event == 'Edit Smartphone Details' and role == 'Admin':
                selected_rows = values['-DETAILS_TABLE-']
                if selected_rows:
                    detail_id = details[selected_rows[0]]['DetailID']
                    details_data = {
                        'Latitude': details[selected_rows[0]]['Latitude'],
                        'Longitude': details[selected_rows[0]]['Longitude'],
                        'CurrentIP': details[selected_rows[0]]['CurrentIP'],
                        'AvailableMemory': details[selected_rows[0]]['AvailableMemory'],
                        'Battery': details[selected_rows[0]]['Battery']
                    }
                    edit_window = smartphone_details_management.open_edit_details_window(details_data)
                    while True:
                        edit_event, edit_values = edit_window.read()
                        if edit_event == 'Submit':
                            updated_details_data = (
                                edit_values['-LATITUDE-'], edit_values['-LONGITUDE-'], edit_values['-CURRENT_IP-'],
                                edit_values['-AVAILABLE_MEMORY-'], edit_values['-BATTERY-']
                            )
                            smartphone_details_management.edit_smartphone_details(detail_id, updated_details_data)
                            details = smartphone_details_management.fetch_smartphone_details()
                            window['-DETAILS_TABLE-'].update(values=[[d['DetailID'], d['Latitude'], d['Longitude'], d['CurrentIP'], d['AvailableMemory'], d['Battery']] for d in details])
                            edit_window.close()
                            break
                        elif edit_event == 'Cancel' or edit_event == sg.WINDOW_CLOSED:
                            edit_window.close()
                            break
            elif event == 'Delete Smartphone Details' and role == 'Admin':
                selected_rows = values['-DETAILS_TABLE-']
                if selected_rows:
                    detail_ids = [details[row]['DetailID'] for row in selected_rows]
                    smartphone_details_management.delete_smartphone_details(detail_ids)
                    details = smartphone_details_management.fetch_smartphone_details()
                    window['-DETAILS_TABLE-'].update(values=[[['DetailID'], d['Latitude'], d['Longitude'], d['CurrentIP'], d['AvailableMemory'], d['Battery']] for d in details])
            elif event == 'Delete Smartphone Details' and role == 'Admin':
                selected_rows = values['-DETAILS_TABLE-']
                if selected_rows:
                    detail_ids = [details[row]['DetailID'] for row in selected_rows]
                    smartphone_details_management.delete_smartphone_details(detail_ids)
                    details = smartphone_details_management.fetch_smartphone_details()
                    window['-DETAILS_TABLE-'].update(values=[[d['DetailID'], d['Latitude'], d['Longitude'], d['CurrentIP'], d['AvailableMemory'], d['Battery']] for d in details])

    def run(self):
        login_win = self.login_window()

        while True:
            event, values = login_win.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            if event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                user = self.auth.authenticate_user(username, password)
                if user:
                    login_win.close()
                    # Determining which dashboard appears based on role
                    if user['Role'] == 'Admin':
                        main_win = self.main_window(user)
                        users = self.admin_dashboard.fetch_all_users()
                        main_win['-USER_TABLE-'].update(values=[
                            [u['UserID'], u['FirstName'], u['LastName'], u['Username'], u['JobTitle'],
                             u['ClearanceLevel'], u['Role']] for u in users])
                    elif user['Role'] == 'Owner':
                        layout = self.owner_dashboard.layout()
                        main_win = sg.Window('Owner Dashboard', layout, finalize=True)
                        devices = self.owner_dashboard.fetch_owner_devices(user['UserID'])
                        main_win['-DEVICE_TABLE-'].update(
                            values=[[d['DeviceID'], d['PhoneNumber'], d['SimCard']] for d in devices])
                    elif user['Role'] == 'DataWriter':
                        main_win = self.main_window(user)
                        users = self.data_writer_dashboard.fetch_all_users()  # Fetch users for DataWriter
                        main_win['-USER_TABLE-'].update(values=[
                            [u['UserID'], u['FirstName'], u['LastName'], u['Username'], u['JobTitle'],
                             u['ClearanceLevel'], u['Role']] for u in users])

                    while True:
                        main_event, main_values = main_win.read()
                        if main_event == sg.WINDOW_CLOSED or main_event == 'Logout':
                            main_win.close()
                            login_win = self.login_window()
                            break
                        # Search button being clicked
                        if main_event == 'Search':
                            search_term = main_values['-SEARCH-']
                            if user['Role'] == 'Admin':
                                results = self.admin_dashboard.search_data(search_term)
                            elif user['Role'] == 'DataWriter':
                                results = self.data_writer_dashboard.search_data(search_term)

                            main_win['-USER_TABLE-'].update(values=[
                                [r['UserID'], r['FirstName'], r['LastName'], r['Username'], r['JobTitle'],
                                 r['ClearanceLevel'], r['Role']] for r in results])
                        # Determines what user ID to use based on which user was clicked
                        if main_event == 'View Smartphones' and user['Role'] in ['Admin', 'Owner', 'DataWriter']:
                            selected_rows = main_values['-USER_TABLE-'] if user['Role'] == 'Admin' or 'DataWriter' else main_values[
                                '-DEVICE_TABLE-']
                            if selected_rows:
                                if user['Role'] == 'Admin' or 'DataWriter':
                                    user_id = users[selected_rows[0]]['UserID']
                                else:
                                    user_id = user['UserID']
                                main_win.hide()
                                self.smartphone_management_window(user_id, user['Role'])
                                main_win.un_hide()

                        # Opens the add data window on click and submits data or cancels addition based on what is clicked.
                        if main_event == 'Add Data' and user['Role'] == 'Admin':
                            add_window = self.admin_dashboard.open_add_data_window()
                            while True:
                                add_event, add_values = add_window.read()
                                if add_event == 'Submit':
                                    user_data = (
                                        add_values['-FIRST_NAME-'], add_values['-LAST_NAME-'], add_values['-USERNAME-'],
                                        add_values['-PASSWORD-'], add_values['-JOB_TITLE-'],
                                        add_values['-CLEARANCE_LEVEL-'],
                                        add_values['-ROLE-']
                                    )
                                    self.admin_dashboard.add_data(user_data)
                                    users = self.admin_dashboard.fetch_all_users()
                                    main_win['-USER_TABLE-'].update(values=[
                                        [u['UserID'], u['FirstName'], u['LastName'], u['Username'], u['JobTitle'],
                                         u['ClearanceLevel'], u['Role']] for u in users])
                                    add_window.close()
                                    break
                                elif add_event == 'Cancel' or add_event == sg.WINDOW_CLOSED:
                                    add_window.close()
                                    break
                        # Gets the data from the highlighted user and opens up the edit data window with the data
                        # already filled in.
                        elif main_event == 'Edit Data' and user['Role'] == 'Admin':
                            selected_rows = main_values['-USER_TABLE-']
                            if selected_rows:
                                user_id = users[selected_rows[0]]['UserID']
                                user_data = {
                                    'FirstName': users[selected_rows[0]]['FirstName'],
                                    'LastName': users[selected_rows[0]]['LastName'],
                                    'Username': users[selected_rows[0]]['Username'],
                                    'Password': users[selected_rows[0]]['Password'],
                                    'JobTitle': users[selected_rows[0]]['JobTitle'],
                                    'ClearanceLevel': users[selected_rows[0]]['ClearanceLevel'],
                                    'Role': users[selected_rows[0]]['Role']
                                }
                                edit_window = self.admin_dashboard.open_edit_data_window(user_data)
                                while True:
                                    edit_event, edit_values = edit_window.read()
                                    if edit_event == 'Submit':
                                        user_data = (
                                            edit_values['-FIRST_NAME-'], edit_values['-LAST_NAME-'],
                                            edit_values['-USERNAME-'],
                                            edit_values['-PASSWORD-'], edit_values['-JOB_TITLE-'],
                                            edit_values['-CLEARANCE_LEVEL-'],
                                            edit_values['-ROLE-']
                                        )
                                        self.admin_dashboard.edit_data(user_id, user_data)
                                        users = self.admin_dashboard.fetch_all_users()
                                        main_win['-USER_TABLE-'].update(values=[
                                            [u['UserID'], u['FirstName'], u['LastName'], u['Username'], u['JobTitle'],
                                             u['ClearanceLevel'], u['Role']] for u in users])
                                        edit_window.close()
                                        break
                                    elif edit_event == 'Cancel' or edit_event == sg.WINDOW_CLOSED:
                                        edit_window.close()
                                        break
                        # Deletes the selected user
                        elif main_event == 'Delete Data' and user['Role'] == 'Admin':
                            selected_rows = main_values['-USER_TABLE-']
                            if selected_rows:
                                user_ids = [users[row]['UserID'] for row in selected_rows]
                                self.admin_dashboard.delete_data(user_ids)
                                users = self.admin_dashboard.fetch_all_users()
                                main_win['-USER_TABLE-'].update(values=[
                                    [u['UserID'], u['FirstName'], u['LastName'], u['Username'], u['JobTitle'],
                                     u['ClearanceLevel'], u['Role']] for u in users])
                        # Handles adding a user as a datawriter
                        elif main_event == 'Add Data' and user['Role'] == 'DataWriter':
                            add_window = self.data_writer_dashboard.open_add_data_window()
                            while True:
                                add_event, add_values = add_window.read()
                                if add_event == 'Submit':
                                    device_data = (
                                        add_values['-PHONE_NUMBER-'], add_values['-SIM_CARD-'], add_values['-USER_ID-'],
                                        add_values['-OWNER_ID-']
                                    )
                                    self.data_writer_dashboard.add_data(device_data)
                                    devices = self.data_writer_dashboard.fetch_all_devices()
                                    main_win['-DEVICE_TABLE-'].update(values=[list(d.values()) for d in devices])
                                    add_window.close()
                                    break
                                elif add_event == 'Cancel' or add_event == sg.WINDOW_CLOSED:
                                    add_window.close()
                                    break
                        # Handles viewing of auth factors and details by owners using the device id
                        elif main_event in ['View Authentication Factors', 'View Smartphone Details'] and user[
                            'Role'] == 'Owner':
                            selected_rows = main_values['-DEVICE_TABLE-']
                            if selected_rows:
                                device_id = devices[selected_rows[0]]['DeviceID']
                                main_win.hide()
                                if main_event == 'View Authentication Factors':
                                    self.auth_factor_management_window(device_id, user['Role'])
                                else:
                                    self.smartphone_details_management_window(device_id, user['Role'])
                                main_win.un_hide()
                else:
                    sg.popup('Login Failed')

        login_win.close()

# Connection to the sql database
if __name__ == "__main__":
    db_conn = DatabaseConnection(host='localhost', user='root', password='aa11632LX1$', database='SmartDeviceManagement')
    app = MainApp(db_conn)
    app.run()
