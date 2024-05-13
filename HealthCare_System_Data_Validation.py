import PySimpleGUI as sg
import datetime
import sqlite3
import time
from datetime import date

""" Data Base Connexion and Creation"""
def Db_connexion(db):
    try:
        connexion = sqlite3.connect(db)
    finally:
        connexion.close()

def Create_table(db):
    try:
        connexion = sqlite3.connect(db)
        cursor = connexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Referencements(
                    Reference              TEXT DEFAULT "Aliou",
                    Reference_Patient      TEXT DEFAULT "1",
                    Reference_Doctor       TEXT DEFAULT "1",
                    Reference_Appointment  TEXT DEFAULT "1"
            )
            """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Patients(
                    Reference                INT,
                    Date                     TEXT,
                    Hour                     TEXT,
                    Id                       TEXT PRIMARY KEY,
                    Name                     TEXT,
                    Address                  TEXT,
                    DOB                      TEXT,
                    Sexe                     TEXT,
                    Medical_Condition        TEXT,
                    Phone_Number             TEXT,
                    Email                    TEXT, 
                    Emergency_Contact_Name   TEXT,
                    Emergency_Contact_Number TEXT,
                    Additional_Information   TEXT,
                    FOREIGN KEY (Reference) REFERENCES Referencements(Reference_Patient)
            )
            """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Doctors(
                    Reference              INT,
                    Date                     TEXT,
                    Hour                     TEXT,
                    Id                     TEXT PRIMARY KEY,
                    Name                   TEXT,
                    Specialisation         TEXT,
                    Level_Access           TEXT,
                    Phone_Number           TEXT,
                    Email                  TEXT, 
                    Additional_Information TEXT,
                    FOREIGN KEY (Reference) REFERENCES Referencements(Reference_Doctor)
            )
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Appointments(
                    Reference  INT,
                    Date                     TEXT,
                    Hour                     TEXT,
                    Id         TEXT PRIMARY KEY,
                    Patient_Id TEXT,
                    Doctor_Id  TEXT,
                    Date       TEXT,
                    Hour       TEXT,
                    Minute     TEXT,
                    Address    TEXT,
                    Repetition TEXT, 
                    Frequence  TEXT,
                    Over       TEXT,
                    Note       TEXT,
                    FOREIGN KEY (Patient_Id) REFERENCES Patients(Id),
                    FOREIGN KEY (Doctor_Id) REFERENCES Doctors(Id)
            )
            """)


        cursor.execute("""
            CREATE INDEX IF NOT EXISTS Index_Appointments_Patient_Id On Appointments(Patient_Id);
            """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS Index_Appointments_Doctor_Id On Appointments(Doctor_Id);
            """)

        
        connexion.commit()

    except sqlite3.Error as e:
        print("Error Creating Table:", e)
    finally:
        if connexion:
            connexion.close()

Data_Base = 'Test_Db.db'

Db_connexion(Data_Base)
Create_table(Data_Base)


"""Combo List """
Minutes            = [10, 15, 20, 25, 30, 45]
Repetition           = ["Week", "Month", "Year"]
Sex                = ["Femele", "Male", "Other"]
Frequence          = [num for num in range(1, 6)]
Hours              = [num for num in range(8, 18)]
Duration           = [num for num in range(1, 11)]
Level_Access       = ["Vistor", "Staff_L2", "Staff_L1", "Administrator"]
Specialisations    = ["General Practice", "Surgery", "Cardiology", "Dermatology", "Endocrinology", "Neurology", "Oncology", "Paediatrics", "Psychiatry", "Gastroenterology", "Specialist Nursery"]
Medical_Conditions = ["Emergency Patients", "Non-Emergency Patients", "Chronic Illness Patients", "Rehabilitation Patients", "Mental Health Patients", "Palliative Care Patients", "Preventive Care Patients", "Other"]


""" Error Messages"""

date = datetime.date.today()

""" Sharing Errors"""

error_name         = "Please enter a full name using alphabetical characters (A-Z or a-z)."
error_address      = "Address cannot be empty."
error_phone_number = "Phone number must be 11 digits not null."  
error_dob_1        = "Please select a date of birth using the DOB button."

