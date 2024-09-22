import datetime
import sqlite3
from Classes.Appointment import Appointment

import Zermelo

# Create a connection to the database
conn = sqlite3.connect('../appointments.db                        ')
c = conn.cursor()

def ImportAppointments(user, startWeek, endWeek):
    list_of_appointments = Zermelo.get_appointments(startWeek, endWeek, user)
    print("Number of appointments: ", len(list_of_appointments))
    # Tables will now be per week, no longer per user
    # First, sort the appointments by week

    appointmentObjectList = {}
    for appointment in list_of_appointments:
        appointmentObject = Appointment(appointment)
        print(appointmentObject)
        week = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()[1]
        print("Week: ", week)
        if week in appointmentObjectList: appointmentObjectList[week].append(appointmentObject)
        else: appointmentObjectList[week] = [appointmentObject]
        print("Type: " + str(type(appointmentObjectList[week])))

    for week in appointmentObjectList:
        table = f""" CREATE TABLE IF NOT EXISTS '{week}' (
            id INTEGER PRIMARY KEY,
            appointmentInstance TEXT,
            start INTEGER,
            end INTEGER,
            startTimeSlot INTEGER,
            endTimeSlot INTEGER,
            branch TEXT,
            type TEXT,
            groupsInDepartments TEXT,
            locationsOfBranch TEXT,
            optional BOOLEAN,
            valid BOOLEAN,
            cancelled BOOLEAN,
            cancelledReason TEXT,
            modified BOOLEAN,
            teacherChanged BOOLEAN,
            groupChanged BOOLEAN,
            locationChanged BOOLEAN,
            timeChanged BOOLEAN,
            moved BOOLEAN,
            created INTEGER,
            hidden BOOLEAN,
            changeDescription TEXT,
            schedulerRemark TEXT,
            content TEXT,
            lastModified INTEGER,
            new BOOLEAN,
            choosableInDepartments TEXT,
            choosableInDepartmentCodes TEXT,
            extraStudentSource TEXT,
            onlineLocationUrl TEXT,
            expectedStudentCount INTEGER,
            expectedStudentCountOnline INTEGER,
            udmUUID TEXT,
            creator TEXT,
            onlineStudents TEXT,
            appointmentLastModified INTEGER,
            remark TEXT,
            availableSpace INTEGER,
            subjects TEXT,
            teachers TEXT,
            onlineTeachers TEXT
        ); """
        c.execute(table)
        print("Table created for week: ", week)
        print(appointmentObjectList[week])
        print(type(appointmentObjectList[week]))
        print(len(appointmentObjectList[week]))
        for appointmentObject in appointmentObjectList[week]:
            c.execute(f"INSERT OR REPLACE INTO '{week}' VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())
    conn.commit()

def close():
    conn.close()