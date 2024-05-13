import PySimpleGUI as sg
import datetime
import sqlite3
import time


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
                    Reference_Patient      INT,
                    Reference_Doctor       INT,
                    Reference_Appointment  INT
            )
            """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Patients(
                    Reference                INT,
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


Tb_Patient_Display      = [[sg.Text('Display')]]

Tb_Patient_Modification = [[sg.Text('Modification')]]


TB_Patient_Bd = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Patient_Registration, key = '-TPtRg-'),
          sg.Tab('Display', Tb_Patient_Display, key = '-TPtDp-'),
          sg.Tab('Modification', Tb_Patient_Modification, key = '-TPtMd-')]])
        
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

Tb_Doctor_Display      = [[sg.Text('Display')]]

Tb_Doctor_Modification = [[sg.Text('Modification')]]


TB_Doctor_Bd       = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Doctor_Registration, key = '-TDrRg-'),
          sg.Tab('Display', Tb_Doctor_Display, key = '-TDrDp-'),
          sg.Tab('Modification', Tb_Doctor_Modification, key = '-TDrMd-')]])
        
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

Tb_Appointment_Display      = [[sg.Text('Display')]]

Tb_Appointment_Modification = [[sg.Text('Modification')]]


TB_Appointment_Bd       = [
    [
      sg.TabGroup([[
          sg.Tab('Registration', Tb_Appointment_Registration, key = '-TDrRg-'),
          sg.Tab('Display', Tb_Appointment_Display, key = '-TDrDp-'),
          sg.Tab('Modification', Tb_Appointment_Modification, key = '-TDrMd-')]])
        
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

    Patient_reference = 0

    Patient = {
        'Reference'                : Patient_reference + 1,
        'Patient_id'               : 'PT0' + str(Patient_reference + 1),
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

    Doctor_reference = 0

    Doctor = {
        'Reference'              : Doctor_reference + 1,
        'Doctor_id'              : 'DC0' + str(Doctor_reference + 1),
        'Doctor_name'            : values['-DrName-'].title(),
        'Specialisation'         : values['-DrSp-'],
        'Level_Access'           : values['-Drlva-'],
        'Phone_Number'           : values['-DrPhn-'],
        'Email'                  : values['-DrEmail-'],
        'Additional_Information' : values['-DrAdi-']
        }

    return Doctor

def Appointment_Registration():
    
    Appointment_reference = 0
    
    Appointment = {
        'Reference'      : Appointment_reference + 1,
        'Appointment_id' : 'APP0' + str(Appointment_reference + 1),
        'Patient_id'     : values['-AppPtId-'],
        'Doctor_id'      : values['-AppDrId-'],
        'Date'           : values['-AppDate-'],
        'Hour'           : values['-AppHour-'],
        'Minute'         : values['-AppMinute-'],
        'Address'        : values['-AppAdt-'],
        'Repetition'     : values['-AppRep-'],
        'Frequence'      : values['-AppFq-'],
        'Over'           : values['-AppFqQt-'],
        'Note'           : values['-AppNote-']
        }

    return Appointment




while True:
    event, values = window.read(timeout = 1000)
    date = datetime.date.today()
    hour = time.strftime('%H: %M: %S')

    
    window['-Date-'].update(date.strftime('%d: %m: %Y'))
    window['-Clock-'].update(time.strftime('%H: %M: %S'))

    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if values is not None:
        Tab_name = values["-Sub_Tab-"]
            

    if Tab_name == '-TbPatient-':
        Patient = Patient_Registration()

        if event == '-Pt_Preview-':
            print(Patient)
            
    elif Tab_name == '-TbDoctor-':
        Doctor = Doctor_Registration()

        if event == '-Dr_Preview-':
            print(Doctor)
        
    elif Tab_name == '-TbAppointment-':
        Appointment = Appointment_Registration()

        if event == '-App_Preview-':
            print(Appointment)


window.close()
    