""" Error Patient Registration"""

error_dob_2                    = f"Date of birth must be after 1899-12-31 and on or before today's date ({date})."
error_sex                      = "Please select a sex from the combo list (drop-down list)."
error_medical_condition        = "Please select a medical condition from the combo list (drop-down list)."
error_emergency_contact_name   = "Emergency contact name can be left empty. If provided, it must use alphabetical characters (A-Z or a-z)."
error_emergency_contact_number = "Emergency contact number can be left empty. If provided, it must be 11 digits."  


""" Error Doctor Registration"""

error_specialisation = "Please select a Doctor Specialisation from the combo list (drop-down list)."
error_level_access   = "Please select a Doctor Level Access from the combo list (drop-down list)."


""" Error Appointment Registration"""

error_date         = f"Appointment Date must be on or after today's ({date})."
error_repetition   = "Please select a Repetition from the combo list (drop-down list)."
error_hour         = "Please select the Appointment Hour from the combo list (drop-down list)."
error_minute       = "Please select the Appointment Minute from the combo list (drop-down list)."
error_frequence    = "Please select the Appointment Frequence from the combo list (drop-down list)."
error_over         = "Please select the Appointment Repetition End (Over) from the combo list (drop-down list)."



""" Patient Front-End """

Col1_Pt_Registration = sg.Column([[sg.Text('Patient Registration'),     sg.Text('Reference Number'), sg.Text('Patient ID')]]) 
Col2_Pt_Registration = sg.Column([[sg.Text('Full Name           '),     sg.Input(key = '-PtName-', size = (20, 1)), sg.Text('Phone Number                      '),           sg.Input(key = '-PtPhn-',   size = (22, 1))]])
Col3_Pt_Registration = sg.Column([[sg.Text('Address               '),   sg.Input(key = '-PtAdt-',  size = (20, 1)), sg.Text('Email*                                 '),     sg.Input(key = '-PtEmail-', size = (22, 1))]])
Col4_Pt_Registration = sg.Column([[sg.Text('Date of Birth        '),    sg.Input(key = '-PtDOB-',  size = (10, 1), readonly = True, enable_events = True),                 sg.CalendarButton('DOB', close_when_date_chosen = True, format = '%Y-%m-%d', key = '-Calendar_DOB-'), sg.Text('Emergency Contact Name*    '),               sg.Input(key = '-PtEcN-',   size = (22, 1))]])
Col5_Pt_Registration = sg.Column([[sg.Text('Sexe                    '), sg.Combo(key = '-PtSex-',  size = (18, 1), values = Sex, default_value = 'Select'), sg.Text('Emergency Contact Number*'),                sg.Input(key = '-PtEcnb-',  size = (22, 1))]])
Col6_Pt_Registration = sg.Column([[sg.Text('Medical Condition '),       sg.Combo(key = '-PtMdc-',  size = (18, 1), values = Medical_Conditions, default_value = 'Select'), sg.Text('Additional Information*          '),        sg.Input(key = '-PtAdi-',   size = (22, 2))]])
Col7_Pt_Registration = sg.Column([[sg.Button('Submit', key = '-Pt_Submit-'), sg.Button('Preview', key = '-Pt_Preview-')]])



Tb_Patient_Registration = [
    [Col1_Pt_Registration],
    [Col2_Pt_Registration],
    [Col3_Pt_Registration],
    [Col4_Pt_Registration],
    [Col5_Pt_Registration],
    [Col6_Pt_Registration],
    [Col7_Pt_Registration]
    ]


Col1_Pt_Displays = sg.Column([[sg.Button('Personal Info',         key = '-PtDPi-'),  sg.Text('Print Here the Patient personal Information. Note Some of this Information can be modify')]])
Col2_Pt_Displays = sg.Column([[sg.Button('Up-Coming Appointment', key = '-PtDApp-'), sg.Text('Print Here if upcoming Appointment.')]])
Col3_Pt_Displays = sg.Column([[sg.Button('Login Info',            key = '-PtDLi-'),  sg.Text('Print Here the login Information. Note: The Password can be change')]])


Tb_Patient_Display      = [
        [Col1_Pt_Displays],
        [Col2_Pt_Displays],
        [Col3_Pt_Displays]
                           ]

Tb_Patient_Modification = [[sg.Text('Modification')]]


TB_Patient_Bd = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Patient_Registration, key = '-TPtRg-'),
          sg.Tab('Display',      Tb_Patient_Display,      key = '-TPtDp-'),
          sg.Tab('Modification', Tb_Patient_Modification, key = '-TPtMd-')]], key = '-TPtBd-')
        
        ]
    ]

"""Doctor Front-End"""

Col1_Dr_Registration = sg.Column([[sg.Text('Doctor Registration'),  sg.Text('Reference Number'), sg.Text('Doctor ID')]]) 
Col2_Dr_Registration = sg.Column([[sg.Text('Full Name           '), sg.Input(key = '-DrName-',  size = (20, 1)),  sg.Text('Phone Number            '),             sg.Input(key = '-DrPhn-',   size = (22, 1))]])
Col3_Dr_Registration = sg.Column([[sg.Text('Specialisation      '), sg.Combo(key = '-DrSp-',          size = (18, 1), values = Specialisations, default_value = 'Select' ),  sg.Text('Email*                        '),       sg.Input(key = '-DrEmail-', size = (22, 1))]])
Col4_Dr_Registration = sg.Column([[sg.Text('Level Access      '),   sg.Combo(key = '-Drlva-',   size = (18, 1), values = Level_Access, default_value = 'Select'),  sg.Text('Additional Information* '),       sg.Input(key = '-DrAdi-',   size = (22, 2))]])
Col5_Dr_Registration = sg.Column([[sg.Button('Submit', key = '-Dr_Submit-'), sg.Button('Preview', key = '-Dr_Preview-')]])


Tb_Doctor_Registration = [
    [Col1_Dr_Registration],
    [Col2_Dr_Registration],
    [Col3_Dr_Registration],
    [Col4_Dr_Registration],
    [Col5_Dr_Registration]
    ]


Col1_Dr_Displays = sg.Column([[sg.Button('Personal Info',         key = '-DrDPi-'),  sg.Text('Print Here the Doctor personal Information. Note Some of this Information can be modify')]])
Col2_Dr_Displays = sg.Column([[sg.Button('Up-Coming Appointment', key = '-DrDApp-'), sg.Text('Print Here if upcoming Appointment.')]])
Col3_Dr_Displays = sg.Column([[sg.Button('Login Info',            key = '-DrDLi-'),  sg.Text('Print Here the login Information. Note: The Password can be change')]])


Tb_Doctor_Display      = [
        [Col1_Dr_Displays],
        [Col2_Dr_Displays],
        [Col3_Dr_Displays]
                         ]

Tb_Doctor_Modification = [[sg.Text('Modification')]]


TB_Doctor_Bd       = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Doctor_Registration, key = '-TDrRg-'),
          sg.Tab('Display',      Tb_Doctor_Display,      key = '-TDrDp-'),
          sg.Tab('Modification', Tb_Doctor_Modification, key = '-TDrMd-')]], key = '-TDrBd-')
        
        ]
    ]


"""Appointment Front-End"""

Col1_App_Registration = sg.Column([[sg.Text('Appointment Registration'),  sg.Text('Reference Number'), sg.Text('Appointment Code')]]) 
Col2_App_Registration = sg.Column([[sg.Text('Patient Id   '),  sg.Input(key = '-AppPtId-', size = (12, 1)), sg.Text('                 Doctor Id '),     sg.Input(key = '-AppDrId-',   size = (12, 1))]])
Col3_App_Registration = sg.Column([[sg.Text('Date          '), sg.Input(key = '-AppDate-', size = (12, 1),readonly = True, enable_events = True ),      sg.CalendarButton('Date', close_when_date_chosen = True, format = '%Y-%m-%d', key = '-Calendar_APT-') , sg.Text('Hour        ' ), sg.Combo(key = '-AppHour-',   size = (5, 1), values = Hours , default_value = 'Hours'), sg.Combo(key = '-AppMinute-', size = (5, 1), values = Minutes , default_value = 'Minute')]])
Col4_App_Registration = sg.Column([[sg.Text('Repetition  '),   sg.Combo(key = '-AppRep-',  size = (18, 1), values = Repetition, default_value = 'Select' ), sg.Text('   Frequence'),                    sg.Combo(key = '-AppFq-',     size = (6, 2), values = Frequence, default_value = 'Repeat' ), sg.Combo(key = '-AppFqQt-',   size = (6, 2), values = Duration, default_value = 'Over' )]])
Col5_App_Registration = sg.Column([[sg.Text('Adress      '),   sg.Input(key = '-AppAdt-',  size = (20, 1)), sg.Text('   Note*       '),                sg.Input(key = '-AppNote-',   size = (22, 3))]])
Col6_App_Registration = sg.Column([[sg.Button('Submit', key = '-App_Submit-'), sg.Button('Preview', key = '-App_Preview-')]])


Tb_Appointment_Registration = [
    [Col1_App_Registration],
    [Col2_App_Registration],
    [Col3_App_Registration],
    [Col4_App_Registration],
    [Col5_App_Registration],
    [Col6_App_Registration]
    ]

Col1_App_Displays = sg.Column([[sg.Button('All Appointment',       key = '-AppDAllApp-'),  sg.Text('Print Here All Appointment Registered.')]])
Col2_App_Displays = sg.Column([[sg.Button('Up-Coming Appointment', key = '-AppDApp-'),     sg.Text('Print Here if upcoming Appointment.')]])



Tb_Appointment_Display  = [
        [Col1_App_Displays],
        [Col2_App_Displays]
                         ]

Tb_Appointment_Modification = [[sg.Text('Modification')]]


TB_Appointment_Bd       = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Appointment_Registration, key = '-TAppRg-'),
          sg.Tab('Display',      Tb_Appointment_Display, key = '-TAppDp-'),
          sg.Tab('Modification', Tb_Appointment_Modification, key = '-TAppMd-')]], key = '-TAppBd-')
        
        ]
    ]


"""Research Front-End"""

Col01_Adc_Research = sg.Column([[sg.Text('Advenced research ')]])
Col02_Adc_Research = sg.Column([[sg.Text('Format   Appointment (0000)   Doctor (0000)   Patient (0000)     ')]])
Col03_Adc_Research = sg.Column([[sg.Text('Id   '),                     sg.Input(key = '-RshId-',      size = (12, 1)),  sg.Text(' Full Name '),     sg.Input(key = '-RshName-',      size = (20, 1))]])
Col04_Adc_Research = sg.Column([[sg.Text('If Appointment can be add                                If Doctor can be add                                If Patient can be add     ')]])
Col05_Adc_Research = sg.Column([[sg.Text('Medical Condition '),        sg.Combo(key = '-RshPtMdc0-',  size = (18, 1), values = Medical_Conditions, default_value = 'Select'),  sg.Text('Full Name     ' ), sg.Input(key = '-RshDrName1-',   size = (20, 1)),  sg.Text('Full Name           ' ),    sg.Input(key = '-RshPtName1-',   size = (20, 1))]])
Col06_Adc_Research = sg.Column([[sg.Text('Doctor Id              '),   sg.Input(key = '-RshDrId-',    size = (20, 1)),  sg.Text('Specialisation'),  sg.Combo(key = '-RshDrSp1-',     size = (18, 1), values = Specialisations , default_value = 'Select'),  sg.Text('Medical Condition'),        sg.Combo(key = '-RshPtMdc1-',    size = (18, 2), values = Medical_Conditions , default_value = 'Select')]])
Col07_Adc_Research = sg.Column([[sg.Text('Doctor Name        '),       sg.Input(key = '-RshDrName0-', size = (20, 1)),  sg.Text('Patient Ages  '),  sg.Input(key = '-RshPtAge-',     size = (5, 1))]])
Col08_Adc_Research = sg.Column([[sg.Text('Specialisation       '),     sg.Combo(key = '-RshDrSp0-',   size = (18, 1), values = Specialisations ,   default_value = 'Select')]])
Col09_Adc_Research = sg.Column([[sg.Text('Patient Id             '),   sg.Input(key = '-RshPtId-',    size = (20, 1))]])
Col10_Adc_Research = sg.Column([[sg.Text('Patient Name       '),       sg.Input(key = '-RshPtNme0-',  size = (20, 1))]])
Col11_Adc_Research = sg.Column([[sg.Text('Date                     '), sg.Input(readonly = True, enable_events = True, key = '-RshDate-',    size = (20, 1)), sg.CalendarButton('Appointment', close_when_date_chosen = True, format = '%d-%m-%Y', key = '-Calendar_RSH-')]])
Col12_Adc_Research = sg.Column([[sg.Button('Submit'), sg.Button('Preview')]])



TB_Research = [
    [Col01_Adc_Research],
    [Col02_Adc_Research],
    [Col03_Adc_Research],
    [Col04_Adc_Research],
    [Col05_Adc_Research],
    [Col06_Adc_Research],
    [Col07_Adc_Research],
    [Col08_Adc_Research],
    [Col09_Adc_Research],
    [Col10_Adc_Research],
    [Col11_Adc_Research],
    [Col12_Adc_Research]
    ]


"""Deletion Front-End"""

TB_Deletion        = [[sg.Text('Deletion')]]

"""Recovery Front-End"""

TB_Recovery        = [[sg.Text('Recovery')]]

"""User Control Front-End"""

TB_User_Control_Bd = [[sg.Text('User Control')]]

"""Information Front-End"""

TB_Information     = [[sg.Text('Information')]]

""" Main windows Front-End"""

Col1_Main_Window = sg.Column([[sg.Text('HealthCare Management System                                                                                                    '), sg.Text ('', key ='-Date-'), sg.Text ('', key ='-Clock-')]])

Sub_Tab = [
    [
        sg.Tab('Patient',      TB_Patient_Bd,      key = '-TbPatient-'),
        sg.Tab('Doctor',       TB_Doctor_Bd,       key = '-TbDoctor-'),
        sg.Tab('Appointment',  TB_Appointment_Bd,  key = '-TbAppointment-'),
        sg.Tab('Research',     TB_Research,        key = '-TbResearch-'),
        sg.Tab('Deletion',     TB_Deletion,        key = '-TbDeletion-'),
        sg.Tab('Recovery',     TB_Recovery,        key = '-TbRecovery-'),
        sg.Tab('User Control', TB_User_Control_Bd, key = '-TbControl-'),
        sg.Tab('Information',  TB_Information,     key = '-TbInformation-')
        ]
    ]


Main_Tab = [
        [Col1_Main_Window],
        [ sg.TabGroup(Sub_Tab, key = '-Sub_Tab-') ],
        [ sg.Button('Exit')]
    ]

window = sg.Window('HealthCare Management System', Main_Tab)


""" Registration Back-End"""

def Patient_Registration():

    Patient = {
        'Reference'                : Patient_reference,
        'Date'                     : str(date),
        'Hour'                     : str(hour),
        'Patient_id'               : 'PT0' + str(Patient_reference),
        'Patient_name'             : values['-PtName-'].title(),
        'Address'                  : values['-PtAdt-'],
        'DOB'                      : values['-PtDOB-'],
        'Sexe'                     : values['-PtSex-'],
        'Medical_Condition'        : values['-PtMdc-'],
        'Phone_Number'             : values['-PtPhn-'],
        'Email'                    : values['-PtEmail-'],
        'Emergency_Contact_name'   : values['-PtEcN-'],
        'Emergency_Contact_number' : values['-PtEcnb-'],
        'Additional_Information'   : values['-PtAdi-']
        }

    return Patient
    
def Doctor_Registration():

    Doctor = {
        'Reference'              : Doctor_reference,
        'Date'                   : str(date),
        'Hour'                   : str(hour),
        'Doctor_id'              : 'DC0' + str(Doctor_reference),
        'Doctor_name'            : values['-DrName-'].title(),
        'Specialisation'         : values['-DrSp-'],
        'Level_Access'           : values['-Drlva-'],
        'Phone_Number'           : values['-DrPhn-'],
        'Email'                  : values['-DrEmail-'],
        'Additional_Information' : values['-DrAdi-']
        }

    return Doctor

def Appointment_Registration():
    
    Appointment = {
        'Reference'        : Appointment_reference,
        'Date'             : str(date),
        'Hour'             : str(hour),
        'Appointment_id'   : 'APP0' + str(Appointment_reference),
        'Patient_id'       : values['-AppPtId-'],
        'Doctor_id'        : values['-AppDrId-'],
        'Appointment_Date' : values['-AppDate-'],
        'Appointment_Hour' : values['-AppHour-'],
        'Minute'           : values['-AppMinute-'],
        'Address'          : values['-AppAdt-'],
        'Repetition'       : values['-AppRep-'],
        'Frequence'        : values['-AppFq-'],
        'Over'             : values['-AppFqQt-'],
        'Note'             : values['-AppNote-']
        }

    return Appointment

""" Check Error Function"""

def checkError_name(user_input):
    if "".join(user_input.split()).isalpha() == True:
        return True
    else:
        return False

def checkError_phone_number(user_input):
    user_input = user_input.strip()
    if user_input.isdigit() and len(user_input) == 11 and int(user_input) > 0:
        return True
    else:
        return False


def checkError_emergency_contact_name(user_input):
    if user_input.strip():
        if "".join(user_input.split()).isalpha() == True:
            return True
        else:
            return False
    else:
        return True

def checkError_emergency_contact_number(user_input):
    user_input = user_input.strip()
    if user_input:
        if user_input.isdigit() and len(user_input) == 11 and int(user_input) > 0:
            return True
        else:
            return False
    else:
        return True


def checkError_DOB(Patient, user_input):
    try:
        user_input = date.fromisoformat(Patient['DOB'])
    except ValueError:
        print(ValueError)
    Reference_Date = date.fromisoformat("1900-01-01")
    Today = datetime.date.today()
    
    if Today < user_input or user_input < Reference_Date:
        return False
    else:
        return True


""" Data Validation (Check_Error from user input) """

def Error_Patient_Registration(Patient):
    Error_messages = []
    error = True
    
    if checkError_name(Patient['Patient_name']) is False:
        error *= checkError_name(Patient['Patient_name'])
        Error_messages.append(error_name)
      

    if not Patient['Address'].strip():
        error *= False
        Error_messages.append(error_address)
      
       
    if not Patient['DOB'].strip():
        error *= False
        Error_messages.append(error_dob_1)
      
    if Patient['DOB'].strip():       
        if checkError_DOB(Patient, Patient['DOB']) is False:
            error *= checkError_DOB(Patient, Patient['DOB'])
            Error_messages.append(error_dob_2)

    if Patient['Sexe'] not in Sex:
        error *= False
        Error_messages.append(error_sex)
       
        
    if Patient['Medical_Condition'] not in Medical_Conditions:
        error *= False
        Error_messages.append(error_medical_condition)
        

    if checkError_phone_number(Patient['Phone_Number']) is False:
        error *= checkError_phone_number(Patient['Phone_Number'])
        Error_messages.append(error_phone_number)
        

    if checkError_emergency_contact_name(Patient['Emergency_Contact_name']) is False:
        error *= checkError_emergency_contact_name(Patient['Emergency_Contact_name'])
        Error_messages.append(error_emergency_contact_name)
        

    if checkError_emergency_contact_number(Patient['Emergency_Contact_number']) is False:
        error *= checkError_emergency_contact_number(Patient['Emergency_Contact_number'])
        Error_messages.append(error_emergency_contact_number)
        

    if error != 1:
        Displays_Error_Messages(Error_messages)


    return error



def Error_Doctor_Registration(Doctor):
    Error_messages = []
    error = True
    
    if checkError_name(Doctor['Doctor_name']) is False:
        error *= checkError_name(Doctor['Doctor_name'])
        Error_messages.append(error_name)
      

    if Doctor['Specialisation'] not in Specialisations:
        error *= False
        Error_messages.append(error_specialisation)
       
        
    if Doctor['Level_Access'] not in Level_Access:
        error *= False
        Error_messages.append(error_level_access)
        

    if checkError_phone_number(Doctor['Phone_Number']) is False:
        error *= checkError_phone_number(Doctor['Phone_Number'])
        Error_messages.append(error_phone_number)
                

    if error != 1:
        Displays_Error_Messages(Error_messages)


    return error



def Error_Appointment_Registration(Appointment):
    Error_messages = []
    error = True
    

    if not Appointment['Address'].strip():
        error *= False
        Error_messages.append(error_address)
      
       
    if not Appointment['Date'].strip():
        error *= False
        Error_messages.append(error_date)
      

    if Appointment['Repetition'] not in Repetition:
        error *= False
        Error_messages.append(error_repetition)
       
        
    if Appointment['Hour'] not in Hours:
        error *= False
        Error_messages.append(error_hour)


    if Appointment['Minute'] not in Minutes :
        error *= False
        Error_messages.append(error_minute)


    if Appointment['Frequence'] not in Frequence:
        error *= False
        Error_messages.append(error_frequence)

    if Appointment['Over'] not in Duration:
        error *= False
        Error_messages.append(error_over)

                

    if error != 1:
        Displays_Error_Messages(Error_messages)


    return error


""" Displays Error Message in pop up"""

def Displays_Error_Messages(Error_messages):
    formatted_errors = []
    for i, error in enumerate(Error_messages, start = 1):
        formatted_errors.append(f"{i}.{error}")

    popup_message = "\n".join(formatted_errors)
    sg.popup("Errors: ", popup_message, title = "Error", non_blocking = True)

""" Displays Personal Data"""

def Displays_Patient_Data(Patient):
    print("--------------- Patient Data--------------- ")
    print(f"\nReference                    : {Patient['Reference']}                ")
    print(f"Date                         : {Patient['Date']}                       ")
    print(f"Hour                         : {Patient['Hour']}                       ")
    print(f"ID                           : {Patient['Patient_id']}                 ")
    print(f"Full Name                    : {Patient['Patient_name']}               ")
    print(f"Address                      : {Patient['Address']}                    ")
    print(f"DOB                          : {Patient['DOB']}                        ")
    print(f"Sex                          : {Patient['Sexe']}                       ")
    print(f"Medical Condition            : {Patient['Medical_Condition']}          ")
    print(f"Phone Number                 : {Patient['Phone_Number']}               ")
    print(f"Email                        : {Patient['Email']}                      ")
    print(f"Emergency Contact Name       : {Patient['Emergency_Contact_name']}     ")
    print(f"Emergency Contact Number     : {Patient['Emergency_Contact_number']}   ")
    print(f"Additional Information       : {Patient['Additional_Information']}     ")


def Displays_Doctor_Data(Doctor):
    print("--------- Doctor Detail------------                              ")
    print(f"\nReference                  : {Doctor['Reference']}            ")
    print(f"Date                       : {Doctor['Date']}                   ")
    print(f"Hour                       : {Doctor['Hour']}                   ")
    print(f"ID                         : {Doctor['Doctor_id']}              ")
    print(f"Name                       : {Doctor['Doctor_name']}            ")
    print(f"Specialisation             : {Doctor['Specialisation']}         ")
    print(f"Level Access               : {Doctor['Level_Access']}           ")
    print(f"Phone Number               : {Doctor['Phone_Number']}           ")
    print(f"Email                      : {Doctor['Email']}                  ")
    print(f"Additional Information     : {Doctor['Additional_Information']} ")


def Displays_Appointment_Data(Appointment): 
    print("--------- Appointment Detail------------                                         ")
    print(f"\nReference        : {Appointment['Reference']}                                 ")
    print(f"Date             : {Appointment['Date']}                                        ")
    print(f"Hour             : {Appointment['Hour']}                                        ")
    print(f"ID               : {Appointment['Appointment_id']}                              ")
    print(f"ID Patient       : {Appointment['Patient_id']}                                  ")
    print(f"ID Doctor        : {Appointment['Doctor_id']}                                   ")
    print(f"Appointment Date : {Appointment['Appointment_Date']}                            ")
    print(f"Appointment Hour : {Appointment['Appointment_Hour']}:{Appointment['Minute']}    ")
    print(f"Repetition       : {Appointment['Repetition']}                                  ")
    print(f"Frequence        : {Appointment['Frequence']}                                   ")
    print(f"Over             : {Appointment['Over']}                                        ")
    print(f"Note             : {Appointment['Note']}                                        ")


""" Import Referencements"""

def Referencements():
    connexion = sqlite3.connect(Data_Base)
    cursor = connexion.cursor()

    result = cursor.execute('SELECT * FROM Referencements LIMIT 1').fetchone()
    if not result:
        cursor.execute("INSERT INTO Referencements DEFAULT VALUES")
        connexion.commit()
        connexion.close()
        return 1, 1, 1
        
    else:
        ref = cursor.execute('SELECT * FROM Referencements WHERE ROWID IN (SELECT max(ROWID) FROM Referencements) ').fetchone()
        connexion.close()
        return int(ref[1]), int(ref[2]), int(ref[3])

Patient_reference, Doctor_reference, Appointment_reference = Referencements()

print(Patient_reference, Doctor_reference, Appointment_reference)



""" Submission Data"""

def Patient_Submission(Patient):
    connexion = sqlite3.connect(Data_Base)
    cursor = connexion.cursor()
    cursor.execute("UPDATE Referencements SET Reference_Patient = ? WHERE Reference = ?  ", (str(Patient_reference), "Aliou",  ))
    cursor.execute("INSERT INTO Patients(Reference, Date, Hour, Id, Name, Address, DOB, Sexe, Medical_Condition, Phone_Number, Email, Emergency_Contact_Name, Emergency_Contact_Number, Additional_Information) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (Patient['Reference'], Patient['Date'], Patient['Hour'], Patient['Patient_id'], Patient['Patient_name'], Patient['Address'], Patient['DOB'], Patient['Sexe'], Patient['Medical_Condition'], Patient['Phone_Number'], Patient['Email'], Patient['Emergency_Contact_name'], Patient['Emergency_Contact_number'], Patient['Additional_Information']))    
    
    connexion.commit()
    connexion.close()
    Displays_Patient_Data(Patient)


""" Events in each Tab"""

def Patient_Tab_Event():
    global Patient_reference
    SubTab_name = values['-TPtBd-']
    Patient = Patient_Registration()
    
    if SubTab_name == '-TPtRg-':
        if event == '-Pt_Preview-':
            Displays_Patient_Data(Patient)
        elif event == '-Pt_Submit-':
            if Error_Patient_Registration(Patient) == 1:
                Patient_reference = Patient['Reference'] + 1
                Patient_Submission(Patient)
                print(Patient_reference)
##            print(Error_Patient_Registration()
    elif SubTab_name == '-TPtDp-':
        if event == '-PtDPi-':
            Displays_Patient_Data(Patient)


def Doctor_Tab_Event():
    SubTab_name = values['-TDrBd-']
    Doctor = Doctor_Registration()
    
    if SubTab_name == '-TDrRg-':
        if event == '-Dr_Preview-':
            Displays_Doctor_Data(Doctor)
        elif event == '-Dr_Submit-':
            Error_Doctor_Registration(Doctor)
##            print(Error_Doctor_Registration()
    elif SubTab_name == '-TDrDp-':
        if event == '-DrDPi-':
            Displays_Doctor_Data(Doctor)


def Appointment_Tab_Event():
    pass



while True:
    event, values = window.read(timeout = 1000)
    date = datetime.date.today()
    hour = time.strftime('%H: %M: %S')
    print = sg.Print
    
    window['-Date-'].update(date.strftime('%d: %m: %Y'))
    window['-Clock-'].update(time.strftime('%H: %M: %S'))

    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if values is not None:
        Tab_name = values["-Sub_Tab-"]
            
    if Tab_name == '-TbPatient-':
        Patient_Tab_Event()
    
    elif Tab_name == '-TbDoctor-':
        Doctor_Tab_Event()        

    elif Tab_name == '-TbAppointment-':
        SubTab_name = values['-TAppBd-']
        Appointment = Appointment_Registration()

        if event == '-App_Preview-':
            Displays_Appointment_Data(Appointment)
        elif event == '-App_Submit-':
            Error_Appointment_Registration()
##            print(Error_Appointment_Registration())
            print(Appointment)


window.close()
    
